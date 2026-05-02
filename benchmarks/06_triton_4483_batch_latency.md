# Benchmark 06: triton_4483_batch_latency

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
batch_1,c06_triton_4483_batch_latency,throughput_infer_s,75.9241
batch_1,c06_triton_4483_batch_latency,client_avg_latency_usec,13137.0
batch_1,c06_triton_4483_batch_latency,server_avg_request_latency_usec,10140.0
batch_1,c06_triton_4483_batch_latency,compute_input_usec,183.0
batch_1,c06_triton_4483_batch_latency,compute_infer_usec,9827.0
batch_1,c06_triton_4483_batch_latency,compute_output_usec,12.0
batch_2,c06_triton_4483_batch_latency,throughput_infer_s,103.896
batch_2,c06_triton_4483_batch_latency,client_avg_latency_usec,19165.0
batch_2,c06_triton_4483_batch_latency,server_avg_request_latency_usec,12955.0
batch_2,c06_triton_4483_batch_latency,compute_input_usec,303.0
batch_2,c06_triton_4483_batch_latency,compute_infer_usec,12522.0
batch_2,c06_triton_4483_batch_latency,compute_output_usec,10.0
batch_4,c06_triton_4483_batch_latency,throughput_infer_s,124.0
batch_4,c06_triton_4483_batch_latency,client_avg_latency_usec,32096.0
batch_4,c06_triton_4483_batch_latency,server_avg_request_latency_usec,19304.0
batch_4,c06_triton_4483_batch_latency,compute_input_usec,573.0
batch_4,c06_triton_4483_batch_latency,compute_infer_usec,18606.0
batch_4,c06_triton_4483_batch_latency,compute_output_usec,10.0
batch_8,c06_triton_4483_batch_latency,throughput_infer_s,136.0
batch_8,c06_triton_4483_batch_latency,client_avg_latency_usec,57567.0
batch_8,c06_triton_4483_batch_latency,server_avg_request_latency_usec,32837.0
batch_8,c06_triton_4483_batch_latency,compute_input_usec,1584.0
batch_8,c06_triton_4483_batch_latency,compute_infer_usec,31054.0
batch_8,c06_triton_4483_batch_latency,compute_output_usec,22.0
batch_16,c06_triton_4483_batch_latency,throughput_infer_s,144.0
batch_16,c06_triton_4483_batch_latency,client_avg_latency_usec,109309.0
batch_16,c06_triton_4483_batch_latency,server_avg_request_latency_usec,59491.0
batch_16,c06_triton_4483_batch_latency,compute_input_usec,3309.0
batch_16,c06_triton_4483_batch_latency,compute_infer_usec,55956.0
batch_16,c06_triton_4483_batch_latency,compute_output_usec,27.0
batch_32,c06_triton_4483_batch_latency,throughput_infer_s,138.62
batch_32,c06_triton_4483_batch_latency,client_avg_latency_usec,222231.0
batch_32,c06_triton_4483_batch_latency,server_avg_request_latency_usec,115993.0
batch_32,c06_triton_4483_batch_latency,compute_input_usec,6783.0
batch_32,c06_triton_4483_batch_latency,compute_infer_usec,108889.0
batch_32,c06_triton_4483_batch_latency,compute_output_usec,43.0
batch_64,c06_triton_4483_batch_latency,throughput_infer_s,140.772
batch_64,c06_triton_4483_batch_latency,client_avg_latency_usec,433568.0
batch_64,c06_triton_4483_batch_latency,server_avg_request_latency_usec,265554.0
batch_64,c06_triton_4483_batch_latency,compute_input_usec,48010.0
batch_64,c06_triton_4483_batch_latency,compute_infer_usec,217111.0
batch_64,c06_triton_4483_batch_latency,compute_output_usec,77.0
batch_128,c06_triton_4483_batch_latency,throughput_infer_s,127.986
batch_128,c06_triton_4483_batch_latency,client_avg_latency_usec,915560.0
batch_128,c06_triton_4483_batch_latency,server_avg_request_latency_usec,521936.0
batch_128,c06_triton_4483_batch_latency,compute_input_usec,95572.0
batch_128,c06_triton_4483_batch_latency,compute_infer_usec,425814.0
batch_128,c06_triton_4483_batch_latency,compute_output_usec,139.0
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
# c06 Triton #4483 batch-size latency behavior

Source URL: https://github.com/triton-inference-server/server/issues/4483

Status: accepted as an explanatory/non-bug case.

Raw performance evidence: confirmed. The issue body includes `perf_analyzer` results for batch sizes 1 through 128, including throughput, average latency, and server compute-infer time.

