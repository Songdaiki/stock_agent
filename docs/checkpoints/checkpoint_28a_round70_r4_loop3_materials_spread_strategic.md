# Checkpoint 28A Round 70 R4 Loop 3 Materials / Spread / Strategic Resources

## Scope

Round 70 reflects `docs/round/round_70.md`.

This patch is calibration/evaluation material only. It does not change production
scoring, StageClassifier thresholds, RedTeam rules, or candidate generation.

## What Changed

- Added R4 Loop-3 canonical archetype splits:
  - `LUBRICANTS_HIGH_MARGIN_MIX`
  - `COPPER_AI_GRID_STRUCTURAL_DEMAND`
  - `EVENT_PREMIUM_GOVERNANCE_OVERLAY`
  - `COMMODITY_PRICE_4C_OVERLAY`
- Added R4 Loop-3 score-profile draft:
  - `data/sector_taxonomy/score_weight_profiles_round70_r4_loop3_v3.csv`
- Added R4 Loop-3 case pack:
  - `data/e2r_case_library/cases_r4_loop3_round70.jsonl`
- Added report builder:
  - `src/e2r/sector/round70_r4_loop3_materials_spread_strategic.py`
  - `src/e2r/cli/build_round70_r4_loop3_report.py`
- Added tests:
  - `tests/test_round70_r4_loop3_materials_spread_strategic.py`

## Generated Reports

Generated under:

`output/e2r_round70_r4_loop3_materials_spread_strategic/`

Files:

- `round70_r4_loop3_materials_spread_strategic_summary.md`
- `round70_r4_loop3_case_matrix.csv`
- `round70_r4_loop3_stage_date_plan.csv`
- `round70_r4_loop3_green_guardrails.md`
- `round70_r4_loop3_risk_overlays.md`
- `round70_r4_loop3_price_validation_plan.md`
- `round70_r4_loop3_price_fields.csv`

## Summary

- target_count: 16
- case_candidate_count: 14
- structural_success_count: 1
- success_candidate_count: 3
- cyclical_success_count: 3
- event_premium_count: 3
- overheat_count: 1
- stage4b_case_count: 3
- stage4c_case_count: 3
- green_possible_count: 5
- redteam_first_count: 5
- gate_only_target_count: 2
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## Interpretation

R4 Loop 3 separates four things that look similar in price charts:

- structural resource rerating
- commodity/spread cycle
- event premium
- speculative material theme

Simple example:

`희토류 가격 급등` is useful routing evidence. It is not Stage 3-Green evidence
unless the company also has production capacity, price floor, offtake, customer
contracts, and a visible FCF path.

Another example:

`정유 영업이익 흑자전환` can be real and important, but if it came from crack
spread or inventory gain, the patch keeps it as cycle/Watch until core margin
and repeat FCF are verified.

## Key Guardrails

- Do not apply Round-70 v3.0 weights to production scoring yet.
- Do not treat commodity price, spread recovery, tender offers, policy headlines,
  or science themes as Green evidence by themselves.
- Do not invent spread, offtake, price floor, production capacity, FCF, capital
  return, project FID, or stage prices.
- Korea Zinc-style tender offers are event premium first.
- Chemical spread recovery is RedTeam-first when China/Middle East oversupply can
  reverse OP/FCF.
- Copper AI-grid demand is Watch-to-Green only after cost curve, production,
  FCF, and capital return are verified.

## Verification

Commands run:

```bash
PYTHONPATH=src python -m unittest tests.test_round70_r4_loop3_materials_spread_strategic -v
PYTHONPATH=src python -m e2r.cli.build_round70_r4_loop3_report
```

Result:

- Round-70 focused tests passed.
- Reports were generated.

Full repository test result is recorded in the final commit summary for this
round.
