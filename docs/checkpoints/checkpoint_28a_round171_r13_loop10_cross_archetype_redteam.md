# Checkpoint 28A Round 171: R13 Loop 10 Cross-Archetype RedTeam / 4B / Price Validation

## 목적

`docs/round/round_171.md`의 R13 Loop 10 내용을 별도 calibration pack으로 반영했다.
R13은 새 섹터가 아니라 R1~R12 후보를 마지막에 검문하는 공통 overlay다.

쉬운 예로, SK하이닉스 HBM처럼 EPS/FCF 체급 변화와 가격경로가 같이 맞으면
`STRUCTURAL_SUCCESS_ALIGNED`로 남길 수 있다. 하지만 Supermicro처럼 매출 성장이 강해도
감사인 사임과 공시 지연이 나오면 회계 신뢰가 깨졌기 때문에 hard 4C가 우선한다.

## 반영 파일

- `src/e2r/sector/round171_r13_loop10_cross_archetype_redteam.py`
- `src/e2r/cli/build_round171_r13_loop10_report.py`
- `tests/test_round171_r13_loop10_cross_archetype_redteam.py`
- `data/e2r_case_library/cases_r13_loop10_round171.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round171_r13_loop10_v10.csv`
- `output/e2r_round171_r13_loop10_cross_archetype_redteam/`

## R13 v10 공통 overlay 축

| axis | weight |
| --- | ---: |
| EPS/FCF·ROE·AFFO·OPM bodyweight change | 24 |
| evidence visibility | 20 |
| durability / repeatability | 16 |
| disclosure confidence / RedTeam | 12 |
| capital discipline / leverage / FCF | 10 |
| market mispricing / rerating gap | 10 |
| valuation room / 4B margin | 8 |

## R13 v10 Stage cap

R13 Loop 10은 `Stage 3-Green = 점수 높음`을 금지하고, 후보가 마지막 검문소를 모두 통과했는지 본다.
예를 들어 `tenant lease`가 있으면 Stage 2까지는 갈 수 있지만, AFFO/NOI와 가격경로가 없으면 Stage 3는 막힌다.

| cap | band | cap |
| --- | --- | --- |
| `stage1_theme_headline_cap` | Stage 1 | 45 |
| `stage2_verified_evidence_cap` | Stage 2 | 70 |
| `stage3_green_all_checks_gate` | Stage 3 | requires all Green checks |
| `stage4b_4c_final_redteam_gate` | 4B/4C | watch or break |

## Loop 10 추가 반영 사례

- `GE Vernova`: backlog, revenue/margin guide, price path가 같이 맞는 structural aligned 사례.
- `Datadog/Fortinet/Cisco`: AI가 기존 SW를 무조건 대체한다는 단순 공포가 아니라, observability·security·networking 수요가 revenue, billings, AI orders로 확인될 때만 구조 후보로 남긴다.
- `Bavarian Nordic`: 질병 이벤트가 정부 stockpile 계약과 guidance raise로 승격된 Stage 2 사례.
- `Bayer Crop Science`: 농업 input도 seed/IP licensing이 EBITDA로 연결되면 Stage 2 후보가 될 수 있지만, 반복 licensing revenue와 litigation cost 통제가 필요하다.
- `Circle`: regulated stablecoin infra는 가능성이 있지만 4B와 convertibility gate를 같이 본다.
- `BXDC/Fermi`: AI real asset 수요가 있어도 asset, tenant, NOI/AFFO가 없으면 Stage 3 금지.
- `Supermicro/CrowdStrike/Bluebird/Novo/Equinix/CoreWeave`: 회계, 운영 신뢰, 상업화, 가격전쟁, AFFO, circular financing hard gate.
- `Whirlpool/Hertz/LK-99`: hardware cycle, EV fleet unit economics, 과학 테마 재현 실패 반례.
- `STAGE2_EVIDENCE_NOT_GREEN`: 계약·고객·승인·ARR 같은 실체 있는 Stage 2 증거가 있어도 EPS/FCF 전환, 반복성, 가격경로, RedTeam 통과 전에는 Green으로 올리지 않는다.

## 산출 요약

| 항목 | 값 |
| --- | ---: |
| overlay target | 22 |
| source canonical target | 16 |
| overlay axis | 7 |
| stage cap | 4 |
| case candidate | 46 |
| structural success | 3 |
| success candidate | 14 |
| cyclical success | 1 |
| event premium | 1 |
| failed rerating | 8 |
| Stage 4B case | 8 |
| Stage 4C case | 12 |
| hard gate target | 10 |

해석하면, R13은 “후보를 더 만드는 라운드”가 아니라 “후보를 끝까지 통과시킬지 죽일지 판단하는 라운드”다.
예를 들어 Datadog/Fortinet/Cisco는 AI infra SW 수요가 숫자로 확인되면 살아남지만, Supermicro처럼 회계 신뢰가 깨지면 성장률이 좋아도 4C가 먼저 적용된다.
또한 tenant lease나 정부주문처럼 보기 좋은 증거가 있어도, 이익 전환과 반복성이 확인되기 전에는 `STAGE2_EVIDENCE_NOT_GREEN`으로 남긴다.

## 핵심 가드레일

- Stage 3-Green은 점수만으로 나오지 않는다.
- sector score, EPS/FCF 체급 변화, 반복성, 가격경로 alignment, disclosure confidence, 4B valuation room, hard 4C flag 부재가 모두 필요하다.
- price-only rally, event premium, cycle success는 structural Green과 분리한다.
- 회계 신뢰, 운영 신뢰, 상업화 실패, AFFO 품질, circular AI financing, stablecoin convertibility, policy shock은 hard 또는 hard-review gate로 둔다.
- round171 case pack은 candidate generation input이 아니다.
- production scoring/staging/RedTeam 로직은 변경하지 않았다.

## 산출물

- `round171_r13_loop10_cross_archetype_redteam_summary.md`
- `round171_r13_loop10_case_matrix.csv`
- `round171_r13_loop10_overlay_target_matrix.csv`
- `round171_r13_loop10_stage_date_plan.csv`
- `round171_r13_loop10_redteam_gate_plan.md`
- `round171_r13_loop10_price_validation_plan.md`
- `round171_r13_loop10_price_fields.csv`
- `round171_r13_loop10_overlay_axes.csv`
- `round171_r13_loop10_stage_caps.csv`

## 검증

- round171 전용 테스트가 target coverage, overlay axes, stage cap, hard-gate rules, report writer, production import guard를 확인한다.
- `PYTHONPATH=src python -m e2r.cli.build_round171_r13_loop10_report` 통과.
- `PYTHONPATH=src python -m unittest tests/test_round171_r13_loop10_cross_archetype_redteam.py -v` 통과.
- `PYTHONPATH=src python -m compileall -q src tests` 통과.
- `git diff --check` 통과.
- `PYTHONPATH=src python -m unittest discover -s tests -v` 통과: 2202 tests.
