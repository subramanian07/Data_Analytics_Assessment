CREATE TABLE dbo.fact_returns (
    return_fact_key         BIGINT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    return_date_key         INT NOT NULL,
    customer_key            INT NOT NULL,
    product_key             INT NOT NULL,
    store_key               INT NOT NULL,
    sales_order_id          VARCHAR(50) NOT NULL,
    sales_order_line_id     VARCHAR(50) NOT NULL,
    return_id               VARCHAR(50) NOT NULL,
    return_quantity         INT NOT NULL,
    return_amount           DECIMAL(18,2) NOT NULL,
    CONSTRAINT fk_fact_returns_date
        FOREIGN KEY (return_date_key) REFERENCES dbo.dim_date(date_key),
    CONSTRAINT fk_fact_returns_customer
        FOREIGN KEY (customer_key) REFERENCES dbo.dim_customer(customer_key),
    CONSTRAINT fk_fact_returns_product
        FOREIGN KEY (product_key) REFERENCES dbo.dim_product(product_key),
    CONSTRAINT fk_fact_returns_store
        FOREIGN KEY (store_key) REFERENCES dbo.dim_store(store_key)
);