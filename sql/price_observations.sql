USE medicinal_plant_price_trend_analysis;

-- Creating a table titled "price_observations"
DROP TABLE price_observations;

CREATE TABLE price_observations(
	observation_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    plant_id INT UNSIGNED NOT NULL,
    market VARCHAR(250) NOT NULL,
    source_year SMALLINT UNSIGNED NOT NULL,
    reporting_month TINYINT UNSIGNED NOT NULL,
    reporting_month_name VARCHAR(10) NOT NULL,
    source_suffix TINYINT NOT NULL,
    fortnight VARCHAR(10) NOT NULL,
    period_status VARCHAR(50) NOT NULL,
    source_workbook VARCHAR(100) NOT NULL,
    source_sheet VARCHAR(150) NOT NULL,
    original_price_value VARCHAR(255) NULL,
    analytical_price DECIMAL(12,2) NULL,
    range_lower DECIMAL(12,2) NULL,
    range_upper DECIMAL(12,2) NULL,
    data_quality_status VARCHAR(100) NOT NULL,
    analytical_price_status VARCHAR(100) NOT NULL,

    CONSTRAINT fk_observation_plant FOREIGN KEY (plant_id) REFERENCES plants(plant_id),
    CONSTRAINT chk_reporting_month CHECK (reporting_month BETWEEN 1 AND 12),

    INDEX idx_market_period (market, source_year, reporting_month),
    INDEX idx_plant_period (plant_id, source_year, reporting_month),
    INDEX idx_analytical_price (analytical_price)
);

DESCRIBE price_observations;