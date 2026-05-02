# Examples

This directory contains small runnable CSV inputs for the Change-Point Engine.

Full raw-input/baseline/trace-on/review A/B reports live in [`../benchmarks/`](../benchmarks/README.md).

## Quick Example

Run the small synthetic service trace:

```bash
python3 change_trace_engine.py examples/perf_trace.csv
```

## Real-World-Style Examples

Five compact incident-style examples live in `examples/real_world/`.

Run any CSV directly through the engine:

```bash
python3 change_trace_engine.py examples/real_world/spotify_2025_envoy_retry.csv
```

| Input |
|---|---|
| `examples/real_world/calcom_2026_db_cascade.csv` |
| `examples/real_world/clerk_2025_auth_contention.csv` |
| `examples/real_world/cloudflare_2025_bot_feature_file.csv` |
| `examples/real_world/github_2024_db_query.csv` |
| `examples/real_world/spotify_2025_envoy_retry.csv` |
