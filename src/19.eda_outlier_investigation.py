
from pathlib import Path
import pandas as pd

# Define project paths.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "medicinal_plant_prices_analytical.csv"
)

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTLIER_FILE = REPORT_DIR / "eda_step06_iqr_outliers.csv"
SUMMARY_FILE = REPORT_DIR / "eda_step06_outlier_summary.csv"

# Load data without changing source representations.
df = pd.read_csv(INPUT_FILE, dtype=str, keep_default_na=False)

# Convert analytical prices temporarily.
df["numeric_price"] = pd.to_numeric(
    df["analytical_price"],
    errors="coerce",
)

# Keep positive numeric prices for this investigation.
prices = df[df["numeric_price"] > 0].copy()

# Create a consistent plant identifier.
prices["plant_identifier"] = (
    prices["botanical_name_part"].str.strip()
    + " | "
    + prices["trade_name_part"].str.strip()
)

group_columns = ["plant_identifier", "market"]

# Calculate IQR limits separately for each plant-market pair.
group_stats = (
    prices.groupby(group_columns)["numeric_price"]
    .agg(
        observation_count="count",
        q1=lambda values: values.quantile(0.25),
        median_price="median",
        q3=lambda values: values.quantile(0.75),
    )
    .reset_index()
)

group_stats["iqr"] = group_stats["q3"] - group_stats["q1"]

group_stats["upper_screening_limit"] = (
    group_stats["q3"] + 1.5 * group_stats["iqr"]
)

# Merge limits back into the observations.
prices = prices.merge(
    group_stats,
    on=group_columns,
    how="left",
    validate="many_to_one",
)

# Apply the provisional minimum of 10 observations per group.
eligible = prices[
    prices["observation_count"] >= 10
].copy()

# Flag values above their group's upper IQR limit.
outliers = eligible[
    eligible["numeric_price"] > eligible["upper_screening_limit"]
].copy()

# Select useful source-identification fields.
review_columns = [
    "source_year",
    "reporting_month",
    "reporting_month_name",
    "fortnight",
    "source_workbook",
    "source_sheet",
    "botanical_name_part",
    "trade_name_part",
    "market",
    "original_price_value",
    "numeric_price",
    "observation_count",
    "q1",
    "median_price",
    "q3",
    "iqr",
    "upper_screening_limit",
]

outliers[review_columns].to_csv(
    OUTLIER_FILE,
    index=False,
    encoding="utf-8-sig",
)

# Summarize flagged records by plant-market pair.
outlier_summary = (
    outliers.groupby(group_columns)
    .agg(
        flagged_observations=("numeric_price", "size"),
        highest_flagged_value=("numeric_price", "max"),
        median_price=("median_price", "first"),
        upper_screening_limit=("upper_screening_limit", "first"),
    )
    .reset_index()
    .sort_values(
        ["flagged_observations", "highest_flagged_value"],
        ascending=False,
    )
)

outlier_summary.to_csv(
    SUMMARY_FILE,
    index=False,
    encoding="utf-8-sig",
)

# Print investigation results.
print("=" * 65)
print("EDA STEP 6: IQR OUTLIER INVESTIGATION")
print("=" * 65)

print(f"Positive numeric observations: {len(prices):,}")
print(f"Eligible plant-market pairs: {len(group_stats[group_stats['observation_count'] >= 10]):,}")
print(f"Flagged observations: {len(outliers):,}")
print(f"Plant-market pairs with flagged observations: {len(outlier_summary):,}")

print("\nPairs with the most flagged observations:")
if not outlier_summary.empty:
    print(outlier_summary.head(10).to_string(index=False))
else:
    print("No observations exceeded the screening limits.")

print("\nReports saved:")
print(OUTLIER_FILE)
print(SUMMARY_FILE)

print("\nNo source values were removed or changed.")
