# Benchmark 02: vllm_19954_ttft_explosion

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
before,c02_vllm_19954_ttft_explosion,traffic_request_rate,30.0
before,c02_vllm_19954_ttft_explosion,successful_requests,10000.0
before,c02_vllm_19954_ttft_explosion,benchmark_duration_s,451.28
before,c02_vllm_19954_ttft_explosion,request_throughput_req_s,22.16
before,c02_vllm_19954_ttft_explosion,output_token_throughput_tok_s,4457.76
before,c02_vllm_19954_ttft_explosion,total_token_throughput_tok_s,9344.38
before,c02_vllm_19954_ttft_explosion,mean_ttft_ms,987.38
before,c02_vllm_19954_ttft_explosion,median_ttft_ms,538.83
before,c02_vllm_19954_ttft_explosion,p99_ttft_ms,8046.79
before,c02_vllm_19954_ttft_explosion,mean_tpot_ms,262.05
before,c02_vllm_19954_ttft_explosion,median_tpot_ms,267.88
before,c02_vllm_19954_ttft_explosion,p99_tpot_ms,427.91
before,c02_vllm_19954_ttft_explosion,mean_itl_ms,245.41
before,c02_vllm_19954_ttft_explosion,median_itl_ms,220.48
before,c02_vllm_19954_ttft_explosion,p99_itl_ms,678.37
after,c02_vllm_19954_ttft_explosion,traffic_request_rate,30.0
after,c02_vllm_19954_ttft_explosion,successful_requests,10000.0
after,c02_vllm_19954_ttft_explosion,benchmark_duration_s,538.73
after,c02_vllm_19954_ttft_explosion,request_throughput_req_s,18.56
after,c02_vllm_19954_ttft_explosion,output_token_throughput_tok_s,3739.29
after,c02_vllm_19954_ttft_explosion,total_token_throughput_tok_s,7832.67
after,c02_vllm_19954_ttft_explosion,mean_ttft_ms,55239.91
after,c02_vllm_19954_ttft_explosion,median_ttft_ms,55251.84
after,c02_vllm_19954_ttft_explosion,p99_ttft_ms,124103.15
after,c02_vllm_19954_ttft_explosion,mean_tpot_ms,118.82
after,c02_vllm_19954_ttft_explosion,median_tpot_ms,120.96
after,c02_vllm_19954_ttft_explosion,p99_tpot_ms,138.4
after,c02_vllm_19954_ttft_explosion,mean_itl_ms,117.63
after,c02_vllm_19954_ttft_explosion,median_itl_ms,116.3
after,c02_vllm_19954_ttft_explosion,p99_itl_ms,185.65
followup_rate_15,c02_vllm_19954_ttft_explosion,traffic_request_rate,15.0
followup_rate_15,c02_vllm_19954_ttft_explosion,successful_requests,10000.0
followup_rate_15,c02_vllm_19954_ttft_explosion,benchmark_duration_s,732.51
followup_rate_15,c02_vllm_19954_ttft_explosion,request_throughput_req_s,13.65
followup_rate_15,c02_vllm_19954_ttft_explosion,output_token_throughput_tok_s,2745.98
followup_rate_15,c02_vllm_19954_ttft_explosion,total_token_throughput_tok_s,5756.47
followup_rate_15,c02_vllm_19954_ttft_explosion,mean_ttft_ms,151.45
followup_rate_15,c02_vllm_19954_ttft_explosion,median_ttft_ms,150.05
followup_rate_15,c02_vllm_19954_ttft_explosion,p99_ttft_ms,232.58
followup_rate_15,c02_vllm_19954_ttft_explosion,mean_tpot_ms,83.09
followup_rate_15,c02_vllm_19954_ttft_explosion,median_tpot_ms,82.86
followup_rate_15,c02_vllm_19954_ttft_explosion,p99_tpot_ms,92.83
followup_rate_15,c02_vllm_19954_ttft_explosion,mean_itl_ms,82.61
followup_rate_15,c02_vllm_19954_ttft_explosion,median_itl_ms,79.79
followup_rate_15,c02_vllm_19954_ttft_explosion,p99_itl_ms,121.49
followup_rate_20,c02_vllm_19954_ttft_explosion,traffic_request_rate,20.0
followup_rate_20,c02_vllm_19954_ttft_explosion,successful_requests,10000.0
followup_rate_20,c02_vllm_19954_ttft_explosion,benchmark_duration_s,574.73
followup_rate_20,c02_vllm_19954_ttft_explosion,request_throughput_req_s,17.4
followup_rate_20,c02_vllm_19954_ttft_explosion,output_token_throughput_tok_s,3501.61
followup_rate_20,c02_vllm_19954_ttft_explosion,total_token_throughput_tok_s,7338.59
followup_rate_20,c02_vllm_19954_ttft_explosion,mean_ttft_ms,202.64
followup_rate_20,c02_vllm_19954_ttft_explosion,median_ttft_ms,192.53
followup_rate_20,c02_vllm_19954_ttft_explosion,p99_ttft_ms,504.41
followup_rate_20,c02_vllm_19954_ttft_explosion,mean_tpot_ms,105.78
followup_rate_20,c02_vllm_19954_ttft_explosion,median_tpot_ms,107.33
followup_rate_20,c02_vllm_19954_ttft_explosion,p99_tpot_ms,134.2
followup_rate_20,c02_vllm_19954_ttft_explosion,mean_itl_ms,104.81
followup_rate_20,c02_vllm_19954_ttft_explosion,median_itl_ms,101.82
followup_rate_20,c02_vllm_19954_ttft_explosion,p99_itl_ms,167.8
followup_rate_25,c02_vllm_19954_ttft_explosion,traffic_request_rate,25.0
followup_rate_25,c02_vllm_19954_ttft_explosion,successful_requests,10000.0
followup_rate_25,c02_vllm_19954_ttft_explosion,benchmark_duration_s,545.22
followup_rate_25,c02_vllm_19954_ttft_explosion,request_throughput_req_s,18.34
followup_rate_25,c02_vllm_19954_ttft_explosion,output_token_throughput_tok_s,3690.11
followup_rate_25,c02_vllm_19954_ttft_explosion,total_token_throughput_tok_s,7734.74
followup_rate_25,c02_vllm_19954_ttft_explosion,mean_ttft_ms,26991.39
followup_rate_25,c02_vllm_19954_ttft_explosion,median_ttft_ms,27854.9
followup_rate_25,c02_vllm_19954_ttft_explosion,p99_ttft_ms,64714.36
followup_rate_25,c02_vllm_19954_ttft_explosion,mean_tpot_ms,117.66
followup_rate_25,c02_vllm_19954_ttft_explosion,median_tpot_ms,120.7
followup_rate_25,c02_vllm_19954_ttft_explosion,p99_tpot_ms,138.94
followup_rate_25,c02_vllm_19954_ttft_explosion,mean_itl_ms,116.59
followup_rate_25,c02_vllm_19954_ttft_explosion,median_itl_ms,115.69
followup_rate_25,c02_vllm_19954_ttft_explosion,p99_itl_ms,179.79
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
# c02 vLLM #19954 upgrade TTFT explosion

