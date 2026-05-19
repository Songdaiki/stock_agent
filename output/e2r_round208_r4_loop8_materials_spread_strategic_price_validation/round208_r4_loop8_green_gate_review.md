# Round-208 R4 Loop-8 Green Gate Review

## Green Required Evidence

- `actual_product_spread`
- `cost_curve_advantage`
- `supply_discipline_or_capacity_shutdown`
- `inventory_build_absent`
- `fcf_after_working_capital`
- `price_floor_or_offtake`
- `medium_term_eps_revision`
- `capex_and_dilution_risk_passed`
- `price_path_after_evidence`

## Green Forbidden Patterns

- `commodity_price_spike_only`
- `tender_offer_premium`
- `governance_battle_only`
- `policy_support_without_fcf`
- `unconfirmed_media_report`
- `restructuring_plan_without_margin`
- `lithium_or_polysilicon_price_event_only`
- `geopolitical_refining_margin_shock_only`

## Shadow Score Adjustments

| axis | direction | points | reason |
| --- | --- | ---: | --- |
| `actual_product_spread` | raise | 5 | R4 Stage 3는 원자재 가격보다 제품 스프레드 확인이 먼저다. |
| `fcf_after_working_capital` | raise | 5 | 재고와 운전자본 이후 FCF가 보여야 구조적 rerating 후보가 된다. |
| `supply_discipline_confirmed` | raise | 5 | 공급규율 또는 설비중단이 실제 확인되어야 spread 회복이 지속된다. |
| `capacity_shutdown_confirmed` | raise | 4 | 롯데케미칼 Daesan NCC처럼 확정된 shutdown은 Stage 2 근거다. |
| `price_floor_or_offtake` | raise | 5 | 전략자원은 price floor/offtake가 있어야 commodity cycle과 분리된다. |
| `cost_curve_advantage` | raise | 4 | cost curve 우위가 있어야 가격 하락에도 FCF 방어가 가능하다. |
| `strategic_customer_or_government_offtake` | raise | 4 | 정부 지원이나 전략고객은 offtake/FCF로 연결될 때 의미가 있다. |
| `inventory_normalization` | raise | 4 | 화학/소재는 재고 축적이 아니어야 spread 개선이 신뢰된다. |
| `capital_return_from_cashflow` | raise | 3 | 현금흐름에서 나오는 환원은 governance event premium과 다르다. |
| `commodity_price_up_only` | lower | -5 | 원자재 가격 상승만으로는 EPS/FCF 체급 변화를 증명하지 못한다. |
| `restructuring_plan_without_margin` | lower | -4 | 구조조정 계획은 OPM/FCF 회복 전까지 Stage 2 watch다. |
| `policy_support_without_fcf` | lower | -4 | 정책 지원만 있고 FCF가 없으면 Green 금지다. |
| `tender_offer_or_governance_premium` | lower | -5 | 공개매수/경영권 프리미엄은 구조적 Stage 3와 분리한다. |
| `unconfirmed_media_report` | lower | -5 | OCI SpaceX, 풍산 M&A 보도처럼 미확정 보도는 event premium이다. |
| `capacity_cut_expectation_only` | lower | -3 | capacity cut 기대만 있고 spread/OPM이 없으면 Green 금지다. |
| `lithium_price_event` | lower | -4 | 리튬 가격 반등은 cyclical/event로 먼저 본다. |
| `refining_margin_geopolitical_shock` | lower | -3 | 지정학적 정제마진 spike는 multi-quarter floor 전까지 cycle이다. |
| `customer_or_contract_unconfirmed` | lower | -4 | 고객 또는 계약이 미확정이면 confidence cap을 둔다. |
| `capex_heavy_project_pre_revenue` | lower | -4 | 상업가동 전 대형 CAPEX 프로젝트는 dilution/FCF 리스크가 크다. |

## What Not To Change

- Do not apply these weights to production scoring yet.
- Do not use Round208 cases as candidate-generation input.
- Do not lower Stage 3-Green thresholds to force promotion.
- Do not invent full OHLC, stage prices, or MFE/MAE when only reported anchors exist.
- Do not treat commodity price spike, governance battle, policy support, restructuring plan, or unconfirmed media report as Green evidence alone.
