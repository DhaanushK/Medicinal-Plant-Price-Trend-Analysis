
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

MARKET_FILE = REPORT_DIR / "eda_step08_outlier_rates_by_market.csv"
YEAR_FILE = REPORT_DIR / "eda_step08_outlier_rates_by_year.csv"


# --------------------------------------------------
# 2. LOAD THE ANALYTICAL DATASET
# --------------------------------------------------

# Read all source columns as strings to preserve their original values.
df = pd.read_csv(INPUT_FILE, dtype=str, keep_default_na=False)

# Convert prices temporarily for numerical analysis.
df["numeric_price"] = pd.to_numeric(
    df["analytical_price"],
    errors="coerce",
)

# Use positive numeric prices only.
prices = df[df["numeric_price"] > 0].copy()

# Create the plant identifier used in previous EDA steps.
prices["plant_identifier"] = (
    prices["botanical_name_part"].str.strip()
    + " | "
    + prices["trade_name_part"].str.strip()
)

group_columns = ["plant_identifier", "market"]


# --------------------------------------------------
# 3. CALCULATE IQR SCREENING LIMITS
# --------------------------------------------------

# Calculate observation counts and quartiles for each plant-market pair.
group_stats = (
    prices.groupby(group_columns)["numeric_price"]
    .agg(
        pair_observations="count",
        q1=lambda values: values.quantile(0.25),
        q3=lambda values: values.quantile(0.75),
    )
    .reset_index()
)

# Calculate the interquartile range and upper screening limit.
group_stats["iqr"] = group_stats["q3"] - group_stats["q1"]

group_stats["upper_screening_limit"] = (
    group_stats["q3"] + 1.5 * group_stats["iqr"]
)


# --------------------------------------------------
# 4. ATTACH LIMITS AND SELECT ELIGIBLE PAIRS
# --------------------------------------------------

# Attach each plant-market pair's statistics to its observations.
prices = prices.merge(
    group_stats,
    on=group_columns,
    how="left",
    validate="many_to_one",
)

# Keep pairs with at least 10 positive numeric observations.
eligible = prices[prices["pair_observations"] >= 10].copy()


# --------------------------------------------------
# 5. FLAG POTENTIAL OUTLIERS
# --------------------------------------------------

# Flag prices above the pair-specific upper IQR screening limit.
eligible["is_iqr_flagged"] = (
    eligible["numeric_price"] > eligible["upper_screening_limit"]
).astype(int)


# --------------------------------------------------
# 6. SUMMARIZE OUTLIER RATES BY MARKET
# --------------------------------------------------

market_summary = (
    eligible.groupby("market")
    .agg(
        eligible_observations=("numeric_price", "size"),
        flagged_observations=("is_iqr_flagged", "sum"),
    )
    .reset_index()
)

# Count each affected plant-market pair only once per market.
unique_affected = (
    eligible.loc[
        eligible["is_iqr_flagged"] == 1,
        ["market", "plant_identifier"],
    ]
    .drop_duplicates()
    .groupby("market")
    .size()
    .rename("unique_affected_pairs")
    .reset_index()
)

# Add the distinct affected-pair counts to the market summary.
market_summary = market_summary.merge(
    unique_affected,
    on="market",
    how="left",
)

market_summary["unique_affected_pairs"] = (
    market_summary["unique_affected_pairs"]
    .fillna(0)
    .astype(int)
)

# Calculate the percentage of eligible observations flagged as outliers.
market_summary["outlier_rate_percentage"] = (
    market_summary["flagged_observations"]
    / market_summary["eligible_observations"]
    * 100
).round(2)

# Sort markets from highest to lowest outlier rate.
market_summary = market_summary.sort_values(
    "outlier_rate_percentage",
    ascending=False,
)

# Save the market-level report.
market_summary.to_csv(
    MARKET_FILE,
    index=False,
    encoding="utf-8-sig",
)


# --------------------------------------------------
# 7. SUMMARIZE OUTLIER RATES BY YEAR
# --------------------------------------------------

year_summary = (
    eligible.groupby("source_year")
    .agg(
        eligible_observations=("numeric_price", "size"),
        flagged_observations=("is_iqr_flagged", "sum"),
    )
    .reset_index()
)

# Calculate each year's outlier rate among eligible observations.
year_summary["outlier_rate_percentage"] = (
    year_summary["flagged_observations"]
    / year_summary["eligible_observations"]
    * 100
).round(2)

# Save the year-level report.
year_summary.to_csv(
    YEAR_FILE,
    index=False,
    encoding="utf-8-sig",
)


# --------------------------------------------------
# 8. PRINT RESULTS
# --------------------------------------------------

print("=" * 65)
print("EDA STEP 8: OUTLIER RATES")
print("=" * 65)

print(f"Positive numeric observations: {len(prices):,}")
print(
    "Eligible observations in pairs meeting threshold: "
    f"{len(eligible):,}"
)
print(
    "Flagged observations: "
    f"{int(eligible['is_iqr_flagged'].sum()):,}"
)

print("\nMarkets with the highest outlier rates:")
print(market_summary.head(10).to_string(index=False))

print("\nOutlier rates by year:")
print(year_summary.to_string(index=False))

print("\nReports saved:")
print(MARKET_FILE)
print(YEAR_FILE)

print("\nNo source values were removed or changed.")
