# Checkpoint 28A Round 62: R9 Loop 2 Mobility/Transport/Leisure

Round 62 adds the R9 Loop-2 calibration pack for mobility, transport, and leisure.

This is calibration and evaluation material only. It does not change production scoring, StageClassifier thresholds, or candidate generation.

## What Changed

- Added `src/e2r/sector/round62_r9_loop2_mobility_transport_leisure.py`.
- Added `src/e2r/cli/build_round62_r9_loop2_report.py`.
- Added `tests/test_round62_r9_loop2_mobility_transport_leisure.py`.
- Generated:
  - `data/e2r_case_library/cases_r9_loop2_round62.jsonl`
  - `data/sector_taxonomy/score_weight_profiles_round62_r9_loop2_v2.csv`
  - `output/e2r_round62_r9_loop2_mobility_transport_leisure/`

## Core Rule

R9 must not score demand recovery, hybrid labels, tourism policy, freight spikes, eVTOL milestones, or space themes as Stage 3 evidence by themselves.

Simple example:

- Weak evidence: “Part 135 approval was received.”
- Stronger evidence: “Type certification, commercial flight revenue, unit economics, and cash runway are verified.”

## Target Coverage

Round 62 covers 14 targets:

- `AUTO_MOBILITY_COMPLETED_VEHICLE`
- `AUTO_MOBILITY_COMPONENTS`
- `AUTO_COMPONENTS_EV_ADAS`
- `TIRE_AUTO_COMPONENT_SPREAD`
- `AIRLINE_TRAVEL_CYCLE`
- `TRAVEL_LEISURE_REOPENING`
- `CASINO_DUTYFREE_TOURISM`
- `SHIPPING_FREIGHT_CYCLE`
- `LOGISTICS_PARCEL_FREIGHT`
- `RENTAL_USED_CAR_MOBILITY`
- `MOBILITY_RENTAL_MICROMOBILITY`
- `URBAN_AIR_DRONE`
- `SPACE_SUPPLYCHAIN`
- `SATELLITE_CONNECTIVITY_INFRA`

Counts:

- Targets: 14
- Case records: 15
- Success candidates: 4
- Cyclical success records: 1
- Event premium records: 2
- 4B watch cases: 9
- 4C thesis-break cases: 6
- Green-possible targets: 2

## Case Pack

Key cases added:

- Hyundai hybrid value-up and shareholder-return case
- Hyundai tariff margin-cut watch case
- Toyota hybrid parts bottleneck reference
- Korean Air / Asiana integration cycle-watch case
- China group visa tourism policy event
- SES airline connectivity backlog case
- Maersk overcapacity and Suez route normalization cases
- Hertz EV rental unit-economics failures
- Michelin tire demand cut case
- Lime micromobility FCF/debt watch case
- Joby discounted offering case
- Lilium eVTOL cash-crunch counterexample
- Archer Part 135 without type-certification case

## Guardrails

- Do not use Round 62 cases as candidate-generation input.
- Do not change production scoring from this pack.
- Do not invent OPM, FCF, tariff cost, freight rates, casino drop amount, unit economics, certification, backlog, or stage prices.
- Keep Stage 3-Green strict.
- Treat shipping overcapacity, EV rental residual-value failure, eVTOL cash burn, tire demand cuts, tourism policy-only rallies, and micromobility going-concern risk as RedTeam gates.

## Generated Reports

The CLI writes:

- `round62_r9_loop2_mobility_transport_leisure_summary.md`
- `round62_r9_loop2_case_matrix.csv`
- `round62_r9_loop2_stage_date_plan.csv`
- `round62_r9_loop2_green_guardrails.md`
- `round62_r9_loop2_risk_overlays.md`
- `round62_r9_loop2_price_validation_plan.md`
- `round62_r9_loop2_price_fields.csv`

## Verification

Targeted tests:

```bash
PYTHONPATH=src python -m unittest tests.test_round62_r9_loop2_mobility_transport_leisure -v
```

Report generation:

```bash
PYTHONPATH=src python -m e2r.cli.build_round62_r9_loop2_report
```

Full verification was run after implementation.
