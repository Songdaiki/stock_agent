# Round-173 R2 Loop-11 Price Validation Plan

## Method

1. Assign Stage 1/2/3/4B/4C dates from dated source evidence only.
2. Backfill KRX daily bars for `price_at_stage1` through `price_at_stage4c`.
3. Calculate 20D/60D/120D/252D returns after Stage 2 and Stage 3.
4. Calculate MFE/MAE after Stage 2, especially 60D/120D/252D.
5. Compare price speed against OP/EPS revision speed to decide Stage 3 vs 4B-watch.
6. Keep media-report-only, private-company-linkage, policy-license, and on-device-theme caps explicit.

## Priority Case Checks

| case_id | target | stage marker | check |
| --- | --- | --- | --- |
| `hanmi_hbm_bonder_stage3_4b_case` | `HBM_BONDER_EQUIPMENT_KOREA` | undated | needs_source_date_backfill |
| `isu_petasys_ai_server_pcb_487pct_4b_case` | `AI_SERVER_PCB_MLB_KOREA` | undated | needs_price_backfill |
| `leeno_ai_test_socket_stage25_case` | `SEMICONDUCTOR_TEST_SOCKET_KOREA` | undated | needs_price_backfill |
| `db_hitek_foundry_reram_stage2_case` | `SYSTEM_SEMI_FOUNDARY_OPTION_KOREA` | 2025-12-10 | needs_price_backfill |
| `rebellions_sapeon_related_stock_green_cap_case` | `AI_CHIP_FABRIC_PRIVATE_RELATED` | 2026-03-26 | needs_price_backfill |
| `hanmi_micron_media_report_not_contract_case` | `MOU_OR_REPORT_NOT_CONTRACT` | undated | needs_source_date_backfill |
| `samsung_labor_disruption_overlay_case` | `HBM_SUPPLY_CHAIN_LABOR_DISRUPTION_OVERLAY` | 2026-05-15 | needs_price_backfill |
| `on_device_ai_revenue_missing_case` | `ON_DEVICE_AI_THEME` | undated | needs_case_backfill |
| `hbm_test_equipment_stage2_case` | `HBM_TEST_EQUIPMENT_KOREA` | undated | needs_case_backfill |
| `advanced_packaging_equipment_customer_order_case` | `ADVANCED_PACKAGING_EQUIPMENT_KOREA` | undated | needs_case_backfill |
| `ai_chip_private_related_direct_revenue_missing_case` | `AI_CHIP_LISTED_EARNINGS_LINK_GATE` | 2026-03-26 | needs_price_backfill |

## Alignment Labels

- `stage3_catch_and_4b_cool_required`: the case should be detectable before a large move, then cooled when crowded.
- `structural_success_but_late_4b`: structure was real, but current price path demands 4B monitoring.
- `quality_business_not_green_yet`: high quality is watch evidence, not Green without revisions and customer detail.
- `policy_license_not_green`: policy or license must become revenue before Stage 3.
- `listed_link_missing`: private-company event does not equal listed-company earnings evidence.
- `hard_redteam_alignment`: labor disruption, direct earnings link missing, or disclosure break correctly blocks positive narrative.
