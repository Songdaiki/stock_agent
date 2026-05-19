"""Round-204 R13 Loop-7 cross-archetype RedTeam price validation pack.

Round 204 is a calibration-only cross-sector review. It does not add a new
sector; it judges whether R1-R12 Stage 3, 4B, and 4C calls match later price
paths and hard evidence.

Simple example: a resource-discovery headline can move Korea Gas 30% intraday.
That is price-before-evidence. It stays Stage 1/4B-watch until drilling,
commerciality, development plan, revenue conversion, and cash-flow evidence
are visible as-of the case date.

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


ROUND204_SOURCE_ROUND_PATH = "docs/round/round_204.md"
ROUND204_LARGE_SECTOR = "CROSS_ARCHETYPE_OVERLAY"
ROUND204_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round204_r13_loop7_cross_archetype_price_validation"
ROUND204_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r13_loop7_round204.jsonl"
ROUND204_DEFAULT_AUDIT_PATH = "data/sector_taxonomy/round204_r13_loop7_cross_archetype_price_validation_audit.json"

ROUND204_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "STRUCTURAL_SUCCESS_ALIGNED": E2RArchetype.STRUCTURAL_SUCCESS_ALIGNED.value,
    "STRUCTURAL_SUCCESS_BUT_4B_WATCH": E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH.value,
    "SECTOR_SUCCESS_BUT_4B_WATCH": E2RArchetype.SECTOR_SUCCESS_BUT_4B_WATCH.value,
    "CROWDED_RERATING_4B_WATCH": E2RArchetype.CROWDED_RERATING_4B_WATCH.value,
    "PRICE_ONLY_RALLY": E2RArchetype.PRICE_ONLY_RALLY.value,
    "EVENT_PREMIUM": E2RArchetype.EVENT_PREMIUM.value,
    "FALSE_POSITIVE_SCORE": E2RArchetype.FALSE_POSITIVE_SCORE.value,
    "EVIDENCE_GOOD_BUT_PRICE_FAILED": E2RArchetype.EVIDENCE_GOOD_BUT_PRICE_FAILED.value,
    "THESIS_BREAK_4C": E2RArchetype.THESIS_BREAK_4C.value,
    "OPERATIONAL_TRUST_BREAK": E2RArchetype.OPERATIONAL_TRUST_BREAK.value,
    "LEGAL_REGULATORY_REDTEAM": E2RArchetype.LEGAL_REGULATORY_REDTEAM.value,
    "LEVERAGE_FCF_BREAKDOWN": E2RArchetype.LEVERAGE_FCF_BREAKDOWN.value,
    "COMMERCIALIZATION_FAILURE": E2RArchetype.COMMERCIALIZATION_FAILURE.value,
    "DISCLOSURE_CONFIDENCE_CAP": E2RArchetype.DISCLOSURE_CONFIDENCE_CAP.value,
    "CIRCULAR_AI_FINANCING_WATCH": E2RArchetype.CIRCULAR_AI_FINANCING_WATCH.value,
    "UNKNOWN_INSUFFICIENT_EVIDENCE": E2RArchetype.UNKNOWN_INSUFFICIENT_EVIDENCE.value,
}

ROUND204_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "cross_evidence_confirmed",
    "eps_fcf_durability_confirmed",
    "structural_visibility_confirmed",
    "price_path_alignment_confirmed",
    "not_price_only_rally",
    "no_hard_redteam",
    "not_saturated_4b",
    "revenue_or_eps_conversion_confirmed",
)

ROUND204_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "policy_news_only",
    "resource_estimate_without_commerciality",
    "ai_capex_or_partnership_without_revenue",
    "contract_headline_without_calloff",
    "media_or_event_price_rally",
    "high_score_without_price_validation",
    "past_winner_similarity",
    "price_rally_before_evidence",
    "saturated_4b",
    "hard_redteam",
)

ROUND204_STAGE4B_STATUSES: tuple[str, ...] = ("none", "watch", "elevated", "graduated")

ROUND204_HARD_4C_GATES: tuple[str, ...] = (
    "fatal_safety_accident",
    "consumer_trust_break",
    "regulatory_safety_probe",
    "operational_system_review",
    "contract_cancellation",
    "contract_value_collapse",
    "customer_strategy_pullback",
    "ev_demand_slowdown",
    "gwh_calloff_failure",
    "accounting_or_disclosure_trust_break",
    "legal_regulatory_break",
    "commercialization_failure",
    "cashflow_or_leverage_breakdown",
)

ROUND204_PRICE_VALIDATION_FIELDS: tuple[str, ...] = (
    "price_data_source",
    "full_ohlc_available",
    "reported_price_anchor",
    "reported_return_anchor",
    "stage3_price",
    "stage4b_price",
    "stage4c_price",
    "peak_price",
    "reported_mfe_minimum_pct",
    "reported_market_cap_mfe_minimum_pct",
    "mfe_1d",
    "mfe_30d",
    "mfe_90d",
    "mfe_180d",
    "mfe_1y",
    "mfe_2y",
    "mae_1d",
    "mae_30d",
    "mae_90d",
    "drawdown_after_peak",
    "below_stage3_price_flag",
    "contract_value_before",
    "contract_value_after",
    "contract_value_drawdown_pct",
    "lost_expected_revenue",
    "lost_revenue_vs_prior_revenue_pct",
    "price_validation_status",
)


@dataclass(frozen=True)
class Round204ScoreAdjustment:
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
class Round204CaseCandidate:
    case_id: str
    symbol: str
    company_name: str
    source_sector: str
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
    reported_mfe_minimum_pct: float | None
    reported_market_cap_mfe_minimum_pct: float | None
    mfe_1d: float | None
    mae_1d: float | None
    stage3_price_anchor: float | None
    peak_price_anchor: float | None
    stage4c_price_anchor: float | None
    contract_value_drawdown_pct: float | None
    lost_revenue_vs_prior_revenue_pct: float | None
    score_price_alignment: str
    rerating_result: str
    stage_failure_type: str
    price_validation_status: str
    notes: str

    @property
    def large_sector(self) -> str:
        return ROUND204_LARGE_SECTOR

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND204_SCORE_ADJUSTMENTS: tuple[Round204ScoreAdjustment, ...] = (
    Round204ScoreAdjustment("price_path_alignment", 5, "raise", "Stage 3 이후 실제 대형 MFE가 확인된 케이스를 보상한다."),
    Round204ScoreAdjustment("stage3_to_large_mfe_confirmation", 5, "raise", "SK하이닉스와 한화에어로스페이스처럼 Stage 3 이후 큰 가격경로가 확인되어야 한다."),
    Round204ScoreAdjustment("cross_evidence", 4, "raise", "섹터별 증거가 가격경로와 RedTeam을 함께 통과해야 한다."),
    Round204ScoreAdjustment("eps_fcf_durability", 4, "raise", "대형 rerating은 EPS/FCF 지속성이 확인되어야 한다."),
    Round204ScoreAdjustment("contract_quality", 5, "raise", "계약 cancellation과 value collapse를 피하려면 계약 질을 강하게 봐야 한다."),
    Round204ScoreAdjustment("capacity_bottleneck", 4, "raise", "HBM/방산 같은 성공 케이스는 병목과 visibility가 같이 있었다."),
    Round204ScoreAdjustment("customer_visibility", 4, "raise", "고객 수요와 납품/공급 visibility가 Stage 3 이후 MFE를 설명한다."),
    Round204ScoreAdjustment("operational_trust", 5, "raise", "제주항공 같은 operational trust break는 hard 4C 기준점이다."),
    Round204ScoreAdjustment("hard_4c_early_warning", 5, "raise", "계약취소·안전사고·공시신뢰 훼손은 빠르게 hard 4C로 잡아야 한다."),
    Round204ScoreAdjustment("policy_news_only", -5, "lower", "정책 뉴스만으로 Stage 3-Green을 만들지 않는다."),
    Round204ScoreAdjustment("resource_estimate_without_commerciality", -5, "lower", "자원 추정은 상업성 확인 전까지 price-only event다."),
    Round204ScoreAdjustment("ai_capex_or_partnership_without_revenue", -4, "lower", "AI 투자·파트너십은 매출과 마진 전까지 Stage 2 watch다."),
    Round204ScoreAdjustment("contract_headline_without_calloff", -5, "lower", "계약 headline은 call-off/GWh/margin 전까지 Green 충분조건이 아니다."),
    Round204ScoreAdjustment("media_or_event_price_rally", -5, "lower", "언론/이벤트 급등은 evidence-before-price가 아니면 4B-watch 우선이다."),
    Round204ScoreAdjustment("high_score_without_price_validation", -5, "lower", "높은 점수도 가격경로·4B·4C 검증을 통과해야 한다."),
    Round204ScoreAdjustment("past_winner_similarity", -4, "lower", "과거 성공 종목과 닮았다는 이유만으로 Green을 만들지 않는다."),
)


ROUND204_CASE_CANDIDATES: tuple[Round204CaseCandidate, ...] = (
    Round204CaseCandidate(
        case_id="r13_sk_hynix_hbm_4b_benchmark",
        symbol="000660",
        company_name="SK하이닉스",
        source_sector="R2",
        primary_archetype=E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH,
        secondary_archetypes=(E2RArchetype.MEMORY_HBM_CAPACITY, E2RArchetype.CROWDED_RERATING_4B_WATCH),
        case_type="structural_success",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=date(2026, 5, 14),
        stage4c_date=None,
        stage3_decision="success_benchmark_but_new_calls_after_market_cap_milestone_should_be_4b_watch_not_fresh_stage3",
        stage4b_status="elevated",
        hard_4c_confirmed=False,
        evidence_fields=("hbm_demand", "memory_price_recovery", "capacity_bottleneck", "customer_visibility", "reported_2025_return_274pct", "reported_2026_ytd_return_over_200pct"),
        red_flag_fields=("market_cap_one_trillion_watch", "crowding_watch", "ai_capex_dependency", "consensus_saturation_watch"),
        price_data_source="Reuters reported return path",
        reported_price_anchor="market cap below $100B to about $942B",
        reported_return_anchor="2025 +274%; 2026 to 2026-05-14 >+200%",
        reported_mfe_minimum_pct=1022.0,
        reported_market_cap_mfe_minimum_pct=842.0,
        mfe_1d=None,
        mae_1d=None,
        stage3_price_anchor=None,
        peak_price_anchor=None,
        stage4c_price_anchor=None,
        contract_value_drawdown_pct=None,
        lost_revenue_vs_prior_revenue_pct=None,
        score_price_alignment="aligned",
        rerating_result="true_rerating",
        stage_failure_type="green_success",
        price_validation_status="reported_return_anchor_not_full_ohlc",
        notes="Stage 3 success benchmark; by 2026-05-14 the proper posture is 4B-watch/elevated, not a new Green call.",
    ),
    Round204CaseCandidate(
        case_id="r13_hanwha_aerospace_defense_mfe_4b",
        symbol="012450",
        company_name="한화에어로스페이스",
        source_sector="R1",
        primary_archetype=E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH,
        secondary_archetypes=(E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG, E2RArchetype.CROWDED_RERATING_4B_WATCH),
        case_type="structural_success",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=date(2025, 3, 21),
        stage4c_date=None,
        stage3_decision="large_mfe_success_benchmark_but_capital_raise_after_big_rerating_is_4b_watch_not_hard_4c",
        stage4b_status="elevated",
        hard_4c_confirmed=False,
        evidence_fields=("defense_backlog", "export_contract_visibility", "reported_stage3_anchor_187500", "reported_peak_1435000", "reported_mfe_665pct"),
        red_flag_fields=("large_capital_raise_after_rerating", "dilution_watch", "crowding_watch", "not_automatic_4c"),
        price_data_source="FT/Reuters reported price anchors",
        reported_price_anchor="187,500 KRW to 1,435,000 KRW",
        reported_return_anchor="+665.3% from reported anchor to reported peak; -13% on capital raise event",
        reported_mfe_minimum_pct=665.3,
        reported_market_cap_mfe_minimum_pct=None,
        mfe_1d=None,
        mae_1d=-13.0,
        stage3_price_anchor=187500.0,
        peak_price_anchor=1435000.0,
        stage4c_price_anchor=None,
        contract_value_drawdown_pct=None,
        lost_revenue_vs_prior_revenue_pct=None,
        score_price_alignment="aligned",
        rerating_result="true_rerating",
        stage_failure_type="green_success",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="Large MFE confirms the structural defense case; the capital raise shock is 4B-watch/elevated, not a hard thesis break.",
    ),
    Round204CaseCandidate(
        case_id="r13_kogas_resource_price_only",
        symbol="036460",
        company_name="한국가스공사",
        source_sector="R11",
        primary_archetype=E2RArchetype.PRICE_ONLY_RALLY,
        secondary_archetypes=(E2RArchetype.DOMESTIC_RESOURCE_DISCOVERY_EVENT, E2RArchetype.EVENT_PREMIUM),
        case_type="event_premium",
        stage1_date=date(2024, 6, 3),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=date(2024, 6, 3),
        stage4c_date=None,
        stage3_decision="blocked_until_drilling_commerciality_development_plan_revenue_conversion_and_cash_flow_are_visible",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("east_sea_resource_discovery_headline", "drilling_approval", "intraday_peak_38700", "intraday_mfe_30pct"),
        red_flag_fields=("resource_estimate_without_commerciality", "policy_news_only", "price_rally_before_evidence", "drilling_result_absent"),
        price_data_source="WSJ intraday price anchor",
        reported_price_anchor="38,700 KRW event-day intraday peak",
        reported_return_anchor="+30% intraday",
        reported_mfe_minimum_pct=30.0,
        reported_market_cap_mfe_minimum_pct=None,
        mfe_1d=30.0,
        mae_1d=None,
        stage3_price_anchor=None,
        peak_price_anchor=38700.0,
        stage4c_price_anchor=None,
        contract_value_drawdown_pct=None,
        lost_revenue_vs_prior_revenue_pct=None,
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="false_yellow",
        price_validation_status="event_anchor_not_stage3",
        notes="Resource estimate and drilling approval are not commerciality; this is Stage 1/4B-watch, not Green evidence.",
    ),
    Round204CaseCandidate(
        case_id="r13_samsung_sds_kkr_ai_cb_event",
        symbol="018260",
        company_name="삼성SDS",
        source_sector="R8",
        primary_archetype=E2RArchetype.PRICE_ONLY_RALLY,
        secondary_archetypes=(E2RArchetype.AI_CLOUD_CAPITAL_ALLOCATION, E2RArchetype.CIRCULAR_AI_FINANCING_WATCH, E2RArchetype.EVENT_PREMIUM),
        case_type="success_candidate",
        stage1_date=None,
        stage2_date=date(2026, 4, 15),
        stage3_date=None,
        stage4b_date=date(2026, 4, 15),
        stage4c_date=None,
        stage3_decision="stage2_watch_until_enterprise_ai_revenue_margin_recurring_cloud_revenue_and_fcf_are_visible",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("kkr_convertible_bond_820m", "ai_infrastructure_capital_allocation", "mna_advice", "intraday_mfe_20_8pct"),
        red_flag_fields=("ai_capex_or_partnership_without_revenue", "convertible_bond_dilution_watch", "mna_hope_without_integration", "price_rally_before_evidence"),
        price_data_source="Reuters intraday return anchor",
        reported_price_anchor="exact price unavailable",
        reported_return_anchor="+20.8% intraday",
        reported_mfe_minimum_pct=20.8,
        reported_market_cap_mfe_minimum_pct=None,
        mfe_1d=20.8,
        mae_1d=None,
        stage3_price_anchor=None,
        peak_price_anchor=None,
        stage4c_price_anchor=None,
        contract_value_drawdown_pct=None,
        lost_revenue_vs_prior_revenue_pct=None,
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="stage2_watch_success",
        price_validation_status="event_anchor_not_stage3",
        notes="AI infrastructure investment and CB financing can be Stage 2 watch, but not Stage 3 until revenue, margin, recurring cloud revenue, and FCF appear.",
    ),
    Round204CaseCandidate(
        case_id="r13_jeju_air_fatal_crash_hard_4c",
        symbol="089590",
        company_name="제주항공",
        source_sector="R9",
        primary_archetype=E2RArchetype.OPERATIONAL_TRUST_BREAK,
        secondary_archetypes=(E2RArchetype.THESIS_BREAK_4C, E2RArchetype.LEGAL_REGULATORY_REDTEAM),
        case_type="4c_thesis_break",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2024, 12, 30),
        stage3_decision="not_applicable_operational_trust_break_is_hard_4c",
        stage4b_status="none",
        hard_4c_confirmed=True,
        evidence_fields=("fatal_crash", "record_low_6920", "intraday_mae_15_7pct", "government_safety_probe"),
        red_flag_fields=("fatal_safety_accident", "consumer_trust_break", "regulatory_safety_probe", "operational_system_review"),
        price_data_source="Reuters intraday price anchor",
        reported_price_anchor="6,920 KRW record low",
        reported_return_anchor="-15.7% intraday",
        reported_mfe_minimum_pct=None,
        reported_market_cap_mfe_minimum_pct=None,
        mfe_1d=None,
        mae_1d=-15.7,
        stage3_price_anchor=None,
        peak_price_anchor=None,
        stage4c_price_anchor=6920.0,
        contract_value_drawdown_pct=None,
        lost_revenue_vs_prior_revenue_pct=None,
        score_price_alignment="aligned",
        rerating_result="thesis_break",
        stage_failure_type="should_have_been_red",
        price_validation_status="reported_intraday_anchor",
        notes="Fatal safety accident and safety probe are hard 4C operational trust evidence.",
    ),
    Round204CaseCandidate(
        case_id="r13_lges_contract_cancellation_4c",
        symbol="373220",
        company_name="LG에너지솔루션",
        source_sector="R3",
        primary_archetype=E2RArchetype.THESIS_BREAK_4C,
        secondary_archetypes=(E2RArchetype.BATTERY_CONTRACT_DISCLOSURE_CONFIDENCE, E2RArchetype.DISCLOSURE_CONFIDENCE_CAP),
        case_type="4c_thesis_break",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 12, 18),
        stage3_decision="contract_headline_should_be_blocked_until_calloff_gwh_margin_and_fcf_are_confirmed",
        stage4b_status="none",
        hard_4c_confirmed=True,
        evidence_fields=("ford_ev_battery_supply_deal_cancelled", "freudenberg_order_terminated", "lost_expected_revenue_13_5t_krw", "intraday_mae_7_6pct"),
        red_flag_fields=("contract_cancellation", "customer_strategy_pullback", "ev_demand_slowdown", "contract_headline_without_calloff"),
        price_data_source="Reuters intraday return and lost revenue anchors",
        reported_price_anchor="exact price unavailable",
        reported_return_anchor="-7.6% intraday on Ford cancellation",
        reported_mfe_minimum_pct=None,
        reported_market_cap_mfe_minimum_pct=None,
        mfe_1d=None,
        mae_1d=-7.6,
        stage3_price_anchor=None,
        peak_price_anchor=None,
        stage4c_price_anchor=None,
        contract_value_drawdown_pct=None,
        lost_revenue_vs_prior_revenue_pct=52.7,
        score_price_alignment="aligned",
        rerating_result="thesis_break",
        stage_failure_type="should_have_been_red",
        price_validation_status="reported_intraday_anchor",
        notes="Ford and Freudenberg cancellations remove about KRW13.5T expected revenue, over half of 2024 revenue.",
    ),
    Round204CaseCandidate(
        case_id="r13_lnf_tesla_contract_value_collapse",
        symbol="066970",
        company_name="L&F",
        source_sector="R3",
        primary_archetype=E2RArchetype.THESIS_BREAK_4C,
        secondary_archetypes=(E2RArchetype.BATTERY_CONTRACT_DISCLOSURE_CONFIDENCE, E2RArchetype.DISCLOSURE_CONFIDENCE_CAP),
        case_type="4c_thesis_break",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 12, 29),
        stage3_decision="contract_value_collapse_is_hard_4c_and_prevents_contract_headline_green",
        stage4b_status="none",
        hard_4c_confirmed=True,
        evidence_fields=("tesla_cathode_contract_value_collapse", "contract_value_2_9b_to_7386", "ev_demand_slowdown", "4680_production_difficulty"),
        red_flag_fields=("contract_value_collapse", "customer_strategy_pullback", "ev_demand_slowdown", "gwh_calloff_failure"),
        price_data_source="Reuters contract-value anchor",
        reported_price_anchor="stock OHLC unavailable",
        reported_return_anchor="contract value $2.9B to $7,386",
        reported_mfe_minimum_pct=None,
        reported_market_cap_mfe_minimum_pct=None,
        mfe_1d=None,
        mae_1d=None,
        stage3_price_anchor=None,
        peak_price_anchor=None,
        stage4c_price_anchor=None,
        contract_value_drawdown_pct=-99.999745,
        lost_revenue_vs_prior_revenue_pct=None,
        score_price_alignment="aligned",
        rerating_result="thesis_break",
        stage_failure_type="should_have_been_red",
        price_validation_status="contract_value_anchor_stock_ohlc_unavailable",
        notes="Tesla deal value collapsed from $2.9B to $7,386; contract headlines require call-off, GWh, margin, and FCF checks.",
    ),
    Round204CaseCandidate(
        case_id="r13_hanwha_aerospace_capital_raise_4b_not_4c",
        symbol="012450",
        company_name="한화에어로스페이스 증자 overlay",
        source_sector="R1/R13",
        primary_archetype=E2RArchetype.CROWDED_RERATING_4B_WATCH,
        secondary_archetypes=(E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH, E2RArchetype.LEVERAGE_FCF_BREAKDOWN),
        case_type="4b_watch",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=date(2025, 3, 21),
        stage4c_date=None,
        stage3_decision="capital_raise_after_big_rally_is_4b_watch_or_elevated_unless_backlog_eps_or_thesis_breaks",
        stage4b_status="elevated",
        hard_4c_confirmed=False,
        evidence_fields=("capital_raise_3_6t_krw", "share_price_down_13pct", "overseas_factory_and_partner_investment", "backlog_thesis_alive"),
        red_flag_fields=("dilution_watch", "capital_allocation_watch", "not_automatic_4c", "crowding_watch"),
        price_data_source="FT/Reuters event return",
        reported_price_anchor="exact price unavailable",
        reported_return_anchor="-13% on capital raise announcement",
        reported_mfe_minimum_pct=None,
        reported_market_cap_mfe_minimum_pct=None,
        mfe_1d=None,
        mae_1d=-13.0,
        stage3_price_anchor=None,
        peak_price_anchor=None,
        stage4c_price_anchor=None,
        contract_value_drawdown_pct=None,
        lost_revenue_vs_prior_revenue_pct=None,
        score_price_alignment="aligned",
        rerating_result="true_rerating",
        stage_failure_type="green_success",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="Dilution after a large rally is 4B-watch/elevated while backlog and EPS thesis remain alive; it is not automatic hard 4C.",
    ),
)


def round204_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND204_CASE_CANDIDATES:
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
                "Round204 R13 Loop-7 cross-archetype RedTeam, 4B, 4C, and "
                "price-path validation case. This is calibration-only and must "
                "not be used for candidate generation."
            ),
            stage1_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "headline" in field
                or "approval" in field
                or "policy" in field
                or "reported" in field
                or "intraday" in field
                or "demand" in field
            ),
            stage2_evidence=candidate.evidence_fields if candidate.stage2_date else (),
            stage3_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "hbm" in field
                or "backlog" in field
                or "customer" in field
                or "capacity" in field
                or "contract_visibility" in field
            ),
            stage4b_evidence=tuple(
                field
                for field in (*candidate.evidence_fields, *candidate.red_flag_fields)
                if "return" in field
                or "rally" in field
                or "crowding" in field
                or "market_cap" in field
                or "dilution" in field
                or "capital_raise" in field
                or "price_rally" in field
            ),
            stage4c_evidence=tuple(
                field
                for field in candidate.red_flag_fields
                if "break" in field
                or "cancellation" in field
                or "collapse" in field
                or "accident" in field
                or "trust" in field
                or "probe" in field
                or "slowdown" in field
                or "calloff" in field
            ),
            must_have_fields=ROUND204_GREEN_REQUIRED_FIELDS,
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
                "price_path_alignment_delta": 5.0,
                "large_mfe_confirmation_delta": 5.0,
                "hard_4c_early_warning_delta": 5.0,
                "contract_quality_delta": 5.0,
                "operational_trust_delta": 5.0,
                "policy_news_only_delta": -5.0,
                "price_only_rally_delta": -5.0,
                "contract_headline_without_calloff_delta": -5.0,
                "ai_capex_or_partnership_without_revenue_delta": -4.0,
                "past_winner_similarity_delta": -4.0,
            },
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "full_ohlc_complete_false",
                "price_validation_partial_with_reported_price_anchors",
                "do_not_invent_price_or_stage_dates",
                "do_not_treat_price_only_event_policy_ai_or_contract_headline_as_green_evidence",
                *ROUND204_GREEN_REQUIRED_FIELDS,
                *ROUND204_GREEN_FORBIDDEN_PATTERNS,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(
                stage3_price=candidate.stage3_price_anchor,
                stage4c_price=candidate.stage4c_price_anchor,
                peak_price=candidate.peak_price_anchor,
                peak_return_from_stage3=candidate.reported_mfe_minimum_pct,
                mfe_1y=candidate.reported_mfe_minimum_pct,
                mae_30d=candidate.mae_1d,
                price_validation_status=candidate.price_validation_status,
            ),
            data_quality=CaseDataQuality(
                official_data_available=True,
                report_data_available=True,
                price_data_available=False,
                stage_dates_confidence=0.85 if candidate.stage4b_date or candidate.stage4c_date else 0.6,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round204_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND204_CASE_CANDIDATES:
        rows.append(
            {
                "case_id": candidate.case_id,
                "symbol": candidate.symbol,
                "company_name": candidate.company_name,
                "source_sector": candidate.source_sector,
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
                "reported_mfe_minimum_pct": _float_text(candidate.reported_mfe_minimum_pct),
                "reported_market_cap_mfe_minimum_pct": _float_text(candidate.reported_market_cap_mfe_minimum_pct),
                "mfe_1d": _float_text(candidate.mfe_1d),
                "mae_1d": _float_text(candidate.mae_1d),
                "contract_value_drawdown_pct": _float_text(candidate.contract_value_drawdown_pct),
                "lost_revenue_vs_prior_revenue_pct": _float_text(candidate.lost_revenue_vs_prior_revenue_pct),
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


def round204_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND204_SCORE_ADJUSTMENTS)


def round204_price_validation_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round204_price_validation": "true"} for field in ROUND204_PRICE_VALIDATION_FIELDS)


def round204_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {"round204_label": label, "canonical_archetype": canonical}
        for label, canonical in ROUND204_REQUIRED_TARGET_ALIASES.items()
    )


def round204_summary() -> dict[str, int | bool | str]:
    cases = round204_case_records()
    return {
        "case_candidate_count": len(cases),
        "required_target_count": len(ROUND204_REQUIRED_TARGET_ALIASES),
        "score_adjustment_count": len(ROUND204_SCORE_ADJUSTMENTS),
        "price_validation_field_count": len(ROUND204_PRICE_VALIDATION_FIELDS),
        "structural_success_count": sum(1 for case in cases if case.case_type == "structural_success"),
        "event_premium_count": sum(1 for case in cases if case.case_type == "event_premium"),
        "hard_4c_case_count": sum(1 for case in ROUND204_CASE_CANDIDATES if case.hard_4c_confirmed),
        "stage3_case_count": sum(1 for case in ROUND204_CASE_CANDIDATES if case.stage3_date),
        "stage4b_watch_or_elevated_count": sum(
            1 for case in ROUND204_CASE_CANDIDATES if case.stage4b_status in {"watch", "elevated"}
        ),
        "reported_price_anchor_count": sum(
            1 for case in ROUND204_CASE_CANDIDATES if case.price_validation_status != "needs_ohlc_backfill"
        ),
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
        "price_validation_completed": "partial_with_reported_price_anchors",
        "full_ohlc_complete": False,
    }


def write_round204_r13_loop7_reports(
    *,
    output_directory: str | Path = ROUND204_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND204_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND204_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    cases = write_case_library(round204_case_records(), cases_path)
    audit = Path(audit_path)
    audit.parent.mkdir(parents=True, exist_ok=True)
    paths = {
        "cases": cases,
        "audit_json": audit,
        "summary": output / "round204_r13_loop7_price_validation_summary.md",
        "case_matrix": output / "round204_r13_loop7_case_matrix.csv",
        "target_aliases": output / "round204_r13_loop7_target_aliases.csv",
        "score_adjustments": output / "round204_r13_loop7_score_adjustments.csv",
        "price_validation_fields": output / "round204_r13_loop7_price_validation_fields.csv",
        "green_gate_review": output / "round204_r13_loop7_green_gate_review.md",
        "price_validation_plan": output / "round204_r13_loop7_price_validation_plan.md",
        "stage4b_4c_review": output / "round204_r13_loop7_stage4b_4c_review.md",
    }
    audit.write_text(json.dumps(round204_audit_payload(), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_rows(round204_case_rows(), paths["case_matrix"])
    _write_rows(round204_target_alias_rows(), paths["target_aliases"])
    _write_rows(round204_score_adjustment_rows(), paths["score_adjustments"])
    _write_rows(round204_price_validation_field_rows(), paths["price_validation_fields"])
    paths["summary"].write_text(render_round204_summary_markdown(), encoding="utf-8")
    paths["green_gate_review"].write_text(render_round204_green_gate_review_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round204_price_validation_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round204_stage4b_4c_review_markdown(), encoding="utf-8")
    return paths


def round204_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND204_SOURCE_ROUND_PATH,
        "large_sector": ROUND204_LARGE_SECTOR,
        "summary": round204_summary(),
        "target_aliases": list(round204_target_alias_rows()),
        "green_required_fields": list(ROUND204_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND204_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_statuses": list(ROUND204_STAGE4B_STATUSES),
        "hard_4c_gates": list(ROUND204_HARD_4C_GATES),
        "score_adjustments": list(round204_score_adjustment_rows()),
        "case_ids": [case.case_id for case in ROUND204_CASE_CANDIDATES],
        "what_not_to_change": [
            "do_not_apply_to_production_scoring_yet",
            "do_not_use_round204_cases_as_candidate_generation_input",
            "do_not_lower_stage3_green_thresholds",
            "do_not_treat_price_only_event_policy_ai_or_contract_headline_as_green_evidence",
            "do_not_invent_full_ohlc_or_stage_prices_when_only_reported_anchors_exist",
            "keep_full_ohlc_complete_false_until_official_backfill_is_done",
        ],
    }


def render_round204_summary_markdown() -> str:
    summary = round204_summary()
    lines = [
        "# Round-204 R13 Loop-7 Price-Path Validation Summary",
        "",
        f"- source_round: `{ROUND204_SOURCE_ROUND_PATH}`",
        "- large_sector: `CROSS_ARCHETYPE_OVERLAY`",
        "- scope: Stage 3 success, 4B timing, price-only rally, event premium, hard 4C, contract quality, and operational trust",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- required_target_count: {summary['required_target_count']}",
        f"- score_adjustment_count: {summary['score_adjustment_count']}",
        f"- price_validation_field_count: {summary['price_validation_field_count']}",
        f"- structural_success_count: {summary['structural_success_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- hard_4c_case_count: {summary['hard_4c_case_count']}",
        f"- stage3_case_count: {summary['stage3_case_count']}",
        f"- stage4b_watch_or_elevated_count: {summary['stage4b_watch_or_elevated_count']}",
        f"- reported_price_anchor_count: {summary['reported_price_anchor_count']}",
        "- production_scoring_changed: false",
        "- candidate_generation_input: false",
        "- shadow_weight_only: true",
        "- price_validation_completed: partial_with_reported_price_anchors",
        "- full_ohlc_complete: false",
        "",
        "## Interpretation",
        "",
        "- SK하이닉스와 한화에어로스페이스는 Stage 3가 대형 MFE를 잡을 수 있음을 보여주는 aligned success benchmark다.",
        "- SK하이닉스는 2026-05-14 기준 신규 Green보다 4B-watch/elevated로 보는 게 맞다.",
        "- 한화에어로스페이스 증자 충격은 4B-watch/elevated이지 backlog/EPS thesis가 살아 있으면 hard 4C가 아니다.",
        "- 한국가스공사와 삼성SDS는 가격이 증거보다 먼저 간 이벤트라 Green을 막아야 한다.",
        "- 제주항공 fatal crash는 operational trust hard 4C다.",
        "- LGES와 L&F는 계약 취소와 계약가치 붕괴 hard 4C 기준점이다.",
        "",
        "쉬운 예: `as_of_date=2026-04-15`에 삼성SDS가 KKR CB와 AI 인프라 기대감으로 장중 급등해도, AI 매출·마진·반복 cloud revenue가 없으면 Stage 3-Green이 아니라 Stage 2/4B-watch다.",
    ]
    return "\n".join(lines) + "\n"


def render_round204_green_gate_review_markdown() -> str:
    lines = [
        "# Round-204 R13 Loop-7 Green Gate Review",
        "",
        "## Green Required Evidence",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND204_GREEN_REQUIRED_FIELDS)
    lines.extend(["", "## Green Forbidden Patterns", ""])
    lines.extend(f"- `{field}`" for field in ROUND204_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(["", "## Shadow Score Adjustments", "", "| axis | direction | points | reason |", "| --- | --- | ---: | --- |"])
    for adjustment in ROUND204_SCORE_ADJUSTMENTS:
        lines.append(f"| `{adjustment.axis}` | {adjustment.direction} | {adjustment.points} | {adjustment.reason} |")
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not apply these weights to production scoring yet.",
            "- Do not use Round204 cases as candidate-generation input.",
            "- Do not lower Stage 3-Green thresholds to force promotion.",
            "- Do not invent full OHLC, stage prices, or MFE/MAE when only reported anchors exist.",
            "- Do not treat price-only rallies, policy events, AI partnership/capex plans, or contract headlines as Green evidence alone.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round204_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-204 R13 Loop-7 Price Validation Plan",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND204_PRICE_VALIDATION_FIELDS)
    lines.extend(["", "## Case Anchors", "", "| case | price data source | reported anchor | status |", "| --- | --- | --- | --- |"])
    for case in ROUND204_CASE_CANDIDATES:
        lines.append(
            f"| `{case.case_id}` | {case.price_data_source} | {case.reported_return_anchor} | `{case.price_validation_status}` |"
        )
    lines.extend(
        [
            "",
            "## Backfill Rule",
            "",
            "- Use reported Reuters/FT/WSJ anchors only for fields they explicitly support.",
            "- Keep full OHLC fields unavailable until KRX/Naver/Yahoo adjusted daily bars are backfilled.",
            "- Split Stage 3 anchor, 4B event, 4C event, and contract-value collapse date.",
            "- Do not create a Stage 3 anchor when the case intentionally has no Stage 3 date.",
            "- Price-only rally cases must remain Stage 1/4B-watch until revenue/EPS evidence appears.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round204_stage4b_4c_review_markdown() -> str:
    lines = [
        "# Round-204 R13 Loop-7 Stage 4B / 4C Review",
        "",
        "## 4B Status Definitions",
        "",
        "- `watch`: Stage 3 success has produced a large MFE, or price moves before full evidence.",
        "- `elevated`: valuation/crowding/capital raise/market-cap milestone risk is high while core thesis may remain alive.",
        "- `graduated`: new evidence no longer moves price and the old frame is fully replaced.",
        "",
        "## Hard 4C Gates",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND204_HARD_4C_GATES)
    lines.extend(
        [
            "",
            "## R13 Interpretation",
            "",
            "- 4B is not automatic hard 4C. Dilution after a large rally is 4B-watch/elevated unless backlog, EPS, or trust breaks.",
            "- Operational trust breaks and fatal safety accidents are hard 4C.",
            "- Contract cancellation and contract-value collapse are hard 4C.",
            "- Price-only policy, resource, or AI events are Stage 1/Stage 2 plus 4B-watch, not Green.",
            "",
            "## Case Review",
            "",
            "| case | 4B status | hard 4C confirmed | interpretation |",
            "| --- | --- | --- | --- |",
        ]
    )
    for case in ROUND204_CASE_CANDIDATES:
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


def _float_text(value: float | None) -> str:
    return "" if value is None else str(value)


__all__ = [
    "ROUND204_CASE_CANDIDATES",
    "ROUND204_DEFAULT_AUDIT_PATH",
    "ROUND204_DEFAULT_CASES_PATH",
    "ROUND204_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND204_GREEN_FORBIDDEN_PATTERNS",
    "ROUND204_GREEN_REQUIRED_FIELDS",
    "ROUND204_HARD_4C_GATES",
    "ROUND204_PRICE_VALIDATION_FIELDS",
    "ROUND204_REQUIRED_TARGET_ALIASES",
    "ROUND204_SCORE_ADJUSTMENTS",
    "ROUND204_SOURCE_ROUND_PATH",
    "ROUND204_STAGE4B_STATUSES",
    "Round204CaseCandidate",
    "Round204ScoreAdjustment",
    "render_round204_green_gate_review_markdown",
    "render_round204_price_validation_plan_markdown",
    "render_round204_stage4b_4c_review_markdown",
    "render_round204_summary_markdown",
    "round204_audit_payload",
    "round204_case_records",
    "round204_case_rows",
    "round204_price_validation_field_rows",
    "round204_score_adjustment_rows",
    "round204_summary",
    "round204_target_alias_rows",
    "write_round204_r13_loop7_reports",
]
