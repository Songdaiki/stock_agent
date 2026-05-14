# Blind Discovery Replay Runbook

Blind discovery replay asks:

```text
Could E2R_STANDARD discover candidates without using the answer key?
```

The answer key is `data/benchmark_labels/e2r_known_winners.json`.
It is evaluation-only.

## Command

```bash
PYTHONPATH=src python -m e2r.cli.run_blind_discovery_replay \
  --start-date 2023-01-01 \
  --end-date 2026-05-14 \
  --frequency monthly \
  --market KR \
  --flow E2R_STANDARD \
  --output-directory output/backtests/blind_discovery
```

## Output

```text
blind_discovery_summary.md/json
discovered_candidates.csv/json
benchmark_recall_report.md/json
missed_benchmark_labels.md
false_positive_report.md
stage_lifecycle_report.md
evidence_coverage_report.md
limitations.md
```

## Evaluation Order

Correct order:

```text
1. run E2R_STANDARD candidate generation
2. write discovered candidates
3. load benchmark labels
4. compare labels against outputs
```

Wrong order:

```text
benchmark labels -> candidate generation
```

## Success Criteria

Structural labels:

```text
should appear at least in event_search/deep_research or Stage 2
within expected window tolerance
```

One-off / boom-bust labels:

```text
must not become Stage 3-Green
```

Missing historical report/news snapshots:

```text
must be reported, not hidden
```

## Current Limitation

The current repo has curated historical case fixtures.
It does not yet have complete archived search snapshots.

So a miss can mean:

```text
source_missing
no_report_snapshot
no_news_snapshot
not_in_universe
```

That is why future live runs should store search/report snapshots.
