
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    ROOT / "reports" / "eda_step09_november_spike_comparison.csv"
)
OUTPUT_FILE = (
    ROOT / "reports" / "eda_step09_anomaly_register.csv"
)

data = pd.read_csv(INPUT_FILE)

# Identify unusually large or unusually small November values.
# These thresholds are screening rules, not proof of data errors.
large_increase = data["november_to_reference_ratio"] >= 10
large_decrease = data["november_to_reference_ratio"] <= 0.1

register = data.loc[large_increase | large_decrease].copy()

# Assign a descriptive anomaly category.
register["anomaly_category"] = "Requires review"

register.loc[
    large_increase.loc[register.index],
    "anomaly_category",
] = "November value unusually high"

register.loc[
    large_decrease.loc[register.index],
    "anomaly_category",
] = "November value unusually low"

# Preserve the values and recommend review rather than automatic correction.
register["recommended_treatment"] = (
    "Preserve original value; flag for review; "
    "exclude from baseline trend comparisons pending verification"
)

register["evidence"] = (
    "Raw CSV and original Excel value matched; "
    "neighboring reporting periods differ substantially"
)

# Keep the most useful fields first.
columns = [
    "botanical_name_part",
    "trade_name_part",
    "market",
    "Nov 2022 - 1",
    "neighbor_reference_median",
    "november_to_reference_ratio",
    "absolute_percentage_difference",
    "anomaly_category",
    "recommended_treatment",
    "evidence",
]

register = register[columns].sort_values(
    ["anomaly_category", "botanical_name_part", "market"]
)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
register.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print(f"Anomaly records registered: {len(register):,}")

print("\nCounts by anomaly category:")
print(register["anomaly_category"].value_counts().to_string())

print("\nAffected plants:")
print(
    register.groupby(
        ["botanical_name_part", "trade_name_part", "anomaly_category"]
    ).size().to_string()
)

print(f"\nRegister saved to: {OUTPUT_FILE}")
