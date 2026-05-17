# Checkpoint 28A Round 53: R13 Cross-Archetype RedTeam / 4B / 4C Overlay

## 목적

Round 53은 새 산업 섹터가 아니라 전 섹터 공통 검증 레이어다.
R1~R12에서 후보가 나온 뒤, R13은 다음을 확인한다.

- 점수와 EPS/FCF 증거가 같이 움직였는가
- 가격 경로가 증거를 검증했는가
- 회계/감사/공시/법적/운영 신뢰 문제가 없는가
- 4B 과열이나 4C 논리 훼손이 이미 발생했는가

쉬운 예시:
`AI 서버 수요`로 점수가 높아도 감사인 사임과 보고 지연이 있으면 Green 후보가 아니라 `REDTEAM_ACCOUNTING_TRUST_OVERLAY` 또는 `THESIS_BREAK_4C`로 봐야 한다.

## 반영 내용

- `src/e2r/sector/archetypes.py`
  - R13 공통 오버레이 archetype 14개 추가
- `src/e2r/sector/round53_r13_cross_archetype_redteam.py`
  - R13 target 14개
  - R13 case candidate 15개
  - RedTeam gate plan
  - price/stage validation field plan
- `src/e2r/cli/build_round53_r13_report.py`
  - R13 리포트 생성 CLI 추가
- `tests/test_round53_r13_cross_archetype_redteam.py`
  - R13 타깃, 케이스, Green 가드레일, CLI, report writer 테스트 추가
- `data/e2r_case_library/cases_r13_round53.jsonl`
  - R13 case pack 생성
- `data/sector_taxonomy/score_weight_profiles_round53_r13_v1.csv`
  - R13 overlay score/gate profile 생성
- `output/e2r_round53_r13_cross_archetype_redteam/`
  - summary, case matrix, target matrix, stage-date plan, redteam gate plan, price-field plan 생성

## R13 Target Summary

- target_count: 14
- case_candidate_count: 15
- structural_success_count: 1
- success_candidate_count: 1
- cyclical_success_count: 1
- event_premium_count: 1
- overheat_count: 1
- failed_rerating_count: 3
- stage4b_case_count: 2
- stage4c_case_count: 7
- hard_gate_target_count: 6
- green_possible_count: 1
- watch_yellow_first_count: 4
- redteam_first_count: 9

## 추가된 R13 Archetype

- `REDTEAM_ACCOUNTING_TRUST_OVERLAY`
- `FINANCIAL_REPORTING_INTEGRITY_RISK`
- `PRICE_ONLY_RALLY`
- `EVENT_PREMIUM`
- `CYCLICAL_SUCCESS`
- `STRUCTURAL_SUCCESS_ALIGNED`
- `EVIDENCE_GOOD_BUT_PRICE_FAILED`
- `FALSE_POSITIVE_SCORE`
- `CROWDED_RERATING_4B_WATCH`
- `THESIS_BREAK_4C`
- `LEGAL_REGULATORY_REDTEAM`
- `OPERATIONAL_TRUST_BREAK`
- `LEVERAGE_FCF_BREAKDOWN`
- `UNKNOWN_INSUFFICIENT_EVIDENCE`

## 핵심 가드레일

- R13 case record는 후보 생성 input이 아니다.
- production scoring/staging/red-team 로직은 바꾸지 않았다.
- Stage 3-Green 기준을 낮추지 않았다.
- 가격만 오른 rally는 Green evidence가 아니다.
- event premium과 cycle success는 구조적 성공과 분리한다.
- auditor resignation, filing delay, regulatory denial, operational trust break, cash runway collapse는 hard RedTeam evidence다.
- `unknown_insufficient_evidence`는 정상 출력이다. 모르는 증거는 채우지 않는다.

## 생성 명령

```bash
PYTHONPATH=src python -m e2r.cli.build_round53_r13_report
```

## 검증

```bash
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest tests.test_round53_r13_cross_archetype_redteam -v
PYTHONPATH=src python -m unittest discover -s tests -v
```

Round 53 단위 테스트는 11개 모두 통과했다.
전체 테스트는 825개 모두 통과했다.

## 다음 단계

R13은 점수 적용이 아니라 검증막이다.
다음 Checkpoint에서 할 일은 R1~R12 후보의 shadow score와 R13 overlay 결과를 나란히 출력해서, 어떤 후보가 `STRUCTURAL_SUCCESS_ALIGNED`, `CROWDED_RERATING_4B_WATCH`, `FALSE_POSITIVE_SCORE`, `THESIS_BREAK_4C`로 갈리는지 확인하는 것이다.
