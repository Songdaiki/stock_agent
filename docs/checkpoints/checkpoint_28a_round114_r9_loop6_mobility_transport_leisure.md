# Checkpoint 28A Round 114 R9 Loop-6 Mobility/Transport/Leisure

## 목적

Round 114는 모빌리티·운송·레저 케이스 라이브러리의 Loop-6 확장이다. 생산 점수나 StageClassifier는 바꾸지 않고, 향후 섹터별 scoring shadow test에 쓸 calibration/evaluation 자료만 추가했다.

쉬운 예시:
`Part 135`는 항공 운항자 관련 이정표일 수 있지만, 기체 타입 인증이나 상업 매출 증거는 아니다. 그래서 eVTOL Green 근거가 아니라 RedTeam 게이트로 분리했다.

## 반영 내용

- `src/e2r/sector/round114_r9_loop6_mobility_transport_leisure.py` 추가
- `src/e2r/cli/build_round114_r9_loop6_report.py` 추가
- `tests/test_round114_r9_loop6_mobility_transport_leisure.py` 추가
- `src/e2r/sector/archetypes.py`에 Round 114 신규 archetype 추가
- `data/e2r_case_library/cases_r9_loop6_round114.jsonl` 생성
- `data/sector_taxonomy/score_weight_profiles_round114_r9_loop6_v6.csv` 생성
- `output/e2r_round114_r9_loop6_mobility_transport_leisure/` 리포트 생성

## 신규 Archetype

- `AUTO_US_LOCALIZATION_LABOR_VISA_RISK`
- `AV_CRASH_DISCLOSURE_PROBE_OVERLAY`
- `AUTONOMOUS_TRUCKING_PAID_FREIGHT_MILESTONE`
- `TOURISM_POLICY_EVENT`
- `PART135_NOT_TYPE_CERTIFICATION`

## 요약 수치

- target_count: 33
- case_candidate_count: 20
- success_candidate_count: 8
- cyclical_success_count: 1
- event_premium_count: 2
- stage4b_case_count: 10
- stage4c_case_count: 7
- green_possible_count: 2
- watch_yellow_first_count: 17
- redteam_first_count: 14
- gate_only_target_count: 10

## 핵심 Guardrail

- 미국 현지화는 공장 ramp-up, 숙련 노동, 비자, 품질비용 리스크를 통과해야 tariff benefit으로 본다.
- AV crash disclosure와 NHTSA probe는 로보택시 확장 서사를 막는 RedTeam evidence다.
- paid driverless freight는 Stage 2 근거가 될 수 있지만, 반복 고객·utilization·cost per mile·보험비가 없으면 Green 근거가 아니다.
- 관광 정책 이벤트는 관광객 지출, 카지노 drop amount, 면세 ASP, RevPAR, OPM이 확인되기 전까지 Stage 1 성격이다.
- Part 135는 type certification, production certification, scaled commercial revenue가 아니다.

## 생성 리포트

- `output/e2r_round114_r9_loop6_mobility_transport_leisure/round114_r9_loop6_mobility_transport_leisure_summary.md`
- `output/e2r_round114_r9_loop6_mobility_transport_leisure/round114_r9_loop6_case_matrix.csv`
- `output/e2r_round114_r9_loop6_mobility_transport_leisure/round114_r9_loop6_stage_date_plan.csv`
- `output/e2r_round114_r9_loop6_mobility_transport_leisure/round114_r9_loop6_green_guardrails.md`
- `output/e2r_round114_r9_loop6_mobility_transport_leisure/round114_r9_loop6_risk_overlays.md`
- `output/e2r_round114_r9_loop6_mobility_transport_leisure/round114_r9_loop6_price_validation_plan.md`
- `output/e2r_round114_r9_loop6_mobility_transport_leisure/round114_r9_loop6_price_fields.csv`

## 검증

- `PYTHONPATH=src python -m unittest tests.test_round114_r9_loop6_mobility_transport_leisure -v`

전체 테스트는 커밋 전 별도 실행한다.

## 생산 영향

- production scoring 변경 없음
- case records를 candidate-generation input으로 사용하지 않음
- Stage 3-Green 기준 완화 없음
- 가격 데이터는 아직 backfill 필요
