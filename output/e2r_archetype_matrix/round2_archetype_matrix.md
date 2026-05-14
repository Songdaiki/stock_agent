# Round-2 E2R Archetype Matrix

This is calibration material. It is not production scoring.

| priority | archetype | structure | Green policy |
|---:|---|---|---|
| 1 | CONTRACT_BACKLOG_INDUSTRIAL | 수요 급증 -> 장기공급계약/수주잔고/CAPA 부족 -> 가격 전가 -> EPS/FCF 상향 | Green allowed only with disclosure + financial actual + research/consensus-revision cross evidence. |
| 1 | DEFENSE_GOVERNMENT_BACKLOG | 지정학/국방비 증가 -> 정부 고객 장기계약 -> 수주잔고/납품 스케줄 -> 매출/OP visibility | Green allowed with government customer, delivery visibility, and margin/revision evidence. |
| 2 | SHIPBUILDING_OFFSHORE_BACKLOG | 선가 상승/수주 슬롯 -> 저가수주 소진 -> 고마진 선박 인도 -> EPS 턴어라운드 | Green allowed selectively; low-margin backlog and cancellation risk must be cleared. |
| 1 | EXPORT_RECURRING_CONSUMER | 해외 수요 -> 채널 확장 -> 반복소비/ASP/OPM -> 내수 소비재 프레임 제거 | Contract quality is not required; recurring export demand and EPS/OP revision are required. |
| 1 | K_BEAUTY_EXPORT_DISTRIBUTION | K뷰티 글로벌 수요 -> 미국/일본/유럽 채널 -> 반복 주문/OPM/ROE -> 중국 의존 프레임 제거 | Green allowed through export/channel/recurring-demand evidence, not contract quality. |
| 1 | MEMORY_HBM_CAPACITY | AI 수요 -> HBM/DRAM/NAND 수요 -> CAPA 재배치/공급규율 -> 다년 EPS/FCF 상향 | Green allowed with memory-specific revision, pricing, supply discipline, and capacity evidence. |
| 2 | SEMI_EQUIPMENT_CAPEX | 고객사 AI/HBM capex -> 병목 장비/소재 -> 수주잔고/매출화 -> OP leverage | Green allowed with confirmed order-to-revenue conversion and customer capex durability. |
| 2 | MEDICAL_DEVICE_HEALTHCARE_EXPORT | 의료/미용기기 수출 -> 소모품/반복 매출 -> OPM/ROE | Green allowed with export channel plus repeat consumable/service revenue. |
| 2 | FINANCIAL_SPREAD_BALANCE_SHEET | ROE + 저PBR + 자본정책 -> Korea discount 해소 -> PBR-ROE rerating | Green allowed with ROE/PBR and durable capital return, not low PBR alone. |
| 2 | TURNAROUND_COST_RESTRUCTURING | 적자사업 제거/고정비 leverage -> OP 흑자전환 -> EPS 체급 변화 | Green allowed only when cost improvement is recurring and paired with growth/FCF. |
| 2 | COMMODITY_SPREAD | 제품가격-원가 스프레드 -> OP leverage, but usually cyclical rather than structural | Green restricted by cycle cap unless structural cost-curve or supply discipline is explicit. |
| 1 | SHIPPING_FREIGHT_CYCLE | 운임 급등 -> EPS 폭발 -> 공급/수요 정상화 시 급락 위험 | Green very restricted; normally cyclical success or Yellow/Red rather than structural Green. |
| 2 | BATTERY_MATERIALS_CAPEX_OVERHEAT | EV 기대 -> 장기공급계약/CAPA 투자 -> 원자재/수요/CAPA 과잉 리스크 | Green highly restricted; overheat and CAPA overbuild penalties dominate unless contract economics are clear. |
| 2 | AUTO_MOBILITY_COMPONENTS | 믹스/수출/환율/주주환원 -> EPS/FCF 안정 성장 -> 저평가 프레임 해소 | Green allowed with durable mix/FCF/return evidence; component cost pass-through must be proven. |
| 3 | CONSTRUCTION_REAL_ESTATE_CREDIT | 수주보다 PF/신용/원가가 핵심 | Green very restricted; credit and cash-flow evidence must dominate order headline. |
| 3 | UTILITIES_REGULATED_TARIFF | 요금/원가/정책 -> EPS 턴어라운드, but regulation risk remains high | Green restricted unless tariff pass-through regime changes, not just one-time relief. |
| 3 | BIOTECH_REGULATORY | 임상/허가/기술이전 -> 매출화/로열티 전환 여부가 핵심 | Green blocked before real revenue/royalty and dilution control. |
| 3 | ROBOTICS_FACTORY_AUTOMATION | 테마 기대 -> 실제 수주/매출 전환 여부가 핵심 | Green restricted until revenue conversion and repeatability are proven. |
| 3 | PLATFORM_SOFTWARE_INTERNET | MAU/ARPU/광고/커머스 -> 수익화와 OPM leverage -> 플랫폼 프레임 재평가 | Green allowed only with monetization and margin leverage, not MAU alone. |
| 3 | GAME_CONTENT_IP | 신작/IP/콘텐츠 -> 글로벌 매출 -> 반복 monetization 여부가 핵심 | Green restricted unless IP repeatability and monetization are visible. |
| 3 | HOLDING_RESTRUCTURING_GOVERNANCE | NAV discount -> 자사주/소각/지배구조 개선 -> Korea discount 해소 | Green allowed only if governance action is backed by FCF/NAV improvement. |
| 1 | ONE_OFF_EVENT_DEMAND | 일회성 수요 -> EPS 폭발 -> 다음 해 정상화 | Green blocked by default; normally Stage 3-Red/Yellow guardrail. |
| 1 | THEME_VALUATION_OVERHEAT | 테마/주가 급등/밸류 과열 -> EPS/FCF가 따라오지 않으면 붕괴 | Green blocked unless real EPS/FCF evidence overwhelms overheat risk. |
| 3 | RETAIL_DOMESTIC_CONSUMER | 소비 회복/점포효율/비용 leverage -> OP 개선 | Green restricted unless OP/FCF improvement is structural, not traffic-only. |
| 3 | GENERIC_UNCLASSIFIED | 아직 명확한 E2R 구조가 배정되지 않은 종목 | Green blocked until a real archetype and evidence family are assigned. |

