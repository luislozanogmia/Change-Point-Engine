# A/B Report: `c01_vllm_7592_scheduler_regression`

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
max_num_seqs_1024,c01_vllm_7592_scheduler_regression_0_5_4_true,requests_per_second,3.1797
max_num_seqs_1024,c01_vllm_7592_scheduler_regression_0_5_4_true,delay_ms,39.72
max_num_seqs_1024,c01_vllm_7592_scheduler_regression_0_5_3_true,requests_per_second,3.1341
max_num_seqs_1024,c01_vllm_7592_scheduler_regression_0_5_3_true,delay_ms,40.15
max_num_seqs_1024,c01_vllm_7592_scheduler_regression_0_5_2_true,requests_per_second,3.1696
max_num_seqs_1024,c01_vllm_7592_scheduler_regression_0_5_2_true,delay_ms,39.67
max_num_seqs_1024,c01_vllm_7592_scheduler_regression_0_5_1_true,requests_per_second,3.1745
max_num_seqs_1024,c01_vllm_7592_scheduler_regression_0_5_1_true,delay_ms,39.61
max_num_seqs_768,c01_vllm_7592_scheduler_regression_0_5_4_true,requests_per_second,4.1047
max_num_seqs_768,c01_vllm_7592_scheduler_regression_0_5_4_true,delay_ms,43.4
max_num_seqs_768,c01_vllm_7592_scheduler_regression_0_5_3_true,requests_per_second,3.9708
max_num_seqs_768,c01_vllm_7592_scheduler_regression_0_5_3_true,delay_ms,44.42
max_num_seqs_768,c01_vllm_7592_scheduler_regression_0_5_2_true,requests_per_second,4.0413
max_num_seqs_768,c01_vllm_7592_scheduler_regression_0_5_2_true,delay_ms,43.6
max_num_seqs_768,c01_vllm_7592_scheduler_regression_0_5_1_true,requests_per_second,4.0439
max_num_seqs_768,c01_vllm_7592_scheduler_regression_0_5_1_true,delay_ms,43.57
max_num_seqs_512,c01_vllm_7592_scheduler_regression_0_5_4_true,requests_per_second,4.6486
max_num_seqs_512,c01_vllm_7592_scheduler_regression_0_5_4_true,delay_ms,46.79
max_num_seqs_512,c01_vllm_7592_scheduler_regression_0_5_3_true,requests_per_second,4.6377
max_num_seqs_512,c01_vllm_7592_scheduler_regression_0_5_3_true,delay_ms,46.25
max_num_seqs_512,c01_vllm_7592_scheduler_regression_0_5_2_true,requests_per_second,4.7419
max_num_seqs_512,c01_vllm_7592_scheduler_regression_0_5_2_true,delay_ms,45.15
max_num_seqs_512,c01_vllm_7592_scheduler_regression_0_5_1_true,requests_per_second,4.747
max_num_seqs_512,c01_vllm_7592_scheduler_regression_0_5_1_true,delay_ms,45.13
max_num_seqs_384,c01_vllm_7592_scheduler_regression_0_5_4_true,requests_per_second,4.798
max_num_seqs_384,c01_vllm_7592_scheduler_regression_0_5_4_true,delay_ms,49.66
max_num_seqs_384,c01_vllm_7592_scheduler_regression_0_5_3_true,requests_per_second,4.8605
max_num_seqs_384,c01_vllm_7592_scheduler_regression_0_5_3_true,delay_ms,45.93
max_num_seqs_384,c01_vllm_7592_scheduler_regression_0_5_2_true,requests_per_second,4.9834
max_num_seqs_384,c01_vllm_7592_scheduler_regression_0_5_2_true,delay_ms,44.72
max_num_seqs_384,c01_vllm_7592_scheduler_regression_0_5_1_true,requests_per_second,5.0019
max_num_seqs_384,c01_vllm_7592_scheduler_regression_0_5_1_true,delay_ms,44.61
max_num_seqs_256,c01_vllm_7592_scheduler_regression_0_5_4_true,requests_per_second,4.9096
max_num_seqs_256,c01_vllm_7592_scheduler_regression_0_5_4_true,delay_ms,48.27
max_num_seqs_256,c01_vllm_7592_scheduler_regression_0_5_3_true,requests_per_second,5.4424
max_num_seqs_256,c01_vllm_7592_scheduler_regression_0_5_3_true,delay_ms,42.23
max_num_seqs_256,c01_vllm_7592_scheduler_regression_0_5_2_true,requests_per_second,5.5876
max_num_seqs_256,c01_vllm_7592_scheduler_regression_0_5_2_true,delay_ms,41.1
max_num_seqs_256,c01_vllm_7592_scheduler_regression_0_5_1_true,requests_per_second,5.5949
max_num_seqs_256,c01_vllm_7592_scheduler_regression_0_5_1_true,delay_ms,41.04
max_num_seqs_128,c01_vllm_7592_scheduler_regression_0_5_4_true,requests_per_second,4.2047
max_num_seqs_128,c01_vllm_7592_scheduler_regression_0_5_4_true,delay_ms,32.77
max_num_seqs_128,c01_vllm_7592_scheduler_regression_0_5_3_true,requests_per_second,4.0718
max_num_seqs_128,c01_vllm_7592_scheduler_regression_0_5_3_true,delay_ms,29.7
max_num_seqs_128,c01_vllm_7592_scheduler_regression_0_5_2_true,requests_per_second,4.1528
max_num_seqs_128,c01_vllm_7592_scheduler_regression_0_5_2_true,delay_ms,29.11
max_num_seqs_128,c01_vllm_7592_scheduler_regression_0_5_1_true,requests_per_second,4.1544
max_num_seqs_128,c01_vllm_7592_scheduler_regression_0_5_1_true,delay_ms,29.1
max_num_seqs_64,c01_vllm_7592_scheduler_regression_0_5_4_true,requests_per_second,2.435
max_num_seqs_64,c01_vllm_7592_scheduler_regression_0_5_4_true,delay_ms,26.88
max_num_seqs_64,c01_vllm_7592_scheduler_regression_0_5_3_true,requests_per_second,2.3879
max_num_seqs_64,c01_vllm_7592_scheduler_regression_0_5_3_true,delay_ms,25.74
max_num_seqs_64,c01_vllm_7592_scheduler_regression_0_5_2_true,requests_per_second,2.4141
max_num_seqs_64,c01_vllm_7592_scheduler_regression_0_5_2_true,delay_ms,25.45
max_num_seqs_64,c01_vllm_7592_scheduler_regression_0_5_1_true,requests_per_second,2.4175
max_num_seqs_64,c01_vllm_7592_scheduler_regression_0_5_1_true,delay_ms,25.41
max_num_seqs_32,c01_vllm_7592_scheduler_regression_0_5_4_true,requests_per_second,1.6103
max_num_seqs_32,c01_vllm_7592_scheduler_regression_0_5_4_true,delay_ms,19.83
max_num_seqs_32,c01_vllm_7592_scheduler_regression_0_5_3_true,requests_per_second,1.5846
max_num_seqs_32,c01_vllm_7592_scheduler_regression_0_5_3_true,delay_ms,19.55
max_num_seqs_32,c01_vllm_7592_scheduler_regression_0_5_2_true,requests_per_second,1.593
max_num_seqs_32,c01_vllm_7592_scheduler_regression_0_5_2_true,delay_ms,19.44
max_num_seqs_32,c01_vllm_7592_scheduler_regression_0_5_1_true,requests_per_second,1.5942
max_num_seqs_32,c01_vllm_7592_scheduler_regression_0_5_1_true,delay_ms,19.43
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
# c01 vLLM #7592 scheduler regression

