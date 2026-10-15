
from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "medicinal_plant_prices_analytical.csv"
)

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load the analytical dataset without changing source values.
df = pd.read_csv(INPUT_FILE, dtype=str, keep_default_na=False)

# Convert analytical prices temporarily for counting.
price = pd.to_numeric(df["analytical_price"], errors="coerce")
df["has_positive_price"] = price.gt(0)

# Create a combined plant identifier for reporting.
df["plant_identifier"] = (
    df["botanical_name_part"].str.strip()
    + " | "
    + df["trade_name_part"].str.strip()
)

# Summarize observations and usable prices by plant.
plant_summary = (
    df.groupby("plant_identifier", dropna=False)
    .agg(
        total_observations=("plant_identifier", "size"),
        positive_price_observations=("has_positive_price", "sum"),
    )
    .reset_index()
)

plant_summary["price_availability_percentage"] = (
    plant_summary["positive_price_observations"]
    / plant_summary["total_observations"]
    * 100
).round(2)

plant_summary = plant_summary.sort_values(
    ["positive_price_observations", "total_observations"],
    ascending=False,
)

plant_summary.to_csv(
    REPORT_DIR / "eda_step02_plant_coverage.csv",
    index=False,
    encoding="utf-8-sig",
)

# Summarize observations and usable prices by market.
market_summary = (
    df.groupby("market", dropna=False)
    .agg(
        total_observations=("market", "size"),
        positive_price_observations=("has_positive_price", "sum"),
    )
    .reset_index()
)

market_summary["price_availability_percentage"] = (
    market_summary["positive_price_observations"]
    / market_summary["total_observations"]
    * 100
).round(2)

market_summary = market_summary.sort_values(
    ["positive_price_observations", "total_observations"],
    ascending=False,
)

market_summary.to_csv(
    REPORT_DIR / "eda_step02_market_coverage.csv",
    index=False,
    encoding="utf-8-sig",
)

# Display the leading entries for initial inspection.
print("=" * 65)
print("EDA STEP 2: PLANT AND MARKET COVERAGE")
print("=" * 65)

print(f"Unique plant identifiers: {len(plant_summary):,}")
print(f"Unique markets: {len(market_summary):,}")

print("\nTop 10 plants by positive numeric price observations:")
print(plant_summary.head(10).to_string(index=False))

print("\nTop 10 markets by positive numeric price observations:")
print(market_summary.head(10).to_string(index=False))

print("\nReports saved:")
print(REPORT_DIR / "eda_step02_plant_coverage.csv")
print(REPORT_DIR / "eda_step02_market_coverage.csv")

print("\nNo source values were modified.")
