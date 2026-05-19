"""Round-200 R9 Loop-7 mobility/transport/leisure price-path validation pack.

Round 200 is a calibration-only layer for Korean auto hybrid/value-up,
tariff-localization, SDV delay, airline integration, airline safety, freight
cycle, tourism policy, duty-free, and casino utilization cases. It records why
auto/airline/freight/tourism headlines must be separated from unit economics,
FCF after capex, margin durability, shareholder return execution, load factor
with yield, integration synergy, freight normalization, tourist spend, casino
drop/hold, and operational trust.

Simple example: China visa-free tourism policy can be Stage 1 or Stage 2
attention. It is not Stage 3-Green until tourist spend, duty-free sales, OPM,
and inventory turns are visible as-of the case date.

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


ROUND200_SOURCE_ROUND_PATH = "docs/round/round_200.md"
ROUND200_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round200_r9_loop7_mobility_transport_leisure_price_validation"
ROUND200_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r9_loop7_round200.jsonl"
ROUND200_DEFAULT_AUDIT_PATH = (
    "data/sector_taxonomy/round200_r9_loop7_mobility_transport_leisure_price_validation_audit.json"
)

ROUND200_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "AUTO_MOBILITY_COMPLETED_VEHICLE": E2RArchetype.AUTO_MOBILITY_COMPLETED_VEHICLE.value,
    "AUTO_HYBRID_VALUEUP": E2RArchetype.AUTO_HYBRID_VALUEUP.value,
    "AUTO_TARIFF_LOCALIZATION": E2RArchetype.AUTO_TARIFF_LOCALIZATION.value,
    "AUTO_SDV_DELAY_CAPEX_OVERLAY": E2RArchetype.AUTO_SDV_DELAY_CAPEX_OVERLAY.value,
    "AUTO_MOBILITY_COMPONENTS": E2RArchetype.AUTO_MOBILITY_COMPONENTS.value,
    "AUTO_COMPONENT_QUALITY_RECALL_OVERLAY": E2RArchetype.AUTO_COMPONENT_QUALITY_RECALL_OVERLAY.value,
    "HYBRID_COMPONENT_BOTTLENECK": E2RArchetype.HYBRID_COMPONENT_BOTTLENECK.value,
    "AIRLINE_INTEGRATION_SCALE": E2RArchetype.AIRLINE_INTEGRATION_SCALE.value,
    "AIRLINE_TRAVEL_CYCLE": E2RArchetype.AIRLINE_TRAVEL_CYCLE.value,
    "AIRLINE_SAFETY_REGULATORY_OVERLAY": E2RArchetype.AIRLINE_SAFETY_REGULATORY_OVERLAY.value,
    "TRANSPORT_SAFETY_REGULATORY_OVERLAY": E2RArchetype.TRANSPORT_SAFETY_REGULATORY_OVERLAY.value,
    "CASINO_DUTYFREE_TOURISM": E2RArchetype.CASINO_DUTYFREE_TOURISM.value,
    "CASINO_DUTYFREE_TOURISM_POLICY_KOREA": E2RArchetype.CASINO_DUTYFREE_TOURISM_POLICY_KOREA.value,
    "CASINO_RETURN_VISITOR_UNIT_ECONOMICS": E2RArchetype.CASINO_RETURN_VISITOR_UNIT_ECONOMICS.value,
    "TRAVEL_LEISURE_REOPENING": E2RArchetype.TRAVEL_LEISURE_REOPENING.value,
    "TOURISM_POLICY_EVENT": E2RArchetype.TOURISM_POLICY_EVENT.value,
    "SHIPPING_FREIGHT_CYCLE": E2RArchetype.SHIPPING_FREIGHT_CYCLE.value,
    "SHIPPING_FREIGHT_CYCLE_KOREA": E2RArchetype.SHIPPING_FREIGHT_CYCLE_KOREA.value,
    "LOGISTICS_PARCEL_FREIGHT": E2RArchetype.LOGISTICS_PARCEL_FREIGHT.value,
    "RENTAL_USED_CAR_MOBILITY": E2RArchetype.RENTAL_USED_CAR_MOBILITY.value,
    "AUTONOMOUS_ROBOTAXI_DEPLOYMENT": E2RArchetype.AUTONOMOUS_ROBOTAXI_DEPLOYMENT.value,
    "FLEET_UNIT_ECONOMICS_OVERLAY": E2RArchetype.FLEET_UNIT_ECONOMICS_OVERLAY.value,
}

ROUND200_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "unit_economics_confirmed",
    "fcf_after_capex_confirmed",
    "margin_durability_confirmed",
    "hybrid_mix_load_factor_freight_contract_or_tourist_spend_confirmed",
    "shareholder_return_or_deleveraging_confirmed",
    "safety_and_operational_trust_passed",
    "tariff_fuel_fx_freight_normalization_stress_passed",
    "price_path_after_unit_economics",
)

ROUND200_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "travel_reopening_only",
    "freight_rate_spike_only",
    "robotaxi_or_sdv_story_only",
    "tourist_arrival_policy_only",
    "merger_completion_without_synergy",
    "ev_or_ai_mobility_theme_only",
    "capex_heavy_localization_without_margin",
    "safety_failure",
    "tariff_margin_cut",
    "utilization_weak",
    "cycle_normalization",
)

ROUND200_STAGE4B_STATUSES: tuple[str, ...] = ("none", "watch", "elevated", "graduated")

ROUND200_HARD_4C_GATES: tuple[str, ...] = (
    "fatal_safety_accident",
    "operational_trust_break",
    "margin_guidance_cut_with_structural_cause",
    "tariff_shock_not_offset_by_localization",
    "fuel_cost_spike_not_passed_through",
    "freight_rate_collapse",
    "container_overcapacity",
    "integration_failure",
    "regulatory_block",
    "tourist_spend_failure",
    "casino_utilization_collapse",
    "debt_or_capex_burden",
)

ROUND200_PRICE_BACKFILL_FIELDS: tuple[str, ...] = (
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
    "MFE_5D",
    "MFE_20D",
    "MFE_30D",
    "MFE_60D",
    "MFE_90D",
    "MFE_180D",
    "MFE_1Y",
    "MFE_2Y",
    "MAE_5D",
    "MAE_20D",
    "MAE_30D",
    "MAE_60D",
    "MAE_90D",
    "MAE_180D",
    "MAE_1Y",
    "MAE_2Y",
    "drawdown_after_peak",
    "relative_strength_vs_kospi",
    "relative_strength_vs_auto_basket",
    "relative_strength_vs_airline_basket",
    "relative_strength_vs_shipping_basket",
    "relative_strength_vs_tourism_basket",
    "hybrid_mix",
    "fcf_after_capex",
    "shareholder_return_execution",
    "operating_margin",
    "localization_ratio",
    "tariff_cost",
    "margin_guidance_cut_flag",
    "unit_economics",
    "load_factor",
    "yield",
    "integration_synergy",
    "fleet_utilization",
    "freight_rate",
    "tourist_spend",
    "casino_drop",
    "casino_hold_rate",
    "safety_incident_flag",
    "hard_4c_confirmed",
)


@dataclass(frozen=True)
class Round200ScoreAdjustment:
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
class Round200CaseCandidate:
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
        return Round10LargeSector.MOBILITY_TRANSPORT_LEISURE

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND200_SCORE_ADJUSTMENTS: tuple[Round200ScoreAdjustment, ...] = (
    Round200ScoreAdjustment("hybrid_mix", 5, "raise", "완성차 Green은 hybrid mix가 실제 margin과 FCF로 내려올 때 강하다."),
    Round200ScoreAdjustment("fcf_after_capex", 5, "raise", "R9는 투자 이후 남는 FCF가 핵심이다."),
    Round200ScoreAdjustment("shareholder_return_execution", 4, "raise", "자사주/배당 실행은 value-up의 실제 증거다."),
    Round200ScoreAdjustment("operating_margin_durability", 4, "raise", "OPM 목표가 유지되어야 체급 변화가 지속된다."),
    Round200ScoreAdjustment("localization_tariff_hedge", 3, "raise", "현지화는 tariff 충격을 흡수할 때만 점수를 준다."),
    Round200ScoreAdjustment("unit_economics", 5, "raise", "운송/레저는 단위경제성이 Stage 3의 중심이다."),
    Round200ScoreAdjustment("load_factor_with_yield", 4, "raise", "항공은 탑승률과 yield가 같이 좋아야 한다."),
    Round200ScoreAdjustment("integration_synergy_realized", 4, "raise", "합병 완료보다 실제 통합 시너지와 비용절감이 중요하다."),
    Round200ScoreAdjustment("fleet_utilization", 4, "raise", "차량/항공/카지노/리조트는 가동률이 숫자로 보여야 한다."),
    Round200ScoreAdjustment("tourist_spend_conversion", 4, "raise", "관광객 수보다 실제 객단가와 구매전환이 중요하다."),
    Round200ScoreAdjustment("casino_drop_and_hold", 4, "raise", "카지노는 drop과 hold rate가 확인되어야 한다."),
    Round200ScoreAdjustment("safety_record_and_operational_trust", 5, "raise", "운송 섹터 Green은 안전과 운영신뢰를 통과해야 한다."),
    Round200ScoreAdjustment("travel_reopening_only", -5, "lower", "여행수요 회복만으로 Stage 3-Green을 만들지 않는다."),
    Round200ScoreAdjustment("freight_rate_spike_only", -5, "lower", "운임 spike는 구조적 E2R보다 사이클로 분리한다."),
    Round200ScoreAdjustment("robotaxi_or_sdv_story_only", -5, "lower", "SDV/로보택시 narrative는 유료 SW 매출과 안전 전까지 Stage 1~2다."),
    Round200ScoreAdjustment("tourist_arrival_policy_only", -4, "lower", "무비자/입국자 증가는 spend와 OPM 전까지 정책 이벤트다."),
    Round200ScoreAdjustment("merger_completion_without_synergy", -3, "lower", "합병 완료만으로 통합 시너지를 발명하지 않는다."),
    Round200ScoreAdjustment("ev_or_ai_mobility_theme_only", -4, "lower", "EV/AI mobility 테마는 FCF와 unit economics 전까지 제한한다."),
    Round200ScoreAdjustment("capex_heavy_localization_without_margin", -3, "lower", "현지화 CAPEX가 margin을 훼손하면 Green을 낮춘다."),
    Round200ScoreAdjustment("safety_failure", -5, "lower", "fatal safety accident는 hard RedTeam이다."),
    Round200ScoreAdjustment("tariff_margin_cut", -4, "lower", "관세로 margin guidance가 하향되면 4C-watch다."),
    Round200ScoreAdjustment("utilization_weak", -4, "lower", "가동률/객단가/drop 부진은 여행·카지노 Green을 막는다."),
    Round200ScoreAdjustment("cycle_normalization", -4, "lower", "운임/여행/수요 정상화는 4B/4C watch다."),
)


ROUND200_CASE_CANDIDATES: tuple[Round200CaseCandidate, ...] = (
    Round200CaseCandidate(
        case_id="hyundai_motor_hybrid_valueup_tariff_4c_watch",
        symbol="005380",
        company_name="현대차",
        primary_archetype=E2RArchetype.AUTO_HYBRID_VALUEUP,
        secondary_archetypes=(E2RArchetype.AUTO_MOBILITY_COMPLETED_VEHICLE, E2RArchetype.AUTO_TARIFF_LOCALIZATION),
        case_type="structural_success",
        stage1_date=None,
        stage2_date=date(2024, 8, 28),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 9, 18),
        stage3_decision="conditional_until_hybrid_mix_fcf_buyback_execution_margin_and_tariff_localization_are_verified",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("hybrid_sales_target_1_33m_2028", "4tn_krw_buyback_2025_2027", "dividend_expansion", "opm_target_10pct_2030"),
        red_flag_fields=("tariff_margin_cut_2025_watch", "us_localization_capex", "margin_guidance_cut", "tariff_cost_absorption_unverified"),
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="green_success",
        price_validation_status="needs_ohlc_backfill",
        notes="Hybrid/value-up is a strong Stage 2 or conditional Stage 3 candidate, while tariff margin cut remains 4C-watch.",
    ),
    Round200CaseCandidate(
        case_id="kia_hybrid_valueup_sdv_delay_capex_watch",
        symbol="000270",
        company_name="기아",
        primary_archetype=E2RArchetype.AUTO_HYBRID_VALUEUP,
        secondary_archetypes=(E2RArchetype.AUTO_SDV_DELAY_CAPEX_OVERLAY, E2RArchetype.AUTO_MOBILITY_COMPLETED_VEHICLE),
        case_type="success_candidate",
        stage1_date=None,
        stage2_date=date(2026, 4, 9),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2026, 4, 9),
        stage3_decision="deferred_until_hybrid_mix_opm_fcf_shareholder_return_and_paid_sdv_software_revenue_are_visible",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("hybrid_expansion", "sdv_ai_mobility_investment_plan", "investment_plan_up_30pct", "humanoid_robot_factory_option"),
        red_flag_fields=("sdv_launch_delay_2028", "ev_target_cut", "capex_burden", "software_revenue_unverified", "event_day_price_down_5_5pct"),
        score_price_alignment="evidence_good_but_price_failed",
        rerating_result="unknown",
        stage_failure_type="false_yellow",
        price_validation_status="needs_ohlc_backfill",
        notes="Hybrid can score, but SDV delay and capex burden keep the case in watch/yellow until unit economics are visible.",
    ),
    Round200CaseCandidate(
        case_id="korean_air_asiana_integration_scale_stage2_watch",
        symbol="003490",
        company_name="대한항공",
        primary_archetype=E2RArchetype.AIRLINE_INTEGRATION_SCALE,
        secondary_archetypes=(E2RArchetype.AIRLINE_TRAVEL_CYCLE, E2RArchetype.TRANSPORT_SAFETY_REGULATORY_OVERLAY),
        case_type="success_candidate",
        stage1_date=None,
        stage2_date=date(2024, 12, 12),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="deferred_until_integration_synergy_route_optimization_load_factor_yield_debt_lcc_integration_and_fcf",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("asiana_acquisition_completed", "63_88pct_stake_secured", "international_capacity_scale", "route_optimization_lcc_integration_plan"),
        red_flag_fields=("integration_synergy_unverified", "mileage_conflict_watch", "debt_burden", "service_quality_watch", "fuel_cost_watch"),
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="needs_ohlc_backfill",
        notes="Asiana completion is Stage 2; Green waits for integration synergy, FCF, load factor, yield, and service quality.",
    ),
    Round200CaseCandidate(
        case_id="jeju_air_fatal_crash_operational_trust_4c_break",
        symbol="089590",
        company_name="제주항공",
        primary_archetype=E2RArchetype.AIRLINE_SAFETY_REGULATORY_OVERLAY,
        secondary_archetypes=(E2RArchetype.AIRLINE_TRAVEL_CYCLE, E2RArchetype.TRANSPORT_SAFETY_REGULATORY_OVERLAY),
        case_type="4c_thesis_break",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2024, 12, 30),
        stage3_decision="hard_blocked_by_fatal_safety_accident_and_operational_trust_break",
        stage4b_status="none",
        hard_4c_confirmed=True,
        evidence_fields=("fatal_crash_muan_airport", "179_fatalities", "shares_record_low_after_crash", "government_safety_inspection"),
        red_flag_fields=("fatal_safety_accident", "operational_trust_break", "safety_investigation_long_tail", "consumer_confidence_damage"),
        score_price_alignment="aligned",
        rerating_result="thesis_break",
        stage_failure_type="should_have_been_red",
        price_validation_status="needs_ohlc_backfill",
        notes="Fatal accident is an R9 hard 4C gate; travel demand cannot override operational trust break.",
    ),
    Round200CaseCandidate(
        case_id="hmm_red_sea_freight_cycle_stage2_4b_watch",
        symbol="011200",
        company_name="HMM",
        primary_archetype=E2RArchetype.SHIPPING_FREIGHT_CYCLE,
        secondary_archetypes=(E2RArchetype.SHIPPING_FREIGHT_CYCLE_KOREA,),
        case_type="cyclical_success",
        stage1_date=None,
        stage2_date=date(2025, 11, 6),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="deferred_freight_spike_is_cycle_until_long_contract_fcf_dividend_and_capacity_discipline_are_visible",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("red_sea_disruption", "container_volume_growth", "maersk_guidance_raise", "freight_rebound"),
        red_flag_fields=("freight_rate_spike_only", "container_overcapacity", "red_sea_normalization_watch", "freight_peak_out_watch", "cycle_normalization"),
        score_price_alignment="unknown",
        rerating_result="cyclical_rerating",
        stage_failure_type="stage2_watch_success",
        price_validation_status="needs_ohlc_backfill",
        notes="Freight rebound can create MFE, but shipping stays cyclical until contract, FCF, dividend, and capacity discipline are visible.",
    ),
    Round200CaseCandidate(
        case_id="hotel_shilla_china_visa_tourism_event_stage2_watch",
        symbol="008770",
        company_name="호텔신라",
        primary_archetype=E2RArchetype.CASINO_DUTYFREE_TOURISM,
        secondary_archetypes=(E2RArchetype.TRAVEL_LEISURE_REOPENING, E2RArchetype.TOURISM_POLICY_EVENT, E2RArchetype.CASINO_DUTYFREE_TOURISM_POLICY_KOREA),
        case_type="success_candidate",
        stage1_date=date(2025, 3, 20),
        stage2_date=date(2025, 9, 29),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="deferred_until_dutyfree_sales_spend_per_tourist_conversion_commission_rate_opm_and_inventory_turns",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("china_group_visa_free_policy_announced", "china_group_visa_free_program_started", "dutyfree_cruise_tour_response", "visitor_count_recovery"),
        red_flag_fields=("tourist_arrival_policy_only", "tourist_spend_unverified", "opm_unverified", "inventory_turn_unverified", "policy_event_premium"),
        score_price_alignment="unknown",
        rerating_result="event_premium",
        stage_failure_type="stage2_watch_success",
        price_validation_status="needs_ohlc_backfill",
        notes="Visa-free tourism is Stage 1~2; Green waits for duty-free spend, conversion, OPM, and inventory turns.",
    ),
    Round200CaseCandidate(
        case_id="lotte_tour_dream_tower_casino_utilization_gap_watch",
        symbol="032350",
        company_name="롯데관광개발",
        primary_archetype=E2RArchetype.CASINO_RETURN_VISITOR_UNIT_ECONOMICS,
        secondary_archetypes=(E2RArchetype.CASINO_DUTYFREE_TOURISM, E2RArchetype.TRAVEL_LEISURE_REOPENING, E2RArchetype.TOURISM_POLICY_EVENT),
        case_type="failed_rerating",
        stage1_date=date(2025, 9, 29),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="insufficient_company_level_drop_hold_occupancy_adr_repeat_visitor_fcf_and_debt_evidence",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("china_tourism_policy_watch", "jeju_foreigner_casino_exposure", "dream_tower_casino_hotel_option"),
        red_flag_fields=("casino_drop_unverified", "hold_rate_unverified", "occupancy_unverified", "tourism_policy_event_only", "debt_and_utilization_watch"),
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="unknown",
        price_validation_status="needs_ohlc_backfill",
        notes="Casino/tourism policy is Stage 1 attention only before drop, hold, occupancy, ADR, repeat visitors, and FCF.",
    ),
)


def round200_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND200_CASE_CANDIDATES:
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
                "Round200 R9 Loop-7 mobility/transport/leisure price-path validation case. "
                "This is calibration-only and must not be used for candidate generation."
            ),
            stage1_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "policy" in field or "option" in field or "recovery" in field or "disruption" in field or "target" in field
            ),
            stage2_evidence=candidate.evidence_fields if candidate.stage2_date else (),
            stage3_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "buyback" in field or "opm" in field or "fcf" in field or "synergy" in field or "unit" in field
            ),
            stage4b_evidence=tuple(
                field
                for field in (*candidate.evidence_fields, *candidate.red_flag_fields)
                if "price" in field or "premium" in field or "spike" in field or "peak" in field or "cycle" in field or "policy" in field
            ),
            stage4c_evidence=tuple(
                field
                for field in candidate.red_flag_fields
                if "safety" in field
                or "trust" in field
                or "tariff" in field
                or "margin" in field
                or "overcapacity" in field
                or "normalization" in field
                or "utilization" in field
                or "debt" in field
            ),
            must_have_fields=ROUND200_GREEN_REQUIRED_FIELDS,
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
                "hybrid_mix_delta": 5.0,
                "fcf_after_capex_delta": 5.0,
                "shareholder_return_execution_delta": 4.0,
                "operating_margin_durability_delta": 4.0,
                "unit_economics_delta": 5.0,
                "safety_record_and_operational_trust_delta": 5.0,
                "travel_reopening_only_delta": -5.0,
                "freight_rate_spike_only_delta": -5.0,
                "safety_failure_delta": -5.0,
                "tariff_margin_cut_delta": -4.0,
            },
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "needs_ohlc_backfill_true",
                "do_not_invent_price_or_stage_dates",
                "do_not_treat_policy_freight_reopening_merger_or_sdv_headline_as_green_evidence",
                *ROUND200_GREEN_REQUIRED_FIELDS,
                *ROUND200_GREEN_FORBIDDEN_PATTERNS,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=True,
                report_data_available=True,
                price_data_available=False,
                stage_dates_confidence=0.8 if candidate.stage2_date or candidate.stage4c_date else 0.35,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round200_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND200_CASE_CANDIDATES:
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


def round200_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND200_SCORE_ADJUSTMENTS)


def round200_price_backfill_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round200_backfill": "true"} for field in ROUND200_PRICE_BACKFILL_FIELDS)


def round200_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {"round200_label": label, "canonical_archetype": canonical}
        for label, canonical in ROUND200_REQUIRED_TARGET_ALIASES.items()
    )


def round200_summary() -> dict[str, int | bool]:
    cases = round200_case_records()
    return {
        "case_candidate_count": len(cases),
        "required_target_count": len(ROUND200_REQUIRED_TARGET_ALIASES),
        "score_adjustment_count": len(ROUND200_SCORE_ADJUSTMENTS),
        "price_backfill_field_count": len(ROUND200_PRICE_BACKFILL_FIELDS),
        "structural_success_count": sum(1 for case in cases if case.case_type == "structural_success"),
        "success_candidate_count": sum(1 for case in cases if case.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for case in cases if case.case_type == "cyclical_success"),
        "failed_rerating_count": sum(1 for case in cases if case.case_type == "failed_rerating"),
        "hard_4c_case_count": sum(1 for case in ROUND200_CASE_CANDIDATES if case.hard_4c_confirmed),
        "stage3_case_count": sum(1 for case in ROUND200_CASE_CANDIDATES if case.stage3_date),
        "stage4b_watch_or_elevated_count": sum(
            1 for case in ROUND200_CASE_CANDIDATES if case.stage4b_status in {"watch", "elevated"}
        ),
        "needs_ohlc_backfill_count": sum(1 for case in ROUND200_CASE_CANDIDATES if case.price_validation_status == "needs_ohlc_backfill"),
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
        "needs_ohlc_backfill": True,
    }


def write_round200_r9_loop7_reports(
    *,
    output_directory: str | Path = ROUND200_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND200_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND200_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    cases = write_case_library(round200_case_records(), cases_path)
    audit = Path(audit_path)
    audit.parent.mkdir(parents=True, exist_ok=True)
    paths = {
        "cases": cases,
        "audit_json": audit,
        "summary": output / "round200_r9_loop7_price_validation_summary.md",
        "case_matrix": output / "round200_r9_loop7_case_matrix.csv",
        "target_aliases": output / "round200_r9_loop7_target_aliases.csv",
        "score_adjustments": output / "round200_r9_loop7_score_adjustments.csv",
        "price_backfill_fields": output / "round200_r9_loop7_price_backfill_fields.csv",
        "green_gate_review": output / "round200_r9_loop7_green_gate_review.md",
        "price_backfill_plan": output / "round200_r9_loop7_price_backfill_plan.md",
        "stage4b_4c_review": output / "round200_r9_loop7_stage4b_4c_review.md",
    }
    audit.write_text(json.dumps(round200_audit_payload(), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_rows(round200_case_rows(), paths["case_matrix"])
    _write_rows(round200_target_alias_rows(), paths["target_aliases"])
    _write_rows(round200_score_adjustment_rows(), paths["score_adjustments"])
    _write_rows(round200_price_backfill_field_rows(), paths["price_backfill_fields"])
    paths["summary"].write_text(render_round200_summary_markdown(), encoding="utf-8")
    paths["green_gate_review"].write_text(render_round200_green_gate_review_markdown(), encoding="utf-8")
    paths["price_backfill_plan"].write_text(render_round200_price_backfill_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round200_stage4b_4c_review_markdown(), encoding="utf-8")
    return paths


def round200_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND200_SOURCE_ROUND_PATH,
        "large_sector": Round10LargeSector.MOBILITY_TRANSPORT_LEISURE.value,
        "summary": round200_summary(),
        "target_aliases": list(round200_target_alias_rows()),
        "green_required_fields": list(ROUND200_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND200_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_statuses": list(ROUND200_STAGE4B_STATUSES),
        "hard_4c_gates": list(ROUND200_HARD_4C_GATES),
        "score_adjustments": list(round200_score_adjustment_rows()),
        "case_ids": [case.case_id for case in ROUND200_CASE_CANDIDATES],
        "what_not_to_change": [
            "do_not_apply_to_production_scoring_yet",
            "do_not_use_round200_cases_as_candidate_generation_input",
            "do_not_lower_stage3_green_thresholds",
            "do_not_treat_travel_reopening_freight_spike_sdv_policy_merger_or_tourism_headline_as_green_evidence",
            "do_not_invent_unit_economics_fcf_margin_load_factor_yield_tourist_spend_drop_hold_or_stage_prices",
            "do_not_confirm_hard_4c_without_reliable_primary_or_major_source",
        ],
    }


def render_round200_summary_markdown() -> str:
    summary = round200_summary()
    lines = [
        "# Round-200 R9 Loop-7 Price-Path Validation Summary",
        "",
        f"- source_round: `{ROUND200_SOURCE_ROUND_PATH}`",
        "- large_sector: `MOBILITY_TRANSPORT_LEISURE`",
        "- scope: auto hybrid/value-up, tariff-localization, airline integration, safety, freight cycle, tourism policy, duty-free, and casino utilization",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- required_target_count: {summary['required_target_count']}",
        f"- score_adjustment_count: {summary['score_adjustment_count']}",
        f"- price_backfill_field_count: {summary['price_backfill_field_count']}",
        f"- structural_success_count: {summary['structural_success_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- cyclical_success_count: {summary['cyclical_success_count']}",
        f"- failed_rerating_count: {summary['failed_rerating_count']}",
        f"- hard_4c_case_count: {summary['hard_4c_case_count']}",
        f"- stage3_case_count: {summary['stage3_case_count']}",
        f"- stage4b_watch_or_elevated_count: {summary['stage4b_watch_or_elevated_count']}",
        f"- needs_ohlc_backfill_count: {summary['needs_ohlc_backfill_count']}",
        "- production_scoring_changed: false",
        "- candidate_generation_input: false",
        "- shadow_weight_only: true",
        "- needs_ohlc_backfill: true",
        "",
        "## Interpretation",
        "",
        "- R9는 hybrid/value-up처럼 구조 후보가 있지만, 해운·항공·여행은 사이클과 이벤트가 가격을 먼저 밀기 쉽다.",
        "- 현대차는 hybrid mix, 주주환원, OPM target이 강하지만 tariff margin cut을 4C-watch로 붙인다.",
        "- 기아 SDV/AI mobility는 paid software revenue와 unit economics 전 Stage 3가 아니다.",
        "- 대한항공 Asiana completion은 Stage 2지만 통합 시너지, FCF, load factor, yield 전 Green 금지다.",
        "- 제주항공 fatal accident는 operational trust hard 4C gate다.",
        "- HMM freight rebound는 cyclical success로 보고 구조적 Green과 분리한다.",
        "- 호텔신라/롯데관광개발은 관광객 수보다 tourist spend, drop, hold, occupancy, OPM이 필요하다.",
        "",
        "쉬운 예: `as_of_date=2025-09-29`에 중국 무비자 정책이 시작되어도 면세 매출과 객단가가 없으면 Stage 3-Green이 아니라 Stage 1~2 watch다.",
    ]
    return "\n".join(lines) + "\n"


def render_round200_green_gate_review_markdown() -> str:
    lines = [
        "# Round-200 R9 Loop-7 Green Gate Review",
        "",
        "## Green Required Evidence",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND200_GREEN_REQUIRED_FIELDS)
    lines.extend(["", "## Green Forbidden Patterns", ""])
    lines.extend(f"- `{field}`" for field in ROUND200_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(["", "## Shadow Score Adjustments", "", "| axis | direction | points | reason |", "| --- | --- | ---: | --- |"])
    for adjustment in ROUND200_SCORE_ADJUSTMENTS:
        lines.append(f"| `{adjustment.axis}` | {adjustment.direction} | {adjustment.points} | {adjustment.reason} |")
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not apply these weights to production scoring yet.",
            "- Do not use Round200 cases as candidate-generation input.",
            "- Do not lower Stage 3-Green thresholds to force promotion.",
            "- Do not invent unit economics, FCF, margin, load factor, yield, tourist spend, drop, hold, stage prices, or MFE/MAE.",
            "- Do not treat travel reopening, freight spike, SDV/robotaxi story, tourism policy, or merger completion as Green evidence alone.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round200_price_backfill_plan_markdown() -> str:
    lines = [
        "# Round-200 R9 Loop-7 Price Backfill Plan",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND200_PRICE_BACKFILL_FIELDS)
    lines.extend(["", "## Priority Cases", "", "| case | stage marker | current status | 4B status | hard 4C |", "| --- | --- | --- | --- | --- |"])
    for case in ROUND200_CASE_CANDIDATES:
        stage_marker = case.stage3_date or case.stage2_date or case.stage4b_date or case.stage4c_date or case.stage1_date
        lines.append(
            f"| `{case.case_id}` | {_date_text(stage_marker) or 'undated'} | "
            f"{case.price_validation_status} | `{case.stage4b_status}` | {str(case.hard_4c_confirmed).lower()} |"
        )
    lines.extend(
        [
            "",
            "## Backfill Rule",
            "",
            "- Use official OHLC data for exact MFE/MAE.",
            "- Keep unknown values null or `needs_ohlc_backfill`.",
            "- Split hybrid/value-up, tariff shock, SDV delay, merger, fatal safety, freight, and tourism policy dates.",
            "- Do not create a Stage 3 anchor when the case intentionally has no Stage 3 date.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round200_stage4b_4c_review_markdown() -> str:
    lines = [
        "# Round-200 R9 Loop-7 Stage 4B / 4C Review",
        "",
        "## 4B Status Definitions",
        "",
        "- `watch`: hybrid/value-up, merger, freight spike, tourism policy, or SDV narrative runs ahead of unit economics.",
        "- `elevated`: margin guidance cuts, tariff cost, fuel cost, freight peak, weak tourist spend, or integration cost appears.",
        "- `graduated`: good sales, freight, or tourist numbers stop surprising and price reaction fades.",
        "",
        "## Hard 4C Gates",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND200_HARD_4C_GATES)
    lines.extend(
        [
            "",
            "## R9 Interpretation",
            "",
            "- fatal safety accident is hard 4C even if travel demand is strong.",
            "- tariff margin cut is 4C-watch unless localization offsets the structural margin hit.",
            "- freight spike is cyclical success and should not become structural Green by itself.",
            "- tourism policy needs spend, OPM, drop, hold, and utilization before Green.",
            "",
            "## Case Review",
            "",
            "| case | 4B status | hard 4C confirmed | interpretation |",
            "| --- | --- | --- | --- |",
        ]
    )
    for case in ROUND200_CASE_CANDIDATES:
        lines.append(
            f"| `{case.case_id}` | `{case.stage4b_status}` | {str(case.hard_4c_confirmed).lower()} | {case.notes} |"
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


__all__ = [
    "ROUND200_CASE_CANDIDATES",
    "ROUND200_DEFAULT_AUDIT_PATH",
    "ROUND200_DEFAULT_CASES_PATH",
    "ROUND200_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND200_GREEN_FORBIDDEN_PATTERNS",
    "ROUND200_GREEN_REQUIRED_FIELDS",
    "ROUND200_HARD_4C_GATES",
    "ROUND200_PRICE_BACKFILL_FIELDS",
    "ROUND200_REQUIRED_TARGET_ALIASES",
    "ROUND200_SCORE_ADJUSTMENTS",
    "ROUND200_SOURCE_ROUND_PATH",
    "ROUND200_STAGE4B_STATUSES",
    "Round200CaseCandidate",
    "Round200ScoreAdjustment",
    "render_round200_green_gate_review_markdown",
    "render_round200_price_backfill_plan_markdown",
    "render_round200_stage4b_4c_review_markdown",
    "render_round200_summary_markdown",
    "round200_audit_payload",
    "round200_case_records",
    "round200_case_rows",
    "round200_price_backfill_field_rows",
    "round200_score_adjustment_rows",
    "round200_summary",
    "round200_target_alias_rows",
    "write_round200_r9_loop7_reports",
]