Source URL: https://github.com/vllm-project/vllm/issues/7592

Status: accepted.

Raw performance evidence: confirmed. The issue body includes a version comparison table for `max_num_seqs` with request throughput and delay for vLLM 0.5.1 through 0.5.4, both with `enable_chunked_prefill` disabled and enabled.

Resolution evidence: confirmed. The issue was closed as completed. PR https://github.com/vllm-project/vllm/pull/7874 is titled as a bugfix for #7592, says `FIX #7592`, describes scheduler queue sorting as the fix, and was merged on 2024-09-02.

Normalized CSV: feasible. `normalized.csv` extracts the visible table rows from the issue body for the enabled chunked-prefill request/s and delay metrics.

RAW EVIDENCE:
Public source read: https://github.com/vllm-project/vllm/issues/7592

Issue title:
[Performance]: vllm 0.5.4 with enable_chunked_prefill =True, throughput is slightly lower than 0.5.3~0.5.0.

Evidence excerpt from issue body:

vLLM 0.5.4 with enable_chunked_prefill=True, throughput is slightly lower than 0.5.3~0.5.1.

Visible table values for enable_chunked_prefill=True:

max_num_seqs | v0.5.4 req/s | v0.5.4 delay ms | v0.5.3 req/s | v0.5.3 delay ms | v0.5.2 req/s | v0.5.2 delay ms | v0.5.1 req/s | v0.5.1 delay ms
1024 | 3.1797 | 39.72 | 3.1341 | 40.15 | 3.1696 | 39.67 | 3.1745 | 39.61
768 | 4.1047 | 43.4 | 3.9708 | 44.42 | 4.0413 | 43.6 | 4.0439 | 43.57
512 | 4.6486 | 46.79 | 4.6377 | 46.25 | 4.7419 | 45.15 | 4.747 | 45.13
384 | 4.798 | 49.66 | 4.8605 | 45.93 | 4.9834 | 44.72 | 5.0019 | 44.61
256 | 4.9096 | 48.27 | 5.4424 | 42.23 | 5.5876 | 41.1 | 5.5949 | 41.04
128 | 4.2047 | 32.77 | 4.0718 | 29.7 | 4.1528 | 29.11 | 4.1544 | 29.1
64 | 2.435 | 26.88 | 2.3879 | 25.74 | 2.4141 | 25.45 | 2.4175 | 25.41
32 | 1.6103 | 19.83 | 1.5846 | 19.55 | 1.593 | 19.44 | 1.5942 | 19.43

