# Checkpoint 28A Round 203 R12 Loop 7 Agri/Life/Misc Price Validation

## 목적

Round 203은 R12 농업·생활서비스·기타 케이스를 가격경로 검증용 case library로 구조화했다.

핵심 원칙은 단순하다. R12에서 Stage 3 후보가 되려면 “생활필수/방어주/정책 테마”가 아니라 반복매출, churn 안정, ARPU, unit economics, 규제 통과, 현금전환이 확인되어야 한다.

예: `as_of_date=2025-05-19`에 브라질 조류독감 수입제한 뉴스로 poultry basket이 급등해도, 2025-06-23 제한 완화가 나오면 구조적 Stage 3가 아니라 event fade로 본다.

## 추가 파일

- `src/e2r/sector/round203_r12_loop7_agri_life_misc_price_validation.py`
- `src/e2r/cli/build_round203_r12_loop7_report.py`
- `tests/test_round203_r12_loop7_agri_life_misc_price_validation.py`
- `data/e2r_case_library/cases_r12_loop7_round203.jsonl`
- `data/sector_taxonomy/round203_r12_loop7_agri_life_misc_price_validation_audit.json`
- `output/e2r_round203_r12_loop7_agri_life_misc_price_validation/`

## 케이스 요약

| case | 판정 | Stage 3 | 해석 |
| --- | --- | ---: | --- |
| 코웨이 | `success_candidate` | 없음 | R12에서 가장 강한 recurring-service 후보지만 계정·churn·ARPU·FCF 전 보류 |
| 대동/TYM | `success_candidate` | 없음 | 농기계 수출·자율주행 테마는 attention, 딜러 sell-through와 재고 확인 필요 |
| 메가스터디교육 | `event_premium` | 없음 | 의대정원 정책은 수강생·repeat course·OPM 전 Green 금지 |
| 교육·에듀테크 basket | `4b_watch` | 없음 | 교실 디지털기기 규제는 양날의 policy overlay |
| 하림/마니커류 poultry basket | `event_premium` | 없음 | 질병/수입제한 이벤트는 단기 MFE 가능, 완화 시 event fade |
| KT&G | `success_candidate` | 없음 | 안정 cashflow 후보지만 volume, HNB, 규제 리스크 확인 필요 |
| 스마트팜 basket | `event_premium` | 없음 | 정책·AI농업 narrative만으로 Green 금지 |

## Green Gate

필수 증거:

- `recurring_revenue_confirmed`
- `repeat_purchase_or_repeat_course_confirmed`
- `churn_or_retention_stable`
- `arpu_or_price_pass_through_confirmed`
- `unit_economics_positive`
- `cash_conversion_confirmed`
- `inventory_and_receivables_stable`
- `regulatory_risk_passed`
- `subsidy_dependency_low`
- `price_path_after_evidence`

금지 패턴:

- `defensive_theme_only`
- `education_policy_only`
- `agri_cycle_only`
- `smart_farm_policy_only`
- `disease_event_only`
- `import_ban_event_only`
- `unconfirmed_export_theme`
- `dealer_inventory_unknown`
- `subsidy_dependent_unit_economics`
- `regulated_product_without_growth`

## Production 변경 여부

- production scoring changed: false
- candidate generation input: false
- shadow weight only: true
- needs OHLC backfill: true

이번 라운드는 production score를 바꾸지 않는다. 케이스와 점수축은 향후 shadow scoring과 가격경로 검증에만 사용한다.
