# Data-Cleaning Policy
## Medicinal Plant Market Intelligence

### 1. Purpose

This document defines the rules for validating, standardizing, and preparing medicinal plant market-price data collected from the e-CHARAK Price Wise portal.

**Source:** https://echarak.ayush.gov.in/Pricewise  
**Study period:** 2017–2025

The original Excel workbooks must remain unchanged. All cleaning and transformation operations will be performed on separate processed datasets.

### 2. Source Coverage

Some months and fortnights are absent from the downloaded source data. These gaps reflect the reporting periods available in the collected government-published files.

- Do not create artificial price observations for missing periods.
- Distinguish unavailable reporting periods from blank price cells.
- Record the actual coverage of each year, month, and fortnight.
- Disclose coverage limitations in the project report and dashboard.

### 3. Original Data Preservation

For every observation, preserve the original reporting period, medicinal plant identifier, market name, and source price value wherever available.

Every transformation must be reproducible and documented.

### 4. Special-Value Handling

| Source value | Initial handling rule | Status |
|---|---|---|
| `***` | Treat as missing for numerical analysis while preserving the original value. | Assumption pending verification |
| `undefined` | Treat as unavailable in the analytical price field; preserve the source value. | Unavailable/unresolved |
| `0*` | Do not convert automatically to numeric zero. Flag for review. | Meaning unverified |
| `0,0` | Preserve the original notation and investigate before numeric conversion. | Meaning unverified |
| Price range, e.g. `300-1080` | Preserve the original range and handle separately from single numeric prices. | Requires a defined analytical method |
| Blank cell | Treat as a missing observation, not as zero. | Missing value |

These rules describe our analytical treatment, not confirmed definitions provided by e-CHARAK.

### 5. Fortnight Standardization

Apply the project's documented reporting-period convention:

- If a month-year appears once with suffix `-1`, interpret it as the first fortnight.
- If both `-1` and `-2` are present for the same month-year, interpret `-1` as the second fortnight and `-2` as the first fortnight.
- Preserve the original worksheet name alongside the standardized period.

Do not infer a missing fortnight or invent a reporting date.

### 6. Structural Standardization

The source workbooks contain medicinal plants as rows and market names as columns.

The processed analytical dataset will use a normalized structure with one row per medicinal plant, market, and reporting period.

Proposed fields:

- `source_year`
- `source_sheet`
- `reporting_month`
- `fortnight`
- `botanical_name_part`
- `trade_name_part`
- `market`
- `original_price_value`
- `analytical_price`
- `data_quality_status`

### 7. Numeric Validation

- Convert a source value to a number only when its numeric meaning and formatting are sufficiently clear.
- Do not automatically classify every zero as invalid.
- Do not assume that commas always indicate decimal separators.
- Do not silently convert price ranges to averages or single values.
- Record values that require manual review.

### 8. Validation and Quality Assurance

Before the processed dataset is approved:

- Verify worksheet and reporting-period coverage.
- Check duplicate plant-market-period observations.
- Validate market and medicinal plant identifiers.
- Compare source and processed observation counts.
- Review missing-value and special-value frequencies.
- Confirm that no original source workbook was modified.

### 9. Limitations

The source does not provide an explanation for every special notation encountered in the downloaded worksheets. Interpretations that cannot be verified will be documented as assumptions.

The resulting analysis will describe reported prices and observed differences. It will not claim that a market offers the lowest total purchasing cost without evidence about comparable units and other relevant costs.

### 10. Versioning

**Policy version:** 1.0  
**Study period:** 2017–2025  
**Status:** Initial policy, pending implementation and validation