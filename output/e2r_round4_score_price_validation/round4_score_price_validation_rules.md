# Round-4 Score-Price Validation Rules

Source round: `docs/round/round_04.md`

This is calibration material. It does not change production scoring.

## Global Alignment Rules
- Score must lead to a Stage label before the relevant price path is judged.
- A structural success needs rerating within roughly 6-24 months after Stage 2/3 evidence.
- Price movement must be supported by EPS/OP/FCF or credible revision evidence, not theme alone.
- If a Stage 3-like score is followed by quick 4C, the score was probably a false positive.
- Event premium, one-off demand, and credit relief can move price but are not true structural rerating.

## Counterexample Rules
- High price return without EPS/FCF evidence becomes price_moved_without_evidence.
- Good evidence without rerating becomes evidence_good_but_price_failed.
- A Green-like score that should have been Red becomes should_have_been_red.
- A report-driven candidate with no commercialization or cash-flow conversion remains Green-restricted.

## Archetype Rules

### AI_DATA_CENTER_INFRASTRUCTURE
- principle: AI 키워드가 아니라 주문, 병목, 매출 전환이 리레이팅과 맞아야 한다.
- success_requires: confirmed_orders, customer_capex_visibility, capacity_bottleneck, op_eps_revision
- reject_if: ai_keyword_only, no_confirmed_order, customer_capex_cut, price_only_rally
- expected_rerating_result: true_rerating_or_theme_overheat
- stage_failure_focus: missed_structural, should_have_been_red
- score_weight_adjustment_hint: Score confirmed order/revenue exposure above AI keyword exposure.
- Green policy: Green possible only with confirmed order/revenue and cross-evidence.

### BIOTECH_REGULATORY
- principle: 임상/허가 뉴스와 매출화/로열티 현금흐름을 분리한다.
- success_requires: commercialization_path, royalty_or_revenue_conversion, cash_runway, dilution_risk_low
- reject_if: clinical_news_only, approval_delay, cb_or_rights_dilution, cash_burn
- expected_rerating_result: event_premium_or_no_rerating
- stage_failure_focus: should_have_been_red, false_green
- score_weight_adjustment_hint: Block pre-revenue Green unless royalty/revenue conversion is visible.
- Green policy: Pre-revenue clinical stories are Green-blocked.

### CONSTRUCTION_REAL_ESTATE_CREDIT
- principle: PF, 현금흐름, 신용위험이 수주 뉴스보다 먼저다.
- success_requires: pf_risk_resolved, cash_flow_improvement, debt_reduction, cost_ratio_stable
- reject_if: credit_relief_only, pf_loss, unsold_inventory, liquidity_stress
- expected_rerating_result: credit_relief_rally_or_no_rerating
- stage_failure_focus: should_have_been_red, false_green
- score_weight_adjustment_hint: Cap order/backlog score when PF and liquidity risk remain unresolved.
- Green policy: Green very restricted; credit risk must be resolved first.

### EDUCATION_SPECIALTY_SERVICES
- principle: 정책/입시 이벤트와 반복 서비스 매출을 구분한다.
- success_requires: recurring_service_revenue, opm_improvement, student_retention_or_pricing, policy_risk_low
- reject_if: policy_event_only, regulatory_change, one_time_enrollment_spike, margin_pressure
- expected_rerating_result: event_premium_or_true_rerating
- stage_failure_focus: false_yellow, stage2_watch_success
- score_weight_adjustment_hint: Reward recurring revenue and retention; cap policy-event rallies.
- Green policy: Green requires durable recurring revenue, not policy-event traffic.

### FINANCIAL_SPREAD_BALANCE_SHEET
- principle: 저PBR만이 아니라 ROE, 자본비율, 주주환원이 같이 리레이팅을 설명해야 한다.
- success_requires: roe_improvement, capital_ratio_stable, credit_cost_stable, capital_return_execution
- reject_if: low_pbr_only, pf_credit_cost, capital_ratio_deterioration, roe_decline
- expected_rerating_result: true_rerating_or_no_rerating
- stage_failure_focus: false_green, false_yellow
- score_weight_adjustment_hint: Reward ROE/PBR and executed return; penalize credit cost risk.
- Green policy: Green possible with ROE/PBR gap plus executed shareholder return.

### GAME_CONTENT_IP
- principle: 신작 기대와 반복 IP monetization을 분리해서 검증한다.
- success_requires: actual_revenue_conversion, ip_repeatability, global_sales, op_eps_revision
- reject_if: new_game_hype_only, single_ip_dependence, launch_failure, contract_or_scandal_risk
- expected_rerating_result: true_rerating_or_event_premium
- stage_failure_focus: false_green, should_have_been_red
- score_weight_adjustment_hint: Give credit after revenue conversion; heavily penalize pre-launch hype.
- Green policy: Green requires repeat monetization, not release anticipation.

