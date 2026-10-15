
from pathlib import Path
import pandas as pd


# --------------------------------------------------
# 1. DEFINE PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "reports"

HISTORY_FILE = REPORT_DIR / "eda_step09_extreme_change_history.csv"

OUTPUT_FILE = REPORT_DIR / "eda_step09_sudden_movements.csv"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. LOAD THE HISTORICAL RECORDS
# --------------------------------------------------

df = pd.read_csv(HISTORY_FILE)

df["calendar_month"] = pd.to_datetime(
    df["calendar_month"],
    errors="coerce",
)

df["median_price"] = pd.to_numeric(
    df["median_price"],
    errors="coerce",
)

df = df.dropna(
    subset=["calendar_month", "median_price"]
).copy()

pair_columns = ["plant_identifier", "market"]

df = df.sort_values(
    pair_columns + ["calendar_month"]
)


# --------------------------------------------------
# 3. CHECK THAT MONTHS ARE CONSECUTIVE
# --------------------------------------------------

# Calculate the previous observed median for each pair.
df["previous_observed_month"] = (
    df.groupby(pair_columns)["calendar_month"].shift(1)
)

df["previous_observed_median"] = (
    df.groupby(pair_columns)["median_price"].shift(1)
)

# Calculate the number of calendar months between observations.
df["months_between_observations"] = (
    (df["calendar_month"].dt.year
     - df["previous_observed_month"].dt.year) * 12
    + df["calendar_month"].dt.month
    - df["previous_observed_month"].dt.month
)

# Only calculate consecutive-month changes when the previous
# observation is exactly one calendar month earlier.
df["mom_change_pct"] = (
    (
        df["median_price"] - df["previous_observed_median"]
    )
    / df["previous_observed_median"]
    * 100
).where(
    (df["months_between_observations"] == 1)
    & (df["previous_observed_median"] > 0)
)

df["mom_absolute_change"] = (
    df["median_price"] - df["previous_observed_median"]
).where(df["months_between_observations"] == 1)


# --------------------------------------------------
# 4. IDENTIFY LARGE CONSECUTIVE-MONTH MOVEMENTS
# --------------------------------------------------

# This is a review threshold, not a claim that a value is incorrect.
sudden = df[
    df["mom_change_pct"].abs() >= 50
].copy()

sudden["movement_direction"] = sudden[
    "mom_change_pct"
].apply(
    lambda value: "Increase" if value > 0 else "Decrease"
)

sudden["review_threshold_pct"] = 50

sudden = sudden.sort_values(
    "mom_change_pct",
    ascending=False,
)

sudden.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig",
)


# --------------------------------------------------
# 5. PRINT RESULTS
# --------------------------------------------------

print("=" * 70)
print("EDA STEP 9.6: SUDDEN MONTHLY PRICE MOVEMENTS")
print("=" * 70)

print(f"Historical observations reviewed: {len(df):,}")

print(
    "Consecutive-month comparisons available: "
    f"{int(df['mom_change_pct'].notna().sum()):,}"
)

print(f"Movements flagged at +/-50%: {len(sudden):,}")

if not sudden.empty:
    print("\nLargest consecutive-month increases:")
    print(
        sudden[sudden["movement_direction"] == "Increase"]
        .head(10)[
            pair_columns
            + [
                "previous_observed_month",
                "calendar_month",
                "previous_observed_median",
                "median_price",
                "mom_change_pct",
            ]
        ]
        .to_string(index=False)
    )

    print("\nLargest consecutive-month decreases:")
    print(
        sudden[sudden["movement_direction"] == "Decrease"]
        .sort_values("mom_change_pct")
        .head(10)[
            pair_columns
            + [
                "previous_observed_month",
                "calendar_month",
                "previous_observed_median",
                "median_price",
                "mom_change_pct",
            ]
        ]
        .to_string(index=False)
    )
else:
    print("\nNo consecutive-month movements met the review threshold.")

print("\nReport saved:")
print(OUTPUT_FILE)

print(
    "\nOnly consecutive calendar months are compared. "
    "Missing months are not bridged."
)
