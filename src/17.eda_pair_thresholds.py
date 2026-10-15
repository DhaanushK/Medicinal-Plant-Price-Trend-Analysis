
from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "eda_step03_plant_market_pairs.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "eda_step04_pair_thresholds.csv"
)

# Load the plant-market coverage report.
pairs = pd.read_csv(INPUT_FILE)

# Check the required field.
required_column = "positive_price_observations"

if required_column not in pairs.columns:
    raise ValueError(
        f"Missing required column: {required_column}"
    )

# Define thresholds for initial descriptive analysis.
thresholds = [1, 5, 10, 20]

total_pairs = len(pairs)
results = []

# Count how many pairs meet each minimum.
for threshold in thresholds:
    qualifying_pairs = int(
        pairs[required_column].ge(threshold).sum()
    )

    results.append({
        "minimum_positive_observations": threshold,
        "qualifying_pairs": qualifying_pairs,
        "total_pairs": total_pairs,
        "percentage_of_all_pairs": round(
            qualifying_pairs / total_pairs * 100, 2
        ) if total_pairs else 0,
    })

summary = pd.DataFrame(results)

# Save the threshold assessment.
summary.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig",
)

# Display results.
print("=" * 65)
print("EDA STEP 4: PLANT-MARKET OBSERVATION THRESHOLDS")
print("=" * 65)

print(f"Total plant-market pairs: {total_pairs:,}")
print("\nPairs meeting each minimum:")
print(summary.to_string(index=False))

print(f"\nReport saved:\n{OUTPUT_FILE}")
