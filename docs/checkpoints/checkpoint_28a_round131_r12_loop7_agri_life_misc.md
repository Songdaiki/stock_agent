# Checkpoint 28A Round 131: R12 Loop 7 Agriculture / Life Services / Misc

## 목적

`docs/round/round_131.md`의 R12 Loop 7 내용을 별도 calibration pack으로 반영했다.
이 라운드는 농업, 교육, 생활가전, 키오스크, 전자담배, cannabis 같은 테마성 높은 영역에서
단순 뉴스와 반복 현금흐름을 분리하는 데 초점이 있다.

예를 들어 조류독감 뉴스만 있으면 Stage 1 재료다. 하지만 정부 백신 주문,
반복 접종, 매출과 OPM이 확인되면 Stage 2 이상으로 볼 수 있다. 반대로
AI 교육 기능 출시가 있어도 bookings miss와 margin 압박이 같이 나오면 RedTeam 신호다.

## 반영 파일

- `src/e2r/sector/round131_r12_loop7_agri_life_misc.py`
- `src/e2r/cli/build_round131_r12_loop7_report.py`
- `tests/test_round131_r12_loop7_agri_life_misc.py`
- `data/e2r_case_library/cases_r12_loop7_round131.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round131_r12_loop7_v7.csv`
- `output/e2r_round131_r12_loop7_agri_life_misc/`

## R12 v7 기본 점수축

R12 Loop 7은 생산 점수를 바꾸지 않고, 아래 7개 축을 calibration 산출물로만 추가했다.

| axis | weight |
| --- | ---: |
| EPS/FCF·OPM conversion | 22 |
| recurring contract/revenue/regulatory visibility | 20 |
| unit economics / price pass-through / demand durability | 18 |
| market mispricing / rerating gap | 8 |
| valuation room / 4B margin | 6 |
| capital discipline / debt / cash runway | 10 |
| regulation / litigation / public health / disclosure | 16 |

## 핵심 가드레일

- Stage 3-Green 기준은 낮추지 않았다.
- R12 Loop 7 case pack은 candidate generation input이 아니다.
- 질병, 곡물가격, AI 교육, 스마트팜, 셀프체크아웃, 니코틴, cannabis 뉴스만으로 Green을 만들지 않는다.
- 반복계약, 반복매출, unit economics, 판가전가, 규제승인 범위, public-health gate, FCF가 확인돼야 한다.
- right-to-repair, Chapter 11, bookings miss, dividend suspension, local self-checkout regulation, youth-safety warning은 RedTeam 자료로 유지한다.

## 산출물

- `round131_r12_loop7_agri_life_misc_summary.md`
- `round131_r12_loop7_case_matrix.csv`
- `round131_r12_loop7_stage_date_plan.csv`
- `round131_r12_loop7_green_guardrails.md`
- `round131_r12_loop7_unit_economics_caps.md`
- `round131_r12_loop7_price_validation_plan.md`
- `round131_r12_loop7_price_fields.csv`
- `round131_r12_loop7_base_score_axes.csv`

## 검증

- round131 전용 테스트가 R12 Loop 7 대상 archetype, base score axis, writer 산출물, production import guard를 확인한다.
- 전체 테스트는 `PYTHONPATH=src python -m unittest discover -s tests -v`로 검증한다.
