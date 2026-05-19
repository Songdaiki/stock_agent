# Checkpoint 28A Round 200 R9 Loop 7 Mobility Transport Leisure Price Validation

## Scope

Round 200 반영 범위는 모빌리티, 운송, 레저의 가격경로 검증 팩이다.
이번 패치는 production scoring을 바꾸지 않고, case library와 shadow weight 검증 재료만 추가했다.

쉬운 예: `as_of_date=2025-09-29`에 중국 무비자 정책 뉴스가 있어도, 면세 객단가와 실제 매출 전환이 아직 없으면 Stage 3-Green 근거가 아니라 Stage 1~2 관찰 근거다.

## Added Files

- `src/e2r/sector/round200_r9_loop7_mobility_transport_leisure_price_validation.py`
- `src/e2r/cli/build_round200_r9_loop7_report.py`
- `tests/test_round200_r9_loop7_mobility_transport_leisure_price_validation.py`
- `data/e2r_case_library/cases_r9_loop7_round200.jsonl`
- `data/sector_taxonomy/round200_r9_loop7_mobility_transport_leisure_price_validation_audit.json`
- `output/e2r_round200_r9_loop7_mobility_transport_leisure_price_validation/`

## Case Pack

| case_id | company | archetype focus | role |
| --- | --- | --- | --- |
| `hyundai_motor_hybrid_valueup_tariff_4c_watch` | 현대차 | hybrid/value-up + tariff localization | structural candidate with 4C-watch |
| `kia_hybrid_valueup_sdv_delay_capex_watch` | 기아 | hybrid/value-up + SDV/capex delay | evidence-good but price-path watch |
| `korean_air_asiana_integration_scale_stage2_watch` | 대한항공 | airline integration scale | Stage 2 watch until synergy/FCF |
| `jeju_air_fatal_crash_operational_trust_4c_break` | 제주항공 | airline safety/regulatory | hard 4C operational trust break |
| `hmm_red_sea_freight_cycle_stage2_4b_watch` | HMM | freight cycle | cyclical success, not structural Green |
| `hotel_shilla_china_visa_tourism_event_stage2_watch` | 호텔신라 | tourism policy/duty-free | event premium until spend/OPM |
| `lotte_tour_dream_tower_casino_utilization_gap_watch` | 롯데관광개발 | casino return visitor unit economics | utilization gap watch |

## Green Gate

Round 200의 핵심은 headline과 unit economics를 분리하는 것이다.

Green에 필요한 필드는 다음과 같다.

- `unit_economics_confirmed`
- `fcf_after_capex_confirmed`
- `margin_durability_confirmed`
- `hybrid_mix_load_factor_freight_contract_or_tourist_spend_confirmed`
- `shareholder_return_or_deleveraging_confirmed`
- `safety_and_operational_trust_passed`
- `tariff_fuel_fx_freight_normalization_stress_passed`
- `price_path_after_unit_economics`

Green을 막는 패턴은 다음과 같다.

- 여행 재개만 있는 경우
- 운임 spike만 있는 경우
- SDV/로보택시 스토리만 있는 경우
- 관광객 정책 이벤트만 있는 경우
- 합병 완료만 있고 시너지가 없는 경우
- EV/AI 모빌리티 테마만 있는 경우
- 현지화 CAPEX가 margin을 훼손하는 경우
- 안전 사고, tariff margin cut, utilization 약화, cycle normalization

## Stage 4B / 4C Notes

- 제주항공 fatal accident는 `fatal_safety_accident`와 `operational_trust_break`로 hard 4C다.
- 현대차/기아는 hybrid mix와 주주환원이 강해도 tariff, SDV 지연, CAPEX 부담이 4C-watch가 될 수 있다.
- HMM은 freight rebound가 커도 구조적 E2R Green이 아니라 cycle success와 4B-watch로 분리한다.
- 호텔신라/롯데관광개발은 관광객 수보다 `tourist_spend`, `casino_drop`, `hold_rate`, `occupancy`, `OPM` 확인이 필요하다.

## Outputs

Generated report files:

- `round200_r9_loop7_price_validation_summary.md`
- `round200_r9_loop7_case_matrix.csv`
- `round200_r9_loop7_target_aliases.csv`
- `round200_r9_loop7_score_adjustments.csv`
- `round200_r9_loop7_price_backfill_fields.csv`
- `round200_r9_loop7_green_gate_review.md`
- `round200_r9_loop7_price_backfill_plan.md`
- `round200_r9_loop7_stage4b_4c_review.md`

## Commands Run

```bash
PYTHONPATH=src python -m unittest tests.test_round200_r9_loop7_mobility_transport_leisure_price_validation -v
PYTHONPATH=src python -m e2r.cli.build_round200_r9_loop7_report
```

Full test suite was also run after the patch.

## What Not To Change

- Do not apply Round 200 score weights to production scoring yet.
- Do not use Round 200 cases as candidate-generation input.
- Do not lower Stage 3-Green thresholds to force promotion.
- Do not invent unit economics, FCF, margin, load factor, yield, tourist spend, drop, hold, prices, MFE, or MAE.
- Do not treat travel reopening, freight spike, SDV/robotaxi story, tourism policy, or merger completion as Green evidence alone.

## Next

Next step is OHLC/price-path backfill. In practice, 현대차처럼 좋은 evidence가 있어도 tariff margin cut 이후의 price path를 봐야 하고, HMM처럼 price가 먼저 움직인 case는 freight cycle normalization 전후의 MFE/MAE를 분리해야 한다.
