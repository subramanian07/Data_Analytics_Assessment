CREATE INDEX ix_dim_date_date_key ON dbo.dim_date(date_key);
CREATE INDEX ix_dim_customer_customer_key ON dbo.dim_customer(customer_key);
CREATE INDEX ix_dim_product_product_key ON dbo.dim_product(product_key);
CREATE INDEX ix_dim_product_category_product_category_key ON dbo.dim_product_category(product_category_key);
CREATE INDEX ix_dim_store_store_key ON dbo.dim_store(store_key);
CREATE INDEX ix_dim_promotion_promotion_key ON dbo.dim_promotion(promotion_key);

CREATE INDEX ix_fact_sales_date_key ON dbo.fact_sales(date_key);
CREATE INDEX ix_fact_sales_customer_key ON dbo.fact_sales(customer_key);
CREATE INDEX ix_fact_sales_product_key ON dbo.fact_sales(product_key);
CREATE INDEX ix_fact_sales_store_key ON dbo.fact_sales(store_key);

CREATE INDEX ix_fact_returns_date_key ON dbo.fact_returns(return_date_key);
CREATE INDEX ix_fact_returns_product_key ON dbo.fact_returns(product_key);
CREATE INDEX ix_fact_returns_store_key ON dbo.fact_returns(store_key);