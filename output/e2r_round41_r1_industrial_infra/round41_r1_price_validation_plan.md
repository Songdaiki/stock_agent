# Round-41 R1 Price Validation Plan

## Method

1. Assign stage dates from source evidence only.
2. Store stage-date close prices from official price data.
3. Calculate MFE_30D / 90D / 180D / 1Y / 2Y.
4. Calculate MAE_30D / 90D / 180D / 1Y.
5. Calculate peak price, drawdown after peak, and below-stage3 flag.
6. Compare price paths with OP/EPS revision, backlog growth, contract quality, and margin evidence.

## Priority Case Checks

| case_id | stage2 candidate | check |
| --- | --- | --- |
| `hd_hyundai_electric_transformer_shortage_candidate` | needs_source_date | needs_price_backfill |
| `hyosung_heavy_transformer_backlog_candidate` | needs_source_date | needs_price_backfill |
| `hanwha_aerospace_romania_k9_success_case` | 2024-07-09 | needs_price_backfill |
| `hanwha_aerospace_europe_land_arms_visibility_candidate` | 2024-10-07 | needs_price_backfill |
| `hyundai_rotem_morocco_rail_order_case` | 2025-02-26 | needs_price_backfill |
| `korean_shipbuilders_contract_rally_case` | needs_source_date | needs_price_backfill |
| `meta_constellation_nuclear_ppa_reference` | 2025-06-03 | missing_kr_equity_mapping |
| `anduril_lccm_reference_case` | 2026-05-13 | missing_public_price_data |
| `palantir_maven_contract_case` | 2024-05-29 | needs_price_backfill |
| `hanwha_aerospace_dilution_risk_case` | 2025-03-27 | needs_price_backfill |
| `nuscale_cfpp_cancel_4c_case` | 2023-11-01 | needs_price_backfill |
| `khnp_czech_legal_delay_case` | 2025-05-01 | missing_direct_symbol_mapping |

## Alignment Labels

- `aligned`: Stage 2/3 evidence and price rerating persist together.
- `cyclical_success`: price worked, but structural EPS persistence is not yet proven.
- `event_premium`: policy, tender, reconstruction, or MOU premium without revenue conversion.
- `false_positive_score`: order or theme looked strong, but margin/EPS/price failed.
- `thesis_break`: cancellation, legal delay, dilution shock, or project failure damages the thesis.
