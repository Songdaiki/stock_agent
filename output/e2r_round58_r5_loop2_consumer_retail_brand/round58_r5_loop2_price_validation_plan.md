# Round-58 R5 Loop-2 Price Validation Plan

## Method

1. Assign stage dates from source evidence only.
2. Store stage-date close prices from official price data.
3. Calculate MFE_30D / 90D / 180D / 1Y / 2Y.
4. Calculate MAE_30D / 90D / 180D / 1Y.
5. Compare export, sell-through, reorder, OPM, EPS revision, inventory, receivables, churn, regulation, and price path.
6. Mark food recall, tariff, data breach, supplier regulation, hardware cycle, and IP litigation explicitly.

## Priority Case Checks

| case_id | target | stage marker | check |
| --- | --- | --- | --- |
| `samyang_buldak_export_rerating_case` | `EXPORT_RECURRING_CONSUMER` | 2024-06-14 | needs_price_backfill |
| `samyang_buldak_denmark_recall_case` | `FOOD_SAFETY_RECALL_OVERLAY` | 2024-06-12 | needs_price_backfill |
| `kbeauty_us_export_overtake_france_case` | `K_BEAUTY_EXPORT_DISTRIBUTION` | 2025-06-05 | missing_direct_symbol_mapping |
| `kbeauty_tariff_risk_case` | `K_BEAUTY_EXPORT_DISTRIBUTION` | undated | needs_source_date_and_price_backfill |
| `apr_medicube_beauty_device_case` | `K_BEAUTY_EXPORT_DISTRIBUTION` | 2025-10-20 | needs_price_backfill |
| `medicube_ulta_tiktok_omnichannel_case` | `K_BEAUTY_EXPORT_DISTRIBUTION` | 2026-02-13 | missing_direct_symbol_mapping |
| `coupang_supplier_regulation_case` | `DATA_SECURITY_SUPPLIER_REGULATION_OVERLAY` | 2026-02-26 | needs_price_backfill |
| `coupang_data_breach_case` | `DATA_SECURITY_SUPPLIER_REGULATION_OVERLAY` | undated | needs_source_date_and_price_backfill |
| `coway_rental_recurring_case` | `HOME_LIVING_APPLIANCE_RENTAL` | undated | needs_source_date_and_price_backfill |
| `whirlpool_dividend_suspension_case` | `HOME_LIVING_APPLIANCE_RENTAL` | undated | needs_source_date_and_price_backfill |
| `shein_temu_ip_litigation_case` | `APPAREL_FAST_FASHION_BRAND_OEM` | 2026-05-11 | missing_public_price_data |

## Alignment Labels

- `EXPORT_RECURRING_ALIGNED`: export, ASP, OPM, EPS revision, and price path align.
- `FOOD_SAFETY_REGULATORY_4C_WATCH`: recall or country sales ban requires Stage 3 review.
- `KBEAUTY_STRUCTURAL_SUCCESS_CANDIDATE`: channel and export evidence route research; sell-through must be verified.
- `BEAUTY_DEVICE_4B`: successful device/export story, but valuation and price run require 4B-watch.
- `ECOMMERCE_SCALE_WITH_TRUST_RISK`: trust/regulation breaks the scale narrative.
- `HARDWARE_CYCLE_FAILURE`: appliance hardware cycle lacks recurring service economics.
- `FAST_FASHION_LEGAL_4C`: IP, supplier, product safety, or customs risk blocks Green.
