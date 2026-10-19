USE medicinal_plant_price_trend_analysis;

SELECT
    po.observation_id,
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
ORDER BY po.analytical_price DESC;


SELECT
    COUNT(*) AS total_high_price_records,
    COUNT(DISTINCT plant_id) AS distinct_plants,
    COUNT(DISTINCT market) AS distinct_markets,
    COUNT(DISTINCT source_year) AS distinct_years,
    MIN(analytical_price) AS minimum_price,
    MAX(analytical_price) AS maximum_price
FROM price_observations
WHERE analytical_price > 10000;


SELECT
    p.botanical_name_part,
    p.trade_name_part,
    COUNT(*) AS high_price_records,
    COUNT(DISTINCT po.market) AS markets_covered,
    COUNT(DISTINCT po.source_year) AS years_covered,
    MIN(po.analytical_price) AS minimum_price,
    MAX(po.analytical_price) AS maximum_price
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
WHERE po.analytical_price > 10000
GROUP BY
    p.botanical_name_part,
    p.trade_name_part
ORDER BY
    maximum_price DESC,
    high_price_records DESC;


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
WHERE p.trade_name_part = 'Gambhari-Bark'
  AND po.analytical_price > 10000
ORDER BY
    po.source_year,
    po.reporting_month,
    po.source_suffix,
    po.analytical_price DESC;

SELECT
    p.trade_name_part,
    po.market,
    po.original_price_value,
    po.analytical_price,
    po.source_sheet
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
WHERE po.source_year = 2022
  AND po.reporting_month = 11
  AND po.source_suffix = 1
  AND po.analytical_price > 10000
ORDER BY
    p.trade_name_part,
    po.analytical_price DESC;


SELECT
    g.market,
    g.analytical_price AS gambhari_price,
    v.analytical_price AS vai_vidang_price,
    g.analytical_price - v.analytical_price AS price_difference,
    ROUND(
        g.analytical_price / NULLIF(v.analytical_price, 0),
        3
    ) AS price_ratio
FROM price_observations AS g
JOIN plants AS gp
    ON g.plant_id = gp.plant_id
JOIN price_observations AS v
    ON g.market = v.market
   AND g.source_year = v.source_year
   AND g.reporting_month = v.reporting_month
   AND g.source_suffix = v.source_suffix
JOIN plants AS vp
    ON v.plant_id = vp.plant_id
WHERE gp.trade_name_part = 'Gambhari-Bark'
  AND vp.trade_name_part = 'Vai-Vidang-Seed'
  AND g.source_year = 2022
  AND g.reporting_month = 11
  AND g.source_suffix = 1
ORDER BY g.analytical_price DESC;



SELECT
    g.source_year,
    g.reporting_month,
    g.reporting_month_name,
    g.source_suffix,
    g.market,
    g.analytical_price AS gambhari_price,
    v.analytical_price AS vai_vidang_price,
    ROUND(
        g.analytical_price / NULLIF(v.analytical_price, 0),
        3
    ) AS price_ratio
FROM price_observations AS g
JOIN plants AS gp
    ON g.plant_id = gp.plant_id
JOIN price_observations AS v
    ON g.market = v.market
   AND g.source_year = v.source_year
   AND g.reporting_month = v.reporting_month
   AND g.source_suffix = v.source_suffix
JOIN plants AS vp
    ON v.plant_id = vp.plant_id
WHERE gp.trade_name_part = 'Gambhari-Bark'
  AND vp.trade_name_part = 'Vai-Vidang-Seed'
  AND g.analytical_price > 0
  AND v.analytical_price > 0
ORDER BY
    g.source_year,
    g.reporting_month,
    g.source_suffix,
    g.market;