Resolution evidence: confirmed. A Triton contributor explained that larger batches require more data movement and work, that `max_batch_size=128` is a user-provided maximum rather than a constant-time promise, and the reporter later accepted that Triton was working as expected.

Normalized CSV: feasible. `normalized.csv` extracts the issue-body batch-size rows.

RAW EVIDENCE:
Public source read: https://github.com/triton-inference-server/server/issues/4483

Issue title:
Compute infer time increases linearly with batch size even with batching

Visible perf_analyzer issue-body rows:
Batch 1: throughput 75.9241 infer/sec, client avg latency 13137 usec, server compute infer 9827 usec.
Batch 2: throughput 103.896 infer/sec, client avg latency 19165 usec, server compute infer 12522 usec.
Batch 4: throughput 124 infer/sec, client avg latency 32096 usec, server compute infer 18606 usec.
Batch 8: throughput 136 infer/sec, client avg latency 57567 usec, server compute infer 31054 usec.
Batch 16: throughput 144 infer/sec, client avg latency 109309 usec, server compute infer 55956 usec.
Batch 32: throughput 138.62 infer/sec, client avg latency 222231 usec, server compute infer 108889 usec.
Batch 64: throughput 140.772 infer/sec, client avg latency 433568 usec, server compute infer 217111 usec.
Batch 128: throughput 127.986 infer/sec, client avg latency 915560 usec, server compute infer 425814 usec.

Follow-up with CUDA shared memory also showed increasing compute infer time:
Batch 1 compute infer 8897 usec.
Batch 128 compute infer 407990 usec.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
Server compute-infer latency rises roughly linearly as requested batch size increases, while throughput plateaus around 128-144 infer/sec and then drops at batch 128.

2. Evidence
- Batch 1: 9,827 usec server compute infer; 13,137 usec client avg latency; 75.9241 infer/sec.
- Batch 16: 55,956 usec server compute infer; 109,309 usec client avg latency; 144 infer/sec.
- Batch 128: 425,814 usec server compute infer; 915,560 usec client avg latency; 127.986 infer/sec.
- CUDA shared memory follow-up still shows compute infer rising from 8,897 usec at batch 1 to 407,990 usec at batch 128.
- Public resolution says this is expected: larger batches require more data movement/work, and `max_batch_size=128` is only a configured maximum.

3. Missing evidence
- No GPU kernel-level profile, memory bandwidth data, model architecture details, or per-request queueing/batching breakdown beyond the reported perf_analyzer rows.
- No comparison against an optimized model/runtime target proving the observed slope is abnormal.

4. Recommended next diagnostic step
If further investigation is needed, profile GPU execution and data movement across batch sizes with Nsight or equivalent tooling, then compare compute, transfer, and batching overhead rather than assuming max batch size implies constant latency.
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
# c06 Triton #4483 batch-size latency behavior

Source URL: https://github.com/triton-inference-server/server/issues/4483

Status: accepted as an explanatory/non-bug case.

Raw performance evidence: confirmed. The issue body includes `perf_analyzer` results for batch sizes 1 through 128, including throughput, average latency, and server compute-infer time.

Resolution evidence: confirmed. A Triton contributor explained that larger batches require more data movement and work, that `max_batch_size=128` is a user-provided maximum rather than a constant-time promise, and the reporter later accepted that Triton was working as expected.

Normalized CSV: feasible. `normalized.csv` extracts the issue-body batch-size rows.

RAW EVIDENCE:
Public source read: https://github.com/triton-inference-server/server/issues/4483

Issue title:
Compute infer time increases linearly with batch size even with batching

Visible perf_analyzer issue-body rows:
Batch 1: throughput 75.9241 infer/sec, client avg latency 13137 usec, server compute infer 9827 usec.
Batch 2: throughput 103.896 infer/sec, client avg latency 19165 usec, server compute infer 12522 usec.
Batch 4: throughput 124 infer/sec, client avg latency 32096 usec, server compute infer 18606 usec.
Batch 8: throughput 136 infer/sec, client avg latency 57567 usec, server compute infer 31054 usec.
Batch 16: throughput 144 infer/sec, client avg latency 109309 usec, server compute infer 55956 usec.
Batch 32: throughput 138.62 infer/sec, client avg latency 222231 usec, server compute infer 108889 usec.
Batch 64: throughput 140.772 infer/sec, client avg latency 433568 usec, server compute infer 217111 usec.
Batch 128: throughput 127.986 infer/sec, client avg latency 915560 usec, server compute infer 425814 usec.

