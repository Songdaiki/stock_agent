"""Round-36 cases_v18 expansion and score-weight validation v2.1.

Round 36 adds price-path validation plans to the calibration pack. It expands
grid transformer shortage, animal-health biosecurity, telehealth, precious
metals miners, kiosk/self-checkout, AI data-center optical networking, AI grid
flexibility software, and pharma-channel privacy risk. This module is
calibration/report material only. Production feature engineering, scoring,
staging, and RedTeam code must not import it.
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


ROUND36_SOURCE_ROUND_PATH = "docs/round/round_36.md"
ROUND36_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round36_score_weight_v21"
ROUND36_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_v18_round36.jsonl"
ROUND36_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round36_v21.csv"


@dataclass(frozen=True)
class Round36ScoreWeightDraft:
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
class Round36ScoreTarget:
    target_id: str
    large_sector: Round10LargeSector
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    validation_group: str
    score_weight: Round36ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    validation_metrics: tuple[str, ...]
    success_criteria: str
    failure_criteria: str
    normalization_point: str

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round36CaseCandidate:
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


ROUND36_SCORE_TARGETS: tuple[Round36ScoreTarget, ...] = (
    Round36ScoreTarget(
        "GRID_TRANSFORMER_SHORTAGE",
        Round10LargeSector.INDUSTRIAL_ORDERS_INFRA,
        E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,
        Round10ThemePosture.GREEN_POSSIBLE,
        "green_possible",
        Round36ScoreWeightDraft(22, 25, 23, 12, 12, 1, 5),
        ("transformer_shortage", "grid_expansion", "ai_datacenter_power", "lead_time_extended"),
        ("contract_to_sales", "multi_year_delivery", "backlog_growth", "op_eps_revision"),
        ("pricing_power", "capa_constraint", "fy1_fy2_fy3_revision", "old_frame_mispricing"),
        ("contract_to_sales", "multi_year_delivery", "backlog_growth", "pricing_power", "op_eps_revision"),
        ("capacity_normalization", "low_margin_contract", "project_delay", "raw_material"),
        ("datacenter_project_delay", "margin_compression", "order_cancel", "capa_normalization"),
        ("mfe_90d", "mfe_180d", "mfe_1y", "mfe_2y", "mae_90d", "op_eps_revision", "backlog_growth", "per_pbr_band"),
        "Stage 2/3 after order backlog and OP/EPS revisions should align with 6-24 month rerating.",
        "Theme rally without OP/EPS or margin follow-through becomes false_positive_score.",
        "Transformer shortage is a high-Green-potential axis only when contract quality, backlog, lead time, and revisions are source-backed.",
    ),
    Round36ScoreTarget(
        "ANIMAL_HEALTH_BIOSECURITY",
        Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE,
        E2RArchetype.ONE_OFF_EVENT_DEMAND,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        "cycle_event",
        Round36ScoreWeightDraft(16, 14, 8, 10, 8, 0, 5),
        ("animal_disease_event", "bird_flu", "asf", "conditional_vaccine_approval"),
        ("government_stockpile", "repeat_vaccination", "biosecurity_contract", "animal_health_sales_growth"),
        ("recurring_vaccine_revenue", "policy_use_clear", "event_normalization_risk_low"),
        ("government_stockpile", "repeat_vaccination", "biosecurity_contract", "animal_health_sales_growth"),
        ("disease_event_normalization", "policy_uncertainty", "one_off_demand", "disease_control"),
        ("disease_normalization", "stockpile_cancellation", "policy_nonuse", "sales_reversal"),
        ("mfe_30d", "mfe_90d", "post_event_drawdown", "next_year_revenue_retention", "inventory_oneoff_check"),
        "Recurring vaccine or biosecurity revenue after the event can support Watch-to-Green.",
        "Disease headline rally that normalizes with no recurring revenue is one_off_event.",
        "Animal health must separate recurring vaccines from one-off disease-event themes.",
    ),
    Round36ScoreTarget(
        "TELEHEALTH_BEHAVIORAL_HEALTH",
        Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE,
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        "watch_to_green",
        Round36ScoreWeightDraft(17, 16, 6, 12, 10, 0, 6),
        ("telehealth_adoption", "behavioral_health_platform", "dtc_healthcare", "online_therapy"),
        ("employer_or_insurance_contract", "repeat_usage", "cac_stable", "fcf_improvement"),
        ("b2b_b2b2c_recurring_revenue", "low_churn", "privacy_risk_controlled"),
        ("employer_or_insurance_contract", "repeat_usage", "cac_stable", "fcf_improvement"),
        ("cac", "privacy", "reimbursement", "churn", "impairment", "dtc_ad_dependency"),
        ("forecast_withdrawal", "privacy_settlement", "impairment", "cac_spike"),
        ("revenue_growth", "cac_to_revenue", "fcf_margin", "churn", "privacy_event_drawdown", "mfe_90d", "mae_1y"),
        "Revenue growth plus improving FCF and stable CAC can align.",
        "DTC growth with CAC, impairment, or privacy drawdown becomes false_positive_score.",
        "Telehealth needs B2B/B2B2C repeat revenue and privacy discipline, not DTC ad spend growth alone.",
    ),
    Round36ScoreTarget(
        "PRECIOUS_METALS_SAFE_HAVEN_MINERS",
        Round10LargeSector.MATERIALS_SPREAD_STRATEGIC,
        E2RArchetype.COMMODITY_SPREAD,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        "cycle_event",
        Round36ScoreWeightDraft(20, 10, 16, 9, 8, 5, 5),
        ("gold_price_breakout", "safe_haven_demand", "real_yield_down", "silver_price_breakout"),
        ("realized_price_up", "aisc_stable_or_down", "fcf_growth", "buyback_or_dividend"),
        ("production_stable", "jurisdiction_risk_low", "capital_return_visible"),
        ("realized_price_up", "aisc_stable_or_down", "fcf_growth", "buyback_or_dividend"),
        ("gold_price_reversal", "aisc", "jurisdiction", "production_decline", "price_theme_only"),
        ("commodity_peak_reversal", "aisc_spike", "mine_disruption", "political_risk"),
        ("gold_relative_return", "aisc_change", "fcf_yield", "capital_return", "drawdown_after_commodity_peak"),
        "Gold price, cost discipline, FCF, and capital return moving together can align as cyclical_success.",
        "Gold price headline without cost/production/FCF support becomes false_positive_score.",
        "Precious-metals miners are cycle-sensitive; Green is limited unless realized price and FCF are both visible.",
    ),
    Round36ScoreTarget(
        "SERVICE_KIOSK_SELF_CHECKOUT",
        Round10LargeSector.CONSUMER_RETAIL_BRAND,
        E2RArchetype.RETAIL_DOMESTIC_CONSUMER,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        "watch_to_green",
        Round36ScoreWeightDraft(17, 15, 7, 12, 10, 0, 5),
        ("kiosk_installation", "self_checkout", "retail_automation", "labor_cost_pressure"),
        ("installed_base_growth", "maintenance_recurring_revenue", "payment_fee_revenue", "loss_prevention_effect"),
        ("recurring_revenue_above_hardware", "gross_margin_improvement", "customer_recontract"),
        ("installed_base_growth", "maintenance_recurring_revenue", "payment_fee_revenue", "loss_prevention_effect"),
        ("theft", "customer_friction", "one_off_hardware", "maintenance_cost", "retailer_retreat", "pseudo_automation"),
        ("retailer_rollbacks", "theft_loss_spike", "customer_backlash", "hardware_sales_reversal"),
        ("hardware_vs_recurring_revenue", "gross_margin", "renewal_rate", "shrink_change", "mfe_180d", "mae_180d"),
        "Recurring maintenance, payment, or software economics can support Watch-to-Green.",
        "One-off hardware or retailer rollback after theft/customer friction is one_off_hardware.",
        "Kiosk/self-checkout must prove recurring economics and loss-prevention value.",
    ),
    Round36ScoreTarget(
        "OPTICAL_NETWORKING_AI_DATACENTER",
        Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS,
        E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE,
        Round10ThemePosture.GREEN_POSSIBLE,
        "green_possible",
        Round36ScoreWeightDraft(21, 22, 20, 13, 12, 0, 5),
        ("fiber_optic_cable", "optical_transceiver", "ai_datacenter_network", "hyperscaler_contract"),
        ("hyperscaler_long_contract", "direct_ai_datacenter_supply", "bottleneck_optical_component", "op_eps_revision"),
        ("multi_year_contract", "delivery_economics_visible", "customer_concentration_controlled"),
        ("hyperscaler_long_contract", "direct_ai_datacenter_supply", "bottleneck_optical_component", "op_eps_revision"),
        ("hyperscaler_concentration", "valuation_crowding", "capex_delay", "inventory", "unclear_ai_dc_exposure"),
        ("capex_delay", "hyperscaler_order_cut", "inventory_glut", "valuation_unwind"),
        ("mfe_90d", "mfe_180d", "mfe_1y", "op_eps_revision", "customer_concentration", "valuation_multiple", "drawdown_after_4b"),
        "Contract, OP/EPS revision, and rerating moving together are aligned.",
        "AI optical theme rally without order/EPS support is price_moved_without_evidence.",
        "Optical networking is Green-possible only when AI data-center contract and delivery economics are explicit.",
    ),
    Round36ScoreTarget(
        "AI_GRID_FLEXIBILITY_SOFTWARE",
        Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS,
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        "watch_to_green",
        Round36ScoreWeightDraft(17, 17, 15, 13, 10, 0, 6),
        ("ai_datacenter_grid_stress", "load_forecasting", "smart_grid_flexibility", "grid_interconnection"),
        ("utility_or_datacenter_customer", "commercial_pilot", "recurring_sw_revenue", "interconnection_savings"),
        ("customer_diversification", "arr_or_recurring_revenue", "opm_improvement"),
        ("utility_or_datacenter_customer", "recurring_sw_revenue", "interconnection_savings", "opm_improvement"),
        ("commercialization", "utility_adoption", "regulation", "proof_of_concept_only", "no_revenue"),
        ("utility_adoption_delay", "pilot_nonconversion", "regulatory_delay", "no_revenue"),
        ("contract_to_revenue", "arr_or_recurring_revenue", "opm_improvement", "theme_drawdown", "mfe_1y", "mae_1y"),
        "PoC converting into recurring contracts and revenue can support Watch-to-Green.",
        "Research or policy headline without revenue is theme_watch or false_positive.",
        "AI grid flexibility software is important but early; commercialization proof is the core gate.",
    ),
    Round36ScoreTarget(
        "PHARMA_CHANNEL_AND_PRIVACY_RISK",
        Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE,
        E2RArchetype.BIOTECH_PRE_REVENUE_REGULATORY,
        Round10ThemePosture.REDTEAM_FIRST,
        "red_flag",
        Round36ScoreWeightDraft(16, 15, 6, 12, 10, 0, 6),
        ("online_medical_platform", "telehealth_prescription", "online_pharmacy", "dtc_drug_platform"),
        ("b2b_b2b2c_contract", "low_cac", "privacy_compliance", "legal_distribution_channel"),
        ("recurring_usage", "fcf_improvement", "regulatory_quality_clear"),
        ("b2b_b2b2c_contract", "low_cac", "privacy_compliance", "legal_distribution_channel"),
        ("privacy", "advertising_cac", "fda_warning", "illegal_pharmacy", "liability", "impairment"),
        ("privacy_settlement", "ftc_or_fda_warning", "illegal_channel", "impairment", "cac_spike"),
        ("cac_to_revenue", "fcf_margin", "privacy_legal_drawdown", "churn", "mfe_1y", "mae_1y"),
        "B2B contracts, low CAC, privacy compliance, legal channels, and FCF can align.",
        "DTC growth followed by privacy/CAC/impairment is 4C-style failure.",
        "Online pharma channels remain RedTeam-first when privacy, advertising, quality, or regulatory risk is unresolved.",
    ),
)


ROUND36_CASE_CANDIDATES: tuple[Round36CaseCandidate, ...] = (
    Round36CaseCandidate("us_transformer_shortage_korea_import_success_candidate", "GRID_TRANSFORMER_SHORTAGE", "GRID_KR_IMPORT", "US transformer shortage Korea import success candidate", "KR", "success_candidate", ("transformer_shortage", "lead_time_extended", "pricing_power"), ("capacity_normalization", "project_delay"), "US transformer shortage can support Korean power-equipment suppliers when contracts and revisions appear."),
    Round36CaseCandidate("transformer_leadtime_price_increase_success_candidate", "GRID_TRANSFORMER_SHORTAGE", "TRANS_LEAD", "Transformer lead-time and price increase success candidate", "GLOBAL", "success_candidate", ("lead_time_extended", "backlog_growth", "op_eps_revision"), ("raw_material", "low_margin_contract"), "Long lead times and price increases need backlog and margin confirmation."),
    Round36CaseCandidate("low_margin_power_equipment_contract_counterexample", "GRID_TRANSFORMER_SHORTAGE", "GRID_LOWMARGIN", "Low-margin power equipment contract counterexample", "GLOBAL", "failed_rerating", ("contract_to_sales",), ("low_margin_contract", "margin_compression"), "Large power-equipment contract is weak if margin is low."),
    Round36CaseCandidate("datacenter_project_delay_transformer_4c", "GRID_TRANSFORMER_SHORTAGE", "GRID_DELAY_4C", "Datacenter project delay transformer 4C", "GLOBAL", "4c_thesis_break", ("ai_datacenter_power",), ("datacenter_project_delay", "order_cancel"), "Data-center project delay can break transformer order visibility."),
    Round36CaseCandidate("zoetis_bird_flu_vaccine_conditional_approval_candidate", "ANIMAL_HEALTH_BIOSECURITY", "ZTS_BIRD", "Zoetis bird-flu vaccine conditional approval candidate", "US", "success_candidate", ("conditional_vaccine_approval", "government_stockpile"), ("policy_uncertainty", "disease_normalization"), "Conditional vaccine approval is Stage 1-2, not Green without recurring use."),
    Round36CaseCandidate("hpai_poultry_event_oneoff_counterexample", "ANIMAL_HEALTH_BIOSECURITY", "HPAI_ONEOFF", "HPAI poultry event one-off counterexample", "GLOBAL", "one_off", ("animal_disease_event", "bird_flu"), ("disease_event_normalization", "disease_control"), "Disease events can normalize quickly and should not be extrapolated."),
    Round36CaseCandidate("animal_vaccine_stockpile_candidate", "ANIMAL_HEALTH_BIOSECURITY", "ANIMAL_STOCK", "Animal vaccine stockpile candidate", "GLOBAL", "success_candidate", ("government_stockpile", "repeat_vaccination"), ("policy_nonuse", "stockpile_cancellation"), "Government stockpile and repeat vaccination can support Watch-to-Green."),
    Round36CaseCandidate("disease_control_normalization_counterexample", "ANIMAL_HEALTH_BIOSECURITY", "DISEASE_NORM", "Disease control normalization counterexample", "GLOBAL", "failed_rerating", ("asf", "bird_flu"), ("disease_normalization", "sales_reversal"), "Disease control can erase event-driven demand."),
    Round36CaseCandidate("teladoc_betterhelp_cac_impairment_4c", "TELEHEALTH_BEHAVIORAL_HEALTH", "TDOC_BH_4C", "Teladoc BetterHelp CAC impairment 4C", "US", "4c_thesis_break", ("behavioral_health_platform", "dtc_healthcare"), ("impairment", "cac_spike"), "High CAC and impairment can break telehealth growth narratives."),
    Round36CaseCandidate("employer_insurance_telehealth_contract_candidate", "TELEHEALTH_BEHAVIORAL_HEALTH", "TEL_B2B", "Employer insurance telehealth contract candidate", "US", "success_candidate", ("employer_or_insurance_contract", "repeat_usage"), ("reimbursement", "churn"), "B2B/B2B2C telehealth contracts are stronger than DTC ads."),
    Round36CaseCandidate("betterhelp_privacy_ftc_counterexample", "TELEHEALTH_BEHAVIORAL_HEALTH", "BH_PRIV", "BetterHelp privacy FTC counterexample", "US", "failed_rerating", ("online_therapy",), ("privacy_settlement", "privacy"), "Sensitive-health privacy risk can cap platform valuation."),
    Round36CaseCandidate("telehealth_dtc_ad_cost_counterexample", "TELEHEALTH_BEHAVIORAL_HEALTH", "TEL_DTC_CAC", "Telehealth DTC ad cost counterexample", "US", "failed_rerating", ("dtc_healthcare",), ("dtc_ad_dependency", "cac"), "DTC ad spend can make revenue growth low quality."),
    Round36CaseCandidate("barrick_record_gold_price_profit_candidate", "PRECIOUS_METALS_SAFE_HAVEN_MINERS", "GOLD_BARRICK", "Barrick record gold price profit candidate", "US", "cyclical_success", ("realized_price_up", "aisc_stable_or_down", "fcf_growth", "buyback_or_dividend"), ("gold_price_reversal", "jurisdiction"), "Gold miner success needs realized price, cost control, FCF, and capital return."),
    Round36CaseCandidate("gold_price_correction_4b_watch", "PRECIOUS_METALS_SAFE_HAVEN_MINERS", "GOLD_4B", "Gold price correction 4B watch", "GLOBAL", "4b_watch", ("gold_price_breakout",), ("commodity_peak_reversal", "gold_price_reversal"), "Gold price peak can create 4B-watch before miner fundamentals break."),
    Round36CaseCandidate("miner_aisc_inflation_counterexample", "PRECIOUS_METALS_SAFE_HAVEN_MINERS", "AISC_INFL", "Miner AISC inflation counterexample", "GLOBAL", "failed_rerating", ("safe_haven_demand",), ("aisc_spike", "production_decline"), "Gold price benefit can disappear if AISC rises."),
    Round36CaseCandidate("jurisdiction_risk_gold_miner_4c", "PRECIOUS_METALS_SAFE_HAVEN_MINERS", "GOLD_JUR_4C", "Jurisdiction risk gold miner 4C", "GLOBAL", "4c_thesis_break", ("silver_price_breakout", "gold_price_breakout"), ("political_risk", "mine_disruption"), "Jurisdiction or mine disruption can break miner FCF path."),
    Round36CaseCandidate("kiosk_recurring_service_candidate", "SERVICE_KIOSK_SELF_CHECKOUT", "KIOSK_RECUR", "Kiosk recurring service candidate", "GLOBAL", "success_candidate", ("maintenance_recurring_revenue", "payment_fee_revenue"), ("customer_friction", "retailer_retreat"), "Kiosk recurring service is stronger than one-time hardware."),
    Round36CaseCandidate("target_dollar_general_self_checkout_theft_counterexample", "SERVICE_KIOSK_SELF_CHECKOUT", "SELF_THEFT", "Target Dollar General self-checkout theft counterexample", "US", "failed_rerating", ("self_checkout",), ("theft_loss_spike", "retailer_rollbacks"), "Retailer retreat after theft blocks automation Green."),
    Round36CaseCandidate("pseudo_automation_worker_burden_counterexample", "SERVICE_KIOSK_SELF_CHECKOUT", "PSEUDO_WORK", "Pseudo automation worker burden counterexample", "GLOBAL", "failed_rerating", ("retail_automation",), ("pseudo_automation", "customer_backlash"), "Automation that shifts workload without margin benefit is weak evidence."),
    Round36CaseCandidate("one_off_kiosk_hardware_sales_counterexample", "SERVICE_KIOSK_SELF_CHECKOUT", "KIOSK_HW_ONE", "One-off kiosk hardware sales counterexample", "GLOBAL", "failed_rerating", ("kiosk_installation",), ("one_off_hardware", "hardware_sales_reversal"), "One-off kiosk sales should not be treated as recurring visibility."),
    Round36CaseCandidate("meta_corning_fiber_contract_success_candidate", "OPTICAL_NETWORKING_AI_DATACENTER", "GLW_META_R36", "Meta Corning fiber contract success candidate", "US", "success_candidate", ("hyperscaler_long_contract", "direct_ai_datacenter_supply", "bottleneck_optical_component"), ("hyperscaler_concentration", "valuation_crowding"), "AI data-center optical contract can become a Green-eligible bottleneck case."),
    Round36CaseCandidate("optical_networking_valuation_crowding_4b", "OPTICAL_NETWORKING_AI_DATACENTER", "OPTICAL_CROWD_4B", "Optical networking valuation crowding 4B", "US", "4b_watch", ("ai_datacenter_network",), ("valuation_crowding", "valuation_unwind"), "Optical demand can still become 4B-watch if price outruns revisions."),
    Round36CaseCandidate("optical_customer_concentration_counterexample", "OPTICAL_NETWORKING_AI_DATACENTER", "OPTICAL_CONC", "Optical customer concentration counterexample", "GLOBAL", "failed_rerating", ("fiber_optic_cable",), ("hyperscaler_concentration", "hyperscaler_order_cut"), "Customer concentration can cap optical visibility."),
    Round36CaseCandidate("ai_datacenter_capex_delay_optical_4c", "OPTICAL_NETWORKING_AI_DATACENTER", "OPTICAL_CAPEX_4C", "AI datacenter capex delay optical 4C", "GLOBAL", "4c_thesis_break", ("optical_transceiver",), ("capex_delay", "inventory_glut"), "AI data-center capex delay can break optical component demand."),
    Round36CaseCandidate("ai_datacenter_load_forecasting_candidate", "AI_GRID_FLEXIBILITY_SOFTWARE", "AIGRID_LOAD", "AI datacenter load forecasting candidate", "GLOBAL", "success_candidate", ("load_forecasting", "ai_datacenter_grid_stress"), ("proof_of_concept_only", "no_revenue"), "Load forecasting is useful only if it converts into customer revenue."),
    Round36CaseCandidate("grid_flexible_datacenter_candidate", "AI_GRID_FLEXIBILITY_SOFTWARE", "AIGRID_FLEX", "Grid flexible datacenter candidate", "GLOBAL", "success_candidate", ("utility_or_datacenter_customer", "interconnection_savings"), ("utility_adoption_delay", "regulation"), "Flexible data centers need utility/customer adoption and recurring software revenue."),
    Round36CaseCandidate("smart_grid_poc_no_revenue_counterexample", "AI_GRID_FLEXIBILITY_SOFTWARE", "GRID_POC", "Smart-grid PoC no revenue counterexample", "GLOBAL", "failed_rerating", ("smart_grid_flexibility",), ("proof_of_concept_only", "no_revenue"), "PoC or research headline should not become score evidence."),
    Round36CaseCandidate("utility_adoption_delay_4c", "AI_GRID_FLEXIBILITY_SOFTWARE", "UTILITY_DELAY_4C", "Utility adoption delay 4C", "GLOBAL", "4c_thesis_break", ("grid_interconnection",), ("utility_adoption_delay", "pilot_nonconversion"), "Utility adoption delay can break software commercialization."),
    Round36CaseCandidate("betterhelp_privacy_ftc_4c", "PHARMA_CHANNEL_AND_PRIVACY_RISK", "BH_PRIV_4C", "BetterHelp privacy FTC 4C", "US", "4c_thesis_break", ("online_medical_platform",), ("privacy_settlement", "ftc_or_fda_warning"), "Sensitive-health privacy settlement is 4C-style platform risk."),
    Round36CaseCandidate("teladoc_betterhelp_impairment_4c", "PHARMA_CHANNEL_AND_PRIVACY_RISK", "TDOC_IMPAIR_4C", "Teladoc BetterHelp impairment 4C", "US", "4c_thesis_break", ("dtc_drug_platform",), ("impairment", "cac_spike"), "Impairment and CAC pressure can break online-health thesis."),
    Round36CaseCandidate("legal_telehealth_b2b_contract_candidate", "PHARMA_CHANNEL_AND_PRIVACY_RISK", "LEGAL_TEL_B2B", "Legal telehealth B2B contract candidate", "US", "success_candidate", ("b2b_b2b2c_contract", "privacy_compliance"), ("liability", "advertising_cac"), "Legal B2B telehealth can be monitored when privacy and CAC are controlled."),
    Round36CaseCandidate("online_pharma_cac_privacy_counterexample", "PHARMA_CHANNEL_AND_PRIVACY_RISK", "ONLINE_CAC_PRIV", "Online pharma CAC privacy counterexample", "GLOBAL", "failed_rerating", ("online_pharmacy",), ("advertising_cac", "privacy", "illegal_channel"), "DTC pharma channel with CAC/privacy risk remains RedTeam-first."),
)


def target_for(target_id: str) -> Round36ScoreTarget | None:
    for target in ROUND36_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round36_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND36_CASE_CANDIDATES:
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
                f"Round36 v2.1 calibration candidate for {candidate.target_id}; "
                "stage dates, prices, and numeric evidence remain unfilled."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=tuple(field for field in candidate.evidence_fields if field in target.green_conditions),
            stage3_evidence=(),
            stage4b_evidence=candidate.red_flag_fields if candidate.case_type == "4b_watch" else (),
            stage4c_evidence=candidate.red_flag_fields if candidate.case_type == "4c_thesis_break" else (),
            must_have_fields=target.green_conditions,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason="; ".join(candidate.red_flag_fields) if candidate.case_type not in {"success_candidate", "structural_success", "cyclical_success"} else None,
            score_price_alignment="unknown",
            rerating_result="cyclical_rerating" if candidate.case_type == "cyclical_success" else ("thesis_break" if candidate.case_type == "4c_thesis_break" else "unknown"),
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
                "theme_label_is_not_score_evidence",
                "do_not_invent_stage_dates_or_prices",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Validation group: {target.validation_group}.",
            price_validation=PriceValidation(price_validation_status="needs_price_backfill"),
            data_quality=CaseDataQuality(False, False, False, 0.0),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round36_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND36_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "validation_group": target.validation_group,
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
                "stage4c_conditions": "|".join(target.stage4c_conditions),
                "validation_metrics": "|".join(target.validation_metrics),
                "success_criteria": target.success_criteria,
                "failure_criteria": target.failure_criteria,
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round36_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND36_CASE_CANDIDATES:
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
                "validation_group": target.validation_group,
                "evidence_fields": "|".join(candidate.evidence_fields),
                "red_flag_fields": "|".join(candidate.red_flag_fields),
                "price_validation_status": "needs_price_backfill",
                "production_input": "false",
                "notes": candidate.notes,
            }
        )
    return tuple(rows)


def round36_summary() -> dict[str, int | bool]:
    records = round36_case_records()
    positive = sum(1 for record in records if record.case_type in {"success_candidate", "structural_success", "cyclical_success"})
    stage4c = sum(1 for record in records if record.case_type == "4c_thesis_break")
    stage4b = sum(1 for record in records if record.case_type == "4b_watch")
    return {
        "target_count": len(ROUND36_SCORE_TARGETS),
        "case_candidate_count": len(records),
        "success_candidate_count": positive,
        "counterexample_or_risk_count": len(records) - positive,
        "stage4b_case_count": stage4b,
        "stage4c_case_count": stage4c,
        "green_possible_count": sum(1 for target in ROUND36_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND36_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND36_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round36_score_weight_reports(
    *,
    output_directory: str | Path = ROUND36_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND36_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND36_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round36_score_weight_v21_summary.md",
        "case_matrix": output / "round36_case_candidate_matrix.csv",
        "green_guardrails": output / "round36_green_guardrail_review.md",
        "validation_plan": output / "round36_archetype_price_validation_plan.md",
        "grid_optical_power": output / "round36_grid_optical_power_review.md",
        "healthcare_event_risk": output / "round36_healthcare_event_risk_review.md",
        "cycle_service_review": output / "round36_cycle_service_review.md",
    }
    _write_case_jsonl(round36_case_records(), cases)
    _write_rows(round36_score_profile_rows(), score_profiles)
    _write_rows(round36_case_candidate_rows(), paths["case_matrix"])
    paths["summary"].write_text(render_round36_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round36_green_guardrail_markdown(), encoding="utf-8")
    paths["validation_plan"].write_text(render_round36_validation_plan_markdown(), encoding="utf-8")
    paths["grid_optical_power"].write_text(render_round36_grid_optical_power_markdown(), encoding="utf-8")
    paths["healthcare_event_risk"].write_text(render_round36_healthcare_event_risk_markdown(), encoding="utf-8")
    paths["cycle_service_review"].write_text(render_round36_cycle_service_markdown(), encoding="utf-8")
    return paths


def render_round36_summary_markdown() -> str:
    summary = round36_summary()
    lines = [
        "# Round-36 Score-Weight Validation v2.1 Summary",
        "",
        f"- source_round: `{ROUND36_SOURCE_ROUND_PATH}`",
        f"- target_count: {summary['target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- counterexample_or_risk_count: {summary['counterexample_or_risk_count']}",
        f"- stage4b_case_count: {summary['stage4b_case_count']}",
        f"- stage4c_case_count: {summary['stage4c_case_count']}",
        f"- green_possible_count: {summary['green_possible_count']}",
        f"- watch_yellow_first_count: {summary['watch_yellow_first_count']}",
        f"- redteam_first_count: {summary['redteam_first_count']}",
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "- Round 36 adds cases_v18 and explicit price-path validation plans.",
        "- Example: transformer shortage can be Green-possible only when backlog, lead time, pricing, and OP/EPS revisions line up.",
        "- Example: animal-health disease headlines are usually event/cycle evidence unless government stockpile or repeat vaccination revenue is visible.",
        "- Example: telehealth and pharma-channel growth can fail through CAC, privacy, advertising, or impairment.",
        "- Theme names, case IDs, policy headlines, PoCs, and price rallies are not score evidence by themselves.",
    ]
    return "\n".join(lines) + "\n"


def render_round36_green_guardrail_markdown() -> str:
    lines = [
        "# Round-36 Green Guardrail Review",
        "",
        "| target | posture | validation_group | Green unlock evidence | Red flags |",
        "|---|---|---|---|---|",
    ]
    for target in ROUND36_SCORE_TARGETS:
        lines.append(
            "| "
            f"{target.target_id} | {target.posture.value} | {target.validation_group} | "
            f"{', '.join(target.green_conditions)} | {', '.join(target.red_flags)} |"
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "- Do not apply v2.1 weights to production scoring yet.",
            "- Do not use case IDs, theme labels, disease headlines, PoCs, or commodity prices as candidate-generation input.",
            "- Do not invent stage dates, prices, contract terms, vaccine stockpile, CAC, AISC, recurring revenue, hyperscaler terms, ARR, or privacy status.",
            "- Do not lower Stage 3-Green thresholds to improve recall.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round36_validation_plan_markdown() -> str:
    lines = [
        "# Round-36 Archetype Price Validation Plan",
        "",
        "Round 36 separates validation by archetype behavior rather than by theme name.",
        "",
        "| target | validation_group | metrics | success | failure |",
        "|---|---|---|---|---|",
    ]
    for target in ROUND36_SCORE_TARGETS:
        lines.append(
            "| "
            f"{target.target_id} | {target.validation_group} | {', '.join(target.validation_metrics)} | "
            f"{target.success_criteria} | {target.failure_criteria} |"
        )
    lines.extend(
        [
            "",
            "## Group Rules",
            "- green_possible: compare Stage 2/3 dates with MFE/MAE, revision persistence, and valuation-band changes.",
            "- watch_to_green: require recurring revenue, margin/FCF improvement, and customer retention before Green-like interpretation.",
            "- cycle_event: report cyclical_success separately from structural_success and track drawdown after peak.",
            "- red_flag: treat privacy, regulation, CAC, and legal events as thesis-break candidates before promotion.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round36_grid_optical_power_markdown() -> str:
    return "\n".join(
        [
            "# Round-36 Grid / Optical / AI Power Review",
            "",
            "Power-grid and AI-networking cases can be Green-possible, but only with source-backed revenue visibility.",
            "",
            "## Grid Transformer Shortage",
            "- Needs contract-to-sales, multi-year delivery, backlog growth, pricing power, and OP/EPS revision.",
            "- Low-margin contract or data-center project delay blocks Green.",
            "",
            "## Optical AI Data Center",
            "- Needs hyperscaler contract, direct AI data-center supply, bottleneck component evidence, and OP/EPS revision.",
            "- Customer concentration and valuation crowding trigger 4B/RedTeam checks.",
            "",
            "## AI Grid Flexibility Software",
            "- Starts as Watch-to-Green.",
            "- PoC must convert into utility/data-center contracts and recurring software revenue.",
        ]
    ) + "\n"


def render_round36_healthcare_event_risk_markdown() -> str:
    return "\n".join(
        [
            "# Round-36 Healthcare / Event Risk Review",
            "",
            "Healthcare access and disease events need stronger RedTeam separation.",
            "",
            "## Animal Health",
            "- Disease headline alone is one-off event evidence.",
            "- Government stockpile, repeat vaccination, or biosecurity contracts can lift it into Watch-to-Green.",
            "",
            "## Telehealth / Pharma Channel",
            "- B2B/B2B2C contracts, low CAC, repeat usage, privacy compliance, and FCF can support higher stages.",
            "- DTC ad spend, impairment, FTC/FDA warnings, privacy settlement, illegal pharmacy, and CAC spikes are 4C-style risks.",
        ]
    ) + "\n"


def render_round36_cycle_service_markdown() -> str:
    return "\n".join(
        [
            "# Round-36 Cycle / Service Automation Review",
            "",
            "Round 36 keeps commodity and service-automation stories from masquerading as structural E2R.",
            "",
            "## Precious Metals Miners",
            "- Gold/silver price alone is not enough.",
            "- Realized price, AISC, production, FCF, and capital return must move together.",
            "- Treat most successful cases as cyclical_success unless structural evidence is unusually strong.",
            "",
            "## Kiosk / Self-Checkout",
            "- One-time hardware sales are weak evidence.",
            "- Recurring maintenance, payment/software revenue, loss prevention, and renewal rates are the key checks.",
            "- Theft, customer friction, retailer retreat, and pseudo-automation cap Green.",
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
    "ROUND36_CASE_CANDIDATES",
    "ROUND36_DEFAULT_CASES_PATH",
    "ROUND36_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND36_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND36_SCORE_TARGETS",
    "ROUND36_SOURCE_ROUND_PATH",
    "Round36CaseCandidate",
    "Round36ScoreTarget",
    "Round36ScoreWeightDraft",
    "render_round36_cycle_service_markdown",
    "render_round36_green_guardrail_markdown",
    "render_round36_grid_optical_power_markdown",
    "render_round36_healthcare_event_risk_markdown",
    "render_round36_summary_markdown",
    "render_round36_validation_plan_markdown",
    "round36_case_candidate_rows",
    "round36_case_records",
    "round36_score_profile_rows",
    "round36_summary",
    "target_for",
    "write_round36_score_weight_reports",
]
