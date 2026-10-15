
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

OUTPUT_FILE = REPORT_DIR / "eda_step05_price_distributions.csv"

# Load the analytical dataset without altering the source file.
df = pd.read_csv(INPUT_FILE, dtype=str, keep_default_na=False)

# Convert analytical prices temporarily for statistical analysis.
df["numeric_price"] = pd.to_numeric(
    df["analytical_price"],
    errors="coerce",
)

# Retain positive numeric prices for this initial analysis.
usable = df[df["numeric_price"] > 0].copy()

# Create a plant identifier that includes both names and plant parts.
usable["plant_identifier"] = (
    usable["botanical_name_part"].str.strip()
    + " | "
    + usable["trade_name_part"].str.strip()
)

# Group prices by plant and market.
group_columns = ["plant_identifier", "market"]

summary = (
    usable.groupby(group_columns)["numeric_price"]
    .agg(
        observation_count="count",
        mean_price="mean",
        median_price="median",
        minimum_price="min",
        maximum_price="max",
        standard_deviation="std",
    )
    .reset_index()
)

# Calculate the 25th and 75th percentiles.
quartiles = (
    usable.groupby(group_columns)["numeric_price"]
    .quantile([0.25, 0.75])
    .unstack()
    .reset_index()
)

quartiles = quartiles.rename(
    columns={
        0.25: "price_25th_percentile",
        0.75: "price_75th_percentile",
    }
)

summary = summary.merge(
    quartiles,
    on=group_columns,
    how="left",
    validate="one_to_one",
)

# Apply the provisional minimum-observation threshold.
summary = summary[
    summary["observation_count"] >= 10
].copy()

# Round statistics for readability, without changing source data.
statistic_columns = [
    "mean_price",
    "median_price",
    "minimum_price",
    "maximum_price",
    "standard_deviation",
    "price_25th_percentile",
    "price_75th_percentile",
]

summary[statistic_columns] = summary[statistic_columns].round(2)

# Sort by the number of observations, highest first.
summary = summary.sort_values(
    ["observation_count", "plant_identifier", "market"],
    ascending=[False, True, True],
)

# Save the summary.
summary.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig",
)

# Display initial results.
print("=" * 65)
print("EDA STEP 5: PRICE DISTRIBUTIONS")
print("=" * 65)

print(f"Positive numeric price observations: {len(usable):,}")
print(f"Plant-market pairs meeting threshold: {len(summary):,}")

print("\nPairs with the most observations:")
print(summary.head(10).to_string(index=False))

print("\nOverall descriptive statistics for positive numeric prices:")
print(
    usable["numeric_price"]
    .describe(percentiles=[0.25, 0.50, 0.75, 0.90, 0.95, 0.99])
    .round(2)
    .to_string()
)

print(f"\nReport saved:\n{OUTPUT_FILE}")
print("\nNo source values were modified.")
