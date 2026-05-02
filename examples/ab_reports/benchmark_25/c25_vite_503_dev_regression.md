# A/B Report: `c25_vite_503_dev_regression`

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
vite_5_0_2,c25_vite_503_dev_regression,dev_page_load_time_min_value_s_seconds,1.5
vite_5_0_2,c25_vite_503_dev_regression,dev_page_load_time_max_value_s_seconds,2.0
vite_5_0_3,c25_vite_503_dev_regression,dev_page_load_time_min_value_s_seconds,5.0
vite_5_0_3,c25_vite_503_dev_regression,dev_page_load_time_max_value_s_seconds,10.0
vite_5_0_3_vs_5_0_2,c25_vite_503_dev_regression,reported_slowdown_min_value_s_x,3.0
vite_5_0_3_vs_5_0_2,c25_vite_503_dev_regression,reported_slowdown_max_value_s_x,10.0
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
# c25 Vite 5.0.3 Dev Regression

Source: https://github.com/vitejs/vite/issues/15177

Status: accepted

Verification date: 2026-05-02

Summary: Vite issue #15177 reports a dev performance regression after upgrading from Vite 5.0.2 to 5.0.3. The public issue body describes Vitest + Playwright loading a Vite app with a few hundred JS files and about 80k lines of code. It reports 5.0.3 taking 3-10x longer, with 5.0.2 at about 1.5-2 seconds and 5.0.3 at about 5-10 seconds. A maintainer identified that reverting vitejs/vite#15135 fixed the regression, and PR #15178 performed that revert. The reporter confirmed Vite 5.0.4 did not have the same performance problem.

Raw performance evidence confirmed:
- Vite 5.0.2 first load: about 1.5-2 seconds.
- Vite 5.0.3 loads: about 5-10 seconds, reported as 3-10x slower.
- Workload: few hundred JS files and about 80k LOC using custom Vitest + Playwright browser infra.

Resolution evidence confirmed:
- Maintainer comment says reverting vitejs/vite#15135 fixes the regression.
- vitejs/vite#15178 is merged and titled as a revert of #15135.
- Vite 5.0.4 changelog includes #15178.
- Reporter confirms 5.0.4 does not have the same performance problem.

normalized.csv: created from visible timing ranges in the issue body.

RAW EVIDENCE:
Source: https://github.com/vitejs/vite/issues/15177

Issue title: 3-10x slower performance in dev in Vite 5.0.3.

Raw performance evidence:

- The reporter updated Vite from 5.0.2 to 5.0.3 and tests started timing out.
- The setup uses custom infrastructure with Vitest + Playwright to open a browser using Vite.
- Vite loads a few hundred JS files, about 80k lines of code, and renders React content.
- With Vite 5.0.3 the reporter says webpages consistently take 3-10x longer to load.
- The issue includes a video attachment as reproduction evidence.
- The issue body says the first load via Vite 5.0.2 takes about 1.5-2 seconds.
- It then says after upgrading to Vite 5.0.3, restarting Vite, and loading the page again twice, both loads take 5-10 seconds.

Visible numeric values:

- Workload: few hundred JS files.
- Workload size: about 80k lines of code.
- 5.0.2 load time: about 1.5-2 seconds.
- 5.0.3 load time: about 5-10 seconds.
- Reported slowdown: 3-10x.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
- Vite 5.0.3 introduced a dev-load regression versus Vite 5.0.2 for a Vitest + Playwright browser workflow.

2. Evidence
- Reporter says tests began timing out after upgrading from 5.0.2 to 5.0.3.
- Workload is a Vite-loaded React app with a few hundred JavaScript files and about 80k lines of code.
- Vite 5.0.2 first load is reported at about 1.5-2 seconds.
- Vite 5.0.3 loads are reported at about 5-10 seconds, or 3-10x slower.
- Maintainer says reverting vitejs/vite#15135 fixes the regression, and the reporter confirms 5.0.4 no longer has the issue.

3. Missing evidence
- No exact reproduction repository, machine specs, browser details, or repeated benchmark table are provided in the prompt.
- The provided evidence does not quantify variance or isolate which operation inside dev loading became slower.
- The video attachment is mentioned but not described with measurable details.

4. Recommended next diagnostic step
- Run the same workload on Vite 5.0.2, 5.0.3, and 5.0.4 with repeated cold/warm dev-load measurements and CPU/server tracing, then compare the reverted change's effect on request handling and transform timing.
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
# c25 Vite 5.0.3 Dev Regression

Source: https://github.com/vitejs/vite/issues/15177

Status: accepted

Verification date: 2026-05-02

Summary: Vite issue #15177 reports a dev performance regression after upgrading from Vite 5.0.2 to 5.0.3. The public issue body describes Vitest + Playwright loading a Vite app with a few hundred JS files and about 80k lines of code. It reports 5.0.3 taking 3-10x longer, with 5.0.2 at about 1.5-2 seconds and 5.0.3 at about 5-10 seconds. A maintainer identified that reverting vitejs/vite#15135 fixed the regression, and PR #15178 performed that revert. The reporter confirmed Vite 5.0.4 did not have the same performance problem.

