# Medicinal Plant Market Intelligence
## Project Progress Documentation — Up to Pre-EDA Stage

**Project Title:** Medicinal Plant Market Intelligence: Market Price Analysis and Sourcing Insights

**Domain:** Data Analytics, Business Intelligence and Market Research

**Primary Data Source:** e-CHARAK Price Wise — Ministry of AYUSH, Government of India

**Study Period:** 2017–2025

**Current Stage:** Data Preparation, Cleaning, Quality Assessment and Validation Completed; Exploratory Data Analysis (EDA) Pending

**Tools:** Python, Pandas, Excel, MySQL and Power BI

---

# 1. Project Overview

The project aims to analyze historical medicinal plant market-price information to help medicinal-herb businesses understand price variations, assess market-level differences, identify potential sourcing opportunities and make better-informed purchasing decisions.

The project follows a business analytics approach rather than a machine learning or deep learning approach. The objective is to convert raw market-price information into reliable, interpretable business insights using data preparation, descriptive analysis, SQL queries, spreadsheet analysis and interactive dashboards.

The project will use the following workflow:

1. Data collection and source assessment.
2. Workbook auditing and reporting-period identification.
3. Data restructuring and standardization.
4. Price-value classification and cleaning.
5. Data-quality investigation and validation.
6. Exploratory Data Analysis (EDA).
7. MySQL database design and analytical queries.
8. Excel-based analysis and validation.
9. Power BI dashboard development.
10. Final interpretation, documentation and recommendations.

**Current progress:** Steps 1–5 have been completed for the working dataset. EDA and subsequent analytical implementation stages remain pending.

# 2. Problem Statement

Medicinal-herb businesses may encounter differences in reported prices across markets, medicinal plants, plant parts and reporting periods. Without systematically organized historical data, it can be difficult to examine these differences and identify potentially relevant sourcing opportunities.

The project addresses the following business question:

**How can medicinal-herb businesses use historical market prices, market information and product characteristics to identify price variations, evaluate potential sourcing opportunities and make better-informed purchasing decisions?**

The project will investigate this question using the available e-CHARAK market-price records.

The analysis will remain limited to what the dataset supports. It will not assume that a lower reported price automatically represents a better purchase, because price units, product comparability, transport costs, quality and other purchasing considerations have not yet been established by the source data.

# 3. Dataset Source and Scope

## 3.1 Primary data source

Official portal: https://echarak.ayush.gov.in/Pricewise

The downloaded Excel workbooks contain medicinal plant information and reported market prices.

The dataset includes the following types of information:

- Botanical name and plant part.
- Trade name and plant part.
- Market names.
- Reported price values.
- Source workbook and worksheet information.
- Reporting month and inferred fortnight.

## 3.2 Study period

The selected study period is **2017–2025**.

A 2026 workbook was present in the original downloaded archive, but it was excluded from the current analysis scope.

The source data does not contain a complete record for every month or fortnight in the study period. These gaps are limitations of the available published source data and must not be treated as records accidentally deleted during cleaning.

## 3.3 Dataset suitability

The e-CHARAK dataset is conditionally suitable for descriptive market-price analysis because it contains medicinal plant identities, plant parts, market names and reported prices.

Its suitability for individual analyses will depend on data availability, price interpretation and comparability. In particular, the dataset does not automatically support conclusions about actual purchasing costs, demand, sales, profit, supplier reliability or guaranteed savings.

# 4. Project Environment and Folder Structure

The project is maintained locally at:

`D:\Masters in AI\Medicinal Plant BI`

The principal folders are:

```text
Medicinal Plant BI/
│
├── .venv/
├── .env
├── .gitignore
├── requirements.txt
│
├── data/
│   ├── raw/
│   │   └── price_wise/
│   │       ├── 2017.xlsx
│   │       ├── 2018.xlsx
│   │       ├── 2019.xlsx
│   │       ├── 2020.xlsx
│   │       ├── 2021.xlsx
│   │       ├── 2022.xlsx
│   │       ├── 2023.xlsx
│   │       ├── 2024.xlsx
│   │       └── 2025.xlsx
│   │
│   └── processed/
│       ├── medicinal_plant_prices_raw_long.csv
│       ├── medicinal_plant_prices_cleaned.csv
│       └── medicinal_plant_prices_analytical.csv
│
├── reports/
│   ├── workbook_audit.csv
│   ├── worksheet_audit.csv
│   ├── period_coverage.csv
│   ├── price_quality_audit.csv
│   ├── price_exceptions.csv
│   ├── price_completeness_by_year.csv
│   ├── price_completeness_by_market.csv
│   ├── price_value_classification.csv
│   ├── price_value_classification_by_year.csv
│   ├── price_value_classification_by_market.csv
│   ├── cleaning_summary.csv
│   ├── numeric_price_summary_by_year.csv
│   ├── numeric_price_summary_by_market.csv
│   ├── zero_negative_price_review.csv
│   ├── zero_price_investigation.csv
│   ├── high_price_investigation.csv
│   ├── analytical_dataset_validation.txt
│   └── ...
│
└── src/
    ├── 01_data_audit.py
    ├── 02_period_coverage.py
    ├── 03_price_quality_check.py
    ├── 04_inspect_price_exceptions.py
    ├── 05_standardize_periods.py
    ├── 06_validate_long_dataset.py
    ├── 07_price_completeness.py
    ├── 08_classify_price_values.py
    ├── 09_clean_price_values.py
    ├── 10.validate_numeric_prices.py
    ├── 11.investigate_suspicious_prices.py
    ├── 12.create_analytical_dataset.py
    └── 13.validate_analytical_dataset.py
```

The listing represents the principal project structure and outputs created during this stage. Some intermediate reports, including `duplicate_key_review.csv` and `unprocessed_worksheets.csv`, are also generated by the scripts.

**Important:** the scripts currently use a mixture of underscores and dots in their filenames. The commands documented in this project must match the actual filenames saved in the `src` directory.

The Python virtual environment and dependencies have been configured. The `.env` file is used for environment-specific configuration and must not be committed to version control.

# 5. Phase 1 — Workbook Audit

**Script:** `src/01_data_audit.py`

## Objective

To inspect the downloaded Excel workbooks before attempting to combine their contents.

## Work performed

The script reads the annual Excel workbooks individually and records workbook and worksheet metadata. This provides an initial understanding of the files and their structure.

The audit produced:

- `reports/workbook_audit.csv`
- `reports/worksheet_audit.csv`

The original source workbooks were retained in the raw-data directory.

The working study period includes nine annual workbooks, from 2017 through 2025. The 2026 workbook was excluded from the subsequent study-period processing.

## Outcome

The source files could be inspected programmatically, allowing later scripts to work directly with the individual annual workbooks instead of depending on an outdated copy of the original ZIP archive.

# 6. Phase 2 — Reporting-Period Coverage Assessment

**Script:** `src/02_period_coverage.py`

**Output:** `reports/period_coverage.csv`

## Objective

To identify the reporting months available in the downloaded dataset and make source-coverage limitations explicit.

## Coverage identified

| Year | Months represented | Months absent |
|---|---|---|
| 2017 | January–April, November–December | May–October |
| 2018 | January–August, October | September, November, December |
| 2019 | January–August, October–December | September |
| 2020 | January–March, June–August, October–December | April, May, September |
| 2021 | January–August, October–December | September |
| 2022 | January–August, October–December | September |
| 2023 | January–August, October–November | September, December |
| 2024 | January–March | April–December |
| 2025 | March, December | January, February, April–November |

These entries describe the observed worksheet-based coverage in the working source files, not a claim that every day or fortnight within each represented month is available.

The March 2023 worksheet that was initially empty was manually corrected by the user. The corrected 2023 workbook replaced the earlier local version and was included in subsequent processing.

## Outcome

The coverage assessment established that the dataset is incomplete across multiple years. The missing months and reporting periods must be disclosed in later analysis.

A year with few available reporting periods cannot be compared directly with a year having much broader coverage without considering that difference.

# 7. Phase 3 — Price-Value Quality Assessment

**Scripts:**

- `src/03_price_quality_check.py`
- `src/04_inspect_price_exceptions.py`

**Outputs:**

- `reports/price_quality_audit.csv`
- `reports/price_exceptions.csv`

## Objective

To investigate how price values are represented in the source workbooks before converting them into numerical values.

## Issues identified

The source data contains several types of values:

- Blank cells.
- Numeric-looking values.
- `N/A`-style unavailable entries, where present.
- `undefined`.
- `***`.
- `0*`.
- `0,0`.
- Price ranges such as `300-1080`.
- Zero values.

The portal did not provide an authoritative legend explaining all of these special representations during the user's source inspection.

Consequently, the project does not assign unsupported meanings to these values.

## Established cleaning principles

