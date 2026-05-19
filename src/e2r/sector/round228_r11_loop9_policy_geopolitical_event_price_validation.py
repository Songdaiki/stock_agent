"""Round-228 R11 Loop-9 policy/geopolitical/event validation pack.

Round 228 converts ``docs/round/round_228.md`` into structured, calibration-only
case records. It does not change production scoring.

Easy example: Korea Gas can jump on an East Sea oil/gas headline. That is not
Stage 3-Green until drilling, commerciality, development economics, and revenue
conversion are visible as of the case date.
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


ROUND228_SOURCE_ROUND_PATH = "docs/round/round_228.md"
ROUND228_LARGE_SECTOR = Round10LargeSector.POLICY_GEOPOLITICAL_EVENT
ROUND228_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round228_r11_loop9_policy_geopolitical_event_price_validation"
ROUND228_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r11_loop9_round228.jsonl"
ROUND228_DEFAULT_AUDIT_PATH = "data/sector_taxonomy/round228_r11_loop9_policy_geopolitical_event_price_validation_audit.json"
ROUND228_DEFAULT_STAGE3_BIAS = "very_conservative"

ROUND228_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "GOVERNANCE_REFORM_VALUEUP_POLICY": E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN.value,
    "TAX_POLICY_MARKET_SHOCK": E2RArchetype.TAX_POLICY_MARKET_SHOCK_OVERLAY.value,
    "US_KOREA_TARIFF_TRADE_DEAL": E2RArchetype.INDUSTRIAL_POLICY_TARIFF_EVENT.value,
    "POLICY_INDUCED_CAPEX_TARIFF_HEDGE": E2RArchetype.STEEL_TARIFF_EVENT_KOREA.value,
    "SEMICONDUCTOR_POLICY_SUPPORT": E2RArchetype.MEMORY_SUPERCYCLE_AI_CAPEX.value,
    "FISCAL_STIMULUS_CONSUMPTION_EVENT": E2RArchetype.EVENT_PREMIUM.value,
    "ENERGY_SECURITY_LONG_TERM_OFFTAKE": E2RArchetype.ENERGY_SECURITY_POLICY_EVENT.value,
    "DOMESTIC_RESOURCE_DISCOVERY_EVENT": E2RArchetype.DOMESTIC_RESOURCE_DISCOVERY_EVENT.value,
    "MARKET_STRUCTURE_REFORM": E2RArchetype.MARKET_STRUCTURE_WATCH.value,
    "MACRO_FX_OUTFLOW_OVERLAY": E2RArchetype.POLICY_MARKET_SHOCK_OVERLAY.value,
    "PRICE_ONLY_RALLY": E2RArchetype.PRICE_ONLY_RALLY.value,
    "EVENT_PREMIUM": E2RArchetype.EVENT_PREMIUM.value,
}

ROUND228_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "policy_or_event_escalated_to_company_contract",
    "contract_amount_or_funded_budget_confirmed",
    "financing_or_fid_confirmed",
    "actual_order_or_procurement_award",
    "revenue_recognition_path_visible",
    "margin_or_eps_fcf_revision_visible",
    "repeat_demand_not_event_fade",
    "policy_reversal_and_macro_fx_risk_passed",
    "price_path_after_evidence",
)

ROUND228_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "policy_news_only",
    "mou_only",
    "geopolitical_headline_only",
    "resource_estimate_without_drilling",
    "fiscal_stimulus_without_revenue_conversion",
    "support_package_without_order",
    "energy_security_headline_only",
    "capex_for_tariff_without_funding",
    "tax_policy_surprise",
    "macro_fx_outflow_risk",
    "price_rally_before_commerciality",
)

ROUND228_STAGE4B_WATCH_TRIGGERS: tuple[str, ...] = (
    "same_day_policy_or_resource_spike",
    "policy_mou_resource_theme_basket_rally",
    "support_package_rally_before_order",
    "consumer_voucher_local_consumption_basket_rally",
    "resource_discovery_plus_20_to_30pct_before_commerciality",
    "trade_deal_or_valueup_basket_overheat",
)

ROUND228_HARD_4C_GATES: tuple[str, ...] = (
    "policy_reversal",
    "tax_policy_confidence_break",
    "drilling_failure",
    "commerciality_absent",
    "mou_failure",
    "budget_not_funded",
    "tariff_reescalation",
    "fx_outflow_shock",
    "funding_failure",
    "fid_delay",
    "project_cancellation",
    "policy_induced_capex_loss",
)

ROUND228_PRICE_VALIDATION_FIELDS: tuple[str, ...] = (
    "price_data_source",
    "full_ohlc_available",
    "reported_price_anchor",
    "reported_return_anchor",
    "market_index_anchor",
    "stage1_price",
    "stage2_price",
    "stage3_price",
    "stage4b_price",
    "stage4c_price",
    "mfe_1d",
    "mae_1d",
    "policy_amount_anchor",
    "contract_or_offtake_anchor",
    "macro_growth_or_fx_anchor",
    "resource_commerciality_anchor",
    "price_validation_status",
)


@dataclass(frozen=True)
class Round228ScoreAdjustment:
    axis: str
    points: int
    direction: str
    reason: str

    def as_row(self) -> dict[str, str]:
        return {"axis": self.axis, "points": str(self.points), "direction": self.direction, "reason": self.reason}


@dataclass(frozen=True)
class Round228ShadowWeightRow:
    archetype: E2RArchetype
    actual_contract_or_budget: int
    funded_policy: int
    policy_to_revenue_bridge: int
    shareholder_rights_reform: int
    long_term_offtake: int
    financing_or_fid: int
    macro_fx_risk: int
    event_penalty: int
    watch_4b_sensitivity: int
    hard_4c_sensitivity: int
    notes: str

    def as_row(self) -> dict[str, str]:
        return {
            "archetype": self.archetype.value,
            "actual_contract_or_budget": _signed(self.actual_contract_or_budget),
            "funded_policy": _signed(self.funded_policy),
            "policy_to_revenue_bridge": _signed(self.policy_to_revenue_bridge),
            "shareholder_rights_reform": _signed(self.shareholder_rights_reform),
            "long_term_offtake": _signed(self.long_term_offtake),
            "financing_or_fid": _signed(self.financing_or_fid),
            "macro_fx_risk": _signed(self.macro_fx_risk),
            "event_penalty": _signed(self.event_penalty),
            "4b_watch_sensitivity": _signed(self.watch_4b_sensitivity),
            "hard_4c_sensitivity": _signed(self.hard_4c_sensitivity),
            "notes": self.notes,
        }


@dataclass(frozen=True)
class Round228DeepSubArchetype:
    category: str
    primary_archetype: E2RArchetype
    terms: tuple[str, ...]

    def as_row(self) -> dict[str, str]:
        return {"category": self.category, "primary_archetype": self.primary_archetype.value, "terms": "|".join(self.terms)}


@dataclass(frozen=True)
class Round228CaseCandidate:
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
    stage1_price_anchor: float | None
    stage2_price_anchor: float | None
    stage3_price_anchor: float | None
    stage4b_price_anchor: float | None
    stage4c_price_anchor: float | None
    extra_price_metrics: Mapping[str, float | str | bool]
    score_price_alignment: str
    rerating_result: str
    stage_failure_type: str
    price_validation_status: str
    notes: str

    @property
    def large_sector(self) -> str:
        return ROUND228_LARGE_SECTOR.value

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND228_SCORE_ADJUSTMENTS: tuple[Round228ScoreAdjustment, ...] = (
    Round228ScoreAdjustment("actual_contract_or_budget", 5, "raise", "R11은 정책이 실제 계약·예산으로 승격될 때만 강하게 본다."),
    Round228ScoreAdjustment("funded_policy", 5, "raise", "지원책은 재원과 집행 경로가 있어야 Stage 2 이상으로 간다."),
    Round228ScoreAdjustment("policy_to_company_revenue_bridge", 5, "raise", "정책이 회사 매출·마진·EPS/FCF로 내려오는 연결고리가 필요하다."),
    Round228ScoreAdjustment("shareholder_rights_reform", 4, "raise", "상법·자사주 소각은 market-structure Stage 2 토양이다."),
    Round228ScoreAdjustment("treasury_share_cancellation_rule", 4, "raise", "자사주 소각 의무는 value-up 실행 가능성을 높인다."),
    Round228ScoreAdjustment("long_term_offtake", 5, "raise", "장기 offtake는 단순 정책 뉴스보다 강한 Stage 2 증거다."),
    Round228ScoreAdjustment("project_fid_or_financing", 4, "raise", "FID와 financing이 없으면 자원·에너지 이벤트는 Green이 아니다."),
    Round228ScoreAdjustment("macro_relief_with_margin_recovery", 4, "raise", "관세 relief는 회사 마진 회복으로 확인되어야 한다."),
    Round228ScoreAdjustment("policy_news_only", -5, "lower", "정책 뉴스만으로는 Stage 3-Green 금지다."),
    Round228ScoreAdjustment("resource_estimate_without_drilling", -5, "lower", "시추 전 자원 추정은 event premium이다."),
    Round228ScoreAdjustment("tax_policy_surprise", -5, "lower", "세제 surprise는 value-up confidence를 훼손할 수 있다."),
    Round228ScoreAdjustment("capex_for_tariff_without_funding", -5, "lower", "관세 hedge CAPEX도 funding과 ROI가 없으면 4C-watch다."),
    Round228ScoreAdjustment("macro_fx_outflow_risk", -4, "lower", "대규모 해외투자 pledge는 환율·자금유출 리스크를 만든다."),
    Round228ScoreAdjustment("stimulus_without_revenue_conversion", -4, "lower", "소비쿠폰은 매출·마진 전환 전까지 event premium이다."),
    Round228ScoreAdjustment("support_package_without_order", -4, "lower", "지원 package만 있고 주문·마진이 없으면 Green이 아니다."),
    Round228ScoreAdjustment("energy_security_headline_only", -4, "lower", "에너지 안보 headline은 offtake/FID/마진 전까지 제한한다."),
    Round228ScoreAdjustment("price_rally_before_commerciality", -5, "lower", "상업성 전 급등은 4B-watch다."),
)


ROUND228_SHADOW_WEIGHT_ROWS: tuple[Round228ShadowWeightRow, ...] = (
    Round228ShadowWeightRow(E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN, 3, 4, 3, 5, 0, 0, 1, -2, 4, 3, "Commercial Act reform is market-structure Stage 2, not company Green."),
    Round228ShadowWeightRow(E2RArchetype.TAX_POLICY_MARKET_SHOCK_OVERLAY, 0, 0, 0, 0, 0, 0, 3, -5, 3, 5, "Tax-policy surprise can break value-up confidence."),
    Round228ShadowWeightRow(E2RArchetype.INDUSTRIAL_POLICY_TARIFF_EVENT, 4, 4, 4, 0, 0, 3, 5, -3, 4, 4, "Tariff relief is Stage 2 but FX outflow and growth shock remain."),
    Round228ShadowWeightRow(E2RArchetype.STEEL_TARIFF_EVENT_KOREA, 2, 2, 3, 0, 0, 5, 3, -5, 4, 4, "Hyundai Steel shows CAPEX without funding/margin clarity can fail."),
    Round228ShadowWeightRow(E2RArchetype.MEMORY_SUPERCYCLE_AI_CAPEX, 3, 5, 4, 0, 0, 3, 1, -3, 4, 3, "Chip support is Stage 2; company orders, margins, and EPS are required."),
    Round228ShadowWeightRow(E2RArchetype.EVENT_PREMIUM, 2, 5, 3, 0, 0, 0, 2, -4, 5, 3, "Fiscal stimulus and vouchers are Stage 1/2 until retail sales and margins convert."),
    Round228ShadowWeightRow(E2RArchetype.ENERGY_SECURITY_POLICY_EVENT, 5, 3, 5, 0, 5, 5, 2, -2, 3, 4, "POSCO Alaska LNG offtake is Stage 2; FID, margin, and cashflow are required."),
    Round228ShadowWeightRow(E2RArchetype.DOMESTIC_RESOURCE_DISCOVERY_EVENT, 0, 0, 0, 0, 0, 0, 2, -5, 5, 5, "Korea Gas +30% before drilling/commerciality is price_moved_without_evidence."),
)


ROUND228_DEEP_SUB_ARCHETYPES: tuple[Round228DeepSubArchetype, ...] = (
    Round228DeepSubArchetype("거버넌스 / 밸류업", E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN, ("Commercial Act amendment", "fiduciary duty to all shareholders", "treasury share cancellation", "Korea discount", "company-level payout execution")),
    Round228DeepSubArchetype("세제 / 시장충격", E2RArchetype.TAX_POLICY_MARKET_SHOCK_OVERLAY, ("capital gains tax threshold", "transaction tax", "policy confidence break", "market-level 4C-watch")),
    Round228DeepSubArchetype("관세 / 무역협상 / FX", E2RArchetype.INDUSTRIAL_POLICY_TARIFF_EVENT, ("25% tariff threat", "15% tariff deal", "$350B U.S. investment pledge", "FX outflow", "margin recovery")),
    Round228DeepSubArchetype("정책 유도 CAPEX", E2RArchetype.STEEL_TARIFF_EVENT_KOREA, ("Hyundai Steel U.S. plant", "tariff hedge", "funding uncertainty", "CAPEX without ROI")),
    Round228DeepSubArchetype("반도체 정책지원", E2RArchetype.MEMORY_SUPERCYCLE_AI_CAPEX, ("33T won chip support", "financial assistance", "Samsung Electronics", "SK Hynix", "orders and margin required")),
    Round228DeepSubArchetype("재정·소비 부양", E2RArchetype.EVENT_PREMIUM, ("supplementary budget", "consumer vouchers", "same-store sales", "margin conversion")),
    Round228DeepSubArchetype("에너지 안보 / 장기 offtake", E2RArchetype.ENERGY_SECURITY_POLICY_EVENT, ("POSCO International Alaska LNG", "20-year offtake", "FID", "pipeline steel", "cashflow economics")),
    Round228DeepSubArchetype("자원 발견 이벤트", E2RArchetype.DOMESTIC_RESOURCE_DISCOVERY_EVENT, ("East Sea oil and gas", "Korea Gas", "drilling success rate", "commerciality unknown", "price moved before evidence")),
)


ROUND228_CASE_CANDIDATES: tuple[Round228CaseCandidate, ...] = (
    Round228CaseCandidate(
        case_id="r11_loop9_commercial_act_valueup_reform",
        symbol="KOSPI/valueup_basket",
        company_name="Commercial Act / 밸류업 거버넌스 개혁",
        primary_archetype=E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN,
        secondary_archetypes=(E2RArchetype.MARKET_STRUCTURE_WATCH, E2RArchetype.EVENT_PREMIUM),
        case_type="success_candidate",
        stage1_date=date(2025, 7, 3),
        stage2_date=date(2025, 8, 25),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="market_structure_reform_is_stage2_until_company_level_cancellation_payout_roe_eps_and_fcf_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("commercial_act_revision", "fiduciary_duty_to_all_shareholders", "kospi_event_return_1_34pct", "treasury_share_cancellation_within_one_year"),
        red_flag_fields=("market_structure_reform_without_earnings", "company_level_payout_unverified", "roe_eps_unverified", "policy_reversal_watch"),
        price_data_source="Reuters/FT market-structure anchors",
        reported_price_anchor="KOSPI 3,116.27 close on 2025-07-03",
        reported_return_anchor="KOSPI +1.34%; newly acquired treasury shares must be cancelled within one year",
        mfe_1d=1.34,
        mae_1d=None,
        stage1_price_anchor=3116.27,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"kospi_close_2025_07_03": 3116.27, "kospi_event_return_pct": 1.34, "treasury_share_cancellation_rule": "newly_acquired_treasury_shares_cancel_within_one_year", "ft_2026_kospi_context": "KOSPI topped 6000 after 2025/2026 gains"},
        score_price_alignment="aligned",
        rerating_result="policy_event_rerating",
        stage_failure_type="stage2_watch_success",
        price_validation_status="market_structure_anchor_not_company_ohlc",
        notes="상법 개정은 market-structure Stage 2 토양이다. 회사별 Green은 실제 소각·배당·ROE/EPS 확인 후다.",
    ),
    Round228CaseCandidate(
        case_id="r11_loop9_tax_policy_market_shock",
        symbol="KOSPI/tax_sensitive_basket",
        company_name="세제안 shock",
        primary_archetype=E2RArchetype.TAX_POLICY_MARKET_SHOCK_OVERLAY,
        secondary_archetypes=(E2RArchetype.POLICY_MARKET_SHOCK_EVENT,),
        case_type="failed_rerating",
        stage1_date=date(2025, 8, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 8, 1),
        stage3_decision="tax_policy_surprise_is_redteam_macro_watch_not_positive_stage_evidence",
        stage4b_status="not_applicable",
        hard_4c_confirmed=False,
        evidence_fields=("capital_gains_tax_threshold_reduction_proposal", "corporate_dividend_transaction_tax_increase_proposal", "kospi_event_mae_minus_3_9pct"),
        red_flag_fields=("tax_policy_surprise", "policy_confidence_break", "market_structure_reversal_watch", "dividend_tax_increase_watch"),
        price_data_source="MarketWatch reported market-return and tax-policy anchor",
        reported_price_anchor="KOSPI -3.9% on tax-policy proposal shock",
        reported_return_anchor="CGT threshold 5B to 1B KRW; transaction tax 15bp to 20bp",
        mfe_1d=None,
        mae_1d=-3.9,
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"kospi_event_mae_pct": -3.9, "capital_gains_threshold_before_krw_bn": 5.0, "capital_gains_threshold_after_krw_bn": 1.0, "threshold_reduction_pct": -80.0, "transaction_tax_before_bp": 15.0, "transaction_tax_after_bp": 20.0, "transaction_tax_increase_pct": 33.3, "petition_signatures": 42000.0, "petition_review_threshold": 50000.0},
        score_price_alignment="false_positive_score",
        rerating_result="no_rerating",
        stage_failure_type="should_have_been_red",
        price_validation_status="reported_market_anchor_not_company_ohlc",
        notes="세제 surprise는 value-up momentum의 반대편에 있는 policy-confidence 4C-watch다.",
    ),
    Round228CaseCandidate(
        case_id="r11_loop9_us_korea_trade_tariff_fx_watch",
        symbol="auto_steel_shipbuilding_exporters",
        company_name="한미 tariff / $350B deal",
        primary_archetype=E2RArchetype.INDUSTRIAL_POLICY_TARIFF_EVENT,
        secondary_archetypes=(E2RArchetype.AUTO_TARIFF_LOCALIZATION, E2RArchetype.STEEL_TARIFF_EVENT_KOREA, E2RArchetype.POLICY_MARKET_SHOCK_OVERLAY),
        case_type="success_candidate",
        stage1_date=date(2025, 4, 1),
        stage2_date=date(2025, 10, 29),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 12, 1),
        stage3_decision="tariff_relief_is_macro_stage2_until_company_margin_recovery_fcf_order_and_eps_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("tariff_25_to_15pct", "semiconductor_pharma_tariffs_capped_15pct", "us_investment_pledge_350bn_usd", "won_reaction_plus_0_54pct"),
        red_flag_fields=("macro_fx_outflow_risk", "bok_growth_hit_2025_2026", "average_tariff_still_15pct_vs_prior_fta_zero", "company_margin_recovery_unverified"),
        price_data_source="Reuters/FT macro-trade anchors",
        reported_price_anchor="Company-specific OHLC unavailable; won +0.54% on deal headline",
        reported_return_anchor="Tariff 25% to 15%; BOK growth hit -0.45pp in 2025 and -0.60pp in 2026",
        mfe_1d=0.54,
        mae_1d=None,
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"tariff_before_pct": 25.0, "tariff_after_pct": 15.0, "tariff_reduction_pct": -40.0, "average_tariff_vs_prior_fta_pct": 15.0, "bok_growth_hit_2025_pp": -0.45, "bok_growth_hit_2026_pp": -0.60, "us_investment_pledge_usd_bn": 350.0, "annual_dollar_outflow_limit_usd_bn": 20.0, "foreign_exchange_bond_cap_2026_usd_bn": 5.0, "foreign_exchange_bond_cap_2025_usd_bn": 3.5, "bond_cap_increase_pct": 42.9, "won_reaction_pct": 0.54},
        score_price_alignment="aligned",
        rerating_result="policy_event_rerating",
        stage_failure_type="stage2_watch_success",
        price_validation_status="macro_anchor_not_company_ohlc",
        notes="관세 relief는 Stage 2지만, 회사별 마진 회복·FCF·EPS와 $350B FX outflow watch를 같이 확인해야 한다.",
    ),
    Round228CaseCandidate(
        case_id="r11_loop9_hyundai_steel_us_capex_tariff_strategy_fail",
        symbol="004020",
        company_name="현대제철",
        primary_archetype=E2RArchetype.STEEL_TARIFF_EVENT_KOREA,
        secondary_archetypes=(E2RArchetype.PROJECT_DELAY_CAPEX_OVERLAY, E2RArchetype.STEEL_EXPORT_TARIFF_4C),
        case_type="failed_rerating",
        stage1_date=date(2025, 3, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 4, 22),
        stage3_decision="tariff_hedge_capex_without_funding_margin_and_roi_clarity_is_4c_watch",
        stage4b_status="not_applicable",
        hard_4c_confirmed=False,
        evidence_fields=("us_steel_plant_6bn_usd", "hyundai_motor_group_us_package_21bn_usd", "reported_share_drop_above_21pct"),
        red_flag_fields=("capex_for_tariff_without_funding", "funding_plan_unclear", "domestic_demand_weakness", "chinese_imports", "labor_dispute_watch"),
        price_data_source="Reuters policy-induced capex / market-reaction anchor",
        reported_price_anchor="Hyundai Steel shares dropped more than 21% after U.S. plant announcement",
        reported_return_anchor="$6B U.S. steel plant; half via borrowing and possible POSCO equity input",
        mfe_1d=None,
        mae_1d=-21.0,
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"us_plant_investment_usd_bn": 6.0, "hyundai_motor_group_us_package_usd_bn": 21.0, "reported_share_drop_after_announcement_pct": -21.0, "funding_plan": "half_borrowing_possible_posco_equity", "policy_goal": "tariff_mitigation"},
        score_price_alignment="evidence_good_but_price_failed",
        rerating_result="no_rerating",
        stage_failure_type="should_have_been_red",
        price_validation_status="reported_event_return_not_full_ohlc",
        notes="관세 hedge CAPEX처럼 보였지만 funding·마진·ROI 불확실성 때문에 4C-watch로 둔다.",
    ),
    Round228CaseCandidate(
        case_id="r11_loop9_semiconductor_support_package",
        symbol="005930/000660/semiconductor_basket",
        company_name="반도체 33조 지원 package",
        primary_archetype=E2RArchetype.MEMORY_SUPERCYCLE_AI_CAPEX,
        secondary_archetypes=(E2RArchetype.SEMI_EQUIPMENT_CAPEX, E2RArchetype.INDUSTRIAL_POLICY_TARIFF_EVENT),
        case_type="success_candidate",
        stage1_date=date(2025, 4, 15),
        stage2_date=date(2025, 4, 15),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="semiconductor_policy_support_is_stage2_until_company_orders_margin_eps_fcf_and_price_path_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("support_package_26_to_33tn_krw", "financial_assistance_17_to_20tn_krw", "semiconductor_exports_141_9bn_usd", "semiconductor_exports_share_21pct"),
        red_flag_fields=("support_package_without_order", "company_level_order_unverified", "margin_eps_fcf_unverified", "export_control_china_competition_watch"),
        price_data_source="Reuters policy-support anchor",
        reported_price_anchor="Company-specific OHLC unavailable",
        reported_return_anchor="Support package 26T to 33T KRW; finance 17T to 20T KRW",
        mfe_1d=None,
        mae_1d=None,
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"support_package_before_krw_trn": 26.0, "support_package_after_krw_trn": 33.0, "support_package_increase_pct": 26.9, "financial_assistance_before_krw_trn": 17.0, "financial_assistance_after_krw_trn": 20.0, "financial_assistance_increase_pct": 17.6, "semiconductor_export_value_2024_usd_bn": 141.9, "semiconductor_share_exports_2024_pct": 21.0},
        score_price_alignment="unknown",
        rerating_result="policy_event_rerating",
        stage_failure_type="stage2_watch_success",
        price_validation_status="policy_anchor_company_ohlc_unavailable",
        notes="반도체 지원은 Stage 2 policy support다. 개별 기업 Green은 주문·마진·EPS/FCF 확인 후다.",
    ),
    Round228CaseCandidate(
        case_id="r11_loop9_fiscal_stimulus_voucher_event",
        symbol="domestic_consumption_basket",
        company_name="30.5조 추경·소비쿠폰",
        primary_archetype=E2RArchetype.EVENT_PREMIUM,
        secondary_archetypes=(E2RArchetype.POLICY_LOCAL_SERVICE_THEME, E2RArchetype.RETAIL_DOMESTIC_CONSUMER),
        case_type="event_premium",
        stage1_date=date(2025, 6, 19),
        stage2_date=date(2025, 7, 7),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="fiscal_stimulus_is_stage1_or_stage2_until_same_store_sales_margin_credit_and_fcf_conversion_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("supplementary_budget_30_5tn_krw", "approved_stimulus_31_8tn_krw", "voucher_program_10_3tn_krw", "voucher_150k_to_500k_krw"),
        red_flag_fields=("fiscal_stimulus_without_revenue_conversion", "one_off_consumption_watch", "fiscal_deficit_watch", "inflation_pressure_watch"),
        price_data_source="Reuters/WSJ fiscal-policy anchors",
        reported_price_anchor="Sector stock data unavailable after deep search",
        reported_return_anchor="31.8T KRW approved stimulus; 150k to 500k KRW vouchers",
        mfe_1d=None,
        mae_1d=None,
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"supplementary_budget_initial_krw_trn": 30.5, "approved_stimulus_krw_trn": 31.8, "increase_vs_initial_pct": 4.3, "growth_spending_krw_trn": 20.2, "tax_shortfall_makeup_krw_trn": 10.3, "voucher_program_krw_trn": 10.3, "voucher_amount_krw": "150000-500000", "most_people_voucher_krw": 250000.0, "eligible_recipients_mn": 51.0, "share_receiving_250k_pct": 84.0, "treasury_bond_financing_krw_trn": 19.8, "fiscal_deficit_gdp_pct": 4.2, "government_debt_gdp_pct": "49.0-49.1"},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="false_yellow",
        price_validation_status="policy_anchor_sector_ohlc_unavailable",
        notes="소비쿠폰·추경은 domestic-demand event다. 실제 same-store sales와 margin 전에는 소비주 Green 금지다.",
    ),
    Round228CaseCandidate(
        case_id="r11_loop9_posco_international_alaska_lng_offtake",
        symbol="047050",
        company_name="POSCO International",
        primary_archetype=E2RArchetype.ENERGY_SECURITY_POLICY_EVENT,
        secondary_archetypes=(E2RArchetype.GENERAL_TRADING_RESOURCE_INFRA,),
        case_type="success_candidate",
        stage1_date=date(2025, 9, 1),
        stage2_date=date(2025, 12, 4),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="long_term_lng_offtake_is_stage2_until_fid_pricing_margin_steel_supply_economics_and_cashflow_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("alaska_lng_20_year_offtake", "lng_supply_1mtpa", "total_contract_volume_20mt", "pipeline_807_miles", "pipeline_steel_supply"),
        red_flag_fields=("fid_not_confirmed", "lng_price_margin_unverified", "pipeline_permitting_watch", "project_cost_overrun_watch", "offtake_margin_failure_watch"),
        price_data_source="Reuters LNG offtake/project anchor",
        reported_price_anchor="POSCO International event-day OHLC unavailable after deep search",
        reported_return_anchor="1 mtpa LNG for 20 years; 807-mile pipeline steel supply opportunity",
        mfe_1d=None,
        mae_1d=None,
        stage1_price_anchor=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"lng_supply_volume_mtpa": 1.0, "contract_duration_years": 20.0, "total_contract_volume_mt": 20.0, "pipeline_length_miles": 807.0, "preliminary_commitments_secured_mtpa": 11.0, "fid_status": "not_yet_planned_before_year_end"},
        score_price_alignment="aligned",
        rerating_result="policy_event_rerating",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="실제 장기 LNG offtake는 단순 정책보다 강한 Stage 2다. FID·pricing·margin·cashflow 전에는 Stage 3가 아니다.",
    ),
    Round228CaseCandidate(
        case_id="r11_loop9_kogas_east_sea_resource_event",
        symbol="036460",
        company_name="한국가스공사 / 동해 석유·가스",
        primary_archetype=E2RArchetype.DOMESTIC_RESOURCE_DISCOVERY_EVENT,
        secondary_archetypes=(E2RArchetype.PRICE_ONLY_RALLY, E2RArchetype.RESOURCE_EXPLORATION_DRILL_BIT_GATE),
        case_type="event_premium",
        stage1_date=date(2024, 6, 3),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=date(2024, 6, 3),
        stage4c_date=None,
        stage3_decision="resource_estimate_and_drilling_approval_are_stage1_until_drilling_commerciality_and_revenue_conversion",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("east_sea_oil_gas_exploration_approval", "kogas_event_peak_38700_krw", "kogas_event_mfe_30pct", "resource_possibility_14bn_barrels", "success_rate_20pct"),
        red_flag_fields=("resource_estimate_without_drilling", "commerciality_absent", "price_rally_before_commerciality", "drilling_cost_burden", "commercial_production_target_2035_if_successful"),
        price_data_source="Reuters/WSJ price and exploration anchors",
        reported_price_anchor="Korea Gas 38,700 KRW and +30% event move",
        reported_return_anchor="Daesung Energy +30%, SK Innovation +6%, SK Gas +7%; success rate about 20%",
        mfe_1d=30.0,
        mae_1d=None,
        stage1_price_anchor=38700.0,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=38700.0,
        stage4c_price_anchor=None,
        extra_price_metrics={"kogas_event_peak_price": 38700.0, "kogas_event_mfe_1d_pct": 30.0, "implied_pre_event_reference_price": 29769.0, "daesung_energy_event_mfe_pct": 30.0, "sk_innovation_event_mfe_pct": 6.0, "sk_gas_event_mfe_pct": 7.0, "resource_possibility_bbl_bn": 14.0, "success_rate_pct": 20.0, "failure_probability_pct": 80.0, "drilling_cost_per_well_krw_bn": 100.0, "possible_wells": 10.0, "possible_total_drilling_cost_krw_trn": 1.0, "commercial_production_target_year": 2035.0},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="false_yellow",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="자원 추정과 탐사 승인 전 +30%는 대표적인 price_moved_without_evidence다. 상업성 전에는 Green이 아니다.",
    ),
)


def round228_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND228_CASE_CANDIDATES:
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
                "Round228 R11 Loop-9 policy/geopolitical/event price validation case. "
                "Calibration-only; not production scoring input."
            ),
            stage1_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "policy" in field
                or "event" in field
                or "approval" in field
                or "revision" in field
                or "support" in field
                or "tariff" in field
            ),
            stage2_evidence=candidate.evidence_fields if candidate.stage2_date else (),
            stage3_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "contract" in field
                or "offtake" in field
                or "fid" in field
                or "margin" in field
                or "eps" in field
                or "cashflow" in field
            ),
            stage4b_evidence=tuple(
                field
                for field in (*candidate.evidence_fields, *candidate.red_flag_fields)
                if "price" in field or "mfe" in field or "rally" in field or "event" in field or "theme" in field
            ),
            stage4c_evidence=tuple(
                field
                for field in candidate.red_flag_fields
                if "shock" in field
                or "failure" in field
                or "watch" in field
                or "risk" in field
                or "absent" in field
                or "commerciality" in field
                or "funding" in field
                or "tax" in field
            ),
            must_have_fields=ROUND228_GREEN_REQUIRED_FIELDS,
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
            score_weight_hint={f"{item.axis}_delta": float(item.points) for item in ROUND228_SCORE_ADJUSTMENTS},
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "full_ohlc_complete_false",
                "r11_default_stage3_bias_very_conservative",
                "price_validation_partial_with_reported_price_anchors",
                "do_not_invent_price_or_stage_dates",
                "do_not_treat_policy_geopolitical_resource_or_stimulus_event_as_green_alone",
                *ROUND228_GREEN_REQUIRED_FIELDS,
                *ROUND228_GREEN_FORBIDDEN_PATTERNS,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(
                stage1_price=candidate.stage1_price_anchor,
                stage2_price=candidate.stage2_price_anchor,
                stage3_price=candidate.stage3_price_anchor,
                stage4b_price=candidate.stage4b_price_anchor,
                stage4c_price=candidate.stage4c_price_anchor,
                mfe_30d=candidate.mfe_1d,
                mae_30d=candidate.mae_1d,
                price_validation_status=candidate.price_validation_status,
            ),
            data_quality=CaseDataQuality(
                official_data_available=True,
                report_data_available=True,
                price_data_available=candidate.stage1_price_anchor is not None
                or candidate.stage2_price_anchor is not None
                or candidate.mfe_1d is not None
                or candidate.mae_1d is not None,
                stage_dates_confidence=0.8 if candidate.stage1_date or candidate.stage2_date or candidate.stage4c_date else 0.65,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round228_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND228_CASE_CANDIDATES:
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
                "stage1_price_anchor": _float_text(candidate.stage1_price_anchor),
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


def round228_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND228_SCORE_ADJUSTMENTS)


def round228_shadow_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(row.as_row() for row in ROUND228_SHADOW_WEIGHT_ROWS)


def round228_deep_sub_archetype_rows() -> tuple[dict[str, str], ...]:
    return tuple(row.as_row() for row in ROUND228_DEEP_SUB_ARCHETYPES)


def round228_price_validation_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round228_price_validation": "true"} for field in ROUND228_PRICE_VALIDATION_FIELDS)


def round228_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple({"round228_label": label, "canonical_archetype": canonical} for label, canonical in ROUND228_REQUIRED_TARGET_ALIASES.items())


def round228_summary() -> dict[str, int | bool | str]:
    cases = ROUND228_CASE_CANDIDATES
    return {
        "source_round": ROUND228_SOURCE_ROUND_PATH,
        "large_sector": ROUND228_LARGE_SECTOR.value,
        "case_candidate_count": len(cases),
        "success_candidate_count": sum(1 for case in cases if case.case_type == "success_candidate"),
        "event_premium_count": sum(1 for case in cases if case.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for case in cases if case.case_type == "failed_rerating"),
        "price_moved_without_evidence_count": sum(1 for case in cases if case.score_price_alignment == "price_moved_without_evidence"),
        "stage3_case_count": sum(1 for case in cases if case.stage3_date is not None),
        "stage4b_watch_count": sum(1 for case in cases if case.stage4b_status == "watch"),
        "hard_4c_case_count": sum(1 for case in cases if case.hard_4c_confirmed),
        "target_archetype_count": len(ROUND228_REQUIRED_TARGET_ALIASES),
        "deep_sub_archetype_count": len(ROUND228_DEEP_SUB_ARCHETYPES),
        "shadow_weight_row_count": len(ROUND228_SHADOW_WEIGHT_ROWS),
        "price_validation_completed": "partial_with_reported_price_anchors",
        "full_ohlc_complete": False,
        "r11_default_stage3_bias": ROUND228_DEFAULT_STAGE3_BIAS,
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
    }


def round228_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND228_SOURCE_ROUND_PATH,
        "large_sector": ROUND228_LARGE_SECTOR.value,
        "summary": round228_summary(),
        "target_aliases": dict(ROUND228_REQUIRED_TARGET_ALIASES),
        "green_required_fields": list(ROUND228_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND228_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_watch_triggers": list(ROUND228_STAGE4B_WATCH_TRIGGERS),
        "hard_4c_gates": list(ROUND228_HARD_4C_GATES),
        "deep_sub_archetypes": round228_deep_sub_archetype_rows(),
        "shadow_weights": round228_shadow_weight_rows(),
        "what_not_to_change": [
            "do_not_use_round228_cases_as_candidate_generation_input",
            "do_not_apply_shadow_weights_to_production_scoring_yet",
            "do_not_treat_policy_geopolitical_resource_stimulus_or_trade_deal_event_as_green",
            "do_not_invent_ohlc_or_stage_dates",
        ],
    }


def render_round228_summary_markdown() -> str:
    summary = round228_summary()
    lines = [
        "# Round 228 R11 Loop 9 Policy Geopolitical Event Price Validation",
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
        f"- price_moved_without_evidence: {summary['price_moved_without_evidence_count']}",
        f"- Stage 3 dated cases: {summary['stage3_case_count']}",
        f"- 4B-watch cases: {summary['stage4b_watch_count']}",
        f"- hard_4c_case_count: {summary['hard_4c_case_count']}",
        f"- deep_sub_archetype_count: {summary['deep_sub_archetype_count']}",
        f"- shadow_weight_row_count: {summary['shadow_weight_row_count']}",
        f"- r11_default_stage3_bias: {summary['r11_default_stage3_bias']}",
        f"- full_ohlc_complete: {str(summary['full_ohlc_complete']).lower()}",
        "",
        "## Case Matrix",
        "",
        "| case | company | type | stage2 | stage3 | 4B | 4C | alignment | note |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for case in ROUND228_CASE_CANDIDATES:
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
            "- R11 default is Stage 1/2 event premium, not Stage 3-Green.",
            "- Commercial Act reform is positive market-structure Stage 2, but company Green needs payout, ROE/EPS, and FCF.",
            "- Tax-policy shock and Hyundai Steel CAPEX uncertainty are 4C-watch examples.",
            "- Tariff relief and chip support are policy Stage 2 until company margin, order, and EPS/FCF confirm.",
            "- POSCO International Alaska LNG is stronger Stage 2 because it has long-term offtake, but FID and margin still gate Green.",
            "- Korea Gas East Sea is the clean price_moved_without_evidence example.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round228_green_gate_review_markdown() -> str:
    lines = [
        "# Round 228 R11 Green Gate Review",
        "",
        "Do not apply these weights to production scoring yet.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND228_GREEN_REQUIRED_FIELDS)
    lines.extend(["", "## Forbidden Patterns", ""])
    lines.extend(f"- {field}" for field in ROUND228_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(
        [
            "",
            "## Easy Example",
            "- `정책 발표 + 관련주 급등` is Stage 1/2 event premium.",
            "- `정책 + 실제 계약/예산 + financing/FID + 매출 인식 + EPS/FCF revision` is the bundle that can support deeper Stage review.",
            "- `자원 매장 가능성 + 상업성 전 +30%` is 4B-watch, not Green.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round228_stage4b_4c_review_markdown() -> str:
    lines = ["# Round 228 R11 4B/4C Review", "", "## 4B Watch Triggers", ""]
    lines.extend(f"- {field}" for field in ROUND228_STAGE4B_WATCH_TRIGGERS)
    lines.extend(["", "## Hard 4C Gates", ""])
    lines.extend(f"- {field}" for field in ROUND228_HARD_4C_GATES)
    lines.extend(
        [
            "",
            "## Plain-Language Gate Notes",
            "",
            "- Policy news is not Stage 3 until contract, budget, financing, revenue, and EPS/FCF evidence appear.",
            "- Tax surprise and FX outflow pressure are macro 4C-watch inputs.",
            "- Resource discovery needs drilling and commerciality before any Green review.",
        ]
    )
    lines.extend(["", "## Case Notes", ""])
    for case in ROUND228_CASE_CANDIDATES:
        if case.stage4b_status == "watch" or case.red_flag_fields:
            lines.append(f"- {case.case_id}: {', '.join(case.red_flag_fields)}")
    return "\n".join(lines) + "\n"


def render_round228_price_validation_plan_markdown() -> str:
    lines = [
        "# Round 228 R11 Price Validation Plan",
        "",
        "- price_validation_completed: partial_with_reported_price_anchors",
        "- full_ohlc_complete: false",
        "- r11_default_stage3_bias: very_conservative",
        "- Do not invent OHLC, peak, MFE, or MAE where raw adjusted daily prices are unavailable.",
        "",
        "## Backfill Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND228_PRICE_VALIDATION_FIELDS)
    return "\n".join(lines) + "\n"


def write_round228_r11_loop9_reports(
    output_directory: str | Path = ROUND228_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND228_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND228_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "cases": write_case_library(round228_case_records(), cases_path),
        "audit": _write_json(round228_audit_payload(), audit_path),
        "summary": output / "round228_r11_loop9_price_validation_summary.md",
        "case_matrix": output / "round228_r11_loop9_case_matrix.csv",
        "target_aliases": output / "round228_r11_loop9_target_aliases.csv",
        "score_adjustments": output / "round228_r11_loop9_score_adjustments.csv",
        "shadow_weights": output / "round228_r11_loop9_shadow_weights.csv",
        "deep_sub_archetypes": output / "round228_r11_loop9_deep_sub_archetypes.csv",
        "price_validation_fields": output / "round228_r11_loop9_price_validation_fields.csv",
        "green_gate_review": output / "round228_r11_loop9_green_gate_review.md",
        "price_validation_plan": output / "round228_r11_loop9_price_validation_plan.md",
        "stage4b_4c_review": output / "round228_r11_loop9_stage4b_4c_review.md",
    }
    paths["summary"].write_text(render_round228_summary_markdown(), encoding="utf-8")
    _write_csv(round228_case_rows(), paths["case_matrix"])
    _write_csv(round228_target_alias_rows(), paths["target_aliases"])
    _write_csv(round228_score_adjustment_rows(), paths["score_adjustments"])
    _write_csv(round228_shadow_weight_rows(), paths["shadow_weights"])
    _write_csv(round228_deep_sub_archetype_rows(), paths["deep_sub_archetypes"])
    _write_csv(round228_price_validation_field_rows(), paths["price_validation_fields"])
    paths["green_gate_review"].write_text(render_round228_green_gate_review_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round228_price_validation_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round228_stage4b_4c_review_markdown(), encoding="utf-8")
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
