# Round-203 R12 Loop-7 Price Backfill Plan

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
- `relative_strength_vs_rental_service_basket`
- `relative_strength_vs_agri_machinery_basket`
- `relative_strength_vs_education_policy_basket`
- `relative_strength_vs_poultry_basket`
- `relative_strength_vs_regulated_consumer_basket`
- `relative_strength_vs_smart_farm_basket`
- `event_volume_spike`
- `event_turnover_spike`
- `recurring_account_count`
- `churn_rate`
- `arpu`
- `repeat_course_revenue`
- `commercial_installation_count`
- `service_contract_revenue`
- `dealer_sell_through`
- `dealer_inventory`
- `farmer_financing_terms`
- `feed_cost`
- `import_restriction_status`
- `policy_reversal_flag`
- `regulatory_pass`
- `unit_economics_metric`
- `cash_conversion`
- `hard_4c_confirmed`

## Priority Cases

| case | stage marker | current status | 4B status | hard 4C |
| --- | --- | --- | --- | --- |
| `coway_rental_recurring_service_candidate` | undated | needs_ohlc_backfill | `watch` | false |
| `daedong_tym_agri_machinery_export_watch` | undated | needs_ohlc_backfill | `watch` | false |
| `megastudy_medical_quota_policy_event_watch` | 2025-03-07 | needs_ohlc_backfill | `watch` | false |
| `education_edtech_phone_ban_policy_watch` | 2025-08-27 | needs_ohlc_backfill | `watch` | false |
| `poultry_basket_brazil_bird_flu_import_ban_event_fade_r12` | 2025-05-19 | needs_ohlc_backfill | `watch` | false |
| `ktng_regulated_consumer_cashflow_watch` | undated | needs_ohlc_backfill | `watch` | false |
| `smart_farm_basket_unit_economics_insufficient` | undated | needs_ohlc_backfill | `watch` | false |

## Backfill Rule

- Use official OHLC data for exact MFE/MAE.
- Event cases need short windows: 5D, 20D, and 60D matter because policy or disease fade can be fast.
- Recurring-service cases need longer windows: 180D, 1Y, and 2Y matter because evidence compounds slowly.
- Keep unknown values null or `needs_ohlc_backfill`.
- Split policy/event date, evidence date, reversal date, and thesis-break date.
- Do not create a Stage 3 anchor when the case intentionally has no Stage 3 date.
