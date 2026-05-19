# Round 231 R1 Loop 10 Industrial Orders / Infrastructure Price Validation

This pack is calibration-only. Production scoring and candidate generation are unchanged.

## Summary

- source_round: docs/round/round_231.md
- large_sector: INDUSTRIAL_ORDERS_INFRA
- cases: 8
- structural_success: 1
- success_candidate: 6
- event_premium_count: 2
- thesis_break_watch_count: 1
- Stage 3 dated cases: 1
- 4B-watch cases: 7
- price_failed_count: 2
- full_ohlc_complete: false

## Case Matrix

| case | company | type | stage3 | 4B | 4C | round alignment | note |
|---|---|---|---|---|---|---|---|
| r1_loop10_ls_electric_grid_transformer_price_failed | LS ELECTRIC | success_candidate |  |  |  | evidence_good_but_price_failed | Strong grid/data-center evidence and company contract, but event price failed; Stage 3 requires delivery, margin and FCF. |
| r1_loop10_hyundai_rotem_k2_export_aligned | Hyundai Rotem | structural_success | 2024-04-09 |  |  | aligned_partial | K2 delivery/revenue/OP revision makes this a Stage 3 candidate; follow-up Poland/Peru contracts support continuation. |
| r1_loop10_lig_nex1_cheongung_export_crowding | LIG Nex1 | success_candidate |  | 2024-07-02 |  | success_candidate_4B_watch | Iraq export validates Stage 2, but 1H +69% and downgrade selloff show 4B/crowding risk. |
| r1_loop10_hanwha_aerospace_poland_missile_jv_dilution_watch | Hanwha Aerospace | success_candidate |  | 2025-03-21 |  | success_candidate_aligned_4B_detection | Poland missile JV is Stage 2; large capital raise after rerating is 4B/dilution watch, not hard 4C. |
| r1_loop10_samsung_ea_gs_fadhili_epc | Samsung E&A / GS E&C | success_candidate |  | 2024-04-03 |  | success_candidate | Large EPC contract is Stage 2; Stage 3 requires margin, progress revenue, cash collection and working-capital control. |
| r1_loop10_hyundai_ec_jafurah_gas_infra | Hyundai E&C | success_candidate |  |  |  | success_candidate | Sovereign gas-infra contract is Stage 2; margin, progress revenue and cash recovery required before Green. |
| r1_loop10_hd_hyundai_heavy_mipo_masga_event | HD Hyundai Heavy / HD Hyundai Mipo | success_candidate |  | 2025-08-27 |  | event_premium_success_candidate | Merger/MASGA is Stage 2 and 4B-watch; funded order and margin required for Stage 3. |
| r1_loop10_hanwha_ocean_china_sanction_watch | Hanwha Ocean | 4c_thesis_break |  |  | 2025-10-14 | thesis_break_watch | China sanctions are 4C-watch; hard 4C requires actual revenue or contract disruption. |

## Interpretation
- Hyundai Rotem is the cleanest R1 order-to-revenue Stage 3 candidate because delivery, revenue, OP revision, and price reaction align.
- LS Electric is strong Stage 2 watch, but event-day price failure and unverified margin/FCF block Green.
- LIG Nex1 and Hanwha Aerospace prove that good defense export evidence still needs 4B/crowding and dilution watch.
- Samsung E&A, GS E&C, and Hyundai E&C are EPC Stage 2 cases until margin, progress revenue, cash collection, and working capital confirm.
- HD Hyundai Heavy/Mipo MASGA is a policy/merger event premium before funded U.S. order and margin evidence.
- Hanwha Ocean is geopolitical 4C-watch, not hard 4C, until actual revenue or contract disruption is confirmed.
