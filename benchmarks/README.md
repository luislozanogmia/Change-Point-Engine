# Benchmarks

This directory contains the public A/B reports from the Change-Point Engine research run.

Each numbered report preserves the comparison format used during development:

1. normalized engine input
2. generated Change-Point trace
3. baseline prompt with raw input only
4. baseline model response
5. trace-on prompt with the same raw input plus the trace
6. trace-on model response
7. review verdict

The reports are included so reviewers can inspect what changed between raw-input analysis and trace-assisted analysis. The trace is not treated as root-cause proof; it surfaces structure, candidate change-point type, evidence, and missing-evidence guardrails.

## What Was Used

The set currently contains 27 complete reports:

- 25 benchmark and incident cases from the overnight research set.
- 2 earlier real-data reports used while developing and debugging the engine.

The cases were normalized into the engine's required CSV shape:

```csv
timestamp,service,metric,value
```

For benchmark tables, `timestamp` can be a condition label such as `baseline`, `regressed`, `fixed`, `batch_16`, or `version_1_2_0`.

## Reports

| # | Report |
|---:|---|
| 01 | [vLLM scheduler regression](01_vllm_7592_scheduler_regression.md) |
| 02 | [vLLM TTFT explosion](02_vllm_19954_ttft_explosion.md) |
| 03 | [vLLM 4 GPU vs 8 GPU](03_vllm_3297_4gpu_8gpu.md) |
| 04 | [PyTorch CPU Inductor regression](04_pytorch_161878_cpu_inductor.md) |
| 05 | [llama.cpp batched CUDA regression](05_llama_cpp_3479_batched_cuda.md) |
| 06 | [Triton batch latency](06_triton_4483_batch_latency.md) |
| 07 | [Triton response cache](07_triton_4379_response_cache.md) |
| 08 | [Ray Tune utilization collapse](08_ray_tune_utilization_collapse.md) |
| 09 | [Pydantic startup regression](09_pydantic_startup_regression.md) |
| 10 | [Cloudflare 2019 WAF outage](10_cloudflare_2019_waf_outage.md) |
| 11 | [Cloudflare 2025 outage](11_cloudflare_2025_outage.md) |
| 12 | [GitHub January 2025 database query incident](12_github_jan_2025_db_query.md) |
| 13 | [Datadog network cache bottleneck](13_datadog_network_cache_bottleneck.md) |
| 14 | [OpenShift kubelet regression](14_openshift_kubelet_regression.md) |
| 15 | [Percona server LP1631309](15_percona_server_lp1631309.md) |
| 16 | [MySQL SSL defaults regression](16_mysql_92360_ssl_defaults.md) |
| 17 | [MySQL ALTER TABLE FORCE regression](17_mysql_111353_alter_table_force.md) |
| 18 | [Go runtime mutex regression](18_go_67585_runtime_mutex_regression.md) |
| 19 | [Quarkus native image regression](19_quarkus_38683_native_image.md) |
| 20 | [Kafka producer regression](20_kafka_producer_regression.md) |
| 21 | [Node.js file loading regression](21_node_js_file_loading_regression.md) |
| 22 | [Vite 503 dev regression](22_vite_503_dev_regression.md) |
| 23 | [Vite Windows startup regression](23_vite_6030_windows_startup_regression.md) |
| 24 | [Bun test runner regression](24_bun_23120_test_runner_regression.md) |
| 25 | [Bun runtime regression](25_bun_17000_runtime_regression.md) |
| 26 | [vLLM Qwen3 AWQ concurrency](26_vllm_qwen3_awq_concurrency_2025.md) |
| 27 | [PyTorch and vLLM full prompts and outputs](27_pytorch_and_vllm_full_prompts_outputs.md) |

