# A/B Report: `c08_ray_tune_utilization_collapse`

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
ray_tune_workload,c08_ray_tune_utilization_collapse,total_worker_cpus_count,32.0
after_about_1100_completed_trials,c08_ray_tune_utilization_collapse,busy_worker_cpus_after_degradation_count,6.0
6_busy_cpus_out_of_32_total_derived_from_visible_counts,c08_ray_tune_utilization_collapse,worker_utilization_after_degradation_percent,18.75
reporter_says_less_than_25_percent_busy,c08_ray_tune_utilization_collapse,reported_utilization_upper_bound_percent,25.0
approximate_threshold_reported_by_issue_author,c08_ray_tune_utilization_collapse,completed_trials_at_degradation_count,1100.0
total_grid_search_trials,c08_ray_tune_utilization_collapse,trial_count_total_count,19440.0
tune_status_line_at_degradation,c08_ray_tune_utilization_collapse,trial_count_pending_count,1000.0
tune_status_line_at_degradation,c08_ray_tune_utilization_collapse,trial_count_running_count,32.0
tune_status_line_at_degradation,c08_ray_tune_utilization_collapse,trial_count_terminated_count,1898.0
issue_problem_statement,c08_ray_tune_utilization_collapse,gcs_log_size_initial_report_gb,16.0
approximate_lines_in_gcs_server_out,c08_ray_tune_utilization_collapse,gcs_log_lines_count,89000000.0
minimal_reproduction_section,c08_ray_tune_utilization_collapse,gcs_log_size_reproduction_gb,22.0
warning_sample,c08_ray_tune_utilization_collapse,choose_trial_to_run_warning_1_s,0.513
warning_sample,c08_ray_tune_utilization_collapse,choose_trial_to_run_warning_2_s,0.626
warning_sample,c08_ray_tune_utilization_collapse,choose_trial_to_run_warning_3_s,0.521
warning_sample,c08_ray_tune_utilization_collapse,choose_trial_to_run_warning_4_s,0.626
warning_sample,c08_ray_tune_utilization_collapse,choose_trial_to_run_warning_5_s,0.611
warning_sample,c08_ray_tune_utilization_collapse,choose_trial_to_run_warning_6_s,0.532
warning_sample,c08_ray_tune_utilization_collapse,choose_trial_to_run_warning_7_s,0.719
warning_sample,c08_ray_tune_utilization_collapse,choose_trial_to_run_warning_8_s,0.541
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
# c08 Ray Tune utilization collapse

Source: https://github.com/ray-project/ray/issues/15504

Status: accepted

Raw performance evidence exists: yes. The issue body reports a reproducible Ray Tune scheduling degradation: 32 worker CPUs are initially fully utilized, then after about 1100 completed trials only about 6 worker CPUs remain busy while Tune reports 32 running trials. It also includes warning log timings for `choose_trial_to_run` around 0.5-0.7 s and GCS log growth to 16-22 GB.

Resolution evidence exists: yes. The public issue is closed as completed, and the fix PR, https://github.com/ray-project/ray/pull/15811, is merged. Its title is "[tune] Track live trials in a set in the TrialRunner to reduce linear scans"; its body says it closes #15504 and explains that Ray Tune was scanning all trials several times on each `TrialRunner.step()` invocation.

Normalization: feasible for the visible numeric evidence from the issue body. `normalized.csv` captures the reported worker utilization collapse, trial-count context, log size, and warning latency samples.

RAW EVIDENCE:
Public source: https://github.com/ray-project/ray/issues/15504

Relevant raw performance evidence from the issue body:

- Workload: grid search of 19440 Ray Tune trials using FIFOScheduler and default search_alg with 32 worker CPUs.
- Initial behavior: first few minutes show 100% worker utilization.
- Regression behavior: after about 1100 completed trials, only about 6 worker CPUs are busy while Tune logs "Number of trials: 2930/19440 (1000 PENDING, 32 RUNNING, 1898 TERMINATED)".
- The reporter summarizes this as scheduling keeping less than 25% of worker CPUs busy.
- GCS logging evidence: `gcs_server.out` is reported as 16 GB and filled with about 89 million placement-group scheduling lines; the reproduction section reports `gcs_server.out` of 22 GB.
- Warning samples from the reproduction:
  - 2021-04-26 12:20:16 choose_trial_to_run took 0.513 s
  - 2021-04-26 12:20:16 choose_trial_to_run took 0.626 s
  - 2021-04-26 12:20:17 choose_trial_to_run took 0.521 s
  - 2021-04-26 12:20:18 choose_trial_to_run took 0.626 s
  - 2021-04-26 12:20:18 choose_trial_to_run took 0.611 s
  - 2021-04-26 12:20:19 choose_trial_to_run took 0.532 s
  - 2021-04-26 12:20:20 choose_trial_to_run took 0.719 s
  - 2021-04-26 12:20:20 choose_trial_to_run took 0.541 s

Environment stated by reporter:
- Ubuntu 20.04
- Python 3.8.8
- Ray 1.3.0

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
Ray Tune scheduling throughput collapses during a large grid search: workers start fully utilized, then most CPUs become idle even though Tune reports many running trials.

2. Evidence
- Workload: 19,440 trials, FIFOScheduler/default search algorithm, 32 worker CPUs.
- Initial state: 100% worker utilization for the first few minutes.
- After about 1,100 completed trials, only about 6 of 32 worker CPUs remain busy while Tune reports 32 running trials.
- Reporter summarizes utilization as below 25%.
- `choose_trial_to_run` warning samples take about 0.513-0.719 s.
- GCS logs grow to 16-22 GB, including about 89 million placement-group scheduling lines.
- Resolution PR says TrialRunner was scanning all trials several times per `step()` and fixes this by tracking live trials in a set.

3. Missing evidence
- No end-to-end before/after benchmark numbers from the merged fix in the provided evidence.
- No flamegraph or scheduler CPU profile from the failing run.
- No precise timeline tying log growth, trial count, and worker idleness second by second.

4. Recommended next diagnostic step
Reproduce on Ray 1.3.0 and a fixed version with scheduler profiling enabled, then compare `TrialRunner.step()`/`choose_trial_to_run` time, worker utilization, and GCS log growth across completed-trial counts.
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
# c08 Ray Tune utilization collapse

Source: https://github.com/ray-project/ray/issues/15504

Status: accepted

Raw performance evidence exists: yes. The issue body reports a reproducible Ray Tune scheduling degradation: 32 worker CPUs are initially fully utilized, then after about 1100 completed trials only about 6 worker CPUs remain busy while Tune reports 32 running trials. It also includes warning log timings for `choose_trial_to_run` around 0.5-0.7 s and GCS log growth to 16-22 GB.

Resolution evidence exists: yes. The public issue is closed as completed, and the fix PR, https://github.com/ray-project/ray/pull/15811, is merged. Its title is "[tune] Track live trials in a set in the TrialRunner to reduce linear scans"; its body says it closes #15504 and explains that Ray Tune was scanning all trials several times on each `TrialRunner.step()` invocation.

Normalization: feasible for the visible numeric evidence from the issue body. `normalized.csv` captures the reported worker utilization collapse, trial-count context, log size, and warning latency samples.

RAW EVIDENCE:
Public source: https://github.com/ray-project/ray/issues/15504

Relevant raw performance evidence from the issue body:

- Workload: grid search of 19440 Ray Tune trials using FIFOScheduler and default search_alg with 32 worker CPUs.
- Initial behavior: first few minutes show 100% worker utilization.
- Regression behavior: after about 1100 completed trials, only about 6 worker CPUs are busy while Tune logs "Number of trials: 2930/19440 (1000 PENDING, 32 RUNNING, 1898 TERMINATED)".
- The reporter summarizes this as scheduling keeping less than 25% of worker CPUs busy.
- GCS logging evidence: `gcs_server.out` is reported as 16 GB and filled with about 89 million placement-group scheduling lines; the reproduction section reports `gcs_server.out` of 22 GB.
- Warning samples from the reproduction:
  - 2021-04-26 12:20:16 choose_trial_to_run took 0.513 s
  - 2021-04-26 12:20:16 choose_trial_to_run took 0.626 s
  - 2021-04-26 12:20:17 choose_trial_to_run took 0.521 s
  - 2021-04-26 12:20:18 choose_trial_to_run took 0.626 s
  - 2021-04-26 12:20:18 choose_trial_to_run took 0.611 s
  - 2021-04-26 12:20:19 choose_trial_to_run took 0.532 s
  - 2021-04-26 12:20:20 choose_trial_to_run took 0.719 s
  - 2021-04-26 12:20:20 choose_trial_to_run took 0.541 s

