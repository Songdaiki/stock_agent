# Checkpoint 28A-5: Round-3 Extension Archetype Matrix

## Why

Round 2 made the first archetype matrix useful, but it still leaned on the 25
core buckets.

`docs/round/round_03.md` adds the next layer:

```text
core archetype
-> extension archetype
-> stage posture
-> case-record fields
```

Example:

```text
AI_DATA_CENTER_INFRASTRUCTURE
-> not just "전력기기"
-> power/cooling/server/network bottleneck
-> Green eligible only with confirmed orders and customer CAPEX visibility
```

## What Changed

Added:

- `src/e2r/sector/round3_extension_matrix.py`
- `src/e2r/cli/build_round3_extension_matrix_report.py`
- `tests/test_round3_extension_matrix.py`
- `docs/e2r_extension_matrix_round3.md`
- `output/e2r_round3_extension_matrix/round3_extension_archetype_plan.md`
- `output/e2r_round3_extension_matrix/round3_stage_posture_matrix.csv`
- `output/e2r_round3_extension_matrix/round3_case_record_field_contract.md`
- `output/e2r_round3_extension_matrix/round3_case_coverage_summary.md`

## Stage Posture

Round 3 separates archetypes into:

- `GREEN_ELIGIBLE`
- `YELLOW_WATCH`
- `RED_4B_GUARDRAIL`

This is report-facing calibration only.

Example:

```text
ROBOTICS_FACTORY_AUTOMATION
-> YELLOW_WATCH
-> customer adoption and revenue conversion required
-> no Green from MOU/theme alone

CONSTRUCTION_REAL_ESTATE_CREDIT
-> RED_4B_GUARDRAIL
-> PF/cash-flow risk dominates headline orders
```

## Priority

The first 12 Round-3 priority archetypes are:

1. `CONTRACT_BACKLOG_INDUSTRIAL`
2. `DEFENSE_GOVERNMENT_BACKLOG`
3. `SHIPBUILDING_OFFSHORE_BACKLOG`
4. `EXPORT_RECURRING_CONSUMER`
5. `K_BEAUTY_EXPORT_DISTRIBUTION`
6. `MEMORY_HBM_CAPACITY`
7. `SEMI_EQUIPMENT_CAPEX`
8. `FINANCIAL_SPREAD_BALANCE_SHEET`
9. `MEDICAL_DEVICE_HEALTHCARE_EXPORT`
10. `THEME_VALUATION_OVERHEAT`
11. `ONE_OFF_EVENT_DEMAND`
12. `AI_DATA_CENTER_INFRASTRUCTURE`

## Important

No production scoring changed.

The matrix is not imported by:

- feature engineering
- stage classification
- Red Team
- E2R standard pipeline

## Still Not Changed

- StageClassifier thresholds
- live candidate generation
- deterministic feature scoring
- Red Team decisions
