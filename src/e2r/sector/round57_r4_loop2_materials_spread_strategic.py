"""Round-57 R4 Loop-2 materials, spread, and strategic-resources pack.

Round 57 tightens the R4 rules by separating commodity price/spread cycles
from structural supply-chain rerating. It is calibration/report material only:
production feature engineering, scoring, staging, and RedTeam code must not
import it.
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


ROUND57_SOURCE_ROUND_PATH = "docs/round/round_57.md"
ROUND57_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round57_r4_loop2_materials_spread_strategic"
ROUND57_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r4_loop2_round57.jsonl"
ROUND57_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round57_r4_loop2_v2.csv"


@dataclass(frozen=True)
class Round57ScoreWeightDraft:
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
class Round57ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round57ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    loop2_penalty_axes: tuple[str, ...]
    normalization_point: str

    @property
    def large_sector(self) -> Round10LargeSector:
        return Round10LargeSector.MATERIALS_SPREAD_STRATEGIC

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round57CaseCandidate:
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


ROUND57_SCORE_TARGETS: tuple[Round57ScoreTarget, ...] = (
    Round57ScoreTarget(
        "REFINING_OIL_SPREAD",
        E2RArchetype.REFINING_OIL_SPREAD,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round57ScoreWeightDraft(20, 10, 18, 10, 9, 2, 5),
        ("refining_margin", "inventory_gain", "oil_price_or_geopolitical_event", "logistics_normalization"),
        ("core_refining_margin", "inventory_noise_excluded", "op_revision_1q", "fcf_margin"),
        ("repeat_fcf", "core_margin_durable", "inventory_noise_excluded"),
        ("refining_margin_peak", "inventory_gain_crowded", "spread_recovery_fully_priced"),
        ("refining_margin_drop", "inventory_loss", "logistics_delay", "demand_slowdown"),
        ("repeat_fcf", "core_margin_durable", "inventory_noise_excluded"),
        ("inventory_loss", "refining_margin_drop", "temporary_crack_spread"),
        ("inventory_gain_loss", "refining_margin", "commodity_price"),
        "Refining is Watch: inventory gains and crack spread rebounds are not durable FCF by themselves.",
    ),
    Round57ScoreTarget(
        "CHEMICAL_SPREAD",
        E2RArchetype.CHEMICAL_SPREAD,
        Round10ThemePosture.REDTEAM_FIRST,
        Round57ScoreWeightDraft(20, 7, 16, 8, 7, 0, 5),
        ("chemical_spread", "product_price_rebound", "china_stimulus", "inventory_restocking"),
        ("spread_change_90d", "op_revision_1q", "capacity_shutdown", "inventory_normalization"),
        ("durable_spread", "supply_glut_easing", "fcf_margin"),
        ("chemical_spread_recovery_crowded",),
        ("china_middle_east_capacity_glut", "supply_glut", "spread_reversal", "inventory_increase", "op_fcf_drop"),
        ("supply_glut_easing", "capacity_restructuring", "durable_fcf"),
        ("china_middle_east_capacity_glut", "spread_reversal", "supply_glut", "inventory_increase"),
        ("oversupply", "supply_glut", "china_middle_east_capacity"),
        "Chemicals are RedTeam-first because spread recovery often fails before FCF becomes structural.",
    ),
    Round57ScoreTarget(
        "STEEL_METAL_SPREAD",
        E2RArchetype.STEEL_METAL_SPREAD,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round57ScoreWeightDraft(18, 9, 16, 10, 9, 1, 5),
        ("steel_spread", "iron_ore_price", "china_output_cut", "construction_demand"),
        ("steel_spread_improvement", "cost_cut", "op_revision_1q", "inventory_normalization"),
        ("supply_discipline", "demand_recovery", "fcf_margin"),
        ("steel_recovery_crowded", "dividend_expectation_full"),
        ("china_exports_surge", "construction_demand_weak", "iron_ore_price_drop", "dividend_cut"),
        ("supply_discipline", "demand_recovery", "fcf_margin"),
        ("chinese_exports", "demand_weak", "dividend_cut", "price_pressure"),
        ("steel_spread", "china_supply", "dividend_change"),
        "Steel and iron ore are Watch; China supply, demand, and dividends decide whether the story survives.",
    ),
    Round57ScoreTarget(
        "NONFERROUS_STRATEGIC_METALS",
        E2RArchetype.NONFERROUS_STRATEGIC_METALS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round57ScoreWeightDraft(18, 14, 15, 12, 11, 2, 5),
        ("copper_zinc_aluminum_price", "smelting_margin", "ai_grid_demand", "mine_disruption"),
        ("smelting_margin", "customer_demand", "op_revision_1q", "fcf_margin"),
        ("cost_curve_advantage", "supply_constraint", "fcf_conversion"),
        ("nonferrous_price_rally_crowded", "event_premium_confused_with_fcf"),
        ("metal_price_drop", "china_demand_slowdown", "smelting_margin_drop", "governance_event_only"),
        ("cost_curve_advantage", "supply_constraint", "fcf_conversion"),
        ("metal_price_drop", "smelting_margin_drop", "event_premium", "governance_dispute"),
        ("smelting_margin", "commodity_price", "event_premium"),
        "Nonferrous metals need smelting-margin and FCF evidence; tender offers are event premiums.",
    ),
    Round57ScoreTarget(
        "RARE_METALS_STRATEGIC_MATERIALS",
        E2RArchetype.RARE_METALS_STRATEGIC_MATERIALS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round57ScoreWeightDraft(18, 20, 18, 14, 13, 5, 5),
        ("rare_earth_export_control", "defense_supply_chain", "government_supply_policy", "strategic_supply_chain"),
        ("government_investment", "price_floor", "offtake_contract", "production_capacity", "customer_contract"),
        ("price_floor", "offtake_contract", "production_ramp", "fcf_conversion", "policy_support_durable"),
        ("rare_earth_price_spike_crowded", "price_only_rally"),
        ("project_delay", "policy_support_cut", "rare_earth_price_drop", "execution_failure"),
        ("government_support", "price_floor", "offtake_contract", "production_capacity", "fcf_conversion"),
        ("no_production_capacity", "no_offtake", "no_price_floor", "project_delay", "policy_dependency"),
        ("price_floor", "offtake", "government_support", "production_capacity"),
        "Rare metals can move toward Green only when price floor, offtake, government support, production, and FCF are visible.",
    ),
    Round57ScoreTarget(
        "LITHIUM_BATTERY_RAW_MATERIAL",
        E2RArchetype.LITHIUM_BATTERY_RAW_MATERIAL,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round57ScoreWeightDraft(18, 9, 16, 9, 7, 0, 5),
        ("lithium_price_rebound", "mine_shutdown", "ev_or_ess_demand", "capex_cut"),
        ("low_cost_mine", "offtake_contract", "fcf_defense", "capex_discipline"),
        ("durable_fcf", "restart_supply_risk_controlled", "low_cost_position"),
        ("lithium_rebound_crowded",),
        ("lithium_price_crash", "mine_restart", "ev_demand_slowdown", "capex_cut", "supply_rebound"),
        ("low_cost_mine", "offtake_contract", "fcf_defense", "capex_discipline"),
        ("price_crash", "mine_restart", "ev_demand_slowdown", "supply_rebound"),
        ("lithium_price", "mine_shutdown_restart", "ev_demand"),
        "Lithium is Cycle/Watch: price rebound without low-cost FCF and offtake stays capped.",
    ),
    Round57ScoreTarget(
        "PRECIOUS_METALS_SAFE_HAVEN_MINERS",
        E2RArchetype.PRECIOUS_METALS_SAFE_HAVEN_MINERS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round57ScoreWeightDraft(20, 10, 16, 9, 8, 5, 5),
        ("gold_silver_price", "safe_haven_demand", "real_rate_drop", "mine_output"),
        ("realized_price", "aisc_control", "fcf_improvement", "buyback_or_dividend"),
        ("cost_control", "capital_return", "production_stable", "fcf_conversion"),
        ("record_gold_price_crowded", "miner_group_overheat"),
        ("gold_price_correction", "aisc_rise", "production_drop", "jurisdiction_risk"),
        ("realized_price", "aisc_control", "capital_return", "fcf_conversion"),
        ("gold_price_correction", "aisc_rise", "mine_risk"),
        ("realized_price", "aisc", "capital_return"),
        "Gold miners can work, but safe-haven price alone is a cycle signal until AISC and returns confirm FCF.",
    ),
    Round57ScoreTarget(
        "ADVANCED_MATERIAL_SPECULATIVE_THEME",
        E2RArchetype.ADVANCED_MATERIAL_SPECULATIVE_THEME,
        Round10ThemePosture.REDTEAM_FIRST,
        Round57ScoreWeightDraft(5, 5, 5, 5, 5, 0, 3),
        ("superconductor_graphene_mxene_theme", "paper_or_lab_result", "quantum_material_keyword"),
        ("commercial_contract", "qualified_customer", "revenue_conversion"),
        ("commercial_revenue", "repeat_customer", "fcf_path"),
        ("speculative_material_theme_overheat", "paper_only_price_run"),
        ("no_commercialization", "paper_only", "no_revenue", "dilution"),
        ("commercial_contract", "revenue_conversion", "fcf_path"),
        ("paper_only", "no_revenue", "theme_only", "no_commercialization"),
        ("commercialization", "revenue_conversion", "dilution"),
        "Advanced materials are RedTeam-first before commercial revenue. A paper or lab result is not Green evidence.",
    ),
    Round57ScoreTarget(
        "PAPER_PACKAGING_CYCLE",
        E2RArchetype.PAPER_PACKAGING_CYCLE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round57ScoreWeightDraft(17, 12, 12, 10, 8, 3, 5),
        ("paper_price", "corrugated_spread", "packaging_mna", "plastic_replacement"),
        ("volume_recovery", "price_cost_spread", "mna_or_consolidation", "cash_return"),
        ("durable_spread", "scale_economics", "cash_return"),
        ("packaging_mna_premium_crowded",),
        ("low_volume", "price_pressure", "regulatory_divestiture", "mature_industry_limit"),
        ("volume_recovery", "price_cost_spread", "cash_return"),
        ("low_volume", "price_pressure", "competition_remedy", "mature_industry"),
        ("packaging_mna", "competition_remedy", "mature_industry"),
        "Packaging is mature and cyclical; M&A premium is not durable spread evidence by itself.",
    ),
    Round57ScoreTarget(
        "AGRI_COMMODITY_INPUTS",
        E2RArchetype.AGRI_COMMODITY_INPUTS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round57ScoreWeightDraft(18, 10, 14, 8, 8, 0, 5),
        ("grain_price", "feed_cost", "weather_event", "fertilizer_price", "disease_event"),
        ("price_pass_through", "inventory_status", "demand_visibility", "op_revision_1q"),
        ("repeat_margin", "cost_pass_through", "fcf_margin"),
        ("agri_event_crowded",),
        ("commodity_cost_reversal", "weather_normalization", "inventory_loss"),
        ("price_pass_through", "repeat_margin", "fcf_margin"),
        ("weather_event_only", "inventory_loss", "commodity_reversal"),
        ("weather", "inventory", "commodity_cost"),
        "Agri inputs are Event/Watch because weather and commodity costs reverse quickly.",
    ),
    Round57ScoreTarget(
        "LNG_ENERGY_TRADING_DISTRIBUTION",
        E2RArchetype.LNG_ENERGY_TRADING_DISTRIBUTION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round57ScoreWeightDraft(18, 16, 16, 10, 10, 2, 5),
        ("lng_long_term_contract", "energy_procurement", "lpg_distribution", "energy_security"),
        ("long_term_contract", "margin_visible", "fid_status", "inventory_status"),
        ("repeat_fcf", "project_stake", "energy_security_value", "margin_visible"),
        ("lng_contract_story_crowded",),
        ("price_reversal", "inventory_loss", "tariff_policy_shock", "financing_delay", "fid_delay"),
        ("long_term_contract", "margin_visible", "repeat_fcf", "project_stake"),
        ("price_reversal", "inventory_loss", "financing_delay", "fid_delay"),
        ("long_term_contract", "fid", "margin", "inventory"),
        "LNG can be Watch-to-Green when long contracts, FID, project economics, and FCF are explicit.",
    ),
    Round57ScoreTarget(
        "GENERAL_TRADING_RESOURCE_INFRA",
        E2RArchetype.GENERAL_TRADING_RESOURCE_INFRA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round57ScoreWeightDraft(17, 20, 12, 15, 18, 8, 5),
        ("resource_rights", "energy_contract", "buyback_dividend", "conglomerate_discount_rerating"),
        ("long_term_offtake", "project_stake", "fcf", "capital_return", "valuation_discount"),
        ("resource_infra_fcf_frame", "capital_allocation_execution", "valuation_discount_narrows"),
        ("sogo_shosha_story_crowded", "resource_infra_rerating_full"),
        ("commodity_price_drop", "project_delay", "capital_allocation_retreat", "fx_hit"),
        ("long_term_offtake", "project_stake", "fcf", "capital_return"),
        ("commodity_cycle", "project_delay", "capital_allocation_retreat"),
        ("resource_rights", "project_stake", "capital_return", "valuation_discount"),
        "Trading/resource houses rerate on resource-infra FCF and capital allocation, not sales scale alone.",
    ),
    Round57ScoreTarget(
        "ENERGY_UTILITY_LNG_GAS",
        E2RArchetype.ENERGY_UTILITY_LNG_GAS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round57ScoreWeightDraft(17, 18, 6, 12, 10, 5, 5),
        ("lng_gas_utility", "tariff_or_cost_pass_through", "uncollected_receivable_recovery"),
        ("tariff_visibility", "debt_stability", "cash_flow_recovery"),
        ("regulated_cost_pass_through", "debt_reduction", "capital_return_capacity"),
        ("gas_utility_turnaround_crowded",),
        ("tariff_freeze", "debt_burden", "receivable_growth", "policy_risk"),
        ("tariff_visibility", "cash_flow_recovery", "debt_reduction"),
        ("tariff_freeze", "debt_burden", "policy_risk"),
        ("tariff", "receivable", "debt", "policy"),
        "LNG/gas utilities are regulated Watch; tariff, receivables, and debt matter more than gas price.",
    ),
)


ROUND57_CASE_CANDIDATES: tuple[Round57CaseCandidate, ...] = (
    Round57CaseCandidate(
        "mp_materials_dod_apple_price_floor_case",
        "RARE_METALS_STRATEGIC_MATERIALS",
        "MP",
        "MP Materials 국방부·Apple price floor",
        "US",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("government_investment", "price_floor", "offtake_contract", "long_term_purchase", "supply_chain_security", "production_capacity"),
        ("project_execution_risk", "policy_dependency", "rare_earth_price_drop", "capacity_ramp_up_risk"),
        "price_floor_offtake_green_candidate",
        "needs_source_date_and_price_backfill",
        ("round_57.md AP MP Materials Pentagon Apple agreements",),
        "Month-level source marker exists, but exact stage date and price must be backfilled before price alignment.",
    ),
    Round57CaseCandidate(
        "china_heavy_rare_earth_export_control_case",
        "RARE_METALS_STRATEGIC_MATERIALS",
        "RARE_EARTH_CONTROL_REF",
        "중국 heavy rare earth 수출통제",
        "GLOBAL",
        "event_premium",
        None,
        date(2026, 5, 13),
        None,
        None,
        None,
        ("rare_earth_export_control", "heavy_rare_earth_shortage", "geopolitical_bottleneck", "strategic_supply_chain"),
        ("price_only_rally", "no_production_capacity", "no_offtake", "policy_reversal"),
        "geopolitical_bottleneck_reference",
        "missing_direct_symbol_mapping",
        ("round_57.md Reuters rare-earth export controls",),
        "Export control is macro Stage 1/2 evidence, not company-level Green without production, offtake, and FCF.",
    ),
    Round57CaseCandidate(
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
        ("twenty_year_lng_supply", "project_stake", "steel_supply", "long_term_offtake", "energy_security"),
        ("fid_pending", "financing_risk", "lng_price_risk", "project_delay"),
        "watch_to_green_candidate",
        "needs_price_backfill",
        ("round_57.md Reuters POSCO Alaska LNG deal",),
        "A 20-year LNG contract plus project stake and steel supply is stronger than spot LNG exposure.",
        (E2RArchetype.LNG_ENERGY_TRADING_DISTRIBUTION,),
    ),
    Round57CaseCandidate(
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
        "structural_resource_success",
        "needs_price_backfill",
        ("round_57.md Berkshire Japanese trading houses",),
        "Resource/infra FCF plus capital allocation can change the market frame for trading houses.",
    ),
    Round57CaseCandidate(
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
        "commodity_cyclical_success",
        "needs_price_backfill",
        ("round_57.md Reuters Barrick Q1 profit and buyback",),
        "Gold price plus AISC control and buyback can be profitable, but it remains a commodity cycle until durability is proven.",
    ),
    Round57CaseCandidate(
        "sk_innovation_refining_recovery_case",
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
        ("refining_op_improvement", "earnings_beat", "refining_recovery", "inventory_noise_excluded_check_needed"),
        ("recovery_delay_warning", "refining_margin_reversal", "inventory_loss"),
        "commodity_cyclical_success",
        "needs_price_backfill",
        ("round_57.md Reuters SK Innovation Q1 profit",),
        "Strong refining recovery remains Watch because margin, inventory, and recovery duration still need validation.",
    ),
    Round57CaseCandidate(
        "copper_ai_grid_demand_case",
        "NONFERROUS_STRATEGIC_METALS",
        "COPPER_GRID_REF",
        "구리 AI 데이터센터·전력망 수요",
        "GLOBAL",
        "success_candidate",
        None,
        date(2025, 12, 12),
        None,
        None,
        None,
        ("copper_price", "ai_grid_demand", "supply_constraint", "smelting_margin_check_needed"),
        ("metal_price_drop", "china_demand_slowdown", "no_company_fcf_mapping"),
        "structural_resource_success_candidate",
        "missing_direct_symbol_mapping",
        ("round_57.md copper AI grid demand",),
        "Copper demand can route research, but company-level Green still needs cost curve, margin, and FCF evidence.",
    ),
    Round57CaseCandidate(
        "korea_zinc_tender_offer_event_case",
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
        ("event_premium", "governance_dispute", "fcf_not_verified", "hostile_takeover"),
        "event_premium_misclassified",
        "needs_price_backfill",
        ("round_57.md Korea Zinc tender offer",),
        "Tender-offer price reaction must be separated from zinc smelting and durable FCF rerating.",
        (E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE,),
    ),
    Round57CaseCandidate(
        "ds_smith_international_paper_packaging_case",
        "PAPER_PACKAGING_CYCLE",
        "DS_SMITH_REF",
        "DS Smith / International Paper packaging M&A",
        "EU",
        "event_premium",
        None,
        date(2025, 4, 14),
        None,
        None,
        None,
        ("packaging_mna", "scale_economics_candidate", "competition_remedy", "plant_divestment"),
        ("mature_industry", "regulatory_divestiture", "price_pressure", "low_volume"),
        "event_premium_misclassified",
        "missing_public_price_data",
        ("round_57.md DS Smith International Paper packaging",),
        "Packaging M&A premium is not a structural spread rerating unless durable margin and cash return follow.",
    ),
    Round57CaseCandidate(
        "lg_chem_lotte_chemical_oversupply_case",
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
        ("china_middle_east_capacity_glut", "operating_loss", "op_profit_collapse", "spread_reversal", "supply_glut"),
        "spread_recovery_false_green",
        "needs_price_backfill",
        ("round_57.md Reuters Korean petrochemical oversupply",),
        "Chemical Green is blocked when China/Middle East capacity and spread reversal crush OP/FCF.",
    ),
    Round57CaseCandidate(
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
        ("lithium_price_crash", "mine_restart", "supply_rebound", "ev_demand_slowdown", "capex_cut"),
        "commodity_price_4c",
        "missing_price_data",
        ("round_57.md Reuters lithium prices stabilize after crash",),
        "Lithium price rebound is not structural when mine restarts and EV demand slowdown can cap the cycle.",
    ),
    Round57CaseCandidate(
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
        "commodity_price_4c",
        "needs_price_backfill",
        ("round_57.md Reuters BHP profit and dividend cut",),
        "Commodity downturn can reduce both FCF and capital return, breaking a structural thesis.",
    ),
    Round57CaseCandidate(
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
        ("paper_only", "no_revenue", "no_commercialization", "theme_only", "dilution"),
        "price_moved_without_evidence",
        "missing_price_data",
        ("round_57.md speculative advanced materials note",),
        "Scientific-material narratives are RedTeam-first until commercial revenue and customer validation exist.",
    ),
)


ROUND57_PRICE_FIELDS: tuple[str, ...] = (
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
    "peak_date",
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
    "below_stage2_price_flag",
    "below_stage3_price_flag",
    "commodity_type",
    "commodity_price_at_stage",
    "commodity_price_peak",
    "commodity_price_change_30D",
    "commodity_price_change_90D",
    "commodity_price_change_1Y",
    "product_spread_metric",
    "spread_change_30D",
    "spread_change_90D",
    "inventory_gain_loss",
    "refining_margin",
    "chemical_spread",
    "steel_spread",
    "smelting_margin",
    "revenue_revision_1q",
    "op_revision_1q",
    "eps_revision_1q",
    "eps_revision_1y",
    "fcf_margin",
    "dividend_change",
    "buyback_amount",
    "offtake_contract_flag",
    "offtake_contract_value",
    "offtake_duration_years",
    "price_floor_flag",
    "price_floor_level",
    "government_support_flag",
    "government_investment_amount",
    "strategic_supply_chain_flag",
    "production_capacity",
    "capacity_ramp_up_date",
    "project_execution_risk_flag",
    "customer_contract_flag",
    "tender_offer_flag",
    "governance_event_flag",
    "event_premium_flag",
    "hostile_takeover_flag",
    "capital_structure_risk_flag",
    "oversupply_flag",
    "supply_glut_flag",
    "mine_shutdown_flag",
    "mine_restart_flag",
    "capex_cut_flag",
    "dividend_cut_flag",
    "packaging_mna_flag",
    "competition_remedy_flag",
    "plant_divestment_flag",
    "mature_industry_flag",
    "score_price_alignment",
    "price_validation_status",
    "review_notes",
)


def target_for(target_id: str) -> Round57ScoreTarget | None:
    for target in ROUND57_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round57_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND57_CASE_CANDIDATES:
        target = target_for(candidate.target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {candidate.target_id}")
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
                f"Round57 R4 Loop-2 case for {candidate.target_id}; "
                "commodity cycle and structural supply-chain rerating remain separated."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage2_signals or field in target.green_conditions),
            stage3_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage3_conditions),
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
            score_price_alignment=_score_price_alignment(candidate),
            rerating_result=_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
            score_weight_hint=_score_weight_hint(target),
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "require_price_path_validation",
                "commodity_price_is_not_structural_evidence",
                "require_price_floor_offtake_or_fcf_for_rare_metals_green",
                "event_premium_is_not_fcf_rerating",
                "spread_recovery_needs_inventory_exclusion",
                "do_not_invent_spread_offtake_price_floor_or_stage_prices",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=False,
                price_data_available=False,
                stage_dates_confidence=0.75 if candidate.stage2_date or candidate.stage4c_date else 0.2,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round57_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND57_SCORE_TARGETS:
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
                "loop2_penalty_axes": "|".join(target.loop2_penalty_axes),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round57_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND57_CASE_CANDIDATES:
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


def round57_stage_date_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "target_id": target.target_id,
            "stage1": "|".join(target.stage1_signals),
            "stage2": "|".join(target.stage2_signals),
            "stage3": "|".join(target.stage3_conditions),
            "stage4b": "|".join(target.stage4b_conditions),
            "stage4c": "|".join(target.stage4c_conditions),
            "red_flags": "|".join(target.red_flags),
            "loop2_penalty_axes": "|".join(target.loop2_penalty_axes),
            "production_scoring_changed": "false",
        }
        for target in ROUND57_SCORE_TARGETS
    )


def round57_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round57_backfill": "true"} for field in ROUND57_PRICE_FIELDS)


def round57_summary() -> dict[str, int | bool]:
    records = round57_case_records()
    return {
        "target_count": len(ROUND57_SCORE_TARGETS),
        "case_candidate_count": len(records),
        "structural_success_count": sum(1 for record in records if record.case_type == "structural_success"),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for record in records if record.case_type == "cyclical_success"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "overheat_count": sum(1 for record in records if record.case_type == "overheat"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND57_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND57_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND57_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round57_r4_loop2_reports(
    *,
    output_directory: str | Path = ROUND57_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND57_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND57_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round57_r4_loop2_materials_spread_strategic_summary.md",
        "case_matrix": output / "round57_r4_loop2_case_matrix.csv",
        "stage_date_plan": output / "round57_r4_loop2_stage_date_plan.csv",
        "green_guardrails": output / "round57_r4_loop2_green_guardrails.md",
        "risk_overlays": output / "round57_r4_loop2_risk_overlays.md",
        "price_validation_plan": output / "round57_r4_loop2_price_validation_plan.md",
        "price_fields": output / "round57_r4_loop2_price_fields.csv",
    }
    _write_case_jsonl(round57_case_records(), cases)
    _write_rows(round57_score_profile_rows(), score_profiles)
    _write_rows(round57_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round57_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round57_price_field_rows(), paths["price_fields"])
    paths["summary"].write_text(render_round57_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round57_green_guardrail_markdown(), encoding="utf-8")
    paths["risk_overlays"].write_text(render_round57_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round57_price_validation_plan_markdown(), encoding="utf-8")
    return paths


def render_round57_summary_markdown() -> str:
    summary = round57_summary()
    lines = [
        "# Round-57 R4 Loop-2 Materials / Spread / Strategic Resources Summary",
        "",
        f"- source_round: `{ROUND57_SOURCE_ROUND_PATH}`",
        "- large_sector: `MATERIALS_SPREAD_STRATEGIC`",
        "- loop: `R4 Loop 2 / v2.0`",
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
        "- R4 Loop 2 says commodity price and structural rerating are different things.",
        "- Example: rare metals need government support, price floor, offtake, production capacity, and FCF before Green can be considered.",
        "- Example: chemical spread recovery stays Watch/Red when China or Middle East oversupply can reverse OP/FCF.",
        "- Example: Korea Zinc-type tender offers are event premiums, not automatic FCF rerating.",
        "- Example: refining recovery must exclude inventory gains before it can be treated as durable margin evidence.",
    ]
    return "\n".join(lines) + "\n"


def render_round57_green_guardrail_markdown() -> str:
    lines = [
        "# Round-57 R4 Loop-2 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Loop-2 penalties |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND57_SCORE_TARGETS:
        lines.append(
            "| "
            f"`{target.target_id}` | {target.posture.value} | "
            f"{', '.join(target.green_conditions)} | {', '.join(target.loop2_penalty_axes)} |"
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not apply R4 Loop-2 v2.0 weights to production scoring yet.",
            "- Do not treat commodity price, spread recovery, tender offers, or policy headlines as Green evidence by themselves.",
            "- Do not invent contract value, spread, offtake, price floor, production capacity, FCF, or stage prices.",
            "- Treat oversupply, mine restart, dividend cut, event premium, and no commercialization as RedTeam fields.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round57_risk_overlay_markdown() -> str:
    lines = [
        "# Round-57 R4 Loop-2 Risk Overlays",
        "",
        "- `STRUCTURAL_RESOURCE_SUCCESS`: resource/infra FCF and capital allocation change the market frame.",
        "- `COMMODITY_CYCLICAL_SUCCESS`: commodity price or spread improved, but durability is not proven.",
        "- `EVENT_PREMIUM_MISCLASSIFIED`: tender offer, M&A, or governance event is being confused with EPS/FCF rerating.",
        "- `SPREAD_RECOVERY_FALSE_GREEN`: refining, chemical, steel, or packaging spread recovery is scored before inventory and oversupply are checked.",
        "- `PRICE_FLOOR_OFFTAKE_GREEN_CANDIDATE`: price floor, offtake, government support, production, and FCF are visible.",
        "- `COMMODITY_PRICE_4C`: commodity price collapse, mine restart, dividend cut, or oversupply breaks the thesis.",
        "",
        "Simple example: `희토류 가격 급등` is useful routing evidence. It is not Green if the company has no production, offtake, price floor, or FCF path.",
    ]
    return "\n".join(lines) + "\n"


def render_round57_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-57 R4 Loop-2 Price Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign stage dates from source evidence only.",
        "2. Store stage-date close prices from official price data.",
        "3. Calculate MFE_30D / 90D / 180D / 1Y / 2Y.",
        "4. Calculate MAE_30D / 90D / 180D / 1Y.",
        "5. Compare commodity price, product spread, inventory gain/loss, offtake, price floor, government support, FCF, and price path.",
        "6. Mark event premium, oversupply, supply glut, mine restart, dividend cut, and no commercialization explicitly.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | target | stage marker | check |",
        "| --- | --- | --- | --- |",
    ]
    for row in round57_case_candidate_rows():
        stage_date = row["stage4c_date"] or row["stage4b_date"] or row["stage3_date"] or row["stage2_date"] or row["stage1_date"] or "undated"
        lines.append(f"| `{row['case_id']}` | `{row['target_id']}` | {stage_date} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `STRUCTURAL_RESOURCE_SUCCESS`: evidence and price path support durable resource/infra rerating.",
            "- `COMMODITY_CYCLICAL_SUCCESS`: spread or commodity price worked, but structural durability remains unproven.",
            "- `EVENT_PREMIUM_MISCLASSIFIED`: event-day price reaction should not be scored as FCF rerating.",
            "- `SPREAD_RECOVERY_FALSE_GREEN`: spread rebound was a false Green risk because oversupply or inventory reversed it.",
            "- `PRICE_FLOOR_OFFTAKE_GREEN_CANDIDATE`: price floor, offtake, government support, and production make rare metals higher quality.",
            "- `COMMODITY_PRICE_4C`: commodity price collapse or supply restart breaks the thesis.",
        ]
    )
    return "\n".join(lines) + "\n"


def _score_price_alignment(candidate: Round57CaseCandidate) -> str:
    if "event_premium" in candidate.alignment_hint or candidate.case_type == "event_premium":
        return "price_moved_without_evidence"
    if candidate.case_type in {"4b_watch", "overheat"}:
        return "price_moved_without_evidence"
    if candidate.case_type == "4c_thesis_break":
        return "false_positive_score"
    if candidate.case_type in {"structural_success", "success_candidate", "cyclical_success"}:
        return "aligned"
    return "unknown"


def _rerating_result(candidate: Round57CaseCandidate) -> str:
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
    return "unknown" if candidate.case_type == "success_candidate" else "no_rerating"


def _score_weight_hint(target: Round57ScoreTarget) -> dict[str, float]:
    weights = target.score_weight.as_dict()
    return {
        "eps_fcf": float(weights["eps_fcf"]),
        "visibility": float(weights["structural_visibility"]),
        "bottleneck": float(weights["bottleneck_pricing"]),
        "mispricing": float(weights["market_mispricing"]),
        "valuation": float(weights["valuation"]),
        "capital_allocation": float(weights["capital_allocation"]),
    }


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
        writer = csv.DictWriter(handle, fieldnames=tuple(rows_tuple[0].keys()))
        writer.writeheader()
        for row in rows_tuple:
            writer.writerow(dict(row))
    return path


__all__ = [
    "ROUND57_CASE_CANDIDATES",
    "ROUND57_DEFAULT_CASES_PATH",
    "ROUND57_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND57_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND57_PRICE_FIELDS",
    "ROUND57_SCORE_TARGETS",
    "Round57CaseCandidate",
    "Round57ScoreTarget",
    "Round57ScoreWeightDraft",
    "render_round57_green_guardrail_markdown",
    "render_round57_price_validation_plan_markdown",
    "render_round57_risk_overlay_markdown",
    "render_round57_summary_markdown",
    "round57_case_candidate_rows",
    "round57_case_records",
    "round57_price_field_rows",
    "round57_score_profile_rows",
    "round57_stage_date_rows",
    "round57_summary",
    "target_for",
    "write_round57_r4_loop2_reports",
]