Follow-up with CUDA shared memory also showed increasing compute infer time:
Batch 1 compute infer 8897 usec.
Batch 128 compute infer 407990 usec.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: load_parameter_sweep
  Selected detectors: load_scaling_saturation, tail_amplification_under_load, mean_median_divergence
  Evidence: 48/48 rows use load-parameter labels; treat rows as parameter sweep points

SIGNAL BLOCKS:
  [1] batch_work_scaling: c06_triton_4483_batch_latency.client_avg_latency_usec at batch_128 (13137.0 -> 915560.0), confidence=0.9
      Evidence: batch parameter increased 128.0x while client_avg_latency_usec increased 69.7x; throughput metric throughput_infer_s: first=75.92, peak=144, last=128; treat as per-request work/payload scaling before calling it queue saturation
  [2] batch_work_scaling: c06_triton_4483_batch_latency.server_avg_request_latency_usec at batch_128 (10140.0 -> 521936.0), confidence=0.8
      Evidence: batch parameter increased 128.0x while server_avg_request_latency_usec increased 51.5x; throughput metric throughput_infer_s: first=75.92, peak=144, last=128; treat as per-request work/payload scaling before calling it queue saturation
  [3] parameter_sweep_cliff: c06_triton_4483_batch_latency.throughput_infer_s at batch_1 (144.0 -> 75.9241), confidence=0.61
      Evidence: throughput_infer_s varies 1.9x across the sweep; best condition=batch_16 value=144; worst condition=batch_1 value=75.92; this is a parameter-sensitive performance cliff, not incident time

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c06_triton_4483_batch_latency.client_avg_latency_usec scales with batch/payload work; check expected cost model before calling it saturation.
  Option C: parameter sensitivity is present; do not flatten the sweep into one average.
  Option C: batch-size sweeps may reflect more per-request work, not a queueing failure.
  Option D: detector output is incomplete; request more metrics if evidence is thin.

GUARDRAIL:
  Do not turn timing into causality without dependency, deploy, or resource evidence.

Return concise structured findings.
```

## Trace-On Response

```text
1. Performance issue

Batch-size sweep shows latency and server compute-infer time rising sharply as batch size increases, while throughput improves only up to about batch 16 and then flattens or declines. This is a parameter-sensitive batch workload behavior, not proven queue saturation or a Triton defect.

2. Evidence

- Issue-body perf_analyzer rows cover batch sizes 1 through 128.
- Client average latency rises from 13,137 usec at batch 1 to 915,560 usec at batch 128, about 69.7x.
- Server compute-infer time rises from 9,827 usec at batch 1 to 425,814 usec at batch 128.
- Throughput rises from 75.9241 infer/sec at batch 1 to a peak of 144 infer/sec at batch 16, then ends lower at 127.986 infer/sec at batch 128.
- CUDA shared-memory follow-up still shows compute-infer increasing from 8,897 usec at batch 1 to 407,990 usec at batch 128.
- Trace flags this as batch/payload work scaling and parameter sensitivity; it explicitly warns against treating timing alone as causality.
- Resolution evidence says a Triton contributor explained larger batches require more data movement and work, and the reporter accepted the behavior as expected.

3. Missing evidence

- No model architecture, tensor shape, payload size, GPU utilization, memory bandwidth, kernel timing, or host/device transfer breakdown is provided here.
- No evidence isolates queueing delay versus compute work versus data movement.
- No independent expected cost model for how this model should scale with batch size is included.
- No concurrency/request scheduling details beyond the visible perf_analyzer rows are available.

4. Recommended next diagnostic step

Build an expected per-batch cost breakdown for this specific model and profile representative batch sizes, especially 1, 16, 64, and 128, with GPU utilization, memory transfer, and kernel timing. Use that to separate normal per-request work scaling from any avoidable overhead before claiming saturation or a server-side regression.
```

## Verdict Review

```text
Winner: trace-on

Concise reason: Both answers identify that latency rises with batch size and cite the public resolution that this is expected larger-batch work/data movement, not a proven Triton defect. Trace-on wins because it explicitly preserves the trace distinction between parameter-sweep work scaling and queue saturation, calls out throughput peaking near batch 16 then flattening/declining, and recommends building an expected per-batch cost breakdown before claiming abnormal behavior.

Engine action: Keep the load-parameter sweep detectors. Strengthen the engine action language around batch sweeps: when batch size changes, default to "per-request work/payload scaling until disproven" and require evidence such as queue time, concurrency, utilization, transfer breakdown, or an expected model cost curve before labeling saturation or regression.
```
