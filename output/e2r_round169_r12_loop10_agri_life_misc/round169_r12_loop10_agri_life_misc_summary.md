# Round-169 R12 Loop-10 Agriculture / Life Services / Misc Summary

- source_round: `docs/round/round_169.md`
- large_sector: `EDUCATION_LIFE_AGRI_MISC`
- target_count: 30
- source_canonical_target_count: 30
- base_score_axis_count: 7
- stage_cap_count: 4
- case_candidate_count: 24
- success_candidate_count: 5
- cyclical_success_count: 2
- event_premium_count: 2
- failed_rerating_count: 5
- stage4b_case_count: 3
- stage4c_case_count: 10
- green_possible_count: 0
- watch_yellow_first_count: 17
- redteam_first_count: 13
- gate_only_target_count: 9
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## Interpretation

- R12 Loop-10 separates recurring FCF from disease, weather, policy, AI, hardware, and regulation headlines.
- Example: smart farming news is Stage 1 until actual orders, unit economics, energy cost, and FCF are visible.
- Example: education apps need bookings, paid conversion, CAC, and monetization, not user growth alone.
- Example: rental appliances can improve quality only if recurring care revenue and churn data beat the hardware cycle.
- Example: a right-to-repair lawsuit can turn software lock-in from a positive story into a RedTeam gate.
- Example: partial cannabis rescheduling is not full legalization until license scope, channels, and tax effects are verified.

## R12 v10 Base Score Axes

- `eps_fcf_opm_conversion`: 22
- `recurring_contract_revenue_regulatory_visibility`: 20
- `unit_economics_price_pass_through_demand_durability`: 18
- `regulation_litigation_public_health_disclosure`: 16
- `capital_discipline_debt_cash_runway`: 10
- `market_mispricing_rerating_gap`: 8
- `valuation_room_4b_margin`: 6

## R12 v10 Stage Caps

- `stage1_theme_event_cap`: Stage 1 / 45
- `stage2_repeat_revenue_unit_economics_cap`: Stage 2 / 70
- `stage3_recurring_fcf_gate`: Stage 3 / requires_score_above_70_and_recurring_fcf
- `stage4b_4c_misc_theme_unwind_gate`: 4B/4C / watch_or_break

These axes are calibration material only. Example: `recurring_contract_revenue_regulatory_visibility` can lift Bayer, Zoetis, or Juul to Stage 2, but Stage 3 still needs repeat revenue, verified regulatory scope, and FCF.
