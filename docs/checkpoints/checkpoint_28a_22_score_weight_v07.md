# Checkpoint 28A-22: Score-Weight v0.7 Recalibration Pack

## Purpose

Round 22 extends the calibration loop for thin and important archetypes. It is not a production scoring change.

The round adds v0.7 score-weight hypotheses and case-mining candidates for:

- `SECURITIES_BROKERAGE_CYCLE`
- `INSURANCE_UNDERWRITING_CYCLE`
- `EDUCATION_SPECIALTY_SERVICES`
- `RETAIL_ECOMMERCE_LOGISTICS`
- `BUILDING_MATERIALS_REIT`
- `CLOUD_AI_SOFTWARE_INFRA`
- `CRO_CLINICAL_SERVICE`
- `APPAREL_BRAND_OEM`
- `MEMORY_HBM_CAPACITY`
- `VALUE_UP_SHAREHOLDER_RETURN`

## Files Added

- `src/e2r/sector/round22_score_weight_v07.py`
- `src/e2r/cli/build_round22_score_weight_report.py`
- `tests/test_round22_score_weight_v07.py`
- `data/e2r_case_library/cases_v04_round22.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round22_v07.csv`
- `output/e2r_round22_score_weight_v07/round22_score_weight_v07_summary.md`
- `output/e2r_round22_score_weight_v07/round22_case_candidate_matrix.csv`
- `output/e2r_round22_score_weight_v07/round22_green_guardrail_review.md`
- `output/e2r_round22_score_weight_v07/round22_price_validation_plan.md`
- `output/e2r_round22_score_weight_v07/round22_stage4b_watch_review.md`

## Summary

- target_count: 10
- case_candidate_count: 40
- success_candidate_count: 18
- counterexample_or_risk_count: 22
- green_possible_count: 4
- watch_yellow_first_count: 6
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## Key Recalibrations

- Brokerage is Watch-first. Trading value can lift EPS, but durability is weak and PF/proprietary losses can break the thesis.
- Insurance emphasizes loss ratio, CSM/ROE, capital ratio, and shareholder return execution.
- Education remains Watch-first unless adult, overseas, B2B, or subscription revenue offsets birthrate/regulation risk.
- Retail and logistics prioritize OPM/FCF over sales growth.
- Building materials and REITs remain Green-restricted because PF, rates, vacancy, and dividend risk can dominate.
- Cloud/SaaS is Green-possible only through recurring revenue, margin, and FCF.
- CRO is weaker than CDMO but more scoreable than pre-revenue biotech when backlog and customer diversity exist.
- Apparel is more conservative than K-food/K-beauty because inventory, markdown, and channel concentration risk are high.
- HBM remains Green-possible, but large post-rerating crowding requires 4B-watch diagnostics.
- Value-up requires execution, ROE/FCF, and PBR/NAV logic. Policy expectation alone is Stage 1.

## Easy Examples

- A brokerage can look strong when market trading value jumps. But if PF losses hit at the same time, it should not become Green.
- An insurer can rerate from better ROE and capital return. But a low-PBR insurer with no buyback cancellation or dividend execution remains a value trap.
- SK Hynix-like HBM evidence can be structural, but after a huge multi-year run the system should turn on 4B-watch rather than keep treating price strength as fresh evidence.

## Guardrails

- Do not use `cases_v04_round22.jsonl` as candidate-generation input.
- Do not use case IDs, policy headlines, theme labels, or raw low-PBR/AI/turnover words as scoring evidence.
- Do not apply v0.7 score weights to production scoring yet.
- Do not invent stage dates, prices, CSM, K-ICS, ARR, FCF, turnover, margins, or contract values.

## Commands Run

```bash
PYTHONPATH=src python -m unittest tests.test_round22_score_weight_v07 -v
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m e2r.cli.build_round22_score_weight_report \
  --output-directory output/e2r_round22_score_weight_v07 \
  --cases data/e2r_case_library/cases_v04_round22.jsonl \
  --score-profiles data/sector_taxonomy/score_weight_profiles_round22_v07.csv
```

## Result

Round 22 is represented as a v0.7 calibration pack with explicit Green guardrails and 4B-watch separation. The next step is price-path backfill and shadow score-price validation.
