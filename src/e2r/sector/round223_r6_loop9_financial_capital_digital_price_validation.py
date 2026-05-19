"""Round-223 R6 Loop-9 financial/capital/digital price validation pack.

Round 223 is calibration/evaluation material only. It converts
``docs/round/round_223.md`` into R6 case records, shadow weights, and
Green/4B/4C guardrails.

Easy example: ``low PBR + value-up policy`` is only Stage 1/2 attention.
It is not Stage 3-Green until ROE, CET1/K-ICS, repeated cancellation or
dividend execution, credit-cost control, and price-path confirmation are
visible as-of the case date.
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


ROUND223_SOURCE_ROUND_PATH = "docs/round/round_223.md"
ROUND223_ANALYST_ROUND_ID = "round_151"
ROUND223_LARGE_SECTOR = Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL
ROUND223_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round223_r6_loop9_financial_capital_digital_price_validation"
ROUND223_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r6_loop9_round223.jsonl"
ROUND223_DEFAULT_AUDIT_PATH = "data/sector_taxonomy/round223_r6_loop9_financial_capital_digital_price_validation_audit.json"

ROUND223_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "BANK_VALUEUP_ROE_PBR_RERATING": E2RArchetype.BANK_ROE_PBR_RERATING_KOREA.value,
    "BANK_CAPITAL_RETURN_EXECUTION": E2RArchetype.BANK_HOLDING_VALUEUP_CAPITAL_RETURN.value,
    "SECURITIES_CAPITAL_MARKET_BOOM": E2RArchetype.SECURITIES_BROKERAGE_MARKET_BETA.value,
    "HOLDING_NAV_DISCOUNT_VALUEUP": E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE.value,
    "INSURANCE_NAV_CAPITAL_RELEASE": E2RArchetype.INSURANCE_NAV_VALUEUP_SAMSUNG_ELECTRONICS_STAKE.value,
    "DIGITAL_ASSET_BANK_EQUITY_OPTION": E2RArchetype.DIGITAL_ASSET_BANK_EQUITY_OPTION.value,
    "DIGITAL_ASSET_PLATFORM_MERGER": E2RArchetype.DIGITAL_ASSET_EXCHANGE_CONSOLIDATION.value,
    "INTERNET_BANK_IPO_PROFITABILITY": E2RArchetype.INTERNET_BANK_PROFITABILITY.value,
    "INTERNET_BANK_GOVERNANCE_4C": E2RArchetype.PLATFORM_GOVERNANCE_LEGAL_RISK.value,
    "KRW_STABLECOIN_POLICY_THEME": E2RArchetype.KRW_STABLECOIN_POLICY_THEME.value,
    "PAYMENT_PRIVACY_REGULATORY_4C": E2RArchetype.PAYMENT_PRIVACY_REGULATORY_4C.value,
    "PRICE_ONLY_RALLY": E2RArchetype.PRICE_ONLY_RALLY.value,
    "EVENT_PREMIUM": E2RArchetype.EVENT_PREMIUM.value,
}

ROUND223_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "roe_improvement_or_sustainability",
    "cet1_kics_or_capital_buffer",
    "actual_buyback_cancellation_or_repeated_dividend_execution",
    "credit_cost_pf_risk_passed",
    "pbr_roe_gap_rerating_runway",
    "capital_release_or_nav_monetization_quality",
    "regulated_digital_revenue_or_equity_method_income",
    "privacy_data_governance_exchange_trust_passed",
    "price_path_after_evidence",
)

ROUND223_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "low_pbr_only",
    "policy_valueup_only",
    "treasury_buyback_without_cancellation",
    "stablecoin_policy_theme_only",
    "digital_asset_equity_option_without_revenue",
    "fintech_user_growth_without_profit",
    "internet_bank_ipo_without_listed_price_path",
    "major_shareholder_legal_risk",
    "privacy_data_or_exchange_trust_break",
    "capital_ratio_weakening_after_mna",
    "event_rally_before_regulated_revenue",
)

ROUND223_STAGE4B_WATCH_TRIGGERS: tuple[str, ...] = (
    "bank_or_insurance_trades_near_or_above_book_after_pbr_rerating",
    "buyback_cancellation_surprise_fades",
    "nav_rally_transfers_to_holding_or_insurance_without_monetization",
    "securities_basket_surges_on_trading_value_cycle",
    "stablecoin_related_basket_two_to_three_x_without_revenue",
    "digital_asset_stake_investment_at_exchange_volume_peak",
    "mna_or_stock_swap_priced_before_regulatory_approval",
)

ROUND223_HARD_4C_GATES: tuple[str, ...] = (
    "pf_credit_cost_spike",
    "cet1_or_kics_weakening",
    "buyback_cancellation_cancelled",
    "dividend_payout_retreat",
    "large_acquisition_capital_ratio_damage",
    "major_shareholder_suitability_risk",
    "financial_crime_or_governance_legal_break",
    "privacy_data_transfer_fine",
    "stablecoin_forex_risk_regulation_tightening",
    "digital_asset_volume_collapse",
    "exchange_security_incident_or_abnormal_withdrawal",
    "equity_stake_impairment",
)

ROUND223_PRICE_VALIDATION_FIELDS: tuple[str, ...] = (
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
    "event_swing_pp",
    "discount_to_nav_or_book",
    "transaction_value",
    "implied_equity_value",
    "reported_theme_basket_return",
    "regulated_revenue_confirmed",
    "issuer_license_confirmed",
    "exchange_trust_incident",
    "price_validation_status",
)


@dataclass(frozen=True)
class Round223ScoreAdjustment:
    axis: str
    points: int
    direction: str
    reason: str

    def as_row(self) -> dict[str, str]:
        return {"axis": self.axis, "points": str(self.points), "direction": self.direction, "reason": self.reason}


@dataclass(frozen=True)
class Round223ShadowWeightRow:
    archetype: E2RArchetype
    roe: int
    capital_buffer: int
    buyback_cancel: int
    shareholder_return: int
    pbr_roe_gap: int
    credit_cost: int
    regulated_revenue: int
    nav_monetization: int
    event_penalty: int
    privacy_governance_redteam: int
    stage4b_watch_sensitivity: int
    hard4c_sensitivity: int
    notes: str

    def as_row(self) -> dict[str, str]:
        return {
            "archetype": self.archetype.value,
            "roe": _signed_int_text(self.roe),
            "capital_buffer": _signed_int_text(self.capital_buffer),
            "buyback_cancel": _signed_int_text(self.buyback_cancel),
            "shareholder_return": _signed_int_text(self.shareholder_return),
            "pbr_roe_gap": _signed_int_text(self.pbr_roe_gap),
            "credit_cost": _signed_int_text(self.credit_cost),
            "regulated_revenue": _signed_int_text(self.regulated_revenue),
            "nav_monetization": _signed_int_text(self.nav_monetization),
            "event_penalty": _signed_int_text(self.event_penalty),
            "privacy_governance_redteam": _signed_int_text(self.privacy_governance_redteam),
            "4b_watch_sensitivity": _signed_int_text(self.stage4b_watch_sensitivity),
            "hard4c_sensitivity": _signed_int_text(self.hard4c_sensitivity),
            "notes": self.notes,
        }


@dataclass(frozen=True)
class Round223CaseCandidate:
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
    stage4b_price_anchor: float | None
    stage4c_price_anchor: float | None
    peak_price_anchor: float | None
    extra_price_metrics: Mapping[str, float | str | bool]
    score_price_alignment: str
    rerating_result: str
    stage_failure_type: str
    price_validation_status: str
    notes: str

    @property
    def large_sector(self) -> str:
        return ROUND223_LARGE_SECTOR.value

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND223_SCORE_ADJUSTMENTS: tuple[Round223ScoreAdjustment, ...] = (
    Round223ScoreAdjustment("roe_sustainability", 5, "raise", "저PBR보다 ROE가 유지되거나 개선되는지가 PBR 프레임 변화의 핵심이다."),
    Round223ScoreAdjustment("cet1_or_capital_buffer", 5, "raise", "은행 CET1과 보험 K-ICS/CSM buffer가 있어야 환원과 인수가 지속된다."),
    Round223ScoreAdjustment("real_buyback_cancellation", 5, "raise", "자사주 매입보다 실제 소각이 자본배분 실행 증거다."),
    Round223ScoreAdjustment("dividend_payout_visibility", 4, "raise", "배당과 소각이 반복 policy로 고정될 때 신뢰도가 올라간다."),
    Round223ScoreAdjustment("credit_cost_control", 5, "raise", "PF와 credit cost가 안정돼야 금융주 rerating이 지속된다."),
    Round223ScoreAdjustment("pbr_roe_gap", 4, "raise", "ROE 대비 PBR discount가 줄어들 여지가 있어야 한다."),
    Round223ScoreAdjustment("capital_release_quality", 4, "raise", "보험/지주 NAV는 매각대금 활용과 자본 release가 확인될 때 강해진다."),
    Round223ScoreAdjustment("regulated_revenue_visibility", 4, "raise", "디지털자산/결제는 실제 수수료, 지분법, reserve income이 필요하다."),
    Round223ScoreAdjustment("nav_discount_with_monetization", 4, "raise", "NAV discount는 소각/배당/자산화로 이어질 때만 강하다."),
    Round223ScoreAdjustment("digital_asset_equity_value_with_regulation", 3, "raise", "디지털자산 지분 옵션은 규제 승인과 수익화 구조가 붙어야 한다."),
    Round223ScoreAdjustment("low_pbr_only", -5, "lower", "저PBR만으로는 Stage 3-Green을 만들 수 없다."),
    Round223ScoreAdjustment("policy_valueup_only", -4, "lower", "밸류업 정책 기대만 있고 실행이 없으면 Stage 1 attention이다."),
    Round223ScoreAdjustment("treasury_buyback_without_cancellation", -4, "lower", "자사주 매입만 있고 소각이 없으면 자본배분 품질을 제한한다."),
    Round223ScoreAdjustment("stablecoin_policy_theme_only", -5, "lower", "스테이블코인 정책 테마만으로는 규제수익을 증명하지 못한다."),
    Round223ScoreAdjustment("digital_asset_equity_option_without_revenue", -3, "lower", "지분 옵션만 있고 지분법/수수료/거래량 지속성이 없으면 Green 금지다."),
    Round223ScoreAdjustment("fintech_user_growth_without_profit", -3, "lower", "사용자 수 성장만 있고 take-rate/이익이 없으면 제한한다."),
    Round223ScoreAdjustment("privacy_or_data_trust_break", -5, "lower", "개인정보·데이터·거래소 신뢰 훼손은 핀테크 hard gate다."),
    Round223ScoreAdjustment("major_shareholder_legal_risk", -5, "lower", "인터넷은행은 대주주 적격성 리스크가 성장성보다 먼저다."),
    Round223ScoreAdjustment("capital_ratio_weakening", -4, "lower", "대형 인수나 비은행 확장이 자본비율을 훼손하면 제한한다."),
    Round223ScoreAdjustment("mna_expansion_without_capital_buffer", -3, "lower", "M&A 확장은 자본 buffer와 수익성을 확인하기 전 Stage 2 watch다."),
    Round223ScoreAdjustment("event_rally_before_regulated_revenue", -5, "lower", "규제수익 전 가격 급등은 4B/event premium이다."),
)


ROUND223_SHADOW_WEIGHT_ROWS: tuple[Round223ShadowWeightRow, ...] = (
    Round223ShadowWeightRow(E2RArchetype.BANK_ROE_PBR_RERATING_KOREA, 5, 5, 4, 5, 5, 5, 0, 0, -3, 2, 4, 4, "KB/bank value-up needs ROE, CET1, credit cost, and repeated return execution."),
    Round223ShadowWeightRow(E2RArchetype.SECURITIES_BROKERAGE_MARKET_BETA, 4, 3, 0, 2, 3, 3, 0, 0, -3, 2, 5, 4, "Securities +13.5% is cyclical until brokerage/IB revenue and ROE confirm."),
    Round223ShadowWeightRow(E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE, 2, 2, 5, 5, 5, 1, 0, 5, -2, 2, 4, 3, "SK Square needs actual cancellation and discount narrowing."),
    Round223ShadowWeightRow(E2RArchetype.INSURANCE_NAV_VALUEUP_SAMSUNG_ELECTRONICS_STAKE, 3, 5, 1, 4, 5, 3, 0, 5, -2, 3, 4, 4, "Samsung Life needs use of proceeds and K-ICS/CSM confirmation."),
    Round223ShadowWeightRow(E2RArchetype.DIGITAL_ASSET_BANK_EQUITY_OPTION, 2, 4, 0, 1, 2, 2, 5, 2, -3, 4, 5, 4, "Hana/Dunamu is Stage 2 until regulated revenue and capital impact confirm."),
    Round223ShadowWeightRow(E2RArchetype.DIGITAL_ASSET_EXCHANGE_CONSOLIDATION, 2, 3, 0, 1, 2, 2, 5, 1, -4, 5, 5, 5, "Naver/Dunamu has exchange-trust 4C-watch from abnormal withdrawal."),
    Round223ShadowWeightRow(E2RArchetype.INTERNET_BANK_PROFITABILITY, 5, 4, 0, 1, 4, 5, 2, 0, -4, 3, 5, 4, "K Bank IPO candidate needs listed price path, ROE/NIM/credit quality."),
    Round223ShadowWeightRow(E2RArchetype.PLATFORM_GOVERNANCE_LEGAL_RISK, 0, 0, 0, 0, 0, 0, 0, 0, -3, 5, 3, 5, "KakaoBank Green is blocked by major shareholder legal/ownership risk."),
    Round223ShadowWeightRow(E2RArchetype.KRW_STABLECOIN_POLICY_THEME, 0, 1, 0, 0, 1, 0, 1, 0, -5, 4, 5, 4, "Stablecoin rally is price_moved_without_evidence until licensing/revenue clarity."),
)


ROUND223_CASE_CANDIDATES: tuple[Round223CaseCandidate, ...] = (
    Round223CaseCandidate(
        case_id="r6_loop9_kb_financial_bank_valueup",
        symbol="105560",
        company_name="KB금융",
        primary_archetype=E2RArchetype.BANK_ROE_PBR_RERATING_KOREA,
        secondary_archetypes=(E2RArchetype.BANK_HOLDING_VALUEUP_CAPITAL_RETURN, E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN),
        case_type="success_candidate",
        stage1_date=date(2024, 2, 1),
        stage2_date=date(2025, 1, 1),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="stage3_requires_roe_cet1_credit_cost_repeated_cancellation_and_dividend_execution_not_low_pbr_alone",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("corporate_valueup_programme", "kb_2025_net_profit_5_84tn_krw", "kb_net_profit_growth_15_1pct", "big4_profit_nearly_18tn_krw", "book_value_breakthrough_reported"),
        red_flag_fields=("source_confidence_medium_low", "roe_cet1_credit_cost_unverified", "repeated_shareholder_return_execution_unverified", "price_data_unavailable_after_deep_search"),
        price_data_source="public company profile / KED-derived summary via indexed source",
        reported_price_anchor="KB reportedly traded above book value; stock OHLC unavailable",
        reported_return_anchor="2025 net profit 5.84T KRW, +15.1%; Big4 financial groups nearly 18T KRW",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"kb_2025_net_profit_krw_trn": 5.84, "kb_net_profit_growth_pct": 15.1, "big4_2025_net_profit_krw_trn": 18.0, "kb_share_of_big4_profit_pct": 32.4, "book_value_breakthrough_reported": True, "source_confidence": "medium_low"},
        score_price_alignment="unknown",
        rerating_result="policy_event_rerating",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Value-up Stage 2 candidate; Stage 3 requires ROE/CET1/credit cost and repeated shareholder return execution.",
    ),
    Round223CaseCandidate(
        case_id="r6_loop9_securities_financial_basket_capital_market_boom",
        symbol="securities_basket/financial_groups_basket",
        company_name="증권주/금융주 basket",
        primary_archetype=E2RArchetype.SECURITIES_BROKERAGE_MARKET_BETA,
        secondary_archetypes=(E2RArchetype.SECURITIES_BROKERAGE_CYCLE, E2RArchetype.BANK_ROE_PBR_RERATING_KOREA, E2RArchetype.VALUE_UP_CROWDED_4B_WATCH),
        case_type="cyclical_success",
        stage1_date=date(2025, 1, 1),
        stage2_date=date(2026, 5, 6),
        stage3_date=None,
        stage4b_date=date(2026, 5, 6),
        stage4c_date=None,
        stage3_decision="securities_market_cycle_is_stage2_cyclical_until_brokerage_ib_revenue_roe_and_risk_controls_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("kospi_event_return_6_45pct", "kospi_intraday_high_return_7_06pct", "securities_firms_plus_13_5pct", "financial_groups_plus_4_2pct", "foreign_net_purchase_3_1tn_krw"),
        red_flag_fields=("brokerage_ib_revenue_unverified", "market_cycle_revenue_not_structural", "margin_loan_unwind_watch", "price_moved_before_company_level_roe"),
        price_data_source="Reuters reported market-sector return anchors",
        reported_price_anchor="sector basket absolute prices unavailable",
        reported_return_anchor="KOSPI +6.45%, securities +13.5%, financial groups +4.2%, foreign net purchase 3.1T KRW",
        mfe_1d=13.5,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"kospi_event_return_pct": 6.45, "kospi_intraday_high_return_pct": 7.06, "securities_firms_mfe_1d_pct": 13.5, "financial_groups_mfe_1d_pct": 4.2, "securities_relative_outperformance_pp": 7.05, "financial_groups_relative_underperformance_pp": -2.25, "foreign_net_purchase_krw_trn": 3.1},
        score_price_alignment="aligned",
        rerating_result="cyclical_rerating",
        stage_failure_type="stage2_watch_success",
        price_validation_status="reported_sector_return_not_full_ohlc",
        notes="Securities rally is Stage 2/cyclical; brokerage/IB revenue, ROE and risk controls required before Green.",
    ),
    Round223CaseCandidate(
        case_id="r6_loop9_sk_square_nav_discount_valueup",
        symbol="402340",
        company_name="SK스퀘어",
        primary_archetype=E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE,
        secondary_archetypes=(E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN, E2RArchetype.TREASURY_SHARE_CANCEL_EXECUTION, E2RArchetype.VALUE_UP_CROWDED_4B_WATCH),
        case_type="success_candidate",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2024, 11, 21),
        stage3_date=None,
        stage4b_date=date(2026, 5, 1),
        stage4c_date=None,
        stage3_decision="stage3_requires_repeated_cancellation_discount_narrowing_and_nav_monetization_not_underlying_skhynix_rally_only",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("buyback_cancelled_100bn_krw", "additional_buyback_cancel_plan_100bn_krw", "sk_hynix_stake_20pct", "sk_hynix_stake_value_18bn_usd", "barrons_discount_47pct"),
        red_flag_fields=("sk_hynix_price_dependency", "discount_narrowing_price_path_unverified", "repeated_cancellation_unverified", "nav_trade_crowding_watch"),
        price_data_source="Reuters / Barron's valuation anchors",
        reported_price_anchor="stock OHLC unavailable; 47% to >50% discount valuation anchors",
        reported_return_anchor="200B KRW buyback/cancel programme; SK Hynix stake 20%; discount 47% in 2026 view",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"cancelled_buyback_krw_bn": 100.0, "additional_buyback_cancel_plan_krw_bn": 100.0, "total_buyback_cancel_program_krw_bn": 200.0, "sk_hynix_stake_pct": 20.0, "sk_hynix_stake_value_2024_usd_bn": 18.0, "minimum_nav_discount_2024_pct": 50.0, "barrons_discount_2026_pct": 47.0, "implied_value_capture_ratio_2026_pct": 53.0},
        score_price_alignment="unknown",
        rerating_result="policy_event_rerating",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Actual cancellation supports Stage 2; repeated cancellation and discount narrowing required for Stage 3.",
    ),
    Round223CaseCandidate(
        case_id="r6_loop9_samsung_life_nav_capital_release",
        symbol="032830",
        company_name="삼성생명",
        primary_archetype=E2RArchetype.INSURANCE_NAV_VALUEUP_SAMSUNG_ELECTRONICS_STAKE,
        secondary_archetypes=(E2RArchetype.INSURANCE_CAPITAL_RELEASE_VALUEUP, E2RArchetype.INSURANCE_KICS_CSM_GATE, E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN),
        case_type="success_candidate",
        stage1_date=date(2025, 1, 1),
        stage2_date=date(2026, 3, 19),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="stage3_requires_use_of_proceeds_shareholder_return_kics_csm_and_core_insurance_profit",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("samsung_electronics_stake_sale_1_3tn_krw", "samsung_electronics_stake_owned_about_10pct", "book_value_discount_about_50pct", "regulatory_capital_release_watch"),
        red_flag_fields=("use_of_proceeds_unverified", "kics_csm_unverified", "regulatory_forced_sale_risk", "samsung_electronics_nav_dependency"),
        price_data_source="Reuters / Barron's valuation anchors",
        reported_price_anchor="stock OHLC unavailable; about 50% of book value valuation anchor",
        reported_return_anchor="Samsung Electronics stake sale 1.3T KRW; Samsung Electronics stake about 10%",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"samsung_electronics_stake_sale_krw_trn": 1.3, "samsung_electronics_stake_sale_usd_mn": 867.07, "samsung_electronics_stake_owned_pct": 10.0, "trading_level_vs_book_pct": 50.0, "implied_book_discount_pct": 50.0},
        score_price_alignment="unknown",
        rerating_result="policy_event_rerating",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Hidden NAV and capital release are Stage 2; use of proceeds, K-ICS/CSM and shareholder return required for Stage 3.",
    ),
    Round223CaseCandidate(
        case_id="r6_loop9_hana_dunamu_equity_option",
        symbol="086790",
        company_name="하나금융/하나은행",
        primary_archetype=E2RArchetype.DIGITAL_ASSET_BANK_EQUITY_OPTION,
        secondary_archetypes=(E2RArchetype.BANK_DIGITAL_ASSET_EQUITY_STAKE, E2RArchetype.REGULATED_STABLECOIN_INFRA, E2RArchetype.BANK_HOLDING_VALUEUP_CAPITAL_RETURN),
        case_type="success_candidate",
        stage1_date=date(2025, 1, 1),
        stage2_date=date(2026, 5, 14),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="stage3_requires_equity_method_income_regulatory_approval_capital_ratio_impact_and_exchange_volume_durability",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("dunamu_stake_acquired_6_55pct", "transaction_value_1_003tn_krw", "implied_dunamu_equity_value_15_31tn_krw", "upbit_trading_volume_share_over_80pct", "blockchain_remittance_poc"),
        red_flag_fields=("equity_method_income_unverified", "regulatory_approval_unverified", "capital_ratio_impact_unverified", "exchange_trust_incident_watch"),
        price_data_source="Reuters / WSJ transaction anchors",
        reported_price_anchor="Hana stock OHLC unavailable",
        reported_return_anchor="1.003T KRW for 6.55% stake; implied Dunamu equity value about 15.31T KRW",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"transaction_value_krw_trn": 1.003, "stake_acquired_pct": 6.55, "implied_dunamu_equity_value_krw_trn": 15.31, "shares_acquired_mn": 2.284, "price_per_dunamu_share_krw": 439142.0, "upbit_trading_volume_share_pct": 80.0, "kakao_investment_remaining_stake_pct": 4.03},
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Dunamu stake is Stage 2; regulated revenue, equity-method earnings, capital impact and exchange trust required for Stage 3.",
    ),
    Round223CaseCandidate(
        case_id="r6_loop9_naver_dunamu_platform_merger_trust_watch",
        symbol="035420",
        company_name="NAVER / NAVER Financial / Dunamu",
        primary_archetype=E2RArchetype.DIGITAL_ASSET_EXCHANGE_CONSOLIDATION,
        secondary_archetypes=(E2RArchetype.DIGITAL_ASSET_TOKENIZATION, E2RArchetype.EXCHANGE_SECURITY_OPERATIONAL_RISK, E2RArchetype.EVENT_PREMIUM),
        case_type="event_premium",
        stage1_date=date(2025, 1, 1),
        stage2_date=date(2025, 11, 27),
        stage3_date=None,
        stage4b_date=date(2025, 11, 27),
        stage4c_date=date(2025, 11, 27),
        stage3_decision="stage3_requires_regulatory_approval_closing_revenue_integration_volume_durability_and_exchange_trust",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("naver_financial_dunamu_all_stock_deal_15_13tn_krw", "upbit_market_share_about_70pct", "event_initial_plus_7pct", "exchange_ratio_2_54"),
        red_flag_fields=("abnormal_withdrawal_54bn_krw", "event_mae_same_day_minus_4_2pct", "regulatory_approval_unverified", "exchange_trust_4c_watch"),
        price_data_source="Reuters event-return and transaction anchors",
        reported_price_anchor="absolute price unavailable",
        reported_return_anchor="initially >+7%, then -4.2% after Upbit abnormal withdrawal; deal value 15.13T KRW",
        mfe_1d=7.0,
        mae_1d=-4.2,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"deal_value_krw_trn": 15.13, "deal_value_usd_bn": 10.27, "event_mfe_initial_pct": 7.0, "event_mae_same_day_pct": -4.2, "event_swing_pp": -11.2, "abnormal_withdrawal_krw_bn": 54.0, "exchange_ratio_naver_financial_per_dunamu": 2.54, "upbit_market_share_pct": 70.0},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="stage2_watch_success",
        price_validation_status="reported_event_return_not_full_ohlc",
        notes="Strong Stage 2 digital-asset merger, but abnormal withdrawal creates exchange-trust 4C-watch.",
    ),
    Round223CaseCandidate(
        case_id="r6_loop9_kbank_internet_bank_ipo_watch",
        symbol="unlisted_KBank",
        company_name="K Bank",
        primary_archetype=E2RArchetype.INTERNET_BANK_PROFITABILITY,
        secondary_archetypes=(E2RArchetype.FINTECH_IPO_VALUATION_RISK, E2RArchetype.FINTECH_SUPERAPP_IPO_OPTION_KOREA),
        case_type="success_candidate",
        stage1_date=date(2024, 9, 10),
        stage2_date=date(2024, 9, 10),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="ipo_plan_and_operating_profit_are_stage2_until_listed_price_path_roe_nim_credit_cost_and_fee_income_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("ipo_raise_max_984bn_krw", "ipo_price_range_9500_12000", "valuation_up_to_5tn_krw", "h1_2024_operating_profit_86_7bn_krw", "customers_over_10mn"),
        red_flag_fields=("unlisted_no_stock_ohlc", "listed_price_path_unverified", "roe_nim_credit_quality_unverified", "ipo_valuation_risk"),
        price_data_source="Reuters IPO plan anchor",
        reported_price_anchor="unlisted / IPO candidate at report date",
        reported_return_anchor="IPO max 984B KRW; valuation up to 5T KRW; 1H 2024 operating profit 86.7B KRW",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"ipo_raise_max_krw_bn": 984.0, "ipo_price_range_krw": "9500-12000", "shares_to_sell_mn": 82.0, "new_shares_mn": 41.0, "existing_shares_mn": 41.0, "max_offer_value_check_krw_bn": 984.0, "shares_outstanding_mn": 376.0, "implied_market_cap_at_12000_krw_trn": 4.512, "reported_valuation_up_to_krw_trn": 5.0, "h1_2024_operating_profit_krw_bn": 86.7, "customer_count_mn": 10.0},
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="unlisted_no_stock_ohlc",
        notes="IPO profitability Stage 2 candidate; listed price path, ROE/NIM/credit cost required before Green.",
    ),
    Round223CaseCandidate(
        case_id="r6_loop9_kakao_kakaobank_legal_governance_watch",
        symbol="035720/323410",
        company_name="Kakao / KakaoBank",
        primary_archetype=E2RArchetype.PLATFORM_GOVERNANCE_LEGAL_RISK,
        secondary_archetypes=(E2RArchetype.INTERNET_BANK_PROFITABILITY, E2RArchetype.PAYMENT_FINTECH_INFRA),
        case_type="4c_thesis_break",
        stage1_date=date(2021, 1, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2024, 7, 23),
        stage3_decision="internet_bank_growth_is_blocked_until_major_shareholder_legal_and_ownership_risk_clear",
        stage4b_status="none",
        hard_4c_confirmed=False,
        evidence_fields=("kakaobank_mobile_banking_scale", "kakao_ecosystem_financial_platform"),
        red_flag_fields=("kakao_founder_arrest", "major_shareholder_legal_risk", "bank_ownership_cap_risk_over_10pct", "kakao_ytd_drawdown_24pct", "legal_relief_2025_10_21"),
        price_data_source="Reuters legal event anchors",
        reported_price_anchor="KakaoBank OHLC unavailable; Kakao event return available",
        reported_return_anchor="Kakao -3.4% event move, YTD -24%; bank ownership cap risk if convicted",
        mfe_1d=None,
        mae_1d=-3.4,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"kakao_event_mae_1d_pct": -3.4, "kakao_ytd_drawdown_context_pct": -24.0, "kakao_group_assets_krw_trn": 86.0, "kim_controlled_stake_pct": 24.0, "bank_ownership_cap_risk_pct": 10.0, "legal_relief_date": "2025-10-21 acquittal"},
        score_price_alignment="evidence_good_but_price_failed",
        rerating_result="thesis_break",
        stage_failure_type="should_have_been_red",
        price_validation_status="reported_event_return_not_full_ohlc_for_kakao_kakaobank_ohlc_unavailable",
        notes="Major shareholder legal risk blocks KakaoBank Green until ownership-risk and profitability metrics clear.",
    ),
    Round223CaseCandidate(
        case_id="r6_loop9_stablecoin_policy_theme_overheat",
        symbol="377300/LG_CNS/158430/ME2ON",
        company_name="Kakao Pay / stablecoin basket",
        primary_archetype=E2RArchetype.KRW_STABLECOIN_POLICY_THEME,
        secondary_archetypes=(E2RArchetype.DIGITAL_ASSET_THEME_OVERHEAT, E2RArchetype.PRICE_ONLY_RALLY, E2RArchetype.STABLECOIN_REGULATORY_ECONOMICS),
        case_type="overheat",
        stage1_date=date(2025, 6, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=date(2025, 6, 1),
        stage4c_date=None,
        stage3_decision="stablecoin_policy_theme_is_not_green_before_issuer_license_reserve_income_fee_revenue_and_regulatory_capital",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("won_stablecoin_policy_pledge", "digital_asset_reform_expectation", "kakao_pay_more_than_2x", "lg_cns_plus_70pct", "aton_plus_80pct", "me2on_3x"),
        red_flag_fields=("stablecoin_policy_theme_only", "regulated_revenue_confirmed_false", "issuer_license_confirmed_false", "reserve_income_confirmed_false", "foreign_exchange_risk_regulatory_watch"),
        price_data_source="FT reported return anchors",
        reported_price_anchor="absolute prices unavailable",
        reported_return_anchor="Kakao Pay >2x, LG CNS +70%, Aton +80%, ME2ON 3x before regulated revenue clarity",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"kakao_pay_mfe_month_pct": 100.0, "lg_cns_mfe_month_pct": 70.0, "aton_mfe_month_pct": 80.0, "me2on_mfe_month_pct": 200.0, "margin_loan_context_krw_trn": 20.5, "regulated_revenue_confirmed": False, "issuer_license_confirmed": False, "reserve_income_confirmed": False},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="theme_overheat",
        stage_failure_type="false_yellow",
        price_validation_status="reported_return_anchor_not_full_ohlc",
        notes="Stablecoin theme rallied before licensed issuer, reserve income, fee revenue or regulatory capital clarity.",
    ),
)


def round223_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND223_CASE_CANDIDATES:
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
                "Round223 R6 Loop-9 financial/capital/digital price-path validation. "
                "Calibration-only; not production scoring input."
            ),
            stage1_evidence=tuple(field for field in candidate.evidence_fields if "policy" in field or "programme" in field or "ipo" in field or "platform" in field or "theme" in field),
            stage2_evidence=candidate.evidence_fields if candidate.stage2_date else (),
            stage3_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "profit" in field
                or "roe" in field
                or "cet1" in field
                or "kics" in field
                or "buyback" in field
                or "cancel" in field
                or "capital" in field
                or "regulated" in field
            ),
            stage4b_evidence=tuple(
                field
                for field in (*candidate.evidence_fields, *candidate.red_flag_fields)
                if "plus" in field
                or "2x" in field
                or "3x" in field
                or "rally" in field
                or "theme" in field
                or "book_value" in field
                or "crowding" in field
            ),
            stage4c_evidence=tuple(
                field
                for field in candidate.red_flag_fields
                if "risk" in field
                or "weakening" in field
                or "withdrawal" in field
                or "trust" in field
                or "legal" in field
                or "privacy" in field
                or "credit" in field
                or "pf" in field
            ),
            must_have_fields=ROUND223_GREEN_REQUIRED_FIELDS,
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
            score_weight_hint={f"{item.axis}_delta": float(item.points) for item in ROUND223_SCORE_ADJUSTMENTS},
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "full_ohlc_complete_false",
                "price_validation_partial_with_reported_price_anchors",
                "do_not_invent_ohlc_stage_prices_or_business_metrics",
                "do_not_treat_low_pbr_valueup_stablecoin_digital_asset_or_ipo_theme_as_green_alone",
                *ROUND223_GREEN_REQUIRED_FIELDS,
                *ROUND223_GREEN_FORBIDDEN_PATTERNS,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(
                stage2_price=candidate.stage2_price_anchor,
                stage3_price=candidate.stage3_price_anchor,
                stage4b_price=candidate.stage4b_price_anchor,
                stage4c_price=candidate.stage4c_price_anchor,
                peak_price=candidate.peak_price_anchor,
                mfe_30d=candidate.mfe_1d,
                mae_30d=candidate.mae_1d,
                price_validation_status=candidate.price_validation_status,
            ),
            data_quality=CaseDataQuality(
                official_data_available=True,
                report_data_available=True,
                price_data_available=(
                    candidate.stage2_price_anchor is not None
                    or candidate.stage3_price_anchor is not None
                    or candidate.mfe_1d is not None
                    or candidate.mae_1d is not None
                ),
                stage_dates_confidence=0.82 if candidate.stage2_date or candidate.stage4c_date else 0.65,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round223_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND223_CASE_CANDIDATES:
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
                "stage2_price": _float_text(candidate.stage2_price_anchor),
                "stage3_price": _float_text(candidate.stage3_price_anchor),
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


def round223_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND223_SCORE_ADJUSTMENTS)


def round223_shadow_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(row.as_row() for row in ROUND223_SHADOW_WEIGHT_ROWS)


def round223_price_validation_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round223_price_validation": "true"} for field in ROUND223_PRICE_VALIDATION_FIELDS)


def round223_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple({"round223_label": label, "canonical_archetype": canonical} for label, canonical in ROUND223_REQUIRED_TARGET_ALIASES.items())


def round223_summary() -> dict[str, int | bool | str]:
    cases = ROUND223_CASE_CANDIDATES
    return {
        "source_round": ROUND223_SOURCE_ROUND_PATH,
        "analyst_round_id": ROUND223_ANALYST_ROUND_ID,
        "large_sector": ROUND223_LARGE_SECTOR.value,
        "case_candidate_count": len(cases),
        "success_candidate_count": sum(1 for case in cases if case.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for case in cases if case.case_type == "cyclical_success"),
        "event_premium_count": sum(1 for case in cases if case.case_type == "event_premium"),
        "overheat_count": sum(1 for case in cases if case.case_type == "overheat"),
        "thesis_break_count": sum(1 for case in cases if case.case_type == "4c_thesis_break"),
        "stage3_case_count": sum(1 for case in cases if case.stage3_date is not None),
        "stage4b_watch_count": sum(1 for case in cases if case.stage4b_status == "watch"),
        "stage4c_watch_count": sum(1 for case in cases if case.stage4c_date is not None and not case.hard_4c_confirmed),
        "hard_4c_case_count": sum(1 for case in cases if case.hard_4c_confirmed),
        "target_archetype_count": len(ROUND223_REQUIRED_TARGET_ALIASES),
        "shadow_weight_row_count": len(ROUND223_SHADOW_WEIGHT_ROWS),
        "price_validation_completed": "partial_with_reported_price_anchors",
        "full_ohlc_complete": False,
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
    }


def round223_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND223_SOURCE_ROUND_PATH,
        "analyst_round_id": ROUND223_ANALYST_ROUND_ID,
        "large_sector": ROUND223_LARGE_SECTOR.value,
        "summary": round223_summary(),
        "target_aliases": dict(ROUND223_REQUIRED_TARGET_ALIASES),
        "green_required_fields": list(ROUND223_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND223_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_watch_triggers": list(ROUND223_STAGE4B_WATCH_TRIGGERS),
        "hard_4c_gates": list(ROUND223_HARD_4C_GATES),
        "score_adjustments": list(round223_score_adjustment_rows()),
        "shadow_weights": list(round223_shadow_weight_rows()),
        "case_ids": [case.case_id for case in ROUND223_CASE_CANDIDATES],
        "what_not_to_change": [
            "do_not_use_round223_cases_as_candidate_generation_input",
            "do_not_apply_shadow_weights_to_production_scoring_yet",
            "do_not_lower_stage3_green_thresholds",
            "do_not_treat_low_pbr_valueup_stablecoin_digital_asset_or_ipo_theme_as_green",
            "do_not_invent_ohlc_stage_prices_or_business_metrics",
        ],
    }


def render_round223_summary_markdown() -> str:
    summary = round223_summary()
    lines = [
        "# Round 223 R6 Loop 9 Financial Capital Digital Price Validation",
        "",
        "This pack is calibration-only. Production scoring and candidate generation are unchanged.",
        "",
        "## Summary",
        "",
        f"- source_round: {summary['source_round']}",
        f"- analyst_round_id: {summary['analyst_round_id']}",
        f"- large_sector: {summary['large_sector']}",
        f"- cases: {summary['case_candidate_count']}",
        f"- success_candidate: {summary['success_candidate_count']}",
        f"- cyclical_success: {summary['cyclical_success_count']}",
        f"- event_premium: {summary['event_premium_count']}",
        f"- overheat: {summary['overheat_count']}",
        f"- 4c_thesis_break: {summary['thesis_break_count']}",
        f"- Stage 3 dated cases: {summary['stage3_case_count']}",
        f"- 4B-watch cases: {summary['stage4b_watch_count']}",
        f"- 4C-watch cases: {summary['stage4c_watch_count']}",
        f"- full_ohlc_complete: {str(summary['full_ohlc_complete']).lower()}",
        "",
        "## Case Matrix",
        "",
        "| case | company | type | stage2 | stage3 | 4B | 4C-watch | alignment | note |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for case in ROUND223_CASE_CANDIDATES:
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
            "- KB, SK Square, Samsung Life, Hana, and K Bank are Stage 2 candidates until capital execution and price-path proof improve.",
            "- Securities basket strength is cyclical_success; company-level brokerage, IB revenue, ROE, and risk controls must confirm.",
            "- NAVER/Dunamu is event-premium Stage 2 with exchange-trust 4C-watch.",
            "- Stablecoin policy basket rallies are price_moved_without_evidence until licensing, reserve income, fee revenue, and capital rules exist.",
            "- Kakao/KakaoBank shows major-shareholder legal risk can block Green before internet-bank growth scoring matters.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round223_green_gate_review_markdown() -> str:
    lines = ["# Round 223 R6 Green Gate Review", "", "Do not apply these weights to production scoring yet.", "", "## Required Fields", ""]
    lines.extend(f"- {field}" for field in ROUND223_GREEN_REQUIRED_FIELDS)
    lines.extend(["", "## Forbidden Patterns", ""])
    lines.extend(f"- {field}" for field in ROUND223_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(["", "## Shadow Score Adjustments", "", "| axis | direction | points | reason |", "|---|---|---:|---|"])
    for adjustment in ROUND223_SCORE_ADJUSTMENTS:
        lines.append(f"| {adjustment.axis} | {adjustment.direction} | {adjustment.points} | {adjustment.reason} |")
    lines.extend(
        [
            "",
            "## Easy Examples",
            "- `저PBR + 밸류업`은 Stage 1/2 관심이다. ROE, CET1, 반복 소각, credit cost 통과 전 Green이 아니다.",
            "- `증권주 +13.5%`는 거래대금 사이클 4B-watch다. 개별 증권사 ROE/IB 수익 확인 전 Green이 아니다.",
            "- `스테이블코인 관련주 2~3배`는 수익모델 전 가격 선반영이다. 발행권, reserve income, fee revenue 없으면 event premium이다.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round223_stage4b_4c_review_markdown() -> str:
    lines = ["# Round 223 R6 4B / 4C Review", "", "## 4B Watch Triggers", ""]
    lines.extend(f"- {field}" for field in ROUND223_STAGE4B_WATCH_TRIGGERS)
    lines.extend(["", "## Hard 4C Gates", ""])
    lines.extend(f"- {field}" for field in ROUND223_HARD_4C_GATES)
    lines.extend(["", "## Case Review", "", "| case | 4B status | hard 4C | interpretation |", "|---|---|---|---|"])
    for case in ROUND223_CASE_CANDIDATES:
        lines.append(f"| {case.case_id} | {case.stage4b_status} | {str(case.hard_4c_confirmed).lower()} | {case.notes} |")
    return "\n".join(lines) + "\n"


def render_round223_price_validation_plan_markdown() -> str:
    lines = [
        "# Round 223 R6 Price Validation Plan",
        "",
        "- price_validation_completed: partial_with_reported_price_anchors",
        "- full_ohlc_complete: false",
        "- Do not invent OHLC, peak, MFE, MAE, stage prices, or business metrics where source anchors are unavailable.",
        "",
        "## Backfill Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND223_PRICE_VALIDATION_FIELDS)
    lines.extend(["", "## Case Anchors", "", "| case | data source | reported anchor | status |", "|---|---|---|---|"])
    for case in ROUND223_CASE_CANDIDATES:
        lines.append(f"| {case.case_id} | {case.price_data_source} | {case.reported_return_anchor} | {case.price_validation_status} |")
    return "\n".join(lines) + "\n"


def write_round223_r6_loop9_reports(
    output_directory: str | Path = ROUND223_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND223_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND223_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "cases": write_case_library(round223_case_records(), cases_path),
        "audit": _write_json(round223_audit_payload(), audit_path),
        "summary": output / "round223_r6_loop9_price_validation_summary.md",
        "case_matrix": output / "round223_r6_loop9_case_matrix.csv",
        "target_aliases": output / "round223_r6_loop9_target_aliases.csv",
        "score_adjustments": output / "round223_r6_loop9_score_adjustments.csv",
        "shadow_weights": output / "round223_r6_loop9_shadow_weights.csv",
        "price_validation_fields": output / "round223_r6_loop9_price_validation_fields.csv",
        "green_gate_review": output / "round223_r6_loop9_green_gate_review.md",
        "price_validation_plan": output / "round223_r6_loop9_price_validation_plan.md",
        "stage4b_4c_review": output / "round223_r6_loop9_stage4b_4c_review.md",
    }
    paths["summary"].write_text(render_round223_summary_markdown(), encoding="utf-8")
    _write_csv(round223_case_rows(), paths["case_matrix"])
    _write_csv(round223_target_alias_rows(), paths["target_aliases"])
    _write_csv(round223_score_adjustment_rows(), paths["score_adjustments"])
    _write_csv(round223_shadow_weight_rows(), paths["shadow_weights"])
    _write_csv(round223_price_validation_field_rows(), paths["price_validation_fields"])
    paths["green_gate_review"].write_text(render_round223_green_gate_review_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round223_price_validation_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round223_stage4b_4c_review_markdown(), encoding="utf-8")
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
