# Performance and resource decisions

Load this reference only when latency, throughput, CPU, memory, I/O, network, storage, scale, or “optimization” is material.

Before changing code, identify the target and representative workload, record a baseline, locate the bottleneck, and define correctness equivalence plus the response criterion. Reject optimizations inferred only from code shape or microbenchmarks unrelated to the end-to-end path.

Measure the resource that matters before and after under comparable conditions. Include warm-up, variance, concurrency, input distribution, caching, external-service behavior, and platform constraints when they can alter the result. Record trade-offs: a latency win may increase memory, network chatter, tail behavior, operational burden, or UX regressions.

At scale, combine per-operation frequency with population/exposure and recovery cost. A rare failure can dominate expected harm; an O(n²) path can be irrelevant at 100 items and critical at 1M.

Claim only what the data supports: “12% lower median latency in fixture X” is not “faster in production.” Preserve the benchmark/profile command and result needed to reproduce the conclusion.
