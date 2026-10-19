-- Creating tabled titled "price_observation_staging"
USE medicinal_plant_price_trend_analysis;

CREATE TABLE price_observations_staging (
    plant_id INT UNSIGNED NOT NULL,
    source_year SMALLINT UNSIGNED NOT NULL,
    reporting_month TINYINT UNSIGNED NOT NULL,
    reporting_month_name VARCHAR(10) NOT NULL,
    source_suffix TINYINT NOT NULL,
    fortnight VARCHAR(10) NOT NULL,
    period_status VARCHAR(50) NOT NULL,
    source_workbook VARCHAR(100) NOT NULL,
    source_sheet VARCHAR(150) NOT NULL,
    botanical_name_part VARCHAR(255) NOT NULL,
    trade_name_part VARCHAR(255) NOT NULL,
    market VARCHAR(250) NOT NULL,
    original_price_value VARCHAR(255) NULL,
    analytical_price DECIMAL(12,2) NULL,
    range_lower DECIMAL(12,2) NULL,
    range_upper DECIMAL(12,2) NULL,
    data_quality_status VARCHAR(100) NOT NULL,
    analytical_price_status VARCHAR(100) NOT NULL
);

ALTER TABLE price_observations_staging
    MODIFY COLUMN analytical_price VARCHAR(50) NULL,
    MODIFY COLUMN range_lower VARCHAR(50) NULL,
    MODIFY COLUMN range_upper VARCHAR(50) NULL;

TRUNCATE TABLE price_observations_staging;

SELECT COUNT(*) AS existing_staging_rows
FROM price_observations_staging;


-- Check whether LOCAL INFILE is enabled on the MySQL server.
-- The client connection must also allow LOCAL INFILE.
SHOW GLOBAL VARIABLES LIKE 'local_infile';

-- Import the CSV into the staging table.
-- Replace the placeholder with the absolute path to your CSV file.
-- Run this only when you need to load the data again.

LOAD DATA LOCAL INFILE 'REPLACE_WITH_ABSOLUTE_PATH_TO_CSV'
INTO TABLE price_observations_staging
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(
    plant_id,
    source_year,
    reporting_month,
    reporting_month_name,
    source_suffix,
    fortnight,
    period_status,
    source_workbook,
    source_sheet,
    botanical_name_part,
    trade_name_part,
    market,
    original_price_value,
    analytical_price,
    range_lower,
    range_upper,
    data_quality_status,
    analytical_price_status
);