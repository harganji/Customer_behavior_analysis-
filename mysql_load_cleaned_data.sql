CREATE DATABASE IF NOT EXISTS customer_behavior;
USE customer_behavior;

-- The Python notebook/script writes the cleaned dataframe to this table:
-- customer_behavior.customer_data

SELECT COUNT(*) AS rows_loaded
FROM customer_data;

SELECT *
FROM customer_data
LIMIT 10;
