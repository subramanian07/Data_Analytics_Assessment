# Assessment 6 - Data Quality, Governance, and Streaming Mini Project

## Overview
This project implements a near-real-time streaming ingestion flow for order events using Bronze and Silver layers.

## Flow
1. Bronze notebook ingests streaming events into raw Bronze table
2. Silver notebook reads Bronze incrementally as stream
3. Watermark is applied on event timestamp
4. Deduplication is applied using order_id + event_ts
5. Data quality validations are applied
6. Valid and invalid records are separated
7. Log tables capture notebook runs and micro-batch monitoring metrics

## Tables
### Business tables
- dbo.a6_bronze_order_events
- dbo.a6_silver_valid_orders
- dbo.a6_silver_invalid_orders

### Log tables
- dbo.a6_notebook_run_log
- dbo.a6_batch_monitoring_log

## Incremental Logic
Incremental processing is handled through Structured Streaming checkpoints:
- Bronze checkpoint tracks source ingestion progress
- Silver checkpoint tracks Bronze-to-Silver progress

## Watermark and Late Data
Watermark on event_ts_parsed is set to 10 minutes.
This allows late-arriving events within 10 minutes to be processed while keeping streaming state bounded.

## Data Quality Rules
- order_id must not be null or empty
- customer_id must exist in reference customer table
- quantity must be greater than zero
- event timestamp must be valid, not future-dated, and within acceptable range

## Monitoring
Monitoring captures:
- total input records
- valid records
- invalid records
- estimated late records
- average latency
- notebook run status
- latest successful runs