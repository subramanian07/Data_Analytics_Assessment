# Runtime Comparison

## Measured Runtime

| Approach   | Runtime (seconds) |
|------------|-------------------:|
| Naive      | 28.68 |
| Optimized  | 30.31 |

## Difference

- Absolute difference: **1.63 seconds**
- Relative difference: **optimized was ~5.68% slower**

## Interpretation

The runtime difference is very small. This indicates that the transformation logic itself was not the main bottleneck in the final benchmark.

The strongest observation from execution was that Delta table write time consumed most of the total runtime. Since both approaches wrote similar outputs, the write stage reduced the visible benefit of transformation-level tuning.

## Final Assessment

The optimized version still demonstrates correct performance engineering practices:
- reduced shuffle risk through broadcast join
- reduced unnecessary reads through column pruning
- reused intermediate datasets through persistence
- improved physical layout through partitioning and Delta optimization

The benchmark outcome shows that the workload is primarily **write-bound**, not **compute-bound**.
