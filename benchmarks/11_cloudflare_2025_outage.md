# Benchmark 11: cloudflare_2025_outage

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
11_05_utc_database_access_control_change_deployed,c12_cloudflare_2025_outage,database_change_time_hour_utc,11.0833
11_20_utc_significant_failures_began,c12_cloudflare_2025_outage,network_failure_start_hour_utc,11.3333
11_28_utc_first_customer_http_errors,c12_cloudflare_2025_outage,impact_start_hour_utc,11.4667
11_31_utc_first_automated_test_detected_issue,c12_cloudflare_2025_outage,first_automated_detection_hour_utc,11.5167
11_32_utc_manual_investigation_started,c12_cloudflare_2025_outage,manual_investigation_start_hour_utc,11.5333
11_35_utc_incident_call_created,c12_cloudflare_2025_outage,incident_call_created_hour_utc,11.5833
query_generated_feature_file_every_five_minutes,c12_cloudflare_2025_outage,feature_file_generation_interval_minutes,5.0
feature_file_doubled_in_size,c12_cloudflare_2025_outage,feature_file_size_multiplier_x,2.0
bot_management_runtime_feature_limit,c12_cloudflare_2025_outage,feature_limit_count,200.0
current_feature_use_described_as_about_60_features,c12_cloudflare_2025_outage,normal_feature_count_count,60.0
13_04_utc_workers_kv_bypass_patch,c12_cloudflare_2025_outage,workers_kv_bypass_time_hour_utc,13.0667
13_05_utc_kv_and_access_bypass_implemented,c12_cloudflare_2025_outage,impact_reduced_time_hour_utc,13.0833
13_37_utc_rollback_focus,c12_cloudflare_2025_outage,rollback_focus_time_hour_utc,13.6167
14_24_utc_stopped_bad_file_generation_and_propagation,c12_cloudflare_2025_outage,bad_file_generation_stopped_hour_utc,14.4
14_30_utc_main_impact_resolved,c12_cloudflare_2025_outage,main_impact_resolved_hour_utc,14.5
17_06_utc_all_operations_fully_restored,c12_cloudflare_2025_outage,all_services_resolved_hour_utc,17.1
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
# c12 Cloudflare 2025 outage

Source: https://blog.cloudflare.com/18-november-2025-outage/

Status: accepted

Raw performance evidence exists: yes. Cloudflare reports significant failures beginning at 11:20 UTC, HTTP 5xx spikes, increased CDN latency, Workers KV elevated 5xx errors, Access authentication failures, and Turnstile/dashboard availability impacts. The post identifies a doubled Bot Management feature file and a 200-feature runtime limit as the proximate failure mode.

Resolution evidence exists: yes. Cloudflare stopped bad feature-file generation and propagation, inserted a known-good file, restarted the core proxy, restored main impact at 14:30, and had all systems functioning normally by 17:06.

Normalization: feasible from visible timeline and numeric limits. `normalized.csv` captures the incident timeline and explicit numeric values.

RAW EVIDENCE:
Public source: https://blog.cloudflare.com/18-november-2025-outage/

Relevant raw performance evidence:

- At 11:20 UTC on 2025-11-18, Cloudflare's network began experiencing significant failures to deliver core network traffic.
- Users saw an error page indicating a failure within Cloudflare's network.
- The incident produced a spike in HTTP 5xx status codes served by the Cloudflare network.
- The feature file used by Bot Management doubled in size after a database permissions change caused duplicate rows.
- The feature-file generation query ran every five minutes, producing alternating good/bad configuration files during rollout.
- The Bot Management runtime limit was 200 features, while current use was about 60 features; the bad file exceeded the 200-feature limit.
- Impacted services included core CDN/security services, Turnstile, Workers KV, Dashboard, Email Security, and Access.
- Cloudflare also observed significant increases in CDN response latency during the impact period.
- Turnstile/dashboard availability impact appeared during 11:30-13:10 and 14:40-15:30 windows.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
Cloudflare had a broad availability and latency incident beginning at 11:20 UTC on 2025-11-18, affecting core traffic delivery and several dependent products.

2. Evidence
- HTTP 5xx responses spiked across the Cloudflare network.
- CDN response latency increased significantly during the impact period.
- Workers KV saw elevated 5xx errors; Access, Turnstile, dashboard, Email Security, and core CDN/security services were impacted.
- The Bot Management feature file doubled after a database permissions change produced duplicate rows.
- The bad file exceeded the Bot Management runtime limit of 200 features; normal use was about 60 features.
- Generation ran every five minutes, creating alternating good and bad configuration files during rollout.
- Cloudflare restored main impact by 14:30 UTC and all systems by 17:06 UTC after stopping bad generation, inserting a known-good file, and restarting core proxy components.

3. Missing evidence
- Exact 5xx rates, request volumes, and latency percentiles by service/region.
- The specific database permission change details and validation gaps.
- Runtime failure logs showing how exceeding the 200-feature limit translated into request failures.
- Blast-radius data for each product and customer segment.

4. Recommended next diagnostic step
Correlate feature-file versions and propagation timestamps with per-service 5xx/latency metrics and Bot Management runtime logs to confirm the exact failure path and identify where rollout validation should have blocked the oversized file.
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
# c12 Cloudflare 2025 outage

