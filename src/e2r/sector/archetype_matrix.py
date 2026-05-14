"""Round-2 E2R archetype matrix.

This module stores the analyst's second case-matrix synthesis as
calibration/evaluation material. It is intentionally not imported by production
scoring, staging, research, or pipeline modules.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import COUNTEREXAMPLE_GROUPS, POSITIVE_GROUPS, E2RArchetype
from e2r.sector.case_library import E2RCaseRecord, load_case_library
from e2r.sector.research_framework import ROUND1_CORE_ARCHETYPES, round1_core_for


ROUND2_PEER_NORMALIZATION_METRICS = (
    "sector_eps_growth_percentile",
    "sector_op_growth_percentile",
    "sector_opm_expansion_percentile",
    "sector_fcf_growth_percentile",
    "sector_revision_percentile",
    "sector_price_strength_percentile",
    "sector_valuation_discount_percentile",
    "sector_trading_value_spike_percentile",
)


ROUND2_DEEP_DIVE_PRIORITY_GROUPS: Mapping[int, tuple[E2RArchetype, ...]] = {
    1: (
        E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,
        E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,
        E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG,
        E2RArchetype.EXPORT_RECURRING_CONSUMER,
        E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,
        E2RArchetype.MEMORY_HBM_CAPACITY,
        E2RArchetype.SEMI_EQUIPMENT_CAPEX,
        E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT,
        E2RArchetype.SHIPPING_FREIGHT_CYCLE,
        E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT,
    ),
    2: (
        E2RArchetype.AUTO_MOBILITY_COMPONENTS,
        E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
        E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE,
        E2RArchetype.TURNAROUND_COST_RESTRUCTURING,
        E2RArchetype.GAME_CONTENT_IP,
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        E2RArchetype.BIOTECH_REGULATORY,
    ),
    3: (
        E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT,
        E2RArchetype.UTILITIES_REGULATED_TARIFF,
        E2RArchetype.RETAIL_DOMESTIC_CONSUMER,
        E2RArchetype.ROBOTICS_FACTORY_AUTOMATION,
        E2RArchetype.COMMODITY_SPREAD,
        E2RArchetype.ONE_OFF_EVENT_DEMAND,
        E2RArchetype.THEME_VALUATION_OVERHEAT,
        E2RArchetype.GENERIC_UNCLASSIFIED,
    ),
}


ROUND2_FIRST_SHADOW_SCORING_ARCHETYPES = (
    E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,
    E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,
    E2RArchetype.EXPORT_RECURRING_CONSUMER,
    E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,
    E2RArchetype.MEMORY_HBM_CAPACITY,
    E2RArchetype.SEMI_EQUIPMENT_CAPEX,
    E2RArchetype.SHIPPING_FREIGHT_CYCLE,
    E2RArchetype.ONE_OFF_EVENT_DEMAND,
    E2RArchetype.THEME_VALUATION_OVERHEAT,
    E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
)


ROUND2_PROMOTION_BANDS = (
    "Stage 2",
    "Stage 2-High",
    "Stage 3-Watch",
    "Stage 3-Yellow",
    "Stage 3-Green",
)


ROUND2_SOURCE_ROUND_PATHS = (
    "docs/round/round_01.md",
    "docs/round/round_02.md",
)

# Backward-compatible alias for older report consumers.
ROUND2_SOURCE_ROUND_PATH = ROUND2_SOURCE_ROUND_PATHS[-1]


ROUND2_PRICE_PATTERN_TYPES: Mapping[str, str] = {
    "DIRECT_RERATING": "Stage 2 이후 조정 없이 급등하는 유형",
    "STAIR_STEP_RERATING": "Stage 2 이후 20~30% 조정 반복 후 계속 상승하는 유형",
    "CYCLE_SPIKE_NORMALIZATION": "EPS는 폭발하지만 4B/4C가 빨리 와야 하는 유형",
    "THEME_FRONT_RUN": "가격이 먼저 가고 EPS/FCF가 못 따라오는 유형",
    "ACCOUNTING_TRUST_COLLAPSE": "Stage 2~3처럼 보이다가 회계/감사/신뢰 이슈로 4C가 터지는 유형",
    "SECTOR_SPREAD_RERATING": "선도주 리레이팅 이후 동종 섹터로 Stage 1->2가 확산되는 유형",
    "MARGIN_NORMALIZATION_RERATING": "저마진 물량 정리나 비용구조 개선으로 OPM이 정상화되는 유형",
    "BACKLOG_RERATING": "계약 하나보다 수주잔고 체급 변화가 가격 프레임을 바꾸는 유형",
    "PROGRAM_MILESTONE_RERATING": "정부/프로그램 milestone이 납품과 매출 인식으로 이어지는 유형",
    "PRICE_ORDER_RERATING": "선가/운임/제품가격과 수주가 동시에 움직이는 유형",
    "EXPORT_CHANNEL_RERATING": "수출 채널 확장과 반복 수요가 내수 프레임을 깨는 유형",
    "CAPACITY_BOTTLENECK_RERATING": "HBM/CAPA/장비 리드타임 병목이 다년 EPS 경로를 바꾸는 유형",
    "VALUE_UP_RERATING": "ROE/PBR/주주환원 조합이 Korea discount를 줄이는 유형",
    "REGULATORY_REVENUE_CONVERSION": "허가/기술이전이 실제 매출·로열티·FCF로 전환되어야 하는 유형",
}


ROUND2_ARCHETYPE_PRICE_PATTERNS: Mapping[E2RArchetype, tuple[str, ...]] = {
    E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL: (
        "STAIR_STEP_RERATING",
        "SECTOR_SPREAD_RERATING",
        "MARGIN_NORMALIZATION_RERATING",
    ),
    E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG: (
        "BACKLOG_RERATING",
        "PROGRAM_MILESTONE_RERATING",
    ),
    E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG: (
        "PRICE_ORDER_RERATING",
        "BACKLOG_RERATING",
        "CYCLE_SPIKE_NORMALIZATION",
    ),
    E2RArchetype.EXPORT_RECURRING_CONSUMER: (
        "EXPORT_CHANNEL_RERATING",
        "STAIR_STEP_RERATING",
    ),
    E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION: (
        "EXPORT_CHANNEL_RERATING",
        "THEME_FRONT_RUN",
    ),
    E2RArchetype.MEMORY_HBM_CAPACITY: (
        "CAPACITY_BOTTLENECK_RERATING",
        "STAIR_STEP_RERATING",
        "CYCLE_SPIKE_NORMALIZATION",
    ),
    E2RArchetype.SEMI_EQUIPMENT_CAPEX: (
        "CAPACITY_BOTTLENECK_RERATING",
        "CYCLE_SPIKE_NORMALIZATION",
    ),
    E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT: (
        "THEME_FRONT_RUN",
        "CYCLE_SPIKE_NORMALIZATION",
    ),
    E2RArchetype.COMMODITY_SPREAD: (
        "CYCLE_SPIKE_NORMALIZATION",
    ),
    E2RArchetype.SHIPPING_FREIGHT_CYCLE: (
        "CYCLE_SPIKE_NORMALIZATION",
    ),
    E2RArchetype.AUTO_MOBILITY_COMPONENTS: (
        "VALUE_UP_RERATING",
        "MARGIN_NORMALIZATION_RERATING",
    ),
    E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET: (
        "VALUE_UP_RERATING",
    ),
    E2RArchetype.BIOTECH_REGULATORY: (
        "REGULATORY_REVENUE_CONVERSION",
        "THEME_FRONT_RUN",
    ),
    E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT: (
        "EXPORT_CHANNEL_RERATING",
        "DIRECT_RERATING",
    ),
    E2RArchetype.ONE_OFF_EVENT_DEMAND: (
        "CYCLE_SPIKE_NORMALIZATION",
    ),
    E2RArchetype.THEME_VALUATION_OVERHEAT: (
        "THEME_FRONT_RUN",
        "ACCOUNTING_TRUST_COLLAPSE",
    ),
}


@dataclass(frozen=True)
class ArchetypeMatrixEntry:
    """Research playbook for one Round-2 archetype."""

    archetype: E2RArchetype
    priority_tier: int
    structure: str
    success_cases: tuple[str, ...]
    success_candidate_cases: tuple[str, ...]
    counterexample_cases: tuple[str, ...]
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_signals: tuple[str, ...]
    stage4b_signals: tuple[str, ...]
    stage4c_signals: tuple[str, ...]
    score_weight_hint: Mapping[str, float]
    green_gate_policy: str
    peer_metrics: tuple[str, ...] = ROUND2_PEER_NORMALIZATION_METRICS

    @property
    def green_restricted(self) -> bool:
        text = self.green_gate_policy.lower()
        return "restricted" in text or "blocked" in text or "limited" in text


def _weights(
    eps_fcf: float,
    visibility: float,
    bottleneck: float,
    mispricing: float,
    valuation: float,
) -> Mapping[str, float]:
    return {
        "eps_fcf": eps_fcf,
        "structural_visibility": visibility,
        "bottleneck_pricing": bottleneck,
        "market_mispricing": mispricing,
        "valuation_rerating": valuation,
    }


def _entry(
    archetype: E2RArchetype,
    *,
    priority_tier: int,
    structure: str,
    success_cases: tuple[str, ...] = (),
    success_candidate_cases: tuple[str, ...] = (),
    counterexample_cases: tuple[str, ...] = (),
    stage1: tuple[str, ...],
    stage2: tuple[str, ...],
    stage3: tuple[str, ...],
    stage4b: tuple[str, ...],
    stage4c: tuple[str, ...],
    weights: Mapping[str, float],
    green_gate_policy: str,
) -> ArchetypeMatrixEntry:
    return ArchetypeMatrixEntry(
        archetype=archetype,
        priority_tier=priority_tier,
        structure=structure,
        success_cases=success_cases,
        success_candidate_cases=success_candidate_cases,
        counterexample_cases=counterexample_cases,
        stage1_signals=stage1,
        stage2_signals=stage2,
        stage3_signals=stage3,
        stage4b_signals=stage4b,
        stage4c_signals=stage4c,
        score_weight_hint=weights,
        green_gate_policy=green_gate_policy,
    )


ROUND2_ARCHETYPE_MATRIX: Mapping[E2RArchetype, ArchetypeMatrixEntry] = {
    E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL: _entry(
        E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,
        priority_tier=1,
        structure="수요 급증 -> 장기공급계약/수주잔고/CAPA 부족 -> 가격 전가 -> EPS/FCF 상향",
        success_cases=("HD현대일렉트릭", "일진전기"),
        success_candidate_cases=("효성중공업", "LS ELECTRIC", "제룡전기"),
        counterexample_cases=("대한전선-like", "단기 공급계약 테마주"),
        stage1=("supply_contract_disclosure", "trading_value_spike", "backlog_keyword"),
        stage2=("contract_amount_to_sales_10pct_plus", "contract_duration_24m_plus", "op_eps_revision", "backlog_growth"),
        stage3=("backlog_to_sales_100pct_plus", "lead_time_extended", "capa_shortage", "asp_opm_improvement", "fy1_fy2_eps_revision"),
        stage4b=("target_price_raises_cluster", "excessive_price_runup", "new_order_slowdown", "revision_momentum_slowdown"),
        stage4c=("contract_cancellation_or_delay", "asp_opm_decline", "backlog_decline", "oversupply"),
        weights=_weights(20, 24, 22, 12, 12),
        green_gate_policy="Green allowed only with disclosure + financial actual + research/consensus-revision cross evidence.",
    ),
    E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG: _entry(
        E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,
        priority_tier=1,
        structure="지정학/국방비 증가 -> 정부 고객 장기계약 -> 수주잔고/납품 스케줄 -> 매출/OP visibility",
        success_cases=("한화에어로스페이스",),
        success_candidate_cases=("현대로템", "LIG넥스원", "한국항공우주"),
        counterexample_cases=("단순 방산 테마주", "납기 지연/원가 상승 방산"),
        stage1=("defense_contract_news", "government_customer", "geopolitical_momentum"),
        stage2=("order_backlog_to_sales_rising", "multi_year_delivery_schedule", "op_eps_revision"),
        stage3=("government_customer", "multi_year_contract", "delivery_visibility", "opm_improvement", "fy2_fy3_revision"),
        stage4b=("defense_sector_overheat", "valuation_consensus_saturated", "new_contract_expectation_priced_in"),
        stage4c=("delivery_delay", "cost_overrun", "contract_cancellation", "export_approval_or_political_risk"),
        weights=_weights(20, 24, 17, 14, 14),
        green_gate_policy="Green allowed with government customer, delivery visibility, and margin/revision evidence.",
    ),
    E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG: _entry(
        E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG,
        priority_tier=2,
        structure="선가 상승/수주 슬롯 -> 저가수주 소진 -> 고마진 선박 인도 -> EPS 턴어라운드",
        success_candidate_cases=("삼성중공업", "HD현대중공업", "HD한국조선해양", "한화오션"),
        counterexample_cases=("러시아/Zvezda 계약 리스크", "저가수주 잔존 조선사"),
        stage1=("large_order", "newbuild_price_index_up", "shipbuilding_trading_value_spike"),
        stage2=("low_margin_backlog_rolloff", "high_margin_delivery_start", "op_turnaround_revision"),
        stage3=("backlog_quality_improvement", "fy2_fy3_ship_price_reflection", "cost_stability", "long_delivery_slots"),
        stage4b=("order_peak", "newbuild_price_slowdown", "valuation_saturated"),
        stage4c=("contract_cancellation", "steel_or_labor_cost_spike", "delivery_delay", "order_cycle_slowdown"),
        weights=_weights(20, 22, 18, 13, 13),
        green_gate_policy="Green allowed selectively; low-margin backlog and cancellation risk must be cleared.",
    ),
    E2RArchetype.EXPORT_RECURRING_CONSUMER: _entry(
        E2RArchetype.EXPORT_RECURRING_CONSUMER,
        priority_tier=1,
        structure="해외 수요 -> 채널 확장 -> 반복소비/ASP/OPM -> 내수 소비재 프레임 제거",
        success_cases=("삼양식품",),
        success_candidate_cases=("농심", "오리온"),
        counterexample_cases=("단일 제품 유행", "원가 상승 음식료", "리콜/규제 소비재"),
        stage1=("export_growth", "earnings_surprise", "overseas_channel_news"),
        stage2=("fy1_fy2_eps_revision", "export_ratio_rising", "opm_expansion", "target_price_revision"),
        stage3=("recurring_consumption", "channel_diversification", "asp_hold", "capa_and_volume_growth", "old_domestic_frame"),
        stage4b=("margin_peak", "global_brand_consensus_crowded", "inventory_or_channel_stuffing_risk"),
        stage4c=("export_growth_slowdown", "overseas_inventory_issue", "asp_opm_decline", "regulatory_or_recall_issue"),
        weights=_weights(22, 23, 12, 16, 13),
        green_gate_policy="Contract quality is not required; recurring export demand and EPS/OP revision are required.",
    ),
    E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION: _entry(
        E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,
        priority_tier=1,
        structure="K뷰티 글로벌 수요 -> 미국/일본/유럽 채널 -> 반복 주문/OPM/ROE -> 중국 의존 프레임 제거",
        success_candidate_cases=("실리콘투", "코스맥스", "한국콜마", "APR", "브이티"),
        counterexample_cases=("중국 의존 화장품", "인디 브랜드 유행성 과열", "채널 재고/매출채권 리스크"),
        stage1=("us_japan_europe_export_growth", "kbeauty_channel_news", "cosmetics_export_data"),
        stage2=("fy1_fy2_op_eps_revision", "opm_roe_improvement", "channel_expansion", "customer_diversification"),
        stage3=("repeat_orders", "offline_or_major_retail_entry", "no_inventory_receivable_problem", "china_dependence_down", "old_china_cosmetics_frame"),
        stage4b=("kbeauty_overcrowding", "new_brand_saturation", "target_price_overheat"),
        stage4c=("sell_through_slowdown", "inventory_increase", "receivables_deterioration", "tariff_or_regulation_impact"),
        weights=_weights(22, 23, 12, 16, 13),
        green_gate_policy="Green allowed through export/channel/recurring-demand evidence, not contract quality.",
    ),
    E2RArchetype.MEMORY_HBM_CAPACITY: _entry(
        E2RArchetype.MEMORY_HBM_CAPACITY,
        priority_tier=1,
        structure="AI 수요 -> HBM/DRAM/NAND 수요 -> CAPA 재배치/공급규율 -> 다년 EPS/FCF 상향",
        success_cases=("SK하이닉스",),
        success_candidate_cases=("삼성전자 메모리", "Micron"),
        counterexample_cases=("단순 메모리 가격 반등", "공급과잉 전환"),
        stage1=("memory_price_increase", "hbm_demand", "earnings_turnaround"),
        stage2=("fy1_fy2_fy3_op_eps_revision", "customer_supply_race", "supply_discipline", "price_increase"),
        stage3=("lta_or_prepayment_or_price_band", "capa_constraint", "multi_year_consensus_revision", "pbr_to_per_frame_shift"),
        stage4b=("per_rerating_consensus", "target_multiple_saturated", "capex_expansion_news", "customer_price_resistance"),
        stage4c=("dram_nand_hbm_price_decline", "oversupply", "customer_ai_capex_slowdown", "consensus_revision_down"),
        weights=_weights(24, 21, 19, 15, 12),
        green_gate_policy="Green allowed with memory-specific revision, pricing, supply discipline, and capacity evidence.",
    ),
    E2RArchetype.SEMI_EQUIPMENT_CAPEX: _entry(
        E2RArchetype.SEMI_EQUIPMENT_CAPEX,
        priority_tier=2,
        structure="고객사 AI/HBM capex -> 병목 장비/소재 -> 수주잔고/매출화 -> OP leverage",
        success_candidate_cases=("한미반도체", "이수페타시스", "ISC", "리노공업"),
        counterexample_cases=("단일 고객 장비주", "국산화 테마 장비주"),
        stage1=("customer_capex_news", "equipment_order", "ai_hbm_keyword"),
        stage2=("backlog_growth", "customer_diversification", "revenue_conversion", "op_eps_revision"),
        stage3=("bottleneck_equipment_position", "long_customer_capex_path", "repeat_or_consumable_demand", "high_opm"),
        stage4b=("capex_peak", "customer_order_slowdown", "equipment_lead_time_normalization"),
        stage4c=("order_cancellation", "customer_capex_cut", "inventory_build"),
        weights=_weights(22, 20, 18, 14, 12),
        green_gate_policy="Green allowed with confirmed order-to-revenue conversion and customer capex durability.",
    ),
    E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT: _entry(
        E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT,
        priority_tier=2,
        structure="EV 기대 -> 장기공급계약/CAPA 투자 -> 원자재/수요/CAPA 과잉 리스크",
        success_candidate_cases=("초기 양극재 장기계약 구간",),
        counterexample_cases=("에코프로비엠/에코프로 2023", "CAPA 과잉 소재주", "단순 테마 소재주"),
        stage1=("long_term_contract", "capa_expansion", "ev_demand_expectation"),
        stage2=("price_and_margin_rising_together", "customer_contract_quality", "capex_without_fcf_damage"),
        stage3=("long_term_contract", "price_pass_through", "demand_durability", "valuation_runway"),
        stage4b=("price_runup", "crowding", "per_pbr_overheat", "revision_slowdown"),
        stage4c=("ev_demand_slowdown", "mineral_price_decline", "capa_overbuild", "margin_compression"),
        weights=_weights(20, 16, 14, 10, 10),
        green_gate_policy="Green highly restricted; overheat and CAPA overbuild penalties dominate unless contract economics are clear.",
    ),
    E2RArchetype.COMMODITY_SPREAD: _entry(
        E2RArchetype.COMMODITY_SPREAD,
        priority_tier=2,
        structure="제품가격-원가 스프레드 -> OP leverage, but usually cyclical rather than structural",
        success_candidate_cases=("정유 spread 회복주", "철강 spread 회복주", "비철/제련 구조주"),
        counterexample_cases=("순수 가격 사이클", "중국 공급과잉 화학"),
        stage1=("product_price_up", "spread_improvement"),
        stage2=("op_eps_revision", "inventory_demand_improvement", "cost_structure_improvement"),
        stage3=("cost_curve_advantage", "capacity_discipline", "long_term_supply_constraint"),
        stage4b=("spread_peak", "inventory_build", "broad_consensus_bullish"),
        stage4c=("spread_reversal", "china_or_global_capacity_addition", "demand_slowdown"),
        weights=_weights(20, 12, 18, 10, 10),
        green_gate_policy="Green restricted by cycle cap unless structural cost-curve or supply discipline is explicit.",
    ),
    E2RArchetype.SHIPPING_FREIGHT_CYCLE: _entry(
        E2RArchetype.SHIPPING_FREIGHT_CYCLE,
        priority_tier=1,
        structure="운임 급등 -> EPS 폭발 -> 공급/수요 정상화 시 급락 위험",
        success_cases=("HMM 2020~2021",),
        success_candidate_cases=("Maersk 2020~2021",),
        counterexample_cases=("HMM 고점 이후", "Maersk 2024", "신규 선복 증가"),
        stage1=("freight_rate_spike", "spot_rate_surge"),
        stage2=("contract_freight_reflection", "op_eps_explosion", "vessel_shortage"),
        stage3=("multi_year_contract_freight", "fleet_supply_constraint"),
        stage4b=("freight_rate_peak", "spot_future_divergence", "new_vessel_supply"),
        stage4c=("freight_rate_drop", "overcapacity", "demand_slowdown"),
        weights=_weights(20, 10, 18, 8, 8),
        green_gate_policy="Green very restricted; normally cyclical success or Yellow/Red rather than structural Green.",
    ),
    E2RArchetype.AUTO_MOBILITY_COMPONENTS: _entry(
        E2RArchetype.AUTO_MOBILITY_COMPONENTS,
        priority_tier=2,
        structure="믹스/수출/환율/주주환원 -> EPS/FCF 안정 성장 -> 저평가 프레임 해소",
        success_candidate_cases=("현대차", "기아", "현대모비스", "HL만도"),
        counterexample_cases=("원가전가 실패 부품주", "EV 수요 둔화 부품주"),
        stage1=("sales_mix_fx_improvement", "shareholder_return_announcement"),
        stage2=("op_eps_revision", "high_margin_mix", "shareholder_return"),
        stage3=("global_share_gain", "valuation_discount_resolution", "roe_fcf_durability"),
        stage4b=("peak_margin", "tariff_policy_risk", "valuation_rerating_complete"),
        stage4c=("tariff_or_demand_slowdown", "cost_increase", "recall_or_quality_cost"),
        weights=_weights(20, 18, 10, 15, 17),
        green_gate_policy="Green allowed with durable mix/FCF/return evidence; component cost pass-through must be proven.",
    ),
    E2RArchetype.ROBOTICS_FACTORY_AUTOMATION: _entry(
        E2RArchetype.ROBOTICS_FACTORY_AUTOMATION,
        priority_tier=3,
        structure="테마 기대 -> 실제 수주/매출 전환 여부가 핵심",
        success_candidate_cases=("레인보우로보틱스", "스마트팩토리 장비주"),
        counterexample_cases=("로봇 테마 고밸류", "단발성 MOU"),
        stage1=("strategic_investment", "robot_theme", "order_news"),
        stage2=("revenue_conversion", "customer_diversification", "op_improvement"),
        stage3=("repeat_revenue_or_consumables", "customer_lock_in", "cost_leverage"),
        stage4b=("order_delay", "missed_results", "valuation_overheat"),
        stage4c=("revenue_failure", "customer_order_cut", "theme_unwind"),
        weights=_weights(20, 15, 10, 12, 10),
        green_gate_policy="Green restricted until revenue conversion and repeatability are proven.",
    ),
    E2RArchetype.PLATFORM_SOFTWARE_INTERNET: _entry(
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        priority_tier=3,
        structure="MAU/ARPU/광고/커머스 -> 수익화와 OPM leverage -> 플랫폼 프레임 재평가",
        success_candidate_cases=("네이버", "더존비즈온"),
        counterexample_cases=("MAU만 높은 플랫폼", "규제 리스크 플랫폼"),
        stage1=("mau_traffic_recovery", "ad_commerce_improvement"),
        stage2=("arpu_up", "op_leverage", "cost_efficiency"),
        stage3=("recurring_revenue", "pricing_power", "margin_expansion", "old_frame_valuation"),
        stage4b=("platform_multiple_saturated", "ai_cost_ignored", "crowded_reports"),
        stage4c=("regulation", "take_rate_decline", "traffic_decline"),
        weights=_weights(20, 22, 8, 16, 14),
        green_gate_policy="Green allowed only with monetization and margin leverage, not MAU alone.",
    ),
    E2RArchetype.GAME_CONTENT_IP: _entry(
        E2RArchetype.GAME_CONTENT_IP,
        priority_tier=3,
        structure="신작/IP/콘텐츠 -> 글로벌 매출 -> 반복 monetization 여부가 핵심",
        success_candidate_cases=("크래프톤", "하이브", "JYP", "에스엠"),
        counterexample_cases=("신작 기대만 있는 게임주", "엔터 계약/스캔들 리스크"),
        stage1=("new_game_or_comeback_or_tour", "traffic_or_preorder"),
        stage2=("revenue_conversion", "opm_eps_revision"),
        stage3=("ip_repeatability", "global_monetization", "low_churn"),
        stage4b=("hit_peak", "crowded_ip_reports", "valuation_saturation"),
        stage4c=("new_game_failure", "contract_risk", "core_ip_damage"),
        weights=_weights(20, 18, 8, 14, 12),
        green_gate_policy="Green restricted unless IP repeatability and monetization are visible.",
    ),
    E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET: _entry(
        E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
        priority_tier=2,
        structure="ROE + 저PBR + 자본정책 -> Korea discount 해소 -> PBR-ROE rerating",
        success_candidate_cases=("KB금융", "신한지주", "하나금융", "메리츠금융"),
        counterexample_cases=("단순 저PBR 금융주", "PF/충당금 리스크 금융"),
        stage1=("value_up_disclosure", "buyback_or_dividend", "low_pbr"),
        stage2=("roe_improvement", "capital_ratio_stable", "credit_cost_stable", "capital_return_durability"),
        stage3=("pbr_roe_frame_change", "recurring_roe", "credible_shareholder_return"),
        stage4b=("pbr_gap_closed", "return_policy_fully_priced", "roe_peak"),
        stage4c=("credit_cost_up", "pf_loss", "capital_ratio_deterioration"),
        weights=_weights(15, 20, 5, 15, 25),
        green_gate_policy="Green allowed with ROE/PBR and durable capital return, not low PBR alone.",
    ),
    E2RArchetype.BIOTECH_REGULATORY: _entry(
        E2RArchetype.BIOTECH_REGULATORY,
        priority_tier=3,
        structure="임상/허가/기술이전 -> 매출화/로열티 전환 여부가 핵심",
        success_candidate_cases=("알테오젠", "유한양행"),
        counterexample_cases=("임상 뉴스만 있는 바이오", "임상 실패/허가 지연", "CB/유증 반복 바이오"),
        stage1=("clinical_approval_or_license_news",),
        stage2=("milestone_payment", "commercialization_path", "cash_flow_improvement"),
        stage3=("actual_sales_or_royalty", "eps_fcf_conversion", "low_dilution_risk"),
        stage4b=("royalty_curve_priced", "clinical_news_crowded"),
        stage4c=("clinical_failure", "approval_delay", "rights_or_cb_dilution"),
        weights=_weights(8, 15, 5, 10, 5),
        green_gate_policy="Green blocked before real revenue/royalty and dilution control.",
    ),
    E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT: _entry(
        E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT,
        priority_tier=2,
        structure="의료/미용기기 수출 -> 소모품/반복 매출 -> OPM/ROE",
        success_candidate_cases=("클래시스", "휴젤", "파마리서치", "원텍"),
        counterexample_cases=("단일 장비 판매", "규제/허가 지연"),
        stage1=("export_country_expansion", "approval", "new_product"),
        stage2=("consumable_or_repeat_revenue", "opm_roe", "fy1_fy2_eps_revision"),
        stage3=("global_channel", "repeat_consumable_structure", "high_fcf_conversion"),
        stage4b=("medical_beauty_crowding", "margin_peak", "valuation_saturation"),
        stage4c=("approval_delay", "regulation", "competition_intensifies"),
        weights=_weights(20, 22, 13, 14, 12),
        green_gate_policy="Green allowed with export channel plus repeat consumable/service revenue.",
    ),
    E2RArchetype.RETAIL_DOMESTIC_CONSUMER: _entry(
        E2RArchetype.RETAIL_DOMESTIC_CONSUMER,
        priority_tier=3,
        structure="소비 회복/점포효율/비용 leverage -> OP 개선",
        success_candidate_cases=("BGF리테일", "GS리테일", "신세계", "호텔신라"),
        counterexample_cases=("이마트류 경쟁 심화", "단기 소비 회복 테마"),
        stage1=("same_store_sales_recovery", "consumer_recovery_news"),
        stage2=("opm_improvement", "inventory_normalization", "cost_leverage"),
        stage3=("structural_channel_advantage", "fcf_improvement", "valuation_discount_resolution"),
        stage4b=("reopening_trade_crowded", "margin_peak", "traffic_growth_slowdown"),
        stage4c=("inventory_increase", "competition_intensifies", "consumer_slowdown"),
        weights=_weights(18, 16, 7, 14, 14),
        green_gate_policy="Green restricted unless OP/FCF improvement is structural, not traffic-only.",
    ),
    E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT: _entry(
        E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT,
        priority_tier=3,
        structure="수주보다 PF/신용/원가가 핵심",
        success_candidate_cases=("PF 리스크 해소 건설사", "해외 플랜트/인프라 수주"),
        counterexample_cases=("PF 부실 건설사", "원가 상승 미반영"),
        stage1=("order_or_presale_recovery", "pf_concern_eases"),
        stage2=("cost_ratio_stabilizes", "cash_flow_improves", "debt_reduction"),
        stage3=("post_restructuring_repeat_cash_flow",),
        stage4b=("credit_relief_fully_priced", "order_quality_ignored"),
        stage4c=("pf_loss", "unsold_inventory_increase", "credit_rating_downgrade"),
        weights=_weights(18, 12, 6, 12, 10),
        green_gate_policy="Green very restricted; credit and cash-flow evidence must dominate order headline.",
    ),
    E2RArchetype.UTILITIES_REGULATED_TARIFF: _entry(
        E2RArchetype.UTILITIES_REGULATED_TARIFF,
        priority_tier=3,
        structure="요금/원가/정책 -> EPS 턴어라운드, but regulation risk remains high",
        success_candidate_cases=("한국전력", "한국가스공사"),
        counterexample_cases=("요금 동결", "부채/정책 리스크"),
        stage1=("tariff_or_cost_improvement", "policy_change"),
        stage2=("loss_reduction", "cash_flow_improvement"),
        stage3=("regulatory_frame_change", "durable_tariff_pass_through"),
        stage4b=("policy_relief_fully_priced", "debt_burden_ignored"),
        stage4c=("tariff_freeze", "cost_spike", "debt_pressure"),
        weights=_weights(18, 18, 5, 12, 10),
        green_gate_policy="Green restricted unless tariff pass-through regime changes, not just one-time relief.",
    ),
    E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE: _entry(
        E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE,
        priority_tier=3,
        structure="NAV discount -> 자사주/소각/지배구조 개선 -> Korea discount 해소",
        success_candidate_cases=("SK스퀘어", "삼성물산", "value-up 지주사"),
        counterexample_cases=("주주환원 없는 저PBR 지주사", "자회사 가치 훼손"),
        stage1=("buyback_or_cancellation_or_dividend", "governance_reform"),
        stage2=("nav_discount_narrowing_catalyst", "subsidiary_earnings_improvement"),
        stage3=("structural_governance_change", "repeat_shareholder_return", "foreign_ownership_rerating"),
        stage4b=("event_premium_fully_priced", "return_policy_no_longer_incremental"),
        stage4c=("controlling_shareholder_risk", "subsidiary_value_impairment"),
        weights=_weights(12, 18, 5, 20, 25),
        green_gate_policy="Green allowed only if governance action is backed by FCF/NAV improvement.",
    ),
    E2RArchetype.TURNAROUND_COST_RESTRUCTURING: _entry(
        E2RArchetype.TURNAROUND_COST_RESTRUCTURING,
        priority_tier=2,
        structure="적자사업 제거/고정비 leverage -> OP 흑자전환 -> EPS 체급 변화",
        success_candidate_cases=("적자사업 매각 기업", "흑자전환 제조/플랫폼"),
        counterexample_cases=("일회성 비용절감", "구조조정 실패"),
        stage1=("loss_reduction", "cost_cut"),
        stage2=("op_turnaround", "cash_flow_improvement"),
        stage3=("recurring_margin", "growth_and_cost_structure_improve_together"),
        stage4b=("turnaround_fully_priced", "margin_peak"),
        stage4c=("restructuring_failure", "debt_or_liquidity_risk"),
        weights=_weights(22, 18, 8, 15, 12),
        green_gate_policy="Green allowed only when cost improvement is recurring and paired with growth/FCF.",
    ),
    E2RArchetype.ONE_OFF_EVENT_DEMAND: _entry(
        E2RArchetype.ONE_OFF_EVENT_DEMAND,
        priority_tier=1,
        structure="일회성 수요 -> EPS 폭발 -> 다음 해 정상화",
        counterexample_cases=("씨젠 2020", "Abbott COVID tests", "Zoom 2020"),
        stage1=("explosive_temporary_demand", "one_off_demand_spike"),
        stage2=("short_term_eps_spike", "red_flag_present"),
        stage3=("green_blocked_unless_recurrence_proven",),
        stage4b=("market_extrapolates_one_off", "valuation_overheat"),
        stage4c=("demand_normalization", "guidance_down", "asp_drop"),
        weights=_weights(20, 5, 5, 5, 5),
        green_gate_policy="Green blocked by default; normally Stage 3-Red/Yellow guardrail.",
    ),
    E2RArchetype.THEME_VALUATION_OVERHEAT: _entry(
        E2RArchetype.THEME_VALUATION_OVERHEAT,
        priority_tier=1,
        structure="테마/주가 급등/밸류 과열 -> EPS/FCF가 따라오지 않으면 붕괴",
        counterexample_cases=("에코프로비엠/에코프로 2023", "SMCI 2024", "로봇/AI 무실적 테마주"),
        stage1=("price_surge", "theme_news"),
        stage2=("only_if_real_eps_fcf_evidence_exists",),
        stage3=("green_extremely_limited",),
        stage4b=("valuation_saturation", "crowded_reports", "price_blowoff"),
        stage4c=("accounting_issue", "guidance_miss", "revision_down"),
        weights=_weights(10, 5, 5, 5, 5),
        green_gate_policy="Green blocked unless real EPS/FCF evidence overwhelms overheat risk.",
    ),
    E2RArchetype.GENERIC_UNCLASSIFIED: _entry(
        E2RArchetype.GENERIC_UNCLASSIFIED,
        priority_tier=3,
        structure="아직 명확한 E2R 구조가 배정되지 않은 종목",
        counterexample_cases=("분류 불명 테마주",),
        stage1=("unknown_sector_signal",),
        stage2=("requires_manual_classification",),
        stage3=("blocked_until_archetype_assigned",),
        stage4b=("unknown",),
        stage4c=("unknown",),
        weights=_weights(10, 5, 5, 5, 5),
        green_gate_policy="Green blocked until a real archetype and evidence family are assigned.",
    ),
}


def matrix_entry(archetype: E2RArchetype | str) -> ArchetypeMatrixEntry:
    item = archetype if isinstance(archetype, E2RArchetype) else E2RArchetype(str(archetype))
    core = round1_core_for(item)
    return ROUND2_ARCHETYPE_MATRIX[core]


def all_matrix_entries() -> tuple[ArchetypeMatrixEntry, ...]:
    return tuple(ROUND2_ARCHETYPE_MATRIX[item] for item in ROUND1_CORE_ARCHETYPES)


def deep_dive_priority_tier(archetype: E2RArchetype | str) -> int:
    item = round1_core_for(archetype)
    for tier, archetypes in ROUND2_DEEP_DIVE_PRIORITY_GROUPS.items():
        if item in archetypes:
            return tier
    return 3


def first_shadow_scoring_candidate(archetype: E2RArchetype | str) -> bool:
    return round1_core_for(archetype) in ROUND2_FIRST_SHADOW_SCORING_ARCHETYPES


def price_patterns_for(archetype: E2RArchetype | str) -> tuple[str, ...]:
    item = round1_core_for(archetype)
    return ROUND2_ARCHETYPE_PRICE_PATTERNS.get(item, ("DIRECT_RERATING",))


def round2_case_gap_summary(records: Iterable[E2RCaseRecord]) -> tuple[dict[str, object], ...]:
    rows = tuple(records)
    output: list[dict[str, object]] = []
    for entry in all_matrix_entries():
        archetype_records = tuple(record for record in rows if round1_core_for(record.primary_archetype) == entry.archetype)
        positive = tuple(record for record in archetype_records if record.case_type in POSITIVE_GROUPS)
        counter = tuple(record for record in archetype_records if record.case_type in COUNTEREXAMPLE_GROUPS)
        if entry.archetype in {
            E2RArchetype.ONE_OFF_EVENT_DEMAND,
            E2RArchetype.THEME_VALUATION_OVERHEAT,
            E2RArchetype.GENERIC_UNCLASSIFIED,
        }:
            status = "green_guardrail_only" if len(counter) >= 2 else "needs_more_counterexamples"
        else:
            status = "covered_2x2" if len(positive) >= 2 and len(counter) >= 2 else "needs_more_cases"
        output.append(
            {
                "archetype": entry.archetype.value,
                "priority_tier": entry.priority_tier,
                "deep_dive_priority_tier": deep_dive_priority_tier(entry.archetype),
                "first_shadow_scoring_candidate": first_shadow_scoring_candidate(entry.archetype),
                "positive_count": len(positive),
                "counterexample_count": len(counter),
                "status": status,
                "positive_case_ids": tuple(record.case_id for record in positive),
                "counterexample_case_ids": tuple(record.case_id for record in counter),
                "price_patterns": price_patterns_for(entry.archetype),
            }
        )
    return tuple(output)


def write_round2_matrix_reports(
    *,
    case_path: str | Path = "data/e2r_case_library/cases_v02.jsonl",
    output_directory: str | Path = "output/e2r_archetype_matrix",
) -> dict[str, Path]:
    records = load_case_library(case_path)
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    matrix_md = output / "round2_archetype_matrix.md"
    weights_csv = output / "round2_score_weight_table.csv"
    priority_md = output / "round2_case_mining_priorities.md"
    peer_md = output / "round2_peer_normalization_metrics.md"
    gap_csv = output / "round2_case_gap_matrix.csv"
    shadow_md = output / "round2_shadow_scoring_plan.md"
    price_patterns_md = output / "round2_price_pattern_taxonomy.md"
    matrix_md.write_text(render_round2_matrix_markdown(), encoding="utf-8")
    _write_weights_csv(weights_csv)
    priority_md.write_text(render_round2_priority_markdown(records), encoding="utf-8")
    peer_md.write_text(render_peer_normalization_markdown(), encoding="utf-8")
    _write_gap_csv(gap_csv, records)
    shadow_md.write_text(render_shadow_scoring_plan_markdown(records), encoding="utf-8")
    price_patterns_md.write_text(render_price_pattern_taxonomy_markdown(), encoding="utf-8")
    return {
        "matrix": matrix_md,
        "weights": weights_csv,
        "priority": priority_md,
        "peer_metrics": peer_md,
        "case_gap_matrix": gap_csv,
        "shadow_scoring_plan": shadow_md,
        "price_pattern_taxonomy": price_patterns_md,
    }


def render_round2_matrix_markdown() -> str:
    lines = [
        "# Round-2 E2R Archetype Matrix",
        "",
        "This is calibration material. It is not production scoring.",
        "",
        "| priority | archetype | structure | Green policy |",
        "|---:|---|---|---|",
    ]
    for entry in all_matrix_entries():
        lines.append(
            f"| {entry.priority_tier} | {entry.archetype.value} | {entry.structure} | {entry.green_gate_policy} |"
        )
    lines.extend(
        [
            "",
            "## Stage Criteria",
        ]
    )
    for entry in all_matrix_entries():
        lines.extend(
            [
                "",
                f"### {entry.archetype.value}",
                f"- success_cases: {', '.join(entry.success_cases) if entry.success_cases else '-'}",
                f"- success_candidate_cases: {', '.join(entry.success_candidate_cases) if entry.success_candidate_cases else '-'}",
                f"- counterexample_cases: {', '.join(entry.counterexample_cases) if entry.counterexample_cases else '-'}",
                f"- Stage 1: {', '.join(entry.stage1_signals)}",
                f"- Stage 2: {', '.join(entry.stage2_signals)}",
                f"- Stage 3: {', '.join(entry.stage3_signals)}",
                f"- 4B: {', '.join(entry.stage4b_signals)}",
                f"- 4C: {', '.join(entry.stage4c_signals)}",
                f"- price_patterns: {', '.join(price_patterns_for(entry.archetype))}",
            ]
        )
    return "\n".join(lines) + "\n"


def render_round2_priority_markdown(records: Iterable[E2RCaseRecord]) -> str:
    gaps = round2_case_gap_summary(records)
    lines = [
        "# Round-2 Case Mining Priorities",
        "",
        "Source rounds: " + ", ".join(f"`{path}`" for path in ROUND2_SOURCE_ROUND_PATHS),
        "",
        "There are two priority concepts:",
        "",
        "- deep-dive priority: where the case matrix should be expanded first",
        "- first shadow-scoring candidate: where shadow weights can be compared first after coverage improves",
        "",
        "| current priority | deep-dive priority | first shadow? | archetype | positive | counterexamples | status |",
        "|---:|---:|---|---|---:|---:|---|",
    ]
    for row in sorted(gaps, key=lambda item: (int(item["deep_dive_priority_tier"]), int(item["priority_tier"]), str(item["archetype"]))):
        lines.append(
            f"| {row['priority_tier']} | {row['deep_dive_priority_tier']} | "
            f"{'yes' if row['first_shadow_scoring_candidate'] else 'no'} | {row['archetype']} | {row['positive_count']} | "
            f"{row['counterexample_count']} | {row['status']} |"
        )
    lines.extend(
        [
            "",
            "## Deep-Dive Priority Groups",
        ]
    )
    for tier, archetypes in sorted(ROUND2_DEEP_DIVE_PRIORITY_GROUPS.items()):
        lines.append(f"- Priority {tier}: " + ", ".join(item.value for item in archetypes))
    lines.extend(
        [
            "",
            "## First Shadow-Scoring Candidate Set",
            ", ".join(item.value for item in ROUND2_FIRST_SHADOW_SCORING_ARCHETYPES),
            "",
            "## Promotion Band Reminder",
            ", ".join(ROUND2_PROMOTION_BANDS),
            "",
            "A strong candidate can remain deterministic Stage 2 while being reported as Stage 3-Watch.",
            "Example: HD/Iljin-style cases can show `deterministic_stage=Stage 2` and `promotion_band=Stage 3-Watch` until Green evidence is complete.",
            "",
            "Round 2 also adds price-pattern labels. Example: a shipping case can be `CYCLE_SPIKE_NORMALIZATION`, while SMCI-like cases can be `ACCOUNTING_TRUST_COLLAPSE`.",
        ]
    )
    lines.extend(
        [
            "",
            "## What not to change yet",
            "- Do not apply score weights before case/path coverage is checked.",
            "- Do not lower Stage 3-Green to improve recall.",
            "- Do not use this matrix as candidate-generation input.",
            "- Use it to decide what evidence snapshots, price paths, and counterexamples to add next.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_price_pattern_taxonomy_markdown() -> str:
    lines = [
        "# Round-2 Price Pattern Taxonomy",
        "",
        "This is lifecycle calibration material, not a production trading signal.",
        "",
        "Round 2 links Stage progression to price-path behavior so 4B/4C is not treated as price-only.",
        "",
        "## Pattern Types",
    ]
    for pattern, description in ROUND2_PRICE_PATTERN_TYPES.items():
        lines.append(f"- `{pattern}`: {description}")
    lines.extend(
        [
            "",
            "## Archetype Mapping",
            "",
            "| archetype | price patterns | Green implication |",
            "|---|---|---|",
        ]
    )
    for entry in all_matrix_entries():
        patterns = price_patterns_for(entry.archetype)
        descriptions = "; ".join(f"{pattern}: {ROUND2_PRICE_PATTERN_TYPES[pattern]}" for pattern in patterns)
        lines.append(f"| {entry.archetype.value} | {descriptions} | {entry.green_gate_policy} |")
    lines.extend(
        [
            "",
            "## Example",
            "",
            "A power-equipment candidate can be Stage 2 with `STAIR_STEP_RERATING`: it may pull back 20~30% and still remain structurally intact if backlog, margin, and revision evidence persist.",
            "",
            "A theme or one-off case can have strong price action, but `THEME_FRONT_RUN` or `CYCLE_SPIKE_NORMALIZATION` keeps Green restricted until EPS/FCF durability is proven.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_shadow_scoring_plan_markdown(records: Iterable[E2RCaseRecord]) -> str:
    gaps = {row["archetype"]: row for row in round2_case_gap_summary(records)}
    lines = [
        "# Round-2 First Shadow-Scoring Plan",
        "",
        "This is not production scoring. It identifies which archetypes should be compared first in a future shadow-score run.",
        "",
        "| archetype | positive | counterexamples | coverage status | Green posture |",
        "|---|---:|---:|---|---|",
    ]
    for archetype in ROUND2_FIRST_SHADOW_SCORING_ARCHETYPES:
        entry = matrix_entry(archetype)
        row = gaps[archetype.value]
        lines.append(
            f"| {archetype.value} | {row['positive_count']} | {row['counterexample_count']} | "
            f"{row['status']} | {entry.green_gate_policy} |"
        )
    lines.extend(
        [
            "",
            "## Rules",
            "- Run old deterministic score and future archetype-aware score side by side.",
            "- Do not replace StageClassifier in the first shadow run.",
            "- Use promotion bands for visibility before changing Green gates.",
            "- Keep one-off and overheat archetypes as guardrails, not Green factories.",
            "- Review price-pattern labels before treating a move as durable rerating.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_peer_normalization_markdown() -> str:
    lines = [
        "# Round-2 Peer Normalization Metrics",
        "",
        "Absolute scores are not enough. Each archetype should also be interpreted against peers.",
        "",
        "Example: Samyang Foods' OPM should be compared inside export consumer peers, not against semiconductors.",
        "",
        "## Metrics",
    ]
    for metric in ROUND2_PEER_NORMALIZATION_METRICS:
        lines.append(f"- `{metric}`")
    lines.extend(
        [
            "",
            "## Fallback order",
            "1. Raw sector peer group",
            "2. Round-1 core archetype peer group",
            "3. Market-wide peer group",
        ]
    )
    return "\n".join(lines) + "\n"


def _write_weights_csv(path: Path) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "archetype",
                "priority_tier",
                "deep_dive_priority_tier",
                "first_shadow_scoring_candidate",
                "eps_fcf",
                "structural_visibility",
                "bottleneck_pricing",
                "market_mispricing",
                "valuation_rerating",
                "green_gate_policy",
            ),
        )
        writer.writeheader()
        for entry in all_matrix_entries():
            writer.writerow(
                {
                    "archetype": entry.archetype.value,
                    "priority_tier": entry.priority_tier,
                    "deep_dive_priority_tier": deep_dive_priority_tier(entry.archetype),
                    "first_shadow_scoring_candidate": str(first_shadow_scoring_candidate(entry.archetype)).lower(),
                    **entry.score_weight_hint,
                    "green_gate_policy": entry.green_gate_policy,
                }
            )
    return path


def _write_gap_csv(path: Path, records: Iterable[E2RCaseRecord]) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "archetype",
                "priority_tier",
                "deep_dive_priority_tier",
                "first_shadow_scoring_candidate",
                "positive_count",
                "counterexample_count",
                "status",
                "price_patterns",
                "positive_case_ids",
                "counterexample_case_ids",
            ),
        )
        writer.writeheader()
        for row in round2_case_gap_summary(records):
            writer.writerow(
                {
                    **{key: value for key, value in row.items() if not key.endswith("_case_ids")},
                    "price_patterns": "|".join(row["price_patterns"]),
                    "positive_case_ids": "|".join(row["positive_case_ids"]),
                    "counterexample_case_ids": "|".join(row["counterexample_case_ids"]),
                }
            )
    return path


__all__ = [
    "ArchetypeMatrixEntry",
    "ROUND2_ARCHETYPE_MATRIX",
    "ROUND2_ARCHETYPE_PRICE_PATTERNS",
    "ROUND2_DEEP_DIVE_PRIORITY_GROUPS",
    "ROUND2_FIRST_SHADOW_SCORING_ARCHETYPES",
    "ROUND2_PEER_NORMALIZATION_METRICS",
    "ROUND2_PRICE_PATTERN_TYPES",
    "ROUND2_PROMOTION_BANDS",
    "ROUND2_SOURCE_ROUND_PATH",
    "ROUND2_SOURCE_ROUND_PATHS",
    "all_matrix_entries",
    "deep_dive_priority_tier",
    "first_shadow_scoring_candidate",
    "matrix_entry",
    "price_patterns_for",
    "render_peer_normalization_markdown",
    "render_price_pattern_taxonomy_markdown",
    "render_round2_matrix_markdown",
    "render_round2_priority_markdown",
    "render_shadow_scoring_plan_markdown",
    "round2_case_gap_summary",
    "write_round2_matrix_reports",
]
