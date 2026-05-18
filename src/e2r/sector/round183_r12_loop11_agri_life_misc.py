"""Round-183 R12 Loop-11 Korea agriculture, life services, and misc pack.

Round 183 keeps R12 Korea-focused. It recalibrates agriculture machinery,
fertilizer/feed, livestock disease events, tuna/legal risk, regulated
consumer, heated tobacco, education policy, AI tutor disruption, kids IP,
smart farm, and kiosk themes.

This is calibration/report material only. Production feature engineering,
scoring, staging, and RedTeam code must not import it.
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


ROUND183_SOURCE_ROUND_PATH = "docs/round/round_183.md"
ROUND183_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round183_r12_loop11_agri_life_misc"
ROUND183_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r12_loop11_round183.jsonl"
ROUND183_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round183_r12_loop11_v11.csv"
ROUND183_SOURCE_CANONICAL_TARGET_IDS: tuple[str, ...] = (
    "AGRI_MACHINERY_EXPORT_CYCLE_KOREA",
    "AGRI_MACHINERY_AUTONOMOUS_ROBOT_OPTION",
    "FERTILIZER_INPUT_PRICE_COST_KOREA",
    "LIVESTOCK_DISEASE_PRICE_EVENT_KOREA",
    "FEED_GRAIN_COST_PASS_THROUGH",
    "TUNA_FISHERY_GLOBAL_BRAND_LEGAL_RISK",
    "CONSUMER_REGULATED_PRODUCT_KOREA",
    "HEATED_TOBACCO_GLOBAL_DISTRIBUTION",
    "EDUCATION_POLICY_EVENT_KOREA",
    "EDTECH_AI_DISRUPTION_KOREA",
    "KIDS_IP_PLATFORM_KOREA",
    "SMART_FARM_UNIT_ECONOMICS_KOREA",
    "SERVICE_KIOSK_LOCAL_REGULATION_KOREA",
    "DISCLOSURE_CONFIDENCE_CAP",
)
ROUND183_SOURCE_CANONICAL_TARGET_COUNT = len(ROUND183_SOURCE_CANONICAL_TARGET_IDS)


@dataclass(frozen=True)
class Round183ScoreWeightDraft:
    eps_fcf_opm_conversion: int | str
    recurring_order_regulatory_visibility: int | str
    unit_economics_pass_through_demand_durability: int | str
    price_path_early_validation: int | str
    regulation_litigation_public_health_disclosure: int | str
    capital_discipline_debt_cash_runway: int | str
    valuation_room_4b_margin: int | str

    def as_dict(self) -> dict[str, int | str]:
        return {
            "eps_fcf_opm_conversion": self.eps_fcf_opm_conversion,
            "recurring_order_regulatory_visibility": self.recurring_order_regulatory_visibility,
            "unit_economics_pass_through_demand_durability": self.unit_economics_pass_through_demand_durability,
            "price_path_early_validation": self.price_path_early_validation,
            "regulation_litigation_public_health_disclosure": self.regulation_litigation_public_health_disclosure,
            "capital_discipline_debt_cash_runway": self.capital_discipline_debt_cash_runway,
            "valuation_room_4b_margin": self.valuation_room_4b_margin,
        }


@dataclass(frozen=True)
class Round183BaseScoreAxis:
    axis_id: str
    points: int
    loop11_direction: str
    reason: str


@dataclass(frozen=True)
class Round183StageCap:
    stage_band: str
    max_score: str
    required_evidence: tuple[str, ...]
    example_cases: tuple[str, ...]
    green_policy: str


@dataclass(frozen=True)
class Round183ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round183ScoreWeightDraft
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
        return Round10LargeSector.EDUCATION_LIFE_AGRI_MISC

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round183CaseCandidate:
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
class Round183ScoreStagePriceAlignment:
    case_id: str
    detected_stage: str
    price_path_status: str
    verdict: str
    normalization_adjustment: str


def _weights(
    eps: int | str,
    visibility: int | str,
    unit: int | str,
    price: int | str,
    regulation: int | str,
    capital: int | str,
    valuation: int | str,
) -> Round183ScoreWeightDraft:
    return Round183ScoreWeightDraft(eps, visibility, unit, price, regulation, capital, valuation)


def _target(
    target_id: str,
    archetype: E2RArchetype,
    posture: Round10ThemePosture,
    weight: Round183ScoreWeightDraft,
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
) -> Round183ScoreTarget:
    return Round183ScoreTarget(target_id, archetype, posture, weight, stage1, stage2, stage3, stage4b, stage4c, green, red, penalties, note, gate_only)


def _d(value: str) -> date:
    return date.fromisoformat(value)


GATE_WEIGHT = _weights("gate", "gate", "gate", "gate", "gate", "gate", "gate")
CAP_WEIGHT = _weights("cap", "cap", "cap", "cap", "+", "cap", "cap")

ROUND183_BASE_SCORE_AXES: tuple[Round183BaseScoreAxis, ...] = (
    Round183BaseScoreAxis("eps_fcf_opm_conversion", 22, "raise_actual_conversion", "R12 stories can start from disease, policy, AI, IP, or commodity news, but OP/EPS/FCF and OPM conversion decide stage promotion."),
    Round183BaseScoreAxis("recurring_order_regulatory_visibility", 20, "raise_repeatability", "Repeat revenue, repeat contract, export channel, regulated distribution, licensing, FDA/regulatory scope, and subscriptions matter more than theme labels."),
    Round183BaseScoreAxis("unit_economics_pass_through_demand_durability", 18, "raise_unit_economics", "Farm income, dealer inventory, feed cost, CAC, churn, IP diversification, fuel cost, and price pass-through determine durability."),
    Round183BaseScoreAxis("price_path_early_validation", 10, "capture_but_cool_event_price", "IPO pops and event rallies validate Stage 1/2 price-path, but they often need 4B-watch."),
    Round183BaseScoreAxis("regulation_litigation_public_health_disclosure", 16, "hard_redteam_gate", "Public-health regulation, legal settlement, policy reversal, AI substitution, disease normalization, and low disclosure confidence cap unsafe Green."),
    Round183BaseScoreAxis("capital_discipline_debt_cash_runway", 8, "check_funding_quality", "Smart farm, education, IP, and regulated-consumer names need debt, cash-runway, inventory, and receivables checks."),
    Round183BaseScoreAxis("valuation_room_4b_margin", 6, "small_but_required", "R12 event stories often price narrative before FCF, so valuation room is small and 4B has to be explicit."),
)

ROUND183_STAGE_CAPS: tuple[Round183StageCap, ...] = (
    Round183StageCap(
        "Stage 1",
        "45",
        ("disease_news", "grain_or_fertilizer_price", "medical_quota_policy", "ai_education_news", "kids_ip_viral", "heated_tobacco_news", "smart_farm_or_kiosk_theme"),
        ("harim_manikar_livestock_disease_event_case", "megastudy_medical_quota_policy_event_case"),
        "Theme/news can route research, but it stays capped until repeat revenue, contract, price pass-through, regulatory scope, or OPM/FCF evidence appears.",
    ),
    Round183StageCap(
        "Stage 2",
        "70",
        ("government_policy_confirmed", "actual_order_or_contract", "regulated_distribution", "repeat_enrollment", "export_channel", "price_path_confirmed", "brand_or_ip_revenue_visible"),
        ("pinkfong_ipo_stage2_4b_watch_case", "ktng_lil_heated_tobacco_distribution_case"),
        "Stage 2 can recognize price-path and visibility, but Stage 3 waits for unit economics and FCF conversion.",
    ),
    Round183StageCap(
        "Stage 3",
        "requires_5_of_8",
        ("repeat_revenue_or_repeat_contract", "op_eps_revision_or_quarterly_op_beat", "price_pass_through_faster_than_cost", "demand_structural_not_event", "stage2_60d_mfe_20pct", "inventory_receivables_dealer_inventory_not_worse", "no_regulatory_or_legal_hard_issue", "valuation_not_overheated"),
        ("ktng_possible_only_with_ngp_opm_fcf_and_regulation", "pinkfong_possible_only_with_multi_ip_opm_fcf"),
        "R12 Stage 3 is possible but strict: repeat revenue, unit economics, regulation, and FCF must be source-backed.",
    ),
    Round183StageCap(
        "Stage 4B",
        "requires_3_of_5",
        ("ipo_or_news_1d_20pct", "narrative_rises_before_repeat_revenue", "basket_indiscriminate_rally", "op_eps_revision_lags_price", "community_or_news_keyword_crowding"),
        ("pinkfong_ipo_stage2_4b_watch_case", "samsung_publishing_baby_shark_event_4b_watch_case"),
        "Cool R12 price-path cases when IP, disease, policy, AI education, or fertilizer narratives move before durable earnings.",
    ),
    Round183StageCap(
        "Stage 4C",
        "hard_gate",
        ("legal_settlement_or_collusion", "public_health_regulation_tightening", "policy_reversal_or_cut", "ai_substitutes_core_education_service", "disease_normalization_or_price_drop", "input_cost_overwhelms_price", "one_hit_ip_revenue_slowdown", "dealer_inventory_or_demand_slowdown", "large_dilution_or_cash_burn"),
        ("dongwon_starkist_settlement_legal_4c_watch_case", "qanda_ai_tutor_disruption_overlay_case"),
        "One hard legal, regulatory, policy, AI-disruption, disease-normalization, cost, IP, inventory, or dilution issue can block Green.",
    ),
)

ROUND183_SCORE_TARGETS: tuple[Round183ScoreTarget, ...] = (
    _target(
        "AGRI_MACHINERY_EXPORT_CYCLE_KOREA",
        E2RArchetype.AGRI_MACHINERY_EXPORT_CYCLE_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(16, 18, 16, 8, 10, 8, 6),
        stage1=("agri_machinery_export", "north_america_compact_tractor", "autonomous_tractor_narrative"),
        stage2=("export_sales", "dealer_network", "kioti_or_branson_brand", "parts_service_option"),
        stage3=("export_sales_growth", "opm_fcf_improvement", "dealer_inventory_stable", "parts_service_repeat_revenue", "farmer_financing_cost_stable"),
        stage4b=("agri_robot_theme_priced_before_sales", "tractor_export_theme_crowding"),
        stage4c=("north_america_tractor_demand_slowdown", "dealer_inventory_increase", "grain_price_or_farm_income_weakness", "financing_cost_delay"),
        green=("opm_fcf_improvement", "dealer_inventory_stable", "parts_service_repeat_revenue", "price_path_confirmed"),
        red=("dealer_inventory_increase", "farm_income_weakness", "financing_cost_delay"),
        penalties=("dealer_inventory", "farmer_capex_cycle", "opm_fcf_backfill"),
        note="Daedong/TYM can be Stage 2 candidates, but North America farm capex cycle caps Green.",
    ),
    _target(
        "AGRI_MACHINERY_AUTONOMOUS_ROBOT_OPTION",
        E2RArchetype.AGRI_MACHINERY_AUTONOMOUS_ROBOT_OPTION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(10, 12, 12, 6, 10, 8, 5),
        stage1=("autonomous_tractor", "agricultural_robot", "smart_agri_option"),
        stage2=("commercial_launch", "paid_order", "dealer_support", "service_attach"),
        stage3=("recurring_software_or_service_revenue", "farmer_roi_verified", "op_eps_conversion"),
        stage4b=("robot_option_priced_before_revenue",),
        stage4c=("commercial_sales_missing", "farmer_roi_missing", "right_to_repair_or_service_backlash"),
        green=("paid_order", "recurring_software_or_service_revenue", "farmer_roi_verified", "op_eps_conversion"),
        red=("commercial_sales_missing", "farmer_roi_missing", "service_backlash"),
        penalties=("commercialization", "farmer_roi", "service_attach"),
        note="Autonomous agriculture is an option until commercial sales and farmer ROI are verified.",
    ),
    _target(
        "FERTILIZER_INPUT_PRICE_COST_KOREA",
        E2RArchetype.FERTILIZER_INPUT_PRICE_COST_KOREA,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights(14, 10, 18, 7, 14, 5, 4),
        stage1=("grain_price", "fertilizer_price", "food_security_narrative", "supply_chain_shock"),
        stage2=("fertilizer_price_pass_through", "government_procurement", "product_mix_improvement"),
        stage3=("price_pass_through", "volume_maintained", "energy_raw_material_cost_stable", "opm_fcf_improvement", "farmer_roi_maintained"),
        stage4b=("fertilizer_theme_crowding", "food_security_basket_rally"),
        stage4c=("grain_price_decline", "farmer_purchase_delay", "ammonia_urea_energy_cost_spike", "inventory_loss"),
        green=("price_pass_through", "volume_maintained", "opm_fcf_improvement", "farmer_roi_maintained"),
        red=("input_cost_spike", "farmer_margin_risk", "volume_missing", "inventory_loss"),
        penalties=("input_cost", "farmer_margin", "volume", "inventory"),
        note="Namhae Chemical/KG Chemical need volume, OPM, FCF, and farmer margin, not fertilizer-price headlines only.",
    ),
    _target(
        "LIVESTOCK_DISEASE_PRICE_EVENT_KOREA",
        E2RArchetype.LIVESTOCK_DISEASE_PRICE_EVENT_KOREA,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("bird_flu", "asf", "broiler_price", "egg_price", "culling", "substitution_demand"),
        stage2=("selling_price_increase", "shipment_volume", "feed_price_pass_through"),
        stage3=("normally_green_blocked_unless_recurring_non_disease_fcf",),
        stage4b=("disease_news_1d_20pct", "livestock_basket_rally"),
        stage4c=("disease_normalization", "livestock_price_decline", "feed_cost_rise", "consumer_or_antitrust_backlash"),
        green=(),
        red=("disease_normalization", "price_normalization", "feed_cost_rise", "antitrust_or_price_investigation"),
        penalties=("one_off_disease", "price_normalization", "feed_cost", "consumer_backlash"),
        note="Harim/Maniker/Pamstory-style disease rallies are Stage 1 events and usually Green-blocked.",
        gate_only=True,
    ),
    _target(
        "FEED_GRAIN_COST_PASS_THROUGH",
        E2RArchetype.FEED_GRAIN_COST_PASS_THROUGH,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(13, 10, 18, 6, 10, 5, 4),
        stage1=("grain_price_move", "feed_cost_move", "livestock_price_link"),
        stage2=("feed_price_pass_through", "volume_stable", "customer_contract_or_channel"),
        stage3=("feed_cost_pass_through", "opm_fcf_improvement", "receivables_inventory_stable"),
        stage4b=("feed_theme_basket_rally",),
        stage4c=("grain_cost_spike_not_passed_through", "livestock_demand_drop", "margin_squeeze"),
        green=("feed_cost_pass_through", "volume_stable", "opm_fcf_improvement"),
        red=("cost_not_passed_through", "demand_drop", "margin_squeeze"),
        penalties=("grain_cost", "pass_through", "volume", "receivables"),
        note="Feed names need pass-through and volume proof before Stage 3.",
    ),
    _target(
        "TUNA_FISHERY_GLOBAL_BRAND_LEGAL_RISK",
        E2RArchetype.TUNA_FISHERY_GLOBAL_BRAND_LEGAL_RISK,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(15, 15, 12, 6, 18, 8, 5),
        stage1=("tuna_price", "fishery_fleet", "starkist_brand_cashflow"),
        stage2=("global_tuna_brand", "us_retail_channel", "food_staple_recurring"),
        stage3=("brand_opm", "fuel_fx_stable", "legal_cost_normalized", "fcf_improvement"),
        stage4b=("brand_asset_priced_before_legal_risk",),
        stage4c=("price_fixing_settlement", "legal_reserve", "fuel_cost_spike", "fishery_quota_risk"),
        green=("brand_opm", "legal_cost_normalized", "fcf_improvement"),
        red=("legal_settlement", "price_fixing", "fuel_cost", "quota"),
        penalties=("legal", "fuel", "quota", "fx"),
        note="Dongwon has global brand value, but StarKist legal settlement is a 4C-watch gate.",
    ),
    _target(
        "CONSUMER_REGULATED_PRODUCT_KOREA",
        E2RArchetype.CONSUMER_REGULATED_PRODUCT_KOREA,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(18, 18, 12, 6, 18, 10, 8),
        stage1=("tobacco_cash_cow", "ginseng_health_option", "regulated_consumer_repeat"),
        stage2=("recurring_consumption", "cash_flow_stability", "shareholder_return"),
        stage3=("opm_fcf_maintained", "ngp_or_core_revenue_growth", "tax_regulatory_risk_contained", "public_health_gate_passed"),
        stage4b=("regulated_consumer_defensive_premium",),
        stage4c=("public_health_regulation", "tax_increase", "youth_safety_controversy", "advertising_or_flavor_restriction"),
        green=("opm_fcf_maintained", "recurring_consumption", "shareholder_return", "public_health_gate_passed"),
        red=("public_health_regulation", "tax_increase", "youth_safety", "advertising_restriction"),
        penalties=("public_health", "tax", "youth_safety", "regulatory_scope"),
        note="KT&G can be Green-eligible only with FCF, returns, and public-health/regulatory stability.",
    ),
    _target(
        "HEATED_TOBACCO_GLOBAL_DISTRIBUTION",
        E2RArchetype.HEATED_TOBACCO_GLOBAL_DISTRIBUTION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(16, 18, 10, 6, 18, 8, 6),
        stage1=("heated_tobacco_growth", "lil_iqos_portfolio", "global_distribution_option"),
        stage2=("pmi_ktng_distribution", "overseas_sales", "regulated_channel"),
        stage3=("ngp_overseas_revenue_growth", "opm_fcf_maintained", "regulatory_stability", "youth_safety_limited"),
        stage4b=("smoke_free_product_premium_before_sales",),
        stage4c=("reduced_risk_claim_denied", "public_health_warning", "youth_safety_controversy", "tax_or_display_restriction"),
        green=("ngp_overseas_revenue_growth", "opm_fcf_maintained", "regulatory_stability"),
        red=("public_health_warning", "youth_safety", "tax_or_display_restriction"),
        penalties=("public_health", "ngp_sales", "regulatory_scope", "youth_safety"),
        note="Heated tobacco has repeat-consumption potential, but public-health and marketing-scope gates remain hard.",
    ),
    _target(
        "EDUCATION_POLICY_EVENT_KOREA",
        E2RArchetype.EDUCATION_POLICY_EVENT_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(14, 16, 12, 8, 16, 5, 5),
        stage1=("medical_quota_policy", "exam_prep_demand", "private_education_narrative"),
        stage2=("policy_confirmed", "enrollment_growth", "medical_track_revenue", "op_eps_revision"),
        stage3=("repeat_enrollment", "paid_conversion", "cac_stable", "opm_fcf_improvement", "policy_uncertainty_lower"),
        stage4b=("medical_quota_theme_rally", "education_basket_crowding"),
        stage4c=("policy_freeze_or_reversal", "doctor_strike_policy_uncertainty", "low_birth_rate", "ai_tutor_substitution"),
        green=("repeat_enrollment", "paid_conversion", "cac_stable", "opm_fcf_improvement"),
        red=("policy_reversal", "low_birth_rate", "ai_substitution", "opm_missing"),
        penalties=("policy_reversal", "student_count", "ai_tutor", "cac"),
        note="Medical-quota education trades are Stage 1/2 until repeat enrollment and OPM are verified.",
    ),
    _target(
        "EDTECH_AI_DISRUPTION_KOREA",
        E2RArchetype.EDTECH_AI_DISRUPTION_KOREA,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("ai_tutor", "ai_problem_solving", "personalized_learning"),
        stage2=("paid_conversion", "b2b_or_b2g_contract", "repeat_subscription"),
        stage3=("not_green_without_paid_repeat_opm",),
        stage4b=("ai_education_theme_priced_before_bookings",),
        stage4c=("ai_substitutes_core_service", "tuition_price_pressure", "cac_rise", "content_commoditization"),
        green=(),
        red=("ai_substitution", "price_pressure", "cac_rise", "content_commoditization"),
        penalties=("cannibalization", "cac", "paid_conversion", "bookings"),
        note="AI education can help, but it can also replace listed education services; treat it as RedTeam-first.",
        gate_only=True,
    ),
    _target(
        "KIDS_IP_PLATFORM_KOREA",
        E2RArchetype.KIDS_IP_PLATFORM_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(18, 18, 14, 12, 12, 6, 8),
        stage1=("baby_shark_viral", "kids_ip_global_narrative", "affiliate_value_expectation"),
        stage2=("ipo_price_path", "ip_revenue", "operating_profit", "licensing_merchandise_apps_live_tour"),
        stage3=("multi_ip_revenue", "bebefinn_or_new_ip_scale", "opm_fcf_maintained", "post_ipo_guidance_met"),
        stage4b=("ipo_pop", "one_hit_valuation", "affiliate_price_event"),
        stage4c=("one_hit_ip_revenue_slowdown", "post_ipo_guidance_miss", "ip_dependency_high"),
        green=("multi_ip_revenue", "opm_fcf_maintained", "post_ipo_guidance_met"),
        red=("one_hit_dependency", "ipo_premium", "guidance_miss"),
        penalties=("one_hit", "ipo_premium", "direct_earnings_link", "guidance"),
        note="Pinkfong/Samsung Publishing are strong Stage 2 price-path cases but need multi-IP revenue for Stage 3.",
    ),
    _target(
        "SMART_FARM_UNIT_ECONOMICS_KOREA",
        E2RArchetype.SMART_FARM_UNIT_ECONOMICS_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(10, 14, 18, 6, 12, 10, 4),
        stage1=("smart_farm_policy", "greenhouse_order_news", "agri_tech_narrative"),
        stage2=("actual_order", "contract_amount", "customer_or_government_budget", "operating_yield_visible"),
        stage3=("unit_economics_verified", "opm_fcf_positive", "repeat_order", "energy_cost_controlled"),
        stage4b=("smart_farm_theme_priced_before_unit_economics",),
        stage4c=("unit_economics_failure", "energy_cost_spike", "capex_burden", "dilution_or_cash_burn"),
        green=("unit_economics_verified", "opm_fcf_positive", "repeat_order"),
        red=("unit_economics_failure", "energy_cost", "capex_burden", "cash_burn"),
        penalties=("unit_economics", "energy_cost", "capex", "cash_runway"),
        note="Smart farm stays Watch until real orders and unit economics are visible.",
    ),
    _target(
        "SERVICE_KIOSK_LOCAL_REGULATION_KOREA",
        E2RArchetype.SERVICE_KIOSK_LOCAL_REGULATION_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(12, 14, 14, 6, 14, 6, 4),
        stage1=("kiosk_theme", "self_checkout_unmanned_store", "labor_cost_narrative"),
        stage2=("installed_base", "maintenance_fee", "transaction_fee", "recurring_service_contract"),
        stage3=("maintenance_or_fee_revenue", "opm_fcf_improvement", "regulatory_accessibility_compliance"),
        stage4b=("unmanned_store_theme_rally",),
        stage4c=("local_regulation", "accessibility_rule_cost", "security_or_payment_issue", "merchant_demand_slowdown"),
        green=("maintenance_or_fee_revenue", "opm_fcf_improvement", "regulatory_accessibility_compliance"),
        red=("local_regulation", "accessibility_cost", "security_issue", "demand_slowdown"),
        penalties=("maintenance_revenue", "fee_revenue", "local_regulation", "security"),
        note="Kiosk themes need maintenance/fee revenue, not installation counts only.",
    ),
    _target(
        "DISCLOSURE_CONFIDENCE_CAP",
        E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        Round10ThemePosture.REDTEAM_FIRST,
        CAP_WEIGHT,
        stage1=("theme_headline", "disease_or_policy_headline", "ip_or_ai_headline"),
        stage2=("detail_fetch_required", "contract_or_unit_economics_detail_required", "regulatory_scope_required"),
        stage3=("multi_source_confirmation", "repeat_revenue_or_opm_detail", "parser_confidence_sufficient"),
        stage4b=("headline_priced_before_detail",),
        stage4c=("contract_detail_missing", "repeat_revenue_missing", "unit_economics_missing", "regulatory_scope_missing", "opm_fcf_missing"),
        green=("repeat_revenue_detail", "unit_economics_detail", "regulatory_scope_detail", "opm_fcf_detail"),
        red=("detail_missing", "parser_confidence_low", "opm_fcf_missing"),
        penalties=("disclosure", "detail", "unit_economics", "parser_confidence"),
        note="R12 headlines stay capped when repeat revenue, unit economics, regulatory scope, or OPM/FCF detail is missing.",
    ),
)

ROUND183_SCORE_STAGE_PRICE_ALIGNMENT: tuple[Round183ScoreStagePriceAlignment, ...] = (
    Round183ScoreStagePriceAlignment("pinkfong_ipo_stage2_4b_watch_case", "Stage 2 strong plus 4B-watch", "IPO first-day max +62% and close +9% is strong price-path but also IPO premium", "stage2_price_path_not_green", "capture IPO price-path while requiring multi-IP OPM/FCF before Stage 3"),
    Round183ScoreStagePriceAlignment("samsung_publishing_baby_shark_event_4b_watch_case", "Stage 1 event plus 4B-watch", "Baby Shark chart event drove affiliate-price premium without direct recurring earnings proof", "affiliate_ip_event_not_green", "cap direct Stage 3 credit until revenue linkage is verified"),
    Round183ScoreStagePriceAlignment("ktng_lil_heated_tobacco_distribution_case", "Stage 2/3 candidate", "Repeat consumption and global distribution can support higher stage, but public-health gates remain", "regulated_repeat_candidate", "require NGP overseas revenue, OPM/FCF, shareholder return, and regulatory stability"),
    Round183ScoreStagePriceAlignment("dongwon_starkist_settlement_legal_4c_watch_case", "Stage 2 plus 4C-watch", "Global brand cash flow exists, but StarKist settlement is a legal hard-risk field", "brand_cashflow_with_legal_4c", "apply legal-settlement RedTeam before any Green consideration"),
    Round183ScoreStagePriceAlignment("megastudy_medical_quota_policy_event_case", "Stage 1/2 policy event", "Medical-quota news can move education stocks, but policy reversals and AI substitution cap Green", "policy_event_not_repeat_revenue", "require repeat enrollment, paid conversion, CAC, and OPM before Stage 3"),
)

ROUND183_CASE_CANDIDATES: tuple[Round183CaseCandidate, ...] = (
    Round183CaseCandidate(
        "pinkfong_ipo_stage2_4b_watch_case",
        "KIDS_IP_PLATFORM_KOREA",
        "PINKFONG",
        "The Pinkfong Company kids IP platform IPO",
        "KR",
        "4b_watch",
        None,
        None,
        None,
        None,
        None,
        ("baby_shark_16bn_youtube_views", "ipo_max_plus_62pct", "ipo_close_plus_9pct", "revenue_97_4bn_krw", "operating_profit_18_8bn_krw", "bebefinn_diversification_option"),
        ("one_hit_dependency", "ipo_premium", "post_ipo_guidance_needed", "baby_shark_concentration"),
        "stage2_strong_price_path_plus_4b_watch",
        "needs_listing_date_price_path_multi_ip_revenue_backfill",
        ("round_183.md Financial Times Pinkfong IPO",),
        "Pinkfong is a clear R12 Stage 2 price-path case, but one-hit and IPO-premium risks keep it 4B-watch until multi-IP revenue and OPM/FCF are proven.",
        (E2RArchetype.EVENT_PRICE_RALLY_NOT_STAGE3,),
    ),
    Round183CaseCandidate(
        "samsung_publishing_baby_shark_event_4b_watch_case",
        "KIDS_IP_PLATFORM_KOREA",
        "068290",
        "Samsung Publishing Baby Shark affiliate event premium",
        "KR",
        "event_premium",
        None,
        None,
        None,
        None,
        None,
        ("baby_shark_chart_event", "samsung_publishing_plus_76pct", "affiliate_value_expectation"),
        ("direct_earnings_link_missing", "one_hit_dependency", "ip_theme_premium"),
        "affiliate_ip_event_price_path_not_stage3",
        "needs_event_date_price_and_earnings_link_backfill",
        ("round_183.md Pinkfong/Samsung Publishing Baby Shark event",),
        "Samsung Publishing shows affiliate IP event price-path, but Stage 3 needs direct earnings linkage.",
    ),
    Round183CaseCandidate(
        "ktng_lil_heated_tobacco_distribution_case",
        "HEATED_TOBACCO_GLOBAL_DISTRIBUTION",
        "033780",
        "KT&G lil heated tobacco global distribution",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("pmi_ktng_lil_distribution", "iqos_portfolio", "repeat_consumption", "global_smoke_free_channel_option", "cash_flow_stability"),
        ("public_health_risk", "tax_regulatory_risk", "youth_safety_controversy", "ngp_sales_backfill_needed"),
        "regulated_repeat_consumption_stage2_3_candidate",
        "needs_ngp_overseas_sales_opm_fcf_regulatory_price_backfill",
        ("round_183.md KT&G lil PMI distribution",),
        "KT&G can be a rare R12 Stage 2/3 candidate, but public-health and regulatory scope must be checked.",
        (E2RArchetype.CONSUMER_REGULATED_PRODUCT_KOREA,),
    ),
    Round183CaseCandidate(
        "ktng_public_health_regulation_4c_watch_case",
        "CONSUMER_REGULATED_PRODUCT_KOREA",
        "033780",
        "KT&G regulated consumer public-health gate",
        "KR",
        "4c_thesis_break",
        _d("2026-05-15"),
        None,
        None,
        None,
        _d("2026-05-15"),
        ("repeat_consumption", "regulated_consumer_product", "who_nicotine_youth_warning"),
        ("public_health_warning", "youth_addiction_risk", "flavor_packaging_marketing_risk", "tax_or_display_restriction"),
        "public_health_gate_can_override_repeat_consumption",
        "needs_ktng_direct_exposure_regulatory_scope_price_backfill",
        ("round_183.md Reuters WHO nicotine pouch youth addiction warning",),
        "Public-health regulation is a hard gate across regulated consumer products even when repeat consumption is strong.",
        (E2RArchetype.NICOTINE_POUCH_YOUTH_SAFETY_OVERLAY,),
    ),
    Round183CaseCandidate(
        "daedong_tym_agri_machinery_export_stage2_candidate_case",
        "AGRI_MACHINERY_EXPORT_CYCLE_KOREA",
        "000490/002900",
        "Daedong and TYM Korea agri machinery export cycle",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("kioti_brand", "branson_brand", "north_america_compact_tractor", "export_revenue", "parts_service_option"),
        ("dealer_inventory_unknown", "farmer_capex_cycle", "farm_income_financing_cost", "opm_fcf_backfill_needed"),
        "agri_machinery_export_stage2_candidate",
        "needs_krx_price_op_revision_dealer_inventory_backfill",
        ("round_183.md Daedong/TYM agriculture machinery section",),
        "Daedong/TYM are Stage 2 candidates when exports and service revenue verify, but farm capex cycle can break the thesis.",
        (E2RArchetype.AGRI_MACHINERY_AUTONOMOUS_ROBOT_OPTION,),
    ),
    Round183CaseCandidate(
        "daedong_autonomous_agri_robot_option_watch_case",
        "AGRI_MACHINERY_AUTONOMOUS_ROBOT_OPTION",
        "000490",
        "Daedong autonomous tractor and agri robot option",
        "KR",
        "event_premium",
        None,
        None,
        None,
        None,
        None,
        ("autonomous_tractor_option", "agricultural_robot_narrative", "utv_skid_steer_expansion"),
        ("commercial_sales_missing", "farmer_roi_missing", "service_attach_missing"),
        "autonomous_option_stage1_2_until_revenue",
        "needs_commercial_sales_farmer_roi_price_backfill",
        ("round_183.md Daedong autonomous machinery option",),
        "Autonomous machinery is optionality until commercial sales and farmer ROI are proven.",
    ),
    Round183CaseCandidate(
        "megastudy_medical_quota_policy_event_case",
        "EDUCATION_POLICY_EVENT_KOREA",
        "215200/068930/096240",
        "Megastudy Digital Daesung Creverse medical quota policy event",
        "KR",
        "event_premium",
        _d("2025-03-07"),
        None,
        None,
        _d("2025-03-07"),
        None,
        ("medical_quota_policy", "exam_prep_demand", "policy_freeze_or_adjustment", "private_education_narrative"),
        ("policy_reversal_risk", "low_birth_rate", "ai_tutor_substitution", "bookings_opm_missing"),
        "education_policy_stage1_2_not_green",
        "needs_enrollment_paid_conversion_opm_price_backfill",
        ("round_183.md Reuters medical student quota freeze", "round_183.md AP medical school admissions boost"),
        "Medical-quota policy can create Stage 1/2 education events, but repeated enrollment and OPM are required for Stage 3.",
        (E2RArchetype.EDTECH_AI_DISRUPTION_KOREA,),
    ),
    Round183CaseCandidate(
        "qanda_ai_tutor_disruption_overlay_case",
        "EDTECH_AI_DISRUPTION_KOREA",
        "QANDA_PRIVATE/KR_EDUCATION_BASKET",
        "QANDA AI tutor disruption overlay for Korea education stocks",
        "KR",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        None,
        ("ai_math_solver", "ai_tutor", "90m_registered_users", "8m_mau", "50_country_usage"),
        ("ai_substitutes_core_service", "tuition_price_pressure", "cac_rise", "content_commoditization"),
        "ai_tutor_can_be_4c_for_legacy_education",
        "needs_listed_company_exposure_and_price_backfill",
        ("round_183.md QANDA AI tutor section",),
        "AI education can be either monetization or disruption; for legacy education it is a 4C-watch until paid conversion helps rather than cannibalizes.",
    ),
    Round183CaseCandidate(
        "dongwon_starkist_settlement_legal_4c_watch_case",
        "TUNA_FISHERY_GLOBAL_BRAND_LEGAL_RISK",
        "006040",
        "Dongwon Industries StarKist tuna brand and legal settlement",
        "KR",
        "4c_thesis_break",
        _d("2024-08-14"),
        None,
        None,
        None,
        _d("2024-08-14"),
        ("starkist_brand", "us_retail_channel", "food_staple_recurring", "settlement_200m_usd", "starkist_130m_usd_burden"),
        ("price_fixing_settlement", "legal_reserve", "fuel_cost_risk", "fishery_quota_risk"),
        "global_brand_stage2_plus_legal_4c_watch",
        "needs_brand_opm_legal_reserve_fuel_fx_price_backfill",
        ("round_183.md Reuters StarKist tuna price-fixing settlement",),
        "Dongwon has global brand assets, but StarKist settlement is a legal RedTeam gate.",
    ),
    Round183CaseCandidate(
        "harim_manikar_livestock_disease_event_case",
        "LIVESTOCK_DISEASE_PRICE_EVENT_KOREA",
        "136480/027740/027710",
        "Harim Maniker Pamstory livestock disease and broiler price event",
        "KR",
        "event_premium",
        None,
        None,
        None,
        None,
        None,
        ("bird_flu", "broiler_price", "egg_price", "culling", "substitution_demand"),
        ("disease_normalization", "feed_cost_rise", "price_normalization", "consumer_or_antitrust_backlash"),
        "disease_event_price_path_not_structural_green",
        "needs_event_date_livestock_price_feed_cost_backfill",
        ("round_183.md H5N8 livestock disease event section",),
        "Livestock disease can drive event rallies, but it is not structural Green without recurring non-disease FCF.",
    ),
    Round183CaseCandidate(
        "kg_namhae_fertilizer_farmer_margin_cycle_case",
        "FERTILIZER_INPUT_PRICE_COST_KOREA",
        "001390/025860/001550/097870",
        "KG Chemical Namhae Chemical fertilizer input-price cycle",
        "KR",
        "cyclical_success",
        None,
        None,
        None,
        None,
        None,
        ("fertilizer_price", "food_security_narrative", "government_procurement_option", "price_pass_through_possible"),
        ("input_cost_risk", "farmer_margin_risk", "volume_missing", "inventory_loss"),
        "fertilizer_cycle_stage1_2_until_volume_opm_fcf",
        "needs_fertilizer_price_volume_input_cost_opm_price_backfill",
        ("round_183.md Namhae Chemical KG Chemical fertilizer section",),
        "Fertilizer names can be Stage 1/2 cycle cases, but volume, farmer margin, and OPM/FCF decide promotion.",
    ),
    Round183CaseCandidate(
        "pamstory_sajo_feed_grain_pass_through_case",
        "FEED_GRAIN_COST_PASS_THROUGH",
        "027710/008040",
        "Pamstory Sajo DongA One feed grain cost pass-through",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("feed_cost_signal", "grain_price_signal", "livestock_price_link"),
        ("grain_cost_spike_not_passed_through", "margin_squeeze", "receivables_or_inventory_missing"),
        "feed_pass_through_required_before_stage3",
        "needs_feed_cost_price_pass_through_volume_price_backfill",
        ("round_183.md feed grain cost pass-through section",),
        "Feed names need pass-through and volume proof before Stage 3.",
    ),
    Round183CaseCandidate(
        "greenplus_woodumji_smart_farm_unit_economics_watch_case",
        "SMART_FARM_UNIT_ECONOMICS_KOREA",
        "186230/403490",
        "Green Plus Woodumji Farm smart farm unit economics watch",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("smart_farm_order_narrative", "greenhouse_policy", "agri_tech_narrative"),
        ("unit_economics_missing", "energy_cost", "capex_burden", "opm_missing"),
        "smart_farm_watch_until_orders_unit_economics",
        "needs_contract_amount_unit_economics_opm_price_backfill",
        ("round_183.md smart farm watch section",),
        "Smart farm remains Watch until orders, unit economics, and OPM/FCF are visible.",
    ),
    Round183CaseCandidate(
        "korea_kiosk_local_regulation_watch_case",
        "SERVICE_KIOSK_LOCAL_REGULATION_KOREA",
        "063570/089150/094940",
        "Korea kiosk and self-checkout local regulation watch",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("kiosk_theme", "unmanned_store", "labor_cost_narrative"),
        ("maintenance_fee_missing", "local_regulation", "accessibility_cost", "security_or_payment_issue"),
        "installation_count_not_stage3_without_fee_revenue",
        "needs_installed_base_fee_revenue_regulation_price_backfill",
        ("round_183.md kiosk self-checkout section",),
        "Kiosk names need maintenance or transaction-fee revenue before Stage 3.",
    ),
    Round183CaseCandidate(
        "r12_disclosure_confidence_cap_case",
        "DISCLOSURE_CONFIDENCE_CAP",
        "KR_R12_DISCLOSURE_BASKET",
        "R12 disclosure confidence cap basket",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("theme_headline", "disease_policy_ip_ai_headline", "unit_economics_claim"),
        ("contract_detail_missing", "repeat_revenue_missing", "unit_economics_missing", "regulatory_scope_missing", "opm_fcf_missing", "parser_confidence_low"),
        "r12_detail_missing_cap",
        "needs_contract_repeat_revenue_unit_economics_regulatory_opm_backfill",
        ("round_183.md OpenDART detail caution",),
        "R12 headline evidence is capped until details, repeat revenue, unit economics, regulatory scope, and OPM/FCF are parsed.",
    ),
)

ROUND183_PRICE_FIELDS: tuple[str, ...] = (
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
    "relative_strength_vs_kosdaq",
    "relative_strength_vs_agri_basket",
    "relative_strength_vs_education_basket",
    "relative_strength_vs_consumer_regulated_basket",
    "op_revision_before_stage3",
    "op_revision_after_stage3",
    "eps_revision_before_stage3",
    "eps_revision_after_stage3",
    "recurring_revenue_ratio",
    "subscription_or_repeat_revenue",
    "order_backlog",
    "contract_amount",
    "contract_counterparty",
    "contract_period",
    "export_sales_ratio",
    "dealer_inventory_signal",
    "farm_income_signal",
    "grain_price_signal",
    "feed_cost_signal",
    "livestock_price_signal",
    "price_pass_through_signal",
    "regulatory_approval_status",
    "public_health_risk_flag",
    "youth_safety_flag",
    "legal_settlement_flag",
    "antitrust_or_collusion_flag",
    "policy_event_type",
    "policy_reversal_risk",
    "medical_quota_policy_status",
    "student_count_trend",
    "cac",
    "churn",
    "paid_conversion",
    "ip_revenue",
    "licensing_revenue",
    "merchandise_revenue",
    "one_hit_dependency",
    "post_ipo_guidance",
    "inventory_days",
    "receivables_days",
    "cash_runway_months",
    "dilution_event_flag",
    "disclosure_confidence",
    "valuation_at_stage3",
    "valuation_at_stage4b",
)


def round183_target_for(target_id: str) -> Round183ScoreTarget | None:
    for target in ROUND183_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round183_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND183_CASE_CANDIDATES:
        target = round183_target_for(candidate.target_id)
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
                f"Round183 R12 Loop-11 case for {candidate.target_id}; "
                "Korea agriculture, life service, education, kids IP, regulated consumer, and misc themes are separated from repeat revenue, unit economics, price pass-through, regulatory scope, OPM/FCF, and price-path evidence."
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
                if candidate.case_type in {"failed_rerating", "event_premium", "overheat", "4b_watch", "4c_thesis_break", "one_off", "cyclical_success"}
                else None
            ),
            score_price_alignment=_score_price_alignment(candidate),
            rerating_result=_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
            score_weight_hint=_score_weight_hint(target),
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "r12_theme_news_is_not_stage3_evidence_alone",
                "repeat_revenue_opm_fcf_unit_economics_required",
                "stage3_early_catch_requires_5_of_8_loop11_conditions",
                "do_not_invent_stage_prices_mfe_mae_or_unit_economics",
                "opendart_detail_required_for_watch_disclosures",
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


def round183_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND183_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "eps_fcf_opm_conversion": str(weights["eps_fcf_opm_conversion"]),
                "recurring_order_regulatory_visibility": str(weights["recurring_order_regulatory_visibility"]),
                "unit_economics_pass_through_demand_durability": str(weights["unit_economics_pass_through_demand_durability"]),
                "price_path_early_validation": str(weights["price_path_early_validation"]),
                "regulation_litigation_public_health_disclosure": str(weights["regulation_litigation_public_health_disclosure"]),
                "capital_discipline_debt_cash_runway": str(weights["capital_discipline_debt_cash_runway"]),
                "valuation_room_4b_margin": str(weights["valuation_room_4b_margin"]),
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


def round183_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND183_CASE_CANDIDATES:
        target = round183_target_for(candidate.target_id)
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


def round183_stage_date_rows() -> tuple[dict[str, str], ...]:
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
        for target in ROUND183_SCORE_TARGETS
    )


def round183_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round183_backfill": "true"} for field in ROUND183_PRICE_FIELDS)


def round183_base_score_axis_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "axis_id": item.axis_id,
            "points": str(item.points),
            "loop11_direction": item.loop11_direction,
            "reason": item.reason,
            "production_scoring_changed": "false",
        }
        for item in ROUND183_BASE_SCORE_AXES
    )


def round183_stage_cap_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "stage_band": item.stage_band,
            "max_score": item.max_score,
            "required_evidence": "|".join(item.required_evidence),
            "example_cases": "|".join(item.example_cases),
            "green_policy": item.green_policy,
            "production_scoring_changed": "false",
        }
        for item in ROUND183_STAGE_CAPS
    )


def round183_score_stage_price_alignment_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "case_id": item.case_id,
            "detected_stage": item.detected_stage,
            "price_path_status": item.price_path_status,
            "verdict": item.verdict,
            "normalization_adjustment": item.normalization_adjustment,
            "production_scoring_changed": "false",
        }
        for item in ROUND183_SCORE_STAGE_PRICE_ALIGNMENT
    )


def round183_summary() -> dict[str, int | bool]:
    records = round183_case_records()
    return {
        "target_count": len(ROUND183_SCORE_TARGETS),
        "source_canonical_target_count": ROUND183_SOURCE_CANONICAL_TARGET_COUNT,
        "case_candidate_count": len(records),
        "base_score_axis_count": len(ROUND183_BASE_SCORE_AXES),
        "stage_cap_count": len(ROUND183_STAGE_CAPS),
        "score_stage_price_alignment_count": len(ROUND183_SCORE_STAGE_PRICE_ALIGNMENT),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "cyclical_success_count": sum(1 for record in records if record.case_type == "cyclical_success"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND183_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND183_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND183_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "gate_only_target_count": sum(1 for target in ROUND183_SCORE_TARGETS if target.gate_only),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round183_r12_loop11_reports(
    *,
    output_directory: str | Path = ROUND183_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND183_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND183_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round183_r12_loop11_agri_life_misc_summary.md",
        "case_matrix": output / "round183_r12_loop11_case_matrix.csv",
        "stage_date_plan": output / "round183_r12_loop11_stage_date_plan.csv",
        "green_guardrails": output / "round183_r12_loop11_green_guardrails.md",
        "risk_overlays": output / "round183_r12_loop11_risk_overlays.md",
        "price_validation_plan": output / "round183_r12_loop11_price_validation_plan.md",
        "price_fields": output / "round183_r12_loop11_price_fields.csv",
        "base_score_axes": output / "round183_r12_loop11_base_score_axes.csv",
        "stage_caps": output / "round183_r12_loop11_stage_caps.csv",
        "score_stage_price_alignment": output / "round183_r12_loop11_score_stage_price_alignment.csv",
        "score_stage_price_alignment_md": output / "round183_r12_loop11_score_stage_price_alignment.md",
    }
    _write_case_jsonl(round183_case_records(), cases)
    _write_rows(round183_score_profile_rows(), score_profiles)
    _write_rows(round183_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round183_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round183_price_field_rows(), paths["price_fields"])
    _write_rows(round183_base_score_axis_rows(), paths["base_score_axes"])
    _write_rows(round183_stage_cap_rows(), paths["stage_caps"])
    _write_rows(round183_score_stage_price_alignment_rows(), paths["score_stage_price_alignment"])
    paths["summary"].write_text(render_round183_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round183_green_guardrail_markdown(), encoding="utf-8")
    paths["risk_overlays"].write_text(render_round183_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round183_price_validation_plan_markdown(), encoding="utf-8")
    paths["score_stage_price_alignment_md"].write_text(render_round183_score_stage_price_alignment_markdown(), encoding="utf-8")
    return paths


def render_round183_summary_markdown() -> str:
    summary = round183_summary()
    lines = [
        "# Round-183 R12 Loop-11 Korea Agriculture / Life Services / Misc Summary",
        "",
        f"- source_round: `{ROUND183_SOURCE_ROUND_PATH}`",
        "- large_sector: `EDUCATION_LIFE_AGRI_MISC`",
        "- loop: `R12 Loop 11 / v11.0`",
        f"- target_count: {summary['target_count']}",
        f"- source_canonical_target_count: {summary['source_canonical_target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- base_score_axis_count: {summary['base_score_axis_count']}",
        f"- stage_cap_count: {summary['stage_cap_count']}",
        f"- score_stage_price_alignment_count: {summary['score_stage_price_alignment_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- failed_rerating_count: {summary['failed_rerating_count']}",
        f"- cyclical_success_count: {summary['cyclical_success_count']}",
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
        "- R12 Loop 11 separates agriculture, disease, education, AI tutor, tobacco, kids IP, smart farm, and kiosk narratives from repeat revenue and OPM/FCF proof.",
        "- Example: Pinkfong IPO price-path is Stage 2 strong, but one-hit and IPO-premium risks keep it 4B-watch until multi-IP OPM/FCF are proven.",
        "- Example: KT&G can be Stage 2/3 candidate, but public-health, youth-safety, tax, and regulatory gates remain hard.",
        "- Example: medical-quota education rallies are Stage 1/2 policy events unless repeat enrollment, paid conversion, CAC, and OPM improve.",
    ]
    return "\n".join(lines) + "\n"


def render_round183_green_guardrail_markdown() -> str:
    lines = [
        "# Round-183 R12 Loop-11 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Loop-11 penalties |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND183_SCORE_TARGETS:
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
            "- Do not apply R12 Loop-11 v11.0 weights to production scoring yet.",
            "- Do not treat agriculture, disease-beneficiary, medical-quota, AI education, smart-farm, heated-tobacco, or kids-IP headlines as Green evidence by themselves.",
            "- Do not invent stage prices, MFE/MAE, OPM, FCF, unit economics, repeat revenue, contracts, regulatory scope, or price pass-through.",
            "- Green requires repeat revenue or contract, OPM/FCF conversion, unit economics, price pass-through, and legal/regulatory stability.",
            "- OpenDART list-only evidence is insufficient; detail fetch should stay limited to watch disclosures.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round183_risk_overlay_markdown() -> str:
    lines = [
        "# Round-183 R12 Loop-11 Risk Overlays",
        "",
        "| target | stage4c conditions | red flags |",
        "| --- | --- | --- |",
    ]
    for target in ROUND183_SCORE_TARGETS:
        if target.red_flags or target.gate_only:
            lines.append(f"| `{target.target_id}` | {', '.join(target.stage4c_conditions)} | {', '.join(target.red_flags)} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- R12 is sensitive to legal settlement, public-health regulation, policy reversal, AI tutor substitution, disease normalization, input-cost squeeze, one-hit IP, and dealer inventory.",
            "- Example: Pinkfong can have strong price-path but still needs one-hit and IPO-premium 4B checks.",
            "- Example: Dongwon/StarKist brand cash flow needs legal-settlement RedTeam before higher-stage confidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round183_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-183 R12 Loop-11 Price Validation Plan",
        "",
        "R12 needs both event-date price-path validation and operating unit-economics backfill because event themes and repeat-revenue candidates are mixed.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND183_PRICE_FIELDS)
    lines.extend(
        [
            "",
            "## Case Backfill Priorities",
            "",
            "- `pinkfong_ipo_stage2_4b_watch_case`: IPO listing date, max/close return, multi-IP revenue, OPM, FCF, and post-IPO guidance.",
            "- `ktng_lil_heated_tobacco_distribution_case`: overseas NGP revenue, OPM/FCF, shareholder return, public-health scope, and price path.",
            "- `daedong_tym_agri_machinery_export_stage2_candidate_case`: KRX OHLCV, export sales, dealer inventory, farm-income, financing cost, and OP revision.",
            "- `megastudy_medical_quota_policy_event_case`: policy dates, enrollment, paid conversion, CAC, OPM, and AI tutor substitution risk.",
            "- `dongwon_starkist_settlement_legal_4c_watch_case`: settlement reserves, brand OPM, fuel/FX, and sector price MAE.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round183_score_stage_price_alignment_markdown() -> str:
    lines = [
        "# Round-183 R12 Loop-11 Score / Stage / Price Alignment",
        "",
        "| case | detected stage | price path status | verdict | adjustment |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in ROUND183_SCORE_STAGE_PRICE_ALIGNMENT:
        lines.append(f"| `{row.case_id}` | {row.detected_stage} | {row.price_path_status} | {row.verdict} | {row.normalization_adjustment} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Pinkfong/Samsung Publishing explain how a real IP price-path can be Stage 2 or 4B-watch without becoming Green.",
            "- KT&G explains how repeat consumption can be Green-eligible only with public-health and regulatory gates passed.",
            "- Megastudy-style education policy rallies explain why policy events need repeat enrollment and OPM checks.",
        ]
    )
    return "\n".join(lines) + "\n"


def _score_weight_hint(target: Round183ScoreTarget) -> Mapping[str, float]:
    values: dict[str, float] = {}
    for key, value in target.score_weight.as_dict().items():
        if isinstance(value, int):
            values[key] = float(value)
    return values


def _score_price_alignment(candidate: Round183CaseCandidate) -> str:
    if candidate.case_type == "success_candidate":
        return "unknown"
    if candidate.case_type in {"event_premium", "4b_watch", "cyclical_success"}:
        return "price_moved_without_evidence"
    if candidate.case_type == "4c_thesis_break":
        return "false_positive_score"
    if candidate.case_type == "failed_rerating":
        return "evidence_good_but_price_failed"
    return "unknown"


def _rerating_result(candidate: Round183CaseCandidate) -> str:
    if candidate.case_type == "success_candidate":
        return "unknown"
    if candidate.case_type == "event_premium":
        return "event_premium"
    if candidate.case_type == "cyclical_success":
        return "cyclical_rerating"
    if candidate.case_type == "4b_watch":
        return "theme_overheat"
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    if candidate.case_type == "failed_rerating":
        return "no_rerating"
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
    "ROUND183_BASE_SCORE_AXES",
    "ROUND183_CASE_CANDIDATES",
    "ROUND183_DEFAULT_CASES_PATH",
    "ROUND183_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND183_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND183_PRICE_FIELDS",
    "ROUND183_SCORE_STAGE_PRICE_ALIGNMENT",
    "ROUND183_SCORE_TARGETS",
    "ROUND183_SOURCE_CANONICAL_TARGET_COUNT",
    "ROUND183_SOURCE_CANONICAL_TARGET_IDS",
    "ROUND183_STAGE_CAPS",
    "render_round183_green_guardrail_markdown",
    "render_round183_price_validation_plan_markdown",
    "render_round183_risk_overlay_markdown",
    "render_round183_score_stage_price_alignment_markdown",
    "render_round183_summary_markdown",
    "round183_base_score_axis_rows",
    "round183_case_candidate_rows",
    "round183_case_records",
    "round183_price_field_rows",
    "round183_score_profile_rows",
    "round183_score_stage_price_alignment_rows",
    "round183_stage_cap_rows",
    "round183_stage_date_rows",
    "round183_summary",
    "round183_target_for",
    "write_round183_r12_loop11_reports",
]
