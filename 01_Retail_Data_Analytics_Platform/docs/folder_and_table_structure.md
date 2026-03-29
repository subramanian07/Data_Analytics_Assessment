# Folder and Table Structure

## Workspace Structure

```
Retail_Analytics_Platform
├── Bronze
├── Silver
├── Gold
├── Notebooks
├── Pipelines
├── Audit
```

---

## Lakehouse Tables

### Bronze

* bronze_customers
* bronze_products
* bronze_orders
* bronze_order_items
* bronze_returns

---

### Silver

* silver_customers
* silver_products
* silver_orders
* silver_order_items
* silver_returns

---

### Error Tables

* silver_customers_error
* silver_products_error
* silver_orders_error
* silver_order_items_error
* silver_returns_error

---

### Gold

* dim_customer
* dim_product
* dim_date
* fact_sales
* fact_returns

---

### Audit

* pl_control_config_log
* pl_bad_records_log
* pl_watermark_log