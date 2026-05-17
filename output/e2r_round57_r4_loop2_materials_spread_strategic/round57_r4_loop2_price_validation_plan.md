# Round-57 R4 Loop-2 Price Validation Plan

## Method

1. Assign stage dates from source evidence only.
2. Store stage-date close prices from official price data.
3. Calculate MFE_30D / 90D / 180D / 1Y / 2Y.
4. Calculate MAE_30D / 90D / 180D / 1Y.
5. Compare commodity price, product spread, inventory gain/loss, offtake, price floor, government support, FCF, and price path.
6. Mark event premium, oversupply, supply glut, mine restart, dividend cut, and no commercialization explicitly.

## Priority Case Checks

| case_id | target | stage marker | check |
| --- | --- | --- | --- |
| `mp_materials_dod_apple_price_floor_case` | `RARE_METALS_STRATEGIC_MATERIALS` | undated | needs_source_date_and_price_backfill |
| `china_heavy_rare_earth_export_control_case` | `RARE_METALS_STRATEGIC_MATERIALS` | 2026-05-13 | missing_direct_symbol_mapping |
| `posco_international_alaska_lng_20y_case` | `GENERAL_TRADING_RESOURCE_INFRA` | 2025-12-04 | needs_price_backfill |
| `berkshire_japan_sogo_shosha_case` | `GENERAL_TRADING_RESOURCE_INFRA` | 2025-03-17 | needs_price_backfill |
| `barrick_record_gold_buyback_case` | `PRECIOUS_METALS_SAFE_HAVEN_MINERS` | 2026-05-11 | needs_price_backfill |
| `sk_innovation_refining_recovery_case` | `REFINING_OIL_SPREAD` | 2026-05-13 | needs_price_backfill |
| `copper_ai_grid_demand_case` | `NONFERROUS_STRATEGIC_METALS` | 2025-12-12 | missing_direct_symbol_mapping |
| `korea_zinc_tender_offer_event_case` | `NONFERROUS_STRATEGIC_METALS` | 2024-09-13 | needs_price_backfill |
| `ds_smith_international_paper_packaging_case` | `PAPER_PACKAGING_CYCLE` | 2025-04-14 | missing_public_price_data |
| `lg_chem_lotte_chemical_oversupply_case` | `CHEMICAL_SPREAD` | 2025-02-07 | needs_price_backfill |
| `lithium_price_86pct_crash_case` | `LITHIUM_BATTERY_RAW_MATERIAL` | 2025-01-13 | missing_price_data |
| `bhp_iron_ore_profit_dividend_cut_case` | `STEEL_METAL_SPREAD` | 2025-08-18 | needs_price_backfill |
| `advanced_material_speculative_theme_counterexample` | `ADVANCED_MATERIAL_SPECULATIVE_THEME` | undated | missing_price_data |

## Alignment Labels

- `STRUCTURAL_RESOURCE_SUCCESS`: evidence and price path support durable resource/infra rerating.
- `COMMODITY_CYCLICAL_SUCCESS`: spread or commodity price worked, but structural durability remains unproven.
- `EVENT_PREMIUM_MISCLASSIFIED`: event-day price reaction should not be scored as FCF rerating.
- `SPREAD_RECOVERY_FALSE_GREEN`: spread rebound was a false Green risk because oversupply or inventory reversed it.
- `PRICE_FLOOR_OFFTAKE_GREEN_CANDIDATE`: price floor, offtake, government support, and production make rare metals higher quality.
- `COMMODITY_PRICE_4C`: commodity price collapse or supply restart breaks the thesis.
