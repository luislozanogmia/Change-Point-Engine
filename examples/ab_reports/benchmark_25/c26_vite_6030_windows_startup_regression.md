# A/B Report: `c26_vite_6030_windows_startup_regression`

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
vite_2_6_14_run_1,c26_vite_6030_windows_startup_regression,dev_startup_time_windows_value_seconds,12.0
vite_2_6_14_run_2,c26_vite_6030_windows_startup_regression,dev_startup_time_windows_value_seconds,7.0
vite_2_6_14_run_3,c26_vite_6030_windows_startup_regression,dev_startup_time_windows_value_seconds,7.0
vite_2_6_14_run_4,c26_vite_6030_windows_startup_regression,dev_startup_time_windows_value_seconds,6.0
vite_2_6_14_run_5,c26_vite_6030_windows_startup_regression,dev_startup_time_windows_value_seconds,6.0
vite_2_7_1_run_1,c26_vite_6030_windows_startup_regression,dev_startup_time_windows_value_seconds,46.0
vite_2_7_1_run_2,c26_vite_6030_windows_startup_regression,dev_startup_time_windows_value_seconds,47.0
vite_2_7_1_run_3,c26_vite_6030_windows_startup_regression,dev_startup_time_windows_value_seconds,46.0
vite_2_7_1_run_4,c26_vite_6030_windows_startup_regression,dev_startup_time_windows_value_seconds,47.0
vite_2_7_1_run_5,c26_vite_6030_windows_startup_regression,dev_startup_time_windows_value_seconds,48.0
vite_2_6_14_run_1,c26_vite_6030_windows_startup_regression,dev_startup_time_wsl2_value_seconds,3.0
vite_2_6_14_run_2,c26_vite_6030_windows_startup_regression,dev_startup_time_wsl2_value_seconds,4.0
vite_2_6_14_run_3,c26_vite_6030_windows_startup_regression,dev_startup_time_wsl2_value_seconds,4.0
vite_2_6_14_run_4,c26_vite_6030_windows_startup_regression,dev_startup_time_wsl2_value_seconds,4.0
vite_2_6_14_run_5,c26_vite_6030_windows_startup_regression,dev_startup_time_wsl2_value_seconds,4.0
vite_2_7_1_run_1,c26_vite_6030_windows_startup_regression,dev_startup_time_wsl2_value_seconds,7.0
vite_2_7_1_run_2,c26_vite_6030_windows_startup_regression,dev_startup_time_wsl2_value_seconds,7.0
vite_2_7_1_run_3,c26_vite_6030_windows_startup_regression,dev_startup_time_wsl2_value_seconds,8.0
vite_2_7_1_run_4,c26_vite_6030_windows_startup_regression,dev_startup_time_wsl2_value_seconds,8.0
vite_2_7_1_run_5,c26_vite_6030_windows_startup_regression,dev_startup_time_wsl2_value_seconds,6.0
2_7_0_beta_4,c26_vite_6030_windows_startup_regression,bisect_startup_time_value_milliseconds,9441.0
2_7_0_beta_5,c26_vite_6030_windows_startup_regression,bisect_startup_time_value_milliseconds,18540.0
before_pr_5665,c26_vite_6030_windows_startup_regression,pr_5665_comparison_value_milliseconds,8858.0
after_pr_5665,c26_vite_6030_windows_startup_regression,pr_5665_comparison_value_milliseconds,29174.0
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
# c26 Vite #6030 Windows Startup Regression

Source: https://github.com/vitejs/vite/issues/6030

Status: accepted

Verification date: 2026-05-02

Summary: Vite issue #6030 reports that upgrading from Vite 2.6.14 to 2.7.1 made dev startup/build performance slower on Windows 10 and Ubuntu 20.04 under WSL2. The issue body includes repeated timing samples: Windows 2.6.14 ran in 6-12 seconds while 2.7.1 ran in 46-48 seconds; WSL2 2.6.14 ran in 3-4 seconds while 2.7.1 ran in 6-8 seconds. Later comments narrowed the regression to the 2.7 beta series and PR #5665, with profile zips attached. Maintainers discussed reducing `fs.realpath` calls and later closed the issue after performance work; the reporter confirmed Vite 4.3-era performance built under one second.

