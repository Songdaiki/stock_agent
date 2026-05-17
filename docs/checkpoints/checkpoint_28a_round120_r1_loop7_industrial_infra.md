# Checkpoint 28A Round 120: R1 Loop 7 Industrial Orders / Infrastructure

## 목적

Round 120은 R13 Loop 6 이후 다시 R1 산업재·수주·인프라로 돌아온 Loop 7 팩이다. 이번 라운드의 핵심은 단순히 “수주 뉴스가 있다”가 아니라, 점수표가 실제 Stage를 어떻게 잡았고 그 Stage가 실제 가격경로와 맞았는지를 더 명확하게 기록하는 것이다.

쉬운 예시는 다음과 같다.

- GE Vernova는 orders, backlog, guidance, price reaction이 같이 나와 `score -> stage -> price`가 잘 맞은 사례다. 다만 이미 크게 리레이팅되었으므로 4B-watch가 붙는다.
- LS Electric 525kV 변압기 계약과 현대로템 모로코 철도 수주는 Stage 2 evidence가 강하다. 하지만 margin, OP/EPS/FCF, 공식 가격경로 backfill 전까지 Stage 3-Green은 제한한다.
- 한화에어로스페이스는 방산 backlog가 좋아도 증자와 희석 shock이 나오면 stage_after_redteam이 강등되어야 하는 사례다.
- HD Hyundai-Huntington 조선 협력은 MoU/MoA 단계이므로 event/watch이지 Green이 아니다.

## 반영 내용

- R1 Loop 7 산업재·수주·인프라 팩을 추가했다.
- 기존 R1 Loop 6의 전력망, 변압기, 방산, 조선, 원전, 철도, 재건 후보 구조를 유지하면서 Round 120 문서의 stage/price validation 중심으로 확장했다.
- R1 v7 기본 점수표를 데이터화했다.
- Stage 1/2/3/4B/4C cap matrix를 추가했다.
- 핵심 6개 케이스에 대해 score → stage → price alignment 표를 추가했다.
- 생산 scoring, staging, RedTeam 로직은 변경하지 않았다.
- 케이스 레코드는 candidate generation 입력으로 쓰지 않는다.

## 산출물

- `src/e2r/sector/round120_r1_loop7_industrial_infra.py`
- `src/e2r/cli/build_round120_r1_loop7_report.py`
- `tests/test_round120_r1_loop7_industrial_infra.py`
- `data/e2r_case_library/cases_r1_loop7_round120.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round120_r1_loop7_v7.csv`
- `output/e2r_round120_r1_loop7_industrial_infra/round120_r1_loop7_industrial_infra_summary.md`
- `output/e2r_round120_r1_loop7_industrial_infra/round120_r1_loop7_case_matrix.csv`
- `output/e2r_round120_r1_loop7_industrial_infra/round120_r1_loop7_stage_date_plan.csv`
- `output/e2r_round120_r1_loop7_industrial_infra/round120_r1_loop7_green_guardrails.md`
- `output/e2r_round120_r1_loop7_industrial_infra/round120_r1_loop7_risk_overlays.md`
- `output/e2r_round120_r1_loop7_industrial_infra/round120_r1_loop7_price_validation_plan.md`
- `output/e2r_round120_r1_loop7_industrial_infra/round120_r1_loop7_price_fields.csv`
- `output/e2r_round120_r1_loop7_industrial_infra/round120_r1_loop7_base_score_weights.csv`
- `output/e2r_round120_r1_loop7_industrial_infra/round120_r1_loop7_stage_caps.csv`
- `output/e2r_round120_r1_loop7_industrial_infra/round120_r1_loop7_score_stage_price_alignment.csv`
- `output/e2r_round120_r1_loop7_industrial_infra/round120_r1_loop7_score_stage_price_alignment.md`

## 요약 수치

- target_count: 24
- case_candidate_count: 26
- base_score_component_count: 7
- stage_cap_count: 5
- score_stage_price_alignment_count: 6
- structural_success_count: 1
- success_candidate_count: 11
- cyclical_success_count: 0
- event_premium_count: 3
- failed_rerating_count: 1
- stage4b_case_count: 4
- stage4c_case_count: 7
- green_possible_count: 5
- watch_yellow_first_count: 12
- redteam_first_count: 7
- hard_gate_target_count: 5
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## R1 v7 기본 점수표

```text
EPS/FCF revision 가능성        25
계약·수주잔고 visibility        24
병목·가격결정력                 20
시장 오해·리레이팅 gap          12
valuation room / 4B 여지         8
capital discipline / FCF 전환     6
정보 신뢰도 / disclosure detail   5
```

이 점수표는 바로 production scoring에 적용하지 않는다. 지금은 calibration/report material이다.

## Stage Cap

- Stage 1 cap: 최대 45점. 산업 뉴스, 정책 뉴스, MoU, macro shortage만 있는 경우다.
- Stage 2 cap: 최대 70점. 계약금액, 고객, 기간, 납품스케줄, backlog/guidance 일부가 확인된 경우다.
- Stage 3: 70점 이상 가능. OP/EPS/FCF, margin, FCF conversion, price-path alignment가 필요하다.
- Stage 4B: 구조는 좋지만 이미 리레이팅이 과밀한 monitoring 구간이다.
- Stage 4C: dilution, 계약취소, 납기, 저마진, 인허가, 정책 shock 같은 hard RedTeam이다.

## Green 차단 원칙

R1 Loop 7에서 Green을 만들면 안 되는 경우:

- 수주 뉴스만 있고 OP/EPS/FCF 전환이 없는 경우
- MoU/MoA only인 경우
- OpenDART list-only 공시이고 detail 필드가 없는 경우
- 철도 대형계약이지만 margin, warranty, FX, financing이 불명확한 경우
- 방산 수주가 좋아도 대규모 희석이나 자본배분 shock이 있는 경우
- 전력장비 성공 사례라도 valuation room이 이미 4B 수준으로 줄어든 경우

## 검증

실행 명령:

```bash
PYTHONPATH=src python -m unittest tests.test_round120_r1_loop7_industrial_infra -v
PYTHONPATH=src python -m e2r.cli.build_round120_r1_loop7_report
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
git diff --check
```

검증 결과:

- Round 120 전용 테스트: 13개 통과
- 전체 테스트: 1559개 통과
- diff whitespace check: 통과

## 다음 단계

다음 순서는 R2 Loop 7 AI·반도체·전자부품이다. Round 120에서 추가한 `score -> stage -> price` 검증 포맷을 R2에서도 유지해야 한다. 예를 들어 AI/HBM은 이름만으로 점수를 주지 않고, LTA, 선수금, CAPA 제약, 컨센서스 상향, 실제 가격경로까지 같이 확인해야 한다.
