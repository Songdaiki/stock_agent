# Checkpoint 28A Round 51: R11 Policy / Geopolitical / Disaster / Event

## 목적

`docs/round/round_51.md` 내용을 R11 정책·지정학·재난·이벤트 케이스팩으로 반영했다.

이번 라운드는 Stage 3-Green 후보를 늘리기 위한 점수 변경이 아니다. 핵심 목적은 이벤트성 뉴스가 구조적 E2R로 오인되는 것을 막는 것이다.

간단한 예:

- `as_of_date=2024-08-15`에 엠폭스 비상사태 뉴스가 나오면 Stage 1 관심 신호가 될 수 있다.
- 하지만 정부 주문, stockpile 계약, 반복 조달, EPS/FCF 전환이 없으면 Stage 3-Green 근거가 아니다.
- 같은 방식으로 LK-99 같은 preprint/SNS 테마는 기술 검증, 고객, 매출이 없으면 Green이 아니라 RedTeam/4B-watch/4C 판단 대상이다.

## 추가된 코드

- `src/e2r/sector/round51_r11_policy_geopolitical_event.py`
- `src/e2r/cli/build_round51_r11_report.py`
- `tests/test_round51_r11_policy_geopolitical_event.py`

## 추가된 enum

`src/e2r/sector/archetypes.py`에 R11 canonical archetype을 추가했다.

- `NORTH_KOREA_POLICY_EVENT`
- `GEOPOLITICAL_RECONSTRUCTION`
- `CLIMATE_DISASTER_EVENT`
- `EVENT_DISEASE_PEST_DEMAND`
- `DIAGNOSTICS_INFECTIOUS_EVENT`
- `SPECULATIVE_SCIENCE_THEME`
- `ADVANCED_MATERIAL_SPECULATIVE_THEME`
- `POLICY_LOCAL_THEME`

기존 `DISASTER_REBUILD_EVENT`, `ONE_OFF_EVENT_DEMAND`, `THEME_VALUATION_OVERHEAT`도 R11 score target으로 함께 사용한다.

## 산출물

- `data/e2r_case_library/cases_r11_round51.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round51_r11_v1.csv`
- `output/e2r_round51_r11_policy_geopolitical_event/round51_r11_policy_geopolitical_event_summary.md`
- `output/e2r_round51_r11_policy_geopolitical_event/round51_r11_case_matrix.csv`
- `output/e2r_round51_r11_policy_geopolitical_event/round51_r11_stage_date_plan.csv`
- `output/e2r_round51_r11_policy_geopolitical_event/round51_r11_green_guardrails.md`
- `output/e2r_round51_r11_policy_geopolitical_event/round51_r11_event_false_positive_caps.md`
- `output/e2r_round51_r11_policy_geopolitical_event/round51_r11_price_validation_plan.md`
- `output/e2r_round51_r11_policy_geopolitical_event/round51_r11_price_fields.csv`

## 요약

- target_count: 11
- case_candidate_count: 11
- success_candidate_count: 3
- event_premium_count: 4
- overheat_count: 1
- stage4b_case_count: 2
- stage4c_case_count: 3
- green_possible_count: 0
- watch_yellow_first_count: 1
- redteam_first_count: 10
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## 반영한 핵심 판단

R11은 대부분 RedTeam-first다.

- 남북경협/금강산/개성공단: 정책 헤드라인만으로는 Green 금지.
- 우크라 재건: MOU나 회의가 아니라 실제 프로젝트, 자금, 참여 기업, 계약 경제성이 필요.
- 재난 복구: 일회성 수요일 수 있으므로 예산, 보험, 실제 주문, 반복 수요가 필요.
- 폭염/기후 이벤트: 전력망·냉각·HVAC·ESS 리서치로 연결될 수 있지만 날씨 자체는 Green 근거가 아니다.
- 전염병/해충 이벤트: 정부 주문, stockpile 계약, 반복 조달이 없으면 이벤트 프리미엄이다.
- 감염병 진단: COVID식 진단 수요는 정상화 리스크가 크다.
- 초전도체/맥신/그래핀 같은 speculative science: 기술 검증, 고객, 매출 전까지 Green 금지.
- 지역 정책 테마: 예산, 계약, 착공, 매출 가시성이 없으면 라우팅 태그일 뿐이다.

## 생산 점수 영향

생산 scoring/staging/red-team 로직은 변경하지 않았다.

이번 파일들은 calibration/evaluation material이다. 즉, 나중에 점수 가중치를 설계할 때 “이벤트성 케이스를 어떻게 막을지” 참고하는 자료다.

## 검증

실행한 명령:

```bash
PYTHONPATH=src python -m e2r.cli.build_round51_r11_report
PYTHONPATH=src python -m unittest tests.test_round51_r11_policy_geopolitical_event -v
```

결과:

- Round51 R11 테스트 11개 통과.

전체 테스트 결과는 최종 커밋 전 별도로 확인한다.
