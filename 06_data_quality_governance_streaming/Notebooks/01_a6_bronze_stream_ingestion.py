from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# from 00_a6_config_and_helpers import *
# In Fabric, paste helper functions in a utility notebook and reference it

run_id = generate_run_id()
notebook_name = "01_a6_bronze_stream_ingestion"
layer_name = "BRONZE"

bronze_table = A6_CONFIG["bronze_table"]
checkpoint_path = A6_CONFIG["bronze_checkpoint"]

log_notebook_start(
    run_id=run_id,
    notebook_name=notebook_name,
    layer_name=layer_name,
    source_name="eventhub_or_kafka_orders",
    target_name=bronze_table,
    watermark_value=None
)

order_event_schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("unit_price", DoubleType(), True),
    StructField("event_ts", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("source_system", StringType(), True)
])

try:
    # --------------------------------------------------------
    # Replace below with real Kafka / Event Hub source if needed
    # --------------------------------------------------------
    source_path = "Files/assessment_06/input/order_events"

    raw_stream_df = (
        spark.readStream
             .format("json")
             .schema(order_event_schema)
             .load(source_path)
    )

    bronze_df = (
        raw_stream_df
        .withColumn("message_key", F.lit(None).cast("string"))
        .withColumn("message_value", F.to_json(F.struct("*")))
        .withColumn("topic_name", F.lit("orders-topic"))
        .withColumn("partition_id", F.lit(0))
        .withColumn("offset_value", F.lit(None).cast("long"))
        .withColumn("kafka_ingestion_ts", F.current_timestamp())
        .withColumn("event_ts_parsed", F.to_timestamp("event_ts"))
        .withColumn("bronze_ingestion_ts", F.current_timestamp())
        .withColumn("ingestion_date", F.to_date(F.current_timestamp()))
    )

    def process_bronze_batch(batch_df, batch_id):
        if batch_df.rdd.isEmpty():
            return

        total_input_records = batch_df.count()

        batch_df.write.mode("append").saveAsTable(bronze_table)

        log_batch_metrics(
            run_id=run_id,
            notebook_name=notebook_name,
            layer_name=layer_name,
            batch_id=batch_id,
            source_name="eventhub_or_kafka_orders",
            target_name=bronze_table,
            watermark_value=None,
            total_input_records=total_input_records,
            deduplicated_records=total_input_records,
            duplicate_records=0,
            valid_records=0,
            invalid_records=0,
            late_records_estimated=0,
            avg_latency_seconds=0,
            status="SUCCESS"
        )

    query = (
        bronze_df.writeStream
                 .foreachBatch(process_bronze_batch)
                 .outputMode("append")
                 .option("checkpointLocation", checkpoint_path)
                 .start()
    )

    print("Bronze stream started.")
    log_notebook_end(run_id, notebook_name, "SUCCESS")

except Exception as e:
    log_notebook_end(run_id, notebook_name, "FAILED", str(e))
    raise