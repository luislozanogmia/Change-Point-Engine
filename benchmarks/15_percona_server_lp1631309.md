# Benchmark 15: percona_server_lp1631309

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
percona_5_6_27,c16_percona_server_lp1631309,sysbench_oltp_read_only_tps,660.0
percona_5_6_28,c16_percona_server_lp1631309,sysbench_oltp_read_only_tps,36.0
percona_5_7_unmodified,c16_percona_server_lp1631309,sysbench_threads_8_transactions_per_sec,46.0
percona_5_7_rollback,c16_percona_server_lp1631309,sysbench_threads_8_transactions_per_sec,69.0
percona_5_7_us_sleep,c16_percona_server_lp1631309,sysbench_threads_8_transactions_per_sec,239.0
group_a_run_1,c16_percona_server_lp1631309,sysbench_group_transactions_per_sec,34.87
group_a_run_2,c16_percona_server_lp1631309,sysbench_group_transactions_per_sec,12.52
group_a_run_3,c16_percona_server_lp1631309,sysbench_group_transactions_per_sec,9.13
group_b_run_1,c16_percona_server_lp1631309,sysbench_group_transactions_per_sec,437.99
group_b_run_2,c16_percona_server_lp1631309,sysbench_group_transactions_per_sec,455.6
group_b_run_3,c16_percona_server_lp1631309,sysbench_group_transactions_per_sec,466.09
group_c_run_1,c16_percona_server_lp1631309,sysbench_group_transactions_per_sec,69.87
group_c_run_2,c16_percona_server_lp1631309,sysbench_group_transactions_per_sec,69.39
group_c_run_3,c16_percona_server_lp1631309,sysbench_group_transactions_per_sec,69.37
group_d_run_1,c16_percona_server_lp1631309,sysbench_group_transactions_per_sec,384.81
group_d_run_2,c16_percona_server_lp1631309,sysbench_group_transactions_per_sec,416.51
group_d_run_3,c16_percona_server_lp1631309,sysbench_group_transactions_per_sec,402.94
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
# c16 Percona Server Launchpad #1631309

Source: https://bugs.launchpad.net/percona-server/+bug/1631309

Status: accepted.

The Launchpad bug is public and contains sysbench TPS comparison data for Percona Server variants. Raw performance evidence exists because the report lists measured TPS values including 5.6.27 at 660 tps versus 5.6.28 at 36 tps, plus follow-up 5.7 branch measurements such as unmodified 46, rollback 69, and us-sleep 239 transactions/sec. Resolution evidence exists because Launchpad marks the Percona Server 5.6 and 5.7 tasks Fix Released, with 5.7 fixed in milestone 5.7.18-14.

Normalized CSV feasibility: feasible. The source exposes concrete numeric TPS values.

RAW EVIDENCE:
Public source checked:
https://bugs.launchpad.net/percona-server/+bug/1631309

Raw performance evidence confirmed:
- Initial report: Percona Server 5.6.27 measured 660 tps.
- Initial report: Percona Server 5.6.28 measured 36 tps.
- Initial report describes sysbench OLTP read-only throughput dropping by 50% single-thread up to 95% at 40 threads on a 16-core machine.
- Follow-up reproduction with 8 sysbench threads: 5.7-unmodified 46 transactions/sec, 5.7-rollback 69 transactions/sec, 5.7-us-sleep 239 transactions/sec.
- Additional visible transaction/sec groups include 34.87/12.52/9.13, 437.99/455.60/466.09, 69.87/69.39/69.37, and 384.81/416.51/402.94.

No non-visible values were inferred.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
Percona Server showed a severe sysbench OLTP read-only throughput regression between versions, especially at higher thread counts.

2. Evidence
- Initial report measured Percona Server 5.6.27 at 660 tps and 5.6.28 at 36 tps.
- The report described throughput drops from 50% in single-thread testing up to 95% at 40 threads on a 16-core machine.
- Follow-up 8-thread measurements showed 5.7-unmodified at 46 transactions/sec, 5.7-rollback at 69 transactions/sec, and 5.7-us-sleep at 239 transactions/sec.
- Additional visible transaction/sec groups included 34.87/12.52/9.13, 437.99/455.60/466.09, 69.87/69.39/69.37, and 384.81/416.51/402.94.
- Launchpad marked the Percona Server 5.6 and 5.7 tasks Fix Released, with the 5.7 fix in milestone 5.7.18-14.

3. Missing evidence
- Full sysbench command line, schema size, duration, warmup, and hardware/storage details.
- CPU, mutex, I/O, and wait-event profiles for the slow and fixed builds.
- Exact patch or code path responsible for the 5.6.28/5.7 regression.
- Statistical variation across repeated benchmark runs.

4. Recommended next diagnostic step
Reproduce the sysbench workload on the same hardware across 5.6.27, 5.6.28, affected 5.7, rollback, and fixed builds while collecting wait-event and CPU profiles to identify the bottleneck responsible for the TPS collapse.
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
# c16 Percona Server Launchpad #1631309

Source: https://bugs.launchpad.net/percona-server/+bug/1631309

