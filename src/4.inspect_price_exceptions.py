
from pathlib import Path
import pandas as pd

# Read the latest individual workbooks, not the old ZIP.
PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw" / "price_wise"
OUTPUT_FILE = PROJECT_DIR / "reports" / "price_exceptions.csv"

exceptions = []

excel_files = sorted(
    path for path in RAW_DIR.iterdir()
    if path.suffix.lower() in {".xlsx", ".xlsm", ".xls"}
    and path.stem.isdigit()
    and 2017 <= int(path.stem) <= 2025
    and not path.name.startswith("~$")
)

for file_path in excel_files:
    excel = pd.ExcelFile(file_path)

    for sheet in excel.sheet_names:
        raw = pd.read_excel(
            excel,
            sheet_name=sheet,
            header=None,
        )

        if raw.empty or raw.shape[1] < 3:
            continue

        # The first row contains market names.
        # The first two columns identify each medicinal plant.
        headers = raw.iloc[0]
        data = raw.iloc[1:]

        for row_index in data.index:
            botanical = raw.iloc[row_index, 0]
            trade_name = raw.iloc[row_index, 1]

            for col_index in range(2, raw.shape[1]):
                value = raw.iloc[row_index, col_index]

                if pd.isna(value):
                    continue

                original_text = str(value).strip()
                normalized = original_text.replace(",", ".")

                # Check whether the original value is numeric.
                try:
                    float(normalized)
                    is_numeric = True
                except ValueError:
                    is_numeric = False

                # Identify zero-like values and values needing review.
                is_zero_like = normalized in {
                    "0", "0.0", "0.00"
                }
                contains_comma = "," in original_text

                if is_zero_like or not is_numeric or contains_comma:
                    if is_zero_like:
                        issue = "Zero-like value"
                    elif not is_numeric:
                        issue = "Non-numeric value"
                    else:
                        issue = "Comma-formatted value"

                    exceptions.append({
                        "workbook": file_path.name,
                        "worksheet": sheet,
                        "botanical_name_part": botanical,
                        "trade_name_part": trade_name,
                        "market": headers.iloc[col_index],
                        "original_value": original_text,
                        "issue": issue,
                    })

# Save the investigation list without modifying source workbooks.
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

report = pd.DataFrame(exceptions)
report.to_csv(OUTPUT_FILE, index=False)

print(f"Flagged entries: {len(report)}")
print(f"Report saved to: {OUTPUT_FILE}")

if not report.empty:
    print("\nIssue counts:")
    print(report["issue"].value_counts().to_string())

    print("\nSample entries:")
    print(report.head(25).to_string(index=False))
