# Round-145 R13 Loop-8 Cross-Archetype RedTeam / 4B / Price Validation

- source_round: `docs/round/round_145.md`
- large_sector: `CROSS_ARCHETYPE_REDTEAM_4B_PRICE_VALIDATION`
- target_count: 21
- overlay_axis_count: 7
- stage_cap_count: 4
- case_candidate_count: 43
- structural_success_count: 3
- success_candidate_count: 11
- cyclical_success_count: 1
- event_premium_count: 1
- overheat_count: 1
- failed_rerating_count: 8
- stage4b_case_count: 8
- stage4c_case_count: 12
- hard_gate_target_count: 10
- green_possible_count: 1
- watch_yellow_first_count: 6
- redteam_first_count: 14
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## Interpretation

- Round 145 is a common validation overlay, not a sector score-owner.
- High score is not enough. Stage 3-Green needs cross-evidence, EPS/FCF durability, price-path alignment, no hard RedTeam, and no saturated 4B.
- Example: SK하이닉스 HBM can be structurally aligned and also require 4B-watch because the new frame is already crowded.
- Example: Supermicro-style auditor resignation blocks Green even if prior AI-server revenue was strong.
- Example: data-center real assets require AFFO-per-share, capex, tenant, funding-cost, and power/water checks before structural confidence.
- Example: AI cloud contracts are capped if supplier, investor, customer, and capacity-guarantee economics form a circular financing loop.
- Example: OpenDART list-only contract headlines are capped until amount, customer/use, and duration or margin detail is verified.
- Example: a policy/MOU event stays Event Premium until funded contract, order, budget, or earnings evidence appears.

## R13 v8 Cross-Archetype Overlay Axes

- `eps_fcf_roe_affo_opm_bodyweight_change`: 24
- `evidence_visibility`: 20
- `durability_repeatability`: 16
- `disclosure_confidence_redteam`: 12
- `capital_discipline_leverage_fcf`: 10
- `market_mispricing_rerating_gap`: 10
- `valuation_room_4b_margin`: 8

## R13 v8 Stage Caps

- `stage1_theme_headline_cap`: Stage 1 / 45
- `stage2_verified_evidence_cap`: Stage 2 / 70
- `stage3_green_all_checks_gate`: Stage 3 / requires_all_green_checks
- `stage4b_4c_final_redteam_gate`: 4B/4C / watch_or_break

Stage 3-Green remains blocked unless sector score, EPS/FCF bodyweight change, repeatability, price-path alignment, disclosure confidence, 4B valuation room, and no hard 4C flag all line up.
