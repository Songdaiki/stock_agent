# Checkpoint 28A Round 30: Score-Weight v1.5 Calibration Pack

## Summary

Round 30 반영은 production scoring 변경이 아니라 calibration/evaluation pack 추가다.
예를 들면 `HBM 장비`는 HBM 수요의 2차 수혜가 될 수 있지만, 고객사 CAPEX가 줄면 바로 논리가 훼손될 수 있다. 그래서 HBM 자체보다 visibility를 낮추고 customer CAPEX risk를 더 강하게 둔다.

## Added

- `src/e2r/sector/round30_score_weight_v15.py`
- `src/e2r/cli/build_round30_score_weight_report.py`
- `tests/test_round30_score_weight_v15.py`
- `data/e2r_case_library/cases_v12_round30.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round30_v15.csv`
- `output/e2r_round30_score_weight_v15/round30_score_weight_v15_summary.md`
- `output/e2r_round30_score_weight_v15/round30_case_candidate_matrix.csv`
- `output/e2r_round30_score_weight_v15/round30_green_guardrail_review.md`
- `output/e2r_round30_score_weight_v15/round30_cycle_cap_review.md`
- `output/e2r_round30_score_weight_v15/round30_semicapex_boundary_review.md`
- `output/e2r_round30_score_weight_v15/round30_price_validation_plan.md`

## Coverage

- score target count: 10
- case candidate count: 28
- success / structural / cyclical candidate count: 13
- 4C thesis-break case count: 5
- Green-possible target count: 3
- Watch-first target count: 6
- RedTeam-first target count: 1

## Main Calibration Changes

- Semi equipment/materials/PCB is Watch-to-Green because it depends on customer CAPEX, delivery conversion, and inventory discipline.
- Completed vehicles can be Green-possible when hybrid/mix, FCF, ROE/PBR rerating, and shareholder return are source-backed.
- Auto parts and tires remain Watch-to-Green because customer concentration, raw materials, and quality cost are strong risks.
- Airlines, casino/duty-free tourism, and agri/livestock are cycle-heavy and should not become Green from policy or reopening headlines alone.
- Convenience retail must score same-store sales, PB mix, OPM, and FCF, not store count.
- Space/drone narratives require actual delivery contracts, government/defense customers, certification, and repeat revenue.
- AI data-center cooling and memory/HBM remain Green-possible but require 4B/4C monitoring for CAPEX reversal, overbuild, and crowding.

## Guardrails

- Case IDs and theme labels are not production candidate input.
- No production scoring, staging, or RedTeam thresholds changed.
- No stage dates, prices, contract size, OP YoY, ASP, OPM, store productivity, tourist mix, CAPEX, or FCF were invented.
- Stage 3-Green remains strict and must still require cross-evidence plus price-path validation.

## Verification

```bash
PYTHONPATH=src python -m unittest tests.test_round30_score_weight_v15 -v
PYTHONPATH=src python -m e2r.cli.build_round30_score_weight_report
```

The full suite is still expected to show the pre-existing unrelated `round_17.md` deletion failures until that deleted round document is restored or the old test is retired.
