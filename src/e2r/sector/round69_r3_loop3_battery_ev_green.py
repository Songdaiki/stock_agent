"""Round-69 R3 Loop-3 battery, EV, and green-energy pack.

Round 69 tightens the Round-56 R3 split. It separates ESS LFP grid storage
from generic battery recycling/ESS shift, adds battery-health transparency
and lithium-cycle overlays, and keeps EV CAPA, solar tariff, wind project,
fire/certification, and SOH risks explicit.

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


ROUND69_SOURCE_ROUND_PATH = "docs/round/round_69.md"
ROUND69_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round69_r3_loop3_battery_ev_green"
ROUND69_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r3_loop3_round69.jsonl"
ROUND69_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round69_r3_loop3_v3.csv"


@dataclass(frozen=True)
class Round69ScoreWeightDraft:
    eps_fcf: int | str
    structural_visibility: int | str
    bottleneck_pricing: int | str
    market_mispricing: int | str
    valuation: int | str
    capital_allocation: int | str
    information_confidence: int | str

    def as_dict(self) -> dict[str, int | str]:
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
class Round69ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round69ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    loop3_penalty_axes: tuple[str, ...]
    normalization_point: str
    gate_only: bool = False

    @property
    def large_sector(self) -> Round10LargeSector:
        return Round10LargeSector.BATTERY_EV_GREEN

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round69CaseCandidate:
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


def _w(
    eps_fcf: int | str,
    visibility: int | str,
    bottleneck: int | str,
    mispricing: int | str,
    valuation: int | str,
    capital: int | str = 0,
    confidence: int | str = 5,
) -> Round69ScoreWeightDraft:
    return Round69ScoreWeightDraft(eps_fcf, visibility, bottleneck, mispricing, valuation, capital, confidence)


def _target(
    target_id: str,
    archetype: E2RArchetype,
    posture: Round10ThemePosture,
    weight: Round69ScoreWeightDraft,
    *,
    stage1: tuple[str, ...],
    stage2: tuple[str, ...],
    stage3: tuple[str, ...],
    stage4b: tuple[str, ...],
    stage4c: tuple[str, ...],
    green: tuple[str, ...],
    red: tuple[str, ...],
    penalties: tuple[str, ...],
    note: str,
    gate_only: bool = False,
) -> Round69ScoreTarget:
    return Round69ScoreTarget(
        target_id,
        archetype,
        posture,
        weight,
        stage1,
        stage2,
        stage3,
        stage4b,
        stage4c,
        green,
        red,
        penalties,
        note,
        gate_only,
    )


ROUND69_SCORE_TARGETS: tuple[Round69ScoreTarget, ...] = (
    _target(
        "BATTERY_MATERIALS_CAPEX_OVERHEAT",
        E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT,
        Round10ThemePosture.REDTEAM_FIRST,
        _w(17, 12, 12, 8, 7),
        stage1=("ev_growth_narrative", "long_term_supply_contract", "capa_expansion_news"),
        stage2=("real_contract", "price_margin_improvement", "op_eps_revision", "line_utilization"),
        stage3=("long_term_contract", "price_pass_through", "fcf_after_capex", "demand_visibility"),
        stage4b=("per_pbr_overheat", "capa_race", "target_price_crowding"),
        stage4c=("ev_demand_slowdown", "raw_material_price_drop", "capa_overbuild", "customer_contract_cancelled", "plant_idle"),
        green=("contract_quality", "price_pass_through", "fcf_after_capex", "demand_visibility"),
        red=("ev_demand_slowdown", "capa_overbuild", "lithium_price_crash", "customer_contract_cancelled", "plant_idle"),
        penalties=("ev_demand_slowdown", "capa_overbuild", "contract_cancellation", "mineral_price"),
        note="Loop 3 lowers battery-material scores because EV CAPA and contracts can quickly become 4C.",
    ),
    _target(
        "BATTERY_EQUIPMENT_PARTS",
        E2RArchetype.BATTERY_EQUIPMENT_PARTS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(19, 16, 11, 11, 9),
        stage1=("battery_equipment_order", "cell_customer_capex", "delivery_schedule_keyword"),
        stage2=("customer_order", "delivery_schedule", "margin_visibility", "revenue_conversion"),
        stage3=("order_to_revenue_conversion", "customer_diversification", "op_eps_revision"),
        stage4b=("equipment_capex_cycle_crowded", "cell_capex_peak"),
        stage4c=("customer_capex_cut", "delivery_delay", "margin_miss", "single_customer", "ev_line_idle"),
        green=("customer_order", "delivery_schedule", "margin_visibility", "op_eps_revision"),
        red=("customer_capex_cut", "delivery_delay", "single_customer", "ev_line_idle"),
        penalties=("customer_capex_cut", "delivery_delay", "ev_line_idle"),
        note="Battery equipment is Watch-to-Green only when CAPEX becomes delivery, revenue, and margin.",
    ),
    _target(
        "BATTERY_RECYCLING_ESS_SHIFT",
        E2RArchetype.BATTERY_RECYCLING_ESS_SHIFT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(20, 18, 14, 11, 10),
        stage1=("battery_recycling", "second_life_battery", "black_mass", "recycling_policy"),
        stage2=("recycling_volume", "metal_recovery_revenue", "customer_contract", "ess_use_case"),
        stage3=("recurring_recycling_fcf", "second_life_revenue", "soh_validation", "customer_diversification"),
        stage4b=("recycling_premium_overheat", "critical_minerals_narrative_crowded"),
        stage4c=("recycling_volume_shortfall", "soh_validation_failure", "metal_price_drop", "second_life_margin_miss"),
        green=("recycling_volume", "metal_recovery_revenue", "customer_contract", "soh_validation", "recurring_fcf"),
        red=("contract_value_missing", "recycling_volume_shortfall", "metal_price_drop", "soh_unreliable"),
        penalties=("recycling_volume", "soh_validation", "metal_price", "contract_value_missing"),
        note="Recycling/second-life stays Watch-to-Green but now requires SOH and grading-cost validation.",
    ),
    _target(
        "ESS_LFP_GRID_STORAGE",
        E2RArchetype.ESS_LFP_GRID_STORAGE,
        Round10ThemePosture.GREEN_POSSIBLE,
        _w(22, 21, 15, 12, 11),
        stage1=("ess_shift", "lfp_ess_production", "north_america_ess_demand", "grid_storage"),
        stage2=("ess_customer_contract", "ess_contract_value", "ess_contract_duration", "ess_contract_volume_gwh", "production_factory"),
        stage3=("ess_revenue_growth", "ess_opm", "fcf_conversion", "customer_diversification"),
        stage4b=("ess_narrative_crowded", "lfp_ess_related_rally"),
        stage4c=("ess_margin_miss", "lfp_competition", "customer_demand_slowdown", "subsidy_or_tariff_damage"),
        green=("ess_contract_value", "ess_contract_duration", "customer", "gwh_volume", "ess_margin", "fcf_conversion"),
        red=("contract_value_missing", "ess_margin_unverified", "customer_concentration", "subsidy_dependency"),
        penalties=("ess_margin", "lfp_competition", "customer_concentration", "subsidy"),
        note="ESS LFP grid storage is split out because value, duration, customer, and GWh can make a cleaner Stage 2/3 path.",
    ),
    _target(
        "EV_INFRASTRUCTURE",
        E2RArchetype.EV_INFRASTRUCTURE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(16, 13, 7, 10, 8),
        stage1=("charging_station", "fast_charging", "ev_infrastructure_policy"),
        stage2=("utilization", "recurring_revenue", "subsidy_visibility"),
        stage3=("profitable_utilization", "repeat_revenue", "subsidy_independent_margin"),
        stage4b=("ev_charging_theme_crowded",),
        stage4c=("low_utilization", "subsidy_cut", "fire_regulation", "maintenance_cost"),
        green=("utilization", "recurring_revenue", "profitability"),
        red=("low_utilization", "subsidy_dependency", "fire_regulation"),
        penalties=("utilization", "fire_regulation", "subsidy_dependency"),
        note="EV infrastructure needs utilization and unit economics, not charger-count headlines.",
    ),
    _target(
        "HYDROGEN_FUEL_CELL_INFRA",
        E2RArchetype.HYDROGEN_FUEL_CELL_INFRA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(18, 18, 12, 12, 10),
        stage1=("hydrogen_factory_groundbreaking", "hydrogen_policy", "electrolyzer_or_fuel_cell_capex"),
        stage2=("customer_or_demand_source", "production_capacity", "delivery_contract", "plant_completion_date"),
        stage3=("utilization", "op_eps_conversion", "subsidy_independent_economics"),
        stage4b=("hydrogen_theme_overheat",),
        stage4c=("subsidy_cut", "customer_absent", "low_utilization", "project_delay"),
        green=("customer_demand", "production_capacity", "utilization", "op_eps_conversion"),
        red=("subsidy_dependency", "customer_absent", "low_utilization"),
        penalties=("customer_absent", "utilization", "subsidy_dependency", "infrastructure_gap"),
        note="Hydrogen CAPEX can reach Stage 2, but Green needs customers, utilization, and OP conversion.",
    ),
    _target(
        "SOLAR_TARIFF_SUPPLYCHAIN",
        E2RArchetype.SOLAR_TARIFF_SUPPLYCHAIN,
        Round10ThemePosture.REDTEAM_FIRST,
        _w(16, 13, 11, 9, 7),
        stage1=("solar_factory", "us_factory", "subsidy_policy"),
        stage2=("utilization", "customer_contract", "supply_chain_stable", "op_turnaround"),
        stage3=("subsidy_independent_fcf", "supply_chain_clean", "margin_visible"),
        stage4b=("solar_us_manufacturing_narrative_crowded", "subsidy_premium"),
        stage4c=("tariff_risk", "customs_detention", "uflpa_detention", "feoc_risk", "worker_furlough", "component_delay"),
        green=("utilization", "customer_contract", "supply_chain_stable", "fcf_margin"),
        red=("tariff_risk", "customs_detention", "uflpa_detention", "subsidy_dependency", "feoc_risk"),
        penalties=("customs", "tariff", "uflpa", "feoc", "supply_chain_disruption"),
        note="Solar stays RedTeam-first because subsidy and US manufacturing can break on customs or supply-chain detention.",
    ),
    _target(
        "RENEWABLE_ENERGY_POLICY",
        E2RArchetype.RENEWABLE_ENERGY_POLICY,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(16, 13, 9, 9, 7),
        stage1=("wind_project", "renewable_policy", "ppa_or_project_news"),
        stage2=("permitted_project", "funding_visible", "cost_schedule_visible", "construction_start"),
        stage3=("project_economics", "op_eps_conversion", "cost_controlled", "repeat_project_backlog"),
        stage4b=("renewable_policy_crowded", "project_premium"),
        stage4c=("impairment", "project_delay", "financing_cost_increase", "foundation_cost", "cost_overrun"),
        green=("permitting", "funding", "cost_schedule", "margin_visibility"),
        red=("permitting_delay", "financing_cost", "cost_overrun", "impairment"),
        penalties=("rates", "cost_overrun", "permitting", "impairment"),
        note="Wind/PPA policy stories remain Watch until project economics survive rates, permits, and foundation costs.",
    ),
    _target(
        "WASTE_RECYCLING_ENVIRONMENT",
        E2RArchetype.WASTE_RECYCLING_ENVIRONMENT,
        Round10ThemePosture.GREEN_POSSIBLE,
        _w(18, 22, 15, 13, 12, 3),
        stage1=("waste_treatment_platform", "permit_value", "plastic_recycling", "waste_to_energy"),
        stage2=("treatment_volume", "long_term_contract", "utilization", "fcf_visible"),
        stage3=("permit_asset", "recurring_fcf", "valuation_frame_change", "mna_value_support"),
        stage4b=("waste_mna_premium_crowded", "permit_value_fully_priced"),
        stage4c=("utilization_drop", "capex_burden", "metal_price_drop", "regulatory_cost"),
        green=("permit_asset", "treatment_volume", "utilization", "recurring_fcf"),
        red=("utilization_drop", "capex_burden", "commodity_recycling_price_drop"),
        penalties=("utilization", "capex", "metal_price", "regulatory_cost"),
        note="Waste treatment remains the clearest R3 Green-capable axis when permits, volume, and recurring FCF are proven.",
    ),
    _target(
        "CARBON_CREDIT_CBAM_COMPLIANCE",
        E2RArchetype.CARBON_CREDIT_CBAM_COMPLIANCE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(14, 17, 10, 12, 8, 2, 6),
        stage1=("eu_ets_or_cbam_policy", "carbon_accounting", "compliance_monitoring"),
        stage2=("carbon_accounting_revenue", "verification_revenue", "low_carbon_product_premium"),
        stage3=("recurring_compliance_revenue", "cost_pass_through", "industrial_customer_base"),
        stage4b=("carbon_price_theme_crowded",),
        stage4c=("carbon_price_drop", "free_allowance_expansion", "greenwashing_risk", "policy_delay"),
        green=("recurring_revenue", "verification_customer", "cost_pass_through"),
        red=("carbon_price_volatility", "greenwashing", "policy_reversal"),
        penalties=("policy_reform", "carbon_price", "greenwashing"),
        note="Carbon price is not enough; compliance revenue and cost pass-through are the stronger route.",
    ),
    _target(
        "DATA_CENTER_WATER_REUSE_INFRA",
        E2RArchetype.DATA_CENTER_WATER_REUSE_INFRA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(16, 18, 14, 12, 10, 2),
        stage1=("ai_datacenter_water_use", "water_reuse", "closed_loop_cooling", "water_treatment"),
        stage2=("data_center_customer", "reuse_project", "contracted_revenue"),
        stage3=("repeat_water_reuse_revenue", "margin_visible", "local_permit_support"),
        stage4b=("water_reuse_theme_crowded",),
        stage4c=("customer_absent", "local_opposition", "unit_economics_weak", "permitting_delay"),
        green=("data_center_customer", "contracted_revenue", "unit_economics"),
        red=("customer_absent", "local_opposition", "weak_economics"),
        penalties=("customer_absent", "local_opposition", "economics"),
        note="Data-center water reuse needs named customers and economics before Green.",
    ),
    _target(
        "EV_FIRE_RISK_OVERLAY",
        E2RArchetype.EV_FIRE_RISK_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        _w("gate", "gate", "gate", "gate", "gate", "gate", "gate"),
        stage1=("ev_fire", "battery_recall", "insurance_cost", "battery_certification"),
        stage2=("risk_event_detected",),
        stage3=("not_applicable_gate_only",),
        stage4b=("not_applicable_gate_only",),
        stage4c=("battery_fire", "certification_requirement", "battery_supplier_disclosure", "recall", "insurance_cost", "parking_charging_regulation"),
        green=(),
        red=("battery_fire", "certification_requirement", "recall", "insurance_cost", "fire_regulation"),
        penalties=("fire", "certification", "recall", "insurance"),
        note="EV fire/certification/recall/regulation overlay is a RedTeam gate, not positive score.",
        gate_only=True,
    ),
    _target(
        "BATTERY_HEALTH_TRANSPARENCY_OVERLAY",
        E2RArchetype.BATTERY_HEALTH_TRANSPARENCY_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        _w("gate", "gate", "gate", "gate", "gate", "gate", "gate"),
        stage1=("soh_unreliable", "battery_passport", "second_life_validation", "residual_capacity_uncertainty"),
        stage2=("transparency_risk_detected",),
        stage3=("not_applicable_gate_only",),
        stage4b=("not_applicable_gate_only",),
        stage4c=("soh_unreliable", "residual_capacity_uncertainty", "second_life_grading_cost", "warranty_enforcement_risk"),
        green=(),
        red=("soh_unreliable", "second_life_grading_cost", "battery_passport_compliance", "warranty_risk"),
        penalties=("soh", "second_life_validation", "battery_passport", "grading_cost"),
        note="SOH opacity is a battery recycling and second-life RedTeam gate, not a Green input.",
        gate_only=True,
    ),
    _target(
        "LITHIUM_CYCLE_OVERLAY",
        E2RArchetype.LITHIUM_CYCLE_OVERLAY,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w("cycle", "cycle", "cycle", "cycle", "cycle", "cycle", 5),
        stage1=("lithium_price_rebound", "mine_shutdown", "ess_lithium_demand"),
        stage2=("ess_demand_outlook_improves", "cost_curve_support", "inventory_absorption"),
        stage3=("low_cost_structure", "long_term_offtake", "fcf_defense", "capex_discipline"),
        stage4b=("lithium_rebound_crowded", "mine_restart_ignored", "sodium_ion_ignored"),
        stage4c=("lithium_price_crash", "mine_restart_supply_rebound", "ev_demand_slowdown", "capex_cut"),
        green=("low_cost_structure", "long_term_offtake", "fcf_defense", "capex_discipline"),
        red=("lithium_price_crash", "mine_restart", "supply_rebound", "sodium_ion_competition"),
        penalties=("price_crash", "mine_restart", "sodium_ion", "ev_demand_slowdown"),
        note="Lithium is a cycle overlay by default; ESS demand can help Stage 1/2 but does not make Green alone.",
    ),
)


ROUND69_CASE_CANDIDATES: tuple[Round69CaseCandidate, ...] = (
    Round69CaseCandidate(
        "lg_energy_tesla_lfp_ess_contract_case",
        "ESS_LFP_GRID_STORAGE",
        "373220_TESLA_ESS",
        "LGES-Tesla LFP ESS supply contract",
        "KR",
        "success_candidate",
        None,
        date(2025, 7, 30),
        None,
        None,
        None,
        ("ess_contract_value_4_3b", "ess_contract_duration_2027_08_2030_07", "tesla_customer_reported", "lfp_ess_us_production", "extension_option_7y"),
        ("customer_name_officially_confidential", "ess_margin_unverified", "lfp_competition", "ira_tariff_feoc_risk"),
        "ess_contract_aligned",
        "needs_price_backfill",
        ("round_69.md WSJ LG Energy Tesla ESS deal",),
        "Contract value, duration, customer indication, and ESS use case make this the cleanest R3 Loop-3 Stage 2 ESS reference.",
    ),
    Round69CaseCandidate(
        "sk_on_flatiron_ess_7_2gwh_case",
        "ESS_LFP_GRID_STORAGE",
        "SKON_FLATIRON_REF",
        "SK On-Flatiron ESS 7.2GWh supply",
        "KR",
        "success_candidate",
        None,
        date(2025, 9, 3),
        None,
        None,
        None,
        ("ess_contract_volume_7_2gwh", "ess_contract_duration_2026_2030", "lfp_ess_mass_production", "ev_line_to_ess_conversion"),
        ("contract_value_missing", "ess_margin_unverified", "customer_demand_unverified", "ev_line_conversion_cost"),
        "ess_contract_stage2_value_missing",
        "needs_price_backfill",
        ("round_69.md Reuters SK On Flatiron ESS deal",),
        "GWh and duration support Stage 2, but missing contract value caps EPS/FCF and Green credit.",
    ),
    Round69CaseCandidate(
        "gm_lg_ultium_ohio_idle_case",
        "BATTERY_MATERIALS_CAPEX_OVERHEAT",
        "GM_LG_ULTIUM_REF",
        "GM-LG Ultium Ohio plant idle",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2026, 5, 12),
        ("ev_battery_capa", "tennessee_ess_shift_candidate"),
        ("ev_demand_slowdown", "plant_idle", "layoff_furlough", "capacity_underutilization", "restart_uncertain"),
        "ev_capa_false_green_plus_ess_shift_watch",
        "needs_price_backfill",
        ("round_69.md Reuters GM-LG Ohio battery plant",),
        "EV CAPA can become hard 4C while a separate ESS conversion remains only a Watch candidate.",
        (E2RArchetype.ESS_LFP_GRID_STORAGE,),
    ),
    Round69CaseCandidate(
        "ford_lges_ev_contract_cancel_case",
        "BATTERY_MATERIALS_CAPEX_OVERHEAT",
        "FORD_LGES_CANCEL_REF",
        "Ford-LGES EV battery contract cancellation",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2025, 12, 17),
        ("ev_battery_contract_6_5b", "ford_ev_program"),
        ("contract_cancelled", "ev_model_discontinued", "write_down_19_5b", "policy_shift", "ev_demand_slowdown"),
        "ev_battery_contract_cancellation_hard_4c",
        "needs_price_backfill",
        ("round_69.md Reuters Ford LGES contract cancellation",),
        "Long-term EV battery supply contracts are not automatically Green if customer EV strategy changes.",
    ),
    Round69CaseCandidate(
        "redwood_recycling_energy_storage_case",
        "BATTERY_RECYCLING_ESS_SHIFT",
        "REDWOOD_REF",
        "Redwood recycling and energy storage",
        "US",
        "success_candidate",
        None,
        date(2025, 10, 23),
        None,
        date(2025, 10, 23),
        None,
        ("battery_recycling", "metal_recovery_lithium_cobalt_nickel_copper", "grid_services", "datacenter_ess", "strategic_customers"),
        ("private_company_reference", "recycling_margin_unverified", "soh_validation_needed", "public_price_unavailable"),
        "recycling_plus_storage_structural_reference",
        "missing_public_price_data",
        ("round_69.md Reuters Redwood recycling funding",),
        "Recycling gets stronger when recovered metals, ESS/grid services, data-center demand, and customers connect.",
        (E2RArchetype.ESS_LFP_GRID_STORAGE,),
    ),
    Round69CaseCandidate(
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
        ("waste_treatment_platform", "permit_asset", "plastic_recycling", "waste_to_energy", "mna_value_1tn_krw", "metro_area_coverage"),
        ("utilization_drop", "capex_burden", "regulatory_cost"),
        "waste_platform_structural_reference",
        "missing_public_price_data",
        ("round_69.md Reuters EQT KJ Environment platform",),
        "Waste treatment is R3's clearest Green-capable infrastructure reference when permits, volume, and recurring FCF are visible.",
    ),
    Round69CaseCandidate(
        "hyundai_hydrogen_fuel_cell_plant_case",
        "HYDROGEN_FUEL_CELL_INFRA",
        "005380",
        "현대차 수소연료전지 울산 공장",
        "KR",
        "success_candidate",
        None,
        date(2025, 10, 30),
        None,
        date(2025, 10, 30),
        None,
        ("hydrogen_capex_930bn_krw", "plant_completion_2027", "fuel_cell_capacity", "electrolyzer_plan", "commercial_vehicle_ship_construction_equipment"),
        ("customer_absent", "subsidy_dependency", "low_utilization", "hydrogen_infra_gap"),
        "hydrogen_capex_stage1_to_stage2_candidate",
        "needs_price_backfill",
        ("round_69.md Reuters Hyundai hydrogen fuel-cell plant",),
        "Actual CAPEX is stronger than policy talk, but customers, utilization, and OP conversion are still required.",
    ),
    Round69CaseCandidate(
        "qcells_customs_detention_furlough_case",
        "SOLAR_TARIFF_SUPPLYCHAIN",
        "QCELLS_REF",
        "Qcells customs detention and furlough",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2025, 11, 8),
        ("solar_us_factory", "subsidy_policy"),
        ("customs_detention", "uflpa_flag", "component_delay", "furlough_layoff", "production_disruption"),
        "solar_policy_supplychain_4c",
        "missing_public_price_data",
        ("round_69.md Reuters Qcells customs detention",),
        "Solar subsidy and US manufacturing narrative can break when customs and component supply stop production.",
    ),
    Round69CaseCandidate(
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
        ("offshore_wind_project", "renewable_policy", "ppa"),
        ("impairment_1_7b", "project_delay", "cost_overrun", "financing_cost_increase", "foundation_cost"),
        "wind_project_impairment_4c",
        "needs_price_backfill",
        ("round_69.md Reuters Orsted Sunrise Wind impairment",),
        "Renewable policy and PPAs cannot overcome project economics when rates, foundations, and delay create impairment.",
    ),
    Round69CaseCandidate(
        "lithium_price_86pct_crash_case",
        "LITHIUM_CYCLE_OVERLAY",
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
        ("lithium_price_crash", "raw_material_price_drop", "mine_restart_supply_rebound", "ev_demand_slowdown"),
        "lithium_cycle_hard_counterexample",
        "missing_price_data",
        ("round_69.md Reuters lithium prices after crash",),
        "Lithium rebound is not structural Green without cost curve, offtake, FCF, and CAPEX discipline.",
    ),
    Round69CaseCandidate(
        "lithium_ess_demand_recovery_case",
        "LITHIUM_CYCLE_OVERLAY",
        "LITHIUM_ESS_REF",
        "리튬 ESS demand recovery",
        "GLOBAL",
        "cyclical_success",
        None,
        date(2026, 1, 5),
        None,
        None,
        None,
        ("ess_lithium_demand_growth", "datacenter_storage_demand", "china_power_market_reform"),
        ("mine_restart_supply_rebound", "sodium_ion_competition", "ev_subsidy_expiry"),
        "lithium_ess_demand_recovery_but_cycle_watch",
        "missing_price_data",
        ("round_69.md Reuters energy storage lithium demand",),
        "ESS can improve lithium demand, but lithium miners remain cycle/Watch until FCF and supply response are controlled.",
    ),
    Round69CaseCandidate(
        "korea_ev_battery_certification_fire_case",
        "EV_FIRE_RISK_OVERLAY",
        "EV_FIRE_RISK_REF",
        "Korea EV battery certification and fire risk",
        "KR",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2024, 8, 25),
        ("ev_growth_narrative",),
        ("battery_fire", "battery_certification", "battery_supplier_disclosure", "parking_charging_regulation", "insurance_cost"),
        "ev_fire_regulatory_overlay",
        "missing_price_data",
        ("round_69.md Reuters Korea EV battery certification",),
        "EV fire and battery disclosure should become a separate RedTeam overlay for battery, charging, and ESS candidates.",
    ),
    Round69CaseCandidate(
        "battery_soh_transparency_case",
        "BATTERY_HEALTH_TRANSPARENCY_OVERLAY",
        "BATTERY_SOH_REF",
        "Battery SOH transparency and second-life risk",
        "GLOBAL",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("soh_unreliable", "residual_capacity_uncertainty", "second_life_battery", "battery_passport"),
        ("soh_validation_failure", "second_life_grading_cost", "warranty_enforcement_risk", "battery_passport_compliance"),
        "battery_health_transparency_redteam",
        "needs_exact_stage_date_backfill",
        ("round_69.md arXiv battery health validation",),
        "Second-life and recycling economics can be overstated when SOH and residual capacity are not independently validated.",
    ),
)


ROUND69_PRICE_FIELDS: tuple[str, ...] = (
    "case_id", "symbol", "company_name", "primary_archetype", "secondary_archetypes",
    "stage1_date", "stage2_date", "stage3_date", "stage4b_date", "stage4c_date",
    "stage1_price", "stage2_price", "stage3_price", "stage4b_price", "stage4c_price", "peak_price", "peak_date",
    "MFE_30D", "MFE_90D", "MFE_180D", "MFE_1Y", "MFE_2Y",
    "MAE_30D", "MAE_90D", "MAE_180D", "MAE_1Y",
    "drawdown_after_peak", "below_stage2_price_flag", "below_stage3_price_flag",
    "ev_demand_indicator", "ev_sales_growth", "ev_subsidy_change_flag", "ev_tax_credit_expiry_flag",
    "automaker_ev_cutback_flag", "ev_model_discontinued_flag", "plant_idle_flag", "layoff_furlough_flag",
    "contract_cancelled_flag", "capacity_utilization", "capex_amount", "capex_to_revenue", "capex_cut_flag",
    "ess_contract_value", "ess_contract_duration_months", "ess_contract_customer", "ess_contract_volume_gwh",
    "ess_capacity_gwh", "ess_capacity_utilization", "ess_margin", "ess_revenue_growth", "lfp_ess_flag",
    "grid_storage_flag", "data_center_storage_flag", "battery_material_contract_value",
    "battery_material_contract_duration", "price_pass_through_flag", "raw_material_price_change",
    "lithium_price_change", "nickel_price_change", "cobalt_price_change", "black_mass_price",
    "metal_recovery_revenue", "recycling_volume", "recovered_material_volume", "recovery_rate", "pCAM_output",
    "recycling_customer_contract", "second_life_battery_flag", "soh_validation_flag",
    "battery_passport_compliance_flag", "battery_grading_cost", "waste_treatment_volume",
    "waste_treatment_capacity", "permit_asset_flag", "recurring_fcf_flag", "waste_to_energy_flag",
    "plastic_recycling_revenue", "catchment_area_population_share", "hydrogen_capex_amount",
    "hydrogen_plant_completion_date", "fuel_cell_capacity", "electrolyzer_capacity",
    "hydrogen_customer_contract", "hydrogen_subsidy_dependency", "hydrogen_capacity_utilization",
    "solar_tariff_event", "customs_detention_flag", "uflpa_flag", "feoc_flag", "component_delay_flag",
    "solar_capacity_utilization", "furlough_layoff_flag", "wind_project_delay_flag",
    "wind_project_impairment", "financing_cost_change", "foundation_cost_increase", "permitting_delay_flag",
    "grid_connection_delay_flag", "carbon_credit_price", "cbam_exposure", "carbon_accounting_revenue",
    "pass_through_ability", "ev_fire_event_flag", "battery_certification_flag",
    "battery_supplier_disclosure_flag", "recall_flag", "insurance_cost_change",
    "underground_parking_regulation_flag", "overcharge_prevention_charger_flag",
    "score_price_alignment", "price_validation_status", "review_notes",
)


def round69_target_for(target_id: str) -> Round69ScoreTarget | None:
    for target in ROUND69_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round69_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND69_CASE_CANDIDATES:
        target = round69_target_for(candidate.target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {candidate.target_id}")
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
                f"Round69 R3 Loop-3 case for {candidate.target_id}; "
                "EV growth, ESS contracts, recycling economics, and green-policy risks remain separated."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage2_signals or field in target.green_conditions),
            stage3_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage3_conditions),
            stage4b_evidence=stage4b_evidence,
            stage4c_evidence=stage4c_evidence,
            must_have_fields=target.green_conditions,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason=(
                "; ".join(candidate.red_flag_fields)
                if candidate.case_type in {"failed_rerating", "event_premium", "overheat", "4b_watch", "4c_thesis_break", "one_off"}
                else None
            ),
            score_price_alignment=_score_price_alignment(candidate),
            rerating_result=_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
            score_weight_hint=_score_weight_hint(target),
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "require_price_path_validation",
                "ev_growth_is_not_fcf_evidence",
                "do_not_invent_contract_value_margin_utilization_customer_or_stage_prices",
                "ess_lfp_storage_needs_value_duration_customer_gwh_margin",
                "battery_recycling_needs_soh_validation_and_recovered_material_revenue",
                "solar_wind_policy_requires_project_economics",
                "ev_fire_certification_is_redteam_gate",
                "lithium_is_cycle_overlay_not_structural_green_by_default",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=False,
                price_data_available=False,
                stage_dates_confidence=0.75 if candidate.stage1_date or candidate.stage2_date or candidate.stage4b_date or candidate.stage4c_date else 0.2,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round69_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND69_SCORE_TARGETS:
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
                "loop3_penalty_axes": "|".join(target.loop3_penalty_axes),
                "gate_only": str(target.gate_only).lower(),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round69_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND69_CASE_CANDIDATES:
        target = round69_target_for(candidate.target_id)
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
                "stage1_date": candidate.stage1_date.isoformat() if candidate.stage1_date else "",
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


def round69_stage_date_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "target_id": target.target_id,
            "stage1": "|".join(target.stage1_signals),
            "stage2": "|".join(target.stage2_signals),
            "stage3": "|".join(target.stage3_conditions),
            "stage4b": "|".join(target.stage4b_conditions),
            "stage4c": "|".join(target.stage4c_conditions),
            "loop3_penalty_axes": "|".join(target.loop3_penalty_axes),
            "gate_only": str(target.gate_only).lower(),
            "production_scoring_changed": "false",
        }
        for target in ROUND69_SCORE_TARGETS
    )


def round69_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round69_backfill": "true"} for field in ROUND69_PRICE_FIELDS)


def round69_summary() -> dict[str, int | bool]:
    records = round69_case_records()
    return {
        "target_count": len(ROUND69_SCORE_TARGETS),
        "case_candidate_count": len(records),
        "structural_success_count": sum(1 for record in records if record.case_type == "structural_success"),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for record in records if record.case_type == "cyclical_success"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND69_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND69_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND69_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "gate_only_target_count": sum(1 for target in ROUND69_SCORE_TARGETS if target.gate_only),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round69_r3_loop3_reports(
    *,
    output_directory: str | Path = ROUND69_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND69_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND69_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round69_r3_loop3_battery_ev_green_summary.md",
        "case_matrix": output / "round69_r3_loop3_case_matrix.csv",
        "stage_date_plan": output / "round69_r3_loop3_stage_date_plan.csv",
        "green_guardrails": output / "round69_r3_loop3_green_guardrails.md",
        "risk_overlays": output / "round69_r3_loop3_risk_overlays.md",
        "price_validation_plan": output / "round69_r3_loop3_price_validation_plan.md",
        "price_fields": output / "round69_r3_loop3_price_fields.csv",
    }
    _write_case_jsonl(round69_case_records(), cases)
    _write_rows(round69_score_profile_rows(), score_profiles)
    _write_rows(round69_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round69_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round69_price_field_rows(), paths["price_fields"])
    paths["summary"].write_text(render_round69_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round69_green_guardrail_markdown(), encoding="utf-8")
    paths["risk_overlays"].write_text(render_round69_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round69_price_validation_plan_markdown(), encoding="utf-8")
    return paths


def render_round69_summary_markdown() -> str:
    summary = round69_summary()
    lines = [
        "# Round-69 R3 Loop-3 Battery / EV / Green-Energy Summary",
        "",
        f"- source_round: `{ROUND69_SOURCE_ROUND_PATH}`",
        "- large_sector: `BATTERY_EV_GREEN`",
        "- loop: `R3 Loop 3 / v3.0`",
        f"- target_count: {summary['target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- structural_success_count: {summary['structural_success_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- cyclical_success_count: {summary['cyclical_success_count']}",
        f"- failed_rerating_count: {summary['failed_rerating_count']}",
        f"- stage4b_case_count: {summary['stage4b_case_count']}",
        f"- stage4c_case_count: {summary['stage4c_case_count']}",
        f"- green_possible_count: {summary['green_possible_count']}",
        f"- watch_yellow_first_count: {summary['watch_yellow_first_count']}",
        f"- redteam_first_count: {summary['redteam_first_count']}",
        f"- gate_only_target_count: {summary['gate_only_target_count']}",
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "",
        "- R3 Loop 3 says EV growth and durable FCF are different things.",
        "- Example: an ESS LFP contract with value, duration, customer, and GWh can be Stage 2 evidence.",
        "- Example: EV CAPA becomes 4C when plants idle or contracts are cancelled.",
        "- Example: waste treatment can be Green-capable when permits, processing volume, and recurring FCF are proven.",
        "- Example: battery recycling needs SOH validation before second-life economics can be trusted.",
    ]
    return "\n".join(lines) + "\n"


def render_round69_green_guardrail_markdown() -> str:
    lines = [
        "# Round-69 R3 Loop-3 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Loop-3 penalties |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND69_SCORE_TARGETS:
        lines.append(
            "| "
            f"`{target.target_id}` | {target.posture.value} | "
            f"{', '.join(target.green_conditions) or 'not_applicable'} | {', '.join(target.loop3_penalty_axes)} |"
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not apply R3 Loop-3 v3.0 weights to production scoring yet.",
            "- Do not treat EV growth, ESS, recycling, hydrogen, solar, wind, or lithium labels as Green evidence by themselves.",
            "- Do not invent contract value, customer, duration, GWh, margin, utilization, recovery volume, SOH, stage prices, or FCF.",
            "- Treat plant idle, contract cancellation, customs detention, wind impairment, lithium supply rebound, EV fire, and SOH opacity as RedTeam fields.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round69_risk_overlay_markdown() -> str:
    lines = [
        "# Round-69 R3 Loop-3 Risk Overlays",
        "",
        "- `EV_CAPA_FALSE_GREEN`: CAPA expansion exists, but demand slowdown, plant idle, layoff, or contract cancellation breaks the thesis.",
        "- `ESS_CONTRACT_ALIGNED`: ESS value, duration, customer, GWh, production route, and later margin/FCF are visible.",
        "- `ESS_SHIFT_BUT_EV_OVERHANG`: ESS transition exists, but EV slowdown or idle plant still weighs on the path.",
        "- `RECYCLING_SECOND_LIFE_RISK`: recycling or second-life story ignores SOH, residual capacity, and grading cost.",
        "- `SOLAR_POLICY_SUPPLYCHAIN_4C`: US manufacturing/subsidy narrative breaks on customs, UFLPA, tariff, FEOC, or component detention.",
        "- `WIND_PROJECT_IMPAIRMENT_4C`: PPA/policy narrative breaks on foundation cost, financing cost, delay, or impairment.",
        "- `LITHIUM_CYCLICAL_SUCCESS_OR_FAILURE`: lithium price and ESS demand are cycle signals unless FCF/offtake are durable.",
        "- `EV_FIRE_REGULATORY_OVERLAY`: fire, certification, supplier disclosure, recall, parking/charging regulation, or insurance cost blocks unsafe Green.",
        "",
        "Simple example: `ESS 전환` is useful evidence. It is not Green if there is no contract value, margin, utilization, or FCF.",
    ]
    return "\n".join(lines) + "\n"


def render_round69_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-69 R3 Loop-3 Price Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign stage dates from source evidence only.",
        "2. Store stage-date close prices from official price data.",
        "3. Calculate MFE_30D / 90D / 180D / 1Y / 2Y.",
        "4. Calculate MAE_30D / 90D / 180D / 1Y.",
        "5. Compare EV demand, ESS contracts, factory utilization, CAPEX, mineral prices, subsidy/tariff, fire/certification, and SOH events with price path.",
        "6. Mark plant idle, contract cancellation, customs detention, wind impairment, lithium crash, EV fire regulation, and SOH opacity explicitly.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | target | stage marker | check |",
        "| --- | --- | --- | --- |",
    ]
    for row in round69_case_candidate_rows():
        stage_date = row["stage4c_date"] or row["stage4b_date"] or row["stage3_date"] or row["stage2_date"] or row["stage1_date"] or "undated"
        lines.append(f"| `{row['case_id']}` | `{row['target_id']}` | {stage_date} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `ess_contract_aligned`: contract value, duration, customer, GWh, ESS use case, and later price/EPS path align.",
            "- `ev_capa_false_green_plus_ess_shift_watch`: EV CAPA is broken, while ESS conversion remains only Watch.",
            "- `recycling_plus_storage_structural_reference`: recycling, recovered metals, ESS/grid services, and customers connect.",
            "- `solar_policy_supplychain_4c`: policy/subsidy story failed because customs, UFLPA, tariff, or component supply broke production.",
            "- `wind_project_impairment_4c`: policy/PPA story failed because project economics broke.",
            "- `battery_health_transparency_redteam`: SOH and residual-capacity opacity blocks unsafe second-life/recycling Green.",
        ]
    )
    return "\n".join(lines) + "\n"


def _score_price_alignment(candidate: Round69CaseCandidate) -> str:
    if "value_missing" in candidate.alignment_hint or "overhang" in candidate.alignment_hint:
        return "evidence_good_but_price_failed"
    if candidate.case_type in {"structural_success", "success_candidate", "cyclical_success"}:
        return "aligned"
    if candidate.case_type in {"4b_watch", "overheat"}:
        return "price_moved_without_evidence"
    if candidate.case_type == "4c_thesis_break":
        return "false_positive_score"
    if candidate.case_type == "failed_rerating":
        return "evidence_good_but_price_failed"
    return "false_positive_score"


def _rerating_result(candidate: Round69CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "true_rerating"
    if candidate.case_type == "cyclical_success":
        return "cyclical_rerating"
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    if candidate.case_type in {"4b_watch", "overheat"}:
        return "theme_overheat"
    return "unknown" if candidate.case_type == "success_candidate" else "no_rerating"


def _score_weight_hint(target: Round69ScoreTarget) -> dict[str, float]:
    weights = target.score_weight.as_dict()
    return {
        "eps_fcf": _numeric_weight(weights["eps_fcf"]),
        "visibility": _numeric_weight(weights["structural_visibility"]),
        "bottleneck": _numeric_weight(weights["bottleneck_pricing"]),
        "mispricing": _numeric_weight(weights["market_mispricing"]),
        "valuation": _numeric_weight(weights["valuation"]),
        "capital_allocation": _numeric_weight(weights["capital_allocation"]),
    }


def _numeric_weight(value: int | str) -> float:
    if isinstance(value, int):
        return float(value)
    return 0.0


def _write_case_jsonl(records: Iterable[E2RCaseRecord], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(record.as_dict(), ensure_ascii=False, sort_keys=True) for record in records]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return path


def _write_rows(rows: Iterable[Mapping[str, str]], path: Path) -> Path:
    rows_tuple = tuple(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows_tuple:
        path.write_text("", encoding="utf-8")
        return path
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows_tuple[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows_tuple)
    return path
