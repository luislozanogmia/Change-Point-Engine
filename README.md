# Change-Point Engine

Research preview for deterministic performance traces.

Change-Point Engine is a 0-parameter performance analysis tool that turns benchmark, incident, and observability data into deterministic traces. It surfaces change type, metric shifts, load cliffs, tail latency, fix windows, release lineage, and evidence guardrails before any root-cause explanation.

It does **not** decide root cause. It computes structure first so an engineer or AI agent can explain the performance issue from evidence instead of starting from noisy logs.

## Status

This is a research preview, not a production monitoring product.

- API stability: experimental
- Input schema: stable enough for trials
- Detectors: evolving from real-world cases
- Intended users: performance engineers, SREs, AI agents, benchmark reviewers

## Install

No runtime dependencies are required.

```bash
git clone https://github.com/luislozanogmia/Change-Point-Engine.git
cd Change-Point-Engine
python3 change_trace_engine.py examples/perf_trace.csv
```

Run tests:

```bash
python3 -m unittest tests/test_change_trace_engine.py
```

## Input

Use a CSV with four columns:

```csv
timestamp,service,metric,value
10:42:00,auth,p95_latency_ms,180
10:42:05,auth,p95_latency_ms,182
10:42:10,auth,p95_latency_ms,620
```

`timestamp` can also be a condition label for benchmark tables:

```csv
timestamp,service,metric,value
baseline,kafka,throughput_records_per_second,115000
regressed,kafka,throughput_records_per_second,105000
reverted,kafka,throughput_records_per_second,115000
confirmed_fixed,kafka,throughput_records_per_second,117000
```

## CLI

Run a trace:

```bash
python3 change_trace_engine.py examples/perf_trace.csv
```

Run one of the benchmark examples:

```bash
python3 change_trace_engine.py examples/benchmark_25/c07_triton_4379_response_cache/input.csv
```

Normalize a Datadog-style export:

```bash
python3 change_trace_engine.py datadog_export.csv --normalize --source datadog > trace_input.csv
python3 change_trace_engine.py trace_input.csv
```

## Agent Use

Any model can use the trace. For simple summarization, small local models can work. For agentic workflows that compare evidence, inspect logs, fetch source issues, or decide next diagnostics, use frontier models.

Recommended agent instruction:

```text
Use Change-Point Engine before explaining a performance issue.
1. Convert available metrics/log tables to timestamp,service,metric,value CSV.
2. Run: python3 change_trace_engine.py <csv>
3. Treat the trace as structured evidence, not root-cause proof.
4. Explain the issue using the trace, raw evidence, and missing-evidence guardrails.
5. Do not invent root cause without deploy, dependency, profile, bisection, or owner evidence.
```

See [AGENTS.md](AGENTS.md) for a copy-paste agent workflow.

## Detector Families

Current detector families include:

- `mean_shift`
- `event_rate_shift`
- `variance_shift`
- `trend_shift`
- `downstream_lag`
- `distribution_tail_shift`
- `cross_sectional_regression_outlier`
- `load_scaling_saturation`
- `tail_amplification_under_load`
- `mean_median_divergence`
- `parameter_sweep_cliff`
- `condition_delta`
- `phase_delta`
- `capacity_underuse`
- `resource_saturation`
- `impact_spike`
- `impact_window`
- `config_expansion`
- `batch_work_scaling`
- `control_plane_accumulation`
- `fix_validation_window`
- `profile_hotspot`
- `version_fix_lineage`
- `database_error_incident`
- `phased_remediation`
- `cache_cardinality_shift`
- `mechanism_evidence`
- `release_resolution_metadata`
- `runtime_engine_attribution_gate`

## What Worked

In the 25-case research benchmark, trace-on analysis beat or matched baseline analysis in every accepted case.

Result after general detector updates:

| Outcome | Count |
|---|---:|
| Trace-on wins | 19/25 |
| Similar | 6/25 |
| Baseline wins | 0/25 |

After the edge-case updates, six former ties were rerun:

| Outcome | Count |
|---|---:|
| Trace-on wins | 5/6 |
| Similar | 1/6 |
| Baseline wins | 0/6 |

The strongest trace gains appeared when the raw evidence was noisy, sparse, or mixed across conditions:

- Load and parameter sweeps
- Tail-latency regressions
- Baseline/regressed/fixed windows
- Version and canary validation
- Cache hit vs high-cardinality miss behavior
- Multi-phase remediation stories
- Runtime attribution where profiles or bisection were missing

## What Did Not Work

The trace is less differentiated when the source is already a polished incident postmortem. Cloudflare's WAF outage remained similar because the public write-up already contained deployment timing, CPU saturation, 502s, traffic loss, mitigation, and recovery.

The engine also does not replace missing observability. If the public issue has no raw data, no fix evidence, or only screenshots, the trace should ask for more evidence instead of manufacturing certainty.

## Edge Cases That Changed the Engine

The benchmark surfaced gaps that became new detector families:

| Edge Case | Problem | Update |
|---|---|---|
| Triton response cache | Repeated inputs were fast, random unique inputs degraded. | Added `cache_cardinality_shift`. |
| Datadog remote cache | Baseline preserved mechanism detail better than trace. | Added `mechanism_evidence`. |
| Percona sysbench regression | Version and rollback labels mattered. | Added `release_resolution_metadata`. |
| Kafka producer regression | Revert/fix lineage mattered; partitioner was tested but not proven. | Improved `fix_validation_window` and `mechanism_evidence`. |
| Bun runtime regression | WebKit/runtime context was resolution evidence, not exact cause. | Added `runtime_engine_attribution_gate`. |
| Cloudflare WAF outage | Trace added little over a strong postmortem. | Kept as a control case for "similar is acceptable." |

## Research Path

### v0.01

Initial timestamped service trace:

- Mean shifts
- Event-rate shifts
- Variance/trend shifts
- Downstream timing relationships
- Root-cause guardrail

### v0.02

Benchmark-shape routing:

- Percentile distribution routing
- Cross-sectional benchmark regression
- Load/concurrency scaling
- Mean/median divergence
- Tail amplification under load

### v0.03

Sparse real-world case support:

- Condition tables
- Phase deltas
- Resource saturation
- Impact windows
- Config expansion
- Batch work scaling
- Control-plane accumulation
- Fix-validation windows
- Profile hotspots
- Version/fix lineage
- Database incident evidence
- Phased remediation

### v0.04

Edge-case pass:

- Cache-cardinality shifts
- Named mechanism evidence
- Release-resolution metadata
- Runtime-engine attribution gating

### v0.05 Candidates

Potential next work:

- Better HAR and Datadog normalization
- First-class pprof/flamegraph import
- Confidence calibration across detector families
- JSON output mode
- Agent benchmark harness
- More public benchmark cases with raw data and verified fixes

## Repo Layout

| Path | Purpose |
|---|---|
| `change_trace_engine.py` | Core 0-parameter trace engine and CLI |
| `examples/` | Input/output examples, including the 25-case benchmark set |
| `tests/` | Unit tests and minimal CSV fixtures for detector families and edge cases |
| `tools/build_case_prompts.py` | Research helper for A/B prompt generation |
| `tools/github_case_harvest.py` | Research helper for finding public issue candidates |

See [examples/README.md](examples/README.md) for the full input/output example index.

## License

MIT. See [LICENSE](LICENSE).
