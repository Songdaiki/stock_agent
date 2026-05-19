"""Round-217 R13 Loop-8 cross-archetype RedTeam price validation pack.

Round 217 is calibration/evaluation material only. It puts Stage 3 success,
4B-watch, hard 4C, and price-moved-without-evidence cases in one table.

Easy example: SK Hynix can validate a real Stage 3 success because HBM demand,
OP revision, and the later price path line up. Korea Gas cannot become Green
from an oil/gas discovery headline because commerciality and revenue evidence
were not visible when the price moved.
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


ROUND217_SOURCE_ROUND_PATH = "docs/round/round_217.md"
ROUND217_LARGE_SECTOR = "CROSS_ARCHETYPE_REDTEAM_PRICE_VALIDATION"
ROUND217_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round217_r13_loop8_cross_archetype_price_validation"
ROUND217_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r13_loop8_round217.jsonl"
ROUND217_DEFAULT_AUDIT_PATH = "data/sector_taxonomy/round217_r13_loop8_cross_archetype_price_validation_audit.json"

ROUND217_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "STRUCTURAL_SUCCESS_ALIGNED": E2RArchetype.STRUCTURAL_SUCCESS_ALIGNED.value,
    "STRUCTURAL_SUCCESS_BUT_4B_WATCH": E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH.value,
    "CROWDED_RERATING_4B_WATCH": E2RArchetype.CROWDED_RERATING_4B_WATCH.value,
    "PRICE_ONLY_RALLY": E2RArchetype.PRICE_ONLY_RALLY.value,
    "EVENT_PREMIUM": E2RArchetype.EVENT_PREMIUM.value,
    "FALSE_POSITIVE_SCORE": E2RArchetype.FALSE_POSITIVE_SCORE.value,
    "EVIDENCE_GOOD_BUT_PRICE_FAILED": E2RArchetype.EVIDENCE_GOOD_BUT_PRICE_FAILED.value,
    "THESIS_BREAK_4C": E2RArchetype.THESIS_BREAK_4C.value,
    "OPERATIONAL_TRUST_BREAK": E2RArchetype.OPERATIONAL_TRUST_BREAK.value,
    "CONTRACT_QUALITY_BREAK": E2RArchetype.CONTRACT_QUALITY_BREAK.value,
    "GOVERNANCE_DILUTION_EVENT": E2RArchetype.GOVERNANCE_DILUTION_EVENT.value,
    "LEGAL_REGULATORY_REDTEAM": E2RArchetype.LEGAL_REGULATORY_REDTEAM.value,
    "MARKET_STRUCTURE_WATCH": E2RArchetype.MARKET_STRUCTURE_WATCH.value,
    "ORDER_TO_REVENUE_CONVERSION": E2RArchetype.ORDER_TO_REVENUE_CONVERSION.value,
    "KRW_STABLECOIN_POLICY_THEME": E2RArchetype.KRW_STABLECOIN_POLICY_THEME.value,
    "STRATEGIC_MATERIALS_WITH_GOVERNANCE_OVERLAY": E2RArchetype.STRATEGIC_MATERIALS_WITH_GOVERNANCE_OVERLAY.value,
    "UNKNOWN_INSUFFICIENT_EVIDENCE": E2RArchetype.UNKNOWN_INSUFFICIENT_EVIDENCE.value,
}

ROUND217_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "company_level_evidence_confirmed",
    "revenue_eps_fcf_path_confirmed",
    "price_path_after_evidence_confirmed",
    "meaningful_stage3_mfe_confirmed",
    "mae_not_excessive",
    "not_saturated_4b",
    "no_hard_redteam",
    "contract_operational_governance_trust_passed",
)

ROUND217_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "policy_news_only",
    "resource_estimate_without_commerciality",
    "stablecoin_policy_theme_only",
    "ai_capex_or_partnership_without_revenue",
    "contract_headline_without_calloff",
    "mou_or_preliminary_deal",
    "governance_premium_only",
    "dilution_without_clear_fcf",
    "high_score_without_price_validation",
    "price_rally_before_evidence",
)

ROUND217_STAGE4B_WATCH_TRIGGERS: tuple[str, ...] = (
    "stage3_return_2x_to_5x_or_more",
    "market_cap_milestone_headline",
    "large_capital_raise_cb_or_share_issue",
    "event_day_20_to_30pct_rally",
    "policy_mou_resource_or_stablecoin_theme_rally",
    "good_news_price_response_fade",
    "valuation_ahead_of_evidence",
)

ROUND217_HARD_4C_GATES: tuple[str, ...] = (
    "contract_cancellation",
    "contract_value_collapse",
    "fatal_safety_accident",
    "operational_trust_break",
    "major_governance_legal_break",
    "privacy_or_security_trust_break",
    "pf_workout_or_credit_break",
    "regulatory_reversal",
    "commercialization_failure",
    "financing_failure",
)

ROUND217_PRICE_VALIDATION_FIELDS: tuple[str, ...] = (
    "price_data_source",
    "full_ohlc_available",
    "reported_price_anchor",
    "reported_return_anchor",
    "stage1_price",
    "stage2_price",
    "stage3_price",
    "stage4b_price",
    "stage4c_price",
    "peak_price",
    "peak_return_from_stage3_pct",
    "mfe_1d",
    "mae_1d",
    "reported_return_2025_pct",
    "reported_return_2026_ytd_pct",
    "market_cap_mfe_minimum_pct",
    "contract_value_drawdown_pct",
    "lost_revenue_vs_prior_revenue_pct",
    "event_mfe_pct",
    "event_mae_pct",
    "price_validation_status",
)


@dataclass(frozen=True)
class Round217ScoreAdjustment:
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
class Round217ShadowWeightRow:
    archetype: E2RArchetype
    price_path_alignment: int
    stage3_mfe_confirmation: int
    order_to_revenue: int
    eps_fcf_revision: int
    actual_contract: int
    contract_quality: int
    operational_trust: int
    event_penalty: int
    governance_redteam: int
    stage4b_watch_sensitivity: int
    hard_4c_sensitivity: int
    notes: str

    def as_row(self) -> dict[str, str]:
        return {
            "archetype": self.archetype.value,
            "price_path_alignment": _signed_int_text(self.price_path_alignment),
            "stage3_mfe_confirmation": _signed_int_text(self.stage3_mfe_confirmation),
            "order_to_revenue": _signed_int_text(self.order_to_revenue),
            "eps_fcf_revision": _signed_int_text(self.eps_fcf_revision),
            "actual_contract": _signed_int_text(self.actual_contract),
            "contract_quality": _signed_int_text(self.contract_quality),
            "operational_trust": _signed_int_text(self.operational_trust),
            "event_penalty": _signed_int_text(self.event_penalty),
            "governance_redteam": _signed_int_text(self.governance_redteam),
            "4b_watch_sensitivity": _signed_int_text(self.stage4b_watch_sensitivity),
            "hard_4c_sensitivity": _signed_int_text(self.hard_4c_sensitivity),
            "notes": self.notes,
        }


@dataclass(frozen=True)
class Round217CaseCandidate:
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
    stage1_price_anchor: float | None
    stage2_price_anchor: float | None
    stage3_price_anchor: float | None
    stage4b_price_anchor: float | None
    stage4c_price_anchor: float | None
    peak_price_anchor: float | None
    reported_mfe_pct: float | None
    reported_market_cap_mfe_pct: float | None
    mfe_1d: float | None
    mae_1d: float | None
    contract_value_drawdown_pct: float | None
    lost_revenue_vs_prior_revenue_pct: float | None
    extra_price_metrics: Mapping[str, float | str | bool]
    score_price_alignment: str
    rerating_result: str
    stage_failure_type: str
    price_validation_status: str
    notes: str

    @property
    def large_sector(self) -> str:
        return ROUND217_LARGE_SECTOR

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND217_SCORE_ADJUSTMENTS: tuple[Round217ScoreAdjustment, ...] = (
    Round217ScoreAdjustment("price_path_alignment", 5, "raise", "Stage 3 이후 가격경로가 증거와 맞으면 보상한다."),
    Round217ScoreAdjustment("stage3_to_large_mfe_confirmation", 5, "raise", "대형 MFE가 확인된 Stage 3 성공 사례를 보상한다."),
    Round217ScoreAdjustment("order_to_revenue_conversion", 5, "raise", "수주 headline보다 납품·매출·OP revision 전환을 우선한다."),
    Round217ScoreAdjustment("eps_fcf_revision", 5, "raise", "OP/EPS/FCF revision이 Stage 3의 몸통이다."),
    Round217ScoreAdjustment("actual_contract", 5, "raise", "실제 계약과 납품 경로가 있으면 visibility가 올라간다."),
    Round217ScoreAdjustment("customer_visibility", 4, "raise", "고객과 공급 visibility가 가격경로와 맞을 때 보상한다."),
    Round217ScoreAdjustment("operational_trust", 5, "raise", "운영 신뢰는 Green의 필수 통과 gate다."),
    Round217ScoreAdjustment("hard_4c_early_warning", 5, "raise", "계약취소·안전사고·신뢰 훼손은 hard 4C로 조기 감지한다."),
    Round217ScoreAdjustment("contract_quality", 5, "raise", "계약금액 headline보다 call-off, take-or-pay, margin, FCF를 확인한다."),
    Round217ScoreAdjustment("policy_news_only", -5, "lower", "정책 뉴스만으로 Green을 만들지 않는다."),
    Round217ScoreAdjustment("resource_estimate_without_commerciality", -5, "lower", "자원 추정은 상업성 전까지 event premium이다."),
    Round217ScoreAdjustment("stablecoin_policy_theme_only", -5, "lower", "스테이블코인 정책 기대는 실제 수익모델 전까지 감점한다."),
    Round217ScoreAdjustment("ai_capex_or_partnership_without_revenue", -4, "lower", "AI 투자·협업은 매출과 마진 전까지 Stage 2 watch다."),
    Round217ScoreAdjustment("contract_headline_without_calloff", -5, "lower", "call-off 없는 계약 headline은 Green 충분조건이 아니다."),
    Round217ScoreAdjustment("mou_or_preliminary_deal", -5, "lower", "MOU·예비계약은 실제 계약 전 Green 금지다."),
    Round217ScoreAdjustment("governance_premium_only", -5, "lower", "지배구조 이벤트 프리미엄만으로 구조적 rerating을 주지 않는다."),
    Round217ScoreAdjustment("dilution_without_clear_fcf", -4, "lower", "FCF 설명 없는 증자·희석은 4B/RedTeam 감점이다."),
    Round217ScoreAdjustment("high_score_without_price_validation", -5, "lower", "높은 shadow score도 가격경로 검증 전에는 보류한다."),
)

ROUND217_SHADOW_WEIGHT_ROWS: tuple[Round217ShadowWeightRow, ...] = (
    Round217ShadowWeightRow(E2RArchetype.STRUCTURAL_SUCCESS_ALIGNED, 5, 5, 5, 5, 4, 3, 3, 0, 0, 4, 2, "SK Hynix and Hyundai Rotem show Stage 3 can create large MFE when evidence converts to earnings/revenue."),
    Round217ShadowWeightRow(E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH, 5, 5, 4, 4, 4, 3, 3, -1, 2, 5, 3, "SK Hynix after market-cap milestone becomes 4B-watch/elevated, not a fresh Green."),
    Round217ShadowWeightRow(E2RArchetype.CAPITAL_ALLOCATION_DILUTION_OVERLAY, 2, 3, 2, 2, 2, 2, 2, -2, 5, 5, 3, "Hanwha Aero capital raise after a large rally is 4B-watch, not automatic hard 4C."),
    Round217ShadowWeightRow(E2RArchetype.PRICE_ONLY_RALLY, 0, 0, 0, 0, 0, 0, 1, -5, 1, 5, 3, "Korea Gas and stablecoin basket show price moved before revenue evidence."),
    Round217ShadowWeightRow(E2RArchetype.CONTRACT_QUALITY_BREAK, 0, 0, 0, 0, 5, 5, 2, 0, 1, 3, 5, "LGES and L&F show cancellation/value collapse hard 4C."),
    Round217ShadowWeightRow(E2RArchetype.OPERATIONAL_TRUST_BREAK, 0, 0, 0, 0, 0, 1, 5, 0, 2, 3, 5, "Jeju Air fatal crash is hard operational trust 4C."),
    Round217ShadowWeightRow(E2RArchetype.KRW_STABLECOIN_POLICY_THEME, 0, 0, 0, 0, 0, 0, 2, -5, 3, 5, 4, "Stablecoin policy rally is not Green until regulated revenue is visible."),
    Round217ShadowWeightRow(E2RArchetype.STRATEGIC_MATERIALS_WITH_GOVERNANCE_OVERLAY, 2, 2, 2, 3, 3, 3, 2, -3, 5, 5, 4, "Korea Zinc strategic project is Stage 2 but governance/dilution blocks Stage 3."),
)

ROUND217_CASE_CANDIDATES: tuple[Round217CaseCandidate, ...] = (
    Round217CaseCandidate(
        case_id="r13_loop8_sk_hynix_hbm_stage3_4b",
        symbol="000660",
        company_name="SK하이닉스",
        source_sector="R2",
        primary_archetype=E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH,
        secondary_archetypes=(E2RArchetype.MEMORY_HBM_CAPACITY, E2RArchetype.STRUCTURAL_SUCCESS_ALIGNED, E2RArchetype.CROWDED_RERATING_4B_WATCH),
        case_type="structural_success",
        stage1_date=None,
        stage2_date=date(2024, 6, 25),
        stage3_date=date(2024, 6, 25),
        stage4b_date=date(2026, 5, 14),
        stage4c_date=None,
        stage3_decision="hbm_dominance_memory_price_upcycle_and_op_revision_aligned_with_later_large_mfe_but_2026_posture_is_4b_watch",
        stage4b_status="elevated",
        hard_4c_confirmed=False,
        evidence_fields=("hbm_dominance", "dram_price_upcycle", "op_revision_2024_30t_2025_53t", "stage3_price_222000", "peak_price_1946000", "market_cap_near_one_trillion_usd"),
        red_flag_fields=("market_cap_milestone_headline", "crowded_rerating_watch", "ai_capex_dependency", "not_fresh_stage3_after_2026_05_14"),
        price_data_source="MarketWatch / Reuters / Tom's Hardware reported anchors",
        reported_price_anchor="222,000 KRW Stage 3 anchor to 1,946,000 KRW reported peak",
        reported_return_anchor="Stage 3 to reported peak +776.6%; 2025 +274%; 2026 YTD >+200%",
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=222000.0,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=1946000.0,
        reported_mfe_pct=776.6,
        reported_market_cap_mfe_pct=842.0,
        mfe_1d=None,
        mae_1d=None,
        contract_value_drawdown_pct=None,
        lost_revenue_vs_prior_revenue_pct=None,
        extra_price_metrics={"reported_return_2025_pct": 274.0, "reported_return_2026_ytd_pct": 200.0, "minimum_compounded_return_from_2025_start_pct": 1022.0},
        score_price_alignment="aligned",
        rerating_result="true_rerating",
        stage_failure_type="green_success",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="HBM와 OP revision이 가격경로와 맞은 Stage 3 성공 benchmark지만 2026년 5월 기준 신규 Green이 아니라 4B-watch다.",
    ),
    Round217CaseCandidate(
        case_id="r13_loop8_hyundai_rotem_k2_delivery_aligned",
        symbol="064350",
        company_name="현대로템",
        source_sector="R1",
        primary_archetype=E2RArchetype.ORDER_TO_REVENUE_CONVERSION,
        secondary_archetypes=(E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG, E2RArchetype.STRUCTURAL_SUCCESS_ALIGNED),
        case_type="structural_success",
        stage1_date=None,
        stage2_date=date(2024, 4, 9),
        stage3_date=date(2024, 4, 9),
        stage4b_date=date(2025, 8, 1),
        stage4c_date=None,
        stage3_decision="k2_delivery_revenue_and_op_revision_aligned_with_price_reaction",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("k2_poland_delivery_18_units", "k2_export_revenue_270b_krw", "op_growth_estimate_85pct", "stage3_price_41300", "poland_second_contract_6_5b_usd"),
        red_flag_fields=("delivery_schedule_watch", "political_export_watch", "cost_overrun_watch"),
        price_data_source="WSJ / Reuters reported price and contract anchors",
        reported_price_anchor="41,300 KRW on 2024-04-09",
        reported_return_anchor="+9.3% event move; KOSPI relative outperformance +9.6pp",
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=41300.0,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        reported_mfe_pct=9.3,
        reported_market_cap_mfe_pct=None,
        mfe_1d=9.3,
        mae_1d=None,
        contract_value_drawdown_pct=None,
        lost_revenue_vs_prior_revenue_pct=None,
        extra_price_metrics={"implied_pre_event_reference_price": 37786.0, "relative_outperformance_vs_kospi_pp": 9.6, "k2_export_revenue_1q_krw_bn": 270.0, "op_growth_estimate_pct": 85.0, "poland_second_contract_usd_bn": 6.5},
        score_price_alignment="aligned",
        rerating_result="true_rerating",
        stage_failure_type="green_success",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="현대로템은 방산 수주 headline보다 납품·매출·OP revision이 Stage 3를 만든다는 기준점이다.",
    ),
    Round217CaseCandidate(
        case_id="r13_loop8_hanwha_aero_dilution_4b_not_4c",
        symbol="012450",
        company_name="한화에어로스페이스",
        source_sector="R1/R13",
        primary_archetype=E2RArchetype.CAPITAL_ALLOCATION_DILUTION_OVERLAY,
        secondary_archetypes=(E2RArchetype.CROWDED_RERATING_4B_WATCH, E2RArchetype.GOVERNANCE_DILUTION_EVENT, E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG),
        case_type="4b_watch",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=date(2025, 3, 21),
        stage4c_date=None,
        stage3_decision="capital_raise_after_large_rerating_is_4b_watch_or_elevated_unless_backlog_eps_or_thesis_breaks",
        stage4b_status="elevated",
        hard_4c_confirmed=False,
        evidence_fields=("capital_raise_3_6t_krw", "event_mae_13pct", "share_sale_price_605000", "discount_to_prior_close_16pct", "pre_event_ytd_more_than_doubled"),
        red_flag_fields=("large_capital_raise_cb_or_share_issue", "dilution_without_clear_fcf", "crowded_rerating_watch", "not_automatic_4c"),
        price_data_source="Reuters / FT reported event anchors",
        reported_price_anchor="3.6T KRW capital raise event; 605,000 KRW share sale price",
        reported_return_anchor="-13% event drawdown; share sale discount -16%; pre-event YTD more than doubled",
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=605000.0,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        reported_mfe_pct=None,
        reported_market_cap_mfe_pct=None,
        mfe_1d=None,
        mae_1d=-13.0,
        contract_value_drawdown_pct=None,
        lost_revenue_vs_prior_revenue_pct=None,
        extra_price_metrics={"capital_raise_krw_trn": 3.6, "discount_to_prior_close_pct": -16.0, "pre_event_ytd_status": "more_than_doubled"},
        score_price_alignment="aligned",
        rerating_result="true_rerating",
        stage_failure_type="green_success",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="대시세 후 증자는 4B-watch/elevated다. 수주·EPS thesis가 살아 있으면 자동 hard 4C가 아니다.",
    ),
    Round217CaseCandidate(
        case_id="r13_loop8_kogas_resource_price_only",
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
        stage3_decision="resource_discovery_event_blocked_until_drilling_commerciality_development_plan_revenue_and_cash_flow_are_visible",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("east_sea_resource_exploration_approval", "possible_14b_barrels", "event_peak_price_38700", "event_mfe_30pct", "drilling_cost_per_attempt_100b_krw"),
        red_flag_fields=("resource_estimate_without_commerciality", "policy_news_only", "price_rally_before_evidence", "drilling_result_absent"),
        price_data_source="WSJ reported intraday price anchor",
        reported_price_anchor="38,700 KRW event-day intraday peak",
        reported_return_anchor="+30% intraday before commerciality evidence",
        stage1_price_anchor=29769.0,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=38700.0,
        stage4c_price_anchor=None,
        peak_price_anchor=38700.0,
        reported_mfe_pct=30.0,
        reported_market_cap_mfe_pct=None,
        mfe_1d=30.0,
        mae_1d=None,
        contract_value_drawdown_pct=None,
        lost_revenue_vs_prior_revenue_pct=None,
        extra_price_metrics={"implied_pre_event_reference_price": 29769.0, "drilling_cost_per_attempt_krw_bn": 100.0},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="false_yellow",
        price_validation_status="reported_event_anchor_not_stage3",
        notes="정책·자원발견 이벤트는 경제성·상업성 전까지 Stage 1/4B-watch이며 Green 금지다.",
    ),
    Round217CaseCandidate(
        case_id="r13_loop8_lges_lnf_contract_quality_4c",
        symbol="373220/066970",
        company_name="LG에너지솔루션 / L&F",
        source_sector="R3",
        primary_archetype=E2RArchetype.CONTRACT_QUALITY_BREAK,
        secondary_archetypes=(E2RArchetype.THESIS_BREAK_4C, E2RArchetype.DISCLOSURE_CONFIDENCE_CAP),
        case_type="4c_thesis_break",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 12, 18),
        stage3_decision="contract_headline_customer_name_and_contract_amount_are_not_green_without_actual_calloff_take_or_pay_gwh_delivery_margin_and_fcf",
        stage4b_status="none",
        hard_4c_confirmed=True,
        evidence_fields=("ford_ev_battery_deal_cancelled", "freudenberg_contract_terminated", "lges_lost_expected_revenue_13_5t_krw", "lnf_tesla_contract_value_2_9b_to_7386_usd"),
        red_flag_fields=("contract_cancellation", "contract_value_collapse", "customer_strategy_pullback", "contract_headline_without_calloff"),
        price_data_source="Reuters reported event return and contract-value anchors",
        reported_price_anchor="LGES -7.6% event move; L&F contract value collapse",
        reported_return_anchor="LGES expected revenue loss 13.5T KRW; L&F $2.9B to $7,386",
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        reported_mfe_pct=None,
        reported_market_cap_mfe_pct=None,
        mfe_1d=None,
        mae_1d=-7.6,
        contract_value_drawdown_pct=-99.999745,
        lost_revenue_vs_prior_revenue_pct=52.7,
        extra_price_metrics={"lges_lost_expected_revenue_krw_trn": 13.5, "lges_2024_revenue_krw_trn": 25.62, "lnf_initial_contract_value_usd_bn": 2.9, "lnf_revised_contract_value_usd": 7386.0},
        score_price_alignment="aligned",
        rerating_result="thesis_break",
        stage_failure_type="should_have_been_red",
        price_validation_status="reported_event_and_contract_anchor_not_full_ohlc",
        notes="계약 headline은 충분조건이 아니다. 계약 취소와 가치 붕괴는 hard 4C다.",
    ),
    Round217CaseCandidate(
        case_id="r13_loop8_jeju_air_operational_trust_hard_4c",
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
        stage3_decision="fatal_accident_is_operational_trust_hard_4c_and_blocks_travel_demand_green",
        stage4b_status="none",
        hard_4c_confirmed=True,
        evidence_fields=("fatal_crash_179_deaths", "record_low_6920", "intraday_mae_15_7pct", "market_cap_wipeout_95_7b_krw"),
        red_flag_fields=("fatal_safety_accident", "operational_trust_break", "major_governance_legal_break", "regulatory_safety_probe"),
        price_data_source="Reuters reported price/event anchors",
        reported_price_anchor="6,920 KRW record low",
        reported_return_anchor="-15.7% intraday; market cap wipeout 95.7B KRW",
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=6920.0,
        peak_price_anchor=None,
        reported_mfe_pct=None,
        reported_market_cap_mfe_pct=None,
        mfe_1d=None,
        mae_1d=-15.7,
        contract_value_drawdown_pct=None,
        lost_revenue_vs_prior_revenue_pct=None,
        extra_price_metrics={"implied_pre_event_reference_price": 8209.0, "market_cap_wipeout_krw_bn": 95.7, "ak_holdings_mae_pct": -12.0, "hanatour_mae_pct": -7.0, "very_good_tour_mae_pct": -11.0},
        score_price_alignment="aligned",
        rerating_result="thesis_break",
        stage_failure_type="should_have_been_red",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="여행수요가 좋아도 fatal safety accident는 operational trust hard 4C다.",
    ),
    Round217CaseCandidate(
        case_id="r13_loop8_stablecoin_theme_price_only",
        symbol="377300/LG_CNS/158430/ME2ON",
        company_name="Kakao Pay / stablecoin basket",
        source_sector="R6",
        primary_archetype=E2RArchetype.KRW_STABLECOIN_POLICY_THEME,
        secondary_archetypes=(E2RArchetype.PRICE_ONLY_RALLY, E2RArchetype.EVENT_PREMIUM, E2RArchetype.MARKET_STRUCTURE_WATCH),
        case_type="overheat",
        stage1_date=date(2025, 6, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=date(2025, 6, 1),
        stage4c_date=None,
        stage3_decision="stablecoin_policy_theme_blocked_until_issuer_license_reserve_income_fee_revenue_and_regulatory_capital_are_visible",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("krw_stablecoin_policy_expectation", "kakao_pay_more_than_double", "lg_cns_70pct", "aton_80pct", "me2on_200pct"),
        red_flag_fields=("stablecoin_policy_theme_only", "policy_news_only", "regulated_revenue_unconfirmed", "issuer_license_unconfirmed", "reserve_income_unconfirmed"),
        price_data_source="FT reported return anchors",
        reported_price_anchor="monthly return anchors only",
        reported_return_anchor="Kakao Pay >+100%, LG CNS +70%, Aton +80%, ME2ON +200%",
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        reported_mfe_pct=200.0,
        reported_market_cap_mfe_pct=None,
        mfe_1d=None,
        mae_1d=None,
        contract_value_drawdown_pct=None,
        lost_revenue_vs_prior_revenue_pct=None,
        extra_price_metrics={"kakao_pay_mfe_month_pct": 100.0, "lg_cns_mfe_month_pct": 70.0, "aton_mfe_month_pct": 80.0, "me2on_mfe_month_pct": 200.0, "regulated_revenue_confirmed": False},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="theme_overheat",
        stage_failure_type="false_yellow",
        price_validation_status="reported_return_anchor_not_full_ohlc",
        notes="스테이블코인 정책 기대는 발행권·reserve income·수수료·규제자본 전까지 Stage 3 금지다.",
    ),
    Round217CaseCandidate(
        case_id="r13_loop8_korea_zinc_strategic_governance_watch",
        symbol="010130",
        company_name="고려아연",
        source_sector="R4",
        primary_archetype=E2RArchetype.STRATEGIC_MATERIALS_WITH_GOVERNANCE_OVERLAY,
        secondary_archetypes=(E2RArchetype.GOVERNANCE_DILUTION_EVENT, E2RArchetype.CAPITAL_ALLOCATION_DILUTION_OVERLAY, E2RArchetype.EVENT_PREMIUM),
        case_type="success_candidate",
        stage1_date=date(2024, 9, 1),
        stage2_date=date(2025, 12, 1),
        stage3_date=None,
        stage4b_date=date(2025, 12, 24),
        stage4c_date=None,
        stage3_decision="strategic_material_project_is_stage2_until_offtake_capex_fcf_dilution_governance_and_execution_clear",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("us_critical_minerals_smelter_7_4b_usd", "share_issue_1_9b_usd", "new_investor_stake_10pct", "event_mfe_5pct"),
        red_flag_fields=("governance_premium_only", "dilution_without_clear_fcf", "governance_battle", "project_execution_watch"),
        price_data_source="Reuters reported event anchors",
        reported_price_anchor="$7.4B smelter project; $1.9B share issue; event +5%",
        reported_return_anchor="U.S. smelter event +5%; YoungPoong event -10.5%",
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        reported_mfe_pct=5.0,
        reported_market_cap_mfe_pct=None,
        mfe_1d=5.0,
        mae_1d=-10.5,
        contract_value_drawdown_pct=None,
        lost_revenue_vs_prior_revenue_pct=None,
        extra_price_metrics={"us_smelter_project_usd_bn": 7.4, "share_issue_for_project_usd_bn": 1.9, "new_investor_stake_pct": 10.0, "youngpoong_event_mae_pct": -10.5},
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="전략광물 프로젝트는 Stage 2 후보지만 offtake, FCF, dilution, governance가 풀리기 전 Stage 3는 보류한다.",
    ),
)


def round217_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND217_CASE_CANDIDATES:
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
                "Round217 R13 Loop-8 cross-archetype price validation case. "
                "Calibration-only; not candidate-generation input."
            ),
            stage1_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "policy" in field
                or "event" in field
                or "approval" in field
                or "headline" in field
                or "expectation" in field
                or "project" in field
            ),
            stage2_evidence=candidate.evidence_fields if candidate.stage2_date else (),
            stage3_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "revision" in field
                or "delivery" in field
                or "revenue" in field
                or "hbm" in field
                or "stage3_price" in field
            ),
            stage4b_evidence=tuple(
                field
                for field in (*candidate.evidence_fields, *candidate.red_flag_fields)
                if "mfe" in field
                or "market_cap" in field
                or "milestone" in field
                or "rally" in field
                or "theme" in field
                or "capital_raise" in field
                or "dilution" in field
                or "crowded" in field
            ),
            stage4c_evidence=tuple(
                field
                for field in candidate.red_flag_fields
                if "cancellation" in field
                or "collapse" in field
                or "accident" in field
                or "trust" in field
                or "legal" in field
                or "reversal" in field
                or "failure" in field
            ),
            must_have_fields=ROUND217_GREEN_REQUIRED_FIELDS,
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
                "stage3_to_large_mfe_confirmation_delta": 5.0,
                "order_to_revenue_conversion_delta": 5.0,
                "eps_fcf_revision_delta": 5.0,
                "contract_quality_delta": 5.0,
                "operational_trust_delta": 5.0,
                "hard_4c_early_warning_delta": 5.0,
                "policy_news_only_delta": -5.0,
                "resource_estimate_without_commerciality_delta": -5.0,
                "stablecoin_policy_theme_only_delta": -5.0,
                "contract_headline_without_calloff_delta": -5.0,
                "dilution_without_clear_fcf_delta": -4.0,
            },
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "full_ohlc_complete_false",
                "price_validation_partial_with_reported_price_anchors",
                "do_not_invent_price_or_stage_dates",
                "do_not_treat_price_only_policy_resource_stablecoin_contract_headline_or_governance_event_as_green",
                *ROUND217_GREEN_REQUIRED_FIELDS,
                *ROUND217_GREEN_FORBIDDEN_PATTERNS,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(
                stage1_price=candidate.stage1_price_anchor,
                stage2_price=candidate.stage2_price_anchor,
                stage3_price=candidate.stage3_price_anchor,
                stage4b_price=candidate.stage4b_price_anchor,
                stage4c_price=candidate.stage4c_price_anchor,
                peak_price=candidate.peak_price_anchor,
                peak_return_from_stage3=candidate.reported_mfe_pct,
                mfe_30d=candidate.mfe_1d,
                mfe_1y=candidate.reported_mfe_pct,
                mae_30d=candidate.mae_1d,
                price_validation_status=candidate.price_validation_status,
            ),
            data_quality=CaseDataQuality(
                official_data_available=True,
                report_data_available=True,
                price_data_available=(
                    candidate.stage1_price_anchor is not None
                    or candidate.stage2_price_anchor is not None
                    or candidate.stage3_price_anchor is not None
                    or candidate.stage4b_price_anchor is not None
                    or candidate.stage4c_price_anchor is not None
                    or candidate.peak_price_anchor is not None
                    or candidate.mfe_1d is not None
                    or candidate.mae_1d is not None
                ),
                stage_dates_confidence=0.85 if candidate.stage4b_date or candidate.stage4c_date or candidate.stage3_date else 0.6,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round217_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND217_CASE_CANDIDATES:
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
                "stage3_price": _float_text(candidate.stage3_price_anchor),
                "stage4b_price": _float_text(candidate.stage4b_price_anchor),
                "stage4c_price": _float_text(candidate.stage4c_price_anchor),
                "peak_price": _float_text(candidate.peak_price_anchor),
                "reported_mfe_pct": _float_text(candidate.reported_mfe_pct),
                "reported_market_cap_mfe_pct": _float_text(candidate.reported_market_cap_mfe_pct),
                "mfe_1d": _float_text(candidate.mfe_1d),
                "mae_1d": _float_text(candidate.mae_1d),
                "contract_value_drawdown_pct": _float_text(candidate.contract_value_drawdown_pct),
                "lost_revenue_vs_prior_revenue_pct": _float_text(candidate.lost_revenue_vs_prior_revenue_pct),
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


def round217_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND217_SCORE_ADJUSTMENTS)


def round217_shadow_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(row.as_row() for row in ROUND217_SHADOW_WEIGHT_ROWS)


def round217_price_validation_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round217_price_validation": "true"} for field in ROUND217_PRICE_VALIDATION_FIELDS)


def round217_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {"round217_label": label, "canonical_archetype": canonical}
        for label, canonical in ROUND217_REQUIRED_TARGET_ALIASES.items()
    )


def round217_summary() -> dict[str, int | bool | str]:
    cases = ROUND217_CASE_CANDIDATES
    return {
        "source_round": ROUND217_SOURCE_ROUND_PATH,
        "large_sector": ROUND217_LARGE_SECTOR,
        "case_candidate_count": len(cases),
        "structural_success_count": sum(1 for case in cases if case.case_type == "structural_success"),
        "event_premium_count": sum(1 for case in cases if case.case_type == "event_premium"),
        "overheat_count": sum(1 for case in cases if case.case_type == "overheat"),
        "watch_count": sum(1 for case in cases if case.case_type == "4b_watch"),
        "hard_4c_case_count": sum(1 for case in cases if case.hard_4c_confirmed),
        "price_moved_without_evidence_count": sum(1 for case in cases if case.score_price_alignment == "price_moved_without_evidence"),
        "aligned_success_count": sum(1 for case in cases if case.score_price_alignment == "aligned" and not case.hard_4c_confirmed),
        "stage3_case_count": sum(1 for case in cases if case.stage3_date is not None),
        "stage4b_watch_or_elevated_count": sum(1 for case in cases if case.stage4b_status in {"watch", "elevated"}),
        "target_archetype_count": len(ROUND217_REQUIRED_TARGET_ALIASES),
        "shadow_weight_row_count": len(ROUND217_SHADOW_WEIGHT_ROWS),
        "price_validation_completed": "partial_with_reported_price_anchors",
        "full_ohlc_complete": False,
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
    }


def round217_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND217_SOURCE_ROUND_PATH,
        "large_sector": ROUND217_LARGE_SECTOR,
        "summary": round217_summary(),
        "target_aliases": dict(ROUND217_REQUIRED_TARGET_ALIASES),
        "green_required_fields": list(ROUND217_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND217_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_watch_triggers": list(ROUND217_STAGE4B_WATCH_TRIGGERS),
        "hard_4c_gates": list(ROUND217_HARD_4C_GATES),
        "score_adjustments": list(round217_score_adjustment_rows()),
        "shadow_weights": list(round217_shadow_weight_rows()),
        "case_ids": [case.case_id for case in ROUND217_CASE_CANDIDATES],
        "what_not_to_change": [
            "do_not_apply_to_production_scoring_yet",
            "do_not_use_round217_cases_as_candidate_generation_input",
            "do_not_lower_stage3_green_thresholds",
            "do_not_treat_price_only_event_policy_resource_stablecoin_or_contract_headline_as_green",
            "do_not_invent_full_ohlc_or_stage_prices_when_only_reported_anchors_exist",
        ],
    }


def render_round217_summary_markdown() -> str:
    summary = round217_summary()
    lines = [
        "# Round 217 R13 Loop 8 Cross-Archetype Price Validation",
        "",
        "This pack is calibration-only. Production scoring and candidate generation are unchanged.",
        "",
        "## Summary",
        "",
        f"- source_round: {summary['source_round']}",
        f"- large_sector: {summary['large_sector']}",
        f"- cases: {summary['case_candidate_count']}",
        f"- structural_success: {summary['structural_success_count']}",
        f"- event_premium: {summary['event_premium_count']}",
        f"- overheat: {summary['overheat_count']}",
        f"- hard_4c: {summary['hard_4c_case_count']}",
        f"- price_moved_without_evidence: {summary['price_moved_without_evidence_count']}",
        f"- Stage 3 dated cases: {summary['stage3_case_count']}",
        f"- 4B watch/elevated cases: {summary['stage4b_watch_or_elevated_count']}",
        "- price_validation_completed: partial_with_reported_price_anchors",
        "- full_ohlc_complete: false",
        "",
        "## Case Matrix",
        "",
        "| case | company | type | stage3 | 4B | 4C | alignment | note |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for case in ROUND217_CASE_CANDIDATES:
        lines.append(
            "| "
            + " | ".join(
                (
                    case.case_id,
                    case.company_name,
                    case.case_type,
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
            "- SK하이닉스와 현대로템은 Stage 3가 실제 대형 MFE나 강한 price reaction을 만들 수 있음을 보여준다.",
            "- 한화에어로스페이스 증자 shock은 4B-watch/elevated이지 자동 hard 4C가 아니다.",
            "- 한국가스공사와 stablecoin basket은 가격이 증거보다 먼저 간 event premium이다.",
            "- LGES/L&F와 제주항공은 계약품질·운영신뢰 hard 4C 기준점이다.",
            "- 고려아연은 전략자원 Stage 2 후보지만 governance/dilution이 풀리기 전 Stage 3 보류다.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round217_green_gate_review_markdown() -> str:
    lines = [
        "# Round 217 R13 Green Gate Review",
        "",
        "Do not apply these weights to production scoring yet.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND217_GREEN_REQUIRED_FIELDS)
    lines.extend(["", "## Forbidden Patterns", ""])
    lines.extend(f"- {field}" for field in ROUND217_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(["", "## Shadow Score Adjustments", "", "| axis | direction | points | reason |", "|---|---|---:|---|"])
    for adjustment in ROUND217_SCORE_ADJUSTMENTS:
        lines.append(f"| {adjustment.axis} | {adjustment.direction} | {adjustment.points} | {adjustment.reason} |")
    lines.extend(
        [
            "",
            "## Easy Examples",
            "- `HBM 수요 + OP revision + 이후 가격경로`는 Stage 3 성공 검증이다.",
            "- `동해 가스 가능성 + 당일 +30%`는 상업성 전 가격 선행 이벤트다.",
            "- `계약 취소 또는 fatal accident`는 구조가 좋아도 hard 4C다.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round217_stage4b_4c_review_markdown() -> str:
    lines = [
        "# Round 217 R13 4B / 4C Review",
        "",
        "## 4B Watch Triggers",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND217_STAGE4B_WATCH_TRIGGERS)
    lines.extend(["", "## Hard 4C Gates", ""])
    lines.extend(f"- {field}" for field in ROUND217_HARD_4C_GATES)
    lines.extend(
        [
            "",
            "## Case Review",
            "",
            "| case | 4B status | hard 4C | interpretation |",
            "|---|---|---|---|",
        ]
    )
    for case in ROUND217_CASE_CANDIDATES:
        lines.append(f"| {case.case_id} | {case.stage4b_status} | {str(case.hard_4c_confirmed).lower()} | {case.notes} |")
    return "\n".join(lines) + "\n"


def render_round217_price_validation_plan_markdown() -> str:
    lines = [
        "# Round 217 R13 Price Validation Plan",
        "",
        "- price_validation_completed: partial_with_reported_price_anchors",
        "- full_ohlc_complete: false",
        "- Do not invent OHLC, stage prices, MFE, or MAE where raw adjusted daily prices are unavailable.",
        "",
        "## Backfill Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND217_PRICE_VALIDATION_FIELDS)
    lines.extend(["", "## Case Anchors", "", "| case | data source | reported anchor | status |", "|---|---|---|---|"])
    for case in ROUND217_CASE_CANDIDATES:
        lines.append(f"| {case.case_id} | {case.price_data_source} | {case.reported_return_anchor} | {case.price_validation_status} |")
    return "\n".join(lines) + "\n"


def write_round217_r13_loop8_reports(
    output_directory: str | Path = ROUND217_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND217_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND217_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)

    paths = {
        "cases": write_case_library(round217_case_records(), cases_path),
        "audit": _write_json(round217_audit_payload(), audit_path),
        "summary": output / "round217_r13_loop8_price_validation_summary.md",
        "case_matrix": output / "round217_r13_loop8_case_matrix.csv",
        "target_aliases": output / "round217_r13_loop8_target_aliases.csv",
        "score_adjustments": output / "round217_r13_loop8_score_adjustments.csv",
        "shadow_weights": output / "round217_r13_loop8_shadow_weights.csv",
        "price_validation_fields": output / "round217_r13_loop8_price_validation_fields.csv",
        "green_gate_review": output / "round217_r13_loop8_green_gate_review.md",
        "price_validation_plan": output / "round217_r13_loop8_price_validation_plan.md",
        "stage4b_4c_review": output / "round217_r13_loop8_stage4b_4c_review.md",
    }
    paths["summary"].write_text(render_round217_summary_markdown(), encoding="utf-8")
    _write_csv(round217_case_rows(), paths["case_matrix"])
    _write_csv(round217_target_alias_rows(), paths["target_aliases"])
    _write_csv(round217_score_adjustment_rows(), paths["score_adjustments"])
    _write_csv(round217_shadow_weight_rows(), paths["shadow_weights"])
    _write_csv(round217_price_validation_field_rows(), paths["price_validation_fields"])
    paths["green_gate_review"].write_text(render_round217_green_gate_review_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round217_price_validation_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round217_stage4b_4c_review_markdown(), encoding="utf-8")
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


def _signed_int_text(value: int) -> str:
    return f"+{value}" if value > 0 else str(value)
