
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "reports"
OUTPUT_FILE = REPORT_DIR / "EDA_supporting_files_audit.csv"
REPORT_FILE = REPORT_DIR / "EDA_consolidated_report.md"

# Supporting files referenced by the consolidated EDA report.
expected_files = [
    "workbook_audit.csv",
    "worksheet_audit.csv",
    "period_coverage.csv",
    "price_quality_audit.csv",
    "price_exceptions.csv",
    "cleaning_summary.csv",
    "numeric_price_summary_by_year.csv",
    "numeric_price_summary_by_market.csv",
    "zero_negative_price_review.csv",
    "analytical_dataset_validation.txt",
    "eda_step01_readiness_by_status.csv",
    "eda_step01_readiness_by_year.csv",
    "eda_step02_plant_coverage.csv",
    "eda_step02_market_coverage.csv",
    "eda_step03_plant_market_pairs.csv",
    "eda_step04_pair_thresholds.csv",
    "eda_step05_price_distributions.csv",
    "eda_step06_iqr_outliers.csv",
    "eda_step07_outlier_patterns_by_pair.csv",
    "eda_step09_price_changes.csv",
    "eda_step09_sudden_movements.csv",
    "eda_step09_source_spike_investigation.csv",
    "eda_step09_raw_vs_analytical_spike_check.csv",
    "eda_step09_original_excel_spike_verification.csv",
    "eda_step09_november_spike_comparison.csv",
    "eda_step09_anomaly_register.csv",
]

audit_rows = []

# Check this file in its actual location rather than in reports/.
processed_file = ROOT / "data" / "processed" / "unprocessed_worksheets.csv"

audit_rows = [{
    "filename": "data/processed/unprocessed_worksheets.csv",
    "exists": processed_file.exists(),
    "read_status": (
        "CSV readable"
        if processed_file.exists()
        else "Missing"
    ),
    "row_count": "",
    "column_count": "",
    "columns": "",
}]

if processed_file.exists():
    try:
        df = pd.read_csv(processed_file, nrows=0)
        audit_rows[0]["column_count"] = len(df.columns)
        audit_rows[0]["columns"] = " | ".join(map(str, df.columns))

        with processed_file.open(
            "r", encoding="utf-8-sig", errors="replace"
        ) as f:
            audit_rows[0]["row_count"] = max(
                sum(1 for _ in f) - 1, 0
            )
    except Exception as exc:
        audit_rows[0]["read_status"] = (
            f"Read error: {type(exc).__name__}: {exc}"
        )

for filename in expected_files:
    path = REPORT_DIR / filename

    row = {
        "filename": filename,
        "exists": path.exists(),
        "read_status": "",
        "row_count": "",
        "column_count": "",
        "columns": "",
    }

    if not path.exists():
        row["read_status"] = "Missing"
        audit_rows.append(row)
        continue

    try:
        if path.suffix.lower() == ".csv":
            df = pd.read_csv(path, nrows=0)
            row["column_count"] = len(df.columns)
            row["columns"] = " | ".join(map(str, df.columns))

            # Count data rows without loading the whole file into memory.
            with path.open("r", encoding="utf-8-sig", errors="replace") as f:
                row["row_count"] = max(sum(1 for _ in f) - 1, 0)

            row["read_status"] = "CSV readable"

        elif path.suffix.lower() == ".txt":
            content = path.read_text(encoding="utf-8", errors="replace")
            row["row_count"] = len(content.splitlines())
            row["read_status"] = "Text readable"

        else:
            row["read_status"] = "Exists; format not inspected"

    except Exception as exc:
        row["read_status"] = f"Read error: {type(exc).__name__}: {exc}"

    audit_rows.append(row)

audit = pd.DataFrame(audit_rows)
audit.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("=== Supporting-file audit ===")
print(f"Expected files: {len(audit):,}")
print(f"Files found: {audit['exists'].sum():,}")
print(f"Files missing: {(~audit['exists']).sum():,}")

print("\nMissing files:")
missing = audit.loc[~audit["exists"], "filename"]
print(missing.to_string(index=False) if len(missing) else "None")

print("\nFiles with read errors:")
errors = audit[
    audit["read_status"].str.startswith("Read error", na=False)
]
print(
    errors[["filename", "read_status"]].to_string(index=False)
    if len(errors)
    else "None"
)

print("\n=== Key report claim checks ===")

if REPORT_FILE.exists():
    text = REPORT_FILE.read_text(encoding="utf-8")

    claims = {
        "Total observations": "374,830",
        "Plant identifiers": "110",
        "Markets": "31",
        "Positive numeric prices": "71,890",
        "November anomaly pairs": "18",
        "No automatic correction caveat": "not automatically",
        "Unverified price-unit caveat": "unit",
    }

    for label, phrase in claims.items():
        print(f"{label}: {'FOUND' if phrase.lower() in text.lower() else 'CHECK'}")
else:
    print("Consolidated EDA report is missing.")

print(f"\nAudit file saved to: {OUTPUT_FILE}")

print(
    "\nNext, review the column names and row counts in this audit "
    "before reconciling individual numerical claims."
)
