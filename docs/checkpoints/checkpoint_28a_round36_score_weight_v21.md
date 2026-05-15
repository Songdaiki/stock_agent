# Checkpoint 28A Round 36: Score-Weight Validation v2.1

Round 36 반영 상태: 완료.

## 목적

`docs/round/round_36.md`의 v2.1 내용을 case library와 검증계획 리포트로 구조화했다.

이번 라운드의 핵심은 단순 점수비중 추가가 아니라, 각 archetype별로 주가 경로가 점수 가설과 맞는지 어떻게 검증할지를 붙인 것이다.

예를 들어 `GRID_TRANSFORMER_SHORTAGE`는 Green 가능형이지만, 변압기 테마명만으로는 안 된다. 수주잔고, 리드타임, 가격 전가, OP/EPS revision이 같이 보이고 Stage 2/3 이후 MFE/MAE와 밸류에이션 band가 맞게 움직이는지 확인해야 한다.

## 추가 산출물

- `src/e2r/sector/round36_score_weight_v21.py`
- `src/e2r/cli/build_round36_score_weight_report.py`
- `tests/test_round36_score_weight_v21.py`
- `data/e2r_case_library/cases_v18_round36.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round36_v21.csv`
- `output/e2r_round36_score_weight_v21/round36_score_weight_v21_summary.md`
- `output/e2r_round36_score_weight_v21/round36_case_candidate_matrix.csv`
- `output/e2r_round36_score_weight_v21/round36_green_guardrail_review.md`
- `output/e2r_round36_score_weight_v21/round36_archetype_price_validation_plan.md`
- `output/e2r_round36_score_weight_v21/round36_grid_optical_power_review.md`
- `output/e2r_round36_score_weight_v21/round36_healthcare_event_risk_review.md`
- `output/e2r_round36_score_weight_v21/round36_cycle_service_review.md`

## 요약

- target_count: 8
- case_candidate_count: 32
- success_candidate_count: 11
- counterexample_or_risk_count: 21
- stage4b_case_count: 2
- stage4c_case_count: 7
- green_possible_count: 2
- watch_yellow_first_count: 5
- redteam_first_count: 1
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## 핵심 교정

1. 전력설비/변압기는 Green 가능성이 높은 축이지만, 계약 질과 OP/EPS revision이 필수다.

2. 동물백신/방역은 반복 백신·정부 비축이면 후보지만, 질병 뉴스만 있으면 one-off event다.

3. 원격의료/온라인 정신건강은 CAC, 개인정보, DTC 광고비, impairment가 핵심 리스크다.

4. 금은/금광주는 commodity cycle로 분리한다.
   realized price, AISC, FCF, 자본환원이 같이 움직일 때만 후보가 된다.

5. 키오스크/셀프체크아웃은 장비 판매보다 유지보수·결제·소프트웨어 반복매출과 theft/loss prevention 효과를 봐야 한다.

6. 광섬유/광통신은 AI 데이터센터 직접 납품과 hyperscaler 계약이 있을 때 Green 가능성이 생긴다.

7. AI grid flexibility SW는 기술적으로 중요하지만 PoC에서 반복 매출로 넘어가는지가 핵심이다.

8. 온라인 의료/약물 플랫폼은 개인정보, 광고비, FDA/FTC, 불법 약국, liability를 강하게 감점해야 한다.

## 검증 분류

- green_possible: Stage 2/3 이후 MFE/MAE, revision 지속성, valuation band 변화를 본다.
- watch_to_green: recurring revenue, FCF 개선, retention이 확인되어야 한다.
- cycle_event: structural_success와 분리해서 cyclical_success로 표시하고 peak 이후 drawdown을 본다.
- red_flag: privacy, regulation, CAC, legal event를 승격 전 thesis-break 후보로 먼저 본다.

## 검증

실행한 명령:

```bash
PYTHONPATH=src python -m unittest tests.test_round36_score_weight_v21 -v
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m e2r.cli.build_round36_score_weight_report
PYTHONPATH=src python -m unittest discover -s tests -v
```

라운드36 단위 테스트, compileall, 리포트 생성은 통과했다.

전체 테스트는 623개를 실행했고, 기존 워킹트리의 `docs/round/round_17.md` 삭제 때문에 `test_round17_theme_absorption_audit.py` 7개가 FileNotFoundError로 실패했다. 라운드36 신규 테스트는 통과했다.

## 다음 단계

- cases_v18 가격 경로 backfill
- 각 case의 Stage 1/2/3/4B/4C 후보일자 설정
- green_possible / watch_to_green / cycle_event / red_flag 별 score-price alignment 계산
- production scoring 변경 전 shadow scoring으로 기존 deterministic score와 병렬 비교
