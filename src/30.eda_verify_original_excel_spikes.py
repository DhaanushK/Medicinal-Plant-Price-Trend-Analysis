
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

RAW_FILE = (
    ROOT / "data" / "processed"
    / "medicinal_plant_prices_raw_long.csv"
)
WORKBOOK_DIR = ROOT / "data" / "raw" / "price_wise"
OUTPUT_FILE = (
    ROOT / "reports"
    / "eda_step09_original_excel_spike_verification.csv"
)

raw = pd.read_csv(RAW_FILE, dtype=str, keep_default_na=False)

# Select the three plants investigated in the previous step.
plant_terms = ["Black bitumen", "Embelia ribes", "Gmelina arborea"]

plant_mask = pd.Series(False, index=raw.index)

for term in plant_terms:
    plant_mask |= (
        raw["botanical_name_part"].str.contains(
            term, case=False, regex=False
        )
        | raw["trade_name_part"].str.contains(
            term, case=False, regex=False
        )
    )

period_mask = (
    raw["source_year"].eq("2022")
    & raw["source_sheet"].str.match(
        r"^(Oct|Nov|Dec) 2022", case=False
    )
)

selected = raw.loc[plant_mask & period_mask].copy()

# For this comparison only, blank and N/A are equivalent
# missing representations. The source data is not modified.
def is_missing_representation(value):
    return str(value).strip().upper() in {"", "N/A"}


results = []
sheet_cache = {}

for _, record in selected.iterrows():
    workbook_name = Path(record["source_workbook"]).name
    workbook_path = WORKBOOK_DIR / workbook_name
    sheet_name = record["source_sheet"]

    result = {
        "source_workbook": workbook_name,
        "source_sheet": sheet_name,
        "botanical_name_part": record["botanical_name_part"],
        "trade_name_part": record["trade_name_part"],
        "market": record["market"],
        "raw_csv_value": record["original_price_value"].strip(),
        "excel_value": "",
        "verification_status": "",
    }

    if not workbook_path.exists():
        result["verification_status"] = "Workbook not found"
        results.append(result)
        continue

    cache_key = (str(workbook_path), sheet_name)

    try:
        if cache_key not in sheet_cache:
            sheet_cache[cache_key] = pd.read_excel(
                workbook_path,
                sheet_name=sheet_name,
                dtype=str,
                keep_default_na=False,
            )

        sheet = sheet_cache[cache_key]

        if len(sheet.columns) < 3:
            result["verification_status"] = "Unexpected worksheet layout"
            results.append(result)
            continue

        botanical_col = sheet.columns[0]
        trade_col = sheet.columns[1]

        botanical_match = (
            sheet[botanical_col].astype(str).str.strip()
            == record["botanical_name_part"].strip()
        )
        trade_match = (
            sheet[trade_col].astype(str).str.strip()
            == record["trade_name_part"].strip()
        )

        row_matches = sheet.loc[botanical_match & trade_match]

        market_columns = [
            col for col in sheet.columns
            if str(col).strip() == record["market"].strip()
        ]

        if len(row_matches) == 0:
            result["verification_status"] = "Plant row not matched"

        elif len(row_matches) > 1:
            result["verification_status"] = "Multiple plant rows matched"

        elif len(market_columns) == 0:
            result["verification_status"] = "Market column not matched"

        elif len(market_columns) > 1:
            result["verification_status"] = "Multiple market columns matched"

        else:
            excel_value = str(
                row_matches.iloc[0][market_columns[0]]
            ).strip()

            raw_value = record["original_price_value"].strip()
            result["excel_value"] = excel_value

            if raw_value == excel_value:
                result["verification_status"] = "Exact value match"

            elif (
                is_missing_representation(raw_value)
                and is_missing_representation(excel_value)
            ):
                result["verification_status"] = (
                    "Equivalent missing representation"
                )

            else:
                result["verification_status"] = (
                    "Value differs; investigate"
                )

    except Exception as exc:
        result["verification_status"] = (
            f"Read error: {type(exc).__name__}: {exc}"
        )

    results.append(result)

report = pd.DataFrame(results)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
report.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print(f"Selected records: {len(report):,}")
print("\nVerification status counts:")
print(report["verification_status"].value_counts().to_string())

# Highlight non-missing numeric values of 10,000 or more,
# plus any values that still differ or could not be matched.
numeric_values = pd.to_numeric(report["raw_csv_value"], errors="coerce")

review_mask = (
    report["verification_status"].ne("Exact value match")
    & report["verification_status"].ne(
        "Equivalent missing representation"
    )
) | (numeric_values >= 10000)

review = report.loc[review_mask].copy()

print(f"\nRecords requiring review: {len(review):,}")
print(review.to_string(index=False, max_rows=60))

print(f"\nFull report saved to: {OUTPUT_FILE}")
