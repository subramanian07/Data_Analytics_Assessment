# Performance Notes

## Summary
The assessment compared a naive PySpark implementation against an optimized implementation on a synthetic retail dataset containing 20 million sales rows and 2 million returns rows.

Observed runtime:
- Naive: 28.68 seconds
- Optimized: 30.31 seconds

The optimized version was slightly slower overall, but this does not mean the tuning approach was incorrect. The benchmark showed that the workload was dominated by Delta table write time rather than transformation time.

---

## Optimization Techniques Applied

### 1. Column Pruning
Only required columns were selected from the source tables in the optimized flow. This reduces memory usage and unnecessary I/O.

### 2. Early Filtering
Null checks were applied early to reduce avoidable processing. In this dataset, the impact was limited because the synthetic data already had very few invalid rows.

### 3. Broadcast Join
The product dimension was broadcast in the optimized top-10-products transformation. This reduced shuffle cost for the dimension join.

### 4. Persisting
Reused DataFrames were persisted using `MEMORY_AND_DISK` to avoid repeated recomputation across multiple outputs.

### 5. Partitioning
A partitioned Delta version of the fact sales table was created using `order_year` and `order_month`.

### 6. File Compaction and Z-Ordering
Delta optimization steps were included for long-term storage efficiency and improved selective reads where supported.

---

## Why the Optimized Runtime Was Not Lower

### 1. Write-Dominated Workload
The largest portion of runtime came from writing Delta output tables. The write stage alone took about 26 seconds, which means total runtime was driven mainly by storage I/O rather than transformation complexity.

### 2. Similar Output Volume
Both naive and optimized flows wrote similar final datasets, so both incurred almost the same write cost.

### 3. Optimization Overhead
The optimized flow still has some orchestration overhead such as persistence management, broadcast planning, and partitioned-table handling. When transformation savings are modest, that overhead can offset the gains.

### 4. Limited Partition Pruning Benefit
Partitioning helps most when queries filter on partition columns. In this workload, most transformations scanned the dataset broadly, so partition pruning benefit was limited.

---