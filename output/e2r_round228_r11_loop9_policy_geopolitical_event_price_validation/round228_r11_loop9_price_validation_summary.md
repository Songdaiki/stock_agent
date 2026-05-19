# Round 228 R11 Loop 9 Policy Geopolitical Event Price Validation

This pack is calibration-only. Production scoring and candidate generation are unchanged.

## Summary

- source_round: docs/round/round_228.md
- large_sector: POLICY_GEOPOLITICAL_EVENT
- cases: 8
- success_candidate: 4
- event_premium: 2
- failed_rerating: 2
- price_moved_without_evidence: 2
- Stage 3 dated cases: 0
- 4B-watch cases: 6
- hard_4c_case_count: 0
- deep_sub_archetype_count: 8
- shadow_weight_row_count: 8
- r11_default_stage3_bias: very_conservative
- full_ohlc_complete: false

## Case Matrix

| case | company | type | stage2 | stage3 | 4B | 4C | alignment | note |
|---|---|---|---|---|---|---|---|---|
| r11_loop9_commercial_act_valueup_reform | Commercial Act / 밸류업 거버넌스 개혁 | success_candidate | 2025-08-25 |  |  |  | aligned | 상법 개정은 market-structure Stage 2 토양이다. 회사별 Green은 실제 소각·배당·ROE/EPS 확인 후다. |
| r11_loop9_tax_policy_market_shock | 세제안 shock | failed_rerating |  |  |  | 2025-08-01 | false_positive_score | 세제 surprise는 value-up momentum의 반대편에 있는 policy-confidence 4C-watch다. |
| r11_loop9_us_korea_trade_tariff_fx_watch | 한미 tariff / $350B deal | success_candidate | 2025-10-29 |  |  | 2025-12-01 | aligned | 관세 relief는 Stage 2지만, 회사별 마진 회복·FCF·EPS와 $350B FX outflow watch를 같이 확인해야 한다. |
| r11_loop9_hyundai_steel_us_capex_tariff_strategy_fail | 현대제철 | failed_rerating |  |  |  | 2025-04-22 | evidence_good_but_price_failed | 관세 hedge CAPEX처럼 보였지만 funding·마진·ROI 불확실성 때문에 4C-watch로 둔다. |
| r11_loop9_semiconductor_support_package | 반도체 33조 지원 package | success_candidate | 2025-04-15 |  |  |  | unknown | 반도체 지원은 Stage 2 policy support다. 개별 기업 Green은 주문·마진·EPS/FCF 확인 후다. |
| r11_loop9_fiscal_stimulus_voucher_event | 30.5조 추경·소비쿠폰 | event_premium | 2025-07-07 |  |  |  | price_moved_without_evidence | 소비쿠폰·추경은 domestic-demand event다. 실제 same-store sales와 margin 전에는 소비주 Green 금지다. |
| r11_loop9_posco_international_alaska_lng_offtake | POSCO International | success_candidate | 2025-12-04 |  |  |  | aligned | 실제 장기 LNG offtake는 단순 정책보다 강한 Stage 2다. FID·pricing·margin·cashflow 전에는 Stage 3가 아니다. |
| r11_loop9_kogas_east_sea_resource_event | 한국가스공사 / 동해 석유·가스 | event_premium |  |  | 2024-06-03 |  | price_moved_without_evidence | 자원 추정과 탐사 승인 전 +30%는 대표적인 price_moved_without_evidence다. 상업성 전에는 Green이 아니다. |

## Interpretation
- R11 default is Stage 1/2 event premium, not Stage 3-Green.
- Commercial Act reform is positive market-structure Stage 2, but company Green needs payout, ROE/EPS, and FCF.
- Tax-policy shock and Hyundai Steel CAPEX uncertainty are 4C-watch examples.
- Tariff relief and chip support are policy Stage 2 until company margin, order, and EPS/FCF confirm.
- POSCO International Alaska LNG is stronger Stage 2 because it has long-term offtake, but FID and margin still gate Green.
- Korea Gas East Sea is the clean price_moved_without_evidence example.