| Source representation | Treatment adopted |
|---|---|
| Blank cell | Treat as missing, not zero |
| `undefined` | Treat as unavailable in the analytical copy |
| `***` | Treat as missing in the analytical copy; meaning unverified |
| `0*` | Preserve and flag for review |
| `0,0` | Preserve and flag for review |
| Price range | Preserve both endpoints; do not automatically replace with a midpoint |
| Numeric-looking value | Parse provisionally and retain the original value |
| Zero | Investigate its meaning before using it as a genuine price |

The original source values remain available for traceability.

# 8. Phase 4 — Long-Format Data Restructuring

**Script:** `src/05_standardize_periods.py`

**Outputs:**

- `data/processed/medicinal_plant_prices_raw_long.csv`
- `data/processed/unprocessed_worksheets.csv`

## 8.1 Why restructuring was required

The source workbooks use a wide format:

- The first column contains `Botanical name - Part`.
- The second column contains `Trade name - Part`.
- Remaining columns contain market names.
- Cells contain the reported prices.

This arrangement is convenient for viewing individual worksheets but is less suitable for systematic market-level analysis, SQL querying and dashboard development.

The data was reshaped into a long format, where each row represents a plant-market-reporting-period observation.

## 8.2 Output schema

The resulting raw long-format dataset contains 12 columns:

1. `source_year`
2. `reporting_month`
3. `reporting_month_name`
4. `source_suffix`
5. `fortnight`
6. `period_status`
7. `source_workbook`
8. `source_sheet`
9. `botanical_name_part`
10. `trade_name_part`
11. `market`
12. `original_price_value`

The `original_price_value` field preserves the source representation rather than forcing all entries into numeric form.

## 8.3 Fortnight-standardization rule

The source worksheet labels contain suffixes such as `MMM YYYY - 1` and `MMM YYYY - 2`.

The following rule was implemented:

- When both suffixes are present for a month and year, suffix `-1` is assigned to the second fortnight and suffix `-2` to the first fortnight.
- When only suffix `-1` is present, it is assigned to the first fortnight.
- When only suffix `-2` is present, the fortnight is left unresolved rather than guessed.
- The original worksheet label and suffix are retained for traceability.

These are project-specific interpretation rules based on the observed source convention. They are not claimed to be an officially documented portal definition.

## 8.4 Restructuring results

The script processed nine annual workbooks and generated:

| Metric | Result |
|---|---:|
| Total observations | 374,830 |
| First-fortnight assignments | 217,010 |
| Second-fortnight assignments | 157,820 |
| Worksheets read in the later processing run | 136 |
| Worksheets listed as unprocessed in the review output | 0 |

The zero unprocessed-worksheet count means the script did not flag any worksheets in that output. It does not prove that every original source value is valid or that every reporting period is present.

# 9. Phase 5 — Structural Validation of the Long Dataset

**Script:** `src/06_validate_long_dataset.py`

**Output:** `reports/duplicate_key_review.csv`

## Objective

To verify that restructuring preserved the expected number of observations and generated the intended schema.

## Validation results

| Check | Result |
|---|---|
| Total observations | 374,830 |
| Number of columns | 12 |
| Study years represented | 2017–2025 |
| Blank source-year identifiers | 0 |
| Blank source-sheet identifiers | 0 |
| Blank botanical-name-and-part identifiers | 0 |
| Blank trade-name-and-part identifiers | 0 |
| Blank market identifiers | 0 |
| Duplicate plant-market-sheet keys | 0 |

The original price field contained 291,503 blank values. These were preserved as missing observations rather than replaced with zero.

Special representations identified included:

| Representation | Count |
|---|---:|
| `***` | 12 |
| `undefined` | 4,400 |
| `0*` | 8 |
| `0,0` | 6,830 |

## Outcome

The long-format dataset passed the implemented structural checks. The project proceeded to more detailed price-value classification.

# 10. Phase 6 — Price Completeness Assessment

**Script:** `src/07_price_completeness.py`

**Outputs:**

- `reports/price_completeness_by_year.csv`
- `reports/price_completeness_by_market.csv`

## Objective

To quantify how much of the long-format dataset contains nonblank price values.

## Initial findings by year

| Year | Nonblank values | Reported completeness |
|---|---:|---:|
| 2017 | 8,310 | 37.77% |
| 2018 | 31,046 | 59.42% |
| 2019 | 13,012 | 21.43% |
| 2020 | 6,786 | 14.90% |
| 2021 | 7,548 | 13.78% |
| 2022 | 8,028 | 11.98% |
| 2023 | 7,113 | 12.27% |
| 2024 | 761 | 5.58% |
| 2025 | 723 | 76.91% |

