# Checkpoint 28A Round 172: R1 Loop 11 Korea Industrial Orders / Infrastructure

## 목적

`docs/round/round_172.md`의 R1 Loop 11 내용을 calibration pack으로 반영했다.
이번 라운드는 산업재·수주·인프라를 국장 중심으로 다시 잡고, 두 가지 질문을 강하게 추가한다.

1. 주가 대폭 상승 전에 Stage 3 후보로 포착할 수 있었는가?
2. 상승 릴레이가 끝나기 전에 Stage 4B 또는 4C로 식힐 수 있는가?

쉬운 예로, HD현대일렉트릭은 변압기 병목과 OP/EPS/FCF 전환이 맞으면 Stage 3 후보가 될 수 있다.
하지만 이미 K-변압기 narrative가 과밀해졌다면 같은 후보에도 4B-watch를 붙여야 한다.
반대로 HD현대미포 LOI는 본계약이 아니므로 주가가 움직여도 Stage 3로 올리지 않는다.

## 반영 파일

- `src/e2r/sector/round172_r1_loop11_industrial_infra.py`
- `src/e2r/cli/build_round172_r1_loop11_report.py`
- `tests/test_round172_r1_loop11_industrial_infra.py`
- `data/e2r_case_library/cases_r1_loop11_round172.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round172_r1_loop11_v11.csv`
- `output/e2r_round172_r1_loop11_industrial_infra/`

## Loop 11 target

원문 canonical target 11개와 보조 legal gate 1개를 분리했다.

| target | 역할 |
| --- | --- |
| `GRID_TRANSFORMER_SHORTAGE_KOREA` | HD현대일렉트릭/효성중공업/일진전기형 K-변압기 병목 |
| `GRID_US_LOCALIZATION_CAPA` | HICO, 미국 현지 생산, HVDC/CAPA visibility |
| `POWER_EQUIPMENT_BACKLOG_TO_FCF_KOREA` | 수주잔고가 FCF/OPM으로 전환되는지 확인 |
| `SHIPBUILDING_US_PLATFORM_RESTRUCTURING` | 미국 조선 재건, 합병, 구조재편 Stage 2 |
| `SHIP_MRO_RECURRING_PLATFORM` | 선박 MRO/retrofit 반복 매출, IPO 4B 감시 |
| `NUCLEAR_EXPORT_PREFERRED_BIDDER` | 체코 원전 preferred bidder는 Stage 2, 계약 전 Green 금지 |
| `DEFENSE_AIRCRAFT_EXPORT_BACKLOG` | KAI FA-50 같은 고객/금액/납기 있는 Stage 2 |
| `DEFENSE_INTERCEPTOR_COMBAT_VALIDATION` | LIG넥스원 전투검증 + price path는 Stage 2.5 |
| `GEOPOLITICAL_SHIPBUILDING_SANCTION_OVERLAY` | 한화오션 중국 제재 같은 hard RedTeam |
| `MOU_LOI_NOT_CONTRACT` | LOI/MOU/협의는 본계약 전 Stage 3 금지 |
| `DISCLOSURE_CONFIDENCE_CAP` | 공시 detail 부족 시 Stage 3 confidence cap |
| `NUCLEAR_EXPORT_LEGAL_GATE` | 항소·계약체결 금지·IP 이슈 hard gate |

## R1 Loop 11 기본 점수축

| component | points |
| --- | ---: |
| EPS/FCF/OPM conversion | 24 |
| contract/backlog/customer visibility | 20 |
| bottleneck/pricing power | 18 |
| early price-path validation | 12 |
| capital discipline/dilution | 8 |
| disclosure confidence/RedTeam | 8 |
| valuation room / 4B runway | 10 |

이번에 새로 중요한 축은 `early_price_path_validation`이다.
예를 들어 Stage 2 이후 60일 안에 +20% MFE가 나오고 OP/EPS revision도 붙으면 Stage 3 조기 포착 후보가 된다.
반대로 Stage 2 이후 120일 MFE가 +80%를 넘고 리포트가 과밀해지면 4B-watch로 식힌다.

## 케이스 요약

| case | 판정 |
| --- | --- |
| HD현대일렉트릭 | Stage 3 후보 + 4B-watch |
| 효성중공업 | HICO/HVDC Stage 2.5, OP/EPS와 margin backfill 필요 |
| 두산에너빌리티/한전기술/한전KPS | 체코 preferred bidder Stage 2, 계약·scope 전 Green 금지 |
| HD현대중공업·HD현대미포 합병 | Stage 2 + event/4B-watch |
| HD현대마린솔루션 | MRO recurring platform 가능성 + IPO 4B-watch |
| 한국항공우주 | FA-50 필리핀 계약 Stage 2, margin/후속계약 전 Green 금지 |
| LIG넥스원 | combat validation + price path Stage 2.5, 실제 수출계약 전 Green 금지 |
| 한화오션 | 미국 조선/MRO option이 있어도 중국 제재는 hard RedTeam |
| HD현대미포 LOI-only | LOI/협의는 본계약 전 Stage 3 금지 |
| 두산에너빌리티 legal gate | preferred bidder rally를 항소/계약체결 금지가 cap |

## 산출 요약

| 항목 | 값 |
| --- | ---: |
| target | 12 |
| source canonical target | 11 |
| case candidate | 12 |
| base score component | 7 |
| stage cap | 6 |
| score-stage-price alignment | 10 |
| structural success | 1 |
| success candidate | 7 |
| event premium | 1 |
| Stage 4B case | 5 |
| Stage 4C case | 2 |
| hard gate target | 3 |

## 핵심 가드레일

- Round 172 case pack은 candidate generation input이 아니다.
- production scoring/staging/RedTeam 로직은 변경하지 않았다.
- Stage 3-Green은 수주 뉴스가 아니라 OP/EPS/FCF, margin, 수주잔고 질, 가격경로, detail confidence가 같이 맞을 때만 가능하다.
- preferred bidder, LOI, MOU, merger, IPO premium, combat validation은 단독으로 Green을 만들 수 없다.
- 법적 gate, 제재, 계약 취소/정정, 대규모 희석, 공시 detail 부족은 4C 또는 cap으로 둔다.

## 산출물

- `round172_r1_loop11_industrial_infra_summary.md`
- `round172_r1_loop11_case_matrix.csv`
- `round172_r1_loop11_stage_date_plan.csv`
- `round172_r1_loop11_green_guardrails.md`
- `round172_r1_loop11_risk_overlays.md`
- `round172_r1_loop11_price_validation_plan.md`
- `round172_r1_loop11_price_fields.csv`
- `round172_r1_loop11_base_score_weights.csv`
- `round172_r1_loop11_stage_caps.csv`
- `round172_r1_loop11_score_stage_price_alignment.csv`
- `round172_r1_loop11_score_stage_price_alignment.md`

## 검증

- `PYTHONPATH=src python -m e2r.cli.build_round172_r1_loop11_report` 통과.
- `PYTHONPATH=src python -m unittest tests/test_round172_r1_loop11_industrial_infra.py -v` 통과.
- `PYTHONPATH=src python -m compileall -q src tests` 통과.
- `PYTHONPATH=src python -m unittest discover -s tests -v` 통과. `2215 tests`.
- `git diff --check` 통과.
