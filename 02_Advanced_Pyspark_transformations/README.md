# Assessment 2: Advanced PySpark Transformation and Performance Optimization

## Objective

The objective of this assessment is to demonstrate PySpark capabilities in handling large-scale data transformations (20M+ rows) and applying performance optimization techniques.

---

## Dataset

A synthetic retail dataset was generated using PySpark:

* **Fact Sales**: 20 million rows
* **Fact Returns**: 2 million rows
* **Dimensions**:

  * Customer (1M rows)
  * Product (100K rows)

All datasets were stored as Delta tables.

---

## Business Outputs

The following transformations were implemented:

1. **Daily Sales by Region**
2. **Top 10 Products by Category**
3. **Customer Lifetime Value (CLV)**
4. **Monthly Return Rate**

---

## Approach

### Naive Implementation

* Direct transformations on full dataset
* No explicit performance tuning
* Standard joins and aggregations

### Optimized Implementation

Applied multiple Spark optimization techniques:

* Column pruning (select only required columns)
* Early filtering (predicate pushdown)
* Broadcast join for small dimension tables
* Persisting reused DataFrames
* Partitioned Delta table (year/month)
* File compaction (OPTIMIZE)
* Z-ordering (if supported)

---

## Runtime Comparison

| Approach  | Runtime (seconds) |
| --------- | ----------------- |
| Naive     | ~28.7 sec         |
| Optimized | ~30.3 sec         |

---

## Key Observation

Although optimization techniques were applied, the runtime difference was minimal. This is because:

* The workload is **write-heavy**
* Delta table writes (~26 seconds) dominate total runtime
* Transformation optimizations have limited impact when I/O is the bottleneck

---

## Performance Insights

### What Improved

* Broadcast join reduced shuffle in product join
* Column pruning reduced memory and I/O
* Persist avoided recomputation across multiple outputs

### What Did Not Improve Much

* Partitioning did not significantly help as queries scanned most data
* Persist introduced overhead when materialized eagerly (initial version)
* Write cost dominated total runtime

---

## Trade-offs

| Optimization    | Benefit                  | Trade-off                    |
| --------------- | ------------------------ | ---------------------------- |
| Broadcast Join  | Faster joins             | Only useful for small tables |
| Persisting      | Avoid recomputation      | Memory + initial overhead    |
| Partitioning    | Faster filtered reads    | No benefit without filters   |
| File Compaction | Better read performance  | Extra maintenance cost       |
| Z-ordering      | Faster selective queries | Not always supported         |

---

## Validation

All optimized outputs were validated against naive results:

* Row counts matched
* Aggregate totals matched

---

## Conclusion

This assessment demonstrates:

* Strong PySpark transformation capabilities
* Understanding of distributed processing
* Awareness of performance tuning techniques
* Ability to analyze real-world trade-offs

The results highlight that **Spark optimization is workload-dependent**, and improvements must be aligned with data size, query patterns, and storage behavior.

---

## How to Run

1. Open Fabric notebook:
   `nb_04_advanced_pyspark_transformations`

2. Execute all cells in order:

   * Data generation
   * Delta table creation
   * Naive transformations
   * Optimized transformations
   * Runtime comparison

3. Output tables will be created with prefix:
   `a2_`

---

## Output Tables

### Source Tables

* a2_fact_sales_20m
* a2_fact_returns_2m
* a2_dim_customer
* a2_dim_product

### Naive Outputs

* a2_daily_sales_by_region_naive
* a2_top_10_products_by_category_naive
* a2_customer_lifetime_value_naive
* a2_monthly_return_rate_naive

### Optimized Outputs

* a2_daily_sales_by_region_optimized
* a2_top_10_products_by_category_optimized
* a2_customer_lifetime_value_optimized
* a2_monthly_return_rate_optimized

### Comparison

* a2_runtime_comparison
