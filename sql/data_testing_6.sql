USE medicinal_plant_price_trend_analysis;

SELECT
    COUNT(*) AS total_observations,
    COUNT(DISTINCT plant_id) AS distinct_plants,
    COUNT(DISTINCT market) AS distinct_markets,
    COUNT(DISTINCT source_year) AS distinct_years,

    SUM(CASE
        WHEN analytical_price > 0 THEN 1
        ELSE 0
    END) AS positive_price_records,

    SUM(CASE
        WHEN analytical_price IS NULL THEN 1
        ELSE 0
    END) AS missing_price_records,

    SUM(CASE
        WHEN analytical_price = 0 THEN 1
        ELSE 0
    END) AS zero_price_records,

    SUM(CASE
        WHEN analytical_price < 0 THEN 1
        ELSE 0
    END) AS negative_price_records,

    COUNT(DISTINCT CASE
        WHEN analytical_price > 0 THEN market
    END) AS markets_with_positive_prices

FROM price_observations;


SELECT
    data_quality_status,
    analytical_price_status,
    COUNT(*) AS observation_count,
    SUM(
        CASE WHEN analytical_price > 0 THEN 1 ELSE 0 END
    ) AS positive_price_count,
    SUM(
        CASE WHEN analytical_price IS NULL THEN 1 ELSE 0 END
    ) AS missing_analytical_price_count,
    SUM(
        CASE WHEN analytical_price = 0 THEN 1 ELSE 0 END
    ) AS zero_price_count
FROM price_observations
GROUP BY
    data_quality_status,
    analytical_price_status
ORDER BY observation_count DESC;


SELECT
    source_year,
    COUNT(*) AS total_records,

    SUM(CASE
        WHEN analytical_price > 0 THEN 1
        ELSE 0
    END) AS positive_prices,

    SUM(CASE
        WHEN analytical_price IS NULL THEN 1
        ELSE 0
    END) AS missing_prices,

    SUM(CASE
        WHEN analytical_price = 0 THEN 1
        ELSE 0
    END) AS zero_prices,

    ROUND(
        100.0 * SUM(
            CASE WHEN analytical_price > 0 THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS positive_price_coverage_pct

FROM price_observations
GROUP BY source_year
ORDER BY source_year;