# Checkpoint 28A Round 119: E2R First Principles Guardrail

## 목적

Round 119는 새 섹터 팩이나 점수 변경이 아니다. R1~R13 반복 작업 전체가 계속 같은 최상위 원칙을 따르도록 고정하는 메타 라운드다.

핵심 체인은 다음과 같다.

```text
산업 구조 변화
-> EPS/FCF 체급 변화
-> 이익 지속성 잠김
-> 시장의 과거 프레임 오해
-> 밸류에이션 리레이팅
-> 가격경로 검증
-> RedTeam / 4B / 4C 통과
```

쉬운 예시는 이렇다.

- 전력설비 뉴스가 있어도 계약금액, 계약기간, 수주잔고, 마진, EPS/FCF 상향이 없으면 Green이 아니다.
- HBM이라는 단어가 있어도 LTA, 선수금, CAPA 제약, 컨센서스 상향, 리레이팅 여지가 없으면 Green이 아니다.
- 정책, MOU, 재난, 질병 뉴스는 계약, 예산, financing, 매출, guidance로 승격되기 전까지 event premium이다.

## 반영 내용

- E2R first-principles 체인 7단계를 데이터화했다.
- Stage 3-Green gate 7개를 명시했다.
- R1~R13 Loop 7에서 각 라운드가 봐야 할 focus map을 만들었다.
- Theme tag는 routing 전용이고 score evidence가 아니라는 guardrail을 명시했다.
- false Green 패턴 10개를 따로 뽑았다.
- production scoring, feature engineering, staging, RedTeam 로직은 변경하지 않았다.

## 산출물

- `src/e2r/sector/round119_e2r_first_principles.py`
- `src/e2r/cli/build_round119_first_principles_report.py`
- `tests/test_round119_e2r_first_principles.py`
- `data/sector_taxonomy/e2r_first_principles_round119.csv`
- `output/e2r_round119_first_principles/round119_first_principles_summary.json`
- `output/e2r_round119_first_principles/round119_first_principles_summary.md`
- `output/e2r_round119_first_principles/round119_green_gate_checklist.md`
- `output/e2r_round119_first_principles/round119_loop7_focus_map.csv`
- `output/e2r_round119_first_principles/round119_theme_tag_guardrails.md`
- `output/e2r_round119_first_principles/round119_false_green_patterns.csv`

## 요약 수치

- principle_step_count: 7
- green_gate_count: 7
- loop7_focus_count: 13
- theme_tag_rule_count: 5
- false_green_pattern_count: 10
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false
- theme_tags_are_score_evidence: false

## Green Gate

Stage 3-Green은 다음 7개 gate를 통과해야 한다.

- cross_evidence
- eps_fcf_durability
- structural_visibility
- old_frame_mispricing
- price_path_alignment
- no_hard_redteam
- not_saturated_4b

예를 들어 `price_path_alignment`는 주가가 먼저 급등한 뒤 증거가 따라오지 않는 경우를 막는 gate다. 반대로 공시/리포트/실적이 먼저 나오고, 그 날짜 이후 가격 경로가 논리와 맞으면 통과할 수 있다.

## Theme Tag 원칙

Raw theme tag는 attention routing만 한다. 점수 증거가 아니다.

예:

```text
HBM tag
-> 검색/cheap scan 우선순위는 올릴 수 있음
-> 그러나 Stage 3-Green 점수는 HBM 수요, CAPA 제약, LTA/선수금, EPS/FCF revision이 있어야 가능
```

## 검증

실행 명령:

```bash
PYTHONPATH=src python -m unittest tests.test_round119_e2r_first_principles -v
PYTHONPATH=src python -m e2r.cli.build_round119_first_principles_report
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
git diff --check
```

검증 결과:

- Round 119 전용 테스트: 9개 통과
- 전체 테스트: 1546개 통과
- diff whitespace check: 통과

## 다음 단계

다음 Loop 7부터는 각 섹터 팩이 이 원칙을 기준으로 작성되어야 한다. 핵심은 archetype을 더 많이 만드는 것이 아니라, 각 archetype에서 EPS/FCF 체급 변화가 실제로 지속되는 증거가 무엇인지 구분하는 것이다.
