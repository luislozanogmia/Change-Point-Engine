# A/B Report: `c29_bun_17000_runtime_regression`

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
bun_1_1_4,c29_bun_17000_runtime_regression,matmul_runtime_value_seconds,1.8
bun_1_1_5,c29_bun_17000_runtime_regression,matmul_runtime_value_seconds,4.5
bun_1_2_2,c29_bun_17000_runtime_regression,matmul_runtime_value_seconds,4.5
node_18_20_3,c29_bun_17000_runtime_regression,matmul_runtime_value_seconds,3.1
deno_1_39_1,c29_bun_17000_runtime_regression,matmul_runtime_value_seconds,3.1
bun_fixed_canary,c29_bun_17000_runtime_regression,matmul_runtime_value_seconds,1.32
bun_1_2_12,c29_bun_17000_runtime_regression,matmul_runtime_value_seconds,2.47
node_comparison_in_fix_comment,c29_bun_17000_runtime_regression,matmul_runtime_value_seconds,1.76
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
# c29 Bun #17000 Runtime Regression

Source: https://github.com/oven-sh/bun/issues/17000

Status: accepted

Verification date: 2026-05-02

Summary: Bun issue #17000 reports a JavaScript runtime performance regression between Bun 1.1.4 and 1.1.5+ on a public `matmul.js` script from the PLB2 benchmark set. The issue body reports 1.8 seconds on Bun 1.1.4 and 4.5 seconds on Bun 1.1.5 and Bun 1.2.2, slower than Node 18.20.3 and Deno 1.39.1 at 3.1 seconds. Discussion identified JavaScriptCore as the likely source. PR #19467, `sync webkit`, merged and closed the issue; a maintainer comment says the fix would ship in Bun 1.2.13 and gives canary timing of 1.32 seconds versus Bun 1.2.12 at 2.47 seconds.

Raw performance evidence confirmed:
- Bun 1.1.4: 1.8 seconds.
- Bun 1.1.5 and Bun 1.2.2: 4.5 seconds.
- Node 18.20.3 and Deno 1.39.1: 3.1 seconds.
- Fixed canary: 1.32 seconds.
- Bun 1.2.12: 2.47 seconds.

Resolution evidence confirmed:
- PR #19467 `sync webkit` merged on 2025-05-06 and closes issue #17000.
- Maintainer comment says the fix would be in Bun 1.2.13.
- Reporter replied with thanks after fix evidence.

normalized.csv: created from visible timing values in the issue body and resolution comment.

RAW EVIDENCE:
Source: https://github.com/oven-sh/bun/issues/17000

Issue title: Performance regression between v1.1.4 and v1.1.5+

Raw performance evidence:

- Reproduction:
  - `wget https://raw.githubusercontent.com/attractivechaos/plb2/refs/heads/master/src/javascript/matmul.js`
  - `time bun matmul.js`
- Reporter platform: Darwin 24.2.0 arm64 arm.
- Reporter timing on Mac M1:
  - Bun 1.1.4: 1.8 seconds.
  - Bun 1.1.5 and Bun 1.2.2: 4.5 seconds.
  - Node 18.20.3 and Deno 1.39.1: 3.1 seconds.
- Reporter says expected behavior is that the script should take 1.8 seconds.
- Reporter says current behavior is 4.5 seconds, slower than Node/Deno.

Resolution timing evidence from maintainer comment:
- New canary build on macOS:
  - `time bun matmul.js`: executed in 1.32 seconds.
  - `time bun-1.2.12 matmul.js`: executed in 2.47 seconds.
  - `time node matmul.js`: executed in 1.76 seconds.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
- Bun's JavaScript runtime regressed on the PLB2 `matmul.js` workload after Bun 1.1.4, with Bun 1.1.5 and 1.2.2 running much slower.

