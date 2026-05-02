# A/B Report: `c07_triton_4379_response_cache`

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
repeated_identical_inputs,c07_triton_4379_response_cache_repeated_identical_inputs,value_numeric,25000.0
random_inputs_start,c07_triton_4379_response_cache_random_inputs_start,value_numeric,600.0
random_inputs_end,c07_triton_4379_response_cache_random_inputs_end,value_numeric,100.0
response_cache_size,c07_triton_4379_response_cache_response_cache_size,value_numeric,2000000000.0
```

## Baseline Prompt: Raw Input Only

```text
You are a fresh performance benchmark evaluator with zero prior context.

Analyze ONLY the public evidence below. Identify:
1. the performance issue,
2. the evidence,
3. the missing evidence,
4. the recommended next diagnostic step.

Do not invent root cause beyond the evidence.

CASE:
# c07 Triton #4379 response cache degradation

Source URL: https://github.com/triton-inference-server/server/issues/4379

Status: accepted as an explanatory/partially actionable case.

Raw performance evidence: confirmed. The issue body reports response-cache throughput above 25000 inference/s for repeated identical inputs, but degradation from 600 inference/s to 100 inference/s over time for randomly generated inputs.

Resolution evidence: confirmed. A Triton contributor acknowledged a known cache-insertion issue for unhashable inputs and later explained that random unique requests can cause cache management overhead and eviction. The same contributor stated there were no current plans to investigate further and recommended profiling with Nsight/NVTX if pursuing the degradation.

Normalized CSV: feasible with caveats. `normalized.csv` captures only the visible numeric claims; no timestamp sequence or full run table is visible in the issue text, and `25000++` is represented as a lower-bound text/numeric value rather than an exact measurement.

RAW EVIDENCE:
Public source read: https://github.com/triton-inference-server/server/issues/4379

Issue title:
Response cache is not working well

Visible performance evidence from issue body:
- With response cache enabled and repeatedly identical request input, inference/second can reach 25000++ at concurrency 3 using Performance Analyzer.
- With randomly generated input for each request, Triton server performance gets worse over time from 600 inference/second down to 100 inference/second.

Configuration details visible in issue:
- Triton v2.17.0, container 21.12.
- ONNX Runtime BERT model deployed on GPU.
- dynamic_batching enabled.
- response_cache enable: True.

Reporter comment:
- `--response-cache-byte-size` was set to 2G bytes.
- Reporter says random requests were used to measure response-cache overhead.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
Triton response cache performs very well for repeated identical inputs, but throughput degrades over time when requests use random unique inputs.

2. Evidence
- Identical repeated request input with response cache enabled reportedly reaches 25000++ inference/sec at concurrency 3.
- Randomly generated request input reportedly degrades from about 600 inference/sec to about 100 inference/sec over time.
- Configuration includes Triton v2.17.0/container 21.12, ONNX Runtime BERT on GPU, dynamic batching, response_cache enabled, and 2 GB cache size.
- Maintainer explanation identifies cache-management overhead and eviction as plausible for random unique requests, with a known cache-insertion issue for unhashable inputs also acknowledged.

3. Missing evidence
- No full time-series table, cache hit/miss/eviction counters, CPU profile, memory profile, or timestamped degradation curve.
- No controlled comparison with cache disabled under the same random-input workload.
- No Nsight/NVTX trace showing where overhead accumulates.

4. Recommended next diagnostic step
Run paired benchmarks with cache enabled versus disabled for the random-input workload while collecting cache metrics and an Nsight/NVTX profile to quantify insertion, lookup, eviction, and backend inference overhead.
```

## Trace-On Prompt: Raw Input Plus Change Trace

```text
You are a fresh performance benchmark evaluator with zero prior context.

Analyze ONLY the public evidence and precomputed deterministic trace below. Identify:
1. the performance issue,
2. the evidence,
3. the missing evidence,
4. the recommended next diagnostic step.

Use the trace as structured evidence. Do not treat it as root-cause proof.
Do not invent root cause beyond the evidence.

CASE:
# c07 Triton #4379 response cache degradation

Source URL: https://github.com/triton-inference-server/server/issues/4379

Status: accepted as an explanatory/partially actionable case.

