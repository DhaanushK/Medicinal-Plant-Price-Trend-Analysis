
from pathlib import Path
import calendar
import re
import pandas as pd

# Locate the project and source folders.
PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw" / "price_wise"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Restrict the analysis to our agreed study period.
START_YEAR = 2017
END_YEAR = 2025

# Match worksheet names such as:
# Jan 2019 - 1, Jan 2019 - 2, Sept 2018 -1
PERIOD_PATTERN = re.compile(
    r"^([A-Za-z]{3,9})\s+(\d{4})\s*-\s*([12])$"
)

MONTH_LOOKUP = {
    name.lower(): number
    for number, name in enumerate(calendar.month_name)
    if name
}
MONTH_LOOKUP.update({
    name.lower(): number
    for number, name in enumerate(calendar.month_abbr)
    if name
})
# Support the alternative four-letter abbreviation used in the source.
MONTH_LOOKUP["sept"] = 9

def parse_period(sheet_name):
    """Extract the month, year, and suffix from a worksheet name."""
    match = PERIOD_PATTERN.match(str(sheet_name).strip())

    if not match:
        return None

    month_text, year_text, suffix_text = match.groups()
    month = MONTH_LOOKUP.get(month_text.lower())

    if month is None:
        return None

    year = int(year_text)

    if not START_YEAR <= year <= END_YEAR:
        return None

    return {
        "reporting_month": month,
        "reporting_month_name": calendar.month_abbr[month],
        "source_year": year,
        "suffix": int(suffix_text),
    }

# Find the annual Excel files directly, not the older ZIP.
workbooks = sorted(
    path for path in RAW_DIR.iterdir()
    if path.suffix.lower() in {".xlsx", ".xlsm", ".xls"}
    and path.stem.isdigit()
    and START_YEAR <= int(path.stem) <= END_YEAR
    and not path.name.startswith("~$")
)

if not workbooks:
    raise FileNotFoundError(
        f"No annual Excel workbooks found in {RAW_DIR}"
    )

# First pass: identify which suffixes exist for each month and year.
period_inventory = []

for workbook in workbooks:
    excel = pd.ExcelFile(workbook)

    for sheet_name in excel.sheet_names:
        period = parse_period(sheet_name)

        if period is not None:
            period_inventory.append({
                "workbook": workbook.name,
                "source_sheet": sheet_name,
                **period,
            })

inventory = pd.DataFrame(period_inventory)

if inventory.empty:
    raise ValueError("No worksheet names matched the period pattern.")

suffixes_by_month = (
    inventory.groupby(["source_year", "reporting_month"])["suffix"]
    .apply(set)
    .to_dict()
)

# Second pass: reshape each worksheet into one row per plant-market-period.
records = []
unmatched_sheets = []

for workbook in workbooks:
    print(f"Processing {workbook.name}")
    excel = pd.ExcelFile(workbook)

    for sheet_name in excel.sheet_names:
        period = parse_period(sheet_name)

        if period is None:
            unmatched_sheets.append({
                "workbook": workbook.name,
                "source_sheet": sheet_name,
                "reason": "Worksheet name not recognized",
            })
            continue

        raw = pd.read_excel(
            excel,
            sheet_name=sheet_name,
            header=None,
        )

        if raw.empty or raw.shape[1] < 3:
            unmatched_sheets.append({
                "workbook": workbook.name,
                "source_sheet": sheet_name,
                "reason": "Empty or insufficient columns",
            })
            continue

        # The first row contains plant-field and market headings.
        headers = raw.iloc[0]
        data = raw.iloc[1:].copy()

        # Determine the fortnight using the user's rule.
        suffix_set = suffixes_by_month[
            (period["source_year"], period["reporting_month"])
        ]

        if suffix_set == {1, 2}:
            fortnight = (
                "Second" if period["suffix"] == 1 else "First"
            )
            period_status = "Both suffixes present"
        elif suffix_set == {1}:
            fortnight = "First"
            period_status = "Only suffix -1 present"
        else:
            fortnight = "Unresolved"
            period_status = "Suffix -2 only; review required"

        # Market columns start after the two plant identifier columns.
        for row_index in data.index:
            botanical = raw.iloc[row_index, 0]
            trade_name = raw.iloc[row_index, 1]

            # Skip completely empty plant rows.
            if pd.isna(botanical) and pd.isna(trade_name):
                continue

            for col_index in range(2, raw.shape[1]):
                market = headers.iloc[col_index]
                original_value = raw.iloc[row_index, col_index]

                # Preserve missing cells as explicit observations.
                # Do not convert special values or prices yet.
                records.append({
                    "source_year": period["source_year"],
                    "reporting_month": period["reporting_month"],
                    "reporting_month_name": (
                        period["reporting_month_name"]
                    ),
                    "source_suffix": period["suffix"],
                    "fortnight": fortnight,
                    "period_status": period_status,
                    "source_workbook": workbook.name,
                    "source_sheet": sheet_name,
                    "botanical_name_part": botanical,
                    "trade_name_part": trade_name,
                    "market": market,
                    "original_price_value": original_value,
                })

# Save the long-format dataset and worksheet review report.
output_file = OUTPUT_DIR / "medicinal_plant_prices_raw_long.csv"
review_file = OUTPUT_DIR / "unprocessed_worksheets.csv"

result = pd.DataFrame(records)
result.to_csv(output_file, index=False)

# Always write a consistent schema, even when no worksheets need review.
review_columns = ["workbook", "source_sheet", "reason"]

review_df = pd.DataFrame(
    unmatched_sheets,
    columns=review_columns,
)

review_df.to_csv(review_file, index=False, encoding="utf-8-sig")

print("\nTransformation completed.")
print(f"Source workbooks: {len(workbooks)}")
print(f"Output observations: {len(result):,}")
print(f"Long-format dataset: {output_file}")
print(f"Worksheet review: {review_file}")
print("\nFortnight assignment:")
print(result["fortnight"].value_counts(dropna=False))
