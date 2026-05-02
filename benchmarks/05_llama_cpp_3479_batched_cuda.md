# Benchmark 05: llama_cpp_3479_batched_cuda

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
load_1,c05_llama_cpp_3479_batched_cuda_vllm_issue_vllm_comparison,tokens_per_second,46.0
load_10,c05_llama_cpp_3479_batched_cuda_vllm_issue_vllm_comparison,tokens_per_second,400.0
load_60,c05_llama_cpp_3479_batched_cuda_vllm_issue_vllm_comparison,tokens_per_second,1800.0
load_1,c05_llama_cpp_3479_batched_cuda_llama_cpp_issue_llama_cpp_a100,tokens_per_second,108.29
load_8,c05_llama_cpp_3479_batched_cuda_llama_cpp_issue_llama_cpp_a100,tokens_per_second,247.3
load_10,c05_llama_cpp_3479_batched_cuda_llama_cpp_issue_llama_cpp_a100,tokens_per_second,296.58
load_16,c05_llama_cpp_3479_batched_cuda_llama_cpp_issue_llama_cpp_a100,tokens_per_second,368.59
load_32,c05_llama_cpp_3479_batched_cuda_llama_cpp_issue_llama_cpp_a100,tokens_per_second,422.33
load_60,c05_llama_cpp_3479_batched_cuda_llama_cpp_issue_llama_cpp_a100,tokens_per_second,489.99
load_64,c05_llama_cpp_3479_batched_cuda_llama_cpp_issue_llama_cpp_a100,tokens_per_second,481.83
load_8,c05_llama_cpp_3479_batched_cuda_master_pr_serving_multiple_clients,tokens_per_second,247.3
load_8,c05_llama_cpp_3479_batched_cuda_pr_pr_serving_multiple_clients,tokens_per_second,470.36
load_16,c05_llama_cpp_3479_batched_cuda_master_pr_serving_multiple_clients,tokens_per_second,368.59
load_16,c05_llama_cpp_3479_batched_cuda_pr_pr_serving_multiple_clients,tokens_per_second,656.3
load_32,c05_llama_cpp_3479_batched_cuda_master_pr_serving_multiple_clients,tokens_per_second,422.33
load_32,c05_llama_cpp_3479_batched_cuda_pr_pr_serving_multiple_clients,tokens_per_second,845.67
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
# c05 llama.cpp #3479 batched CUDA performance

Source URL: https://github.com/ggml-org/llama.cpp/issues/3479

Status: accepted.

Raw performance evidence: confirmed. The issue body includes vLLM comparison values and llama.cpp batch-size tokens/s tables for OpenLLaMA 7B F16 on A100. A later comment adds 1-GPU vs 2-GPU batched-bench tables.

Resolution evidence: confirmed. PR https://github.com/ggml-org/llama.cpp/pull/3749 resolves #3479, was merged on 2023-10-24, and includes before/after benchmark tables. A maintainer comment on the issue says that after #3749 the performance is now comparable.

Normalized CSV: feasible. `normalized.csv` extracts the issue-body batch-size tokens/s values and the PR's serving-multiple-clients master/PR comparison.

RAW EVIDENCE:
Public source read: https://github.com/ggml-org/llama.cpp/issues/3479

Issue title:
llama : improve batched decoding performance

Visible vLLM comparison from issue:
Batch size 1: 46 tokens/s
Batch size 10: 400 tokens/s
Batch size 60: 1.8k tokens/s

Visible llama.cpp A100/OpenLLaMA 7B F16 results:
Batch size 1: 108.29 tokens/s
Batch size 8: 247.30 tokens/s
Batch size 10: 296.58 tokens/s
Batch size 16: 368.59 tokens/s
Batch size 32: 422.33 tokens/s
Batch size 60: 489.99 tokens/s
Batch size 64: 481.83 tokens/s

Issue statement:
At batch size 60, llama.cpp performance is roughly 5x slower than the vLLM value reported in the referenced post.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
llama.cpp batched CUDA decoding underperforms the cited vLLM comparison at large batch sizes, especially batch size 60.

2. Evidence
The issue reports vLLM at 46 tokens/s for batch size 1, 400 tokens/s for batch size 10, and 1.8k tokens/s for batch size 60. The llama.cpp A100/OpenLLaMA 7B F16 table reports 108.29 tokens/s at batch size 1, 296.58 tokens/s at batch size 10, and 489.99 tokens/s at batch size 60. The issue states that at batch size 60 llama.cpp is roughly 5x slower than the vLLM value from the referenced post. PR #3749 later resolved #3479, and a maintainer stated performance became comparable after the PR.

3. Missing evidence
The prompt does not include identical benchmark setups for vLLM and llama.cpp, full hardware/software configuration, profiler traces, repeated-run variance, or the before/after PR #3749 benchmark details needed to quantify the exact fix.

4. Recommended next diagnostic step
Reproduce batch-size scaling for llama.cpp before and after PR #3749 on the same A100/OpenLLaMA 7B F16 setup, then compare against vLLM under matched settings while collecting CUDA kernel timing and batching-efficiency metrics.
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
# c05 llama.cpp #3479 batched CUDA performance

Source URL: https://github.com/ggml-org/llama.cpp/issues/3479

Status: accepted.

