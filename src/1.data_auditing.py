from pathlib import Path
import pandas as pd

# Locate the project and original Excel files.
PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw" / "price_wise"
REPORT_DIR = PROJECT_DIR / "reports"

# Create the reports directory if it does not exist.
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Find supported Excel workbooks.
excel_files = sorted(
    path for path in RAW_DIR.glob("*")
    if path.suffix.lower() in {".xlsx", ".xlsm", ".xls"}
    and not path.name.startswith("~$")
)

if not excel_files:
    raise FileNotFoundError(
        f"No Excel files found in: {RAW_DIR}\n"
        "Check that the workbooks are in the correct folder."
    )

workbook_report = []
sheet_report = []

for file_path in excel_files:
    print(f"\nInspecting workbook: {file_path.name}")

    # Read workbook metadata without modifying the original file.
    try:
        excel_file = pd.ExcelFile(file_path)
    except Exception as error:
        workbook_report.append({
            "file": file_path.name,
            "status": f"Could not open: {error}",
            "sheet_count": None,
        })
        continue

    workbook_report.append({
        "file": file_path.name,
        "status": "Opened successfully",
        "sheet_count": len(excel_file.sheet_names),
    })

    for sheet_name in excel_file.sheet_names:
        # Read the first rows without assuming where headers begin.
        preview = pd.read_excel(
            excel_file,
            sheet_name=sheet_name,
            header=None,
            nrows=8,
        )

        # Read the sheet dimensions for an initial structural check.
        full_sheet = pd.read_excel(
            excel_file,
            sheet_name=sheet_name,
            header=None,
        )

        sheet_report.append({
            "file": file_path.name,
            "sheet_name": sheet_name,
            "row_count": len(full_sheet),
            "column_count": full_sheet.shape[1],
            "non_empty_cells": int(full_sheet.notna().sum().sum()),
            "first_rows_preview": preview.to_string(index=False, header=False),
        })

        print(f"\n  Sheet: {sheet_name}")
        print(f"  Rows: {len(full_sheet)}")
        print(f"  Columns: {full_sheet.shape[1]}")
        print("  First rows:")
        print(preview.to_string(index=False, header=False))

# Save the structural audit reports separately from the source data.
pd.DataFrame(workbook_report).to_csv(
    REPORT_DIR / "workbook_audit.csv", index=False
)

pd.DataFrame(sheet_report).to_csv(
    REPORT_DIR / "worksheet_audit.csv", index=False
)

print("\nAudit completed.")
print(f"Workbook report: {REPORT_DIR / 'workbook_audit.csv'}")
print(f"Worksheet report: {REPORT_DIR / 'worksheet_audit.csv'}")
