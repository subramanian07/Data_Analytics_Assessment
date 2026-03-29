# Retail Dimensional Data Modeling – Assessment 3

## Objective
Design an enterprise-ready dimensional data warehouse model for retail analytics covering:

- Sales performance
- Returns analysis
- Customer behavior
- Product trends
- Regional revenue

---

## Approach

The model follows a **Star Schema** with one **Snowflake extension** for product hierarchy.

### Fact Tables
- fact_sales → Sales transactions (order line level)
- fact_returns → Return transactions (return event level)

### Conformed Dimensions
- dim_date
- dim_customer
- dim_product
- dim_store

### Additional Dimensions
- dim_promotion
- dim_product_category (snowflake extension)

---

## Key Design Highlights

- Clearly defined **fact grain**
- **Surrogate keys** used across dimensions
- **SCD Type 2** for customer, product, store
- **Degenerate dimensions** for order tracking
- Designed for **Power BI semantic modeling**

---

## Folder Overview

| Folder    | Description |
|-----------|-------------|
| diagrams  | Schema diagram |
| ddl       | Table creation scripts |
| docs      | Design explanation |

---

## How to Use

1. Execute DDL scripts in order
2. Load dimension tables first
3. Load fact tables
4. Connect Power BI using star schema relationships

---

## Business Value

This model enables:

- Sales vs Returns comparison
- Customer segmentation analysis
- Product category performance
- Regional reporting
- Time-based trend analysis

---

## Author
Subramanian