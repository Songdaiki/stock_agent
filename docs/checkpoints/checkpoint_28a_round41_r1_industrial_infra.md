# Checkpoint 28A Round 41: R1 Industrial Orders / Infrastructure

## Summary

Round 41 applied the Round-40 protocol to R1:

```text
R1 = 산업재·수주·인프라
```

The core rule is:

```text
수주 뉴스
-> 계약질 / 납품기간 / 수주잔고 / 마진 / EPS 상향 확인
-> 가격 경로 검증
-> 그 다음에만 Stage 3 후보 여부를 판단
```

This patch does not change production scoring, StageClassifier thresholds, candidate generation, or RedTeam logic.

## What Was Added

- `src/e2r/sector/round41_r1_industrial_infra.py`
- `src/e2r/cli/build_round41_r1_report.py`
- `tests/test_round41_r1_industrial_infra.py`
- `data/e2r_case_library/cases_r1_round41.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round41_r1_v1.csv`
- `output/e2r_round41_r1_industrial_infra/round41_r1_industrial_infra_summary.md`
- `output/e2r_round41_r1_industrial_infra/round41_r1_case_matrix.csv`
- `output/e2r_round41_r1_industrial_infra/round41_r1_stage_date_plan.csv`
- `output/e2r_round41_r1_industrial_infra/round41_r1_green_guardrails.md`
- `output/e2r_round41_r1_industrial_infra/round41_r1_price_validation_plan.md`
- `output/e2r_round41_r1_industrial_infra/round41_r1_price_fields.csv`

## R1 Targets

Round 41 records 12 R1 targets:

- `GRID_TRANSFORMER_SHORTAGE`
- `CONTRACT_BACKLOG_INDUSTRIAL`
- `DEFENSE_GOVERNMENT_BACKLOG`
- `DEFENSE_TECH_AUTONOMOUS_SYSTEMS`
- `DEFENSE_DRONE_COUNTER_UAS`
- `DEFENSE_AI_SOFTWARE_INTELLIGENCE`
- `SHIPBUILDING_OFFSHORE_BACKLOG`
- `RAIL_INFRASTRUCTURE`
- `NUCLEAR_SMR_GRID_POLICY`
- `GEOPOLITICAL_RECONSTRUCTION`
- `SMART_FACTORY_AUTOMATION`
- `AI_DATA_CENTER_POWER_EQUIPMENT`

## Case Pack

The Round 41 case pack contains 15 records:

- structural_success: 1
- success_candidate: 7
- cyclical_success: 1
- event_premium: 1
- failed_rerating: 2
- 4B-watch: 1
- 4C-thesis-break: 2

Examples:

- `hanwha_aerospace_romania_k9_success_case`: strong government backlog case, still needs 1Y/2Y price-path and EPS revision backfill.
- `hanwha_aerospace_dilution_risk_case`: shows why strong defense backlog still needs capital-allocation RedTeam checks.
- `nuscale_cfpp_cancel_4c_case`: SMR policy narrative can break on cost, financing, and customer subscription failure.
- `geopolitical_reconstruction_no_contract_event_watch`: reconstruction or mega-project policy is not Green evidence without a binding contract.

## Guardrails

- R1 is Green-capable, but Green is not automatic.
- Order headlines, MOU, policy events, and case IDs are not score evidence.
- Missing contract size, duration, margin, EPS, FCF, or price fields remain missing.
- R1 v1.0 weights are shadow/calibration material only.
- No production scoring change was made.

## Verification

Commands run:

```bash
PYTHONPATH=src python -m unittest tests.test_round41_r1_industrial_infra -v
PYTHONPATH=src python -m e2r.cli.build_round41_r1_report
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
git diff --check -- docs/round/round_41.md src/e2r/sector/round41_r1_industrial_infra.py src/e2r/cli/build_round41_r1_report.py tests/test_round41_r1_industrial_infra.py data/e2r_case_library/cases_r1_round41.jsonl data/sector_taxonomy/score_weight_profiles_round41_r1_v1.csv output/e2r_round41_r1_industrial_infra docs/checkpoints/checkpoint_28a_round41_r1_industrial_infra.md
```

Targeted Round 41 tests passed.

The full test suite still has the pre-existing Round 17 fixture-file issue from the deleted `docs/round/round_17.md`; Round 41 did not introduce that failure.
