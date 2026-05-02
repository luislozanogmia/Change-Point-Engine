# A/B Report: `c28_bun_23120_test_runner_regression`

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
bun_1_2_22,c28_bun_23120_test_runner_regression,test_suite_finish_time_value_seconds,2.25
bun_1_2_23,c28_bun_23120_test_runner_regression,test_suite_finish_time_value_seconds,3.34
elysia_bunx_bun_1_2_22_test,c28_bun_23120_test_runner_regression,hyperfine_mean_value_seconds,3.342
elysia_bunx_bun_1_2_22_test,c28_bun_23120_test_runner_regression,hyperfine_stddev_value_seconds,0.238
elysia_bunx_bun_1_2_23_test,c28_bun_23120_test_runner_regression,hyperfine_mean_value_seconds,4.185
elysia_bunx_bun_1_2_23_test,c28_bun_23120_test_runner_regression,hyperfine_stddev_value_seconds,0.138
elysia_bun_1_2_22_vs_1_2_23,c28_bun_23120_test_runner_regression,reported_speedup_value_x,1.25
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
# c28 Bun #23120 Test Runner Regression

Source: https://github.com/oven-sh/bun/issues/23120

Status: accepted

Verification date: 2026-05-02

Summary: Bun issue #23120 reports a test runner performance regression in Bun 1.2.23 versus Bun 1.2.22. The issue body shows the same 951-test suite taking 2.25 seconds on Bun 1.2.22 and 3.34 seconds on Bun 1.2.23. A commenter reproduced on the public Elysia project using `hyperfine`, where Bun 1.2.22 ran 1.25 +/- 0.10 times faster than Bun 1.2.23. PR #23199, titled `bun:test performance regression fix`, was merged and closed the issue.

Raw performance evidence confirmed:
- Bun 1.2.22: 951 tests across 94 files in 2.25 seconds.
- Bun 1.2.23: same suite in 3.34 seconds.
- Hyperfine reproduction on Elysia: Bun 1.2.23 mean 4.185 s +/- 0.138; Bun 1.2.22 mean 3.342 s +/- 0.238; 10 runs.

Resolution evidence confirmed:
- PR #23199: `bun:test performance regression fix`.
- PR #23199 was merged on 2025-10-03 and closes issue #23120.

normalized.csv: created from visible timing values in the issue body and hyperfine comment.

RAW EVIDENCE:
Source: https://github.com/oven-sh/bun/issues/23120

Issue title: [Bun 1.2.23] - regression: test performance

Raw performance evidence:

- Reporter platform: Darwin 22.6.0 x86_64 i386.
- Reporter says Bun 1.2.22 finished in 2.25 seconds:
  - 951 pass.
  - 0 fail.
  - 3170 expect() calls.
  - Ran 951 tests across 94 files. [2.25s]
- Reporter says Bun 1.2.23 finished in 3.34 seconds:
  - 951 pass.
  - 0 fail.
  - 3170 expect() calls.
  - Ran 951 tests across 94 files. [3.34s]

Public reproduction evidence:

- Commenter RiskyMH reproduced using Elysia on macOS M3:
  - Commands: `bunx bun@1.2.23 test` and `bunx bun@1.2.22 test`.
  - Hyperfine warmup: 3; runs: 10.
  - Bun 1.2.23 mean: 4.185 s +/- 0.138 s; range 4.045 s to 4.385 s.
  - Bun 1.2.22 mean: 3.342 s +/- 0.238 s; range 3.066 s to 3.786 s.
  - Summary: Bun 1.2.22 ran 1.25 +/- 0.10 times faster than Bun 1.2.23.

Reproduction project:
- https://github.com/elysiajs/elysia

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
- Bun 1.2.23 regressed test runner performance compared with Bun 1.2.22.

2. Evidence
- Reporter's same 951-test, 94-file suite completed in 2.25 s on Bun 1.2.22 and 3.34 s on Bun 1.2.23.
- Both runs passed 951 tests with 3170 `expect()` calls, indicating comparable workload completion.
- Independent Elysia reproduction with hyperfine shows Bun 1.2.23 mean 4.185 s +/- 0.138 versus Bun 1.2.22 mean 3.342 s +/- 0.238 across 10 runs.
- Hyperfine summary says Bun 1.2.22 was 1.25 +/- 0.10 times faster than Bun 1.2.23.
- PR #23199 is titled as a `bun:test` performance regression fix and closes the issue.

3. Missing evidence
- The reporter's original project or full reproduction steps are not included.
- No profiler output or breakdown identifies which test runner phase slowed down.
- Platform differences exist between the reporter's Darwin x86_64 environment and the Elysia macOS M3 reproduction.

4. Recommended next diagnostic step
- Reproduce the Elysia hyperfine comparison locally across Bun 1.2.22, 1.2.23, and the PR #23199 fixed build while profiling test discovery, module loading, and assertion execution phases.
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
# c28 Bun #23120 Test Runner Regression

Source: https://github.com/oven-sh/bun/issues/23120

Status: accepted

Verification date: 2026-05-02

Summary: Bun issue #23120 reports a test runner performance regression in Bun 1.2.23 versus Bun 1.2.22. The issue body shows the same 951-test suite taking 2.25 seconds on Bun 1.2.22 and 3.34 seconds on Bun 1.2.23. A commenter reproduced on the public Elysia project using `hyperfine`, where Bun 1.2.22 ran 1.25 +/- 0.10 times faster than Bun 1.2.23. PR #23199, titled `bun:test performance regression fix`, was merged and closed the issue.

