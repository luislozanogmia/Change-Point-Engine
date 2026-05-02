#!/usr/bin/env python3
"""Build baseline and trace-on prompts for extracted benchmark cases."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from change_trace_engine import analyze_csv


BASELINE_TEMPLATE = """You are a fresh performance benchmark evaluator with zero prior context.

Analyze ONLY the public evidence below. Identify:
1. the performance issue,
2. the evidence,
3. the missing evidence,
4. the recommended next diagnostic step.

Do not invent root cause beyond the evidence.

CASE:
{summary}

RAW EVIDENCE:
{raw_evidence}

Return concise structured findings.
"""


TRACE_TEMPLATE = """You are a fresh performance benchmark evaluator with zero prior context.

Analyze ONLY the public evidence and precomputed deterministic trace below. Identify:
1. the performance issue,
2. the evidence,
3. the missing evidence,
4. the recommended next diagnostic step.

Use the trace as structured evidence. Do not treat it as root-cause proof.
Do not invent root cause beyond the evidence.

CASE:
{summary}

RAW EVIDENCE:
{raw_evidence}

PRECOMPUTED CHANGE TRACE:
{trace}

Return concise structured findings.
"""


def read_optional(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip() if path.exists() else ""


def parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = str(value).strip().replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def clean_token(value: str | None, fallback: str) -> str:
    text = str(value or "").strip()
    if not text:
        text = fallback
    out = []
    for ch in text.lower():
        out.append(ch if ch.isalnum() else "_")
    cleaned = "_".join(part for part in "".join(out).split("_") if part)
    return cleaned or fallback


def timestamp_for(row: dict[str, str], row_index: int) -> str:
    for key, prefix in (
        ("timestamp", ""),
        ("max_num_seqs", "max_num_seqs_"),
        ("batch_size", "batch_"),
        ("batch_or_clients", "load_"),
        ("gpu_count", "gpu_"),
        ("run_label", ""),
        ("variant", ""),
        ("commit_or_condition", ""),
        ("scenario", ""),
        ("stage", ""),
        ("context", ""),
        ("name", ""),
        ("metric_scope", ""),
    ):
        value = row.get(key)
        if value not in (None, ""):
            return clean_token(f"{prefix}{value}", f"row_{row_index}")
    return f"row_{row_index}"


def service_for(row: dict[str, str], case_id: str) -> str:
    parts = [case_id]
    for key in ("version", "chunked_prefill", "series", "source_context", "scenario"):
        value = row.get(key)
        if value not in (None, ""):
            parts.append(str(value))
    return clean_token("_".join(parts), case_id)


def metric_name(*parts: str | None) -> str:
    text = "_".join(str(part) for part in parts if part not in (None, ""))
    return clean_token(text, "metric")


def coerce_to_trace_csv(source: Path, target: Path, case_id: str) -> Path:
    with source.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    required = {"timestamp", "service", "metric", "value"}
    if required.issubset(set(fieldnames)):
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        return target

    id_columns = {
        "case_id",
        "source",
        "source_url",
        "notes",
        "value_text",
        "unit",
        "spread",
        "spread_ms",
    }
    context_columns = {
        "timestamp",
        "max_num_seqs",
        "batch_size",
        "batch_or_clients",
        "gpu_count",
        "run_label",
        "variant",
        "commit_or_condition",
        "scenario",
        "stage",
        "context",
        "name",
        "metric_scope",
        "version",
        "chunked_prefill",
        "series",
        "source_context",
    }
    output_rows: list[dict[str, str]] = []
    for i, row in enumerate(rows, 1):
        timestamp = timestamp_for(row, i)
        service = service_for(row, case_id)

        if "metric" in row and "value" in row and parse_float(row.get("value")) is not None:
            metric = metric_name(row.get("metric"), row.get("unit"))
            output_rows.append(
                {
                    "timestamp": timestamp,
                    "service": service,
                    "metric": metric,
                    "value": str(parse_float(row.get("value"))),
                }
            )
            continue

        if "measurement" in row:
            for value_column in ("value", "value_ms", "min_value_s", "max_value_s"):
                value = parse_float(row.get(value_column))
                if value is None:
                    continue
                metric = metric_name(row.get("measurement"), value_column, row.get("unit"))
                output_rows.append(
                    {
                        "timestamp": timestamp,
                        "service": service,
                        "metric": metric,
                        "value": str(value),
                    }
                )
            continue

        for key in fieldnames:
            if key in id_columns or key in context_columns:
                continue
            value = parse_float(row.get(key))
            if value is None:
                continue
            output_rows.append(
                {
                    "timestamp": timestamp,
                    "service": service,
                    "metric": metric_name(key),
                    "value": str(value),
                }
            )

    if not output_rows:
        raise ValueError(f"Could not coerce {source} into trace rows")

    with target.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "service", "metric", "value"])
        writer.writeheader()
        writer.writerows(output_rows)
    return target


def build_for_case(case_dir: Path, output_root: Path) -> None:
    case_id = case_dir.name
    raw = read_optional(case_dir / "raw_evidence.txt")
    summary = read_optional(case_dir / "source_summary.md")
    normalized = case_dir / "normalized.csv"
    if not raw or not summary or not normalized.exists():
        return

    trace_input = case_dir / "trace_input.csv"
    coerce_to_trace_csv(normalized, trace_input, case_id)
    trace = analyze_csv(trace_input)
    out = output_root / case_id
    out.mkdir(parents=True, exist_ok=True)
    (out / "trace.txt").write_text(trace + "\n", encoding="utf-8")
    (out / "baseline_prompt.txt").write_text(
        BASELINE_TEMPLATE.format(summary=summary, raw_evidence=raw).strip() + "\n",
        encoding="utf-8",
    )
    (out / "trace_on_prompt.txt").write_text(
        TRACE_TEMPLATE.format(summary=summary, raw_evidence=raw, trace=trace).strip() + "\n",
        encoding="utf-8",
    )
    for filename in ("baseline_output.txt", "trace_on_output.txt", "review.md"):
        target = out / filename
        if not target.exists():
            target.write_text("", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases-root", default="artifacts/overnight_25_case_benchmark/cases")
    parser.add_argument("--runs-root", default="artifacts/overnight_25_case_benchmark/runs")
    parser.add_argument("--case-list", default="")
    args = parser.parse_args()

    cases_root = Path(args.cases_root)
    output_root = Path(args.runs_root)
    allowed: set[str] | None = None
    if args.case_list:
        allowed = {
            line.strip()
            for line in Path(args.case_list).read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        }

    for case_dir in sorted(p for p in cases_root.iterdir() if p.is_dir()):
        if allowed is not None and case_dir.name not in allowed:
            continue
        build_for_case(case_dir, output_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
