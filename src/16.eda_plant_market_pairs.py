
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

# Load the analytical dataset without modifying source values.
df = pd.read_csv(INPUT_FILE, dtype=str, keep_default_na=False)

# Convert analytical prices temporarily for analysis.
price = pd.to_numeric(df["analytical_price"], errors="coerce")
df["has_positive_price"] = price.gt(0).astype(int)

# Identify each plant using both botanical and trade names.
df["plant_identifier"] = (
    df["botanical_name_part"].str.strip()
    + " | "
    + df["trade_name_part"].str.strip()
)

# Count records and usable prices for each plant-market pair.
pair_summary = (
    df.groupby(
        ["plant_identifier", "market"],
        dropna=False,
    )
    .agg(
        total_observations=("market", "size"),
        positive_price_observations=("has_positive_price", "sum"),
    )
    .reset_index()
)

# Calculate the proportion of observations with positive prices.
pair_summary["price_availability_percentage"] = (
    pair_summary["positive_price_observations"]
    / pair_summary["total_observations"]
    * 100
).round(2)

# Rank pairs by their number of positive numeric prices.
pair_summary = pair_summary.sort_values(
    ["positive_price_observations", "total_observations"],
    ascending=False,
)

# Save the complete pair-level report.
output_file = REPORT_DIR / "eda_step03_plant_market_pairs.csv"

pair_summary.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig",
)

# Summarize the number of pairs by positive-price count.
pair_count_summary = (
    pair_summary["positive_price_observations"]
    .value_counts()
    .sort_index()
    .rename_axis("positive_price_observations")
    .reset_index(name="number_of_plant_market_pairs")
)

pair_count_summary.to_csv(
    REPORT_DIR / "eda_step03_pair_count_distribution.csv",
    index=False,
    encoding="utf-8-sig",
)

# Display key results.
print("=" * 65)
print("EDA STEP 3: PLANT-MARKET PAIR COVERAGE")
print("=" * 65)

print(f"Unique plants: {df['plant_identifier'].nunique():,}")
print(f"Unique markets: {df['market'].nunique():,}")
print(f"Plant-market pairs: {len(pair_summary):,}")

print("\nPairs with the most positive numeric prices:")
print(pair_summary.head(10).to_string(index=False))

print("\nPairs with zero positive numeric prices:")
zero_pairs = pair_summary[
    pair_summary["positive_price_observations"] == 0
]
print(f"{len(zero_pairs):,}")

print("\nPair-count distribution saved.")
print(f"Report: {output_file}")
print(
    "Report:",
    REPORT_DIR / "eda_step03_pair_count_distribution.csv",
)

print("\nNo source values were modified.")
