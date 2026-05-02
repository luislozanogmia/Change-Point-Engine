# A/B Report: `c13_github_jan_2025_db_query`

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
01_26_utc_start,c13_github_jan_2025_db_query,start_time_hour_utc,1.4333
01_56_utc_end,c13_github_jan_2025_db_query,end_time_hour_utc,1.9333
reported_incident_duration,c13_github_jan_2025_db_query,duration_minutes,31.0
average_error_rate_of_update_requests,c13_github_jan_2025_db_query,average_error_rate_percent,6.0
peak_error_rate_of_update_requests,c13_github_jan_2025_db_query,peak_error_rate_percent,6.85
time_to_find_errant_query,c13_github_jan_2025_db_query,time_from_engagement_to_query_identified_minutes,14.0
context_incident_in_same_report,c13_github_jan_2025_db_query,duration_minutes,49.0
context_incident_in_same_report,c13_github_jan_2025_db_query,duration_minutes,26.0
context_incident_peak_error_rate,c13_github_jan_2025_db_query,peak_error_rate_percent,44.0
report_says_over_three_seconds,c13_github_jan_2025_db_query,average_successful_request_latency_lower_bound_s,3.0
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
# c13 GitHub January 2025 availability DB query

Source: https://github.blog/news-insights/company-news/github-availability-report-january-2025/

Status: accepted

Raw performance evidence exists: yes. The January 9 incident report states that GitHub returned 500 responses across many services because a deployment introduced a query that saturated a primary database server. The average error rate was 6%, peaking at 6.85% of update requests.

Resolution evidence exists: yes. GitHub says it mitigated by identifying the problematic query and rolling back the deployment, with 14 minutes from engagement to finding the errant query.

Normalization: feasible from visible incident values. `normalized.csv` captures the January 9 case values and includes the other visible January incidents for context.

RAW EVIDENCE:
Public source: https://github.blog/news-insights/company-news/github-availability-report-january-2025/

Relevant raw performance evidence:

- January 9, 2025, 01:26-01:56 UTC: GitHub experienced widespread disruption to many services.
- Users received 500 responses when trying to access various functionality.
- The cause was a deployment that introduced a query saturating a primary database server.
- Average error rate was 6%.
- Peak error rate was 6.85% of update requests.
- The incident lasted 31 minutes.

Additional context in the same availability report:

- January 13 incident lasted 49 minutes and made all Git operations unavailable due to an internal load-balancer request-dropping configuration change.
- January 30 incident lasted 26 minutes; web requests peaked at 44% error rate, and successful requests averaged over 3 seconds.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
GitHub experienced a 31-minute availability incident on 2025-01-09 where many services returned 500 responses after a deployment introduced a database query that saturated a primary database server.

2. Evidence
- Incident window: 01:26-01:56 UTC.
- Disruption was widespread across many services.
- Users received HTTP 500 responses across affected functionality.
- Average error rate was 6%.
- Peak error rate was 6.85% of update requests.
- GitHub identified the problematic query and rolled back the deployment; the errant query was found 14 minutes after engagement.

3. Missing evidence
- Query text, query plan, row counts, lock/wait profile, and database saturation metrics.
- Per-service error rates and traffic volume during the incident.
- Deployment diff and whether query load was predicted in staging or canary.
- Recovery timeline after rollback by service.

4. Recommended next diagnostic step
Analyze database telemetry around 01:26-01:56 UTC, especially the deployed query's execution plan, CPU/I/O/lock waits, and call volume, then compare it with pre-deployment baselines to validate why the primary database saturated.
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
# c13 GitHub January 2025 availability DB query

Source: https://github.blog/news-insights/company-news/github-availability-report-january-2025/

Status: accepted

Raw performance evidence exists: yes. The January 9 incident report states that GitHub returned 500 responses across many services because a deployment introduced a query that saturated a primary database server. The average error rate was 6%, peaking at 6.85% of update requests.

Resolution evidence exists: yes. GitHub says it mitigated by identifying the problematic query and rolling back the deployment, with 14 minutes from engagement to finding the errant query.

Normalization: feasible from visible incident values. `normalized.csv` captures the January 9 case values and includes the other visible January incidents for context.

RAW EVIDENCE:
Public source: https://github.blog/news-insights/company-news/github-availability-report-january-2025/

Relevant raw performance evidence:

- January 9, 2025, 01:26-01:56 UTC: GitHub experienced widespread disruption to many services.
- Users received 500 responses when trying to access various functionality.
- The cause was a deployment that introduced a query saturating a primary database server.
- Average error rate was 6%.
- Peak error rate was 6.85% of update requests.
- The incident lasted 31 minutes.

