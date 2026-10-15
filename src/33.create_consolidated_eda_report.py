
from pathlib import Path
from datetime import date

# Resolve paths relative to the project root.
ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "reports"
OUTPUT_FILE = REPORT_DIR / "EDA_consolidated_report.md"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# The report records completed analysis and its known limitations.
report = r"""# Medicinal Plant Market Intelligence
## Exploratory Data Analysis (EDA) Report

**Project domain:** Business Analytics and Market Intelligence  
**Primary data source:** e-CHARAK Price Wise  
**Study period:** 2017–2025  
**Tools:** Python, pandas, Excel; SQL and Power BI are planned for later stages.

---

## 1. Executive Summary

This project examines historical medicinal plant market-price observations to
understand data availability, differences between markets, price distributions,
and unusual price movements. The intended business use is to help medicinal
herb businesses investigate historical price variation and identify potential
sourcing opportunities.

The standardized long dataset contains 374,830 observations from nine annual
workbooks covering 2017–2025. It represents 110 plant identifiers and 31
markets.

After conservative price parsing and quality review, 71,890 observations
were classified as positive numeric prices for descriptive analysis.
A further 302,772 observations were unparsed or unavailable, while 168 zero
values from the December 2025 - 1 worksheet were flagged as presumed missing
based on the observed source pattern.

The EDA identified incomplete price coverage, a highly right-skewed price
distribution, plant-market pairs with insufficient numeric observations, and
unusual historical price movements. A focused investigation of three plants
identified 18 plant-market pairs with exceptional November 2022 values.
Those values were verified against the corresponding original Excel workbook
and preserved without automatic correction.

**Interpretation:** The dataset supports exploratory descriptions of observed
prices, subject to coverage and data-quality limitations. It does not, by
itself, establish the best place to purchase a plant or prove that a price
movement reflects a genuine market event.

---

## 2. Business Problem and Objectives

### Business problem

Medicinal herb businesses need a structured way to review historical market
prices, compare the availability of price observations across plants and
markets, and identify records that require further investigation before
purchasing decisions are made.

### EDA objectives

1. Assess the completeness and consistency of the collected data.
2. Understand the coverage of plants, markets, and plant-market pairs.
3. Describe the distribution of usable numeric prices.
4. Identify unusual price observations and sudden changes.
5. Preserve traceability to the original source data.
6. Establish limitations and rules for responsible downstream analysis.

### Intended business questions

- Which plants and markets have enough recorded prices for descriptive
  comparisons?
- How variable are recorded prices for a plant within a market?
- Which observations show unusual changes relative to nearby periods?
- Which findings require source verification before they can inform sourcing?

These are analytical questions. The EDA does not yet demonstrate savings,
profitability, supply reliability, or causal explanations for price changes.

---

## 3. Data Source and Scope

The primary source is the e-CHARAK Price Wise portal:

https://echarak.ayush.gov.in/Pricewise

The local study covers annual Excel workbooks from 2017 through 2025.
The 2026 workbook is outside the defined study period.

The original workbook structure is wide: plant identifiers are recorded in
the first two columns, while market names appear in subsequent columns.
The project transformed the worksheets into a long-format dataset so that
each row represents a plant-market observation from a source worksheet.

### Important source limitations

- The official meaning of all special source notations has not been verified.
- The exact price unit and price definition have not been confirmed.
- Blank cells must not be interpreted as zero.
- The availability of observations differs considerably by year, market,
  plant, and reporting period.
- A recorded price should not automatically be assumed to represent a
  directly comparable product, quality, quantity, or transaction.

---

## 4. Data Preparation and Validation

### Processing workflow

The project used separate scripts to audit the workbooks, assess period
coverage, inspect special price notations, standardize reporting periods,
validate the long dataset, classify and clean price values, and construct
the analytical dataset.

The principal processed files are:

- `data/processed/medicinal_plant_prices_raw_long.csv`
- `data/processed/medicinal_plant_prices_cleaned.csv`
- `data/processed/medicinal_plant_prices_analytical.csv`

The raw long dataset preserves source values and worksheet identifiers.
The analytical dataset adds parsed price fields and quality-status labels.

### Dataset validation results

| Validation item | Result |
|---|---:|
| Observations in the analytical dataset | 374,830 |
| Columns in the analytical dataset | 17 |
| Study years | 2017–2025 |
| Plant identifiers | 110 |
| Markets | 31 |
| Duplicate plant-market-worksheet keys | 0 |
| Flagged December 2025 presumed-missing zeros | 168 |

The analytical dataset validation script reported that required columns were
present and that the flagged December zeros belonged to the expected
worksheet and retained their original value.

### Reporting-period standardization

The source worksheet label is retained alongside standardized period fields.
Fortnight assignment follows the project's documented suffix rules.
Worksheets with unresolved suffix interpretation should not be assigned a
fortnight by guessing.

The standardized long dataset contains:

| Fortnight classification | Observations |
|---|---:|
| First fortnight | 217,010 |
| Second fortnight | 157,820 |
| Total | 374,830 |

---

## 5. Data Quality and Price Classification

The original long dataset contains the following price-value classifications:

| Source-value classification | Observations |
|---|---:|
| Blank | 291,503 |
| Numeric-formatted | 72,058 |
| `0,0` | 6,830 |
| `undefined` | 4,400 |
| Other comma-formatted values | 15 |
| `***` | 12 |
| `0*` | 8 |
| Price ranges | 4 |
| **Total** | **374,830** |

These categories describe the observed representations; they do not establish
the official meaning of every notation.

### Cleaning decisions

- Blank values remain missing.
- `undefined` and `***` are not treated as numeric prices.
- `0*` and `0,0` are retained for review rather than automatically converted.
- Price ranges retain their endpoints; no midpoint is invented.
- No missing price is imputed.
- Original workbooks remain unchanged.

Of the 72,058 numeric-parsed observations, 71,890 were positive and 168
were zero. No negative numeric prices were found.

The 168 zero values occur in `Dec 2025 - 1`. Based on the observed pattern
of missing values in that worksheet, they were flagged as presumed missing.
This is a project-level assumption for analytical caution, not an official
source definition.

The analytical dataset classifies 71,890 records as positive numeric prices
and 6,857 as requiring review, alongside the missing and placeholder
categories. These status categories should be consulted before using
observations in a specific analysis.

---

## 6. Price Completeness and Temporal Coverage

### Positive numeric-price coverage by year

| Year | Total observations | Positive numeric prices | Positive share |
|---|---:|---:|---:|
| 2017 | 22,000 | 8,306 | 37.75% |
| 2018 | 52,250 | 31,031 | 59.39% |
| 2019 | 60,720 | 10,363 | 17.07% |
| 2020 | 45,540 | 4,806 | 10.55% |
| 2021 | 54,780 | 5,346 | 9.76% |
| 2022 | 66,990 | 5,928 | 8.85% |
| 2023 | 57,970 | 5,234 | 9.03% |
| 2024 | 13,640 | 321 | 2.35% |
| 2025 | 940 | 555 | 59.04% |

### Interpretation

Coverage varies significantly over the study period. The relatively high
positive share in 2025 must not be interpreted as improved overall coverage:
the year contains only 940 observations and four markets in this dataset.

Similarly, the low positive share in 2024 limits the strength of annual
comparisons. Changes in observed prices may be affected by which markets and
periods have usable values, not only by market conditions.

A dashboard should therefore display observation counts or coverage
alongside price statistics, and should avoid presenting years as equally
representative when their data availability differs.

---

## 7. Plant and Market Coverage

### Coverage overview

- Plant identifiers: 110
- Markets: 31
- Possible plant-market pairs: 3,410

The pair count represents the combinations of plant identifiers and markets
in the dataset, not the number of pairs with sufficient observations for
every analysis.

### Plant-market pair availability

| Positive-price availability threshold | Pairs meeting threshold |
|---|---:|
| At least 1 observation | 2,445 (71.70%) |
| At least 5 observations | 2,058 (60.35%) |
| At least 10 observations | 1,962 (57.54%) |
| At least 20 observations | 1,684 (49.38%) |

A provisional minimum of ten positive numeric observations per plant-market
pair was adopted for descriptive pair-level comparisons. This is a practical
screening threshold, not proof of statistical representativeness.

The ten-observation threshold alone does not guarantee adequate temporal
coverage. Observations may be clustered in a small portion of the study
period. Trend comparisons should also examine the number and distribution
of observed reporting periods.

### Illustrative market coverage

Kolkata had 9,306 positive prices out of 14,940 observations (62.29%).
Berhampur had 6,175 positive prices out of 14,840 (41.61%).
Mumbai had 5,221 positive prices out of 14,630 (35.69%).

These counts describe data availability in the collected dataset. They do
not establish that any market is cheaper, better supplied, or more suitable
for sourcing.

---

## 8. Overall Price Distribution

The distribution was calculated from 71,890 positive numeric-price
observations.

| Statistic | Value |
|---|---:|
| Minimum | 4 |
| First quartile (Q1) | 60 |
| Median | 140 |
| Third quartile (Q3) | 370 |
| 90th percentile | 860 |
| 95th percentile | 1,790 |
| 99th percentile | 130,000 |
| Mean | 3,059.42 |
| Standard deviation | 21,418.15 |
| Maximum | 315,000 |

**Units are unverified.** These figures are reported in the numeric scale
found in the source data; they must not be labelled INR/kg or another unit
without source confirmation.

The mean is much higher than the median, and the upper tail extends to very
large values. This indicates a strongly right-skewed distribution.

For descriptive analysis, the median and quartiles are useful complements
to the mean. However, even medians are meaningful only when the underlying
prices refer to sufficiently comparable observations.

---

## 9. Outlier Investigation

### Initial high-price screening

The 99th percentile of the positive numeric-price distribution was 130,000. There were 682 observations above this threshold.

These records were flagged for investigation, not automatically classified as errors. A high value can reflect a legitimate difference, a source notation issue, a data-entry problem, or another factor that the available data cannot resolve.

### Plant-market IQR screening

For plant-market pairs with at least ten positive numeric observations, the upper screening limit was calculated as:

`Q3 + 1.5 × IQR`

where `IQR = Q3 - Q1`.

The investigation flagged 2,402 observations across 806 distinct plant-market groups, approximately 3.34% of the 71,890 positive numeric observations.

An IQR flag indicates that an observation is unusual relative to its group's distribution. It does not prove that the value is incorrect. Flagged observations were retained.

### Distribution of flagged observations

The corrected year-level summary reports both the number of flagged observations and the number of distinct plant-market pairs affected within each year.

The market-level summary likewise distinguishes flagged observations from distinct plant-market pairs. For example, Kolkata had 263 flagged observations across 44 distinct plant-market pairs. Chennai had 214 flagged observations across 52 pairs.

These counts describe the distribution of detected flags. They should not be interpreted as outlier rates or as evidence that a market has poorer data quality without considering the number of usable observations in that market.

### Interpretation limitations

- The number of flagged records depends on the selected threshold.
- Raw counts by year or market are not comparable without considering the number of usable observations in each group.
- The same plant-market pair may have multiple flagged observations across reporting periods.
- An unusual value may represent a real event, a reporting anomaly, or an unresolved source issue.
- Outlier treatment must not be based on a desire to make charts appear smoother.

## 10. Historical Price Changes

Historical comparisons were calculated for candidate plant-market pairs
using available numeric observations. Monthly comparisons were made only
where the relevant calendar months were available; missing months were not
bridged as if continuous observations existed.

The price-change analysis reported:

| Measure | Result |
|---|---:|
| Candidate plant-market pairs | 1,949 |
| Monthly records analysed | 40,634 |
| Available month-over-month comparisons | 32,044 |
| Available year-over-year comparisons | 11,417 |

The largest apparent changes include substantial increases and decreases.
Some movements are driven by values that are dramatically different from
neighboring periods.

For example, the November 2022 investigation found extreme changes for
Black bitumen (Shilajit), Embelia ribes (Vai-Vidang), and Gmelina arborea
(Gambhari). These cases are discussed separately in the next section.

### Interpretation rules

- Percentage changes can be misleading when the comparison baseline is
  very small.
- A missing month is not a zero-price month.
- A change between two recorded values does not establish why the price
  changed.
- Large changes require source and context checks before they are presented
  as market movements.
- The reporting period and observation count should accompany any trend.

---

## 11. November 2022 Source-Level Anomaly Investigation

### Investigation method

Three plants were examined across October, November, and December 2022.
Their raw long-format values were compared with the analytical dataset and
then checked against the original `2022.xlsx` worksheets.

The comparison selected 465 records. All 465 matched an analytical record.
After accounting for blank-versus-`N/A` representations, the verification
reported 108 exact value matches and 357 equivalent missing representations.

Twelve exceptionally large values were checked against the original
workbook and matched their source cells exactly.

### Findings

#### Black bitumen — Stone / Shilajit — Stone

Across six markets, the values in `Nov 2022 - 1` were approximately 56–59.
Neighboring observed values were approximately 1,346–1,489. The November
values were around 96% lower than the neighboring-period reference values.

#### Embelia ribes — Seed / Vai-Vidang — Seed

Across six markets, `Nov 2022 - 1` values were approximately 95,504–100,004.
Neighboring values were approximately 1,550–1,713. November values were
roughly 59–61 times the neighboring-period reference values.

#### Gmelina arborea — Bark / Gambhari — Bark

Across six markets, `Nov 2022 - 1` values were approximately 238,754–250,004.
Neighboring values were approximately 91–117. November values were roughly
2,326–2,474 times the neighboring-period reference values.

### Anomaly register

The report `eda_step09_anomaly_register.csv` contains 18 flagged
plant-market pairs:

- 12 unusually high November values.
- 6 unusually low November values.

### Conclusion and treatment

The unusual values are present in the original workbook and were preserved
through extraction and analytical processing. Therefore, the investigation
found no evidence that these values were created by the cleaning process.

However, matching the original workbook does not establish whether the
published values are valid market prices. They remain source-level anomalies
requiring further clarification.

Recommended treatment:

1. Preserve the original values.
2. Retain the anomaly register for traceability.
3. Exclude these flagged observations from baseline trend comparisons
   provisionally, pending verification.
4. Do not substitute neighboring values or delete records automatically.
5. If additional evidence becomes available, reassess the records and
   document any revised treatment.

---

## 12. Key Business Implications

### Data coverage must accompany price comparisons

A market with more observed prices may appear more informative simply
because it has better coverage. Dashboards should show observation counts,
usable-price coverage, and the time span alongside price statistics.

### Compare like with like

Plant identity, plant part, market, and reporting period must be considered
before comparing prices. The source's price definition and units should be
confirmed before interpreting numeric differences as directly comparable
commercial prices.

### Separate screening flags from confirmed errors

IQR outliers and sudden movements are investigation signals. They should be
distinguished from confirmed source errors and preserved for review.

### Do not equate the lowest recorded price with the best sourcing option

A sourcing decision may depend on product quality, grade, availability,
quantity, transport, handling, and other costs. These variables have not
been established by the price dataset alone.

The current EDA identifies places and records worth investigating; it does
not establish a definitive sourcing recommendation.

---

## 13. Limitations and Assumptions

1. The study uses the collected e-CHARAK Price Wise workbooks; completeness
   of the portal's entire historical record has not been independently
   established.
2. The official meaning of special notations such as `***`, `0*`, `0,0`,
   and `undefined` remains unverified.
3. The exact unit and definition of the reported prices remain unverified.
4. Missing values are not assumed to be zero.
5. The 168 zeros in `Dec 2025 - 1` are treated as presumed missing for
   analysis based on the observed worksheet pattern, not an official rule.
6. Price ranges are preserved rather than converted to midpoints.
7. The IQR and percentage-change thresholds are screening choices, not
   authoritative definitions of errors.
8. The ten-positive-observation pair threshold is provisional and does not
   guarantee temporal representativeness.
9. The November 2022 anomalies match the source workbook but have not been
   independently confirmed as invalid published prices.
10. Historical price differences do not establish causation or future
    price direction.
11. The analysis does not yet incorporate quality grades, transport costs,
    transaction quantities, supply reliability, or confirmed demand data.

---

## 14. Recommended Next Steps

1. Retain the source workbooks, raw long dataset, cleaned dataset, analytical
   dataset, and anomaly reports as separate traceable artifacts.
2. Review the official price definitions and special notations if source
   documentation or clarification becomes available.
3. Build a reproducible analytical dataset that preserves source values,
   quality flags, and period identifiers.
4. Design SQL tables and validation checks for plants, markets, reporting
   periods, and price observations.
5. Develop Power BI visuals for data coverage, median-price comparisons,
   price distributions, trends, and flagged observations.
6. Show observation counts and coverage limitations alongside dashboard
   comparisons.
7. Avoid definitive sourcing recommendations until comparability, price
   units, and relevant purchasing costs are understood.

---

## 15. Supporting Reports

The following supporting outputs were generated during the EDA workflow:

- `workbook_audit.csv`
- `worksheet_audit.csv`
- `period_coverage.csv`
- `price_quality_audit.csv`
- `price_exceptions.csv`
- `data/processed/unprocessed_worksheets.csv`
- `medicinal_plant_prices_raw_long.csv`
- `medicinal_plant_prices_cleaned.csv`
- `medicinal_plant_prices_analytical.csv`
- `analytical_dataset_validation.txt`
- `eda_step01_readiness_by_status.csv`
- `eda_step01_readiness_by_year.csv`
- `eda_step02_plant_coverage.csv`
- `eda_step02_market_coverage.csv`
- `eda_step03_plant_market_pairs.csv`
- `eda_step04_pair_thresholds.csv`
- `eda_step05_price_distributions.csv`
- `eda_step06_iqr_outliers.csv`
- `eda_step07_outlier_patterns_by_pair.csv`
- `eda_step09_price_changes.csv`
- `eda_step09_sudden_movements.csv`
- `eda_step09_source_spike_investigation.csv`
- `eda_step09_raw_vs_analytical_spike_check.csv`
- `eda_step09_original_excel_spike_verification.csv`
- `eda_step09_november_spike_comparison.csv`
- `eda_step09_anomaly_register.csv`

Supporting files are located in the project's `reports` directory unless
otherwise specified. Filenames listed here should be checked against the
actual project directory before final submission.

---

## 16. Final EDA Conclusion

The project has established a reproducible long-format analytical dataset
and documented its principal data-quality, coverage, distribution, and
historical-change characteristics.

The EDA shows that missing data and inconsistent coverage are substantial
constraints, that the numeric price distribution has a pronounced upper
tail, and that unusual observations can materially affect historical
comparisons.

The focused November 2022 investigation verified that a group of extreme
values is present in the original Excel workbook. These observations have
been preserved and documented rather than automatically corrected.

The dataset is ready for carefully qualified descriptive analysis and
dashboard development. Claims about definitive market competitiveness,
sourcing profitability, or causal market changes require further evidence.

---

**Report generation date:** __REPORT_DATE__
"""

# Add the actual generation date without changing analytical results.
report = report.replace("__REPORT_DATE__", date.today().isoformat())

OUTPUT_FILE.write_text(report, encoding="utf-8")

print("Consolidated EDA report created successfully.")
print(f"Output: {OUTPUT_FILE}")
print(f"Report size: {OUTPUT_FILE.stat().st_size:,} bytes")
print("\nNext: open the Markdown file and review its contents.")
