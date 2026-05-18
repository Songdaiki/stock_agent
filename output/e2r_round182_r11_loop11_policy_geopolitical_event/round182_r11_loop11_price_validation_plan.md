# Round-182 R11 Loop-11 Price Validation Plan

R11 needs event-date price-path validation because policy, exploration, short-selling, political, and energy shocks move prices before fundamentals confirm.

## Required Fields

- `ticker`
- `company_name`
- `event_type`
- `event_date`
- `event_headline`
- `event_source`
- `stage1_date`
- `stage2_date`
- `stage3_date`
- `stage4b_date`
- `stage4c_date`
- `stage1_trigger`
- `stage2_trigger`
- `stage3_trigger`
- `stage4b_trigger`
- `stage4c_trigger`
- `price_at_event`
- `price_at_stage1`
- `price_at_stage2`
- `price_at_stage3`
- `price_at_stage4b`
- `price_at_stage4c`
- `return_1d_after_event`
- `return_5d_after_event`
- `return_20d_after_event`
- `return_60d_after_event`
- `return_120d_after_event`
- `mfe_5d_after_event`
- `mae_5d_after_event`
- `mfe_20d_after_event`
- `mae_20d_after_event`
- `mfe_60d_after_event`
- `mae_60d_after_event`
- `mfe_120d_after_event`
- `mae_120d_after_event`
- `relative_strength_vs_kospi`
- `relative_strength_vs_sector`
- `market_wide_shock_flag`
- `daily_limit_flag`
- `volume_spike_flag`
- `contract_or_budget_confirmed`
- `government_order_flag`
- `exploration_result_flag`
- `commerciality_confirmed_flag`
- `guidance_raised_flag`
- `op_revision_after_event`
- `eps_revision_after_event`
- `policy_reversal_risk`
- `drill_bit_gate`
- `resource_success_probability`
- `funding_withdrawal_flag`
- `market_structure_event_flag`
- `short_selling_resumption_flag`
- `political_risk_flag`
- `geopolitical_energy_shock_flag`
- `disclosure_confidence`
- `valuation_at_stage2`
- `valuation_at_stage4b`

## Case Backfill Priorities

- `korea_east_sea_gas_discovery_stage1_4b_watch_case`: event date returns, daily-limit flags, commerciality result, and OP/EPS linkage.
- `short_selling_ban_extension_policy_overlay_case`: short-selling policy dates, trading value, brokerage ROE, and resumption impact.
- `political_system_shock_martial_law_case`: KOSPI/KOSDAQ, won, foreign flow, and valuation-room impact.
- `hormuz_middle_east_energy_import_shock_case`: oil, FX, sector MAE, exporter risk-off, and cost-sensitive sector hit.
- `brokerage_short_selling_fines_market_trust_case`: enforcement dates, brokerage earnings link, trading value, IB/WM, PF risk, and ROE.