## Stage Criteria

### CONTRACT_BACKLOG_INDUSTRIAL
- success_cases: HD현대일렉트릭, 일진전기
- success_candidate_cases: 효성중공업, LS ELECTRIC, 제룡전기
- counterexample_cases: 대한전선-like, 단기 공급계약 테마주
- Stage 1: supply_contract_disclosure, trading_value_spike, backlog_keyword
- Stage 2: contract_amount_to_sales_10pct_plus, contract_duration_24m_plus, op_eps_revision, backlog_growth
- Stage 3: backlog_to_sales_100pct_plus, lead_time_extended, capa_shortage, asp_opm_improvement, fy1_fy2_eps_revision
- 4B: target_price_raises_cluster, excessive_price_runup, new_order_slowdown, revision_momentum_slowdown
- 4C: contract_cancellation_or_delay, asp_opm_decline, backlog_decline, oversupply
- price_patterns: STAIR_STEP_RERATING, SECTOR_SPREAD_RERATING, MARGIN_NORMALIZATION_RERATING

### DEFENSE_GOVERNMENT_BACKLOG
- success_cases: 한화에어로스페이스
- success_candidate_cases: 현대로템, LIG넥스원, 한국항공우주
- counterexample_cases: 단순 방산 테마주, 납기 지연/원가 상승 방산
- Stage 1: defense_contract_news, government_customer, geopolitical_momentum
- Stage 2: order_backlog_to_sales_rising, multi_year_delivery_schedule, op_eps_revision
- Stage 3: government_customer, multi_year_contract, delivery_visibility, opm_improvement, fy2_fy3_revision
- 4B: defense_sector_overheat, valuation_consensus_saturated, new_contract_expectation_priced_in
- 4C: delivery_delay, cost_overrun, contract_cancellation, export_approval_or_political_risk
- price_patterns: BACKLOG_RERATING, PROGRAM_MILESTONE_RERATING

