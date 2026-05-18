"""Round-177 R6 Loop-11 Korea financial, capital allocation, and digital finance.

Round 177 applies Loop 11 to Korea-focused banks, financial holdings,
insurance, brokerages, internet banking, digital-asset equity options, Toss
IPO/stablecoin optionality, and guarantee-insurance security risk.

It is calibration/report material only. Production feature engineering,
scoring, staging, and RedTeam code must not import it.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import CaseDataQuality, E2RCaseRecord, PriceValidation
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture


ROUND177_SOURCE_ROUND_PATH = "docs/round/round_177.md"
ROUND177_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round177_r6_loop11_financial_capital_digital"
ROUND177_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r6_loop11_round177.jsonl"
ROUND177_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round177_r6_loop11_v11.csv"
ROUND177_SOURCE_CANONICAL_TARGET_IDS: tuple[str, ...] = (
    "BANK_HOLDING_VALUEUP_CAPITAL_RETURN_KOREA",
    "BANK_ROE_PBR_RERATING_KOREA",
    "BANK_CREDIT_COST_PF_OVERLAY",
    "REGIONAL_BANK_HIGH_ROE_VALUEUP",
    "INSURANCE_CAPITAL_RELEASE_VALUEUP_KOREA",
    "INSURANCE_KICS_CSM_GATE",
    "SECURITIES_BROKERAGE_MARKET_BETA",
    "SECURITIES_IB_PF_RISK_OVERLAY",
    "INTERNET_BANK_PROFITABILITY",
    "DIGITAL_ASSET_EXCHANGE_EQUITY_OPTION",
    "FINTECH_SUPERAPP_IPO_OPTION_KOREA",
    "KRW_STABLECOIN_POLICY_OPTION",
    "GUARANTEE_INSURANCE_IPO_SECURITY_RISK",
    "DISCLOSURE_CONFIDENCE_CAP",
)
ROUND177_SOURCE_CANONICAL_TARGET_COUNT = len(ROUND177_SOURCE_CANONICAL_TARGET_IDS)


@dataclass(frozen=True)
class Round177ScoreWeightDraft:
    roe_eps_fcf: int | str
    capital_return_execution: int | str
    capital_ratio_credit_cost: int | str
    regulatory_revenue_visibility: int | str
    early_price_validation: int | str
    governance_disclosure: int | str
    valuation_4b_room: int | str

    def as_dict(self) -> dict[str, int | str]:
        return {
            "roe_eps_fcf": self.roe_eps_fcf,
            "capital_return_execution": self.capital_return_execution,
            "capital_ratio_credit_cost": self.capital_ratio_credit_cost,
            "regulatory_revenue_visibility": self.regulatory_revenue_visibility,
            "early_price_validation": self.early_price_validation,
            "governance_disclosure": self.governance_disclosure,
            "valuation_4b_room": self.valuation_4b_room,
        }


@dataclass(frozen=True)
class Round177ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round177ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    loop11_penalty_axes: tuple[str, ...]
    normalization_point: str
    hard_gate: bool = False

    @property
    def large_sector(self) -> Round10LargeSector:
        return Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round177CaseCandidate:
    case_id: str
    target_id: str
    symbol: str
    company_name: str
    market: str
    case_type: str
    stage1_date: date | None
    stage2_date: date | None
    stage3_date: date | None
    stage4b_date: date | None
    stage4c_date: date | None
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
class Round177BaseScoreWeight:
    component: str
    points: int
    loop11_direction: str
    reason: str

    def as_row(self) -> dict[str, str]:
        return {
            "component": self.component,
            "points": str(self.points),
            "loop11_direction": self.loop11_direction,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class Round177StageCap:
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
        }


@dataclass(frozen=True)
class Round177ScoreStagePriceAlignment:
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
        }


def _weights(
    roe: int | str,
    capital_return: int | str,
    capital_credit: int | str,
    regulatory: int | str,
    price: int | str,
    governance: int | str,
    valuation: int | str,
) -> Round177ScoreWeightDraft:
    return Round177ScoreWeightDraft(roe, capital_return, capital_credit, regulatory, price, governance, valuation)


def _target(
    target_id: str,
    archetype: E2RArchetype,
    posture: Round10ThemePosture,
    weight: Round177ScoreWeightDraft,
    *,
    stage1: tuple[str, ...],
    stage2: tuple[str, ...],
    stage3: tuple[str, ...],
    stage4b: tuple[str, ...],
    stage4c: tuple[str, ...],
    green: tuple[str, ...],
    red: tuple[str, ...],
    penalties: tuple[str, ...],
    note: str,
    hard_gate: bool = False,
) -> Round177ScoreTarget:
    return Round177ScoreTarget(
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


GATE_WEIGHT = _weights("gate", "gate", "gate", "gate", "gate", "gate", "gate")


ROUND177_BASE_SCORE_WEIGHTS: tuple[Round177BaseScoreWeight, ...] = (
    Round177BaseScoreWeight("roe_eps_fcf_durability", 22, "raise_profit_quality", "Low PBR is only Stage 1; ROE, net profit, EPS, and FCF durability drive Stage 2/3."),
    Round177BaseScoreWeight("capital_return_execution", 18, "execution_before_policy", "Buyback, cancellation, dividend, payout ratio, and total shareholder return must be executed, not merely expected."),
    Round177BaseScoreWeight("capital_ratio_credit_cost_stability", 18, "hard_quality_gate", "CET1, K-ICS, PF exposure, reserves, and credit cost can block financial rerating."),
    Round177BaseScoreWeight("regulatory_revenue_model_visibility", 14, "digital_finance_gate", "Digital asset, stablecoin, IPO, exchange, and fintech options need approved regulation and revenue economics."),
    Round177BaseScoreWeight("early_price_path_validation", 10, "loop11_axis", "60D/120D MFE and relative strength separate early Stage 3 from late value-up chasing."),
    Round177BaseScoreWeight("governance_disclosure_confidence", 10, "raise_detail_requirement", "Financials need precise disclosure on cancellation, dividend, capital ratio, stake value, and security incidents."),
    Round177BaseScoreWeight("valuation_room_4b_runway", 8, "cool_crowded_valueup", "PBR band expansion and financial-basket crowding reduce Stage 3 runway."),
)


ROUND177_STAGE_CAPS: tuple[Round177StageCap, ...] = (
    Round177StageCap(
        "Stage 1",
        "45",
        ("low_pbr", "valueup_policy", "buyback_cancel_expectation", "stablecoin_theme", "toss_ipo", "dunamu_stake_news"),
        ("kb_financial_valueup_stage3_candidate", "toss_superapp_ipo_stablecoin_related_stock_cap_case"),
        "Low PBR, policy, IPO, or stablecoin names route research only. They do not create Stage 3.",
    ),
    Round177StageCap(
        "Stage 2",
        "70",
        ("actual_buyback_cancel_or_dividend", "roe_cet1_kics_stable", "net_profit_growth", "stake_acquisition", "ipo_filing", "regulatory_bill", "users_or_transaction_volume"),
        ("woori_financial_nonbank_capital_buffer_gate_case", "naver_dunamu_equity_option_security_4c_watch_case"),
        "Stage 2 can be strong, but Green waits for repeat return, capital ratio, credit cost, revenue model, and price path.",
    ),
    Round177StageCap(
        "Stage 3",
        "requires_5_of_8",
        ("roe_or_net_profit_yoy_improves", "cet1_or_kics_stable_after_return", "actual_cancel_or_dividend_expansion", "credit_cost_pf_reserve_stable", "pbr_band_starts_up", "stage2_60d_mfe_20pct", "relative_strength_vs_financial_basket", "repeat_return_or_medium_term_target"),
        ("kb_financial_valueup_stage3_candidate", "shinhan_overseas_profit_valueup_candidate", "jb_financial_regional_high_roe_valueup_case"),
        "Stage 3 requires financial bodyweight and capital quality, not cheap valuation by itself.",
    ),
    Round177StageCap(
        "Stage 4B",
        "requires_3_of_5",
        ("stage2_120d_mfe_60pct", "pbr_breaks_historical_top_band", "valuation_expands_before_return_execution", "financial_basket_crowded", "price_rises_before_credit_cost_confirmation"),
        ("financial_valueup_crowded_4b_watch_case", "kb_financial_valueup_stage3_candidate"),
        "Financial rerating is cooled when PBR and price outrun return execution and credit quality.",
    ),
    Round177StageCap(
        "Stage 4C",
        "hard_gate",
        ("cet1_or_kics_sharp_drop", "pf_credit_cost_spike", "buyback_cancel_cancelled_or_return_cut", "capital_raise_or_at1_pressure", "exchange_hack_abnormal_withdrawal_customer_compensation", "ipo_valuation_cut_or_delay", "stablecoin_rule_hurts_issuer_margin", "ransomware_financial_service_disruption"),
        ("naver_dunamu_equity_option_security_4c_watch_case", "seoul_guarantee_ipo_ransomware_security_case", "bank_credit_cost_pf_overlay_case"),
        "Any capital-ratio, credit, security, regulation, or trust break can block Green immediately.",
    ),
)


ROUND177_SCORE_TARGETS: tuple[Round177ScoreTarget, ...] = (
    _target(
        "BANK_HOLDING_VALUEUP_CAPITAL_RETURN_KOREA",
        E2RArchetype.BANK_HOLDING_VALUEUP_CAPITAL_RETURN_KOREA,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(23, 20, 20, 8, 10, 11, 8),
        stage1=("bank_low_pbr", "korea_discount", "valueup_policy", "buyback_or_dividend_expectation"),
        stage2=("net_profit_growth", "shareholder_return_execution", "cet1_stable", "credit_cost_stable", "pbr_roe_band_watch"),
        stage3=("roe_stable_or_improving", "repeat_return_policy", "cet1_after_return_stable", "credit_cost_pf_controlled", "pbr_roe_band_change"),
        stage4b=("bank_valueup_crowded", "pbr_band_above_history", "return_policy_fully_priced"),
        stage4c=("credit_cost_spike", "pf_loss", "cet1_deterioration", "return_policy_retreat"),
        green=("roe", "net_profit_growth", "cet1_ratio", "credit_cost", "shareholder_return_execution", "pbr_roe_band_change"),
        red=("low_pbr_only", "credit_cost", "pf_exposure", "cet1_deterioration", "return_policy_failure"),
        penalties=("credit_cost", "cet1", "pf_exposure", "return_execution", "valueup_crowding"),
        note="KB/Shinhan/Hana/Woori-style financial holdings can be Green-capable only when return execution and capital quality confirm the rerating.",
    ),
    _target(
        "BANK_ROE_PBR_RERATING_KOREA",
        E2RArchetype.BANK_ROE_PBR_RERATING_KOREA,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(24, 18, 18, 8, 10, 10, 12),
        stage1=("low_pbr_bank_leader", "financial_valueup_rally", "foreign_inflow"),
        stage2=("roe_improves", "record_net_profit", "actual_cancel_or_dividend", "pbr_band_starts_up"),
        stage3=("roe_pbr_frame_change", "credit_cost_stable", "repeat_capital_return", "financial_basket_relative_strength"),
        stage4b=("pbr_band_upper_break", "leader_stock_everyone_knows", "return_execution_fully_priced"),
        stage4c=("roe_down", "pbr_rerating_reverses", "credit_cost_spike", "capital_ratio_hit"),
        green=("roe", "pbr_band_change", "credit_cost", "repeat_capital_return", "relative_strength"),
        red=("pbr_rerating_without_roe", "credit_cost", "capital_ratio_hit", "crowded_valueup"),
        penalties=("roe_quality", "credit_cost", "pbr_crowding"),
        note="KB/Shinhan-style Stage 3 candidate path focuses on ROE/PBR band change and repeat return, not low PBR alone.",
    ),
    _target(
        "BANK_CREDIT_COST_PF_OVERLAY",
        E2RArchetype.BANK_CREDIT_COST_PF_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("pf_exposure_watch", "real_estate_credit_risk", "reserve_build"),
        stage2=("credit_cost_stable", "pf_reserve_adequate"),
        stage3=("not_green_if_credit_cost_spikes",),
        stage4b=("financial_rally_ignores_pf",),
        stage4c=("pf_credit_cost_spike", "reserve_shortfall", "capital_raise_pressure", "return_policy_cut"),
        green=(),
        red=("pf_exposure", "credit_cost_spike", "reserve_shortfall", "capital_raise_pressure", "return_policy_cut"),
        penalties=("pf_exposure", "credit_cost", "reserve", "capital_ratio"),
        note="PF and credit-cost issues are hard RedTeam gates across bank and securities candidates.",
        hard_gate=True,
    ),
    _target(
        "REGIONAL_BANK_HIGH_ROE_VALUEUP",
        E2RArchetype.REGIONAL_BANK_HIGH_ROE_VALUEUP,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(22, 18, 20, 6, 10, 10, 8),
        stage1=("regional_bank_low_pbr", "high_dividend", "activist_pressure"),
        stage2=("high_roe", "dividend_policy", "regional_credit_quality", "southeast_asia_subsidiary"),
        stage3=("credit_cost_stable", "repeat_dividend_or_cancel", "pbr_band_up", "liquidity_discount_eases"),
        stage4b=("small_financial_valueup_basket_spike", "trading_value_thin"),
        stage4c=("regional_credit_quality_worse", "liquidity_gap", "dividend_cut"),
        green=("high_roe", "credit_cost_stable", "dividend_policy", "pbr_band_change", "liquidity_discount_eases"),
        red=("regional_credit_risk", "liquidity_discount", "dividend_sustainability_unknown"),
        penalties=("credit_quality", "liquidity", "dividend_sustainability"),
        note="JB/BNK/DGB-style regional banks can reach Stage 2/3 but liquidity and regional credit risk cap the score.",
    ),
    _target(
        "INSURANCE_CAPITAL_RELEASE_VALUEUP_KOREA",
        E2RArchetype.INSURANCE_CAPITAL_RELEASE_VALUEUP_KOREA,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(22, 18, 20, 6, 10, 10, 8),
        stage1=("insurance_valueup", "dividend_expectation", "capital_release"),
        stage2=("k_ics_stable", "csm_quality", "loss_ratio_stable", "dividend_or_buyback_execution"),
        stage3=("capital_release_repeatable", "roe_improves", "k_ics_after_return_stable", "csm_margin_quality"),
        stage4b=("insurance_dividend_yield_chasing", "kics_csm_not_confirmed_but_price_up"),
        stage4c=("k_ics_drop", "csm_quality_damage", "loss_ratio_worse", "investment_loss"),
        green=("k_ics_ratio", "csm_quality", "loss_ratio", "roe", "shareholder_return_execution"),
        red=("k_ics_unknown", "csm_quality_unknown", "loss_ratio_worse", "ifrs17_volatility"),
        penalties=("k_ics", "csm", "loss_ratio", "ifrs17"),
        note="DB Insurance/Samsung Fire-style candidates need K-ICS, CSM, loss ratio, and return execution before Stage 3.",
    ),
    _target(
        "INSURANCE_KICS_CSM_GATE",
        E2RArchetype.INSURANCE_KICS_CSM_GATE,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("insurance_yield_rally", "csm_headline", "k_ics_headline"),
        stage2=("k_ics_detail_required", "csm_quality_required", "loss_ratio_required"),
        stage3=("not_green_without_kics_csm_loss_ratio",),
        stage4b=("dividend_expectation_before_capital_quality",),
        stage4c=("k_ics_drop", "csm_quality_damage", "loss_ratio_spike", "ifrs17_volatility"),
        green=(),
        red=("k_ics_missing", "csm_quality_missing", "loss_ratio_missing", "capital_release_unverified"),
        penalties=("k_ics", "csm", "loss_ratio"),
        note="Insurance headlines are capped before K-ICS, CSM quality, and loss-ratio detail.",
        hard_gate=True,
    ),
    _target(
        "SECURITIES_BROKERAGE_MARKET_BETA",
        E2RArchetype.SECURITIES_BROKERAGE_MARKET_BETA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(20, 8, 12, 8, 10, 10, 7),
        stage1=("kospi_rally", "trading_value_growth", "brokerage_beta"),
        stage2=("brokerage_revenue_growth", "margin_lending_growth", "ib_pipeline", "op_eps_revision"),
        stage3=("roe_structure_improved", "ib_pipeline_durable", "pf_risk_low", "market_beta_not_only_driver"),
        stage4b=("trading_value_cycle_peak", "securities_basket_overheated"),
        stage4c=("trading_value_drop", "pf_loss", "ib_loss", "tax_policy_shock"),
        green=("brokerage_revenue", "ib_fee", "pf_risk_low", "roe_improvement"),
        red=("market_beta_only", "trading_value_drop", "pf_loss", "tax_policy_shock"),
        penalties=("market_beta", "pf_loss", "tax_policy", "trading_value_cycle"),
        note="Brokerage can reach Stage 2 on market beta, but Stage 3 is capped unless IB, PF, and ROE durability confirm.",
    ),
    _target(
        "SECURITIES_IB_PF_RISK_OVERLAY",
        E2RArchetype.SECURITIES_IB_PF_RISK_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("ib_pf_watch", "real_estate_pf_exposure"),
        stage2=("ib_pipeline", "pf_exposure_disclosed"),
        stage3=("not_green_if_pf_loss_or_ib_impairment",),
        stage4b=("brokerage_rally_ignores_pf",),
        stage4c=("pf_loss", "ib_impairment", "liquidity_stress", "capital_raise"),
        green=(),
        red=("pf_loss", "ib_impairment", "liquidity_stress", "capital_raise"),
        penalties=("pf", "ib_loss", "liquidity"),
        note="Securities PF/IB loss is a hard cap for brokerage rerating.",
        hard_gate=True,
    ),
    _target(
        "INTERNET_BANK_PROFITABILITY",
        E2RArchetype.INTERNET_BANK_PROFITABILITY,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(22, 8, 18, 18, 10, 10, 7),
        stage1=("internet_bank_users", "mau", "platform_bank_premium"),
        stage2=("record_profit", "non_interest_income_growth", "overseas_virtual_bank_option", "loan_growth_quality"),
        stage3=("roe_improves", "credit_cost_stable", "repeat_non_interest_income", "valuation_not_overheated"),
        stage4b=("platform_premium_before_profit", "users_without_profit_bodyweight"),
        stage4c=("credit_cost_spike", "loan_quality_worse", "valuation_derating", "overseas_option_delay"),
        green=("record_profit", "roe", "credit_cost", "non_interest_income_repeatability", "valuation_room"),
        red=("user_count_only", "credit_cost_unknown", "platform_valuation_risk", "loan_quality_risk"),
        penalties=("valuation", "credit_cost", "loan_quality", "user_count_only"),
        note="KakaoBank needs record profit, non-interest income, credit quality, and valuation discipline; users alone are Stage 1.",
    ),
    _target(
        "DIGITAL_ASSET_EXCHANGE_EQUITY_OPTION",
        E2RArchetype.DIGITAL_ASSET_EXCHANGE_EQUITY_OPTION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(14, 6, 8, 24, 10, 14, 8),
        stage1=("dunamu_upbit_stake", "digital_asset_option", "stablecoin_growth"),
        stage2=("all_stock_deal_value", "exchange_market_share", "stock_swap_terms", "initial_price_reaction"),
        stage3=("regulatory_approval", "exchange_security_stable", "equity_value_transmission", "fee_or_stablecoin_revenue"),
        stage4b=("crypto_equity_option_priced_before_approval",),
        stage4c=("abnormal_withdrawal", "exchange_hack", "regulatory_approval_fail", "crypto_volume_decline"),
        green=("regulatory_approval", "security_stability", "equity_method_income", "revenue_model", "shareholder_value_transmission"),
        red=("abnormal_withdrawal", "security_incident", "regulatory_pending", "crypto_volume_decline"),
        penalties=("security", "regulatory", "equity_transmission", "crypto_volume"),
        note="Naver-Dunamu-style equity option can be Stage 2, but security and approval block Stage 3.",
    ),
    _target(
        "FINTECH_SUPERAPP_IPO_OPTION_KOREA",
        E2RArchetype.FINTECH_SUPERAPP_IPO_OPTION_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(12, 5, 8, 25, 10, 12, 8),
        stage1=("toss_ipo_expectation", "superapp_users", "won_stablecoin_theme"),
        stage2=("30m_users", "global_launch", "ipo_valuation_expectation", "stablecoin_bill_expectation"),
        stage3=("ipo_filing", "profitability_fcf", "regulated_stablecoin_approval", "direct_equity_link"),
        stage4b=("related_stocks_spike_without_equity_link", "ipo_narrative_crowded"),
        stage4c=("ipo_delay", "valuation_cut", "stablecoin_rule_restrictive", "credit_loss_or_cac_worse"),
        green=("ipo_filing", "profitability", "fcf", "direct_equity_link", "regulated_revenue_model"),
        red=("related_stock_without_link", "valuation_cut", "ipo_delay", "stablecoin_unapproved"),
        penalties=("ipo_delay", "direct_link", "stablecoin_approval", "valuation"),
        note="Toss direct exposure can be Stage 2; listed related stocks are capped before direct ownership and revenue model proof.",
    ),
    _target(
        "KRW_STABLECOIN_POLICY_OPTION",
        E2RArchetype.KRW_STABLECOIN_POLICY_OPTION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(8, 4, 6, 28, 10, 14, 8),
        stage1=("won_stablecoin_policy", "payment_theme", "fintech_theme"),
        stage2=("regulatory_bill", "issuer_candidate", "reserve_model_discussion", "payment_volume_option"),
        stage3=("regulatory_approval", "issued_volume", "reserve_economics", "issuer_margin", "redemption_transparency"),
        stage4b=("stablecoin_related_stock_rally_before_revenue",),
        stage4c=("issuer_margin_hurt_by_rule", "redemption_or_reserve_issue", "regulatory_delay"),
        green=(),
        red=("regulatory_approval_missing", "issued_volume_missing", "reserve_economics_missing", "issuer_margin_unknown"),
        penalties=("regulatory", "reserve", "issuer_margin", "volume"),
        note="KRW stablecoin is Stage 1/2 optionality until approval, volume, reserve, redemption, and issuer economics are visible.",
    ),
    _target(
        "GUARANTEE_INSURANCE_IPO_SECURITY_RISK",
        E2RArchetype.GUARANTEE_INSURANCE_IPO_SECURITY_RISK,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights(18, 12, 18, 8, 8, 20, 6),
        stage1=("guarantee_insurance_ipo", "public_fund_recovery", "dividend_expectation"),
        stage2=("kospi_listing", "guarantee_balance_scale", "kdic_stake_sale_option"),
        stage3=("cyber_resilience_confirmed", "dividend_policy", "capital_quality", "service_stability"),
        stage4b=("stable_financial_ipo_premium_priced",),
        stage4c=("ransomware_attack", "service_disruption", "core_system_recovery_delay", "financial_security_trust_break"),
        green=("cyber_resilience", "service_stability", "capital_quality", "dividend_policy"),
        red=("ransomware", "service_disruption", "security_remediation_missing", "trust_break"),
        penalties=("security", "service_disruption", "trust"),
        note="Seoul Guarantee IPO optionality is capped by ransomware and financial-service operational trust risk.",
        hard_gate=True,
    ),
    _target(
        "DISCLOSURE_CONFIDENCE_CAP",
        E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("cap", "cap", "cap", "cap", "cap", "+", "cap"),
        stage1=("opendart_list_only", "policy_headline", "media_report_only"),
        stage2=("detail_fetch_required", "buyback_cancel_detail", "dividend_detail", "capital_ratio_detail", "stake_terms"),
        stage3=("multi_source_confirmation", "capital_return_executed", "capital_ratio_verified", "security_incident_absent"),
        stage4b=("financial_headline_rally",),
        stage4c=("capital_ratio_missing", "return_detail_missing", "security_detail_missing", "routine_disclosure_only"),
        green=("capital_return_detail", "capital_ratio_detail", "credit_cost_detail", "regulatory_detail", "security_detail"),
        red=("detail_missing", "routine_disclosure_only", "capital_ratio_unknown", "security_detail_missing"),
        penalties=("disclosure_detail", "capital_ratio", "credit_cost", "security"),
        note="OpenDART list or policy headlines cannot support financial Green without detailed capital, return, credit, and security evidence.",
    ),
    _target(
        "VALUE_UP_CROWDED_4B_WATCH",
        E2RArchetype.VALUE_UP_CROWDED_4B_WATCH,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("watch", "watch", "watch", "watch", "watch", "+", "watch"),
        stage1=("valueup_reform", "financial_basket_rally"),
        stage2=("financial_shares_broad_rally", "market_reform_expectation"),
        stage3=("individual_roe_return_credit_confirmed",),
        stage4b=("financial_basket_crowded", "pbr_rerating_before_execution", "credit_cost_unconfirmed_price_rise"),
        stage4c=("policy_tax_shock", "return_execution_failure", "credit_cost_spike"),
        green=(),
        red=("crowded_valueup", "policy_only", "execution_missing", "credit_cost_unconfirmed"),
        penalties=("crowding", "policy_only", "execution_missing"),
        note="Financial value-up basket rally is useful for 4B cooling, not automatic Green.",
        hard_gate=True,
    ),
)


ROUND177_CASE_CANDIDATES: tuple[Round177CaseCandidate, ...] = (
    Round177CaseCandidate(
        "kb_financial_valueup_stage3_candidate",
        "BANK_HOLDING_VALUEUP_CAPITAL_RETURN_KOREA",
        "105560",
        "KB Financial value-up leader",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("net_profit_5_84tn_krw", "net_profit_growth_15_1pct", "financial_holding_valueup_leader", "capital_return_execution_required"),
        ("credit_cost_unconfirmed", "cet1_unconfirmed", "pbr_crowding_4b_risk"),
        "stage3_candidate_with_4b_watch",
        "needs_krx_price_cet1_credit_cost_return_backfill",
        ("round_177.md KB Financial value-up case",),
        "KB is a canonical R6 Stage 3 candidate, but Green needs CET1, credit cost, repeated return, and PBR band proof.",
        (E2RArchetype.BANK_ROE_PBR_RERATING_KOREA, E2RArchetype.VALUE_UP_CROWDED_4B_WATCH),
    ),
    Round177CaseCandidate(
        "shinhan_overseas_profit_valueup_candidate",
        "BANK_ROE_PBR_RERATING_KOREA",
        "055550",
        "Shinhan Financial overseas-profit rerating candidate",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("net_profit_4_97tn_krw", "net_profit_growth_11_7pct", "overseas_pre_tax_profit_over_1tn_krw", "profit_diversification"),
        ("cet1_unconfirmed", "return_execution_needed", "financial_basket_4b_crowding"),
        "overseas_profit_diversification_stage2_3_candidate",
        "needs_price_roe_cet1_return_backfill",
        ("round_177.md Shinhan overseas profit case",),
        "Shinhan is a Stage 2/3 candidate when overseas profit and return execution become repeatable.",
        (E2RArchetype.BANK_HOLDING_VALUEUP_CAPITAL_RETURN_KOREA,),
    ),
    Round177CaseCandidate(
        "woori_financial_nonbank_capital_buffer_gate_case",
        "BANK_HOLDING_VALUEUP_CAPITAL_RETURN_KOREA",
        "316140",
        "Woori Financial non-bank expansion with capital-buffer gate",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("net_profit_3_14tn_krw", "non_bank_expansion", "insurance_acquisition", "digital_tower_sale_capital_buffer_review"),
        ("cet1_pressure", "capital_buffer_needed", "return_cut_risk"),
        "stage2_with_cet1_gate",
        "needs_cet1_mna_return_price_backfill",
        ("round_177.md Woori insurance acquisition and capital buffer case",),
        "Woori is Stage 2 until non-bank expansion proves CET1 and return-policy durability.",
        (E2RArchetype.BANK_CREDIT_COST_PF_OVERLAY,),
    ),
    Round177CaseCandidate(
        "jb_financial_regional_high_roe_valueup_case",
        "REGIONAL_BANK_HIGH_ROE_VALUEUP",
        "175330",
        "JB Financial regional-bank high-ROE value-up candidate",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("ttm_net_profit_578_7bn_krw", "asset_50_8tn_krw", "high_profitability", "southeast_asia_subsidiary"),
        ("regional_credit_risk", "liquidity_discount", "dividend_sustainability_needed"),
        "regional_bank_stage2_3_candidate_with_liquidity_cap",
        "needs_price_roe_credit_liquidity_backfill",
        ("round_177.md JB Financial regional value-up case",),
        "Regional banks can be early Stage 3 only when high ROE survives credit and liquidity checks.",
    ),
    Round177CaseCandidate(
        "korea_insurance_capital_release_valueup_case",
        "INSURANCE_CAPITAL_RELEASE_VALUEUP_KOREA",
        "005830/000810/001450",
        "DB Insurance / Samsung Fire / Hyundai Marine insurance value-up basket",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("capital_release", "dividend_buyback_expectation", "csm_kics_required", "loss_ratio_required"),
        ("k_ics_unknown", "csm_quality_unknown", "loss_ratio_unknown", "ifrs17_volatility"),
        "insurance_stage2_3_candidate_with_kics_csm_gate",
        "needs_kics_csm_loss_ratio_price_backfill",
        ("round_177.md insurance value-up section",),
        "Insurance names are Stage 2/3 only when K-ICS, CSM quality, loss ratio, and return execution are verified.",
        (E2RArchetype.INSURANCE_KICS_CSM_GATE,),
    ),
    Round177CaseCandidate(
        "kakaobank_profitability_valuation_cap_case",
        "INTERNET_BANK_PROFITABILITY",
        "323410",
        "KakaoBank internet-bank profitability with valuation cap",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("customer_count_26_7m", "mau_20m", "record_profit", "non_interest_income_growth", "indonesia_superbank_thailand_virtual_bank_option"),
        ("platform_valuation_risk", "credit_cost_unconfirmed", "loan_quality_risk", "users_only_not_green"),
        "platform_bank_stage2_3_candidate_with_valuation_cap",
        "needs_profit_credit_cost_valuation_price_backfill",
        ("round_177.md KakaoBank internet-bank profitability case",),
        "KakaoBank is judged by record profit, non-interest income, and credit cost, not user count alone.",
    ),
    Round177CaseCandidate(
        "naver_dunamu_equity_option_security_4c_watch_case",
        "DIGITAL_ASSET_EXCHANGE_EQUITY_OPTION",
        "035420",
        "Naver-Dunamu digital-asset equity option with security watch",
        "KR",
        "4c_thesis_break",
        date(2025, 11, 27),
        date(2025, 11, 27),
        None,
        None,
        date(2025, 11, 27),
        ("dunamu_15_13tn_krw_all_stock_deal", "naver_financial_2_54_shares_per_dunamu_share", "initial_stock_reaction_plus_7pct", "upbit_market_share"),
        ("abnormal_withdrawal_54bn_krw", "security_incident", "regulatory_approval_pending", "crypto_volume_risk"),
        "stage2_plus_same_day_4c_watch",
        "needs_intraday_and_krx_path_security_resolution_backfill",
        ("round_177.md Reuters Naver-Dunamu deal and abnormal withdrawal",),
        "The deal is Stage 2 equity-option evidence, but abnormal withdrawal makes security a hard Stage 4C-watch.",
        (E2RArchetype.EXCHANGE_SECURITY_OPERATIONAL_RISK, E2RArchetype.KRW_STABLECOIN_POLICY_OPTION),
    ),
    Round177CaseCandidate(
        "toss_superapp_ipo_stablecoin_related_stock_cap_case",
        "FINTECH_SUPERAPP_IPO_OPTION_KOREA",
        "TOSS_RELATED_BASKET",
        "Toss superapp IPO and KRW stablecoin option related-stock cap",
        "KR",
        "event_premium",
        date(2025, 9, 9),
        date(2025, 9, 9),
        None,
        None,
        None,
        ("30m_plus_users", "australia_launch", "us_ipo_target_2026_q2", "valuation_10_15bn_usd", "won_stablecoin_intent"),
        ("direct_ownership_link_missing", "ipo_not_filed", "stablecoin_approval_missing", "revenue_model_missing"),
        "stage1_2_option_related_stock_green_cap",
        "not_price_applicable_related_basket",
        ("round_177.md Reuters Toss global push and stablecoin intent",),
        "Toss direct exposure can be Stage 2, but listed related stocks cannot become Green before direct equity and revenue-model proof.",
        (E2RArchetype.KRW_STABLECOIN_POLICY_OPTION,),
    ),
    Round177CaseCandidate(
        "seoul_guarantee_ipo_ransomware_security_case",
        "GUARANTEE_INSURANCE_IPO_SECURITY_RISK",
        "SGI",
        "Seoul Guarantee Insurance IPO with ransomware trust break",
        "KR",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        None,
        ("kospi_listing", "guarantee_balance_344_4bn_usd", "kdic_stake_sale_option", "dividend_public_fund_recovery"),
        ("ransomware_attack", "service_disruption", "core_system_recovery_4_days", "financial_security_trust_break"),
        "ipo_stage2_but_security_hard_cap",
        "needs_listing_price_and_security_remediation_backfill",
        ("round_177.md Seoul Guarantee Insurance IPO and ransomware case",),
        "Financial-service security failure blocks stable guarantee-insurance Green until resilience is proven.",
    ),
    Round177CaseCandidate(
        "securities_brokerage_market_beta_cycle_case",
        "SECURITIES_BROKERAGE_MARKET_BETA",
        "039490/006800/071050/005940",
        "Kiwoom / Mirae / Korea Investment / NH securities brokerage beta basket",
        "KR",
        "cyclical_success",
        date(2026, 5, 6),
        date(2026, 5, 6),
        None,
        None,
        None,
        ("kospi_7000_rally", "trading_value_beta", "brokerage_volume", "ib_pipeline_needed"),
        ("market_beta_only", "pf_exposure", "trading_value_cycle", "tax_policy_risk"),
        "stage2_cycle_not_structural_green",
        "needs_trading_value_pf_ib_price_backfill",
        ("round_177.md Reuters KOSPI 7000 and securities beta case",),
        "Brokerages can be Stage 2 cycle winners, but market turnover alone is not structural Stage 3.",
        (E2RArchetype.SECURITIES_IB_PF_RISK_OVERLAY,),
    ),
    Round177CaseCandidate(
        "financial_valueup_crowded_4b_watch_case",
        "VALUE_UP_CROWDED_4B_WATCH",
        "KR_FINANCIAL_BASKET",
        "Korea financial value-up crowded 4B watch",
        "KR",
        "4b_watch",
        date(2026, 5, 6),
        date(2026, 5, 6),
        None,
        date(2026, 5, 6),
        None,
        ("kospi_7000_reform_ai_rally", "broader_financial_shares_rally", "valueup_consensus", "pbr_rerating"),
        ("financial_basket_crowded", "return_execution_not_individualized", "credit_cost_unconfirmed", "policy_tax_shock_risk"),
        "valueup_basket_4b_watch",
        "needs_basket_relative_strength_pbr_band_backfill",
        ("round_177.md Reuters KOSPI 7000 financial rally",),
        "Broad financial value-up rally is a 4B cooling signal unless individual ROE, return, and credit quality keep improving.",
    ),
    Round177CaseCandidate(
        "bank_credit_cost_pf_overlay_case",
        "BANK_CREDIT_COST_PF_OVERLAY",
        "KR_BANK_SECURITIES_BASKET",
        "Korea bank and securities PF credit-cost overlay",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("pf_exposure", "real_estate_credit_cost", "reserve_build_required", "capital_ratio_required"),
        ("pf_credit_cost_spike", "reserve_shortfall", "capital_raise_pressure", "return_policy_cut"),
        "credit_cost_pf_hard_gate",
        "not_price_applicable_overlay",
        ("round_177.md PF credit cost hard gate",),
        "PF credit-cost spikes override value-up narratives across banks and securities.",
    ),
    Round177CaseCandidate(
        "financial_disclosure_confidence_cap_case",
        "DISCLOSURE_CONFIDENCE_CAP",
        "KR_FINANCIAL_DISCLOSURE_BASKET",
        "Financial disclosure detail confidence cap",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("opendart_list_only", "buyback_dividend_headline", "capital_ratio_headline", "stake_value_headline"),
        ("return_detail_missing", "capital_ratio_unknown", "credit_cost_unknown", "security_detail_missing"),
        "financial_headline_without_detail_cap",
        "not_price_applicable_overlay",
        ("round_177.md OpenDART detail fetch and disclosure confidence note",),
        "Financial headlines need detail fetch and normalized fields before Green evidence.",
    ),
)


ROUND177_SCORE_STAGE_PRICE_ALIGNMENT: tuple[Round177ScoreStagePriceAlignment, ...] = (
    Round177ScoreStagePriceAlignment("kb_financial_valueup_stage3_candidate", "Stage 3 candidate + 4B-watch", "Net profit and leader frame strong; KRX/PBR/CET1 path need backfill", "valueup_leader_requires_capital_quality", "credit profit and return; cap before CET1, credit cost, and PBR-band proof"),
    Round177ScoreStagePriceAlignment("shinhan_overseas_profit_valueup_candidate", "Stage 2/3 candidate", "Overseas profit diversification supports rerating but return execution needs proof", "overseas_profit_diversification_candidate", "credit overseas profit; require repeat return and CET1"),
    Round177ScoreStagePriceAlignment("woori_financial_nonbank_capital_buffer_gate_case", "Stage 2", "Non-bank expansion has CET1/capital-buffer gate", "nonbank_expansion_capital_gate", "credit M&A option; cap before CET1 and return durability"),
    Round177ScoreStagePriceAlignment("jb_financial_regional_high_roe_valueup_case", "Stage 2/3 candidate", "High ROE regional bank needs liquidity and credit quality checks", "regional_high_roe_with_liquidity_cap", "credit high ROE; penalize liquidity and regional credit risk"),
    Round177ScoreStagePriceAlignment("korea_insurance_capital_release_valueup_case", "Stage 2/3 candidate", "Capital release needs K-ICS, CSM, loss ratio, and IFRS17 quality", "insurance_capital_release_requires_kics_csm", "credit return option; cap before K-ICS/CSM/loss ratio"),
    Round177ScoreStagePriceAlignment("kakaobank_profitability_valuation_cap_case", "Stage 2/3 candidate", "Record profit and non-interest income matter; users alone do not", "internet_bank_profit_not_user_count", "credit profit model; penalize credit cost and platform valuation"),
    Round177ScoreStagePriceAlignment("naver_dunamu_equity_option_security_4c_watch_case", "Stage 2 + 4C-watch", "Deal-value reaction and abnormal withdrawal occur together", "digital_asset_equity_option_security_gate", "credit deal value; hard-review security and approval"),
    Round177ScoreStagePriceAlignment("toss_superapp_ipo_stablecoin_related_stock_cap_case", "Stage 1/2 option", "Toss story is strong but listed related-stock linkage is missing", "related_stock_green_cap", "credit optionality; require IPO filing, direct equity, and revenue model"),
    Round177ScoreStagePriceAlignment("seoul_guarantee_ipo_ransomware_security_case", "Stage 2 -> 4C-watch", "IPO and guarantee balance are offset by ransomware service disruption", "guarantee_insurance_security_hard_cap", "credit IPO option; block Green before security remediation"),
    Round177ScoreStagePriceAlignment("securities_brokerage_market_beta_cycle_case", "Stage 2 cycle", "KOSPI rally can lift brokerage revenue but remains cyclical", "brokerage_market_beta_not_green", "credit trading value; cap before IB/PF/ROE durability"),
    Round177ScoreStagePriceAlignment("financial_valueup_crowded_4b_watch_case", "4B-watch", "Financial basket rally can outrun individual return and credit confirmation", "valueup_crowding_4b_watch", "cool broad basket when PBR rerating precedes execution"),
    Round177ScoreStagePriceAlignment("bank_credit_cost_pf_overlay_case", "hard gate", "PF credit cost can invalidate value-up narratives", "pf_credit_cost_hard_gate", "require reserve and capital-ratio proof"),
)


ROUND177_PRICE_FIELDS: tuple[str, ...] = (
    "ticker",
    "symbol",
    "company_name",
    "primary_archetype",
    "secondary_archetypes",
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
    "return_20d_after_stage2",
    "return_60d_after_stage2",
    "return_120d_after_stage2",
    "return_252d_after_stage2",
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
    "roe",
    "roe_change_yoy",
    "net_profit",
    "net_profit_growth_yoy",
    "cet1_ratio",
    "cet1_change_qoq",
    "k_ics_ratio",
    "credit_cost",
    "pf_exposure",
    "reserve_build",
    "dividend_per_share",
    "dividend_payout_ratio",
    "buyback_amount",
    "cancelled_share_amount",
    "total_shareholder_return_ratio",
    "pbr_at_stage2",
    "pbr_at_stage3",
    "pbr_at_stage4b",
    "pbr_band_percentile",
    "digital_asset_stake_value",
    "equity_method_income",
    "exchange_security_incident_flag",
    "stablecoin_regulatory_status",
    "fintech_take_rate",
    "ipo_valuation",
    "ipo_delay_flag",
    "disclosure_confidence",
    "governance_risk_flag",
    "stage_before_redteam",
    "stage_after_redteam",
    "score_before_redteam",
    "score_after_redteam",
    "score_price_alignment",
    "price_validation_status",
    "review_notes",
)


def round177_target_for(target_id: str) -> Round177ScoreTarget | None:
    for target in ROUND177_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round177_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND177_CASE_CANDIDATES:
        target = round177_target_for(candidate.target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {candidate.target_id}")
        weights = target.score_weight.as_dict()
        stage4b_evidence = candidate.evidence_fields if candidate.case_type in {"4b_watch", "overheat"} or candidate.stage4b_date else ()
        stage4c_evidence = candidate.red_flag_fields if candidate.case_type == "4c_thesis_break" or candidate.stage4c_date or target.hard_gate else ()
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
            stage1_date=candidate.stage1_date,
            stage2_date=candidate.stage2_date,
            stage3_date=candidate.stage3_date,
            stage4b_date=candidate.stage4b_date,
            stage4c_date=candidate.stage4c_date,
            evidence_summary=(
                f"Round177 R6 Loop-11 Korea financial/capital/digital case for {candidate.target_id}; "
                "calibration-only and focused on ROE, capital return, capital ratio, credit cost, regulation, security, and price path."
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
                if candidate.case_type in {"failed_rerating", "event_premium", "overheat", "4b_watch", "4c_thesis_break", "one_off"}
                else None
            ),
            score_price_alignment=_round177_score_price_alignment(candidate),
            rerating_result=_round177_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
            score_weight_hint={
                "roe_eps_fcf": _numeric_weight(weights["roe_eps_fcf"]),
                "capital_return_execution": _numeric_weight(weights["capital_return_execution"]),
                "capital_ratio_credit_cost": _numeric_weight(weights["capital_ratio_credit_cost"]),
                "regulatory_revenue_visibility": _numeric_weight(weights["regulatory_revenue_visibility"]),
                "early_price_validation": _numeric_weight(weights["early_price_validation"]),
                "governance_disclosure": _numeric_weight(weights["governance_disclosure"]),
                "valuation_4b_room": _numeric_weight(weights["valuation_4b_room"]),
            },
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "low_pbr_valueup_high_dividend_stablecoin_toss_ipo_or_dunamu_headline_is_not_structural_evidence",
                "require_roe_cet1_kics_credit_cost_actual_return_revenue_model_and_price_path_for_green",
                "stage3_early_catch_requires_5_of_8_loop11_conditions",
                "stage4b_cooling_requires_3_of_5_loop11_conditions",
                "do_not_invent_cet1_kics_credit_cost_pf_return_stake_value_security_resolution_stage_prices_or_mfe_mae",
                "security_regulatory_credit_or_capital_ratio_break_blocks_green",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=False,
                price_data_available=False,
                stage_dates_confidence=0.75
                if candidate.stage1_date or candidate.stage2_date or candidate.stage3_date or candidate.stage4b_date or candidate.stage4c_date
                else 0.2,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round177_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND177_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "roe_eps_fcf": str(weights["roe_eps_fcf"]),
                "capital_return_execution": str(weights["capital_return_execution"]),
                "capital_ratio_credit_cost": str(weights["capital_ratio_credit_cost"]),
                "regulatory_revenue_visibility": str(weights["regulatory_revenue_visibility"]),
                "early_price_validation": str(weights["early_price_validation"]),
                "governance_disclosure": str(weights["governance_disclosure"]),
                "valuation_4b_room": str(weights["valuation_4b_room"]),
                "stage1_signals": "|".join(target.stage1_signals),
                "stage2_signals": "|".join(target.stage2_signals),
                "stage3_conditions": "|".join(target.stage3_conditions),
                "stage4b_conditions": "|".join(target.stage4b_conditions),
                "stage4c_conditions": "|".join(target.stage4c_conditions),
                "green_conditions": "|".join(target.green_conditions),
                "red_flags": "|".join(target.red_flags),
                "loop11_penalty_axes": "|".join(target.loop11_penalty_axes),
                "hard_gate": str(target.hard_gate).lower(),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round177_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND177_CASE_CANDIDATES:
        target = round177_target_for(candidate.target_id)
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
                "stage1_date": candidate.stage1_date.isoformat() if candidate.stage1_date else "",
                "stage2_date": candidate.stage2_date.isoformat() if candidate.stage2_date else "",
                "stage3_date": candidate.stage3_date.isoformat() if candidate.stage3_date else "",
                "stage4b_date": candidate.stage4b_date.isoformat() if candidate.stage4b_date else "",
                "stage4c_date": candidate.stage4c_date.isoformat() if candidate.stage4c_date else "",
                "evidence_fields": "|".join(candidate.evidence_fields),
                "red_flag_fields": "|".join(candidate.red_flag_fields),
                "alignment_hint": candidate.alignment_hint,
                "price_validation_status": candidate.price_validation_status,
                "production_input": "false",
                "notes": candidate.notes,
            }
        )
    return tuple(rows)


def round177_stage_date_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "target_id": target.target_id,
            "stage1": "|".join(target.stage1_signals),
            "stage2": "|".join(target.stage2_signals),
            "stage3": "|".join(target.stage3_conditions),
            "stage4b": "|".join(target.stage4b_conditions),
            "stage4c": "|".join(target.stage4c_conditions),
            "loop11_penalty_axes": "|".join(target.loop11_penalty_axes),
            "hard_gate": str(target.hard_gate).lower(),
            "production_scoring_changed": "false",
        }
        for target in ROUND177_SCORE_TARGETS
    )


def round177_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round177_backfill": "true"} for field in ROUND177_PRICE_FIELDS)


def round177_base_score_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(weight.as_row() for weight in ROUND177_BASE_SCORE_WEIGHTS)


def round177_stage_cap_rows() -> tuple[dict[str, str], ...]:
    return tuple(cap.as_row() for cap in ROUND177_STAGE_CAPS)


def round177_score_stage_price_alignment_rows() -> tuple[dict[str, str], ...]:
    return tuple(row.as_row() for row in ROUND177_SCORE_STAGE_PRICE_ALIGNMENT)


def round177_summary() -> dict[str, int | bool]:
    records = round177_case_records()
    return {
        "target_count": len(ROUND177_SCORE_TARGETS),
        "source_canonical_target_count": ROUND177_SOURCE_CANONICAL_TARGET_COUNT,
        "case_candidate_count": len(records),
        "base_score_component_count": len(ROUND177_BASE_SCORE_WEIGHTS),
        "stage_cap_count": len(ROUND177_STAGE_CAPS),
        "score_stage_price_alignment_count": len(ROUND177_SCORE_STAGE_PRICE_ALIGNMENT),
        "structural_success_count": sum(1 for record in records if record.case_type == "structural_success"),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for record in records if record.case_type == "cyclical_success"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND177_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND177_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND177_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "hard_gate_target_count": sum(1 for target in ROUND177_SCORE_TARGETS if target.hard_gate),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round177_r6_loop11_reports(
    *,
    output_directory: str | Path = ROUND177_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND177_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND177_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round177_r6_loop11_financial_capital_digital_summary.md",
        "case_matrix": output / "round177_r6_loop11_case_matrix.csv",
        "stage_date_plan": output / "round177_r6_loop11_stage_date_plan.csv",
        "green_guardrails": output / "round177_r6_loop11_green_guardrails.md",
        "risk_overlays": output / "round177_r6_loop11_risk_overlays.md",
        "price_validation_plan": output / "round177_r6_loop11_price_validation_plan.md",
        "price_fields": output / "round177_r6_loop11_price_fields.csv",
        "base_score_weights": output / "round177_r6_loop11_base_score_weights.csv",
        "stage_caps": output / "round177_r6_loop11_stage_caps.csv",
        "score_stage_price_alignment": output / "round177_r6_loop11_score_stage_price_alignment.csv",
        "score_stage_price_alignment_md": output / "round177_r6_loop11_score_stage_price_alignment.md",
    }
    _write_case_jsonl(round177_case_records(), cases)
    _write_rows(round177_score_profile_rows(), score_profiles)
    _write_rows(round177_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round177_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round177_price_field_rows(), paths["price_fields"])
    _write_rows(round177_base_score_weight_rows(), paths["base_score_weights"])
    _write_rows(round177_stage_cap_rows(), paths["stage_caps"])
    _write_rows(round177_score_stage_price_alignment_rows(), paths["score_stage_price_alignment"])
    paths["summary"].write_text(render_round177_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round177_green_guardrail_markdown(), encoding="utf-8")
    paths["risk_overlays"].write_text(render_round177_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round177_price_validation_plan_markdown(), encoding="utf-8")
    paths["score_stage_price_alignment_md"].write_text(render_round177_score_stage_price_alignment_markdown(), encoding="utf-8")
    return paths


def render_round177_summary_markdown() -> str:
    summary = round177_summary()
    lines = [
        "# Round-177 R6 Loop-11 Korea Financial / Capital / Digital Summary",
        "",
        f"- source_round: `{ROUND177_SOURCE_ROUND_PATH}`",
        "- large_sector: `FINANCIAL_CAPITAL_DIGITAL`",
        "- loop: `R6 Loop 11 / v11.0`",
        f"- target_count: {summary['target_count']}",
        f"- source_canonical_target_count: {summary['source_canonical_target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- base_score_component_count: {summary['base_score_component_count']}",
        f"- stage_cap_count: {summary['stage_cap_count']}",
        f"- score_stage_price_alignment_count: {summary['score_stage_price_alignment_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- cyclical_success_count: {summary['cyclical_success_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- failed_rerating_count: {summary['failed_rerating_count']}",
        f"- stage4b_case_count: {summary['stage4b_case_count']}",
        f"- stage4c_case_count: {summary['stage4c_case_count']}",
        f"- green_possible_count: {summary['green_possible_count']}",
        f"- watch_yellow_first_count: {summary['watch_yellow_first_count']}",
        f"- redteam_first_count: {summary['redteam_first_count']}",
        f"- hard_gate_target_count: {summary['hard_gate_target_count']}",
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "",
        "- R6 Loop 11 is Korea-first and treats low PBR, value-up, stablecoin, Toss IPO, Dunamu stake, and brokerage rally as routing evidence before capital-quality proof.",
        "- Stage 3-Green remains strict. ROE, CET1/K-ICS, credit cost, executed return, revenue model, disclosure confidence, and price path must line up.",
        "- The base score weights are ROE/EPS/FCF 22, capital return execution 18, capital ratio/credit cost 18, regulatory/revenue visibility 14, early price path 10, governance/disclosure 10, valuation/4B room 8.",
        "- Example: KB Financial can be a Stage 3 candidate, but CET1 and credit cost still cap Green.",
        "- Example: Naver-Dunamu can be Stage 2 equity-option evidence, but abnormal withdrawal makes it 4C-watch.",
        "- Example: Toss related stocks are Stage 1/2 options until direct equity, IPO filing, and stablecoin economics are verified.",
        "- Example: Seoul Guarantee shows why financial-service security incidents can block Green despite IPO and stable business narrative.",
    ]
    return "\n".join(lines) + "\n"


def render_round177_green_guardrail_markdown() -> str:
    lines = [
        "# Round-177 R6 Loop-11 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Loop-11 penalties |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND177_SCORE_TARGETS:
        lines.append(
            "| "
            f"`{target.target_id}` | {target.posture.value} | "
            f"{', '.join(target.green_conditions)} | {', '.join(target.loop11_penalty_axes)} |"
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not apply R6 Loop-11 v11.0 weights to production scoring yet.",
            "- Do not lower Stage 3-Green thresholds because a financial stock rerated.",
            "- Do not use Round 177 case records as candidate-generation input.",
            "- Do not treat low PBR, value-up policy, high dividend, Toss IPO, stablecoin, Dunamu stake, or brokerage volume as Green by itself.",
            "- Do not invent CET1, K-ICS, credit cost, PF exposure, buyback cancellation, dividends, stake value, security remediation, stage prices, or MFE/MAE.",
            "- Apply 4B-watch when PBR/price expands before individual return execution and credit quality are confirmed.",
            "- Apply 4C/hard review for PF credit-cost spike, capital-ratio deterioration, return cut, abnormal withdrawal, ransomware, IPO valuation cut, or stablecoin issuer-margin damage.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round177_risk_overlay_markdown() -> str:
    lines = [
        "# Round-177 R6 Loop-11 Risk Overlays",
        "",
        "- `LOW_PBR_NOT_GREEN`: low PBR and value-up policy route research, but do not prove rerating.",
        "- `CAPITAL_RATIO_CREDIT_GATE`: CET1, K-ICS, PF exposure, reserve build, and credit cost can block Green.",
        "- `RETURN_EXECUTION_REQUIRED`: actual cancellation, dividend, and repeat capital-return targets matter more than buyback headlines.",
        "- `VALUE_UP_CROWDED_4B`: financial-basket rerating can become 4B when PBR expands before execution.",
        "- `DIGITAL_ASSET_SECURITY_4C`: exchange abnormal withdrawal, hacking, or approval failure blocks digital-asset equity options.",
        "- `STABLECOIN_OPTION_NOT_REVENUE`: KRW stablecoin intent is not issuer revenue before approval, volume, reserve, redemption, and margin.",
        "- `FINTECH_RELATED_STOCK_CAP`: Toss-related stocks need direct ownership and revenue-model proof before Stage 3.",
        "- `FINANCIAL_DISCLOSURE_DETAIL_CAP`: OpenDART list or media headline is capped before details are normalized.",
        "",
        "Simple example: if `as_of_date=2025-11-27`, Naver-Dunamu deal terms can support Stage 2. The same-day Upbit abnormal withdrawal is a RedTeam input and cannot be ignored.",
    ]
    return "\n".join(lines) + "\n"


def render_round177_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-177 R6 Loop-11 Price Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign Stage 1/2/3/4B/4C dates from dated source evidence only.",
        "2. Backfill KRX daily bars for `price_at_stage1` through `price_at_stage4c`.",
        "3. Calculate 20D/60D/120D/252D returns and MFE/MAE after Stage 2.",
        "4. Compare price speed against ROE, net profit, CET1, K-ICS, credit cost, PF exposure, actual return, security, and regulation.",
        "5. Separate bank/insurance Green-capable cases from brokerage cycle, fintech option, stablecoin policy, security 4C, and disclosure caps.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | target | stage marker | check |",
        "| --- | --- | --- | --- |",
    ]
    for row in round177_case_candidate_rows():
        stage_date = row["stage4c_date"] or row["stage4b_date"] or row["stage3_date"] or row["stage2_date"] or row["stage1_date"] or "undated"
        lines.append(f"| `{row['case_id']}` | `{row['target_id']}` | {stage_date} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `valueup_leader_requires_capital_quality`: leader-frame rerating needs CET1 and credit-cost proof.",
            "- `nonbank_expansion_capital_gate`: M&A expansion is capped before capital-buffer proof.",
            "- `digital_asset_equity_option_security_gate`: exchange equity option is blocked by security events.",
            "- `brokerage_market_beta_not_green`: trading-value cycle is not structural Green by itself.",
            "- `valueup_crowding_4b_watch`: broad financial rally is cooled when price outruns execution.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round177_score_stage_price_alignment_markdown() -> str:
    lines = [
        "# Round-177 R6 Loop-11 Score -> Stage -> Price Alignment",
        "",
        "## Base Score Weights",
        "",
        "| component | points | direction | reason |",
        "| --- | ---: | --- | --- |",
    ]
    for row in ROUND177_BASE_SCORE_WEIGHTS:
        lines.append(f"| `{row.component}` | {row.points} | {row.loop11_direction} | {row.reason} |")
    lines.extend(
        [
            "",
            "## Stage Caps",
            "",
            "| stage band | max score | evidence | examples | Green policy |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for cap in ROUND177_STAGE_CAPS:
        lines.append(
            f"| `{cap.stage_band}` | {cap.max_score} | {', '.join(cap.required_evidence)} | "
            f"{', '.join(cap.example_cases)} | {cap.green_policy} |"
        )
    lines.extend(
        [
            "",
            "## Alignment Cases",
            "",
            "| case | detected stage | price-path status | verdict | adjustment |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in ROUND177_SCORE_STAGE_PRICE_ALIGNMENT:
        lines.append(
            f"| `{row.case_id}` | {row.detected_stage} | {row.price_path_status} | "
            f"{row.verdict} | {row.normalization_adjustment} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- KB/Shinhan/JB/insurance are the Green-capable tests: profit, capital, return, and credit quality must align.",
            "- Woori, KakaoBank, Toss, and Naver-Dunamu test Stage 2 option value with explicit caps.",
            "- Seoul Guarantee, PF credit, security incidents, and stablecoin regulation are hard RedTeam checks.",
            "- Brokerage and broad financial value-up rallies are useful Stage 2/4B signals, not automatic structural Green.",
        ]
    )
    return "\n".join(lines) + "\n"


def _round177_score_price_alignment(candidate: Round177CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "aligned"
    if candidate.case_type in {"success_candidate", "cyclical_success"}:
        return "unknown"
    if candidate.case_type in {"event_premium", "overheat", "4b_watch"}:
        return "price_moved_without_evidence"
    if candidate.case_type in {"4c_thesis_break", "failed_rerating"}:
        return "false_positive_score"
    return "unknown"


def _round177_rerating_result(candidate: Round177CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "true_rerating"
    if candidate.case_type == "cyclical_success":
        return "cyclical_rerating"
    if candidate.case_type == "4b_watch" or candidate.case_type == "overheat":
        return "theme_overheat"
    if candidate.case_type == "event_premium":
        return "event_premium"
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    if candidate.case_type == "failed_rerating":
        return "no_rerating"
    return "unknown"


def _numeric_weight(value: int | str) -> float:
    if isinstance(value, int):
        return float(value)
    if value in {"gate", "cap", "+", "event", "watch"}:
        return 0.0
    return float(value)


def _write_case_jsonl(records: Iterable[E2RCaseRecord], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(record.as_dict(), ensure_ascii=False, sort_keys=True) for record in records]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return path


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


__all__ = [
    "ROUND177_BASE_SCORE_WEIGHTS",
    "ROUND177_CASE_CANDIDATES",
    "ROUND177_DEFAULT_CASES_PATH",
    "ROUND177_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND177_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND177_PRICE_FIELDS",
    "ROUND177_SCORE_STAGE_PRICE_ALIGNMENT",
    "ROUND177_SCORE_TARGETS",
    "ROUND177_SOURCE_CANONICAL_TARGET_COUNT",
    "ROUND177_SOURCE_CANONICAL_TARGET_IDS",
    "ROUND177_STAGE_CAPS",
    "Round177BaseScoreWeight",
    "Round177CaseCandidate",
    "Round177ScoreStagePriceAlignment",
    "Round177ScoreTarget",
    "Round177ScoreWeightDraft",
    "Round177StageCap",
    "render_round177_green_guardrail_markdown",
    "render_round177_price_validation_plan_markdown",
    "render_round177_risk_overlay_markdown",
    "render_round177_score_stage_price_alignment_markdown",
    "render_round177_summary_markdown",
    "round177_base_score_weight_rows",
    "round177_case_candidate_rows",
    "round177_case_records",
    "round177_price_field_rows",
    "round177_score_profile_rows",
    "round177_score_stage_price_alignment_rows",
    "round177_stage_cap_rows",
    "round177_stage_date_rows",
    "round177_summary",
    "round177_target_for",
    "write_round177_r6_loop11_reports",
]
