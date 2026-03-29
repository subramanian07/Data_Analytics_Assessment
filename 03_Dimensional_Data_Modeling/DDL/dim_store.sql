CREATE TABLE dbo.dim_store (
    store_key               INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    store_id                VARCHAR(50) NOT NULL,
    store_name              VARCHAR(255) NOT NULL,
    store_type              VARCHAR(50) NULL,
    city                    VARCHAR(100) NULL,
    state                   VARCHAR(100) NULL,
    country                 VARCHAR(100) NULL,
    region                  VARCHAR(100) NULL,
    opening_date            DATE NULL,
    effective_from_date     DATE NOT NULL,
    effective_to_date       DATE NOT NULL,
    is_current              CHAR(1) NOT NULL,
    CONSTRAINT uq_dim_store UNIQUE (store_id, effective_from_date)
);