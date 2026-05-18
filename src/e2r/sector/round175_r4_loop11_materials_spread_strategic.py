"""Round-175 R4 Loop-11 Korea materials, spreads, and strategic resources.

Round 175 applies Loop 11 to Korea-focused copper/grid wires, Poongsan's
copper-defense hybrid, OCI polysilicon report risk, Korean steel tariff
directionality, lithium/rare-earth price events, and commodity/spread caps.

It is calibration/report material only. Production feature engineering,
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


ROUND175_SOURCE_ROUND_PATH = "docs/round/round_175.md"
ROUND175_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round175_r4_loop11_materials_spread_strategic"
ROUND175_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r4_loop11_round175.jsonl"
ROUND175_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round175_r4_loop11_v11.csv"
ROUND175_SOURCE_CANONICAL_TARGET_IDS: tuple[str, ...] = (
    "COPPER_AI_GRID_KOREA",
    "COPPER_PROCESSING_PLUS_DEFENSE",
    "DEFENSE_AMMO_EVENT_PREMIUM",
    "POLYSILICON_NON_CHINA_SUPPLY_OPTION",
    "POLYSILICON_REPORT_NOT_CONTRACT",
    "STEEL_TARIFF_EVENT_KOREA",
    "STEEL_EXPORT_TARIFF_4C",
    "SPECIALTY_STEEL_US_LOCALIZATION_OPTION",
    "LITHIUM_PRICE_EVENT_KOREA",
    "RARE_EARTH_THEME_KOREA",
    "CHEMICAL_SPREAD_KOREA",
    "EVENT_PREMIUM_GOVERNANCE_OVERLAY",
    "DISCLOSURE_CONFIDENCE_CAP",
)
ROUND175_SOURCE_CANONICAL_TARGET_COUNT = len(ROUND175_SOURCE_CANONICAL_TARGET_IDS)


@dataclass(frozen=True)
class Round175ScoreWeightDraft:
    eps_fcf_opm: int | str
    contract_offtake_customer_visibility: int | str
    bottleneck_pricing: int | str
    early_price_validation: int | str
    cycle_spread_durability: int | str
    disclosure_redteam: int | str
    valuation_4b_room: int | str

    def as_dict(self) -> dict[str, int | str]:
        return {
            "eps_fcf_opm": self.eps_fcf_opm,
            "contract_offtake_customer_visibility": self.contract_offtake_customer_visibility,
            "bottleneck_pricing": self.bottleneck_pricing,
            "early_price_validation": self.early_price_validation,
            "cycle_spread_durability": self.cycle_spread_durability,
            "disclosure_redteam": self.disclosure_redteam,
            "valuation_4b_room": self.valuation_4b_room,
        }


@dataclass(frozen=True)
class Round175ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round175ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    loop11_penalty_axes: tuple[str, ...]
    normalization_point: str
    hard_gate: bool = False

    @property
    def large_sector(self) -> Round10LargeSector:
        return Round10LargeSector.MATERIALS_SPREAD_STRATEGIC

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round175CaseCandidate:
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
class Round175BaseScoreWeight:
    component: str
    points: int
    loop11_direction: str
    reason: str

    def as_row(self) -> dict[str, str]:
        return {
            "component": self.component,
            "points": str(self.points),
            "loop11_direction": self.loop11_direction,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class Round175StageCap:
    stage_band: str
    max_score: str
    required_evidence: tuple[str, ...]
    example_cases: tuple[str, ...]
    green_policy: str

    def as_row(self) -> dict[str, str]:
        return {
            "stage_band": self.stage_band,
            "max_score": self.max_score,
            "required_evidence": "|".join(self.required_evidence),
            "example_cases": "|".join(self.example_cases),
            "green_policy": self.green_policy,
        }


@dataclass(frozen=True)
class Round175ScoreStagePriceAlignment:
    case_id: str
    detected_stage: str
    price_path_status: str
    verdict: str
    normalization_adjustment: str

    def as_row(self) -> dict[str, str]:
        return {
            "case_id": self.case_id,
            "detected_stage": self.detected_stage,
            "price_path_status": self.price_path_status,
            "verdict": self.verdict,
            "normalization_adjustment": self.normalization_adjustment,
        }


def _weights(
    eps: int | str,
    visibility: int | str,
    bottleneck: int | str,
    price: int | str,
    cycle: int | str,
    disclosure: int | str,
    valuation: int | str,
) -> Round175ScoreWeightDraft:
    return Round175ScoreWeightDraft(eps, visibility, bottleneck, price, cycle, disclosure, valuation)


def _target(
    target_id: str,
    archetype: E2RArchetype,
    posture: Round10ThemePosture,
    weight: Round175ScoreWeightDraft,
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
    hard_gate: bool = False,
) -> Round175ScoreTarget:
    return Round175ScoreTarget(
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
        hard_gate,
    )


ROUND175_BASE_SCORE_WEIGHTS: tuple[Round175BaseScoreWeight, ...] = (
    Round175BaseScoreWeight(
        "eps_fcf_opm_conversion",
        22,
        "keep_high",
        "Commodity price is capped until OP/EPS/FCF and margin conversion are visible.",
    ),
    Round175BaseScoreWeight(
        "contract_offtake_customer_visibility",
        20,
        "raise_detail_requirement",
        "Customer, contract amount, period, offtake, price floor, and confirmed sale terms drive Stage 2.",
    ),
    Round175BaseScoreWeight(
        "bottleneck_pricing_power",
        16,
        "allow_macro_bottleneck_but_cap_green",
        "Copper shortage, non-China supply, tariffs, and strategic scarcity matter only when company economics follow.",
    ),
    Round175BaseScoreWeight(
        "early_price_path_validation",
        12,
        "loop11_axis",
        "Stage 2 after-rally MFE/MAE and event-day moves distinguish early catch from late event chasing.",
    ),
    Round175BaseScoreWeight(
        "cycle_spread_durability",
        12,
        "raise_for_r4",
        "R4 must test raw material prices, inventory P/L, export volume, spread, and pass-through durability.",
    ),
    Round175BaseScoreWeight(
        "disclosure_confidence_redteam",
        10,
        "hard_review",
        "Media-only, report-only, company denial, missing terms, CB/BW, and direct tariff exposure can hard-cap the case.",
    ),
    Round175BaseScoreWeight(
        "valuation_room_4b_runway",
        8,
        "cool_event_rallies",
        "Theme baskets, commodity spikes, M&A rumors, and tariff rallies reduce runway quickly.",
    ),
)


ROUND175_STAGE_CAPS: tuple[Round175StageCap, ...] = (
    Round175StageCap(
        "Stage 1",
        "45",
        ("copper_price_up", "steel_tariff", "lithium_rebound", "rare_earth_export_control", "polysilicon_supply_chain", "mna_rumor"),
        ("copper_ai_grid_korea_basket_stage2_cap_case", "lithium_rare_earth_price_only_theme_case"),
        "Commodity, tariff, and resource keywords route research only. They do not create Stage 3.",
    ),
    Round175StageCap(
        "Stage 2",
        "70",
        ("contract", "offtake", "actual_customer", "policy_or_tariff_confirmed", "factory_or_capa_detail", "mna_bid_or_sale_terms"),
        ("poongsan_copper_defense_mna_unwind_case", "oci_holdings_spacex_polysilicon_report_cap_case"),
        "Stage 2 is possible when evidence is real, but Green waits for OP/EPS/FCF and durability.",
    ),
    Round175StageCap(
        "Stage 3",
        "requires_4_of_7",
        ("price_increase_to_op_eps", "export_volume_or_sales_volume_up", "cost_pass_through", "offtake_or_price_floor", "60d_mfe_20pct", "valuation_not_overheated", "disclosure_detail_sufficient"),
        ("copper_ai_grid_korea_basket_stage2_cap_case",),
        "Stage 3 is possible only when commodity/spread gains lock into company earnings and the price path is not already 4B.",
    ),
    Round175StageCap(
        "Stage 4B",
        "requires_3_of_5",
        ("one_day_commodity_tariff_export_control_rally_10pct", "stage2_120d_mfe_80pct", "narrative_rises_before_contract_revenue", "eps_revision_lags_price", "theme_basket_broad_rally"),
        ("lithium_rare_earth_price_only_theme_case", "steel_tariff_directionality_korea_case"),
        "Commodity and tariff rallies are cooled when earnings cannot follow.",
    ),
    Round175StageCap(
        "Stage 4C",
        "hard_gate",
        ("mna_review_dropped_or_sale_denied", "media_report_only_no_contract", "direct_export_tariff_hit", "commodity_price_crash", "spread_reworsens", "cb_bw_or_equity_raise", "op_eps_revision_down", "inventory_loss_expands", "production_or_export_volume_declines"),
        ("poongsan_copper_defense_mna_unwind_case", "seah_steel_export_tariff_4c_case"),
        "Hard RedTeam overrides event narratives when terms disappear, tariffs hit exports, or spreads reverse.",
    ),
)


ROUND175_SCORE_TARGETS: tuple[Round175ScoreTarget, ...] = (
    _target(
        "COPPER_AI_GRID_KOREA",
        E2RArchetype.COPPER_AI_GRID_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(20, 14, 20, 12, 12, 8, 7),
        stage1=("copper_price_up", "ai_data_center", "power_grid", "ev_energy_transition", "mine_disruption"),
        stage2=("copper_price_confirmed", "grid_wire_order", "backlog", "copper_passthrough", "op_eps_revision"),
        stage3=("individual_order_backlog_up", "opm_defended", "copper_passthrough_contract", "fcf_improvement", "60d_mfe_20pct"),
        stage4b=("copper_price_only_rally", "grid_wire_basket_crowded", "eps_revision_lags_price"),
        stage4c=("copper_price_reversal", "inventory_loss", "opm_drop", "orders_missing"),
        green=("order_backlog", "copper_passthrough", "opm", "op_eps_revision", "fcf"),
        red=("price_only_rally", "orders_missing", "opm_missing", "inventory_loss"),
        penalties=("commodity_cycle", "individual_order_missing", "opm_missing"),
        note="Copper AI-grid macro is Stage 1/2; Korean wires and processors need orders, pass-through, OPM, and FCF before Stage 3.",
    ),
    _target(
        "COPPER_PROCESSING_PLUS_DEFENSE",
        E2RArchetype.COPPER_PROCESSING_PLUS_DEFENSE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(20, 17, 16, 12, 12, 9, 7),
        stage1=("copper_processing", "ammo_defense", "mna_rumor", "copper_price_up"),
        stage2=("hanwha_bid_report", "estimated_1_5tn_won_sale_value", "ammo_business_value", "copper_margin"),
        stage3=("actual_sale_contract", "defense_order_backlog", "copper_processing_margin", "op_eps_revision", "fcf"),
        stage4b=("mna_premium_priced", "commodity_defense_hybrid_crowded"),
        stage4c=("hanwha_review_dropped", "poongsan_sale_denial", "event_premium_unwind"),
        green=("actual_sale_contract", "defense_backlog", "processing_margin", "op_eps_revision", "fcf"),
        red=("sale_denial", "mna_review_dropped", "mna_premium_only", "copper_margin_missing"),
        penalties=("mna_event", "confirmation", "processing_margin"),
        note="Poongsan-style copper plus ammunition can be Stage 2, but M&A rumor and structural earnings must be separated.",
    ),
    _target(
        "DEFENSE_AMMO_EVENT_PREMIUM",
        E2RArchetype.DEFENSE_AMMO_EVENT_PREMIUM,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("event", "event", "event", "event", "event", "event", "event"),
        stage1=("ammo_mna_rumor", "defense_unit_sale_report", "buyer_name_reported"),
        stage2=("indicative_bid_reported", "estimated_sale_value"),
        stage3=("not_green_without_final_sale_or_order_backlog",),
        stage4b=("mna_rumor_rally", "premium_before_contract"),
        stage4c=("buyer_drops_review", "seller_denies_sale", "no_transaction"),
        green=(),
        red=("mna_only", "final_contract_missing", "buyer_review_dropped", "seller_denial"),
        penalties=("mna_rumor", "final_terms_missing", "unwind"),
        note="Ammunition M&A rumor is event premium until a final transaction or defense order backlog exists.",
        hard_gate=True,
    ),
    _target(
        "POLYSILICON_NON_CHINA_SUPPLY_OPTION",
        E2RArchetype.POLYSILICON_NON_CHINA_SUPPLY_OPTION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(18, 18, 16, 10, 12, 10, 7),
        stage1=("non_china_polysilicon", "ira_feoc", "spacex_name", "satellite_power", "data_center_power"),
        stage2=("multi_year_supply_talks", "malaysia_polysilicon", "potential_customer", "supply_chain_option"),
        stage3=("confirmed_supply_contract", "contract_amount", "supply_period", "volume", "asp_opm", "revenue_recognition"),
        stage4b=("spacex_name_rally", "ai_data_center_solar_story_crowded"),
        stage4c=("contract_not_confirmed", "company_cannot_confirm", "polysilicon_price_weakness", "solar_oversupply"),
        green=("confirmed_contract", "amount", "period", "volume", "asp_opm", "fcf"),
        red=("media_report_only", "company_confirmation_missing", "contract_terms_missing", "polysilicon_cycle"),
        penalties=("confirmation", "contract_terms", "polysilicon_cycle"),
        note="OCI-style non-China polysilicon is Stage 1/2 option before confirmed customer, volume, ASP, and margin.",
    ),
    _target(
        "POLYSILICON_REPORT_NOT_CONTRACT",
        E2RArchetype.POLYSILICON_REPORT_NOT_CONTRACT,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("cap", "cap", "cap", "cap", "cap", "+", "cap"),
        stage1=("media_report", "talks_reported", "potential_customer"),
        stage2=("detail_check_required",),
        stage3=("not_green_without_confirmed_contract",),
        stage4b=("famous_customer_name_rally",),
        stage4c=("contract_absent", "company_cannot_confirm", "report_fails_to_convert"),
        green=(),
        red=("report_only", "company_confirmation_missing", "contract_absent", "terms_missing"),
        penalties=("report_only", "confirmation", "terms"),
        note="Report-only polysilicon supply talks are capped until the company confirms contract amount, period, and volume.",
        hard_gate=True,
    ),
    _target(
        "STEEL_TARIFF_EVENT_KOREA",
        E2RArchetype.STEEL_TARIFF_EVENT_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(18, 10, 14, 12, 14, 9, 7),
        stage1=("us_china_steel_tariff", "eu_quota_cut", "china_tariff", "steel_event"),
        stage2=("tariff_target_china_only", "korean_steel_relief", "asp_up", "export_volume_stable"),
        stage3=("asp_up_and_volume_stable", "raw_material_labor_cost_control", "opm_fcf_improvement", "op_eps_revision"),
        stage4b=("tariff_event_rally", "steel_basket_broad_rally", "opm_not_confirmed"),
        stage4c=("tariff_hits_korean_exports", "export_volume_down", "price_pass_through_failure"),
        green=("asp", "export_volume", "opm", "fcf", "cost_control"),
        red=("tariff_direction_unclear", "all_import_tariff", "export_exposure_high", "opm_missing"),
        penalties=("tariff_scope", "export_exposure", "cost_control"),
        note="Steel tariff events are directional: China-only tariffs can be a rally, all-import tariffs can be 4C for Korean exporters.",
    ),
    _target(
        "STEEL_EXPORT_TARIFF_4C",
        E2RArchetype.STEEL_EXPORT_TARIFF_4C,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("gate", "gate", "gate", "gate", "gate", "gate", "gate"),
        stage1=("steel_tariff_headline", "export_market_tariff"),
        stage2=("risk_event_detected",),
        stage3=("not_green_while_direct_export_tariff_hits",),
        stage4b=("tariff_relief_rally_without_terms",),
        stage4c=("us_steel_tariff_50pct", "korean_export_competitiveness_hit", "seah_steel_8pct_drop"),
        green=(),
        red=("direct_export_tariff", "export_exposure_high", "local_production_absent", "price_path_down"),
        penalties=("tariff_scope", "export_exposure", "local_production"),
        note="Direct export tariff exposure is a hard RedTeam gate for steel exporters unless local production offsets it.",
        hard_gate=True,
    ),
    _target(
        "SPECIALTY_STEEL_US_LOCALIZATION_OPTION",
        E2RArchetype.SPECIALTY_STEEL_US_LOCALIZATION_OPTION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(18, 17, 13, 10, 12, 9, 7),
        stage1=("octg", "steel_pipe", "us_local_mill", "offshore_wind_foundation", "energy_infrastructure"),
        stage2=("local_us_production", "customer_volume", "tariff_exemption_or_localization", "margin_detail"),
        stage3=("us_local_revenue", "margin_expansion", "export_tariff_offset", "op_eps_revision", "fcf"),
        stage4b=("localization_story_crowded", "tariff_relief_priced_before_margin"),
        stage4c=("local_volume_missing", "tariff_cost_hits", "margin_missing"),
        green=("local_revenue", "margin", "tariff_offset", "op_eps_revision", "fcf"),
        red=("local_volume_missing", "tariff_cost", "margin_missing"),
        penalties=("localization", "margin", "volume"),
        note="Specialty steel localization can be Stage 1/2, but US local volume and margin must prove the offset.",
    ),
    _target(
        "LITHIUM_PRICE_EVENT_KOREA",
        E2RArchetype.LITHIUM_PRICE_EVENT_KOREA,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("event", "event", "event", "event", "event", "event", "event"),
        stage1=("lithium_mine_suspension", "lithium_price_rebound", "spodumene", "brine", "resource_security_story"),
        stage2=("actual_offtake", "production_volume", "government_investment", "plant_operating"),
        stage3=("production_volume", "op_eps_fcf", "long_term_contract", "price_floor", "stage2_price_path"),
        stage4b=("lithium_event_rally", "two_or_three_limit_up_without_earnings", "theme_basket_crowded"),
        stage4c=("lithium_price_redeclines", "cash_burn", "stock_promotion_risk", "cb_bw"),
        green=(),
        red=("price_only_rally", "production_missing", "fcf_missing", "commodity_cycle", "cash_burn"),
        penalties=("event_rally", "production", "fcf", "cash_burn"),
        note="Lithium price events remain Stage 1/4B-watch before real production, offtake, price floor, and FCF.",
        hard_gate=True,
    ),
    _target(
        "RARE_EARTH_THEME_KOREA",
        E2RArchetype.RARE_EARTH_THEME_KOREA,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("event", "event", "event", "event", "event", "event", "event"),
        stage1=("rare_earth_export_control", "magnet", "ferrite", "stainless_specialty", "export_license"),
        stage2=("actual_rare_earth_revenue", "supply_contract", "production_capacity", "customer"),
        stage3=("rare_earth_revenue", "offtake", "op_eps_fcf", "long_term_contract"),
        stage4b=("rare_earth_theme_rally", "price_only_limit_up", "community_keyword_crowded"),
        stage4c=("export_license_recovers", "revenue_absent", "cb_bw", "commodity_price_reversal"),
        green=(),
        red=("theme_only", "actual_revenue_missing", "offtake_missing", "cb_bw", "price_only_rally"),
        penalties=("theme_only", "revenue", "offtake", "dilution"),
        note="Rare-earth Korea themes are Stage 1/4B-watch before actual revenue, offtake, and FCF.",
        hard_gate=True,
    ),
    _target(
        "CHEMICAL_SPREAD_KOREA",
        E2RArchetype.CHEMICAL_SPREAD_KOREA,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights(16, 8, 12, 9, 16, 10, 6),
        stage1=("chemical_spread_rebound", "polysilicon_or_chemical_price", "china_capacity_news"),
        stage2=("spread_margin_signal", "inventory_loss_excluded", "cost_pass_through", "op_revision"),
        stage3=("durable_spread", "volume_stable", "opm_fcf_improvement", "low_cost_position"),
        stage4b=("spread_rebound_priced_before_volume", "chemical_basket_crowded"),
        stage4c=("china_supply_glut", "spread_reworsens", "inventory_loss", "op_eps_revision_down"),
        green=("durable_spread", "volume", "opm", "fcf", "low_cost_position"),
        red=("spread_reworsens", "china_supply_glut", "inventory_loss", "volume_down"),
        penalties=("spread", "inventory", "volume", "china_supply"),
        note="Korea chemical spread recovery is Watch/Red unless spread and volume convert to durable OP/FCF.",
    ),
    _target(
        "EVENT_PREMIUM_GOVERNANCE_OVERLAY",
        E2RArchetype.EVENT_PREMIUM_GOVERNANCE_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("gate", "gate", "gate", "gate", "gate", "gate", "gate"),
        stage1=("mna_rumor", "governance_event", "tender_or_sale_report"),
        stage2=("indicative_offer", "buyer_named", "estimated_value_reported"),
        stage3=("not_green_without_final_terms_and_fcf_link",),
        stage4b=("event_premium_rally", "rumor_priced_before_terms"),
        stage4c=("deal_dropped", "seller_denial", "terms_absent"),
        green=(),
        red=("event_only", "final_terms_missing", "deal_dropped", "seller_denial"),
        penalties=("event_premium", "final_terms", "unwind"),
        note="Governance/M&A event premium is separated from structural rerating.",
        hard_gate=True,
    ),
    _target(
        "DISCLOSURE_CONFIDENCE_CAP",
        E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("cap", "cap", "cap", "cap", "cap", "+", "cap"),
        stage1=("headline_disclosure", "opendart_list_only", "media_report_only"),
        stage2=("detail_fetch_required", "counterparty", "amount", "period", "volume", "price_floor"),
        stage3=("multi_source_confirmation", "terms_verified", "opm_fcf_visible"),
        stage4b=("headline_theme_rally",),
        stage4c=("customer_missing", "amount_missing", "period_missing", "margin_unknown", "company_denial"),
        green=("counterparty", "amount", "period", "offtake_volume", "price_floor", "opm_fcf"),
        red=("detail_missing", "company_confirmation_missing", "terms_missing", "margin_unknown"),
        penalties=("disclosure_detail", "confirmation", "terms"),
        note="Commodity/material contract headlines cannot support Stage 3-Green until terms and earnings conversion are verified.",
    ),
)


ROUND175_CASE_CANDIDATES: tuple[Round175CaseCandidate, ...] = (
    Round175CaseCandidate(
        "copper_ai_grid_korea_basket_stage2_cap_case",
        "COPPER_AI_GRID_KOREA",
        "LS/001440/000500/103590",
        "LS / Daehan Cable / Gaon Cable / Poongsan copper-grid basket",
        "KR",
        "success_candidate",
        date(2025, 12, 12),
        date(2025, 12, 12),
        None,
        None,
        None,
        ("copper_up_35pct", "copper_11952_usd_per_ton", "ai_data_center_demand", "power_grid_demand", "mine_disruption", "individual_order_backfill_needed"),
        ("individual_order_missing", "opm_missing", "fcf_missing", "commodity_cycle_risk", "price_only_rally_risk"),
        "macro_bottleneck_stage1_2_individual_stage3_cap",
        "needs_krx_price_and_revision_backfill",
        ("round_175.md Reuters copper tight supply and AI demand",),
        "Copper AI-grid is a real macro bottleneck, but Korean individual wires/processors need order backlog, pass-through, OPM, and FCF before Stage 3.",
        (E2RArchetype.COPPER_AI_GRID_STRUCTURAL_DEMAND,),
    ),
    Round175CaseCandidate(
        "poongsan_copper_defense_mna_unwind_case",
        "COPPER_PROCESSING_PLUS_DEFENSE",
        "103140",
        "Poongsan copper processing plus defense event",
        "KR",
        "4c_thesis_break",
        date(2026, 4, 3),
        date(2026, 4, 3),
        None,
        None,
        date(2026, 4, 9),
        ("copper_products", "ammunition_business", "hanwha_bid_report", "estimated_1_5tn_won_sale_value", "mna_premium"),
        ("hanwha_review_dropped", "poongsan_sale_denial", "final_sale_missing", "event_premium_unwind"),
        "stage2_event_then_4c_unwind",
        "needs_price_backfill",
        ("round_175.md Reuters Hanwha Poongsan ammunition business report", "round_175.md Reuters Hanwha drops plan and Poongsan denies sale"),
        "Poongsan is the clean R4 training case: copper plus ammo can reach Stage 2, but M&A rumor must unwind when review is dropped and sale is denied.",
        (E2RArchetype.DEFENSE_AMMO_EVENT_PREMIUM, E2RArchetype.EVENT_PREMIUM_GOVERNANCE_OVERLAY),
    ),
    Round175CaseCandidate(
        "oci_holdings_spacex_polysilicon_report_cap_case",
        "POLYSILICON_NON_CHINA_SUPPLY_OPTION",
        "010060",
        "OCI Holdings non-China polysilicon / SpaceX talks",
        "KR",
        "event_premium",
        date(2026, 4, 14),
        None,
        None,
        None,
        None,
        ("oci_terrasus_malaysia_polysilicon", "spacex_supply_talks_reported", "non_china_polysilicon", "ira_subsidy_qualification_option", "media_report_only"),
        ("company_confirmation_missing", "contract_amount_missing", "supply_period_missing", "volume_missing", "polysilicon_cycle_risk"),
        "report_not_contract_cap",
        "needs_price_backfill",
        ("round_175.md Reuters OCI TerraSus SpaceX polysilicon talks",),
        "OCI non-China polysilicon can route research, but SpaceX talks are not Stage 3 without confirmed amount, period, volume, ASP, and OPM.",
        (E2RArchetype.POLYSILICON_REPORT_NOT_CONTRACT, E2RArchetype.DISCLOSURE_CONFIDENCE_CAP),
    ),
    Round175CaseCandidate(
        "steel_tariff_directionality_korea_case",
        "STEEL_TARIFF_EVENT_KOREA",
        "005490/004020/016380",
        "POSCO Holdings / Hyundai Steel / KG Steel tariff directionality",
        "KR",
        "event_premium",
        date(2024, 4, 17),
        None,
        None,
        None,
        None,
        ("china_steel_tariff_event", "posco_intraday_6_5pct", "hyundai_steel_intraday_6_0pct", "kg_steel_intraday_8_9pct", "tariff_direction_matters"),
        ("all_import_tariff_can_reverse", "export_exposure", "opm_missing", "volume_missing", "event_only"),
        "tariff_directionality_required",
        "needs_exact_stage_date_backfill",
        ("round_175.md WSJ Biden Chinese steel tariff event", "round_175.md Reuters Trump import steel tariff event"),
        "Steel tariff scoring must split China-only tariffs from all-import tariffs. Directionality is the evidence, not the word tariff.",
        (E2RArchetype.EVENT_PREMIUM_GOVERNANCE_OVERLAY,),
    ),
    Round175CaseCandidate(
        "seah_steel_export_tariff_4c_case",
        "STEEL_EXPORT_TARIFF_4C",
        "306200/003030",
        "SeAH Steel export tariff shock",
        "KR",
        "4c_thesis_break",
        date(2025, 6, 2),
        None,
        None,
        None,
        date(2025, 6, 2),
        ("us_steel_aluminum_tariff_50pct", "korea_major_steel_exporter", "seah_steel_price_drop_8pct", "direct_export_tariff_hit"),
        ("direct_export_tariff", "us_export_exposure", "local_production_absent_or_unproven", "price_path_down"),
        "direct_tariff_4c_price_path_aligned",
        "needs_exact_stage_date_backfill",
        ("round_175.md Reuters US 50pct steel tariff and Korea steel share drop",),
        "SeAH Steel is the clean price-path 4C check: a direct tariff hit matters more than generic steel price upside.",
        (E2RArchetype.STEEL_TARIFF_EVENT_KOREA,),
    ),
    Round175CaseCandidate(
        "specialty_steel_us_localization_option_case",
        "SPECIALTY_STEEL_US_LOCALIZATION_OPTION",
        "003030/058650",
        "SeAH specialty steel US localization option",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("steel_pipe", "octg", "seah_steel_usa", "offshore_wind_foundation", "us_localization_option", "energy_infrastructure"),
        ("local_volume_missing", "margin_missing", "tariff_offset_unproven", "op_eps_missing"),
        "localization_watch_until_volume_margin",
        "needs_case_backfill",
        ("round_175.md specialty steel localization watch",),
        "US localization can reduce tariff risk, but Stage 3 needs local revenue, margin, OP/EPS, and FCF.",
        (E2RArchetype.STEEL_EXPORT_TARIFF_4C,),
    ),
    Round175CaseCandidate(
        "lithium_rare_earth_price_only_theme_case",
        "LITHIUM_PRICE_EVENT_KOREA",
        "005490/001570/101670/047400/081150",
        "POSCO Holdings / Kumyang / Hydro Lithium / Union Materials / Tplex price-only themes",
        "KR",
        "event_premium",
        None,
        None,
        None,
        None,
        None,
        ("lithium_price_rebound", "rare_earth_export_control", "resource_security_narrative", "theme_basket_rally"),
        ("actual_offtake_missing", "production_volume_missing", "op_eps_fcf_missing", "cb_bw_risk", "price_only_rally"),
        "price_only_commodity_theme_cap",
        "needs_case_backfill",
        ("round_175.md lithium and rare earth Korea theme cap",),
        "Lithium and rare-earth Korea themes stay Stage 1/4B-watch before actual offtake, production, revenue, and FCF.",
        (E2RArchetype.RARE_EARTH_THEME_KOREA, E2RArchetype.COMMODITY_PRICE_4C_OVERLAY),
    ),
    Round175CaseCandidate(
        "rare_earth_theme_korea_stage1_case",
        "RARE_EARTH_THEME_KOREA",
        "047400/081150/037370",
        "Union Materials / Tplex / EG rare-earth theme",
        "KR",
        "overheat",
        None,
        None,
        None,
        None,
        None,
        ("rare_earth_export_control", "magnet_ferrite_stainless_specialty_keywords", "event_rally_possible"),
        ("actual_rare_earth_revenue_missing", "supply_contract_missing", "offtake_missing", "price_only_theme"),
        "rare_earth_theme_watch_red_until_revenue",
        "needs_case_backfill",
        ("round_175.md rare-earth Korea theme note",),
        "Rare-earth keyword exposure can route research but cannot become Stage 3 without revenue, offtake, and FCF.",
        (E2RArchetype.EVENT_PREMIUM_GOVERNANCE_OVERLAY,),
    ),
    Round175CaseCandidate(
        "chemical_spread_korea_watch_red_case",
        "CHEMICAL_SPREAD_KOREA",
        "004000/009830/010060",
        "Lotte Fine Chemical / Hanwha Solutions / OCI chemical spread watch",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("chemical_spread_signal", "polysilicon_or_chemical_price", "volume_margin_backfill_needed"),
        ("china_capacity_risk", "spread_reworsens", "inventory_loss_risk", "volume_missing", "op_revision_missing"),
        "chemical_spread_watch_red_until_durable_margin",
        "needs_case_backfill",
        ("round_175.md chemical spread Korea watch note",),
        "Chemical spread recovery must show durable spread, volume, OPM, and FCF before Stage 3.",
        (E2RArchetype.CHEMICAL_SPREAD,),
    ),
    Round175CaseCandidate(
        "disclosure_confidence_materials_cap_case",
        "DISCLOSURE_CONFIDENCE_CAP",
        "KR_MATERIALS_BASKET",
        "Korea materials disclosure confidence cap",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("headline_contract_or_media_report", "detail_fetch_required", "counterparty_amount_period_volume_price_floor_required"),
        ("detail_missing", "company_confirmation_missing", "terms_missing", "margin_unknown", "stage_prices_missing"),
        "detail_missing_cap",
        "not_price_applicable",
        ("round_175.md disclosure confidence cap",),
        "OpenDART list or media headline is not enough; missing counterparty, amount, period, volume, price floor, or margin caps Stage 3.",
    ),
)


ROUND175_SCORE_STAGE_PRICE_ALIGNMENT: tuple[Round175ScoreStagePriceAlignment, ...] = (
    Round175ScoreStagePriceAlignment("copper_ai_grid_korea_basket_stage2_cap_case", "Stage 1/2", "Copper macro price path strong; Korean individual KRX/revision path needs backfill", "macro_bottleneck_not_company_green", "credit copper AI-grid bottleneck; cap before individual order backlog, OPM, and FCF"),
    Round175ScoreStagePriceAlignment("poongsan_copper_defense_mna_unwind_case", "Stage 2 -> 4C-watch", "M&A premium should unwind after Hanwha review drop and Poongsan sale denial", "event_unwind_alignment", "remove M&A premium; retain copper/defense only if OP/EPS evidence exists"),
    Round175ScoreStagePriceAlignment("oci_holdings_spacex_polysilicon_report_cap_case", "Stage 1/2 option", "SpaceX talks can move price but remain media-only before confirmation", "report_not_contract_cap", "support research routing; block Stage 3 before confirmed terms"),
    Round175ScoreStagePriceAlignment("steel_tariff_directionality_korea_case", "Stage 1 event", "China-only tariff can lift Korean steel while all-import tariff can hurt it", "directionality_required", "score tariff target and export exposure before stage upgrade"),
    Round175ScoreStagePriceAlignment("seah_steel_export_tariff_4c_case", "4C-watch", "US 50% steel tariff and -8% price reaction are aligned hard risk", "direct_tariff_4c_alignment", "apply export exposure and local-production offset gates"),
    Round175ScoreStagePriceAlignment("specialty_steel_us_localization_option_case", "Stage 1/2 option", "Localization can offset tariff but needs volume and margin", "localization_not_green_yet", "cap before local revenue, margin, and FCF"),
    Round175ScoreStagePriceAlignment("lithium_rare_earth_price_only_theme_case", "Stage 1 / 4B-watch", "Lithium/rare-earth event rally is price-only without production and FCF", "event_rally_not_structural", "credit event only lightly; block Green without offtake and earnings"),
    Round175ScoreStagePriceAlignment("rare_earth_theme_korea_stage1_case", "Stage 1 / overheat watch", "Rare-earth keyword basket can rally without revenue", "theme_only_contained", "cap before actual rare-earth revenue and supply contract"),
    Round175ScoreStagePriceAlignment("chemical_spread_korea_watch_red_case", "Watch/Red", "Spread can reverse before volume and FCF stabilize", "spread_durability_required", "require durable spread, volume, and OPM/FCF"),
    Round175ScoreStagePriceAlignment("disclosure_confidence_materials_cap_case", "cap", "Missing counterparty/amount/period/volume/margin keeps Stage capped", "detail_cap_correct", "fetch and parse detail before considering Stage 3"),
)


ROUND175_PRICE_FIELDS: tuple[str, ...] = (
    "ticker",
    "symbol",
    "company_name",
    "primary_archetype",
    "secondary_archetypes",
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
    "stage1_price",
    "stage2_price",
    "stage3_price",
    "stage4b_price",
    "stage4c_price",
    "return_1d_after_event",
    "return_5d_after_event",
    "return_20d_after_stage2",
    "return_60d_after_stage2",
    "return_120d_after_stage2",
    "return_252d_after_stage2",
    "mfe_20d_after_stage2",
    "mae_20d_after_stage2",
    "mfe_60d_after_stage2",
    "mae_60d_after_stage2",
    "mfe_120d_after_stage2",
    "mae_120d_after_stage2",
    "relative_strength_vs_kospi",
    "relative_strength_vs_sector",
    "relative_strength_vs_commodity_price",
    "commodity_price_at_stage",
    "commodity_price_change_20d",
    "commodity_price_change_60d",
    "op_revision_before_stage3",
    "op_revision_after_stage3",
    "eps_revision_before_stage3",
    "eps_revision_after_stage3",
    "contract_amount",
    "contract_counterparty",
    "contract_period",
    "offtake_volume",
    "price_floor_flag",
    "media_report_only_flag",
    "company_confirmation_flag",
    "tariff_target",
    "tariff_scope",
    "export_exposure_to_tariff_market",
    "local_production_flag",
    "inventory_loss_flag",
    "spread_margin_signal",
    "raw_material_cost_signal",
    "copper_price_at_stage",
    "copper_passthrough_flag",
    "mna_bid_value",
    "mna_review_dropped_flag",
    "seller_denial_flag",
    "polysilicon_price_signal",
    "rare_earth_revenue_flag",
    "lithium_production_volume",
    "cb_bw_or_equity_raise_flag",
    "disclosure_confidence",
    "opendart_rcept_no",
    "opendart_detail_fetched_flag",
    "detail_parser_confidence",
    "valuation_at_stage3",
    "valuation_at_stage4b",
    "stage_before_redteam",
    "stage_after_redteam",
    "score_before_redteam",
    "score_after_redteam",
    "score_price_alignment",
    "price_validation_status",
    "review_notes",
)


def round175_target_for(target_id: str) -> Round175ScoreTarget | None:
    for target in ROUND175_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round175_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND175_CASE_CANDIDATES:
        target = round175_target_for(candidate.target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {candidate.target_id}")
        weights = target.score_weight.as_dict()
        stage4b_evidence = candidate.evidence_fields if candidate.case_type in {"4b_watch", "overheat"} or candidate.stage4b_date else ()
        stage4c_evidence = candidate.red_flag_fields if candidate.case_type == "4c_thesis_break" or candidate.stage4c_date or target.hard_gate else ()
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
                f"Round175 R4 Loop-11 Korea materials/spread/strategic resource case for {candidate.target_id}; "
                "calibration-only and focused on commodity event caps, contract/offtake proof, tariff directionality, and 4B/4C cooling."
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
            score_price_alignment=_round175_score_price_alignment(candidate),
            rerating_result=_round175_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
            score_weight_hint={
                "eps_fcf": _numeric_weight(weights["eps_fcf_opm"]),
                "visibility": _numeric_weight(weights["contract_offtake_customer_visibility"]),
                "bottleneck_pricing": _numeric_weight(weights["bottleneck_pricing"]),
                "early_price_validation": _numeric_weight(weights["early_price_validation"]),
                "cycle_spread_durability": _numeric_weight(weights["cycle_spread_durability"]),
                "disclosure_redteam": _numeric_weight(weights["disclosure_redteam"]),
                "valuation_4b_room": _numeric_weight(weights["valuation_4b_room"]),
            },
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "commodity_price_is_not_structural_evidence",
                "require_contract_offtake_price_floor_volume_opm_fcf_for_green",
                "stage3_early_catch_requires_4_of_7_loop11_conditions",
                "stage4b_cooling_requires_3_of_5_loop11_conditions",
                "do_not_invent_contract_amount_counterparty_period_offtake_price_floor_tariff_scope_stage_prices_or_mfe_mae",
                "media_report_tariff_lithium_rare_earth_mna_rumor_and_commodity_event_do_not_create_green",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=False,
                price_data_available=False,
                stage_dates_confidence=0.75
                if candidate.stage1_date or candidate.stage2_date or candidate.stage3_date or candidate.stage4b_date or candidate.stage4c_date
                else 0.2,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round175_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND175_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "eps_fcf_opm": str(weights["eps_fcf_opm"]),
                "contract_offtake_customer_visibility": str(weights["contract_offtake_customer_visibility"]),
                "bottleneck_pricing": str(weights["bottleneck_pricing"]),
                "early_price_validation": str(weights["early_price_validation"]),
                "cycle_spread_durability": str(weights["cycle_spread_durability"]),
                "disclosure_redteam": str(weights["disclosure_redteam"]),
                "valuation_4b_room": str(weights["valuation_4b_room"]),
                "stage1_signals": "|".join(target.stage1_signals),
                "stage2_signals": "|".join(target.stage2_signals),
                "stage3_conditions": "|".join(target.stage3_conditions),
                "stage4b_conditions": "|".join(target.stage4b_conditions),
                "stage4c_conditions": "|".join(target.stage4c_conditions),
                "green_conditions": "|".join(target.green_conditions),
                "red_flags": "|".join(target.red_flags),
                "loop11_penalty_axes": "|".join(target.loop11_penalty_axes),
                "hard_gate": str(target.hard_gate).lower(),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round175_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND175_CASE_CANDIDATES:
        target = round175_target_for(candidate.target_id)
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


def round175_stage_date_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "target_id": target.target_id,
            "stage1": "|".join(target.stage1_signals),
            "stage2": "|".join(target.stage2_signals),
            "stage3": "|".join(target.stage3_conditions),
            "stage4b": "|".join(target.stage4b_conditions),
            "stage4c": "|".join(target.stage4c_conditions),
            "loop11_penalty_axes": "|".join(target.loop11_penalty_axes),
            "hard_gate": str(target.hard_gate).lower(),
            "production_scoring_changed": "false",
        }
        for target in ROUND175_SCORE_TARGETS
    )


def round175_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round175_backfill": "true"} for field in ROUND175_PRICE_FIELDS)


def round175_base_score_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(weight.as_row() for weight in ROUND175_BASE_SCORE_WEIGHTS)


def round175_stage_cap_rows() -> tuple[dict[str, str], ...]:
    return tuple(cap.as_row() for cap in ROUND175_STAGE_CAPS)


def round175_score_stage_price_alignment_rows() -> tuple[dict[str, str], ...]:
    return tuple(row.as_row() for row in ROUND175_SCORE_STAGE_PRICE_ALIGNMENT)


def round175_summary() -> dict[str, int | bool]:
    records = round175_case_records()
    return {
        "target_count": len(ROUND175_SCORE_TARGETS),
        "source_canonical_target_count": ROUND175_SOURCE_CANONICAL_TARGET_COUNT,
        "case_candidate_count": len(records),
        "base_score_component_count": len(ROUND175_BASE_SCORE_WEIGHTS),
        "stage_cap_count": len(ROUND175_STAGE_CAPS),
        "score_stage_price_alignment_count": len(ROUND175_SCORE_STAGE_PRICE_ALIGNMENT),
        "structural_success_count": sum(1 for record in records if record.case_type == "structural_success"),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "overheat_count": sum(1 for record in records if record.case_type == "overheat"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND175_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND175_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND175_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "hard_gate_target_count": sum(1 for target in ROUND175_SCORE_TARGETS if target.hard_gate),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round175_r4_loop11_reports(
    *,
    output_directory: str | Path = ROUND175_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND175_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND175_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round175_r4_loop11_materials_spread_strategic_summary.md",
        "case_matrix": output / "round175_r4_loop11_case_matrix.csv",
        "stage_date_plan": output / "round175_r4_loop11_stage_date_plan.csv",
        "green_guardrails": output / "round175_r4_loop11_green_guardrails.md",
        "risk_overlays": output / "round175_r4_loop11_risk_overlays.md",
        "price_validation_plan": output / "round175_r4_loop11_price_validation_plan.md",
        "price_fields": output / "round175_r4_loop11_price_fields.csv",
        "base_score_weights": output / "round175_r4_loop11_base_score_weights.csv",
        "stage_caps": output / "round175_r4_loop11_stage_caps.csv",
        "score_stage_price_alignment": output / "round175_r4_loop11_score_stage_price_alignment.csv",
        "score_stage_price_alignment_md": output / "round175_r4_loop11_score_stage_price_alignment.md",
    }
    _write_case_jsonl(round175_case_records(), cases)
    _write_rows(round175_score_profile_rows(), score_profiles)
    _write_rows(round175_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round175_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round175_price_field_rows(), paths["price_fields"])
    _write_rows(round175_base_score_weight_rows(), paths["base_score_weights"])
    _write_rows(round175_stage_cap_rows(), paths["stage_caps"])
    _write_rows(round175_score_stage_price_alignment_rows(), paths["score_stage_price_alignment"])
    paths["summary"].write_text(render_round175_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round175_green_guardrail_markdown(), encoding="utf-8")
    paths["risk_overlays"].write_text(render_round175_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round175_price_validation_plan_markdown(), encoding="utf-8")
    paths["score_stage_price_alignment_md"].write_text(render_round175_score_stage_price_alignment_markdown(), encoding="utf-8")
    return paths


def render_round175_summary_markdown() -> str:
    summary = round175_summary()
    lines = [
        "# Round-175 R4 Loop-11 Korea Materials / Spreads / Strategic Resources Summary",
        "",
        f"- source_round: `{ROUND175_SOURCE_ROUND_PATH}`",
        "- large_sector: `MATERIALS_SPREAD_STRATEGIC`",
        "- loop: `R4 Loop 11 / v11.0`",
        f"- target_count: {summary['target_count']}",
        f"- source_canonical_target_count: {summary['source_canonical_target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- base_score_component_count: {summary['base_score_component_count']}",
        f"- stage_cap_count: {summary['stage_cap_count']}",
        f"- score_stage_price_alignment_count: {summary['score_stage_price_alignment_count']}",
        f"- structural_success_count: {summary['structural_success_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- overheat_count: {summary['overheat_count']}",
        f"- failed_rerating_count: {summary['failed_rerating_count']}",
        f"- stage4c_case_count: {summary['stage4c_case_count']}",
        f"- green_possible_count: {summary['green_possible_count']}",
        f"- watch_yellow_first_count: {summary['watch_yellow_first_count']}",
        f"- redteam_first_count: {summary['redteam_first_count']}",
        f"- hard_gate_target_count: {summary['hard_gate_target_count']}",
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "",
        "- R4 Loop 11 is Korea-first and treats copper, steel, lithium, rare earth, and polysilicon moves as event/cycle evidence before company-level proof.",
        "- Stage 3-Green remains strict. Commodity price, tariff, export-control, SpaceX, or M&A rumor keywords do not create Green by themselves.",
        "- The base score weights are EPS/FCF/OPM 22, contract/offtake/customer visibility 20, bottleneck/pricing 16, early price path 12, cycle/spread durability 12, disclosure/RedTeam 10, valuation/4B room 8.",
        "- Example: copper AI-grid demand can be Stage 1/2 macro evidence, but LS/Daehan/Gaon/Poongsan need individual orders, pass-through, OPM, and FCF.",
        "- Example: Poongsan can be Stage 2 on copper plus ammunition/M&A value, then 4C-watch when Hanwha drops review and Poongsan denies sale.",
        "- Example: OCI Holdings SpaceX polysilicon talks remain report-not-contract until company confirmation and supply terms appear.",
        "- Example: steel tariff scoring must split China-only tariff from all-import tariff. The same word can mean opposite price paths.",
    ]
    return "\n".join(lines) + "\n"


def render_round175_green_guardrail_markdown() -> str:
    lines = [
        "# Round-175 R4 Loop-11 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Loop-11 penalties |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND175_SCORE_TARGETS:
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
            "- Do not apply R4 Loop-11 v11.0 weights to production scoring yet.",
            "- Do not lower Stage 3-Green thresholds because a commodity or steel basket moved.",
            "- Do not use Round 175 case records as candidate-generation input.",
            "- Do not treat copper price, steel tariff, rare-earth export control, lithium rebound, non-China polysilicon, M&A rumor, or SpaceX name as Green by itself.",
            "- Do not invent contract amount, counterparty, period, offtake volume, price floor, tariff scope, stage prices, MFE/MAE, OPM, FCF, or commodity price exposure.",
            "- Apply 4B-watch when commodity, tariff, export-control, or M&A event rallies outrun OP/EPS revision.",
            "- Apply 4C/hard review for M&A review dropped, sale denial, media-only contract, direct export tariff, spread reversal, inventory loss, OP/EPS downgrade, CB/BW, or production/export volume decline.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round175_risk_overlay_markdown() -> str:
    lines = [
        "# Round-175 R4 Loop-11 Risk Overlays",
        "",
        "- `COPPER_MACRO_NOT_COMPANY_GREEN`: copper AI-grid shortage is Stage 1/2 macro evidence before company order/OPM/FCF proof.",
        "- `POONGSAN_MNA_UNWIND_4C`: M&A premium must be removed when buyer review is dropped and seller denies sale.",
        "- `POLYSILICON_REPORT_CAP`: SpaceX or non-China supply story is capped before confirmed contract terms.",
        "- `STEEL_TARIFF_DIRECTIONALITY`: China-only tariff and all-import tariff can point in opposite directions.",
        "- `DIRECT_EXPORT_TARIFF_4C`: Korean steel exporters with direct US tariff exposure require hard RedTeam.",
        "- `LITHIUM_RARE_EARTH_PRICE_ONLY_CAP`: mineral or export-control event without revenue, offtake, production, and FCF remains Stage 1/4B-watch.",
        "- `CHEMICAL_SPREAD_DURABILITY`: spread rebound needs volume, cost pass-through, OPM, and FCF durability.",
        "- `DISCLOSURE_CONFIDENCE_CAPPED`: media or OpenDART list headlines are capped until counterparty, amount, period, volume, price floor, and margin are parsed.",
        "",
        "Simple example: if `as_of_date=2026-04-14`, OCI's SpaceX talks can be research input. It cannot become Stage 3-Green unless a confirmed contract and terms were available by that date.",
    ]
    return "\n".join(lines) + "\n"


def render_round175_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-175 R4 Loop-11 Price Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign Stage 1/2/3/4B/4C dates from dated source evidence only.",
        "2. Backfill KRX daily bars for `price_at_stage1` through `price_at_stage4c`.",
        "3. Calculate 1D/5D event returns plus 20D/60D/120D/252D returns and MFE/MAE after Stage 2.",
        "4. Compare price speed against OP/EPS revision, commodity price, spread, export volume, and tariff scope.",
        "5. Separate company-level Stage 2 proof from event-led 4B-watch and direct-risk 4C-watch.",
        "6. Keep media-only, company-unconfirmed, export-tariff, M&A unwind, commodity-cycle, and disclosure-detail caps explicit.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | target | stage marker | check |",
        "| --- | --- | --- | --- |",
    ]
    for row in round175_case_candidate_rows():
        stage_date = row["stage4c_date"] or row["stage4b_date"] or row["stage3_date"] or row["stage2_date"] or row["stage1_date"] or "undated"
        lines.append(f"| `{row['case_id']}` | `{row['target_id']}` | {stage_date} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `macro_bottleneck_not_company_green`: commodity macro signal exists, but individual company proof is missing.",
            "- `event_unwind_alignment`: an event premium should reverse when the event fails.",
            "- `report_not_contract_cap`: famous customer name or media report is not a contract.",
            "- `directionality_required`: tariff target and scope must be parsed before scoring.",
            "- `direct_tariff_4c_alignment`: price-path downside matches a hard export tariff risk.",
            "- `event_rally_not_structural`: lithium/rare-earth/commodity price event is not structural evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round175_score_stage_price_alignment_markdown() -> str:
    lines = [
        "# Round-175 R4 Loop-11 Score -> Stage -> Price Alignment",
        "",
        "## Base Score Weights",
        "",
        "| component | points | direction | reason |",
        "| --- | ---: | --- | --- |",
    ]
    for row in ROUND175_BASE_SCORE_WEIGHTS:
        lines.append(f"| `{row.component}` | {row.points} | {row.loop11_direction} | {row.reason} |")
    lines.extend(
        [
            "",
            "## Stage Caps",
            "",
            "| stage band | max score | evidence | examples | Green policy |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for cap in ROUND175_STAGE_CAPS:
        lines.append(
            f"| `{cap.stage_band}` | {cap.max_score} | {', '.join(cap.required_evidence)} | "
            f"{', '.join(cap.example_cases)} | {cap.green_policy} |"
        )
    lines.extend(
        [
            "",
            "## Alignment Cases",
            "",
            "| case | detected stage | price-path status | verdict | adjustment |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in ROUND175_SCORE_STAGE_PRICE_ALIGNMENT:
        lines.append(
            f"| `{row.case_id}` | {row.detected_stage} | {row.price_path_status} | "
            f"{row.verdict} | {row.normalization_adjustment} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Copper AI-grid is the strongest macro bottleneck test, but individual Korean names need company-level conversion.",
            "- Poongsan is the clean event-unwind case: copper-defense structure and M&A premium must be split.",
            "- OCI Holdings is the clean report-not-contract case: SpaceX talks remain capped before confirmation.",
            "- Korean steel tariff cases force directionality parsing: China-only tariff and all-import tariff are not the same signal.",
            "- Lithium and rare-earth themes remain price-only until offtake, production, revenue, and FCF are proven.",
        ]
    )
    return "\n".join(lines) + "\n"


def _round175_score_price_alignment(candidate: Round175CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "aligned"
    if candidate.case_type == "success_candidate":
        return "unknown"
    if candidate.case_type in {"event_premium", "overheat", "4b_watch"}:
        return "price_moved_without_evidence"
    if candidate.case_type in {"4c_thesis_break", "failed_rerating"}:
        return "false_positive_score"
    return "unknown"


def _round175_rerating_result(candidate: Round175CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "true_rerating"
    if candidate.case_type == "4b_watch" or candidate.case_type == "overheat":
        return "theme_overheat"
    if candidate.case_type == "event_premium":
        return "event_premium"
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    if candidate.case_type == "failed_rerating":
        return "no_rerating"
    return "unknown"


def _numeric_weight(value: int | str) -> float:
    if isinstance(value, int):
        return float(value)
    if value in {"gate", "cap", "+", "event"}:
        return 0.0
    return float(value)


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
        for row in rows_tuple:
            writer.writerow(dict(row))
    return path


__all__ = [
    "ROUND175_BASE_SCORE_WEIGHTS",
    "ROUND175_CASE_CANDIDATES",
    "ROUND175_DEFAULT_CASES_PATH",
    "ROUND175_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND175_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND175_PRICE_FIELDS",
    "ROUND175_SCORE_STAGE_PRICE_ALIGNMENT",
    "ROUND175_SCORE_TARGETS",
    "ROUND175_SOURCE_CANONICAL_TARGET_COUNT",
    "ROUND175_SOURCE_CANONICAL_TARGET_IDS",
    "ROUND175_STAGE_CAPS",
    "Round175BaseScoreWeight",
    "Round175CaseCandidate",
    "Round175ScoreStagePriceAlignment",
    "Round175ScoreTarget",
    "Round175ScoreWeightDraft",
    "Round175StageCap",
    "render_round175_green_guardrail_markdown",
    "render_round175_price_validation_plan_markdown",
    "render_round175_risk_overlay_markdown",
    "render_round175_score_stage_price_alignment_markdown",
    "render_round175_summary_markdown",
    "round175_base_score_weight_rows",
    "round175_case_candidate_rows",
    "round175_case_records",
    "round175_price_field_rows",
    "round175_score_profile_rows",
    "round175_score_stage_price_alignment_rows",
    "round175_stage_cap_rows",
    "round175_stage_date_rows",
    "round175_summary",
    "round175_target_for",
    "write_round175_r4_loop11_reports",
]
