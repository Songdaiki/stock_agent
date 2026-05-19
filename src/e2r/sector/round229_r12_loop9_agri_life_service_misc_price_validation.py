"""Round-229 R12 Loop-9 agri/life-service/misc validation pack.

Round 229 converts ``docs/round/round_229.md`` into structured,
calibration-only case records. It does not change production scoring.

Easy example: a fried-chicken stock can jump 20-30% after a celebrity dinner.
That is an event premium, not Stage 3-Green, until store traffic, repeat demand,
franchise margin, and cash conversion are visible as of the case date.
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


ROUND229_SOURCE_ROUND_PATH = "docs/round/round_229.md"
ROUND229_RAW_LARGE_SECTOR_LABEL = "AGRI_LIFE_SERVICE_MISC"
ROUND229_LARGE_SECTOR = Round10LargeSector.EDUCATION_LIFE_AGRI_MISC
ROUND229_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round229_r12_loop9_agri_life_service_misc_price_validation"
ROUND229_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r12_loop9_round229.jsonl"
ROUND229_DEFAULT_AUDIT_PATH = "data/sector_taxonomy/round229_r12_loop9_agri_life_service_misc_price_validation_audit.json"
ROUND229_DEFAULT_STAGE3_BIAS = "conservative_except_recurring_service"

ROUND229_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "HOME_LIVING_APPLIANCE_RENTAL": E2RArchetype.HOME_LIVING_APPLIANCE_RENTAL.value,
    "CONSUMER_REGULATED_CASHFLOW": E2RArchetype.CONSUMER_REGULATED_PRODUCT.value,
    "AGRI_MACHINERY_EXPORT_CYCLE": E2RArchetype.AGRI_MACHINERY_EXPORT_CYCLE_KOREA.value,
    "AGRI_MACHINERY_SOFTWARE_LOCKIN": E2RArchetype.AGRI_MACHINERY_SOFTWARE_LOCKIN.value,
    "EDUCATION_POLICY_EVENT": E2RArchetype.EDUCATION_POLICY_EVENT.value,
    "HOME_CHILD_EDUCATION": E2RArchetype.HOME_CHILD_EDUCATION.value,
    "EDTECH_AI_DISRUPTION": E2RArchetype.EDTECH_AI_DISRUPTION.value,
    "CLASSROOM_DEVICE_REGULATION": E2RArchetype.EDTECH_AI_DISRUPTION_KOREA.value,
    "LIVESTOCK_DISEASE_PRICE_REGULATORY": E2RArchetype.LIVESTOCK_DISEASE_PRICE_REGULATORY.value,
    "FOOD_SERVICE_EVENT_PREMIUM": E2RArchetype.FOOD_SERVICE_EVENT_PREMIUM.value,
    "SMART_FARM_AGRI_TECH": E2RArchetype.SMART_FARM_AGRI_TECH.value,
    "VERTICAL_FARMING_UNIT_ECONOMICS": E2RArchetype.VERTICAL_FARMING_UNIT_ECONOMICS.value,
    "PRICE_ONLY_RALLY": E2RArchetype.PRICE_ONLY_RALLY.value,
    "EVENT_PREMIUM": E2RArchetype.EVENT_PREMIUM.value,
}

ROUND229_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "recurring_revenue_or_repeat_purchase_confirmed",
    "churn_or_retention_stable",
    "arpu_or_pricing_power_confirmed",
    "unit_economics_confirmed",
    "cash_conversion_visible",
    "inventory_or_receivables_stable",
    "regulatory_risk_passed",
    "subsidy_dependency_low",
    "price_path_after_evidence",
)

ROUND229_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "defensive_theme_only",
    "education_policy_only",
    "medical_quota_policy_only",
    "agri_export_theme_only",
    "smart_farm_policy_only",
    "smart_farm_technology_paper_only",
    "disease_event_only",
    "import_ban_event_only",
    "celebrity_food_event_only",
    "regulated_cashflow_without_growth",
    "dealer_inventory_unknown",
)

ROUND229_STAGE4B_WATCH_TRIGGERS: tuple[str, ...] = (
    "education_or_smart_farm_policy_rally_before_revenue",
    "bird_flu_import_ban_poultry_basket_rally",
    "celebrity_food_event_plus_20_to_30pct_without_sales",
    "defensive_dividend_frame_multiple_expansion_before_growth",
    "rental_multiple_expands_before_account_arpu_fcf",
    "medical_quota_policy_rally_before_student_conversion",
)

ROUND229_HARD_4C_GATES: tuple[str, ...] = (
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
    "celebrity_event_fade",
    "subsidy_withdrawal",
    "unit_economics_failure",
    "cash_conversion_deterioration",
)

ROUND229_PRICE_VALIDATION_FIELDS: tuple[str, ...] = (
    "price_data_source",
    "full_ohlc_available",
    "reported_price_anchor",
    "reported_return_anchor",
    "stage1_price",
    "stage2_price",
    "stage3_price",
    "stage4b_price",
    "stage4c_price",
    "mfe_1d",
    "mae_1d",
    "business_metric_anchor",
    "policy_metric_anchor",
    "technology_metric_anchor",
    "unit_economics_anchor",
    "price_validation_status",
)


@dataclass(frozen=True)
class Round229ScoreAdjustment:
    axis: str
    points: int
    direction: str
    reason: str

    def as_row(self) -> dict[str, str]:
        return {"axis": self.axis, "points": str(self.points), "direction": self.direction, "reason": self.reason}


@dataclass(frozen=True)
class Round229ShadowWeightRow:
    archetype: E2RArchetype
    recurring_revenue: int
    churn_stability: int
    arpu_or_repeat_purchase: int
    unit_economics: int
    cash_conversion: int
    inventory_quality: int
    regulatory_pass: int
    event_penalty: int
    watch_4b_sensitivity: int
    hard_4c_sensitivity: int
    notes: str

    def as_row(self) -> dict[str, str]:
        return {
            "archetype": self.archetype.value,
            "recurring_revenue": _signed(self.recurring_revenue),
            "churn_stability": _signed(self.churn_stability),
            "arpu_or_repeat_purchase": _signed(self.arpu_or_repeat_purchase),
            "unit_economics": _signed(self.unit_economics),
            "cash_conversion": _signed(self.cash_conversion),
            "inventory_quality": _signed(self.inventory_quality),
            "regulatory_pass": _signed(self.regulatory_pass),
            "event_penalty": _signed(self.event_penalty),
            "4b_watch_sensitivity": _signed(self.watch_4b_sensitivity),
            "hard_4c_sensitivity": _signed(self.hard_4c_sensitivity),
            "notes": self.notes,
        }


@dataclass(frozen=True)
class Round229DeepSubArchetype:
    category: str
    primary_archetype: E2RArchetype
    terms: tuple[str, ...]

    def as_row(self) -> dict[str, str]:
        return {"category": self.category, "primary_archetype": self.primary_archetype.value, "terms": "|".join(self.terms)}


@dataclass(frozen=True)
class Round229CaseCandidate:
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
    price_data_source: str
    reported_price_anchor: str
    reported_return_anchor: str
    mfe_1d: float | None
    mae_1d: float | None
    stage1_price_anchor: float | None
    stage2_price_anchor: float | None
    stage3_price_anchor: float | None
    stage4b_price_anchor: float | None
    stage4c_price_anchor: float | None
    extra_price_metrics: Mapping[str, float | str | bool]
    score_price_alignment: str
    round_alignment_label: str
    rerating_result: str
    round_rerating_label: str
    stage_failure_type: str
    round_stage_failure_label: str
    price_validation_status: str
    notes: str

    @property
    def large_sector(self) -> str:
        return ROUND229_LARGE_SECTOR.value

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND229_SCORE_ADJUSTMENTS: tuple[Round229ScoreAdjustment, ...] = (
    Round229ScoreAdjustment("recurring_revenue", 5, "raise", "렌탈·구독·반복구매는 R12에서 가장 중요한 구조 증거다."),
    Round229ScoreAdjustment("churn_stability", 5, "raise", "반복매출도 churn이 올라가면 구조성이 약해진다."),
    Round229ScoreAdjustment("ARPU_or_repeat_purchase", 4, "raise", "가격전가 또는 반복구매가 확인되어야 한다."),
    Round229ScoreAdjustment("cash_conversion", 5, "raise", "매출이 현금흐름으로 전환되어야 Stage 3 검토가 가능하다."),
    Round229ScoreAdjustment("unit_economics", 5, "raise", "스마트팜·교육·외식은 unit economics 확인이 핵심이다."),
    Round229ScoreAdjustment("commercial_installation", 4, "raise", "스마트팜 기술은 상업 설치와 유지보수 매출 전까지 Stage 1이다."),
    Round229ScoreAdjustment("service_contract_visibility", 4, "raise", "서비스 계약과 유지보수 가시성은 반복매출 품질을 높인다."),
    Round229ScoreAdjustment("dealer_sell_through", 4, "raise", "농기계 export narrative는 딜러 판매와 재고가 확인되어야 한다."),
    Round229ScoreAdjustment("inventory_quality", 4, "raise", "재고·매출채권 안정은 R12 Green 가드레일이다."),
    Round229ScoreAdjustment("regulatory_pass", 4, "raise", "규제소비재·교육·식품은 규제 통과 여부가 중요하다."),
    Round229ScoreAdjustment("pricing_power_after_input_cost", 4, "raise", "원가 상승 이후 가격전가가 확인되어야 한다."),
    Round229ScoreAdjustment("defensive_theme_only", -5, "lower", "방어주라는 말만으로는 Green이 아니다."),
    Round229ScoreAdjustment("education_policy_only", -5, "lower", "의대정원 같은 정책은 수강생·ARPU·OPM 전까지 event premium이다."),
    Round229ScoreAdjustment("agri_cycle_only", -4, "lower", "농기계 export cycle은 재고와 financing이 빠지면 제한한다."),
    Round229ScoreAdjustment("smart_farm_policy_only", -5, "lower", "스마트팜 정책/논문은 매출·마진 전까지 Green 금지다."),
    Round229ScoreAdjustment("disease_event_only", -5, "lower", "질병 이벤트는 수입제한 완화 시 fade될 수 있다."),
    Round229ScoreAdjustment("celebrity_food_event_only", -5, "lower", "바이럴 외식 이벤트는 매출 증거 전까지 price_moved_without_evidence다."),
    Round229ScoreAdjustment("import_ban_event_only", -4, "lower", "수입금지 뉴스만으로 poultry basket을 구조로 보지 않는다."),
    Round229ScoreAdjustment("unconfirmed_export_theme", -3, "lower", "수출 테마는 sell-through와 마진 전까지 제한한다."),
    Round229ScoreAdjustment("dealer_inventory_unknown", -4, "lower", "농기계 딜러 재고 미확인은 4C-watch 입력이다."),
    Round229ScoreAdjustment("subsidy_dependent_unit_economics", -4, "lower", "보조금 의존 unit economics는 Green을 막는다."),
    Round229ScoreAdjustment("regulated_product_without_growth", -3, "lower", "규제소비재도 성장·환원·FCF 없이는 제한한다."),
)


ROUND229_SHADOW_WEIGHT_ROWS: tuple[Round229ShadowWeightRow, ...] = (
    Round229ShadowWeightRow(E2RArchetype.HOME_LIVING_APPLIANCE_RENTAL, 5, 5, 4, 5, 5, 4, 3, -1, 3, 4, "Coway recurring rental can be Stage 3 candidate but needs accounts/churn/FCF/OHLC."),
    Round229ShadowWeightRow(E2RArchetype.CONSUMER_REGULATED_PRODUCT, 4, 2, 3, 4, 5, 3, 5, -2, 3, 4, "KT&G regulated cashflow is candidate but growth/shareholder return/regulatory risk must be verified."),
    Round229ShadowWeightRow(E2RArchetype.AGRI_MACHINERY_EXPORT_CYCLE_KOREA, 2, 0, 1, 5, 4, 5, 2, -3, 4, 4, "Daedong/TYM export story needs dealer sell-through, inventory and financing."),
    Round229ShadowWeightRow(E2RArchetype.EDUCATION_POLICY_EVENT, 3, 2, 5, 4, 5, 1, 4, -5, 5, 4, "Medical quota policy is event unless repeat course, ARPU, and OPM confirm."),
    Round229ShadowWeightRow(E2RArchetype.EDTECH_AI_DISRUPTION_KOREA, 2, 2, 3, 4, 4, 1, 5, -4, 4, 4, "Phone ban creates policy friction for edtech; company revenue impact required."),
    Round229ShadowWeightRow(E2RArchetype.LIVESTOCK_DISEASE_PRICE_REGULATORY, 1, 0, 2, 3, 3, 5, 4, -5, 5, 5, "Bird flu import restriction is one-off; easing or free-status recognition is event fade."),
    Round229ShadowWeightRow(E2RArchetype.FOOD_SERVICE_EVENT_PREMIUM, 2, 0, 3, 4, 4, 3, 2, -5, 5, 3, "Celebrity chicken event is price_moved_without_evidence until traffic/margin confirm."),
    Round229ShadowWeightRow(E2RArchetype.SMART_FARM_AGRI_TECH, 2, 0, 1, 5, 5, 3, 4, -5, 5, 5, "Smart farm tech needs commercial installation, service revenue and subsidy-independent unit economics."),
)


ROUND229_DEEP_SUB_ARCHETYPES: tuple[Round229DeepSubArchetype, ...] = (
    Round229DeepSubArchetype("생활 렌탈", E2RArchetype.HOME_LIVING_APPLIANCE_RENTAL, ("Coway", "water purifier", "air purifier", "bidet", "mattress rental", "Malaysia account growth", "churn", "ARPU", "service network")),
    Round229DeepSubArchetype("규제소비재", E2RArchetype.CONSUMER_REGULATED_PRODUCT, ("KT&G", "tobacco", "HNB", "ginseng", "regulated cashflow", "dividend", "buyback", "volume decline", "tax regulation")),
    Round229DeepSubArchetype("농기계", E2RArchetype.AGRI_MACHINERY_EXPORT_CYCLE_KOREA, ("Daedong", "KIOTI", "TYM", "North America tractor channel", "dealer sell-through", "farmer financing", "inventory", "autonomous tractor")),
    Round229DeepSubArchetype("교육", E2RArchetype.EDUCATION_POLICY_EVENT, ("MegaStudy Education", "medical school quota", "repeat course", "ARPU", "OPM", "birth-rate demand risk")),
    Round229DeepSubArchetype("교육 디지털 규제", E2RArchetype.EDTECH_AI_DISRUPTION_KOREA, ("classroom phone ban", "digital device regulation", "edtech friction", "AI education disruption", "student device exception")),
    Round229DeepSubArchetype("축산·질병", E2RArchetype.LIVESTOCK_DISEASE_PRICE_REGULATORY, ("Harim", "Maniker", "poultry basket", "Brazil bird flu", "import restriction", "restriction easing", "feed cost")),
    Round229DeepSubArchetype("생활서비스·외식", E2RArchetype.FOOD_SERVICE_EVENT_PREMIUM, ("Kyochon F&B", "Cherrybro", "Neuromeka", "Jensen Huang chicken event", "celebrity food event", "traffic", "same-store sales")),
    Round229DeepSubArchetype("스마트팜", E2RArchetype.SMART_FARM_AGRI_TECH, ("Green Plus", "Woomdungi Farm", "greenhouse automation", "UAV yield estimation", "government subsidy", "unit economics", "maintenance revenue")),
)


ROUND229_CASE_CANDIDATES: tuple[Round229CaseCandidate, ...] = (
    Round229CaseCandidate(
        case_id="r12_loop9_coway_recurring_rental_watch",
        symbol="021240",
        company_name="코웨이",
        primary_archetype=E2RArchetype.HOME_LIVING_APPLIANCE_RENTAL,
        secondary_archetypes=(E2RArchetype.EVENT_PREMIUM,),
        case_type="success_candidate",
        stage1_date=date(2022, 1, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="recurring_rental_service_can_be_green_candidate_only_after_accounts_churn_arpu_fcf_and_price_path_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("water_purifier_air_purifier_bidet_mattress_rental", "overseas_subsidiaries_present", "recurring_account_base_candidate"),
        red_flag_fields=("rental_accounts_unverified", "churn_unverified", "arpu_unverified", "fcf_unverified", "product_safety_recall_watch", "governance_capital_allocation_watch"),
        price_data_source="public company profile only",
        reported_price_anchor="price_data_unavailable_after_deep_search",
        reported_return_anchor="business model anchor only; no event-day OHLC",
        mfe_1d=None,
        mae_1d=None,
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"business_anchor": "water purifier / air purifier / bidet / mattress rental recurring model", "overseas_subsidiaries": "Malaysia|United States|Thailand|Indonesia|Vietnam|Europe|Japan|China"},
        score_price_alignment="unknown",
        round_alignment_label="success_candidate",
        rerating_result="unknown",
        round_rerating_label="recurring_service_rerating_candidate",
        stage_failure_type="stage2_watch_success",
        round_stage_failure_label="stage2_watch_success_candidate",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="R12에서 가장 구조적인 recurring-service 후보지만 rental accounts, churn, ARPU, OPM/FCF, OHLC 확인 전 Stage 3는 보류한다.",
    ),
    Round229CaseCandidate(
        case_id="r12_loop9_ktng_regulated_cashflow_watch",
        symbol="033780",
        company_name="KT&G",
        primary_archetype=E2RArchetype.CONSUMER_REGULATED_PRODUCT,
        secondary_archetypes=(E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN,),
        case_type="success_candidate",
        stage1_date=date(2024, 1, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="regulated_cashflow_is_not_green_until_shareholder_return_hnb_growth_volume_defense_fcf_and_regulatory_risk_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("tobacco_hnb_ginseng_cashflow", "defensive_dividend_candidate", "revenue_2024_about_5_9tn_krw"),
        red_flag_fields=("buyback_cancellation_unverified", "hnb_growth_unverified", "volume_decline_watch", "tax_regulation_watch", "ginseng_demand_watch"),
        price_data_source="public company profile evidence only",
        reported_price_anchor="price_data_unavailable_after_deep_search",
        reported_return_anchor="2024 revenue about 5.9T KRW, source confidence medium_low",
        mfe_1d=None,
        mae_1d=None,
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"revenue_2024_krw_trn": 5.9, "source_confidence": "medium_low", "business_anchor": "tobacco + ginseng + regulated consumer cashflow"},
        score_price_alignment="unknown",
        round_alignment_label="success_candidate",
        rerating_result="unknown",
        round_rerating_label="regulated_cashflow_watch",
        stage_failure_type="stage2_watch_success",
        round_stage_failure_label="stage2_watch_success_candidate",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Regulated cashflow 후보지만 주주환원·HNB 성장·volume decline·규제 리스크와 OHLC 확인 전 Green 금지다.",
    ),
    Round229CaseCandidate(
        case_id="r12_loop9_daedong_tym_agri_machinery_watch",
        symbol="000490/002900",
        company_name="대동/TYM",
        primary_archetype=E2RArchetype.AGRI_MACHINERY_EXPORT_CYCLE_KOREA,
        secondary_archetypes=(E2RArchetype.AGRI_MACHINERY_SOFTWARE_LOCKIN,),
        case_type="success_candidate",
        stage1_date=date(2023, 1, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="agri_machinery_export_theme_is_not_green_until_dealer_sell_through_inventory_farmer_financing_opm_and_fcf_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("kioti_brand_north_america_channel", "tractor_combine_utv_engine_business", "autonomous_tractor_precision_agriculture_narrative"),
        red_flag_fields=("dealer_sell_through_unverified", "dealer_inventory_unknown", "farmer_financing_unknown", "opm_fcf_unverified", "agri_cycle_only"),
        price_data_source="public company profile evidence only",
        reported_price_anchor="price_data_unavailable_after_deep_search",
        reported_return_anchor="business profile anchor only; no event-day OHLC",
        mfe_1d=None,
        mae_1d=None,
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"business_anchor": "Daedong KIOTI / tractors / combines / UTV / engines; TYM agri machinery export channel"},
        score_price_alignment="unknown",
        round_alignment_label="unknown_insufficient_evidence",
        rerating_result="unknown",
        round_rerating_label="agri_machinery_watch",
        stage_failure_type="unknown",
        round_stage_failure_label="stage1_attention_only",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="농기계 export와 자율주행 농기계 narrative는 dealer sell-through, inventory, farmer financing, OPM 전 Green 금지다.",
    ),
    Round229CaseCandidate(
        case_id="r12_loop9_megastudy_medical_quota_policy",
        symbol="215200",
        company_name="메가스터디교육/교육주",
        primary_archetype=E2RArchetype.EDUCATION_POLICY_EVENT,
        secondary_archetypes=(E2RArchetype.HOME_CHILD_EDUCATION, E2RArchetype.EVENT_PREMIUM),
        case_type="event_premium",
        stage1_date=date(2024, 2, 1),
        stage2_date=date(2026, 2, 1),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="medical_quota_policy_is_stage1_or_stage2_until_students_arpu_opm_and_cash_conversion_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("medical_school_quota_policy", "quota_3058_to_3548_in_2027", "quota_3871_by_2031"),
        red_flag_fields=("education_policy_only", "student_conversion_unverified", "arpu_unverified", "opm_unverified", "birth_rate_demand_collapse_watch", "private_education_regulation_watch"),
        price_data_source="AP policy evidence",
        reported_price_anchor="price_data_unavailable_after_deep_search",
        reported_return_anchor="medical quota +16.0% in 2027 and +26.6% by 2031 vs original 3,058",
        mfe_1d=None,
        mae_1d=None,
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"original_quota": 3058.0, "quota_2027": 3548.0, "quota_increase_2027": 490.0, "quota_increase_2027_pct": 16.0, "quota_2031": 3871.0, "quota_increase_2031_vs_original": 813.0, "quota_increase_2031_pct": 26.6},
        score_price_alignment="unknown",
        round_alignment_label="event_premium",
        rerating_result="event_premium",
        round_rerating_label="education_policy_watch",
        stage_failure_type="false_yellow",
        round_stage_failure_label="stage1_or_stage2_attention_only",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="의대정원 정책은 routing signal이다. 실제 수강생·ARPU·OPM 전 Stage 3가 아니다.",
    ),
    Round229CaseCandidate(
        case_id="r12_loop9_edtech_phone_ban_policy_watch",
        symbol="education_edtech_basket",
        company_name="교육/에듀테크 basket",
        primary_archetype=E2RArchetype.EDTECH_AI_DISRUPTION_KOREA,
        secondary_archetypes=(E2RArchetype.EDTECH_AI_DISRUPTION, E2RArchetype.EVENT_PREMIUM),
        case_type="failed_rerating",
        stage1_date=date(2025, 8, 27),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2026, 3, 1),
        stage3_decision="classroom_phone_ban_is_policy_friction_until_company_revenue_impact_is_confirmed",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("classroom_phone_device_ban_law", "law_effective_2026_03", "student_social_media_impact_survey"),
        red_flag_fields=("classroom_device_regulation", "digital_learning_platform_friction", "company_revenue_impact_unverified", "education_policy_only"),
        price_data_source="Reuters policy evidence",
        reported_price_anchor="price_data_unavailable_after_deep_search",
        reported_return_anchor="37% daily-life impact survey; 22% anxiety without social media; effective 2026-03",
        mfe_1d=None,
        mae_1d=None,
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"law_effective_date": "2026-03", "social_media_daily_life_impact_pct": 37.0, "anxiety_without_social_media_pct": 22.0, "digital_device_exception": "disability_or_educational_purpose"},
        score_price_alignment="unknown",
        round_alignment_label="policy_watch",
        rerating_result="no_rerating",
        round_rerating_label="education_regulation_watch",
        stage_failure_type="should_have_been_red",
        round_stage_failure_label="stage1_attention_only",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="교실 휴대전화 금지법은 오프라인 discipline에는 우호적일 수 있지만 디지털 학습 플랫폼에는 friction이다.",
    ),
    Round229CaseCandidate(
        case_id="r12_loop9_poultry_bird_flu_import_event",
        symbol="Harim/Maniker/Cherrybro_basket",
        company_name="poultry basket",
        primary_archetype=E2RArchetype.LIVESTOCK_DISEASE_PRICE_REGULATORY,
        secondary_archetypes=(E2RArchetype.EVENT_PREMIUM,),
        case_type="event_premium",
        stage1_date=date(2025, 5, 19),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 6, 23),
        stage3_decision="bird_flu_import_restriction_is_one_off_until_domestic_price_volume_opm_and_duration_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("brazil_bird_flu_import_restriction", "brazil_2024_poultry_exports_over_5m_tons", "restriction_easing_or_free_status_recognition"),
        red_flag_fields=("disease_event_only", "import_ban_event_only", "disease_event_cleared", "restriction_easing_event_fade", "feed_cost_watch"),
        price_data_source="Reuters import restriction / bird-flu-free evidence",
        reported_price_anchor="price_data_unavailable_after_deep_search",
        reported_return_anchor="Brazil poultry exports >5M tons; EU share 4.4%; restrictions later eased/free-status recognition",
        mfe_1d=None,
        mae_1d=None,
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"brazil_2024_poultry_exports_mn_tons": 5.0, "eu_share_of_brazil_exports_pct": 4.4, "event_type": "Brazil commercial farm bird flu import restriction followed by easing/free-status recognition"},
        score_price_alignment="unknown",
        round_alignment_label="event_premium",
        rerating_result="event_premium",
        round_rerating_label="one_off_disease_event",
        stage_failure_type="false_yellow",
        round_stage_failure_label="should_have_been_stage1_or_4b_watch",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="질병 이벤트는 one-off다. 수입제한 완화나 bird-flu-free recognition이 event fade trigger다.",
    ),
    Round229CaseCandidate(
        case_id="r12_loop9_kyochon_jensen_chicken_event",
        symbol="Kyochon/Cherrybro/Neuromeka_basket",
        company_name="fried chicken event basket",
        primary_archetype=E2RArchetype.FOOD_SERVICE_EVENT_PREMIUM,
        secondary_archetypes=(E2RArchetype.PRICE_ONLY_RALLY, E2RArchetype.EVENT_PREMIUM),
        case_type="overheat",
        stage1_date=date(2025, 10, 31),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=date(2025, 10, 31),
        stage4c_date=None,
        stage3_decision="celebrity_food_event_is_price_moved_without_evidence_until_sales_margin_and_repeat_demand_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("jensen_huang_chicken_dinner_viral_event", "fried_chicken_related_stocks_intraday_plus_20_to_30pct"),
        red_flag_fields=("celebrity_food_event_only", "fundamental_revenue_evidence_not_confirmed", "price_moved_before_evidence", "viral_fade_watch", "franchise_margin_unverified"),
        price_data_source="MarketWatch / Tom's Hardware event-return summary",
        reported_price_anchor="fried chicken related stocks intraday +20% to +30%",
        reported_return_anchor="reported event MFE midpoint +25%; no full OHLC or 30D/90D path",
        mfe_1d=25.0,
        mae_1d=None,
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"reported_event_mfe_range_pct": "20-30", "reported_event_mfe_midpoint_pct": 25.0, "fundamental_revenue_evidence_confirmed": False, "related_names": "Kyochon F&B|Cherrybro|Neuromeka"},
        score_price_alignment="price_moved_without_evidence",
        round_alignment_label="price_moved_without_evidence",
        rerating_result="event_premium",
        round_rerating_label="celebrity_food_event_premium",
        stage_failure_type="false_yellow",
        round_stage_failure_label="should_have_been_stage1_or_4b_watch",
        price_validation_status="reported_event_return_range_not_full_ohlc",
        notes="Jensen Huang 치킨 이벤트는 매출·마진 증거가 아니라 celebrity/viral event premium이다.",
    ),
    Round229CaseCandidate(
        case_id="r12_loop9_smart_farm_unit_economics_watch",
        symbol="GreenPlus/WoomdungiFarm_basket",
        company_name="스마트팜 basket",
        primary_archetype=E2RArchetype.SMART_FARM_AGRI_TECH,
        secondary_archetypes=(E2RArchetype.VERTICAL_FARMING_UNIT_ECONOMICS, E2RArchetype.EVENT_PREMIUM),
        case_type="event_premium",
        stage1_date=date(2024, 1, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="smart_farm_policy_or_technology_is_stage1_until_commercial_installation_service_revenue_unit_economics_and_fcf_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("smart_farm_adoption_barriers", "greenhouse_uav_counting_accuracy_94_4pct", "uav_weight_estimation_accuracy_87_5pct"),
        red_flag_fields=("smart_farm_policy_only", "smart_farm_technology_paper_only", "commercial_installation_unverified", "maintenance_revenue_unverified", "subsidy_dependent_unit_economics", "unit_economics_failure_watch"),
        price_data_source="arXiv smart-farm adoption / greenhouse UAV evidence",
        reported_price_anchor="price_data_unavailable_after_deep_search",
        reported_return_anchor="UAV counting accuracy 94.4%, weight estimation 87.5%, but no listed-company revenue proof",
        mfe_1d=None,
        mae_1d=None,
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"uav_counting_accuracy_pct": 94.4, "uav_weight_estimation_accuracy_pct": 87.5, "flight_distance_m": 13.2, "flight_time_sec": 10.5, "adoption_barriers": "farmer_age|education|land_size|government_support|technical_hurdles|financial_constraints"},
        score_price_alignment="unknown",
        round_alignment_label="unknown_insufficient_evidence",
        rerating_result="event_premium",
        round_rerating_label="smart_farm_policy_tech_watch",
        stage_failure_type="false_yellow",
        round_stage_failure_label="stage1_attention_only",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="스마트팜은 장기 테마지만 commercial installation·unit economics·반복서비스 전 Green 금지다.",
    ),
)


def round229_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND229_CASE_CANDIDATES:
        stage3_terms = ("churn", "arpu", "fcf", "cash", "unit", "revenue", "opm", "margin", "repeat")
        record = E2RCaseRecord(
            case_id=candidate.case_id,
            symbol=candidate.symbol,
            company_name=candidate.company_name,
            market="KR",
            sector_raw=candidate.primary_archetype.value,
            primary_archetype=candidate.primary_archetype,
            secondary_archetypes=candidate.secondary_archetypes,
            expected_group=candidate.expected_group,
            large_sector=candidate.large_sector,
            case_type=candidate.case_type,
            stage1_date=candidate.stage1_date,
            stage2_date=candidate.stage2_date,
            stage3_date=candidate.stage3_date,
            stage4b_date=candidate.stage4b_date,
            stage4c_date=candidate.stage4c_date,
            evidence_summary=(
                "Round229 R12 Loop-9 agri/life-service/misc price validation case. "
                "Calibration-only; not production scoring input."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=candidate.evidence_fields if candidate.stage2_date else (),
            stage3_evidence=tuple(field for field in candidate.evidence_fields if any(term in field for term in stage3_terms)),
            stage4b_evidence=tuple(
                field
                for field in (*candidate.evidence_fields, *candidate.red_flag_fields)
                if "price" in field or "mfe" in field or "event" in field or "rally" in field or "viral" in field
            ),
            stage4c_evidence=tuple(
                field
                for field in candidate.red_flag_fields
                if "watch" in field
                or "failure" in field
                or "decline" in field
                or "fade" in field
                or "regulation" in field
                or "churn" in field
                or "inventory" in field
            ),
            must_have_fields=ROUND229_GREEN_REQUIRED_FIELDS,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason=(
                "; ".join(candidate.red_flag_fields)
                if candidate.case_type in {"event_premium", "overheat", "failed_rerating", "4c_thesis_break"}
                else None
            ),
            score_price_alignment=candidate.score_price_alignment,
            rerating_result=candidate.rerating_result,
            stage_failure_type=candidate.stage_failure_type,
            price_pattern=candidate.stage3_decision,
            score_weight_hint={f"{item.axis}_delta": float(item.points) for item in ROUND229_SCORE_ADJUSTMENTS},
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "full_ohlc_complete_false",
                "r12_default_stage3_bias_conservative_except_recurring_service",
                "price_validation_partial_with_reported_price_anchors",
                "do_not_invent_price_or_stage_dates",
                "do_not_treat_policy_disease_celebrity_or_smart_farm_theme_as_green_alone",
                *ROUND229_GREEN_REQUIRED_FIELDS,
                *ROUND229_GREEN_FORBIDDEN_PATTERNS,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(
                stage1_price=candidate.stage1_price_anchor,
                stage2_price=candidate.stage2_price_anchor,
                stage3_price=candidate.stage3_price_anchor,
                stage4b_price=candidate.stage4b_price_anchor,
                stage4c_price=candidate.stage4c_price_anchor,
                mfe_30d=candidate.mfe_1d,
                mae_30d=candidate.mae_1d,
                price_validation_status=candidate.price_validation_status,
            ),
            data_quality=CaseDataQuality(
                official_data_available=True,
                report_data_available=True,
                price_data_available=candidate.stage1_price_anchor is not None
                or candidate.stage2_price_anchor is not None
                or candidate.mfe_1d is not None
                or candidate.mae_1d is not None,
                stage_dates_confidence=0.75 if candidate.stage1_date or candidate.stage2_date or candidate.stage4c_date else 0.6,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round229_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND229_CASE_CANDIDATES:
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
                "price_data_source": candidate.price_data_source,
                "reported_price_anchor": candidate.reported_price_anchor,
                "reported_return_anchor": candidate.reported_return_anchor,
                "mfe_1d": _float_text(candidate.mfe_1d),
                "mae_1d": _float_text(candidate.mae_1d),
                "stage1_price_anchor": _float_text(candidate.stage1_price_anchor),
                "extra_price_metrics": json.dumps(candidate.extra_price_metrics, ensure_ascii=False, sort_keys=True),
                "score_price_alignment": candidate.score_price_alignment,
                "round_alignment_label": candidate.round_alignment_label,
                "rerating_result": candidate.rerating_result,
                "round_rerating_label": candidate.round_rerating_label,
                "stage_failure_type": candidate.stage_failure_type,
                "round_stage_failure_label": candidate.round_stage_failure_label,
                "price_validation_status": candidate.price_validation_status,
                "evidence_fields": "|".join(candidate.evidence_fields),
                "red_flag_fields": "|".join(candidate.red_flag_fields),
                "notes": candidate.notes,
            }
        )
    return tuple(rows)


def round229_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND229_SCORE_ADJUSTMENTS)


def round229_shadow_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(row.as_row() for row in ROUND229_SHADOW_WEIGHT_ROWS)


def round229_deep_sub_archetype_rows() -> tuple[dict[str, str], ...]:
    return tuple(row.as_row() for row in ROUND229_DEEP_SUB_ARCHETYPES)


def round229_price_validation_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round229_price_validation": "true"} for field in ROUND229_PRICE_VALIDATION_FIELDS)


def round229_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple({"round229_label": label, "canonical_archetype": canonical} for label, canonical in ROUND229_REQUIRED_TARGET_ALIASES.items())


def round229_summary() -> dict[str, int | bool | str]:
    cases = ROUND229_CASE_CANDIDATES
    return {
        "source_round": ROUND229_SOURCE_ROUND_PATH,
        "raw_large_sector_label": ROUND229_RAW_LARGE_SECTOR_LABEL,
        "large_sector": ROUND229_LARGE_SECTOR.value,
        "case_candidate_count": len(cases),
        "success_candidate_count": sum(1 for case in cases if case.case_type == "success_candidate"),
        "event_premium_count": sum(1 for case in cases if case.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for case in cases if case.case_type == "failed_rerating"),
        "overheat_count": sum(1 for case in cases if case.case_type == "overheat"),
        "price_moved_without_evidence_count": sum(1 for case in cases if case.score_price_alignment == "price_moved_without_evidence"),
        "stage3_case_count": sum(1 for case in cases if case.stage3_date is not None),
        "stage4b_watch_count": sum(1 for case in cases if case.stage4b_status == "watch"),
        "hard_4c_case_count": sum(1 for case in cases if case.hard_4c_confirmed),
        "target_archetype_count": len(ROUND229_REQUIRED_TARGET_ALIASES),
        "deep_sub_archetype_count": len(ROUND229_DEEP_SUB_ARCHETYPES),
        "shadow_weight_row_count": len(ROUND229_SHADOW_WEIGHT_ROWS),
        "price_validation_completed": "partial_with_reported_price_anchors",
        "full_ohlc_complete": False,
        "r12_default_stage3_bias": ROUND229_DEFAULT_STAGE3_BIAS,
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
    }


def round229_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND229_SOURCE_ROUND_PATH,
        "raw_large_sector_label": ROUND229_RAW_LARGE_SECTOR_LABEL,
        "large_sector": ROUND229_LARGE_SECTOR.value,
        "summary": round229_summary(),
        "target_aliases": dict(ROUND229_REQUIRED_TARGET_ALIASES),
        "green_required_fields": list(ROUND229_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND229_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_watch_triggers": list(ROUND229_STAGE4B_WATCH_TRIGGERS),
        "hard_4c_gates": list(ROUND229_HARD_4C_GATES),
        "deep_sub_archetypes": round229_deep_sub_archetype_rows(),
        "shadow_weights": round229_shadow_weight_rows(),
        "what_not_to_change": [
            "do_not_use_round229_cases_as_candidate_generation_input",
            "do_not_apply_shadow_weights_to_production_scoring_yet",
            "do_not_treat_education_policy_disease_event_smart_farm_theme_or_celebrity_food_event_as_green",
            "do_not_invent_ohlc_or_stage_dates",
        ],
    }


def render_round229_summary_markdown() -> str:
    summary = round229_summary()
    lines = [
        "# Round 229 R12 Loop 9 Agri Life Service Misc Price Validation",
        "",
        "This pack is calibration-only. Production scoring and candidate generation are unchanged.",
        "",
        "## Summary",
        "",
        f"- source_round: {summary['source_round']}",
        f"- raw_large_sector_label: {summary['raw_large_sector_label']}",
        f"- mapped_large_sector: {summary['large_sector']}",
        f"- cases: {summary['case_candidate_count']}",
        f"- success_candidate: {summary['success_candidate_count']}",
        f"- event_premium: {summary['event_premium_count']}",
        f"- failed_rerating: {summary['failed_rerating_count']}",
        f"- overheat: {summary['overheat_count']}",
        f"- price_moved_without_evidence: {summary['price_moved_without_evidence_count']}",
        f"- Stage 3 dated cases: {summary['stage3_case_count']}",
        f"- 4B-watch cases: {summary['stage4b_watch_count']}",
        f"- hard_4c_case_count: {summary['hard_4c_case_count']}",
        f"- deep_sub_archetype_count: {summary['deep_sub_archetype_count']}",
        f"- shadow_weight_row_count: {summary['shadow_weight_row_count']}",
        f"- r12_default_stage3_bias: {summary['r12_default_stage3_bias']}",
        f"- full_ohlc_complete: {str(summary['full_ohlc_complete']).lower()}",
        "",
        "## Case Matrix",
        "",
        "| case | company | type | stage2 | stage3 | 4B | 4C | round alignment | note |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for case in ROUND229_CASE_CANDIDATES:
        lines.append(
            "| "
            + " | ".join(
                (
                    case.case_id,
                    case.company_name,
                    case.case_type,
                    _date_text(case.stage2_date),
                    _date_text(case.stage3_date),
                    _date_text(case.stage4b_date),
                    _date_text(case.stage4c_date),
                    case.round_alignment_label,
                    case.notes,
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "- R12 default is Stage 1/2 watch or event premium, except recurring-service evidence can become a stronger candidate.",
            "- Coway and KT&G remain structural candidates, but accounts, churn, ARPU, FCF, shareholder return, and regulation must be verified.",
            "- Daedong/TYM needs dealer sell-through, inventory, farmer financing, OPM, and FCF.",
            "- Medical-quota and classroom-device policy are routing signals, not company Green evidence.",
            "- Poultry disease and Jensen chicken events are one-off/event-premium examples.",
            "- Smart-farm technology metrics are not company revenue or unit-economics evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round229_green_gate_review_markdown() -> str:
    lines = [
        "# Round 229 R12 Green Gate Review",
        "",
        "Do not apply these weights to production scoring yet.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND229_GREEN_REQUIRED_FIELDS)
    lines.extend(["", "## Forbidden Patterns", ""])
    lines.extend(f"- {field}" for field in ROUND229_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(
        [
            "",
            "## Easy Example",
            "- `의대정원 확대 + 교육주 기대` is Stage 1/2 event routing.",
            "- `실제 수강생 증가 + ARPU + OPM + cash conversion` is the evidence bundle required for deeper Stage review.",
            "- `치킨 이벤트 +20-30%` is 4B-watch/event premium until repeat demand and margin prove otherwise.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round229_stage4b_4c_review_markdown() -> str:
    lines = ["# Round 229 R12 4B/4C Review", "", "## 4B Watch Triggers", ""]
    lines.extend(f"- {field}" for field in ROUND229_STAGE4B_WATCH_TRIGGERS)
    lines.extend(["", "## Hard 4C Gates", ""])
    lines.extend(f"- {field}" for field in ROUND229_HARD_4C_GATES)
    lines.extend(
        [
            "",
            "## Plain-Language Gate Notes",
            "",
            "- Recurring service candidates need churn, ARPU, FCF, and price path after evidence.",
            "- Disease and celebrity events can move prices before evidence; keep them in 4B-watch/event premium.",
            "- Smart-farm technical accuracy is not enough without commercial installation and unit economics.",
        ]
    )
    lines.extend(["", "## Case Notes", ""])
    for case in ROUND229_CASE_CANDIDATES:
        if case.stage4b_status == "watch" or case.red_flag_fields:
            lines.append(f"- {case.case_id}: {', '.join(case.red_flag_fields)}")
    return "\n".join(lines) + "\n"


def render_round229_price_validation_plan_markdown() -> str:
    lines = [
        "# Round 229 R12 Price Validation Plan",
        "",
        "- price_validation_completed: partial_with_reported_price_anchors",
        "- full_ohlc_complete: false",
        "- r12_default_stage3_bias: conservative_except_recurring_service",
        "- Do not invent OHLC, peak, MFE, or MAE where raw adjusted daily prices are unavailable.",
        "",
        "## Backfill Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND229_PRICE_VALIDATION_FIELDS)
    return "\n".join(lines) + "\n"


def write_round229_r12_loop9_reports(
    output_directory: str | Path = ROUND229_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND229_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND229_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "cases": write_case_library(round229_case_records(), cases_path),
        "audit": _write_json(round229_audit_payload(), audit_path),
        "summary": output / "round229_r12_loop9_price_validation_summary.md",
        "case_matrix": output / "round229_r12_loop9_case_matrix.csv",
        "target_aliases": output / "round229_r12_loop9_target_aliases.csv",
        "score_adjustments": output / "round229_r12_loop9_score_adjustments.csv",
        "shadow_weights": output / "round229_r12_loop9_shadow_weights.csv",
        "deep_sub_archetypes": output / "round229_r12_loop9_deep_sub_archetypes.csv",
        "price_validation_fields": output / "round229_r12_loop9_price_validation_fields.csv",
        "green_gate_review": output / "round229_r12_loop9_green_gate_review.md",
        "price_validation_plan": output / "round229_r12_loop9_price_validation_plan.md",
        "stage4b_4c_review": output / "round229_r12_loop9_stage4b_4c_review.md",
    }
    paths["summary"].write_text(render_round229_summary_markdown(), encoding="utf-8")
    _write_csv(round229_case_rows(), paths["case_matrix"])
    _write_csv(round229_target_alias_rows(), paths["target_aliases"])
    _write_csv(round229_score_adjustment_rows(), paths["score_adjustments"])
    _write_csv(round229_shadow_weight_rows(), paths["shadow_weights"])
    _write_csv(round229_deep_sub_archetype_rows(), paths["deep_sub_archetypes"])
    _write_csv(round229_price_validation_field_rows(), paths["price_validation_fields"])
    paths["green_gate_review"].write_text(render_round229_green_gate_review_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round229_price_validation_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round229_stage4b_4c_review_markdown(), encoding="utf-8")
    return paths


def _write_json(payload: object, path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def _write_csv(rows: Iterable[dict[str, str]], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    rows = tuple(rows)
    if not rows:
        target.write_text("", encoding="utf-8")
        return target
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return target


def _date_text(value: date | None) -> str:
    return value.isoformat() if value else ""


def _float_text(value: float | None) -> str:
    return "" if value is None else f"{value:g}"


def _signed(value: int) -> str:
    return f"{value:+d}"
