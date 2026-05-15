# Round-44 R4 Price Validation Plan

## Method

1. Assign stage dates from source evidence only.
2. Store stage-date close prices from official price data.
3. Calculate MFE_30D / 90D / 180D / 1Y / 2Y.
4. Calculate MAE_30D / 90D / 180D / 1Y.
5. Calculate peak price, drawdown after peak, and below-stage3 flag.
6. Compare price paths with commodity price, product spread, EPS revision, FCF, dividend, buyback, offtake, price floor, and supply-glut evidence.

## Priority Case Checks

| case_id | stage candidate | check |
| --- | --- | --- |
| `mp_materials_dod_apple_offtake_case` | needs_source_date | needs_source_date_and_price_backfill |
| `china_rare_earth_export_control_bottleneck_case` | 2026-05-13 | missing_direct_symbol_mapping |
| `korea_zinc_tender_event_premium_case` | 2024-09-13 | needs_price_backfill |
| `berkshire_japan_sogo_shosha_case` | 2025-03-17 | needs_price_backfill |
| `posco_international_alaska_lng_20y_case` | 2025-12-04 | needs_price_backfill |
| `barrick_record_gold_buyback_case` | 2026-05-11 | needs_price_backfill |
| `sk_innovation_refining_recovery_watch` | 2026-05-13 | needs_price_backfill |
| `lg_chem_lotte_chemical_oversupply_4c` | 2025-02-07 | needs_price_backfill |
| `baosteel_steel_oversupply_cost_cut_case` | 2025-04-28 | missing_public_price_data |
| `bhp_iron_ore_profit_dividend_cut_case` | 2025-08-18 | needs_price_backfill |
| `lithium_price_86pct_crash_case` | 2025-01-13 | missing_price_data |
| `ds_smith_packaging_consolidation_case` | 2024-03-07 | missing_public_price_data |
| `rare_metals_theme_price_only_4b_watch` | needs_source_date | missing_price_data |

## Alignment Labels

- `structural_success`: price floor, offtake, long contract, FCF, and capital allocation persist together.
- `cyclical_success`: commodity price or spread drove EPS and price, but structural durability is not proven.
- `event_premium`: tender, control, M&A, or policy event moved price before core economics were verified.
- `false_positive_score`: price/spread news looked strong but EPS/FCF durability failed.
- `thesis_break`: supply glut, price crash, project delay, dividend cut, or inventory loss damages the thesis.
