"""Round-231 R1 Loop-10 industrial orders/infrastructure validation pack.

This pack converts ``docs/round/round_231.md`` into structured,
calibration-only case records. It does not change production scoring.

Easy example: a transformer contract is not enough for Stage 3-Green. The
contract must turn into delivery, revenue, margin, EPS/FCF, and then price-path
confirmation. Hyundai Rotem has a reported delivery/revenue/OP-revision anchor;
LS Electric has strong evidence but a weak event-day price path, so it remains
Stage 2 watch instead of Green.
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


ROUND231_SOURCE_ROUND_PATH = "docs/round/round_231.md"
ROUND231_LARGE_SECTOR = "INDUSTRIAL_ORDERS_INFRA"
ROUND231_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round231_r1_loop10_industrial_orders_infra_price_validation"
ROUND231_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r1_loop10_round231.jsonl"
ROUND231_DEFAULT_AUDIT_PATH = (
    "data/sector_taxonomy/round231_r1_loop10_industrial_orders_infra_price_validation_audit.json"
)

ROUND231_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "GRID_POWER_EQUIPMENT_AI_DATACENTER": E2RArchetype.GRID_POWER_EQUIPMENT_AI_DATACENTER.value,
    "TRANSFORMER_CAPACITY_BOTTLENECK": E2RArchetype.TRANSFORMER_CAPACITY_BOTTLENECK.value,
    "DEFENSE_EXPORT_ORDER_TO_REVENUE": E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG.value,
    "MISSILE_DEFENSE_EXPORT_PLATFORM": E2RArchetype.DEFENSE_INTERCEPTOR_COMBAT_VALIDATION.value,
    "DEFENSE_LOCAL_PRODUCTION_JV": E2RArchetype.DEFENSE_LOCAL_PRODUCTION_PLATFORM.value,
    "CAPITAL_ALLOCATION_DILUTION_OVERLAY": E2RArchetype.CAPITAL_ALLOCATION_DILUTION_OVERLAY.value,
    "OVERSEAS_EPC_CONTRACT_BACKLOG": E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG.value,
    "SAUDI_GAS_INFRA_BACKLOG": E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG_KOREA.value,
    "SHIPBUILDING_US_POLICY_MASGA": E2RArchetype.SHIPBUILDING_US_POLICY_MASGA.value,
    "GEOPOLITICAL_SHIPBUILDING_SANCTION": E2RArchetype.GEOPOLITICAL_SHIPBUILDING_SANCTION.value,
    "CONTRACT_HEADLINE_NOT_STAGE3": E2RArchetype.CONTRACT_HEADLINE_NOT_STAGE3.value,
    "PRICE_ONLY_RALLY": E2RArchetype.PRICE_ONLY_RALLY.value,
}

ROUND231_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "confirmed_contract_amount",
    "contract_duration_or_delivery_schedule",
    "actual_delivery_or_revenue_recognition",
    "opm_eps_or_fcf_revision",
    "backlog_quality",
    "cashflow_or_working_capital_passed",
    "geopolitical_financing_dilution_risk_passed",
    "price_path_after_evidence",
)

ROUND231_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "contract_headline_only",
    "policy_or_mou_without_funded_order",
    "record_high_policy_event",
    "unknown_margin",
    "epc_cash_collection_unknown",
    "local_production_economics_unknown",
    "geopolitical_sanction_unpriced",
    "dilution_after_rerating_ignored",
)

ROUND231_STAGE4B_WATCH_TRIGGERS: tuple[str, ...] = (
    "policy_merger_mou_record_high",
    "preferred_bidder_or_export_headline_after_40_to_70pct_rally",
    "large_order_announcement_day_surge",
    "power_equipment_theme_multiple_before_company_margin",
    "large_equity_cb_or_capex_after_rerating",
    "good_news_with_weak_or_negative_price_response",
)

ROUND231_HARD_4C_GATES: tuple[str, ...] = (
    "contract_cancellation",
    "final_contract_failure",
    "epc_cost_overrun",
    "margin_collapse",
    "working_capital_deterioration",
    "customer_payment_delay",
    "geopolitical_sanction_causing_revenue_disruption",
    "us_china_policy_reversal",
    "local_production_failure",
    "equipment_order_cycle_peak_out",
    "dilution_without_fcf_conversion",
)

ROUND231_PRICE_VALIDATION_FIELDS: tuple[str, ...] = (
    "price_data_source",
    "full_ohlc_available",
    "reported_price_anchor",
    "reported_return_anchor",
    "stage2_price_anchor",
    "stage3_price",
    "stage4b_price",
    "stage4c_price",
    "mfe_1d",
    "mae_1d",
    "contract_value_anchor",
    "delivery_window",
    "target_price_anchor",
    "price_validation_status",
)


@dataclass(frozen=True)
class Round231ScoreAdjustment:
    axis: str
    points: int
    direction: str
    reason: str

    def as_row(self) -> dict[str, str]:
        return {"axis": self.axis, "points": str(self.points), "direction": self.direction, "reason": self.reason}


@dataclass(frozen=True)
class Round231ShadowWeightRow:
    archetype: E2RArchetype
    contract_amount: int
    order_to_revenue: int
    delivery_schedule: int
    backlog_margin: int
    customer_quality: int
    capacity_bottleneck: int
    us_grid_exposure: int
    price_path_alignment: int
    event_penalty: int
    geopolitical_redteam: int
    dilution_redteam: int
    watch_4b_sensitivity: int
    hard_4c_sensitivity: int
    notes: str

    def as_row(self) -> dict[str, str]:
        return {
            "archetype": self.archetype.value,
            "contract_amount": _signed(self.contract_amount),
            "order_to_revenue": _signed(self.order_to_revenue),
            "delivery_schedule": _signed(self.delivery_schedule),
            "backlog_margin": _signed(self.backlog_margin),
            "customer_quality": _signed(self.customer_quality),
            "capacity_bottleneck": _signed(self.capacity_bottleneck),
            "us_grid_exposure": _signed(self.us_grid_exposure),
            "price_path_alignment": _signed(self.price_path_alignment),
            "event_penalty": _signed(self.event_penalty),
            "geopolitical_redteam": _signed(self.geopolitical_redteam),
            "dilution_redteam": _signed(self.dilution_redteam),
            "4b_watch_sensitivity": _signed(self.watch_4b_sensitivity),
            "hard_4c_sensitivity": _signed(self.hard_4c_sensitivity),
            "notes": self.notes,
        }


@dataclass(frozen=True)
class Round231DeepSubArchetype:
    category: str
    primary_archetype: E2RArchetype
    terms: tuple[str, ...]

    def as_row(self) -> dict[str, str]:
        return {"category": self.category, "primary_archetype": self.primary_archetype.value, "terms": "|".join(self.terms)}


@dataclass(frozen=True)
class Round231CaseCandidate:
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


ROUND231_SCORE_ADJUSTMENTS: tuple[Round231ScoreAdjustment, ...] = (
    Round231ScoreAdjustment("confirmed_contract_amount", 5, "raise", "계약금액은 Stage 2 이상의 기본 증거다."),
    Round231ScoreAdjustment("order_to_revenue_conversion", 5, "raise", "수주가 납품·매출로 내려와야 Stage 3 후보가 된다."),
    Round231ScoreAdjustment("delivery_schedule", 4, "raise", "납기와 인도 일정은 visibility를 높인다."),
    Round231ScoreAdjustment("backlog_margin_visibility", 5, "raise", "수주잔고가 마진·현금흐름으로 이어져야 한다."),
    Round231ScoreAdjustment("customer_quality", 4, "raise", "정부·유틸리티·국영 에너지 고객은 계약 신뢰도를 높인다."),
    Round231ScoreAdjustment("capacity_bottleneck", 4, "raise", "변압기 리드타임·CAPA 부족은 구조적 visibility를 보강한다."),
    Round231ScoreAdjustment("us_grid_exposure", 4, "raise", "AI 데이터센터·전력망 노출은 R1 전력기기 후보의 별도 축이다."),
    Round231ScoreAdjustment("price_path_alignment", 5, "raise", "증거 이후 가격경로가 따라오는지 확인해야 한다."),
    Round231ScoreAdjustment("contract_headline_without_margin", -5, "lower", "수주 headline만으로 Stage 3-Green을 주지 않는다."),
    Round231ScoreAdjustment("policy_or_mou_without_order", -5, "lower", "정책·MOU·합병 이벤트는 funded order 전 Green 금지다."),
    Round231ScoreAdjustment("record_high_on_policy_event", -4, "lower", "정책 이벤트 record high는 4B-watch다."),
    Round231ScoreAdjustment("unconfirmed_us_shipbuilding_policy_premium", -4, "lower", "미국 조선정책 프리미엄은 수주와 마진 전 event premium이다."),
    Round231ScoreAdjustment("geopolitical_sanction_unpriced", -4, "lower", "제재 리스크를 무시한 Green을 막는다."),
    Round231ScoreAdjustment("equipment_cycle_without_margin", -3, "lower", "장비 사이클은 마진 확인 전 Yellow/Stage 2에 둔다."),
    Round231ScoreAdjustment("epc_backlog_without_cashflow", -4, "lower", "EPC는 현금회수와 working capital 확인 전 Green 금지다."),
    Round231ScoreAdjustment("dilution_after_rerating", -5, "lower", "리레이팅 후 증자·CB는 4B/capital-allocation watch다."),
    Round231ScoreAdjustment("local_production_margin_unclear", -3, "lower", "현지생산·기술이전은 마진 희석을 확인해야 한다."),
)


ROUND231_SHADOW_WEIGHT_ROWS: tuple[Round231ShadowWeightRow, ...] = (
    Round231ShadowWeightRow(E2RArchetype.GRID_POWER_EQUIPMENT_AI_DATACENTER, 4, 4, 4, 5, 4, 5, 5, 3, -2, 1, 1, 4, 3, "LS Electric has strong U.S. grid evidence, but margin/FCF and price path are required."),
    Round231ShadowWeightRow(E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG, 5, 5, 5, 5, 5, 0, 0, 5, -1, 2, 1, 4, 3, "Hyundai Rotem shows delivery, revenue, and OP revision can support Stage 3."),
    Round231ShadowWeightRow(E2RArchetype.DEFENSE_INTERCEPTOR_COMBAT_VALIDATION, 5, 4, 4, 5, 5, 0, 0, 3, -2, 2, 1, 5, 3, "LIG Nex1 export platform needs 4B-watch after a large 1H rally."),
    Round231ShadowWeightRow(E2RArchetype.DEFENSE_LOCAL_PRODUCTION_PLATFORM, 4, 4, 5, 5, 5, 0, 0, 3, -3, 2, 5, 5, 4, "Localization/JV is Stage 2; dilution after rerating is 4B-watch."),
    Round231ShadowWeightRow(E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG, 5, 4, 4, 5, 5, 0, 0, 4, -3, 2, 2, 4, 4, "Fadhili EPC is Stage 2; margin and cash collection are required."),
    Round231ShadowWeightRow(E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG_KOREA, 5, 4, 4, 5, 5, 0, 0, 2, -3, 2, 1, 3, 4, "Jafurah gas infra is Stage 2 until margin and cash recovery confirm."),
    Round231ShadowWeightRow(E2RArchetype.SHIPBUILDING_US_POLICY_MASGA, 4, 3, 4, 5, 4, 2, 0, 3, -5, 3, 1, 5, 4, "MASGA/merger record highs are Stage 2 plus 4B-watch until funded orders confirm."),
    Round231ShadowWeightRow(E2RArchetype.GEOPOLITICAL_SHIPBUILDING_SANCTION, 0, 0, 0, 0, 0, 0, 0, 2, 0, 5, 1, 3, 5, "China sanctions are 4C-watch; hard 4C requires actual revenue or contract disruption."),
)


ROUND231_DEEP_SUB_ARCHETYPES: tuple[Round231DeepSubArchetype, ...] = (
    Round231DeepSubArchetype("power equipment / transformer", E2RArchetype.GRID_POWER_EQUIPMENT_AI_DATACENTER, ("LS Electric", "U.S. transformer shortage", "AI data center", "525kV EHV transformer", "delivery 2027-2029")),
    Round231DeepSubArchetype("defense order to revenue", E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG, ("Hyundai Rotem", "K2 Poland", "delivery", "revenue", "OP revision")),
    Round231DeepSubArchetype("missile defense export", E2RArchetype.DEFENSE_INTERCEPTOR_COMBAT_VALIDATION, ("LIG Nex1", "Cheongung-II", "M-SAM", "Iraq", "Saudi", "crowding watch")),
    Round231DeepSubArchetype("defense localization dilution", E2RArchetype.DEFENSE_LOCAL_PRODUCTION_PLATFORM, ("Hanwha Aerospace", "Poland missile JV", "K239 Chunmoo", "technology transfer", "dilution")),
    Round231DeepSubArchetype("overseas EPC backlog", E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG, ("Samsung E&A", "GS E&C", "Fadhili", "EPC margin", "cash collection")),
    Round231DeepSubArchetype("Saudi gas infra", E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG_KOREA, ("Hyundai E&C", "Jafurah", "gas network", "pipeline", "sovereign EPC")),
    Round231DeepSubArchetype("shipbuilding policy/MASGA", E2RArchetype.SHIPBUILDING_US_POLICY_MASGA, ("HD Hyundai Heavy", "HD Hyundai Mipo", "MASGA", "merger", "funded order required")),
    Round231DeepSubArchetype("geopolitical shipbuilding sanction", E2RArchetype.GEOPOLITICAL_SHIPBUILDING_SANCTION, ("Hanwha Ocean", "China sanctions", "U.S.-linked subsidiaries", "4C-watch")),
)


ROUND231_CASE_CANDIDATES: tuple[Round231CaseCandidate, ...] = (
    Round231CaseCandidate(
        case_id="r1_loop10_ls_electric_grid_transformer_price_failed",
        symbol="010120",
        company_name="LS ELECTRIC",
        primary_archetype=E2RArchetype.GRID_POWER_EQUIPMENT_AI_DATACENTER,
        secondary_archetypes=(E2RArchetype.POWER_EQUIPMENT_EXPORT_US_GRID, E2RArchetype.TRANSFORMER_CAPACITY_BOTTLENECK),
        case_type="success_candidate",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2024, 7, 1),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="strong_us_grid_transformer_evidence_but_event_day_price_failed_and_margin_fcf_unverified",
        stage4b_status="4B-watch-if-theme-multiple-prepays-delivery-margin",
        hard_4c_confirmed=False,
        evidence_fields=("us_data_center_grid_demand", "target_price_raise_86_7pct", "us_revenue_share_expected_20pct", "312m_usd_utility_transformer_contract", "525kv_ehv_transformers", "delivery_2027_2029"),
        red_flag_fields=("event_day_price_failed_minus_5_4pct", "margin_fcf_unverified", "transformer_price_normalization_risk", "project_delay_risk"),
        price_data_source="MarketWatch price/target anchor + Reuters transformer-sector contract anchor",
        reported_price_anchor="208,500 KRW on 2024-07-01; target 280,000 KRW",
        reported_return_anchor="-5.4% event-day MAE; target upside +34.3%; target raise +86.7%",
        mfe_1d=None,
        mae_1d=-5.4,
        stage2_price_anchor=208500.0,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        peak_return_from_stage3_pct=None,
        extra_price_metrics={"target_price": 280000.0, "target_upside_from_stage2_price_pct": 34.3, "target_raise_pct": 86.7, "us_revenue_share_2024_expected_pct": 20.0, "us_revenue_share_2022_max_pct": 5.0, "minimum_relative_mix_increase_pct": 300.0, "us_utility_transformer_contract_usd_mn": 312.0, "gsu_transformer_demand_growth_since_2019_pct": 274.0, "substation_transformer_demand_growth_since_2019_pct": 116.0, "transformer_price_increase_5y_pct": 80.0, "large_transformer_lead_time_years": 4.0},
        score_price_alignment="evidence_good_but_price_failed",
        round_alignment_label="evidence_good_but_price_failed",
        rerating_result="unknown",
        round_rerating_label="U.S._grid_power_equipment_watch",
        stage_failure_type="stage2_watch_success",
        round_stage_failure_label="stage2_watch_not_green",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="Strong grid/data-center evidence and company contract, but event price failed; Stage 3 requires delivery, margin and FCF.",
    ),
    Round231CaseCandidate(
        case_id="r1_loop10_hyundai_rotem_k2_export_aligned",
        symbol="064350",
        company_name="Hyundai Rotem",
        primary_archetype=E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,
        secondary_archetypes=(E2RArchetype.DEFENSE_LOCAL_PRODUCTION_PLATFORM, E2RArchetype.RAIL_INFRASTRUCTURE),
        case_type="structural_success",
        stage1_date=date(2022, 1, 1),
        stage2_date=date(2024, 4, 9),
        stage3_date=date(2024, 4, 9),
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="k2_delivery_revenue_and_op_revision_confirm_order_to_revenue_stage3_candidate",
        stage4b_status="4B-watch-if-second_batch_or_latin_america_price_prepaid",
        hard_4c_confirmed=False,
        evidence_fields=("k2_18_units_delivered_to_poland", "k2_export_revenue_270bn_krw", "op_growth_estimate_85pct_yoy", "poland_second_contract_6_5bn_usd", "peru_framework_195_units"),
        red_flag_fields=("local_production_delay_risk", "technology_transfer_margin_dilution", "payment_risk", "delivery_delay_risk"),
        price_data_source="WSJ / Reuters reported price and contract anchors",
        reported_price_anchor="41,300 KRW on 2024-04-09; KB target 47,500 KRW",
        reported_return_anchor="+9.3% event MFE; KOSPI -0.3%; relative +9.6pp",
        mfe_1d=9.3,
        mae_1d=None,
        stage2_price_anchor=41300.0,
        stage3_price_anchor=41300.0,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        peak_return_from_stage3_pct=None,
        extra_price_metrics={"implied_pre_event_reference_price": 37786.0, "kospi_same_context_return_pct": -0.3, "relative_outperformance_vs_kospi_pp": 9.6, "k2_export_revenue_1q_krw_bn": 270.0, "op_growth_estimate_pct": 85.0, "kb_target_price": 47500.0, "target_upside_from_stage3_price_pct": 15.0, "poland_second_contract_usd_bn": 6.5, "poland_second_contract_units": 180.0, "poland_local_production_units": 61.0, "peru_framework_units_total": 195.0},
        score_price_alignment="aligned",
        round_alignment_label="aligned_partial",
        rerating_result="true_rerating",
        round_rerating_label="defense_export_revenue_conversion",
        stage_failure_type="green_success",
        round_stage_failure_label="green_success_candidate",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="K2 delivery/revenue/OP revision makes this a Stage 3 candidate; follow-up Poland/Peru contracts support continuation.",
    ),
    Round231CaseCandidate(
        case_id="r1_loop10_lig_nex1_cheongung_export_crowding",
        symbol="079550",
        company_name="LIG Nex1",
        primary_archetype=E2RArchetype.DEFENSE_INTERCEPTOR_COMBAT_VALIDATION,
        secondary_archetypes=(E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG, E2RArchetype.CROWDED_RERATING_4B_WATCH),
        case_type="success_candidate",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2024, 9, 20),
        stage3_date=None,
        stage4b_date=date(2024, 7, 2),
        stage4c_date=None,
        stage3_decision="large_missile_export_validates_stage2_but_delivery_margin_cash_collection_and_eps_revision_required",
        stage4b_status="4B-watch",
        hard_4c_confirmed=False,
        evidence_fields=("iraq_contract_3_71tn_krw", "iraq_contract_2_8bn_usd", "cheongung_msam_export", "saudi_prior_contract_3_2bn_usd", "q2_op_growth_estimate_40pct"),
        red_flag_fields=("first_half_2024_stock_gain_69pct", "downgrade_after_crowding", "stage4b_event_mae_minus_11pct", "delivery_delay_or_payment_risk"),
        price_data_source="Reuters / MarketWatch reported price and contract anchors",
        reported_price_anchor="195,700 KRW close after 4B/crowding event",
        reported_return_anchor="Iraq order +3.6%; 1H stock +69%; downgrade event -11%",
        mfe_1d=3.6,
        mae_1d=-11.0,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=195700.0,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        peak_return_from_stage3_pct=None,
        extra_price_metrics={"iraq_contract_krw_trn": 3.71, "iraq_contract_usd_bn": 2.8, "saudi_prior_contract_usd_bn": 3.2, "wider_market_same_context_pct": 0.9, "relative_outperformance_pp": 2.7, "first_half_2024_stock_gain_pct": 69.0, "kospi_first_half_2024_gain_pct": 5.4, "first_half_relative_outperformance_pp": 63.6, "implied_pre_4b_reference_price": 219888.0, "q2_op_estimate_krw_bn": 56.2, "q2_op_growth_estimate_pct": 40.0, "target_price": 200000.0},
        score_price_alignment="aligned",
        round_alignment_label="success_candidate_4B_watch",
        rerating_result="unknown",
        round_rerating_label="missile_defense_export_platform_watch",
        stage_failure_type="stage2_watch_success",
        round_stage_failure_label="stage2_watch_success_with_crowding",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="Iraq export validates Stage 2, but 1H +69% and downgrade selloff show 4B/crowding risk.",
    ),
    Round231CaseCandidate(
        case_id="r1_loop10_hanwha_aerospace_poland_missile_jv_dilution_watch",
        symbol="012450",
        company_name="Hanwha Aerospace",
        primary_archetype=E2RArchetype.DEFENSE_LOCAL_PRODUCTION_PLATFORM,
        secondary_archetypes=(E2RArchetype.CAPITAL_ALLOCATION_DILUTION_OVERLAY, E2RArchetype.DEFENSE_CAPITAL_ALLOCATION_SHOCK),
        case_type="success_candidate",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2025, 4, 15),
        stage3_date=None,
        stage4b_date=date(2025, 3, 21),
        stage4c_date=None,
        stage3_decision="poland_missile_jv_is_stage2_but_order_volume_margin_delivery_and_cash_collection_required",
        stage4b_status="4B-watch",
        hard_4c_confirmed=False,
        evidence_fields=("poland_missile_jv", "cgr_080_guided_missiles", "k239_chunmoo_system", "local_production_model", "technology_transfer"),
        red_flag_fields=("capital_raise_3_6tn_krw", "capital_raise_event_mae_minus_13pct", "dilution_after_rerating", "local_production_margin_unclear"),
        price_data_source="Reuters / FT reported event and capital-raising anchors",
        reported_price_anchor="Affiliate issue price 758,000 KRW/share; event price path reported as -13%",
        reported_return_anchor="3.6T KRW capital raise caused -13% selloff",
        mfe_1d=None,
        mae_1d=-13.0,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        peak_return_from_stage3_pct=None,
        extra_price_metrics={"capital_raise_initial_krw_trn": 3.6, "capital_raise_initial_usd_bn": 2.46, "affiliate_share_issue_krw_trn": 1.3, "rights_offering_krw_trn": 2.3, "total_revised_raise_krw_trn": 3.6, "affiliate_issue_price_krw": 758000.0},
        score_price_alignment="aligned",
        round_alignment_label="success_candidate_aligned_4B_detection",
        rerating_result="unknown",
        round_rerating_label="defense_localization_watch_with_dilution",
        stage_failure_type="stage2_watch_success",
        round_stage_failure_label="4B_watch_not_hard_4C",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="Poland missile JV is Stage 2; large capital raise after rerating is 4B/dilution watch, not hard 4C.",
    ),
    Round231CaseCandidate(
        case_id="r1_loop10_samsung_ea_gs_fadhili_epc",
        symbol="028050/006360",
        company_name="Samsung E&A / GS E&C",
        primary_archetype=E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG,
        secondary_archetypes=(E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG_KOREA, E2RArchetype.EPC_LOW_MARGIN_ORDER_OVERLAY),
        case_type="success_candidate",
        stage1_date=date(2024, 4, 2),
        stage2_date=date(2024, 4, 3),
        stage3_date=None,
        stage4b_date=date(2024, 4, 3),
        stage4c_date=None,
        stage3_decision="fadhili_epc_is_stage2_but_margin_progress_revenue_cash_collection_and_working_capital_required",
        stage4b_status="4B-watch",
        hard_4c_confirmed=False,
        evidence_fields=("aramco_fadhili_contracts_7_7bn_usd", "samsung_ea_contract_estimate_6bn_usd", "fadhili_capacity_increase_60pct", "state_customer"),
        red_flag_fields=("epc_margin_unknown", "cash_collection_unknown", "working_capital_risk", "event_day_rally_not_stage3"),
        price_data_source="Reuters / WSJ reported contract and price anchors",
        reported_price_anchor="Samsung E&A 26,750 KRW event peak; KB target 35,000 KRW",
        reported_return_anchor="+8.5% event MFE; KOSPI -1.4%; relative +9.9pp",
        mfe_1d=8.5,
        mae_1d=None,
        stage2_price_anchor=26750.0,
        stage3_price_anchor=None,
        stage4b_price_anchor=26750.0,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        peak_return_from_stage3_pct=None,
        extra_price_metrics={"implied_pre_event_reference_price": 24654.0, "kospi_same_context_pct": -1.4, "relative_outperformance_vs_kospi_pp": 9.9, "aramco_total_fadhili_contracts_usd_bn": 7.7, "samsung_ea_contract_estimate_usd_bn": 6.0, "samsung_share_of_total_project_pct": 77.9, "fadhili_capacity_before_bscfd": 2.5, "fadhili_capacity_after_bscfd": 4.0, "capacity_increase_pct": 60.0, "kb_target_price": 35000.0, "target_upside_from_event_peak_pct": 30.8},
        score_price_alignment="aligned",
        round_alignment_label="success_candidate",
        rerating_result="event_premium",
        round_rerating_label="EPC_backlog_watch",
        stage_failure_type="stage2_watch_success",
        round_stage_failure_label="stage2_watch_success",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="Large EPC contract is Stage 2; Stage 3 requires margin, progress revenue, cash collection and working-capital control.",
    ),
    Round231CaseCandidate(
        case_id="r1_loop10_hyundai_ec_jafurah_gas_infra",
        symbol="000720",
        company_name="Hyundai E&C",
        primary_archetype=E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG_KOREA,
        secondary_archetypes=(E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG, E2RArchetype.EPC_LOW_MARGIN_ORDER_OVERLAY),
        case_type="success_candidate",
        stage1_date=date(2024, 6, 1),
        stage2_date=date(2024, 6, 30),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="sovereign_gas_infra_epc_is_stage2_but_margin_progress_revenue_and_cash_recovery_required",
        stage4b_status="4B-watch-if_middle_east_epc_expectation_prepays_margin",
        hard_4c_confirmed=False,
        evidence_fields=("aramco_package_above_25bn_usd", "jafurah_expansion", "main_gas_network_4000km_pipeline", "added_capacity_3_2_bscfd", "sovereign_customer"),
        red_flag_fields=("company_price_path_unavailable", "epc_margin_unknown", "payment_delay_risk", "cost_overrun_risk"),
        price_data_source="Reuters contract / infrastructure evidence",
        reported_price_anchor="Reuters did not provide Hyundai E&C stock reaction anchor",
        reported_return_anchor="Aramco package >$25B; gas network +4,000km and +3.2B scf/day",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        peak_return_from_stage3_pct=None,
        extra_price_metrics={"aramco_contract_package_usd_bn_min": 25.0, "jafurah_reserves_tcf": 229.0, "jafurah_condensates_bbl_bn": 75.0, "jafurah_sales_gas_target_bscfd": 2.0, "main_gas_network_added_capacity_bscfd": 3.2, "main_gas_network_added_pipeline_km": 4000.0},
        score_price_alignment="unknown",
        round_alignment_label="success_candidate",
        rerating_result="unknown",
        round_rerating_label="Saudi_gas_infra_backlog_watch",
        stage_failure_type="stage2_watch_success",
        round_stage_failure_label="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Sovereign gas-infra contract is Stage 2; margin, progress revenue and cash recovery required before Green.",
    ),
    Round231CaseCandidate(
        case_id="r1_loop10_hd_hyundai_heavy_mipo_masga_event",
        symbol="329180/010620",
        company_name="HD Hyundai Heavy / HD Hyundai Mipo",
        primary_archetype=E2RArchetype.SHIPBUILDING_US_POLICY_MASGA,
        secondary_archetypes=(E2RArchetype.SHIPBUILDING_US_PLATFORM_RESTRUCTURING, E2RArchetype.MOU_LOI_NOT_CONTRACT),
        case_type="success_candidate",
        stage1_date=date(2025, 8, 1),
        stage2_date=date(2025, 8, 27),
        stage3_date=None,
        stage4b_date=date(2025, 8, 27),
        stage4c_date=None,
        stage3_decision="masga_merger_policy_event_is_stage2_and_4b_watch_until_funded_us_order_margin_and_fcf_confirm",
        stage4b_status="4B-watch",
        hard_4c_confirmed=False,
        evidence_fields=("us_korea_shipbuilding_cooperation", "masga_policy", "hd_hyundai_heavy_mipo_merger", "us_shipbuilding_market_target"),
        red_flag_fields=("record_high_policy_event", "funded_order_missing", "margin_missing", "integration_cost_risk"),
        price_data_source="Reuters reported event return anchor",
        reported_price_anchor="Record highs; share exchange ratio 1 Mipo = 1.04059146 Heavy",
        reported_return_anchor="HD Hyundai Heavy +11.3%; HD Hyundai Mipo +14.6%",
        mfe_1d=14.6,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        peak_return_from_stage3_pct=None,
        extra_price_metrics={"hd_hyundai_heavy_event_mfe_1d_pct": 11.3, "hd_hyundai_mipo_event_mfe_1d_pct": 14.6, "record_high_status": True, "share_exchange_ratio_mipo_per_heavy": 1.04059146},
        score_price_alignment="price_moved_without_evidence",
        round_alignment_label="event_premium_success_candidate",
        rerating_result="event_premium",
        round_rerating_label="U.S._shipbuilding_policy_watch",
        stage_failure_type="stage2_watch_success",
        round_stage_failure_label="stage2_watch_success",
        price_validation_status="reported_event_return_not_full_ohlc",
        notes="Merger/MASGA is Stage 2 and 4B-watch; funded order and margin required for Stage 3.",
    ),
    Round231CaseCandidate(
        case_id="r1_loop10_hanwha_ocean_china_sanction_watch",
        symbol="042660",
        company_name="Hanwha Ocean",
        primary_archetype=E2RArchetype.GEOPOLITICAL_SHIPBUILDING_SANCTION,
        secondary_archetypes=(E2RArchetype.GEOPOLITICAL_SHIPBUILDING_SANCTION_OVERLAY, E2RArchetype.DEFENSE_US_SHIPBUILDING_PLATFORM),
        case_type="4c_thesis_break",
        stage1_date=date(2024, 1, 1),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 10, 14),
        stage3_decision="us_shipbuilding_policy_and_mro_exposure_are_not_green_when_geopolitical_sanction_watch_is_present",
        stage4b_status="4C-watch-not-hard-4C",
        hard_4c_confirmed=False,
        evidence_fields=("philly_shipyard_acquisition", "us_shipbuilding_rebuild_exposure", "us_investment_plan_5bn_usd"),
        red_flag_fields=("china_sanctions_five_us_linked_subsidiaries", "transactions_cooperation_ban", "event_close_mae_minus_5_8pct", "actual_revenue_disruption_unconfirmed"),
        price_data_source="Reuters / AP reported event-return and investment anchors",
        reported_price_anchor="Hanwha Ocean close -5.8% after China sanctions",
        reported_return_anchor="China sanctioned five U.S.-linked subsidiaries; U.S. investment plan $5B",
        mfe_1d=None,
        mae_1d=-5.8,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        peak_return_from_stage3_pct=None,
        extra_price_metrics={"philly_shipyard_acquisition_usd_mn": 100.0, "announced_us_investment_usd_bn": 5.0, "investment_vs_acquisition_multiple": 50.0, "sanctioned_entities": 5.0, "hard_4c_confirmed": False},
        score_price_alignment="evidence_good_but_price_failed",
        round_alignment_label="thesis_break_watch",
        rerating_result="thesis_break",
        round_rerating_label="geopolitical_sanction_watch",
        stage_failure_type="should_have_been_red",
        round_stage_failure_label="4C_watch_not_hard_4C",
        price_validation_status="reported_event_return_not_full_ohlc",
        notes="China sanctions are 4C-watch; hard 4C requires actual revenue or contract disruption.",
    ),
)


def round231_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    stage3_terms = ("delivery", "revenue", "op_revision", "eps", "fcf", "margin", "cash", "price")
    for candidate in ROUND231_CASE_CANDIDATES:
        record = E2RCaseRecord(
            case_id=candidate.case_id,
            symbol=candidate.symbol,
            company_name=candidate.company_name,
            market="KR",
            sector_raw=candidate.primary_archetype.value,
            primary_archetype=candidate.primary_archetype,
            secondary_archetypes=candidate.secondary_archetypes,
            expected_group=candidate.expected_group,
            large_sector=ROUND231_LARGE_SECTOR,
            case_type=candidate.case_type,
            stage1_date=candidate.stage1_date,
            stage2_date=candidate.stage2_date,
            stage3_date=candidate.stage3_date,
            stage4b_date=candidate.stage4b_date,
            stage4c_date=candidate.stage4c_date,
            evidence_summary=(
                "Round231 R1 Loop-10 industrial orders/infrastructure price validation case. "
                "Calibration-only; not production scoring input."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=candidate.evidence_fields if candidate.stage2_date else (),
            stage3_evidence=tuple(field for field in candidate.evidence_fields if any(term in field.lower() for term in stage3_terms)),
            stage4b_evidence=tuple(field for field in (*candidate.evidence_fields, *candidate.red_flag_fields) if "4b" in field.lower() or "rally" in field.lower() or "event" in field.lower() or "record" in field.lower() or "dilution" in field.lower()),
            stage4c_evidence=tuple(field for field in candidate.red_flag_fields if "sanction" in field.lower() or "delay" in field.lower() or "risk" in field.lower() or "collapse" in field.lower() or "cancellation" in field.lower() or "disruption" in field.lower()),
            must_have_fields=ROUND231_GREEN_REQUIRED_FIELDS,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason="; ".join(candidate.red_flag_fields) if candidate.case_type in {"event_premium", "overheat", "failed_rerating", "4b_watch", "4c_thesis_break"} else None,
            score_price_alignment=candidate.score_price_alignment,
            rerating_result=candidate.rerating_result,
            stage_failure_type=candidate.stage_failure_type,
            price_pattern=candidate.stage3_decision,
            score_weight_hint={f"{item.axis}_delta": float(item.points) for item in ROUND231_SCORE_ADJUSTMENTS},
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "full_ohlc_complete_false",
                "price_validation_partial_with_reported_price_anchors",
                "do_not_invent_price_or_stage_dates",
                "do_not_treat_contract_policy_mou_or_record_high_as_green_alone",
                *ROUND231_GREEN_REQUIRED_FIELDS,
                *ROUND231_GREEN_FORBIDDEN_PATTERNS,
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
                stage_dates_confidence=0.85 if candidate.stage3_date else 0.75,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round231_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND231_CASE_CANDIDATES:
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
                "stage2_price_anchor": _float_text(candidate.stage2_price_anchor),
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


def round231_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND231_SCORE_ADJUSTMENTS)


def round231_shadow_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(row.as_row() for row in ROUND231_SHADOW_WEIGHT_ROWS)


def round231_deep_sub_archetype_rows() -> tuple[dict[str, str], ...]:
    return tuple(row.as_row() for row in ROUND231_DEEP_SUB_ARCHETYPES)


def round231_price_validation_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round231_price_validation": "true"} for field in ROUND231_PRICE_VALIDATION_FIELDS)


def round231_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple({"round231_label": label, "canonical_archetype": canonical} for label, canonical in ROUND231_REQUIRED_TARGET_ALIASES.items())


def round231_summary() -> dict[str, int | bool | str]:
    cases = ROUND231_CASE_CANDIDATES
    return {
        "source_round": ROUND231_SOURCE_ROUND_PATH,
        "large_sector": ROUND231_LARGE_SECTOR,
        "case_candidate_count": len(cases),
        "structural_success_count": sum(1 for case in cases if case.case_type == "structural_success"),
        "success_candidate_count": sum(1 for case in cases if case.case_type == "success_candidate"),
        "event_premium_count": sum(1 for case in cases if case.rerating_result == "event_premium"),
        "thesis_break_watch_count": sum(1 for case in cases if "thesis_break" in case.round_alignment_label or case.rerating_result == "thesis_break"),
        "hard_4c_case_count": sum(1 for case in cases if case.hard_4c_confirmed),
        "stage3_case_count": sum(1 for case in cases if case.stage3_date is not None),
        "stage4b_watch_count": sum(1 for case in cases if "4B" in case.stage4b_status),
        "price_failed_count": sum(1 for case in cases if case.score_price_alignment == "evidence_good_but_price_failed"),
        "target_archetype_count": len(ROUND231_REQUIRED_TARGET_ALIASES),
        "deep_sub_archetype_count": len(ROUND231_DEEP_SUB_ARCHETYPES),
        "shadow_weight_row_count": len(ROUND231_SHADOW_WEIGHT_ROWS),
        "price_validation_completed": "partial_with_reported_price_anchors",
        "full_ohlc_complete": False,
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
    }


def round231_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND231_SOURCE_ROUND_PATH,
        "large_sector": ROUND231_LARGE_SECTOR,
        "summary": round231_summary(),
        "target_aliases": dict(ROUND231_REQUIRED_TARGET_ALIASES),
        "green_required_fields": list(ROUND231_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND231_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_watch_triggers": list(ROUND231_STAGE4B_WATCH_TRIGGERS),
        "hard_4c_gates": list(ROUND231_HARD_4C_GATES),
        "deep_sub_archetypes": round231_deep_sub_archetype_rows(),
        "shadow_weights": round231_shadow_weight_rows(),
        "what_not_to_change": [
            "do_not_use_round231_cases_as_candidate_generation_input",
            "do_not_apply_shadow_weights_to_production_scoring_yet",
            "do_not_treat_contract_policy_mou_record_high_or_epc_headline_as_green",
            "do_not_invent_ohlc_or_stage_dates",
        ],
    }


def render_round231_summary_markdown() -> str:
    summary = round231_summary()
    lines = [
        "# Round 231 R1 Loop 10 Industrial Orders / Infrastructure Price Validation",
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
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- thesis_break_watch_count: {summary['thesis_break_watch_count']}",
        f"- Stage 3 dated cases: {summary['stage3_case_count']}",
        f"- 4B-watch cases: {summary['stage4b_watch_count']}",
        f"- price_failed_count: {summary['price_failed_count']}",
        f"- full_ohlc_complete: {str(summary['full_ohlc_complete']).lower()}",
        "",
        "## Case Matrix",
        "",
        "| case | company | type | stage3 | 4B | 4C | round alignment | note |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for case in ROUND231_CASE_CANDIDATES:
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
            "- Hyundai Rotem is the cleanest R1 order-to-revenue Stage 3 candidate because delivery, revenue, OP revision, and price reaction align.",
            "- LS Electric is strong Stage 2 watch, but event-day price failure and unverified margin/FCF block Green.",
            "- LIG Nex1 and Hanwha Aerospace prove that good defense export evidence still needs 4B/crowding and dilution watch.",
            "- Samsung E&A, GS E&C, and Hyundai E&C are EPC Stage 2 cases until margin, progress revenue, cash collection, and working capital confirm.",
            "- HD Hyundai Heavy/Mipo MASGA is a policy/merger event premium before funded U.S. order and margin evidence.",
            "- Hanwha Ocean is geopolitical 4C-watch, not hard 4C, until actual revenue or contract disruption is confirmed.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round231_green_gate_review_markdown() -> str:
    lines = [
        "# Round 231 R1 Green Gate Review",
        "",
        "Do not apply these weights to production scoring yet.",
        "",
        "R1 Stage 3-Green means order -> delivery -> revenue -> margin -> EPS/FCF. A contract headline alone is not enough.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND231_GREEN_REQUIRED_FIELDS)
    lines.extend(["", "## Forbidden Patterns", ""])
    lines.extend(f"- {field}" for field in ROUND231_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(
        [
            "",
            "## Easy Example",
            "- `K2 delivery + revenue + OP revision + price reaction` can become a Stage 3 candidate.",
            "- `$312M transformer contract + event-day price -5.4%` stays Stage 2 watch until margin/FCF confirm.",
            "- `MASGA merger record high` is 4B-watch until funded orders and margin appear.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round231_stage4b_4c_review_markdown() -> str:
    lines = ["# Round 231 R1 4B/4C Review", "", "## 4B Watch Triggers", ""]
    lines.extend(f"- {field}" for field in ROUND231_STAGE4B_WATCH_TRIGGERS)
    lines.extend(["", "## Hard 4C Gates", ""])
    lines.extend(f"- {field}" for field in ROUND231_HARD_4C_GATES)
    lines.extend(
        [
            "",
            "## Plain-Language Gate Notes",
            "",
            "- 4B catches event premium, crowding, record highs, and dilution after rerating.",
            "- 4C catches thesis breaks such as contract cancellation, margin collapse, payment delay, and sanction-driven revenue disruption.",
            "- Hanwha Ocean is 4C-watch here because sanction exists, but revenue disruption is not yet confirmed.",
            "",
            "## Case Notes",
            "",
        ]
    )
    for case in ROUND231_CASE_CANDIDATES:
        if "4B" in case.stage4b_status or case.stage4c_date or case.red_flag_fields:
            lines.append(f"- {case.case_id}: {', '.join(case.red_flag_fields)}")
    return "\n".join(lines) + "\n"


def render_round231_price_validation_plan_markdown() -> str:
    lines = [
        "# Round 231 R1 Price Validation Plan",
        "",
        "- price_validation_completed: partial_with_reported_price_anchors",
        "- full_ohlc_complete: false",
        "- Do not invent OHLC, peak, MFE, or MAE where raw adjusted daily prices are unavailable.",
        "",
        "## Backfill Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in ROUND231_PRICE_VALIDATION_FIELDS)
    return "\n".join(lines) + "\n"


def write_round231_r1_loop10_reports(
    output_directory: str | Path = ROUND231_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND231_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND231_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "cases": write_case_library(round231_case_records(), cases_path),
        "audit": _write_json(round231_audit_payload(), audit_path),
        "summary": output / "round231_r1_loop10_price_validation_summary.md",
        "case_matrix": output / "round231_r1_loop10_case_matrix.csv",
        "target_aliases": output / "round231_r1_loop10_target_aliases.csv",
        "score_adjustments": output / "round231_r1_loop10_score_adjustments.csv",
        "shadow_weights": output / "round231_r1_loop10_shadow_weights.csv",
        "deep_sub_archetypes": output / "round231_r1_loop10_deep_sub_archetypes.csv",
        "price_validation_fields": output / "round231_r1_loop10_price_validation_fields.csv",
        "green_gate_review": output / "round231_r1_loop10_green_gate_review.md",
        "price_validation_plan": output / "round231_r1_loop10_price_validation_plan.md",
        "stage4b_4c_review": output / "round231_r1_loop10_stage4b_4c_review.md",
    }
    paths["summary"].write_text(render_round231_summary_markdown(), encoding="utf-8")
    _write_csv(round231_case_rows(), paths["case_matrix"])
    _write_csv(round231_target_alias_rows(), paths["target_aliases"])
    _write_csv(round231_score_adjustment_rows(), paths["score_adjustments"])
    _write_csv(round231_shadow_weight_rows(), paths["shadow_weights"])
    _write_csv(round231_deep_sub_archetype_rows(), paths["deep_sub_archetypes"])
    _write_csv(round231_price_validation_field_rows(), paths["price_validation_fields"])
    paths["green_gate_review"].write_text(render_round231_green_gate_review_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round231_price_validation_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round231_stage4b_4c_review_markdown(), encoding="utf-8")
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
