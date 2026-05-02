# Benchmark 14: openshift_kubelet_regression

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
baseline_low,c15_openshift_kubelet_regression,kubelet_cpu_usage_percent,20.0
baseline_high,c15_openshift_kubelet_regression,kubelet_cpu_usage_percent,25.0
regressed_low,c15_openshift_kubelet_regression,kubelet_cpu_usage_percent_higher,30.0
regressed_high,c15_openshift_kubelet_regression,kubelet_cpu_usage_percent_higher,35.0
regressed,c15_openshift_kubelet_regression,kubelet_cpu_orion_changepoint_value,34.879
regressed,c15_openshift_kubelet_regression,kubelet_cpu_orion_delta_delta,29.1073
baseline,c15_openshift_kubelet_regression,pod_ready_latency_ms,2000.0
regressed,c15_openshift_kubelet_regression,pod_ready_latency_ms,3000.0
regressed,c15_openshift_kubelet_regression,pod_ready_latency_delta_percent,50.0
getallocationpods,c15_openshift_kubelet_regression,pprof_cpu_time_percent,15.0
after_fix,c15_openshift_kubelet_regression,kubelet_cpu_usage_percent,25.0
after_fix,c15_openshift_kubelet_regression,pod_ready_latency_ms,2000.0
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
# c15 OpenShift kubelet regression

Source: https://developers.redhat.com/articles/2025/10/20/case-study-kubelet-regression-openshift

Status: accepted.

The Red Hat article is a public case study of a kubelet performance regression detected in OpenShift CI. Raw performance evidence is visible through Orion changepoint tables, CI/prow run links, pprof discussion, and summary measurements: kubelet 1.33 showed about 30-35% higher CPU usage and pod readiness latency around 3000 ms versus kubelet 1.32.6 baseline around 20-25% CPU and 2000 ms latency. Resolution evidence is visible because the article identifies an upstream patch reverting PR #130796 and says follow-up runs normalized CPU to about 25%, latency to about 2000 ms, and showed no changepoints across multiple nightly builds.

Normalized CSV feasibility: feasible from the article's visible summary and changepoint numbers.

RAW EVIDENCE:
Public source checked:
https://developers.redhat.com/articles/2025/10/20/case-study-kubelet-regression-openshift

Raw performance evidence confirmed:
- OpenShift 4.20 scale tests on a 6-node control plane cluster detected a 30% increase in kubelet CPU usage and a 50% increase in pod readiness latency.
- Kubelet 1.33 reproduced the regression; rolling back to kubelet 1.32.6 restored normal performance.
- Article summary: kubelet 1.33 CPU usage was about 30-35% higher; kubelet 1.32.6 returned to about 20-25% baseline.
- Article summary: pod readiness latency was about 3000 ms with kubelet 1.33 and about 2000 ms with kubelet 1.32.6.
- Orion CPU changepoint table includes value 34.879 with delta 29.1073 at build 1945711780562997248.
- Orion pod-ready-latency table includes 2000 ms before and 3000 ms at the changepoint, delta 50.
- Profiling attributed about 15% additional CPU time to the new getAllocationPods() path.

No extra numeric rows were inferred beyond what is visible in the article.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
OpenShift CI detected a kubelet regression in OpenShift 4.20 scale tests: kubelet 1.33 used more CPU and increased pod readiness latency versus kubelet 1.32.6.

2. Evidence
- Scale tests on a six-node control-plane cluster showed about 30% higher kubelet CPU and 50% higher pod readiness latency.
- Kubelet 1.33 CPU was about 30-35%, compared with a kubelet 1.32.6 baseline of about 20-25%.
- Pod readiness latency was about 3000 ms with kubelet 1.33 versus about 2000 ms with kubelet 1.32.6.
- Orion CPU changepoint table reported value 34.879 with delta 29.1073 at build 1945711780562997248.
- Orion pod-ready-latency changepoint showed 2000 ms before and 3000 ms at the changepoint, delta 50.
- Profiling attributed about 15% additional CPU time to the new `getAllocationPods()` path.
- Follow-up runs after reverting upstream PR #130796 normalized CPU to about 25% and latency to about 2000 ms, with no changepoints across multiple nightly builds.

