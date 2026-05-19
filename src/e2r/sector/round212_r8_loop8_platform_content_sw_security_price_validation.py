"""Round-212 R8 Loop-8 platform/content/software/security price validation.

Round 212 is calibration/evaluation material only. It structures
``docs/round/round_212.md`` into case records, reported price anchors, and
shadow scoring notes.

Easy example: an AI partnership headline can route a company to Stage 1 or
Stage 2. It is not Stage 3-Green until paid usage, ARR proxy, bookings, OPM,
FCF, customer retention, and operational trust are visible as-of the case date.
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


ROUND212_SOURCE_ROUND_PATH = "docs/round/round_212.md"
ROUND212_LARGE_SECTOR = Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY
ROUND212_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round212_r8_loop8_platform_content_sw_security_price_validation"
ROUND212_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r8_loop8_round212.jsonl"
ROUND212_DEFAULT_AUDIT_PATH = "data/sector_taxonomy/round212_r8_loop8_platform_content_sw_security_price_validation_audit.json"

ROUND212_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "B2B_SAAS_ERP_WORKFLOW": E2RArchetype.B2B_SAAS_ERP_WORKFLOW.value,
    "CLOUD_AI_SOFTWARE_INFRA": E2RArchetype.CLOUD_AI_SOFTWARE_INFRA.value,
    "AI_CLOUD_CAPITAL_ALLOCATION": E2RArchetype.AI_CLOUD_CAPITAL_ALLOCATION.value,
    "AI_SOFTWARE_APPLICATION": E2RArchetype.AI_SOFTWARE_APPLICATION.value,
    "PLATFORM_SOFTWARE_INTERNET": E2RArchetype.PLATFORM_SOFTWARE_INTERNET.value,
    "WEBTOON_PLATFORM_IP_MONETIZATION": E2RArchetype.WEBTOON_PLATFORM_IP_MONETIZATION.value,
    "GAME_CONTENT_IP_REPEAT_MONETIZATION": E2RArchetype.GAME_CONTENT_IP_REPEAT_MONETIZATION.value,
    "SINGLE_IP_RELEASE_EVENT_PREMIUM": E2RArchetype.SINGLE_IP_RELEASE_EVENT_PREMIUM.value,
    "KPOP_PLATFORM_CONTENT_IP": E2RArchetype.KPOP_PLATFORM_CONTENT_IP.value,
    "PLATFORM_GOVERNANCE_LEGAL_RISK": E2RArchetype.PLATFORM_GOVERNANCE_LEGAL_RISK.value,
    "SECURITY_OPERATIONAL_TRUST_OVERLAY": E2RArchetype.SECURITY_OPERATIONAL_TRUST_OVERLAY.value,
    "PRIVATE_EQUITY_SOFTWARE_RERATING": E2RArchetype.PRIVATE_EQUITY_SOFTWARE_RERATING.value,
    "PRICE_ONLY_RALLY": E2RArchetype.PRICE_ONLY_RALLY.value,
    "EVENT_PREMIUM": E2RArchetype.EVENT_PREMIUM.value,
}

ROUND212_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "recurring_revenue_or_bookings",
    "arr_proxy_or_paid_usage",
    "arpu_or_take_rate_conversion",
    "opm_or_gross_margin_improvement",
    "fcf_conversion",
    "customer_retention_or_churn_stability",
    "ip_monetization_beyond_single_launch",
    "ai_feature_converts_to_paid_revenue_or_cost_saving",
    "privacy_security_governance_risk_passed",
    "price_path_after_evidence",
)

ROUND212_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "ai_partnership_headline_only",
    "ai_infra_capital_plan_only",
    "mau_without_arpu",
    "ipo_debut_premium_only",
    "mna_without_integration",
    "game_launch_first_week_only",
    "single_ip_dependence",
    "founder_legal_risk",
    "security_or_privacy_incident",
    "price_moved_before_monetization",
)

ROUND212_STAGE4B_WATCH_TRIGGERS: tuple[str, ...] = (
    "ai_partnership_announcement_spike",
    "ai_infra_kkr_mna_expectation_twenty_pct_spike",
    "ipo_debut_premium_before_profit",
    "webtoon_ip_valuation_before_paid_monetization",
    "game_launch_sales_before_retention",
    "kpop_comeback_expectation_over_governance_risk",
    "good_news_but_price_reaction_fades",
)

ROUND212_HARD_4C_GATES: tuple[str, ...] = (
    "privacy_breach",
    "security_outage",
    "founder_or_major_shareholder_legal_break",
    "regulatory_sanction",
    "ai_product_monetization_failure",
    "arr_churn_spike",
    "paid_user_decline",
    "game_launch_failure",
    "ip_litigation",
    "mna_integration_failure",
    "single_ip_collapse",
    "advertising_or_commerce_take_rate_damage",
    "fcf_deterioration_from_ai_capex",
)

ROUND212_PRICE_VALIDATION_FIELDS: tuple[str, ...] = (
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
    "relative_outperformance_pp",
    "ipo_price",
    "debut_price",
    "transaction_value",
    "arr_or_revenue_proxy",
    "price_validation_status",
)


@dataclass(frozen=True)
class Round212ScoreAdjustment:
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
class Round212CaseCandidate:
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
        return ROUND212_LARGE_SECTOR.value

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND212_SCORE_ADJUSTMENTS: tuple[Round212ScoreAdjustment, ...] = (
    Round212ScoreAdjustment("recurring_revenue", 5, "raise", "R8 Green은 반복매출이나 bookings가 확인될 때 가능하다."),
    Round212ScoreAdjustment("arr_proxy", 5, "raise", "ARR proxy는 SaaS/클라우드의 체급 변화를 보는 핵심 축이다."),
    Round212ScoreAdjustment("paid_usage_conversion", 5, "raise", "MAU보다 paid usage와 ARPU 전환이 중요하다."),
    Round212ScoreAdjustment("bookings_repeatability", 4, "raise", "게임·콘텐츠는 첫 주 판매보다 반복 bookings가 중요하다."),
    Round212ScoreAdjustment("enterprise_contract_quality", 4, "raise", "기업 AI/클라우드는 계약 품질과 고객 lock-in이 필요하다."),
    Round212ScoreAdjustment("opm_improvement", 5, "raise", "AI·클라우드 매출이 실제 OPM 개선으로 이어져야 한다."),
    Round212ScoreAdjustment("fcf_conversion", 5, "raise", "투자와 매출이 FCF로 전환되는지 확인해야 한다."),
    Round212ScoreAdjustment("customer_retention_or_churn", 4, "raise", "SaaS와 플랫폼은 churn 안정이 Stage 3 visibility다."),
    Round212ScoreAdjustment("ip_monetization_beyond_launch", 4, "raise", "신작·웹툰·K-pop은 반복 IP 수익화가 필요하다."),
    Round212ScoreAdjustment("operational_trust", 5, "raise", "플랫폼과 보안은 개인정보, 장애, 거버넌스 신뢰가 먼저다."),
    Round212ScoreAdjustment("ai_feature_only", -5, "lower", "AI 기능만 있고 유료 매출이나 비용절감이 없으면 제한한다."),
    Round212ScoreAdjustment("partnership_headline_only", -5, "lower", "제휴 헤드라인만으로는 Stage 3-Green을 만들 수 없다."),
    Round212ScoreAdjustment("mau_without_arpu", -4, "lower", "MAU만 있고 ARPU/paid usage가 없으면 제한한다."),
    Round212ScoreAdjustment("ipo_debut_premium", -4, "lower", "IPO 프리미엄은 수익성 확인 전 event premium이다."),
    Round212ScoreAdjustment("mna_without_integration", -4, "lower", "M&A는 integration과 시너지 확인 전 Stage 2다."),
    Round212ScoreAdjustment("ai_capex_without_revenue", -5, "lower", "AI capex가 매출·마진 없이 먼저 커지면 4B-watch다."),
    Round212ScoreAdjustment("game_launch_first_week_only", -4, "lower", "첫 주 판매만 있고 retention/bookings가 없으면 Green 금지다."),
    Round212ScoreAdjustment("single_ip_dependence", -4, "lower", "단일 IP 의존은 반복 monetization 전까지 risk cap이다."),
    Round212ScoreAdjustment("founder_legal_risk", -5, "lower", "창업자·대주주 legal risk는 콘텐츠/IP 매력을 먼저 차단한다."),
    Round212ScoreAdjustment("privacy_security_trust_break", -5, "lower", "개인정보·보안 신뢰 훼손은 플랫폼 hard gate다."),
)


ROUND212_CASE_CANDIDATES: tuple[Round212CaseCandidate, ...] = (
    Round212CaseCandidate(
        case_id="r8_loop8_douzone_bizon_eqt_saas",
        symbol="012510",
        company_name="더존비즈온",
        primary_archetype=E2RArchetype.B2B_SAAS_ERP_WORKFLOW,
        secondary_archetypes=(E2RArchetype.PRIVATE_EQUITY_SOFTWARE_RERATING, E2RArchetype.PLATFORM_SOFTWARE_INTERNET),
        case_type="success_candidate",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2025, 11, 7),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="stage3_requires_arr_proxy_churn_opm_fcf_and_customer_lock_in_not_eqt_transaction_alone",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("eqt_37_6pct_stake_acquisition", "cloud_erp_accounting_tax_compliance", "sme_lock_in_software_business", "long_term_operational_improvement_plan"),
        red_flag_fields=("transaction_event_not_recurring_revenue_proof", "arr_proxy_unverified", "churn_unverified", "regulatory_approval_required"),
        price_data_source="Reuters transaction evidence anchor",
        reported_price_anchor="Douzone Korea OHLC unavailable after deep search",
        reported_return_anchor="EQT $930M investment for 37.6% stake; implied equity value about $2.473B",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        extra_price_metrics={"eqt_investment_usd_mn": 930.0, "stake_acquired_pct": 37.6, "implied_equity_value_usd_bn": 2.473},
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="EQT investment supports Stage 2, but Stage 3 waits for ARR proxy, churn, OPM, and FCF conversion.",
    ),
    Round212CaseCandidate(
        case_id="r8_loop8_samsung_sds_kkr_ai_event",
        symbol="018260",
        company_name="삼성SDS",
        primary_archetype=E2RArchetype.AI_CLOUD_CAPITAL_ALLOCATION,
        secondary_archetypes=(E2RArchetype.CLOUD_AI_SOFTWARE_INFRA, E2RArchetype.EVENT_PREMIUM),
        case_type="event_premium",
        stage1_date=date(2025, 1, 1),
        stage2_date=date(2026, 4, 15),
        stage3_date=None,
        stage4b_date=date(2026, 4, 15),
        stage4c_date=None,
        stage3_decision="stage3_forbidden_until_ai_revenue_conversion_enterprise_contract_quality_opm_and_fcf_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("kkr_820m_usd_convertible_bond", "ai_infra_mna_capital_allocation_plan", "existing_cash_6_4tn_krw", "intraday_event_spike_20_8pct"),
        red_flag_fields=("ai_capex_without_revenue", "cb_dilution_watch", "mna_execution_unverified", "stablecoin_regulatory_risk"),
        price_data_source="Reuters reported event return anchor",
        reported_price_anchor="absolute price unavailable",
        reported_return_anchor="intraday +20.8%; morning trade +19.4%; KOSPI same context +3.0%",
        mfe_1d=20.8,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        extra_price_metrics={"stage2_event_mfe_1d_pct": 20.8, "morning_trade_return_pct": 19.4, "kospi_same_context_return_pct": 3.0, "relative_intraday_outperformance_vs_kospi_pp": 17.8, "cb_investment_usd_mn": 820.0, "cb_investment_krw_trn": 1.207, "existing_cash_krw_trn": 6.4, "combined_cash_cb_krw_trn": 7.607},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="stage2_watch_success",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="KKR/AI capital allocation is Stage 2 and 4B-watch; AI revenue conversion and FCF are required for Stage 3.",
    ),
    Round212CaseCandidate(
        case_id="r8_loop8_lg_cns_ai_cloud_ipo_failed_price",
        symbol="LG_CNS",
        company_name="LG CNS",
        primary_archetype=E2RArchetype.CLOUD_AI_SOFTWARE_INFRA,
        secondary_archetypes=(E2RArchetype.AI_SOFTWARE_APPLICATION, E2RArchetype.EVENT_PREMIUM),
        case_type="failed_rerating",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2025, 2, 5),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="cloud_ai_sales_mix_and_ipo_are_not_green_without_recurring_revenue_margin_retention_and_fcf",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("cloud_ai_services_over_half_sales", "large_ipo_1_2tn_krw", "enterprise_it_services"),
        red_flag_fields=("ipo_debut_price_failed", "recurring_cloud_revenue_unverified", "customer_retention_unverified", "fcf_unverified"),
        price_data_source="Reuters IPO price anchor",
        reported_price_anchor="IPO price 61,900 KRW; debut 59,700 KRW",
        reported_return_anchor="debut return -3.55%",
        mfe_1d=None,
        mae_1d=-3.55,
        stage2_price_anchor=61900.0,
        stage3_price_anchor=None,
        extra_price_metrics={"ipo_price_krw": 61900.0, "debut_price_krw": 59700.0, "debut_mae_pct": -3.55, "ipo_proceeds_krw_trn": 1.2, "cloud_ai_sales_mix_pct_min": 50.0},
        score_price_alignment="evidence_good_but_price_failed",
        rerating_result="no_rerating",
        stage_failure_type="false_yellow",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="Cloud/AI sales mix was real, but IPO price action failed; recurring revenue, margin, retention, and FCF are required.",
    ),
    Round212CaseCandidate(
        case_id="r8_loop8_naver_webtoon_ip_platform",
        symbol="035420",
        company_name="NAVER/Webtoon",
        primary_archetype=E2RArchetype.WEBTOON_PLATFORM_IP_MONETIZATION,
        secondary_archetypes=(E2RArchetype.PLATFORM_SOFTWARE_INTERNET, E2RArchetype.EVENT_PREMIUM),
        case_type="success_candidate",
        stage1_date=date(2024, 6, 1),
        stage2_date=date(2024, 6, 19),
        stage3_date=None,
        stage4b_date=date(2024, 6, 27),
        stage4c_date=None,
        stage3_decision="stage3_requires_paid_content_arpu_ip_licensing_operating_leverage_and_fcf_not_mau_or_ipo_valuation_alone",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("webtoon_ipo_2_7bn_usd_valuation", "webtoon_170m_mau", "webtoon_315m_usd_ipo_raise", "naver_holdco_discount_50pct"),
        red_flag_fields=("mau_without_arpu", "webtoon_net_loss", "holdco_discount", "paid_content_growth_unverified"),
        price_data_source="FT/MarketWatch/Investopedia reported price anchors",
        reported_price_anchor="Naver 165,300 KRW; Webtoon IPO $21, first close $23, next-day intraday high $25.66",
        reported_return_anchor="Naver -0.9%; Webtoon +9.5% first close, +22.2% from IPO to next-day intraday high",
        mfe_1d=22.2,
        mae_1d=-0.9,
        stage2_price_anchor=165300.0,
        stage3_price_anchor=None,
        extra_price_metrics={"naver_stage2_price_krw": 165300.0, "naver_event_mae_pct": -0.9, "naver_target_price_krw": 210000.0, "target_upside_pct": 27.0, "webtoon_ipo_price_usd": 21.0, "webtoon_first_day_close_usd": 23.0, "webtoon_first_day_close_return_pct": 9.5, "webtoon_next_day_intraday_high_usd": 25.66, "webtoon_mfe_from_ipo_to_intraday_high_pct": 22.2, "webtoon_revenue_prior_year_usd_bn": 1.28, "webtoon_net_loss_prior_year_usd_mn": 145.0, "net_loss_margin_pct": 11.3},
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="Webtoon MAU and IPO are Stage 2. Stage 3 requires paid content, ARPU, IP monetization, operating leverage, and FCF.",
    ),
    Round212CaseCandidate(
        case_id="r8_loop8_kakao_openai_ai_partnership",
        symbol="035720",
        company_name="카카오",
        primary_archetype=E2RArchetype.AI_SOFTWARE_APPLICATION,
        secondary_archetypes=(E2RArchetype.PLATFORM_SOFTWARE_INTERNET, E2RArchetype.PRICE_ONLY_RALLY),
        case_type="overheat",
        stage1_date=date(2025, 2, 4),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=date(2025, 2, 4),
        stage4c_date=None,
        stage3_decision="openai_partnership_is_stage1_or_4b_until_paid_ai_usage_arpu_opm_and_fcf_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("openai_kakao_partnership", "kakaotalk_97pct_domestic_share", "ai_product_expectation"),
        red_flag_fields=("partnership_headline_only", "price_moved_before_monetization", "paid_usage_unverified", "governance_overhang_watch"),
        price_data_source="Reuters event return anchor",
        reported_price_anchor="absolute price unavailable",
        reported_return_anchor="prior day +9%, announcement day -2%, peak-to-fade swing -11pp",
        mfe_1d=9.0,
        mae_1d=-2.0,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        extra_price_metrics={"event_mfe_prior_day_pct": 9.0, "event_mae_following_day_pct": -2.0, "two_session_cumulative_return_pct": 6.8, "event_fade_from_peak_pp": -11.0, "kakaotalk_domestic_market_share_pct": 97.0},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="false_yellow",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="OpenAI partnership is routing evidence, not Green; paid usage, ARPU, OPM, and FCF must appear first.",
    ),
    Round212CaseCandidate(
        case_id="r8_loop8_krafton_inzoi_adk_ip",
        symbol="259960",
        company_name="크래프톤",
        primary_archetype=E2RArchetype.GAME_CONTENT_IP_REPEAT_MONETIZATION,
        secondary_archetypes=(E2RArchetype.SINGLE_IP_RELEASE_EVENT_PREMIUM, E2RArchetype.GAME_CONTENT_IP),
        case_type="success_candidate",
        stage1_date=date(2025, 3, 28),
        stage2_date=date(2025, 4, 4),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="stage3_requires_retention_dlc_live_service_bookings_console_expansion_and_ip_extension_revenue",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("inzoi_first_week_sales_above_1m", "steam_global_top_seller", "adk_acquisition_516m_usd", "anime_ip_pipeline"),
        red_flag_fields=("game_launch_first_week_only", "retention_unverified", "single_ip_dependence", "mna_integration_unverified"),
        price_data_source="Reuters ADK transaction plus InZOI release/sales evidence",
        reported_price_anchor="Krafton Korea OHLC unavailable after deep search",
        reported_return_anchor="ADK 75B JPY / $516.21M; inZOI first-week sales above 1M copies",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        extra_price_metrics={"adk_transaction_value_jpy_bn": 75.0, "adk_transaction_value_usd_mn": 516.21, "inzoi_first_week_sales_mn": 1.0, "steam_peak_concurrent_players": 87377.0, "twitch_peak_viewers": 175000.0},
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="First-week sales and ADK acquisition support Stage 2. Stage 3 waits for repeat bookings, retention, and IP extension revenue.",
    ),
    Round212CaseCandidate(
        case_id="r8_loop8_hybe_legal_governance_watch",
        symbol="352820",
        company_name="HYBE",
        primary_archetype=E2RArchetype.PLATFORM_GOVERNANCE_LEGAL_RISK,
        secondary_archetypes=(E2RArchetype.KPOP_PLATFORM_CONTENT_IP, E2RArchetype.SECURITY_OPERATIONAL_TRUST_OVERLAY),
        case_type="failed_rerating",
        stage1_date=date(2024, 1, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2026, 4, 21),
        stage3_decision="content_ip_cannot_be_green_before_founder_legal_risk_artist_conflict_and_governance_trust_pass",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("bts_weverse_kpop_ip_expectation", "legal_event_price_reaction", "warrant_declined_relief"),
        red_flag_fields=("founder_legal_risk", "governance_legal_overhang", "artist_concentration_watch", "hard_4c_not_confirmed"),
        price_data_source="Reuters/AP legal event anchors",
        reported_price_anchor="absolute price unavailable",
        reported_return_anchor="HYBE -2.4% on detention warrant request; prosecutors later declined warrant request",
        mfe_1d=None,
        mae_1d=-2.4,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        extra_price_metrics={"stage4c_event_mae_1d_pct": -2.4, "alleged_profit_krw_bn": 190.0, "hard_4c_status": "not_confirmed_warrant_declined"},
        score_price_alignment="false_positive_score",
        rerating_result="thesis_break",
        stage_failure_type="should_have_been_red",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="Legal/governance risk blocks Green. Warrant decline means hard 4C is not confirmed, so this remains 4C-watch.",
    ),
)


def round212_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND212_CASE_CANDIDATES:
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
                "Round212 R8 Loop-8 platform/content/software/security price-path "
                "validation case. Calibration-only; not production scoring input."
            ),
            stage1_evidence=tuple(field for field in candidate.evidence_fields if "partnership" in field or "ipo" in field or "launch" in field or "expectation" in field),
            stage2_evidence=candidate.evidence_fields if candidate.stage2_date else (),
            stage3_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "recurring" in field
                or "arr" in field
                or "paid" in field
                or "bookings" in field
                or "revenue" in field
                or "lock_in" in field
                or "opm" in field
            ),
            stage4b_evidence=tuple(
                field
                for field in (*candidate.evidence_fields, *candidate.red_flag_fields)
                if "event" in field or "spike" in field or "price" in field or "ipo" in field or "premium" in field or "valuation" in field
            ),
            stage4c_evidence=tuple(
                field
                for field in candidate.red_flag_fields
                if "legal" in field
                or "governance" in field
                or "privacy" in field
                or "security" in field
                or "trust" in field
                or "retention" in field
                or "single_ip" in field
                or "fcf" in field
            ),
            must_have_fields=ROUND212_GREEN_REQUIRED_FIELDS,
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
                "recurring_revenue_delta": 5.0,
                "arr_proxy_delta": 5.0,
                "paid_usage_conversion_delta": 5.0,
                "bookings_repeatability_delta": 4.0,
                "enterprise_contract_quality_delta": 4.0,
                "opm_improvement_delta": 5.0,
                "fcf_conversion_delta": 5.0,
                "customer_retention_or_churn_delta": 4.0,
                "ip_monetization_beyond_launch_delta": 4.0,
                "operational_trust_delta": 5.0,
                "ai_feature_only_delta": -5.0,
                "partnership_headline_only_delta": -5.0,
                "mau_without_arpu_delta": -4.0,
                "ipo_debut_premium_delta": -4.0,
                "mna_without_integration_delta": -4.0,
                "ai_capex_without_revenue_delta": -5.0,
                "game_launch_first_week_only_delta": -4.0,
                "single_ip_dependence_delta": -4.0,
                "founder_legal_risk_delta": -5.0,
                "privacy_security_trust_break_delta": -5.0,
            },
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "full_ohlc_complete_false",
                "price_validation_partial_with_reported_price_anchors",
                "do_not_invent_price_or_stage_dates",
                "do_not_treat_ai_partnership_ipo_mna_first_week_sales_or_mau_as_green_alone",
                *ROUND212_GREEN_REQUIRED_FIELDS,
                *ROUND212_GREEN_FORBIDDEN_PATTERNS,
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
                stage_dates_confidence=0.8 if candidate.stage2_date or candidate.stage4c_date else 0.65,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round212_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND212_CASE_CANDIDATES:
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


def round212_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND212_SCORE_ADJUSTMENTS)


def round212_price_validation_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round212_price_validation": "true"} for field in ROUND212_PRICE_VALIDATION_FIELDS)


def round212_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {"round212_label": label, "canonical_archetype": canonical}
        for label, canonical in ROUND212_REQUIRED_TARGET_ALIASES.items()
    )


def round212_summary() -> dict[str, int | bool | str]:
    cases = ROUND212_CASE_CANDIDATES
    return {
        "source_round": ROUND212_SOURCE_ROUND_PATH,
        "large_sector": ROUND212_LARGE_SECTOR.value,
        "case_candidate_count": len(cases),
        "success_candidate_count": sum(1 for case in cases if case.case_type == "success_candidate"),
        "event_premium_count": sum(1 for case in cases if case.case_type == "event_premium"),
        "overheat_count": sum(1 for case in cases if case.case_type == "overheat"),
        "failed_rerating_count": sum(1 for case in cases if case.case_type == "failed_rerating"),
        "stage3_case_count": sum(1 for case in cases if case.stage3_date is not None),
        "stage4b_watch_count": sum(1 for case in cases if case.stage4b_status == "watch"),
        "hard_4c_case_count": sum(1 for case in cases if case.hard_4c_confirmed),
        "target_archetype_count": len(ROUND212_REQUIRED_TARGET_ALIASES),
        "price_validation_completed": "partial_with_reported_price_anchors",
        "full_ohlc_complete": False,
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
    }


def round212_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND212_SOURCE_ROUND_PATH,
        "large_sector": ROUND212_LARGE_SECTOR.value,
        "summary": round212_summary(),
        "target_aliases": dict(ROUND212_REQUIRED_TARGET_ALIASES),
        "green_required_fields": list(ROUND212_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND212_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_watch_triggers": list(ROUND212_STAGE4B_WATCH_TRIGGERS),
        "hard_4c_gates": list(ROUND212_HARD_4C_GATES),
        "what_not_to_change": [
            "do_not_use_round212_cases_as_candidate_generation_input",
            "do_not_apply_shadow_weights_to_production_scoring_yet",
            "do_not_treat_ai_partnership_ipo_mna_first_week_sales_or_mau_as_green",
            "do_not_invent_ohlc_or_stage_dates",
        ],
    }


def render_round212_summary_markdown() -> str:
    summary = round212_summary()
    lines = [
        "# Round 212 R8 Loop 8 Platform Content Software Security Price Validation",
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
        f"- overheat: {summary['overheat_count']}",
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
    for case in ROUND212_CASE_CANDIDATES:
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
            "- Douzone is a B2B SaaS Stage 2 candidate, but Stage 3 waits for ARR proxy, churn, OPM, and FCF.",
            "- Samsung SDS is Stage 2 and 4B-watch because price moved before AI revenue conversion.",
            "- LG CNS shows that cloud/AI evidence can still fail price validation at IPO.",
            "- NAVER/Webtoon needs paid content, ARPU, IP monetization, operating leverage, and FCF beyond MAU and IPO valuation.",
            "- Kakao/OpenAI is price-moved-without-evidence until paid AI usage and margin improve.",
            "- Krafton needs retention and repeat bookings beyond inZOI first-week sales.",
            "- HYBE remains governance/legal 4C-watch, not hard 4C, because the warrant was declined later.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round212_green_gate_review_markdown() -> str:
    lines = [
        "# Round 212 R8 Green Gate Review",
        "",
        "Do not apply these weights to production scoring yet.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND212_GREEN_REQUIRED_FIELDS)
    lines.extend(["", "## Forbidden Patterns", ""])
    lines.extend(f"- {field}" for field in ROUND212_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(
        [
            "",
            "## Easy Example",
            "- `AI partnership headline` means Stage 1 routing.",
            "- `AI product paid usage + ARPU + OPM/FCF` is the bundle that can support Stage 3.",
            "- `IPO pop or M&A announcement` is event premium until recurring revenue and integration proof exist.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round212_stage4b_4c_review_markdown() -> str:
    lines = [
        "# Round 212 R8 4B/4C Review",
        "",
        "## 4B Watch Triggers",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND212_STAGE4B_WATCH_TRIGGERS)
    lines.extend(["", "## Hard 4C Gates", ""])
    lines.extend(f"- {field}" for field in ROUND212_HARD_4C_GATES)
    lines.extend(["", "## Case Notes", ""])
    for case in ROUND212_CASE_CANDIDATES:
        if case.stage4b_status == "watch" or case.red_flag_fields:
            lines.append(f"- {case.case_id}: {', '.join(case.red_flag_fields)}")
    return "\n".join(lines) + "\n"


def render_round212_price_validation_plan_markdown() -> str:
    lines = [
        "# Round 212 R8 Price Validation Plan",
        "",
        "- price_validation_completed: partial_with_reported_price_anchors",
        "- full_ohlc_complete: false",
        "- Do not invent OHLC, peak, MFE, or MAE where raw adjusted daily prices are unavailable.",
        "",
        "## Backfill Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND212_PRICE_VALIDATION_FIELDS)
    return "\n".join(lines) + "\n"


def write_round212_r8_loop8_reports(
    output_directory: str | Path = ROUND212_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND212_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND212_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)

    paths = {
        "cases": write_case_library(round212_case_records(), cases_path),
        "audit": _write_json(round212_audit_payload(), audit_path),
        "summary": output / "round212_r8_loop8_price_validation_summary.md",
        "case_matrix": output / "round212_r8_loop8_case_matrix.csv",
        "target_aliases": output / "round212_r8_loop8_target_aliases.csv",
        "score_adjustments": output / "round212_r8_loop8_score_adjustments.csv",
        "price_validation_fields": output / "round212_r8_loop8_price_validation_fields.csv",
        "green_gate_review": output / "round212_r8_loop8_green_gate_review.md",
        "price_validation_plan": output / "round212_r8_loop8_price_validation_plan.md",
        "stage4b_4c_review": output / "round212_r8_loop8_stage4b_4c_review.md",
    }
    paths["summary"].write_text(render_round212_summary_markdown(), encoding="utf-8")
    _write_csv(round212_case_rows(), paths["case_matrix"])
    _write_csv(round212_target_alias_rows(), paths["target_aliases"])
    _write_csv(round212_score_adjustment_rows(), paths["score_adjustments"])
    _write_csv(round212_price_validation_field_rows(), paths["price_validation_fields"])
    paths["green_gate_review"].write_text(render_round212_green_gate_review_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round212_price_validation_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round212_stage4b_4c_review_markdown(), encoding="utf-8")
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
