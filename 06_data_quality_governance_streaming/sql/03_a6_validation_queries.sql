-- Latest notebook runs
SELECT *
FROM dbo.a6_notebook_run_log
ORDER BY created_ts DESC;

-- Latest batch monitoring
SELECT *
FROM dbo.a6_batch_monitoring_log
ORDER BY processed_ts DESC;

-- Latest successful bronze run
SELECT MAX(end_ts) AS latest_successful_bronze_run
FROM dbo.a6_notebook_run_log
WHERE layer_name = 'BRONZE'
  AND status = 'SUCCESS';

-- Latest successful silver run
SELECT MAX(end_ts) AS latest_successful_silver_run
FROM dbo.a6_notebook_run_log
WHERE layer_name = 'SILVER'
  AND status = 'SUCCESS';

-- Silver valid count
SELECT COUNT(*) AS valid_record_count
FROM dbo.a6_silver_valid_orders;

-- Silver invalid count
SELECT COUNT(*) AS invalid_record_count
FROM dbo.a6_silver_invalid_orders;

-- Invalid reasons
SELECT
    dq_error_reason,
    COUNT(*) AS bad_record_count
FROM dbo.a6_silver_invalid_orders
GROUP BY dq_error_reason
ORDER BY bad_record_count DESC;

-- Monitoring summary
SELECT
    processed_ts,
    notebook_name,
    layer_name,
    batch_id,
    total_input_records,
    deduplicated_records,
    duplicate_records,
    valid_records,
    invalid_records,
    late_records_estimated,
    avg_latency_seconds,
    watermark_value,
    status
FROM dbo.a6_batch_monitoring_log
ORDER BY processed_ts DESC;