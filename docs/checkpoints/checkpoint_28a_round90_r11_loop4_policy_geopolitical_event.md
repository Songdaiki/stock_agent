# Checkpoint 28A Round 90 R11 Loop 4 Policy / Geopolitical / Disaster / Event

## Scope

- source round: `docs/round/round_90.md`
- large sector: `POLICY_GEOPOLITICAL_EVENT`
- purpose: event, policy, disease, reconstruction, climate-disaster, and speculative-science themes are separated by whether they became actual contracts, budgets, financing, orders, revenue, or EPS/FCF evidence.
- production scoring changed: false
- case records used as candidate-generation input: false

## What Changed

- Added two canonical archetypes:
  - `REAL_RECONSTRUCTION_FINANCING`
  - `CLIMATE_EVENT_TO_GRID_INFRA`
- Added Round 90 calibration pack:
  - `src/e2r/sector/round90_r11_loop4_policy_geopolitical_event.py`
  - `src/e2r/cli/build_round90_r11_loop4_report.py`
  - `tests/test_round90_r11_loop4_policy_geopolitical_event.py`
- Generated calibration outputs:
  - `data/e2r_case_library/cases_r11_loop4_round90.jsonl`
  - `data/sector_taxonomy/score_weight_profiles_round90_r11_loop4_v4.csv`
  - `output/e2r_round90_r11_loop4_policy_geopolitical_event/`

## Summary

- target_count: 15
- case_candidate_count: 13
- success_candidate_count: 4
- event_premium_count: 4
- stage4b_case_count: 2
- stage4c_case_count: 4
- watch_yellow_first_count: 6
- redteam_first_count: 9
- gate_only_target_count: 2

## Key Calibration Split

- `GEOPOLITICAL_RECONSTRUCTION` is still mostly Watch. Example: a reconstruction conference or MOU can route research, but it is not enough for Green.
- `REAL_RECONSTRUCTION_FINANCING` is stronger. Example: EBRD/IFC financing plus operating company and infrastructure asset is better evidence, but company-level contract, revenue, and margin still need validation.
- `CLIMATE_DISASTER_EVENT` captures heatwave, cooling, air-quality, and disaster routing.
- `CLIMATE_EVENT_TO_GRID_INFRA` captures the stronger path where the event turns into VPP, ESS, grid response, cooling infrastructure, or repeat program evidence.

## Guardrails

- News is not Green evidence by itself.
- Stage 3-Green was not loosened.
- Do not invent contracts, budgets, financing, dose amounts, guidance, stage prices, or revenue.
- North Korea policy themes remain Red-biased until sanctions relief and cash-flow projects exist.
- Speculative science themes remain Red-biased until independent replication, commercial products, customer contracts, and revenue exist.
- One-off disease, pest, disaster, and weather events must be checked for demand normalization.

## Verification

- `PYTHONPATH=src python -m unittest tests.test_round90_r11_loop4_policy_geopolitical_event -v`
- `PYTHONPATH=src python -m e2r.cli.build_round90_r11_loop4_report`

Full test-suite status is recorded in the final commit notes for this round.
