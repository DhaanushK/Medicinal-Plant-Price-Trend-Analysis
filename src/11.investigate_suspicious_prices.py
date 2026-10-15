
from pathlib import Path
import pandas as pd

# Project root and input/output paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "medicinal_plant_prices_cleaned.csv"
)

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

ZERO_REPORT = REPORT_DIR / "zero_price_investigation.csv"
HIGH_REPORT = REPORT_DIR / "high_price_investigation.csv"

# Read all columns as text to preserve the original source values.
df = pd.read_csv(INPUT_FILE, dtype=str, keep_default_na=False)

# Convert the analytical price into a temporary numeric column.
# The original_price_value column remains unchanged.
df["numeric_price"] = pd.to_numeric(
    df["analytical_price"],
    errors="coerce"
)

# Select useful identifying columns for manual investigation.
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
    "analytical_price",
    "price_quality_status",
]

# Keep only columns that actually exist in the dataset.
review_columns = [
    column for column in review_columns
    if column in df.columns
]

# Report 1: numeric prices equal to zero.
zero_prices = df[df["numeric_price"] == 0].copy()

zero_prices[review_columns].to_csv(
    ZERO_REPORT,
    index=False,
    encoding="utf-8-sig"
)

# Report 2: prices above the 99th percentile.
# This is a screening threshold, not proof of an invalid price.
valid_prices = df["numeric_price"].dropna()

if not valid_prices.empty:
    high_threshold = valid_prices.quantile(0.99)

    high_prices = df[
        df["numeric_price"] > high_threshold
    ].copy()

    high_prices[review_columns].assign(
        screening_threshold=high_threshold
    ).to_csv(
        HIGH_REPORT,
        index=False,
        encoding="utf-8-sig"
    )
else:
    high_threshold = None

    df.iloc[0:0][review_columns].to_csv(
        HIGH_REPORT,
        index=False,
        encoding="utf-8-sig"
    )

# Display the results.
print("=" * 60)
print("SUSPICIOUS PRICE INVESTIGATION")
print("=" * 60)

print(f"Total observations: {len(df):,}")
print(f"Zero-price records: {len(zero_prices):,}")

if high_threshold is not None:
    print(f"99th-percentile screening threshold: {high_threshold:,.2f}")
    print(f"High-price records above threshold: {len(high_prices):,}")

print("\nReports saved:")
print(ZERO_REPORT)
print(HIGH_REPORT)

print("\nNo source values were modified or deleted.")
