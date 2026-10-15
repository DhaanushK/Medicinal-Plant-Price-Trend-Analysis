
from pathlib import Path
import pandas as pd

# Locate the project directory from this script's location.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Input files created during our previous steps.
DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "medicinal_plant_prices_analytical.csv"
)

REPORT_DIR = PROJECT_ROOT / "reports"

# Load the analytical dataset without changing the source file.
df = pd.read_csv(DATA_FILE, low_memory=False)

print("=" * 65)
print("CONSOLIDATED EDA REPORT — NUMERICAL RECONCILIATION")
print("=" * 65)

# 1. Verify dataset dimensions.
print("\n1. DATASET DIMENSIONS")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

# 2. Display column names so we can verify the expected schema.
print("\n2. AVAILABLE COLUMNS")
for column in df.columns:
    print(f"- {column}")

# 3. Verify period coverage.

# 3. Verify period coverage using the actual column name.
print("\n3. YEAR COVERAGE")

year_column = "source_year"

if year_column in df.columns:
    years = pd.to_numeric(df[year_column], errors="coerce").dropna()
    print(f"Minimum year: {int(years.min()) if not years.empty else 'N/A'}")
    print(f"Maximum year: {int(years.max()) if not years.empty else 'N/A'}")
    print(f"Distinct years: {years.nunique()}")
else:
    print(f"Column '{year_column}' not found.")

# 4. Check unique plants and markets.
print("\n4. PLANT AND MARKET COVERAGE")

plant_columns = ["botanical_name_part", "trade_name_part"]
market_column = "market"

if all(column in df.columns for column in plant_columns):
    # Count unique botanical/trade-name combinations as plant identifiers.
    unique_plants = df[plant_columns].drop_duplicates()
    print(f"Unique plant identifiers: {len(unique_plants):,}")
else:
    print("Required plant-name columns were not found.")

if market_column in df.columns:
    print(f"Unique markets: {df[market_column].nunique(dropna=True):,}")
else:
    print(f"Column '{market_column}' not found.")


# 5. Check duplicate records using the reporting-period key.
print("\n5. DUPLICATE KEY CHECK")

key_columns = [
    "botanical_name_part",
    "trade_name_part",
    "market",
    "source_workbook",
    "source_sheet",
]

if all(column in df.columns for column in key_columns):
    duplicate_count = int(df.duplicated(subset=key_columns).sum())
    print(f"Duplicate plant-market-period records: {duplicate_count:,}")
else:
    missing_columns = [
        column for column in key_columns if column not in df.columns
    ]
    print(f"Cannot verify duplicates. Missing columns: {missing_columns}")


# 6. Identify the analytical price column and calculate numeric counts.
print("\n6. NUMERIC PRICE CHECK")

price_column = "analytical_price"

if price_column in df.columns:
    numeric_prices = pd.to_numeric(df[price_column], errors="coerce")

    positive_count = int((numeric_prices > 0).sum())
    zero_count = int((numeric_prices == 0).sum())
    negative_count = int((numeric_prices < 0).sum())

    print(f"Positive numeric prices: {positive_count:,}")
    print(f"Zero numeric prices: {zero_count:,}")
    print(f"Negative numeric prices: {negative_count:,}")
    print(f"Missing or non-numeric prices: {int(numeric_prices.isna().sum()):,}")

    # Recalculate descriptive statistics using positive prices only.
    positive_prices = numeric_prices[numeric_prices > 0]

    if not positive_prices.empty:
        print("\nPositive-price distribution:")
        print(f"Count: {len(positive_prices):,}")
        print(f"Mean: {positive_prices.mean():,.2f}")
        print(f"Standard deviation: {positive_prices.std():,.2f}")
        print(f"Minimum: {positive_prices.min():,.2f}")
        print(f"Q1 (25th percentile): {positive_prices.quantile(0.25):,.2f}")
        print(f"Median: {positive_prices.median():,.2f}")
        print(f"Q3 (75th percentile): {positive_prices.quantile(0.75):,.2f}")
        print(f"P90: {positive_prices.quantile(0.90):,.2f}")
        print(f"P95: {positive_prices.quantile(0.95):,.2f}")
        print(f"P99: {positive_prices.quantile(0.99):,.2f}")
        print(f"Maximum: {positive_prices.max():,.2f}")
else:
    print(
        f"Column '{price_column}' not found. "
        "Inspect the available columns above before proceeding."
    )

# 7. Inspect analytical status counts without modifying them.
print("\n7. ANALYTICAL PRICE STATUS COUNTS")

status_column = "analytical_price_status"

if status_column in df.columns:
    status_counts = (
        df[status_column]
        .fillna("[blank status]")
        .value_counts(dropna=False)
    )

    for status, count in status_counts.items():
        print(f"{status}: {count:,}")
else:
    print(f"Column '{status_column}' not found.")

# 8. Save a small audit summary for later documentation.
summary_lines = [
    "CONSOLIDATED EDA NUMERICAL RECONCILIATION",
    f"Dataset rows: {len(df):,}",
    f"Dataset columns: {len(df.columns)}",
]

if "year" in df.columns:
    years = pd.to_numeric(df["year"], errors="coerce").dropna()
    if not years.empty:
        summary_lines.append(
            f"Year coverage: {int(years.min())}-{int(years.max())}"
        )

plant_columns = ["botanical_name_part", "trade_name_part"]

if all(column in df.columns for column in plant_columns):
    unique_plants = df[plant_columns].drop_duplicates()
    summary_lines.append(f"Unique plant identifiers: {len(unique_plants):,}")

if market_column in df.columns:
    summary_lines.append(
        f"Unique markets: {df[market_column].nunique(dropna=True):,}"
    )

if price_column in df.columns:
    numeric_prices = pd.to_numeric(df[price_column], errors="coerce")
    summary_lines.append(
        f"Positive numeric prices: {int((numeric_prices > 0).sum()):,}"
    )
    summary_lines.append(
        f"Zero numeric prices: {int((numeric_prices == 0).sum()):,}"
    )

output_file = REPORT_DIR / "EDA_numerical_reconciliation.txt"
output_file.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

print("\n" + "=" * 65)
print(f"Reconciliation summary saved to: {output_file}")
print("No source data or existing reports were modified.")
print("=" * 65)
