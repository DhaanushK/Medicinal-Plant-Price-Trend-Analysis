
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

OUTPUT_FILE = REPORT_DIR / "eda_step09_trend_readiness.csv"


# --------------------------------------------------
# 2. LOAD THE ANALYTICAL DATASET
# --------------------------------------------------

# Read values as strings to avoid changing source notation.
df = pd.read_csv(
    INPUT_FILE,
    dtype=str,
    keep_default_na=False,
)

print("=" * 70)
print("EDA STEP 9.1: PRICE TREND READINESS")
print("=" * 70)

print(f"Dataset rows: {len(df):,}")
print(f"Dataset columns: {len(df.columns)}")


# --------------------------------------------------
# 3. IDENTIFY THE REPORTING-PERIOD COLUMN
# --------------------------------------------------

# Prefer a standardized reporting period where available.
period_candidates = [
    "standardized_reporting_period",
    "reporting_period",
    "standardized_period",
    "period_label",
    "source_worksheet",
    "worksheet_name",
    "sheet_name",
    "source_sheet",
]

period_column = next(
    (column for column in period_candidates if column in df.columns),
    None,
)

if period_column is None:
    print("\nCould not identify the reporting-period column.")
    print("Available columns:")
    print(df.columns.tolist())
    raise SystemExit(
        "Please share the column list so the period field can be mapped."
    )

print(f"Reporting-period column: {period_column}")


# --------------------------------------------------
# 4. PREPARE ANALYSIS FIELDS
# --------------------------------------------------

required_columns = [
    "botanical_name_part",
    "trade_name_part",
    "market",
    "source_year",
    "analytical_price",
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns are missing: {missing_columns}"
    )

# Build a consistent plant identifier.
df["plant_identifier"] = (
    df["botanical_name_part"].str.strip()
    + " | "
    + df["trade_name_part"].str.strip()
)

# Convert prices temporarily for analysis.
df["numeric_price"] = pd.to_numeric(
    df["analytical_price"],
    errors="coerce",
)

# Retain positive prices only for price-trend readiness.
prices = df[df["numeric_price"] > 0].copy()

# Prepare source years as numeric values for year coverage.
prices["year_numeric"] = pd.to_numeric(
    prices["source_year"],
    errors="coerce",
)


# --------------------------------------------------
# 5. SUMMARIZE COVERAGE BY PLANT-MARKET PAIR
# --------------------------------------------------

group_columns = ["plant_identifier", "market"]

# Count observations, reporting periods, and years represented.
readiness = (
    prices.groupby(group_columns)
    .agg(
        positive_price_observations=("numeric_price", "count"),
        distinct_reporting_periods=(period_column, "nunique"),
        distinct_years=("year_numeric", "nunique"),
        first_year=("year_numeric", "min"),
        last_year=("year_numeric", "max"),
        minimum_price=("numeric_price", "min"),
        median_price=("numeric_price", "median"),
        maximum_price=("numeric_price", "max"),
    )
    .reset_index()
)

# Calculate the span between the first and last observed years.
readiness["year_span"] = (
    readiness["last_year"] - readiness["first_year"]
).fillna(0).astype(int)


# --------------------------------------------------
# 6. CLASSIFY TREND READINESS
# --------------------------------------------------

# These are preliminary screening rules, not proof of comparability.
readiness["trend_readiness"] = "Needs more observations"

readiness.loc[
    (readiness["positive_price_observations"] >= 10)
    & (readiness["distinct_reporting_periods"] >= 6)
    & (readiness["distinct_years"] >= 2),
    "trend_readiness",
] = "Candidate for trend analysis"

# Pairs with sufficient observations but limited period/year coverage
# are kept separate for later review.
readiness.loc[
    (readiness["positive_price_observations"] >= 10)
    & (readiness["distinct_reporting_periods"] >= 6)
    & (readiness["distinct_years"] < 2),
    "trend_readiness",
] = "Review period coverage"


# --------------------------------------------------
# 7. SORT AND SAVE THE REPORT
# --------------------------------------------------

readiness = readiness.sort_values(
    [
        "trend_readiness",
        "distinct_years",
        "distinct_reporting_periods",
        "positive_price_observations",
    ],
    ascending=[True, False, False, False],
)

readiness.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig",
)


# --------------------------------------------------
# 8. PRINT SUMMARY
# --------------------------------------------------

print(f"\nPlant-market pairs assessed: {len(readiness):,}")

print("\nTrend readiness classification:")
print(
    readiness["trend_readiness"]
    .value_counts()
    .to_string()
)

print("\nPairs with the most reporting-period coverage:")
print(
    readiness.sort_values(
        ["distinct_reporting_periods", "positive_price_observations"],
        ascending=False,
    )
    .head(10)
    .to_string(index=False)
)

print("\nReport saved:")
print(OUTPUT_FILE)

print("\nThe source dataset was not modified.")
