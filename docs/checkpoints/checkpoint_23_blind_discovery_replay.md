# Checkpoint 23 Blind Discovery Replay

## Purpose

Blind discovery replay evaluates E2R outputs against hidden benchmark labels only after candidate generation.

The core rule:

```text
E2R_STANDARD output first
benchmark labels second
```

## Added

```text
data/benchmark_labels/e2r_known_winners.json
src/e2r/backtest/benchmark_labels.py
src/e2r/backtest/blind_discovery_replay.py
src/e2r/cli/run_blind_discovery_replay.py
```

## Output

The CLI writes:

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

## Current Interpretation

The current repo has historical case fixtures, not complete archived search snapshots.

Therefore:

```text
detected label = candidate appeared from available historical fixture data
missed label = may be missing source/snapshot, not necessarily scoring failure
```

## Guardrail

Benchmark labels are not imported by:

```text
E2R_STANDARD
cheap scan
feature engineering
StageClassifier
RedTeam
```

Tests enforce this separation.
