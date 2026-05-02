"""
change_trace_engine.py - deterministic change-point traces for performance data.

The engine does not decide root cause. It turns normalized performance data
into signal blocks and a trace that an engineer or AI agent can reason over.

Input CSV columns:
    timestamp, service, metric, value

Example:
    python change_trace_engine.py examples/perf_trace.csv
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, TextIO


LATENCY_TERMS = ("latency", "p50", "p90", "p95", "p99", "duration", "delay")
ERROR_TERMS = ("error", "errors", "error_rate", "fail", "failure", "5xx", "timeout", "crash", "oom")
RESOURCE_TERMS = ("cpu", "memory", "connection", "sessions", "lag", "queue", "rows", "restart")
THROUGHPUT_TERMS = ("throughput", "tps", "rps", "requests_per_second")
LOAD_TERMS = ("vu", "vus", "virtual_user", "virtual_users", "users", "load")
EVENT_RATE_TERMS = ("error", "errors", "error_rate", "fail", "failure", "5xx", "timeout", "crash", "oom", "retry", "restart")
MECHANISM_TERMS = (
    "envoy",
    "ena",
    "transmit_queue",
    "transmit_queues",
    "hypervisor",
    "pod",
    "prestop",
    "termination",
    "cpu_throttl",
    "partitioner",
    "webkit",
    "javascriptcore",
    "jsc",
    "runtime",
    "regex",
    "backtracking",
    "futex",
    "mutex",
)


@dataclass(frozen=True)
class TimeSeriesPoint:
    timestamp: str
    service: str
    metric: str
    value: float
    order: int


@dataclass(frozen=True)
class SignalBlock:
    family: str
    service: str
    metric: str
    timestamp: str
    index: int
    confidence: float
    evidence: str
    before: float | None = None
    after: float | None = None
    related_service: str | None = None
    related_metric: str | None = None
    related_timestamp: str | None = None
    metadata: dict[str, str] | None = None

    def short_name(self) -> str:
        return f"{self.service}.{self.metric}"


@dataclass(frozen=True)
class DetectorRoute:
    data_shape: str
    selected_detectors: tuple[str, ...]
    evidence: str


def load_csv(path: str | Path) -> list[TimeSeriesPoint]:
    """Load normalized performance rows from CSV."""
    raw_rows: list[tuple[str, str, str, float]] = []
    with Path(path).open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"timestamp", "service", "metric", "value"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"CSV missing required columns: {', '.join(sorted(missing))}")
        for row in reader:
            raw_rows.append(
                (
                    str(row["timestamp"]).strip(),
                    str(row["service"]).strip(),
                    str(row["metric"]).strip(),
                    float(row["value"]),
                )
            )

    # Use timestamp rank, not file position, so CSVs grouped by service still
    # produce correct cross-service timing relationships.
    timestamp_rank = {
        ts: i for i, ts in enumerate(sorted({r[0] for r in raw_rows}))
    }
    rows = [
        TimeSeriesPoint(
            timestamp=timestamp,
            service=service,
            metric=metric,
            value=value,
            order=timestamp_rank[timestamp],
        )
        for timestamp, service, metric, value in raw_rows
    ]
    return rows


def normalize_export(path: str | Path, source: str = "auto") -> list[dict[str, str]]:
    """Normalize common monitoring exports into timestamp, service, metric, value rows.

    Supported inputs:
      - Already-normalized long CSV: timestamp, service, metric, value
      - Datadog-style long CSV: timestamp/time/date, service, metric/query, value
      - Datadog-style wide CSV: timestamp/time/date plus one metric column per query
    """
    if source not in {"auto", "datadog"}:
        raise ValueError(f"Unsupported source: {source}")

    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = [name.strip() for name in (reader.fieldnames or []) if name]
        rows = list(reader)

    if not fieldnames:
        raise ValueError("CSV has no header row")

    lower_to_name = {name.lower().strip(): name for name in fieldnames}
    timestamp_col = _first_column(lower_to_name, ("timestamp", "time", "date", "datetime"))
    if timestamp_col is None:
        raise ValueError("Could not find timestamp/time/date column")

    service_col = _first_column(lower_to_name, ("service", "service_name", "name"))
    metric_col = _first_column(lower_to_name, ("metric", "query", "series", "scope"))
    value_col = _first_column(lower_to_name, ("value", "avg", "count", "sum", "min", "max"))

    normalized: list[dict[str, str]] = []
    if service_col and metric_col and value_col:
        for raw in rows:
            value = _parse_number(raw.get(value_col, ""))
            if value is None:
                continue
            metric_name = _clean_metric_name(raw.get(metric_col, "metric"))
            service_name = _clean_service_name(raw.get(service_col, "")) or _extract_service(raw.get(metric_col, ""))
            normalized.append(
                {
                    "timestamp": str(raw.get(timestamp_col, "")).strip(),
                    "service": service_name or "unknown",
                    "metric": metric_name,
                    "value": _format_number(value),
                }
            )
        return normalized

    value_columns = [name for name in fieldnames if name != timestamp_col]
    for raw in rows:
        timestamp = str(raw.get(timestamp_col, "")).strip()
        for column in value_columns:
            value = _parse_number(raw.get(column, ""))
            if value is None:
                continue
            normalized.append(
                {
                    "timestamp": timestamp,
                    "service": _extract_service(column) or "unknown",
                    "metric": _clean_metric_name(column),
                    "value": _format_number(value),
                }
            )
    return normalized


def write_normalized_csv(rows: list[dict[str, str]], output: TextIO = sys.stdout) -> None:
    writer = csv.DictWriter(output, fieldnames=["timestamp", "service", "metric", "value"])
    writer.writeheader()
    writer.writerows(rows)


def _first_column(lower_to_name: dict[str, str], candidates: tuple[str, ...]) -> str | None:
    for candidate in candidates:
        if candidate in lower_to_name:
            return lower_to_name[candidate]
    return None


def _parse_number(value: str | None) -> float | None:
    if value is None:
        return None
    cleaned = str(value).strip().replace(",", "")
    if cleaned == "":
        return None
    try:
        parsed = float(cleaned)
    except ValueError:
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def _format_number(value: float) -> str:
    return str(int(value)) if value.is_integer() else f"{value:.12g}"


def _extract_service(text: str | None) -> str:
    if not text:
        return ""
    patterns = (
        r"(?:service|service_name)[:=]([A-Za-z0-9_.-]+)",
        r"\{[^}]*service:([A-Za-z0-9_.-]+)",
        r"\{[^}]*service=([A-Za-z0-9_.-]+)",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return _clean_service_name(match.group(1))
    if "." in text:
        prefix = text.split(".", 1)[0]
        if prefix and not prefix.lower().startswith(("avg:", "sum:", "max:", "min:", "count:")):
            return _clean_service_name(prefix)
    return ""


def _clean_service_name(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value).strip()).strip("_").lower()


def _clean_metric_name(value: str | None) -> str:
    if not value:
        return "metric"
    text = str(value).strip()
    text = re.sub(r"^(avg|sum|max|min|count):", "", text)
    text = re.sub(r"\{.*?\}", "", text)
    text = text.replace(" ", "_")
    text = re.sub(r"[^A-Za-z0-9_.-]+", "_", text)
    text = text.strip("._")
    if "." in text:
        maybe_service, maybe_metric = text.split(".", 1)
        if maybe_service and maybe_metric and not maybe_service.lower() in {"system", "trace", "runtime"}:
            text = maybe_metric
    return text.lower() or "metric"


def _median(values: list[float]) -> float:
    return statistics.median(values) if values else 0.0


def _mad(values: list[float]) -> float:
    if not values:
        return 0.0
    med = _median(values)
    return statistics.median([abs(v - med) for v in values])


def _slope(values: list[float]) -> float:
    """Least-squares slope over evenly spaced points."""
    n = len(values)
    if n < 2:
        return 0.0
    mean_x = (n - 1) / 2
    mean_y = sum(values) / n
    denom = sum((i - mean_x) ** 2 for i in range(n))
    if denom == 0:
        return 0.0
    return sum((i - mean_x) * (y - mean_y) for i, y in enumerate(values)) / denom


def _confidence_from_score(score: float, floor: float = 3.0, ceiling: float = 10.0) -> float:
    bounded = max(floor, min(score, ceiling))
    return round(0.55 + ((bounded - floor) / (ceiling - floor)) * 0.4, 2)


def _metric_contains(metric: str, terms: tuple[str, ...]) -> bool:
    m = metric.lower()
    return any(term in m for term in terms)


def group_series(points: Iterable[TimeSeriesPoint]) -> dict[tuple[str, str], list[TimeSeriesPoint]]:
    grouped: dict[tuple[str, str], list[TimeSeriesPoint]] = {}
    for p in points:
        grouped.setdefault((p.service, p.metric), []).append(p)
    for series in grouped.values():
        series.sort(key=lambda p: p.order)
    return grouped


def classify_detector_route(points: list[TimeSeriesPoint]) -> DetectorRoute:
    """Pick the detector family from the input shape before running detectors."""
    if not points:
        return DetectorRoute(
            data_shape="empty",
            selected_detectors=(),
            evidence="no rows were provided",
        )

    percentile_like = sum(1 for p in points if _parse_percentile_label(p.timestamp) is not None)
    metric_text = " ".join(p.metric.lower() for p in points)
    event_like = sum(1 for p in points if _metric_contains(p.metric, EVENT_RATE_TERMS))
    load_like = any(_metric_contains(p.metric, LOAD_TERMS) for p in points)
    throughput_like = any(_metric_contains(p.metric, THROUGHPUT_TERMS) for p in points)
    ratio_like = sum(1 for p in points if _is_ratio_metric(p.metric))
    concurrency_like = sum(1 for p in points if _parse_concurrency_label(p.timestamp) is not None)
    load_parameter_like = sum(1 for p in points if _parse_load_parameter_label(p.timestamp) is not None)
    unique_timestamps = {p.timestamp for p in points}
    time_label_like = sum(1 for label in unique_timestamps if _looks_like_time_label(label))

    if ratio_like >= max(3, len(points) * 0.2):
        return DetectorRoute(
            data_shape="benchmark_regression_table",
            selected_detectors=("cross_sectional_regression_outlier",),
            evidence=(
                f"{ratio_like}/{len(points)} rows are ratio metrics; "
                "treat rows as benchmark cases, not incident time"
            ),
        )

    if concurrency_like >= max(3, len(points) * 0.5):
        return DetectorRoute(
            data_shape="load_scaling_curve",
            selected_detectors=(
                "load_scaling_saturation",
                "tail_amplification_under_load",
                "mean_median_divergence",
            ),
            evidence=(
                f"{concurrency_like}/{len(points)} rows use concurrency labels; "
                "treat rows as load-scaling points"
            ),
        )

    if load_parameter_like >= max(3, len(points) * 0.5):
        return DetectorRoute(
            data_shape="load_parameter_sweep",
            selected_detectors=(
                "load_scaling_saturation",
                "tail_amplification_under_load",
                "mean_median_divergence",
            ),
            evidence=(
                f"{load_parameter_like}/{len(points)} rows use load-parameter labels; "
                "treat rows as parameter sweep points"
            ),
        )

    if percentile_like >= max(4, len(points) * 0.5):
        return DetectorRoute(
            data_shape="benchmark_distribution",
            selected_detectors=("distribution_tail_shift",),
            evidence=(
                f"{percentile_like}/{len(points)} rows use percentile labels; "
                "treat rows as distribution buckets, not incident time"
            ),
        )

    if "percentile" in metric_text and percentile_like >= 3:
        return DetectorRoute(
            data_shape="benchmark_distribution",
            selected_detectors=("distribution_tail_shift",),
            evidence="metric names and row labels indicate percentile distribution data",
        )

    if event_like >= max(3, len(points) * 0.85):
        return DetectorRoute(
            data_shape="event_rate_timeseries",
            selected_detectors=("event_rate_shift", "downstream_lag"),
            evidence=(
                f"{event_like}/{len(points)} rows use error/resource event metrics; "
                "route to event-rate shifts before generic mean shifts"
            ),
        )

    if 2 <= len(unique_timestamps) <= 20 and len(points) <= 120 and time_label_like < len(unique_timestamps) * 0.5:
        return DetectorRoute(
            data_shape="benchmark_condition_table",
            selected_detectors=("condition_delta",),
            evidence=(
                f"{len(unique_timestamps)} condition labels across {len(points)} rows; "
                "treat rows as benchmark conditions, not continuous incident time"
            ),
        )

    detectors = ["mean_shift", "event_rate_shift", "variance_shift", "trend_shift", "downstream_lag"]
    if load_like and throughput_like:
        detectors.insert(3, "throughput_plateau")

    return DetectorRoute(
        data_shape="timestamped_service_timeseries",
        selected_detectors=tuple(detectors),
        evidence="rows look like service metrics over ordered timestamps",
    )


def _parse_percentile_label(label: str) -> float | None:
    text = str(label).strip().lower()
    match = re.fullmatch(r"[qp](\d+(?:\.\d+)?)", text)
    if match:
        return float(match.group(1))
    match = re.search(r"(?:p|percentile[_-]?)(\d+(?:\.\d+)?)", text)
    if match:
        return float(match.group(1))
    return None


def _is_ratio_metric(metric: str) -> bool:
    text = metric.lower()
    return bool(re.search(r"(^|_)ratio($|_)|ratio[_-]|[_-]ratio", text))


def _parse_concurrency_label(label: str) -> float | None:
    text = str(label).strip().lower()
    match = re.fullmatch(r"(?:concurrency|conc|c)[_-]?(\d+(?:\.\d+)?)", text)
    if match:
        return float(match.group(1))
    return None


def _parse_load_parameter_label(label: str) -> float | None:
    text = str(label).strip().lower()
    match = re.fullmatch(
        r"(?:concurrency|conc|c|max_num_seqs|max[_-]?seqs|batch|batch_size|bs|vus?|users?)[_-]?(\d+(?:\.\d+)?)",
        text,
    )
    if match:
        return float(match.group(1))
    return None


def _looks_like_time_label(label: str) -> bool:
    text = str(label).strip()
    if re.search(r"\d{1,2}:\d{2}(?::\d{2})?", text):
        return True
    if re.search(r"\d{4}-\d{2}-\d{2}", text):
        return True
    if re.fullmatch(r"\d+(?:\.\d+)?", text):
        return True
    return False


def detect_mean_shift(series: list[TimeSeriesPoint], min_window: int = 3) -> SignalBlock | None:
    """Find the strongest sustained median shift in one series."""
    if len(series) < min_window * 2:
        return None

    values = [p.value for p in series]
    candidates: list[tuple[float, int, float, float, float]] = []
    for split in range(min_window, len(values) - min_window + 1):
        before_values = values[split - min_window:split]
        after_values = values[split:split + min_window]
        before = _median(before_values)
        after = _median(after_values)
        noise = max(_mad(before_values), _mad(after_values), abs(before) * 0.03, 1e-9)
        score = abs(after - before) / noise
        candidates.append((score, split, before, after, noise))

    if not candidates:
        return None

    max_score = max(c[0] for c in candidates)
    # Prefer the earliest split within 90% of the best score. For operational
    # traces, earlier change timing is more useful than a slightly stronger
    # confirmation window one sample later.
    best = next(c for c in candidates if c[0] >= max_score * 0.90)
    score, split, before, after, noise = best
    min_relative_delta = 0.15
    relative_delta = abs(after - before) / max(abs(before), 1e-9)
    if score < 3.0 or relative_delta < min_relative_delta:
        return None

    change_index = split
    for i in range(split, min(split + min_window, len(series))):
        sample_delta = abs(series[i].value - before)
        sample_relative_delta = sample_delta / max(abs(before), 1e-9)
        if sample_delta / max(noise, 1e-9) >= 3.0 and sample_relative_delta >= min_relative_delta:
            change_index = i
            break

    p = series[change_index]
    return SignalBlock(
        family="mean_shift",
        service=p.service,
        metric=p.metric,
        timestamp=p.timestamp,
        index=p.order,
        before=round(before, 4),
        after=round(after, 4),
        confidence=_confidence_from_score(score),
        evidence=(
            f"rolling median shifted from {before:.4g} to {after:.4g}; "
            f"score={score:.2f} using MAD-normalized delta"
        ),
    )


def detect_variance_shift(series: list[TimeSeriesPoint], min_window: int = 4) -> SignalBlock | None:
    """Find a strong instability change in one series."""
    if len(series) < min_window * 2:
        return None

    values = [p.value for p in series]
    best: tuple[float, int, float, float] | None = None
    for split in range(min_window, len(values) - min_window + 1):
        before_values = values[split - min_window:split]
        after_values = values[split:split + min_window]
        before_sd = statistics.pstdev(before_values)
        after_sd = statistics.pstdev(after_values)
        low = max(min(before_sd, after_sd), max(abs(_median(before_values)), 1.0) * 0.01)
        high = max(before_sd, after_sd)
        ratio = high / max(low, 1e-9)
        if best is None or ratio > best[0]:
            best = (ratio, split, before_sd, after_sd)

    if best is None:
        return None
    ratio, split, before_sd, after_sd = best
    if ratio < 3.0:
        return None

    p = series[split]
    return SignalBlock(
        family="variance_shift",
        service=p.service,
        metric=p.metric,
        timestamp=p.timestamp,
        index=p.order,
        before=round(before_sd, 4),
        after=round(after_sd, 4),
        confidence=_confidence_from_score(ratio),
        evidence=f"rolling standard deviation changed from {before_sd:.4g} to {after_sd:.4g}; ratio={ratio:.2f}",
    )


def detect_trend_shift(series: list[TimeSeriesPoint], min_window: int = 4) -> SignalBlock | None:
    """Find a trend acceleration/deceleration."""
    if len(series) < min_window * 2:
        return None

    values = [p.value for p in series]
    split = len(values) // 2
    before_values = values[:split]
    after_values = values[split:]
    before_slope = _slope(before_values)
    after_slope = _slope(after_values)
    delta = after_slope - before_slope
    scale = max(abs(_median(values)), 1.0)
    normalized = abs(delta) / scale
    if normalized < 0.04:
        return None

    p = series[split]
    score = normalized * 100
    return SignalBlock(
        family="trend_shift",
        service=p.service,
        metric=p.metric,
        timestamp=p.timestamp,
        index=p.order,
        before=round(before_slope, 4),
        after=round(after_slope, 4),
        confidence=_confidence_from_score(score, floor=4.0, ceiling=20.0),
        evidence=f"slope changed from {before_slope:.4g} to {after_slope:.4g}",
    )


def detect_event_rate_shift(series: list[TimeSeriesPoint]) -> SignalBlock | None:
    """Detect count/rate event surges without labeling them as generic mean shifts."""
    if not _metric_contains(series[0].metric, EVENT_RATE_TERMS):
        return None
    block = detect_mean_shift(series)
    if block is None:
        return None
    return SignalBlock(
        family="event_rate_shift",
        service=block.service,
        metric=block.metric,
        timestamp=block.timestamp,
        index=block.index,
        confidence=block.confidence,
        evidence=block.evidence.replace("rolling median shifted", "event-rate median shifted"),
        before=block.before,
        after=block.after,
    )


def detect_distribution_tail_shifts(grouped: dict[tuple[str, str], list[TimeSeriesPoint]]) -> list[SignalBlock]:
    """Detect percentile-tail divergence in benchmark distribution comparisons."""
    blocks: list[SignalBlock] = []
    for (_service, _metric), series in grouped.items():
        ranked = [
            (percentile, point)
            for point in series
            if (percentile := _parse_percentile_label(point.timestamp)) is not None
        ]
        if len(ranked) < 5:
            continue
        ranked.sort(key=lambda item: item[0])

        lower = [(p, point) for p, point in ranked if p <= 75]
        tail = [(p, point) for p, point in ranked if p >= 90]
        if len(lower) < 3 or len(tail) < 2:
            continue

        lower_values = [point.value for _p, point in lower]
        tail_values = [point.value for _p, point in tail]
        lower_median = _median(lower_values)
        tail_median = _median(tail_values)
        lower_noise = max(_mad(lower_values), abs(lower_median) * 0.10, 1.0)
        delta = tail_median - lower_median
        score = abs(delta) / lower_noise

        if score < 3.0:
            continue

        direction = "higher" if delta > 0 else "lower"
        first_tail = next(
            (
                point
                for _p, point in tail
                if abs(point.value - lower_median) / lower_noise >= 3.0
            ),
            tail[0][1],
        )
        strongest = max(tail, key=lambda item: abs(item[1].value - lower_median))[1]
        blocks.append(
            SignalBlock(
                family="distribution_tail_shift",
                service=first_tail.service,
                metric=first_tail.metric,
                timestamp=first_tail.timestamp,
                index=first_tail.order,
                before=round(lower_median, 4),
                after=round(tail_median, 4),
                confidence=_confidence_from_score(score),
                related_timestamp=strongest.timestamp,
                related_metric=strongest.metric,
                evidence=(
                    f"lower percentiles median={lower_median:.4g}; tail median={tail_median:.4g}; "
                    f"tail is {direction} by {delta:.4g}; strongest tail bucket={strongest.timestamp} "
                    f"value={strongest.value:.4g}"
                ),
            )
        )
    return blocks


def detect_cross_sectional_regression_outliers(grouped: dict[tuple[str, str], list[TimeSeriesPoint]]) -> list[SignalBlock]:
    """Detect benchmark rows where new/old ratios show broad regression."""
    blocks: list[SignalBlock] = []
    for (_service, metric), series in grouped.items():
        if not _is_ratio_metric(metric):
            continue
        values = [p.value for p in series]
        if len(values) < 4:
            continue
        regressions = [p for p in series if p.value < 0.8]
        severe = [p for p in series if p.value < 0.5]
        if len(regressions) < max(2, len(series) * 0.25):
            continue
        worst = min(series, key=lambda p: p.value)
        med = _median(values)
        blocks.append(
            SignalBlock(
                family="cross_sectional_regression_outlier",
                service=worst.service,
                metric=worst.metric,
                timestamp=worst.timestamp,
                index=worst.order,
                before=1.0,
                after=round(worst.value, 4),
                confidence=_confidence_from_score((1 - worst.value) * 10, floor=2.0, ceiling=8.0),
                evidence=(
                    f"{len(regressions)}/{len(series)} benchmark cases are below 0.80; "
                    f"{len(severe)} are below 0.50; median ratio={med:.4g}; "
                    f"worst case={worst.timestamp} value={worst.value:.4g}"
                ),
            )
        )
    return blocks


def detect_load_scaling_saturation(grouped: dict[tuple[str, str], list[TimeSeriesPoint]]) -> list[SignalBlock]:
    """Detect rising concurrency with flat throughput and rising latency."""
    blocks: list[SignalBlock] = []
    by_service: dict[str, dict[str, list[TimeSeriesPoint]]] = {}
    for (service, metric), series in grouped.items():
        by_service.setdefault(service, {})[metric] = sorted(series, key=lambda p: p.order)

    for service, metrics in by_service.items():
        throughput_items = [
            (metric, series)
            for metric, series in metrics.items()
            if _metric_contains(metric, THROUGHPUT_TERMS) or metric.lower().endswith("tok_s")
        ]
        latency_items = [
            (metric, series)
            for metric, series in metrics.items()
            if _metric_contains(metric, LATENCY_TERMS) or any(term in metric.lower() for term in ("ttft", "tpot", "itl"))
        ]
        if not latency_items:
            continue

        conc_points = [_parse_load_parameter_label(p.timestamp) for series in metrics.values() for p in series]
        conc_values = sorted({c for c in conc_points if c is not None})
        if len(conc_values) < 3:
            continue
        load_gain = conc_values[-1] / max(conc_values[0], 1e-9)
        scaling_table = _format_load_scaling_table(metrics, conc_values)

        plateau_evidence = ""
        if throughput_items:
            metric, series = max(throughput_items, key=lambda item: len(item[1]))
            sorted_series = sorted(series, key=lambda p: _parse_load_parameter_label(p.timestamp) or 0)
            first = sorted_series[0].value
            peak = max(p.value for p in sorted_series)
            last = sorted_series[-1].value
            plateau_evidence = (
                f"throughput metric {metric}: first={first:.4g}, peak={peak:.4g}, last={last:.4g}; "
            )
            peak_point = max(sorted_series, key=lambda p: p.value)
            low_point = min(sorted_series, key=lambda p: p.value)
            sweep_ratio = peak_point.value / max(low_point.value, 1e-9)
            if sweep_ratio >= 1.5 and peak_point.timestamp != low_point.timestamp:
                blocks.append(
                    SignalBlock(
                        family="parameter_sweep_cliff",
                        service=service,
                        metric=metric,
                        timestamp=low_point.timestamp,
                        index=low_point.order,
                        before=round(peak_point.value, 4),
                        after=round(low_point.value, 4),
                        confidence=_confidence_from_score(sweep_ratio, floor=1.5, ceiling=4.0),
                        evidence=(
                            f"{metric} varies {sweep_ratio:.1f}x across the sweep; "
                            f"best condition={peak_point.timestamp} value={peak_point.value:.4g}; "
                            f"worst condition={low_point.timestamp} value={low_point.value:.4g}; "
                            "this is a parameter-sensitive performance cliff, not incident time"
                        ),
                        metadata={"table": scaling_table} if scaling_table else None,
                    )
                )

        for metric, series in latency_items:
            sorted_series = sorted(series, key=lambda p: _parse_load_parameter_label(p.timestamp) or 0)
            if len(sorted_series) < 3:
                continue
            first = sorted_series[0]
            last = sorted_series[-1]
            ratio = last.value / max(first.value, 1e-9)
            if ratio < 3.0:
                continue
            is_batch_sweep = all(str(p.timestamp).lower().startswith("batch_") for p in sorted_series)
            if is_batch_sweep:
                blocks.append(
                    SignalBlock(
                        family="batch_work_scaling",
                        service=service,
                        metric=metric,
                        timestamp=last.timestamp,
                        index=last.order,
                        before=round(first.value, 4),
                        after=round(last.value, 4),
                        confidence=_confidence_from_score(ratio, floor=3.0, ceiling=80.0),
                        evidence=(
                            f"batch parameter increased {load_gain:.1f}x while {metric} increased {ratio:.1f}x; "
                            f"{plateau_evidence}treat as per-request work/payload scaling before calling it queue saturation"
                        ),
                        metadata={"table": scaling_table} if scaling_table else None,
                    )
                )
                continue
            blocks.append(
                SignalBlock(
                    family="load_scaling_saturation",
                    service=service,
                    metric=metric,
                    timestamp=last.timestamp,
                    index=last.order,
                    before=round(first.value, 4),
                    after=round(last.value, 4),
                    confidence=_confidence_from_score(ratio, floor=3.0, ceiling=15.0),
                    evidence=(
                        f"concurrency increased {load_gain:.1f}x while {metric} increased "
                        f"{ratio:.1f}x ({first.value:.4g} -> {last.value:.4g}); "
                        f"{plateau_evidence}this suggests saturation/queueing under load"
                    ),
                    metadata={"table": scaling_table} if scaling_table else None,
                )
            )
            if metric.startswith("p99_"):
                mean_metric = metric.replace("p99_", "mean_", 1)
                mean_series = metrics.get(mean_metric)
                if mean_series:
                    mean_sorted = sorted(mean_series, key=lambda p: _parse_load_parameter_label(p.timestamp) or 0)
                    mean_ratio = mean_sorted[-1].value / max(mean_sorted[0].value, 1e-9)
                    tail_ratio = ratio
                    if tail_ratio >= mean_ratio * 1.3 and tail_ratio >= 5:
                        blocks.append(
                            SignalBlock(
                                family="tail_amplification_under_load",
                                service=service,
                                metric=metric,
                                timestamp=last.timestamp,
                                index=last.order,
                                before=round(first.value, 4),
                                after=round(last.value, 4),
                                confidence=_confidence_from_score(tail_ratio / max(mean_ratio, 1e-9), floor=1.3, ceiling=4.0),
                                evidence=(
                                    f"tail {metric} increased {tail_ratio:.1f}x while {mean_metric} "
                                    f"increased {mean_ratio:.1f}x; tail degradation grows faster than the mean"
                                ),
                            )
                        )

            if metric.startswith("mean_"):
                median_metric = metric.replace("mean_", "median_", 1)
                median_series = metrics.get(median_metric)
                if median_series:
                    median_sorted = sorted(median_series, key=lambda p: _parse_load_parameter_label(p.timestamp) or 0)
                    divergence_points: list[str] = []
                    for mean_point, median_point in zip(sorted_series, median_sorted):
                        mean_to_median = mean_point.value / max(median_point.value, 1e-9)
                        if mean_to_median >= 2.0:
                            divergence_points.append(
                                f"{mean_point.timestamp}: mean={mean_point.value:.4g}, "
                                f"median={median_point.value:.4g}, ratio={mean_to_median:.1f}x"
                            )
                    if divergence_points:
                        worst = max(
                            zip(sorted_series, median_sorted),
                            key=lambda pair: pair[0].value / max(pair[1].value, 1e-9),
                        )
                        worst_ratio = worst[0].value / max(worst[1].value, 1e-9)
                        blocks.append(
                            SignalBlock(
                                family="mean_median_divergence",
                                service=service,
                                metric=metric,
                                timestamp=worst[0].timestamp,
                                index=worst[0].order,
                                before=round(worst[1].value, 4),
                                after=round(worst[0].value, 4),
                                confidence=_confidence_from_score(worst_ratio, floor=2.0, ceiling=8.0),
                                evidence=(
                                    f"{metric} diverges from {median_metric}; "
                                    + "; ".join(divergence_points[:4])
                                    + "; this preserves a bursty-stall anomaly that a generic saturation summary can hide"
                                ),
                            )
                        )
        break
    return blocks


def detect_condition_deltas(grouped: dict[tuple[str, str], list[TimeSeriesPoint]]) -> list[SignalBlock]:
    """Detect sparse benchmark condition deltas without requiring rolling windows."""
    blocks: list[SignalBlock] = []
    for (_service, _metric), series in grouped.items():
        if len(series) < 2:
            continue
        values = [p.value for p in series]
        low = min(series, key=lambda p: p.value)
        high = max(series, key=lambda p: p.value)
        absolute_delta = high.value - low.value
        ratio = high.value / max(low.value, 1e-9) if low.value >= 0 else 0.0
        relative = abs(absolute_delta) / max(abs(low.value), abs(high.value), 1e-9)
        material_floor = 1.08 if _metric_contains(series[0].metric, THROUGHPUT_TERMS) else 1.2
        if ratio < material_floor and relative < 0.12:
            continue
        later_or_worse = high if high.order >= low.order else low
        blocks.append(
            SignalBlock(
                family="condition_delta",
                service=later_or_worse.service,
                metric=later_or_worse.metric,
                timestamp=later_or_worse.timestamp,
                index=later_or_worse.order,
                before=round(low.value, 4),
                after=round(high.value, 4),
                confidence=_confidence_from_score(max(ratio, relative * 10), floor=1.5, ceiling=8.0),
                evidence=(
                    f"{later_or_worse.metric} changes across benchmark conditions; "
                    f"min={low.value:.4g} at {low.timestamp}; max={high.value:.4g} at {high.timestamp}; "
                    f"ratio={ratio:.2f}x; compare conditions before explaining cause"
                ),
            )
        )
    return _compact_condition_blocks(blocks)


def detect_phase_deltas(grouped: dict[tuple[str, str], list[TimeSeriesPoint]]) -> list[SignalBlock]:
    """Detect sparse before/after deltas encoded in metric names."""
    by_service: dict[str, list[TimeSeriesPoint]] = {}
    for (_service, _metric), series in grouped.items():
        for point in series:
            by_service.setdefault(point.service, []).append(point)

    blocks: list[SignalBlock] = []
    for service, points in by_service.items():
        before = [p for p in points if re.search(r"(^|_)(before|pre|v1)($|_)", p.metric)]
        after = [p for p in points if re.search(r"(^|_)(after|post|regress|v2|fixed|resolution)($|_)", p.metric)]
        for before_point in before:
            candidates = [
                after_point for after_point in after
                if _metric_family_token(before_point.metric) == _metric_family_token(after_point.metric)
                or _metric_family_token(before_point.metric) in after_point.metric
                or _metric_family_token(after_point.metric) in before_point.metric
            ]
            if not candidates:
                continue
            after_point = max(candidates, key=lambda p: abs(p.value - before_point.value))
            high = max(before_point.value, after_point.value)
            low = min(before_point.value, after_point.value)
            ratio = high / max(low, 1e-9)
            if ratio < 1.2:
                continue
            blocks.append(
                SignalBlock(
                    family="phase_delta",
                    service=service,
                    metric=_metric_family_token(before_point.metric),
                    timestamp=after_point.timestamp,
                    index=after_point.order,
                    before=round(before_point.value, 4),
                    after=round(after_point.value, 4),
                    confidence=_confidence_from_score(ratio, floor=1.2, ceiling=8.0),
                    evidence=(
                        f"sparse phase labels compare {before_point.metric}={before_point.value:.4g} "
                        f"with {after_point.metric}={after_point.value:.4g}; ratio={ratio:.2f}x"
                    ),
                )
            )
            break
    return _compact_condition_blocks(blocks, limit=4)


def _metric_family_token(metric: str) -> str:
    text = metric.lower()
    text = re.sub(r"(^|_)(before|after|pre|post|regressed|regression|resolution|resolved|fixed|v1|v2)($|_)", "_", text)
    text = re.sub(r"pydantic|fastapi|mysql|node|vite|bun|go|ray|cloudflare|vllm", "", text)
    parts = [
        p for p in text.split("_")
        if p and p not in {"lower", "bound", "value", "ms", "s", "seconds", "percent", "count", "time"}
    ]
    return "_".join(parts[:3]) or "metric"


def detect_threshold_signals(grouped: dict[tuple[str, str], list[TimeSeriesPoint]]) -> list[SignalBlock]:
    """Surface single-row sparse signals like CPU saturation or low utilization."""
    blocks: list[SignalBlock] = []
    for (_service, _metric), series in grouped.items():
        for point in series:
            metric = point.metric.lower()
            family = ""
            evidence = ""
            confidence = 0.7
            if "utilization" in metric and "percent" in metric and point.value <= 25:
                family = "capacity_underuse"
                evidence = f"{point.metric} is {point.value:.4g}%, indicating low resource use despite active work"
                confidence = 0.78
            elif "cpu" in metric and "percent" in metric and point.value >= 90:
                family = "resource_saturation"
                evidence = f"{point.metric} is {point.value:.4g}%, indicating CPU saturation"
                confidence = 0.86
            elif ("traffic_lost" in metric or "lost_percent" in metric) and point.value >= 30:
                family = "impact_spike"
                evidence = f"{point.metric} is {point.value:.4g}%, indicating material user-visible impact"
                confidence = 0.82
            elif ("offline_duration" in metric or "duration_minutes" in metric) and point.value >= 10:
                family = "impact_window"
                evidence = f"{point.metric} is {point.value:.4g} minutes, indicating a sustained impact window"
                confidence = 0.72
            elif ("multiplier" in metric or metric.endswith("_x")) and point.value >= 1.5:
                family = "config_expansion"
                evidence = f"{point.metric} is {point.value:.4g}x, indicating a material expansion/change in generated configuration"
                confidence = 0.78
            elif (
                ("error" in metric or "failure" in metric or "5xx" in metric)
                and "time" not in metric
                and "hour" not in metric
                and point.value > 0
            ):
                family = "event_presence"
                evidence = f"{point.metric} is non-zero ({point.value:.4g}); preserve as event evidence"
                confidence = 0.68

            if not family:
                continue
            blocks.append(
                SignalBlock(
                    family=family,
                    service=point.service,
                    metric=point.metric,
                    timestamp=point.timestamp,
                    index=point.order,
                    confidence=confidence,
                    evidence=evidence,
                    after=round(point.value, 4),
                )
            )
    return sorted(blocks, key=lambda b: (-b.confidence, b.index))[:6]


def detect_named_pattern_signals(grouped: dict[tuple[str, str], list[TimeSeriesPoint]]) -> list[SignalBlock]:
    """Detect sparse engineering patterns encoded by metric/condition names."""
    blocks: list[SignalBlock] = []
    by_service: dict[str, list[TimeSeriesPoint]] = {}
    all_points: list[TimeSeriesPoint] = []
    for (_service, _metric), series in grouped.items():
        for point in series:
            all_points.append(point)
            by_service.setdefault(point.service, []).append(point)

    global_text = " ".join(f"{p.timestamp} {p.service} {p.metric}" for p in all_points).lower()
    if "cache" in global_text and "repeated" in global_text and ("random" in global_text or "unique" in global_text):
        point = max(
            all_points,
            key=lambda p: (
                p.value if any(term in f"{p.timestamp} {p.service} {p.metric}".lower() for term in ("random", "unique", "cache"))
                else 0
            ),
        )
        blocks.append(
            SignalBlock(
                family="cache_cardinality_shift",
                service=point.service,
                metric=point.metric,
                timestamp=point.timestamp,
                index=point.order,
                confidence=0.8,
                evidence=(
                    "cache workload contrasts repeated/hit-like inputs with random or unique inputs; "
                    "preserve cache-cardinality and miss/eviction pressure before naming root cause"
                ),
                after=round(point.value, 4),
                metadata={"mechanisms": "cache_cardinality, repeated_inputs, random_or_unique_inputs"},
            )
        )

    for service, points in by_service.items():
        text = " ".join(f"{p.timestamp} {p.metric}" for p in points).lower()
        mechanism_terms = _extract_mechanism_terms(text)
        release_metadata = _extract_release_metadata(points)

        if mechanism_terms:
            point = next(
                (
                    p for p in points
                    if any(term in f"{p.timestamp} {p.metric}".lower() for term in mechanism_terms)
                ),
                points[0],
            )
            blocks.append(
                SignalBlock(
                    family="mechanism_evidence",
                    service=service,
                    metric=point.metric,
                    timestamp=point.timestamp,
                    index=point.order,
                    confidence=0.72,
                    evidence=(
                        "named low-level mechanisms appear in the evidence; retain them as evidence labels "
                        "without promoting them to root cause unless backed by profiling, bisection, or owner notes"
                    ),
                    after=round(point.value, 4),
                    metadata={"mechanisms": ", ".join(mechanism_terms)},
                )
            )

        if release_metadata:
            point = next(
                (
                    p for p in points
                    if any(token in p.timestamp.lower() for token in ("fixed", "canary", "revert", "rollback", "after_pr"))
                ),
                points[-1],
            )
            blocks.append(
                SignalBlock(
                    family="release_resolution_metadata",
                    service=service,
                    metric=point.metric,
                    timestamp=point.timestamp,
                    index=point.order,
                    confidence=0.74,
                    evidence=(
                        "version/release/fix labels are present; preserve introduced, regressed, reverted, "
                        "fixed, or canary metadata alongside metric deltas"
                    ),
                    after=round(point.value, 4),
                    metadata=release_metadata,
                )
            )

        if _needs_runtime_attribution_gate(text):
            point = next((p for p in points if "fixed" in p.timestamp.lower() or "canary" in p.timestamp.lower()), points[-1])
            blocks.append(
                SignalBlock(
                    family="runtime_engine_attribution_gate",
                    service=service,
                    metric=point.metric,
                    timestamp=point.timestamp,
                    index=point.order,
                    confidence=0.75,
                    evidence=(
                        "runtime-engine or JS-engine context is present, but exact attribution requires profile, "
                        "bisection, or upstream fix notes; treat engine sync as resolution context until then"
                    ),
                    after=round(point.value, 4),
                    metadata={"gate": "profiles_or_bisection_required_before_exact_runtime_root_cause"},
                )
            )

        if "trial" in text and "utilization" in text and ("pending" in text or "terminated" in text):
            point = max(points, key=lambda p: p.value if "trial" in p.metric else 0)
            blocks.append(
                SignalBlock(
                    family="control_plane_accumulation",
                    service=service,
                    metric=point.metric,
                    timestamp=point.timestamp,
                    index=point.order,
                    confidence=0.8,
                    evidence=(
                        "trial-count and low-utilization evidence appear together; inspect scheduler/control-plane "
                        "work accumulating with completed or pending tasks"
                    ),
                    after=round(point.value, 4),
                )
            )

        if ("baseline" in text or "before" in text) and "regress" in text and ("fix" in text or "revert" in text):
            point = next((p for p in points if "fix" in p.timestamp or "revert" in p.timestamp), points[-1])
            blocks.append(
                SignalBlock(
                    family="fix_validation_window",
                    service=service,
                    metric=point.metric,
                    timestamp=point.timestamp,
                    index=point.order,
                    confidence=0.82,
                    evidence=(
                        "baseline/regressed/fixed or reverted conditions are present; compare the full "
                        "regression window before attributing cause"
                    ),
                    after=round(point.value, 4),
                )
            )

        if any(term in text for term in ("cpu_seconds", "futex", "pprof", "profile", "hotspot", "stack")):
            point = max(points, key=lambda p: p.value if any(term in p.metric.lower() for term in ("cpu", "futex")) else 0)
            blocks.append(
                SignalBlock(
                    family="profile_hotspot",
                    service=service,
                    metric=point.metric,
                    timestamp=point.timestamp,
                    index=point.order,
                    confidence=0.78,
                    evidence=(
                        "profile/hotspot counters appear with the regression evidence; inspect code-path "
                        "attribution instead of only metric deltas"
                    ),
                    after=round(point.value, 4),
                )
            )

        if re.search(r"v?\d+[_-]\d+", text) and ("fixed" in text or "canary" in text or "after_pr" in text):
            point = next((p for p in points if any(t in p.timestamp for t in ("fixed", "canary", "after_pr"))), points[-1])
            blocks.append(
                SignalBlock(
                    family="version_fix_lineage",
                    service=service,
                    metric=point.metric,
                    timestamp=point.timestamp,
                    index=point.order,
                    confidence=0.76,
                    evidence=(
                        "versioned regression and fixed/canary conditions are present; preserve fix lineage "
                        "alongside the timing delta"
                    ),
                    after=round(point.value, 4),
                )
            )

        if "db" in text or "database" in text or "query" in text:
            error_points = [p for p in points if "error" in p.metric.lower() or "5xx" in p.metric.lower()]
            if error_points:
                point = max(error_points, key=lambda p: p.value)
                blocks.append(
                    SignalBlock(
                        family="database_error_incident",
                        service=service,
                        metric=point.metric,
                        timestamp=point.timestamp,
                        index=point.order,
                        confidence=0.76,
                        evidence=(
                            "database/query labels appear with error-rate evidence; inspect deployment/query "
                            "saturation as a candidate incident structure"
                        ),
                        after=round(point.value, 4),
                    )
                )

        if text.count("after_") >= 2 or "post_resolution" in text:
            point = next((p for p in points if "post_resolution" in p.timestamp), points[-1])
            blocks.append(
                SignalBlock(
                    family="phased_remediation",
                    service=service,
                    metric=point.metric,
                    timestamp=point.timestamp,
                    index=point.order,
                    confidence=0.74,
                    evidence=(
                        "multiple after/post-remediation stages are present; preserve staged fixes and residual "
                        "bottlenecks instead of collapsing to one before/after delta"
                    ),
                    after=round(point.value, 4),
                )
            )

    return sorted(blocks, key=lambda b: (-b.confidence, b.index))[:8]


def _extract_mechanism_terms(text: str) -> list[str]:
    terms: list[str] = []
    for term in MECHANISM_TERMS:
        pattern = r"(^|[^a-z0-9])" + re.escape(term) + r"([^a-z0-9]|$)"
        if re.search(pattern, text) and term not in terms:
            terms.append(term)
    return terms[:8]


def _extract_release_metadata(points: list[TimeSeriesPoint]) -> dict[str, str]:
    buckets: dict[str, list[str]] = {
        "baseline": [],
        "regressed": [],
        "reverted": [],
        "fixed": [],
        "canary": [],
        "rollback": [],
    }
    version_labels: list[str] = []
    for point in points:
        label = point.timestamp.lower()
        is_clock_or_incident_time = any(token in label for token in ("utc", "hour", "minute", "second", "duration"))
        if not is_clock_or_incident_time and re.search(r"(?:^|_)(?:v\d+[_-]\d+|[a-z][a-z0-9]+_\d+[_-]\d+)", label):
            version_labels.append(point.timestamp)
        for key in buckets:
            if key in label:
                buckets[key].append(point.timestamp)
        if re.search(r"(^|_)after_pr($|_)", label):
            buckets["fixed"].append(point.timestamp)

    metadata = {key: ", ".join(dict.fromkeys(values)) for key, values in buckets.items() if values}
    if version_labels:
        metadata["versions"] = ", ".join(dict.fromkeys(version_labels[:8]))
    has_resolution = any(key in metadata for key in ("regressed", "reverted", "fixed", "canary", "rollback", "versions"))
    if not has_resolution:
        return {}
    return metadata


def _needs_runtime_attribution_gate(text: str) -> bool:
    runtime_context = any(term in text for term in ("bun", "node", "deno", "webkit", "javascriptcore", "jsc", "runtime"))
    fix_context = any(term in text for term in ("fixed", "canary", "after_pr", "sync", "upstream"))
    comparison_context = sum(1 for term in ("bun", "node", "deno") if term in text) >= 2
    return runtime_context and fix_context and comparison_context


def _format_load_scaling_table(metrics: dict[str, list[TimeSeriesPoint]], conc_values: list[float]) -> str:
    wanted = [
        "request_throughput_req_s",
        "output_token_throughput_tok_s",
        "mean_ttft_ms",
        "p99_ttft_ms",
        "mean_tpot_ms",
        "median_itl_ms",
        "p99_itl_ms",
    ]
    available = [metric for metric in wanted if metric in metrics]
    if not available:
        return ""
    lines = ["  concurrency | " + " | ".join(available)]
    lines.append("  " + " | ".join(["---"] * (len(available) + 1)))
    for conc in conc_values:
        row = [f"{conc:g}"]
        for metric in available:
            value = next(
                (p.value for p in metrics[metric] if _parse_load_parameter_label(p.timestamp) == conc),
                None,
            )
            row.append("" if value is None else f"{value:.4g}")
        lines.append("  " + " | ".join(row))
    return "\n".join(lines)


def detect_throughput_plateaus(grouped: dict[tuple[str, str], list[TimeSeriesPoint]]) -> list[SignalBlock]:
    """Detect throughput flattening while load rises for the same service."""
    blocks: list[SignalBlock] = []
    by_service: dict[str, dict[str, list[TimeSeriesPoint]]] = {}
    for (service, metric), series in grouped.items():
        by_service.setdefault(service, {})[metric] = series

    for service, metrics in by_service.items():
        load_series = [
            s for metric, s in metrics.items()
            if _metric_contains(metric, LOAD_TERMS)
        ]
        throughput_series = [
            (metric, s) for metric, s in metrics.items()
            if _metric_contains(metric, THROUGHPUT_TERMS)
        ]
        if not load_series or not throughput_series:
            continue
        load_values = [p.value for p in load_series[0]]
        if len(load_values) < 4 or load_values[-1] <= load_values[0] * 1.2:
            continue

        for metric, series in throughput_series:
            values = [p.value for p in series]
            if len(values) < 4:
                continue
            first_slope = _slope(values[:len(values) // 2])
            last_slope = _slope(values[len(values) // 2:])
            total_gain = values[-1] - values[0]
            load_gain = load_values[-1] - load_values[0]
            if total_gain <= 0:
                continue
            if abs(last_slope) <= max(abs(first_slope) * 0.25, 1e-9):
                p = series[len(series) // 2]
                blocks.append(
                    SignalBlock(
                        family="throughput_plateau",
                        service=service,
                        metric=metric,
                        timestamp=p.timestamp,
                        index=p.order,
                        before=round(first_slope, 4),
                        after=round(last_slope, 4),
                        confidence=0.82,
                        evidence=(
                            f"load rose by {load_gain:.4g} while throughput slope flattened "
                            f"from {first_slope:.4g} to {last_slope:.4g}"
                        ),
                    )
                )
    return blocks


def detect_downstream_lag(blocks: list[SignalBlock], max_lag_points: int = 8) -> list[SignalBlock]:
    """Surface timing relationships for LLM reasoning without deciding causality."""
    timing_blocks: list[SignalBlock] = []
    seen_pairs: set[tuple[str, str, str, str]] = set()
    candidates = [
        b for b in blocks
        if b.family in {"mean_shift", "variance_shift", "trend_shift", "throughput_plateau", "event_rate_shift"}
    ]
    ordered = sorted(candidates, key=lambda b: b.index)
    for i, first in enumerate(ordered):
        for later in ordered[i + 1:]:
            lag = later.index - first.index
            if lag <= 0 or lag > max_lag_points or first.service == later.service:
                continue
            later_is_symptom = (
                _metric_contains(later.metric, LATENCY_TERMS)
                or _metric_contains(later.metric, ERROR_TERMS)
                or _metric_contains(later.metric, RESOURCE_TERMS)
                or later.family == "throughput_plateau"
            )
            first_is_signal = (
                _metric_contains(first.metric, LATENCY_TERMS)
                or _metric_contains(first.metric, ERROR_TERMS)
                or _metric_contains(first.metric, RESOURCE_TERMS)
                or first.family == "throughput_plateau"
            )
            if not (first_is_signal and later_is_symptom):
                continue
            pair = (first.service, first.metric, later.service, later.metric)
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            timing_blocks.append(
                SignalBlock(
                    family="downstream_lag",
                    service=first.service,
                    metric=first.metric,
                    timestamp=first.timestamp,
                    index=first.index,
                    related_service=later.service,
                    related_metric=later.metric,
                    related_timestamp=later.timestamp,
                    confidence=0.78,
                    evidence=(
                        f"{first.short_name()} changed before {later.short_name()} "
                        f"by {lag} row(s); timing suggests a candidate cascade, not proof"
                    ),
                )
            )
            if len(timing_blocks) >= 8:
                return timing_blocks
    return timing_blocks


class ChangeTraceEngine:
    """0-parameter performance signal-to-trace engine."""

    def __init__(self, points: list[TimeSeriesPoint]):
        self.points = points
        self.grouped = group_series(points)
        self.route = classify_detector_route(points)

    def analyze(self) -> list[SignalBlock]:
        blocks: list[SignalBlock] = []
        if "condition_delta" in self.route.selected_detectors:
            blocks.extend(detect_condition_deltas(self.grouped))
            blocks.extend(detect_phase_deltas(self.grouped))
            blocks.extend(detect_threshold_signals(self.grouped))
            blocks.extend(detect_named_pattern_signals(self.grouped))
            return sorted(blocks, key=lambda b: (b.index, b.family, b.service, b.metric))

        if "cross_sectional_regression_outlier" in self.route.selected_detectors:
            blocks.extend(detect_cross_sectional_regression_outliers(self.grouped))
            return sorted(blocks, key=lambda b: (b.index, b.family, b.service, b.metric))

        if "load_scaling_saturation" in self.route.selected_detectors:
            blocks.extend(detect_load_scaling_saturation(self.grouped))
            return sorted(blocks, key=lambda b: (b.index, b.family, b.service, b.metric))

        if "distribution_tail_shift" in self.route.selected_detectors:
            blocks.extend(detect_distribution_tail_shifts(self.grouped))
            return sorted(blocks, key=lambda b: (b.index, b.family, b.service, b.metric))

        for (_service, metric), series in self.grouped.items():
            if _metric_contains(metric, LOAD_TERMS):
                continue
            if self.route.data_shape == "event_rate_timeseries":
                block = detect_event_rate_shift(series)
                if block is not None:
                    blocks.append(block)
                continue

            detectors = []
            if _metric_contains(metric, EVENT_RATE_TERMS):
                block = detect_event_rate_shift(series)
                if block is not None:
                    blocks.append(block)
                    continue
            if "mean_shift" in self.route.selected_detectors:
                detectors.append(detect_mean_shift)
            if "variance_shift" in self.route.selected_detectors:
                detectors.append(detect_variance_shift)
            if "trend_shift" in self.route.selected_detectors:
                detectors.append(detect_trend_shift)
            for detector in detectors:
                block = detector(series)
                if block is not None:
                    blocks.append(block)

        if "throughput_plateau" in self.route.selected_detectors:
            blocks.extend(detect_throughput_plateaus(self.grouped))
        blocks = _compact_signal_blocks(blocks)
        if "downstream_lag" in self.route.selected_detectors:
            blocks.extend(detect_downstream_lag(blocks))
        return sorted(blocks, key=lambda b: (b.index, b.family, b.service, b.metric))

    def format_trace(self, blocks: list[SignalBlock] | None = None) -> str:
        if blocks is None:
            blocks = self.analyze()

        lines: list[str] = []
        lines.append("--- CHANGE TRACE ---")
        lines.append("This trace surfaces evidence and candidate explanations. It does not decide root cause.")
        lines.append("")
        lines.append("DETECTOR ROUTE:")
        lines.append(f"  Data shape: {self.route.data_shape}")
        selected = ", ".join(self.route.selected_detectors) if self.route.selected_detectors else "none"
        lines.append(f"  Selected detectors: {selected}")
        lines.append(f"  Evidence: {self.route.evidence}")
        lines.append("")

        primary = [
            b for b in blocks
            if b.family in {
                "mean_shift",
                "variance_shift",
                "trend_shift",
                "throughput_plateau",
                "event_rate_shift",
                "distribution_tail_shift",
                "cross_sectional_regression_outlier",
                "load_scaling_saturation",
                "tail_amplification_under_load",
                "mean_median_divergence",
                "parameter_sweep_cliff",
                "condition_delta",
                "phase_delta",
                "capacity_underuse",
                "resource_saturation",
                "impact_spike",
                "impact_window",
                "event_presence",
                "config_expansion",
                "batch_work_scaling",
                "control_plane_accumulation",
                "fix_validation_window",
                "profile_hotspot",
                "version_fix_lineage",
                "release_resolution_metadata",
                "mechanism_evidence",
                "cache_cardinality_shift",
                "runtime_engine_attribution_gate",
                "database_error_incident",
                "phased_remediation",
            }
        ]
        primary_priority = {
            "cache_cardinality_shift": 0,
            "batch_work_scaling": 0,
            "fix_validation_window": 0,
            "release_resolution_metadata": 1,
            "profile_hotspot": 1,
            "control_plane_accumulation": 1,
            "database_error_incident": 1,
            "phased_remediation": 1,
            "runtime_engine_attribution_gate": 1,
            "resource_saturation": 1,
            "impact_spike": 1,
            "impact_window": 1,
            "mechanism_evidence": 2,
            "capacity_underuse": 2,
            "phase_delta": 2,
            "cross_sectional_regression_outlier": 2,
            "load_scaling_saturation": 3,
            "condition_delta": 4,
            "parameter_sweep_cliff": 4,
        }
        primary.sort(key=lambda b: (primary_priority.get(b.family, 5), b.index, b.service, b.metric))
        timing = [b for b in blocks if b.family == "downstream_lag"]

        lines.append("SIGNAL BLOCKS:")
        if not primary:
            lines.append("  No strong change blocks detected.")
        for i, block in enumerate(primary, 1):
            before_after = ""
            if block.before is not None and block.after is not None:
                before_after = f" ({block.before} -> {block.after})"
            lines.append(
                f"  [{i}] {block.family}: {block.short_name()} at {block.timestamp}"
                f"{before_after}, confidence={block.confidence}"
            )
            lines.append(f"      Evidence: {block.evidence}")
            if block.metadata:
                for key, value in block.metadata.items():
                    if key == "table":
                        continue
                    lines.append(f"      {key}: {value}")

        load_tables = [
            b.metadata["table"]
            for b in primary
            if b.metadata and b.metadata.get("table")
        ]
        if load_tables:
            lines.append("")
            lines.append("SCALING TABLE:")
            lines.append(load_tables[0])

        lines.append("")
        lines.append("CANDIDATE CASCADES:")
        if not timing:
            lines.append("  No cross-service timing cascade detected.")
        for block in timing:
            lines.append(
                f"  {block.short_name()} before "
                f"{block.related_service}.{block.related_metric} "
                f"({block.timestamp} -> {block.related_timestamp})"
            )
            lines.append(f"      Evidence: {block.evidence}")

        lines.append("")
        lines.append("OPTIONS FOR THE LLM TO WEIGH:")
        if primary:
            earliest = primary[0]
            if earliest.family == "distribution_tail_shift":
                lines.append(
                    f"  Option A: {earliest.short_name()} shows a tail-distribution shift "
                    f"starting at {earliest.timestamp}."
                )
            elif earliest.family == "cross_sectional_regression_outlier":
                lines.append(
                    f"  Option A: {earliest.short_name()} shows broad benchmark regression; "
                    f"inspect the worst case at {earliest.timestamp}."
                )
            elif earliest.family == "load_scaling_saturation":
                lines.append(
                    f"  Option A: {earliest.short_name()} grows sharply under load; "
                    "inspect saturation, queueing, and scheduling."
                )
            elif earliest.family == "tail_amplification_under_load":
                lines.append(
                    f"  Option A: {earliest.short_name()} tail grows faster than mean under load; "
                    "inspect bursty stalls and tail-specific bottlenecks."
                )
            elif earliest.family == "mean_median_divergence":
                lines.append(
                    f"  Option A: {earliest.short_name()} mean diverges from median; "
                    "inspect uneven latency distribution and intermittent stalls."
                )
            elif earliest.family == "parameter_sweep_cliff":
                lines.append(
                    f"  Option A: {earliest.short_name()} changes sharply across parameter settings; "
                    "inspect the best/worst condition boundary."
                )
            elif earliest.family == "condition_delta":
                lines.append(
                    f"  Option A: {earliest.short_name()} differs across benchmark conditions; "
                    "compare conditions before explaining cause."
                )
            elif earliest.family == "batch_work_scaling":
                lines.append(
                    f"  Option A: {earliest.short_name()} scales with batch/payload work; "
                    "check expected cost model before calling it saturation."
                )
            elif earliest.family == "fix_validation_window":
                lines.append(
                    f"  Option A: {earliest.short_name()} sits inside a baseline/regressed/fixed window; "
                    "preserve fix validation before explaining cause."
                )
            elif earliest.family == "cache_cardinality_shift":
                lines.append(
                    f"  Option A: {earliest.short_name()} shows a cache-cardinality workload shift; "
                    "compare repeated-hit and high-cardinality miss/eviction behavior."
                )
            elif earliest.family == "release_resolution_metadata":
                lines.append(
                    f"  Option A: {earliest.short_name()} has release/fix lineage; "
                    "preserve versions, revert, fixed, and canary labels before explaining cause."
                )
            elif earliest.family == "runtime_engine_attribution_gate":
                lines.append(
                    f"  Option A: {earliest.short_name()} has runtime-engine context; "
                    "require profile, bisection, or fix notes before exact attribution."
                )
            elif earliest.family == "event_rate_shift":
                lines.append(f"  Option A: {earliest.short_name()} is the first visible event-rate shift.")
            else:
                lines.append(f"  Option A: {earliest.short_name()} is the first visible shift.")
        if timing:
            lines.append("  Option B: later services are downstream symptoms of the first shift.")
        if any(b.family == "throughput_plateau" for b in primary):
            lines.append("  Option C: load saturation is present; inspect capacity and pools.")
        if any(b.family == "distribution_tail_shift" for b in primary):
            lines.append("  Option C: average latency may hide tail degradation; inspect p90/p95/p99 behavior.")
        if any(b.family == "cross_sectional_regression_outlier" for b in primary):
            lines.append("  Option C: this is a benchmark matrix; prioritize widespread regressions over one-off noise.")
        if any(b.family == "load_scaling_saturation" for b in primary):
            lines.append("  Option C: throughput may look stable while individual latency collapses under concurrency.")
        if any(b.family == "mean_median_divergence" for b in primary):
            lines.append("  Option C: preserve mean/median contradictions; they can point to bursty stalls.")
        if any(b.family == "tail_amplification_under_load" for b in primary):
            lines.append("  Option C: tail amplification can be the main user-visible failure even when averages look explainable.")
        if any(b.family == "parameter_sweep_cliff" for b in primary):
            lines.append("  Option C: parameter sensitivity is present; do not flatten the sweep into one average.")
        if any(b.family == "condition_delta" for b in primary):
            lines.append("  Option C: this is sparse benchmark evidence; preserve condition labels and deltas.")
        if any(b.family == "batch_work_scaling" for b in primary):
            lines.append("  Option C: batch-size sweeps may reflect more per-request work, not a queueing failure.")
        if any(b.family == "fix_validation_window" for b in primary):
            lines.append("  Option C: fix/revert validation can be stronger than a single regression point.")
        if any(b.family == "cache_cardinality_shift" for b in primary):
            lines.append("  Option C: repeated-input cache wins and unique-input degradation are different workloads.")
        if any(b.family == "mechanism_evidence" for b in primary):
            lines.append("  Option C: preserve named mechanisms as evidence labels, not automatic root cause.")
        if any(b.family == "release_resolution_metadata" for b in primary):
            lines.append("  Option C: release/fix metadata can be the strongest resolution evidence.")
        if any(b.family == "runtime_engine_attribution_gate" for b in primary):
            lines.append("  Option C: runtime-engine attribution needs profiles, bisection, or upstream fix notes.")
        lines.append("  Option D: detector output is incomplete; request more metrics if evidence is thin.")

        lines.append("")
        lines.append("GUARDRAIL:")
        lines.append("  Do not turn timing into causality without dependency, deploy, or resource evidence.")
        return "\n".join(lines)


def analyze_csv(path: str | Path) -> str:
    points = load_csv(path)
    return ChangeTraceEngine(points).format_trace()


def _compact_signal_blocks(blocks: list[SignalBlock]) -> list[SignalBlock]:
    """Keep the most useful detector block per metric for readable traces."""
    priority = {
        "mean_shift": 0,
        "throughput_plateau": 1,
        "variance_shift": 2,
        "trend_shift": 3,
    }
    best: dict[tuple[str, str], SignalBlock] = {}
    for block in blocks:
        key = (block.service, block.metric)
        current = best.get(key)
        if current is None:
            best[key] = block
            continue
        candidate_rank = (priority.get(block.family, 99), block.index, -block.confidence)
        current_rank = (priority.get(current.family, 99), current.index, -current.confidence)
        if candidate_rank < current_rank:
            best[key] = block
    return list(best.values())


def _compact_condition_blocks(blocks: list[SignalBlock], limit: int = 8) -> list[SignalBlock]:
    """Keep the largest sparse deltas so traces remain readable."""
    return sorted(
        blocks,
        key=lambda b: (
            abs((b.after or 0.0) - (b.before or 0.0)) / max(abs(b.before or 0.0), 1e-9),
            b.confidence,
        ),
        reverse=True,
    )[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description="Change-Point Engine")
    parser.add_argument("csv_path", help="CSV export or normalized CSV")
    parser.add_argument(
        "--normalize",
        action="store_true",
        help="Print normalized timestamp,service,metric,value CSV instead of running a trace",
    )
    parser.add_argument(
        "--source",
        choices=("auto", "datadog"),
        default="auto",
        help="Input export source for --normalize",
    )
    args = parser.parse_args()
    if args.normalize:
        write_normalized_csv(normalize_export(args.csv_path, source=args.source))
        return 0
    print(analyze_csv(args.csv_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
