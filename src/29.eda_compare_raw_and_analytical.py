
from pathlib import Path
import pandas as pd

# Project folders
ROOT = Path(__file__).resolve().parent.parent

RAW_FILE = ROOT / "data" / "processed" / "medicinal_plant_prices_raw_long.csv"
ANALYTICAL_FILE = ROOT / "data" / "processed" / "medicinal_plant_prices_analytical.csv"
OUTPUT_FILE = ROOT / "reports" / "eda_step09_raw_vs_analytical_spike_check.csv"

# Read both datasets without changing the source files.
raw = pd.read_csv(RAW_FILE, dtype=str, keep_default_na=False)
analytical = pd.read_csv(ANALYTICAL_FILE, dtype=str, keep_default_na=False)

print("Raw dataset columns:")
print(raw.columns.tolist())

print("\nAnalytical dataset columns:")
print(analytical.columns.tolist())

# Match records using the fields that uniquely identify an observation.
keys = [
    "source_year",
    "source_sheet",
    "botanical_name_part",
    "trade_name_part",
    "market",
]

# Stop with a clear message if the expected identifying fields are missing.
for column in keys + ["original_price_value"]:
    if column not in raw.columns:
        raise ValueError(f"Missing column in raw dataset: {column}")

for column in keys:
    if column not in analytical.columns:
        raise ValueError(f"Missing column in analytical dataset: {column}")

# Keep the three plants involved in the November 2022 investigation.
plant_terms = [
    "Black bitumen",
    "Embelia ribes",
    "Gmelina arborea",
]

plant_mask = pd.Series(False, index=raw.index)

for term in plant_terms:
    plant_mask |= (
        raw["botanical_name_part"].str.contains(term, case=False, regex=False)
        | raw["trade_name_part"].str.contains(term, case=False, regex=False)
    )

# Restrict the comparison to October, November, and December 2022.
period_mask = (
    raw["source_year"].eq("2022")
    & raw["source_sheet"].str.match(r"^(Oct|Nov|Dec) 2022", case=False)
)

raw_subset = raw.loc[plant_mask & period_mask].copy()

# Add suffixes so raw and analytical fields can be distinguished.
comparison = raw_subset.merge(
    analytical,
    on=keys,
    how="left",
    suffixes=("_raw", "_analytical"),
    indicator=True,
    validate="one_to_one",
)

# Select useful fields for reviewing original values and analytical results.
preferred_columns = [
    "source_year",
    "source_sheet",
    "botanical_name_part",
    "trade_name_part",
    "market",
    "original_price_value_raw",
    "original_price_value_analytical",
    "analytical_price_status",
    "_merge",
]

# Keep fields that actually exist in the merged dataset.
display_columns = [
    column for column in preferred_columns
    if column in comparison.columns
]

# Save the investigation report without modifying either input dataset.
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
comparison.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("\n--- Comparison summary ---")
print(f"Raw records selected: {len(raw_subset):,}")
print(f"Matched analytical records: {(comparison['_merge'] == 'both').sum():,}")
print(f"Unmatched raw records: {(comparison['_merge'] != 'both').sum():,}")

print("\n--- Selected raw versus analytical records ---")
print(
    comparison[display_columns]
    .sort_values(["botanical_name_part", "market", "source_sheet"])
    .to_string(index=False, max_rows=80)
)

print(f"\nFull report saved to: {OUTPUT_FILE}")
