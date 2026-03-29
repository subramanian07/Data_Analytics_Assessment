from pyspark.sql import functions as F
from datetime import datetime
import uuid

# ============================================================
# CONFIG
# ============================================================

A6_CONFIG = {
    "bronze_table": "dbo.a6_bronze_order_events",
    "silver_valid_table": "dbo.a6_silver_valid_orders",
    "silver_invalid_table": "dbo.a6_silver_invalid_orders",
    "run_log_table": "dbo.a6_notebook_run_log",
    "batch_log_table": "dbo.a6_batch_monitoring_log",
    "customer_dim_table": "dbo.dim_customer",
    "bronze_checkpoint": "Files/assessment_06/checkpoints/bronze_orders",
    "silver_checkpoint": "Files/assessment_06/checkpoints/silver_orders",
    "watermark_value": "10 minutes"
}

# ============================================================
# RUN ID
# ============================================================

def generate_run_id(prefix="A6"):
    return f"{prefix}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"

# ============================================================
# NOTEBOOK RUN LOG HELPERS
# ============================================================

def log_notebook_start(run_id, notebook_name, layer_name, source_name, target_name, watermark_value=None):
    row = [{
        "run_id": run_id,
        "notebook_name": notebook_name,
        "layer_name": layer_name,
        "start_ts": datetime.utcnow(),
        "end_ts": None,
        "status": "STARTED",
        "source_name": source_name,
        "target_name": target_name,
        "watermark_value": watermark_value,
        "error_message": None,
        "created_ts": datetime.utcnow()
    }]
    spark.createDataFrame(row).write.mode("append").saveAsTable(A6_CONFIG["run_log_table"])

def log_notebook_end(run_id, notebook_name, status, error_message=None):
    query = f"""
    UPDATE {A6_CONFIG['run_log_table']}
       SET end_ts = current_timestamp(),
           status = '{status}',
           error_message = { 'NULL' if error_message is None else "'" + error_message.replace("'", "''") + "'" }
     WHERE run_id = '{run_id}'
       AND notebook_name = '{notebook_name}'
       AND status = 'STARTED'
    """
    spark.sql(query)

# ============================================================
# BATCH MONITORING LOG
# ============================================================

def log_batch_metrics(
    run_id,
    notebook_name,
    layer_name,
    batch_id,
    source_name,
    target_name,
    watermark_value,
    total_input_records,
    deduplicated_records,
    duplicate_records,
    valid_records,
    invalid_records,
    late_records_estimated,
    avg_latency_seconds,
    status
):
    row = [{
        "run_id": run_id,
        "notebook_name": notebook_name,
        "layer_name": layer_name,
        "batch_id": int(batch_id),
        "processed_ts": datetime.utcnow(),
        "source_name": source_name,
        "target_name": target_name,
        "watermark_value": watermark_value,
        "total_input_records": int(total_input_records),
        "deduplicated_records": int(deduplicated_records),
        "duplicate_records": int(duplicate_records),
        "valid_records": int(valid_records),
        "invalid_records": int(invalid_records),
        "late_records_estimated": int(late_records_estimated),
        "avg_latency_seconds": float(avg_latency_seconds) if avg_latency_seconds is not None else None,
        "status": status,
        "created_ts": datetime.utcnow()
    }]
    spark.createDataFrame(row).write.mode("append").saveAsTable(A6_CONFIG["batch_log_table"])