# Round-38 Score-Weight Validation v2.3 Summary

- source_round: `docs/round/round_38.md`
- target_count: 8
- case_candidate_count: 28
- success_candidate_count: 9
- counterexample_or_risk_count: 19
- stage4b_case_count: 2
- stage4c_case_count: 8
- green_possible_count: 4
- watch_yellow_first_count: 2
- redteam_first_count: 2
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## Interpretation
- Round 38 adds cases_v20 and v2.3 price-path validation plans.
- Example: AI server ODM/EMS can be Green-possible, but low margin, inventory, customer concentration, and audit risk cap it.
- Example: neocloud has take-or-pay visibility, but high debt and GPU depreciation keep it watch-first.
- Example: Supermicro-style auditor resignation is a hard RedTeam 4C gate, not a score-weight adjustment.
- Theme names, case IDs, revenue growth headlines, and price spikes are not score evidence by themselves.