Raw performance evidence confirmed:
- Bun 1.2.22: 951 tests across 94 files in 2.25 seconds.
- Bun 1.2.23: same suite in 3.34 seconds.
- Hyperfine reproduction on Elysia: Bun 1.2.23 mean 4.185 s +/- 0.138; Bun 1.2.22 mean 3.342 s +/- 0.238; 10 runs.

Resolution evidence confirmed:
- PR #23199: `bun:test performance regression fix`.
- PR #23199 was merged on 2025-10-03 and closes issue #23120.

normalized.csv: created from visible timing values in the issue body and hyperfine comment.

RAW EVIDENCE:
Source: https://github.com/oven-sh/bun/issues/23120

Issue title: [Bun 1.2.23] - regression: test performance

Raw performance evidence:

- Reporter platform: Darwin 22.6.0 x86_64 i386.
- Reporter says Bun 1.2.22 finished in 2.25 seconds:
  - 951 pass.
  - 0 fail.
  - 3170 expect() calls.
  - Ran 951 tests across 94 files. [2.25s]
- Reporter says Bun 1.2.23 finished in 3.34 seconds:
  - 951 pass.
  - 0 fail.
  - 3170 expect() calls.
  - Ran 951 tests across 94 files. [3.34s]

Public reproduction evidence:

- Commenter RiskyMH reproduced using Elysia on macOS M3:
  - Commands: `bunx bun@1.2.23 test` and `bunx bun@1.2.22 test`.
  - Hyperfine warmup: 3; runs: 10.
  - Bun 1.2.23 mean: 4.185 s +/- 0.138 s; range 4.045 s to 4.385 s.
  - Bun 1.2.22 mean: 3.342 s +/- 0.238 s; range 3.066 s to 3.786 s.
  - Summary: Bun 1.2.22 ran 1.25 +/- 0.10 times faster than Bun 1.2.23.

Reproduction project:
- https://github.com/elysiajs/elysia

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 5 condition labels across 7 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] release_resolution_metadata: c28_bun_23120_test_runner_regression.reported_speedup_value_x at elysia_bun_1_2_22_vs_1_2_23, confidence=0.74
      Evidence: version/release/fix labels are present; preserve introduced, regressed, reverted, fixed, or canary metadata alongside metric deltas
      versions: bun_1_2_22, bun_1_2_23, elysia_bunx_bun_1_2_22_test, elysia_bunx_bun_1_2_23_test, elysia_bun_1_2_22_vs_1_2_23
  [2] condition_delta: c28_bun_23120_test_runner_regression.test_suite_finish_time_value_seconds at bun_1_2_23 (2.25 -> 3.34), confidence=0.66
      Evidence: test_suite_finish_time_value_seconds changes across benchmark conditions; min=2.25 at bun_1_2_22; max=3.34 at bun_1_2_23; ratio=1.48x; compare conditions before explaining cause
  [3] condition_delta: c28_bun_23120_test_runner_regression.hyperfine_mean_value_seconds at elysia_bunx_bun_1_2_23_test (3.342 -> 4.185), confidence=0.58
      Evidence: hyperfine_mean_value_seconds changes across benchmark conditions; min=3.342 at elysia_bunx_bun_1_2_22_test; max=4.185 at elysia_bunx_bun_1_2_23_test; ratio=1.25x; compare conditions before explaining cause
  [4] condition_delta: c28_bun_23120_test_runner_regression.hyperfine_stddev_value_seconds at elysia_bunx_bun_1_2_23_test (0.138 -> 0.238), confidence=0.72
      Evidence: hyperfine_stddev_value_seconds changes across benchmark conditions; min=0.138 at elysia_bunx_bun_1_2_23_test; max=0.238 at elysia_bunx_bun_1_2_22_test; ratio=1.72x; compare conditions before explaining cause

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c28_bun_23120_test_runner_regression.reported_speedup_value_x has release/fix lineage; preserve versions, revert, fixed, and canary labels before explaining cause.
  Option C: this is sparse benchmark evidence; preserve condition labels and deltas.
  Option C: release/fix metadata can be the strongest resolution evidence.
  Option D: detector output is incomplete; request more metrics if evidence is thin.

GUARDRAIL:
  Do not turn timing into causality without dependency, deploy, or resource evidence.

Return concise structured findings.
```

## Trace-On Response

```text
1. Performance issue
- Bun 1.2.23 regressed test runner throughput versus Bun 1.2.22 on the same test workload.

2. Evidence
- Reporter evidence shows the same 951-test, 94-file suite taking 2.25 s on Bun 1.2.22 and 3.34 s on Bun 1.2.23.
- The trace captures this condition delta as 2.25 s to 3.34 s, a 1.48x spread.
- Independent hyperfine reproduction on Elysia shows Bun 1.2.22 mean 3.342 s versus Bun 1.2.23 mean 4.185 s, a 1.25x slowdown for 1.2.23.
- PR #23199 is identified as a merged test performance regression fix that closed the issue.

3. Missing evidence
- No CPU profile, test scheduling breakdown, module loading breakdown, or assertion/runtime attribution is included.
- The public evidence covers two workloads but not a larger version matrix or hardware-normalized measurements.
- The trace does not establish the internal root cause of the test runner slowdown.

4. Recommended next diagnostic step
- Benchmark Bun 1.2.22, 1.2.23, and the fixed build on the reporter suite and Elysia with profiling enabled, separating startup, discovery, module loading, execution, and reporting time.
```

## Verdict Review

```text
Winner: trace-on

Concise reason: Trace-on concisely combines the reporter suite delta, the independent Elysia hyperfine delta, and the merged performance-fix PR without adding unsupported phase-level causality.

Engine action: Keep condition_delta behavior for paired version benchmark rows; no new detector gap flagged.
```
