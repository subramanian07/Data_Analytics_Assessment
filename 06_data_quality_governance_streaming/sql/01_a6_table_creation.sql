-- ============================================================
-- BUSINESS TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS dbo.a6_bronze_order_events
(
    message_key             VARCHAR(200),
    message_value           VARCHAR(4000),
    topic_name              VARCHAR(200),
    partition_id            INT,
    offset_value            BIGINT,
    kafka_ingestion_ts      DATETIME2,
    order_id                VARCHAR(100),
    customer_id             VARCHAR(100),
    product_id              VARCHAR(100),
    quantity                INT,
    unit_price              DECIMAL(18,2),
    event_ts                VARCHAR(100),
    event_ts_parsed         DATETIME2,
    event_type              VARCHAR(100),
    source_system           VARCHAR(100),
    bronze_ingestion_ts     DATETIME2,
    ingestion_date          DATE
);

CREATE TABLE IF NOT EXISTS dbo.a6_silver_valid_orders
(
    silver_valid_id         BIGINT GENERATED ALWAYS AS IDENTITY,
    run_id                  VARCHAR(100),
    batch_id                BIGINT,
    order_id                VARCHAR(100),
    customer_id             VARCHAR(100),
    product_id              VARCHAR(100),
    quantity                INT,
    unit_price              DECIMAL(18,2),
    event_ts                DATETIME2,
    event_type              VARCHAR(100),
    source_system           VARCHAR(100),
    topic_name              VARCHAR(200),
    partition_id            INT,
    offset_value            BIGINT,
    bronze_ingestion_ts     DATETIME2,
    silver_processed_ts     DATETIME2,
    created_ts              DATETIME2
);

CREATE TABLE IF NOT EXISTS dbo.a6_silver_invalid_orders
(
    silver_invalid_id       BIGINT GENERATED ALWAYS AS IDENTITY,
    run_id                  VARCHAR(100),
    batch_id                BIGINT,
    order_id                VARCHAR(100),
    customer_id             VARCHAR(100),
    product_id              VARCHAR(100),
    quantity                INT,
    unit_price              DECIMAL(18,2),
    event_ts_raw            VARCHAR(100),
    event_ts_parsed         DATETIME2,
    event_type              VARCHAR(100),
    source_system           VARCHAR(100),
    topic_name              VARCHAR(200),
    partition_id            INT,
    offset_value            BIGINT,
    bronze_ingestion_ts     DATETIME2,
    silver_processed_ts     DATETIME2,
    dq_error_reason         VARCHAR(2000),
    created_ts              DATETIME2
);