Source URL: https://github.com/vllm-project/vllm/issues/19954

Status: accepted.

Raw performance evidence: confirmed. The issue body includes `benchmark_serving.py` output for "Before" and "After" upgrading from 0.8.5 to 0.9.2, including request throughput and TTFT/TPOT/ITL metrics. A follow-up comment adds request-rate-specific runs at 15, 20, and 25 req/s.

Resolution evidence: confirmed. The issue was closed as completed by the reporter. The final reporter comment says the issue was resolved and identifies a 0.9.x A100 maximum-run limit as the cause.

Normalized CSV: feasible. `normalized.csv` extracts the visible benchmark summary values from the issue body and follow-up comment.

RAW EVIDENCE:
Public source read: https://github.com/vllm-project/vllm/issues/19954

Issue title:
[Performance]: Performance decrease after upgrading from 0.8.5 to 0.9.2

Evidence excerpt from issue body:

Before:
Successful requests: 10000
Benchmark duration (s): 451.28
Request throughput (req/s): 22.16
Output token throughput (tok/s): 4457.76
Total Token throughput (tok/s): 9344.38
Mean TTFT (ms): 987.38
Median TTFT (ms): 538.83
P99 TTFT (ms): 8046.79

After:
Successful requests: 10000
Benchmark duration (s): 538.73
Request throughput (req/s): 18.56
Output token throughput (tok/s): 3739.29
Total Token throughput (tok/s): 7832.67
Mean TTFT (ms): 55239.91
Median TTFT (ms): 55251.84
P99 TTFT (ms): 124103.15

