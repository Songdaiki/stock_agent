# Round-54 R1 Loop-2 Price Validation Plan

## Method

1. Assign stage dates from source evidence only.
2. Store stage-date close prices from official price data.
3. Calculate MFE_30D / 90D / 180D / 1Y / 2Y.
4. Calculate MAE_30D / 90D / 180D / 1Y.
5. Compare contract quality, backlog, margin, OP/EPS revision, and price path.
6. Mark capital-allocation shock, project delay, CAPA normalization, and low-margin backlog explicitly.

## Priority Case Checks

| case_id | target | stage marker | check |
| --- | --- | --- | --- |
| `us_transformer_shortage_korea_import_case` | `GRID_TRANSFORMER_SHORTAGE` | 2026-05-11 | needs_price_backfill |
| `ls_electric_525kv_datacenter_transformer_case` | `GRID_TRANSFORMER_SHORTAGE` | undated | needs_contract_date_backfill |
| `ge_vernova_data_center_orders_case` | `AI_DATA_CENTER_POWER_EQUIPMENT` | 2026-04-22 | needs_price_backfill |
| `hanwha_aerospace_romania_k9_case` | `DEFENSE_GOVERNMENT_BACKLOG` | 2024-07-09 | needs_price_backfill |
| `hanwha_aerospace_europe_sales_case` | `DEFENSE_GOVERNMENT_BACKLOG` | 2024-10-07 | needs_price_backfill |
| `hanwha_aerospace_dilution_case` | `DEFENSE_GOVERNMENT_BACKLOG` | 2025-03-27 | needs_price_backfill |
| `hyundai_rotem_morocco_rail_case` | `RAIL_INFRASTRUCTURE` | 2025-02-26 | needs_price_backfill |
| `korean_shipbuilder_contract_rally_case` | `SHIPBUILDING_OFFSHORE_BACKLOG` | undated | needs_source_date_backfill |
| `hanwha_ocean_mro_rerating_case` | `SHIPBUILDING_OFFSHORE_BACKLOG` | 2025-04-28 | needs_price_backfill |
| `meta_constellation_nuclear_ppa_case` | `NUCLEAR_SMR_GRID_POLICY` | 2025-06-03 | needs_price_backfill |
| `nuscale_cfpp_cancel_case` | `NUCLEAR_SMR_GRID_POLICY` | 2023-11-01 | needs_price_backfill |
| `data_center_delay_transformer_soft_4c_case` | `GRID_TRANSFORMER_SHORTAGE` | 2026-02-24 | needs_price_backfill |

## Alignment Labels

- `contract_quality_aligned`: contract value/duration/delivery/margin/EPS and price path align.
- `project_delay_risk`: demand exists but project execution threatens order growth.
- `capital_allocation_shock`: backlog remains attractive but dilution or funding damages price path.
- `policy_to_contract_failed`: policy/MOU does not become funded order or revenue.
- `crowded_rerating_4b`: good structure but market recognition is already crowded.