2. Evidence
- Reporter measured Bun 1.1.4 at 1.8 seconds on Mac M1.
- The same script took 4.5 seconds on Bun 1.1.5 and Bun 1.2.2.
- Node 18.20.3 and Deno 1.39.1 were reported at 3.1 seconds, faster than the affected Bun versions but slower than Bun 1.1.4.
- Maintainer resolution timing shows a canary at 1.32 seconds versus Bun 1.2.12 at 2.47 seconds and Node at 1.76 seconds.
- PR #19467, `sync webkit`, merged and closed the issue, with the fix expected in Bun 1.2.13.

3. Missing evidence
- The prompt does not include repeated runs, variance, hardware details beyond Mac M1/Darwin arm64, or profiler output.
- The discussion points to JavaScriptCore, but the provided evidence does not isolate the exact engine change responsible.
- No direct timing is shown for Bun 1.2.13 release itself.

4. Recommended next diagnostic step
- Run repeated `matmul.js` timings and CPU profiles across Bun 1.1.4, 1.1.5, 1.2.12, the fixed canary, and Bun 1.2.13 to confirm the regression window and the fix's release behavior.
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
# c29 Bun #17000 Runtime Regression

Source: https://github.com/oven-sh/bun/issues/17000

Status: accepted

Verification date: 2026-05-02

Summary: Bun issue #17000 reports a JavaScript runtime performance regression between Bun 1.1.4 and 1.1.5+ on a public `matmul.js` script from the PLB2 benchmark set. The issue body reports 1.8 seconds on Bun 1.1.4 and 4.5 seconds on Bun 1.1.5 and Bun 1.2.2, slower than Node 18.20.3 and Deno 1.39.1 at 3.1 seconds. Discussion identified JavaScriptCore as the likely source. PR #19467, `sync webkit`, merged and closed the issue; a maintainer comment says the fix would ship in Bun 1.2.13 and gives canary timing of 1.32 seconds versus Bun 1.2.12 at 2.47 seconds.

Raw performance evidence confirmed:
- Bun 1.1.4: 1.8 seconds.
- Bun 1.1.5 and Bun 1.2.2: 4.5 seconds.
- Node 18.20.3 and Deno 1.39.1: 3.1 seconds.
- Fixed canary: 1.32 seconds.
- Bun 1.2.12: 2.47 seconds.

Resolution evidence confirmed:
- PR #19467 `sync webkit` merged on 2025-05-06 and closes issue #17000.
- Maintainer comment says the fix would be in Bun 1.2.13.
- Reporter replied with thanks after fix evidence.

normalized.csv: created from visible timing values in the issue body and resolution comment.

RAW EVIDENCE:
Source: https://github.com/oven-sh/bun/issues/17000

Issue title: Performance regression between v1.1.4 and v1.1.5+

Raw performance evidence:

- Reproduction:
  - `wget https://raw.githubusercontent.com/attractivechaos/plb2/refs/heads/master/src/javascript/matmul.js`
  - `time bun matmul.js`
- Reporter platform: Darwin 24.2.0 arm64 arm.
- Reporter timing on Mac M1:
  - Bun 1.1.4: 1.8 seconds.
  - Bun 1.1.5 and Bun 1.2.2: 4.5 seconds.
  - Node 18.20.3 and Deno 1.39.1: 3.1 seconds.
- Reporter says expected behavior is that the script should take 1.8 seconds.
- Reporter says current behavior is 4.5 seconds, slower than Node/Deno.

