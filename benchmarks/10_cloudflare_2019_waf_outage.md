# Benchmark 10: cloudflare_2019_waf_outage

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
post_says_cpu_spiked_to_nearly_100_percent,c11_cloudflare_2019_waf_outage,cpu_utilization_peak_percent,100.0
reported_during_initial_response,c11_cloudflare_2019_waf_outage,traffic_lost_percent,80.0
post_says_http_https_went_offline_for_27_minutes,c11_cloudflare_2019_waf_outage,service_offline_duration_minutes,27.0
13_42_utc_deployment_decimal_hour,c11_cloudflare_2019_waf_outage,deploy_time_hour_utc,13.7
three_minutes_after_13_42_utc_deployment,c11_cloudflare_2019_waf_outage,first_page_time_hour_utc,13.75
waf_identified_as_cause,c11_cloudflare_2019_waf_outage,waf_identified_time_hour_utc,14.0
14_07_utc_global_waf_termination,c11_cloudflare_2019_waf_outage,global_waf_termination_time_hour_utc,14.1167
14_09_utc_traffic_and_cpu_back_to_expected_levels,c11_cloudflare_2019_waf_outage,traffic_cpu_recovered_time_hour_utc,14.15
14_52_utc_waf_re_enabled_globally,c11_cloudflare_2019_waf_outage,waf_reenabled_time_hour_utc,14.8667
post_incident_manual_inspection,c11_cloudflare_2019_waf_outage,waf_rules_inspected_count,3868.0
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
# c11 Cloudflare 2019 WAF outage

Source: https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/

Status: accepted

Raw performance evidence exists: yes. Cloudflare reports that a WAF Managed Rules update exhausted CPU on every HTTP/HTTPS-serving CPU core worldwide, with CPU spiking to nearly 100%, widespread 502s, and a reported loss of 80% of traffic during the incident.

Resolution evidence exists: yes. The post gives a concrete timeline: WAF identified as the cause at 14:00 UTC, global WAF termination executed at 14:07, traffic and CPU returned to expected levels by 14:09, and WAF was re-enabled globally at 14:52 after validation.

Normalization: feasible from visible incident timeline and numeric impact values. `normalized.csv` captures traffic loss, CPU saturation, and key response times.

RAW EVIDENCE:
Public source: https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/

Relevant raw performance evidence:

- Cloudflare says a new WAF Managed Rules rule exhausted CPU on every CPU core handling HTTP/HTTPS traffic worldwide.
- The post states CPU dedicated to serving HTTP/HTTPS traffic spiked to nearly 100% usage across the network.
- Customers saw 502 error pages when visiting Cloudflare domains.
- At 13:42 UTC, an engineer deployed a WAF XSS detection rules change.
- Three minutes later, the first PagerDuty page was sent for a WAF fault.
- Cloudflare received alerts for many end-to-end tests failing, a global traffic drop, widespread 502 errors, and CPU exhaustion reports.
- A leader told the author that Cloudflare had lost 80% of traffic.
- The post says Cloudflare's HTTP/HTTPS service was offline for 27 minutes.
- The outage was caused by a WAF regular expression with excessive backtracking.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
A WAF Managed Rules deployment caused global CPU exhaustion on HTTP/HTTPS-serving cores, producing widespread 502s and major traffic loss.

2. Evidence
- Cloudflare reports the new WAF rule exhausted CPU on every CPU core handling HTTP/HTTPS traffic worldwide.
- HTTP/HTTPS-serving CPU spiked to nearly 100% usage across the network.
- Customers saw 502 error pages.
- A leader reported Cloudflare had lost 80% of traffic.
- The HTTP/HTTPS service was offline for 27 minutes.
- Timeline: WAF change deployed at 13:42 UTC; first WAF fault page about three minutes later; WAF identified as cause at 14:00; global WAF termination at 14:07; traffic and CPU returned to expected levels by 14:09; WAF re-enabled globally at 14:52.
- The post attributes the outage to a WAF regular expression with excessive backtracking.

3. Missing evidence
- No per-datacenter CPU charts, request-rate/error-rate tables, or raw monitoring data in the provided evidence.
- No exact regex benchmark data or synthetic reproduction measurements.
- No granular breakdown of which traffic/classes were most affected.

4. Recommended next diagnostic step
Validate WAF rule performance before global rollout with regex backtracking tests, staged deployment, CPU/error-rate guardrails, and automatic rollback on global CPU or 502 spikes.
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
# c11 Cloudflare 2019 WAF outage

Source: https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/

Status: accepted

Raw performance evidence exists: yes. Cloudflare reports that a WAF Managed Rules update exhausted CPU on every HTTP/HTTPS-serving CPU core worldwide, with CPU spiking to nearly 100%, widespread 502s, and a reported loss of 80% of traffic during the incident.

