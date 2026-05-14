# Checkpoint 22 Monthly Replay Suite

## What Changed

Checkpoint 22 adds an operator-grade monthly replay suite on top of the Checkpoint 21 historical replay engine.

The suite runs these modes together:

```text
case_fixture
official_only
hybrid
```

and writes one report folder:

```text
output/backtests/monthly_replay_suite/YYYY-MM-DD_to_YYYY-MM-DD/
```

Simple example:

```text
case_fixture says HD현대일렉트릭 reached Stage 3-Green
official_only says the same case is limited by missing report/news evidence
hybrid shows the practical replay result when report fixtures exist
```

That distinction matters because a report-driven historical winner should not be treated as proven by official-only data.

## Commands Run

Implementation verification:

```bash
PYTHONPATH=src python -m unittest tests.test_monthly_replay_suite -v
```

Full requested monthly suite:

```bash
PYTHONPATH=src python -m e2r.cli.run_monthly_replay_suite \
  --start-date 2023-01-01 \
  --end-date 2026-05-14 \
  --modes case_fixture,official_only,hybrid \
  --frequency monthly \
  --output-directory output/backtests/monthly_replay_suite
```

Full test suite was also run after implementation.

## Output Files

The suite generated:

```text
suite_summary.md
suite_summary.json
mode_comparison.md
mode_comparison.json
stage3_lifecycle_summary.md
stage3_lifecycle_results.csv
stage3_lifecycle_results.json
known_case_validation.md
missed_winners.md
false_positives.md
stage4b_4c_review.md
evidence_coverage.md
next_backtest_readiness.md
top_stage3_candidate_cards.md
```

Each mode also preserves its Checkpoint 21 outputs under:

```text
case_fixture/
official_only/
hybrid/
```

These are under `output/` and are not committed.

## Monthly Suite Result

Run period:

```text
2023-01-01 to 2026-05-14
```

Top-level counts from the fixture monthly replay:

```text
replay_dates: 126
total scanned instruments/cases: 1008
total candidates: 702
event_search_or_higher: 702
deep_research: 418
Stage 2: 32
Stage 3-Green: 202
Stage 3-Yellow: 46
Stage 3-Red: 84
Stage 4B: 0
Stage 4C: 0
still_active: 10
missed known winners: 6
false-positive / boom-bust rows: 6
```

Interpretation:

```text
Layer 1 recall is active.
Stage 3-Green is still deterministic.
The large Stage 3 counts are monthly repeated fixture detections, not unique live discoveries.
```

## Mode Comparison

The generated mode comparison showed:

```text
case_fixture:
  candidates: 234
  Green / Yellow / Red: 101 / 23 / 42
  missed winners: 0

official_only:
  candidates: 234
  Green / Yellow / Red: 0 / 0 / 0
  missed winners: 8

hybrid:
  candidates: 234
  Green / Yellow / Red: 101 / 23 / 42
  missed winners: 0
```

This is expected for the current fixture set.

Example:

```text
HD현대일렉트릭 is report-driven in the fixture.
case_fixture can replay it.
official_only excludes that report and records the limitation.
```

## Stage 3 Lifecycle Highlights

For Stage 3-Green lifecycle rows:

```text
count: 6
average MFE_1Y: 2.575845
average MAE_1Y: -0.040361
below_entry_rate: 0.0
average time_to_50pct: 1.333333
average time_to_100pct: 2.0
average time_to_200pct: 2.0
median peak_return_from_stage: 2.522727
worst drawdown_after_peak: -0.322581
```

For Stage 3-Yellow lifecycle rows:

```text
count: 2
average MFE_1Y: 0.566667
average MAE_1Y: -0.066667
below_entry_rate: 0.0
```

Stage 3-Red rows exist in candidate snapshots, but the current Korea lifecycle slice has no valid post-2023 price-path rows for those warning cases in this run.

## Known Cases

Known structural cases are present in `known_case_validation.md`, including:

```text
HD현대일렉트릭
효성중공업
일진전기
산일전기
삼양식품
한화에어로스페이스
```

Known warning cases are also present:

```text
씨젠
SMCI
대한전선-like
```

NVIDIA and Zoom are US fixtures, so they are not included in the default KR monthly suite unless the replay market is expanded.

## Missed Winners

Missed structural winners in this suite are official-only misses.

Reason:

```text
official_only_excluded_report_news
```

This is acceptable for the current official-only fixture replay, but it is not sufficient for live-discovery proof.

Recommended fix:

```text
add historical report/news snapshots
or run hybrid for practical replay
```

## False Positives

The suite did not show one-off or boom-bust fixtures becoming unsafe Stage 3-Green.

Examples:

```text
씨젠 -> contained as Stage 3-Red in case_fixture/hybrid
대한전선-like -> not Stage 3-Green
```

This aligns with the E2R rule:

```text
one-off demand != structural E2R
```

## 4B / 4C Findings

The suite writes `stage4b_4c_review.md`.

In this monthly KR run:

```text
Stage 4B count: 0
Stage 4C count: 0
```

This should not be read as proof that 4B/4C is unnecessary.
It means the current KR monthly fixture slice lacks enough 4B/4C lifecycle evidence.

The suite preserves the rule:

```text
No 4B evidence -> do not fabricate 4B
```

## Evidence Coverage

Aggregate evidence counts:

```text
disclosure: 627
research_report: 418
news: 70
financial_actual: 702
consensus: 418
consensus_revision: 418
price: 762
```

Limitations:

```text
missing_report_news_snapshot_count: 632
official_only excludes report/news/consensus fixtures by design
4B evidence coverage remains sparse
```

## Larger Backtest Readiness

Status:

```text
ready for a larger fixture backtest: yes, with limitations
```

Best next mode:

```text
hybrid weekly
```

Do not loosen Stage 3-Green thresholds yet.
The right next step is evidence expansion, not easier Green classification.

Recommended next patches:

```text
add more historical report/news snapshots
add more 4B evidence fixtures
expand official historical disclosure/financial rows
then run hybrid weekly before daily
```
