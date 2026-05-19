# Round-192 R1 Loop-7 Green Gate Review

## Green Required Evidence

- `contract_amount_to_prior_sales`
- `contract_duration_months`
- `delivery_schedule`
- `customer_or_government_budget_financing`
- `backlog_growth`
- `opm_or_eps_revision`
- `price_path_after_evidence`

## Green Forbidden Patterns

- `order_headline_only`
- `margin_unknown`
- `delivery_schedule_unknown`
- `financing_condition_unknown`
- `ipo_or_supply_demand_price_spike`
- `price_moves_before_evidence`

## Shadow Score Adjustments

| axis | direction | points | reason |
| --- | --- | ---: | --- |
| `contract_quality` | raise | 2 | 계약 headline보다 계약 질을 더 본다. |
| `delivery_schedule` | raise | 2 | 방산/조선은 납품 일정이 매출 인식의 핵심이다. |
| `order_to_revenue_conversion` | raise | 2 | 수주가 매출과 이익으로 넘어가는지를 확인한다. |
| `op_eps_revision` | raise | 3 | Stage 3는 OP/EPS 체급 변화가 보여야 한다. |
| `margin_visibility` | raise | 3 | 저마진 수주는 Stage 3-Green을 막아야 한다. |
| `government_financing_or_budget` | raise | 2 | 정부 예산/금융 조건이 계약 지속성을 좌우한다. |
| `price_path_alignment` | raise | 2 | 증거 뒤에 가격경로가 따라오는지 검증한다. |
| `order_headline` | lower | -3 | 수주 뉴스만으로 Green을 주지 않는다. |
| `theme_keyword` | lower | -3 | 테마 키워드는 Stage 1 라우팅까지만 제한한다. |
| `broker_target_only` | lower | -2 | 목표가 상향만으로 구조적 evidence를 만들지 않는다. |
| `ipo_first_day_price_move` | lower | -4 | 상장 첫날 급등은 event premium/수급성으로 본다. |
| `contract_amount_without_margin` | lower | -2 | 계약금액만 있고 마진이 없으면 Stage 2에 머문다. |
| `policy_or_mou_without_budget` | lower | -3 | 정책/MOU는 예산과 계약 없이는 Green 근거가 아니다. |

## What Not To Change

- Do not apply these weights to production scoring yet.
- Do not use Round192 cases as candidate-generation input.
- Do not lower Stage 3-Green thresholds to force promotion.
- Do not invent contract margin, delivery schedules, financing, stage prices, or MFE/MAE.
