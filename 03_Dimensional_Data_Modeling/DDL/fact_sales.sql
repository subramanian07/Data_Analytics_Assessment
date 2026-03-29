CREATE TABLE dbo.fact_sales (
    sales_fact_key          BIGINT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    date_key                INT NOT NULL,
    customer_key            INT NOT NULL,
    product_key             INT NOT NULL,
    store_key               INT NOT NULL,
    promotion_key           INT NULL,
    sales_order_id          VARCHAR(50) NOT NULL,
    sales_order_line_id     VARCHAR(50) NOT NULL,
    order_quantity          INT NOT NULL,
    gross_sales_amount      DECIMAL(18,2) NOT NULL,
    discount_amount         DECIMAL(18,2) NOT NULL,
    net_sales_amount        DECIMAL(18,2) NOT NULL,
    unit_cost_amount        DECIMAL(18,2) NULL,
    margin_amount           DECIMAL(18,2) NULL,
    CONSTRAINT fk_fact_sales_date
        FOREIGN KEY (date_key) REFERENCES dbo.dim_date(date_key),
    CONSTRAINT fk_fact_sales_customer
        FOREIGN KEY (customer_key) REFERENCES dbo.dim_customer(customer_key),
    CONSTRAINT fk_fact_sales_product
        FOREIGN KEY (product_key) REFERENCES dbo.dim_product(product_key),
    CONSTRAINT fk_fact_sales_store
        FOREIGN KEY (store_key) REFERENCES dbo.dim_store(store_key),
    CONSTRAINT fk_fact_sales_promotion
        FOREIGN KEY (promotion_key) REFERENCES dbo.dim_promotion(promotion_key)
);