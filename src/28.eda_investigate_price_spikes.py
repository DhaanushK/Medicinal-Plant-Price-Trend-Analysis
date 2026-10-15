
from pathlib import Path
import pandas as pd


# --------------------------------------------------
# 1. DEFINE PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "medicinal_plant_prices_analytical.csv"
)

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = REPORT_DIR / "eda_step09_source_spike_investigation.csv"


# --------------------------------------------------
# 2. LOAD THE ANALYTICAL DATASET
# --------------------------------------------------

df = pd.read_csv(
    INPUT_FILE,
    dtype=str,
    keep_default_na=False,
)

# Build the same plant identifier used in earlier EDA steps.
df["plant_identifier"] = (
    df["botanical_name_part"].str.strip()
    + " | "
    + df["trade_name_part"].str.strip()
)

# Convert price values only for inspection.
df["numeric_price"] = pd.to_numeric(
    df["analytical_price"],
    errors="coerce",
)

# Select the three plants involved in the sudden movements.
plant_patterns = [
    "Gmelina arborea-Bark",
    "Embelia ribes-Seed",
    "Black bitumen-Stone",
]

selected = df[
    df["botanical_name_part"].str.strip().isin(plant_patterns)
    & df["source_year"].isin(["2022"])
].copy()


# --------------------------------------------------
# 3. KEEP OCTOBER, NOVEMBER, AND DECEMBER WORKSHEETS
# --------------------------------------------------

# Normalize whitespace for matching; preserve source_sheet unchanged.
normalized_sheet = (
    selected["source_sheet"]
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

selected = selected[
    normalized_sheet.str.match(
        r"^(Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+2022\s*-\s*[12]$",
        case=False,
    )
].copy()


# --------------------------------------------------
# 4. SELECT AVAILABLE SOURCE AND ANALYSIS FIELDS
# --------------------------------------------------

preferred_columns = [
    "plant_identifier",
    "botanical_name_part",
    "trade_name_part",
    "market",
    "source_year",
    "source_sheet",
    "analytical_price",
    "numeric_price",
    "analytical_price_status",
]

output_columns = [
    column for column in preferred_columns
    if column in selected.columns
]

selected = selected[output_columns].sort_values(
    ["plant_identifier", "market", "source_sheet"]
)

selected.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig",
)


# --------------------------------------------------
# 5. PRINT THE INVESTIGATION RESULTS
# --------------------------------------------------

print("=" * 70)
print("EDA STEP 9.7: SOURCE PRICE-SPIKE INVESTIGATION")
print("=" * 70)

print(f"Matching source observations: {len(selected):,}")

if not selected.empty:
    print("\nObservation counts by plant and worksheet:")
    print(
        selected.groupby(
            ["plant_identifier", "source_sheet"]
        )
        .agg(
            observations=("market", "size"),
            positive_numeric_prices=("numeric_price",
                                      lambda values: (values > 0).sum()),
            minimum_numeric_price=("numeric_price", "min"),
            median_numeric_price=("numeric_price", "median"),
            maximum_numeric_price=("numeric_price", "max"),
        )
        .to_string()
    )

    print("\nIndividual source records:")
    print(selected.to_string(index=False))
else:
    print(
        "No matching rows found. Check the botanical-name labels "
        "and worksheet names in the source dataset."
    )

print("\nReport saved:")
print(OUTPUT_FILE)

print(
    "\nThis investigation preserves recorded values. "
    "It does not classify any price as an error automatically."
)