Raw performance evidence: confirmed. The issue body reports response-cache throughput above 25000 inference/s for repeated identical inputs, but degradation from 600 inference/s to 100 inference/s over time for randomly generated inputs.

Resolution evidence: confirmed. A Triton contributor acknowledged a known cache-insertion issue for unhashable inputs and later explained that random unique requests can cause cache management overhead and eviction. The same contributor stated there were no current plans to investigate further and recommended profiling with Nsight/NVTX if pursuing the degradation.

Normalized CSV: feasible with caveats. `normalized.csv` captures only the visible numeric claims; no timestamp sequence or full run table is visible in the issue text, and `25000++` is represented as a lower-bound text/numeric value rather than an exact measurement.

RAW EVIDENCE:
Public source read: https://github.com/triton-inference-server/server/issues/4379

Issue title:
Response cache is not working well

Visible performance evidence from issue body:
- With response cache enabled and repeatedly identical request input, inference/second can reach 25000++ at concurrency 3 using Performance Analyzer.
- With randomly generated input for each request, Triton server performance gets worse over time from 600 inference/second down to 100 inference/second.

Configuration details visible in issue:
- Triton v2.17.0, container 21.12.
- ONNX Runtime BERT model deployed on GPU.
- dynamic_batching enabled.
- response_cache enable: True.

Reporter comment:
- `--response-cache-byte-size` was set to 2G bytes.
- Reporter says random requests were used to measure response-cache overhead.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 4 condition labels across 4 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] cache_cardinality_shift: c07_triton_4379_response_cache_response_cache_size.value_numeric at response_cache_size, confidence=0.8
      Evidence: cache workload contrasts repeated/hit-like inputs with random or unique inputs; preserve cache-cardinality and miss/eviction pressure before naming root cause
      mechanisms: cache_cardinality, repeated_inputs, random_or_unique_inputs

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c07_triton_4379_response_cache_response_cache_size.value_numeric shows a cache-cardinality workload shift; compare repeated-hit and high-cardinality miss/eviction behavior.
  Option C: repeated-input cache wins and unique-input degradation are different workloads.
  Option D: detector output is incomplete; request more metrics if evidence is thin.

GUARDRAIL:
  Do not turn timing into causality without dependency, deploy, or resource evidence.

Return concise structured findings.
```

## Trace-On Response

```text
1. Performance issue
Response-cache behavior differs sharply by request pattern: repeated identical inputs show very high throughput, while randomly generated inputs reportedly degrade over time from about 600 infer/s to about 100 infer/s.

2. Evidence
- The issue reports 25,000++ infer/s at concurrency 3 when identical inputs are repeatedly served from cache.
- With randomly generated inputs, the reporter observed throughput falling from 600 infer/s to 100 infer/s over time.
- Configuration evidence includes Triton v2.17.0/container 21.12, ONNX Runtime BERT on GPU, dynamic batching enabled, response cache enabled, and a 2 GB cache size.
- The trace found no strong computed change blocks and classifies the data as sparse benchmark conditions rather than a continuous time series.

3. Missing evidence
- Full timestamped throughput series for the random-input run.
- Cache hit/miss, insertion, eviction, memory usage, and lock/contention metrics.
- CPU/GPU utilization over time and request latency distribution.
- Comparable runs with cache disabled and with bounded unique-input cardinality.
- No trace evidence proving whether degradation is caused by cache insertion, eviction, hashing, batching interaction, or another factor.

4. Recommended next diagnostic step
Run a controlled A/B benchmark with cache disabled, cache enabled with repeated inputs, and cache enabled with controlled unique-input rates. Capture time-series throughput, cache hit/miss/eviction counters, CPU/GPU utilization, and an Nsight/NVTX profile during the degradation window.
```

## Verdict Review

```text
Winner: similar

Concise reason: Both outputs identify the same cache-cardinality contrast: repeated identical inputs perform extremely well, while random unique inputs degrade over time. Baseline gives a slightly stronger maintainer-cache-overhead explanation; trace-on adds useful caution that the sparse trace does not prove the mechanism.

Engine action: Keep current sparse-condition caution. Consider a cache workload detector for repeated-hit versus high-cardinality-miss/eviction patterns, but this case does not require a hard winner.
```
