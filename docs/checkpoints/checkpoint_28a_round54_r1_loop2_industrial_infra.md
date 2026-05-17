# Checkpoint 28A Round 54: R1 Loop-2 Industrial Orders / Infrastructure

## 목적

Round 54는 R13까지 1회전을 끝낸 뒤 다시 R1로 돌아온 Loop 2 보강 라운드다.
Round 41의 R1 v1.0 지도를 덮어쓰지 않고, 가격경로와 RedTeam 조건을 더 강하게 붙였다.

쉬운 예시:
철도 수주가 `as_of_date=2025-02-26`에 발표되면 Stage 2 후보는 될 수 있다.
하지만 그날 기준으로 마진, financing, 납품 스케줄, OP/EPS 상향이 확인되지 않으면 Stage 3-Green으로 올리지 않는다.

## 반영 내용

- `src/e2r/sector/archetypes.py`
  - R1 Loop-2 canonical archetype 7개 추가
- `src/e2r/sector/round54_r1_loop2_industrial_infra.py`
  - R1 Loop-2 target 12개
  - R1 Loop-2 case candidate 12개
  - Green guardrail
  - Loop-2 risk overlay
  - price/stage validation field plan
- `src/e2r/cli/build_round54_r1_loop2_report.py`
  - R1 Loop-2 리포트 생성 CLI 추가
- `tests/test_round54_r1_loop2_industrial_infra.py`
  - target, case, score profile, price field, CLI, production import guard 테스트 추가
- `data/e2r_case_library/cases_r1_loop2_round54.jsonl`
  - R1 Loop-2 case pack 생성
- `data/sector_taxonomy/score_weight_profiles_round54_r1_loop2_v2.csv`
  - R1 Loop-2 v2.0 shadow score profile 생성
- `output/e2r_round54_r1_loop2_industrial_infra/`
  - summary, case matrix, stage-date plan, guardrails, risk overlays, price field plan 생성

## 추가된 Canonical Archetype

- `GRID_TRANSFORMER_SHORTAGE`
- `AI_DATA_CENTER_POWER_EQUIPMENT`
- `DEFENSE_TECH_AUTONOMOUS_SYSTEMS`
- `DEFENSE_DRONE_COUNTER_UAS`
- `DEFENSE_AI_SOFTWARE_INTELLIGENCE`
- `RAIL_INFRASTRUCTURE`
- `SMART_FACTORY_AUTOMATION`

기존 R1 핵심 archetype도 Loop-2 target으로 유지했다.

- `CONTRACT_BACKLOG_INDUSTRIAL`
- `DEFENSE_GOVERNMENT_BACKLOG`
- `SHIPBUILDING_OFFSHORE_BACKLOG`
- `NUCLEAR_SMR_GRID_POLICY`
- `GEOPOLITICAL_RECONSTRUCTION`

## Round 54 Summary

- target_count: 12
- case_candidate_count: 12
- structural_success_count: 1
- success_candidate_count: 5
- cyclical_success_count: 1
- failed_rerating_count: 1
- stage4b_case_count: 3
- stage4c_case_count: 2
- green_possible_count: 5
- watch_yellow_first_count: 7
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## 핵심 보강점

Round 54의 핵심은 “수주가 있다”가 아니라 다음이 같이 있어야 한다는 점이다.

- 계약금액
- 계약기간
- 납품 스케줄
- 수주잔고
- 마진
- EPS/OP 상향
- 가격경로 리레이팅

그리고 Loop 2부터 다음을 강한 감점축으로 둔다.

- `project_delay`
- `capital_allocation_shock`
- `CAPA_normalization`
- `low_margin_backlog`
- `financing_failure`
- `cost_overrun`

## 대표 케이스

- `us_transformer_shortage_korea_import_case`
  - 변압기 병목은 R1 최상위 Green 가능 축으로 유지하되, 회사별 가격/실적 backfill 필요
- `ls_electric_525kv_datacenter_transformer_case`
  - 계약월은 확인되지만 정확한 계약일은 만들지 않고 `needs_contract_date_backfill`로 유지
- `ge_vernova_data_center_orders_case`
  - orders/backlog와 가격 반응이 맞지만 YTD 급등 때문에 4B-watch
- `hanwha_aerospace_romania_k9_case`
  - 방산 정부 백로그 aligned 후보
- `hanwha_aerospace_dilution_case`
  - 수주잔고가 좋아도 dilution과 자본배분 충격은 4B/4C-watch
- `hyundai_rotem_morocco_rail_case`
  - 대형 철도 수주 Stage 2 후보, margin/financing 확인 필요
- `nuscale_cfpp_cancel_case`
  - SMR 비용초과와 고객확보 실패는 hard 4C 반례
- `data_center_delay_transformer_soft_4c_case`
  - AI 데이터센터 수요가 있어도 프로젝트 지연은 전력설비 soft 4C

## 가드레일

- Production scoring/staging/red-team 로직은 변경하지 않았다.
- R1 Loop-2 v2.0 weight는 shadow/calibration material이다.
- 케이스팩은 후보 생성 input이 아니다.
- Stage 3-Green 기준을 낮추지 않았다.
- MOU, 정책 기대, prototype, 프로젝트 headline은 Green evidence가 아니다.
- 계약일, 계약금액, 마진, 가격은 확인되지 않으면 만들지 않는다.

## 생성 명령

```bash
PYTHONPATH=src python -m e2r.cli.build_round54_r1_loop2_report
```

## 검증

```bash
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest tests.test_round54_r1_loop2_industrial_infra -v
PYTHONPATH=src python -m unittest discover -s tests -v
git diff --check
```

Round54 단위 테스트는 12개 모두 통과했다.
전체 테스트는 837개 모두 통과했다.

## 다음 단계

다음 라운드는 문서 지시대로 R2 Loop 2로 넘어간다.
Round54 산출물은 향후 shadow scoring에서 `contract_quality_aligned`, `project_delay_risk`, `capital_allocation_shock`, `policy_to_contract_failed`, `crowded_rerating_4b`가 실제 후보를 어떻게 나누는지 검증하는 데 사용한다.
