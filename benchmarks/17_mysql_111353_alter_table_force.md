# Benchmark 17: mysql_111353_alter_table_force

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
mysql_5_7_initial,c18_mysql_111353_alter_table_force,alter_table_force_elapsed_seconds,31.139
mysql_8_0_33_initial,c18_mysql_111353_alter_table_force,alter_table_force_elapsed_seconds,110.049
mysql_8_0_42_run_1,c18_mysql_111353_alter_table_force,alter_table_force_elapsed_seconds,108.0
mysql_8_0_42_fastest,c18_mysql_111353_alter_table_force,alter_table_force_elapsed_seconds,107.0
mysql_8_0_42_run_3,c18_mysql_111353_alter_table_force,alter_table_force_elapsed_seconds,121.0
mysql_8_0_42_run_4,c18_mysql_111353_alter_table_force,alter_table_force_elapsed_seconds,124.0
mysql_8_0_42_run_5,c18_mysql_111353_alter_table_force,alter_table_force_elapsed_seconds,124.0
mysql_8_0_with_8_4_doublewrite_pages_run_1,c18_mysql_111353_alter_table_force,alter_table_force_elapsed_seconds,65.0
mysql_8_0_with_8_4_doublewrite_pages_run_2,c18_mysql_111353_alter_table_force,alter_table_force_elapsed_seconds,63.0
mysql_8_0_with_8_4_doublewrite_pages_run_3,c18_mysql_111353_alter_table_force,alter_table_force_elapsed_seconds,62.0
mysql_8_0_with_8_4_doublewrite_pages_fastest,c18_mysql_111353_alter_table_force,alter_table_force_elapsed_seconds,61.0
mysql_8_4_or_fixed_behavior,c18_mysql_111353_alter_table_force,alter_table_force_elapsed_seconds,56.0
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
# c18 MySQL bug #111353 ALTER TABLE FORCE regression

Source: https://bugs.mysql.com/bug.php?id=111353

Status: accepted.

The MySQL bug page is public and contains concrete benchmark timings showing ALTER TABLE ... FORCE taking roughly three times longer in MySQL 8.0.33 than in the reporter's 5.7 baseline: 1m50.049s versus 0m31.139s. Resolution evidence exists in the bug discussion through bug #114420/default handling in MySQL 8.4 and a documented workaround: setting `innodb_doublewrite_pages=128` in 8.0 gives timing close to the 5.7/8.4 behavior.

Normalized CSV feasibility: feasible. The source exposes visible elapsed-time values for affected, workaround, and comparison versions.

RAW EVIDENCE:
Public source checked:
https://bugs.mysql.com/bug.php?id=111353

Raw performance evidence confirmed:
- Initial report: MySQL 8.0.33 ALTER TABLE FORCE fastest time 1m50.049s.
- Initial report: MySQL 5.7 comparison time 0m31.139s.
- Follow-up on MySQL 8.0.42: ALTER FORCE rows include 1:48, 1:47, 2:01, 2:04, 2:04; fastest 1:47.
- Follow-up with the 8.4 value for innodb_doublewrite_pages: rows include 1:05, 1:03, 1:02, 1:01, 1:02; fastest 1:01.
- Additional follow-up rows show 0:56 repeated after ALTER ADD 0:00:57, with fastest 0:56.

No non-visible values were inferred.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
- `ALTER TABLE ... FORCE` is substantially slower on MySQL 8.0.33/8.0.42 than the reported 5.7 baseline.

2. Evidence
- Initial report: MySQL 8.0.33 fastest time is 1m50.049s versus MySQL 5.7 at 0m31.139s.
- MySQL 8.0.42 follow-up remains slow, with ALTER FORCE runs from 1:47 to 2:04 and fastest 1:47.
- Using the 8.4 value for `innodb_doublewrite_pages` gives faster runs from 1:01 to 1:05.
- Additional follow-up rows show about 0:56 after ALTER ADD 0:00:57.
- Discussion links the improvement to default handling/workaround behavior, including `innodb_doublewrite_pages=128`.

3. Missing evidence
- Full reproduction details for table size, schema, storage, filesystem, hardware, and MySQL configuration.
- I/O, doublewrite, redo, and wait metrics for slow and workaround runs.
- Direct comparison to MySQL 8.4 under the same environment and workload.

4. Recommended next diagnostic step
- Re-run the ALTER FORCE benchmark on the same dataset while varying only `innodb_doublewrite_pages`, collecting elapsed time plus InnoDB I/O/doublewrite and wait metrics.
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
# c18 MySQL bug #111353 ALTER TABLE FORCE regression

Source: https://bugs.mysql.com/bug.php?id=111353

Status: accepted.