Additional context in the same availability report:

- January 13 incident lasted 49 minutes and made all Git operations unavailable due to an internal load-balancer request-dropping configuration change.
- January 30 incident lasted 26 minutes; web requests peaked at 44% error rate, and successful requests averaged over 3 seconds.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 9 condition labels across 10 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] impact_window: c13_github_jan_2025_db_query.duration_minutes at context_incident_in_same_report, confidence=0.72
      Evidence: duration_minutes is 49 minutes, indicating a sustained impact window
  [2] impact_window: c13_github_jan_2025_db_query.duration_minutes at context_incident_in_same_report, confidence=0.72
      Evidence: duration_minutes is 26 minutes, indicating a sustained impact window
  [3] database_error_incident: c13_github_jan_2025_db_query.peak_error_rate_percent at context_incident_peak_error_rate, confidence=0.76
      Evidence: database/query labels appear with error-rate evidence; inspect deployment/query saturation as a candidate incident structure
  [4] impact_window: c13_github_jan_2025_db_query.duration_minutes at reported_incident_duration, confidence=0.72
      Evidence: duration_minutes is 31 minutes, indicating a sustained impact window
  [5] condition_delta: c13_github_jan_2025_db_query.duration_minutes at context_incident_in_same_report (26.0 -> 49.0), confidence=0.75
      Evidence: duration_minutes changes across benchmark conditions; min=26 at context_incident_in_same_report; max=49 at context_incident_in_same_report; ratio=1.88x; compare conditions before explaining cause
  [6] condition_delta: c13_github_jan_2025_db_query.peak_error_rate_percent at peak_error_rate_of_update_requests (6.85 -> 44.0), confidence=0.95
      Evidence: peak_error_rate_percent changes across benchmark conditions; min=6.85 at peak_error_rate_of_update_requests; max=44 at context_incident_peak_error_rate; ratio=6.42x; compare conditions before explaining cause
  [7] event_presence: c13_github_jan_2025_db_query.average_error_rate_percent at average_error_rate_of_update_requests, confidence=0.68
      Evidence: average_error_rate_percent is non-zero (6); preserve as event evidence
  [8] event_presence: c13_github_jan_2025_db_query.peak_error_rate_percent at context_incident_peak_error_rate, confidence=0.68
      Evidence: peak_error_rate_percent is non-zero (44); preserve as event evidence
  [9] event_presence: c13_github_jan_2025_db_query.peak_error_rate_percent at peak_error_rate_of_update_requests, confidence=0.68
      Evidence: peak_error_rate_percent is non-zero (6.85); preserve as event evidence

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c13_github_jan_2025_db_query.duration_minutes is the first visible shift.
  Option C: this is sparse benchmark evidence; preserve condition labels and deltas.
  Option D: detector output is incomplete; request more metrics if evidence is thin.

GUARDRAIL:
  Do not turn timing into causality without dependency, deploy, or resource evidence.

Return concise structured findings.
```

## Trace-On Response

```text
## 1. Performance Issue

GitHub availability incident with elevated 500 responses across many services during a 31-minute window on January 9, 2025, associated in the public report with a deployment-introduced database query saturating a primary database server.

## 2. Evidence

- Incident window: January 9, 2025, 01:26-01:56 UTC, lasting 31 minutes.
- Users received 500 responses across various functionality.
- Reported average error rate was 6%.
- Reported peak error rate was 6.85% of update requests.
- Public resolution says GitHub identified the problematic query and rolled back the deployment, with 14 minutes from engagement to finding the query.
- The trace preserves this as sparse incident evidence and warns not to overread condition deltas from other January incidents.

## 3. Missing Evidence

- Query text, execution plan, lock/wait profile, and database saturation metrics.
- Per-service error rates and request-volume denominators.
- Deployment timeline relative to the first errors.
- Database CPU, I/O, connection, queue, and replication metrics during the incident.
- Evidence separating the January 9 database-query incident from other January incidents in the same report.

## 4. Recommended Next Diagnostic Step

Correlate the January 9 deployment timeline with database telemetry and request error time series. Inspect the deployed query plan, primary database saturation metrics, and rollback timing to confirm the mechanism and blast radius.
```

## Verdict Review

```text
Winner: trace-on

Reason: Trace-on keeps the January 9 incident details intact while explicitly separating this database-query incident from other January incidents in the same report. That is better than baseline because the trace contained mixed sparse incident evidence and trace-on avoids overreading cross-incident condition deltas.

Engine action: Strengthen incident-window/entity disambiguation for co-reported outages so detector output groups metrics by exact date, incident, and affected system before producing deltas.
```