These percentages measure nonblank cells in the observed dataset. They do not measure completeness relative to every possible market, plant, day or reporting period.

The 2025 figure is especially important to interpret carefully: that year contains only 940 observations across three reporting worksheets and four markets. Its high nonblank percentage does not mean that it provides broad coverage comparable with earlier years.

The market-level report also revealed uneven data availability. For example, Kolkata had 62.41% nonblank values, while Khariar Road had 0% in the recorded observations examined by that report.

## Limitation identified

A nonblank value is not necessarily a usable price. For example, `undefined` is nonblank text but does not represent a usable numeric price.

This led to a separate classification step.

# 11. Phase 7 — Classification of Price Values

**Script:** `src/08_classify_price_values.py`

**Outputs:**

- `reports/price_value_classification.csv`
- `reports/price_value_classification_by_year.csv`
- `reports/price_value_classification_by_market.csv`

## Objective

To classify the original price representations before cleaning them for analysis.

## Overall classification

| Classification | Count | Percentage |
|---|---:|---:|
| Blank | 291,503 | 77.77% |
| Numeric-formatted value | 72,058 | 19.22% |
| `0,0` | 6,830 | 1.82% |
| `undefined` | 4,400 | 1.17% |
| Other comma-formatted values | 15 | Approximately 0.004% |
| `***` | 12 | Approximately 0.003% |
| `0*` | 8 | Approximately 0.002% |
| Price ranges | 4 | Approximately 0.001% |
| **Total** | **374,830** | **100% approximately** |

Percentages are rounded.

## Notable observations

- All 4,400 `undefined` entries were associated with Gaurela-Pendra-Marwahi in the source data examined.
- Most `0,0` entries were associated with Himachal.
- The `***`, `0*` and range values were relatively few but still required explicit handling.

The classification report provided a measurable basis for the next cleaning stage.

# 12. Phase 8 — Creation of the Cleaned Dataset

**Script:** `src/09_clean_price_values.py`

**Outputs:**

- `data/processed/medicinal_plant_prices_cleaned.csv`
- `reports/cleaning_summary.csv`

## Objective

To create an analytical copy of the long-format dataset while preserving source values and documenting how each value was handled.

## Cleaning logic

The script retained the original price value and introduced analytical fields for numeric interpretation and quality status.

The implemented treatment was:

- Blank values were classified as missing.
- `undefined` and `***` were classified as missing placeholders.
- `0*` and `0,0` were flagged for review.
- Recognized numeric values were parsed provisionally.
- Price ranges were represented using lower and upper endpoints.
- Unrecognized representations were flagged for review.
- Negative values, if encountered, were not automatically accepted as valid prices.

The cleaned dataset contains 16 columns.

## Cleaning results

| Quality status | Count |
|---|---:|
| Missing: blank source cell | 291,503 |
| Numeric-formatted: parsed; validation pending | 72,058 |
| Review required: ambiguous comma-zero | 6,830 |
| Missing: undefined placeholder | 4,400 |
| Review required: unrecognized notation | 15 |
| Missing: asterisk placeholder | 12 |
| Review required: flagged zero | 8 |
| Price range: endpoints preserved | 4 |
| **Total** | **374,830** |

## Outcome

The cleaned dataset retained all 374,830 observations. No source rows were deleted, and special values were not silently converted into ordinary prices.

The cleaning summary reconciled with the total observation count.

# 13. Phase 9 — Numeric Price Validation

**Script:** `src/10.validate_numeric_prices.py`

**Outputs:**

- `reports/numeric_price_summary_by_year.csv`
- `reports/numeric_price_summary_by_market.csv`
- `reports/zero_negative_price_review.csv`

## Objective

To examine the distribution of parsed numeric prices and identify zero or negative values that require further investigation.

## Validation results

| Metric | Result |
|---|---:|
| Total observations | 374,830 |
| Parsed numeric prices | 72,058 |
| Unparsed or unavailable prices | 302,772 |
| Zero prices | 168 |
| Negative prices | 0 |

The numeric-price distribution was:

| Statistic | Value |
|---|---:|
| Mean | 3,052.29 |
| Standard deviation | 21,393.67 |
| Minimum | 0 |
| 25th percentile | 60 |
| Median | 140 |
| 75th percentile | 370 |
| 90th percentile | 860 |
| 95th percentile | 1,775.75 |
| 99th percentile | 130,000 |
| Maximum | 315,000 |

