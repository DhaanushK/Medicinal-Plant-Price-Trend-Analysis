
from pathlib import Path
import pandas as pd

# Resolve the project folders.
ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
PROCESSED = ROOT / "data" / "processed"

checks = []


def record_check(claim, expected, actual, note=""):
    """Record whether a reported figure matches its supporting data."""
    passed = expected == actual

    checks.append({
        "claim": claim,
        "expected": expected,
        "actual": actual,
        "status": "PASS" if passed else "REVIEW",
        "note": note,
    })

    print(
        f"[{'PASS' if passed else 'REVIEW'}] {claim}: "
        f"expected={expected}, actual={actual}"
    )


def read_csv(path):
    """Read a CSV or report a clear error if it is unavailable."""
    if not path.exists():
        print(f"[MISSING] {path}")
        return None

    try:
        return pd.read_csv(path, low_memory=False)
    except Exception as error:
        print(f"[ERROR] Cannot read {path.name}: {error}")
        return None


print("=" * 72)
print("CONSOLIDATED EDA REPORT — CLAIM AUDIT")
print("=" * 72)

# 1. Analytical dataset totals and unique identifiers.
analytical = read_csv(
    PROCESSED / "medicinal_plant_prices_analytical.csv"
)

if analytical is not None:
    record_check(
        "Analytical dataset row count",
        374830,
        len(analytical),
    )

    record_check(
        "Analytical dataset column count",
        17,
        len(analytical.columns),
    )

    plant_columns = ["botanical_name_part", "trade_name_part"]

    if all(column in analytical.columns for column in plant_columns):
        unique_plants = len(analytical[plant_columns].drop_duplicates())
        record_check("Unique plant identifiers", 110, unique_plants)

    if "market" in analytical.columns:
        record_check(
            "Unique markets",
            31,
            analytical["market"].nunique(dropna=True),
        )

    if "source_year" in analytical.columns:
        years = pd.to_numeric(
            analytical["source_year"], errors="coerce"
        ).dropna()

        record_check(
            "Number of study years",
            9,
            years.nunique(),
            "Expected coverage: 2017–2025",
        )

# 2. Plant-market coverage and thresholds.
pairs = read_csv(REPORTS / "eda_step03_plant_market_pairs.csv")

if pairs is not None:
    record_check("Plant-market pair count", 3410, len(pairs))

thresholds = read_csv(REPORTS / "eda_step04_pair_thresholds.csv")

if thresholds is not None:
    threshold_column = "minimum_positive_observations"
    count_column = "qualifying_pairs"

    if threshold_column in thresholds.columns and count_column in thresholds.columns:
        for threshold, expected in [(1, 2445), (5, 2058), (10, 1962), (20, 1684)]:
            rows = thresholds[
                pd.to_numeric(
                    thresholds[threshold_column], errors="coerce"
                ) == threshold
            ]

            if len(rows) == 1:
                actual = int(rows.iloc[0][count_column])
                record_check(
                    f"Pairs with at least {threshold} positive prices",
                    expected,
                    actual,
                )
            else:
                print(f"[REVIEW] Threshold {threshold}: expected one row.")

# 3. IQR outlier totals.
outliers = read_csv(REPORTS / "eda_step06_iqr_outliers.csv")

if outliers is not None:
    record_check("IQR-flagged observations", 2402, len(outliers))

outlier_groups = read_csv(REPORTS / "eda_step06_outlier_summary.csv")

if outlier_groups is not None:
    record_check("Plant-market groups with IQR flags", 806, len(outlier_groups))

    if "flagged_observations" in outlier_groups.columns:
        total_flagged = int(
            pd.to_numeric(
                outlier_groups["flagged_observations"], errors="coerce"
            ).sum()
        )

        record_check(
            "Sum of grouped IQR-flagged observations",
            2402,
            total_flagged,
        )

# 4. Historical price-change totals.
monthly_changes = read_csv(REPORTS / "eda_step09_price_changes.csv")

if monthly_changes is not None:
    record_check(
        "Monthly records in price-change analysis",
        40634,
        len(monthly_changes),
    )

change_summary = read_csv(
    REPORTS / "eda_step09_price_change_summary.csv"
)

if change_summary is not None:
    record_check(
        "Candidate plant-market pairs for price changes",
        1949,
        len(change_summary),
    )

    for column, expected, label in [
        ("available_mom_comparisons", 32044, "Available MoM comparisons"),
        ("available_yoy_comparisons", 11417, "Available YoY comparisons"),
    ]:
        if column in change_summary.columns:
            actual = int(
                pd.to_numeric(
                    change_summary[column], errors="coerce"
                ).fillna(0).sum()
            )
            record_check(label, expected, actual)

# 5. Sudden movement count.
movements = read_csv(REPORTS / "eda_step09_sudden_movements.csv")

if movements is not None:
    record_check("Flagged sudden movements", 279, len(movements))

# 6. November 2022 anomaly evidence.
spike = read_csv(REPORTS / "eda_step09_source_spike_investigation.csv")
raw_check = read_csv(REPORTS / "eda_step09_raw_vs_analytical_spike_check.csv")
excel_check = read_csv(REPORTS / "eda_step09_original_excel_spike_verification.csv")
anomalies = read_csv(REPORTS / "eda_step09_anomaly_register.csv")

if spike is not None:
    record_check("Source-spike investigation records", 465, len(spike))

if raw_check is not None:
    record_check("Raw-to-analytical matched records", 465, len(raw_check))

if excel_check is not None:
    record_check("Original Excel verification records", 465, len(excel_check))

    if "verification_status" in excel_check.columns:
        counts = excel_check["verification_status"].value_counts()

        record_check(
            "Exact Excel value matches",
            108,
            int(counts.get("Exact value match", 0)),
        )

        record_check(
            "Equivalent missing representations",
            357,
            int(counts.get("Equivalent missing representation", 0)),
        )

if anomalies is not None:
    record_check("November anomaly-register records", 18, len(anomalies))

    if "anomaly_category" in anomalies.columns:
        categories = anomalies["anomaly_category"].astype(str)

        high_count = int(categories.str.contains("high", case=False).sum())
        low_count = int(categories.str.contains("low", case=False).sum())

        record_check("Unusually high November anomalies", 12, high_count)
        record_check("Unusually low November anomalies", 6, low_count)

# 7. Save the results.
audit = pd.DataFrame(checks)
output_path = REPORTS / "EDA_report_claim_audit.csv"

audit.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\n" + "=" * 72)
print("AUDIT SUMMARY")
print("=" * 72)

if not audit.empty:
    print(audit["status"].value_counts().to_string())

print(f"\nAudit results saved to: {output_path}")
print("REVIEW results require investigation; they are not automatically errors.")
