"""Round-213 R9 Loop-8 mobility/transport/leisure price validation pack.

Round 213 is calibration/evaluation material only. It structures
``docs/round/round_213.md`` into case records, reported event anchors, and
shadow scoring notes.

Easy example: a visa-free tourism policy can lift hotel and casino stocks for
one day. It is not Stage 3-Green until tourist spend, casino drop/hold,
occupancy, margin, FCF, and operational trust are visible as of the case date.
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


ROUND213_SOURCE_ROUND_PATH = "docs/round/round_213.md"
ROUND213_LARGE_SECTOR = Round10LargeSector.MOBILITY_TRANSPORT_LEISURE
ROUND213_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round213_r9_loop8_mobility_transport_leisure_price_validation"
ROUND213_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r9_loop8_round213.jsonl"
ROUND213_DEFAULT_AUDIT_PATH = "data/sector_taxonomy/round213_r9_loop8_mobility_transport_leisure_price_validation_audit.json"

ROUND213_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "AUTO_HYBRID_VALUEUP": E2RArchetype.AUTO_HYBRID_VALUEUP.value,
    "AUTO_TARIFF_LOCALIZATION": E2RArchetype.AUTO_TARIFF_LOCALIZATION.value,
    "AUTO_SDV_DELAY_CAPEX_OVERLAY": E2RArchetype.AUTO_SDV_DELAY_CAPEX_OVERLAY.value,
    "AUTO_PRICE_WAR_EUROPE_OVERLAY": E2RArchetype.AUTO_PRICE_WAR_EUROPE_OVERLAY.value,
    "AIRLINE_INTEGRATION_SCALE": E2RArchetype.AIRLINE_INTEGRATION_SCALE.value,
    "AIRLINE_SAFETY_REGULATORY_OVERLAY": E2RArchetype.AIRLINE_SAFETY_REGULATORY_OVERLAY.value,
    "SHIPPING_FREIGHT_CYCLE": E2RArchetype.SHIPPING_FREIGHT_CYCLE.value,
    "CASINO_DUTYFREE_TOURISM": E2RArchetype.CASINO_DUTYFREE_TOURISM.value,
    "TRAVEL_LEISURE_REOPENING": E2RArchetype.TRAVEL_LEISURE_REOPENING.value,
    "FLEET_UNIT_ECONOMICS_OVERLAY": E2RArchetype.FLEET_UNIT_ECONOMICS_OVERLAY.value,
    "PRICE_ONLY_RALLY": E2RArchetype.PRICE_ONLY_RALLY.value,
    "THESIS_BREAK_4C": E2RArchetype.THESIS_BREAK_4C.value,
    "OPERATIONAL_TRUST_BREAK": E2RArchetype.OPERATIONAL_TRUST_BREAK.value,
}

ROUND213_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "unit_economics",
    "fcf_after_capex",
    "margin_durability",
    "hybrid_mix_or_load_factor_or_freight_contract_or_tourist_spend",
    "shareholder_return_or_deleveraging",
    "safety_and_operational_trust_passed",
    "tariff_fuel_fx_freight_normalization_stress_passed",
    "price_path_after_evidence",
)

ROUND213_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "travel_reopening_only",
    "freight_rate_spike_only",
    "robotaxi_or_sdv_story_only",
    "tourist_arrival_policy_only",
    "merger_completion_without_synergy",
    "ev_or_ai_mobility_theme_only",
    "capex_heavy_localization_without_margin",
    "safety_failure",
    "tariff_margin_cut",
    "utilization_weak",
    "cycle_normalization",
)

ROUND213_STAGE4B_WATCH_TRIGGERS: tuple[str, ...] = (
    "hybrid_valueup_fast_rerating",
    "sdv_ai_mobility_before_software_revenue",
    "airline_merger_completion_price_spike",
    "red_sea_freight_rate_spike",
    "china_visa_free_tourism_basket_spike",
    "tourism_redirect_event_before_sales",
)

ROUND213_HARD_4C_GATES: tuple[str, ...] = (
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

ROUND213_PRICE_VALIDATION_FIELDS: tuple[str, ...] = (
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
    "relative_underperformance_pp",
    "freight_or_tourism_metric",
    "capacity_or_transaction_value",
    "safety_or_margin_event",
    "price_validation_status",
)


@dataclass(frozen=True)
class Round213ScoreAdjustment:
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
class Round213CaseCandidate:
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
    stage4c_price_anchor: float | None
    extra_price_metrics: Mapping[str, float | str]
    score_price_alignment: str
    rerating_result: str
    stage_failure_type: str
    price_validation_status: str
    notes: str

    @property
    def large_sector(self) -> str:
        return ROUND213_LARGE_SECTOR.value

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND213_SCORE_ADJUSTMENTS: tuple[Round213ScoreAdjustment, ...] = (
    Round213ScoreAdjustment("hybrid_mix", 5, "raise", "완성차는 EV 테마보다 hybrid mix와 마진 방어가 중요하다."),
    Round213ScoreAdjustment("fcf_after_capex", 5, "raise", "R9 Green은 capex 이후 FCF가 남는지 확인해야 한다."),
    Round213ScoreAdjustment("shareholder_return_execution", 5, "raise", "자사주·배당 실행은 완성차 rerating의 핵심 증거다."),
    Round213ScoreAdjustment("operating_margin_durability", 5, "raise", "관세·연료·운임 stress 이후에도 마진이 유지돼야 한다."),
    Round213ScoreAdjustment("localization_tariff_hedge", 4, "raise", "현지 생산은 관세 충격을 줄이는 Stage 2~3 증거가 될 수 있다."),
    Round213ScoreAdjustment("unit_economics", 5, "raise", "렌터카·항공·관광은 이용률보다 unit economics가 먼저다."),
    Round213ScoreAdjustment("load_factor_with_yield", 4, "raise", "항공은 탑승률과 yield가 같이 좋아야 한다."),
    Round213ScoreAdjustment("integration_synergy_realized", 4, "raise", "항공 통합은 완료보다 시너지 실현이 중요하다."),
    Round213ScoreAdjustment("freight_contract_mix", 4, "raise", "해운은 spot 운임보다 contract mix와 FCF가 중요하다."),
    Round213ScoreAdjustment("tourist_spend_conversion", 5, "raise", "관광은 입국자 수보다 소비 전환이 핵심이다."),
    Round213ScoreAdjustment("casino_drop_and_hold", 5, "raise", "카지노는 관광객보다 drop/hold와 OPM을 확인해야 한다."),
    Round213ScoreAdjustment("safety_record_and_operational_trust", 5, "raise", "항공과 모빌리티는 안전 신뢰가 Green의 전제다."),
    Round213ScoreAdjustment("travel_reopening_only", -5, "lower", "여행 재개만으로는 Stage 3-Green을 만들 수 없다."),
    Round213ScoreAdjustment("freight_rate_spike_only", -5, "lower", "운임 spike는 cycle일 수 있으므로 Green을 제한한다."),
    Round213ScoreAdjustment("robotaxi_or_sdv_story_only", -5, "lower", "SDV/로보택시 스토리는 유료 SW 매출 전까지 제한한다."),
    Round213ScoreAdjustment("tourist_arrival_policy_only", -5, "lower", "무비자 정책과 입국자 수만으로는 관광주 Green 금지다."),
    Round213ScoreAdjustment("merger_completion_without_synergy", -4, "lower", "합병 완료만 있고 시너지·FCF가 없으면 Stage 2다."),
    Round213ScoreAdjustment("ev_or_ai_mobility_theme_only", -4, "lower", "EV/AI mobility 테마만으로는 이익 체급 변화가 아니다."),
    Round213ScoreAdjustment("capex_heavy_localization_without_margin", -4, "lower", "현지화 capex가 마진을 방어하지 못하면 제한한다."),
    Round213ScoreAdjustment("safety_failure", -5, "lower", "fatal safety accident는 hard 4C다."),
    Round213ScoreAdjustment("tariff_margin_cut", -5, "lower", "관세가 구조적으로 마진 목표를 깎으면 4C-watch다."),
    Round213ScoreAdjustment("utilization_weak", -5, "lower", "관광·카지노·항공은 utilization이 약하면 Green 금지다."),
    Round213ScoreAdjustment("cycle_normalization", -5, "lower", "해운과 관광 cycle 정상화는 Stage 4C risk다."),
)


ROUND213_CASE_CANDIDATES: tuple[Round213CaseCandidate, ...] = (
    Round213CaseCandidate(
        case_id="r9_loop8_hyundai_hybrid_valueup_tariff_watch",
        symbol="005380",
        company_name="현대차",
        primary_archetype=E2RArchetype.AUTO_HYBRID_VALUEUP,
        secondary_archetypes=(E2RArchetype.AUTO_TARIFF_LOCALIZATION, E2RArchetype.AUTO_MOBILITY_COMPLETED_VEHICLE),
        case_type="structural_success",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2024, 8, 28),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 9, 18),
        stage3_decision="stage3_candidate_if_hybrid_mix_fcf_buyback_execution_and_opm_confirm_but_tariff_margin_cut_is_4c_watch",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("hybrid_sales_target_2028_1_33m", "buyback_plan_4tn_krw", "shareholder_return_35pct_profit", "long_term_opm_target_above_10pct", "stage2_close_return_4_7pct"),
        red_flag_fields=("tariff_margin_target_cut", "q2_2025_tariff_cost_828bn_krw", "localization_capex_watch", "stage3_price_unavailable"),
        price_data_source="Reuters reported event returns and margin target anchors",
        reported_price_anchor="absolute Hyundai close unavailable; event close return +4.7%",
        reported_return_anchor="intraday +5.0%, close +4.7%; later OPM midpoint cut 7.5% to 6.5%",
        mfe_1d=5.0,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"stage2_event_mfe_intraday_pct": 5.0, "stage2_event_close_return_pct": 4.7, "sales_target_2030_mn": 5.55, "sales_target_growth_vs_2023_pct": 30.0, "hybrid_sales_target_2028_mn": 1.33, "hybrid_target_increase_pct": 40.0, "buyback_plan_krw_trn": 4.0, "shareholder_return_policy_pct": 35.0, "margin_midpoint_before_pct": 7.5, "margin_midpoint_after_pct": 6.5, "relative_margin_target_cut_pct": -13.3, "q2_2025_tariff_cost_krw_bn": 828.0},
        score_price_alignment="aligned",
        rerating_result="true_rerating",
        stage_failure_type="stage2_watch_success",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="Hybrid/value-up can become Stage 3 if FCF, buyback execution, and OPM confirm; tariff margin cut remains 4C-watch.",
    ),
    Round213CaseCandidate(
        case_id="r9_loop8_kia_sdv_delay_capex_watch",
        symbol="000270",
        company_name="기아",
        primary_archetype=E2RArchetype.AUTO_SDV_DELAY_CAPEX_OVERLAY,
        secondary_archetypes=(E2RArchetype.AUTO_HYBRID_VALUEUP, E2RArchetype.FLEET_UNIT_ECONOMICS_OVERLAY),
        case_type="success_candidate",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2026, 4, 9),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2026, 4, 9),
        stage3_decision="hybrid_plan_positive_but_sdv_delay_ev_target_cut_and_capex_hike_block_green_until_sw_revenue_and_fcf_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("hybrid_target_2030_1_1m", "sales_target_2030_4_13m", "sdv_ai_investment_plan", "hybrid_target_increase_60pct"),
        red_flag_fields=("sdv_launch_delay_one_year", "investment_plan_increase_30pct", "ev_target_cut_20pct", "stage2_event_mae_minus_5_5pct"),
        price_data_source="Reuters reported event return and capex target anchors",
        reported_price_anchor="absolute Kia close unavailable; event close return -5.5%",
        reported_return_anchor="Kia -5.5%, KOSPI -1.6%, relative -3.9pp",
        mfe_1d=None,
        mae_1d=-5.5,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"stage2_event_mae_1d_pct": -5.5, "kospi_same_day_return_pct": -1.6, "relative_underperformance_pp": -3.9, "investment_plan_krw_trn": 41.4, "investment_plan_increase_pct": 30.0, "implied_prior_investment_plan_krw_trn": 31.85, "ev_target_2030_mn": 1.0, "ev_target_cut_pct": 20.0, "sales_target_2030_mn": 4.13, "sales_2025_mn": 3.14, "sales_target_growth_vs_2025_pct": 31.5, "hybrid_target_2030_mn": 1.1, "hybrid_target_increase_pct": 60.0},
        score_price_alignment="evidence_good_but_price_failed",
        rerating_result="unknown",
        stage_failure_type="false_yellow",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="Hybrid plan is positive, but SDV delay, EV target cut, capex burden, and weak price reaction block Green.",
    ),
    Round213CaseCandidate(
        case_id="r9_loop8_korean_air_asiana_integration",
        symbol="003490",
        company_name="대한항공",
        primary_archetype=E2RArchetype.AIRLINE_INTEGRATION_SCALE,
        secondary_archetypes=(E2RArchetype.AIRLINE_TRAVEL_CYCLE, E2RArchetype.FLEET_UNIT_ECONOMICS_OVERLAY),
        case_type="success_candidate",
        stage1_date=date(2020, 1, 1),
        stage2_date=date(2024, 12, 12),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="stage3_requires_integration_synergy_route_optimization_load_factor_yield_debt_and_fcf",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("asiana_acquisition_complete", "asiana_stake_63_88pct", "international_capacity_rank_12", "route_optimization_plan", "lcc_consolidation_plan"),
        red_flag_fields=("integration_synergy_unverified", "boeing_order_capex_watch", "fuel_cost_watch", "debt_capex_burden"),
        price_data_source="Reuters/Business Insider transaction anchors",
        reported_price_anchor="Korean Air OHLC unavailable after deep search",
        reported_return_anchor="Asiana deal $1.3B; Boeing order $36.2B, 27.8x Asiana deal value",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"asiana_stake_acquired_pct": 63.88, "asiana_deal_value_usd_bn": 1.3, "international_capacity_rank": 12.0, "boeing_order_value_usd_bn": 36.2, "aircraft_order_count": 103.0, "spare_engine_purchase_usd_mn": 690.0, "ge_engine_maintenance_contract_usd_bn": 13.0, "capex_scale_vs_asiana_deal_multiple": 27.8},
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Merger completion is Stage 2; synergy, load factor, yield, debt, capex burden, and FCF decide promotion.",
    ),
    Round213CaseCandidate(
        case_id="r9_loop8_jeju_air_fatal_crash_hard_4c",
        symbol="089590",
        company_name="제주항공",
        primary_archetype=E2RArchetype.AIRLINE_SAFETY_REGULATORY_OVERLAY,
        secondary_archetypes=(E2RArchetype.OPERATIONAL_TRUST_BREAK, E2RArchetype.THESIS_BREAK_4C),
        case_type="4c_thesis_break",
        stage1_date=date(2023, 1, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2024, 12, 30),
        stage3_decision="fatal_safety_accident_is_hard_4c_and_blocks_any_travel_demand_green",
        stage4b_status="watch",
        hard_4c_confirmed=True,
        evidence_fields=("travel_demand_recovery_lcc_context",),
        red_flag_fields=("fatal_safety_accident_179_deaths", "operational_trust_break", "emergency_safety_inspection", "record_low_price"),
        price_data_source="Reuters reported price anchor and event return",
        reported_price_anchor="6,920 KRW intraday low after fatal crash",
        reported_return_anchor="Jeju Air intraday -15.7%; market cap wipeout 95.7B KRW",
        mfe_1d=None,
        mae_1d=-15.7,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4c_price_anchor=6920.0,
        extra_price_metrics={"stage4c_price_anchor_krw": 6920.0, "stage4c_event_mae_1d_pct": -15.7, "implied_pre_event_reference_price_krw": 8209.0, "market_cap_wipeout_krw_bn": 95.7, "ak_holdings_event_mae_pct": -12.0, "korean_air_event_mae_pct": -1.3, "asiana_event_mae_pct": -0.8, "hanatour_event_mae_pct": -7.0, "very_good_tour_event_mae_pct": -11.0},
        score_price_alignment="false_positive_score",
        rerating_result="thesis_break",
        stage_failure_type="should_have_been_red",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="Fatal crash is a hard 4C safety/trust break; travel-demand recovery cannot offset it.",
    ),
    Round213CaseCandidate(
        case_id="r9_loop8_hmm_red_sea_freight_cycle",
        symbol="011200",
        company_name="HMM",
        primary_archetype=E2RArchetype.SHIPPING_FREIGHT_CYCLE,
        secondary_archetypes=(E2RArchetype.SHIPPING_FREIGHT_CYCLE_KOREA, E2RArchetype.PRICE_ONLY_RALLY),
        case_type="cyclical_success",
        stage1_date=date(2024, 5, 1),
        stage2_date=date(2024, 7, 3),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="freight_rate_spike_is_cyclical_stage2_until_multi_quarter_floor_contract_mix_fcf_and_capital_return_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("red_sea_disruption", "freightos_index_up_40pct", "capacity_tied_up_5_9pct", "maersk_profit_swing_2_521bn_usd"),
        red_flag_fields=("freight_rate_spike_only", "cycle_normalization", "container_overcapacity_watch", "hmm_stock_ohlc_unavailable"),
        price_data_source="Reuters/WSJ freight-rate and proxy stock anchors",
        reported_price_anchor="HMM OHLC unavailable after deep search",
        reported_return_anchor="Freightos +40% to $5,068; Hapag-Lloyd proxy +7%; Maersk profit swing +$2.521B",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"freightos_index_usd": 5068.0, "freightos_index_6w_return_pct": 40.0, "implied_prior_freightos_index_usd": 3620.0, "capacity_tied_up_low_pct": 5.0, "capacity_tied_up_high_pct": 9.0, "hapag_lloyd_proxy_stock_return_pct": 7.0, "maersk_q4_2024_net_profit_usd_bn": 2.085, "maersk_q4_2023_net_loss_usd_bn": -0.436, "maersk_profit_swing_usd_bn": 2.521, "maersk_shipping_rate_increase_pct": 38.0, "maersk_ocean_freight_revenue_increase_pct": 49.0, "maersk_ebit_swing_usd_bn": 2.52},
        score_price_alignment="aligned",
        rerating_result="cyclical_rerating",
        stage_failure_type="stage2_watch_success",
        price_validation_status="hmm_stock_price_data_unavailable_after_deep_search",
        notes="Freight spike can produce earnings, but this remains cyclical until rate floor, contract mix, FCF, and capital return confirm.",
    ),
    Round213CaseCandidate(
        case_id="r9_loop8_hotel_shilla_paradise_china_visa_event",
        symbol="008770/034230",
        company_name="호텔신라/파라다이스",
        primary_archetype=E2RArchetype.CASINO_DUTYFREE_TOURISM,
        secondary_archetypes=(E2RArchetype.TRAVEL_LEISURE_REOPENING, E2RArchetype.PRICE_ONLY_RALLY),
        case_type="event_premium",
        stage1_date=date(2025, 3, 20),
        stage2_date=date(2025, 8, 6),
        stage3_date=None,
        stage4b_date=date(2025, 8, 6),
        stage4c_date=None,
        stage3_decision="tourist_arrivals_and_visa_policy_are_not_green_until_spend_dutyfree_sales_casino_drop_hold_opm_and_fcf_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("china_group_visa_free_policy", "visitor_growth_2024_48pct", "hotel_shilla_event_return_4_8pct", "paradise_event_return_2_9pct"),
        red_flag_fields=("tourist_arrival_policy_only", "tourist_spend_unverified", "casino_drop_hold_unverified", "flight_capacity_already_105pct_pre_covid"),
        price_data_source="Reuters reported event returns and tourism metrics",
        reported_price_anchor="absolute prices unavailable",
        reported_return_anchor="Hotel Shilla +4.8%; Paradise +2.9%; Hyundai Department +7.1%; Hankook Cosmetics +9.9%",
        mfe_1d=4.8,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"hotel_shilla_event_mfe_1d_pct": 4.8, "paradise_event_mfe_1d_pct": 2.9, "hyundai_department_event_mfe_1d_pct": 7.1, "hankook_cosmetics_event_mfe_1d_pct": 9.9, "visitors_2024_mn": 16.4, "visitor_growth_2024_pct": 48.0, "chinese_share_of_visitors_pct": 28.0, "target_visitors_2025_mn": 18.5, "visitor_target_growth_vs_2024_pct": 12.8, "korea_china_flight_capacity_vs_pre_pandemic_pct": 105.0},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="stage2_watch_success",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="Visa-free policy is Stage 1/2 and event premium until tourist spend, duty-free sales, casino drop/hold, OPM, and FCF confirm.",
    ),
    Round213CaseCandidate(
        case_id="r9_loop8_lotte_tour_china_japan_redirect",
        symbol="032350",
        company_name="롯데관광개발",
        primary_archetype=E2RArchetype.TRAVEL_LEISURE_REOPENING,
        secondary_archetypes=(E2RArchetype.CASINO_DUTYFREE_TOURISM, E2RArchetype.PRICE_ONLY_RALLY),
        case_type="event_premium",
        stage1_date=date(2025, 11, 21),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=date(2025, 11, 21),
        stage4c_date=None,
        stage3_decision="tourism_redirect_event_is_not_green_until_casino_drop_hold_occupancy_adr_and_fcf_confirm",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("china_japan_diplomatic_dispute_tourism_redirect", "lotte_tour_event_return_above_20pct", "yellow_balloon_event_return_24pct"),
        red_flag_fields=("tourist_redirect_event_only", "casino_utilization_unverified", "political_instability_watch", "refinancing_or_license_risk_watch"),
        price_data_source="Reuters/FT reported event returns and industry risk anchors",
        reported_price_anchor="absolute prices unavailable",
        reported_return_anchor="Lotte Tour +20%+, Yellow Balloon +24%, Shinsegae +6%",
        mfe_1d=20.0,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4c_price_anchor=None,
        extra_price_metrics={"lotte_tour_event_mfe_pct_min": 20.0, "yellow_balloon_event_mfe_pct": 24.0, "shinsegae_event_mfe_pct": 6.0, "inspire_project_value_usd_bn": 1.6, "bain_loan_called_usd_mn": 275.0, "mohegan_equity_investment_usd_mn": 300.0},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="false_yellow",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="Tourism redirect event produced price movement before casino drop, hold rate, occupancy, ADR, and FCF were confirmed.",
    ),
)


def round213_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND213_CASE_CANDIDATES:
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
                "Round213 R9 Loop-8 mobility/transport/leisure price-path "
                "validation case. Calibration-only; not production scoring input."
            ),
            stage1_evidence=tuple(field for field in candidate.evidence_fields if "policy" in field or "target" in field or "recovery" in field or "disruption" in field),
            stage2_evidence=candidate.evidence_fields if candidate.stage2_date else (),
            stage3_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "hybrid" in field
                or "buyback" in field
                or "shareholder" in field
                or "opm" in field
                or "synergy" in field
                or "drop" in field
                or "fcf" in field
            ),
            stage4b_evidence=tuple(
                field
                for field in (*candidate.evidence_fields, *candidate.red_flag_fields)
                if "event" in field or "spike" in field or "policy" in field or "freight" in field or "tourism" in field or "redirect" in field
            ),
            stage4c_evidence=tuple(
                field
                for field in candidate.red_flag_fields
                if "safety" in field
                or "tariff" in field
                or "margin" in field
                or "fuel" in field
                or "cycle" in field
                or "overcapacity" in field
                or "utilization" in field
                or "capex" in field
                or "debt" in field
                or "trust" in field
            ),
            must_have_fields=ROUND213_GREEN_REQUIRED_FIELDS,
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
                "hybrid_mix_delta": 5.0,
                "fcf_after_capex_delta": 5.0,
                "shareholder_return_execution_delta": 5.0,
                "operating_margin_durability_delta": 5.0,
                "localization_tariff_hedge_delta": 4.0,
                "unit_economics_delta": 5.0,
                "load_factor_with_yield_delta": 4.0,
                "integration_synergy_realized_delta": 4.0,
                "freight_contract_mix_delta": 4.0,
                "tourist_spend_conversion_delta": 5.0,
                "casino_drop_and_hold_delta": 5.0,
                "safety_record_and_operational_trust_delta": 5.0,
                "travel_reopening_only_delta": -5.0,
                "freight_rate_spike_only_delta": -5.0,
                "robotaxi_or_sdv_story_only_delta": -5.0,
                "tourist_arrival_policy_only_delta": -5.0,
                "merger_completion_without_synergy_delta": -4.0,
                "ev_or_ai_mobility_theme_only_delta": -4.0,
                "capex_heavy_localization_without_margin_delta": -4.0,
                "safety_failure_delta": -5.0,
                "tariff_margin_cut_delta": -5.0,
                "utilization_weak_delta": -5.0,
                "cycle_normalization_delta": -5.0,
            },
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "full_ohlc_complete_false",
                "price_validation_partial_with_reported_price_anchors",
                "do_not_invent_price_or_stage_dates",
                "do_not_treat_travel_reopening_freight_spike_sdv_story_tourism_policy_or_merger_completion_as_green_alone",
                *ROUND213_GREEN_REQUIRED_FIELDS,
                *ROUND213_GREEN_FORBIDDEN_PATTERNS,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(
                stage2_price=candidate.stage2_price_anchor,
                stage3_price=candidate.stage3_price_anchor,
                stage4c_price=candidate.stage4c_price_anchor,
                mfe_30d=candidate.mfe_1d,
                mae_30d=candidate.mae_1d,
                price_validation_status=candidate.price_validation_status,
            ),
            data_quality=CaseDataQuality(
                official_data_available=True,
                report_data_available=True,
                price_data_available=candidate.stage2_price_anchor is not None or candidate.stage4c_price_anchor is not None or candidate.mfe_1d is not None or candidate.mae_1d is not None,
                stage_dates_confidence=0.8 if candidate.stage2_date or candidate.stage4c_date else 0.65,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round213_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND213_CASE_CANDIDATES:
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


def round213_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND213_SCORE_ADJUSTMENTS)


def round213_price_validation_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round213_price_validation": "true"} for field in ROUND213_PRICE_VALIDATION_FIELDS)


def round213_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {"round213_label": label, "canonical_archetype": canonical}
        for label, canonical in ROUND213_REQUIRED_TARGET_ALIASES.items()
    )


def round213_summary() -> dict[str, int | bool | str]:
    cases = ROUND213_CASE_CANDIDATES
    return {
        "source_round": ROUND213_SOURCE_ROUND_PATH,
        "large_sector": ROUND213_LARGE_SECTOR.value,
        "case_candidate_count": len(cases),
        "structural_success_count": sum(1 for case in cases if case.case_type == "structural_success"),
        "success_candidate_count": sum(1 for case in cases if case.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for case in cases if case.case_type == "cyclical_success"),
        "event_premium_count": sum(1 for case in cases if case.case_type == "event_premium"),
        "thesis_break_count": sum(1 for case in cases if case.case_type == "4c_thesis_break"),
        "stage3_case_count": sum(1 for case in cases if case.stage3_date is not None),
        "stage4b_watch_count": sum(1 for case in cases if case.stage4b_status == "watch"),
        "hard_4c_case_count": sum(1 for case in cases if case.hard_4c_confirmed),
        "target_archetype_count": len(ROUND213_REQUIRED_TARGET_ALIASES),
        "price_validation_completed": "partial_with_reported_price_anchors",
        "full_ohlc_complete": False,
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
    }


def round213_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND213_SOURCE_ROUND_PATH,
        "large_sector": ROUND213_LARGE_SECTOR.value,
        "summary": round213_summary(),
        "target_aliases": dict(ROUND213_REQUIRED_TARGET_ALIASES),
        "green_required_fields": list(ROUND213_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND213_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_watch_triggers": list(ROUND213_STAGE4B_WATCH_TRIGGERS),
        "hard_4c_gates": list(ROUND213_HARD_4C_GATES),
        "what_not_to_change": [
            "do_not_use_round213_cases_as_candidate_generation_input",
            "do_not_apply_shadow_weights_to_production_scoring_yet",
            "do_not_treat_travel_reopening_freight_spike_sdv_story_tourism_policy_or_merger_completion_as_green",
            "do_not_invent_ohlc_or_stage_dates",
        ],
    }


def render_round213_summary_markdown() -> str:
    summary = round213_summary()
    lines = [
        "# Round 213 R9 Loop 8 Mobility Transport Leisure Price Validation",
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
        f"- cyclical_success: {summary['cyclical_success_count']}",
        f"- event_premium: {summary['event_premium_count']}",
        f"- 4c_thesis_break: {summary['thesis_break_count']}",
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
    for case in ROUND213_CASE_CANDIDATES:
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
            "- Hyundai can be a hybrid/value-up Stage 3 candidate, but tariff margin cut remains 4C-watch.",
            "- Kia shows hybrid evidence can still fail price validation when SDV delay, EV target cut, and capex burden appear.",
            "- Korean Air merger completion is Stage 2 until synergy, load factor, yield, debt, and FCF confirm.",
            "- Jeju Air fatal crash is hard 4C and blocks any travel-demand Green.",
            "- HMM and shipping remain cyclical until rate floor, contract mix, FCF, and capital return confirm.",
            "- Hotel Shilla, Paradise, and Lotte Tour are tourism policy/event premium until spend, drop/hold, occupancy, OPM, and FCF appear.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round213_green_gate_review_markdown() -> str:
    lines = [
        "# Round 213 R9 Green Gate Review",
        "",
        "Do not apply these weights to production scoring yet.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND213_GREEN_REQUIRED_FIELDS)
    lines.extend(["", "## Forbidden Patterns", ""])
    lines.extend(f"- {field}" for field in ROUND213_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(
        [
            "",
            "## Easy Example",
            "- `China visa-free tourism policy` means Stage 1/2 routing.",
            "- `tourist spend + casino drop/hold + OPM + FCF` is the bundle that can support Stage 3.",
            "- `fatal airline accident` is hard 4C even if travel demand is recovering.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round213_stage4b_4c_review_markdown() -> str:
    lines = [
        "# Round 213 R9 4B/4C Review",
        "",
        "## 4B Watch Triggers",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND213_STAGE4B_WATCH_TRIGGERS)
    lines.extend(["", "## Hard 4C Gates", ""])
    lines.extend(f"- {field}" for field in ROUND213_HARD_4C_GATES)
    lines.extend(["", "## Case Notes", ""])
    for case in ROUND213_CASE_CANDIDATES:
        if case.stage4b_status == "watch" or case.red_flag_fields:
            lines.append(f"- {case.case_id}: {', '.join(case.red_flag_fields)}")
    return "\n".join(lines) + "\n"


def render_round213_price_validation_plan_markdown() -> str:
    lines = [
        "# Round 213 R9 Price Validation Plan",
        "",
        "- price_validation_completed: partial_with_reported_price_anchors",
        "- full_ohlc_complete: false",
        "- Do not invent OHLC, peak, MFE, or MAE where raw adjusted daily prices are unavailable.",
        "",
        "## Backfill Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND213_PRICE_VALIDATION_FIELDS)
    return "\n".join(lines) + "\n"


def write_round213_r9_loop8_reports(
    output_directory: str | Path = ROUND213_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND213_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND213_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)

    paths = {
        "cases": write_case_library(round213_case_records(), cases_path),
        "audit": _write_json(round213_audit_payload(), audit_path),
        "summary": output / "round213_r9_loop8_price_validation_summary.md",
        "case_matrix": output / "round213_r9_loop8_case_matrix.csv",
        "target_aliases": output / "round213_r9_loop8_target_aliases.csv",
        "score_adjustments": output / "round213_r9_loop8_score_adjustments.csv",
        "price_validation_fields": output / "round213_r9_loop8_price_validation_fields.csv",
        "green_gate_review": output / "round213_r9_loop8_green_gate_review.md",
        "price_validation_plan": output / "round213_r9_loop8_price_validation_plan.md",
        "stage4b_4c_review": output / "round213_r9_loop8_stage4b_4c_review.md",
    }
    paths["summary"].write_text(render_round213_summary_markdown(), encoding="utf-8")
    _write_csv(round213_case_rows(), paths["case_matrix"])
    _write_csv(round213_target_alias_rows(), paths["target_aliases"])
    _write_csv(round213_score_adjustment_rows(), paths["score_adjustments"])
    _write_csv(round213_price_validation_field_rows(), paths["price_validation_fields"])
    paths["green_gate_review"].write_text(render_round213_green_gate_review_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round213_price_validation_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round213_stage4b_4c_review_markdown(), encoding="utf-8")
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
