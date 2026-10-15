
from pathlib import Path
import pandas as pd

# Load the cleaned dataset.
PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "medicinal_plant_prices_cleaned.csv"
)
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(
    INPUT_FILE,
    dtype=str,
    keep_default_na=False,
)

# Convert only the analytical price field for validation.
# Original source values remain unchanged.
df["numeric_price"] = pd.to_numeric(
    df["analytical_price"],
    errors="coerce",
)

prices = df["numeric_price"]
valid = prices.notna()

valid_prices = prices[valid]

print("=" * 60)
print("NUMERIC PRICE VALIDATION")
print("=" * 60)

print(f"\nTotal observations: {len(df):,}")
print(f"Parsed numeric prices: {int(valid.sum()):,}")
print(f"Unparsed or unavailable prices: {int((~valid).sum()):,}")

if not valid_prices.empty:
    print("\nOverall numeric distribution:")
    print(valid_prices.describe(
        percentiles=[0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
    ).to_string())

    print(f"\nZero prices: {int((valid_prices == 0).sum()):,}")
    print(f"Negative prices: {int((valid_prices < 0).sum()):,}")

# Summarize numeric prices by reporting year.
year_summary = (
    df.loc[valid]
    .groupby("source_year")["numeric_price"]
    .agg(
        observation_count="count",
        minimum="min",
        median="median",
        mean="mean",
        maximum="max",
    )
    .reset_index()
)

year_summary.to_csv(
    REPORT_DIR / "numeric_price_summary_by_year.csv",
    index=False,
)

# Summarize numeric prices by market.
market_summary = (
    df.loc[valid]
    .groupby("market")["numeric_price"]
    .agg(
        observation_count="count",
        minimum="min",
        median="median",
        mean="mean",
        maximum="max",
    )
    .reset_index()
    .sort_values("observation_count", ascending=False)
)

market_summary.to_csv(
    REPORT_DIR / "numeric_price_summary_by_market.csv",
    index=False,
)

# Save zero and negative records for review.
# Do not delete or automatically correct them.
review = df.loc[
    valid & (df["numeric_price"] <= 0)
].copy()

review.to_csv(
    REPORT_DIR / "zero_negative_price_review.csv",
    index=False,
)

print("\nSaved reports:")
print(REPORT_DIR / "numeric_price_summary_by_year.csv")
print(REPORT_DIR / "numeric_price_summary_by_market.csv")
print(REPORT_DIR / "zero_negative_price_review.csv")

print("\nNo prices were removed or changed in the cleaned dataset.")
