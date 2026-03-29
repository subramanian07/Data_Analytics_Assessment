CREATE TABLE dbo.dim_promotion (
    promotion_key           INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    promotion_id            VARCHAR(50) NOT NULL,
    promotion_name          VARCHAR(255) NOT NULL,
    promotion_type          VARCHAR(50) NULL,
    campaign_name           VARCHAR(100) NULL,
    discount_percent        DECIMAL(5,2) NULL,
    start_date              DATE NULL,
    end_date                DATE NULL,
    CONSTRAINT uq_dim_promotion UNIQUE (promotion_id)
);