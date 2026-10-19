# Medicinal Plant Market Intelligence: Data Quality Report

## 1. Project Overview

This report documents data-quality checks performed on historical medicinal plant market price observations sourced from the Ministry of AYUSH's e-CHARAK portal for 2017 to 2025.

The purpose is to document missing values, ambiguous price notations, unusual price observations, and limitations that may affect market comparisons and trend analysis.

## 2. Dataset Summary

| Metric | Result |
|---|---:|
| Total observations | 374,830 |
| Distinct plant IDs | 110 |
| Distinct markets | 31 |
| Years covered | 9 |
| Records with positive prices | 71,890 |
| Records with missing analytical prices | 302,772 |
| Records with zero prices | 168 |
| Records with negative prices | 0 |
| Markets with positive prices | 29 |

Two markets, Gaurela-Pendra-Marwahi and Khariar Road, contain records but no positive analytical prices. They remain in the dataset.

## 3. Data-Quality Categories

| Category | Record count | Treatment |
|---|---:|---|
| Blank source cells | 291,503 | Retained as missing |
| Numeric prices parsed, pending validation | 71,890 | Retained for analysis with validation caveat |
| Ambiguous comma-zero notation | 6,830 | Analytical price left missing pending review |
| Undefined placeholders | 4,400 | Retained as missing |
| Presumed-missing zeroes from December 2025, suffix 1 | 168 | Excluded from positive-price summaries |
| Unrecognized notation | 15 | Retained for review |
| Asterisk placeholders | 12 | Retained as missing |
| Flagged zero values | 8 | Retained for review |
| Price ranges with preserved endpoints | 4 | Retained for review |

The category counts sum to 374,830 observations. The 302,772 records with missing analytical prices are distinct from the 168 zero-price records.

## 4. Annual Price Coverage

Coverage is calculated as the percentage of records with a positive analytical price within each year.

| Year | Total records | Positive prices | Missing prices | Zero prices | Positive-price coverage |
|---|---:|---:|---:|---:|---:|
| 2017 | 22,000 | 8,306 | 13,694 | 0 | 37.75% |
| 2018 | 52,250 | 31,031 | 21,219 | 0 | 59.39% |
| 2019 | 60,720 | 10,363 | 50,357 | 0 | 17.07% |
| 2020 | 45,540 | 4,806 | 40,734 | 0 | 10.55% |
| 2021 | 54,780 | 5,346 | 49,434 | 0 | 9.76% |
| 2022 | 66,990 | 5,928 | 61,062 | 0 | 8.85% |
| 2023 | 57,970 | 5,234 | 52,736 | 0 | 9.03% |
| 2024 | 13,640 | 321 | 13,319 | 0 | 2.35% |
| 2025 | 940 | 555 | 217 | 168 | 59.04% |

### Interpretation

- 2018 has the highest positive-price coverage among 2017–2024.
- Coverage is substantially lower from 2019 onward, particularly in 2022–2024.
- 2024 has only 321 positive-price records out of 13,640.
- 2025 contains only 940 records, including 168 presumed-missing zeroes. Its coverage percentage should not be interpreted as evidence of complete annual reporting.
- Differences in data availability may affect annual averages, trend comparisons, and market rankings.

## 5. Unusual Price Observations

A screening query identified 1,527 records with analytical prices above 10,000, involving 13 plants, 21 markets, and 8 years.

These observations were treated as candidates for review, not automatically classified as errors. The source does not consistently provide a confirmed price unit, and large values may not be corrected without additional evidence.

Examples investigated include high values for Kashmiri Kesar, Irani Kesar, Chandan (White), Gambhari-Bark, Vai-Vidang-Seed, and other plants.

## 6. Gambhari-Bark: November 2022 Finding

The original source workbook was checked for the six high Gambhari-Bark observations in `2022.xlsx`, sheet `Nov 2022 - 1`.

| Market | First-fortnight value | Second-fortnight value |
|---|---:|---:|
| Delhi | 250,004 | 98 |
| Saharanpur | 244,379 | 96 |
| Amritsar | 243,754 | 91 |
| Kanpur | 242,504 | 91 |
| Tanakpur | 241,254 | 91 |
| Haldwani | 238,754 | 94 |

The first-fortnight values matched the displayed source workbook values. The second-fortnight values were much lower in all six markets.

The cause of the discrepancy and the applicable price unit remain unconfirmed. The values have not been changed.

**Treatment:** Preserve the original source values and flag the observations for further source-level validation. Do not apply automatic corrections.

## 7. Other Findings Requiring Caution

- A Neem-Leaf observation for Kolkata in June 2023 contains a value of 40,240. The original workbook display was checked and showed `40,240`, but the unit and reason for the extreme value remain unconfirmed.
- Ambiguous `0,0` notations and other unrecognized formats were not converted into numeric prices without evidence.
- Some plant-market-year combinations have very few observations or cover only a small number of months.
- Plant and market averages can be distorted by extreme observations and uneven coverage.
- The source price unit has not been confirmed for all records.

## 8. Analytical Rules

1. Use `analytical_price > 0` for positive-price summaries.
2. Do not treat the 168 presumed-missing zeroes as genuine prices.
3. Keep missing and ambiguous prices as missing rather than guessing their intended values.
4. Preserve original source values for traceability.
5. Flag extreme values for review instead of automatically deleting or correcting them.
6. Report observation counts alongside averages and medians.
7. Interpret annual and market comparisons cautiously when price coverage is low or uneven.
8. Clearly state that source units and some reporting anomalies remain unresolved.

## 9. Conclusion

The database contains 374,830 observations across 110 plant identifiers, 31 markets, and 9 years. It has 71,890 positive analytical prices, while 302,772 observations have missing analytical prices and 168 have zero values treated as presumed missing.

The data is suitable for exploratory analysis with explicit quality controls. However, substantial missingness, uneven annual coverage, unconfirmed units, and unresolved extreme values limit the reliability of unqualified price comparisons.

All source values should remain unchanged unless a correction can be supported by verifiable evidence.
