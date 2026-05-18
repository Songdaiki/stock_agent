"""Round-179 R8 Loop-11 Korea platform/content/software/security pack.

Round 179 narrows the R8 platform/content/software/security taxonomy to
Korea-focused AI cloud, ERP/SaaS, webtoon, game IP, K-pop, platform privacy,
security, legal, and guidance-risk cases. It is calibration/report material
only. Production feature engineering, scoring, staging, and RedTeam code must
not import it.
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


ROUND179_SOURCE_ROUND_PATH = "docs/round/round_179.md"
ROUND179_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round179_r8_loop11_platform_content_sw_security"
ROUND179_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r8_loop11_round179.jsonl"
ROUND179_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round179_r8_loop11_v11.csv"
ROUND179_SOURCE_CANONICAL_TARGET_IDS: tuple[str, ...] = (
    "ENTERPRISE_AI_CLOUD_INFRA_KOREA",
    "B2B_SAAS_ERP_WORKFLOW_KOREA",
    "PRIVATE_EQUITY_SOFTWARE_RERATING",
    "AI_CLOUD_CAPITAL_ALLOCATION",
    "SOVEREIGN_KOREAN_AI_MODEL",
    "WEBTOON_PLATFORM_IP_MONETIZATION",
    "PLATFORM_PRIVACY_SECURITY_OVERLAY",
    "GAME_CONTENT_IP_REPEAT_MONETIZATION",
    "GAME_SINGLE_IP_EVENT_PREMIUM",
    "GAME_IP_LAUNCH_DELAY_LEGAL_RISK",
    "KPOP_PLATFORM_CONTENT_IP",
    "ENTERTAINMENT_GOVERNANCE_LEGAL_OVERLAY",
    "AD_CONTENT_PLATFORM_GUIDANCE_RISK",
    "DISCLOSURE_CONFIDENCE_CAP",
)
ROUND179_SOURCE_CANONICAL_TARGET_COUNT = len(ROUND179_SOURCE_CANONICAL_TARGET_IDS)


@dataclass(frozen=True)
class Round179ScoreWeightDraft:
    arr_bookings_ad_ip_cloud_revenue: int | str
    recurrence_retention_workflow_lockin: int | str
    opm_fcf_gross_margin_conversion: int | str
    ai_cloud_platform_ip_bottleneck: int | str
    early_price_path_validation: int | str
    operational_trust_security_legal_governance: int | str
    valuation_room_4b_runway: int | str

    def as_dict(self) -> dict[str, int | str]:
        return {
            "arr_bookings_ad_ip_cloud_revenue": self.arr_bookings_ad_ip_cloud_revenue,
            "recurrence_retention_workflow_lockin": self.recurrence_retention_workflow_lockin,
            "opm_fcf_gross_margin_conversion": self.opm_fcf_gross_margin_conversion,
            "ai_cloud_platform_ip_bottleneck": self.ai_cloud_platform_ip_bottleneck,
            "early_price_path_validation": self.early_price_path_validation,
            "operational_trust_security_legal_governance": self.operational_trust_security_legal_governance,
            "valuation_room_4b_runway": self.valuation_room_4b_runway,
        }


@dataclass(frozen=True)
class Round179ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round179ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    loop11_penalty_axes: tuple[str, ...]
    normalization_point: str
    gate_only: bool = False

    @property
    def large_sector(self) -> Round10LargeSector:
        return Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round179CaseCandidate:
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
class Round179BaseScoreWeight:
    component: str
    points: int
    loop11_direction: str
    reason: str


@dataclass(frozen=True)
class Round179StageCap:
    stage_band: str
    max_score: str
    required_evidence: tuple[str, ...]
    example_cases: tuple[str, ...]
    green_policy: str


@dataclass(frozen=True)
class Round179ScoreStagePriceAlignment:
    case_id: str
    detected_stage: str
    price_path_status: str
    verdict: str
    normalization_adjustment: str


def _weights(
    revenue: int | str,
    recurrence: int | str,
    margin: int | str,
    bottleneck: int | str,
    price: int | str,
    trust: int | str,
    valuation: int | str,
) -> Round179ScoreWeightDraft:
    return Round179ScoreWeightDraft(revenue, recurrence, margin, bottleneck, price, trust, valuation)


def _target(
    target_id: str,
    archetype: E2RArchetype,
    posture: Round10ThemePosture,
    weight: Round179ScoreWeightDraft,
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
    gate_only: bool = False,
) -> Round179ScoreTarget:
    return Round179ScoreTarget(target_id, archetype, posture, weight, stage1, stage2, stage3, stage4b, stage4c, green, red, penalties, note, gate_only)


GATE_WEIGHT = _weights("gate", "gate", "gate", "gate", "gate", "gate", "gate")
CAP_WEIGHT = _weights("cap", "cap", "cap", "cap", "cap", "+", "cap")


ROUND179_BASE_SCORE_WEIGHTS: tuple[Round179BaseScoreWeight, ...] = (
    Round179BaseScoreWeight("arr_bookings_ad_ip_cloud_revenue", 24, "raise_actual_revenue", "AI, game IP, webtoon, or K-pop names matter only when ARR, bookings, ad/IP revenue, cloud revenue, or live-service revenue appears."),
    Round179BaseScoreWeight("recurrence_retention_workflow_lockin", 18, "raise_repeatability", "ERP renewal, SaaS churn, live-service bookings, fan platform ARPU, and paid content retention separate Stage 2 from Stage 3."),
    Round179BaseScoreWeight("opm_fcf_gross_margin_conversion", 14, "margin_bodyweight", "AI and content revenue must convert to OPM, FCF, or gross-margin durability."),
    Round179BaseScoreWeight("ai_cloud_platform_ip_bottleneck", 12, "bounded_narrative_credit", "AI/cloud/platform/IP bottleneck gets credit, but not enough to create Green alone."),
    Round179BaseScoreWeight("early_price_path_validation", 10, "loop11_axis", "Stage 2 이후 60D MFE helps identify early Stage 3, while Stage 2 이후 120D MFE helps 4B cooling."),
    Round179BaseScoreWeight("operational_trust_security_legal_governance", 14, "hard_redteam_gate", "Privacy, security, founder legal risk, governance, release delay, lawsuit, and guidance misses can cap or break the thesis."),
    Round179BaseScoreWeight("valuation_room_4b_runway", 8, "cool_headline_rerating", "AI SW, game IP, webtoon, K-pop, and platform narratives often reprice before repeat revenue confirms."),
)


ROUND179_STAGE_CAPS: tuple[Round179StageCap, ...] = (
    Round179StageCap(
        "Stage 1",
        "45",
        ("ai_cloud", "sovereign_ai", "game_new_title", "webtoon_ipo", "kpop_china_reopening", "platform_mau", "security_theme_news"),
        ("naver_hyperclova_x_sovereign_ai_stage1_2_case", "samsung_sds_ai_cloud_kkr_cb_stage2_4b_watch_case"),
        "AI, IP, MAU, webtoon IPO, K-pop reopening, or security headlines route research only.",
    ),
    Round179StageCap(
        "Stage 2",
        "70",
        ("strategic_investment", "contract_amount", "ipo", "new_ip_sales", "arr_bookings_guidance", "cloud_customer", "platform_ad_revenue"),
        ("samsung_sds_ai_cloud_kkr_cb_stage2_4b_watch_case", "douzone_bizon_eqt_erp_workflow_stage2_3_case", "webtoon_ipo_guidance_miss_4c_watch_case"),
        "Stage 2 can be strong, but Green waits for ARR, bookings, revenue, OPM/FCF, retention, and trust evidence.",
    ),
    Round179StageCap(
        "Stage 3",
        "requires_5_of_8",
        ("arr_bookings_cloud_ip_or_ad_revenue_grows", "op_eps_revision_or_quarterly_op_beat", "repeat_revenue_structure", "customer_or_platform_stickiness", "stage2_60d_mfe_20pct", "opm_fcf_improves", "no_security_legal_hard_issue", "valuation_not_overheated"),
        ("douzone_bizon_eqt_erp_workflow_stage2_3_case", "shiftup_game_ip_repeat_monetization_4b_watch_case", "krafton_pubg_bgmi_india_inzoi_stage2_3_4c_watch_case"),
        "Stage 3 requires repeat economics and clean trust/legal posture, not feature/IP/user-count narratives alone.",
    ),
    Round179StageCap(
        "Stage 4B",
        "requires_3_of_5",
        ("stage2_120d_mfe_80pct", "ai_game_ip_webtoon_kpop_keyword_2x", "arr_bookings_opm_cannot_follow_price", "ipo_strategic_investment_or_mna_headline_overheat", "same_narrative_crowded_in_news_reports"),
        ("samsung_sds_ai_cloud_kkr_cb_stage2_4b_watch_case", "shiftup_game_ip_repeat_monetization_4b_watch_case"),
        "Cool candidates when price and valuation move before ARR/bookings/OPM or repeat revenue.",
    ),
    Round179StageCap(
        "Stage 4C",
        "hard_gate",
        ("security_incident_or_data_leak", "founder_or_management_legal_risk", "game_release_delay_or_lawsuit_or_community_backlash", "arr_or_bookings_guidance_miss", "post_ipo_revenue_guidance_miss", "ad_or_ip_adaptation_revenue_decline", "ai_investment_cost_margin_pressure", "platform_ownership_or_foreign_regulatory_conflict"),
        ("naver_line_privacy_security_governance_4c_watch_case", "kakao_founder_legal_overhang_relief_case", "krafton_subnautica2_delay_lawsuit_4c_watch_case"),
        "Security, privacy, legal, guidance, release, and governance failures immediately block unsafe Green.",
    ),
)


ROUND179_SCORE_TARGETS: tuple[Round179ScoreTarget, ...] = (
    _target(
        "ENTERPRISE_AI_CLOUD_INFRA_KOREA",
        E2RArchetype.ENTERPRISE_AI_CLOUD_INFRA_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(20, 16, 14, 18, 10, 14, 8),
        stage1=("ai_cloud", "physical_ai", "enterprise_automation", "sovereign_ai_option"),
        stage2=("strategic_investor", "kkr_cb", "ai_offering_expansion", "cash_for_mna"),
        stage3=("ai_cloud_revenue", "arr", "long_term_cloud_contract", "opm_fcf_improvement", "mna_execution"),
        stage4b=("strategic_investor_name_rerating", "ai_option_priced_before_revenue"),
        stage4c=("cb_dilution", "ai_revenue_missing", "mna_execution_failure", "ai_investment_margin_pressure"),
        green=("ai_cloud_revenue", "arr", "long_term_cloud_contract", "opm_fcf_improvement", "mna_execution"),
        red=("cb_dilution", "actual_ai_arr_missing", "mna_execution_unknown", "ai_cost_margin_pressure"),
        penalties=("cb_dilution", "ai_arr_missing", "mna_execution", "margin"),
        note="Samsung SDS-style AI cloud is strong Stage 2; Green waits for actual AI/cloud revenue, ARR, contracts, and FCF.",
    ),
    _target(
        "B2B_SAAS_ERP_WORKFLOW_KOREA",
        E2RArchetype.B2B_SAAS_ERP_WORKFLOW_KOREA,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(24, 22, 16, 8, 10, 12, 8),
        stage1=("erp_cloud", "sme_accounting_tax_compliance", "workflow_software"),
        stage2=("strategic_pe_investment", "recurring_software_model", "workflow_lock_in", "stake_sale"),
        stage3=("arr_growth", "low_churn", "opm_fcf_improvement", "arpu_growth", "renewal_rate"),
        stage4b=("pe_premium_priced_before_arr", "software_multiple_crowded"),
        stage4c=("arr_churn_miss", "opm_decline", "regulatory_approval_delay", "workflow_competition"),
        green=("arr_growth", "low_churn", "opm_fcf_improvement", "arpu_growth", "renewal_rate"),
        red=("arr_churn_missing", "opm_unconfirmed", "regulatory_approval_pending", "pe_event_premium"),
        penalties=("arr_missing", "churn", "opm", "pe_event_premium"),
        note="Douzone-style ERP workflow can be Green-capable only after ARR, churn, OPM, FCF, and workflow lock-in confirm.",
    ),
    _target(
        "PRIVATE_EQUITY_SOFTWARE_RERATING",
        E2RArchetype.PRIVATE_EQUITY_SOFTWARE_RERATING,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(18, 18, 16, 8, 10, 14, 8),
        stage1=("pe_interest", "software_takeout_premium", "governance_improvement_expectation"),
        stage2=("strategic_stake", "operation_improvement_plan", "core_business_focus"),
        stage3=("opm_improvement", "fcf_conversion", "arr_growth", "operational_kpi_improves"),
        stage4b=("pe_name_premium_before_execution",),
        stage4c=("deal_approval_delay", "operation_improvement_failure", "debt_or_governance_issue"),
        green=("opm_improvement", "fcf_conversion", "arr_growth", "operational_kpi_improves"),
        red=("event_premium_only", "opm_unconfirmed", "deal_delay", "governance_issue"),
        penalties=("event_premium", "execution", "governance"),
        note="Private-equity validation supports Stage 2, but not Green before operating KPIs improve.",
    ),
    _target(
        "AI_CLOUD_CAPITAL_ALLOCATION",
        E2RArchetype.AI_CLOUD_CAPITAL_ALLOCATION,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights(16, 12, 14, 18, 10, 20, 8),
        stage1=("cash_balance", "ai_mna_option", "stablecoin_option"),
        stage2=("capital_allocation_strategy", "strategic_advice", "cb_or_external_capital"),
        stage3=("disciplined_mna", "ai_revenue_after_capex", "fcf_after_investment"),
        stage4b=("mna_option_overpriced",),
        stage4c=("cb_dilution", "bad_mna", "capex_overrun", "margin_pressure"),
        green=("disciplined_mna", "ai_revenue_after_capex", "fcf_after_investment"),
        red=("cb_dilution", "mna_execution_unknown", "ai_investment_cost", "margin_pressure"),
        penalties=("dilution", "mna", "capex", "margin"),
        note="AI-cloud capital allocation is a RedTeam overlay when CB, M&A, or capex risks outrun revenue evidence.",
        gate_only=True,
    ),
    _target(
        "SOVEREIGN_KOREAN_AI_MODEL",
        E2RArchetype.SOVEREIGN_KOREAN_AI_MODEL,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(14, 14, 12, 22, 10, 18, 8),
        stage1=("korean_llm", "sovereign_ai", "technical_report", "benchmark"),
        stage2=("model_release", "public_enterprise_adoption_expectation", "cloud_usage_pipeline"),
        stage3=("b2b_paid_api", "naver_cloud_revenue", "ai_search_ad_arpu", "inference_margin", "enterprise_contract"),
        stage4b=("sovereign_ai_keyword_overheated",),
        stage4c=("inference_cost_pressure", "b2b_monetization_missing", "ai_search_arpu_missing", "model_competition"),
        green=("b2b_paid_api", "cloud_revenue", "ai_search_ad_arpu", "inference_margin", "enterprise_contract"),
        red=("b2b_monetization_missing", "inference_cost_unknown", "ai_search_arpu_missing", "technical_report_only"),
        penalties=("monetization", "inference_cost", "arpu", "competition"),
        note="Naver HyperCLOVA X is Stage 1/2 before paid B2B API, cloud usage, and AI ad monetization.",
    ),
    _target(
        "WEBTOON_PLATFORM_IP_MONETIZATION",
        E2RArchetype.WEBTOON_PLATFORM_IP_MONETIZATION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(20, 18, 14, 14, 10, 16, 8),
        stage1=("webtoon_ip", "creator_platform", "k_content"),
        stage2=("nasdaq_ipo", "paid_content", "ad_revenue", "ip_adaptation_pipeline"),
        stage3=("paid_content_growth", "ad_arpu", "ip_adaptation_revenue", "opm_fcf", "retention"),
        stage4b=("ipo_premium", "global_ip_platform_crowded"),
        stage4c=("guidance_miss", "ip_adaptation_revenue_decline", "net_loss", "platform_valuation_compression"),
        green=("paid_content_growth", "ad_arpu", "ip_adaptation_revenue", "opm_fcf", "retention"),
        red=("guidance_miss", "ip_adaptation_revenue_decline", "net_loss", "monetization_gap"),
        penalties=("guidance", "ip_adaptation", "net_loss", "monetization"),
        note="Webtoon platform needs paid content, ad revenue, IP adaptation revenue, and OPM/FCF; IPO alone is Stage 2.",
    ),
    _target(
        "PLATFORM_PRIVACY_SECURITY_OVERLAY",
        E2RArchetype.PLATFORM_PRIVACY_SECURITY_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("global_platform_asset", "line_ly_corp", "platform_data"),
        stage2=("buyback_or_asset_monetization", "platform_asset_value"),
        stage3=("not_green_if_data_leak_or_regulatory_pressure",),
        stage4b=("platform_asset_repricing_ignores_security",),
        stage4c=("data_leak", "privacy_security_incident", "foreign_regulatory_pressure", "capital_relationship_review"),
        green=(),
        red=("data_leak", "privacy_security_incident", "regulatory_pressure", "governance_uncertainty"),
        penalties=("privacy", "security", "regulatory", "governance"),
        note="Platform overseas expansion must pass privacy, security, and governance gates.",
        gate_only=True,
    ),
    _target(
        "GAME_CONTENT_IP_REPEAT_MONETIZATION",
        E2RArchetype.GAME_CONTENT_IP_REPEAT_MONETIZATION,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(24, 20, 16, 12, 10, 10, 8),
        stage1=("game_ip", "new_title", "global_console_expansion", "live_service"),
        stage2=("new_ip_sales", "live_service_cash_cow", "bookings_visibility", "india_platform_option"),
        stage3=("live_service_bookings", "repeat_sales", "dlc_or_ugc_monetization", "opm_fcf", "pipeline_stability"),
        stage4b=("ipo_or_hit_title_premium", "valuation_before_repeat_bookings"),
        stage4c=("release_delay", "developer_lawsuit", "community_backlash", "new_ip_sales_slowdown"),
        green=("live_service_bookings", "repeat_sales", "opm_fcf", "pipeline_stability", "bookings_growth"),
        red=("single_ip_concentration", "release_delay", "lawsuit", "community_backlash", "valuation_premium"),
        penalties=("single_ip", "launch", "legal", "valuation"),
        note="Krafton/Shift Up-style games need repeat bookings and OPM/FCF, not only a hit-title headline.",
    ),
    _target(
        "GAME_SINGLE_IP_EVENT_PREMIUM",
        E2RArchetype.GAME_SINGLE_IP_EVENT_PREMIUM,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(18, 12, 12, 18, 10, 14, 8),
        stage1=("new_title_hype", "ipo_premium", "single_ip_success"),
        stage2=("initial_sales", "pc_port", "preorder_actual", "publisher_pipeline"),
        stage3=("repeat_bookings", "retention", "follow_on_sales", "opm_fcf"),
        stage4b=("single_ip_valuation_premium", "ipo_premium_crowded"),
        stage4c=("single_ip_fade", "pipeline_gap", "platform_fee_pressure", "user_retention_miss"),
        green=("repeat_bookings", "retention", "follow_on_sales", "opm_fcf"),
        red=("single_ip_concentration", "ipo_valuation_premium", "pipeline_uncertainty", "retention_miss"),
        penalties=("single_ip", "ipo", "pipeline", "retention"),
        note="Single-IP game events stay Watch/Yellow before repeat bookings and retention evidence.",
    ),
    _target(
        "GAME_IP_LAUNCH_DELAY_LEGAL_RISK",
        E2RArchetype.GAME_IP_LAUNCH_DELAY_LEGAL_RISK,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("sequel_expectation", "new_ip_pipeline"),
        stage2=("publisher_portfolio", "release_schedule"),
        stage3=("not_green_if_delay_or_lawsuit",),
        stage4b=("ip_hype_before_release",),
        stage4c=("release_delay", "earnout_dispute", "developer_lawsuit", "community_backlash"),
        green=(),
        red=("release_delay", "developer_lawsuit", "community_backlash", "earnout_dispute"),
        penalties=("release_delay", "lawsuit", "community", "trust"),
        note="Game release delay, developer lawsuit, and community trust issues are 4C-watch gates.",
        gate_only=True,
    ),
    _target(
        "KPOP_PLATFORM_CONTENT_IP",
        E2RArchetype.KPOP_PLATFORM_CONTENT_IP,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(20, 20, 14, 14, 10, 14, 8),
        stage1=("kpop_ip", "china_reopening", "fan_platform", "global_touring"),
        stage2=("strategic_stake", "touring_schedule", "fan_platform_arpu_expectation", "china_option"),
        stage3=("china_performance_reopens", "fan_platform_arpu", "album_tour_revenue", "opm_fcf", "artist_pipeline_stability"),
        stage4b=("kpop_china_reopening_crowded", "ip_expectation_priced"),
        stage4c=("founder_legal_risk", "governance_issue", "artist_ip_break", "china_delay"),
        green=("fan_platform_arpu", "album_tour_revenue", "opm_fcf", "artist_pipeline_stability", "china_performance_reopens"),
        red=("founder_legal_risk", "governance_issue", "artist_ip_concentration", "china_delay"),
        penalties=("legal", "governance", "artist_ip", "china"),
        note="K-pop can be Stage 2 on IP and China reopening, but Green waits for fan platform, touring, ARPU, and clean governance.",
    ),
    _target(
        "ENTERTAINMENT_GOVERNANCE_LEGAL_OVERLAY",
        E2RArchetype.ENTERTAINMENT_GOVERNANCE_LEGAL_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("entertainment_ip", "stake_battle", "platform_option"),
        stage2=("legal_overhang_relief", "governance_restructuring"),
        stage3=("not_green_until_legal_overhang_clears",),
        stage4b=("ip_value_ignores_legal_risk",),
        stage4c=("founder_legal_risk", "stock_manipulation_case", "management_warrant", "fan_backlash"),
        green=(),
        red=("founder_legal_risk", "governance_discount", "stock_manipulation_case", "management_warrant"),
        penalties=("legal", "governance", "fan_backlash"),
        note="Entertainment platform/IP evidence is capped when founder, governance, or legal risks are active.",
        gate_only=True,
    ),
    _target(
        "AD_CONTENT_PLATFORM_GUIDANCE_RISK",
        E2RArchetype.AD_CONTENT_PLATFORM_GUIDANCE_RISK,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("ad_platform", "content_platform", "ip_adaptation"),
        stage2=("ad_revenue_visibility", "ip_revenue_pipeline"),
        stage3=("not_green_if_guidance_miss",),
        stage4b=("platform_ip_ipo_premium",),
        stage4c=("guidance_miss", "ad_revenue_decline", "ip_adaptation_revenue_decline", "net_loss"),
        green=(),
        red=("guidance_miss", "ad_revenue_decline", "ip_adaptation_revenue_decline", "net_loss"),
        penalties=("guidance", "ad_revenue", "ip_adaptation", "loss"),
        note="Ad/content platform guidance misses are hard RedTeam evidence after IPO or platform repricing.",
        gate_only=True,
    ),
    _target(
        "DISCLOSURE_CONFIDENCE_CAP",
        E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        Round10ThemePosture.REDTEAM_FIRST,
        CAP_WEIGHT,
        stage1=("ai_feature_headline", "game_ip_headline", "webtoon_ipo_headline", "kpop_reopening_headline", "platform_mau_headline"),
        stage2=("arr_bookings_contract_detail_required", "opm_fcf_required", "legal_security_status_required"),
        stage3=("multi_source_confirmation", "arr_or_bookings_or_revenue_verified"),
        stage4b=("headline_rerating",),
        stage4c=("arr_missing", "bookings_missing", "contract_missing", "opm_missing", "security_or_legal_detail_missing"),
        green=("arr", "bookings", "cloud_revenue", "ad_revenue", "ip_revenue", "opm_fcf", "security_legal_clean"),
        red=("arr_missing", "bookings_missing", "contract_missing", "opm_missing", "legal_security_missing"),
        penalties=("disclosure", "arr_bookings", "opm_fcf", "legal_security"),
        note="R8 disclosure confidence is capped when ARR, bookings, contracts, OPM/FCF, security, or legal details are missing.",
    ),
)


ROUND179_SCORE_STAGE_PRICE_ALIGNMENT: tuple[Round179ScoreStagePriceAlignment, ...] = (
    Round179ScoreStagePriceAlignment("samsung_sds_ai_cloud_kkr_cb_stage2_4b_watch_case", "Stage 2 strong plus 4B watch", "KKR CB caused +20.8% reaction before AI ARR evidence", "ai_cloud_cb_stage2_not_green", "score KKR and cash as Stage 2; cool with CB dilution and AI revenue gap"),
    Round179ScoreStagePriceAlignment("douzone_bizon_eqt_erp_workflow_stage2_3_case", "Stage 2 to Stage 3 candidate", "EQT validates workflow software, but ARR/churn/OPM need backfill", "erp_workflow_requires_arr_churn_opm", "promote only after repeat SaaS economics confirm"),
    Round179ScoreStagePriceAlignment("webtoon_ipo_guidance_miss_4c_watch_case", "Stage 2 to 4C-watch", "IPO debut was positive, later guidance miss and IP adaptation decline broke narrative", "webtoon_guidance_miss_blocks_green", "turn guidance miss and IP revenue decline into RedTeam inputs"),
    Round179ScoreStagePriceAlignment("krafton_pubg_bgmi_india_inzoi_stage2_3_4c_watch_case", "Stage 2 to Stage 3 candidate plus 4C-watch", "cash-cow and inZOI evidence coexist with Subnautica delay/legal risk", "game_ip_repeat_revenue_needs_legal_split", "separate PUBG/BGMI bookings from Subnautica legal risk"),
    Round179ScoreStagePriceAlignment("naver_line_privacy_security_governance_4c_watch_case", "4C-watch overlay", "data leak and Japan regulatory pressure override platform-asset narrative", "privacy_security_governance_gate", "hard-cap platform rerating when privacy/security trust breaks"),
)


def _d(value: str) -> date:
    return date.fromisoformat(value)


ROUND179_CASE_CANDIDATES: tuple[Round179CaseCandidate, ...] = (
    Round179CaseCandidate(
        "samsung_sds_ai_cloud_kkr_cb_stage2_4b_watch_case",
        "ENTERPRISE_AI_CLOUD_INFRA_KOREA",
        "018260",
        "Samsung SDS AI cloud and KKR CB capital allocation",
        "KR",
        "4b_watch",
        None,
        _d("2026-04-15"),
        None,
        _d("2026-04-15"),
        None,
        ("kkr_820m_usd_cb", "share_price_20_8pct_jump", "ai_offering_expansion", "physical_ai_option", "6_4tn_krw_cash", "mna_capital_allocation_strategy"),
        ("cb_dilution_risk", "actual_ai_arr_missing", "mna_execution_unknown", "ai_cloud_revenue_missing"),
        "stage2_strong_with_4b_watch",
        "needs_ai_arr_cloud_revenue_cb_dilution_price_backfill",
        ("round_179.md Samsung SDS KKR CB case",),
        "Samsung SDS has strong Stage 2 AI-cloud/capital-allocation evidence, but Green waits for AI revenue, ARR, OPM/FCF, and dilution absorption.",
        (E2RArchetype.AI_CLOUD_CAPITAL_ALLOCATION, E2RArchetype.PRIVATE_EQUITY_SOFTWARE_RERATING),
    ),
    Round179CaseCandidate(
        "douzone_bizon_eqt_erp_workflow_stage2_3_case",
        "B2B_SAAS_ERP_WORKFLOW_KOREA",
        "012510",
        "Douzone Bizon EQT ERP workflow rerating candidate",
        "KR",
        "success_candidate",
        None,
        _d("2025-11-07"),
        None,
        None,
        None,
        ("eqt_37_6pct_stake", "930m_usd_transaction", "erp_accounting_tax_compliance_workflow", "cloud_based_enterprise_software", "operational_improvement_plan"),
        ("arr_churn_missing", "opm_improvement_unconfirmed", "regulatory_approval_pending"),
        "stage2_3_workflow_candidate",
        "needs_arr_churn_opm_price_backfill",
        ("round_179.md Douzone Bizon EQT case",),
        "Douzone is a Stage 2/3 candidate only if PE validation converts into ARR, churn stability, ARPU, OPM, and FCF.",
        (E2RArchetype.PRIVATE_EQUITY_SOFTWARE_RERATING,),
    ),
    Round179CaseCandidate(
        "naver_hyperclova_x_sovereign_ai_stage1_2_case",
        "SOVEREIGN_KOREAN_AI_MODEL",
        "035420",
        "NAVER HyperCLOVA X sovereign Korean AI model",
        "KR",
        "event_premium",
        None,
        None,
        None,
        None,
        None,
        ("hyperclova_x_think_technical_report", "korean_english_bilingual_llm", "korea_benchmark", "sovereign_ai_option"),
        ("b2b_monetization_missing", "inference_cost_unknown", "ai_search_arpu_missing", "technical_report_only"),
        "stage1_2_ai_option_monetization_gate",
        "needs_b2b_api_cloud_revenue_arpu_price_backfill",
        ("round_179.md NAVER HyperCLOVA X case",),
        "NAVER sovereign AI is Stage 1/2 before paid API, cloud usage, enterprise contracts, inference margin, and AI search ARPU.",
    ),
    Round179CaseCandidate(
        "shiftup_game_ip_repeat_monetization_4b_watch_case",
        "GAME_CONTENT_IP_REPEAT_MONETIZATION",
        "462870",
        "Shift Up Nikke and Stellar Blade repeat monetization",
        "KR",
        "4b_watch",
        None,
        _d("2025-06-01"),
        None,
        None,
        None,
        ("nikke_live_service_ip", "stellar_blade_pc_3d_1m_sales", "stellar_blade_total_3m_sales", "2025_op_181bn_krw", "unbound_acquisition_pipeline"),
        ("single_ip_concentration", "ipo_valuation_premium", "future_pipeline_uncertainty", "tencent_stake_risk"),
        "stage2_3_game_ip_candidate_with_4b_watch",
        "needs_bookings_retention_opm_price_backfill",
        ("round_179.md Shift Up case",),
        "Shift Up can be Stage 2/3 candidate, but IPO and hit-title premiums require 4B cooling until repeat bookings and retention confirm.",
        (E2RArchetype.GAME_SINGLE_IP_EVENT_PREMIUM,),
    ),
    Round179CaseCandidate(
        "krafton_pubg_bgmi_india_inzoi_stage2_3_4c_watch_case",
        "GAME_CONTENT_IP_REPEAT_MONETIZATION",
        "259960",
        "Krafton PUBG/BGMI India and inZOI with Subnautica legal risk",
        "KR",
        "success_candidate",
        None,
        _d("2025-12-19"),
        None,
        None,
        None,
        ("bgmi_240m_downloads", "india_666m_usd_tech_fund", "india_game_sector_200m_usd_investment", "inzoi_first_week_1m_sales", "pubg_cash_cow"),
        ("subnautica2_release_delay", "developer_lawsuit", "earnout_dispute", "new_ip_hit_dependency", "ai_first_hr_uncertainty"),
        "stage2_3_candidate_with_4c_watch_overlay",
        "needs_bookings_opm_legal_price_backfill",
        ("round_179.md Krafton case",),
        "Krafton needs PUBG/BGMI bookings and inZOI monetization separated from Subnautica delay and developer legal risk.",
        (E2RArchetype.GAME_IP_LAUNCH_DELAY_LEGAL_RISK,),
    ),
    Round179CaseCandidate(
        "sm_tencent_music_china_reopening_kpop_stage2_case",
        "KPOP_PLATFORM_CONTENT_IP",
        "041510",
        "SM Entertainment Tencent Music stake and China reopening option",
        "KR",
        "success_candidate",
        None,
        _d("2025-05-27"),
        None,
        None,
        None,
        ("tencent_music_9_7pct_stake", "243bn_krw_stake_purchase", "china_performance_reopening_option", "kpop_ip", "fan_platform_option"),
        ("china_reopening_delay", "kakao_governance_overhang", "artist_pipeline_risk"),
        "stage2_kpop_ip_china_option",
        "needs_touring_fan_arpu_opm_price_backfill",
        ("round_179.md SM Tencent Music case",),
        "SM is Stage 2 on strategic stake and China reopening option; Green needs real touring, fan platform ARPU, OPM, and governance quality.",
        (E2RArchetype.ENTERTAINMENT_GOVERNANCE_LEGAL_OVERLAY,),
    ),
    Round179CaseCandidate(
        "hybe_founder_legal_risk_kpop_cap_case",
        "ENTERTAINMENT_GOVERNANCE_LEGAL_OVERLAY",
        "352820",
        "HYBE founder legal risk K-pop valuation cap",
        "KR",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        _d("2026-04-21"),
        ("global_ip_platform", "weverse_fan_platform_option", "touring_fandom"),
        ("founder_detention_warrant_news", "stock_reaction_minus_2_4pct", "capital_market_act_risk", "governance_cap"),
        "legal_governance_4c_watch",
        "needs_legal_resolution_price_backfill",
        ("round_179.md HYBE founder legal risk case",),
        "HYBE IP and platform strength are capped while founder legal risk and governance overhang remain active.",
    ),
    Round179CaseCandidate(
        "webtoon_ipo_guidance_miss_4c_watch_case",
        "WEBTOON_PLATFORM_IP_MONETIZATION",
        "WBTN_REFERENCE",
        "Webtoon Entertainment IPO then guidance miss",
        "US",
        "4c_thesis_break",
        None,
        _d("2024-06-27"),
        None,
        None,
        _d("2026-05-01"),
        ("nasdaq_ipo", "ipo_price_21_usd", "debut_9_5pct_up", "global_creator_platform", "naver_platform_value"),
        ("q2_revenue_guidance_miss", "after_hours_minus_15pct", "ip_adaptation_revenue_decline_23pct", "net_loss", "revenue_yoy_down_1_5pct"),
        "ipo_stage2_guidance_miss_4c_watch",
        "needs_webtoon_price_guidance_backfill",
        ("round_179.md Webtoon IPO/guidance miss case",),
        "Webtoon IPO is Stage 2 visibility; guidance miss and IP adaptation decline become 4C-watch.",
        (E2RArchetype.AD_CONTENT_PLATFORM_GUIDANCE_RISK,),
    ),
    Round179CaseCandidate(
        "naver_line_privacy_security_governance_4c_watch_case",
        "PLATFORM_PRIVACY_SECURITY_OVERLAY",
        "035420/4689_REFERENCE",
        "NAVER-LY/LINE privacy security and Japan regulatory pressure",
        "KR/JP",
        "4c_thesis_break",
        None,
        _d("2024-08-02"),
        None,
        None,
        _d("2024-08-02"),
        ("line_ly_platform_asset", "buyback_asset_monetization", "softbank_naver_voting_rights_change"),
        ("data_leak", "japan_regulatory_pressure", "naver_dependency_reduction_demand", "capital_relationship_review", "300k_plus_user_records_exposure"),
        "platform_asset_security_governance_gate",
        "needs_platform_event_price_backfill",
        ("round_179.md NAVER-LY/LINE privacy case",),
        "Platform overseas asset value is capped when privacy, data leak, and regulator pressure appear.",
    ),
    Round179CaseCandidate(
        "kakao_founder_legal_overhang_relief_case",
        "ENTERTAINMENT_GOVERNANCE_LEGAL_OVERLAY",
        "035720",
        "Kakao founder legal overhang then partial relief",
        "KR",
        "4b_watch",
        None,
        _d("2025-10-21"),
        None,
        _d("2025-10-21"),
        None,
        ("kakaotalk_platform_asset", "sm_entertainment_content_option", "acquittal_partial_legal_relief"),
        ("founder_legal_risk", "stock_manipulation_case", "15_year_sentence_request", "governance_discount"),
        "legal_overhang_partial_relief_not_green",
        "needs_legal_event_price_backfill",
        ("round_179.md Kakao legal overhang case",),
        "Kakao legal relief can reduce risk, but platform Green remains capped until governance discount is resolved.",
    ),
    Round179CaseCandidate(
        "krafton_subnautica2_delay_lawsuit_4c_watch_case",
        "GAME_IP_LAUNCH_DELAY_LEGAL_RISK",
        "259960",
        "Krafton Subnautica 2 delay and lawsuit",
        "KR",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        _d("2026-07-01"),
        ("subnautica_ip_sequel", "publisher_portfolio_expansion"),
        ("release_delay", "earnout_dispute", "developer_lawsuit", "community_backlash"),
        "game_release_legal_4c_watch",
        "needs_release_legal_price_backfill",
        ("round_179.md Krafton Subnautica 2 delay case",),
        "A strong game IP can still be 4C-watch when release timing and developer/community trust break.",
    ),
    Round179CaseCandidate(
        "r8_disclosure_confidence_cap_case",
        "DISCLOSURE_CONFIDENCE_CAP",
        "KR_R8_DISCLOSURE_BASKET",
        "Korea R8 disclosure confidence cap basket",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("ai_feature_headline", "game_ip_headline", "webtoon_ipo_headline", "kpop_reopening_headline", "platform_mau_headline"),
        ("arr_missing", "bookings_missing", "contract_amount_missing", "opm_missing", "legal_security_detail_missing"),
        "disclosure_detail_missing_cap",
        "needs_arr_bookings_opm_legal_detail_backfill",
        ("round_179.md R8 disclosure confidence cap",),
        "R8 headlines are capped when ARR, bookings, contract amount, OPM/FCF, security, or legal details are missing.",
    ),
)


ROUND179_PRICE_FIELDS: tuple[str, ...] = (
    "ticker",
    "company_name",
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
    "relative_strength_vs_software_basket",
    "relative_strength_vs_game_basket",
    "relative_strength_vs_content_basket",
    "arr",
    "arr_growth_yoy",
    "bookings",
    "bookings_growth_yoy",
    "cloud_revenue",
    "cloud_revenue_growth_yoy",
    "ad_revenue",
    "ip_adaptation_revenue",
    "paid_content_revenue",
    "live_service_revenue",
    "fan_platform_arpu",
    "op_revision_before_stage3",
    "op_revision_after_stage3",
    "eps_revision_before_stage3",
    "eps_revision_after_stage3",
    "gross_margin",
    "opm",
    "fcf",
    "churn",
    "retention",
    "renewal_rate",
    "contract_amount",
    "strategic_investor",
    "cb_or_dilution_flag",
    "ipo_event_flag",
    "guidance_miss_flag",
    "release_delay_flag",
    "lawsuit_flag",
    "privacy_security_incident_flag",
    "founder_legal_risk_flag",
    "regulatory_pressure_flag",
    "disclosure_confidence",
    "valuation_at_stage3",
    "valuation_at_stage4b",
)


def round179_target_for(target_id: str) -> Round179ScoreTarget | None:
    for target in ROUND179_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round179_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND179_CASE_CANDIDATES:
        target = round179_target_for(candidate.target_id)
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
                f"Round179 R8 Loop-11 case for {candidate.target_id}; "
                "Korea platform/content/software/security narratives are separated from ARR, bookings, ad/IP revenue, cloud revenue, OPM, FCF, retention, security, legal, and governance evidence."
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
            score_price_alignment=_score_price_alignment(candidate),
            rerating_result=_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
            score_weight_hint=_score_weight_hint(target),
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "ai_ip_mau_ipo_or_kpop_headline_is_not_stage3",
                "require_arr_bookings_ad_ip_cloud_revenue_opm_fcf_retention_and_trust_for_green",
                "stage3_early_catch_requires_5_of_8_loop11_conditions",
                "do_not_invent_arr_bookings_cloud_revenue_ad_revenue_ip_revenue_opm_fcf_retention_stage_prices_or_mfe_mae",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=False,
                price_data_available=False,
                stage_dates_confidence=0.75 if candidate.stage2_date or candidate.stage4b_date or candidate.stage4c_date else 0.2,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round179_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND179_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "arr_bookings_ad_ip_cloud_revenue": str(weights["arr_bookings_ad_ip_cloud_revenue"]),
                "recurrence_retention_workflow_lockin": str(weights["recurrence_retention_workflow_lockin"]),
                "opm_fcf_gross_margin_conversion": str(weights["opm_fcf_gross_margin_conversion"]),
                "ai_cloud_platform_ip_bottleneck": str(weights["ai_cloud_platform_ip_bottleneck"]),
                "early_price_path_validation": str(weights["early_price_path_validation"]),
                "operational_trust_security_legal_governance": str(weights["operational_trust_security_legal_governance"]),
                "valuation_room_4b_runway": str(weights["valuation_room_4b_runway"]),
                "stage1_signals": "|".join(target.stage1_signals),
                "stage2_signals": "|".join(target.stage2_signals),
                "stage3_conditions": "|".join(target.stage3_conditions),
                "stage4b_conditions": "|".join(target.stage4b_conditions),
                "stage4c_conditions": "|".join(target.stage4c_conditions),
                "green_conditions": "|".join(target.green_conditions),
                "red_flags": "|".join(target.red_flags),
                "loop11_penalty_axes": "|".join(target.loop11_penalty_axes),
                "gate_only": str(target.gate_only).lower(),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round179_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND179_CASE_CANDIDATES:
        target = round179_target_for(candidate.target_id)
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


def round179_stage_date_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "target_id": target.target_id,
            "stage1": "|".join(target.stage1_signals),
            "stage2": "|".join(target.stage2_signals),
            "stage3": "|".join(target.stage3_conditions),
            "stage4b": "|".join(target.stage4b_conditions),
            "stage4c": "|".join(target.stage4c_conditions),
            "red_flags": "|".join(target.red_flags),
            "loop11_penalty_axes": "|".join(target.loop11_penalty_axes),
            "gate_only": str(target.gate_only).lower(),
            "production_scoring_changed": "false",
        }
        for target in ROUND179_SCORE_TARGETS
    )


def round179_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round179_backfill": "true"} for field in ROUND179_PRICE_FIELDS)


def round179_base_score_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "component": item.component,
            "points": str(item.points),
            "loop11_direction": item.loop11_direction,
            "reason": item.reason,
            "production_scoring_changed": "false",
        }
        for item in ROUND179_BASE_SCORE_WEIGHTS
    )


def round179_stage_cap_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "stage_band": item.stage_band,
            "max_score": item.max_score,
            "required_evidence": "|".join(item.required_evidence),
            "example_cases": "|".join(item.example_cases),
            "green_policy": item.green_policy,
            "production_scoring_changed": "false",
        }
        for item in ROUND179_STAGE_CAPS
    )


def round179_score_stage_price_alignment_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "case_id": item.case_id,
            "detected_stage": item.detected_stage,
            "price_path_status": item.price_path_status,
            "verdict": item.verdict,
            "normalization_adjustment": item.normalization_adjustment,
            "production_scoring_changed": "false",
        }
        for item in ROUND179_SCORE_STAGE_PRICE_ALIGNMENT
    )


def round179_summary() -> dict[str, int | bool]:
    records = round179_case_records()
    return {
        "target_count": len(ROUND179_SCORE_TARGETS),
        "source_canonical_target_count": ROUND179_SOURCE_CANONICAL_TARGET_COUNT,
        "case_candidate_count": len(records),
        "base_score_component_count": len(ROUND179_BASE_SCORE_WEIGHTS),
        "stage_cap_count": len(ROUND179_STAGE_CAPS),
        "score_stage_price_alignment_count": len(ROUND179_SCORE_STAGE_PRICE_ALIGNMENT),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND179_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND179_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND179_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "gate_only_target_count": sum(1 for target in ROUND179_SCORE_TARGETS if target.gate_only),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round179_r8_loop11_reports(
    *,
    output_directory: str | Path = ROUND179_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND179_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND179_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round179_r8_loop11_platform_content_sw_security_summary.md",
        "case_matrix": output / "round179_r8_loop11_case_matrix.csv",
        "stage_date_plan": output / "round179_r8_loop11_stage_date_plan.csv",
        "green_guardrails": output / "round179_r8_loop11_green_guardrails.md",
        "risk_overlays": output / "round179_r8_loop11_risk_overlays.md",
        "price_validation_plan": output / "round179_r8_loop11_price_validation_plan.md",
        "price_fields": output / "round179_r8_loop11_price_fields.csv",
        "base_score_weights": output / "round179_r8_loop11_base_score_weights.csv",
        "stage_caps": output / "round179_r8_loop11_stage_caps.csv",
        "score_stage_price_alignment": output / "round179_r8_loop11_score_stage_price_alignment.csv",
        "score_stage_price_alignment_md": output / "round179_r8_loop11_score_stage_price_alignment.md",
    }
    _write_case_jsonl(round179_case_records(), cases)
    _write_rows(round179_score_profile_rows(), score_profiles)
    _write_rows(round179_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round179_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round179_price_field_rows(), paths["price_fields"])
    _write_rows(round179_base_score_weight_rows(), paths["base_score_weights"])
    _write_rows(round179_stage_cap_rows(), paths["stage_caps"])
    _write_rows(round179_score_stage_price_alignment_rows(), paths["score_stage_price_alignment"])
    paths["summary"].write_text(render_round179_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round179_green_guardrail_markdown(), encoding="utf-8")
    paths["risk_overlays"].write_text(render_round179_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round179_price_validation_plan_markdown(), encoding="utf-8")
    paths["score_stage_price_alignment_md"].write_text(render_round179_score_stage_price_alignment_markdown(), encoding="utf-8")
    return paths


def render_round179_summary_markdown() -> str:
    summary = round179_summary()
    lines = [
        "# Round-179 R8 Loop-11 Korea Platform / Content / Software / Security Summary",
        "",
        f"- source_round: `{ROUND179_SOURCE_ROUND_PATH}`",
        "- large_sector: `PLATFORM_CONTENT_SW_SECURITY`",
        "- loop: `R8 Loop 11 / v11.0`",
        f"- target_count: {summary['target_count']}",
        f"- source_canonical_target_count: {summary['source_canonical_target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- base_score_component_count: {summary['base_score_component_count']}",
        f"- stage_cap_count: {summary['stage_cap_count']}",
        f"- score_stage_price_alignment_count: {summary['score_stage_price_alignment_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- failed_rerating_count: {summary['failed_rerating_count']}",
        f"- stage4b_case_count: {summary['stage4b_case_count']}",
        f"- stage4c_case_count: {summary['stage4c_case_count']}",
        f"- green_possible_count: {summary['green_possible_count']}",
        f"- watch_yellow_first_count: {summary['watch_yellow_first_count']}",
        f"- redteam_first_count: {summary['redteam_first_count']}",
        f"- gate_only_target_count: {summary['gate_only_target_count']}",
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "",
        "- R8 Loop 11 separates AI/cloud/IP/platform headlines from ARR, bookings, cloud revenue, ad/IP revenue, OPM, FCF, and trust evidence.",
        "- Example: `AI cloud` is Stage 1/2 until paid cloud revenue or ARR appears.",
        "- Example: Samsung SDS KKR CB is strong Stage 2 evidence, but Green waits for AI cloud revenue and dilution absorption.",
        "- Example: `new game IP sold well` can be Stage 2, but Green waits for repeat bookings, retention, OPM, and FCF.",
        "- Example: Webtoon IPO is Stage 2 visibility, but guidance miss and IP adaptation decline become 4C-watch.",
    ]
    return "\n".join(lines) + "\n"


def render_round179_green_guardrail_markdown() -> str:
    lines = [
        "# Round-179 R8 Loop-11 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Loop-11 penalties |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND179_SCORE_TARGETS:
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
            "- Do not apply R8 Loop-11 v11.0 weights to production scoring yet.",
            "- Do not treat AI feature, game IP, Webtoon IPO, K-pop IP, platform MAU, strategic investor, or M&A headline as Green evidence by itself.",
            "- Do not invent ARR, bookings, cloud revenue, ad revenue, IP revenue, OPM, FCF, churn, retention, stage prices, or MFE/MAE.",
            "- Green requires ARR/bookings/revenue evidence, repeatability, OPM/FCF conversion, clean trust/legal status, and price-path support.",
            "- Security incident, privacy leak, founder legal risk, release delay, lawsuit, guidance miss, IP adaptation miss, and platform governance conflict remain RedTeam gates.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round179_risk_overlay_markdown() -> str:
    lines = [
        "# Round-179 R8 Loop-11 Risk Overlays",
        "",
        "- `AI_CLOUD_REVENUE_GATE`: AI cloud option needs paid cloud revenue, ARR, contract, and OPM/FCF.",
        "- `ERP_WORKFLOW_REPEAT_GATE`: ERP/SaaS rerating needs ARR, churn, renewal, OPM, and FCF.",
        "- `SOVEREIGN_AI_MONETIZATION_GATE`: technical report and benchmark remain Stage 1/2 before B2B paid API or cloud usage.",
        "- `GAME_REPEAT_BOOKINGS_GATE`: hit game IP needs live-service bookings, retention, DLC/UGC, and pipeline stability.",
        "- `WEBTOON_GUIDANCE_4C`: Webtoon post-IPO guidance miss or IP adaptation revenue decline blocks unsafe Green.",
        "- `PLATFORM_PRIVACY_SECURITY_4C`: data leak and foreign regulatory pressure hard-cap platform rerating.",
        "- `ENTERTAINMENT_LEGAL_GOVERNANCE_CAP`: founder/legal/governance risk caps K-pop and platform IP.",
        "- `DISCLOSURE_CONFIDENCE_CAP`: ARR, bookings, contract, OPM/FCF, security, and legal detail must be disclosed.",
        "",
        "Simple example: `MAU is large` is useful context. It is not Green if ARPU, ad revenue, OPM, FCF, and privacy/security trust are missing.",
    ]
    return "\n".join(lines) + "\n"


def render_round179_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-179 R8 Loop-11 Price Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign stage dates only from source evidence.",
        "2. Store stage-date close prices from official price data.",
        "3. Calculate 20D/60D/120D/252D returns and MFE/MAE after Stage 2.",
        "4. Compare AI/cloud/IP/platform headlines with ARR, bookings, cloud revenue, ad revenue, paid content, live-service revenue, OPM, FCF, retention, security, legal, and guidance events.",
        "5. Keep missing stage prices and MFE/MAE null until official price backfill is available.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | target | stage marker | check |",
        "| --- | --- | --- | --- |",
    ]
    for row in round179_case_candidate_rows():
        stage_date = row["stage4c_date"] or row["stage4b_date"] or row["stage3_date"] or row["stage2_date"] or row["stage1_date"] or "undated"
        lines.append(f"| `{row['case_id']}` | `{row['target_id']}` | {stage_date} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `AI_CLOUD_CB_STAGE2_NOT_GREEN`: strategic investor and AI option are Stage 2 until AI ARR/revenue confirms.",
            "- `ERP_WORKFLOW_REQUIRES_ARR_CHURN_OPM`: ERP/SaaS needs repeat economics.",
            "- `WEBTOON_GUIDANCE_MISS_BLOCKS_GREEN`: IPO platform premium is broken by weak guidance.",
            "- `GAME_IP_REPEAT_REVENUE_NEEDS_LEGAL_SPLIT`: bookings and legal/release risk must be separated.",
            "- `PRIVACY_SECURITY_GOVERNANCE_GATE`: data leak/regulatory pressure blocks platform Green.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round179_score_stage_price_alignment_markdown() -> str:
    lines = [
        "# Round-179 R8 Loop-11 Score / Stage / Price Alignment",
        "",
        "Round 179 checks whether Korea platform/content/software/security evidence moves from AI, IP, IPO, MAU, and K-pop narratives into ARR, bookings, ad/IP revenue, cloud revenue, OPM, FCF, retention, and clean trust/legal evidence.",
        "This is calibration material only; it does not change production scoring.",
        "",
        "| case | score-stage view | price-path signal | verdict | normalization adjustment |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in ROUND179_SCORE_STAGE_PRICE_ALIGNMENT:
        lines.append(
            "| "
            f"`{item.case_id}` | {item.detected_stage} | {item.price_path_status} | "
            f"{item.verdict} | {item.normalization_adjustment} |"
        )
    lines.extend(
        [
            "",
            "## What This Means",
            "",
            "- Stage 3-Green remains strict. R8 Loop 11 improves Stage 2/3 diagnostics and 4B/4C cooling without weakening Green.",
            "- Samsung SDS is a simple example: KKR and AI cloud support Stage 2, while CB dilution and missing AI ARR keep Green locked.",
            "- Webtoon is a simple example: IPO visibility supports Stage 2, while guidance miss and IP adaptation decline become 4C-watch.",
            "- The same company can have a positive candidate path and a risk overlay. For example, Krafton has PUBG/BGMI/inZOI positives and Subnautica legal/release risk that must be separated.",
        ]
    )
    return "\n".join(lines) + "\n"


def _score_price_alignment(candidate: Round179CaseCandidate) -> str:
    if candidate.case_type == "4c_thesis_break":
        return "false_positive_score"
    if candidate.case_type in {"4b_watch", "overheat", "event_premium"}:
        return "price_moved_without_evidence"
    if candidate.case_type == "failed_rerating":
        return "evidence_good_but_price_failed"
    if candidate.case_type in {"structural_success", "success_candidate"} and "candidate" in candidate.alignment_hint:
        return "aligned"
    return "unknown"


def _rerating_result(candidate: Round179CaseCandidate) -> str:
    if candidate.case_type == "4c_thesis_break":
        return "thesis_break"
    if candidate.case_type in {"4b_watch", "overheat"}:
        return "theme_overheat"
    if candidate.case_type == "event_premium":
        return "event_premium"
    if candidate.case_type == "failed_rerating":
        return "no_rerating"
    if candidate.case_type == "structural_success":
        return "true_rerating"
    return "unknown"


def _score_weight_hint(target: Round179ScoreTarget) -> dict[str, float]:
    weights = target.score_weight.as_dict()
    return {
        "revenue": _numeric_weight(weights["arr_bookings_ad_ip_cloud_revenue"]),
        "recurrence": _numeric_weight(weights["recurrence_retention_workflow_lockin"]),
        "margin_fcf": _numeric_weight(weights["opm_fcf_gross_margin_conversion"]),
        "bottleneck": _numeric_weight(weights["ai_cloud_platform_ip_bottleneck"]),
        "price_validation": _numeric_weight(weights["early_price_path_validation"]),
        "trust_governance": _numeric_weight(weights["operational_trust_security_legal_governance"]),
    }


def _numeric_weight(value: int | str) -> float:
    if isinstance(value, int):
        return float(value)
    return 0.0


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
    "ROUND179_BASE_SCORE_WEIGHTS",
    "ROUND179_CASE_CANDIDATES",
    "ROUND179_DEFAULT_CASES_PATH",
    "ROUND179_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND179_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND179_PRICE_FIELDS",
    "ROUND179_SCORE_STAGE_PRICE_ALIGNMENT",
    "ROUND179_SCORE_TARGETS",
    "ROUND179_SOURCE_CANONICAL_TARGET_COUNT",
    "ROUND179_SOURCE_CANONICAL_TARGET_IDS",
    "ROUND179_STAGE_CAPS",
    "render_round179_green_guardrail_markdown",
    "render_round179_price_validation_plan_markdown",
    "render_round179_risk_overlay_markdown",
    "render_round179_score_stage_price_alignment_markdown",
    "render_round179_summary_markdown",
    "round179_base_score_weight_rows",
    "round179_case_candidate_rows",
    "round179_case_records",
    "round179_price_field_rows",
    "round179_score_profile_rows",
    "round179_score_stage_price_alignment_rows",
    "round179_stage_cap_rows",
    "round179_stage_date_rows",
    "round179_summary",
    "round179_target_for",
    "write_round179_r8_loop11_reports",
]
