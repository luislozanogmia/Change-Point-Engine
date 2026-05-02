# Benchmark 18: go_67585_runtime_mutex_regression

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
before,c19_go_67585_runtime_mutex_regression,tile38queryload_20_us_per_op,370.0
after,c19_go_67585_runtime_mutex_regression,tile38queryload_20_us_per_op,372.8
before,c19_go_67585_runtime_mutex_regression,tile38queryload_20_k_ops_per_sec,40.54
after,c19_go_67585_runtime_mutex_regression,tile38queryload_20_k_ops_per_sec,40.24
before,c19_go_67585_runtime_mutex_regression,chancontended_20_us_per_op,42.76
after,c19_go_67585_runtime_mutex_regression,chancontended_20_us_per_op,82.1
regressed,c19_go_67585_runtime_mutex_regression,runtime_lock_cpu_gomaxprocs_88_cpu_seconds,541.94
comparison,c19_go_67585_runtime_mutex_regression,runtime_lock_cpu_gomaxprocs_44_cpu_seconds,19.5
comparison,c19_go_67585_runtime_mutex_regression,runtime_lock_cpu_gomaxprocs_22_cpu_seconds,4.13
regressed,c19_go_67585_runtime_mutex_regression,futex_syscalls_chancontended_count,27153822.0
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
# c19 Go #67585 runtime mutex regression

Source: https://github.com/golang/go/issues/67585

Status: accepted.

The Go issue is public and contains detailed benchstat/SWEET/profile evidence for a runtime mutex regression. Raw evidence includes Tile38QueryLoad, runtime ChanContended, futex-count bpftrace output, and CPU profile percentages by GOMAXPROCS. Resolution evidence is public: Go contributors chose revert as the safe resolution, linked multiple revert CLs, and later confirmed Tile38QueryLoad-88 returned to its prior sec/op and latency baseline.

Normalized CSV feasibility: feasible. Multiple visible numeric rows are available in the issue comments.

RAW EVIDENCE:
Public source checked:
https://github.com/golang/go/issues/67585

Raw performance evidence confirmed:
- Benchstat Tile38QueryLoad-20: before 370.0us, after 372.8us, +0.75% sec/op.
- Benchstat Tile38QueryLoad-20 ops/s: before 40.54k, after 40.24k, -0.74%.
- Runtime ChanContended-20: before 42.76us/op, after 82.10us/op, +91.97%.
- bpftrace futex count example: runtime.test-go 27,153,822 futex syscalls for 20,000,000 channel operations.
- Tile38 GOMAXPROCS profile: runtime.lock cum CPU 541.94s/35.17% at 88, 19.50s/2.41% at 44, 4.13s/0.56% at 22.

These are raw benchmark/profile values copied from the public issue comments. No additional values were inferred.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
- A Go runtime mutex change regresses contended synchronization performance, most visibly in channel contention and high-GOMAXPROCS Tile38QueryLoad profiles.

2. Evidence
- Tile38QueryLoad-20 sec/op moves from 370.0us to 372.8us, a +0.75% regression.
- Tile38QueryLoad-20 ops/s moves from 40.54k to 40.24k, a -0.74% regression.
- Runtime ChanContended-20 worsens from 42.76us/op to 82.10us/op, a +91.97% regression.
- bpftrace shows 27,153,822 futex syscalls for 20,000,000 channel operations.
- Tile38 GOMAXPROCS profile shows runtime.lock cumulative CPU at 541.94s/35.17% for 88, versus 19.50s/2.41% for 44 and 4.13s/0.56% for 22.
- Public resolution evidence says contributors selected revert, and later confirmation indicates Tile38QueryLoad-88 returned to prior baseline.

3. Missing evidence
- Exact commit range and benchmark environment details in the supplied evidence.
- Before/after profiles for the reverted state using the same run configuration.
- Broader workload impact outside Tile38 and runtime channel contention.

4. Recommended next diagnostic step
- Reproduce the ChanContended and Tile38QueryLoad benchmarks across the candidate change and revert, collecting futex counts and CPU profiles at multiple GOMAXPROCS values.
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
# c19 Go #67585 runtime mutex regression

Source: https://github.com/golang/go/issues/67585

Status: accepted.

The Go issue is public and contains detailed benchstat/SWEET/profile evidence for a runtime mutex regression. Raw evidence includes Tile38QueryLoad, runtime ChanContended, futex-count bpftrace output, and CPU profile percentages by GOMAXPROCS. Resolution evidence is public: Go contributors chose revert as the safe resolution, linked multiple revert CLs, and later confirmed Tile38QueryLoad-88 returned to its prior sec/op and latency baseline.

Normalized CSV feasibility: feasible. Multiple visible numeric rows are available in the issue comments.

