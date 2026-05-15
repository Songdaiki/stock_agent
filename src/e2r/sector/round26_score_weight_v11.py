"""Round-26 cases_v08 expansion and score-weight v1.1 hypotheses.

Round 26 broadens v1.1 calibration across AI infrastructure, K-beauty,
fintech, renewables, construction credit, and financial cycles. It is
report-only calibration material. Production feature engineering, scoring,
staging, and RedTeam code must not import this module.
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


ROUND26_SOURCE_ROUND_PATH = "docs/round/round_26.md"
ROUND26_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round26_score_weight_v11"
ROUND26_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_v08_round26.jsonl"
ROUND26_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round26_v11.csv"


@dataclass(frozen=True)
class Round26ScoreWeightDraft:
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
class Round26ScoreTarget:
    target_id: str
    large_sector: Round10LargeSector
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round26ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    normalization_point: str

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round26CaseCandidate:
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


ROUND26_SCORE_TARGETS: tuple[Round26ScoreTarget, ...] = (
    Round26ScoreTarget(
        "AI_DATA_CENTER_COOLING",
        Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS,
        E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round26ScoreWeightDraft(21, 22, 22, 13, 12, 0, 5),
        ("liquid_cooling_keyword", "hvac_acquisition", "high_density_server_heat", "ai_datacenter_capex"),
        ("customer_datacenter_capex_link", "confirmed_order_or_delivery", "cooling_bottleneck", "op_eps_revision"),
        ("direct_capex_link", "delivery_or_service_revenue", "cooling_bottleneck_position", "repeat_service_revenue"),
        ("customer_datacenter_capex_link", "confirmed_order_or_delivery", "cooling_bottleneck", "repeat_service_revenue", "op_eps_revision"),
        ("liquid_cooling_theme_only", "no_customer_order", "ai_capex_delay", "low_margin_project", "customer_concentration"),
        ("ai_cooling_narrative_crowded", "orders_fully_priced", "capex_pull_forward"),
        ("ai_capex_delay", "project_margin_damage", "customer_order_delay", "service_attach_failure"),
        "AI cooling is Green-possible only when cooling bottleneck evidence turns into orders, delivery, service revenue, and OP revision.",
    ),
    Round26ScoreTarget(
        "MEMORY_HBM_CAPACITY",
        Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS,
        E2RArchetype.MEMORY_HBM_CAPACITY,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round26ScoreWeightDraft(24, 21, 19, 15, 12, 0, 5),
        ("hbm_demand", "memory_price_increase", "earnings_turnaround"),
        ("fy1_fy2_fy3_revision", "dram_nand_hbm_pricing", "supply_discipline", "customer_supply_preorder"),
        ("long_term_contract_or_prepayment", "price_band", "capacity_constraint", "multi_year_revision", "cyclical_discount_removed"),
        ("hbm_demand", "supply_discipline", "medium_term_revision", "capacity_constraint", "long_term_contract_or_prepayment"),
        ("capex_reversal", "cycle_peak", "crowding", "price_only_memory_rally", "customer_ai_capex_slowdown"),
        ("one_to_two_year_price_surge", "market_cap_multiple_saturation", "customer_price_resistance", "capex_expansion", "global_crowding"),
        ("memory_price_down", "supply_glut", "customer_ai_capex_slowdown", "consensus_revision_down"),
        "HBM remains Green-possible, but successful rerating must automatically turn on 4B-watch diagnostics.",
    ),
    Round26ScoreTarget(
        "K_BEAUTY_EXPORT_DISTRIBUTION",
        Round10LargeSector.CONSUMER_RETAIL_BRAND,
        E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round26ScoreWeightDraft(22, 23, 12, 16, 13, 0, 5),
        ("kbeauty_export_growth", "us_japan_channel", "offline_retail_entry", "viral_demand"),
        ("repeat_orders", "customer_diversification", "opm_roe_improvement", "china_dependency_down"),
        ("global_channel_expansion", "repeat_sell_through", "inventory_discipline", "new_export_frame"),
        ("export_growth", "channel_diversification", "repeat_orders", "opm_roe_improvement", "inventory_receivables_clean"),
        ("inventory", "receivables", "china_dependency", "tariff", "channel_stuffing", "viral_only"),
        ("kbeauty_crowding", "offline_channel_success_priced"),
        ("channel_stuffing", "inventory_build", "receivables_spike", "tariff_damage", "sell_through_slowdown"),
        "K-beauty can be Green when export channels repeat and inventory/receivables remain clean; viral shipment alone is not enough.",
    ),
    Round26ScoreTarget(
        "DIGITAL_ASSET_TOKENIZATION",
        Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL,
        E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round26ScoreWeightDraft(16, 18, 8, 16, 12, 3, 5),
        ("stablecoin_bill", "sto_law_expectation", "fintech_partnership", "tokenization_theme"),
        ("license_or_approval", "actual_issuance", "transaction_volume", "fee_model"),
        ("payment_or_custody_infrastructure_sticky", "regulated_revenue", "liquidity_risk_low", "fcf_visible"),
        ("license_or_approval", "actual_issuance", "transaction_volume", "fee_or_spread_revenue", "regulatory_risk_low"),
        ("regulation", "security", "adoption", "liquidity", "no_revenue", "theme_only"),
        ("tokenization_event_priced", "crypto_theme_crowded"),
        ("regulatory_delay", "security_incident", "volume_failure", "liquidity_break", "revenue_model_failure"),
        "Digital assets remain Watch-first until regulation, issuance, volume, and fee economics are proven.",
    ),
    Round26ScoreTarget(
        "HYDROGEN_RENEWABLE",
        Round10LargeSector.BATTERY_EV_GREEN,
        E2RArchetype.UTILITIES_REGULATED_TARIFF,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round26ScoreWeightDraft(18, 18, 12, 12, 10, 0, 5),
        ("hydrogen_capex", "solar_policy", "fuel_cell_plant", "renewable_subsidy"),
        ("production_capacity", "utilization_up", "customer_or_government_demand", "op_eps_conversion"),
        ("capex_to_revenue_conversion", "stable_subsidy_or_tariff", "supply_chain_stable", "margin_visible"),
        ("actual_capex", "utilization_up", "customer_or_government_demand", "op_eps_conversion", "policy_risk_low"),
        ("policy", "subsidy", "tariff", "customs", "supply_chain", "utilization"),
        ("renewable_policy_theme_priced", "hydrogen_theme_crowded"),
        ("customs_detention", "component_delay", "subsidy_cut", "project_delay", "utilization_failure"),
        "Hydrogen/solar is Watch-first: policy themes need capex, utilization, customers, and OP conversion.",
    ),
    Round26ScoreTarget(
        "CLOUD_AI_SOFTWARE_INFRA",
        Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY,
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round26ScoreWeightDraft(20, 23, 8, 16, 14, 0, 5),
        ("cloud_transition", "erp_saas_demand", "ai_feature_launch", "b2b_customer_growth"),
        ("recurring_revenue_growth", "arpu_up", "opm_improvement", "retention_confirmed"),
        ("customer_lock_in", "fcf_conversion", "pricing_power", "old_si_or_legacy_software_frame"),
        ("recurring_revenue", "arpu", "retention", "opm_or_fcf_improvement", "ai_cost_control"),
        ("ai_feature_only", "ai_cost_overrun", "churn", "si_revenue_only", "opm_decline"),
        ("saas_ai_narrative_overheated", "multiple_saturation"),
        ("churn", "ai_cost_overrun", "opm_decline", "competition_intensifies"),
        "Cloud/SaaS can be Green, but AI wording is only Stage 1 unless recurring revenue, OPM, and FCF improve.",
    ),
    Round26ScoreTarget(
        "SECURITY_IDENTITY_DEEPFAKE",
        Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY,
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round26ScoreWeightDraft(20, 20, 10, 14, 13, 0, 5),
        ("security_threat_growth", "deepfake_regulation", "identity_or_cctv_demand", "government_security_budget"),
        ("recurring_subscription", "customer_retention", "opm_improvement", "enterprise_or_government_contract"),
        ("mission_critical_lock_in", "low_churn", "customer_diversification", "fcf_conversion", "operational_trust_intact"),
        ("recurring_subscription", "low_churn", "customer_diversification", "opm_improvement", "no_major_outage"),
        ("operational_trust", "outage", "legal", "customer_retention", "contract_absence"),
        ("security_theme_crowded", "deepfake_regulation_priced"),
        ("major_outage", "legal_claim", "customer_churn", "contract_loss", "trust_break"),
        "Security can be structural, but operational trust is a hard gate because one outage can become 4C.",
    ),
    Round26ScoreTarget(
        "CRO_CLINICAL_SERVICE",
        Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE,
        E2RArchetype.CDMO_HEALTHCARE_CONTRACT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round26ScoreWeightDraft(18, 20, 8, 12, 12, 0, 5),
        ("clinical_trial_count_growth", "pharma_rd_growth", "order_backlog_growth"),
        ("sales_op_growth", "customer_diversification", "repeat_service_revenue"),
        ("multi_year_backlog", "customer_portfolio_diversified", "funding_cycle_stable", "high_margin_service_mix"),
        ("service_backlog", "customer_diversification", "repeat_clinical_service_revenue", "opm_improvement", "funding_cycle_stable"),
        ("biotech_funding_cycle_down", "customer_concentration", "trial_delay", "low_margin_backlog", "customer_budget_cut"),
        ("biotech_rd_expectation_overheated", "service_multiple_saturation"),
        ("clinical_trial_cut", "customer_budget_cut", "order_cancellation", "forecast_cut"),
        "CRO is Watch-to-Green: stronger than pre-revenue biotech, weaker than CDMO due funding-cycle exposure.",
    ),
    Round26ScoreTarget(
        "CONSTRUCTION_BUILDING_MATERIALS",
        Round10LargeSector.CONSTRUCTION_REAL_ESTATE_MATERIALS,
        E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round26ScoreWeightDraft(17, 12, 12, 12, 12, 5, 5),
        ("price_hike", "housing_start_recovery", "rate_down", "relief_rally"),
        ("shipment_recovery", "cost_stability", "pf_risk_low", "fcf_or_dividend_stable"),
        ("supply_rationalization", "pricing_power", "credit_risk_contained", "cash_flow_recovery"),
        ("cost_stability", "price_pass_through", "shipment_recovery", "pf_risk_low", "fcf_improvement"),
        ("credit", "rates", "vacancy", "pf", "unsold_inventory", "relief_only"),
        ("rate_cut_reit_theme_priced", "construction_relief_priced"),
        ("pf_delinquency", "unsold_inventory", "liquidity_stress", "dividend_cut", "cost_up"),
        "Construction/materials stay Watch-first because PF, unsold inventory, rates, and liquidity can dominate order headlines.",
    ),
    Round26ScoreTarget(
        "INSURANCE_UNDERWRITING_CYCLE",
        Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL,
        E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round26ScoreWeightDraft(15, 21, 4, 15, 25, 10, 5),
        ("low_pbr", "value_up_disclosure", "loss_ratio_improvement", "dividend_or_buyback_expectation"),
        ("roe_improvement", "csm_growth", "capital_ratio_stable", "shareholder_return_execution"),
        ("pbr_roe_frame_change", "repeat_shareholder_return", "underwriting_profit_stable", "credit_risk_low"),
        ("roe_improvement", "csm_or_loss_ratio_stability", "capital_ratio_stable", "shareholder_return_execution", "credit_risk_low"),
        ("underwriting", "capital_ratio", "cyber_operational", "credit_cost", "low_pbr_only"),
        ("pbr_normalized", "insurance_value_up_crowded", "return_expectation_priced"),
        ("loss_ratio_worsens", "capital_ratio_down", "cyber_operational_risk", "credit_cost_up", "shareholder_return_retreat"),
        "Insurance is PBR-ROE-return rerating, not EPS explosion; underwriting, capital, and cyber resilience are gates.",
    ),
    Round26ScoreTarget(
        "SECURITIES_BROKERAGE_CYCLE",
        Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL,
        E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round26ScoreWeightDraft(18, 14, 5, 15, 18, 8, 5),
        ("trading_value_growth", "equity_market_rally", "ipo_ib_recovery_expectation", "vc_exit_expectation"),
        ("brokerage_revenue_growth", "ib_fee_growth", "capital_ratio_stable", "op_eps_revision"),
        ("repeat_turnover_or_ib_recovery", "pf_risk_low", "roe_structure_improves", "shareholder_return_capacity"),
        ("brokerage_revenue_growth", "ib_pipeline", "capital_ratio_stable", "pf_risk_low", "roe_improvement"),
        ("market_turnover", "pf", "proprietary_loss", "ipo_cycle", "vc_exit_market_weakness"),
        ("market_turnover_peak", "brokerage_group_overheated", "ipo_expectation_priced"),
        ("trading_value_collapse", "pf_loss", "proprietary_loss", "capital_ratio_down", "ipo_pipeline_delay"),
        "Brokerage remains Watch-first because turnover and IPO recovery can reverse faster than banks or insurers.",
    ),
)


ROUND26_CASE_CANDIDATES: tuple[Round26CaseCandidate, ...] = (
    Round26CaseCandidate("ecolab_coolit_ai_liquid_cooling_candidate", "AI_DATA_CENTER_COOLING", "ECL_COOLIT", "Ecolab/CoolIT AI liquid cooling", "US", "success_candidate", ("customer_datacenter_capex_link", "cooling_bottleneck", "confirmed_order_or_delivery"), ("customer_concentration", "project_margin"), "AI cooling candidate needs delivery, service revenue, and OP revision backfill."),
    Round26CaseCandidate("samsung_flaktgroup_hvac_candidate", "AI_DATA_CENTER_COOLING", "005930_FLKT", "Samsung FlaktGroup HVAC", "KR", "success_candidate", ("hvac_acquisition", "ai_datacenter_capex"), ("non_core_exposure", "revenue_exposure_unclear"), "HVAC acquisition supports search routing; revenue exposure must be proven."),
    Round26CaseCandidate("liquid_cooling_theme_no_order_counterexample", "AI_DATA_CENTER_COOLING", "COOLING_THEME", "액체냉각테마_무수주", "KR", "failed_rerating", ("liquid_cooling_keyword",), ("liquid_cooling_theme_only", "no_customer_order"), "Cooling keyword without order is not score evidence."),
    Round26CaseCandidate("ai_capex_delay_cooling_4c", "AI_DATA_CENTER_COOLING", "COOL_CAPEX_4C", "AI_CAPEX지연_냉각", "US", "4c_thesis_break", ("cooling_project_pipeline",), ("ai_capex_delay", "customer_order_delay"), "AI CAPEX delay can break cooling backlog assumptions."),
    Round26CaseCandidate("sk_hynix_hbm_success_case", "MEMORY_HBM_CAPACITY", "000660", "SK하이닉스 HBM", "KR", "structural_success", ("hbm_demand", "supply_discipline", "medium_term_revision"), ("capex_reversal", "memory_price_down"), "HBM structural success candidate; exact price path must be source-filled."),
    Round26CaseCandidate("sk_hynix_4b_crowding_watch", "MEMORY_HBM_CAPACITY", "000660", "SK하이닉스 4B crowding", "KR", "4b_watch", ("one_to_two_year_price_surge", "global_crowding", "market_cap_multiple_saturation"), ("capex_reversal", "revision_slowdown"), "Successful HBM rerating needs 4B-watch after large price move."),
    Round26CaseCandidate("simple_dram_rebound_counterexample", "MEMORY_HBM_CAPACITY", "DRAM_REBOUND", "단순DRAM반등", "KR", "failed_rerating", ("memory_price_rebound",), ("no_medium_term_revision", "cycle_only"), "Simple DRAM rebound is cyclical unless medium-term evidence exists."),
    Round26CaseCandidate("ai_capex_cut_memory_4c", "MEMORY_HBM_CAPACITY", "MEMORY_CAPEX_4C", "AI_CAPEX둔화_메모리", "KR", "4c_thesis_break", ("hbm_exposure",), ("customer_ai_capex_slowdown", "memory_price_down"), "Customer AI CAPEX slowdown is a hard memory risk."),
    Round26CaseCandidate("kbeauty_us_offline_channel_candidate", "K_BEAUTY_EXPORT_DISTRIBUTION", "KBEAUTY_US", "K뷰티 미국오프라인채널", "KR", "success_candidate", ("export_growth", "offline_retail_entry", "repeat_orders"), ("tariff", "inventory"), "US offline expansion needs sell-through and inventory discipline."),
    Round26CaseCandidate("kbeauty_oem_odm_customer_diversification_candidate", "K_BEAUTY_EXPORT_DISTRIBUTION", "KBEAUTY_ODM", "K뷰티 OEM/ODM 고객다변화", "KR", "success_candidate", ("customer_diversification", "opm_roe_improvement"), ("customer_concentration", "receivables"), "OEM/ODM needs diversified customers and margin evidence."),
    Round26CaseCandidate("china_dependency_cosmetic_counterexample", "K_BEAUTY_EXPORT_DISTRIBUTION", "KBEAUTY_CHINA", "중국의존화장품", "KR", "failed_rerating", ("cosmetic_sales",), ("china_dependency", "channel_concentration"), "China dependency caps Green until channel mix changes."),
    Round26CaseCandidate("channel_stuffing_inventory_receivables_4c", "K_BEAUTY_EXPORT_DISTRIBUTION", "KBEAUTY_STUFFING_4C", "채널스터핑재고채권4C", "KR", "4c_thesis_break", ("shipment_growth",), ("channel_stuffing", "inventory_build", "receivables_spike"), "Shipment growth without sell-through can become 4C."),
    Round26CaseCandidate("toss_won_stablecoin_candidate", "DIGITAL_ASSET_TOKENIZATION", "TOSS_STABLE", "토스 원화 스테이블코인", "KR", "success_candidate", ("stablecoin_plan", "fintech_platform"), ("regulatory_delay", "no_revenue"), "Stablecoin candidate needs approval, issuance, volume, and fee economics."),
    Round26CaseCandidate("stablecoin_regulatory_delay_4c", "DIGITAL_ASSET_TOKENIZATION", "STABLE_REG_4C", "스테이블코인규제지연", "KR", "4c_thesis_break", ("stablecoin_plan",), ("regulatory_delay", "no_issuance"), "Regulatory delay can break tokenization thesis."),
    Round26CaseCandidate("sto_law_expectation_without_revenue_counterexample", "DIGITAL_ASSET_TOKENIZATION", "STO_NO_REV", "STO법제화기대_무매출", "KR", "failed_rerating", ("sto_law_expectation",), ("no_revenue", "theme_only"), "STO law expectation is Stage 1 until revenue appears."),
    Round26CaseCandidate("crypto_theme_no_revenue_counterexample", "DIGITAL_ASSET_TOKENIZATION", "CRYPTO_THEME", "코인테마_무매출", "KR", "failed_rerating", ("crypto_theme",), ("theme_only", "no_revenue"), "Crypto theme without business economics is not score evidence."),
    Round26CaseCandidate("hyundai_hydrogen_fuel_cell_plant_candidate", "HYDROGEN_RENEWABLE", "005380_H2", "현대차 수소연료전지공장", "KR", "success_candidate", ("hydrogen_capex", "fuel_cell_plant"), ("utilization_failure", "policy_risk"), "Hydrogen plant needs utilization, customers, and OP conversion backfill."),
    Round26CaseCandidate("qcells_customs_detention_4c", "HYDROGEN_RENEWABLE", "QCELLS_CUSTOMS", "Qcells 통관억류", "KR", "4c_thesis_break", ("solar_factory_capacity",), ("customs_detention", "factory_furlough"), "Customs detention can break solar policy-benefit thesis."),
    Round26CaseCandidate("hydrogen_theme_no_revenue_counterexample", "HYDROGEN_RENEWABLE", "H2_THEME", "수소테마_무매출", "KR", "failed_rerating", ("hydrogen_policy",), ("theme_only", "no_revenue_conversion"), "Hydrogen theme without revenue is not score evidence."),
    Round26CaseCandidate("solar_subsidy_dependency_counterexample", "HYDROGEN_RENEWABLE", "SOLAR_SUBSIDY", "태양광보조금의존", "KR", "failed_rerating", ("subsidy_expectation",), ("subsidy_dependency", "policy_reversal"), "Subsidy expectation alone is not Green evidence."),
    Round26CaseCandidate("douzone_bizon_cloud_erp_candidate", "CLOUD_AI_SOFTWARE_INFRA", "012510", "더존비즈온 클라우드 ERP", "KR", "success_candidate", ("cloud_erp", "recurring_revenue", "smb_lock_in"), ("ai_cost_overrun", "churn"), "Cloud ERP candidate needs OPM and FCF backfill."),
    Round26CaseCandidate("ai_feature_no_fcf_counterexample", "CLOUD_AI_SOFTWARE_INFRA", "AI_SW_NO_FCF", "AI기능_무현금흐름", "KR", "failed_rerating", ("ai_feature_launch",), ("no_paid_usage", "no_fcf"), "AI feature without paid usage is not structural evidence."),
    Round26CaseCandidate("cloud_cost_margin_pressure_4c", "CLOUD_AI_SOFTWARE_INFRA", "CLOUD_MARGIN_4C", "클라우드비용_마진압박", "KR", "4c_thesis_break", ("cloud_growth",), ("ai_cost_overrun", "opm_decline"), "Cloud growth can break if AI/cloud costs destroy margin."),
    Round26CaseCandidate("saas_churn_counterexample", "CLOUD_AI_SOFTWARE_INFRA", "SAAS_CHURN", "SaaS churn", "US", "failed_rerating", ("subscription_revenue",), ("churn", "retention_down"), "Subscription label needs retention evidence."),
    Round26CaseCandidate("recurring_security_subscription_candidate", "SECURITY_IDENTITY_DEEPFAKE", "SEC_SUB", "보안반복구독", "KR", "success_candidate", ("recurring_subscription", "customer_retention"), ("major_outage", "legal_claim"), "Security subscription can score with retention and no major outage."),
    Round26CaseCandidate("crowdstrike_outage_4c", "SECURITY_IDENTITY_DEEPFAKE", "CRWD", "CrowdStrike outage", "US", "4c_thesis_break", ("security_subscription",), ("major_outage", "legal_claim"), "Major outage is hard 4C risk even for recurring security revenue."),
    Round26CaseCandidate("deepfake_regulation_stage1_candidate", "SECURITY_IDENTITY_DEEPFAKE", "DEEPFAKE_REG", "딥페이크규제Stage1", "KR", "success_candidate", ("deepfake_regulation", "security_demand"), ("contract_absence", "theme_only"), "Deepfake regulation is Stage 1 until contracts or subscription revenue appear."),
    Round26CaseCandidate("security_theme_no_contract_counterexample", "SECURITY_IDENTITY_DEEPFAKE", "SEC_THEME", "보안테마_무계약", "KR", "failed_rerating", ("security_theme",), ("contract_absence", "theme_only"), "Security theme without contract is not score evidence."),
    Round26CaseCandidate("cro_revenue_backlog_candidate", "CRO_CLINICAL_SERVICE", "CRO_BACKLOG", "CRO 매출수주잔고", "KR", "success_candidate", ("service_backlog", "clinical_service_revenue"), ("customer_budget_cut", "funding_cycle"), "CRO can score when backlog converts to revenue."),
    Round26CaseCandidate("charles_river_funding_crunch_4c", "CRO_CLINICAL_SERVICE", "CRL", "Charles River funding crunch", "US", "4c_thesis_break", ("biotech_service_revenue",), ("biotech_funding_cycle_down", "forecast_cut"), "Funding crunch can turn CRO visibility into 4C."),
    Round26CaseCandidate("biotech_customer_budget_cut_counterexample", "CRO_CLINICAL_SERVICE", "CRO_BUDGET_CUT", "바이오고객예산축소", "US", "failed_rerating", ("clinical_volume",), ("customer_budget_cut", "volume_without_margin"), "Clinical volume is insufficient if customer budgets decline."),
    Round26CaseCandidate("cro_customer_diversification_success_candidate", "CRO_CLINICAL_SERVICE", "CRO_DIVERSIFIED", "CRO 고객다변화", "KR", "success_candidate", ("customer_diversification", "repeat_service_revenue"), ("funding_cycle", "customer_concentration"), "Diversified customers can improve CRO visibility."),
    Round26CaseCandidate("pf_delinquency_4c", "CONSTRUCTION_BUILDING_MATERIALS", "PF_DELINQ_4C", "PF연체4C", "KR", "4c_thesis_break", ("construction_credit_exposure",), ("pf_delinquency", "liquidity_stress"), "PF delinquency is hard RedTeam evidence."),
    Round26CaseCandidate("building_materials_price_hike_candidate", "CONSTRUCTION_BUILDING_MATERIALS", "MATERIAL_PRICE", "건자재가격인상", "KR", "success_candidate", ("price_hike", "cost_stability"), ("pf", "volume_decline"), "Price hike candidate needs shipment, cost, and credit checks."),
    Round26CaseCandidate("reit_rate_cut_dividend_candidate", "CONSTRUCTION_BUILDING_MATERIALS", "REIT_RATE", "리츠금리하락배당", "KR", "success_candidate", ("rate_down", "dividend_stability"), ("vacancy", "dividend_cut"), "REIT candidate needs occupancy and dividend coverage."),
    Round26CaseCandidate("builder_liquidity_support_relief_rally_counterexample", "CONSTRUCTION_BUILDING_MATERIALS", "BUILDER_RELIEF", "건설사지원랠리", "KR", "failed_rerating", ("liquidity_support",), ("relief_only", "unsold_inventory"), "Liquidity support can be relief rally, not structural rerating."),
    Round26CaseCandidate("insurer_underwriting_valueup_candidate", "INSURANCE_UNDERWRITING_CYCLE", "INS_VALUEUP", "보험언더라이팅Value-up", "KR", "success_candidate", ("loss_ratio_stability", "roe", "shareholder_return"), ("loss_ratio_worsens", "capital_ratio_down"), "Insurance candidate needs CSM/K-ICS and return execution backfill."),
    Round26CaseCandidate("low_pbr_insurer_no_capital_return_counterexample", "INSURANCE_UNDERWRITING_CYCLE", "INS_LOW_PBR", "저PBR보험_환원부재", "KR", "failed_rerating", ("low_pbr",), ("capital_return_limited", "low_roe"), "Low PBR without return execution is value trap risk."),
    Round26CaseCandidate("brokerage_trading_value_rally_candidate", "SECURITIES_BROKERAGE_CYCLE", "BROKER_TURNOVER", "거래대금회복_증권사", "KR", "success_candidate", ("trading_value_growth", "brokerage_revenue_growth"), ("turnover_peak", "pf_loss"), "Brokerage candidate requires revenue and PF risk confirmation."),
    Round26CaseCandidate("securities_pf_loss_4c", "SECURITIES_BROKERAGE_CYCLE", "BROKER_PF_4C", "증권사_PF손실", "KR", "4c_thesis_break", ("brokerage_balance_sheet",), ("pf_loss", "capital_ratio_down"), "PF loss can override trading-value recovery."),
)


def target_for(target_id: str) -> Round26ScoreTarget | None:
    for target in ROUND26_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round26_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND26_CASE_CANDIDATES:
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
                f"Round26 v1.1 calibration candidate for {candidate.target_id}; "
                "stage dates, prices, and numeric evidence remain unfilled."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=tuple(field for field in candidate.evidence_fields if field in target.green_conditions),
            stage3_evidence=(),
            stage4b_evidence=candidate.evidence_fields if candidate.case_type == "4b_watch" else (),
            stage4c_evidence=candidate.red_flag_fields if candidate.case_type == "4c_thesis_break" else (),
            must_have_fields=target.green_conditions,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason="; ".join(candidate.red_flag_fields) if candidate.case_type not in {"success_candidate", "structural_success"} else None,
            score_price_alignment="unknown",
            rerating_result="event_premium" if candidate.case_type == "event_premium" else "unknown",
            price_pattern="unknown",
            score_weight_hint={
                "eps_fcf": float(weights["eps_fcf"]),
                "visibility": float(weights["structural_visibility"]),
                "bottleneck": float(weights["bottleneck_pricing"]),
                "mispricing": float(weights["market_mispricing"]),
                "valuation": float(weights["valuation"]),
                "capital_allocation": float(weights["capital_allocation"]),
                "information_confidence": float(weights["information_confidence"]),
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


def round26_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND26_SCORE_TARGETS:
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
                "green_conditions": "|".join(target.green_conditions),
                "red_flags": "|".join(target.red_flags),
                "stage4b_conditions": "|".join(target.stage4b_conditions),
                "stage4c_conditions": "|".join(target.stage4c_conditions),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round26_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND26_CASE_CANDIDATES:
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


def round26_summary() -> dict[str, int | bool]:
    records = round26_case_records()
    positive = sum(1 for record in records if record.case_type in {"success_candidate", "structural_success"})
    stage4c = sum(1 for record in records if record.case_type == "4c_thesis_break")
    stage4b = sum(1 for record in records if record.case_type == "4b_watch")
    return {
        "target_count": len(ROUND26_SCORE_TARGETS),
        "case_candidate_count": len(records),
        "success_candidate_count": positive,
        "counterexample_or_risk_count": len(records) - positive,
        "stage4b_case_count": stage4b,
        "stage4c_case_count": stage4c,
        "green_possible_count": sum(1 for target in ROUND26_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND26_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round26_score_weight_reports(
    *,
    output_directory: str | Path = ROUND26_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND26_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND26_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round26_score_weight_v11_summary.md",
        "case_matrix": output / "round26_case_candidate_matrix.csv",
        "green_guardrails": output / "round26_green_guardrail_review.md",
        "stage4b_watch": output / "round26_stage4b_watch_review.md",
        "risk_boundary": output / "round26_risk_boundary_review.md",
        "price_validation_plan": output / "round26_price_validation_plan.md",
    }
    _write_case_jsonl(round26_case_records(), cases)
    _write_rows(round26_score_profile_rows(), score_profiles)
    _write_rows(round26_case_candidate_rows(), paths["case_matrix"])
    paths["summary"].write_text(render_round26_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round26_green_guardrail_markdown(), encoding="utf-8")
    paths["stage4b_watch"].write_text(render_round26_stage4b_watch_markdown(), encoding="utf-8")
    paths["risk_boundary"].write_text(render_round26_risk_boundary_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round26_price_validation_plan_markdown(), encoding="utf-8")
    return paths


def render_round26_summary_markdown() -> str:
    summary = round26_summary()
    lines = [
        "# Round-26 Score-Weight v1.1 Summary",
        "",
        f"- source_round: `{ROUND26_SOURCE_ROUND_PATH}`",
        f"- target_count: {summary['target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- counterexample_or_risk_count: {summary['counterexample_or_risk_count']}",
        f"- stage4b_case_count: {summary['stage4b_case_count']}",
        f"- stage4c_case_count: {summary['stage4c_case_count']}",
        f"- green_possible_count: {summary['green_possible_count']}",
        f"- watch_yellow_first_count: {summary['watch_yellow_first_count']}",
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "- Round 26 expands v1.1 calibration, not production scoring.",
        "- Example: K-beauty needs repeat sell-through, channel diversification, clean inventory, and ROE/OPM evidence.",
        "- Example: stablecoin/STO themes stay Watch until approval, issuance, volume, and fee economics are visible.",
        "- Example: construction and building materials remain Watch because PF and unsold inventory can dominate price hikes.",
        "- Theme names, case IDs, policies, PoCs, and revenue growth headlines are not score evidence by themselves.",
    ]
    return "\n".join(lines) + "\n"


def render_round26_green_guardrail_markdown() -> str:
    lines = [
        "# Round-26 Green Guardrail Review",
        "",
        "| target | posture | Green unlock evidence | Red flags |",
        "|---|---|---|---|",
    ]
    for target in ROUND26_SCORE_TARGETS:
        lines.append(
            "| "
            f"{target.target_id} | {target.posture.value} | "
            f"{', '.join(target.green_conditions)} | {', '.join(target.red_flags)} |"
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "- Do not apply v1.1 weights to production scoring yet.",
            "- Do not score policies, AI features, PoCs, revenue headlines, or theme labels without source-backed economics.",
            "- Do not invent stage dates, prices, margins, retention, FCF, reimbursement, issuance volume, or contract values.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round26_stage4b_watch_markdown() -> str:
    hbm = target_for("MEMORY_HBM_CAPACITY")
    cooling = target_for("AI_DATA_CENTER_COOLING")
    beauty = target_for("K_BEAUTY_EXPORT_DISTRIBUTION")
    lines = [
        "# Round-26 4B Watch Review",
        "",
        "Round 26 keeps Green strict while carrying 4B-watch into successful AI/HBM/K-beauty reratings.",
        "",
        "## MEMORY_HBM_CAPACITY",
    ]
    if hbm:
        lines.extend(f"- {item}" for item in hbm.stage4b_conditions)
    lines.append("")
    lines.append("## AI_DATA_CENTER_COOLING")
    if cooling:
        lines.extend(f"- {item}" for item in cooling.stage4b_conditions)
    lines.append("")
    lines.append("## K_BEAUTY_EXPORT_DISTRIBUTION")
    if beauty:
        lines.extend(f"- {item}" for item in beauty.stage4b_conditions)
    lines.extend(
        [
            "",
            "## Rule",
            "- Price-only warning remains `price_only_4b_watch`, not full evidence-based 4B.",
            "- Full 4B requires crowding, saturation, order slowdown, revision slowdown, capex reversal, channel stuffing, or other deterioration evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round26_risk_boundary_markdown() -> str:
    lines = [
        "# Round-26 Risk Boundary Review",
        "",
        "Round 26 separates Green-possible structures from Watch-first or 4C-heavy structures.",
        "",
        "## Green-Possible With Strict Gates",
    ]
    for target in ROUND26_SCORE_TARGETS:
        if target.posture == Round10ThemePosture.GREEN_POSSIBLE:
            lines.append(f"- {target.target_id}: {target.normalization_point}")
    lines.extend(["", "## Watch-First / 4C-Sensitive"])
    for target in ROUND26_SCORE_TARGETS:
        if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST:
            lines.append(f"- {target.target_id}: {', '.join(target.stage4c_conditions)}")
    lines.extend(
        [
            "",
            "## Rule",
            "- Stage 3-Green still requires cross-evidence and price-path validation.",
            "- Channel stuffing, stablecoin regulatory delay, renewable customs detention, PF delinquency, and AI CAPEX cuts are hard 4C-style examples.",
            "- 4B/4C cases are calibration examples, not production labels.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round26_price_validation_plan_markdown() -> str:
    return "\n".join(
        [
            "# Round-26 Price Validation Plan",
            "",
            "1. Backfill tradable case price paths where symbols exist.",
            "2. Keep policy, synthetic, and reference counterexamples as `needs_price_backfill` or `missing_price_data`.",
            "3. Calculate MFE/MAE, peak, drawdown, and below-entry flags only from source data.",
            "4. Run shadow score-price alignment before production scoring changes.",
            "",
            "## Priority Validation",
            "- K-beauty: export/channel evidence versus inventory, receivables, and channel stuffing.",
            "- Digital assets: approval, issuance, transaction volume, and fee economics versus theme-only rallies.",
            "- Construction/materials: price hikes and dividends versus PF, unsold inventory, liquidity, and rates.",
            "- HBM/AI cooling: structural EPS success versus crowding, capex delay, and price-only rerating.",
        ]
    ) + "\n"


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
    "ROUND26_CASE_CANDIDATES",
    "ROUND26_DEFAULT_CASES_PATH",
    "ROUND26_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND26_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND26_SCORE_TARGETS",
    "ROUND26_SOURCE_ROUND_PATH",
    "Round26CaseCandidate",
    "Round26ScoreTarget",
    "Round26ScoreWeightDraft",
    "render_round26_green_guardrail_markdown",
    "render_round26_price_validation_plan_markdown",
    "render_round26_risk_boundary_markdown",
    "render_round26_stage4b_watch_markdown",
    "render_round26_summary_markdown",
    "round26_case_candidate_rows",
    "round26_case_records",
    "round26_score_profile_rows",
    "round26_summary",
    "target_for",
    "write_round26_score_weight_reports",
]
