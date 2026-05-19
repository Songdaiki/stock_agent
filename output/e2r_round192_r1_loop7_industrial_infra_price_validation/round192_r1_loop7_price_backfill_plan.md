# Round-192 R1 Loop-7 Price Backfill Plan

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
- `relative_strength_vs_defense_basket`
- `relative_strength_vs_shipbuilding_basket`
- `relative_strength_vs_power_equipment_basket`
- `contract_amount_to_prior_sales`
- `contract_duration_months`
- `backlog_to_sales`
- `delivery_schedule`
- `government_financing_flag`
- `local_production_flag`
- `op_eps_revision`
- `margin_visibility`
- `capital_raise_flag`
- `sanction_watch_flag`
- `ipo_first_day_return`
- `disclosure_confidence`
- `stage4b_status`
- `hard_4c_confirmed`

## Priority Cases

| case | stage marker | current status | price anchor |
| --- | --- | --- | --- |
| `hyundai_rotem_k2_export_price_path` | 2024-04-09 | needs_ohlc_backfill | 41300 |
| `lig_nex1_msami_iraq_combat_validation` | 2024-09-20 | needs_ohlc_backfill | none |
| `hanwha_aerospace_poland_chunmoo_4b_timing` | 2024-04-25 | needs_ohlc_backfill | 217000 |
| `samsung_heavy_shipbuilding_contract_stage2_not_green` | 2024-07-01 | needs_ohlc_backfill | none |
| `hd_hyundai_marine_solution_ipo_price_only_rally` | 2024-05-08 | needs_ohlc_backfill | 163900 |
| `kai_fa50_philippines_stage2_watch` | 2025-06-04 | needs_ohlc_backfill | none |
| `hanwha_ocean_sanction_watch_not_hard_4c` | undated | needs_ohlc_backfill | none |

## Backfill Rule

- Use official OHLC data for exact MFE/MAE.
- Keep unknown values null or `needs_ohlc_backfill`.
- A price anchor from an article is a hint, not a substitute for official OHLC.