### SHIPBUILDING_OFFSHORE_BACKLOG
- success_cases: -
- success_candidate_cases: 삼성중공업, HD현대중공업, HD한국조선해양, 한화오션
- counterexample_cases: 러시아/Zvezda 계약 리스크, 저가수주 잔존 조선사
- Stage 1: large_order, newbuild_price_index_up, shipbuilding_trading_value_spike
- Stage 2: low_margin_backlog_rolloff, high_margin_delivery_start, op_turnaround_revision
- Stage 3: backlog_quality_improvement, fy2_fy3_ship_price_reflection, cost_stability, long_delivery_slots
- 4B: order_peak, newbuild_price_slowdown, valuation_saturated
- 4C: contract_cancellation, steel_or_labor_cost_spike, delivery_delay, order_cycle_slowdown
- price_patterns: PRICE_ORDER_RERATING, BACKLOG_RERATING, CYCLE_SPIKE_NORMALIZATION

### EXPORT_RECURRING_CONSUMER
- success_cases: 삼양식품
- success_candidate_cases: 농심, 오리온
- counterexample_cases: 단일 제품 유행, 원가 상승 음식료, 리콜/규제 소비재
- Stage 1: export_growth, earnings_surprise, overseas_channel_news
- Stage 2: fy1_fy2_eps_revision, export_ratio_rising, opm_expansion, target_price_revision
- Stage 3: recurring_consumption, channel_diversification, asp_hold, capa_and_volume_growth, old_domestic_frame
- 4B: margin_peak, global_brand_consensus_crowded, inventory_or_channel_stuffing_risk
- 4C: export_growth_slowdown, overseas_inventory_issue, asp_opm_decline, regulatory_or_recall_issue
- price_patterns: EXPORT_CHANNEL_RERATING, STAIR_STEP_RERATING

### K_BEAUTY_EXPORT_DISTRIBUTION
- success_cases: -
- success_candidate_cases: 실리콘투, 코스맥스, 한국콜마, APR, 브이티
- counterexample_cases: 중국 의존 화장품, 인디 브랜드 유행성 과열, 채널 재고/매출채권 리스크
- Stage 1: us_japan_europe_export_growth, kbeauty_channel_news, cosmetics_export_data
- Stage 2: fy1_fy2_op_eps_revision, opm_roe_improvement, channel_expansion, customer_diversification
- Stage 3: repeat_orders, offline_or_major_retail_entry, no_inventory_receivable_problem, china_dependence_down, old_china_cosmetics_frame
- 4B: kbeauty_overcrowding, new_brand_saturation, target_price_overheat
- 4C: sell_through_slowdown, inventory_increase, receivables_deterioration, tariff_or_regulation_impact
- price_patterns: EXPORT_CHANNEL_RERATING, THEME_FRONT_RUN

### MEMORY_HBM_CAPACITY
- success_cases: SK하이닉스
- success_candidate_cases: 삼성전자 메모리, Micron
- counterexample_cases: 단순 메모리 가격 반등, 공급과잉 전환
- Stage 1: memory_price_increase, hbm_demand, earnings_turnaround
- Stage 2: fy1_fy2_fy3_op_eps_revision, customer_supply_race, supply_discipline, price_increase
- Stage 3: lta_or_prepayment_or_price_band, capa_constraint, multi_year_consensus_revision, pbr_to_per_frame_shift
- 4B: per_rerating_consensus, target_multiple_saturated, capex_expansion_news, customer_price_resistance
- 4C: dram_nand_hbm_price_decline, oversupply, customer_ai_capex_slowdown, consensus_revision_down
- price_patterns: CAPACITY_BOTTLENECK_RERATING, STAIR_STEP_RERATING, CYCLE_SPIKE_NORMALIZATION

