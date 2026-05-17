"""Round-54 R1 Loop-2 industrial orders and infrastructure pack.

Round 54 restarts the sector loop at R1. It keeps the first R1 map intact but
adds stronger price-path, capital-allocation, project-delay, 4B, and 4C
validation around orders, backlog, transformers, defense, shipbuilding, rail,
nuclear, reconstruction, and factory automation.

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


ROUND54_SOURCE_ROUND_PATH = "docs/round/round_54.md"
ROUND54_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round54_r1_loop2_industrial_infra"
ROUND54_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r1_loop2_round54.jsonl"
ROUND54_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round54_r1_loop2_v2.csv"


@dataclass(frozen=True)
class Round54ScoreWeightDraft:
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
class Round54ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round54ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    loop2_penalty_axes: tuple[str, ...]
    normalization_point: str

    @property
    def large_sector(self) -> Round10LargeSector:
        return Round10LargeSector.INDUSTRIAL_ORDERS_INFRA

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round54CaseCandidate:
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


ROUND54_SCORE_TARGETS: tuple[Round54ScoreTarget, ...] = (
    Round54ScoreTarget(
        "GRID_TRANSFORMER_SHORTAGE",
        E2RArchetype.GRID_TRANSFORMER_SHORTAGE,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round54ScoreWeightDraft(23, 25, 23, 12, 12, 1, 5),
        ("ai_data_center_power_demand", "ev_grid_demand", "grid_modernization", "lead_time_extended"),
        ("supply_contract", "contract_value_to_sales", "backlog_growth", "op_eps_revision"),
        ("fy1_fy2_fy3_revision", "long_lead_time", "price_increase", "old_industrial_frame_rerating"),
        ("sector_wide_ai_grid_consensus", "valuation_band_expansion", "capacity_addition_news"),
        ("data_center_project_delay", "new_order_slowdown", "capa_normalization", "low_margin_contract"),
        ("contract_quality", "lead_time_extended", "pricing_power", "backlog_growth", "op_eps_revision"),
        ("capa_normalization", "data_center_delay", "low_margin_contract", "new_order_growth_slowdown"),
        ("data_center_delay", "project_delay", "capa_normalization", "low_margin_contract"),
        "Loop 2 raises transformer EPS/FCF weight because demand, price, lead time, and Korean contract references are all visible.",
    ),
    Round54ScoreTarget(
        "AI_DATA_CENTER_POWER_EQUIPMENT",
        E2RArchetype.AI_DATA_CENTER_POWER_EQUIPMENT,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round54ScoreWeightDraft(21, 22, 18, 13, 12, 0, 5),
        ("ups_pdu_switchgear_keyword", "modular_power", "data_center_internal_power_demand"),
        ("confirmed_booking", "delivery_schedule", "op_eps_revision", "bookings_growth"),
        ("backlog_growth", "revenue_conversion", "op_margin_improvement", "customer_visible"),
        ("ai_power_equipment_theme_crowded", "ytd_return_extreme", "capacity_addition_news"),
        ("bookings_slowdown", "project_delay", "low_margin_project", "data_center_capex_delay"),
        ("bookings_growth", "delivery_schedule", "backlog_growth", "op_margin_improvement"),
        ("bookings_slowdown", "low_margin_project", "data_center_delay"),
        ("bookings_slowdown", "project_delay", "low_margin_project"),
        "Data-center power equipment is Green-capable only when bookings convert to revenue and OP, not from AI tags alone.",
    ),
    Round54ScoreTarget(
        "CONTRACT_BACKLOG_INDUSTRIAL",
        E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round54ScoreWeightDraft(20, 24, 18, 13, 12, 1, 5),
        ("supply_contract_news", "trading_value_breakout", "backlog_keyword"),
        ("contract_amount_to_sales", "contract_duration", "delivery_schedule", "op_eps_revision"),
        ("multi_year_backlog", "margin_visible", "capacity_constraint", "fy1_fy2_revision"),
        ("crowded_order_story", "target_price_cluster", "new_order_growth_slowdown"),
        ("contract_cancelled", "delivery_delay", "margin_miss", "customer_credit_issue"),
        ("contract_value", "contract_duration", "delivery_schedule", "margin_visible", "op_eps_revision"),
        ("contract_quality_unclear", "delivery_delay", "margin_uncertainty"),
        ("contract_quality_unclear", "delivery_delay", "margin_uncertainty"),
        "Generic backlog needs contract size, duration, delivery, margin, and EPS evidence together.",
    ),
    Round54ScoreTarget(
        "DEFENSE_GOVERNMENT_BACKLOG",
        E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round54ScoreWeightDraft(20, 24, 17, 14, 14, 3, 5),
        ("nato_rearmament", "defense_export_news", "government_customer"),
        ("official_contract", "multi_year_delivery", "order_backlog_growth", "op_eps_revision"),
        ("government_backlog_to_sales", "delivery_visibility", "opm_improvement", "export_mix_growth"),
        ("defense_rerating_crowded", "capital_raise_after_runup", "valuation_band_full"),
        ("delivery_delay", "cost_overrun", "export_permit_issue", "dilution_shock", "contract_cancelled"),
        ("government_customer", "multi_year_contract", "delivery_schedule", "backlog_growth", "opm_improvement"),
        ("delivery_delay", "cost_overrun", "export_permit_issue", "dilution"),
        ("capital_allocation_shock", "dilution", "delivery_delay", "export_permit_issue"),
        "Loop 2 keeps defense Green-capable but makes dilution and unclear overseas expansion funding first-class guardrails.",
    ),
    Round54ScoreTarget(
        "DEFENSE_TECH_AUTONOMOUS_SYSTEMS",
        E2RArchetype.DEFENSE_TECH_AUTONOMOUS_SYSTEMS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round54ScoreWeightDraft(20, 22, 15, 15, 14, 2, 5),
        ("autonomous_weapon_keyword", "low_cost_munition_framework", "prototype_program"),
        ("framework_agreement", "evaluation_schedule", "procurement_quantity_hint"),
        ("program_of_record", "mass_procurement", "production_capacity", "eps_conversion"),
        ("prototype_theme_crowded", "defense_ai_valuation_jump"),
        ("procurement_delay", "program_cancelled", "valuation_overheat", "export_control"),
        ("framework_to_order_conversion", "production_capacity", "customer_budget", "eps_conversion"),
        ("procurement_delay", "valuation_overheat", "prototype_only", "program_cancelled"),
        ("prototype_only", "procurement_delay", "valuation_overheat"),
        "Framework and prototypes are Watch until they become funded procurement and revenue.",
    ),
    Round54ScoreTarget(
        "DEFENSE_DRONE_COUNTER_UAS",
        E2RArchetype.DEFENSE_DRONE_COUNTER_UAS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round54ScoreWeightDraft(20, 22, 14, 14, 13, 3, 5),
        ("drone_or_counter_uas_keyword", "loitering_munition", "directed_energy_keyword"),
        ("military_order", "delivery_schedule", "production_capacity"),
        ("repeat_procurement", "export_customer", "margin_visible"),
        ("drone_theme_crowding", "mna_dilution"),
        ("export_control", "procurement_delay", "production_failure", "dilution"),
        ("actual_order", "delivery_schedule", "production_capacity", "repeat_procurement"),
        ("mna_dilution", "export_control", "prototype_only"),
        ("prototype_only", "mna_dilution", "export_control"),
        "Drone and counter-UAS stories need production capacity and repeat procurement.",
    ),
    Round54ScoreTarget(
        "DEFENSE_AI_SOFTWARE_INTELLIGENCE",
        E2RArchetype.DEFENSE_AI_SOFTWARE_INTELLIGENCE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round54ScoreWeightDraft(19, 21, 10, 15, 14, 0, 5),
        ("military_ai_software", "command_control_software", "prototype_contract"),
        ("prototype_contract", "government_customer", "deployment_schedule"),
        ("program_of_record", "recurring_license", "gross_margin_visible"),
        ("defense_ai_software_crowded", "multiple_expansion_without_arr"),
        ("prototype_not_renewed", "political_ethics_risk", "budget_cycle_cut"),
        ("government_customer", "deployment_schedule", "recurring_license", "gross_margin_visible"),
        ("prototype_stage", "political_ethics_risk", "budget_cycle"),
        ("prototype_stage", "budget_cycle", "political_ethics_risk"),
        "Defense AI software must separate prototype revenue from repeat software economics.",
    ),
    Round54ScoreTarget(
        "SHIPBUILDING_OFFSHORE_BACKLOG",
        E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round54ScoreWeightDraft(20, 22, 18, 13, 13, 1, 5),
        ("newbuilding_price_up", "ship_order_recovery", "lng_or_offshore_order", "naval_mro_option"),
        ("large_order", "low_margin_backlog_rolloff", "high_margin_delivery_start", "op_eps_revision"),
        ("backlog_quality_improves", "fy2_fy3_margin_recognition", "cost_pressure_controlled"),
        ("shipbuilder_group_rally", "newbuilding_price_narrative_crowded", "mro_option_crowded", "block_sale_overhang"),
        ("steel_plate_cost_spike", "labor_cost_spike", "order_slowdown", "contract_cancelled", "delivery_delay"),
        ("newbuilding_price_up", "low_margin_backlog_rolloff", "high_margin_delivery_start", "op_eps_revision"),
        ("low_margin_backlog", "steel_plate_cost", "labor_cost", "block_sale_overhang"),
        ("low_margin_backlog", "steel_plate_cost", "labor_cost", "block_sale_overhang"),
        "Shipbuilding needs order quality, newbuilding prices, margin recognition, and overhang checks.",
    ),
    Round54ScoreTarget(
        "RAIL_INFRASTRUCTURE",
        E2RArchetype.RAIL_INFRASTRUCTURE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round54ScoreWeightDraft(20, 23, 12, 14, 12, 1, 5),
        ("rail_order_news", "foreign_rail_investment", "urban_or_high_speed_rail_policy"),
        ("official_contract", "contract_amount_to_sales", "delivery_schedule"),
        ("delivery_visibility", "margin_visible", "op_eps_revision", "financing_risk_low"),
        ("rail_order_expectation_fully_priced",),
        ("project_delay", "financing_failure", "margin_miss", "contract_cancelled"),
        ("official_contract", "contract_amount_to_sales", "delivery_schedule", "margin_visible", "financing_secured"),
        ("project_delay", "margin_uncertainty", "financing"),
        ("project_delay", "margin_uncertainty", "financing"),
        "Rail contracts can reach Stage 2, but Green needs margin, delivery, and financing evidence.",
    ),
    Round54ScoreTarget(
        "NUCLEAR_SMR_GRID_POLICY",
        E2RArchetype.NUCLEAR_SMR_GRID_POLICY,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round54ScoreWeightDraft(18, 22, 10, 14, 12, 2, 5),
        ("nuclear_policy", "ai_power_demand", "ppa_or_preferred_bidder_news", "smr_news"),
        ("ppa_or_signed_contract", "permitting_visible", "supplier_revenue_path"),
        ("legal_risk_low", "financing_visible", "fy2_fy3_revenue_visibility", "ppa_price_visible"),
        ("nuclear_theme_rally", "policy_premium_crowded", "smr_story_crowded"),
        ("legal_injunction", "project_cancelled", "cost_overrun", "financing_failed", "customer_subscription_failed"),
        ("ppa_or_signed_contract", "permitting", "financing", "supplier_revenue_path", "ppa_price_visible"),
        ("legal_delay", "cost_overrun", "financing_failed", "policy_headline_only", "customer_subscription_failed"),
        ("cost_overrun", "financing_failed", "legal_delay", "customer_subscription_failed"),
        "Existing nuclear PPA is stronger evidence than SMR policy narrative; SMR needs cost, customer, permit, and financing proof.",
    ),
    Round54ScoreTarget(
        "GEOPOLITICAL_RECONSTRUCTION",
        E2RArchetype.GEOPOLITICAL_RECONSTRUCTION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round54ScoreWeightDraft(10, 8, 8, 10, 7, 0, 4),
        ("reconstruction_policy", "neom_or_ukraine_theme", "mou_or_bid_news"),
        ("binding_contract", "revenue_schedule", "financing_visible"),
        ("actual_delivery_and_margin", "eps_conversion"),
        ("policy_event_crowded", "event_premium_fades"),
        ("no_contract", "project_delay", "financing_failure", "policy_reversal"),
        ("binding_contract", "revenue_schedule", "financing_visible", "margin_visible"),
        ("actual_contract_missing", "policy_event_only", "mou_only"),
        ("policy_to_contract_failed", "financing_failure", "mou_only"),
        "Reconstruction and Neom-style themes remain Event/Watch before binding contracts and revenue schedules.",
    ),
    Round54ScoreTarget(
        "SMART_FACTORY_AUTOMATION",
        E2RArchetype.SMART_FACTORY_AUTOMATION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round54ScoreWeightDraft(18, 16, 8, 12, 10, 0, 5),
        ("smart_factory_keyword", "automation_order", "factory_ai_keyword"),
        ("actual_order", "installed_base", "recurring_maintenance_or_software"),
        ("revenue_conversion", "opm_improvement", "customer_diversification"),
        ("automation_theme_crowded",),
        ("mou_or_poc_only", "customer_capex_delay", "no_revenue_conversion"),
        ("actual_order", "installed_base", "recurring_revenue", "opm_improvement"),
        ("mou_only", "poc_only", "revenue_conversion_failure"),
        ("mou_only", "poc_only", "customer_capex_delay"),
        "Smart factory stories need order-to-revenue conversion; PoC and MOU stay Watch.",
    ),
)


ROUND54_CASE_CANDIDATES: tuple[Round54CaseCandidate, ...] = (
    Round54CaseCandidate(
        "us_transformer_shortage_korea_import_case",
        "GRID_TRANSFORMER_SHORTAGE",
        "POWER_TRANSFORMER_IMPORT",
        "US power transformer shortage / Korean import reference",
        "GLOBAL",
        "success_candidate",
        date(2026, 5, 11),
        date(2026, 5, 11),
        None,
        None,
        None,
        ("gsu_transformer_demand_growth", "substation_transformer_demand_growth", "lead_time_four_years", "price_up_80pct", "korea_import_slot"),
        ("data_center_delay", "capa_normalization", "tariff_cost_spike"),
        "structural_shortage_candidate_needs_company_price_backfill",
        "needs_price_backfill",
        ("round_54.md Reuters transformer shortage import/factory slot reference",),
        "Transformer shortage is R1 Loop-2 top Green-capable evidence, but company-specific MFE/MAE and EPS revisions must be backfilled.",
        (E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,),
    ),
    Round54CaseCandidate(
        "ls_electric_525kv_datacenter_transformer_case",
        "GRID_TRANSFORMER_SHORTAGE",
        "010120",
        "LS ELECTRIC 525kV data-center transformer contract",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("525kv_transformer_contract", "us_utility_counterparty", "data_center_delivery_2027_2029", "contract_value_312m_usd"),
        ("exact_contract_date_needed", "margin_unverified", "capa_normalization"),
        "contract_quality_aligned_but_exact_stage_date_needs_backfill",
        "needs_contract_date_backfill",
        ("round_54.md Reuters LS Electric 525kV transformer contract reference",),
        "The month-level contract reference is strong, but exact contract date and margin data are not invented.",
        (E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,),
    ),
    Round54CaseCandidate(
        "ge_vernova_data_center_orders_case",
        "AI_DATA_CENTER_POWER_EQUIPMENT",
        "GEV",
        "GE Vernova data-center power orders",
        "US",
        "4b_watch",
        date(2026, 4, 22),
        date(2026, 4, 22),
        None,
        date(2026, 4, 22),
        None,
        ("orders_up_71pct", "backlog_163b_usd", "electrification_revenue_growth", "data_center_orders", "event_day_price_up_15pct"),
        ("ytd_return_70pct", "crowded_ai_power_equipment", "bookings_slowdown_risk"),
        "aligned_plus_4b_watch",
        "needs_price_backfill",
        ("round_54.md WSJ GE Vernova orders/backlog reference",),
        "Orders/backlog and price reaction align, but 70% YTD move requires 4B-watch.",
        (E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE, E2RArchetype.CROWDED_RERATING_4B_WATCH),
    ),
    Round54CaseCandidate(
        "hanwha_aerospace_romania_k9_case",
        "DEFENSE_GOVERNMENT_BACKLOG",
        "012450",
        "한화에어로스페이스 루마니아 K9 계약",
        "KR",
        "structural_success",
        None,
        date(2024, 7, 9),
        None,
        None,
        None,
        ("romania_k9_contract", "k10_ammunition_vehicle", "contract_1bn_usd", "delivery_to_2029", "backlog_growth", "event_day_price_up"),
        ("delivery_delay", "cost_overrun", "dilution"),
        "defense_backlog_aligned_candidate",
        "needs_price_backfill",
        ("round_54.md Reuters Romania K9 contract reference",),
        "Government customer, multi-year delivery, backlog growth, and event-day price reaction align; 180D/1Y/2Y price path still needs backfill.",
        (E2RArchetype.STRUCTURAL_SUCCESS_ALIGNED,),
    ),
    Round54CaseCandidate(
        "hanwha_aerospace_europe_sales_case",
        "DEFENSE_GOVERNMENT_BACKLOG",
        "012450",
        "한화에어로스페이스 유럽 지상무기 매출 visibility",
        "KR",
        "success_candidate",
        None,
        date(2024, 10, 7),
        None,
        None,
        None,
        ("europe_land_arms_sales_double_by_2027", "poland_contracts", "romania_contract", "local_production_preference", "backlog_10x_since_2020"),
        ("localization_cost", "delivery_delay", "dilution"),
        "multi_year_visibility_candidate",
        "needs_price_backfill",
        ("round_54.md Reuters Europe land arms sales visibility reference",),
        "Regional repeat demand and local production improve visibility beyond a one-off contract.",
        (E2RArchetype.STRUCTURAL_SUCCESS_ALIGNED,),
    ),
    Round54CaseCandidate(
        "hanwha_aerospace_dilution_case",
        "DEFENSE_GOVERNMENT_BACKLOG",
        "012450",
        "한화에어로스페이스 대규모 자본조달 리스크",
        "KR",
        "failed_rerating",
        date(2025, 3, 27),
        date(2025, 3, 27),
        None,
        date(2025, 3, 27),
        None,
        ("share_issuance_plan", "overseas_expansion_capex", "drone_engine_development"),
        ("large_equity_issuance", "dilution", "use_of_proceeds_unclear", "event_day_price_down_13pct"),
        "capital_allocation_shock_4b_watch",
        "needs_price_backfill",
        ("round_54.md FT/Reuters Hanwha share sale reference",),
        "Strong defense backlog can be hit by dilution and unclear capital allocation.",
        (E2RArchetype.CROWDED_RERATING_4B_WATCH, E2RArchetype.LEVERAGE_FCF_BREAKDOWN),
    ),
    Round54CaseCandidate(
        "hyundai_rotem_morocco_rail_case",
        "RAIL_INFRASTRUCTURE",
        "064350",
        "현대로템 모로코 철도 수주",
        "KR",
        "success_candidate",
        None,
        date(2025, 2, 26),
        None,
        None,
        None,
        ("morocco_oncf_contract", "large_rail_order", "contract_1_54b_usd", "largest_rail_order", "delivery_schedule_needed"),
        ("margin_uncertainty", "financing", "project_delay"),
        "rail_infrastructure_stage2_candidate",
        "needs_price_backfill",
        ("round_54.md Reuters Hyundai Rotem Morocco rail order reference",),
        "A large signed rail order is Stage-2 style evidence; margin, delivery schedule, financing, and MFE need backfill.",
        (E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,),
    ),
    Round54CaseCandidate(
        "korean_shipbuilder_contract_rally_case",
        "SHIPBUILDING_OFFSHORE_BACKLOG",
        "KR_SHIPBUILDERS",
        "한국 조선주 수주·선가 랠리",
        "KR",
        "cyclical_success",
        None,
        None,
        None,
        None,
        None,
        ("contract_wins", "newbuilding_price_index_up", "korea_order_share_recovery", "group_price_reaction"),
        ("low_margin_backlog", "steel_plate_cost", "labor_cost", "order_slowdown"),
        "shipbuilding_price_aligned_candidate",
        "needs_source_date_backfill",
        ("round_54.md WSJ Korean shipbuilder contract rally reference",),
        "Shipbuilding showed strong price reaction, but structural Green still depends on backlog quality and margin recognition.",
        (E2RArchetype.CYCLICAL_SUCCESS,),
    ),
    Round54CaseCandidate(
        "hanwha_ocean_mro_rerating_case",
        "SHIPBUILDING_OFFSHORE_BACKLOG",
        "042660",
        "한화오션 MRO 기대 리레이팅",
        "KR",
        "4b_watch",
        date(2025, 4, 28),
        date(2025, 4, 28),
        None,
        date(2025, 4, 28),
        None,
        ("shipbuilding_defense_mro_option", "philadelphia_shipyard", "us_navy_mro_expectation", "price_up_139pct_ytd"),
        ("kdb_block_sale_overhang", "valuation_after_rapid_rise", "mro_contract_unverified"),
        "shipbuilding_defense_mro_success_candidate_plus_4b_watch",
        "needs_price_backfill",
        ("round_54.md Reuters Hanwha Ocean KDB stake sale/MRO reference",),
        "MRO can change the valuation frame, but +139% YTD plus KDB overhang makes 4B-watch mandatory.",
        (E2RArchetype.CROWDED_RERATING_4B_WATCH,),
    ),
    Round54CaseCandidate(
        "meta_constellation_nuclear_ppa_case",
        "NUCLEAR_SMR_GRID_POLICY",
        "CEG",
        "Meta-Constellation nuclear PPA",
        "US",
        "success_candidate",
        None,
        date(2025, 6, 3),
        None,
        None,
        None,
        ("twenty_year_nuclear_ppa", "ai_data_center_power_demand", "carbon_free_power_visibility", "premarket_price_up_13_4pct"),
        ("ppa_price_unverified", "regulatory_risk", "korea_equipment_mapping_needed"),
        "nuclear_ppa_aligned_reference",
        "needs_price_backfill",
        ("round_54.md Reuters Meta Constellation PPA reference",),
        "Existing nuclear PPA is stronger than SMR policy talk, but Korean equipment mapping needs direct contract evidence.",
        (E2RArchetype.NUCLEAR_SMR_GRID_POLICY,),
    ),
    Round54CaseCandidate(
        "nuscale_cfpp_cancel_case",
        "NUCLEAR_SMR_GRID_POLICY",
        "SMR",
        "NuScale CFPP cancellation",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2023, 11, 1),
        ("smr_project", "policy_theme", "customer_subscription_attempt"),
        ("cost_overrun", "customer_subscription_failure", "financing_failure", "project_cancelled", "staff_reduction"),
        "smr_hard_4c",
        "needs_price_backfill",
        ("round_54.md NuScale CFPP cancellation reference",),
        "SMR policy narrative breaks when cost, financing, and customer subscription fail.",
        (E2RArchetype.THESIS_BREAK_4C,),
    ),
    Round54CaseCandidate(
        "data_center_delay_transformer_soft_4c_case",
        "GRID_TRANSFORMER_SHORTAGE",
        "DATA_CENTER_DELAY",
        "데이터센터 지연 전력설비 soft 4C reference",
        "GLOBAL",
        "4c_thesis_break",
        date(2026, 2, 24),
        None,
        None,
        None,
        date(2026, 2, 24),
        ("ai_data_center_demand", "transformer_supply_delay", "grid_interconnection_delay"),
        ("data_center_project_cancelled", "local_opposition", "energy_shortage", "tariff_cost_spike", "investor_ai_bubble_concern"),
        "data_center_delay_transformer_soft_4c_overlay",
        "needs_price_backfill",
        ("round_54.md Guardian data-center delay reference",),
        "AI data-center demand does not automatically make every transformer order Green when projects are delayed or cancelled.",
        (E2RArchetype.THESIS_BREAK_4C,),
    ),
)


ROUND54_PRICE_FIELDS: tuple[str, ...] = (
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
    "peak_date",
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
    "below_stage2_price_flag",
    "below_stage3_price_flag",
    "contract_value",
    "contract_value_to_sales",
    "contract_duration_months",
    "contract_start_date",
    "contract_end_date",
    "counterparty",
    "delivery_schedule",
    "backlog_growth",
    "backlog_to_revenue",
    "new_order_growth",
    "book_to_bill",
    "gross_margin_change",
    "op_margin_change",
    "eps_revision_1q",
    "eps_revision_1y",
    "op_revision_1q",
    "op_revision_1y",
    "capex_amount",
    "dilution_flag",
    "share_issuance_amount",
    "use_of_proceeds_clarity",
    "regulator_revision_request_flag",
    "project_delay_flag",
    "data_center_delay_flag",
    "local_opposition_flag",
    "grid_interconnection_delay_flag",
    "financing_secured_flag",
    "ship_newbuilding_price_index",
    "low_margin_backlog_flag",
    "steel_plate_cost_change",
    "labor_cost_change",
    "naval_mro_contract_flag",
    "block_sale_overhang_flag",
    "nuclear_ppa_flag",
    "smr_flag",
    "cost_overrun_flag",
    "licensing_risk_flag",
    "customer_subscription_flag",
    "score_price_alignment",
    "price_validation_status",
    "review_notes",
)


def target_for(target_id: str) -> Round54ScoreTarget | None:
    for target in ROUND54_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round54_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND54_CASE_CANDIDATES:
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
                f"Round54 R1 Loop-2 case for {candidate.target_id}; "
                "price-path, project-delay, capital-allocation, and 4B/4C evidence remain calibration-only."
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
                "require_contract_quality_delivery_margin_eps_revision_for_green",
                "do_not_invent_contract_dates_prices_or_margins",
                "project_delay_capital_allocation_shock_capa_normalization_are_loop2_penalties",
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


def round54_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND54_SCORE_TARGETS:
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
                "loop2_penalty_axes": "|".join(target.loop2_penalty_axes),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round54_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND54_CASE_CANDIDATES:
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


def round54_stage_date_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "target_id": target.target_id,
            "stage1": "|".join(target.stage1_signals),
            "stage2": "|".join(target.stage2_signals),
            "stage3": "|".join(target.stage3_conditions),
            "stage4b": "|".join(target.stage4b_conditions),
            "stage4c": "|".join(target.stage4c_conditions),
            "loop2_penalty_axes": "|".join(target.loop2_penalty_axes),
            "production_scoring_changed": "false",
        }
        for target in ROUND54_SCORE_TARGETS
    )


def round54_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round54_backfill": "true"} for field in ROUND54_PRICE_FIELDS)


def round54_summary() -> dict[str, int | bool]:
    records = round54_case_records()
    return {
        "target_count": len(ROUND54_SCORE_TARGETS),
        "case_candidate_count": len(records),
        "structural_success_count": sum(1 for record in records if record.case_type == "structural_success"),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for record in records if record.case_type == "cyclical_success"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND54_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND54_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND54_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round54_r1_loop2_reports(
    *,
    output_directory: str | Path = ROUND54_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND54_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND54_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round54_r1_loop2_industrial_infra_summary.md",
        "case_matrix": output / "round54_r1_loop2_case_matrix.csv",
        "stage_date_plan": output / "round54_r1_loop2_stage_date_plan.csv",
        "green_guardrails": output / "round54_r1_loop2_green_guardrails.md",
        "loop2_risk_overlays": output / "round54_r1_loop2_risk_overlays.md",
        "price_validation_plan": output / "round54_r1_loop2_price_validation_plan.md",
        "price_fields": output / "round54_r1_loop2_price_fields.csv",
    }
    _write_case_jsonl(round54_case_records(), cases)
    _write_rows(round54_score_profile_rows(), score_profiles)
    _write_rows(round54_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round54_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round54_price_field_rows(), paths["price_fields"])
    paths["summary"].write_text(render_round54_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round54_green_guardrail_markdown(), encoding="utf-8")
    paths["loop2_risk_overlays"].write_text(render_round54_loop2_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round54_price_validation_plan_markdown(), encoding="utf-8")
    return paths


def render_round54_summary_markdown() -> str:
    summary = round54_summary()
    lines = [
        "# Round-54 R1 Loop-2 Industrial Orders / Infrastructure Summary",
        "",
        f"- source_round: `{ROUND54_SOURCE_ROUND_PATH}`",
        "- large_sector: `INDUSTRIAL_ORDERS_INFRA`",
        "- loop: `R1 Loop 2 / v2.0`",
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
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "",
        "- R1 Loop 2 keeps industrial orders Green-capable, but order headlines alone are still not enough.",
        "- Example: transformer shortage is strong only when contract value, duration, backlog, margin, EPS revision, and price path align.",
        "- Example: defense backlog can be strong, but large equity issuance or unclear overseas CAPEX can move the case into 4B/4C-watch.",
        "- Example: SMR policy narrative is weaker than an existing nuclear PPA because cost, customer subscription, permit, and financing risk remain open.",
    ]
    return "\n".join(lines) + "\n"


def render_round54_green_guardrail_markdown() -> str:
    lines = [
        "# Round-54 R1 Loop-2 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Loop-2 penalties |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND54_SCORE_TARGETS:
        lines.append(
            "| "
            f"`{target.target_id}` | {target.posture.value} | "
            f"{', '.join(target.green_conditions)} | {', '.join(target.loop2_penalty_axes)} |"
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not apply R1 Loop-2 v2.0 weights to production scoring yet.",
            "- Do not lower Stage 3-Green thresholds because R1 is Green-capable.",
            "- Do not treat MOU, policy expectation, prototype, or project headline as Green evidence.",
            "- Do not invent contract values, contract dates, delivery schedules, margins, or stage prices.",
            "- Treat project delay, capital-allocation shock, CAPA normalization, low-margin backlog, financing failure, and cost overrun as strong penalties.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round54_loop2_risk_overlay_markdown() -> str:
    lines = [
        "# Round-54 R1 Loop-2 Risk Overlays",
        "",
        "- `contract_quality_aligned`: contract amount, duration, delivery schedule, margin, EPS revision, and price rerating align.",
        "- `backlog_without_margin`: backlog exists but margin and EPS conversion are unclear.",
        "- `project_delay_risk`: data-center, rail, nuclear, reconstruction, or infrastructure demand exists but projects are delayed.",
        "- `capital_allocation_shock`: share issuance, unclear use of proceeds, or large overseas CAPEX dilutes the case.",
        "- `policy_to_contract_failed`: reconstruction, Neom, rail, or nuclear policy does not convert into funded contracts.",
        "- `crowded_rerating_4b`: a good structure is already broadly recognized and valuation/mispricing has compressed.",
        "",
        "Simple example: `as_of_date=2025-02-26` and a rail contract is announced. That can be Stage 2 evidence. It is not Stage 3-Green until margin, financing, delivery schedule, and OP/EPS path are visible as of that date.",
    ]
    return "\n".join(lines) + "\n"


def render_round54_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-54 R1 Loop-2 Price Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign stage dates from source evidence only.",
        "2. Store stage-date close prices from official price data.",
        "3. Calculate MFE_30D / 90D / 180D / 1Y / 2Y.",
        "4. Calculate MAE_30D / 90D / 180D / 1Y.",
        "5. Compare contract quality, backlog, margin, OP/EPS revision, and price path.",
        "6. Mark capital-allocation shock, project delay, CAPA normalization, and low-margin backlog explicitly.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | target | stage marker | check |",
        "| --- | --- | --- | --- |",
    ]
    for row in round54_case_candidate_rows():
        stage_date = row["stage4c_date"] or row["stage4b_date"] or row["stage3_date"] or row["stage2_date"] or row["stage1_date"] or "undated"
        lines.append(f"| `{row['case_id']}` | `{row['target_id']}` | {stage_date} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `contract_quality_aligned`: contract value/duration/delivery/margin/EPS and price path align.",
            "- `project_delay_risk`: demand exists but project execution threatens order growth.",
            "- `capital_allocation_shock`: backlog remains attractive but dilution or funding damages price path.",
            "- `policy_to_contract_failed`: policy/MOU does not become funded order or revenue.",
            "- `crowded_rerating_4b`: good structure but market recognition is already crowded.",
        ]
    )
    return "\n".join(lines) + "\n"


def _score_price_alignment(candidate: Round54CaseCandidate) -> str:
    if candidate.case_type in {"structural_success", "success_candidate", "cyclical_success"}:
        return "aligned"
    if candidate.case_type in {"event_premium", "overheat", "4b_watch"}:
        return "price_moved_without_evidence"
    if candidate.case_type == "failed_rerating" and "capital_allocation" in candidate.alignment_hint:
        return "evidence_good_but_price_failed"
    return "false_positive_score"


def _rerating_result(candidate: Round54CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "true_rerating"
    if candidate.case_type == "cyclical_success":
        return "cyclical_rerating"
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    if candidate.case_type == "4b_watch":
        return "theme_overheat"
    if candidate.case_type == "event_premium":
        return "event_premium"
    return "unknown" if candidate.case_type == "success_candidate" else "no_rerating"


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
        writer = csv.DictWriter(handle, fieldnames=tuple(rows_tuple[0].keys()))
        writer.writeheader()
        for row in rows_tuple:
            writer.writerow(dict(row))
    return path


__all__ = [
    "ROUND54_CASE_CANDIDATES",
    "ROUND54_DEFAULT_CASES_PATH",
    "ROUND54_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND54_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND54_PRICE_FIELDS",
    "ROUND54_SCORE_TARGETS",
    "Round54CaseCandidate",
    "Round54ScoreTarget",
    "Round54ScoreWeightDraft",
    "render_round54_green_guardrail_markdown",
    "render_round54_loop2_risk_overlay_markdown",
    "render_round54_price_validation_plan_markdown",
    "render_round54_summary_markdown",
    "round54_case_candidate_rows",
    "round54_case_records",
    "round54_price_field_rows",
    "round54_score_profile_rows",
    "round54_stage_date_rows",
    "round54_summary",
    "target_for",
    "write_round54_r1_loop2_reports",
]
