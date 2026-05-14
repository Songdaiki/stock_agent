# Checkpoint 28A-15: Round 14 Score-Weight v0.4

## Summary

Round 14 was added as calibration material, not production scoring logic.

The round reinforces the correct direction:

```text
theme tag -> large sector -> archetype -> evidence field -> score hypothesis -> price validation
```

This keeps theme labels such as `스테이블코인`, `편의점`, `초전도체`, or `폐배터리` from becoming direct score inputs.

## Added

- `src/e2r/sector/round14_score_weight_v04.py`
- `src/e2r/cli/build_round14_score_weight_report.py`
- `tests/test_round14_score_weight_v04.py`
- `docs/e2r_score_weight_normalization_round14.md`
- Round 14 output reports under `output/e2r_round14_score_weight_v04/`
- Round 14 CSVs under `data/sector_taxonomy/`

## Covered Theme Families

- Retail / convenience / offline logistics
- Insurance underwriting and value-up
- Payment / fintech infrastructure
- Digital asset tokenization
- K-beauty OEM/ODM supply chain
- Battery recycling / ESS shift
- Hydrogen / renewable policy infrastructure
- Tire / auto component spread
- CDMO healthcare contracts
- Platform / software / security
- Robotics / factory automation
- Construction / PF / building materials
- Disease / pest event demand
- Speculative science themes
- Agri / livestock / food commodity cycles

## Guardrails

- `production_scoring_changed: false`
- `theme_tags_are_score_input: false`
- StageClassifier thresholds were not changed.
- Green remains evidence-backed.
- RedTeam-first themes remain guarded unless recurring EPS/FCF evidence appears.

## Easy Example

`편의점` can be a useful search tag.

But it does not create a Green candidate by itself. It needs store efficiency, OPM improvement, inventory discipline, and FCF improvement. If only foot traffic improves while delivery cost or rent pressure rises, it stays Watch/Yellow or becomes a risk case.

## Verification

- Round 14 tests added.
- Production scoring modules are tested to ensure they do not import the Round 14 calibration module.

## Next Step

Use Round 14 to build `cases_v03.jsonl`, backfill price paths, and run score-price alignment before any shadow scoring.
