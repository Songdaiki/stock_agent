# Checkpoint 28A Round 170 R11 Loop 10

## 목적

`docs/round/round_170.md`의 R11 정책/지정학/재난/이벤트 Loop 10 내용을 calibration 자료로 반영했다.

이번 라운드의 핵심은 “뉴스가 크다”와 “돈이 실제로 묶였다”를 분리하는 것이다. 예를 들어 전염병 뉴스는 Stage 1 라우팅 신호가 될 수 있지만, 정부 stockpile 계약, 계약금액, 매출 가이던스 상향, EBITDA margin 상향이 붙어야 Stage 2 후보가 된다.

## 반영 파일

- `src/e2r/sector/round170_r11_loop10_policy_geopolitical_event.py`
- `src/e2r/cli/build_round170_r11_loop10_report.py`
- `tests/test_round170_r11_loop10_policy_geopolitical_event.py`
- `data/e2r_case_library/cases_r11_loop10_round170.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round170_r11_loop10_v10.csv`
- `output/e2r_round170_r11_loop10_policy_geopolitical_event/`

## 핵심 반영

- R11 Loop 10 대상 canonical archetype 24개를 별도 round170 팩으로 분리했다.
- `round_170.md`의 대상 canonical archetype 24개와 별도 source count를 맞췄다.
- 케이스 후보 19개를 유지했다.
  - Stage 2 후보: Bavarian Nordic stockpile, Ukraine critical infra financing, China rare-earth export control, climate-to-grid infrastructure.
  - Event premium: China group visa tourism policy, disaster rebuild material, local policy theme.
  - RedTeam/4C: Moderna BARDA cancellation, North Korea Kumgang dismantling, LK-99 replication failure, Abbott diagnostics normalization.
  - 4B/4C-watch: AI citizen dividend policy shock, China rare-earth partial easing and approval recovery.
- `Round170BaseScoreAxis`를 추가해 R11 v10 기본 점수축 7개를 명시했다.
- 새 기본 점수축은 총 100점이다.
  - actual contract / budget / order / financing visibility: 28
  - EPS/FCF / revenue guidance conversion: 20
  - recurrence / durability: 14
  - bottleneck / policy intensity / geopolitical reality: 12
  - RedTeam / disclosure confidence: 12
  - market mispricing / rerating gap: 8
  - valuation room / 4B margin: 6
- Stage cap도 별도 산출물로 추가했다.
  - Stage 1 headline cap: 정책 발표, 전염병 뉴스, 재건회의, 수출통제 headline, 관광정책, preprint/SNS 과학테마는 최대 40점 라우팅 신호다.
  - Stage 2 money committed cap: 정부계약, stockpile, project financing, concession, guidance 상향은 최대 70점 후보 신호다.
  - Stage 3 repeat cash-flow gate: 반복조달, 매출 인식, EPS/FCF 전환, event 이후 수요 지속성이 있어야 한다.
  - 4B/4C event unwind gate: 조달 취소, funding withdrawal, 재현 실패, 수요 정상화, 정책 shock은 RedTeam으로 남긴다.

## Guardrails

- case record는 candidate-generation input으로 쓰지 않는다.
- StageClassifier, FeatureEngineering, RedTeam, E2R_STANDARD flow는 round170 팩을 import하지 않는다.
- 정책 발표, 재건회의, 수출통제 headline, 관광정책, 논문/preprint만으로 Stage 3-Green을 만들지 않는다.
- 정부계약 취소, funding withdrawal, 수요 정상화, 재현 실패, 시설 철거, 정책 shock은 RedTeam/4C 성격으로 유지한다.
- 희토류 수출통제는 macro bottleneck으로 볼 수 있지만, 수출 승인 회복·truce extension·가격 정상화가 나오면 event basket 4C-watch로 따로 본다.
- OpenDART/news detail에서 계약금액, 예산, 정부주문, financing, 공사착수, 매출 인식이 확인되지 않으면 Stage 3를 cap한다.

## 생성 리포트

- `round170_r11_loop10_policy_geopolitical_event_summary.md`
- `round170_r11_loop10_case_matrix.csv`
- `round170_r11_loop10_stage_date_plan.csv`
- `round170_r11_loop10_green_guardrails.md`
- `round170_r11_loop10_event_false_positive_caps.md`
- `round170_r11_loop10_price_validation_plan.md`
- `round170_r11_loop10_price_fields.csv`
- `round170_r11_loop10_base_score_axes.csv`
- `round170_r11_loop10_stage_caps.csv`

## 검증

- `PYTHONPATH=src python -m unittest tests/test_round170_r11_loop10_policy_geopolitical_event.py -v`
  - 12개 테스트 통과
- `PYTHONPATH=src python -m compileall -q src tests`
  - 통과
- 신규 산출물 시크릿 문자열 스캔
  - 통과
- `git diff --check`
  - 통과
- `PYTHONPATH=src python -m unittest discover -s tests -v`
  - 2189개 테스트 통과
- `PYTHONPATH=src python -m e2r.cli.build_round170_r11_loop10_report`
  - 케이스 JSONL, 점수 profile CSV, summary/guardrail/price-validation report 생성 확인
