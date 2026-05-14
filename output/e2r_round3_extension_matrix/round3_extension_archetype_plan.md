# Round-3 Extension Archetype Matrix

Source round: `docs/round/round_03.md`

This is calibration material. It does not change production scoring.

## Stage Posture Levels

- `GREEN_ELIGIBLE`: Green can exist later, but only with strict cross-evidence.
- `YELLOW_WATCH`: useful candidates, but Green is exceptional.
- `RED_4B_GUARDRAIL`: mainly used to prevent unsafe Green or detect 4B/4C.

## Priority Queue

| rank | archetype | posture | direct positives | direct counterexamples | status |
|---:|---|---|---:|---:|---|
| 1 | CONTRACT_BACKLOG_INDUSTRIAL | GREEN_ELIGIBLE | 3 | 1 | needs_more_cases |
| 2 | DEFENSE_GOVERNMENT_BACKLOG | GREEN_ELIGIBLE | 1 | 1 | needs_more_cases |
| 3 | SHIPBUILDING_OFFSHORE_BACKLOG | GREEN_ELIGIBLE | 1 | 1 | needs_more_cases |
| 4 | EXPORT_RECURRING_CONSUMER | GREEN_ELIGIBLE | 1 | 2 | needs_more_cases |
| 5 | K_BEAUTY_EXPORT_DISTRIBUTION | GREEN_ELIGIBLE | 2 | 2 | covered_2x2 |
| 6 | MEMORY_HBM_CAPACITY | GREEN_ELIGIBLE | 2 | 2 | covered_2x2 |
| 7 | SEMI_EQUIPMENT_CAPEX | GREEN_ELIGIBLE | 1 | 1 | needs_more_cases |
| 8 | FINANCIAL_SPREAD_BALANCE_SHEET | GREEN_ELIGIBLE | 0 | 2 | needs_more_cases |
| 9 | MEDICAL_DEVICE_HEALTHCARE_EXPORT | GREEN_ELIGIBLE | 1 | 2 | needs_more_cases |
| 10 | THEME_VALUATION_OVERHEAT | RED_4B_GUARDRAIL | 0 | 1 | needs_more_cases |
| 11 | ONE_OFF_EVENT_DEMAND | RED_4B_GUARDRAIL | 0 | 1 | needs_more_cases |
| 12 | AI_DATA_CENTER_INFRASTRUCTURE | GREEN_ELIGIBLE | 2 | 1 | needs_more_cases |
| 13 | ROBOTICS_FACTORY_AUTOMATION | YELLOW_WATCH | 0 | 2 | needs_more_cases |
| 14 | PLATFORM_SOFTWARE_INTERNET | YELLOW_WATCH | 2 | 2 | covered_2x2 |
| 15 | GAME_CONTENT_IP | YELLOW_WATCH | 1 | 1 | needs_more_cases |
| 16 | SHIPPING_FREIGHT_CYCLE | RED_4B_GUARDRAIL | 1 | 1 | needs_more_cases |
| 17 | CONSTRUCTION_REAL_ESTATE_CREDIT | RED_4B_GUARDRAIL | 0 | 2 | guardrail_counterexamples_present |
| 18 | UTILITIES_REGULATED_TARIFF | YELLOW_WATCH | 0 | 0 | needs_more_cases |
| 19 | NUCLEAR_SMR_GRID_POLICY | YELLOW_WATCH | 0 | 2 | needs_more_cases |
| 20 | HOLDING_RESTRUCTURING_GOVERNANCE | YELLOW_WATCH | 0 | 3 | needs_more_cases |
| 21 | TRAVEL_LEISURE_REOPENING | YELLOW_WATCH | 1 | 1 | needs_more_cases |
| 22 | BIOTECH_REGULATORY | RED_4B_GUARDRAIL | 0 | 0 | needs_more_cases |
| 23 | RARE_METALS_STRATEGIC_MATERIALS | YELLOW_WATCH | 0 | 0 | needs_more_cases |

## Extension Details

