# A/B Report: `c21_quarkus_38683_native_image`

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
quarkus_3_7_1_with_exclusions,c21_quarkus_38683_native_image,peak_rss_gb,11.3
quarkus_3_7_1_with_exclusions,c21_quarkus_38683_native_image,build_time_seconds,335.0
quarkus_3_5,c21_quarkus_38683_native_image,peak_rss_gb,8.32
quarkus_3_5,c21_quarkus_38683_native_image,build_time_seconds,233.0
quarkus_3_2_baseline,c21_quarkus_38683_native_image,peak_rss_gb,5.83
quarkus_3_2_baseline,c21_quarkus_38683_native_image,build_time_seconds,228.0
before_pr,c21_quarkus_38683_native_image,analysis_time_seconds,24.5
after_pr,c21_quarkus_38683_native_image,analysis_time_seconds,14.2
before_pr,c21_quarkus_38683_native_image,reachable_types_count,21686.0
after_pr,c21_quarkus_38683_native_image,reachable_types_count,17892.0
before_pr,c21_quarkus_38683_native_image,reflection_types_count,12568.0
after_pr,c21_quarkus_38683_native_image,reflection_types_count,8328.0
before_pr,c21_quarkus_38683_native_image,total_image_size_mb,149.54
after_pr,c21_quarkus_38683_native_image,total_image_size_mb,97.27
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
# c21 Quarkus #38683 native-image build regression

Source: https://github.com/quarkusio/quarkus/issues/38683

Status: accepted.

The Quarkus issue is public and contains extensive native-image build logs with elapsed build time, analysis time, peak RSS, GC time, reachable types, reflection registrations, generated image size, and code/heap sizes. Resolution evidence is public: PR #38886 was merged and closed the issue, and the PR body includes before/after native-image numbers showing reduced build time and image size.

Normalized CSV feasibility: feasible. The issue and PR expose concrete numeric before/after values.

RAW EVIDENCE:
Public sources checked:
https://github.com/quarkusio/quarkus/issues/38683
https://github.com/quarkusio/quarkus/pull/38886

Raw performance evidence confirmed:
- Issue reports Quarkus 3.7.1 native build: Peak RSS 11.30GB, finished in 5m35s.
- Issue reports Quarkus 3.5 comparison: Peak RSS 8.32GB, finished in 3m53s.
- Issue reports Quarkus 3.2 baseline: Peak RSS 5.83GB, finished in 3m48s.
- PR #38886 before: analysis 24.5s, 21,686 reachable types, 12,568 reflection types, total image 149.54MB.
- PR #38886 after: analysis 14.2s, 17,892 reachable types, 8,328 reflection types, total image 97.27MB.

No values were inferred beyond visible issue/PR text.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
- Quarkus native-image builds regress in build time and memory use between older baselines and Quarkus 3.7.1, with excess reachable/reflection metadata contributing to larger images.

2. Evidence
- Quarkus 3.7.1 native build reports Peak RSS 11.30GB and finishes in 5m35s.
- Quarkus 3.5 comparison reports Peak RSS 8.32GB and finishes in 3m53s.
- Quarkus 3.2 baseline reports Peak RSS 5.83GB and finishes in 3m48s.
- PR #38886 before values: analysis 24.5s, 21,686 reachable types, 12,568 reflection types, image 149.54MB.
- PR #38886 after values: analysis 14.2s, 17,892 reachable types, 8,328 reflection types, image 97.27MB.
- Public resolution evidence says PR #38886 was merged and closed the issue.

3. Missing evidence
- Full native-image command line, application shape, extensions, GraalVM version, host specs, and repeated-run variance.
- Direct before/after total build time and peak RSS for PR #38886 under the same workload.
- Attribution of which registrations/types account for the regression.

4. Recommended next diagnostic step
- Rebuild the same app across Quarkus 3.2, 3.5, 3.7.1, and the PR #38886 fix, collecting repeated native-image logs and diffing reachable/reflection registrations.
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
# c21 Quarkus #38683 native-image build regression

Source: https://github.com/quarkusio/quarkus/issues/38683

Status: accepted.

The Quarkus issue is public and contains extensive native-image build logs with elapsed build time, analysis time, peak RSS, GC time, reachable types, reflection registrations, generated image size, and code/heap sizes. Resolution evidence is public: PR #38886 was merged and closed the issue, and the PR body includes before/after native-image numbers showing reduced build time and image size.

Normalized CSV feasibility: feasible. The issue and PR expose concrete numeric before/after values.

RAW EVIDENCE:
Public sources checked:
https://github.com/quarkusio/quarkus/issues/38683
https://github.com/quarkusio/quarkus/pull/38886

Raw performance evidence confirmed:
- Issue reports Quarkus 3.7.1 native build: Peak RSS 11.30GB, finished in 5m35s.
- Issue reports Quarkus 3.5 comparison: Peak RSS 8.32GB, finished in 3m53s.
- Issue reports Quarkus 3.2 baseline: Peak RSS 5.83GB, finished in 3m48s.
- PR #38886 before: analysis 24.5s, 21,686 reachable types, 12,568 reflection types, total image 149.54MB.
- PR #38886 after: analysis 14.2s, 17,892 reachable types, 8,328 reflection types, total image 97.27MB.

