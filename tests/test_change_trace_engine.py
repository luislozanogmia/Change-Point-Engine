import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from change_trace_engine import ChangeTraceEngine, load_csv, normalize_export


FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "perf_trace.csv"
BENCHMARK_FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "tests"
    / "fixtures"
    / "quarkus_distribution_trace.csv"
)
PYTORCH_FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "tests"
    / "fixtures"
    / "pytorch_benchmark_regression.csv"
)
VLLM_FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "tests"
    / "fixtures"
    / "vllm_concurrency_scaling.csv"
)


class ChangeTraceEngineTests(unittest.TestCase):
    def test_auth_shift_is_first_visible_signal(self):
        engine = ChangeTraceEngine(load_csv(FIXTURE))
        blocks = engine.analyze()
        signal_blocks = [b for b in blocks if b.family in {"mean_shift", "throughput_plateau"}]

        self.assertGreaterEqual(len(signal_blocks), 3)
        first = min(signal_blocks, key=lambda b: b.index)
        self.assertEqual(first.service, "auth")
        self.assertEqual(first.metric, "p95_latency_ms")
        self.assertEqual(first.family, "mean_shift")

    def test_trace_surfaces_options_without_deciding_root_cause(self):
        engine = ChangeTraceEngine(load_csv(FIXTURE))
        trace = engine.format_trace()

        self.assertIn("DETECTOR ROUTE", trace)
        self.assertIn("timestamped_service_timeseries", trace)
        self.assertIn("does not decide root cause", trace)
        self.assertIn("OPTIONS FOR THE LLM TO WEIGH", trace)
        self.assertIn("auth.p95_latency_ms is the first visible shift", trace)
        self.assertIn("GUARDRAIL", trace)

    def test_downstream_lag_is_detected(self):
        engine = ChangeTraceEngine(load_csv(FIXTURE))
        blocks = engine.analyze()
        lag_blocks = [b for b in blocks if b.family == "downstream_lag"]

        self.assertTrue(
            any(
                b.service == "auth"
                and b.related_service in {"gateway", "checkout"}
                for b in lag_blocks
            )
        )

    def test_normalizes_datadog_wide_export(self):
        with TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "datadog_wide.csv"
            fixture.write_text(
                "\n".join(
                    [
                        "Time,avg:trace.http.request.duration{service:gateway},sum:trace.http.errors{service:checkout}",
                        "2026-04-15T10:00:00Z,120,0",
                        "2026-04-15T10:01:00Z,450,7",
                    ]
                ),
                encoding="utf-8",
            )

            rows = normalize_export(fixture, source="datadog")

        self.assertEqual(rows[0]["timestamp"], "2026-04-15T10:00:00Z")
        self.assertEqual(rows[0]["service"], "gateway")
        self.assertEqual(rows[0]["metric"], "trace.http.request.duration")
        self.assertEqual(rows[0]["value"], "120")
        self.assertEqual(rows[1]["service"], "checkout")
        self.assertEqual(rows[1]["metric"], "trace.http.errors")

    def test_normalizes_datadog_long_export(self):
        with TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "datadog_long.csv"
            fixture.write_text(
                "\n".join(
                    [
                        "timestamp,service,query,value",
                        "2026-04-15T10:00:00Z,auth,avg:auth.p95_latency_ms{env:prod},180",
                        "2026-04-15T10:01:00Z,auth,avg:auth.p95_latency_ms{env:prod},620",
                    ]
                ),
                encoding="utf-8",
            )

            rows = normalize_export(fixture, source="datadog")

        self.assertEqual(rows[0]["service"], "auth")
        self.assertEqual(rows[0]["metric"], "p95_latency_ms")
        self.assertEqual(rows[1]["value"], "620")

    def test_distribution_benchmark_routes_to_tail_shift_not_mean_shift(self):
        engine = ChangeTraceEngine(load_csv(BENCHMARK_FIXTURE))
        blocks = engine.analyze()
        trace = engine.format_trace(blocks)

        self.assertEqual(engine.route.data_shape, "benchmark_distribution")
        self.assertEqual(engine.route.selected_detectors, ("distribution_tail_shift",))
        self.assertTrue(any(b.family == "distribution_tail_shift" for b in blocks))
        self.assertFalse(any(b.family == "mean_shift" for b in blocks))
        self.assertIn("distribution_tail_shift", trace)
        self.assertIn("average latency may hide tail degradation", trace)

    def test_benchmark_matrix_routes_to_cross_sectional_regression(self):
        engine = ChangeTraceEngine(load_csv(PYTORCH_FIXTURE))
        blocks = engine.analyze()

        self.assertEqual(engine.route.data_shape, "benchmark_regression_table")
        self.assertEqual(engine.route.selected_detectors, ("cross_sectional_regression_outlier",))
        self.assertTrue(any(b.family == "cross_sectional_regression_outlier" for b in blocks))

    def test_concurrency_curve_routes_to_load_scaling_saturation(self):
        engine = ChangeTraceEngine(load_csv(VLLM_FIXTURE))
        blocks = engine.analyze()

        self.assertEqual(engine.route.data_shape, "load_scaling_curve")
        self.assertEqual(
            engine.route.selected_detectors,
            ("load_scaling_saturation", "tail_amplification_under_load", "mean_median_divergence"),
        )
        self.assertTrue(any(b.family == "load_scaling_saturation" for b in blocks))
        self.assertTrue(any(b.family == "mean_median_divergence" for b in blocks))
        self.assertTrue(any(b.family == "tail_amplification_under_load" for b in blocks))

    def test_load_parameter_sweep_routes_to_load_scaling(self):
        with TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "max_num_seqs.csv"
            fixture.write_text(
                "\n".join(
                    [
                        "timestamp,service,metric,value",
                        "max_num_seqs_1024,vllm_054_enable,requests_per_second,3.1797",
                        "max_num_seqs_768,vllm_054_enable,requests_per_second,4.1047",
                        "max_num_seqs_512,vllm_054_enable,requests_per_second,4.6486",
                        "max_num_seqs_384,vllm_054_enable,requests_per_second,4.7980",
                        "max_num_seqs_256,vllm_054_enable,requests_per_second,4.9096",
                        "max_num_seqs_128,vllm_054_enable,requests_per_second,4.2047",
                        "max_num_seqs_64,vllm_054_enable,requests_per_second,2.4350",
                        "max_num_seqs_32,vllm_054_enable,requests_per_second,1.6103",
                        "max_num_seqs_1024,vllm_054_enable,delay_ms,39.72",
                        "max_num_seqs_768,vllm_054_enable,delay_ms,43.4",
                        "max_num_seqs_512,vllm_054_enable,delay_ms,46.79",
                        "max_num_seqs_384,vllm_054_enable,delay_ms,49.66",
                        "max_num_seqs_256,vllm_054_enable,delay_ms,48.27",
                        "max_num_seqs_128,vllm_054_enable,delay_ms,32.77",
                        "max_num_seqs_64,vllm_054_enable,delay_ms,26.88",
                        "max_num_seqs_32,vllm_054_enable,delay_ms,19.83",
                    ]
                ),
                encoding="utf-8",
            )

            engine = ChangeTraceEngine(load_csv(fixture))

        self.assertEqual(engine.route.data_shape, "load_parameter_sweep")
        self.assertIn("load_scaling_saturation", engine.route.selected_detectors)

    def test_sparse_benchmark_routes_to_condition_delta(self):
        with TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "before_after.csv"
            fixture.write_text(
                "\n".join(
                    [
                        "timestamp,service,metric,value",
                        "before_fix,node_loader,load_time_ms,850",
                        "after_regression,node_loader,load_time_ms,3800",
                    ]
                ),
                encoding="utf-8",
            )

            engine = ChangeTraceEngine(load_csv(fixture))
            blocks = engine.analyze()

        self.assertEqual(engine.route.data_shape, "benchmark_condition_table")
        self.assertEqual(engine.route.selected_detectors, ("condition_delta",))
        self.assertTrue(any(b.family == "condition_delta" for b in blocks))

    def test_cache_cardinality_shift_is_detected_across_condition_labels(self):
        with TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "cache_cardinality.csv"
            fixture.write_text(
                "\n".join(
                    [
                        "timestamp,service,metric,value",
                        "repeated_identical_inputs,cache_case_repeated_identical_inputs,value_numeric,25000",
                        "random_inputs_start,cache_case_random_inputs_start,value_numeric,600",
                        "random_inputs_end,cache_case_random_inputs_end,value_numeric,100",
                        "response_cache_size,cache_case_response_cache_size,value_numeric,2000000000",
                    ]
                ),
                encoding="utf-8",
            )

            engine = ChangeTraceEngine(load_csv(fixture))
            blocks = engine.analyze()
            trace = engine.format_trace(blocks)

        self.assertTrue(any(b.family == "cache_cardinality_shift" for b in blocks))
        self.assertIn("cache-cardinality", trace)
        self.assertIn("repeated-input cache wins", trace)

    def test_mechanism_evidence_is_retained_without_root_cause_promotion(self):
        with TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "mechanisms.csv"
            fixture.write_text(
                "\n".join(
                    [
                        "timestamp,service,metric,value",
                        "baseline,remote_cache,p99_latency_ms,100",
                        "incident,remote_cache,p99_latency_spike_ms,1000",
                        "ena_bug,remote_cache,transmit_queues_used_bug_count,1",
                        "ena_bug,remote_cache,transmit_queues_available_count,8",
                        "after_prestop_hook,remote_cache,p99_remote_cache_latency_upper_ms,100",
                    ]
                ),
                encoding="utf-8",
            )

            trace = ChangeTraceEngine(load_csv(fixture)).format_trace()

        self.assertIn("mechanism_evidence", trace)
        self.assertIn("mechanisms:", trace)
        self.assertIn("transmit_queue", trace)
        self.assertIn("not automatic root cause", trace)

    def test_release_metadata_and_runtime_gate_are_retained(self):
        with TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "runtime_release.csv"
            fixture.write_text(
                "\n".join(
                    [
                        "timestamp,service,metric,value",
                        "bun_1_1_4,runtime,matmul_runtime_seconds,1.8",
                        "bun_1_1_5,runtime,matmul_runtime_seconds,4.5",
                        "node_18_20_3,runtime,matmul_runtime_seconds,3.1",
                        "deno_1_39_1,runtime,matmul_runtime_seconds,3.1",
                        "bun_fixed_canary,runtime,matmul_runtime_seconds,1.32",
                    ]
                ),
                encoding="utf-8",
            )

            trace = ChangeTraceEngine(load_csv(fixture)).format_trace()

        self.assertIn("release_resolution_metadata", trace)
        self.assertIn("versions:", trace)
        self.assertIn("runtime_engine_attribution_gate", trace)
        self.assertIn("profiles, bisection, or upstream fix notes", trace)


if __name__ == "__main__":
    unittest.main()