Environment stated by reporter:
- Ubuntu 20.04
- Python 3.8.8
- Ray 1.3.0

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 11 condition labels across 20 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] control_plane_accumulation: c08_ray_tune_utilization_collapse.trial_count_total_count at total_grid_search_trials, confidence=0.8
      Evidence: trial-count and low-utilization evidence appear together; inspect scheduler/control-plane work accumulating with completed or pending tasks
  [2] phased_remediation: c08_ray_tune_utilization_collapse.choose_trial_to_run_warning_8_s at warning_sample, confidence=0.74
      Evidence: multiple after/post-remediation stages are present; preserve staged fixes and residual bottlenecks instead of collapsing to one before/after delta
  [3] capacity_underuse: c08_ray_tune_utilization_collapse.worker_utilization_after_degradation_percent at 6_busy_cpus_out_of_32_total_derived_from_visible_counts, confidence=0.78
      Evidence: worker_utilization_after_degradation_percent is 18.75%, indicating low resource use despite active work
  [4] capacity_underuse: c08_ray_tune_utilization_collapse.reported_utilization_upper_bound_percent at reporter_says_less_than_25_percent_busy, confidence=0.78
      Evidence: reported_utilization_upper_bound_percent is 25%, indicating low resource use despite active work

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c08_ray_tune_utilization_collapse.trial_count_total_count is the first visible shift.
  Option D: detector output is incomplete; request more metrics if evidence is thin.

GUARDRAIL:
  Do not turn timing into causality without dependency, deploy, or resource evidence.

Return concise structured findings.
```

## Trace-On Response

```text
## 1. Performance Issue

Ray Tune scheduling/control-plane degradation during a large grid search. Worker CPU utilization collapses after many completed trials even though Tune still reports active running trials.

## 2. Evidence

- Workload has 19,440 grid-search trials and 32 worker CPUs.
- Initial utilization is reported as 100% for the first few minutes.
- After about 1,100 completed trials, only about 6 of 32 worker CPUs remain busy while Tune reports 32 running trials.
- The issue body reports less than 25% worker utilization during the degraded phase; the trace derives 18.75% from 6/32 busy CPUs.
- Warning samples show `choose_trial_to_run` taking about 0.5-0.7 seconds repeatedly.
- GCS logs grew to 16-22 GB with tens of millions of placement-group scheduling lines.
- Resolution evidence says the merged fix reduced linear scans by tracking live trials in a set, but this supports the accepted fix rather than independently proving every causal link.

## 3. Missing Evidence

- Time series linking trial count, completed trials, scheduler step latency, pending/running counts, and worker utilization.
- CPU profiles for the Ray driver/scheduler during the degraded phase.
- Breakdown of time spent in `TrialRunner.step()` and `choose_trial_to_run`.
- Confirmation that workers were idle due to scheduler delay rather than task execution, placement, or resource constraints.

## 4. Recommended Next Diagnostic Step

Reproduce the large grid search with scheduler profiling enabled and record worker utilization, scheduler-loop latency, trial-state counts, and GCS activity over time. Verify whether scheduler scans grow with total trials and whether the live-trial set change removes the utilization collapse.
```

## Verdict Review

```text
Winner: trace-on

Reason: Trace-on preserves the key collapse evidence, adds the derived 18.75% utilization signal, and is more careful that the live-trial-set PR supports the accepted fix without independently proving every causal link. It keeps the scheduler/control-plane hypothesis framed at the right confidence.

Engine action: Keep the capacity-underuse plus control-plane-accumulation route; add a scheduler-loop scaling detector that links completed-trial count, scheduler scan cost, and worker idleness when those metrics co-occur.
```
