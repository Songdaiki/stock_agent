"""Round-214 R10 Loop-8 construction/real-estate/materials validation pack.

Round 214 is calibration/evaluation material only. It structures
``docs/round/round_214.md`` into case records, reported anchors, and shadow
scoring notes.

Easy example: a $6B EPC contract is a strong Stage 2 signal. It is not
Stage 3-Green until margin, progress revenue, working-capital cash collection,
and cost control are visible as of the case date.
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


ROUND214_SOURCE_ROUND_PATH = "docs/round/round_214.md"
ROUND214_LARGE_SECTOR = Round10LargeSector.CONSTRUCTION_REAL_ESTATE_MATERIALS
ROUND214_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round214_r10_loop8_construction_real_estate_materials_price_validation"
ROUND214_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r10_loop8_round214.jsonl"
ROUND214_DEFAULT_AUDIT_PATH = "data/sector_taxonomy/round214_r10_loop8_construction_real_estate_materials_price_validation_audit.json"

ROUND214_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "OVERSEAS_EPC_CONTRACT_BACKLOG_KOREA": E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG_KOREA.value,
    "EPC_LOW_MARGIN_ORDER_OVERLAY": E2RArchetype.EPC_LOW_MARGIN_ORDER_OVERLAY.value,
    "PF_RESTRUCTURING_RELIEF": E2RArchetype.PF_RESTRUCTURING_RELIEF.value,
    "PF_CREDIT_REDTEAM_OVERLAY": E2RArchetype.PF_CREDIT_REDTEAM_OVERLAY.value,
    "APARTMENT_QUALITY_SAFETY_OVERLAY": E2RArchetype.APARTMENT_QUALITY_SAFETY_OVERLAY.value,
    "OPERATIONAL_TRUST_HARD_4C": E2RArchetype.OPERATIONAL_TRUST_HARD_4C.value,
    "AI_DATA_CENTER_REAL_ASSET_DEVELOPMENT": E2RArchetype.AI_DATA_CENTER_REAL_ASSET_DEVELOPMENT.value,
    "AI_DATA_CENTER_NO_REVENUE_NO_TENANT": E2RArchetype.AI_DATA_CENTER_NO_REVENUE_NO_TENANT.value,
    "DATA_CENTER_POWER_WATER_PERMITTING": E2RArchetype.DATA_CENTER_POWER_WATER_PERMITTING.value,
    "PRICE_ONLY_RALLY": E2RArchetype.PRICE_ONLY_RALLY.value,
    "THESIS_BREAK_4C": E2RArchetype.THESIS_BREAK_4C.value,
}

ROUND214_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "company_level_contract_or_tenant",
    "margin_or_noi_affo_visibility",
    "cash_flow_after_working_capital",
    "pf_funding_cost_passed",
    "project_progress_or_cost_control",
    "tenant_occupancy_utilization_confirmed",
    "capex_per_share_or_dilution_passed",
    "safety_quality_trust_passed",
    "price_path_after_evidence",
)

ROUND214_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "contract_headline_only",
    "pf_relief_policy_only",
    "real_estate_rebound_theme_only",
    "data_center_theme_without_tenant",
    "asset_headline_without_noi_affo",
    "reit_dividend_headline_only",
    "safety_incident",
    "working_capital_deterioration",
    "low_margin_epc_order",
    "tenant_absent",
    "power_water_permitting_failure",
)

ROUND214_STAGE4B_WATCH_TRIGGERS: tuple[str, ...] = (
    "large_epc_award_event_rally",
    "pf_support_policy_sector_rally",
    "data_center_theme_basket_rally",
    "reit_rate_cut_only_rally",
    "reconstruction_disaster_recovery_theme",
)

ROUND214_HARD_4C_GATES: tuple[str, ...] = (
    "pf_workout_debt_reschedule",
    "pf_delinquency_spike",
    "unsold_apartment_failure",
    "construction_cost_overrun",
    "working_capital_deterioration",
    "contract_cancellation",
    "owner_payment_delay",
    "low_margin_epc_loss",
    "apartment_collapse_quality_failure",
    "repeated_workplace_fatality",
    "worksite_shutdown",
    "license_cancellation_risk",
    "tenant_absence",
    "power_water_permitting_failure",
    "affo_integrity_break",
    "capex_dilution",
)

ROUND214_PRICE_VALIDATION_FIELDS: tuple[str, ...] = (
    "price_data_source",
    "full_ohlc_available",
    "reported_price_anchor",
    "reported_return_anchor",
    "stage2_event_peak_price",
    "stage2_event_mfe_1d_pct",
    "implied_pre_event_reference_price",
    "kospi_context_return_pct",
    "relative_outperformance_pp",
    "contract_value_or_capex",
    "pf_delinquency_or_support_metric",
    "safety_or_quality_metric",
    "tenant_noi_affo_status",
    "price_validation_status",
)


@dataclass(frozen=True)
class Round214ScoreAdjustment:
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
class Round214CaseCandidate:
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
    stage4c_price_anchor: float | None
    extra_price_metrics: Mapping[str, float | str]
    score_price_alignment: str
    rerating_result: str
    stage_failure_type: str
    price_validation_status: str
    notes: str

    @property
    def large_sector(self) -> str:
        return ROUND214_LARGE_SECTOR.value

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND214_SCORE_ADJUSTMENTS: tuple[Round214ScoreAdjustment, ...] = (
    Round214ScoreAdjustment("cash_flow_after_working_capital", 5, "raise", "건설/EPC는 수주보다 현금회수가 Stage 3를 결정한다."),
    Round214ScoreAdjustment("epc_margin_visibility", 5, "raise", "대형 EPC 수주도 마진이 확인되기 전에는 Stage 2다."),
    Round214ScoreAdjustment("project_cost_control", 5, "raise", "공사비와 원가율 안정이 Green의 전제다."),
    Round214ScoreAdjustment("handover_milestone", 4, "raise", "인도 milestone은 Stage 2 evidence로 인정한다."),
    Round214ScoreAdjustment("pf_credit_cleanup", 5, "raise", "PF는 지원책보다 부실 정리와 credit cleanup이 중요하다."),
    Round214ScoreAdjustment("funding_cost_control", 5, "raise", "금융비용이 안정돼야 R10 rerating이 지속된다."),
    Round214ScoreAdjustment("tenant_contract_quality", 5, "raise", "데이터센터는 tenant 계약이 있어야 자산 headline을 넘는다."),
    Round214ScoreAdjustment("noi_affo_visibility", 5, "raise", "부동산/데이터센터는 NOI/AFFO가 확인돼야 Green이 가능하다."),
    Round214ScoreAdjustment("power_water_permitting_secured", 4, "raise", "데이터센터는 전력·용수·인허가가 병목이다."),
    Round214ScoreAdjustment("safety_quality_trust", 5, "raise", "건설주는 안전·품질 신뢰가 깨지면 수주잔고보다 RedTeam이 먼저다."),
    Round214ScoreAdjustment("contract_headline_only", -5, "lower", "수주 headline만으로는 Stage 3-Green 금지다."),
    Round214ScoreAdjustment("pf_relief_policy_only", -5, "lower", "PF 지원책은 relief이지 Green 증거가 아니다."),
    Round214ScoreAdjustment("real_estate_rebound_theme_only", -4, "lower", "부동산 회복 테마만으로는 이익 체급 변화가 아니다."),
    Round214ScoreAdjustment("data_center_theme_without_tenant", -5, "lower", "임차계약 없는 데이터센터 테마는 price-only rally다."),
    Round214ScoreAdjustment("asset_headline_without_noi_affo", -5, "lower", "자산 headline만 있고 NOI/AFFO가 없으면 Green 금지다."),
    Round214ScoreAdjustment("epc_backlog_without_margin", -5, "lower", "수주잔고가 있어도 저마진이면 Stage 3를 막는다."),
    Round214ScoreAdjustment("low_margin_order_risk", -4, "lower", "저마진 수주는 4C-watch다."),
    Round214ScoreAdjustment("capex_per_share_dilution", -4, "lower", "데이터센터 capex가 주당가치를 희석하면 감점한다."),
    Round214ScoreAdjustment("quality_safety_incident", -5, "lower", "아파트 붕괴와 반복 사망사고는 hard 4C다."),
    Round214ScoreAdjustment("workplace_fatality_repeated", -5, "lower", "반복 사망사고와 현장중단은 operational trust break다."),
)


ROUND214_CASE_CANDIDATES: tuple[Round214CaseCandidate, ...] = (
    Round214CaseCandidate(
        case_id="r10_loop8_samsung_ea_fadhili_epc",
        symbol="028050",
        company_name="삼성E&A",
        primary_archetype=E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG_KOREA,
        secondary_archetypes=(E2RArchetype.EPC_LOW_MARGIN_ORDER_OVERLAY,),
        case_type="success_candidate",
        stage1_date=date(2024, 4, 2),
        stage2_date=date(2024, 4, 3),
        stage3_date=None,
        stage4b_date=date(2024, 4, 3),
        stage4c_date=None,
        stage3_decision="stage3_requires_epc_margin_progress_revenue_cash_collection_and_cost_control",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("fadhili_gas_expansion_epc", "samsung_contract_value_6bn_usd", "fadihli_capacity_25_to_40_bscfd", "completion_target_2027_11", "event_peak_price_26750_krw"),
        red_flag_fields=("epc_margin_unverified", "progress_revenue_unverified", "cash_collection_unverified", "low_margin_order_risk_watch"),
        price_data_source="WSJ/Reuters reported price and contract anchors",
        reported_price_anchor="26,750 KRW intraday event peak",
        reported_return_anchor="Samsung E&A intraday +8.5%; KOSPI -1.4%",
        mfe_1d=8.5,
        mae_1d=None,
        stage2_price_anchor=26750.0,
        stage3_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={
            "stage2_event_peak_price_krw": 26750.0,
            "stage2_event_mfe_1d_pct": 8.5,
            "implied_pre_event_reference_price_krw": 24654.0,
            "kospi_same_context_return_pct": -1.4,
            "relative_intraday_outperformance_vs_kospi_pp": 9.9,
            "contract_value_usd_bn": 6.0,
            "aramco_total_project_usd_bn": 7.7,
            "samsung_share_of_project_pct": 77.9,
            "kb_target_price_krw": 35000.0,
            "target_upside_from_event_peak_pct": 30.8,
        },
        score_price_alignment="aligned",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="Large EPC award is Stage 2 and event 4B-watch; Stage 3 requires margin, progress revenue, and cash collection.",
    ),
    Round214CaseCandidate(
        case_id="r10_loop8_hyundai_ec_jafurah_gas_infra",
        symbol="000720",
        company_name="현대건설",
        primary_archetype=E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG_KOREA,
        secondary_archetypes=(E2RArchetype.EPC_LOW_MARGIN_ORDER_OVERLAY,),
        case_type="success_candidate",
        stage1_date=date(2024, 6, 1),
        stage2_date=date(2024, 6, 30),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="sovereign_epc_contract_is_stage2_until_margin_working_capital_and_cash_recovery_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("aramco_contract_package_25bn_usd", "jafurah_gas_infrastructure", "hyundai_ec_consortium_included", "main_gas_network_expansion"),
        red_flag_fields=("stock_price_anchor_unavailable", "epc_margin_unverified", "working_capital_burden_watch", "owner_payment_delay_watch"),
        price_data_source="Reuters contract and infrastructure evidence",
        reported_price_anchor="Hyundai E&C stock reaction anchor unavailable",
        reported_return_anchor="Aramco signed >$25B Jafurah/main gas network package",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={
            "aramco_contract_package_usd_bn": 25.0,
            "jafurah_sales_gas_target_bscfd": 2.0,
            "main_gas_network_added_capacity_bscfd": 3.2,
            "main_gas_network_added_pipeline_km": 4000.0,
            "jafurah_gas_reserves_tcf": 229.0,
            "jafurah_condensates_bbl_bn": 75.0,
        },
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Sovereign EPC scale supports Stage 2; Green waits for margin, working capital, and cash recovery.",
    ),
    Round214CaseCandidate(
        case_id="r10_loop8_daewoo_ec_grand_faw_handover",
        symbol="047040",
        company_name="대우건설",
        primary_archetype=E2RArchetype.INFRA_RECONSTRUCTION_POLICY,
        secondary_archetypes=(E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG_KOREA,),
        case_type="success_candidate",
        stage1_date=date(2023, 1, 1),
        stage2_date=date(2024, 11, 12),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="handover_milestone_is_stage2_until_profit_recognition_cash_collection_and_follow_on_orders_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("grand_faw_port_handover", "five_docks_completed", "operation_start_planned_2026", "iraq_development_road_17bn_usd"),
        red_flag_fields=("profit_recognition_unverified", "cash_collection_unverified", "iraq_political_risk_watch", "payment_delay_watch"),
        price_data_source="Reuters infrastructure handover evidence",
        reported_price_anchor="Daewoo E&C stock reaction anchor unavailable",
        reported_return_anchor="Grand Faw 5 docks handed over; $17B Development Road project context",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={
            "completed_docks": 5.0,
            "planned_operation_start_year": 2026.0,
            "expected_capacity_2028_mn_containers": 3.5,
            "iraq_development_road_project_usd_bn": 17.0,
        },
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Handover milestone is Stage 2; profit recognition, cash recovery, and follow-on orders decide promotion.",
    ),
    Round214CaseCandidate(
        case_id="r10_loop8_taeyoung_pf_hard_4c",
        symbol="009410",
        company_name="태영건설/PF stress",
        primary_archetype=E2RArchetype.PF_CREDIT_REDTEAM_OVERLAY,
        secondary_archetypes=(E2RArchetype.PF_RESTRUCTURING_RELIEF, E2RArchetype.THESIS_BREAK_4C),
        case_type="4c_thesis_break",
        stage1_date=date(2023, 1, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2023, 12, 1),
        stage3_decision="debt_reschedule_and_pf_delinquency_spike_are_redteam_not_green",
        stage4b_status="watch",
        hard_4c_confirmed=True,
        evidence_fields=("government_support_40_6tn_krw", "syndicated_loan_1tn_to_5tn_krw", "pf_restructuring_policy"),
        red_flag_fields=("pf_workout_debt_reschedule", "pf_delinquency_spike", "liquidity_support_dependency", "sector_contagion_risk"),
        price_data_source="Reuters PF stress and policy support anchors",
        reported_price_anchor="Taeyoung stock reaction anchor unavailable",
        reported_return_anchor="PF delinquency 0.37% to 2.70%; relative increase +629.7%",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={
            "government_support_package_krw_trn": 40.6,
            "pf_delinquency_2021_end_pct": 0.37,
            "pf_delinquency_2023_end_pct": 2.70,
            "pf_delinquency_absolute_increase_pp": 2.33,
            "pf_delinquency_relative_increase_pct": 629.7,
            "syndicated_loan_initial_krw_trn": 1.0,
            "syndicated_loan_max_krw_trn": 5.0,
            "loan_expandability_multiple": 5.0,
        },
        score_price_alignment="false_positive_score",
        rerating_result="thesis_break",
        stage_failure_type="should_have_been_red",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="PF debt reschedule and delinquency spike are hard 4C; liquidity support is relief, not Green.",
    ),
    Round214CaseCandidate(
        case_id="r10_loop8_hdc_hyundai_development_quality_safety_4c",
        symbol="294870",
        company_name="HDC현대산업개발",
        primary_archetype=E2RArchetype.APARTMENT_QUALITY_SAFETY_OVERLAY,
        secondary_archetypes=(E2RArchetype.OPERATIONAL_TRUST_HARD_4C, E2RArchetype.THESIS_BREAK_4C),
        case_type="4c_thesis_break",
        stage1_date=date(2021, 1, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2022, 1, 11),
        stage3_decision="apartment_collapse_quality_failure_is_hard_4c_until_safety_trust_costs_and_orders_recover",
        stage4b_status="watch",
        hard_4c_confirmed=True,
        evidence_fields=("housing_brand_development_context",),
        red_flag_fields=("apartment_collapse_quality_failure", "fatalities_2022_collapse_6", "prior_related_gwangju_fatalities_9", "operational_trust_break"),
        price_data_source="Public accident record; lower confidence for stock-price validation",
        reported_price_anchor="HDC stock reaction anchor unavailable",
        reported_return_anchor="6 fatalities in 2022 collapse; 9 fatalities in prior related Gwangju collapse",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={
            "fatalities_2022_collapse": 6.0,
            "prior_2021_related_gwangju_collapse_fatalities": 9.0,
            "combined_related_gwangju_fatalities": 15.0,
            "source_confidence": "medium_for_accident_facts_low_for_price_validation",
        },
        score_price_alignment="false_positive_score",
        rerating_result="thesis_break",
        stage_failure_type="should_have_been_red",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Apartment collapse and repeated Gwangju safety incidents are hard 4C for construction quality trust.",
    ),
    Round214CaseCandidate(
        case_id="r10_loop8_posco_ec_dl_construction_safety_watch",
        symbol="POSCO_EC/DL_CONSTRUCTION",
        company_name="POSCO E&C / DL Construction",
        primary_archetype=E2RArchetype.OPERATIONAL_TRUST_HARD_4C,
        secondary_archetypes=(E2RArchetype.APARTMENT_QUALITY_SAFETY_OVERLAY, E2RArchetype.THESIS_BREAK_4C),
        case_type="failed_rerating",
        stage1_date=date(2025, 1, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 1, 1),
        stage3_decision="repeated_workplace_fatality_and_site_shutdown_are_4c_watch_until_safety_trust_restored",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("industrial_safety_crackdown", "construction_fatality_rate_high", "regulatory_fine_proposal"),
        red_flag_fields=("repeated_workplace_fatality", "worksite_shutdown", "license_cancellation_risk", "operating_profit_fine_risk"),
        price_data_source="Reuters safety-regulation and operational evidence anchors",
        reported_price_anchor="Direct listed vehicle mapping and stock reaction anchor unavailable",
        reported_return_anchor="POSCO E&C 103 sites halted; DL Construction about 80 executives resigned",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={
            "korea_industrial_death_rate_2023_per_100k": 3.9,
            "oecd_average_death_rate_per_100k": 2.6,
            "relative_excess_vs_oecd_pct": 50.0,
            "korea_construction_death_rate_per_100k": 15.9,
            "posco_ec_sites_halted": 103.0,
            "dl_construction_executives_resigned": 80.0,
            "proposed_fine_pct_of_operating_profit": 5.0,
            "workplace_deaths_2024": 589.0,
            "construction_share": "nearly_half",
        },
        score_price_alignment="false_positive_score",
        rerating_result="thesis_break",
        stage_failure_type="should_have_been_red",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Repeated fatal accidents, site shutdowns, and license/fine risk require 4C-watch and safety-trust gate.",
    ),
    Round214CaseCandidate(
        case_id="r10_loop8_ai_data_center_real_asset_watch",
        symbol="SK/AWS/Samsung_SDS/SK_Telecom_related",
        company_name="SK/AWS·OpenAI 데이터센터",
        primary_archetype=E2RArchetype.AI_DATA_CENTER_REAL_ASSET_DEVELOPMENT,
        secondary_archetypes=(
            E2RArchetype.AI_DATA_CENTER_NO_REVENUE_NO_TENANT,
            E2RArchetype.DATA_CENTER_POWER_WATER_PERMITTING,
            E2RArchetype.PRICE_ONLY_RALLY,
        ),
        case_type="success_candidate",
        stage1_date=date(2025, 6, 20),
        stage2_date=date(2026, 2, 11),
        stage3_date=None,
        stage4b_date=date(2025, 6, 20),
        stage4c_date=None,
        stage3_decision="ai_data_center_is_stage2_until_tenant_noi_affo_power_water_and_capex_per_share_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("sk_aws_ulsan_ai_data_center_7tn_krw", "initial_capacity_100mw", "potential_expansion_1gw", "openai_samsung_sk_initial_20mw_plan", "aws_additional_korea_investment_5bn_usd"),
        red_flag_fields=("data_center_theme_without_tenant", "tenant_absent", "noi_affo_unverified", "power_water_permitting_watch", "capex_per_share_dilution_watch"),
        price_data_source="Reuters investment and event-return anchors",
        reported_price_anchor="AI data-center basket reported returns, not direct R10 listed real-asset OHLC",
        reported_return_anchor="SK Hynix >+3%, Kakao +11%, LG CNS +9%",
        mfe_1d=11.0,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={
            "sk_aws_investment_krw_trn": 7.0,
            "sk_aws_investment_usd_bn": 5.11,
            "aws_component_usd_bn": 4.0,
            "initial_capacity_mw": 100.0,
            "potential_expansion_gw": 1.0,
            "capacity_expansion_potential_multiple": 10.0,
            "construction_start_planned": "2025-09",
            "full_operation_planned_year": 2029.0,
            "openai_samsung_sk_initial_capacity_mw": 20.0,
            "aws_additional_korea_investment_usd_bn": 5.0,
            "sk_hynix_event_mfe_pct_min": 3.0,
            "kakao_event_mfe_pct": 11.0,
            "lg_cns_event_mfe_pct": 9.0,
        },
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="stage2_watch_success",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="AI data center investment is Stage 1/2; tenant, NOI/AFFO, power/water, and capex per share are required before Green.",
    ),
)


def round214_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND214_CASE_CANDIDATES:
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
                "Round214 R10 Loop-8 construction/real-estate/materials price-path "
                "validation case. Calibration-only; not production scoring input."
            ),
            stage1_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "cycle" in field or "policy" in field or "context" in field or "data_center" in field
            ),
            stage2_evidence=candidate.evidence_fields if candidate.stage2_date else (),
            stage3_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "margin" in field
                or "cash" in field
                or "tenant" in field
                or "noi" in field
                or "affo" in field
                or "handover" in field
                or "capacity" in field
            ),
            stage4b_evidence=tuple(
                field
                for field in (*candidate.evidence_fields, *candidate.red_flag_fields)
                if "event" in field or "theme" in field or "policy" in field or "contract" in field or "basket" in field
            ),
            stage4c_evidence=tuple(
                field
                for field in candidate.red_flag_fields
                if "pf" in field
                or "safety" in field
                or "fatality" in field
                or "collapse" in field
                or "worksite" in field
                or "license" in field
                or "margin" in field
                or "cash" in field
                or "tenant" in field
                or "capex" in field
                or "delay" in field
                or "loss" in field
            ),
            must_have_fields=ROUND214_GREEN_REQUIRED_FIELDS,
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
                "cash_flow_after_working_capital_delta": 5.0,
                "epc_margin_visibility_delta": 5.0,
                "project_cost_control_delta": 5.0,
                "handover_milestone_delta": 4.0,
                "pf_credit_cleanup_delta": 5.0,
                "funding_cost_control_delta": 5.0,
                "tenant_contract_quality_delta": 5.0,
                "noi_affo_visibility_delta": 5.0,
                "power_water_permitting_secured_delta": 4.0,
                "safety_quality_trust_delta": 5.0,
                "contract_headline_only_delta": -5.0,
                "pf_relief_policy_only_delta": -5.0,
                "real_estate_rebound_theme_only_delta": -4.0,
                "data_center_theme_without_tenant_delta": -5.0,
                "asset_headline_without_noi_affo_delta": -5.0,
                "epc_backlog_without_margin_delta": -5.0,
                "low_margin_order_risk_delta": -4.0,
                "capex_per_share_dilution_delta": -4.0,
                "quality_safety_incident_delta": -5.0,
                "workplace_fatality_repeated_delta": -5.0,
            },
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "full_ohlc_complete_false",
                "price_validation_partial_with_reported_price_anchors",
                "do_not_invent_price_or_stage_dates",
                "do_not_treat_epc_pf_relief_data_center_theme_or_real_estate_rebound_as_green_alone",
                *ROUND214_GREEN_REQUIRED_FIELDS,
                *ROUND214_GREEN_FORBIDDEN_PATTERNS,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(
                stage2_price=candidate.stage2_price_anchor,
                stage3_price=candidate.stage3_price_anchor,
                stage4b_price=candidate.stage2_price_anchor if candidate.stage4b_date else None,
                stage4c_price=candidate.stage4c_price_anchor,
                mfe_30d=candidate.mfe_1d,
                mae_30d=candidate.mae_1d,
                price_validation_status=candidate.price_validation_status,
            ),
            data_quality=CaseDataQuality(
                official_data_available=True,
                report_data_available=True,
                price_data_available=candidate.stage2_price_anchor is not None
                or candidate.stage4c_price_anchor is not None
                or candidate.mfe_1d is not None
                or candidate.mae_1d is not None,
                stage_dates_confidence=0.8 if candidate.stage2_date or candidate.stage4c_date else 0.65,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round214_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND214_CASE_CANDIDATES:
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
                "stage2_price_anchor": _float_text(candidate.stage2_price_anchor),
                "stage4c_price_anchor": _float_text(candidate.stage4c_price_anchor),
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


def round214_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND214_SCORE_ADJUSTMENTS)


def round214_price_validation_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round214_price_validation": "true"} for field in ROUND214_PRICE_VALIDATION_FIELDS)


def round214_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {"round214_label": label, "canonical_archetype": canonical}
        for label, canonical in ROUND214_REQUIRED_TARGET_ALIASES.items()
    )


def round214_summary() -> dict[str, int | bool | str]:
    cases = ROUND214_CASE_CANDIDATES
    return {
        "source_round": ROUND214_SOURCE_ROUND_PATH,
        "large_sector": ROUND214_LARGE_SECTOR.value,
        "case_candidate_count": len(cases),
        "success_candidate_count": sum(1 for case in cases if case.case_type == "success_candidate"),
        "failed_rerating_count": sum(1 for case in cases if case.case_type == "failed_rerating"),
        "thesis_break_count": sum(1 for case in cases if case.case_type == "4c_thesis_break"),
        "price_moved_without_evidence_count": sum(
            1 for case in cases if case.score_price_alignment == "price_moved_without_evidence"
        ),
        "stage3_case_count": sum(1 for case in cases if case.stage3_date is not None),
        "stage4b_watch_count": sum(1 for case in cases if case.stage4b_status == "watch"),
        "hard_4c_case_count": sum(1 for case in cases if case.hard_4c_confirmed),
        "target_archetype_count": len(ROUND214_REQUIRED_TARGET_ALIASES),
        "price_validation_completed": "partial_with_reported_price_anchors",
        "full_ohlc_complete": False,
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
    }


def round214_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND214_SOURCE_ROUND_PATH,
        "large_sector": ROUND214_LARGE_SECTOR.value,
        "summary": round214_summary(),
        "target_aliases": dict(ROUND214_REQUIRED_TARGET_ALIASES),
        "green_required_fields": list(ROUND214_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND214_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_watch_triggers": list(ROUND214_STAGE4B_WATCH_TRIGGERS),
        "hard_4c_gates": list(ROUND214_HARD_4C_GATES),
        "what_not_to_change": [
            "do_not_use_round214_cases_as_candidate_generation_input",
            "do_not_apply_shadow_weights_to_production_scoring_yet",
            "do_not_treat_epc_pf_relief_data_center_theme_or_real_estate_rebound_as_green",
            "do_not_invent_ohlc_or_stage_dates",
        ],
    }


def render_round214_summary_markdown() -> str:
    summary = round214_summary()
    lines = [
        "# Round 214 R10 Loop 8 Construction Real Estate Materials Price Validation",
        "",
        "This pack is calibration-only. Production scoring and candidate generation are unchanged.",
        "",
        "## Summary",
        "",
        f"- source_round: {summary['source_round']}",
        f"- large_sector: {summary['large_sector']}",
        f"- cases: {summary['case_candidate_count']}",
        f"- success_candidate: {summary['success_candidate_count']}",
        f"- failed_rerating: {summary['failed_rerating_count']}",
        f"- 4c_thesis_break: {summary['thesis_break_count']}",
        f"- price_moved_without_evidence: {summary['price_moved_without_evidence_count']}",
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
    for case in ROUND214_CASE_CANDIDATES:
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
            "- Samsung E&A, Hyundai E&C, and Daewoo E&C are Stage 2 candidates, not automatic Stage 3-Green.",
            "- EPC headline needs margin, progress revenue, working-capital cash recovery, and cost control.",
            "- PF debt reschedule and delinquency spike are hard RedTeam inputs, not Green evidence.",
            "- Apartment collapse and repeated fatal accidents are construction quality/safety 4C gates.",
            "- AI data-center real asset stories need tenant, NOI/AFFO, power/water, and capex-per-share proof.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round214_green_gate_review_markdown() -> str:
    lines = [
        "# Round 214 R10 Green Gate Review",
        "",
        "Do not apply these weights to production scoring yet.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND214_GREEN_REQUIRED_FIELDS)
    lines.extend(["", "## Forbidden Patterns", ""])
    lines.extend(f"- {field}" for field in ROUND214_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(
        [
            "",
            "## Easy Example",
            "- `$6B EPC contract` means Stage 2 routing.",
            "- `margin + cash collection + cost control + price path after evidence` is the bundle that can support Stage 3.",
            "- `PF debt reschedule` or `apartment collapse` is RedTeam / 4C, not a rebound Green.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round214_stage4b_4c_review_markdown() -> str:
    lines = [
        "# Round 214 R10 4B/4C Review",
        "",
        "## 4B Watch Triggers",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND214_STAGE4B_WATCH_TRIGGERS)
    lines.extend(["", "## Hard 4C Gates", ""])
    lines.extend(f"- {field}" for field in ROUND214_HARD_4C_GATES)
    lines.extend(["", "## Case Notes", ""])
    for case in ROUND214_CASE_CANDIDATES:
        if case.stage4b_status == "watch" or case.red_flag_fields:
            lines.append(f"- {case.case_id}: {', '.join(case.red_flag_fields)}")
    return "\n".join(lines) + "\n"


def render_round214_price_validation_plan_markdown() -> str:
    lines = [
        "# Round 214 R10 Price Validation Plan",
        "",
        "- price_validation_completed: partial_with_reported_price_anchors",
        "- full_ohlc_complete: false",
        "- Do not invent OHLC, peak, MFE, or MAE where raw adjusted daily prices are unavailable.",
        "",
        "## Backfill Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND214_PRICE_VALIDATION_FIELDS)
    return "\n".join(lines) + "\n"


def write_round214_r10_loop8_reports(
    output_directory: str | Path = ROUND214_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND214_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND214_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)

    paths = {
        "cases": write_case_library(round214_case_records(), cases_path),
        "audit": _write_json(round214_audit_payload(), audit_path),
        "summary": output / "round214_r10_loop8_price_validation_summary.md",
        "case_matrix": output / "round214_r10_loop8_case_matrix.csv",
        "target_aliases": output / "round214_r10_loop8_target_aliases.csv",
        "score_adjustments": output / "round214_r10_loop8_score_adjustments.csv",
        "price_validation_fields": output / "round214_r10_loop8_price_validation_fields.csv",
        "green_gate_review": output / "round214_r10_loop8_green_gate_review.md",
        "price_validation_plan": output / "round214_r10_loop8_price_validation_plan.md",
        "stage4b_4c_review": output / "round214_r10_loop8_stage4b_4c_review.md",
    }
    paths["summary"].write_text(render_round214_summary_markdown(), encoding="utf-8")
    _write_csv(round214_case_rows(), paths["case_matrix"])
    _write_csv(round214_target_alias_rows(), paths["target_aliases"])
    _write_csv(round214_score_adjustment_rows(), paths["score_adjustments"])
    _write_csv(round214_price_validation_field_rows(), paths["price_validation_fields"])
    paths["green_gate_review"].write_text(render_round214_green_gate_review_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round214_price_validation_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round214_stage4b_4c_review_markdown(), encoding="utf-8")
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