3. Missing evidence
- Full pprof profiles, flamegraphs, and sample counts.
- Exact workload shape, pod count, node count beyond control-plane size, and test duration.
- The specific code behavior in PR #130796 that increased `getAllocationPods()` CPU.
- Confidence intervals and variance across repeated test runs.

4. Recommended next diagnostic step
Compare kubelet 1.33 and 1.32.6 pprof profiles under the same scale workload, focusing on `getAllocationPods()` call frequency and CPU cost, then verify the revert across repeated CI runs.
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
# c15 OpenShift kubelet regression

Source: https://developers.redhat.com/articles/2025/10/20/case-study-kubelet-regression-openshift

Status: accepted.

The Red Hat article is a public case study of a kubelet performance regression detected in OpenShift CI. Raw performance evidence is visible through Orion changepoint tables, CI/prow run links, pprof discussion, and summary measurements: kubelet 1.33 showed about 30-35% higher CPU usage and pod readiness latency around 3000 ms versus kubelet 1.32.6 baseline around 20-25% CPU and 2000 ms latency. Resolution evidence is visible because the article identifies an upstream patch reverting PR #130796 and says follow-up runs normalized CPU to about 25%, latency to about 2000 ms, and showed no changepoints across multiple nightly builds.

Normalized CSV feasibility: feasible from the article's visible summary and changepoint numbers.

RAW EVIDENCE:
Public source checked:
https://developers.redhat.com/articles/2025/10/20/case-study-kubelet-regression-openshift

Raw performance evidence confirmed:
- OpenShift 4.20 scale tests on a 6-node control plane cluster detected a 30% increase in kubelet CPU usage and a 50% increase in pod readiness latency.
- Kubelet 1.33 reproduced the regression; rolling back to kubelet 1.32.6 restored normal performance.
- Article summary: kubelet 1.33 CPU usage was about 30-35% higher; kubelet 1.32.6 returned to about 20-25% baseline.
- Article summary: pod readiness latency was about 3000 ms with kubelet 1.33 and about 2000 ms with kubelet 1.32.6.
- Orion CPU changepoint table includes value 34.879 with delta 29.1073 at build 1945711780562997248.
- Orion pod-ready-latency table includes 2000 ms before and 3000 ms at the changepoint, delta 50.
- Profiling attributed about 15% additional CPU time to the new getAllocationPods() path.

No extra numeric rows were inferred beyond what is visible in the article.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 8 condition labels across 12 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] fix_validation_window: c15_openshift_kubelet_regression.kubelet_cpu_usage_percent at after_fix, confidence=0.82
      Evidence: baseline/regressed/fixed or reverted conditions are present; compare the full regression window before attributing cause
  [2] phased_remediation: c15_openshift_kubelet_regression.pprof_cpu_time_percent at getallocationpods, confidence=0.74
      Evidence: multiple after/post-remediation stages are present; preserve staged fixes and residual bottlenecks instead of collapsing to one before/after delta
  [3] release_resolution_metadata: c15_openshift_kubelet_regression.pprof_cpu_time_percent at getallocationpods, confidence=0.74
      Evidence: version/release/fix labels are present; preserve introduced, regressed, reverted, fixed, or canary metadata alongside metric deltas
      baseline: baseline_high, baseline_low, baseline
      regressed: regressed_high, regressed_low, regressed
  [4] profile_hotspot: c15_openshift_kubelet_regression.kubelet_cpu_usage_percent_higher at regressed_high, confidence=0.78
      Evidence: profile/hotspot counters appear with the regression evidence; inspect code-path attribution instead of only metric deltas
  [5] mechanism_evidence: c15_openshift_kubelet_regression.pod_ready_latency_ms at after_fix, confidence=0.72
      Evidence: named low-level mechanisms appear in the evidence; retain them as evidence labels without promoting them to root cause unless backed by profiling, bisection, or owner notes
      mechanisms: pod
  [6] condition_delta: c15_openshift_kubelet_regression.kubelet_cpu_usage_percent at baseline_low (20.0 -> 25.0), confidence=0.58
      Evidence: kubelet_cpu_usage_percent changes across benchmark conditions; min=20 at baseline_low; max=25 at after_fix; ratio=1.25x; compare conditions before explaining cause
  [7] condition_delta: c15_openshift_kubelet_regression.pod_ready_latency_ms at regressed (2000.0 -> 3000.0), confidence=0.66
      Evidence: pod_ready_latency_ms changes across benchmark conditions; min=2000 at after_fix; max=3000 at regressed; ratio=1.50x; compare conditions before explaining cause
  [8] condition_delta: c15_openshift_kubelet_regression.kubelet_cpu_usage_percent_higher at regressed_low (30.0 -> 35.0), confidence=0.55
      Evidence: kubelet_cpu_usage_percent_higher changes across benchmark conditions; min=30 at regressed_low; max=35 at regressed_high; ratio=1.17x; compare conditions before explaining cause

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c15_openshift_kubelet_regression.kubelet_cpu_usage_percent sits inside a baseline/regressed/fixed window; preserve fix validation before explaining cause.
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