Resolution evidence exists: yes. The post gives a concrete timeline: WAF identified as the cause at 14:00 UTC, global WAF termination executed at 14:07, traffic and CPU returned to expected levels by 14:09, and WAF was re-enabled globally at 14:52 after validation.

Normalization: feasible from visible incident timeline and numeric impact values. `normalized.csv` captures traffic loss, CPU saturation, and key response times.

RAW EVIDENCE:
Public source: https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/

Relevant raw performance evidence:

- Cloudflare says a new WAF Managed Rules rule exhausted CPU on every CPU core handling HTTP/HTTPS traffic worldwide.
- The post states CPU dedicated to serving HTTP/HTTPS traffic spiked to nearly 100% usage across the network.
- Customers saw 502 error pages when visiting Cloudflare domains.
- At 13:42 UTC, an engineer deployed a WAF XSS detection rules change.
- Three minutes later, the first PagerDuty page was sent for a WAF fault.
- Cloudflare received alerts for many end-to-end tests failing, a global traffic drop, widespread 502 errors, and CPU exhaustion reports.
- A leader told the author that Cloudflare had lost 80% of traffic.
- The post says Cloudflare's HTTP/HTTPS service was offline for 27 minutes.
- The outage was caused by a WAF regular expression with excessive backtracking.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 10 condition labels across 10 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] resource_saturation: c11_cloudflare_2019_waf_outage.cpu_utilization_peak_percent at post_says_cpu_spiked_to_nearly_100_percent, confidence=0.86
      Evidence: cpu_utilization_peak_percent is 100%, indicating CPU saturation
  [2] impact_window: c11_cloudflare_2019_waf_outage.service_offline_duration_minutes at post_says_http_https_went_offline_for_27_minutes, confidence=0.72
      Evidence: service_offline_duration_minutes is 27 minutes, indicating a sustained impact window
  [3] impact_spike: c11_cloudflare_2019_waf_outage.traffic_lost_percent at reported_during_initial_response, confidence=0.82
      Evidence: traffic_lost_percent is 80%, indicating material user-visible impact
  [4] mechanism_evidence: c11_cloudflare_2019_waf_outage.global_waf_termination_time_hour_utc at 14_07_utc_global_waf_termination, confidence=0.72
      Evidence: named low-level mechanisms appear in the evidence; retain them as evidence labels without promoting them to root cause unless backed by profiling, bisection, or owner notes
      mechanisms: termination

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c11_cloudflare_2019_waf_outage.cpu_utilization_peak_percent is the first visible shift.
  Option C: preserve named mechanisms as evidence labels, not automatic root cause.
  Option D: detector output is incomplete; request more metrics if evidence is thin.

GUARDRAIL:
  Do not turn timing into causality without dependency, deploy, or resource evidence.

Return concise structured findings.
```

## Trace-On Response

```text
## Performance issue
A WAF Managed Rules update caused global HTTP/HTTPS serving capacity to fail, producing CPU saturation, widespread 502s, and major traffic loss.

## Evidence
- Cloudflare reports CPU dedicated to HTTP/HTTPS traffic spiked to nearly 100% across the network.
- Trace flags resource saturation at 100% CPU utilization.
- Customers saw 502 error pages across Cloudflare domains.
- A leader reported that Cloudflare had lost 80% of traffic; trace flags this as material user-visible impact.
- The HTTP/HTTPS service was offline for 27 minutes; trace flags this as a sustained impact window.
- Timeline evidence: WAF rules change deployed at 13:42 UTC, first WAF fault page about three minutes later, WAF identified as cause at 14:00, global WAF termination at 14:07, and traffic/CPU back to expected levels by 14:09.
- Public writeup attributes the outage to a WAF regular expression with excessive backtracking.

## Missing evidence
- Per-datacenter CPU, request, and 502 time series before and after the WAF rule deploy.
- Rule-level profiling showing regex evaluation cost under production traffic.
- Validation results from staging or canary systems before global deployment.
- Independent evidence tying each impacted service symptom directly to CPU exhaustion.

## Recommended next diagnostic step
Replay representative production-like traffic against the deployed WAF rule set with regex-level CPU profiling, then verify canary and rollout controls would have detected the near-100% CPU saturation before global propagation.
```

## Verdict Review

```text
Winner: similar

Concise reason: Both outputs capture the core WAF deployment, near-100% CPU saturation, 502s, 80% traffic loss, 27-minute impact window, and excessive regex backtracking explanation. Trace-on adds structured impact labels but does not materially change the review.

Engine action: No major engine change. Resource-saturation plus impact-window detection is working adequately here; optional improvement is to recognize deploy-to-saturation-to-error incident timelines as a stronger cascade.
```
