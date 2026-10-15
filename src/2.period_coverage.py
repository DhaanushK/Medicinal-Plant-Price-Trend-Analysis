
from pathlib import Path
import calendar
import re
import pandas as pd

# Locate the project folders.
PROJECT_DIR = Path(__file__).resolve().parent.parent
AUDIT_FILE = PROJECT_DIR / "reports" / "worksheet_audit.csv"
OUTPUT_FILE = PROJECT_DIR / "reports" / "period_coverage.csv"

# Restrict the analysis to our planned study period.
START_YEAR = 2017
END_YEAR = 2025

MONTHS = {name: number for number, name in enumerate(
    calendar.month_abbr
) if name}

# Read the worksheet inventory created in Step 1.
audit = pd.read_csv(AUDIT_FILE)

records = []

for _, row in audit.iterrows():
    # Extract month, year, and suffix from worksheet names.
    match = re.match(
        r"^([A-Za-z]{3})\s+(\d{4})\s*-\s*([12])$",
        str(row["sheet_name"]).strip()
    )

    if not match:
        continue

    month_name, year_text, suffix_text = match.groups()
    year = int(year_text)

    if not START_YEAR <= year <= END_YEAR:
        continue

    month = MONTHS.get(month_name.title())

    if month is None:
        continue

    records.append({
        "file": row["file"],
        "sheet_name": row["sheet_name"],
        "year": year,
        "month": month,
        "month_name": calendar.month_abbr[month],
        "suffix": int(suffix_text),
        "row_count": row["row_count"],
        "column_count": row["column_count"],
        "non_empty_cells": row["non_empty_cells"],
    })

periods = pd.DataFrame(records)

if periods.empty:
    raise ValueError(
        "No reporting periods matched the expected worksheet names."
    )

# Summarize the suffixes present for each month and year.
summary = []

for (year, month), group in periods.groupby(["year", "month"]):
    suffixes = sorted(group["suffix"].unique())
    suffix_set = set(suffixes)

    # Apply the user's fortnight-label convention.
    if suffix_set == {1, 2}:
        fortnight_map = {"1": "Second fortnight", "2": "First fortnight"}
        interpretation = "Both fortnights available"
    elif suffix_set == {1}:
        fortnight_map = {"1": "First fortnight"}
        interpretation = "Only first fortnight label present"
    else:
        fortnight_map = {}
        interpretation = "Suffix -2 only; interpretation needs review"

    for _, row in group.iterrows():
        suffix = str(row["suffix"])

        summary.append({
            **row.to_dict(),
            "fortnight": fortnight_map.get(
                suffix, "Unresolved"
            ),
            "period_coverage": interpretation,
            "empty_or_suspicious": (
                row["row_count"] == 0
                or row["column_count"] < 3
                or row["non_empty_cells"] == 0
            ),
        })

# Include months with no worksheet at all.
available_months = set(
    zip(periods["year"], periods["month"])
)

for year in range(START_YEAR, END_YEAR + 1):
    for month in range(1, 13):
        if (year, month) not in available_months:
            summary.append({
                "file": f"{year}.xlsx",
                "sheet_name": None,
                "year": year,
                "month": month,
                "month_name": calendar.month_abbr[month],
                "suffix": None,
                "row_count": None,
                "column_count": None,
                "non_empty_cells": None,
                "fortnight": "No worksheet available",
                "period_coverage": "Month missing from supplied files",
                "empty_or_suspicious": True,
            })

# Save a report for review.
coverage = pd.DataFrame(summary).sort_values(
    ["year", "month", "suffix"],
    na_position="first"
)

coverage.to_csv(OUTPUT_FILE, index=False)

print("Period coverage audit completed.")
print(f"Report saved to: {OUTPUT_FILE}")
print("\nCoverage status by year:")

for year, group in coverage.groupby("year"):
    months_present = group.loc[
        group["sheet_name"].notna(), "month"
    ].nunique()

    print(f"{year}: {months_present}/12 months represented")

print("\nReview the CSV for missing months and unusual worksheets.")
