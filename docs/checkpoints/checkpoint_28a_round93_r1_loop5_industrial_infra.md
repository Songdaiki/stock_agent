# Checkpoint 28A Round 93: R1 Loop 5 Industrial Orders / Infrastructure

## 목적

`round_93.md`는 R1 산업재·수주·인프라 팩을 Loop 5 기준으로 다시 좁힌다. 섹터 점수를 바로 바꾸는 작업이 아니라, 전력망·데이터센터 전력설비·방산·조선·철도·원전 후보에서 어떤 증거가 Stage 3 후보로 이어질 수 있고, 어떤 증거는 Yellow/RedTeam에 머물러야 하는지 정리하는 calibration 팩이다.

쉬운 예시는 다음과 같다. 변압기 수요가 강하고 수주 공시가 있어도 계약금액, 고객, 기간, 납품 일정, 마진이 확인되지 않으면 Stage 3-Green으로 올리지 않는다. 이 경우 `DISCLOSURE_CONFIDENCE_CAP`으로 확신을 제한하고, detail fetch와 파싱 결과를 기다린다.

## 반영 내용

- `src/e2r/sector/round93_r1_loop5_industrial_infra.py` 추가
- `src/e2r/cli/build_round93_r1_loop5_report.py` 추가
- `tests/test_round93_r1_loop5_industrial_infra.py` 추가
- `E2RArchetype`에 `GRID_SUPPLY_SLOT_PREBUY`, `GAS_TURBINE_POWER_BACKLOG` 추가
- 산출물 생성:
  - `data/e2r_case_library/cases_r1_loop5_round93.jsonl`
  - `data/sector_taxonomy/score_weight_profiles_round93_r1_loop5_v5.csv`
  - `output/e2r_round93_r1_loop5_industrial_infra/`

## 핵심 결과

- score target: 19개
- case candidate: 19개
- structural success: 1개
- success candidate: 10개
- event premium: 2개
- failed rerating: 1개
- Stage 4B case: 3개
- Stage 4C case: 3개
- hard gate target: 3개
- production scoring changed: false
- case records used as candidate-generation input: false

## 새로 강화한 축

### GRID_SUPPLY_SLOT_PREBUY

변압기나 전력설비는 단순 수요보다 생산 슬롯 선점, 선수금, 고객 프로젝트 일정이 더 강한 visibility가 될 수 있다. 다만 슬롯 선점이 실제 매출·마진·EPS로 전환되지 않으면 Green 근거가 아니다.

### GAS_TURBINE_POWER_BACKLOG

AI 데이터센터 전력 수요가 가스터빈과 전력설비 수주로 이어지는 경로를 별도 archetype으로 분리했다. 전력 backlog와 가이던스 상향은 Stage 2 근거가 될 수 있지만, 관세 비용, 풍력 부문 손실, 납기 지연, 프로젝트 취소 리스크를 같이 봐야 한다.

### DISCLOSURE_CONFIDENCE_CAP

OpenDART 목록형 공시는 Layer 1 후보를 만들 수 있지만, detail이 없으면 Stage 3 확신을 제한한다. 예를 들어 “단일판매·공급계약체결” 제목만 있고 금액·상대방·기간·마진이 없으면 아직 계약 품질을 안다고 볼 수 없다.

## 추가 케이스

대표적으로 다음 케이스를 추가했다.

- `ls_electric_525kv_us_datacenter_transformer_case`
- `ge_vernova_power_backlog_turbine_case`
- `us_power_demand_record_eia_case`

기존 R1 Loop 4 케이스도 유지하되, Loop 5에서는 공시 detail, 슬롯 visibility, 가스터빈 backlog, 데이터센터 허가 지연, 방산 희석 리스크를 더 명시적으로 분리했다.

## 변경하지 않은 것

- StageClassifier threshold는 변경하지 않았다.
- FeatureEngineering / scoring / staging / RedTeam production logic은 이 팩을 import하지 않는다.
- 케이스 레코드는 calibration/evaluation 전용이며 후보 생성 입력으로 쓰지 않는다.
- Stage 3-Green을 쉽게 만들기 위한 완화는 하지 않았다.

## 실행 명령

```bash
PYTHONPATH=src python -m unittest tests.test_round93_r1_loop5_industrial_infra -v
PYTHONPATH=src python -m e2r.cli.build_round93_r1_loop5_report
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
git diff --check
```

## 검증 상태

- Round93 대상 테스트: 통과
- 전체 테스트: 통과
- `git diff --check`: 통과

## 다음 작업

R1 Loop 5는 산업재·수주·인프라의 증거 기준을 더 촘촘하게 만들었다. 다음 단계에서는 다른 라운드 팩에도 같은 방식으로 “좋은 신호”, “Green을 막는 신호”, “가격만 오른 신호”를 분리하고, 최종적으로는 생산 점수 변경 전에 shadow score로 비교해야 한다.
