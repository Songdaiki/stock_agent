# Round-183 R12 Loop-11 Price Validation Plan

R12 needs both event-date price-path validation and operating unit-economics backfill because event themes and repeat-revenue candidates are mixed.

## Required Fields

- `ticker`
- `company_name`
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
- `price_at_stage1`
- `price_at_stage2`
- `price_at_stage3`
- `price_at_stage4b`
- `price_at_stage4c`
- `return_1d_after_event`
- `return_5d_after_event`
- `return_20d_after_stage2`
- `return_60d_after_stage2`
- `return_120d_after_stage2`
- `return_252d_after_stage2`
- `mfe_60d_after_stage2`
- `mae_60d_after_stage2`
- `mfe_120d_after_stage2`
- `mae_120d_after_stage2`
- `mfe_252d_after_stage2`
- `mae_252d_after_stage2`
- `relative_strength_vs_kospi`
- `relative_strength_vs_kosdaq`
- `relative_strength_vs_agri_basket`
- `relative_strength_vs_education_basket`
- `relative_strength_vs_consumer_regulated_basket`
- `op_revision_before_stage3`
- `op_revision_after_stage3`
- `eps_revision_before_stage3`
- `eps_revision_after_stage3`
- `recurring_revenue_ratio`
- `subscription_or_repeat_revenue`
- `order_backlog`
- `contract_amount`
- `contract_counterparty`
- `contract_period`
- `export_sales_ratio`
- `dealer_inventory_signal`
- `farm_income_signal`
- `grain_price_signal`
- `feed_cost_signal`
- `livestock_price_signal`
- `price_pass_through_signal`
- `regulatory_approval_status`
- `public_health_risk_flag`
- `youth_safety_flag`
- `legal_settlement_flag`
- `antitrust_or_collusion_flag`
- `policy_event_type`
- `policy_reversal_risk`
- `medical_quota_policy_status`
- `student_count_trend`
- `cac`
- `churn`
- `paid_conversion`
- `ip_revenue`
- `licensing_revenue`
- `merchandise_revenue`
- `one_hit_dependency`
- `post_ipo_guidance`
- `inventory_days`
- `receivables_days`
- `cash_runway_months`
- `dilution_event_flag`
- `disclosure_confidence`
- `valuation_at_stage3`
- `valuation_at_stage4b`

## Case Backfill Priorities

- `pinkfong_ipo_stage2_4b_watch_case`: IPO listing date, max/close return, multi-IP revenue, OPM, FCF, and post-IPO guidance.
- `ktng_lil_heated_tobacco_distribution_case`: overseas NGP revenue, OPM/FCF, shareholder return, public-health scope, and price path.
- `daedong_tym_agri_machinery_export_stage2_candidate_case`: KRX OHLCV, export sales, dealer inventory, farm-income, financing cost, and OP revision.
- `megastudy_medical_quota_policy_event_case`: policy dates, enrollment, paid conversion, CAC, OPM, and AI tutor substitution risk.
- `dongwon_starkist_settlement_legal_4c_watch_case`: settlement reserves, brand OPM, fuel/FX, and sector price MAE.
