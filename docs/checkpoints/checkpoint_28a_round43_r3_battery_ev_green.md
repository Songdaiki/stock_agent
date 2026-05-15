# Checkpoint 28A Round 43: R3 Battery / EV / Green Energy

## Summary

Round 43 was converted into a calibration-only R3 case pack for `BATTERY_EV_GREEN`.

This patch does not change production scoring, staging, RedTeam, or candidate generation. It records the R3 research matrix as:

- R3 target sub-archetypes
- shadow score-weight drafts
- stage-date guidance
- case records
- price-validation fields
- Green/Watch/RedTeam guardrails

Simple example: an EV battery CAPEX headline is not enough. If the same evidence set later shows plant idle, worker furlough, EV demand slowdown, or raw-material price collapse, the case should move toward RedTeam/4C rather than Green.

## Files Added

- `src/e2r/sector/round43_r3_battery_ev_green.py`
- `src/e2r/cli/build_round43_r3_report.py`
- `tests/test_round43_r3_battery_ev_green.py`
- `data/e2r_case_library/cases_r3_round43.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round43_r3_v1.csv`
- `output/e2r_round43_r3_battery_ev_green/round43_r3_battery_ev_green_summary.md`
- `output/e2r_round43_r3_battery_ev_green/round43_r3_case_matrix.csv`
- `output/e2r_round43_r3_battery_ev_green/round43_r3_stage_date_plan.csv`
- `output/e2r_round43_r3_battery_ev_green/round43_r3_green_guardrails.md`
- `output/e2r_round43_r3_battery_ev_green/round43_r3_price_validation_plan.md`
- `output/e2r_round43_r3_battery_ev_green/round43_r3_price_fields.csv`

## Coverage

- target_count: 12
- case_candidate_count: 14
- structural_success_count: 1
- success_candidate_count: 3
- cyclical_success_count: 1
- event_premium_count: 1
- failed_rerating_count: 1
- stage4b_case_count: 1
- stage4c_case_count: 6
- green_possible_count: 1
- watch_yellow_first_count: 8
- redteam_first_count: 3

## Key Guardrails

- R3 should be conservative because growth themes can hide CAPEX overbuild, demand slowdown, subsidy risk, and commodity-price reversal.
- Battery materials and solar supply-chain stories are RedTeam-first until demand, utilization, margin, and FCF are proven.
- ESS, hydrogen, EV infrastructure, carbon compliance, and water reuse are Watch-to-Green only with contracts, utilization, and unit economics.
- Waste treatment is Green-capable when permits, treatment volume, utilization, and recurring FCF are source-backed.
- EV fire, recall, insurance cost, customs detention, worker furlough, project impairment, and lithium price crash are hard risk evidence.

## Verification

Commands run:

```bash
PYTHONPATH=src python -m unittest tests/test_round43_r3_battery_ev_green.py -v
PYTHONPATH=src python -m e2r.cli.build_round43_r3_report
```

Result:

- Round 43 tests passed.
- Reports and JSONL/CSV outputs were generated.
- Production modules are tested to avoid importing the Round 43 case pack.

Full-suite note: the broader repo currently has unrelated round-file deletions in the working tree, including `docs/round/round_17.md`, which is known to break existing round17 tests until restored or intentionally handled.