Source: https://blog.cloudflare.com/18-november-2025-outage/

Status: accepted

Raw performance evidence exists: yes. Cloudflare reports significant failures beginning at 11:20 UTC, HTTP 5xx spikes, increased CDN latency, Workers KV elevated 5xx errors, Access authentication failures, and Turnstile/dashboard availability impacts. The post identifies a doubled Bot Management feature file and a 200-feature runtime limit as the proximate failure mode.

Resolution evidence exists: yes. Cloudflare stopped bad feature-file generation and propagation, inserted a known-good file, restarted the core proxy, restored main impact at 14:30, and had all systems functioning normally by 17:06.

Normalization: feasible from visible timeline and numeric limits. `normalized.csv` captures the incident timeline and explicit numeric values.

RAW EVIDENCE:
Public source: https://blog.cloudflare.com/18-november-2025-outage/

Relevant raw performance evidence:

- At 11:20 UTC on 2025-11-18, Cloudflare's network began experiencing significant failures to deliver core network traffic.
- Users saw an error page indicating a failure within Cloudflare's network.
- The incident produced a spike in HTTP 5xx status codes served by the Cloudflare network.
- The feature file used by Bot Management doubled in size after a database permissions change caused duplicate rows.
- The feature-file generation query ran every five minutes, producing alternating good/bad configuration files during rollout.
- The Bot Management runtime limit was 200 features, while current use was about 60 features; the bad file exceeded the 200-feature limit.
- Impacted services included core CDN/security services, Turnstile, Workers KV, Dashboard, Email Security, and Access.
- Cloudflare also observed significant increases in CDN response latency during the impact period.
- Turnstile/dashboard availability impact appeared during 11:30-13:10 and 14:40-15:30 windows.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 16 condition labels across 16 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] release_resolution_metadata: c12_cloudflare_2025_outage.rollback_focus_time_hour_utc at 13_37_utc_rollback_focus, confidence=0.74
      Evidence: version/release/fix labels are present; preserve introduced, regressed, reverted, fixed, or canary metadata alongside metric deltas
      rollback: 13_37_utc_rollback_focus
  [2] mechanism_evidence: c12_cloudflare_2025_outage.feature_limit_count at bot_management_runtime_feature_limit, confidence=0.72
      Evidence: named low-level mechanisms appear in the evidence; retain them as evidence labels without promoting them to root cause unless backed by profiling, bisection, or owner notes
      mechanisms: runtime
  [3] config_expansion: c12_cloudflare_2025_outage.feature_file_size_multiplier_x at feature_file_doubled_in_size, confidence=0.78
      Evidence: feature_file_size_multiplier_x is 2x, indicating a material expansion/change in generated configuration

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c12_cloudflare_2025_outage.rollback_focus_time_hour_utc has release/fix lineage; preserve versions, revert, fixed, and canary labels before explaining cause.
  Option C: preserve named mechanisms as evidence labels, not automatic root cause.
  Option C: release/fix metadata can be the strongest resolution evidence.
  Option D: detector output is incomplete; request more metrics if evidence is thin.

GUARDRAIL:
  Do not turn timing into causality without dependency, deploy, or resource evidence.

Return concise structured findings.
```

## Trace-On Response

```text
## Performance issue
Cloudflare experienced a broad core-network outage with HTTP 5xx spikes, elevated CDN latency, and multiple service impacts after Bot Management feature-file generation produced oversized bad configuration files.

## Evidence
- Significant failures began at 11:20 UTC on 2025-11-18.
- Users saw Cloudflare network error pages.
- The incident produced HTTP 5xx spikes and significant CDN response-latency increases.
- Impacted services included core CDN/security services, Turnstile, Workers KV, Dashboard, Email Security, and Access.
- Public evidence says the Bot Management feature file doubled in size after a database permissions change caused duplicate rows.
- The generation query ran every five minutes and produced alternating good/bad files during rollout.
- The runtime feature limit was 200 features; normal use was about 60 features, and the bad file exceeded the 200-feature limit.
- Trace flags the 2x feature-file expansion as the visible configuration-change signal, but this is structured evidence rather than standalone proof.
- Main impact was restored at 14:30 and all systems were functioning normally by 17:06.

## Missing evidence
- Exact feature counts and file sizes for good versus bad generated files.
- Per-service error-rate and latency timelines aligned to feature-file propagation.
- Runtime logs showing where the >200-feature limit failed and how that produced each symptom.
- Validation coverage showing why duplicate rows and oversized feature files were not rejected before rollout.

## Recommended next diagnostic step
Reconstruct the feature-file generation and propagation timeline, validate exact good/bad feature counts against the 200-feature runtime limit, and correlate those transitions with service-level 5xx and latency metrics.
```

## Verdict Review

```text
Winner: trace-on

Concise reason: Trace-on cleanly ties the broad outage to the Bot Management feature-file expansion, duplicate rows, five-minute generation cadence, and 200-feature runtime limit while preserving uncertainty around proof.

Engine action: Keep config-expansion detection. Add follow-up prompt language for generated artifact validation: exact good/bad artifact size, runtime limit breach, and propagation timeline correlation.
```