### HOLDING_RESTRUCTURING_GOVERNANCE
- principle: 이벤트 프리미엄과 구조적 discount narrowing을 분리한다.
- success_requires: buyback_cancellation_or_return, nav_discount_catalyst, fcf_support, governance_execution
- reject_if: governance_dispute_only, buyback_without_cancel, subsidiary_value_impairment, event_premium_only
- expected_rerating_result: event_premium_or_true_rerating
- stage_failure_focus: false_yellow, stage2_watch_success
- score_weight_adjustment_hint: Score executed shareholder return and NAV/FCF support above event headlines.
- Green policy: Green requires executed capital return backed by NAV/FCF improvement.

### MEDICAL_DEVICE_HEALTHCARE_EXPORT
- principle: 단일 장비 판매가 아니라 반복 소모품/수출 재주문이 리레이팅을 설명해야 한다.
- success_requires: export_country_expansion, repeat_consumable_revenue, opm_roe, fy1_fy2_eps_revision
- reject_if: single_device_sale, approval_delay, competition_intensifies, asp_decline
- expected_rerating_result: true_rerating
- stage_failure_focus: missed_structural, false_yellow
- score_weight_adjustment_hint: Increase repeat revenue visibility; do not over-score one-time device sales.
- Green policy: Green possible with export channel plus recurring revenue and FCF proof.

### NUCLEAR_SMR_GRID_POLICY
- principle: 정책 기대와 실제 계약/매출 전환을 분리한다.
- success_requires: binding_contract, revenue_conversion_path, project_financing, margin_visibility
- reject_if: policy_headline_only, legal_delay, project_financing_absent, cost_overrun
- expected_rerating_result: policy_event_rerating_or_true_rerating
- stage_failure_focus: false_yellow, should_have_been_red
- score_weight_adjustment_hint: Keep policy signal as radar unless contract economics are visible.
- Green policy: Green only with contract economics and low legal/policy risk.

### PLATFORM_SOFTWARE_INTERNET
- principle: MAU나 트래픽이 아니라 ARPU, take-rate, OPM, FCF가 주가 경로와 맞아야 한다.
- success_requires: arpu_or_take_rate_up, opm_improvement, fcf_improvement, rerating_after_monetization
- reject_if: mau_without_monetization, traffic_only, ai_cost_overrun, regulatory_margin_hit
- expected_rerating_result: true_rerating_or_no_rerating
- stage_failure_focus: false_yellow, missed_structural
- score_weight_adjustment_hint: Increase monetization/OPM proof; do not score MAU as structural visibility by itself.
- Green policy: Green is rare and requires monetization plus margin/FCF proof.

### RETAIL_DOMESTIC_CONSUMER
- principle: 단순 반등이 아니라 2-4개 분기 OPM/FCF 개선이 이어지는지 본다.
- success_requires: same_store_sales, opm_improvement, fcf_improvement, inventory_normalization
- reject_if: traffic_only_rebound, inventory_build, wage_or_rent_pressure, one_quarter_rebound
- expected_rerating_result: true_rerating_or_cyclical_rerating
- stage_failure_focus: false_yellow, evidence_good_but_price_failed
- score_weight_adjustment_hint: Require repeated margin/FCF evidence before structural credit.
- Green policy: Green requires durable store efficiency or cash-flow improvement.

### ROBOTICS_FACTORY_AUTOMATION
- principle: 대기업 투자나 MOU는 Stage 1/2 재료지만, 실제 매출/OP 전환 전 Green은 막는다.
- success_requires: customer_adoption, revenue_conversion, repeat_order, opm_improvement
- reject_if: theme_only_mou, strategic_investment_without_revenue, cash_burn, price_only_rally
- expected_rerating_result: theme_overheat_or_true_rerating
- stage_failure_focus: should_have_been_red, missed_structural
- score_weight_adjustment_hint: Treat strategic investment as radar; score revenue conversion separately.
- Green policy: Green blocked until revenue and margin evidence are visible.

### TRAVEL_LEISURE_REOPENING
- principle: 리오프닝 반등과 구조적 수익성 개선을 구분한다.
- success_requires: visitor_recovery, fixed_cost_leverage, op_eps_revision, customer_mix_improvement
- reject_if: one_time_reopening, oil_or_fx_shock, china_tourism_dependency, demand_slowdown
- expected_rerating_result: cyclical_rerating_or_no_rerating
- stage_failure_focus: false_yellow, should_have_been_red
- score_weight_adjustment_hint: Treat reopening as cyclical unless repeated margin/FCF improvement exists.
- Green policy: Green exceptional; most cases stay Yellow/Watch.

### UTILITIES_REGULATED_TARIFF
- principle: 저평가가 아니라 요금, 원가보상, 부채 정상화가 가격 경로와 맞아야 한다.
- success_requires: tariff_or_cost_pass_through, debt_normalization, cash_flow_improvement, policy_durability
- reject_if: tariff_freeze, policy_event_only, debt_burden, dividend_capacity_absent
- expected_rerating_result: policy_event_rerating_or_no_rerating
- stage_failure_focus: false_yellow, should_have_been_red
- score_weight_adjustment_hint: Score policy durability and balance-sheet repair, not low valuation alone.
- Green policy: Green requires durable regulatory regime change.

## What Not To Change
- Do not change StageClassifier thresholds from Round 4.
- Do not use case records as candidate-generation input.
- Do not treat price-only rallies as structural rerating.
