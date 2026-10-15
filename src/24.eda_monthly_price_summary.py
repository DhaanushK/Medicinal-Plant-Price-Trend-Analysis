
from pathlib import Path
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

OUTPUT_FILE = REPORT_DIR / "eda_step09_monthly_price_summary.csv"


# --------------------------------------------------
# 2. LOAD THE ANALYTICAL DATASET
# --------------------------------------------------

df = pd.read_csv(
    INPUT_FILE,
    dtype=str,
    keep_default_na=False,
)

# Convert prices temporarily for numerical analysis.
df["numeric_price"] = pd.to_numeric(
    df["analytical_price"],
    errors="coerce",
)

# Use the normalized month and year from the worksheet label.
# This follows the validated parsing rules from Step 9.2.
parsed = df["source_sheet"].str.strip().str.replace(
    r"\s+", " ", regex=True
)

period_parts = parsed.str.extract(
    r"^(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|"
    r"Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|"
    r"Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+"
    r"(\d{4})\s*-\s*[12]$",
    flags=0,
    expand=True,
)

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

df["parsed_month"] = (
    period_parts[0].str.lower().map(month_lookup)
)

df["parsed_year"] = pd.to_numeric(
    period_parts[1],
    errors="coerce",
)

if df["parsed_month"].isna().any() or df["parsed_year"].isna().any():
    raise ValueError(
        "Some worksheet labels could not be parsed. "
        "Check the source_sheet values before continuing."
    )

# Build a calendar month key for grouping.
df["calendar_month"] = pd.to_datetime(
    {
        "year": df["parsed_year"].astype(int),
        "month": df["parsed_month"].astype(int),
        "day": 1,
    }
)


# --------------------------------------------------
# 3. PREPARE PLANT AND MARKET IDENTIFIERS
# --------------------------------------------------

df["plant_identifier"] = (
    df["botanical_name_part"].str.strip()
    + " | "
    + df["trade_name_part"].str.strip()
)

# Positive prices only; missing and ambiguous values are excluded.
prices = df[df["numeric_price"] > 0].copy()


# --------------------------------------------------
# 4. SUMMARIZE MONTHLY PRICES
# --------------------------------------------------

group_columns = [
    "plant_identifier",
    "market",
    "calendar_month",
]

monthly = (
    prices.groupby(group_columns)
    .agg(
        positive_price_observations=("numeric_price", "count"),
        median_price=("numeric_price", "median"),
        minimum_price=("numeric_price", "min"),
        maximum_price=("numeric_price", "max"),
        distinct_source_sheets=("source_sheet", "nunique"),
    )
    .reset_index()
)

# Add year and month as separate fields for reporting.
monthly["year"] = monthly["calendar_month"].dt.year
monthly["month"] = monthly["calendar_month"].dt.month

monthly = monthly.sort_values(
    ["plant_identifier", "market", "calendar_month"]
)


# --------------------------------------------------
# 5. SAVE AND PRINT RESULTS
# --------------------------------------------------

monthly.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig",
)

print("=" * 70)
print("EDA STEP 9.3: MONTHLY PRICE SUMMARY")
print("=" * 70)

print(f"Positive price observations: {len(prices):,}")
print(f"Plant-market-month groups: {len(monthly):,}")
print(
    "Unique plant-market pairs: "
    f"{monthly[['plant_identifier', 'market']].drop_duplicates().shape[0]:,}"
)

print("\nMonthly groups by year:")
print(
    monthly.groupby("year")
    .agg(
        observed_plant_market_months=("calendar_month", "size"),
        positive_price_observations=("positive_price_observations", "sum"),
    )
    .to_string()
)

print("\nExample: Acorus calamus Root in Kolkata")
example = monthly[
    monthly["plant_identifier"].str.startswith("Acorus calamus-Root | Bach-Root")
    & (monthly["market"] == "Kolkata")
]

print(example.to_string(index=False))

print("\nReport saved:")
print(OUTPUT_FILE)

print("\nNo missing months were filled and no source values were modified.")
