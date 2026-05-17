# Checkpoint 28A Round 132: R13 Loop 7 Cross-Archetype RedTeam / 4B / Price Validation

## 목적

`docs/round/round_132.md`의 R13 Loop 7 내용을 별도 calibration pack으로 반영했다.
R13은 새 섹터가 아니라 R1~R12 후보를 마지막에 검문하는 공통 overlay다.

쉬운 예로, SK하이닉스 HBM처럼 EPS/FCF 체급 변화와 가격경로가 같이 맞으면
`STRUCTURAL_SUCCESS_ALIGNED`로 남길 수 있다. 하지만 Supermicro처럼 매출 성장이 강해도
감사인 사임과 공시 지연이 나오면 회계 신뢰가 깨졌기 때문에 hard 4C가 우선한다.

## 반영 파일

- `src/e2r/sector/round132_r13_loop7_cross_archetype_redteam.py`
- `src/e2r/cli/build_round132_r13_loop7_report.py`
- `tests/test_round132_r13_loop7_cross_archetype_redteam.py`
- `data/e2r_case_library/cases_r13_loop7_round132.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round132_r13_loop7_v7.csv`
- `output/e2r_round132_r13_loop7_cross_archetype_redteam/`

## R13 v7 공통 overlay 축

| axis | weight |
| --- | ---: |
| EPS/FCF·ROE·AFFO·OPM bodyweight change | 24 |
| evidence visibility | 20 |
| durability / repeatability | 16 |
| market mispricing / rerating gap | 10 |
| valuation room / 4B margin | 10 |
| capital discipline / leverage / FCF | 10 |
| disclosure confidence / RedTeam | 10 |

## 핵심 가드레일

- Stage 3-Green은 점수만으로 나오지 않는다.
- sector score, EPS/FCF 체급 변화, 반복성, 가격경로 alignment, disclosure confidence, 4B valuation room, hard 4C flag 부재가 모두 필요하다.
- price-only rally, event premium, cycle success는 structural Green과 분리한다.
- 회계 신뢰, 운영 신뢰, 상업화 실패, AFFO 품질, circular AI financing, stablecoin convertibility, policy shock은 hard 또는 hard-review gate로 둔다.
- round132 case pack은 candidate generation input이 아니다.
- production scoring/staging/RedTeam 로직은 변경하지 않았다.

## 산출물

- `round132_r13_loop7_cross_archetype_redteam_summary.md`
- `round132_r13_loop7_case_matrix.csv`
- `round132_r13_loop7_overlay_target_matrix.csv`
- `round132_r13_loop7_stage_date_plan.csv`
- `round132_r13_loop7_redteam_gate_plan.md`
- `round132_r13_loop7_price_validation_plan.md`
- `round132_r13_loop7_price_fields.csv`
- `round132_r13_loop7_overlay_axes.csv`

## 검증

- round132 전용 테스트가 target coverage, overlay axes, hard-gate rules, report writer, production import guard를 확인한다.
- 전체 테스트는 `PYTHONPATH=src python -m unittest discover -s tests -v`로 검증한다.
