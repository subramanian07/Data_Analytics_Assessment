# Retail Data Analytics Platform – Lakehouse Medallion Pipeline

## Overview

This project implements an end-to-end batch data pipeline using Microsoft Fabric Lakehouse following the Medallion Architecture (Bronze, Silver, Gold).

The pipeline ingests raw enterprise-style data, cleans and standardizes it, and builds analytical datasets for reporting.

---

## Architecture

The solution follows a layered design:

* **Bronze Layer** → Raw ingestion (as-is)
* **Silver Layer** → Data cleansing & validation
* **Gold Layer** → Business-ready analytics model

---

## Source Data

The pipeline processes the following files:

* customers.csv
* products.csv
* orders.csv
* order_items.json
* returns.csv

These datasets contain:

* duplicate records
* null values
* invalid keys
* inconsistent date formats
* late-arriving data

---

## Technologies Used

* Microsoft Fabric Lakehouse
* PySpark (Notebooks)
* Delta Lake
* SQL (DDL scripts)

---

## Pipeline Flow

### 1. Bronze Layer

* Ingests data **exactly as received**
* Adds audit columns:

  * ingestion_ts
  * source_file_name
  * pipeline_run_id

---

### 2. Silver Layer

* Cleans and standardizes data
* Handles:

  * duplicates
  * null values
  * invalid product IDs
  * date normalization
* Invalid records are stored in **error tables**
* Uses Delta MERGE for idempotent processing

---

### 3. Gold Layer

Creates analytical model:

#### Dimensions

* dim_customer
* dim_product
* dim_date

#### Facts

* fact_sales
* fact_returns

Optimized for reporting (Power BI ready)

---

## Incremental Processing

* Implemented using Delta Lake MERGE
* Ensures:

  * idempotent reruns
  * late-arriving data handling
  * no duplicate records

---

## Audit & Logging

Control tables:

* pl_control_config_log → step-level logging
* pl_bad_records_log → optional reject tracking
* pl_watermark_log → incremental framework

Features:

* pipeline_run_id tracking across layers
* step-level status (STARTED, SUCCESS, FAILED)
* restart capability

---

## Bad Records Handling

* Bronze → stores all records (no filtering)
* Silver → applies validation
* Invalid records → stored in error tables
* Pipeline continues processing valid data

---

## Project Structure

```
Retail_Data_Analytics_Platform/
│
├── README.md
├── assumptions.md
├── setup_and_run.md
├── architecture_design.md
│
├── notebooks/
│   ├── 01_setup/
│   │   ├── nb_audit_control_tables_pyspark.ipynb
│   │   └── nb_audit_control_tables_sql.ipynb
│   │
│   ├── 02_bronze/
│   │   ├── nb_01_bronze_ingestion.ipynb
│   │   └── nb_validate_bronze_tables.ipynb
│   │
│   ├── 03_silver/
│   │   ├── nb_02_silver_transformation.ipynb
│   │   └── nb_validate_silver_tables.ipynb
│   │
│   ├── 04_gold/
│   │   ├── nb_03_gold_curated.ipynb
│   │   └── nb_validate_gold_tables.ipynb
│
├── sql/
│   ├── 01_create_control_tables.sql
│   └── 02_create_gold_tables.sql
│
├── docs/
│   ├── bad_records_handling.md
│   ├── incremental_loading_design.md
│   └── folder_and_table_structure.md
│
└── sample_output/
    ├── gold_fact_sales_sample.png
    ├── gold_dim_customer_sample.png
    ├── gold_dim_product_sample.png
    ├── gold_dim_date_sample.png
    └── gold_fact_returns_sample.png
```

---

## How to Run

1. Run setup notebook
2. Run Bronze ingestion
3. Run Silver transformation
4. Run Gold curation

Refer: `setup_and_run.md`

---

## Output

Final datasets:

* fact_sales
* fact_returns
* dim_customer
* dim_product
* dim_date

---

## Key Design Principles

* Medallion architecture
* Separation of concerns
* Delta Lake for reliability
* Modular notebooks
* Scalable design

---

## Author
Subramanian Thirunavukkarasu