
from pathlib import Path
import pandas as pd

# Read the individual Excel files, including the corrected 2023 workbook.
PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw" / "price_wise"
REPORT_DIR = PROJECT_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

results = []

# Inspect only workbooks from the agreed study period.
excel_files = sorted(
    path for path in RAW_DIR.iterdir()
    if path.suffix.lower() in {".xlsx", ".xlsm", ".xls"}
    and path.stem.isdigit()
    and 2017 <= int(path.stem) <= 2025
    and not path.name.startswith("~$")
)

if not excel_files:
    raise FileNotFoundError(
        f"No annual Excel files found in {RAW_DIR}"
    )

for file_path in excel_files:
    print(f"Inspecting {file_path.name}")

    excel = pd.ExcelFile(file_path)

    for sheet in excel.sheet_names:
        raw = pd.read_excel(
            excel,
            sheet_name=sheet,
            header=None,
        )

        # Record empty sheets without attempting price analysis.
        if raw.empty or raw.shape[1] < 3:
            results.append({
                "file": file_path.name,
                "sheet": sheet,
                "status": "Empty or insufficient columns",
                "plant_rows": max(0, len(raw) - 1),
                "market_columns": max(0, raw.shape[1] - 2),
                "non_empty_price_cells": 0,
                "zero_like_cells": 0,
                "comma_containing_cells": 0,
                "non_numeric_cells": 0,
            })
            continue

        # First row contains column headings.
        # First two columns identify the medicinal plant.
        data = raw.iloc[1:, 2:].copy()

        # Keep the original values; use text only for diagnosis.
        text = data.astype("string").apply(
            lambda column: column.str.strip()
        )

        populated = data.notna() & text.ne("")
        zero_like = text.isin(
            ["0", "0.0", "0.00", "0,0", "0,00"]
        )

        # Count values containing commas for manual review.
        comma_values = text.apply(
            lambda column: column.str.contains(
                ",", regex=False, na=False
            )
        )

        # Diagnostic conversion only; never write it back to source.
        numeric = data.apply(
            pd.to_numeric, errors="coerce"
        )

        non_numeric = populated & numeric.isna()

        # Do not double-count recognized zero-like entries as text.
        non_numeric_other = non_numeric & ~zero_like

        results.append({
            "file": file_path.name,
            "sheet": sheet,
            "status": "Read successfully",
            "plant_rows": len(raw) - 1,
            "market_columns": raw.shape[1] - 2,
            "non_empty_price_cells": int(populated.sum().sum()),
            "zero_like_cells": int(zero_like.sum().sum()),
            "comma_containing_cells": int(
                (comma_values & populated).sum().sum()
            ),
            "non_numeric_cells": int(
                non_numeric_other.sum().sum()
            ),
        })

# Save the revised audit separately from the source data.
report = pd.DataFrame(results)
output_file = REPORT_DIR / "price_quality_audit.csv"
report.to_csv(output_file, index=False)

print("\nPrice-quality audit completed.")
print(f"Workbooks inspected: {len(excel_files)}")
print(f"Worksheets inspected: {len(report)}")
print(f"Report saved to: {output_file}")

print("\nMarch 2023 verification:")
print(
    report[
        (report["file"] == "2023.xlsx")
        & (report["sheet"] == "Mar 2023 - 1")
    ].to_string(index=False)
)
