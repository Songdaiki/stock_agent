"""Round-186 R2 Loop-12 Korea AI, semiconductor, and electronics pack.

Round 186 extends the R2 case library around Korea-listed glass substrate,
system semiconductor design-house, HBM test equipment, advanced packaging,
PCB/substrate, MLCC, ADAS/lidar, on-device AI, and semiconductor CAPEX
themes. It is calibration/report material only. Production feature
engineering, scoring, staging, and RedTeam code must not import this module.
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


ROUND186_SOURCE_ROUND_PATH = "docs/round/round_186.md"
ROUND186_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round186_r2_loop12_ai_semiconductor_electronics"
ROUND186_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r2_loop12_round186.jsonl"
ROUND186_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round186_r2_loop12_v12.csv"
ROUND186_SOURCE_CANONICAL_TARGET_IDS: tuple[str, ...] = (
    "GLASS_SUBSTRATE_ADVANCED_PACKAGING_KOREA",
    "SYSTEM_SEMI_DESIGN_HOUSE_AI_ORDER",
    "HBM_TEST_EQUIPMENT_KOREA",
    "ADVANCED_PACKAGING_EQUIPMENT_BASKET",
    "AI_SERVER_PCB_SUBSTRATE_SECOND_WAVE",
    "MLCC_AI_SERVER_COMPONENTS",
    "CAMERA_LIDAR_ADAS_ELECTRONICS",
    "ON_DEVICE_AI_THEME_KOREA",
    "SEMI_CAPEX_ORDER_TO_REVENUE",
    "IP_LEAK_SUPPLY_CHAIN_REDTEAM",
    "LABOR_PRODUCTION_DISRUPTION_OVERLAY",
    "DISCLOSURE_CONFIDENCE_CAP",
)
ROUND186_SOURCE_CANONICAL_TARGET_COUNT = len(ROUND186_SOURCE_CANONICAL_TARGET_IDS)


@dataclass(frozen=True)
class Round186ScoreWeightDraft:
    eps_fcf_opm: int | str
    customer_contract_shipment_visibility: int | str
    bottleneck_process_adoption: int | str
    early_price_validation: int | str
    mass_production_yield_diversification: int | str
    ip_labor_security_disclosure_redteam: int | str
    valuation_4b_room: int | str

    def as_dict(self) -> dict[str, int | str]:
        return {
            "eps_fcf_opm": self.eps_fcf_opm,
            "customer_contract_shipment_visibility": self.customer_contract_shipment_visibility,
            "bottleneck_process_adoption": self.bottleneck_process_adoption,
            "early_price_validation": self.early_price_validation,
            "mass_production_yield_diversification": self.mass_production_yield_diversification,
            "ip_labor_security_disclosure_redteam": self.ip_labor_security_disclosure_redteam,
            "valuation_4b_room": self.valuation_4b_room,
        }


@dataclass(frozen=True)
class Round186ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round186ScoreWeightDraft
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
        return Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round186CaseCandidate:
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
class Round186BaseScoreWeight:
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
class Round186StageCap:
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
class Round186ScoreStagePriceAlignment:
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
    visibility: int | str,
    bottleneck: int | str,
    price: int | str,
    production: int | str,
    redteam: int | str,
    valuation: int | str,
) -> Round186ScoreWeightDraft:
    return Round186ScoreWeightDraft(eps, visibility, bottleneck, price, production, redteam, valuation)


CAP_WEIGHT = _w("cap", "cap", "cap", "cap", "cap", "cap", "+")
GATE_WEIGHT = _w("gate", "gate", "gate", "gate", "gate", "gate", "gate")


ROUND186_BASE_SCORE_WEIGHTS: tuple[Round186BaseScoreWeight, ...] = (
    Round186BaseScoreWeight("eps_fcf_opm_conversion", 24, "keep_high", "R2 Loop 12 requires OP/EPS/FCF conversion; AI exposure is not enough."),
    Round186BaseScoreWeight("customer_contract_shipment_visibility", 22, "detail_required", "Customer name, order size, delivery schedule, design win, and shipment visibility define Stage 2 quality."),
    Round186BaseScoreWeight("bottleneck_process_technology_adoption", 16, "sector_specific", "HBM test, glass substrate, 2nm, AI server substrate, MLCC, ADAS, and advanced packaging need adoption proof."),
    Round186BaseScoreWeight("early_price_path_validation", 12, "required_backfill", "Stage 2 이후 MFE, relative strength, and event return decide whether market validation or 4B overheating is occurring."),
    Round186BaseScoreWeight("mass_production_yield_customer_diversification", 8, "green_gate", "Mass production, yield, repeat order, and customer diversification prevent technology-only Green."),
    Round186BaseScoreWeight("ip_labor_security_disclosure_redteam", 10, "raised_for_loop12", "IP leakage, labor disruption, production delay, and missing order detail can break a semiconductor rerating."),
    Round186BaseScoreWeight("valuation_room_4b_runway", 8, "cool_crowded_keywords", "AI/HBM/glass/NPU keyword crowding reduces runway when price runs ahead of revisions."),
)


ROUND186_STAGE_CAPS: tuple[Round186StageCap, ...] = (
    Round186StageCap(
        "Stage 1",
        "45",
        ("hbm", "ai_server", "advanced_packaging", "glass_substrate", "cxl", "on_device_ai", "npu", "adas", "mlcc", "pcb"),
        ("on_device_ai_theme_korea_stage1_2_4b_watch_case",),
        "Theme keywords route research only. Green is blocked before customer, shipment, revenue, OP/EPS, and price-path evidence.",
    ),
    Round186StageCap(
        "Stage 2",
        "70",
        ("customer_name", "design_participation", "process_adoption", "government_grant", "production_facility", "strategic_investment", "equipment_order", "customer_capex"),
        ("skc_absolics_glass_substrate_stage2_case", "gaonchips_pfn_samsung_2nm_stage2_case"),
        "Stage 2 can be strong, but Stage 3 waits for order size, shipment, yield, revenue, and OP/EPS conversion.",
    ),
    Round186StageCap(
        "Stage 3",
        "requires_5_of_8",
        ("customer_amount_period_or_order_size", "shipment_or_mass_production_schedule", "op_eps_revision_or_op_beat", "customer_diversification_or_repeat_order", "60d_mfe_20pct_after_stage2", "relative_strength_vs_market", "no_ip_labor_production_hard_issue", "valuation_not_overheated"),
        ("hbm_test_equipment_basket_stage3_candidate_case", "ai_server_pcb_mlcc_second_wave_stage3_candidate_case"),
        "Stage 3 early catch is possible only when earnings conversion, customer/order detail, production evidence, price path, and RedTeam align.",
    ),
    Round186StageCap(
        "Stage 4B",
        "requires_4_of_6",
        ("stage2_120d_mfe_80pct", "basket_rally_without_contract_detail", "price_faster_than_op_eps_revision", "crowded_ai_hbm_glass_npu_keywords", "peer_top_quartile_valuation", "media_mou_design_win_only_price_rally"),
        ("on_device_ai_theme_korea_stage1_2_4b_watch_case",),
        "Good narratives are cooled when price and keyword crowding outrun order, shipment, yield, and revision evidence.",
    ),
    Round186StageCap(
        "Stage 4C",
        "hard_gate",
        ("customer_contract_cancel_or_correction", "order_size_customer_undisclosed_price_only_rally", "mass_production_delay_or_yield_failure", "customer_capex_delay", "labor_or_production_disruption", "ip_leak_or_china_catchup", "accounting_audit_disclosure_issue", "large_cb_bw_or_dilution"),
        ("samsung_supply_chain_labor_disruption_4c_case", "korea_memory_ip_leak_cxmt_4c_case"),
        "A single hard IP, labor, production, disclosure, customer CAPEX, or dilution issue can block Green.",
    ),
)


ROUND186_SCORE_TARGETS: tuple[Round186ScoreTarget, ...] = (
    Round186ScoreTarget(
        "GLASS_SUBSTRATE_ADVANCED_PACKAGING_KOREA",
        E2RArchetype.GLASS_SUBSTRATE_ADVANCED_PACKAGING_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(20, 20, 18, 10, 10, 12, 8),
        ("glass_substrate", "advanced_packaging", "ai_server_packaging", "hpc_or_defense_application"),
        ("chips_grant", "georgia_covington_facility", "test_batch_production", "production_ramp_plan"),
        ("customer_qualification", "yield_visible", "commercial_shipment", "revenue_recognition", "opm_fcf_visible"),
        ("glass_substrate_basket_rally", "customer_yield_missing_rally"),
        ("customer_missing", "yield_failure", "shipment_delay", "capex_return_unclear"),
        ("customer_qualification", "yield_visible", "shipment_revenue", "op_eps_revision"),
        ("customer_missing", "yield_missing", "revenue_missing", "capex_risk"),
        ("customer_missing", "yield_missing", "commercial_revenue_missing"),
        "Glass substrate is Stage 2-quality when facility/grant/test production exist, but Green waits for customer, yield, shipment, and revenue.",
    ),
    Round186ScoreTarget(
        "SYSTEM_SEMI_DESIGN_HOUSE_AI_ORDER",
        E2RArchetype.SYSTEM_SEMI_DESIGN_HOUSE_AI_ORDER,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(20, 22, 16, 10, 8, 10, 8),
        ("system_semi", "ai_chip_design_house", "samsung_2nm", "npu_or_hpc_chip"),
        ("customer_name", "design_role_confirmed", "advanced_packaging_included", "tapeout_or_order_reference"),
        ("order_size_visible", "revenue_recognition", "repeat_nre_or_royalty", "mass_production", "op_eps_revision"),
        ("design_win_price_rally_without_order_size", "2nm_ai_chip_keyword_crowded"),
        ("order_size_undisclosed", "revenue_missing", "foundry_execution_risk", "tapeout_delay"),
        ("order_size", "revenue_recognition", "repeat_design_win", "op_eps_revision"),
        ("order_size_missing", "revenue_missing", "single_customer", "foundry_execution_risk"),
        ("order_size_missing", "design_win_to_revenue_gap", "foundry_execution_risk"),
        "Design-house Stage 2 needs customer and role; Stage 3 waits for order size, revenue, repeat design win, and OP/EPS conversion.",
    ),
    Round186ScoreTarget(
        "HBM_TEST_EQUIPMENT_KOREA",
        E2RArchetype.HBM_TEST_EQUIPMENT_KOREA,
        Round10ThemePosture.GREEN_POSSIBLE,
        _w(23, 22, 17, 12, 8, 10, 8),
        ("hbm_test", "memory_test_handler", "cube_prober", "wafer_test", "sk_hynix_capex"),
        ("customer_capex", "actual_equipment_order", "shipment_schedule", "hbm_test_exposure"),
        ("customer_order_conversion", "op_eps_revision", "shipment_to_revenue", "repeat_order", "60d_mfe_20pct"),
        ("hbm_test_theme_crowded", "price_before_order", "basket_rotation"),
        ("order_missing", "shipment_delay", "customer_capex_delay", "op_eps_revision_down"),
        ("customer_order", "shipment_schedule", "op_eps_revision", "repeat_order", "price_path_aligned"),
        ("actual_order_missing", "shipment_missing", "price_only_rally", "capex_delay"),
        ("actual_order_missing", "op_eps_missing", "price_only_rally"),
        "HBM test equipment can become Stage 3, but individual order, shipment, OP/EPS, repeat order, and price path must be backfilled.",
    ),
    Round186ScoreTarget(
        "ADVANCED_PACKAGING_EQUIPMENT_BASKET",
        E2RArchetype.ADVANCED_PACKAGING_EQUIPMENT_BASKET,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(21, 20, 17, 10, 8, 11, 8),
        ("advanced_packaging_equipment", "wafer_bonding", "underfill", "die_attach", "post_bond_inspection"),
        ("customer_qualification", "equipment_order", "shipment_schedule", "spinoff_focus"),
        ("actual_customer", "order_value", "shipment_revenue", "margin_visible", "op_eps_revision"),
        ("packaging_equipment_keyword_rally", "spinoff_price_ahead_of_orders"),
        ("actual_order_missing", "governance_allocation_risk", "share_price_failed", "shipment_delay"),
        ("customer_order", "shipment_revenue", "op_eps_revision", "governance_clean"),
        ("order_missing", "governance_risk", "allocation_unclear", "price_failed"),
        ("order_missing", "governance_allocation", "shipment_delay"),
        "Advanced packaging equipment remains capped before customer orders, shipment revenue, margin, and governance clarity.",
    ),
    Round186ScoreTarget(
        "AI_SERVER_PCB_SUBSTRATE_SECOND_WAVE",
        E2RArchetype.AI_SERVER_PCB_SUBSTRATE_SECOND_WAVE,
        Round10ThemePosture.GREEN_POSSIBLE,
        _w(23, 21, 16, 12, 8, 9, 8),
        ("ai_server_pcb", "high_layer_pcb", "fc_bga", "server_board", "accelerator_board"),
        ("ai_server_customer_demand", "substrate_or_pcb_order_signal", "inventory_normalization", "asp_signal"),
        ("asp_confirmation", "op_eps_revision", "customer_diversification", "server_auto_mix", "price_path_aligned"),
        ("ai_server_parts_keyword_rally", "inventory_not_cleared_rally"),
        ("inventory_risk", "customer_concentration", "op_eps_missing", "smartphone_cycle_drag"),
        ("asp_confirmation", "inventory_normalization", "op_eps_revision", "customer_diversification"),
        ("inventory_risk", "customer_concentration", "op_eps_missing", "price_only_rally"),
        ("inventory_asp_opm_missing", "customer_concentration"),
        "AI server PCB/substrate second-wave names need ASP, inventory, OPM, customer diversification, and price-path evidence.",
    ),
    Round186ScoreTarget(
        "MLCC_AI_SERVER_COMPONENTS",
        E2RArchetype.MLCC_AI_SERVER_COMPONENTS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(21, 19, 14, 10, 8, 9, 8),
        ("mlcc", "ai_server_component", "semiconductor_substrate", "automotive_electronics", "camera_module"),
        ("component_mix_improvement", "asp_signal", "inventory_signal", "ai_server_or_auto_mix"),
        ("asp_confirmation", "inventory_normalized", "op_eps_revision", "customer_mix_improvement"),
        ("mlcc_ai_server_keyword_rally", "smartphone_weakness_ignored"),
        ("inventory_build", "asp_missing", "smartphone_weakness", "customer_concentration"),
        ("asp_confirmation", "inventory_normalization", "op_eps_revision", "mix_improvement"),
        ("inventory_risk", "asp_missing", "smartphone_cycle", "customer_concentration"),
        ("inventory_asp_gate", "smartphone_cycle_drag"),
        "MLCC and components can support Stage 2, but Green needs ASP, inventory, mix, and OP/EPS conversion.",
    ),
    Round186ScoreTarget(
        "CAMERA_LIDAR_ADAS_ELECTRONICS",
        E2RArchetype.CAMERA_LIDAR_ADAS_ELECTRONICS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(20, 19, 13, 10, 8, 9, 8),
        ("camera_module", "lidar", "adas", "robotics_sensor", "ar_headset_sensor"),
        ("strategic_collaboration", "equity_stake", "design_win_option", "sensor_capacity_expansion"),
        ("commercial_revenue", "customer_design_win", "mass_production", "op_eps_revision", "apple_concentration_relief"),
        ("lidar_name_rally_without_revenue", "strategic_investment_priced_as_contract"),
        ("direct_revenue_missing", "apple_concentration", "adas_adoption_delay", "commercialization_delay"),
        ("commercial_revenue", "design_win", "mass_production", "op_eps_revision"),
        ("direct_revenue_missing", "customer_adoption_missing", "apple_concentration"),
        ("commercial_revenue_missing", "adoption_timing"),
        "Camera/lidar/ADAS exposure is Stage 2 option evidence until design-win revenue and mass production are visible.",
    ),
    Round186ScoreTarget(
        "ON_DEVICE_AI_THEME_KOREA",
        E2RArchetype.ON_DEVICE_AI_THEME_KOREA,
        Round10ThemePosture.REDTEAM_FIRST,
        _w(16, 14, 10, 10, 6, 10, 6),
        ("on_device_ai", "lpddr", "video_ip", "automotive_ap", "npu", "cxl"),
        ("design_win", "license", "customer_pilot", "adoption_signal"),
        ("mass_production_revenue", "royalty_or_license_revenue", "op_eps_revision", "repeat_customer"),
        ("price_only_theme", "npu_keyword_crowded", "cxl_keyword_crowded"),
        ("direct_revenue_missing", "adoption_missing", "customer_detail_missing", "op_eps_revision_missing"),
        ("mass_production_revenue", "royalty_revenue", "op_eps_revision", "customer_detail"),
        ("theme_only", "direct_revenue_missing", "adoption_missing", "price_only_rally"),
        ("theme_only", "revenue_missing", "customer_missing"),
        "On-device AI routes research. It cannot become Green before adoption revenue, royalty/license evidence, and OP/EPS revision.",
    ),
    Round186ScoreTarget(
        "SEMI_CAPEX_ORDER_TO_REVENUE",
        E2RArchetype.SEMI_CAPEX_ORDER_TO_REVENUE,
        Round10ThemePosture.GREEN_POSSIBLE,
        _w(22, 21, 16, 12, 8, 10, 8),
        ("semi_capex", "memory_capex", "foundry_capex", "process_equipment"),
        ("customer_capex_plan", "equipment_order", "shipment_schedule", "order_backlog"),
        ("shipment_to_revenue", "op_eps_revision", "repeat_order", "margin_visible", "60d_mfe_20pct"),
        ("capex_cycle_keyword_rally", "order_priced_before_revenue"),
        ("customer_capex_delay", "order_pushout", "inventory_build", "op_eps_revision_down"),
        ("equipment_order", "shipment_revenue", "op_eps_revision", "repeat_order"),
        ("capex_delay", "order_pushout", "op_eps_missing", "price_only_rally"),
        ("capex_cycle_cap", "order_to_revenue_gap"),
        "Semi CAPEX names can be Stage 3 only when customer CAPEX becomes orders, shipment revenue, OP/EPS, and repeat demand.",
    ),
    Round186ScoreTarget(
        "IP_LEAK_SUPPLY_CHAIN_REDTEAM",
        E2RArchetype.IP_LEAK_SUPPLY_CHAIN_REDTEAM,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        ("k_memory_moat", "hbm_process_advantage", "supply_chain_premium"),
        ("ip_leak_report", "china_memory_catchup_risk", "process_technology_disclosure"),
        ("not_green_until_moat_and_customer_confidence_reconfirmed",),
        ("moat_priced_without_ip_risk",),
        ("ip_leak", "china_cxmt_catchup", "customer_confidence_damage", "valuation_room_reduced"),
        (),
        ("ip_leak", "china_catchup", "customer_confidence_damage"),
        ("ip_leak", "china_competition", "moat_uncertain"),
        "IP leakage and China catch-up are hard RedTeam overlays for memory, equipment, test, and materials supply chains.",
        hard_gate=True,
    ),
    Round186ScoreTarget(
        "LABOR_PRODUCTION_DISRUPTION_OVERLAY",
        E2RArchetype.LABOR_PRODUCTION_DISRUPTION_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        ("samsung_supply_chain", "memory_production", "ai_datacenter_chip_supply"),
        ("strike_notice", "production_disruption_risk", "delivery_delay_risk"),
        ("not_green_until_disruption_resolved_and_delivery_evidence_recovered",),
        ("positive_supply_chain_story_ignores_production_risk",),
        ("labor_disruption", "production_delay", "delivery_delay", "customer_capex_delay", "op_eps_revision_down"),
        (),
        ("labor_disruption", "production_delay", "delivery_delay"),
        ("labor_disruption", "production_risk", "delivery_delay"),
        "Labor or production disruption can hard-cap Samsung-exposed supply-chain candidates even when AI/HBM demand is strong.",
        hard_gate=True,
    ),
    Round186ScoreTarget(
        "DISCLOSURE_CONFIDENCE_CAP",
        E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        Round10ThemePosture.REDTEAM_FIRST,
        CAP_WEIGHT,
        ("opendart_list_only", "media_report", "mou", "loi", "design_win_headline"),
        ("detail_fetch_required", "customer_amount_period_shipment_margin_required"),
        ("not_green_until_binding_detail_and_eps_fcf_path",),
        ("headline_priced_before_detail",),
        ("customer_missing", "order_size_missing", "duration_missing", "shipment_missing", "margin_unknown", "non_binding"),
        ("binding_customer", "order_size", "shipment_schedule", "margin_visible", "op_eps_revision"),
        ("opendart_list_only", "media_only", "mou_loi", "non_binding", "detail_missing"),
        ("detail_missing", "customer_unknown", "amount_unknown", "shipment_unknown"),
        "Round 186 caps OpenDART list-only, media-only, design-win-only, MOU, and missing-detail evidence before Green.",
    ),
)


ROUND186_CASE_CANDIDATES: tuple[Round186CaseCandidate, ...] = (
    Round186CaseCandidate(
        "skc_absolics_glass_substrate_stage2_case",
        "GLASS_SUBSTRATE_ADVANCED_PACKAGING_KOREA",
        "011790",
        "SKC / Absolics glass substrate",
        "KR",
        "success_candidate",
        ("glass_substrate", "advanced_packaging", "chips_grant_75m_usd", "georgia_covington_facility", "test_batch_production", "production_ramp_plan"),
        ("customer_missing", "yield_missing", "revenue_missing", "capex_risk"),
        "stage2_strong_not_green_until_customer_yield_revenue_opm",
        "needs_customer_yield_revenue_price_backfill",
        ("round_186.md Reuters Absolics CHIPS grant", "round_186.md AP Absolics test batch production"),
        "SKC/Absolics has facility, grant, and test-production evidence. Stage 3 waits for customer qualification, yield, shipment, revenue, OPM, and FCF.",
        (E2RArchetype.STAGE2_STRONG_NOT_GREEN, E2RArchetype.COMMERCIALIZATION_FAILURE),
    ),
    Round186CaseCandidate(
        "gaonchips_pfn_samsung_2nm_stage2_case",
        "SYSTEM_SEMI_DESIGN_HOUSE_AI_ORDER",
        "399720",
        "가온칩스 Samsung 2nm / Preferred Networks AI chip design",
        "KR",
        "success_candidate",
        ("preferred_networks_customer", "samsung_2nm_foundry_order", "gaonchips_design_role", "advanced_packaging_included", "generative_ai_hpc_chip"),
        ("order_size_undisclosed", "revenue_recognition_missing", "foundry_execution_risk", "repeat_design_win_missing"),
        "stage2_strong_until_order_size_revenue_repeat_nre_royalty",
        "needs_order_size_revenue_repeat_design_price_backfill",
        ("round_186.md Reuters Samsung 2nm Preferred Networks / Gaonchips",),
        "Customer and design role are strong Stage 2 evidence, but order size, revenue recognition, repeat NRE/royalty, and OP/EPS are required before Stage 3.",
        (E2RArchetype.STAGE2_STRONG_NOT_GREEN, E2RArchetype.DISCLOSURE_CONFIDENCE_CAP),
    ),
    Round186CaseCandidate(
        "hbm_test_equipment_basket_stage3_candidate_case",
        "HBM_TEST_EQUIPMENT_KOREA",
        "089030/232140/003160/092870",
        "테크윙·와이씨·디아이·엑시콘 HBM test equipment basket",
        "KR",
        "success_candidate",
        ("hbm_test_equipment", "sk_hynix_packaging_plant_capex", "sk_hynix_euv_purchase", "customer_capex_macro", "individual_order_needed"),
        ("individual_contract_missing", "shipment_schedule_missing", "op_eps_revision_missing", "price_only_rally_risk"),
        "stage2_macro_stage3_candidate_only_after_individual_order_revision_price_path",
        "needs_contract_shipment_op_revision_mfe_mae_backfill",
        ("round_186.md Reuters SK Hynix packaging plant", "round_186.md Reuters SK Hynix EUV purchase"),
        "HBM CAPEX is real macro evidence, but each listed test-equipment candidate needs customer order, shipment, OP/EPS, repeat order, and price-path validation.",
        (E2RArchetype.SEMI_EQUIPMENT_AI_CAPEX, E2RArchetype.STRUCTURAL_STAGE3_EARLY_CAPTURE),
    ),
    Round186CaseCandidate(
        "hanwha_precision_spinoff_hbm_equipment_stage2_4c_watch_case",
        "ADVANCED_PACKAGING_EQUIPMENT_BASKET",
        "012450/HANWHA_PRECISION",
        "한화정밀기계 / 한화 산업솔루션 HBM equipment option",
        "KR",
        "failed_rerating",
        ("hbm_equipment_option", "industrial_solutions_spinoff", "semiconductor_equipment_unit_focus"),
        ("actual_order_missing", "share_price_failed_minus_8pct", "governance_allocation_risk", "minority_value_unclear"),
        "stage2_option_but_governance_and_price_failed_watch",
        "needs_actual_order_governance_price_backfill",
        ("round_186.md Reuters Hanwha spin-off and price reaction",),
        "HBM equipment option is Stage 2 attention, but spin-off, governance, value allocation, and price-failed evidence cap Stage 3.",
        (E2RArchetype.EVIDENCE_GOOD_BUT_PRICE_FAILED, E2RArchetype.CAPITAL_ALLOCATION_DILUTION_OVERLAY),
    ),
    Round186CaseCandidate(
        "lg_innotek_aeva_lidar_stage2_case",
        "CAMERA_LIDAR_ADAS_ELECTRONICS",
        "011070",
        "LG이노텍 Aeva lidar strategic collaboration",
        "KR",
        "success_candidate",
        ("aeva_strategic_collaboration", "lg_innotek_32m_usd_equity_stake", "lidar_sensor_option", "robotics_ar_sensing_option"),
        ("direct_revenue_missing", "apple_concentration", "adas_adoption_timing_risk", "commercialization_delay"),
        "stage2_option_not_green_before_design_win_revenue_mass_production",
        "needs_design_win_revenue_adoption_price_backfill",
        ("round_186.md Reuters LG Innotek Aeva collaboration",),
        "LG Innotek receives Stage 2 option credit for lidar collaboration, but revenue, design win, mass production, OP/EPS, and Apple concentration relief are required.",
        (E2RArchetype.STAGE2_EVIDENCE_NOT_GREEN,),
    ),
    Round186CaseCandidate(
        "ai_server_pcb_mlcc_second_wave_stage3_candidate_case",
        "AI_SERVER_PCB_SUBSTRATE_SECOND_WAVE",
        "353200/222800/007810/356860",
        "대덕전자·심텍·코리아써키트·티엘비 AI server PCB/substrate basket",
        "KR",
        "success_candidate",
        ("ai_server_pcb", "high_layer_pcb", "fc_bga", "server_board", "asp_confirmation_needed", "inventory_normalization_needed"),
        ("inventory_risk", "customer_concentration", "op_eps_missing", "price_only_rally_risk"),
        "stage2_to_stage3_candidate_requires_asp_inventory_opm_customer",
        "needs_asp_inventory_opm_customer_price_backfill",
        ("round_186.md AI server PCB/substrate second-wave basket",),
        "AI server PCB/substrate can be a Stage 2~3 path only if ASP, inventory, OPM, customer diversification, and price path align.",
        (E2RArchetype.ADVANCED_PACKAGING_PCB, E2RArchetype.STRUCTURAL_STAGE3_EARLY_CAPTURE),
    ),
    Round186CaseCandidate(
        "samsung_electromechanics_mlcc_ai_server_stage2_case",
        "MLCC_AI_SERVER_COMPONENTS",
        "009150",
        "삼성전기 MLCC / substrate / AI server components",
        "KR",
        "success_candidate",
        ("mlcc", "semiconductor_substrate", "ai_server_component_exposure", "automotive_electronics_mix", "asp_inventory_gate"),
        ("asp_missing", "inventory_risk", "smartphone_weakness", "customer_mix_unverified"),
        "stage2_component_mix_option_before_asp_inventory_op_eps",
        "needs_asp_inventory_mix_op_revision_price_backfill",
        ("round_186.md Samsung Electro-Mechanics MLCC/substrate component context",),
        "Samsung Electro-Mechanics is Stage 2 option evidence until ASP, inventory normalization, mix, and OP/EPS conversion are visible.",
        (E2RArchetype.ELECTRONIC_COMPONENTS_MLCC_SENSOR,),
    ),
    Round186CaseCandidate(
        "on_device_ai_theme_korea_stage1_2_4b_watch_case",
        "ON_DEVICE_AI_THEME_KOREA",
        "080220/094360/054450/396270",
        "제주반도체·칩스앤미디어·텔레칩스·넥스트칩 on-device AI basket",
        "KR",
        "4b_watch",
        ("on_device_ai", "lpddr", "video_ip", "automotive_ap", "npu", "design_win_watch"),
        ("direct_revenue_missing", "mass_production_missing", "op_eps_revision_missing", "price_only_theme_risk"),
        "stage1_2_theme_route_but_price_only_rally_is_4b_watch",
        "needs_design_win_revenue_royalty_price_backfill",
        ("round_186.md on-device AI / NPU Korea basket",),
        "On-device AI names route research, but price-only moves before adoption revenue, royalty/license, mass production, and OP/EPS become 4B-watch.",
        (E2RArchetype.PRICE_ONLY_RALLY, E2RArchetype.CROWDED_RERATING_4B_WATCH),
    ),
    Round186CaseCandidate(
        "semi_capex_order_to_revenue_stage3_candidate_case",
        "SEMI_CAPEX_ORDER_TO_REVENUE",
        "240810/036930/084370/281820",
        "원익IPS·주성엔지니어링·유진테크·케이씨텍 semi CAPEX equipment basket",
        "KR",
        "success_candidate",
        ("semi_capex", "customer_capex_plan", "equipment_order_needed", "shipment_to_revenue_needed", "op_eps_revision_needed"),
        ("customer_capex_delay", "order_pushout", "op_eps_missing", "inventory_build"),
        "stage2_to_stage3_only_when_capex_becomes_order_revenue_revision",
        "needs_customer_order_shipment_op_revision_price_backfill",
        ("round_186.md semi CAPEX order-to-revenue rule",),
        "Semi CAPEX candidates need customer orders, shipment-to-revenue, OP/EPS revision, repeat demand, and price-path validation.",
        (E2RArchetype.SEMI_EQUIPMENT_CAPEX, E2RArchetype.STRUCTURAL_STAGE3_EARLY_CAPTURE),
    ),
    Round186CaseCandidate(
        "samsung_supply_chain_labor_disruption_4c_case",
        "LABOR_PRODUCTION_DISRUPTION_OVERLAY",
        "005930",
        "삼성전자 노동·생산 차질 supply-chain overlay",
        "KR",
        "4c_thesis_break",
        ("strike_notice", "45000_plus_workers_possible", "memory_supply_chain_disruption_risk", "ai_datacenter_chip_supply_risk"),
        ("labor_disruption", "production_delay_risk", "delivery_delay_risk", "op_eps_revision_down_risk"),
        "hard_redteam_overlay_for_samsung_exposed_supply_chain",
        "needs_disruption_resolution_and_delivery_price_backfill",
        ("round_186.md Reuters Samsung strike threat",),
        "Labor or production disruption remains visible as a hard/soft 4C overlay for Samsung-exposed equipment, material, and component candidates.",
        (E2RArchetype.OPERATIONAL_TRUST_BREAK,),
    ),
    Round186CaseCandidate(
        "korea_memory_ip_leak_cxmt_4c_case",
        "IP_LEAK_SUPPLY_CHAIN_REDTEAM",
        "005930/000660/KR_MEMORY_SUPPLY_CHAIN",
        "한국 메모리 IP leakage / CXMT catch-up overlay",
        "KR",
        "4c_thesis_break",
        ("ip_leak_report", "cxmt_china_memory_catchup", "dram_hbm_process_moat_risk", "customer_confidence_risk"),
        ("ip_leak", "china_catchup", "valuation_room_reduced", "customer_confidence_damage"),
        "hard_redteam_overlay_for_k_semiconductor_premium",
        "needs_ip_case_resolution_moat_price_backfill",
        ("round_186.md Reuters Korea prosecutors CXMT leak case",),
        "IP leakage and China catch-up risk reduce valuation room across memory, equipment, test, materials, and component supply chains.",
        (E2RArchetype.LEGAL_REGULATORY_REDTEAM, E2RArchetype.THESIS_BREAK_4C),
    ),
    Round186CaseCandidate(
        "glass_substrate_commercialization_risk_case",
        "GLASS_SUBSTRATE_ADVANCED_PACKAGING_KOREA",
        "011790/GLASS_BASKET",
        "유리기판 commercialization risk reference",
        "KR",
        "failed_rerating",
        ("factory_and_grant_stage2", "test_batch_production", "production_ramp_plan"),
        ("customer_qualification_missing", "yield_missing", "shipment_missing", "opm_missing", "basket_rally_before_revenue"),
        "factory_grant_is_stage2_not_commercial_green",
        "needs_customer_yield_shipment_opm_price_backfill",
        ("round_186.md AP Absolics ramp plan and commercialization cap",),
        "Glass substrate factory and grant evidence can be strong but should remain commercialization-gated before customer qualification, yield, shipment, and OPM.",
        (E2RArchetype.COMMERCIALIZATION_FAILURE, E2RArchetype.DISCLOSURE_CONFIDENCE_CAP),
    ),
    Round186CaseCandidate(
        "r2_loop12_disclosure_confidence_reference_case",
        "DISCLOSURE_CONFIDENCE_CAP",
        "R2_DISCLOSURE_CAP",
        "R2 Loop 12 order/design-win disclosure confidence reference",
        "KR",
        "failed_rerating",
        ("watch_disclosure_detail_required", "customer_amount_period_shipment_required", "margin_required", "parser_confidence_required"),
        ("opendart_list_only", "media_only", "mou_loi", "non_binding", "order_size_missing", "customer_missing"),
        "list_media_design_win_only_cannot_create_green",
        "needs_opendart_detail_parser_and_contract_backfill",
        ("round_186.md OpenDART detail and no-invented-fields rule",),
        "Round 186 explicitly keeps list-only, media-only, MOU/LOI, design-win-only, and missing-detail evidence out of Stage 3-Green.",
    ),
)


ROUND186_SCORE_STAGE_PRICE_ALIGNMENT: tuple[Round186ScoreStagePriceAlignment, ...] = (
    Round186ScoreStagePriceAlignment("skc_absolics_glass_substrate_stage2_case", "Stage 2 strong", "Facility/grant/test production exists; KRX and customer-yield price backfill required", "commercialization_gate_not_green", "credit advanced packaging and grant; cap before customer, yield, shipment, revenue, and OPM"),
    Round186ScoreStagePriceAlignment("gaonchips_pfn_samsung_2nm_stage2_case", "Stage 2 strong", "Customer and technology node visible; order size and listed-company revenue missing", "design_win_to_revenue_gate", "credit customer/design role; cap before order size, revenue, repeat design win, and OP/EPS"),
    Round186ScoreStagePriceAlignment("hbm_test_equipment_basket_stage3_candidate_case", "Stage 2~3 candidate", "Macro CAPEX visible; individual order and 60D/120D MFE backfill required", "stage3_candidate_if_order_revision_price_align", "credit HBM test bottleneck; cap if customer order or OP/EPS missing"),
    Round186ScoreStagePriceAlignment("hanwha_precision_spinoff_hbm_equipment_stage2_4c_watch_case", "Stage 2 + governance/price cap", "HBM equipment option exists but price failed and governance allocation is unclear", "evidence_good_but_price_failed", "apply governance and value-allocation haircut until actual order and shareholder-value link appear"),
    Round186ScoreStagePriceAlignment("ai_server_pcb_mlcc_second_wave_stage3_candidate_case", "Stage 2~3 candidate", "AI server substrate/MLCC basket needs ASP, inventory, OPM, and customer backfill", "stage3_candidate_if_asp_inventory_opm_align", "credit second-wave component exposure; cap when inventory or customer detail is missing"),
    Round186ScoreStagePriceAlignment("on_device_ai_theme_korea_stage1_2_4b_watch_case", "Stage 1/2 -> 4B-watch", "Theme can run before mass-production revenue", "price_only_theme_requires_4b_watch", "route research, but block Green before design-win revenue, royalty/license, mass production, and OP/EPS"),
    Round186ScoreStagePriceAlignment("samsung_supply_chain_labor_disruption_4c_case", "4C overlay", "Labor/production disruption can interrupt delivery and customer confidence", "hard_redteam_alignment", "apply operational disruption overlay to Samsung-exposed supply-chain candidates"),
    Round186ScoreStagePriceAlignment("korea_memory_ip_leak_cxmt_4c_case", "4C overlay", "IP leakage and China catch-up reduce Korea semiconductor moat and valuation room", "hard_redteam_alignment", "apply IP/security overlay across memory, equipment, test, materials, and components"),
)


ROUND186_PRICE_FIELDS: tuple[str, ...] = (
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
    "relative_strength_vs_kosdaq",
    "relative_strength_vs_semiconductor_basket",
    "relative_strength_vs_ai_hardware_basket",
    "relative_strength_vs_hbm_equipment_basket",
    "contract_amount",
    "contract_counterparty",
    "contract_period",
    "order_size",
    "customer_name",
    "design_win_flag",
    "tapeout_flag",
    "mass_production_flag",
    "shipment_schedule",
    "revenue_recognition_timing",
    "op_revision_before_stage3",
    "op_revision_after_stage3",
    "eps_revision_before_stage3",
    "eps_revision_after_stage3",
    "opm",
    "fcf_signal",
    "inventory_signal",
    "asp_signal",
    "yield_signal",
    "customer_qualification_status",
    "customer_diversification_flag",
    "capex_linked_customer",
    "customer_capex_delay_flag",
    "ip_leak_risk_flag",
    "labor_disruption_flag",
    "production_disruption_flag",
    "media_report_only_flag",
    "mou_loi_flag",
    "non_binding_flag",
    "cb_bw_or_dilution_flag",
    "disclosure_confidence",
    "valuation_at_stage3",
    "valuation_at_stage4b",
)


def round186_target_for(target_id: str) -> Round186ScoreTarget | None:
    for target in ROUND186_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round186_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND186_CASE_CANDIDATES:
        target = round186_target_for(candidate.target_id)
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
                f"Round186 R2 Loop-12 Korea AI/semiconductor/electronics case for {candidate.target_id}; "
                "calibration-only and focused on order/customer/shipment, OP/EPS/FCF, price path, commercialization gates, and IP/labor/disclosure RedTeam."
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
            score_price_alignment=_round186_score_price_alignment(candidate),
            rerating_result=_round186_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
            score_weight_hint={
                "eps_fcf": _numeric_weight(weights["eps_fcf_opm"]),
                "visibility": _numeric_weight(weights["customer_contract_shipment_visibility"]),
                "bottleneck": _numeric_weight(weights["bottleneck_process_adoption"]),
                "early_price_validation": _numeric_weight(weights["early_price_validation"]),
                "production_yield_diversification": _numeric_weight(weights["mass_production_yield_diversification"]),
                "redteam": _numeric_weight(weights["ip_labor_security_disclosure_redteam"]),
                "valuation_4b_room": _numeric_weight(weights["valuation_4b_room"]),
            },
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "stage3_early_catch_requires_5_of_8_loop12_conditions",
                "stage4b_cooling_requires_4_of_6_loop12_conditions",
                "require_customer_order_shipment_op_eps_price_path_for_green",
                "ip_labor_production_and_disclosure_can_block_green",
                "design_win_mou_media_only_cannot_create_stage3",
                "do_not_invent_contract_prices_yield_shipments_mfe_mae_or_customers",
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


def round186_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND186_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "eps_fcf_opm": str(weights["eps_fcf_opm"]),
                "customer_contract_shipment_visibility": str(weights["customer_contract_shipment_visibility"]),
                "bottleneck_process_adoption": str(weights["bottleneck_process_adoption"]),
                "early_price_validation": str(weights["early_price_validation"]),
                "mass_production_yield_diversification": str(weights["mass_production_yield_diversification"]),
                "ip_labor_security_disclosure_redteam": str(weights["ip_labor_security_disclosure_redteam"]),
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


def round186_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND186_CASE_CANDIDATES:
        target = round186_target_for(candidate.target_id)
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


def round186_stage_date_rows() -> tuple[dict[str, str], ...]:
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
        for target in ROUND186_SCORE_TARGETS
    )


def round186_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round186_backfill": "true"} for field in ROUND186_PRICE_FIELDS)


def round186_base_score_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND186_BASE_SCORE_WEIGHTS)


def round186_stage_cap_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND186_STAGE_CAPS)


def round186_score_stage_price_alignment_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND186_SCORE_STAGE_PRICE_ALIGNMENT)


def round186_summary() -> dict[str, int | bool]:
    records = round186_case_records()
    return {
        "target_count": len(ROUND186_SCORE_TARGETS),
        "source_canonical_target_count": ROUND186_SOURCE_CANONICAL_TARGET_COUNT,
        "case_candidate_count": len(records),
        "base_score_axis_count": len(ROUND186_BASE_SCORE_WEIGHTS),
        "stage_cap_count": len(ROUND186_STAGE_CAPS),
        "score_stage_price_alignment_count": len(ROUND186_SCORE_STAGE_PRICE_ALIGNMENT),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "hard_gate_target_count": sum(1 for target in ROUND186_SCORE_TARGETS if target.hard_gate),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round186_r2_loop12_reports(
    *,
    output_directory: str | Path = ROUND186_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND186_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND186_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round186_r2_loop12_ai_semiconductor_electronics_summary.md",
        "case_matrix": output / "round186_r2_loop12_case_matrix.csv",
        "stage_date_plan": output / "round186_r2_loop12_stage_date_plan.csv",
        "green_guardrails": output / "round186_r2_loop12_green_guardrails.md",
        "risk_overlays": output / "round186_r2_loop12_risk_overlays.md",
        "price_validation_plan": output / "round186_r2_loop12_price_validation_plan.md",
        "price_fields": output / "round186_r2_loop12_price_fields.csv",
        "base_score_weights": output / "round186_r2_loop12_base_score_weights.csv",
        "stage_caps": output / "round186_r2_loop12_stage_caps.csv",
        "score_stage_price_alignment": output / "round186_r2_loop12_score_stage_price_alignment.csv",
        "score_stage_price_alignment_md": output / "round186_r2_loop12_score_stage_price_alignment.md",
    }
    _write_case_jsonl(round186_case_records(), cases)
    _write_rows(round186_score_profile_rows(), score_profiles)
    _write_rows(round186_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round186_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round186_price_field_rows(), paths["price_fields"])
    _write_rows(round186_base_score_weight_rows(), paths["base_score_weights"])
    _write_rows(round186_stage_cap_rows(), paths["stage_caps"])
    _write_rows(round186_score_stage_price_alignment_rows(), paths["score_stage_price_alignment"])
    paths["summary"].write_text(render_round186_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round186_green_guardrail_markdown(), encoding="utf-8")
    paths["risk_overlays"].write_text(render_round186_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round186_price_validation_plan_markdown(), encoding="utf-8")
    paths["score_stage_price_alignment_md"].write_text(render_round186_score_stage_price_alignment_markdown(), encoding="utf-8")
    return paths


def render_round186_summary_markdown() -> str:
    summary = round186_summary()
    lines = [
        "# Round-186 R2 Loop-12 Korea AI / Semiconductor / Electronics Summary",
        "",
        f"- source_round: `{ROUND186_SOURCE_ROUND_PATH}`",
        f"- large_sector: `{Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS.value}`",
        "- loop: `R2 Loop 12 / v12.0`",
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
        "- R2 Loop 12 is Korea-first and reduces repeated focus on prior central HBM names.",
        "- Example: SKC/Absolics has grant, factory, and test production, but customer, yield, shipment, revenue, and OPM still gate Stage 3.",
        "- Example: 가온칩스 has customer/design-role evidence, but order size and revenue recognition are missing before Stage 3.",
        "- Example: HBM test equipment can move from Stage 2 to Stage 3 only after individual customer orders, shipment schedule, OP/EPS revision, and price-path validation.",
        "- Example: Samsung labor disruption and CXMT/IP leakage are RedTeam overlays, not positive evidence.",
    ]
    return "\n".join(lines) + "\n"


def render_round186_green_guardrail_markdown() -> str:
    lines = [
        "# Round-186 R2 Loop-12 Green Guardrails",
        "",
        "Stage 3-Green is not granted for AI, HBM, glass substrate, NPU, design-win, MOU, or media-report words alone.",
        "",
        "## Stage 3 Early Catch",
        "",
        "R2 Loop 12 requires at least 5 of 8 checks:",
    ]
    stage3 = next(item for item in ROUND186_STAGE_CAPS if item.stage_band == "Stage 3")
    lines.extend(f"- `{field}`" for field in stage3.required_evidence)
    lines.extend(
        [
            "",
            "## What This Means",
            "",
            "- 유리기판: 공장·보조금은 Stage 2지만 고객·수율·출하·매출 전에는 Green 금지.",
            "- 디자인하우스: 고객명과 설계 역할은 강하지만 order size와 매출 인식 전에는 Green 금지.",
            "- HBM 테스트/장비: 고객사 CAPEX는 macro evidence이고, 개별 장비 수주·출하·OP/EPS가 필요.",
            "- PCB/MLCC: AI server exposure만으로 부족하고 ASP, 재고, OPM, 고객다변화가 필요.",
            "- IP leak, 노동·생산 차질, CAPEX 지연, 공시 detail 부족은 Green을 막을 수 있다.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round186_risk_overlay_markdown() -> str:
    lines = [
        "# Round-186 R2 Loop-12 Risk Overlays",
        "",
        "| target | hard gate | red flags |",
        "| --- | --- | --- |",
    ]
    for target in ROUND186_SCORE_TARGETS:
        lines.append(f"| `{target.target_id}` | {str(target.hard_gate).lower()} | {', '.join(target.red_flags)} |")
    lines.extend(
        [
            "",
            "## Hard 4C Examples",
            "",
            "- `IP_LEAK_SUPPLY_CHAIN_REDTEAM`: IP leakage and China memory catch-up reduce Korea semiconductor moat and valuation room.",
            "- `LABOR_PRODUCTION_DISRUPTION_OVERLAY`: labor or production disruption can damage delivery reliability and customer confidence.",
            "- `DISCLOSURE_CONFIDENCE_CAP`: list-only, media-only, MOU/LOI, order-size missing, customer missing, or shipment missing cannot create Green.",
            "",
            "Simple example: if `as_of_date=2025-01-01`, a later customer qualification result cannot be used to make SKC/Absolics Green on that date.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round186_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-186 R2 Loop-12 Price Validation Plan",
        "",
        "R2 Loop 12 must backfill contract/order fields, shipment/yield fields, price-path fields, and IP/labor/disclosure fields together.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND186_PRICE_FIELDS)
    lines.extend(
        [
            "",
            "## Backfill Priorities",
            "",
            "- `skc_absolics_glass_substrate_stage2_case`: customer, yield, shipment, revenue, OPM, and glass-basket price path.",
            "- `gaonchips_pfn_samsung_2nm_stage2_case`: order size, tape-out, revenue recognition, repeat design win, and OP/EPS.",
            "- `hbm_test_equipment_basket_stage3_candidate_case`: individual order, shipment schedule, OP/EPS, repeat order, MFE/MAE, and relative strength.",
            "- `ai_server_pcb_mlcc_second_wave_stage3_candidate_case`: ASP, inventory normalization, OPM, customer diversification, and price path.",
            "- `samsung_supply_chain_labor_disruption_4c_case` and `korea_memory_ip_leak_cxmt_4c_case`: resolution status and valuation-room impact.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round186_score_stage_price_alignment_markdown() -> str:
    lines = [
        "# Round-186 R2 Loop-12 Score / Stage / Price Alignment",
        "",
        "| case | detected stage | price path status | verdict | adjustment |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in ROUND186_SCORE_STAGE_PRICE_ALIGNMENT:
        lines.append(f"| `{row.case_id}` | {row.detected_stage} | {row.price_path_status} | {row.verdict} | {row.normalization_adjustment} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- SKC/Absolics and 가온칩스 are strong Stage 2 examples, not automatic Stage 3.",
            "- HBM test equipment and AI server PCB/MLCC baskets are Stage 2~3 candidates only after order/revenue/revision and price-path validation.",
            "- On-device AI is a research route, but price-only moves are 4B-watch until adoption revenue appears.",
            "- Labor disruption and IP leakage are RedTeam overlays that can interrupt otherwise positive R2 narratives.",
        ]
    )
    return "\n".join(lines) + "\n"


def _round186_score_price_alignment(candidate: Round186CaseCandidate) -> str:
    if candidate.case_type in {"success_candidate", "structural_success"}:
        return "unknown"
    if candidate.case_type in {"event_premium", "4b_watch", "cyclical_success"}:
        return "price_moved_without_evidence"
    if candidate.case_type == "4c_thesis_break":
        return "false_positive_score"
    if candidate.case_type == "failed_rerating":
        return "evidence_good_but_price_failed"
    return "unknown"


def _round186_rerating_result(candidate: Round186CaseCandidate) -> str:
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
    "ROUND186_BASE_SCORE_WEIGHTS",
    "ROUND186_CASE_CANDIDATES",
    "ROUND186_DEFAULT_CASES_PATH",
    "ROUND186_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND186_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND186_PRICE_FIELDS",
    "ROUND186_SCORE_STAGE_PRICE_ALIGNMENT",
    "ROUND186_SCORE_TARGETS",
    "ROUND186_SOURCE_CANONICAL_TARGET_COUNT",
    "ROUND186_SOURCE_CANONICAL_TARGET_IDS",
    "ROUND186_STAGE_CAPS",
    "render_round186_green_guardrail_markdown",
    "render_round186_price_validation_plan_markdown",
    "render_round186_risk_overlay_markdown",
    "render_round186_score_stage_price_alignment_markdown",
    "render_round186_summary_markdown",
    "round186_base_score_weight_rows",
    "round186_case_candidate_rows",
    "round186_case_records",
    "round186_price_field_rows",
    "round186_score_profile_rows",
    "round186_score_stage_price_alignment_rows",
    "round186_stage_cap_rows",
    "round186_stage_date_rows",
    "round186_summary",
    "round186_target_for",
    "write_round186_r2_loop12_reports",
]
