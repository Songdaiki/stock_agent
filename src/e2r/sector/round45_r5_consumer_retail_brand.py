"""Round-45 R5 consumer, retail, and brand calibration pack.

Round 45 expands the Round-40 protocol for consumer, retail, and brand
themes. It stores target sub-archetypes, shadow score-weight drafts,
stage-date guidance, case candidates, and price-validation fields.

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


ROUND45_SOURCE_ROUND_PATH = "docs/round/round_45.md"
ROUND45_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round45_r5_consumer_retail_brand"
ROUND45_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r5_round45.jsonl"
ROUND45_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round45_r5_v1.csv"


@dataclass(frozen=True)
class Round45ScoreWeightDraft:
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
class Round45ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round45ScoreWeightDraft
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
        return Round10LargeSector.CONSUMER_RETAIL_BRAND

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round45CaseCandidate:
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


ROUND45_SCORE_TARGETS: tuple[Round45ScoreTarget, ...] = (
    Round45ScoreTarget(
        "EXPORT_RECURRING_CONSUMER",
        E2RArchetype.EXPORT_RECURRING_CONSUMER,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round45ScoreWeightDraft(22, 23, 12, 16, 13, 0, 5),
        ("export_growth", "k_food_or_ramen_viral", "capa_expansion", "overseas_channel_news"),
        ("asp_increase", "us_europe_shipments", "op_eps_revision", "target_price_revision"),
        ("repeat_order", "overseas_channel_scale", "opm_improvement", "fy1_fy2_eps_revision"),
        ("k_food_rerating_crowded", "single_product_story_overpriced", "capacity_expansion_priced"),
        ("recall", "food_safety_ban", "inventory_build", "channel_stuffing", "single_product_demand_slowdown"),
        ("export_growth", "recurring_demand", "channel_expansion", "op_eps_revision", "inventory_stable"),
        ("single_product_dependency", "recall", "inventory_build", "channel_stuffing"),
        "K-food Green needs export, repeat demand, channel expansion, OPM, and revision support together.",
    ),
    Round45ScoreTarget(
        "FOOD_AGRI_LIVESTOCK_CYCLE",
        E2RArchetype.FOOD_AGRI_LIVESTOCK_CYCLE,
        Round10ThemePosture.REDTEAM_FIRST,
        Round45ScoreWeightDraft(18, 10, 14, 8, 8, 0, 5),
        ("feed_cost_change", "disease_or_weather_event", "food_commodity_price"),
        ("price_pass_through", "cost_relief", "inventory_status"),
        ("repeat_margin", "fcf_margin", "commodity_cycle_controlled"),
        ("commodity_food_event_crowded",),
        ("feed_cost_reversal", "disease_normalization", "inventory_loss", "one_off_price_spike"),
        ("repeat_margin", "cost_pass_through", "fcf_margin"),
        ("one_off_price", "commodity_reversal", "inventory_loss"),
        "Food/agri/livestock stays cycle-capped; cost and disease events are not structural evidence by themselves.",
    ),
    Round45ScoreTarget(
        "RETAIL_CONVENIENCE_OFFLINE",
        E2RArchetype.RETAIL_CONVENIENCE_OFFLINE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round45ScoreWeightDraft(18, 16, 5, 13, 14, 3, 5),
        ("store_expansion", "pb_product_mix", "same_store_sales_recovery"),
        ("store_profitability", "opm_improvement", "overseas_store_profitability"),
        ("defensive_recurring_sales", "pb_mix", "fcf_stability", "valuation_frame_improves"),
        ("store_count_story_crowded", "defensive_retail_premium_full"),
        ("same_store_sales_slowdown", "rent_labor_cost_pressure", "store_density_competition"),
        ("same_store_sales", "pb_mix", "opm_improvement", "fcf_stability"),
        ("store_count_only", "labor_cost_pressure", "rent_pressure", "store_density"),
        "Convenience retail can move Watch-to-Green only when store efficiency, not store count, drives OPM and FCF.",
    ),
    Round45ScoreTarget(
        "RETAIL_ECOMMERCE_LOGISTICS",
        E2RArchetype.RETAIL_ECOMMERCE_LOGISTICS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round45ScoreWeightDraft(18, 16, 5, 13, 14, 3, 5),
        ("gmv_or_sales_growth", "logistics_network_expansion", "customer_count_growth"),
        ("logistics_cost_stability", "opm_improvement", "fcf_improvement"),
        ("repeat_customers", "cost_leverage", "low_regulatory_risk", "low_data_security_risk"),
        ("scale_narrative_crowded",),
        ("data_breach", "supplier_regulation", "payment_delay", "logistics_cost_increase", "fcf_deterioration"),
        ("repeat_customer_base", "logistics_efficiency", "fcf_improvement", "trust_and_regulation_clean"),
        ("data_breach", "supplier_pressure", "payment_delay", "trust_damage"),
        "E-commerce scale is not Green evidence unless unit economics, FCF, and trust/regulation are clean.",
    ),
    Round45ScoreTarget(
        "ECOMMERCE_FRESH_LOGISTICS",
        E2RArchetype.ECOMMERCE_FRESH_LOGISTICS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round45ScoreWeightDraft(17, 15, 6, 12, 10, 1, 5),
        ("fresh_food_delivery_growth", "cold_chain_expansion", "repeat_order_growth"),
        ("unit_economics_improvement", "waste_rate_control", "delivery_cost_control"),
        ("repeat_order", "cold_chain_efficiency", "op_fcf_turnaround"),
        ("fresh_logistics_growth_story_crowded",),
        ("delivery_cost_increase", "waste_rate_spike", "delayed_profitability", "cash_burn"),
        ("unit_economics", "repeat_orders", "waste_rate_control", "fcf_path"),
        ("cash_burn", "waste_rate", "delivery_cost", "profitability_delay"),
        "Fresh e-commerce must prove unit economics; GMV alone is Stage 1 only.",
    ),
    Round45ScoreTarget(
        "K_BEAUTY_EXPORT_DISTRIBUTION",
        E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round45ScoreWeightDraft(22, 23, 12, 16, 13, 0, 5),
        ("us_japan_export_growth", "k_beauty_viral", "brand_awareness"),
        ("sephora_ulta_target_costco_channel", "offline_channel_entry", "op_eps_revision"),
        ("sell_through", "repeat_orders", "opm_improvement", "china_dependency_down"),
        ("k_beauty_group_overheated", "indie_brand_valuation_surge"),
        ("inventory_build", "receivables_growth", "tariff", "china_channel_slowdown", "us_channel_slowdown"),
        ("export_growth", "channel_diversification", "sell_through", "repeat_orders", "opm_roe_improvement"),
        ("tariff", "china_dependency", "inventory_build", "receivables_growth", "sell_through_failure"),
        "K-beauty Green needs offline sell-through and repeat orders, not just online viral traffic.",
    ),
    Round45ScoreTarget(
        "BEAUTY_OEM_ODM_SUPPLYCHAIN",
        E2RArchetype.BEAUTY_OEM_ODM_SUPPLYCHAIN,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round45ScoreWeightDraft(22, 23, 12, 16, 13, 0, 5),
        ("global_k_beauty_order_growth", "brand_customer_growth"),
        ("customer_diversification", "capacity_utilization", "opm_improvement"),
        ("repeat_orders", "overseas_customer_diversification", "eps_fcf_bodyweight_change"),
        ("beauty_supply_chain_premium_crowded",),
        ("customer_sell_through_slowdown", "inventory_build", "receivables_growth", "customer_concentration"),
        ("customer_diversification", "repeat_orders", "capacity_utilization", "opm_improvement"),
        ("inventory_build", "receivables_growth", "customer_concentration", "sell_through_failure"),
        "Beauty OEM/ODM needs customer diversification and repeat orders; customer inventory risk is a hard gate.",
    ),
    Round45ScoreTarget(
        "APPAREL_FAST_FASHION_BRAND_OEM",
        E2RArchetype.APPAREL_FAST_FASHION_BRAND_OEM,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round45ScoreWeightDraft(18, 16, 8, 14, 12, 0, 5),
        ("brand_momentum", "fast_fashion_growth", "oem_order_growth"),
        ("order_visibility", "inventory_turnover", "discount_rate_control"),
        ("repeat_orders", "inventory_turnover", "brand_pricing_power", "opm_improvement"),
        ("fashion_brand_hype_crowded",),
        ("ip_litigation", "product_safety_regulation", "supplier_exclusivity_dispute", "inventory_buildup", "discount_rate_up"),
        ("order_visibility", "inventory_turnover", "discount_rate_control", "opm_improvement"),
        ("ip_litigation", "regulatory_enforcement", "unsafe_products", "inventory_buildup", "discounting"),
        "Apparel and fast fashion are Watch because inventory, discounting, IP, and regulation can break the thesis.",
    ),
    Round45ScoreTarget(
        "HOME_LIVING_APPLIANCE_RENTAL",
        E2RArchetype.HOME_LIVING_APPLIANCE_RENTAL,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round45ScoreWeightDraft(17, 15, 6, 12, 10, 2, 5),
        ("rental_accounts_growth", "overseas_accounts_growth", "new_product_launch"),
        ("churn_stable", "filter_service_recurring_revenue", "opm_fcf_improvement"),
        ("recurring_revenue_over_hardware_cycle", "low_churn", "service_margin"),
        ("rental_account_growth_crowded",),
        ("replacement_demand_slowdown", "housing_cycle_down", "dividend_suspension", "quality_recall"),
        ("rental_accounts", "churn_stable", "recurring_service_revenue", "fcf_improvement"),
        ("hardware_cycle", "housing_cycle", "consumer_sentiment", "dividend_cut", "quality_recall"),
        "Home appliance Green needs recurring rental/service economics, not replacement-cycle hardware sales.",
    ),
    Round45ScoreTarget(
        "HOME_CHILD_EDUCATION",
        E2RArchetype.HOME_CHILD_EDUCATION,
        Round10ThemePosture.REDTEAM_FIRST,
        Round45ScoreWeightDraft(16, 12, 5, 10, 8, 0, 5),
        ("kids_product_growth", "education_or_childcare_theme", "household_product_news"),
        ("recurring_demand", "channel_expansion", "opm_improvement"),
        ("subscription_or_repeat_purchase", "policy_risk_low", "fcf_path"),
        ("kids_theme_crowded",),
        ("low_birth_rate_tam_decline", "policy_regulation", "one_off_product_cycle"),
        ("recurring_demand", "channel_expansion", "opm_improvement"),
        ("low_birth_rate", "tam_decline", "policy_regulation"),
        "Kids/home education needs recurring demand and TAM discipline; demographics can cap rerating.",
    ),
    Round45ScoreTarget(
        "CONSUMER_REGULATED_PRODUCT",
        E2RArchetype.CONSUMER_REGULATED_PRODUCT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round45ScoreWeightDraft(18, 14, 8, 12, 10, 0, 5),
        ("regulated_consumer_product_approval", "new_market_access", "policy_change"),
        ("legal_revenue", "distribution_approval", "margin_visibility"),
        ("regulated_market_open", "repeat_revenue", "low_social_backlash"),
        ("regulated_product_theme_crowded",),
        ("license_reversal", "social_backlash", "product_safety_issue", "regulatory_ban"),
        ("legal_revenue", "approval", "repeat_revenue", "margin_visibility"),
        ("regulatory_ban", "social_backlash", "product_safety_issue"),
        "Regulated consumer products stay Watch until approvals translate into legal recurring revenue.",
    ),
)


ROUND45_CASE_CANDIDATES: tuple[Round45CaseCandidate, ...] = (
    Round45CaseCandidate(
        "samyang_buldak_export_rerating_case",
        "EXPORT_RECURRING_CONSUMER",
        "003230",
        "Samyang Foods Buldak export rerating",
        "KR",
        "success_candidate",
        None,
        date(2024, 6, 14),
        None,
        None,
        None,
        ("buldak_export_growth", "us_europe_shipments", "asp_increase", "capa_expansion", "op_estimate_revision", "target_price_revision"),
        ("single_product_dependency", "recall", "overseas_inventory", "channel_stuffing"),
        "aligned_candidate",
        "needs_price_backfill",
        ("MarketWatch Samyang Foods Q2 earnings market talk",),
        "K-food reference where export, ASP, CAPA, OP estimate revision, target revision, and price reaction moved together.",
    ),
    Round45CaseCandidate(
        "samyang_buldak_recall_risk_case",
        "EXPORT_RECURRING_CONSUMER",
        "003230_RECALL_REF",
        "Samyang Buldak food-safety recall risk",
        "KR",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2024, 6, 12),
        ("buldak_global_product",),
        ("recall", "food_safety_ban", "country_specific_regulation", "single_product_dependency"),
        "food_safety_4c_watch",
        "needs_price_backfill",
        ("Time Denmark Samyang spicy noodle recall",),
        "Successful K-food candidates still need recall, food-safety, and country-regulation guardrails.",
    ),
    Round45CaseCandidate(
        "kbeauty_us_offline_channel_case",
        "K_BEAUTY_EXPORT_DISTRIBUTION",
        "K_BEAUTY_US_CHANNEL_REF",
        "K-beauty US offline channel expansion",
        "KR",
        "success_candidate",
        None,
        date(2025, 6, 5),
        None,
        None,
        None,
        ("us_cosmetics_export_growth", "sephora_ulta_target_costco_channel", "offline_channel_entry", "sell_through_to_verify"),
        ("tariff", "china_channel_slowdown", "inventory_build", "receivables_growth"),
        "structural_success_candidate",
        "missing_direct_symbol_mapping",
        ("Reuters K-beauty US demand",),
        "K-beauty moves beyond viral only when offline channel sell-through and repeat orders are verified.",
    ),
    Round45CaseCandidate(
        "apr_medicube_device_export_case",
        "K_BEAUTY_EXPORT_DISTRIBUTION",
        "278470",
        "APR Medicube device and export rerating",
        "KR",
        "4b_watch",
        None,
        None,
        None,
        None,
        None,
        ("overseas_sales_ratio", "skincare_device_success", "social_commerce", "brand_rerating"),
        ("valuation_saturation", "celebrity_tiktok_demand", "competition", "tariff", "regulation"),
        "aligned_success_candidate_plus_4b_watch",
        "needs_source_date_and_price_backfill",
        ("Financial Times APR Medicube skincare device",),
        "APR is a success candidate but the round document only gives a broad 2025 early-to-Q2 window, so stage dates remain unfilled.",
    ),
    Round45CaseCandidate(
        "cu_gs25_store_efficiency_case",
        "RETAIL_CONVENIENCE_OFFLINE",
        "CONV_STORE_REF",
        "CU / GS25 store efficiency reference",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("store_count", "same_store_sales_to_verify", "pb_mix_to_verify", "store_profitability_to_verify"),
        ("store_count_only", "labor_cost", "rent_pressure", "store_density_competition"),
        "watch_to_green_reference",
        "needs_source_date_and_price_backfill",
        ("Wikipedia CU store",),
        "Store count is routing context only; store efficiency, PB mix, and OPM must be verified before higher stages.",
    ),
    Round45CaseCandidate(
        "coupang_supplier_regulation_case",
        "RETAIL_ECOMMERCE_LOGISTICS",
        "CPNG",
        "Coupang supplier pressure and payment delay regulation",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2026, 2, 26),
        ("ecommerce_scale",),
        ("supplier_pressure", "payment_delay", "retail_law_violation", "margin_sustainability_doubt"),
        "regulatory_4c_watch",
        "needs_price_backfill",
        ("Reuters Coupang supplier fine",),
        "E-commerce margin improvement must be separated from supplier pressure and regulatory risk.",
    ),
    Round45CaseCandidate(
        "coupang_data_breach_case",
        "RETAIL_ECOMMERCE_LOGISTICS",
        "CPNG",
        "Coupang data breach",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        None,
        ("ecommerce_customer_base",),
        ("data_breach", "regulatory_investigation", "customer_trust_damage", "governance_risk"),
        "data_security_4c",
        "needs_source_date_and_price_backfill",
        ("Barrons Coupang data breach", "Reuters Coupang data breach follow-up"),
        "The document provides a 2025-12 month but no day, so the 4C date is intentionally left null.",
    ),
    Round45CaseCandidate(
        "coway_rental_recurring_case",
        "HOME_LIVING_APPLIANCE_RENTAL",
        "021240",
        "Coway rental and service recurring model",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("rental_accounts", "filter_service_recurring_revenue", "overseas_subsidiaries", "churn_to_verify"),
        ("hardware_cycle", "replacement_demand_slowdown", "consumer_sentiment"),
        "recurring_revenue_watch_candidate",
        "needs_source_date_and_price_backfill",
        ("Wikipedia Coway company",),
        "Coway is a Watch-to-Green reference only if rental accounts, churn, service revenue, OPM, and FCF are verified.",
    ),
    Round45CaseCandidate(
        "whirlpool_hardware_cycle_4c_case",
        "HOME_LIVING_APPLIANCE_RENTAL",
        "WHR",
        "Whirlpool hardware replacement-cycle failure",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2026, 5, 7),
        ("home_appliance_hardware_cycle",),
        ("replacement_demand_collapse", "housing_turnover_slowdown", "dividend_suspension", "debt_reduction_pressure"),
        "hardware_cycle_4c",
        "needs_price_backfill",
        ("Reuters Whirlpool dividend suspension",),
        "Hardware replacement demand is not recurring rental economics; dividend suspension and demand collapse are hard RedTeam evidence.",
    ),
    Round45CaseCandidate(
        "shein_temu_ip_regulatory_case",
        "APPAREL_FAST_FASHION_BRAND_OEM",
        "SHEIN_TEMU_REF",
        "Shein / Temu IP and regulatory risk",
        "GLOBAL",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2026, 5, 11),
        ("fast_fashion_growth",),
        ("copyright_litigation", "supplier_exclusivity_dispute", "unsafe_product_regulation", "eu_enforcement"),
        "legal_regulatory_4c_watch",
        "missing_direct_symbol_mapping",
        ("Reuters Shein Temu copyright battle", "Financial Times France Shein Temu enforcement",),
        "Fast-fashion growth needs inventory and legal/regulatory guardrails before any high-conviction label.",
    ),
)


ROUND45_PRICE_FIELDS: tuple[str, ...] = (
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
    "export_sales_growth",
    "overseas_sales_ratio",
    "asp_change",
    "same_store_sales_growth",
    "pb_mix_ratio",
    "op_margin_change",
    "eps_revision_1q",
    "eps_revision_1y",
    "fcf_margin",
    "inventory_growth",
    "receivables_growth",
    "channel_sell_through_signal",
    "recall_flag",
    "food_safety_flag",
    "tariff_flag",
    "customer_count",
    "rental_accounts",
    "churn_rate",
    "subscription_revenue_ratio",
    "data_breach_flag",
    "supplier_regulation_flag",
    "ip_litigation_flag",
    "product_safety_flag",
    "score_price_alignment",
    "price_validation_status",
)


def target_for(target_id: str) -> Round45ScoreTarget | None:
    for target in ROUND45_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round45_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND45_CASE_CANDIDATES:
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
                f"Round45 R5 case for {candidate.target_id}; "
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
                "consumer_sales_growth_is_not_structural_evidence_alone",
                "sell_through_and_fcf_required_for_green",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=False,
                price_data_available=False,
                stage_dates_confidence=0.7 if candidate.stage2_date or candidate.stage4c_date else 0.3,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round45_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND45_SCORE_TARGETS:
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


def round45_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND45_CASE_CANDIDATES:
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


def round45_stage_date_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND45_SCORE_TARGETS:
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


def round45_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round45_backfill": "true"} for field in ROUND45_PRICE_FIELDS)


def round45_summary() -> dict[str, int | bool]:
    records = round45_case_records()
    return {
        "target_count": len(ROUND45_SCORE_TARGETS),
        "case_candidate_count": len(records),
        "structural_success_count": sum(1 for record in records if record.case_type == "structural_success"),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for record in records if record.case_type == "cyclical_success"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "overheat_count": sum(1 for record in records if record.case_type == "overheat"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch"),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND45_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND45_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND45_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round45_r5_reports(
    *,
    output_directory: str | Path = ROUND45_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND45_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND45_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round45_r5_consumer_retail_brand_summary.md",
        "case_matrix": output / "round45_r5_case_matrix.csv",
        "stage_date_plan": output / "round45_r5_stage_date_plan.csv",
        "green_guardrails": output / "round45_r5_green_guardrails.md",
        "price_validation_plan": output / "round45_r5_price_validation_plan.md",
        "price_fields": output / "round45_r5_price_fields.csv",
    }
    _write_case_jsonl(round45_case_records(), cases)
    _write_rows(round45_score_profile_rows(), score_profiles)
    _write_rows(round45_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round45_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round45_price_field_rows(), paths["price_fields"])
    paths["summary"].write_text(render_round45_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round45_green_guardrail_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round45_price_validation_plan_markdown(), encoding="utf-8")
    return paths


def render_round45_summary_markdown() -> str:
    summary = round45_summary()
    lines = [
        "# Round-45 R5 Consumer / Retail / Brand Summary",
        "",
        f"- source_round: `{ROUND45_SOURCE_ROUND_PATH}`",
        "- large_sector: `CONSUMER_RETAIL_BRAND`",
        f"- target_count: {summary['target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
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
        "- R5 should separate repeat export/channel rerating from viral, store-count, GMV, and hardware-cycle stories.",
        "- Example: Samyang can route to higher-quality research when export, ASP, CAPA, and OP revision move together.",
        "- Example: Coupang scale is not enough; supplier regulation and data breach are hard RedTeam evidence.",
        "- Example: K-beauty offline channel expansion is promising only after sell-through, repeat orders, inventory, and receivables are checked.",
    ]
    return "\n".join(lines) + "\n"


def render_round45_green_guardrail_markdown() -> str:
    lines = [
        "# Round-45 R5 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Red flags |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND45_SCORE_TARGETS:
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
            "- Do not apply these R5 v1.0 weights to production scoring yet.",
            "- Do not treat viral traffic, GMV, store count, user count, product hype, or listing expectation as score evidence by themselves.",
            "- Do not invent export growth, sell-through, inventory, receivables, churn, rental accounts, OPM, FCF, or price-path fields.",
            "- Do not lower Stage 3-Green for consumer stories. Green requires repeat demand, channel expansion, OPM/FCF, and clean inventory/receivables.",
            "- Treat recall, food safety, supplier regulation, data breach, IP litigation, product safety, and hardware replacement-cycle failure as RedTeam evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round45_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-45 R5 Price Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign stage dates from source evidence only.",
        "2. Store stage-date close prices from official price data.",
        "3. Calculate MFE_30D / 90D / 180D / 1Y / 2Y.",
        "4. Calculate MAE_30D / 90D / 180D / 1Y.",
        "5. Calculate peak price, drawdown after peak, and below-stage3 flag.",
        "6. Compare price paths with export growth, overseas sales, ASP, OPM, inventory, receivables, sell-through, rental accounts, churn, and 4C flags.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | stage candidate | check |",
        "| --- | --- | --- |",
    ]
    priority = {"apr_medicube_device_export_case", "coupang_data_breach_case", "cu_gs25_store_efficiency_case", "coway_rental_recurring_case"}
    for row in round45_case_candidate_rows():
        if row["stage2_date"] or row["stage4b_date"] or row["stage4c_date"] or row["case_id"] in priority:
            stage_date = row["stage2_date"] or row["stage4b_date"] or row["stage4c_date"] or "needs_source_date"
            lines.append(f"| `{row['case_id']}` | {stage_date} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `aligned_candidate`: export, channel, ASP/OPM, revision, and price path move together.",
            "- `viral_price_move`: viral or celebrity-driven price action appears before sell-through and FCF.",
            "- `channel_stuffing_risk`: shipment growth exists but sell-through, inventory, or receivables are unclear.",
            "- `regulatory_thesis_break`: recall, data breach, supplier regulation, IP, product safety, or policy damage appears.",
            "- `hardware_cycle_failure`: appliance replacement demand weakens without rental/service recurring protection.",
            "- `watch_to_green`: repeated revenue exists, but explosive EPS/FCF and price-path evidence still need validation.",
        ]
    )
    return "\n".join(lines) + "\n"


def _score_price_alignment(candidate: Round45CaseCandidate) -> str:
    if "aligned" in candidate.alignment_hint and candidate.case_type in {"structural_success", "success_candidate"}:
        return "aligned"
    if candidate.case_type in {"event_premium", "overheat", "4b_watch"}:
        return "price_moved_without_evidence"
    if candidate.case_type in {"failed_rerating", "4c_thesis_break"}:
        return "false_positive_score"
    return "unknown"


def _rerating_result(candidate: Round45CaseCandidate) -> str:
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
    "ROUND45_CASE_CANDIDATES",
    "ROUND45_DEFAULT_CASES_PATH",
    "ROUND45_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND45_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND45_PRICE_FIELDS",
    "ROUND45_SCORE_TARGETS",
    "ROUND45_SOURCE_ROUND_PATH",
    "Round45CaseCandidate",
    "Round45ScoreTarget",
    "Round45ScoreWeightDraft",
    "render_round45_green_guardrail_markdown",
    "render_round45_price_validation_plan_markdown",
    "render_round45_summary_markdown",
    "round45_case_candidate_rows",
    "round45_case_records",
    "round45_price_field_rows",
    "round45_score_profile_rows",
    "round45_stage_date_rows",
    "round45_summary",
    "target_for",
    "write_round45_r5_reports",
]