Follow-up comment:
Traffic request rate 15 had mean TTFT 151.45 ms.
Traffic request rate 20 had mean TTFT 202.64 ms.
Traffic request rate 25 had mean TTFT 26991.39 ms.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
After upgrading vLLM from 0.8.5 to 0.9.2, serving throughput decreases and time-to-first-token becomes extremely high under the reported workload.

2. Evidence
The "Before" run on 0.8.5 reports 22.16 req/s, mean TTFT 987.38 ms, median TTFT 538.83 ms, and P99 TTFT 8046.79 ms. The "After" run on 0.9.2 reports 18.56 req/s, mean TTFT 55239.91 ms, median TTFT 55251.84 ms, and P99 TTFT 124103.15 ms. Follow-up request-rate tests show mean TTFT remains low at 15 req/s and 20 req/s, but rises sharply to 26991.39 ms at 25 req/s.

3. Missing evidence
The prompt does not provide full model/server configuration, hardware, concurrency settings, queue depth over time, GPU utilization, memory pressure, or repeated-run variance. The final reporter comment attributes the issue to a 0.9.x A100 maximum-run limit, but the public evidence here does not include the detailed measurements proving that causal path.

4. Recommended next diagnostic step
Run controlled load sweeps around the apparent saturation point, especially 20-25 req/s, on both 0.8.5 and 0.9.2 while collecting queue length, active/running request counts, GPU utilization, memory usage, and TTFT distributions.
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
# c02 vLLM #19954 upgrade TTFT explosion

Source URL: https://github.com/vllm-project/vllm/issues/19954

Status: accepted.

Raw performance evidence: confirmed. The issue body includes `benchmark_serving.py` output for "Before" and "After" upgrading from 0.8.5 to 0.9.2, including request throughput and TTFT/TPOT/ITL metrics. A follow-up comment adds request-rate-specific runs at 15, 20, and 25 req/s.

Resolution evidence: confirmed. The issue was closed as completed by the reporter. The final reporter comment says the issue was resolved and identifies a 0.9.x A100 maximum-run limit as the cause.

Normalized CSV: feasible. `normalized.csv` extracts the visible benchmark summary values from the issue body and follow-up comment.

RAW EVIDENCE:
Public source read: https://github.com/vllm-project/vllm/issues/19954

Issue title:
[Performance]: Performance decrease after upgrading from 0.8.5 to 0.9.2

Evidence excerpt from issue body:

Before:
Successful requests: 10000
Benchmark duration (s): 451.28
Request throughput (req/s): 22.16
Output token throughput (tok/s): 4457.76
Total Token throughput (tok/s): 9344.38
Mean TTFT (ms): 987.38
Median TTFT (ms): 538.83
P99 TTFT (ms): 8046.79

After:
Successful requests: 10000
Benchmark duration (s): 538.73
Request throughput (req/s): 18.56
Output token throughput (tok/s): 3739.29
Total Token throughput (tok/s): 7832.67
Mean TTFT (ms): 55239.91
Median TTFT (ms): 55251.84
P99 TTFT (ms): 124103.15

