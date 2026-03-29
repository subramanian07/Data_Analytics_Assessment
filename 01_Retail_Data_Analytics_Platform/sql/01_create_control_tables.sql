CREATE SCHEMA IF NOT EXISTS ETL;

CREATE TABLE ETL.pl_control_config_log (
    run_id STRING,
    pipeline_name STRING,
    pipeline_step_name STRING,
    source_file_path STRING,
    target_table_name STRING,
    step_status STRING,
    pipeline_status STRING,
    record_count INT,
    error_message STRING,
    step_start_time TIMESTAMP,
    step_end_time TIMESTAMP,
    pipeline_start_time TIMESTAMP,
    pipeline_end_time TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
) 
USING DELTA;

CREATE TABLE ETL.pl_bad_records_log (
    run_id STRING,
    pipeline_name STRING,
    pipeline_step_name STRING,
    error_data STRING,
    error_message STRING,
    created_at TIMESTAMP
)
USING DELTA;

CREATE TABLE ETL.pl_watermark_log (
    run_id STRING,
    pipeline_name STRING,
    pipeline_step_name STRING,
    source_name STRING,
    watermark_column STRING,
    watermark_value STRING,
    updated_at TIMESTAMP
)
USING DELTA;