"""Round-43 R3 battery/EV/green-energy calibration pack.

Round 43 expands the Round-40 protocol for R3 battery, EV, and green-energy
themes. It stores target sub-archetypes, shadow score-weight drafts,
stage-date guidance, case candidates, and price-validation fields.

This module is calibration/report material only. Production feature
engineering, scoring, staging, and RedTeam code must not import it.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import CaseDataQuality, E2RCaseRecord, PriceValidation
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture


ROUND43_SOURCE_ROUND_PATH = "docs/round/round_43.md"
ROUND43_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round43_r3_battery_ev_green"
ROUND43_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r3_round43.jsonl"
ROUND43_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round43_r3_v1.csv"


@dataclass(frozen=True)
class Round43ScoreWeightDraft:
    eps_fcf: int
    structural_visibility: int
    bottleneck_pricing: int
    market_mispricing: int
    valuation: int
    capital_allocation: int
    information_confidence: int

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
class Round43ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round43ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    normalization_point: str
    gate_only: bool = False

    @property
    def large_sector(self) -> Round10LargeSector:
        return Round10LargeSector.BATTERY_EV_GREEN

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round43CaseCandidate:
    case_id: str
    target_id: str
    symbol: str
    company_name: str
    market: str
    case_type: str
    stage1_date: date | None
    stage2_date: date | None
    stage3_date: date | None
    stage4b_date: date | None
    stage4c_date: date | None
    evidence_fields: tuple[str, ...]
    red_flag_fields: tuple[str, ...]
    alignment_hint: str
    price_validation_status: str
    source_refs: tuple[str, ...]
    notes: str
    secondary_archetypes: tuple[E2RArchetype, ...] = ()

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND43_SCORE_TARGETS: tuple[Round43ScoreTarget, ...] = (
    Round43ScoreTarget(
        "BATTERY_MATERIALS_CAPEX_OVERHEAT",
        E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT,
        Round10ThemePosture.REDTEAM_FIRST,
        Round43ScoreWeightDraft(20, 16, 14, 10, 10, 0, 5),
        ("ev_growth_narrative", "long_term_supply_contract", "capa_expansion_news"),
        ("real_contract", "price_margin_improvement", "op_eps_revision"),
        ("long_term_contract", "price_pass_through", "fcf_after_capex", "demand_visibility"),
        ("per_pbr_overheat", "capa_race", "target_price_crowding"),
        ("ev_demand_slowdown", "raw_material_price_drop", "capa_overbuild", "customer_line_idle"),
        ("contract_quality", "price_pass_through", "fcf_after_capex", "demand_visibility"),
        ("ev_demand_slowdown", "capa_overbuild", "lithium_price_crash", "customer_capex_cut"),
        "Battery materials stay RedTeam-first because CAPEX and mineral cycles can reverse the story quickly.",
    ),
    Round43ScoreTarget(
        "BATTERY_EQUIPMENT_PARTS",
        E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round43ScoreWeightDraft(19, 17, 12, 12, 10, 0, 5),
        ("battery_equipment_order", "cell_customer_capex", "delivery_schedule_keyword"),
        ("customer_order", "delivery_schedule", "margin_visibility"),
        ("order_to_revenue_conversion", "customer_diversification", "op_eps_revision"),
        ("equipment_capex_cycle_crowded", "cell_capex_peak"),
        ("customer_capex_cut", "delivery_delay", "margin_miss"),
        ("customer_order", "delivery_schedule", "margin_visibility", "op_eps_revision"),
        ("customer_capex_cut", "delivery_delay", "single_customer"),
        "Battery equipment can become Watch-to-Green only when customer CAPEX converts to revenue and margin.",
    ),
    Round43ScoreTarget(
        "BATTERY_RECYCLING_ESS_SHIFT",
        E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round43ScoreWeightDraft(20, 16, 14, 10, 10, 0, 5),
        ("ess_shift", "battery_recycling", "lfp_ess_production", "solid_state_battery_keyword"),
        ("ess_customer_contract", "capacity_utilization", "recycling_volume", "metal_recovery_revenue"),
        ("recurring_ess_or_recycling_fcf", "margin_visible", "ev_slowdown_offset"),
        ("ess_narrative_crowded", "recycling_premium_overheat"),
        ("recycling_volume_shortfall", "metal_price_drop", "utilization_drop", "ev_demand_slowdown"),
        ("ess_contract", "capacity_utilization", "recycling_volume", "fcf_margin"),
        ("recycling_volume_shortfall", "ev_demand_slowdown", "metal_price_drop", "utilization_drop"),
        "ESS shift is a separate Watch path, but it cannot erase EV slowdown risk without contracts and utilization.",
    ),
    Round43ScoreTarget(
        "EV_INFRASTRUCTURE",
        E2RArchetype.AUTO_MOBILITY_COMPONENTS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round43ScoreWeightDraft(17, 14, 7, 11, 9, 0, 5),
        ("charging_station", "charger_installation", "ev_infrastructure_policy"),
        ("utilization", "recurring_revenue", "subsidy_visibility"),
        ("profitable_utilization", "repeat_revenue", "subsidy_independent_margin"),
        ("ev_charging_theme_crowded",),
        ("low_utilization", "subsidy_cut", "fire_regulation", "maintenance_cost"),
        ("utilization", "recurring_revenue", "profitability"),
        ("low_utilization", "subsidy_dependency", "fire_regulation"),
        "EV charging needs utilization and unit economics, not installation count alone.",
    ),
    Round43ScoreTarget(
        "HYDROGEN_FUEL_CELL_INFRA",
        E2RArchetype.UTILITIES_REGULATED_TARIFF,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round43ScoreWeightDraft(18, 18, 12, 12, 10, 0, 5),
        ("hydrogen_fuel_cell_factory", "hydrogen_policy", "electrolyzer_or_commercial_vehicle"),
        ("customer_or_demand_source", "production_capacity", "delivery_contract"),
        ("utilization", "op_eps_conversion", "subsidy_independent_economics"),
        ("hydrogen_theme_overheat",),
        ("subsidy_cut", "customer_absent", "low_utilization", "project_delay"),
        ("customer_demand", "production_capacity", "utilization", "op_eps_conversion"),
        ("subsidy_dependency", "customer_absent", "low_utilization"),
        "Hydrogen is Watch-to-Green only when CAPEX has customers, utilization, and operating-profit conversion.",
    ),
    Round43ScoreTarget(
        "SOLAR_TARIFF_SUPPLYCHAIN",
        E2RArchetype.UTILITIES_REGULATED_TARIFF,
        Round10ThemePosture.REDTEAM_FIRST,
        Round43ScoreWeightDraft(18, 17, 12, 12, 10, 0, 5),
        ("solar_factory", "subsidy_policy", "module_or_cell_demand"),
        ("utilization", "customer_contract", "supply_chain_stable", "op_turnaround"),
        ("subsidy_independent_fcf", "supply_chain_clean", "margin_visible"),
        ("solar_manufacturing_narrative_crowded", "subsidy_premium"),
        ("tariff_risk", "customs_detention", "uflpa_detention", "subsidy_cut", "worker_furlough"),
        ("utilization", "customer_contract", "supply_chain_stable", "fcf_margin"),
        ("tariff_risk", "customs_detention", "uflpa_detention", "subsidy_dependency"),
        "Solar is RedTeam-first because policy benefit and policy/supply-chain break can arrive together.",
    ),
    Round43ScoreTarget(
        "RENEWABLE_ENERGY_POLICY",
        E2RArchetype.UTILITIES_REGULATED_TARIFF,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round43ScoreWeightDraft(18, 16, 10, 11, 9, 0, 5),
        ("wind_or_renewable_project", "carbon_policy", "renewable_power_policy"),
        ("permitted_project", "funding_visible", "cost_schedule_visible"),
        ("project_economics", "op_eps_conversion", "cost_controlled"),
        ("renewable_policy_crowded", "project_premium"),
        ("permitting_delay", "financing_cost", "cost_overrun", "project_delay", "impairment"),
        ("permitting", "funding", "cost_schedule", "margin_visibility"),
        ("permitting_delay", "financing_cost", "cost_overrun", "impairment"),
        "Renewable policy remains Watch until project economics survive rates, permits, and cost pressure.",
    ),
    Round43ScoreTarget(
        "ENERGY_DISTRIBUTION_FUEL",
        E2RArchetype.COMMODITY_SPREAD,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round43ScoreWeightDraft(18, 15, 16, 10, 10, 2, 5),
        ("lng_or_lpg_distribution", "fuel_spread", "energy_price_move"),
        ("spread_improvement", "inventory_status", "demand_visibility"),
        ("repeat_spread_margin", "fcf_defense", "capital_allocation_disciplined"),
        ("fuel_spread_crowded",),
        ("energy_price_reversal", "inventory_loss", "tariff_or_policy_shock"),
        ("spread_improvement", "inventory_status", "fcf_margin"),
        ("price_reversal", "inventory_loss", "policy_shock"),
        "Energy distribution is spread/cycle driven and should carry cycle caps.",
    ),
    Round43ScoreTarget(
        "WASTE_RECYCLING_ENVIRONMENT",
        E2RArchetype.UTILITIES_REGULATED_TARIFF,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round43ScoreWeightDraft(18, 22, 15, 13, 12, 3, 5),
        ("waste_treatment_platform", "recycling_demand", "permit_value", "waste_to_energy"),
        ("treatment_volume", "long_term_contract", "utilization", "fcf_visible"),
        ("permit_asset", "recurring_fcf", "valuation_frame_change", "mna_value_support"),
        ("waste_mna_premium_crowded", "permit_value_fully_priced"),
        ("utilization_drop", "capex_burden", "metal_price_drop", "regulatory_cost"),
        ("permit_asset", "treatment_volume", "utilization", "recurring_fcf"),
        ("utilization_drop", "capex_burden", "commodity_recycling_price_drop"),
        "Waste treatment is one of the few R3 Green-capable areas when permits and recurring FCF are proven.",
    ),
    Round43ScoreTarget(
        "CARBON_CREDIT_CBAM_COMPLIANCE",
        E2RArchetype.UTILITIES_REGULATED_TARIFF,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round43ScoreWeightDraft(14, 17, 10, 12, 8, 2, 6),
        ("eu_ets_or_cbam_policy", "carbon_accounting", "compliance_monitoring"),
        ("carbon_accounting_revenue", "verification_revenue", "low_carbon_product_premium"),
        ("recurring_compliance_revenue", "cost_pass_through", "industrial_customer_base"),
        ("carbon_price_theme_crowded",),
        ("carbon_price_drop", "free_allowance_expansion", "greenwashing_risk", "policy_delay"),
        ("recurring_revenue", "verification_customer", "cost_pass_through"),
        ("carbon_price_volatility", "greenwashing", "policy_reversal"),
        "Carbon credits alone are Watch; compliance software/service revenue is the stronger route.",
    ),
    Round43ScoreTarget(
        "DATA_CENTER_WATER_REUSE_INFRA",
        E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round43ScoreWeightDraft(16, 18, 14, 12, 10, 2, 5),
        ("ai_datacenter_water_use", "water_reuse", "closed_loop_cooling", "water_treatment"),
        ("data_center_customer", "reuse_project", "contracted_revenue"),
        ("repeat_water_reuse_revenue", "margin_visible", "local_permit_support"),
        ("water_reuse_theme_crowded",),
        ("customer_absent", "local_opposition", "unit_economics_weak"),
        ("data_center_customer", "contracted_revenue", "unit_economics"),
        ("customer_absent", "local_opposition", "weak_economics"),
        "Data-center water reuse is Watch-to-Green only with named customers and economics.",
    ),
    Round43ScoreTarget(
        "EV_FIRE_RISK_OVERLAY",
        E2RArchetype.THEME_VALUATION_OVERHEAT,
        Round10ThemePosture.REDTEAM_FIRST,
        Round43ScoreWeightDraft(0, 0, 0, 0, 0, 0, 0),
        ("ev_fire", "battery_recall", "insurance_cost", "regulatory_investigation"),
        ("risk_event_detected",),
        ("not_applicable_gate_only",),
        ("not_applicable_gate_only",),
        ("recall", "fire_regulation", "insurance_cost_spike", "plant_shutdown", "customer_loss"),
        (),
        ("recall", "fire_regulation", "insurance_cost", "plant_shutdown", "customer_loss"),
        "EV fire/recall/regulation overlay is a RedTeam gate, not a positive scoring bucket.",
        gate_only=True,
    ),
)


ROUND43_CASE_CANDIDATES: tuple[Round43CaseCandidate, ...] = (
    Round43CaseCandidate(
        "lg_energy_solution_ess_shift_case",
        "BATTERY_RECYCLING_ESS_SHIFT",
        "373220",
        "LG에너지솔루션 ESS 전환",
        "KR",
        "success_candidate",
        None,
        date(2025, 7, 25),
        None,
        None,
        None,
        ("ess_shift", "lfp_ess_capacity_expansion", "q2_op_profit", "ev_slowdown_offset_candidate"),
        ("ev_demand_slowdown", "tariff_policy_risk", "event_day_price_decline"),
        "evidence_good_but_price_failed_or_delayed",
        "needs_price_backfill",
        ("Reuters LG Energy Solution ESS shift",),
        "ESS shift is positive, but the market initially focused on EV demand and policy risk.",
    ),
    Round43CaseCandidate(
        "gm_lg_ultium_ohio_ev_slowdown_case",
        "BATTERY_MATERIALS_CAPEX_OVERHEAT",
        "GM_LG_ULTIUM_REF",
        "GM-LG Ultium Ohio EV slowdown",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2026, 5, 12),
        ("ev_battery_capa", "plant_restart_uncertain", "ess_shift_candidate"),
        ("ev_demand_slowdown", "plant_idle", "layoff", "capacity_underutilization"),
        "ev_demand_4c_plus_ess_watch",
        "needs_price_backfill",
        ("Reuters GM-LG Ohio battery plant",),
        "EV CAPA expansion thesis breaks when plant restart and utilization become uncertain.",
    ),
    Round43CaseCandidate(
        "hyundai_hydrogen_fuel_cell_plant_case",
        "HYDROGEN_FUEL_CELL_INFRA",
        "005380",
        "현대차 수소연료전지 울산 공장",
        "KR",
        "success_candidate",
        None,
        date(2025, 10, 30),
        None,
        None,
        None,
        ("hydrogen_fuel_cell_factory", "capex_amount", "production_capacity", "electrolyzer_plan"),
        ("customer_absent", "subsidy_dependency", "low_utilization"),
        "stage1_to_stage2_success_candidate",
        "needs_price_backfill",
        ("Reuters Hyundai hydrogen fuel-cell plant",),
        "Actual CAPEX is stronger than policy talk, but customer, utilization, and OP conversion are still required.",
    ),
    Round43CaseCandidate(
        "eqt_kj_environment_waste_platform_case",
        "WASTE_RECYCLING_ENVIRONMENT",
        "KJ_ENV_REF",
        "EQT-KJ Environment 폐기물 플랫폼",
        "KR",
        "structural_success",
        None,
        date(2024, 8, 16),
        None,
        None,
        None,
        ("waste_treatment_platform", "permit_asset", "recycling_operation", "waste_to_energy", "mna_value_support"),
        ("utilization_drop", "capex_burden"),
        "structural_success_reference",
        "missing_public_price_data",
        ("Reuters EQT KJ Environment platform",),
        "Waste treatment can be infrastructure-like when permits, treatment assets, and recurring FCF are visible.",
    ),
    Round43CaseCandidate(
        "eu_ets_cbam_policy_case",
        "CARBON_CREDIT_CBAM_COMPLIANCE",
        "EU_ETS_CBAM_REF",
        "EU ETS / CBAM compliance watch",
        "EU",
        "event_premium",
        None,
        date(2026, 5, 12),
        None,
        None,
        None,
        ("eu_ets_policy", "cbam_compliance", "carbon_accounting_demand"),
        ("policy_delay", "carbon_price_volatility", "greenwashing_risk"),
        "policy_structural_watch",
        "missing_direct_symbol_mapping",
        ("Reuters EU ETS revamp", "arXiv CBAM study"),
        "Policy matters, but Green needs recurring compliance revenue or low-carbon product premium.",
    ),
    Round43CaseCandidate(
        "qcells_customs_detention_case",
        "SOLAR_TARIFF_SUPPLYCHAIN",
        "QCELLS_REF",
        "Qcells 통관 억류",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2025, 11, 8),
        ("solar_us_factory", "subsidy_policy"),
        ("customs_detention", "uflpa_detention", "worker_furlough", "production_disruption"),
        "solar_supply_chain_4c",
        "missing_public_price_data",
        ("AP Qcells customs detention", "Reuters Qcells furloughs",),
        "Solar policy benefit can break through customs detention, forced-labor compliance, and production disruption.",
    ),
    Round43CaseCandidate(
        "qcells_china_linked_solar_policy_case",
        "SOLAR_TARIFF_SUPPLYCHAIN",
        "QCELLS_POLICY_REF",
        "중국계 태양광 규제 리스크",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2026, 5, 8),
        ("solar_factory", "us_solar_manufacturing_policy"),
        ("china_linked_policy_risk", "financing_stall", "customer_counterparty_risk"),
        "solar_policy_supply_chain_risk",
        "missing_public_price_data",
        ("Reuters China-linked solar policy risk",),
        "Solar policy support and ownership/supply-chain regulation can move in opposite directions.",
    ),
    Round43CaseCandidate(
        "orsted_sunrise_wind_impairment_case",
        "RENEWABLE_ENERGY_POLICY",
        "ORSTED.CO",
        "Ørsted Sunrise Wind impairment",
        "EU",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2025, 1, 20),
        ("offshore_wind_project", "renewable_policy"),
        ("impairment", "project_delay", "cost_overrun", "financing_cost"),
        "wind_project_4c",
        "needs_price_backfill",
        ("Reuters Orsted Sunrise Wind impairment",),
        "Renewable projects can break when rates, foundations, cost inflation, and schedule delays overwhelm policy support.",
    ),
    Round43CaseCandidate(
        "lithium_price_86pct_crash_case",
        "BATTERY_MATERIALS_CAPEX_OVERHEAT",
        "LITHIUM_CYCLE_REF",
        "리튬 가격 86% 급락",
        "GLOBAL",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2025, 1, 13),
        ("lithium_price_cycle", "mine_shutdown"),
        ("lithium_price_crash", "raw_material_price_drop", "mine_restart_cap", "revenue_drop"),
        "lithium_cycle_4c",
        "missing_price_data",
        ("Reuters lithium prices stabilize after crash",),
        "Lithium price rebounds are not structural unless cost curve, offtake, FCF, and CAPEX discipline are proven.",
    ),
    Round43CaseCandidate(
        "albemarle_cost_cut_low_lithium_case",
        "BATTERY_MATERIALS_CAPEX_OVERHEAT",
        "ALB",
        "Albemarle 저리튬 가격 비용절감",
        "US",
        "cyclical_success",
        None,
        date(2025, 2, 12),
        None,
        None,
        None,
        ("cost_cut", "quarterly_profit", "capex_cut", "low_lithium_price_survival"),
        ("lithium_price_drop", "revenue_drop", "capex_cut"),
        "cost_cut_survival_not_structural_green",
        "needs_price_backfill",
        ("Reuters Albemarle low lithium results",),
        "Cost cuts can stabilize results, but low lithium price survival is cyclical until durable FCF is proven.",
    ),
    Round43CaseCandidate(
        "battery_materials_capex_overheat_4b_watch",
        "BATTERY_MATERIALS_CAPEX_OVERHEAT",
        "BATTERY_MATERIALS_4B_REF",
        "2차전지 소재 CAPA 과열 4B-watch",
        "KR",
        "4b_watch",
        None,
        None,
        None,
        None,
        None,
        ("capa_expansion_news", "per_pbr_overheat", "target_price_crowding"),
        ("ev_demand_slowdown", "capa_overbuild", "raw_material_price_drop"),
        "battery_materials_4b_watch",
        "missing_price_data",
        ("Round43 battery materials 4B note",),
        "Battery material rallies need 4B-watch when CAPA and valuation move faster than contracts, utilization, and FCF.",
    ),
    Round43CaseCandidate(
        "battery_equipment_customer_capex_cut_counterexample",
        "BATTERY_EQUIPMENT_PARTS",
        "BATTERY_EQUIP_REF",
        "배터리 장비 고객사 CAPEX cut 반례",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("battery_equipment_order_story",),
        ("customer_capex_cut", "delivery_delay", "margin_miss", "single_customer"),
        "false_positive_score_risk",
        "missing_price_data",
        ("Round43 battery equipment capex warning",),
        "Equipment order stories fail when customer CAPEX is cut before delivery and margin conversion.",
    ),
    Round43CaseCandidate(
        "ev_fire_recall_regulation_overlay_case",
        "EV_FIRE_RISK_OVERLAY",
        "EV_FIRE_RISK_REF",
        "EV 화재·리콜·규제 overlay",
        "GLOBAL",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        None,
        ("ev_growth_narrative",),
        ("recall", "fire_regulation", "insurance_cost", "customer_loss"),
        "redteam_overlay_4c_watch",
        "missing_price_data",
        ("Round43 EV fire risk overlay",),
        "EV fire, recall, insurance, or regulation risk should block unsafe Green regardless of growth narrative.",
    ),
    Round43CaseCandidate(
        "data_center_water_reuse_infra_watch_candidate",
        "DATA_CENTER_WATER_REUSE_INFRA",
        "WATER_REUSE_REF",
        "AI 데이터센터 물 재활용 인프라",
        "GLOBAL",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("ai_datacenter_water_use", "water_reuse", "closed_loop_cooling"),
        ("customer_absent", "local_opposition", "weak_economics"),
        "watch_to_green_design_candidate",
        "needs_source_date_and_price_backfill",
        ("Round43 data-center water reuse design note",),
        "Water reuse is a plausible Watch-to-Green path, but customer contracts and unit economics must be sourced.",
    ),
)


ROUND43_PRICE_FIELDS: tuple[str, ...] = (
    "case_id",
    "symbol",
    "company_name",
    "primary_archetype",
    "secondary_archetypes",
    "stage1_date",
    "stage2_date",
    "stage3_date",
    "stage4b_date",
    "stage4c_date",
    "stage1_price",
    "stage2_price",
    "stage3_price",
    "stage4b_price",
    "stage4c_price",
    "peak_price",
    "MFE_30D",
    "MFE_90D",
    "MFE_180D",
    "MFE_1Y",
    "MFE_2Y",
    "MAE_30D",
    "MAE_90D",
    "MAE_180D",
    "MAE_1Y",
    "drawdown_after_peak",
    "below_stage3_price_flag",
    "ev_demand_indicator",
    "ess_contract_value",
    "capacity_utilization",
    "capex_amount",
    "capex_to_revenue",
    "fcf_margin",
    "op_margin_change",
    "eps_revision_1q",
    "eps_revision_1y",
    "lithium_price_change",
    "nickel_price_change",
    "raw_material_price_change",
    "solar_tariff_event",
    "customs_detention_flag",
    "subsidy_change_flag",
    "plant_idle_flag",
    "furlough_layoff_flag",
    "project_impairment_flag",
    "recycling_volume",
    "metal_recovery_revenue",
    "waste_treatment_volume",
    "carbon_credit_price",
    "cbam_exposure",
    "score_price_alignment",
    "price_validation_status",
)


def target_for(target_id: str) -> Round43ScoreTarget | None:
    for target in ROUND43_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round43_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND43_CASE_CANDIDATES:
        target = target_for(candidate.target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {candidate.target_id}")
        weights = target.score_weight.as_dict()
        stage4b_evidence = candidate.evidence_fields if candidate.case_type == "4b_watch" or candidate.stage4b_date else ()
        stage4c_evidence = candidate.red_flag_fields if candidate.case_type == "4c_thesis_break" or candidate.stage4c_date else ()
        record = E2RCaseRecord(
            case_id=candidate.case_id,
            symbol=candidate.symbol,
            company_name=candidate.company_name,
            market=candidate.market,
            sector_raw=candidate.target_id,
            primary_archetype=target.canonical_archetype,
            secondary_archetypes=candidate.secondary_archetypes,
            expected_group=candidate.expected_group,
            large_sector=target.large_sector.value,
            case_type=candidate.case_type,
            stage1_date=candidate.stage1_date,
            stage2_date=candidate.stage2_date,
            stage3_date=candidate.stage3_date,
            stage4b_date=candidate.stage4b_date,
            stage4c_date=candidate.stage4c_date,
            evidence_summary=(
                f"Round43 R3 case for {candidate.target_id}; "
                "case evidence is calibration-only and missing prices remain unfilled."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage2_signals or field in target.green_conditions),
            stage3_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage3_conditions),
            stage4b_evidence=stage4b_evidence,
            stage4c_evidence=stage4c_evidence,
            must_have_fields=target.green_conditions,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason="; ".join(candidate.red_flag_fields) if candidate.case_type in {"failed_rerating", "event_premium", "4b_watch", "4c_thesis_break"} else None,
            score_price_alignment=_score_price_alignment(candidate),
            rerating_result=_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
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
                "theme_label_is_not_score_evidence",
                "growth_theme_is_not_fcf_evidence",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=False,
                price_data_available=False,
                stage_dates_confidence=0.7 if candidate.stage2_date or candidate.stage4b_date or candidate.stage4c_date else 0.3,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round43_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND43_SCORE_TARGETS:
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
                "gate_only": str(target.gate_only).lower(),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round43_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND43_CASE_CANDIDATES:
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
                "stage2_date": candidate.stage2_date.isoformat() if candidate.stage2_date else "",
                "stage3_date": candidate.stage3_date.isoformat() if candidate.stage3_date else "",
                "stage4b_date": candidate.stage4b_date.isoformat() if candidate.stage4b_date else "",
                "stage4c_date": candidate.stage4c_date.isoformat() if candidate.stage4c_date else "",
                "evidence_fields": "|".join(candidate.evidence_fields),
                "red_flag_fields": "|".join(candidate.red_flag_fields),
                "alignment_hint": candidate.alignment_hint,
                "price_validation_status": candidate.price_validation_status,
                "production_input": "false",
                "notes": candidate.notes,
            }
        )
    return tuple(rows)


def round43_stage_date_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND43_SCORE_TARGETS:
        rows.append(
            {
                "target_id": target.target_id,
                "stage1": "|".join(target.stage1_signals),
                "stage2": "|".join(target.stage2_signals),
                "stage3": "|".join(target.stage3_conditions),
                "stage4b": "|".join(target.stage4b_conditions),
                "stage4c": "|".join(target.stage4c_conditions),
                "production_scoring_changed": "false",
            }
        )
    return tuple(rows)


def round43_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round43_backfill": "true"} for field in ROUND43_PRICE_FIELDS)


def round43_summary() -> dict[str, int | bool]:
    records = round43_case_records()
    return {
        "target_count": len(ROUND43_SCORE_TARGETS),
        "case_candidate_count": len(records),
        "structural_success_count": sum(1 for record in records if record.case_type == "structural_success"),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for record in records if record.case_type == "cyclical_success"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch"),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND43_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND43_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND43_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round43_r3_reports(
    *,
    output_directory: str | Path = ROUND43_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND43_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND43_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round43_r3_battery_ev_green_summary.md",
        "case_matrix": output / "round43_r3_case_matrix.csv",
        "stage_date_plan": output / "round43_r3_stage_date_plan.csv",
        "green_guardrails": output / "round43_r3_green_guardrails.md",
        "price_validation_plan": output / "round43_r3_price_validation_plan.md",
        "price_fields": output / "round43_r3_price_fields.csv",
    }
    _write_case_jsonl(round43_case_records(), cases)
    _write_rows(round43_score_profile_rows(), score_profiles)
    _write_rows(round43_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round43_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round43_price_field_rows(), paths["price_fields"])
    paths["summary"].write_text(render_round43_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round43_green_guardrail_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round43_price_validation_plan_markdown(), encoding="utf-8")
    return paths


def render_round43_summary_markdown() -> str:
    summary = round43_summary()
    lines = [
        "# Round-43 R3 Battery / EV / Green Energy Summary",
        "",
        f"- source_round: `{ROUND43_SOURCE_ROUND_PATH}`",
        "- large_sector: `BATTERY_EV_GREEN`",
        f"- target_count: {summary['target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- structural_success_count: {summary['structural_success_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- cyclical_success_count: {summary['cyclical_success_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- failed_rerating_count: {summary['failed_rerating_count']}",
        f"- stage4b_case_count: {summary['stage4b_case_count']}",
        f"- stage4c_case_count: {summary['stage4c_case_count']}",
        f"- green_possible_count: {summary['green_possible_count']}",
        f"- watch_yellow_first_count: {summary['watch_yellow_first_count']}",
        f"- redteam_first_count: {summary['redteam_first_count']}",
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "",
        "- R3 is a growth-theme sector, but the score frame must prioritize durability: utilization, contracts, margin, FCF, subsidy dependence, CAPEX burden, and policy/supply-chain risk.",
        "- Example: an EV battery CAPEX headline is not Green if demand slows and the plant sits idle.",
        "- Example: waste treatment can be Green-capable when permits, treatment volume, utilization, and recurring FCF are visible.",
    ]
    return "\n".join(lines) + "\n"


def render_round43_green_guardrail_markdown() -> str:
    lines = [
        "# Round-43 R3 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Red flags |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND43_SCORE_TARGETS:
        lines.append(
            "| "
            f"`{target.target_id}` | {target.posture.value} | "
            f"{', '.join(target.green_conditions) or 'not applicable'} | {', '.join(target.red_flags)} |"
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not apply these R3 v1.0 weights to production scoring yet.",
            "- Do not treat EV, ESS, solar, hydrogen, recycling, or carbon-policy labels as score evidence by themselves.",
            "- Do not invent contracts, utilization, margin, FCF, CAPEX, subsidy, tariff, mineral-price, or price-path fields.",
            "- Do not lower Stage 3-Green for growth themes. Most R3 paths should remain Watch until FCF is visible.",
            "- Treat plant idle, worker furlough, customs detention, impairment, lithium price crash, fire, recall, and regulation as RedTeam evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round43_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-43 R3 Price Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign stage dates from source evidence only.",
        "2. Store stage-date close prices from official price data.",
        "3. Calculate MFE_30D / 90D / 180D / 1Y / 2Y.",
        "4. Calculate MAE_30D / 90D / 180D / 1Y.",
        "5. Calculate peak price, drawdown after peak, and below-stage3 flag.",
        "6. Compare price paths with OP/EPS revision, utilization, CAPEX, FCF, mineral prices, subsidy/tariff events, and project-break evidence.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | stage candidate | check |",
        "| --- | --- | --- |",
    ]
    for row in round43_case_candidate_rows():
        if row["stage2_date"] or row["stage4b_date"] or row["stage4c_date"]:
            stage_date = row["stage2_date"] or row["stage4b_date"] or row["stage4c_date"] or "needs_source_date"
            lines.append(f"| `{row['case_id']}` | {stage_date} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `aligned`: contracts, utilization, margin, FCF, and price rerating persist together.",
            "- `cyclical_success`: mineral or energy cycle helped price, but structural durability is not proven.",
            "- `event_premium`: subsidy, policy, plant, MOU, or factory news moved attention without revenue conversion.",
            "- `false_positive_score`: growth-theme evidence looked strong, but demand, CAPEX, margin, or FCF failed.",
            "- `thesis_break`: plant idle, worker furlough, customs detention, impairment, or mineral-price crash damages the thesis.",
        ]
    )
    return "\n".join(lines) + "\n"


def _score_price_alignment(candidate: Round43CaseCandidate) -> str:
    if "evidence_good_but_price_failed" in candidate.alignment_hint:
        return "evidence_good_but_price_failed"
    if "aligned" in candidate.alignment_hint:
        return "aligned"
    if candidate.case_type == "event_premium":
        return "price_moved_without_evidence"
    if candidate.case_type in {"4b_watch"}:
        return "price_moved_without_evidence"
    if candidate.case_type in {"failed_rerating", "4c_thesis_break"}:
        return "false_positive_score"
    return "unknown"


def _rerating_result(candidate: Round43CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "true_rerating"
    if candidate.case_type == "cyclical_success":
        return "cyclical_rerating"
    if candidate.case_type == "event_premium":
        return "event_premium"
    if candidate.case_type == "4b_watch":
        return "theme_overheat"
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    if candidate.case_type == "failed_rerating":
        return "no_rerating"
    return "unknown"


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
        writer = csv.DictWriter(handle, fieldnames=tuple(row_tuple[0].keys()), lineterminator="\n")
        writer.writeheader()
        for row in row_tuple:
            writer.writerow(row)
    return path


__all__ = [
    "ROUND43_CASE_CANDIDATES",
    "ROUND43_DEFAULT_CASES_PATH",
    "ROUND43_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND43_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND43_PRICE_FIELDS",
    "ROUND43_SCORE_TARGETS",
    "ROUND43_SOURCE_ROUND_PATH",
    "Round43CaseCandidate",
    "Round43ScoreTarget",
    "Round43ScoreWeightDraft",
    "render_round43_green_guardrail_markdown",
    "render_round43_price_validation_plan_markdown",
    "render_round43_summary_markdown",
    "round43_case_candidate_rows",
    "round43_case_records",
    "round43_price_field_rows",
    "round43_score_profile_rows",
    "round43_stage_date_rows",
    "round43_summary",
    "target_for",
    "write_round43_r3_reports",
]
