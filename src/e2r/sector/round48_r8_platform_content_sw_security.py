"""Round-48 R8 platform, content, software, and security calibration pack.

Round 48 separates repeat software/content/platform revenue from user-count,
AI-feature, new-title, security-theme, NFT, and metaverse narratives. R8 can be
Green-eligible when ARR, ARPU, OPM, FCF, retention, bookings, ad revenue, or
security renewals are visible. Legal, privacy, copyright, child-safety,
single-IP, operational-trust, and outage risks can quickly turn a growth story
into 4B/4C.

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


ROUND48_SOURCE_ROUND_PATH = "docs/round/round_48.md"
ROUND48_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round48_r8_platform_content_sw_security"
ROUND48_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r8_round48.jsonl"
ROUND48_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round48_r8_v1.csv"


@dataclass(frozen=True)
class Round48ScoreWeightDraft:
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
class Round48ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round48ScoreWeightDraft
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
        return Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round48CaseCandidate:
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


ROUND48_SCORE_TARGETS: tuple[Round48ScoreTarget, ...] = (
    Round48ScoreTarget(
        "PLATFORM_SOFTWARE_INTERNET",
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round48ScoreWeightDraft(18, 18, 7, 15, 13, 1, 5),
        ("portal_or_messenger_growth", "commerce_platform_growth", "ad_platform_recovery"),
        ("arpu_growth", "recurring_revenue", "opm_improvement", "governance_clean"),
        ("platform_monetization", "fcf_conversion", "regulatory_risk_low"),
        ("platform_multiple_crowded", "user_count_story_overpriced"),
        ("privacy_lawsuit", "founder_legal_case", "regulatory_investigation", "trust_damage"),
        ("arpu_growth", "recurring_revenue", "opm_improvement", "fcf_conversion", "governance_clean"),
        ("regulation", "governance", "privacy", "legal_overhang", "trust_damage"),
        "Platform Green needs monetization and trust, not user count alone.",
    ),
    Round48ScoreTarget(
        "CLOUD_AI_SOFTWARE_INFRA",
        E2RArchetype.CLOUD_AI_SOFTWARE_INFRA,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round48ScoreWeightDraft(20, 23, 8, 16, 14, 0, 5),
        ("cloud_erp_transition", "b2b_saas_growth", "ai_workflow_feature"),
        ("arr_growth", "recurring_revenue_ratio", "customer_retention", "opm_improvement"),
        ("customer_lock_in", "fcf_conversion", "net_retention_rate", "valuation_frame_shift"),
        ("ai_saas_narrative_crowded", "valuation_saturation"),
        ("churn_spike", "ai_compute_cost_surge", "opm_decline", "si_revenue_reversion"),
        ("arr_growth", "recurring_revenue_ratio", "net_retention_rate", "opm_improvement", "fcf_conversion"),
        ("churn", "ai_cost", "si_revenue_mix", "customer_concentration", "margin_slowdown"),
        "B2B SaaS can be Green, but only when repeat revenue and margin/FCF are visible.",
    ),
    Round48ScoreTarget(
        "AI_SOFTWARE_APPLICATION",
        E2RArchetype.AI_SOFTWARE_APPLICATION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round48ScoreWeightDraft(19, 18, 9, 15, 13, 0, 5),
        ("ai_application_launch", "enterprise_ai_adoption", "api_usage_growth"),
        ("paid_customer_growth", "api_revenue", "workflow_integration", "gross_margin_visibility"),
        ("repeat_paid_usage", "fcf_conversion", "compute_cost_controlled"),
        ("ai_app_narrative_crowded", "valuation_before_margin_proof"),
        ("compute_cost_spike", "model_dependency", "copyright_lawsuit", "data_privacy_lawsuit"),
        ("paid_usage", "api_revenue", "workflow_integration", "compute_cost_controlled", "fcf_conversion"),
        ("compute_cost", "model_dependency", "copyright", "data_privacy", "free_user_growth_only"),
        "AI software needs paid usage and unit economics, not feature announcements.",
    ),
    Round48ScoreTarget(
        "GENERATIVE_AI_IP_RISK",
        E2RArchetype.GENERATIVE_AI_IP_RISK,
        Round10ThemePosture.REDTEAM_FIRST,
        Round48ScoreWeightDraft(5, 5, 5, 5, 5, 0, 6),
        ("generative_ai_training_data", "content_license", "open_source_dependency"),
        ("licensed_dataset", "rights_cleared_revenue", "enterprise_contract"),
        ("rights_cleared_repeat_revenue", "liability_risk_low"),
        ("genai_ip_story_overheated",),
        ("copyright_lawsuit", "license_gap", "privacy_lawsuit", "opensource_supply_chain_risk"),
        ("licensed_data", "rights_cleared_revenue", "enterprise_contract", "liability_risk_low"),
        ("copyright", "license_risk", "privacy", "open_source_supply_chain"),
        "Generative AI IP is a RedTeam overlay; rights and revenue must be proven.",
    ),
    Round48ScoreTarget(
        "CONTACT_CENTER_AI_AUTOMATION",
        E2RArchetype.CONTACT_CENTER_AI_AUTOMATION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round48ScoreWeightDraft(19, 20, 8, 14, 13, 0, 5),
        ("ccaas_ai_agent_assist", "contact_center_automation", "seat_expansion"),
        ("enterprise_contract", "seat_expansion", "retention_rate", "opm_improvement"),
        ("workflow_embedded", "low_churn", "enterprise_retention", "fcf_conversion"),
        ("contact_center_ai_crowded",),
        ("churn_spike", "it_budget_cut", "privacy_event", "automation_roi_failure"),
        ("enterprise_contract", "seat_expansion", "low_churn", "retention_rate", "opm_improvement"),
        ("churn", "it_budget_cut", "privacy", "roi_failure"),
        "Contact-center AI needs enterprise retention and workflow economics.",
    ),
    Round48ScoreTarget(
        "SERVICE_KIOSK_SELF_CHECKOUT",
        E2RArchetype.SERVICE_KIOSK_SELF_CHECKOUT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round48ScoreWeightDraft(17, 15, 7, 12, 10, 0, 5),
        ("kiosk_installation", "self_checkout_rollout", "unmanned_store_theme"),
        ("maintenance_revenue", "payment_fee_revenue", "store_roi"),
        ("recurring_maintenance", "low_theft", "customer_acceptance", "fcf_visibility"),
        ("kiosk_theme_crowded",),
        ("theft_rate_up", "customer_complaint", "hardware_one_off", "regulatory_restriction"),
        ("maintenance_revenue", "payment_fee_revenue", "store_roi", "customer_acceptance"),
        ("theft", "customer_complaint", "hardware_one_off", "regulation"),
        "Kiosk themes need recurring maintenance/payment economics, not hardware installation counts.",
    ),
    Round48ScoreTarget(
        "GAME_CONTENT_IP",
        E2RArchetype.GAME_CONTENT_IP,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round48ScoreWeightDraft(20, 18, 6, 14, 12, 0, 5),
        ("new_title_announcement", "ip_expansion", "user_growth", "platform_growth"),
        ("bookings_growth", "sell_through", "live_service_monetization", "op_eps_revision"),
        ("repeat_ip_portfolio", "global_monetization", "single_ip_risk_low"),
        ("single_ip_valuation_crowded", "launch_expectations_saturated"),
        ("game_delay", "bookings_cut", "child_safety_regulation", "user_growth_slowdown"),
        ("bookings_growth", "sell_through", "live_service_monetization", "repeat_ip_portfolio"),
        ("single_ip", "game_delay", "child_safety", "regulatory_ban", "bookings_cut"),
        "Game IP is Watch unless bookings and repeat monetization are proven.",
    ),
    Round48ScoreTarget(
        "MEDIA_AD_CONTENT_CYCLE",
        E2RArchetype.MEDIA_AD_CONTENT_CYCLE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round48ScoreWeightDraft(18, 16, 6, 14, 12, 0, 5),
        ("ad_market_recovery", "ctv_growth", "digital_ad_rebound"),
        ("ad_revenue_growth", "ad_arpu", "opm_improvement"),
        ("repeat_platform_ad_revenue", "budget_resilience", "hybrid_ad_subscription_model"),
        ("adtech_valuation_crowded", "growth_expectations_saturated"),
        ("client_budget_cut", "revenue_miss", "privacy_lawsuit", "scam_ad_regulation", "ai_disintermediation"),
        ("ad_revenue_growth", "ad_arpu", "opm_improvement", "budget_resilience"),
        ("ad_cycle", "client_budget_cut", "privacy", "scam_ads", "ai_disintermediation"),
        "Ad platforms need repeat revenue and budget resilience; ad-cycle rebounds stay capped.",
    ),
    Round48ScoreTarget(
        "STREAMING_AD_PLATFORM",
        E2RArchetype.STREAMING_AD_PLATFORM,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round48ScoreWeightDraft(19, 20, 8, 14, 13, 0, 5),
        ("ad_tier_user_growth", "streaming_ad_inventory", "ctv_ad_platform"),
        ("ad_tier_users", "ad_revenue_growth", "ad_arpu", "own_ad_tech"),
        ("subscription_ad_hybrid", "arpu_expansion", "privacy_risk_low", "fcf_support"),
        ("streaming_ad_multiple_crowded", "ad_tier_growth_fully_priced"),
        ("privacy_lawsuit", "ad_arpu_saturation", "ad_load_pressure", "subscriber_churn"),
        ("ad_tier_users", "ad_revenue_growth", "ad_arpu", "privacy_risk_low"),
        ("privacy", "ad_arpu_saturation", "ad_load", "subscriber_churn"),
        "Streaming ad platforms can improve, but privacy and ad ARPU are hard gates.",
    ),
    Round48ScoreTarget(
        "SECURITY_IDENTITY_DEEPFAKE",
        E2RArchetype.SECURITY_IDENTITY_DEEPFAKE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round48ScoreWeightDraft(20, 20, 10, 14, 13, 0, 5),
        ("cybersecurity_demand", "identity_threat", "deepfake_regulation"),
        ("arr_growth", "customer_diversification", "low_churn", "opm_improvement"),
        ("security_platform_lock_in", "renewal_strength", "operational_trust_intact"),
        ("security_valuation_crowded", "incident_risk_ignored"),
        ("global_outage", "customer_lawsuit", "renewal_risk", "trust_damage"),
        ("arr_growth", "low_churn", "renewal_rate", "customer_diversification", "operational_trust_intact"),
        ("outage", "lawsuit", "renewal_risk", "trust_damage", "gross_negligence_claim"),
        "Security Green requires operational trust; one outage can become hard 4C.",
    ),
    Round48ScoreTarget(
        "METAVERSE_NFT_THEME",
        E2RArchetype.METAVERSE_NFT_THEME,
        Round10ThemePosture.REDTEAM_FIRST,
        Round48ScoreWeightDraft(5, 5, 5, 6, 5, 0, 3),
        ("nft_metaverse_headline", "virtual_asset_content", "token_price_rally"),
        ("platform_fee_revenue", "repeat_transaction_volume", "legal_revenue"),
        ("repeat_platform_revenue", "liquidity_stable", "regulatory_risk_low"),
        ("token_price_only_rally", "nft_theme_crowded"),
        ("no_recurring_revenue", "liquidity_collapse", "regulatory_risk", "token_price_collapse"),
        ("platform_fee_revenue", "repeat_transaction_volume", "regulated_revenue"),
        ("no_revenue", "liquidity", "token_price_only", "regulation"),
        "NFT/metaverse remains Green-blocked before repeat revenue and liquidity proof.",
    ),
    Round48ScoreTarget(
        "PLATFORM_GOVERNANCE_LEGAL_RISK",
        E2RArchetype.PLATFORM_GOVERNANCE_LEGAL_RISK,
        Round10ThemePosture.REDTEAM_FIRST,
        Round48ScoreWeightDraft(5, 5, 5, 5, 5, 0, 5),
        ("founder_legal_case", "ma_governance_dispute", "regulatory_probe"),
        ("legal_overhang_resolved", "governance_improvement", "minority_shareholder_protection"),
        ("trust_recovered", "governance_risk_low", "valuation_recovery_with_earnings"),
        ("legal_resolution_event_premium",),
        ("founder_arrest", "stock_manipulation_case", "regulatory_investigation", "platform_trust_damage"),
        ("legal_overhang_resolved", "governance_improvement", "trust_recovered"),
        ("founder_legal_case", "regulatory_investigation", "governance", "trust_damage"),
        "Legal and governance risk is a RedTeam overlay, not a positive score family.",
    ),
)


ROUND48_CASE_CANDIDATES: tuple[Round48CaseCandidate, ...] = (
    Round48CaseCandidate(
        "douzone_bizon_eqt_cloud_erp_case",
        "CLOUD_AI_SOFTWARE_INFRA",
        "012510",
        "Douzone Bizon cloud ERP EQT investment case",
        "KR",
        "success_candidate",
        None,
        date(2025, 11, 7),
        None,
        None,
        None,
        ("cloud_erp", "b2b_saas", "accounting_tax_compliance", "customer_lock_in"),
        ("arr_unverified", "opm_unverified", "fcf_unverified", "si_revenue_mix"),
        "cloud_erp_success_candidate_needs_backfill",
        "needs_price_backfill",
        ("Reuters EQT Douzone Bizon stake",),
        "B2B SaaS is Green-eligible only after ARR, retention, OPM, and FCF are verified.",
    ),
    Round48CaseCandidate(
        "palantir_ai_platform_revenue_case",
        "AI_SOFTWARE_APPLICATION",
        "PLTR",
        "Palantir AI platform revenue growth case",
        "US",
        "success_candidate",
        None,
        None,
        None,
        date(2025, 5, 5),
        None,
        ("ai_platform_revenue_growth", "commercial_revenue_growth", "government_revenue_growth", "contract_value", "rule_of_40"),
        ("valuation_saturation", "government_contract_concentration", "political_ethical_risk"),
        "ai_software_aligned_candidate_plus_4b_watch",
        "needs_source_date_and_price_backfill",
        ("MarketWatch Palantir AI demand", "Financial Times Palantir valuation watch"),
        "Palantir is an AI software success candidate, but valuation and concentration require 4B-watch.",
    ),
    Round48CaseCandidate(
        "netflix_ad_tier_growth_case",
        "STREAMING_AD_PLATFORM",
        "NFLX",
        "Netflix advertising tier growth and privacy watch",
        "US",
        "success_candidate",
        None,
        date(2024, 11, 12),
        None,
        None,
        None,
        ("ad_tier_users", "own_ad_tech", "ad_revenue_growth", "new_subscriber_mix"),
        ("privacy_lawsuit", "ad_arpu_saturation", "ad_load_pressure"),
        "streaming_ad_platform_success_candidate_privacy_watch",
        "needs_price_backfill",
        ("Reuters Netflix ad tier users", "The Verge Netflix ads upfront 2026"),
        "Streaming ad tier is structural only if ARPU and privacy/legal risk are controlled.",
    ),
    Round48CaseCandidate(
        "tencent_game_ai_ad_case",
        "GAME_CONTENT_IP",
        "0700.HK",
        "Tencent gaming and AI advertising mixed case",
        "HK",
        "success_candidate",
        None,
        date(2026, 5, 13),
        None,
        None,
        None,
        ("domestic_game_growth", "international_game_growth", "ai_ad_targeting", "ad_revenue_growth"),
        ("ai_capex_increase", "profit_miss", "competition_cost"),
        "game_ad_platform_success_but_ai_cost_watch",
        "needs_price_backfill",
        ("Reuters Tencent Q1 AI investment",),
        "Game IP and AI advertising help only if AI cost does not pressure margins.",
        (E2RArchetype.MEDIA_AD_CONTENT_CYCLE, E2RArchetype.AI_SOFTWARE_APPLICATION),
    ),
    Round48CaseCandidate(
        "trade_desk_revenue_miss_case",
        "MEDIA_AD_CONTENT_CYCLE",
        "TTD",
        "The Trade Desk adtech revenue miss and weak guide",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        None,
        ("ctv_adtech_platform", "programmatic_ad_growth"),
        ("revenue_miss", "weak_guidance", "premium_valuation", "growth_slowdown", "competition"),
        "premium_valuation_miss",
        "needs_source_date_and_price_backfill",
        ("Barron's Trade Desk revenue miss",),
        "Adtech can be structurally interesting, but premium valuation turns revenue misses into large drawdowns.",
    ),
    Round48CaseCandidate(
        "crowdstrike_outage_case",
        "SECURITY_IDENTITY_DEEPFAKE",
        "CRWD",
        "CrowdStrike global outage operational-trust break",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2024, 7, 19),
        ("security_arr", "endpoint_security_platform"),
        ("global_outage", "customer_lawsuit", "gross_negligence_claim", "renewal_risk", "trust_damage"),
        "security_operational_trust_hard_4c",
        "needs_price_backfill",
        ("CrowdStrike outage reference",),
        "Security software needs operational trust; a global outage is hard RedTeam evidence.",
    ),
    Round48CaseCandidate(
        "kakao_founder_legal_overhang_case",
        "PLATFORM_GOVERNANCE_LEGAL_RISK",
        "035720",
        "Kakao founder SM stock-manipulation legal overhang",
        "KR",
        "4b_watch",
        None,
        None,
        None,
        None,
        None,
        ("platform_assets", "legal_overhang", "founder_case", "acquittal_resolution"),
        ("founder_legal_case", "stock_manipulation_case", "governance_overhang", "regulatory_investigation"),
        "legal_overhang_watch_resolved_by_acquittal",
        "needs_source_date_and_price_backfill",
        ("Reuters Kakao founder acquittal",),
        "Platform assets can be strong while legal overhang suppresses valuation; exact event dates need backfill.",
    ),
    Round48CaseCandidate(
        "roblox_safety_forecast_cut_case",
        "GAME_CONTENT_IP",
        "RBLX",
        "Roblox child-safety forecast cut",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2026, 5, 1),
        ("platform_user_growth", "game_platform_bookings"),
        ("child_safety_regulation", "forecast_cut", "bookings_cut", "user_growth_slowdown"),
        "game_platform_safety_4c",
        "needs_price_backfill",
        ("Reuters Roblox forecast cut",),
        "Large user platforms are not Green if safety rules cut bookings and growth.",
    ),
    Round48CaseCandidate(
        "take_two_gta_delay_case",
        "GAME_CONTENT_IP",
        "TTWO",
        "Take-Two GTA VI second delay",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2025, 11, 6),
        ("major_game_ip", "single_title_expectation"),
        ("single_title_delay", "booking_deferral", "development_cost_inflation", "release_risk"),
        "single_ip_delay_4c_watch",
        "needs_price_backfill",
        ("Reuters Take-Two GTA VI delay",),
        "A major IP can still break near-term rerating when launch timing is delayed.",
    ),
    Round48CaseCandidate(
        "wpp_ad_cycle_slowdown_case",
        "MEDIA_AD_CONTENT_CYCLE",
        "WPP",
        "WPP advertising-cycle slowdown",
        "UK",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2025, 6, 9),
        ("ad_market_recovery",),
        ("client_budget_cut", "ad_growth_forecast_cut", "profit_decline", "dividend_cut", "ai_disintermediation"),
        "ad_cycle_4c_watch",
        "needs_price_backfill",
        ("Reuters WPP ad forecast cut", "Guardian WPP profit decline"),
        "Traditional advertising remains cycle-sensitive and exposed to client budget cuts and AI disruption.",
    ),
    Round48CaseCandidate(
        "meta_scam_ads_lawsuit_case",
        "PLATFORM_GOVERNANCE_LEGAL_RISK",
        "META",
        "Meta scam ads lawsuit and ad trust risk",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2026, 5, 11),
        ("ai_ad_targeting", "platform_ad_revenue"),
        ("scam_ad_lawsuit", "consumer_protection", "regulatory_lawsuit", "brand_trust_damage"),
        "platform_ad_governance_4c_watch",
        "needs_price_backfill",
        ("Reuters California county Meta scam ads lawsuit",),
        "AI advertising must be paired with ad quality and legal trust; scam-ad claims are RedTeam evidence.",
        (E2RArchetype.MEDIA_AD_CONTENT_CYCLE,),
    ),
)


ROUND48_PRICE_FIELDS: tuple[str, ...] = (
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
    "arr_growth",
    "subscription_revenue_growth",
    "recurring_revenue_ratio",
    "churn_rate",
    "net_retention_rate",
    "customer_count",
    "large_customer_concentration",
    "op_margin_change",
    "fcf_margin",
    "ai_revenue_contribution",
    "compute_cost_ratio",
    "model_dependency_flag",
    "copyright_lawsuit_flag",
    "license_risk_flag",
    "bookings_growth",
    "daily_active_users",
    "monthly_active_users",
    "single_ip_revenue_ratio",
    "game_delay_flag",
    "platform_safety_flag",
    "regulatory_ban_flag",
    "ad_revenue_growth",
    "ad_arpu",
    "ad_tier_users",
    "client_budget_cut_flag",
    "privacy_lawsuit_flag",
    "scam_ad_lawsuit_flag",
    "security_outage_flag",
    "customer_lawsuit_flag",
    "renewal_rate",
    "incident_recovery_days",
    "trust_damage_flag",
    "founder_legal_case_flag",
    "governance_overhang_flag",
    "regulatory_investigation_flag",
    "score_price_alignment",
    "price_validation_status",
)


def target_for(target_id: str) -> Round48ScoreTarget | None:
    for target in ROUND48_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round48_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND48_CASE_CANDIDATES:
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
                f"Round48 R8 case for {candidate.target_id}; "
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
                "user_count_or_ai_feature_is_not_structural_evidence_alone",
                "arr_arpu_opm_fcf_required_for_green",
                "trust_safety_legal_risk_can_block_green",
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


def round48_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND48_SCORE_TARGETS:
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


def round48_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND48_CASE_CANDIDATES:
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


def round48_stage_date_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND48_SCORE_TARGETS:
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


def round48_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round48_backfill": "true"} for field in ROUND48_PRICE_FIELDS)


def round48_summary() -> dict[str, int | bool]:
    records = round48_case_records()
    return {
        "target_count": len(ROUND48_SCORE_TARGETS),
        "case_candidate_count": len(records),
        "structural_success_count": sum(1 for record in records if record.case_type == "structural_success"),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for record in records if record.case_type == "cyclical_success"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "overheat_count": sum(1 for record in records if record.case_type == "overheat"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch"),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND48_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND48_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND48_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round48_r8_reports(
    *,
    output_directory: str | Path = ROUND48_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND48_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND48_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round48_r8_platform_content_sw_security_summary.md",
        "case_matrix": output / "round48_r8_case_matrix.csv",
        "stage_date_plan": output / "round48_r8_stage_date_plan.csv",
        "green_guardrails": output / "round48_r8_green_guardrails.md",
        "price_validation_plan": output / "round48_r8_price_validation_plan.md",
        "price_fields": output / "round48_r8_price_fields.csv",
    }
    _write_case_jsonl(round48_case_records(), cases)
    _write_rows(round48_score_profile_rows(), score_profiles)
    _write_rows(round48_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round48_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round48_price_field_rows(), paths["price_fields"])
    paths["summary"].write_text(render_round48_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round48_green_guardrail_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round48_price_validation_plan_markdown(), encoding="utf-8")
    return paths


def render_round48_summary_markdown() -> str:
    summary = round48_summary()
    lines = [
        "# Round-48 R8 Platform / Content / Software / Security Summary",
        "",
        f"- source_round: `{ROUND48_SOURCE_ROUND_PATH}`",
        "- large_sector: `PLATFORM_CONTENT_SW_SECURITY`",
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
        "- R8 is a repeat-revenue and trust-risk round, not a user-count or AI-feature round.",
        "- Example: Douzone Bizon is attractive only if ARR, retention, OPM, and FCF show SaaS quality.",
        "- Example: Palantir can be aligned but still needs 4B-watch when valuation outruns EPS/FCF.",
        "- Example: CrowdStrike shows one operational-trust break can override recurring security revenue.",
    ]
    return "\n".join(lines) + "\n"


def render_round48_green_guardrail_markdown() -> str:
    lines = [
        "# Round-48 R8 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Red flags |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND48_SCORE_TARGETS:
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
            "- Do not apply these R8 v1.0 weights to production scoring yet.",
            "- Do not treat user count, AI feature, new title, security threat headline, NFT/metaverse label, or ad recovery headline as Green evidence by itself.",
            "- Do not invent ARR, ARPU, churn, net retention, bookings, ad revenue, ad-tier users, security renewal, incident recovery, legal status, or price-path fields.",
            "- Do not lower Stage 3-Green for platform recall. Green requires repeat revenue, ARPU/ARR, OPM, FCF, retention, and trust/legal safety.",
            "- Treat outage, customer lawsuit, privacy lawsuit, scam ads, founder legal case, single-IP delay, child-safety forecast cut, and no recurring revenue as RedTeam evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round48_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-48 R8 Price Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign stage dates from source evidence only.",
        "2. Store stage-date close prices from official price data.",
        "3. Calculate MFE_30D / 90D / 180D / 1Y / 2Y.",
        "4. Calculate MAE_30D / 90D / 180D / 1Y.",
        "5. Calculate peak price, drawdown after peak, and below-stage3 flag.",
        "6. Compare price paths with ARR, bookings, ad revenue, churn, OPM, FCF, security incidents, privacy/legal events, and launch delays.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | stage candidate | check |",
        "| --- | --- | --- |",
    ]
    priority = {
        "palantir_ai_platform_revenue_case",
        "trade_desk_revenue_miss_case",
        "kakao_founder_legal_overhang_case",
    }
    for row in round48_case_candidate_rows():
        if row["stage2_date"] or row["stage4b_date"] or row["stage4c_date"] or row["case_id"] in priority:
            stage_date = row["stage2_date"] or row["stage4b_date"] or row["stage4c_date"] or "needs_source_date"
            lines.append(f"| `{row['case_id']}` | {stage_date} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `aligned`: ARR/OPM/FCF/bookings/ad revenue moves with price rerating.",
            "- `theme_or_feature_only`: AI feature, new title, security theme, or user count exists without economics.",
            "- `premium_valuation_miss`: growth business suffers large drawdown from revenue or guide miss.",
            "- `operational_trust_break`: outage, privacy, safety, or legal issue damages platform trust.",
            "- `single_ip_risk`: game/content rerating depends too heavily on one launch or IP.",
            "- `privacy_or_legal_overhang`: lawsuits and governance risk suppress rerating.",
        ]
    )
    return "\n".join(lines) + "\n"


def _score_price_alignment(candidate: Round48CaseCandidate) -> str:
    if "aligned" in candidate.alignment_hint and candidate.case_type in {"structural_success", "success_candidate"}:
        return "aligned"
    if candidate.case_type in {"event_premium", "overheat", "4b_watch"}:
        return "price_moved_without_evidence"
    if candidate.case_type in {"failed_rerating", "4c_thesis_break"}:
        return "false_positive_score"
    return "unknown"


def _rerating_result(candidate: Round48CaseCandidate) -> str:
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
    "ROUND48_CASE_CANDIDATES",
    "ROUND48_DEFAULT_CASES_PATH",
    "ROUND48_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND48_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND48_PRICE_FIELDS",
    "ROUND48_SCORE_TARGETS",
    "ROUND48_SOURCE_ROUND_PATH",
    "Round48CaseCandidate",
    "Round48ScoreTarget",
    "Round48ScoreWeightDraft",
    "render_round48_green_guardrail_markdown",
    "render_round48_price_validation_plan_markdown",
    "render_round48_summary_markdown",
    "round48_case_candidate_rows",
    "round48_case_records",
    "round48_price_field_rows",
    "round48_score_profile_rows",
    "round48_stage_date_rows",
    "round48_summary",
    "target_for",
    "write_round48_r8_reports",
]
