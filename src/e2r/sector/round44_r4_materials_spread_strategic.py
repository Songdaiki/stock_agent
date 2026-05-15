"""Round-44 R4 materials/spread/strategic-resources calibration pack.

Round 44 expands the Round-40 protocol for R4 materials, spread, and
strategic-resource themes. It stores target sub-archetypes, shadow
score-weight drafts, stage-date guidance, case candidates, and
price-validation fields.

This module is calibration/report material only. Production feature
engineering, scoring, staging, and RedTeam code must not import it.
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


ROUND44_SOURCE_ROUND_PATH = "docs/round/round_44.md"
ROUND44_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round44_r4_materials_spread_strategic"
ROUND44_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r4_round44.jsonl"
ROUND44_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round44_r4_v1.csv"


@dataclass(frozen=True)
class Round44ScoreWeightDraft:
    eps_fcf: int
    structural_visibility: int
    bottleneck_pricing: int
    market_mispricing: int
    valuation: int
    capital_allocation: int
    information_confidence: int

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
class Round44ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round44ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    normalization_point: str

    @property
    def large_sector(self) -> Round10LargeSector:
        return Round10LargeSector.MATERIALS_SPREAD_STRATEGIC

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round44CaseCandidate:
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


ROUND44_SCORE_TARGETS: tuple[Round44ScoreTarget, ...] = (
    Round44ScoreTarget(
        "REFINING_OIL_SPREAD",
        E2RArchetype.COMMODITY_SPREAD,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round44ScoreWeightDraft(20, 10, 18, 10, 10, 2, 5),
        ("refining_margin_rebound", "oil_price_or_geopolitical_event", "inventory_gain"),
        ("refining_op_improvement", "core_margin_ex_inventory", "logistics_normalization"),
        ("repeat_fcf", "high_margin_mix", "inventory_noise_excluded"),
        ("refining_margin_peak", "oil_spread_recovery_crowded"),
        ("refining_margin_drop", "inventory_loss", "logistics_or_production_delay"),
        ("repeat_fcf", "core_margin", "inventory_noise_excluded"),
        ("inventory_loss", "refining_margin_drop", "logistics_delay"),
        "Refining is cycle/watch; Green requires repeated FCF and core margin, not inventory gains.",
    ),
    Round44ScoreTarget(
        "CHEMICAL_SPREAD",
        E2RArchetype.COMMODITY_SPREAD,
        Round10ThemePosture.REDTEAM_FIRST,
        Round44ScoreWeightDraft(20, 8, 16, 8, 8, 0, 5),
        ("chemical_spread_recovery", "china_stimulus", "product_price_rebound"),
        ("op_improvement", "spread_improvement", "inventory_normalization"),
        ("supply_glut_easing", "capacity_restructuring", "durable_margin"),
        ("spread_recovery_fully_priced",),
        ("china_middle_east_capacity_glut", "spread_reversal", "inventory_increase", "op_fcf_drop"),
        ("supply_glut_easing", "capacity_restructuring", "durable_margin"),
        ("china_middle_east_capacity_glut", "spread_reversal", "inventory_increase"),
        "Chemicals are RedTeam-first because supply glut can erase temporary spread recovery.",
    ),
    Round44ScoreTarget(
        "STEEL_METAL_SPREAD",
        E2RArchetype.COMMODITY_SPREAD,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round44ScoreWeightDraft(18, 10, 16, 10, 10, 1, 5),
        ("steel_price_rebound", "china_output_cut", "construction_demand_recovery"),
        ("cost_cut", "steel_spread_improvement", "inventory_normalization"),
        ("china_supply_discipline", "demand_recovery", "fcf_margin"),
        ("steel_recovery_crowded",),
        ("chinese_exports_surge", "domestic_demand_weak", "tariff_conflict", "price_pressure"),
        ("supply_discipline", "demand_recovery", "fcf_margin"),
        ("chinese_exports", "construction_demand_weak", "price_pressure"),
        "Steel is Watch because China supply/export pressure can cap structural rerating.",
    ),
    Round44ScoreTarget(
        "NONFERROUS_STRATEGIC_METALS",
        E2RArchetype.RARE_METALS_STRATEGIC_MATERIALS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round44ScoreWeightDraft(18, 14, 15, 12, 11, 2, 5),
        ("copper_zinc_aluminum_price", "smelting_margin", "nonferrous_cycle"),
        ("metal_price_support", "smelting_margin_improvement", "customer_demand"),
        ("cost_curve_advantage", "supply_constraint", "fcf_conversion"),
        ("nonferrous_price_rally_crowded",),
        ("metal_price_drop", "china_demand_slowdown", "smelting_margin_drop"),
        ("cost_curve_advantage", "supply_constraint", "fcf_conversion"),
        ("metal_price_drop", "china_demand", "margin_drop"),
        "Nonferrous metals need cost-curve and smelting-margin evidence; price alone is cycle.",
    ),
    Round44ScoreTarget(
        "RARE_METALS_STRATEGIC_MATERIALS",
        E2RArchetype.RARE_METALS_STRATEGIC_MATERIALS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round44ScoreWeightDraft(18, 18, 18, 14, 13, 5, 5),
        ("rare_earth_export_control", "defense_supply_chain", "government_supply_policy"),
        ("government_investment", "price_floor", "offtake_contract", "long_term_purchase"),
        ("production_capacity", "fcf_conversion", "policy_support_durable", "customer_contracts"),
        ("rare_earth_theme_overheat", "price_only_rally"),
        ("project_delay", "rare_earth_price_drop", "policy_support_cut", "execution_failure"),
        ("government_investment", "price_floor", "offtake_contract", "production_capacity", "fcf_conversion"),
        ("project_delay", "policy_dependency", "price_only_rally"),
        "Rare metals can move toward Green only with government support, price floor, offtake, production, and FCF.",
    ),
    Round44ScoreTarget(
        "LITHIUM_BATTERY_RAW_MATERIAL",
        E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round44ScoreWeightDraft(19, 10, 16, 9, 8, 0, 5),
        ("lithium_price_rebound", "mine_closure", "ev_or_ess_demand"),
        ("low_cost_mine", "offtake", "fcf_defense", "capex_discipline"),
        ("price_cycle_beyond_rebound", "durable_fcf", "restart_supply_risk_controlled"),
        ("lithium_rebound_crowded",),
        ("lithium_price_crash", "mine_restart_supply_rebound", "ev_demand_slowdown", "capex_cut"),
        ("low_cost_mine", "offtake", "fcf_defense", "capex_discipline"),
        ("price_crash", "mine_restart", "ev_demand_slowdown"),
        "Lithium is cycle/watch; low-cost FCF and offtake must be proven before stronger stages.",
    ),
    Round44ScoreTarget(
        "PRECIOUS_METALS_SAFE_HAVEN_MINERS",
        E2RArchetype.COMMODITY_SPREAD,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round44ScoreWeightDraft(20, 10, 16, 9, 8, 5, 5),
        ("gold_silver_breakout", "real_rate_drop", "safe_haven_demand"),
        ("realized_price", "aisc_control", "fcf_improvement", "buyback_or_dividend"),
        ("cost_control", "capital_return", "production_stable", "fcf_conversion"),
        ("record_gold_price_crowded", "miner_group_overheat"),
        ("gold_price_correction", "aisc_rise", "production_drop", "political_mine_risk"),
        ("realized_price", "aisc_control", "capital_return", "fcf_conversion"),
        ("gold_price_correction", "aisc_rise", "mine_risk"),
        "Precious-metal miners can work, but they remain cycle/watch unless cost and capital returns persist.",
    ),
    Round44ScoreTarget(
        "ADVANCED_MATERIAL_SPECULATIVE_THEME",
        E2RArchetype.THEME_VALUATION_OVERHEAT,
        Round10ThemePosture.REDTEAM_FIRST,
        Round44ScoreWeightDraft(5, 5, 5, 5, 5, 0, 3),
        ("superconductor_graphene_mxene_theme", "paper_or_lab_result", "quantum_material_keyword"),
        ("commercial_contract", "qualified_customer", "revenue_conversion"),
        ("commercial_revenue", "repeat_customer", "fcf_path"),
        ("speculative_material_theme_overheat",),
        ("no_commercialization", "paper_only", "no_revenue", "dilution"),
        ("commercial_contract", "revenue_conversion", "fcf_path"),
        ("paper_only", "no_revenue", "theme_only"),
        "Speculative advanced materials are RedTeam-first until commercialization and revenue exist.",
    ),
    Round44ScoreTarget(
        "PAPER_PACKAGING_CYCLE",
        E2RArchetype.COMMODITY_SPREAD,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round44ScoreWeightDraft(17, 13, 12, 10, 9, 3, 5),
        ("paper_or_corrugated_spread", "ecommerce_packaging", "plastic_replacement"),
        ("volume_recovery", "price_cost_spread", "mna_or_consolidation"),
        ("durable_spread", "scale_economics", "cash_return"),
        ("packaging_mna_premium_crowded",),
        ("low_volume", "price_pressure", "regulatory_divestiture", "mature_industry_limit"),
        ("volume_recovery", "price_cost_spread", "cash_return"),
        ("low_volume", "price_pressure", "mature_industry"),
        "Packaging is mature and cyclical; consolidation premium is not structural evidence by itself.",
    ),
    Round44ScoreTarget(
        "AGRI_COMMODITY_INPUTS",
        E2RArchetype.COMMODITY_SPREAD,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round44ScoreWeightDraft(18, 10, 14, 8, 8, 0, 5),
        ("grain_price", "weather_event", "disease_or_feed_cost", "fertilizer_price"),
        ("price_pass_through", "inventory_status", "demand_visibility"),
        ("repeat_margin", "cost_pass_through", "fcf_margin"),
        ("agri_event_crowded",),
        ("commodity_cost_reversal", "weather_normalization", "inventory_loss"),
        ("price_pass_through", "repeat_margin", "fcf_margin"),
        ("weather_event_only", "inventory_loss", "commodity_reversal"),
        "Agri inputs are event/watch because weather, disease, and commodity costs can reverse.",
    ),
    Round44ScoreTarget(
        "LNG_ENERGY_TRADING_DISTRIBUTION",
        E2RArchetype.COMMODITY_SPREAD,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round44ScoreWeightDraft(18, 15, 16, 10, 10, 2, 5),
        ("lng_long_term_offtake", "lpg_or_fuel_distribution", "energy_procurement_stability"),
        ("long_term_contract", "margin_visible", "inventory_status"),
        ("repeat_fcf", "project_stake", "energy_security_value"),
        ("lng_contract_story_crowded",),
        ("price_reversal", "inventory_loss", "tariff_policy_shock", "financing_delay"),
        ("long_term_contract", "margin_visible", "repeat_fcf", "project_stake"),
        ("price_reversal", "inventory_loss", "financing_delay"),
        "LNG trading/distribution can become Watch-to-Green with long contracts and FCF, not price exposure alone.",
    ),
    Round44ScoreTarget(
        "GENERAL_TRADING_RESOURCE_INFRA",
        E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round44ScoreWeightDraft(17, 19, 12, 15, 18, 8, 5),
        ("resource_rights", "energy_contract", "buyback_dividend", "conglomerate_discount_rerating"),
        ("long_term_offtake", "project_stake", "fcf", "capital_return"),
        ("resource_infra_fcf_frame", "capital_allocation_execution", "valuation_discount_narrows"),
        ("sogo_shosha_story_crowded", "resource_infra_rerating_full"),
        ("commodity_price_drop", "project_delay", "capital_allocation_retreat", "fx_hit"),
        ("long_term_offtake", "project_stake", "fcf", "capital_return"),
        ("commodity_cycle", "project_delay", "capital_allocation_retreat"),
        "Trading houses rerate on resource/infra FCF plus capital allocation, not sales scale alone.",
    ),
    Round44ScoreTarget(
        "ENERGY_UTILITY_LNG_GAS",
        E2RArchetype.UTILITIES_REGULATED_TARIFF,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round44ScoreWeightDraft(17, 18, 6, 12, 10, 5, 5),
        ("lng_gas_utility", "tariff_or_cost_pass_through", "uncollected_receivable_recovery"),
        ("tariff_visibility", "debt_stability", "cash_flow_recovery"),
        ("regulated_cost_pass_through", "debt_reduction", "capital_return_capacity"),
        ("gas_utility_turnaround_crowded",),
        ("tariff_freeze", "debt_burden", "receivable_growth", "policy_risk"),
        ("tariff_visibility", "cash_flow_recovery", "debt_reduction"),
        ("tariff_freeze", "debt_burden", "policy_risk"),
        "LNG/gas utilities are regulated Watch; tariff and debt evidence matter more than commodity price.",
    ),
)


ROUND44_CASE_CANDIDATES: tuple[Round44CaseCandidate, ...] = (
    Round44CaseCandidate(
        "mp_materials_dod_apple_offtake_case",
        "RARE_METALS_STRATEGIC_MATERIALS",
        "MP",
        "MP Materials 국방부·Apple offtake",
        "US",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("government_investment", "price_floor", "offtake_contract", "long_term_purchase", "supply_chain_security"),
        ("project_execution", "policy_dependency", "rare_earth_price_drop"),
        "structural_success_candidate",
        "needs_source_date_and_price_backfill",
        ("AP MP Materials Pentagon Apple agreements",),
        "Rare-earth theme becomes higher quality when government investment, price floor, and long-term offtake are all present.",
    ),
    Round44CaseCandidate(
        "china_rare_earth_export_control_bottleneck_case",
        "RARE_METALS_STRATEGIC_MATERIALS",
        "RARE_EARTH_CONTROL_REF",
        "중국 희토류 수출통제 병목",
        "GLOBAL",
        "event_premium",
        None,
        date(2026, 5, 13),
        None,
        None,
        None,
        ("rare_earth_export_control", "heavy_rare_earth_shortage", "geopolitical_bottleneck"),
        ("price_only_rally", "no_production_capacity", "policy_reversal"),
        "geopolitical_bottleneck_reference",
        "missing_direct_symbol_mapping",
        ("Reuters rare earth export controls",),
        "Export-control news routes research but cannot create company-level Green without production, offtake, and FCF.",
    ),
    Round44CaseCandidate(
        "korea_zinc_tender_event_premium_case",
        "NONFERROUS_STRATEGIC_METALS",
        "010130",
        "Korea Zinc 공개매수 이벤트",
        "KR",
        "event_premium",
        None,
        date(2024, 9, 13),
        None,
        None,
        None,
        ("tender_offer", "governance_event", "strategic_metal_exposure", "event_day_price_reaction"),
        ("event_premium", "governance_dispute", "fcf_not_verified"),
        "event_premium_governance_watch",
        "needs_price_backfill",
        ("Reuters Korea Zinc tender offer",),
        "The price reaction should be separated from structural smelting/FCF rerating.",
        (E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE,),
    ),
    Round44CaseCandidate(
        "berkshire_japan_sogo_shosha_case",
        "GENERAL_TRADING_RESOURCE_INFRA",
        "JP_TRADING_HOUSES_REF",
        "Berkshire 일본 5대 상사 투자",
        "JP",
        "structural_success",
        None,
        date(2025, 3, 17),
        None,
        None,
        None,
        ("resource_infra_fcf", "capital_return", "conglomerate_discount_rerating", "buyback_dividend"),
        ("commodity_cycle", "fx_risk", "complex_conglomerate_discount"),
        "structural_reference_case",
        "needs_price_backfill",
        ("Financial Times Berkshire Japanese trading houses",),
        "Trading houses can rerate when resource/infra FCF and capital allocation change the market frame.",
    ),
    Round44CaseCandidate(
        "posco_international_alaska_lng_20y_case",
        "GENERAL_TRADING_RESOURCE_INFRA",
        "047050",
        "POSCO International Alaska LNG 20년 계약",
        "KR",
        "success_candidate",
        None,
        date(2025, 12, 4),
        None,
        None,
        None,
        ("twenty_year_lng_supply", "project_stake", "steel_supply", "long_term_offtake"),
        ("fid_pending", "financing_risk", "lng_price_risk", "project_delay"),
        "watch_to_green_candidate",
        "needs_price_backfill",
        ("Reuters POSCO Alaska LNG deal",),
        "Long-term LNG contract plus project stake is stronger than spot-price exposure, but FID and margin remain gates.",
        (E2RArchetype.COMMODITY_SPREAD,),
    ),
    Round44CaseCandidate(
        "barrick_record_gold_buyback_case",
        "PRECIOUS_METALS_SAFE_HAVEN_MINERS",
        "GOLD",
        "Barrick record gold and buyback",
        "US",
        "cyclical_success",
        None,
        date(2026, 5, 11),
        None,
        None,
        None,
        ("record_gold_price", "realized_price", "aisc_control", "buyback_amount", "net_income_growth"),
        ("gold_price_correction", "aisc_rise", "mine_political_risk"),
        "cyclical_success_candidate",
        "needs_price_backfill",
        ("Reuters Barrick Q1 profit and buyback",),
        "Gold price, cost control, and buyback can work, but this remains commodity/cycle until durability is proven.",
    ),
    Round44CaseCandidate(
        "sk_innovation_refining_recovery_watch",
        "REFINING_OIL_SPREAD",
        "096770",
        "SK Innovation 정유 흑자전환",
        "KR",
        "cyclical_success",
        None,
        date(2026, 5, 13),
        None,
        None,
        None,
        ("refining_op_improvement", "earnings_beat", "refining_recovery"),
        ("recovery_delay_warning", "refining_margin_reversal", "inventory_loss"),
        "cyclical_recovery_candidate",
        "needs_price_backfill",
        ("Reuters SK Innovation Q1 profit",),
        "Strong profit is cycle/watch because the company warned recovery could take time.",
    ),
    Round44CaseCandidate(
        "lg_chem_lotte_chemical_oversupply_4c",
        "CHEMICAL_SPREAD",
        "KR_CHEMICALS_REF",
        "LG Chem / Lotte Chemical 공급과잉",
        "KR",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2025, 2, 7),
        ("chemical_spread_story",),
        ("china_middle_east_capacity_glut", "operating_loss", "op_profit_collapse", "spread_reversal"),
        "hard_counterexample_for_chemical_green",
        "needs_price_backfill",
        ("Reuters Korean petrochemical oversupply",),
        "Chemical Green is blocked when China/Middle East capacity and spread reversal crush OP/FCF.",
    ),
    Round44CaseCandidate(
        "baosteel_steel_oversupply_cost_cut_case",
        "STEEL_METAL_SPREAD",
        "BAOSTEEL_REF",
        "Baosteel 철강 공급과잉·비용절감",
        "CN",
        "cyclical_success",
        None,
        date(2025, 4, 28),
        None,
        None,
        None,
        ("cost_cut", "q1_profit_increase", "output_cut_expectation"),
        ("overcapacity", "weak_demand", "chinese_exports_surge"),
        "cost_cut_cycle_success",
        "missing_public_price_data",
        ("Reuters Baosteel output cuts",),
        "Cost cuts and output cuts can lift price, but steel remains capped by Chinese supply/export pressure.",
    ),
    Round44CaseCandidate(
        "bhp_iron_ore_profit_dividend_cut_case",
        "STEEL_METAL_SPREAD",
        "BHP",
        "BHP 철광석 이익·배당 축소",
        "AU",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2025, 8, 18),
        ("iron_ore_cycle", "capital_return"),
        ("iron_ore_price_drop", "china_demand_slowdown", "profit_low", "dividend_cut"),
        "iron_ore_downcycle_4c",
        "needs_price_backfill",
        ("Reuters BHP profit and dividend cut",),
        "Commodity downturn can reduce both FCF and capital return, damaging the structural thesis.",
    ),
    Round44CaseCandidate(
        "lithium_price_86pct_crash_case",
        "LITHIUM_BATTERY_RAW_MATERIAL",
        "LITHIUM_CYCLE_REF",
        "리튬 가격 86% 급락",
        "GLOBAL",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2025, 1, 13),
        ("lithium_price_cycle", "mine_shutdown"),
        ("lithium_price_crash", "mine_restart_supply_rebound", "ev_demand_slowdown", "capex_cut"),
        "lithium_4c_cycle",
        "missing_price_data",
        ("Reuters lithium prices stabilize after crash",),
        "Lithium price rebound is not structural when mine restarts can cap the cycle.",
        (E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT,),
    ),
    Round44CaseCandidate(
        "ds_smith_packaging_consolidation_case",
        "PAPER_PACKAGING_CYCLE",
        "DS_SMITH_REF",
        "DS Smith 포장재 consolidation",
        "EU",
        "event_premium",
        None,
        date(2024, 3, 7),
        None,
        None,
        None,
        ("packaging_consolidation", "mna_premium", "scale_economics_candidate"),
        ("low_volume", "price_pressure", "mature_industry_limit", "regulatory_divestiture"),
        "mature_consolidation_event_premium",
        "missing_public_price_data",
        ("Reuters Mondi DS Smith", "Reuters International Paper divestiture",),
        "Packaging M&A premium must be separated from durable spread and cash-return evidence.",
    ),
    Round44CaseCandidate(
        "advanced_material_speculative_theme_counterexample",
        "ADVANCED_MATERIAL_SPECULATIVE_THEME",
        "ADV_MATERIAL_THEME_REF",
        "초전도체·그래핀·맥신 테마 반례",
        "GLOBAL",
        "overheat",
        None,
        None,
        None,
        None,
        None,
        ("superconductor_graphene_mxene_theme", "paper_or_lab_result"),
        ("paper_only", "no_revenue", "no_commercialization", "theme_only"),
        "price_moved_without_evidence",
        "missing_price_data",
        ("Round44 speculative advanced materials note",),
        "Lab or paper narratives are not scoring evidence before commercialization and revenue.",
    ),
    Round44CaseCandidate(
        "chemical_spread_recovery_false_positive",
        "CHEMICAL_SPREAD",
        "CHEMICAL_SPREAD_REF",
        "화학 spread 회복 오판 반례",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("chemical_spread_recovery", "product_price_rebound"),
        ("china_middle_east_capacity_glut", "spread_reversal", "inventory_increase"),
        "false_positive_score_risk",
        "missing_price_data",
        ("Round44 chemical spread warning",),
        "Product spread recovery should not become Green without supply-glut easing and durable FCF.",
    ),
    Round44CaseCandidate(
        "rare_metals_theme_price_only_4b_watch",
        "RARE_METALS_STRATEGIC_MATERIALS",
        "RARE_THEME_4B_REF",
        "희토류 테마 price-only 4B-watch",
        "GLOBAL",
        "4b_watch",
        None,
        None,
        None,
        None,
        None,
        ("rare_earth_export_control", "price_only_rally"),
        ("no_production_capacity", "no_offtake", "no_fcf", "policy_reversal"),
        "rare_metals_4b_watch",
        "missing_price_data",
        ("Round44 rare metals 4B note",),
        "Rare-earth headlines can create 4B-watch when price moves before production, offtake, and FCF.",
    ),
)


ROUND44_PRICE_FIELDS: tuple[str, ...] = (
    "case_id",
    "symbol",
    "company_name",
    "primary_archetype",
    "secondary_archetypes",
    "stage1_date",
    "stage2_date",
    "stage3_date",
    "stage4b_date",
    "stage4c_date",
    "stage1_price",
    "stage2_price",
    "stage3_price",
    "stage4b_price",
    "stage4c_price",
    "peak_price",
    "MFE_30D",
    "MFE_90D",
    "MFE_180D",
    "MFE_1Y",
    "MFE_2Y",
    "MAE_30D",
    "MAE_90D",
    "MAE_180D",
    "MAE_1Y",
    "drawdown_after_peak",
    "below_stage3_price_flag",
    "commodity_price_at_stage",
    "commodity_price_peak",
    "commodity_price_change_90D",
    "commodity_price_change_1Y",
    "spread_metric",
    "spread_change",
    "inventory_gain_loss",
    "revenue_revision_1q",
    "op_revision_1q",
    "eps_revision_1y",
    "fcf_margin",
    "dividend_change",
    "buyback_amount",
    "offtake_contract_flag",
    "price_floor_flag",
    "government_support_flag",
    "tender_offer_flag",
    "governance_event_flag",
    "capex_cut_flag",
    "oversupply_flag",
    "supply_glut_flag",
    "score_price_alignment",
    "price_validation_status",
)


def target_for(target_id: str) -> Round44ScoreTarget | None:
    for target in ROUND44_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round44_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND44_CASE_CANDIDATES:
        target = target_for(candidate.target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {candidate.target_id}")
        weights = target.score_weight.as_dict()
        stage4b_evidence = candidate.evidence_fields if candidate.case_type == "4b_watch" or candidate.stage4b_date else ()
        stage4c_evidence = candidate.red_flag_fields if candidate.case_type == "4c_thesis_break" or candidate.stage4c_date else ()
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
                f"Round44 R4 case for {candidate.target_id}; "
                "case evidence is calibration-only and missing prices remain unfilled."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage2_signals or field in target.green_conditions),
            stage3_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage3_conditions),
            stage4b_evidence=stage4b_evidence,
            stage4c_evidence=stage4c_evidence,
            must_have_fields=target.green_conditions,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason="; ".join(candidate.red_flag_fields) if candidate.case_type in {"failed_rerating", "event_premium", "overheat", "4b_watch", "4c_thesis_break"} else None,
            score_price_alignment=_score_price_alignment(candidate),
            rerating_result=_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
            score_weight_hint={
                "eps_fcf": float(weights["eps_fcf"]),
                "visibility": float(weights["structural_visibility"]),
                "bottleneck": float(weights["bottleneck_pricing"]),
                "mispricing": float(weights["market_mispricing"]),
                "valuation": float(weights["valuation"]),
                "capital_allocation": float(weights["capital_allocation"]),
            },
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "require_price_path_validation",
                "require_cross_evidence_for_green",
                "theme_label_is_not_score_evidence",
                "commodity_price_is_not_structural_evidence",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=False,
                price_data_available=False,
                stage_dates_confidence=0.7 if candidate.stage2_date or candidate.stage4b_date or candidate.stage4c_date else 0.3,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round44_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND44_SCORE_TARGETS:
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
                "stage4b_conditions": "|".join(target.stage4b_conditions),
                "stage4c_conditions": "|".join(target.stage4c_conditions),
                "green_conditions": "|".join(target.green_conditions),
                "red_flags": "|".join(target.red_flags),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round44_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND44_CASE_CANDIDATES:
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


def round44_stage_date_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND44_SCORE_TARGETS:
        rows.append(
            {
                "target_id": target.target_id,
                "stage1": "|".join(target.stage1_signals),
                "stage2": "|".join(target.stage2_signals),
                "stage3": "|".join(target.stage3_conditions),
                "stage4b": "|".join(target.stage4b_conditions),
                "stage4c": "|".join(target.stage4c_conditions),
                "production_scoring_changed": "false",
            }
        )
    return tuple(rows)


def round44_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round44_backfill": "true"} for field in ROUND44_PRICE_FIELDS)


def round44_summary() -> dict[str, int | bool]:
    records = round44_case_records()
    return {
        "target_count": len(ROUND44_SCORE_TARGETS),
        "case_candidate_count": len(records),
        "structural_success_count": sum(1 for record in records if record.case_type == "structural_success"),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for record in records if record.case_type == "cyclical_success"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "overheat_count": sum(1 for record in records if record.case_type == "overheat"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch"),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND44_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND44_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND44_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round44_r4_reports(
    *,
    output_directory: str | Path = ROUND44_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND44_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND44_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round44_r4_materials_spread_strategic_summary.md",
        "case_matrix": output / "round44_r4_case_matrix.csv",
        "stage_date_plan": output / "round44_r4_stage_date_plan.csv",
        "green_guardrails": output / "round44_r4_green_guardrails.md",
        "price_validation_plan": output / "round44_r4_price_validation_plan.md",
        "price_fields": output / "round44_r4_price_fields.csv",
    }
    _write_case_jsonl(round44_case_records(), cases)
    _write_rows(round44_score_profile_rows(), score_profiles)
    _write_rows(round44_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round44_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round44_price_field_rows(), paths["price_fields"])
    paths["summary"].write_text(render_round44_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round44_green_guardrail_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round44_price_validation_plan_markdown(), encoding="utf-8")
    return paths


def render_round44_summary_markdown() -> str:
    summary = round44_summary()
    lines = [
        "# Round-44 R4 Materials / Spread / Strategic Resources Summary",
        "",
        f"- source_round: `{ROUND44_SOURCE_ROUND_PATH}`",
        "- large_sector: `MATERIALS_SPREAD_STRATEGIC`",
        f"- target_count: {summary['target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- structural_success_count: {summary['structural_success_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- cyclical_success_count: {summary['cyclical_success_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- overheat_count: {summary['overheat_count']}",
        f"- failed_rerating_count: {summary['failed_rerating_count']}",
        f"- stage4b_case_count: {summary['stage4b_case_count']}",
        f"- stage4c_case_count: {summary['stage4c_case_count']}",
        f"- green_possible_count: {summary['green_possible_count']}",
        f"- watch_yellow_first_count: {summary['watch_yellow_first_count']}",
        f"- redteam_first_count: {summary['redteam_first_count']}",
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "",
        "- R4 should separate structural rerating from commodity cycles, price rallies, and event premiums.",
        "- Example: rare-earth export controls route research, but company-level Green needs production capacity, offtake, price floor, and FCF.",
        "- Example: Korea Zinc tender news can move price sharply, but it is event premium until core FCF, smelting margin, and capital allocation evidence are verified.",
    ]
    return "\n".join(lines) + "\n"


def render_round44_green_guardrail_markdown() -> str:
    lines = [
        "# Round-44 R4 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Red flags |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND44_SCORE_TARGETS:
        lines.append(
            "| "
            f"`{target.target_id}` | {target.posture.value} | "
            f"{', '.join(target.green_conditions)} | {', '.join(target.red_flags)} |"
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not apply these R4 v1.0 weights to production scoring yet.",
            "- Do not treat commodity price rallies, spread headlines, tender offers, policy events, or theme labels as score evidence by themselves.",
            "- Do not invent commodity price, spread, offtake, price floor, FCF, dividend, buyback, or price-path fields.",
            "- Do not lower Stage 3-Green for commodity cycles. Most R4 paths should remain Watch/Cycle/Event until FCF durability is proven.",
            "- Treat supply glut, price crash, project delay, dividend cut, inventory loss, and no-commercialization advanced materials as RedTeam evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round44_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-44 R4 Price Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign stage dates from source evidence only.",
        "2. Store stage-date close prices from official price data.",
        "3. Calculate MFE_30D / 90D / 180D / 1Y / 2Y.",
        "4. Calculate MAE_30D / 90D / 180D / 1Y.",
        "5. Calculate peak price, drawdown after peak, and below-stage3 flag.",
        "6. Compare price paths with commodity price, product spread, EPS revision, FCF, dividend, buyback, offtake, price floor, and supply-glut evidence.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | stage candidate | check |",
        "| --- | --- | --- |",
    ]
    priority = {"mp_materials_dod_apple_offtake_case", "rare_metals_theme_price_only_4b_watch"}
    for row in round44_case_candidate_rows():
        if row["stage2_date"] or row["stage4b_date"] or row["stage4c_date"] or row["case_id"] in priority:
            stage_date = row["stage2_date"] or row["stage4b_date"] or row["stage4c_date"] or "needs_source_date"
            lines.append(f"| `{row['case_id']}` | {stage_date} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `structural_success`: price floor, offtake, long contract, FCF, and capital allocation persist together.",
            "- `cyclical_success`: commodity price or spread drove EPS and price, but structural durability is not proven.",
            "- `event_premium`: tender, control, M&A, or policy event moved price before core economics were verified.",
            "- `false_positive_score`: price/spread news looked strong but EPS/FCF durability failed.",
            "- `thesis_break`: supply glut, price crash, project delay, dividend cut, or inventory loss damages the thesis.",
        ]
    )
    return "\n".join(lines) + "\n"


def _score_price_alignment(candidate: Round44CaseCandidate) -> str:
    if "structural" in candidate.alignment_hint and candidate.case_type == "structural_success":
        return "aligned"
    if candidate.case_type in {"event_premium", "overheat", "4b_watch"}:
        return "price_moved_without_evidence"
    if candidate.case_type in {"failed_rerating", "4c_thesis_break"}:
        return "false_positive_score"
    return "unknown"


def _rerating_result(candidate: Round44CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "true_rerating"
    if candidate.case_type == "cyclical_success":
        return "cyclical_rerating"
    if candidate.case_type == "event_premium":
        return "event_premium"
    if candidate.case_type == "overheat":
        return "theme_overheat"
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    if candidate.case_type == "failed_rerating":
        return "no_rerating"
    return "unknown"


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
        writer = csv.DictWriter(handle, fieldnames=tuple(row_tuple[0].keys()), lineterminator="\n")
        writer.writeheader()
        for row in row_tuple:
            writer.writerow(row)
    return path


__all__ = [
    "ROUND44_CASE_CANDIDATES",
    "ROUND44_DEFAULT_CASES_PATH",
    "ROUND44_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND44_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND44_PRICE_FIELDS",
    "ROUND44_SCORE_TARGETS",
    "ROUND44_SOURCE_ROUND_PATH",
    "Round44CaseCandidate",
    "Round44ScoreTarget",
    "Round44ScoreWeightDraft",
    "render_round44_green_guardrail_markdown",
    "render_round44_price_validation_plan_markdown",
    "render_round44_summary_markdown",
    "round44_case_candidate_rows",
    "round44_case_records",
    "round44_price_field_rows",
    "round44_score_profile_rows",
    "round44_stage_date_rows",
    "round44_summary",
    "target_for",
    "write_round44_r4_reports",
]
