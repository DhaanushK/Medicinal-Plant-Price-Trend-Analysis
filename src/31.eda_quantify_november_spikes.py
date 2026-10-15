
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    ROOT / "data" / "processed"
    / "medicinal_plant_prices_analytical.csv"
)
OUTPUT_FILE = (
    ROOT / "reports"
    / "eda_step09_november_spike_comparison.csv"
)

data = pd.read_csv(INPUT_FILE, dtype=str, keep_default_na=False)

# Focus on the three plants involved in the source-level investigation.
plant_terms = ["Black bitumen", "Embelia ribes", "Gmelina arborea"]

plant_mask = pd.Series(False, index=data.index)

for term in plant_terms:
    plant_mask |= (
        data["botanical_name_part"].str.contains(
            term, case=False, regex=False
        )
        | data["trade_name_part"].str.contains(
            term, case=False, regex=False
        )
    )

# Keep the surrounding source worksheets for 2022.
sheets = [
    "Oct 2022 - 1",
    "Nov 2022 - 1",
    "Nov 2022 - 2",
    "Dec 2022 - 1",
    "Dec 2022 - 2",
]

subset = data.loc[
    plant_mask
    & data["source_year"].eq("2022")
    & data["source_sheet"].isin(sheets)
].copy()

# Convert accepted analytical prices to numeric values.
# Unavailable or review-only values remain missing for this comparison.
subset["analytical_price"] = pd.to_numeric(
    subset["analytical_price"], errors="coerce"
)

# One row per plant-market pair, with each source worksheet as a column.
index_columns = [
    "botanical_name_part",
    "trade_name_part",
    "market",
]

wide = subset.pivot_table(
    index=index_columns,
    columns="source_sheet",
    values="analytical_price",
    aggfunc="first",
)

# Ensure every requested worksheet has a column, even if all values are missing.
for sheet in sheets:
    if sheet not in wide.columns:
        wide[sheet] = float("nan")

wide = wide[sheets].reset_index()

# Use the four surrounding worksheets as a reference, excluding Nov 2022 - 1.
reference_columns = [
    "Oct 2022 - 1",
    "Nov 2022 - 2",
    "Dec 2022 - 1",
    "Dec 2022 - 2",
]

wide["neighbor_reference_median"] = wide[
    reference_columns
].median(axis=1)

# Measure how far the Nov 2022 - 1 value is from the reference median.
# This is a screening measure, not proof of an error.
wide["november_minus_one"] = wide["Nov 2022 - 1"]

wide["november_to_reference_ratio"] = (
    wide["november_minus_one"]
    / wide["neighbor_reference_median"].where(
        wide["neighbor_reference_median"] > 0
    )
)

wide["absolute_percentage_difference"] = (
    (
        wide["november_minus_one"]
        - wide["neighbor_reference_median"]
    ).abs()
    / wide["neighbor_reference_median"].where(
        wide["neighbor_reference_median"] > 0
    )
    * 100
)

# Keep pairs where both the November value and reference median are available.
review = wide.loc[
    wide["november_minus_one"].notna()
    & wide["neighbor_reference_median"].notna()
].copy()

review["screening_note"] = review.apply(
    lambda row: (
        "Large November value relative to neighbors"
        if row["november_to_reference_ratio"] >= 10
        else "Small November value relative to neighbors"
        if row["november_to_reference_ratio"] <= 0.1
        else "No 10x difference under this screening rule"
    ),
    axis=1,
)

# Save the detailed comparison report.
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
review.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print(f"Plant-market pairs with a comparison: {len(review):,}")

print("\n--- Largest relative differences ---")
print(
    review.sort_values(
        "absolute_percentage_difference", ascending=False
    ).head(25).to_string(index=False)
)

print(f"\nFull report saved to: {OUTPUT_FILE}")
