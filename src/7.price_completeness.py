
from pathlib import Path
import pandas as pd

# Load the transformed dataset without modifying its source values.
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

# Treat only genuinely blank strings as blank in this audit.
prices = df["original_price_value"].astype(str).str.strip()
df["price_is_blank"] = prices.eq("")
df["price_is_present"] = ~df["price_is_blank"]

# Summarize completeness by year.
year_report = (
    df.groupby("source_year")
    .agg(
        total_observations=("original_price_value", "size"),
        blank_prices=("price_is_blank", "sum"),
        present_prices=("price_is_present", "sum"),
        markets=("market", "nunique"),
        reporting_sheets=("source_sheet", "nunique"),
    )
    .reset_index()
)

year_report["blank_percentage"] = (
    year_report["blank_prices"]
    / year_report["total_observations"] * 100
).round(2)

year_report["present_percentage"] = (
    year_report["present_prices"]
    / year_report["total_observations"] * 100
).round(2)

# Summarize completeness by market across the full study period.
market_report = (
    df.groupby("market")
    .agg(
        total_observations=("original_price_value", "size"),
        blank_prices=("price_is_blank", "sum"),
        present_prices=("price_is_present", "sum"),
        years=("source_year", "nunique"),
        reporting_sheets=("source_sheet", "nunique"),
    )
    .reset_index()
)

market_report["blank_percentage"] = (
    market_report["blank_prices"]
    / market_report["total_observations"] * 100
).round(2)

market_report["present_percentage"] = (
    market_report["present_prices"]
    / market_report["total_observations"] * 100
).round(2)

# Save separate reports for review.
year_path = REPORT_DIR / "price_completeness_by_year.csv"
market_path = REPORT_DIR / "price_completeness_by_market.csv"

year_report.to_csv(year_path, index=False)
market_report.to_csv(market_path, index=False)

print("PRICE COMPLETENESS AUDIT")
print(f"Total observations: {len(df):,}")
print(f"Blank price cells: {int(df['price_is_blank'].sum()):,}")
print(f"Present price cells: {int(df['price_is_present'].sum()):,}")

print("\nCompleteness by year:")
print(
    year_report[
        [
            "source_year",
            "total_observations",
            "blank_prices",
            "present_prices",
            "blank_percentage",
            "markets",
        ]
    ].to_string(index=False)
)

print("\n10 markets with the highest blank percentages:")
print(
    market_report.sort_values(
        "blank_percentage", ascending=False
    ).head(10)[
        [
            "market",
            "total_observations",
            "blank_prices",
            "present_prices",
            "blank_percentage",
        ]
    ].to_string(index=False)
)

print(f"\nSaved: {year_path}")
print(f"Saved: {market_path}")