### FINANCIAL_SPREAD_BALANCE_SHEET
- posture: GREEN_ELIGIBLE
- structure: ROE 지속성 + PBR-ROE gap + 자본비율 + 주주환원
- must_have_fields: roe_improvement, cet1_or_capital_ratio_stable, credit_cost_stable, capital_return_execution
- red_flag_fields: pf_credit_cost, capital_ratio_deterioration, roe_decline
- example_cases: KB금융, 신한지주, 메리츠금융, 단순 저PBR 지방은행
- Green policy: Green possible only with ROE/PBR and executed capital return, not low PBR alone.

### MEDICAL_DEVICE_HEALTHCARE_EXPORT
- posture: GREEN_ELIGIBLE
- structure: 의료/미용기기 수출 -> 소모품/반복 매출 -> OPM/ROE
- must_have_fields: export_country_expansion, consumable_or_repeat_revenue, opm_roe, fy1_fy2_eps_revision
- red_flag_fields: approval_delay, competition_intensifies, asp_decline
- example_cases: Classys, 파마리서치, 휴젤, 원텍
- Green policy: Green possible with export channel plus recurring consumable/service revenue.

### AI_DATA_CENTER_INFRASTRUCTURE
- posture: GREEN_ELIGIBLE
- structure: AI 데이터센터 증설 -> 전력/냉각/서버/네트워크 병목 -> 다년 CAPEX -> 수주잔고와 EPS 상향
- must_have_fields: confirmed_orders, customer_capex_visibility, op_eps_revision, capacity_bottleneck
- red_flag_fields: ai_capex_cut, data_center_delay, theme_without_revenue
- example_cases: HD현대일렉트릭/효성중공업 전력망, 이수페타시스 AI 서버 PCB
- Green policy: Green possible only with confirmed order/revenue exposure, not AI keyword exposure.

### ROBOTICS_FACTORY_AUTOMATION
- posture: YELLOW_WATCH
- structure: 테마 기대 -> 실제 고객사 도입 -> 수주/매출 전환 -> 반복 서비스/SW 매출
- must_have_fields: customer_adoption, revenue_conversion, repeat_service_or_consumables, gross_margin_improvement
- red_flag_fields: theme_only_mou, no_revenue, cash_flow_deterioration
- example_cases: Rainbow Robotics, Doosan Robotics, 무실적 로봇 테마주
- Green policy: Green very restricted until repeat revenue and OPM evidence are visible.

### PLATFORM_SOFTWARE_INTERNET
- posture: YELLOW_WATCH
- structure: MAU/traffic -> ARPU/take rate -> 비용 효율화 -> OPM leverage
- must_have_fields: arpu_or_take_rate_up, opm_improvement, recurring_revenue, fy1_fy2_op_revision
- red_flag_fields: mau_without_monetization, regulation, ai_cost_overrun
- example_cases: NAVER, Kakao turnaround, 더존비즈온
- Green policy: MAU alone cannot create Green; monetization and margin leverage are required.

### GAME_CONTENT_IP
- posture: YELLOW_WATCH
- structure: IP/신작/팬덤 -> 글로벌 매출 -> 반복 monetization -> OPM leverage
- must_have_fields: actual_revenue_conversion, ip_repeatability, global_monetization, op_eps_revision
- red_flag_fields: new_game_hype_only, single_ip_dependence, contract_or_scandal_risk
- example_cases: Krafton, Shift Up, HYBE/JYP/SM, 신작 기대만 있는 게임주
- Green policy: Green restricted unless IP portfolio and repeat monetization are proven.

### CONSTRUCTION_REAL_ESTATE_CREDIT
- posture: RED_4B_GUARDRAIL
- structure: 수주/분양보다 PF·현금흐름·원가율이 먼저인 credit-sensitive archetype
- must_have_fields: cash_flow_improvement, cost_ratio_stable, debt_reduction, pf_risk_low
- red_flag_fields: pf_loss, unsold_inventory, liquidity_stress, credit_rating_downgrade
- example_cases: PF 리스크 해소형 건설사, Taeyoung E&C류 PF 문제
- Green policy: Green very restricted; order headline cannot override PF/cash-flow risk.

