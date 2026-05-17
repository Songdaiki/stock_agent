"""Round-75 R9 Loop-3 mobility, transport, and leisure pack.

Round 75 tightens the Round-49 R9 pack. It separates auto value-up and
satellite-connectivity cases from airline, tourism, shipping, rental,
micromobility, and eVTOL cycle/event stories. Demand recovery, hybrid labels,
tourism policy, freight spikes, and partial eVTOL certification are not Stage 3
evidence unless OPM, FCF, capital return, unit economics, certification,
backlog, or recurring revenue are proven.

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


ROUND75_SOURCE_ROUND_PATH = "docs/round/round_75.md"
ROUND75_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round75_r9_loop3_mobility_transport_leisure"
ROUND75_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r9_loop3_round75.jsonl"
ROUND75_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round75_r9_loop3_v3.csv"


@dataclass(frozen=True)
class Round75ScoreWeightDraft:
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
class Round75ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round75ScoreWeightDraft
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
        return Round10LargeSector.MOBILITY_TRANSPORT_LEISURE

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round75CaseCandidate:
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


GATE_WEIGHT = Round75ScoreWeightDraft("gate", "gate", "gate", "gate", "gate", "gate", "gate")


ROUND75_SCORE_TARGETS: tuple[Round75ScoreTarget, ...] = (
    Round75ScoreTarget(
        "AUTO_MOBILITY_COMPLETED_VEHICLE",
        E2RArchetype.AUTO_MOBILITY_COMPLETED_VEHICLE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round75ScoreWeightDraft(20, 18, 10, 15, 17, 10, 5),
        ("hybrid_demand", "ev_slowdown_response", "shareholder_return_policy", "local_production_plan"),
        ("sales_target", "op_margin_target", "buyback_or_dividend", "fcf_margin", "roe_pbr_rerating"),
        ("durable_fcf", "high_margin_mix", "shareholder_return_execution", "old_auto_discount_removed"),
        ("valueup_narrative_crowded", "hybrid_story_fully_priced", "peak_margin_ignored"),
        ("tariff_hit", "op_margin_cut", "recall_cost", "peak_margin_reversal", "demand_slowdown"),
        ("hybrid_or_mix_improvement", "op_margin_target", "fcf_margin", "shareholder_return", "tariff_risk_low"),
        ("tariff", "op_margin_cut", "recall", "peak_margin", "local_production_capex"),
        ("tariff", "opm_cut", "recall", "peak_margin"),
        "Completed vehicles can be Watch-to-Green only when hybrid/mix, OPM, FCF, and capital return are source-backed.",
    ),
    Round75ScoreTarget(
        "AUTO_HYBRID_VALUEUP",
        E2RArchetype.AUTO_HYBRID_VALUEUP,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round75ScoreWeightDraft(21, 20, 11, 15, 17, 10, 5),
        ("ev_slowdown_response", "hybrid_lineup_expansion", "erev_strategy", "shareholder_return_policy"),
        ("sales_target", "op_margin_target", "buyback_or_dividend", "dividend_policy_change", "fcf_margin"),
        ("roe_fcf_persistent", "shareholder_return_execution", "hybrid_mix_margin", "pbr_per_frame_improves"),
        ("auto_valueup_narrative_crowded", "hybrid_margin_fully_priced"),
        ("tariff_hit", "op_margin_cut", "recall_cost", "peak_margin_reversal", "demand_slowdown"),
        ("hybrid_sales_growth", "op_margin_target", "fcf_margin", "shareholder_return_ratio", "tariff_risk_low"),
        ("tariff", "hybrid_capa", "quality_cost", "return_execution"),
        ("tariff", "hybrid_capa", "quality_cost", "return_execution"),
        "Auto hybrid value-up is Green-eligible only when hybrid mix, OPM, FCF, and returns align.",
    ),
    Round75ScoreTarget(
        "AUTO_MOBILITY_COMPONENTS",
        E2RArchetype.AUTO_MOBILITY_COMPONENTS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round75ScoreWeightDraft(20, 18, 11, 14, 14, 3, 5),
        ("hybrid_component_demand", "electronics_component", "lighting_or_adas_demand"),
        ("customer_delivery", "customer_diversification", "opm_improvement", "cost_pass_through"),
        ("high_value_mix", "repeat_program_visibility", "fcf_improvement", "quality_cost_low"),
        ("component_group_multiple_expansion",),
        ("customer_concentration", "raw_material_cost_spike", "quality_cost", "program_delay"),
        ("customer_delivery", "cost_pass_through", "customer_diversification", "op_eps_revision"),
        ("customer_concentration", "raw_material", "quality_cost", "bottleneck_normalization"),
        ("customer_concentration", "raw_material", "bottleneck_normalization"),
        "Auto components need customer diversification, cost pass-through, OPM, and repeat programs.",
    ),
    Round75ScoreTarget(
        "HYBRID_COMPONENT_BOTTLENECK",
        E2RArchetype.HYBRID_COMPONENT_BOTTLENECK,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round75ScoreWeightDraft(21, 19, 14, 14, 13, 2, 5),
        ("hybrid_wait_time", "motor_bottleneck", "inverter_bottleneck", "magnet_bottleneck"),
        ("customer_delivery", "hybrid_component_order", "capa_shortage", "opm_improvement"),
        ("high_value_hybrid_mix", "fcf_improvement", "cost_pass_through", "customer_delivery_visible"),
        ("hybrid_component_bottleneck_crowded",),
        ("capacity_normalization", "single_customer", "raw_material_cost_spike", "quality_cost"),
        ("hybrid_component_order", "customer_delivery", "opm_improvement", "cost_pass_through"),
        ("capacity_normalization", "single_customer", "raw_material", "quality_cost"),
        ("capacity_normalization", "single_customer", "raw_material"),
        "Hybrid bottleneck needs actual deliveries and margin, not just hybrid demand.",
    ),
    Round75ScoreTarget(
        "AUTO_COMPONENTS_EV_ADAS",
        E2RArchetype.AUTO_COMPONENTS_EV_ADAS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round75ScoreWeightDraft(18, 16, 9, 13, 11, 0, 5),
        ("adas_adoption", "sensor_or_camera_order", "ev_component_demand"),
        ("actual_adoption", "customer_diversification", "development_cost_control"),
        ("content_per_vehicle_growth", "multi_customer_program", "op_eps_revision"),
        ("adas_theme_crowded",),
        ("actual_adoption_missing", "customer_concentration", "development_cost", "program_delay"),
        ("actual_adoption", "customer_diversification", "op_eps_revision"),
        ("actual_adoption_missing", "customer_concentration", "development_cost"),
        ("actual_adoption", "development_cost", "single_customer"),
        "ADAS parts need actual adoption and customer diversification, not autonomy theme labels.",
    ),
    Round75ScoreTarget(
        "AUTONOMOUS_ROBOTAXI_DEPLOYMENT",
        E2RArchetype.AUTONOMOUS_ROBOTAXI_DEPLOYMENT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round75ScoreWeightDraft(17, 17, 10, 15, 10, 0, 6),
        ("robotaxi_partnership", "pilot_launch", "service_area_expansion", "autonomous_platform"),
        ("robotaxi_service_area", "robotaxi_fleet_size", "paid_ride_volume", "platform_integration"),
        ("unit_economics", "safety_record_clean", "insurance_liability_cost_stable", "vehicle_utilization"),
        ("robotaxi_scale_narrative_crowded",),
        ("safety_recall", "weather_handling_failure", "nhtsa_scrutiny", "service_suspension", "insurance_liability_cost"),
        ("paid_ride_volume", "vehicle_utilization", "safety_record_clean", "unit_economics"),
        ("safety_recall", "nhtsa_scrutiny", "weather_handling", "unit_economics"),
        ("safety", "nhtsa", "weather", "unit_economics"),
        "Robotaxi is Watch-to-Green only after deployment, paid rides, safety, and unit economics are proven.",
    ),
    Round75ScoreTarget(
        "TIRE_AUTO_COMPONENT_SPREAD",
        E2RArchetype.TIRE_AUTO_COMPONENT_SPREAD,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round75ScoreWeightDraft(17, 12, 12, 10, 9, 2, 5),
        ("tire_demand_recovery", "raw_material_spread", "replacement_market"),
        ("oe_re_mix", "north_america_demand_stable", "op_eps_revision", "fcf_margin"),
        ("spread_fcf_persistent", "replacement_demand_resilient", "china_competition_controlled"),
        ("spread_peak_ignored",),
        ("north_america_demand_slowdown", "replacement_market_weakness", "raw_material_spike", "tariff_hit", "fcf_guidance_cut"),
        ("oe_re_mix", "raw_material_spread", "op_eps_revision", "fcf_margin"),
        ("north_america_demand", "raw_material", "tariff", "fcf_guidance_cut"),
        ("north_america_demand", "raw_material", "tariff", "fcf"),
        "Tire Green is restricted; demand recovery must become margin and FCF.",
    ),
    Round75ScoreTarget(
        "AIRLINE_TRAVEL_CYCLE",
        E2RArchetype.AIRLINE_TRAVEL_CYCLE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round75ScoreWeightDraft(18, 14, 5, 12, 10, 2, 5),
        ("passenger_recovery", "cargo_rate", "airline_merger", "reopening_news"),
        ("revenue_op_improvement", "integration_synergy", "passenger_cargo_mix", "load_factor"),
        ("fcf_cost_stability", "fuel_fx_risk_low", "integration_cost_controlled"),
        ("integration_or_reopening_crowded", "cargo_cycle_ignored"),
        ("fuel_shock", "fx_loss", "integration_cost", "cargo_passenger_slowdown", "tariff_trade_uncertainty"),
        ("load_factor", "yield_or_margin", "fuel_fx_risk_low", "integration_cost_controlled"),
        ("fuel", "fx", "integration_cost", "cargo_cycle", "regulatory_condition"),
        ("fuel", "fx", "integration", "cargo_cycle"),
        "Airline recovery is Watch-first; traffic without margin is not Green evidence.",
    ),
    Round75ScoreTarget(
        "TRAVEL_LEISURE_REOPENING",
        E2RArchetype.TRAVEL_LEISURE_REOPENING,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round75ScoreWeightDraft(17, 13, 5, 12, 10, 1, 5),
        ("tourist_recovery", "hotel_occupancy", "leisure_reopening"),
        ("revpar_improvement", "op_leverage", "visitor_spend", "average_spend_per_visitor"),
        ("repeat_travel_spend", "occupancy_and_margin_visible", "revpar_persistent"),
        ("reopening_policy_crowded",),
        ("visitor_mix_weak", "occupancy_slowdown", "cost_inflation", "policy_event_only"),
        ("visitor_spend", "hotel_occupancy", "revpar", "opm_improvement"),
        ("tourist_mix", "policy_event_only", "cost_inflation", "occupancy_slowdown"),
        ("tourist_mix", "occupancy", "policy_event"),
        "Travel needs spend and operating leverage, not arrival headlines alone.",
    ),
    Round75ScoreTarget(
        "CASINO_DUTYFREE_TOURISM",
        E2RArchetype.CASINO_DUTYFREE_TOURISM,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round75ScoreWeightDraft(18, 13, 5, 12, 10, 2, 5),
        ("visa_policy", "china_group_tourism", "casino_dutyfree_recovery"),
        ("tourist_spend", "casino_drop_amount", "duty_free_sales", "hotel_occupancy", "vip_mix"),
        ("visitor_mix_diversified", "china_dependence_lower", "cashflow_margin_visible"),
        ("tourism_policy_rally_crowded", "spend_unverified_policy_rally"),
        ("drop_slowdown", "duty_free_asp_weak", "china_mix_weak", "capex_burden"),
        ("tourist_arrivals", "casino_drop_amount", "duty_free_sales", "opm_improvement"),
        ("china_dependence", "drop_amount", "duty_free_asp", "policy_event_only"),
        ("china_dependence", "drop_amount", "dutyfree_asp"),
        "Tourism policy is Stage 1 until actual spend, drop, ASP, and OPM are visible.",
    ),
    Round75ScoreTarget(
        "SHIPPING_FREIGHT_CYCLE",
        E2RArchetype.SHIPPING_FREIGHT_CYCLE,
        Round10ThemePosture.REDTEAM_FIRST,
        Round75ScoreWeightDraft(20, 7, 18, 8, 7, 0, 5),
        ("freight_rate_spike", "red_sea_disruption", "capacity_adjustment"),
        ("freight_rate_index", "ebitda_improvement", "cash_or_dividend"),
        ("multi_year_supply_discipline", "contract_rate_visibility"),
        ("freight_peak", "shipping_stock_crowded", "red_sea_premium_overpriced"),
        ("freight_rate_collapse", "spot_rate_below_breakeven", "overcapacity", "new_ship_delivery", "suez_route_normalization"),
        ("contract_vs_spot_rate", "fleet_capacity_discipline", "ebitda_cashflow", "overcapacity_low"),
        ("overcapacity", "freight_peak", "demand_slowdown", "route_normalization"),
        ("overcapacity", "freight_peak", "suez_normalization"),
        "Shipping is cycle-heavy; structural Green is highly restricted.",
    ),
    Round75ScoreTarget(
        "LOGISTICS_PARCEL_FREIGHT",
        E2RArchetype.LOGISTICS_PARCEL_FREIGHT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round75ScoreWeightDraft(18, 15, 6, 12, 10, 2, 5),
        ("parcel_volume", "freight_volume", "network_efficiency"),
        ("unit_price_stable", "labor_cost_control", "opm_improvement", "automation_cost_payback"),
        ("network_density_advantage", "recurring_shipper_contract"),
        ("logistics_efficiency_crowded",),
        ("unit_price_pressure", "labor_cost_spike", "volume_slowdown", "automation_cost_overrun"),
        ("volume_growth", "unit_price_stable", "labor_cost_control", "opm_improvement"),
        ("unit_price_pressure", "labor_cost", "volume_slowdown"),
        ("unit_price", "labor_cost", "volume"),
        "Logistics needs unit price and labor-cost control, not volume alone.",
    ),
    Round75ScoreTarget(
        "RENTAL_USED_CAR_MOBILITY",
        E2RArchetype.RENTAL_USED_CAR_MOBILITY,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round75ScoreWeightDraft(15, 12, 6, 10, 8, 1, 5),
        ("rental_demand", "used_car_price", "fleet_strategy", "ev_fleet_strategy"),
        ("fleet_margin", "residual_value_stable", "repair_cost_control", "utilization_rate"),
        ("asset_turnover_and_fcf", "residual_value_resilient", "repair_cost_stable"),
        ("fleet_strategy_crowded",),
        ("residual_value_drop", "repair_cost_spike", "insurance_cost", "fleet_writedown", "low_customer_demand"),
        ("residual_value", "repair_cost_per_vehicle", "utilization_rate", "fcf_margin"),
        ("residual_value", "repair_cost", "interest_rate", "fleet_writedown"),
        ("residual_value", "repair_cost", "interest", "ev_fleet"),
        "Rental and used-car stories need unit economics and residual value.",
    ),
    Round75ScoreTarget(
        "MOBILITY_RENTAL_MICROMOBILITY",
        E2RArchetype.MOBILITY_RENTAL_MICROMOBILITY,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round75ScoreWeightDraft(16, 13, 6, 11, 8, 1, 5),
        ("ipo_filing", "city_expansion", "ridership_growth"),
        ("revenue_growth", "fcf_positive", "unit_economics", "utilization_rate"),
        ("recurring_usage", "debt_stability", "regulatory_risk_controlled", "platform_partner_risk_low"),
        ("ipo_valuation_crowded",),
        ("debt_maturity", "going_concern", "regulatory_restriction", "seasonality_loss", "platform_partner_dependency"),
        ("micromobility_revenue", "micromobility_fcf", "utilization_rate", "debt_maturity_manageable"),
        ("unit_economics", "debt", "regulation", "seasonality", "uber_dependency"),
        ("debt", "seasonality", "uber_dependency", "unit_economics"),
        "Micromobility needs FCF and debt stability; rides or city count alone is not enough.",
    ),
    Round75ScoreTarget(
        "URBAN_AIR_DRONE",
        E2RArchetype.URBAN_AIR_DRONE,
        Round10ThemePosture.REDTEAM_FIRST,
        Round75ScoreWeightDraft(8, 8, 6, 12, 6, 0, 5),
        ("part135", "strategic_investment", "evtol_policy", "drone_theme"),
        ("type_certification", "production_certification", "commercial_operation", "customer_contract"),
        ("commercial_revenue", "unit_economics", "cash_runway_secure"),
        ("pre_revenue_valuation_crowded", "certification_story_overpriced"),
        ("certification_delay", "cash_burn", "discounted_offering", "production_delay", "pre_revenue_valuation"),
        ("type_certification_flag", "commercial_revenue", "cash_runway_months", "dilution_risk_low"),
        ("certification", "cash_burn", "dilution", "pre_revenue", "discounted_offering"),
        ("certification", "cash_burn", "dilution", "pre_revenue"),
        "eVTOL/drone is RedTeam-first until certification, revenue, and cash runway are proven.",
    ),
    Round75ScoreTarget(
        "SPACE_SUPPLYCHAIN",
        E2RArchetype.SPACE_SUPPLYCHAIN,
        Round10ThemePosture.REDTEAM_FIRST,
        Round75ScoreWeightDraft(14, 13, 8, 12, 9, 0, 5),
        ("space_theme", "satellite_supply_contract", "launch_program"),
        ("actual_contract", "delivery_revenue", "backlog_visibility"),
        ("repeat_space_supply_revenue", "customer_contract_quality"),
        ("spacex_supplychain_theme_crowded",),
        ("no_actual_contract", "launch_delay", "capex_debt_stress"),
        ("actual_delivery_contract", "revenue_conversion", "backlog_visibility"),
        ("no_contract", "launch_delay", "capex_debt", "theme_only"),
        ("no_contract", "launch_delay", "capex_debt"),
        "Space supply-chain labels need actual contracts and delivery revenue.",
    ),
    Round75ScoreTarget(
        "SATELLITE_CONNECTIVITY_INFRA",
        E2RArchetype.SATELLITE_CONNECTIVITY_INFRA,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round75ScoreWeightDraft(19, 21, 10, 13, 11, 2, 5),
        ("airline_connectivity_contract", "secure_communications", "satellite_backlog"),
        ("connectivity_revenue_growth", "airline_contract_count", "ebitda_improvement", "gross_backlog"),
        ("recurring_connectivity_revenue", "gross_backlog", "debt_capex_manageable"),
        ("connectivity_narrative_crowded", "secure_comms_story_overpriced"),
        ("launch_delay", "contract_cancellation", "capex_debt_stress", "competitor_constellation", "government_budget_delay"),
        ("satellite_backlog", "connectivity_revenue_growth", "airline_contract_count", "capex_debt_ratio_ok"),
        ("capex_debt", "launch_delay", "competitor_constellation", "contract_cancellation"),
        ("capex_debt", "launch_delay", "customer_concentration"),
        "Satellite connectivity can be Green-eligible only with real backlog and recurring revenue.",
    ),
    Round75ScoreTarget(
        "TRANSPORT_SAFETY_REGULATORY_OVERLAY",
        E2RArchetype.TRANSPORT_SAFETY_REGULATORY_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        ("transport_safety_event", "autonomous_vehicle_recall", "evtOL_safety_event", "airline_safety_event"),
        ("incident_quantified", "regulatory_response", "service_recovery"),
        ("not_applicable_gate_only",),
        ("safety_risk_underpriced",),
        ("safety_recall", "nhtsa_scrutiny", "certification_delay", "service_suspension", "accident_liability"),
        (),
        ("safety_recall", "nhtsa_scrutiny", "certification", "service_suspension"),
        ("safety", "regulatory", "certification"),
        "Transport safety and certification events are RedTeam gates, not positive score inputs.",
        gate_only=True,
    ),
    Round75ScoreTarget(
        "FLEET_UNIT_ECONOMICS_OVERLAY",
        E2RArchetype.FLEET_UNIT_ECONOMICS_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        ("fleet_unit_economics_warning", "ev_fleet_strategy", "micromobility_unit_economics"),
        ("residual_value_stable", "repair_cost_control", "utilization_rate", "debt_maturity_manageable"),
        ("not_applicable_gate_only",),
        ("fleet_growth_overpriced",),
        ("fleet_depreciation", "repair_cost_spike", "insurance_cost", "utilization_drop", "going_concern"),
        (),
        ("residual_value", "repair_cost", "utilization", "debt", "going_concern"),
        ("fleet_depreciation", "repair_cost", "utilization", "debt"),
        "Fleet economics overlays guard rental, EV fleet, and micromobility stories.",
        gate_only=True,
    ),
)


ROUND75_CASE_CANDIDATES: tuple[Round75CaseCandidate, ...] = (
    Round75CaseCandidate(
        "hyundai_hybrid_valueup_case",
        "AUTO_HYBRID_VALUEUP",
        "005380",
        "Hyundai Motor hybrid value-up",
        "KR",
        "success_candidate",
        date(2024, 8, 28),
        date(2024, 8, 28),
        None,
        None,
        None,
        ("hybrid_sales_growth", "op_margin_target", "buyback_amount", "dividend_policy_change", "shareholder_return_ratio"),
        ("tariff_event_flag", "peak_margin", "recall_flag"),
        "auto_valueup_aligned_candidate",
        "needs_price_backfill",
        ("round_75.md Reuters Hyundai hybrid expansion and shareholder return",),
        "Hyundai is a candidate because hybrid mix, OPM target, FCF, and shareholder return are linked.",
    ),
    Round75CaseCandidate(
        "hyundai_tariff_margin_cut_case",
        "AUTO_MOBILITY_COMPLETED_VEHICLE",
        "005380",
        "Hyundai tariff margin cut and US localization",
        "KR",
        "4b_watch",
        None,
        date(2025, 9, 18),
        None,
        date(2025, 9, 18),
        None,
        ("local_production_ratio", "hybrid_ev_us_capacity", "tariff_response"),
        ("op_margin_cut_flag", "tariff_cost_amount", "local_production_capex", "us_ramp_up_risk"),
        "auto_tariff_margin_watch",
        "needs_price_backfill",
        ("round_75.md Reuters Hyundai US output and margin goal cut",),
        "US localization may help long term, but tariff-driven OPM target cuts cap valuation rerating.",
    ),
    Round75CaseCandidate(
        "toyota_hybrid_parts_bottleneck_case",
        "HYBRID_COMPONENT_BOTTLENECK",
        "7203.T",
        "Toyota hybrid parts bottleneck reference",
        "JP",
        "success_candidate",
        None,
        date(2025, 3, 31),
        None,
        date(2025, 3, 31),
        None,
        ("hybrid_sales_growth", "inverter_supply_constraint_flag", "magnet_supply_constraint_flag", "motor_supply_constraint_flag"),
        ("customer_concentration", "raw_material_cost_change", "bottleneck_normalization"),
        "hybrid_component_bottleneck_reference",
        "needs_price_backfill",
        ("round_75.md Reuters Toyota hybrid bottleneck",),
        "Hybrid parts can be Watch-to-Green only after real delivery, margin, and cost pass-through are confirmed.",
    ),
    Round75CaseCandidate(
        "avride_hyundai_ioniq5_robotaxi_case",
        "AUTONOMOUS_ROBOTAXI_DEPLOYMENT",
        "005380",
        "Avride Hyundai IONIQ 5 robotaxi partnership",
        "KR",
        "success_candidate",
        None,
        date(2025, 3, 5),
        None,
        None,
        None,
        ("robotaxi_partnership", "platform_integration_flag", "robotaxi_fleet_size", "service_area_expansion"),
        ("safety_record_unverified", "unit_economics_unverified", "insurance_liability_cost_unverified"),
        "robotaxi_deployment_aligned_stage2_candidate",
        "needs_price_backfill",
        ("round_75.md Reuters Avride Hyundai robotaxi",),
        "Robotaxi deployment becomes Stage 2 evidence only after service area, fleet, rides, safety, and unit economics are verified.",
        (E2RArchetype.AUTO_MOBILITY_COMPLETED_VEHICLE,),
    ),
    Round75CaseCandidate(
        "waymo_flood_recall_robotaxi_case",
        "TRANSPORT_SAFETY_REGULATORY_OVERLAY",
        "GOOGL",
        "Waymo flooded-road robotaxi recall",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2026, 5, 1),
        ("robotaxi_service_area", "paid_ride_volume"),
        ("safety_recall_flag", "weather_handling_failure_flag", "nhtsa_scrutiny_flag", "remote_assistance_cost"),
        "robotaxi_safety_4c",
        "needs_price_backfill",
        ("round_75.md The Verge Waymo flooded-road recall",),
        "Robotaxi scale cannot stay Green if safety recall and weather-handling failures break operational trust.",
        (E2RArchetype.AUTONOMOUS_ROBOTAXI_DEPLOYMENT,),
    ),
    Round75CaseCandidate(
        "waymo_houston_expansion_case",
        "AUTONOMOUS_ROBOTAXI_DEPLOYMENT",
        "GOOGL",
        "Waymo Houston robotaxi expansion",
        "US",
        "4b_watch",
        None,
        date(2026, 5, 1),
        None,
        date(2026, 5, 1),
        None,
        ("robotaxi_service_area", "paid_ride_volume", "platform_integration_flag"),
        ("safety_recall_flag", "unit_economics_unverified", "insurance_liability_cost_unverified"),
        "robotaxi_deployment_expansion_safety_watch",
        "needs_price_backfill",
        ("round_75.md Waymo Houston expansion",),
        "Deployment expansion remains Watch until ride economics and safety record are proven.",
    ),
    Round75CaseCandidate(
        "korean_air_asiana_integration_case",
        "AIRLINE_TRAVEL_CYCLE",
        "003490",
        "Korean Air Asiana integration",
        "KR",
        "cyclical_success",
        date(2024, 12, 12),
        date(2025, 2, 7),
        None,
        date(2025, 2, 7),
        None,
        ("asiana_integration_flag", "record_revenue", "operating_profit_growth", "cargo_revenue_growth"),
        ("jet_fuel_price", "fx_rate_exposure", "integration_cost", "cargo_cycle", "tariff_trade_uncertainty"),
        "airline_integration_cycle_watch",
        "needs_price_backfill",
        ("round_75.md Reuters Korean Air record revenue and integration",),
        "Airline integration can be Stage 1/2, but fuel, FX, cargo cycle, and integration cost keep Green restricted.",
    ),
    Round75CaseCandidate(
        "china_group_visa_tourism_case",
        "CASINO_DUTYFREE_TOURISM",
        "KR_TOURISM_POLICY",
        "Korea China group visa tourism policy basket",
        "KR",
        "event_premium",
        date(2025, 9, 29),
        None,
        None,
        date(2025, 9, 29),
        None,
        ("visa_free_policy_flag", "china_tourist_arrivals", "tourism_policy_event"),
        ("average_spend_unverified", "casino_drop_amount_unverified", "duty_free_asp_unverified", "policy_event_only"),
        "tourism_policy_event_stage1",
        "needs_price_backfill",
        ("round_75.md Reuters China group visa-free entry",),
        "Visa-free tourism is Stage 1 until spend, drop amount, duty-free ASP, RevPAR, and OPM are visible.",
    ),
    Round75CaseCandidate(
        "ses_airline_connectivity_case",
        "SATELLITE_CONNECTIVITY_INFRA",
        "SESG.PA",
        "SES airline connectivity backlog",
        "EU",
        "success_candidate",
        None,
        date(2026, 5, 12),
        None,
        date(2026, 5, 12),
        None,
        ("connectivity_revenue_growth", "airline_contract_count", "new_contracts_value", "gross_backlog"),
        ("capex_debt_ratio", "launch_delay_flag", "competitor_constellation", "government_budget_delay"),
        "satellite_connectivity_aligned_candidate",
        "needs_price_backfill",
        ("round_75.md Reuters SES airline connectivity",),
        "SES is different from a space theme because revenue, airline contracts, and backlog are visible.",
    ),
    Round75CaseCandidate(
        "maersk_container_rate_collapse_case",
        "SHIPPING_FREIGHT_CYCLE",
        "MAERSK-B.CO",
        "Maersk overcapacity freight-rate collapse",
        "DK",
        "4c_thesis_break",
        date(2024, 3, 14),
        None,
        None,
        date(2025, 10, 3),
        date(2025, 10, 3),
        ("freight_rate_index", "container_rate", "red_sea_disruption_flag"),
        ("spot_rate_below_breakeven_flag", "overcapacity_flag", "fleet_capacity_growth", "freight_rate_collapse"),
        "shipping_cyclical_success_or_4c",
        "needs_price_backfill",
        ("round_75.md Reuters Maersk unsustainable container rates", "round_75.md Reuters falling ocean rates",),
        "Shipping freight spikes are cyclical unless contract rates and supply discipline persist.",
    ),
    Round75CaseCandidate(
        "maersk_suez_overcapacity_loss_case",
        "SHIPPING_FREIGHT_CYCLE",
        "MAERSK-B.CO",
        "Maersk Suez route normalization",
        "DK",
        "4b_watch",
        None,
        None,
        None,
        date(2026, 1, 15),
        None,
        ("red_sea_disruption_flag", "suez_route_normalization_flag"),
        ("red_sea_premium_normalization", "freight_rate_premium_loss", "route_normalization"),
        "red_sea_premium_normalization_4c_watch",
        "needs_price_backfill",
        ("round_75.md Reuters Maersk Suez Canal sailings",),
        "Red Sea route normalization can remove event-driven freight premium.",
    ),
    Round75CaseCandidate(
        "hertz_ev_rental_failure_case",
        "FLEET_UNIT_ECONOMICS_OVERLAY",
        "HTZ",
        "Hertz EV rental residual-value failure",
        "US",
        "4c_thesis_break",
        date(2024, 1, 11),
        None,
        None,
        None,
        date(2024, 1, 11),
        ("ev_fleet_ratio", "fleet_strategy"),
        ("repair_cost_per_vehicle", "used_car_residual_value", "fleet_write_down", "low_customer_demand"),
        "rental_ev_unit_economics_4c",
        "needs_price_backfill",
        ("round_75.md Axios Hertz sells 20,000 EVs",),
        "EV fleet transition breaks if residual value, repair cost, insurance, and utilization do not work.",
        (E2RArchetype.RENTAL_USED_CAR_MOBILITY,),
    ),
    Round75CaseCandidate(
        "michelin_tire_demand_cut_case",
        "TIRE_AUTO_COMPONENT_SPREAD",
        "ML.PA",
        "Michelin tire demand outlook cut",
        "EU",
        "4c_thesis_break",
        date(2025, 10, 13),
        None,
        None,
        None,
        date(2025, 10, 13),
        ("tire_demand_recovery", "raw_material_spread"),
        ("north_america_demand_slowdown", "replacement_market_weakness", "tariff_event_flag", "fx_rate_exposure"),
        "tire_demand_slowdown_4c_watch",
        "needs_price_backfill",
        ("round_75.md Reuters Michelin annual outlook cut",),
        "Tire margin visibility breaks when replacement demand, volume, tariff, and FX turn adverse.",
    ),
    Round75CaseCandidate(
        "lime_ipo_micromobility_case",
        "MOBILITY_RENTAL_MICROMOBILITY",
        "LIME_PRIVATE",
        "Lime micromobility IPO filing",
        "US",
        "success_candidate",
        None,
        date(2026, 5, 8),
        None,
        date(2026, 5, 8),
        None,
        ("micromobility_revenue", "micromobility_fcf", "city_count", "platform_partner_revenue_ratio"),
        ("net_loss", "debt_maturity_amount", "going_concern_flag", "seasonality_risk", "uber_dependency_flag"),
        "micromobility_fcf_but_leverage_risk",
        "needs_price_backfill",
        ("round_75.md MarketWatch Lime IPO filing",),
        "FCF positive is useful, but debt maturity, seasonality, net loss, and Uber dependence keep this Watch.",
    ),
    Round75CaseCandidate(
        "joby_discounted_offering_case",
        "URBAN_AIR_DRONE",
        "JOBY",
        "Joby discounted offering",
        "US",
        "4c_thesis_break",
        date(2025, 10, 8),
        None,
        None,
        None,
        date(2025, 10, 8),
        ("blade_acquisition", "pre_revenue_flag", "commercial_launch_preparation"),
        ("discounted_offering_flag", "evt_cash_burn", "pre_revenue_flag", "dilution", "type_certification_missing"),
        "evtOL_execution_candidate_but_dilution_4c_watch",
        "needs_price_backfill",
        ("round_75.md Reuters Joby discounted offering",),
        "Launch infrastructure is not commercialization; discounted offering highlights cash-runway risk.",
    ),
    Round75CaseCandidate(
        "lilium_evtol_cash_crunch_case",
        "URBAN_AIR_DRONE",
        "LILM",
        "Lilium eVTOL cash crunch",
        "EU",
        "4c_thesis_break",
        date(2024, 11, 25),
        None,
        None,
        None,
        date(2024, 11, 25),
        ("evtol_policy", "pre_revenue_flag"),
        ("cash_burn", "certification_delay", "funding_gap", "production_delay", "profitability_delay"),
        "evtol_cash_burn_hard_counterexample",
        "needs_price_backfill",
        ("round_75.md Reuters Lilium cash crunch",),
        "eVTOL funding and certification delays are hard RedTeam evidence before commercial revenue.",
    ),
    Round75CaseCandidate(
        "archer_part135_no_type_cert_case",
        "URBAN_AIR_DRONE",
        "ACHR",
        "Archer Part 135 without type certification",
        "US",
        "event_premium",
        date(2024, 6, 5),
        None,
        None,
        date(2024, 6, 5),
        None,
        ("part135_flag", "evtol_policy"),
        ("type_certification_flag_missing", "production_certification_flag_missing", "cash_runway_months_needed"),
        "part135_stage1_not_stage3",
        "needs_price_backfill",
        ("round_75.md Reuters Archer Part 135",),
        "Part 135 is a milestone, not proof that the aircraft is type-certified or commercially scaled.",
    ),
    Round75CaseCandidate(
        "archer_nyc_network_case",
        "URBAN_AIR_DRONE",
        "ACHR",
        "Archer New York air taxi network plan",
        "US",
        "event_premium",
        date(2025, 4, 17),
        None,
        None,
        date(2025, 4, 17),
        None,
        ("vertiport_contract_flag", "evtol_policy", "commercial_launch_preparation"),
        ("type_certification_flag_missing", "commercial_revenue_missing", "cash_runway_months_needed"),
        "evtOL_certification_not_commercialization",
        "needs_price_backfill",
        ("round_75.md Archer NYC network",),
        "A network plan can support Stage 1, but Type Certification, commercial revenue, and unit economics remain required.",
    ),
)


ROUND75_PRICE_FIELDS: tuple[str, ...] = (
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
    "vehicle_sales_growth",
    "hybrid_sales_growth",
    "ev_sales_growth",
    "erev_plan_flag",
    "operating_margin",
    "op_margin_target",
    "op_margin_cut_flag",
    "fcf_margin",
    "buyback_amount",
    "dividend_policy_change",
    "shareholder_return_ratio",
    "tariff_event_flag",
    "tariff_cost_amount",
    "local_production_ratio",
    "recall_flag",
    "quality_cost_flag",
    "hybrid_component_order",
    "hybrid_component_revenue",
    "inverter_supply_constraint_flag",
    "magnet_supply_constraint_flag",
    "motor_supply_constraint_flag",
    "customer_concentration",
    "raw_material_cost_change",
    "capacity_normalization_flag",
    "adas_component_revenue",
    "camera_lidar_radar_revenue",
    "autonomous_platform_customer",
    "mass_adoption_flag",
    "robotaxi_service_area",
    "robotaxi_fleet_size",
    "paid_ride_volume",
    "rides_per_week",
    "cost_per_mile",
    "vehicle_utilization",
    "safety_recall_flag",
    "nhtsa_scrutiny_flag",
    "weather_handling_failure_flag",
    "insurance_liability_cost",
    "remote_assistance_cost",
    "platform_integration_flag",
    "passenger_revenue_growth",
    "cargo_revenue_growth",
    "load_factor",
    "jet_fuel_price",
    "fx_rate_exposure",
    "integration_cost",
    "synergy_amount",
    "asiana_integration_flag",
    "lcc_integration_flag",
    "tourist_arrivals",
    "china_tourist_arrivals",
    "visa_free_policy_flag",
    "casino_drop_amount",
    "vip_mix",
    "duty_free_sales",
    "duty_free_asp",
    "hotel_occupancy",
    "revpar",
    "average_spend_per_visitor",
    "alipay_wechatpay_integration_flag",
    "freight_rate_index",
    "container_rate",
    "spot_rate_below_breakeven_flag",
    "fleet_capacity_growth",
    "red_sea_disruption_flag",
    "suez_route_normalization_flag",
    "overcapacity_flag",
    "ebitda_change",
    "dividend_change",
    "rental_fleet_size",
    "ev_fleet_ratio",
    "used_car_residual_value",
    "repair_cost_per_vehicle",
    "insurance_cost_change",
    "vehicle_depreciation_charge",
    "fleet_write_down",
    "utilization_rate",
    "micromobility_revenue",
    "micromobility_fcf",
    "net_loss",
    "debt_maturity_amount",
    "going_concern_flag",
    "city_count",
    "seasonality_risk",
    "platform_partner_revenue_ratio",
    "uber_dependency_flag",
    "evt_cash_burn",
    "cash_runway_months",
    "type_certification_flag",
    "part135_flag",
    "production_certification_flag",
    "discounted_offering_flag",
    "offering_discount_pct",
    "pre_revenue_flag",
    "commercial_launch_date",
    "vertiport_contract_flag",
    "satellite_backlog",
    "connectivity_revenue_growth",
    "airline_contract_count",
    "new_contracts_value",
    "gross_backlog",
    "capex_debt_ratio",
    "launch_delay_flag",
    "secure_comms_revenue_flag",
    "score_price_alignment",
    "price_validation_status",
    "review_notes",
)


ROUND75_RISK_OVERLAYS: tuple[str, ...] = (
    "AUTO_VALUEUP_ALIGNED",
    "AUTO_TARIFF_MARGIN_WATCH",
    "HYBRID_COMPONENT_BOTTLENECK",
    "ROBOTAXI_DEPLOYMENT_ALIGNED",
    "ROBOTAXI_SAFETY_4C",
    "AIRLINE_INTEGRATION_CYCLE_WATCH",
    "TOURISM_POLICY_EVENT",
    "SHIPPING_CYCLICAL_SUCCESS_OR_4C",
    "RENTAL_EV_UNIT_ECONOMICS_4C",
    "MICROMOBILITY_FCF_BUT_LEVERAGE_RISK",
    "EVTOL_CERTIFICATION_NOT_COMMERCIALIZATION",
    "SATELLITE_CONNECTIVITY_ALIGNED",
)


def target_for(target_id: str) -> Round75ScoreTarget | None:
    for target in ROUND75_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round75_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND75_CASE_CANDIDATES:
        target = target_for(candidate.target_id)
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
                f"Round75 R9 Loop-3 case for {candidate.target_id}; "
                "demand recovery, hybrid, tourism, freight, eVTOL, and space labels are separated from OPM, FCF, unit economics, certification, and backlog evidence."
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
                "require_cross_evidence_for_green",
                "demand_recovery_or_policy_headline_is_not_green_evidence_alone",
                "hybrid_label_is_not_margin_or_fcf",
                "freight_spike_is_not_structural_green",
                "part135_is_not_type_certification_or_revenue",
                "tourism_policy_is_stage1_until_spend_drop_asp_and_opm_are_verified",
                "do_not_invent_opm_fcf_tariff_freight_drop_unit_economics_certification_backlog_or_stage_prices",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=False,
                price_data_available=False,
                stage_dates_confidence=0.75 if candidate.stage2_date or candidate.stage4b_date or candidate.stage4c_date else 0.2,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round75_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND75_SCORE_TARGETS:
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


def round75_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND75_CASE_CANDIDATES:
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


def round75_stage_date_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "target_id": target.target_id,
            "stage1": "|".join(target.stage1_signals),
            "stage2": "|".join(target.stage2_signals),
            "stage3": "|".join(target.stage3_conditions),
            "stage4b": "|".join(target.stage4b_conditions),
            "stage4c": "|".join(target.stage4c_conditions),
            "red_flags": "|".join(target.red_flags),
            "loop3_penalty_axes": "|".join(target.loop3_penalty_axes),
            "gate_only": str(target.gate_only).lower(),
            "production_scoring_changed": "false",
        }
        for target in ROUND75_SCORE_TARGETS
    )


def round75_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round75_backfill": "true"} for field in ROUND75_PRICE_FIELDS)


def round75_summary() -> dict[str, int | bool]:
    records = round75_case_records()
    return {
        "target_count": len(ROUND75_SCORE_TARGETS),
        "case_candidate_count": len(records),
        "structural_success_count": sum(1 for record in records if record.case_type == "structural_success"),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for record in records if record.case_type == "cyclical_success"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "overheat_count": sum(1 for record in records if record.case_type == "overheat"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND75_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND75_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND75_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "gate_only_target_count": sum(1 for target in ROUND75_SCORE_TARGETS if target.gate_only),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round75_r9_loop3_reports(
    *,
    output_directory: str | Path = ROUND75_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND75_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND75_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round75_r9_loop3_mobility_transport_leisure_summary.md",
        "case_matrix": output / "round75_r9_loop3_case_matrix.csv",
        "stage_date_plan": output / "round75_r9_loop3_stage_date_plan.csv",
        "green_guardrails": output / "round75_r9_loop3_green_guardrails.md",
        "risk_overlays": output / "round75_r9_loop3_risk_overlays.md",
        "price_validation_plan": output / "round75_r9_loop3_price_validation_plan.md",
        "price_fields": output / "round75_r9_loop3_price_fields.csv",
    }
    _write_case_jsonl(round75_case_records(), cases)
    _write_rows(round75_score_profile_rows(), score_profiles)
    _write_rows(round75_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round75_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round75_price_field_rows(), paths["price_fields"])
    paths["summary"].write_text(render_round75_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round75_green_guardrail_markdown(), encoding="utf-8")
    paths["risk_overlays"].write_text(render_round75_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round75_price_validation_plan_markdown(), encoding="utf-8")
    return paths


def render_round75_summary_markdown() -> str:
    summary = round75_summary()
    lines = [
        "# Round 75 R9 Loop-3 Mobility/Transport/Leisure Summary",
        "",
        "Round 75 is calibration material only. It does not change production scoring.",
        "",
        "## Counts",
    ]
    for key, value in summary.items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Core Rule",
            "",
            "Demand recovery, hybrid labels, tourism policy, freight spikes, eVTOL milestones, and space themes are not Stage 3 evidence by themselves.",
            "Green requires OPM, FCF, capital return, unit economics, certification, backlog, or recurring revenue evidence.",
            "",
            "Example: Part 135 is a useful eVTOL milestone. It is not the same as aircraft type certification, commercial revenue, or positive unit economics.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round75_green_guardrail_markdown() -> str:
    lines = [
        "# Round 75 R9 Loop-3 Green Guardrails",
        "",
        "- Do not apply R9 Loop-3 v3.0 weights to production scoring yet.",
        "- Do not use case records as candidate-generation input.",
        "- Do not treat demand recovery, hybrid labels, tourism policy, freight spikes, eVTOL milestones, or space themes as Green evidence alone.",
        "- Completed-vehicle Green requires hybrid/mix, OPM, FCF, and capital-return execution.",
        "- Tourism policy is Stage 1 until spend, drop amount, duty-free ASP, RevPAR, and OPM are verified.",
        "- Freight spikes stay Red/Watch unless contract rates and supply discipline persist.",
        "- Part 135 is not type certification or commercialization.",
        "- Do not invent OPM, FCF, tariff cost, freight rates, casino drop, unit economics, certification, backlog, or stage prices.",
        "",
        "간단한 예시: 중국 단체관광 무비자 뉴스는 좋은 촉매지만, 카지노 drop amount와 면세 객단가가 확인되기 전에는 Stage 3-Green 근거가 아닙니다.",
    ]
    return "\n".join(lines) + "\n"


def render_round75_risk_overlay_markdown() -> str:
    lines = ["# Round 75 R9 Loop-3 Risk Overlays", ""]
    for overlay in ROUND75_RISK_OVERLAYS:
        lines.append(f"- {overlay}")
    lines.extend(
        [
            "",
            "These overlays are diagnostic calibration labels. They are not production score inputs.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round75_price_validation_plan_markdown() -> str:
    lines = [
        "# Round 75 R9 Loop-3 Price Validation Plan",
        "",
        "For every case, backfill stage prices and forward MFE/MAE before applying score-weight changes.",
        "",
        "## Priority Cases",
    ]
    for row in round75_case_candidate_rows():
        stage_date = row["stage2_date"] or row["stage4b_date"] or row["stage4c_date"] or row["stage1_date"] or "date_needed"
        lines.append(f"- {row['case_id']}: {stage_date} / {row['alignment_hint']}")
    lines.extend(
        [
            "",
            "## Required Validation Fields",
            "",
            ", ".join(ROUND75_PRICE_FIELDS),
        ]
    )
    return "\n".join(lines) + "\n"


def _score_price_alignment(candidate: Round75CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "aligned"
    if candidate.case_type in {"success_candidate", "cyclical_success"}:
        return "unknown"
    if candidate.case_type in {"4c_thesis_break", "failed_rerating", "overheat"}:
        return "false_positive_score"
    if candidate.case_type == "event_premium":
        return "price_moved_without_evidence"
    return "unknown"


def _rerating_result(candidate: Round75CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "true_rerating"
    if candidate.case_type == "cyclical_success":
        return "cyclical_rerating"
    if candidate.case_type == "event_premium":
        return "event_premium"
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    return "unknown"


def _score_weight_hint(target: Round75ScoreTarget) -> dict[str, float]:
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


def _write_case_jsonl(records: Iterable[E2RCaseRecord], path: Path) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record.as_dict(), ensure_ascii=False, sort_keys=True))
            fh.write("\n")


def _write_rows(rows: Iterable[Mapping[str, str]], path: Path) -> None:
    rows = tuple(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
