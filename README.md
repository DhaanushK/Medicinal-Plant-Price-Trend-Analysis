# Medicinal Plant Market Intelligence

**Market Price Analysis and Sourcing Insights**

A data analytics and business intelligence project exploring historical medicinal plant market-price records to understand price distributions, market-level differences, reporting coverage, and potential sourcing insights.

## Project Overview

Medicinal plant prices may vary across plants, plant parts, markets, and reporting periods. This project organizes historical market-price records and applies data-quality assessment, exploratory data analysis (EDA), SQL, spreadsheet analysis, and business intelligence to investigate those differences.

**Primary business question**

> How can medicinal-herb businesses use historical market prices, market information, and product characteristics to identify price variations, evaluate potential sourcing opportunities, and make better-informed purchasing decisions?

The project focuses on descriptive analytics and business intelligence, not machine learning or deep learning.

## Data Source and Scope

- **Source:** [e-CHARAK Price Wise](https://echarak.ayush.gov.in/Pricewise), Ministry of AYUSH, Government of India
- **Study period:** 2017–2025
- **Primary tools:** Python, Pandas, MySQL, Excel, and Power BI

The project uses annual Excel workbooks and retains source-period metadata and original price representations for traceability.

## Work Completed

- Audited source workbooks and worksheets.
- Assessed reporting-period coverage.
- Restructured the source data into long format.
- Classified price representations and documented cleaning decisions.
- Created cleaned and analytical datasets.
- Investigated zero values and unusually high reported prices.
- Validated dataset structure and selected record-level conditions.
- Conducted exploratory analyses of plant-market coverage, price distributions, outliers, timelines, and price changes.
- Consolidated EDA findings and audited supporting reports.
- Designed a normalized MySQL schema with separate plant and price-observation tables.
- Imported and validated 374,830 observations, including checks for missing prices, duplicate candidate keys, and plant-market coverage.
- Analyzed Neem-Leaf monthly median prices across Berhampur, Kolkata, and Silliguri, with visualizations and documented data-quality caveats.

The analytical dataset contains **374,830 observations and 17 columns**. Structural and data-quality checks were performed, but validation does not establish that every source price is accurate or directly comparable.

## Repository Structure

```text
Medicinal-Plant-Market-Business-Intelligence/
├── notebooks/
│   └── 06_neem_leaf_visualization.py
├── reports/
│   ├── charts/
│   ├── data_cleaning_policy.md
│   ├── data_quality_report.md
│   ├── data_source_notes.md
│   └── neem_leaf_market_analysis.md
├── sql/
│   ├── plants.sql
│   ├── plants_staging.sql
│   ├── price_observations.sql
│   ├── price_observations_staging.sql
│   └── data_testing_*.sql
├── src/
├── requirements.txt
├── .gitignore
└── README.md
```

Raw source workbooks, processed datasets, and most intermediate CSV/TXT outputs are maintained locally and excluded from Git. The structure above highlights the main published project components rather than every local file.

## Environment Setup

### 1. Clone the repository

```bash
git clone https://github.com/DhaanushK/Medicinal-Plant-Market-Business-Intelligence.git
cd Medicinal-Plant-Market-Business-Intelligence
```

### 2. Create and activate a virtual environment

On Windows:

```bat
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bat
python -m pip install -r requirements.txt
```

### 4. Prepare the data

The source Excel workbooks and generated datasets are not included in the repository. Place the required source workbooks in the local data directories expected by the relevant scripts, and inspect each script's input and output paths before running it. Execute scripts in their intended workflow order because later stages may depend on files generated earlier.

## MySQL Setup and Analysis

The project uses a MySQL database named `medicinal_plant_price_trend_analysis`, with separate tables for plant names and price observations. SQL scripts for table creation, staging, and data testing are available in the `sql/` directory.

The staging import script includes an example path placeholder. Before using it, replace the placeholder with the absolute path to your local import CSV and verify that `LOCAL INFILE` is enabled for both the MySQL server and client connection. **Do not rerun a script containing `TRUNCATE TABLE` against a staging table whose contents you need to preserve.**

## Neem-Leaf Visualization

The script `notebooks/06_neem_leaf_visualization.py` generates charts from a CSV exported from MySQL Workbench. To run it:

1. Execute the SQL query used to summarize monthly Neem-Leaf prices for Berhampur, Kolkata, and Silliguri.
2. Export the query result with these columns to `reports/neem_leaf_monthly_market_trends.csv`:
   - `market`
   - `source_year`
   - `reporting_month`
   - `reporting_month_name`
   - `positive_observations`
   - `monthly_median_price`
3. Install the dependencies and run:

   ```bash
   python notebooks/06_neem_leaf_visualization.py
   ```

The script writes the generated charts to `reports/charts/`. The exported CSV is not committed to the repository, so it must be recreated locally before running the visualization script.

## Data Quality and Interpretation

The source data has incomplete reporting periods and multiple price representations. Some special values have no verified official definition in the project documentation.

The project follows these principles:

- Blank source cells are treated as missing, not zero.
- Unverified special representations are preserved or flagged rather than assigned unsupported meanings.
- The 168 zero values in the `Dec 2025 - 1` worksheet are flagged as **presumed missing**, based on source inspection; this is not an officially confirmed definition.
- High-value observations are flagged for investigation rather than automatically deleted.
- Missing reporting periods are not filled with invented observations.
- Reported prices are not assumed to have a verified unit or to be directly comparable across all products and markets.

A lower reported price alone does not prove that a sourcing opportunity is commercially better. Product comparability, quality, transport costs, and other purchasing factors would need separate evidence.

## Planned Work

- Build a Power BI dashboard.
- Translate supported findings into practical business recommendations.

## Reproducibility and Limitations

The repository contains selected analysis scripts, SQL scripts, charts, and documentation. Raw source files, generated datasets, and large intermediate outputs are excluded from the repository to avoid unnecessary size and duplication. Follow the instructions above to recreate the CSV input needed for the Neem-Leaf visualization.

Refer to the included reports for the documented analytical findings, assumptions, and limitations. The project is descriptive analysis of historical reported prices; incomplete coverage, inconsistent reporting, and unverified units limit direct comparisons and any conclusions about sourcing opportunities.
