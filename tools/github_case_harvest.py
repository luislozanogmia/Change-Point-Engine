#!/usr/bin/env python3
"""Harvest public GitHub issues that may work as change-trace benchmark cases."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path


API = "https://api.github.com"


QUERIES = [
    '"Serving Benchmark Result" is:issue is:closed',
    '"Performance regression" "benchmark" is:issue is:closed',
    '"throughput" "latency" "P99" is:issue is:closed',
    '"p95" "p99" "regression" is:issue is:closed',
    '"requests/sec" "latency" is:issue is:closed',
    '"ops/sec" "regression" is:issue is:closed',
    '"benchmark results" "fixed" is:issue is:closed',
    '"slow" "p99" "fixed" is:issue is:closed',
    '"TTFT" "ITL" is:issue is:closed',
    '"Mean TTFT" "P99 TTFT" is:issue is:closed',
    '"tail latency" "regression" is:issue is:closed',
]


RAW_PATTERNS = [
    r"\bp(?:50|75|90|95|99|99\.9)\b",
    r"\bq(?:50|75|90|95|99)\b",
    r"\bmean\b.*\bmedian\b",
    r"\bthroughput\b",
    r"\blatency\b",
    r"\brequests?/s(?:ec)?\b",
    r"\bops/s(?:ec)?\b",
    r"\btok/s\b",
    r"\bTTFT\b",
    r"\bITL\b",
    r"\bms\b",
    r"\bseconds?\b",
    r"\bbenchmark\b",
    r"\|[^\n]+\|[^\n]+\|",
    r"```[\s\S]{80,}?```",
]


RESOLUTION_PATTERNS = [
    r"\bfixed\b",
    r"\bresolved\b",
    r"\bclosed by\b",
    r"\bmerged\b",
    r"\bworkaround\b",
    r"\bnot planned\b",
    r"\bduplicate\b",
    r"\broot cause\b",
    r"\bcaused by\b",
    r"\bregression was introduced\b",
    r"\bthis is expected\b",
]


@dataclass
class Candidate:
    title: str
    html_url: str
    repo: str
    number: int
    state_reason: str | None
    raw_score: int
    resolution_score: int
    evidence_terms: list[str]
    resolution_terms: list[str]
    body_excerpt: str
    comments_excerpt: str


def request_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as response:
        remaining = response.headers.get("x-ratelimit-remaining")
        if remaining == "0":
            reset = int(response.headers.get("x-ratelimit-reset", "0"))
            sleep_for = max(1, reset - int(time.time()) + 1)
            time.sleep(sleep_for)
        return json.loads(response.read().decode("utf-8"))


def search_issues(query: str, pages: int, per_page: int) -> list[dict]:
    out: list[dict] = []
    encoded = urllib.parse.quote(query)
    for page in range(1, pages + 1):
        url = f"{API}/search/issues?q={encoded}&per_page={per_page}&page={page}"
        data = request_json(url)
        out.extend(data.get("items", []))
        if len(data.get("items", [])) < per_page:
            break
        time.sleep(0.25)
    return out


def get_comments(comments_url: str, max_comments: int) -> list[dict]:
    try:
        comments = request_json(f"{comments_url}?per_page={max_comments}")
    except Exception:
        return []
    if not isinstance(comments, list):
        return []
    return comments[:max_comments]


def matched(patterns: list[str], text: str) -> list[str]:
    hits = []
    for pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            hits.append(pattern)
    return hits


def excerpt(text: str, limit: int = 1200) -> str:
    compact = re.sub(r"\n{3,}", "\n\n", text.strip())
    if len(compact) <= limit:
        return compact
    return compact[:limit].rstrip() + "\n..."


def issue_to_candidate(issue: dict, comments: list[dict]) -> Candidate | None:
    body = issue.get("body") or ""
    comments_text = "\n\n".join(c.get("body") or "" for c in comments)
    combined = f"{issue.get('title')}\n\n{body}\n\n{comments_text}"
    raw_terms = matched(RAW_PATTERNS, combined)
    resolution_terms = matched(RESOLUTION_PATTERNS, combined)

    raw_score = len(raw_terms)
    resolution_score = len(resolution_terms)
    if issue.get("state_reason"):
        resolution_score += 1

    if raw_score < 4 or resolution_score < 1:
        return None

    repo_url = issue.get("repository_url", "")
    repo = repo_url.replace(f"{API}/repos/", "")
    return Candidate(
        title=issue.get("title") or "",
        html_url=issue.get("html_url") or "",
        repo=repo,
        number=int(issue.get("number") or 0),
        state_reason=issue.get("state_reason"),
        raw_score=raw_score,
        resolution_score=resolution_score,
        evidence_terms=raw_terms,
        resolution_terms=resolution_terms,
        body_excerpt=excerpt(body),
        comments_excerpt=excerpt(comments_text),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--pages", type=int, default=2)
    parser.add_argument("--per-page", type=int, default=30)
    parser.add_argument("--max-comments", type=int, default=20)
    args = parser.parse_args()

    seen: set[str] = set()
    candidates: list[Candidate] = []
    for query in QUERIES:
        print(f"query: {query}", file=sys.stderr)
        for issue in search_issues(query, args.pages, args.per_page):
            url = issue.get("html_url") or ""
            if not url or url in seen:
                continue
            seen.add(url)
            comments = get_comments(issue.get("comments_url") or "", args.max_comments)
            candidate = issue_to_candidate(issue, comments)
            if candidate:
                candidates.append(candidate)
        time.sleep(0.5)

    candidates.sort(key=lambda c: (c.raw_score + c.resolution_score, c.raw_score), reverse=True)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps([asdict(c) for c in candidates], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"wrote {len(candidates)} candidates to {output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
