# Checkpoint 28A Round 213 R9 Loop 8 Mobility Transport Leisure Price Validation

## 목적

라운드213은 R9 모빌리티·운송·레저 가격경로 검증 팩이다.

핵심 원칙은 단순하다. `하이브리드 전환`, `항공 통합`, `운임 급등`, `무비자 관광`, `여행 재개`는 Stage 1~2 후보를 만들 수 있다. 하지만 Stage 3-Green은 unit economics, capex 이후 FCF, 마진 지속성, 안전·운영 신뢰, 관광 소비 전환, 해운 계약 mix 같은 증거가 같이 확인되어야 한다.

예를 들면 중국 무비자 정책으로 호텔·카지노 주가가 하루 올라도 그것만으로는 Green이 아니다. 실제 면세 매출, 카지노 drop/hold, 객실 점유율, OPM, FCF가 따라와야 한다.

## 반영 내용

- `src/e2r/sector/round213_r9_loop8_mobility_transport_leisure_price_validation.py` 추가
- `src/e2r/cli/build_round213_r9_loop8_report.py` 추가
- `tests/test_round213_r9_loop8_mobility_transport_leisure_price_validation.py` 추가
- R9 Loop 8 케이스 7개를 calibration-only case record로 구조화
- reported price anchor만 있는 케이스는 full OHLC로 확장하지 않고 부분 검증 상태로 남김
- production scoring과 candidate generation은 변경하지 않음

## 케이스 요약

| case | 판단 | Stage 3 처리 |
|---|---|---|
| 현대차 | hybrid/value-up 구조 후보 | FCF·자사주 실행·OPM 확인 전 보류, 관세 마진 cut은 4C-watch |
| 기아 | hybrid 계획은 긍정이나 SDV 지연·EV target cut·capex 부담 | 소프트웨어 매출과 FCF 확인 전 보류 |
| 대한항공 | 아시아나 통합 Stage 2 | 시너지·load factor·yield·부채·FCF 확인 전 보류 |
| 제주항공 | fatal safety accident hard 4C | 여행수요 회복으로 상쇄 불가 |
| HMM | Red Sea 운임 spike cyclic success | 운임 floor·contract mix·FCF·환원 확인 전 Green 제한 |
| 호텔신라/파라다이스 | 중국 무비자 event premium | 관광 소비·카지노 drop/hold·OPM 전 보류 |
| 롯데관광개발 | 관광 redirect event premium | 카지노 utilization·ADR·FCF 전 보류 |

## Green Gate

R9 Stage 3-Green 필수 조건:

- unit_economics
- fcf_after_capex
- margin_durability
- hybrid_mix_or_load_factor_or_freight_contract_or_tourist_spend
- shareholder_return_or_deleveraging
- safety_and_operational_trust_passed
- tariff_fuel_fx_freight_normalization_stress_passed
- price_path_after_evidence

Green 금지 패턴:

- travel_reopening_only
- freight_rate_spike_only
- robotaxi_or_sdv_story_only
- tourist_arrival_policy_only
- merger_completion_without_synergy
- ev_or_ai_mobility_theme_only
- capex_heavy_localization_without_margin
- safety_failure
- tariff_margin_cut
- utilization_weak
- cycle_normalization

## 4B / 4C 보정

4B-watch는 하이브리드/value-up 급등, SDV/AI mobility 스토리 선반영, 항공 합병 완료 직후 가격 spike, Red Sea 운임 spike, 중국 무비자 관광 basket spike, 관광 redirect event처럼 가격이 실적 증거보다 먼저 움직이는 경우에 붙인다.

Hard 4C는 fatal safety accident, operational trust break, 구조적 마진 가이던스 하향, 관세 충격 미상쇄, 연료비 전가 실패, 운임 붕괴, 컨테이너 공급과잉, 통합 실패, 규제 차단, 관광 소비 실패, 카지노 utilization 붕괴, 부채·capex 부담처럼 논리 훼손이 명확할 때만 확정한다.

## 산출물

- `data/e2r_case_library/cases_r9_loop8_round213.jsonl`
- `data/sector_taxonomy/round213_r9_loop8_mobility_transport_leisure_price_validation_audit.json`
- `output/e2r_round213_r9_loop8_mobility_transport_leisure_price_validation/round213_r9_loop8_price_validation_summary.md`
- `output/e2r_round213_r9_loop8_mobility_transport_leisure_price_validation/round213_r9_loop8_case_matrix.csv`
- `output/e2r_round213_r9_loop8_mobility_transport_leisure_price_validation/round213_r9_loop8_score_adjustments.csv`
- `output/e2r_round213_r9_loop8_mobility_transport_leisure_price_validation/round213_r9_loop8_green_gate_review.md`
- `output/e2r_round213_r9_loop8_mobility_transport_leisure_price_validation/round213_r9_loop8_stage4b_4c_review.md`

## 검증

라운드213 전용 테스트와 전체 테스트를 실행한다.

```bash
PYTHONPATH=src python -m unittest tests.test_round213_r9_loop8_mobility_transport_leisure_price_validation -v
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
```

## 결론

라운드213은 모빌리티·운송·레저에서 Stage 3-Green을 막아야 하는 흔한 오판을 분리했다. 여행 재개, 운임 급등, 항공 합병, SDV/AI mobility 스토리가 있어도 unit economics와 FCF가 확인되기 전에는 Green으로 올리지 않는다.
