# Checkpoint 28A-6: Round 4 Score-Price Validation

## Summary

Round 4 was applied as calibration material only. Production scoring and
StageClassifier thresholds were not changed.

The analyst note in `docs/round/round_04.md` was converted into:

- case-library schema extensions for price-path validation
- stage failure type labels
- score-price alignment rules
- archetype-specific Green guardrails for platform, game/IP, robotics, retail,
  construction/PF, utilities, nuclear, governance, financials, biotech, medical
  device, travel, AI data center, and education/service cases

## Implemented Files

- `src/e2r/sector/round4_score_price_validation.py`
- `src/e2r/cli/build_round4_score_price_validation_report.py`
- `tests/test_round4_score_price_validation.py`
- `docs/e2r_score_price_validation_round4.md`
- `output/e2r_round4_score_price_validation/round4_score_price_validation_rules.md`
- `output/e2r_round4_score_price_validation/round4_case_field_contract.md`
- `output/e2r_round4_score_price_validation/round4_alignment_summary.csv`
- `output/e2r_round4_score_price_validation/round4_stage_failure_matrix.md`

## Schema Changes

`PriceValidation` now supports:

- `peak_return_from_stage3`
- `time_to_50pct`
- `time_to_100pct`
- `time_to_200pct`

`E2RCaseRecord` now supports:

- `stage_failure_type`

Example:

```text
로봇 테마주
-> 대기업 투자 뉴스는 있음
-> 실제 매출 전환은 없음
-> 주가는 급등 후 되돌림
-> stage_failure_type = should_have_been_red
```

## Key Round 4 Rule

Score and Stage must be checked against the later price path. A high score is
not enough if it did not become a rerating, and a price rally is not enough if
it was not backed by EPS/FCF evidence.

## Current Output

The current v0.2 case pack still has incomplete price/stage failure data:

```text
stage_failure_type unknown: 66
green_success: 0
false_green: 0
missed_structural: 0
```

This means Round 4 mostly created the validation structure. The next work is to
fill stage dates and price paths, then rerun alignment evaluation.

## What Not To Change

- Do not lower Stage 3-Green thresholds.
- Do not use case records as candidate-generation input.
- Do not treat event premium as true structural rerating.
- Do not treat price-only rallies as EPS/FCF evidence.
- Do not apply archetype score weights until coverage and price validation are
  filled.

## Verification

Commands run:

```bash
PYTHONPATH=src python -m unittest tests.test_round4_score_price_validation tests.test_case_price_backfill tests.test_score_price_alignment -v
PYTHONPATH=src python -m e2r.cli.build_round4_score_price_validation_report --cases data/e2r_case_library/cases_v02.jsonl --output-directory output/e2r_round4_score_price_validation
```

Full test run was executed after the patch before commit.
