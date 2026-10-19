USE medicinal_plant_price_trend_analysis;

-- Creating a table titled "plants_staging"

CREATE TABLE plants_staging(
	botanical_name_part VARCHAR(255) NOT NULL,
    trade_name_part VARCHAR(255) NOT NULL
);

-- We've imported plants.csv using the Table Data Import Wizard

-- Validating the staging table
SELECT COUNT(*) AS staging_rows FROM plants_staging;
SELECT * FROM plants_staging ORDER BY botanical_name_part LIMIT 10;

-- Inserting plants into permanent table
INSERT INTO plants(botanical_name_part, trade_name_part)
SELECT botanical_name_part, trade_name_part FROM plants_staging;

-- Verifying the number of records
SELECT COUNT(*) AS plants_count FROM plants;

-- Checking that names match the staging table

SELECT p.plant_id, p.botanical_name_part, p.trade_name_part
FROM plants AS p
ORDER BY p.plant_id LIMIT 10;

-- Validating the Uniqueness
SELECT botanical_name_part, trade_name_part,
COUNT(*) AS duplicate_round FROM plants
GROUP BY botanical_name_part, trade_name_part
HAVING COUNT(*) >1;