# Checkpoint 27: As-Of Stage Promotion Autopsy

## What Changed

- Added stage-gate diagnostics that mirror the current `StageClassifier` thresholds without changing them.
- Added an as-of stage-promotion autopsy CLI:
  `PYTHONPATH=src python -m e2r.cli.analyze_asof_stage_promotion ...`
- Added output files under `output/backtests/asof_stage_promotion_autopsy/`:
  - `2026-05-14_autopsy.md`
  - `2026-05-14_autopsy.json`
  - `score_components_by_candidate.csv`
  - `stage_gate_matrix.csv`
  - `feature_input_coverage.csv`

## Why It Was Needed

The as-of replay was finding benchmark names, but most stayed at Stage 0 or Stage 1.
The autopsy now shows the exact gate that blocks promotion.

Example:

- HD현대일렉트릭 now reaches Stage 2 after merged evidence scoring.
- It does not become Stage 3-Green because the Green gates for total score, visibility, bottleneck, valuation, and contract quality still fail.
- That is intentional: Stage 3-Green thresholds were not loosened.

## Gate Results

Latest autopsy on `output/backtests/asof_research_replay/2023-01-01_to_2026-05-14`:

- candidates analyzed: 53
- Stage 2 in autopsy sample: 19
- Stage 3-Green: 0
- Stage 3-Yellow: 0
- Stage 3-Red: 0
- Red Team hard blocks: 0
- Parser audit hard blocks: 0

Detected benchmark gate summary:

| Case | Autopsy Stage | Main Block |
| --- | ---: | --- |
| HD현대일렉트릭 | 2 | Stage 3 total, visibility, bottleneck, valuation, contract quality |
| 효성중공업 | 1 | Stage 2 total score |
| 일진전기 | 2 | Stage 3 total, visibility, bottleneck, contract quality |
| 산일전기 | 1 | Stage 2 total score |
| 삼양식품 | 1 | Stage 2 total score |
| 한화에어로스페이스 | 1 | Stage 2 total and EPS/FCF |
| 실리콘투 | 0 | missing scored evidence coverage |
| 삼성전자 memory | 1 | Stage 2 total, valuation, information confidence |
| SK하이닉스 memory | 1 | Stage 2 total, valuation, information confidence |

## What Not To Change

- Do not lower Stage 3-Green thresholds just to improve recall.
- Do not use benchmark labels as evidence.
- Do not fabricate missing report, disclosure, EPS, FCF, RPO, or contract fields.
- Do not treat Stage 2 as conviction; it is a candidate-monitoring stage.

## Remaining Work

- Improve evidence coverage for cases still blocked by Stage 2 total score.
- Add stronger historical report/news snapshots for cases like 삼양식품, 산일전기, 한화에어로스페이스, 실리콘투, 삼성전자, and SK하이닉스.
- Improve scoring only where explicit evidence is parsed but not currently scored.
