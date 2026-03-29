# Grain and SCD Strategy

## Fact Grain

### FactSales
One row per:
- order
- product
- store
- date

### FactReturns
One row per:
- return event
- product
- store

---

## Surrogate Keys

Used for all dimensions to:
- handle source system changes
- support SCD
- improve joins

---

## Slowly Changing Dimensions

### Type 2 (Historical Tracking)
- dim_customer
- dim_product
- dim_store

Columns:
- effective_from_date
- effective_to_date
- is_current

---

### Type 1
- dim_promotion

---

### Static
- dim_date