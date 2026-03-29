print("Latest notebook runs")
display(
    spark.sql("""
        SELECT *
        FROM dbo.a6_notebook_run_log
        ORDER BY created_ts DESC
    """)
)

print("Latest batch monitoring")
display(
    spark.sql("""
        SELECT *
        FROM dbo.a6_batch_monitoring_log
        ORDER BY processed_ts DESC
    """)
)

print("Valid records")
display(
    spark.sql("""
        SELECT COUNT(*) AS valid_record_count
        FROM dbo.a6_silver_valid_orders
    """)
)

print("Invalid records")
display(
    spark.sql("""
        SELECT COUNT(*) AS invalid_record_count
        FROM dbo.a6_silver_invalid_orders
    """)
)

print("Invalid reasons")
display(
    spark.sql("""
        SELECT dq_error_reason, COUNT(*) AS bad_record_count
        FROM dbo.a6_silver_invalid_orders
        GROUP BY dq_error_reason
        ORDER BY bad_record_count DESC
    """)
)

print("Latest successful Bronze run")
display(
    spark.sql("""
        SELECT MAX(end_ts) AS latest_successful_bronze_run
        FROM dbo.a6_notebook_run_log
        WHERE layer_name = 'BRONZE'
          AND status = 'SUCCESS'
    """)
)

print("Latest successful Silver run")
display(
    spark.sql("""
        SELECT MAX(end_ts) AS latest_successful_silver_run
        FROM dbo.a6_notebook_run_log
        WHERE layer_name = 'SILVER'
          AND status = 'SUCCESS'
    """)
)