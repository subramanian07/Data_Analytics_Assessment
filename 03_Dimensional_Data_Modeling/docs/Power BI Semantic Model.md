# Power BI Semantic Model

## Model Design

- Star schema
- One-to-many relationships
- Single direction filtering

---

## Benefits

- Simple DAX
- Fast performance
- Easy slicing/filtering
- Reusable measures

---

## Example Measures

Total Sales =
SUM(fact_sales[net_sales_amount])

Total Returns =
SUM(fact_returns[return_amount])

Return Rate % =
DIVIDE([Total Returns], [Total Sales], 0)

---

## Supported Analysis

- Sales trends
- Returns trends
- Customer segmentation
- Regional performance
- Product hierarchy analysis

---

## Why It Works Well

- Conformed dimensions allow cross-fact analysis
- Clean separation of facts improves clarity
- Optimized for BI tools like Power BI