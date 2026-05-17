# Checkpoint 28A Round 106: R1 Loop 6 Industrial Orders / Infrastructure

## 목적

`round_106.md`는 R1 산업재·수주·인프라 팩을 Loop 6 기준으로 다시 보강한다. 이번 작업도 생산 점수 변경이 아니라 calibration/evaluation 팩이다. 케이스 레코드는 후보 생성 입력으로 쓰지 않고, 향후 shadow scoring과 가격경로 검증을 위한 구조화 자료로만 저장한다.

쉬운 예시는 다음과 같다. LS Electric 525kV 변압기 계약처럼 초고압 수출계약이 확인되면 일반 전력망 뉴스보다 강한 Stage 2 근거가 될 수 있다. 하지만 계약마진, 고객 프로젝트 지연, 납품 일정, OP/EPS 상향이 확인되지 않으면 Stage 3-Green 근거로 쓰면 안 된다.

## 반영 내용

- `src/e2r/sector/round106_r1_loop6_industrial_infra.py` 추가
- `src/e2r/cli/build_round106_r1_loop6_report.py` 추가
- `tests/test_round106_r1_loop6_industrial_infra.py` 추가
- `E2RArchetype`에 Round106 신규 보정축 추가:
  - `GRID_EHV_TRANSFORMER_EXPORT`
  - `POWER_EQUIPMENT_CAPITAL_RETURN`
  - `DATA_CENTER_GRID_FLEXIBILITY_OVERLAY`
  - `DEFENSE_US_SHIPBUILDING_PLATFORM`
  - `SHIPBUILDING_PROCUREMENT_LEADTIME`
  - `NUCLEAR_GRID_INJECTION_RIGHTS`
- 산출물 생성:
  - `data/e2r_case_library/cases_r1_loop6_round106.jsonl`
  - `data/sector_taxonomy/score_weight_profiles_round106_r1_loop6_v6.csv`
  - `output/e2r_round106_r1_loop6_industrial_infra/`

## 핵심 결과

- score target: 24개
- case candidate: 26개
- structural success: 1개
- success candidate: 11개
- event premium: 3개
- failed rerating: 1개
- Stage 4B case: 4개
- Stage 4C case: 7개
- hard gate target: 5개
- production scoring changed: false
- case records used as candidate-generation input: false

## 새로 강화한 축

### GRID_EHV_TRANSFORMER_EXPORT

525kV/765kV 같은 초고압 변압기 수출계약은 일반 전력망 수요 뉴스보다 강한 근거다. 다만 계약금액, 고객, 납품기간, 마진, OP/EPS 전환이 확인되어야 한다.

### POWER_EQUIPMENT_CAPITAL_RETURN

전력장비 수주잔고가 FCF와 자사주/배당으로 이어지면 질이 좋아진다. 동시에 시장이 이미 자본환원까지 가격에 반영했는지 4B-watch를 켜야 한다.

### DATA_CENTER_GRID_FLEXIBILITY_OVERLAY

AI 데이터센터 load flexibility 연구는 전력망 병목을 설명하는 배경 근거다. 하지만 개별 기업 매출 계약이 아니므로, 예를 들어 모델 논문만으로 장비업체 Stage 3-Green을 만들 수 없다.

### DATA_CENTER_POWER_WATER_PERMITTING

데이터센터 수요가 강해도 지역반발, 전력망 접속, 수자원, moratorium이 프로젝트 일정을 깨뜨릴 수 있다. 이 축은 긍정 점수가 아니라 RedTeam gate다.

### DEFENSE_US_SHIPBUILDING_PLATFORM

미국 조선 재건과 한국 조선 협력은 옵션 가치가 있지만 MoA만으로 반복 매출을 확정하면 안 된다. 실제 계약, yard CAPEX, 인력 병목, 마진 확인 전까지 Watch다.

### SHIPBUILDING_PROCUREMENT_LEADTIME

조선·플랜트는 수주잔고가 좋아도 pipe spool, 기자재, supplier delay가 납기와 마진을 훼손할 수 있다. 이 축은 납기·마진 gate다.

### NUCLEAR_GRID_INJECTION_RIGHTS

기존 원전 PPA·재가동은 SMR 정책 테마보다 강한 증거일 수 있다. 그래도 grid injection rights, FERC/PJM 승인, 재가동 CAPEX가 확인되지 않으면 확신을 제한한다.

## 변경하지 않은 것

- StageClassifier threshold는 변경하지 않았다.
- FeatureEngineering / scoring / staging / RedTeam production logic은 이 팩을 import하지 않는다.
- 케이스 레코드는 calibration/evaluation 전용이며 후보 생성 입력으로 쓰지 않는다.
- Stage 3-Green을 쉽게 만들기 위한 완화는 하지 않았다.
- 가격, 계약마진, stage price는 만들지 않고 `needs_price_backfill`로 남겼다.

## 실행 명령

```bash
PYTHONPATH=src python -m unittest tests.test_round106_r1_loop6_industrial_infra -v
PYTHONPATH=src python -m e2r.cli.build_round106_r1_loop6_report
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
git diff --check
```

## 검증 상태

- Round106 대상 테스트: 통과
- 전체 테스트: 통과
- `git diff --check`: 통과

## 다음 작업

Round106은 R1 산업재·수주·인프라를 더 촘촘히 나눴다. 다음 단계에서는 R2 Loop 6에서도 같은 원칙으로 “강한 구조 증거”, “Watch 증거”, “Green을 막는 RedTeam gate”를 분리해야 한다.
