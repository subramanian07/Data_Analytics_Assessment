from pyspark.sql import functions as F
from datetime import datetime

run_id = generate_run_id()
notebook_name = "02_a6_silver_validation_and_split"
layer_name = "SILVER"

bronze_table = A6_CONFIG["bronze_table"]
silver_valid_table = A6_CONFIG["silver_valid_table"]
silver_invalid_table = A6_CONFIG["silver_invalid_table"]
customer_dim_table = A6_CONFIG["customer_dim_table"]
checkpoint_path = A6_CONFIG["silver_checkpoint"]
watermark_value = A6_CONFIG["watermark_value"]

log_notebook_start(
    run_id=run_id,
    notebook_name=notebook_name,
    layer_name=layer_name,
    source_name=bronze_table,
    target_name=f"{silver_valid_table},{silver_invalid_table}",
    watermark_value=watermark_value
)

try:
    bronze_stream_df = spark.readStream.table(bronze_table)

    dim_customer_df = (
        spark.read.table(customer_dim_table)
             .select(F.col("customer_id").cast("string").alias("ref_customer_id"))
             .dropDuplicates()
    )

    # --------------------------------------------------------
    # Incremental logic:
    # Only newly appended bronze records are streamed forward
    # Checkpoint maintains processed progress
    # --------------------------------------------------------

    prepared_stream_df = (
        bronze_stream_df
        .withColumn("order_id", F.trim(F.col("order_id")))
        .withColumn("customer_id", F.trim(F.col("customer_id")))
        .withColumn("product_id", F.trim(F.col("product_id")))
        .withColumn("event_ts_parsed", F.coalesce(F.col("event_ts_parsed"), F.to_timestamp("event_ts")))
    )

    # --------------------------------------------------------
    # Watermark + deduplication
    # --------------------------------------------------------
    deduped_stream_df = (
        prepared_stream_df
        .withWatermark("event_ts_parsed", watermark_value)
        .dropDuplicates(["order_id", "event_ts_parsed"])
    )

    def process_silver_batch(batch_df, batch_id):
        if batch_df.rdd.isEmpty():
            return

        total_input_records = batch_df.count()

        # Late record estimation for reporting
        late_df = batch_df.filter(
            F.col("event_ts_parsed") < F.expr(f"current_timestamp() - interval 10 minutes")
        )
        late_records_estimated = late_df.count()

        df = (
            batch_df.join(
                dim_customer_df,
                batch_df.customer_id == dim_customer_df.ref_customer_id,
                "left"
            )
            .withColumn("silver_processed_ts", F.current_timestamp())
            .withColumn("created_ts", F.current_timestamp())
        )

        # DQ validations
        df = (
            df.withColumn(
                "dq_order_id_valid",
                F.when(F.col("order_id").isNotNull() & (F.col("order_id") != ""), True).otherwise(False)
            )
            .withColumn(
                "dq_customer_valid",
                F.when(F.col("ref_customer_id").isNotNull(), True).otherwise(False)
            )
            .withColumn(
                "dq_quantity_valid",
                F.when(F.col("quantity") > 0, True).otherwise(False)
            )
            .withColumn(
                "dq_event_ts_valid",
                F.when(
                    F.col("event_ts_parsed").isNotNull() &
                    (F.col("event_ts_parsed") <= F.current_timestamp()) &
                    (F.col("event_ts_parsed") >= F.expr("current_timestamp() - interval 30 days")),
                    True
                ).otherwise(False)
            )
        )

        df = (
            df.withColumn(
                "dq_error_reason",
                F.concat_ws("; ",
                    F.when(~F.col("dq_order_id_valid"), F.lit("NULL_OR_EMPTY_ORDER_ID")),
                    F.when(~F.col("dq_customer_valid"), F.lit("INVALID_CUSTOMER_ID")),
                    F.when(~F.col("dq_quantity_valid"), F.lit("QUANTITY_MUST_BE_GREATER_THAN_ZERO")),
                    F.when(~F.col("dq_event_ts_valid"), F.lit("INVALID_EVENT_TIMESTAMP"))
                )
            )
            .withColumn(
                "is_valid_record",
                F.col("dq_order_id_valid") &
                F.col("dq_customer_valid") &
                F.col("dq_quantity_valid") &
                F.col("dq_event_ts_valid")
            )
        )

        valid_df = (
            df.filter(F.col("is_valid_record") == True)
              .select(
                  F.lit(run_id).alias("run_id"),
                  F.lit(int(batch_id)).alias("batch_id"),
                  "order_id",
                  "customer_id",
                  "product_id",
                  "quantity",
                  "unit_price",
                  F.col("event_ts_parsed").alias("event_ts"),
                  "event_type",
                  "source_system",
                  "topic_name",
                  "partition_id",
                  "offset_value",
                  "bronze_ingestion_ts",
                  "silver_processed_ts",
                  "created_ts"
              )
        )

        invalid_df = (
            df.filter(F.col("is_valid_record") == False)
              .select(
                  F.lit(run_id).alias("run_id"),
                  F.lit(int(batch_id)).alias("batch_id"),
                  "order_id",
                  "customer_id",
                  "product_id",
                  "quantity",
                  "unit_price",
                  F.col("event_ts").alias("event_ts_raw"),
                  "event_ts_parsed",
                  "event_type",
                  "source_system",
                  "topic_name",
                  "partition_id",
                  "offset_value",
                  "bronze_ingestion_ts",
                  "silver_processed_ts",
                  "dq_error_reason",
                  "created_ts"
              )
        )

        valid_records = valid_df.count()
        invalid_records = invalid_df.count()

        # Since input batch already comes after dropDuplicates,
        # duplicates removed can be estimated by comparing raw bronze batch count
        # only if you track raw input earlier. For assessment, keep 0 or estimate separately.
        deduplicated_records = total_input_records
        duplicate_records = 0

        latency_df = (
            batch_df.withColumn(
                "latency_seconds",
                F.col("bronze_ingestion_ts").cast("long") - F.col("event_ts_parsed").cast("long")
            )
        )

        avg_latency_seconds = latency_df.select(F.avg("latency_seconds")).collect()[0][0]

        valid_df.write.mode("append").saveAsTable(silver_valid_table)
        invalid_df.write.mode("append").saveAsTable(silver_invalid_table)

        log_batch_metrics(
            run_id=run_id,
            notebook_name=notebook_name,
            layer_name=layer_name,
            batch_id=batch_id,
            source_name=bronze_table,
            target_name=f"{silver_valid_table},{silver_invalid_table}",
            watermark_value=watermark_value,
            total_input_records=total_input_records,
            deduplicated_records=deduplicated_records,
            duplicate_records=duplicate_records,
            valid_records=valid_records,
            invalid_records=invalid_records,
            late_records_estimated=late_records_estimated,
            avg_latency_seconds=avg_latency_seconds if avg_latency_seconds else 0,
            status="SUCCESS"
        )

    query = (
        deduped_stream_df.writeStream
                         .foreachBatch(process_silver_batch)
                         .outputMode("append")
                         .option("checkpointLocation", checkpoint_path)
                         .start()
    )

    print("Silver stream started.")
    log_notebook_end(run_id, notebook_name, "SUCCESS")

except Exception as e:
    log_notebook_end(run_id, notebook_name, "FAILED", str(e))
    raise