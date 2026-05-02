# Examples

This directory contains input/output examples for the Change-Point Engine.

## Quick Example

Run the small synthetic service trace:

```bash
python3 change_trace_engine.py examples/perf_trace.csv
```

## Real-World-Style Examples

Five compact incident-style examples live in `examples/real_world/`.

Each input CSV has a matching generated trace in `examples/real_world_outputs/`.

| Input | Output |
|---|---|
| `examples/real_world/calcom_2026_db_cascade.csv` | `examples/real_world_outputs/calcom_2026_db_cascade.trace.txt` |
| `examples/real_world/clerk_2025_auth_contention.csv` | `examples/real_world_outputs/clerk_2025_auth_contention.trace.txt` |
| `examples/real_world/cloudflare_2025_bot_feature_file.csv` | `examples/real_world_outputs/cloudflare_2025_bot_feature_file.trace.txt` |
| `examples/real_world/github_2024_db_query.csv` | `examples/real_world_outputs/github_2024_db_query.trace.txt` |
| `examples/real_world/spotify_2025_envoy_retry.csv` | `examples/real_world_outputs/spotify_2025_envoy_retry.trace.txt` |

## Benchmark 25

The `examples/benchmark_25/` directory contains 25 sanitized benchmark/incident examples from the research run.

Each case contains:

- `input.csv`: normalized `timestamp,service,metric,value` input
- `output.trace.txt`: generated Change-Point Engine output

These examples intentionally exclude raw issue dumps, prompts, evaluator outputs, and private working artifacts. They are meant to show how the engine routes different performance data shapes and what trace structure it produces.

For the full A/B comparison format, use `examples/ab_reports/`. Those reports show:

1. baseline prompt with raw public input only
2. baseline model response
3. trace-on prompt with the same raw input plus Change-Point trace
4. trace-on model response
5. review verdict

| Case | Pattern Highlight |
|---|---|
| `c01_vllm_7592_scheduler_regression` | scheduler/control-plane regression |
| `c02_vllm_19954_ttft_explosion` | TTFT/tail-latency explosion |
| `c03_vllm_3297_4gpu_8gpu` | condition delta across GPU count |
| `c04_pytorch_161878_cpu_inductor` | benchmark regression matrix |
| `c05_llama_cpp_3479_batched_cuda` | batch work scaling |
| `c06_triton_4483_batch_latency` | batch-size latency cliff |
| `c07_triton_4379_response_cache` | cache-cardinality shift |
| `c08_ray_tune_utilization_collapse` | control-plane accumulation and low utilization |
| `c09_pydantic_startup_regression` | startup regression condition delta |
| `c11_cloudflare_2019_waf_outage` | resource saturation and impact window |
| `c12_cloudflare_2025_outage` | phased incident remediation |
| `c13_github_jan_2025_db_query` | database/query incident evidence |
| `c14_datadog_network_cache_bottleneck` | phased remediation and mechanism evidence |
| `c15_openshift_kubelet_regression` | versioned performance regression |
| `c16_percona_server_lp1631309` | version and rollback metadata |
| `c17_mysql_92360_ssl_defaults` | version/config regression |
| `c18_mysql_111353_alter_table_force` | database operation regression |
| `c19_go_67585_runtime_mutex_regression` | runtime/profile hotspot |
| `c21_quarkus_38683_native_image` | fix-validation window |
| `c23_kafka_producer_regression` | baseline/regressed/reverted/fixed lineage |
| `c24_node_js_file_loading_regression` | file-loading regression |
| `c25_vite_503_dev_regression` | dev-server performance regression |
| `c26_vite_6030_windows_startup_regression` | platform-specific startup regression |
| `c28_bun_23120_test_runner_regression` | release-to-release test-runner regression |
| `c29_bun_17000_runtime_regression` | runtime attribution gating |

## A/B Reports

The A/B reports are indexed here:

```text
examples/ab_reports/README.md
```

They include all 25 benchmark cases plus the earlier vLLM/PyTorch reports used while developing the engine.
