"""Round-35 cases_v17 expansion and score-weight v2.0 hypotheses.

Round 35 adds healthcare commercialization and service automation cases that
often look attractive in headlines but need strict monetization checks:
biosimilars, GLP-1 obesity drugs, gene therapy, AI drug discovery, contact
center AI, kiosks/self-checkout, originator patent-cliff defense, and pharma
platform regulatory risk. This is report-only calibration material. Production
feature engineering, scoring, staging, and RedTeam code must not import this
module.
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


ROUND35_SOURCE_ROUND_PATH = "docs/round/round_35.md"
ROUND35_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round35_score_weight_v20"
ROUND35_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_v17_round35.jsonl"
ROUND35_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round35_v20.csv"


@dataclass(frozen=True)
class Round35ScoreWeightDraft:
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
class Round35ScoreTarget:
    target_id: str
    large_sector: Round10LargeSector
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round35ScoreWeightDraft
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
class Round35CaseCandidate:
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


ROUND35_SCORE_TARGETS: tuple[Round35ScoreTarget, ...] = (
    Round35ScoreTarget(
        "BIOSIMILAR_COMMERCIALIZATION",
        Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE,
        E2RArchetype.BIOTECH_ROYALTY_COMMERCIALIZATION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round35ScoreWeightDraft(18, 20, 6, 13, 11, 0, 6),
        ("biosimilar_approval", "patent_expiry", "launch_news", "price_discount"),
        ("payer_or_pbm_adoption", "prescription_volume_growth", "manufacturing_cost_advantage", "multi_country_launch"),
        ("margin_defense", "uptake_visible", "competition_intensity_controlled"),
        ("payer_or_pbm_adoption", "prescription_volume_growth", "manufacturing_cost_advantage", "margin_defense"),
        ("price_competition", "payer_adoption", "pbm_incentive", "margin_pressure", "approval_only"),
        ("price_margin_collapse", "payer_rejection", "supply_quality_issue", "uptake_failure"),
        "Biosimilar approval is only Stage 1; prescription conversion, payer access, and margin defense unlock higher stages.",
    ),
    Round35ScoreTarget(
        "OBESITY_GLP1_COMMERCIALIZATION",
        Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE,
        E2RArchetype.BIOTECH_ROYALTY_COMMERCIALIZATION,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round35ScoreWeightDraft(22, 20, 12, 13, 12, 0, 6),
        ("glp1_demand", "obesity_market", "oral_glp1", "supply_expansion"),
        ("prescription_volume_growth", "reimbursement_expansion", "supply_capacity", "op_eps_revision"),
        ("competition_risk_controlled", "compounded_drug_risk_controlled", "advertising_regulation_clear"),
        ("prescription_volume_growth", "reimbursement_expansion", "supply_capacity", "op_eps_revision"),
        ("competition", "reimbursement", "supply", "compounded_drugs", "advertising_regulation"),
        ("guidance_cut", "prescription_slowdown", "compounded_substitution", "regulatory_campaign_halt"),
        "GLP-1 can be Green-eligible, but market size alone is not evidence; prescriptions, reimbursement, supply, and revisions matter.",
    ),
    Round35ScoreTarget(
        "GENE_THERAPY_RARE_DISEASE",
        Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE,
        E2RArchetype.BIOTECH_PRE_REVENUE_REGULATORY,
        Round10ThemePosture.REDTEAM_FIRST,
        Round35ScoreWeightDraft(8, 12, 8, 10, 6, 0, 5),
        ("gene_therapy_approval", "rare_disease_unmet_need", "high_price_therapy"),
        ("patient_uptake", "reimbursement_coverage", "treatment_center_ready", "cash_runway"),
        ("commercialization_numbers_visible", "manufacturing_stable", "safety_risk_controlled"),
        ("patient_uptake", "reimbursement_coverage", "commercialization_numbers_visible", "cash_runway"),
        ("commercialization_slow", "reimbursement", "cash_burn", "manufacturing", "safety", "approval_only"),
        ("cash_crunch", "reimbursement_failure", "patient_uptake_failure", "safety_issue"),
        "Gene therapy is RedTeam-first; approval does not equal commercialization or FCF.",
    ),
    Round35ScoreTarget(
        "AI_DRUG_DISCOVERY_PLATFORM",
        Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE,
        E2RArchetype.BIOTECH_PRE_REVENUE_REGULATORY,
        Round10ThemePosture.REDTEAM_FIRST,
        Round35ScoreWeightDraft(6, 10, 7, 12, 6, 0, 5),
        ("ai_drug_platform", "candidate_discovery", "big_pharma_partnership"),
        ("clinical_entry", "milestone_revenue", "cash_runway", "pipeline_diversification"),
        ("late_stage_probability_visible", "approved_or_near_approved_asset", "platform_revenue_visible"),
        ("milestone_revenue", "clinical_entry", "cash_runway", "pipeline_diversification"),
        ("clinical_failure", "no_approved_drug", "cash_burn", "data_quality", "platform_hype"),
        ("trial_failure", "cash_runway_break", "partnership_loss", "data_quality_issue"),
        "AI drug discovery remains Watch/Red until milestones, clinical success, and commercialization evidence appear.",
    ),
    Round35ScoreTarget(
        "CONTACT_CENTER_AI_AUTOMATION",
        Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY,
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round35ScoreWeightDraft(19, 20, 8, 14, 13, 0, 5),
        ("contact_center_ai", "ccaas", "agent_assist", "ai_bot"),
        ("arr_growth", "seat_expansion", "enterprise_retention", "cost_saving_roi"),
        ("opm_or_fcf_improvement", "privacy_risk_controlled", "churn_controlled"),
        ("arr_growth", "seat_expansion", "enterprise_retention", "opm_or_fcf_improvement"),
        ("churn", "it_budget", "privacy", "ai_error", "seat_contraction", "poc_only"),
        ("enterprise_churn_spike", "privacy_incident", "ai_error_liability", "seat_contraction"),
        "Contact-center AI can be Watch-to-Green only when ARR, seats, retention, ROI, and margin evidence are visible.",
    ),
    Round35ScoreTarget(
        "SERVICE_KIOSK_SELF_CHECKOUT",
        Round10LargeSector.CONSUMER_RETAIL_BRAND,
        E2RArchetype.RETAIL_DOMESTIC_CONSUMER,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round35ScoreWeightDraft(17, 15, 7, 12, 10, 0, 5),
        ("kiosk_installation", "self_checkout", "retail_automation", "computer_vision_checkout"),
        ("installed_base_growth", "maintenance_recurring_revenue", "payment_or_software_revenue", "loss_prevention_effect"),
        ("customer_friction_controlled", "theft_risk_controlled", "hardware_mix_low"),
        ("installed_base_growth", "maintenance_recurring_revenue", "payment_or_software_revenue", "loss_prevention_effect"),
        ("theft", "customer_friction", "regulation", "one_off_hardware", "maintenance_cost", "pseudo_automation"),
        ("retailer_rollbacks", "theft_loss_spike", "regulatory_restriction", "customer_backlash"),
        "Kiosk and self-checkout stay Watch-first unless recurring service/software economics and loss-prevention benefits are proven.",
    ),
    Round35ScoreTarget(
        "BIOSIMILAR_ORIGINATOR_DEFENSE",
        Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE,
        E2RArchetype.BIOTECH_ROYALTY_COMMERCIALIZATION,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round35ScoreWeightDraft(19, 18, 8, 13, 11, 2, 6),
        ("patent_cliff", "originator_defense", "successor_drug", "pipeline_transition"),
        ("successor_revenue_growth", "blockbuster_dependence_down", "pipeline_diversification", "eps_fcf_defense"),
        ("pricing_pressure_defended", "erosion_offset_visible", "cash_return_or_capital_strength"),
        ("successor_revenue_growth", "blockbuster_dependence_down", "pipeline_diversification", "eps_fcf_defense"),
        ("patent_cliff", "biosimilar_erosion", "pipeline_failure", "pricing_pressure", "successor_absent"),
        ("successor_failure", "rapid_revenue_erosion", "pipeline_setback", "pricing_power_loss"),
        "Originators can recover if successor drugs offset patent cliffs; otherwise erosion becomes 4C evidence.",
    ),
    Round35ScoreTarget(
        "PHARMA_PLATFORM_REGULATORY_RISK",
        Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE,
        E2RArchetype.BIOTECH_PRE_REVENUE_REGULATORY,
        Round10ThemePosture.REDTEAM_FIRST,
        Round35ScoreWeightDraft(17, 15, 8, 12, 10, 0, 6),
        ("telehealth_prescription", "compounded_drug", "online_pharmacy", "pharma_marketing"),
        ("legal_distribution_channel", "reimbursement_or_pharmacy_network", "quality_control", "recurring_prescription_revenue"),
        ("regulatory_clarity", "safety_quality_visible", "liability_risk_controlled"),
        ("legal_distribution_channel", "quality_control", "regulatory_clarity", "recurring_prescription_revenue"),
        ("fda_warning", "compounding_quality", "illegal_pharmacy", "advertising_rule", "liability", "gray_channel"),
        ("fda_warning", "illegal_distribution", "quality_failure", "advertising_halt", "liability_claim"),
        "Large drug demand does not unlock Green if the channel is gray; regulation, quality, and liability are primary gates.",
    ),
)


ROUND35_CASE_CANDIDATES: tuple[Round35CaseCandidate, ...] = (
    Round35CaseCandidate("humira_biosimilar_discount_access_candidate", "BIOSIMILAR_COMMERCIALIZATION", "HUMIRA_BIO_DISC", "Humira biosimilar discount access candidate", "US", "success_candidate", ("price_discount", "payer_or_pbm_adoption"), ("margin_pressure", "uptake_failure"), "Discount access can help adoption, but needs prescription and margin evidence."),
    Round35CaseCandidate("humira_biosimilar_slow_uptake_counterexample", "BIOSIMILAR_COMMERCIALIZATION", "HUMIRA_SLOW", "Humira biosimilar slow uptake counterexample", "US", "failed_rerating", ("biosimilar_approval", "price_discount"), ("payer_adoption", "uptake_failure"), "Cheaper biosimilar can still fail to convert prescriptions quickly."),
    Round35CaseCandidate("ustekinumab_biosimilar_multi_approval_candidate", "BIOSIMILAR_COMMERCIALIZATION", "USTE_BIO", "Ustekinumab biosimilar multi-approval candidate", "GLOBAL", "success_candidate", ("biosimilar_approval", "multi_country_launch"), ("price_competition", "margin_pressure"), "Multiple approvals expand opportunity but increase price competition."),
    Round35CaseCandidate("biosimilar_price_margin_pressure_4c", "BIOSIMILAR_COMMERCIALIZATION", "BIO_MARGIN_4C", "Biosimilar price margin pressure 4C", "GLOBAL", "4c_thesis_break", ("launch_news",), ("price_margin_collapse", "supply_quality_issue"), "Price discount without margin defense can break the thesis."),
    Round35CaseCandidate("lilly_oral_glp1_foundayo_candidate", "OBESITY_GLP1_COMMERCIALIZATION", "LLY_ORAL", "Lilly oral GLP-1 uptake candidate", "US", "success_candidate", ("oral_glp1", "prescription_volume_growth"), ("competition", "prescription_slowdown"), "Oral GLP-1 can widen market if prescriptions and supply scale."),
    Round35CaseCandidate("novo_wegovy_slowdown_compounded_alternative_4c", "OBESITY_GLP1_COMMERCIALIZATION", "NVO_WEGOVY_4C", "Novo Wegovy slowdown and compounded alternative 4C", "US", "4c_thesis_break", ("glp1_demand",), ("guidance_cut", "compounded_substitution"), "Large GLP-1 demand can still break if competition or compounded alternatives cut guidance."),
    Round35CaseCandidate("glp1_advertising_regulation_india_counterexample", "OBESITY_GLP1_COMMERCIALIZATION", "GLP1_AD_REG", "GLP-1 advertising regulation India counterexample", "IN", "failed_rerating", ("obesity_market",), ("advertising_regulation", "regulatory_campaign_halt"), "Country advertising rules can block commercial narrative."),
    Round35CaseCandidate("oral_glp1_uptake_below_expectation_counterexample", "OBESITY_GLP1_COMMERCIALIZATION", "ORAL_GLP1_SLOW", "Oral GLP-1 uptake below expectation counterexample", "US", "failed_rerating", ("oral_glp1",), ("prescription_slowdown", "reimbursement"), "Launch prescriptions must be compared with revenue expectations."),
    Round35CaseCandidate("bluebird_gene_therapy_approval_but_cash_crunch_4c", "GENE_THERAPY_RARE_DISEASE", "BLUE_4C", "Bluebird gene therapy approval but cash crunch 4C", "US", "4c_thesis_break", ("gene_therapy_approval",), ("cash_crunch", "patient_uptake_failure"), "Approval did not prevent cash crunch when commercialization was slow."),
    Round35CaseCandidate("rare_disease_reimbursement_delay_counterexample", "GENE_THERAPY_RARE_DISEASE", "RARE_REIMB", "Rare disease reimbursement delay counterexample", "GLOBAL", "failed_rerating", ("rare_disease_unmet_need",), ("reimbursement_failure", "commercialization_slow"), "High unmet need still needs reimbursement."),
    Round35CaseCandidate("gene_therapy_patient_uptake_slow_counterexample", "GENE_THERAPY_RARE_DISEASE", "GENE_UPTAKE", "Gene therapy patient uptake slow counterexample", "GLOBAL", "failed_rerating", ("high_price_therapy",), ("patient_uptake_failure", "treatment_center_ready"), "Patient identification and centers can bottleneck launch."),
    Round35CaseCandidate("gene_therapy_commercialization_success_candidate_if_reimbursement", "GENE_THERAPY_RARE_DISEASE", "GENE_COMM", "Gene therapy commercialization candidate if reimbursement", "GLOBAL", "success_candidate", ("patient_uptake", "reimbursement_coverage"), ("cash_burn", "safety"), "Commercialization can improve only after reimbursement and uptake are visible."),
    Round35CaseCandidate("recursion_exscientia_ai_drug_platform_candidate", "AI_DRUG_DISCOVERY_PLATFORM", "RXRX_EXAI", "Recursion Exscientia AI drug platform candidate", "US", "success_candidate", ("big_pharma_partnership", "cash_runway"), ("platform_hype", "clinical_failure"), "Platform consolidation needs milestones and clinical progress."),
    Round35CaseCandidate("ai_drug_no_approved_product_counterexample", "AI_DRUG_DISCOVERY_PLATFORM", "AIDRUG_NOAPP", "AI drug no approved product counterexample", "GLOBAL", "failed_rerating", ("ai_drug_platform",), ("no_approved_drug", "platform_hype"), "AI platform alone is not commercialization evidence."),
    Round35CaseCandidate("ai_drug_cash_burn_counterexample", "AI_DRUG_DISCOVERY_PLATFORM", "AIDRUG_BURN", "AI drug cash burn counterexample", "GLOBAL", "failed_rerating", ("candidate_discovery",), ("cash_burn", "cash_runway_break"), "Cash burn can dominate platform narratives."),
    Round35CaseCandidate("ai_drug_big_pharma_milestone_candidate", "AI_DRUG_DISCOVERY_PLATFORM", "AIDRUG_MILE", "AI drug big pharma milestone candidate", "GLOBAL", "success_candidate", ("milestone_revenue", "clinical_entry"), ("data_quality", "clinical_failure"), "Milestone revenue is stronger than platform description."),
    Round35CaseCandidate("five9_contact_center_software_candidate", "CONTACT_CENTER_AI_AUTOMATION", "FIVN", "Five9 contact center software candidate", "US", "success_candidate", ("ccaas", "arr_growth", "enterprise_retention"), ("churn", "it_budget"), "Contact-center software needs recurring revenue and retention."),
    Round35CaseCandidate("minerva_cq_agent_assist_case_candidate", "CONTACT_CENTER_AI_AUTOMATION", "MINERVA_CQ", "Minerva CQ agent assist case candidate", "US", "success_candidate", ("agent_assist", "cost_saving_roi"), ("poc_only", "ai_error"), "Agent-assist is useful only when ROI translates to recurring software revenue."),
    Round35CaseCandidate("contact_center_ai_no_arr_counterexample", "CONTACT_CENTER_AI_AUTOMATION", "CCAI_NOARR", "Contact center AI no ARR counterexample", "GLOBAL", "failed_rerating", ("contact_center_ai",), ("poc_only", "seat_contraction"), "AI demo without ARR or seat expansion stays capped."),
    Round35CaseCandidate("ai_customer_service_privacy_error_4c", "CONTACT_CENTER_AI_AUTOMATION", "CCAI_PRIV_4C", "AI customer service privacy error 4C", "GLOBAL", "4c_thesis_break", ("ai_bot",), ("privacy_incident", "ai_error_liability"), "Privacy or AI-answer error can break enterprise adoption."),
    Round35CaseCandidate("computer_vision_self_checkout_candidate", "SERVICE_KIOSK_SELF_CHECKOUT", "CV_CHECKOUT", "Computer vision self-checkout candidate", "GLOBAL", "success_candidate", ("computer_vision_checkout", "loss_prevention_effect"), ("theft", "customer_friction"), "Self-checkout needs loss-prevention and customer experience proof."),
    Round35CaseCandidate("self_checkout_theft_counterexample", "SERVICE_KIOSK_SELF_CHECKOUT", "SELF_THEFT", "Self-checkout theft counterexample", "GLOBAL", "failed_rerating", ("self_checkout",), ("theft_loss_spike", "retailer_rollbacks"), "Theft can reverse self-checkout adoption."),
    Round35CaseCandidate("pseudo_automation_workload_counterexample", "SERVICE_KIOSK_SELF_CHECKOUT", "PSEUDO_AUTO", "Pseudo automation workload counterexample", "GLOBAL", "failed_rerating", ("retail_automation",), ("pseudo_automation", "customer_backlash"), "Automation that shifts labor to customers or staff should not score like productivity."),
    Round35CaseCandidate("kiosk_one_off_hardware_counterexample", "SERVICE_KIOSK_SELF_CHECKOUT", "KIOSK_HW", "Kiosk one-off hardware counterexample", "GLOBAL", "failed_rerating", ("kiosk_installation",), ("one_off_hardware", "maintenance_cost"), "One-time hardware sales lack recurring visibility."),
    Round35CaseCandidate("abbvie_rinvoq_skyrizi_successor_candidate", "BIOSIMILAR_ORIGINATOR_DEFENSE", "ABBV_SUCCESSOR", "AbbVie Rinvoq Skyrizi successor candidate", "US", "success_candidate", ("successor_drug", "successor_revenue_growth"), ("pricing_pressure", "pipeline_failure"), "Successor drug revenue can offset patent cliff erosion."),
    Round35CaseCandidate("humira_biosimilar_erosion_counterexample", "BIOSIMILAR_ORIGINATOR_DEFENSE", "HUMIRA_EROSION", "Humira biosimilar erosion counterexample", "US", "failed_rerating", ("patent_cliff",), ("biosimilar_erosion", "pricing_power_loss"), "Patent cliff can erode originator pricing power."),
    Round35CaseCandidate("patent_cliff_no_successor_4c", "BIOSIMILAR_ORIGINATOR_DEFENSE", "PATENT_NO_SUCC_4C", "Patent cliff no successor 4C", "GLOBAL", "4c_thesis_break", ("originator_defense",), ("successor_failure", "rapid_revenue_erosion"), "No successor drug turns patent cliff into thesis break."),
    Round35CaseCandidate("pipeline_transition_success_case", "BIOSIMILAR_ORIGINATOR_DEFENSE", "PIPE_TRANS", "Pipeline transition success case", "GLOBAL", "success_candidate", ("pipeline_transition", "eps_fcf_defense"), ("pipeline_setback", "pricing_pressure"), "Pipeline transition needs EPS/FCF defense, not just trial news."),
    Round35CaseCandidate("compounded_glp1_quality_risk_4c", "PHARMA_PLATFORM_REGULATORY_RISK", "CMPD_GLP1_4C", "Compounded GLP-1 quality risk 4C", "US", "4c_thesis_break", ("compounded_drug",), ("fda_warning", "quality_failure"), "Compounded drug quality risk can break channel narrative."),
    Round35CaseCandidate("online_pharmacy_illegal_risk_counterexample", "PHARMA_PLATFORM_REGULATORY_RISK", "ONLINE_PHARM", "Online pharmacy illegal risk counterexample", "GLOBAL", "failed_rerating", ("online_pharmacy",), ("illegal_distribution", "liability_claim"), "Illegal pharmacy exposure is not scalable recurring revenue."),
    Round35CaseCandidate("legal_telehealth_prescription_channel_candidate", "PHARMA_PLATFORM_REGULATORY_RISK", "TELEHEALTH_LEGAL", "Legal telehealth prescription channel candidate", "US", "success_candidate", ("telehealth_prescription", "legal_distribution_channel"), ("advertising_rule", "liability"), "Legal channel plus quality control can become a monitored commercialization path."),
    Round35CaseCandidate("pharma_advertising_regulation_4c", "PHARMA_PLATFORM_REGULATORY_RISK", "PHARMA_AD_4C", "Pharma advertising regulation 4C", "GLOBAL", "4c_thesis_break", ("pharma_marketing",), ("advertising_halt", "advertising_rule"), "Advertising or promotion restriction can break a channel-growth thesis."),
)


def target_for(target_id: str) -> Round35ScoreTarget | None:
    for target in ROUND35_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round35_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND35_CASE_CANDIDATES:
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
                f"Round35 v2.0 calibration candidate for {candidate.target_id}; "
                "stage dates, prices, and numeric evidence remain unfilled."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=tuple(field for field in candidate.evidence_fields if field in target.green_conditions),
            stage3_evidence=(),
            stage4b_evidence=candidate.red_flag_fields if candidate.case_type == "4b_watch" else (),
            stage4c_evidence=candidate.red_flag_fields if candidate.case_type == "4c_thesis_break" else (),
            must_have_fields=target.green_conditions,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason="; ".join(candidate.red_flag_fields) if candidate.case_type not in {"success_candidate", "structural_success", "cyclical_success"} else None,
            score_price_alignment="unknown",
            rerating_result="thesis_break" if candidate.case_type == "4c_thesis_break" else "unknown",
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
                "approval_or_market_size_alone_is_not_green",
                *target.red_flags,
            ),
            notes=candidate.notes,
            price_validation=PriceValidation(price_validation_status="needs_price_backfill"),
            data_quality=CaseDataQuality(False, False, False, 0.0),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round35_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND35_SCORE_TARGETS:
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


def round35_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND35_CASE_CANDIDATES:
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


def round35_summary() -> dict[str, int | bool]:
    records = round35_case_records()
    positive = sum(1 for record in records if record.case_type in {"success_candidate", "structural_success", "cyclical_success"})
    stage4c = sum(1 for record in records if record.case_type == "4c_thesis_break")
    stage4b = sum(1 for record in records if record.case_type == "4b_watch")
    return {
        "target_count": len(ROUND35_SCORE_TARGETS),
        "case_candidate_count": len(records),
        "success_candidate_count": positive,
        "counterexample_or_risk_count": len(records) - positive,
        "stage4b_case_count": stage4b,
        "stage4c_case_count": stage4c,
        "green_possible_count": sum(1 for target in ROUND35_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND35_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND35_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round35_score_weight_reports(
    *,
    output_directory: str | Path = ROUND35_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND35_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND35_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round35_score_weight_v20_summary.md",
        "case_matrix": output / "round35_case_candidate_matrix.csv",
        "green_guardrails": output / "round35_green_guardrail_review.md",
        "biotech_commercialization": output / "round35_biotech_commercialization_review.md",
        "glp1_regulatory": output / "round35_glp1_regulatory_review.md",
        "service_automation": output / "round35_service_automation_review.md",
        "price_validation_plan": output / "round35_price_validation_plan.md",
    }
    _write_case_jsonl(round35_case_records(), cases)
    _write_rows(round35_score_profile_rows(), score_profiles)
    _write_rows(round35_case_candidate_rows(), paths["case_matrix"])
    paths["summary"].write_text(render_round35_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round35_green_guardrail_markdown(), encoding="utf-8")
    paths["biotech_commercialization"].write_text(render_round35_biotech_commercialization_markdown(), encoding="utf-8")
    paths["glp1_regulatory"].write_text(render_round35_glp1_regulatory_markdown(), encoding="utf-8")
    paths["service_automation"].write_text(render_round35_service_automation_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round35_price_validation_plan_markdown(), encoding="utf-8")
    return paths


def render_round35_summary_markdown() -> str:
    summary = round35_summary()
    lines = [
        "# Round-35 Score-Weight v2.0 Summary",
        "",
        f"- source_round: `{ROUND35_SOURCE_ROUND_PATH}`",
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
        "- Round 35 adds v2.0 calibration cases and target weights only.",
        "- Example: biosimilar approval is not enough; payer access, prescription uptake, and margin defense are required.",
        "- Example: GLP-1 demand can support Green only when prescriptions, reimbursement, supply, and revisions are source-backed.",
        "- Example: AI drug discovery remains RedTeam-first until clinical milestones and commercialization evidence exist.",
        "- Approval news, market-size narratives, AI labels, PoCs, and user/install counts are not score evidence by themselves.",
    ]
    return "\n".join(lines) + "\n"


def render_round35_green_guardrail_markdown() -> str:
    lines = [
        "# Round-35 Green Guardrail Review",
        "",
        "| target | posture | Green unlock evidence | Red flags |",
        "|---|---|---|---|",
    ]
    for target in ROUND35_SCORE_TARGETS:
        lines.append(
            "| "
            f"{target.target_id} | {target.posture.value} | "
            f"{', '.join(target.green_conditions)} | {', '.join(target.red_flags)} |"
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "- Do not apply v2.0 weights to production scoring yet.",
            "- Do not use case IDs, drug names, platform labels, or automation headlines as candidate-generation input.",
            "- Do not invent stage dates, prices, prescription counts, payer access, reimbursement, ARR, seats, ROI, or unit economics.",
            "- Do not lower Stage 3-Green thresholds to improve healthcare or AI-service recall.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round35_biotech_commercialization_markdown() -> str:
    return "\n".join(
        [
            "# Round-35 Biotech Commercialization Review",
            "",
            "Round 35 separates approval headlines from actual commercialization.",
            "",
            "## Biosimilars",
            "- Approval and discount access are Stage 1 signals.",
            "- Higher stages need payer/PBM adoption, prescription conversion, manufacturing cost advantage, and margin defense.",
            "",
            "## Gene Therapy / Rare Disease",
            "- Approval is not commercialization.",
            "- Reimbursement, patient uptake, treatment-center readiness, manufacturing, and cash runway are gating evidence.",
        ]
    ) + "\n"


def render_round35_glp1_regulatory_markdown() -> str:
    return "\n".join(
        [
            "# Round-35 GLP-1 / Pharma Regulatory Review",
            "",
            "GLP-1 and pharma-platform narratives need commercial and regulatory proof.",
            "",
            "## GLP-1",
            "- Green-possible with prescription growth, reimbursement expansion, supply capacity, and OP/EPS revisions.",
            "- Competition, compounded alternatives, supply limits, and advertising rules are RedTeam gates.",
            "",
            "## Pharma Channels",
            "- Legal telehealth or pharmacy channels can be monitored.",
            "- Illegal pharmacy, FDA warning, compounding quality, or advertising shutdown can be 4C evidence.",
        ]
    ) + "\n"


def render_round35_service_automation_markdown() -> str:
    return "\n".join(
        [
            "# Round-35 Service Automation Review",
            "",
            "Service automation should be scored through recurring economics, not technology demos.",
            "",
            "## Contact Center AI",
            "- ARR, seat expansion, retention, cost-saving ROI, and FCF/OPM improvement can support Green-like interpretation.",
            "- PoCs, demos, privacy incidents, AI errors, or seat contraction keep it Watch/Red.",
            "",
            "## Kiosk / Self-Checkout",
            "- Installed base is weak unless maintenance, payment, software, or loss-prevention economics are visible.",
            "- Theft, customer friction, and pseudo-automation are strong counterexamples.",
        ]
    ) + "\n"


def render_round35_price_validation_plan_markdown() -> str:
    return "\n".join(
        [
            "# Round-35 Price Validation Plan",
            "",
            "1. Backfill tradable case price paths where symbols exist.",
            "2. Keep synthetic, private, global reference, regulatory, and clinical cases as `needs_price_backfill` or `missing_price_data`.",
            "3. Calculate MFE/MAE, peak, drawdown, and below-entry flags only from source data.",
            "4. Run shadow score-price alignment before any production scoring change.",
            "",
            "## Priority Validation",
            "- Biosimilars/originators: uptake and margin defense versus price erosion and patent cliff.",
            "- GLP-1/pharma channels: prescription growth and supply versus compounding, reimbursement, and regulation.",
            "- Gene therapy/AI drug: commercialization and milestones versus cash burn and clinical failure.",
            "- Contact-center AI/kiosks: ARR, ROI, maintenance, and software economics versus demos, theft, and customer friction.",
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
    "ROUND35_CASE_CANDIDATES",
    "ROUND35_DEFAULT_CASES_PATH",
    "ROUND35_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND35_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND35_SCORE_TARGETS",
    "ROUND35_SOURCE_ROUND_PATH",
    "Round35CaseCandidate",
    "Round35ScoreTarget",
    "Round35ScoreWeightDraft",
    "render_round35_biotech_commercialization_markdown",
    "render_round35_glp1_regulatory_markdown",
    "render_round35_green_guardrail_markdown",
    "render_round35_price_validation_plan_markdown",
    "render_round35_service_automation_markdown",
    "render_round35_summary_markdown",
    "round35_case_candidate_rows",
    "round35_case_records",
    "round35_score_profile_rows",
    "round35_summary",
    "target_for",
    "write_round35_score_weight_reports",
]
