
from pathlib import Path
import pandas as pd

# Locate the transformed dataset.
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "medicinal_plant_prices_raw_long.csv"
)

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

# Preserve text values such as "NA" during validation.
df = pd.read_csv(
    DATA_FILE,
    dtype=str,
    keep_default_na=False,
)

print("=" * 60)
print("LONG-FORMAT DATASET VALIDATION")
print("=" * 60)

# 1. Basic dataset structure.
print(f"\nTotal observations: {len(df):,}")
print(f"Total columns: {len(df.columns)}")
print("\nColumn names:")
print(df.columns.tolist())

# 2. Verify the study-period boundaries.
years = sorted(
    df["source_year"].dropna().unique().tolist()
)

print("\nYears represented:")
print(years)

# 3. Verify fortnight assignments.
print("\nFortnight counts:")
print(df["fortnight"].value_counts(dropna=False).to_string())

print("\nPeriod-status counts:")
print(df["period_status"].value_counts(dropna=False).to_string())

# 4. Check missing identifiers and source prices.
identifier_columns = [
    "source_year",
    "source_sheet",
    "botanical_name_part",
    "trade_name_part",
    "market",
]

print("\nBlank identifier counts:")
for column in identifier_columns:
    blank_count = int(
        df[column].astype(str).str.strip().eq("").sum()
    )
    print(f"{column}: {blank_count:,}")

blank_prices = int(
    df["original_price_value"].astype(str).str.strip().eq("").sum()
)

print(f"\nBlank original price cells: {blank_prices:,}")

# 5. Count special source values without changing them.
values = df["original_price_value"].astype(str).str.strip()

special_values = [
    "***",
    "undefined",
    "0*",
    "0,0",
]

print("\nSelected original-value counts:")
for value in special_values:
    count = int(values.eq(value).sum())
    print(f"{value}: {count:,}")

# 6. Check duplicate observations.
# Include source sheet and plant identifiers so we can inspect
# repeated plant-market records rather than deleting them.
key_columns = [
    "source_workbook",
    "source_sheet",
    "botanical_name_part",
    "trade_name_part",
    "market",
]

duplicate_mask = df.duplicated(
    subset=key_columns,
    keep=False,
)

print(
    "\nRows involved in repeated plant-market-sheet keys: "
    f"{int(duplicate_mask.sum()):,}"
)

# Save repeated keys for manual inspection.
duplicate_file = (
    PROJECT_DIR
    / "reports"
    / "duplicate_key_review.csv"
)

duplicate_file.parent.mkdir(parents=True, exist_ok=True)

df.loc[duplicate_mask].sort_values(
    key_columns
).to_csv(duplicate_file, index=False)

print(f"Duplicate review saved to: {duplicate_file}")

# 7. Check the expected number of columns.
expected_columns = 12

print(f"\nExpected columns: {expected_columns}")
print(f"Actual columns: {len(df.columns)}")

if len(df.columns) == expected_columns:
    print("Column-count check: PASSED")
else:
    print("Column-count check: REVIEW REQUIRED")

print("\nValidation finished. No source data was modified.")