Raw performance evidence confirmed:
- Windows 10, Vite 2.6.14: 12, 7, 7, 6, 6 seconds.
- Windows 10, Vite 2.7.1: 46, 47, 46, 47, 48 seconds.
- Ubuntu 20.04 WSL2, Vite 2.6.14: 3, 4, 4, 4, 4 seconds.
- Ubuntu 20.04 WSL2, Vite 2.7.1: 7, 7, 8, 8, 6 seconds.
- Later retest: 2.7.0-beta.4 at 9441 ms, 2.7.0-beta.5 at 18540 ms, before PR #5665 at 8858 ms, after PR #5665 at 29174 ms.

Resolution evidence confirmed:
- Maintainer comment identified excess `realPath` calls and suggested/coded reductions.
- PR #6412, `fix: reduce number of fs.realpath calls`, was closed after testing and discussion.
- Maintainer closed the issue on 2023-04-01 saying recent Vite performance improvements completed the work and asked users to try Vite 4.3 beta.
- Reporter confirmed on 2023-04-05 that it built under one second.

normalized.csv: created from visible timing samples in the issue body and comments.

RAW EVIDENCE:
Source: https://github.com/vitejs/vite/issues/6030

Issue title: Vite 2.7.x is about 1.9 to 6.2 times slower than 2.6.14

Raw performance evidence:

- Reporter says upgrading from Vite 2.6.14 to 2.7.x made the development build about 6.2x slower on Windows and about 1.9x slower on Ubuntu 20.04 under WSL2.
- Windows 10 timing samples, rounded to nearest second:
  - Vite 2.6.14: 12, 7, 7, 6, 6 seconds.
  - Vite 2.7.1: 46, 47, 46, 47, 48 seconds.
- Ubuntu 20.04 WSL2 timing samples, rounded to nearest second:
  - Vite 2.6.14: 3, 4, 4, 4, 4 seconds.
  - Vite 2.7.1: 7, 7, 8, 8, 6 seconds.
- Reporter attached profile traces and said the main regression appeared to be how often `realPath` was called.
- A later PR test comment reported:
  - Vite 2.6.14: 9, 9, 10, 9, 9 seconds.
  - Vite 2.7.1: 46, 47, 46, 47, 48 seconds.
  - PR test: 36, 38, 38, 36, 32 seconds.
  - PR test with preserveSymlinks: 31, 26, 26, 27, 28 seconds.
- Another bisect-style comment reported:
  - 2.7.0-beta.4: 9441 ms.
  - 2.7.0-beta.5: 18540 ms.
  - Before PR #5665: 8858 ms.
  - After PR #5665: 29174 ms.

Workload/context:
- Reproduction repo: https://github.com/Lani/vite-2.7-slow
- Command: `npm run dev -- --force`
- Windows system: Windows 10, Node 14.15.4, npm 6.14.10.
- Ubuntu system: Ubuntu 20.04.3 LTS under WSL2/container, Node 14.15.4.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
- Vite 2.7.x had a dev startup/build regression versus Vite 2.6.14, especially on Windows 10 and also on Ubuntu 20.04 under WSL2.

2. Evidence
- Windows 10 samples increased from 6-12 seconds on Vite 2.6.14 to 46-48 seconds on Vite 2.7.1.
- WSL2 samples increased from 3-4 seconds on Vite 2.6.14 to 6-8 seconds on Vite 2.7.1.
- Later PR testing still showed 2.7.1 around 46-48 seconds, with tested mitigations improving but not restoring 2.6.14 performance.
- Bisect-style timings show 2.7.0-beta.4 at 9441 ms, 2.7.0-beta.5 at 18540 ms, before PR #5665 at 8858 ms, and after PR #5665 at 29174 ms.
- Reporter attached profiles and noted frequent `realPath` calls; maintainers discussed reducing `fs.realpath` calls.

3. Missing evidence
- The prompt does not include the profile contents, exact dependency graph, filesystem layout, or full statistical benchmark method.
- The evidence suggests a likely area but does not prove a single root cause from the public timings alone.
- The later Vite 4.3-era resolution is not tied to a specific measured fix in the provided evidence.

4. Recommended next diagnostic step
- Reproduce `npm run dev -- --force` on the linked repo across 2.6.14, 2.7 beta points, 2.7.1, and candidate fixes while collecting syscall/profile data focused on `fs.realpath` volume and call sites.
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
# c26 Vite #6030 Windows Startup Regression

