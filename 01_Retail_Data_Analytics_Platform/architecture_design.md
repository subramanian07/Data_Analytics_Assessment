###### Architecture Design ######

## Overview
This project implements a batch Medallion Architecture in Microsoft Fabric Lakehouse.

## Bronze Layer
Purpose:
- ingest raw files exactly as received
- preserve replayable raw history
- add audit metadata

Tables:
- bronze_customers
- bronze_products
- bronze_orders
- bronze_order_items
- bronze_returns

## Silver Layer
Purpose:
- standardize and clean source data
- apply validation checks
- separate invalid rows
- support incremental idempotent loads

Tables:
- silver_customers
- silver_products
- silver_orders
- silver_order_items
- silver_returns

Error tables:
- silver_customers_error
- silver_products_error
- silver_orders_error
- silver_order_items_error
- silver_returns_error

## Gold Layer
Purpose:
- provide business-ready analytical model for reporting

Dimensions:
- dim_customer
- dim_product
- dim_date

Facts:
- fact_sales
- fact_returns

## Audit and Logging
- pl_control_config_log stores run-level and step-level execution status
- pipeline_run_id enables traceability across layers
- Silver error tables document row-level data quality issues

## Incremental Processing
Incremental and rerun-safe behavior is implemented using Delta MERGE in Silver and Gold.