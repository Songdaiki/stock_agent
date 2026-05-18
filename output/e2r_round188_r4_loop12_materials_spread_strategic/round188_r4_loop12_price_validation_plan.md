# Round-188 R4 Loop-12 Price Validation Plan

R4 Loop 12 must backfill spread, ex-inventory OP, restructuring execution, tariff, production disruption, and price-path fields together.

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
- `relative_strength_vs_chemical_basket`
- `relative_strength_vs_refining_basket`
- `relative_strength_vs_materials_basket`
- `refining_margin`
- `petrochemical_spread`
- `rubber_spread`
- `raw_material_cost_signal`
- `inventory_gain_loss_signal`
- `op_ex_inventory_effect`
- `op_revision_before_stage3`
- `op_revision_after_stage3`
- `eps_revision_before_stage3`
- `eps_revision_after_stage3`
- `fcf_signal`
- `opm`
- `capacity_cut_amount`
- `plant_shutdown_flag`
- `shutdown_duration`
- `merger_or_consolidation_flag`
- `government_support_amount`
- `tax_or_utility_support`
- `asset_sale_amount`
- `debt_reduction_use`
- `new_capacity_addition`
- `china_oversupply_flag`
- `tariff_or_antidumping_flag`
- `export_exposure`
- `production_disruption_flag`
- `factory_fire_flag`
- `capex_burden_flag`
- `media_report_only_flag`
- `plan_detail_disclosed_flag`
- `disclosure_confidence`
- `valuation_at_stage3`
- `valuation_at_stage4b`

## Backfill Priorities

- `sk_innovation_refining_spread_turnaround_case`: refining margin, op_ex_inventory_effect, FCF, battery/petrochem drag, 60D/120D MFE.
- `lotte_hd_hyundai_ncc_capacity_cut_stage2_case`: capacity_cut_amount, shutdown_duration, spread, utilization, OP, FCF.
- `lg_chem_nav_governance_restructuring_stage2_case`: asset sale, debt reduction, buyback/cancel execution, NAV discount, FCF.
- `soil_shaheen_oversupply_4c_watch_case`: new capacity, capex burden, spread dilution, operating loss, relative price reaction.
- `kumho_tire_gwangju_fire_hard_4c_case`: factory fire date, capacity loss, revenue guidance, customer supply, event return.
