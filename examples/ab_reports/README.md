# A/B Reports

These reports document the research comparison format:

1. baseline prompt with raw public input only
2. baseline model response
3. trace-on prompt with the same raw input plus Change-Point trace
4. trace-on model response
5. review verdict

The reports intentionally exclude private working notes and local paths. They are included so users can inspect what changed between raw-log analysis and trace-assisted analysis.

## Benchmark 25

- [`c01_vllm_7592_scheduler_regression`](benchmark_25/c01_vllm_7592_scheduler_regression.md)
- [`c02_vllm_19954_ttft_explosion`](benchmark_25/c02_vllm_19954_ttft_explosion.md)
- [`c03_vllm_3297_4gpu_8gpu`](benchmark_25/c03_vllm_3297_4gpu_8gpu.md)
- [`c04_pytorch_161878_cpu_inductor`](benchmark_25/c04_pytorch_161878_cpu_inductor.md)
- [`c05_llama_cpp_3479_batched_cuda`](benchmark_25/c05_llama_cpp_3479_batched_cuda.md)
- [`c06_triton_4483_batch_latency`](benchmark_25/c06_triton_4483_batch_latency.md)
- [`c07_triton_4379_response_cache`](benchmark_25/c07_triton_4379_response_cache.md)
- [`c08_ray_tune_utilization_collapse`](benchmark_25/c08_ray_tune_utilization_collapse.md)
- [`c09_pydantic_startup_regression`](benchmark_25/c09_pydantic_startup_regression.md)
- [`c11_cloudflare_2019_waf_outage`](benchmark_25/c11_cloudflare_2019_waf_outage.md)
- [`c12_cloudflare_2025_outage`](benchmark_25/c12_cloudflare_2025_outage.md)
- [`c13_github_jan_2025_db_query`](benchmark_25/c13_github_jan_2025_db_query.md)
- [`c14_datadog_network_cache_bottleneck`](benchmark_25/c14_datadog_network_cache_bottleneck.md)
- [`c15_openshift_kubelet_regression`](benchmark_25/c15_openshift_kubelet_regression.md)
- [`c16_percona_server_lp1631309`](benchmark_25/c16_percona_server_lp1631309.md)
- [`c17_mysql_92360_ssl_defaults`](benchmark_25/c17_mysql_92360_ssl_defaults.md)
- [`c18_mysql_111353_alter_table_force`](benchmark_25/c18_mysql_111353_alter_table_force.md)
- [`c19_go_67585_runtime_mutex_regression`](benchmark_25/c19_go_67585_runtime_mutex_regression.md)
- [`c21_quarkus_38683_native_image`](benchmark_25/c21_quarkus_38683_native_image.md)
- [`c23_kafka_producer_regression`](benchmark_25/c23_kafka_producer_regression.md)
- [`c24_node_js_file_loading_regression`](benchmark_25/c24_node_js_file_loading_regression.md)
- [`c25_vite_503_dev_regression`](benchmark_25/c25_vite_503_dev_regression.md)
- [`c26_vite_6030_windows_startup_regression`](benchmark_25/c26_vite_6030_windows_startup_regression.md)
- [`c28_bun_23120_test_runner_regression`](benchmark_25/c28_bun_23120_test_runner_regression.md)
- [`c29_bun_17000_runtime_regression`](benchmark_25/c29_bun_17000_runtime_regression.md)

## Early Real-Data Reports

- [`vllm_qwen3_awq_concurrency_2025`](early_real_data/vllm_qwen3_awq_concurrency_2025.md)
- [`pytorch_and_vllm_full_prompts_outputs`](early_real_data/pytorch_and_vllm_full_prompts_outputs.md)
