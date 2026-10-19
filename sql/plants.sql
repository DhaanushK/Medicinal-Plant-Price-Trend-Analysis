-- Creating a databasse for our project
CREATE DATABASE medicinal_plant_price_trend_analysis;
USE medicinal_plant_price_trend_analysis;

-- Verifying whether our database got created & selected
SELECT DATABASE();

-- Creating a table titled "plants"

CREATE TABLE plants(
	plant_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    botanical_name_part VARCHAR(255) NOT NULL,
    trade_name_part VARCHAR(255) NOT NULL,
    UNIQUE KEY 	unique_plant_names(
		botanical_name_part,
        trade_name_part
	)
);

DESCRIBE plants;
SHOW TABLES;

-- Retrieving the ID Mapping from this environment
SELECT plant_id, botanical_name_part, trade_name_part FROM plants
ORDER BY plant_id;
