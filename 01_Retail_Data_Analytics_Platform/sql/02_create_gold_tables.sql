CREATE TABLE dim_customer (
    customer_id STRING,
    customer_name STRING,
    email STRING
)
USING DELTA;

CREATE TABLE dim_product (
    product_id STRING,
    product_name STRING,
    category STRING,
    price DECIMAL(18,2)
)
USING DELTA;

CREATE TABLE dim_date (
    date DATE,
    year INT,
    month INT,
    day INT,
    quarter INT
)
USING DELTA;

CREATE TABLE fact_sales (
    order_id STRING,
    customer_id STRING,
    product_id STRING,
    order_date DATE,
    quantity INT,
    amount DECIMAL(18,2)
)
USING DELTA;

CREATE TABLE fact_returns (
    return_id STRING,
    order_id STRING,
    product_id STRING,
    return_date DATE,
    return_qty INT
)
USING DELTA;