"""Round-193 R2 Loop-7 Korean AI/semiconductor price-path validation pack.

Round 193 is a calibration-only follow-up to the broader R2 Loop-7 AI,
semiconductor, and electronics pack. It adds Korean HBM equipment, AI chip
design-house, HBM catch-up, policy foundry, AI server PCB, and 4B benchmark
cases so future scoring work can separate real customer/order/revenue evidence
from AI narrative and price-only moves.

This module is report/evaluation material only. Production candidate
generation, feature engineering, scoring, staging, and RedTeam code must not
import it.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import CaseDataQuality, E2RCaseRecord, PriceValidation, write_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector


ROUND193_SOURCE_ROUND_PATH = "docs/round/round_193.md"
ROUND193_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round193_r2_loop7_ai_semiconductor_price_validation"
ROUND193_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r2_loop7_round193.jsonl"
ROUND193_DEFAULT_AUDIT_PATH = "data/sector_taxonomy/round193_r2_loop7_ai_semiconductor_price_validation_audit.json"

ROUND193_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "MEMORY_HBM_CAPACITY": E2RArchetype.MEMORY_HBM_CAPACITY.value,
    "MEMORY_HBM_LTA_PREPAYMENT": E2RArchetype.MEMORY_HBM_LTA_PREPAYMENT.value,
    "HBM_CATCHUP_EXECUTION": E2RArchetype.HBM_CATCHUP_EXECUTION.value,
    "SEMI_EQUIPMENT_AI_CAPEX": E2RArchetype.SEMI_EQUIPMENT_AI_CAPEX.value,
    "HBM_BONDER_EQUIPMENT_KOREA": E2RArchetype.HBM_BONDER_EQUIPMENT_KOREA.value,
    "ADVANCED_PACKAGING_EQUIPMENT_KOREA": E2RArchetype.ADVANCED_PACKAGING_EQUIPMENT_KOREA.value,
    "ADVANCED_PACKAGING_PCB": E2RArchetype.ADVANCED_PACKAGING_PCB.value,
    "AI_CHIP_FABRIC_INFRA": E2RArchetype.AI_CHIP_FABRIC_INFRA.value,
    "SYSTEM_SEMI_DESIGN_HOUSE_AI_ORDER": E2RArchetype.SYSTEM_SEMI_DESIGN_HOUSE_AI_ORDER.value,
    "AI_ACCELERATOR_CHIP_PUREPLAY": E2RArchetype.AI_ACCELERATOR_CHIP_PUREPLAY.value,
    "COMMODITY_MEMORY_GENERAL_SEMI": E2RArchetype.COMMODITY_MEMORY_GENERAL_SEMI.value,
    "AI_DATA_CENTER_INFRASTRUCTURE": E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE.value,
    "REDTEAM_ACCOUNTING_TRUST_OVERLAY": E2RArchetype.REDTEAM_ACCOUNTING_TRUST_OVERLAY.value,
    "REDTEAM_OPERATIONAL_TRUST": E2RArchetype.HBM_CATCHUP_EXECUTION_RISK.value,
    "AI_CAPEX_CROWDING_OVERLAY": E2RArchetype.AI_CAPEX_CROWDING_OVERLAY.value,
    "CIRCULAR_AI_FINANCING_OVERLAY": E2RArchetype.CIRCULAR_AI_FINANCING_OVERLAY.value,
    "DISCLOSURE_CONFIDENCE_CAP": E2RArchetype.DISCLOSURE_CONFIDENCE_CAP.value,
    "POLICY_FOUNDRY_EVENT": E2RArchetype.AI_CHIP_FABRIC_INFRA.value,
    "AI_SERVER_PCB_SUBSTRATE_SECOND_WAVE": E2RArchetype.AI_SERVER_PCB_SUBSTRATE_SECOND_WAVE.value,
}

ROUND193_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "company_level_customer_evidence",
    "order_contract_shipment_or_design_win_quality",
    "revenue_recognition_path",
    "gross_margin_or_opm_improvement",
    "eps_fcf_revision",
    "customer_diversification_or_long_term_demand",
    "price_path_after_evidence",
)

ROUND193_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "ai_name_only",
    "hbm_keyword_only",
    "server_theme_only",
    "broker_target_only",
    "unconfirmed_media_report",
    "policy_beneficiary_only",
    "stock_price_moves_before_evidence",
    "margin_unknown",
)

ROUND193_STAGE4B_STATUSES: tuple[str, ...] = ("none", "watch", "elevated", "graduated", "benchmark")

ROUND193_PRICE_BACKFILL_FIELDS: tuple[str, ...] = (
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
    "peak_date",
    "peak_price",
    "MFE_20D",
    "MFE_60D",
    "MFE_90D",
    "MFE_120D",
    "MFE_180D",
    "MFE_252D",
    "MFE_1Y",
    "MFE_2Y",
    "MAE_20D",
    "MAE_60D",
    "MAE_90D",
    "MAE_120D",
    "MAE_180D",
    "MAE_252D",
    "MAE_1Y",
    "MAE_2Y",
    "relative_strength_vs_kospi",
    "relative_strength_vs_hbm_basket",
    "relative_strength_vs_semiconductor_equipment_basket",
    "relative_strength_vs_ai_server_pcb_basket",
    "customer_visibility",
    "customer_diversification_confirmed",
    "customer_name_confirmed",
    "order_amount",
    "contract_or_purchase_order_flag",
    "shipment_or_volume_ramp_flag",
    "design_win_flag",
    "tapeout_flag",
    "volume_production_flag",
    "revenue_recognition_flag",
    "gross_margin_visibility",
    "opm_visibility",
    "eps_revision",
    "fcf_revision",
    "hbm_capacity_bottleneck",
    "hbm_lta_flag",
    "prepayment_flag",
    "advanced_packaging_direct_link",
    "policy_foundry_flag",
    "media_report_without_confirmation_flag",
    "stock_price_rally_before_evidence_flag",
    "labor_disruption_flag",
    "production_disruption_flag",
    "accounting_trust_flag",
    "circular_financing_flag",
    "stage4b_status",
    "hard_4c_confirmed",
)


@dataclass(frozen=True)
class Round193ScoreAdjustment:
    axis: str
    points: int
    direction: str
    reason: str

    def as_row(self) -> dict[str, str]:
        return {
            "axis": self.axis,
            "points": str(self.points),
            "direction": self.direction,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class Round193CaseCandidate:
    case_id: str
    symbol: str
    company_name: str
    primary_archetype: E2RArchetype
    secondary_archetypes: tuple[E2RArchetype, ...]
    case_type: str
    stage1_date: date | None
    stage2_date: date | None
    stage3_date: date | None
    stage4b_date: date | None
    stage4c_date: date | None
    stage2_price_anchor: float | None
    stage3_price_anchor: float | None
    stage4b_price_anchor: float | None
    peak_price_anchor: float | None
    stage3_decision: str
    stage4b_status: str
    hard_4c_confirmed: bool
    evidence_fields: tuple[str, ...]
    red_flag_fields: tuple[str, ...]
    score_price_alignment: str
    rerating_result: str
    stage_failure_type: str
    price_validation_status: str
    notes: str

    @property
    def large_sector(self) -> Round10LargeSector:
        return Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND193_SCORE_ADJUSTMENTS: tuple[Round193ScoreAdjustment, ...] = (
    Round193ScoreAdjustment("customer_visibility", 3, "raise", "R2 Green은 회사 단위 고객 증거가 있어야 한다."),
    Round193ScoreAdjustment("order_to_revenue_conversion", 3, "raise", "수주/설계가 매출 인식으로 내려오는지를 본다."),
    Round193ScoreAdjustment("hbm_capacity_bottleneck", 3, "raise", "HBM 병목은 실제 CAPA/장비/고객 연결 때만 강하다."),
    Round193ScoreAdjustment("gross_margin_visibility", 3, "raise", "AI 수혜가 마진으로 연결되는지 확인한다."),
    Round193ScoreAdjustment("eps_revision", 3, "raise", "Stage 3는 EPS/FCF 체급 변화가 보여야 한다."),
    Round193ScoreAdjustment("customer_diversification_confirmed", 2, "raise", "미확인 루머가 아니라 고객 다변화가 확인되어야 한다."),
    Round193ScoreAdjustment("advanced_packaging_direct_link", 2, "raise", "HBM/AI 패키징 직접 연결은 R2 핵심 증거다."),
    Round193ScoreAdjustment("price_path_alignment", 2, "raise", "증거 뒤에 가격경로가 따라오는지 검증한다."),
    Round193ScoreAdjustment("ai_keyword", -4, "lower", "AI 이름만으로 Stage 3 근거를 만들지 않는다."),
    Round193ScoreAdjustment("server_theme", -3, "lower", "서버 테마는 Stage 1 라우팅까지만 제한한다."),
    Round193ScoreAdjustment("design_win_without_revenue", -3, "lower", "design win은 Stage 2일 수 있으나 매출 전 Green은 금지한다."),
    Round193ScoreAdjustment("policy_foundry_without_order", -3, "lower", "정책 파운드리는 회사 주문/매출 전 event premium이다."),
    Round193ScoreAdjustment("media_report_without_company_confirmation", -3, "lower", "미확인 고객 보도는 4B/가격선행 감시로 둔다."),
    Round193ScoreAdjustment("stock_price_rally_before_evidence", -4, "lower", "가격이 증거보다 먼저 가면 price-only 위험이다."),
    Round193ScoreAdjustment("customer_name_unknown", -2, "lower", "고객명 없는 AI 공급망 서사는 confidence를 낮춘다."),
    Round193ScoreAdjustment("margin_unknown", -2, "lower", "마진이 없으면 수주가 EPS/FCF로 바뀌었는지 모른다."),
)


ROUND193_CASE_CANDIDATES: tuple[Round193CaseCandidate, ...] = (
    Round193CaseCandidate(
        case_id="hanmi_semiconductor_tsv_tc_bonder_4b_watch",
        symbol="042700",
        company_name="한미반도체",
        primary_archetype=E2RArchetype.HBM_BONDER_EQUIPMENT_KOREA,
        secondary_archetypes=(E2RArchetype.SEMI_EQUIPMENT_AI_CAPEX, E2RArchetype.AI_CAPEX_CROWDING_OVERLAY),
        case_type="structural_success",
        stage1_date=None,
        stage2_date=date(2024, 3, 26),
        stage3_date=date(2024, 3, 26),
        stage4b_date=date(2024, 3, 28),
        stage4c_date=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=139100.0,
        peak_price_anchor=None,
        stage3_decision="possible_after_revenue_margin_eps_backfill",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=(
            "sk_hynix_tsv_tc_bonder_customer",
            "hbm_packaging_equipment",
            "recent_contracts_about_200b_krw",
            "hbm_capacity_bottleneck",
            "micron_unconfirmed_media_report_price_spike",
        ),
        red_flag_fields=("media_report_without_company_confirmation", "price_ahead_of_confirmed_customer", "order_pushout"),
        score_price_alignment="aligned",
        rerating_result="true_rerating",
        stage_failure_type="green_success",
        price_validation_status="needs_ohlc_backfill",
        notes="HBM bonder customer/order evidence can support Stage 3 candidate status, but the Micron unconfirmed report spike needs early 4B-watch.",
    ),
    Round193CaseCandidate(
        case_id="gaonchips_pfn_samsung_2nm_design_win_stage2",
        symbol="399720",
        company_name="가온칩스",
        primary_archetype=E2RArchetype.SYSTEM_SEMI_DESIGN_HOUSE_AI_ORDER,
        secondary_archetypes=(E2RArchetype.AI_CHIP_FABRIC_INFRA,),
        case_type="success_candidate",
        stage1_date=None,
        stage2_date=date(2024, 7, 9),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        stage3_decision="deferred_until_tapeout_volume_revenue_margin",
        stage4b_status="none",
        hard_4c_confirmed=False,
        evidence_fields=("preferred_networks_ai_chip_design", "samsung_2nm_gaa", "advanced_packaging_link", "design_win"),
        red_flag_fields=("design_win_without_revenue", "tapeout_before_volume", "no_margin_visibility"),
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="needs_ohlc_backfill",
        notes="AI chip design win is strong Stage 2 evidence, but Stage 3 waits for tape-out, volume production, revenue, and margin.",
    ),
    Round193CaseCandidate(
        case_id="samsung_electronics_hbm_catchup_failed_2025_watch",
        symbol="005930",
        company_name="삼성전자",
        primary_archetype=E2RArchetype.HBM_CATCHUP_EXECUTION,
        secondary_archetypes=(E2RArchetype.HBM_CATCHUP_EXECUTION_RISK, E2RArchetype.REDTEAM_ACCOUNTING_TRUST_OVERLAY),
        case_type="failed_rerating",
        stage1_date=None,
        stage2_date=date(2025, 4, 30),
        stage3_date=None,
        stage4b_date=date(2026, 5, 6),
        stage4c_date=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        stage3_decision="forbidden_until_qualification_volume_hbm_sales_eps",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("hbm_catchup_story", "hbm_sales_decline", "chip_profit_down_42pct", "nvidia_qualification_lag", "broad_ai_memory_rally_2026"),
        red_flag_fields=("labor_strike_watch", "production_disruption_watch", "qualification_lag", "hbm_sales_decline"),
        score_price_alignment="evidence_good_but_price_failed",
        rerating_result="no_rerating",
        stage_failure_type="false_green",
        price_validation_status="needs_ohlc_backfill",
        notes="2025 HBM catch-up was not Green because HBM sales and chip profit were weak. The 2026 AI rally is a separate 4B-watch context.",
    ),
    Round193CaseCandidate(
        case_id="db_hitek_policy_foundry_event_premium",
        symbol="000990",
        company_name="DB하이텍",
        primary_archetype=E2RArchetype.AI_CHIP_FABRIC_INFRA,
        secondary_archetypes=(),
        case_type="event_premium",
        stage1_date=date(2025, 12, 10),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        stage3_decision="forbidden_policy_without_order_revenue",
        stage4b_status="none",
        hard_4c_confirmed=False,
        evidence_fields=("government_4_5t_krw_foundry_review", "policy_foundry_candidate", "consultation_target"),
        red_flag_fields=("policy_foundry_without_order", "customer_order_absent", "revenue_conversion_absent"),
        score_price_alignment="price_moved_without_evidence",
        rerating_result="policy_event_rerating",
        stage_failure_type="should_have_been_red",
        price_validation_status="needs_ohlc_backfill",
        notes="Government foundry review is Stage 1/weak Stage 2 attention, not company Stage 3 before orders, customers, margin, and revenue.",
    ),
    Round193CaseCandidate(
        case_id="isu_petasis_ai_server_pcb_insufficient_evidence",
        symbol="007660",
        company_name="이수페타시스",
        primary_archetype=E2RArchetype.ADVANCED_PACKAGING_PCB,
        secondary_archetypes=(E2RArchetype.AI_SERVER_PCB_SUBSTRATE_SECOND_WAVE, E2RArchetype.PRICE_ONLY_RALLY),
        case_type="overheat",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        stage3_decision="forbidden_until_customer_contract_margin_eps",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("ai_server_pcb_narrative", "mlb_supply_chain_watch", "price_move_needs_backfill"),
        red_flag_fields=("customer_name_unknown", "contract_amount_missing", "margin_unknown", "eps_revision_missing", "inventory_risk"),
        score_price_alignment="price_moved_without_evidence",
        rerating_result="theme_overheat",
        stage_failure_type="should_have_been_red",
        price_validation_status="needs_ohlc_backfill",
        notes="AI server PCB narrative is watchable, but Green is blocked before customer/order/margin/EPS evidence.",
    ),
    Round193CaseCandidate(
        case_id="sk_hynix_hbm_2026_4b_benchmark",
        symbol="000660",
        company_name="SK하이닉스",
        primary_archetype=E2RArchetype.MEMORY_HBM_CAPACITY,
        secondary_archetypes=(E2RArchetype.MEMORY_HBM_LTA_PREPAYMENT, E2RArchetype.AI_CAPEX_CROWDING_OVERLAY),
        case_type="4b_watch",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=date(2026, 5, 14),
        stage4c_date=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        stage3_decision="existing_success_anchor_not_new_stage3",
        stage4b_status="benchmark",
        hard_4c_confirmed=False,
        evidence_fields=("hbm_market_leadership", "hbm_share_61pct_reference", "advanced_packaging_investment_19t_krw", "large_2025_2026_rerating"),
        red_flag_fields=("valuation_crowding", "customer_price_resistance", "capacity_normalization", "ai_capex_cut_watch"),
        score_price_alignment="aligned",
        rerating_result="true_rerating",
        stage_failure_type="green_success",
        price_validation_status="needs_ohlc_backfill",
        notes="SK Hynix remains the R2 success anchor, but Round193 uses it as a 4B benchmark rather than a new Stage 3 candidate.",
    ),
)


def round193_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND193_CASE_CANDIDATES:
        record = E2RCaseRecord(
            case_id=candidate.case_id,
            symbol=candidate.symbol,
            company_name=candidate.company_name,
            market="KR",
            sector_raw=candidate.primary_archetype.value,
            primary_archetype=candidate.primary_archetype,
            secondary_archetypes=candidate.secondary_archetypes,
            expected_group=candidate.expected_group,
            large_sector=candidate.large_sector.value,
            case_type=candidate.case_type,
            stage1_date=candidate.stage1_date,
            stage2_date=candidate.stage2_date,
            stage3_date=candidate.stage3_date,
            stage4b_date=candidate.stage4b_date,
            stage4c_date=candidate.stage4c_date,
            evidence_summary=(
                "Round193 R2 Loop-7 price-path validation case. "
                "This is calibration-only and must not be used for candidate generation."
            ),
            stage1_evidence=tuple(field for field in candidate.evidence_fields if "narrative" in field or "policy" in field),
            stage2_evidence=candidate.evidence_fields,
            stage3_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if field
                in {
                    "sk_hynix_tsv_tc_bonder_customer",
                    "hbm_packaging_equipment",
                    "recent_contracts_about_200b_krw",
                    "hbm_capacity_bottleneck",
                }
            ),
            stage4b_evidence=tuple(field for field in candidate.evidence_fields if "price" in field or "rally" in field or "rerating" in field),
            stage4c_evidence=() if not candidate.hard_4c_confirmed else candidate.red_flag_fields,
            must_have_fields=ROUND193_GREEN_REQUIRED_FIELDS,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason=(
                "; ".join(candidate.red_flag_fields)
                if candidate.case_type in {"event_premium", "overheat", "failed_rerating", "4b_watch", "4c_thesis_break"}
                else None
            ),
            score_price_alignment=candidate.score_price_alignment,
            rerating_result=candidate.rerating_result,
            stage_failure_type=candidate.stage_failure_type,
            price_pattern=candidate.stage3_decision,
            score_weight_hint={
                "customer_visibility_delta": 3.0,
                "order_to_revenue_conversion_delta": 3.0,
                "hbm_capacity_bottleneck_delta": 3.0,
                "gross_margin_visibility_delta": 3.0,
                "eps_revision_delta": 3.0,
                "ai_keyword_delta": -4.0,
                "design_win_without_revenue_delta": -3.0,
                "stock_price_rally_before_evidence_delta": -4.0,
            },
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "needs_ohlc_backfill_true",
                "do_not_invent_price_or_stage_dates",
                *ROUND193_GREEN_REQUIRED_FIELDS,
                *ROUND193_GREEN_FORBIDDEN_PATTERNS,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(
                stage2_price=candidate.stage2_price_anchor,
                stage3_price=candidate.stage3_price_anchor,
                stage4b_price=candidate.stage4b_price_anchor,
                peak_price=candidate.peak_price_anchor,
                price_validation_status=candidate.price_validation_status,
            ),
            data_quality=CaseDataQuality(
                official_data_available=True,
                report_data_available=True,
                price_data_available=False,
                stage_dates_confidence=0.8 if candidate.stage2_date or candidate.stage3_date or candidate.stage4b_date else 0.35,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round193_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND193_CASE_CANDIDATES:
        rows.append(
            {
                "case_id": candidate.case_id,
                "symbol": candidate.symbol,
                "company_name": candidate.company_name,
                "primary_archetype": candidate.primary_archetype.value,
                "secondary_archetypes": "|".join(item.value for item in candidate.secondary_archetypes),
                "case_type": candidate.case_type,
                "stage1_date": _date_text(candidate.stage1_date),
                "stage2_date": _date_text(candidate.stage2_date),
                "stage3_date": _date_text(candidate.stage3_date),
                "stage4b_date": _date_text(candidate.stage4b_date),
                "stage4c_date": _date_text(candidate.stage4c_date),
                "stage2_price_anchor": _float_text(candidate.stage2_price_anchor),
                "stage3_price_anchor": _float_text(candidate.stage3_price_anchor),
                "stage4b_price_anchor": _float_text(candidate.stage4b_price_anchor),
                "peak_price_anchor": _float_text(candidate.peak_price_anchor),
                "stage3_decision": candidate.stage3_decision,
                "stage4b_status": candidate.stage4b_status,
                "hard_4c_confirmed": str(candidate.hard_4c_confirmed).lower(),
                "score_price_alignment": candidate.score_price_alignment,
                "rerating_result": candidate.rerating_result,
                "stage_failure_type": candidate.stage_failure_type,
                "price_validation_status": candidate.price_validation_status,
                "evidence_fields": "|".join(candidate.evidence_fields),
                "red_flag_fields": "|".join(candidate.red_flag_fields),
                "notes": candidate.notes,
            }
        )
    return tuple(rows)


def round193_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND193_SCORE_ADJUSTMENTS)


def round193_price_backfill_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round193_backfill": "true"} for field in ROUND193_PRICE_BACKFILL_FIELDS)


def round193_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {"round193_label": label, "canonical_archetype": canonical}
        for label, canonical in ROUND193_REQUIRED_TARGET_ALIASES.items()
    )


def round193_summary() -> dict[str, int | bool]:
    cases = round193_case_records()
    return {
        "case_candidate_count": len(cases),
        "required_target_count": len(ROUND193_REQUIRED_TARGET_ALIASES),
        "score_adjustment_count": len(ROUND193_SCORE_ADJUSTMENTS),
        "price_backfill_field_count": len(ROUND193_PRICE_BACKFILL_FIELDS),
        "structural_success_count": sum(1 for case in cases if case.case_type == "structural_success"),
        "success_candidate_count": sum(1 for case in cases if case.case_type == "success_candidate"),
        "event_premium_count": sum(1 for case in cases if case.case_type == "event_premium"),
        "overheat_count": sum(1 for case in cases if case.case_type == "overheat"),
        "failed_rerating_count": sum(1 for case in cases if case.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for case in ROUND193_CASE_CANDIDATES if case.stage4b_status in {"watch", "elevated", "benchmark"}),
        "hard_4c_confirmed_count": sum(1 for case in ROUND193_CASE_CANDIDATES if case.hard_4c_confirmed),
        "needs_ohlc_backfill_count": sum(1 for case in ROUND193_CASE_CANDIDATES if case.price_validation_status == "needs_ohlc_backfill"),
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
        "needs_ohlc_backfill": True,
    }


def write_round193_r2_loop7_reports(
    *,
    output_directory: str | Path = ROUND193_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND193_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND193_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    cases = write_case_library(round193_case_records(), cases_path)
    audit = Path(audit_path)
    audit.parent.mkdir(parents=True, exist_ok=True)
    paths = {
        "cases": cases,
        "audit_json": audit,
        "summary": output / "round193_r2_loop7_price_validation_summary.md",
        "case_matrix": output / "round193_r2_loop7_case_matrix.csv",
        "target_aliases": output / "round193_r2_loop7_target_aliases.csv",
        "score_adjustments": output / "round193_r2_loop7_score_adjustments.csv",
        "price_backfill_fields": output / "round193_r2_loop7_price_backfill_fields.csv",
        "green_gate_review": output / "round193_r2_loop7_green_gate_review.md",
        "price_backfill_plan": output / "round193_r2_loop7_price_backfill_plan.md",
        "stage4b_4c_review": output / "round193_r2_loop7_stage4b_4c_review.md",
    }
    audit.write_text(json.dumps(round193_audit_payload(), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_rows(round193_case_rows(), paths["case_matrix"])
    _write_rows(round193_target_alias_rows(), paths["target_aliases"])
    _write_rows(round193_score_adjustment_rows(), paths["score_adjustments"])
    _write_rows(round193_price_backfill_field_rows(), paths["price_backfill_fields"])
    paths["summary"].write_text(render_round193_summary_markdown(), encoding="utf-8")
    paths["green_gate_review"].write_text(render_round193_green_gate_review_markdown(), encoding="utf-8")
    paths["price_backfill_plan"].write_text(render_round193_price_backfill_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round193_stage4b_4c_review_markdown(), encoding="utf-8")
    return paths


def round193_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND193_SOURCE_ROUND_PATH,
        "large_sector": Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS.value,
        "summary": round193_summary(),
        "target_aliases": list(round193_target_alias_rows()),
        "green_required_fields": list(ROUND193_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND193_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_statuses": list(ROUND193_STAGE4B_STATUSES),
        "score_adjustments": list(round193_score_adjustment_rows()),
        "case_ids": [case.case_id for case in ROUND193_CASE_CANDIDATES],
        "what_not_to_change": [
            "do_not_apply_to_production_scoring_yet",
            "do_not_use_round193_cases_as_candidate_generation_input",
            "do_not_lower_stage3_green_thresholds",
            "do_not_treat_ai_name_or_hbm_keyword_as_green_evidence",
            "do_not_invent_prices_stage_dates_customers_or_margins",
        ],
    }


def render_round193_summary_markdown() -> str:
    summary = round193_summary()
    lines = [
        "# Round-193 R2 Loop-7 Price-Path Validation Summary",
        "",
        f"- source_round: `{ROUND193_SOURCE_ROUND_PATH}`",
        "- large_sector: `AI_SEMICONDUCTOR_ELECTRONICS`",
        "- scope: Korean HBM equipment, AI chip design-house, HBM catch-up, policy foundry, AI PCB, and 4B benchmark validation",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- required_target_count: {summary['required_target_count']}",
        f"- score_adjustment_count: {summary['score_adjustment_count']}",
        f"- price_backfill_field_count: {summary['price_backfill_field_count']}",
        f"- structural_success_count: {summary['structural_success_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- overheat_count: {summary['overheat_count']}",
        f"- failed_rerating_count: {summary['failed_rerating_count']}",
        f"- stage4b_case_count: {summary['stage4b_case_count']}",
        f"- hard_4c_confirmed_count: {summary['hard_4c_confirmed_count']}",
        f"- needs_ohlc_backfill_count: {summary['needs_ohlc_backfill_count']}",
        "- production_scoring_changed: false",
        "- candidate_generation_input: false",
        "- shadow_weight_only: true",
        "- needs_ohlc_backfill: true",
        "",
        "## Interpretation",
        "",
        "- R2에서 진짜 Stage 3는 AI 이름이 아니라 고객, 수주, 출하, 매출 인식, 마진, EPS/FCF가 연결되는 순간이다.",
        "- 한미반도체는 HBM 장비 Stage 3 후보지만, 미확인 Micron 보도 급등 구간은 4B-watch로 분리해야 한다.",
        "- 가온칩스는 design win이 강해도 양산, 매출, 마진 전에는 Stage 2/Watch다.",
        "- 삼성전자는 2025년 HBM catch-up 구간에서 Green이 아니라 watch/failed-rerating 진단이 맞다.",
        "- DB하이텍 정책 파운드리와 이수페타시스 AI PCB narrative는 회사 매출 증거 전 Green 금지다.",
        "- SK하이닉스는 신규 Stage 3가 아니라 4B benchmark로 기록한다.",
        "",
        "쉬운 예: `as_of_date=2024-07-09`에 가온칩스가 AI칩 설계에 참여했다는 보도는 Stage 2 근거가 될 수 있다. 하지만 그날 tape-out, 양산, 매출 인식, 마진이 없으면 Stage 3-Green으로 올리면 안 된다.",
    ]
    return "\n".join(lines) + "\n"


def render_round193_green_gate_review_markdown() -> str:
    lines = [
        "# Round-193 R2 Loop-7 Green Gate Review",
        "",
        "## Green Required Evidence",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND193_GREEN_REQUIRED_FIELDS)
    lines.extend(
        [
            "",
            "## Green Forbidden Patterns",
            "",
        ]
    )
    lines.extend(f"- `{field}`" for field in ROUND193_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(
        [
            "",
            "## Shadow Score Adjustments",
            "",
            "| axis | direction | points | reason |",
            "| --- | --- | ---: | --- |",
        ]
    )
    for row in ROUND193_SCORE_ADJUSTMENTS:
        lines.append(f"| `{row.axis}` | {row.direction} | {row.points} | {row.reason} |")
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not apply these weights to production scoring yet.",
            "- Do not use Round193 cases as candidate-generation input.",
            "- Do not lower Stage 3-Green thresholds to force promotion.",
            "- Do not invent customer names, orders, shipments, margins, stage prices, or MFE/MAE.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round193_price_backfill_plan_markdown() -> str:
    lines = [
        "# Round-193 R2 Loop-7 Price Backfill Plan",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND193_PRICE_BACKFILL_FIELDS)
    lines.extend(
        [
            "",
            "## Priority Cases",
            "",
            "| case | stage marker | current status | price anchor |",
            "| --- | --- | --- | --- |",
        ]
    )
    for case in ROUND193_CASE_CANDIDATES:
        stage_marker = case.stage3_date or case.stage2_date or case.stage4b_date or case.stage1_date
        anchor = case.stage3_price_anchor or case.stage2_price_anchor or case.stage4b_price_anchor or case.peak_price_anchor
        lines.append(
            f"| `{case.case_id}` | {_date_text(stage_marker) or 'undated'} | "
            f"{case.price_validation_status} | {_float_text(anchor) or 'none'} |"
        )
    lines.extend(
        [
            "",
            "## Backfill Rule",
            "",
            "- Use official OHLC data for exact MFE/MAE.",
            "- Keep unknown values null or `needs_ohlc_backfill`.",
            "- Article intraday anchors are hints, not substitutes for official OHLC.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round193_stage4b_4c_review_markdown() -> str:
    lines = [
        "# Round-193 R2 Loop-7 Stage 4B / 4C Review",
        "",
        "## 4B Status Definitions",
        "",
        "- `watch`: AI/HBM logic is plausible but price, valuation, or consensus is running ahead.",
        "- `elevated`: customer CAPEX, margin, financing, or concentration risk becomes material.",
        "- `graduated`: new orders or earnings beats no longer create meaningful rerating.",
        "- `benchmark`: already-successful anchor used to calibrate 4B timing, not a new Stage 3 case.",
        "",
        "## Case Review",
        "",
        "| case | 4B status | hard 4C confirmed | interpretation |",
        "| --- | --- | --- | --- |",
    ]
    for case in ROUND193_CASE_CANDIDATES:
        lines.append(
            f"| `{case.case_id}` | `{case.stage4b_status}` | {str(case.hard_4c_confirmed).lower()} | {case.notes} |"
        )
    lines.extend(
        [
            "",
            "## Hard 4C Gate",
            "",
            "- HBM customer qualification failure",
            "- order push-out",
            "- customer CAPEX cut",
            "- HBM/memory price decline",
            "- capacity oversupply",
            "- customer concentration risk becoming real",
            "- prolonged labor or production disruption",
            "- accounting/disclosure trust break",
            "- IP leakage or technology leakage",
            "- circular AI financing confirmed",
            "- dilution through capital raise or CB that breaks the thesis",
        ]
    )
    return "\n".join(lines) + "\n"


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


def _date_text(value: date | None) -> str:
    return value.isoformat() if value else ""


def _float_text(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:g}"


__all__ = [
    "ROUND193_CASE_CANDIDATES",
    "ROUND193_DEFAULT_AUDIT_PATH",
    "ROUND193_DEFAULT_CASES_PATH",
    "ROUND193_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND193_GREEN_FORBIDDEN_PATTERNS",
    "ROUND193_GREEN_REQUIRED_FIELDS",
    "ROUND193_PRICE_BACKFILL_FIELDS",
    "ROUND193_REQUIRED_TARGET_ALIASES",
    "ROUND193_SCORE_ADJUSTMENTS",
    "ROUND193_SOURCE_ROUND_PATH",
    "ROUND193_STAGE4B_STATUSES",
    "Round193CaseCandidate",
    "Round193ScoreAdjustment",
    "render_round193_green_gate_review_markdown",
    "render_round193_price_backfill_plan_markdown",
    "render_round193_stage4b_4c_review_markdown",
    "render_round193_summary_markdown",
    "round193_audit_payload",
    "round193_case_records",
    "round193_case_rows",
    "round193_price_backfill_field_rows",
    "round193_score_adjustment_rows",
    "round193_summary",
    "round193_target_alias_rows",
    "write_round193_r2_loop7_reports",
]
