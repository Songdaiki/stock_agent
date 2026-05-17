# Checkpoint 28A Round 115 R10 Loop-6 Construction / Real Estate / Building Materials

## 목적

Round 115는 R10 건설·부동산·건자재 케이스 라이브러리의 Loop-6 확장이다. 생산 scoring이나 StageClassifier는 바꾸지 않고, PF·REIT·데이터센터·콜드체인·건자재·재건 테마를 calibration/evaluation 자료로만 정리했다.

쉬운 예시:
AI 데이터센터 REIT IPO가 있어도 자산 취득, binding tenant lease, NOI/AFFO, 전력·수자원 확보가 없으면 Stage 3-Green 근거가 아니다. 이것은 “좋은 테마”와 “검증된 현금흐름”을 분리하기 위한 장치다.

## 반영 내용

- `src/e2r/sector/round115_r10_loop6_construction_real_estate_materials.py` 추가
- `src/e2r/cli/build_round115_r10_loop6_report.py` 추가
- `tests/test_round115_r10_loop6_construction_real_estate_materials.py` 추가
- R10 Loop-6 신규 archetype enum 추가
- `data/e2r_case_library/cases_r10_loop6_round115.jsonl` 생성
- `data/sector_taxonomy/score_weight_profiles_round115_r10_loop6_v6.csv` 생성
- `output/e2r_round115_r10_loop6_construction_real_estate_materials/` 리포트 생성

## 신규 Archetype

- `DATA_CENTER_SPONSOR_PREMIUM_PIPELINE`
- `AI_DATA_CENTER_POWER_CAMPUS`
- `AI_DATA_CENTER_NO_REVENUE_NO_TENANT`
- `DATA_CENTER_WATER_RIGHTS_REFERENDUM`
- `DATA_CENTER_RATEPAYER_UTILITY_COST_OVERLAY`
- `PRECAST_WALLING_BUILDING_SOLUTIONS`

## 요약 수치

- target_count: 28
- case_candidate_count: 25
- success_candidate_count: 6
- event_premium_count: 5
- stage4b_case_count: 13
- stage4c_case_count: 7
- green_possible_count: 6
- watch_yellow_first_count: 8
- redteam_first_count: 14
- gate_only_target_count: 9

## 핵심 Guardrail

- PF 지원책은 Stage 1 relief다. PF exposure 감소, refinancing 성공, cash conversion 개선 전까지 Green 근거가 아니다.
- 고배당 REIT는 occupancy, NOI/AFFO, dividend coverage, LTV, funding cost를 확인해야 한다.
- 데이터센터 REIT는 자산·tenant·NOI/AFFO·전력·수자원·AFFO integrity를 통과해야 한다.
- sponsor premium과 acquisition pipeline은 Stage 1/2 근거일 뿐 현재 cash flow가 아니다.
- 무매출 AI power campus, non-binding LOI, tenant 부재는 RedTeam gate다.
- water rights, referendum, local moratorium, ratepayer utility cost는 데이터센터 실물 프로젝트의 timing을 깨뜨릴 수 있다.
- 건자재는 가격인상만으로 부족하다. 출하량, 원가율, OPM, FCF가 같이 확인되어야 한다.
- precast/walling/water-management M&A는 synergy, margin, FCF, leverage가 확인되기 전까지 Watch다.

## 생성 리포트

- `output/e2r_round115_r10_loop6_construction_real_estate_materials/round115_r10_loop6_construction_real_estate_materials_summary.md`
- `output/e2r_round115_r10_loop6_construction_real_estate_materials/round115_r10_loop6_case_matrix.csv`
- `output/e2r_round115_r10_loop6_construction_real_estate_materials/round115_r10_loop6_stage_date_plan.csv`
- `output/e2r_round115_r10_loop6_construction_real_estate_materials/round115_r10_loop6_green_guardrails.md`
- `output/e2r_round115_r10_loop6_construction_real_estate_materials/round115_r10_loop6_risk_overlays.md`
- `output/e2r_round115_r10_loop6_construction_real_estate_materials/round115_r10_loop6_price_validation_plan.md`
- `output/e2r_round115_r10_loop6_construction_real_estate_materials/round115_r10_loop6_price_fields.csv`

## 검증

- `PYTHONPATH=src python -m unittest tests.test_round115_r10_loop6_construction_real_estate_materials -v`

전체 테스트는 커밋 전 별도 실행한다.

## 생산 영향

- production scoring 변경 없음
- case records를 candidate-generation input으로 사용하지 않음
- Stage 3-Green 기준 완화 없음
- 가격 데이터는 아직 backfill 필요