Additional comments:
- Reporter said reverting PR #6867 made the bug disappear.
- Reporter said the PR caused chunked prefill peak throughput to drop by 15%.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
vLLM 0.5.4 shows a chunked-prefill performance regression versus prior 0.5.x releases, most visibly at mid-range `max_num_seqs`.

2. Evidence
With `enable_chunked_prefill=True`, `max_num_seqs=256` drops from about 5.59 req/s in 0.5.1-0.5.2 and 5.44 req/s in 0.5.3 to 4.91 req/s in 0.5.4, while delay increases from about 41-42 ms to 48.27 ms. At `max_num_seqs=384`, throughput also falls from 5.00 req/s in 0.5.1 to 4.80 req/s in 0.5.4, with delay rising from 44.61 ms to 49.66 ms. The reporter also stated that reverting PR #6867 made the issue disappear and estimated a 15% chunked-prefill peak-throughput drop. A merged PR, #7874, explicitly fixed #7592 by changing scheduler queue sorting.

3. Missing evidence
The prompt does not include full benchmark configuration, hardware details, statistical variance, repeated trial counts, or direct profiler data. The exact mechanism by which scheduler queue sorting affected throughput is not proven from the public evidence alone.

4. Recommended next diagnostic step
Reproduce the benchmark across v0.5.3, v0.5.4, the PR #6867 revert, and the #7874 fix using identical hardware and request traces, then collect scheduler queue ordering metrics and latency/throughput distributions for the affected `max_num_seqs` range.
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
# c01 vLLM #7592 scheduler regression

Source URL: https://github.com/vllm-project/vllm/issues/7592

Status: accepted.

Raw performance evidence: confirmed. The issue body includes a version comparison table for `max_num_seqs` with request throughput and delay for vLLM 0.5.1 through 0.5.4, both with `enable_chunked_prefill` disabled and enabled.

Resolution evidence: confirmed. The issue was closed as completed. PR https://github.com/vllm-project/vllm/pull/7874 is titled as a bugfix for #7592, says `FIX #7592`, describes scheduler queue sorting as the fix, and was merged on 2024-09-02.

Normalized CSV: feasible. `normalized.csv` extracts the visible table rows from the issue body for the enabled chunked-prefill request/s and delay metrics.

RAW EVIDENCE:
Public source read: https://github.com/vllm-project/vllm/issues/7592

Issue title:
[Performance]: vllm 0.5.4 with enable_chunked_prefill =True, throughput is slightly lower than 0.5.3~0.5.0.

Evidence excerpt from issue body:

vLLM 0.5.4 with enable_chunked_prefill=True, throughput is slightly lower than 0.5.3~0.5.1.

Visible table values for enable_chunked_prefill=True:

