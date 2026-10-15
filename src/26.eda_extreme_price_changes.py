
from pathlib import Path
import pandas as pd


# --------------------------------------------------
# 1. DEFINE PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "reports"

SUMMARY_INPUT = REPORT_DIR / "eda_step09_price_change_summary.csv"
DETAIL_INPUT = REPORT_DIR / "eda_step09_price_changes.csv"

EXTREME_REPORT = REPORT_DIR / "eda_step09_extreme_change_review.csv"
HISTORY_REPORT = REPORT_DIR / "eda_step09_extreme_change_history.csv"

PAIR_COLUMNS = ["plant_identifier", "market"]


# --------------------------------------------------
# 2. LOAD EXISTING PRICE-CHANGE REPORTS
# --------------------------------------------------

summary = pd.read_csv(SUMMARY_INPUT)
monthly = pd.read_csv(DETAIL_INPUT)

summary["overall_observed_change_pct"] = pd.to_numeric(
    summary["overall_observed_change_pct"],
    errors="coerce",
)

summary["first_observed_month"] = pd.to_datetime(
    summary["first_observed_month"],
    errors="coerce",
)

summary["last_observed_month"] = pd.to_datetime(
    summary["last_observed_month"],
    errors="coerce",
)

monthly["calendar_month"] = pd.to_datetime(
    monthly["calendar_month"],
    errors="coerce",
)


# --------------------------------------------------
# 3. FLAG EXTREME OBSERVED CHANGES
# --------------------------------------------------

# A change of +/-100% is a review flag, not proof of an error.
extreme = summary[
    summary["overall_observed_change_pct"].abs() >= 100
].copy()

extreme["change_direction"] = extreme[
    "overall_observed_change_pct"
].apply(
    lambda value: (
        "Increase" if value > 0 else "Decrease"
    )
)

extreme["review_reason"] = (
    "Absolute first-to-latest observed change is at least 100%; "
    "inspect the monthly history and source records."
)

extreme = extreme.sort_values(
    "overall_observed_change_pct",
    ascending=False,
)

extreme.to_csv(
    EXTREME_REPORT,
    index=False,
    encoding="utf-8-sig",
)


# --------------------------------------------------
# 4. EXTRACT MONTHLY HISTORY FOR FLAGGED PAIRS
# --------------------------------------------------

# Retain all available monthly records for the flagged pairs.
history = monthly.merge(
    extreme[PAIR_COLUMNS].drop_duplicates(),
    on=PAIR_COLUMNS,
    how="inner",
    validate="many_to_one",
)

history = history.sort_values(
    PAIR_COLUMNS + ["calendar_month"]
)

history.to_csv(
    HISTORY_REPORT,
    index=False,
    encoding="utf-8-sig",
)


# --------------------------------------------------
# 5. PRINT SUMMARY
# --------------------------------------------------

print("=" * 70)
print("EDA STEP 9.5: EXTREME PRICE-CHANGE REVIEW")
print("=" * 70)

print(f"Plant-market pairs assessed: {len(summary):,}")
print(f"Pairs flagged for review: {len(extreme):,}")

print("\nFlagged increases: "
      f"{(extreme['change_direction'] == 'Increase').sum():,}")

print("Flagged decreases: "
      f"{(extreme['change_direction'] == 'Decrease').sum():,}")

display_columns = [
    "plant_identifier",
    "market",
    "first_observed_month",
    "last_observed_month",
    "first_observed_median",
    "latest_observed_median",
    "overall_observed_change_pct",
    "elapsed_months",
]

print("\nLargest flagged increases:")
print(
    extreme[extreme["change_direction"] == "Increase"]
    .head(10)[display_columns]
    .to_string(index=False)
)

print("\nLargest flagged decreases:")
print(
    extreme[extreme["change_direction"] == "Decrease"]
    .sort_values("overall_observed_change_pct")
    .head(10)[display_columns]
    .to_string(index=False)
)

print("\nReports saved:")
print(EXTREME_REPORT)
print(HISTORY_REPORT)

print(
    "\nThese flags identify changes for investigation; "
    "they do not establish that a price is incorrect."
)
