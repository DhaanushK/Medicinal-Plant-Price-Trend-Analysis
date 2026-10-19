USE medicinal_plant_price_trend_analysis;

WITH ranked_prices AS (
    SELECT
        po.market,
        po.analytical_price,
        ROW_NUMBER() OVER (
            PARTITION BY po.market
            ORDER BY po.analytical_price
        ) AS row_num,
        COUNT(*) OVER (
            PARTITION BY po.market
        ) AS market_count
    FROM price_observations AS po
    JOIN plants AS p
        ON po.plant_id = p.plant_id
    WHERE p.botanical_name_part = 'Azadirachta indica-Leaf'
      AND po.analytical_price > 0
),
market_medians AS (
    SELECT
        market,
        AVG(analytical_price) AS median_price
    FROM ranked_prices
    WHERE row_num IN (
        FLOOR((market_count + 1) / 2),
        FLOOR((market_count + 2) / 2)
    )
    GROUP BY market
)
SELECT
    po.market,
    COUNT(*) AS observations,
    ROUND(AVG(po.analytical_price), 2) AS average_price,
    ROUND(mm.median_price, 2) AS median_price
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
JOIN market_medians AS mm
    ON po.market = mm.market
WHERE p.botanical_name_part = 'Azadirachta indica-Leaf'
  AND po.analytical_price > 0
GROUP BY po.market, mm.median_price
ORDER BY median_price DESC;

SELECT
    COUNT(*) AS total_observations,
    ROUND(AVG(analytical_price), 2) AS average_with_all_records,
    ROUND(
        AVG(
            CASE
                WHEN NOT (
                    source_year = 2023
                    AND reporting_month = 6
                    AND source_suffix = 2
                    AND analytical_price = 40240
                )
                THEN analytical_price
            END
        ),
        2
    ) AS average_without_extreme_record,
    ROUND(
        MAX(analytical_price),
        2
    ) AS maximum_price
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
WHERE p.botanical_name_part = 'Azadirachta indica-Leaf'
  AND po.market = 'Kolkata'
  AND po.analytical_price > 0;

  WITH yearly_market_prices AS (
    SELECT
        po.market,
        po.source_year,
        po.analytical_price,
        ROW_NUMBER() OVER (
            PARTITION BY po.market, po.source_year
            ORDER BY po.analytical_price
        ) AS row_num,
        COUNT(*) OVER (
            PARTITION BY po.market, po.source_year
        ) AS row_count
    FROM price_observations AS po
    JOIN plants AS p
        ON po.plant_id = p.plant_id
    WHERE p.botanical_name_part = 'Azadirachta indica-Leaf'
      AND po.analytical_price > 0
),
yearly_medians AS (
    SELECT
        market,
        source_year,
        AVG(analytical_price) AS median_price
    FROM yearly_market_prices
    WHERE row_num IN (
        FLOOR((row_count + 1) / 2),
        FLOOR((row_count + 2) / 2)
    )
    GROUP BY market, source_year
)
SELECT
    po.market,
    po.source_year,
    COUNT(*) AS observations,
    ROUND(AVG(po.analytical_price), 2) AS average_price,
    ROUND(ym.median_price, 2) AS median_price
FROM price_observations AS po
JOIN plants AS p
    ON po.plant_id = p.plant_id
JOIN yearly_medians AS ym
    ON po.market = ym.market
   AND po.source_year = ym.source_year
WHERE p.botanical_name_part = 'Azadirachta indica-Leaf'
  AND po.analytical_price > 0
GROUP BY
    po.market,
    po.source_year,
    ym.median_price
ORDER BY
    po.market,
    po.source_year;


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