Raw performance evidence confirmed:
- Vite 5.0.2 first load: about 1.5-2 seconds.
- Vite 5.0.3 loads: about 5-10 seconds, reported as 3-10x slower.
- Workload: few hundred JS files and about 80k LOC using custom Vitest + Playwright browser infra.

Resolution evidence confirmed:
- Maintainer comment says reverting vitejs/vite#15135 fixes the regression.
- vitejs/vite#15178 is merged and titled as a revert of #15135.
- Vite 5.0.4 changelog includes #15178.
- Reporter confirms 5.0.4 does not have the same performance problem.

normalized.csv: created from visible timing ranges in the issue body.

RAW EVIDENCE:
Source: https://github.com/vitejs/vite/issues/15177

Issue title: 3-10x slower performance in dev in Vite 5.0.3.

Raw performance evidence:

- The reporter updated Vite from 5.0.2 to 5.0.3 and tests started timing out.
- The setup uses custom infrastructure with Vitest + Playwright to open a browser using Vite.
- Vite loads a few hundred JS files, about 80k lines of code, and renders React content.
- With Vite 5.0.3 the reporter says webpages consistently take 3-10x longer to load.
- The issue includes a video attachment as reproduction evidence.
- The issue body says the first load via Vite 5.0.2 takes about 1.5-2 seconds.
- It then says after upgrading to Vite 5.0.3, restarting Vite, and loading the page again twice, both loads take 5-10 seconds.

Visible numeric values:

- Workload: few hundred JS files.
- Workload size: about 80k lines of code.
- 5.0.2 load time: about 1.5-2 seconds.
- 5.0.3 load time: about 5-10 seconds.
- Reported slowdown: 3-10x.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 3 condition labels across 6 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] release_resolution_metadata: c25_vite_503_dev_regression.reported_slowdown_max_value_s_x at vite_5_0_3_vs_5_0_2, confidence=0.74
      Evidence: version/release/fix labels are present; preserve introduced, regressed, reverted, fixed, or canary metadata alongside metric deltas
      versions: vite_5_0_2, vite_5_0_3, vite_5_0_3_vs_5_0_2
  [2] condition_delta: c25_vite_503_dev_regression.dev_page_load_time_max_value_s_seconds at vite_5_0_3 (2.0 -> 10.0), confidence=0.95
      Evidence: dev_page_load_time_max_value_s_seconds changes across benchmark conditions; min=2 at vite_5_0_2; max=10 at vite_5_0_3; ratio=5.00x; compare conditions before explaining cause
  [3] condition_delta: c25_vite_503_dev_regression.dev_page_load_time_min_value_s_seconds at vite_5_0_3 (1.5 -> 5.0), confidence=0.89
      Evidence: dev_page_load_time_min_value_s_seconds changes across benchmark conditions; min=1.5 at vite_5_0_2; max=5 at vite_5_0_3; ratio=3.33x; compare conditions before explaining cause
  [4] config_expansion: c25_vite_503_dev_regression.reported_slowdown_max_value_s_x at vite_5_0_3_vs_5_0_2, confidence=0.78
      Evidence: reported_slowdown_max_value_s_x is 10x, indicating a material expansion/change in generated configuration
  [5] config_expansion: c25_vite_503_dev_regression.reported_slowdown_min_value_s_x at vite_5_0_3_vs_5_0_2, confidence=0.78
      Evidence: reported_slowdown_min_value_s_x is 3x, indicating a material expansion/change in generated configuration

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c25_vite_503_dev_regression.reported_slowdown_max_value_s_x has release/fix lineage; preserve versions, revert, fixed, and canary labels before explaining cause.
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
- Vite 5.0.3 regressed dev page load performance versus Vite 5.0.2 for a Vitest + Playwright workflow loading a React app with a few hundred JS files and about 80k LOC.

2. Evidence
- The issue reports Vite 5.0.2 first load at about 1.5-2 seconds.
- The same workflow on Vite 5.0.3 took about 5-10 seconds and was described as 3-10x slower.
- The trace captures a max-load delta from 2.0 s to 10.0 s, a 5.00x spread, and a min-load delta from 1.5 s to 5.0 s, a 3.33x spread.
- Resolution evidence says reverting #15135 fixed the regression, and the reporter confirmed Vite 5.0.4 did not show the same problem.

3. Missing evidence
- The trace does not include browser/network waterfall data, CPU profiles, module transform timings, or per-file load breakdowns.
- The evidence is based on reported timing ranges rather than a controlled benchmark distribution.
- It does not prove which internal subsystem caused the slowdown, even though a revert is associated with the fix.

4. Recommended next diagnostic step
- Run the reproduction on Vite 5.0.2, 5.0.3, and 5.0.4 with repeated cold and warm starts, collecting Vite debug timing, browser performance traces, and transform/load counts to isolate where the extra seconds appear.
```

## Verdict Review

```text
Winner: trace-on

Concise reason: Trace-on cleanly uses the trace's min/max load-time deltas, preserves the 5.0.2 to 5.0.3 regression and 5.0.4 confirmation, and avoids overstating the internal subsystem cause.

Engine action: Keep condition_delta plus config_expansion behavior for sparse version-comparison evidence; no new detector gap flagged.
```
