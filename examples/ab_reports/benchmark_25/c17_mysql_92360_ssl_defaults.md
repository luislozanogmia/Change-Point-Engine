# A/B Report: `c17_mysql_92360_ssl_defaults`

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
mysql_8_0_3,c17_mysql_92360_ssl_defaults,sysbench_point_select_qps_or_tps,510000.0
mysql_8_0_11,c17_mysql_92360_ssl_defaults,sysbench_point_select_qps_or_tps,420000.0
mysql_8_0,c17_mysql_92360_ssl_defaults,sysbench_point_select_128_threads_tps,480011.29
mysql_8_0,c17_mysql_92360_ssl_defaults,sysbench_point_select_128_threads_qps,480011.29
mysql_5_7,c17_mysql_92360_ssl_defaults,replay_point_select_qps,557000.0
mysql_8_0,c17_mysql_92360_ssl_defaults,replay_point_select_qps,510000.0
mysql_8_0,c17_mysql_92360_ssl_defaults,broadwell_max_m_qps,1.184
mysql_5_7,c17_mysql_92360_ssl_defaults,broadwell_max_m_qps,1.313
ssl_0,c17_mysql_92360_ssl_defaults,ssl_point_select_w_qps,35.0
ssl_1,c17_mysql_92360_ssl_defaults,ssl_point_select_w_qps,20.0
before_log_10s,c17_mysql_92360_ssl_defaults,slow_query_log_512_threads_qps,1650241.84
before_log_20s,c17_mysql_92360_ssl_defaults,slow_query_log_512_threads_qps,1648605.56
before_log_30s,c17_mysql_92360_ssl_defaults,slow_query_log_512_threads_qps,1661280.02
after_log_50s,c17_mysql_92360_ssl_defaults,slow_query_log_512_threads_qps,553805.37
after_log_60s,c17_mysql_92360_ssl_defaults,slow_query_log_512_threads_qps,549367.49
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
# c17 MySQL bug #92360 SSL/default performance difference

Source: https://bugs.mysql.com/bug.php?id=92360

Status: accepted.

The MySQL bug page is public and contains QPS/TPS rows across sysbench point-select runs, including 128-thread and 512-thread results. Raw performance evidence exists as visible numeric benchmark rows such as 480011.29 QPS/TPS, 557k versus 510k QPS, SSL off/on observations of 35w versus 20w QPS, and slow-query-log rows dropping from about 1.65M QPS to about 550k QPS. Resolution evidence exists in the bug history as a configuration/default explanation rather than a code fix: Oracle/MySQL triage explains OpenSSL/default certificate behavior in 8.0.11 and configuration effects.

Normalized CSV feasibility: feasible. The visible table/comment text exposes concrete QPS/TPS values.

RAW EVIDENCE:
Public source checked:
https://bugs.mysql.com/bug.php?id=92360

Raw performance evidence confirmed:
- Reported MySQL 8.0.3 result: 510k SQL TPS/QPS.
- Reported MySQL 8.0.11 result: 420k SQL TPS/QPS.
- 128-thread point-select run: tps 480011.29 and qps 480011.29.
- Replay result: MySQL 5.7 reaches 557k QPS while MySQL 8.0 reaches 510k QPS.
- Broadwell comparison in comments: 1.184M QPS for MySQL 8.0 and 1.313M QPS for MySQL 5.7.
- SSL comparison: ssl=0 gives 35w QPS; ssl=1 gives 20w QPS and lock contention.
- Slow query log example: QPS around 1,650,241 to 1,661,280 before enabling slow_query_log, then around 553,805 and 549,367 after.

No values were invented.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
- MySQL 8.0 point-select throughput is reported lower than MySQL 5.7/earlier 8.0 baselines, with additional large drops when SSL or slow query logging are enabled.

2. Evidence
- 8.0.3 reported at 510k SQL TPS/QPS versus 8.0.11 at 420k.
- 128-thread point-select run shows 480011.29 TPS/QPS.
- Replay comparison shows 5.7 at 557k QPS versus 8.0 at 510k QPS.
- Broadwell comparison shows 8.0 at 1.184M QPS versus 5.7 at 1.313M QPS.
- SSL comparison reports ssl=0 at 35w QPS and ssl=1 at 20w QPS with lock contention.
- Slow query log example drops from about 1.65M QPS to about 550k QPS.
- Triage/resolution evidence points to OpenSSL/default certificate and configuration behavior, not a confirmed code fix.

3. Missing evidence
- Controlled apples-to-apples benchmark matrix across versions with identical config, hardware, schema, dataset, and sysbench parameters.
- CPU, lock, and wait-profile data tied to each throughput row.
- Explicit isolation of SSL, certificate defaults, and slow-query-log settings from other 8.0 changes.

4. Recommended next diagnostic step
- Reproduce point-select runs on one host while toggling only SSL/default certificate settings and slow_query_log, collecting QPS plus CPU/lock/wait profiles for each configuration.
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
# c17 MySQL bug #92360 SSL/default performance difference

Source: https://bugs.mysql.com/bug.php?id=92360

Status: accepted.

