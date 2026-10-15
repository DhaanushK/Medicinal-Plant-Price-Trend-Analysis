
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# Step 1: Check whether the analytical dataset is
# ready for Exploratory Data Analysis (EDA).
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

# Read as strings to preserve the original representations.
df = pd.read_csv(INPUT_FILE, dtype=str, keep_default_na=False)

# Confirm that the columns needed for this assessment exist.
required_columns = [
    "source_year",
    "market",
    "botanical_name_part",
    "trade_name_part",
    "original_price_value",
    "analytical_price",
    "analytical_price_status",
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns missing: {missing_columns}\n"
        f"Available columns: {df.columns.tolist()}"
    )

# Convert the analytical price into a temporary numeric series.
# This does not change the values stored in the dataset.
numeric_price = pd.to_numeric(
    df["analytical_price"],
    errors="coerce",
)

# Count usable positive numeric prices separately from zeros.
positive_prices = numeric_price.gt(0)
zero_prices = numeric_price.eq(0)
negative_prices = numeric_price.lt(0)
unparsed_prices = numeric_price.isna()

# Summarize every analytical status.
status_summary = (
    df["analytical_price_status"]
    .value_counts(dropna=False)
    .rename_axis("analytical_price_status")
    .reset_index(name="observation_count")
)

status_summary["percentage"] = (
    status_summary["observation_count"] / len(df) * 100
).round(2)

status_summary.to_csv(
    REPORT_DIR / "eda_step01_readiness_by_status.csv",
    index=False,
    encoding="utf-8-sig",
)

# Summarize observations and numeric-price availability by year.
year_summary = df[["source_year"]].copy()
year_summary["positive_numeric_price"] = positive_prices.astype(int)
year_summary["zero_price"] = zero_prices.astype(int)
year_summary["negative_price"] = negative_prices.astype(int)
year_summary["unparsed_or_unavailable"] = unparsed_prices.astype(int)

year_summary = (
    year_summary.groupby("source_year", dropna=False)
    .agg(
        total_observations=("source_year", "size"),
        positive_numeric_prices=("positive_numeric_price", "sum"),
        zero_prices=("zero_price", "sum"),
        negative_prices=("negative_price", "sum"),
        unparsed_or_unavailable=("unparsed_or_unavailable", "sum"),
    )
    .reset_index()
)

year_summary["positive_price_percentage"] = (
    year_summary["positive_numeric_prices"]
    / year_summary["total_observations"] * 100
).round(2)

year_summary.to_csv(
    REPORT_DIR / "eda_step01_readiness_by_year.csv",
    index=False,
    encoding="utf-8-sig",
)

# Print the overall readiness report.
print("=" * 65)
print("EDA STEP 1: DATASET READINESS")
print("=" * 65)

print(f"Total observations: {len(df):,}")
print(f"Total columns: {len(df.columns)}")
print(f"Positive numeric prices: {int(positive_prices.sum()):,}")
print(f"Zero prices: {int(zero_prices.sum()):,}")
print(f"Negative prices: {int(negative_prices.sum()):,}")
print(f"Unparsed or unavailable prices: {int(unparsed_prices.sum()):,}")

print("\nAnalytical status summary:")
print(status_summary.to_string(index=False))

print("\nYear-wise price availability:")
print(year_summary.to_string(index=False))

print("\nReports saved:")
print(REPORT_DIR / "eda_step01_readiness_by_status.csv")
print(REPORT_DIR / "eda_step01_readiness_by_year.csv")

print("\nNo source values were modified.")
