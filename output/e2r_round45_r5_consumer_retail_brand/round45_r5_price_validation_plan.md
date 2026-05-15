# Round-45 R5 Price Validation Plan

## Method

1. Assign stage dates from source evidence only.
2. Store stage-date close prices from official price data.
3. Calculate MFE_30D / 90D / 180D / 1Y / 2Y.
4. Calculate MAE_30D / 90D / 180D / 1Y.
5. Calculate peak price, drawdown after peak, and below-stage3 flag.
6. Compare price paths with export growth, overseas sales, ASP, OPM, inventory, receivables, sell-through, rental accounts, churn, and 4C flags.

## Priority Case Checks

| case_id | stage candidate | check |
| --- | --- | --- |
| `samyang_buldak_export_rerating_case` | 2024-06-14 | needs_price_backfill |
| `samyang_buldak_recall_risk_case` | 2024-06-12 | needs_price_backfill |
| `kbeauty_us_offline_channel_case` | 2025-06-05 | missing_direct_symbol_mapping |
| `apr_medicube_device_export_case` | needs_source_date | needs_source_date_and_price_backfill |
| `cu_gs25_store_efficiency_case` | needs_source_date | needs_source_date_and_price_backfill |
| `coupang_supplier_regulation_case` | 2026-02-26 | needs_price_backfill |
| `coupang_data_breach_case` | needs_source_date | needs_source_date_and_price_backfill |
| `coway_rental_recurring_case` | needs_source_date | needs_source_date_and_price_backfill |
| `whirlpool_hardware_cycle_4c_case` | 2026-05-07 | needs_price_backfill |
| `shein_temu_ip_regulatory_case` | 2026-05-11 | missing_direct_symbol_mapping |

## Alignment Labels

- `aligned_candidate`: export, channel, ASP/OPM, revision, and price path move together.
- `viral_price_move`: viral or celebrity-driven price action appears before sell-through and FCF.
- `channel_stuffing_risk`: shipment growth exists but sell-through, inventory, or receivables are unclear.
- `regulatory_thesis_break`: recall, data breach, supplier regulation, IP, product safety, or policy damage appears.
- `hardware_cycle_failure`: appliance replacement demand weakens without rental/service recurring protection.
- `watch_to_green`: repeated revenue exists, but explosive EPS/FCF and price-path evidence still need validation.
