# Checkpoint 28A Round 145: R13 Loop 8 Cross-Archetype RedTeam / 4B / Price Validation

## 목적

`docs/round/round_145.md`의 R13 Loop 8 내용을 별도 calibration pack으로 반영했다.
R13은 새 섹터가 아니라 R1~R12 후보를 마지막에 검문하는 공통 overlay다.

쉬운 예로, SK하이닉스 HBM처럼 EPS/FCF 체급 변화와 가격경로가 같이 맞으면
`STRUCTURAL_SUCCESS_ALIGNED`로 남길 수 있다. 하지만 Supermicro처럼 매출 성장이 강해도
감사인 사임과 공시 지연이 나오면 회계 신뢰가 깨졌기 때문에 hard 4C가 우선한다.

## 반영 파일

- `src/e2r/sector/round145_r13_loop8_cross_archetype_redteam.py`
- `src/e2r/cli/build_round145_r13_loop8_report.py`
- `tests/test_round145_r13_loop8_cross_archetype_redteam.py`
- `data/e2r_case_library/cases_r13_loop8_round145.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round145_r13_loop8_v8.csv`
- `output/e2r_round145_r13_loop8_cross_archetype_redteam/`

## R13 v8 공통 overlay 축

| axis | weight |
| --- | ---: |
| EPS/FCF·ROE·AFFO·OPM bodyweight change | 24 |
| evidence visibility | 20 |
| durability / repeatability | 16 |
| disclosure confidence / RedTeam | 12 |
| capital discipline / leverage / FCF | 10 |
| market mispricing / rerating gap | 10 |
| valuation room / 4B margin | 8 |

## R13 v8 Stage cap

R13 Loop 8은 `Stage 3-Green = 점수 높음`을 금지하고, 후보가 마지막 검문소를 모두 통과했는지 본다.
예를 들어 `tenant lease`가 있으면 Stage 2까지는 갈 수 있지만, AFFO/NOI와 가격경로가 없으면 Stage 3는 막힌다.

| cap | band | cap |
| --- | --- | --- |
| `stage1_theme_headline_cap` | Stage 1 | 45 |
| `stage2_verified_evidence_cap` | Stage 2 | 70 |
| `stage3_green_all_checks_gate` | Stage 3 | requires all Green checks |
| `stage4b_4c_final_redteam_gate` | 4B/4C | watch or break |

## Loop 8 추가 반영 사례

- `GE Vernova`: backlog, revenue/margin guide, price path가 같이 맞는 structural aligned 사례.
- `Bavarian Nordic`: 질병 이벤트가 정부 stockpile 계약과 guidance raise로 승격된 Stage 2 사례.
- `Circle`: regulated stablecoin infra는 가능성이 있지만 4B와 convertibility gate를 같이 본다.
- `BXDC/Fermi`: AI real asset 수요가 있어도 asset, tenant, NOI/AFFO가 없으면 Stage 3 금지.
- `Supermicro/CrowdStrike/Bluebird/Novo/Equinix/CoreWeave`: 회계, 운영 신뢰, 상업화, 가격전쟁, AFFO, circular financing hard gate.
- `Whirlpool/Hertz/LK-99`: hardware cycle, EV fleet unit economics, 과학 테마 재현 실패 반례.

## 핵심 가드레일

- Stage 3-Green은 점수만으로 나오지 않는다.
- sector score, EPS/FCF 체급 변화, 반복성, 가격경로 alignment, disclosure confidence, 4B valuation room, hard 4C flag 부재가 모두 필요하다.
- price-only rally, event premium, cycle success는 structural Green과 분리한다.
- 회계 신뢰, 운영 신뢰, 상업화 실패, AFFO 품질, circular AI financing, stablecoin convertibility, policy shock은 hard 또는 hard-review gate로 둔다.
- round145 case pack은 candidate generation input이 아니다.
- production scoring/staging/RedTeam 로직은 변경하지 않았다.

## 산출물

- `round145_r13_loop8_cross_archetype_redteam_summary.md`
- `round145_r13_loop8_case_matrix.csv`
- `round145_r13_loop8_overlay_target_matrix.csv`
- `round145_r13_loop8_stage_date_plan.csv`
- `round145_r13_loop8_redteam_gate_plan.md`
- `round145_r13_loop8_price_validation_plan.md`
- `round145_r13_loop8_price_fields.csv`
- `round145_r13_loop8_overlay_axes.csv`
- `round145_r13_loop8_stage_caps.csv`

## 검증

- round145 전용 테스트가 target coverage, overlay axes, stage cap, hard-gate rules, report writer, production import guard를 확인한다.
- 전체 테스트는 `PYTHONPATH=src python -m unittest discover -s tests -v`로 검증한다.
