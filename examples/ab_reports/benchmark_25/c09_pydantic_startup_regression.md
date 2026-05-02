# A/B Report: `c09_pydantic_startup_regression`

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
reporter_says_startup_was_about_5_seconds_before_v2,c09_pydantic_startup_regression,startup_before_pydantic_v2_s,5.0
reporter_says_startup_was_over_20_seconds_after_v2,c09_pydantic_startup_regression,startup_after_pydantic_v2_lower_bound_s,20.0
reporter_comment_says_memoization_reduced_initialization_from_about_20_s_to_about_10_s,c09_pydantic_startup_regression,startup_after_fieldinfo_typeadapter_memoization_s,10.0
reporter_closing_comment_says_services_start_in_about_7_seconds,c09_pydantic_startup_regression,startup_after_resolution_s,7.0
pydantic_v2_0_3_fastapi_v0_100_0_cprofile_walk_cumulative_time,c09_pydantic_startup_regression,pydantic_v2_walk_cumtime_s,20.191
pydantic_v2_0_3_fastapi_v0_100_0_cprofile_walk_cumulative_time,c09_pydantic_startup_regression,pydantic_v2_walk_cumtime_s,18.577
pydantic_v2_0_3_fastapi_v0_100_0_cprofile_typeadapter_init_cumulative_time,c09_pydantic_startup_regression,pydantic_v2_typeadapter_init_cumtime_s,31.855
pydantic_v1_10_10_fastapi_v0_100_0_cprofile_create_response_field_cumulative_time,c09_pydantic_startup_regression,pydantic_v1_fastapi_100_create_response_field_cumtime_s,1.593
pydantic_v1_10_10_fastapi_v0_99_1_cprofile_dependencies_model_init_cumulative_time,c09_pydantic_startup_regression,pydantic_v1_fastapi_099_dependencies_init_cumtime_s,0.521
reporter_comment_with_patched_walk_timing,c09_pydantic_startup_regression,walk_entries_count_count,2639.0
reporter_comment_with_patched_walk_timing,c09_pydantic_startup_regression,walk_total_duration_s,15.628021955490112
top_patched_walk_timing_entry,c09_pydantic_startup_regression,top_walk_definition_ref_duration_s,2.6756765842437744
top_patched_walk_timing_entry,c09_pydantic_startup_regression,top_walk_default_duration_s,1.8995928764343262
reporter_says_initial_memory_usage_was_like_2x_better,c09_pydantic_startup_regression,memory_improvement_after_resolution_x,2.0
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
# c09 Pydantic startup regression

Source: https://github.com/pydantic/pydantic/issues/6768

Status: accepted

Raw performance evidence exists: yes. The issue reports FastAPI application startup degrading from about 5 s to over 20 s after moving to Pydantic v2, and includes cProfile tables for Pydantic v2.0.3/FastAPI v0.100.0 versus Pydantic v1.10.10/FastAPI v0.100.0 and v0.99.1. Later comments add measured `walk` duration data.

Resolution evidence exists: yes. A maintainer asked whether the reporter was okay closing the issue, and the reporter agreed after seeing startup around 7 s, close to the old Pydantic v1 behavior. The reporter specifically cites https://github.com/pydantic/pydantic/pull/11434 as the fix that made a big improvement and reduced initial memory usage by about 2x. The issue is closed as completed.

Normalization: feasible from visible startup and profile numbers. `normalized.csv` captures startup-time claims, profile cumulative times, and the final resolved startup observation.

RAW EVIDENCE:
Public source: https://github.com/pydantic/pydantic/issues/6768

Relevant raw performance evidence from the issue body:

- The reporter states FastAPI application startup degraded from about 5 s to over 20 s after using Pydantic v2.
- Pydantic v2.0.3 with FastAPI v0.100.0 cProfile highlights:
  - `_core_utils.py:193(_walk)`: 3854141/395376 calls, 3.575 s tottime, 18.577 s cumtime.
  - `_core_utils.py:190(walk)`: 3850208/395376 calls, 3.395 s tottime, 20.191 s cumtime.
  - `type_adapter.py:142(__init__)`: 9812 calls, 1.773 s tottime, 31.855 s cumtime.
- Pydantic v1.10.10 with FastAPI v0.100.0 cProfile highlights:
  - `_abc._abc_subclasscheck`: 871294/78525 calls, 2.790 s tottime, 3.005 s cumtime.
  - `copy.py:128(deepcopy)`: 545241/8813 calls, 0.775 s tottime, 1.942 s cumtime.
  - `fastapi/utils.py:63(create_response_field)`: 10618 calls, 0.490 s tottime, 1.593 s cumtime.
