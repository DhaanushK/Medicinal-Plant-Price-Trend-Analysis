USE medicinal_plant_price_trend_analysis;

CREATE OR REPLACE VIEW positive_price_observations AS
SELECT
    po.observation_id,
    p.botanical_name_part,
    p.trade_name_part,
    po.plant_id,
    po.market,
    po.source_year,
    po.reporting_month,
    po.reporting_month_name,
    po.source_suffix,
    po.fortnight,
    po.analytical_price,
    po.original_price_value,
    po.data_quality_status,
    po.analytical_price_status,
    po.source_workbook,
    po.source_sheet
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
WHERE po.analytical_price > 0;

SELECT
    COUNT(*) AS positive_observations,
    COUNT(DISTINCT plant_id) AS plants_covered,
    COUNT(DISTINCT market) AS markets_covered,
    COUNT(DISTINCT source_year) AS years_covered
FROM positive_price_observations;

SELECT
    po.market,
    COUNT(*) AS total_observations,
    SUM(
        CASE
            WHEN po.analytical_price > 0 THEN 1
            ELSE 0
        END
    ) AS positive_price_observations
FROM price_observations AS po
GROUP BY po.market
ORDER BY positive_price_observations ASC, po.market;

WITH ranked_prices AS (
    SELECT
        source_year,
        reporting_month,
        market,
        analytical_price,
        ROW_NUMBER() OVER (
            PARTITION BY source_year
            ORDER BY analytical_price
        ) AS price_rank,
        COUNT(*) OVER (
            PARTITION BY source_year
        ) AS year_count
    FROM positive_price_observations
    WHERE botanical_name_part = 'Azadirachta indica-Leaf'
),
annual_summary AS (
    SELECT
        source_year,
        COUNT(*) AS positive_observations,
        COUNT(DISTINCT market) AS markets_covered,
        COUNT(DISTINCT reporting_month) AS months_covered,
        ROUND(AVG(analytical_price), 2) AS mean_price,
        ROUND(
            AVG(
                CASE
                    WHEN price_rank IN (
                        FLOOR((year_count + 1) / 2),
                        FLOOR((year_count + 2) / 2)
                    )
                    THEN analytical_price
                END
            ),
            2
        ) AS median_price,
        MIN(analytical_price) AS minimum_price,
        MAX(analytical_price) AS maximum_price
    FROM ranked_prices
    GROUP BY source_year
)
SELECT *
FROM annual_summary
ORDER BY source_year;

WITH ranked_prices AS (
    SELECT
        market,
        source_year,
        reporting_month,
        analytical_price,
        ROW_NUMBER() OVER (
            PARTITION BY market, source_year
            ORDER BY analytical_price
        ) AS price_rank,
        COUNT(*) OVER (
            PARTITION BY market, source_year
        ) AS observation_count
    FROM positive_price_observations
    WHERE botanical_name_part = 'Azadirachta indica-Leaf'
),
market_year_summary AS (
    SELECT
        market,
        source_year,
        COUNT(*) AS positive_observations,
        COUNT(DISTINCT reporting_month) AS months_covered,
        ROUND(AVG(analytical_price), 2) AS mean_price,
        ROUND(
            AVG(
                CASE
                    WHEN price_rank IN (
                        FLOOR((observation_count + 1) / 2),
                        FLOOR((observation_count + 2) / 2)
                    )
                    THEN analytical_price
                END
            ),
            2
        ) AS median_price,
        MIN(analytical_price) AS minimum_price,
        MAX(analytical_price) AS maximum_price
    FROM ranked_prices
    GROUP BY market, source_year
)
SELECT *
FROM market_year_summary
ORDER BY market, source_year;


