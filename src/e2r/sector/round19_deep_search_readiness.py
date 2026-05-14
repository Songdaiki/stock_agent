"""Round-19 deep-search readiness and score-normalization research loop.

Round 19 does not change production scoring. It turns the analyst judgment
into a report-only audit: theme absorption is mostly complete, but score
normalization still needs more success/counterexample cases and price-path
validation before any Stage 3-Green gate or score weight is changed.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import ArchetypeCoverage, E2RCaseRecord, coverage_by_archetype, load_case_library
from e2r.sector.theme_tag_mapper import audit_theme_tag_coverage, load_raw_theme_tags, load_theme_tag_map


ROUND19_SOURCE_ROUND_PATH = "docs/round/r_19.md"
ROUND19_DEFAULT_CASE_LIBRARY = "data/e2r_case_library/cases_v03_price_filled.jsonl"
ROUND19_DEFAULT_RAW_TAGS = "data/sector_taxonomy/raw_theme_tags_v05.csv"
ROUND19_DEFAULT_THEME_MAP = "data/sector_taxonomy/theme_tag_map_v05.csv"
ROUND19_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round19_deep_search_readiness"


class Round19Priority(str, Enum):
    """Round-19 research priority buckets."""

    GREEN_VALIDATION = "GREEN_VALIDATION"
    REDTEAM_DEFENSE = "REDTEAM_DEFENSE"
    THIN_BACKFILL = "THIN_BACKFILL"
    EVENT_POLICY_GUARDRAIL = "EVENT_POLICY_GUARDRAIL"


@dataclass(frozen=True)
class Round19DeepSearchTarget:
    """One archetype or sub-archetype that still needs research validation."""

    target_id: str
    canonical_archetype: E2RArchetype
    priority: Round19Priority
    why_it_matters: str
    must_have_evidence: tuple[str, ...]
    red_flag_evidence: tuple[str, ...]
    planned_queries: tuple[str, ...]


@dataclass(frozen=True)
class Round19TargetStatus:
    """Readiness status for a Round-19 target using the current case pack."""

    target: Round19DeepSearchTarget
    positive_count: int
    counterexample_count: int
    total_count: int
    missing_positive_cases: int
    missing_counterexamples: int
    price_gap_count: int
    readiness_status: str
    recommended_next_step: str

    def as_row(self) -> dict[str, str]:
        return {
            "target_id": self.target.target_id,
            "canonical_archetype": self.target.canonical_archetype.value,
            "priority": self.target.priority.value,
            "positive_count": str(self.positive_count),
            "counterexample_count": str(self.counterexample_count),
            "total_count": str(self.total_count),
            "missing_positive_cases": str(self.missing_positive_cases),
            "missing_counterexamples": str(self.missing_counterexamples),
            "price_gap_count": str(self.price_gap_count),
            "readiness_status": self.readiness_status,
            "recommended_next_step": self.recommended_next_step,
            "must_have_evidence": "|".join(self.target.must_have_evidence),
            "red_flag_evidence": "|".join(self.target.red_flag_evidence),
            "planned_queries": "|".join(self.target.planned_queries),
        }


ROUND19_DEEP_SEARCH_TARGETS: tuple[Round19DeepSearchTarget, ...] = (
    Round19DeepSearchTarget(
        target_id="K_BEAUTY_OEM_ODM_EXPORT",
        canonical_archetype=E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,
        priority=Round19Priority.GREEN_VALIDATION,
        why_it_matters="K뷰티는 계약보다 수출채널, 반복주문, 재고/채권 품질이 Green 판단의 핵심이다.",
        must_have_evidence=("export_growth", "channel_expansion", "repeat_orders", "opm_roe_improvement"),
        red_flag_evidence=("china_dependency", "channel_stuffing", "receivables_growth_without_cash"),
        planned_queries=("K뷰티 ODM 수출 OPM ROE PDF", "화장품 미국 일본 채널 확장 반복 주문 리포트"),
    ),
    Round19DeepSearchTarget(
        target_id="MEDICAL_DEVICE_EXPORT",
        canonical_archetype=E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT,
        priority=Round19Priority.GREEN_VALIDATION,
        why_it_matters="의료기기는 장비 판매보다 소모품/반복시술, 허가, 수출국 확장이 visibility다.",
        must_have_evidence=("export_countries", "approval_or_registration", "consumable_or_repeat_revenue", "opm_fcf"),
        red_flag_evidence=("single_device_no_consumable", "approval_delay", "channel_inventory"),
        planned_queries=("의료기기 수출 소모품 반복매출 OPM PDF", "미용의료기기 허가 수출국 확장 리포트"),
    ),
    Round19DeepSearchTarget(
        target_id="CDMO_CONTRACT_UTILIZATION",
        canonical_archetype=E2RArchetype.CDMO_HEALTHCARE_CONTRACT,
        priority=Round19Priority.GREEN_VALIDATION,
        why_it_matters="CDMO는 임상 바이오가 아니라 장기계약, capacity, utilization, FCF로 봐야 한다.",
        must_have_evidence=("long_term_contract", "capacity_utilization", "customer_diversification", "fcf_conversion"),
        red_flag_evidence=("underutilization", "contract_delay", "quality_issue", "customer_concentration"),
        planned_queries=("CDMO 장기계약 가동률 FCF 리포트", "바이오의약품 위탁생산 capacity utilization PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="INSURANCE_UNDERWRITING_VALUEUP",
        canonical_archetype=E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
        priority=Round19Priority.GREEN_VALIDATION,
        why_it_matters="보험/금융은 저PBR보다 ROE, CSM/자본비율, 주주환원 실행이 중요하다.",
        must_have_evidence=("roe", "capital_ratio", "credit_or_loss_cost", "shareholder_return_execution"),
        red_flag_evidence=("low_pbr_only", "pf_credit_cost", "capital_ratio_down"),
        planned_queries=("손해보험 ROE CSM 주주환원 리포트", "금융지주 ROE PBR CET1 자사주 소각 PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="AI_DATA_CENTER_POWER_GRID",
        canonical_archetype=E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE,
        priority=Round19Priority.GREEN_VALIDATION,
        why_it_matters="AI 인프라는 AI 키워드가 아니라 전력/냉각/서버 수주와 EPS 전환이 핵심이다.",
        must_have_evidence=("confirmed_order", "power_or_cooling_bottleneck", "op_eps_revision", "capacity_constraint"),
        red_flag_evidence=("ai_keyword_only", "no_confirmed_order", "customer_capex_cut"),
        planned_queries=("AI 데이터센터 전력 설비 수주 EPS 상향 PDF", "AI 서버 PCB 전력망 병목 리포트"),
    ),
    Round19DeepSearchTarget(
        target_id="SEMI_EQUIPMENT_PCB",
        canonical_archetype=E2RArchetype.SEMI_EQUIPMENT_CAPEX,
        priority=Round19Priority.GREEN_VALIDATION,
        why_it_matters="반도체 장비/PCB는 고객사 capex와 실제 수주/매출 전환이 없으면 테마에 그친다.",
        must_have_evidence=("customer_capex", "orders", "revenue_conversion", "customer_diversification"),
        red_flag_evidence=("single_customer_delay", "capex_cut", "theme_without_order"),
        planned_queries=("HBM 장비 수주 고객사 CAPEX 리포트", "AI 서버 PCB 수주 매출 전환 PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="BATTERY_EV_OVERHEAT_ESS_SHIFT",
        canonical_archetype=E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT,
        priority=Round19Priority.REDTEAM_DEFENSE,
        why_it_matters="2차전지는 EV 수요 둔화와 ESS 전환을 분리하지 않으면 Green 오판이 난다.",
        must_have_evidence=("contract_quality", "price_pass_through", "fcf_after_capex", "demand_visibility"),
        red_flag_evidence=("ev_demand_slowdown", "capa_overbuild", "mineral_price_down", "valuation_heat"),
        planned_queries=("2차전지 EV 수요 둔화 CAPA 과잉 리포트", "ESS 전환 배터리 가동률 마진 PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="CHEMICAL_SPREAD_OVERSUPPLY",
        canonical_archetype=E2RArchetype.COMMODITY_SPREAD,
        priority=Round19Priority.REDTEAM_DEFENSE,
        why_it_matters="화학/소재는 EPS 반등이 있어도 중국 공급과잉이면 구조적 Green이 아니다.",
        must_have_evidence=("product_spread", "inventory_status", "capacity_discipline", "op_eps_revision"),
        red_flag_evidence=("china_oversupply", "spread_reversal", "inventory_loss", "demand_slowdown"),
        planned_queries=("석유화학 중국 공급과잉 영업손실 리포트", "화학 spread reversal inventory loss PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="CONSTRUCTION_PF_CREDIT",
        canonical_archetype=E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT,
        priority=Round19Priority.REDTEAM_DEFENSE,
        why_it_matters="건설은 수주보다 PF, 신용, 원가율, 현금흐름이 먼저다.",
        must_have_evidence=("pf_exposure", "cash_flow", "cost_ratio", "credit_risk"),
        red_flag_evidence=("pf_stress", "unsold_inventory", "liquidity_support_only", "cost_overrun"),
        planned_queries=("건설 PF 리스크 현금흐름 원가율 리포트", "해외 플랜트 수주 마진 PF 부실 PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="SHIPPING_FREIGHT_BOOM_BUST",
        canonical_archetype=E2RArchetype.SHIPPING_FREIGHT_CYCLE,
        priority=Round19Priority.REDTEAM_DEFENSE,
        why_it_matters="해운은 큰 EPS 폭발이 가능하지만 운임 정상화와 선복 공급을 4B/4C로 봐야 한다.",
        must_have_evidence=("freight_rate", "contract_vs_spot", "vessel_supply", "op_eps_revision"),
        red_flag_evidence=("spot_rate_collapse", "overcapacity", "new_vessel_supply", "demand_slowdown"),
        planned_queries=("해운 운임 overcapacity 4C 리포트", "컨테이너 운임 계약운임 spot rate PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="DIGITAL_ASSET_TOKENIZATION",
        canonical_archetype=E2RArchetype.THEME_VALUATION_OVERHEAT,
        priority=Round19Priority.REDTEAM_DEFENSE,
        why_it_matters="스테이블코인/STO는 규제·실제 수익모델 없이는 테마 premium이다.",
        must_have_evidence=("regulated_revenue", "license_or_partner", "transaction_volume", "cash_flow"),
        red_flag_evidence=("law_headline_only", "no_revenue", "security_risk", "theme_price_only"),
        planned_queries=("스테이블코인 STO 규제 수익모델 거래량 리포트", "토큰증권 실제 매출 라이선스 PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="ROBOTICS_REVENUE_CONVERSION",
        canonical_archetype=E2RArchetype.ROBOTICS_FACTORY_AUTOMATION,
        priority=Round19Priority.REDTEAM_DEFENSE,
        why_it_matters="로봇은 대기업 투자만으로 Green이 아니라 실제 매출, 반복수요, OPM 전환이 필요하다.",
        must_have_evidence=("customer_order", "revenue_conversion", "repeat_revenue", "opm_improvement"),
        red_flag_evidence=("mou_only", "tam_without_revenue", "valuation_overheat", "order_delay"),
        planned_queries=("로봇 수주 매출 전환 OPM 리포트", "휴머노이드 로봇 TAM 무실적 테마 반례"),
    ),
    Round19DeepSearchTarget(
        target_id="PLATFORM_GOVERNANCE_MONETIZATION",
        canonical_archetype=E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        priority=Round19Priority.REDTEAM_DEFENSE,
        why_it_matters="플랫폼은 MAU보다 ARPU/OPM/FCF와 거버넌스 리스크가 Stage를 가른다.",
        must_have_evidence=("arpu", "take_rate", "opm", "fcf", "governance_risk_low"),
        red_flag_evidence=("mau_only", "ai_cost_overrun", "legal_governance_issue", "regulatory_risk"),
        planned_queries=("플랫폼 ARPU OPM FCF 거버넌스 리스크 리포트", "카카오 거버넌스 리스크 valuation rerating 반례"),
    ),
    Round19DeepSearchTarget(
        target_id="WASTE_RECYCLING_ENVIRONMENT",
        canonical_archetype=E2RArchetype.UTILITIES_REGULATED_TARIFF,
        priority=Round19Priority.THIN_BACKFILL,
        why_it_matters="폐기물/재활용은 처리량, 가동률, 가격, FCF가 있어야 정책 테마를 넘는다.",
        must_have_evidence=("processing_volume", "utilization", "pricing", "fcf_after_capex"),
        red_flag_evidence=("policy_headline_only", "capex_without_fcf", "utilization_down"),
        planned_queries=("폐기물 재활용 처리량 가동률 FCF 리포트", "폐배터리 재활용 volume utilization margin PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="CRO_CLINICAL_SERVICE",
        canonical_archetype=E2RArchetype.CDMO_HEALTHCARE_CONTRACT,
        priority=Round19Priority.THIN_BACKFILL,
        why_it_matters="CRO는 임상 뉴스가 아니라 서비스 계약, 임상 물량, 가동률, 마진으로 본다.",
        must_have_evidence=("service_contract", "clinical_volume", "utilization", "opm_fcf_conversion"),
        red_flag_evidence=("trial_delay", "customer_concentration", "volume_without_margin"),
        planned_queries=("CRO 임상서비스 계약 물량 가동률 리포트", "임상시험 수탁 서비스 OPM FCF PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="DIGITAL_HEALTHCARE_AI",
        canonical_archetype=E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT,
        priority=Round19Priority.THIN_BACKFILL,
        why_it_matters="디지털 헬스케어 AI는 허가/수가/반복매출 없이 AI 키워드만 있으면 부족하다.",
        must_have_evidence=("approval", "reimbursement_or_paid_usage", "recurring_revenue", "hospital_adoption"),
        red_flag_evidence=("pilot_only", "no_reimbursement", "ai_keyword_only"),
        planned_queries=("디지털 헬스케어 AI 허가 수가 병원 도입 리포트", "의료 AI 반복매출 OPM PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="SECURITY_IDENTITY_DEEPFAKE",
        canonical_archetype=E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        priority=Round19Priority.THIN_BACKFILL,
        why_it_matters="보안/딥페이크는 규제 수요와 반복계약이 있어야 테마가 아니라 매출이 된다.",
        must_have_evidence=("recurring_contract", "security_demand", "regulatory_demand", "op_eps_revision"),
        red_flag_evidence=("theme_only_security", "budget_cut", "churn", "no_recurring_revenue"),
        planned_queries=("딥페이크 보안 반복계약 규제수요 리포트", "IT보안 매출 성장 OPM recurring contract PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="CLOUD_AI_SOFTWARE_INFRA",
        canonical_archetype=E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        priority=Round19Priority.THIN_BACKFILL,
        why_it_matters="클라우드/AI SW는 사용량이 유료 매출과 OPM으로 전환되는지 확인해야 한다.",
        must_have_evidence=("recurring_revenue", "paid_usage", "arpu", "opm_leverage"),
        red_flag_evidence=("mau_without_monetization", "ai_cost_overrun", "churn"),
        planned_queries=("클라우드 AI SaaS recurring revenue ARPU OPM 리포트", "AI 소프트웨어 유료 사용량 FCF PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="APPAREL_BRAND_OEM",
        canonical_archetype=E2RArchetype.EXPORT_RECURRING_CONSUMER,
        priority=Round19Priority.THIN_BACKFILL,
        why_it_matters="의류 브랜드/OEM은 주문 visibility, 재고, 브랜드 momentum과 마진을 같이 봐야 한다.",
        must_have_evidence=("order_visibility", "brand_momentum", "inventory_status", "opm_improvement"),
        red_flag_evidence=("inventory_build", "single_brand_fad", "margin_squeeze"),
        planned_queries=("의류 OEM 주문 재고 OPM 리포트", "의류 브랜드 수출 반복주문 inventory PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="BUILDING_MATERIALS_CYCLE",
        canonical_archetype=E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT,
        priority=Round19Priority.THIN_BACKFILL,
        why_it_matters="건자재는 건설 경기보다 가격전가, 원가, 물량, PF 노출을 분리해야 한다.",
        must_have_evidence=("volume", "price_pass_through", "cost_spread", "cash_flow"),
        red_flag_evidence=("construction_slowdown", "cost_inflation", "pf_exposure"),
        planned_queries=("건자재 가격전가 원가 스프레드 리포트", "시멘트 건자재 물량 현금흐름 PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="REIT_DEVELOPMENT_TRUST",
        canonical_archetype=E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE,
        priority=Round19Priority.THIN_BACKFILL,
        why_it_matters="리츠/부동산 신탁은 배당률보다 금리, 임대율, 자산가치, 차입 리파이낸싱이 중요하다.",
        must_have_evidence=("occupancy", "rental_income", "refinancing_cost", "nav_discount"),
        red_flag_evidence=("rate_up", "vacancy_up", "asset_impairment", "refinancing_stress"),
        planned_queries=("리츠 임대율 차입 리파이낸싱 NAV 리포트", "부동산신탁 credit risk 배당 PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="RAIL_INFRASTRUCTURE",
        canonical_archetype=E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,
        priority=Round19Priority.THIN_BACKFILL,
        why_it_matters="철도 인프라는 정책명이 아니라 funded project, confirmed order, margin visibility가 필요하다.",
        must_have_evidence=("funded_project", "confirmed_order", "delivery_schedule", "margin_visibility"),
        red_flag_evidence=("policy_headline_only", "project_delay", "low_margin_order"),
        planned_queries=("철도 인프라 수주 funded project margin 리포트", "철도 차량 신호 시스템 장기계약 PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="SERVICE_KIOSK_AUTOMATION",
        canonical_archetype=E2RArchetype.ROBOTICS_FACTORY_AUTOMATION,
        priority=Round19Priority.THIN_BACKFILL,
        why_it_matters="키오스크/자동화는 설치 대수보다 반복 서비스 매출과 유지보수 margin이 중요하다.",
        must_have_evidence=("installed_base", "recurring_service_revenue", "maintenance_margin", "customer_retention"),
        red_flag_evidence=("hardware_one_time_sale", "churn", "low_margin_installation"),
        planned_queries=("키오스크 자동화 반복 서비스 매출 OPM 리포트", "서비스 자동화 유지보수 매출 PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="URBAN_AIR_DRONE",
        canonical_archetype=E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,
        priority=Round19Priority.THIN_BACKFILL,
        why_it_matters="드론/UAM은 방산·상업 수주와 규제승인이 없으면 미래 TAM에 그친다.",
        must_have_evidence=("government_or_commercial_order", "revenue_conversion", "regulatory_approval"),
        red_flag_evidence=("mou_only", "regulatory_delay", "tam_without_revenue"),
        planned_queries=("드론 방산 수주 매출 전환 리포트", "UAM 규제 승인 상업 수주 PDF"),
    ),
    Round19DeepSearchTarget(
        target_id="POLICY_EVENT_DISASTER_THEMES",
        canonical_archetype=E2RArchetype.ONE_OFF_EVENT_DEMAND,
        priority=Round19Priority.EVENT_POLICY_GUARDRAIL,
        why_it_matters="남북경협, 재건, 전염병, 재난 테마는 대부분 event premium이라 4B/4C 방어가 우선이다.",
        must_have_evidence=("binding_policy_or_contract", "revenue_visibility", "funding", "duration"),
        red_flag_evidence=("headline_only", "temporary_demand", "no_revenue", "policy_delay"),
        planned_queries=("정책 이벤트 테마 매출화 실패 반례", "전염병 진단 일회성 수요 EPS 정상화 사례"),
    ),
)


def round19_theme_absorption_summary(
    *,
    raw_tags_path: str | Path = ROUND19_DEFAULT_RAW_TAGS,
    theme_map_path: str | Path = ROUND19_DEFAULT_THEME_MAP,
) -> Mapping[str, int | bool]:
    """Summarize whether the raw theme map itself is absorbed."""

    raw_tags = load_raw_theme_tags(raw_tags_path)
    entries = load_theme_tag_map(theme_map_path)
    audit = audit_theme_tag_coverage(raw_tags, entries)
    return {
        "raw_theme_tags": audit.total_raw_tags,
        "mapped_theme_tags": audit.mapped_tags,
        "unmatched_theme_tags": audit.unmatched_count,
        "ambiguous_theme_tags": audit.ambiguous_count,
        "theme_absorption_ready": audit.unmatched_count == 0,
    }


def round19_target_statuses(
    records: Iterable[E2RCaseRecord],
    *,
    min_positive_cases: int = 2,
    min_counterexamples: int = 2,
    targets: Iterable[Round19DeepSearchTarget] = ROUND19_DEEP_SEARCH_TARGETS,
) -> tuple[Round19TargetStatus, ...]:
    """Evaluate Round-19 targets against current case coverage and price gaps."""

    record_tuple = tuple(records)
    coverage_by_key = {
        row.archetype: row
        for row in coverage_by_archetype(
            record_tuple,
            min_positive_cases=min_positive_cases,
            min_counterexamples=min_counterexamples,
        )
    }
    statuses: list[Round19TargetStatus] = []
    for target in targets:
        coverage = coverage_by_key.get(target.canonical_archetype)
        positive_count = coverage.positive_count if coverage else 0
        counter_count = coverage.counterexample_count if coverage else 0
        total_count = coverage.total_count if coverage else 0
        effective_min_positive = 0 if target.priority == Round19Priority.EVENT_POLICY_GUARDRAIL else min_positive_cases
        missing_positive = max(0, effective_min_positive - positive_count)
        missing_counter = max(0, min_counterexamples - counter_count)
        price_gap = _price_gap_count(record_tuple, target.canonical_archetype)
        readiness = _readiness_status(
            missing_positive_cases=missing_positive,
            missing_counterexamples=missing_counter,
            price_gap_count=price_gap,
        )
        statuses.append(
            Round19TargetStatus(
                target=target,
                positive_count=positive_count,
                counterexample_count=counter_count,
                total_count=total_count,
                missing_positive_cases=missing_positive,
                missing_counterexamples=missing_counter,
                price_gap_count=price_gap,
                readiness_status=readiness,
                recommended_next_step=_recommended_next_step(readiness, target.priority),
            )
        )
    return tuple(statuses)


def round19_readiness_summary(
    *,
    case_library_path: str | Path = ROUND19_DEFAULT_CASE_LIBRARY,
    raw_tags_path: str | Path = ROUND19_DEFAULT_RAW_TAGS,
    theme_map_path: str | Path = ROUND19_DEFAULT_THEME_MAP,
) -> Mapping[str, int | bool | str]:
    records = load_case_library(case_library_path)
    theme = round19_theme_absorption_summary(raw_tags_path=raw_tags_path, theme_map_path=theme_map_path)
    statuses = round19_target_statuses(records)
    return {
        **theme,
        "case_count": len(records),
        "deep_search_targets": len(statuses),
        "targets_needing_deep_search": sum(1 for status in statuses if status.readiness_status == "needs_success_counterexample_deep_search"),
        "targets_needing_price_validation": sum(1 for status in statuses if status.readiness_status == "needs_price_path_validation"),
        "targets_ready_for_shadow_review": sum(1 for status in statuses if status.readiness_status == "shadow_profile_ready_for_review"),
        "production_scoring_changed": False,
        "production_scoring_ready": False,
        "reason": "theme_absorption_ready_but_case_price_validation_incomplete",
    }


def render_round19_readiness_report(
    *,
    case_library_path: str | Path = ROUND19_DEFAULT_CASE_LIBRARY,
    raw_tags_path: str | Path = ROUND19_DEFAULT_RAW_TAGS,
    theme_map_path: str | Path = ROUND19_DEFAULT_THEME_MAP,
) -> str:
    summary = round19_readiness_summary(
        case_library_path=case_library_path,
        raw_tags_path=raw_tags_path,
        theme_map_path=theme_map_path,
    )
    records = load_case_library(case_library_path)
    statuses = round19_target_statuses(records)
    lines = [
        "# Round-19 Deep Search Readiness",
        "",
        f"- source_round: `{ROUND19_SOURCE_ROUND_PATH}`",
        f"- raw_theme_tags: {summary['raw_theme_tags']}",
        f"- mapped_theme_tags: {summary['mapped_theme_tags']}",
        f"- unmatched_theme_tags: {summary['unmatched_theme_tags']}",
        f"- ambiguous_theme_tags: {summary['ambiguous_theme_tags']}",
        f"- theme_absorption_ready: {str(summary['theme_absorption_ready']).lower()}",
        f"- case_count: {summary['case_count']}",
        f"- deep_search_targets: {summary['deep_search_targets']}",
        f"- targets_needing_deep_search: {summary['targets_needing_deep_search']}",
        f"- targets_needing_price_validation: {summary['targets_needing_price_validation']}",
        f"- targets_ready_for_shadow_review: {summary['targets_ready_for_shadow_review']}",
        f"- production_scoring_changed: {str(summary['production_scoring_changed']).lower()}",
        f"- production_scoring_ready: {str(summary['production_scoring_ready']).lower()}",
        f"- readiness_reason: `{summary['reason']}`",
        "",
        "## Interpretation",
        "- 테마 흡수 구조는 동작한다. 예: `스테이블코인`도 검색/라우팅 태그로는 흡수된다.",
        "- 하지만 점수는 테마명이 아니라 실제 증거에서 나와야 한다. 예: 규제 승인, 실제 거래량, 수익모델이 없으면 Green 근거가 아니다.",
        "- 현재 단계는 shadow scoring과 case validation이다. Production StageClassifier/score weight는 변경하지 않는다.",
        "",
        "## Priority Targets",
        "",
        "| target | canonical | priority | positive | counter | price gaps | status | next step |",
        "|---|---|---|---:|---:|---:|---|---|",
    ]
    for status in statuses:
        lines.append(
            "| "
            f"{status.target.target_id} | "
            f"{status.target.canonical_archetype.value} | "
            f"{status.target.priority.value} | "
            f"{status.positive_count} | "
            f"{status.counterexample_count} | "
            f"{status.price_gap_count} | "
            f"{status.readiness_status} | "
            f"{status.recommended_next_step} |"
        )
    lines.extend(
        [
            "",
            "## Research Loop",
            "1. Audit unmatched/ambiguous theme tags.",
            "2. Deep-search under-covered archetypes only.",
            "3. Add success and counterexample cases with must-have/red-flag evidence.",
            "4. Backfill stage-date price paths and MFE/MAE.",
            "5. Run shadow score profiles and compare score-price alignment.",
            "6. Recalibrate weak archetypes before any production scoring change.",
            "",
            "## What Not To Change",
            "- Do not lower Stage 3-Green thresholds to improve recall.",
            "- Do not use raw theme tags as score evidence.",
            "- Do not use case labels or benchmark labels as candidate-generation input.",
            "- Do not fabricate OpenDART detail fields, report numbers, dates, or prices.",
            "- Do not apply score_weight_profiles_v05 to production scoring yet.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_round19_deep_search_readiness_reports(
    *,
    case_library_path: str | Path = ROUND19_DEFAULT_CASE_LIBRARY,
    raw_tags_path: str | Path = ROUND19_DEFAULT_RAW_TAGS,
    theme_map_path: str | Path = ROUND19_DEFAULT_THEME_MAP,
    output_directory: str | Path = ROUND19_DEFAULT_OUTPUT_DIRECTORY,
) -> dict[str, Path]:
    """Write Round-19 report-only outputs."""

    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    records = load_case_library(case_library_path)
    statuses = round19_target_statuses(records)
    paths = {
        "summary": output / "round19_deep_search_readiness.md",
        "targets": output / "round19_undercovered_archetype_priority.csv",
        "plan": output / "round19_deep_search_plan.csv",
        "price_gaps": output / "round19_price_validation_gap.csv",
        "blockers": output / "round19_production_scoring_blockers.md",
    }
    paths["summary"].write_text(
        render_round19_readiness_report(
            case_library_path=case_library_path,
            raw_tags_path=raw_tags_path,
            theme_map_path=theme_map_path,
        ),
        encoding="utf-8",
    )
    _write_status_rows(statuses, paths["targets"])
    _write_plan_rows(statuses, paths["plan"])
    _write_price_gap_rows(records, paths["price_gaps"])
    paths["blockers"].write_text(_render_blockers(statuses), encoding="utf-8")
    return paths


def _write_status_rows(statuses: Iterable[Round19TargetStatus], path: Path) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = (
            "target_id",
            "canonical_archetype",
            "priority",
            "positive_count",
            "counterexample_count",
            "total_count",
            "missing_positive_cases",
            "missing_counterexamples",
            "price_gap_count",
            "readiness_status",
            "recommended_next_step",
            "must_have_evidence",
            "red_flag_evidence",
            "planned_queries",
        )
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for status in statuses:
            writer.writerow(status.as_row())
    return path


def _write_plan_rows(statuses: Iterable[Round19TargetStatus], path: Path) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("target_id", "priority", "canonical_archetype", "query", "purpose", "guardrail"),
        )
        writer.writeheader()
        for status in statuses:
            for query in status.target.planned_queries:
                writer.writerow(
                    {
                        "target_id": status.target.target_id,
                        "priority": status.target.priority.value,
                        "canonical_archetype": status.target.canonical_archetype.value,
                        "query": query,
                        "purpose": "case_success_counterexample_deep_search",
                        "guardrail": "do_not_use_theme_or_case_label_as_score_evidence",
                    }
                )
    return path


def _write_price_gap_rows(records: Iterable[E2RCaseRecord], path: Path) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("case_id", "symbol", "company_name", "primary_archetype", "price_validation_status"),
        )
        writer.writeheader()
        for record in records:
            status = record.price_validation.price_validation_status
            if status == "price_filled":
                continue
            writer.writerow(
                {
                    "case_id": record.case_id,
                    "symbol": record.symbol,
                    "company_name": record.company_name,
                    "primary_archetype": record.primary_archetype.value,
                    "price_validation_status": status,
                }
            )
    return path


def _render_blockers(statuses: Iterable[Round19TargetStatus]) -> str:
    rows = tuple(statuses)
    needs_deep_search = tuple(row for row in rows if row.readiness_status == "needs_success_counterexample_deep_search")
    needs_price = tuple(row for row in rows if row.readiness_status == "needs_price_path_validation")
    lines = [
        "# Round-19 Production Scoring Blockers",
        "",
        "- production_scoring_changed: false",
        "- production_scoring_ready: false",
        "",
        "## Main Blockers",
        f"- targets_needing_success_counterexample_deep_search: {len(needs_deep_search)}",
        f"- targets_needing_price_path_validation: {len(needs_price)}",
        "",
        "## Deep Search First",
    ]
    for row in needs_deep_search:
        lines.append(
            f"- {row.target.target_id}: needs +{row.missing_positive_cases} positive, "
            f"+{row.missing_counterexamples} counterexample case(s)"
        )
    lines.extend(["", "## Price Validation First"])
    for row in needs_price:
        lines.append(f"- {row.target.target_id}: {row.price_gap_count} case(s) still need price-path validation")
    lines.extend(
        [
            "",
            "## Guardrail",
            "Theme absorption is like putting books on the right shelves. It does not prove the books are correct.",
            "Score normalization needs the actual pages: evidence fields, stage dates, price paths, and counterexamples.",
        ]
    )
    return "\n".join(lines) + "\n"


def _price_gap_count(records: tuple[E2RCaseRecord, ...], archetype: E2RArchetype) -> int:
    return sum(
        1
        for record in records
        if record.primary_archetype == archetype and record.price_validation.price_validation_status != "price_filled"
    )


def _readiness_status(
    *,
    missing_positive_cases: int,
    missing_counterexamples: int,
    price_gap_count: int,
) -> str:
    if missing_positive_cases or missing_counterexamples:
        return "needs_success_counterexample_deep_search"
    if price_gap_count:
        return "needs_price_path_validation"
    return "shadow_profile_ready_for_review"


def _recommended_next_step(readiness_status: str, priority: Round19Priority) -> str:
    if readiness_status == "needs_success_counterexample_deep_search":
        if priority == Round19Priority.REDTEAM_DEFENSE:
            return "add_counterexamples_and_4b_4c_cases_first"
        if priority == Round19Priority.THIN_BACKFILL:
            return "add_2_positive_and_2_counterexample_case_candidates"
        return "add_missing_success_or_counterexample_cases"
    if readiness_status == "needs_price_path_validation":
        return "backfill_stage_prices_mfe_mae_before_shadow_weight_review"
    return "shadow_score_review_only_no_production_change"


__all__ = [
    "ROUND19_DEEP_SEARCH_TARGETS",
    "ROUND19_DEFAULT_CASE_LIBRARY",
    "ROUND19_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND19_DEFAULT_RAW_TAGS",
    "ROUND19_DEFAULT_THEME_MAP",
    "ROUND19_SOURCE_ROUND_PATH",
    "Round19DeepSearchTarget",
    "Round19Priority",
    "Round19TargetStatus",
    "render_round19_readiness_report",
    "round19_readiness_summary",
    "round19_target_statuses",
    "round19_theme_absorption_summary",
    "write_round19_deep_search_readiness_reports",
]