These statistics describe the values parsed as numeric. The price units and the exact meaning of the reported price were not independently verified at this stage. Therefore, the values should not yet be assigned an assumed unit or used for definitive cross-market price comparisons.

The difference between the mean and median indicates that the distribution is strongly right-skewed, with some very large values influencing the mean.

No prices were removed or changed during this validation step.

# 14. Phase 10 — Investigation of Suspicious Prices

**Script:** `src/11.investigate_suspicious_prices.py`

**Outputs:**

- `reports/zero_price_investigation.csv`
- `reports/high_price_investigation.csv`

## 14.1 High-price investigation

The 99th percentile, 130,000, was used as a screening threshold. Numeric values strictly above that threshold were selected for review.

A total of **682 high-price records** were flagged.

| Botanical name – Part | Flagged records |
|---|---:|
| Crocus sativus (Kashmiri) – Stigma | 379 |
| Crocus sativus (Irani) – Stigma | 297 |
| Gmelina arborea – Bark | 6 |
| **Total** | **682** |

These values were flagged because they are unusually high relative to the observed distribution. They were not automatically classified as errors or removed.

The concentration among two Crocus sativus product entries suggests that product-specific characteristics or source conventions may contribute to the high values. This remains an observation to investigate, not a verified explanation.

## 14.2 Zero-price investigation

The investigation identified 168 zero-price records. All were associated with the `Dec 2025 - 1` worksheet.

| Market | Zero-price records |
|---|---:|
| Silliguri | 76 |
| Deogarh | 53 |
| Berhampur | 24 |
| Kolkata | 15 |
| **Total** | **168** |

The user inspected the original December 2025 worksheet and observed that zeros appear to be used for terms whose prices are missing or unfilled, whereas other worksheets use `N/A`.

Based on this observation, the project adopted a provisional interpretation:

**The 168 zeros in `Dec 2025 - 1` are presumed missing prices rather than confirmed market prices.**

This is a source-based inference, not an officially confirmed portal definition.

The original zero values remain preserved. They are not replaced with blanks or deleted from the dataset.

# 15. Phase 11 — Creation of the Analytical Dataset

**Script:** `src/12.create_analytical_dataset.py`

**Input:**

`data/processed/medicinal_plant_prices_cleaned.csv`

**Output:**

`data/processed/medicinal_plant_prices_analytical.csv`

## Objective

To create a separate analytical working dataset that explicitly identifies the 168 suspected missing-price records.

## Transformation performed

The script added a new field:

`analytical_price_status`

The status field classifies records for analytical use. It distinguishes positive numeric prices awaiting validation, missing values, records requiring review and the presumed-missing December zeros.

The 168 zero-price records were identified using the condition that:

- The source worksheet is `Dec 2025 - 1`.
- The parsed analytical price equals zero.

Their new status is:

`Presumed missing: zero in Dec 2025 - 1`

The script does not overwrite the cleaned dataset. It creates a separate CSV file.

## Output results

| Metric | Result |
|---|---:|
| Total observations | 374,830 |
| Output columns | 17 |
| Presumed-missing zero records flagged | 168 |
| Original zero values preserved | 168 |

The analytical status summary was:

| Analytical status | Count |
|---|---:|
| Missing: blank source cell | 291,503 |
| Numeric price: validation pending | 71,890 |
| Review required | 6,857 |
| Missing: undefined placeholder | 4,400 |
| Presumed missing: zero in Dec 2025 - 1 | 168 |
| Missing: asterisk placeholder | 12 |
| **Total** | **374,830** |

The 71,890 positive numeric-price records result from separating the 168 flagged zeros from the original 72,058 parsed numeric prices.

The dataset still contains the original values and all 374,830 observations.

# 16. Phase 12 — Final Structural Validation

**Script:** `src/13.validate_analytical_dataset.py`

**Input:**

`data/processed/medicinal_plant_prices_analytical.csv`

**Output:**

`reports/analytical_dataset_validation.txt`

## Validation checks performed

The script verified the required fields, identified the records carrying the presumed-missing status, checked their source worksheet and original value, and counted duplicate plant-market-sheet keys.

## Results

| Validation check | Result |
|---|---|
| Total observations | 374,830 |
| Total columns | 17 |
| Missing required columns | None |
| Presumed-missing records | 168 |
| All flagged records belong to `Dec 2025 - 1` | True |
| All flagged original values equal zero | True |
| Duplicate plant-market-sheet keys | 0 |
| Overall validation status | **PASSED** |

