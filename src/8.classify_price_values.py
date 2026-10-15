
from pathlib import Path
import re
import pandas as pd

# Load the original values from our long-format dataset.
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "medicinal_plant_prices_raw_long.csv"
)
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(
    DATA_FILE,
    dtype=str,
    keep_default_na=False,
)

values = df["original_price_value"].astype(str).str.strip()

# Recognize only straightforward numeric strings.
# Decimal commas and special symbols remain separately classified.
numeric_pattern = re.compile(r"^[+-]?\d+(?:\.\d+)?$")

# Recognize simple ranges such as 300-1080 or 300 - 1080.
range_pattern = re.compile(
    r"^\s*\d+(?:\.\d+)?\s*[-–]\s*\d+(?:\.\d+)?\s*$"
)

def classify(value):
    """Classify source notation without altering the original value."""
    if value == "":
        return "Blank"

    if value.lower() == "undefined":
        return "Undefined placeholder"

    if value == "***":
        return "Asterisk placeholder"

    if value == "0*":
        return "Flagged zero"

    if value == "0,0":
        return "Ambiguous comma-zero notation"

    if range_pattern.fullmatch(value):
        return "Price range"

    if numeric_pattern.fullmatch(value):
        return "Numeric-formatted value"

    if "," in value:
        return "Other comma-formatted value"

    return "Other text or notation"

# Add a classification column to the in-memory copy only.
df["value_class"] = values.map(classify)

# Overall frequency and percentage by category.
overall = (
    df["value_class"]
    .value_counts()
    .rename_axis("value_class")
    .reset_index(name="observations")
)

overall["percentage"] = (
    overall["observations"] / len(df) * 100
).round(2)

# Classification by year.
by_year = pd.crosstab(
    df["source_year"],
    df["value_class"],
).reset_index()

# Classification by market.
by_market = pd.crosstab(
    df["market"],
    df["value_class"],
).reset_index()

# Save the three reports.
overall.to_csv(
    REPORT_DIR / "price_value_classification.csv",
    index=False,
)

by_year.to_csv(
    REPORT_DIR / "price_value_classification_by_year.csv",
    index=False,
)

by_market.to_csv(
    REPORT_DIR / "price_value_classification_by_market.csv",
    index=False,
)

print("PRICE VALUE CLASSIFICATION")
print(f"Total observations: {len(df):,}")
print(overall.to_string(index=False))

print("\nReports saved:")
print(REPORT_DIR / "price_value_classification.csv")
print(REPORT_DIR / "price_value_classification_by_year.csv")
print(REPORT_DIR / "price_value_classification_by_market.csv")

print("\nOriginal source values have not been modified.")