No values were inferred beyond visible issue/PR text.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 5 condition labels across 14 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] release_resolution_metadata: c21_quarkus_38683_native_image.analysis_time_seconds at after_pr, confidence=0.74
      Evidence: version/release/fix labels are present; preserve introduced, regressed, reverted, fixed, or canary metadata alongside metric deltas
      baseline: quarkus_3_2_baseline
      fixed: after_pr
      versions: quarkus_3_2_baseline, quarkus_3_5, quarkus_3_7_1_with_exclusions
  [2] phased_remediation: c21_quarkus_38683_native_image.total_image_size_mb at before_pr, confidence=0.74
      Evidence: multiple after/post-remediation stages are present; preserve staged fixes and residual bottlenecks instead of collapsing to one before/after delta
  [3] condition_delta: c21_quarkus_38683_native_image.analysis_time_seconds at before_pr (14.2 -> 24.5), confidence=0.72
      Evidence: analysis_time_seconds changes across benchmark conditions; min=14.2 at after_pr; max=24.5 at before_pr; ratio=1.73x; compare conditions before explaining cause
  [4] condition_delta: c21_quarkus_38683_native_image.reachable_types_count at before_pr (17892.0 -> 21686.0), confidence=0.57
      Evidence: reachable_types_count changes across benchmark conditions; min=1.789e+04 at after_pr; max=2.169e+04 at before_pr; ratio=1.21x; compare conditions before explaining cause
  [5] condition_delta: c21_quarkus_38683_native_image.reflection_types_count at before_pr (8328.0 -> 12568.0), confidence=0.67
      Evidence: reflection_types_count changes across benchmark conditions; min=8328 at after_pr; max=1.257e+04 at before_pr; ratio=1.51x; compare conditions before explaining cause
  [6] condition_delta: c21_quarkus_38683_native_image.total_image_size_mb at before_pr (97.27 -> 149.54), confidence=0.67
      Evidence: total_image_size_mb changes across benchmark conditions; min=97.27 at after_pr; max=149.5 at before_pr; ratio=1.54x; compare conditions before explaining cause
  [7] condition_delta: c21_quarkus_38683_native_image.build_time_seconds at quarkus_3_7_1_with_exclusions (228.0 -> 335.0), confidence=0.65
      Evidence: build_time_seconds changes across benchmark conditions; min=228 at quarkus_3_2_baseline; max=335 at quarkus_3_7_1_with_exclusions; ratio=1.47x; compare conditions before explaining cause
  [8] condition_delta: c21_quarkus_38683_native_image.peak_rss_gb at quarkus_3_7_1_with_exclusions (5.83 -> 11.3), confidence=0.76
      Evidence: peak_rss_gb changes across benchmark conditions; min=5.83 at quarkus_3_2_baseline; max=11.3 at quarkus_3_7_1_with_exclusions; ratio=1.94x; compare conditions before explaining cause
  [9] version_fix_lineage: c21_quarkus_38683_native_image.analysis_time_seconds at after_pr, confidence=0.76
      Evidence: versioned regression and fixed/canary conditions are present; preserve fix lineage alongside the timing delta

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c21_quarkus_38683_native_image.analysis_time_seconds has release/fix lineage; preserve versions, revert, fixed, and canary labels before explaining cause.
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
- Quarkus native-image builds show increased build time, peak RSS, analysis cost, reachable types, reflection registrations, and image size in affected conditions, with PR evidence showing improvement after the fix.

2. Evidence
- Issue evidence reports Quarkus 3.7.1 native build at 11.30GB peak RSS and 5m35s, versus Quarkus 3.5 at 8.32GB and 3m53s, and Quarkus 3.2 at 5.83GB and 3m48s.
- Trace build time ranges from 228s to 335s, a 1.47x condition delta.
- Peak RSS ranges from 5.83GB to 11.30GB, a 1.94x condition delta.
- PR before/after evidence shows analysis time improving from 24.5s to 14.2s, reachable types from 21,686 to 17,892, reflection types from 12,568 to 8,328, and image size from 149.54MB to 97.27MB.

3. Missing evidence
- Exact project, dependency graph, GraalVM/native-image version, JVM flags, and build host parity across all version comparisons.
- Native-image phase breakdown beyond the visible summary metrics.
- Evidence proving which dependency or registration change caused the resource increase.
- Repeat runs with variance for build time and memory.

4. Recommended next diagnostic step
- Reproduce the native-image build across Quarkus 3.2, 3.5, 3.7.1, before-PR, and after-PR using the same host and GraalVM version, collecting native-image phase reports, reflection registration diffs, reachable-type diffs, peak RSS, and elapsed time.
```

## Verdict Review

```text
Winner: trace-on

Concise reason: Trace-on integrates the multiple condition deltas across build time, peak RSS, analysis time, reachable types, reflection types, and image size, giving a clearer multi-metric native-image regression summary than baseline.

Engine action: Keep multi-signal condition_delta behavior for benchmark-condition tables; no new detector gap flagged.
```