max_num_seqs | v0.5.4 req/s | v0.5.4 delay ms | v0.5.3 req/s | v0.5.3 delay ms | v0.5.2 req/s | v0.5.2 delay ms | v0.5.1 req/s | v0.5.1 delay ms
1024 | 3.1797 | 39.72 | 3.1341 | 40.15 | 3.1696 | 39.67 | 3.1745 | 39.61
768 | 4.1047 | 43.4 | 3.9708 | 44.42 | 4.0413 | 43.6 | 4.0439 | 43.57
512 | 4.6486 | 46.79 | 4.6377 | 46.25 | 4.7419 | 45.15 | 4.747 | 45.13
384 | 4.798 | 49.66 | 4.8605 | 45.93 | 4.9834 | 44.72 | 5.0019 | 44.61
256 | 4.9096 | 48.27 | 5.4424 | 42.23 | 5.5876 | 41.1 | 5.5949 | 41.04
128 | 4.2047 | 32.77 | 4.0718 | 29.7 | 4.1528 | 29.11 | 4.1544 | 29.1
64 | 2.435 | 26.88 | 2.3879 | 25.74 | 2.4141 | 25.45 | 2.4175 | 25.41
32 | 1.6103 | 19.83 | 1.5846 | 19.55 | 1.593 | 19.44 | 1.5942 | 19.43

Additional comments:
- Reporter said reverting PR #6867 made the bug disappear.
- Reporter said the PR caused chunked prefill peak throughput to drop by 15%.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: load_parameter_sweep
  Selected detectors: load_scaling_saturation, tail_amplification_under_load, mean_median_divergence
  Evidence: 64/64 rows use load-parameter labels; treat rows as parameter sweep points

SIGNAL BLOCKS:
  [1] parameter_sweep_cliff: c01_vllm_7592_scheduler_regression_0_5_4_true.requests_per_second at max_num_seqs_32 (4.9096 -> 1.6103), confidence=0.8
      Evidence: requests_per_second varies 3.0x across the sweep; best condition=max_num_seqs_256 value=4.91; worst condition=max_num_seqs_32 value=1.61; this is a parameter-sensitive performance cliff, not incident time

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c01_vllm_7592_scheduler_regression_0_5_4_true.requests_per_second changes sharply across parameter settings; inspect the best/worst condition boundary.
  Option C: parameter sensitivity is present; do not flatten the sweep into one average.
  Option D: detector output is incomplete; request more metrics if evidence is thin.

GUARDRAIL:
  Do not turn timing into causality without dependency, deploy, or resource evidence.

Return concise structured findings.
```

## Trace-On Response

```text
1. Performance issue
- vLLM 0.5.4 with `enable_chunked_prefill=True` shows a parameter-sensitive throughput regression, especially around smaller `max_num_seqs` values. The trace indicates this should be treated as a sweep cliff, not a single averaged slowdown.

2. Evidence
- Public issue data compares vLLM 0.5.1 through 0.5.4 across `max_num_seqs` settings with request/s and delay.
- At `max_num_seqs=256`, v0.5.4 reaches 4.9096 req/s versus 5.4424-5.5949 req/s for v0.5.3-v0.5.1, with delay rising to 48.27 ms versus about 41-42 ms.
- At `max_num_seqs=384`, v0.5.4 is 4.798 req/s versus 4.8605-5.0019 req/s for prior versions, with delay rising to 49.66 ms versus about 44.6-45.9 ms.
- The deterministic trace flags a 3.0x sweep variation in v0.5.4 true chunked-prefill throughput, with best at `max_num_seqs=256` and worst at `max_num_seqs=32`.
- Reporter comments say reverting PR #6867 made the issue disappear and estimated a 15% peak-throughput drop, but that is supporting evidence, not proof of cause.

3. Missing evidence
- No scheduler-level timings, queue ordering logs, GPU utilization, prefill/decode split, or per-request latency distribution are provided.
- No controlled A/B run isolating only the suspected scheduler change is shown in the trace.
- The table does not establish whether the issue is from scheduling, resource saturation, workload shape, or another version difference.

4. Recommended next diagnostic step
- Re-run the benchmark around the cliff boundaries, especially `max_num_seqs=256`, `384`, and neighboring values, with scheduler queue metrics, prefill/decode phase timings, GPU utilization, and per-request latency histograms for v0.5.3, v0.5.4, and a revert/test build of the suspected scheduler change.
```

## Verdict Review

```text
Winner: trace-on

Reason:
Baseline correctly identifies the vLLM 0.5.4 chunked-prefill regression. Trace-on adds the useful structure: `load_parameter_sweep` and `parameter_sweep_cliff`, making clear this is not incident time and that the best/worst `max_num_seqs` boundary matters.

Engine action:
No further patch needed.
```
