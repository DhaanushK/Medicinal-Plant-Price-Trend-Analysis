\# Power BI Dashboard Documentation



\## Project Title

\*\*Medicinal Plant Market Price and Trend Analysis\*\*



\## 1. Objective

Develop an interactive Power BI dashboard to explore medicinal plant market prices, compare reported prices across markets, and analyze price trends over time using data sourced from the e-CHARAK Price Wise dataset published by the Ministry of AYUSH.



\## 2. Data Source

\- \*\*Source:\*\* e-CHARAK Price Wise

\- \*\*Coverage:\*\* 2017 to 2025

\- \*\*Analytical dataset:\*\* `medicinal\_plant\_prices\_analytical.csv`

\- \*\*Database:\*\* MySQL

\- \*\*Visualization tool:\*\* Microsoft Power BI Desktop



The dataset contains 374,830 observations across 110 medicinal plants and 31 markets. The analysis uses positive-price observations where appropriate.



\## 3. Dashboard Pages



\### Page 1: Overview

Provides a high-level summary of the available price data.



\*\*Key performance indicators\*\*

\- Positive Price Observations: 71,890

\- Average Reported Price: 3,059.42

\- Median Reported Price: 140.00



\*\*Visualizations\*\*

\- Average reported price by year

\- Average reported price by market

\- Positive observation count by year



\*\*Interactive filters\*\*

\- Plant selector

\- Market selector



\### Page 2: Plant Price Trend Analysis

Focuses on the historical price pattern and observation coverage for the selected medicinal plant.



\*\*Visualizations\*\*

\- Median reported price by year

\- Observation count by year

\- Data quality note highlighting interpretation limitations



\*\*Interactive filters\*\*

\- Plant selector

\- Market selector



\## 4. Data Model

The Power BI report uses the MySQL tables and view:

\- `plants`

\- `price\_observations`

\- `positive\_price\_observations`



The `plants` table is related to the observation tables through `plant\_id`. These relationships allow the plant selection to filter the relevant observations.



The positive-price view excludes zero and non-positive prices from analyses that require valid positive values.



\## 5. Data Quality and Interpretation

\- The source data contains many missing analytical prices.

\- Zero-price records are treated as presumed missing values where identified during data preparation.

\- Data availability varies across years, especially in 2024 and 2025.

\- Average prices can be strongly affected by extreme observations.

\- Median prices are included to provide a more robust view of typical reported prices.

\- Price units and currency context have not been independently verified. Values should not be interpreted as a confirmed currency amount.

\- Comparisons across years and markets should account for differences in observation counts and data coverage.



\## 6. Analytical Example

Neem-Leaf is used as a focused example for exploring market differences and historical price trends. A reported Kolkata observation of 40,240 in June 2023 was retained because it was present in the source workbook. Its unit and context have not been verified, so it should be investigated before drawing conclusions from it.



\## 7. Repository Screenshots

\- `powerbi/dashboard\_overview.jpg`

\- `powerbi/plant\_price\_trend\_analysis.jpg`



\## 8. How to Use the Dashboard

1\. Open `powerbi/Medicinal\_Plant\_Trend\_Analysis.pbix` in Power BI Desktop.

2\. Select a medicinal plant using the plant selector.

3\. Optionally select a market to narrow the analysis.

4\. Review the KPI cards and charts on the Overview page.

5\. Navigate to Plant Price Trend Analysis to inspect the historical median price and observation coverage.

6\. Interpret results alongside the data quality limitations documented above.



\## 9. Limitations

The dashboard describes patterns in the available reported data. Uneven data coverage, missing prices, unverified units, and extreme observations limit direct comparisons. The results should not be treated as verified market quotations or as a forecast of future prices.



