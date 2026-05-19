# Round-200 R9 Loop-7 Green Gate Review

## Green Required Evidence

- `unit_economics_confirmed`
- `fcf_after_capex_confirmed`
- `margin_durability_confirmed`
- `hybrid_mix_load_factor_freight_contract_or_tourist_spend_confirmed`
- `shareholder_return_or_deleveraging_confirmed`
- `safety_and_operational_trust_passed`
- `tariff_fuel_fx_freight_normalization_stress_passed`
- `price_path_after_unit_economics`

## Green Forbidden Patterns

- `travel_reopening_only`
- `freight_rate_spike_only`
- `robotaxi_or_sdv_story_only`
- `tourist_arrival_policy_only`
- `merger_completion_without_synergy`
- `ev_or_ai_mobility_theme_only`
- `capex_heavy_localization_without_margin`
- `safety_failure`
- `tariff_margin_cut`
- `utilization_weak`
- `cycle_normalization`

## Shadow Score Adjustments

| axis | direction | points | reason |
| --- | --- | ---: | --- |
| `hybrid_mix` | raise | 5 | 완성차 Green은 hybrid mix가 실제 margin과 FCF로 내려올 때 강하다. |
| `fcf_after_capex` | raise | 5 | R9는 투자 이후 남는 FCF가 핵심이다. |
| `shareholder_return_execution` | raise | 4 | 자사주/배당 실행은 value-up의 실제 증거다. |
| `operating_margin_durability` | raise | 4 | OPM 목표가 유지되어야 체급 변화가 지속된다. |
| `localization_tariff_hedge` | raise | 3 | 현지화는 tariff 충격을 흡수할 때만 점수를 준다. |
| `unit_economics` | raise | 5 | 운송/레저는 단위경제성이 Stage 3의 중심이다. |
| `load_factor_with_yield` | raise | 4 | 항공은 탑승률과 yield가 같이 좋아야 한다. |
| `integration_synergy_realized` | raise | 4 | 합병 완료보다 실제 통합 시너지와 비용절감이 중요하다. |
| `fleet_utilization` | raise | 4 | 차량/항공/카지노/리조트는 가동률이 숫자로 보여야 한다. |
| `tourist_spend_conversion` | raise | 4 | 관광객 수보다 실제 객단가와 구매전환이 중요하다. |
| `casino_drop_and_hold` | raise | 4 | 카지노는 drop과 hold rate가 확인되어야 한다. |
| `safety_record_and_operational_trust` | raise | 5 | 운송 섹터 Green은 안전과 운영신뢰를 통과해야 한다. |
| `travel_reopening_only` | lower | -5 | 여행수요 회복만으로 Stage 3-Green을 만들지 않는다. |
| `freight_rate_spike_only` | lower | -5 | 운임 spike는 구조적 E2R보다 사이클로 분리한다. |
| `robotaxi_or_sdv_story_only` | lower | -5 | SDV/로보택시 narrative는 유료 SW 매출과 안전 전까지 Stage 1~2다. |
| `tourist_arrival_policy_only` | lower | -4 | 무비자/입국자 증가는 spend와 OPM 전까지 정책 이벤트다. |
| `merger_completion_without_synergy` | lower | -3 | 합병 완료만으로 통합 시너지를 발명하지 않는다. |
| `ev_or_ai_mobility_theme_only` | lower | -4 | EV/AI mobility 테마는 FCF와 unit economics 전까지 제한한다. |
| `capex_heavy_localization_without_margin` | lower | -3 | 현지화 CAPEX가 margin을 훼손하면 Green을 낮춘다. |
| `safety_failure` | lower | -5 | fatal safety accident는 hard RedTeam이다. |
| `tariff_margin_cut` | lower | -4 | 관세로 margin guidance가 하향되면 4C-watch다. |
| `utilization_weak` | lower | -4 | 가동률/객단가/drop 부진은 여행·카지노 Green을 막는다. |
| `cycle_normalization` | lower | -4 | 운임/여행/수요 정상화는 4B/4C watch다. |

## What Not To Change

- Do not apply these weights to production scoring yet.
- Do not use Round200 cases as candidate-generation input.
- Do not lower Stage 3-Green thresholds to force promotion.
- Do not invent unit economics, FCF, margin, load factor, yield, tourist spend, drop, hold, stage prices, or MFE/MAE.
- Do not treat travel reopening, freight spike, SDV/robotaxi story, tourism policy, or merger completion as Green evidence alone.
