
from pathlib import Path
import pandas as pd

# Define project paths.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "eda_step06_iqr_outliers.csv"
)

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

GROUP_REPORT = REPORT_DIR / "eda_step07_outlier_patterns_by_pair.csv"
YEAR_REPORT = REPORT_DIR / "eda_step07_outlier_patterns_by_year.csv"
MARKET_REPORT = REPORT_DIR / "eda_step07_outlier_patterns_by_market.csv"

# Load the previously generated outlier report.
outliers = pd.read_csv(INPUT_FILE)

if outliers.empty:
    print("No IQR-flagged observations are available for analysis.")
    raise SystemExit(0)

# Build a plant identifier for reporting.
outliers["plant_identifier"] = (
    outliers["botanical_name_part"].astype(str).str.strip()
    + " | "
    + outliers["trade_name_part"].astype(str).str.strip()
)

# Summarize the flagged observations by plant-market pair.
group_summary = (
    outliers.groupby(["plant_identifier", "market"])
    .agg(
        flagged_count=("numeric_price", "size"),
        highest_flagged_value=("numeric_price", "max"),
        lowest_flagged_value=("numeric_price", "min"),
        median_price=("median_price", "first"),
        upper_screening_limit=("upper_screening_limit", "first"),
        reporting_periods=("source_sheet", "nunique"),
    )
    .reset_index()
)

group_summary = group_summary.sort_values(
    ["flagged_count", "highest_flagged_value"],
    ascending=False,
)

group_summary.to_csv(
    GROUP_REPORT,
    index=False,
    encoding="utf-8-sig",
)


# Summarize flagged observations by source year.
year_summary = (
    outliers.groupby("source_year")
    .agg(
        flagged_observations=("numeric_price", "size"),
        highest_flagged_value=("numeric_price", "max"),
    )
    .reset_index()
)

# Count distinct plant-market combinations for each year.
unique_pairs_by_year = (
    outliers[
        ["source_year", "plant_identifier", "market"]
    ]
    .drop_duplicates()
    .groupby("source_year")
    .size()
    .rename("affected_plant_market_pairs")
    .reset_index()
)

year_summary = year_summary.merge(
    unique_pairs_by_year,
    on="source_year",
    how="left",
)



# Summarize flagged observations by market.
market_summary = (
    outliers.groupby("market")
    .agg(
        flagged_observations=("numeric_price", "size"),
        highest_flagged_value=("numeric_price", "max"),
    )
    .reset_index()
)

# Count distinct plant-market pairs with flagged observations.
unique_pairs_by_market = (
    outliers[
        ["plant_identifier", "market"]
    ]
    .drop_duplicates()
    .groupby("market")
    .size()
    .rename("affected_plant_market_pairs")
    .reset_index()
)

# Combine observation counts and distinct pair counts.
market_summary = (
    market_summary
    .merge(
        unique_pairs_by_market,
        on="market",
        how="left",
    )
    .sort_values("flagged_observations", ascending=False)
)

market_summary.to_csv(
    MARKET_REPORT,
    index=False,
    encoding="utf-8-sig",
)


# Display the results.
print("=" * 65)
print("EDA STEP 7: OUTLIER FREQUENCY AND TIMING")
print("=" * 65)

print(f"Total flagged observations: {len(outliers):,}")
print(f"Plant-market groups affected: {len(group_summary):,}")

print("\nTop 10 groups by flagged-observation count:")
print(group_summary.head(10).to_string(index=False))

print("\nOutlier counts by year:")
print(year_summary.to_string(index=False))

print("\nTop 10 markets by flagged-observation count:")
print(market_summary.head(10).to_string(index=False))

print("\nReports saved:")
print(GROUP_REPORT)
print(YEAR_REPORT)
print(MARKET_REPORT)

print("\nNo source values were removed or changed.")