### SEMI_EQUIPMENT_CAPEX
- success_cases: -
- success_candidate_cases: 한미반도체, 이수페타시스, ISC, 리노공업
- counterexample_cases: 단일 고객 장비주, 국산화 테마 장비주
- Stage 1: customer_capex_news, equipment_order, ai_hbm_keyword
- Stage 2: backlog_growth, customer_diversification, revenue_conversion, op_eps_revision
- Stage 3: bottleneck_equipment_position, long_customer_capex_path, repeat_or_consumable_demand, high_opm
- 4B: capex_peak, customer_order_slowdown, equipment_lead_time_normalization
- 4C: order_cancellation, customer_capex_cut, inventory_build
- price_patterns: CAPACITY_BOTTLENECK_RERATING, CYCLE_SPIKE_NORMALIZATION

### MEDICAL_DEVICE_HEALTHCARE_EXPORT
- success_cases: -
- success_candidate_cases: 클래시스, 휴젤, 파마리서치, 원텍
- counterexample_cases: 단일 장비 판매, 규제/허가 지연
- Stage 1: export_country_expansion, approval, new_product
- Stage 2: consumable_or_repeat_revenue, opm_roe, fy1_fy2_eps_revision
- Stage 3: global_channel, repeat_consumable_structure, high_fcf_conversion
- 4B: medical_beauty_crowding, margin_peak, valuation_saturation
- 4C: approval_delay, regulation, competition_intensifies
- price_patterns: EXPORT_CHANNEL_RERATING, DIRECT_RERATING

### FINANCIAL_SPREAD_BALANCE_SHEET
- success_cases: -
- success_candidate_cases: KB금융, 신한지주, 하나금융, 메리츠금융
- counterexample_cases: 단순 저PBR 금융주, PF/충당금 리스크 금융
- Stage 1: value_up_disclosure, buyback_or_dividend, low_pbr
- Stage 2: roe_improvement, capital_ratio_stable, credit_cost_stable, capital_return_durability
- Stage 3: pbr_roe_frame_change, recurring_roe, credible_shareholder_return
- 4B: pbr_gap_closed, return_policy_fully_priced, roe_peak
- 4C: credit_cost_up, pf_loss, capital_ratio_deterioration
- price_patterns: VALUE_UP_RERATING

### TURNAROUND_COST_RESTRUCTURING
- success_cases: -
- success_candidate_cases: 적자사업 매각 기업, 흑자전환 제조/플랫폼
- counterexample_cases: 일회성 비용절감, 구조조정 실패
- Stage 1: loss_reduction, cost_cut
- Stage 2: op_turnaround, cash_flow_improvement
- Stage 3: recurring_margin, growth_and_cost_structure_improve_together
- 4B: turnaround_fully_priced, margin_peak
- 4C: restructuring_failure, debt_or_liquidity_risk
- price_patterns: DIRECT_RERATING

### COMMODITY_SPREAD
- success_cases: -
- success_candidate_cases: 정유 spread 회복주, 철강 spread 회복주, 비철/제련 구조주
- counterexample_cases: 순수 가격 사이클, 중국 공급과잉 화학
- Stage 1: product_price_up, spread_improvement
- Stage 2: op_eps_revision, inventory_demand_improvement, cost_structure_improvement
- Stage 3: cost_curve_advantage, capacity_discipline, long_term_supply_constraint
- 4B: spread_peak, inventory_build, broad_consensus_bullish
- 4C: spread_reversal, china_or_global_capacity_addition, demand_slowdown
- price_patterns: CYCLE_SPIKE_NORMALIZATION

### SHIPPING_FREIGHT_CYCLE
- success_cases: HMM 2020~2021
- success_candidate_cases: Maersk 2020~2021
- counterexample_cases: HMM 고점 이후, Maersk 2024, 신규 선복 증가
- Stage 1: freight_rate_spike, spot_rate_surge
- Stage 2: contract_freight_reflection, op_eps_explosion, vessel_shortage
- Stage 3: multi_year_contract_freight, fleet_supply_constraint
- 4B: freight_rate_peak, spot_future_divergence, new_vessel_supply
- 4C: freight_rate_drop, overcapacity, demand_slowdown
- price_patterns: CYCLE_SPIKE_NORMALIZATION

