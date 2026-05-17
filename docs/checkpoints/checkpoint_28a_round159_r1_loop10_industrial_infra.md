# Checkpoint 28A Round 159 R1 Loop 10 Industrial Infrastructure

## 목적

`docs/round/round_159.md`의 R1 Loop 10 내용을 캘리브레이션 팩으로 반영했다.

이번 라운드는 산업재·인프라에서 단순한 수주 증가가 아니라 다음 흐름이 실제로 이어지는지를 분리한다.

```text
계약/백로그/승인 게이트
-> 매출·마진·EPS·FCF 전환
-> 가격 경로 정합성
-> 4B/4C RedTeam 감시
```

쉬운 예로, 변압기 쇼티지 뉴스만 있으면 Stage 1이다. 계약금액·납기·고객·마진이 보이면 Stage 2가 될 수 있고, 그 계약이 OP/EPS/FCF 상향과 가격 경로까지 맞아야 Stage 3 후보가 된다.

## 반영 내용

- `src/e2r/sector/round159_r1_loop10_industrial_infra.py` 추가
- `src/e2r/cli/build_round159_r1_loop10_report.py` 추가
- `tests/test_round159_r1_loop10_industrial_infra.py` 추가
- Loop 10 원문 핵심 target 15개와 보조 risk overlay 9개를 함께 기록
- Round 159 전용 case pack과 score profile 생성

## 핵심 변경점

- v10 기본 점수표를 별도 캘리브레이션 자료로 기록
  - EPS/FCF: 25
  - 계약·백로그 visibility: 22
  - 병목·pricing power: 18
  - capital discipline / dilution: 10
  - mispricing: 9
  - valuation room: 7
  - disclosure confidence / RedTeam: 9
- `POWER_EQUIPMENT_BACKLOG_TO_FCF`, `GAS_TURBINE_POWER_BACKLOG`, `GRID_EHV_TRANSFORMER_EXPORT`, `NUCLEAR_EXISTING_PPA_RESTART`를 핵심 검증 축으로 유지
- 원문 표의 15개 target 외에 `NUCLEAR_GRID_INJECTION_RIGHTS`, `DATA_CENTER_POWER_WATER_PERMITTING`, `CAPITAL_ALLOCATION_DILUTION_OVERLAY` 같은 보조 overlay를 별도 target으로 보존했다. 예를 들어 Constellation은 PPA만으로 Green이 아니라 grid injection rights가 통과해야 하므로, 이 보조 gate가 필요하다.
- 신규 반례 추가
  - `siemens_orders_profit_miss_case`: 주문/백로그가 좋아도 매출·이익 미스면 Green 금지
  - `oklo_smr_no_revenue_watch_case`: SMR 규제 milestone만으로는 Stage 3 금지
- score-stage-price alignment 표를 6개에서 10개로 확대
- Stage cap에 `profit_miss`, `FSS correction`, `no revenue SMR`, `PPA/grid approval gate`를 명시

## 산출 요약

| 항목 | 값 |
| --- | ---: |
| score target | 24 |
| case candidate | 28 |
| base score component | 7 |
| stage cap | 5 |
| score-stage-price alignment | 10 |
| structural success | 1 |
| success candidate | 11 |
| event premium | 3 |
| failed rerating | 3 |
| Stage 4B case | 4 |
| Stage 4C case | 7 |
| Green possible target | 5 |
| hard gate target | 5 |

해석하면, 이번 팩은 “수주가 있다”를 “Stage 3 가능”으로 바로 바꾸지 않는다.
예를 들어 LS Electric 525kV 계약은 고객·전압·계약금액·납품기간이 있어 Stage 2 근거는 강하지만,
OP/EPS/FCF와 가격경로가 확인되기 전까지 Stage 3는 제한한다.

## 산출물

- `data/e2r_case_library/cases_r1_loop10_round159.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round159_r1_loop10_v10.csv`
- `output/e2r_round159_r1_loop10_industrial_infra/round159_r1_loop10_industrial_infra_summary.md`
- `output/e2r_round159_r1_loop10_industrial_infra/round159_r1_loop10_case_matrix.csv`
- `output/e2r_round159_r1_loop10_industrial_infra/round159_r1_loop10_score_stage_price_alignment.md`

## 안전장치

- production scoring은 변경하지 않았다.
- case library는 candidate-generation input이 아니다.
- 종목명 하드코딩으로 Stage를 올리는 로직은 추가하지 않았다.
- 계약금액, 마진, stage price, FCF는 없는 값을 만들지 않는다.

## 검증

```bash
PYTHONPATH=src python -m unittest tests/test_round159_r1_loop10_industrial_infra.py -v
PYTHONPATH=src python -m e2r.cli.build_round159_r1_loop10_report
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
```

전용 테스트와 전체 테스트가 통과했다.