### UTILITIES_REGULATED_TARIFF
- posture: YELLOW_WATCH
- structure: 정책·요금·원가 -> EPS 턴어라운드, but regulation risk remains
- must_have_fields: tariff_or_cost_improvement, cash_flow_improvement, debt_normalization
- red_flag_fields: tariff_freeze, policy_reversal, debt_burden
- example_cases: KEPCO, 한국가스공사
- Green policy: Watch by default; Green needs durable cost pass-through regime change.

### NUCLEAR_SMR_GRID_POLICY
- posture: YELLOW_WATCH
- structure: 정책/수출 수주 -> project financing/기자재 매출화 -> 규제·소송 리스크 확인
- must_have_fields: actual_contract_or_loi, project_financing, revenue_conversion_path
- red_flag_fields: legal_delay, policy_reversal, cost_overrun
- example_cases: 두산에너빌리티, 체코 원전 정책계약, 원전 법적 지연
- Green policy: Watch by default; Green requires binding contract economics and low legal/policy risk.

### HOLDING_RESTRUCTURING_GOVERNANCE
- posture: YELLOW_WATCH
- structure: NAV discount -> 자사주/소각/배당/지배구조 개선 -> Korea discount 해소
- must_have_fields: actual_cancellation_or_return, nav_discount_catalyst, governance_execution
- red_flag_fields: buyback_without_cancel, subsidiary_value_impairment, event_premium_only
- example_cases: SK스퀘어, 삼성물산, Korea Zinc governance battle
- Green policy: Watch until capital return is executed and backed by FCF/NAV improvement.

### TRAVEL_LEISURE_REOPENING
- posture: YELLOW_WATCH
- structure: 출입국/관광 회복 -> 고정비 레버리지 -> OP/EPS 상향, but cycle/policy risk remains
- must_have_fields: visitor_recovery, op_eps_revision, fixed_cost_leverage, customer_mix
- red_flag_fields: oil_or_fx_shock, china_tourism_dependency, demand_slowdown
- example_cases: 대한항공 리오프닝, 면세 중국 관광 의존
- Green policy: Normally Watch/Yellow; Green needs repeat visitor growth and low China/oil/FX dependence.

### BIOTECH_REGULATORY
- posture: RED_4B_GUARDRAIL
- structure: 임상/허가/기술이전 -> 매출화/로열티 전환 여부가 핵심
- must_have_fields: milestone_payment, commercialization_path, cash_runway
- red_flag_fields: clinical_failure, approval_delay, cb_or_rights_dilution
- example_cases: 알테오젠, 유한양행, 임상 뉴스만 있는 바이오
- Green policy: Pre-revenue clinical stories are Green-blocked; royalty or revenue conversion is required.

### RARE_METALS_STRATEGIC_MATERIALS
- posture: YELLOW_WATCH
- structure: 제련마진/전략금속 공급망/거버넌스 이벤트가 섞이는 소재 archetype
- must_have_fields: smelting_margin, strategic_supply_chain, fcf_or_governance_improvement
- red_flag_fields: pure_metal_price_rally, event_premium_only, governance_dispute_drag
- example_cases: Korea Zinc governance battle, 순수 금속가격 상승 반례
- Green policy: Watch by default; event premium alone is not structural Green.

### RETAIL_DOMESTIC_CONSUMER
- posture: YELLOW_WATCH
- structure: 소비 회복 -> 점포효율/객단가/비용 레버리지 -> OPM 개선
- must_have_fields: same_store_sales, opm_improvement, inventory_normalization, high_margin_mix
- red_flag_fields: inventory_increase, online_competition, rent_or_wage_pressure
- example_cases: BGF리테일/CU, GS리테일/GS25, 단기 소비 회복 테마
- Green policy: Watch by default; Green requires structural store efficiency and FCF improvement.

## What Not To Change
- Do not change StageClassifier thresholds from this matrix.
- Do not use case records as candidate-generation input.
- Do not treat extension labels as stock-name rules.
- Keep one-off, theme, construction/PF, and pre-revenue biotech Green-restricted.
