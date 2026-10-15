
from pathlib import Path
import pandas as pd

# Locate the project and reports folders.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "reports"

# Supporting files containing the report's key numerical claims.
FILES_TO_INSPECT = [
    "eda_step01_readiness_by_year.csv",
    "eda_step02_plant_coverage.csv",
    "eda_step02_market_coverage.csv",
    "eda_step03_plant_market_pairs.csv",
    "eda_step04_pair_thresholds.csv",
    "eda_step05_price_distributions.csv",
    "eda_step06_outlier_summary.csv",
    "eda_step07_outlier_patterns_by_year.csv",
    "eda_step07_outlier_patterns_by_market.csv",
    "eda_step09_price_change_summary.csv",
    "eda_step09_sudden_movements.csv",
    "eda_step09_source_spike_investigation.csv",
    "eda_step09_raw_vs_analytical_spike_check.csv",
    "eda_step09_original_excel_spike_verification.csv",
    "eda_step09_november_spike_comparison.csv",
    "eda_step09_anomaly_register.csv",
]

print("=" * 75)
print("EDA SUPPORTING FILE SCHEMA INSPECTION")
print("=" * 75)

inspection_results = []

for filename in FILES_TO_INSPECT:
    file_path = REPORT_DIR / filename

    print(f"\n{'-' * 75}")
    print(f"FILE: {filename}")

    if not file_path.exists():
        print("STATUS: FILE NOT FOUND")
        inspection_results.append({
            "file": filename,
            "status": "Missing",
            "rows": None,
            "columns": "",
        })
        continue

    try:
        # Read the CSV without altering the original file.
        data = pd.read_csv(file_path, low_memory=False)

        print(f"Rows: {len(data):,}")
        print(f"Columns ({len(data.columns)}): {list(data.columns)}")

        # Show at most two rows to understand the file's structure.
        if not data.empty:
            print("\nSample records:")
            print(data.head(2).to_string(index=False))
        else:
            print("The file contains headers but no data rows.")

        inspection_results.append({
            "file": filename,
            "status": "Read successfully",
            "rows": len(data),
            "columns": " | ".join(map(str, data.columns)),
        })

    except Exception as error:
        print(f"STATUS: READ ERROR — {error}")
        inspection_results.append({
            "file": filename,
            "status": f"Read error: {error}",
            "rows": None,
            "columns": "",
        })

# Save a compact inventory for later auditing.
inventory = pd.DataFrame(inspection_results)
output_path = REPORT_DIR / "EDA_support_schema_inventory.csv"
inventory.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"\n{'=' * 75}")
print(f"Inspection inventory saved to: {output_path}")
print("=" * 75)
