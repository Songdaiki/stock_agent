# Round-175 R4 Loop-11 Price Validation Plan

## Method

1. Assign Stage 1/2/3/4B/4C dates from dated source evidence only.
2. Backfill KRX daily bars for `price_at_stage1` through `price_at_stage4c`.
3. Calculate 1D/5D event returns plus 20D/60D/120D/252D returns and MFE/MAE after Stage 2.
4. Compare price speed against OP/EPS revision, commodity price, spread, export volume, and tariff scope.
5. Separate company-level Stage 2 proof from event-led 4B-watch and direct-risk 4C-watch.
6. Keep media-only, company-unconfirmed, export-tariff, M&A unwind, commodity-cycle, and disclosure-detail caps explicit.

## Priority Case Checks

| case_id | target | stage marker | check |
| --- | --- | --- | --- |
| `copper_ai_grid_korea_basket_stage2_cap_case` | `COPPER_AI_GRID_KOREA` | 2025-12-12 | needs_krx_price_and_revision_backfill |
| `poongsan_copper_defense_mna_unwind_case` | `COPPER_PROCESSING_PLUS_DEFENSE` | 2026-04-09 | needs_price_backfill |
| `oci_holdings_spacex_polysilicon_report_cap_case` | `POLYSILICON_NON_CHINA_SUPPLY_OPTION` | 2026-04-14 | needs_price_backfill |
| `steel_tariff_directionality_korea_case` | `STEEL_TARIFF_EVENT_KOREA` | 2024-04-17 | needs_exact_stage_date_backfill |
| `seah_steel_export_tariff_4c_case` | `STEEL_EXPORT_TARIFF_4C` | 2025-06-02 | needs_exact_stage_date_backfill |
| `specialty_steel_us_localization_option_case` | `SPECIALTY_STEEL_US_LOCALIZATION_OPTION` | undated | needs_case_backfill |
| `lithium_rare_earth_price_only_theme_case` | `LITHIUM_PRICE_EVENT_KOREA` | undated | needs_case_backfill |
| `rare_earth_theme_korea_stage1_case` | `RARE_EARTH_THEME_KOREA` | undated | needs_case_backfill |
| `chemical_spread_korea_watch_red_case` | `CHEMICAL_SPREAD_KOREA` | undated | needs_case_backfill |
| `disclosure_confidence_materials_cap_case` | `DISCLOSURE_CONFIDENCE_CAP` | undated | not_price_applicable |

## Alignment Labels

- `macro_bottleneck_not_company_green`: commodity macro signal exists, but individual company proof is missing.
- `event_unwind_alignment`: an event premium should reverse when the event fails.
- `report_not_contract_cap`: famous customer name or media report is not a contract.
- `directionality_required`: tariff target and scope must be parsed before scoring.
- `direct_tariff_4c_alignment`: price-path downside matches a hard export tariff risk.
- `event_rally_not_structural`: lithium/rare-earth/commodity price event is not structural evidence.
