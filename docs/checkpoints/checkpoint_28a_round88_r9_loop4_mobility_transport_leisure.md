# Checkpoint 28A Round 88 R9 Loop 4 Mobility/Transport/Leisure

## 반영 범위

`docs/round/round_88.md`의 R9 Loop 4 내용을 calibration pack으로 반영했다. 이 작업은 생산 scoring 변경이 아니라, 모빌리티·운송·레저 대섹터의 archetype, 케이스, 가격 검증 필드, RedTeam gate를 확장하는 작업이다.

간단한 예시: `Part 135`는 eVTOL 운항사업자 자격에 가깝다. 기체 `Type Certification`, 상업 매출, unit economics가 아니므로 Stage 3-Green 근거로 쓰면 안 된다.

## 생성/수정 파일

- `src/e2r/sector/round88_r9_loop4_mobility_transport_leisure.py`
- `src/e2r/cli/build_round88_r9_loop4_report.py`
- `tests/test_round88_r9_loop4_mobility_transport_leisure.py`
- `data/e2r_case_library/cases_r9_loop4_round88.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round88_r9_loop4_v4.csv`
- `output/e2r_round88_r9_loop4_mobility_transport_leisure/`

## 핵심 변경

- R9 target을 19개에서 25개로 확장했다.
- 새 RedTeam/gate archetype을 반영했다:
  - `AUTO_TARIFF_LOCALIZATION`
  - `ROBOTAXI_OPERATIONAL_REALITY_CHECK`
  - `ROBOTAXI_SAFETY_REGULATORY_OVERLAY`
  - `AIRLINE_INTEGRATION_SCALE`
  - `EV_RENTAL_UNIT_ECONOMICS`
  - `EVTOL_CERTIFICATION_CASH_BURN`
- 케이스 후보 16개를 Round 88 우선 검증표에 맞췄다.
- 가격 검증 필드에 `wait_time_minutes`, `ride_completion_rate`, `local_production_capacity`, `evtol_cash_burn` 등을 추가했다.
- 생산 scoring/staging/RedTeam 로직은 변경하지 않았다.

## 요약 수치

- target_count: 25
- case_candidate_count: 16
- success_candidate_count: 4
- cyclical_success_count: 1
- event_premium_count: 2
- stage4b_case_count: 8
- stage4c_case_count: 7
- green_possible_count: 2
- watch_yellow_first_count: 14
- redteam_first_count: 9
- gate_only_target_count: 6

## Green Guardrail

R9에서 `수요 회복`, `관광 정책`, `운임 상승`, `로보택시 출시`, `eVTOL 인증 일부 단계`는 그 자체로 Green 근거가 아니다.

예를 들어 Tesla robotaxi rollout은 도시 확장 뉴스가 있어도 긴 대기시간, misrouting, 제한된 운행영역이 있으면 `ROBOTAXI_OPERATIONAL_REALITY_CHECK`로 분리한다. 즉, “도시 진출”이 아니라 “실제 ride completion과 unit economics”를 봐야 한다.

## 검증

실행한 targeted test:

```bash
PYTHONPATH=src python -m unittest tests.test_round88_r9_loop4_mobility_transport_leisure -v
```

결과: 통과.

전체 테스트와 diff check는 커밋 전 최종 검증에서 별도로 실행한다.
