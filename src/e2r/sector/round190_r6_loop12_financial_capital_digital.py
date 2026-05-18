"""Round-190 R6 Loop-12 Korea financial/capital/digital pack.

Round 190 tightens R6 around financial value-up execution, insurance NAV,
digital-asset equity options, biometric payments, stablecoin policy themes,
credit-information recurring data, brokerage beta, and policy/privacy hard
gates. It is calibration/report material only. Production feature
engineering, scoring, staging, and RedTeam code must not import this module.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import CaseDataQuality, E2RCaseRecord, PriceValidation
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture


ROUND190_SOURCE_ROUND_PATH = "docs/round/round_190.md"
ROUND190_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round190_r6_loop12_financial_capital_digital"
ROUND190_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r6_loop12_round190.jsonl"
ROUND190_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round190_r6_loop12_v12.csv"
ROUND190_SOURCE_CANONICAL_TARGET_IDS: tuple[str, ...] = (
    "INSURANCE_NAV_VALUEUP_SAMSUNG_ELECTRONICS_STAKE",
    "SHAREHOLDER_RETURN_COMPOUNDING_FINANCIAL_HOLDCO",
    "DIGITAL_ASSET_BANK_EQUITY_OPTION",
    "KRW_STABLECOIN_POLICY_THEME",
    "PAYMENT_BIOMETRIC_INFRASTRUCTURE",
    "PAYMENT_PRIVACY_REGULATORY_4C",
    "CREDIT_INFORMATION_RECURRING_DATA",
    "SECURITIES_BROKERAGE_MARKET_BETA",
    "BUYBACK_EXECUTION_PRICE_FAILED",
    "POLICY_TAX_REVERSAL_MARKET_SHOCK",
    "DISCLOSURE_CONFIDENCE_CAP",
)
ROUND190_SOURCE_CANONICAL_TARGET_COUNT = len(ROUND190_SOURCE_CANONICAL_TARGET_IDS)


@dataclass(frozen=True)
class Round190ScoreWeightDraft:
    roe_eps_fcf_durability: int | str
    capital_return_execution: int | str
    capital_ratio_credit_cost_stability: int | str
    digital_finance_revenue_model_visibility: int | str
    early_price_validation: int | str
    security_privacy_policy_redteam: int | str
    valuation_4b_room: int | str

    def as_dict(self) -> dict[str, int | str]:
        return {
            "roe_eps_fcf_durability": self.roe_eps_fcf_durability,
            "capital_return_execution": self.capital_return_execution,
            "capital_ratio_credit_cost_stability": self.capital_ratio_credit_cost_stability,
            "digital_finance_revenue_model_visibility": self.digital_finance_revenue_model_visibility,
            "early_price_validation": self.early_price_validation,
            "security_privacy_policy_redteam": self.security_privacy_policy_redteam,
            "valuation_4b_room": self.valuation_4b_room,
        }


@dataclass(frozen=True)
class Round190ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round190ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    loop12_penalty_axes: tuple[str, ...]
    normalization_point: str
    hard_gate: bool = False

    @property
    def large_sector(self) -> Round10LargeSector:
        return Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round190CaseCandidate:
    case_id: str
    target_id: str
    symbol: str
    company_name: str
    market: str
    case_type: str
    evidence_fields: tuple[str, ...]
    red_flag_fields: tuple[str, ...]
    alignment_hint: str
    price_validation_status: str
    source_refs: tuple[str, ...]
    notes: str
    secondary_archetypes: tuple[E2RArchetype, ...] = ()

    @property
    def expected_group(self) -> str:
        return self.case_type


@dataclass(frozen=True)
class Round190BaseScoreWeight:
    component: str
    points: int
    loop12_direction: str
    reason: str

    def as_row(self) -> dict[str, str]:
        return {
            "component": self.component,
            "points": str(self.points),
            "loop12_direction": self.loop12_direction,
            "reason": self.reason,
            "production_scoring_changed": "false",
        }


@dataclass(frozen=True)
class Round190StageCap:
    stage_band: str
    max_score: str
    required_evidence: tuple[str, ...]
    example_cases: tuple[str, ...]
    green_policy: str

    def as_row(self) -> dict[str, str]:
        return {
            "stage_band": self.stage_band,
            "max_score": self.max_score,
            "required_evidence": "|".join(self.required_evidence),
            "example_cases": "|".join(self.example_cases),
            "green_policy": self.green_policy,
            "production_scoring_changed": "false",
        }


@dataclass(frozen=True)
class Round190ScoreStagePriceAlignment:
    case_id: str
    detected_stage: str
    price_path_status: str
    verdict: str
    normalization_adjustment: str

    def as_row(self) -> dict[str, str]:
        return {
            "case_id": self.case_id,
            "detected_stage": self.detected_stage,
            "price_path_status": self.price_path_status,
            "verdict": self.verdict,
            "normalization_adjustment": self.normalization_adjustment,
            "production_scoring_changed": "false",
        }


def _w(
    roe: int | str,
    return_execution: int | str,
    capital: int | str,
    digital: int | str,
    price: int | str,
    redteam: int | str,
    valuation: int | str,
) -> Round190ScoreWeightDraft:
    return Round190ScoreWeightDraft(roe, return_execution, capital, digital, price, redteam, valuation)


CAP_WEIGHT = _w("cap", "cap", "cap", "cap", "cap", "cap", "+")
GATE_WEIGHT = _w("gate", "gate", "gate", "gate", "gate", "gate", "gate")


ROUND190_BASE_SCORE_WEIGHTS: tuple[Round190BaseScoreWeight, ...] = (
    Round190BaseScoreWeight("roe_eps_fcf_durability", 22, "keep_high", "R6 Loop 12 requires durable ROE, profit, EPS, or FCF, not low-PBR or fintech keywords alone."),
    Round190BaseScoreWeight("capital_return_execution", 18, "raised_for_loop12", "Actual buyback cancellation, dividend expansion, or recurring total-shareholder-return policy is execution evidence."),
    Round190BaseScoreWeight("capital_ratio_credit_cost_stability", 16, "hard_quality_gate", "CET1, K-ICS, CSM, PF exposure, reserve build, and credit cost separate value-up from capital pressure."),
    Round190BaseScoreWeight("digital_finance_revenue_model_visibility", 16, "raised_for_loop12", "Dunamu stake, stablecoin, FacePay, or credit-data optionality needs equity-method income, issuance, take-rate, or recurring data revenue."),
    Round190BaseScoreWeight("early_price_validation", 10, "required_backfill", "Stage 2 이후 60D/120D MFE and relative strength validate whether capital return or digital-finance evidence is being confirmed."),
    Round190BaseScoreWeight("security_privacy_policy_redteam", 12, "hard_review", "Exchange security, privacy consent, biometric data, tax reversal, and regulatory uncertainty can block Green."),
    Round190BaseScoreWeight("valuation_4b_room", 6, "cool_crowded_financial_rallies", "Value-up, Dunamu, stablecoin, and buyback narratives need 4B cooling when price outruns ROE/EPS and execution."),
)


ROUND190_STAGE_CAPS: tuple[Round190StageCap, ...] = (
    Round190StageCap(
        "Stage 1",
        "45",
        ("low_pbr", "valueup_keyword", "dunamu_or_stablecoin_keyword", "facepay_headline", "buyback_headline", "brokerage_beta"),
        ("hana_financial_dunamu_equity_option_stage2_case", "krw_stablecoin_policy_theme_4b_watch_case"),
        "Low-PBR, value-up, stablecoin, Dunamu, FacePay, or buyback words route research only. Green is blocked before ROE, capital, execution, revenue model, and price path align.",
    ),
    Round190StageCap(
        "Stage 2",
        "70",
        ("roe_or_net_profit_improves", "capital_ratio_stable", "buyback_or_dividend_execution", "digital_finance_option_identified", "event_return_or_relative_strength"),
        ("samsung_life_insurance_nav_valueup_stage23_case", "meritz_financial_shareholder_return_stage23_case"),
        "Stage 2 can be strong when NAV, capital return, capital ratio, or digital optionality exists, but Stage 3 waits for durable execution and hard-risk clearance.",
    ),
    Round190StageCap(
        "Stage 3",
        "requires_6_of_9",
        (
            "roe_or_net_profit_improves_yoy",
            "cet1_kics_or_csm_stable",
            "actual_buyback_cancel_or_dividend_expansion_executed",
            "credit_cost_or_pf_reserve_stable",
            "stage2_60d_mfe_20pct",
            "pbr_band_rises_from_history",
            "repeat_return_policy_or_midterm_tsr_target",
            "digital_take_rate_issuance_or_equity_method_income_confirmed",
            "no_privacy_security_regulatory_hard_issue",
        ),
        ("meritz_financial_shareholder_return_stage23_case", "nice_credit_information_recurring_data_stage23_case"),
        "Stage 3 early catch requires at least 6 of 9 checks. For example, a buyback headline alone is Stage 1; executed cancellation plus ROE/capital stability can be Stage 2~3.",
    ),
    Round190StageCap(
        "Stage 4B",
        "requires_4_of_6",
        (
            "stage2_120d_mfe_60pct",
            "valueup_stablecoin_or_dunamu_keyword_doubles_price_before_earnings",
            "pbr_rerating_ahead_of_roe_eps",
            "actual_cancellation_equity_method_or_take_rate_missing",
            "policy_or_regulatory_framework_unclear",
            "financial_basket_crowded",
        ),
        ("krw_stablecoin_policy_theme_4b_watch_case", "stablecoin_related_stock_price_only_rally_case"),
        "Crowded financial and digital-finance rallies are cooled when price moves before earnings, capital return, issuance, or take-rate evidence.",
    ),
    Round190StageCap(
        "Stage 4C",
        "hard_gate",
        (
            "cet1_or_kics_falls_sharply",
            "pf_credit_cost_spike",
            "buyback_cancelled_or_return_cut",
            "large_capital_raise_or_capital_pressure",
            "exchange_hack_or_abnormal_withdrawal",
            "privacy_or_biometric_data_leak",
            "stablecoin_regulation_damages_issuer_margin",
            "tax_policy_shock_hits_valueup_basket",
            "buyback_price_fail_and_operating_concern_dominates",
        ),
        ("kakaopay_privacy_regulatory_4c_watch_case", "policy_tax_reversal_market_shock_4c_watch_case"),
        "A single capital, credit, security, privacy, policy, or buyback-execution hard issue can block Green.",
    ),
)


def _target(
    target_id: str,
    archetype: E2RArchetype,
    posture: Round10ThemePosture,
    weight: Round190ScoreWeightDraft,
    stage1: tuple[str, ...],
    stage2: tuple[str, ...],
    stage3: tuple[str, ...],
    stage4b: tuple[str, ...],
    stage4c: tuple[str, ...],
    green: tuple[str, ...],
    red: tuple[str, ...],
    penalties: tuple[str, ...],
    note: str,
    *,
    hard_gate: bool = False,
) -> Round190ScoreTarget:
    return Round190ScoreTarget(
        target_id,
        archetype,
        posture,
        weight,
        stage1,
        stage2,
        stage3,
        stage4b,
        stage4c,
        green,
        red,
        penalties,
        note,
        hard_gate,
    )


ROUND190_SCORE_TARGETS: tuple[Round190ScoreTarget, ...] = (
    _target(
        "INSURANCE_NAV_VALUEUP_SAMSUNG_ELECTRONICS_STAKE",
        E2RArchetype.INSURANCE_NAV_VALUEUP_SAMSUNG_ELECTRONICS_STAKE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(18, 14, 22, 0, 10, 18, 18),
        ("samsung_electronics_stake", "insurance_nav_discount", "valueup_tailwind", "book_value_discount"),
        ("major_equity_stake_value", "nav_discount", "k_ics_or_csm_check", "shareholder_return_policy"),
        ("roe_or_net_profit_improves_yoy", "k_ics_csm_stable", "nav_discount_closes_with_return_execution", "pbr_band_rises_from_history"),
        ("samsung_electronics_stake_priced_before_insurance_execution",),
        ("k_ics_deteriorates", "csm_weakens", "return_execution_missing", "samsung_electronics_price_only_linkage"),
        ("k_ics_csm_stable", "return_execution", "roe_profit_improvement", "nav_discount_narrows"),
        ("k_ics_csm_missing", "return_execution_missing", "nav_is_price_only"),
        ("insurance_nav", "capital_ratio", "return_execution"),
        "Insurance NAV optionality is Stage 2 evidence; Stage 3 waits for K-ICS/CSM, ROE/profit, and actual return execution.",
    ),
    _target(
        "SHAREHOLDER_RETURN_COMPOUNDING_FINANCIAL_HOLDCO",
        E2RArchetype.SHAREHOLDER_RETURN_COMPOUNDING_FINANCIAL_HOLDCO,
        Round10ThemePosture.GREEN_POSSIBLE,
        _w(24, 24, 18, 0, 10, 10, 14),
        ("financial_holdco_valueup", "buyback_cancel_policy", "roe_improvement", "total_shareholder_return"),
        ("repeat_buyback_cancel", "dividend_expansion", "capital_ratio_stable", "credit_cost_stable"),
        ("roe_compounds", "actual_return_execution_repeats", "eps_accretion_from_buyback", "pbr_band_rerates_with_profit"),
        ("return_story_crowded_before_roe",),
        ("credit_cost_spike", "capital_ratio_pressure", "return_cut", "securities_cycle_loss"),
        ("repeat_buyback_cancel", "roe_profit_improvement", "capital_ratio_stable", "credit_cost_stable"),
        ("credit_cost_unconfirmed", "capital_ratio_unconfirmed", "return_detail_missing"),
        ("capital_return", "roe", "credit_cost"),
        "Meritz-style financial holdco compounding can be Green-eligible only with repeated return execution and capital/credit stability.",
    ),
    _target(
        "DIGITAL_ASSET_BANK_EQUITY_OPTION",
        E2RArchetype.DIGITAL_ASSET_BANK_EQUITY_OPTION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(16, 8, 14, 24, 10, 20, 8),
        ("bank_digital_asset_stake", "dunamu_or_upbit_keyword", "blockchain_remittance", "digital_asset_policy"),
        ("stake_value_disclosed", "equity_method_income_check", "regulatory_approval", "exchange_volume_or_fee_revenue"),
        ("equity_method_income_confirmed", "regulated_revenue_model", "capital_ratio_stable", "security_trust_intact"),
        ("dunamu_keyword_doubles_price_before_income",),
        ("exchange_security_incident", "regulatory_sanction", "equity_method_income_missing", "crypto_volume_reversal"),
        ("equity_method_income", "regulated_revenue_model", "security_trust_intact"),
        ("regulatory_approval_pending", "exchange_security_risk", "equity_method_income_missing"),
        ("digital_asset_stake", "equity_method_income", "security"),
        "A bank's digital-asset stake is Stage 2 optionality before equity-method income, regulation, and security evidence are verified.",
    ),
    _target(
        "KRW_STABLECOIN_POLICY_THEME",
        E2RArchetype.KRW_STABLECOIN_POLICY_THEME,
        Round10ThemePosture.REDTEAM_FIRST,
        _w(8, 4, 10, 24, 12, 30, 12),
        ("won_stablecoin_policy", "stablecoin_related_stock_rally", "bok_pilot", "issuer_keyword"),
        ("regulatory_framework_draft", "issuer_candidate", "payment_or_reserve_model_check"),
        ("not_green_until_issuance_volume_reserve_income_take_rate_and_regulation_are_verified",),
        ("stablecoin_theme_doubles_price_before_revenue", "policy_framework_unclear", "issuer_economics_missing"),
        ("stablecoin_regulation_damages_margin", "reserve_rule_blocks_income", "issuer_capital_requirement", "price_only_rally"),
        ("stablecoin_issuance_volume", "reserve_income", "take_rate", "regulatory_clarity"),
        ("issuer_economics_missing", "regulatory_framework_unclear", "price_only_rally"),
        ("stablecoin_policy", "issuer_economics", "4b_watch"),
        "Won stablecoin policy can route research, but it is a 4B-watch theme until issuance, reserve income, take-rate, and regulation are real.",
    ),
    _target(
        "PAYMENT_BIOMETRIC_INFRASTRUCTURE",
        E2RArchetype.PAYMENT_BIOMETRIC_INFRASTRUCTURE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(14, 8, 12, 26, 10, 24, 6),
        ("facepay_headline", "biometric_payment", "merchant_count", "user_count"),
        ("approved_service", "user_merchant_scale", "take_rate_check", "listed_stock_link_check"),
        ("take_rate_confirmed", "transaction_volume", "issuer_economics_visible", "privacy_controls_verified"),
        ("facepay_headline_priced_before_revenue",),
        ("biometric_privacy_issue", "take_rate_missing", "issuer_economics_missing", "listed_stock_direct_link_missing"),
        ("take_rate", "transaction_volume", "privacy_control", "listed_stock_revenue_link"),
        ("take_rate_missing", "biometric_privacy_risk", "direct_revenue_link_missing"),
        ("biometric_payment", "take_rate", "privacy"),
        "FacePay scale is Stage 2 infrastructure evidence; Stage 3 waits for take-rate, transaction volume, privacy control, and listed-stock revenue linkage.",
    ),
    _target(
        "PAYMENT_PRIVACY_REGULATORY_4C",
        E2RArchetype.PAYMENT_PRIVACY_REGULATORY_4C,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        ("payment_platform_scale", "cross_border_data_transfer", "privacy_fine", "consent_issue"),
        ("regulatory_response", "governance_fix", "platform_trust_check"),
        ("not_green_until_privacy_issue_is_resolved_and_user_trust_is_intact",),
        ("payment_platform_priced_before_privacy_resolution",),
        ("customer_data_transfer_without_consent", "privacy_fine", "platform_trust_damage", "regulatory_sanction"),
        ("privacy_governance_resolved", "regulator_cleared", "trust_metrics_stable"),
        ("privacy_fine", "consent_issue", "platform_trust_damage"),
        ("privacy", "regulation", "trust"),
        "Payment privacy and consent issues are hard RedTeam gates for digital-finance rerating.",
        hard_gate=True,
    ),
    _target(
        "CREDIT_INFORMATION_RECURRING_DATA",
        E2RArchetype.CREDIT_INFORMATION_RECURRING_DATA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(20, 8, 12, 24, 8, 20, 8),
        ("credit_information_service", "rating_data", "authentication", "financial_customer_base"),
        ("recurring_data_revenue", "subscription_or_usage_fee", "financial_it_budget", "regulatory_data_protection"),
        ("data_subscription_growth", "opm_or_eps_improves", "customer_retention", "security_trust_intact"),
        ("credit_data_story_priced_before_growth",),
        ("data_protection_tightens", "security_incident", "financial_it_budget_cut", "growth_rate_missing"),
        ("recurring_data_revenue", "opm_eps_improvement", "customer_retention", "security_trust_intact"),
        ("security_incident_risk", "growth_rate_missing", "regulatory_data_protection"),
        ("credit_data", "recurring_revenue", "security"),
        "Credit-information data can be Stage 2~3 when recurring revenue and OPM/EPS conversion are explicit.",
    ),
    _target(
        "SECURITIES_BROKERAGE_MARKET_BETA",
        E2RArchetype.SECURITIES_BROKERAGE_MARKET_BETA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(18, 8, 12, 8, 12, 30, 12),
        ("kospi_rally", "trading_value_spike", "brokerage_fee_growth", "brokerage_beta"),
        ("trading_value_sustained", "ib_pipeline_check", "pf_loss_check", "capital_ratio_check"),
        ("not_green_until_brokerage_fee_ib_pipeline_credit_cost_and_capital_are_visible",),
        ("market_beta_priced_before_earnings", "financial_basket_crowded"),
        ("trading_value_reverses", "pf_ib_loss", "tax_policy_shock", "market_drawdown"),
        ("sustained_fee_income", "ib_pipeline_quality", "capital_ratio_stable"),
        ("market_beta_only", "trading_value_cycle", "pf_ib_loss_risk", "tax_policy_risk"),
        ("brokerage_beta", "cyclical_cap"),
        "Brokerage rallies can be cyclical successes, but market beta alone should not become structural Green.",
    ),
    _target(
        "BUYBACK_EXECUTION_PRICE_FAILED",
        E2RArchetype.BUYBACK_EXECUTION_PRICE_FAILED,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        ("buyback_cancel_headline", "treasury_share_cancel", "shareholder_return_policy"),
        ("buyback_amount", "cancelled_share_amount", "eps_accretion_check", "same_day_price_reaction"),
        ("not_green_until_buyback_execution_aligns_with_roe_eps_fcf_and_price_validation",),
        ("buyback_headline_priced_before_operating_improvement",),
        ("same_day_price_drop", "operating_concern_dominates", "eps_roe_not_confirmed", "market_expectation_priced"),
        ("eps_accretion", "roe_profit_improvement", "positive_price_validation"),
        ("price_failed", "operating_concern_dominates", "eps_roe_missing"),
        ("buyback_execution", "price_failure", "operating_context"),
        "Actual cancellation is useful evidence, but price failure and operating concern can cap the rerating.",
        hard_gate=True,
    ),
    _target(
        "POLICY_TAX_REVERSAL_MARKET_SHOCK",
        E2RArchetype.POLICY_TAX_REVERSAL_MARKET_SHOCK,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        ("valueup_policy", "tax_policy_change", "financial_basket_rally", "kospi_market_shock"),
        ("tax_reversal_detected", "basket_drawdown", "policy_risk_repriced"),
        ("not_green_until_policy_risk_clears_and_company_specific_roe_return_execution_remains_intact",),
        ("valueup_basket_crowded_before_policy_detail",),
        ("capital_gains_tax_threshold_lowered", "dividend_tax_hike", "transaction_tax_hike", "kospi_market_shock"),
        ("policy_risk_cleared", "company_specific_execution_intact"),
        ("tax_policy_shock", "valueup_basket_crowding", "policy_reversal"),
        ("policy_tax", "market_shock", "valueup"),
        "Policy tax reversal can break financial value-up baskets even when company-level narratives look intact.",
        hard_gate=True,
    ),
    _target(
        "DISCLOSURE_CONFIDENCE_CAP",
        E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        Round10ThemePosture.REDTEAM_FIRST,
        CAP_WEIGHT,
        ("opendart_list_only", "media_report_only", "buyback_or_dividend_headline", "stablecoin_or_dunamu_headline"),
        ("detail_fetch_required", "capital_return_detail_required", "capital_ratio_required", "revenue_model_required"),
        ("not_green_until_capital_return_capital_ratio_digital_revenue_security_and_price_fields_are_verified",),
        ("headline_priced_before_detail",),
        ("return_detail_missing", "capital_ratio_unknown", "digital_finance_revenue_missing", "security_detail_missing"),
        ("capital_return_detail", "capital_ratio", "digital_revenue_model", "security_resolution"),
        ("opendart_list_only", "media_report_only", "detail_missing", "security_detail_missing"),
        ("detail_missing", "capital_ratio", "digital_revenue"),
        "Round 190 caps list-only, media-only, buyback-only, stablecoin-only, and missing capital/revenue/security detail before Green.",
    ),
)


ROUND190_CASE_CANDIDATES: tuple[Round190CaseCandidate, ...] = (
    Round190CaseCandidate(
        "samsung_life_insurance_nav_valueup_stage23_case",
        "INSURANCE_NAV_VALUEUP_SAMSUNG_ELECTRONICS_STAKE",
        "032830",
        "삼성생명 insurance NAV value-up",
        "KR",
        "success_candidate",
        ("samsung_electronics_10pct_stake", "book_value_discount_50pct", "insurance_nav_discount", "valueup_tailwind", "hedge_fund_interest"),
        ("k_ics_csm_missing", "return_execution_missing", "samsung_electronics_price_only_linkage", "insurance_roe_missing"),
        "nav_stage2_to_stage3_if_kics_csm_return_and_pbr_band_align",
        "needs_nav_kics_csm_return_execution_price_backfill",
        ("round_190.md Samsung Life NAV / Samsung Electronics stake",),
        "Samsung Life is a NAV/value-up Stage 2~3 candidate, but Green waits for K-ICS, CSM, ROE/profit, return execution, and price path.",
    ),
    Round190CaseCandidate(
        "meritz_financial_shareholder_return_stage23_case",
        "SHAREHOLDER_RETURN_COMPOUNDING_FINANCIAL_HOLDCO",
        "138040",
        "메리츠금융지주 shareholder return compounding",
        "KR",
        "success_candidate",
        ("meritz_fire_securities_holdco", "shareholder_return_candidate", "buyback_cancel_detail_required", "roe_improvement_candidate"),
        ("dart_detail_missing", "credit_cost_unconfirmed", "securities_cycle_exposure", "capital_ratio_unconfirmed"),
        "stage2_to_stage3_if_repeat_return_roe_capital_and_credit_cost_align",
        "needs_buyback_cancel_dividend_roe_capital_credit_price_backfill",
        ("round_190.md Meritz return compounding",),
        "Meritz-style return compounding is Green-eligible only after repeated return execution, ROE, capital ratio, credit cost, and price path are confirmed.",
        (E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN,),
    ),
    Round190CaseCandidate(
        "hana_financial_dunamu_equity_option_stage2_case",
        "DIGITAL_ASSET_BANK_EQUITY_OPTION",
        "086790",
        "하나금융 Dunamu equity option",
        "KR",
        "success_candidate",
        ("dunamu_6_55pct_stake", "deal_value_1_003tn_krw", "fourth_largest_shareholder", "blockchain_remittance_validation"),
        ("regulatory_approval_pending", "exchange_security_risk", "equity_method_income_missing", "crypto_volume_risk"),
        "stage2_option_not_green_before_equity_method_regulation_and_security",
        "needs_equity_method_income_regulation_security_volume_price_backfill",
        ("round_190.md Hana Bank / Dunamu stake",),
        "A Dunamu stake can create Stage 2 optionality, but equity-method income, regulatory approval, security, and fee durability gate Stage 3.",
        (E2RArchetype.BANK_DIGITAL_ASSET_EQUITY_STAKE, E2RArchetype.EXCHANGE_SECURITY_OPERATIONAL_RISK),
    ),
    Round190CaseCandidate(
        "toss_facepay_payment_biometric_stage2_case",
        "PAYMENT_BIOMETRIC_INFRASTRUCTURE",
        "TOSS_RELATED_BASKET",
        "Toss FacePay biometric payment infrastructure",
        "KR",
        "success_candidate",
        ("facepay_4_8m_users", "330k_retail_locations", "10m_user_target", "1m_merchant_target", "government_approval"),
        ("take_rate_missing", "listed_stock_direct_link_missing", "biometric_privacy_risk", "issuer_economics_missing"),
        "stage2_infrastructure_option_until_take_rate_transaction_volume_and_privacy_clear",
        "needs_take_rate_transaction_volume_privacy_direct_link_price_backfill",
        ("round_190.md Toss FacePay",),
        "FacePay has infrastructure scale, but listed-stock linkage and transaction economics must be proven before high-conviction scoring.",
        (E2RArchetype.PAYMENT_PRIVACY_REGULATORY_4C,),
    ),
    Round190CaseCandidate(
        "nice_credit_information_recurring_data_stage23_case",
        "CREDIT_INFORMATION_RECURRING_DATA",
        "034310/030190",
        "NICE credit information recurring data",
        "KR",
        "success_candidate",
        ("credit_information_service", "data_subscription", "authentication_revenue", "financial_customer_base", "recurring_data_revenue_option"),
        ("data_protection_regulation", "security_incident_risk", "financial_it_budget_cut", "growth_rate_missing"),
        "stage2_to_stage3_if_recurring_data_revenue_opm_eps_and_security_align",
        "needs_recurring_data_revenue_opm_eps_security_price_backfill",
        ("round_190.md NICE credit information",),
        "Credit-information recurring data can become Stage 2~3 when recurring revenue, OPM/EPS, retention, and security evidence align.",
    ),
    Round190CaseCandidate(
        "krw_stablecoin_policy_theme_4b_watch_case",
        "KRW_STABLECOIN_POLICY_THEME",
        "KRW_STABLECOIN_BASKET",
        "KRW stablecoin policy theme 4B-watch",
        "KR",
        "4b_watch",
        ("kakaopay_monthly_double", "lg_cns_plus_70pct", "aton_plus_80pct", "me2on_tripled", "won_stablecoin_policy_promise"),
        ("issuer_economics_missing", "regulatory_framework_unclear", "bok_concern", "price_only_rally"),
        "stablecoin_theme_requires_4b_watch_until_issuer_economics_and_regulation_exist",
        "needs_issuance_reserve_income_take_rate_regulation_price_backfill",
        ("round_190.md KRW stablecoin basket",),
        "Stablecoin policy headlines can double related stocks before revenue evidence; that is 4B-watch, not proof of structural Green.",
        (E2RArchetype.DIGITAL_ASSET_THEME_OVERHEAT, E2RArchetype.CROWDED_RERATING_4B_WATCH),
    ),
    Round190CaseCandidate(
        "kakaopay_privacy_regulatory_4c_watch_case",
        "PAYMENT_PRIVACY_REGULATORY_4C",
        "377300",
        "KakaoPay privacy regulatory 4C-watch",
        "KR",
        "4c_thesis_break",
        ("payment_network", "digital_finance_policy_exposure", "privacy_governance_issue"),
        ("alipay_singapore_data_transfer", "fss_15bn_krw_fine", "consent_issue", "platform_trust_damage"),
        "privacy_consent_issue_is_hard_gate_before_payment_platform_rerating",
        "needs_regulatory_resolution_trust_metrics_price_backfill",
        ("round_190.md KakaoPay privacy fine / Alipay transfer",),
        "Privacy and consent problems are hard gates for payment-platform rerating until resolved.",
        (E2RArchetype.PLATFORM_PRIVACY_SECURITY_OVERLAY,),
    ),
    Round190CaseCandidate(
        "samsung_electronics_buyback_execution_price_failed_case",
        "BUYBACK_EXECUTION_PRICE_FAILED",
        "005930",
        "Samsung Electronics buyback execution price-fail",
        "KR",
        "failed_rerating",
        ("14_6tn_krw_treasury_cancel", "buyback_cancel_executed"),
        ("same_day_minus_5_2pct", "operating_concern_dominates", "market_expectation_priced", "eps_roe_not_confirmed"),
        "actual_cancellation_is_not_enough_when_price_and_operating_context_fail",
        "needs_eps_roe_fcf_operating_context_price_backfill",
        ("round_190.md Samsung Electronics buyback cancel price fail",),
        "Buyback cancellation is real evidence, but if operating concern dominates and price fails, rerating should be capped.",
        (E2RArchetype.TREASURY_SHARE_CANCEL_EXECUTION, E2RArchetype.EVIDENCE_GOOD_BUT_PRICE_FAILED),
    ),
    Round190CaseCandidate(
        "policy_tax_reversal_market_shock_4c_watch_case",
        "POLICY_TAX_REVERSAL_MARKET_SHOCK",
        "KR_VALUEUP_BASKET",
        "Korea value-up tax reversal market shock",
        "KR",
        "4c_thesis_break",
        ("governance_reform_expectation", "valueup_basket_rally", "tax_policy_change"),
        ("capital_gains_tax_threshold_lowered", "corporate_dividend_tax_hike", "securities_transaction_tax_hike", "kospi_minus_3_9pct"),
        "policy_tax_shock_can_break_valueup_basket_before_company_specific_execution",
        "needs_policy_resolution_company_specific_execution_price_backfill",
        ("round_190.md Korea tax policy shock / value-up basket",),
        "A policy tax shock can invalidate value-up basket momentum even when company-level narratives remain popular.",
        (E2RArchetype.TAX_POLICY_MARKET_SHOCK_OVERLAY,),
    ),
    Round190CaseCandidate(
        "securities_brokerage_market_beta_cycle_case",
        "SECURITIES_BROKERAGE_MARKET_BETA",
        "003540/006800/039490/005940",
        "Korea securities brokerage market beta cycle",
        "KR",
        "cyclical_success",
        ("kospi_7000_rally", "broader_financial_shares_rally", "trading_value_beta", "brokerage_fee_growth_option"),
        ("market_beta_only", "trading_value_cycle", "pf_ib_loss_risk", "tax_policy_risk"),
        "cyclical_success_not_structural_green_without_fee_ib_capital_and_credit_quality",
        "needs_trading_value_fee_ib_capital_credit_price_backfill",
        ("round_190.md securities brokerage market beta",),
        "Brokerage can work cyclically when trading value rises, but structural Green needs fee durability, IB quality, capital, and credit evidence.",
        (E2RArchetype.SECURITIES_IB_PF_RISK_OVERLAY,),
    ),
    Round190CaseCandidate(
        "stablecoin_related_stock_price_only_rally_case",
        "KRW_STABLECOIN_POLICY_THEME",
        "KRW_STABLECOIN_BASKET",
        "Stablecoin related stock price-only rally",
        "KR",
        "4b_watch",
        ("stablecoin_related_stock_double", "policy_keyword", "payment_or_it_theme"),
        ("direct_revenue_model_missing", "issued_volume_missing", "reserve_economics_missing", "policy_framework_unclear"),
        "price_only_stablecoin_rally_is_4b_watch_before_revenue_model",
        "needs_direct_revenue_issuance_reserve_take_rate_price_backfill",
        ("round_190.md stablecoin price-only rally",),
        "A stablecoin price-only rally should cool into 4B-watch until actual issuance and issuer economics are visible.",
        (E2RArchetype.DIGITAL_ASSET_THEME_OVERHEAT, E2RArchetype.CROWDED_RERATING_4B_WATCH),
    ),
    Round190CaseCandidate(
        "digital_asset_exchange_security_incident_4c_reference_case",
        "DIGITAL_ASSET_BANK_EQUITY_OPTION",
        "DIGITAL_ASSET_SECURITY_REF",
        "Digital asset exchange security incident reference",
        "KR",
        "4c_thesis_break",
        ("digital_asset_exchange_equity_option", "exchange_fee_revenue_option"),
        ("exchange_hack_or_abnormal_withdrawal", "customer_compensation", "regulatory_sanction", "security_trust_break"),
        "exchange_security_incident_is_hard_gate_for_bank_equity_option",
        "needs_security_resolution_customer_compensation_regulatory_price_backfill",
        ("round_190.md digital asset security hard gate",),
        "Exchange security or abnormal withdrawal incidents can turn a digital-asset equity option into hard 4C.",
        (E2RArchetype.EXCHANGE_SECURITY_OPERATIONAL_RISK, E2RArchetype.THESIS_BREAK_4C),
    ),
    Round190CaseCandidate(
        "r6_loop12_disclosure_confidence_reference_case",
        "DISCLOSURE_CONFIDENCE_CAP",
        "R6_DISCLOSURE_CAP",
        "R6 Loop 12 financial / digital detail confidence reference",
        "KR",
        "failed_rerating",
        ("watch_disclosure_detail_required", "buyback_cancel_detail_required", "dividend_policy_detail_required", "capital_ratio_required", "stake_value_required", "security_resolution_required"),
        ("opendart_list_only", "media_report_only", "return_detail_missing", "capital_ratio_unknown", "digital_finance_revenue_missing", "security_detail_missing"),
        "list_media_financial_keyword_only_cannot_create_green",
        "needs_opendart_detail_return_capital_revenue_security_price_backfill",
        ("round_190.md disclosure confidence rule",),
        "R6 Loop 12 requires detail fetch and forbids invented missing return, capital ratio, digital revenue, security, and stage price fields.",
    ),
)


ROUND190_SCORE_STAGE_PRICE_ALIGNMENT: tuple[Round190ScoreStagePriceAlignment, ...] = (
    Round190ScoreStagePriceAlignment("samsung_life_insurance_nav_valueup_stage23_case", "Stage 2 -> Stage 3 candidate", "NAV discount is visible, but K-ICS, CSM, return execution, ROE, and 60D MFE need backfill", "stage2_to_stage3_if_capital_return_and_pbr_align", "credit NAV; cap before insurance capital and return execution"),
    Round190ScoreStagePriceAlignment("meritz_financial_shareholder_return_stage23_case", "Stage 2 -> Stage 3 candidate", "Return policy is visible, but repeated cancellation, ROE, capital ratio, and credit cost need backfill", "stage2_to_stage3_if_repeat_return_and_capital_align", "credit return execution; require capital/credit stability"),
    Round190ScoreStagePriceAlignment("hana_financial_dunamu_equity_option_stage2_case", "Stage 2", "Dunamu stake value is real optionality, but equity-method income and security/regulation gate Stage 3", "digital_asset_stake_stage2_not_green", "credit stake value; cap before income and security proof"),
    Round190ScoreStagePriceAlignment("toss_facepay_payment_biometric_stage2_case", "Stage 2 option", "Users and merchants are visible, but take-rate, transaction volume, listed-stock link, and privacy controls need backfill", "facepay_stage2_until_economics", "credit infrastructure scale; require economics and privacy"),
    Round190ScoreStagePriceAlignment("nice_credit_information_recurring_data_stage23_case", "Stage 2 -> Stage 3 candidate", "Recurring data is plausible, but revenue growth, OPM/EPS, and security need backfill", "stage2_to_stage3_if_recurring_revenue_aligns", "credit recurring data; require growth and trust"),
    Round190ScoreStagePriceAlignment("krw_stablecoin_policy_theme_4b_watch_case", "Stage 2 -> 4B-watch", "Theme stocks moved before issuance, reserve income, or take-rate proof", "stablecoin_theme_requires_4b_watch", "cool price-only stablecoin rallies"),
    Round190ScoreStagePriceAlignment("kakaopay_privacy_regulatory_4c_watch_case", "4C-watch", "Privacy fine and consent issues can break payment-platform trust", "privacy_regulatory_hard_gate", "block Green until regulator and trust issues clear"),
    Round190ScoreStagePriceAlignment("samsung_electronics_buyback_execution_price_failed_case", "Failed rerating", "Buyback cancellation happened, but same-day price failure shows operating concern dominated", "buyback_execution_price_failed", "cap buyback signal until EPS/ROE/FCF and price path confirm"),
    Round190ScoreStagePriceAlignment("policy_tax_reversal_market_shock_4c_watch_case", "4C-watch", "Tax reversal can shock the value-up basket", "policy_tax_hard_gate", "block basket Green until policy and company execution are clear"),
    Round190ScoreStagePriceAlignment("securities_brokerage_market_beta_cycle_case", "Cyclical Stage 2", "Brokerage beta can work with trading value, but it is cyclical without fee/IB/capital quality", "market_beta_cycle_not_structural_green", "cap brokerage beta before durable earnings proof"),
    Round190ScoreStagePriceAlignment("stablecoin_related_stock_price_only_rally_case", "4B-watch", "price-only move on stablecoin policy before direct revenue model", "price_only_theme_4b_watch", "cool until issuance/reserve/take-rate fields exist"),
    Round190ScoreStagePriceAlignment("digital_asset_exchange_security_incident_4c_reference_case", "4C-watch", "Exchange security incidents can invalidate digital-asset equity optionality", "security_incident_hard_gate", "block until customer and regulator resolution"),
    Round190ScoreStagePriceAlignment("r6_loop12_disclosure_confidence_reference_case", "Confidence cap", "List/media financial keywords lack return, capital, revenue, security, and price detail", "detail_confidence_cap", "require verified financial and digital-finance details"),
)


ROUND190_PRICE_FIELDS: tuple[str, ...] = (
    "ticker",
    "company_name",
    "canonical_archetype",
    "case_type",
    "stage1_date",
    "stage2_date",
    "stage3_date",
    "stage4b_date",
    "stage4c_date",
    "stage1_trigger",
    "stage2_trigger",
    "stage3_trigger",
    "stage4b_trigger",
    "stage4c_trigger",
    "price_at_stage1",
    "price_at_stage2",
    "price_at_stage3",
    "price_at_stage4b",
    "price_at_stage4c",
    "return_1d_after_event",
    "return_5d_after_event",
    "return_20d_after_stage2",
    "return_60d_after_stage2",
    "return_120d_after_stage2",
    "return_252d_after_stage2",
    "mfe_20d_after_stage2",
    "mae_20d_after_stage2",
    "mfe_60d_after_stage2",
    "mae_60d_after_stage2",
    "mfe_120d_after_stage2",
    "mae_120d_after_stage2",
    "mfe_252d_after_stage2",
    "mae_252d_after_stage2",
    "relative_strength_vs_kospi",
    "relative_strength_vs_financial_basket",
    "relative_strength_vs_bank_basket",
    "relative_strength_vs_insurance_basket",
    "relative_strength_vs_fintech_basket",
    "roe",
    "roe_change_yoy",
    "net_profit",
    "net_profit_growth_yoy",
    "cet1_ratio",
    "k_ics_ratio",
    "csm",
    "credit_cost",
    "pf_exposure",
    "reserve_build",
    "dividend_per_share",
    "dividend_payout_ratio",
    "buyback_amount",
    "cancelled_share_amount",
    "total_shareholder_return_ratio",
    "eps_accretion_from_buyback",
    "pbr_at_stage2",
    "pbr_at_stage3",
    "pbr_at_stage4b",
    "pbr_band_percentile",
    "nav_discount",
    "major_equity_stake_value",
    "digital_asset_stake_value",
    "equity_method_income",
    "stablecoin_regulatory_status",
    "stablecoin_issuance_volume",
    "reserve_income",
    "take_rate",
    "merchant_count",
    "user_count",
    "transaction_volume",
    "privacy_fine_flag",
    "biometric_data_risk_flag",
    "exchange_security_incident_flag",
    "regulatory_approval_pending",
    "tax_policy_shock_flag",
    "disclosure_confidence",
    "valuation_at_stage3",
    "valuation_at_stage4b",
)


def round190_target_for(target_id: str) -> Round190ScoreTarget | None:
    for target in ROUND190_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round190_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND190_CASE_CANDIDATES:
        target = round190_target_for(candidate.target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {candidate.target_id}")
        weights = target.score_weight.as_dict()
        stage4b_evidence = candidate.evidence_fields if candidate.case_type == "4b_watch" else ()
        stage4c_evidence = candidate.red_flag_fields if candidate.case_type == "4c_thesis_break" or target.hard_gate else ()
        record = E2RCaseRecord(
            case_id=candidate.case_id,
            symbol=candidate.symbol,
            company_name=candidate.company_name,
            market=candidate.market,
            sector_raw=candidate.target_id,
            primary_archetype=target.canonical_archetype,
            secondary_archetypes=candidate.secondary_archetypes,
            expected_group=candidate.expected_group,
            large_sector=target.large_sector.value,
            case_type=candidate.case_type,
            evidence_summary=(
                f"Round190 R6 Loop-12 Korea financial/capital/digital case for {candidate.target_id}; "
                "calibration-only and focused on ROE/EPS/FCF durability, capital return execution, capital ratio, credit cost, digital-finance revenue model, security/privacy/policy RedTeam, and price path."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage2_signals or field in target.green_conditions),
            stage3_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage3_conditions or field in target.green_conditions),
            stage4b_evidence=stage4b_evidence,
            stage4c_evidence=stage4c_evidence,
            must_have_fields=target.green_conditions,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason=(
                "; ".join(candidate.red_flag_fields)
                if candidate.case_type in {"failed_rerating", "event_premium", "overheat", "4b_watch", "4c_thesis_break", "one_off", "cyclical_success"}
                else None
            ),
            score_price_alignment=_round190_score_price_alignment(candidate),
            rerating_result=_round190_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
            score_weight_hint={
                "roe_eps_fcf_durability": _numeric_weight(weights["roe_eps_fcf_durability"]),
                "capital_return_execution": _numeric_weight(weights["capital_return_execution"]),
                "capital_ratio_credit_cost_stability": _numeric_weight(weights["capital_ratio_credit_cost_stability"]),
                "digital_finance_revenue_model_visibility": _numeric_weight(weights["digital_finance_revenue_model_visibility"]),
                "early_price_validation": _numeric_weight(weights["early_price_validation"]),
                "security_privacy_policy_redteam": _numeric_weight(weights["security_privacy_policy_redteam"]),
                "valuation_4b_room": _numeric_weight(weights["valuation_4b_room"]),
            },
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "stage3_early_catch_requires_6_of_9_loop12_conditions",
                "stage4b_cooling_requires_4_of_6_loop12_conditions",
                "low_pbr_valueup_stablecoin_dunamu_facepay_or_buyback_headline_is_not_structural_evidence",
                "require_roe_capital_ratio_actual_return_revenue_model_security_and_price_path_for_green",
                "privacy_security_policy_credit_and_capital_ratio_hard_issues_can_block_green",
                "do_not_invent_roe_capital_ratio_buyback_take_rate_stablecoin_issuance_prices_or_stage_dates",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=bool(candidate.source_refs),
                price_data_available=False,
                stage_dates_confidence=0.2,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round190_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND190_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "roe_eps_fcf_durability": str(weights["roe_eps_fcf_durability"]),
                "capital_return_execution": str(weights["capital_return_execution"]),
                "capital_ratio_credit_cost_stability": str(weights["capital_ratio_credit_cost_stability"]),
                "digital_finance_revenue_model_visibility": str(weights["digital_finance_revenue_model_visibility"]),
                "early_price_validation": str(weights["early_price_validation"]),
                "security_privacy_policy_redteam": str(weights["security_privacy_policy_redteam"]),
                "valuation_4b_room": str(weights["valuation_4b_room"]),
                "stage1_signals": "|".join(target.stage1_signals),
                "stage2_signals": "|".join(target.stage2_signals),
                "stage3_conditions": "|".join(target.stage3_conditions),
                "stage4b_conditions": "|".join(target.stage4b_conditions),
                "stage4c_conditions": "|".join(target.stage4c_conditions),
                "green_conditions": "|".join(target.green_conditions),
                "red_flags": "|".join(target.red_flags),
                "loop12_penalty_axes": "|".join(target.loop12_penalty_axes),
                "hard_gate": str(target.hard_gate).lower(),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round190_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND190_CASE_CANDIDATES:
        target = round190_target_for(candidate.target_id)
        assert target is not None
        rows.append(
            {
                "case_id": candidate.case_id,
                "target_id": candidate.target_id,
                "symbol": candidate.symbol,
                "company_name": candidate.company_name,
                "market": candidate.market,
                "case_type": candidate.case_type,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "evidence_fields": "|".join(candidate.evidence_fields),
                "red_flag_fields": "|".join(candidate.red_flag_fields),
                "alignment_hint": candidate.alignment_hint,
                "price_validation_status": candidate.price_validation_status,
                "production_input": "false",
                "notes": candidate.notes,
            }
        )
    return tuple(rows)


def round190_stage_date_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "target_id": target.target_id,
            "stage1": "|".join(target.stage1_signals),
            "stage2": "|".join(target.stage2_signals),
            "stage3": "|".join(target.stage3_conditions),
            "stage4b": "|".join(target.stage4b_conditions),
            "stage4c": "|".join(target.stage4c_conditions),
            "red_flags": "|".join(target.red_flags),
            "hard_gate": str(target.hard_gate).lower(),
            "production_scoring_changed": "false",
        }
        for target in ROUND190_SCORE_TARGETS
    )


def round190_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round190_backfill": "true"} for field in ROUND190_PRICE_FIELDS)


def round190_base_score_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND190_BASE_SCORE_WEIGHTS)


def round190_stage_cap_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND190_STAGE_CAPS)


def round190_score_stage_price_alignment_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND190_SCORE_STAGE_PRICE_ALIGNMENT)


def round190_summary() -> dict[str, int | bool]:
    records = round190_case_records()
    return {
        "target_count": len(ROUND190_SCORE_TARGETS),
        "source_canonical_target_count": ROUND190_SOURCE_CANONICAL_TARGET_COUNT,
        "case_candidate_count": len(records),
        "base_score_axis_count": len(ROUND190_BASE_SCORE_WEIGHTS),
        "stage_cap_count": len(ROUND190_STAGE_CAPS),
        "score_stage_price_alignment_count": len(ROUND190_SCORE_STAGE_PRICE_ALIGNMENT),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for record in records if record.case_type == "cyclical_success"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "hard_gate_target_count": sum(1 for target in ROUND190_SCORE_TARGETS if target.hard_gate),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round190_r6_loop12_reports(
    *,
    output_directory: str | Path = ROUND190_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND190_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND190_DEFAULT_SCORE_PROFILE_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    cases = Path(cases_path)
    score_profiles = Path(score_profile_path)
    cases.parent.mkdir(parents=True, exist_ok=True)
    score_profiles.parent.mkdir(parents=True, exist_ok=True)
    paths = {
        "cases": cases,
        "score_profiles": score_profiles,
        "summary": output / "round190_r6_loop12_financial_capital_digital_summary.md",
        "case_matrix": output / "round190_r6_loop12_case_matrix.csv",
        "stage_date_plan": output / "round190_r6_loop12_stage_date_plan.csv",
        "green_guardrails": output / "round190_r6_loop12_green_guardrails.md",
        "risk_overlays": output / "round190_r6_loop12_risk_overlays.md",
        "price_validation_plan": output / "round190_r6_loop12_price_validation_plan.md",
        "price_fields": output / "round190_r6_loop12_price_fields.csv",
        "base_score_weights": output / "round190_r6_loop12_base_score_weights.csv",
        "stage_caps": output / "round190_r6_loop12_stage_caps.csv",
        "score_stage_price_alignment": output / "round190_r6_loop12_score_stage_price_alignment.csv",
        "score_stage_price_alignment_md": output / "round190_r6_loop12_score_stage_price_alignment.md",
    }
    _write_case_jsonl(round190_case_records(), cases)
    _write_rows(round190_score_profile_rows(), score_profiles)
    _write_rows(round190_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round190_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round190_price_field_rows(), paths["price_fields"])
    _write_rows(round190_base_score_weight_rows(), paths["base_score_weights"])
    _write_rows(round190_stage_cap_rows(), paths["stage_caps"])
    _write_rows(round190_score_stage_price_alignment_rows(), paths["score_stage_price_alignment"])
    paths["summary"].write_text(render_round190_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round190_green_guardrail_markdown(), encoding="utf-8")
    paths["risk_overlays"].write_text(render_round190_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round190_price_validation_plan_markdown(), encoding="utf-8")
    paths["score_stage_price_alignment_md"].write_text(render_round190_score_stage_price_alignment_markdown(), encoding="utf-8")
    return paths


def render_round190_summary_markdown() -> str:
    summary = round190_summary()
    lines = [
        "# Round-190 R6 Loop-12 Financial / Capital / Digital Summary",
        "",
        f"- source_round: `{ROUND190_SOURCE_ROUND_PATH}`",
        f"- large_sector: `{Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL.value}`",
        "- loop: `R6 Loop 12 / v12.0`",
        f"- target_count: {summary['target_count']}",
        f"- source_canonical_target_count: {summary['source_canonical_target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- base_score_axis_count: {summary['base_score_axis_count']}",
        f"- stage_cap_count: {summary['stage_cap_count']}",
        f"- score_stage_price_alignment_count: {summary['score_stage_price_alignment_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- cyclical_success_count: {summary['cyclical_success_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- failed_rerating_count: {summary['failed_rerating_count']}",
        f"- stage4b_case_count: {summary['stage4b_case_count']}",
        f"- stage4c_case_count: {summary['stage4c_case_count']}",
        f"- hard_gate_target_count: {summary['hard_gate_target_count']}",
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "",
        "- R6 Loop 12 separates financial rerating from low-PBR, stablecoin, Dunamu, FacePay, buyback, and brokerage-beta headlines.",
        "- Example: Samsung Life NAV is Stage 2 evidence, but K-ICS, CSM, ROE/profit, return execution, and price path gate Stage 3.",
        "- Example: Meritz-style return compounding can be Green-eligible only with repeated execution plus capital and credit stability.",
        "- Example: KRW stablecoin theme rallies are 4B-watch until issuance, reserve income, take-rate, and regulation become visible.",
        "- Example: KakaoPay privacy issues and policy-tax shocks are hard RedTeam gates.",
    ]
    return "\n".join(lines) + "\n"


def render_round190_green_guardrail_markdown() -> str:
    lines = [
        "# Round-190 R6 Loop-12 Green Guardrails",
        "",
        "Stage 3-Green is not granted for low-PBR, value-up, stablecoin, Dunamu, FacePay, brokerage, or buyback words alone.",
        "",
        "## Stage 3 Early Catch",
        "",
        "R6 Loop 12 requires at least 6 of 9 checks:",
    ]
    stage3 = next(item for item in ROUND190_STAGE_CAPS if item.stage_band == "Stage 3")
    lines.extend(f"- `{field}`" for field in stage3.required_evidence)
    lines.extend(
        [
            "",
            "## What This Means",
            "",
            "- 삼성생명: 삼성전자 지분/NAV는 Stage 2, K-ICS·CSM·ROE·환원 실행 전 Green 금지.",
            "- 메리츠금융: 반복 환원과 ROE가 자본비율·credit cost와 같이 맞아야 Green 후보.",
            "- 하나금융/Dunamu: 지분가치는 옵션이지만 equity-method income과 보안/규제가 필요.",
            "- KRW stablecoin: 정책 테마와 주가 급등은 4B-watch, 발행량·reserve income·take-rate 전 Green 금지.",
            "- Toss FacePay: 사용자/가맹점 숫자는 Stage 2 인프라, take-rate·거래액·개인정보 통제가 필요.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round190_risk_overlay_markdown() -> str:
    lines = [
        "# Round-190 R6 Loop-12 Risk Overlays",
        "",
        "| target | hard gate | red flags |",
        "| --- | --- | --- |",
    ]
    for target in ROUND190_SCORE_TARGETS:
        lines.append(f"| `{target.target_id}` | {str(target.hard_gate).lower()} | {', '.join(target.red_flags)} |")
    lines.extend(
        [
            "",
            "## Hard / Cap Examples",
            "",
            "- `PAYMENT_PRIVACY_REGULATORY_4C`: 개인정보·동의·플랫폼 신뢰 문제는 결제 플랫폼 Green hard gate다.",
            "- `BUYBACK_EXECUTION_PRICE_FAILED`: 실제 소각도 가격과 영업 논리가 실패하면 Green 근거가 아니다.",
            "- `POLICY_TAX_REVERSAL_MARKET_SHOCK`: 세제 역풍은 value-up 바스켓을 4C-watch로 돌릴 수 있다.",
            "- `KRW_STABLECOIN_POLICY_THEME`: 발행량·reserve income·take-rate 없는 주가 급등은 4B-watch다.",
            "- `DISCLOSURE_CONFIDENCE_CAP`: 환원·자본비율·디지털 수익모델·보안 detail 없으면 Green 금지.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round190_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-190 R6 Loop-12 Price Validation Plan",
        "",
        "R6 Loop 12 must backfill ROE, capital ratio, credit cost, actual return execution, digital-finance revenue model, privacy/security/policy gates, and price-path fields together.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND190_PRICE_FIELDS)
    lines.extend(
        [
            "",
            "## Backfill Priorities",
            "",
            "- `samsung_life_insurance_nav_valueup_stage23_case`: NAV discount, K-ICS, CSM, ROE, return execution, PBR band, 60D/120D MFE.",
            "- `meritz_financial_shareholder_return_stage23_case`: buyback cancellation, dividend, ROE, capital ratio, credit cost, price path.",
            "- `hana_financial_dunamu_equity_option_stage2_case`: stake value, equity-method income, regulation, exchange security, volume/fee durability.",
            "- `krw_stablecoin_policy_theme_4b_watch_case`: issuance, reserve income, take-rate, regulatory status, price-only rally diagnostics.",
            "- `kakaopay_privacy_regulatory_4c_watch_case`: fine, consent resolution, trust metrics, regulator status, price path.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round190_score_stage_price_alignment_markdown() -> str:
    lines = [
        "# Round-190 R6 Loop-12 Score / Stage / Price Alignment",
        "",
        "| case | detected stage | price path status | verdict | adjustment |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in ROUND190_SCORE_STAGE_PRICE_ALIGNMENT:
        lines.append(f"| `{row.case_id}` | {row.detected_stage} | {row.price_path_status} | {row.verdict} | {row.normalization_adjustment} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Samsung Life is the simple NAV example: Samsung Electronics stake value is not enough without K-ICS, CSM, ROE/profit, return execution, and price validation.",
            "- Financial value-up needs ROE, capital ratio, credit cost, and actual return execution, not only low-PBR language.",
            "- Digital-finance options need revenue-model fields such as equity-method income, issuance, reserve income, take-rate, or recurring data revenue.",
            "- Privacy, security, and policy shocks are not score bonuses; they are RedTeam gates that can block Green or create 4C-watch.",
        ]
    )
    return "\n".join(lines) + "\n"


def _round190_score_price_alignment(candidate: Round190CaseCandidate) -> str:
    if candidate.case_type in {"success_candidate", "structural_success"}:
        return "unknown"
    if candidate.case_type in {"event_premium", "4b_watch"}:
        return "price_moved_without_evidence"
    if candidate.case_type == "cyclical_success":
        return "price_moved_without_evidence"
    if candidate.case_type == "4c_thesis_break":
        return "false_positive_score"
    if candidate.case_type == "failed_rerating":
        return "evidence_good_but_price_failed"
    return "unknown"


def _round190_rerating_result(candidate: Round190CaseCandidate) -> str:
    if candidate.case_type in {"success_candidate", "structural_success"}:
        return "unknown"
    if candidate.case_type == "event_premium":
        return "event_premium"
    if candidate.case_type == "cyclical_success":
        return "cyclical_rerating"
    if candidate.case_type == "4b_watch":
        return "theme_overheat"
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    if candidate.case_type == "failed_rerating":
        return "no_rerating"
    return "unknown"


def _numeric_weight(value: int | str) -> float:
    return float(value) if isinstance(value, int) else 0.0


def _write_case_jsonl(records: Iterable[E2RCaseRecord], path: Path) -> None:
    lines = []
    for record in records:
        record.validate()
        lines.append(json.dumps(record.as_dict(), ensure_ascii=False, sort_keys=True))
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def _write_rows(rows: Iterable[Mapping[str, str]], path: Path) -> None:
    rows = tuple(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


__all__ = [
    "ROUND190_BASE_SCORE_WEIGHTS",
    "ROUND190_CASE_CANDIDATES",
    "ROUND190_DEFAULT_CASES_PATH",
    "ROUND190_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND190_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND190_PRICE_FIELDS",
    "ROUND190_SCORE_STAGE_PRICE_ALIGNMENT",
    "ROUND190_SCORE_TARGETS",
    "ROUND190_SOURCE_CANONICAL_TARGET_COUNT",
    "ROUND190_SOURCE_CANONICAL_TARGET_IDS",
    "ROUND190_STAGE_CAPS",
    "render_round190_green_guardrail_markdown",
    "render_round190_price_validation_plan_markdown",
    "render_round190_risk_overlay_markdown",
    "render_round190_score_stage_price_alignment_markdown",
    "render_round190_summary_markdown",
    "round190_base_score_weight_rows",
    "round190_case_candidate_rows",
    "round190_case_records",
    "round190_price_field_rows",
    "round190_score_profile_rows",
    "round190_score_stage_price_alignment_rows",
    "round190_stage_cap_rows",
    "round190_stage_date_rows",
    "round190_summary",
    "round190_target_for",
    "write_round190_r6_loop12_reports",
]
