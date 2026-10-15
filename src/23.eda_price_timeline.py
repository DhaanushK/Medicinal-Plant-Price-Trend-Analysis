
from pathlib import Path
import re
import pandas as pd


# --------------------------------------------------
# 1. DEFINE PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "medicinal_plant_prices_analytical.csv"
)

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

TIMELINE_FILE = REPORT_DIR / "eda_step09_price_timeline.csv"
SUMMARY_FILE = REPORT_DIR / "eda_step09_timeline_summary.csv"


# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

df = pd.read_csv(
    INPUT_FILE,
    dtype=str,
    keep_default_na=False,
)

required_columns = [
    "botanical_name_part",
    "trade_name_part",
    "market",
    "source_year",
    "source_sheet",
    "analytical_price",
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")


# --------------------------------------------------
# 3. NORMALIZE WORKSHEET LABELS
# --------------------------------------------------

# Normalize whitespace for parsing only.
# The original source_sheet column remains unchanged.
def parse_worksheet_label(label):
    normalized = re.sub(r"\s+", " ", label.strip())

    # Accept month names such as Sep, Sept, or September.
    match = re.fullmatch(
        r"([A-Za-z]+)\s+(\d{4})\s*-\s*(1|2)",
        normalized,
    )

    if not match:
        return pd.Series({
            "parsed_month": "",
            "parsed_year": pd.NA,
            "fortnight_suffix": "",
            "period_start": pd.NaT,
            "period_parse_status": "Unparsed label",
        })

    month_text, year_text, suffix = match.groups()

    month_lookup = {
        "jan": 1, "january": 1,
        "feb": 2, "february": 2,
        "mar": 3, "march": 3,
        "apr": 4, "april": 4,
        "may": 5,
        "jun": 6, "june": 6,
        "jul": 7, "july": 7,
        "aug": 8, "august": 8,
        "sep": 9, "sept": 9, "september": 9,
        "oct": 10, "october": 10,
        "nov": 11, "november": 11,
        "dec": 12, "december": 12,
    }

    month_number = month_lookup.get(month_text.lower())

    if month_number is None:
        return pd.Series({
            "parsed_month": "",
            "parsed_year": int(year_text),
            "fortnight_suffix": suffix,
            "period_start": pd.NaT,
            "period_parse_status": "Unknown month",
        })

    # Use the first day of the month as a sortable month key.
    period_start = pd.Timestamp(
        year=int(year_text),
        month=month_number,
        day=1,
    )

    return pd.Series({
        "parsed_month": month_number,
        "parsed_year": int(year_text),
        "fortnight_suffix": suffix,
        "period_start": period_start,
        "period_parse_status": "Parsed",
    })


parsed = df["source_sheet"].apply(parse_worksheet_label)
df = pd.concat([df, parsed], axis=1)


# --------------------------------------------------
# 4. RESOLVE FORTNIGHT LABELS
# --------------------------------------------------

# Determine which suffixes exist for each calendar month.
month_keys = ["parsed_year", "parsed_month"]

valid_month_rows = df[df["period_parse_status"] == "Parsed"]

suffixes_by_month = (
    valid_month_rows.groupby(month_keys)["fortnight_suffix"]
    .agg(lambda values: set(values))
    .to_dict()
)


def resolve_fortnight(row):
    if row["period_parse_status"] != "Parsed":
        return "Unresolved"

    suffixes = suffixes_by_month.get(
        (row["parsed_year"], row["parsed_month"]),
        set(),
    )

    suffix = row["fortnight_suffix"]

    if suffixes == {"1", "2"}:
        return "Second fortnight" if suffix == "1" else "First fortnight"

    if suffixes == {"1"}:
        return "First fortnight"

    # A suffix of -2 alone does not identify a fortnight
    # under the project's agreed rule.
    return "Unresolved"


df["fortnight_resolution"] = df.apply(
    resolve_fortnight,
    axis=1,
)


# --------------------------------------------------
# 5. PREPARE PLANT, MARKET, AND PRICE FIELDS
# --------------------------------------------------

df["plant_identifier"] = (
    df["botanical_name_part"].str.strip()
    + " | "
    + df["trade_name_part"].str.strip()
)

df["numeric_price"] = pd.to_numeric(
    df["analytical_price"],
    errors="coerce",
)

df["source_year_numeric"] = pd.to_numeric(
    df["source_year"],
    errors="coerce",
)

df["has_positive_price"] = df["numeric_price"] > 0


# --------------------------------------------------
# 6. CREATE THE DETAILED TIMELINE
# --------------------------------------------------

# Retain one row per original observation.
# Unresolved periods remain visible instead of being guessed.
timeline_columns = [
    "plant_identifier",
    "market",
    "source_year",
    "source_sheet",
    "parsed_year",
    "parsed_month",
    "period_start",
    "fortnight_suffix",
    "fortnight_resolution",
    "period_parse_status",
    "analytical_price",
    "numeric_price",
    "has_positive_price",
]

timeline = df[timeline_columns].copy()

timeline = timeline.sort_values(
    [
        "plant_identifier",
        "market",
        "period_start",
        "fortnight_resolution",
        "source_sheet",
    ],
    na_position="last",
)

timeline.to_csv(
    TIMELINE_FILE,
    index=False,
    encoding="utf-8-sig",
)


# --------------------------------------------------
# 7. SUMMARIZE TIMELINE COVERAGE
# --------------------------------------------------

# Count only distinct original worksheet labels as reporting periods.
summary = (
    timeline.groupby(["plant_identifier", "market"])
    .agg(
        total_observations=("source_sheet", "size"),
        distinct_source_sheets=("source_sheet", "nunique"),
        distinct_months=("period_start", "nunique"),
        distinct_years=("source_year", "nunique"),
        positive_price_observations=("has_positive_price", "sum"),
        parsed_observations=("period_parse_status",
                             lambda values: (values == "Parsed").sum()),
        unresolved_fortnight_observations=(
            "fortnight_resolution",
            lambda values: (values == "Unresolved").sum(),
        ),
    )
    .reset_index()
)

summary.to_csv(
    SUMMARY_FILE,
    index=False,
    encoding="utf-8-sig",
)


# --------------------------------------------------
# 8. PRINT VALIDATION AND SUMMARY
# --------------------------------------------------

print("=" * 70)
print("EDA STEP 9.2: PRICE TIMELINE")
print("=" * 70)

print(f"Total observations: {len(timeline):,}")
print(
    "Parsed worksheet observations: "
    f"{(timeline['period_parse_status'] == 'Parsed').sum():,}"
)
print(
    "Unparsed worksheet observations: "
    f"{(timeline['period_parse_status'] != 'Parsed').sum():,}"
)
print(
    "Unresolved fortnight observations: "
    f"{(timeline['fortnight_resolution'] == 'Unresolved').sum():,}"
)

print("\nFortnight resolution counts:")
print(timeline["fortnight_resolution"].value_counts().to_string())

print("\nPairs with the most distinct months:")
print(
    summary.sort_values(
        ["distinct_months", "positive_price_observations"],
        ascending=False,
    )
    .head(10)
    .to_string(index=False)
)

print("\nReports saved:")
print(TIMELINE_FILE)
print(SUMMARY_FILE)

print("\nThe original analytical dataset was not modified.")