- Pydantic v1.10.10 with FastAPI v0.99.1 cProfile highlights:
  - `_abc._abc_subclasscheck`: 858955/76183 calls, 1.997 s tottime, 2.190 s cumtime.
  - `copy.py:128(deepcopy)`: 538585/2157 calls, 0.825 s tottime, 1.788 s cumtime.
  - `fastapi/dependencies/models.py:16(__init__)`: 23230 calls, 0.509 s tottime, 0.521 s cumtime.

Additional visible raw evidence from comments:

- Memoizing FastAPI FieldInfo-to-TypeAdapter mapping reportedly reduced initialization time from about 20 s to about 10 s.
- A later `walk` timing sample reports ENTRIES COUNT 2639 and TOTAL DURATION 15.628021955490112 s, with top entries including `definition-ref:<unknown>` at 2.6756765842437744 s and `default:<unknown>` at 1.8995928764343262 s.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
FastAPI application startup regresses substantially after moving to Pydantic v2, with startup rising from about 5 seconds to over 20 seconds.

2. Evidence
- Reporter states startup increased from about 5 s to over 20 s after using Pydantic v2.
- Pydantic v2.0.3/FastAPI v0.100.0 profile shows heavy time in schema walking and TypeAdapter construction:
  - `_core_utils.py:190(walk)`: 20.191 s cumulative.
  - `_core_utils.py:193(_walk)`: 18.577 s cumulative.
  - `type_adapter.py:142(__init__)`: 31.855 s cumulative across 9,812 calls.
- Pydantic v1 profiles show top cumulative times around 1.6-3.0 s for comparable visible hotspots.
- Memoizing FastAPI FieldInfo-to-TypeAdapter mapping reportedly reduces initialization from about 20 s to about 10 s.
- Later resolution reports startup around 7 s and about 2x lower initial memory after PR #11434.

3. Missing evidence
- No complete application reproduction or exact model/route structure in the provided evidence.
- No full before/after profile for PR #11434 in the prompt.
- No isolated attribution between FastAPI integration behavior and Pydantic core behavior beyond profile hotspots.

4. Recommended next diagnostic step
Capture a minimal reproducible FastAPI app and compare profiles across Pydantic v1, early v2, and the fixed version, focusing on TypeAdapter creation, schema walking, and repeated FieldInfo-to-TypeAdapter construction.
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
# c09 Pydantic startup regression

Source: https://github.com/pydantic/pydantic/issues/6768

Status: accepted

Raw performance evidence exists: yes. The issue reports FastAPI application startup degrading from about 5 s to over 20 s after moving to Pydantic v2, and includes cProfile tables for Pydantic v2.0.3/FastAPI v0.100.0 versus Pydantic v1.10.10/FastAPI v0.100.0 and v0.99.1. Later comments add measured `walk` duration data.

Resolution evidence exists: yes. A maintainer asked whether the reporter was okay closing the issue, and the reporter agreed after seeing startup around 7 s, close to the old Pydantic v1 behavior. The reporter specifically cites https://github.com/pydantic/pydantic/pull/11434 as the fix that made a big improvement and reduced initial memory usage by about 2x. The issue is closed as completed.

Normalization: feasible from visible startup and profile numbers. `normalized.csv` captures startup-time claims, profile cumulative times, and the final resolved startup observation.

RAW EVIDENCE:
Public source: https://github.com/pydantic/pydantic/issues/6768

Relevant raw performance evidence from the issue body:

- The reporter states FastAPI application startup degraded from about 5 s to over 20 s after using Pydantic v2.
- Pydantic v2.0.3 with FastAPI v0.100.0 cProfile highlights:
  - `_core_utils.py:193(_walk)`: 3854141/395376 calls, 3.575 s tottime, 18.577 s cumtime.
  - `_core_utils.py:190(walk)`: 3850208/395376 calls, 3.395 s tottime, 20.191 s cumtime.
  - `type_adapter.py:142(__init__)`: 9812 calls, 1.773 s tottime, 31.855 s cumtime.
- Pydantic v1.10.10 with FastAPI v0.100.0 cProfile highlights:
  - `_abc._abc_subclasscheck`: 871294/78525 calls, 2.790 s tottime, 3.005 s cumtime.
  - `copy.py:128(deepcopy)`: 545241/8813 calls, 0.775 s tottime, 1.942 s cumtime.
  - `fastapi/utils.py:63(create_response_field)`: 10618 calls, 0.490 s tottime, 1.593 s cumtime.
- Pydantic v1.10.10 with FastAPI v0.99.1 cProfile highlights:
  - `_abc._abc_subclasscheck`: 858955/76183 calls, 1.997 s tottime, 2.190 s cumtime.
  - `copy.py:128(deepcopy)`: 538585/2157 calls, 0.825 s tottime, 1.788 s cumtime.
  - `fastapi/dependencies/models.py:16(__init__)`: 23230 calls, 0.509 s tottime, 0.521 s cumtime.

Additional visible raw evidence from comments:

