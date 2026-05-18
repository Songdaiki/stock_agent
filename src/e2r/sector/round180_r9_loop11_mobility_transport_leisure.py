"""Round-180 R9 Loop-11 Korea mobility, transport, and leisure pack.

Round 180 narrows the R9 mobility/transport/leisure taxonomy to Korea-focused
completed vehicle, auto-parts, logistics, tourism, casino/duty-free, airline
safety, shipping, and travel-agency evidence. It is calibration/report material
only. Production feature engineering, scoring, staging, and RedTeam code must
not import it.
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


ROUND180_SOURCE_ROUND_PATH = "docs/round/round_180.md"
ROUND180_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round180_r9_loop11_mobility_transport_leisure"
ROUND180_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r9_loop11_round180.jsonl"
ROUND180_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round180_r9_loop11_v11.csv"
ROUND180_SOURCE_CANONICAL_TARGET_IDS: tuple[str, ...] = (
    "AUTO_HYBRID_LOCALIZATION_KOREA",
    "AUTO_SDV_DELAY_CAPEX_OVERLAY",
    "AUTO_PRICE_WAR_EUROPE_OVERLAY",
    "AUTO_COMPONENT_RESTRUCTURING_KOREA",
    "AUTO_COMPONENT_QUALITY_RECALL_OVERLAY",
    "ECOMMERCE_LOGISTICS_REPEAT_CONTRACT",
    "LOGISTICS_LABOR_REGULATION_OVERLAY",
    "CASINO_DUTYFREE_TOURISM_POLICY_KOREA",
    "CASINO_RETURN_VISITOR_UNIT_ECONOMICS",
    "AIRLINE_SAFETY_REGULATORY_OVERLAY",
    "SHIPPING_FREIGHT_CYCLE_KOREA",
    "PARCEL_VOLUME_PRICE_COST_SPREAD",
    "TRAVEL_AGENCY_POLICY_EVENT",
    "DISCLOSURE_CONFIDENCE_CAP",
)
ROUND180_SOURCE_CANONICAL_TARGET_COUNT = len(ROUND180_SOURCE_CANONICAL_TARGET_IDS)


@dataclass(frozen=True)
class Round180ScoreWeightDraft:
    eps_fcf_opm_conversion: int | str
    contract_volume_operating_visibility: int | str
    unit_fleet_economics: int | str
    safety_regulation_labor_quality_risk: int | str
    early_price_path_validation: int | str
    recurrence_demand_durability: int | str
    valuation_room_4b_runway: int | str

    def as_dict(self) -> dict[str, int | str]:
        return {
            "eps_fcf_opm_conversion": self.eps_fcf_opm_conversion,
            "contract_volume_operating_visibility": self.contract_volume_operating_visibility,
            "unit_fleet_economics": self.unit_fleet_economics,
            "safety_regulation_labor_quality_risk": self.safety_regulation_labor_quality_risk,
            "early_price_path_validation": self.early_price_path_validation,
            "recurrence_demand_durability": self.recurrence_demand_durability,
            "valuation_room_4b_runway": self.valuation_room_4b_runway,
        }


@dataclass(frozen=True)
class Round180ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round180ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    loop11_penalty_axes: tuple[str, ...]
    normalization_point: str
    gate_only: bool = False

    @property
    def large_sector(self) -> Round10LargeSector:
        return Round10LargeSector.MOBILITY_TRANSPORT_LEISURE

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round180CaseCandidate:
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


@dataclass(frozen=True)
class Round180BaseScoreWeight:
    component: str
    points: int
    loop11_direction: str
    reason: str


@dataclass(frozen=True)
class Round180StageCap:
    stage_band: str
    max_score: str
    required_evidence: tuple[str, ...]
    example_cases: tuple[str, ...]
    green_policy: str


@dataclass(frozen=True)
class Round180ScoreStagePriceAlignment:
    case_id: str
    detected_stage: str
    price_path_status: str
    verdict: str
    normalization_adjustment: str


def _weights(
    eps_fcf: int | str,
    visibility: int | str,
    unit: int | str,
    risk: int | str,
    price: int | str,
    recurrence: int | str,
    valuation: int | str,
) -> Round180ScoreWeightDraft:
    return Round180ScoreWeightDraft(eps_fcf, visibility, unit, risk, price, recurrence, valuation)


def _target(
    target_id: str,
    archetype: E2RArchetype,
    posture: Round10ThemePosture,
    weight: Round180ScoreWeightDraft,
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
) -> Round180ScoreTarget:
    return Round180ScoreTarget(target_id, archetype, posture, weight, stage1, stage2, stage3, stage4b, stage4c, green, red, penalties, note, gate_only)


GATE_WEIGHT = _weights("gate", "gate", "gate", "gate", "gate", "gate", "gate")
CAP_WEIGHT = _weights("cap", "cap", "cap", "+", "cap", "cap", "cap")


ROUND180_BASE_SCORE_WEIGHTS: tuple[Round180BaseScoreWeight, ...] = (
    Round180BaseScoreWeight("eps_fcf_opm_conversion", 22, "raise_margin_bodyweight", "R9 demand recovery matters only when it converts into OPM, FCF, or OP/EPS revisions."),
    Round180BaseScoreWeight("contract_volume_operating_visibility", 18, "raise_operating_visibility", "Sales targets, US localization, logistics contracts, parcel volume, casino drop, duty-free sales, freight, and visitor data are Stage 2 evidence."),
    Round180BaseScoreWeight("unit_fleet_economics", 18, "raise_unit_economics", "Utilization, cost per mile, parcel unit price, casino hold rate, RevPAR, repair cost, and residual value separate Stage 2 from Stage 3."),
    Round180BaseScoreWeight("safety_regulation_labor_quality_risk", 14, "hard_redteam_gate", "Safety accidents, inspections, recalls, warranty costs, labor regulation, tariff pressure, and price wars can cap or break R9 candidates."),
    Round180BaseScoreWeight("early_price_path_validation", 10, "loop11_axis", "Stage 2 이후 60D MFE helps early Stage 3, while Stage 2 이후 120D MFE helps 4B cooling."),
    Round180BaseScoreWeight("recurrence_demand_durability", 10, "raise_repeatability", "Repeat logistics contracts, repeat visitors, recurring demand, and durable hybrid mix are required before Green."),
    Round180BaseScoreWeight("valuation_room_4b_runway", 8, "cool_theme_rerating", "Tourism, freight, hybrid, and logistics headlines often reprice before unit economics confirm."),
)


ROUND180_STAGE_CAPS: tuple[Round180StageCap, ...] = (
    Round180StageCap(
        "Stage 1",
        "45",
        ("hybrid_expansion", "us_localization", "china_group_visa_free", "freight_rate_rise", "parcel_volume_growth", "casino_or_dutyfree_recovery_news"),
        ("tourism_visa_free_dutyfree_casino_policy_event_case", "travel_agency_policy_event_stage1_2_case"),
        "Hybrid, tourism, freight, parcel, casino, or duty-free headlines route research only.",
    ),
    Round180StageCap(
        "Stage 2",
        "70",
        ("sales_target", "local_production_plan", "contract_amount", "logistics_alliance", "airline_or_casino_revenue", "freight_or_volume_or_backlog"),
        ("kia_hybrid_localization_sdv_delay_stage2_4c_watch_case", "cj_logistics_shinsegae_oneday_volume_stage2_3_case", "hyundai_mobis_lighting_restructuring_quality_recall_case"),
        "Stage 2 can be strong, but Green waits for OPM/FCF, unit economics, repeat demand, and clean risk gates.",
    ),
    Round180StageCap(
        "Stage 3",
        "requires_5_of_8",
        ("op_eps_revision_or_quarterly_op_beat", "volume_sales_drop_or_revenue_increases", "opm_fcf_improves", "unit_economics_not_deteriorating", "stage2_60d_mfe_20pct", "repeat_contract_or_recurring_demand_confirmed", "no_safety_quality_regulatory_hard_issue", "valuation_not_overheated"),
        ("cj_logistics_shinsegae_oneday_volume_stage2_3_case", "casino_return_visitor_unit_economics_gate_case"),
        "Stage 3 requires five of eight R9 conditions; policy, freight, hybrid, or volume headlines alone cannot create Green.",
    ),
    Round180StageCap(
        "Stage 4B",
        "requires_3_of_5",
        ("stage2_120d_mfe_60pct", "tourism_freight_hybrid_news_basket_rally", "policy_freight_theme_priced_before_earnings", "op_eps_revision_cannot_follow_price", "crowded_sector_narrative"),
        ("tourism_visa_free_dutyfree_casino_policy_event_case", "hmm_pan_ocean_freight_cycle_4b_4c_watch_case"),
        "Cool R9 candidates when price moves before OPM, FCF, unit economics, or repeat evidence.",
    ),
    Round180StageCap(
        "Stage 4C",
        "hard_gate",
        ("airline_or_large_safety_accident", "government_safety_inspection_or_operating_restriction", "freight_decline_and_overcapacity", "opm_target_cut", "quality_recall_or_warranty_cost", "volume_up_but_opm_down", "visitor_up_but_spend_or_drop_weak", "delivery_labor_or_regulation_cost_spike"),
        ("jeju_air_muan_crash_hard_4c_case", "kia_sdv_delay_capex_price_war_overlay_case", "hyundai_mobis_iccu_quality_recall_overlay_case"),
        "One hard safety, quality, freight, labor, unit-economics, or margin break can block unsafe Green.",
    ),
)


ROUND180_SCORE_TARGETS: tuple[Round180ScoreTarget, ...] = (
    _target(
        "AUTO_HYBRID_LOCALIZATION_KOREA",
        E2RArchetype.AUTO_HYBRID_LOCALIZATION_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(20, 22, 14, 14, 10, 12, 8),
        stage1=("hybrid_demand", "ev_slowdown_response", "us_tariff_hedge"),
        stage2=("georgia_hybrid_production", "kia_40pct_allocation", "us_capacity_1_2m", "localization_plan"),
        stage3=("hybrid_sales_growth", "opm_defense", "tariff_cost_absorbed", "fcf_and_return_stable", "sdv_capex_control"),
        stage4b=("hybrid_localization_narrative_crowded", "auto_basket_rally_before_margin"),
        stage4c=("sdv_delay", "ev_target_cut", "capex_hike", "europe_price_war", "opm_cut"),
        green=("hybrid_sales_growth", "opm_defense", "tariff_cost_absorbed", "fcf_and_return_stable", "sdv_capex_control"),
        red=("sdv_delay", "ev_target_cut", "capex_hike", "europe_price_war", "opm_cut"),
        penalties=("sdv_delay", "ev_target_cut", "capex", "price_war", "tariff"),
        note="Kia-style hybrid localization is Stage 2 evidence; Green waits for OPM/FCF and tariff absorption.",
    ),
    _target(
        "AUTO_SDV_DELAY_CAPEX_OVERLAY",
        E2RArchetype.AUTO_SDV_DELAY_CAPEX_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("sdv_ai_car_narrative", "software_defined_vehicle_plan"),
        stage2=("sdv_roadmap", "ai_partner", "nvidia_or_deepmind_partner"),
        stage3=("not_green_if_launch_delay_or_capex_hike",),
        stage4b=("sdv_narrative_priced_before_execution",),
        stage4c=("sdv_delay", "ev_target_cut", "capex_hike", "share_price_negative_reaction"),
        green=(),
        red=("sdv_delay", "ev_target_cut", "capex_hike", "share_price_negative_reaction"),
        penalties=("delay", "capex", "ev_target_cut", "execution"),
        note="SDV delay and capex hike are RedTeam gates, not software rerating evidence.",
        gate_only=True,
    ),
    _target(
        "AUTO_PRICE_WAR_EUROPE_OVERLAY",
        E2RArchetype.AUTO_PRICE_WAR_EUROPE_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("europe_sales_defense", "china_ev_competition"),
        stage2=("price_gap_reduction", "volume_defense"),
        stage3=("not_green_if_margin_cut_needed",),
        stage4b=("volume_story_ignores_margin_cap",),
        stage4c=("price_cut_signal", "gross_margin_pressure", "opm_cap", "china_ev_price_competition"),
        green=(),
        red=("price_cut_signal", "gross_margin_pressure", "opm_cap", "china_ev_price_competition"),
        penalties=("price_cut", "opm", "competition", "europe"),
        note="European price competition can defend revenue while capping margin.",
        gate_only=True,
    ),
    _target(
        "AUTO_COMPONENT_RESTRUCTURING_KOREA",
        E2RArchetype.AUTO_COMPONENT_RESTRUCTURING_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(20, 20, 14, 16, 10, 12, 8),
        stage1=("auto_parts_restructuring", "lighting_business", "adas_or_ev_component"),
        stage2=("lighting_business_scale", "opmobility_deal", "portfolio_restructuring", "customer_diversification"),
        stage3=("deal_finalized", "opm_improvement", "fcf_or_return_improvement", "quality_cost_low"),
        stage4b=("restructuring_premium_priced_before_deal",),
        stage4c=("iccu_quality_issue", "ev_recall", "warranty_cost", "customer_trust_damage"),
        green=("deal_finalized", "opm_improvement", "fcf_or_return_improvement", "quality_cost_low"),
        red=("iccu_quality_issue", "ev_recall", "warranty_cost", "customer_trust_damage"),
        penalties=("quality", "recall", "warranty", "deal_not_final"),
        note="Hyundai Mobis-style restructuring is Stage 2; Green waits for deal finality, OPM, FCF, and clean quality cost.",
    ),
    _target(
        "AUTO_COMPONENT_QUALITY_RECALL_OVERLAY",
        E2RArchetype.AUTO_COMPONENT_QUALITY_RECALL_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("ev_component_exposure", "electronics_component"),
        stage2=("component_program_visibility",),
        stage3=("not_green_if_quality_cost_active",),
        stage4b=("component_rerating_ignores_recall",),
        stage4c=("iccu_defect", "recall", "warranty_cost", "reputation_risk"),
        green=(),
        red=("iccu_defect", "recall", "warranty_cost", "reputation_risk"),
        penalties=("recall", "warranty", "quality", "trust"),
        note="Auto-component quality or recall evidence is a Green-blocking overlay.",
        gate_only=True,
    ),
    _target(
        "ECOMMERCE_LOGISTICS_REPEAT_CONTRACT",
        E2RArchetype.ECOMMERCE_LOGISTICS_REPEAT_CONTRACT,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(22, 22, 18, 12, 10, 10, 6),
        stage1=("ecommerce_logistics_competition", "fast_delivery", "customer_trust_shock"),
        stage2=("three_year_logistics_alliance", "incremental_revenue_potential", "one_day_volume_growth", "customer_diversification"),
        stage3=("parcel_unit_price_defended", "opm_fcf_improvement", "automation_efficiency", "repeat_customer_contracts", "labor_cost_controlled"),
        stage4b=("fast_delivery_basket_rally", "volume_story_priced_before_margin"),
        stage4c=("unit_price_down", "labor_regulation_cost", "volume_up_opm_down", "delivery_pause_or_operation_disruption"),
        green=("parcel_unit_price_defended", "opm_fcf_improvement", "automation_efficiency", "repeat_customer_contracts", "labor_cost_controlled"),
        red=("unit_price_down", "labor_regulation_cost", "volume_up_opm_down", "delivery_pause_or_operation_disruption"),
        penalties=("unit_price", "labor", "opm", "operation"),
        note="CJ Logistics-style repeat contract can become Green-capable only after unit price, OPM/FCF, automation, and labor costs confirm.",
    ),
    _target(
        "LOGISTICS_LABOR_REGULATION_OVERLAY",
        E2RArchetype.LOGISTICS_LABOR_REGULATION_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("parcel_volume_growth", "delivery_competition"),
        stage2=("labor_policy_change", "delivery_operation_pause"),
        stage3=("not_green_if_labor_cost_spikes",),
        stage4b=("volume_growth_ignores_labor_cost",),
        stage4c=("labor_regulation_cost", "delivery_pause", "courier_regulation", "unit_cost_spike"),
        green=(),
        red=("labor_regulation_cost", "delivery_pause", "courier_regulation", "unit_cost_spike"),
        penalties=("labor", "regulation", "unit_cost", "operation"),
        note="Logistics volume is capped when labor/regulation cost can erase OPM.",
        gate_only=True,
    ),
    _target(
        "CASINO_DUTYFREE_TOURISM_POLICY_KOREA",
        E2RArchetype.CASINO_DUTYFREE_TOURISM_POLICY_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(14, 18, 18, 14, 12, 14, 10),
        stage1=("china_group_visa_free", "casino_dutyfree_hotel_basket_rally", "tourism_policy"),
        stage2=("visa_free_execution", "payment_options", "cruise_or_group_tour_preparation", "visitor_arrivals"),
        stage3=("average_spend", "dutyfree_sales", "casino_drop_amount", "hold_rate", "revpar", "opm_fcf"),
        stage4b=("policy_news_basket_rally", "tourism_policy_priced_before_spend"),
        stage4c=("return_visitor_weak", "low_spend_tourist_mix", "policy_end", "tourist_safety_concern", "casino_drop_weak"),
        green=("average_spend", "dutyfree_sales", "casino_drop_amount", "hold_rate", "revpar", "opm_fcf"),
        red=("return_visitor_weak", "low_spend_tourist_mix", "policy_end", "tourist_safety_concern", "casino_drop_weak"),
        penalties=("spend_missing", "drop_missing", "return_visitor", "policy_event"),
        note="Tourism policy can move prices, but Green waits for spend, drop, RevPAR, and OPM/FCF.",
    ),
    _target(
        "CASINO_RETURN_VISITOR_UNIT_ECONOMICS",
        E2RArchetype.CASINO_RETURN_VISITOR_UNIT_ECONOMICS,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(20, 18, 22, 12, 10, 12, 6),
        stage1=("foreigner_only_casino", "jeju_casino", "tourist_recovery"),
        stage2=("visitor_arrivals", "casino_revenue", "hotel_occupancy", "payment_option"),
        stage3=("casino_drop_amount", "hold_rate", "return_visitor_rate", "average_spend", "revpar", "opm_fcf"),
        stage4b=("casino_policy_rally_before_drop",),
        stage4c=("return_visitor_weak", "drop_amount_weak", "hold_rate_weak", "debt_or_capex_burden", "low_spend_mix"),
        green=("casino_drop_amount", "hold_rate", "return_visitor_rate", "average_spend", "revpar", "opm_fcf"),
        red=("return_visitor_weak", "drop_amount_weak", "hold_rate_weak", "debt_or_capex_burden", "low_spend_mix"),
        penalties=("drop", "hold", "return_visitor", "debt"),
        note="Casino evidence can be Green-capable only when return visitors and unit economics confirm.",
    ),
    _target(
        "AIRLINE_SAFETY_REGULATORY_OVERLAY",
        E2RArchetype.AIRLINE_SAFETY_REGULATORY_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("lcc_recovery", "international_route_recovery"),
        stage2=("load_factor_recovery", "cost_normalization"),
        stage3=("not_green_if_safety_accident_or_inspection",),
        stage4b=("travel_recovery_ignores_safety",),
        stage4c=("fatal_accident", "safety_inspection", "travel_cancellation", "consumer_trust_damage", "operating_restriction"),
        green=(),
        red=("fatal_accident", "safety_inspection", "travel_cancellation", "consumer_trust_damage", "operating_restriction"),
        penalties=("safety", "inspection", "trust", "cancellation"),
        note="Airline safety accidents and inspections are hard 4C gates.",
        gate_only=True,
    ),
    _target(
        "SHIPPING_FREIGHT_CYCLE_KOREA",
        E2RArchetype.SHIPPING_FREIGHT_CYCLE_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(20, 12, 18, 14, 12, 8, 6),
        stage1=("freight_rate_spike", "red_sea_disruption", "spot_rate_rally"),
        stage2=("ebitda_increase", "dividend_or_cashflow_potential", "freight_index_improves"),
        stage3=("multi_year_supply_discipline", "contract_freight_visibility", "fleet_discipline", "cashflow_resilience"),
        stage4b=("freight_spike_basket_rally", "shipping_stocks_crowded"),
        stage4c=("route_normalization", "overcapacity", "freight_rate_decline", "new_vessel_supply", "earnings_downcycle"),
        green=("multi_year_supply_discipline", "contract_freight_visibility", "fleet_discipline", "cashflow_resilience"),
        red=("route_normalization", "overcapacity", "freight_rate_decline", "new_vessel_supply", "earnings_downcycle"),
        penalties=("freight_cycle", "overcapacity", "route_normalization", "new_supply"),
        note="Korea shipping can be a strong cycle, but structural Green is heavily restricted.",
    ),
    _target(
        "PARCEL_VOLUME_PRICE_COST_SPREAD",
        E2RArchetype.PARCEL_VOLUME_PRICE_COST_SPREAD,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(22, 20, 20, 12, 10, 10, 6),
        stage1=("parcel_volume_growth", "fast_delivery_competition"),
        stage2=("shipment_volume_growth", "customer_diversification", "automation_capex", "hub_efficiency"),
        stage3=("parcel_unit_price_defended", "delivery_cost_per_unit_down", "opm_fcf_improves", "automation_payback", "labor_cost_controlled"),
        stage4b=("parcel_volume_story_crowded",),
        stage4c=("unit_price_down", "delivery_cost_per_unit_up", "volume_up_opm_down", "labor_regulation_cost"),
        green=("parcel_unit_price_defended", "delivery_cost_per_unit_down", "opm_fcf_improves", "automation_payback", "labor_cost_controlled"),
        red=("unit_price_down", "delivery_cost_per_unit_up", "volume_up_opm_down", "labor_regulation_cost"),
        penalties=("unit_price", "unit_cost", "opm", "labor"),
        note="Parcel volume only matters when unit price, unit cost, automation payback, and OPM/FCF improve.",
    ),
    _target(
        "TRAVEL_AGENCY_POLICY_EVENT",
        E2RArchetype.TRAVEL_AGENCY_POLICY_EVENT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(14, 16, 12, 12, 12, 16, 10),
        stage1=("tourism_policy", "outbound_travel_recovery", "china_visa_free"),
        stage2=("departure_count", "package_asp", "reservation_growth", "tour_product_margin"),
        stage3=("package_asp_up", "opm_fcf_improves", "repeat_travel_demand", "cancellation_low"),
        stage4b=("policy_event_travel_basket_rally",),
        stage4c=("asp_missing", "departure_count_missing", "opm_missing", "policy_only_rally", "cancellation_spike"),
        green=("package_asp_up", "opm_fcf_improves", "repeat_travel_demand", "cancellation_low"),
        red=("asp_missing", "departure_count_missing", "opm_missing", "policy_only_rally", "cancellation_spike"),
        penalties=("asp", "opm", "policy_only", "cancellation"),
        note="Travel-agency policy rallies stay Stage 1/2 until package ASP, departures, and OPM confirm.",
    ),
    _target(
        "DISCLOSURE_CONFIDENCE_CAP",
        E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        Round10ThemePosture.REDTEAM_FIRST,
        CAP_WEIGHT,
        stage1=("freight_policy_contract_headline", "tourism_policy_headline", "hybrid_localization_headline"),
        stage2=("contract_amount_required", "freight_rate_required", "casino_drop_required", "opm_required", "unit_economics_required"),
        stage3=("multi_source_confirmation", "unit_economics_verified", "opm_fcf_verified"),
        stage4b=("headline_rerating",),
        stage4c=("contract_amount_missing", "freight_rate_missing", "casino_drop_missing", "opm_missing", "unit_economics_missing"),
        green=("contract_amount", "freight_rate", "casino_drop", "opm_fcf", "unit_economics"),
        red=("contract_amount_missing", "freight_rate_missing", "casino_drop_missing", "opm_missing", "unit_economics_missing"),
        penalties=("disclosure", "detail", "opm_fcf", "unit_economics"),
        note="R9 disclosure confidence is capped when contract, freight, casino drop, OPM, or unit-economics detail is missing.",
    ),
)


ROUND180_SCORE_STAGE_PRICE_ALIGNMENT: tuple[Round180ScoreStagePriceAlignment, ...] = (
    Round180ScoreStagePriceAlignment("kia_hybrid_localization_sdv_delay_stage2_4c_watch_case", "Stage 2 plus 4C-watch", "Hybrid localization is positive, but SDV delay and capex hike drove a negative price reaction", "hybrid_stage2_not_green_until_opm_tariff", "score localization as Stage 2; keep SDV delay, EV target cut, capex hike, and Europe price war as RedTeam gates"),
    Round180ScoreStagePriceAlignment("cj_logistics_shinsegae_oneday_volume_stage2_3_case", "Stage 2 to Stage 3 candidate", "Three-year alliance and +120% one-day volume need parcel unit price and OPM backfill", "logistics_volume_needs_unit_margin", "promote only after unit price, automation payback, OPM/FCF, and labor cost control confirm"),
    Round180ScoreStagePriceAlignment("tourism_visa_free_dutyfree_casino_policy_event_case", "Stage 1/2 event plus 4B-watch", "Visa-free policy moved hotel/casino/duty-free names before spend/drop evidence", "tourism_policy_not_green_before_spend_drop", "treat policy reaction as price-path evidence, not Stage 3 proof"),
    Round180ScoreStagePriceAlignment("jeju_air_muan_crash_hard_4c_case", "hard 4C", "Fatal accident and safety inspection override LCC recovery", "airline_safety_hard_gate", "immediate Green block and 4C-watch regardless of demand recovery"),
    Round180ScoreStagePriceAlignment("hmm_pan_ocean_freight_cycle_4b_4c_watch_case", "cycle/4B/4C watch", "Freight spikes can lift prices, but route normalization and overcapacity can break earnings", "shipping_cycle_green_restricted", "cool shipping when freight normalizes or price outruns rate/EBITDA evidence"),
)


def _d(value: str) -> date:
    return date.fromisoformat(value)


ROUND180_CASE_CANDIDATES: tuple[Round180CaseCandidate, ...] = (
    Round180CaseCandidate(
        "kia_hybrid_localization_sdv_delay_stage2_4c_watch_case",
        "AUTO_HYBRID_LOCALIZATION_KOREA",
        "000270",
        "Kia hybrid US localization with SDV delay and price-war overlay",
        "KR",
        "success_candidate",
        None,
        _d("2025-03-28"),
        None,
        None,
        _d("2026-04-09"),
        ("georgia_hybrid_production", "kia_40pct_georgia_allocation", "us_capacity_1_2m", "tariff_hedge", "hybrid_localization"),
        ("sdv_delay", "ev_target_cut_20pct", "capex_hike_30pct", "europe_price_war", "share_price_minus_5_5pct"),
        "stage2_hybrid_localization_with_4c_watch",
        "needs_kia_opm_tariff_hybrid_mix_price_backfill",
        ("round_180.md Reuters Kia hybrid Georgia case", "round_180.md Reuters Kia SDV delay case", "round_180.md Reuters Kia Europe price war case"),
        "Kia hybrid localization is Stage 2 evidence, but SDV delay, EV target cut, capex hike, and Europe price competition block Green until OPM/FCF and tariff absorption are proven.",
        (E2RArchetype.AUTO_SDV_DELAY_CAPEX_OVERLAY, E2RArchetype.AUTO_PRICE_WAR_EUROPE_OVERLAY),
    ),
    Round180CaseCandidate(
        "hyundai_mobis_lighting_restructuring_quality_recall_case",
        "AUTO_COMPONENT_RESTRUCTURING_KOREA",
        "012330",
        "Hyundai Mobis lighting restructuring with ICCU quality overlay",
        "KR",
        "success_candidate",
        None,
        _d("2026-01-27"),
        None,
        None,
        None,
        ("opmobility_lighting_stake_talks", "lighting_revenue_over_1bn_eur", "portfolio_restructuring", "customer_diversification_option"),
        ("deal_not_final", "iccu_quality_issue", "ev_recall", "warranty_cost_risk", "customer_trust_damage"),
        "stage2_restructuring_with_quality_cap",
        "needs_deal_finality_opm_quality_cost_price_backfill",
        ("round_180.md OPmobility Hyundai Mobis lighting case", "round_180.md ICCU recall discussion"),
        "Hyundai Mobis restructuring can be Stage 2, but quality and warranty cost must remain clean before Stage 3.",
        (E2RArchetype.AUTO_COMPONENT_QUALITY_RECALL_OVERLAY,),
    ),
    Round180CaseCandidate(
        "cj_logistics_shinsegae_oneday_volume_stage2_3_case",
        "ECOMMERCE_LOGISTICS_REPEAT_CONTRACT",
        "000120",
        "CJ Logistics Shinsegae alliance and one-day delivery volume",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("shinsegae_3y_logistics_alliance", "300bn_krw_incremental_revenue_potential", "one_day_overnight_volume_120pct_growth", "customer_diversification", "naver_customer_option"),
        ("parcel_unit_price_unknown", "labor_cost_risk", "opm_fcf_backfill_needed", "domestic_growth_slowdown", "overseas_recovery_delay"),
        "stage2_3_logistics_candidate_needs_unit_margin",
        "needs_parcel_unit_price_opm_fcf_labor_price_backfill",
        ("round_180.md MarketWatch CJ Logistics Shinsegae case", "round_180.md Reuters Coupang breach competition case"),
        "CJ Logistics is a Stage 2/3 candidate only if contract volume converts into parcel unit price defense, automation efficiency, OPM, and FCF.",
        (E2RArchetype.PARCEL_VOLUME_PRICE_COST_SPREAD, E2RArchetype.LOGISTICS_LABOR_REGULATION_OVERLAY),
    ),
    Round180CaseCandidate(
        "tourism_visa_free_dutyfree_casino_policy_event_case",
        "CASINO_DUTYFREE_TOURISM_POLICY_KOREA",
        "008770/034230/114090/032350",
        "Hotel Shilla Paradise GKL Lotte Tour tourism visa-free policy basket",
        "KR",
        "event_premium",
        _d("2025-08-06"),
        _d("2025-09-29"),
        None,
        _d("2025-08-06"),
        None,
        ("china_group_visa_free_policy", "hotel_shilla_4_8pct", "paradise_2_9pct", "hyundai_department_7_1pct", "korea_cosmetics_9_9pct", "visa_free_execution", "payment_option_expansion"),
        ("actual_spend_missing", "casino_drop_missing", "return_visitor_risk", "policy_event_4b", "low_spend_tourist_mix"),
        "policy_price_reaction_not_green_before_spend_drop",
        "needs_spend_drop_revpar_opm_price_backfill",
        ("round_180.md Reuters China group visa-free policy case", "round_180.md Reuters visa-free execution case"),
        "Tourism policy moved prices, but Stage 3 waits for visitor spend, casino drop, hold rate, RevPAR, and OPM/FCF.",
        (E2RArchetype.CASINO_RETURN_VISITOR_UNIT_ECONOMICS,),
    ),
    Round180CaseCandidate(
        "casino_return_visitor_unit_economics_gate_case",
        "CASINO_RETURN_VISITOR_UNIT_ECONOMICS",
        "032350/034230/114090",
        "Jeju Dream Tower Paradise GKL return visitor and casino unit economics gate",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("jeju_dream_tower_casino", "foreigner_only_casino", "visitor_arrivals_needed", "casino_drop_amount_needed", "hotel_revpar_needed"),
        ("return_visitor_weak", "low_spend_tourist_mix", "hold_rate_missing", "revpar_missing", "debt_or_capex_burden"),
        "casino_stage2_3_requires_drop_hold_return_visitor",
        "needs_casino_drop_hold_return_visitor_revpar_price_backfill",
        ("round_180.md FT Inspire casino return visitor warning",),
        "Casino names need return visitor, drop, hold rate, spend, RevPAR, and cash-flow data before Green.",
    ),
    Round180CaseCandidate(
        "jeju_air_muan_crash_hard_4c_case",
        "AIRLINE_SAFETY_REGULATORY_OVERLAY",
        "089590",
        "Jeju Air Muan crash hard safety 4C",
        "KR",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        _d("2024-12-30"),
        ("lcc_recovery_prior", "international_route_recovery_prior"),
        ("muan_crash_179_fatalities", "share_price_intraday_minus_15_7pct", "safety_inspection", "travel_cancellation", "consumer_trust_damage"),
        "airline_safety_hard_4c",
        "needs_accident_event_price_backfill",
        ("round_180.md Reuters Jeju Air crash case",),
        "Airline demand recovery is overridden by fatal safety accident, inspection, cancellations, and trust damage.",
    ),
    Round180CaseCandidate(
        "hmm_pan_ocean_freight_cycle_4b_4c_watch_case",
        "SHIPPING_FREIGHT_CYCLE_KOREA",
        "011200/028670",
        "HMM and Pan Ocean freight cycle 4B/4C watch",
        "KR",
        "4b_watch",
        None,
        None,
        None,
        None,
        None,
        ("freight_rate_up", "ebitda_cycle", "red_sea_disruption", "dividend_cashflow_option"),
        ("overcapacity", "route_normalization", "freight_downcycle", "new_vessel_supply", "earnings_downcycle"),
        "shipping_cycle_watch_green_restricted",
        "needs_freight_index_ebitda_price_backfill",
        ("round_180.md Reuters Maersk freight normalization case", "round_180.md Reuters Hapag-Lloyd freight case"),
        "Korea shipping can rally on freight, but route normalization and overcapacity require 4B/4C cooling before structural Green.",
    ),
    Round180CaseCandidate(
        "kia_sdv_delay_capex_price_war_overlay_case",
        "AUTO_SDV_DELAY_CAPEX_OVERLAY",
        "000270",
        "Kia SDV delay capex hike and Europe price-war overlay",
        "KR",
        "4c_thesis_break",
        None,
        _d("2026-04-09"),
        None,
        None,
        _d("2026-04-09"),
        ("sdv_roadmap", "ai_car_narrative", "hybrid_localization_context"),
        ("sdv_delay_2027_to_2028", "ev_target_cut_20pct", "capex_hike_30pct", "share_price_minus_5_5pct", "europe_price_gap_pressure"),
        "sdv_strategy_event_is_not_green_if_delay_capex_margin_breaks",
        "needs_sdv_event_price_backfill",
        ("round_180.md Reuters Kia SDV delay case", "round_180.md Reuters Europe price competition case"),
        "SDV and AI-car narratives are capped when launch timing, capex, EV targets, and pricing power worsen.",
    ),
    Round180CaseCandidate(
        "hyundai_mobis_iccu_quality_recall_overlay_case",
        "AUTO_COMPONENT_QUALITY_RECALL_OVERLAY",
        "012330",
        "Hyundai Mobis ICCU quality and recall overlay",
        "KR",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        None,
        ("ev_component_exposure", "component_program_visibility"),
        ("iccu_defect", "korea_us_recall", "warranty_cost", "reputation_risk"),
        "component_quality_cost_blocks_green",
        "needs_recall_cost_price_backfill",
        ("round_180.md ICCU quality recall case",),
        "Auto components need quality and warranty-cost checks before customer CAPEX or EV content can support Green.",
    ),
    Round180CaseCandidate(
        "cj_logistics_labor_regulation_margin_cap_case",
        "LOGISTICS_LABOR_REGULATION_OVERLAY",
        "000120/002320",
        "CJ Logistics and Hanjin labor regulation margin cap",
        "KR",
        "failed_rerating",
        None,
        _d("2025-06-03"),
        None,
        None,
        None,
        ("parcel_volume_growth", "fast_delivery_competition", "delivery_operation_pause"),
        ("election_day_delivery_pause", "labor_regulation_cost", "unit_price_pressure", "opm_risk"),
        "volume_without_margin_labor_cap",
        "needs_labor_cost_unit_price_price_backfill",
        ("round_180.md Reuters delivery workers election pause case",),
        "Parcel volume growth is capped when labor, regulation, unit price, and OPM risks are unresolved.",
    ),
    Round180CaseCandidate(
        "travel_agency_policy_event_stage1_2_case",
        "TRAVEL_AGENCY_POLICY_EVENT",
        "039130/080160",
        "HanaTour ModeTour travel-agency policy event watch",
        "KR",
        "event_premium",
        _d("2025-08-06"),
        None,
        None,
        _d("2025-08-06"),
        None,
        ("china_tourism_policy", "travel_reopening", "outbound_package_option", "travel_basket_rally"),
        ("package_asp_missing", "departure_count_missing", "opm_missing", "policy_only_rally"),
        "travel_policy_event_not_green_before_asp_opm",
        "needs_departure_asp_opm_price_backfill",
        ("round_180.md China visa-free tourism policy case",),
        "Travel agency policy events can be Stage 1/2, but Green waits for departures, package ASP, OPM, and repeat travel demand.",
    ),
    Round180CaseCandidate(
        "r9_disclosure_confidence_cap_case",
        "DISCLOSURE_CONFIDENCE_CAP",
        "KR_R9_DISCLOSURE_BASKET",
        "Korea R9 disclosure confidence cap basket",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("freight_policy_contract_headline", "tourism_policy_headline", "hybrid_localization_headline"),
        ("contract_amount_missing", "freight_rate_missing", "casino_drop_missing", "opm_missing", "unit_economics_missing"),
        "disclosure_detail_missing_cap",
        "needs_contract_freight_drop_opm_unit_economics_backfill",
        ("round_180.md R9 disclosure confidence cap",),
        "R9 headlines are capped when contract amount, freight rate, casino drop, OPM/FCF, or unit economics are missing.",
    ),
)


ROUND180_PRICE_FIELDS: tuple[str, ...] = (
    "ticker",
    "company_name",
    "stage1_date",
    "stage2_date",
    "stage3_date",
    "stage4b_date",
    "stage4c_date",
    "stage1_trigger",
    "stage2_trigger",
    "stage3_trigger",
    "stage4b_trigger",
    "stage4c_trigger",
    "price_at_stage1",
    "price_at_stage2",
    "price_at_stage3",
    "price_at_stage4b",
    "price_at_stage4c",
    "return_1d_after_event",
    "return_5d_after_event",
    "return_20d_after_stage2",
    "return_60d_after_stage2",
    "return_120d_after_stage2",
    "return_252d_after_stage2",
    "mfe_60d_after_stage2",
    "mae_60d_after_stage2",
    "mfe_120d_after_stage2",
    "mae_120d_after_stage2",
    "mfe_252d_after_stage2",
    "mae_252d_after_stage2",
    "relative_strength_vs_kospi",
    "relative_strength_vs_transport_basket",
    "relative_strength_vs_auto_basket",
    "relative_strength_vs_tourism_basket",
    "relative_strength_vs_shipping_basket",
    "op_revision_before_stage3",
    "op_revision_after_stage3",
    "eps_revision_before_stage3",
    "eps_revision_after_stage3",
    "vehicle_sales_volume",
    "hybrid_mix",
    "us_localization_ratio",
    "tariff_cost",
    "price_cut_signal",
    "sdv_delay_flag",
    "capex_hike_flag",
    "parcel_volume",
    "parcel_unit_price",
    "delivery_cost_per_unit",
    "automation_capex",
    "labor_regulation_flag",
    "visitor_arrivals",
    "average_spend",
    "duty_free_sales",
    "casino_drop_amount",
    "casino_hold_rate",
    "hotel_revpar",
    "freight_rate_index",
    "teu_or_bulk_volume",
    "vessel_supply_growth",
    "red_sea_route_normalization_flag",
    "safety_accident_flag",
    "recall_flag",
    "quality_cost_flag",
    "insurance_compensation_flag",
    "disclosure_confidence",
    "valuation_at_stage3",
    "valuation_at_stage4b",
)


def round180_target_for(target_id: str) -> Round180ScoreTarget | None:
    for target in ROUND180_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round180_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND180_CASE_CANDIDATES:
        target = round180_target_for(candidate.target_id)
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
                f"Round180 R9 Loop-11 case for {candidate.target_id}; "
                "Korea mobility, transport, and leisure headlines are separated from OPM, FCF, repeat contracts, unit economics, safety, quality, labor, and price-path evidence."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage2_signals or field in target.green_conditions),
            stage3_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage3_conditions or field in target.green_conditions),
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
                "mobility_tourism_freight_hybrid_headline_is_not_stage3",
                "require_opm_fcf_unit_economics_repeat_contract_or_repeat_demand_for_green",
                "stage3_early_catch_requires_5_of_8_loop11_conditions",
                "do_not_invent_contract_amount_freight_rate_casino_drop_opm_unit_economics_stage_prices_or_mfe_mae",
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


def round180_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND180_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "eps_fcf_opm_conversion": str(weights["eps_fcf_opm_conversion"]),
                "contract_volume_operating_visibility": str(weights["contract_volume_operating_visibility"]),
                "unit_fleet_economics": str(weights["unit_fleet_economics"]),
                "safety_regulation_labor_quality_risk": str(weights["safety_regulation_labor_quality_risk"]),
                "early_price_path_validation": str(weights["early_price_path_validation"]),
                "recurrence_demand_durability": str(weights["recurrence_demand_durability"]),
                "valuation_room_4b_runway": str(weights["valuation_room_4b_runway"]),
                "stage1_signals": "|".join(target.stage1_signals),
                "stage2_signals": "|".join(target.stage2_signals),
                "stage3_conditions": "|".join(target.stage3_conditions),
                "stage4b_conditions": "|".join(target.stage4b_conditions),
                "stage4c_conditions": "|".join(target.stage4c_conditions),
                "green_conditions": "|".join(target.green_conditions),
                "red_flags": "|".join(target.red_flags),
                "loop11_penalty_axes": "|".join(target.loop11_penalty_axes),
                "gate_only": str(target.gate_only).lower(),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round180_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND180_CASE_CANDIDATES:
        target = round180_target_for(candidate.target_id)
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


def round180_stage_date_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "target_id": target.target_id,
            "stage1": "|".join(target.stage1_signals),
            "stage2": "|".join(target.stage2_signals),
            "stage3": "|".join(target.stage3_conditions),
            "stage4b": "|".join(target.stage4b_conditions),
            "stage4c": "|".join(target.stage4c_conditions),
            "red_flags": "|".join(target.red_flags),
            "loop11_penalty_axes": "|".join(target.loop11_penalty_axes),
            "gate_only": str(target.gate_only).lower(),
            "production_scoring_changed": "false",
        }
        for target in ROUND180_SCORE_TARGETS
    )


def round180_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round180_backfill": "true"} for field in ROUND180_PRICE_FIELDS)


def round180_base_score_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "component": item.component,
            "points": str(item.points),
            "loop11_direction": item.loop11_direction,
            "reason": item.reason,
            "production_scoring_changed": "false",
        }
        for item in ROUND180_BASE_SCORE_WEIGHTS
    )


def round180_stage_cap_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "stage_band": item.stage_band,
            "max_score": item.max_score,
            "required_evidence": "|".join(item.required_evidence),
            "example_cases": "|".join(item.example_cases),
            "green_policy": item.green_policy,
            "production_scoring_changed": "false",
        }
        for item in ROUND180_STAGE_CAPS
    )


def round180_score_stage_price_alignment_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "case_id": item.case_id,
            "detected_stage": item.detected_stage,
            "price_path_status": item.price_path_status,
            "verdict": item.verdict,
            "normalization_adjustment": item.normalization_adjustment,
            "production_scoring_changed": "false",
        }
        for item in ROUND180_SCORE_STAGE_PRICE_ALIGNMENT
    )


def round180_summary() -> dict[str, int | bool]:
    records = round180_case_records()
    return {
        "target_count": len(ROUND180_SCORE_TARGETS),
        "source_canonical_target_count": ROUND180_SOURCE_CANONICAL_TARGET_COUNT,
        "case_candidate_count": len(records),
        "base_score_component_count": len(ROUND180_BASE_SCORE_WEIGHTS),
        "stage_cap_count": len(ROUND180_STAGE_CAPS),
        "score_stage_price_alignment_count": len(ROUND180_SCORE_STAGE_PRICE_ALIGNMENT),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND180_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND180_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND180_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "gate_only_target_count": sum(1 for target in ROUND180_SCORE_TARGETS if target.gate_only),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round180_r9_loop11_reports(
    *,
    output_directory: str | Path = ROUND180_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND180_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND180_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round180_r9_loop11_mobility_transport_leisure_summary.md",
        "case_matrix": output / "round180_r9_loop11_case_matrix.csv",
        "stage_date_plan": output / "round180_r9_loop11_stage_date_plan.csv",
        "green_guardrails": output / "round180_r9_loop11_green_guardrails.md",
        "risk_overlays": output / "round180_r9_loop11_risk_overlays.md",
        "price_validation_plan": output / "round180_r9_loop11_price_validation_plan.md",
        "price_fields": output / "round180_r9_loop11_price_fields.csv",
        "base_score_weights": output / "round180_r9_loop11_base_score_weights.csv",
        "stage_caps": output / "round180_r9_loop11_stage_caps.csv",
        "score_stage_price_alignment": output / "round180_r9_loop11_score_stage_price_alignment.csv",
        "score_stage_price_alignment_md": output / "round180_r9_loop11_score_stage_price_alignment.md",
    }
    _write_case_jsonl(round180_case_records(), cases)
    _write_rows(round180_score_profile_rows(), score_profiles)
    _write_rows(round180_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round180_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round180_price_field_rows(), paths["price_fields"])
    _write_rows(round180_base_score_weight_rows(), paths["base_score_weights"])
    _write_rows(round180_stage_cap_rows(), paths["stage_caps"])
    _write_rows(round180_score_stage_price_alignment_rows(), paths["score_stage_price_alignment"])
    paths["summary"].write_text(render_round180_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round180_green_guardrail_markdown(), encoding="utf-8")
    paths["risk_overlays"].write_text(render_round180_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round180_price_validation_plan_markdown(), encoding="utf-8")
    paths["score_stage_price_alignment_md"].write_text(render_round180_score_stage_price_alignment_markdown(), encoding="utf-8")
    return paths


def render_round180_summary_markdown() -> str:
    summary = round180_summary()
    lines = [
        "# Round-180 R9 Loop-11 Korea Mobility / Transport / Leisure Summary",
        "",
        f"- source_round: `{ROUND180_SOURCE_ROUND_PATH}`",
        "- large_sector: `MOBILITY_TRANSPORT_LEISURE`",
        "- loop: `R9 Loop 11 / v11.0`",
        f"- target_count: {summary['target_count']}",
        f"- source_canonical_target_count: {summary['source_canonical_target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- base_score_component_count: {summary['base_score_component_count']}",
        f"- stage_cap_count: {summary['stage_cap_count']}",
        f"- score_stage_price_alignment_count: {summary['score_stage_price_alignment_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
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
        "- R9 Loop 11 separates hybrid, tourism, freight, casino, duty-free, parcel, and travel headlines from OPM/FCF and unit economics.",
        "- Example: Kia hybrid localization is Stage 2 evidence, but SDV delay and capex hike are 4C-watch inputs.",
        "- Example: CJ Logistics volume growth is useful only if parcel unit price, automation payback, OPM, and FCF improve.",
        "- Example: Hotel Shilla or Paradise can rally on visa policy, but Green waits for spend, casino drop, hold rate, RevPAR, and OPM/FCF.",
        "- Example: Jeju Air safety accident is a hard 4C gate even if LCC travel demand had been recovering.",
    ]
    return "\n".join(lines) + "\n"


def render_round180_green_guardrail_markdown() -> str:
    lines = [
        "# Round-180 R9 Loop-11 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Loop-11 penalties |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND180_SCORE_TARGETS:
        lines.append(
            "| "
            f"`{target.target_id}` | {target.posture.value} | "
            f"{', '.join(target.green_conditions)} | {', '.join(target.loop11_penalty_axes)} |"
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not apply R9 Loop-11 v11.0 weights to production scoring yet.",
            "- Do not treat hybrid, localization, tourism policy, freight spike, parcel volume, casino recovery, or duty-free headline as Green evidence by itself.",
            "- Do not invent contract amount, freight rate, casino drop, OPM, FCF, unit economics, stage prices, or MFE/MAE.",
            "- Green requires OPM/FCF conversion, repeat contract or recurring demand, unit economics, clean safety/quality/regulatory status, and price-path support.",
            "- Safety accident, recall, warranty cost, labor regulation, price war, freight overcapacity, weak spend/drop, and low disclosure confidence remain RedTeam gates.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round180_risk_overlay_markdown() -> str:
    lines = [
        "# Round-180 R9 Loop-11 Risk Overlays",
        "",
        "| target | stage4c conditions | red flags |",
        "| --- | --- | --- |",
    ]
    for target in ROUND180_SCORE_TARGETS:
        if target.red_flags or target.gate_only:
            lines.append(f"| `{target.target_id}` | {', '.join(target.stage4c_conditions)} | {', '.join(target.red_flags)} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- R9 is especially sensitive to safety, quality, labor, freight cycle, and unit-economics breaks.",
            "- Example: visitor count without spend/drop is not enough for casino or duty-free Green.",
            "- Example: parcel volume without unit price and OPM can become 4C-watch rather than Stage 3.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round180_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-180 R9 Loop-11 Price Validation Plan",
        "",
        "R9 needs event-date price-path validation because policy, safety, freight, and hybrid events can move prices before fundamentals confirm.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND180_PRICE_FIELDS)
    lines.extend(
        [
            "",
            "## Case Backfill Priorities",
            "",
            "- `kia_hybrid_localization_sdv_delay_stage2_4c_watch_case`: hybrid mix, tariff cost, OPM, FCF, and SDV event price reaction.",
            "- `cj_logistics_shinsegae_oneday_volume_stage2_3_case`: parcel volume, unit price, delivery cost per unit, automation payback, OPM, and FCF.",
            "- `tourism_visa_free_dutyfree_casino_policy_event_case`: visitor arrivals, average spend, duty-free sales, casino drop, hold rate, RevPAR, and OPM.",
            "- `jeju_air_muan_crash_hard_4c_case`: accident date price reaction, cancellations, safety inspection, and insurance/compensation impacts.",
            "- `hmm_pan_ocean_freight_cycle_4b_4c_watch_case`: freight index, TEU/bulk volume, vessel supply, Red Sea route normalization, EBITDA, and price-path MFE/MAE.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round180_score_stage_price_alignment_markdown() -> str:
    lines = [
        "# Round-180 R9 Loop-11 Score / Stage / Price Alignment",
        "",
        "| case | detected stage | price path status | verdict | adjustment |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in ROUND180_SCORE_STAGE_PRICE_ALIGNMENT:
        lines.append(f"| `{row.case_id}` | {row.detected_stage} | {row.price_path_status} | {row.verdict} | {row.normalization_adjustment} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Kia and Hyundai Mobis show why strategic narratives must be split from execution and quality gates.",
            "- CJ Logistics shows why volume must be tied to unit margin.",
            "- Tourism and shipping show why price reaction can be Stage 1/2 or 4B-watch without Green.",
            "- Jeju Air shows why safety can override demand recovery immediately.",
        ]
    )
    return "\n".join(lines) + "\n"


def _score_weight_hint(target: Round180ScoreTarget) -> Mapping[str, float]:
    values: dict[str, float] = {}
    for key, value in target.score_weight.as_dict().items():
        if isinstance(value, int):
            values[key] = float(value)
    return values


def _score_price_alignment(candidate: Round180CaseCandidate) -> str:
    if candidate.case_type == "event_premium":
        return "price_moved_without_evidence"
    if candidate.case_type == "4c_thesis_break":
        return "false_positive_score"
    if candidate.case_type == "failed_rerating":
        return "evidence_good_but_price_failed"
    if candidate.case_type == "4b_watch":
        return "price_moved_without_evidence"
    return "unknown"


def _rerating_result(candidate: Round180CaseCandidate) -> str:
    if candidate.case_type == "event_premium":
        return "policy_event_rerating"
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    if candidate.case_type == "failed_rerating":
        return "no_rerating"
    if candidate.target_id == "SHIPPING_FREIGHT_CYCLE_KOREA":
        return "cyclical_rerating"
    return "unknown"


def _write_case_jsonl(records: Iterable[E2RCaseRecord], path: Path) -> None:
    lines = []
    for record in records:
        record.validate()
        lines.append(json.dumps(record.as_dict(), ensure_ascii=False, sort_keys=True))
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def _write_rows(rows: Iterable[Mapping[str, str]], path: Path) -> None:
    rows = tuple(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


__all__ = [
    "ROUND180_BASE_SCORE_WEIGHTS",
    "ROUND180_CASE_CANDIDATES",
    "ROUND180_DEFAULT_CASES_PATH",
    "ROUND180_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND180_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND180_PRICE_FIELDS",
    "ROUND180_SCORE_STAGE_PRICE_ALIGNMENT",
    "ROUND180_SCORE_TARGETS",
    "ROUND180_SOURCE_CANONICAL_TARGET_COUNT",
    "ROUND180_SOURCE_CANONICAL_TARGET_IDS",
    "ROUND180_STAGE_CAPS",
    "render_round180_green_guardrail_markdown",
    "render_round180_price_validation_plan_markdown",
    "render_round180_risk_overlay_markdown",
    "render_round180_score_stage_price_alignment_markdown",
    "render_round180_summary_markdown",
    "round180_base_score_weight_rows",
    "round180_case_candidate_rows",
    "round180_case_records",
    "round180_price_field_rows",
    "round180_score_profile_rows",
    "round180_score_stage_price_alignment_rows",
    "round180_stage_cap_rows",
    "round180_stage_date_rows",
    "round180_summary",
    "round180_target_for",
    "write_round180_r9_loop11_reports",
]
