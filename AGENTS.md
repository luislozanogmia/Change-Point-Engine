# Agent Instructions

Use this repo as a deterministic pre-analysis step for performance problems.

## Goal

Do not ask the model to discover root cause directly from noisy metrics. Compute the performance structure first, then let the model explain it.

## Workflow

1. Collect the available metrics, benchmark table, incident timeline, or observability export.
2. Convert it to CSV:

   ```csv
   timestamp,service,metric,value
   ```

3. Run:

   ```bash
   python3 change_trace_engine.py <path-to-csv>
   ```

4. Read the `DETECTOR ROUTE`, `SIGNAL BLOCKS`, `CANDIDATE CASCADES`, `OPTIONS FOR THE LLM TO WEIGH`, and `GUARDRAIL` sections.
5. Use the trace as structured evidence, not as proof.
6. Explain:

   - The performance issue
   - The evidence
   - What is missing
   - The next diagnostic step

## Guardrails

- Do not turn timing into causality without dependency, deploy, resource, profile, bisection, or owner evidence.
- Do not collapse phased remediation into one root cause.
- Preserve version, canary, revert, and fix labels.
- Preserve named mechanisms as evidence labels, not automatic root cause.
- If the trace says evidence is thin, ask for more metrics.

## Model Guidance

Any model can read the trace. For autonomous tasks that fetch logs, inspect source issues, run comparisons, or write diagnostics, prefer frontier AI models.

