"""Round-182 R11 Loop-11 Korea policy, geopolitical, disaster, and event pack.

Round 182 keeps R11 Korea-focused. It uses East Sea gas exploration, short
selling policy, martial-law political shock, and Hormuz/Middle East energy
shock to calibrate event handling. Event price rallies are useful Stage 1
signals, but they do not become Stage 3 without contracts, budgets, government
orders, commercial exploration results, revenue guidance, or EPS/FCF conversion.

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


ROUND182_SOURCE_ROUND_PATH = "docs/round/round_182.md"
ROUND182_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round182_r11_loop11_policy_geopolitical_event"
ROUND182_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r11_loop11_round182.jsonl"
ROUND182_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round182_r11_loop11_v11.csv"
ROUND182_SOURCE_CANONICAL_TARGET_IDS: tuple[str, ...] = (
    "DOMESTIC_RESOURCE_DISCOVERY_EVENT",
    "RESOURCE_EXPLORATION_DRILL_BIT_GATE",
    "ENERGY_SECURITY_POLICY_EVENT",
    "MARKET_STRUCTURE_SHORT_SELLING_POLICY",
    "SHORT_SELLING_RESUMPTION_RISK",
    "POLITICAL_SYSTEM_SHOCK_KOREA",
    "GEOPOLITICAL_ENERGY_IMPORT_SHOCK",
    "EVENT_PRICE_RALLY_NOT_STAGE3",
    "POLICY_DIRECTIONALITY_ERROR",
    "DISCLOSURE_CONFIDENCE_CAP",
)
ROUND182_SOURCE_CANONICAL_TARGET_COUNT = len(ROUND182_SOURCE_CANONICAL_TARGET_IDS)


@dataclass(frozen=True)
class Round182ScoreWeightDraft:
    contract_budget_order_exploration_visibility: int | str
    eps_fcf_revenue_guidance_conversion: int | str
    price_path_event_detection: int | str
    recurrence_durability: int | str
    redteam_disclosure_confidence: int | str
    policy_directionality: int | str
    valuation_room_4b_runway: int | str

    def as_dict(self) -> dict[str, int | str]:
        return {
            "contract_budget_order_exploration_visibility": self.contract_budget_order_exploration_visibility,
            "eps_fcf_revenue_guidance_conversion": self.eps_fcf_revenue_guidance_conversion,
            "price_path_event_detection": self.price_path_event_detection,
            "recurrence_durability": self.recurrence_durability,
            "redteam_disclosure_confidence": self.redteam_disclosure_confidence,
            "policy_directionality": self.policy_directionality,
            "valuation_room_4b_runway": self.valuation_room_4b_runway,
        }


@dataclass(frozen=True)
class Round182ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round182ScoreWeightDraft
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
        return Round10LargeSector.POLICY_GEOPOLITICAL_EVENT

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round182CaseCandidate:
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
class Round182BaseScoreWeight:
    component: str
    points: int
    loop11_direction: str
    reason: str


@dataclass(frozen=True)
class Round182StageCap:
    stage_band: str
    max_score: str
    required_evidence: tuple[str, ...]
    example_cases: tuple[str, ...]
    green_policy: str


@dataclass(frozen=True)
class Round182ScoreStagePriceAlignment:
    case_id: str
    detected_stage: str
    price_path_status: str
    verdict: str
    normalization_adjustment: str


def _weights(
    visibility: int | str,
    eps_fcf: int | str,
    price: int | str,
    recurrence: int | str,
    redteam: int | str,
    directionality: int | str,
    valuation: int | str,
) -> Round182ScoreWeightDraft:
    return Round182ScoreWeightDraft(visibility, eps_fcf, price, recurrence, redteam, directionality, valuation)


def _target(
    target_id: str,
    archetype: E2RArchetype,
    posture: Round10ThemePosture,
    weight: Round182ScoreWeightDraft,
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
) -> Round182ScoreTarget:
    return Round182ScoreTarget(target_id, archetype, posture, weight, stage1, stage2, stage3, stage4b, stage4c, green, red, penalties, note, gate_only)


def _d(value: str) -> date:
    return date.fromisoformat(value)


GATE_WEIGHT = _weights("gate", "gate", "gate", "gate", "gate", "gate", "gate")
CAP_WEIGHT = _weights("cap", "cap", "cap", "cap", "+", "cap", "cap")

ROUND182_BASE_SCORE_WEIGHTS: tuple[Round182BaseScoreWeight, ...] = (
    Round182BaseScoreWeight("contract_budget_order_exploration_visibility", 26, "raise_actual_money_or_result", "R11 events only graduate when contracts, budgets, government orders, commercial exploration results, or institutional rules are verified."),
    Round182BaseScoreWeight("eps_fcf_revenue_guidance_conversion", 18, "raise_company_conversion", "Stage 3 needs company revenue, OP/EPS, FCF, or guidance conversion rather than news flow."),
    Round182BaseScoreWeight("price_path_event_detection", 14, "separate_event_rally_from_green", "Event stocks can move 20~30% quickly; the scorer must capture price reaction without calling it Stage 3."),
    Round182BaseScoreWeight("recurrence_durability", 12, "raise_repeatability", "Repeated procurement, commercial production, long-term contract, or durable institutional revenue is required before Green."),
    Round182BaseScoreWeight("redteam_disclosure_confidence", 14, "hard_redteam_gate", "Drill-bit failure, policy reversal, political shock, energy import shock, and low disclosure confidence can block unsafe Green."),
    Round182BaseScoreWeight("policy_directionality", 8, "split_winners_and_losers", "The same policy can help one basket and hurt another; directionality must be explicit."),
    Round182BaseScoreWeight("valuation_room_4b_runway", 8, "cool_price_only_event", "Price-only event rallies, short-selling squeezes, and policy-theme baskets often become 4B before Green."),
)

ROUND182_STAGE_CAPS: tuple[Round182StageCap, ...] = (
    Round182StageCap(
        "Stage 1",
        "45",
        ("policy_announcement", "exploration_announcement", "short_selling_rule_change", "political_shock", "war_or_hormuz_energy_shock", "disaster_news"),
        ("korea_east_sea_gas_discovery_stage1_4b_watch_case", "short_selling_ban_extension_policy_overlay_case"),
        "Large news can route research and validate event price-path, but it stays capped until actual money, contracts, or commercial results appear.",
    ),
    Round182StageCap(
        "Stage 2",
        "70",
        ("exploration_started", "budget_confirmed", "government_order", "monitoring_system_adopted", "contract_or_revenue_path_confirmed", "commerciality_workflow_visible"),
        ("short_selling_ban_extension_policy_overlay_case", "brokerage_short_selling_fines_market_trust_case"),
        "Stage 2 can recognize policy or institutional visibility, but Stage 3 still needs company-level EPS/FCF or durable revenue.",
    ),
    Round182StageCap(
        "Stage 3",
        "requires_5_of_8",
        ("contract_budget_order_or_commercial_exploration_result", "individual_company_revenue_or_guidance_raise", "op_eps_fcf_revision", "recurrence_or_long_term_contract", "stage2_60d_mfe_20pct", "policy_reversal_risk_low", "disclosure_detail_sufficient", "valuation_not_overheated"),
        ("none_yet_round182_green_restricted",),
        "R11 Stage 3 is rare; event price rally alone cannot pass this gate.",
    ),
    Round182StageCap(
        "Stage 4B",
        "requires_3_of_5",
        ("same_day_limit_up_or_1d_20pct", "news_without_contract_budget_or_revenue", "related_basket_indiscriminate_rally", "no_eps_revision", "community_or_news_keyword_crowding"),
        ("korea_east_sea_gas_discovery_stage1_4b_watch_case", "short_selling_resumption_high_beta_4b_watch_case"),
        "Cool R11 candidates when price moves before contracts, budgets, commerciality, or EPS/FCF evidence.",
    ),
    Round182StageCap(
        "Stage 4C",
        "hard_gate",
        ("exploration_failure_or_no_commerciality", "government_contract_cancelled_or_budget_withdrawn", "policy_reversal", "political_system_shock", "won_rate_oil_market_wide_riskoff", "short_selling_resumption_valuation_compression", "price_only_rally_unwinds_without_revenue", "disclosure_detail_absent_plus_price_only_rally"),
        ("political_system_shock_martial_law_case", "hormuz_middle_east_energy_import_shock_case"),
        "One hard political, energy, policy reversal, exploration failure, or market-wide shock can override otherwise positive candidates.",
    ),
)

ROUND182_SCORE_TARGETS: tuple[Round182ScoreTarget, ...] = (
    _target(
        "DOMESTIC_RESOURCE_DISCOVERY_EVENT",
        E2RArchetype.DOMESTIC_RESOURCE_DISCOVERY_EVENT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(12, 4, 18, 4, 18, 8, 6),
        stage1=("government_announcement", "possible_reserve_headline", "daily_limit_rally", "resource_theme_basket"),
        stage2=("exploratory_drilling_started", "budget_visible", "knoc_project_structure", "drill_result_partial"),
        stage3=("commercial_discovery", "appraisal_drilling", "development_plan", "commercial_production_or_long_term_contract", "op_eps_fcf_reflected"),
        stage4b=("daily_limit_rally_before_drilling", "resource_theme_crowding"),
        stage4c=("exploration_failure", "no_commerciality", "budget_cut", "result_delay"),
        green=("commercial_discovery", "development_plan", "commercial_production_or_long_term_contract", "op_eps_fcf_reflected"),
        red=("exploration_failure", "no_commerciality", "budget_cut", "result_delay"),
        penalties=("drill_bit", "commerciality", "time_to_revenue", "success_probability"),
        note="East Sea gas discovery is Stage 1 price-path evidence, not Stage 3 proof before drilling and commerciality.",
    ),
    _target(
        "RESOURCE_EXPLORATION_DRILL_BIT_GATE",
        E2RArchetype.RESOURCE_EXPLORATION_DRILL_BIT_GATE,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("prospect_estimate", "consultant_report", "government_announcement"),
        stage2=("knoc_drilling", "drilling_budget", "well_count_plan"),
        stage3=("commercial_reserve_confirmed", "final_investment_decision", "production_plan"),
        stage4b=("prospect_headline_priced_before_drilling",),
        stage4c=("80pct_failure_probability", "exploration_failure", "commerciality_absent", "woodside_caveat"),
        green=(),
        red=("80pct_failure_probability", "exploration_failure", "commerciality_absent", "woodside_caveat"),
        penalties=("failure_probability", "commerciality", "reserve_unconfirmed", "fid_missing"),
        note="Drill-bit gates prevent resource estimates from becoming Stage 3 before commercial reserves exist.",
        gate_only=True,
    ),
    _target(
        "ENERGY_SECURITY_POLICY_EVENT",
        E2RArchetype.ENERGY_SECURITY_POLICY_EVENT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(14, 8, 10, 8, 14, 10, 6),
        stage1=("energy_security_headline", "gas_oil_import_security", "domestic_resource_option"),
        stage2=("government_project_structure", "supply_security_policy", "import_substitution_path"),
        stage3=("company_revenue_path", "contract_or_margin_impact", "op_eps_fcf_conversion"),
        stage4b=("energy_security_theme_basket_rally",),
        stage4c=("oil_price_shock_cost_pressure", "policy_reversal", "exploration_failure"),
        green=("company_revenue_path", "contract_or_margin_impact", "op_eps_fcf_conversion"),
        red=("oil_price_shock_cost_pressure", "policy_reversal", "exploration_failure"),
        penalties=("import_cost", "policy_reversal", "exploration", "margin"),
        note="Energy-security policy can be Stage 1/2, but company revenue or margin path is required.",
    ),
    _target(
        "MARKET_STRUCTURE_SHORT_SELLING_POLICY",
        E2RArchetype.MARKET_STRUCTURE_SHORT_SELLING_POLICY,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(16, 4, 14, 6, 12, 18, 6),
        stage1=("short_selling_ban_extension", "illegal_short_selling_monitoring", "retail_confidence_narrative"),
        stage2=("monitoring_system_adopted", "rule_change_confirmed", "violating_institutions_fined", "resumption_schedule_confirmed"),
        stage3=("brokerage_revenue_or_roe_link", "trading_value_sustained", "company_eps_fcf_conversion"),
        stage4b=("high_beta_short_squeeze", "growth_basket_indiscriminate_rally"),
        stage4c=("short_selling_resumption", "valuation_compression", "foreign_hedge_activity_returns", "msci_accessibility_issue"),
        green=("brokerage_revenue_or_roe_link", "trading_value_sustained", "company_eps_fcf_conversion"),
        red=("short_selling_resumption", "valuation_compression", "foreign_hedge_activity_returns", "msci_accessibility_issue"),
        penalties=("fundamental_link_missing", "price_only_squeeze", "resumption", "foreign_access"),
        note="Short-selling policy is a market-structure overlay, not individual company Green evidence.",
    ),
    _target(
        "SHORT_SELLING_RESUMPTION_RISK",
        E2RArchetype.SHORT_SELLING_RESUMPTION_RISK,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("short_selling_ban_beneficiary", "high_short_interest_growth_basket"),
        stage2=("resumption_schedule", "monitoring_system"),
        stage3=("not_green_if_eps_fcf_missing",),
        stage4b=("price_only_short_squeeze", "high_beta_rally"),
        stage4c=("short_selling_resumption", "valuation_compression", "liquidity_reversal"),
        green=(),
        red=("short_selling_resumption", "valuation_compression", "liquidity_reversal"),
        penalties=("short_squeeze", "valuation", "resumption", "liquidity"),
        note="High-beta short-ban rallies are 4B/4C watch unless fundamentals confirm.",
        gate_only=True,
    ),
    _target(
        "POLITICAL_SYSTEM_SHOCK_KOREA",
        E2RArchetype.POLITICAL_SYSTEM_SHOCK_KOREA,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("martial_law", "impeachment_risk", "kospi_volatility", "won_fx_shock"),
        stage2=("market_stabilization_fund", "liquidity_support", "political_resolution_path"),
        stage3=("not_company_eps_fcf_evidence",),
        stage4b=("political_theme_rally_without_contract",),
        stage4c=("market_wide_risk_premium_spike", "foreign_outflow", "currency_volatility", "kospi_kosdaq_riskoff"),
        green=(),
        red=("market_wide_risk_premium_spike", "foreign_outflow", "currency_volatility", "kospi_kosdaq_riskoff"),
        penalties=("political_risk", "fx", "foreign_flow", "valuation_room"),
        note="Political system shock is a market-wide RedTeam overlay that temporarily cuts valuation room.",
        gate_only=True,
    ),
    _target(
        "GEOPOLITICAL_ENERGY_IMPORT_SHOCK",
        E2RArchetype.GEOPOLITICAL_ENERGY_IMPORT_SHOCK,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("middle_east_conflict", "hormuz_risk", "oil_price_shock", "won_volatility"),
        stage2=("policy_response", "energy_supply_stabilization", "market_stabilization"),
        stage3=("not_company_structural_green_evidence",),
        stage4b=("refinery_or_energy_theme_overreaction",),
        stage4c=("market_circuit_breaker", "exporter_riskoff", "airline_petrochemical_cost_shock", "won_weakness"),
        green=(),
        red=("market_circuit_breaker", "exporter_riskoff", "airline_petrochemical_cost_shock", "won_weakness"),
        penalties=("oil_import_dependency", "fx", "market_mae", "input_cost"),
        note="Korea is an energy importer; Hormuz or Middle East shock is a market-wide 4C overlay.",
        gate_only=True,
    ),
    _target(
        "EVENT_PRICE_RALLY_NOT_STAGE3",
        E2RArchetype.EVENT_PRICE_RALLY_NOT_STAGE3,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("same_day_limit_up", "event_headline", "basket_rally"),
        stage2=("verified_event_path", "budget_or_contract_possible"),
        stage3=("not_green_without_contract_budget_revenue",),
        stage4b=("price_rally_before_cashflow", "theme_keyword_crowding"),
        stage4c=("price_only_rally_unwinds", "no_revenue_conversion", "disclosure_detail_absent"),
        green=(),
        red=("price_only_rally_unwinds", "no_revenue_conversion", "disclosure_detail_absent"),
        penalties=("price_only", "crowding", "no_revenue", "detail_missing"),
        note="R11 explicitly records event price rallies but blocks Stage 3 unless cash-flow evidence appears.",
        gate_only=True,
    ),
    _target(
        "POLICY_DIRECTIONALITY_ERROR",
        E2RArchetype.POLICY_DIRECTIONALITY_ERROR,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("policy_or_political_theme", "tariff_short_selling_energy_policy", "political_event"),
        stage2=("affected_company_mapping", "winner_loser_split", "budget_or_contract_detail"),
        stage3=("company_revenue_or_margin_link", "directionality_verified"),
        stage4b=("policy_theme_basket_indiscriminate_rally",),
        stage4c=("policy_reversal", "wrong_beneficiary_mapping", "political_direction_reversal", "no_company_exposure"),
        green=(),
        red=("policy_reversal", "wrong_beneficiary_mapping", "political_direction_reversal", "no_company_exposure"),
        penalties=("directionality", "beneficiary_mapping", "policy_reversal", "no_exposure"),
        note="The same policy can help or hurt different baskets; wrong beneficiary mapping must cap Green.",
        gate_only=True,
    ),
    _target(
        "DISCLOSURE_CONFIDENCE_CAP",
        E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        Round10ThemePosture.REDTEAM_FIRST,
        CAP_WEIGHT,
        stage1=("event_headline", "policy_headline", "resource_or_shock_headline"),
        stage2=("budget_contract_order_detail_required", "exploration_result_required", "guidance_detail_required"),
        stage3=("multi_source_confirmation", "detail_fields_verified", "company_conversion_verified"),
        stage4b=("headline_rerating",),
        stage4c=("budget_detail_missing", "contract_detail_missing", "exploration_result_missing", "guidance_missing", "price_only_rally"),
        green=("budget_contract_order_detail", "exploration_result", "guidance_detail", "company_conversion"),
        red=("budget_detail_missing", "contract_detail_missing", "exploration_result_missing", "guidance_missing", "price_only_rally"),
        penalties=("disclosure", "detail", "guidance", "parser_confidence"),
        note="R11 headlines stay capped when budget, contract, order, exploration result, or guidance detail is missing.",
    ),
)

ROUND182_SCORE_STAGE_PRICE_ALIGNMENT: tuple[Round182ScoreStagePriceAlignment, ...] = (
    Round182ScoreStagePriceAlignment("korea_east_sea_gas_discovery_stage1_4b_watch_case", "Stage 1 plus 4B-watch", "KOGAS and Daesung Energy rallied near +30% on resource possibility before drill-bit results", "resource_event_rally_not_stage3", "capture price-path as Stage 1; block Stage 3 until commercial discovery and OP/EPS evidence"),
    Round182ScoreStagePriceAlignment("short_selling_ban_extension_policy_overlay_case", "Stage 1/2 policy overlay", "Market-structure policy can support sentiment but not company EPS by itself", "short_selling_policy_not_company_green", "separate liquidity overlay from company fundamentals"),
    Round182ScoreStagePriceAlignment("political_system_shock_martial_law_case", "market-wide 4C overlay", "Martial-law shock raises Korea risk premium and cuts valuation room", "political_shock_hard_overlay", "apply market-wide RedTeam overlay rather than company Green evidence"),
    Round182ScoreStagePriceAlignment("hormuz_middle_east_energy_import_shock_case", "market-wide 4C overlay", "Energy import shock drove Korea market and FX risk-off", "energy_import_shock_hard_overlay", "cut valuation room and raise MAE risk for affected exporters and cost-sensitive sectors"),
    Round182ScoreStagePriceAlignment("brokerage_short_selling_fines_market_trust_case", "Stage 1/2 trust evidence", "Institutional fines can improve market trust but do not prove brokerage ROE", "market_trust_not_brokerage_green", "require trading value, IB/WM, PF risk, and ROE before brokerage Stage 3"),
)

ROUND182_CASE_CANDIDATES: tuple[Round182CaseCandidate, ...] = (
    Round182CaseCandidate(
        "korea_east_sea_gas_discovery_stage1_4b_watch_case",
        "DOMESTIC_RESOURCE_DISCOVERY_EVENT",
        "036460/117580/096770/018670",
        "KOGAS Daesung Energy SK Innovation SK Gas East Sea gas discovery event",
        "KR",
        "4b_watch",
        _d("2024-06-03"),
        None,
        None,
        _d("2024-06-03"),
        None,
        ("government_announcement", "14bn_barrels_possible_reserves", "kogas_plus_30pct", "daesung_energy_plus_30pct", "sk_innovation_plus_6pct", "sk_gas_plus_7pct"),
        ("pre_drilling_commerciality_absent", "success_probability_20pct", "failure_probability_80pct", "op_eps_fcf_absent"),
        "stage1_price_path_success_not_stage3",
        "needs_drill_result_commerciality_revenue_price_backfill",
        ("round_182.md Reuters East Sea gas prospects",),
        "East Sea gas discovery is the R11 textbook Stage 1 price-path event and 4B-watch, not Stage 3 before commerciality.",
        (E2RArchetype.EVENT_PRICE_RALLY_NOT_STAGE3, E2RArchetype.RESOURCE_EXPLORATION_DRILL_BIT_GATE),
    ),
    Round182CaseCandidate(
        "korea_gas_daewang_whale_drill_bit_gate_case",
        "RESOURCE_EXPLORATION_DRILL_BIT_GATE",
        "036460/117580",
        "Daewang Whale East Sea exploration drill-bit gate",
        "KR",
        "failed_rerating",
        _d("2024-06-07"),
        None,
        None,
        _d("2024-06-07"),
        None,
        ("consultant_report", "great_potential_headline", "knoc_drilling_needed", "success_probability_20pct"),
        ("failure_probability_80pct", "commercial_reserve_unconfirmed", "woodside_caveat", "final_investment_decision_missing"),
        "drill_bit_gate_blocks_green",
        "needs_exploration_result_reserve_fid_price_backfill",
        ("round_182.md Reuters consultant caveat",),
        "Resource exploration must pass drill-bit and commerciality gates before any Stage 3 consideration.",
    ),
    Round182CaseCandidate(
        "energy_security_policy_event_skgas_skinno_case",
        "ENERGY_SECURITY_POLICY_EVENT",
        "096770/018670/010950",
        "SK Innovation SK Gas S-Oil Korea energy-security policy event",
        "KR",
        "event_premium",
        _d("2024-06-03"),
        None,
        None,
        None,
        None,
        ("domestic_resource_option", "energy_security_headline", "sk_innovation_plus_6pct", "sk_gas_plus_7pct"),
        ("direct_company_revenue_link_missing", "exploration_result_missing", "oil_import_cost_risk"),
        "energy_security_headline_not_revenue_until_contract_or_margin",
        "needs_company_revenue_margin_price_backfill",
        ("round_182.md East Sea gas and energy-security reaction",),
        "Energy-security policy can move related names, but company revenue or margin path must be proven.",
    ),
    Round182CaseCandidate(
        "short_selling_ban_extension_policy_overlay_case",
        "MARKET_STRUCTURE_SHORT_SELLING_POLICY",
        "KR_SHORT_SELLING_POLICY_BASKET",
        "Korea short-selling ban extension and monitoring system policy overlay",
        "KR",
        "event_premium",
        _d("2024-04-25"),
        _d("2024-06-13"),
        None,
        None,
        None,
        ("illegal_short_selling_monitoring_system", "short_selling_ban_extended_to_2025_q1", "retail_investor_confidence", "market_transparency_debate"),
        ("company_fundamental_link_missing", "msci_accessibility_issue", "short_selling_resumption_risk"),
        "market_structure_event_not_company_stage3",
        "needs_trading_value_brokerage_roe_price_backfill",
        ("round_182.md Reuters short-selling ban extension", "round_182.md Reuters monitoring system"),
        "Short-selling policy is a market-structure overlay; individual Stage 3 needs company revenue/ROE evidence.",
        (E2RArchetype.SHORT_SELLING_RESUMPTION_RISK,),
    ),
    Round182CaseCandidate(
        "short_selling_resumption_high_beta_4b_watch_case",
        "SHORT_SELLING_RESUMPTION_RISK",
        "KR_HIGH_SHORT_INTEREST_GROWTH_BASKET",
        "KOSDAQ high-beta short-selling ban beneficiary basket",
        "KR",
        "4b_watch",
        _d("2024-06-13"),
        None,
        None,
        _d("2024-06-13"),
        None,
        ("short_selling_ban_beneficiary", "high_short_interest_growth_basket", "price_only_short_squeeze"),
        ("eps_fcf_missing", "short_selling_resumption_risk", "valuation_compression_risk"),
        "short_ban_squeeze_is_4b_watch_without_fundamentals",
        "needs_eps_fcf_resumption_price_backfill",
        ("round_182.md short-selling policy high-beta risk",),
        "High-beta short-ban rallies are 4B-watch unless EPS/FCF confirms.",
    ),
    Round182CaseCandidate(
        "political_system_shock_martial_law_case",
        "POLITICAL_SYSTEM_SHOCK_KOREA",
        "KR_MARKET",
        "Korea martial-law political system shock",
        "KR",
        "4c_thesis_break",
        _d("2024-12-03"),
        None,
        None,
        None,
        _d("2024-12-03"),
        ("martial_law_declaration", "national_assembly_reversal", "kospi_decline", "market_stabilization_fund_ready"),
        ("political_system_shock", "currency_volatility", "foreign_risk_premium", "valuation_room_temporary_cut"),
        "market_wide_political_4c_overlay",
        "needs_market_fx_sector_mae_backfill",
        ("round_182.md Reuters martial law", "round_182.md Barrons market reaction"),
        "Martial-law shock is a market-wide R11 overlay that lowers valuation room for otherwise valid candidates.",
    ),
    Round182CaseCandidate(
        "hormuz_middle_east_energy_import_shock_case",
        "GEOPOLITICAL_ENERGY_IMPORT_SHOCK",
        "KR_MARKET/HYUNDAI/SAMSUNG/SKHYNIX",
        "Korea market Hormuz and Middle East energy-import shock",
        "KR",
        "4c_thesis_break",
        _d("2026-03-04"),
        None,
        None,
        None,
        _d("2026-03-04"),
        ("middle_east_iran_conflict", "kospi_minus_12_06pct", "won_17y_low", "hyundai_minus_15_8pct", "samsung_electronics_minus_11_7pct", "sk_hynix_minus_9_6pct"),
        ("oil_import_dependency", "won_volatility", "exporter_riskoff", "market_wide_mae_risk"),
        "geopolitical_energy_import_shock_4c_overlay",
        "needs_oil_fx_sector_mae_backfill",
        ("round_182.md Reuters Iran conflict Korea market shock",),
        "Energy-import shock can override sector evidence by cutting valuation room and raising MAE risk.",
    ),
    Round182CaseCandidate(
        "event_price_rally_not_stage3_daewang_whale_case",
        "EVENT_PRICE_RALLY_NOT_STAGE3",
        "036460/117580",
        "Daewang Whale event price rally is not Stage 3",
        "KR",
        "4b_watch",
        _d("2024-06-03"),
        None,
        None,
        _d("2024-06-03"),
        None,
        ("same_day_limit_up", "resource_headline", "basket_rally", "price_signal_plus_8"),
        ("pre_drilling_stage3_cap", "success_probability_20pct", "commercial_production_delay", "no_eps_revision"),
        "big_price_move_is_not_stage3_evidence",
        "needs_commerciality_eps_price_backfill",
        ("round_182.md event rally cap section",),
        "A +20~30% event rally is price-path evidence, not Stage 3 evidence without cash-flow conversion.",
    ),
    Round182CaseCandidate(
        "political_theme_event_premium_directionality_case",
        "POLICY_DIRECTIONALITY_ERROR",
        "KR_POLITICAL_THEME_BASKET",
        "Korea political theme event premium directionality case",
        "KR",
        "event_premium",
        _d("2024-12-03"),
        None,
        None,
        _d("2024-12-03"),
        None,
        ("political_event", "policy_theme_price_move", "theme_basket_rally"),
        ("budget_contract_missing", "fundamental_link_missing", "policy_direction_reversal_risk", "no_company_exposure"),
        "political_theme_price_move_not_stage3",
        "needs_budget_contract_company_exposure_backfill",
        ("round_182.md political theme event premium section",),
        "Political or policy theme rallies need beneficiary directionality, budget, contract, and company exposure checks.",
    ),
    Round182CaseCandidate(
        "brokerage_short_selling_fines_market_trust_case",
        "MARKET_STRUCTURE_SHORT_SELLING_POLICY",
        "KR_BROKERAGE_BASKET",
        "Korea brokerage short-selling fines and market trust evidence",
        "KR",
        "failed_rerating",
        _d("2025-02-13"),
        _d("2025-02-13"),
        None,
        None,
        None,
        ("jpmorgan_morgan_stanley_nomura_ubs_fined", "market_trust_policy_evidence", "illegal_short_selling_enforcement"),
        ("brokerage_earnings_link_missing", "trading_value_missing", "ib_wm_roe_missing", "pf_risk_unchecked"),
        "market_trust_policy_not_brokerage_stage3_without_roe",
        "needs_trading_value_ib_wm_pf_roe_backfill",
        ("round_182.md Reuters short-selling fines",),
        "Short-selling enforcement can improve trust, but brokerage Stage 3 needs trading value, IB/WM, PF risk, and ROE evidence.",
    ),
    Round182CaseCandidate(
        "r11_disclosure_confidence_cap_case",
        "DISCLOSURE_CONFIDENCE_CAP",
        "KR_R11_DISCLOSURE_BASKET",
        "Korea R11 disclosure confidence cap basket",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("event_headline", "policy_headline", "resource_or_shock_headline"),
        ("budget_detail_missing", "contract_detail_missing", "exploration_result_missing", "guidance_missing", "price_only_rally"),
        "event_detail_missing_cap",
        "needs_budget_contract_order_exploration_guidance_backfill",
        ("round_182.md R11 disclosure confidence cap",),
        "R11 headline evidence is capped when budget, contract, order, exploration result, or guidance detail is missing.",
    ),
)

ROUND182_PRICE_FIELDS: tuple[str, ...] = (
    "ticker",
    "company_name",
    "event_type",
    "event_date",
    "event_headline",
    "event_source",
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
    "price_at_event",
    "price_at_stage1",
    "price_at_stage2",
    "price_at_stage3",
    "price_at_stage4b",
    "price_at_stage4c",
    "return_1d_after_event",
    "return_5d_after_event",
    "return_20d_after_event",
    "return_60d_after_event",
    "return_120d_after_event",
    "mfe_5d_after_event",
    "mae_5d_after_event",
    "mfe_20d_after_event",
    "mae_20d_after_event",
    "mfe_60d_after_event",
    "mae_60d_after_event",
    "mfe_120d_after_event",
    "mae_120d_after_event",
    "relative_strength_vs_kospi",
    "relative_strength_vs_sector",
    "market_wide_shock_flag",
    "daily_limit_flag",
    "volume_spike_flag",
    "contract_or_budget_confirmed",
    "government_order_flag",
    "exploration_result_flag",
    "commerciality_confirmed_flag",
    "guidance_raised_flag",
    "op_revision_after_event",
    "eps_revision_after_event",
    "policy_reversal_risk",
    "drill_bit_gate",
    "resource_success_probability",
    "funding_withdrawal_flag",
    "market_structure_event_flag",
    "short_selling_resumption_flag",
    "political_risk_flag",
    "geopolitical_energy_shock_flag",
    "disclosure_confidence",
    "valuation_at_stage2",
    "valuation_at_stage4b",
)


def round182_target_for(target_id: str) -> Round182ScoreTarget | None:
    for target in ROUND182_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round182_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND182_CASE_CANDIDATES:
        target = round182_target_for(candidate.target_id)
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
                f"Round182 R11 Loop-11 case for {candidate.target_id}; "
                "Korea policy, geopolitical, disaster, resource, short-selling, and market-shock headlines are separated from contracts, budgets, orders, commercial exploration, revenue guidance, EPS/FCF, and price-path evidence."
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
                "event_news_is_not_green_evidence_alone",
                "contract_budget_order_exploration_revenue_or_eps_required",
                "stage3_early_catch_requires_5_of_8_loop11_conditions",
                "do_not_invent_contracts_budgets_orders_exploration_results_guidance_stage_prices_or_mfe_mae",
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


def round182_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND182_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "contract_budget_order_exploration_visibility": str(weights["contract_budget_order_exploration_visibility"]),
                "eps_fcf_revenue_guidance_conversion": str(weights["eps_fcf_revenue_guidance_conversion"]),
                "price_path_event_detection": str(weights["price_path_event_detection"]),
                "recurrence_durability": str(weights["recurrence_durability"]),
                "redteam_disclosure_confidence": str(weights["redteam_disclosure_confidence"]),
                "policy_directionality": str(weights["policy_directionality"]),
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


def round182_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND182_CASE_CANDIDATES:
        target = round182_target_for(candidate.target_id)
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


def round182_stage_date_rows() -> tuple[dict[str, str], ...]:
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
        for target in ROUND182_SCORE_TARGETS
    )


def round182_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round182_backfill": "true"} for field in ROUND182_PRICE_FIELDS)


def round182_base_score_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "component": item.component,
            "points": str(item.points),
            "loop11_direction": item.loop11_direction,
            "reason": item.reason,
            "production_scoring_changed": "false",
        }
        for item in ROUND182_BASE_SCORE_WEIGHTS
    )


def round182_stage_cap_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "stage_band": item.stage_band,
            "max_score": item.max_score,
            "required_evidence": "|".join(item.required_evidence),
            "example_cases": "|".join(item.example_cases),
            "green_policy": item.green_policy,
            "production_scoring_changed": "false",
        }
        for item in ROUND182_STAGE_CAPS
    )


def round182_score_stage_price_alignment_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "case_id": item.case_id,
            "detected_stage": item.detected_stage,
            "price_path_status": item.price_path_status,
            "verdict": item.verdict,
            "normalization_adjustment": item.normalization_adjustment,
            "production_scoring_changed": "false",
        }
        for item in ROUND182_SCORE_STAGE_PRICE_ALIGNMENT
    )


def round182_summary() -> dict[str, int | bool]:
    records = round182_case_records()
    return {
        "target_count": len(ROUND182_SCORE_TARGETS),
        "source_canonical_target_count": ROUND182_SOURCE_CANONICAL_TARGET_COUNT,
        "case_candidate_count": len(records),
        "base_score_component_count": len(ROUND182_BASE_SCORE_WEIGHTS),
        "stage_cap_count": len(ROUND182_STAGE_CAPS),
        "score_stage_price_alignment_count": len(ROUND182_SCORE_STAGE_PRICE_ALIGNMENT),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND182_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND182_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND182_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "gate_only_target_count": sum(1 for target in ROUND182_SCORE_TARGETS if target.gate_only),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round182_r11_loop11_reports(
    *,
    output_directory: str | Path = ROUND182_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND182_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND182_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round182_r11_loop11_policy_geopolitical_event_summary.md",
        "case_matrix": output / "round182_r11_loop11_case_matrix.csv",
        "stage_date_plan": output / "round182_r11_loop11_stage_date_plan.csv",
        "green_guardrails": output / "round182_r11_loop11_green_guardrails.md",
        "risk_overlays": output / "round182_r11_loop11_risk_overlays.md",
        "price_validation_plan": output / "round182_r11_loop11_price_validation_plan.md",
        "price_fields": output / "round182_r11_loop11_price_fields.csv",
        "base_score_weights": output / "round182_r11_loop11_base_score_weights.csv",
        "stage_caps": output / "round182_r11_loop11_stage_caps.csv",
        "score_stage_price_alignment": output / "round182_r11_loop11_score_stage_price_alignment.csv",
        "score_stage_price_alignment_md": output / "round182_r11_loop11_score_stage_price_alignment.md",
    }
    _write_case_jsonl(round182_case_records(), cases)
    _write_rows(round182_score_profile_rows(), score_profiles)
    _write_rows(round182_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round182_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round182_price_field_rows(), paths["price_fields"])
    _write_rows(round182_base_score_weight_rows(), paths["base_score_weights"])
    _write_rows(round182_stage_cap_rows(), paths["stage_caps"])
    _write_rows(round182_score_stage_price_alignment_rows(), paths["score_stage_price_alignment"])
    paths["summary"].write_text(render_round182_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round182_green_guardrail_markdown(), encoding="utf-8")
    paths["risk_overlays"].write_text(render_round182_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round182_price_validation_plan_markdown(), encoding="utf-8")
    paths["score_stage_price_alignment_md"].write_text(render_round182_score_stage_price_alignment_markdown(), encoding="utf-8")
    return paths


def render_round182_summary_markdown() -> str:
    summary = round182_summary()
    lines = [
        "# Round-182 R11 Loop-11 Korea Policy / Geopolitical / Event Summary",
        "",
        f"- source_round: `{ROUND182_SOURCE_ROUND_PATH}`",
        "- large_sector: `POLICY_GEOPOLITICAL_EVENT`",
        "- loop: `R11 Loop 11 / v11.0`",
        f"- target_count: {summary['target_count']}",
        f"- source_canonical_target_count: {summary['source_canonical_target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- base_score_component_count: {summary['base_score_component_count']}",
        f"- stage_cap_count: {summary['stage_cap_count']}",
        f"- score_stage_price_alignment_count: {summary['score_stage_price_alignment_count']}",
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
        "- R11 Loop 11 separates big policy/event news from actual contract, budget, order, exploration result, and EPS/FCF conversion.",
        "- Example: KOGAS and Daesung Energy can rally on East Sea gas news, but Stage 3 waits for commercial discovery and company earnings evidence.",
        "- Example: short-selling policy is a market-structure overlay, not company Green evidence.",
        "- Example: martial-law and Hormuz-style energy shocks are market-wide 4C overlays that cut valuation room.",
    ]
    return "\n".join(lines) + "\n"


def render_round182_green_guardrail_markdown() -> str:
    lines = [
        "# Round-182 R11 Loop-11 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Loop-11 penalties |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND182_SCORE_TARGETS:
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
            "- Do not apply R11 Loop-11 v11.0 weights to production scoring yet.",
            "- Do not treat policy announcement, exploration headline, short-selling ban, political event, or war shock as Green evidence by itself.",
            "- Do not invent contracts, budgets, government orders, exploration results, guidance, stage prices, or MFE/MAE.",
            "- Green requires actual money/result plus company revenue, OP/EPS, FCF, recurrence, and low policy reversal risk.",
            "- Price-only rallies, drill-bit risk, policy reversal, martial-law shock, energy-import shock, and low disclosure confidence remain RedTeam gates.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round182_risk_overlay_markdown() -> str:
    lines = [
        "# Round-182 R11 Loop-11 Risk Overlays",
        "",
        "| target | stage4c conditions | red flags |",
        "| --- | --- | --- |",
    ]
    for target in ROUND182_SCORE_TARGETS:
        if target.red_flags or target.gate_only:
            lines.append(f"| `{target.target_id}` | {', '.join(target.stage4c_conditions)} | {', '.join(target.red_flags)} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- R11 is especially sensitive to drill-bit, policy reversal, market-structure, political, FX, oil, and market-wide shock risks.",
            "- Example: a +30% event rally is useful price-path evidence but can still be 4B-watch.",
            "- Example: martial-law shock is not a company event; it temporarily lowers valuation room across the market.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round182_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-182 R11 Loop-11 Price Validation Plan",
        "",
        "R11 needs event-date price-path validation because policy, exploration, short-selling, political, and energy shocks move prices before fundamentals confirm.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND182_PRICE_FIELDS)
    lines.extend(
        [
            "",
            "## Case Backfill Priorities",
            "",
            "- `korea_east_sea_gas_discovery_stage1_4b_watch_case`: event date returns, daily-limit flags, commerciality result, and OP/EPS linkage.",
            "- `short_selling_ban_extension_policy_overlay_case`: short-selling policy dates, trading value, brokerage ROE, and resumption impact.",
            "- `political_system_shock_martial_law_case`: KOSPI/KOSDAQ, won, foreign flow, and valuation-room impact.",
            "- `hormuz_middle_east_energy_import_shock_case`: oil, FX, sector MAE, exporter risk-off, and cost-sensitive sector hit.",
            "- `brokerage_short_selling_fines_market_trust_case`: enforcement dates, brokerage earnings link, trading value, IB/WM, PF risk, and ROE.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round182_score_stage_price_alignment_markdown() -> str:
    lines = [
        "# Round-182 R11 Loop-11 Score / Stage / Price Alignment",
        "",
        "| case | detected stage | price path status | verdict | adjustment |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in ROUND182_SCORE_STAGE_PRICE_ALIGNMENT:
        lines.append(f"| `{row.case_id}` | {row.detected_stage} | {row.price_path_status} | {row.verdict} | {row.normalization_adjustment} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- KOGAS/Daesung Energy show why event rallies must be captured but capped before commercial evidence.",
            "- Short-selling policy shows why market structure must be separated from company fundamentals.",
            "- Martial-law and Hormuz shocks show why R11 can reduce valuation room across otherwise valid candidates.",
        ]
    )
    return "\n".join(lines) + "\n"


def _score_weight_hint(target: Round182ScoreTarget) -> Mapping[str, float]:
    values: dict[str, float] = {}
    for key, value in target.score_weight.as_dict().items():
        if isinstance(value, int):
            values[key] = float(value)
    return values


def _score_price_alignment(candidate: Round182CaseCandidate) -> str:
    if candidate.case_type == "event_premium":
        return "price_moved_without_evidence"
    if candidate.case_type == "4c_thesis_break":
        return "false_positive_score"
    if candidate.case_type == "failed_rerating":
        return "evidence_good_but_price_failed"
    if candidate.case_type == "4b_watch":
        return "price_moved_without_evidence"
    return "unknown"


def _rerating_result(candidate: Round182CaseCandidate) -> str:
    if candidate.case_type == "event_premium":
        return "event_premium"
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    if candidate.case_type == "failed_rerating":
        return "no_rerating"
    if candidate.case_type == "4b_watch":
        return "theme_overheat"
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
    "ROUND182_BASE_SCORE_WEIGHTS",
    "ROUND182_CASE_CANDIDATES",
    "ROUND182_DEFAULT_CASES_PATH",
    "ROUND182_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND182_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND182_PRICE_FIELDS",
    "ROUND182_SCORE_STAGE_PRICE_ALIGNMENT",
    "ROUND182_SCORE_TARGETS",
    "ROUND182_SOURCE_CANONICAL_TARGET_COUNT",
    "ROUND182_SOURCE_CANONICAL_TARGET_IDS",
    "ROUND182_STAGE_CAPS",
    "render_round182_green_guardrail_markdown",
    "render_round182_price_validation_plan_markdown",
    "render_round182_risk_overlay_markdown",
    "render_round182_score_stage_price_alignment_markdown",
    "render_round182_summary_markdown",
    "round182_base_score_weight_rows",
    "round182_case_candidate_rows",
    "round182_case_records",
    "round182_price_field_rows",
    "round182_score_profile_rows",
    "round182_score_stage_price_alignment_rows",
    "round182_stage_cap_rows",
    "round182_stage_date_rows",
    "round182_summary",
    "round182_target_for",
    "write_round182_r11_loop11_reports",
]
