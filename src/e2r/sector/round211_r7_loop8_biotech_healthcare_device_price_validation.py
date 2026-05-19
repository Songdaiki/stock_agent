"""Round-211 R7 Loop-8 biotech/healthcare/device price validation pack.

Round 211 is calibration/evaluation material only. It turns
``docs/round/round_211.md`` into structured case records and shadow scoring
notes.

Easy example: an FDA approval is Stage 2 attention. It is not Stage 3-Green
until prescriptions, reimbursement, revenue, royalties, utilization, margin,
cash runway, and price path after evidence are visible as of the case date.
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


ROUND211_SOURCE_ROUND_PATH = "docs/round/round_211.md"
ROUND211_LARGE_SECTOR = Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE
ROUND211_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round211_r7_loop8_biotech_healthcare_device_price_validation"
ROUND211_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r7_loop8_round211.jsonl"
ROUND211_DEFAULT_AUDIT_PATH = "data/sector_taxonomy/round211_r7_loop8_biotech_healthcare_device_price_validation_audit.json"

ROUND211_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "BIOTECH_ROYALTY_COMMERCIALIZATION": E2RArchetype.BIOTECH_ROYALTY_COMMERCIALIZATION.value,
    "SC_FORMULATION_ROYALTY_PLATFORM": E2RArchetype.SC_FORMULATION_ROYALTY_PLATFORM.value,
    "KOREA_ONCOLOGY_DRUG_COMMERCIALIZATION": E2RArchetype.KOREA_ONCOLOGY_DRUG_COMMERCIALIZATION.value,
    "BIOSIMILAR_COMMERCIALIZATION": E2RArchetype.BIOSIMILAR_COMMERCIALIZATION.value,
    "BIOSIMILAR_TARIFF_HEDGE_MANUFACTURING": E2RArchetype.BIOSIMILAR_TARIFF_HEDGE_MANUFACTURING.value,
    "CDMO_HEALTHCARE_CONTRACT": E2RArchetype.CDMO_HEALTHCARE_CONTRACT.value,
    "CDMO_US_TARIFF_HEDGE_CAPACITY": E2RArchetype.CDMO_US_TARIFF_HEDGE_CAPACITY.value,
    "VACCINE_CMO_RESTRUCTURING": E2RArchetype.VACCINE_CMO_RESTRUCTURING.value,
    "BOTULINUM_US_MARKET_ENTRY": E2RArchetype.BOTULINUM_US_MARKET_ENTRY.value,
    "MEDICAL_DEVICE_HEALTHCARE_EXPORT": E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT.value,
    "DIGITAL_HEALTHCARE_AI": E2RArchetype.DIGITAL_HEALTHCARE_AI.value,
    "MEDICAL_AI_EXTERNAL_VALIDATION": E2RArchetype.MEDICAL_AI_EXTERNAL_VALIDATION.value,
    "MEDICAL_AI_SUBGROUP_GENERALIZATION_RISK": E2RArchetype.MEDICAL_AI_SUBGROUP_GENERALIZATION_RISK.value,
    "APPROVAL_ONLY_NOT_COMMERCIALIZATION": E2RArchetype.APPROVAL_ONLY_NOT_COMMERCIALIZATION.value,
    "MANUFACTURING_INSPECTION_CRL_OVERLAY": E2RArchetype.MANUFACTURING_INSPECTION_CRL_OVERLAY.value,
    "COMMERCIALIZATION_FAILURE_OVERLAY": E2RArchetype.COMMERCIALIZATION_FAILURE_OVERLAY.value,
}

ROUND211_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "approval_or_regulatory_clearance",
    "commercial_launch",
    "prescription_volume_or_hospital_adoption",
    "reimbursement_or_payer_access",
    "revenue_recognition",
    "royalty_or_gross_margin_confirmation",
    "capacity_utilization_or_channel_penetration",
    "cash_runway_and_dilution_risk_passed",
    "partner_execution_risk_passed",
    "price_path_after_evidence",
)

ROUND211_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "approval_news_only",
    "clinical_headline_only",
    "paper_validation_without_revenue",
    "mna_without_utilization",
    "fda_approval_without_commercial_sales",
    "partner_peak_sales_without_royalty_visibility",
    "pre_revenue_biotech_story",
    "cash_burn_or_dilution_risk",
    "manufacturing_inspection_issue",
    "subgroup_performance_risk",
)

ROUND211_STAGE4B_WATCH_TRIGGERS: tuple[str, ...] = (
    "fda_approval_price_spike_before_sales",
    "partner_peak_sales_repeated_without_royalty",
    "cdmo_capacity_premium_before_utilization",
    "mna_announcement_day_spike",
    "medical_ai_validation_price_spike_before_reimbursement",
    "valuation_moves_before_commercial_revenue",
)

ROUND211_HARD_4C_GATES: tuple[str, ...] = (
    "fda_crl_or_approval_rejection",
    "efficacy_or_safety_trial_failure",
    "commercialization_failure",
    "prescription_volume_underperformance",
    "reimbursement_failure",
    "royalty_non_recognition",
    "large_dilution",
    "cash_runway_break",
    "manufacturing_inspection_failure",
    "product_safety_issue",
    "subgroup_clinical_performance_failure",
    "partner_launch_failure",
    "patent_ip_legal_loss",
)

ROUND211_PRICE_VALIDATION_FIELDS: tuple[str, ...] = (
    "price_data_source",
    "full_ohlc_available",
    "reported_price_anchor",
    "reported_return_anchor",
    "stage2_price",
    "stage3_price",
    "stage4b_price",
    "stage4c_price",
    "mfe_1d",
    "mae_1d",
    "relative_underperformance_pp",
    "commercial_sales_anchor",
    "trial_size",
    "approval_or_launch_date",
    "capacity_or_transaction_value",
    "price_validation_status",
)


@dataclass(frozen=True)
class Round211ScoreAdjustment:
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
class Round211CaseCandidate:
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
    stage2_price_anchor: float | None
    stage3_price_anchor: float | None
    extra_price_metrics: Mapping[str, float | str]
    score_price_alignment: str
    rerating_result: str
    stage_failure_type: str
    price_validation_status: str
    notes: str

    @property
    def large_sector(self) -> str:
        return ROUND211_LARGE_SECTOR.value

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND211_SCORE_ADJUSTMENTS: tuple[Round211ScoreAdjustment, ...] = (
    Round211ScoreAdjustment("commercial_revenue", 5, "raise", "승인 이후 실제 매출이 보여야 R7 Stage 3 후보가 된다."),
    Round211ScoreAdjustment("royalty_recognition", 5, "raise", "파트너 매출보다 회사의 로열티 인식과 현금 유입이 더 중요하다."),
    Round211ScoreAdjustment("prescription_volume", 5, "raise", "처방량은 임상·승인이 실제 사용으로 바뀌는 증거다."),
    Round211ScoreAdjustment("reimbursement_access", 5, "raise", "보험·수가 접근이 없으면 의료 제품 매출 지속성이 약하다."),
    Round211ScoreAdjustment("capacity_utilization", 5, "raise", "CDMO/CMO는 공장 보유보다 가동률과 수주 전환이 핵심이다."),
    Round211ScoreAdjustment("contract_backlog", 4, "raise", "CDMO와 CMO는 고객 계약과 backlog가 Stage 3 visibility를 만든다."),
    Round211ScoreAdjustment("gross_margin_visibility", 4, "raise", "매출이 있어도 gross margin이 확인돼야 EPS/FCF 체급 변화로 이어진다."),
    Round211ScoreAdjustment("cash_runway", 4, "raise", "현금 runway가 있어야 희석 없이 상업화까지 버틸 수 있다."),
    Round211ScoreAdjustment("us_commercial_launch_with_sales", 4, "raise", "미국 출시와 초기 매출이 함께 있으면 Stage 2에서 Stage 3 후보로 올라간다."),
    Round211ScoreAdjustment("external_validation_with_adoption", 3, "raise", "의료AI는 외부검증에 병원 도입이나 수가가 붙어야 점수를 준다."),
    Round211ScoreAdjustment("approval_news_only", -5, "lower", "승인 뉴스만으로는 Stage 3-Green을 만들 수 없다."),
    Round211ScoreAdjustment("clinical_headline_only", -5, "lower", "임상 헤드라인은 처방·매출·로열티 전까지 Stage 2 watch다."),
    Round211ScoreAdjustment("paper_validation_without_revenue", -4, "lower", "논문 성능은 좋지만 수가·도입·반복매출 없이는 Green 금지다."),
    Round211ScoreAdjustment("mna_without_utilization", -4, "lower", "M&A 발표만 있고 가동률·마진이 없으면 event premium이다."),
    Round211ScoreAdjustment("fda_approval_without_commercial_sales", -4, "lower", "FDA approval 이후 상업 매출이 없으면 Stage 3 보류다."),
    Round211ScoreAdjustment("partner_peak_sales_without_royalty_visibility", -3, "lower", "파트너 peak sales 전망만 있고 로열티 가시성이 없으면 제한한다."),
    Round211ScoreAdjustment("pre_revenue_biotech_story", -5, "lower", "pre-revenue 바이오 스토리는 희석과 현금 runway를 먼저 본다."),
    Round211ScoreAdjustment("cash_burn_or_dilution_risk", -5, "lower", "대규모 희석이나 cash runway 붕괴는 Green hard blocker다."),
    Round211ScoreAdjustment("manufacturing_inspection_issue", -3, "lower", "제조시설 inspection 이슈는 approval과 launch를 지연시킬 수 있다."),
    Round211ScoreAdjustment("subgroup_performance_risk", -3, "lower", "의료AI subgroup 성능 약점은 실제 도입 리스크다."),
)


ROUND211_CASE_CANDIDATES: tuple[Round211CaseCandidate, ...] = (
    Round211CaseCandidate(
        case_id="r7_loop8_alteogen_keytruda_qlex_royalty_watch",
        symbol="196170",
        company_name="알테오젠",
        primary_archetype=E2RArchetype.SC_FORMULATION_ROYALTY_PLATFORM,
        secondary_archetypes=(E2RArchetype.BIOTECH_ROYALTY_COMMERCIALIZATION, E2RArchetype.PATENT_CHALLENGE_OVERLAY),
        case_type="success_candidate",
        stage1_date=date(2025, 3, 27),
        stage2_date=date(2025, 9, 19),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 3, 5),
        stage3_decision="stage3_candidate_only_until_alteogen_royalty_recognition_cash_receipt_and_price_path_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("keytruda_qlex_fda_approval", "keytruda_qlex_2025_sales_40m_usd", "merck_target_conversion_30_40pct", "keytruda_2024_sales_30bn_usd", "alteogen_enzyme_used"),
        red_flag_fields=("royalty_recognition_unverified", "cash_receipt_unverified", "halozyme_patent_dispute_watch", "korea_stock_ohlc_unavailable"),
        price_data_source="Reuters/WSJ/MarketWatch evidence anchors",
        reported_price_anchor="Alteogen Korea OHLC unavailable after deep search",
        reported_return_anchor="Keytruda Qlex 2025 sales $40M; analyst potential above $6B; Merck target 30-40% conversion within two years",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        extra_price_metrics={"keytruda_2024_sales_usd_bn": 30.0, "keytruda_qlex_2025_sales_usd_mn": 40.0, "qlex_sales_vs_keytruda_2024_pct": 0.13, "merck_target_conversion_low_pct": 30.0, "merck_target_conversion_high_pct": 40.0, "potential_qlex_sales_usd_bn": 6.0, "potential_qlex_sales_vs_keytruda_2024_pct": 20.0},
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Approval plus initial Qlex sales makes this the strongest R7 commercialization watch, but Stage 3 waits for Alteogen royalty and cash receipt.",
    ),
    Round211CaseCandidate(
        case_id="r7_loop8_yuhan_lazcluze_approval_royalty_watch",
        symbol="000100",
        company_name="유한양행",
        primary_archetype=E2RArchetype.KOREA_ONCOLOGY_DRUG_COMMERCIALIZATION,
        secondary_archetypes=(E2RArchetype.BIOTECH_ROYALTY_COMMERCIALIZATION, E2RArchetype.APPROVAL_ONLY_NOT_COMMERCIALIZATION),
        case_type="success_candidate",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2024, 8, 20),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="stage3_requires_prescription_volume_partner_sales_yuhan_royalty_recognition_and_eps_revision",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("fda_approval_rybrevant_lazcluze", "phase3_risk_reduction_30pct", "mariposa_trial_858_participants", "jnj_partner_execution"),
        red_flag_fields=("prescription_volume_unverified", "partner_sales_unverified", "yuhan_royalty_unverified", "approval_only_not_green"),
        price_data_source="Barron's FDA approval and public drug approval summary",
        reported_price_anchor="Yuhan Korea OHLC unavailable after deep search",
        reported_return_anchor="J&J +0.4% premarket on approval/acquisition news",
        mfe_1d=0.4,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        extra_price_metrics={"jnj_event_return_premarket_pct": 0.4, "risk_reduction_vs_osimertinib_pct": 30.0, "trial_size": 858.0},
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="FDA approval is Stage 2. Stage 3 waits for prescriptions, partner sales, royalty recognition, and EPS revision.",
    ),
    Round211CaseCandidate(
        case_id="r7_loop8_sk_bioscience_idt_cmo_event",
        symbol="302440",
        company_name="SK바이오사이언스",
        primary_archetype=E2RArchetype.CDMO_HEALTHCARE_CONTRACT,
        secondary_archetypes=(E2RArchetype.VACCINE_CMO_RESTRUCTURING, E2RArchetype.CDMO_US_TARIFF_HEDGE_CAPACITY),
        case_type="event_premium",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2024, 6, 27),
        stage3_date=None,
        stage4b_date=date(2024, 6, 27),
        stage4c_date=None,
        stage3_decision="mna_is_stage2_event_premium_until_utilization_backlog_margin_and_fcf_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("idt_biologika_60pct_acquisition", "deal_value_339bn_krw", "global_cmo_production_base", "event_price_spike"),
        red_flag_fields=("mna_without_utilization", "integration_cost_unverified", "new_order_failure_risk", "cash_burn_watch"),
        price_data_source="Reuters/MarketWatch reported event anchors",
        reported_price_anchor="MarketWatch reported KRW 52,200 after +5.8%",
        reported_return_anchor="Reuters intraday +11.7%; MarketWatch +5.8% to 52,200 KRW",
        mfe_1d=11.7,
        mae_1d=None,
        stage2_price_anchor=52200.0,
        stage3_price_anchor=None,
        extra_price_metrics={"marketwatch_event_mfe_1d_pct": 5.8, "implied_prior_close_krw": 49338.0, "reuters_intraday_mfe_pct": 11.7, "deal_value_krw_bn": 339.0, "deal_value_usd_mn": 243.75},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="stage2_watch_success",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="The IDT deal is Stage 2 and 4B-watch event premium; utilization, backlog, margin, and FCF are required for Stage 3.",
    ),
    Round211CaseCandidate(
        case_id="r7_loop8_celltrion_us_factory_tariff_hedge",
        symbol="068270",
        company_name="셀트리온",
        primary_archetype=E2RArchetype.BIOSIMILAR_TARIFF_HEDGE_MANUFACTURING,
        secondary_archetypes=(E2RArchetype.BIOSIMILAR_COMMERCIALIZATION, E2RArchetype.CDMO_US_TARIFF_HEDGE_CAPACITY),
        case_type="success_candidate",
        stage1_date=date(2025, 7, 29),
        stage2_date=date(2025, 9, 23),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="stage3_requires_product_transfer_fda_quality_readiness_utilization_gross_margin_and_fcf",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("us_pharma_tariff_hedge", "imclone_systems_acquisition_330m_usd", "planned_investment_700bn_krw", "us_product_line_protection"),
        red_flag_fields=("product_transfer_unverified", "utilization_unverified", "capex_burden_watch", "biosimilar_pricing_pressure"),
        price_data_source="Reuters transaction and investment anchors",
        reported_price_anchor="Celltrion Korea OHLC unavailable after deep search",
        reported_return_anchor="US facility acquisition $330M; expansion up to 700B KRW / $478.17M",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        extra_price_metrics={"planned_investment_krw_bn": 700.0, "imclone_acquisition_usd_mn": 330.0, "imclone_acquisition_krw_bn": 483.1, "expansion_investment_krw_bn": 700.0, "expansion_investment_usd_mn": 478.17},
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="US manufacturing is Stage 2 tariff-hedge evidence; product transfer, utilization, margin, and FCF decide promotion.",
    ),
    Round211CaseCandidate(
        case_id="r7_loop8_samsung_biologics_gsk_facility_saturation",
        symbol="207940",
        company_name="삼성바이오로직스",
        primary_archetype=E2RArchetype.CDMO_US_TARIFF_HEDGE_CAPACITY,
        secondary_archetypes=(E2RArchetype.CDMO_HEALTHCARE_CONTRACT,),
        case_type="success_candidate",
        stage1_date=date(2025, 1, 1),
        stage2_date=date(2025, 12, 22),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="new_us_facility_event_is_not_fresh_stage3_until_utilization_contract_transfer_margin_and_fcf_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("gsk_rockville_facility_acquisition", "deal_value_280m_usd", "drug_substance_capacity_60000l", "us_demand_response"),
        red_flag_fields=("weak_price_reaction", "valuation_saturation_watch", "contract_transfer_unverified", "utilization_unverified", "capex_overrun_watch"),
        price_data_source="Reuters reported event return and capacity anchor",
        reported_price_anchor="Samsung Biologics -0.4% while KOSPI +2.0%",
        reported_return_anchor="relative underperformance -2.4pp on GSK facility acquisition event",
        mfe_1d=None,
        mae_1d=-0.4,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        extra_price_metrics={"stage2_event_mae_1d_pct": -0.4, "kospi_same_day_return_pct": 2.0, "relative_underperformance_pp": -2.4, "deal_value_usd_mn": 280.0, "facility_capacity_liters": 60000.0},
        score_price_alignment="evidence_good_but_price_failed",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="Good CDMO capacity evidence met weak price reaction, which is valuation-saturation watch rather than fresh Green.",
    ),
    Round211CaseCandidate(
        case_id="r7_loop8_hugel_letybo_us_launch",
        symbol="145020",
        company_name="휴젤",
        primary_archetype=E2RArchetype.BOTULINUM_US_MARKET_ENTRY,
        secondary_archetypes=(E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT, E2RArchetype.BOTULINUM_AESTHETIC_REGULATED),
        case_type="success_candidate",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2025, 3, 7),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="stage3_requires_us_sales_channel_penetration_asp_repeat_orders_and_opm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("letybo_us_fda_approval", "us_dermatology_office_rollout", "botox_competitor", "potential_25_33pct_discount"),
        red_flag_fields=("us_sales_unverified", "channel_penetration_unverified", "pricing_war_watch", "safety_or_regulatory_watch"),
        price_data_source="Allure/New York Post product launch evidence",
        reported_price_anchor="Hugel Korea OHLC unavailable after deep search",
        reported_return_anchor="Letybo estimated $9-12/unit vs Botox $12-18/unit; potential 25-33.3% discount",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        extra_price_metrics={"letybo_unit_price_low_usd": 9.0, "letybo_unit_price_high_usd": 12.0, "botox_unit_price_low_usd": 12.0, "botox_unit_price_high_usd": 18.0, "potential_discount_low_pct": 25.0, "potential_discount_high_pct": 33.3},
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="US rollout is Stage 2; US sales, channel penetration, ASP stability, repeat orders, and OPM are required before Green.",
    ),
    Round211CaseCandidate(
        case_id="r7_loop8_lunit_medical_ai_validation_not_green",
        symbol="328130",
        company_name="루닛",
        primary_archetype=E2RArchetype.MEDICAL_AI_EXTERNAL_VALIDATION,
        secondary_archetypes=(E2RArchetype.DIGITAL_HEALTHCARE_AI, E2RArchetype.MEDICAL_AI_SUBGROUP_GENERALIZATION_RISK),
        case_type="failed_rerating",
        stage1_date=date(2023, 1, 1),
        stage2_date=date(2025, 3, 17),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="external_validation_is_not_green_without_reimbursement_hospital_adoption_recurring_revenue_and_cash_runway",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("external_validation_163449_dbt_exams", "overall_auc_0_91", "commercial_model_validation"),
        red_flag_fields=("reimbursement_unverified", "hospital_adoption_unverified", "subgroup_performance_risk", "cash_runway_unverified"),
        price_data_source="arXiv clinical validation evidence",
        reported_price_anchor="Lunit Korea OHLC unavailable after deep search",
        reported_return_anchor="AUC 0.91 overall; weaker AUC in non-invasive cancer and calcification subgroups",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        extra_price_metrics={"exam_count": 163449.0, "overall_auc": 0.91, "non_invasive_cancer_auc": 0.85, "calcification_auc": 0.80, "dense_breast_auc": 0.90},
        score_price_alignment="unknown",
        rerating_result="no_rerating",
        stage_failure_type="false_yellow",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="External validation is useful Stage 2 evidence, but reimbursement, adoption, revenue, and cash runway are missing.",
    ),
)


def round211_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND211_CASE_CANDIDATES:
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
                "Round211 R7 Loop-8 biotech/healthcare/device price-path "
                "validation case. Calibration-only; not production scoring input."
            ),
            stage1_evidence=tuple(field for field in candidate.evidence_fields if "approval" in field or "launch" in field or "validation" in field or "acquisition" in field),
            stage2_evidence=candidate.evidence_fields if candidate.stage2_date else (),
            stage3_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "sales" in field
                or "royalty" in field
                or "utilization" in field
                or "revenue" in field
                or "commercial" in field
                or "capacity" in field
            ),
            stage4b_evidence=tuple(
                field
                for field in (*candidate.evidence_fields, *candidate.red_flag_fields)
                if "event" in field or "spike" in field or "price" in field or "valuation" in field or "premium" in field or "weak_price" in field
            ),
            stage4c_evidence=tuple(
                field
                for field in candidate.red_flag_fields
                if "patent" in field
                or "inspection" in field
                or "failure" in field
                or "safety" in field
                or "cash" in field
                or "dilution" in field
                or "subgroup" in field
                or "partner" in field
                or "reimbursement" in field
            ),
            must_have_fields=ROUND211_GREEN_REQUIRED_FIELDS,
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
            score_weight_hint={
                "commercial_revenue_delta": 5.0,
                "royalty_recognition_delta": 5.0,
                "prescription_volume_delta": 5.0,
                "reimbursement_access_delta": 5.0,
                "capacity_utilization_delta": 5.0,
                "contract_backlog_delta": 4.0,
                "gross_margin_visibility_delta": 4.0,
                "cash_runway_delta": 4.0,
                "us_commercial_launch_with_sales_delta": 4.0,
                "external_validation_with_adoption_delta": 3.0,
                "approval_news_only_delta": -5.0,
                "clinical_headline_only_delta": -5.0,
                "paper_validation_without_revenue_delta": -4.0,
                "mna_without_utilization_delta": -4.0,
                "fda_approval_without_commercial_sales_delta": -4.0,
                "partner_peak_sales_without_royalty_visibility_delta": -3.0,
                "pre_revenue_biotech_story_delta": -5.0,
                "cash_burn_or_dilution_risk_delta": -5.0,
                "manufacturing_inspection_issue_delta": -3.0,
                "subgroup_performance_risk_delta": -3.0,
            },
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "full_ohlc_complete_false",
                "price_validation_partial_with_reported_price_anchors",
                "do_not_invent_price_or_stage_dates",
                "do_not_treat_approval_clinical_paper_mna_or_peak_sales_story_as_green_alone",
                *ROUND211_GREEN_REQUIRED_FIELDS,
                *ROUND211_GREEN_FORBIDDEN_PATTERNS,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(
                stage2_price=candidate.stage2_price_anchor,
                stage3_price=candidate.stage3_price_anchor,
                mfe_30d=candidate.mfe_1d,
                mae_30d=candidate.mae_1d,
                price_validation_status=candidate.price_validation_status,
            ),
            data_quality=CaseDataQuality(
                official_data_available=True,
                report_data_available=True,
                price_data_available=candidate.stage2_price_anchor is not None or candidate.mfe_1d is not None or candidate.mae_1d is not None,
                stage_dates_confidence=0.8 if candidate.stage2_date else 0.65,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round211_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND211_CASE_CANDIDATES:
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
                "extra_price_metrics": json.dumps(candidate.extra_price_metrics, ensure_ascii=False, sort_keys=True),
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


def round211_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND211_SCORE_ADJUSTMENTS)


def round211_price_validation_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round211_price_validation": "true"} for field in ROUND211_PRICE_VALIDATION_FIELDS)


def round211_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {"round211_label": label, "canonical_archetype": canonical}
        for label, canonical in ROUND211_REQUIRED_TARGET_ALIASES.items()
    )


def round211_summary() -> dict[str, int | bool | str]:
    cases = ROUND211_CASE_CANDIDATES
    return {
        "source_round": ROUND211_SOURCE_ROUND_PATH,
        "large_sector": ROUND211_LARGE_SECTOR.value,
        "case_candidate_count": len(cases),
        "success_candidate_count": sum(1 for case in cases if case.case_type == "success_candidate"),
        "event_premium_count": sum(1 for case in cases if case.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for case in cases if case.case_type == "failed_rerating"),
        "stage3_case_count": sum(1 for case in cases if case.stage3_date is not None),
        "stage4b_watch_count": sum(1 for case in cases if case.stage4b_status == "watch"),
        "hard_4c_case_count": sum(1 for case in cases if case.hard_4c_confirmed),
        "target_archetype_count": len(ROUND211_REQUIRED_TARGET_ALIASES),
        "price_validation_completed": "partial_with_reported_price_anchors",
        "full_ohlc_complete": False,
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
    }


def round211_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND211_SOURCE_ROUND_PATH,
        "large_sector": ROUND211_LARGE_SECTOR.value,
        "summary": round211_summary(),
        "target_aliases": dict(ROUND211_REQUIRED_TARGET_ALIASES),
        "green_required_fields": list(ROUND211_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND211_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_watch_triggers": list(ROUND211_STAGE4B_WATCH_TRIGGERS),
        "hard_4c_gates": list(ROUND211_HARD_4C_GATES),
        "what_not_to_change": [
            "do_not_use_round211_cases_as_candidate_generation_input",
            "do_not_apply_shadow_weights_to_production_scoring_yet",
            "do_not_treat_approval_clinical_paper_mna_or_partner_peak_sales_as_green",
            "do_not_invent_ohlc_or_stage_dates",
        ],
    }


def render_round211_summary_markdown() -> str:
    summary = round211_summary()
    lines = [
        "# Round 211 R7 Loop 8 Biotech Healthcare Device Price Validation",
        "",
        "This pack is calibration-only. Production scoring and candidate generation are unchanged.",
        "",
        "## Summary",
        "",
        f"- source_round: {summary['source_round']}",
        f"- large_sector: {summary['large_sector']}",
        f"- cases: {summary['case_candidate_count']}",
        f"- success_candidate: {summary['success_candidate_count']}",
        f"- event_premium: {summary['event_premium_count']}",
        f"- failed_rerating: {summary['failed_rerating_count']}",
        f"- Stage 3 dated cases: {summary['stage3_case_count']}",
        f"- 4B-watch cases: {summary['stage4b_watch_count']}",
        f"- hard_4c_case_count: {summary['hard_4c_case_count']}",
        f"- full_ohlc_complete: {str(summary['full_ohlc_complete']).lower()}",
        "",
        "## Case Matrix",
        "",
        "| case | company | type | stage2 | stage3 | 4B | 4C | alignment | note |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for case in ROUND211_CASE_CANDIDATES:
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
                    case.score_price_alignment,
                    case.notes,
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "- Alteogen is the strongest R7 commercialization watch, but Stage 3 waits for Alteogen royalty recognition and cash receipt.",
            "- Yuhan, Hugel, and Celltrion are Stage 2 until prescriptions, sales, royalties, channel penetration, utilization, margin, and FCF confirm.",
            "- SK Bioscience IDT is Stage 2/event premium because M&A without utilization is not Green.",
            "- Samsung Biologics shows that good CDMO capacity news can still fail price confirmation when valuation is saturated.",
            "- Lunit external validation is not Green without reimbursement, hospital adoption, recurring revenue, and cash runway.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round211_green_gate_review_markdown() -> str:
    lines = [
        "# Round 211 R7 Green Gate Review",
        "",
        "Do not apply these weights to production scoring yet.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND211_GREEN_REQUIRED_FIELDS)
    lines.extend(["", "## Forbidden Patterns", ""])
    lines.extend(f"- {field}" for field in ROUND211_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(
        [
            "",
            "## Easy Example",
            "- `FDA approval` means Stage 2 attention.",
            "- `FDA approval + prescriptions + reimbursement + revenue + royalties + cash runway` is the bundle that can support Stage 3.",
            "- `M&A announcement + same-day price spike` is 4B/event premium until utilization, backlog, margin, and FCF exist.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round211_stage4b_4c_review_markdown() -> str:
    lines = [
        "# Round 211 R7 4B/4C Review",
        "",
        "## 4B Watch Triggers",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND211_STAGE4B_WATCH_TRIGGERS)
    lines.extend(["", "## Hard 4C Gates", ""])
    lines.extend(f"- {field}" for field in ROUND211_HARD_4C_GATES)
    lines.extend(["", "## Case Notes", ""])
    for case in ROUND211_CASE_CANDIDATES:
        if case.stage4b_status == "watch" or case.red_flag_fields:
            lines.append(f"- {case.case_id}: {', '.join(case.red_flag_fields)}")
    return "\n".join(lines) + "\n"


def render_round211_price_validation_plan_markdown() -> str:
    lines = [
        "# Round 211 R7 Price Validation Plan",
        "",
        "- price_validation_completed: partial_with_reported_price_anchors",
        "- full_ohlc_complete: false",
        "- Do not invent OHLC, peak, MFE, or MAE where raw adjusted daily prices are unavailable.",
        "",
        "## Backfill Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND211_PRICE_VALIDATION_FIELDS)
    return "\n".join(lines) + "\n"


def write_round211_r7_loop8_reports(
    output_directory: str | Path = ROUND211_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND211_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND211_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)

    paths = {
        "cases": write_case_library(round211_case_records(), cases_path),
        "audit": _write_json(round211_audit_payload(), audit_path),
        "summary": output / "round211_r7_loop8_price_validation_summary.md",
        "case_matrix": output / "round211_r7_loop8_case_matrix.csv",
        "target_aliases": output / "round211_r7_loop8_target_aliases.csv",
        "score_adjustments": output / "round211_r7_loop8_score_adjustments.csv",
        "price_validation_fields": output / "round211_r7_loop8_price_validation_fields.csv",
        "green_gate_review": output / "round211_r7_loop8_green_gate_review.md",
        "price_validation_plan": output / "round211_r7_loop8_price_validation_plan.md",
        "stage4b_4c_review": output / "round211_r7_loop8_stage4b_4c_review.md",
    }
    paths["summary"].write_text(render_round211_summary_markdown(), encoding="utf-8")
    _write_csv(round211_case_rows(), paths["case_matrix"])
    _write_csv(round211_target_alias_rows(), paths["target_aliases"])
    _write_csv(round211_score_adjustment_rows(), paths["score_adjustments"])
    _write_csv(round211_price_validation_field_rows(), paths["price_validation_fields"])
    paths["green_gate_review"].write_text(render_round211_green_gate_review_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round211_price_validation_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round211_stage4b_4c_review_markdown(), encoding="utf-8")
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
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return target


def _date_text(value: date | None) -> str:
    return value.isoformat() if value else ""


def _float_text(value: float | None) -> str:
    return "" if value is None else f"{value:g}"
