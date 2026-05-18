"""Round-188 R4 Loop-12 Korea materials/spread/strategic-resources pack.

Round 188 tightens R4 around Korea refining, petrochemical restructuring,
NCC capacity cuts, Shaheen oversupply risk, synthetic-rubber tariff risk,
and tire/rubber production disruption. It is calibration/report material
only. Production feature engineering, scoring, staging, and RedTeam code must
not import this module.
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


ROUND188_SOURCE_ROUND_PATH = "docs/round/round_188.md"
ROUND188_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round188_r4_loop12_materials_spread_strategic"
ROUND188_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r4_loop12_round188.jsonl"
ROUND188_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round188_r4_loop12_v12.csv"
ROUND188_SOURCE_CANONICAL_TARGET_IDS: tuple[str, ...] = (
    "REFINING_SPREAD_TURNAROUND_KOREA",
    "REFINING_PETCHEM_MIX_DRAG",
    "PETROCHEMICAL_RESTRUCTURING_KOREA",
    "NCC_CAPACITY_CUT_STAGE2",
    "NCC_OVERLOAD_SHAHEEN_RISK",
    "SPECIALTY_CHEM_GOVERNANCE_RESTRUCTURING",
    "SYNTHETIC_RUBBER_TARIFF_RISK",
    "TIRE_RUBBER_PRODUCTION_DISRUPTION",
    "COMMODITY_SPREAD_CYCLE_NOT_STRUCTURAL",
    "DISCLOSURE_CONFIDENCE_CAP",
)
ROUND188_SOURCE_CANONICAL_TARGET_COUNT = len(ROUND188_SOURCE_CANONICAL_TARGET_IDS)


@dataclass(frozen=True)
class Round188ScoreWeightDraft:
    eps_fcf_opm: int | str
    spread_product_margin_durability: int | str
    restructuring_supply_cut_visibility: int | str
    early_price_validation: int | str
    cycle_commodity_risk: int | str
    operational_tariff_disclosure_redteam: int | str
    valuation_4b_room: int | str

    def as_dict(self) -> dict[str, int | str]:
        return {
            "eps_fcf_opm": self.eps_fcf_opm,
            "spread_product_margin_durability": self.spread_product_margin_durability,
            "restructuring_supply_cut_visibility": self.restructuring_supply_cut_visibility,
            "early_price_validation": self.early_price_validation,
            "cycle_commodity_risk": self.cycle_commodity_risk,
            "operational_tariff_disclosure_redteam": self.operational_tariff_disclosure_redteam,
            "valuation_4b_room": self.valuation_4b_room,
        }


@dataclass(frozen=True)
class Round188ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round188ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    loop12_penalty_axes: tuple[str, ...]
    normalization_point: str
    hard_gate: bool = False

    @property
    def large_sector(self) -> Round10LargeSector:
        return Round10LargeSector.MATERIALS_SPREAD_STRATEGIC

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round188CaseCandidate:
    case_id: str
    target_id: str
    symbol: str
    company_name: str
    market: str
    case_type: str
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
class Round188BaseScoreWeight:
    component: str
    points: int
    loop12_direction: str
    reason: str

    def as_row(self) -> dict[str, str]:
        return {
            "component": self.component,
            "points": str(self.points),
            "loop12_direction": self.loop12_direction,
            "reason": self.reason,
            "production_scoring_changed": "false",
        }


@dataclass(frozen=True)
class Round188StageCap:
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
            "production_scoring_changed": "false",
        }


@dataclass(frozen=True)
class Round188ScoreStagePriceAlignment:
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
            "production_scoring_changed": "false",
        }


def _w(
    eps: int | str,
    spread: int | str,
    restructuring: int | str,
    price: int | str,
    cycle: int | str,
    redteam: int | str,
    valuation: int | str,
) -> Round188ScoreWeightDraft:
    return Round188ScoreWeightDraft(eps, spread, restructuring, price, cycle, redteam, valuation)


CAP_WEIGHT = _w("cap", "cap", "cap", "cap", "cap", "cap", "+")
GATE_WEIGHT = _w("gate", "gate", "gate", "gate", "gate", "gate", "gate")


ROUND188_BASE_SCORE_WEIGHTS: tuple[Round188BaseScoreWeight, ...] = (
    Round188BaseScoreWeight("eps_fcf_opm_conversion", 22, "keep_high", "R4 Loop 12 requires OP/EPS/FCF conversion, not refining, petrochemical, tariff, or raw-material keywords."),
    Round188BaseScoreWeight("spread_product_margin_durability", 18, "separate_cycle_from_structural", "Refining margin, petrochemical spread, rubber spread, and ex-inventory OP must become durable FCF."),
    Round188BaseScoreWeight("restructuring_supply_cut_visibility", 18, "raised_for_loop12", "Plant shutdown, capacity cut, merger, government support, asset sale, and debt reduction can make spread recovery more durable."),
    Round188BaseScoreWeight("early_price_path_validation", 10, "required_backfill", "Stage 2 이후 MFE, event return, OP beat reaction, and relative strength separate validation from headline rallies."),
    Round188BaseScoreWeight("cycle_commodity_risk", 12, "hard_cycle_cap", "China oversupply, Middle East disruption reversal, oil/naphtha cycle, and inventory effects cap structural interpretation."),
    Round188BaseScoreWeight("operational_tariff_disclosure_redteam", 12, "hard_review", "Factory fire, production halt, anti-dumping tariff, undisclosed restructuring detail, and disclosure gaps can block Green."),
    Round188BaseScoreWeight("valuation_room_4b_runway", 8, "cool_crowded_spread_rallies", "Refining, petrochemical restructuring, tariff, and commodity narratives need 4B cooling when price outruns OP/FCF."),
)


ROUND188_STAGE_CAPS: tuple[Round188StageCap, ...] = (
    Round188StageCap(
        "Stage 1",
        "45",
        ("refining_margin_rebound", "petrochemical_restructuring", "ncc_shutdown_headline", "tariff_or_antidumping", "commodity_price_rally", "factory_news"),
        ("sk_innovation_refining_spread_turnaround_case", "lotte_hd_hyundai_ncc_capacity_cut_stage2_case"),
        "Spread or restructuring keywords route research only. Green is blocked before ex-inventory OP, durable spread, FCF, and price path evidence.",
    ),
    Round188StageCap(
        "Stage 2",
        "70",
        ("government_restructuring_approval", "capacity_cut_amount", "plant_shutdown", "quarterly_op_beat", "stake_sale_or_asset_sale", "factory_normalization_plan"),
        ("lotte_hd_hyundai_ncc_capacity_cut_stage2_case", "lg_chem_nav_governance_restructuring_stage2_case"),
        "Stage 2 can be strong, but Stage 3 waits for actual spread recovery, OP/EPS/FCF revision, utilization, and low hard-risk evidence.",
    ),
    Round188StageCap(
        "Stage 3",
        "requires_5_of_8",
        ("op_eps_revision_or_quarterly_op_beat", "op_ex_inventory_effect_improves", "product_spread_improves_two_quarters", "capacity_cut_or_restructuring_executed", "fcf_improvement", "60d_mfe_20pct_after_stage2", "no_china_tariff_cost_hard_issue", "valuation_not_near_cycle_peak"),
        ("sk_innovation_refining_spread_turnaround_case",),
        "Stage 3 early catch is possible only when OP/EPS/FCF, ex-inventory profit, spread durability, restructuring execution, and price path align.",
    ),
    Round188StageCap(
        "Stage 4B",
        "requires_4_of_6",
        ("stage2_120d_mfe_60pct", "refining_petrochem_tariff_headline_basket_rally", "op_eps_revision_lags_price", "spread_depends_on_event_supply_disruption", "china_oversupply_not_resolved", "valuation_near_prior_cycle_peak"),
        ("sk_innovation_refining_cycle_peak_4b_case",),
        "Spread rallies are cooled when price moves faster than ex-inventory earnings, FCF, and restructuring execution.",
    ),
    Round188StageCap(
        "Stage 4C",
        "hard_gate",
        ("large_factory_fire_or_production_halt", "capacity_cut_delay_or_restructuring_failure", "new_capacity_worsens_oversupply", "china_oversupply_persists", "tariff_or_antidumping_hits_exports", "inventory_loss_expands", "spread_collapse", "battery_or_petrochem_drag_consumes_refining_profit", "price_only_rally_before_plan_detail"),
        ("soil_shaheen_oversupply_4c_watch_case", "kumho_tire_gwangju_fire_hard_4c_case"),
        "A single hard production, oversupply, tariff, inventory, spread, drag, or disclosure-detail issue can block Green.",
    ),
)


ROUND188_SCORE_TARGETS: tuple[Round188ScoreTarget, ...] = (
    Round188ScoreTarget(
        "REFINING_SPREAD_TURNAROUND_KOREA",
        E2RArchetype.REFINING_SPREAD_TURNAROUND_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(22, 20, 6, 10, 12, 8, 8),
        ("refining_margin_rebound", "diesel_jet_fuel_shortage", "middle_east_disruption", "refinery_outage"),
        ("quarterly_op_beat", "refining_margin_recovery", "inventory_effect_disclosed", "op_revision"),
        ("op_ex_inventory_effect_improves", "fcf_improvement", "petrochem_battery_drag_reduces", "spread_improves_two_quarters", "60d_mfe_20pct_after_stage2"),
        ("refining_margin_news_rally", "war_supply_disruption_priced", "cycle_peak_near"),
        ("refining_margin_drop", "inventory_loss", "battery_loss_expands", "petrochemical_spread_weak", "logistics_normalization_delay"),
        ("op_ex_inventory_effect_improves", "fcf_improvement", "drag_reduction", "spread_durable"),
        ("inventory_loss", "temporary_supply_disruption", "battery_drag", "petrochem_drag"),
        ("refining_spread", "inventory_effect", "drag_reduction", "cycle_peak"),
        "Refining OP beat can be Stage 2~3 candidate evidence, but cycle peak and battery/petrochemical drag cap Green.",
    ),
    Round188ScoreTarget(
        "REFINING_PETCHEM_MIX_DRAG",
        E2RArchetype.REFINING_PETCHEM_MIX_DRAG,
        Round10ThemePosture.REDTEAM_FIRST,
        CAP_WEIGHT,
        ("refining_profit", "battery_loss", "petrochemical_loss", "mixed_business_drag"),
        ("segment_profit_bridge", "battery_loss_disclosed", "petrochem_spread_disclosed"),
        ("not_green_until_non_refining_drag_reduces_and_fcf_improves",),
        ("refining_profit_priced_while_drag_persists",),
        ("battery_loss_expands", "petrochemical_spread_weak", "refining_profit_consumed_by_drag"),
        ("battery_loss_reduces", "petrochem_spread_recovers", "fcf_improvement"),
        ("battery_loss_expands", "petrochem_drag", "segment_bridge_missing"),
        ("mix_drag", "segment_profit_bridge"),
        "Refining strength is capped when battery or petrochemical losses consume OP/FCF.",
    ),
    Round188ScoreTarget(
        "PETROCHEMICAL_RESTRUCTURING_KOREA",
        E2RArchetype.PETROCHEMICAL_RESTRUCTURING_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(19, 14, 20, 8, 14, 12, 8),
        ("petrochemical_oversupply", "china_capacity", "ncc_restructuring_need", "government_pressure"),
        ("restructuring_plan_submitted", "government_support", "capacity_cut_direction", "asset_sale_or_merger"),
        ("plant_shutdown_executed", "spread_recovery", "op_eps_revision", "fcf_improvement", "utilization_improves"),
        ("restructuring_news_rally_before_spread", "government_aid_priced_before_fcf"),
        ("plan_detail_missing", "china_oversupply_persists", "spread_weak", "capital_injection_burden", "impairment_risk"),
        ("plant_shutdown_executed", "spread_recovery", "fcf_improvement", "op_eps_revision"),
        ("plan_detail_missing", "spread_weak", "china_oversupply", "cashflow_unknown"),
        ("restructuring_detail", "spread_to_fcf", "oversupply"),
        "Petrochemical restructuring is Stage 2 evidence; Stage 3 waits for concrete closures, spread recovery, OP/EPS, and FCF.",
    ),
    Round188ScoreTarget(
        "NCC_CAPACITY_CUT_STAGE2",
        E2RArchetype.NCC_CAPACITY_CUT_STAGE2,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(18, 14, 22, 8, 12, 10, 8),
        ("ncc_capacity_cut", "daesan_ncc", "government_restructuring", "plant_shutdown"),
        ("capacity_cut_amount", "shutdown_duration", "merger_or_consolidation", "government_support_amount", "capital_injection"),
        ("ethylene_propylene_spread_recovery", "ncc_utilization_improves", "operating_loss_to_profit", "fcf_improvement"),
        ("capacity_cut_news_rally_before_spread",),
        ("shutdown_delayed", "spread_recovery_missing", "china_oversupply", "new_capacity_offsets_cut", "capital_injection_burden"),
        ("capacity_cut_executed", "spread_recovery", "utilization_improves", "fcf_improvement"),
        ("spread_recovery_missing", "china_oversupply", "shutdown_delayed"),
        ("capacity_cut", "utilization", "spread_recovery"),
        "NCC capacity cuts are Stage 2 strong but not Green before product spread, utilization, OP, and FCF recover.",
    ),
    Round188ScoreTarget(
        "NCC_OVERLOAD_SHAHEEN_RISK",
        E2RArchetype.NCC_OVERLOAD_SHAHEEN_RISK,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        ("shaheen_project", "aramco_investment", "ethylene_capacity_addition"),
        ("new_capacity_addition", "completion_timeline", "capex_burden"),
        ("not_green_until_new_capacity_absorbed_by_demand_and_spread_recovers",),
        ("strategic_asset_priced_before_spread_recovery",),
        ("new_capacity_worsens_oversupply", "q2_operating_loss", "spread_dilution", "capex_burden", "capacity_cut_effect_limited"),
        ("demand_absorbs_new_capacity", "spread_recovers", "capex_burden_low"),
        ("new_capacity_worsens_oversupply", "spread_dilution", "capex_burden"),
        ("oversupply_new_capacity", "capex_burden"),
        "Shaheen can be a strategic asset, but in an oversupply cycle it is a hard RedTeam capacity-addition overlay.",
        hard_gate=True,
    ),
    Round188ScoreTarget(
        "SPECIALTY_CHEM_GOVERNANCE_RESTRUCTURING",
        E2RArchetype.SPECIALTY_CHEM_GOVERNANCE_RESTRUCTURING,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(17, 12, 14, 8, 10, 10, 18),
        ("nav_discount", "activism", "petrochemical_drag", "battery_stake_value"),
        ("board_refresh_or_buyback_demand", "stake_sale", "asset_sale_amount", "debt_reduction_use"),
        ("buyback_or_cancel_executed", "net_debt_reduction", "fcf_recovery", "petrochemical_restructuring", "nav_discount_closes"),
        ("activism_news_rally_before_execution", "nav_discount_story_crowded"),
        ("actual_buyback_missing", "petrochemical_drag", "cashflow_effect_unknown", "capital_allocation_not_executed"),
        ("capital_return_executed", "debt_reduction", "fcf_recovery", "petrochemical_drag_reduces"),
        ("buyback_missing", "petrochemical_drag", "cashflow_unknown"),
        ("nav_discount", "capital_allocation", "petrochemical_drag"),
        "Specialty-chem governance can be Stage 2, but Stage 3 needs real capital return, debt reduction, FCF, and petrochemical drag relief.",
    ),
    Round188ScoreTarget(
        "SYNTHETIC_RUBBER_TARIFF_RISK",
        E2RArchetype.SYNTHETIC_RUBBER_TARIFF_RISK,
        Round10ThemePosture.REDTEAM_FIRST,
        _w(17, 14, 6, 8, 14, 18, 8),
        ("synthetic_rubber_spread", "epdm", "sbr_br_ssbr", "tire_auto_construction_demand"),
        ("product_mix", "rubber_spread", "customer_demand", "china_antidumping_duty"),
        ("spread_improves", "china_exposure_reduces", "opm_fcf_improves", "auto_tire_demand_recovers"),
        ("tariff_headline_rally", "rubber_cycle_rally_without_opm"),
        ("china_antidumping_duty", "auto_construction_demand_slowdown", "butadiene_cost_rise", "export_exposure_hit"),
        ("spread_improves", "china_exposure_reduces", "opm_fcf_improves"),
        ("china_antidumping_duty", "demand_cycle", "butadiene_cost"),
        ("tariff", "rubber_spread", "auto_construction_cycle"),
        "Synthetic rubber remains Watch/Red until tariff, China demand, raw-material cost, OPM, and FCF are cleared.",
    ),
    Round188ScoreTarget(
        "TIRE_RUBBER_PRODUCTION_DISRUPTION",
        E2RArchetype.TIRE_RUBBER_PRODUCTION_DISRUPTION,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        ("tire_demand", "rubber_material_chain", "factory_capacity", "global_auto_customer"),
        ("production_disruption_identified", "capacity_loss_percent", "customer_supply_risk"),
        ("not_green_until_factory_normalized_and_revenue_guidance_recovered",),
        ("tire_demand_story_ignores_production_disruption",),
        ("factory_fire", "production_halt", "capacity_loss_20pct", "revenue_target_cut_risk", "customer_supply_disruption"),
        ("factory_normalized", "customer_supply_restored", "revenue_guidance_recovered"),
        ("factory_fire", "production_halt", "capacity_loss_20pct"),
        ("production_disruption", "customer_supply", "revenue_guidance"),
        "A major tire/rubber production disruption is a hard operational 4C overlay even if spreads or demand look favorable.",
        hard_gate=True,
    ),
    Round188ScoreTarget(
        "COMMODITY_SPREAD_CYCLE_NOT_STRUCTURAL",
        E2RArchetype.COMMODITY_SPREAD_CYCLE_NOT_STRUCTURAL,
        Round10ThemePosture.REDTEAM_FIRST,
        CAP_WEIGHT,
        ("commodity_price_rally", "spread_rebound", "tariff_headline", "raw_material_price_move"),
        ("spread_rebound_measured", "op_revision_observed", "cycle_driver_identified"),
        ("not_green_until_spread_op_fcf_and_supply_cut_are_durable",),
        ("cycle_rally_priced_as_structural",),
        ("spread_reversal", "china_oversupply", "event_supply_disruption_reversal", "inventory_loss"),
        ("durable_spread", "supply_cut", "fcf_improvement"),
        ("cycle_only", "price_only_rally", "inventory_noise"),
        ("cycle_cap", "spread_durability"),
        "R4 commodity spread moves are capped unless durable spread, supply discipline, OP/EPS, FCF, and price path confirm.",
    ),
    Round188ScoreTarget(
        "DISCLOSURE_CONFIDENCE_CAP",
        E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        Round10ThemePosture.REDTEAM_FIRST,
        CAP_WEIGHT,
        ("opendart_list_only", "media_report", "policy_headline", "restructuring_plan", "factory_announcement"),
        ("detail_fetch_required", "product_spread_required", "utilization_opm_fcf_required"),
        ("not_green_until_product_spread_opm_fcf_and_plan_detail_are_verified",),
        ("headline_priced_before_detail",),
        ("plan_detail_missing", "media_report_only", "spread_missing", "opm_unknown", "capacity_cut_amount_missing"),
        ("plan_detail_disclosed", "product_spread", "opm_fcf_visible", "capacity_cut_executed"),
        ("list_only", "media_only", "plan_detail_missing", "spread_missing"),
        ("detail_missing", "spread_missing", "opm_unknown"),
        "Round 188 caps list-only, media-only, policy-only, restructuring-plan-only, and missing spread/OPM/FCF evidence before Green.",
    ),
)


ROUND188_CASE_CANDIDATES: tuple[Round188CaseCandidate, ...] = (
    Round188CaseCandidate(
        "sk_innovation_refining_spread_turnaround_case",
        "REFINING_SPREAD_TURNAROUND_KOREA",
        "096770",
        "SK이노베이션 refining spread turnaround",
        "KR",
        "success_candidate",
        ("q1_op_2_2tn_krw", "consensus_beat", "refining_margin_recovery", "middle_east_supply_disruption", "diesel_jet_fuel_shortage"),
        ("battery_drag", "petrochemical_drag", "recovery_duration_warning", "cycle_peak_risk"),
        "stage2_strong_to_stage3_only_if_ex_inventory_op_fcf_and_drag_reduction_align",
        "needs_ex_inventory_op_fcf_drag_price_backfill",
        ("round_188.md Reuters SK Innovation Q1 profit / refining recovery",),
        "SK Innovation is Stage 2 strong; Stage 3 waits for ex-inventory OP, FCF, spread durability, and battery/petrochemical drag reduction.",
        (E2RArchetype.REFINING_PETCHEM_MIX_DRAG, E2RArchetype.STRUCTURAL_STAGE3_EARLY_CAPTURE),
    ),
    Round188CaseCandidate(
        "sk_innovation_refining_cycle_peak_4b_case",
        "COMMODITY_SPREAD_CYCLE_NOT_STRUCTURAL",
        "096770",
        "SK이노베이션 refining margin cycle peak watch",
        "KR",
        "4b_watch",
        ("refining_margin_spike", "war_supply_disruption", "jet_fuel_diesel_shortage", "op_beat"),
        ("event_supply_disruption_reversal", "margin_normalization", "price_rally_before_fcf", "cycle_peak_risk"),
        "refining_margin_event_rally_requires_4b_watch_if_price_outruns_fcf",
        "needs_120d_mfe_revision_spread_normalization_backfill",
        ("round_188.md Reuters refining disruption / jet fuel diesel shortage",),
        "A strong refining OP beat can become 4B-watch when war-driven disruption and crack spreads normalize before FCF becomes durable.",
        (E2RArchetype.CYCLE_SUCCESS_NOT_STRUCTURAL, E2RArchetype.CROWDED_RERATING_4B_WATCH),
    ),
    Round188CaseCandidate(
        "lotte_hd_hyundai_ncc_capacity_cut_stage2_case",
        "NCC_CAPACITY_CUT_STAGE2",
        "011170/267250/004000",
        "롯데케미칼·HD현대케미칼 대산 NCC 구조조정",
        "KR",
        "success_candidate",
        ("daesan_ncc_integration", "1_1m_ton_shutdown", "3_year_halt", "2tn_krw_government_support", "1_2tn_krw_capital_injection"),
        ("spread_recovery_not_confirmed", "china_oversupply", "fcf_not_confirmed", "new_capacity_offsets_cut"),
        "stage2_strong_but_green_blocked_before_spread_utilization_op_fcf",
        "needs_spread_utilization_op_fcf_price_backfill",
        ("round_188.md Reuters first petrochemical restructuring deal",),
        "Daesan NCC capacity cut is Stage 2 strong; Stage 3 waits for product spread, utilization, OP, and FCF recovery.",
        (E2RArchetype.STAGE2_STRONG_NOT_GREEN,),
    ),
    Round188CaseCandidate(
        "lg_chem_hanwha_dl_yncc_plan_submission_stage2_case",
        "PETROCHEMICAL_RESTRUCTURING_KOREA",
        "051910/009830/DL_CHEM/YNCC",
        "LG화학·한화솔루션·DL케미칼 / YNCC restructuring plan",
        "KR",
        "success_candidate",
        ("restructuring_plan_submitted", "ncc_capacity_cut_direction", "government_pressure", "25pct_capacity_cut_goal"),
        ("plan_detail_missing", "cashflow_effect_unknown", "china_oversupply", "impairment_risk"),
        "plan_submission_is_stage2_not_green_before_detail_spread_fcf",
        "needs_plan_detail_capacity_cut_spread_fcf_backfill",
        ("round_188.md Reuters LG Chem restructuring plan",),
        "Plan submission is Stage 2 evidence, not Green before concrete shutdowns, spread recovery, OP/EPS revision, and cash-flow effects.",
        (E2RArchetype.STAGE2_EVIDENCE_NOT_GREEN, E2RArchetype.DISCLOSURE_CONFIDENCE_CAP),
    ),
    Round188CaseCandidate(
        "lg_chem_nav_governance_restructuring_stage2_case",
        "SPECIALTY_CHEM_GOVERNANCE_RESTRUCTURING",
        "051910",
        "LG화학 NAV discount / governance restructuring",
        "KR",
        "success_candidate",
        ("nav_discount_73pct", "palliser_activism", "board_refresh_buyback_request", "lges_stake_sale_2tn_krw", "debt_reduction_use"),
        ("petrochemical_drag", "actual_buyback_missing", "cashflow_effect_unknown", "capital_allocation_not_executed"),
        "stage2_governance_option_not_green_before_buyback_fcf_drag_reduction",
        "needs_buyback_debt_fcf_nav_price_backfill",
        ("round_188.md Reuters Palliser LG Chem", "round_188.md Reuters LG Chem LGES stake sale"),
        "LG Chem is Stage 2 governance/restructuring optionality; Stage 3 needs execution, FCF, debt reduction, and petrochemical drag relief.",
        (E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN, E2RArchetype.STAGE2_EVIDENCE_NOT_GREEN),
    ),
    Round188CaseCandidate(
        "soil_shaheen_oversupply_4c_watch_case",
        "NCC_OVERLOAD_SHAHEEN_RISK",
        "010950",
        "S-Oil Shaheen oversupply risk",
        "KR",
        "4c_thesis_break",
        ("shaheen_project", "aramco_backed_project", "1_8m_tpy_ethylene_capacity", "2026_completion", "q2_operating_loss"),
        ("new_capacity_worsens_oversupply", "spread_dilution", "capex_burden", "capacity_cut_effect_limited"),
        "strategic_asset_but_hard_oversupply_redteam_until_demand_spread_absorb_new_capacity",
        "needs_new_capacity_spread_capex_loss_price_backfill",
        ("round_188.md Reuters S-Oil Shaheen capacity / petrochemical production",),
        "Shaheen is a strategic asset, but in Korea petrochemical oversupply it is a RedTeam capacity-addition overlay, not Stage 3.",
        (E2RArchetype.THESIS_BREAK_4C,),
    ),
    Round188CaseCandidate(
        "korea_petrochemical_oversupply_hard_cap_case",
        "COMMODITY_SPREAD_CYCLE_NOT_STRUCTURAL",
        "KOREA_PETROCHEM_SECTOR",
        "한국 석유화학 oversupply hard cap",
        "KR",
        "failed_rerating",
        ("10_companies_capacity_cut_agreement", "270_370m_ton_cut", "up_to_25pct_capacity_cut", "government_crisis_label"),
        ("china_oversupply", "demand_weakness", "margin_recovery_delayed_to_2027", "policy_restructuring_not_green"),
        "government_restructuring_is_crisis_admission_until_spread_and_fcf_recover",
        "needs_sector_spread_capacity_cut_fcf_price_backfill",
        ("round_188.md Reuters Korean petrochemical capacity cut",),
        "Government restructuring can be Stage 2 evidence, but it begins from crisis recognition and cannot create Green without spread and FCF recovery.",
        (E2RArchetype.CYCLE_SUCCESS_NOT_STRUCTURAL,),
    ),
    Round188CaseCandidate(
        "kumho_petrochemical_epdm_tariff_risk_case",
        "SYNTHETIC_RUBBER_TARIFF_RISK",
        "011780",
        "금호석유화학 EPDM tariff risk",
        "KR",
        "failed_rerating",
        ("epdm", "synthetic_rubber_product_mix", "tire_auto_construction_demand", "rubber_spread"),
        ("china_antidumping_duty", "auto_construction_demand_cycle", "butadiene_cost_rise", "export_exposure"),
        "watch_red_until_tariff_demand_spread_opm_and_fcf_are_cleared",
        "needs_tariff_spread_export_demand_price_backfill",
        ("round_188.md Reuters China anti-dumping duties on EPDM",),
        "Kumho Petrochemical remains Watch/Red until tariff, China demand, rubber spread, OPM, and FCF are cleared.",
        (E2RArchetype.TARIFF_IMPORT_REGULATION_OVERLAY,),
    ),
    Round188CaseCandidate(
        "kumho_tire_gwangju_fire_hard_4c_case",
        "TIRE_RUBBER_PRODUCTION_DISRUPTION",
        "073240",
        "금호타이어 광주공장 화재 생산차질",
        "KR",
        "4c_thesis_break",
        ("gwangju_factory_fire", "production_halt", "12m_tire_capacity", "20pct_global_capacity", "share_price_minus_8pct", "revenue_target_cut_risk"),
        ("factory_fire", "production_halt", "capacity_loss_20pct", "customer_supply_disruption", "revenue_target_cut_risk"),
        "major_factory_fire_is_hard_4c_even_if_rubber_spread_or_tire_demand_look_favorable",
        "needs_fire_recovery_customer_supply_revenue_price_backfill",
        ("round_188.md Reuters Kumho Tire Gwangju fire",),
        "A large tire production disruption is a hard operational 4C overlay; one factory event can break the price path.",
        (E2RArchetype.OPERATIONAL_TRUST_HARD_4C,),
    ),
    Round188CaseCandidate(
        "r4_loop12_disclosure_confidence_reference_case",
        "DISCLOSURE_CONFIDENCE_CAP",
        "R4_DISCLOSURE_CAP",
        "R4 Loop 12 spread / restructuring detail confidence reference",
        "KR",
        "failed_rerating",
        ("watch_disclosure_detail_required", "product_spread_required", "capacity_cut_amount_required", "opm_fcf_required", "plan_detail_required"),
        ("opendart_list_only", "media_report_only", "plan_detail_missing", "spread_missing", "opm_unknown"),
        "list_media_policy_restructuring_plan_only_cannot_create_green",
        "needs_opendart_detail_spread_opm_fcf_backfill",
        ("round_188.md disclosure confidence rule",),
        "R4 Loop 12 requires detail fetch and forbids invented missing spread, capacity cut, utilization, OPM, FCF, and stage price fields.",
    ),
)


ROUND188_SCORE_STAGE_PRICE_ALIGNMENT: tuple[Round188ScoreStagePriceAlignment, ...] = (
    Round188ScoreStagePriceAlignment("sk_innovation_refining_spread_turnaround_case", "Stage 2 strong", "OP beat is strong, but ex-inventory OP, FCF, drag reduction, and 60D MFE need backfill", "stage2_to_stage3_if_spread_fcf_drag_align", "credit OP beat; cap before durable spread, ex-inventory OP, FCF, and drag reduction"),
    Round188ScoreStagePriceAlignment("sk_innovation_refining_cycle_peak_4b_case", "Stage 2 -> 4B-watch", "War/supply-disruption margin can normalize before FCF becomes structural", "cycle_peak_requires_4b_watch", "cool refining headline rallies when price outruns OP/EPS revision"),
    Round188ScoreStagePriceAlignment("lotte_hd_hyundai_ncc_capacity_cut_stage2_case", "Stage 2 strong", "Capacity cut is visible, but spread/FCF recovery is not yet proven", "capacity_cut_not_green_before_spread_fcf", "credit shutdown/support; cap before utilization, spread, OP, and FCF recover"),
    Round188ScoreStagePriceAlignment("lg_chem_hanwha_dl_yncc_plan_submission_stage2_case", "Stage 2 watch", "Plan submission lacks shutdown detail and cash-flow effect", "plan_submission_cap", "require plan detail, executed cut, spread recovery, and FCF"),
    Round188ScoreStagePriceAlignment("lg_chem_nav_governance_restructuring_stage2_case", "Stage 2 governance option", "NAV/activism/stake sale need capital-return and FCF execution", "governance_execution_gate", "credit NAV discount and stake sale; cap before buyback/cancel, debt reduction, and FCF"),
    Round188ScoreStagePriceAlignment("soil_shaheen_oversupply_4c_watch_case", "4C-watch", "New capacity during oversupply can offset restructuring", "new_capacity_blocks_green", "apply oversupply, capex burden, and spread dilution hard gate"),
    Round188ScoreStagePriceAlignment("kumho_petrochemical_epdm_tariff_risk_case", "Watch/Red", "Tariff and auto/construction cycle can overwhelm product mix", "tariff_cycle_cap", "require ex-China sales, rubber spread, OPM, and FCF"),
    Round188ScoreStagePriceAlignment("kumho_tire_gwangju_fire_hard_4c_case", "4C hard gate", "Factory fire and 20% capacity disruption broke the price path", "production_disruption_hard_gate", "block Green until production, customer supply, and revenue guidance recover"),
)


ROUND188_PRICE_FIELDS: tuple[str, ...] = (
    "ticker",
    "company_name",
    "canonical_archetype",
    "case_type",
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
    "mfe_20d_after_stage2",
    "mae_20d_after_stage2",
    "mfe_60d_after_stage2",
    "mae_60d_after_stage2",
    "mfe_120d_after_stage2",
    "mae_120d_after_stage2",
    "mfe_252d_after_stage2",
    "mae_252d_after_stage2",
    "relative_strength_vs_kospi",
    "relative_strength_vs_chemical_basket",
    "relative_strength_vs_refining_basket",
    "relative_strength_vs_materials_basket",
    "refining_margin",
    "petrochemical_spread",
    "rubber_spread",
    "raw_material_cost_signal",
    "inventory_gain_loss_signal",
    "op_ex_inventory_effect",
    "op_revision_before_stage3",
    "op_revision_after_stage3",
    "eps_revision_before_stage3",
    "eps_revision_after_stage3",
    "fcf_signal",
    "opm",
    "capacity_cut_amount",
    "plant_shutdown_flag",
    "shutdown_duration",
    "merger_or_consolidation_flag",
    "government_support_amount",
    "tax_or_utility_support",
    "asset_sale_amount",
    "debt_reduction_use",
    "new_capacity_addition",
    "china_oversupply_flag",
    "tariff_or_antidumping_flag",
    "export_exposure",
    "production_disruption_flag",
    "factory_fire_flag",
    "capex_burden_flag",
    "media_report_only_flag",
    "plan_detail_disclosed_flag",
    "disclosure_confidence",
    "valuation_at_stage3",
    "valuation_at_stage4b",
)


def round188_target_for(target_id: str) -> Round188ScoreTarget | None:
    for target in ROUND188_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round188_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND188_CASE_CANDIDATES:
        target = round188_target_for(candidate.target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {candidate.target_id}")
        weights = target.score_weight.as_dict()
        stage4b_evidence = candidate.evidence_fields if candidate.case_type == "4b_watch" else ()
        stage4c_evidence = candidate.red_flag_fields if candidate.case_type == "4c_thesis_break" or target.hard_gate else ()
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
            evidence_summary=(
                f"Round188 R4 Loop-12 Korea materials/spread case for {candidate.target_id}; "
                "calibration-only and focused on spread durability, ex-inventory OP, restructuring execution, FCF, tariff/production risk, and price path."
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
            score_price_alignment=_round188_score_price_alignment(candidate),
            rerating_result=_round188_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
            score_weight_hint={
                "eps_fcf": _numeric_weight(weights["eps_fcf_opm"]),
                "spread_product_margin_durability": _numeric_weight(weights["spread_product_margin_durability"]),
                "restructuring_supply_cut_visibility": _numeric_weight(weights["restructuring_supply_cut_visibility"]),
                "early_price_validation": _numeric_weight(weights["early_price_validation"]),
                "cycle_commodity_risk": _numeric_weight(weights["cycle_commodity_risk"]),
                "operational_tariff_disclosure_redteam": _numeric_weight(weights["operational_tariff_disclosure_redteam"]),
                "valuation_4b_room": _numeric_weight(weights["valuation_4b_room"]),
            },
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "stage3_early_catch_requires_5_of_8_loop12_conditions",
                "stage4b_cooling_requires_4_of_6_loop12_conditions",
                "commodity_spread_or_restructuring_keyword_cannot_create_stage3",
                "require_ex_inventory_op_spread_fcf_restructuring_execution_and_price_path_for_green",
                "china_oversupply_tariff_factory_fire_shaheen_and_drag_can_block_green",
                "do_not_invent_spread_capacity_cut_opm_fcf_stage_prices_or_restructuring_details",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=False,
                price_data_available=False,
                stage_dates_confidence=0.2,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round188_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND188_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "eps_fcf_opm": str(weights["eps_fcf_opm"]),
                "spread_product_margin_durability": str(weights["spread_product_margin_durability"]),
                "restructuring_supply_cut_visibility": str(weights["restructuring_supply_cut_visibility"]),
                "early_price_validation": str(weights["early_price_validation"]),
                "cycle_commodity_risk": str(weights["cycle_commodity_risk"]),
                "operational_tariff_disclosure_redteam": str(weights["operational_tariff_disclosure_redteam"]),
                "valuation_4b_room": str(weights["valuation_4b_room"]),
                "stage1_signals": "|".join(target.stage1_signals),
                "stage2_signals": "|".join(target.stage2_signals),
                "stage3_conditions": "|".join(target.stage3_conditions),
                "stage4b_conditions": "|".join(target.stage4b_conditions),
                "stage4c_conditions": "|".join(target.stage4c_conditions),
                "green_conditions": "|".join(target.green_conditions),
                "red_flags": "|".join(target.red_flags),
                "loop12_penalty_axes": "|".join(target.loop12_penalty_axes),
                "hard_gate": str(target.hard_gate).lower(),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round188_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND188_CASE_CANDIDATES:
        target = round188_target_for(candidate.target_id)
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
                "alignment_hint": candidate.alignment_hint,
                "price_validation_status": candidate.price_validation_status,
                "production_input": "false",
                "notes": candidate.notes,
            }
        )
    return tuple(rows)


def round188_stage_date_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "target_id": target.target_id,
            "stage1": "|".join(target.stage1_signals),
            "stage2": "|".join(target.stage2_signals),
            "stage3": "|".join(target.stage3_conditions),
            "stage4b": "|".join(target.stage4b_conditions),
            "stage4c": "|".join(target.stage4c_conditions),
            "red_flags": "|".join(target.red_flags),
            "hard_gate": str(target.hard_gate).lower(),
            "production_scoring_changed": "false",
        }
        for target in ROUND188_SCORE_TARGETS
    )


def round188_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round188_backfill": "true"} for field in ROUND188_PRICE_FIELDS)


def round188_base_score_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND188_BASE_SCORE_WEIGHTS)


def round188_stage_cap_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND188_STAGE_CAPS)


def round188_score_stage_price_alignment_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND188_SCORE_STAGE_PRICE_ALIGNMENT)


def round188_summary() -> dict[str, int | bool]:
    records = round188_case_records()
    return {
        "target_count": len(ROUND188_SCORE_TARGETS),
        "source_canonical_target_count": ROUND188_SOURCE_CANONICAL_TARGET_COUNT,
        "case_candidate_count": len(records),
        "base_score_axis_count": len(ROUND188_BASE_SCORE_WEIGHTS),
        "stage_cap_count": len(ROUND188_STAGE_CAPS),
        "score_stage_price_alignment_count": len(ROUND188_SCORE_STAGE_PRICE_ALIGNMENT),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "hard_gate_target_count": sum(1 for target in ROUND188_SCORE_TARGETS if target.hard_gate),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round188_r4_loop12_reports(
    *,
    output_directory: str | Path = ROUND188_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND188_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND188_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round188_r4_loop12_materials_spread_strategic_summary.md",
        "case_matrix": output / "round188_r4_loop12_case_matrix.csv",
        "stage_date_plan": output / "round188_r4_loop12_stage_date_plan.csv",
        "green_guardrails": output / "round188_r4_loop12_green_guardrails.md",
        "risk_overlays": output / "round188_r4_loop12_risk_overlays.md",
        "price_validation_plan": output / "round188_r4_loop12_price_validation_plan.md",
        "price_fields": output / "round188_r4_loop12_price_fields.csv",
        "base_score_weights": output / "round188_r4_loop12_base_score_weights.csv",
        "stage_caps": output / "round188_r4_loop12_stage_caps.csv",
        "score_stage_price_alignment": output / "round188_r4_loop12_score_stage_price_alignment.csv",
        "score_stage_price_alignment_md": output / "round188_r4_loop12_score_stage_price_alignment.md",
    }
    _write_case_jsonl(round188_case_records(), cases)
    _write_rows(round188_score_profile_rows(), score_profiles)
    _write_rows(round188_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round188_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round188_price_field_rows(), paths["price_fields"])
    _write_rows(round188_base_score_weight_rows(), paths["base_score_weights"])
    _write_rows(round188_stage_cap_rows(), paths["stage_caps"])
    _write_rows(round188_score_stage_price_alignment_rows(), paths["score_stage_price_alignment"])
    paths["summary"].write_text(render_round188_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round188_green_guardrail_markdown(), encoding="utf-8")
    paths["risk_overlays"].write_text(render_round188_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round188_price_validation_plan_markdown(), encoding="utf-8")
    paths["score_stage_price_alignment_md"].write_text(render_round188_score_stage_price_alignment_markdown(), encoding="utf-8")
    return paths


def render_round188_summary_markdown() -> str:
    summary = round188_summary()
    lines = [
        "# Round-188 R4 Loop-12 Materials / Spread / Strategic Resources Summary",
        "",
        f"- source_round: `{ROUND188_SOURCE_ROUND_PATH}`",
        f"- large_sector: `{Round10LargeSector.MATERIALS_SPREAD_STRATEGIC.value}`",
        "- loop: `R4 Loop 12 / v12.0`",
        f"- target_count: {summary['target_count']}",
        f"- source_canonical_target_count: {summary['source_canonical_target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- base_score_axis_count: {summary['base_score_axis_count']}",
        f"- stage_cap_count: {summary['stage_cap_count']}",
        f"- score_stage_price_alignment_count: {summary['score_stage_price_alignment_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- failed_rerating_count: {summary['failed_rerating_count']}",
        f"- stage4b_case_count: {summary['stage4b_case_count']}",
        f"- stage4c_case_count: {summary['stage4c_case_count']}",
        f"- hard_gate_target_count: {summary['hard_gate_target_count']}",
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "",
        "- R4 Loop 12 separates spread rebound from structural EPS/FCF rerating.",
        "- Example: SK Innovation OP beat is Stage 2 strong, but ex-inventory OP, FCF, and drag reduction gate Stage 3.",
        "- Example: Lotte/HD Hyundai NCC capacity cut is Stage 2 strong, not Green before spread and FCF recover.",
        "- Example: LG Chem NAV activism is a Stage 2 governance option, but execution and FCF are required.",
        "- Example: S-Oil Shaheen, Kumho Tire fire, China oversupply, tariff, and missing restructuring detail are RedTeam overlays.",
    ]
    return "\n".join(lines) + "\n"


def render_round188_green_guardrail_markdown() -> str:
    lines = [
        "# Round-188 R4 Loop-12 Green Guardrails",
        "",
        "Stage 3-Green is not granted for refining margin, petrochemical restructuring, tariff, raw-material, factory, or policy words alone.",
        "",
        "## Stage 3 Early Catch",
        "",
        "R4 Loop 12 requires at least 5 of 8 checks:",
    ]
    stage3 = next(item for item in ROUND188_STAGE_CAPS if item.stage_band == "Stage 3")
    lines.extend(f"- `{field}`" for field in stage3.required_evidence)
    lines.extend(
        [
            "",
            "## What This Means",
            "",
            "- SK이노베이션: OP beat는 Stage 2 strong이지만 재고손익 제외 OP, FCF, drag 축소가 필요.",
            "- 롯데케미칼/HD현대케미칼: NCC 3년 중단과 정부 지원은 Stage 2, spread/FCF 전 Green 금지.",
            "- LG화학: NAV·행동주의·LGES 지분매각은 Stage 2 option이고 실제 환원·부채감소·FCF가 필요.",
            "- S-Oil: Shaheen은 전략자산일 수 있지만 공급과잉 구간에서는 RedTeam capacity-addition overlay.",
            "- 금호타이어: 공장 화재와 20% capacity 차질은 spread나 수요 회복과 무관하게 hard 4C.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round188_risk_overlay_markdown() -> str:
    lines = [
        "# Round-188 R4 Loop-12 Risk Overlays",
        "",
        "| target | hard gate | red flags |",
        "| --- | --- | --- |",
    ]
    for target in ROUND188_SCORE_TARGETS:
        lines.append(f"| `{target.target_id}` | {str(target.hard_gate).lower()} | {', '.join(target.red_flags)} |")
    lines.extend(
        [
            "",
            "## Hard / Cap Examples",
            "",
            "- `NCC_OVERLOAD_SHAHEEN_RISK`: 신규 ethylene CAPA가 구조조정 효과를 약화하면 Green을 막는다.",
            "- `TIRE_RUBBER_PRODUCTION_DISRUPTION`: 공장 화재, 생산중단, capacity loss, 고객 공급 차질은 hard 4C다.",
            "- `SYNTHETIC_RUBBER_TARIFF_RISK`: 중국 반덤핑 관세와 자동차/건설 수요 cycle은 Watch/Red cap이다.",
            "- `REFINING_PETCHEM_MIX_DRAG`: 정유 이익을 배터리·석화 drag가 잠식하면 Stage 3를 제한한다.",
            "- `DISCLOSURE_CONFIDENCE_CAP`: 제품별 spread, 가동률, OPM, FCF, 구조조정 세부안 미공개면 Green 금지.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round188_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-188 R4 Loop-12 Price Validation Plan",
        "",
        "R4 Loop 12 must backfill spread, ex-inventory OP, restructuring execution, tariff, production disruption, and price-path fields together.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND188_PRICE_FIELDS)
    lines.extend(
        [
            "",
            "## Backfill Priorities",
            "",
            "- `sk_innovation_refining_spread_turnaround_case`: refining margin, op_ex_inventory_effect, FCF, battery/petrochem drag, 60D/120D MFE.",
            "- `lotte_hd_hyundai_ncc_capacity_cut_stage2_case`: capacity_cut_amount, shutdown_duration, spread, utilization, OP, FCF.",
            "- `lg_chem_nav_governance_restructuring_stage2_case`: asset sale, debt reduction, buyback/cancel execution, NAV discount, FCF.",
            "- `soil_shaheen_oversupply_4c_watch_case`: new capacity, capex burden, spread dilution, operating loss, relative price reaction.",
            "- `kumho_tire_gwangju_fire_hard_4c_case`: factory fire date, capacity loss, revenue guidance, customer supply, event return.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round188_score_stage_price_alignment_markdown() -> str:
    lines = [
        "# Round-188 R4 Loop-12 Score / Stage / Price Alignment",
        "",
        "| case | detected stage | price path status | verdict | adjustment |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in ROUND188_SCORE_STAGE_PRICE_ALIGNMENT:
        lines.append(f"| `{row.case_id}` | {row.detected_stage} | {row.price_path_status} | {row.verdict} | {row.normalization_adjustment} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- SK Innovation shows why a strong OP beat can be Stage 2 while Green waits for durable FCF and drag reduction.",
            "- NCC restructuring shows why capacity cuts are useful but not sufficient before spread and FCF recover.",
            "- Shaheen and Kumho Tire show that new capacity or production disruption can break the thesis before the price path validates.",
        ]
    )
    return "\n".join(lines) + "\n"


def _round188_score_price_alignment(candidate: Round188CaseCandidate) -> str:
    if candidate.case_type in {"success_candidate", "structural_success"}:
        return "unknown"
    if candidate.case_type in {"event_premium", "4b_watch", "cyclical_success"}:
        return "price_moved_without_evidence"
    if candidate.case_type == "4c_thesis_break":
        return "false_positive_score"
    if candidate.case_type == "failed_rerating":
        return "evidence_good_but_price_failed"
    return "unknown"


def _round188_rerating_result(candidate: Round188CaseCandidate) -> str:
    if candidate.case_type in {"success_candidate", "structural_success"}:
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


def _numeric_weight(value: int | str) -> float:
    return float(value) if isinstance(value, int) else 0.0


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
    "ROUND188_BASE_SCORE_WEIGHTS",
    "ROUND188_CASE_CANDIDATES",
    "ROUND188_DEFAULT_CASES_PATH",
    "ROUND188_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND188_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND188_PRICE_FIELDS",
    "ROUND188_SCORE_STAGE_PRICE_ALIGNMENT",
    "ROUND188_SCORE_TARGETS",
    "ROUND188_SOURCE_CANONICAL_TARGET_COUNT",
    "ROUND188_SOURCE_CANONICAL_TARGET_IDS",
    "ROUND188_STAGE_CAPS",
    "render_round188_green_guardrail_markdown",
    "render_round188_price_validation_plan_markdown",
    "render_round188_risk_overlay_markdown",
    "render_round188_score_stage_price_alignment_markdown",
    "render_round188_summary_markdown",
    "round188_base_score_weight_rows",
    "round188_case_candidate_rows",
    "round188_case_records",
    "round188_price_field_rows",
    "round188_score_profile_rows",
    "round188_score_stage_price_alignment_rows",
    "round188_stage_cap_rows",
    "round188_stage_date_rows",
    "round188_summary",
    "round188_target_for",
    "write_round188_r4_loop12_reports",
]