OpenShift CI detected a kubelet regression where kubelet 1.33 increased CPU usage and pod readiness latency versus the kubelet 1.32.6 baseline. The public evidence supports a real regression with fix validation, while the trace warns to preserve the baseline/regressed/fixed condition labels rather than flattening the case into one metric delta.

2. Evidence

- OpenShift 4.20 scale tests on a 6-node control plane cluster found about 30% higher kubelet CPU usage and 50% higher pod readiness latency.
- Kubelet 1.33 reproduced the regression; rolling back to kubelet 1.32.6 restored normal performance.
- Article summary reports kubelet 1.33 CPU around 30-35% higher, compared with the 1.32.6 baseline around 20-25%.
- Article summary reports pod readiness latency around 3000 ms in the regressed condition and around 2000 ms at baseline/fixed conditions.
- Orion changepoint evidence includes CPU value 34.879 with delta 29.1073, and pod-ready latency moving from 2000 ms to 3000 ms with delta 50.
- Profiling associated about 15% additional CPU time with the getAllocationPods() path.
- Resolution evidence identifies an upstream patch reverting PR #130796, after which follow-up runs normalized CPU to about 25%, latency to about 2000 ms, and showed no changepoints across multiple nightlies.

3. Missing evidence

- The prompt does not include full raw time series, run-to-run variance, confidence intervals, or complete Orion tables.
- The profile hotspot is attribution evidence, not complete root-cause proof by itself.
- The exact workload mix, node/pod scale, kubelet configuration, and environmental controls are summarized but not fully enumerated.
- Residual bottlenecks after remediation are not quantified beyond normalization summaries.

4. Recommended next diagnostic step

Compare the complete baseline, regressed, rollback, and post-fix runs side by side, then inspect pprof and code-path changes around getAllocationPods() and PR #130796. The immediate goal is to confirm that the reverted path accounts for the CPU and pod-readiness deltas across repeated CI runs, not just a single changepoint.
```

## Verdict Review

```text
Winner: trace-on

Concise reason: Baseline correctly captures the kubelet 1.33 CPU and pod-readiness regression, pprof attribution to getAllocationPods(), and validation after reverting PR #130796. Trace-on wins because it preserves the benchmark-condition structure from the trace: baseline, regressed, rollback/fixed, and post-fix runs are treated as staged validation rather than one before/after delta, while still keeping the hotspot attribution appropriately qualified.

Engine action: Keep condition_delta, fix_validation_window, phased_remediation, and profile_hotspot for benchmark condition tables. Add stronger guidance to require the final answer to compare all available condition labels side by side and to separate "profile hotspot attribution" from complete root-cause proof unless code-path and repeated-run evidence close the loop.
```