WITH monthly_ranked AS (
    SELECT
        market,
        source_year,
        reporting_month,
        reporting_month_name,
        analytical_price,
        ROW_NUMBER() OVER (
            PARTITION BY market, source_year, reporting_month
            ORDER BY analytical_price
        ) AS price_rank,
        COUNT(*) OVER (
            PARTITION BY market, source_year, reporting_month
        ) AS observation_count
    FROM positive_price_observations
    WHERE botanical_name_part = 'Azadirachta indica-Leaf'
      AND market IN ('Berhampur', 'Silliguri', 'Kolkata')
),
monthly_summary AS (
    SELECT
        market,
        source_year,
        reporting_month,
        reporting_month_name,
        COUNT(*) AS positive_observations,
        ROUND(AVG(analytical_price), 2) AS mean_price,
        ROUND(
            AVG(
                CASE
                    WHEN price_rank IN (
                        FLOOR((observation_count + 1) / 2),
                        FLOOR((observation_count + 2) / 2)
                    )
                    THEN analytical_price
                END
            ),
            2
        ) AS median_price,
        MIN(analytical_price) AS minimum_price,
        MAX(analytical_price) AS maximum_price
    FROM monthly_ranked
    GROUP BY
        market,
        source_year,
        reporting_month,
        reporting_month_name
)
SELECT *
FROM monthly_summary
ORDER BY market, source_year, reporting_month;

SELECT
    source_year,
    reporting_month,
    reporting_month_name,
    source_suffix,
    fortnight,
    market,
    original_price_value,
    analytical_price,
    data_quality_status,
    analytical_price_status,
    source_workbook,
    source_sheet
FROM price_observations
WHERE plant_id = (
    SELECT plant_id
    FROM plants
    WHERE botanical_name_part = 'Azadirachta indica-Leaf'
)
  AND market = 'Berhampur'
  AND source_year IN (2018, 2019, 2020)
  AND analytical_price > 0
ORDER BY source_year, reporting_month, source_suffix;



SELECT
    market,
    source_year,
    COUNT(*) AS positive_observations,
    COUNT(DISTINCT reporting_month) AS months_covered,
    ROUND(AVG(analytical_price), 2) AS mean_price,
    ROUND(MIN(analytical_price), 2) AS minimum_price,
    ROUND(MAX(analytical_price), 2) AS maximum_price
FROM positive_price_observations
WHERE botanical_name_part = 'Azadirachta indica-Leaf'
  AND source_year IN (2018, 2019, 2020)
  AND market IN (
      'Berhampur',
      'Silliguri',
      'Kolkata',
      'Chennai',
      'Delhi',
      'Mumbai'
  )
GROUP BY market, source_year
ORDER BY market, source_year;


SELECT
    source_year,
    reporting_month,
    reporting_month_name,
    source_suffix,
    market,
    original_price_value,
    analytical_price,
    source_workbook,
    source_sheet
FROM price_observations
WHERE plant_id = (
    SELECT plant_id
    FROM plants
    WHERE botanical_name_part = 'Azadirachta indica-Leaf'
)
  AND market = 'Berhampur'
  AND source_year IN (2018, 2019)
  AND analytical_price > 0
ORDER BY source_year, reporting_month, source_suffix;


SELECT
    reporting_month_name,
    source_year,
    market,
    original_price_value,
    analytical_price,
    analytical_price_status,
    source_sheet
FROM price_observations
WHERE plant_id = (
    SELECT plant_id
    FROM plants
    WHERE botanical_name_part = 'Azadirachta indica-Leaf'
)
AND (
    (source_year = 2018 AND reporting_month = 1)
    OR
    (source_year = 2019 AND reporting_month = 5)
)
AND source_suffix = 1
ORDER BY market, source_year, reporting_month;


SELECT
    source_year,
    reporting_month,
    reporting_month_name,
    COUNT(*) AS positive_observations,
    ROUND(AVG(analytical_price), 2) AS mean_price,
    ROUND(MIN(analytical_price), 2) AS minimum_price,
    ROUND(MAX(analytical_price), 2) AS maximum_price
FROM positive_price_observations
WHERE botanical_name_part = 'Azadirachta indica-Leaf'
  AND market = 'Berhampur'
  AND reporting_month = 5
GROUP BY
    source_year,
    reporting_month,
    reporting_month_name
ORDER BY source_year;


SELECT
    p.botanical_name_part,
    p.trade_name_part,
    po.source_year,
    COUNT(*) AS positive_observations,
    ROUND(AVG(po.analytical_price), 2) AS mean_price,
    MIN(po.analytical_price) AS minimum_price,
    MAX(po.analytical_price) AS maximum_price
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
WHERE po.market = 'Berhampur'
  AND po.reporting_month = 5
  AND po.source_year IN (2018, 2019)
  AND po.analytical_price > 0
GROUP BY
    p.botanical_name_part,
    p.trade_name_part,
    po.source_year
ORDER BY
    p.botanical_name_part,
    p.trade_name_part,
    po.source_year;