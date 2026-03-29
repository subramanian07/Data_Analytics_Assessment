# 3. docs/design_notes

```markdown
# Design Notes

## Modeling Approach
A **star schema** is used for simplicity and BI performance.

A **snowflake extension** is applied to product category to improve governance.

---

## Fact Tables

### FactSales
- Grain: One row per order line
- Captures revenue, quantity, margin

### FactReturns
- Grain: One row per return event
- Captures return quantity and amount

---

## Why Separate Facts?
Sales and returns represent different business processes and must be modeled separately to:

- maintain clean grain
- simplify analytics
- avoid null-heavy design

---

## Conformed Dimensions

Shared across facts:

- Date
- Customer
- Product
- Store

This enables consistent reporting.

---

## Degenerate Dimensions

- sales_order_id
- sales_order_line_id

Used for drillthrough without creating extra dimension tables.

---

## Snowflake Justification

Product hierarchy is separated into:

- dim_product
- dim_product_category

Reason:
- centralized category management
- avoids redundancy