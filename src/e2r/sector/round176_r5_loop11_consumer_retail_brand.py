"""Round-176 R5 Loop-11 Korea consumer, retail, and brand pack.

Round 176 applies Loop 11 to Korea-focused K-beauty distribution, K-beauty
brands, Olive Young/CJ platform optionality, K-beauty OEM/ODM, K-food staple
brands, apparel-license risk, China consumer exposure, tariffs, and channel
stuffing. It is calibration/report material only. Production feature
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


ROUND176_SOURCE_ROUND_PATH = "docs/round/round_176.md"
ROUND176_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round176_r5_loop11_consumer_retail_brand"
ROUND176_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r5_loop11_round176.jsonl"
ROUND176_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round176_r5_loop11_v11.csv"
ROUND176_SOURCE_CANONICAL_TARGET_IDS: tuple[str, ...] = (
    "K_BEAUTY_EXPORT_DISTRIBUTION_KOREA",
    "K_BEAUTY_BRAND_US_CHANNEL",
    "K_BEAUTY_RETAIL_PLATFORM_OPTION",
    "K_BEAUTY_OEM_ODM_SUPPLYCHAIN_KOREA",
    "K_FOOD_GLOBAL_STAPLE_BRAND",
    "K_FOOD_SINGLE_SKU_RISK",
    "APPAREL_LICENSE_BRAND_CHINA_RISK",
    "CHINA_CONSUMER_EXPOSURE_4C",
    "TARIFF_IMPORT_MARGIN_OVERLAY",
    "CHANNEL_STUFFING_INVENTORY_OVERLAY",
    "DISCLOSURE_CONFIDENCE_CAP",
)
ROUND176_SOURCE_CANONICAL_TARGET_COUNT = len(ROUND176_SOURCE_CANONICAL_TARGET_IDS)


@dataclass(frozen=True)
class Round176ScoreWeightDraft:
    eps_fcf_opm: int | str
    export_channel_visibility: int | str
    sell_through_reorder: int | str
    inventory_receivables_margin_quality: int | str
    early_price_validation: int | str
    safety_tariff_disclosure: int | str
    valuation_4b_room: int | str

    def as_dict(self) -> dict[str, int | str]:
        return {
            "eps_fcf_opm": self.eps_fcf_opm,
            "export_channel_visibility": self.export_channel_visibility,
            "sell_through_reorder": self.sell_through_reorder,
            "inventory_receivables_margin_quality": self.inventory_receivables_margin_quality,
            "early_price_validation": self.early_price_validation,
            "safety_tariff_disclosure": self.safety_tariff_disclosure,
            "valuation_4b_room": self.valuation_4b_room,
        }


@dataclass(frozen=True)
class Round176ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round176ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    loop11_penalty_axes: tuple[str, ...]
    normalization_point: str
    hard_gate: bool = False

    @property
    def large_sector(self) -> Round10LargeSector:
        return Round10LargeSector.CONSUMER_RETAIL_BRAND

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round176CaseCandidate:
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


@dataclass(frozen=True)
class Round176BaseScoreWeight:
    component: str
    points: int
    loop11_direction: str
    reason: str

    def as_row(self) -> dict[str, str]:
        return {
            "component": self.component,
            "points": str(self.points),
            "loop11_direction": self.loop11_direction,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class Round176StageCap:
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
        }


@dataclass(frozen=True)
class Round176ScoreStagePriceAlignment:
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
        }


def _weights(
    eps: int | str,
    channel: int | str,
    sell_through: int | str,
    quality: int | str,
    price: int | str,
    safety: int | str,
    valuation: int | str,
) -> Round176ScoreWeightDraft:
    return Round176ScoreWeightDraft(eps, channel, sell_through, quality, price, safety, valuation)


def _target(
    target_id: str,
    archetype: E2RArchetype,
    posture: Round10ThemePosture,
    weight: Round176ScoreWeightDraft,
    *,
    stage1: tuple[str, ...],
    stage2: tuple[str, ...],
    stage3: tuple[str, ...],
    stage4b: tuple[str, ...],
    stage4c: tuple[str, ...],
    green: tuple[str, ...],
    red: tuple[str, ...],
    penalties: tuple[str, ...],
    note: str,
    hard_gate: bool = False,
) -> Round176ScoreTarget:
    return Round176ScoreTarget(
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


ROUND176_BASE_SCORE_WEIGHTS: tuple[Round176BaseScoreWeight, ...] = (
    Round176BaseScoreWeight("eps_fcf_opm_conversion", 23, "keep_high", "Stage 3 needs OP/EPS/FCF and margin conversion, not K-food or K-beauty keywords."),
    Round176BaseScoreWeight("export_channel_visibility", 21, "raise_channel_detail", "US/Japan/Europe sales, Amazon/TikTok/Ulta/Sephora/Costco/Target, offline entry, ASP, and mainstream shelf drive Stage 2."),
    Round176BaseScoreWeight("sell_through_reorder_repeat_consumption", 18, "raise_for_loop11", "Shipment and listing are capped until sell-through, reorder, and repeat consumption are visible."),
    Round176BaseScoreWeight("inventory_receivables_margin_quality", 12, "hard_quality_gate", "Inventory days, receivables days, gross margin, OPM, and discount rate decide whether growth is real."),
    Round176BaseScoreWeight("early_price_path_validation", 10, "loop11_axis", "60D/120D price path separates early Stage 3 catch from late 4B chasing."),
    Round176BaseScoreWeight("safety_tariff_disclosure_confidence", 8, "redteam_review", "Tariff, China exposure, recalls, product safety, and disclosure gaps cap Stage 3."),
    Round176BaseScoreWeight("valuation_room_4b_runway", 8, "cool_brand_rallies", "IPO doubles, viral brand rerating, and K-beauty/K-food crowding reduce runway quickly."),
)


ROUND176_STAGE_CAPS: tuple[Round176StageCap, ...] = (
    Round176StageCap(
        "Stage 1",
        "45",
        ("k_food_viral", "k_beauty_viral", "us_listing_expectation", "tiktok_shop", "amazon", "ulta_sephora_costco_target", "olive_young_us_news"),
        ("silicon2_kbeauty_distribution_stage3_candidate", "dalba_global_ipo_4b_watch_case"),
        "Viral, listing, GMV, and brand awareness route research only. They do not create Stage 3.",
    ),
    Round176StageCap(
        "Stage 2",
        "70",
        ("us_japan_europe_sales", "retail_partnership", "online_sales", "export_growth", "asp", "ipo_or_platform_option", "oem_order_visibility"),
        ("cj_oliveyoung_platform_holdco_cap_case", "nongshim_global_staple_stage2_case"),
        "Stage 2 can be strong, but Green waits for sell-through, reorder, OPM, FCF, and inventory/receivables quality.",
    ),
    Round176StageCap(
        "Stage 3",
        "requires_4_of_7",
        ("export_or_overseas_sales_growth", "op_eps_revision_or_op_beat", "us_japan_europe_channel_expansion", "sell_through_or_reorder", "inventory_receivables_not_worse", "60d_mfe_20pct", "valuation_not_peer_top_quartile"),
        ("silicon2_kbeauty_distribution_stage3_candidate", "kbeauty_oem_odm_supplychain_stage3_candidate", "nongshim_global_staple_stage2_case"),
        "Stage 3 is possible only when channel growth converts into repeat demand, earnings, and quality of working capital.",
    ),
    Round176StageCap(
        "Stage 4B",
        "requires_3_of_5",
        ("stage2_120d_mfe_80pct", "ipo_or_viral_brand_price_doubles", "narrative_before_earnings", "inventory_receivables_start_rising", "kbeauty_kfood_keyword_crowded"),
        ("dalba_global_ipo_4b_watch_case", "silicon2_kbeauty_distribution_stage3_candidate"),
        "Brand and IPO rallies are cooled when price outruns sell-through, reorder, or OP/EPS.",
    ),
    Round176StageCap(
        "Stage 4C",
        "hard_gate",
        ("china_premium_demand_slowdown_earnings_miss", "us_tariff_price_competitiveness_hit", "channel_stuffing", "inventory_or_receivables_spike", "single_viral_sku_demand_drop", "recall_or_safety_issue", "oem_customer_order_cancel_or_indie_brand_churn", "license_brand_saturation_or_mna_overpay"),
        ("amorepacific_china_exposure_4c_case", "fnf_license_brand_china_mna_watch_case", "channel_stuffing_inventory_overlay_case"),
        "Hard RedTeam overrides consumer export narratives when sell-through, inventory, tariff, China exposure, or brand saturation breaks the path.",
    ),
)


ROUND176_SCORE_TARGETS: tuple[Round176ScoreTarget, ...] = (
    _target(
        "K_BEAUTY_EXPORT_DISTRIBUTION_KOREA",
        E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION_KOREA,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(23, 22, 19, 12, 10, 8, 8),
        stage1=("kbeauty_viral", "amazon_tiktok_ecommerce_growth", "us_kbeauty_import_growth"),
        stage2=("portfolio_distributor_role", "us_ecommerce_growth", "brand_portfolio", "offline_channel_expansion"),
        stage3=("op_eps_revision", "portfolio_diversification", "sell_through", "reorder", "inventory_receivables_stable", "fcf_improvement"),
        stage4b=("kbeauty_platform_narrative_crowded", "stock_multibagger", "eps_revision_lags_price"),
        stage4c=("sell_through_slowdown", "inventory_days_up", "receivables_days_up", "discount_rate_up"),
        green=("op_eps_revision", "sell_through", "reorder", "inventory_receivables_stable", "opm_fcf"),
        red=("sell_through_missing", "inventory_receivables_unknown", "price_multibagger", "channel_stuffing_risk"),
        penalties=("sell_through", "inventory_receivables", "valuation_4b"),
        note="Silicon2-style K-beauty distribution can be Stage 2/3, but sell-through, reorder, inventory, receivables, and OPM decide Green.",
    ),
    _target(
        "K_BEAUTY_BRAND_US_CHANNEL",
        E2RArchetype.K_BEAUTY_BRAND_US_CHANNEL,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(21, 22, 17, 11, 10, 8, 7),
        stage1=("brand_viral", "us_retail_expansion_expectation", "tiktok_amazon"),
        stage2=("costco_ulta_target_talks", "sephora_ulta_channel", "listed_price_path", "us_channel_visibility"),
        stage3=("actual_listing", "sell_through", "reorder", "opm_fcf", "tariff_absorption"),
        stage4b=("ipo_price_doubles", "single_brand_valuation_priced", "viral_narrative_crowded"),
        stage4c=("offline_sell_through_failure", "tariff_margin_hit", "single_brand_fade", "inventory_up"),
        green=("actual_listing", "sell_through", "reorder", "opm_fcf", "tariff_absorption"),
        red=("sell_through_missing", "ipo_valuation_risk", "single_brand_dependency", "tariff_risk"),
        penalties=("ipo_4b", "sell_through", "single_brand", "tariff"),
        note="D'Alba/VT/Clio-style brands can be Stage 2/3, but IPO doubles and single-brand rerating need 4B-watch.",
    ),
    _target(
        "K_BEAUTY_RETAIL_PLATFORM_OPTION",
        E2RArchetype.K_BEAUTY_RETAIL_PLATFORM_OPTION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(18, 22, 16, 10, 8, 8, 8),
        stage1=("olive_young_us_expansion", "kbeauty_platform", "sephora_ulta_competition"),
        stage2=("us_first_store", "global_mall", "1300_korea_stores", "platform_curation", "ipo_option"),
        stage3=("cj_consolidated_earnings_link", "oliveyoung_opm_growth", "us_store_sell_through", "ipo_or_cash_realization", "nav_discount_narrows"),
        stage4b=("oliveyoung_expectation_priced_before_cash_link", "ipo_premium_crowded"),
        stage4c=("us_store_sell_through_failure", "ipo_delay", "holdco_discount_persists"),
        green=("cj_cashflow_link", "opm_growth", "sell_through", "ipo_or_cash_realization", "nav_discount_narrows"),
        red=("holdco_link_missing", "cashflow_link_missing", "ipo_event_only", "sell_through_missing"),
        penalties=("holdco_link", "ipo_event", "sell_through"),
        note="CJ/Olive Young is Stage 2 platform optionality; CJ Stage 3 requires cash-flow or NAV discount transmission.",
    ),
    _target(
        "K_BEAUTY_OEM_ODM_SUPPLYCHAIN_KOREA",
        E2RArchetype.K_BEAUTY_OEM_ODM_SUPPLYCHAIN_KOREA,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(23, 20, 20, 13, 10, 7, 7),
        stage1=("indie_brand_boom", "fast_beauty_supply_chain", "kbeauty_us_japan_eu_channels"),
        stage2=("multi_brand_orders", "customer_diversification", "repeat_order_visibility", "us_japan_eu_mix"),
        stage3=("repeat_orders", "customer_diversification", "opm_fcf_improvement", "inventory_receivables_stable", "op_eps_revision"),
        stage4b=("oem_odm_basket_catches_up_late", "multiple_before_eps"),
        stage4c=("brand_sell_through_failure", "channel_inventory_up", "receivables_worse", "indie_brand_churn"),
        green=("repeat_orders", "customer_diversification", "opm_fcf", "inventory_receivables_stable", "op_eps_revision"),
        red=("inventory_receivables_unknown", "brand_sell_through_dependency", "customer_churn", "opm_missing"),
        penalties=("inventory_receivables", "customer_churn", "brand_sell_through"),
        note="Cosmax/Kolmar/C&C-style OEM/ODM can be early Stage 3 candidates when multi-brand repeat orders convert into OPM/FCF.",
    ),
    _target(
        "K_FOOD_GLOBAL_STAPLE_BRAND",
        E2RArchetype.K_FOOD_GLOBAL_STAPLE_BRAND,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(23, 21, 18, 12, 10, 8, 8),
        stage1=("kfood_globalization", "ramen_global_demand", "k_culture"),
        stage2=("record_sales", "overseas_revenue_mix", "walmart_mainstream_shelf", "us_sales_target", "us_plant_expansion_review"),
        stage3=("us_europe_sales_growth", "asp_defended", "op_eps_revision", "inventory_stable", "reorder_repeat_consumption", "china_slowdown_offset"),
        stage4b=("ramen_export_narrative_crowded", "single_sku_or_premium_sku_valuation_rally"),
        stage4c=("china_slowdown_not_offset", "cost_inflation", "inventory_up", "single_sku_fade"),
        green=("overseas_sales_growth", "asp", "op_eps_revision", "reorder", "inventory_stable"),
        red=("op_eps_missing", "china_slowdown", "single_sku_risk", "cost_inflation"),
        penalties=("single_sku", "china", "op_eps"),
        note="Nongshim-style global staple brand is Stage 2/3 when overseas sales and mainstream shelf gains convert into OP/EPS.",
    ),
    _target(
        "K_FOOD_SINGLE_SKU_RISK",
        E2RArchetype.K_FOOD_SINGLE_SKU_RISK,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("gate", "gate", "gate", "gate", "gate", "gate", "gate"),
        stage1=("viral_sku", "premium_sku", "tiktok_food_trend"),
        stage2=("single_sku_sales_growth", "retail_listing"),
        stage3=("not_green_without_portfolio_repeat_demand",),
        stage4b=("single_sku_viral_price_doubles", "food_theme_crowded"),
        stage4c=("viral_sku_demand_drop", "recall_or_food_safety", "retailer_reorder_decline"),
        green=(),
        red=("single_sku_dependency", "portfolio_missing", "reorder_missing", "food_safety_risk"),
        penalties=("single_sku", "reorder", "safety"),
        note="Single-SKU K-food can route research but is hard-capped before portfolio repeat demand and OP/EPS evidence.",
        hard_gate=True,
    ),
    _target(
        "APPAREL_LICENSE_BRAND_CHINA_RISK",
        E2RArchetype.APPAREL_LICENSE_BRAND_CHINA_RISK,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights(16, 14, 10, 12, 8, 8, 7),
        stage1=("licensed_logo_brand_growth", "china_asia_expansion", "taylormade_option"),
        stage2=("brand_revenue_growth", "mna_option", "license_platform"),
        stage3=("inventory_markdown_stable", "china_sell_through", "opm_fcf", "mna_discipline"),
        stage4b=("license_brand_saturation_ignored", "mna_option_priced"),
        stage4c=("licensed_logo_fatigue", "china_consumption_slowdown", "inventory_markdown_up", "mna_governance_overpay"),
        green=("sell_through", "inventory_markdown_stable", "opm_fcf", "mna_discipline"),
        red=("brand_saturation", "china_exposure", "inventory_markdown", "mna_governance_risk"),
        penalties=("china", "inventory", "mna_governance", "brand_saturation"),
        note="F&F-style licensed brands are Watch/Red when China exposure, logo fatigue, and M&A governance risk dominate.",
    ),
    _target(
        "CHINA_CONSUMER_EXPOSURE_4C",
        E2RArchetype.CHINA_CONSUMER_EXPOSURE_4C,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("gate", "gate", "gate", "gate", "gate", "gate", "gate"),
        stage1=("china_consumption_recovery_expectation", "premium_beauty", "turnaround_story"),
        stage2=("north_america_emea_growth", "brand_portfolio", "acquisition"),
        stage3=("not_green_while_china_premium_demand_breaks",),
        stage4b=("recovery_story_priced_before_china_turnaround",),
        stage4c=("china_demand_weakness", "domestic_brand_preference", "earnings_miss", "worst_day_price_drop"),
        green=(),
        red=("china_exposure", "earnings_miss", "premium_beauty_derating", "domestic_brand_preference"),
        penalties=("china", "earnings_miss", "derating"),
        note="Amorepacific/LG H&H-style China premium exposure is a hard 4C watch inside K-beauty.",
        hard_gate=True,
    ),
    _target(
        "TARIFF_IMPORT_MARGIN_OVERLAY",
        E2RArchetype.TARIFF_IMPORT_MARGIN_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("gate", "gate", "gate", "gate", "gate", "gate", "gate"),
        stage1=("us_tariff_uncertainty", "kbeauty_us_export_growth", "kfood_export_growth"),
        stage2=("gross_margin_buffer", "price_hike_tolerance", "retailer_reorder"),
        stage3=("tariff_absorption_without_demand_loss", "margin_buffer_proven", "sell_through_stable"),
        stage4b=("tariff_ignored_by_brand_rally",),
        stage4c=("price_competitiveness_hit", "consumer_purchase_delay", "retailer_inventory_adjustment", "gross_margin_hit"),
        green=(),
        red=("tariff_uncertainty", "margin_buffer_missing", "price_hike_risk", "retailer_reorder_risk"),
        penalties=("tariff", "margin_buffer", "price_hike"),
        note="Tariff can cap K-beauty/K-food Stage 3 unless margin buffer and price pass-through are proven.",
        hard_gate=True,
    ),
    _target(
        "CHANNEL_STUFFING_INVENTORY_OVERLAY",
        E2RArchetype.CHANNEL_STUFFING_INVENTORY_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("gate", "gate", "gate", "gate", "gate", "gate", "gate"),
        stage1=("shipment_growth", "listing_growth", "export_growth"),
        stage2=("channel_expansion", "order_growth"),
        stage3=("sell_through", "reorder", "inventory_days_stable", "receivables_days_stable", "gross_margin_stable"),
        stage4b=("shipment_growth_priced_before_sell_through",),
        stage4c=("shipment_only_growth", "sell_through_slowdown", "inventory_days_up", "receivables_days_up", "discount_rate_up"),
        green=(),
        red=("inventory_days_up", "receivables_days_up", "sell_through_slowdown", "discount_rate_up"),
        penalties=("inventory", "receivables", "sell_through", "discount"),
        note="Shipment growth is capped before sell-through, reorder, inventory days, receivables days, and margin quality are verified.",
        hard_gate=True,
    ),
    _target(
        "DISCLOSURE_CONFIDENCE_CAP",
        E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("cap", "cap", "cap", "cap", "cap", "+", "cap"),
        stage1=("headline_listing", "opendart_list_only", "media_report_only", "brand_viral"),
        stage2=("detail_fetch_required", "channel", "reorder", "inventory", "margin", "contract_terms"),
        stage3=("multi_source_confirmation", "sell_through_verified", "opm_fcf_visible"),
        stage4b=("headline_brand_rally",),
        stage4c=("channel_missing", "reorder_missing", "inventory_unknown", "margin_unknown"),
        green=("channel", "sell_through", "reorder", "inventory", "opm_fcf"),
        red=("detail_missing", "channel_missing", "reorder_missing", "inventory_unknown", "margin_unknown"),
        penalties=("disclosure_detail", "channel", "inventory", "margin"),
        note="Consumer/brand headlines cannot support Stage 3-Green until channel, reorder, inventory, and margin details are verified.",
    ),
    _target(
        "K_BEAUTY_BRAND_MNA_VALIDATION_STAGE2_REFERENCE",
        E2RArchetype.K_BEAUTY_BRAND_MNA_VALIDATION_STAGE2_REFERENCE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(18, 18, 12, 10, 8, 8, 7),
        stage1=("kbeauty_global_demand", "skincare_brand_mna"),
        stage2=("global_major_acquires_korean_brand", "pan_asia_global_growth_potential"),
        stage3=("listed_company_revenue_link", "opm", "transaction_price_detail", "fcf"),
        stage4b=("mna_reference_priced_without_direct_link",),
        stage4c=("mna_reference_not_relevant_to_listed_company", "price_detail_missing"),
        green=("listed_company_link", "transaction_price", "opm", "fcf"),
        red=("direct_link_missing", "transaction_price_missing", "not_listed_company"),
        penalties=("direct_link", "price_detail"),
        note="Dr.G-style M&A validates K-beauty strategic value, but listed-company Stage 3 still needs direct revenue/OPM link.",
    ),
    _target(
        "STRONG_PRIVATE_PLATFORM_BUT_HOLDCO_LINK_CAP",
        E2RArchetype.STRONG_PRIVATE_PLATFORM_BUT_HOLDCO_LINK_CAP,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights("cap", "cap", "cap", "cap", "cap", "+", "cap"),
        stage1=("strong_private_platform", "holdco_hidden_asset", "ipo_expectation"),
        stage2=("platform_growth", "ipo_option", "nav_discount_story"),
        stage3=("cashflow_link_to_listed_parent", "ipo_cash_realization", "shareholder_return", "nav_discount_narrows"),
        stage4b=("hidden_asset_priced_before_cash_link",),
        stage4c=("ipo_delay", "cashflow_link_missing", "holdco_discount_persists"),
        green=(),
        red=("cashflow_link_missing", "ipo_event_only", "holdco_discount", "private_platform_not_listed"),
        penalties=("holdco_link", "cash_realization", "nav_discount"),
        note="A strong private platform cannot create listed-parent Green without cash-flow, IPO, or NAV-discount transmission.",
        hard_gate=True,
    ),
)


ROUND176_CASE_CANDIDATES: tuple[Round176CaseCandidate, ...] = (
    Round176CaseCandidate(
        "silicon2_kbeauty_distribution_stage3_candidate",
        "K_BEAUTY_EXPORT_DISTRIBUTION_KOREA",
        "257720",
        "Silicon2 K-beauty distribution platform",
        "KR",
        "success_candidate",
        date(2025, 6, 5),
        date(2025, 6, 5),
        None,
        None,
        None,
        ("us_kbeauty_imports_surpass_france", "top_kbeauty_ecommerce_growth_71pct", "amazon_ecommerce_growth", "portfolio_distributor_role", "physical_store_sell_through_needed"),
        ("sell_through_missing", "inventory_receivables_unknown", "price_multibagger_4b_risk"),
        "portfolio_distribution_stage2_3_candidate",
        "needs_krx_price_and_working_capital_backfill",
        ("round_176.md Reuters K-beauty startups and Silicon2 CEO",),
        "Silicon2 should be scored as K-beauty portfolio distribution, not one viral brand. Stage 3 needs sell-through, reorder, inventory, receivables, OPM, and FCF.",
        (E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION, E2RArchetype.CHANNEL_STUFFING_INVENTORY_OVERLAY),
    ),
    Round176CaseCandidate(
        "dalba_global_ipo_4b_watch_case",
        "K_BEAUTY_BRAND_US_CHANNEL",
        "483650",
        "D'Alba Global US channel / IPO rerating",
        "KR",
        "4b_watch",
        date(2025, 6, 5),
        date(2025, 6, 5),
        None,
        date(2025, 6, 5),
        None,
        ("vegan_mist_serum_sunscreen_brand", "costco_ulta_target_talks", "us_retail_distribution", "post_listing_price_more_than_double"),
        ("actual_sell_through_missing", "ipo_valuation_risk", "tariff_risk", "single_brand_dependency"),
        "stage2_plus_4b_watch_after_ipo_double",
        "needs_exact_ipo_price_path_backfill",
        ("round_176.md Reuters d'Alba Global US retail talks and post-listing rerating",),
        "D'Alba has strong US channel visibility, but post-listing doubling means Stage 2 plus 4B-watch before sell-through and OPM proof.",
        (E2RArchetype.TARIFF_IMPORT_MARGIN_OVERLAY,),
    ),
    Round176CaseCandidate(
        "cj_oliveyoung_platform_holdco_cap_case",
        "K_BEAUTY_RETAIL_PLATFORM_OPTION",
        "001040",
        "CJ / Olive Young K-beauty retail platform option",
        "KR",
        "success_candidate",
        date(2025, 6, 5),
        date(2025, 6, 5),
        None,
        None,
        None,
        ("olive_young_us_first_store_plan", "global_mall", "1300_plus_korea_stores", "sephora_ulta_kbeauty_competition", "kbeauty_curation_platform"),
        ("cj_cashflow_link_missing", "ipo_event_premium_risk", "us_store_sell_through_missing", "nav_discount_persists"),
        "strong_private_platform_holdco_link_cap",
        "needs_cj_price_and_oliveyoung_financial_link_backfill",
        ("round_176.md Business Insider Olive Young US expansion", "round_176.md Reuters Olive Young LA store and Sephora K-beauty launch"),
        "Olive Young is high-quality Stage 2 platform evidence, but CJ Stage 3 needs cash-flow, IPO, shareholder return, or NAV transmission.",
        (E2RArchetype.STRONG_PRIVATE_PLATFORM_BUT_HOLDCO_LINK_CAP,),
    ),
    Round176CaseCandidate(
        "nongshim_global_staple_stage2_case",
        "K_FOOD_GLOBAL_STAPLE_BRAND",
        "004370",
        "Nongshim Shin Ramyun global staple brand",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("shin_ramyun_record_sales_1_2tn_krw", "overseas_sales_nearly_60pct", "us_sales_2030_target_1_5bn_usd", "walmart_mainstream_shelf_move", "us_capacity_review"),
        ("op_eps_confirmation_needed", "china_slowdown", "single_sku_risk", "inventory_backfill_needed"),
        "global_staple_stage2_3_candidate",
        "needs_source_date_and_krx_price_backfill",
        ("round_176.md Financial Times Nongshim overseas expansion",),
        "Nongshim is the non-Samyang K-food staple reference. Stage 3 needs OP/EPS, ASP, reorder, and inventory stability.",
        (E2RArchetype.K_FOOD_SINGLE_SKU_RISK,),
    ),
    Round176CaseCandidate(
        "kbeauty_oem_odm_supplychain_stage3_candidate",
        "K_BEAUTY_OEM_ODM_SUPPLYCHAIN_KOREA",
        "192820/161890/352480",
        "Cosmax / Kolmar Korea / C&C International fast beauty supply chain",
        "KR",
        "success_candidate",
        date(2025, 6, 5),
        date(2025, 6, 5),
        None,
        None,
        None,
        ("indie_brand_us_channel_expansion", "multi_brand_orders", "fast_beauty_odm", "customer_diversification", "repeat_order_potential"),
        ("inventory_receivables_unknown", "brand_sell_through_dependency", "customer_churn_risk", "opm_backfill_needed"),
        "fast_beauty_repeat_order_stage2_3_candidate",
        "needs_krx_price_op_revision_inventory_receivables_backfill",
        ("round_176.md Reuters K-beauty brand expansion implies OEM/ODM demand",),
        "K-beauty OEM/ODM can be earlier Stage 3 than single brands if customer diversification, repeat orders, OPM, and working capital are clean.",
        (E2RArchetype.BEAUTY_OEM_ODM_SUPPLYCHAIN, E2RArchetype.CHANNEL_STUFFING_INVENTORY_OVERLAY),
    ),
    Round176CaseCandidate(
        "drg_kbeauty_mna_stage2_reference_case",
        "K_BEAUTY_BRAND_MNA_VALIDATION_STAGE2_REFERENCE",
        "PRIVATE_DRG",
        "Dr.G / Gowoonsesang K-beauty M&A reference",
        "KR",
        "success_candidate",
        date(2024, 12, 23),
        date(2024, 12, 23),
        None,
        None,
        None,
        ("loreal_acquires_korean_skincare_brand", "affordable_effective_skincare", "pan_asian_global_growth_potential"),
        ("transaction_price_missing", "listed_company_direct_link_missing", "opm_missing"),
        "mna_reference_not_direct_green",
        "not_price_applicable_private_reference",
        ("round_176.md Reuters L'Oreal acquires Dr.G",),
        "Dr.G validates Korean skincare strategic value but is reference evidence, not a listed-company Green signal without direct linkage.",
    ),
    Round176CaseCandidate(
        "amorepacific_china_exposure_4c_case",
        "CHINA_CONSUMER_EXPOSURE_4C",
        "090430",
        "Amorepacific premium beauty China derating",
        "KR",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        None,
        ("premium_beauty_china_exposure", "q2_earnings_miss", "china_demand_weakness", "domestic_brand_preference", "worst_day_price_drop"),
        ("china_exposure", "earnings_miss", "premium_beauty_derating", "domestic_brand_preference"),
        "kbeauty_china_exposure_4c",
        "needs_exact_stage_date_backfill",
        ("round_176.md Financial Times Amorepacific China demand weakness",),
        "Amorepacific proves K-beauty is not one bucket. China premium exposure can be hard 4C despite global K-beauty strength.",
        (E2RArchetype.K_BEAUTY_TARIFF_IMPORT_REVIEW,),
    ),
    Round176CaseCandidate(
        "kbeauty_tariff_import_margin_review_case",
        "TARIFF_IMPORT_MARGIN_OVERLAY",
        "K_BEAUTY_EXPORT_BASKET",
        "K-beauty tariff import margin review",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("us_kbeauty_imports_1_7bn_usd", "us_import_growth_54pct", "tariff_uncertainty", "retailer_inventory_adjustment_risk"),
        ("tariff_uncertainty", "gross_margin_buffer_missing", "price_hike_risk", "consumer_purchase_delay"),
        "tariff_margin_buffer_stage3_gate",
        "not_price_applicable_overlay",
        ("round_176.md AP K-beauty tariff risk",),
        "US export growth remains positive, but Stage 3 needs gross-margin buffer and price pass-through without demand loss.",
    ),
    Round176CaseCandidate(
        "fnf_license_brand_china_mna_watch_case",
        "APPAREL_LICENSE_BRAND_CHINA_RISK",
        "383220",
        "F&F licensed brand / TaylorMade governance watch",
        "KR",
        "failed_rerating",
        date(2025, 7, 21),
        None,
        None,
        None,
        None,
        ("licensed_logo_brand_platform", "fy2024_revenue_1_3bn_usd_reference", "taylormade_mna_option", "rofr_operational_consent_claim"),
        ("license_brand_saturation", "china_exposure", "mna_governance_risk", "overpay_risk", "inventory_markdown_risk"),
        "license_brand_saturation_mna_governance_watch",
        "needs_price_inventory_margin_backfill",
        ("round_176.md Washington Post licensed Korean fashion brands", "round_176.md Reuters F&F TaylorMade acquisition process"),
        "F&F-style license brands need sell-through, inventory, and M&A discipline; logo fatigue and China exposure keep it Watch/Red.",
    ),
    Round176CaseCandidate(
        "channel_stuffing_inventory_overlay_case",
        "CHANNEL_STUFFING_INVENTORY_OVERLAY",
        "K_CONSUMER_EXPORT_BASKET",
        "K-beauty/K-food shipment versus sell-through overlay",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("shipment_growth", "export_growth", "listing_growth", "sell_through_reorder_required"),
        ("inventory_days_up", "receivables_days_up", "sell_through_slowdown", "discount_rate_up"),
        "shipment_without_sell_through_4c_gate",
        "not_price_applicable_overlay",
        ("round_176.md channel stuffing and receivables risk",),
        "Consumer export Stage 3 requires sell-through and reorder, not shipment alone.",
    ),
    Round176CaseCandidate(
        "kfood_single_sku_viral_risk_case",
        "K_FOOD_SINGLE_SKU_RISK",
        "K_FOOD_SKU_BASKET",
        "K-food single viral SKU risk",
        "KR",
        "event_premium",
        None,
        None,
        None,
        None,
        None,
        ("single_viral_sku", "retail_listing", "premium_sku_narrative"),
        ("single_sku_dependency", "portfolio_missing", "reorder_missing", "food_safety_or_recall_risk"),
        "single_sku_stage2_cap",
        "not_price_applicable_overlay",
        ("round_176.md K-food single SKU risk note",),
        "A single viral SKU can reach Stage 1/2 but cannot create Green without portfolio repeat demand and OP/EPS support.",
    ),
)


ROUND176_SCORE_STAGE_PRICE_ALIGNMENT: tuple[Round176ScoreStagePriceAlignment, ...] = (
    Round176ScoreStagePriceAlignment("silicon2_kbeauty_distribution_stage3_candidate", "Stage 2/3 candidate", "K-beauty import/e-commerce evidence strong; KRX and working capital path need backfill", "portfolio_distribution_not_brand_keyword", "credit portfolio distribution and US channel; cap before sell-through, inventory, receivables, OPM, FCF"),
    Round176ScoreStagePriceAlignment("dalba_global_ipo_4b_watch_case", "Stage 2 + 4B-watch", "Post-listing price more than doubled before sell-through proof", "ipo_double_requires_4b_watch", "credit US channel talks; apply IPO valuation and single-brand risk"),
    Round176ScoreStagePriceAlignment("cj_oliveyoung_platform_holdco_cap_case", "Stage 2 option", "Strong private platform but CJ cash-flow/NAV link needs proof", "holdco_link_cap", "credit platform; cap before IPO/cash realization or consolidated OP/FCF link"),
    Round176ScoreStagePriceAlignment("nongshim_global_staple_stage2_case", "Stage 2/3 candidate", "Global staple evidence strong; OP/EPS and KRX path need backfill", "staple_export_candidate", "credit overseas mix and mainstream shelf; cap before OP/EPS and inventory proof"),
    Round176ScoreStagePriceAlignment("kbeauty_oem_odm_supplychain_stage3_candidate", "Stage 2/3 candidate", "OEM/ODM can catch multi-brand repeat demand before single brands", "repeat_order_supplychain_candidate", "credit customer diversification; cap before receivables and OPM proof"),
    Round176ScoreStagePriceAlignment("drg_kbeauty_mna_stage2_reference_case", "Stage 2 reference", "Private M&A validates strategic value, not direct listed-company Green", "reference_not_direct_green", "support sector evidence only; require listed revenue/OPM link"),
    Round176ScoreStagePriceAlignment("amorepacific_china_exposure_4c_case", "4C-watch", "China demand weakness and earnings miss override K-beauty narrative", "china_exposure_4c_alignment", "apply China premium exposure and earnings miss gate"),
    Round176ScoreStagePriceAlignment("kbeauty_tariff_import_margin_review_case", "RedTeam overlay", "US import growth positive but tariff can pressure margin and reorder", "tariff_margin_gate", "require margin buffer and price pass-through"),
    Round176ScoreStagePriceAlignment("fnf_license_brand_china_mna_watch_case", "Watch/Red", "License brand saturation and TaylorMade M&A governance risk cap rerating", "license_brand_governance_risk", "require sell-through, inventory, and M&A discipline"),
    Round176ScoreStagePriceAlignment("channel_stuffing_inventory_overlay_case", "hard gate", "Shipment growth can hide sell-through weakness", "sell_through_inventory_gate", "require inventory days, receivables days, reorder, and margin quality"),
)


ROUND176_PRICE_FIELDS: tuple[str, ...] = (
    "ticker",
    "symbol",
    "company_name",
    "primary_archetype",
    "secondary_archetypes",
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
    "stage1_price",
    "stage2_price",
    "stage3_price",
    "stage4b_price",
    "stage4c_price",
    "return_20d_after_stage2",
    "return_60d_after_stage2",
    "return_120d_after_stage2",
    "return_252d_after_stage2",
    "mfe_60d_after_stage2",
    "mae_60d_after_stage2",
    "mfe_120d_after_stage2",
    "mae_120d_after_stage2",
    "mfe_252d_after_stage2",
    "mae_252d_after_stage2",
    "relative_strength_vs_kospi",
    "relative_strength_vs_kosdaq",
    "relative_strength_vs_consumer_basket",
    "relative_strength_vs_kbeauty_basket",
    "export_growth_yoy",
    "us_sales_growth_yoy",
    "japan_sales_growth_yoy",
    "europe_sales_growth_yoy",
    "channel_added",
    "channel_type",
    "amazon_sales_signal",
    "tiktok_sales_signal",
    "ulta_sephora_costco_target_signal",
    "offline_sell_through_signal",
    "reorder_signal",
    "op_revision_before_stage3",
    "op_revision_after_stage3",
    "eps_revision_before_stage3",
    "eps_revision_after_stage3",
    "inventory_days",
    "inventory_days_change",
    "receivables_days",
    "receivables_days_change",
    "gross_margin",
    "opm",
    "discount_rate_signal",
    "tariff_exposure",
    "china_exposure",
    "single_sku_dependency",
    "ipo_or_listing_date",
    "post_listing_return",
    "holdco_cashflow_link",
    "nav_discount_signal",
    "mna_option_or_price",
    "disclosure_confidence",
    "opendart_rcept_no",
    "opendart_detail_fetched_flag",
    "detail_parser_confidence",
    "valuation_at_stage3",
    "valuation_at_stage4b",
    "stage_before_redteam",
    "stage_after_redteam",
    "score_before_redteam",
    "score_after_redteam",
    "score_price_alignment",
    "price_validation_status",
    "review_notes",
)


def round176_target_for(target_id: str) -> Round176ScoreTarget | None:
    for target in ROUND176_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round176_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND176_CASE_CANDIDATES:
        target = round176_target_for(candidate.target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {candidate.target_id}")
        weights = target.score_weight.as_dict()
        stage4b_evidence = candidate.evidence_fields if candidate.case_type in {"4b_watch", "overheat"} or candidate.stage4b_date else ()
        stage4c_evidence = candidate.red_flag_fields if candidate.case_type == "4c_thesis_break" or candidate.stage4c_date or target.hard_gate else ()
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
                f"Round176 R5 Loop-11 Korea consumer/retail/brand case for {candidate.target_id}; "
                "calibration-only and focused on export/channel proof, sell-through, reorder, working-capital quality, plus 4B/4C cooling."
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
            score_price_alignment=_round176_score_price_alignment(candidate),
            rerating_result=_round176_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
            score_weight_hint={
                "eps_fcf": _numeric_weight(weights["eps_fcf_opm"]),
                "export_channel_visibility": _numeric_weight(weights["export_channel_visibility"]),
                "sell_through_reorder": _numeric_weight(weights["sell_through_reorder"]),
                "inventory_receivables_margin_quality": _numeric_weight(weights["inventory_receivables_margin_quality"]),
                "early_price_validation": _numeric_weight(weights["early_price_validation"]),
                "safety_tariff_disclosure": _numeric_weight(weights["safety_tariff_disclosure"]),
                "valuation_4b_room": _numeric_weight(weights["valuation_4b_room"]),
            },
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "brand_awareness_or_listing_is_not_structural_evidence",
                "require_export_channel_sellthrough_reorder_inventory_receivables_opm_fcf_for_green",
                "stage3_early_catch_requires_4_of_7_loop11_conditions",
                "stage4b_cooling_requires_3_of_5_loop11_conditions",
                "do_not_invent_channel_sellthrough_reorder_inventory_receivables_margin_stage_prices_or_mfe_mae",
                "viral_brand_ipo_listing_tiktok_amazon_oliveyoung_and_single_sku_do_not_create_green",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=False,
                price_data_available=False,
                stage_dates_confidence=0.75
                if candidate.stage1_date or candidate.stage2_date or candidate.stage3_date or candidate.stage4b_date or candidate.stage4c_date
                else 0.2,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round176_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND176_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "eps_fcf_opm": str(weights["eps_fcf_opm"]),
                "export_channel_visibility": str(weights["export_channel_visibility"]),
                "sell_through_reorder": str(weights["sell_through_reorder"]),
                "inventory_receivables_margin_quality": str(weights["inventory_receivables_margin_quality"]),
                "early_price_validation": str(weights["early_price_validation"]),
                "safety_tariff_disclosure": str(weights["safety_tariff_disclosure"]),
                "valuation_4b_room": str(weights["valuation_4b_room"]),
                "stage1_signals": "|".join(target.stage1_signals),
                "stage2_signals": "|".join(target.stage2_signals),
                "stage3_conditions": "|".join(target.stage3_conditions),
                "stage4b_conditions": "|".join(target.stage4b_conditions),
                "stage4c_conditions": "|".join(target.stage4c_conditions),
                "green_conditions": "|".join(target.green_conditions),
                "red_flags": "|".join(target.red_flags),
                "loop11_penalty_axes": "|".join(target.loop11_penalty_axes),
                "hard_gate": str(target.hard_gate).lower(),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round176_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND176_CASE_CANDIDATES:
        target = round176_target_for(candidate.target_id)
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


def round176_stage_date_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "target_id": target.target_id,
            "stage1": "|".join(target.stage1_signals),
            "stage2": "|".join(target.stage2_signals),
            "stage3": "|".join(target.stage3_conditions),
            "stage4b": "|".join(target.stage4b_conditions),
            "stage4c": "|".join(target.stage4c_conditions),
            "loop11_penalty_axes": "|".join(target.loop11_penalty_axes),
            "hard_gate": str(target.hard_gate).lower(),
            "production_scoring_changed": "false",
        }
        for target in ROUND176_SCORE_TARGETS
    )


def round176_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round176_backfill": "true"} for field in ROUND176_PRICE_FIELDS)


def round176_base_score_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(weight.as_row() for weight in ROUND176_BASE_SCORE_WEIGHTS)


def round176_stage_cap_rows() -> tuple[dict[str, str], ...]:
    return tuple(cap.as_row() for cap in ROUND176_STAGE_CAPS)


def round176_score_stage_price_alignment_rows() -> tuple[dict[str, str], ...]:
    return tuple(row.as_row() for row in ROUND176_SCORE_STAGE_PRICE_ALIGNMENT)


def round176_summary() -> dict[str, int | bool]:
    records = round176_case_records()
    return {
        "target_count": len(ROUND176_SCORE_TARGETS),
        "source_canonical_target_count": ROUND176_SOURCE_CANONICAL_TARGET_COUNT,
        "case_candidate_count": len(records),
        "base_score_component_count": len(ROUND176_BASE_SCORE_WEIGHTS),
        "stage_cap_count": len(ROUND176_STAGE_CAPS),
        "score_stage_price_alignment_count": len(ROUND176_SCORE_STAGE_PRICE_ALIGNMENT),
        "structural_success_count": sum(1 for record in records if record.case_type == "structural_success"),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND176_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND176_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND176_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "hard_gate_target_count": sum(1 for target in ROUND176_SCORE_TARGETS if target.hard_gate),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round176_r5_loop11_reports(
    *,
    output_directory: str | Path = ROUND176_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND176_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND176_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round176_r5_loop11_consumer_retail_brand_summary.md",
        "case_matrix": output / "round176_r5_loop11_case_matrix.csv",
        "stage_date_plan": output / "round176_r5_loop11_stage_date_plan.csv",
        "green_guardrails": output / "round176_r5_loop11_green_guardrails.md",
        "risk_overlays": output / "round176_r5_loop11_risk_overlays.md",
        "price_validation_plan": output / "round176_r5_loop11_price_validation_plan.md",
        "price_fields": output / "round176_r5_loop11_price_fields.csv",
        "base_score_weights": output / "round176_r5_loop11_base_score_weights.csv",
        "stage_caps": output / "round176_r5_loop11_stage_caps.csv",
        "score_stage_price_alignment": output / "round176_r5_loop11_score_stage_price_alignment.csv",
        "score_stage_price_alignment_md": output / "round176_r5_loop11_score_stage_price_alignment.md",
    }
    _write_case_jsonl(round176_case_records(), cases)
    _write_rows(round176_score_profile_rows(), score_profiles)
    _write_rows(round176_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round176_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round176_price_field_rows(), paths["price_fields"])
    _write_rows(round176_base_score_weight_rows(), paths["base_score_weights"])
    _write_rows(round176_stage_cap_rows(), paths["stage_caps"])
    _write_rows(round176_score_stage_price_alignment_rows(), paths["score_stage_price_alignment"])
    paths["summary"].write_text(render_round176_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round176_green_guardrail_markdown(), encoding="utf-8")
    paths["risk_overlays"].write_text(render_round176_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round176_price_validation_plan_markdown(), encoding="utf-8")
    paths["score_stage_price_alignment_md"].write_text(render_round176_score_stage_price_alignment_markdown(), encoding="utf-8")
    return paths


def render_round176_summary_markdown() -> str:
    summary = round176_summary()
    lines = [
        "# Round-176 R5 Loop-11 Korea Consumer / Retail / Brand Summary",
        "",
        f"- source_round: `{ROUND176_SOURCE_ROUND_PATH}`",
        "- large_sector: `CONSUMER_RETAIL_BRAND`",
        "- loop: `R5 Loop 11 / v11.0`",
        f"- target_count: {summary['target_count']}",
        f"- source_canonical_target_count: {summary['source_canonical_target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- base_score_component_count: {summary['base_score_component_count']}",
        f"- stage_cap_count: {summary['stage_cap_count']}",
        f"- score_stage_price_alignment_count: {summary['score_stage_price_alignment_count']}",
        f"- structural_success_count: {summary['structural_success_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- failed_rerating_count: {summary['failed_rerating_count']}",
        f"- stage4b_case_count: {summary['stage4b_case_count']}",
        f"- stage4c_case_count: {summary['stage4c_case_count']}",
        f"- green_possible_count: {summary['green_possible_count']}",
        f"- watch_yellow_first_count: {summary['watch_yellow_first_count']}",
        f"- redteam_first_count: {summary['redteam_first_count']}",
        f"- hard_gate_target_count: {summary['hard_gate_target_count']}",
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "",
        "- R5 Loop 11 is Korea-first and treats K-food/K-beauty names, TikTok, Amazon, Olive Young, and US listing news as routing evidence before sell-through proof.",
        "- Stage 3-Green remains strict. Export/channel growth must convert into reorder, OPM, FCF, inventory/receivables quality, and early price-path validation.",
        "- The base score weights are EPS/FCF/OPM 23, export/channel visibility 21, sell-through/reorder 18, inventory/receivables/margin quality 12, early price path 10, safety/tariff/disclosure 8, valuation/4B room 8.",
        "- Example: Silicon2 can be a Stage 2/3 candidate as a portfolio distributor, but sell-through and working capital cap Green.",
        "- Example: D'Alba has strong US channel visibility, but post-listing doubling requires 4B-watch.",
        "- Example: CJ/Olive Young is a strong platform option, but CJ needs cash-flow, IPO, or NAV transmission.",
        "- Example: Amorepacific proves K-beauty with China premium exposure can be hard 4C despite sector strength.",
    ]
    return "\n".join(lines) + "\n"


def render_round176_green_guardrail_markdown() -> str:
    lines = [
        "# Round-176 R5 Loop-11 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Loop-11 penalties |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND176_SCORE_TARGETS:
        lines.append(
            "| "
            f"`{target.target_id}` | {target.posture.value} | "
            f"{', '.join(target.green_conditions)} | {', '.join(target.loop11_penalty_axes)} |"
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not apply R5 Loop-11 v11.0 weights to production scoring yet.",
            "- Do not lower Stage 3-Green thresholds because a K-food or K-beauty stock moved.",
            "- Do not use Round 176 case records as candidate-generation input.",
            "- Do not treat K-food, K-beauty, US listing, TikTok viral, Olive Young, Amazon, or brand awareness as Green by itself.",
            "- Do not invent channel, sell-through, reorder, inventory days, receivables days, OPM, FCF, tariff absorption, stage prices, or MFE/MAE.",
            "- Apply 4B-watch when IPO, viral brand, K-beauty/K-food narrative, or listing news outruns OP/EPS and sell-through.",
            "- Apply 4C/hard review for China premium demand weakness, tariff margin hit, channel stuffing, inventory/receivables spike, recall/safety issue, customer churn, license-brand saturation, or M&A overpay.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round176_risk_overlay_markdown() -> str:
    lines = [
        "# Round-176 R5 Loop-11 Risk Overlays",
        "",
        "- `SELL_THROUGH_REQUIRED`: export, shipment, GMV, or listing growth is capped before sell-through and reorder.",
        "- `WORKING_CAPITAL_QUALITY_GATE`: inventory days, receivables days, gross margin, and OPM decide whether growth is real.",
        "- `IPO_BRAND_4B`: newly listed or viral brands that double quickly require 4B-watch before sell-through proof.",
        "- `HOLDCO_LINK_CAP`: a strong private platform cannot create listed-parent Green without cash-flow, IPO, or NAV transmission.",
        "- `CHINA_CONSUMER_4C`: premium beauty or apparel with China exposure can be hard 4C despite global K-beauty/K-brand strength.",
        "- `TARIFF_MARGIN_GATE`: US tariff risk caps Stage 3 unless margin buffer and price pass-through are proven.",
        "- `SINGLE_SKU_CAP`: one viral SKU can route research but cannot create Green without portfolio repeat demand.",
        "- `DISCLOSURE_CONFIDENCE_CAPPED`: consumer headlines are capped until channel, reorder, inventory, and margin details are verified.",
        "",
        "Simple example: if `as_of_date=2025-06-05`, D'Alba's US channel talks can be Stage 2 evidence. A later sell-through result cannot be used unless it was available by that date.",
    ]
    return "\n".join(lines) + "\n"


def render_round176_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-176 R5 Loop-11 Price Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign Stage 1/2/3/4B/4C dates from dated source evidence only.",
        "2. Backfill KRX daily bars for `price_at_stage1` through `price_at_stage4c`.",
        "3. Calculate 20D/60D/120D/252D returns and MFE/MAE after Stage 2.",
        "4. Compare price speed against OP/EPS revision, sell-through, reorder, inventory, receivables, margin, tariff, and China exposure.",
        "5. Separate distribution/platform/OEM Stage 2 evidence from brand-viral 4B-watch and China/tariff/working-capital 4C-watch.",
        "6. Keep IPO, private-platform, tariff, single-SKU, channel-stuffing, and disclosure-detail caps explicit.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | target | stage marker | check |",
        "| --- | --- | --- | --- |",
    ]
    for row in round176_case_candidate_rows():
        stage_date = row["stage4c_date"] or row["stage4b_date"] or row["stage3_date"] or row["stage2_date"] or row["stage1_date"] or "undated"
        lines.append(f"| `{row['case_id']}` | `{row['target_id']}` | {stage_date} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `portfolio_distribution_not_brand_keyword`: distributor quality needs sell-through and working capital proof.",
            "- `ipo_double_requires_4b_watch`: post-listing doubling is not Green by itself.",
            "- `holdco_link_cap`: private platform value needs listed-parent transmission.",
            "- `staple_export_candidate`: staple food export evidence needs OP/EPS and inventory proof.",
            "- `repeat_order_supplychain_candidate`: OEM/ODM strength needs customer diversification and receivables quality.",
            "- `china_exposure_4c_alignment`: China demand weakness and earnings miss override broad K-beauty narratives.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round176_score_stage_price_alignment_markdown() -> str:
    lines = [
        "# Round-176 R5 Loop-11 Score -> Stage -> Price Alignment",
        "",
        "## Base Score Weights",
        "",
        "| component | points | direction | reason |",
        "| --- | ---: | --- | --- |",
    ]
    for row in ROUND176_BASE_SCORE_WEIGHTS:
        lines.append(f"| `{row.component}` | {row.points} | {row.loop11_direction} | {row.reason} |")
    lines.extend(
        [
            "",
            "## Stage Caps",
            "",
            "| stage band | max score | evidence | examples | Green policy |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for cap in ROUND176_STAGE_CAPS:
        lines.append(
            f"| `{cap.stage_band}` | {cap.max_score} | {', '.join(cap.required_evidence)} | "
            f"{', '.join(cap.example_cases)} | {cap.green_policy} |"
        )
    lines.extend(
        [
            "",
            "## Alignment Cases",
            "",
            "| case | detected stage | price-path status | verdict | adjustment |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in ROUND176_SCORE_STAGE_PRICE_ALIGNMENT:
        lines.append(
            f"| `{row.case_id}` | {row.detected_stage} | {row.price_path_status} | "
            f"{row.verdict} | {row.normalization_adjustment} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Silicon2 is the clean platform-distribution test: portfolio evidence matters, but working capital gates Green.",
            "- D'Alba is the clean IPO/brand 4B test: US channels can be Stage 2 while valuation is cooled.",
            "- CJ/Olive Young is the private-platform-to-listed-parent transmission test.",
            "- Nongshim and K-beauty OEM/ODM test whether repeat demand reaches OP/EPS before crowding.",
            "- Amorepacific, F&F, tariff, and channel-stuffing overlays prevent broad K-beauty/K-food narratives from becoming unsafe Green.",
        ]
    )
    return "\n".join(lines) + "\n"


def _round176_score_price_alignment(candidate: Round176CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "aligned"
    if candidate.case_type == "success_candidate":
        return "unknown"
    if candidate.case_type in {"event_premium", "overheat", "4b_watch"}:
        return "price_moved_without_evidence"
    if candidate.case_type in {"4c_thesis_break", "failed_rerating"}:
        return "false_positive_score"
    return "unknown"


def _round176_rerating_result(candidate: Round176CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "true_rerating"
    if candidate.case_type == "4b_watch" or candidate.case_type == "overheat":
        return "theme_overheat"
    if candidate.case_type == "event_premium":
        return "event_premium"
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    if candidate.case_type == "failed_rerating":
        return "no_rerating"
    return "unknown"


def _numeric_weight(value: int | str) -> float:
    if isinstance(value, int):
        return float(value)
    if value in {"gate", "cap", "+", "event"}:
        return 0.0
    return float(value)


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
        writer = csv.DictWriter(handle, fieldnames=tuple(rows_tuple[0].keys()), lineterminator="\n")
        writer.writeheader()
        for row in rows_tuple:
            writer.writerow(dict(row))
    return path


__all__ = [
    "ROUND176_BASE_SCORE_WEIGHTS",
    "ROUND176_CASE_CANDIDATES",
    "ROUND176_DEFAULT_CASES_PATH",
    "ROUND176_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND176_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND176_PRICE_FIELDS",
    "ROUND176_SCORE_STAGE_PRICE_ALIGNMENT",
    "ROUND176_SCORE_TARGETS",
    "ROUND176_SOURCE_CANONICAL_TARGET_COUNT",
    "ROUND176_SOURCE_CANONICAL_TARGET_IDS",
    "ROUND176_STAGE_CAPS",
    "Round176BaseScoreWeight",
    "Round176CaseCandidate",
    "Round176ScoreStagePriceAlignment",
    "Round176ScoreTarget",
    "Round176ScoreWeightDraft",
    "Round176StageCap",
    "render_round176_green_guardrail_markdown",
    "render_round176_price_validation_plan_markdown",
    "render_round176_risk_overlay_markdown",
    "render_round176_score_stage_price_alignment_markdown",
    "render_round176_summary_markdown",
    "round176_base_score_weight_rows",
    "round176_case_candidate_rows",
    "round176_case_records",
    "round176_price_field_rows",
    "round176_score_profile_rows",
    "round176_score_stage_price_alignment_rows",
    "round176_stage_cap_rows",
    "round176_stage_date_rows",
    "round176_summary",
    "round176_target_for",
    "write_round176_r5_loop11_reports",
]
