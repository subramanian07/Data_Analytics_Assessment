CREATE TABLE dbo.dim_product_category (
    product_category_key    INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    department_name         VARCHAR(100) NOT NULL,
    category_name           VARCHAR(100) NOT NULL,
    subcategory_name        VARCHAR(100) NOT NULL
);