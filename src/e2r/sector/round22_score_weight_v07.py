"""Round-22 cases_v04 expansion and score-weight v0.7 hypotheses.

Round 22 recalibrates thin and important archetypes. It is still report-only:
case records and v0.7 weights are calibration material, not candidate-generation
input and not production scoring logic.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import CaseDataQuality, E2RCaseRecord, PriceValidation
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture


ROUND22_SOURCE_ROUND_PATH = "docs/round/round_22.md"
ROUND22_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round22_score_weight_v07"
ROUND22_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_v04_round22.jsonl"
ROUND22_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round22_v07.csv"


@dataclass(frozen=True)
class Round22ScoreWeightDraft:
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
class Round22ScoreTarget:
    target_id: str
    large_sector: Round10LargeSector
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round22ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    normalization_point: str

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round22CaseCandidate:
    case_id: str
    target_id: str
    symbol: str
    company_name: str
    market: str
    case_type: str
    evidence_fields: tuple[str, ...]
    red_flag_fields: tuple[str, ...]
    notes: str

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND22_SCORE_TARGETS: tuple[Round22ScoreTarget, ...] = (
    Round22ScoreTarget(
        "SECURITIES_BROKERAGE_CYCLE",
        Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL,
        E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round22ScoreWeightDraft(18, 14, 5, 15, 18, 8, 5),
        ("trading_value_growth", "equity_market_rally", "ipo_ib_recovery_expectation", "value_up_expectation"),
        ("brokerage_revenue_growth", "ib_fee_growth", "capital_ratio_stable", "op_eps_revision"),
        ("repeat_turnover_or_ib_recovery", "pf_risk_low", "roe_structure_improves", "shareholder_return_capacity"),
        ("market_turnover_peak", "brokerage_group_overheated", "ipo_expectation_priced"),
        ("trading_value_collapse", "pf_loss", "proprietary_loss", "capital_ratio_down"),
        ("brokerage_revenue_growth", "ib_pipeline", "capital_ratio_stable", "pf_risk_low", "roe_improvement"),
        ("short_lived_trading_spike", "pf_loss", "proprietary_loss", "vc_exit_market_weakness"),
        "Brokerage is Watch-first: turnover can lift EPS quickly, but durability is weaker than banks or insurers.",
    ),
    Round22ScoreTarget(
        "INSURANCE_UNDERWRITING_CYCLE",
        Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL,
        E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round22ScoreWeightDraft(15, 21, 4, 15, 25, 10, 5),
        ("low_pbr", "value_up_disclosure", "loss_ratio_improvement", "dividend_or_buyback_expectation"),
        ("roe_improvement", "csm_growth", "k_ics_stable", "loss_ratio_stable", "shareholder_return_execution"),
        ("pbr_roe_frame_change", "repeat_shareholder_return", "underwriting_profit_stable", "value_trap_frame_still_used"),
        ("pbr_normalized", "insurance_value_up_crowded", "shareholder_return_expectation_priced"),
        ("loss_ratio_worsens", "capital_ratio_down", "cyber_operational_risk", "shareholder_return_retreat"),
        ("loss_ratio_stability", "csm_or_roe_improvement", "capital_ratio_stable", "shareholder_return_execution"),
        ("low_pbr_only", "capital_return_limited", "cyber_operational_risk", "pf_or_alternative_investment_loss"),
        "Insurance is PBR-ROE-shareholder return rerating, not EPS explosion; capital and underwriting quality dominate.",
    ),
    Round22ScoreTarget(
        "EDUCATION_SPECIALTY_SERVICES",
        Round10LargeSector.EDUCATION_LIFE_AGRI_MISC,
        E2RArchetype.EDUCATION_SPECIALTY_SERVICES,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round22ScoreWeightDraft(18, 17, 5, 12, 12, 2, 5),
        ("exam_policy_change", "student_count_or_price_up", "education_spending_growth"),
        ("repeat_revenue", "opm_improvement", "adult_or_online_expansion", "fcf_improvement"),
        ("adult_overseas_b2b_subscription_offsets_birthrate", "pricing_power", "traditional_hagwon_frame"),
        ("exam_theme_overheated", "policy_expectation_priced"),
        ("private_education_regulation", "student_decline", "price_cut", "ai_substitution"),
        ("repeat_revenue", "adult_or_overseas_expansion", "opm_improvement", "fcf_improvement"),
        ("birthrate_decline", "regulation", "ai_substitution", "offline_fixed_cost"),
        "Education stays Watch-first unless adult, overseas, B2B, or subscription revenue offsets birthrate/regulation risk.",
    ),
    Round22ScoreTarget(
        "RETAIL_ECOMMERCE_LOGISTICS",
        Round10LargeSector.CONSUMER_RETAIL_BRAND,
        E2RArchetype.RETAIL_DOMESTIC_CONSUMER,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round22ScoreWeightDraft(18, 16, 5, 13, 14, 3, 5),
        ("same_store_sales_recovery", "store_expansion", "pb_product_news", "listing_or_stake_event"),
        ("opm_improvement", "inventory_normalization", "cost_leverage", "fy1_fy2_op_revision"),
        ("store_efficiency_change", "cold_chain_repeat_contracts", "fcf_improvement", "old_domestic_retail_frame"),
        ("consumer_recovery_priced", "store_growth_limit", "rent_or_labor_pressure"),
        ("inventory_increase", "online_competition", "consumer_slowdown", "logistics_cost_up"),
        ("opm_improvement", "inventory_normalization", "cost_leverage", "fcf_improvement"),
        ("inventory", "logistics_cost", "competition", "fresh_ecommerce_loss"),
        "Retail/logistics needs OPM and FCF, not revenue growth alone; fresh e-commerce and home shopping stay conservative.",
    ),
    Round22ScoreTarget(
        "BUILDING_MATERIALS_REIT",
        Round10LargeSector.CONSTRUCTION_REAL_ESTATE_MATERIALS,
        E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round22ScoreWeightDraft(17, 12, 12, 12, 12, 5, 5),
        ("price_hike", "housing_start_recovery", "rate_down", "dividend_appeal"),
        ("opm_improvement", "shipment_recovery", "cost_stability", "dividend_stability"),
        ("supply_rationalization", "pricing_power", "repeat_rental_income", "low_debt_risk"),
        ("property_recovery_priced", "dividend_theme_overheated"),
        ("pf_stress", "housing_starts_down", "vacancy_up", "dividend_cut", "cost_up"),
        ("price_pass_through", "volume_recovery", "cost_stability", "credit_risk_contained"),
        ("pf_stress", "rates_up", "vacancy_up", "dividend_cut", "cost_up"),
        "Building materials/REITs are Green-restricted because PF, rates, vacancy, and dividend coverage can dominate.",
    ),
    Round22ScoreTarget(
        "CLOUD_AI_SOFTWARE_INFRA",
        Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY,
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round22ScoreWeightDraft(20, 23, 8, 16, 14, 0, 5),
        ("cloud_transition", "erp_saas_demand", "ai_feature_launch", "b2b_customer_growth"),
        ("recurring_revenue_growth", "arpu_up", "opm_improvement", "retention_confirmed"),
        ("customer_lock_in", "high_fcf_conversion", "pricing_power", "old_software_frame"),
        ("saas_ai_narrative_overheated", "multiple_saturation"),
        ("churn", "ai_cost_overrun", "opm_decline", "competition_intensifies"),
        ("recurring_revenue", "arpu", "retention", "opm_or_fcf_improvement"),
        ("ai_feature_only", "ai_cost_overrun", "churn", "si_revenue_only"),
        "Cloud/SaaS is Green-possible only through recurring revenue, OPM, and FCF, not AI wording.",
    ),
    Round22ScoreTarget(
        "CRO_CLINICAL_SERVICE",
        Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE,
        E2RArchetype.CDMO_HEALTHCARE_CONTRACT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round22ScoreWeightDraft(18, 20, 8, 12, 12, 0, 5),
        ("clinical_trial_count_growth", "pharma_rd_growth", "order_backlog_growth"),
        ("sales_op_growth", "customer_diversification", "repeat_service_revenue"),
        ("multi_year_backlog", "customer_portfolio_diversified", "high_fcf_conversion"),
        ("biotech_rd_expectation_overheated"),
        ("clinical_trial_cut", "customer_budget_cut", "order_cancellation"),
        ("service_backlog", "customer_diversification", "repeat_clinical_service_revenue", "opm_improvement"),
        ("biotech_funding_cycle_down", "customer_concentration", "trial_delay", "low_margin_backlog"),
        "CRO is weaker than CDMO but more scoreable than pre-revenue biotech when backlog and customer diversity are real.",
    ),
    Round22ScoreTarget(
        "APPAREL_BRAND_OEM",
        Round10LargeSector.CONSUMER_RETAIL_BRAND,
        E2RArchetype.EXPORT_RECURRING_CONSUMER,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round22ScoreWeightDraft(18, 16, 8, 14, 12, 0, 5),
        ("overseas_popup", "kfashion_collaboration", "order_growth", "celebrity_ip_collaboration"),
        ("overseas_sales_growth", "inventory_turnover_stable", "opm_improvement", "customer_diversification"),
        ("repeat_brand_purchase", "global_channel_expansion", "fcf_improvement", "old_domestic_apparel_frame"),
        ("brand_hype_overheated", "inventory_risk_expands"),
        ("inventory_increase", "discount_sales", "channel_slowdown", "order_cancellation"),
        ("overseas_channel_expansion", "inventory_turnover", "low_discount_rate", "opm_improvement"),
        ("single_fad_brand", "inventory_build", "discounting", "channel_concentration"),
        "Apparel remains Watch-first; inventory, markdown, and single-channel risk are heavier than K-food/K-beauty.",
    ),
    Round22ScoreTarget(
        "MEMORY_HBM_CAPACITY",
        Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS,
        E2RArchetype.MEMORY_HBM_CAPACITY,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round22ScoreWeightDraft(24, 21, 19, 15, 12, 0, 5),
        ("hbm_demand", "memory_price_increase", "earnings_turnaround"),
        ("fy1_fy2_fy3_revision", "dram_nand_hbm_pricing", "supply_discipline", "customer_supply_preorder"),
        ("long_term_contract_or_prepayment", "price_band", "capacity_constraint", "multi_year_revision", "cyclical_discount_removed"),
        ("one_to_two_year_price_surge", "multiple_saturation", "customer_price_resistance", "capex_expansion", "global_crowding"),
        ("memory_price_down", "supply_glut", "customer_ai_capex_slowdown", "consensus_revision_down"),
        ("hbm_demand", "supply_discipline", "medium_term_revision", "capacity_constraint"),
        ("capex_reversal", "cycle_peak", "crowding", "price_only_memory_rally"),
        "HBM can be Green, but after large rerating it needs strong 4B-watch diagnostics for crowding and capex reversal.",
    ),
    Round22ScoreTarget(
        "VALUE_UP_SHAREHOLDER_RETURN",
        Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL,
        E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round22ScoreWeightDraft(15, 20, 5, 20, 25, 10, 5),
        ("value_up_disclosure", "buyback_or_dividend", "low_pbr", "governance_reform_news"),
        ("actual_cancellation", "repeat_shareholder_return", "roe_improvement", "nav_discount_narrowing_possible"),
        ("pbr_roe_or_nav_frame_change", "repeat_return_policy", "governance_discount_eases"),
        ("value_up_success_fully_recognized", "pbr_normalized", "event_premium_reflected"),
        ("buyback_not_cancelled", "subsidiary_value_damage", "credit_cost_up", "controlling_shareholder_risk"),
        ("actual_cancellation_or_dividend", "roe_or_fcf_improvement", "nav_discount_logic", "execution_evidence"),
        ("policy_headline_only", "buyback_no_cancel", "low_roe_value_trap", "governance_risk"),
        "Value-up can be Green only when execution, ROE/FCF, and PBR/NAV logic exist; policy expectation is Stage 1 only.",
    ),
)


ROUND22_CASE_CANDIDATES: tuple[Round22CaseCandidate, ...] = (
    Round22CaseCandidate("korea_brokerage_trading_value_rally_candidate", "SECURITIES_BROKERAGE_CYCLE", "BROKER_TURNOVER", "거래대금회복_증권사", "KR", "success_candidate", ("trading_value_growth", "brokerage_revenue_growth"), ("turnover_peak", "pf_loss"), "Brokerage candidate requires revenue and risk confirmation."),
    Round22CaseCandidate("securities_pf_loss_4c", "SECURITIES_BROKERAGE_CYCLE", "BROKER_PF_4C", "증권사_PF손실", "KR", "4c_thesis_break", ("brokerage_balance_sheet",), ("pf_loss", "capital_ratio_down"), "PF loss can override trading-value recovery."),
    Round22CaseCandidate("ipo_pipeline_recovery_candidate", "SECURITIES_BROKERAGE_CYCLE", "IPO_PIPE", "IPO파이프라인회복", "KR", "success_candidate", ("ipo_pipeline", "ib_fee_growth"), ("pipeline_delay", "market_turnover_peak"), "IB recovery needs actual fee conversion."),
    Round22CaseCandidate("vc_exit_market_weakness_counterexample", "SECURITIES_BROKERAGE_CYCLE", "VC_EXIT_WEAK", "VC회수시장부진", "KR", "failed_rerating", ("vc_portfolio",), ("exit_market_weakness", "valuation_markdown"), "VC recovery expectation without exits stays Watch."),
    Round22CaseCandidate("samsung_fire_underwriting_valueup_candidate", "INSURANCE_UNDERWRITING_CYCLE", "000810", "삼성화재", "KR", "success_candidate", ("loss_ratio_stability", "roe", "shareholder_return"), ("loss_ratio_worsens", "capital_ratio_down"), "Insurance value-up candidate; CSM/K-ICS/return evidence needs backfill."),
    Round22CaseCandidate("db_insurance_loss_ratio_candidate", "INSURANCE_UNDERWRITING_CYCLE", "005830", "DB손해보험", "KR", "success_candidate", ("loss_ratio_stability", "roe", "capital_ratio"), ("underwriting_deterioration", "return_retreat"), "Loss-ratio and ROE candidate."),
    Round22CaseCandidate("low_pbr_insurer_no_capital_return_counterexample", "INSURANCE_UNDERWRITING_CYCLE", "INS_LOW_PBR", "저PBR보험_환원부재", "KR", "failed_rerating", ("low_pbr",), ("capital_return_limited", "low_roe"), "Low PBR alone is not rerating evidence."),
    Round22CaseCandidate("sgi_ransomware_operational_risk_4c", "INSURANCE_UNDERWRITING_CYCLE", "031210", "서울보증보험_랜섬웨어", "KR", "4c_thesis_break", ("guarantee_insurance",), ("cyber_operational_risk", "service_outage"), "Insurance/financial infrastructure needs cyber operation guardrails."),
    Round22CaseCandidate("megastudy_private_education_candidate", "EDUCATION_SPECIALTY_SERVICES", "215200", "메가스터디교육", "KR", "success_candidate", ("repeat_courses", "pricing_power", "online_education"), ("regulation", "birthrate_decline"), "Education candidate requires proof that repeat/online offsets demographics."),
    Round22CaseCandidate("adult_education_subscription_candidate", "EDUCATION_SPECIALTY_SERVICES", "ADULT_EDU", "성인교육구독", "KR", "success_candidate", ("adult_education", "subscription_revenue"), ("ai_substitution", "churn"), "Adult/subscription education can offset birthrate risk."),
    Round22CaseCandidate("low_birthrate_kids_education_counterexample", "EDUCATION_SPECIALTY_SERVICES", "KIDS_BIRTHRATE", "키즈교육_저출산", "KR", "failed_rerating", ("kids_education",), ("birthrate_decline", "offline_fixed_cost"), "Kids education is structurally exposed to low birthrate."),
    Round22CaseCandidate("education_regulation_4c", "EDUCATION_SPECIALTY_SERVICES", "EDU_REG_4C", "사교육규제", "KR", "4c_thesis_break", ("private_education_revenue",), ("regulation", "price_cut"), "Regulatory pressure can break education pricing."),
    Round22CaseCandidate("convenience_store_pb_efficiency_candidate", "RETAIL_ECOMMERCE_LOGISTICS", "CONV_PB", "편의점_PB효율", "KR", "success_candidate", ("same_store_sales", "pb_mix", "opm_improvement"), ("rent_labor_pressure", "competition"), "Convenience store candidate needs per-store economics."),
    Round22CaseCandidate("cold_chain_recurring_logistics_candidate", "RETAIL_ECOMMERCE_LOGISTICS", "COLD_CHAIN", "콜드체인반복물류", "KR", "success_candidate", ("cold_chain_contracts", "repeat_logistics_revenue"), ("logistics_cost_up", "customer_loss"), "Cold-chain can be structural if contracts repeat and margins hold."),
    Round22CaseCandidate("ecommerce_fresh_loss_counterexample", "RETAIL_ECOMMERCE_LOGISTICS", "FRESH_LOSS", "신선식품이커머스적자", "KR", "failed_rerating", ("ecommerce_sales_growth",), ("fresh_delivery_loss", "logistics_cost_up"), "Fresh e-commerce sales growth without FCF is not structural."),
    Round22CaseCandidate("home_shopping_structural_decline_counterexample", "RETAIL_ECOMMERCE_LOGISTICS", "HOMESHOP_DECLINE", "홈쇼핑구조둔화", "KR", "failed_rerating", ("home_shopping_revenue",), ("channel_decline", "competition"), "Home-shopping structural decline should cap Green."),
    Round22CaseCandidate("cement_price_hike_candidate", "BUILDING_MATERIALS_REIT", "CEMENT_PRICE", "시멘트가격인상", "KR", "success_candidate", ("price_hike", "cost_stability"), ("volume_decline", "pf_stress"), "Price hike needs shipment and cost support."),
    Round22CaseCandidate("reit_rate_cut_dividend_candidate", "BUILDING_MATERIALS_REIT", "REIT_DIV", "리츠금리하락배당", "KR", "success_candidate", ("rate_down", "dividend_coverage", "occupancy"), ("refinancing_stress", "vacancy_up"), "REIT candidate needs occupancy and dividend coverage."),
    Round22CaseCandidate("pf_delinquency_building_materials_4c", "BUILDING_MATERIALS_REIT", "PF_MATERIALS_4C", "PF연체_건자재", "KR", "4c_thesis_break", ("building_materials_exposure",), ("pf_stress", "housing_starts_down"), "PF delinquency can overwhelm material price hikes."),
    Round22CaseCandidate("vacancy_dividend_cut_reit_4c", "BUILDING_MATERIALS_REIT", "REIT_VACANCY_4C", "리츠공실배당삭감", "KR", "4c_thesis_break", ("reit_income",), ("vacancy_up", "dividend_cut"), "Vacancy plus dividend cut is hard REIT risk."),
    Round22CaseCandidate("douzone_bizon_cloud_erp_candidate", "CLOUD_AI_SOFTWARE_INFRA", "012510", "더존비즈온", "KR", "success_candidate", ("cloud_erp", "recurring_revenue", "smb_lock_in"), ("ai_cost_overrun", "churn"), "Cloud ERP case needs margin/FCF backfill."),
    Round22CaseCandidate("ai_feature_no_fcf_counterexample", "CLOUD_AI_SOFTWARE_INFRA", "AI_SW_NO_FCF", "AI기능_무현금흐름", "KR", "failed_rerating", ("ai_feature_launch",), ("no_paid_usage", "no_fcf"), "AI feature without paid usage is not score evidence."),
    Round22CaseCandidate("cloud_cost_margin_pressure_4c", "CLOUD_AI_SOFTWARE_INFRA", "CLOUD_MARGIN_4C", "클라우드비용_마진압박", "KR", "4c_thesis_break", ("cloud_growth",), ("ai_cost_overrun", "opm_decline"), "Cloud growth can break if costs destroy margin."),
    Round22CaseCandidate("saas_churn_counterexample", "CLOUD_AI_SOFTWARE_INFRA", "SAAS_CHURN", "SaaS_Churn", "US", "failed_rerating", ("subscription_revenue",), ("churn", "retention_down"), "Subscription label needs retention evidence."),
    Round22CaseCandidate("icon_global_cro_scale_candidate", "CRO_CLINICAL_SERVICE", "ICLR", "ICON", "US", "success_candidate", ("global_cro_scale", "clinical_service_revenue"), ("funding_cycle", "customer_concentration"), "Global CRO scale candidate."),
    Round22CaseCandidate("medpace_growth_cro_candidate", "CRO_CLINICAL_SERVICE", "MEDP", "Medpace", "US", "success_candidate", ("cro_revenue_growth", "net_income_growth"), ("customer_concentration", "funding_cycle"), "Medpace is growth-CRO reference."),
    Round22CaseCandidate("biotech_funding_crunch_4c", "CRO_CLINICAL_SERVICE", "CRO_FUNDING_4C", "바이오펀딩크런치", "US", "4c_thesis_break", ("clinical_service_exposure",), ("biotech_funding_cycle_down", "order_cancellation"), "Funding crunch can break CRO demand."),
    Round22CaseCandidate("customer_budget_cut_cro_counterexample", "CRO_CLINICAL_SERVICE", "CRO_BUDGET_CUT", "CRO고객예산축소", "US", "failed_rerating", ("clinical_volume",), ("customer_budget_cut", "volume_without_margin"), "Clinical volume without margin is insufficient."),
    Round22CaseCandidate("kfashion_global_channel_candidate", "APPAREL_BRAND_OEM", "KFASHION_CHANNEL", "K패션글로벌채널", "KR", "success_candidate", ("global_channel_expansion", "repeat_brand_purchase"), ("inventory_build", "markdown"), "K-fashion candidate requires repeat channels and inventory control."),
    Round22CaseCandidate("apparel_oem_customer_diversification_candidate", "APPAREL_BRAND_OEM", "APPAREL_OEM", "의류OEM고객다변화", "KR", "success_candidate", ("order_visibility", "customer_diversification", "opm_improvement"), ("order_slowdown", "margin_squeeze"), "OEM candidate needs diversified customers and margin."),
    Round22CaseCandidate("inventory_markdown_4c", "APPAREL_BRAND_OEM", "APPAREL_MARKDOWN_4C", "의류재고할인4C", "KR", "4c_thesis_break", ("brand_sales",), ("inventory_increase", "discount_sales"), "Inventory and markdown can break apparel thesis."),
    Round22CaseCandidate("fashion_cycle_single_brand_counterexample", "APPAREL_BRAND_OEM", "FASHION_FAD", "단일브랜드유행", "KR", "failed_rerating", ("single_brand_hype",), ("single_fad_brand", "channel_concentration"), "Single brand fad remains Watch."),
    Round22CaseCandidate("sk_hynix_hbm_success_case", "MEMORY_HBM_CAPACITY", "000660", "SK하이닉스 HBM", "KR", "structural_success", ("hbm_demand", "supply_discipline", "medium_term_revision"), ("capex_reversal", "memory_price_down"), "HBM structural success candidate; exact price path must be source-filled."),
    Round22CaseCandidate("sk_hynix_4b_crowding_watch", "MEMORY_HBM_CAPACITY", "000660", "SK하이닉스 4B crowding", "KR", "4b_watch", ("one_to_two_year_price_surge", "global_crowding"), ("capex_reversal", "revision_slowdown"), "Successful HBM rerating needs 4B-watch after large price move."),
    Round22CaseCandidate("simple_dram_rebound_counterexample", "MEMORY_HBM_CAPACITY", "DRAM_REBOUND", "단순DRAM반등", "KR", "failed_rerating", ("memory_price_rebound",), ("no_medium_term_revision", "cycle_only"), "Simple DRAM rebound is cyclical unless medium-term evidence exists."),
    Round22CaseCandidate("ai_capex_cut_memory_4c", "MEMORY_HBM_CAPACITY", "MEMORY_CAPEX_4C", "AI_CAPEX둔화_메모리", "KR", "4c_thesis_break", ("hbm_exposure",), ("customer_ai_capex_slowdown", "memory_price_down"), "Customer AI CAPEX slowdown is a hard memory risk."),
    Round22CaseCandidate("sk_square_nav_discount_candidate", "VALUE_UP_SHAREHOLDER_RETURN", "402340", "SK스퀘어", "KR", "success_candidate", ("nav_discount", "buyback_cancellation", "subsidiary_value"), ("subsidiary_value_damage", "execution_risk"), "Value-up candidate needs execution and NAV logic."),
    Round22CaseCandidate("financial_valueup_pbr_roe_candidate", "VALUE_UP_SHAREHOLDER_RETURN", "FIN_VALUEUP", "금융Value-up", "KR", "success_candidate", ("pbr_roe_gap", "shareholder_return", "roe_improvement"), ("credit_cost_up", "return_retreat"), "Financial value-up needs ROE and return execution."),
    Round22CaseCandidate("buyback_no_cancel_counterexample", "VALUE_UP_SHAREHOLDER_RETURN", "BUYBACK_NO_CANCEL", "자사주미소각", "KR", "failed_rerating", ("buyback_announcement",), ("buyback_no_cancel", "policy_headline_only"), "Buyback without cancellation can be value trap."),
    Round22CaseCandidate("low_roe_value_trap_counterexample", "VALUE_UP_SHAREHOLDER_RETURN", "LOW_ROE_TRAP", "저ROE저PBR함정", "KR", "failed_rerating", ("low_pbr",), ("low_roe_value_trap", "no_return_execution"), "Low PBR without ROE/return improvement is not Green."),
)


def target_for(target_id: str) -> Round22ScoreTarget | None:
    for target in ROUND22_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round22_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND22_CASE_CANDIDATES:
        target = target_for(candidate.target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {candidate.target_id}")
        weights = target.score_weight.as_dict()
        record = E2RCaseRecord(
            case_id=candidate.case_id,
            symbol=candidate.symbol,
            company_name=candidate.company_name,
            market=candidate.market,
            sector_raw=candidate.target_id,
            primary_archetype=target.canonical_archetype,
            expected_group=candidate.expected_group,
            large_sector=target.large_sector.value,
            case_type=candidate.case_type,
            evidence_summary=(
                f"Round22 v0.7 calibration candidate for {candidate.target_id}; "
                "stage dates, prices, and numeric fields remain unfilled until source backfill."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=tuple(field for field in candidate.evidence_fields if field in target.green_conditions),
            stage3_evidence=(),
            stage4b_evidence=candidate.evidence_fields if candidate.case_type == "4b_watch" else (),
            stage4c_evidence=candidate.red_flag_fields if candidate.case_type == "4c_thesis_break" else (),
            must_have_fields=target.green_conditions,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason="; ".join(candidate.red_flag_fields) if candidate.case_type != "success_candidate" and candidate.case_type != "structural_success" else None,
            score_price_alignment="unknown",
            rerating_result="unknown",
            price_pattern="unknown",
            score_weight_hint={
                "eps_fcf": float(weights["eps_fcf"]),
                "visibility": float(weights["structural_visibility"]),
                "bottleneck": float(weights["bottleneck_pricing"]),
                "mispricing": float(weights["market_mispricing"]),
                "valuation": float(weights["valuation"]),
                "capital_allocation": float(weights["capital_allocation"]),
            },
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "require_price_path_validation",
                "require_cross_evidence_for_green",
                *target.red_flags,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(price_validation_status="needs_price_backfill"),
            data_quality=CaseDataQuality(False, False, False, 0.0),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round22_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND22_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "eps_fcf": str(weights["eps_fcf"]),
                "structural_visibility": str(weights["structural_visibility"]),
                "bottleneck_pricing": str(weights["bottleneck_pricing"]),
                "market_mispricing": str(weights["market_mispricing"]),
                "valuation": str(weights["valuation"]),
                "capital_allocation": str(weights["capital_allocation"]),
                "information_confidence": str(weights["information_confidence"]),
                "stage1_signals": "|".join(target.stage1_signals),
                "stage2_signals": "|".join(target.stage2_signals),
                "stage3_conditions": "|".join(target.stage3_conditions),
                "stage4b_conditions": "|".join(target.stage4b_conditions),
                "stage4c_conditions": "|".join(target.stage4c_conditions),
                "green_conditions": "|".join(target.green_conditions),
                "red_flags": "|".join(target.red_flags),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round22_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND22_CASE_CANDIDATES:
        target = target_for(candidate.target_id)
        assert target is not None
        rows.append(
            {
                "case_id": candidate.case_id,
                "target_id": candidate.target_id,
                "symbol": candidate.symbol,
                "company_name": candidate.company_name,
                "market": candidate.market,
                "case_type": candidate.case_type,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "evidence_fields": "|".join(candidate.evidence_fields),
                "red_flag_fields": "|".join(candidate.red_flag_fields),
                "price_validation_status": "needs_price_backfill",
                "production_input": "false",
                "notes": candidate.notes,
            }
        )
    return tuple(rows)


def round22_summary() -> dict[str, int | bool]:
    records = round22_case_records()
    positive = sum(1 for record in records if record.case_type in {"success_candidate", "structural_success"})
    return {
        "target_count": len(ROUND22_SCORE_TARGETS),
        "case_candidate_count": len(records),
        "success_candidate_count": positive,
        "counterexample_or_risk_count": len(records) - positive,
        "green_possible_count": sum(1 for target in ROUND22_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND22_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round22_score_weight_reports(
    *,
    output_directory: str | Path = ROUND22_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND22_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND22_DEFAULT_SCORE_PROFILE_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    cases = Path(cases_path)
    score_profiles = Path(score_profile_path)
    cases.parent.mkdir(parents=True, exist_ok=True)
    score_profiles.parent.mkdir(parents=True, exist_ok=True)
    paths = {
        "cases": cases,
        "score_profiles": score_profiles,
        "summary": output / "round22_score_weight_v07_summary.md",
        "case_matrix": output / "round22_case_candidate_matrix.csv",
        "green_guardrails": output / "round22_green_guardrail_review.md",
        "price_validation_plan": output / "round22_price_validation_plan.md",
        "stage4b_watch_review": output / "round22_stage4b_watch_review.md",
    }
    _write_case_jsonl(round22_case_records(), cases)
    _write_rows(round22_score_profile_rows(), score_profiles)
    _write_rows(round22_case_candidate_rows(), paths["case_matrix"])
    paths["summary"].write_text(render_round22_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round22_green_guardrail_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round22_price_validation_plan_markdown(), encoding="utf-8")
    paths["stage4b_watch_review"].write_text(render_round22_stage4b_watch_markdown(), encoding="utf-8")
    return paths


def render_round22_summary_markdown() -> str:
    summary = round22_summary()
    lines = [
        "# Round-22 Score-Weight v0.7 Summary",
        "",
        f"- source_round: `{ROUND22_SOURCE_ROUND_PATH}`",
        f"- target_count: {summary['target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- counterexample_or_risk_count: {summary['counterexample_or_risk_count']}",
        f"- green_possible_count: {summary['green_possible_count']}",
        f"- watch_yellow_first_count: {summary['watch_yellow_first_count']}",
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "- Round 22 recalibrates score-weight hypotheses, not production scoring.",
        "- Example: 증권사는 거래대금이 늘어도 지속성이 약하므로 Watch-first로 둔다.",
        "- Example: 보험은 EPS 폭발보다 손해율, CSM/ROE, 자본비율, 환원 실행을 본다.",
        "- Example: HBM은 Green 가능하지만 큰 리레이팅 이후에는 4B-watch crowding을 강하게 본다.",
        "- Theme names, case IDs, and policy headlines are not score evidence.",
    ]
    return "\n".join(lines) + "\n"


def render_round22_green_guardrail_markdown() -> str:
    lines = [
        "# Round-22 Green Guardrail Review",
        "",
        "| target | posture | Green unlock evidence | Red flags |",
        "|---|---|---|---|",
    ]
    for target in ROUND22_SCORE_TARGETS:
        lines.append(
            "| "
            f"{target.target_id} | {target.posture.value} | "
            f"{', '.join(target.green_conditions)} | {', '.join(target.red_flags)} |"
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "- Do not apply v0.7 weights to production scoring yet.",
            "- Do not make Stage 3-Green easier for brokerage, education, retail, construction, or apparel.",
            "- Do not turn policy headlines, low PBR, AI features, or trading-value spikes into score evidence by themselves.",
            "- Do not invent prices, stage dates, CSM, K-ICS, ARR, FCF, turnover, margins, or contract values.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round22_price_validation_plan_markdown() -> str:
    return "\n".join(
        [
            "# Round-22 Price Validation Plan",
            "",
            "1. Backfill official price paths for cases with tradable symbols.",
            "2. Keep reference cases as `needs_price_backfill` or `missing_price_data` until usable data exists.",
            "3. Calculate stage prices, peak prices, MFE/MAE, and drawdown only from source data.",
            "4. Compare v0.7 shadow weights against price-path and EPS/FCF evidence.",
            "5. Keep production StageClassifier and score weights unchanged until coverage and price validation are sufficient.",
            "",
            "## Priority Validation",
            "- Brokerage: turnover rally versus PF/proprietary loss.",
            "- Insurance/value-up: shareholder return execution versus low-PBR value trap.",
            "- Memory/HBM: structural rerating versus 4B crowding and capex reversal.",
            "- Retail/apparel: OPM/FCF versus inventory, markdown, and logistics cost.",
        ]
    ) + "\n"


def render_round22_stage4b_watch_markdown() -> str:
    hbm = target_for("MEMORY_HBM_CAPACITY")
    value_up = target_for("VALUE_UP_SHAREHOLDER_RETURN")
    lines = [
        "# Round-22 4B Watch Review",
        "",
        "Round 22 explicitly separates successful rerating from post-rerating crowding.",
        "",
        "## MEMORY_HBM_CAPACITY",
        "",
    ]
    if hbm:
        lines.extend(f"- {item}" for item in hbm.stage4b_conditions)
    lines.extend(
        [
            "",
            "## VALUE_UP_SHAREHOLDER_RETURN",
            "",
        ]
    )
    if value_up:
        lines.extend(f"- {item}" for item in value_up.stage4b_conditions)
    lines.extend(
        [
            "",
            "## Rule",
            "- Price-only 4B evidence remains `price_only_4b_watch`, not full 4B.",
            "- Full 4B needs slowdown, saturation, crowding, execution risk, or evidence deterioration.",
        ]
    )
    return "\n".join(lines) + "\n"


def _write_case_jsonl(records: Iterable[E2RCaseRecord], path: Path) -> Path:
    lines = []
    for record in records:
        record.validate()
        lines.append(json.dumps(record.as_dict(), ensure_ascii=False, sort_keys=True))
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return path


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
    "ROUND22_CASE_CANDIDATES",
    "ROUND22_DEFAULT_CASES_PATH",
    "ROUND22_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND22_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND22_SCORE_TARGETS",
    "ROUND22_SOURCE_ROUND_PATH",
    "Round22CaseCandidate",
    "Round22ScoreTarget",
    "Round22ScoreWeightDraft",
    "render_round22_green_guardrail_markdown",
    "render_round22_price_validation_plan_markdown",
    "render_round22_stage4b_watch_markdown",
    "render_round22_summary_markdown",
    "round22_case_candidate_rows",
    "round22_case_records",
    "round22_score_profile_rows",
    "round22_summary",
    "target_for",
    "write_round22_score_weight_reports",
]