The report was saved at:

`reports/analytical_dataset_validation.txt`

## Meaning of the validation result

The analytical dataset passed all checks implemented in the validation script.

This establishes that the file meets the structural and specific record-level conditions tested by the script. It does not establish that all prices are accurate, that all source reporting periods are present, or that prices are comparable across markets.

# 17. Data Governance and Quality Decisions

The following rules govern the current analytical dataset.

## 17.1 Source preservation

The original annual Excel workbooks are retained in the raw-data directory. Cleaning and classification are performed in separate processed files.

## 17.2 No fabricated observations

Missing months, fortnights and prices are not filled with invented values.

## 17.3 No automatic deletion of outliers

The 682 high-price records remain in the dataset. The 130,000 threshold is used only to flag records for review.

## 17.4 No unsupported interpretation of special values

The meanings of `***`, `0*`, `0,0` and `undefined` have not been confirmed by an official source legend. The project records these as cleaning assumptions or unresolved cases.

## 17.5 Provisional treatment of December zeros

The 168 zeros in `Dec 2025 - 1` are flagged as presumed missing based on inspection of the source worksheet. Their original values remain preserved.

## 17.6 Comparability limitations

The price unit, price definition and any relevant product-grade or transaction conventions have not yet been verified. Consequently, the project must not assume that all reported values are directly comparable.

## 17.7 Coverage limitations

The published data contains incomplete reporting periods. Trends and comparisons must be interpreted in the context of actual data availability.

# 18. Current Dataset Versions

Three main CSV datasets have been created.

| Dataset | Rows | Columns | Purpose |
|---|---:|---:|---|
| `medicinal_plant_prices_raw_long.csv` | 374,830 | 12 | Long-format source values with standardized period metadata |
| `medicinal_plant_prices_cleaned.csv` | 374,830 | 16 | Cleaned analytical copy with price-value classifications |
| `medicinal_plant_prices_analytical.csv` | 374,830 | 17 | Current analytical working dataset with explicit analytical statuses |

**Current working dataset:** `data/processed/medicinal_plant_prices_analytical.csv`

The raw long-format dataset and cleaned dataset should also be retained for traceability. The analytical dataset is not a replacement for the original workbooks.

# 19. Project Status Before EDA

## Completed

- Primary source selection and study-period definition.
- Raw workbook organization.
- Workbook and worksheet auditing.
- Reporting-period coverage assessment.
- Long-format restructuring.
- Fortnight-standardization rules.
- Structural validation of the long-format dataset.
- Price completeness assessment.
- Price-value classification.
- Cleaning policy implementation.
- Numeric price-distribution validation.
- Investigation of zero and high-price records.
- Creation of the analytical working dataset.
- Final structural validation of the analytical dataset.

## Pending

- Exploratory Data Analysis (EDA).
- Detailed analysis of price availability by plant, market, year and fortnight.
- Investigation of high-price records and product-specific distributions.
- Verification of source price units and definitions, where documentation is available.
- MySQL database design and data import.
- SQL-based analytical queries.
- Excel analysis and validation.
- Power BI dashboard design and development.
- Final business recommendations and project report.

# 20. Next Planned Stage — Exploratory Data Analysis

EDA will begin with the validated analytical working dataset.

The first objective will be to understand the distribution and availability of usable prices before making business comparisons.

The planned questions include:

1. Which medicinal plants have the most available numeric price observations?
2. Which markets have sufficient price coverage for analysis?
3. How does data availability vary by year and fortnight?
4. What are the distributions of reported prices by plant and market?
5. Which products and markets have unusually high reported values?
6. How do incomplete reporting periods affect possible year-to-year comparisons?
7. How should missing, presumed-missing and review-required values be represented in subsequent analysis?

EDA will be descriptive and diagnostic. It will not automatically treat a high price as erroneous, a low price as a better purchase, or a missing price as zero.

The analysis will also distinguish between the number of source records and the number of usable numeric prices.

---

## Final Progress Summary

The project has progressed from raw annual Excel workbooks to a structurally validated, long-format analytical dataset containing **374,830 observations and 17 columns**.

Price representations have been classified, cleaning assumptions have been documented, suspicious values have been flagged, and the 168 zeros in the December 2025 worksheet have been marked as presumed missing without changing their original values.

The analytical dataset has passed the implemented validation checks. However, source-data coverage, price definitions, units and some special-value meanings remain limitations that must be acknowledged in the analysis.

**The project is now ready to begin Exploratory Data Analysis (EDA).**
