# Round-186 R2 Loop-12 Price Validation Plan

R2 Loop 12 must backfill contract/order fields, shipment/yield fields, price-path fields, and IP/labor/disclosure fields together.

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
- `relative_strength_vs_semiconductor_basket`
- `relative_strength_vs_ai_hardware_basket`
- `relative_strength_vs_hbm_equipment_basket`
- `contract_amount`
- `contract_counterparty`
- `contract_period`
- `order_size`
- `customer_name`
- `design_win_flag`
- `tapeout_flag`
- `mass_production_flag`
- `shipment_schedule`
- `revenue_recognition_timing`
- `op_revision_before_stage3`
- `op_revision_after_stage3`
- `eps_revision_before_stage3`
- `eps_revision_after_stage3`
- `opm`
- `fcf_signal`
- `inventory_signal`
- `asp_signal`
- `yield_signal`
- `customer_qualification_status`
- `customer_diversification_flag`
- `capex_linked_customer`
- `customer_capex_delay_flag`
- `ip_leak_risk_flag`
- `labor_disruption_flag`
- `production_disruption_flag`
- `media_report_only_flag`
- `mou_loi_flag`
- `non_binding_flag`
- `cb_bw_or_dilution_flag`
- `disclosure_confidence`
- `valuation_at_stage3`
- `valuation_at_stage4b`

## Backfill Priorities

- `skc_absolics_glass_substrate_stage2_case`: customer, yield, shipment, revenue, OPM, and glass-basket price path.
- `gaonchips_pfn_samsung_2nm_stage2_case`: order size, tape-out, revenue recognition, repeat design win, and OP/EPS.
- `hbm_test_equipment_basket_stage3_candidate_case`: individual order, shipment schedule, OP/EPS, repeat order, MFE/MAE, and relative strength.
- `ai_server_pcb_mlcc_second_wave_stage3_candidate_case`: ASP, inventory normalization, OPM, customer diversification, and price path.
- `samsung_supply_chain_labor_disruption_4c_case` and `korea_memory_ip_leak_cxmt_4c_case`: resolution status and valuation-room impact.
