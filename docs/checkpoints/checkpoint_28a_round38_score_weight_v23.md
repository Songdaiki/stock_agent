# Checkpoint 28A Round 38: Score-Weight Validation v2.3

## 목적

Round 38은 AI 인프라라는 큰 이름 안에 섞여 있던 서로 다른 경제 구조를 분리한다.

예를 들어 `AI 서버 ODM/EMS`는 수요가 강해도 저마진 조립, 고객집중, 재고, 회계 신뢰도 리스크가 크다. 반대로 `advanced packaging`은 CoWoS/EMIB/HBM 병목이 강할 수 있지만, CAPA 확장 이후 병목 완화가 4B/4C 조건이 된다. `neocloud`는 take-or-pay 계약이 있어도 부채, FCF 적자, GPU 감가상각 때문에 watch-first다.

이번 작업은 production scoring 변경이 아니다. 케이스명이나 테마명은 후보 생성 근거가 아니고, 실제 매출·OP/EPS·마진·재고·계약·부채·회계 신뢰도 증거가 나중에 검증되어야 한다.

## 반영 파일

- `src/e2r/sector/round38_score_weight_v23.py`
- `src/e2r/cli/build_round38_score_weight_report.py`
- `tests/test_round38_score_weight_v23.py`
- `data/e2r_case_library/cases_v20_round38.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round38_v23.csv`
- `output/e2r_round38_score_weight_v23/round38_score_weight_v23_summary.md`
- `output/e2r_round38_score_weight_v23/round38_case_candidate_matrix.csv`
- `output/e2r_round38_score_weight_v23/round38_green_guardrail_review.md`
- `output/e2r_round38_score_weight_v23/round38_archetype_price_validation_plan.md`
- `output/e2r_round38_score_weight_v23/round38_ai_server_risk_review.md`
- `output/e2r_round38_score_weight_v23/round38_neocloud_packaging_review.md`
- `output/e2r_round38_score_weight_v23/round38_accounting_trust_overlay_review.md`

## 요약

- target_count: 8
- case_candidate_count: 28
- success_candidate_count: 9
- counterexample_or_risk_count: 19
- stage4b_case_count: 2
- stage4c_case_count: 8
- green_possible_count: 4
- watch_yellow_first_count: 2
- redteam_first_count: 2
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## 핵심 보정

- `AI_SERVER_ODM_EMS_SUPPLY_CHAIN`: Green 가능성이 있지만, 저마진 조립·고객집중·재고·회계 리스크를 별도 감시한다.
- `AI_SERVER_ACCOUNTING_GOVERNANCE_RISK`: Supermicro식 감사인 사임, 보고서 지연, 내부통제 결함은 hard 4C gate로 둔다.
- `NEOCLOUD_GPU_RENTAL`: take-or-pay는 visibility를 높이지만, 고부채·FCF 적자·GPU 감가상각 때문에 watch-first다.
- `ADVANCED_PACKAGING_COWOS_EMIB`: CoWoS/EMIB/HBM packaging 병목은 Green 가능성이 있지만, CAPEX cycle과 병목 완화는 4B/4C 조건이다.
- `SEMI_EQUIPMENT_AI_CAPEX`: AI CAPEX 수혜지만 고객사 CAPEX cycle, 수출통제, order push-out을 검증해야 한다.
- `POWER_SEMICONDUCTOR_SIC`: SiC는 장기 narrative만으로 Green을 주면 안 된다. Wolfspeed식 부채·CAPEX·수요 둔화 반례가 핵심이다.
- `OPTICAL_NETWORKING_AI_DATACENTER`: 광통신/레이저/PCB lead time 병목은 실제 주문과 OP/EPS 전환이 있어야 한다.
- `REDTEAM_ACCOUNTING_TRUST_OVERLAY`: 점수비중이 아니라 hard RedTeam gate다.

## 검증 그룹

- `high_growth_ai_hardware`: revenue-to-OP/EPS conversion, margin, inventory, customer concentration, audit drawdown
- `high_debt_infra`: debt/EBITDA, FCF margin, contract duration, customer concentration, refinancing drawdown, GPU depreciation cycle
- `ai_packaging_bottleneck`: packaging revenue, bookings/backlog, margin, CAPEX peak 이후 drawdown
- `ai_capex_equipment`: order backlog, guidance, EPS revision, order slowdown 이후 MAE
- `cycle_capex_debt`: utilization, debt/EBITDA, capex/revenue, gross margin, cash burn
- `ai_network_bottleneck`: lead time, order, OP/EPS revision, customer concentration, valuation crowding
- `hard_redteam_gate`: auditor resignation, filing delay, internal control weakness, SEC/DOJ probe

## 하지 않은 것

- StageClassifier threshold는 바꾸지 않았다.
- production feature/scoring/staging/red-team 코드는 이 라운드 팩을 import하지 않는다.
- 케이스 레코드는 후보 생성 input이 아니다.
- stage date, price, margin, contract duration, debt/EBITDA, FCF, customer concentration은 임의로 채우지 않았다.

## 실행 명령

```bash
PYTHONPATH=src python -m unittest tests.test_round38_score_weight_v23 -v
PYTHONPATH=src python -m e2r.cli.build_round38_score_weight_report
```

## 테스트 상태

라운드 38 전용 테스트는 통과했다. 전체 테스트는 기존에 삭제된 Round 17 문서 상태 때문에 별도 확인이 필요하다.
