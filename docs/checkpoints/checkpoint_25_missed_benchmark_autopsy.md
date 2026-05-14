# Checkpoint 25: Blind Replay Miss Autopsy

## What Changed

Added a post-replay autopsy layer that reads the no-proxy blind replay output and explains why benchmark labels were missed.

This does not generate candidates and does not change scoring.

Flow:

```text
blind replay output
-> benchmark recall rows
-> discovered candidates
-> search/report snapshot stores
-> source coverage summary
-> miss reason and fix plan
```

Example:

```text
일진전기 missed
-> no search snapshot
-> no report snapshot
-> no official price/disclosure/financial archive
-> recommended fix: add_search_snapshot first
```

## Files Added

```text
src/e2r/backtest/missed_benchmark_autopsy.py
src/e2r/cli/analyze_blind_replay_misses.py
tests/test_missed_benchmark_autopsy.py
```

## Reports Written

The CLI writes:

```text
output/backtests/blind_discovery_autopsy/2026-05-14_autopsy.json
output/backtests/blind_discovery_autopsy/2026-05-14_autopsy.md
output/backtests/blind_discovery_autopsy/evidence_gap_matrix.csv
output/backtests/blind_discovery_autopsy/recommended_fixes.md
```

These output files are not committed.

## Command Run

```bash
PYTHONPATH=src python -m e2r.cli.analyze_blind_replay_misses \
  --blind-output output/backtests/blind_discovery/2023-01-01_to_2026-05-14 \
  --benchmark-labels data/benchmark_labels/e2r_known_winners.json \
  --output-directory output/backtests/blind_discovery_autopsy \
  --run-date 2026-05-14
```

## Recall Result

No-proxy blind replay:

```text
labels_analyzed: 13
detected: 3
missed: 10
missing_snapshot_related: 10
scoring_or_threshold_related: 0
acceptable_warning_misses: 3
```

Detected labels:

```text
HD현대일렉트릭
효성중공업
삼양식품
```

Missed labels:

```text
일진전기
산일전기
한화에어로스페이스
실리콘투
삼성전자 메모리 리레이팅
SK하이닉스 메모리 리레이팅
씨젠
에코프로비엠
HMM
대한전선-like
```

## Miss Reasons

Primary reason distribution:

```text
no_search_snapshot: 7
stage_not_green_but_detected: 2
detected: 1
outside_expected_window: 1
not_in_universe: 2
```

Detected but not Stage 3-Green:

```text
HD현대일렉트릭
효성중공업
```

This is acceptable for now. The purpose of this checkpoint is Layer-1 recall and evidence coverage, not forcing Stage 3-Green.

## Evidence Coverage

Current no-proxy evidence coverage is thin:

```text
HD현대일렉트릭: search/report snapshot exists, no official archive
효성중공업: search/report snapshot exists, no official archive
삼양식품: search/report snapshot exists, no official archive
씨젠: search/report/news snapshot exists, but expected window was before replay start
```

Most misses are not scoring failures. They are source coverage failures:

```text
no official price archive
no OpenDART disclosure snapshot archive
no financial actual snapshot archive
no search/report snapshots for many labels
```

## Recommended Fix Priority

Autopsy recommended fixes:

```text
add_search_snapshot: 7
manual_review: 3
no_action_expected_false_positive: 3
```

Add evidence snapshots first for:

```text
일진전기
산일전기
한화에어로스페이스
실리콘투
삼성전자 메모리 리레이팅
SK하이닉스 메모리 리레이팅
HMM
```

For each, add:

```text
1. search snapshot
2. report/news snapshot text
3. price history
4. OpenDART disclosure snapshot
5. financial actual snapshot
```

## Acceptable Misses

These are warning/false-positive labels and should not be forced into Green:

```text
씨젠
에코프로비엠
대한전선-like
```

Current recommendation:

```text
no_action_expected_false_positive
```

This means:

```text
The miss is acceptable unless we specifically want warning-case monitoring coverage.
```

## Is This A Threshold Problem?

Not yet.

The autopsy found:

```text
scoring_or_threshold_related: 0 missed labels
```

So the next fix should not be:

```text
lower Stage 3-Green threshold
```

The next fix should be:

```text
add missing historical source snapshots
```

## Weekly Blind Replay Readiness

Not ready yet.

Reason:

```text
weekly replay would mostly repeat the same source-coverage gaps
```

Minimum readiness target:

```text
add search/report snapshots for the 7 source-missing labels
add historical official price/disclosure/financial snapshots
rerun monthly no-proxy blind replay
then run weekly on the improved archive
```

## What Not To Change

Do not:

```text
lower Stage 3-Green thresholds to improve recall
use benchmark labels as evidence
claim fixture proxy success as blind discovery
fabricate report/news snapshots
```

## Verification

Commands run:

```bash
PYTHONPATH=src python -m unittest tests.test_missed_benchmark_autopsy -v
PYTHONPATH=src python -m e2r.cli.analyze_blind_replay_misses ...
```

Full verification is covered by the final test run for this checkpoint.
