# Round-180 R9 Loop-11 Price Validation Plan

R9 needs event-date price-path validation because policy, safety, freight, and hybrid events can move prices before fundamentals confirm.

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
- `relative_strength_vs_transport_basket`
- `relative_strength_vs_auto_basket`
- `relative_strength_vs_tourism_basket`
- `relative_strength_vs_shipping_basket`
- `op_revision_before_stage3`
- `op_revision_after_stage3`
- `eps_revision_before_stage3`
- `eps_revision_after_stage3`
- `vehicle_sales_volume`
- `hybrid_mix`
- `us_localization_ratio`
- `tariff_cost`
- `price_cut_signal`
- `sdv_delay_flag`
- `capex_hike_flag`
- `parcel_volume`
- `parcel_unit_price`
- `delivery_cost_per_unit`
- `automation_capex`
- `labor_regulation_flag`
- `visitor_arrivals`
- `average_spend`
- `duty_free_sales`
- `casino_drop_amount`
- `casino_hold_rate`
- `hotel_revpar`
- `freight_rate_index`
- `teu_or_bulk_volume`
- `vessel_supply_growth`
- `red_sea_route_normalization_flag`
- `safety_accident_flag`
- `recall_flag`
- `quality_cost_flag`
- `insurance_compensation_flag`
- `disclosure_confidence`
- `valuation_at_stage3`
- `valuation_at_stage4b`

## Case Backfill Priorities

- `kia_hybrid_localization_sdv_delay_stage2_4c_watch_case`: hybrid mix, tariff cost, OPM, FCF, and SDV event price reaction.
- `cj_logistics_shinsegae_oneday_volume_stage2_3_case`: parcel volume, unit price, delivery cost per unit, automation payback, OPM, and FCF.
- `tourism_visa_free_dutyfree_casino_policy_event_case`: visitor arrivals, average spend, duty-free sales, casino drop, hold rate, RevPAR, and OPM.
- `jeju_air_muan_crash_hard_4c_case`: accident date price reaction, cancellations, safety inspection, and insurance/compensation impacts.
- `hmm_pan_ocean_freight_cycle_4b_4c_watch_case`: freight index, TEU/bulk volume, vessel supply, Red Sea route normalization, EBITDA, and price-path MFE/MAE.
