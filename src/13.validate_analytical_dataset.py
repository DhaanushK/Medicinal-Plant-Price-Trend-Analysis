
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

REPORT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "analytical_dataset_validation.txt"
)

# Load all values as strings to avoid altering source representations.
df = pd.read_csv(INPUT_FILE, dtype=str, keep_default_na=False)

# Check that the required columns are available.
required_columns = [
    "source_year",
    "source_sheet",
    "botanical_name_part",
    "trade_name_part",
    "market",
    "original_price_value",
    "analytical_price",
    "analytical_price_status",
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

# Identify the records flagged as presumed missing.
flagged = df[
    df["analytical_price_status"]
    == "Presumed missing: zero in Dec 2025 - 1"
]

# Check that the flagged records meet the expected conditions.
flagged_sheet_correct = flagged["source_sheet"].eq(
    "Dec 2025 - 1"
).all()

flagged_values_correct = flagged["original_price_value"].eq(
    "0"
).all()

# Check for duplicate plant-market-sheet keys.
key_columns = [
    "source_year",
    "source_sheet",
    "botanical_name_part",
    "trade_name_part",
    "market",
]

duplicate_count = int(
    df.duplicated(subset=key_columns).sum()
)

# Build validation results.
results = [
    "ANALYTICAL DATASET VALIDATION",
    "=" * 50,
    f"Total observations: {len(df):,}",
    f"Total columns: {len(df.columns)}",
    f"Missing required columns: {missing_columns}",
    f"Presumed-missing records: {len(flagged):,}",
    f"All flagged records are from Dec 2025 - 1: {flagged_sheet_correct}",
    f"All flagged original values are zero: {flagged_values_correct}",
    f"Duplicate plant-market-sheet keys: {duplicate_count}",
]

# Save the validation report.
REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

with open(REPORT_FILE, "w", encoding="utf-8") as file:
    file.write("\n".join(results))

# Display the report.
print("\n".join(results))
print(f"\nReport saved to:\n{REPORT_FILE}")

# Report an overall status without changing any data.
checks_passed = (
    not missing_columns
    and len(flagged) == 168
    and flagged_sheet_correct
    and flagged_values_correct
    and duplicate_count == 0
)

print(
    "\nOverall validation:",
    "PASSED" if checks_passed else "REVIEW REQUIRED",
)