The MySQL bug page is public and contains QPS/TPS rows across sysbench point-select runs, including 128-thread and 512-thread results. Raw performance evidence exists as visible numeric benchmark rows such as 480011.29 QPS/TPS, 557k versus 510k QPS, SSL off/on observations of 35w versus 20w QPS, and slow-query-log rows dropping from about 1.65M QPS to about 550k QPS. Resolution evidence exists in the bug history as a configuration/default explanation rather than a code fix: Oracle/MySQL triage explains OpenSSL/default certificate behavior in 8.0.11 and configuration effects.

Normalized CSV feasibility: feasible. The visible table/comment text exposes concrete QPS/TPS values.

RAW EVIDENCE:
Public source checked:
https://bugs.mysql.com/bug.php?id=92360

Raw performance evidence confirmed:
- Reported MySQL 8.0.3 result: 510k SQL TPS/QPS.
- Reported MySQL 8.0.11 result: 420k SQL TPS/QPS.
- 128-thread point-select run: tps 480011.29 and qps 480011.29.
- Replay result: MySQL 5.7 reaches 557k QPS while MySQL 8.0 reaches 510k QPS.
- Broadwell comparison in comments: 1.184M QPS for MySQL 8.0 and 1.313M QPS for MySQL 5.7.
- SSL comparison: ssl=0 gives 35w QPS; ssl=1 gives 20w QPS and lock contention.
- Slow query log example: QPS around 1,650,241 to 1,661,280 before enabling slow_query_log, then around 553,805 and 549,367 after.

No values were invented.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 11 condition labels across 15 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] phased_remediation: c17_mysql_92360_ssl_defaults.slow_query_log_512_threads_qps at before_log_30s, confidence=0.74
      Evidence: multiple after/post-remediation stages are present; preserve staged fixes and residual bottlenecks instead of collapsing to one before/after delta
  [2] release_resolution_metadata: c17_mysql_92360_ssl_defaults.slow_query_log_512_threads_qps at before_log_30s, confidence=0.74
      Evidence: version/release/fix labels are present; preserve introduced, regressed, reverted, fixed, or canary metadata alongside metric deltas
      versions: mysql_8_0_11, mysql_8_0_3, mysql_8_0, mysql_5_7
  [3] condition_delta: c17_mysql_92360_ssl_defaults.slow_query_log_512_threads_qps at before_log_30s (549367.49 -> 1661280.02), confidence=0.87
      Evidence: slow_query_log_512_threads_qps changes across benchmark conditions; min=5.494e+05 at after_log_60s; max=1.661e+06 at before_log_30s; ratio=3.02x; compare conditions before explaining cause
  [4] condition_delta: c17_mysql_92360_ssl_defaults.sysbench_point_select_qps_or_tps at mysql_8_0_3 (420000.0 -> 510000.0), confidence=0.57
      Evidence: sysbench_point_select_qps_or_tps changes across benchmark conditions; min=4.2e+05 at mysql_8_0_11; max=5.1e+05 at mysql_8_0_3; ratio=1.21x; compare conditions before explaining cause
  [5] condition_delta: c17_mysql_92360_ssl_defaults.ssl_point_select_w_qps at ssl_1 (20.0 -> 35.0), confidence=0.72
      Evidence: ssl_point_select_w_qps changes across benchmark conditions; min=20 at ssl_1; max=35 at ssl_0; ratio=1.75x; compare conditions before explaining cause

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c17_mysql_92360_ssl_defaults.slow_query_log_512_threads_qps is the first visible shift.
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
- MySQL point-select throughput varies materially across benchmark conditions, with the strongest observed drop tied to slow-query-log enabled conditions and additional differences across 8.0.3 vs 8.0.11 and SSL on vs off.

2. Evidence
- Slow-query-log 512-thread QPS ranges from about 1.66M before logging to about 550k after logging, a roughly 3.0x condition delta in the trace.
- Sysbench point-select QPS/TPS shows 510k for MySQL 8.0.3 versus 420k for MySQL 8.0.11, a 1.21x delta.
- SSL comparison shows 35w QPS with ssl=0 versus 20w QPS with ssl=1, a 1.75x delta.
- Public bug evidence also reports 5.7 at 557k QPS versus 8.0 at 510k QPS and comments about SSL/default certificate behavior.

3. Missing evidence
- Controlled reproduction with all non-target settings held constant.
- CPU, lock, TLS, logging, and I/O profiles for each condition.
- Exact server configuration, certificate/default SSL state, slow-query-log settings, hardware, and client workload parity.
- Evidence connecting any default/configuration difference directly to the measured deltas.

4. Recommended next diagnostic step
- Run a controlled A/B benchmark matrix toggling only slow_query_log and SSL/default certificate settings, while collecting CPU, lock contention, TLS, and I/O profiles for each run.
```

## Verdict Review

```text
Winner: trace-on

Concise reason: Trace-on preserves the strongest condition deltas from the trace, especially the 3.0x slow-query-log spread and the SSL on/off spread, while still avoiding unsupported causality around OpenSSL/default certificates.

Engine action: Keep condition_delta behavior for benchmark-condition tables; no new detector gap flagged.
```
