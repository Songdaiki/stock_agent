"""Round-173 R2 Loop-11 Korea AI, semiconductor, and electronics pack.

Round 173 applies Loop 11 to Korea-listed AI, semiconductor equipment,
post-processing, PCB, test socket, system semiconductor, on-device AI, and
private AI-chip related themes. It is calibration/report material only.
Production feature engineering, scoring, staging, and RedTeam code must not
import this module.
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


ROUND173_SOURCE_ROUND_PATH = "docs/round/round_173.md"
ROUND173_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round173_r2_loop11_ai_semiconductor_electronics"
ROUND173_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r2_loop11_round173.jsonl"
ROUND173_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round173_r2_loop11_v11.csv"
ROUND173_SOURCE_CANONICAL_TARGET_IDS: tuple[str, ...] = (
    "HBM_BONDER_EQUIPMENT_KOREA",
    "ADVANCED_PACKAGING_EQUIPMENT_KOREA",
    "AI_SERVER_PCB_MLB_KOREA",
    "SEMICONDUCTOR_TEST_SOCKET_KOREA",
    "HBM_TEST_EQUIPMENT_KOREA",
    "SYSTEM_SEMI_FOUNDARY_OPTION_KOREA",
    "AI_CHIP_FABRIC_PRIVATE_RELATED",
    "ON_DEVICE_AI_THEME",
    "MOU_OR_REPORT_NOT_CONTRACT",
    "DISCLOSURE_CONFIDENCE_CAP",
)
ROUND173_SOURCE_CANONICAL_TARGET_COUNT = len(ROUND173_SOURCE_CANONICAL_TARGET_IDS)


@dataclass(frozen=True)
class Round173ScoreWeightDraft:
    eps_fcf_opm: int | str
    customer_contract_shipment_visibility: int | str
    bottleneck_pricing: int | str
    early_price_validation: int | str
    information_confidence: int | str
    capital_discipline_fcf: int | str
    valuation_4b_room: int | str

    def as_dict(self) -> dict[str, int | str]:
        return {
            "eps_fcf_opm": self.eps_fcf_opm,
            "customer_contract_shipment_visibility": self.customer_contract_shipment_visibility,
            "bottleneck_pricing": self.bottleneck_pricing,
            "early_price_validation": self.early_price_validation,
            "information_confidence": self.information_confidence,
            "capital_discipline_fcf": self.capital_discipline_fcf,
            "valuation_4b_room": self.valuation_4b_room,
        }


@dataclass(frozen=True)
class Round173ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round173ScoreWeightDraft
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
        return Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round173CaseCandidate:
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
class Round173BaseScoreWeight:
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
class Round173StageCap:
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
class Round173ScoreStagePriceAlignment:
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


ROUND173_BASE_SCORE_WEIGHTS: tuple[Round173BaseScoreWeight, ...] = (
    Round173BaseScoreWeight("eps_fcf_opm_conversion", 24, "keep_high", "AI semiconductor candidates need OP/EPS/FCF conversion, not keyword exposure."),
    Round173BaseScoreWeight("customer_contract_shipment_visibility", 22, "raise_detail_requirement", "Customer name, contract amount, shipment schedule, repeat orders, and diversification drive Stage 2/3."),
    Round173BaseScoreWeight("bottleneck_pricing_power", 18, "keep_high", "HBM bonder, AI server PCB, test socket, and foundry capacity bottlenecks matter only when revenue conversion is visible."),
    Round173BaseScoreWeight("early_price_path_validation", 12, "new_loop11_axis", "Stage 2 must be tested against 60D/120D MFE before a late 4B crowding call."),
    Round173BaseScoreWeight("information_confidence_disclosure_detail", 8, "hard_review", "Media reports, MOU, private-company linkage, and missing customer details cap Stage 3."),
    Round173BaseScoreWeight("capital_discipline_fcf_stability", 6, "watch", "Capex, dilution, customer concentration, and FCF drag can cool equipment and component stories."),
    Round173BaseScoreWeight("valuation_room_4b_runway", 10, "raise_4b_focus", "Large semiconductor reratings must be cooled when price outruns revisions or narratives crowd."),
)


ROUND173_STAGE_CAPS: tuple[Round173StageCap, ...] = (
    Round173StageCap(
        "Stage 1",
        "45",
        ("hbm", "ai_server", "cxl", "glass_substrate", "on_device_ai", "npu", "system_semi", "pcb_or_test_theme"),
        ("on_device_ai_revenue_missing_case",),
        "Theme keywords route research only. Green is blocked before customer, shipment, revenue, and OP/EPS evidence.",
    ),
    Round173StageCap(
        "Stage 2",
        "70",
        ("customer_name", "contract_amount", "shipment_schedule", "government_investment", "technology_license", "mou_or_report"),
        ("db_hitek_foundry_reram_stage2_case", "rebellions_sapeon_related_stock_green_cap_case"),
        "Stage 2 can include policy/license/private AI-chip ecosystem evidence, but Stage 3 waits for listed-company earnings link.",
    ),
    Round173StageCap(
        "Stage 2.5",
        "watch",
        ("quality_business", "early_price_path", "ai_testing_or_pcb_exposure", "op_eps_detail_missing"),
        ("leeno_ai_test_socket_stage25_case",),
        "Useful diagnostic watch band, not a canonical Stage change and not Stage 3-Green.",
    ),
    Round173StageCap(
        "Stage 3",
        "requires_4_of_7",
        ("op_eps_revision_or_beat", "confirmed_customer_contract_terms", "revenue_conversion", "customer_diversification", "60d_mfe_20pct", "relative_strength", "valuation_not_peer_top_quartile"),
        ("hanmi_hbm_bonder_stage3_4b_case",),
        "Stage 3 is possible when earnings, customer terms, bottleneck revenue conversion, price path, and valuation room mostly align.",
    ),
    Round173StageCap(
        "Stage 4B",
        "requires_3_of_5",
        ("stage2_120d_mfe_80pct", "stage3_252d_mfe_150pct", "price_300_500pct", "narrative_before_earnings", "keyword_crowding"),
        ("isu_petasys_ai_server_pcb_487pct_4b_case", "hanmi_micron_media_report_not_contract_case"),
        "Good logic is cooled when price and AI narrative crowding outrun OP/EPS revision.",
    ),
    Round173StageCap(
        "Stage 4C",
        "hard_gate",
        ("mou_or_media_report_mistaken_for_contract", "customer_order_cancel", "dilution_cb_bw", "audit_disclosure_issue", "single_customer_capex_cut", "shipment_delay", "op_eps_revision_down", "direct_earnings_link_missing"),
        ("samsung_labor_disruption_overlay_case", "ai_chip_private_related_direct_revenue_missing_case"),
        "Hard RedTeam overrides AI/HBM narratives when contract, shipment, disclosure, or earnings linkage breaks.",
    ),
)


ROUND173_SCORE_STAGE_PRICE_ALIGNMENT: tuple[Round173ScoreStagePriceAlignment, ...] = (
    Round173ScoreStagePriceAlignment("hanmi_hbm_bonder_stage3_4b_case", "Stage 3 candidate + 4B-watch", "Micron media report and SK Hynix order created early price reaction; exact stage prices need KRX backfill", "stage3_catch_and_4b_cool_required", "credit confirmed customer contract; cap unconfirmed Micron report; reduce valuation room after rapid rally"),
    Round173ScoreStagePriceAlignment("isu_petasys_ai_server_pcb_487pct_4b_case", "Stage 3 candidate -> 4B-watch", "AI server PCB rerating can be real, but 487% reference move makes valuation runway limited", "structural_success_but_late_4b", "credit AI server PCB exposure before rerating; apply 4B haircut after 300-500% move"),
    Round173ScoreStagePriceAlignment("leeno_ai_test_socket_stage25_case", "Stage 2.5 -> Stage 3 candidate", "70% AI boom rally is attention, not Green without OP/EPS and socket demand detail", "quality_business_not_green_yet", "credit high-margin socket and testing exposure; cap Stage 3 before customer and revision data"),
    Round173ScoreStagePriceAlignment("db_hitek_foundry_reram_stage2_case", "Stage 1/2", "Policy foundry and ReRAM license are options, not wafer revenue", "policy_license_not_green", "credit policy and license; block Green before customer wafer revenue and OP/EPS revision"),
    Round173ScoreStagePriceAlignment("rebellions_sapeon_related_stock_green_cap_case", "Stage 1/2 event", "Private-company merger and government investment do not automatically flow into listed EPS", "listed_link_missing", "credit ecosystem event; require equity-method income, direct revenue, or customer shipment"),
    Round173ScoreStagePriceAlignment("hanmi_micron_media_report_not_contract_case", "Stage 2 + 4B-watch", "Possible Micron deal moved price but was not a finalized disclosed contract", "media_report_cap_correct", "treat as supporting evidence only until final contract terms are verified"),
    Round173ScoreStagePriceAlignment("samsung_labor_disruption_overlay_case", "4C overlay", "Labor disruption can hurt Samsung exposure and broader supply chain delivery reliability", "hard_redteam_alignment", "apply operational disruption overlay to delivery and execution confidence"),
    Round173ScoreStagePriceAlignment("on_device_ai_revenue_missing_case", "Stage 1/2", "On-device AI theme can move price before actual adoption revenue appears", "theme_without_revenue_blocked", "allow research routing; block Green before design-win revenue and OP/EPS revision"),
    Round173ScoreStagePriceAlignment("hbm_test_equipment_stage2_case", "Stage 2", "HBM test narrative needs actual customer orders, shipment schedule, and OP/EPS conversion", "equipment_watch_not_green_yet", "credit HBM test bottleneck; cap before order and revision proof"),
    Round173ScoreStagePriceAlignment("ai_chip_private_related_direct_revenue_missing_case", "event premium / 4C gate", "Private valuation and listed-company price are separated until direct earnings link appears", "direct_earnings_gate_contains_false_green", "block Stage 3 when listed company has no direct revenue or equity-method income"),
)


def _weights(
    eps: int | str,
    visibility: int | str,
    bottleneck: int | str,
    price: int | str,
    confidence: int | str,
    capital: int | str,
    valuation: int | str,
) -> Round173ScoreWeightDraft:
    return Round173ScoreWeightDraft(eps, visibility, bottleneck, price, confidence, capital, valuation)


ROUND173_SCORE_TARGETS: tuple[Round173ScoreTarget, ...] = (
    Round173ScoreTarget(
        "HBM_BONDER_EQUIPMENT_KOREA",
        E2RArchetype.HBM_BONDER_EQUIPMENT_KOREA,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(24, 22, 20, 12, 8, 6, 8),
        ("hbm_demand", "tc_bonder", "advanced_packaging_equipment", "hbm_packaging_bottleneck"),
        ("sk_hynix_contract", "contract_value", "recent_contract_sum", "micron_potential_customer"),
        ("op_eps_revision", "customer_diversification", "repeat_orders", "equipment_margin", "60d_mfe_20pct"),
        ("rapid_rally", "hbm_bonder_consensus_crowded", "valuation_peer_top_quartile"),
        ("micron_report_not_finalized", "customer_order_delay", "margin_miss", "single_customer_concentration"),
        ("confirmed_contract", "customer_diversification", "op_eps_revision", "equipment_margin", "price_path_aligned"),
        ("unconfirmed_media_report", "valuation_crowding", "single_customer", "shipment_delay"),
        ("unconfirmed_report", "valuation_crowding", "customer_concentration"),
        "Hanmi-style HBM bonder can be Stage 3-capable, but unconfirmed customer reports and rapid rerating create 4B/cap pressure.",
    ),
    Round173ScoreTarget(
        "ADVANCED_PACKAGING_EQUIPMENT_KOREA",
        E2RArchetype.ADVANCED_PACKAGING_EQUIPMENT_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(22, 21, 18, 11, 8, 6, 8),
        ("advanced_packaging", "post_process_tool", "hbm_packaging", "customer_capex"),
        ("customer_order", "shipment_schedule", "equipment_revenue_conversion", "customer_qualification"),
        ("repeat_order", "op_eps_revision", "customer_diversification", "margin_visible"),
        ("packaging_tool_theme_crowded", "order_priced_before_shipment"),
        ("customer_capex_cut", "qualification_delay", "shipment_delay", "order_pushout"),
        ("orders", "shipment", "revenue_conversion", "op_eps_revision"),
        ("customer_order_missing", "shipment_delay", "qualification_delay", "capex_cut"),
        ("order_visibility", "shipment_schedule", "customer_capex"),
        "Advanced packaging equipment stays Watch-to-Green; actual customer orders and shipment-to-revenue conversion gate conviction.",
    ),
    Round173ScoreTarget(
        "AI_SERVER_PCB_MLB_KOREA",
        E2RArchetype.AI_SERVER_PCB_MLB_KOREA,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(23, 22, 18, 12, 8, 6, 7),
        ("ai_server_pcb", "high_layer_mlb", "accelerator_board", "data_center_networking_board"),
        ("ai_server_exposure", "order_visibility", "capacity_expansion", "customer_qualification"),
        ("high_layer_mlb_revenue", "op_eps_revision", "customer_diversification", "pricing_power"),
        ("price_300_500pct", "pcb_consensus_crowded", "valuation_saturation"),
        ("customer_concentration", "inventory_build", "order_delay", "op_eps_revision_down"),
        ("order_visibility", "op_eps_revision", "customer_diversification", "capacity_constraint", "price_path_aligned"),
        ("customer_detail_missing", "valuation_crowding", "inventory", "single_customer"),
        ("price_300_500pct", "customer_concentration", "inventory"),
        "AI server PCB can be a real rerating path before a large move; after a 300-500% move it becomes 4B-watch unless revisions keep up.",
    ),
    Round173ScoreTarget(
        "SEMICONDUCTOR_TEST_SOCKET_KOREA",
        E2RArchetype.SEMICONDUCTOR_TEST_SOCKET_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(22, 20, 16, 11, 8, 6, 9),
        ("ai_chip_testing", "test_socket", "probe_pin", "high_frequency_socket"),
        ("customer_qualification", "socket_mix_improvement", "ai_chip_testing_exposure", "early_price_path"),
        ("op_eps_revision", "high_margin_socket_mix", "repeat_order", "customer_detail_verified"),
        ("ai_test_socket_multiple_crowded", "price_70pct_before_detail"),
        ("customer_detail_missing", "order_delay", "op_eps_revision_missing", "valuation_crowding"),
        ("high_margin_socket", "op_eps_revision", "repeat_order", "customer_detail"),
        ("customer_detail_missing", "revision_missing", "valuation_crowding"),
        ("valuation_crowding", "customer_detail_missing"),
        "High-quality test socket names can be Stage 2.5/3 candidates, but price reaction alone cannot create Green.",
    ),
    Round173ScoreTarget(
        "HBM_TEST_EQUIPMENT_KOREA",
        E2RArchetype.HBM_TEST_EQUIPMENT_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(22, 21, 18, 11, 8, 6, 8),
        ("hbm_test", "cube_prober", "memory_test_handler", "wafer_level_test"),
        ("actual_customer_order", "shipment_schedule", "test_equipment_backlog", "hbm_test_exposure"),
        ("customer_order_conversion", "op_eps_revision", "shipment_to_revenue", "margin_visible"),
        ("test_equipment_theme_crowded", "order_priced_before_delivery"),
        ("order_missing", "shipment_delay", "customer_capex_cut", "op_eps_revision_down"),
        ("customer_order", "shipment_schedule", "op_eps_revision", "margin_visible"),
        ("actual_order_missing", "shipment_delay", "single_customer", "capex_cut"),
        ("order_missing", "shipment_delay", "customer_capex"),
        "HBM test equipment is a Stage 2 watch until customer order, shipment, and OP/EPS conversion are explicit.",
    ),
    Round173ScoreTarget(
        "SYSTEM_SEMI_FOUNDARY_OPTION_KOREA",
        E2RArchetype.SYSTEM_SEMI_FOUNDARY_OPTION_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(18, 18, 12, 9, 8, 6, 9),
        ("system_semi_policy", "foundry_support", "legacy_chip", "reram_license"),
        ("government_foundry_plan", "technology_license", "tapeout_option", "fabless_support"),
        ("customer_wafer_revenue", "utilization_improvement", "op_eps_revision", "mass_production_revenue"),
        ("policy_option_priced", "technology_license_fully_priced"),
        ("customer_revenue_missing", "op_eps_revision_missing", "policy_delay", "license_not_commercialized"),
        ("customer_wafer_revenue", "utilization", "op_eps_revision", "commercial_revenue"),
        ("policy_only", "technology_license_only", "revenue_missing", "revision_missing"),
        ("policy_only", "license_only", "customer_revenue_missing"),
        "Policy and ReRAM license are Stage 1/2 options. Stage 3 waits for wafer revenue, utilization, and OP/EPS evidence.",
    ),
    Round173ScoreTarget(
        "AI_CHIP_FABRIC_PRIVATE_RELATED",
        E2RArchetype.AI_CHIP_FABRIC_PRIVATE_RELATED,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights(14, 14, 12, 8, 8, 6, 6),
        ("private_ai_chip", "npu", "rebellions", "sapeon", "government_investment"),
        ("private_company_merger", "mass_production", "government_investment", "related_listed_company"),
        ("listed_company_direct_revenue", "equity_method_income", "customer_contract", "repeat_shipment"),
        ("related_stock_price_priced_before_eps", "private_valuation_crowded"),
        ("direct_earnings_link_missing", "related_stock_only", "mou_only", "shipment_missing"),
        ("direct_revenue", "equity_method_income", "customer_contract", "shipment"),
        ("direct_earnings_link_missing", "private_valuation_only", "related_stock_only"),
        ("direct_link_missing", "private_valuation", "related_stock_only"),
        "Private AI-chip ecosystem evidence can route research, but listed-company Stage 3 requires direct revenue or equity-method link.",
    ),
    Round173ScoreTarget(
        "ON_DEVICE_AI_THEME",
        E2RArchetype.ON_DEVICE_AI_THEME,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights(16, 14, 10, 10, 8, 6, 6),
        ("on_device_ai", "npu", "smartphone_ai", "edge_ai", "cxl_or_low_power_memory_theme"),
        ("design_win", "adoption_signal", "technical_license", "customer_pilot"),
        ("design_win_revenue", "op_eps_revision", "repeat_customer_order", "customer_detail_verified"),
        ("on_device_ai_theme_crowded", "price_only_theme"),
        ("adoption_missing", "direct_revenue_missing", "op_eps_revision_missing", "customer_detail_missing"),
        ("design_win_revenue", "customer_order", "op_eps_revision"),
        ("theme_only", "direct_revenue_missing", "adoption_missing"),
        ("theme_only", "revenue_missing", "customer_missing"),
        "On-device AI is research routing until actual design-win revenue and revisions appear.",
    ),
    Round173ScoreTarget(
        "MOU_OR_REPORT_NOT_CONTRACT",
        E2RArchetype.MOU_OR_REPORT_NOT_CONTRACT,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("cap", "cap", "cap", "cap", "cap", "cap", "cap"),
        ("media_report", "mou", "loi", "possible_deal", "if_finalized"),
        ("report_or_negotiation_confirmed", "details_unconfirmed"),
        ("not_green_until_final_contract_customer_amount_delivery_margin_visible",),
        ("report_priced_as_contract", "headline_rally"),
        ("final_contract_missing", "customer_unknown", "amount_unknown", "delivery_unknown", "margin_unknown"),
        (),
        ("final_contract_missing", "unconfirmed_report", "terms_undisclosed"),
        ("mou_or_report_only", "detail_missing", "customer_unknown"),
        "Media reports, MOU, or possible deals are supporting Stage 2 evidence only. They cannot create Stage 3-Green.",
        hard_gate=True,
    ),
    Round173ScoreTarget(
        "DISCLOSURE_CONFIDENCE_CAP",
        E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("cap", "cap", "cap", "cap", "+", "cap", "cap"),
        ("opendart_list_only", "contract_headline", "high_signal_disclosure", "ai_component_report"),
        ("detail_fetched", "contract_amount", "counterparty", "delivery_schedule", "margin_detail"),
        ("multi_source_confirmation", "contract_terms_verified", "shipment_or_revenue_detail", "margin_visible"),
        ("undisclosed_ai_contract_theme_crowded",),
        ("detail_missing", "contract_amount_missing", "customer_missing", "duration_missing", "margin_unknown"),
        ("contract_terms", "customer_name", "shipment_schedule", "margin_visible"),
        ("detail_missing", "contract_terms_missing", "customer_missing", "margin_unknown"),
        ("disclosure_confidence_capped", "detail_missing"),
        "OpenDART list-only or headline-only evidence cannot support Stage 3-Green.",
    ),
    Round173ScoreTarget(
        "HBM_SUPPLY_CHAIN_LABOR_DISRUPTION_OVERLAY",
        E2RArchetype.HBM_SUPPLY_CHAIN_LABOR_DISRUPTION_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("gate", "gate", "gate", "gate", "gate", "gate", "gate"),
        ("labor_strike", "memory_supply_disruption", "bonus_gap", "foundry_logic_execution_risk"),
        ("strike_notice", "production_disruption_risk", "delivery_delay_risk"),
        ("not_green_until_disruption_resolved_and_delivery_evidence_recovered",),
        ("positive_supply_chain_story_ignores_labor_gate",),
        ("labor_strike", "delivery_delay", "execution_risk", "customer_supply_disruption", "op_eps_revision_down"),
        ("labor_resolved", "delivery_normalized", "customer_supply_confirmed"),
        ("labor_disruption", "delivery_delay", "execution_risk"),
        ("labor_disruption", "delivery_delay", "execution_risk"),
        "Samsung labor and execution risk is a hard operational overlay for exposed supply-chain candidates.",
        hard_gate=True,
    ),
    Round173ScoreTarget(
        "AI_CHIP_LISTED_EARNINGS_LINK_GATE",
        E2RArchetype.AI_CHIP_LISTED_EARNINGS_LINK_GATE,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("gate", "gate", "gate", "gate", "gate", "gate", "gate"),
        ("private_ai_chip_related_stock", "private_valuation", "listed_parent_or_partner"),
        ("linkage_claimed", "investment_or_merger_news"),
        ("not_green_until_direct_revenue_or_equity_method_income",),
        ("private_valuation_priced_into_listed_stock",),
        ("direct_earnings_link_missing", "revenue_missing", "equity_method_income_missing", "customer_contract_missing"),
        ("direct_revenue", "equity_method_income", "customer_contract", "repeat_shipment"),
        ("direct_earnings_link_missing", "private_valuation_only", "related_stock_only"),
        ("direct_earnings_link_missing", "private_valuation_only", "related_stock_only"),
        "Private AI-chip news must not be translated into listed-company Green without direct earnings linkage.",
        hard_gate=True,
    ),
)


ROUND173_CASE_CANDIDATES: tuple[Round173CaseCandidate, ...] = (
    Round173CaseCandidate(
        "hanmi_hbm_bonder_stage3_4b_case",
        "HBM_BONDER_EQUIPMENT_KOREA",
        "042700",
        "한미반도체",
        "KR",
        "structural_success",
        None,
        None,
        None,
        None,
        None,
        ("hbm_packaging_equipment", "sk_hynix_contract", "contract_value_21_48bn_krw", "recent_contract_sum_200bn_krw", "micron_potential_customer", "intraday_price_reaction_22pct"),
        ("micron_report_not_finalized", "unconfirmed_media_report", "valuation_crowding", "single_customer_concentration"),
        "stage3_candidate_plus_4b_watch_needs_exact_source_date_and_krx_backfill",
        "needs_source_date_backfill",
        ("round_173.md WSJ Hanmi / Micron possible deal",),
        "HBM bonder equipment can be Stage 3-capable when confirmed customer contracts, OP/EPS revision, and price path align; unconfirmed Micron report caps Green.",
        (E2RArchetype.ADVANCED_PACKAGING_EQUIPMENT_KOREA, E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH),
    ),
    Round173CaseCandidate(
        "isu_petasys_ai_server_pcb_487pct_4b_case",
        "AI_SERVER_PCB_MLB_KOREA",
        "007660",
        "이수페타시스",
        "KR",
        "4b_watch",
        None,
        None,
        None,
        None,
        None,
        ("ai_server_pcb", "high_layer_mlb", "accelerator_board", "data_center_networking_board", "stock_surge_487pct"),
        ("valuation_saturation", "customer_detail_missing", "price_300_500pct", "op_eps_revision_must_continue"),
        "ai_server_pcb_success_but_487pct_move_requires_4b_watch",
        "needs_price_backfill",
        ("round_173.md Isu Group / Bloomberg-Yahoo 487% stock surge reference",),
        "AI server PCB can be a real rerating path, but after a 487% move the system must cool it to 4B unless revisions keep up.",
        (E2RArchetype.ADVANCED_PACKAGING_PCB, E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH),
    ),
    Round173CaseCandidate(
        "leeno_ai_test_socket_stage25_case",
        "SEMICONDUCTOR_TEST_SOCKET_KOREA",
        "058470",
        "리노공업",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("test_socket", "probe_pin", "ai_chip_testing", "high_margin_socket", "ai_boom_price_up_70pct"),
        ("customer_detail_missing", "op_eps_revision_missing", "valuation_crowding"),
        "quality_business_stage2_5_not_green_until_socket_revenue_revision",
        "needs_price_backfill",
        ("round_173.md Lee Chae-yoon / Leeno AI stock rally reference",),
        "High-margin test socket quality can justify Stage 2.5, but Stage 3 needs customer detail, socket mix, and OP/EPS revision.",
        (E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH,),
    ),
    Round173CaseCandidate(
        "db_hitek_foundry_reram_stage2_case",
        "SYSTEM_SEMI_FOUNDARY_OPTION_KOREA",
        "000990",
        "DB하이텍",
        "KR",
        "success_candidate",
        date(2025, 12, 10),
        date(2025, 12, 10),
        None,
        None,
        None,
        ("government_12inch_40nm_foundry_plan", "fabless_support", "reram_license", "compute_in_memory_project_option"),
        ("customer_revenue_missing", "op_eps_revision_missing", "policy_delay", "license_not_commercialized"),
        "policy_and_reram_option_stage2_not_green",
        "needs_price_backfill",
        ("round_173.md Reuters South Korea 40nm foundry plan", "round_173.md Weebit Nano / DB HiTek ReRAM context"),
        "Government foundry policy and ReRAM license are options. Stage 3 waits for wafer revenue, utilization, and OP/EPS revision.",
        (E2RArchetype.COMMODITY_MEMORY_GENERAL_SEMI,),
    ),
    Round173CaseCandidate(
        "rebellions_sapeon_related_stock_green_cap_case",
        "AI_CHIP_FABRIC_PRIVATE_RELATED",
        "017670/030200",
        "SK텔레콤·KT 관련 AI칩 노출",
        "KR",
        "event_premium",
        date(2024, 6, 12),
        date(2026, 3, 26),
        None,
        None,
        None,
        ("rebellions_sapeon_merger", "atom_mass_production", "government_investment_250bn_krw", "private_ai_chip_ecosystem"),
        ("listed_company_direct_revenue_missing", "equity_method_income_missing", "related_stock_only", "private_valuation_only"),
        "private_ai_chip_ecosystem_event_not_listed_company_green",
        "needs_price_backfill",
        ("round_173.md Reuters Rebellions-Sapeon merger", "round_173.md Reuters Korea investment in Rebellions"),
        "Private AI-chip ecosystem evidence can move related stocks, but listed-company Green requires direct revenue or equity-method income.",
        (E2RArchetype.AI_CHIP_LISTED_EARNINGS_LINK_GATE,),
    ),
    Round173CaseCandidate(
        "hanmi_micron_media_report_not_contract_case",
        "MOU_OR_REPORT_NOT_CONTRACT",
        "042700",
        "한미반도체 Micron 보도",
        "KR",
        "event_premium",
        None,
        None,
        None,
        None,
        None,
        ("micron_possible_deal_report", "if_finalized_language", "price_reaction_22pct", "sk_hynix_confirmed_order_as_separate_evidence"),
        ("final_contract_missing", "terms_undisclosed", "customer_confirmation_missing", "headline_rally"),
        "media_report_stage2_supporting_evidence_not_contract",
        "needs_source_date_backfill",
        ("round_173.md WSJ Hanmi / Micron possible deal",),
        "Possible Micron deal is strong Stage 2 attention but not a finalized customer contract before disclosure detail.",
        (E2RArchetype.HBM_BONDER_EQUIPMENT_KOREA, E2RArchetype.DISCLOSURE_CONFIDENCE_CAP),
    ),
    Round173CaseCandidate(
        "samsung_labor_disruption_overlay_case",
        "HBM_SUPPLY_CHAIN_LABOR_DISRUPTION_OVERLAY",
        "005930",
        "삼성전자 파업·생산차질 overlay",
        "KR",
        "4c_thesis_break",
        date(2026, 5, 15),
        None,
        None,
        None,
        date(2026, 5, 15),
        ("strike_notice", "memory_supply_chain_disruption_risk", "45000_plus_workers", "division_bonus_gap", "foundry_logic_execution_risk"),
        ("labor_strike", "delivery_delay_risk", "execution_risk", "op_eps_revision_down_risk"),
        "hbm_supply_chain_operational_overlay",
        "needs_price_backfill",
        ("round_173.md Reuters Samsung looming strike / AI boom divisions",),
        "Samsung is not a central success case here, but labor and execution risk must remain a semiconductor supply-chain RedTeam overlay.",
        (E2RArchetype.HBM_CATCHUP_EXECUTION_RISK,),
    ),
    Round173CaseCandidate(
        "on_device_ai_revenue_missing_case",
        "ON_DEVICE_AI_THEME",
        "080220/094360/054450",
        "온디바이스 AI 관련주",
        "KR",
        "event_premium",
        None,
        None,
        None,
        None,
        None,
        ("on_device_ai_theme", "npu_or_low_power_memory_theme", "design_win_watch", "price_only_theme_risk"),
        ("direct_revenue_missing", "adoption_missing", "customer_detail_missing", "op_eps_revision_missing"),
        "theme_routes_research_but_green_blocked_before_revenue",
        "needs_case_backfill",
        ("round_173.md On-device AI related stock warning",),
        "On-device AI can route research, but direct adoption revenue and OP/EPS revision are required before Stage 3.",
        (E2RArchetype.AI_CHIP_LISTED_EARNINGS_LINK_GATE,),
    ),
    Round173CaseCandidate(
        "hbm_test_equipment_stage2_case",
        "HBM_TEST_EQUIPMENT_KOREA",
        "089030/003160/232140",
        "테크윙·디아이·와이씨 HBM 테스트 장비",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("hbm_test", "cube_prober", "memory_test_handler", "wafer_level_test", "actual_customer_order_needed"),
        ("actual_customer_order_missing", "shipment_schedule_missing", "op_eps_revision_missing", "customer_capex_cut"),
        "hbm_test_stage2_until_customer_order_shipment_revision",
        "needs_case_backfill",
        ("round_173.md HBM test equipment target list",),
        "HBM test equipment is a watch path, but customer order, shipment schedule, and OP/EPS conversion are mandatory.",
        (E2RArchetype.SEMI_EQUIPMENT_AI_CAPEX,),
    ),
    Round173CaseCandidate(
        "advanced_packaging_equipment_customer_order_case",
        "ADVANCED_PACKAGING_EQUIPMENT_KOREA",
        "053610/031980",
        "프로텍·피에스케이홀딩스 후공정 장비",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("advanced_packaging_equipment", "customer_order_needed", "shipment_schedule_needed", "equipment_revenue_conversion_needed"),
        ("customer_order_missing", "qualification_delay", "shipment_delay", "margin_unknown"),
        "advanced_packaging_stage2_before_customer_order_conversion",
        "needs_case_backfill",
        ("round_173.md Advanced packaging equipment target list",),
        "Advanced packaging equipment can become Stage 2/3, but only after customer order, shipment, and margin evidence.",
        (E2RArchetype.SEMI_EQUIPMENT_AI_CAPEX,),
    ),
    Round173CaseCandidate(
        "ai_chip_private_related_direct_revenue_missing_case",
        "AI_CHIP_LISTED_EARNINGS_LINK_GATE",
        "017670/030200",
        "국산 AI칩 private 관련주 earnings-link gate",
        "KR",
        "4c_thesis_break",
        date(2024, 6, 12),
        date(2026, 3, 26),
        None,
        None,
        None,
        ("private_ai_chip_merger", "government_investment", "related_listed_company_claim"),
        ("direct_earnings_link_missing", "direct_revenue_missing", "equity_method_income_missing", "customer_contract_missing"),
        "private_valuation_and_listed_eps_must_be_separated",
        "needs_price_backfill",
        ("round_173.md Reuters Rebellions-Sapeon merger", "round_173.md Reuters Rebellions investment"),
        "This is the hard gate version of the private AI-chip related-stock rule.",
        (E2RArchetype.AI_CHIP_FABRIC_PRIVATE_RELATED,),
    ),
)


ROUND173_PRICE_FIELDS: tuple[str, ...] = (
    "case_id",
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
    "peak_price",
    "peak_date",
    "return_20d_after_stage2",
    "return_60d_after_stage2",
    "return_120d_after_stage2",
    "return_252d_after_stage2",
    "return_20d_after_stage3",
    "return_60d_after_stage3",
    "return_120d_after_stage3",
    "return_252d_after_stage3",
    "mfe_60d_after_stage2",
    "mae_60d_after_stage2",
    "mfe_120d_after_stage2",
    "mae_120d_after_stage2",
    "mfe_252d_after_stage2",
    "mae_252d_after_stage2",
    "relative_strength_vs_kospi",
    "relative_strength_vs_kosdaq",
    "relative_strength_vs_semiconductor_basket",
    "valuation_at_stage3",
    "valuation_at_stage4b",
    "op_revision_before_stage3",
    "op_revision_after_stage3",
    "eps_revision_before_stage3",
    "eps_revision_after_stage3",
    "contract_amount",
    "contract_counterparty",
    "contract_period",
    "contract_amount_to_prior_sales",
    "customer_name",
    "customer_diversification_flag",
    "shipment_schedule",
    "equipment_order_value",
    "equipment_revenue_conversion_flag",
    "hbm_bonder_flag",
    "tc_bonder_flag",
    "sk_hynix_contract_flag",
    "micron_potential_customer_flag",
    "micron_final_contract_flag",
    "recent_contract_sum_krw",
    "ai_server_pcb_flag",
    "high_layer_mlb_flag",
    "stock_surge_300_500pct_flag",
    "test_socket_flag",
    "probe_pin_flag",
    "high_margin_socket_mix_flag",
    "hbm_test_equipment_flag",
    "cube_prober_flag",
    "memory_test_handler_flag",
    "system_foundry_policy_flag",
    "reram_license_flag",
    "customer_wafer_revenue_flag",
    "private_ai_chip_flag",
    "rebellions_sapeon_merger_flag",
    "government_investment_amount_krw",
    "listed_company_direct_revenue_flag",
    "equity_method_income_flag",
    "on_device_ai_flag",
    "design_win_revenue_flag",
    "media_report_only_flag",
    "mou_flag",
    "final_contract_missing_flag",
    "disclosure_confidence",
    "opendart_rcept_no",
    "opendart_detail_fetched_flag",
    "detail_parser_confidence",
    "labor_strike_flag",
    "delivery_delay_risk_flag",
    "customer_concentration_flag",
    "dilution_type",
    "cb_bw_issuance_flag",
    "audit_issue_flag",
    "stage_before_redteam",
    "stage_after_redteam",
    "score_before_redteam",
    "score_after_redteam",
    "score_price_alignment",
    "price_validation_status",
    "review_notes",
)


def round173_target_for(target_id: str) -> Round173ScoreTarget | None:
    for target in ROUND173_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round173_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND173_CASE_CANDIDATES:
        target = round173_target_for(candidate.target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {candidate.target_id}")
        weights = target.score_weight.as_dict()
        stage4b_evidence = candidate.evidence_fields if candidate.case_type == "4b_watch" or candidate.stage4b_date else ()
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
                f"Round173 R2 Loop-11 Korea AI/semiconductor/electronics case for {candidate.target_id}; "
                "calibration-only and focused on Stage 3 early catch plus 4B/4C cooling."
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
            score_price_alignment=_round173_score_price_alignment(candidate),
            rerating_result=_round173_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
            score_weight_hint={
                "eps_fcf": _numeric_weight(weights["eps_fcf_opm"]),
                "visibility": _numeric_weight(weights["customer_contract_shipment_visibility"]),
                "bottleneck": _numeric_weight(weights["bottleneck_pricing"]),
                "early_price_validation": _numeric_weight(weights["early_price_validation"]),
                "information_confidence": _numeric_weight(weights["information_confidence"]),
                "capital_discipline_fcf": _numeric_weight(weights["capital_discipline_fcf"]),
                "valuation_4b_room": _numeric_weight(weights["valuation_4b_room"]),
            },
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "require_customer_contract_shipment_revenue_and_revision_for_green",
                "stage3_early_catch_requires_4_of_7_loop11_conditions",
                "stage4b_cooling_requires_3_of_5_loop11_conditions",
                "do_not_invent_contract_dates_prices_margins_customers_or_shipments",
                "mou_media_report_private_valuation_and_theme_do_not_create_green",
                "direct_listed_company_earnings_link_required_for_private_ai_chip_related_stocks",
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


def round173_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND173_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "eps_fcf_opm": str(weights["eps_fcf_opm"]),
                "customer_contract_shipment_visibility": str(weights["customer_contract_shipment_visibility"]),
                "bottleneck_pricing": str(weights["bottleneck_pricing"]),
                "early_price_validation": str(weights["early_price_validation"]),
                "information_confidence": str(weights["information_confidence"]),
                "capital_discipline_fcf": str(weights["capital_discipline_fcf"]),
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


def round173_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND173_CASE_CANDIDATES:
        target = round173_target_for(candidate.target_id)
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


def round173_stage_date_rows() -> tuple[dict[str, str], ...]:
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
        for target in ROUND173_SCORE_TARGETS
    )


def round173_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round173_backfill": "true"} for field in ROUND173_PRICE_FIELDS)


def round173_base_score_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(weight.as_row() for weight in ROUND173_BASE_SCORE_WEIGHTS)


def round173_stage_cap_rows() -> tuple[dict[str, str], ...]:
    return tuple(cap.as_row() for cap in ROUND173_STAGE_CAPS)


def round173_score_stage_price_alignment_rows() -> tuple[dict[str, str], ...]:
    return tuple(row.as_row() for row in ROUND173_SCORE_STAGE_PRICE_ALIGNMENT)


def round173_summary() -> dict[str, int | bool]:
    records = round173_case_records()
    return {
        "target_count": len(ROUND173_SCORE_TARGETS),
        "source_canonical_target_count": ROUND173_SOURCE_CANONICAL_TARGET_COUNT,
        "case_candidate_count": len(records),
        "base_score_component_count": len(ROUND173_BASE_SCORE_WEIGHTS),
        "stage_cap_count": len(ROUND173_STAGE_CAPS),
        "score_stage_price_alignment_count": len(ROUND173_SCORE_STAGE_PRICE_ALIGNMENT),
        "structural_success_count": sum(1 for record in records if record.case_type == "structural_success"),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND173_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND173_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND173_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "hard_gate_target_count": sum(1 for target in ROUND173_SCORE_TARGETS if target.hard_gate),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round173_r2_loop11_reports(
    *,
    output_directory: str | Path = ROUND173_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND173_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND173_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round173_r2_loop11_ai_semiconductor_electronics_summary.md",
        "case_matrix": output / "round173_r2_loop11_case_matrix.csv",
        "stage_date_plan": output / "round173_r2_loop11_stage_date_plan.csv",
        "green_guardrails": output / "round173_r2_loop11_green_guardrails.md",
        "loop11_risk_overlays": output / "round173_r2_loop11_risk_overlays.md",
        "price_validation_plan": output / "round173_r2_loop11_price_validation_plan.md",
        "price_fields": output / "round173_r2_loop11_price_fields.csv",
        "base_score_weights": output / "round173_r2_loop11_base_score_weights.csv",
        "stage_caps": output / "round173_r2_loop11_stage_caps.csv",
        "score_stage_price_alignment": output / "round173_r2_loop11_score_stage_price_alignment.csv",
        "score_stage_price_alignment_md": output / "round173_r2_loop11_score_stage_price_alignment.md",
    }
    _write_case_jsonl(round173_case_records(), cases)
    _write_rows(round173_score_profile_rows(), score_profiles)
    _write_rows(round173_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round173_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round173_price_field_rows(), paths["price_fields"])
    _write_rows(round173_base_score_weight_rows(), paths["base_score_weights"])
    _write_rows(round173_stage_cap_rows(), paths["stage_caps"])
    _write_rows(round173_score_stage_price_alignment_rows(), paths["score_stage_price_alignment"])
    paths["summary"].write_text(render_round173_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round173_green_guardrail_markdown(), encoding="utf-8")
    paths["loop11_risk_overlays"].write_text(render_round173_loop11_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round173_price_validation_plan_markdown(), encoding="utf-8")
    paths["score_stage_price_alignment_md"].write_text(render_round173_score_stage_price_alignment_markdown(), encoding="utf-8")
    return paths


def render_round173_summary_markdown() -> str:
    summary = round173_summary()
    lines = [
        "# Round-173 R2 Loop-11 Korea AI / Semiconductor / Electronics Summary",
        "",
        f"- source_round: `{ROUND173_SOURCE_ROUND_PATH}`",
        "- large_sector: `AI_SEMICONDUCTOR_ELECTRONICS`",
        "- loop: `R2 Loop 11 / v11.0`",
        f"- target_count: {summary['target_count']}",
        f"- source_canonical_target_count: {summary['source_canonical_target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- base_score_component_count: {summary['base_score_component_count']}",
        f"- stage_cap_count: {summary['stage_cap_count']}",
        f"- score_stage_price_alignment_count: {summary['score_stage_price_alignment_count']}",
        f"- structural_success_count: {summary['structural_success_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- failed_rerating_count: {summary['failed_rerating_count']}",
        f"- stage4b_case_count: {summary['stage4b_case_count']}",
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
        "- R2 Loop 11 is Korea-first and excludes the already overused central HBM / global AI success and warning cases from the center of this pack.",
        "- Loop 11 adds a hard early-catch question: could Hanmi, Isu Petasys, or Leeno have been found before the large price move?",
        "- Stage 3-Green remains strict. HBM, AI server PCB, test socket, NPU, CXL, or on-device AI keywords do not create Green by themselves.",
        "- The base score weights are EPS/FCF/OPM 24, customer/contract/shipment visibility 22, bottleneck/pricing 18, early price path 12, information confidence 8, capital/FCF 6, valuation/4B room 10.",
        "- Example: 한미반도체 can be Stage 3-capable from confirmed SK Hynix orders, but a Micron media report alone remains capped until final terms are verified.",
        "- Example: 이수페타시스 can be a successful AI server PCB case before rerating, but after a 487% reference move it becomes 4B-watch.",
        "- Example: DB하이텍 policy foundry and ReRAM license are Stage 1/2 options, not Stage 3-Green before wafer revenue.",
        "- Example: 리벨리온·사피온 related listed stocks need direct revenue or equity-method income before Stage 3.",
    ]
    return "\n".join(lines) + "\n"


def render_round173_green_guardrail_markdown() -> str:
    lines = [
        "# Round-173 R2 Loop-11 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Loop-11 penalties |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND173_SCORE_TARGETS:
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
            "- Do not apply R2 Loop-11 v11.0 weights to production scoring yet.",
            "- Do not lower Stage 3-Green thresholds because AI/HBM themes have strong price paths.",
            "- Do not use Round 173 case records as candidate-generation input.",
            "- Do not treat media reports, MOU, private valuation, government investment, policy option, or on-device AI theme as Green by itself.",
            "- Do not invent customer names, contract amounts, shipment schedules, margins, stage prices, MFE/MAE, or valuation bands.",
            "- Apply 4B-watch when price moves 300-500% or narrative crowds before revisions.",
            "- Apply 4C/hard review for direct earnings link missing, labor disruption, customer cancellation, dilution, disclosure failures, or shipment delay.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round173_loop11_risk_overlay_markdown() -> str:
    lines = [
        "# Round-173 R2 Loop-11 Risk Overlays",
        "",
        "- `EARLY_STAGE3_CATCH`: OP/EPS revision, confirmed customer terms, revenue conversion, customer diversification, 60D MFE, relative strength, and valuation room align.",
        "- `STAGE2_5_WATCH`: quality business and price reaction are above Stage 2 attention but below Stage 3 conviction.",
        "- `HBM_MEDIA_REPORT_CAP`: possible deal, if-finalized language, or media report is supporting evidence only.",
        "- `AI_SERVER_PCB_4B`: AI server PCB can be real, but 300-500% price paths require valuation-room haircut.",
        "- `TEST_SOCKET_DETAIL_CAP`: business quality is not enough without customer, mix, and OP/EPS detail.",
        "- `POLICY_LICENSE_NOT_REVENUE`: government foundry support or ReRAM license is not wafer revenue.",
        "- `PRIVATE_AI_CHIP_LISTED_LINK_GATE`: private AI-chip news cannot become listed-company Green without direct revenue or equity-method income.",
        "- `LABOR_DISRUPTION_4C_OVERLAY`: labor strike or execution disruption reduces delivery and disclosure confidence.",
        "- `DISCLOSURE_CONFIDENCE_CAPPED`: OpenDART list-only/headline evidence is capped until detail fields are parsed.",
        "",
        "Simple example: if `as_of_date=2024-03-01`, a possible Micron deal report can raise attention. A later finalized contract cannot be used on that date, and the possible-deal report itself cannot create Stage 3-Green.",
    ]
    return "\n".join(lines) + "\n"


def render_round173_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-173 R2 Loop-11 Price Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign Stage 1/2/3/4B/4C dates from dated source evidence only.",
        "2. Backfill KRX daily bars for `price_at_stage1` through `price_at_stage4c`.",
        "3. Calculate 20D/60D/120D/252D returns after Stage 2 and Stage 3.",
        "4. Calculate MFE/MAE after Stage 2, especially 60D/120D/252D.",
        "5. Compare price speed against OP/EPS revision speed to decide Stage 3 vs 4B-watch.",
        "6. Keep media-report-only, private-company-linkage, policy-license, and on-device-theme caps explicit.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | target | stage marker | check |",
        "| --- | --- | --- | --- |",
    ]
    for row in round173_case_candidate_rows():
        stage_date = row["stage4c_date"] or row["stage4b_date"] or row["stage3_date"] or row["stage2_date"] or row["stage1_date"] or "undated"
        lines.append(f"| `{row['case_id']}` | `{row['target_id']}` | {stage_date} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `stage3_catch_and_4b_cool_required`: the case should be detectable before a large move, then cooled when crowded.",
            "- `structural_success_but_late_4b`: structure was real, but current price path demands 4B monitoring.",
            "- `quality_business_not_green_yet`: high quality is watch evidence, not Green without revisions and customer detail.",
            "- `policy_license_not_green`: policy or license must become revenue before Stage 3.",
            "- `listed_link_missing`: private-company event does not equal listed-company earnings evidence.",
            "- `hard_redteam_alignment`: labor disruption, direct earnings link missing, or disclosure break correctly blocks positive narrative.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round173_score_stage_price_alignment_markdown() -> str:
    lines = [
        "# Round-173 R2 Loop-11 Score -> Stage -> Price Alignment",
        "",
        "## Base Score Weights",
        "",
        "| component | points | direction | reason |",
        "| --- | ---: | --- | --- |",
    ]
    for row in ROUND173_BASE_SCORE_WEIGHTS:
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
    for cap in ROUND173_STAGE_CAPS:
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
    for row in ROUND173_SCORE_STAGE_PRICE_ALIGNMENT:
        lines.append(
            f"| `{row.case_id}` | {row.detected_stage} | {row.price_path_status} | "
            f"{row.verdict} | {row.normalization_adjustment} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- 한미반도체 is the cleanest Korea R2 early Stage 3 / 4B-watch test, but media-report-only evidence is capped.",
            "- 이수페타시스 tests whether AI server PCB was catchable before a 300-500% move and cooled afterward.",
            "- 리노공업 uses Stage 2.5 as a diagnostic watch band, not a canonical Stage change.",
            "- DB하이텍 and 리벨리온·사피온 related stocks show why policy, license, private valuation, and related-stock narratives must not create Green without revenue.",
            "- 삼성 파업 overlay keeps operational disruption visible to RedTeam without turning it into a recommendation.",
        ]
    )
    return "\n".join(lines) + "\n"


def _round173_score_price_alignment(candidate: Round173CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "aligned"
    if candidate.case_type == "success_candidate":
        return "unknown"
    if candidate.case_type in {"event_premium", "4b_watch"}:
        return "price_moved_without_evidence"
    if candidate.case_type == "4c_thesis_break":
        return "false_positive_score"
    return "unknown"


def _round173_rerating_result(candidate: Round173CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "true_rerating"
    if candidate.case_type == "4b_watch":
        return "theme_overheat"
    if candidate.case_type == "event_premium":
        return "event_premium"
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    return "unknown"


def _numeric_weight(value: int | str) -> float:
    if isinstance(value, int):
        return float(value)
    if value in {"gate", "cap", "+"}:
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
    "ROUND173_BASE_SCORE_WEIGHTS",
    "ROUND173_CASE_CANDIDATES",
    "ROUND173_DEFAULT_CASES_PATH",
    "ROUND173_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND173_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND173_PRICE_FIELDS",
    "ROUND173_SCORE_STAGE_PRICE_ALIGNMENT",
    "ROUND173_SCORE_TARGETS",
    "ROUND173_SOURCE_CANONICAL_TARGET_COUNT",
    "ROUND173_SOURCE_CANONICAL_TARGET_IDS",
    "ROUND173_STAGE_CAPS",
    "Round173BaseScoreWeight",
    "Round173CaseCandidate",
    "Round173ScoreStagePriceAlignment",
    "Round173ScoreTarget",
    "Round173ScoreWeightDraft",
    "Round173StageCap",
    "render_round173_green_guardrail_markdown",
    "render_round173_loop11_risk_overlay_markdown",
    "render_round173_price_validation_plan_markdown",
    "render_round173_score_stage_price_alignment_markdown",
    "render_round173_summary_markdown",
    "round173_base_score_weight_rows",
    "round173_case_candidate_rows",
    "round173_case_records",
    "round173_price_field_rows",
    "round173_score_profile_rows",
    "round173_score_stage_price_alignment_rows",
    "round173_stage_cap_rows",
    "round173_stage_date_rows",
    "round173_summary",
    "round173_target_for",
    "write_round173_r2_loop11_reports",
]
