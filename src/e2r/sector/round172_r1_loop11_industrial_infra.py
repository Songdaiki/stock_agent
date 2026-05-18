"""Round-172 R1 Loop-11 Korea industrial orders and infrastructure pack.

Round 172 returns to R1 with a Korea-first calibration set. It does not add
production scoring. It captures the round note's stricter question: could the
system have found Stage 3 before the large rerating, and could it cool the
candidate into 4B/4C before the late-cycle story became crowded?
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


ROUND172_SOURCE_ROUND_PATH = "docs/round/round_172.md"
ROUND172_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round172_r1_loop11_industrial_infra"
ROUND172_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r1_loop11_round172.jsonl"
ROUND172_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round172_r1_loop11_v11.csv"
ROUND172_SOURCE_CANONICAL_TARGET_IDS: tuple[str, ...] = (
    "GRID_TRANSFORMER_SHORTAGE_KOREA",
    "GRID_US_LOCALIZATION_CAPA",
    "POWER_EQUIPMENT_BACKLOG_TO_FCF_KOREA",
    "SHIPBUILDING_US_PLATFORM_RESTRUCTURING",
    "SHIP_MRO_RECURRING_PLATFORM",
    "NUCLEAR_EXPORT_PREFERRED_BIDDER",
    "DEFENSE_AIRCRAFT_EXPORT_BACKLOG",
    "DEFENSE_INTERCEPTOR_COMBAT_VALIDATION",
    "GEOPOLITICAL_SHIPBUILDING_SANCTION_OVERLAY",
    "MOU_LOI_NOT_CONTRACT",
    "DISCLOSURE_CONFIDENCE_CAP",
)
ROUND172_SOURCE_CANONICAL_TARGET_COUNT = len(ROUND172_SOURCE_CANONICAL_TARGET_IDS)


@dataclass(frozen=True)
class Round172ScoreWeightDraft:
    eps_fcf_opm: int | str
    contract_visibility: int | str
    bottleneck_pricing: int | str
    early_price_validation: int | str
    capital_discipline: int | str
    disclosure_redteam: int | str
    valuation_4b_room: int | str

    def as_dict(self) -> dict[str, int | str]:
        return {
            "eps_fcf_opm": self.eps_fcf_opm,
            "contract_visibility": self.contract_visibility,
            "bottleneck_pricing": self.bottleneck_pricing,
            "early_price_validation": self.early_price_validation,
            "capital_discipline": self.capital_discipline,
            "disclosure_redteam": self.disclosure_redteam,
            "valuation_4b_room": self.valuation_4b_room,
        }


@dataclass(frozen=True)
class Round172ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round172ScoreWeightDraft
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
        return Round10LargeSector.INDUSTRIAL_ORDERS_INFRA

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round172CaseCandidate:
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
class Round172BaseScoreWeight:
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
class Round172StageCap:
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
class Round172ScoreStagePriceAlignment:
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


ROUND172_BASE_SCORE_WEIGHTS: tuple[Round172BaseScoreWeight, ...] = (
    Round172BaseScoreWeight("eps_fcf_opm_conversion", 24, "keep_high", "Stage 3 requires OP/EPS/FCF and margin conversion, not order headlines."),
    Round172BaseScoreWeight("contract_backlog_customer_visibility", 20, "detail_required", "Contract amount, customer, period, backlog quality, and delivery schedule define Stage 2."),
    Round172BaseScoreWeight("bottleneck_pricing_power", 18, "keep_high", "Transformer lead time, CAPA shortage, shipyard slots, defense production scale, and ASP/margin matter."),
    Round172BaseScoreWeight("early_price_path_validation", 12, "new_loop11_axis", "The score must catch early 60D/120D price validation before the candidate becomes crowded."),
    Round172BaseScoreWeight("capital_discipline_dilution", 8, "hard_review", "Capex, dilution, IPO premium, and acquisition funding can cool a good backlog story."),
    Round172BaseScoreWeight("disclosure_confidence_redteam", 8, "hard_review", "LOI/MOU, legal injunction, sanctions, missing detail, or OpenDART list-only evidence caps Stage 3."),
    Round172BaseScoreWeight("valuation_room_4b_runway", 10, "raise_4b_focus", "Good structures with large 120D/252D MFE become 4B-watch rather than fresh Green."),
)


ROUND172_STAGE_CAPS: tuple[Round172StageCap, ...] = (
    Round172StageCap(
        "Stage 1",
        "45",
        ("ai_power_demand", "us_grid_shortage", "shipbuilding_rebuild", "nuclear_export_news", "defense_rearmament", "government_policy"),
        ("hd_hyundai_mipo_loi_only_case",),
        "Green blocked until company-level contract/backlog or execution evidence appears.",
    ),
    Round172StageCap(
        "Stage 2",
        "70",
        ("contract_amount", "customer_name", "delivery_schedule", "backlog", "preferred_bidder", "loi_or_moa", "aircraft_contract"),
        ("doosan_czech_nuclear_preferred_bidder_case", "kai_fa50_philippines_stage2_case"),
        "Green blocked until OP/EPS/FCF, margin, and price path confirm.",
    ),
    Round172StageCap(
        "Stage 2.5",
        "watch",
        ("combat_validation", "early_price_path", "strong_demand_interest", "actual_contract_missing"),
        ("lig_nex1_cheongung_combat_validation_stage25_case", "hyosung_hico_hvdc_stage25_case"),
        "Useful watch band, but not a canonical Stage change and not Stage 3-Green.",
    ),
    Round172StageCap(
        "Stage 3",
        "requires_4_of_6",
        ("op_eps_revision_or_beat", "backlog_growth_and_long_delivery", "margin_improvement", "60d_mfe_20pct", "valuation_not_peer_top_quartile", "dart_detail_verified"),
        ("hd_hyundai_electric_transformer_stage3_4b_case",),
        "Stage 3 is early conviction only when earnings, backlog quality, margin, price path, valuation room, and detail confidence mostly line up.",
    ),
    Round172StageCap(
        "Stage 4B",
        "monitoring",
        ("stage2_120d_mfe_80pct", "stage3_252d_mfe_150pct", "crowded_reports", "peer_top_quartile_valuation", "price_faster_than_revision"),
        ("hd_hyundai_marine_solution_ipo_mro_case", "lig_nex1_cheongung_combat_validation_stage25_case"),
        "Good logic can be cooled when price and consensus have already run ahead.",
    ),
    Round172StageCap(
        "Stage 4C",
        "hard_gate",
        ("contract_cancel_or_correction", "dilution_cb_bw", "audit_or_disclosure_issue", "legal_or_competition_block", "sanction_or_export_control", "low_margin_order", "loi_failed_to_convert"),
        ("hanwha_ocean_china_sanction_4c_case", "doosan_czech_nuclear_legal_gate_case"),
        "Hard RedTeam overrides a positive R1 narrative.",
    ),
)


ROUND172_SCORE_STAGE_PRICE_ALIGNMENT: tuple[Round172ScoreStagePriceAlignment, ...] = (
    Round172ScoreStagePriceAlignment("hd_hyundai_electric_transformer_stage3_4b_case", "Stage 3 candidate + 4B-watch", "KRX bars must backfill 60D/120D/252D MFE and valuation room", "stage3_catch_and_4b_cool_required", "raise bottleneck/visibility, reduce valuation room after crowded rerating"),
    Round172ScoreStagePriceAlignment("hyosung_hico_hvdc_stage25_case", "Stage 2.5 -> Stage 3 candidate", "HICO/HVDC evidence strong; OP/EPS revision and price path still need backfill", "stage2_5_not_green_yet", "credit US localization and HVDC, keep disclosure and margin cap"),
    Round172ScoreStagePriceAlignment("doosan_czech_nuclear_preferred_bidder_case", "Stage 2 + 4B-watch", "Preferred bidder produced a price rally, but final contract and scope were not yet visible", "event_to_contract_not_green_yet", "credit preferred bidder; cap before contract signing, scope, margin, and OP/EPS revision"),
    Round172ScoreStagePriceAlignment("hd_hyundai_heavy_mipo_merger_stage2_4b_case", "Stage 2 + 4B-watch", "Merger announcement had large one-day price reaction and record-high context", "event_to_structural_watch", "credit restructuring; apply 4B watch before real US shipbuilding/MRO contract economics"),
    Round172ScoreStagePriceAlignment("hd_hyundai_marine_solution_ipo_mro_case", "Stage 2/3 candidate + IPO 4B", "IPO first-day premium requires valuation-room haircut", "good_model_but_ipo_4b", "credit recurring MRO; cap Green before post-listing FCF/OPM and customer diversification"),
    Round172ScoreStagePriceAlignment("kai_fa50_philippines_stage2_case", "Stage 2", "Customer, amount, aircraft count, and delivery deadline visible; margin and follow-on exports pending", "stage2_not_green_yet", "credit contract detail; cap before OP/EPS revision and margin visibility"),
    Round172ScoreStagePriceAlignment("lig_nex1_cheongung_combat_validation_stage25_case", "Stage 2.5 + 4B-watch", "Combat validation and +47% rally are strong but contract terms are absent", "price_path_attention_not_green", "allow Stage 2.5 watch; block Green before export contract and EPS revision"),
    Round172ScoreStagePriceAlignment("hanwha_ocean_china_sanction_4c_case", "Stage 2 option -> 4C-watch", "US shipbuilding/MRO option is offset by China sanction retaliation", "hard_redteam_alignment", "apply geopolitical sanction hard gate"),
    Round172ScoreStagePriceAlignment("hd_hyundai_mipo_loi_only_case", "Stage 1 / weak Stage 2", "LOI/contract talk cannot support Stage 3 even if price moves", "green_block_correct", "cap LOI until final contract, customer, margin, and delivery detail appear"),
    Round172ScoreStagePriceAlignment("doosan_czech_nuclear_legal_gate_case", "Stage 2 -> legal 4C-watch", "Preferred bidder rally faced appeal / contract-signing prohibition gate", "legal_gate_contains_false_green", "block Stage 3 before legal gate clears and contract scope is signed"),
)


ROUND172_SCORE_TARGETS: tuple[Round172ScoreTarget, ...] = (
    Round172ScoreTarget(
        "GRID_TRANSFORMER_SHORTAGE_KOREA",
        E2RArchetype.GRID_TRANSFORMER_SHORTAGE_KOREA,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round172ScoreWeightDraft(24, 20, 18, 12, 8, 8, 10),
        ("ai_data_center_power_demand", "us_grid_shortage", "transformer_lead_time_four_years", "transformer_price_increase"),
        ("us_capa_expansion", "ehv_transformer_export", "backlog_visibility", "op_eps_revision"),
        ("op_eps_fcf_revision", "backlog_quality_improvement", "opm_maintained_or_improving", "60d_mfe_20pct", "detail_verified"),
        ("k_transformer_consensus_crowded", "120d_mfe_80pct", "252d_mfe_150pct", "peer_top_quartile_valuation"),
        ("capa_normalization", "customer_project_delay", "raw_material_cost_spike", "margin_miss"),
        ("op_eps_fcf_revision", "backlog_quality", "margin_visible", "price_path_aligned", "valuation_room_remaining"),
        ("capa_normalization", "valuation_crowding", "customer_project_delay", "margin_unknown"),
        ("capa_normalization", "valuation_crowding", "raw_material_cost", "project_delay"),
        "Korea transformer names can reach Stage 3, but strong winners may also need 4B-watch after crowded rerating.",
    ),
    Round172ScoreTarget(
        "GRID_US_LOCALIZATION_CAPA",
        E2RArchetype.GRID_US_LOCALIZATION_CAPA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round172ScoreWeightDraft(22, 21, 18, 11, 8, 8, 10),
        ("hyosung_hico", "memphis_transformer_plant", "buy_america_or_tariff", "us_utility_customer"),
        ("us_plant_expansion", "hvdc_transformer", "765kv_exposure", "local_capa_visibility"),
        ("hico_utilization", "margin_visible", "op_eps_revision", "price_path_aligned"),
        ("k_power_equipment_basket_crowded", "local_capa_priced_before_utilization"),
        ("local_capex_burden", "utilization_miss", "margin_unknown", "disclosure_detail_missing"),
        ("us_local_capa", "hvdc_option", "margin_visible", "op_eps_revision"),
        ("capex_burden", "utilization_missing", "margin_unknown", "detail_missing"),
        ("local_capa_capex", "utilization", "margin_unknown"),
        "US localization and HVDC raise Stage 2.5 visibility, but Stage 3 waits for utilization, margin, and OP/EPS conversion.",
    ),
    Round172ScoreTarget(
        "POWER_EQUIPMENT_BACKLOG_TO_FCF_KOREA",
        E2RArchetype.POWER_EQUIPMENT_BACKLOG_TO_FCF_KOREA,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round172ScoreWeightDraft(24, 21, 17, 12, 8, 8, 10),
        ("power_equipment_backlog", "opm_improvement", "fcf_conversion", "old_low_margin_frame"),
        ("backlog_growth", "low_margin_order_cleanup", "cashflow_visible", "op_eps_revision"),
        ("backlog_to_fcf", "margin_sustained", "old_frame_rerating", "price_path_aligned"),
        ("backlog_to_fcf_consensus_crowded", "price_faster_than_revision"),
        ("low_margin_backlog_returns", "opm_miss", "fcf_miss", "order_growth_slowdown"),
        ("fcf_conversion", "margin_sustained", "backlog_quality", "op_eps_revision"),
        ("low_margin_contract", "fcf_miss", "order_peak", "valuation_crowding"),
        ("low_margin_backlog", "fcf_miss", "valuation_crowding"),
        "Backlog-to-FCF is the R1 quality test: orders matter only when cashflow and margin follow.",
    ),
    Round172ScoreTarget(
        "SHIPBUILDING_US_PLATFORM_RESTRUCTURING",
        E2RArchetype.SHIPBUILDING_US_PLATFORM_RESTRUCTURING,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round172ScoreWeightDraft(18, 18, 12, 12, 8, 8, 10),
        ("masga", "us_shipbuilding_rebuild", "arctic_icebreaker", "naval_defense_demand"),
        ("merger", "share_exchange_ratio", "us_shipbuilding_cooperation", "record_high_price_reaction"),
        ("actual_us_shipbuilding_or_mro_contract", "yard_capa_utilization", "margin_improvement", "fcf_visible"),
        ("merger_announcement_priced", "record_high", "event_day_10pct_rally"),
        ("integration_risk", "event_premium_only", "actual_contract_missing", "margin_unknown"),
        ("actual_contract", "margin_visible", "yard_execution", "op_eps_revision"),
        ("actual_contract_missing", "event_premium", "integration_risk", "share_exchange_dispute"),
        ("mna_event_only", "margin_unknown", "contract_missing"),
        "US shipbuilding restructuring can be Stage 2, but merger news alone is not Stage 3-Green.",
    ),
    Round172ScoreTarget(
        "SHIP_MRO_RECURRING_PLATFORM",
        E2RArchetype.SHIP_MRO_RECURRING_PLATFORM,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round172ScoreWeightDraft(20, 20, 11, 12, 8, 8, 10),
        ("ship_mro", "retrofit", "green_conversion", "parts_service_recurring"),
        ("ipo", "revenue_growth", "service_platform_visibility", "customer_base"),
        ("post_listing_fcf", "recurring_mro_revenue", "opm_sustained", "customer_diversification"),
        ("ipo_first_day_premium", "kkR_overhang", "mro_platform_fully_priced"),
        ("ipo_premium_unwinds", "fcf_miss", "customer_concentration", "overhang"),
        ("recurring_revenue", "opm_sustained", "fcf_visible", "customer_diversified"),
        ("ipo_premium", "fcf_missing", "overhang", "valuation_crowding"),
        ("ipo_premium", "overhang", "fcf_missing"),
        "MRO is higher-quality than one-off ship orders, but IPO premium can make the first price path a 4B case.",
    ),
    Round172ScoreTarget(
        "NUCLEAR_EXPORT_PREFERRED_BIDDER",
        E2RArchetype.NUCLEAR_EXPORT_PREFERRED_BIDDER,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round172ScoreWeightDraft(18, 20, 10, 12, 8, 8, 10),
        ("team_korea_nuclear_export", "czech_nuclear_project", "reactor_equipment_theme"),
        ("preferred_bidder", "project_value", "scope_expected", "price_path_rally"),
        ("final_contract_signed", "supplier_scope_confirmed", "op_eps_revision", "margin_visible"),
        ("preferred_bidder_rally_40pct", "contract_before_scope_priced"),
        ("legal_appeal", "contract_signing_block", "westinghouse_ip_issue", "financing_failure", "political_change"),
        ("final_contract", "scope_confirmed", "op_eps_revision", "margin_visible"),
        ("preferred_bidder_only", "legal_gate", "scope_unknown", "margin_unknown"),
        ("preferred_bidder_only", "legal_gate", "scope_unknown"),
        "Preferred bidder is Stage 2 evidence and can move price, but contract signing and company scope gate Stage 3.",
    ),
    Round172ScoreTarget(
        "DEFENSE_AIRCRAFT_EXPORT_BACKLOG",
        E2RArchetype.DEFENSE_AIRCRAFT_EXPORT_BACKLOG,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round172ScoreWeightDraft(20, 20, 12, 11, 8, 8, 10),
        ("fighter_modernization", "fa50_export_demand", "government_customer"),
        ("aircraft_contract", "contract_amount", "aircraft_count", "delivery_by_2030"),
        ("follow_on_contract", "delivery_margin_visible", "maintenance_or_training_revenue", "op_eps_revision"),
        ("defense_aircraft_story_crowded", "contract_value_priced_before_margin"),
        ("delivery_delay", "warranty_cost", "development_cost", "margin_unknown"),
        ("contract_amount", "delivery_schedule", "government_customer", "margin_visible", "op_eps_revision"),
        ("margin_unknown", "delivery_delay", "warranty_cost", "follow_on_contract_missing"),
        ("margin_unknown", "delivery_delay", "warranty_cost"),
        "Aircraft export contracts are Stage 2; Stage 3 waits for margin, follow-on orders, and OP/EPS conversion.",
    ),
    Round172ScoreTarget(
        "DEFENSE_INTERCEPTOR_COMBAT_VALIDATION",
        E2RArchetype.DEFENSE_INTERCEPTOR_COMBAT_VALIDATION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round172ScoreWeightDraft(18, 17, 15, 12, 8, 8, 10),
        ("combat_validation", "missile_defense_demand", "patriot_alternative", "middle_east_or_europe_interest"),
        ("price_path_47pct", "demand_interest", "unit_cost_advantage", "production_scalability"),
        ("actual_export_contract", "contract_amount", "delivery_schedule", "op_eps_revision"),
        ("contract_before_price_rally", "stage2_120d_mfe_80pct", "war_event_priced"),
        ("war_event_fades", "export_contract_delay", "competitor_price_cut", "production_bottleneck"),
        ("actual_contract", "contract_amount", "delivery_schedule", "op_eps_revision"),
        ("actual_contract_missing", "war_event_only", "production_bottleneck", "valuation_crowding"),
        ("actual_contract_missing", "war_event_only", "valuation_crowding"),
        "Combat validation can lift a defense name to Stage 2.5, but Stage 3-Green waits for signed export contracts and revisions.",
    ),
    Round172ScoreTarget(
        "GEOPOLITICAL_SHIPBUILDING_SANCTION_OVERLAY",
        E2RArchetype.GEOPOLITICAL_SHIPBUILDING_SANCTION_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        Round172ScoreWeightDraft("gate", "gate", "gate", "gate", "gate", "gate", "gate"),
        ("us_shipbuilding_mro", "philly_shipyard", "section_301", "us_china_maritime_tension"),
        ("us_asset_acquisition", "mro_contract", "investment_pledge"),
        ("not_green_until_sanction_scope_and_customer_impact_cleared",),
        ("us_shipbuilding_option_priced_before_sanction_risk",),
        ("china_sanctions", "export_control", "geopolitical_retaliation", "share_price_drop", "customer_or_supplier_restriction"),
        (),
        ("sanction", "export_control", "geopolitical_retaliation", "customer_damage"),
        ("sanction", "export_control", "geopolitical_retaliation"),
        "US shipbuilding exposure can be attractive, but sanction retaliation is a hard RedTeam overlay.",
        hard_gate=True,
    ),
    Round172ScoreTarget(
        "MOU_LOI_NOT_CONTRACT",
        E2RArchetype.MOU_LOI_NOT_CONTRACT,
        Round10ThemePosture.REDTEAM_FIRST,
        Round172ScoreWeightDraft("cap", "cap", "cap", "cap", "cap", "cap", "cap"),
        ("mou", "loi", "contract_talk", "order_report_without_final_contract"),
        ("loi_or_negotiation_confirmed", "details_undisclosed"),
        ("not_green_until_final_contract_amount_customer_margin_delivery_visible",),
        ("loi_priced_as_order", "headline_order_rally"),
        ("final_contract_missing", "customer_unknown", "margin_unknown", "terms_undisclosed", "loi_failed_to_convert"),
        (),
        ("loi_only", "final_contract_missing", "terms_undisclosed"),
        ("loi_only", "mou_only", "detail_missing"),
        "LOI/MOU/contract talk can route research, but it cannot support Stage 3.",
        hard_gate=True,
    ),
    Round172ScoreTarget(
        "DISCLOSURE_CONFIDENCE_CAP",
        E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        Round10ThemePosture.REDTEAM_FIRST,
        Round172ScoreWeightDraft("cap", "cap", "cap", "cap", "cap", "cap", "+"),
        ("opendart_list_only", "contract_headline", "high_signal_disclosure"),
        ("opendart_detail_fetched", "contract_amount", "counterparty", "contract_duration"),
        ("contract_amount_to_sales", "delivery_schedule", "margin_visible", "multi_source_confirmation"),
        ("undisclosed_contract_theme_crowded",),
        ("detail_missing", "contract_amount_missing", "counterparty_missing", "duration_missing", "margin_unknown"),
        ("contract_value", "contract_duration", "counterparty", "delivery_schedule", "margin_visible"),
        ("detail_missing", "contract_amount_missing", "counterparty_missing", "duration_missing", "margin_unknown"),
        ("disclosure_confidence_capped", "detail_missing", "margin_unknown"),
        "OpenDART list-only or headline-only contract evidence cannot support Stage 3-Green.",
    ),
    Round172ScoreTarget(
        "NUCLEAR_EXPORT_LEGAL_GATE",
        E2RArchetype.NUCLEAR_EXPORT_LEGAL_GATE,
        Round10ThemePosture.REDTEAM_FIRST,
        Round172ScoreWeightDraft("gate", "gate", "gate", "gate", "gate", "gate", "gate"),
        ("preferred_bidder", "appeal", "contract_signing_block", "westinghouse_ip_issue"),
        ("legal_gate_identified", "competition_authority_review", "appeal_resolution_needed"),
        ("not_green_until_appeal_resolved_and_contract_signed",),
        ("preferred_bidder_rally_ignores_legal_gate",),
        ("contract_signing_prohibited", "appeal_pending", "ip_dispute", "political_change", "financing_failure"),
        (),
        ("legal_gate_cleared", "contract_signed", "scope_confirmed"),
        ("appeal_pending", "contract_signing_block", "ip_dispute"),
        "Nuclear export preferred bidder rallies stay capped while legal or competition authority gates are open.",
        hard_gate=True,
    ),
)


ROUND172_CASE_CANDIDATES: tuple[Round172CaseCandidate, ...] = (
    Round172CaseCandidate(
        "hd_hyundai_electric_transformer_stage3_4b_case",
        "GRID_TRANSFORMER_SHORTAGE_KOREA",
        "267260",
        "HD현대일렉트릭",
        "KR",
        "structural_success",
        date(2025, 1, 1),
        date(2026, 3, 1),
        date(2026, 5, 11),
        date(2026, 5, 11),
        None,
        ("us_transformer_shortage", "lead_time_four_years", "transformer_price_up_80pct", "alabama_second_factory", "ehv_transformer_export", "op_eps_fcf_revision_needed"),
        ("valuation_crowding", "capa_normalization", "raw_material_cost", "customer_project_delay"),
        "stage3_candidate_plus_4b_watch_needs_krx_backfill",
        "needs_price_backfill",
        ("round_172.md Reuters US transformer shortage", "round_172.md HD Hyundai Electric context"),
        "K-transformer flagship case: the system must catch Stage 3 before crowded rerating, then apply 4B-watch when valuation room shrinks.",
        (E2RArchetype.POWER_EQUIPMENT_BACKLOG_TO_FCF_KOREA, E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH),
    ),
    Round172CaseCandidate(
        "hyosung_hico_hvdc_stage25_case",
        "GRID_US_LOCALIZATION_CAPA",
        "298040",
        "효성중공업",
        "KR",
        "success_candidate",
        date(2025, 12, 2),
        date(2025, 12, 2),
        None,
        None,
        None,
        ("hyosung_hico_memphis", "transformer_plant_expansion_157m_usd", "hvdc_transformer", "765kv_ehv_exposure", "us_local_capa"),
        ("margin_unknown", "utilization_missing", "local_capex_burden", "disclosure_confidence_capped"),
        "stage2_5_us_localization_hvdc_needs_margin_revision",
        "needs_price_backfill",
        ("round_172.md Reuters grid equipment makers invest in US", "round_172.md Hyosung Heavy context"),
        "US localization and HVDC raise visibility, but Stage 3 waits for HICO utilization, margin, OP/EPS, and KRX price path.",
        (E2RArchetype.GRID_TRANSFORMER_SHORTAGE_KOREA,),
    ),
    Round172CaseCandidate(
        "doosan_czech_nuclear_preferred_bidder_case",
        "NUCLEAR_EXPORT_PREFERRED_BIDDER",
        "034020",
        "두산에너빌리티",
        "KR",
        "success_candidate",
        date(2024, 7, 17),
        date(2024, 7, 17),
        None,
        date(2024, 10, 30),
        None,
        ("khpn_czech_preferred_bidder", "project_value_18_2b_usd", "reactor_equipment_scope_expected", "three_month_price_rally_48pct"),
        ("preferred_bidder_only", "scope_unknown", "margin_unknown", "legal_appeal"),
        "preferred_bidder_stage2_price_rally_not_green",
        "needs_price_backfill",
        ("round_172.md Reuters Czech preferred bidder",),
        "Preferred bidder can move price, but Stage 3 waits for final contract, supplier scope, margin, and OP/EPS revision.",
        (E2RArchetype.EVENT_TO_CONTRACT_ESCALATION, E2RArchetype.NUCLEAR_EXPORT_LEGAL_GATE),
    ),
    Round172CaseCandidate(
        "kepco_engineering_czech_nuclear_preferred_bidder_case",
        "NUCLEAR_EXPORT_PREFERRED_BIDDER",
        "052690",
        "한전기술",
        "KR",
        "success_candidate",
        date(2024, 7, 17),
        date(2024, 7, 17),
        None,
        None,
        None,
        ("khpn_czech_preferred_bidder", "engineering_scope_expected", "three_month_price_rally_41pct"),
        ("preferred_bidder_only", "engineering_scope_unconfirmed", "margin_unknown", "legal_appeal"),
        "engineering_scope_stage2_not_green",
        "needs_price_backfill",
        ("round_172.md Reuters Czech preferred bidder",),
        "Engineering scope must be confirmed before preferred-bidder price action becomes Stage 3 evidence.",
        (E2RArchetype.NUCLEAR_EXPORT_LEGAL_GATE,),
    ),
    Round172CaseCandidate(
        "kepco_kps_czech_nuclear_preferred_bidder_case",
        "NUCLEAR_EXPORT_PREFERRED_BIDDER",
        "051600",
        "한전KPS",
        "KR",
        "success_candidate",
        date(2024, 7, 17),
        date(2024, 7, 17),
        None,
        None,
        None,
        ("khpn_czech_preferred_bidder", "maintenance_scope_expected", "three_month_price_rally_14pct"),
        ("preferred_bidder_only", "maintenance_scope_unconfirmed", "margin_unknown", "legal_appeal"),
        "maintenance_scope_stage2_not_green",
        "needs_price_backfill",
        ("round_172.md Reuters Czech preferred bidder",),
        "Maintenance/service scope must be confirmed before Stage 3; preferred bidder alone is Stage 2.",
        (E2RArchetype.NUCLEAR_EXPORT_LEGAL_GATE,),
    ),
    Round172CaseCandidate(
        "hd_hyundai_heavy_mipo_merger_stage2_4b_case",
        "SHIPBUILDING_US_PLATFORM_RESTRUCTURING",
        "329180/010620",
        "HD현대중공업·HD현대미포",
        "KR",
        "success_candidate",
        date(2025, 8, 27),
        date(2025, 8, 27),
        None,
        date(2025, 8, 27),
        None,
        ("masga_us_shipbuilding_rebuild", "affiliate_merger", "share_exchange", "hd_heavy_price_up_11_3pct", "hd_mipo_price_up_14_6pct", "record_high"),
        ("event_premium", "actual_us_contract_missing", "integration_risk", "margin_unknown"),
        "event_to_structural_stage2_plus_4b_watch",
        "needs_price_backfill",
        ("round_172.md Reuters HD Hyundai Heavy / Mipo merger",),
        "Merger and US shipbuilding narrative are Stage 2 watch evidence; Stage 3 waits for real contracts, margin, and FCF.",
        (E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG, E2RArchetype.EVENT_TO_CONTRACT_ESCALATION),
    ),
    Round172CaseCandidate(
        "hd_hyundai_marine_solution_ipo_mro_case",
        "SHIP_MRO_RECURRING_PLATFORM",
        "443060",
        "HD현대마린솔루션",
        "KR",
        "4b_watch",
        date(2024, 5, 8),
        date(2024, 5, 8),
        None,
        date(2024, 5, 8),
        None,
        ("ship_mro_platform", "retrofit_service", "parts_service_recurring", "ipo_540m_usd", "first_day_return_97pct", "revenue_growth"),
        ("ipo_premium", "valuation_crowding", "kkR_overhang", "post_listing_fcf_unverified"),
        "good_recurring_platform_but_ipo_4b_watch",
        "needs_price_backfill",
        ("round_172.md WSJ HD Hyundai Marine IPO",),
        "MRO platform quality is separated from IPO first-day valuation premium.",
        (E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH,),
    ),
    Round172CaseCandidate(
        "kai_fa50_philippines_stage2_case",
        "DEFENSE_AIRCRAFT_EXPORT_BACKLOG",
        "047810",
        "한국항공우주",
        "KR",
        "success_candidate",
        date(2025, 6, 4),
        date(2025, 6, 4),
        None,
        None,
        None,
        ("philippines_fa50_contract", "contract_975_3bn_krw", "aircraft_count_12", "delivery_by_2030", "government_customer"),
        ("margin_unknown", "warranty_cost", "long_delivery_schedule", "follow_on_contract_missing"),
        "aircraft_export_stage2_not_green_until_margin_revision",
        "needs_price_backfill",
        ("round_172.md Reuters KAI Philippines FA-50 contract",),
        "Customer, amount, aircraft count, and delivery are Stage 2; margin and OP/EPS decide Stage 3.",
        (E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,),
    ),
    Round172CaseCandidate(
        "lig_nex1_cheongung_combat_validation_stage25_case",
        "DEFENSE_INTERCEPTOR_COMBAT_VALIDATION",
        "079550",
        "LIG넥스원",
        "KR",
        "success_candidate",
        date(2025, 6, 13),
        date(2025, 6, 13),
        None,
        date(2025, 6, 13),
        None,
        ("cheongung_ii_combat_validation", "patriot_alternative", "middle_east_europe_interest", "unit_cost_advantage", "price_up_47pct"),
        ("actual_export_contract_missing", "war_event_only", "production_bottleneck", "valuation_crowding"),
        "combat_validation_stage2_5_plus_4b_watch_not_green",
        "needs_price_backfill",
        ("round_172.md Financial Times Cheongung-II combat validation",),
        "Combat validation and price path raise attention, but Green waits for signed export contract and OP/EPS revision.",
        (E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG, E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH),
    ),
    Round172CaseCandidate(
        "hanwha_ocean_china_sanction_4c_case",
        "GEOPOLITICAL_SHIPBUILDING_SANCTION_OVERLAY",
        "042660",
        "한화오션",
        "KR",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        None,
        ("philly_shipyard_acquisition", "us_navy_mro", "us_shipbuilding_investment_pledge", "us_shipbuilding_rebuild_option"),
        ("china_sanctions", "geopolitical_retaliation", "section_301", "share_price_drop", "us_china_maritime_tension"),
        "us_shipbuilding_option_broken_by_geopolitical_sanction",
        "needs_source_date_backfill",
        ("round_172.md AP Hanwha Ocean China sanctions",),
        "US shipbuilding/MRO option remains visible, but China sanction retaliation is a hard RedTeam overlay.",
        (E2RArchetype.SHIPBUILDING_US_PLATFORM_RESTRUCTURING,),
    ),
    Round172CaseCandidate(
        "hd_hyundai_mipo_loi_only_case",
        "MOU_LOI_NOT_CONTRACT",
        "010620",
        "HD현대미포 LOI-only 수주설",
        "KR",
        "event_premium",
        date(2025, 4, 8),
        None,
        None,
        None,
        None,
        ("container_ship_loi_report", "contract_talk_confirmed", "delivery_2027_2028_reported", "details_undisclosed"),
        ("final_contract_missing", "customer_unknown", "margin_unknown", "terms_undisclosed", "loi_only"),
        "loi_not_contract_green_block",
        "needs_price_backfill",
        ("round_172.md Reuters HD Hyundai Mipo contract talks",),
        "LOI/negotiation is not a signed contract. It may route research, but it cannot become Stage 3.",
        (E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,),
    ),
    Round172CaseCandidate(
        "doosan_czech_nuclear_legal_gate_case",
        "NUCLEAR_EXPORT_LEGAL_GATE",
        "034020",
        "두산에너빌리티 체코 원전 legal gate",
        "KR",
        "4c_thesis_break",
        date(2024, 7, 17),
        date(2024, 7, 17),
        None,
        None,
        date(2024, 10, 30),
        ("czech_nuclear_preferred_bidder", "contract_signing_expected", "project_value_18b_usd"),
        ("contract_signing_prohibited", "appeal_pending", "westinghouse_ip_issue", "competition_authority_review"),
        "preferred_bidder_legal_gate_blocks_stage3",
        "needs_price_backfill",
        ("round_172.md Reuters Czech watchdog contract signing prohibition",),
        "Preferred bidder rally is contained by legal gate until appeals clear and company scope is signed.",
        (E2RArchetype.NUCLEAR_EXPORT_PREFERRED_BIDDER,),
    ),
)


ROUND172_PRICE_FIELDS: tuple[str, ...] = (
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
    "MFE_30D",
    "MFE_90D",
    "MFE_180D",
    "MFE_1Y",
    "MFE_2Y",
    "MAE_30D",
    "MAE_90D",
    "MAE_180D",
    "MAE_1Y",
    "volume_spike_flag",
    "relative_strength_vs_kospi",
    "relative_strength_vs_sector",
    "valuation_at_stage3",
    "valuation_at_stage4b",
    "eps_revision_before_stage3",
    "eps_revision_after_stage3",
    "op_revision_before_stage3",
    "op_revision_after_stage3",
    "contract_amount",
    "contract_value",
    "contract_value_to_sales",
    "contract_duration_months",
    "contract_start_date",
    "contract_end_date",
    "counterparty",
    "customer_name",
    "delivery_schedule",
    "order_backlog_value",
    "backlog_quality_score",
    "opm_change",
    "fcf_margin_change",
    "transformer_lead_time_months",
    "transformer_price_increase_pct",
    "ehv_transformer_flag",
    "us_local_capa_flag",
    "hico_memphis_plant_flag",
    "hico_plant_expansion_usd",
    "hvdc_transformer_flag",
    "czech_preferred_bidder_flag",
    "final_contract_signed_flag",
    "supplier_scope_confirmed_flag",
    "westinghouse_appeal_flag",
    "contract_signing_block_flag",
    "share_exchange_ratio",
    "merger_event_flag",
    "ipo_first_day_return_pct",
    "mro_recurring_revenue_flag",
    "kkR_overhang_flag",
    "fa50_aircraft_count",
    "fa50_contract_amount_krw",
    "delivery_by_2030_flag",
    "combat_validation_flag",
    "cheongung_ii_flag",
    "price_up_47pct_flag",
    "actual_export_contract_flag",
    "geopolitical_sanction_flag",
    "china_sanction_flag",
    "section_301_flag",
    "mou_flag",
    "loi_flag",
    "final_contract_missing_flag",
    "opendart_rcept_no",
    "opendart_detail_fetched_flag",
    "disclosure_confidence_score",
    "detail_parser_confidence",
    "disclosure_signal_class",
    "routine_disclosure_flag",
    "risk_disclosure_flag",
    "high_signal_disclosure_flag",
    "contract_amount_disclosed_flag",
    "customer_name_disclosed_flag",
    "margin_disclosed_flag",
    "dilution_type",
    "cb_bw_issuance_flag",
    "audit_issue_flag",
    "legal_gate_flag",
    "sanction_risk_flag",
    "low_margin_order_flag",
    "stage_before_redteam",
    "stage_after_redteam",
    "score_before_redteam",
    "score_after_redteam",
    "score_price_alignment",
    "price_validation_status",
    "review_notes",
)


def round172_target_for(target_id: str) -> Round172ScoreTarget | None:
    for target in ROUND172_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round172_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND172_CASE_CANDIDATES:
        target = round172_target_for(candidate.target_id)
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
                f"Round172 R1 Loop-11 Korea industrial case for {candidate.target_id}; "
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
            score_price_alignment=_round172_score_price_alignment(candidate),
            rerating_result=_round172_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
            score_weight_hint={
                "eps_fcf": _numeric_weight(weights["eps_fcf_opm"]),
                "visibility": _numeric_weight(weights["contract_visibility"]),
                "bottleneck": _numeric_weight(weights["bottleneck_pricing"]),
                "early_price_validation": _numeric_weight(weights["early_price_validation"]),
                "capital_discipline": _numeric_weight(weights["capital_discipline"]),
                "disclosure_redteam": _numeric_weight(weights["disclosure_redteam"]),
                "valuation_4b_room": _numeric_weight(weights["valuation_4b_room"]),
            },
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "require_price_path_validation",
                "require_contract_quality_customer_delivery_margin_eps_fcf_for_green",
                "stage3_early_catch_requires_4_of_6_loop11_conditions",
                "stage4b_cooling_required_when_price_runs_ahead_of_revision",
                "do_not_invent_contract_dates_prices_margins_or_counterparties",
                "loi_mou_preferred_bidder_and_ipo_premium_do_not_create_green",
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


def round172_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND172_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "eps_fcf_opm": str(weights["eps_fcf_opm"]),
                "contract_visibility": str(weights["contract_visibility"]),
                "bottleneck_pricing": str(weights["bottleneck_pricing"]),
                "early_price_validation": str(weights["early_price_validation"]),
                "capital_discipline": str(weights["capital_discipline"]),
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


def round172_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND172_CASE_CANDIDATES:
        target = round172_target_for(candidate.target_id)
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


def round172_stage_date_rows() -> tuple[dict[str, str], ...]:
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
        for target in ROUND172_SCORE_TARGETS
    )


def round172_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round172_backfill": "true"} for field in ROUND172_PRICE_FIELDS)


def round172_base_score_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(weight.as_row() for weight in ROUND172_BASE_SCORE_WEIGHTS)


def round172_stage_cap_rows() -> tuple[dict[str, str], ...]:
    return tuple(cap.as_row() for cap in ROUND172_STAGE_CAPS)


def round172_score_stage_price_alignment_rows() -> tuple[dict[str, str], ...]:
    return tuple(row.as_row() for row in ROUND172_SCORE_STAGE_PRICE_ALIGNMENT)


def round172_summary() -> dict[str, int | bool]:
    records = round172_case_records()
    return {
        "target_count": len(ROUND172_SCORE_TARGETS),
        "source_canonical_target_count": ROUND172_SOURCE_CANONICAL_TARGET_COUNT,
        "case_candidate_count": len(records),
        "base_score_component_count": len(ROUND172_BASE_SCORE_WEIGHTS),
        "stage_cap_count": len(ROUND172_STAGE_CAPS),
        "score_stage_price_alignment_count": len(ROUND172_SCORE_STAGE_PRICE_ALIGNMENT),
        "structural_success_count": sum(1 for record in records if record.case_type == "structural_success"),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for record in records if record.case_type == "cyclical_success"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND172_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND172_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND172_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "hard_gate_target_count": sum(1 for target in ROUND172_SCORE_TARGETS if target.hard_gate),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round172_r1_loop11_reports(
    *,
    output_directory: str | Path = ROUND172_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND172_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND172_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round172_r1_loop11_industrial_infra_summary.md",
        "case_matrix": output / "round172_r1_loop11_case_matrix.csv",
        "stage_date_plan": output / "round172_r1_loop11_stage_date_plan.csv",
        "green_guardrails": output / "round172_r1_loop11_green_guardrails.md",
        "loop11_risk_overlays": output / "round172_r1_loop11_risk_overlays.md",
        "price_validation_plan": output / "round172_r1_loop11_price_validation_plan.md",
        "price_fields": output / "round172_r1_loop11_price_fields.csv",
        "base_score_weights": output / "round172_r1_loop11_base_score_weights.csv",
        "stage_caps": output / "round172_r1_loop11_stage_caps.csv",
        "score_stage_price_alignment": output / "round172_r1_loop11_score_stage_price_alignment.csv",
        "score_stage_price_alignment_md": output / "round172_r1_loop11_score_stage_price_alignment.md",
    }
    _write_case_jsonl(round172_case_records(), cases)
    _write_rows(round172_score_profile_rows(), score_profiles)
    _write_rows(round172_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round172_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round172_price_field_rows(), paths["price_fields"])
    _write_rows(round172_base_score_weight_rows(), paths["base_score_weights"])
    _write_rows(round172_stage_cap_rows(), paths["stage_caps"])
    _write_rows(round172_score_stage_price_alignment_rows(), paths["score_stage_price_alignment"])
    paths["summary"].write_text(render_round172_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round172_green_guardrail_markdown(), encoding="utf-8")
    paths["loop11_risk_overlays"].write_text(render_round172_loop11_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round172_price_validation_plan_markdown(), encoding="utf-8")
    paths["score_stage_price_alignment_md"].write_text(render_round172_score_stage_price_alignment_markdown(), encoding="utf-8")
    return paths


def render_round172_summary_markdown() -> str:
    summary = round172_summary()
    lines = [
        "# Round-172 R1 Loop-11 Korea Industrial Orders / Infrastructure Summary",
        "",
        f"- source_round: `{ROUND172_SOURCE_ROUND_PATH}`",
        "- large_sector: `INDUSTRIAL_ORDERS_INFRA`",
        "- loop: `R1 Loop 11 / v11.0`",
        f"- target_count: {summary['target_count']}",
        f"- source_canonical_target_count: {summary['source_canonical_target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- base_score_component_count: {summary['base_score_component_count']}",
        f"- stage_cap_count: {summary['stage_cap_count']}",
        f"- score_stage_price_alignment_count: {summary['score_stage_price_alignment_count']}",
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
        f"- hard_gate_target_count: {summary['hard_gate_target_count']}",
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "",
        "- R1 Loop 11 is Korea-first and excludes the previously overused global success cases from the center of the pack.",
        "- Loop 11 adds early price-path validation: the system must test whether Stage 3 was visible before the large rerating.",
        "- Stage 3-Green remains strict. Orders, preferred bidder, LOI, IPO premium, combat validation, or merger news are not enough by themselves.",
        "- The base score weights are EPS/FCF/OPM 24, contract visibility 20, bottleneck/pricing 18, early price path 12, capital discipline 8, disclosure/RedTeam 8, valuation/4B room 10.",
        "- Example: HD현대일렉트릭 can be a Stage 3 candidate and a 4B-watch case at the same time.",
        "- Example: LIG넥스원 can rise to Stage 2.5 from combat validation and price path, but signed export contract and OP/EPS revision are still required for Stage 3.",
        "- Example: HD현대미포 LOI-only contract talk stays capped even if the headline moves price.",
        "- Example: 한화오션's US shipbuilding option is hard-reviewed when China sanction retaliation appears.",
    ]
    return "\n".join(lines) + "\n"


def render_round172_green_guardrail_markdown() -> str:
    lines = [
        "# Round-172 R1 Loop-11 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Loop-11 penalties |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND172_SCORE_TARGETS:
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
            "- Do not apply R1 Loop-11 v11.0 weights to production scoring yet.",
            "- Do not lower Stage 3-Green thresholds because Korea R1 has strong winners.",
            "- Do not use Round 172 case records as candidate-generation input.",
            "- Do not treat preferred bidder, LOI, MOU, merger, IPO premium, or combat validation as Stage 3-Green by itself.",
            "- Do not invent contract amounts, counterparties, delivery schedules, margins, stage prices, MFE/MAE, or valuation bands.",
            "- Apply 4B-watch when price and consensus move faster than revisions.",
            "- Apply 4C/hard review for legal gates, sanctions, contract cancellation/correction, dilution, or disclosure failures.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round172_loop11_risk_overlay_markdown() -> str:
    lines = [
        "# Round-172 R1 Loop-11 Risk Overlays",
        "",
        "- `EARLY_STAGE3_CATCH`: OP/EPS/FCF, backlog quality, margin, 60D MFE, valuation room, and detail confidence align before the large rerating.",
        "- `STAGE2_5_WATCH`: strong evidence such as combat validation or US localization is above Stage 2 attention but below Stage 3 conviction.",
        "- `K_TRANSFORMER_4B`: a strong K-transformer thesis can still be a 4B-watch case once everyone accepts the new frame.",
        "- `PREFERRED_BIDDER_NOT_CONTRACT`: preferred bidder can be Stage 2 and move price, but final contract and scope gate Stage 3.",
        "- `LOI_NOT_CONTRACT`: LOI, MoA, or contract talks are not signed contract evidence.",
        "- `IPO_PREMIUM_4B`: a good recurring platform can be too expensive after first-day IPO rerating.",
        "- `COMBAT_VALIDATION_WITHOUT_EXPORT_CONTRACT`: defense attention can rise, but Green waits for contract amount, delivery, and revisions.",
        "- `GEOPOLITICAL_SANCTION_4C`: US shipbuilding exposure is capped or broken by sanction retaliation and export-control risk.",
        "- `DISCLOSURE_CONFIDENCE_CAPPED`: OpenDART list-only/headline evidence is capped until detail fields are parsed.",
        "",
        "Simple example: if `as_of_date=2025-04-08`, an LOI report can be used as Stage 1 attention. A 2025-04-09 signed-contract article cannot be used on 2025-04-08, and the LOI itself cannot become Stage 3-Green.",
    ]
    return "\n".join(lines) + "\n"


def render_round172_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-172 R1 Loop-11 Price Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign Stage 1/2/3/4B/4C dates from dated source evidence only.",
        "2. Backfill KRX daily bars for `price_at_stage1` through `price_at_stage4c`.",
        "3. Calculate 20D/60D/120D/252D returns after Stage 2 and Stage 3.",
        "4. Calculate MFE/MAE after Stage 2, especially 60D/120D/252D.",
        "5. Compare price speed against OP/EPS revision speed to decide Stage 3 vs 4B-watch.",
        "6. Store `score_price_alignment` and keep LOI/MOU, preferred bidder, IPO, legal gate, sanction, and missing detail labels explicit.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | target | stage marker | check |",
        "| --- | --- | --- | --- |",
    ]
    for row in round172_case_candidate_rows():
        stage_date = row["stage4c_date"] or row["stage4b_date"] or row["stage3_date"] or row["stage2_date"] or row["stage1_date"] or "undated"
        lines.append(f"| `{row['case_id']}` | `{row['target_id']}` | {stage_date} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `stage3_catch_and_4b_cool_required`: the case should be detectable before a large move, then cooled when crowded.",
            "- `stage2_5_not_green_yet`: evidence is stronger than a headline, but not enough for Green.",
            "- `event_to_contract_not_green_yet`: event or preferred bidder must convert into signed contract and company scope.",
            "- `good_model_but_ipo_4b`: business quality exists, but the first price path is IPO premium.",
            "- `green_block_correct`: LOI/MOU or missing detail correctly blocks Stage 3.",
            "- `hard_redteam_alignment`: sanction, legal gate, or disclosure break correctly blocks positive narrative.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round172_score_stage_price_alignment_markdown() -> str:
    lines = [
        "# Round-172 R1 Loop-11 Score -> Stage -> Price Alignment",
        "",
        "## Base Score Weights",
        "",
        "| component | points | direction | reason |",
        "| --- | ---: | --- | --- |",
    ]
    for row in ROUND172_BASE_SCORE_WEIGHTS:
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
    for cap in ROUND172_STAGE_CAPS:
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
    for row in ROUND172_SCORE_STAGE_PRICE_ALIGNMENT:
        lines.append(
            f"| `{row.case_id}` | {row.detected_stage} | {row.price_path_status} | "
            f"{row.verdict} | {row.normalization_adjustment} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- HD현대일렉트릭 is the cleanest Korea R1 early Stage 3 / 4B-watch test.",
            "- 효성중공업 and LIG넥스원 use Stage 2.5 as a diagnostic watch band, not a canonical Stage change.",
            "- Czech nuclear preferred bidder cases prove price can move before final contract; that is Stage 2, not Green.",
            "- HD현대미포 LOI and 한화오션 sanction cases prove why Stage 4C and disclosure caps must remain strict.",
        ]
    )
    return "\n".join(lines) + "\n"


def _round172_score_price_alignment(candidate: Round172CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "aligned"
    if candidate.case_type == "success_candidate" and "stage2_5" in candidate.alignment_hint:
        return "unknown"
    if candidate.case_type == "success_candidate":
        return "aligned"
    if candidate.case_type in {"event_premium", "4b_watch"}:
        return "price_moved_without_evidence"
    if candidate.case_type == "4c_thesis_break":
        return "false_positive_score"
    return "unknown"


def _round172_rerating_result(candidate: Round172CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "true_rerating"
    if candidate.case_type == "event_premium":
        return "event_premium"
    if candidate.case_type == "4b_watch":
        return "theme_overheat"
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    if "preferred_bidder" in candidate.alignment_hint:
        return "policy_event_rerating"
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
    "ROUND172_BASE_SCORE_WEIGHTS",
    "ROUND172_CASE_CANDIDATES",
    "ROUND172_DEFAULT_CASES_PATH",
    "ROUND172_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND172_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND172_PRICE_FIELDS",
    "ROUND172_SCORE_STAGE_PRICE_ALIGNMENT",
    "ROUND172_SCORE_TARGETS",
    "ROUND172_SOURCE_CANONICAL_TARGET_COUNT",
    "ROUND172_SOURCE_CANONICAL_TARGET_IDS",
    "ROUND172_STAGE_CAPS",
    "Round172BaseScoreWeight",
    "Round172CaseCandidate",
    "Round172ScoreStagePriceAlignment",
    "Round172ScoreTarget",
    "Round172ScoreWeightDraft",
    "Round172StageCap",
    "render_round172_green_guardrail_markdown",
    "render_round172_loop11_risk_overlay_markdown",
    "render_round172_price_validation_plan_markdown",
    "render_round172_score_stage_price_alignment_markdown",
    "render_round172_summary_markdown",
    "round172_base_score_weight_rows",
    "round172_case_candidate_rows",
    "round172_case_records",
    "round172_price_field_rows",
    "round172_score_profile_rows",
    "round172_score_stage_price_alignment_rows",
    "round172_stage_cap_rows",
    "round172_stage_date_rows",
    "round172_summary",
    "round172_target_for",
    "write_round172_r1_loop11_reports",
]
