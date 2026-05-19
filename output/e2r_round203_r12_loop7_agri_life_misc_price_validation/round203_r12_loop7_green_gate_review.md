# Round-203 R12 Loop-7 Green Gate Review

## Green Required Evidence

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

## Green Forbidden Patterns

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
- `policy_news_only`
- `price_rally_before_company_evidence`

## Shadow Score Adjustments

| axis | direction | points | reason |
| --- | --- | ---: | --- |
| `recurring_revenue` | raise | 5 | R12에서 가장 강한 증거는 반복 결제 구조다. |
| `churn_stability` | raise | 5 | 렌탈·교육·서비스는 churn 안정성이 visibility를 만든다. |
| `arpu_or_repeat_course` | raise | 4 | ARPU나 반복 수강 매출이 있어야 정책 이벤트를 숫자로 연결한다. |
| `cash_conversion` | raise | 5 | 반복매출도 현금전환이 확인되어야 Stage 3 후보가 된다. |
| `unit_economics` | raise | 5 | 스마트팜·키오스크·렌탈은 unit economics가 핵심 splitter다. |
| `commercial_installation` | raise | 4 | 스마트팜은 정책보다 상업 설치와 운영계약을 우선한다. |
| `service_contract_visibility` | raise | 4 | 유지보수·서비스 계약은 일회성 하드웨어 매출보다 강하다. |
| `dealer_sell_through` | raise | 4 | 농기계는 딜러 재고가 아니라 실제 sell-through가 중요하다. |
| `inventory_quality` | raise | 4 | 재고와 매출채권 안정은 R12 false positive를 줄인다. |
| `regulatory_pass` | raise | 4 | 규제 소비재는 규제 통과와 허용 범위 확인이 필요하다. |
| `pricing_power_after_input_cost` | raise | 3 | 사료비·원가 상승 후 가격전가가 확인되어야 한다. |
| `defensive_theme_only` | lower | -5 | 방어주라는 이유만으로 Stage 3를 만들지 않는다. |
| `education_policy_only` | lower | -5 | 교육정책은 routing 증거이며 수강생·ARPU 전 Green이 아니다. |
| `agri_cycle_only` | lower | -4 | 농기계·농산물 사이클만으로 구조적 visibility를 주지 않는다. |
| `smart_farm_policy_only` | lower | -5 | 스마트팜 정책/AI농업 narrative는 설치·수주 전 Stage 1이다. |
| `disease_event_only` | lower | -5 | 질병 이벤트는 단기 MFE용이며 반복수요가 아니다. |
| `import_ban_event_only` | lower | -4 | 수입금지 뉴스는 완화되면 event fade가 될 수 있다. |
| `unconfirmed_export_theme` | lower | -3 | 수출 기대는 sell-through와 OPM 전까지 제한한다. |
| `dealer_inventory_unknown` | lower | -4 | 농기계 딜러 재고가 확인되지 않으면 visibility를 낮춘다. |
| `subsidy_dependent_unit_economics` | lower | -4 | 보조금 의존 unit economics는 Green blocker다. |
| `regulated_product_without_growth` | lower | -3 | 규제소비재 현금흐름은 성장·환원 없이 re-rating이 제한된다. |

## What Not To Change

- Do not apply these weights to production scoring yet.
- Do not use Round203 cases as candidate-generation input.
- Do not lower Stage 3-Green thresholds to force promotion.
- Do not invent accounts, churn, ARPU, unit economics, cash conversion, stage prices, or MFE/MAE.
- Do not treat policy, disease, smart-farm, agri-export, defensive, or regulated-cashflow themes as Green evidence alone.