Source: https://github.com/vitejs/vite/issues/6030

Status: accepted

Verification date: 2026-05-02

Summary: Vite issue #6030 reports that upgrading from Vite 2.6.14 to 2.7.1 made dev startup/build performance slower on Windows 10 and Ubuntu 20.04 under WSL2. The issue body includes repeated timing samples: Windows 2.6.14 ran in 6-12 seconds while 2.7.1 ran in 46-48 seconds; WSL2 2.6.14 ran in 3-4 seconds while 2.7.1 ran in 6-8 seconds. Later comments narrowed the regression to the 2.7 beta series and PR #5665, with profile zips attached. Maintainers discussed reducing `fs.realpath` calls and later closed the issue after performance work; the reporter confirmed Vite 4.3-era performance built under one second.

Raw performance evidence confirmed:
- Windows 10, Vite 2.6.14: 12, 7, 7, 6, 6 seconds.
- Windows 10, Vite 2.7.1: 46, 47, 46, 47, 48 seconds.
- Ubuntu 20.04 WSL2, Vite 2.6.14: 3, 4, 4, 4, 4 seconds.
- Ubuntu 20.04 WSL2, Vite 2.7.1: 7, 7, 8, 8, 6 seconds.
- Later retest: 2.7.0-beta.4 at 9441 ms, 2.7.0-beta.5 at 18540 ms, before PR #5665 at 8858 ms, after PR #5665 at 29174 ms.

Resolution evidence confirmed:
- Maintainer comment identified excess `realPath` calls and suggested/coded reductions.
- PR #6412, `fix: reduce number of fs.realpath calls`, was closed after testing and discussion.
- Maintainer closed the issue on 2023-04-01 saying recent Vite performance improvements completed the work and asked users to try Vite 4.3 beta.
- Reporter confirmed on 2023-04-05 that it built under one second.

normalized.csv: created from visible timing samples in the issue body and comments.

RAW EVIDENCE:
Source: https://github.com/vitejs/vite/issues/6030

Issue title: Vite 2.7.x is about 1.9 to 6.2 times slower than 2.6.14

Raw performance evidence:

- Reporter says upgrading from Vite 2.6.14 to 2.7.x made the development build about 6.2x slower on Windows and about 1.9x slower on Ubuntu 20.04 under WSL2.
- Windows 10 timing samples, rounded to nearest second:
  - Vite 2.6.14: 12, 7, 7, 6, 6 seconds.
  - Vite 2.7.1: 46, 47, 46, 47, 48 seconds.
- Ubuntu 20.04 WSL2 timing samples, rounded to nearest second:
  - Vite 2.6.14: 3, 4, 4, 4, 4 seconds.
  - Vite 2.7.1: 7, 7, 8, 8, 6 seconds.
- Reporter attached profile traces and said the main regression appeared to be how often `realPath` was called.
- A later PR test comment reported:
  - Vite 2.6.14: 9, 9, 10, 9, 9 seconds.
  - Vite 2.7.1: 46, 47, 46, 47, 48 seconds.
  - PR test: 36, 38, 38, 36, 32 seconds.
  - PR test with preserveSymlinks: 31, 26, 26, 27, 28 seconds.
- Another bisect-style comment reported:
  - 2.7.0-beta.4: 9441 ms.
  - 2.7.0-beta.5: 18540 ms.
  - Before PR #5665: 8858 ms.
  - After PR #5665: 29174 ms.