Raw performance evidence: confirmed. The issue body includes vLLM comparison values and llama.cpp batch-size tokens/s tables for OpenLLaMA 7B F16 on A100. A later comment adds 1-GPU vs 2-GPU batched-bench tables.

Resolution evidence: confirmed. PR https://github.com/ggml-org/llama.cpp/pull/3749 resolves #3479, was merged on 2023-10-24, and includes before/after benchmark tables. A maintainer comment on the issue says that after #3749 the performance is now comparable.

Normalized CSV: feasible. `normalized.csv` extracts the issue-body batch-size tokens/s values and the PR's serving-multiple-clients master/PR comparison.

RAW EVIDENCE:
Public source read: https://github.com/ggml-org/llama.cpp/issues/3479

Issue title:
llama : improve batched decoding performance

Visible vLLM comparison from issue:
Batch size 1: 46 tokens/s
Batch size 10: 400 tokens/s
Batch size 60: 1.8k tokens/s

Visible llama.cpp A100/OpenLLaMA 7B F16 results:
Batch size 1: 108.29 tokens/s
Batch size 8: 247.30 tokens/s
Batch size 10: 296.58 tokens/s
Batch size 16: 368.59 tokens/s
Batch size 32: 422.33 tokens/s
Batch size 60: 489.99 tokens/s
Batch size 64: 481.83 tokens/s

Issue statement:
At batch size 60, llama.cpp performance is roughly 5x slower than the vLLM value reported in the referenced post.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 7 condition labels across 16 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] condition_delta: c05_llama_cpp_3479_batched_cuda_llama_cpp_issue_llama_cpp_a100.tokens_per_second at load_60 (108.29 -> 489.99), confidence=0.94
      Evidence: tokens_per_second changes across benchmark conditions; min=108.3 at load_1; max=490 at load_60; ratio=4.52x; compare conditions before explaining cause
  [2] condition_delta: c05_llama_cpp_3479_batched_cuda_vllm_issue_vllm_comparison.tokens_per_second at load_60 (46.0 -> 1800.0), confidence=0.95
      Evidence: tokens_per_second changes across benchmark conditions; min=46 at load_1; max=1800 at load_60; ratio=39.13x; compare conditions before explaining cause
  [3] condition_delta: c05_llama_cpp_3479_batched_cuda_master_pr_serving_multiple_clients.tokens_per_second at load_8 (247.3 -> 422.33), confidence=0.71
      Evidence: tokens_per_second changes across benchmark conditions; min=247.3 at load_8; max=422.3 at load_32; ratio=1.71x; compare conditions before explaining cause
  [4] condition_delta: c05_llama_cpp_3479_batched_cuda_pr_pr_serving_multiple_clients.tokens_per_second at load_8 (470.36 -> 845.67), confidence=0.73
      Evidence: tokens_per_second changes across benchmark conditions; min=470.4 at load_8; max=845.7 at load_32; ratio=1.80x; compare conditions before explaining cause

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c05_llama_cpp_3479_batched_cuda_llama_cpp_issue_llama_cpp_a100.tokens_per_second differs across benchmark conditions; compare conditions before explaining cause.
  Option C: this is sparse benchmark evidence; preserve condition labels and deltas.
  Option D: detector output is incomplete; request more metrics if evidence is thin.

GUARDRAIL:
  Do not turn timing into causality without dependency, deploy, or resource evidence.

Return concise structured findings.
```

## Trace-On Response

```text
1. Performance issue
- llama.cpp CUDA batched decoding scales with batch size, but much less effectively than the reported vLLM comparison at high batch size. The issue is a batched throughput gap, especially around batch size 60.

2. Evidence
- vLLM comparison: batch size 1 at 46 tok/s, batch size 10 at 400 tok/s, and batch size 60 at 1800 tok/s.
- llama.cpp A100/OpenLLaMA 7B F16: batch size 1 at 108.29 tok/s, 10 at 296.58 tok/s, 32 at 422.33 tok/s, 60 at 489.99 tok/s, and 64 at 481.83 tok/s.
- At batch size 60, the issue states llama.cpp is roughly 5x slower than vLLM.
- The deterministic trace preserves condition labels and shows llama.cpp rising 4.52x from batch 1 to 60, while the vLLM comparison rises 39.13x from batch 1 to 60. PR comparison rows also show higher post-PR throughput, but those are still benchmark deltas, not root-cause proof.

3. Missing evidence
- The trace does not include CUDA kernel profiles, occupancy, memory bandwidth, batching implementation details, prompt/decode mix, exact parity of model/configuration with vLLM, or end-to-end serving overhead breakdown.
- Cross-system comparison may include configuration and implementation differences that are not controlled in the trace.

4. Recommended next diagnostic step
- Reproduce batch-size sweeps under matched model, precision, hardware, sequence lengths, and serving settings, then collect CUDA profiling for batch 32/60/64 to identify whether the bottleneck is kernel efficiency, memory movement, synchronization, or batching overhead.
```

## Verdict Review

```text
Winner: trace-on

Reason:
Baseline correctly identifies the llama.cpp vs vLLM batch-size throughput gap. Trace-on is stronger because it keeps the condition labels and contrasts scaling shape: llama.cpp 4.52x versus vLLM comparison 39.13x from batch 1 to 60.

Engine action:
No further patch needed.
```
