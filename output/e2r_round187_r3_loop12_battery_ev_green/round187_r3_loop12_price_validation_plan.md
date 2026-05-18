# Round-187 R3 Loop-12 Price Validation Plan

R3 Loop 12 must backfill contract, cancellation, subsidy-quality, utilization, safety, and policy fields together.

## Required Fields

- `ticker`
- `company_name`
- `canonical_archetype`
- `case_type`
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
- `mfe_20d_after_stage2`
- `mae_20d_after_stage2`
- `mfe_60d_after_stage2`
- `mae_60d_after_stage2`
- `mfe_120d_after_stage2`
- `mae_120d_after_stage2`
- `mfe_252d_after_stage2`
- `mae_252d_after_stage2`
- `relative_strength_vs_kospi`
- `relative_strength_vs_kosdaq`
- `relative_strength_vs_battery_basket`
- `relative_strength_vs_renewable_basket`
- `relative_strength_vs_hydrogen_basket`
- `contract_amount`
- `contract_counterparty`
- `contract_period`
- `gwh_mw_or_tonnage`
- `production_start_date`
- `revenue_recognition_timing`
- `customer_name_disclosed`
- `customer_strategy_risk`
- `utilization_rate`
- `line_conversion_flag`
- `ess_revenue_signal`
- `ev_revenue_signal`
- `subsidy_amount`
- `profit_ex_subsidy`
- `ira_ampc_dependency`
- `op_revision_before_stage3`
- `op_revision_after_stage3`
- `eps_revision_before_stage3`
- `eps_revision_after_stage3`
- `opm`
- `fcf_signal`
- `contract_cancellation_flag`
- `factory_idle_or_sale_review_flag`
- `customs_detention_flag`
- `uflpa_risk_flag`
- `wind_permit_halt_flag`
- `battery_fire_flag`
- `fatal_accident_flag`
- `supplier_disclosure_issue_flag`
- `inventory_loss_flag`
- `raw_material_price_exposure`
- `safety_or_quality_issue`
- `dilution_event_flag`
- `disclosure_confidence`
- `valuation_at_stage3`
- `valuation_at_stage4b`

## Backfill Priorities

- `lges_ess_pivot_tax_credit_stage2_case`: profit_ex_subsidy, utilization, ESS revenue, FCF, and price path.
- `lges_ford_freudenberg_contract_cancellation_4c_case`: cancellation dates, expected revenue loss, MAE, and utilization impact.
- `doosan_fuelcell_ceres_sofc_stage23_candidate_case`: sales, customer, recurring service, OPM, FCF, and 60D/120D MFE.
- `qcells_us_localization_stage2_case`: customs clearance, normal operation, margin, FCF, and localization price path.
- `aricell_battery_safety_fire_hard_4c_case`: safety resolution, regulatory clearance, and trust recovery.
