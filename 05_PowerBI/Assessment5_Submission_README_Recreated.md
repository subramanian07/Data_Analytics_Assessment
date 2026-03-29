# Assessment 5 - Power BI Semantic Model and DAX Optimization

## Submission contents

- `Assessment5_DAX_Measures_Recreated.docx` - DAX measures and implementation notes
- `Assessment5_Submission_README_Recreated.md` - this README
- `Assessment5_PowerBI_Build_Guide.docx` - step-by-step build guide already prepared earlier

## Scope used for this assessment

This submission uses the simplified Gold-layer model available in the Fabric Lakehouse:

- `gold_fact_sales`
- `gold_fact_returns`
- `gold_dim_date`
- `gold_dim_customer`
- `gold_dim_product`

`DimStore` and `DimPromotion` were not available in the Gold layer, so they were intentionally excluded from the semantic model.

## Semantic model design

### Tables used

**Fact tables**
- `gold_fact_sales`
- `gold_fact_returns`

**Dimension tables**
- `gold_dim_date`
- `gold_dim_customer`
- `gold_dim_product`

### Relationship design

Recommended relationships:

- `gold_fact_sales[order_date_key]` -> `gold_dim_date[date_key]`
- `gold_fact_sales[customer_key]` -> `gold_dim_customer[customer_key]`
- `gold_fact_sales[product_key]` -> `gold_dim_product[product_key]`
- `gold_fact_returns[return_date_key]` -> `gold_dim_date[date_key]`
- `gold_fact_returns[customer_key]` -> `gold_dim_customer[customer_key]`
- `gold_fact_returns[product_key]` -> `gold_dim_product[product_key]`

### Cardinality and cross-filter direction

- Cardinality: **Many-to-one** from fact to dimension
- Cross-filter direction: **Single direction** from dimension to fact

This keeps the model predictable, avoids ambiguous filtering, and improves performance.

## Date table

Use `gold_dim_date` as the dedicated date table and mark `gold_dim_date[full_date]` as the official date column in Power BI.

Typical date columns:
- `date_key`
- `full_date`
- `year`
- `quarter`
- `month_number`
- `month_name`
- `year_month`

## Measures implemented

Minimum measures covered in the DAX file:

1. Total Sales
2. Total Cost
3. Total Returns Amount
4. Net Sales
5. Gross Margin
6. Gross Margin %
7. Return Rate %
8. Order Count
9. Average Order Value
10. Customer Count
11. Sales LY
12. YoY Sales Growth %
13. Top Product Rank
14. Sales PM
15. MoM Sales Growth %

## Incremental refresh

Incremental refresh should be configured on the large fact tables:

- `gold_fact_sales`
- `gold_fact_returns`

### Suggested policy

- Store data for **5 years**
- Refresh only the **last 1 month**

### Setup summary

1. In Power Query, create parameters `RangeStart` and `RangeEnd` as DateTime.
2. Filter sales date using:
   - `order_date >= RangeStart`
   - `order_date < RangeEnd`
3. Filter returns date using:
   - `return_date >= RangeStart`
   - `return_date < RangeEnd`
4. Apply incremental refresh in model settings for each fact table.

## Performance optimization approach

The model uses the following optimization choices:

- Star-schema design with separate fact and dimension tables
- Single-direction relationships only
- Dedicated date table for time intelligence
- Business logic implemented as measures instead of unnecessary calculated columns
- Hide technical keys from report view
- Remove unused columns to reduce memory footprint
- Incremental refresh on transaction facts

### Optional aggregation strategy

If needed, create an aggregated table at `YearMonth x Product Category` or `YearMonth x Region` grain for faster KPI and trend visuals.

## RLS definition

### Preferred approach

If a `region` column exists in `gold_dim_customer`, implement dynamic RLS using a small security mapping table.

Example table:

- `security_region_access[user_email]`
- `security_region_access[region]`

Role filter:

```DAX
[user_email] = USERPRINCIPALNAME()
```

Then relate the security table to the customer dimension through region.

### Fallback approach

If region is not available, document that Region Manager RLS could not be implemented exactly from the current Gold layer and demonstrate RLS using another available business attribute such as customer segment or product category.

## Suggested report pages

### Page 1 - Executive Sales Overview

Recommended visuals:
- KPI cards: Total Sales, Net Sales, Gross Margin %, Return Rate %, Customer Count, Average Order Value
- Line chart: Net Sales by YearMonth
- Bar chart: Top Products by Net Sales
- Donut or bar chart: Sales by Product Category
- Matrix: Customer segment or category performance

### Page 2 - Returns and Customer Insights

Recommended visuals:
- Return Rate % by Product Category
- Customer Count by segment or region
- Monthly Returns trend
- Product table with Net Sales, Return Rate %, and Top Product Rank

## Screenshot checklist for submission

Capture these screenshots for the final assessment pack:

1. **Model view** showing relationships
2. **Measures pane** with key DAX measures
3. **Incremental refresh setup** on fact tables
4. **Manage roles / RLS setup**
5. **Report page 1**
6. **Report page 2**

## Final explanation to assessor

This semantic model was built on the available Gold-layer tables in Fabric using a simplified star schema. Since `DimStore` and `DimPromotion` were not available, the model uses Sales and Returns facts with Date, Customer, and Product dimensions. The model supports core business reporting through reusable DAX measures such as Total Sales, Net Sales, Gross Margin %, Return Rate, Average Order Value, YoY Sales Growth, Customer Count, and Top Product Rank. Performance considerations include single-direction relationships, a dedicated date table, hidden technical keys, and incremental refresh on the fact tables. Dynamic RLS can be implemented for Region Managers when a region attribute is available in the dimensional model.