Follow-up comment:
Traffic request rate 15 had mean TTFT 151.45 ms.
Traffic request rate 20 had mean TTFT 202.64 ms.
Traffic request rate 25 had mean TTFT 26991.39 ms.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 5 condition labels across 75 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] condition_delta: c02_vllm_19954_ttft_explosion.mean_itl_ms at followup_rate_15 (82.61 -> 245.41), confidence=0.87
      Evidence: mean_itl_ms changes across benchmark conditions; min=82.61 at followup_rate_15; max=245.4 at before; ratio=2.97x; compare conditions before explaining cause
  [2] condition_delta: c02_vllm_19954_ttft_explosion.mean_tpot_ms at followup_rate_15 (83.09 -> 262.05), confidence=0.88
      Evidence: mean_tpot_ms changes across benchmark conditions; min=83.09 at followup_rate_15; max=262.1 at before; ratio=3.15x; compare conditions before explaining cause
  [3] condition_delta: c02_vllm_19954_ttft_explosion.mean_ttft_ms at followup_rate_15 (151.45 -> 55239.91), confidence=0.95
      Evidence: mean_ttft_ms changes across benchmark conditions; min=151.4 at followup_rate_15; max=5.524e+04 at after; ratio=364.74x; compare conditions before explaining cause
  [4] condition_delta: c02_vllm_19954_ttft_explosion.median_tpot_ms at followup_rate_15 (82.86 -> 267.88), confidence=0.88
      Evidence: median_tpot_ms changes across benchmark conditions; min=82.86 at followup_rate_15; max=267.9 at before; ratio=3.23x; compare conditions before explaining cause
  [5] condition_delta: c02_vllm_19954_ttft_explosion.median_ttft_ms at followup_rate_15 (150.05 -> 55251.84), confidence=0.95
      Evidence: median_ttft_ms changes across benchmark conditions; min=150.1 at followup_rate_15; max=5.525e+04 at after; ratio=368.22x; compare conditions before explaining cause
  [6] condition_delta: c02_vllm_19954_ttft_explosion.p99_itl_ms at followup_rate_15 (121.49 -> 678.37), confidence=0.95
      Evidence: p99_itl_ms changes across benchmark conditions; min=121.5 at followup_rate_15; max=678.4 at before; ratio=5.58x; compare conditions before explaining cause
  [7] condition_delta: c02_vllm_19954_ttft_explosion.p99_tpot_ms at followup_rate_15 (92.83 -> 427.91), confidence=0.94
      Evidence: p99_tpot_ms changes across benchmark conditions; min=92.83 at followup_rate_15; max=427.9 at before; ratio=4.61x; compare conditions before explaining cause
  [8] condition_delta: c02_vllm_19954_ttft_explosion.p99_ttft_ms at followup_rate_15 (232.58 -> 124103.15), confidence=0.95
      Evidence: p99_ttft_ms changes across benchmark conditions; min=232.6 at followup_rate_15; max=1.241e+05 at after; ratio=533.59x; compare conditions before explaining cause

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c02_vllm_19954_ttft_explosion.mean_itl_ms differs across benchmark conditions; compare conditions before explaining cause.
  Option C: this is sparse benchmark evidence; preserve condition labels and deltas.
  Option D: detector output is incomplete; request more metrics if evidence is thin.

GUARDRAIL:
  Do not turn timing into causality without dependency, deploy, or resource evidence.

Return concise structured findings.
```

## Trace-On Response

```text
1. Performance issue
- After upgrading vLLM from 0.8.5 to 0.9.2, the benchmark shows a large TTFT regression and lower throughput. The trace points to a condition-dependent TTFT explosion, especially under the original after-upgrade benchmark condition.

2. Evidence
- Before upgrade: 22.16 req/s, mean TTFT 987.38 ms, median TTFT 538.83 ms, p99 TTFT 8046.79 ms.
- After upgrade: 18.56 req/s, mean TTFT 55239.91 ms, median TTFT 55251.84 ms, p99 TTFT 124103.15 ms.
- Follow-up request-rate runs show mean TTFT of 151.45 ms at 15 req/s, 202.64 ms at 20 req/s, and 26991.39 ms at 25 req/s, indicating a sharp threshold between 20 and 25 req/s.
- The deterministic trace flags mean TTFT changing from 151.45 ms to 55239.91 ms across conditions, and p99 TTFT from 232.58 ms to 124103.15 ms. These are strong condition deltas, not root-cause proof.

3. Missing evidence
- The trace does not include queue depth over time, admission/scheduler state, GPU utilization, KV-cache pressure, memory headroom, request length distribution, or server configuration diffs beyond the version change.
- It does not prove why 25 req/s crosses the latency threshold.
- The final reported cause is mentioned, but the trace does not include the direct diagnostic artifacts that establish it.

4. Recommended next diagnostic step
- Perform a controlled request-rate sweep from 20 to 25 req/s in small increments on the upgraded version, collecting queue depth, TTFT breakdown, scheduler/admission metrics, GPU and memory utilization, and any configured maximum-run or concurrency limits.
```

## Verdict Review

```text
Winner: trace-on

Reason:
Baseline is correct. Trace-on is better because it quantifies the condition deltas and makes the 20 -> 25 req/s threshold easier to see. It keeps TTFT explosion as evidence, not root-cause proof.

Engine action:
No further patch needed.
```
