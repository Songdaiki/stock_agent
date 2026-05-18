# Round-172 R1 Loop-11 Price Validation Plan

## Method

1. Assign Stage 1/2/3/4B/4C dates from dated source evidence only.
2. Backfill KRX daily bars for `price_at_stage1` through `price_at_stage4c`.
3. Calculate 20D/60D/120D/252D returns after Stage 2 and Stage 3.
4. Calculate MFE/MAE after Stage 2, especially 60D/120D/252D.
5. Compare price speed against OP/EPS revision speed to decide Stage 3 vs 4B-watch.
6. Store `score_price_alignment` and keep LOI/MOU, preferred bidder, IPO, legal gate, sanction, and missing detail labels explicit.

## Priority Case Checks

| case_id | target | stage marker | check |
| --- | --- | --- | --- |
| `hd_hyundai_electric_transformer_stage3_4b_case` | `GRID_TRANSFORMER_SHORTAGE_KOREA` | 2026-05-11 | needs_price_backfill |
| `hyosung_hico_hvdc_stage25_case` | `GRID_US_LOCALIZATION_CAPA` | 2025-12-02 | needs_price_backfill |
| `doosan_czech_nuclear_preferred_bidder_case` | `NUCLEAR_EXPORT_PREFERRED_BIDDER` | 2024-10-30 | needs_price_backfill |
| `kepco_engineering_czech_nuclear_preferred_bidder_case` | `NUCLEAR_EXPORT_PREFERRED_BIDDER` | 2024-07-17 | needs_price_backfill |
| `kepco_kps_czech_nuclear_preferred_bidder_case` | `NUCLEAR_EXPORT_PREFERRED_BIDDER` | 2024-07-17 | needs_price_backfill |
| `hd_hyundai_heavy_mipo_merger_stage2_4b_case` | `SHIPBUILDING_US_PLATFORM_RESTRUCTURING` | 2025-08-27 | needs_price_backfill |
| `hd_hyundai_marine_solution_ipo_mro_case` | `SHIP_MRO_RECURRING_PLATFORM` | 2024-05-08 | needs_price_backfill |
| `kai_fa50_philippines_stage2_case` | `DEFENSE_AIRCRAFT_EXPORT_BACKLOG` | 2025-06-04 | needs_price_backfill |
| `lig_nex1_cheongung_combat_validation_stage25_case` | `DEFENSE_INTERCEPTOR_COMBAT_VALIDATION` | 2025-06-13 | needs_price_backfill |
| `hanwha_ocean_china_sanction_4c_case` | `GEOPOLITICAL_SHIPBUILDING_SANCTION_OVERLAY` | undated | needs_source_date_backfill |
| `hd_hyundai_mipo_loi_only_case` | `MOU_LOI_NOT_CONTRACT` | 2025-04-08 | needs_price_backfill |
| `doosan_czech_nuclear_legal_gate_case` | `NUCLEAR_EXPORT_LEGAL_GATE` | 2024-10-30 | needs_price_backfill |

## Alignment Labels

- `stage3_catch_and_4b_cool_required`: the case should be detectable before a large move, then cooled when crowded.
- `stage2_5_not_green_yet`: evidence is stronger than a headline, but not enough for Green.
- `event_to_contract_not_green_yet`: event or preferred bidder must convert into signed contract and company scope.
- `good_model_but_ipo_4b`: business quality exists, but the first price path is IPO premium.
- `green_block_correct`: LOI/MOU or missing detail correctly blocks Stage 3.
- `hard_redteam_alignment`: sanction, legal gate, or disclosure break correctly blocks positive narrative.
