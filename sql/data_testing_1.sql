USE medicinal_plant_price_trend_analysis;

WITH yearly_prices AS (
    SELECT
        source_year,
        analytical_price
    FROM price_observations
    WHERE analytical_price > 0
)
SELECT
    source_year,
    COUNT(*) AS positive_price_observations,
    ROUND(AVG(analytical_price), 2) AS average_price,
    ROUND(MIN(analytical_price), 2) AS minimum_price,
    ROUND(MAX(analytical_price), 2) AS maximum_price
FROM yearly_prices
GROUP BY source_year
ORDER BY source_year;

SELECT
    source_year,
    COUNT(*) AS total_observations,
    SUM(analytical_price > 0) AS positive_prices,
    SUM(analytical_price = 0) AS zero_prices,
    SUM(analytical_price IS NULL) AS missing_prices,
    ROUND(
        100.0 * SUM(analytical_price > 0) / COUNT(*),
        2
    ) AS positive_price_coverage_pct
FROM price_observations
GROUP BY source_year
ORDER BY source_year;

SELECT
    source_year,
    analytical_price_status,
    COUNT(*) AS record_count
FROM price_observations
GROUP BY
    source_year,
    analytical_price_status
ORDER BY
    source_year,
    record_count DESC;

SELECT
    source_year,
    original_price_value,
    data_quality_status,
    COUNT(*) AS record_count
FROM price_observations
WHERE analytical_price_status = 'Review required'
GROUP BY
    source_year,
    original_price_value,
    data_quality_status
ORDER BY
    source_year,
    record_count DESC
LIMIT 50;

SELECT
    po.source_year,
    po.reporting_month,
    po.source_suffix,
    p.botanical_name_part,
    p.trade_name_part,
    po.market,
    po.original_price_value,
    po.analytical_price,
    po.data_quality_status,
    po.source_workbook,
    po.source_sheet
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
WHERE po.data_quality_status LIKE 'Review required%'
ORDER BY
    po.source_year,
    po.reporting_month,
    p.botanical_name_part
LIMIT 30;

SELECT
    source_year,
    data_quality_status,
    COUNT(*) AS record_count
FROM price_observations
WHERE data_quality_status LIKE 'Review required%'
GROUP BY
    source_year,
    data_quality_status
ORDER BY
    source_year,
    record_count DESC;

SELECT
    market,
    COUNT(*) AS positive_price_observations,
    COUNT(DISTINCT plant_id) AS distinct_plants,
    ROUND(AVG(analytical_price), 2) AS average_price,
    ROUND(MIN(analytical_price), 2) AS minimum_price,
    ROUND(MAX(analytical_price), 2) AS maximum_price
FROM price_observations
WHERE analytical_price > 0
GROUP BY market
ORDER BY average_price DESC;

SELECT
    p.botanical_name_part,
    p.trade_name_part,
    COUNT(DISTINCT po.market) AS markets_covered,
    COUNT(*) AS positive_price_observations,
    ROUND(AVG(po.analytical_price), 2) AS average_price
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
WHERE po.analytical_price > 0
GROUP BY
    p.plant_id,
    p.botanical_name_part,
    p.trade_name_part
ORDER BY
    markets_covered DESC,
    positive_price_observations DESC
LIMIT 15;

SELECT
    po.market,
    COUNT(*) AS positive_price_observations,
    COUNT(DISTINCT po.source_year) AS years_covered,
    ROUND(AVG(po.analytical_price), 2) AS average_price,
    ROUND(MIN(po.analytical_price), 2) AS minimum_price,
    ROUND(MAX(po.analytical_price), 2) AS maximum_price
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
WHERE p.botanical_name_part = 'Azadirachta indica-Leaf'
  AND po.analytical_price > 0
GROUP BY po.market
ORDER BY average_price DESC;

SELECT
    po.source_year,
    po.reporting_month,
    po.source_suffix,
    po.market,
    p.botanical_name_part,
    p.trade_name_part,
    po.original_price_value,
    po.analytical_price,
    po.data_quality_status,
    po.analytical_price_status,
    po.source_workbook,
    po.source_sheet
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
WHERE p.botanical_name_part = 'Azadirachta indica-Leaf'
  AND po.market = 'Kolkata'
  AND po.analytical_price = 40240;