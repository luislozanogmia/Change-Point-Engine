# Benchmark 20: kafka_producer_regression

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
baseline_pre_regression,c23_kafka_producer_regression,throughput_value_records_per_second,115000.0
regressed,c23_kafka_producer_regression,throughput_value_records_per_second,105000.0
reverted,c23_kafka_producer_regression,throughput_value_records_per_second,115000.0
default_partitioner_test,c23_kafka_producer_regression,throughput_value_records_per_second,105000.0
confirmed_good_baseline,c23_kafka_producer_regression,throughput_value_records_per_second,118000.0
confirmed_fixed,c23_kafka_producer_regression,throughput_value_records_per_second,117000.0
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
# c23 Kafka Producer Regression

Source: https://issues.apache.org/jira/browse/KAFKA-14020

Status: accepted

Verification date: 2026-05-02

Summary: KAFKA-14020 reports a KafkaProducer throughput regression introduced by commit `f7db6031b84a136ad0e257df722b20faa7c37b8a`. The public Jira issue includes raw benchmark evidence from Kafka Streams benchmark infrastructure: many pre-regression runs around 115,000 records/sec, 40 runs including/after the regressing commit around 105,000 records/sec, and a reverted-trunk run returning to about 115,000 records/sec. A later comment confirms PR apache/kafka#12365 fixes the regression, with baseline and fixed throughput values.

Raw performance evidence confirmed:
- Pre-regression throughput: neighborhood of 115,000 records/sec.
- Regressed throughput: neighborhood of 105,000 records/sec across 40 runs.
- Revert test: return to around 115,000 records/sec.
- Fix confirmation: parent baseline 118k +/- 1k and PR/fixed commit 117k +/- 1k.

Resolution evidence confirmed:
- Jira resolution is Fixed, status Resolved, fixVersion 3.3.0.
- apache/kafka#12365 is merged.
- Reporter reran the same benchmark and confirmed the PR fixes the regression.

normalized.csv: created from visible numeric throughput values in the public Jira issue.

RAW EVIDENCE:
Source: https://issues.apache.org/jira/browse/KAFKA-14020

Issue title: Performance regression in Producer

Raw performance evidence:

- The issue states that commit `f7db6031b84a136ad0e257df722b20faa7c37b8a` introduced a 10% KafkaProducer performance regression under default config.
- Benchmark context: Kafka Streams benchmark provisioning 5 independent AWS clusters, with one broker node on i3.large and one client node on i3.large.
- Benchmark flow: run the producer for 10 minutes to generate test data, then run Kafka Streams configurations.
- Observed regression: the simplest Kafka Streams configuration is bounded by data-generator throughput, and investigation showed the data generator producer had regressed.
- The issue states numerous benchmark runs before the commit showed throughput around 115,000 records/sec.
- It also states 40 runs including and after the commit showed throughput around 105,000 records/sec.
- A trunk test with the commit reverted showed return to around 115,000 records/sec.

Configuration shown in Jira:

```
properties.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, broker);
properties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
properties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
```

Additional comment evidence:

2022-06-25 John Roesler:
- Setting the partitioner back to `DefaultPartitioner` did not help.
- Throughput of that test was `105k±2k` records/sec.

2022-07-12 John Roesler:
- The reporter reran the same benchmark after apache/kafka#12365.
- Baseline good performance at parent commit `e3202b9`: `118k±1k`.
- Fixed commit `3a6500b`: `117k±1k`.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
- KafkaProducer throughput regresses by about 10% under the reported default producer configuration after commit `f7db6031b84a136ad0e257df722b20faa7c37b8a`.

2. Evidence
- Jira states pre-regression benchmark runs were around 115,000 records/sec.
- Forty runs including/after the regressing commit were around 105,000 records/sec.
- Reverting the commit returned throughput to around 115,000 records/sec.
- Testing the partitioner change alone did not help, with throughput at `105k±2k` records/sec.
- Fix confirmation reports parent baseline `118k±1k` and fixed commit `117k±1k`.
- Resolution evidence says the issue was fixed in 3.3.0 and apache/kafka#12365 was merged.

3. Missing evidence
- Per-run raw throughput table for all pre/post/revert runs in the supplied prompt.
- CPU, allocation, network, batching, and broker/client metrics that identify the mechanism.
- Confirmation across producer-only benchmarks outside the Kafka Streams benchmark setup.

4. Recommended next diagnostic step
- Re-run the producer benchmark at parent, regressing commit, revert, and fixed commit with identical AWS/client/broker setup, collecting throughput plus producer metrics, CPU, allocation, and request/batch statistics.
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
# c23 Kafka Producer Regression

Source: https://issues.apache.org/jira/browse/KAFKA-14020

Status: accepted

Verification date: 2026-05-02

Summary: KAFKA-14020 reports a KafkaProducer throughput regression introduced by commit `f7db6031b84a136ad0e257df722b20faa7c37b8a`. The public Jira issue includes raw benchmark evidence from Kafka Streams benchmark infrastructure: many pre-regression runs around 115,000 records/sec, 40 runs including/after the regressing commit around 105,000 records/sec, and a reverted-trunk run returning to about 115,000 records/sec. A later comment confirms PR apache/kafka#12365 fixes the regression, with baseline and fixed throughput values.