### BATTERY_MATERIALS_CAPEX_OVERHEAT
- success_cases: -
- success_candidate_cases: 초기 양극재 장기계약 구간
- counterexample_cases: 에코프로비엠/에코프로 2023, CAPA 과잉 소재주, 단순 테마 소재주
- Stage 1: long_term_contract, capa_expansion, ev_demand_expectation
- Stage 2: price_and_margin_rising_together, customer_contract_quality, capex_without_fcf_damage
- Stage 3: long_term_contract, price_pass_through, demand_durability, valuation_runway
- 4B: price_runup, crowding, per_pbr_overheat, revision_slowdown
- 4C: ev_demand_slowdown, mineral_price_decline, capa_overbuild, margin_compression
- price_patterns: THEME_FRONT_RUN, CYCLE_SPIKE_NORMALIZATION

### AUTO_MOBILITY_COMPONENTS
- success_cases: -
- success_candidate_cases: 현대차, 기아, 현대모비스, HL만도
- counterexample_cases: 원가전가 실패 부품주, EV 수요 둔화 부품주
- Stage 1: sales_mix_fx_improvement, shareholder_return_announcement
- Stage 2: op_eps_revision, high_margin_mix, shareholder_return
- Stage 3: global_share_gain, valuation_discount_resolution, roe_fcf_durability
- 4B: peak_margin, tariff_policy_risk, valuation_rerating_complete
- 4C: tariff_or_demand_slowdown, cost_increase, recall_or_quality_cost
- price_patterns: VALUE_UP_RERATING, MARGIN_NORMALIZATION_RERATING

### CONSTRUCTION_REAL_ESTATE_CREDIT
- success_cases: -
- success_candidate_cases: PF 리스크 해소 건설사, 해외 플랜트/인프라 수주
- counterexample_cases: PF 부실 건설사, 원가 상승 미반영
- Stage 1: order_or_presale_recovery, pf_concern_eases
- Stage 2: cost_ratio_stabilizes, cash_flow_improves, debt_reduction
- Stage 3: post_restructuring_repeat_cash_flow
- 4B: credit_relief_fully_priced, order_quality_ignored
- 4C: pf_loss, unsold_inventory_increase, credit_rating_downgrade
- price_patterns: DIRECT_RERATING

### UTILITIES_REGULATED_TARIFF
- success_cases: -
- success_candidate_cases: 한국전력, 한국가스공사
- counterexample_cases: 요금 동결, 부채/정책 리스크
- Stage 1: tariff_or_cost_improvement, policy_change
- Stage 2: loss_reduction, cash_flow_improvement
- Stage 3: regulatory_frame_change, durable_tariff_pass_through
- 4B: policy_relief_fully_priced, debt_burden_ignored
- 4C: tariff_freeze, cost_spike, debt_pressure
- price_patterns: DIRECT_RERATING

### BIOTECH_REGULATORY
- success_cases: -
- success_candidate_cases: 알테오젠, 유한양행
- counterexample_cases: 임상 뉴스만 있는 바이오, 임상 실패/허가 지연, CB/유증 반복 바이오
- Stage 1: clinical_approval_or_license_news
- Stage 2: milestone_payment, commercialization_path, cash_flow_improvement
- Stage 3: actual_sales_or_royalty, eps_fcf_conversion, low_dilution_risk
- 4B: royalty_curve_priced, clinical_news_crowded
- 4C: clinical_failure, approval_delay, rights_or_cb_dilution
- price_patterns: REGULATORY_REVENUE_CONVERSION, THEME_FRONT_RUN

### ROBOTICS_FACTORY_AUTOMATION
- success_cases: -
- success_candidate_cases: 레인보우로보틱스, 스마트팩토리 장비주
- counterexample_cases: 로봇 테마 고밸류, 단발성 MOU
- Stage 1: strategic_investment, robot_theme, order_news
- Stage 2: revenue_conversion, customer_diversification, op_improvement
- Stage 3: repeat_revenue_or_consumables, customer_lock_in, cost_leverage
- 4B: order_delay, missed_results, valuation_overheat
- 4C: revenue_failure, customer_order_cut, theme_unwind
- price_patterns: DIRECT_RERATING

