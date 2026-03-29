CREATE TABLE dbo.dim_product (
    product_key             INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    product_id              VARCHAR(50) NOT NULL,
    product_name            VARCHAR(255) NOT NULL,
    sku                     VARCHAR(100) NULL,
    brand                   VARCHAR(100) NULL,
    product_category_key    INT NOT NULL,
    unit_cost               DECIMAL(18,2) NULL,
    unit_price              DECIMAL(18,2) NULL,
    effective_from_date     DATE NOT NULL,
    effective_to_date       DATE NOT NULL,
    is_current              CHAR(1) NOT NULL,
    CONSTRAINT fk_dim_product_category
        FOREIGN KEY (product_category_key)
        REFERENCES dbo.dim_product_category(product_category_key),
    CONSTRAINT uq_dim_product UNIQUE (product_id, effective_from_date)
);