RAW EVIDENCE:
Public source checked:
https://github.com/golang/go/issues/67585

Raw performance evidence confirmed:
- Benchstat Tile38QueryLoad-20: before 370.0us, after 372.8us, +0.75% sec/op.
- Benchstat Tile38QueryLoad-20 ops/s: before 40.54k, after 40.24k, -0.74%.
- Runtime ChanContended-20: before 42.76us/op, after 82.10us/op, +91.97%.
- bpftrace futex count example: runtime.test-go 27,153,822 futex syscalls for 20,000,000 channel operations.
- Tile38 GOMAXPROCS profile: runtime.lock cum CPU 541.94s/35.17% at 88, 19.50s/2.41% at 44, 4.13s/0.56% at 22.

These are raw benchmark/profile values copied from the public issue comments. No additional values were inferred.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 4 condition labels across 10 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] profile_hotspot: c19_go_67585_runtime_mutex_regression.futex_syscalls_chancontended_count at regressed, confidence=0.78
      Evidence: profile/hotspot counters appear with the regression evidence; inspect code-path attribution instead of only metric deltas
  [2] release_resolution_metadata: c19_go_67585_runtime_mutex_regression.futex_syscalls_chancontended_count at regressed, confidence=0.74
      Evidence: version/release/fix labels are present; preserve introduced, regressed, reverted, fixed, or canary metadata alongside metric deltas
      regressed: regressed
  [3] mechanism_evidence: c19_go_67585_runtime_mutex_regression.runtime_lock_cpu_gomaxprocs_88_cpu_seconds at regressed, confidence=0.72
      Evidence: named low-level mechanisms appear in the evidence; retain them as evidence labels without promoting them to root cause unless backed by profiling, bisection, or owner notes
      mechanisms: runtime, futex
  [4] condition_delta: c19_go_67585_runtime_mutex_regression.chancontended_20_us_per_op at before (42.76 -> 82.1), confidence=0.75
      Evidence: chancontended_20_us_per_op changes across benchmark conditions; min=42.76 at before; max=82.1 at after; ratio=1.92x; compare conditions before explaining cause

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c19_go_67585_runtime_mutex_regression.futex_syscalls_chancontended_count is the first visible shift.
  Option C: this is sparse benchmark evidence; preserve condition labels and deltas.
  Option C: preserve named mechanisms as evidence labels, not automatic root cause.
  Option C: release/fix metadata can be the strongest resolution evidence.
  Option D: detector output is incomplete; request more metrics if evidence is thin.

GUARDRAIL:
  Do not turn timing into causality without dependency, deploy, or resource evidence.

Return concise structured findings.
```

## Trace-On Response

```text
1. Performance issue

Go runtime channel/mutex contention benchmarks show a regression after the compared change, with the clearest slowdown in `Runtime ChanContended-20`. Tile38 query load shows smaller throughput/latency movement, while high-GOMAXPROCS profiles show runtime locking becoming a prominent hotspot.

2. Evidence

- `Runtime ChanContended-20` increased from 42.76 us/op before to 82.10 us/op after, about 1.92x slower.
- Tile38QueryLoad-20 changed from 370.0 us to 372.8 us, with ops/sec decreasing from 40.54k to 40.24k.
- bpftrace evidence reports 27,153,822 futex syscalls for 20,000,000 channel operations in the contended case.
- CPU profile evidence shows `runtime.lock` cumulative CPU rising notably at high GOMAXPROCS, including 541.94s / 35.17% at GOMAXPROCS=88.
- Public resolution evidence says the safe fix was revert, and later Tile38QueryLoad-88 returned to its prior sec/op and latency baseline.

3. Missing evidence

- Direct code-path attribution proving which runtime change caused the futex/lock increase.
- A controlled before/after profile comparison for the exact reverted change across the same hardware and GOMAXPROCS matrix.
- Distribution data beyond the cited benchmark/profile rows, such as repeated run variance and confidence intervals for all affected workloads.

4. Recommended next diagnostic step

Reproduce `Runtime ChanContended` and Tile38QueryLoad on the before, after, and reverted revisions under the same GOMAXPROCS settings, collecting paired CPU profiles plus futex/lock counters. Use that to connect the observed benchmark delta to a specific runtime lock path before making a root-cause claim.
```

## Verdict Review

```text
Winner: trace-on

Reason: Trace-on keeps the same benchmark and profile evidence as baseline but makes the causal boundary clearer: the futex and runtime.lock data show a prominent contention hotspot, while direct code-path attribution still needs controlled before/after profiles.

Engine action: Keep profile-hotspot detection; add a runtime-contention pattern that links lock/futex counters with benchmark regressions while requiring paired profiles before root-cause claims.
```
