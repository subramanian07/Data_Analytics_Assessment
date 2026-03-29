# Setup and Run Guide

## Prerequisites
- Microsoft Fabric workspace
- Lakehouse created and attached to all notebooks
- Source files uploaded to Lakehouse Files/raw

## Source files
- customers.csv
- products.csv
- orders.csv
- order_items.json
- returns.csv

## Execution order

### Step 1: Create control tables
Run:
- nb_audit_control_tables_pyspark.ipynb

### Step 2: Bronze ingestion
Run:
- nb_01_bronze_ingestion.ipynb

Validate:
- nb_validate_bronze_tables.ipynb

### Step 3: Silver transformation
Run:
- nb_02_silver_transformation.ipynb

Validate:
- nb_validate_silver_tables.ipynb

### Step 4: Gold curation
Run:
- nb_03_gold_curated.ipynb

Validate:
- nb_validate_gold_tables.ipynb

## Notes
- Attach Retail_Analytics_Lakehouse to every notebook before execution.
- Use the same pipeline_run_id across Bronze, Silver, and Gold during one manual test cycle.
- Bronze stores all source rows as received.
- Silver handles data quality validation and redirects invalid rows to error tables.
- Gold builds curated fact and dimension tables for reporting.