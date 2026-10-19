# Neem-Leaf Market Price Analysis

## 1. Objective

Analyze recorded Neem-Leaf market prices across Berhampur, Kolkata, and Silliguri using monthly median prices from the medicinal plant market dataset.

## 2. Data and Methodology

- Source: Ministry of AYUSH e-CHARAK price data, 2017 to 2025.
- Database: MySQL, with Python and Pandas used for data preparation and Matplotlib used for visualization.
- Analysis metric: Median of positive recorded prices for each market and reporting month.
- Observation counts are retained to indicate how much data supports each monthly median.
- Zero prices and missing or ambiguous values are not treated as valid positive prices in this analysis.

## 3. Key Findings

### Berhampur
Recorded monthly medians were generally around 18 to 27 during the observed months in 2018. In 2019, monthly medians rose to approximately 115 to 120 from May through December. Subsequent recorded medians were generally lower, around 70 to 105 in 2020 and around 70 to 85 in 2021 and 2022.

### Kolkata
Recorded monthly medians generally increased from approximately 17 to 25 in 2017 and 2018 to around 40 to 50 during much of 2019 to 2022. A June 2023 record of 40,240 was confirmed in the source workbook but remains flagged because its unit and context have not been established. It is excluded from the focused trend line only, not modified in the underlying data.

### Silliguri
Recorded monthly medians were generally around 22 to 25 during 2018, rose during 2019 and were frequently around 70 to 80 during 2021 to 2023. The 2025 values are based on very few observations and should be interpreted cautiously.

## 4. Data Quality and Limitations

- The source does not establish the price unit in the reviewed records.
- Reporting coverage varies by market, year and month.
- Some monthly medians are based on only one or two observations.
- Missing months are not interpolated.
- The June 2023 Kolkata value of 40,240 is preserved and flagged for further validation.
- These findings describe recorded observations and do not establish the causes of price changes or represent a complete market-wide price index.

## 5. Conclusion

The analysis identifies distinct recorded price patterns across the three selected markets. Median prices help reduce the influence of extreme observations, while observation counts and data-quality flags provide essential context. Further interpretation requires more consistent reporting coverage and confirmation of source price units.
