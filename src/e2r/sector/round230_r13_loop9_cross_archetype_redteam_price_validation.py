"""Round-230 R13 Loop-9 cross-archetype RedTeam validation pack.

Round 230 converts ``docs/round/round_230.md`` into structured,
calibration-only case records. It does not change production scoring.

Easy example: SK Hynix shows that a strong Stage 3 can produce very large MFE.
The same case later needs 4B-watch when market-cap headlines and crowding
appear. In contrast, Korea Gas or stablecoin basket rallies before commercial
revenue are price moves without evidence, not Stage 3-Green.
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


ROUND230_SOURCE_ROUND_PATH = "docs/round/round_230.md"
ROUND230_LARGE_SECTOR = "CROSS_ARCHETYPE_REDTEAM_PRICE_VALIDATION"
ROUND230_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round230_r13_loop9_cross_archetype_redteam_price_validation"
ROUND230_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r13_loop9_round230.jsonl"
ROUND230_DEFAULT_AUDIT_PATH = "data/sector_taxonomy/round230_r13_loop9_cross_archetype_redteam_price_validation_audit.json"
ROUND230_DEFAULT_STAGE3_BIAS = "redteam_first_after_price_validation"

ROUND230_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "STRUCTURAL_SUCCESS_ALIGNED": E2RArchetype.STRUCTURAL_SUCCESS_ALIGNED.value,
    "STRUCTURAL_SUCCESS_BUT_4B_WATCH": E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH.value,
    "CROWDED_RERATING_4B_WATCH": E2RArchetype.CROWDED_RERATING_4B_WATCH.value,
    "PRICE_MOVED_WITHOUT_EVIDENCE": E2RArchetype.PRICE_ONLY_RALLY.value,
    "EVENT_PREMIUM": E2RArchetype.EVENT_PREMIUM.value,
    "FALSE_POSITIVE_SCORE": E2RArchetype.FALSE_POSITIVE_SCORE.value,
    "EVIDENCE_GOOD_BUT_PRICE_FAILED": E2RArchetype.EVIDENCE_GOOD_BUT_PRICE_FAILED.value,
    "CONTRACT_QUALITY_BREAK": E2RArchetype.CONTRACT_QUALITY_BREAK.value,
    "OPERATIONAL_TRUST_BREAK": E2RArchetype.OPERATIONAL_TRUST_BREAK.value,
    "SECURITY_PRIVACY_TRUST_BREAK": E2RArchetype.SECURITY_OPERATIONAL_TRUST_OVERLAY.value,
    "POLICY_INDUCED_CAPEX_FAILURE": E2RArchetype.EVIDENCE_GOOD_BUT_PRICE_FAILED.value,
    "POLICY_RESOURCE_EVENT_PREMIUM": E2RArchetype.DOMESTIC_RESOURCE_DISCOVERY_EVENT.value,
    "DIGITAL_ASSET_POLICY_OVERHEAT": E2RArchetype.DIGITAL_ASSET_THEME_OVERHEAT.value,
    "AI_CLOUD_CAPITAL_ALLOCATION": E2RArchetype.AI_CLOUD_CAPITAL_ALLOCATION.value,
    "K_BEAUTY_DEVICE_GLOBAL_BRAND": E2RArchetype.BEAUTY_DEVICE_EXPORT.value,
}

ROUND230_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "company_level_evidence",
    "revenue_eps_or_fcf_conversion",
    "price_path_after_evidence",
    "stage3_to_large_mfe_confirmation",
    "mae_not_excessive",
    "not_4b_saturated",
    "no_hard_redteam",
    "contract_operational_governance_security_trust_passed",
)

ROUND230_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "policy_news_only",
    "resource_estimate_without_commerciality",
    "stablecoin_policy_theme_only",
    "ai_capital_allocation_without_revenue",
    "contract_headline_without_calloff",
    "capex_without_funding_or_margin",
    "mna_or_cb_event_without_revenue",
    "ipo_or_debut_premium",
    "high_score_without_price_validation",
    "fatal_safety_accident",
    "security_privacy_breach_with_revenue_cut",
)

ROUND230_STAGE4B_WATCH_TRIGGERS: tuple[str, ...] = (
    "stage3_after_2x_to_5x_price_move",
    "market_cap_milestone_headline",
    "large_cb_equity_or_mna_event",
    "news_day_plus_20_to_30pct_move",
    "policy_mou_resource_stablecoin_theme_rally",
    "ipo_or_debut_after_short_term_double",
    "good_news_with_weak_price_response",
    "valuation_moves_ahead_of_evidence",
)

ROUND230_HARD_4C_GATES: tuple[str, ...] = (
    "contract_cancellation",
    "contract_value_collapse",
    "fatal_safety_accident",
    "operational_trust_break",
    "security_or_privacy_breach_with_revenue_cut",
    "major_governance_legal_break",
    "pf_workout_or_credit_break",
    "regulatory_reversal",
    "commercialization_failure",
    "financing_failure",
    "capex_without_funding_clarity",
)

ROUND230_PRICE_VALIDATION_FIELDS: tuple[str, ...] = (
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
    "peak_return_from_stage3",
    "market_cap_anchor",
    "contract_value_anchor",
    "trust_break_cost_anchor",
    "policy_or_theme_revenue_bridge",
    "price_validation_status",
)


@dataclass(frozen=True)
class Round230ScoreAdjustment:
    axis: str
    points: int
    direction: str
    reason: str

    def as_row(self) -> dict[str, str]:
        return {"axis": self.axis, "points": str(self.points), "direction": self.direction, "reason": self.reason}


@dataclass(frozen=True)
class Round230ShadowWeightRow:
    archetype: E2RArchetype
    price_path_alignment: int
    stage3_mfe_confirmation: int
    revenue_eps_conversion: int
    actual_contract_quality: int
    operational_trust: int
    security_privacy_trust: int
    event_penalty: int
    capex_funding_redteam: int
    governance_redteam: int
    watch_4b_sensitivity: int
    hard_4c_sensitivity: int
    notes: str

    def as_row(self) -> dict[str, str]:
        return {
            "archetype": self.archetype.value,
            "price_path_alignment": _signed(self.price_path_alignment),
            "stage3_mfe_confirmation": _signed(self.stage3_mfe_confirmation),
            "revenue_eps_conversion": _signed(self.revenue_eps_conversion),
            "actual_contract_quality": _signed(self.actual_contract_quality),
            "operational_trust": _signed(self.operational_trust),
            "security_privacy_trust": _signed(self.security_privacy_trust),
            "event_penalty": _signed(self.event_penalty),
            "capex_funding_redteam": _signed(self.capex_funding_redteam),
            "governance_redteam": _signed(self.governance_redteam),
            "4b_watch_sensitivity": _signed(self.watch_4b_sensitivity),
            "hard_4c_sensitivity": _signed(self.hard_4c_sensitivity),
            "notes": self.notes,
        }


@dataclass(frozen=True)
class Round230DeepSubArchetype:
    category: str
    primary_archetype: E2RArchetype
    terms: tuple[str, ...]

    def as_row(self) -> dict[str, str]:
        return {"category": self.category, "primary_archetype": self.primary_archetype.value, "terms": "|".join(self.terms)}


@dataclass(frozen=True)
class Round230CaseCandidate:
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
    mfe_1d: float | None
    mae_1d: float | None
    stage2_price_anchor: float | None
    stage3_price_anchor: float | None
    stage4b_price_anchor: float | None
    stage4c_price_anchor: float | None
    peak_price_anchor: float | None
    peak_return_from_stage3_pct: float | None
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
    def expected_group(self) -> str:
        return self.case_type


ROUND230_SCORE_ADJUSTMENTS: tuple[Round230ScoreAdjustment, ...] = (
    Round230ScoreAdjustment("price_path_alignment", 5, "raise", "Stage 3 증거 이후 가격경로가 따라와야 한다."),
    Round230ScoreAdjustment("stage3_to_large_MFE_confirmation", 5, "raise", "SK하이닉스처럼 Stage 3 이후 대형 MFE가 확인되면 성공 기준점이 된다."),
    Round230ScoreAdjustment("revenue_or_EPS_revision", 5, "raise", "가격경로는 revenue/EPS/FCF 전환과 함께 확인해야 한다."),
    Round230ScoreAdjustment("order_to_revenue_conversion", 5, "raise", "계약·수주는 실제 매출 인식까지 이어져야 한다."),
    Round230ScoreAdjustment("commercial_revenue_conversion", 5, "raise", "정책·AI·자원 이벤트는 상업 매출 전환 전 Green이 아니다."),
    Round230ScoreAdjustment("actual_contract_quality", 5, "raise", "계약 headline보다 call-off, take-or-pay, volume, margin이 중요하다."),
    Round230ScoreAdjustment("actual_calloff_or_take_or_pay", 5, "raise", "실제 인출·take-or-pay는 계약 품질을 높인다."),
    Round230ScoreAdjustment("operational_trust", 5, "raise", "운영 신뢰는 항공·서비스·플랫폼의 hard gate다."),
    Round230ScoreAdjustment("security_privacy_trust", 5, "raise", "보안·개인정보 훼손은 매출전망과 보상비용으로 이어진다."),
    Round230ScoreAdjustment("hard_4c_early_warning", 5, "raise", "계약·안전·보안 hard 4C를 빨리 잡아야 한다."),
    Round230ScoreAdjustment("policy_news_only", -5, "lower", "정책 뉴스만으로는 Green 금지다."),
    Round230ScoreAdjustment("resource_estimate_without_commerciality", -5, "lower", "상업성 전 자원 추정 급등은 price_moved_without_evidence다."),
    Round230ScoreAdjustment("stablecoin_policy_theme_only", -5, "lower", "발행권·reserve income 전 stablecoin 테마는 event premium이다."),
    Round230ScoreAdjustment("AI_capital_allocation_without_revenue", -5, "lower", "AI 투자·CB 이벤트는 recurring AI revenue 전 Stage 2/4B다."),
    Round230ScoreAdjustment("contract_headline_without_calloff", -5, "lower", "고객명과 계약 headline만으로 Green을 주면 hard 4C에 취약하다."),
    Round230ScoreAdjustment("capex_without_funding_or_margin", -5, "lower", "funding·margin 없는 CAPEX는 RedTeam이다."),
    Round230ScoreAdjustment("M&A_or_CB_event_without_revenue", -4, "lower", "M&A/CB 이벤트는 매출 전환 전 4B-watch다."),
    Round230ScoreAdjustment("IPO_or_debut_premium", -4, "lower", "상장 초기 프리미엄은 구조 증거가 아니다."),
    Round230ScoreAdjustment("high_score_without_price_validation", -5, "lower", "가격검증이 없는 높은 점수는 calibration 대상이다."),
)


ROUND230_SHADOW_WEIGHT_ROWS: tuple[Round230ShadowWeightRow, ...] = (
    Round230ShadowWeightRow(E2RArchetype.STRUCTURAL_SUCCESS_ALIGNED, 5, 5, 5, 4, 3, 2, 0, 0, 0, 4, 2, "SK Hynix and APR prove Stage 3 can produce large MFE when revenue/EPS conversion exists."),
    Round230ShadowWeightRow(E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH, 5, 5, 5, 4, 3, 2, -1, 1, 1, 5, 3, "Large MFE plus market-cap/valuation milestone requires 4B-watch."),
    Round230ShadowWeightRow(E2RArchetype.AI_CLOUD_CAPITAL_ALLOCATION, 3, 2, 3, 2, 3, 2, -5, 3, 2, 5, 3, "Samsung SDS KKR event is Stage 2 and 4B before AI revenue/FCF."),
    Round230ShadowWeightRow(E2RArchetype.EVIDENCE_GOOD_BUT_PRICE_FAILED, 0, 0, 0, 1, 2, 1, -5, 5, 2, 4, 4, "Hyundai Steel shows policy capex without funding/margin can fail."),
    Round230ShadowWeightRow(E2RArchetype.CONTRACT_QUALITY_BREAK, 0, 0, 0, 5, 2, 1, 0, 1, 1, 3, 5, "LGES/L&F contract cancellation and value collapse are hard 4C."),
    Round230ShadowWeightRow(E2RArchetype.OPERATIONAL_TRUST_BREAK, 0, 0, 0, 0, 5, 2, 0, 0, 2, 3, 5, "Jeju Air fatal crash is hard operational trust 4C."),
    Round230ShadowWeightRow(E2RArchetype.SECURITY_OPERATIONAL_TRUST_OVERLAY, 0, 0, 0, 0, 4, 5, 0, 1, 3, 4, 5, "SK Telecom data breach is strong 4C-watch with revenue/cost impact."),
    Round230ShadowWeightRow(E2RArchetype.PRICE_ONLY_RALLY, 0, 0, 0, 0, 1, 1, -5, 2, 2, 5, 4, "Korea Gas and stablecoin rallies are price_moved_without_evidence until commerciality or revenue."),
)


ROUND230_DEEP_SUB_ARCHETYPES: tuple[Round230DeepSubArchetype, ...] = (
    Round230DeepSubArchetype("성공 검증 / HBM", E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH, ("SK Hynix HBM", "HBM4", "AI memory", "EPS revision", "stage3 to large MFE", "market-cap milestone")),
    Round230DeepSubArchetype("성공 검증 / K-beauty device", E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH, ("APR", "Medicube", "K-beauty device", "overseas revenue growth", "single-brand concentration")),
    Round230DeepSubArchetype("AI capital allocation 4B", E2RArchetype.AI_CLOUD_CAPITAL_ALLOCATION, ("Samsung SDS", "KKR convertible bond", "AI infrastructure", "M&A", "capital allocation", "recurring AI revenue required")),
    Round230DeepSubArchetype("정책 CAPEX 실패", E2RArchetype.EVIDENCE_GOOD_BUT_PRICE_FAILED, ("Hyundai Steel U.S. plant", "tariff hedge", "funding uncertainty", "margin clarity", "policy-induced capex failure")),
    Round230DeepSubArchetype("계약품질 hard 4C", E2RArchetype.CONTRACT_QUALITY_BREAK, ("LGES", "L&F", "contract cancellation", "contract value collapse", "actual call-off", "take-or-pay")),
    Round230DeepSubArchetype("운영안전 hard 4C", E2RArchetype.OPERATIONAL_TRUST_BREAK, ("Jeju Air", "fatal crash", "operational safety", "market-cap wipeout", "consumer trust")),
    Round230DeepSubArchetype("보안·개인정보 4C", E2RArchetype.SECURITY_OPERATIONAL_TRUST_OVERLAY, ("SK Telecom", "cyberattack", "customer data leak", "revenue forecast cut", "security investment", "USIM replacement")),
    Round230DeepSubArchetype("정책·자원·디지털자산 price-only", E2RArchetype.PRICE_ONLY_RALLY, ("Korea Gas", "East Sea oil and gas", "stablecoin policy basket", "Kakao Pay", "ME2ON", "commerciality required", "licensed revenue required")),
)


ROUND230_CASE_CANDIDATES: tuple[Round230CaseCandidate, ...] = (
    Round230CaseCandidate(
        case_id="r13_loop9_sk_hynix_hbm_stage3_4b",
        symbol="000660",
        company_name="SK하이닉스",
        source_sector="R2",
        primary_archetype=E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH,
        secondary_archetypes=(E2RArchetype.MEMORY_HBM_CAPACITY, E2RArchetype.CROWDED_RERATING_4B_WATCH),
        case_type="structural_success",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2024, 6, 25),
        stage3_date=date(2024, 6, 25),
        stage4b_date=date(2026, 5, 4),
        stage4c_date=None,
        stage3_decision="hbm_dominance_memory_price_upcycle_and_eps_revision_confirm_stage3_success_but_2026_market_cap_milestone_requires_4b_watch",
        stage4b_status="4B-watch/elevated",
        hard_4c_confirmed=False,
        evidence_fields=("hbm_dominance", "dram_price_upcycle", "op_revision_2024_30tn_2025_53tn_krw", "stage3_price_222000", "reported_peak_1447000", "reported_peak_return_551_8pct"),
        red_flag_fields=("market_cap_milestone_headline", "reported_2025_return_274pct", "reported_2026_return_above_200pct", "crowding_watch"),
        price_data_source="MarketWatch / Reuters reported price and return anchors",
        reported_price_anchor="222,000 KRW Stage 3 anchor to 1,447,000 KRW reported record high",
        reported_return_anchor="MFE +551.8%; 2025 +274%; 2026 >+200%; market cap about $942B",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=222000.0,
        stage3_price_anchor=222000.0,
        stage4b_price_anchor=1447000.0,
        stage4c_price_anchor=None,
        peak_price_anchor=1447000.0,
        peak_return_from_stage3_pct=551.8,
        extra_price_metrics={"reported_return_2025_pct": 274.0, "reported_return_2026_to_2026_05_14_pct_min": 200.0, "minimum_compounded_return_from_2025_start_pct": 1022.0, "market_cap_2026_usd_bn": 942.0, "minimum_market_cap_mfe_pct": 842.0},
        score_price_alignment="aligned",
        round_alignment_label="aligned",
        rerating_result="true_rerating",
        round_rerating_label="true_rerating",
        stage_failure_type="green_success",
        round_stage_failure_label="green_success_then_4b_watch",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="Stage 3 성공 benchmark다. 다만 2026년 현재는 신규 Green이 아니라 4B-watch/crowding watch다.",
    ),
    Round230CaseCandidate(
        case_id="r13_loop9_apr_medicube_structural_4b",
        symbol="278470",
        company_name="APR / Medicube",
        source_sector="R5",
        primary_archetype=E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH,
        secondary_archetypes=(E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION, E2RArchetype.BEAUTY_DEVICE_EXPORT),
        case_type="structural_success",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2025, 7, 8),
        stage3_date=date(2025, 10, 1),
        stage4b_date=date(2025, 7, 8),
        stage4c_date=None,
        stage3_decision="overseas_revenue_growth_and_real_revenue_conversion_support_structural_success_but_single_brand_device_concentration_requires_4b_watch",
        stage4b_status="4B-watch",
        hard_4c_confirmed=False,
        evidence_fields=("stage2_price_158300", "ipo_after_plus_75pct", "q4_revenue_440m_usd_plus_124pct", "overseas_revenue_362m_usd_plus_203pct", "fy_revenue_1_2bn_usd", "medicube_revenue_1_1bn_usd"),
        red_flag_fields=("single_brand_device_concentration", "medicube_revenue_share_91_7pct", "valuation_crowding_watch", "fast_product_cycle_watch"),
        price_data_source="Business Insider / Vogue Business anchors",
        reported_price_anchor="158,300 KRW on 2025-07-08; market cap about $4.2B",
        reported_return_anchor="IPO to stage2 MFE >75%; Q4 revenue +124%; overseas revenue +203%",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=158300.0,
        stage3_price_anchor=None,
        stage4b_price_anchor=158300.0,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        peak_return_from_stage3_pct=None,
        extra_price_metrics={"implied_ipo_reference_price_max": 90457.0, "ipo_to_stage2_mfe_min_pct": 75.0, "market_cap_july_2025_usd_bn": 4.2, "q4_2025_revenue_usd_mn": 440.0, "q4_2025_revenue_growth_pct": 124.0, "q4_2025_overseas_revenue_usd_mn": 362.0, "q4_2025_overseas_growth_pct": 203.0, "fy_2025_revenue_usd_bn": 1.2, "medicube_fy_2025_revenue_usd_bn": 1.1, "medicube_revenue_share_pct": 91.7},
        score_price_alignment="aligned",
        round_alignment_label="aligned",
        rerating_result="true_rerating",
        round_rerating_label="K_beauty_device_true_rerating_plus_4B_watch",
        stage_failure_type="green_success",
        round_stage_failure_label="green_success_candidate_plus_4b_watch",
        price_validation_status="reported_price_and_revenue_anchor_not_full_ohlc",
        notes="Viral이 실제 해외 매출로 내려온 구조 후보지만 매출 집중도와 valuation 때문에 4B-watch가 필요하다.",
    ),
    Round230CaseCandidate(
        case_id="r13_loop9_samsung_sds_kkr_ai_event_4b",
        symbol="018260",
        company_name="삼성SDS",
        source_sector="R8",
        primary_archetype=E2RArchetype.AI_CLOUD_CAPITAL_ALLOCATION,
        secondary_archetypes=(E2RArchetype.CROWDED_RERATING_4B_WATCH, E2RArchetype.EVENT_PREMIUM),
        case_type="success_candidate",
        stage1_date=date(2025, 1, 1),
        stage2_date=date(2026, 4, 15),
        stage3_date=None,
        stage4b_date=date(2026, 4, 15),
        stage4c_date=None,
        stage3_decision="kkr_cb_and_ai_capital_allocation_are_stage2_and_4b_watch_until_recurring_ai_revenue_margin_and_fcf_confirm",
        stage4b_status="4B-watch",
        hard_4c_confirmed=False,
        evidence_fields=("kkr_820m_usd_convertible_bond", "ai_infrastructure_capital_allocation", "existing_cash_6_4tn_krw", "event_mfe_20_8pct"),
        red_flag_fields=("ai_capital_allocation_without_revenue", "mna_or_cb_event_without_revenue", "price_moved_before_recurring_ai_revenue", "valuation_ahead_of_evidence"),
        price_data_source="Reuters reported event return anchor",
        reported_price_anchor="Samsung SDS intraday +20.8%; KOSPI +3.0% context",
        reported_return_anchor="KKR $820M CB, relative intraday outperformance +17.8pp",
        mfe_1d=20.8,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        peak_return_from_stage3_pct=None,
        extra_price_metrics={"morning_trade_return_pct": 19.4, "kospi_same_context_return_pct": 3.0, "relative_intraday_outperformance_vs_kospi_pp": 17.8, "cb_investment_usd_mn": 820.0, "fx_rate_krw_per_usd": 1472.0, "cb_investment_krw_trn": 1.207, "existing_cash_krw_trn": 6.4, "combined_cash_plus_cb_krw_trn": 7.607},
        score_price_alignment="price_moved_without_evidence",
        round_alignment_label="event_premium_success_candidate",
        rerating_result="event_premium",
        round_rerating_label="AI_cloud_capital_allocation_watch",
        stage_failure_type="stage2_watch_success",
        round_stage_failure_label="should_not_be_green_yet",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="좋은 Stage 2 후보지만 AI revenue conversion 전 +20.8%는 Green이 아니라 4B-watch다.",
    ),
    Round230CaseCandidate(
        case_id="r13_loop9_hyundai_steel_policy_capex_failure",
        symbol="004020",
        company_name="현대제철",
        source_sector="R4/R11",
        primary_archetype=E2RArchetype.EVIDENCE_GOOD_BUT_PRICE_FAILED,
        secondary_archetypes=(E2RArchetype.STEEL_TARIFF_EVENT_KOREA, E2RArchetype.FALSE_POSITIVE_SCORE),
        case_type="failed_rerating",
        stage1_date=date(2025, 3, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 4, 22),
        stage3_decision="policy_induced_tariff_hedge_capex_without_funding_margin_and_fcf_clarity_is_redteam_not_green",
        stage4b_status="not_applicable",
        hard_4c_confirmed=False,
        evidence_fields=("us_plant_5_8_to_6bn_usd", "hyundai_motor_group_us_package_21bn_usd", "tariff_hedge_capex_plan"),
        red_flag_fields=("capex_without_funding_or_margin", "funding_plan_unclear", "domestic_demand_weakness", "chinese_imports", "labor_disputes", "relative_underperformance_vs_kospi"),
        price_data_source="Reuters policy-induced capex / market-reaction anchor",
        reported_price_anchor="Hyundai Steel shares -21.2% after U.S. plant announcement",
        reported_return_anchor="POSCO Holdings -18.3%; KOSPI -5.5%; relative underperformance -15.7pp",
        mfe_1d=None,
        mae_1d=-21.2,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        peak_return_from_stage3_pct=None,
        extra_price_metrics={"us_plant_investment_usd_bn_range": "5.8-6.0", "hyundai_motor_group_us_package_usd_bn": 21.0, "reported_share_drop_after_announcement_pct": -21.2, "posco_holdings_same_period_pct": -18.3, "benchmark_index_same_period_pct": -5.5, "relative_underperformance_vs_kospi_pp": -15.7, "funding_plan": "half_borrowing_possible_posco_equity"},
        score_price_alignment="evidence_good_but_price_failed",
        round_alignment_label="false_positive_score_prevention",
        rerating_result="no_rerating",
        round_rerating_label="policy_capex_without_funding_failed",
        stage_failure_type="should_have_been_red",
        round_stage_failure_label="4C_watch",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="정책·관세 대응 CAPEX는 funding·margin·FCF가 없으면 Green이 아니라 RedTeam이다.",
    ),
    Round230CaseCandidate(
        case_id="r13_loop9_lges_lnf_contract_quality_hard_4c",
        symbol="373220/066970",
        company_name="LGES / L&F",
        source_sector="R3",
        primary_archetype=E2RArchetype.CONTRACT_QUALITY_BREAK,
        secondary_archetypes=(E2RArchetype.FALSE_POSITIVE_SCORE,),
        case_type="4c_thesis_break",
        stage1_date=None,
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 12, 17),
        stage3_decision="customer_name_and_contract_headline_are_not_green_without_actual_calloff_take_or_pay_delivery_margin_and_fcf",
        stage4b_status="not_applicable",
        hard_4c_confirmed=True,
        evidence_fields=("ford_contract_cancellation_9_6tn_krw", "freudenberg_contract_cancellation_3_9tn_krw", "tesla_cathode_contract_value_collapse"),
        red_flag_fields=("contract_cancellation", "contract_value_collapse", "contract_headline_without_calloff", "lost_revenue_vs_2024_revenue_52_7pct"),
        price_data_source="Reuters reported event and contract-value anchors",
        reported_price_anchor="Stock OHLC unavailable beyond reported contract anchors",
        reported_return_anchor="LGES lost expected revenue 13.5T KRW; L&F contract value collapsed from $2.9B to $7,386",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        peak_return_from_stage3_pct=None,
        extra_price_metrics={"lges_ford_cancelled_contract_krw_trn": 9.6, "lges_freudenberg_cancelled_contract_krw_trn": 3.9, "lges_total_lost_expected_revenue_krw_trn": 13.5, "lges_2024_revenue_krw_trn": 25.62, "lost_revenue_vs_2024_revenue_pct": 52.7, "lnf_initial_contract_value_usd_bn": 2.9, "lnf_revised_contract_value_usd": 7386.0, "lnf_contract_value_drawdown_pct": -99.999745},
        score_price_alignment="evidence_good_but_price_failed",
        round_alignment_label="thesis_break",
        rerating_result="thesis_break",
        round_rerating_label="contract_quality_failure",
        stage_failure_type="should_have_been_red",
        round_stage_failure_label="hard_4C",
        price_validation_status="reported_event_and_contract_anchor_not_full_ohlc",
        notes="R3 Green gate는 고객명이 아니라 actual call-off, take-or-pay, volume, OPM, FCF다.",
    ),
    Round230CaseCandidate(
        case_id="r13_loop9_jeju_air_operational_safety_hard_4c",
        symbol="089590",
        company_name="제주항공",
        source_sector="R9",
        primary_archetype=E2RArchetype.OPERATIONAL_TRUST_BREAK,
        secondary_archetypes=(E2RArchetype.FALSE_POSITIVE_SCORE,),
        case_type="4c_thesis_break",
        stage1_date=date(2023, 1, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2024, 12, 30),
        stage3_decision="fatal_safety_accident_is_hard_4c_and_blocks_travel_demand_green",
        stage4b_status="not_applicable",
        hard_4c_confirmed=True,
        evidence_fields=("fatal_crash", "179_fatalities", "jeju_air_intraday_minus_15_7pct", "market_cap_wipeout_95_7bn_krw"),
        red_flag_fields=("fatal_safety_accident", "operational_trust_break", "consumer_trust_break", "safety_regulatory_watch"),
        price_data_source="Reuters reported price/event anchors",
        reported_price_anchor="Jeju Air event low 6,920 KRW; implied pre-event reference about 8,209 KRW",
        reported_return_anchor="Jeju Air -15.7%; market cap wipeout 95.7B KRW; fatalities 179",
        mfe_1d=None,
        mae_1d=-15.7,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=6920.0,
        peak_price_anchor=None,
        peak_return_from_stage3_pct=None,
        extra_price_metrics={"event_low_price": 6920.0, "implied_pre_event_reference_price": 8209.0, "market_cap_wipeout_krw_bn": 95.7, "fatalities": 179.0, "ak_holdings_mae_pct": -12.0, "korean_air_mae_pct": -1.3, "asiana_mae_pct": -0.8, "hanatour_mae_pct": -7.0, "very_good_tour_mae_pct": -11.0},
        score_price_alignment="evidence_good_but_price_failed",
        round_alignment_label="thesis_break",
        rerating_result="thesis_break",
        round_rerating_label="operational_safety_trust_break",
        stage_failure_type="should_have_been_red",
        round_stage_failure_label="hard_4C",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="여행수요가 좋아도 fatal accident가 나오면 Green은 즉시 차단한다.",
    ),
    Round230CaseCandidate(
        case_id="r13_loop9_skt_security_privacy_4c_watch",
        symbol="017670",
        company_name="SK텔레콤",
        source_sector="R8",
        primary_archetype=E2RArchetype.SECURITY_OPERATIONAL_TRUST_OVERLAY,
        secondary_archetypes=(E2RArchetype.PLATFORM_PRIVACY_SECURITY_OVERLAY, E2RArchetype.OPERATIONAL_TRUST_BREAK),
        case_type="4c_thesis_break",
        stage1_date=date(2024, 1, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 4, 28),
        stage3_decision="security_privacy_breach_with_revenue_cut_and_costs_is_strong_4c_watch_until_penalty_and_recovery_path_confirm",
        stage4b_status="not_applicable",
        hard_4c_confirmed=False,
        evidence_fields=("cyberattack_customer_data_leak", "23m_users_free_usim_replacement", "26_96m_data_pieces_leaked", "revenue_forecast_cut_800bn_krw", "security_investment_700bn_krw"),
        red_flag_fields=("security_privacy_breach_with_revenue_cut", "customer_trust_break", "benefit_package_cost_500bn_krw", "government_negligence_finding", "regulatory_penalty_watch"),
        price_data_source="Reuters reported price / breach / cost anchors",
        reported_price_anchor="SK Telecom -8.5% intraday, -6.7% close on 2025-04-28",
        reported_return_anchor="Revenue forecast cut 800B KRW; security investment 700B KRW over five years",
        mfe_1d=None,
        mae_1d=-8.5,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        peak_return_from_stage3_pct=None,
        extra_price_metrics={"event_close_mae_pct": -6.7, "affected_users_initial_mn": 23.0, "leaked_user_data_pieces_mn": 26.96, "security_investment_krw_bn": 700.0, "annualized_security_investment_krw_bn": 140.0, "revenue_forecast_cut_2025_krw_bn": 800.0, "customer_benefit_package_cost_krw_bn": 500.0, "usim_replacement_users_by_late_june_mn": 9.39},
        score_price_alignment="evidence_good_but_price_failed",
        round_alignment_label="thesis_break_watch",
        rerating_result="thesis_break",
        round_rerating_label="cybersecurity_operational_trust_break",
        stage_failure_type="should_have_been_red",
        round_stage_failure_label="strong_4C_watch",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="보안사고는 단순 one-day issue가 아니라 매출전망·보상비용·신뢰비용으로 이어지는 4C gate다.",
    ),
    Round230CaseCandidate(
        case_id="r13_loop9_policy_resource_stablecoin_price_only",
        symbol="036460/377300/LG_CNS/Aton/ME2ON",
        company_name="Korea Gas / stablecoin policy basket",
        source_sector="R6/R11",
        primary_archetype=E2RArchetype.PRICE_ONLY_RALLY,
        secondary_archetypes=(E2RArchetype.DOMESTIC_RESOURCE_DISCOVERY_EVENT, E2RArchetype.DIGITAL_ASSET_THEME_OVERHEAT, E2RArchetype.EVENT_PREMIUM),
        case_type="overheat",
        stage1_date=date(2024, 6, 3),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=date(2024, 6, 3),
        stage4c_date=None,
        stage3_decision="resource_estimate_and_stablecoin_policy_are_stage1_or_4b_until_commerciality_licensed_revenue_and_reserve_income_confirm",
        stage4b_status="4B-watch",
        hard_4c_confirmed=False,
        evidence_fields=("kogas_event_mfe_30pct", "resource_possibility_14bn_barrels", "stablecoin_policy_basket_two_to_three_x_moves"),
        red_flag_fields=("resource_estimate_without_commerciality", "stablecoin_policy_theme_only", "regulated_revenue_unconfirmed", "issuer_license_unconfirmed", "reserve_income_unconfirmed"),
        price_data_source="WSJ / FT reported event-return anchors",
        reported_price_anchor="Korea Gas 38,700 KRW and +30%; Kakao Pay >2x, ME2ON 3x",
        reported_return_anchor="Resource commerciality and stablecoin regulated revenue not confirmed",
        mfe_1d=30.0,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=38700.0,
        stage4c_price_anchor=None,
        peak_price_anchor=38700.0,
        peak_return_from_stage3_pct=None,
        extra_price_metrics={"kogas_event_peak_price": 38700.0, "kogas_event_mfe_1d_pct": 30.0, "kogas_implied_pre_event_reference_price": 29769.0, "resource_possibility_bbl_bn": 14.0, "drilling_cost_per_attempt_krw_bn": 100.0, "economic_viability_confirmed": False, "kakao_pay_mfe_month_pct_min": 100.0, "lg_cns_mfe_month_pct": 70.0, "aton_mfe_month_pct": 80.0, "me2on_mfe_month_pct": 200.0, "regulated_revenue_confirmed": False, "issuer_license_confirmed": False, "reserve_income_confirmed": False},
        score_price_alignment="price_moved_without_evidence",
        round_alignment_label="price_moved_without_evidence",
        rerating_result="event_premium",
        round_rerating_label="policy_resource_digital_asset_event_premium",
        stage_failure_type="false_yellow",
        round_stage_failure_label="should_have_been_stage1_or_4B_watch",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="정책·자원·디지털자산 이벤트는 실제 계약·경제성·규제수익 전에는 Green 금지다.",
    ),
)


def round230_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    stage3_terms = ("revenue", "eps", "fcf", "revision", "hbm", "overseas", "margin", "price_path")
    for candidate in ROUND230_CASE_CANDIDATES:
        record = E2RCaseRecord(
            case_id=candidate.case_id,
            symbol=candidate.symbol,
            company_name=candidate.company_name,
            market="KR",
            sector_raw=candidate.primary_archetype.value,
            primary_archetype=candidate.primary_archetype,
            secondary_archetypes=candidate.secondary_archetypes,
            expected_group=candidate.expected_group,
            large_sector=ROUND230_LARGE_SECTOR,
            case_type=candidate.case_type,
            stage1_date=candidate.stage1_date,
            stage2_date=candidate.stage2_date,
            stage3_date=candidate.stage3_date,
            stage4b_date=candidate.stage4b_date,
            stage4c_date=candidate.stage4c_date,
            evidence_summary=(
                "Round230 R13 Loop-9 cross-archetype RedTeam price validation case. "
                "Calibration-only; not production scoring input."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=candidate.evidence_fields if candidate.stage2_date else (),
            stage3_evidence=tuple(field for field in candidate.evidence_fields if any(term in field.lower() for term in stage3_terms)),
            stage4b_evidence=tuple(
                field
                for field in (*candidate.evidence_fields, *candidate.red_flag_fields)
                if "mfe" in field or "price" in field or "market_cap" in field or "valuation" in field or "event" in field
            ),
            stage4c_evidence=tuple(
                field
                for field in candidate.red_flag_fields
                if "break" in field
                or "collapse" in field
                or "accident" in field
                or "breach" in field
                or "failure" in field
                or "cut" in field
                or "cancellation" in field
                or "redteam" in field
            ),
            must_have_fields=ROUND230_GREEN_REQUIRED_FIELDS,
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
            score_weight_hint={f"{item.axis}_delta": float(item.points) for item in ROUND230_SCORE_ADJUSTMENTS},
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "full_ohlc_complete_false",
                "r13_default_stage3_bias_redteam_first_after_price_validation",
                "price_validation_partial_with_reported_price_anchors",
                "do_not_invent_price_or_stage_dates",
                "do_not_treat_policy_resource_stablecoin_cb_or_capex_event_as_green_alone",
                *ROUND230_GREEN_REQUIRED_FIELDS,
                *ROUND230_GREEN_FORBIDDEN_PATTERNS,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(
                stage2_price=candidate.stage2_price_anchor,
                stage3_price=candidate.stage3_price_anchor,
                stage4b_price=candidate.stage4b_price_anchor,
                stage4c_price=candidate.stage4c_price_anchor,
                peak_price=candidate.peak_price_anchor,
                peak_return_from_stage3=candidate.peak_return_from_stage3_pct,
                mfe_30d=candidate.mfe_1d,
                mae_30d=candidate.mae_1d,
                price_validation_status=candidate.price_validation_status,
            ),
            data_quality=CaseDataQuality(
                official_data_available=True,
                report_data_available=True,
                price_data_available=candidate.stage2_price_anchor is not None
                or candidate.stage3_price_anchor is not None
                or candidate.stage4b_price_anchor is not None
                or candidate.stage4c_price_anchor is not None
                or candidate.mfe_1d is not None
                or candidate.mae_1d is not None,
                stage_dates_confidence=0.85 if candidate.stage3_date or candidate.stage4c_date else 0.75,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round230_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND230_CASE_CANDIDATES:
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
                "mfe_1d": _float_text(candidate.mfe_1d),
                "mae_1d": _float_text(candidate.mae_1d),
                "stage3_price_anchor": _float_text(candidate.stage3_price_anchor),
                "stage4b_price_anchor": _float_text(candidate.stage4b_price_anchor),
                "stage4c_price_anchor": _float_text(candidate.stage4c_price_anchor),
                "peak_return_from_stage3_pct": _float_text(candidate.peak_return_from_stage3_pct),
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


def round230_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND230_SCORE_ADJUSTMENTS)


def round230_shadow_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(row.as_row() for row in ROUND230_SHADOW_WEIGHT_ROWS)


def round230_deep_sub_archetype_rows() -> tuple[dict[str, str], ...]:
    return tuple(row.as_row() for row in ROUND230_DEEP_SUB_ARCHETYPES)


def round230_price_validation_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round230_price_validation": "true"} for field in ROUND230_PRICE_VALIDATION_FIELDS)


def round230_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple({"round230_label": label, "canonical_archetype": canonical} for label, canonical in ROUND230_REQUIRED_TARGET_ALIASES.items())


def round230_summary() -> dict[str, int | bool | str]:
    cases = ROUND230_CASE_CANDIDATES
    return {
        "source_round": ROUND230_SOURCE_ROUND_PATH,
        "large_sector": ROUND230_LARGE_SECTOR,
        "case_candidate_count": len(cases),
        "structural_success_count": sum(1 for case in cases if case.case_type == "structural_success"),
        "success_candidate_count": sum(1 for case in cases if case.case_type == "success_candidate"),
        "failed_rerating_count": sum(1 for case in cases if case.case_type == "failed_rerating"),
        "overheat_count": sum(1 for case in cases if case.case_type == "overheat"),
        "hard_4c_case_count": sum(1 for case in cases if case.hard_4c_confirmed),
        "stage3_case_count": sum(1 for case in cases if case.stage3_date is not None),
        "stage4b_watch_count": sum(1 for case in cases if "4B" in case.stage4b_status),
        "price_moved_without_evidence_count": sum(1 for case in cases if case.score_price_alignment == "price_moved_without_evidence"),
        "target_archetype_count": len(ROUND230_REQUIRED_TARGET_ALIASES),
        "deep_sub_archetype_count": len(ROUND230_DEEP_SUB_ARCHETYPES),
        "shadow_weight_row_count": len(ROUND230_SHADOW_WEIGHT_ROWS),
        "price_validation_completed": "partial_with_reported_price_anchors",
        "full_ohlc_complete": False,
        "r13_default_stage3_bias": ROUND230_DEFAULT_STAGE3_BIAS,
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
    }


def round230_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND230_SOURCE_ROUND_PATH,
        "large_sector": ROUND230_LARGE_SECTOR,
        "summary": round230_summary(),
        "target_aliases": dict(ROUND230_REQUIRED_TARGET_ALIASES),
        "green_required_fields": list(ROUND230_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND230_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_watch_triggers": list(ROUND230_STAGE4B_WATCH_TRIGGERS),
        "hard_4c_gates": list(ROUND230_HARD_4C_GATES),
        "deep_sub_archetypes": round230_deep_sub_archetype_rows(),
        "shadow_weights": round230_shadow_weight_rows(),
        "what_not_to_change": [
            "do_not_use_round230_cases_as_candidate_generation_input",
            "do_not_apply_shadow_weights_to_production_scoring_yet",
            "do_not_treat_policy_resource_stablecoin_cb_or_capex_event_as_green",
            "do_not_invent_ohlc_or_stage_dates",
        ],
    }


def render_round230_summary_markdown() -> str:
    summary = round230_summary()
    lines = [
        "# Round 230 R13 Loop 9 Cross-Archetype RedTeam Price Validation",
        "",
        "This pack is calibration-only. Production scoring and candidate generation are unchanged.",
        "",
        "## Summary",
        "",
        f"- source_round: {summary['source_round']}",
        f"- large_sector: {summary['large_sector']}",
        f"- cases: {summary['case_candidate_count']}",
        f"- structural_success: {summary['structural_success_count']}",
        f"- success_candidate: {summary['success_candidate_count']}",
        f"- failed_rerating: {summary['failed_rerating_count']}",
        f"- overheat: {summary['overheat_count']}",
        f"- hard_4c_case_count: {summary['hard_4c_case_count']}",
        f"- Stage 3 dated cases: {summary['stage3_case_count']}",
        f"- 4B-watch cases: {summary['stage4b_watch_count']}",
        f"- price_moved_without_evidence: {summary['price_moved_without_evidence_count']}",
        f"- deep_sub_archetype_count: {summary['deep_sub_archetype_count']}",
        f"- shadow_weight_row_count: {summary['shadow_weight_row_count']}",
        f"- r13_default_stage3_bias: {summary['r13_default_stage3_bias']}",
        f"- full_ohlc_complete: {str(summary['full_ohlc_complete']).lower()}",
        "",
        "## Case Matrix",
        "",
        "| case | company | source | type | stage3 | 4B | 4C | round alignment | note |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for case in ROUND230_CASE_CANDIDATES:
        lines.append(
            "| "
            + " | ".join(
                (
                    case.case_id,
                    case.company_name,
                    case.source_sector,
                    case.case_type,
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
            "- SK Hynix and APR/Medicube are aligned structural-success benchmarks, but both need 4B-watch after major rerating.",
            "- Samsung SDS is Stage 2 plus 4B-watch; CB and AI capital allocation are not recurring AI revenue.",
            "- Hyundai Steel prevents false Green from policy-induced CAPEX without funding or margin clarity.",
            "- LGES/L&F and Jeju Air are hard 4C anchors.",
            "- SK Telecom is strong security/privacy 4C-watch because breach cost and revenue forecast changed.",
            "- Korea Gas and stablecoin basket are price_moved_without_evidence before commerciality or licensed revenue.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round230_green_gate_review_markdown() -> str:
    lines = [
        "# Round 230 R13 Green Gate Review",
        "",
        "Do not apply these weights to production scoring yet.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND230_GREEN_REQUIRED_FIELDS)
    lines.extend(["", "## Forbidden Patterns", ""])
    lines.extend(f"- {field}" for field in ROUND230_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(
        [
            "",
            "## Easy Example",
            "- `Stage 3 evidence + large MFE` validates a structural case, but may also trigger 4B-watch.",
            "- `CB/M&A/AI headline + one-day +20%` is Stage 2/4B-watch until recurring revenue appears.",
            "- `contract cancellation`, `fatal accident`, or `security breach with revenue cut` are hard RedTeam gates.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round230_stage4b_4c_review_markdown() -> str:
    lines = ["# Round 230 R13 4B/4C Review", "", "## 4B Watch Triggers", ""]
    lines.extend(f"- {field}" for field in ROUND230_STAGE4B_WATCH_TRIGGERS)
    lines.extend(["", "## Hard 4C Gates", ""])
    lines.extend(f"- {field}" for field in ROUND230_HARD_4C_GATES)
    lines.extend(
        [
            "",
            "## Plain-Language Gate Notes",
            "",
            "- 4B is about graduation, crowding, price prepayment, and event premium.",
            "- 4C is about thesis break: contract, safety, security, funding, or commercialization failure.",
            "- Price-only rallies stay watch items until company-level revenue, EPS, FCF, or licensed economics are visible.",
        ]
    )
    lines.extend(["", "## Case Notes", ""])
    for case in ROUND230_CASE_CANDIDATES:
        if "4B" in case.stage4b_status or case.red_flag_fields:
            lines.append(f"- {case.case_id}: {', '.join(case.red_flag_fields)}")
    return "\n".join(lines) + "\n"


def render_round230_price_validation_plan_markdown() -> str:
    lines = [
        "# Round 230 R13 Price Validation Plan",
        "",
        "- price_validation_completed: partial_with_reported_price_anchors",
        "- full_ohlc_complete: false",
        "- r13_default_stage3_bias: redteam_first_after_price_validation",
        "- Do not invent OHLC, peak, MFE, or MAE where raw adjusted daily prices are unavailable.",
        "",
        "## Backfill Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND230_PRICE_VALIDATION_FIELDS)
    return "\n".join(lines) + "\n"


def write_round230_r13_loop9_reports(
    output_directory: str | Path = ROUND230_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND230_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND230_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "cases": write_case_library(round230_case_records(), cases_path),
        "audit": _write_json(round230_audit_payload(), audit_path),
        "summary": output / "round230_r13_loop9_price_validation_summary.md",
        "case_matrix": output / "round230_r13_loop9_case_matrix.csv",
        "target_aliases": output / "round230_r13_loop9_target_aliases.csv",
        "score_adjustments": output / "round230_r13_loop9_score_adjustments.csv",
        "shadow_weights": output / "round230_r13_loop9_shadow_weights.csv",
        "deep_sub_archetypes": output / "round230_r13_loop9_deep_sub_archetypes.csv",
        "price_validation_fields": output / "round230_r13_loop9_price_validation_fields.csv",
        "green_gate_review": output / "round230_r13_loop9_green_gate_review.md",
        "price_validation_plan": output / "round230_r13_loop9_price_validation_plan.md",
        "stage4b_4c_review": output / "round230_r13_loop9_stage4b_4c_review.md",
    }
    paths["summary"].write_text(render_round230_summary_markdown(), encoding="utf-8")
    _write_csv(round230_case_rows(), paths["case_matrix"])
    _write_csv(round230_target_alias_rows(), paths["target_aliases"])
    _write_csv(round230_score_adjustment_rows(), paths["score_adjustments"])
    _write_csv(round230_shadow_weight_rows(), paths["shadow_weights"])
    _write_csv(round230_deep_sub_archetype_rows(), paths["deep_sub_archetypes"])
    _write_csv(round230_price_validation_field_rows(), paths["price_validation_fields"])
    paths["green_gate_review"].write_text(render_round230_green_gate_review_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round230_price_validation_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round230_stage4b_4c_review_markdown(), encoding="utf-8")
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
