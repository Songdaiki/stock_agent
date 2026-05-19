"""Round-226 R9 Loop-9 mobility/transport/leisure price validation pack.

Round 226 is calibration/evaluation material only. It converts
``docs/round/round_226.md`` into structured case records, shadow weights, and
guardrail reports.

Easy example: a China visa-free headline can lift duty-free/casino stocks on
the event day. It is not Stage 3-Green until tourist spend, casino drop/hold,
OPM, and FCF are visible as of the case date.
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


ROUND226_SOURCE_ROUND_PATH = "docs/round/round_226.md"
ROUND226_LARGE_SECTOR = Round10LargeSector.MOBILITY_TRANSPORT_LEISURE
ROUND226_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round226_r9_loop9_mobility_transport_leisure_price_validation"
ROUND226_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r9_loop9_round226.jsonl"
ROUND226_DEFAULT_AUDIT_PATH = "data/sector_taxonomy/round226_r9_loop9_mobility_transport_leisure_price_validation_audit.json"

ROUND226_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "AUTO_HYBRID_VALUEUP": E2RArchetype.AUTO_HYBRID_VALUEUP.value,
    "AUTO_TARIFF_MARGIN_4C_WATCH": E2RArchetype.AUTO_TARIFF_LOCALIZATION.value,
    "AUTO_SDV_DELAY_CAPEX_OVERLAY": E2RArchetype.AUTO_SDV_DELAY_CAPEX_OVERLAY.value,
    "AUTO_PARTS_THERMAL_MANAGEMENT_MNA": E2RArchetype.AUTO_MOBILITY_COMPONENTS.value,
    "LOGISTICS_ECOMMERCE_CONTRACT": E2RArchetype.ECOMMERCE_LOGISTICS_REPEAT_CONTRACT.value,
    "AIRLINE_INTEGRATION_SCALE": E2RArchetype.AIRLINE_INTEGRATION_SCALE.value,
    "AIRLINE_CAPEX_DEBT_WATCH": E2RArchetype.AIRLINE_TRAVEL_CYCLE.value,
    "AIRLINE_SAFETY_OPERATIONAL_TRUST_4C": E2RArchetype.AIRLINE_SAFETY_REGULATORY_OVERLAY.value,
    "SHIPPING_FREIGHT_CYCLE": E2RArchetype.SHIPPING_FREIGHT_CYCLE.value,
    "TOURISM_DUTYFREE_CASINO_EVENT": E2RArchetype.CASINO_DUTYFREE_TOURISM_POLICY_KOREA.value,
    "TRAVEL_REDIRECT_EVENT_PREMIUM": E2RArchetype.TOURISM_POLICY_EVENT.value,
    "PRICE_ONLY_RALLY": E2RArchetype.PRICE_ONLY_RALLY.value,
    "EVENT_PREMIUM": E2RArchetype.EVENT_PREMIUM.value,
}

ROUND226_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "unit_economics",
    "fcf_after_capex",
    "margin_durability",
    "hybrid_mix_or_load_factor_or_freight_contract_or_tourist_spend",
    "shareholder_return_or_deleveraging",
    "safety_and_operational_trust_passed",
    "tariff_fuel_fx_freight_normalization_stress_passed",
    "price_path_after_evidence",
)

ROUND226_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "travel_reopening_only",
    "freight_rate_spike_only",
    "robotaxi_or_sdv_story_only",
    "tourist_arrival_policy_only",
    "tourism_redirect_event_only",
    "merger_completion_without_synergy",
    "ev_or_ai_mobility_theme_only",
    "capex_heavy_localization_without_margin",
    "fatal_safety_accident",
    "margin_guidance_cut",
)

ROUND226_STAGE4B_WATCH_TRIGGERS: tuple[str, ...] = (
    "hybrid_valueup_fast_rerating",
    "sdv_ai_mobility_before_software_revenue",
    "airline_merger_completion_price_spike",
    "aircraft_order_growth_ignores_capex_debt",
    "red_sea_freight_rate_spike",
    "tourism_policy_day_basket_rally",
    "china_japan_redirect_before_actual_spend",
)

ROUND226_HARD_4C_GATES: tuple[str, ...] = (
    "fatal_safety_accident",
    "operational_trust_break",
    "margin_guidance_cut_with_structural_cause",
    "tariff_shock_not_offset_by_localization",
    "fuel_cost_spike_not_passed_through",
    "freight_rate_collapse",
    "container_overcapacity",
    "integration_failure",
    "regulatory_block",
    "tourist_spend_failure",
    "casino_utilization_collapse",
    "debt_or_capex_burden",
)

ROUND226_PRICE_VALIDATION_FIELDS: tuple[str, ...] = (
    "price_data_source",
    "full_ohlc_available",
    "reported_price_anchor",
    "reported_return_anchor",
    "stage1_price",
    "stage2_price",
    "stage3_price",
    "stage4b_price",
    "stage4c_price",
    "mfe_1d",
    "mae_1d",
    "mfe_event",
    "mae_event",
    "relative_underperformance_pp",
    "operating_metric_anchor",
    "capex_or_debt_anchor",
    "cycle_or_policy_anchor",
    "price_validation_status",
)


@dataclass(frozen=True)
class Round226ScoreAdjustment:
    axis: str
    points: int
    direction: str
    reason: str

    def as_row(self) -> dict[str, str]:
        return {"axis": self.axis, "points": str(self.points), "direction": self.direction, "reason": self.reason}


@dataclass(frozen=True)
class Round226ShadowWeightRow:
    archetype: E2RArchetype
    unit_economics: int
    fcf_after_capex: int
    hybrid_mix: int
    shareholder_return: int
    margin_durability: int
    localization_hedge: int
    logistics_margin: int
    safety_trust: int
    event_penalty: int
    cycle_normalization_redteam: int
    watch_4b_sensitivity: int
    hard_4c_sensitivity: int
    notes: str

    def as_row(self) -> dict[str, str]:
        return {
            "archetype": self.archetype.value,
            "unit_economics": _signed(self.unit_economics),
            "fcf_after_capex": _signed(self.fcf_after_capex),
            "hybrid_mix": _signed(self.hybrid_mix),
            "shareholder_return": _signed(self.shareholder_return),
            "margin_durability": _signed(self.margin_durability),
            "localization_hedge": _signed(self.localization_hedge),
            "logistics_margin": _signed(self.logistics_margin),
            "safety_trust": _signed(self.safety_trust),
            "event_penalty": _signed(self.event_penalty),
            "cycle_normalization_redteam": _signed(self.cycle_normalization_redteam),
            "4b_watch_sensitivity": _signed(self.watch_4b_sensitivity),
            "hard_4c_sensitivity": _signed(self.hard_4c_sensitivity),
            "notes": self.notes,
        }


@dataclass(frozen=True)
class Round226CaseCandidate:
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
    extra_price_metrics: Mapping[str, float | str | bool]
    score_price_alignment: str
    rerating_result: str
    stage_failure_type: str
    price_validation_status: str
    notes: str

    @property
    def large_sector(self) -> str:
        return ROUND226_LARGE_SECTOR.value

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND226_SCORE_ADJUSTMENTS: tuple[Round226ScoreAdjustment, ...] = (
    Round226ScoreAdjustment("hybrid_mix", 5, "raise", "완성차는 EV 테마보다 hybrid mix가 실제 OPM/FCF로 이어지는지가 중요하다."),
    Round226ScoreAdjustment("fcf_after_capex", 5, "raise", "자동차·항공·물류는 capex 이후 FCF가 보여야 Stage 3 후보가 된다."),
    Round226ScoreAdjustment("shareholder_return_execution", 5, "raise", "value-up은 발표보다 buyback/dividend 실행이 핵심이다."),
    Round226ScoreAdjustment("operating_margin_durability", 5, "raise", "수요 회복보다 마진 지속성이 이익 체급 변화를 만든다."),
    Round226ScoreAdjustment("localization_tariff_hedge", 4, "raise", "관세 환경에서는 현지화가 마진 방어 evidence가 될 수 있다."),
    Round226ScoreAdjustment("unit_economics", 5, "raise", "모빌리티·여행·물류는 volume보다 단위 경제성이 우선이다."),
    Round226ScoreAdjustment("logistics_contract_margin", 4, "raise", "물류 계약은 매출 증가보다 margin과 automation efficiency를 본다."),
    Round226ScoreAdjustment("load_factor_with_yield", 4, "raise", "항공은 탑승률만이 아니라 yield와 같이 봐야 한다."),
    Round226ScoreAdjustment("integration_synergy_realized", 4, "raise", "항공 합병은 완료보다 실제 시너지와 비용 통제가 필요하다."),
    Round226ScoreAdjustment("freight_contract_mix", 4, "raise", "해운은 spot 급등보다 contract mix와 rate floor가 중요하다."),
    Round226ScoreAdjustment("tourist_spend_conversion", 5, "raise", "관광은 입국자 수보다 객단가와 소비 전환이 Stage 3 evidence다."),
    Round226ScoreAdjustment("casino_drop_and_hold", 5, "raise", "카지노/면세는 drop, hold, OPM으로 정책 이벤트를 검증해야 한다."),
    Round226ScoreAdjustment("safety_record_and_operational_trust", 5, "raise", "안전·운영 신뢰는 항공/여행 Green의 선결 조건이다."),
    Round226ScoreAdjustment("travel_reopening_only", -5, "lower", "여행 수요 회복만으로는 spend와 OPM을 알 수 없다."),
    Round226ScoreAdjustment("freight_rate_spike_only", -5, "lower", "운임 급등만으로는 구조적 E2R이 아니라 cycle일 수 있다."),
    Round226ScoreAdjustment("robotaxi_or_sdv_story_only", -5, "lower", "SDV/로보택시 스토리는 software revenue 전까지 watch다."),
    Round226ScoreAdjustment("tourist_arrival_policy_only", -5, "lower", "무비자 정책만으로는 면세/카지노 현금흐름을 알 수 없다."),
    Round226ScoreAdjustment("tourism_redirect_event_only", -5, "lower", "관광 redirect 기대 급등은 event premium이다."),
    Round226ScoreAdjustment("merger_completion_without_synergy", -4, "lower", "합병 완료만 있고 load factor/yield/FCF가 없으면 제한한다."),
    Round226ScoreAdjustment("ev_or_ai_mobility_theme_only", -4, "lower", "EV/AI mobility 테마만으로 Green을 만들 수 없다."),
    Round226ScoreAdjustment("capex_heavy_localization_without_margin", -4, "lower", "현지화 capex가 마진 방어로 확인되지 않으면 부담이다."),
    Round226ScoreAdjustment("safety_failure", -5, "lower", "fatal safety accident는 hard 4C gate다."),
    Round226ScoreAdjustment("tariff_margin_cut", -5, "lower", "관세 비용이 손익을 때리면 hybrid/value-up 논리를 제한한다."),
    Round226ScoreAdjustment("utilization_weak", -5, "lower", "항공/관광/물류는 낮은 utilization이 FCF를 훼손한다."),
    Round226ScoreAdjustment("cycle_normalization", -5, "lower", "운임·관광·항공 사이클 정상화는 4B/4C 감시 신호다."),
    Round226ScoreAdjustment("logistics_contract_without_margin", -3, "lower", "물류 계약만 있고 margin이 없으면 Stage 2 watch다."),
)


ROUND226_SHADOW_WEIGHT_ROWS: tuple[Round226ShadowWeightRow, ...] = (
    Round226ShadowWeightRow(E2RArchetype.AUTO_HYBRID_VALUEUP, 5, 5, 5, 5, 5, 4, 0, 3, -1, 2, 4, 4, "Hyundai supports Stage 3 candidate but tariff margin shock requires 4C-watch."),
    Round226ShadowWeightRow(E2RArchetype.AUTO_TARIFF_LOCALIZATION, 3, 5, 3, 2, 5, 5, 0, 2, -2, 5, 3, 5, "Tariff cost can override hybrid/value-up if margin durability fails."),
    Round226ShadowWeightRow(E2RArchetype.AUTO_SDV_DELAY_CAPEX_OVERLAY, 2, 3, 2, 1, 3, 2, 0, 3, -5, 4, 5, 4, "Kia SDV delay and capex hike block Green despite hybrid plan."),
    Round226ShadowWeightRow(E2RArchetype.ECOMMERCE_LOGISTICS_REPEAT_CONTRACT, 4, 5, 0, 1, 5, 0, 5, 2, -3, 3, 3, 3, "CJ Logistics contract needs margin, volume and FCF; price failed on event."),
    Round226ShadowWeightRow(E2RArchetype.AIRLINE_INTEGRATION_SCALE, 4, 5, 0, 2, 4, 0, 0, 5, -3, 3, 4, 4, "Korean Air merger is Stage 2 until synergy/load factor/yield/FCF confirm."),
    Round226ShadowWeightRow(E2RArchetype.AIRLINE_TRAVEL_CYCLE, 2, 5, 0, 1, 3, 0, 0, 4, -4, 4, 4, 4, "Large aircraft order is growth plus capex/debt watch."),
    Round226ShadowWeightRow(E2RArchetype.AIRLINE_SAFETY_REGULATORY_OVERLAY, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 5, 5, "Jeju Air fatal crash is hard 4C."),
    Round226ShadowWeightRow(E2RArchetype.SHIPPING_FREIGHT_CYCLE, 4, 5, 0, 2, 3, 0, 0, 2, -5, 5, 5, 4, "HMM/Red Sea freight is cyclical success, not structural Green."),
    Round226ShadowWeightRow(E2RArchetype.CASINO_DUTYFREE_TOURISM_POLICY_KOREA, 5, 5, 0, 1, 4, 0, 0, 3, -5, 4, 5, 4, "Visa-free tourism event needs spend/drop/hold/OPM before Green."),
    Round226ShadowWeightRow(E2RArchetype.TOURISM_POLICY_EVENT, 4, 4, 0, 1, 3, 0, 0, 3, -5, 4, 5, 4, "Lotte Tour redirect rally is event premium until utilization and cashflow confirm."),
)


ROUND226_CASE_CANDIDATES: tuple[Round226CaseCandidate, ...] = (
    Round226CaseCandidate(
        case_id="r9_loop9_hyundai_hybrid_valueup_tariff_watch",
        symbol="005380",
        company_name="현대차",
        primary_archetype=E2RArchetype.AUTO_HYBRID_VALUEUP,
        secondary_archetypes=(E2RArchetype.AUTO_TARIFF_LOCALIZATION, E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN),
        case_type="success_candidate",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2024, 8, 28),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 7, 31),
        stage3_decision="hybrid_valueup_is_stage3_candidate_only_if_mix_opm_fcf_and_buyback_execution_confirm_while_tariff_cost_is_4c_watch",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("investor_day_mfe_intraday_5_0pct", "investor_day_close_return_4_7pct", "2030_sales_target_5_55m", "2028_hybrid_target_1_33m", "buyback_plan_4tn_krw", "shareholder_return_35pct"),
        red_flag_fields=("tariff_event_hyundai_minus_4_5pct", "tariff_event_kia_minus_6_6pct", "tariff_cost_2025_4_1tn_krw", "q4_2025_net_profit_minus_52pct", "q4_2025_op_minus_40pct"),
        price_data_source="Reuters/WSJ reported event and financial anchors",
        reported_price_anchor="2024-08-28 Investor Day +5.0% intraday and +4.7% close",
        reported_return_anchor="2025 tariff event Hyundai -4.5%, Kia -6.6%; 2025 tariff cost 4.1T KRW",
        mfe_1d=5.0,
        mae_1d=-4.5,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"investor_day_mfe_intraday_pct": 5.0, "investor_day_close_return_pct": 4.7, "sales_target_2030_mn": 5.55, "sales_target_growth_pct": 30.0, "hybrid_sales_target_2028_mn": 1.33, "hybrid_target_increase_pct": 40.0, "buyback_plan_krw_tn": 4.0, "shareholder_return_pct": 35.0, "tariff_event_hyundai_mae_pct": -4.5, "tariff_event_kia_mae_pct": -6.6, "tariff_cost_2025_krw_tn": 4.1, "q4_2025_net_profit_decline_pct": -52.0, "q4_2025_operating_profit_decline_pct": -40.0, "q4_2025_revenue_growth_pct": 0.5},
        score_price_alignment="aligned",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="Hybrid/value-up supports Stage 3 candidate review, but tariff margin cost creates simultaneous 4C-watch.",
    ),
    Round226CaseCandidate(
        case_id="r9_loop9_kia_sdv_delay_capex_watch",
        symbol="000270",
        company_name="기아",
        primary_archetype=E2RArchetype.AUTO_SDV_DELAY_CAPEX_OVERLAY,
        secondary_archetypes=(E2RArchetype.AUTO_HYBRID_VALUEUP, E2RArchetype.AUTO_TARIFF_LOCALIZATION),
        case_type="failed_rerating",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2026, 4, 9),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2026, 4, 9),
        stage3_decision="hybrid_target_is_positive_but_sdv_delay_ev_target_cut_and_capex_hike_block_green",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("investment_plan_41_4tn_krw", "investment_plan_plus_30pct", "2030_hybrid_target_1_1m", "hybrid_target_plus_60pct", "2030_sales_target_4_13m"),
        red_flag_fields=("sdv_launch_delay_2027_to_2028", "ev_target_cut_20pct", "capex_burden", "software_revenue_unverified", "fcf_after_capex_unverified"),
        price_data_source="Reuters reported strategy and capex anchor",
        reported_price_anchor="Raw event-day OHLC unavailable after deep search",
        reported_return_anchor="SDV delay, capex +30%, EV target -20%, hybrid target +60%",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"investment_plan_krw_tn": 41.4, "investment_plan_usd_bn": 28.0, "investment_plan_increase_pct": 30.0, "implied_prior_investment_plan_krw_tn": 31.85, "ev_target_2030_mn": 1.0, "ev_target_cut_pct": 20.0, "sales_target_2030_mn": 4.13, "sales_2025_mn": 3.14, "sales_target_growth_pct": 31.5, "hybrid_target_2030_mn": 1.1, "hybrid_target_increase_pct": 60.0, "implied_prior_hybrid_target_mn": 0.6875},
        score_price_alignment="evidence_good_but_price_failed",
        rerating_result="no_rerating",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Hybrid expansion is useful, but SDV delay, EV target cut, and capex hike block Green before software revenue and FCF are visible.",
    ),
    Round226CaseCandidate(
        case_id="r9_loop9_cj_logistics_shinsegae_contract_price_failed",
        symbol="000120",
        company_name="CJ대한통운",
        primary_archetype=E2RArchetype.ECOMMERCE_LOGISTICS_REPEAT_CONTRACT,
        secondary_archetypes=(E2RArchetype.LOGISTICS_PARCEL_FREIGHT, E2RArchetype.RETAIL_ECOMMERCE_LOGISTICS),
        case_type="success_candidate",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2024, 4, 1),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="logistics_contract_is_stage2_until_parcel_volume_margin_automation_efficiency_overseas_recovery_and_fcf_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("shinsegae_three_year_logistics_partnership", "expected_annual_revenue_boost_300bn_krw", "target_price_116000_krw", "target_upside_17_1pct"),
        red_flag_fields=("stage2_event_mae_minus_0_2pct", "target_cut_minus_17pct", "domestic_growth_slowdown", "overseas_recovery_delay", "margin_unverified"),
        price_data_source="MarketWatch reported price, target, and revenue anchor",
        reported_price_anchor="99,100 KRW and -0.2% on reported event anchor",
        reported_return_anchor="Annual revenue boost 300B KRW expected; target cut 17% to 116,000 KRW",
        mfe_1d=None,
        mae_1d=-0.2,
        stage2_price_anchor=99100.0,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"stage2_price_anchor_krw": 99100.0, "stage2_event_mae_pct": -0.2, "expected_annual_revenue_boost_krw_bn": 300.0, "target_price_krw": 116000.0, "target_upside_pct": 17.1, "target_cut_pct": -17.0, "implied_prior_target_krw": 139759.0},
        score_price_alignment="evidence_good_but_price_failed",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="Logistics contract is Stage 2; margin, parcel volume, automation efficiency, overseas recovery, and FCF are required before Green.",
    ),
    Round226CaseCandidate(
        case_id="r9_loop9_korean_air_asiana_integration_capex_watch",
        symbol="003490",
        company_name="대한항공",
        primary_archetype=E2RArchetype.AIRLINE_INTEGRATION_SCALE,
        secondary_archetypes=(E2RArchetype.AIRLINE_TRAVEL_CYCLE, E2RArchetype.EVENT_PREMIUM),
        case_type="success_candidate",
        stage1_date=date(2020, 1, 1),
        stage2_date=date(2024, 12, 12),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="asiana_integration_is_stage2_until_synergy_load_factor_yield_debt_capex_burden_and_fcf_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("asiana_stake_63_88pct", "asiana_deal_value_1_3bn_usd", "international_capacity_rank_12th", "boeing_order_36_2bn_usd", "aircraft_order_count_103", "total_package_49_89bn_usd"),
        red_flag_fields=("capex_debt_burden", "integration_synergy_unverified", "load_factor_yield_unverified", "fcf_unverified", "fuel_cost_watch"),
        price_data_source="Reuters/AP transaction and aircraft-order anchors",
        reported_price_anchor="Korean Air event-day OHLC unavailable after deep search",
        reported_return_anchor="Asiana acquisition $1.3B; Boeing/GE package about $49.89B",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"asiana_stake_pct": 63.88, "asiana_deal_value_usd_bn": 1.3, "international_capacity_rank": 12.0, "boeing_order_value_usd_bn": 36.2, "aircraft_order_count": 103.0, "spare_engine_purchase_usd_mn": 690.0, "ge_engine_maintenance_contract_usd_bn": 13.0, "total_package_usd_bn": 49.89, "aircraft_order_vs_asiana_deal_multiple": 27.8, "total_package_vs_asiana_deal_multiple": 38.4},
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Merger scale is Stage 2; synergy, load factor, yield, FCF, and capex/debt burden determine promotion.",
    ),
    Round226CaseCandidate(
        case_id="r9_loop9_jeju_air_fatal_crash_hard_4c",
        symbol="089590",
        company_name="제주항공",
        primary_archetype=E2RArchetype.AIRLINE_SAFETY_REGULATORY_OVERLAY,
        secondary_archetypes=(E2RArchetype.AIRLINE_TRAVEL_CYCLE,),
        case_type="4c_thesis_break",
        stage1_date=date(2023, 1, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2024, 12, 30),
        stage3_decision="fatal_crash_is_hard_4c_and_blocks_any_travel_demand_green",
        stage4b_status="not_applicable",
        hard_4c_confirmed=True,
        evidence_fields=("fatal_crash", "fatalities_179", "jeju_air_event_mae_15_7pct", "market_cap_wipeout_95_7bn_krw", "tour_package_cancellations_doubled"),
        red_flag_fields=("fatal_safety_accident", "operational_trust_break", "consumer_trust_break", "booking_cancellations", "hard_4c"),
        price_data_source="Reuters reported event-return and travel-agency anchors",
        reported_price_anchor="Jeju Air intraday -15.7%; market cap wipeout up to 95.7B KRW",
        reported_return_anchor="Hanatour -7%, Very Good Tour -11%; package cancellations doubled and bookings halved for one operator",
        mfe_1d=None,
        mae_1d=-15.7,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"jeju_air_event_mae_1d_pct": -15.7, "market_cap_wipeout_krw_bn": 95.7, "korean_air_mae_pct": -1.3, "asiana_mae_pct": -0.8, "hanatour_mae_pct": -7.0, "very_good_tour_mae_pct": -11.0, "air_busan_mfe_pct": 15.0, "fatalities": 179.0, "tour_package_cancellations": "doubled_for_one_operator", "bookings": "halved_for_one_operator"},
        score_price_alignment="false_positive_score",
        rerating_result="thesis_break",
        stage_failure_type="should_have_been_red",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="Fatal crash is a hard 4C safety/trust break and blocks any reopening-demand Green.",
    ),
    Round226CaseCandidate(
        case_id="r9_loop9_hmm_red_sea_shipping_cycle",
        symbol="011200",
        company_name="HMM / container shipping cycle",
        primary_archetype=E2RArchetype.SHIPPING_FREIGHT_CYCLE,
        secondary_archetypes=(E2RArchetype.SHIPPING_FREIGHT_CYCLE_KOREA, E2RArchetype.COMMODITY_SPREAD),
        case_type="cyclical_success",
        stage1_date=date(2024, 5, 1),
        stage2_date=date(2024, 7, 3),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="red_sea_freight_spike_is_cyclical_success_until_hmm_contract_mix_rate_floor_fcf_and_capital_return_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("freightos_index_5068_usd", "freightos_6w_return_40pct", "capacity_tied_up_5_9pct", "maersk_profit_swing_2_521bn_usd", "maersk_shipping_rates_plus_38pct"),
        red_flag_fields=("freight_rate_spike_only", "route_normalization_watch", "overcapacity_watch", "contract_mix_unverified", "hmm_stock_ohlc_unavailable"),
        price_data_source="Reuters/WSJ freight-rate and proxy-company anchors",
        reported_price_anchor="HMM stock OHLC unavailable; Freightos +40% to $5,068 used as cycle anchor",
        reported_return_anchor="Maersk profit swing +$2.521B; shipping rates +38%; ocean freight revenue +49%",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"freightos_index_usd": 5068.0, "freightos_6w_return_pct": 40.0, "implied_prior_freightos_index_usd": 3620.0, "capacity_tied_up_pct": "5-9", "hapag_lloyd_proxy_return_pct": 7.0, "maersk_q4_2024_net_profit_usd_bn": 2.085, "maersk_q4_2023_net_loss_usd_bn": -0.436, "maersk_profit_swing_usd_bn": 2.521, "maersk_shipping_rate_increase_pct": 38.0, "maersk_ocean_freight_revenue_increase_pct": 49.0, "maersk_ebit_swing_usd_bn": 2.52},
        score_price_alignment="aligned",
        rerating_result="cyclical_rerating",
        stage_failure_type="stage2_watch_success",
        price_validation_status="hmm_stock_price_data_unavailable_after_deep_search",
        notes="Freight spike can be profitable but remains cyclical until contract mix, rate floor, FCF, and capital return confirm durability.",
    ),
    Round226CaseCandidate(
        case_id="r9_loop9_tourism_visa_free_retail_casino_event",
        symbol="008770/034230/069960",
        company_name="호텔신라/파라다이스/현대백화점",
        primary_archetype=E2RArchetype.CASINO_DUTYFREE_TOURISM_POLICY_KOREA,
        secondary_archetypes=(E2RArchetype.CASINO_DUTYFREE_TOURISM, E2RArchetype.TRAVEL_LEISURE_REOPENING, E2RArchetype.EVENT_PREMIUM),
        case_type="event_premium",
        stage1_date=date(2025, 3, 20),
        stage2_date=date(2025, 8, 6),
        stage3_date=None,
        stage4b_date=date(2025, 8, 6),
        stage4c_date=None,
        stage3_decision="china_visa_free_policy_is_stage2_event_until_tourist_spend_duty_free_sales_casino_drop_hold_hotel_occupancy_and_opm_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("hotel_shilla_event_mfe_4_8pct", "paradise_event_mfe_2_9pct", "hyundai_department_event_mfe_7_1pct", "hankook_cosmetics_event_mfe_9_9pct", "2025_target_visitors_18_5m"),
        red_flag_fields=("tourist_arrival_policy_only", "tourist_spend_unverified", "duty_free_sales_unverified", "casino_drop_hold_unverified", "opm_unverified"),
        price_data_source="Reuters tourism-policy and event-return anchors",
        reported_price_anchor="Hotel Shilla +4.8%, Paradise +2.9%, Hyundai Department Store +7.1%, Hankook Cosmetics +9.9%",
        reported_return_anchor="2024 visitors 16.4M; 2025 target 18.5M; visa-free stay up to 15 days",
        mfe_1d=9.9,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"hotel_shilla_event_mfe_1d_pct": 4.8, "paradise_event_mfe_1d_pct": 2.9, "hyundai_department_event_mfe_1d_pct": 7.1, "hankook_cosmetics_event_mfe_1d_pct": 9.9, "visitors_2024_mn": 16.4, "visitor_growth_2024_pct": 48.0, "chinese_share_pct": 28.0, "target_visitors_2025_mn": 18.5, "target_growth_vs_2024_pct": 12.8, "visa_free_stay_days": 15.0},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="stage2_watch_success",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="Visa-free policy is Stage 2/event premium; tourist spend, casino drop/hold, duty-free sales, occupancy, OPM, and FCF decide promotion.",
    ),
    Round226CaseCandidate(
        case_id="r9_loop9_lotte_tour_china_japan_redirect_event",
        symbol="032350/104620",
        company_name="롯데관광개발/Yellow Balloon",
        primary_archetype=E2RArchetype.TOURISM_POLICY_EVENT,
        secondary_archetypes=(E2RArchetype.TRAVEL_LEISURE_REOPENING, E2RArchetype.EVENT_PREMIUM, E2RArchetype.PRICE_ONLY_RALLY),
        case_type="event_premium",
        stage1_date=date(2025, 11, 17),
        stage2_date=date(2025, 11, 21),
        stage3_date=None,
        stage4b_date=date(2025, 11, 21),
        stage4c_date=None,
        stage3_decision="china_japan_redirect_expectation_is_4b_event_premium_until_actual_arrivals_spend_occupancy_casino_drop_adr_and_fcf_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("lotte_tour_event_mfe_above_20pct", "yellow_balloon_event_mfe_24pct", "shinsegae_event_mfe_6pct", "japan_booking_loss_example_80pct"),
        red_flag_fields=("tourism_redirect_event_only", "actual_arrivals_unverified", "tourist_spend_unverified", "occupancy_adr_unverified", "debt_refinancing_watch"),
        price_data_source="Reuters tourism-redirect event anchors",
        reported_price_anchor="Lotte Tour +20%+, Yellow Balloon +24%, Shinsegae +6%",
        reported_return_anchor="Japan booking loss example 80%; Korea redirect status was early signs only",
        mfe_1d=24.0,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"lotte_tour_event_mfe_pct": 20.0, "yellow_balloon_event_mfe_pct": 24.0, "shinsegae_event_mfe_pct": 6.0, "japan_booking_loss_example_pct": 80.0, "redirect_status": "early_signs_only"},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="false_yellow",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="Tourism redirect expectation moved price before actual arrivals, occupancy, casino drop, ADR, and FCF.",
    ),
)


def round226_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND226_CASE_CANDIDATES:
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
                "Round226 R9 Loop-9 mobility/transport/leisure price-path "
                "validation case. Calibration-only; not production scoring input."
            ),
            stage1_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "event" in field or "target" in field or "freight" in field or "visa" in field or "fatal" in field
            ),
            stage2_evidence=candidate.evidence_fields if candidate.stage2_date else (),
            stage3_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "opm" in field
                or "fcf" in field
                or "margin" in field
                or "hybrid" in field
                or "revenue" in field
                or "profit" in field
            ),
            stage4b_evidence=tuple(
                field
                for field in (*candidate.evidence_fields, *candidate.red_flag_fields)
                if "event" in field or "mfe" in field or "policy" in field or "spike" in field or "freight" in field
            ),
            stage4c_evidence=tuple(
                field
                for field in candidate.red_flag_fields
                if "fatal" in field
                or "safety" in field
                or "tariff" in field
                or "capex" in field
                or "debt" in field
                or "overcapacity" in field
                or "trust" in field
            ),
            must_have_fields=ROUND226_GREEN_REQUIRED_FIELDS,
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
            score_weight_hint={f"{item.axis}_delta": float(item.points) for item in ROUND226_SCORE_ADJUSTMENTS},
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "full_ohlc_complete_false",
                "price_validation_partial_with_reported_price_anchors",
                "do_not_invent_price_or_stage_dates",
                "do_not_treat_reopening_freight_sdv_merger_or_tourism_policy_headline_as_green_alone",
                *ROUND226_GREEN_REQUIRED_FIELDS,
                *ROUND226_GREEN_FORBIDDEN_PATTERNS,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(
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
                price_data_available=(
                    candidate.stage2_price_anchor is not None
                    or candidate.mfe_1d is not None
                    or candidate.mae_1d is not None
                ),
                stage_dates_confidence=0.8 if candidate.stage2_date or candidate.stage4c_date else 0.65,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round226_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND226_CASE_CANDIDATES:
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


def round226_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND226_SCORE_ADJUSTMENTS)


def round226_shadow_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(row.as_row() for row in ROUND226_SHADOW_WEIGHT_ROWS)


def round226_price_validation_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round226_price_validation": "true"} for field in ROUND226_PRICE_VALIDATION_FIELDS)


def round226_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple({"round226_label": label, "canonical_archetype": canonical} for label, canonical in ROUND226_REQUIRED_TARGET_ALIASES.items())


def round226_summary() -> dict[str, int | bool | str]:
    cases = ROUND226_CASE_CANDIDATES
    return {
        "source_round": ROUND226_SOURCE_ROUND_PATH,
        "large_sector": ROUND226_LARGE_SECTOR.value,
        "case_candidate_count": len(cases),
        "success_candidate_count": sum(1 for case in cases if case.case_type == "success_candidate"),
        "event_premium_count": sum(1 for case in cases if case.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for case in cases if case.case_type == "failed_rerating"),
        "cyclical_success_count": sum(1 for case in cases if case.case_type == "cyclical_success"),
        "stage3_case_count": sum(1 for case in cases if case.stage3_date is not None),
        "stage4b_watch_count": sum(1 for case in cases if case.stage4b_status == "watch"),
        "hard_4c_case_count": sum(1 for case in cases if case.hard_4c_confirmed),
        "target_archetype_count": len(ROUND226_REQUIRED_TARGET_ALIASES),
        "price_validation_completed": "partial_with_reported_price_anchors",
        "full_ohlc_complete": False,
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
    }


def round226_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND226_SOURCE_ROUND_PATH,
        "large_sector": ROUND226_LARGE_SECTOR.value,
        "summary": round226_summary(),
        "target_aliases": dict(ROUND226_REQUIRED_TARGET_ALIASES),
        "green_required_fields": list(ROUND226_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND226_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_watch_triggers": list(ROUND226_STAGE4B_WATCH_TRIGGERS),
        "hard_4c_gates": list(ROUND226_HARD_4C_GATES),
        "what_not_to_change": [
            "do_not_use_round226_cases_as_candidate_generation_input",
            "do_not_apply_shadow_weights_to_production_scoring_yet",
            "do_not_treat_travel_reopening_freight_spike_sdv_story_merger_or_tourism_policy_as_green",
            "do_not_invent_ohlc_or_stage_dates",
        ],
    }


def render_round226_summary_markdown() -> str:
    summary = round226_summary()
    lines = [
        "# Round 226 R9 Loop 9 Mobility Transport Leisure Price Validation",
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
        f"- cyclical_success: {summary['cyclical_success_count']}",
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
    for case in ROUND226_CASE_CANDIDATES:
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
            "- Hyundai is a hybrid/value-up Stage 2 watch, but tariff cost adds 4C-watch.",
            "- Kia and CJ Logistics show why evidence can be useful while price or capex/margin confirmation still fails.",
            "- Korean Air is integration scale watch, while Jeju Air is a hard safety/trust 4C example.",
            "- HMM is cyclical success; tourism baskets are event premium until spend, utilization, and FCF confirm.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round226_green_gate_review_markdown() -> str:
    lines = [
        "# Round 226 R9 Green Gate Review",
        "",
        "Do not apply these weights to production scoring yet.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND226_GREEN_REQUIRED_FIELDS)
    lines.extend(["", "## Forbidden Patterns", ""])
    lines.extend(f"- {field}" for field in ROUND226_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(
        [
            "",
            "## Easy Example",
            "- `freight rate +40%` can create a Stage 2/cyclical watch.",
            "- `freight rate +40% + contract mix + FCF + capital return + no overcapacity` is the bundle that can support deeper Stage review.",
            "- `fatal safety accident` is hard 4C regardless of travel demand.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round226_stage4b_4c_review_markdown() -> str:
    lines = ["# Round 226 R9 4B/4C Review", "", "## 4B Watch Triggers", ""]
    lines.extend(f"- {field}" for field in ROUND226_STAGE4B_WATCH_TRIGGERS)
    lines.extend(["", "## Hard 4C Gates", ""])
    lines.extend(f"- {field}" for field in ROUND226_HARD_4C_GATES)
    lines.extend(["", "## Case Notes", ""])
    for case in ROUND226_CASE_CANDIDATES:
        if case.stage4b_status == "watch" or case.stage4c_date or case.red_flag_fields:
            lines.append(f"- {case.case_id}: {', '.join(case.red_flag_fields)}")
    return "\n".join(lines) + "\n"


def render_round226_price_validation_plan_markdown() -> str:
    lines = [
        "# Round 226 R9 Price Validation Plan",
        "",
        "- price_validation_completed: partial_with_reported_price_anchors",
        "- full_ohlc_complete: false",
        "- Do not invent OHLC, peak, MFE, or MAE where raw adjusted daily prices are unavailable.",
        "",
        "## Backfill Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND226_PRICE_VALIDATION_FIELDS)
    return "\n".join(lines) + "\n"


def write_round226_r9_loop9_reports(
    output_directory: str | Path = ROUND226_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND226_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND226_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "cases": write_case_library(round226_case_records(), cases_path),
        "audit": _write_json(round226_audit_payload(), audit_path),
        "summary": output / "round226_r9_loop9_price_validation_summary.md",
        "case_matrix": output / "round226_r9_loop9_case_matrix.csv",
        "target_aliases": output / "round226_r9_loop9_target_aliases.csv",
        "score_adjustments": output / "round226_r9_loop9_score_adjustments.csv",
        "shadow_weights": output / "round226_r9_loop9_shadow_weights.csv",
        "price_validation_fields": output / "round226_r9_loop9_price_validation_fields.csv",
        "green_gate_review": output / "round226_r9_loop9_green_gate_review.md",
        "price_validation_plan": output / "round226_r9_loop9_price_validation_plan.md",
        "stage4b_4c_review": output / "round226_r9_loop9_stage4b_4c_review.md",
    }
    paths["summary"].write_text(render_round226_summary_markdown(), encoding="utf-8")
    _write_csv(round226_case_rows(), paths["case_matrix"])
    _write_csv(round226_target_alias_rows(), paths["target_aliases"])
    _write_csv(round226_score_adjustment_rows(), paths["score_adjustments"])
    _write_csv(round226_shadow_weight_rows(), paths["shadow_weights"])
    _write_csv(round226_price_validation_field_rows(), paths["price_validation_fields"])
    paths["green_gate_review"].write_text(render_round226_green_gate_review_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round226_price_validation_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round226_stage4b_4c_review_markdown(), encoding="utf-8")
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
