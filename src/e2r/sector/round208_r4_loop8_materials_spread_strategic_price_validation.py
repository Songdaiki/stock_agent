"""Round-208 R4 Loop-8 materials/spread/strategic-resources price validation.

Round 208 is calibration/evaluation material only. It captures reported price
anchors, event returns, and financial anchors from ``docs/round/round_208.md``.

Simple example: a critical-minerals plant can be useful Stage 2 evidence. It is
not Stage 3-Green until offtake, price floor, cost curve, FCF, capex burden,
dilution risk, and price-path confirmation are visible as-of the replay date.
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


ROUND208_SOURCE_ROUND_PATH = "docs/round/round_208.md"
ROUND208_LARGE_SECTOR = Round10LargeSector.MATERIALS_SPREAD_STRATEGIC
ROUND208_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round208_r4_loop8_materials_spread_strategic_price_validation"
ROUND208_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r4_loop8_round208.jsonl"
ROUND208_DEFAULT_AUDIT_PATH = "data/sector_taxonomy/round208_r4_loop8_materials_spread_strategic_price_validation_audit.json"

ROUND208_REQUIRED_TARGET_ALIASES: Mapping[str, str] = {
    "REFINING_OIL_SPREAD": E2RArchetype.REFINING_OIL_SPREAD.value,
    "CHEMICAL_SPREAD": E2RArchetype.CHEMICAL_SPREAD.value,
    "PETROCHEMICAL_RESTRUCTURING_KOREA": E2RArchetype.PETROCHEMICAL_RESTRUCTURING_KOREA.value,
    "COMMODITY_SPREAD_CYCLE_NOT_STRUCTURAL": E2RArchetype.COMMODITY_SPREAD_CYCLE_NOT_STRUCTURAL.value,
    "NONFERROUS_STRATEGIC_METALS": E2RArchetype.NONFERROUS_STRATEGIC_METALS.value,
    "RARE_METALS_STRATEGIC_MATERIALS": E2RArchetype.RARE_METALS_STRATEGIC_MATERIALS.value,
    "RARE_METALS_PRICE_FLOOR_OFFTAKE": E2RArchetype.RARE_METALS_PRICE_FLOOR_OFFTAKE.value,
    "LITHIUM_BATTERY_RAW_MATERIAL": E2RArchetype.LITHIUM_BATTERY_RAW_MATERIAL.value,
    "LITHIUM_CYCLE_OVERLAY": E2RArchetype.LITHIUM_CYCLE_OVERLAY.value,
    "POLYSILICON_NON_CHINA_SUPPLY_OPTION": E2RArchetype.POLYSILICON_NON_CHINA_SUPPLY_OPTION.value,
    "COPPER_PROCESSING_PLUS_DEFENSE": E2RArchetype.COPPER_PROCESSING_PLUS_DEFENSE.value,
    "EVENT_PREMIUM_GOVERNANCE_OVERLAY": E2RArchetype.EVENT_PREMIUM_GOVERNANCE_OVERLAY.value,
    "COMMODITY_PRICE_4C_OVERLAY": E2RArchetype.COMMODITY_PRICE_4C_OVERLAY.value,
}

ROUND208_GREEN_REQUIRED_FIELDS: tuple[str, ...] = (
    "actual_product_spread",
    "cost_curve_advantage",
    "supply_discipline_or_capacity_shutdown",
    "inventory_build_absent",
    "fcf_after_working_capital",
    "price_floor_or_offtake",
    "medium_term_eps_revision",
    "capex_and_dilution_risk_passed",
    "price_path_after_evidence",
)

ROUND208_GREEN_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "commodity_price_spike_only",
    "tender_offer_premium",
    "governance_battle_only",
    "policy_support_without_fcf",
    "unconfirmed_media_report",
    "restructuring_plan_without_margin",
    "lithium_or_polysilicon_price_event_only",
    "geopolitical_refining_margin_shock_only",
)

ROUND208_STAGE4B_WATCH_TRIGGERS: tuple[str, ...] = (
    "commodity_price_group_rally",
    "restructuring_expectation_multiple_expansion",
    "tender_offer_buyback_governance_battle_rally",
    "lithium_or_polysilicon_supply_discipline_event",
    "geopolitical_refining_margin_spike",
    "unconfirmed_customer_or_mna_report_rally",
)

ROUND208_HARD_4C_GATES: tuple[str, ...] = (
    "spread_reversal",
    "china_oversupply",
    "middle_east_capacity_overhang",
    "inventory_build",
    "ncc_shutdown_or_operating_loss",
    "deal_or_tender_event_failure",
    "regulator_revision_order",
    "large_share_issue_or_dilution",
    "commodity_price_recollapse",
    "project_capex_overrun",
    "offtake_absence",
    "fcf_deterioration",
)

ROUND208_PRICE_VALIDATION_FIELDS: tuple[str, ...] = (
    "price_data_source",
    "full_ohlc_available",
    "reported_price_anchor",
    "reported_return_anchor",
    "stage2_price",
    "stage3_price",
    "stage4b_price",
    "stage4c_price",
    "peak_price",
    "mfe_1d",
    "mae_1d",
    "mfe_from_base_to_record_close",
    "issue_price_discount_pct",
    "operating_loss_worsening_pct",
    "profit_swing",
    "commodity_drawdown_pct",
    "price_validation_status",
)


@dataclass(frozen=True)
class Round208ScoreAdjustment:
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
class Round208CaseCandidate:
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
    extra_price_metrics: Mapping[str, float | str]
    score_price_alignment: str
    rerating_result: str
    stage_failure_type: str
    price_validation_status: str
    notes: str

    @property
    def large_sector(self) -> str:
        return ROUND208_LARGE_SECTOR.value

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND208_SCORE_ADJUSTMENTS: tuple[Round208ScoreAdjustment, ...] = (
    Round208ScoreAdjustment("actual_product_spread", 5, "raise", "R4 Stage 3는 원자재 가격보다 제품 스프레드 확인이 먼저다."),
    Round208ScoreAdjustment("fcf_after_working_capital", 5, "raise", "재고와 운전자본 이후 FCF가 보여야 구조적 rerating 후보가 된다."),
    Round208ScoreAdjustment("supply_discipline_confirmed", 5, "raise", "공급규율 또는 설비중단이 실제 확인되어야 spread 회복이 지속된다."),
    Round208ScoreAdjustment("capacity_shutdown_confirmed", 4, "raise", "롯데케미칼 Daesan NCC처럼 확정된 shutdown은 Stage 2 근거다."),
    Round208ScoreAdjustment("price_floor_or_offtake", 5, "raise", "전략자원은 price floor/offtake가 있어야 commodity cycle과 분리된다."),
    Round208ScoreAdjustment("cost_curve_advantage", 4, "raise", "cost curve 우위가 있어야 가격 하락에도 FCF 방어가 가능하다."),
    Round208ScoreAdjustment("strategic_customer_or_government_offtake", 4, "raise", "정부 지원이나 전략고객은 offtake/FCF로 연결될 때 의미가 있다."),
    Round208ScoreAdjustment("inventory_normalization", 4, "raise", "화학/소재는 재고 축적이 아니어야 spread 개선이 신뢰된다."),
    Round208ScoreAdjustment("capital_return_from_cashflow", 3, "raise", "현금흐름에서 나오는 환원은 governance event premium과 다르다."),
    Round208ScoreAdjustment("commodity_price_up_only", -5, "lower", "원자재 가격 상승만으로는 EPS/FCF 체급 변화를 증명하지 못한다."),
    Round208ScoreAdjustment("restructuring_plan_without_margin", -4, "lower", "구조조정 계획은 OPM/FCF 회복 전까지 Stage 2 watch다."),
    Round208ScoreAdjustment("policy_support_without_fcf", -4, "lower", "정책 지원만 있고 FCF가 없으면 Green 금지다."),
    Round208ScoreAdjustment("tender_offer_or_governance_premium", -5, "lower", "공개매수/경영권 프리미엄은 구조적 Stage 3와 분리한다."),
    Round208ScoreAdjustment("unconfirmed_media_report", -5, "lower", "OCI SpaceX, 풍산 M&A 보도처럼 미확정 보도는 event premium이다."),
    Round208ScoreAdjustment("capacity_cut_expectation_only", -3, "lower", "capacity cut 기대만 있고 spread/OPM이 없으면 Green 금지다."),
    Round208ScoreAdjustment("lithium_price_event", -4, "lower", "리튬 가격 반등은 cyclical/event로 먼저 본다."),
    Round208ScoreAdjustment("refining_margin_geopolitical_shock", -3, "lower", "지정학적 정제마진 spike는 multi-quarter floor 전까지 cycle이다."),
    Round208ScoreAdjustment("customer_or_contract_unconfirmed", -4, "lower", "고객 또는 계약이 미확정이면 confidence cap을 둔다."),
    Round208ScoreAdjustment("capex_heavy_project_pre_revenue", -4, "lower", "상업가동 전 대형 CAPEX 프로젝트는 dilution/FCF 리스크가 크다."),
)


ROUND208_CASE_CANDIDATES: tuple[Round208CaseCandidate, ...] = (
    Round208CaseCandidate(
        case_id="r4_loop8_korea_zinc_event_strategic_watch",
        symbol="010130",
        company_name="고려아연",
        primary_archetype=E2RArchetype.NONFERROUS_STRATEGIC_METALS,
        secondary_archetypes=(
            E2RArchetype.EVENT_PREMIUM_GOVERNANCE_OVERLAY,
            E2RArchetype.RARE_METALS_STRATEGIC_MATERIALS,
            E2RArchetype.CAPITAL_ALLOCATION_DILUTION_OVERLAY,
        ),
        case_type="event_premium",
        stage1_date=date(2024, 9, 13),
        stage2_date=date(2025, 12, 15),
        stage3_date=None,
        stage4b_date=date(2024, 10, 21),
        stage4c_date=date(2024, 10, 30),
        stage3_decision="strategic_metals_project_is_stage2_until_offtake_fcf_dilution_and_capex_risk_clear",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("mbk_young_poong_tender_offer", "us_critical_minerals_plant_7_4bn_usd", "antimony_germanium_gallium_zinc_lead_copper_precious_metals", "commercial_operation_2027_to_2029"),
        red_flag_fields=("tender_offer_premium", "governance_battle", "new_share_issue_dilution", "capex_heavy_project_pre_revenue", "offtake_fcf_missing"),
        price_data_source="Reuters/WSJ/FT reported price anchors",
        reported_price_anchor="556,000 KRW base; 690,000 KRW intraday; 877,000 KRW record close; 1,543,000 KRW pre-share-issue close",
        reported_return_anchor="+19.8% tender event; +24.1% base to intraday peak; +57.7% to record close; -29.9% share issue event; +27% critical minerals event",
        mfe_1d=24.1,
        mae_1d=-29.9,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=877000.0,
        stage4c_price_anchor=1081643.0,
        peak_price_anchor=1543000.0,
        extra_price_metrics={"event_base_price": 556000.0, "tender_offer_price": 660000.0, "mfe_from_base_to_record_close": 57.7, "issue_price_discount_pct": -56.6, "critical_minerals_event_mfe": 27.0},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="false_yellow",
        price_validation_status="reported_price_anchor_not_full_ohlc",
        notes="Governance/tender/buyback are event premium; the U.S. critical-minerals project is Stage 2 until offtake, FCF, capex, and dilution risks clear.",
    ),
    Round208CaseCandidate(
        case_id="r4_loop8_lotte_chemical_petrochem_break",
        symbol="011170",
        company_name="롯데케미칼",
        primary_archetype=E2RArchetype.PETROCHEMICAL_RESTRUCTURING_KOREA,
        secondary_archetypes=(E2RArchetype.CHEMICAL_SPREAD, E2RArchetype.COMMODITY_PRICE_4C_OVERLAY),
        case_type="4c_thesis_break",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2025, 11, 26),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 2, 7),
        stage3_decision="capacity_cut_and_government_support_are_stage2_until_spread_opm_fcf_and_debt_stabilization_recover",
        stage4b_status="none",
        hard_4c_confirmed=True,
        evidence_fields=("daesan_ncc_restructuring_plan", "1_1mn_tpy_shutdown_three_years", "support_package_over_2tn_krw", "capital_increase_1_2tn_krw"),
        red_flag_fields=("operating_loss_895bn_krw", "loss_worsening_157pct", "china_middle_east_oversupply", "demand_slowdown"),
        price_data_source="Reuters financial and restructuring evidence",
        reported_price_anchor="stock OHLC unavailable",
        reported_return_anchor="2024 operating loss 895.0bn KRW; loss worsened +157%; Daesan NCC 1.1mn tpy shutdown for 3 years",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"operating_loss_2024_krw_bn": 895.0, "operating_loss_worsening_pct": 157.0, "daesan_ncc_capacity_mn_tpy": 1.1, "shutdown_years": 3.0, "support_package_krw_trn": 2.0, "capital_increase_krw_trn": 1.2},
        score_price_alignment="false_positive_score",
        rerating_result="thesis_break",
        stage_failure_type="should_have_been_red",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Petrochemical restructuring is relief, not Green, until spread, OPM, FCF, working capital, and debt burden recover.",
    ),
    Round208CaseCandidate(
        case_id="r4_loop8_lg_chem_petrochem_failed_rerating",
        symbol="051910",
        company_name="LG화학",
        primary_archetype=E2RArchetype.CHEMICAL_SPREAD,
        secondary_archetypes=(E2RArchetype.PETROCHEMICAL_RESTRUCTURING_KOREA, E2RArchetype.COMMODITY_PRICE_4C_OVERLAY),
        case_type="failed_rerating",
        stage1_date=date(2024, 1, 1),
        stage2_date=date(2025, 12, 19),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=date(2025, 2, 7),
        stage3_decision="restructuring_plan_and_stake_sale_are_not_green_without_actual_spread_opm_fcf_and_working_capital_recovery",
        stage4b_status="watch",
        hard_4c_confirmed=True,
        evidence_fields=("petrochemical_restructuring_plan_submitted", "lges_stake_sale_shareholder_return_plan"),
        red_flag_fields=("operating_profit_down_63_75pct", "petrochemical_q4_loss_99bn_krw", "china_oversupply", "demand_weakness", "stake_sale_event_negative_return"),
        price_data_source="Reuters financial and event return anchors",
        reported_price_anchor="no stage price anchor",
        reported_return_anchor="LG Chem -2.9% and LGES -6.0% after stake-sale plan; OP -63.75%; petrochemical Q4 loss 99.0bn KRW",
        mfe_1d=None,
        mae_1d=-2.9,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"operating_profit_2024_krw_bn": 916.8, "operating_profit_decline_pct": -63.75, "petrochemical_q4_loss_krw_bn": 99.0, "lges_stake_sale_event_mae_1d": -2.9},
        score_price_alignment="false_positive_score",
        rerating_result="thesis_break",
        stage_failure_type="should_have_been_red",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="Petrochemical spread hope and capital-allocation plan cannot create Green before actual spread, OPM, FCF, and working-capital recovery.",
    ),
    Round208CaseCandidate(
        case_id="r4_loop8_sk_innovation_refining_cycle",
        symbol="096770",
        company_name="SK이노베이션",
        primary_archetype=E2RArchetype.REFINING_OIL_SPREAD,
        secondary_archetypes=(E2RArchetype.COMMODITY_SPREAD_CYCLE_NOT_STRUCTURAL, E2RArchetype.COMMODITY_PRICE_4C_OVERLAY),
        case_type="cyclical_success",
        stage1_date=date(2025, 4, 30),
        stage2_date=date(2026, 5, 13),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="refining_profit_rebound_is_cyclical_stage2_until_multi_quarter_margin_floor_fcf_deleveraging_and_capital_return_are_visible",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("q1_2026_op_2_2tn_krw", "lseg_estimate_beat", "refining_profit_rebound"),
        red_flag_fields=("q1_2025_operating_loss", "refining_recovery_takes_time_warning", "geopolitical_refining_margin_shock_risk", "non_refining_loss_control_needed"),
        price_data_source="Reuters financial and event return anchors",
        reported_price_anchor="no stage price anchor",
        reported_return_anchor="2025 Q1 shares -2.5% before earnings; 2026 Q1 OP 2.2tn KRW vs 1.4tn estimate, +57.1% beat",
        mfe_1d=None,
        mae_1d=-2.5,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"q1_2025_op_loss_krw_bn": -45.0, "profit_swing_2025_vs_2024_krw_bn": -670.0, "q1_2026_op_krw_trn": 2.2, "profit_swing_2026_vs_2025_krw_trn": 2.23, "beat_vs_lseg_estimate_pct": 57.1},
        score_price_alignment="aligned",
        rerating_result="cyclical_rerating",
        stage_failure_type="stage2_watch_success",
        price_validation_status="reported_event_anchor_not_full_ohlc",
        notes="Refining rebound can be Stage 2/cyclical success, but Stage 3 requires multi-quarter margin floor, FCF, deleveraging, and capital return.",
    ),
    Round208CaseCandidate(
        case_id="r4_loop8_posco_lithium_resource_security",
        symbol="005490",
        company_name="POSCO홀딩스",
        primary_archetype=E2RArchetype.LITHIUM_BATTERY_RAW_MATERIAL,
        secondary_archetypes=(E2RArchetype.RARE_METALS_PRICE_FLOOR_OFFTAKE, E2RArchetype.LITHIUM_CYCLE_OVERLAY),
        case_type="success_candidate",
        stage1_date=date(2023, 1, 1),
        stage2_date=date(2025, 11, 11),
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="lithium_resource_security_is_stage2_until_price_floor_offtake_downstream_margin_and_fcf_are_visible",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("minres_lithium_jv_stake_deal", "wodgina_mt_marion_indirect_15pct_stake", "spodumene_concentrate_rights"),
        red_flag_fields=("spodumene_price_collapse", "lithium_cycle_exposure", "downstream_margin_unverified", "posco_stock_reaction_unavailable"),
        price_data_source="Reuters commodity and transaction anchors",
        reported_price_anchor="POSCO stock OHLC unavailable; MinRes +10.8% reported",
        reported_return_anchor="MinRes +10.8%; spodumene >$6,000/t to ~$610/t then ~$880/t",
        mfe_1d=10.8,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"transaction_value_usd_mn": 765.0, "posco_indirect_stake_pct": 15.0, "spodumene_peak_to_low_drawdown_pct": -89.8, "spodumene_low_to_rebound_pct": 44.3, "spodumene_rebound_vs_peak_pct": -85.3},
        score_price_alignment="evidence_good_but_price_failed",
        rerating_result="cyclical_rerating",
        stage_failure_type="stage2_watch_success",
        price_validation_status="posco_stock_ohlc_unavailable_after_deep_search",
        notes="Lithium resource security is Stage 2; Stage 3 needs price floor, offtake economics, downstream margin, and FCF.",
    ),
    Round208CaseCandidate(
        case_id="r4_loop8_oci_non_china_polysilicon_event",
        symbol="010060",
        company_name="OCI홀딩스",
        primary_archetype=E2RArchetype.POLYSILICON_NON_CHINA_SUPPLY_OPTION,
        secondary_archetypes=(E2RArchetype.EVENT_PREMIUM_GOVERNANCE_OVERLAY, E2RArchetype.DISCLOSURE_CONFIDENCE_CAP),
        case_type="success_candidate",
        stage1_date=date(2025, 6, 7),
        stage2_date=date(2025, 6, 7),
        stage3_date=None,
        stage4b_date=date(2026, 4, 14),
        stage4c_date=None,
        stage3_decision="non_china_supply_and_us_capacity_are_stage2_until_confirmed_contract_volume_price_duration_margin_and_fcf_after_capex",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("us_texas_capacity_expansion_1_2bn_usd", "target_capacity_10gw_by_2027", "ai_data_center_power_demand_narrative", "non_china_polysilicon_option"),
        red_flag_fields=("spacex_contract_unconfirmed_media_report", "capex_heavy_project_pre_revenue", "subsidy_policy_risk", "polysilicon_price_decline_risk"),
        price_data_source="FT/Reuters evidence anchors",
        reported_price_anchor="stock OHLC unavailable",
        reported_return_anchor="$1.2B U.S. expansion; target 10GW by 2027; SpaceX report unconfirmed",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"us_investment_usd_bn": 1.2, "target_capacity_gw": 10.0, "target_year": 2027.0, "spacex_report_status": "unconfirmed"},
        score_price_alignment="unknown",
        rerating_result="unknown",
        stage_failure_type="stage2_watch_success",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="U.S. expansion is Stage 2; unconfirmed SpaceX report is event premium and cannot create Green.",
    ),
    Round208CaseCandidate(
        case_id="r4_loop8_poongsan_copper_defense_event",
        symbol="103140",
        company_name="풍산",
        primary_archetype=E2RArchetype.COPPER_PROCESSING_PLUS_DEFENSE,
        secondary_archetypes=(E2RArchetype.EVENT_PREMIUM_GOVERNANCE_OVERLAY, E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG),
        case_type="event_premium",
        stage1_date=date(2026, 4, 3),
        stage2_date=None,
        stage3_date=None,
        stage4b_date=None,
        stage4c_date=None,
        stage3_decision="copper_plus_defense_mna_report_is_stage1_attention_until_transaction_order_margin_and_fcf_are_confirmed",
        stage4b_status="watch",
        hard_4c_confirmed=False,
        evidence_fields=("hanwha_acquisition_report_1_5tn_krw", "ammunition_and_missile_warhead_business", "copper_processing_defense_theme"),
        red_flag_fields=("transaction_not_decided", "unconfirmed_media_report", "management_premium_rumor", "copper_spread_reversal_risk"),
        price_data_source="Reuters evidence source only",
        reported_price_anchor="stock OHLC unavailable",
        reported_return_anchor="reported deal value 1.5tn KRW; transaction not decided",
        mfe_1d=None,
        mae_1d=None,
        stage2_price_anchor=None,
        stage3_price_anchor=None,
        stage4b_price_anchor=None,
        stage4c_price_anchor=None,
        peak_price_anchor=None,
        extra_price_metrics={"reported_deal_value_krw_trn": 1.5, "transaction_status": "not_decided"},
        score_price_alignment="price_moved_without_evidence",
        rerating_result="event_premium",
        stage_failure_type="false_yellow",
        price_validation_status="price_data_unavailable_after_deep_search",
        notes="Hanwha acquisition report is event premium; confirmed transaction or recurring order/margin/FCF evidence is required before Stage 3.",
    ),
)


def round208_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND208_CASE_CANDIDATES:
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
                "Round208 R4 Loop-8 materials/spread/strategic-resources price-path "
                "validation case. Calibration-only; not production scoring input."
            ),
            stage1_evidence=tuple(field for field in candidate.evidence_fields if "event" in field or "report" in field or "tender" in field or "price" in field),
            stage2_evidence=candidate.evidence_fields if candidate.stage2_date else (),
            stage3_evidence=tuple(
                field
                for field in candidate.evidence_fields
                if "offtake" in field
                or "spread" in field
                or "fcf" in field
                or "capacity" in field
                or "contract" in field
                or "production" in field
                or "margin" in field
            ),
            stage4b_evidence=tuple(
                field
                for field in (*candidate.evidence_fields, *candidate.red_flag_fields)
                if "event" in field
                or "tender" in field
                or "governance" in field
                or "unconfirmed" in field
                or "premium" in field
                or "rally" in field
            ),
            stage4c_evidence=tuple(
                field
                for field in candidate.red_flag_fields
                if "loss" in field
                or "oversupply" in field
                or "dilution" in field
                or "share_issue" in field
                or "reversal" in field
                or "decline" in field
                or "fcf" in field
            ),
            must_have_fields=ROUND208_GREEN_REQUIRED_FIELDS,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason=(
                "; ".join(candidate.red_flag_fields)
                if candidate.case_type in {"event_premium", "overheat", "4b_watch", "4c_thesis_break", "failed_rerating"}
                else None
            ),
            score_price_alignment=candidate.score_price_alignment,
            rerating_result=candidate.rerating_result,
            stage_failure_type=candidate.stage_failure_type,
            price_pattern=candidate.stage3_decision,
            score_weight_hint={
                "actual_product_spread_delta": 5.0,
                "fcf_after_working_capital_delta": 5.0,
                "supply_discipline_confirmed_delta": 5.0,
                "capacity_shutdown_confirmed_delta": 4.0,
                "price_floor_or_offtake_delta": 5.0,
                "cost_curve_advantage_delta": 4.0,
                "strategic_customer_or_government_offtake_delta": 4.0,
                "inventory_normalization_delta": 4.0,
                "capital_return_from_cashflow_delta": 3.0,
                "commodity_price_up_only_delta": -5.0,
                "restructuring_plan_without_margin_delta": -4.0,
                "policy_support_without_fcf_delta": -4.0,
                "tender_offer_or_governance_premium_delta": -5.0,
                "unconfirmed_media_report_delta": -5.0,
                "capacity_cut_expectation_only_delta": -3.0,
                "lithium_price_event_delta": -4.0,
                "refining_margin_geopolitical_shock_delta": -3.0,
                "customer_or_contract_unconfirmed_delta": -4.0,
                "capex_heavy_project_pre_revenue_delta": -4.0,
            },
            green_guardrails=(
                "production_scoring_changed_false",
                "candidate_generation_input_false",
                "shadow_weight_only_true",
                "full_ohlc_complete_false",
                "price_validation_partial_with_reported_price_anchors",
                "do_not_invent_price_or_stage_dates",
                "do_not_treat_commodity_price_governance_event_restructuring_plan_policy_support_or_unconfirmed_media_report_as_green_alone",
                *ROUND208_GREEN_REQUIRED_FIELDS,
                *ROUND208_GREEN_FORBIDDEN_PATTERNS,
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
                price_data_available=False,
                stage_dates_confidence=0.8 if candidate.stage4c_date or candidate.stage2_date else 0.65,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round208_case_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND208_CASE_CANDIDATES:
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


def round208_score_adjustment_rows() -> tuple[dict[str, str], ...]:
    return tuple(adjustment.as_row() for adjustment in ROUND208_SCORE_ADJUSTMENTS)


def round208_price_validation_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round208_price_validation": "true"} for field in ROUND208_PRICE_VALIDATION_FIELDS)


def round208_target_alias_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {"round208_label": label, "canonical_archetype": canonical}
        for label, canonical in ROUND208_REQUIRED_TARGET_ALIASES.items()
    )


def round208_summary() -> dict[str, int | bool | str]:
    records = round208_case_records()
    return {
        "case_candidate_count": len(records),
        "required_target_count": len(ROUND208_REQUIRED_TARGET_ALIASES),
        "score_adjustment_count": len(ROUND208_SCORE_ADJUSTMENTS),
        "price_validation_field_count": len(ROUND208_PRICE_VALIDATION_FIELDS),
        "success_candidate_count": sum(1 for case in records if case.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for case in records if case.case_type == "cyclical_success"),
        "event_premium_count": sum(1 for case in records if case.case_type == "event_premium"),
        "failed_or_4c_count": sum(1 for case in records if case.case_type in {"failed_rerating", "4c_thesis_break"}),
        "hard_4c_case_count": sum(1 for case in ROUND208_CASE_CANDIDATES if case.hard_4c_confirmed),
        "stage3_case_count": sum(1 for case in ROUND208_CASE_CANDIDATES if case.stage3_date),
        "stage4b_watch_count": sum(1 for case in ROUND208_CASE_CANDIDATES if case.stage4b_status == "watch"),
        "reported_price_anchor_count": sum(
            1 for case in ROUND208_CASE_CANDIDATES if case.price_validation_status != "price_data_unavailable_after_deep_search"
        ),
        "production_scoring_changed": False,
        "candidate_generation_input": False,
        "shadow_weight_only": True,
        "price_validation_completed": "partial_with_reported_price_anchors",
        "full_ohlc_complete": False,
    }


def write_round208_r4_loop8_reports(
    *,
    output_directory: str | Path = ROUND208_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND208_DEFAULT_CASES_PATH,
    audit_path: str | Path = ROUND208_DEFAULT_AUDIT_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    cases = write_case_library(round208_case_records(), cases_path)
    audit = Path(audit_path)
    audit.parent.mkdir(parents=True, exist_ok=True)
    paths = {
        "cases": cases,
        "audit_json": audit,
        "summary": output / "round208_r4_loop8_price_validation_summary.md",
        "case_matrix": output / "round208_r4_loop8_case_matrix.csv",
        "target_aliases": output / "round208_r4_loop8_target_aliases.csv",
        "score_adjustments": output / "round208_r4_loop8_score_adjustments.csv",
        "price_validation_fields": output / "round208_r4_loop8_price_validation_fields.csv",
        "green_gate_review": output / "round208_r4_loop8_green_gate_review.md",
        "price_validation_plan": output / "round208_r4_loop8_price_validation_plan.md",
        "stage4b_4c_review": output / "round208_r4_loop8_stage4b_4c_review.md",
    }
    audit.write_text(json.dumps(round208_audit_payload(), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_rows(round208_case_rows(), paths["case_matrix"])
    _write_rows(round208_target_alias_rows(), paths["target_aliases"])
    _write_rows(round208_score_adjustment_rows(), paths["score_adjustments"])
    _write_rows(round208_price_validation_field_rows(), paths["price_validation_fields"])
    paths["summary"].write_text(render_round208_summary_markdown(), encoding="utf-8")
    paths["green_gate_review"].write_text(render_round208_green_gate_review_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round208_price_validation_plan_markdown(), encoding="utf-8")
    paths["stage4b_4c_review"].write_text(render_round208_stage4b_4c_review_markdown(), encoding="utf-8")
    return paths


def round208_audit_payload() -> dict[str, object]:
    return {
        "source_round": ROUND208_SOURCE_ROUND_PATH,
        "large_sector": ROUND208_LARGE_SECTOR.value,
        "summary": round208_summary(),
        "target_aliases": list(round208_target_alias_rows()),
        "green_required_fields": list(ROUND208_GREEN_REQUIRED_FIELDS),
        "green_forbidden_patterns": list(ROUND208_GREEN_FORBIDDEN_PATTERNS),
        "stage4b_watch_triggers": list(ROUND208_STAGE4B_WATCH_TRIGGERS),
        "hard_4c_gates": list(ROUND208_HARD_4C_GATES),
        "score_adjustments": list(round208_score_adjustment_rows()),
        "case_ids": [case.case_id for case in ROUND208_CASE_CANDIDATES],
        "what_not_to_change": [
            "do_not_apply_to_production_scoring_yet",
            "do_not_use_round208_cases_as_candidate_generation_input",
            "do_not_lower_stage3_green_thresholds",
            "do_not_treat_commodity_price_governance_event_restructuring_plan_policy_support_or_unconfirmed_media_report_as_green",
            "do_not_invent_full_ohlc_or_stage_prices_when_only_reported_anchors_exist",
            "keep_full_ohlc_complete_false_until_official_backfill_is_done",
        ],
    }


def render_round208_summary_markdown() -> str:
    summary = round208_summary()
    lines = [
        "# Round-208 R4 Loop-8 Price-Path Validation Summary",
        "",
        f"- source_round: `{ROUND208_SOURCE_ROUND_PATH}`",
        f"- large_sector: `{ROUND208_LARGE_SECTOR.value}`",
        "- scope: Korea Zinc event premium, petrochemical restructuring, refining cycle, lithium resource security, non-China polysilicon, and copper-defense event premium",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- required_target_count: {summary['required_target_count']}",
        f"- score_adjustment_count: {summary['score_adjustment_count']}",
        f"- price_validation_field_count: {summary['price_validation_field_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- cyclical_success_count: {summary['cyclical_success_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- failed_or_4c_count: {summary['failed_or_4c_count']}",
        f"- hard_4c_case_count: {summary['hard_4c_case_count']}",
        f"- stage3_case_count: {summary['stage3_case_count']}",
        f"- stage4b_watch_count: {summary['stage4b_watch_count']}",
        f"- reported_price_anchor_count: {summary['reported_price_anchor_count']}",
        "- production_scoring_changed: false",
        "- candidate_generation_input: false",
        "- shadow_weight_only: true",
        "- price_validation_completed: partial_with_reported_price_anchors",
        "- full_ohlc_complete: false",
        "",
        "## Interpretation",
        "",
        "- 고려아연은 전략광물 후보지만 2024년 공개매수/자사주/신주발행 구간은 event premium과 4B/4C-watch다.",
        "- 롯데케미칼과 LG화학은 구조조정 기대보다 실제 spread, OPM, FCF 회복 전까지 Red/Watch가 우선이다.",
        "- SK이노베이션의 정제마진 반등은 cyclical Stage 2이며, multi-quarter margin floor 전까지 Green은 보류한다.",
        "- POSCO홀딩스 리튬 JV는 resource-security Stage 2지만 lithium cycle과 downstream margin을 확인해야 한다.",
        "- OCI SpaceX 보도와 풍산 M&A 보도는 미확정 media report라서 Stage 3 근거가 아니다.",
        "",
        "쉬운 예: `as_of_date=2024-09-13`에 고려아연이 공개매수로 급등해도, 그 급등은 경영권 프리미엄이다. offtake와 FCF가 확인된 전략자원 Stage 3와는 분리해야 한다.",
    ]
    return "\n".join(lines) + "\n"


def render_round208_green_gate_review_markdown() -> str:
    lines = ["# Round-208 R4 Loop-8 Green Gate Review", "", "## Green Required Evidence", ""]
    lines.extend(f"- `{field}`" for field in ROUND208_GREEN_REQUIRED_FIELDS)
    lines.extend(["", "## Green Forbidden Patterns", ""])
    lines.extend(f"- `{field}`" for field in ROUND208_GREEN_FORBIDDEN_PATTERNS)
    lines.extend(["", "## Shadow Score Adjustments", "", "| axis | direction | points | reason |", "| --- | --- | ---: | --- |"])
    for adjustment in ROUND208_SCORE_ADJUSTMENTS:
        lines.append(f"| `{adjustment.axis}` | {adjustment.direction} | {adjustment.points} | {adjustment.reason} |")
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not apply these weights to production scoring yet.",
            "- Do not use Round208 cases as candidate-generation input.",
            "- Do not lower Stage 3-Green thresholds to force promotion.",
            "- Do not invent full OHLC, stage prices, or MFE/MAE when only reported anchors exist.",
            "- Do not treat commodity price spike, governance battle, policy support, restructuring plan, or unconfirmed media report as Green evidence alone.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round208_price_validation_plan_markdown() -> str:
    lines = ["# Round-208 R4 Loop-8 Price Validation Plan", "", "## Required Fields", ""]
    lines.extend(f"- `{field}`" for field in ROUND208_PRICE_VALIDATION_FIELDS)
    lines.extend(["", "## Case Anchors", "", "| case | price data source | reported anchor | status |", "| --- | --- | --- | --- |"])
    for case in ROUND208_CASE_CANDIDATES:
        lines.append(
            f"| `{case.case_id}` | {case.price_data_source} | {case.reported_return_anchor} | `{case.price_validation_status}` |"
        )
    lines.extend(
        [
            "",
            "## Backfill Rule",
            "",
            "- Use reported Reuters/FT/WSJ/MarketWatch anchors only for fields they explicitly support.",
            "- Keep full OHLC unavailable until official or adjusted daily price backfill is done.",
            "- Separate Stage 2 strategic/resource/restructuring evidence, Green-required operating proof, 4B event premium, and 4C spread/dilution breaks.",
            "- Do not create a Stage 3 anchor when the case intentionally has no Stage 3 date.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round208_stage4b_4c_review_markdown() -> str:
    lines = ["# Round-208 R4 Loop-8 Stage 4B / 4C Review", "", "## 4B Watch Triggers", ""]
    lines.extend(f"- `{field}`" for field in ROUND208_STAGE4B_WATCH_TRIGGERS)
    lines.extend(["", "## Hard 4C Gates", ""])
    lines.extend(f"- `{field}`" for field in ROUND208_HARD_4C_GATES)
    lines.extend(
        [
            "",
            "## R4 Loop-8 Interpretation",
            "",
            "- Governance/tender/buyback rallies are event premium and 4B-watch, not structural Green.",
            "- Petrochemical restructuring is Stage 2 relief until spread, OPM, FCF, and working capital recover.",
            "- Refining profit rebounds remain cyclical until multi-quarter margin floor and FCF are visible.",
            "- Unconfirmed customer or M&A media reports are disclosure-confidence caps.",
            "",
            "## Case Review",
            "",
            "| case | 4B status | hard 4C confirmed | interpretation |",
            "| --- | --- | --- | --- |",
        ]
    )
    for case in ROUND208_CASE_CANDIDATES:
        lines.append(
            f"| `{case.case_id}` | `{case.stage4b_status}` | {str(case.hard_4c_confirmed).lower()} | {case.notes} |"
        )
    return "\n".join(lines) + "\n"


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


def _date_text(value: date | None) -> str:
    return value.isoformat() if value else ""


def _float_text(value: float | None) -> str:
    return "" if value is None else str(value)


__all__ = [
    "ROUND208_CASE_CANDIDATES",
    "ROUND208_DEFAULT_AUDIT_PATH",
    "ROUND208_DEFAULT_CASES_PATH",
    "ROUND208_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND208_GREEN_FORBIDDEN_PATTERNS",
    "ROUND208_GREEN_REQUIRED_FIELDS",
    "ROUND208_HARD_4C_GATES",
    "ROUND208_PRICE_VALIDATION_FIELDS",
    "ROUND208_REQUIRED_TARGET_ALIASES",
    "ROUND208_SCORE_ADJUSTMENTS",
    "ROUND208_SOURCE_ROUND_PATH",
    "ROUND208_STAGE4B_WATCH_TRIGGERS",
    "Round208CaseCandidate",
    "Round208ScoreAdjustment",
    "render_round208_green_gate_review_markdown",
    "render_round208_price_validation_plan_markdown",
    "render_round208_stage4b_4c_review_markdown",
    "render_round208_summary_markdown",
    "round208_audit_payload",
    "round208_case_records",
    "round208_case_rows",
    "round208_price_validation_field_rows",
    "round208_score_adjustment_rows",
    "round208_summary",
    "round208_target_alias_rows",
    "write_round208_r4_loop8_reports",
]
