# Round-170 R11 Loop-10 Policy / Geopolitical / Disaster / Event Summary

- source_round: `docs/round/round_170.md`
- large_sector: `POLICY_GEOPOLITICAL_EVENT`
- target_count: 24
- source_canonical_target_count: 24
- case_candidate_count: 19
- success_candidate_count: 7
- event_premium_count: 5
- stage4b_case_count: 4
- stage4c_case_count: 5
- stage4c_watch_count: 1
- watch_yellow_first_count: 12
- redteam_first_count: 12
- gate_only_target_count: 4
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## Interpretation

- R11 Loop-10 is mostly a false-positive defense pack.
- Example: a big outbreak headline can create Stage 1 routing. Without `government_order`, `stockpile_contract`, or `guide_up`, it stays event premium.
- Example: Ukraine reconstruction becomes stronger only when financing, participating companies, construction start, and revenue/margin evidence are visible.
- Example: rare-earth export controls can prove a macro bottleneck, but a company still needs capacity, offtake, price floor, revenue, and FCF evidence.
- Example: visa-free tourism policy is Stage 1 routing until arrivals, spend, casino drop, duty-free sales, RevPAR, and OPM are source-backed.
- Example: LK-99 style preprints are not revenue evidence; replication failure or impurity explanation is a hard 4C-style counterexample.

## R11 v10 Base Score Axes

These axes are calibration material only. They document how Round 170 separates policy/event headlines from actual orders, budgets, financing, guidance, recurrence, and RedTeam detail checks.
- actual_contract_budget_order_financing_visibility: 28
- eps_fcf_revenue_guidance_conversion: 20
- recurrence_durability: 14
- bottleneck_policy_intensity_geopolitical_reality: 12
- redteam_disclosure_confidence: 12
- market_mispricing_rerating_gap: 8
- valuation_room_4b_margin: 6

## R11 v10 Stage Caps

These caps are calibration material only. They document how event headlines, committed money, recurring cash flow, and event unwind should be separated before any future shadow scoring change.
- stage1_event_headline_cap: Stage 1 / 40
- stage2_money_committed_cap: Stage 2 / 70
- stage3_repeat_cashflow_gate: Stage 3 / requires_score_above_70_and_repeat_cashflow
- stage4b_4c_event_unwind_gate: 4B/4C / watch_or_break
