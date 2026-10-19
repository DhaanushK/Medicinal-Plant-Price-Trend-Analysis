USE medicinal_plant_price_trend_analysis;
SELECT
    market,
    source_year,
    COUNT(*) AS positive_price_observations,
    COUNT(DISTINCT reporting_month) AS months_covered,
    ROUND(AVG(analytical_price), 2) AS average_price
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
WHERE p.botanical_name_part = 'Azadirachta indica-Leaf'
  AND po.analytical_price > 0
GROUP BY market, source_year
ORDER BY market, source_year;


SELECT
    po.source_year,
    po.reporting_month,
    po.reporting_month_name,
    po.source_suffix,
    po.fortnight,
    po.market,
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
  AND po.source_year = 2023
  AND po.analytical_price > 0
ORDER BY po.reporting_month, po.source_suffix;

SELECT
    p.botanical_name_part,
    p.trade_name_part,
    COUNT(*) AS positive_price_observations,
    COUNT(DISTINCT po.market) AS markets_covered,
    COUNT(DISTINCT po.source_year) AS years_covered,
    ROUND(AVG(po.analytical_price), 2) AS average_price,
    ROUND(MIN(po.analytical_price), 2) AS minimum_price,
    ROUND(MAX(po.analytical_price), 2) AS maximum_price
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
WHERE po.analytical_price > 0
GROUP BY
    p.botanical_name_part,
    p.trade_name_part
ORDER BY
    markets_covered DESC,
    positive_price_observations DESC
LIMIT 15;

SELECT
    p.botanical_name_part,
    p.trade_name_part,
    po.market,
    po.source_year,
    po.reporting_month_name,
    po.source_suffix,
    po.original_price_value,
    po.analytical_price,
    po.data_quality_status,
    po.analytical_price_status,
    po.source_workbook,
    po.source_sheet
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
WHERE po.analytical_price > 0
ORDER BY po.analytical_price DESC
LIMIT 20;

SELECT
    p.botanical_name_part,
    p.trade_name_part,
    COUNT(*) AS positive_observations,
    ROUND(AVG(po.analytical_price), 2) AS mean_price,
    ROUND(
        AVG(
            CASE
                WHEN po.analytical_price <= 10000
                THEN po.analytical_price
            END
        ),
        2
    ) AS mean_price_up_to_10000,
    ROUND(MIN(po.analytical_price), 2) AS minimum_price,
    ROUND(MAX(po.analytical_price), 2) AS maximum_price
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
WHERE po.analytical_price > 0
GROUP BY
    p.botanical_name_part,
    p.trade_name_part
HAVING MAX(po.analytical_price) > 10000
ORDER BY maximum_price DESC;


SELECT
    p.botanical_name_part,
    p.trade_name_part,
    COUNT(*) AS observations_above_10000,
    COUNT(DISTINCT po.market) AS markets_affected,
    COUNT(DISTINCT po.source_year) AS years_affected,
    ROUND(MIN(po.analytical_price), 2) AS lowest_flagged_price,
    ROUND(MAX(po.analytical_price), 2) AS highest_flagged_price
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
WHERE po.analytical_price > 10000
GROUP BY
    p.botanical_name_part,
    p.trade_name_part
ORDER BY
    observations_above_10000 DESC,
    highest_flagged_price DESC;

SELECT
    p.botanical_name_part,
    p.trade_name_part,
    po.market,
    po.source_year,
    po.reporting_month_name,
    po.source_suffix,
    po.original_price_value,
    po.analytical_price,
    po.data_quality_status,
    po.analytical_price_status,
    po.source_workbook,
    po.source_sheet
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
WHERE po.analytical_price > 10000
  AND p.botanical_name_part IN (
      'Gmelina arborea-Bark',
      'Embelia ribes-Seed',
      'Carthamus tinctorius-Flower',
      'Asparagus racemosus(MP)-Root',
      'Rubia cordifolia(Assam)-Root',
      'Azadirachta indica-Leaf'
  )
ORDER BY
    p.botanical_name_part,
    po.analytical_price DESC;


SELECT
    data_quality_status,
    analytical_price_status,
    COUNT(*) AS observation_count,
    SUM(
        CASE
            WHEN analytical_price > 0 THEN 1
            ELSE 0
        END
    ) AS positive_price_count,
    SUM(
        CASE
            WHEN analytical_price IS NULL THEN 1
            ELSE 0
        END
    ) AS missing_analytical_price_count
FROM price_observations
GROUP BY
    data_quality_status,
    analytical_price_status
ORDER BY observation_count DESC;