### PLATFORM_SOFTWARE_INTERNET
- success_cases: -
- success_candidate_cases: 네이버, 더존비즈온
- counterexample_cases: MAU만 높은 플랫폼, 규제 리스크 플랫폼
- Stage 1: mau_traffic_recovery, ad_commerce_improvement
- Stage 2: arpu_up, op_leverage, cost_efficiency
- Stage 3: recurring_revenue, pricing_power, margin_expansion, old_frame_valuation
- 4B: platform_multiple_saturated, ai_cost_ignored, crowded_reports
- 4C: regulation, take_rate_decline, traffic_decline
- price_patterns: DIRECT_RERATING

### GAME_CONTENT_IP
- success_cases: -
- success_candidate_cases: 크래프톤, 하이브, JYP, 에스엠
- counterexample_cases: 신작 기대만 있는 게임주, 엔터 계약/스캔들 리스크
- Stage 1: new_game_or_comeback_or_tour, traffic_or_preorder
- Stage 2: revenue_conversion, opm_eps_revision
- Stage 3: ip_repeatability, global_monetization, low_churn
- 4B: hit_peak, crowded_ip_reports, valuation_saturation
- 4C: new_game_failure, contract_risk, core_ip_damage
- price_patterns: DIRECT_RERATING

### HOLDING_RESTRUCTURING_GOVERNANCE
- success_cases: -
- success_candidate_cases: SK스퀘어, 삼성물산, value-up 지주사
- counterexample_cases: 주주환원 없는 저PBR 지주사, 자회사 가치 훼손
- Stage 1: buyback_or_cancellation_or_dividend, governance_reform
- Stage 2: nav_discount_narrowing_catalyst, subsidiary_earnings_improvement
- Stage 3: structural_governance_change, repeat_shareholder_return, foreign_ownership_rerating
- 4B: event_premium_fully_priced, return_policy_no_longer_incremental
- 4C: controlling_shareholder_risk, subsidiary_value_impairment
- price_patterns: DIRECT_RERATING

### ONE_OFF_EVENT_DEMAND
- success_cases: -
- success_candidate_cases: -
- counterexample_cases: 씨젠 2020, Abbott COVID tests, Zoom 2020
- Stage 1: explosive_temporary_demand, one_off_demand_spike
- Stage 2: short_term_eps_spike, red_flag_present
- Stage 3: green_blocked_unless_recurrence_proven
- 4B: market_extrapolates_one_off, valuation_overheat
- 4C: demand_normalization, guidance_down, asp_drop
- price_patterns: CYCLE_SPIKE_NORMALIZATION

### THEME_VALUATION_OVERHEAT
- success_cases: -
- success_candidate_cases: -
- counterexample_cases: 에코프로비엠/에코프로 2023, SMCI 2024, 로봇/AI 무실적 테마주
- Stage 1: price_surge, theme_news
- Stage 2: only_if_real_eps_fcf_evidence_exists
- Stage 3: green_extremely_limited
- 4B: valuation_saturation, crowded_reports, price_blowoff
- 4C: accounting_issue, guidance_miss, revision_down
- price_patterns: THEME_FRONT_RUN, ACCOUNTING_TRUST_COLLAPSE

### RETAIL_DOMESTIC_CONSUMER
- success_cases: -
- success_candidate_cases: BGF리테일, GS리테일, 신세계, 호텔신라
- counterexample_cases: 이마트류 경쟁 심화, 단기 소비 회복 테마
- Stage 1: same_store_sales_recovery, consumer_recovery_news
- Stage 2: opm_improvement, inventory_normalization, cost_leverage
- Stage 3: structural_channel_advantage, fcf_improvement, valuation_discount_resolution
- 4B: reopening_trade_crowded, margin_peak, traffic_growth_slowdown
- 4C: inventory_increase, competition_intensifies, consumer_slowdown
- price_patterns: DIRECT_RERATING

### GENERIC_UNCLASSIFIED
- success_cases: -
- success_candidate_cases: -
- counterexample_cases: 분류 불명 테마주
- Stage 1: unknown_sector_signal
- Stage 2: requires_manual_classification
- Stage 3: blocked_until_archetype_assigned
- 4B: unknown
- 4C: unknown
- price_patterns: DIRECT_RERATING
