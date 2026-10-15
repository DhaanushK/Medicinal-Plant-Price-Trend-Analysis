
from pathlib import Path
import pandas as pd


# --------------------------------------------------
# 1. DEFINE PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "reports"

MONTHLY_FILE = REPORT_DIR / "eda_step09_monthly_price_summary.csv"
READINESS_FILE = REPORT_DIR / "eda_step09_trend_readiness.csv"

DETAIL_FILE = REPORT_DIR / "eda_step09_price_changes.csv"
SUMMARY_FILE = REPORT_DIR / "eda_step09_price_change_summary.csv"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. LOAD MONTHLY SUMMARIES AND READINESS RESULTS
# --------------------------------------------------

monthly = pd.read_csv(MONTHLY_FILE)
readiness = pd.read_csv(READINESS_FILE)

monthly["calendar_month"] = pd.to_datetime(
    monthly["calendar_month"],
    errors="coerce",
)

monthly["median_price"] = pd.to_numeric(
    monthly["median_price"],
    errors="coerce",
)

if monthly["calendar_month"].isna().any():
    raise ValueError("Invalid calendar month found in monthly summary.")

if monthly["median_price"].isna().any():
    raise ValueError("Invalid median price found in monthly summary.")

pair_columns = ["plant_identifier", "market"]

# Analyse only pairs classified as trend-analysis candidates.
candidate_pairs = readiness.loc[
    readiness["trend_readiness"] == "Candidate for trend analysis",
    pair_columns,
].drop_duplicates()

monthly = monthly.merge(
    candidate_pairs.assign(is_candidate=True),
    on=pair_columns,
    how="inner",
    validate="many_to_one",
)

monthly = monthly.sort_values(
    pair_columns + ["calendar_month"]
).copy()

# Each plant-market pair should have no more than one row per month.
if monthly.duplicated(pair_columns + ["calendar_month"]).any():
    raise ValueError("Duplicate plant-market-month records found.")


# --------------------------------------------------
# 3. CALCULATE MONTH-OVER-MONTH CHANGES
# --------------------------------------------------

# Create a lookup for the immediately preceding calendar month.
previous_month = monthly[
    pair_columns + ["calendar_month", "median_price"]
].copy()

previous_month["calendar_month"] = (
    previous_month["calendar_month"] + pd.DateOffset(months=1)
)

previous_month = previous_month.rename(
    columns={
        "median_price": "previous_month_median",
    }
)

monthly = monthly.merge(
    previous_month,
    on=pair_columns + ["calendar_month"],
    how="left",
    validate="one_to_one",
)

# A MoM comparison exists only when the previous calendar month exists.
monthly["mom_absolute_change"] = (
    monthly["median_price"] - monthly["previous_month_median"]
)

monthly["mom_percentage_change"] = (
    monthly["mom_absolute_change"]
    / monthly["previous_month_median"]
    * 100
).where(monthly["previous_month_median"] > 0)

monthly["mom_comparison_available"] = (
    monthly["previous_month_median"].notna()
)


# --------------------------------------------------
# 4. CALCULATE YEAR-OVER-YEAR CHANGES
# --------------------------------------------------

# Match each month to the same calendar month one year earlier.
previous_year = monthly[
    pair_columns + ["calendar_month", "median_price"]
].copy()

previous_year["calendar_month"] = (
    previous_year["calendar_month"] + pd.DateOffset(years=1)
)

previous_year = previous_year.rename(
    columns={
        "median_price": "previous_year_same_month_median",
    }
)

monthly = monthly.merge(
    previous_year,
    on=pair_columns + ["calendar_month"],
    how="left",
    validate="one_to_one",
)

monthly["yoy_absolute_change"] = (
    monthly["median_price"]
    - monthly["previous_year_same_month_median"]
)

monthly["yoy_percentage_change"] = (
    monthly["yoy_absolute_change"]
    / monthly["previous_year_same_month_median"]
    * 100
).where(monthly["previous_year_same_month_median"] > 0)

monthly["yoy_comparison_available"] = (
    monthly["previous_year_same_month_median"].notna()
)


# --------------------------------------------------
# 5. SAVE THE DETAILED PRICE-CHANGE REPORT
# --------------------------------------------------

monthly.to_csv(
    DETAIL_FILE,
    index=False,
    encoding="utf-8-sig",
)


# --------------------------------------------------
# 6. SUMMARIZE PRICE MOVEMENTS BY PLANT AND MARKET
# --------------------------------------------------

summary = (
    monthly.groupby(pair_columns)
    .agg(
        observed_months=("calendar_month", "nunique"),
        first_observed_month=("calendar_month", "min"),
        last_observed_month=("calendar_month", "max"),
        first_observed_median=("median_price", "first"),
        latest_observed_median=("median_price", "last"),
        available_mom_comparisons=("mom_percentage_change", "count"),
        available_yoy_comparisons=("yoy_percentage_change", "count"),
        median_mom_change_pct=("mom_percentage_change", "median"),
        median_yoy_change_pct=("yoy_percentage_change", "median"),
    )
    .reset_index()
)

# These describe the first and latest observed months, not necessarily
# consecutive months. Keep the elapsed time visible.
summary["first_observed_month"] = pd.to_datetime(
    summary["first_observed_month"]
)

summary["last_observed_month"] = pd.to_datetime(
    summary["last_observed_month"]
)

summary["overall_observed_change_pct"] = (
    (
        summary["latest_observed_median"]
        - summary["first_observed_median"]
    )
    / summary["first_observed_median"]
    * 100
).where(summary["first_observed_median"] > 0)

summary["elapsed_months"] = (
    (summary["last_observed_month"].dt.year
     - summary["first_observed_month"].dt.year) * 12
    + summary["last_observed_month"].dt.month
    - summary["first_observed_month"].dt.month
)

summary = summary.sort_values(
    "overall_observed_change_pct",
    ascending=False,
    na_position="last",
)

summary.to_csv(
    SUMMARY_FILE,
    index=False,
    encoding="utf-8-sig",
)


# --------------------------------------------------
# 7. PRINT RESULTS
# --------------------------------------------------

print("=" * 70)
print("EDA STEP 9.4: PRICE CHANGE ANALYSIS")
print("=" * 70)

print(f"Candidate plant-market pairs: {len(candidate_pairs):,}")
print(f"Monthly records analysed: {len(monthly):,}")

print(
    "\nAvailable month-over-month comparisons: "
    f"{int(monthly['mom_comparison_available'].sum()):,}"
)

print(
    "Available year-over-year comparisons: "
    f"{int(monthly['yoy_comparison_available'].sum()):,}"
)

print("\nLargest observed overall increases:")
print(
    summary.head(10).to_string(index=False)
)

print("\nLargest observed overall decreases:")
print(
    summary.sort_values(
        "overall_observed_change_pct",
        ascending=True,
        na_position="last",
    )
    .head(10)
    .to_string(index=False)
)

print("\nReports saved:")
print(DETAIL_FILE)
print(SUMMARY_FILE)

print(
    "\nMissing months were not filled. "
    "First-to-latest changes may span gaps."
)