Resolution timing evidence from maintainer comment:
- New canary build on macOS:
  - `time bun matmul.js`: executed in 1.32 seconds.
  - `time bun-1.2.12 matmul.js`: executed in 2.47 seconds.
  - `time node matmul.js`: executed in 1.76 seconds.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 8 condition labels across 8 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] release_resolution_metadata: c29_bun_17000_runtime_regression.matmul_runtime_value_seconds at bun_fixed_canary, confidence=0.74
      Evidence: version/release/fix labels are present; preserve introduced, regressed, reverted, fixed, or canary metadata alongside metric deltas
      fixed: bun_fixed_canary
      canary: bun_fixed_canary
      versions: bun_1_1_4, bun_1_1_5, bun_1_2_12, bun_1_2_2, deno_1_39_1, node_18_20_3
  [2] runtime_engine_attribution_gate: c29_bun_17000_runtime_regression.matmul_runtime_value_seconds at bun_fixed_canary, confidence=0.75
      Evidence: runtime-engine or JS-engine context is present, but exact attribution requires profile, bisection, or upstream fix notes; treat engine sync as resolution context until then
      gate: profiles_or_bisection_required_before_exact_runtime_root_cause
  [3] mechanism_evidence: c29_bun_17000_runtime_regression.matmul_runtime_value_seconds at bun_1_1_4, confidence=0.72
      Evidence: named low-level mechanisms appear in the evidence; retain them as evidence labels without promoting them to root cause unless backed by profiling, bisection, or owner notes
      mechanisms: runtime
  [4] condition_delta: c29_bun_17000_runtime_regression.matmul_runtime_value_seconds at bun_fixed_canary (1.32 -> 4.5), confidence=0.89
      Evidence: matmul_runtime_value_seconds changes across benchmark conditions; min=1.32 at bun_fixed_canary; max=4.5 at bun_1_1_5; ratio=3.41x; compare conditions before explaining cause
  [5] version_fix_lineage: c29_bun_17000_runtime_regression.matmul_runtime_value_seconds at bun_fixed_canary, confidence=0.76
      Evidence: versioned regression and fixed/canary conditions are present; preserve fix lineage alongside the timing delta

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c29_bun_17000_runtime_regression.matmul_runtime_value_seconds has release/fix lineage; preserve versions, revert, fixed, and canary labels before explaining cause.
  Option C: this is sparse benchmark evidence; preserve condition labels and deltas.
  Option C: preserve named mechanisms as evidence labels, not automatic root cause.
  Option C: release/fix metadata can be the strongest resolution evidence.
  Option C: runtime-engine attribution needs profiles, bisection, or upstream fix notes.
  Option D: detector output is incomplete; request more metrics if evidence is thin.

GUARDRAIL:
  Do not turn timing into causality without dependency, deploy, or resource evidence.

Return concise structured findings.
```

## Trace-On Response

```text
1. Performance issue

Bun runtime performance on the PLB2 `matmul.js` workload regressed after Bun 1.1.4, with Bun 1.1.5 and 1.2.2 taking much longer than the earlier Bun version and slower than the cited Node/Deno comparison. Later canary evidence shows the workload improving past both the regressed and original Bun timings.

2. Evidence

- Bun 1.1.4 ran `matmul.js` in 1.8 seconds.
- Bun 1.1.5 and Bun 1.2.2 ran the same workload in 4.5 seconds, about 2.5x slower than 1.1.4.
- Node 18.20.3 and Deno 1.39.1 were reported at 3.1 seconds, faster than regressed Bun but slower than Bun 1.1.4.
- Maintainer fix evidence reports a canary at 1.32 seconds, Bun 1.2.12 at 2.47 seconds, and Node at 1.76 seconds on macOS.
- Public resolution links the fix to merged PR #19467, `sync webkit`, planned for Bun 1.2.13.

3. Missing evidence

- Direct JavaScriptCore or Bun profiling data showing which operation in `matmul.js` slowed down.
- Repeated timing distributions for each runtime/version on the same hardware.
- A commit-by-commit bisect between Bun 1.1.4 and 1.1.5 isolating the first bad runtime change.

4. Recommended next diagnostic step

Run `matmul.js` across Bun 1.1.4, 1.1.5, 1.2.2, 1.2.12, and the fixed canary on the same host with repeated trials and runtime profiles. Use the profiles to identify the changed execution path before treating JavaScriptCore/WebKit as proven root cause.
```

## Verdict Review

```text
Winner: similar

Reason: Both outputs correctly identify the Bun 1.1.4 to 1.1.5/1.2.2 matmul regression and the fixed-canary improvement. Baseline keeps a little more release metadata, while trace-on better frames WebKit/JavaScriptCore as supported by resolution evidence but not isolated by profiling.

Engine action: Preserve version-fix-lineage detection and add explicit runtime-engine attribution gating: require profiles or bisection before elevating a WebKit/JSC sync from resolution context to exact root cause.
```
