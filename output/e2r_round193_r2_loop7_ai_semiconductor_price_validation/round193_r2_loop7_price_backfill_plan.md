# Round-193 R2 Loop-7 Price Backfill Plan

## Required Fields

- `stage1_date`
- `stage2_date`
- `stage3_date`
- `stage4b_date`
- `stage4c_date`
- `stage1_price`
- `stage2_price`
- `stage3_price`
- `stage4b_price`
- `stage4c_price`
- `peak_date`
- `peak_price`
- `MFE_20D`
- `MFE_60D`
- `MFE_90D`
- `MFE_120D`
- `MFE_180D`
- `MFE_252D`
- `MFE_1Y`
- `MFE_2Y`
- `MAE_20D`
- `MAE_60D`
- `MAE_90D`
- `MAE_120D`
- `MAE_180D`
- `MAE_252D`
- `MAE_1Y`
- `MAE_2Y`
- `relative_strength_vs_kospi`
- `relative_strength_vs_hbm_basket`
- `relative_strength_vs_semiconductor_equipment_basket`
- `relative_strength_vs_ai_server_pcb_basket`
- `customer_visibility`
- `customer_diversification_confirmed`
- `customer_name_confirmed`
- `order_amount`
- `contract_or_purchase_order_flag`
- `shipment_or_volume_ramp_flag`
- `design_win_flag`
- `tapeout_flag`
- `volume_production_flag`
- `revenue_recognition_flag`
- `gross_margin_visibility`
- `opm_visibility`
- `eps_revision`
- `fcf_revision`
- `hbm_capacity_bottleneck`
- `hbm_lta_flag`
- `prepayment_flag`
- `advanced_packaging_direct_link`
- `policy_foundry_flag`
- `media_report_without_confirmation_flag`
- `stock_price_rally_before_evidence_flag`
- `labor_disruption_flag`
- `production_disruption_flag`
- `accounting_trust_flag`
- `circular_financing_flag`
- `stage4b_status`
- `hard_4c_confirmed`

## Priority Cases

| case | stage marker | current status | price anchor |
| --- | --- | --- | --- |
| `hanmi_semiconductor_tsv_tc_bonder_4b_watch` | 2024-03-26 | needs_ohlc_backfill | 139100 |
| `gaonchips_pfn_samsung_2nm_design_win_stage2` | 2024-07-09 | needs_ohlc_backfill | none |
| `samsung_electronics_hbm_catchup_failed_2025_watch` | 2025-04-30 | needs_ohlc_backfill | none |
| `db_hitek_policy_foundry_event_premium` | 2025-12-10 | needs_ohlc_backfill | none |
| `isu_petasis_ai_server_pcb_insufficient_evidence` | undated | needs_ohlc_backfill | none |
| `sk_hynix_hbm_2026_4b_benchmark` | 2026-05-14 | needs_ohlc_backfill | none |

## Backfill Rule

- Use official OHLC data for exact MFE/MAE.
- Keep unknown values null or `needs_ohlc_backfill`.
- Article intraday anchors are hints, not substitutes for official OHLC.
