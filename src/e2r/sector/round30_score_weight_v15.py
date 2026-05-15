"""Round-30 cases_v12 expansion and score-weight v1.5 hypotheses.

Round 30 strengthens semi equipment/materials/packaging, completed vehicles,
auto parts, travel cycles, casino/duty-free tourism, convenience retail,
agri/livestock food cycles, space/drone themes, AI data-center cooling, and
memory/HBM. It is report-only calibration material. Production feature
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


ROUND30_SOURCE_ROUND_PATH = "docs/round/round_30.md"
ROUND30_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round30_score_weight_v15"
ROUND30_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_v12_round30.jsonl"
ROUND30_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round30_v15.csv"


@dataclass(frozen=True)
class Round30ScoreWeightDraft:
    eps_fcf: int
    structural_visibility: int
    bottleneck_pricing: int
    market_mispricing: int
    valuation: int
    capital_allocation: int = 0
    information_confidence: int = 5

    def as_dict(self) -> dict[str, int]:
        return {
            "eps_fcf": self.eps_fcf,
            "structural_visibility": self.structural_visibility,
            "bottleneck_pricing": self.bottleneck_pricing,
            "market_mispricing": self.market_mispricing,
            "valuation": self.valuation,
            "capital_allocation": self.capital_allocation,
            "information_confidence": self.information_confidence,
        }


@dataclass(frozen=True)
class Round30ScoreTarget:
    target_id: str
    large_sector: Round10LargeSector
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round30ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    normalization_point: str

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round30CaseCandidate:
    case_id: str
    target_id: str
    symbol: str
    company_name: str
    market: str
    case_type: str
    evidence_fields: tuple[str, ...]
    red_flag_fields: tuple[str, ...]
    notes: str

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND30_SCORE_TARGETS: tuple[Round30ScoreTarget, ...] = (
    Round30ScoreTarget(
        "SEMI_EQUIPMENT_CAPEX",
        Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS,
        E2RArchetype.SEMI_EQUIPMENT_CAPEX,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round30ScoreWeightDraft(22, 20, 18, 14, 12, 0, 5),
        ("hbm_capex", "advanced_packaging", "pcb_or_substrate_keyword", "equipment_order"),
        ("customer_capex_confirmed", "order_backlog_growth", "delivery_schedule", "op_eps_revision"),
        ("hbm_or_advanced_packaging_direct_exposure", "customer_diversification", "revenue_conversion"),
        ("customer_capex_confirmed", "order_backlog_growth", "delivery_schedule", "op_eps_revision", "customer_concentration_risk_low"),
        ("customer_capex", "customer_concentration", "inventory", "order_delay", "adoption_delay"),
        ("customer_capex_cut", "order_delay", "inventory_build", "single_customer_shock"),
        "Semi equipment is Watch-to-Green because it depends on customer CAPEX and delivery conversion.",
    ),
    Round30ScoreTarget(
        "AUTO_COMPLETED_VEHICLE",
        Round10LargeSector.MOBILITY_TRANSPORT_LEISURE,
        E2RArchetype.AUTO_MOBILITY_COMPLETED_VEHICLE,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round30ScoreWeightDraft(20, 18, 10, 15, 17, 10, 5),
        ("hybrid_strategy", "sales_target", "shareholder_return", "export_mix"),
        ("op_fcf_stability", "high_margin_mix", "buyback_or_dividend", "roe_pbr_rerating"),
        ("global_share_gain", "fcf_supports_return", "old_auto_discount_removed"),
        ("op_fcf_stability", "hybrid_or_mix_improvement", "shareholder_return", "roe_pbr_rerating", "tariff_risk_low"),
        ("tariff", "demand_slowdown", "recall", "peak_margin", "policy_risk"),
        ("tariff_hit", "demand_slowdown", "recall_cost", "margin_peak_reversal"),
        "Completed vehicles can be Green when FCF, mix, hybrid response, and capital return are source-backed.",
    ),
    Round30ScoreTarget(
        "AUTO_COMPONENTS_TIRE",
        Round10LargeSector.MOBILITY_TRANSPORT_LEISURE,
        E2RArchetype.AUTO_MOBILITY_COMPONENTS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round30ScoreWeightDraft(20, 17, 10, 14, 14, 3, 5),
        ("auto_parts_order", "ev_or_adas_component", "tire_spread", "customer_program"),
        ("customer_diversification", "cost_pass_through", "op_eps_revision", "raw_material_stable"),
        ("repeat_program_visibility", "margin_stable", "quality_cost_low"),
        ("customer_diversification", "cost_pass_through", "op_eps_revision", "raw_material_stable", "quality_cost_low"),
        ("raw_material", "customer_concentration", "ev_cycle", "quality_cost", "oem_pressure"),
        ("raw_material_margin_squeeze", "customer_program_cut", "quality_recall", "ev_cycle_slowdown"),
        "Auto parts and tires are Watch-to-Green; customer mix and cost pass-through are gates.",
    ),
    Round30ScoreTarget(
        "AIRLINE_TRAVEL_CYCLE",
        Round10LargeSector.MOBILITY_TRANSPORT_LEISURE,
        E2RArchetype.TRAVEL_LEISURE_REOPENING,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round30ScoreWeightDraft(18, 14, 5, 12, 10, 2, 5),
        ("passenger_recovery", "airline_integration", "cargo_mix", "travel_reopening"),
        ("op_recovery", "integration_synergy", "cost_stability", "fcf_improvement"),
        ("sustained_load_factor", "fuel_fx_controlled", "integration_cost_controlled"),
        ("op_recovery", "integration_synergy", "cost_stability", "fcf_improvement", "fuel_fx_risk_low"),
        ("oil_price", "fx", "demand_cycle", "integration_cost", "tariff"),
        ("oil_price_spike", "fx_hit", "demand_slowdown", "integration_cost_overrun"),
        "Airlines are cycle-heavy; Stage 3-Green should be rare without durable FCF and cost control.",
    ),
    Round30ScoreTarget(
        "CASINO_DUTYFREE_TOURISM",
        Round10LargeSector.MOBILITY_TRANSPORT_LEISURE,
        E2RArchetype.TRAVEL_LEISURE_REOPENING,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round30ScoreWeightDraft(18, 13, 5, 12, 10, 2, 5),
        ("tourism_policy", "china_group_tourism", "casino_drop", "dutyfree_sales"),
        ("visitor_growth_converts_to_op", "drop_amount_growth", "dutyfree_ticket_recovery", "cost_leverage"),
        ("tourist_mix_diversified", "op_leverage_confirmed", "capex_burden_low"),
        ("visitor_growth_converts_to_op", "drop_amount_growth", "dutyfree_ticket_recovery", "tourist_mix_diversified", "capex_burden_low"),
        ("tourism_policy", "china_dependency", "capex", "operating_leverage", "weak_demand"),
        ("tourism_demand_miss", "capex_covenant_failure", "china_dependency_hit", "op_leverage_failure"),
        "Tourism policy is Stage 1 until visitor mix and OP leverage are verified.",
    ),
    Round30ScoreTarget(
        "RETAIL_CONVENIENCE_OFFLINE",
        Round10LargeSector.CONSUMER_RETAIL_BRAND,
        E2RArchetype.RETAIL_DOMESTIC_CONSUMER,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round30ScoreWeightDraft(18, 16, 5, 13, 14, 3, 5),
        ("store_network", "pb_mix", "same_store_sales", "overseas_store"),
        ("same_store_sales_growth", "pb_high_margin_mix", "opm_improvement", "fcf_stable"),
        ("store_productivity", "overseas_profitability", "rent_wage_pressure_low"),
        ("same_store_sales_growth", "pb_high_margin_mix", "opm_improvement", "fcf_stable", "rent_wage_pressure_low"),
        ("rent", "wage", "competition", "same_store_sales_slowdown", "store_count_only"),
        ("same_store_sales_slowdown", "rent_wage_pressure", "overcrowding", "pb_mix_deterioration"),
        "Convenience retail is defensive Watch-to-Green; store count alone is not evidence.",
    ),
    Round30ScoreTarget(
        "AGRI_LIVESTOCK_FOOD_COMMODITY",
        Round10LargeSector.EDUCATION_LIFE_AGRI_MISC,
        E2RArchetype.COMMODITY_SPREAD,
        Round10ThemePosture.REDTEAM_FIRST,
        Round30ScoreWeightDraft(18, 10, 14, 8, 8, 0, 5),
        ("grain_price", "feed_cost", "livestock_price", "tuna_price", "smart_farm_order"),
        ("cost_pass_through", "raw_material_stable", "repeat_demand", "export_order"),
        ("sustained_margin", "weather_or_disease_risk_low", "order_or_channel_visibility"),
        ("cost_pass_through", "sustained_margin", "repeat_demand", "weather_or_disease_risk_low"),
        ("commodity_cycle", "disease_event", "feed_cost", "weather", "price_event_only"),
        ("disease_event_reversal", "feed_cost_spike", "weather_shock", "price_reversal"),
        "Agri/livestock is mostly Red/Watch because cost, disease, weather, and commodity cycles dominate.",
    ),
    Round30ScoreTarget(
        "SPACE_SUPPLYCHAIN",
        Round10LargeSector.POLICY_GEOPOLITICAL_EVENT,
        E2RArchetype.THEME_VALUATION_OVERHEAT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round30ScoreWeightDraft(16, 14, 8, 12, 10, 0, 5),
        ("space_keyword", "spacex_supplier", "drone_policy", "urban_air_mobility"),
        ("actual_delivery_contract", "government_or_defense_customer", "certification_complete", "repeat_component_revenue"),
        ("contracted_supply_chain", "revenue_recognition", "regulatory_risk_low"),
        ("actual_delivery_contract", "government_or_defense_customer", "repeat_component_revenue", "certification_complete"),
        ("no_contract", "certification_delay", "theme_overheat", "poc_only", "no_revenue"),
        ("certification_delay", "contract_absence", "program_delay", "theme_liquidity_reversal"),
        "Space and drone themes are Watch/Red unless actual delivery contracts and repeat revenue are visible.",
    ),
    Round30ScoreTarget(
        "AI_DATA_CENTER_COOLING",
        Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS,
        E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round30ScoreWeightDraft(21, 22, 22, 13, 12, 0, 5),
        ("ai_datacenter_capex", "cooling_or_power_bottleneck", "server_order", "korea_ai_capex"),
        ("orders_or_leases", "power_cooling_constraint", "delivery_schedule", "op_eps_revision"),
        ("bottleneck_asset_confirmed", "multi_customer_demand", "capex_delay_risk_low"),
        ("orders_or_leases", "power_cooling_constraint", "delivery_schedule", "op_eps_revision", "capex_delay_risk_low"),
        ("capex_delay", "project_delay", "overbuild", "no_revenue_exposure"),
        ("ai_capex_cut", "project_delay", "overbuild", "revenue_exposure_failure"),
        "AI data-center cooling/power can be Green, but only with order, bottleneck, delivery, and revenue exposure.",
    ),
    Round30ScoreTarget(
        "MEMORY_HBM",
        Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS,
        E2RArchetype.MEMORY_HBM_CAPACITY,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round30ScoreWeightDraft(24, 21, 19, 15, 12, 0, 5),
        ("hbm_demand", "memory_price_increase", "advanced_dram_capex", "customer_supply_shortage"),
        ("fy1_fy2_op_eps_revision", "supply_discipline", "capacity_allocation", "long_term_customer_signal"),
        ("multi_year_revision_path", "capacity_bottleneck", "old_cyclical_discount_removed"),
        ("hbm_demand", "memory_price_increase", "fy1_fy2_op_eps_revision", "supply_discipline", "capacity_bottleneck"),
        ("crowding", "capex_reversal", "memory_price_drop", "customer_capex_cut"),
        ("memory_price_drop", "supply_glut", "customer_capex_cut", "revision_down"),
        "HBM remains Green-possible, but crowding, CAPEX reversal, and price downcycle need 4B/4C monitoring.",
    ),
)


ROUND30_CASE_CANDIDATES: tuple[Round30CaseCandidate, ...] = (
    Round30CaseCandidate("sk_hynix_asml_euv_capex_success_signal", "SEMI_EQUIPMENT_CAPEX", "000660_EUV", "SK하이닉스 ASML EUV CAPEX", "KR", "success_candidate", ("customer_capex_confirmed", "hbm_capex"), ("customer_capex", "order_delay"), "Customer CAPEX confirms upper-chain demand but is not enough for every supplier."),
    Round30CaseCandidate("hbm_equipment_order_backlog_candidate", "SEMI_EQUIPMENT_CAPEX", "HBM_EQUIP", "HBM 장비 수주잔고 후보", "KR", "success_candidate", ("order_backlog_growth", "hbm_or_advanced_packaging_direct_exposure"), ("customer_concentration", "inventory"), "Equipment backlog can score after delivery and customer-diversification checks."),
    Round30CaseCandidate("cxl_glass_substrate_no_revenue_counterexample", "SEMI_EQUIPMENT_CAPEX", "CXL_GLASS_NOREV", "CXL유리기판무매출 반례", "KR", "failed_rerating", ("cxl_keyword", "glass_substrate_keyword"), ("adoption_delay", "no_revenue"), "CXL/glass substrate keywords stay Watch without revenue."),
    Round30CaseCandidate("customer_capex_cut_equipment_4c", "SEMI_EQUIPMENT_CAPEX", "EQUIP_CAPEX_4C", "장비고객CAPEX축소4C", "KR", "4c_thesis_break", ("equipment_order",), ("customer_capex_cut", "order_delay"), "Customer CAPEX cut is a hard equipment 4C risk."),
    Round30CaseCandidate("hyundai_hybrid_shareholder_return_candidate", "AUTO_COMPLETED_VEHICLE", "005380", "현대차 하이브리드 환원 후보", "KR", "success_candidate", ("hybrid_strategy", "shareholder_return", "op_fcf_stability"), ("tariff", "peak_margin"), "Completed-vehicle candidate needs hybrid/mix, FCF, and return execution."),
    Round30CaseCandidate("kia_mix_shareholder_return_candidate", "AUTO_COMPLETED_VEHICLE", "000270", "기아 믹스 환원 후보", "KR", "success_candidate", ("high_margin_mix", "shareholder_return", "roe_pbr_rerating"), ("demand_slowdown", "recall"), "Kia-style mix and return candidate remains source-validation material."),
    Round30CaseCandidate("auto_parts_customer_concentration_counterexample", "AUTO_COMPONENTS_TIRE", "AUTO_PARTS_CONC", "자동차부품 고객집중 반례", "KR", "failed_rerating", ("auto_parts_order",), ("customer_concentration", "oem_pressure"), "Auto parts need customer diversification and cost pass-through."),
    Round30CaseCandidate("tire_raw_material_margin_4c", "AUTO_COMPONENTS_TIRE", "TIRE_RAW_4C", "타이어원재료마진4C", "KR", "4c_thesis_break", ("tire_spread",), ("raw_material_margin_squeeze", "quality_recall"), "Raw-material squeeze can break tire margin visibility."),
    Round30CaseCandidate("korean_air_asiana_integration_candidate", "AIRLINE_TRAVEL_CYCLE", "003490", "대한항공 아시아나 통합 후보", "KR", "success_candidate", ("airline_integration", "integration_synergy"), ("integration_cost", "tariff"), "Airline integration can reach Watch/Stage 2 after cost and synergy evidence."),
    Round30CaseCandidate("korean_air_record_revenue_cycle_candidate", "AIRLINE_TRAVEL_CYCLE", "003490_REV", "대한항공 매출회복 사이클", "KR", "cyclical_success", ("passenger_recovery", "op_recovery"), ("oil_price", "fx"), "Record revenue can be cyclical success, not automatic structural Green."),
    Round30CaseCandidate("airline_oil_fx_4c", "AIRLINE_TRAVEL_CYCLE", "AIR_OILFX_4C", "항공유가환율4C", "KR", "4c_thesis_break", ("passenger_recovery",), ("oil_price_spike", "fx_hit"), "Oil and FX can break airline OP leverage."),
    Round30CaseCandidate("cargo_passenger_mix_slowdown_counterexample", "AIRLINE_TRAVEL_CYCLE", "AIR_MIX_SLOW", "항공화물여객믹스둔화", "KR", "failed_rerating", ("cargo_mix",), ("demand_slowdown", "cargo_yield_normalization"), "Cargo/passenger mix slowdown keeps travel cycle Watch."),
    Round30CaseCandidate("korea_china_group_visa_free_tourism_stage1", "CASINO_DUTYFREE_TOURISM", "TOUR_VISA", "중국단체무비자관광 Stage1", "KR", "event_premium", ("tourism_policy", "china_group_tourism"), ("china_dependency", "tourism_policy"), "Visa-free policy is Stage 1 until drop amount, ticket, and OP prove through."),
    Round30CaseCandidate("hotel_shilla_paradise_tourism_candidate", "CASINO_DUTYFREE_TOURISM", "008770_034230", "호텔신라 파라다이스 관광 후보", "KR", "success_candidate", ("visitor_growth_converts_to_op", "drop_amount_growth"), ("china_dependency", "capex"), "Tourism candidate needs visitor mix and OP leverage."),
    Round30CaseCandidate("inspire_resort_underperformance_4c", "CASINO_DUTYFREE_TOURISM", "INSPIRE_4C", "인스파이어 리조트 부진4C", "KR", "4c_thesis_break", ("casino_drop",), ("capex_covenant_failure", "op_leverage_failure"), "Large casino CAPEX can fail when demand and operation underperform."),
    Round30CaseCandidate("dutyfree_china_dependency_counterexample", "CASINO_DUTYFREE_TOURISM", "DUTYFREE_CHINA", "면세중국의존반례", "KR", "failed_rerating", ("dutyfree_sales",), ("china_dependency", "weak_demand"), "Duty-free recovery needs diversified tourist mix."),
    Round30CaseCandidate("cu_overseas_store_efficiency_candidate", "RETAIL_CONVENIENCE_OFFLINE", "CU_STORE", "CU 해외점포 효율 후보", "KR", "success_candidate", ("overseas_store", "store_productivity"), ("rent", "competition"), "Store count matters only when productivity and profit appear."),
    Round30CaseCandidate("gs25_pb_store_efficiency_candidate", "RETAIL_CONVENIENCE_OFFLINE", "GS25_PB", "GS25 PB 점포효율 후보", "KR", "success_candidate", ("pb_high_margin_mix", "same_store_sales_growth"), ("wage", "overcrowding"), "PB mix and same-store sales are stronger than store count."),
    Round30CaseCandidate("convenience_store_wage_rent_pressure_counterexample", "RETAIL_CONVENIENCE_OFFLINE", "CVS_WAGE_RENT", "편의점임대료인건비압박", "KR", "failed_rerating", ("store_network",), ("rent_wage_pressure", "opm_pressure"), "Rent/wage pressure can offset defensive growth."),
    Round30CaseCandidate("convenience_overcrowding_same_store_slowdown_4c", "RETAIL_CONVENIENCE_OFFLINE", "CVS_SSSG_4C", "편의점과밀SSSG둔화4C", "KR", "4c_thesis_break", ("store_network",), ("same_store_sales_slowdown", "overcrowding"), "Overcrowding and SSSG slowdown can break retail visibility."),
    Round30CaseCandidate("smart_farm_export_order_candidate", "AGRI_LIVESTOCK_FOOD_COMMODITY", "SMART_FARM", "스마트팜 수출수주 후보", "KR", "success_candidate", ("smart_farm_order", "export_order"), ("weather", "project_delay"), "Smart-farm export orders need delivery and margin validation."),
    Round30CaseCandidate("tuna_price_fx_candidate", "AGRI_LIVESTOCK_FOOD_COMMODITY", "TUNA_FX", "참치가격환율 후보", "KR", "cyclical_success", ("tuna_price", "cost_pass_through"), ("price_reversal", "fx_hit"), "Tuna price/FX can be cyclical success, not structural Green by default."),
    Round30CaseCandidate("feed_cost_pressure_counterexample", "AGRI_LIVESTOCK_FOOD_COMMODITY", "FEED_COST", "사료원가압박반례", "KR", "failed_rerating", ("feed_cost",), ("feed_cost_spike", "margin_pressure"), "Feed cost can destroy livestock/food margin."),
    Round30CaseCandidate("livestock_disease_event_oneoff", "AGRI_LIVESTOCK_FOOD_COMMODITY", "LIVESTOCK_DISEASE", "축산질병이벤트", "KR", "one_off", ("livestock_price",), ("disease_event_reversal", "price_event_only"), "Disease event is one-off and should not become Green."),
    Round30CaseCandidate("defense_drone_contract_candidate", "SPACE_SUPPLYCHAIN", "DRONE_DEF", "방산드론계약 후보", "KR", "success_candidate", ("actual_delivery_contract", "government_or_defense_customer"), ("certification_delay", "program_delay"), "Drone can score when it is a defense delivery contract, not a theme."),
    Round30CaseCandidate("spacex_supplier_contract_candidate", "SPACE_SUPPLYCHAIN", "SPACEX_SUPPLY", "스페이스X 공급계약 후보", "KR", "success_candidate", ("spacex_supplier", "actual_delivery_contract"), ("no_revenue", "program_delay"), "SpaceX supplier label needs actual delivery and revenue evidence."),
    Round30CaseCandidate("spacex_theme_no_revenue_counterexample", "SPACE_SUPPLYCHAIN", "SPACEX_THEME", "스페이스X테마무매출반례", "KR", "failed_rerating", ("space_keyword",), ("no_contract", "no_revenue"), "SpaceX-related label alone is not score evidence."),
    Round30CaseCandidate("drone_policy_no_contract_counterexample", "SPACE_SUPPLYCHAIN", "DRONE_POLICY", "드론정책무계약반례", "KR", "failed_rerating", ("drone_policy",), ("poc_only", "no_contract"), "Drone policy without contract remains Watch/Red material."),
)


def target_for(target_id: str) -> Round30ScoreTarget | None:
    for target in ROUND30_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round30_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND30_CASE_CANDIDATES:
        target = target_for(candidate.target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {candidate.target_id}")
        weights = target.score_weight.as_dict()
        record = E2RCaseRecord(
            case_id=candidate.case_id,
            symbol=candidate.symbol,
            company_name=candidate.company_name,
            market=candidate.market,
            sector_raw=candidate.target_id,
            primary_archetype=target.canonical_archetype,
            expected_group=candidate.expected_group,
            large_sector=target.large_sector.value,
            case_type=candidate.case_type,
            evidence_summary=(
                f"Round30 v1.5 calibration candidate for {candidate.target_id}; "
                "stage dates, prices, and numeric evidence remain unfilled."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=tuple(field for field in candidate.evidence_fields if field in target.green_conditions),
            stage3_evidence=(),
            stage4c_evidence=candidate.red_flag_fields if candidate.case_type == "4c_thesis_break" else (),
            must_have_fields=target.green_conditions,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason="; ".join(candidate.red_flag_fields) if candidate.case_type not in {"success_candidate", "structural_success", "cyclical_success"} else None,
            score_price_alignment="unknown",
            rerating_result="event_premium" if candidate.case_type == "event_premium" else "unknown",
            price_pattern="unknown",
            score_weight_hint={
                "eps_fcf": float(weights["eps_fcf"]),
                "visibility": float(weights["structural_visibility"]),
                "bottleneck": float(weights["bottleneck_pricing"]),
                "mispricing": float(weights["market_mispricing"]),
                "valuation": float(weights["valuation"]),
                "capital_allocation": float(weights["capital_allocation"]),
                "information_confidence": float(weights["information_confidence"]),
            },
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "require_price_path_validation",
                "require_cross_evidence_for_green",
                "theme_label_is_not_score_evidence",
                *target.red_flags,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(price_validation_status="needs_price_backfill"),
            data_quality=CaseDataQuality(False, False, False, 0.0),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round30_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND30_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "eps_fcf": str(weights["eps_fcf"]),
                "structural_visibility": str(weights["structural_visibility"]),
                "bottleneck_pricing": str(weights["bottleneck_pricing"]),
                "market_mispricing": str(weights["market_mispricing"]),
                "valuation": str(weights["valuation"]),
                "capital_allocation": str(weights["capital_allocation"]),
                "information_confidence": str(weights["information_confidence"]),
                "stage1_signals": "|".join(target.stage1_signals),
                "stage2_signals": "|".join(target.stage2_signals),
                "stage3_conditions": "|".join(target.stage3_conditions),
                "green_conditions": "|".join(target.green_conditions),
                "red_flags": "|".join(target.red_flags),
                "stage4c_conditions": "|".join(target.stage4c_conditions),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round30_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND30_CASE_CANDIDATES:
        target = target_for(candidate.target_id)
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
                "price_validation_status": "needs_price_backfill",
                "production_input": "false",
                "notes": candidate.notes,
            }
        )
    return tuple(rows)


def round30_summary() -> dict[str, int | bool]:
    records = round30_case_records()
    positive = sum(1 for record in records if record.case_type in {"success_candidate", "structural_success", "cyclical_success"})
    stage4c = sum(1 for record in records if record.case_type == "4c_thesis_break")
    stage4b = sum(1 for record in records if record.case_type == "4b_watch")
    return {
        "target_count": len(ROUND30_SCORE_TARGETS),
        "case_candidate_count": len(records),
        "success_candidate_count": positive,
        "counterexample_or_risk_count": len(records) - positive,
        "stage4b_case_count": stage4b,
        "stage4c_case_count": stage4c,
        "green_possible_count": sum(1 for target in ROUND30_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND30_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND30_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round30_score_weight_reports(
    *,
    output_directory: str | Path = ROUND30_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND30_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND30_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round30_score_weight_v15_summary.md",
        "case_matrix": output / "round30_case_candidate_matrix.csv",
        "green_guardrails": output / "round30_green_guardrail_review.md",
        "cycle_cap": output / "round30_cycle_cap_review.md",
        "semicapex_boundary": output / "round30_semicapex_boundary_review.md",
        "price_validation_plan": output / "round30_price_validation_plan.md",
    }
    _write_case_jsonl(round30_case_records(), cases)
    _write_rows(round30_score_profile_rows(), score_profiles)
    _write_rows(round30_case_candidate_rows(), paths["case_matrix"])
    paths["summary"].write_text(render_round30_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round30_green_guardrail_markdown(), encoding="utf-8")
    paths["cycle_cap"].write_text(render_round30_cycle_cap_markdown(), encoding="utf-8")
    paths["semicapex_boundary"].write_text(render_round30_semicapex_boundary_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round30_price_validation_plan_markdown(), encoding="utf-8")
    return paths


def render_round30_summary_markdown() -> str:
    summary = round30_summary()
    lines = [
        "# Round-30 Score-Weight v1.5 Summary",
        "",
        f"- source_round: `{ROUND30_SOURCE_ROUND_PATH}`",
        f"- target_count: {summary['target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- counterexample_or_risk_count: {summary['counterexample_or_risk_count']}",
        f"- stage4b_case_count: {summary['stage4b_case_count']}",
        f"- stage4c_case_count: {summary['stage4c_case_count']}",
        f"- green_possible_count: {summary['green_possible_count']}",
        f"- watch_yellow_first_count: {summary['watch_yellow_first_count']}",
        f"- redteam_first_count: {summary['redteam_first_count']}",
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "- Round 30 adds v1.5 calibration cases and target weights only.",
        "- Example: semi equipment can benefit from HBM CAPEX, but customer CAPEX cuts can still create 4C.",
        "- Example: completed vehicles can be Green-possible when FCF, hybrid/mix, and shareholder return are source-backed.",
        "- Example: airlines, casino/duty-free, convenience retail, agri/livestock, and space/drone themes remain cycle or Watch-first.",
        "- Theme names, policy headlines, store counts, tourism headlines, and price rallies are not score evidence by themselves.",
    ]
    return "\n".join(lines) + "\n"


def render_round30_green_guardrail_markdown() -> str:
    lines = [
        "# Round-30 Green Guardrail Review",
        "",
        "| target | posture | Green unlock evidence | Red flags |",
        "|---|---|---|---|",
    ]
    for target in ROUND30_SCORE_TARGETS:
        lines.append(
            "| "
            f"{target.target_id} | {target.posture.value} | "
            f"{', '.join(target.green_conditions)} | {', '.join(target.red_flags)} |"
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "- Do not apply v1.5 weights to production scoring yet.",
            "- Do not use case IDs or theme labels as candidate-generation input.",
            "- Do not invent stage dates, prices, contract size, OP YoY, ASP, OPM, store productivity, tourist mix, CAPEX, or FCF.",
            "- Do not lower Stage 3-Green thresholds to improve recall.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round30_cycle_cap_markdown() -> str:
    return "\n".join(
        [
            "# Round-30 Cycle Cap Review",
            "",
            "Round 30 marks several families as cycle-heavy even when short-term earnings improve.",
            "",
            "## Cycle-Capped Targets",
            "- AIRLINE_TRAVEL_CYCLE: fuel, FX, demand cycle, cargo mix, and integration cost cap Green.",
            "- CASINO_DUTYFREE_TOURISM: visa or tourism policy is Stage 1 until OP leverage and tourist mix prove through.",
            "- AGRI_LIVESTOCK_FOOD_COMMODITY: feed cost, weather, disease, and commodity prices dominate.",
            "- AUTO_COMPONENTS_TIRE: raw materials and customer concentration cap confidence.",
            "- SPACE_SUPPLYCHAIN: actual contracts matter; space/drone labels are not enough.",
            "",
            "## Example",
            "- If `as_of_date=2024-12-12`, a later report about integration synergy cannot be used to prove the 2024-12-12 stage.",
        ]
    ) + "\n"


def render_round30_semicapex_boundary_markdown() -> str:
    return "\n".join(
        [
            "# Round-30 Semi CAPEX Boundary Review",
            "",
            "HBM can be structurally strong, but HBM equipment/material/PCB suppliers are usually one step removed from the final bottleneck.",
            "",
            "## Green-Like Evidence",
            "- Customer CAPEX is confirmed.",
            "- Supplier order backlog grows.",
            "- Delivery schedule and revenue conversion are visible.",
            "- OP/EPS revisions are source-backed.",
            "- Customer concentration risk is low or improving.",
            "",
            "## Watch / Red Evidence",
            "- HBM, CXL, glass substrate, or AI-chip keyword appears without revenue exposure.",
            "- Customer CAPEX is delayed or cut.",
            "- Inventory builds before delivery conversion.",
            "- Single-customer dependency is high.",
        ]
    ) + "\n"


def render_round30_price_validation_plan_markdown() -> str:
    return "\n".join(
        [
            "# Round-30 Price Validation Plan",
            "",
            "1. Backfill tradable case price paths where symbols exist.",
            "2. Keep synthetic, theme, and reference counterexamples as `needs_price_backfill` or `missing_price_data`.",
            "3. Calculate MFE/MAE, peak, drawdown, and below-entry flags only from source data.",
            "4. Run shadow score-price alignment before any production scoring change.",
            "",
            "## Priority Validation",
            "- Semi equipment: customer CAPEX/order backlog versus CAPEX cut and inventory 4C.",
            "- Auto: FCF, hybrid/mix, return execution versus tariff, recall, peak margin, and raw material risk.",
            "- Travel/tourism: record revenue and policy events versus fuel, FX, visitor mix, OP leverage, and CAPEX underperformance.",
            "- Convenience/agri/space: prove productivity, margin, repeat revenue, and contracts before any Green-like interpretation.",
        ]
    ) + "\n"


def _write_case_jsonl(records: Iterable[E2RCaseRecord], path: Path) -> Path:
    lines = []
    for record in records:
        record.validate()
        lines.append(json.dumps(record.as_dict(), ensure_ascii=False, sort_keys=True))
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return path


def _write_rows(rows: Iterable[Mapping[str, str]], path: Path) -> Path:
    row_tuple = tuple(rows)
    if not row_tuple:
        path.write_text("", encoding="utf-8")
        return path
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(row_tuple[0].keys()))
        writer.writeheader()
        for row in row_tuple:
            writer.writerow(row)
    return path


__all__ = [
    "ROUND30_CASE_CANDIDATES",
    "ROUND30_DEFAULT_CASES_PATH",
    "ROUND30_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND30_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND30_SCORE_TARGETS",
    "ROUND30_SOURCE_ROUND_PATH",
    "Round30CaseCandidate",
    "Round30ScoreTarget",
    "Round30ScoreWeightDraft",
    "render_round30_cycle_cap_markdown",
    "render_round30_green_guardrail_markdown",
    "render_round30_price_validation_plan_markdown",
    "render_round30_semicapex_boundary_markdown",
    "render_round30_summary_markdown",
    "round30_case_candidate_rows",
    "round30_case_records",
    "round30_score_profile_rows",
    "round30_summary",
    "target_for",
    "write_round30_score_weight_reports",
]
