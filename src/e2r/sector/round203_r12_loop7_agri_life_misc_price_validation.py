"""Round-203 R12 Loop-7 agri/life/misc price-path validation pack.

Round 203 is a calibration-only layer for agriculture, education, rental,
kiosk/life service, regulated consumer, and livestock disease event cases.
The default posture is conservative: most R12 stories start as Watch/Event,
not Stage 3-Green.

Simple example: a medical-school quota policy headline can move education
stocks. It is not Stage 3-Green until company-level students, repeat course
revenue, ARPU, OPM, and cash conversion are visible as-of the case date.

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


ROUND203_SOURCE_ROUND_PATH = "docs/round/round_203.md"
ROUND203_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round203_r12_loop7_agri_life_misc_price_validation"
ROUND203_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r12_loop7_round203.jsonl"
ROUND203_DEFAULT_AUDIT_PATH = "data/sector_taxonomy/round203_r12_loop7_agri_life_misc_price_validation_audit.json"

ROUND203_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "SMART_FARM_AGRI_TECH": E2RArchetype.SMART_FARM_AGRI_TECH.value,
    "AGRI_MACHINERY_DEMAND_CYCLE": E2RArchetype.AGRI_MACHINERY_DEMAND_CYCLE.value,
    "AGRI_MACHINERY_SOFTWARE_LOCKIN": E2RArchetype.AGRI_MACHINERY_SOFTWARE_LOCKIN.value,
    "AGRI_LIVESTOCK_FOOD_COMMODITY": E2RArchetype.AGRI_LIVESTOCK_FOOD_COMMODITY.value,
    "LIVESTOCK_DISEASE_PRICE_REGULATORY": E2RArchetype.LIVESTOCK_DISEASE_PRICE_REGULATORY.value,
    "AGRI_DISEASE_EVENT_OVERLAY": E2RArchetype.AGRI_DISEASE_EVENT_OVERLAY.value,
    "ANIMAL_HEALTH_BIOSECURITY": E2RArchetype.ANIMAL_HEALTH_BIOSECURITY.value,
    "EDUCATION_SPECIALTY_SERVICES": E2RArchetype.EDUCATION_SPECIALTY_SERVICES.value,
    "HOME_CHILD_EDUCATION": E2RArchetype.HOME_CHILD_EDUCATION.value,
    "EDTECH_AI_DISRUPTION": E2RArchetype.EDTECH_AI_DISRUPTION.value,
    "HOME_LIVING_APPLIANCE_RENTAL": E2RArchetype.HOME_LIVING_APPLIANCE_RENTAL.value,
    "SERVICE_KIOSK_SELF_CHECKOUT": E2RArchetype.SERVICE_KIOSK_SELF_CHECKOUT.value,
    "CONSUMER_REGULATED_PRODUCT": E2RArchetype.CONSUMER_REGULATED_PRODUCT.value,
    "NICOTINE_ALTERNATIVE_REGULATED": E2RArchetype.NICOTINE_ALTERNATIVE_REGULATED.value,
    "REGULATED_CONSUMER_APPROVAL_OVERLAY": E2RArchetype.REGULATED_CONSUMER_APPROVAL_OVERLAY.value,
}

ROUND203_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "recurring_revenue_confirmed",
    "repeat_purchase_or_repeat_course_confirmed",
    "churn_or_retention_stable",
    "arpu_or_price_pass_through_confirmed",
    "unit_economics_positive",
    "cash_conversion_confirmed",
    "inventory_and_receivables_stable",
    "regulatory_risk_passed",
    "subsidy_dependency_low",
    "price_path_after_evidence",
)

ROUND203_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "defensive_theme_only",
    "education_policy_only",
    "agri_cycle_only",
    "smart_farm_policy_only",
    "disease_event_only",
    "import_ban_event_only",
    "unconfirmed_export_theme",
    "dealer_inventory_unknown",
    "subsidy_dependent_unit_economics",
    "regulated_product_without_growth",
    "policy_news_only",
    "price_rally_before_company_evidence",
)

ROUND203_STAGE4B_STATUSES: tuple[str, ...] = ("none", "watch", "elevated", "graduated")

ROUND203_HARD_4C_GATES: tuple[str, ...] = (
    "recall_or_product_safety_issue",
    "churn_spike",
    "arpu_decline",
    "dealer_inventory_build",
    "farmer_financing_stress",
    "education_policy_reversal",
    "private_education_regulation",
    "birth_rate_demand_collapse",
    "import_ban_reversal",
    "disease_event_cleared",
    "regulatory_ban_or_youth_safety_restriction",
    "subsidy_withdrawal",
    "unit_economics_failure",
    "cash_conversion_deterioration",
)

ROUND203_PRICE_BACKFILL_FIELDS: tuple[str, ...] = (
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
    "relative_strength_vs_rental_service_basket",
    "relative_strength_vs_agri_machinery_basket",
    "relative_strength_vs_education_policy_basket",
    "relative_strength_vs_poultry_basket",
    "relative_strength_vs_regulated_consumer_basket",
    "relative_strength_vs_smart_farm_basket",
    "event_volume_spike",
    "event_turnover_spike",
    "recurring_account_count",
    "churn_rate",
    "arpu",
    "repeat_course_revenue",
    "commercial_installation_count",
    "service_contract_revenue",
    "dealer_sell_through",
    "dealer_inventory",
    "farmer_financing_terms",
    "feed_cost",
    "import_restriction_status",
    "policy_reversal_flag",
    "regulatory_pass",
    "unit_economics_metric",
    "cash_conversion",
    "hard_4c_confirmed",
)


@dataclass(frozen=True)
class Round203ScoreAdjustment:
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
class Round203CaseCandidate:
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
        return Round10LargeSector.EDUCATION_LIFE_AGRI_MISC

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND203_SCORE_ADJUSTMENTS: tuple[Round203ScoreAdjustment, ...] = (
    Round203ScoreAdjustment("recurring_revenue", 5, "raise", "R12에서 가장 강한 증거는 반복 결제 구조다."),
    Round203ScoreAdjustment("churn_stability", 5, "raise", "렌탈·교육·서비스는 churn 안정성이 visibility를 만든다."),
    Round203ScoreAdjustment("arpu_or_repeat_course", 4, "raise", "ARPU나 반복 수강 매출이 있어야 정책 이벤트를 숫자로 연결한다."),
    Round203ScoreAdjustment("cash_conversion", 5, "raise", "반복매출도 현금전환이 확인되어야 Stage 3 후보가 된다."),
    Round203ScoreAdjustment("unit_economics", 5, "raise", "스마트팜·키오스크·렌탈은 unit economics가 핵심 splitter다."),
    Round203ScoreAdjustment("commercial_installation", 4, "raise", "스마트팜은 정책보다 상업 설치와 운영계약을 우선한다."),
    Round203ScoreAdjustment("service_contract_visibility", 4, "raise", "유지보수·서비스 계약은 일회성 하드웨어 매출보다 강하다."),
    Round203ScoreAdjustment("dealer_sell_through", 4, "raise", "농기계는 딜러 재고가 아니라 실제 sell-through가 중요하다."),
    Round203ScoreAdjustment("inventory_quality", 4, "raise", "재고와 매출채권 안정은 R12 false positive를 줄인다."),
    Round203ScoreAdjustment("regulatory_pass", 4, "raise", "규제 소비재는 규제 통과와 허용 범위 확인이 필요하다."),
    Round203ScoreAdjustment("pricing_power_after_input_cost", 3, "raise", "사료비·원가 상승 후 가격전가가 확인되어야 한다."),
    Round203ScoreAdjustment("defensive_theme_only", -5, "lower", "방어주라는 이유만으로 Stage 3를 만들지 않는다."),
    Round203ScoreAdjustment("education_policy_only", -5, "lower", "교육정책은 routing 증거이며 수강생·ARPU 전 Green이 아니다."),
    Round203ScoreAdjustment("agri_cycle_only", -4, "lower", "농기계·농산물 사이클만으로 구조적 visibility를 주지 않는다."),
    Round203ScoreAdjustment("smart_farm_policy_only", -5, "lower", "스마트팜 정책/AI농업 narrative는 설치·수주 전 Stage 1이다."),
    Round203ScoreAdjustment("disease_event_only", -5, "lower", "질병 이벤트는 단기 MFE용이며 반복수요가 아니다."),
    Round203ScoreAdjustment("import_ban_event_only", -4, "lower", "수입금지 뉴스는 완화되면 event fade가 될 수 있다."),
    Round203ScoreAdjustment("unconfirmed_export_theme", -3, "lower", "수출 기대는 sell-through와 OPM 전까지 제한한다."),
    Round203ScoreAdjustment("dealer_inventory_unknown", -4, "lower", "농기계 딜러 재고가 확인되지 않으면 visibility를 낮춘다."),
    Round203ScoreAdjustment("subsidy_dependent_unit_economics", -4, "lower", "보조금 의존 unit economics는 Green blocker다."),
    Round203ScoreAdjustment("regulated_product_without_growth", -3, "lower", "규제소비재 현금흐름은 성장·환원 없이 re-rating이 제한된다."),
)


ROUND203_CASE_CANDIDATES: tuple[Round203CaseCandidate, ...] = (
    Round203CaseCandidate(
        case_id="coway_rental_recurring_service_candidate",
        symbol="021240",
        company_name="코웨이",
        primary_archetype=E2RArchetype.HOME_LIVING_APPLIANCE_RENTAL,
        secondary_archetypes=(),
        case_type="success_candidate",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="conditional_candidate_only_until_account_growth_churn_arpu_opm_and_fcf_conversion_are_visible",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("rental_account_base", "water_air_bidet_mattress_rental", "malaysia_overseas_growth", "recurring_service_revenue"),
        red_flag_fields=("churn_unverified", "arpu_unverified", "fcf_conversion_unverified", "product_safety_recall_watch", "overseas_growth_slowdown_watch"),
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="needs_ohlc_backfill",
        notes="Coway is the strongest R12 recurring-service candidate, but Stage 3 waits for account, churn, ARPU, OPM, and FCF evidence.",
    ),
    Round203CaseCandidate(
        case_id="daedong_tym_agri_machinery_export_watch",
        symbol="000490|002900",
        company_name="대동 / TYM",
        primary_archetype=E2RArchetype.AGRI_MACHINERY_DEMAND_CYCLE,
        secondary_archetypes=(E2RArchetype.AGRI_MACHINERY_SOFTWARE_LOCKIN,),
        case_type="success_candidate",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="blocked_until_north_america_dealer_sell_through_inventory_financing_opm_fcf_and_precision_agri_revenue_are_visible",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("kioti_tym_tractor_channel", "north_america_export_theme", "autonomous_tractor_expectation", "precision_agriculture_narrative"),
        red_flag_fields=("unconfirmed_export_theme", "dealer_inventory_unknown", "farmer_financing_unverified", "agri_cycle_only", "opm_unverified"),
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="unknown",
        price_validation_status="needs_ohlc_backfill",
        notes="Agri machinery export and autonomy themes are attention evidence; Green requires sell-through, inventory, financing, OPM, and FCF.",
    ),
    Round203CaseCandidate(
        case_id="megastudy_medical_quota_policy_event_watch",
        symbol="215200",
        company_name="메가스터디교육",
        primary_archetype=E2RArchetype.EDUCATION_SPECIALTY_SERVICES,
        secondary_archetypes=(E2RArchetype.HOME_CHILD_EDUCATION,),
        case_type="event_premium",
        stage1_date=None,
        stage2_date=date(2025, 3, 7),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="blocked_until_student_growth_repeat_course_arpu_opm_and_cash_conversion_are_visible",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("medical_school_quota_policy", "private_education_demand_expectation", "policy_freeze_or_adjustment", "medical_admission_policy_watch"),
        red_flag_fields=("education_policy_only", "policy_reversal_watch", "private_education_regulation_watch", "birth_rate_demand_collapse_watch"),
        score_price_alignment="price_moved_without_evidence",
        rerating_result="policy_event_rerating",
        stage_failure_type="false_yellow",
        price_validation_status="needs_ohlc_backfill",
        notes="Medical-quota policy can move education stocks, but Stage 3 needs company-level students, repeat course revenue, ARPU, and OPM.",
    ),
    Round203CaseCandidate(
        case_id="education_edtech_phone_ban_policy_watch",
        symbol="BASKET",
        company_name="교육·에듀테크 basket",
        primary_archetype=E2RArchetype.EDTECH_AI_DISRUPTION,
        secondary_archetypes=(E2RArchetype.HOME_CHILD_EDUCATION,),
        case_type="4b_watch",
        stage1_date=date(2025, 8, 27),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=date(2025, 8, 27),
        stage4c_date=None,
        stage3_decision="policy_overlay_only_not_company_stage3_evidence",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("school_mobile_phone_classroom_ban", "digital_device_policy_change", "education_policy_overlay"),
        red_flag_fields=("education_policy_only", "edtech_ai_disruption_watch", "policy_directionality_unclear", "company_revenue_impact_unverified"),
        score_price_alignment="unknown",
        rerating_result="policy_event_rerating",
        stage_failure_type="unknown",
        price_validation_status="needs_ohlc_backfill",
        notes="Classroom device policy is double-edged; use it as routing or RedTeam evidence until company revenue and margin impact are visible.",
    ),
    Round203CaseCandidate(
        case_id="poultry_basket_brazil_bird_flu_import_ban_event_fade_r12",
        symbol="BASKET",
        company_name="하림 / 마니커류 poultry basket",
        primary_archetype=E2RArchetype.LIVESTOCK_DISEASE_PRICE_REGULATORY,
        secondary_archetypes=(E2RArchetype.AGRI_DISEASE_EVENT_OVERLAY, E2RArchetype.AGRI_LIVESTOCK_FOOD_COMMODITY),
        case_type="event_premium",
        stage1_date=date(2025, 5, 19),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=date(2025, 5, 19),
        stage4c_date=date(2025, 6, 23),
        stage3_decision="blocked_until_company_level_price_pass_through_volume_margin_feed_cost_inventory_and_repeat_demand_are_visible",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("brazil_bird_flu_import_restriction", "domestic_poultry_substitution_theme", "short_term_supply_disruption", "regional_ban_easing"),
        red_flag_fields=("disease_event_only", "import_ban_event_only", "import_ban_reversal", "feed_cost_unverified", "margin_unverified"),
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="false_yellow",
        price_validation_status="needs_ohlc_backfill",
        notes="Bird-flu import restrictions can create short MFE, but easing can quickly fade the event premium.",
    ),
    Round203CaseCandidate(
        case_id="ktng_regulated_consumer_cashflow_watch",
        symbol="033780",
        company_name="KT&G",
        primary_archetype=E2RArchetype.CONSUMER_REGULATED_PRODUCT,
        secondary_archetypes=(E2RArchetype.NICOTINE_ALTERNATIVE_REGULATED, E2RArchetype.REGULATED_CONSUMER_APPROVAL_OVERLAY),
        case_type="success_candidate",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="deferred_until_volume_pricing_hnb_growth_shareholder_return_regulatory_scope_and_fcf_are_visible",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("regulated_cashflow", "tobacco_and_ginseng_business", "heated_tobacco_watch", "shareholder_return_expectation"),
        red_flag_fields=("regulated_product_without_growth", "volume_decline_watch", "youth_safety_regulation_watch", "hnb_competition_watch", "regulatory_ban_watch"),
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="needs_ohlc_backfill",
        notes="Regulated cash flow can support Stage 2 watch, but volume decline, HNB competition, and regulation must be checked before Stage 3.",
    ),
    Round203CaseCandidate(
        case_id="smart_farm_basket_unit_economics_insufficient",
        symbol="BASKET",
        company_name="스마트팜 basket",
        primary_archetype=E2RArchetype.SMART_FARM_AGRI_TECH,
        secondary_archetypes=(E2RArchetype.VERTICAL_FARMING_UNIT_ECONOMICS,),
        case_type="event_premium",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="blocked_until_commercial_installation_orders_maintenance_revenue_unit_economics_and_fcf_are_visible",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("smart_farm_policy", "ai_agriculture_narrative", "farm_adoption_research", "young_farmer_policy_watch"),
        red_flag_fields=("smart_farm_policy_only", "subsidy_dependent_unit_economics", "commercial_installation_unverified", "unit_economics_unverified", "cash_conversion_unverified"),
        score_price_alignment="unknown",
        rerating_result="no_rerating",
        stage_failure_type="unknown",
        price_validation_status="needs_ohlc_backfill",
        notes="Smart-farm policy and AI agriculture narratives stay Stage 1 until commercial installations, orders, service revenue, and unit economics are visible.",
    ),
)


def round203_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND203_CASE_CANDIDATES:
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
                "Round203 R12 Loop-7 agriculture, life service, education, rental, "
                "regulated consumer, and disease-event price-path validation case. "
                "This is calibration-only and must not be used for candidate generation."
            ),
            stage1_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "policy" in field
                or "theme" in field
                or "watch" in field
                or "narrative" in field
                or "restriction" in field
                or "cashflow" in field
                or "rental" in field
            ),
            stage2_evidence=candidate.evidence_fields if candidate.stage2_date else (),
            stage3_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "recurring" in field or "revenue" in field or "cash" in field or "account" in field
            ),
            stage4b_evidence=tuple(
                field
                for field in (*candidate.evidence_fields, *candidate.red_flag_fields)
                if "theme" in field or "policy" in field or "event" in field or "watch" in field or "ban" in field
            ),
            stage4c_evidence=tuple(
                field
                for field in candidate.red_flag_fields
                if "reversal" in field
                or "recall" in field
                or "churn" in field
                or "decline" in field
                or "regulation" in field
                or "inventory" in field
                or "unit_economics" in field
            ),
            must_have_fields=ROUND203_GREEN_REQUIRED_FIELDS,
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
                "recurring_revenue_delta": 5.0,
                "churn_stability_delta": 5.0,
                "arpu_or_repeat_course_delta": 4.0,
                "cash_conversion_delta": 5.0,
                "unit_economics_delta": 5.0,
                "commercial_installation_delta": 4.0,
                "dealer_sell_through_delta": 4.0,
                "regulatory_pass_delta": 4.0,
                "defensive_theme_only_delta": -5.0,
                "education_policy_only_delta": -5.0,
                "smart_farm_policy_only_delta": -5.0,
                "disease_event_only_delta": -5.0,
                "dealer_inventory_unknown_delta": -4.0,
            },
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "needs_ohlc_backfill_true",
                "r12_default_stage3_bias_conservative_except_recurring_service",
                "do_not_invent_price_or_stage_dates",
                "do_not_treat_defensive_policy_disease_smart_farm_agri_export_or_regulated_cashflow_theme_as_green_evidence",
                *ROUND203_GREEN_REQUIRED_FIELDS,
                *ROUND203_GREEN_FORBIDDEN_PATTERNS,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=True,
                report_data_available=True,
                price_data_available=False,
                stage_dates_confidence=0.8 if candidate.stage2_date or candidate.stage4c_date else 0.55,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round203_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND203_CASE_CANDIDATES:
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


def round203_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND203_SCORE_ADJUSTMENTS)


def round203_price_backfill_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round203_backfill": "true"} for field in ROUND203_PRICE_BACKFILL_FIELDS)


def round203_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {"round203_label": label, "canonical_archetype": canonical}
        for label, canonical in ROUND203_REQUIRED_TARGET_ALIASES.items()
    )


def round203_summary() -> dict[str, int | bool | str]:
    cases = round203_case_records()
    return {
        "case_candidate_count": len(cases),
        "required_target_count": len(ROUND203_REQUIRED_TARGET_ALIASES),
        "score_adjustment_count": len(ROUND203_SCORE_ADJUSTMENTS),
        "price_backfill_field_count": len(ROUND203_PRICE_BACKFILL_FIELDS),
        "success_candidate_count": sum(1 for case in cases if case.case_type == "success_candidate"),
        "event_premium_count": sum(1 for case in cases if case.case_type == "event_premium"),
        "watch_case_count": sum(1 for case in cases if case.case_type == "4b_watch"),
        "hard_4c_case_count": sum(1 for case in ROUND203_CASE_CANDIDATES if case.hard_4c_confirmed),
        "stage3_case_count": sum(1 for case in ROUND203_CASE_CANDIDATES if case.stage3_date),
        "stage4b_watch_or_elevated_count": sum(
            1 for case in ROUND203_CASE_CANDIDATES if case.stage4b_status in {"watch", "elevated"}
        ),
        "needs_ohlc_backfill_count": sum(
            1 for case in ROUND203_CASE_CANDIDATES if case.price_validation_status == "needs_ohlc_backfill"
        ),
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
        "needs_ohlc_backfill": True,
        "r12_default_stage3_bias": "conservative_except_recurring_service",
    }


def write_round203_r12_loop7_reports(
    *,
    output_directory: str | Path = ROUND203_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND203_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND203_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    cases = write_case_library(round203_case_records(), cases_path)
    audit = Path(audit_path)
    audit.parent.mkdir(parents=True, exist_ok=True)
    paths = {
        "cases": cases,
        "audit_json": audit,
        "summary": output / "round203_r12_loop7_price_validation_summary.md",
        "case_matrix": output / "round203_r12_loop7_case_matrix.csv",
        "target_aliases": output / "round203_r12_loop7_target_aliases.csv",
        "score_adjustments": output / "round203_r12_loop7_score_adjustments.csv",
        "price_backfill_fields": output / "round203_r12_loop7_price_backfill_fields.csv",
        "green_gate_review": output / "round203_r12_loop7_green_gate_review.md",
        "price_backfill_plan": output / "round203_r12_loop7_price_backfill_plan.md",
        "stage4b_4c_review": output / "round203_r12_loop7_stage4b_4c_review.md",
    }
    audit.write_text(json.dumps(round203_audit_payload(), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_rows(round203_case_rows(), paths["case_matrix"])
    _write_rows(round203_target_alias_rows(), paths["target_aliases"])
    _write_rows(round203_score_adjustment_rows(), paths["score_adjustments"])
    _write_rows(round203_price_backfill_field_rows(), paths["price_backfill_fields"])
    paths["summary"].write_text(render_round203_summary_markdown(), encoding="utf-8")
    paths["green_gate_review"].write_text(render_round203_green_gate_review_markdown(), encoding="utf-8")
    paths["price_backfill_plan"].write_text(render_round203_price_backfill_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round203_stage4b_4c_review_markdown(), encoding="utf-8")
    return paths


def round203_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND203_SOURCE_ROUND_PATH,
        "large_sector": Round10LargeSector.EDUCATION_LIFE_AGRI_MISC.value,
        "summary": round203_summary(),
        "target_aliases": list(round203_target_alias_rows()),
        "green_required_fields": list(ROUND203_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND203_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_statuses": list(ROUND203_STAGE4B_STATUSES),
        "hard_4c_gates": list(ROUND203_HARD_4C_GATES),
        "score_adjustments": list(round203_score_adjustment_rows()),
        "case_ids": [case.case_id for case in ROUND203_CASE_CANDIDATES],
        "what_not_to_change": [
            "do_not_apply_to_production_scoring_yet",
            "do_not_use_round203_cases_as_candidate_generation_input",
            "do_not_lower_stage3_green_thresholds",
            "do_not_treat_defensive_policy_disease_smart_farm_agri_export_or_regulated_cashflow_theme_as_green_evidence",
            "do_not_invent_accounts_churn_arpu_installations_unit_economics_cash_conversion_stage_prices_or_mfe_mae",
            "keep_r12_default_stage3_bias_conservative_except_recurring_service",
        ],
    }


def render_round203_summary_markdown() -> str:
    summary = round203_summary()
    lines = [
        "# Round-203 R12 Loop-7 Price-Path Validation Summary",
        "",
        f"- source_round: `{ROUND203_SOURCE_ROUND_PATH}`",
        "- large_sector: `EDUCATION_LIFE_AGRI_MISC`",
        "- scope: smart farm, agri machinery, education policy, rental recurring service, poultry disease event, regulated consumer, and edtech policy friction",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- required_target_count: {summary['required_target_count']}",
        f"- score_adjustment_count: {summary['score_adjustment_count']}",
        f"- price_backfill_field_count: {summary['price_backfill_field_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- watch_case_count: {summary['watch_case_count']}",
        f"- hard_4c_case_count: {summary['hard_4c_case_count']}",
        f"- stage3_case_count: {summary['stage3_case_count']}",
        f"- stage4b_watch_or_elevated_count: {summary['stage4b_watch_or_elevated_count']}",
        f"- needs_ohlc_backfill_count: {summary['needs_ohlc_backfill_count']}",
        "- production_scoring_changed: false",
        "- candidate_generation_input: false",
        "- shadow_weight_only: true",
        "- needs_ohlc_backfill: true",
        "- r12_default_stage3_bias: conservative_except_recurring_service",
        "",
        "## Interpretation",
        "",
        "- R12는 구조 후보가 있지만 대부분 Stage 1~2 또는 Event/Watch에 머문다.",
        "- 코웨이는 recurring-service 후보지만 계정·churn·ARPU·FCF 전 Stage 3 확정이 아니다.",
        "- 대동/TYM은 농기계 수출·자율주행 테마만으로 Green을 만들지 않는다.",
        "- 메가스터디교육은 의대정원 정책보다 실제 수강생·repeat course·OPM이 필요하다.",
        "- 교실 디지털기기 규제는 교육/에듀테크에 양날의 policy overlay다.",
        "- 조류독감 poultry basket은 단기 MFE 가능성이 있지만 수입제한 완화가 event fade다.",
        "- KT&G는 현금흐름 후보지만 volume decline, HNB 경쟁, 규제 리스크를 같이 본다.",
        "- 스마트팜은 상업 설치·수주·unit economics·반복서비스 전 Green 금지다.",
        "",
        "쉬운 예: `as_of_date=2025-05-19`에 조류독감 수입제한 뉴스로 poultry basket이 급등해도, 2025-06-23 제한 완화가 나오면 구조적 Stage 3가 아니라 event fade로 봐야 한다.",
    ]
    return "\n".join(lines) + "\n"


def render_round203_green_gate_review_markdown() -> str:
    lines = [
        "# Round-203 R12 Loop-7 Green Gate Review",
        "",
        "## Green Required Evidence",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND203_GREEN_REQUIRED_FIELDS)
    lines.extend(["", "## Green Forbidden Patterns", ""])
    lines.extend(f"- `{field}`" for field in ROUND203_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(["", "## Shadow Score Adjustments", "", "| axis | direction | points | reason |", "| --- | --- | ---: | --- |"])
    for adjustment in ROUND203_SCORE_ADJUSTMENTS:
        lines.append(f"| `{adjustment.axis}` | {adjustment.direction} | {adjustment.points} | {adjustment.reason} |")
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not apply these weights to production scoring yet.",
            "- Do not use Round203 cases as candidate-generation input.",
            "- Do not lower Stage 3-Green thresholds to force promotion.",
            "- Do not invent accounts, churn, ARPU, unit economics, cash conversion, stage prices, or MFE/MAE.",
            "- Do not treat policy, disease, smart-farm, agri-export, defensive, or regulated-cashflow themes as Green evidence alone.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round203_price_backfill_plan_markdown() -> str:
    lines = [
        "# Round-203 R12 Loop-7 Price Backfill Plan",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND203_PRICE_BACKFILL_FIELDS)
    lines.extend(["", "## Priority Cases", "", "| case | stage marker | current status | 4B status | hard 4C |", "| --- | --- | --- | --- | --- |"])
    for case in ROUND203_CASE_CANDIDATES:
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
            "- Event cases need short windows: 5D, 20D, and 60D matter because policy or disease fade can be fast.",
            "- Recurring-service cases need longer windows: 180D, 1Y, and 2Y matter because evidence compounds slowly.",
            "- Keep unknown values null or `needs_ohlc_backfill`.",
            "- Split policy/event date, evidence date, reversal date, and thesis-break date.",
            "- Do not create a Stage 3 anchor when the case intentionally has no Stage 3 date.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round203_stage4b_4c_review_markdown() -> str:
    lines = [
        "# Round-203 R12 Loop-7 Stage 4B / 4C Review",
        "",
        "## 4B Status Definitions",
        "",
        "- `watch`: policy, disease, smart-farm, agri-export, education, or defensive-cashflow news moves price before company evidence.",
        "- `elevated`: churn, inventory, regulatory, or unit-economics risk appears while valuation remains high.",
        "- `graduated`: good headlines stop moving price or event premium fades.",
        "",
        "## Hard 4C Gates",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND203_HARD_4C_GATES)
    lines.extend(
        [
            "",
            "## R12 Interpretation",
            "",
            "- recall, churn spike, ARPU decline, or cash-conversion deterioration breaks recurring-service theses.",
            "- dealer inventory, farmer financing stress, and agri-cycle reversal break agri machinery theses.",
            "- education policy reversal, private education regulation, or birth-rate demand collapse breaks education themes.",
            "- import-ban reversal or disease clearance can quickly fade livestock disease events.",
            "- youth-safety or product regulation can cap regulated consumer cash-flow rerating.",
            "",
            "## Case Review",
            "",
            "| case | 4B status | hard 4C confirmed | interpretation |",
            "| --- | --- | --- | --- |",
        ]
    )
    for case in ROUND203_CASE_CANDIDATES:
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
    "ROUND203_CASE_CANDIDATES",
    "ROUND203_DEFAULT_AUDIT_PATH",
    "ROUND203_DEFAULT_CASES_PATH",
    "ROUND203_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND203_GREEN_FORBIDDEN_PATTERNS",
    "ROUND203_GREEN_REQUIRED_FIELDS",
    "ROUND203_HARD_4C_GATES",
    "ROUND203_PRICE_BACKFILL_FIELDS",
    "ROUND203_REQUIRED_TARGET_ALIASES",
    "ROUND203_SCORE_ADJUSTMENTS",
    "ROUND203_SOURCE_ROUND_PATH",
    "ROUND203_STAGE4B_STATUSES",
    "Round203CaseCandidate",
    "Round203ScoreAdjustment",
    "render_round203_green_gate_review_markdown",
    "render_round203_price_backfill_plan_markdown",
    "render_round203_stage4b_4c_review_markdown",
    "render_round203_summary_markdown",
    "round203_audit_payload",
    "round203_case_records",
    "round203_case_rows",
    "round203_price_backfill_field_rows",
    "round203_score_adjustment_rows",
    "round203_summary",
    "round203_target_alias_rows",
    "write_round203_r12_loop7_reports",
]
