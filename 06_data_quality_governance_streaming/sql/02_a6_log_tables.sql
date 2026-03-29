-- ============================================================
-- NOTEBOOK RUN LOG
-- One row per notebook execution
-- ============================================================

CREATE TABLE IF NOT EXISTS dbo.a6_notebook_run_log
(
    run_log_id              BIGINT GENERATED ALWAYS AS IDENTITY,
    run_id                  VARCHAR(100),
    notebook_name           VARCHAR(200),
    layer_name              VARCHAR(50),      -- BRONZE / SILVER
    start_ts                DATETIME2,
    end_ts                  DATETIME2,
    status                  VARCHAR(50),      -- STARTED / SUCCESS / FAILED
    source_name             VARCHAR(200),
    target_name             VARCHAR(200),
    watermark_value         VARCHAR(50),
    error_message           VARCHAR(2000),
    created_ts              DATETIME2
);

-- ============================================================
-- BATCH MONITORING LOG
-- One row per micro-batch
-- ============================================================

CREATE TABLE IF NOT EXISTS dbo.a6_batch_monitoring_log
(
    batch_log_id                BIGINT GENERATED ALWAYS AS IDENTITY,
    run_id                      VARCHAR(100),
    notebook_name               VARCHAR(200),
    layer_name                  VARCHAR(50),
    batch_id                    BIGINT,
    processed_ts                DATETIME2,
    source_name                 VARCHAR(200),
    target_name                 VARCHAR(200),
    watermark_value             VARCHAR(50),
    total_input_records         BIGINT,
    deduplicated_records        BIGINT,
    duplicate_records           BIGINT,
    valid_records               BIGINT,
    invalid_records             BIGINT,
    late_records_estimated      BIGINT,
    avg_latency_seconds         DECIMAL(18,2),
    status                      VARCHAR(50),
    created_ts                  DATETIME2
);