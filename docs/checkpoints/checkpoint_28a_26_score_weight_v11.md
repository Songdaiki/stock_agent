# Checkpoint 28A-26: Round 26 Score-Weight v1.1 Calibration

## Purpose

Round 26 was applied as calibration material only.

The change adds v1.1 score-weight hypotheses and case candidates for:

- AI_DATA_CENTER_COOLING
- MEMORY_HBM_CAPACITY
- K_BEAUTY_EXPORT_DISTRIBUTION
- DIGITAL_ASSET_TOKENIZATION
- HYDROGEN_RENEWABLE
- CLOUD_AI_SOFTWARE_INFRA
- SECURITY_IDENTITY_DEEPFAKE
- CRO_CLINICAL_SERVICE
- CONSTRUCTION_BUILDING_MATERIALS
- INSURANCE_UNDERWRITING_CYCLE
- SECURITIES_BROKERAGE_CYCLE

Production scoring, StageClassifier thresholds, RedTeam rules, and candidate generation were not changed.

## Outputs

- `src/e2r/sector/round26_score_weight_v11.py`
- `src/e2r/cli/build_round26_score_weight_report.py`
- `tests/test_round26_score_weight_v11.py`
- `data/e2r_case_library/cases_v08_round26.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round26_v11.csv`
- `output/e2r_round26_score_weight_v11/round26_score_weight_v11_summary.md`
- `output/e2r_round26_score_weight_v11/round26_case_candidate_matrix.csv`
- `output/e2r_round26_score_weight_v11/round26_green_guardrail_review.md`
- `output/e2r_round26_score_weight_v11/round26_stage4b_watch_review.md`
- `output/e2r_round26_score_weight_v11/round26_risk_boundary_review.md`
- `output/e2r_round26_score_weight_v11/round26_price_validation_plan.md`

## Summary

- target_count: 11
- case_candidate_count: 40
- success_candidate_count: 16
- counterexample_or_risk_count: 24
- stage4b_case_count: 1
- stage4c_case_count: 10
- green_possible_count: 6
- watch_yellow_first_count: 5
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## Key Interpretation

Round 26 keeps the same rule: theme labels are routing clues, not score evidence.

Example: `액침냉각` or `AI cooling` can help generate a query, but it is not enough for score. A stronger cooling case needs direct data-center CAPEX linkage, confirmed order or delivery, cooling bottleneck evidence, repeat service revenue, and OP/EPS revision.

Example: K-beauty can be Green-possible, but only when export channels repeat, inventory and receivables are clean, and OPM/ROE evidence supports the rerating. Viral shipment growth alone stays weak.

Example: stablecoin/STO remains Watch-first until regulation, issuance, transaction volume, and fee economics are visible. A bill or policy headline is not revenue evidence.

Example: construction and building materials remain Watch-first because PF delinquency, unsold inventory, liquidity stress, and rates can dominate price hikes or dividend narratives.

## Green-Possible With Strict Gates

- AI_DATA_CENTER_COOLING
- MEMORY_HBM_CAPACITY
- K_BEAUTY_EXPORT_DISTRIBUTION
- CLOUD_AI_SOFTWARE_INFRA
- SECURITY_IDENTITY_DEEPFAKE
- INSURANCE_UNDERWRITING_CYCLE

## Watch-First / 4C-Sensitive

- DIGITAL_ASSET_TOKENIZATION
- HYDROGEN_RENEWABLE
- CRO_CLINICAL_SERVICE
- CONSTRUCTION_BUILDING_MATERIALS
- SECURITIES_BROKERAGE_CYCLE

## Guardrails

- Do not use Round 26 case IDs as candidate-generation input.
- Do not apply v1.1 weights to production scoring yet.
- Do not score policies, AI features, PoCs, revenue headlines, or theme labels without source-backed economics.
- Do not invent stage dates, prices, margins, retention, FCF, issuance volume, reimbursement, or contract values.
- Keep Stage 3-Green strict and cross-evidence based.
- Keep price-only rerating warnings as `price_only_4b_watch`, not evidence-based full 4B.

## Commands Run

```bash
PYTHONPATH=src python -m unittest tests.test_round26_score_weight_v11 -v
PYTHONPATH=src python -m compileall -q src/e2r/sector/round26_score_weight_v11.py src/e2r/cli/build_round26_score_weight_report.py tests/test_round26_score_weight_v11.py
PYTHONPATH=src python -m e2r.cli.build_round26_score_weight_report \
  --output-directory output/e2r_round26_score_weight_v11 \
  --cases data/e2r_case_library/cases_v08_round26.jsonl \
  --score-profiles data/sector_taxonomy/score_weight_profiles_round26_v11.csv
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Verification Result

- Round 26 unit tests passed.
- Compileall passed.
- Full repository test run still has an unrelated pre-existing blocker: `docs/round/round_17.md` is deleted in the working tree, so Round 17 tests cannot read their source document.

## Next Step

1. Backfill price paths for tradable Round 26 cases.
2. Keep synthetic/policy counterexamples marked as `needs_price_backfill` or `missing_price_data`.
3. Run shadow score-price alignment before applying any v1.1 weight to production scoring.
4. Validate K-beauty, HBM, cooling, insurance, and cloud/SaaS cases against actual MFE/MAE and 4B/4C paths.
