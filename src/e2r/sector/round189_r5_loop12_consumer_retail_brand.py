"""Round-189 R5 Loop-12 Korea consumer/retail/brand pack.

Round 189 tightens R5 around Korea K-food localization, global staple
brands, K-beauty second-wave brands, e-commerce restructuring JV, department
store redevelopment, and convenience-store PB/SSSG evidence. It is
calibration/report material only. Production feature engineering, scoring,
staging, and RedTeam code must not import this module.
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


ROUND189_SOURCE_ROUND_PATH = "docs/round/round_189.md"
ROUND189_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round189_r5_loop12_consumer_retail_brand"
ROUND189_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r5_loop12_round189.jsonl"
ROUND189_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round189_r5_loop12_v12.csv"
ROUND189_SOURCE_CANONICAL_TARGET_IDS: tuple[str, ...] = (
    "K_FOOD_GLOBAL_LOCALIZATION",
    "K_FOOD_GLOBAL_STAPLE_BRAND_SECOND_WAVE",
    "K_FOOD_SINGLE_SKU_EXPORT_RISK",
    "ECOMMERCE_RESTRUCTURING_JV_KOREA",
    "RETAIL_PLATFORM_DATA_REGULATION_OVERLAY",
    "DEPARTMENT_STORE_MALL_REDEVELOPMENT",
    "CONVENIENCE_STORE_PB_SSSG_KOREA",
    "K_BEAUTY_BRAND_SECOND_WAVE",
    "K_BEAUTY_TARIFF_IMPORT_REVIEW",
    "CHANNEL_STUFFING_INVENTORY_OVERLAY",
    "DISCLOSURE_CONFIDENCE_CAP",
)
ROUND189_SOURCE_CANONICAL_TARGET_COUNT = len(ROUND189_SOURCE_CANONICAL_TARGET_IDS)


@dataclass(frozen=True)
class Round189ScoreWeightDraft:
    eps_fcf_opm_conversion: int | str
    overseas_channel_localization_platform_visibility: int | str
    sellthrough_reorder_recurring_consumption: int | str
    inventory_receivables_margin_quality: int | str
    early_price_validation: int | str
    tariff_regulation_capex_disclosure_redteam: int | str
    valuation_4b_room: int | str

    def as_dict(self) -> dict[str, int | str]:
        return {
            "eps_fcf_opm_conversion": self.eps_fcf_opm_conversion,
            "overseas_channel_localization_platform_visibility": self.overseas_channel_localization_platform_visibility,
            "sellthrough_reorder_recurring_consumption": self.sellthrough_reorder_recurring_consumption,
            "inventory_receivables_margin_quality": self.inventory_receivables_margin_quality,
            "early_price_validation": self.early_price_validation,
            "tariff_regulation_capex_disclosure_redteam": self.tariff_regulation_capex_disclosure_redteam,
            "valuation_4b_room": self.valuation_4b_room,
        }


@dataclass(frozen=True)
class Round189ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round189ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    loop12_penalty_axes: tuple[str, ...]
    normalization_point: str
    hard_gate: bool = False

    @property
    def large_sector(self) -> Round10LargeSector:
        return Round10LargeSector.CONSUMER_RETAIL_BRAND

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round189CaseCandidate:
    case_id: str
    target_id: str
    symbol: str
    company_name: str
    market: str
    case_type: str
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
class Round189BaseScoreWeight:
    component: str
    points: int
    loop12_direction: str
    reason: str

    def as_row(self) -> dict[str, str]:
        return {
            "component": self.component,
            "points": str(self.points),
            "loop12_direction": self.loop12_direction,
            "reason": self.reason,
            "production_scoring_changed": "false",
        }


@dataclass(frozen=True)
class Round189StageCap:
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
            "production_scoring_changed": "false",
        }


@dataclass(frozen=True)
class Round189ScoreStagePriceAlignment:
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
            "production_scoring_changed": "false",
        }


def _w(
    eps: int | str,
    visibility: int | str,
    sellthrough: int | str,
    quality: int | str,
    price: int | str,
    redteam: int | str,
    valuation: int | str,
) -> Round189ScoreWeightDraft:
    return Round189ScoreWeightDraft(eps, visibility, sellthrough, quality, price, redteam, valuation)


CAP_WEIGHT = _w("cap", "cap", "cap", "cap", "cap", "cap", "+")
GATE_WEIGHT = _w("gate", "gate", "gate", "gate", "gate", "gate", "gate")


ROUND189_BASE_SCORE_WEIGHTS: tuple[Round189BaseScoreWeight, ...] = (
    Round189BaseScoreWeight("eps_fcf_opm_conversion", 24, "keep_high", "R5 Loop 12 requires OP/EPS/FCF conversion, not K-food, K-beauty, JV, or convenience-store keywords."),
    Round189BaseScoreWeight("overseas_channel_localization_platform_visibility", 20, "raised_for_loop12", "Overseas sales, local plants, JV, offline entry, mainstream shelf, PB, and SSSG are Stage 2 visibility evidence."),
    Round189BaseScoreWeight("sellthrough_reorder_recurring_consumption", 18, "raised_for_loop12", "K-food and K-beauty need sell-through, reorder, and recurring consumption before Stage 3 conviction."),
    Round189BaseScoreWeight("inventory_receivables_margin_quality", 12, "hard_quality_gate", "Inventory days, receivables days, gross margin, ASP, OPM, and FCF separate real demand from channel stuffing."),
    Round189BaseScoreWeight("early_price_validation", 10, "required_backfill", "Stage 2 이후 60D/120D MFE, event return, and relative strength validate whether the market is confirming the evidence."),
    Round189BaseScoreWeight("tariff_regulation_capex_disclosure_redteam", 10, "hard_review", "Tariff, KFTC data restrictions, CAPEX/utilization drag, cost/logistics, and disclosure gaps can block Green."),
    Round189BaseScoreWeight("valuation_4b_room", 6, "cool_crowded_consumer_rallies", "K-food, K-beauty, JV, and convenience narratives need 4B cooling when price outruns earnings evidence."),
)


ROUND189_STAGE_CAPS: tuple[Round189StageCap, ...] = (
    Round189StageCap(
        "Stage 1",
        "45",
        ("kfood_kbeauty_viral", "amazon_tiktok_entry", "jv_or_platform_headline", "mall_redevelopment_plan", "convenience_defensive_story", "pb_food_keyword"),
        ("kbeauty_brand_second_wave_stage23_case", "emart_shinsegae_alibaba_jv_stage2_case"),
        "Brand, viral, entry, JV, and defensive-retail words route research only. Green is blocked before sell-through, reorder, OP/EPS, FCF, and quality evidence.",
    ),
    Round189StageCap(
        "Stage 2",
        "70",
        ("overseas_channel_added", "local_production_footprint", "jv_announced", "kftc_conditional_approval", "offline_entry", "pb_mix_or_sssg", "export_growth"),
        ("cj_cheiljedang_kfood_localization_stage23_case", "emart_shinsegae_alibaba_jv_stage2_case"),
        "Stage 2 can be strong when channel, factory, JV, export, or PB visibility exists, but Stage 3 waits for OP/EPS/FCF and quality conversion.",
    ),
    Round189StageCap(
        "Stage 3",
        "requires_5_of_8",
        ("export_or_overseas_sales_grows_by_quarter", "op_eps_revision_or_quarterly_op_beat", "sellthrough_or_reorder_evidence", "no_inventory_or_receivables_deterioration", "asp_or_gross_margin_defended", "60d_mfe_20pct_after_stage2", "no_tariff_regulation_capex_hard_issue", "valuation_not_already_overheated"),
        ("cj_cheiljedang_kfood_localization_stage23_case", "orion_global_staple_brand_second_wave_case", "kbeauty_brand_second_wave_stage23_case"),
        "Stage 3 early catch is possible only when growth, sell-through, margin quality, OP/EPS/FCF, and price path align.",
    ),
    Round189StageCap(
        "Stage 4B",
        "requires_4_of_6",
        ("stage2_120d_mfe_80pct", "kfood_kbeauty_jv_headline_doubles_price_before_earnings", "viral_or_channel_entry_priced_before_sellthrough", "inventory_or_receivables_begin_rising", "op_eps_revision_lags_price", "kfood_kbeauty_keywords_crowded"),
        ("kbeauty_online_viral_not_sellthrough_4b_case",),
        "Crowded consumer rallies are cooled when price moves faster than sell-through, reorder, margin, and OP/EPS revision.",
    ),
    Round189StageCap(
        "Stage 4C",
        "hard_gate",
        ("us_tariff_damages_price_competitiveness", "offline_sellthrough_failure", "channel_inventory_or_receivables_spike", "jv_regulation_delays_monetization", "local_plant_utilization_weak", "single_sku_slowdown", "raw_material_or_logistics_cost_damages_opm", "china_russia_regional_risk_cuts_sales", "opendart_or_media_detail_missing"),
        ("kbeauty_tariff_import_review_4c_watch_case", "emart_alibaba_data_regulation_4c_watch_case"),
        "A single hard tariff, sell-through, inventory, JV regulation, utilization, single-SKU, cost, regional, or disclosure-detail issue can block Green.",
    ),
)


def _target(
    target_id: str,
    archetype: E2RArchetype,
    posture: Round10ThemePosture,
    weight: Round189ScoreWeightDraft,
    stage1: tuple[str, ...],
    stage2: tuple[str, ...],
    stage3: tuple[str, ...],
    stage4b: tuple[str, ...],
    stage4c: tuple[str, ...],
    green: tuple[str, ...],
    red: tuple[str, ...],
    penalties: tuple[str, ...],
    note: str,
    *,
    hard_gate: bool = False,
) -> Round189ScoreTarget:
    return Round189ScoreTarget(
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


ROUND189_SCORE_TARGETS: tuple[Round189ScoreTarget, ...] = (
    _target(
        "K_FOOD_GLOBAL_LOCALIZATION",
        E2RArchetype.K_FOOD_GLOBAL_LOCALIZATION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(24, 22, 18, 10, 10, 10, 6),
        ("kfood_global_demand", "bibigo_or_global_brand", "localization_headline", "mainstream_shelf"),
        ("schwans_distribution", "local_production_footprint", "japan_hungary_us_plant", "overseas_channel"),
        ("overseas_sales_growth", "plant_utilization", "opm_fcf_improvement", "asp_defended", "reorder_signal"),
        ("localization_narrative_priced_before_utilization",),
        ("local_plant_utilization_weak", "capex_drag", "logistics_cost", "opm_not_improving"),
        ("plant_utilization", "opm_fcf_improvement", "overseas_sales_growth", "reorder_signal"),
        ("capex_drag", "utilization_unknown", "opm_missing", "fx_logistics_cost"),
        ("localization", "plant_utilization", "opm_fcf"),
        "K-food localization is Stage 2 evidence; Stage 3 needs utilization, ASP, OPM, FCF, and repeat demand.",
    ),
    _target(
        "K_FOOD_GLOBAL_STAPLE_BRAND_SECOND_WAVE",
        E2RArchetype.K_FOOD_GLOBAL_STAPLE_BRAND_SECOND_WAVE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(23, 20, 22, 12, 9, 8, 6),
        ("global_staple_brand", "choco_pie_or_snack_brand", "multi_region_presence"),
        ("local_production", "regional_sales_base", "repeat_snack_consumption", "multi_country_distribution"),
        ("regional_sales_growth", "regional_opm", "input_cost_pass_through", "op_eps_revision", "new_product_reorder"),
        ("global_staple_story_crowded",),
        ("china_consumption_slowdown", "russia_fx_geopolitics", "cocoa_sugar_wheat_cost", "brand_maturity_cap"),
        ("regional_opm", "input_cost_pass_through", "repeat_consumption", "op_eps_revision"),
        ("regional_growth_cap", "input_cost_risk", "fx_or_geopolitics"),
        ("repeat_snack_demand", "regional_opm", "maturity_cap"),
        "Global staple brands can be Stage 2~3 candidates, but regional OPM and cost pass-through are the gate.",
    ),
    _target(
        "K_FOOD_SINGLE_SKU_EXPORT_RISK",
        E2RArchetype.K_FOOD_SINGLE_SKU_EXPORT_RISK,
        Round10ThemePosture.REDTEAM_FIRST,
        CAP_WEIGHT,
        ("single_sku_export_story", "viral_product", "export_headline"),
        ("sku_export_growth", "channel_addition", "opm_check_required"),
        ("not_green_until_multi_sku_reorder_opm_and_inventory_are_verified",),
        ("single_sku_viral_priced_before_reorder",),
        ("single_sku_slowdown", "raw_material_cost", "inventory_build", "channel_concentration"),
        ("multi_sku_reorder", "opm_stable", "inventory_stable"),
        ("single_sku_dependency", "viral_fad", "inventory_unknown"),
        ("single_sku", "viral", "inventory_cap"),
        "Single-SKU export stories are capped until repeat multi-SKU demand, OPM, and inventory quality are verified.",
    ),
    _target(
        "ECOMMERCE_RESTRUCTURING_JV_KOREA",
        E2RArchetype.ECOMMERCE_RESTRUCTURING_JV_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(18, 24, 8, 10, 12, 18, 10),
        ("gmarket_turnaround", "aliexpress_korea", "cross_border_ecommerce", "platform_restructuring"),
        ("50_50_jv", "price_reaction", "kftc_conditional_approval", "market_share_option"),
        ("gmv_recovery", "take_rate_improvement", "ad_revenue_improvement", "logistics_marketing_cost_reduction", "fcf_improvement"),
        ("jv_headline_priced_before_synergy",),
        ("data_sharing_restriction", "coupang_naver_competition", "monetization_delay", "china_crossborder_regulation"),
        ("gmv_recovery", "take_rate_improvement", "profitability_improvement", "fcf_improvement"),
        ("data_restriction", "synergy_missing", "competition_intense"),
        ("jv", "gmv", "take_rate", "data_regulation"),
        "Korea e-commerce JV is Stage 2 until GMV, take-rate, cost, and FCF conversion are visible.",
    ),
    _target(
        "RETAIL_PLATFORM_DATA_REGULATION_OVERLAY",
        E2RArchetype.RETAIL_PLATFORM_DATA_REGULATION_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        ("platform_data_combination", "customer_database", "cross_border_market_share"),
        ("regulatory_approval_condition", "data_sharing_restriction"),
        ("not_green_until_data_rule_allows_monetization_and_platform_profitability_is_verified",),
        ("data_synergy_priced_before_regulation_clears",),
        ("kftc_data_sharing_restriction", "independent_operation_condition", "monetization_delay", "privacy_or_data_rule_tightens"),
        ("regulated_data_use_cleared", "monetization_visible", "profitability_improves"),
        ("kftc_data_sharing_restriction", "data_regulation", "monetization_delay", "privacy_condition"),
        ("data_regulation", "platform_monetization"),
        "Data-sharing restrictions are a RedTeam overlay for retail-platform monetization.",
        hard_gate=True,
    ),
    _target(
        "DEPARTMENT_STORE_MALL_REDEVELOPMENT",
        E2RArchetype.DEPARTMENT_STORE_MALL_REDEVELOPMENT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(18, 20, 8, 12, 9, 24, 9),
        ("mall_redevelopment", "retailtainment", "tourist_recovery", "offline_retail_recovery"),
        ("large_mall_investment_plan", "portfolio_transformation", "lease_income_option"),
        ("foot_traffic_growth", "sales_per_customer", "lease_income_growth", "capex_payback", "opm_fcf_improvement"),
        ("redevelopment_story_priced_before_payback",),
        ("capex_burden", "traffic_recovery_failure", "tourist_spend_weak", "online_competition"),
        ("capex_payback", "lease_income_growth", "opm_fcf_improvement", "traffic_growth"),
        ("capex_burden", "traffic_weak", "payback_unknown"),
        ("mall_redevelopment", "capex_payback", "traffic"),
        "Mall redevelopment is Stage 1~2 before traffic, lease income, CAPEX payback, and FCF are proven.",
    ),
    _target(
        "CONVENIENCE_STORE_PB_SSSG_KOREA",
        E2RArchetype.CONVENIENCE_STORE_PB_SSSG_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(22, 20, 16, 16, 8, 12, 6),
        ("convenience_defensive_story", "pb_food", "ready_to_eat_meals", "single_household_demand"),
        ("store_network", "pb_mix", "sssg", "quick_commerce_or_delivery"),
        ("sssg_growth", "pb_mix_rises", "franchisee_margin_stable", "wage_rent_electricity_controlled", "opm_fcf_improvement"),
        ("defensive_rerating_before_cost_check",),
        ("wage_rent_electricity_cost_pressure", "franchisee_margin_pressure", "store_saturation", "online_grocery_competition"),
        ("sssg_growth", "pb_mix_rises", "franchisee_margin_stable", "opm_fcf_improvement"),
        ("cost_pressure", "franchisee_margin_pressure", "sssg_missing"),
        ("sssg", "pb_mix", "franchisee_margin"),
        "Convenience-store Stage 3 needs SSSG, PB mix, franchise margin, OPM, and FCF, not defensive-stock language.",
    ),
    _target(
        "K_BEAUTY_BRAND_SECOND_WAVE",
        E2RArchetype.K_BEAUTY_BRAND_SECOND_WAVE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(23, 20, 20, 14, 9, 9, 5),
        ("kbeauty_viral", "amazon_tiktok_growth", "brand_second_wave", "us_import_growth"),
        ("us_japan_channel_growth", "brand_portfolio", "offline_entry", "online_sales_growth"),
        ("offline_sell_through", "reorder_signal", "overseas_asp_defended", "inventory_receivables_stable", "opm_fcf_improvement"),
        ("kbeauty_second_wave_basket_rally", "viral_priced_before_sellthrough"),
        ("tariff_exposure", "growth_plateau", "inventory_or_receivables_spike", "low_price_competition"),
        ("offline_sell_through", "reorder_signal", "inventory_receivables_stable", "opm_fcf_improvement"),
        ("sellthrough_missing", "inventory_unknown", "tariff_risk"),
        ("sellthrough", "reorder", "inventory_quality"),
        "K-beauty second wave can become Stage 2~3 only when brand sell-through and reorder evidence is explicit.",
    ),
    _target(
        "K_BEAUTY_TARIFF_IMPORT_REVIEW",
        E2RArchetype.K_BEAUTY_TARIFF_IMPORT_REVIEW,
        Round10ThemePosture.REDTEAM_FIRST,
        CAP_WEIGHT,
        ("us_import_growth", "kbeauty_boom", "tariff_headline"),
        ("tariff_rate_review", "gross_margin_buffer_check", "stockpiling_or_purchase_delay"),
        ("not_green_until_price_hike_tolerance_and_margin_buffer_are_verified",),
        ("import_growth_priced_before_tariff_margin_check",),
        ("us_tariff_25pct_risk", "stockpiling", "purchase_delay", "margin_buffer_missing", "inventory_shock"),
        ("price_hike_tolerance", "gross_margin_buffer", "inventory_stable"),
        ("tariff_exposure", "margin_buffer_missing", "stockpiling"),
        ("tariff", "margin_buffer", "inventory"),
        "K-beauty tariff review caps import-growth narratives until price and margin buffers are proven.",
    ),
    _target(
        "CHANNEL_STUFFING_INVENTORY_OVERLAY",
        E2RArchetype.CHANNEL_STUFFING_INVENTORY_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        ("online_viral", "channel_entry", "export_growth_headline"),
        ("inventory_receivables_check_required", "sellthrough_required", "reorder_required"),
        ("not_green_until_inventory_receivables_and_sellthrough_are_stable",),
        ("viral_or_entry_priced_before_physical_sellthrough",),
        ("channel_inventory_or_receivables_spike", "offline_sellthrough_failure", "growth_plateau", "discounting"),
        ("inventory_receivables_stable", "physical_sellthrough", "reorder_signal"),
        ("inventory_spike", "receivables_spike", "sellthrough_failure"),
        ("channel_stuffing", "inventory_quality"),
        "Channel inventory and receivables spikes are hard quality gates for K-food, K-beauty, and retail.",
        hard_gate=True,
    ),
    _target(
        "DISCLOSURE_CONFIDENCE_CAP",
        E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        Round10ThemePosture.REDTEAM_FIRST,
        CAP_WEIGHT,
        ("opendart_list_only", "media_report", "brand_headline", "entry_headline", "jv_headline"),
        ("detail_fetch_required", "sales_channel_inventory_opm_required", "parser_confidence_required"),
        ("not_green_until_revenue_channel_inventory_opm_and_fcf_detail_are_verified",),
        ("headline_priced_before_detail",),
        ("detail_missing", "media_report_only", "channel_missing", "inventory_missing", "opm_unknown", "fcf_unknown"),
        ("sales_detail", "channel_detail", "inventory_receivables_detail", "opm_fcf_visible"),
        ("list_only", "media_only", "detail_missing", "opm_fcf_missing"),
        ("detail_missing", "opm_unknown", "fcf_unknown"),
        "Round 189 caps list-only, media-only, channel-only, JV-only, and missing inventory/OPM/FCF evidence before Green.",
    ),
)


ROUND189_CASE_CANDIDATES: tuple[Round189CaseCandidate, ...] = (
    Round189CaseCandidate(
        "cj_cheiljedang_kfood_localization_stage23_case",
        "K_FOOD_GLOBAL_LOCALIZATION",
        "097950",
        "CJ제일제당 / CJ푸드빌 K-food localization",
        "KR",
        "success_candidate",
        ("bibigo_global_demand", "schwans_distribution", "japan_hungary_us_plant", "local_production_footprint", "mainstream_shelf_option"),
        ("plant_utilization_unknown", "capex_drag", "opm_fcf_missing", "fx_logistics_cost"),
        "stage2_to_stage3_if_utilization_asp_opm_fcf_and_price_path_align",
        "needs_overseas_sales_utilization_opm_fcf_price_backfill",
        ("round_189.md CJ Group / Schwan's / local plants",),
        "CJ has Stage 2 localization evidence; Stage 3 waits for utilization, ASP, OPM, FCF, and repeat channel evidence.",
        (E2RArchetype.EXPORT_RECURRING_CONSUMER,),
    ),
    Round189CaseCandidate(
        "orion_global_staple_brand_second_wave_case",
        "K_FOOD_GLOBAL_STAPLE_BRAND_SECOND_WAVE",
        "271560",
        "오리온 global staple brand second wave",
        "KR",
        "success_candidate",
        ("choco_pie_global_brand", "russia_vietnam_china_india_footprint", "local_production", "repeat_snack_consumption"),
        ("regional_maturity", "china_russia_risk", "input_cost_risk", "regional_opm_missing"),
        "stage2_to_stage3_if_regional_growth_opm_cost_pass_through_and_revision_align",
        "needs_regional_sales_opm_input_cost_price_backfill",
        ("round_189.md Orion / Choco Pie global staple brand",),
        "Orion is a quiet R5 Stage 2~3 candidate, but regional growth, OPM, input costs, and price path must be backfilled.",
        (E2RArchetype.EXPORT_RECURRING_CONSUMER,),
    ),
    Round189CaseCandidate(
        "bingle_lottewellfood_single_sku_export_watch_case",
        "K_FOOD_SINGLE_SKU_EXPORT_RISK",
        "005180/280360",
        "빙그레·롯데웰푸드 single-SKU export watch",
        "KR",
        "success_candidate",
        ("single_sku_export_story", "kfood_sku_growth", "channel_addition"),
        ("single_sku_dependency", "viral_fad", "inventory_unknown", "raw_material_cost"),
        "stage1_2_watch_until_multi_sku_reorder_opm_and_inventory_clear",
        "needs_sku_sales_inventory_opm_price_backfill",
        ("round_189.md single SKU K-food risk",),
        "Single SKU export can route Layer 1/Stage 2 watch, but Green waits for multi-SKU reorder, OPM, and inventory quality.",
        (E2RArchetype.STAGE2_EVIDENCE_NOT_GREEN,),
    ),
    Round189CaseCandidate(
        "emart_shinsegae_alibaba_jv_stage2_case",
        "ECOMMERCE_RESTRUCTURING_JV_KOREA",
        "139480/004170",
        "이마트·신세계 Alibaba JV Stage 2",
        "KR",
        "success_candidate",
        ("gmarket_aliexpress_50_50_jv", "emart_plus_5_5pct_event_return", "cross_border_market_share_option", "kftc_conditional_approval"),
        ("data_sharing_restriction", "coupang_naver_competition", "gmv_recovery_missing", "take_rate_missing"),
        "stage2_price_aligned_not_green_before_gmv_take_rate_profitability",
        "needs_gmv_take_rate_cost_fcf_regulation_price_backfill",
        ("round_189.md Reuters Shinsegae Alibaba JV", "round_189.md WSJ E-Mart +5.5%", "round_189.md Reuters KFTC conditional approval"),
        "E-Mart/Shinsegae JV has Stage 2 catalyst and price reaction, but data restriction and monetization proof gate Stage 3.",
        (E2RArchetype.RETAIL_PLATFORM_DATA_REGULATION_OVERLAY, E2RArchetype.STAGE2_EVIDENCE_NOT_GREEN),
    ),
    Round189CaseCandidate(
        "kbeauty_brand_second_wave_stage23_case",
        "K_BEAUTY_BRAND_SECOND_WAVE",
        "237880/214420/018290/114840",
        "클리오·토니모리·VT·아이패밀리에스씨 K-beauty brand second wave",
        "KR",
        "success_candidate",
        ("us_kbeauty_import_growth", "online_sales_growth", "brand_portfolio", "amazon_tiktok_signal", "offline_entry_option"),
        ("offline_sellthrough_missing", "inventory_receivables_missing", "tariff_risk", "growth_plateau"),
        "stage2_to_stage3_if_offline_sellthrough_reorder_inventory_and_opm_align",
        "needs_sellthrough_reorder_inventory_receivables_opm_price_backfill",
        ("round_189.md Reuters K-beauty US import / online growth", "round_189.md Clio TonyMoly brand references"),
        "K-beauty brand second wave is a Stage 2~3 candidate basket only with sell-through, reorder, inventory, and OPM evidence.",
        (E2RArchetype.K_BEAUTY_TARIFF_IMPORT_REVIEW, E2RArchetype.CHANNEL_STUFFING_INVENTORY_OVERLAY),
    ),
    Round189CaseCandidate(
        "convenience_store_pb_sssg_stage23_case",
        "CONVENIENCE_STORE_PB_SSSG_KOREA",
        "282330/007070",
        "BGF리테일·GS리테일 PB / SSSG basket",
        "KR",
        "success_candidate",
        ("store_network", "pb_food", "ready_to_eat_meals", "sssg", "quick_commerce_option"),
        ("wage_rent_electricity_cost", "franchisee_margin_pressure", "store_saturation", "sssg_opm_missing"),
        "stage2_to_stage3_if_sssg_pb_mix_franchise_margin_opm_and_fcf_align",
        "needs_sssg_pb_mix_franchise_margin_opm_price_backfill",
        ("round_189.md GS25 store network / convenience store gates",),
        "Convenience-store Stage 3 needs SSSG, PB mix, franchise margin, OPM, FCF, and price-path validation.",
    ),
    Round189CaseCandidate(
        "lotte_shopping_mall_redevelopment_stage12_case",
        "DEPARTMENT_STORE_MALL_REDEVELOPMENT",
        "023530",
        "롯데쇼핑 mall redevelopment Stage 1~2",
        "KR",
        "success_candidate",
        ("7tn_krw_mall_investment_plan", "mall_redevelopment", "retailtainment", "lease_income_option"),
        ("capex_burden", "capex_payback_unknown", "traffic_recovery_missing", "online_competition"),
        "stage1_2_option_not_green_before_capex_payback_traffic_and_fcf",
        "needs_capex_payback_traffic_lease_income_fcf_price_backfill",
        ("round_189.md Lotte Department Store mall investment",),
        "Mall redevelopment is a Stage 1~2 option, but CAPEX payback, traffic, lease income, OPM, and FCF gate Stage 3.",
        (E2RArchetype.STAGE2_EVIDENCE_NOT_GREEN,),
    ),
    Round189CaseCandidate(
        "kbeauty_tariff_import_review_4c_watch_case",
        "K_BEAUTY_TARIFF_IMPORT_REVIEW",
        "K_BEAUTY_TARIFF_BASKET",
        "K-beauty U.S. tariff import review",
        "KR",
        "4c_thesis_break",
        ("us_kbeauty_import_1_7bn_usd", "import_growth_54pct", "tariff_25pct_review", "stockpiling_purchase_delay"),
        ("us_tariff_25pct_risk", "margin_buffer_missing", "purchase_delay", "inventory_shock"),
        "tariff_margin_buffer_hard_review_blocks_import_growth_green",
        "needs_tariff_margin_buffer_price_hike_inventory_price_backfill",
        ("round_189.md AP K-beauty tariff threat",),
        "U.S. import growth is Stage 2 context, but tariff and margin-buffer uncertainty create 4C-watch until price pass-through is proven.",
        (E2RArchetype.TARIFF_IMPORT_REGULATION_OVERLAY,),
    ),
    Round189CaseCandidate(
        "kbeauty_online_viral_not_sellthrough_4b_case",
        "CHANNEL_STUFFING_INVENTORY_OVERLAY",
        "K_BEAUTY_BRAND_BASKET",
        "K-beauty online viral without physical sell-through",
        "KR",
        "4b_watch",
        ("amazon_tiktok_viral", "online_sales_growth", "brand_entry_narrative"),
        ("physical_sellthrough_missing", "growth_plateau", "inventory_receivables_spike", "low_price_competition"),
        "viral_entry_rally_requires_4b_watch_until_physical_sellthrough_and_reorder",
        "needs_physical_sellthrough_reorder_inventory_price_backfill",
        ("round_189.md Reuters physical store sell-through warning",),
        "Online viral growth can become 4B-watch when physical sell-through and reorder are not verified.",
        (E2RArchetype.K_BEAUTY_BRAND_SECOND_WAVE, E2RArchetype.CROWDED_RERATING_4B_WATCH),
    ),
    Round189CaseCandidate(
        "emart_alibaba_data_regulation_4c_watch_case",
        "RETAIL_PLATFORM_DATA_REGULATION_OVERLAY",
        "139480/004170",
        "E-Mart / Shinsegae Alibaba JV data-regulation cap",
        "KR",
        "4c_thesis_break",
        ("kftc_conditional_approval", "50m_customer_database", "data_sharing_restriction_3y", "independent_operation_condition"),
        ("data_sharing_restriction", "monetization_delay", "privacy_condition", "competition_intense"),
        "data_regulation_hard_gate_before_platform_monetization",
        "needs_data_rule_monetization_gmv_take_rate_price_backfill",
        ("round_189.md Reuters KFTC data-sharing restriction",),
        "The JV can be Stage 2, but data-sharing restrictions can cap monetization and block Stage 3.",
    ),
    Round189CaseCandidate(
        "cj_kfood_localization_capex_drag_case",
        "K_FOOD_GLOBAL_LOCALIZATION",
        "097950",
        "CJ K-food localization CAPEX drag",
        "KR",
        "failed_rerating",
        ("local_production_footprint", "new_plant_capex", "global_channel_option"),
        ("plant_utilization_weak", "capex_drag", "opm_not_improving", "fcf_negative"),
        "localization_asset_without_utilization_is_capex_drag_not_green",
        "needs_utilization_opm_fcf_price_backfill",
        ("round_189.md CJ localization capex drag rule",),
        "Local plants are assets and costs; without utilization, OPM, and FCF, localization stays capped.",
        (E2RArchetype.STAGE2_EVIDENCE_NOT_GREEN,),
    ),
    Round189CaseCandidate(
        "orion_global_staple_brand_maturity_cap_case",
        "K_FOOD_GLOBAL_STAPLE_BRAND_SECOND_WAVE",
        "271560",
        "Orion global staple brand maturity cap",
        "KR",
        "failed_rerating",
        ("repeat_brand", "multi_region_footprint", "local_production"),
        ("mature_market_growth_cap", "input_cost_pressure", "regional_fx_geopolitical_risk", "regional_opm_not_improving"),
        "repeat_brand_not_green_if_region_growth_opm_and_cost_pass_through_fail",
        "needs_regional_growth_opm_cost_price_backfill",
        ("round_189.md Orion regional maturity cap",),
        "A global staple brand can still be capped when mature-market growth, input costs, or regional risk prevents OP/EPS expansion.",
        (E2RArchetype.STAGE2_EVIDENCE_NOT_GREEN,),
    ),
    Round189CaseCandidate(
        "convenience_store_cost_pressure_4c_watch_case",
        "CONVENIENCE_STORE_PB_SSSG_KOREA",
        "282330/007070",
        "Convenience-store cost pressure 4C watch",
        "KR",
        "failed_rerating",
        ("store_network", "defensive_demand", "pb_food"),
        ("wage_rent_electricity_cost_pressure", "franchisee_margin_pressure", "store_saturation", "opm_fcf_not_improving"),
        "defensive_retail_not_green_if_cost_pressure_offsets_pb_sssg",
        "needs_cost_franchisee_margin_opm_price_backfill",
        ("round_189.md convenience store cost pressure",),
        "Convenience-store scale is not Stage 3 if wage, rent, electricity, franchise margin, and OPM deteriorate.",
    ),
    Round189CaseCandidate(
        "r5_loop12_disclosure_confidence_reference_case",
        "DISCLOSURE_CONFIDENCE_CAP",
        "R5_DISCLOSURE_CAP",
        "R5 Loop 12 consumer / channel detail confidence reference",
        "KR",
        "failed_rerating",
        ("watch_disclosure_detail_required", "sales_channel_inventory_required", "sellthrough_required", "opm_fcf_required", "parser_confidence_required"),
        ("opendart_list_only", "media_report_only", "channel_missing", "inventory_missing", "opm_unknown", "fcf_unknown"),
        "list_media_channel_only_cannot_create_green",
        "needs_opendart_detail_channel_inventory_opm_fcf_backfill",
        ("round_189.md disclosure confidence rule",),
        "R5 Loop 12 requires detail fetch and forbids invented missing sales, channel, inventory, OPM, FCF, sell-through, and stage price fields.",
    ),
)


ROUND189_SCORE_STAGE_PRICE_ALIGNMENT: tuple[Round189ScoreStagePriceAlignment, ...] = (
    Round189ScoreStagePriceAlignment("cj_cheiljedang_kfood_localization_stage23_case", "Stage 2 -> Stage 3 candidate", "Localization is visible, but utilization, ASP, OPM, FCF, and 60D MFE need backfill", "stage2_to_stage3_if_utilization_opm_fcf_align", "credit local production; cap before utilization and FCF"),
    Round189ScoreStagePriceAlignment("orion_global_staple_brand_second_wave_case", "Stage 2 -> Stage 3 candidate", "Repeat snack demand is visible, but regional OPM and input-cost pass-through need backfill", "stage2_to_stage3_if_regional_opm_cost_align", "credit repeat demand; cap regional maturity and cost risk"),
    Round189ScoreStagePriceAlignment("bingle_lottewellfood_single_sku_export_watch_case", "Stage 1 -> Stage 2 watch", "Single SKU export can move before multi-SKU reorder is proven", "single_sku_requires_watch_cap", "cap until multi-SKU reorder, OPM, and inventory improve"),
    Round189ScoreStagePriceAlignment("emart_shinsegae_alibaba_jv_stage2_case", "Stage 2", "JV and +5.5% event return are real, but GMV/take-rate/FCF and data restrictions gate Stage 3", "jv_stage2_not_green_before_monetization", "credit JV catalyst; cap data regulation and competition"),
    Round189ScoreStagePriceAlignment("kbeauty_brand_second_wave_stage23_case", "Stage 2 -> Stage 3 candidate", "Online growth is strong, but physical sell-through, reorder, inventory, and OPM need backfill", "stage2_to_stage3_if_sellthrough_reorder_inventory_align", "credit channel growth; require sell-through quality"),
    Round189ScoreStagePriceAlignment("convenience_store_pb_sssg_stage23_case", "Stage 2 -> Stage 3 candidate", "Network and PB are visible, but SSSG, franchise margin, OPM, FCF, and cost control need backfill", "stage2_to_stage3_if_sssg_pb_cost_align", "credit PB/SSSG; cap wage/rent/electricity risk"),
    Round189ScoreStagePriceAlignment("lotte_shopping_mall_redevelopment_stage12_case", "Stage 1 -> Stage 2", "Mall plan is optionality, but CAPEX payback and traffic evidence are not proven", "redevelopment_stage12_until_payback", "cap before lease income, traffic, and FCF"),
    Round189ScoreStagePriceAlignment("kbeauty_tariff_import_review_4c_watch_case", "4C-watch", "Tariff risk can erase U.S. import growth if margin buffer is weak", "tariff_margin_buffer_hard_review", "block Green until price pass-through and inventory are verified"),
    Round189ScoreStagePriceAlignment("kbeauty_online_viral_not_sellthrough_4b_case", "Stage 2 -> 4B-watch", "Viral online growth can be priced before physical sell-through", "viral_without_sellthrough_requires_4b_watch", "cool K-beauty basket if price outruns sell-through/reorder"),
    Round189ScoreStagePriceAlignment("emart_alibaba_data_regulation_4c_watch_case", "4C-watch", "Data-sharing limits can delay platform monetization", "data_regulation_hard_gate", "block Green until monetization works inside the rule set"),
    Round189ScoreStagePriceAlignment("cj_kfood_localization_capex_drag_case", "Failed rerating", "Factories are cost centers until utilization and FCF appear", "capex_drag_blocks_green", "cap localization until utilization, OPM, and FCF"),
    Round189ScoreStagePriceAlignment("orion_global_staple_brand_maturity_cap_case", "Failed rerating", "A mature staple brand needs regional growth and cost pass-through", "maturity_cost_cap", "cap repeat-brand narrative when growth and OPM fade"),
    Round189ScoreStagePriceAlignment("convenience_store_cost_pressure_4c_watch_case", "Failed rerating / 4C-watch", "Cost pressure can offset PB and SSSG", "cost_pressure_blocks_green", "cap defensive retail until franchise margin and OPM recover"),
    Round189ScoreStagePriceAlignment("r5_loop12_disclosure_confidence_reference_case", "Confidence cap", "List/media/channel-only evidence lacks sell-through, inventory, OPM, and FCF", "detail_confidence_cap", "require verified channel, inventory, OPM, FCF, and parser confidence"),
)


ROUND189_PRICE_FIELDS: tuple[str, ...] = (
    "ticker",
    "company_name",
    "canonical_archetype",
    "case_type",
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
    "return_1d_after_event",
    "return_5d_after_event",
    "return_20d_after_stage2",
    "return_60d_after_stage2",
    "return_120d_after_stage2",
    "return_252d_after_stage2",
    "mfe_20d_after_stage2",
    "mae_20d_after_stage2",
    "mfe_60d_after_stage2",
    "mae_60d_after_stage2",
    "mfe_120d_after_stage2",
    "mae_120d_after_stage2",
    "mfe_252d_after_stage2",
    "mae_252d_after_stage2",
    "relative_strength_vs_kospi",
    "relative_strength_vs_kosdaq",
    "relative_strength_vs_consumer_basket",
    "relative_strength_vs_kfood_basket",
    "relative_strength_vs_kbeauty_basket",
    "relative_strength_vs_retail_basket",
    "export_growth_yoy",
    "us_sales_growth_yoy",
    "japan_sales_growth_yoy",
    "europe_sales_growth_yoy",
    "china_sales_growth_yoy",
    "channel_added",
    "channel_type",
    "offline_sell_through_signal",
    "reorder_signal",
    "mainstream_shelf_signal",
    "amazon_tiktok_signal",
    "ulta_sephora_costco_target_signal",
    "local_production_flag",
    "plant_utilization",
    "capex_amount",
    "capex_payback_signal",
    "jv_or_platform_event",
    "gmv_growth",
    "take_rate",
    "data_regulation_flag",
    "sssg",
    "pb_mix",
    "franchisee_margin_signal",
    "wage_rent_electricity_cost_signal",
    "op_revision_before_stage3",
    "op_revision_after_stage3",
    "eps_revision_before_stage3",
    "eps_revision_after_stage3",
    "gross_margin",
    "opm",
    "fcf_signal",
    "inventory_days",
    "inventory_days_change",
    "receivables_days",
    "receivables_days_change",
    "discount_rate_signal",
    "tariff_exposure",
    "single_sku_dependency",
    "regional_risk_flag",
    "disclosure_confidence",
    "valuation_at_stage3",
    "valuation_at_stage4b",
)


def round189_target_for(target_id: str) -> Round189ScoreTarget | None:
    for target in ROUND189_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round189_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND189_CASE_CANDIDATES:
        target = round189_target_for(candidate.target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {candidate.target_id}")
        weights = target.score_weight.as_dict()
        stage4b_evidence = candidate.evidence_fields if candidate.case_type == "4b_watch" else ()
        stage4c_evidence = candidate.red_flag_fields if candidate.case_type == "4c_thesis_break" or target.hard_gate else ()
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
            evidence_summary=(
                f"Round189 R5 Loop-12 Korea consumer/retail/brand case for {candidate.target_id}; "
                "calibration-only and focused on overseas channel, localization, sell-through, reorder, inventory/receivables, OPM/FCF, tariff/regulation/CAPEX risk, and price path."
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
            score_price_alignment=_round189_score_price_alignment(candidate),
            rerating_result=_round189_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
            score_weight_hint={
                "eps_fcf": _numeric_weight(weights["eps_fcf_opm_conversion"]),
                "overseas_channel_localization_platform_visibility": _numeric_weight(weights["overseas_channel_localization_platform_visibility"]),
                "sellthrough_reorder_recurring_consumption": _numeric_weight(weights["sellthrough_reorder_recurring_consumption"]),
                "inventory_receivables_margin_quality": _numeric_weight(weights["inventory_receivables_margin_quality"]),
                "early_price_validation": _numeric_weight(weights["early_price_validation"]),
                "tariff_regulation_capex_disclosure_redteam": _numeric_weight(weights["tariff_regulation_capex_disclosure_redteam"]),
                "valuation_4b_room": _numeric_weight(weights["valuation_4b_room"]),
            },
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "stage3_early_catch_requires_5_of_8_loop12_conditions",
                "stage4b_cooling_requires_4_of_6_loop12_conditions",
                "kfood_kbeauty_jv_convenience_keywords_cannot_create_stage3",
                "require_sellthrough_reorder_inventory_opm_fcf_and_price_path_for_green",
                "tariff_regulation_capex_inventory_and_disclosure_can_block_green",
                "do_not_invent_sales_channel_inventory_opm_fcf_sellthrough_prices_or_stage_dates",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=bool(candidate.source_refs),
                price_data_available=False,
                stage_dates_confidence=0.2,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round189_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND189_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "eps_fcf_opm_conversion": str(weights["eps_fcf_opm_conversion"]),
                "overseas_channel_localization_platform_visibility": str(weights["overseas_channel_localization_platform_visibility"]),
                "sellthrough_reorder_recurring_consumption": str(weights["sellthrough_reorder_recurring_consumption"]),
                "inventory_receivables_margin_quality": str(weights["inventory_receivables_margin_quality"]),
                "early_price_validation": str(weights["early_price_validation"]),
                "tariff_regulation_capex_disclosure_redteam": str(weights["tariff_regulation_capex_disclosure_redteam"]),
                "valuation_4b_room": str(weights["valuation_4b_room"]),
                "stage1_signals": "|".join(target.stage1_signals),
                "stage2_signals": "|".join(target.stage2_signals),
                "stage3_conditions": "|".join(target.stage3_conditions),
                "stage4b_conditions": "|".join(target.stage4b_conditions),
                "stage4c_conditions": "|".join(target.stage4c_conditions),
                "green_conditions": "|".join(target.green_conditions),
                "red_flags": "|".join(target.red_flags),
                "loop12_penalty_axes": "|".join(target.loop12_penalty_axes),
                "hard_gate": str(target.hard_gate).lower(),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round189_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND189_CASE_CANDIDATES:
        target = round189_target_for(candidate.target_id)
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
                "alignment_hint": candidate.alignment_hint,
                "price_validation_status": candidate.price_validation_status,
                "production_input": "false",
                "notes": candidate.notes,
            }
        )
    return tuple(rows)


def round189_stage_date_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "target_id": target.target_id,
            "stage1": "|".join(target.stage1_signals),
            "stage2": "|".join(target.stage2_signals),
            "stage3": "|".join(target.stage3_conditions),
            "stage4b": "|".join(target.stage4b_conditions),
            "stage4c": "|".join(target.stage4c_conditions),
            "red_flags": "|".join(target.red_flags),
            "hard_gate": str(target.hard_gate).lower(),
            "production_scoring_changed": "false",
        }
        for target in ROUND189_SCORE_TARGETS
    )


def round189_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round189_backfill": "true"} for field in ROUND189_PRICE_FIELDS)


def round189_base_score_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND189_BASE_SCORE_WEIGHTS)


def round189_stage_cap_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND189_STAGE_CAPS)


def round189_score_stage_price_alignment_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND189_SCORE_STAGE_PRICE_ALIGNMENT)


def round189_summary() -> dict[str, int | bool]:
    records = round189_case_records()
    return {
        "target_count": len(ROUND189_SCORE_TARGETS),
        "source_canonical_target_count": ROUND189_SOURCE_CANONICAL_TARGET_COUNT,
        "case_candidate_count": len(records),
        "base_score_axis_count": len(ROUND189_BASE_SCORE_WEIGHTS),
        "stage_cap_count": len(ROUND189_STAGE_CAPS),
        "score_stage_price_alignment_count": len(ROUND189_SCORE_STAGE_PRICE_ALIGNMENT),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "hard_gate_target_count": sum(1 for target in ROUND189_SCORE_TARGETS if target.hard_gate),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round189_r5_loop12_reports(
    *,
    output_directory: str | Path = ROUND189_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND189_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND189_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round189_r5_loop12_consumer_retail_brand_summary.md",
        "case_matrix": output / "round189_r5_loop12_case_matrix.csv",
        "stage_date_plan": output / "round189_r5_loop12_stage_date_plan.csv",
        "green_guardrails": output / "round189_r5_loop12_green_guardrails.md",
        "risk_overlays": output / "round189_r5_loop12_risk_overlays.md",
        "price_validation_plan": output / "round189_r5_loop12_price_validation_plan.md",
        "price_fields": output / "round189_r5_loop12_price_fields.csv",
        "base_score_weights": output / "round189_r5_loop12_base_score_weights.csv",
        "stage_caps": output / "round189_r5_loop12_stage_caps.csv",
        "score_stage_price_alignment": output / "round189_r5_loop12_score_stage_price_alignment.csv",
        "score_stage_price_alignment_md": output / "round189_r5_loop12_score_stage_price_alignment.md",
    }
    _write_case_jsonl(round189_case_records(), cases)
    _write_rows(round189_score_profile_rows(), score_profiles)
    _write_rows(round189_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round189_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round189_price_field_rows(), paths["price_fields"])
    _write_rows(round189_base_score_weight_rows(), paths["base_score_weights"])
    _write_rows(round189_stage_cap_rows(), paths["stage_caps"])
    _write_rows(round189_score_stage_price_alignment_rows(), paths["score_stage_price_alignment"])
    paths["summary"].write_text(render_round189_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round189_green_guardrail_markdown(), encoding="utf-8")
    paths["risk_overlays"].write_text(render_round189_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round189_price_validation_plan_markdown(), encoding="utf-8")
    paths["score_stage_price_alignment_md"].write_text(render_round189_score_stage_price_alignment_markdown(), encoding="utf-8")
    return paths


def render_round189_summary_markdown() -> str:
    summary = round189_summary()
    lines = [
        "# Round-189 R5 Loop-12 Consumer / Retail / Brand Summary",
        "",
        f"- source_round: `{ROUND189_SOURCE_ROUND_PATH}`",
        f"- large_sector: `{Round10LargeSector.CONSUMER_RETAIL_BRAND.value}`",
        "- loop: `R5 Loop 12 / v12.0`",
        f"- target_count: {summary['target_count']}",
        f"- source_canonical_target_count: {summary['source_canonical_target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- base_score_axis_count: {summary['base_score_axis_count']}",
        f"- stage_cap_count: {summary['stage_cap_count']}",
        f"- score_stage_price_alignment_count: {summary['score_stage_price_alignment_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- failed_rerating_count: {summary['failed_rerating_count']}",
        f"- stage4b_case_count: {summary['stage4b_case_count']}",
        f"- stage4c_case_count: {summary['stage4c_case_count']}",
        f"- hard_gate_target_count: {summary['hard_gate_target_count']}",
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "",
        "- R5 Loop 12 separates real consumer rerating from brand, viral, channel-entry, JV, and defensive-retail words.",
        "- Example: CJ localization is Stage 2 evidence, but utilization, ASP, OPM, FCF, and reorder gate Stage 3.",
        "- Example: E-Mart/Shinsegae Alibaba JV has a price reaction, but data regulation and monetization gate Stage 3.",
        "- Example: K-beauty online growth must become offline sell-through and reorder, or it becomes 4B-watch / 4C-watch.",
        "- Example: BGF/GS convenience-store scale needs SSSG, PB mix, franchise margin, OPM, and FCF.",
    ]
    return "\n".join(lines) + "\n"


def render_round189_green_guardrail_markdown() -> str:
    lines = [
        "# Round-189 R5 Loop-12 Green Guardrails",
        "",
        "Stage 3-Green is not granted for K-food, K-beauty, U.S. entry, JV, mall redevelopment, or convenience-store defensive words alone.",
        "",
        "## Stage 3 Early Catch",
        "",
        "R5 Loop 12 requires at least 5 of 8 checks:",
    ]
    stage3 = next(item for item in ROUND189_STAGE_CAPS if item.stage_band == "Stage 3")
    lines.extend(f"- `{field}`" for field in stage3.required_evidence)
    lines.extend(
        [
            "",
            "## What This Means",
            "",
            "- CJ제일제당: 현지 생산은 Stage 2, 가동률·ASP·OPM·FCF·재주문 전 Green 금지.",
            "- 오리온: 반복소비형 브랜드라도 지역별 성장률·OPM·원가전가가 필요.",
            "- 이마트/신세계: Alibaba JV는 Stage 2 catalyst지만 GMV·take-rate·수익화와 데이터 규제 통과가 필요.",
            "- K뷰티 브랜드 second wave: Amazon/TikTok 성장만으로는 부족하고 오프라인 sell-through와 reorder가 필요.",
            "- BGF/GS리테일: 방어주/점포망이 아니라 SSSG·PB mix·가맹점 마진·OPM·FCF가 Green gate.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round189_risk_overlay_markdown() -> str:
    lines = [
        "# Round-189 R5 Loop-12 Risk Overlays",
        "",
        "| target | hard gate | red flags |",
        "| --- | --- | --- |",
    ]
    for target in ROUND189_SCORE_TARGETS:
        lines.append(f"| `{target.target_id}` | {str(target.hard_gate).lower()} | {', '.join(target.red_flags)} |")
    lines.extend(
        [
            "",
            "## Hard / Cap Examples",
            "",
            "- `RETAIL_PLATFORM_DATA_REGULATION_OVERLAY`: Gmarket/AliExpress JV 데이터 제한은 수익화 cap이다.",
            "- `CHANNEL_STUFFING_INVENTORY_OVERLAY`: 재고·매출채권 급증은 K푸드/K뷰티/유통의 hard quality gate다.",
            "- `K_BEAUTY_TARIFF_IMPORT_REVIEW`: 미국 관세는 gross margin buffer 확인 전 4C-watch다.",
            "- `K_FOOD_SINGLE_SKU_EXPORT_RISK`: 단일 SKU viral은 반복 SKU와 재주문 전 Green 금지다.",
            "- `DISCLOSURE_CONFIDENCE_CAP`: 매출·채널·재고·OPM·FCF detail 없으면 Green 금지.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round189_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-189 R5 Loop-12 Price Validation Plan",
        "",
        "R5 Loop 12 must backfill overseas channel, localization, sell-through, reorder, inventory/receivables, tariff, JV regulation, convenience cost, and price-path fields together.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND189_PRICE_FIELDS)
    lines.extend(
        [
            "",
            "## Backfill Priorities",
            "",
            "- `cj_cheiljedang_kfood_localization_stage23_case`: overseas sales, plant utilization, ASP, OPM, FCF, 60D/120D MFE.",
            "- `orion_global_staple_brand_second_wave_case`: regional sales, regional OPM, input cost, FX/geopolitics, price path.",
            "- `emart_shinsegae_alibaba_jv_stage2_case`: event return, GMV, take-rate, data restriction, platform cost, FCF.",
            "- `kbeauty_brand_second_wave_stage23_case`: offline sell-through, reorder, inventory, receivables, OPM, tariff exposure.",
            "- `convenience_store_pb_sssg_stage23_case`: SSSG, PB mix, franchisee margin, wage/rent/electricity cost, OPM, FCF.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round189_score_stage_price_alignment_markdown() -> str:
    lines = [
        "# Round-189 R5 Loop-12 Score / Stage / Price Alignment",
        "",
        "| case | detected stage | price path status | verdict | adjustment |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in ROUND189_SCORE_STAGE_PRICE_ALIGNMENT:
        lines.append(f"| `{row.case_id}` | {row.detected_stage} | {row.price_path_status} | {row.verdict} | {row.normalization_adjustment} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- CJ and Orion show how K-food can be Stage 2~3 only when localization or repeat demand converts into OPM/FCF.",
            "- E-Mart/Shinsegae shows why a real JV and price reaction can still be capped by data regulation and monetization risk.",
            "- K-beauty and convenience-store cases show why sell-through, reorder, SSSG, PB mix, and inventory quality are required before Green.",
        ]
    )
    return "\n".join(lines) + "\n"


def _round189_score_price_alignment(candidate: Round189CaseCandidate) -> str:
    if candidate.case_type in {"success_candidate", "structural_success"}:
        return "unknown"
    if candidate.case_type in {"event_premium", "4b_watch", "cyclical_success"}:
        return "price_moved_without_evidence"
    if candidate.case_type == "4c_thesis_break":
        return "false_positive_score"
    if candidate.case_type == "failed_rerating":
        return "evidence_good_but_price_failed"
    return "unknown"


def _round189_rerating_result(candidate: Round189CaseCandidate) -> str:
    if candidate.case_type in {"success_candidate", "structural_success"}:
        return "unknown"
    if candidate.case_type == "event_premium":
        return "event_premium"
    if candidate.case_type == "cyclical_success":
        return "cyclical_rerating"
    if candidate.case_type == "4b_watch":
        return "theme_overheat"
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    if candidate.case_type == "failed_rerating":
        return "no_rerating"
    return "unknown"


def _numeric_weight(value: int | str) -> float:
    return float(value) if isinstance(value, int) else 0.0


def _write_case_jsonl(records: Iterable[E2RCaseRecord], path: Path) -> None:
    lines = []
    for record in records:
        record.validate()
        lines.append(json.dumps(record.as_dict(), ensure_ascii=False, sort_keys=True))
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def _write_rows(rows: Iterable[Mapping[str, str]], path: Path) -> None:
    rows = tuple(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


__all__ = [
    "ROUND189_BASE_SCORE_WEIGHTS",
    "ROUND189_CASE_CANDIDATES",
    "ROUND189_DEFAULT_CASES_PATH",
    "ROUND189_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND189_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND189_PRICE_FIELDS",
    "ROUND189_SCORE_STAGE_PRICE_ALIGNMENT",
    "ROUND189_SCORE_TARGETS",
    "ROUND189_SOURCE_CANONICAL_TARGET_COUNT",
    "ROUND189_SOURCE_CANONICAL_TARGET_IDS",
    "ROUND189_STAGE_CAPS",
    "render_round189_green_guardrail_markdown",
    "render_round189_price_validation_plan_markdown",
    "render_round189_risk_overlay_markdown",
    "render_round189_score_stage_price_alignment_markdown",
    "render_round189_summary_markdown",
    "round189_base_score_weight_rows",
    "round189_case_candidate_rows",
    "round189_case_records",
    "round189_price_field_rows",
    "round189_score_profile_rows",
    "round189_score_stage_price_alignment_rows",
    "round189_stage_cap_rows",
    "round189_stage_date_rows",
    "round189_summary",
    "round189_target_for",
    "write_round189_r5_loop12_reports",
]
