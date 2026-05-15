"""Round-41 R1 industrial/order/infrastructure calibration pack.

Round 41 is the first sector-specific round under the Round-40 protocol. It
builds R1 case records, shadow score-weight drafts, stage-date guidance, and
price-path validation plans for industrial orders and infrastructure.

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


ROUND41_SOURCE_ROUND_PATH = "docs/round/round_41.md"
ROUND41_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round41_r1_industrial_infra"
ROUND41_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r1_round41.jsonl"
ROUND41_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round41_r1_v1.csv"


@dataclass(frozen=True)
class Round41ScoreWeightDraft:
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
class Round41ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round41ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    normalization_point: str

    @property
    def large_sector(self) -> Round10LargeSector:
        return Round10LargeSector.INDUSTRIAL_ORDERS_INFRA

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round41CaseCandidate:
    case_id: str
    target_id: str
    symbol: str
    company_name: str
    market: str
    case_type: str
    stage1_date: date | None
    stage2_date: date | None
    stage4b_date: date | None
    stage4c_date: date | None
    evidence_fields: tuple[str, ...]
    red_flag_fields: tuple[str, ...]
    alignment_hint: str
    price_validation_status: str
    source_refs: tuple[str, ...]
    notes: str

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND41_SCORE_TARGETS: tuple[Round41ScoreTarget, ...] = (
    Round41ScoreTarget(
        "GRID_TRANSFORMER_SHORTAGE",
        E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round41ScoreWeightDraft(22, 25, 23, 12, 12, 1, 5),
        ("ai_data_center_power_demand", "ev_grid_demand", "transformer_shortage_news", "lead_time_extended"),
        ("supply_contract", "backlog_growth", "earnings_surprise", "op_eps_revision"),
        ("fy1_fy2_fy3_revision", "long_lead_time", "price_increase", "old_industrial_frame_rerating"),
        ("valuation_band_expansion", "sector_wide_ai_grid_consensus", "capacity_addition_news"),
        ("new_order_slowdown", "low_margin_contract", "capa_normalization", "data_center_project_delay"),
        ("contract_quality", "lead_time_extended", "pricing_power", "op_eps_revision", "backlog_growth"),
        ("capa_normalization", "low_margin_contract", "project_delay"),
        "Transformer shortage can be Green, but only when contract quality, lead time, pricing, backlog, and EPS revision are source-backed.",
    ),
    Round41ScoreTarget(
        "CONTRACT_BACKLOG_INDUSTRIAL",
        E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round41ScoreWeightDraft(20, 24, 18, 13, 12, 1, 5),
        ("supply_contract_news", "trading_value_breakout", "backlog_keyword"),
        ("contract_amount_to_sales", "contract_duration", "delivery_schedule", "op_eps_revision"),
        ("multi_year_backlog", "margin_visible", "capacity_constraint", "fy1_fy2_revision"),
        ("crowded_order_story", "target_price_cluster", "new_order_growth_slowdown"),
        ("contract_cancelled", "delivery_delay", "margin_miss", "customer_credit_issue"),
        ("contract_amount_to_sales", "contract_duration", "delivery_schedule", "margin_visible", "op_eps_revision"),
        ("contract_quality_unclear", "delivery_delay", "margin_uncertainty"),
        "Generic industrial backlog requires contract size, duration, delivery, margin, and EPS evidence together.",
    ),
    Round41ScoreTarget(
        "DEFENSE_GOVERNMENT_BACKLOG",
        E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round41ScoreWeightDraft(20, 24, 17, 14, 14, 3, 5),
        ("geopolitical_budget_growth", "defense_export_news", "government_customer"),
        ("official_contract", "multi_year_delivery", "order_backlog_growth", "op_eps_revision"),
        ("government_backlog_to_sales", "delivery_visibility", "opm_improvement", "export_mix_growth"),
        ("defense_rerating_crowded", "capital_raise_after_runup", "valuation_band_full"),
        ("delivery_delay", "cost_overrun", "export_permit_issue", "dilution_shock", "contract_cancelled"),
        ("government_customer", "multi_year_contract", "delivery_schedule", "backlog_growth", "opm_improvement"),
        ("delivery_delay", "cost_overrun", "export_permit_issue", "dilution"),
        "Defense backlog can be Green, but capital allocation and delivery risk are first-class guardrails.",
    ),
    Round41ScoreTarget(
        "DEFENSE_TECH_AUTONOMOUS_SYSTEMS",
        E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round41ScoreWeightDraft(20, 22, 15, 15, 14, 2, 5),
        ("autonomous_weapon_keyword", "low_cost_munition_framework", "prototype_program"),
        ("framework_agreement", "evaluation_schedule", "procurement_quantity_hint"),
        ("program_of_record", "mass_procurement", "production_capacity", "eps_conversion"),
        ("prototype_theme_crowded", "defense_ai_valuation_jump"),
        ("procurement_delay", "program_cancelled", "valuation_overheat", "export_control"),
        ("framework_to_order_conversion", "production_capacity", "customer_budget", "eps_conversion"),
        ("procurement_delay", "valuation_overheat", "program_cancelled"),
        "Autonomous defense systems stay Watch until framework agreements convert into procurement and revenue.",
    ),
    Round41ScoreTarget(
        "DEFENSE_DRONE_COUNTER_UAS",
        E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round41ScoreWeightDraft(20, 22, 14, 14, 13, 3, 5),
        ("drone_or_counter_uas_keyword", "loitering_munition", "directed_energy_keyword"),
        ("military_order", "delivery_schedule", "production_capacity"),
        ("repeat_procurement", "export_customer", "margin_visible"),
        ("drone_theme_crowding", "mna_dilution"),
        ("export_control", "procurement_delay", "production_failure", "dilution"),
        ("actual_order", "delivery_schedule", "production_capacity", "repeat_procurement"),
        ("mna_dilution", "export_control", "prototype_only"),
        "Drone/counter-UAS evidence must move beyond theme and into repeat procurement.",
    ),
    Round41ScoreTarget(
        "DEFENSE_AI_SOFTWARE_INTELLIGENCE",
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round41ScoreWeightDraft(19, 21, 10, 15, 14, 0, 5),
        ("maven_like_program", "military_ai_software", "command_control_software"),
        ("prototype_contract", "government_customer", "deployment_schedule"),
        ("program_of_record", "recurring_license", "gross_margin_visible"),
        ("defense_ai_software_crowded", "multiple_expansion_without_arr"),
        ("prototype_not_renewed", "political_ethics_risk", "budget_cycle_cut"),
        ("government_customer", "deployment_schedule", "recurring_license", "gross_margin_visible"),
        ("prototype_stage", "political_ethics_risk", "budget_cycle"),
        "Military AI software can rerate only when prototype revenue becomes repeatable software revenue.",
    ),
    Round41ScoreTarget(
        "SHIPBUILDING_OFFSHORE_BACKLOG",
        E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round41ScoreWeightDraft(20, 22, 18, 13, 13, 1, 5),
        ("newbuilding_price_up", "ship_order_recovery", "lng_or_offshore_order"),
        ("large_order", "low_margin_backlog_rolloff", "high_margin_delivery_start", "op_eps_revision"),
        ("backlog_quality_improves", "fy2_fy3_margin_recognition", "cost_pressure_controlled"),
        ("shipbuilder_group_rally", "newbuilding_price_narrative_crowded", "target_price_cluster"),
        ("steel_plate_cost_spike", "labor_cost_spike", "order_slowdown", "contract_cancelled", "delivery_delay"),
        ("newbuilding_price_up", "low_margin_backlog_rolloff", "high_margin_delivery_start", "op_eps_revision"),
        ("low_margin_backlog", "steel_plate_cost", "labor_cost", "contract_cancellation"),
        "Shipbuilding Green depends on backlog quality and margin recognition, not backlog quantity alone.",
    ),
    Round41ScoreTarget(
        "RAIL_INFRASTRUCTURE",
        E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round41ScoreWeightDraft(20, 23, 12, 14, 12, 1, 5),
        ("rail_order_news", "foreign_rail_investment", "urban_or_high_speed_rail_policy"),
        ("official_contract", "contract_amount_to_sales", "delivery_schedule"),
        ("delivery_visibility", "margin_visible", "op_eps_revision", "financing_risk_low"),
        ("rail_order_expectation_fully_priced",),
        ("project_delay", "financing_failure", "margin_miss", "contract_cancelled"),
        ("official_contract", "contract_amount_to_sales", "delivery_schedule", "margin_visible"),
        ("project_delay", "margin_uncertainty", "financing"),
        "Rail can be a backlog candidate, but margin and financing must be verified.",
    ),
    Round41ScoreTarget(
        "NUCLEAR_SMR_GRID_POLICY",
        E2RArchetype.NUCLEAR_SMR_GRID_POLICY,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round41ScoreWeightDraft(18, 22, 10, 14, 12, 2, 5),
        ("nuclear_policy", "ai_power_demand", "ppa_or_preferred_bidder_news"),
        ("ppa_or_signed_contract", "permitting_visible", "supplier_revenue_path"),
        ("legal_risk_low", "financing_visible", "fy2_fy3_revenue_visibility"),
        ("nuclear_theme_rally", "policy_premium_crowded"),
        ("legal_injunction", "project_cancelled", "cost_overrun", "financing_failed", "permitting_failed"),
        ("ppa_or_signed_contract", "permitting", "financing", "supplier_revenue_path"),
        ("legal_delay", "cost_overrun", "financing_failed", "policy_headline_only"),
        "Nuclear/SMR needs PPA or signed contract plus legal, permit, cost, and financing clearance.",
    ),
    Round41ScoreTarget(
        "GEOPOLITICAL_RECONSTRUCTION",
        E2RArchetype.THEME_VALUATION_OVERHEAT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round41ScoreWeightDraft(10, 8, 8, 10, 7, 0, 4),
        ("reconstruction_policy", "neom_or_ukraine_theme", "mou_or_bid_news"),
        ("binding_contract", "revenue_schedule", "financing_visible"),
        ("actual_delivery_and_margin", "eps_conversion"),
        ("policy_event_crowded", "event_premium_fades"),
        ("no_contract", "project_delay", "financing_failure", "policy_reversal"),
        ("binding_contract", "revenue_schedule", "financing_visible", "margin_visible"),
        ("actual_contract_missing", "policy_event_only", "mou_only"),
        "Reconstruction and mega-project policy tags are event/watch until binding contract and revenue visibility exist.",
    ),
    Round41ScoreTarget(
        "SMART_FACTORY_AUTOMATION",
        E2RArchetype.ROBOTICS_FACTORY_AUTOMATION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round41ScoreWeightDraft(18, 16, 8, 12, 10, 0, 5),
        ("smart_factory_keyword", "automation_order", "factory_ai_keyword"),
        ("actual_order", "installed_base", "recurring_maintenance_or_software"),
        ("revenue_conversion", "opm_improvement", "customer_diversification"),
        ("automation_theme_crowded",),
        ("mou_or_poc_only", "customer_capex_delay", "no_revenue_conversion"),
        ("actual_order", "installed_base", "recurring_revenue", "opm_improvement"),
        ("mou_only", "poc_only", "revenue_conversion_failure"),
        "Automation needs order-to-revenue conversion; PoC/MOU is not Stage 3 evidence.",
    ),
    Round41ScoreTarget(
        "AI_DATA_CENTER_POWER_EQUIPMENT",
        E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round41ScoreWeightDraft(21, 22, 18, 13, 12, 0, 5),
        ("ai_data_center_power_equipment", "ups_pdu_switchgear_keyword", "data_center_internal_power_demand"),
        ("confirmed_booking", "delivery_schedule", "op_eps_revision"),
        ("bookings_growth", "backlog_growth", "op_margin_improvement", "customer_visible"),
        ("ai_power_equipment_theme_crowded", "capacity_addition_news"),
        ("bookings_slowdown", "low_margin_project", "data_center_capex_delay"),
        ("confirmed_booking", "delivery_schedule", "backlog_growth", "op_margin_improvement"),
        ("bookings_slowdown", "low_margin_project", "capex_delay"),
        "Data-center internal power equipment can be Green only with bookings, delivery, margin, and EPS evidence.",
    ),
)


ROUND41_CASE_CANDIDATES: tuple[Round41CaseCandidate, ...] = (
    Round41CaseCandidate(
        "hd_hyundai_electric_transformer_shortage_candidate",
        "GRID_TRANSFORMER_SHORTAGE",
        "267260",
        "HD현대일렉트릭",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        ("transformer_shortage", "lead_time_extended", "price_increase", "ai_data_center_power_demand"),
        ("capa_normalization", "low_margin_contract"),
        "needs_price_backfill",
        "needs_price_backfill",
        ("Reuters transformer shortage reference",),
        "Transformer shortage is a structural R1 reference, but company-specific stage prices and EPS revision need backfill.",
    ),
    Round41CaseCandidate(
        "hyosung_heavy_transformer_backlog_candidate",
        "GRID_TRANSFORMER_SHORTAGE",
        "298040",
        "효성중공업",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        ("transformer_backlog", "margin_recovery", "op_eps_revision_candidate"),
        ("low_margin_backlog", "capa_normalization"),
        "needs_price_backfill",
        "needs_price_backfill",
        ("Round41 transformer backlog note",),
        "Hyosung Heavy requires backlog-to-sales, margin recovery, and price-path validation.",
    ),
    Round41CaseCandidate(
        "hanwha_aerospace_romania_k9_success_case",
        "DEFENSE_GOVERNMENT_BACKLOG",
        "012450",
        "한화에어로스페이스 루마니아 K9",
        "KR",
        "structural_success",
        None,
        date(2024, 7, 9),
        None,
        None,
        ("government_customer", "multi_year_contract", "delivery_schedule", "order_backlog_growth", "event_day_price_reaction"),
        ("delivery_delay", "cost_overrun", "dilution"),
        "aligned_candidate",
        "needs_price_backfill",
        ("Reuters Romania K9 order",),
        "Reported event-day price reaction was positive, but 1Y/2Y MFE and EPS revision still need source backfill.",
    ),
    Round41CaseCandidate(
        "hanwha_aerospace_europe_land_arms_visibility_candidate",
        "DEFENSE_GOVERNMENT_BACKLOG",
        "012450",
        "한화에어로스페이스 유럽 지상무기",
        "KR",
        "success_candidate",
        None,
        date(2024, 10, 7),
        None,
        None,
        ("europe_sales_visibility", "order_backlog_growth", "local_production_preference"),
        ("delivery_delay", "localization_cost", "dilution"),
        "needs_price_backfill",
        "needs_price_backfill",
        ("Reuters Europe land arms sales visibility",),
        "European land-arms visibility strengthens defense backlog, but delivery and margin recognition remain open.",
    ),
    Round41CaseCandidate(
        "hyundai_rotem_morocco_rail_order_case",
        "RAIL_INFRASTRUCTURE",
        "064350",
        "현대로템 모로코 철도 수주",
        "KR",
        "success_candidate",
        None,
        date(2025, 2, 26),
        None,
        None,
        ("official_contract", "large_contract", "delivery_schedule", "foreign_customer"),
        ("project_delay", "margin_uncertainty", "financing"),
        "unknown_until_backfill",
        "needs_price_backfill",
        ("Reuters Morocco rail order",),
        "Large rail contract is Stage-2 style evidence; OP revision and 180D/1Y MFE need backfill.",
    ),
    Round41CaseCandidate(
        "korean_shipbuilders_contract_rally_case",
        "SHIPBUILDING_OFFSHORE_BACKLOG",
        "KR_SHIPBUILDERS",
        "한국 조선주 수주·선가 랠리",
        "KR",
        "cyclical_success",
        None,
        None,
        None,
        None,
        ("contract_wins", "newbuilding_price_up", "shipbuilder_group_rally"),
        ("low_margin_backlog", "steel_plate_cost", "labor_cost"),
        "cyclical_to_structural_candidate",
        "needs_price_backfill",
        ("WSJ Korean shipbuilder rally",),
        "Shipbuilding rally needs backlog-quality and margin-recognition checks before structural Green.",
    ),
    Round41CaseCandidate(
        "meta_constellation_nuclear_ppa_reference",
        "NUCLEAR_SMR_GRID_POLICY",
        "CEG",
        "Meta-Constellation 원전 PPA",
        "US",
        "success_candidate",
        None,
        date(2025, 6, 3),
        None,
        None,
        ("twenty_year_ppa", "ai_data_center_power_demand", "carbon_free_power_visibility"),
        ("regulatory_risk", "ppa_price", "operating_cost"),
        "korean_equity_mapping_needed",
        "missing_kr_equity_mapping",
        ("Reuters Meta Constellation PPA",),
        "Existing nuclear PPA is stronger than SMR policy talk, but Korean equipment mapping needs direct contract evidence.",
    ),
    Round41CaseCandidate(
        "anduril_lccm_reference_case",
        "DEFENSE_TECH_AUTONOMOUS_SYSTEMS",
        "ANDURIL_REF",
        "Anduril LCCM framework reference",
        "US",
        "success_candidate",
        None,
        date(2026, 5, 13),
        None,
        None,
        ("framework_agreement", "mass_procurement_target", "containerized_munition"),
        ("procurement_delay", "program_cancelled", "valuation_overheat"),
        "not_direct_kr_candidate_yet",
        "missing_public_price_data",
        ("Reuters Pentagon LCCM framework",),
        "Private/reference case for defense-tech procurement path; not direct KR candidate input.",
    ),
    Round41CaseCandidate(
        "palantir_maven_contract_case",
        "DEFENSE_AI_SOFTWARE_INTELLIGENCE",
        "PLTR",
        "Palantir Maven prototype",
        "US",
        "success_candidate",
        None,
        date(2024, 5, 29),
        None,
        None,
        ("prototype_contract", "government_customer", "military_ai_software"),
        ("prototype_stage", "political_ethics_risk", "budget_cycle"),
        "watch_to_green_candidate",
        "needs_price_backfill",
        ("Reuters Palantir Maven prototype",),
        "Prototype contract is Stage-2 style evidence; recurring program-of-record revenue is required for stronger stages.",
    ),
    Round41CaseCandidate(
        "hanwha_aerospace_dilution_risk_case",
        "DEFENSE_GOVERNMENT_BACKLOG",
        "012450",
        "한화에어로스페이스 유상증자 리스크",
        "KR",
        "failed_rerating",
        None,
        date(2025, 3, 27),
        date(2025, 3, 27),
        None,
        ("capital_raise", "regulator_revision_request", "event_day_drawdown"),
        ("dilution", "unclear_use_of_proceeds", "capital_allocation_risk"),
        "capital_allocation_counterexample",
        "needs_price_backfill",
        ("Reuters Hanwha share issuance plan", "Financial Times share sale report"),
        "Strong backlog can still be hit by dilution/capital-allocation risk; this is a R1 RedTeam case.",
    ),
    Round41CaseCandidate(
        "nuscale_cfpp_cancel_4c_case",
        "NUCLEAR_SMR_GRID_POLICY",
        "SMR",
        "NuScale CFPP 취소",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        date(2023, 11, 1),
        ("smr_project", "policy_theme", "customer_subscription_attempt"),
        ("project_cancelled", "cost_overrun", "financing_failed", "customer_subscription_failed"),
        "thesis_break",
        "needs_price_backfill",
        ("NuScale CFPP cancellation reference",),
        "SMR policy narrative breaks when cost, financing, and customer subscription fail.",
    ),
    Round41CaseCandidate(
        "khnp_czech_legal_delay_case",
        "NUCLEAR_SMR_GRID_POLICY",
        "KHNP_CZECH_REF",
        "KHNP 체코 원전 법적 지연",
        "KR",
        "4c_thesis_break",
        None,
        None,
        None,
        date(2025, 5, 1),
        ("nuclear_export_project", "preferred_bidder_or_contract_expected"),
        ("legal_delay", "contract_signing_blocked", "tender_dispute"),
        "legal_delay_4c_watch",
        "missing_direct_symbol_mapping",
        ("AP Czech court KHNP nuclear project",),
        "Legal injunction or tender dispute should block nuclear policy Green until resolved.",
    ),
    Round41CaseCandidate(
        "low_margin_shipbuilding_backlog_counterexample",
        "SHIPBUILDING_OFFSHORE_BACKLOG",
        "LOW_MARGIN_SHIP",
        "저마진 조선 수주잔고 반례",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        ("ship_order_backlog",),
        ("low_margin_backlog", "steel_plate_cost", "labor_cost", "margin_miss"),
        "false_positive_score_risk",
        "needs_price_backfill",
        ("Round41 shipbuilding margin warning",),
        "Backlog quantity alone is insufficient; backlog quality and margin recognition are the score evidence.",
    ),
    Round41CaseCandidate(
        "geopolitical_reconstruction_no_contract_event_watch",
        "GEOPOLITICAL_RECONSTRUCTION",
        "RECON_EVENT",
        "재건·네옴 정책 무계약 이벤트",
        "KR",
        "event_premium",
        None,
        None,
        None,
        None,
        ("reconstruction_policy", "mou_or_bid_news"),
        ("actual_contract_missing", "policy_event_only", "financing_unknown"),
        "event_premium",
        "missing_contract_evidence",
        ("Round41 reconstruction policy warning",),
        "Reconstruction or mega-project policy can route research, but no binding contract means no Green.",
    ),
    Round41CaseCandidate(
        "transformer_capacity_normalization_4b_watch",
        "GRID_TRANSFORMER_SHORTAGE",
        "POWER_EQUIP_4B",
        "전력설비 CAPA 정상화 4B-watch",
        "KR",
        "4b_watch",
        None,
        None,
        None,
        None,
        ("transformer_shortage", "valuation_band_expansion", "sector_wide_ai_grid_consensus"),
        ("capa_addition", "new_order_growth_slowdown", "new_competition"),
        "4b_watch",
        "needs_price_backfill",
        ("Reuters transformer shortage reference",),
        "Transformer shortage can be Green early, but capacity additions and order-growth slowdown trigger 4B-watch.",
    ),
)


ROUND41_PRICE_FIELDS: tuple[str, ...] = (
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
    "below_stage3_price_flag",
    "op_revision_1q",
    "op_revision_1y",
    "eps_revision_1q",
    "eps_revision_1y",
    "backlog_growth",
    "contract_amount_to_sales",
    "contract_duration_months",
    "margin_change",
    "score_price_alignment",
    "price_validation_status",
)


def target_for(target_id: str) -> Round41ScoreTarget | None:
    for target in ROUND41_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round41_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND41_CASE_CANDIDATES:
        target = target_for(candidate.target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {candidate.target_id}")
        weights = target.score_weight.as_dict()
        stage4b_evidence = candidate.evidence_fields if candidate.case_type == "4b_watch" else ()
        stage4c_evidence = candidate.red_flag_fields if candidate.case_type == "4c_thesis_break" else ()
        record = E2RCaseRecord(
            case_id=candidate.case_id,
            symbol=candidate.symbol,
            company_name=candidate.company_name,
            market=candidate.market,
            sector_raw=candidate.target_id,
            primary_archetype=target.canonical_archetype,
            expected_group=candidate.expected_group,
            large_sector=target.large_sector.value,
            case_type=candidate.case_type,
            stage1_date=candidate.stage1_date,
            stage2_date=candidate.stage2_date,
            stage4b_date=candidate.stage4b_date,
            stage4c_date=candidate.stage4c_date,
            evidence_summary=(
                f"Round41 R1 case for {candidate.target_id}; "
                "source-backed values are kept explicit and missing prices remain unfilled."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage2_signals or field in target.green_conditions),
            stage3_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage3_conditions),
            stage4b_evidence=stage4b_evidence,
            stage4c_evidence=stage4c_evidence,
            must_have_fields=target.green_conditions,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason="; ".join(candidate.red_flag_fields) if candidate.case_type in {"failed_rerating", "event_premium", "4c_thesis_break"} else None,
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
                "require_cross_evidence_for_green",
                "theme_label_is_not_score_evidence",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=False,
                price_data_available=False,
                stage_dates_confidence=0.7 if candidate.stage2_date or candidate.stage4c_date else 0.3,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round41_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND41_SCORE_TARGETS:
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
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round41_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND41_CASE_CANDIDATES:
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
                "stage2_date": candidate.stage2_date.isoformat() if candidate.stage2_date else "",
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


def round41_stage_date_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND41_SCORE_TARGETS:
        rows.append(
            {
                "target_id": target.target_id,
                "stage1": "|".join(target.stage1_signals),
                "stage2": "|".join(target.stage2_signals),
                "stage3": "|".join(target.stage3_conditions),
                "stage4b": "|".join(target.stage4b_conditions),
                "stage4c": "|".join(target.stage4c_conditions),
                "production_scoring_changed": "false",
            }
        )
    return tuple(rows)


def round41_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round41_backfill": "true"} for field in ROUND41_PRICE_FIELDS)


def round41_summary() -> dict[str, int | bool]:
    records = round41_case_records()
    return {
        "target_count": len(ROUND41_SCORE_TARGETS),
        "case_candidate_count": len(records),
        "structural_success_count": sum(1 for record in records if record.case_type == "structural_success"),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for record in records if record.case_type == "cyclical_success"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch"),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND41_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND41_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round41_r1_reports(
    *,
    output_directory: str | Path = ROUND41_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND41_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND41_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round41_r1_industrial_infra_summary.md",
        "case_matrix": output / "round41_r1_case_matrix.csv",
        "stage_date_plan": output / "round41_r1_stage_date_plan.csv",
        "green_guardrails": output / "round41_r1_green_guardrails.md",
        "price_validation_plan": output / "round41_r1_price_validation_plan.md",
        "price_fields": output / "round41_r1_price_fields.csv",
    }
    _write_case_jsonl(round41_case_records(), cases)
    _write_rows(round41_score_profile_rows(), score_profiles)
    _write_rows(round41_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round41_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round41_price_field_rows(), paths["price_fields"])
    paths["summary"].write_text(render_round41_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round41_green_guardrail_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round41_price_validation_plan_markdown(), encoding="utf-8")
    return paths


def render_round41_summary_markdown() -> str:
    summary = round41_summary()
    lines = [
        "# Round-41 R1 Industrial Orders / Infrastructure Summary",
        "",
        f"- source_round: `{ROUND41_SOURCE_ROUND_PATH}`",
        "- large_sector: `INDUSTRIAL_ORDERS_INFRA`",
        f"- target_count: {summary['target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- structural_success_count: {summary['structural_success_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- cyclical_success_count: {summary['cyclical_success_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
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
        "- R1 is one of the strongest E2R sectors, but order headlines alone are not enough.",
        "- Stage 3 candidates require contract quality, delivery period, backlog, margin, EPS/OP revision, and price-path validation.",
        "- Example: a transformer shortage headline routes research. It does not create Stage 3-Green unless company-level backlog, margin, and revision evidence are present.",
        "- Example: defense backlog can be strong, but dilution or unclear capital allocation can still trigger RedTeam risk.",
    ]
    return "\n".join(lines) + "\n"


def render_round41_green_guardrail_markdown() -> str:
    lines = [
        "# Round-41 R1 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Red flags |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND41_SCORE_TARGETS:
        lines.append(
            "| "
            f"`{target.target_id}` | {target.posture.value} | "
            f"{', '.join(target.green_conditions)} | {', '.join(target.red_flags)} |"
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not apply these R1 v1.0 weights to production scoring yet.",
            "- Do not treat order headlines, MOU, policy events, or case IDs as score evidence.",
            "- Do not invent contract size, duration, margin, backlog, EPS, FCF, or price path fields.",
            "- Do not lower Stage 3-Green thresholds because R1 is a Green-capable sector.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round41_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-41 R1 Price Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign stage dates from source evidence only.",
        "2. Store stage-date close prices from official price data.",
        "3. Calculate MFE_30D / 90D / 180D / 1Y / 2Y.",
        "4. Calculate MAE_30D / 90D / 180D / 1Y.",
        "5. Calculate peak price, drawdown after peak, and below-stage3 flag.",
        "6. Compare price paths with OP/EPS revision, backlog growth, contract quality, and margin evidence.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | stage2 candidate | check |",
        "| --- | --- | --- |",
    ]
    for row in round41_case_candidate_rows():
        if row["stage2_date"] or row["case_id"] in {
            "hd_hyundai_electric_transformer_shortage_candidate",
            "hyosung_heavy_transformer_backlog_candidate",
            "korean_shipbuilders_contract_rally_case",
            "nuscale_cfpp_cancel_4c_case",
            "khnp_czech_legal_delay_case",
        }:
            stage2 = row["stage2_date"] or row["stage4c_date"] or "needs_source_date"
            lines.append(f"| `{row['case_id']}` | {stage2} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `aligned`: Stage 2/3 evidence and price rerating persist together.",
            "- `cyclical_success`: price worked, but structural EPS persistence is not yet proven.",
            "- `event_premium`: policy, tender, reconstruction, or MOU premium without revenue conversion.",
            "- `false_positive_score`: order or theme looked strong, but margin/EPS/price failed.",
            "- `thesis_break`: cancellation, legal delay, dilution shock, or project failure damages the thesis.",
        ]
    )
    return "\n".join(lines) + "\n"


def _score_price_alignment(candidate: Round41CaseCandidate) -> str:
    if candidate.case_type == "event_premium":
        return "price_moved_without_evidence"
    if candidate.case_type == "failed_rerating":
        return "false_positive_score"
    return "unknown"


def _rerating_result(candidate: Round41CaseCandidate) -> str:
    if candidate.case_type == "event_premium":
        return "event_premium"
    if candidate.case_type == "cyclical_success":
        return "cyclical_rerating"
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    if candidate.case_type == "failed_rerating":
        return "no_rerating"
    return "unknown"


def _write_case_jsonl(records: Iterable[E2RCaseRecord], path: Path) -> Path:
    lines = []
    for record in records:
        record.validate()
        lines.append(json.dumps(record.as_dict(), ensure_ascii=False, sort_keys=True))
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return path


def _write_rows(rows: Iterable[Mapping[str, str]], path: Path) -> Path:
    row_tuple = tuple(rows)
    if not row_tuple:
        path.write_text("", encoding="utf-8")
        return path
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(row_tuple[0].keys()), lineterminator="\n")
        writer.writeheader()
        for row in row_tuple:
            writer.writerow(row)
    return path


__all__ = [
    "ROUND41_CASE_CANDIDATES",
    "ROUND41_DEFAULT_CASES_PATH",
    "ROUND41_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND41_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND41_PRICE_FIELDS",
    "ROUND41_SCORE_TARGETS",
    "ROUND41_SOURCE_ROUND_PATH",
    "Round41CaseCandidate",
    "Round41ScoreTarget",
    "Round41ScoreWeightDraft",
    "render_round41_green_guardrail_markdown",
    "render_round41_price_validation_plan_markdown",
    "render_round41_summary_markdown",
    "round41_case_candidate_rows",
    "round41_case_records",
    "round41_price_field_rows",
    "round41_score_profile_rows",
    "round41_stage_date_rows",
    "round41_summary",
    "target_for",
    "write_round41_r1_reports",
]
