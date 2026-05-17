"""Round-53 R13 cross-archetype RedTeam and price-validation pack.

Round 53 is not another industry sector. It is a common validation overlay
for all R1-R12 archetypes: accounting trust, price-only rallies, event
premiums, cycle normalization, crowded 4B, hard 4C, and evidence/price
alignment.

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
from e2r.sector.round10_theme_tag_taxonomy import Round10ThemePosture


ROUND53_SOURCE_ROUND_PATH = "docs/round/round_53.md"
ROUND53_LARGE_SECTOR = "CROSS_ARCHETYPE_REDTEAM_VALIDATION"
ROUND53_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round53_r13_cross_archetype_redteam"
ROUND53_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r13_round53.jsonl"
ROUND53_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round53_r13_v1.csv"


@dataclass(frozen=True)
class Round53OverlayWeightDraft:
    eps_fcf: str
    structural_visibility: str
    bottleneck_pricing: str
    market_mispricing: str
    valuation: str
    capital_allocation: str
    information_confidence: str
    redteam_gate: str

    def as_dict(self) -> dict[str, str]:
        return {
            "eps_fcf": self.eps_fcf,
            "structural_visibility": self.structural_visibility,
            "bottleneck_pricing": self.bottleneck_pricing,
            "market_mispricing": self.market_mispricing,
            "valuation": self.valuation,
            "capital_allocation": self.capital_allocation,
            "information_confidence": self.information_confidence,
            "redteam_gate": self.redteam_gate,
        }


@dataclass(frozen=True)
class Round53OverlayTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round53OverlayWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    validation_role: str
    normalization_point: str
    hard_gate: bool = False
    stage3_green_allowed: bool = False

    @property
    def large_sector(self) -> str:
        return ROUND53_LARGE_SECTOR

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round53CaseCandidate:
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


ROUND53_OVERLAY_TARGETS: tuple[Round53OverlayTarget, ...] = (
    Round53OverlayTarget(
        "REDTEAM_ACCOUNTING_TRUST_OVERLAY",
        E2RArchetype.REDTEAM_ACCOUNTING_TRUST_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        Round53OverlayWeightDraft("gate", "gate", "gate", "hard-", "hard-", "gate", "hard-", "hard_block"),
        ("auditor_resignation", "filing_delay", "internal_control_issue"),
        ("restatement", "related_party_risk", "regulatory_probe"),
        ("not_applicable_until_trust_restored",),
        ("accounting_risk_ignored_during_rerating",),
        ("auditor_resignation", "filing_delay", "restatement", "probe_or_management_unreliable"),
        (),
        ("auditor_resignation", "filing_delay", "internal_control_issue", "related_party_risk"),
        "Hard RedTeam gate for accounting/audit trust failures.",
        "High score is invalid when accounting trust breaks.",
        hard_gate=True,
    ),
    Round53OverlayTarget(
        "FINANCIAL_REPORTING_INTEGRITY_RISK",
        E2RArchetype.FINANCIAL_REPORTING_INTEGRITY_RISK,
        Round10ThemePosture.REDTEAM_FIRST,
        Round53OverlayWeightDraft("gate", "gate", "gate", "hard-", "hard-", "0", "hard-", "hard_block"),
        ("late_filing", "material_weakness", "control_deficiency"),
        ("restatement_risk", "going_concern_warning", "qualified_opinion"),
        ("not_applicable_until_reporting_integrity_restored",),
        ("reporting_delay_normalized_by_market",),
        ("qualified_opinion", "material_weakness", "restatement", "going_concern"),
        (),
        ("late_filing", "material_weakness", "restatement", "qualified_opinion"),
        "Hard RedTeam gate for financial-reporting integrity.",
        "Numbers cannot support Stage 3-Green if reporting integrity is broken.",
        hard_gate=True,
    ),
    Round53OverlayTarget(
        "PRICE_ONLY_RALLY",
        E2RArchetype.PRICE_ONLY_RALLY,
        Round10ThemePosture.REDTEAM_FIRST,
        Round53OverlayWeightDraft("0", "0", "0", "-", "-", "0", "-", "green_block"),
        ("price_spike", "sns_theme", "headline_without_numbers"),
        ("no_eps_revision", "no_contract_or_revenue", "no_disclosure_support"),
        ("not_green_without_eps_fcf_and_cross_evidence",),
        ("price_only_4b_watch", "retail_crowding"),
        ("price_reversal", "theme_fade", "no_revenue_conversion"),
        (),
        ("no_eps_fcf", "no_contract", "no_revenue", "theme_only"),
        "Green blocker for price-only moves.",
        "Price can route attention, but it is not structural evidence.",
    ),
    Round53OverlayTarget(
        "EVENT_PREMIUM",
        E2RArchetype.EVENT_PREMIUM,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round53OverlayWeightDraft("0", "+", "0", "0", "0", "0", "+", "event_split"),
        ("tender_offer", "control_battle", "policy_announcement", "mou", "disaster_or_disease_event"),
        ("binding_contract", "funded_budget", "actual_order", "guide_up"),
        ("repeat_contract_or_revenue_plus_eps_fcf",),
        ("event_premium_crowded", "expected_deal_priced"),
        ("event_fade", "deal_failure", "budget_missing", "one_off_demand_normalization"),
        ("binding_contract", "actual_order", "eps_fcf_conversion"),
        ("mou_only", "policy_only", "event_only", "deal_failure"),
        "Separates event premium from structural rerating.",
        "An event can become Stage 2 only when it converts into orders, budget, or earnings.",
    ),
    Round53OverlayTarget(
        "CYCLICAL_SUCCESS",
        E2RArchetype.CYCLICAL_SUCCESS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round53OverlayWeightDraft("+", "0", "+", "0", "-", "0", "+", "cycle_cap"),
        ("freight_rate_spike", "commodity_spread", "refining_margin", "livestock_price"),
        ("op_eps_spike", "cost_spread_confirmed", "cash_generation"),
        ("cycle_durability_and_supply_discipline_required",),
        ("cycle_peak_crowded", "spot_price_peak"),
        ("spread_reversal", "freight_rate_crash", "inventory_build", "capacity_addition"),
        ("multi_period_margin_stability", "supply_discipline"),
        ("normalization_risk", "new_supply", "spot_price_reversal"),
        "Classifies valid cycle wins without calling them structural Green too early.",
        "Cycle success can be real, but Green needs durability beyond spot prices.",
    ),
    Round53OverlayTarget(
        "STRUCTURAL_SUCCESS_ALIGNED",
        E2RArchetype.STRUCTURAL_SUCCESS_ALIGNED,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round53OverlayWeightDraft("+", "+", "+", "+", "+", "+", "+", "pass_if_no_redteam"),
        ("industry_structure_change", "official_disclosure_or_report", "price_attention"),
        ("contract_order_revenue_or_revision", "eps_fcf_bodyweight_change", "cross_evidence"),
        ("price_path_aligned", "medium_term_eps_fcf_revision", "valuation_frame_change", "no_hard_redteam"),
        ("crowded_new_frame", "valuation_saturation", "revision_slowdown"),
        ("hard_redteam", "thesis_break", "eps_fcf_revision_down"),
        ("eps_fcf_bodyweight_change", "cross_evidence", "price_path_aligned", "no_hard_redteam"),
        ("crowded_4b", "valuation_saturation", "revision_slowdown"),
        "Positive validation overlay for true structural rerating cases.",
        "High score survives only when evidence, price path, and RedTeam all align.",
        stage3_green_allowed=True,
    ),
    Round53OverlayTarget(
        "EVIDENCE_GOOD_BUT_PRICE_FAILED",
        E2RArchetype.EVIDENCE_GOOD_BUT_PRICE_FAILED,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round53OverlayWeightDraft("+", "+", "+", "-", "-", "0", "+", "alignment_review"),
        ("strong_disclosure", "solid_report", "eps_revision"),
        ("no_rerating", "price_underperforms_peer", "liquidity_or_frame_stuck"),
        ("requires_mispricing_diagnosis_not_green_promotion",),
        ("market_frame_not_changed",),
        ("evidence_not_monetized", "valuation_frame_stuck", "price_below_stage3"),
        ("additional_price_or_revision_confirmation",),
        ("price_failed", "valuation_frame_stuck", "liquidity_low"),
        "Autopsy bucket when evidence looked good but price never validated the thesis.",
        "Useful for recalibrating market-mispricing and valuation scores.",
    ),
    Round53OverlayTarget(
        "FALSE_POSITIVE_SCORE",
        E2RArchetype.FALSE_POSITIVE_SCORE,
        Round10ThemePosture.REDTEAM_FIRST,
        Round53OverlayWeightDraft("-", "-", "-", "-", "-", "0", "-", "score_recalibration"),
        ("high_score_without_actual_evidence", "proxy_score_overfit"),
        ("earnings_miss", "no_price_validation", "redteam_ignored"),
        ("not_applicable_until_score_axis_fixed",),
        ("false_positive_crowding",),
        ("price_failed", "earnings_failed", "audit_or_redteam_ignored"),
        (),
        ("score_overfit", "no_eps_fcf", "price_failed", "redteam_ignored"),
        "Score calibration bucket for high-score failures.",
        "Example: a candidate scores high from keywords but misses earnings and price validation.",
    ),
    Round53OverlayTarget(
        "CROWDED_RERATING_4B_WATCH",
        E2RArchetype.CROWDED_RERATING_4B_WATCH,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round53OverlayWeightDraft("+", "+", "0", "-", "-", "0", "+", "stage4b_watch"),
        ("large_12m_24m_return", "universally_bullish_reports", "target_multiple_expansion"),
        ("valuation_band_saturated", "revision_momentum_slowing", "capacity_or_new_entrant_news"),
        ("not_new_green_unlock",),
        ("4b_watch", "4b_elevated", "4b_graduated"),
        ("revision_down", "demand_slowdown", "capex_overbuild", "margin_peak"),
        ("fundamentals_intact_but_mispricing_reduced",),
        ("crowding", "valuation_saturation", "revision_slowdown", "capacity_addition"),
        "4B watch overlay for candidates whose fundamentals may remain intact but mispricing is gone.",
        "4B is monitoring language, not a new buy/sell instruction.",
    ),
    Round53OverlayTarget(
        "THESIS_BREAK_4C",
        E2RArchetype.THESIS_BREAK_4C,
        Round10ThemePosture.REDTEAM_FIRST,
        Round53OverlayWeightDraft("hard-", "hard-", "hard-", "hard-", "hard-", "hard-", "hard-", "hard_downgrade"),
        ("contract_cancellation", "order_cut", "regulatory_denial", "demand_crash"),
        ("eps_revision_down", "margin_break", "customer_capex_cut", "depeg_or_reserve_failure"),
        ("not_applicable_after_thesis_break",),
        ("ignored_thesis_break",),
        ("hard_4c", "stage_downgrade", "green_block"),
        (),
        ("contract_cancellation", "order_cut", "regulatory_denial", "demand_crash", "trust_break"),
        "Hard thesis-break overlay.",
        "When core evidence breaks, Stage must be downgraded rather than explained away.",
        hard_gate=True,
    ),
    Round53OverlayTarget(
        "LEGAL_REGULATORY_REDTEAM",
        E2RArchetype.LEGAL_REGULATORY_REDTEAM,
        Round10ThemePosture.REDTEAM_FIRST,
        Round53OverlayWeightDraft("gate", "gate", "0", "-", "-", "0", "-", "hard_review"),
        ("lawsuit", "regulatory_probe", "license_risk", "approval_denial"),
        ("fine_or_restriction", "commercialization_blocked", "export_approval_issue"),
        ("not_green_until_legal_scope_resolved",),
        ("legal_risk_ignored_by_rally",),
        ("approval_denial", "license_revocation", "injunction", "regulatory_sanction"),
        (),
        ("lawsuit", "regulatory_probe", "approval_denial", "license_risk"),
        "Legal/regulatory RedTeam overlay.",
        "Regulatory clearance and commercial scope must be verified before Green.",
        hard_gate=True,
    ),
    Round53OverlayTarget(
        "OPERATIONAL_TRUST_BREAK",
        E2RArchetype.OPERATIONAL_TRUST_BREAK,
        Round10ThemePosture.REDTEAM_FIRST,
        Round53OverlayWeightDraft("gate", "gate", "0", "hard-", "hard-", "0", "hard-", "hard_review"),
        ("security_outage", "privacy_breach", "customer_damage", "platform_safety_incident"),
        ("customer_lawsuit", "renewal_risk", "service_level_break"),
        ("trust_restoration_and_retention_required",),
        ("trust_break_ignored_by_growth_story",),
        ("customer_churn", "lawsuit_damage", "renewal_decline", "brand_trust_loss"),
        (),
        ("security_outage", "privacy_breach", "customer_lawsuit", "operational_trust_damage"),
        "Operational trust-break overlay.",
        "A growth story cannot stay Green if the product damages customers or trust.",
        hard_gate=True,
    ),
    Round53OverlayTarget(
        "LEVERAGE_FCF_BREAKDOWN",
        E2RArchetype.LEVERAGE_FCF_BREAKDOWN,
        Round10ThemePosture.REDTEAM_FIRST,
        Round53OverlayWeightDraft("hard-", "-", "0", "-", "-", "hard-", "-", "green_block"),
        ("negative_fcf", "cash_runway_short", "refinancing_need", "high_debt_to_ebitda"),
        ("dividend_cut", "buyback_cancelled", "distressed_financing", "take_private_discount"),
        ("not_green_without_fcf_and_balance_sheet_repair",),
        ("growth_story_ignores_funding_need",),
        ("cash_runway_collapse", "going_concern", "refinancing_failure", "dilution"),
        (),
        ("negative_fcf", "cash_runway", "refinancing", "dilution", "dividend_cut"),
        "Leverage and FCF breakdown overlay.",
        "Approval, growth, or demand does not equal E2R if cash runway and FCF break.",
        hard_gate=True,
    ),
    Round53OverlayTarget(
        "UNKNOWN_INSUFFICIENT_EVIDENCE",
        E2RArchetype.UNKNOWN_INSUFFICIENT_EVIDENCE,
        Round10ThemePosture.REDTEAM_FIRST,
        Round53OverlayWeightDraft("0", "0", "0", "0", "0", "0", "0", "green_block"),
        ("undated_document", "single_source_claim", "missing_price_or_financials"),
        ("evidence_gap", "unverified_publish_date", "missing_official_confirmation"),
        ("not_green_until_evidence_gap_closed",),
        ("unknown_story_priced_as_fact",),
        ("missing_evidence", "date_unverified", "source_unverified"),
        (),
        ("missing_evidence", "date_unverified", "single_source", "unknown"),
        "Explicit bucket for insufficient evidence.",
        "Unknown is a valid output; do not fill missing evidence.",
    ),
)


ROUND53_CASE_CANDIDATES: tuple[Round53CaseCandidate, ...] = (
    Round53CaseCandidate(
        "sk_hynix_hbm_memory_aligned_4b_watch_case",
        "STRUCTURAL_SUCCESS_ALIGNED",
        "000660",
        "SK하이닉스",
        "KR",
        "structural_success",
        date(2025, 1, 1),
        date(2026, 5, 7),
        date(2026, 5, 14),
        date(2026, 5, 14),
        None,
        ("hbm_demand", "memory_bottleneck", "eps_fcf_revision", "price_rerating", "valuation_frame_change"),
        ("crowded_4b", "capex_expansion", "customer_price_resistance"),
        "structural_success_aligned_but_4b_watch",
        "needs_price_backfill",
        ("round_53.md Reuters SK Hynix chip supply offers", "round_53.md Reuters AI boom market value"),
        "HBM/memory rerating is a structural-aligned case, but Round53 flags crowded 4B watch.",
        (E2RArchetype.MEMORY_HBM_CAPACITY, E2RArchetype.CROWDED_RERATING_4B_WATCH),
    ),
    Round53CaseCandidate(
        "hyundai_motor_valueup_strategy_aligned_case",
        "STRUCTURAL_SUCCESS_ALIGNED",
        "005380",
        "현대차",
        "KR",
        "success_candidate",
        date(2024, 8, 28),
        date(2024, 8, 28),
        None,
        None,
        None,
        ("hybrid_mix", "sales_target_2030", "buyback", "dividend", "fcf_sustainability"),
        ("tariff_risk", "peak_margin", "execution_risk"),
        "strategy_valueup_aligned_requires_fcf_validation",
        "needs_price_backfill",
        ("round_53.md Reuters Hyundai strategy and buyback",),
        "Value-up plus hybrid strategy can align, but Green still needs FCF and execution evidence.",
        (E2RArchetype.AUTO_MOBILITY_COMPLETED_VEHICLE, E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN),
    ),
    Round53CaseCandidate(
        "event_to_contract_escalation_case",
        "EVENT_PREMIUM",
        "EVENT_TO_CONTRACT",
        "event-to-contract reference case",
        "GLOBAL",
        "event_premium",
        None,
        None,
        None,
        None,
        None,
        ("event_news", "stockpile_contract", "guide_up"),
        ("one_off_event", "repeat_contract_unproven"),
        "event_premium_converts_to_stage2_only_after_contract",
        "needs_price_backfill",
        ("round_53.md event-to-contract rule",),
        "Disease or disaster news can route attention, but only a contract/order upgrades it.",
        (E2RArchetype.ONE_OFF_EVENT_DEMAND,),
    ),
    Round53CaseCandidate(
        "supermicro_accounting_trust_4c_case",
        "REDTEAM_ACCOUNTING_TRUST_OVERLAY",
        "SMCI",
        "Super Micro Computer",
        "US",
        "4c_thesis_break",
        date(2024, 1, 1),
        None,
        None,
        None,
        date(2024, 10, 30),
        ("ai_server_rerating", "prior_price_rally"),
        ("auditor_resignation", "filing_delay", "internal_control_issue", "related_party_risk", "regulatory_probe"),
        "early_rerating_success_then_hard_4c",
        "needs_price_backfill",
        ("round_53.md SMCI EY resignation/Hindenburg/DOJ discussion",),
        "Accounting trust failure is a hard RedTeam gate even after a strong AI rerating.",
        (E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE, E2RArchetype.THESIS_BREAK_4C),
    ),
    Round53CaseCandidate(
        "crowdstrike_operational_trust_break_case",
        "OPERATIONAL_TRUST_BREAK",
        "CRWD",
        "CrowdStrike",
        "US",
        "4c_thesis_break",
        date(2024, 7, 19),
        None,
        None,
        None,
        date(2024, 7, 31),
        ("security_platform_growth", "large_customer_base"),
        ("global_outage", "customer_damage", "customer_lawsuit", "trust_damage", "renewal_risk"),
        "operational_trust_break_4c",
        "needs_price_backfill",
        ("round_53.md CrowdStrike outage and customer damage",),
        "A security outage can turn a growth story into operational trust RedTeam.",
        (E2RArchetype.SECURITY_IDENTITY_DEEPFAKE, E2RArchetype.THESIS_BREAK_4C),
    ),
    Round53CaseCandidate(
        "terrausd_luna_algorithmic_stablecoin_break_case",
        "THESIS_BREAK_4C",
        "LUNA",
        "TerraUSD/Luna",
        "CRYPTO",
        "4c_thesis_break",
        date(2022, 5, 7),
        None,
        None,
        None,
        date(2022, 5, 12),
        ("algorithmic_stablecoin_growth", "crypto_liquidity"),
        ("depeg_event", "reserve_failure", "convertibility_failure", "run_risk", "fraud_risk"),
        "algorithmic_stablecoin_thesis_break",
        "needs_price_backfill",
        ("round_53.md TerraUSD/Luna hard 4C pattern",),
        "Depeg/reserve/convertibility failure is a hard thesis break.",
        (E2RArchetype.DIGITAL_ASSET_TOKENIZATION, E2RArchetype.LEGAL_REGULATORY_REDTEAM),
    ),
    Round53CaseCandidate(
        "bluebird_bio_approval_commercialization_failure_case",
        "LEVERAGE_FCF_BREAKDOWN",
        "BLUE",
        "bluebird bio",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        date(2025, 2, 21),
        ("gene_therapy_approval", "rare_disease_treatment"),
        ("cash_crunch", "slow_uptake", "reimbursement_uncertainty", "take_private_discount"),
        "approval_without_commercialization_or_cash_runway",
        "needs_price_backfill",
        ("round_53.md bluebird approval and cash runway failure",),
        "Approval alone is not EPS/FCF; commercialization and cash runway must support the case.",
        (E2RArchetype.BIOTECH_PRE_REVENUE_REGULATORY, E2RArchetype.BIOTECH_ROYALTY_COMMERCIALIZATION),
    ),
    Round53CaseCandidate(
        "novo_nordisk_glp1_4b_to_4c_case",
        "CROWDED_RERATING_4B_WATCH",
        "NOVO",
        "Novo Nordisk",
        "GLOBAL",
        "4c_thesis_break",
        date(2024, 1, 1),
        None,
        None,
        date(2025, 7, 29),
        date(2026, 2, 4),
        ("glp1_tam", "growth_stock_rerating", "pricing_power"),
        ("sales_guide_down", "op_guide_down", "price_pressure", "competition", "copycat_risk"),
        "crowded_4b_then_4c_when_growth_revision_breaks",
        "needs_price_backfill",
        ("round_53.md Novo GLP-1 guide down and 4B/4C pattern",),
        "A crowded growth winner can move from 4B watch to 4C when revisions break.",
        (E2RArchetype.OBESITY_GLP1_COMMERCIALIZATION, E2RArchetype.THESIS_BREAK_4C),
    ),
    Round53CaseCandidate(
        "price_only_theme_rally_case",
        "PRICE_ONLY_RALLY",
        "PRICE_ONLY",
        "price-only theme reference case",
        "GLOBAL",
        "overheat",
        None,
        None,
        None,
        None,
        None,
        ("price_spike", "theme_news", "sns_attention"),
        ("no_eps_fcf", "no_contract", "no_revenue", "theme_only"),
        "price_moved_without_evidence",
        "needs_price_backfill",
        ("round_53.md price-only rally definition",),
        "A price-only rally is useful for detection but cannot create Stage 3-Green.",
        (E2RArchetype.THEME_VALUATION_OVERHEAT,),
    ),
    Round53CaseCandidate(
        "cyclical_success_peak_normalization_case",
        "CYCLICAL_SUCCESS",
        "CYCLE_PEAK",
        "cycle peak reference case",
        "GLOBAL",
        "cyclical_success",
        None,
        None,
        None,
        None,
        None,
        ("freight_or_commodity_peak", "eps_spike", "margin_peak"),
        ("normalization_risk", "capacity_addition", "demand_slowdown"),
        "cyclical_success_not_structural_green",
        "needs_price_backfill",
        ("round_53.md cyclical success rule",),
        "Cycle wins can be valid but should not be mislabeled as structural Green.",
        (E2RArchetype.SHIPPING_FREIGHT_CYCLE, E2RArchetype.COMMODITY_SPREAD),
    ),
    Round53CaseCandidate(
        "evidence_good_but_price_failed_case",
        "EVIDENCE_GOOD_BUT_PRICE_FAILED",
        "EVIDENCE_PRICE_FAIL",
        "evidence-price mismatch reference case",
        "GLOBAL",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("actual_order", "eps_revision", "solid_report"),
        ("price_failed", "valuation_frame_stuck", "liquidity_low"),
        "evidence_good_but_price_failed",
        "needs_price_backfill",
        ("round_53.md evidence-good price-failed rule",),
        "Good evidence without price-frame validation should recalibrate mispricing, not force Green.",
    ),
    Round53CaseCandidate(
        "unknown_insufficient_evidence_case",
        "UNKNOWN_INSUFFICIENT_EVIDENCE",
        "UNKNOWN_EVIDENCE",
        "insufficient evidence reference case",
        "GLOBAL",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("single_source_claim",),
        ("date_unverified", "missing_official_confirmation", "missing_price_data"),
        "unknown_insufficient_evidence",
        "needs_price_backfill",
        ("round_53.md insufficient evidence rule",),
        "Unknown evidence must remain unknown; missing fields are not filled.",
    ),
    Round53CaseCandidate(
        "financial_reporting_integrity_delay_case",
        "FINANCIAL_REPORTING_INTEGRITY_RISK",
        "REPORT_DELAY",
        "financial reporting delay reference case",
        "GLOBAL",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        None,
        ("prior_growth_story",),
        ("late_filing", "material_weakness", "qualified_opinion"),
        "financial_reporting_integrity_hard_gate",
        "needs_price_backfill",
        ("round_53.md reporting integrity risk rule",),
        "Financial-reporting delay and control weakness block evidence confidence.",
    ),
    Round53CaseCandidate(
        "legal_regulatory_redteam_denial_case",
        "LEGAL_REGULATORY_REDTEAM",
        "REG_DENIAL",
        "legal/regulatory denial reference case",
        "GLOBAL",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        None,
        ("approval_or_license_story",),
        ("regulatory_denial", "license_risk", "commercialization_blocked"),
        "legal_regulatory_redteam_hard_review",
        "needs_price_backfill",
        ("round_53.md legal/regulatory RedTeam rule",),
        "Approval, license, and legal scope must be verified before evidence supports Green.",
    ),
    Round53CaseCandidate(
        "false_positive_score_high_score_failure_case",
        "FALSE_POSITIVE_SCORE",
        "FALSE_SCORE",
        "false positive score reference case",
        "GLOBAL",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("high_keyword_score", "thin_proxy_score"),
        ("no_eps_fcf", "price_failed", "earnings_failed", "redteam_ignored"),
        "false_positive_score",
        "needs_price_backfill",
        ("round_53.md false-positive score rule",),
        "High score from weak proxies should be treated as calibration failure.",
    ),
)


ROUND53_PRICE_FIELDS: tuple[str, ...] = (
    "case_id",
    "symbol",
    "company_name",
    "market",
    "primary_sector_round",
    "primary_archetype",
    "secondary_archetypes",
    "case_type",
    "stage1_date",
    "stage2_date",
    "stage3_date",
    "stage4b_date",
    "stage4c_date",
    "stage1_evidence_type",
    "stage2_evidence_type",
    "stage3_evidence_type",
    "stage4b_evidence_type",
    "stage4c_evidence_type",
    "stage1_price",
    "stage2_price",
    "stage3_price",
    "stage4b_price",
    "stage4c_price",
    "peak_price",
    "peak_date",
    "mfe_5d",
    "mfe_20d",
    "mfe_30d",
    "mfe_60d",
    "mfe_90d",
    "mfe_180d",
    "mfe_1y",
    "mfe_2y",
    "mae_5d",
    "mae_20d",
    "mae_30d",
    "mae_60d",
    "mae_90d",
    "mae_180d",
    "mae_1y",
    "drawdown_after_peak",
    "below_stage1_price_flag",
    "below_stage2_price_flag",
    "below_stage3_price_flag",
    "revenue_revision_1q",
    "op_revision_1q",
    "eps_revision_1q",
    "fcf_revision_1q",
    "revenue_revision_1y",
    "op_revision_1y",
    "eps_revision_1y",
    "fcf_revision_1y",
    "gross_margin_change",
    "op_margin_change",
    "per_before",
    "per_after",
    "pbr_before",
    "pbr_after",
    "ev_ebitda_before",
    "ev_ebitda_after",
    "contract_value",
    "contract_duration",
    "contract_amount_to_sales",
    "backlog_to_sales",
    "capacity_utilization",
    "customer_concentration",
    "debt_to_ebitda",
    "net_debt",
    "interest_expense",
    "cash_runway",
    "refinancing_need",
    "dividend_cut",
    "buyback_cancelled",
    "auditor_resignation_flag",
    "filing_delay_flag",
    "internal_control_issue_flag",
    "regulatory_probe_flag",
    "related_party_flag",
    "security_outage_flag",
    "privacy_breach_flag",
    "customer_lawsuit_flag",
    "operational_trust_break_flag",
    "depeg_event_flag",
    "reserve_failure_flag",
    "convertibility_failure_flag",
    "event_premium_flag",
    "cycle_success_flag",
    "price_only_flag",
    "crowded_4b_flag",
    "hard_4c_flag",
    "score_before_redteam",
    "score_after_redteam",
    "stage_before_redteam",
    "stage_after_redteam",
    "score_price_alignment",
    "price_validation_status",
    "review_notes",
)


def target_for(target_id: str) -> Round53OverlayTarget | None:
    for target in ROUND53_OVERLAY_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round53_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND53_CASE_CANDIDATES:
        target = target_for(candidate.target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {candidate.target_id}")
        record = E2RCaseRecord(
            case_id=candidate.case_id,
            symbol=candidate.symbol,
            company_name=candidate.company_name,
            market=candidate.market,
            sector_raw=candidate.target_id,
            primary_archetype=target.canonical_archetype,
            secondary_archetypes=candidate.secondary_archetypes,
            expected_group=candidate.expected_group,
            large_sector=target.large_sector,
            case_type=candidate.case_type,
            stage1_date=candidate.stage1_date,
            stage2_date=candidate.stage2_date,
            stage3_date=candidate.stage3_date,
            stage4b_date=candidate.stage4b_date,
            stage4c_date=candidate.stage4c_date,
            evidence_summary=(
                f"Round53 R13 cross-archetype validation case for {candidate.target_id}; "
                "the overlay is calibration-only and does not change production scoring."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage2_signals),
            stage3_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage3_conditions or field in target.green_conditions),
            stage4b_evidence=candidate.evidence_fields if candidate.stage4b_date or candidate.target_id == "CROWDED_RERATING_4B_WATCH" else (),
            stage4c_evidence=candidate.red_flag_fields if candidate.stage4c_date or target.hard_gate else (),
            must_have_fields=target.green_conditions,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason=(
                "; ".join(candidate.red_flag_fields)
                if candidate.case_type in {"event_premium", "overheat", "failed_rerating", "4b_watch", "4c_thesis_break", "one_off"}
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
                "stage3_green_requires_cross_evidence_eps_fcf_price_alignment_no_hard_redteam",
                "price_only_rally_is_not_green_evidence",
                "hard_redteam_blocks_green",
                "unknown_evidence_stays_unknown",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=False,
                price_data_available=False,
                stage_dates_confidence=0.7 if candidate.stage1_date or candidate.stage2_date or candidate.stage4b_date or candidate.stage4c_date else 0.25,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round53_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND53_OVERLAY_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "eps_fcf": weights["eps_fcf"],
                "structural_visibility": weights["structural_visibility"],
                "bottleneck_pricing": weights["bottleneck_pricing"],
                "market_mispricing": weights["market_mispricing"],
                "valuation": weights["valuation"],
                "capital_allocation": weights["capital_allocation"],
                "information_confidence": weights["information_confidence"],
                "redteam_gate": weights["redteam_gate"],
                "stage1_signals": "|".join(target.stage1_signals),
                "stage2_signals": "|".join(target.stage2_signals),
                "stage3_conditions": "|".join(target.stage3_conditions),
                "stage4b_conditions": "|".join(target.stage4b_conditions),
                "stage4c_conditions": "|".join(target.stage4c_conditions),
                "green_conditions": "|".join(target.green_conditions),
                "red_flags": "|".join(target.red_flags),
                "validation_role": target.validation_role,
                "hard_gate": str(target.hard_gate).lower(),
                "stage3_green_allowed": str(target.stage3_green_allowed).lower(),
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round53_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND53_CASE_CANDIDATES:
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


def round53_stage_date_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "target_id": target.target_id,
            "stage1": "|".join(target.stage1_signals),
            "stage2": "|".join(target.stage2_signals),
            "stage3": "|".join(target.stage3_conditions),
            "stage4b": "|".join(target.stage4b_conditions),
            "stage4c": "|".join(target.stage4c_conditions),
            "hard_gate": str(target.hard_gate).lower(),
            "production_scoring_changed": "false",
        }
        for target in ROUND53_OVERLAY_TARGETS
    )


def round53_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round53_backfill": "true"} for field in ROUND53_PRICE_FIELDS)


def round53_summary() -> dict[str, int | bool]:
    records = round53_case_records()
    return {
        "target_count": len(ROUND53_OVERLAY_TARGETS),
        "case_candidate_count": len(records),
        "structural_success_count": sum(1 for record in records if record.case_type == "structural_success"),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for record in records if record.case_type == "cyclical_success"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "overheat_count": sum(1 for record in records if record.case_type == "overheat"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "hard_gate_target_count": sum(1 for target in ROUND53_OVERLAY_TARGETS if target.hard_gate),
        "green_possible_count": sum(1 for target in ROUND53_OVERLAY_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND53_OVERLAY_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND53_OVERLAY_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round53_r13_reports(
    *,
    output_directory: str | Path = ROUND53_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND53_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND53_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round53_r13_cross_archetype_redteam_summary.md",
        "case_matrix": output / "round53_r13_case_matrix.csv",
        "target_matrix": output / "round53_r13_overlay_target_matrix.csv",
        "stage_date_plan": output / "round53_r13_stage_date_plan.csv",
        "redteam_gate_plan": output / "round53_r13_redteam_gate_plan.md",
        "price_validation_plan": output / "round53_r13_price_validation_plan.md",
        "price_fields": output / "round53_r13_price_fields.csv",
    }
    _write_case_jsonl(round53_case_records(), cases)
    _write_rows(round53_score_profile_rows(), score_profiles)
    _write_rows(round53_score_profile_rows(), paths["target_matrix"])
    _write_rows(round53_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round53_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round53_price_field_rows(), paths["price_fields"])
    paths["summary"].write_text(render_round53_summary_markdown(), encoding="utf-8")
    paths["redteam_gate_plan"].write_text(render_round53_redteam_gate_plan_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round53_price_validation_plan_markdown(), encoding="utf-8")
    return paths


def render_round53_summary_markdown() -> str:
    summary = round53_summary()
    lines = [
        "# Round-53 R13 Cross-Archetype RedTeam / 4B / 4C Summary",
        "",
        f"- source_round: `{ROUND53_SOURCE_ROUND_PATH}`",
        f"- large_sector: `{ROUND53_LARGE_SECTOR}`",
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
        f"- hard_gate_target_count: {summary['hard_gate_target_count']}",
        f"- green_possible_count: {summary['green_possible_count']}",
        f"- watch_yellow_first_count: {summary['watch_yellow_first_count']}",
        f"- redteam_first_count: {summary['redteam_first_count']}",
        "- production_scoring_changed: false",
        "- case_records_are_candidate_generation_input: false",
        "",
        "## Interpretation",
        "",
        "- R13 is a common validation overlay, not a sector score-owner.",
        "- High score is not enough. The score must align with EPS/FCF evidence, price-path validation, and no hard RedTeam.",
        "- Example: a memory/HBM winner can be structurally aligned and still move into 4B watch when the new frame is crowded.",
        "- Example: auditor resignation or filing delay is a hard gate. A prior AI-server rerating does not rescue Stage 3-Green.",
        "- Example: price-only rallies can route attention, but they stay Green-blocked until official or report evidence proves EPS/FCF.",
    ]
    return "\n".join(lines) + "\n"


def render_round53_redteam_gate_plan_markdown() -> str:
    lines = [
        "# Round-53 R13 RedTeam Gate Plan",
        "",
        "| target | posture | hard gate | Green allowed | Red flags |",
        "| --- | --- | --- | --- | --- |",
    ]
    for target in ROUND53_OVERLAY_TARGETS:
        lines.append(
            "| "
            f"`{target.target_id}` | {target.posture.value} | {str(target.hard_gate).lower()} | "
            f"{str(target.stage3_green_allowed).lower()} | {', '.join(target.red_flags)} |"
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not apply Round53 overlay symbols to production scoring yet.",
            "- Do not lower Stage 3-Green to improve recall.",
            "- Do not use R13 case records as candidate-generation input.",
            "- Do not treat price-only movement, event premium, or cycle success as structural Green by itself.",
            "- Do not ignore hard RedTeam evidence such as auditor resignation, filing delay, regulatory denial, operational trust break, cash runway collapse, or hard thesis break.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round53_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-53 R13 Price / Stage Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign Stage 1/2/3/4B/4C dates only from dated evidence.",
        "2. Store stage-date close prices from official price data.",
        "3. Calculate MFE_5D / 20D / 30D / 60D / 90D / 180D / 1Y / 2Y.",
        "4. Calculate MAE_5D / 20D / 30D / 60D / 90D / 180D / 1Y.",
        "5. Compare score-before-RedTeam vs score-after-RedTeam and stage-before-RedTeam vs stage-after-RedTeam.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | target | stage marker | check |",
        "| --- | --- | --- | --- |",
    ]
    for row in round53_case_candidate_rows():
        stage_date = row["stage4c_date"] or row["stage4b_date"] or row["stage3_date"] or row["stage2_date"] or row["stage1_date"] or "undated"
        lines.append(f"| `{row['case_id']}` | `{row['target_id']}` | {stage_date} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `aligned`: EPS/FCF, structural evidence, and price path validate together.",
            "- `price_moved_without_evidence`: price or event moved first, but EPS/FCF evidence is absent.",
            "- `evidence_good_but_price_failed`: evidence looked valid, but price/valuation frame did not confirm.",
            "- `false_positive_score`: model score was high but earnings, price, or RedTeam later invalidated it.",
            "- `thesis_break`: 4C evidence such as audit, trust, legal, cash runway, or demand break appears.",
        ]
    )
    return "\n".join(lines) + "\n"


def _score_price_alignment(candidate: Round53CaseCandidate) -> str:
    if "insufficient" in candidate.alignment_hint:
        return "unknown"
    if "evidence_good_but_price_failed" in candidate.alignment_hint:
        return "evidence_good_but_price_failed"
    if candidate.case_type in {"structural_success", "success_candidate", "cyclical_success"}:
        return "aligned"
    if candidate.case_type in {"event_premium", "overheat", "4b_watch"}:
        return "price_moved_without_evidence"
    return "false_positive_score"


def _rerating_result(candidate: Round53CaseCandidate) -> str:
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
    return "unknown" if "insufficient" in candidate.alignment_hint else "no_rerating"


def _score_weight_hint(target: Round53OverlayTarget) -> dict[str, float]:
    weights = target.score_weight.as_dict()
    return {
        "eps_fcf": _symbolic_weight(weights["eps_fcf"]),
        "visibility": _symbolic_weight(weights["structural_visibility"]),
        "bottleneck": _symbolic_weight(weights["bottleneck_pricing"]),
        "mispricing": _symbolic_weight(weights["market_mispricing"]),
        "valuation": _symbolic_weight(weights["valuation"]),
        "capital_allocation": _symbolic_weight(weights["capital_allocation"]),
        "information_confidence": _symbolic_weight(weights["information_confidence"]),
    }


def _symbolic_weight(value: str) -> float:
    return {
        "+": 1.0,
        "0": 0.0,
        "-": -1.0,
        "gate": 0.0,
        "hard-": -5.0,
    }.get(value, 0.0)


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
    "ROUND53_CASE_CANDIDATES",
    "ROUND53_DEFAULT_CASES_PATH",
    "ROUND53_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND53_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND53_LARGE_SECTOR",
    "ROUND53_OVERLAY_TARGETS",
    "ROUND53_PRICE_FIELDS",
    "Round53CaseCandidate",
    "Round53OverlayTarget",
    "Round53OverlayWeightDraft",
    "render_round53_price_validation_plan_markdown",
    "render_round53_redteam_gate_plan_markdown",
    "render_round53_summary_markdown",
    "round53_case_candidate_rows",
    "round53_case_records",
    "round53_price_field_rows",
    "round53_score_profile_rows",
    "round53_stage_date_rows",
    "round53_summary",
    "target_for",
    "write_round53_r13_reports",
]