- Memoizing FastAPI FieldInfo-to-TypeAdapter mapping reportedly reduced initialization time from about 20 s to about 10 s.
- A later `walk` timing sample reports ENTRIES COUNT 2639 and TOTAL DURATION 15.628021955490112 s, with top entries including `definition-ref:<unknown>` at 2.6756765842437744 s and `default:<unknown>` at 1.8995928764343262 s.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 11 condition labels across 14 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] phased_remediation: c09_pydantic_startup_regression.memory_improvement_after_resolution_x at reporter_says_initial_memory_usage_was_like_2x_better, confidence=0.74
      Evidence: multiple after/post-remediation stages are present; preserve staged fixes and residual bottlenecks instead of collapsing to one before/after delta
  [2] release_resolution_metadata: c09_pydantic_startup_regression.memory_improvement_after_resolution_x at reporter_says_initial_memory_usage_was_like_2x_better, confidence=0.74
      Evidence: version/release/fix labels are present; preserve introduced, regressed, reverted, fixed, or canary metadata alongside metric deltas
      versions: pydantic_v2_0_3_fastapi_v0_100_0_cprofile_walk_cumulative_time, pydantic_v2_0_3_fastapi_v0_100_0_cprofile_typeadapter_init_cumulative_time, pydantic_v1_10_10_fastapi_v0_100_0_cprofile_create_response_field_cumulative_time, pydantic_v1_10_10_fastapi_v0_99_1_cprofile_dependencies_model_init_cumulative_time
  [3] profile_hotspot: c09_pydantic_startup_regression.startup_before_pydantic_v2_s at reporter_says_startup_was_about_5_seconds_before_v2, confidence=0.78
      Evidence: profile/hotspot counters appear with the regression evidence; inspect code-path attribution instead of only metric deltas
  [4] phase_delta: c09_pydantic_startup_regression.startup at reporter_says_startup_was_over_20_seconds_after_v2 (5.0 -> 20.0), confidence=0.71
      Evidence: sparse phase labels compare startup_before_pydantic_v2_s=5 with startup_after_pydantic_v2_lower_bound_s=20; ratio=4.00x
  [5] config_expansion: c09_pydantic_startup_regression.memory_improvement_after_resolution_x at reporter_says_initial_memory_usage_was_like_2x_better, confidence=0.78
      Evidence: memory_improvement_after_resolution_x is 2x, indicating a material expansion/change in generated configuration

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c09_pydantic_startup_regression.memory_improvement_after_resolution_x is the first visible shift.
  Option C: release/fix metadata can be the strongest resolution evidence.
  Option D: detector output is incomplete; request more metrics if evidence is thin.

GUARDRAIL:
  Do not turn timing into causality without dependency, deploy, or resource evidence.

Return concise structured findings.
```

## Trace-On Response

```text
## Performance issue
FastAPI application startup becomes substantially slower after moving to Pydantic v2, increasing from about 5 s to more than 20 s.

## Evidence
- Reporter states startup regressed from about 5 s to over 20 s after adopting Pydantic v2.
- Trace captures a 4.0x startup phase delta from 5 s to a lower bound of 20 s.
- Pydantic v2.0.3 / FastAPI v0.100.0 profile highlights heavy cumulative time in schema walking:
  - `_core_utils.py:190(walk)`: 20.191 s cumulative.
  - `_core_utils.py:193(_walk)`: 18.577 s cumulative.
  - `type_adapter.py:142(__init__)`: 31.855 s cumulative across 9,812 calls.
- Pydantic v1 profiles show lower top cumulative timings, around 1.5-3.0 s for listed hotspots.
- Later comments report memoizing FastAPI FieldInfo-to-TypeAdapter mapping reducing initialization from about 20 s to about 10 s.
- A later `walk` timing sample reports 2,639 entries and 15.628 s total duration.
- Trace also notes a reported 2x initial-memory improvement after resolution, but that is supporting evidence, not a root-cause finding.

## Missing evidence
- A controlled benchmark isolating Pydantic from FastAPI behavior.
- Call graph or allocation data explaining why `walk` and `TypeAdapter` construction expanded.
- Exact version range where the regression begins and where the improvement lands.
- Startup measurements across representative application sizes and schema shapes.

## Recommended next diagnostic step
Run a controlled startup benchmark with profiling and allocation tracing around `TypeAdapter` creation and schema walking, comparing Pydantic v1, early v2, and the fixed version on the same FastAPI app.
```

## Verdict Review

```text
Winner: trace-on

Concise reason: Trace-on keeps the baseline root issue and adds the structured 4x startup phase delta, the repeated TypeAdapter/schema-walk evidence, and the memory-improvement signal without overstating causality.

Engine action: Keep phase-delta and config-expansion signals for startup regressions. Improve ranking so startup latency remains primary and memory improvement is clearly secondary/resolution evidence.
```
