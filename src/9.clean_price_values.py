
from pathlib import Path
import re
import pandas as pd

# Locate the source dataset and output folders.
PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "medicinal_plant_prices_raw_long.csv"
)
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
REPORT_DIR = PROJECT_DIR / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Read source values as text to avoid losing original notation.
df = pd.read_csv(
    INPUT_FILE,
    dtype=str,
    keep_default_na=False,
)

# Store the original value separately before interpreting it.
original = df["original_price_value"].astype(str).str.strip()

# Prepare new analytical fields.
analytical_prices = []
statuses = []
range_lower_values = []
range_upper_values = []

# Recognize ordinary numeric values using a decimal point.
numeric_pattern = re.compile(r"^[+-]?\d+(?:\.\d+)?$")

# Recognize simple price ranges without converting them to one price.
range_pattern = re.compile(
    r"^\s*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*$"
)

for value in original:
    analytical_price = ""
    range_lower = ""
    range_upper = ""

    if value == "":
        status = "Missing: blank source cell"

    elif value.lower() == "undefined":
        status = "Missing: undefined placeholder"

    elif value == "***":
        status = "Missing: asterisk placeholder"

    elif value == "0*":
        status = "Review required: flagged zero"

    elif value == "0,0":
        status = "Review required: ambiguous comma-zero"

    elif range_pattern.fullmatch(value):
        match = range_pattern.fullmatch(value)
        lower = float(match.group(1))
        upper = float(match.group(2))

        if lower <= upper:
            range_lower = lower
            range_upper = upper
            status = "Price range: endpoints preserved"
        else:
            status = "Review required: reversed price range"

    elif numeric_pattern.fullmatch(value):
        # Parse ordinary numeric values while preserving the source string.
        number = float(value)

        if number < 0:
            status = "Review required: negative price"
        else:
            analytical_price = number
            status = "Numeric-formatted: parsed; validation pending"

    else:
        status = "Review required: unrecognized notation"

    analytical_prices.append(analytical_price)
    statuses.append(status)
    range_lower_values.append(range_lower)
    range_upper_values.append(range_upper)

# Add analytical fields without overwriting original values.
df["analytical_price"] = analytical_prices
df["range_lower"] = range_lower_values
df["range_upper"] = range_upper_values
df["data_quality_status"] = statuses

# Save the cleaned analytical copy.
cleaned_file = OUTPUT_DIR / "medicinal_plant_prices_cleaned.csv"
df.to_csv(cleaned_file, index=False)

# Generate a transformation summary.
summary = (
    df["data_quality_status"]
    .value_counts()
    .rename_axis("data_quality_status")
    .reset_index(name="observations")
)

summary_file = REPORT_DIR / "cleaning_summary.csv"
summary.to_csv(summary_file, index=False)

print("PRICE CLEANING COMPLETED")
print(f"Input observations: {len(df):,}")
print(f"Output observations: {len(df):,}")
print(f"Output columns: {len(df.columns)}")

print("\nQuality-status summary:")
print(summary.to_string(index=False))

print(f"\nCleaned dataset: {cleaned_file}")
print(f"Cleaning summary: {summary_file}")
print("\nOriginal source dataset was not modified.")
