# Checkpoint 28A Round 91 R12 Loop 4 Agriculture / Life Services / Misc

## Scope

- source round: `docs/round/round_91.md`
- large sector: `EDUCATION_LIFE_AGRI_MISC`
- purpose: agriculture, life-services, education, rental, kiosk, and regulated-consumer themes are separated by repeat revenue, unit economics, pass-through, regulatory scope, CAC, churn, and FCF evidence.
- production scoring changed: false
- case records used as candidate-generation input: false

## What Changed

- Added two canonical archetypes:
  - `AGRI_INPUT_SEED_CROP_PROTECTION`
  - `FERTILIZER_INPUT_COST_CYCLE`
- Reused existing `HOME_APPLIANCE_HARDWARE_CYCLE` as a separate R12 Loop 4 target instead of folding Whirlpool-style hardware failure into rental appliances.
- Added Round 91 calibration pack:
  - `src/e2r/sector/round91_r12_loop4_agri_life_misc.py`
  - `src/e2r/cli/build_round91_r12_loop4_report.py`
  - `tests/test_round91_r12_loop4_agri_life_misc.py`
- Generated calibration outputs:
  - `data/e2r_case_library/cases_r12_loop4_round91.jsonl`
  - `data/sector_taxonomy/score_weight_profiles_round91_r12_loop4_v4.csv`
  - `output/e2r_round91_r12_loop4_agri_life_misc/`

## Summary

- target_count: 21
- case_candidate_count: 19
- success_candidate_count: 5
- cyclical_success_count: 2
- event_premium_count: 2
- failed_rerating_count: 3
- stage4b_case_count: 3
- stage4c_case_count: 7
- green_possible_count: 0
- watch_yellow_first_count: 14
- redteam_first_count: 7
- gate_only_target_count: 3

## Key Calibration Split

- `SMART_FARM_AGRI_TECH` is not the same as `VERTICAL_FARMING_UNIT_ECONOMICS`.
  - Example: a smart-farm operating contract can be useful evidence.
  - Counterexample: a vertical farm with high energy cost and no premium pricing can become hard 4C.
- `AGRI_INPUT_SEED_CROP_PROTECTION` is not the same as fertilizer or livestock.
  - Example: seed licensing can lift EBITDA.
  - Guardrail: Roundup-style litigation, patent expiry, regulation, and farmer ROI still matter.
- `FERTILIZER_INPUT_COST_CYCLE` remains mostly Watch/cyclical.
  - Example: potash demand can be strong.
  - Guardrail: crop prices, farmer margin, input cost, and supply disruption can reverse the thesis.
- `HOME_LIVING_APPLIANCE_RENTAL` is separated from `HOME_APPLIANCE_HARDWARE_CYCLE`.
  - Example: recurring filter/care revenue is higher quality than one-time appliance replacement demand.

## Guardrails

- Do not treat essential demand, policy support, weather, disease, education users, rental accounts, or FDA/DEA headlines as Green evidence by itself.
- Do not invent unit economics, government orders, completion rates, CAC, churn, regulatory scope, software attach rate, or price-path fields.
- Stage 3-Green was not loosened.
- Chapter 11, AI substitution, bookings misses, dividend suspension, retailer retreat, theft/shrink, public-health reversal, commodity normalization, and right-to-repair risk remain RedTeam evidence.

## Verification

- `PYTHONPATH=src python -m unittest tests.test_round91_r12_loop4_agri_life_misc -v`
- `PYTHONPATH=src python -m e2r.cli.build_round91_r12_loop4_report`

Full test-suite status is recorded in the final commit notes for this round.