Raw performance evidence confirmed:
- Pre-regression throughput: neighborhood of 115,000 records/sec.
- Regressed throughput: neighborhood of 105,000 records/sec across 40 runs.
- Revert test: return to around 115,000 records/sec.
- Fix confirmation: parent baseline 118k +/- 1k and PR/fixed commit 117k +/- 1k.

Resolution evidence confirmed:
- Jira resolution is Fixed, status Resolved, fixVersion 3.3.0.
- apache/kafka#12365 is merged.
- Reporter reran the same benchmark and confirmed the PR fixes the regression.

normalized.csv: created from visible numeric throughput values in the public Jira issue.

RAW EVIDENCE:
Source: https://issues.apache.org/jira/browse/KAFKA-14020

Issue title: Performance regression in Producer

Raw performance evidence:

- The issue states that commit `f7db6031b84a136ad0e257df722b20faa7c37b8a` introduced a 10% KafkaProducer performance regression under default config.
- Benchmark context: Kafka Streams benchmark provisioning 5 independent AWS clusters, with one broker node on i3.large and one client node on i3.large.
- Benchmark flow: run the producer for 10 minutes to generate test data, then run Kafka Streams configurations.
- Observed regression: the simplest Kafka Streams configuration is bounded by data-generator throughput, and investigation showed the data generator producer had regressed.
- The issue states numerous benchmark runs before the commit showed throughput around 115,000 records/sec.
- It also states 40 runs including and after the commit showed throughput around 105,000 records/sec.
- A trunk test with the commit reverted showed return to around 115,000 records/sec.

Configuration shown in Jira:

```
properties.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, broker);
properties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
properties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
```

Additional comment evidence:

2022-06-25 John Roesler:
- Setting the partitioner back to `DefaultPartitioner` did not help.
- Throughput of that test was `105k±2k` records/sec.

2022-07-12 John Roesler:
- The reporter reran the same benchmark after apache/kafka#12365.
- Baseline good performance at parent commit `e3202b9`: `118k±1k`.
- Fixed commit `3a6500b`: `117k±1k`.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 6 condition labels across 6 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] fix_validation_window: c23_kafka_producer_regression.throughput_value_records_per_second at confirmed_fixed, confidence=0.82
      Evidence: baseline/regressed/fixed or reverted conditions are present; compare the full regression window before attributing cause
  [2] release_resolution_metadata: c23_kafka_producer_regression.throughput_value_records_per_second at confirmed_fixed, confidence=0.74
      Evidence: version/release/fix labels are present; preserve introduced, regressed, reverted, fixed, or canary metadata alongside metric deltas
      baseline: baseline_pre_regression, confirmed_good_baseline
      regressed: regressed
      reverted: reverted
      fixed: confirmed_fixed
  [3] mechanism_evidence: c23_kafka_producer_regression.throughput_value_records_per_second at default_partitioner_test, confidence=0.72
      Evidence: named low-level mechanisms appear in the evidence; retain them as evidence labels without promoting them to root cause unless backed by profiling, bisection, or owner notes
      mechanisms: partitioner
  [4] condition_delta: c23_kafka_producer_regression.throughput_value_records_per_second at default_partitioner_test (105000.0 -> 118000.0), confidence=0.55
      Evidence: throughput_value_records_per_second changes across benchmark conditions; min=1.05e+05 at default_partitioner_test; max=1.18e+05 at confirmed_good_baseline; ratio=1.12x; compare conditions before explaining cause

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c23_kafka_producer_regression.throughput_value_records_per_second sits inside a baseline/regressed/fixed window; preserve fix validation before explaining cause.
  Option C: this is sparse benchmark evidence; preserve condition labels and deltas.
  Option C: fix/revert validation can be stronger than a single regression point.
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

KafkaProducer throughput under the benchmark workload regressed from roughly 115k records/sec to roughly 105k records/sec around the reported commit window, then returned near the prior level after revert/fix validation.

2. Evidence

- Public Jira evidence states many pre-regression runs were around 115,000 records/sec.
- Forty runs including and after the reported commit were around 105,000 records/sec, about a 10% drop.
- A trunk test with the commit reverted returned to around 115,000 records/sec.
- Setting the partitioner back to `DefaultPartitioner` did not restore throughput; that test remained about 105k +/- 2k records/sec.
- Later fix validation reports parent baseline `e3202b9` at 118k +/- 1k and fixed commit `3a6500b` at 117k +/- 1k.

3. Missing evidence

- Low-level producer-side metrics explaining what resource or code path changed, such as batching, request rate, serialization cost, CPU, allocation, or network waits.
- Full raw run table for the 40 regressed runs and pre-regression runs, including variance and environment stability.
- A direct profile comparison between the good, regressed, reverted, and fixed commits.

4. Recommended next diagnostic step

Run the same producer benchmark on the good parent, reported regressed commit, reverted trunk, and fixed PR commit, capturing producer metrics and CPU/allocation profiles. Compare throughput alongside batching/request/CPU indicators before attributing the regression to a specific producer mechanism.
```

## Verdict Review

```text
Winner: similar

Reason: Both outputs capture the 115k-to-105k records/sec regression, revert recovery, failed partitioner-only test, and fixed-commit validation. Baseline has slightly more release/PR metadata, while trace-on has cleaner caution about not attributing the mechanism without producer metrics or profiles.

Engine action: Preserve fix-lineage detection and add a release-resolution metadata slot, but keep requiring producer metrics/profiles before naming a specific producer mechanism.
```
