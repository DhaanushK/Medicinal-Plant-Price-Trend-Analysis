
from pathlib import Path
import pandas as pd

# Define project paths.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "medicinal_plant_prices_cleaned.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "medicinal_plant_prices_analytical.csv"
)

# Read all values as strings to preserve source representations.
df = pd.read_csv(INPUT_FILE, dtype=str, keep_default_na=False)

# Check that the columns required for this step exist.
required_columns = [
    "source_sheet",
    "original_price_value",
    "analytical_price",
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns not found: {missing_columns}\n"
        f"Available columns: {df.columns.tolist()}"
    )

# Convert prices temporarily for classification.
numeric_price = pd.to_numeric(
    df["analytical_price"],
    errors="coerce",
)

# Create a new status without depending on another status column.
df["analytical_price_status"] = "Review required"

# Identify numeric prices that can be used provisionally.
valid_numeric = numeric_price.notna() & numeric_price.gt(0)

df.loc[
    valid_numeric,
    "analytical_price_status",
] = "Numeric price: validation pending"

# Preserve existing treatment of known missing placeholders.
source_value = df["original_price_value"].str.strip().str.lower()

df.loc[
    source_value.eq(""),
    "analytical_price_status",
] = "Missing: blank source cell"

df.loc[
    source_value.eq("undefined"),
    "analytical_price_status",
] = "Missing: undefined placeholder"

df.loc[
    source_value.eq("***"),
    "analytical_price_status",
] = "Missing: asterisk placeholder"

# Flag zero values in the December 2025 worksheet.
# This is an inference based on observed source patterns,
# not an officially confirmed definition.
presumed_missing_zero = (
    df["source_sheet"].eq("Dec 2025 - 1")
    & numeric_price.eq(0)
)

df.loc[
    presumed_missing_zero,
    "analytical_price_status",
] = "Presumed missing: zero in Dec 2025 - 1"

# Save a separate analytical copy; do not overwrite the input.
df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig",
)

# Report validation results.
print("=" * 60)
print("ANALYTICAL DATASET CREATION")
print("=" * 60)

print(f"Total observations: {len(df):,}")
print(f"Output columns: {len(df.columns)}")
print(f"Presumed-missing zero records: {int(presumed_missing_zero.sum()):,}")

preserved_zeros = (
    df.loc[presumed_missing_zero, "original_price_value"]
    .eq("0")
    .sum()
)

print(f"Original zero values preserved: {int(preserved_zeros):,}")
print(f"\nSaved analytical dataset:\n{OUTPUT_FILE}")

# Display status counts for review.
print("\nAnalytical status summary:")
print(df["analytical_price_status"].value_counts().to_string())