The MySQL bug page is public and contains concrete benchmark timings showing ALTER TABLE ... FORCE taking roughly three times longer in MySQL 8.0.33 than in the reporter's 5.7 baseline: 1m50.049s versus 0m31.139s. Resolution evidence exists in the bug discussion through bug #114420/default handling in MySQL 8.4 and a documented workaround: setting `innodb_doublewrite_pages=128` in 8.0 gives timing close to the 5.7/8.4 behavior.

Normalized CSV feasibility: feasible. The source exposes visible elapsed-time values for affected, workaround, and comparison versions.

RAW EVIDENCE:
Public source checked:
https://bugs.mysql.com/bug.php?id=111353

Raw performance evidence confirmed:
- Initial report: MySQL 8.0.33 ALTER TABLE FORCE fastest time 1m50.049s.
- Initial report: MySQL 5.7 comparison time 0m31.139s.
- Follow-up on MySQL 8.0.42: ALTER FORCE rows include 1:48, 1:47, 2:01, 2:04, 2:04; fastest 1:47.
- Follow-up with the 8.4 value for innodb_doublewrite_pages: rows include 1:05, 1:03, 1:02, 1:01, 1:02; fastest 1:01.
- Additional follow-up rows show 0:56 repeated after ALTER ADD 0:00:57, with fastest 0:56.

No non-visible values were inferred.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 12 condition labels across 12 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] release_resolution_metadata: c18_mysql_111353_alter_table_force.alter_table_force_elapsed_seconds at mysql_8_4_or_fixed_behavior, confidence=0.74
      Evidence: version/release/fix labels are present; preserve introduced, regressed, reverted, fixed, or canary metadata alongside metric deltas
      fixed: mysql_8_4_or_fixed_behavior
      versions: mysql_5_7_initial, mysql_8_0_33_initial, mysql_8_0_42_fastest, mysql_8_0_42_run_1, mysql_8_0_42_run_3, mysql_8_0_42_run_4, mysql_8_0_42_run_5, mysql_8_0_with_8_4_doublewrite_pages_fastest
  [2] condition_delta: c18_mysql_111353_alter_table_force.alter_table_force_elapsed_seconds at mysql_8_0_42_run_4 (31.139 -> 124.0), confidence=0.92
      Evidence: alter_table_force_elapsed_seconds changes across benchmark conditions; min=31.14 at mysql_5_7_initial; max=124 at mysql_8_0_42_run_4; ratio=3.98x; compare conditions before explaining cause
  [3] version_fix_lineage: c18_mysql_111353_alter_table_force.alter_table_force_elapsed_seconds at mysql_8_4_or_fixed_behavior, confidence=0.76
      Evidence: versioned regression and fixed/canary conditions are present; preserve fix lineage alongside the timing delta

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c18_mysql_111353_alter_table_force.alter_table_force_elapsed_seconds has release/fix lineage; preserve versions, revert, fixed, and canary labels before explaining cause.
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
- ALTER TABLE ... FORCE is substantially slower in MySQL 8.0.x benchmark conditions than in the MySQL 5.7 comparison, with later 8.0.42 runs still showing elevated elapsed time.

2. Evidence
- Initial public evidence reports MySQL 8.0.33 fastest time at 1m50.049s versus MySQL 5.7 at 0m31.139s.
- Follow-up 8.0.42 ALTER FORCE runs include 1:48, 1:47, 2:01, 2:04, and 2:04.
- The trace records elapsed seconds ranging from 31.139s at mysql_5_7_initial to 124s at mysql_8_0_42_run_4, a 3.98x condition delta.
- Workaround/comparison rows with innodb_doublewrite_pages=128 improve to around 1:01, and later rows show about 0:56.

3. Missing evidence
- Full controlled benchmark environment details: schema size, storage, buffer pool state, filesystem, and hardware.
- I/O, doublewrite, redo, flush, and wait-event metrics during ALTER TABLE FORCE.
- Version-to-version isolation showing which configuration/default change accounts for the elapsed-time difference.
- Repeatability statistics beyond the visible timing rows.

4. Recommended next diagnostic step
- Reproduce the ALTER TABLE FORCE benchmark on the same dataset across 5.7, affected 8.0, 8.0 with innodb_doublewrite_pages=128, and 8.4, collecting InnoDB I/O, doublewrite, wait, and flush metrics.
```

## Verdict Review

```text
Winner: trace-on

Concise reason: Trace-on adds the 31.139s to 124s condition delta and better frames the MySQL 8.0.x timings, workaround rows, and missing InnoDB metrics as a controlled benchmark comparison.

Engine action: Keep condition_delta behavior for elapsed-time benchmark rows; no new detector gap flagged.
```
