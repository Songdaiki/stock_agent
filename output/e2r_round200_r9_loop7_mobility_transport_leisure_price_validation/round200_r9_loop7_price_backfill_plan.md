# Round-200 R9 Loop-7 Price Backfill Plan

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
- `MFE_5D`
- `MFE_20D`
- `MFE_30D`
- `MFE_60D`
- `MFE_90D`
- `MFE_180D`
- `MFE_1Y`
- `MFE_2Y`
- `MAE_5D`
- `MAE_20D`
- `MAE_30D`
- `MAE_60D`
- `MAE_90D`
- `MAE_180D`
- `MAE_1Y`
- `MAE_2Y`
- `drawdown_after_peak`
- `relative_strength_vs_kospi`
- `relative_strength_vs_auto_basket`
- `relative_strength_vs_airline_basket`
- `relative_strength_vs_shipping_basket`
- `relative_strength_vs_tourism_basket`
- `hybrid_mix`
- `fcf_after_capex`
- `shareholder_return_execution`
- `operating_margin`
- `localization_ratio`
- `tariff_cost`
- `margin_guidance_cut_flag`
- `unit_economics`
- `load_factor`
- `yield`
- `integration_synergy`
- `fleet_utilization`
- `freight_rate`
- `tourist_spend`
- `casino_drop`
- `casino_hold_rate`
- `safety_incident_flag`
- `hard_4c_confirmed`

## Priority Cases

| case | stage marker | current status | 4B status | hard 4C |
| --- | --- | --- | --- | --- |
| `hyundai_motor_hybrid_valueup_tariff_4c_watch` | 2024-08-28 | needs_ohlc_backfill | `watch` | false |
| `kia_hybrid_valueup_sdv_delay_capex_watch` | 2026-04-09 | needs_ohlc_backfill | `watch` | false |
| `korean_air_asiana_integration_scale_stage2_watch` | 2024-12-12 | needs_ohlc_backfill | `watch` | false |
| `jeju_air_fatal_crash_operational_trust_4c_break` | 2024-12-30 | needs_ohlc_backfill | `none` | true |
| `hmm_red_sea_freight_cycle_stage2_4b_watch` | 2025-11-06 | needs_ohlc_backfill | `watch` | false |
| `hotel_shilla_china_visa_tourism_event_stage2_watch` | 2025-09-29 | needs_ohlc_backfill | `watch` | false |
| `lotte_tour_dream_tower_casino_utilization_gap_watch` | 2025-09-29 | needs_ohlc_backfill | `watch` | false |

## Backfill Rule

- Use official OHLC data for exact MFE/MAE.
- Keep unknown values null or `needs_ohlc_backfill`.
- Split hybrid/value-up, tariff shock, SDV delay, merger, fatal safety, freight, and tourism policy dates.
- Do not create a Stage 3 anchor when the case intentionally has no Stage 3 date.
