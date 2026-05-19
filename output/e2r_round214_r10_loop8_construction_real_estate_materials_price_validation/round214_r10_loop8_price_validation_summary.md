# Round 214 R10 Loop 8 Construction Real Estate Materials Price Validation

This pack is calibration-only. Production scoring and candidate generation are unchanged.

## Summary

- source_round: docs/round/round_214.md
- large_sector: CONSTRUCTION_REAL_ESTATE_MATERIALS
- cases: 7
- success_candidate: 4
- failed_rerating: 1
- 4c_thesis_break: 2
- price_moved_without_evidence: 1
- Stage 3 dated cases: 0
- 4B-watch cases: 7
- hard_4c_case_count: 2
- full_ohlc_complete: false

## Case Matrix

| case | company | type | stage2 | stage3 | 4B | 4C | alignment | note |
|---|---|---|---|---|---|---|---|---|
| r10_loop8_samsung_ea_fadhili_epc | 삼성E&A | success_candidate | 2024-04-03 |  | 2024-04-03 |  | aligned | Large EPC award is Stage 2 and event 4B-watch; Stage 3 requires margin, progress revenue, and cash collection. |
| r10_loop8_hyundai_ec_jafurah_gas_infra | 현대건설 | success_candidate | 2024-06-30 |  |  |  | unknown | Sovereign EPC scale supports Stage 2; Green waits for margin, working capital, and cash recovery. |
| r10_loop8_daewoo_ec_grand_faw_handover | 대우건설 | success_candidate | 2024-11-12 |  |  |  | unknown | Handover milestone is Stage 2; profit recognition, cash recovery, and follow-on orders decide promotion. |
| r10_loop8_taeyoung_pf_hard_4c | 태영건설/PF stress | 4c_thesis_break |  |  |  | 2023-12-01 | false_positive_score | PF debt reschedule and delinquency spike are hard 4C; liquidity support is relief, not Green. |
| r10_loop8_hdc_hyundai_development_quality_safety_4c | HDC현대산업개발 | 4c_thesis_break |  |  |  | 2022-01-11 | false_positive_score | Apartment collapse and repeated Gwangju safety incidents are hard 4C for construction quality trust. |
| r10_loop8_posco_ec_dl_construction_safety_watch | POSCO E&C / DL Construction | failed_rerating |  |  |  | 2025-01-01 | false_positive_score | Repeated fatal accidents, site shutdowns, and license/fine risk require 4C-watch and safety-trust gate. |
| r10_loop8_ai_data_center_real_asset_watch | SK/AWS·OpenAI 데이터센터 | success_candidate | 2026-02-11 |  | 2025-06-20 |  | price_moved_without_evidence | AI data center investment is Stage 1/2; tenant, NOI/AFFO, power/water, and capex per share are required before Green. |

## Interpretation
- Samsung E&A, Hyundai E&C, and Daewoo E&C are Stage 2 candidates, not automatic Stage 3-Green.
- EPC headline needs margin, progress revenue, working-capital cash recovery, and cost control.
- PF debt reschedule and delinquency spike are hard RedTeam inputs, not Green evidence.
- Apartment collapse and repeated fatal accidents are construction quality/safety 4C gates.
- AI data-center real asset stories need tenant, NOI/AFFO, power/water, and capex-per-share proof.
