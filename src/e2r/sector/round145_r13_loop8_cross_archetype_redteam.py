"""Round-145 R13 Loop-8 cross-archetype RedTeam / 4B / price validation pack.

Round 145 is a common validation layer over the R1-R12 sector/archetype work.
It forces the final seven checks from the round note: cross-evidence, EPS/FCF
durability, price-path alignment, disclosure confidence, no hard RedTeam flag,
unsaturated 4B, and policy-shock review. It is calibration and report material
only. It does not change production feature engineering, scoring, staging, or
RedTeam rules.
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


ROUND145_SOURCE_ROUND_PATH = "docs/round/round_145.md"
ROUND145_LARGE_SECTOR = "CROSS_ARCHETYPE_REDTEAM_4B_PRICE_VALIDATION"
ROUND145_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round145_r13_loop8_cross_archetype_redteam"
ROUND145_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r13_loop8_round145.jsonl"
ROUND145_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round145_r13_loop8_v8.csv"


@dataclass(frozen=True)
class Round145OverlayWeightDraft:
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
class Round145OverlayAxis:
    axis_id: str
    weight: int
    stage1_cap_inputs: tuple[str, ...]
    stage2_cap_inputs: tuple[str, ...]
    stage3_unlock_inputs: tuple[str, ...]
    stage4b_inputs: tuple[str, ...]
    stage4c_inputs: tuple[str, ...]
    interpretation: str

    def as_csv_dict(self) -> dict[str, str]:
        return {
            "axis_id": self.axis_id,
            "weight": str(self.weight),
            "stage1_cap_inputs": "|".join(self.stage1_cap_inputs),
            "stage2_cap_inputs": "|".join(self.stage2_cap_inputs),
            "stage3_unlock_inputs": "|".join(self.stage3_unlock_inputs),
            "stage4b_inputs": "|".join(self.stage4b_inputs),
            "stage4c_inputs": "|".join(self.stage4c_inputs),
            "interpretation": self.interpretation,
            "production_scoring_changed": "false",
        }


@dataclass(frozen=True)
class Round145StageCap:
    cap_id: str
    stage_band: str
    score_cap: str
    cap_triggers: tuple[str, ...]
    release_conditions: tuple[str, ...]
    hard_redteam_flags: tuple[str, ...]
    interpretation: str

    def as_dict(self) -> dict[str, str]:
        return {
            "cap_id": self.cap_id,
            "stage_band": self.stage_band,
            "score_cap": self.score_cap,
            "cap_triggers": "|".join(self.cap_triggers),
            "release_conditions": "|".join(self.release_conditions),
            "hard_redteam_flags": "|".join(self.hard_redteam_flags),
            "interpretation": self.interpretation,
            "production_scoring_changed": "false",
        }


@dataclass(frozen=True)
class Round145OverlayTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round145OverlayWeightDraft
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
        return ROUND145_LARGE_SECTOR

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round145CaseCandidate:
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


ROUND145_OVERLAY_AXES: tuple[Round145OverlayAxis, ...] = (
    Round145OverlayAxis(
        "eps_fcf_roe_affo_opm_bodyweight_change",
        24,
        ("tam_headline", "user_growth", "demand_news", "price_headline"),
        ("guidance_raise", "prescription_volume", "arr_billings_bookings", "tenant_lease"),
        ("eps_fcf_improvement", "roe_improvement", "affo_per_share_quality", "opm_expansion", "price_path_aligned"),
        ("eps_revision_slowdown", "multiple_expansion_ahead_of_eps", "new_frame_crowded"),
        ("sales_profit_decline_warning", "price_war", "affo_integrity_break", "commercialization_failure"),
        "R13 starts with the cash-flow bodyweight question. Example: SK하이닉스 HBM can pass; approval-only biotech cannot.",
    ),
    Round145OverlayAxis(
        "evidence_visibility",
        20,
        ("mou", "policy_announcement", "paper_or_patent", "viral_theme"),
        ("contract", "order", "customer", "prescription", "arr", "billings", "backlog", "government_order", "tenant_lease"),
        ("cross_evidence", "official_detail", "multi_source_confirmation", "revenue_recognition_path"),
        ("visibility_fully_priced", "target_price_crowding"),
        ("contract_cancelled", "customer_damage", "filing_delay", "detail_missing"),
        "Evidence visibility turns events into Stage 2. Example: disease news is Stage 1; stockpile order plus guidance can become Stage 2.",
    ),
    Round145OverlayAxis(
        "durability_repeatability",
        16,
        ("one_off_event", "single_contract_headline", "single_product_spike"),
        ("long_term_contract", "recurring_revenue", "renewal", "government_procurement", "prescription_continuity"),
        ("repeatability_after_event", "retention_visible", "reimbursement_or_renewal_stable", "utilization_stable"),
        ("durability_assumed_by_market", "crowded_new_frame"),
        ("normalization", "renewal_decline", "slow_uptake", "customer_churn"),
        "Stage 3 needs repeatability. Example: Circle recurring USDC use is different from an STO theme headline.",
    ),
    Round145OverlayAxis(
        "disclosure_confidence_redteam",
        12,
        ("list_only_disclosure", "single_source_claim", "undated_document", "watch_disclosure_headline"),
        ("detail_fetched", "amount_customer_duration_verified", "audit_status_checked", "legal_scope_checked"),
        ("disclosure_confidence_high", "no_hard_redteam", "redteam_review_passed", "price_path_aligned"),
        ("redteam_ignored_during_crowded_rally", "detail_missing_in_4b"),
        ("auditor_resignation", "global_outage", "affo_misclassification", "depeg", "regulatory_denial", "policy_shock"),
        "This is the final gate. Example: Supermicro growth is blocked when auditor resignation and filing delay appear.",
    ),
    Round145OverlayAxis(
        "capital_discipline_leverage_fcf",
        10,
        ("capex_plan", "growth_financing_story", "ipo_funding"),
        ("fcf_plan", "cash_runway_visible", "debt_maturity_visible", "funding_cost_visible"),
        ("fcf_after_capex", "leverage_controlled", "dividend_or_buyback_covered", "arms_length_financing"),
        ("growth_funded_by_rerating", "debt_ignored"),
        ("cash_crunch", "refinancing_risk", "negative_fcf", "discounted_take_private", "circular_financing"),
        "Capital structure can kill a good story. Example: CoreWeave-style AI contracts stay capped when financing is circular or leverage-heavy.",
    ),
    Round145OverlayAxis(
        "market_mispricing_rerating_gap",
        10,
        ("old_frame_or_neglect", "sector_theme_first_attention"),
        ("new_frame_evidence_better_than_market_frame", "price_response_but_not_crowded"),
        ("valuation_frame_changed_by_numbers", "market_still_under-recognizes_cash_flow"),
        ("new_frame_widely_accepted", "consensus_crowded", "policy_shock_sensitive"),
        ("price_path_failed", "frame_not_changed", "evidence_not_monetized"),
        "Mispricing is validated by price path and numbers, not narrative. Example: BXDC sponsor premium is not enough without assets and AFFO.",
    ),
    Round145OverlayAxis(
        "valuation_room_4b_margin",
        8,
        ("post_drawdown", "low_expectation"),
        ("valuation_not_yet_full_new_frame", "stage2_price_response"),
        ("valuation_room_after_stage3_evidence", "4b_margin_present"),
        ("large_12m_24m_return", "valuation_saturation", "market_already_accepts_new_frame"),
        ("crowded_trade_unwind", "policy_market_shock", "multiple_compression"),
        "Good structure and fresh opportunity are different. Example: SK하이닉스 can be structurally right and still need 4B-watch.",
    ),
)


ROUND145_STAGE_CAPS: tuple[Round145StageCap, ...] = (
    Round145StageCap(
        "stage1_theme_headline_cap",
        "Stage 1",
        "45",
        (
            "theme",
            "policy",
            "mou",
            "paper_or_patent",
            "viral",
            "tam",
            "user_count",
            "demand_news",
            "price_headline",
        ),
        (
            "contract",
            "customer",
            "government_order",
            "tenant_lease",
            "guidance_raise",
            "arr_billings_bookings",
            "prescription_volume",
        ),
        (
            "price_only_rally",
            "theme_only",
            "future_data_leakage",
            "undated_document",
        ),
        "Stage 1 can route research, but headline evidence does not create structural conviction.",
    ),
    Round145StageCap(
        "stage2_verified_evidence_cap",
        "Stage 2",
        "70",
        (
            "contract",
            "customer",
            "amount",
            "duration",
            "guidance_raise",
            "prescription",
            "arr_billings_bookings",
            "government_order",
            "tenant_lease",
            "buyback_cancellation",
            "pbm_formulary",
        ),
        (
            "eps_fcf_roe_affo_opm_improvement",
            "repeatability_confirmed",
            "price_path_aligned",
            "disclosure_detail_sufficient",
            "no_hard_redteam",
            "valuation_room_remaining",
        ),
        (
            "one_off_event",
            "single_contract_extrapolated",
            "no_revenue_conversion",
            "detail_missing",
            "redteam_unchecked",
        ),
        "Verified contracts, orders, or ARR can reach Stage 2; Stage 3 needs cash-flow conversion and price-path validation.",
    ),
    Round145StageCap(
        "stage3_green_all_checks_gate",
        "Stage 3",
        "requires_all_green_checks",
        (
            "candidate_above_70_without_full_checks",
            "green_requested_from_sector_score_only",
        ),
        (
            "eps_fcf_or_cashflow_bodyweight_change",
            "structural_durability",
            "old_frame_mispricing",
            "disclosure_detail",
            "price_path_alignment",
            "4b_valuation_room",
            "hard_4c_absent",
        ),
        (
            "auditor_resignation",
            "global_outage",
            "commercialization_failure",
            "cash_crunch",
            "contract_cancellation",
            "affo_integrity_break",
            "depeg",
            "policy_market_shock",
        ),
        "R13 Green is not score-only. All seven checks must pass before a candidate can remain Green.",
    ),
    Round145StageCap(
        "stage4b_4c_final_redteam_gate",
        "4B/4C",
        "watch_or_break",
        (
            "new_frame_widely_accepted",
            "one_two_year_runup",
            "consensus_crowded",
            "valuation_expansion_ahead_of_eps",
            "policy_shock_sensitive",
        ),
        (
            "revision_still_accelerating",
            "valuation_room_remaining",
            "redteam_clean",
            "price_path_stabilized",
        ),
        (
            "accounting_trust_break",
            "operational_trust_break",
            "legal_regulatory_break",
            "leverage_fcf_breakdown",
            "commercialization_failure",
            "affo_cashflow_integrity_risk",
            "circular_ai_financing",
            "stablecoin_convertibility_failure",
        ),
        "R13 is the final kill-switch layer: good sectors can graduate to 4B or break to 4C.",
    ),
)


ROUND145_OVERLAY_TARGETS: tuple[Round145OverlayTarget, ...] = (
    Round145OverlayTarget(
        "STRUCTURAL_SUCCESS_ALIGNED",
        E2RArchetype.STRUCTURAL_SUCCESS_ALIGNED,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round145OverlayWeightDraft("+", "+", "+", "+", "+", "optional", "+", "pass_if_no_redteam"),
        ("industry_structure_change", "official_disclosure_or_report", "price_attention"),
        ("contract_order_revenue_or_revision", "eps_fcf_bodyweight_change", "cross_evidence"),
        ("medium_term_eps_fcf_revision", "valuation_frame_change", "price_path_aligned", "no_hard_redteam"),
        ("crowded_new_frame", "valuation_saturation", "revision_slowdown"),
        ("hard_redteam", "eps_fcf_revision_down", "thesis_break"),
        ("cross_evidence", "eps_fcf_bodyweight_change", "price_path_aligned", "no_hard_redteam"),
        ("crowded_4b", "valuation_saturation", "revision_slowdown"),
        "Positive validation bucket for cases where evidence, EPS/FCF, and price path align.",
        "High score survives only if evidence, price path, and RedTeam all align.",
        stage3_green_allowed=True,
    ),
    Round145OverlayTarget(
        "STRUCTURAL_SUCCESS_BUT_4B_WATCH",
        E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round145OverlayWeightDraft("maintain", "maintain", "maintain", "weaken", "deduct", "optional", "maintain", "stage4b_watch"),
        ("large_12m_24m_return", "universally_bullish_reports", "target_multiple_expansion"),
        ("valuation_band_saturated", "new_frame_widely_accepted", "revision_still_positive"),
        ("fundamentals_intact_but_mispricing_reduced",),
        ("4b_watch", "4b_elevated", "4b_graduated", "crowded_new_frame"),
        ("revision_down", "demand_slowdown", "capex_overbuild", "margin_peak"),
        ("evidence_intact", "mispricing_not_exhausted"),
        ("crowding", "valuation_saturation", "revision_slowdown", "capacity_addition"),
        "Separates good structures that have already become crowded 4B monitoring cases.",
        "4B is graduation/monitoring language; it is not a fresh Green promotion rule.",
    ),
    Round145OverlayTarget(
        "SECTOR_SUCCESS_BUT_POLICY_SHOCK_WATCH",
        E2RArchetype.SECTOR_SUCCESS_BUT_POLICY_SHOCK_WATCH,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round145OverlayWeightDraft("maintain", "maintain", "maintain", "weaken", "deduct", "optional", "maintain", "policy_4b_overlay"),
        ("sector_success", "crowded_theme", "policy_comment", "market_wide_selloff"),
        ("company_eps_impact_check", "government_clarification", "price_path_retest"),
        ("fundamentals_intact_but_policy_risk_premium_changed",),
        ("policy_shock_4b_watch", "crowded_trade_unwind", "valuation_risk_premium_spike"),
        ("policy_market_shock", "tax_or_redistribution_comment", "market_wide_selloff", "price_path_break"),
        ("fundamentals_intact", "policy_impact_limited", "price_path_recovers"),
        ("policy_market_shock", "crowded_trade_unwind", "valuation_risk_premium_spike"),
        "Separates structurally successful sectors whose price path is vulnerable to policy shock in crowded 4B.",
        "Policy shock is not company EPS evidence; it retests price-path validation.",
    ),
    Round145OverlayTarget(
        "PRICE_ONLY_RALLY",
        E2RArchetype.PRICE_ONLY_RALLY,
        Round10ThemePosture.REDTEAM_FIRST,
        Round145OverlayWeightDraft("0", "0", "0", "-", "-", "0", "-", "green_block"),
        ("price_spike", "sns_theme", "headline_without_numbers"),
        ("no_eps_revision", "no_contract_or_revenue", "no_disclosure_support"),
        ("not_green_without_eps_fcf_and_cross_evidence",),
        ("price_only_4b_watch", "retail_crowding"),
        ("price_reversal", "theme_fade", "no_revenue_conversion"),
        (),
        ("no_eps_fcf", "no_contract", "no_revenue", "theme_only"),
        "Green blocker for price-only moves.",
        "Price can route attention, but price alone is not structural evidence.",
    ),
    Round145OverlayTarget(
        "EVENT_PREMIUM",
        E2RArchetype.EVENT_PREMIUM,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round145OverlayWeightDraft("0~+", "0", "0", "+", "0", "0", "medium", "event_split"),
        ("tender_offer", "control_battle", "policy_announcement", "mou", "disaster_or_disease_event"),
        ("binding_contract", "funded_budget", "actual_order", "guide_up"),
        ("repeat_contract_or_revenue_plus_eps_fcf",),
        ("event_premium_crowded", "expected_deal_priced"),
        ("event_fade", "deal_failure", "budget_missing", "one_off_demand_normalization"),
        ("actual_order", "eps_fcf_conversion"),
        ("mou_only", "policy_only", "event_only", "deal_failure"),
        "Separates policy/event premium from structural rerating.",
        "Events stay event buckets unless orders, budgets, or earnings convert them.",
    ),
    Round145OverlayTarget(
        "EVENT_TO_CONTRACT_ESCALATION",
        E2RArchetype.EVENT_TO_CONTRACT_ESCALATION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round145OverlayWeightDraft("+", "+", "optional", "+", "optional", "0", "+", "stage2_candidate"),
        ("event_news", "policy_or_disease_or_rebuild_trigger", "mou_or_expectation"),
        ("government_order", "stockpile", "funded_budget", "financing", "binding_contract", "guide_up"),
        ("repeat_contract", "revenue_guidance_or_eps_revision", "cross_evidence"),
        ("event_crowded_before_contract",),
        ("budget_missing", "contract_cancelled", "one_off_normalization"),
        ("contract_or_order", "revenue_guidance_or_eps_revision"),
        ("mou_only", "unfunded_policy", "single_headline"),
        "Routes event candidates to Stage 2 only when the event turns into funded contract/order evidence.",
        "Example: disease news is only Stage 1; stockpile order plus guidance can become Stage 2.",
    ),
    Round145OverlayTarget(
        "CYCLICAL_SUCCESS",
        E2RArchetype.CYCLICAL_SUCCESS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round145OverlayWeightDraft("+", "low", "+", "0", "low", "0", "medium", "cycle_cap"),
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
    Round145OverlayTarget(
        "FALSE_POSITIVE_SCORE",
        E2RArchetype.FALSE_POSITIVE_SCORE,
        Round10ThemePosture.REDTEAM_FIRST,
        Round145OverlayWeightDraft("-", "-", "-", "-", "-", "0", "-", "score_recalibration"),
        ("high_score_without_actual_evidence", "proxy_score_overfit"),
        ("earnings_miss", "no_price_validation", "redteam_ignored"),
        ("not_applicable_until_score_axis_fixed",),
        ("false_positive_crowding",),
        ("price_failed", "earnings_failed", "audit_or_redteam_ignored"),
        (),
        ("score_overfit", "no_eps_fcf", "price_failed", "redteam_ignored"),
        "Score calibration bucket for high-score failures.",
        "A keyword-heavy high score is a calibration failure if EPS, price, or RedTeam later rejects it.",
    ),
    Round145OverlayTarget(
        "EVIDENCE_GOOD_BUT_PRICE_FAILED",
        E2RArchetype.EVIDENCE_GOOD_BUT_PRICE_FAILED,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round145OverlayWeightDraft("+", "+", "optional", "0", "-", "optional", "+", "alignment_review"),
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
    Round145OverlayTarget(
        "REDTEAM_ACCOUNTING_TRUST_OVERLAY",
        E2RArchetype.REDTEAM_ACCOUNTING_TRUST_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        Round145OverlayWeightDraft("gate", "gate", "gate", "gate", "gate", "gate", "gate", "hard_block"),
        ("auditor_resignation", "filing_delay", "internal_control_issue"),
        ("financial_restatement", "related_party_risk", "regulatory_probe"),
        ("not_applicable_until_trust_restored",),
        ("accounting_risk_ignored_during_rerating",),
        ("auditor_resignation", "filing_delay", "internal_control_weakness", "restatement", "probe"),
        (),
        ("auditor_resignation", "filing_delay", "internal_control_issue", "related_party_risk"),
        "Hard gate for accounting/audit trust failures.",
        "Growth numbers cannot support Stage 3-Green if reporting integrity breaks.",
        hard_gate=True,
    ),
    Round145OverlayTarget(
        "OPERATIONAL_TRUST_BREAK",
        E2RArchetype.OPERATIONAL_TRUST_BREAK,
        Round10ThemePosture.REDTEAM_FIRST,
        Round145OverlayWeightDraft("gate", "gate", "gate", "gate", "gate", "gate", "gate", "hard_review"),
        ("security_outage", "privacy_breach", "customer_damage", "platform_safety_incident"),
        ("customer_lawsuit", "renewal_risk", "service_level_break"),
        ("trust_restoration_and_retention_required",),
        ("trust_break_ignored_by_growth_story",),
        ("customer_churn", "lawsuit_damage", "renewal_decline", "brand_trust_loss"),
        (),
        ("security_outage", "privacy_breach", "customer_lawsuit", "operational_trust_damage"),
        "Operational trust-break overlay for SaaS, security, platform, and infrastructure names.",
        "Recurring revenue is recurring only while customer trust remains intact.",
        hard_gate=True,
    ),
    Round145OverlayTarget(
        "LEGAL_REGULATORY_REDTEAM",
        E2RArchetype.LEGAL_REGULATORY_REDTEAM,
        Round10ThemePosture.REDTEAM_FIRST,
        Round145OverlayWeightDraft("gate", "gate", "gate", "gate", "gate", "gate", "gate", "hard_soft_gate"),
        ("lawsuit", "regulatory_probe", "license_risk", "approval_denial"),
        ("fine_or_restriction", "commercialization_blocked", "export_approval_issue"),
        ("not_green_until_legal_scope_resolved",),
        ("legal_risk_ignored_by_rally",),
        ("approval_denial", "license_revocation", "injunction", "regulatory_sanction"),
        (),
        ("lawsuit", "regulatory_probe", "approval_denial", "license_risk"),
        "Legal/regulatory RedTeam overlay.",
        "Approval, license, and legal scope must be verified before Green.",
        hard_gate=True,
    ),
    Round145OverlayTarget(
        "LEVERAGE_FCF_BREAKDOWN",
        E2RArchetype.LEVERAGE_FCF_BREAKDOWN,
        Round10ThemePosture.REDTEAM_FIRST,
        Round145OverlayWeightDraft("-", "-", "0", "-", "-", "-", "medium", "green_block"),
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
    Round145OverlayTarget(
        "COMMERCIALIZATION_FAILURE",
        E2RArchetype.COMMERCIALIZATION_FAILURE,
        Round10ThemePosture.REDTEAM_FIRST,
        Round145OverlayWeightDraft("hard-", "hard-", "0", "hard-", "hard-", "hard-", "+", "hard_4c"),
        ("approval_status", "clinical_success", "regulatory_clearance"),
        ("slow_prescription", "reimbursement_failure", "patient_uptake_weak", "cash_runway_collapse"),
        ("commercial_revenue_and_cash_runway_required",),
        ("approval_story_crowded",),
        ("approval_but_no_uptake", "going_concern", "discounted_take_private"),
        (),
        ("slow_uptake", "reimbursement_failure", "commercial_revenue_missing", "cash_runway_collapse"),
        "Biotech/healthcare commercialization failure gate.",
        "Approval is a starting point; prescriptions, reimbursement, revenue, and cash runway decide evidence quality.",
        hard_gate=True,
    ),
    Round145OverlayTarget(
        "AFFO_CASHFLOW_INTEGRITY_RISK",
        E2RArchetype.AFFO_CASHFLOW_INTEGRITY_RISK,
        Round10ThemePosture.REDTEAM_FIRST,
        Round145OverlayWeightDraft("gate", "gate", "gate", "gate", "gate", "gate", "gate", "reit_hard_review"),
        ("affo_growth", "data_center_reit_ai_demand", "dividend_yield_story"),
        ("maintenance_capex", "expansion_capex", "noi_growth", "dividend_coverage"),
        ("affo_quality_verified_before_green",),
        ("ai_real_asset_story_crowded", "funding_cost_ignored"),
        ("affo_overstatement", "maintenance_capex_misclassification", "dividend_coverage_break"),
        (),
        ("affo_integrity_risk", "maintenance_capex", "tenant_concentration", "power_constraint"),
        "REIT and real-asset cashflow integrity review.",
        "AFFO growth must be tested against capex classification, funding cost, and dividend coverage.",
        hard_gate=True,
    ),
    Round145OverlayTarget(
        "CAPEX_AFFO_DILUTION_RISK",
        E2RArchetype.CAPEX_AFFO_DILUTION_RISK,
        Round10ThemePosture.REDTEAM_FIRST,
        Round145OverlayWeightDraft("gate", "gate", "gate", "gate", "gate", "gate", "gate", "reit_infra_hard_review"),
        ("data_center_reit_ai_demand", "ai_real_asset_expansion", "capex_plan"),
        ("capex_budget", "affo_per_share_growth", "tenant_commitment", "power_water_permitting"),
        ("capex_per_share_accretive", "dividend_coverage_intact", "funding_cost_controlled"),
        ("ai_real_asset_story_crowded", "capex_growth_ignored", "tenant_quality_assumed"),
        (
            "capex_growth_above_affo_growth",
            "affo_per_share_miss",
            "funding_cost_spike",
            "power_constraint",
            "tenant_concentration",
        ),
        (),
        (
            "capex_affo_dilution",
            "affo_per_share_growth_weak",
            "funding_cost",
            "power_water_permitting",
            "tenant_concentration",
        ),
        "REIT and infrastructure capex dilution hard review.",
        "AI real-asset growth must be tested per share; capex that outruns AFFO is not structural evidence.",
        hard_gate=True,
    ),
    Round145OverlayTarget(
        "STABLECOIN_CONVERTIBILITY_RISK",
        E2RArchetype.STABLECOIN_CONVERTIBILITY_RISK,
        Round10ThemePosture.REDTEAM_FIRST,
        Round145OverlayWeightDraft("gate", "gate", "gate", "gate", "gate", "gate", "gate", "hard_block"),
        ("stablecoin_growth", "digital_asset_liquidity", "reserve_claim"),
        ("reserve_attestation", "redemption_liquidity", "regulated_fiat_backing"),
        ("fiat_backed_convertibility_verified",),
        ("crypto_liquidity_story_crowded",),
        ("depeg", "reserve_failure", "convertibility_failure", "liquidity_run", "fraud"),
        (),
        ("depeg_event", "reserve_failure", "convertibility_risk", "algorithmic_stablecoin_failure"),
        "Hard gate for stablecoin reserve, redemption, and de-peg failures.",
        "Regulated fiat-backed stablecoin, algorithmic stablecoin, and STO theme stocks must not be conflated.",
        hard_gate=True,
    ),
    Round145OverlayTarget(
        "CIRCULAR_AI_FINANCING_WATCH",
        E2RArchetype.CIRCULAR_AI_FINANCING_WATCH,
        Round10ThemePosture.REDTEAM_FIRST,
        Round145OverlayWeightDraft("gate", "gate", "gate", "gate", "gate", "gate", "gate", "ai_infra_hard_review"),
        ("supplier_investor_customer_loop", "customer_contract_concentration", "gpu_collateral_debt"),
        ("customer_contract", "capacity_guarantee", "unused_capacity_purchase", "financing_terms"),
        ("fcf_positive", "leverage_controlled", "arms_length_contracts", "customer_diversified"),
        ("ai_infra_contract_visibility_priced_without_financing_risk",),
        (
            "circular_financing",
            "supplier_investor_customer_loop",
            "capacity_guarantee",
            "gpu_collateral_debt",
            "customer_concentration",
            "refinancing_risk",
        ),
        (),
        (
            "circular_financing",
            "supplier_investor_customer_loop",
            "capacity_guarantee",
            "gpu_collateral_debt",
            "customer_concentration",
            "refinancing_risk",
        ),
        "Hard review for AI infrastructure contracts where suppliers, customers, lenders, or investors are economically entangled.",
        "Contract visibility is capped until FCF, leverage, customer concentration, and arm's-length financing are verified.",
        hard_gate=True,
    ),
    Round145OverlayTarget(
        "POLICY_MARKET_SHOCK_EVENT",
        E2RArchetype.POLICY_MARKET_SHOCK_EVENT,
        Round10ThemePosture.REDTEAM_FIRST,
        Round145OverlayWeightDraft("gate", "gate", "gate", "gate", "gate", "gate", "gate", "policy_price_path_shock"),
        (
            "tax_policy_comment",
            "ai_windfall_tax",
            "citizen_dividend",
            "market_wide_selloff",
            "redistribution_comment",
        ),
        ("actual_bill", "tax_rate_or_rule_draft", "government_clarification", "company_eps_impact"),
        ("not_green_without_company_eps_fcf_impact", "policy_clarity_required"),
        ("crowded_trade_unwind", "valuation_risk_premium_spike", "market_wide_policy_shock"),
        (
            "market_wide_policy_shock",
            "tax_or_redistribution_comment",
            "government_clarification_needed",
            "valuation_risk_premium_spike",
            "crowded_trade_unwind",
        ),
        (),
        (
            "policy_market_shock",
            "tax_or_redistribution_comment",
            "government_clarification_needed",
            "valuation_risk_premium_spike",
            "crowded_trade_unwind",
        ),
        "Policy, tax, and redistribution comments can break price-path validation in crowded 4B trades.",
        "A policy shock is not company EPS/FCF evidence; it is a RedTeam overlay until actual company impact is verified.",
        hard_gate=True,
    ),
    Round145OverlayTarget(
        "DISCLOSURE_CONFIDENCE_CAPPED",
        E2RArchetype.DISCLOSURE_CONFIDENCE_CAPPED,
        Round10ThemePosture.REDTEAM_FIRST,
        Round145OverlayWeightDraft("cap", "cap", "cap", "cap", "cap", "cap", "+", "stage3_confidence_cap"),
        ("disclosure_detected", "contract_headline", "opendart_list_only"),
        ("opendart_detail_fetched", "contract_amount", "customer_or_use_disclosed"),
        ("contract_amount_to_sales", "margin_or_duration_visible", "multi_source_confirmation"),
        ("undisclosed_contract_theme_crowded",),
        ("detail_missing", "customer_unknown", "amount_undisclosed", "purpose_unknown", "margin_unknown"),
        ("detail_disclosed", "contract_amount", "customer_or_use_visible", "margin_or_duration_visible"),
        ("detail_missing", "customer_undisclosed", "contract_amount_missing", "purpose_missing", "margin_unknown"),
        "Caps Stage 3 confidence when disclosure detail is missing.",
        "OpenDART list-only or headline-only disclosures cannot support Green until amount, customer/use, and duration or margin detail is verified.",
    ),
    Round145OverlayTarget(
        "UNKNOWN_INSUFFICIENT_EVIDENCE",
        E2RArchetype.UNKNOWN_INSUFFICIENT_EVIDENCE,
        Round10ThemePosture.REDTEAM_FIRST,
        Round145OverlayWeightDraft("0", "0", "0", "0", "0", "0", "low", "green_block"),
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


ROUND145_CASE_CANDIDATES: tuple[Round145CaseCandidate, ...] = (
    Round145CaseCandidate(
        "sk_hynix_hbm_memory_structural_4b_watch_case",
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
        ("round_145.md Reuters SK Hynix AI boom / market value",),
        "HBM/memory rerating is structurally aligned, but the price path also requires 4B monitoring.",
        (E2RArchetype.MEMORY_HBM_CAPACITY, E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH),
    ),
    Round145CaseCandidate(
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
        "valueup_strategy_aligned_requires_fcf_validation",
        "needs_price_backfill",
        ("round_145.md Reuters Hyundai sales target / hybrid / buyback",),
        "Hybrid mix and shareholder return can align, but Green still needs FCF and execution evidence.",
        (E2RArchetype.AUTO_MOBILITY_COMPLETED_VEHICLE, E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN),
    ),
    Round145CaseCandidate(
        "korea_buyback_cancellation_policy_to_execution_case",
        "EVENT_TO_CONTRACT_ESCALATION",
        "KOREA_VALUEUP_POLICY",
        "Korea buyback cancellation policy background",
        "KR",
        "success_candidate",
        date(2026, 2, 25),
        None,
        None,
        None,
        None,
        ("commercial_act_revision", "buyback_cancellation_policy", "shareholder_value_policy"),
        ("policy_only", "company_execution_missing", "roe_improvement_unverified"),
        "policy_to_execution_background",
        "needs_price_backfill",
        ("round_145.md Reuters Korea Commercial Act revision",),
        "Policy is Stage 1 background; individual names require actual cancellation, returns, ROE/PBR evidence.",
        (E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN, E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE),
    ),
    Round145CaseCandidate(
        "circle_regulated_stablecoin_infra_4b_watch_case",
        "STRUCTURAL_SUCCESS_BUT_4B_WATCH",
        "CRCL",
        "Circle Internet Group",
        "US",
        "4b_watch",
        date(2026, 5, 11),
        date(2026, 5, 11),
        None,
        date(2026, 5, 11),
        None,
        (
            "fiat_backed_stablecoin",
            "regulated_fiat_backing",
            "stablecoin_circulation",
            "reserve_income",
            "ipo_rerating",
        ),
        (
            "rate_sensitivity",
            "reserve_income_margin_pressure",
            "convertibility_risk",
            "valuation_crowded",
        ),
        "regulated_stablecoin_infra_success_but_4b_watch",
        "needs_price_backfill",
        ("round_145.md Reuters Circle reserve income / USDC circulation",),
        "Regulated fiat-backed stablecoin infrastructure can be a real business, but IPO rerating and rate-sensitive reserve income require 4B-watch and convertibility review.",
        (E2RArchetype.STABLECOIN_CONVERTIBILITY_RISK, E2RArchetype.DIGITAL_ASSET_TOKENIZATION),
    ),
    Round145CaseCandidate(
        "blackstone_digital_infra_trust_stage1_capped_case",
        "DISCLOSURE_CONFIDENCE_CAPPED",
        "BXDC",
        "Blackstone Digital Infrastructure Trust",
        "US",
        "failed_rerating",
        date(2026, 5, 14),
        None,
        None,
        None,
        None,
        ("ai_data_center_acquisition_pipeline", "sponsor_track_record", "hyperscale_tenant_target"),
        (
            "asset_acquired_missing",
            "binding_lease_unknown",
            "noi_affo_unknown",
            "power_water_permitting_unknown",
            "disclosure_confidence_capped",
        ),
        "ai_infra_real_asset_stage1_disclosure_capped",
        "needs_price_backfill",
        ("round_145.md Reuters Blackstone data-center vehicle IPO",),
        "An AI data-center vehicle can be Stage 1, but asset acquisition, binding tenant lease, NOI/AFFO, and power/water detail are required before Stage 3 confidence.",
        (E2RArchetype.DATA_CENTER_REIT_INFRASTRUCTURE, E2RArchetype.CAPEX_AFFO_DILUTION_RISK),
    ),
    Round145CaseCandidate(
        "fermi_ai_real_asset_no_revenue_case",
        "DISCLOSURE_CONFIDENCE_CAPPED",
        "FRMI",
        "Fermi AI real asset no-revenue power-campus case",
        "US",
        "failed_rerating",
        date(2025, 9, 30),
        None,
        None,
        None,
        None,
        ("ai_power_campus", "11gw_power_plan", "ipo_valuation", "sponsor_premium"),
        (
            "no_revenue_flag",
            "binding_tenant_lease_absent",
            "power_delivery_long_dated",
            "power_water_permitting_unknown",
            "disclosure_confidence_capped",
        ),
        "ai_real_asset_no_revenue_high_risk",
        "needs_price_backfill",
        ("round_145.md Reuters Fermi AI data-center IPO",),
        "AI real-asset demand is not Stage 3 evidence before acquired assets, binding tenants, revenue, power delivery, water, permitting, and NOI/AFFO are verified.",
        (E2RArchetype.AI_INFRA_REAL_ASSET_THEME_OVERLAY, E2RArchetype.CAPEX_AFFO_DILUTION_RISK),
    ),
    Round145CaseCandidate(
        "event_to_contract_escalation_reference_case",
        "EVENT_TO_CONTRACT_ESCALATION",
        "EVENT_TO_CONTRACT",
        "event-to-contract reference case",
        "GLOBAL",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("event_news", "government_order", "stockpile", "funded_budget", "guide_up"),
        ("one_off_event", "repeat_contract_unproven"),
        "event_escalates_to_stage2_only_after_contract_or_order",
        "needs_price_backfill",
        ("round_145.md event-to-contract escalation rule",),
        "Disease, rebuild, or policy news can become Stage 2 only after funded order, budget, or guidance.",
        (E2RArchetype.ONE_OFF_EVENT_DEMAND, E2RArchetype.EVENT_PREMIUM),
    ),
    Round145CaseCandidate(
        "korea_ai_tax_policy_market_shock_case",
        "SECTOR_SUCCESS_BUT_POLICY_SHOCK_WATCH",
        "KOSPI_AI_POLICY_SHOCK",
        "Korea AI tax policy market shock reference",
        "KR",
        "4b_watch",
        date(2026, 5, 12),
        None,
        None,
        date(2026, 5, 12),
        None,
        ("ai_windfall_tax_comment", "citizen_dividend_comment", "market_wide_selloff", "crowded_ai_rally"),
        (
            "policy_market_shock",
            "tax_or_redistribution_comment",
            "government_clarification_needed",
            "valuation_risk_premium_spike",
            "crowded_trade_unwind",
        ),
        "policy_market_shock_breaks_crowded_4b_price_path",
        "needs_price_backfill",
        ("round_145.md Barron's Korea AI tax / KOSPI shock",),
        "Policy, tax, or redistribution comments are not company evidence, but they can break the price path of crowded AI and value-up rallies until company-level EPS/FCF impact is clarified.",
        (E2RArchetype.AI_CAPEX_CROWDING_OVERLAY, E2RArchetype.THEME_VALUATION_OVERHEAT),
    ),
    Round145CaseCandidate(
        "coreweave_nvidia_circular_financing_watch_case",
        "CIRCULAR_AI_FINANCING_WATCH",
        "CRWV",
        "CoreWeave / Nvidia circular financing watch",
        "US",
        "failed_rerating",
        date(2026, 5, 13),
        None,
        None,
        None,
        None,
        (
            "ai_cloud_demand",
            "supplier_investor_customer_loop",
            "capacity_guarantee",
            "gpu_capacity_contract",
        ),
        (
            "circular_financing",
            "supplier_investor_customer_loop",
            "capacity_guarantee",
            "gpu_collateral_debt",
            "customer_concentration",
            "refinancing_risk",
        ),
        "contract_visibility_but_circular_financing_watch",
        "needs_price_backfill",
        ("round_145.md Reuters Nvidia / CoreWeave financing and capacity relationship",),
        "AI cloud contract visibility is capped when supplier, investor, customer, and capacity-guarantee relationships are circular or leverage-heavy.",
        (E2RArchetype.NEOCLOUD_GPU_RENTAL, E2RArchetype.CIRCULAR_AI_FINANCING_OVERLAY),
    ),
    Round145CaseCandidate(
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
        ("round_145.md AP SMCI auditor resignation",),
        "Accounting trust failure is a hard RedTeam gate even after a strong AI rerating.",
        (E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE, E2RArchetype.THESIS_BREAK_4C),
    ),
    Round145CaseCandidate(
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
        ("security_platform_growth", "large_customer_base", "recurring_revenue"),
        ("global_outage", "customer_damage", "shareholder_lawsuit", "customer_lawsuit", "renewal_risk"),
        "operational_trust_break_4c",
        "needs_price_backfill",
        ("round_145.md Reuters CrowdStrike outage and lawsuit",),
        "Security SaaS recurring revenue depends on operational trust.",
        (E2RArchetype.SECURITY_IDENTITY_DEEPFAKE, E2RArchetype.THESIS_BREAK_4C),
    ),
    Round145CaseCandidate(
        "terrausd_luna_algorithmic_stablecoin_break_case",
        "STABLECOIN_CONVERTIBILITY_RISK",
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
        ("depeg_event", "reserve_failure", "convertibility_failure", "liquidity_run", "fraud_risk"),
        "algorithmic_stablecoin_thesis_break",
        "needs_price_backfill",
        ("round_145.md Reuters TerraUSD/Luna collapse",),
        "Depeg/reserve/convertibility failure is a hard thesis break.",
        (E2RArchetype.DIGITAL_ASSET_TOKENIZATION, E2RArchetype.LEGAL_REGULATORY_REDTEAM),
    ),
    Round145CaseCandidate(
        "bluebird_bio_commercialization_failure_case",
        "COMMERCIALIZATION_FAILURE",
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
        ("slow_uptake", "reimbursement_uncertainty", "cash_runway_collapse", "discounted_take_private"),
        "approval_without_commercialization_or_cash_runway",
        "needs_price_backfill",
        ("round_145.md Reuters bluebird bio cash crunch",),
        "Approval alone is not EPS/FCF; uptake, reimbursement, revenue, and cash runway must support the case.",
        (E2RArchetype.BIOTECH_PRE_REVENUE_REGULATORY, E2RArchetype.BIOTECH_ROYALTY_COMMERCIALIZATION),
    ),
    Round145CaseCandidate(
        "novo_nordisk_glp1_4b_to_4c_case",
        "STRUCTURAL_SUCCESS_BUT_4B_WATCH",
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
        ("sales_guide_down", "op_guide_down", "price_pressure", "competition", "reimbursement_risk"),
        "crowded_4b_then_4c_when_growth_revision_breaks",
        "needs_price_backfill",
        ("round_145.md Reuters Novo GLP-1 guide down",),
        "A crowded growth winner can move from 4B watch to 4C when revisions break.",
        (E2RArchetype.OBESITY_GLP1_COMMERCIALIZATION, E2RArchetype.THESIS_BREAK_4C),
    ),
    Round145CaseCandidate(
        "equinix_affo_cashflow_integrity_case",
        "AFFO_CASHFLOW_INTEGRITY_RISK",
        "EQIX",
        "Equinix",
        "US",
        "failed_rerating",
        date(2024, 3, 20),
        None,
        None,
        None,
        None,
        ("data_center_reit_ai_demand", "affo_growth", "dividend_yield_story"),
        ("affo_overstatement_allegation", "maintenance_capex_misclassification", "power_constraint", "tenant_concentration"),
        "affo_cashflow_integrity_hard_review",
        "needs_price_backfill",
        ("round_145.md Reuters Hindenburg Equinix short report",),
        "Data-center REIT candidates require AFFO, capex, funding-cost, and dividend-coverage checks.",
        (E2RArchetype.DATA_CENTER_REIT_INFRASTRUCTURE, E2RArchetype.COLD_CHAIN_REIT_LOGISTICS),
    ),
    Round145CaseCandidate(
        "equinix_capex_affo_dilution_case",
        "CAPEX_AFFO_DILUTION_RISK",
        "EQIX",
        "Equinix",
        "US",
        "4c_thesis_break",
        date(2026, 5, 1),
        None,
        None,
        None,
        date(2026, 5, 8),
        ("data_center_reit_ai_demand", "capex_budget", "affo_per_share_growth", "dividend_coverage_ratio"),
        (
            "capex_growth_above_affo_growth",
            "affo_per_share_miss",
            "funding_cost_spike",
            "power_constraint",
            "tenant_concentration",
        ),
        "capex_growth_outpaces_affo_per_share_growth",
        "needs_price_backfill",
        ("round_145.md Reuters Equinix capex / AFFO per share disappointment",),
        "Data-center real-asset demand is not enough if capex growth dilutes AFFO per share or funding cost breaks dividend coverage.",
        (E2RArchetype.DATA_CENTER_REIT_INFRASTRUCTURE, E2RArchetype.DATA_CENTER_CAPEX_AFFO_DILUTION),
    ),
    Round145CaseCandidate(
        "opendart_disclosure_confidence_cap_reference_case",
        "DISCLOSURE_CONFIDENCE_CAPPED",
        "DISCLOSURE_CAP",
        "OpenDART detail confidence cap reference",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("disclosure_detected", "contract_headline", "opendart_list_only"),
        ("detail_missing", "customer_undisclosed", "contract_amount_missing", "purpose_missing", "margin_unknown"),
        "disclosure_confidence_capped_until_detail_fields_are_verified",
        "needs_price_backfill",
        ("round_145.md disclosure confidence cap rule",),
        "A list-only contract headline can route Layer 1, but Stage 3 is capped until detail fields such as amount, customer/use, and duration or margin are verified.",
        (E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,),
    ),
    Round145CaseCandidate(
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
        ("round_145.md price-only rally definition",),
        "A price-only rally is useful for detection but cannot create Stage 3-Green.",
        (E2RArchetype.THEME_VALUATION_OVERHEAT,),
    ),
    Round145CaseCandidate(
        "event_premium_policy_mou_case",
        "EVENT_PREMIUM",
        "EVENT_PREMIUM",
        "event premium policy/MOU reference case",
        "GLOBAL",
        "event_premium",
        None,
        None,
        None,
        None,
        None,
        ("policy_announcement", "mou", "headline_event"),
        ("policy_only", "unfunded_budget", "no_revenue_conversion"),
        "event_premium_not_structural_green",
        "needs_price_backfill",
        ("round_145.md event premium bucket",),
        "Policy, MOU, disease, disaster, or tender premium must be separated from structural EPS/FCF rerating.",
        (E2RArchetype.ONE_OFF_EVENT_DEMAND,),
    ),
    Round145CaseCandidate(
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
        ("round_145.md cyclical success rule",),
        "Cycle wins can be valid but should not be mislabeled as structural Green.",
        (E2RArchetype.SHIPPING_FREIGHT_CYCLE, E2RArchetype.COMMODITY_SPREAD),
    ),
    Round145CaseCandidate(
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
        ("round_145.md false-positive score rule",),
        "High score from weak proxies should be treated as calibration failure.",
    ),
    Round145CaseCandidate(
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
        ("round_145.md evidence-good price-failed rule",),
        "Good evidence without price-frame validation should recalibrate mispricing, not force Green.",
    ),
    Round145CaseCandidate(
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
        ("round_145.md legal/regulatory RedTeam rule",),
        "Approval, license, and legal scope must be verified before evidence supports Green.",
    ),
    Round145CaseCandidate(
        "leverage_fcf_breakdown_reference_case",
        "LEVERAGE_FCF_BREAKDOWN",
        "FCF_BREAK",
        "leverage/FCF breakdown reference case",
        "GLOBAL",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        None,
        ("growth_story", "capex_need", "funding_need"),
        ("negative_fcf", "debt_refinancing_pressure", "interest_expense_spike", "dividend_cut", "going_concern"),
        "leverage_fcf_breakdown_blocks_green",
        "needs_price_backfill",
        ("round_145.md leverage/FCF breakdown rule",),
        "Growth does not equal E2R when FCF and refinancing capacity break.",
    ),
    Round145CaseCandidate(
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
        ("round_145.md insufficient evidence rule",),
        "Unknown evidence must remain unknown; missing fields are not filled.",
    ),
    Round145CaseCandidate(
        "ge_vernova_power_equipment_backlog_structural_case",
        "STRUCTURAL_SUCCESS_ALIGNED",
        "GEV",
        "GE Vernova",
        "US",
        "structural_success",
        date(2026, 4, 22),
        date(2026, 4, 22),
        date(2026, 4, 22),
        None,
        None,
        ("backlog_growth", "revenue_guidance_raise", "adjusted_ebitda_margin_raise", "power_electrification_profit", "price_path_aligned"),
        ("wind_segment_loss", "tariff_cost", "segment_drag_watch"),
        "power_equipment_backlog_to_fcf_structural_aligned",
        "needs_price_backfill",
        ("round_145.md Reuters GE Vernova outlook and backlog",),
        "Power equipment backlog can pass R13 when revenue, margin guidance, and price path move together, while segment drag stays visible.",
        (E2RArchetype.POWER_EQUIPMENT_BACKLOG_TO_FCF, E2RArchetype.AI_DATA_CENTER_POWER_EQUIPMENT),
    ),
    Round145CaseCandidate(
        "datadog_ai_observability_structural_case",
        "STRUCTURAL_SUCCESS_ALIGNED",
        "DDOG",
        "Datadog",
        "US",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("observability_ai_operations", "arr_billings_bookings", "retention_visible", "opm_expansion"),
        ("guidance_risk", "cloud_budget_slowdown", "multiple_expansion_ahead_of_eps"),
        "observability_ai_operations_needs_price_and_guidance_validation",
        "needs_price_backfill",
        ("round_145.md R13 structural success list",),
        "AI observability can remain a structural candidate only if ARR, retention, OPM, FCF, and price path align.",
        (E2RArchetype.OBSERVABILITY_AI_OPERATIONS, E2RArchetype.PLATFORM_SOFTWARE_INTERNET),
    ),
    Round145CaseCandidate(
        "intuitive_surgical_recurring_instruments_case",
        "STRUCTURAL_SUCCESS_ALIGNED",
        "ISRG",
        "Intuitive Surgical",
        "US",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("installed_base", "recurring_instruments_accessories", "procedure_growth", "opm_expansion"),
        ("procedure_mix_risk", "reimbursement_risk", "competition"),
        "surgical_robot_recurring_consumables_needs_price_alignment",
        "needs_price_backfill",
        ("round_145.md R13 structural success list",),
        "Recurring instruments and accessories can validate device quality when procedure growth, OPM, FCF, and price path align.",
        (E2RArchetype.SURGICAL_ROBOT_INSTALLED_BASE, E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT),
    ),
    Round145CaseCandidate(
        "samyang_buldak_export_asp_structural_case",
        "STRUCTURAL_SUCCESS_ALIGNED",
        "003230",
        "Samyang Foods",
        "KR",
        "structural_success",
        date(2024, 5, 1),
        date(2024, 5, 1),
        None,
        None,
        None,
        ("buldak_export_growth", "asp_increase", "op_revision", "channel_expansion", "price_path_aligned"),
        ("one_product_fad_risk", "recall_regulatory_risk", "inventory_channel_risk"),
        "export_recurring_consumer_structural_but_channel_risk_watch",
        "needs_price_backfill",
        ("round_145.md R13 structural success list",),
        "Export consumer winners can pass R13 without contract evidence when export mix, ASP, OP revisions, channel expansion, and price path align.",
        (E2RArchetype.EXPORT_RECURRING_CONSUMER,),
    ),
    Round145CaseCandidate(
        "bavarian_nordic_stockpile_guidance_stage2_case",
        "EVENT_TO_CONTRACT_ESCALATION",
        "BAVA",
        "Bavarian Nordic",
        "DK",
        "success_candidate",
        date(2026, 5, 11),
        date(2026, 5, 11),
        None,
        None,
        None,
        ("disease_event", "government_stockpile_order", "contract_value", "revenue_guidance_raise", "ebitda_margin_guidance_raise"),
        ("one_off_stockpile", "repeat_procurement_unproven", "event_normalization"),
        "government_stockpile_revenue_guidance_stage2",
        "needs_price_backfill",
        ("round_145.md Reuters Bavarian Nordic stockpile contract and guidance",),
        "Disease events are not discarded; they become Stage 2 when stockpile contract value and guidance appear, but recurring procurement is still required for Stage 3.",
        (E2RArchetype.GOVERNMENT_STOCKPILE_REVENUE_GUIDANCE, E2RArchetype.ONE_OFF_EVENT_DEMAND),
    ),
    Round145CaseCandidate(
        "samsung_hbm4_shipment_stage2_case",
        "EVENT_TO_CONTRACT_ESCALATION",
        "005930",
        "Samsung Electronics HBM4 shipment",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("hbm4_shipment", "customer_validation", "memory_price", "eps_revision_candidate"),
        ("catchup_execution_risk", "customer_qualification_risk", "margin_gap_to_leader"),
        "hbm4_shipment_stage2_until_eps_price_validation",
        "needs_price_backfill",
        ("round_145.md Stage 2 but not Green list",),
        "HBM4 shipment can route Stage 2 research, but Green waits for EPS/FCF conversion and price-path validation.",
        (E2RArchetype.HBM_CATCHUP_EXECUTION, E2RArchetype.MEMORY_HBM_CAPACITY),
    ),
    Round145CaseCandidate(
        "lges_tesla_ess_contract_stage2_case",
        "EVENT_TO_CONTRACT_ESCALATION",
        "373220",
        "LG Energy Solution Tesla ESS contract",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("ess_contract", "customer_tesla", "contract_value", "lansing_production", "revenue_recognition_path"),
        ("ramp_margin_risk", "contract_cancellation_risk", "ess_safety_permitting"),
        "ess_contract_stage2_until_ramp_margin_and_price_validation",
        "needs_price_backfill",
        ("round_145.md Stage 2 but not Green list",),
        "A named ESS contract can reach Stage 2, but R13 still asks whether ramp, margin, FCF, and price path validate.",
        (E2RArchetype.ESS_TESLA_MEGAPACK_SUPPLY_CHAIN, E2RArchetype.ESS_LFP_GRID_STORAGE),
    ),
    Round145CaseCandidate(
        "kbeauty_channel_entry_stage2_case",
        "EVENT_TO_CONTRACT_ESCALATION",
        "KBEAUTY_CHANNEL",
        "K-beauty channel entry reference",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("us_japan_channel_entry", "retailer_listing", "repeat_order_candidate", "export_growth"),
        ("channel_stuffing", "inventory_risk", "receivables_risk", "single_brand_fad"),
        "kbeauty_channel_entry_stage2_until_repeat_sellthrough",
        "needs_price_backfill",
        ("round_145.md Stage 2 but not Green list",),
        "K-beauty retail entry is Stage 2 evidence only after sell-through, repeat orders, OPM, and FCF validate it.",
        (E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,),
    ),
    Round145CaseCandidate(
        "biosimilar_pbm_formulary_stage2_case",
        "EVENT_TO_CONTRACT_ESCALATION",
        "BIOSIMILAR_PBM",
        "biosimilar PBM/formulary reference",
        "GLOBAL",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("pbm_formulary", "access_channel", "prescription_volume_candidate", "commercial_revenue_candidate"),
        ("originator_defense", "rebate_pressure", "patent_litigation", "uptake_slow"),
        "biosimilar_pbm_stage2_until_prescription_and_revenue",
        "needs_price_backfill",
        ("round_145.md Stage 2 but not Green list",),
        "PBM/formulary access can be Stage 2, but prescriptions, revenue, reimbursement, and FCF decide Stage 3.",
        (E2RArchetype.BIOSIMILAR_PBM_FORMULARY_SWITCH, E2RArchetype.BIOSIMILAR_COMMERCIALIZATION),
    ),
    Round145CaseCandidate(
        "zoetis_conditional_vaccine_stage2_case",
        "EVENT_TO_CONTRACT_ESCALATION",
        "ZTS",
        "Zoetis conditional bird-flu vaccine license",
        "US",
        "success_candidate",
        date(2025, 2, 14),
        date(2025, 2, 14),
        None,
        None,
        None,
        ("conditional_license", "biosecurity_demand", "government_stockpile_candidate"),
        ("one_off_outbreak", "repeat_vaccination_unproven", "vaccine_unused_risk"),
        "conditional_vaccine_license_stage2_until_actual_order",
        "needs_price_backfill",
        ("round_145.md Stage 2 but not Green list",),
        "A conditional animal-health license can reach Stage 2 only if government order or repeat use follows.",
        (E2RArchetype.ANIMAL_HEALTH_BIOSECURITY,),
    ),
    Round145CaseCandidate(
        "palantir_enterprise_ai_4b_watch_case",
        "STRUCTURAL_SUCCESS_BUT_4B_WATCH",
        "PLTR",
        "Palantir enterprise AI",
        "US",
        "4b_watch",
        None,
        None,
        None,
        None,
        None,
        ("enterprise_ai_platform", "government_programs", "revenue_growth", "price_path_aligned"),
        ("valuation_saturation", "consensus_crowded", "multiple_expansion_ahead_of_eps"),
        "enterprise_ai_structural_but_4b_watch",
        "needs_price_backfill",
        ("round_145.md success but 4B list",),
        "Enterprise AI can be structurally strong and still be 4B-watch when valuation room has compressed.",
        (E2RArchetype.ENTERPRISE_AI_ONTOLOGY_WORKFLOW, E2RArchetype.GOVERNMENT_AI_PROGRAM_OF_RECORD),
    ),
    Round145CaseCandidate(
        "akamai_edge_ai_cloud_4b_watch_case",
        "STRUCTURAL_SUCCESS_BUT_4B_WATCH",
        "AKAM",
        "Akamai edge AI cloud",
        "US",
        "4b_watch",
        None,
        None,
        None,
        None,
        None,
        ("edge_ai_cloud", "security_platform", "cloud_infra_repositioning"),
        ("valuation_room_reduced", "cloud_capex_margin_risk", "competitive_pressure"),
        "edge_ai_cloud_structural_but_4b_watch",
        "needs_price_backfill",
        ("round_145.md success but 4B list",),
        "Edge AI cloud rerating needs 4B monitoring when the new frame is already accepted.",
        (E2RArchetype.EDGE_AI_CLOUD_INFRASTRUCTURE, E2RArchetype.CLOUD_AI_SOFTWARE_INFRA),
    ),
    Round145CaseCandidate(
        "apr_beauty_device_4b_watch_case",
        "STRUCTURAL_SUCCESS_BUT_4B_WATCH",
        "278470",
        "APR beauty device",
        "KR",
        "4b_watch",
        None,
        None,
        None,
        None,
        None,
        ("beauty_device_export", "overseas_sales_growth", "opm_expansion", "price_path_aligned"),
        ("valuation_saturation", "device_replacement_cycle", "channel_inventory_risk"),
        "beauty_device_structural_but_4b_watch",
        "needs_price_backfill",
        ("round_145.md success but 4B list",),
        "Beauty-device winners can be structurally valid and still need 4B valuation-room checks after a large run.",
        (E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION, E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT),
    ),
    Round145CaseCandidate(
        "kioxia_nand_rerating_4b_watch_case",
        "STRUCTURAL_SUCCESS_BUT_4B_WATCH",
        "KIOXIA",
        "Kioxia NAND",
        "JP",
        "4b_watch",
        None,
        None,
        None,
        None,
        None,
        ("nand_price_recovery", "ai_storage_demand", "op_revision", "price_path_aligned"),
        ("memory_cycle_reversal", "capex_supply_response", "valuation_saturation"),
        "nand_rerating_structural_but_4b_watch",
        "needs_price_backfill",
        ("round_145.md success but 4B list",),
        "NAND rerating can be real but still requires cycle and 4B checks after price has moved.",
        (E2RArchetype.AI_STORAGE_NAND_SHORTAGE, E2RArchetype.COMMODITY_MEMORY_GENERAL_SEMI),
    ),
    Round145CaseCandidate(
        "coupang_trust_security_break_case",
        "OPERATIONAL_TRUST_BREAK",
        "CPNG",
        "Coupang trust/security break reference",
        "KR",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        None,
        ("platform_scale", "logistics_execution", "recurring_customer_activity"),
        ("security_outage", "privacy_breach", "customer_damage", "operational_trust_break"),
        "platform_trust_security_hard_4c",
        "needs_price_backfill",
        ("round_145.md hard 4C list",),
        "Platform scale does not protect Green if customer trust or security breaks.",
        (E2RArchetype.PLATFORM_SOFTWARE_INTERNET, E2RArchetype.SECURITY_OPERATIONAL_TRUST_OVERLAY),
    ),
    Round145CaseCandidate(
        "whirlpool_hardware_cycle_fcf_breakdown_case",
        "LEVERAGE_FCF_BREAKDOWN",
        "WHR",
        "Whirlpool hardware cycle",
        "US",
        "4c_thesis_break",
        date(2026, 5, 7),
        None,
        None,
        None,
        date(2026, 5, 7),
        ("home_appliance_hardware", "replacement_cycle", "dividend_suspension", "guidance_cut"),
        ("dividend_cut", "fcf_guidance_cut", "replacement_demand_collapse", "debt_reduction_pressure"),
        "hardware_cycle_fcf_breakdown_4c",
        "needs_price_backfill",
        ("round_145.md hard 4C list",),
        "Hardware replacement-cycle stories are blocked when dividend, FCF guidance, or demand breaks.",
        (E2RArchetype.HOME_APPLIANCE_HARDWARE_CYCLE,),
    ),
    Round145CaseCandidate(
        "hertz_ev_fleet_unit_economics_break_case",
        "LEVERAGE_FCF_BREAKDOWN",
        "HTZ",
        "Hertz EV fleet economics",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        None,
        ("ev_fleet_strategy", "used_car_rental_mobility", "fleet_transition"),
        ("residual_value_loss", "maintenance_cost", "debt_refinancing_pressure", "unit_economics_failure"),
        "ev_fleet_unit_economics_4c",
        "needs_price_backfill",
        ("round_145.md hard 4C list",),
        "EV fleet narratives fail R13 when residual values, maintenance cost, leverage, and unit economics break.",
        (E2RArchetype.EV_RENTAL_UNIT_ECONOMICS, E2RArchetype.RENTAL_USED_CAR_MOBILITY),
    ),
    Round145CaseCandidate(
        "lk99_replication_failure_false_positive_case",
        "FALSE_POSITIVE_SCORE",
        "LK99_THEME",
        "LK-99 replication failure theme basket",
        "GLOBAL",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        None,
        ("preprint_or_social_theme", "theme_basket_rally", "price_spike"),
        ("replication_failure", "no_revenue_conversion", "price_failed", "evidence_unverified"),
        "scientific_theme_replication_failure_4c",
        "needs_price_backfill",
        ("round_145.md hard 4C list",),
        "Scientific-theme price spikes are false positives when replication and commercialization evidence fail.",
        (E2RArchetype.THEME_VALUATION_OVERHEAT, E2RArchetype.UNKNOWN_INSUFFICIENT_EVIDENCE),
    ),
)


ROUND145_PRICE_FIELDS: tuple[str, ...] = (
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
    "MFE_5D",
    "MFE_20D",
    "MFE_30D",
    "MFE_60D",
    "MFE_90D",
    "MFE_180D",
    "MFE_1Y",
    "MFE_2Y",
    "MAE_5D",
    "MAE_20D",
    "MAE_30D",
    "MAE_60D",
    "MAE_90D",
    "MAE_180D",
    "MAE_1Y",
    "drawdown_after_peak",
    "below_stage1_price_flag",
    "below_stage2_price_flag",
    "below_stage3_price_flag",
    "revenue_revision_1q",
    "revenue_revision_1y",
    "op_revision_1q",
    "op_revision_1y",
    "eps_revision_1q",
    "eps_revision_1y",
    "fcf_margin_change",
    "gross_margin_change",
    "op_margin_change",
    "valuation_metric_before",
    "valuation_metric_after",
    "pbr_before",
    "pbr_after",
    "per_before",
    "per_after",
    "ev_ebitda_before",
    "ev_ebitda_after",
    "contract_value",
    "contract_duration_months",
    "contract_amount_to_sales",
    "contract_start_date",
    "contract_end_date",
    "counterparty",
    "product_or_service",
    "backlog_growth",
    "capacity_utilization",
    "customer_concentration",
    "disclosure_type",
    "opendart_rcept_no",
    "opendart_detail_fetched_flag",
    "opendart_detail_cache_path",
    "detail_parser_confidence",
    "disclosure_signal_class",
    "routine_disclosure_flag",
    "risk_disclosure_flag",
    "high_signal_disclosure_flag",
    "disclosure_confidence_score",
    "facility_investment_amount",
    "facility_investment_to_market_cap",
    "expected_completion_date",
    "dilution_type",
    "share_issuance_amount",
    "convertible_bond_amount",
    "bw_amount",
    "debt_to_ebitda",
    "net_debt",
    "interest_expense",
    "cash_runway_months",
    "refinancing_risk_flag",
    "dividend_cut_flag",
    "buyback_cancelled_flag",
    "auditor_resignation_flag",
    "filing_delay_flag",
    "internal_control_issue_flag",
    "regulatory_probe_flag",
    "related_party_risk_flag",
    "security_outage_flag",
    "privacy_breach_flag",
    "customer_lawsuit_flag",
    "operational_trust_break_flag",
    "approval_status",
    "commercial_revenue",
    "patient_uptake",
    "reimbursement_status",
    "going_concern_flag",
    "affo_growth",
    "noi_growth",
    "maintenance_capex",
    "expansion_capex",
    "capex_to_affo_ratio",
    "affo_per_share_growth",
    "affo_integrity_risk_flag",
    "capex_affo_dilution_risk_flag",
    "capex_growth_above_affo_growth_flag",
    "power_water_permitting_flag",
    "tenant_concentration_flag",
    "ai_power_campus_flag",
    "asset_acquired_flag",
    "binding_lease_flag",
    "binding_tenant_lease_absent",
    "no_revenue_flag",
    "power_delivery_long_dated_flag",
    "ipo_valuation",
    "dividend_coverage_ratio",
    "stablecoin_type",
    "depeg_event_flag",
    "reserve_failure_flag",
    "convertibility_risk_flag",
    "algorithmic_stablecoin_flag",
    "stablecoin_circulation",
    "reserve_income",
    "redemption_at_par_flag",
    "circular_financing_flag",
    "supplier_investor_customer_loop_flag",
    "capacity_guarantee_flag",
    "gpu_collateral_debt_flag",
    "customer_contract_concentration",
    "event_only_flag",
    "cycle_only_flag",
    "price_only_rally_flag",
    "crowded_4b_flag",
    "hard_4c_flag",
    "policy_market_shock_flag",
    "unknown_insufficient_evidence_flag",
    "disclosure_confidence_capped_flag",
    "contract_amount_disclosed_flag",
    "customer_name_disclosed_flag",
    "use_of_proceeds_or_contract_purpose_disclosed_flag",
    "margin_disclosed_flag",
    "stage_confidence_cap_reason",
    "score_before_redteam",
    "score_after_redteam",
    "stage_before_redteam",
    "stage_after_redteam",
    "score_price_alignment",
    "price_validation_status",
    "review_notes",
)


def round145_target_for(target_id: str) -> Round145OverlayTarget | None:
    for target in ROUND145_OVERLAY_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round145_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND145_CASE_CANDIDATES:
        target = round145_target_for(candidate.target_id)
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
                f"Round145 R13 Loop-8 cross-archetype validation case for {candidate.target_id}; "
                "this is calibration-only and does not change production scoring."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage2_signals),
            stage3_evidence=tuple(
                field for field in candidate.evidence_fields if field in target.stage3_conditions or field in target.green_conditions
            ),
            stage4b_evidence=candidate.evidence_fields if candidate.stage4b_date or candidate.target_id == "STRUCTURAL_SUCCESS_BUT_4B_WATCH" else (),
            stage4c_evidence=candidate.red_flag_fields if candidate.stage4c_date or target.hard_gate else (),
            must_have_fields=target.green_conditions,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason=(
                "; ".join(candidate.red_flag_fields)
                if candidate.case_type in {"event_premium", "overheat", "failed_rerating", "4b_watch", "4c_thesis_break", "one_off"}
                else None
            ),
            score_price_alignment=_round145_score_price_alignment(candidate),
            rerating_result=_round145_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
            score_weight_hint=_round145_score_weight_hint(target),
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "require_price_path_validation",
                "stage3_green_requires_cross_evidence_eps_fcf_price_alignment_no_hard_redteam_no_saturated_4b",
                "price_only_rally_is_not_green_evidence",
                "event_or_cycle_success_is_not_structural_green_by_itself",
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
                stage_dates_confidence=0.7
                if candidate.stage1_date or candidate.stage2_date or candidate.stage4b_date or candidate.stage4c_date
                else 0.25,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round145_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND145_OVERLAY_TARGETS:
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


def round145_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND145_CASE_CANDIDATES:
        target = round145_target_for(candidate.target_id)
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


def round145_stage_date_rows() -> tuple[dict[str, str], ...]:
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
        for target in ROUND145_OVERLAY_TARGETS
    )


def round145_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round145_backfill": "true"} for field in ROUND145_PRICE_FIELDS)


def round145_overlay_axis_rows() -> tuple[dict[str, str], ...]:
    return tuple(axis.as_csv_dict() for axis in ROUND145_OVERLAY_AXES)


def round145_stage_cap_rows() -> tuple[dict[str, str], ...]:
    return tuple(cap.as_dict() for cap in ROUND145_STAGE_CAPS)


def round145_summary() -> dict[str, int | bool]:
    records = round145_case_records()
    return {
        "target_count": len(ROUND145_OVERLAY_TARGETS),
        "overlay_axis_count": len(ROUND145_OVERLAY_AXES),
        "stage_cap_count": len(ROUND145_STAGE_CAPS),
        "case_candidate_count": len(records),
        "structural_success_count": sum(1 for record in records if record.case_type == "structural_success"),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "cyclical_success_count": sum(1 for record in records if record.case_type == "cyclical_success"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "overheat_count": sum(1 for record in records if record.case_type == "overheat"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "hard_gate_target_count": sum(1 for target in ROUND145_OVERLAY_TARGETS if target.hard_gate),
        "green_possible_count": sum(1 for target in ROUND145_OVERLAY_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND145_OVERLAY_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND145_OVERLAY_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round145_r13_loop8_reports(
    *,
    output_directory: str | Path = ROUND145_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND145_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND145_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round145_r13_loop8_cross_archetype_redteam_summary.md",
        "case_matrix": output / "round145_r13_loop8_case_matrix.csv",
        "target_matrix": output / "round145_r13_loop8_overlay_target_matrix.csv",
        "stage_date_plan": output / "round145_r13_loop8_stage_date_plan.csv",
        "redteam_gate_plan": output / "round145_r13_loop8_redteam_gate_plan.md",
        "price_validation_plan": output / "round145_r13_loop8_price_validation_plan.md",
        "price_fields": output / "round145_r13_loop8_price_fields.csv",
        "overlay_axes": output / "round145_r13_loop8_overlay_axes.csv",
        "stage_caps": output / "round145_r13_loop8_stage_caps.csv",
    }
    _write_case_jsonl(round145_case_records(), cases)
    _write_rows(round145_score_profile_rows(), score_profiles)
    _write_rows(round145_score_profile_rows(), paths["target_matrix"])
    _write_rows(round145_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round145_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round145_price_field_rows(), paths["price_fields"])
    _write_rows(round145_overlay_axis_rows(), paths["overlay_axes"])
    _write_rows(round145_stage_cap_rows(), paths["stage_caps"])
    paths["summary"].write_text(render_round145_summary_markdown(), encoding="utf-8")
    paths["redteam_gate_plan"].write_text(render_round145_redteam_gate_plan_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round145_price_validation_plan_markdown(), encoding="utf-8")
    return paths


def render_round145_summary_markdown() -> str:
    summary = round145_summary()
    lines = [
        "# Round-145 R13 Loop-8 Cross-Archetype RedTeam / 4B / Price Validation",
        "",
        f"- source_round: `{ROUND145_SOURCE_ROUND_PATH}`",
        f"- large_sector: `{ROUND145_LARGE_SECTOR}`",
        f"- target_count: {summary['target_count']}",
        f"- overlay_axis_count: {summary['overlay_axis_count']}",
        f"- stage_cap_count: {summary['stage_cap_count']}",
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
        "- Round 145 is a common validation overlay, not a sector score-owner.",
        "- High score is not enough. Stage 3-Green needs cross-evidence, EPS/FCF durability, price-path alignment, no hard RedTeam, and no saturated 4B.",
        "- Example: SK하이닉스 HBM can be structurally aligned and also require 4B-watch because the new frame is already crowded.",
        "- Example: Supermicro-style auditor resignation blocks Green even if prior AI-server revenue was strong.",
        "- Example: data-center real assets require AFFO-per-share, capex, tenant, funding-cost, and power/water checks before structural confidence.",
        "- Example: AI cloud contracts are capped if supplier, investor, customer, and capacity-guarantee economics form a circular financing loop.",
        "- Example: OpenDART list-only contract headlines are capped until amount, customer/use, and duration or margin detail is verified.",
        "- Example: a policy/MOU event stays Event Premium until funded contract, order, budget, or earnings evidence appears.",
        "",
        "## R13 v8 Cross-Archetype Overlay Axes",
        "",
    ]
    for axis in ROUND145_OVERLAY_AXES:
        lines.append(f"- `{axis.axis_id}`: {axis.weight}")
    lines.extend(
        [
            "",
            "## R13 v8 Stage Caps",
            "",
        ]
    )
    for cap in ROUND145_STAGE_CAPS:
        lines.append(f"- `{cap.cap_id}`: {cap.stage_band} / {cap.score_cap}")
    lines.extend(
        [
            "",
            "Stage 3-Green remains blocked unless sector score, EPS/FCF bodyweight change, repeatability, price-path alignment, disclosure confidence, 4B valuation room, and no hard 4C flag all line up.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round145_redteam_gate_plan_markdown() -> str:
    lines = [
        "# Round-145 R13 Loop-8 RedTeam Gate Plan",
        "",
        "| target | posture | hard gate | Green allowed | Red flags |",
        "| --- | --- | --- | --- | --- |",
    ]
    for target in ROUND145_OVERLAY_TARGETS:
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
            "- Do not apply Round145 overlay symbols to production scoring yet.",
            "- Do not lower Stage 3-Green to improve recall.",
            "- Do not use R13 Loop-8 case records as candidate-generation input.",
            "- Do not treat price-only movement, event premium, or cycle success as structural Green by itself.",
            "- Do not ignore hard RedTeam evidence such as auditor resignation, filing delay, global outage, regulatory denial, cash runway collapse, AFFO integrity risk, capex/AFFO dilution, circular AI financing, or stablecoin de-peg.",
            "- Do not let list-only disclosures support Stage 3 without detail confidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round145_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-145 R13 Loop-8 Price / Stage Validation Plan",
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
    for row in round145_case_candidate_rows():
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
            "- `thesis_break`: 4C evidence such as audit, trust, legal, cash runway, commercialization, AFFO, or convertibility break appears.",
            "- `disclosure_confidence_capped`: contract/list evidence exists, but core detail is missing, so Stage 3 confidence is capped.",
            "- `contract_visibility_but_circular_financing_watch`: AI contract visibility remains capped until arm's-length financing, FCF, leverage, and customer concentration are verified.",
        ]
    )
    return "\n".join(lines) + "\n"


def _round145_score_price_alignment(candidate: Round145CaseCandidate) -> str:
    if "insufficient" in candidate.alignment_hint:
        return "unknown"
    if "evidence_good_but_price_failed" in candidate.alignment_hint:
        return "evidence_good_but_price_failed"
    if candidate.case_type in {"structural_success", "success_candidate", "cyclical_success"}:
        return "aligned"
    if candidate.case_type in {"event_premium", "overheat", "4b_watch"}:
        return "price_moved_without_evidence"
    return "false_positive_score"


def _round145_rerating_result(candidate: Round145CaseCandidate) -> str:
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
    if "policy_to_execution" in candidate.alignment_hint:
        return "policy_event_rerating"
    return "unknown" if "insufficient" in candidate.alignment_hint else "no_rerating"


def _round145_score_weight_hint(target: Round145OverlayTarget) -> dict[str, float]:
    weights = target.score_weight.as_dict()
    return {
        "eps_fcf": _round145_symbolic_weight(weights["eps_fcf"]),
        "visibility": _round145_symbolic_weight(weights["structural_visibility"]),
        "bottleneck": _round145_symbolic_weight(weights["bottleneck_pricing"]),
        "mispricing": _round145_symbolic_weight(weights["market_mispricing"]),
        "valuation": _round145_symbolic_weight(weights["valuation"]),
        "capital_allocation": _round145_symbolic_weight(weights["capital_allocation"]),
        "information_confidence": _round145_symbolic_weight(weights["information_confidence"]),
    }


def _round145_symbolic_weight(value: str) -> float:
    return {
        "+": 1.0,
        "0": 0.0,
        "-": -1.0,
        "low": 0.25,
        "medium": 0.5,
        "optional": 0.25,
        "maintain": 0.5,
        "weaken": -0.5,
        "deduct": -1.0,
        "gate": 0.0,
        "cap": 0.0,
        "hard-": -5.0,
        "0~+": 0.5,
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
        writer = csv.DictWriter(handle, fieldnames=tuple(rows_tuple[0].keys()), lineterminator="\n")
        writer.writeheader()
        for row in rows_tuple:
            writer.writerow(dict(row))
    return path


__all__ = [
    "ROUND145_CASE_CANDIDATES",
    "ROUND145_DEFAULT_CASES_PATH",
    "ROUND145_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND145_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND145_LARGE_SECTOR",
    "ROUND145_OVERLAY_AXES",
    "ROUND145_OVERLAY_TARGETS",
    "ROUND145_PRICE_FIELDS",
    "ROUND145_STAGE_CAPS",
    "Round145CaseCandidate",
    "Round145OverlayAxis",
    "Round145OverlayTarget",
    "Round145OverlayWeightDraft",
    "Round145StageCap",
    "render_round145_price_validation_plan_markdown",
    "render_round145_redteam_gate_plan_markdown",
    "render_round145_summary_markdown",
    "round145_case_candidate_rows",
    "round145_case_records",
    "round145_overlay_axis_rows",
    "round145_price_field_rows",
    "round145_score_profile_rows",
    "round145_stage_date_rows",
    "round145_stage_cap_rows",
    "round145_summary",
    "round145_target_for",
    "write_round145_r13_loop8_reports",
]
