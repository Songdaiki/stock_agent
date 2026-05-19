"""Round-192 R1 Loop-7 Korean price-path validation pack.

Round 192 is a calibration-only follow-up to the broader R1 Loop-7
industrial/orders/infrastructure work. It adds Korean defense, shipbuilding,
MRO, and price-only rally cases so the future scoring work can validate whether
order evidence actually converted into stage, price path, 4B, and 4C outcomes.

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


ROUND192_SOURCE_ROUND_PATH = "docs/round/round_192.md"
ROUND192_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round192_r1_loop7_industrial_infra_price_validation"
ROUND192_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r1_loop7_round192.jsonl"
ROUND192_DEFAULT_AUDIT_PATH = (
    "data/sector_taxonomy/round192_r1_loop7_industrial_infra_price_validation_audit.json"
)

ROUND192_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "DEFENSE_GOVERNMENT_BACKLOG": E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG.value,
    "DEFENSE_LOCAL_PRODUCTION_PLATFORM": E2RArchetype.DEFENSE_LOCAL_PRODUCTION_PLATFORM.value,
    "DEFENSE_INTERCEPTOR_COMBAT_VALIDATION": E2RArchetype.DEFENSE_INTERCEPTOR_COMBAT_VALIDATION.value,
    "CONTRACT_BACKLOG_INDUSTRIAL": E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL.value,
    "SHIPBUILDING_OFFSHORE_BACKLOG": E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG.value,
    "SHIP_MRO_RECURRING_PLATFORM": E2RArchetype.SHIP_MRO_RECURRING_PLATFORM.value,
    "AI_DATA_CENTER_POWER_EQUIPMENT": E2RArchetype.AI_DATA_CENTER_POWER_EQUIPMENT.value,
    "POWER_EQUIPMENT_BACKLOG_TO_FCF": E2RArchetype.POWER_EQUIPMENT_BACKLOG_TO_FCF.value,
    "PRICE_ONLY_RALLY": E2RArchetype.PRICE_ONLY_RALLY.value,
    "CROWDING_4B_WATCH": E2RArchetype.CROWDED_RERATING_4B_WATCH.value,
    "THESIS_BREAK_4C": E2RArchetype.THESIS_BREAK_4C.value,
}

ROUND192_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "contract_amount_to_prior_sales",
    "contract_duration_months",
    "delivery_schedule",
    "customer_or_government_budget_financing",
    "backlog_growth",
    "opm_or_eps_revision",
    "price_path_after_evidence",
)

ROUND192_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "order_headline_only",
    "margin_unknown",
    "delivery_schedule_unknown",
    "financing_condition_unknown",
    "ipo_or_supply_demand_price_spike",
    "price_moves_before_evidence",
)

ROUND192_STAGE4B_STATUSES: tuple[str, ...] = ("none", "watch", "elevated", "graduated", "sanction_watch")

ROUND192_PRICE_BACKFILL_FIELDS: tuple[str, ...] = (
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
    "relative_strength_vs_defense_basket",
    "relative_strength_vs_shipbuilding_basket",
    "relative_strength_vs_power_equipment_basket",
    "contract_amount_to_prior_sales",
    "contract_duration_months",
    "backlog_to_sales",
    "delivery_schedule",
    "government_financing_flag",
    "local_production_flag",
    "op_eps_revision",
    "margin_visibility",
    "capital_raise_flag",
    "sanction_watch_flag",
    "ipo_first_day_return",
    "disclosure_confidence",
    "stage4b_status",
    "hard_4c_confirmed",
)


@dataclass(frozen=True)
class Round192ScoreAdjustment:
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
class Round192CaseCandidate:
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
        return Round10LargeSector.INDUSTRIAL_ORDERS_INFRA

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND192_SCORE_ADJUSTMENTS: tuple[Round192ScoreAdjustment, ...] = (
    Round192ScoreAdjustment("contract_quality", 2, "raise", "계약 headline보다 계약 질을 더 본다."),
    Round192ScoreAdjustment("delivery_schedule", 2, "raise", "방산/조선은 납품 일정이 매출 인식의 핵심이다."),
    Round192ScoreAdjustment("order_to_revenue_conversion", 2, "raise", "수주가 매출과 이익으로 넘어가는지를 확인한다."),
    Round192ScoreAdjustment("op_eps_revision", 3, "raise", "Stage 3는 OP/EPS 체급 변화가 보여야 한다."),
    Round192ScoreAdjustment("margin_visibility", 3, "raise", "저마진 수주는 Stage 3-Green을 막아야 한다."),
    Round192ScoreAdjustment("government_financing_or_budget", 2, "raise", "정부 예산/금융 조건이 계약 지속성을 좌우한다."),
    Round192ScoreAdjustment("price_path_alignment", 2, "raise", "증거 뒤에 가격경로가 따라오는지 검증한다."),
    Round192ScoreAdjustment("order_headline", -3, "lower", "수주 뉴스만으로 Green을 주지 않는다."),
    Round192ScoreAdjustment("theme_keyword", -3, "lower", "테마 키워드는 Stage 1 라우팅까지만 제한한다."),
    Round192ScoreAdjustment("broker_target_only", -2, "lower", "목표가 상향만으로 구조적 evidence를 만들지 않는다."),
    Round192ScoreAdjustment("ipo_first_day_price_move", -4, "lower", "상장 첫날 급등은 event premium/수급성으로 본다."),
    Round192ScoreAdjustment("contract_amount_without_margin", -2, "lower", "계약금액만 있고 마진이 없으면 Stage 2에 머문다."),
    Round192ScoreAdjustment("policy_or_mou_without_budget", -3, "lower", "정책/MOU는 예산과 계약 없이는 Green 근거가 아니다."),
)


ROUND192_CASE_CANDIDATES: tuple[Round192CaseCandidate, ...] = (
    Round192CaseCandidate(
        case_id="hyundai_rotem_k2_export_price_path",
        symbol="064350",
        company_name="현대로템",
        primary_archetype=E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,
        secondary_archetypes=(E2RArchetype.DEFENSE_LOCAL_PRODUCTION_PLATFORM,),
        case_type="structural_success",
        stage1_date=None,
        stage2_date=date(2024, 4, 9),
        stage3_date=None,
        stage4b_date=date(2025, 8, 1),
        stage4c_date=None,
        stage2_price_anchor=41300.0,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        stage3_decision="possible_after_delivery_revenue_op_confirmation",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=(
            "poland_k2_delivery_revenue",
            "op_yoy_85pct_expected",
            "government_customer",
            "local_production_structure",
            "large_follow_on_contract",
            "price_path_large_mfe_possible",
        ),
        red_flag_fields=("delivery_delay", "financing_failure", "local_production_margin_risk"),
        score_price_alignment="aligned",
        rerating_result="true_rerating",
        stage_failure_type="green_success",
        price_validation_status="needs_ohlc_backfill",
        notes="Stage 2 anchor is the 2024-04-09 41,300 KRW article price; exact Stage 3 and MFE/MAE require OHLC backfill.",
    ),
    Round192CaseCandidate(
        case_id="lig_nex1_msami_iraq_combat_validation",
        symbol="079550",
        company_name="LIG넥스원",
        primary_archetype=E2RArchetype.DEFENSE_INTERCEPTOR_COMBAT_VALIDATION,
        secondary_archetypes=(E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,),
        case_type="success_candidate",
        stage1_date=None,
        stage2_date=date(2024, 9, 20),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        stage3_decision="conditional_after_backlog_margin_eps_delivery_visibility",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=(
            "iraq_msami_contract_3_71t_krw",
            "saudi_msami_reference",
            "middle_east_air_defense_demand",
            "combat_validation_watch",
            "event_day_price_up_3_6pct",
        ),
        red_flag_fields=("delivery_delay", "export_permit_risk", "production_capacity_limit", "revenue_recognition_lag"),
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="yellow_success",
        price_validation_status="needs_ohlc_backfill",
        notes="Contract and demand are strong, but Green waits for sales recognition, margin, EPS revision, and delivery visibility.",
    ),
    Round192CaseCandidate(
        case_id="hanwha_aerospace_poland_chunmoo_4b_timing",
        symbol="012450",
        company_name="한화에어로스페이스",
        primary_archetype=E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,
        secondary_archetypes=(
            E2RArchetype.CROWDED_RERATING_4B_WATCH,
            E2RArchetype.CAPITAL_ALLOCATION_DILUTION_OVERLAY,
        ),
        case_type="structural_success",
        stage1_date=None,
        stage2_date=date(2024, 3, 22),
        stage3_date=date(2024, 4, 25),
        stage4b_date=date(2025, 3, 21),
        stage4c_date=None,
        stage2_price_anchor=217000.0,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=1435000.0,
        stage3_decision="possible_with_financing_and_eps_confirmation",
        stage4b_status="elevated",
        hard_4c_confirmed=False,
        evidence_fields=(
            "poland_chunmoo_contract_1_64b_usd",
            "defense_export_growth",
            "opm_improvement_expected",
            "multi_year_backlog",
            "norway_chunmoo_follow_on",
        ),
        red_flag_fields=("capital_raise_shock", "dilution", "financing_condition", "capex_burden"),
        score_price_alignment="aligned",
        rerating_result="true_rerating",
        stage_failure_type="green_success",
        price_validation_status="needs_ohlc_backfill",
        notes="The 2025 capital raise shock is 4B-watch/elevated, not hard 4C while backlog and guidance remain alive.",
    ),
    Round192CaseCandidate(
        case_id="samsung_heavy_shipbuilding_contract_stage2_not_green",
        symbol="010140",
        company_name="삼성중공업",
        primary_archetype=E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG,
        secondary_archetypes=(),
        case_type="success_candidate",
        stage1_date=None,
        stage2_date=date(2024, 7, 1),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        stage3_decision="deferred_until_margin_eps_fcf_delivery_quality",
        stage4b_status="none",
        hard_4c_confirmed=False,
        evidence_fields=("shipbuilding_contract_1_438t_krw", "ship_order_cycle", "stage2_contract_amount"),
        red_flag_fields=("margin_unknown", "low_margin_backlog", "steel_plate_cost", "labor_cost", "delivery_delay"),
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="needs_ohlc_backfill",
        notes="Large shipbuilding contract is Stage 2 evidence only; Green waits for margin, EPS revision, FCF, and delivery-slot quality.",
    ),
    Round192CaseCandidate(
        case_id="hd_hyundai_marine_solution_ipo_price_only_rally",
        symbol="443060",
        company_name="HD현대마린솔루션",
        primary_archetype=E2RArchetype.SHIP_MRO_RECURRING_PLATFORM,
        secondary_archetypes=(E2RArchetype.PRICE_ONLY_RALLY,),
        case_type="event_premium",
        stage1_date=date(2024, 5, 8),
        stage2_date=date(2024, 5, 8),
        stage3_date=None,
        stage4b_date=date(2024, 5, 8),
        stage4c_date=None,
        stage2_price_anchor=163900.0,
        stage3_price_anchor=None,
        stage4b_price_anchor=163900.0,
        peak_price_anchor=None,
        stage3_decision="forbidden_ipo_first_day_price_only",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("ipo_first_day_return_97pct", "mro_platform_potential", "scarcity_premium"),
        red_flag_fields=("ipo_first_day_price_move", "price_only_rally", "recurring_revenue_not_verified"),
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="should_have_been_red",
        price_validation_status="needs_ohlc_backfill",
        notes="IPO first-day +97% is event premium/price-only rally, not Stage 3 evidence.",
    ),
    Round192CaseCandidate(
        case_id="kai_fa50_philippines_stage2_watch",
        symbol="047810",
        company_name="한국항공우주",
        primary_archetype=E2RArchetype.DEFENSE_AIRCRAFT_EXPORT_BACKLOG,
        secondary_archetypes=(E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,),
        case_type="success_candidate",
        stage1_date=None,
        stage2_date=date(2025, 6, 4),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        stage3_decision="deferred_until_backlog_margin_eps_pipeline",
        stage4b_status="none",
        hard_4c_confirmed=False,
        evidence_fields=("philippines_fa50_contract_975_3b_krw", "delivery_to_2030", "aircraft_export_reference"),
        red_flag_fields=("margin_unknown", "pipeline_uncertain", "delivery_delay", "single_contract_not_bodyweight_change"),
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="needs_ohlc_backfill",
        notes="The FA-50 contract supports Stage 2 watch; Stage 3 requires backlog, margin, EPS revision, and export pipeline confirmation.",
    ),
    Round192CaseCandidate(
        case_id="hanwha_ocean_sanction_watch_not_hard_4c",
        symbol="042660",
        company_name="한화오션",
        primary_archetype=E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG,
        secondary_archetypes=(E2RArchetype.GEOPOLITICAL_SHIPBUILDING_SANCTION_OVERLAY,),
        case_type="success_candidate",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        peak_price_anchor=None,
        stage3_decision="deferred_until_backlog_margin_contract_quality",
        stage4b_status="sanction_watch",
        hard_4c_confirmed=False,
        evidence_fields=("us_shipbuilding_mro_option", "china_sanction_watch", "sanction_suspended"),
        red_flag_fields=("geopolitical_sanction", "export_control_risk", "contract_delay", "margin_unknown"),
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="unknown",
        price_validation_status="needs_ohlc_backfill",
        notes="China sanction event is a policy/geopolitical watch item. Suspension means hard 4C is not confirmed.",
    ),
)


def round192_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND192_CASE_CANDIDATES:
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
                "Round192 R1 Loop-7 price-path validation case. "
                "This is calibration-only and must not be used for candidate generation."
            ),
            stage1_evidence=tuple(field for field in candidate.evidence_fields if "theme" in field or "ipo" in field),
            stage2_evidence=candidate.evidence_fields,
            stage3_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if field
                in {
                    "op_yoy_85pct_expected",
                    "poland_chunmoo_contract_1_64b_usd",
                    "opm_improvement_expected",
                    "multi_year_backlog",
                    "large_follow_on_contract",
                }
            ),
            stage4b_evidence=tuple(field for field in candidate.evidence_fields if "price" in field or "capital" in field),
            stage4c_evidence=() if not candidate.hard_4c_confirmed else candidate.red_flag_fields,
            must_have_fields=ROUND192_GREEN_REQUIRED_FIELDS,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason=(
                "; ".join(candidate.red_flag_fields)
                if candidate.case_type in {"event_premium", "overheat", "4b_watch", "4c_thesis_break", "failed_rerating"}
                else None
            ),
            score_price_alignment=candidate.score_price_alignment,
            rerating_result=candidate.rerating_result,
            stage_failure_type=candidate.stage_failure_type,
            price_pattern=candidate.stage3_decision,
            score_weight_hint={
                "contract_quality_delta": 2.0,
                "delivery_schedule_delta": 2.0,
                "op_eps_revision_delta": 3.0,
                "margin_visibility_delta": 3.0,
                "price_path_alignment_delta": 2.0,
                "order_headline_delta": -3.0,
                "ipo_first_day_price_move_delta": -4.0,
            },
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "needs_ohlc_backfill_true",
                "do_not_invent_price_or_stage_dates",
                *ROUND192_GREEN_REQUIRED_FIELDS,
                *ROUND192_GREEN_FORBIDDEN_PATTERNS,
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
                stage_dates_confidence=0.8 if candidate.stage2_date or candidate.stage3_date else 0.35,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round192_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND192_CASE_CANDIDATES:
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


def round192_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND192_SCORE_ADJUSTMENTS)


def round192_price_backfill_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round192_backfill": "true"} for field in ROUND192_PRICE_BACKFILL_FIELDS)


def round192_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {"round192_label": label, "canonical_archetype": canonical}
        for label, canonical in ROUND192_REQUIRED_TARGET_ALIASES.items()
    )


def round192_summary() -> dict[str, int | bool]:
    cases = round192_case_records()
    return {
        "case_candidate_count": len(cases),
        "required_target_count": len(ROUND192_REQUIRED_TARGET_ALIASES),
        "score_adjustment_count": len(ROUND192_SCORE_ADJUSTMENTS),
        "price_backfill_field_count": len(ROUND192_PRICE_BACKFILL_FIELDS),
        "structural_success_count": sum(1 for case in cases if case.case_type == "structural_success"),
        "success_candidate_count": sum(1 for case in cases if case.case_type == "success_candidate"),
        "event_premium_count": sum(1 for case in cases if case.case_type == "event_premium"),
        "stage4b_watch_or_elevated_count": sum(1 for case in ROUND192_CASE_CANDIDATES if case.stage4b_status in {"watch", "elevated"}),
        "hard_4c_confirmed_count": sum(1 for case in ROUND192_CASE_CANDIDATES if case.hard_4c_confirmed),
        "needs_ohlc_backfill_count": sum(1 for case in ROUND192_CASE_CANDIDATES if case.price_validation_status == "needs_ohlc_backfill"),
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
        "needs_ohlc_backfill": True,
    }


def write_round192_r1_loop7_reports(
    *,
    output_directory: str | Path = ROUND192_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND192_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND192_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    cases = write_case_library(round192_case_records(), cases_path)
    audit = Path(audit_path)
    audit.parent.mkdir(parents=True, exist_ok=True)
    paths = {
        "cases": cases,
        "audit_json": audit,
        "summary": output / "round192_r1_loop7_price_validation_summary.md",
        "case_matrix": output / "round192_r1_loop7_case_matrix.csv",
        "target_aliases": output / "round192_r1_loop7_target_aliases.csv",
        "score_adjustments": output / "round192_r1_loop7_score_adjustments.csv",
        "price_backfill_fields": output / "round192_r1_loop7_price_backfill_fields.csv",
        "green_gate_review": output / "round192_r1_loop7_green_gate_review.md",
        "price_backfill_plan": output / "round192_r1_loop7_price_backfill_plan.md",
        "stage4b_4c_review": output / "round192_r1_loop7_stage4b_4c_review.md",
    }
    audit.write_text(json.dumps(round192_audit_payload(), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_rows(round192_case_rows(), paths["case_matrix"])
    _write_rows(round192_target_alias_rows(), paths["target_aliases"])
    _write_rows(round192_score_adjustment_rows(), paths["score_adjustments"])
    _write_rows(round192_price_backfill_field_rows(), paths["price_backfill_fields"])
    paths["summary"].write_text(render_round192_summary_markdown(), encoding="utf-8")
    paths["green_gate_review"].write_text(render_round192_green_gate_review_markdown(), encoding="utf-8")
    paths["price_backfill_plan"].write_text(render_round192_price_backfill_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round192_stage4b_4c_review_markdown(), encoding="utf-8")
    return paths


def round192_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND192_SOURCE_ROUND_PATH,
        "large_sector": Round10LargeSector.INDUSTRIAL_ORDERS_INFRA.value,
        "summary": round192_summary(),
        "target_aliases": list(round192_target_alias_rows()),
        "green_required_fields": list(ROUND192_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND192_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_statuses": list(ROUND192_STAGE4B_STATUSES),
        "score_adjustments": list(round192_score_adjustment_rows()),
        "case_ids": [case.case_id for case in ROUND192_CASE_CANDIDATES],
        "what_not_to_change": [
            "do_not_apply_to_production_scoring_yet",
            "do_not_use_round192_cases_as_candidate_generation_input",
            "do_not_lower_stage3_green_thresholds",
            "do_not_treat_4b_watch_as_hard_4c",
            "do_not_invent_prices_stage_dates_or_margins",
        ],
    }


def render_round192_summary_markdown() -> str:
    summary = round192_summary()
    lines = [
        "# Round-192 R1 Loop-7 Price-Path Validation Summary",
        "",
        f"- source_round: `{ROUND192_SOURCE_ROUND_PATH}`",
        "- large_sector: `INDUSTRIAL_ORDERS_INFRA`",
        "- scope: Korean defense, shipbuilding, MRO, and price-only rally validation",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- required_target_count: {summary['required_target_count']}",
        f"- score_adjustment_count: {summary['score_adjustment_count']}",
        f"- price_backfill_field_count: {summary['price_backfill_field_count']}",
        f"- structural_success_count: {summary['structural_success_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- stage4b_watch_or_elevated_count: {summary['stage4b_watch_or_elevated_count']}",
        f"- hard_4c_confirmed_count: {summary['hard_4c_confirmed_count']}",
        f"- needs_ohlc_backfill_count: {summary['needs_ohlc_backfill_count']}",
        "- production_scoring_changed: false",
        "- candidate_generation_input: false",
        "- shadow_weight_only: true",
        "- needs_ohlc_backfill: true",
        "",
        "## Interpretation",
        "",
        "- R1에서 강한 증거는 수주 뉴스가 아니라 수주가 납품, 마진, OP/EPS, FCF로 넘어가는 순간이다.",
        "- 현대로템과 한화에어로스페이스는 구조적 성공 후보지만, 정확한 MFE/MAE는 공식 OHLC backfill이 필요하다.",
        "- LIG넥스원, 삼성중공업, KAI는 계약이 강해도 매출 인식, 마진, EPS revision 전에는 Stage 2/Watch에 머문다.",
        "- HD현대마린솔루션 IPO 첫날 급등은 Stage 3가 아니라 event premium / price-only rally 반례다.",
        "- 한화오션 제재 이벤트는 sanction watch다. 제재 중단이 있었으므로 hard 4C로 확정하지 않는다.",
        "",
        "쉬운 예: `as_of_date=2024-07-01`에 삼성중공업 1.438조 원 계약을 봤다면 Stage 2 근거는 될 수 있다. 하지만 그날 마진, 납기, EPS 상향이 없으면 Stage 3-Green으로 올리면 안 된다.",
    ]
    return "\n".join(lines) + "\n"


def render_round192_green_gate_review_markdown() -> str:
    lines = [
        "# Round-192 R1 Loop-7 Green Gate Review",
        "",
        "## Green Required Evidence",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND192_GREEN_REQUIRED_FIELDS)
    lines.extend(
        [
            "",
            "## Green Forbidden Patterns",
            "",
        ]
    )
    lines.extend(f"- `{field}`" for field in ROUND192_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(
        [
            "",
            "## Shadow Score Adjustments",
            "",
            "| axis | direction | points | reason |",
            "| --- | --- | ---: | --- |",
        ]
    )
    for row in ROUND192_SCORE_ADJUSTMENTS:
        lines.append(f"| `{row.axis}` | {row.direction} | {row.points} | {row.reason} |")
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not apply these weights to production scoring yet.",
            "- Do not use Round192 cases as candidate-generation input.",
            "- Do not lower Stage 3-Green thresholds to force promotion.",
            "- Do not invent contract margin, delivery schedules, financing, stage prices, or MFE/MAE.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round192_price_backfill_plan_markdown() -> str:
    lines = [
        "# Round-192 R1 Loop-7 Price Backfill Plan",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND192_PRICE_BACKFILL_FIELDS)
    lines.extend(
        [
            "",
            "## Priority Cases",
            "",
            "| case | stage marker | current status | price anchor |",
            "| --- | --- | --- | --- |",
        ]
    )
    for case in ROUND192_CASE_CANDIDATES:
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
            "- A price anchor from an article is a hint, not a substitute for official OHLC.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round192_stage4b_4c_review_markdown() -> str:
    lines = [
        "# Round-192 R1 Loop-7 Stage 4B / 4C Review",
        "",
        "## 4B Status Definitions",
        "",
        "- `watch`: price, valuation, or consensus is late-cycle, but thesis is intact.",
        "- `elevated`: dilution, capex, or capital-allocation risk appeared, but backlog/EPS thesis is not broken.",
        "- `graduated`: rerating is broadly accepted and new contracts no longer surprise.",
        "- `sanction_watch`: geopolitical or policy shock exists, but hard thesis break is not confirmed.",
        "",
        "## Case Review",
        "",
        "| case | 4B status | hard 4C confirmed | interpretation |",
        "| --- | --- | --- | --- |",
    ]
    for case in ROUND192_CASE_CANDIDATES:
        lines.append(
            f"| `{case.case_id}` | `{case.stage4b_status}` | {str(case.hard_4c_confirmed).lower()} | {case.notes} |"
        )
    lines.extend(
        [
            "",
            "## Hard 4C Gate",
            "",
            "- contract cancellation",
            "- financing failure",
            "- government budget cut",
            "- customer order cancellation",
            "- delivery delay that damages earnings",
            "- backlog quality deterioration",
            "- margin collapse",
            "- accounting/disclosure trust break",
            "- persistent sanctions/export control",
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
    "ROUND192_CASE_CANDIDATES",
    "ROUND192_DEFAULT_AUDIT_PATH",
    "ROUND192_DEFAULT_CASES_PATH",
    "ROUND192_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND192_GREEN_FORBIDDEN_PATTERNS",
    "ROUND192_GREEN_REQUIRED_FIELDS",
    "ROUND192_PRICE_BACKFILL_FIELDS",
    "ROUND192_REQUIRED_TARGET_ALIASES",
    "ROUND192_SCORE_ADJUSTMENTS",
    "ROUND192_SOURCE_ROUND_PATH",
    "ROUND192_STAGE4B_STATUSES",
    "Round192CaseCandidate",
    "Round192ScoreAdjustment",
    "render_round192_green_gate_review_markdown",
    "render_round192_price_backfill_plan_markdown",
    "render_round192_stage4b_4c_review_markdown",
    "render_round192_summary_markdown",
    "round192_audit_payload",
    "round192_case_records",
    "round192_case_rows",
    "round192_price_backfill_field_rows",
    "round192_score_adjustment_rows",
    "round192_summary",
    "round192_target_alias_rows",
    "write_round192_r1_loop7_reports",
]
