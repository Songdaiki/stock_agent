# Checkpoint 28A Round 35: Score-Weight v2.0 Calibration Pack

Round 35 반영 상태: 완료.

## 목적

`docs/round/round_35.md`의 바이오·헬스케어 및 서비스 자동화 보강 내용을 case library와 리포트 산출물로 구조화했다.

이번 패치는 production scoring을 바꾸지 않는다. 예를 들어 GLP-1 시장이 크다는 말만으로 Stage 3-Green을 만들지 않고, 실제 처방량·보험·공급·OP/EPS 상향이 확인되어야 한다는 guardrail만 추가했다.

## 추가 산출물

- `src/e2r/sector/round35_score_weight_v20.py`
- `src/e2r/cli/build_round35_score_weight_report.py`
- `tests/test_round35_score_weight_v20.py`
- `data/e2r_case_library/cases_v17_round35.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round35_v20.csv`
- `output/e2r_round35_score_weight_v20/round35_score_weight_v20_summary.md`
- `output/e2r_round35_score_weight_v20/round35_case_candidate_matrix.csv`
- `output/e2r_round35_score_weight_v20/round35_green_guardrail_review.md`
- `output/e2r_round35_score_weight_v20/round35_biotech_commercialization_review.md`
- `output/e2r_round35_score_weight_v20/round35_glp1_regulatory_review.md`
- `output/e2r_round35_score_weight_v20/round35_service_automation_review.md`
- `output/e2r_round35_score_weight_v20/round35_price_validation_plan.md`

## 요약

- target_count: 8
- case_candidate_count: 32
- success_candidate_count: 12
- counterexample_or_risk_count: 20
- stage4b_case_count: 0
- stage4c_case_count: 7
- green_possible_count: 2
- watch_yellow_first_count: 3
- redteam_first_count: 3
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## 핵심 교정

1. 바이오시밀러는 허가만으로 Green 금지.
   PBM/보험 등재, 처방 전환, 제조원가, 마진 방어가 필요하다.

2. GLP-1은 Green 가능성이 있지만 경쟁·보험·공급·조제약·광고규제가 강한 gate다.
   예: 시장 규모가 커도 compounded alternative 때문에 가이던스가 내려가면 4C 후보가 된다.

3. 유전자치료제와 AI 신약개발은 RedTeam-first다.
   승인, 플랫폼, 후보물질 발굴만으로는 EPS/FCF 체급 변화가 아니다.

4. 컨택센터 AI는 ARR, seat expansion, retention, ROI, FCF/OPM이 있어야 Green-like 해석이 가능하다.

5. 키오스크·셀프체크아웃은 theft, 고객불만, pseudo-automation 때문에 Watch-first다.

6. 오리지널 제약사는 특허만료 이후 후속 신약 전환과 EPS/FCF 방어가 핵심이다.

7. pharma platform과 telehealth는 합법 채널, 품질관리, 규제 명확성이 없으면 Green 금지다.

## 검증

실행한 명령:

```bash
PYTHONPATH=src python -m unittest tests.test_round35_score_weight_v20 -v
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m e2r.cli.build_round35_score_weight_report
```

라운드35 단위 테스트와 compileall은 통과했다. 전체 테스트는 현재 워킹트리의 기존 라운드 문서 삭제 상태, 특히 `docs/round/round_17.md` 삭제 이슈 때문에 별도 복구 전에는 실패할 수 있다.

## 다음 단계

- cases_v17 가격 경로 backfill
- MFE/MAE/drawdown 계산
- score-price alignment 검증
- shadow scoring으로 v2.0 가설을 기존 deterministic scoring과 병렬 비교
- 충분히 검증된 archetype만 이후 production scoring 후보로 승격