Workload/context:
- Reproduction repo: https://github.com/Lani/vite-2.7-slow
- Command: `npm run dev -- --force`
- Windows system: Windows 10, Node 14.15.4, npm 6.14.10.
- Ubuntu system: Ubuntu 20.04.3 LTS under WSL2/container, Node 14.15.4.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 14 condition labels across 24 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] release_resolution_metadata: c26_vite_6030_windows_startup_regression.pr_5665_comparison_value_milliseconds at after_pr_5665, confidence=0.74
      Evidence: version/release/fix labels are present; preserve introduced, regressed, reverted, fixed, or canary metadata alongside metric deltas
      fixed: after_pr_5665
      versions: vite_2_6_14_run_1, vite_2_6_14_run_2, vite_2_6_14_run_3, vite_2_6_14_run_4, vite_2_6_14_run_5, vite_2_7_1_run_1, vite_2_7_1_run_2, vite_2_7_1_run_3
  [2] condition_delta: c26_vite_6030_windows_startup_regression.bisect_startup_time_value_milliseconds at 2_7_0_beta_5 (9441.0 -> 18540.0), confidence=0.76
      Evidence: bisect_startup_time_value_milliseconds changes across benchmark conditions; min=9441 at 2_7_0_beta_4; max=1.854e+04 at 2_7_0_beta_5; ratio=1.96x; compare conditions before explaining cause
  [3] condition_delta: c26_vite_6030_windows_startup_regression.pr_5665_comparison_value_milliseconds at before_pr_5665 (8858.0 -> 29174.0), confidence=0.89
      Evidence: pr_5665_comparison_value_milliseconds changes across benchmark conditions; min=8858 at before_pr_5665; max=2.917e+04 at after_pr_5665; ratio=3.29x; compare conditions before explaining cause
  [4] condition_delta: c26_vite_6030_windows_startup_regression.dev_startup_time_wsl2_value_seconds at vite_2_7_1_run_3 (3.0 -> 8.0), confidence=0.84
      Evidence: dev_startup_time_wsl2_value_seconds changes across benchmark conditions; min=3 at vite_2_6_14_run_1; max=8 at vite_2_7_1_run_3; ratio=2.67x; compare conditions before explaining cause
  [5] condition_delta: c26_vite_6030_windows_startup_regression.dev_startup_time_windows_value_seconds at vite_2_7_1_run_5 (6.0 -> 48.0), confidence=0.95
      Evidence: dev_startup_time_windows_value_seconds changes across benchmark conditions; min=6 at vite_2_6_14_run_4; max=48 at vite_2_7_1_run_5; ratio=8.00x; compare conditions before explaining cause
  [6] version_fix_lineage: c26_vite_6030_windows_startup_regression.pr_5665_comparison_value_milliseconds at after_pr_5665, confidence=0.76
      Evidence: versioned regression and fixed/canary conditions are present; preserve fix lineage alongside the timing delta

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c26_vite_6030_windows_startup_regression.pr_5665_comparison_value_milliseconds has release/fix lineage; preserve versions, revert, fixed, and canary labels before explaining cause.
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

Vite dev startup/build time regressed substantially between 2.6.14 and 2.7.x, especially on Windows 10, with additional slowdown visible under Ubuntu 20.04 on WSL2. Bisect-style evidence points to a large timing shift around the 2.7 beta series and PR #5665, but the trace alone does not prove root cause.

2. Evidence

- Windows 10 samples moved from 6-12 seconds on Vite 2.6.14 to 46-48 seconds on Vite 2.7.1.
- WSL2 samples moved from 3-4 seconds on Vite 2.6.14 to 6-8 seconds on Vite 2.7.1.
- A later comparison reports 2.7.0-beta.4 at 9441 ms and 2.7.0-beta.5 at 18540 ms.
- PR #5665 comparison reports 8858 ms before the PR and 29174 ms after it.
- Reporter/profile discussion mentions frequent `realPath` calls, and later performance work reduced `fs.realpath` calls; eventual Vite 4.3-era retest reportedly built under one second.

3. Missing evidence

- Direct profile excerpts quantifying `fs.realpath` or related filesystem-call cost across the same before/after revisions.
- Controlled environment details for all timing samples, including filesystem type, antivirus/indexing state, dependency cache state, and cold versus warm runs.
- A clean fix-validation table showing which specific change restored which part of the regression.

4. Recommended next diagnostic step

Reproduce `npm run dev -- --force` on the repro repo across Vite 2.6.14, 2.7.1, 2.7.0-beta.4, 2.7.0-beta.5, and before/after PR #5665, while collecting Node profiles and filesystem syscall counts. Confirm whether the timing shift aligns with increased realpath/filesystem work before stating causality.
```

## Verdict Review

```text
Winner: trace-on

Reason: Trace-on preserves the Windows/WSL timing deltas and beta/PR #5665 lineage while more clearly stating that the public timing evidence points toward realpath/filesystem work but does not prove root cause. That caution is the right final review posture for this case.

Engine action: Keep version-fix-lineage and condition-delta detection; add a filesystem-call amplification detector that requests syscall/profile counts before promoting `fs.realpath` from suspected area to root cause.
```
