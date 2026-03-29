# Incremental Loading Design

## Design choice
Source files are batch files uploaded to the Fabric Lakehouse raw area.

Because the source is not being extracted incrementally from a live operational source, the working implementation does not apply source-side watermark filtering.

## Implemented incremental behavior
Incremental logic is implemented using Delta MERGE in:
- Silver tables
- Gold tables

## Benefits
- idempotent reruns
- late-arriving data can be reprocessed safely
- duplicates are prevented on rerun
- business keys are used for upsert logic

## Example merge keys
- silver_customers: customer_id
- silver_products: product_id
- silver_orders: order_id
- silver_order_items: order_id + product_id
- silver_returns: return_id
- fact_sales: order_id + product_id
- fact_returns: return_id