# Governance Design Note

## 1. Lineage
The solution captures lineage from source stream to Bronze and Silver using:
- source topic/event hub name
- partition_id
- offset_value
- bronze_ingestion_ts
- silver_processed_ts
- notebook run logs
- batch monitoring logs

## 2. Data Catalog Metadata
The following datasets should be registered/documented:
- dbo.a6_bronze_order_events
- dbo.a6_silver_valid_orders
- dbo.a6_silver_invalid_orders
- dbo.a6_notebook_run_log
- dbo.a6_batch_monitoring_log

Metadata to document:
- business definition
- owner
- refresh type
- schema
- sensitivity
- retention period
- DQ rules

## 3. Access Control
Recommended access:
- Engineers: read/write Bronze and Silver
- Stewards/Operations: read invalid + logs
- BI consumers: read curated valid Silver only

## 4. Retention and Versioning
- Bronze retained for replay and audit
- Silver valid retained for reporting
- Silver invalid retained for remediation
- Delta supports version history and recovery

## 5. Trust for Power BI
Power BI should use only curated valid Silver/Gold data, not raw Bronze.
Trust is supported by:
- DQ validation
- duplicate removal
- late-arriving data handling
- monitoring logs
- invalid record quarantine
- traceable lineage