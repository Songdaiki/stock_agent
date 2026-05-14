"""Round-14 theme-absorbing score-weight v0.4 matrix.

Round 14 turns the analyst's long theme notes into report-only calibration
material. Theme labels are still search/routing tags. They do not become score
inputs, and this module must not be imported by production scoring.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture


ROUND14_SOURCE_ROUND_PATH = "docs/round/round_14.md"


@dataclass(frozen=True)
class Round14ScoreWeightDraft:
    eps_fcf: int
    structural_visibility: int
    bottleneck_pricing: int
    market_mispricing: int
    valuation: int
    capital_allocation: int = 0
    information_confidence: int = 5

    def as_dict(self) -> dict[str, int]:
        return {
            "eps_fcf": self.eps_fcf,
            "structural_visibility": self.structural_visibility,
            "bottleneck_pricing": self.bottleneck_pricing,
            "market_mispricing": self.market_mispricing,
            "valuation": self.valuation,
            "capital_allocation": self.capital_allocation,
            "information_confidence": self.information_confidence,
        }


@dataclass(frozen=True)
class Round14ScoreWeightTarget:
    sub_archetype: str
    large_sector: Round10LargeSector
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    theme_tags: tuple[str, ...]
    score_weight: Round14ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    must_have_evidence: tuple[str, ...]
    red_flags: tuple[str, ...]
    success_candidates: tuple[str, ...]
    counterexamples: tuple[str, ...]
    normalization_point: str

    @property
    def theme_is_score_input(self) -> bool:
        return False

    @property
    def production_scoring_changed(self) -> bool:
        return False


ROUND14_SCORE_WEIGHT_TARGETS: tuple[Round14ScoreWeightTarget, ...] = (
    Round14ScoreWeightTarget(
        "RETAIL_CONVENIENCE_OFFLINE",
        Round10LargeSector.CONSUMER_RETAIL_BRAND,
        E2RArchetype.RETAIL_DOMESTIC_CONSUMER,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        ("편의점", "홈쇼핑", "음식료-유통", "콜드체인", "키즈/유아용품"),
        Round14ScoreWeightDraft(18, 16, 5, 14, 14, 3, 5),
        ("same_store_sales_recovery", "store_expansion", "pb_high_margin_mix", "listing_or_stake_event"),
        ("opm_improvement", "inventory_normalization", "cost_leverage", "fy1_fy2_op_revision"),
        ("store_efficiency_change", "repeat_logistics_revenue", "fcf_improvement", "old_domestic_retail_frame"),
        ("consumption_recovery_fully_priced", "store_growth_limit", "rent_wage_pressure"),
        ("inventory_increase", "online_competition", "consumer_slowdown", "logistics_cost_up"),
        ("opm_improvement", "fcf_improvement", "unit_economics", "inventory_turnover"),
        ("traffic_only", "listing_event_only", "delivery_cost_pressure", "online_margin_pressure"),
        ("convenience_store_efficiency_success_candidate", "cold_chain_repeat_logistics_candidate"),
        ("home_shopping_margin_decline_counterexample", "fresh_ecommerce_loss_counterexample"),
        "Retail can be Green-eligible only when sales translate into OPM and FCF, not traffic alone.",
    ),
    Round14ScoreWeightTarget(
        "INSURANCE_UNDERWRITING_CYCLE",
        Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL,
        E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
        Round10ThemePosture.GREEN_POSSIBLE,
        ("손해보험", "생명보험", "화재", "고배당주", "밸류업 지수"),
        Round14ScoreWeightDraft(15, 20, 5, 15, 25, 10, 5),
        ("valueup_disclosure", "buyback_or_dividend", "low_pbr", "loss_ratio_improvement_news"),
        ("roe_improvement", "csm_growth", "capital_ratio_stable", "return_policy_execution"),
        ("pbr_roe_frame_change", "repeat_return_policy", "stable_loss_ratio", "value_trap_frame_still_used"),
        ("pbr_roe_gap_normalized", "valueup_success_consensus_crowded"),
        ("loss_ratio_worsens", "credit_cost_up", "capital_ratio_down", "return_policy_retreat"),
        ("loss_ratio_improvement", "csm_growth", "capital_ratio", "shareholder_return_execution"),
        ("low_pbr_only", "weak_capital_ratio", "credit_cost", "return_policy_headline_only"),
        ("nonlife_insurance_loss_ratio_success_candidate", "life_insurance_csm_candidate"),
        ("low_pbr_no_roe_value_trap", "pf_credit_cost_financial"),
        "Insurance weights must emphasize ROE-PBR-capital-return alignment over headline dividend yield.",
    ),
    Round14ScoreWeightTarget(
        "PAYMENT_FINTECH_INFRA",
        Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL,
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        ("결제서비스", "토스 관련주", "지역화폐", "신용정보", "STO"),
        Round14ScoreWeightDraft(16, 18, 8, 16, 12, 3, 5),
        ("regulation_news", "business_launch", "bank_or_fintech_partnership"),
        ("license_or_issuance", "transaction_volume", "fee_model", "institutional_adoption"),
        ("payment_custody_settlement_infra", "low_regulatory_risk", "fcf_opm_improvement", "theme_frame_remains"),
        ("regulation_expectation_overheated", "related_stock_rally_without_revenue"),
        ("regulation_denied_or_delayed", "security_issue", "volume_absent", "no_revenue_model"),
        ("regulation_approval", "transaction_volume", "take_rate", "fee_model", "recurring_revenue"),
        ("law_delay", "security_issue", "no_revenue", "adoption_absent"),
        ("stablecoin_payment_infra_candidate", "sto_platform_candidate"),
        ("sto_law_expectation_only_counterexample", "payment_theme_no_fee_model"),
        "Digital finance requires regulation, real volume, and fee economics before Stage 2-plus conviction.",
    ),
    Round14ScoreWeightTarget(
        "DIGITAL_ASSET_TOKENIZATION",
        Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL,
        E2RArchetype.THEME_VALUATION_OVERHEAT,
        Round10ThemePosture.REDTEAM_FIRST,
        ("스테이블코인", "디지털자산", "블록체인", "NFT", "코인 테마"),
        Round14ScoreWeightDraft(10, 8, 5, 8, 5, 0, 5),
        ("law_headline", "token_business_announcement", "crypto_theme_search_spike"),
        ("regulated_issuance", "custody_or_brokerage_fee", "institutional_adoption"),
        ("regulated_revenue", "issued_volume", "cash_flow", "low_security_regulatory_risk"),
        ("law_expectation_crowding", "crypto_theme_price_run"),
        ("regulation_crackdown", "security_issue", "volume_absent", "relatedness_unclear"),
        ("regulated_revenue", "issued_volume", "institutional_adoption", "cash_flow"),
        ("theme_only_tokenization", "law_delay", "no_regulated_revenue", "security_issue"),
        ("crypto_theme_no_revenue_counterexample", "regulation_crackdown_4c"),
        ("nft_theme_overheat_counterexample", "pure_coin_theme_no_cashflow"),
        "Tokenization is RedTeam-first; legal headlines are search signals, not EPS/FCF evidence.",
    ),
    Round14ScoreWeightTarget(
        "BEAUTY_OEM_ODM_SUPPLYCHAIN",
        Round10LargeSector.CONSUMER_RETAIL_BRAND,
        E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,
        Round10ThemePosture.GREEN_POSSIBLE,
        ("화장품 OEM", "화장품 ODM", "화장품 원재료", "화장품 부자재", "K뷰티"),
        Round14ScoreWeightDraft(22, 23, 12, 16, 13, 0, 5),
        ("us_japan_export_growth", "kbeauty_viral", "odm_order_increase"),
        ("fy1_fy2_op_eps_revision", "opm_roe_improvement", "customer_diversification", "channel_expansion"),
        ("repeat_orders", "offline_major_retail_entry", "clean_working_capital", "china_frame_removed"),
        ("kbeauty_overcrowding", "target_multiple_saturated", "competitive_brand_proliferation"),
        ("sell_through_slowdown", "inventory_increase", "receivables_spike", "tariff_regulation_hit"),
        ("export_growth", "customer_diversification", "opm_roe_improvement", "working_capital_clean"),
        ("china_dependency", "viral_only_brand", "channel_stuffing", "receivables_spike"),
        ("kbeauty_oem_odm_success_candidate", "silicontwo_distribution_candidate", "apr_device_channel_candidate"),
        ("channel_stuffing_receivables_4c", "china_dependency_cosmetics_counterexample"),
        "K-beauty supply chain can earn Green only with repeat orders and clean inventory/receivables.",
    ),
    Round14ScoreWeightTarget(
        "BATTERY_RECYCLING_ESS_SHIFT",
        Round10LargeSector.BATTERY_EV_GREEN,
        E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        ("2차전지 소재", "폐배터리", "전고체 배터리", "리튬", "ESS", "전기차 화재"),
        Round14ScoreWeightDraft(20, 16, 14, 10, 10, 0, 5),
        ("long_term_contract", "capex_expansion", "ev_or_ess_demand_news"),
        ("margin_and_price_improve", "customer_contract_quality", "capex_without_fcf_damage", "ess_revenue_conversion"),
        ("long_contract", "price_pass_through", "sustained_demand", "valuation_room"),
        ("price_runup", "crowding", "per_pbr_overheat", "revision_slowdown"),
        ("ev_demand_slows", "mineral_price_down", "utilization_down", "capex_overbuild"),
        ("ess_demand", "recycling_volume", "utilization_improvement", "fcf_after_capex"),
        ("ev_headline_only", "mineral_price_dependency", "recycling_volume_absent", "margin_unclear"),
        ("ess_shift_battery_candidate", "battery_recycling_volume_candidate"),
        ("ecopro_bm_overheat_counterexample", "battery_capa_overbuild", "solid_state_theme_no_revenue"),
        "Battery remains Green-restricted; ESS/recycling are watch paths until utilization and FCF are proven.",
    ),
    Round14ScoreWeightTarget(
        "HYDROGEN_FUEL_CELL_INFRA",
        Round10LargeSector.BATTERY_EV_GREEN,
        E2RArchetype.THEME_VALUATION_OVERHEAT,
        Round10ThemePosture.REDTEAM_FIRST,
        ("수소차 연료전지", "수소차 인프라", "수소차 기타부품", "LNG 발전유통"),
        Round14ScoreWeightDraft(18, 18, 12, 12, 10, 0, 5),
        ("policy_subsidy", "factory_groundbreaking", "hydrogen_capex", "order_news"),
        ("actual_contract", "utilization", "op_eps_revision", "subsidy_and_profitability_confirmed"),
        ("multi_year_demand", "fixed_customer_or_government_demand", "low_policy_risk", "cost_competitiveness"),
        ("policy_expectation_overheated", "subsidy_benefit_fully_priced", "capex_burden_visible"),
        ("subsidy_cut", "utilization_down", "project_delay", "cost_curve_failure"),
        ("actual_capex", "production_capacity", "customer_demand", "op_eps_conversion"),
        ("policy_only", "no_customer", "no_revenue", "utilization_down"),
        ("hydrogen_fuel_cell_plant_candidate", "fuel_cell_service_revenue_candidate"),
        ("hydrogen_theme_no_revenue_counterexample", "subsidy_cut_4c"),
        "Hydrogen needs customers, utilization, and OP/EPS conversion; policy enthusiasm is not enough.",
    ),
    Round14ScoreWeightTarget(
        "RENEWABLE_ENERGY_POLICY",
        Round10LargeSector.BATTERY_EV_GREEN,
        E2RArchetype.UTILITIES_REGULATED_TARIFF,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        ("태양광", "풍력", "탄소배출권", "스마트그리드", "ESS/BESS"),
        Round14ScoreWeightDraft(18, 18, 12, 12, 10, 0, 5),
        ("policy_subsidy", "renewable_capex", "project_start", "order_news"),
        ("actual_contract_or_utilization", "op_eps_revision", "margin_support"),
        ("multi_year_project_backlog", "low_policy_risk", "cost_competitiveness", "customer_or_government_demand"),
        ("policy_premium_crowded", "subsidy_benefit_fully_priced", "capex_burden_visible"),
        ("subsidy_cut", "tariff_or_customs_issue", "supply_chain_disruption", "project_delay"),
        ("project_backlog", "policy_support", "utilization", "margin_visibility"),
        ("policy_dependency", "module_oversupply", "tariff_risk", "subsidy_cut"),
        ("renewable_project_economics_candidate", "ai_dc_bess_stability_candidate"),
        ("solar_tariff_supplychain_4c", "wind_project_delay_counterexample"),
        "Renewables are Watch/Yellow until project economics, utilization, and margins are visible.",
    ),
    Round14ScoreWeightTarget(
        "TIRE_AUTO_COMPONENT_SPREAD",
        Round10LargeSector.MOBILITY_TRANSPORT_LEISURE,
        E2RArchetype.AUTO_MOBILITY_COMPONENTS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        ("타이어", "현대·기아차 부품주", "자동차 경량화", "자율주행", "카메라"),
        Round14ScoreWeightDraft(20, 18, 10, 14, 14, 3, 5),
        ("completed_vehicle_sales", "asp_increase", "customer_order"),
        ("opm_improvement", "raw_material_stable", "customer_diversification", "fy1_fy2_op_revision"),
        ("high_margin_mix_shift", "adas_ev_exposure", "repeat_supply_visibility", "valuation_discount_removed"),
        ("peak_margin", "auto_cycle_peak", "valuation_normalized"),
        ("raw_material_spike", "factory_disruption", "customer_demand_slowdown", "recall_quality_cost"),
        ("customer_diversification", "opm_improvement", "raw_material_spread", "repeat_supply_visibility"),
        ("single_customer_dependency", "ev_demand_slowdown", "factory_fire", "recall_quality_cost"),
        ("tire_spread_success_candidate", "adas_component_customer_diversification_candidate"),
        ("factory_fire_4c_counterexample", "ev_demand_slowdown_component"),
        "Auto parts need customer diversification and raw-material spread, not auto theme exposure alone.",
    ),
    Round14ScoreWeightTarget(
        "CDMO_HEALTHCARE_CONTRACT",
        Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE,
        E2RArchetype.CDMO_HEALTHCARE_CONTRACT,
        Round10ThemePosture.GREEN_POSSIBLE,
        ("CMO", "원료의약품", "바이오시밀러", "CRO", "임상시험수탁"),
        Round14ScoreWeightDraft(20, 24, 12, 12, 12, 0, 5),
        ("large_production_contract", "capacity_expansion", "global_manufacturing_site"),
        ("utilization_up", "sales_op_revision", "long_term_contract", "customer_diversification"),
        ("multi_year_production_visibility", "high_fcf_conversion", "contract_utilization_margin_improve", "bio_fixed_cost_discount_frame"),
        ("capacity_expectation_overheated", "valuation_saturated", "new_plant_fully_priced"),
        ("utilization_down", "contract_delay", "patent_litigation", "price_competition"),
        ("multi_year_production_visibility", "capacity_utilization", "customer_diversification", "fcf_conversion"),
        ("capacity_overbuild", "customer_concentration", "litigation", "price_competition"),
        ("samsung_biologics_cdmo_capacity_candidate", "celltrion_biosimilar_revenue_candidate"),
        ("cdmo_capacity_underutilization", "patent_litigation_delay_counterexample"),
        "CDMO is contract/capacity/utilization scoring, not pre-revenue biotech scoring.",
    ),
    Round14ScoreWeightTarget(
        "PLATFORM_SOFTWARE_INTERNET",
        Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY,
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        ("클라우드 컴퓨팅", "원격근무", "컨택센터", "광고", "AI 소프트웨어"),
        Round14ScoreWeightDraft(20, 22, 8, 16, 14, 0, 5),
        ("mau_or_traffic_recovery", "ad_or_commerce_improvement"),
        ("arpu_increase", "recurring_revenue", "opm_leverage", "cost_efficiency"),
        ("recurring_revenue", "pricing_power", "margin_expansion", "old_frame_valuation"),
        ("software_theme_crowded", "ai_narrative_ahead_of_revenue"),
        ("regulatory_issue", "take_rate_down", "traffic_decline", "ai_cost_overrun"),
        ("recurring_revenue", "arpu", "take_rate", "opm_leverage"),
        ("mau_without_monetization", "ai_cost_overrun", "regulatory_risk", "governance_risk"),
        ("douzone_saas_candidate", "platform_ad_recovery_candidate"),
        ("mau_only_platform", "kakao_governance_risk"),
        "Platform/SW needs monetization and margin leverage; MAU or AI keywords alone do not score.",
    ),
    Round14ScoreWeightTarget(
        "SECURITY_IDENTITY_DEEPFAKE",
        Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY,
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        ("IT보안", "딥페이크", "생체인식", "CCTV", "스마트홈"),
        Round14ScoreWeightDraft(20, 22, 8, 16, 14, 0, 5),
        ("security_demand", "regulatory_security_need", "public_or_enterprise_contract_news"),
        ("recurring_contract", "op_eps_revision", "paid_security_deployment"),
        ("recurring_security_revenue", "opm_leverage", "low_legal_risk", "security_demand_persists"),
        ("security_theme_crowded", "ai_security_narrative_ahead_of_revenue"),
        ("budget_cut", "churn", "governance_or_legal_risk", "no_recurring_revenue"),
        ("recurring_contract", "security_demand", "opm_leverage", "legal_risk_low"),
        ("theme_only_security", "no_recurring_revenue", "budget_cut", "ai_cost_overrun"),
        ("security_identity_candidate", "deepfake_security_contract_candidate"),
        ("deepfake_theme_no_revenue_counterexample", "security_budget_cut_4c"),
        "Security tags require recurring contracts and low legal/governance risk before higher conviction.",
    ),
    Round14ScoreWeightTarget(
        "ROBOTICS_FACTORY_AUTOMATION",
        Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY,
        E2RArchetype.ROBOTICS_FACTORY_AUTOMATION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        ("피지컬AI", "휴머노이드", "제조용 로봇", "서비스용 로봇", "수술용 로봇", "스마트팩토리"),
        Round14ScoreWeightDraft(18, 15, 10, 12, 10, 0, 5),
        ("large_company_investment", "robot_policy", "order_news"),
        ("revenue_conversion", "customer_diversification", "op_improvement"),
        ("repeat_revenue_or_consumables", "customer_lock_in", "cost_leverage"),
        ("robot_theme_overheated", "ipo_valuation_crowded"),
        ("order_delay", "earnings_miss", "monetization_failure", "valuation_overheat"),
        ("customer_adoption", "revenue_conversion", "opm_improvement", "repeat_revenue"),
        ("tam_only", "mou_poc_only", "no_revenue", "high_valuation_ipo"),
        ("rainbow_robotics_samsung_stage1_candidate", "factory_automation_revenue_candidate"),
        ("robot_tam_no_revenue", "mou_only_robot_counterexample"),
        "Robotics is mostly Watch until investment converts into revenue, orders, and repeat economics.",
    ),
    Round14ScoreWeightTarget(
        "CONSTRUCTION_REAL_ESTATE_CREDIT",
        Round10LargeSector.CONSTRUCTION_REAL_ESTATE_MATERIALS,
        E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT,
        Round10ThemePosture.REDTEAM_FIRST,
        ("대형 건설사", "중소형 건설사", "부동산 자산 보유", "개발신탁리츠"),
        Round14ScoreWeightDraft(18, 10, 8, 12, 10, 0, 5),
        ("order_or_housing_recovery", "pf_concern_easing", "liquidity_support"),
        ("cost_ratio_stable", "cash_flow_improvement", "debt_reduction"),
        ("post_restructuring_repeat_cashflow", "credit_risk_resolved", "margin_confirmed"),
        ("credit_relief_fully_priced", "liquidity_support_mistaken_for_structural"),
        ("pf_stress", "unsold_inventory", "credit_rating_down", "liquidity_crunch"),
        ("pf_exposure_clean", "cash_flow", "credit_risk_resolved", "cost_ratio_stability"),
        ("pf_stress", "liquidity_support_dependency", "cost_inflation", "unsold_inventory"),
        ("pf_risk_resolution_candidate", "overseas_infra_margin_contract"),
        ("construction_pf_stress", "credit_relief_rally_not_rerating"),
        "Construction is credit-risk first; a rebound can be relief, not structural E2R.",
    ),
    Round14ScoreWeightTarget(
        "BUILDING_MATERIALS_CYCLE",
        Round10LargeSector.CONSTRUCTION_REAL_ESTATE_MATERIALS,
        E2RArchetype.COMMODITY_SPREAD,
        Round10ThemePosture.REDTEAM_FIRST,
        ("건자재", "시멘트", "레미콘", "콘크리트", "철근", "거푸집", "가구"),
        Round14ScoreWeightDraft(18, 10, 8, 12, 10, 0, 5),
        ("price_hike", "shipment_recovery", "housing_recovery"),
        ("volume_and_price_support", "cost_spread", "cash_flow_improvement"),
        ("durable_price_volume", "cost_pass_through", "pf_risk_contained"),
        ("rebuild_event_fully_priced", "housing_rebound_crowded"),
        ("housing_slowdown", "pf_stress", "cost_inflation", "price_hike_failure"),
        ("price_hike", "shipment_volume", "cost_spread", "housing_cycle"),
        ("pf_stress", "housing_slowdown", "cost_inflation", "price_hike_failure"),
        ("cement_price_hike_candidate", "building_material_spread_candidate"),
        ("housing_slowdown_materials_4c", "pf_materials_counterexample"),
        "Building materials need both price and volume support; PF risk caps Green.",
    ),
    Round14ScoreWeightTarget(
        "EVENT_DISEASE_PEST_DEMAND",
        Round10LargeSector.POLICY_GEOPOLITICAL_EVENT,
        E2RArchetype.ONE_OFF_EVENT_DEMAND,
        Round10ThemePosture.REDTEAM_FIRST,
        ("엠폭스", "코로나19", "전염병 진단", "동물백신", "빈대퇴치", "황사마스크"),
        Round14ScoreWeightDraft(10, 5, 5, 5, 5, 0, 5),
        ("disease_or_disaster_news", "trading_value_spike"),
        ("actual_revenue_or_contract_only", "post_event_revenue"),
        ("repeat_platform_demand", "commercialized_product", "recurring_revenue"),
        ("price_only_rally", "event_demand_extrapolated"),
        ("demand_normalization", "guidance_down", "inventory_increase", "event_fades"),
        ("recurring_non_event_demand", "post_event_revenue", "margin_normalization"),
        ("one_off_demand", "inventory_build", "guidance_down", "demand_cliff"),
        ("infectious_disease_oneoff_counterexample", "fine_dust_mask_oneoff_counterexample"),
        ("seegene_2020_red", "temporary_pest_demand_counterexample"),
        "Disease/pest demand is Red/4B defense material unless recurring non-event revenue is proven.",
    ),
    Round14ScoreWeightTarget(
        "SPECULATIVE_SCIENCE_THEME",
        Round10LargeSector.POLICY_GEOPOLITICAL_EVENT,
        E2RArchetype.THEME_VALUATION_OVERHEAT,
        Round10ThemePosture.REDTEAM_FIRST,
        ("초전도체", "맥신", "그래핀", "양자 기술", "페라이트", "스페이스X 관련주"),
        Round14ScoreWeightDraft(5, 5, 5, 5, 5, 0, 5),
        ("paper_or_science_news", "theme_search_spike", "trading_value_spike"),
        ("actual_revenue_or_contract_only", "verified_product"),
        ("commercial_contract", "revenue_conversion", "repeat_demand"),
        ("price_only_rally", "related_stocks_move_together"),
        ("validation_failure", "demand_normalization", "relatedness_denied", "commercialization_failure"),
        ("commercial_contract", "revenue_conversion", "verified_product"),
        ("paper_only", "relatedness_unclear", "price_only_rally", "commercialization_failure"),
        ("speculative_science_theme_counterexample", "quantum_theme_no_revenue_counterexample"),
        ("superconductor_theme_overheat", "mxene_graphene_theme_counterexample"),
        "Speculative science is not an E2R success path until commercialization and revenue exist.",
    ),
    Round14ScoreWeightTarget(
        "AGRI_LIVESTOCK_FOOD_COMMODITY",
        Round10LargeSector.EDUCATION_LIFE_AGRI_MISC,
        E2RArchetype.COMMODITY_SPREAD,
        Round10ThemePosture.REDTEAM_FIRST,
        ("양돈주", "육계주", "배합사료", "대두", "농기계", "스마트팜", "참치 원양어업"),
        Round14ScoreWeightDraft(18, 10, 14, 8, 8, 0, 5),
        ("grain_meat_fish_price_move", "feed_cost_change", "weather_or_disease_event"),
        ("price_pass_through", "repeat_demand", "op_eps_revision"),
        ("export_or_service_repeat_demand", "cost_pass_through", "structural_margin"),
        ("commodity_price_fully_priced", "disease_event_extrapolated"),
        ("feed_cost_squeeze", "commodity_reversal", "weather_event_fades", "inventory_loss"),
        ("price_pass_through", "feed_cost", "inventory_status", "op_eps_revision"),
        ("disease_event_only", "feed_cost_squeeze", "commodity_reversal", "weather_theme"),
        ("smart_farm_order_candidate", "fishery_price_spread_candidate"),
        ("pork_price_cycle_counterexample", "feed_cost_squeeze_counterexample"),
        "Agri/livestock is mostly cycle/event; without pass-through and repeat demand, Green is restricted.",
    ),
)


def round14_target_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for item in ROUND14_SCORE_WEIGHT_TARGETS:
        weights = item.score_weight.as_dict()
        rows.append(
            {
                "sub_archetype": item.sub_archetype,
                "large_sector": item.large_sector.value,
                "canonical_archetype": item.canonical_archetype.value,
                "posture": item.posture.value,
                "theme_tags": "|".join(item.theme_tags),
                "eps_fcf": str(weights["eps_fcf"]),
                "structural_visibility": str(weights["structural_visibility"]),
                "bottleneck_pricing": str(weights["bottleneck_pricing"]),
                "market_mispricing": str(weights["market_mispricing"]),
                "valuation": str(weights["valuation"]),
                "capital_allocation": str(weights["capital_allocation"]),
                "information_confidence": str(weights["information_confidence"]),
                "stage1_signals": "|".join(item.stage1_signals),
                "stage2_signals": "|".join(item.stage2_signals),
                "stage3_conditions": "|".join(item.stage3_conditions),
                "stage4b_conditions": "|".join(item.stage4b_conditions),
                "stage4c_conditions": "|".join(item.stage4c_conditions),
                "must_have_evidence": "|".join(item.must_have_evidence),
                "red_flags": "|".join(item.red_flags),
                "success_candidates": "|".join(item.success_candidates),
                "counterexamples": "|".join(item.counterexamples),
                "theme_is_score_input": str(item.theme_is_score_input).lower(),
                "production_scoring_changed": str(item.production_scoring_changed).lower(),
                "normalization_point": item.normalization_point,
            }
        )
    return tuple(rows)


def round14_theme_tag_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for item in ROUND14_SCORE_WEIGHT_TARGETS:
        for tag in item.theme_tags:
            rows.append(
                {
                    "theme_tag": tag,
                    "large_sector": item.large_sector.value,
                    "primary_sub_archetype": item.sub_archetype,
                    "canonical_archetype": item.canonical_archetype.value,
                    "posture": item.posture.value,
                    "theme_is_score_input": str(item.theme_is_score_input).lower(),
                    "must_have_evidence": "|".join(item.must_have_evidence),
                    "red_flags": "|".join(item.red_flags),
                }
            )
    return tuple(rows)


def target_for(sub_archetype: str) -> Round14ScoreWeightTarget | None:
    for item in ROUND14_SCORE_WEIGHT_TARGETS:
        if item.sub_archetype == sub_archetype:
            return item
    return None


def round14_policy_groups() -> dict[str, tuple[str, ...]]:
    groups: dict[str, list[str]] = {posture.value: [] for posture in Round10ThemePosture}
    for item in ROUND14_SCORE_WEIGHT_TARGETS:
        groups[item.posture.value].append(item.sub_archetype)
    return {key: tuple(value) for key, value in groups.items()}


def write_round14_score_weight_reports(
    *,
    output_directory: str | Path = "output/e2r_round14_score_weight_v04",
    score_profile_path: str | Path = "data/sector_taxonomy/score_weight_profiles_round14.csv",
    theme_map_path: str | Path = "data/sector_taxonomy/theme_tag_map_round14.csv",
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    score_profile = Path(score_profile_path)
    theme_map = Path(theme_map_path)
    score_profile.parent.mkdir(parents=True, exist_ok=True)
    theme_map.parent.mkdir(parents=True, exist_ok=True)
    paths = {
        "score_profiles": score_profile,
        "theme_map": theme_map,
        "summary": output / "round14_score_weight_v04_summary.md",
        "target_matrix": output / "round14_score_weight_targets.csv",
        "theme_policy": output / "round14_theme_policy_v04.md",
        "case_candidate_plan": output / "round14_case_candidate_plan.md",
        "next_plan": output / "round14_shadow_scoring_next_plan.md",
    }
    _write_rows(round14_target_rows(), paths["score_profiles"])
    _write_rows(round14_target_rows(), paths["target_matrix"])
    _write_rows(round14_theme_tag_rows(), paths["theme_map"])
    paths["summary"].write_text(render_round14_summary_markdown(), encoding="utf-8")
    paths["theme_policy"].write_text(render_round14_theme_policy_markdown(), encoding="utf-8")
    paths["case_candidate_plan"].write_text(render_round14_case_candidate_plan_markdown(), encoding="utf-8")
    paths["next_plan"].write_text(render_round14_next_plan_markdown(), encoding="utf-8")
    return paths


def render_round14_summary_markdown() -> str:
    groups = round14_policy_groups()
    lines = [
        "# Round-14 Score-Weight v0.4 Summary",
        "",
        f"- source_round: `{ROUND14_SOURCE_ROUND_PATH}`",
        f"- target_count: {len(ROUND14_SCORE_WEIGHT_TARGETS)}",
        f"- theme_tag_count: {len(round14_theme_tag_rows())}",
        f"- green_possible_count: {len(groups[Round10ThemePosture.GREEN_POSSIBLE.value])}",
        f"- watch_yellow_first_count: {len(groups[Round10ThemePosture.WATCH_YELLOW_FIRST.value])}",
        f"- redteam_first_count: {len(groups[Round10ThemePosture.REDTEAM_FIRST.value])}",
        "- production_scoring_changed: false",
        "- theme_tags_are_score_input: false",
        "",
        "## Interpretation",
        "- Round 14 is a v0.4 scoring hypothesis, not a production score change.",
        "- Theme tags route search and case mining. Evidence fields create score.",
        "- Example: `스테이블코인` is a tag. It only becomes stronger if regulation, volume, and fee economics appear.",
        "- Price-path backfill and score-price alignment are required before shadow scoring.",
    ]
    return "\n".join(lines) + "\n"


def render_round14_theme_policy_markdown() -> str:
    groups = round14_policy_groups()
    lines = ["# Round-14 Theme Policy v0.4", ""]
    for posture in Round10ThemePosture:
        lines.append(f"## {posture.value}")
        for label in groups[posture.value]:
            lines.append(f"- `{label}`")
        lines.append("")
    lines.extend(
        [
            "## Easy Examples",
            "- Convenience retail can improve, but traffic alone is not enough; OPM and FCF must improve.",
            "- Insurance can be Green-possible when loss ratio, CSM/capital, ROE, and shareholder return align.",
            "- Speculative science can jump in price, but without commercialization it is RedTeam-first.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round14_case_candidate_plan_markdown() -> str:
    lines = ["# Round-14 Case Candidate Plan", ""]
    for item in ROUND14_SCORE_WEIGHT_TARGETS:
        lines.append(f"## {item.sub_archetype}")
        lines.append("### Success / Candidate")
        for case_id in item.success_candidates:
            lines.append(f"- `{case_id}`")
        lines.append("### Counterexample / Risk")
        for case_id in item.counterexamples:
            lines.append(f"- `{case_id}`")
        lines.append("")
    return "\n".join(lines)


def render_round14_next_plan_markdown() -> str:
    return "\n".join(
        [
            "# Round-14 Next Plan",
            "",
            "1. Build `theme_tag_map.csv` from these v0.4 mappings.",
            "2. Convert success candidates and counterexamples into `cases_v03.jsonl` records.",
            "3. Backfill stage2/stage3 price, peak price, MFE/MAE, and drawdown.",
            "4. Run score-price alignment before any shadow scoring.",
            "5. Keep production StageClassifier thresholds unchanged until the case library proves the weights.",
            "",
            "## What Not To Change",
            "- Do not turn theme names into score inputs.",
            "- Do not use these weights in live scoring yet.",
            "- Do not make one-off disease, speculative science, tokenization, construction PF, or battery overheat cases Green without durable EPS/FCF evidence.",
            "",
        ]
    )


def _write_rows(rows: Iterable[Mapping[str, str]], path: Path) -> Path:
    row_tuple = tuple(rows)
    if not row_tuple:
        path.write_text("", encoding="utf-8")
        return path
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(row_tuple[0].keys()))
        writer.writeheader()
        for row in row_tuple:
            writer.writerow(row)
    return path


__all__ = [
    "ROUND14_SCORE_WEIGHT_TARGETS",
    "ROUND14_SOURCE_ROUND_PATH",
    "Round14ScoreWeightDraft",
    "Round14ScoreWeightTarget",
    "render_round14_case_candidate_plan_markdown",
    "render_round14_next_plan_markdown",
    "render_round14_summary_markdown",
    "render_round14_theme_policy_markdown",
    "round14_policy_groups",
    "round14_target_rows",
    "round14_theme_tag_rows",
    "target_for",
    "write_round14_score_weight_reports",
]
