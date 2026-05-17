# Checkpoint 28A Round 169: R12 Loop 10 Agriculture / Life Services / Misc

## 목적

`docs/round/round_169.md`의 R12 Loop 10 내용을 별도 calibration pack으로 반영했다.
이 라운드는 농업, 교육, 생활가전, 키오스크, 전자담배, cannabis 같은 테마성 높은 영역에서
단순 뉴스와 반복 현금흐름을 분리하는 데 초점이 있다.

예를 들어 조류독감 뉴스만 있으면 Stage 1 재료다. 하지만 정부 백신 주문,
반복 접종, 매출과 OPM이 확인되면 Stage 2 이상으로 볼 수 있다. 반대로
AI 교육 기능 출시가 있어도 bookings miss와 margin 압박이 같이 나오면 RedTeam 신호다.

## 반영 파일

- `src/e2r/sector/round169_r12_loop10_agri_life_misc.py`
- `src/e2r/cli/build_round169_r12_loop10_report.py`
- `tests/test_round169_r12_loop10_agri_life_misc.py`
- `data/e2r_case_library/cases_r12_loop10_round169.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round169_r12_loop10_v10.csv`
- `output/e2r_round169_r12_loop10_agri_life_misc/`

## R12 v10 기본 점수축

R12 Loop 10은 생산 점수를 바꾸지 않고, 아래 7개 축을 calibration 산출물로만 추가했다.

| axis | weight |
| --- | ---: |
| EPS/FCF·OPM conversion | 22 |
| recurring contract/revenue/regulatory visibility | 20 |
| unit economics / price pass-through / demand durability | 18 |
| regulation / litigation / public health / disclosure | 16 |
| capital discipline / debt / cash runway | 10 |
| market mispricing / rerating gap | 8 |
| valuation room / 4B margin | 6 |

## R12 v10 Stage cap

이번 라운드는 점수축보다 Stage cap을 더 명시했다. 예를 들어 `AI 교육 기능 출시`는 사용자가 늘어도
bookings와 paid conversion이 같이 좋아지기 전까지 Stage 1~2에 머문다.

| cap | band | cap |
| --- | --- | --- |
| `stage1_theme_event_cap` | Stage 1 | 45 |
| `stage2_repeat_revenue_unit_economics_cap` | Stage 2 | 70 |
| `stage3_recurring_fcf_gate` | Stage 3 | requires score above 70 and recurring FCF |
| `stage4b_4c_misc_theme_unwind_gate` | 4B/4C | watch or break |

## 핵심 가드레일

- Stage 3-Green 기준은 낮추지 않았다.
- R12 Loop 10 case pack은 candidate generation input이 아니다.
- `round_169.md`의 핵심 target 30개에 맞췄다. 이전 R12 보조 overlay 중 일부는 case의 `secondary_archetypes` 참고값으로만 남기고, v10 score target에서는 제외했다.
- `FERTILIZER_INPUT_COST_SULFURIC_ACID`를 추가해 phosphate 가격 강세가 있어도 sulfuric acid, sulfur, ammonia, urea 비용이 마진을 압박하면 RedTeam gate로 처리하게 했다.
- 질병, 곡물가격, AI 교육, 스마트팜, 셀프체크아웃, 니코틴, cannabis 뉴스만으로 Green을 만들지 않는다.
- 반복계약, 반복매출, unit economics, 판가전가, 규제승인 범위, public-health gate, FCF가 확인돼야 한다.
- right-to-repair, Chapter 11, bookings miss, dividend suspension, local self-checkout regulation, youth-safety warning은 RedTeam 자료로 유지한다.

## 산출 요약

| 항목 | 값 |
| --- | ---: |
| score target | 30 |
| source canonical target | 30 |
| base score axis | 7 |
| stage cap | 4 |
| case candidate | 24 |
| success candidate | 5 |
| cyclical success | 2 |
| event premium | 2 |
| failed rerating | 5 |
| Stage 4B case | 3 |
| Stage 4C case | 10 |
| Green possible | 0 |
| Watch/Yellow first | 17 |
| RedTeam first | 13 |
| gate-only target | 9 |

해석하면, 이번 라운드는 “새 Green 후보를 만들기”보다 “테마성 뉴스가 반복 현금흐름으로 전환되는지 검증하기”에 가깝다.
예를 들어 `vertical farming`은 농업 혁신처럼 보일 수 있지만 unit economics와 cash runway가 무너지면 Stage 4C 쪽 증거가 된다.
반대로 animal-health 백신은 단순 질병 뉴스가 아니라 조건부 승인, 정부/농가 반복 주문, OPM/FCF가 같이 확인될 때만 Stage 2 이상으로 올라갈 수 있다.

## 산출물

- `round169_r12_loop10_agri_life_misc_summary.md`
- `round169_r12_loop10_case_matrix.csv`
- `round169_r12_loop10_stage_date_plan.csv`
- `round169_r12_loop10_green_guardrails.md`
- `round169_r12_loop10_unit_economics_caps.md`
- `round169_r12_loop10_price_validation_plan.md`
- `round169_r12_loop10_price_fields.csv`
- `round169_r12_loop10_base_score_axes.csv`
- `round169_r12_loop10_stage_caps.csv`

## 검증

- `PYTHONPATH=src python -m e2r.cli.build_round169_r12_loop10_report` 통과.
- `PYTHONPATH=src python -m unittest tests/test_round169_r12_loop10_agri_life_misc.py -v` 통과: 12개 테스트.
- `PYTHONPATH=src python -m compileall -q src tests` 통과.
- `git diff --check` 통과.
- 신규 산출물 시크릿 문자열 스캔 통과.
- `PYTHONPATH=src python -m unittest discover -s tests -v` 통과: 2177개 테스트.

round169 전용 테스트는 R12 Loop 10 대상 archetype, base score axis, stage cap, writer 산출물, production import guard를 확인한다.