Status: accepted.

The Launchpad bug is public and contains sysbench TPS comparison data for Percona Server variants. Raw performance evidence exists because the report lists measured TPS values including 5.6.27 at 660 tps versus 5.6.28 at 36 tps, plus follow-up 5.7 branch measurements such as unmodified 46, rollback 69, and us-sleep 239 transactions/sec. Resolution evidence exists because Launchpad marks the Percona Server 5.6 and 5.7 tasks Fix Released, with 5.7 fixed in milestone 5.7.18-14.

Normalized CSV feasibility: feasible. The source exposes concrete numeric TPS values.

RAW EVIDENCE:
Public source checked:
https://bugs.launchpad.net/percona-server/+bug/1631309

Raw performance evidence confirmed:
- Initial report: Percona Server 5.6.27 measured 660 tps.
- Initial report: Percona Server 5.6.28 measured 36 tps.
- Initial report describes sysbench OLTP read-only throughput dropping by 50% single-thread up to 95% at 40 threads on a 16-core machine.
- Follow-up reproduction with 8 sysbench threads: 5.7-unmodified 46 transactions/sec, 5.7-rollback 69 transactions/sec, 5.7-us-sleep 239 transactions/sec.
- Additional visible transaction/sec groups include 34.87/12.52/9.13, 437.99/455.60/466.09, 69.87/69.39/69.37, and 384.81/416.51/402.94.

No non-visible values were inferred.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 17 condition labels across 17 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] release_resolution_metadata: c16_percona_server_lp1631309.sysbench_threads_8_transactions_per_sec at percona_5_7_rollback, confidence=0.74
      Evidence: version/release/fix labels are present; preserve introduced, regressed, reverted, fixed, or canary metadata alongside metric deltas
      rollback: percona_5_7_rollback
      versions: percona_5_6_27, percona_5_6_28, percona_5_7_rollback, percona_5_7_unmodified, percona_5_7_us_sleep
  [2] condition_delta: c16_percona_server_lp1631309.sysbench_group_transactions_per_sec at group_b_run_3 (9.13 -> 466.09), confidence=0.95
      Evidence: sysbench_group_transactions_per_sec changes across benchmark conditions; min=9.13 at group_a_run_3; max=466.1 at group_b_run_3; ratio=51.05x; compare conditions before explaining cause
  [3] condition_delta: c16_percona_server_lp1631309.sysbench_oltp_read_only_tps at percona_5_6_28 (36.0 -> 660.0), confidence=0.95
      Evidence: sysbench_oltp_read_only_tps changes across benchmark conditions; min=36 at percona_5_6_28; max=660 at percona_5_6_27; ratio=18.33x; compare conditions before explaining cause
  [4] condition_delta: c16_percona_server_lp1631309.sysbench_threads_8_transactions_per_sec at percona_5_7_us_sleep (46.0 -> 239.0), confidence=0.95
      Evidence: sysbench_threads_8_transactions_per_sec changes across benchmark conditions; min=46 at percona_5_7_unmodified; max=239 at percona_5_7_us_sleep; ratio=5.20x; compare conditions before explaining cause

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c16_percona_server_lp1631309.sysbench_threads_8_transactions_per_sec has release/fix lineage; preserve versions, revert, fixed, and canary labels before explaining cause.
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
Percona Server showed a severe sysbench OLTP read-only throughput regression between versions and variants, with TPS dropping sharply in the reported benchmark conditions.

2. Evidence
- Initial report: Percona Server 5.6.27 measured 660 tps, while 5.6.28 measured 36 tps.
- The report describes 50% lower single-thread throughput and up to 95% lower throughput at 40 threads on a 16-core machine.
- Follow-up 8-thread measurements show 5.7-unmodified at 46 transactions/sec, rollback at 69, and us-sleep at 239.
- Additional visible transaction/sec groups range from about 9.13 to 466.09.
- The trace flags large condition deltas: 18.33x for 5.6.27 versus 5.6.28, 5.20x for 5.7 unmodified versus us-sleep, and 51.05x across grouped runs. It treats these as condition comparisons, not a time cascade.

3. Missing evidence
- Exact benchmark configuration for each run, including hardware, thread count, database settings, dataset size, and warmup duration.
- Variance or repeated-run statistics for the reported TPS values.
- Profiling or wait-event evidence explaining why the affected versions lost throughput.
- Patch-level mapping between rollback/us-sleep variants and the measured performance changes.

4. Recommended next diagnostic step
Reproduce the benchmark under a fixed sysbench and server configuration across the listed variants, collecting repeated TPS runs plus CPU, wait, lock, and profiling data to identify which code path or synchronization behavior accounts for the throughput loss.
```

## Verdict Review

```text
Winner: similar

Concise reason: Both outputs identify the severe cross-version sysbench TPS collapse and the need for controlled reproduction/profiling. Trace-on usefully quantifies condition ratios; baseline keeps fix-release context. Neither materially dominates.

Engine action: Keep condition-delta detection for versioned benchmark regressions. Add optional prompt emphasis to preserve fix/milestone status when present.
```
