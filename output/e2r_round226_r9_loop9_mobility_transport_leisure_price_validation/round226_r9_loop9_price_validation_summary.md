# Round 226 R9 Loop 9 Mobility Transport Leisure Price Validation

This pack is calibration-only. Production scoring and candidate generation are unchanged.

## Summary

- source_round: docs/round/round_226.md
- large_sector: MOBILITY_TRANSPORT_LEISURE
- cases: 8
- success_candidate: 3
- event_premium: 2
- failed_rerating: 1
- cyclical_success: 1
- Stage 3 dated cases: 0
- 4B-watch cases: 7
- hard_4c_case_count: 1
- full_ohlc_complete: false

## Case Matrix

| case | company | type | stage2 | stage3 | 4B | 4C | alignment | note |
|---|---|---|---|---|---|---|---|---|
| r9_loop9_hyundai_hybrid_valueup_tariff_watch | 현대차 | success_candidate | 2024-08-28 |  |  | 2025-07-31 | aligned | Hybrid/value-up supports Stage 3 candidate review, but tariff margin cost creates simultaneous 4C-watch. |
| r9_loop9_kia_sdv_delay_capex_watch | 기아 | failed_rerating | 2026-04-09 |  |  | 2026-04-09 | evidence_good_but_price_failed | Hybrid expansion is useful, but SDV delay, EV target cut, and capex hike block Green before software revenue and FCF are visible. |
| r9_loop9_cj_logistics_shinsegae_contract_price_failed | CJ대한통운 | success_candidate | 2024-04-01 |  |  |  | evidence_good_but_price_failed | Logistics contract is Stage 2; margin, parcel volume, automation efficiency, overseas recovery, and FCF are required before Green. |
| r9_loop9_korean_air_asiana_integration_capex_watch | 대한항공 | success_candidate | 2024-12-12 |  |  |  | unknown | Merger scale is Stage 2; synergy, load factor, yield, FCF, and capex/debt burden determine promotion. |
| r9_loop9_jeju_air_fatal_crash_hard_4c | 제주항공 | 4c_thesis_break |  |  |  | 2024-12-30 | false_positive_score | Fatal crash is a hard 4C safety/trust break and blocks any reopening-demand Green. |
| r9_loop9_hmm_red_sea_shipping_cycle | HMM / container shipping cycle | cyclical_success | 2024-07-03 |  |  |  | aligned | Freight spike can be profitable but remains cyclical until contract mix, rate floor, FCF, and capital return confirm durability. |
| r9_loop9_tourism_visa_free_retail_casino_event | 호텔신라/파라다이스/현대백화점 | event_premium | 2025-08-06 |  | 2025-08-06 |  | price_moved_without_evidence | Visa-free policy is Stage 2/event premium; tourist spend, casino drop/hold, duty-free sales, occupancy, OPM, and FCF decide promotion. |
| r9_loop9_lotte_tour_china_japan_redirect_event | 롯데관광개발/Yellow Balloon | event_premium | 2025-11-21 |  | 2025-11-21 |  | price_moved_without_evidence | Tourism redirect expectation moved price before actual arrivals, occupancy, casino drop, ADR, and FCF. |

## Interpretation
- Hyundai is a hybrid/value-up Stage 2 watch, but tariff cost adds 4C-watch.
- Kia and CJ Logistics show why evidence can be useful while price or capex/margin confirmation still fails.
- Korean Air is integration scale watch, while Jeju Air is a hard safety/trust 4C example.
- HMM is cyclical success; tourism baskets are event premium until spend, utilization, and FCF confirm.
