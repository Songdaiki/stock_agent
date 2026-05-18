"""Round-178 R7 Loop-11 Korea biotech, healthcare, and medical-device pack.

Round 178 narrows the R7 healthcare taxonomy to Korea-focused royalty,
commercialization, biosimilar, botulinum, aesthetic-device, GLP-1 generic,
and medical-AI cases. It is calibration/report material only. Production
feature engineering, scoring, staging, and RedTeam code must not import it.
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


ROUND178_SOURCE_ROUND_PATH = "docs/round/round_178.md"
ROUND178_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round178_r7_loop11_biotech_healthcare_device"
ROUND178_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r7_loop11_round178.jsonl"
ROUND178_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round178_r7_loop11_v11.csv"
ROUND178_SOURCE_CANONICAL_TARGET_IDS: tuple[str, ...] = (
    "SC_FORMULATION_ROYALTY_PLATFORM",
    "BLOCKBUSTER_LIFE_EXTENSION_ROYALTY",
    "KOREA_ONCOLOGY_DRUG_COMMERCIALIZATION",
    "BIOSIMILAR_TARIFF_HEDGE_MANUFACTURING",
    "BIOSIMILAR_COMMERCIALIZATION_KOREA",
    "BOTULINUM_US_MARKET_ENTRY",
    "AESTHETIC_DEVICE_EXPORT_KOREA",
    "BIOTECH_LICENSE_MILESTONE_PLATFORM",
    "GLP1_GENERIC_THEME_KOREA",
    "MEDICAL_AI_REIMBURSEMENT_KOREA",
    "APPROVAL_ONLY_NOT_COMMERCIALIZATION",
    "MANUFACTURING_INSPECTION_CRL_OVERLAY",
    "PATENT_CHALLENGE_OVERLAY",
    "DISCLOSURE_CONFIDENCE_CAP",
)
ROUND178_HELPER_OVERLAY_TARGET_IDS: tuple[str, ...] = ("DEVICE_SAFETY_CHANNEL_OVERLAY",)
ROUND178_SOURCE_CANONICAL_TARGET_COUNT = len(ROUND178_SOURCE_CANONICAL_TARGET_IDS)
ROUND178_HELPER_OVERLAY_TARGET_COUNT = len(ROUND178_HELPER_OVERLAY_TARGET_IDS)


@dataclass(frozen=True)
class Round178ScoreWeightDraft:
    commercialization_eps_fcf_conversion: int | str
    prescription_royalty_reimbursement_repeat_revenue_visibility: int | str
    partner_approval_contract_visibility: int | str
    safety_regulatory_cmc_patent_disclosure_confidence: int | str
    early_price_path_validation: int | str
    cash_runway_capital_discipline: int | str
    valuation_room_4b_runway: int | str

    def as_dict(self) -> dict[str, int | str]:
        return {
            "commercialization_eps_fcf_conversion": self.commercialization_eps_fcf_conversion,
            "prescription_royalty_reimbursement_repeat_revenue_visibility": self.prescription_royalty_reimbursement_repeat_revenue_visibility,
            "partner_approval_contract_visibility": self.partner_approval_contract_visibility,
            "safety_regulatory_cmc_patent_disclosure_confidence": self.safety_regulatory_cmc_patent_disclosure_confidence,
            "early_price_path_validation": self.early_price_path_validation,
            "cash_runway_capital_discipline": self.cash_runway_capital_discipline,
            "valuation_room_4b_runway": self.valuation_room_4b_runway,
        }


@dataclass(frozen=True)
class Round178ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round178ScoreWeightDraft
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
        return Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round178CaseCandidate:
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
class Round178BaseScoreWeight:
    component: str
    points: int
    loop11_direction: str
    reason: str


@dataclass(frozen=True)
class Round178StageCap:
    stage_band: str
    max_score: str
    required_evidence: tuple[str, ...]
    example_cases: tuple[str, ...]
    green_policy: str


@dataclass(frozen=True)
class Round178ScoreStagePriceAlignment:
    case_id: str
    detected_stage: str
    price_path_status: str
    verdict: str
    normalization_adjustment: str


def _weights(
    commercialization: int | str,
    repeat_revenue: int | str,
    partner: int | str,
    safety: int | str,
    price: int | str,
    cash: int | str,
    valuation: int | str,
) -> Round178ScoreWeightDraft:
    return Round178ScoreWeightDraft(commercialization, repeat_revenue, partner, safety, price, cash, valuation)


def _target(
    target_id: str,
    archetype: E2RArchetype,
    posture: Round10ThemePosture,
    weight: Round178ScoreWeightDraft,
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
) -> Round178ScoreTarget:
    return Round178ScoreTarget(
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
        gate_only,
    )


GATE_WEIGHT = _weights("gate", "gate", "gate", "gate", "gate", "gate", "gate")
CAP_WEIGHT = _weights("cap", "cap", "cap", "+", "cap", "cap", "cap")


ROUND178_BASE_SCORE_WEIGHTS: tuple[Round178BaseScoreWeight, ...] = (
    Round178BaseScoreWeight(
        "commercialization_eps_fcf_conversion",
        24,
        "raise_actual_bodyweight",
        "Approval, license, clinical, or AI-performance headlines matter only after royalty, prescription, commercial sales, OPM, FCF, or EPS conversion appears.",
    ),
    Round178BaseScoreWeight(
        "prescription_royalty_reimbursement_repeat_revenue_visibility",
        22,
        "raise_repeat_economics",
        "Royalty recognition, scripts, reimbursement/PBM, procedure volume, consumables, and repeat sales decide Stage 2 to Stage 3 promotion.",
    ),
    Round178BaseScoreWeight(
        "partner_approval_contract_visibility",
        16,
        "stage2_enabler_not_green_alone",
        "FDA/EMA/MFDS approval, big-pharma partner, launch schedule, contract, milestone, and territory can lift Stage 2 but do not unlock Green by themselves.",
    ),
    Round178BaseScoreWeight(
        "safety_regulatory_cmc_patent_disclosure_confidence",
        14,
        "hard_redteam_gate",
        "CRL, manufacturing inspection, patent, reimbursement, safety, off-label, and missing disclosure detail can cap or break the thesis.",
    ),
    Round178BaseScoreWeight(
        "early_price_path_validation",
        10,
        "loop11_axis",
        "Stage 2 이후 60D MFE and Stage 2 이후 120D MFE help separate early Stage 3 from late approval-chasing.",
    ),
    Round178BaseScoreWeight(
        "cash_runway_capital_discipline",
        8,
        "biotech_funding_gate",
        "Cash runway, dilution, capex integration, and milestone timing decide whether commercialization can survive.",
    ),
    Round178BaseScoreWeight(
        "valuation_room_4b_runway",
        6,
        "cool_approval_overheat",
        "Biotech and medical-device narratives often reprice before adoption, royalty, or reimbursement; valuation room is deliberately small.",
    ),
)


ROUND178_STAGE_CAPS: tuple[Round178StageCap, ...] = (
    Round178StageCap(
        "Stage 1",
        "45",
        ("clinical_result", "fda_ema_mfds_approval_expectation", "license_expectation", "sc_formulation_story", "glp1_generic_theme", "medical_ai_auc_or_fda_clearance", "botulinum_us_news"),
        ("medical_ai_reimbursement_korea_gate_case", "samchundang_biosimilar_glp1_patent_watch_case"),
        "Science, approval expectation, license expectation, SC formulation, GLP-1 generic, medical AI, or botulinum news routes research only.",
    ),
    Round178StageCap(
        "Stage 2",
        "70",
        ("fda_ema_mfds_approval", "partner_launch_plan", "contract_or_milestone_or_royalty_structure", "prescription_launch_schedule", "production_facility", "selling_country"),
        ("alteogen_keytruda_sc_royalty_stage3_candidate", "yuhan_lazertinib_oncology_commercialization_case", "celltrion_us_factory_tariff_hedge_stage2_case"),
        "Stage 2 can be strong, but Green waits for actual royalty, scripts, reimbursement, repeat sales, OPM/FCF, and price-path evidence.",
    ),
    Round178StageCap(
        "Stage 3",
        "requires_5_of_8",
        ("approval_or_big_pharma_partner_confirmed", "royalty_milestone_contract_structure_confirmed", "commercial_launch_schedule_confirmed", "actual_prescription_adoption_procedure_volume_increase", "op_eps_revision_or_royalty_revenue_recognition", "stage2_60d_mfe_20pct", "no_patent_cmc_safety_hard_issue", "valuation_not_overheated"),
        ("alteogen_keytruda_sc_royalty_stage3_candidate", "hugel_letybo_us_market_entry_case", "classys_aesthetic_device_export_consumable_case"),
        "Stage 3 requires commercialization and cross-evidence. Approval, license, AI performance, or partner name alone cannot unlock Green.",
    ),
    Round178StageCap(
        "Stage 4B",
        "requires_3_of_5",
        ("stage2_120d_mfe_80pct", "approval_or_partner_name_alone_makes_stock_2x", "valuation_expands_before_royalty_or_adoption", "biotech_or_medical_ai_keywords_crowded", "op_eps_revision_cannot_follow_stock_price"),
        ("alteogen_keytruda_sc_royalty_stage3_candidate", "ablbio_lilly_license_milestone_platform_case"),
        "Approval or partner-name rerating is cooled when valuation moves before royalty, adoption, or OP/EPS confirmation.",
    ),
    Round178StageCap(
        "Stage 4C",
        "hard_gate",
        ("fda_crl", "manufacturing_inspection_issue", "patent_litigation_or_overhang", "commercial_launch_delay", "scripts_or_adoption_weak", "reimbursement_pbm_failure", "safety_warning_counterfeit_off_label_issue", "cash_runway_short_or_large_equity_raise", "medical_ai_reimbursement_absent_and_revenue_absent"),
        ("jj_rybrevant_sc_crl_inspection_overlay_case", "device_safety_channel_overlay_case"),
        "CRL, CMC, patent, reimbursement, safety, cash, or weak adoption issues block unsafe Green immediately.",
    ),
)


ROUND178_SCORE_TARGETS: tuple[Round178ScoreTarget, ...] = (
    _target(
        "SC_FORMULATION_ROYALTY_PLATFORM",
        E2RArchetype.SC_FORMULATION_ROYALTY_PLATFORM,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(24, 24, 18, 12, 10, 6, 6),
        stage1=("sc_formulation_platform", "alt_b4_enzyme", "blockbuster_patent_cliff"),
        stage2=("fda_approval", "big_pharma_partner", "adoption_target", "enzyme_use_confirmed"),
        stage3=("royalty_revenue", "enzyme_supply_revenue", "commercial_sales", "op_eps_revision", "actual_adoption"),
        stage4b=("stock_rerating_before_royalty", "approval_name_driven_rally", "valuation_expands_before_revenue"),
        stage4c=("patent_challenge", "launch_delay", "royalty_rate_dispute", "adoption_shortfall"),
        green=("royalty_revenue", "actual_adoption", "commercial_sales", "op_eps_revision", "stage2_60d_mfe_20pct"),
        red=("patent_challenge", "royalty_rate_missing", "adoption_missing", "approval_already_priced"),
        penalties=("patent", "royalty_missing", "adoption_missing", "valuation_4b"),
        note="Alteogen-style SC formulation can be Green-capable only after royalty/adoption/commercial evidence follows approval and partner confirmation.",
    ),
    _target(
        "BLOCKBUSTER_LIFE_EXTENSION_ROYALTY",
        E2RArchetype.BLOCKBUSTER_LIFE_EXTENSION_ROYALTY,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(24, 24, 18, 12, 10, 6, 6),
        stage1=("blockbuster_patent_cliff", "life_extension_formulation", "patient_convenience"),
        stage2=("partner_launch_plan", "adoption_target", "territory_confirmed", "royalty_structure"),
        stage3=("blockbuster_conversion_rate", "royalty_revenue_recognition", "eps_revision", "repeat_dosing_adoption"),
        stage4b=("blockbuster_story_overcrowded", "conversion_priced_before_royalty"),
        stage4c=("originator_strategy_changes", "patent_loss", "adoption_rate_low", "payer_resistance"),
        green=("royalty_revenue_recognition", "actual_adoption", "eps_revision", "commercial_launch"),
        red=("royalty_revenue_not_backfilled", "adoption_missing", "patent_overhang", "payer_resistance"),
        penalties=("adoption", "payer", "patent", "valuation_4b"),
        note="Blockbuster life-extension royalty needs actual conversion and royalty visibility, not only a patent-cliff story.",
    ),
    _target(
        "KOREA_ONCOLOGY_DRUG_COMMERCIALIZATION",
        E2RArchetype.KOREA_ONCOLOGY_DRUG_COMMERCIALIZATION,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(24, 23, 18, 12, 10, 7, 6),
        stage1=("oncology_trial_success", "partner_name", "first_line_expectation"),
        stage2=("fda_approval", "partner_launch_plan", "peak_sales_expectation", "commercial_launch"),
        stage3=("scripts", "royalty_revenue", "pbm_access", "market_share", "op_eps_revision"),
        stage4b=("peak_sales_story_priced_before_scripts", "partner_name_2x"),
        stage4c=("scripts_weak", "reimbursement_failure", "safety_warning", "competing_standard_of_care"),
        green=("scripts", "royalty_revenue", "pbm_access", "market_share", "op_eps_revision"),
        red=("scripts_missing", "pbm_access_missing", "royalty_missing", "competition"),
        penalties=("scripts", "pbm", "competition", "safety"),
        note="Yuhan-style oncology commercialization needs scripts and royalty, not only FDA approval or a global partner.",
    ),
    _target(
        "BIOSIMILAR_TARIFF_HEDGE_MANUFACTURING",
        E2RArchetype.BIOSIMILAR_TARIFF_HEDGE_MANUFACTURING,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(20, 18, 20, 14, 10, 8, 6),
        stage1=("us_factory_acquisition", "tariff_hedge_story", "biosimilar_launch_plan"),
        stage2=("facility_acquisition", "technology_transfer_plan", "us_manufacturing", "capex_plan"),
        stage3=("facility_utilization", "us_sales", "pbm_formulary", "opm_fcf_improvement"),
        stage4b=("factory_optional_value_priced_before_utilization",),
        stage4c=("facility_underutilization", "tech_transfer_delay", "tariff_policy_changes", "pbm_access_failure"),
        green=("facility_utilization", "us_sales", "pbm_formulary", "opm_fcf_improvement"),
        red=("utilization_missing", "pbm_formulary_missing", "tech_transfer_risk", "capex_integration_risk"),
        penalties=("utilization", "pbm", "tech_transfer", "capex"),
        note="Celltrion US manufacturing is Stage 2 until utilization, PBM/formulary, US sales, and OPM/FCF confirm.",
    ),
    _target(
        "BIOSIMILAR_COMMERCIALIZATION_KOREA",
        E2RArchetype.BIOSIMILAR_COMMERCIALIZATION_KOREA,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(23, 22, 17, 14, 10, 8, 6),
        stage1=("approval_expectation", "partner_agreement", "biosimilar_label"),
        stage2=("approval", "partner", "launch_schedule", "territory"),
        stage3=("prescription_volume", "pbm_formulary", "commercial_sales", "margin", "op_eps_revision"),
        stage4b=("approval_priced_before_switching",),
        stage4c=("patent_litigation", "launch_delay", "pbm_rebate_pressure", "margin_compression"),
        green=("prescription_volume", "pbm_formulary", "commercial_sales", "margin", "op_eps_revision"),
        red=("commercial_sales_missing", "pbm_missing", "patent_overhang", "margin_compression"),
        penalties=("patent", "launch", "pbm", "margin"),
        note="Biosimilar commercialization needs prescription, PBM/formulary, margin, and sales evidence after approval.",
    ),
    _target(
        "BOTULINUM_US_MARKET_ENTRY",
        E2RArchetype.BOTULINUM_US_MARKET_ENTRY,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(23, 22, 17, 14, 10, 8, 6),
        stage1=("us_launch_news", "fda_approval_expectation", "botulinum_aesthetic_theme"),
        stage2=("fda_approval", "us_launch", "licensed_channel", "selling_country_count"),
        stage3=("us_sales", "market_share", "repeat_aesthetic_procedure", "op_eps_revision", "safety_clean"),
        stage4b=("us_entry_story_priced_before_penetration",),
        stage4c=("safety_warning", "counterfeit_or_off_label", "licensed_channel_failure", "competition_discount"),
        green=("us_sales", "market_share", "repeat_aesthetic_procedure", "op_eps_revision", "licensed_channel"),
        red=("us_sales_missing", "market_share_missing", "safety_warning", "licensed_channel_safety_risk"),
        penalties=("safety", "channel", "competition", "penetration_missing"),
        note="Hugel-style botulinum US entry needs actual penetration and safe licensed channels before Green.",
    ),
    _target(
        "AESTHETIC_DEVICE_EXPORT_KOREA",
        E2RArchetype.AESTHETIC_DEVICE_EXPORT_KOREA,
        Round10ThemePosture.GREEN_POSSIBLE,
        _weights(24, 23, 16, 12, 10, 9, 6),
        stage1=("aesthetic_device_export", "global_channel", "installed_base_story"),
        stage2=("selling_country_count", "device_sales_growth", "installed_base", "regulatory_approval"),
        stage3=("consumable_revenue", "procedure_volume", "export_sales", "opm_fcf", "channel_repeat_order"),
        stage4b=("device_multiple_expands_before_consumables",),
        stage4c=("safety_issue", "channel_inventory", "bain_overhang", "consumable_attach_rate_weak"),
        green=("consumable_revenue", "procedure_volume", "export_sales", "opm_fcf", "channel_repeat_order"),
        red=("consumable_data_missing", "safety_issue", "channel_inventory", "valuation_overheat"),
        penalties=("consumable_missing", "safety", "inventory", "valuation"),
        note="Classys-style aesthetic devices are Green-capable only when export, procedure, consumable, OPM, and FCF repeat.",
    ),
    _target(
        "BIOTECH_LICENSE_MILESTONE_PLATFORM",
        E2RArchetype.BIOTECH_LICENSE_MILESTONE_PLATFORM,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(18, 18, 22, 14, 10, 10, 8),
        stage1=("license_expectation", "platform_biology", "big_pharma_interest"),
        stage2=("big_pharma_partner", "upfront_or_milestone", "research_deal", "clinical_transition"),
        stage3=("milestone_receipt", "royalty_visibility", "clinical_progress", "cash_runway_extended"),
        stage4b=("partner_name_rerating_before_milestone",),
        stage4c=("trial_failure", "milestone_delay", "cash_runway_short", "dilution"),
        green=("milestone_receipt", "royalty_visibility", "clinical_progress", "cash_runway_extended"),
        red=("milestone_detail_needed", "clinical_progress_missing", "royalty_not_visible", "cash_runway_short"),
        penalties=("milestone_missing", "clinical", "cash", "dilution"),
        note="ABL Bio-style license platforms are capped before milestone, clinical progress, royalty, and cash runway visibility.",
    ),
    _target(
        "GLP1_GENERIC_THEME_KOREA",
        E2RArchetype.GLP1_GENERIC_THEME_KOREA,
        Round10ThemePosture.REDTEAM_FIRST,
        _weights(12, 12, 14, 24, 10, 14, 8),
        stage1=("glp1_generic_theme", "oral_semaglutide_story", "bioequivalence"),
        stage2=("partner_agreement", "approval", "territory", "launch_claim"),
        stage3=("commercial_sales", "prescription_volume", "patent_clearance", "margin"),
        stage4b=("glp1_theme_crowded", "launch_claim_priced_before_patent_clearance"),
        stage4c=("patent_overhang", "regulatory_delay", "commercial_sales_missing", "margin_compression"),
        green=("commercial_sales", "prescription_volume", "patent_clearance", "margin"),
        red=("patent_overhang", "launch_claim_overstated_risk", "commercial_sales_missing", "hype_communication_risk"),
        penalties=("patent", "regulatory", "commercial_sales_missing", "theme_crowding"),
        note="GLP-1 generic is Stage 1/2 until patent/regulatory clearance and commercial sales confirm.",
        gate_only=True,
    ),
    _target(
        "MEDICAL_AI_REIMBURSEMENT_KOREA",
        E2RArchetype.MEDICAL_AI_REIMBURSEMENT_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _weights(14, 20, 14, 18, 10, 12, 6),
        stage1=("medical_ai_keyword", "fda_clearance", "auc_external_validation", "hospital_pilot"),
        stage2=("hospital_adoption", "reimbursement_code", "paid_deployment", "workflow_integration"),
        stage3=("reimbursement_revenue", "recurring_saas_revenue", "repeat_hospital_usage", "op_eps_revision"),
        stage4b=("medical_ai_theme_crowded", "auc_paper_priced_before_revenue"),
        stage4c=("reimbursement_absent", "revenue_absent", "subgroup_performance_issue", "liability_or_privacy_issue", "cash_burn"),
        green=("reimbursement_revenue", "recurring_saas_revenue", "repeat_hospital_usage", "op_eps_revision"),
        red=("reimbursement_missing", "paid_deployment_missing", "revenue_missing", "cash_burn"),
        penalties=("reimbursement", "paid_deployment", "revenue", "cash_burn"),
        note="Lunit/JLK/Deepnoid-style medical AI needs paid deployment, reimbursement, and recurring revenue after validation.",
    ),
    _target(
        "APPROVAL_ONLY_NOT_COMMERCIALIZATION",
        E2RArchetype.APPROVAL_ONLY_NOT_COMMERCIALIZATION,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("approval_headline", "fda_clearance", "license_headline", "ai_performance_headline"),
        stage2=("approval_or_partner_confirmed", "commercialization_plan_required"),
        stage3=("not_green_without_commercialization",),
        stage4b=("approval_headline_overheated",),
        stage4c=("commercialization_failure", "launch_delay", "adoption_missing"),
        green=(),
        red=("approval_without_sales", "partner_without_royalty", "ai_without_reimbursement", "adoption_missing"),
        penalties=("approval_only", "adoption", "commercialization", "disclosure"),
        note="Approval, license, and AI performance are not Stage 3 evidence before commercialization.",
        gate_only=True,
    ),
    _target(
        "MANUFACTURING_INSPECTION_CRL_OVERLAY",
        E2RArchetype.MANUFACTURING_INSPECTION_CRL_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("cmc_watch", "fda_review_pending"),
        stage2=("inspection_required", "manufacturing_site_required"),
        stage3=("not_green_if_inspection_issue",),
        stage4b=("approval_expectation_before_inspection_clearance",),
        stage4c=("fda_crl", "manufacturing_inspection_observation", "approval_delay", "launch_delay"),
        green=(),
        red=("fda_crl", "manufacturing_inspection_issue", "approval_delay", "launch_delay"),
        penalties=("cmc", "inspection", "approval_delay"),
        note="CMC and CRL issues are hard 4C gates for drug and formulation platforms.",
        gate_only=True,
    ),
    _target(
        "PATENT_CHALLENGE_OVERLAY",
        E2RArchetype.PATENT_CHALLENGE_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("patent_expiry_story", "secondary_patent_watch"),
        stage2=("patent_status_required", "settlement_or_clearance_required"),
        stage3=("not_green_if_patent_overhang",),
        stage4b=("patent_expiry_theme_crowded",),
        stage4c=("patent_litigation", "injunction", "launch_blocked", "royalty_window_shortened"),
        green=(),
        red=("patent_litigation", "secondary_patent_risk", "launch_blocked", "patent_overhang"),
        penalties=("patent", "launch", "royalty_window"),
        note="SC formulation and GLP-1 generic stories must be capped when patent status is unresolved.",
        gate_only=True,
    ),
    _target(
        "DISCLOSURE_CONFIDENCE_CAP",
        E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        Round10ThemePosture.REDTEAM_FIRST,
        CAP_WEIGHT,
        stage1=("opendart_list_only", "approval_headline", "license_headline", "ai_performance_headline"),
        stage2=("detail_fetch_required", "contract_terms_required", "royalty_rate_required", "prescription_or_reimbursement_required"),
        stage3=("multi_source_confirmation", "royalty_or_prescription_or_reimbursement_verified"),
        stage4b=("headline_driven_rally",),
        stage4c=("royalty_rate_missing", "contract_amount_missing", "prescription_missing", "reimbursement_missing"),
        green=("contract_amount", "royalty_rate", "prescription_volume", "reimbursement_status", "commercial_sales"),
        red=("detail_missing", "royalty_rate_missing", "contract_amount_missing", "prescription_missing", "reimbursement_missing"),
        penalties=("disclosure_detail", "royalty", "contract_amount", "prescription", "reimbursement"),
        note="Biotech disclosure confidence is capped when royalty, contract amount, prescription, or reimbursement fields are missing.",
    ),
    _target(
        "DEVICE_SAFETY_CHANNEL_OVERLAY",
        E2RArchetype.DEVICE_SAFETY_CHANNEL_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        stage1=("device_or_botulinum_launch", "aesthetic_channel"),
        stage2=("licensed_provider_channel", "safety_monitoring", "regulatory_approval"),
        stage3=("not_green_if_safety_channel_break",),
        stage4b=("device_theme_overheated",),
        stage4c=("safety_warning", "counterfeit_or_off_label", "licensed_provider_channel_missing", "adverse_events"),
        green=(),
        red=("safety_warning", "counterfeit_or_off_label", "licensed_provider_channel_missing", "adverse_events"),
        penalties=("safety", "channel", "counterfeit", "off_label"),
        note="Aesthetic device and botulinum candidates need safe licensed channels; safety breaks are hard caps.",
        gate_only=True,
    ),
)


ROUND178_SCORE_STAGE_PRICE_ALIGNMENT: tuple[Round178ScoreStagePriceAlignment, ...] = (
    Round178ScoreStagePriceAlignment(
        "alteogen_keytruda_sc_royalty_stage3_candidate",
        "Stage 2 to Stage 3 candidate plus 4B watch",
        "approval and partner evidence can precede royalty revenue, but stock may already have rerated",
        "royalty_platform_requires_adoption_revenue_and_4b_cooling",
        "give Stage 2/3 credit only after royalty/adoption; flag 4B when valuation moves first",
    ),
    Round178ScoreStagePriceAlignment(
        "yuhan_lazertinib_oncology_commercialization_case",
        "Stage 2 to Stage 3 candidate",
        "FDA approval and J&J partnership need scripts, PBM, and royalty follow-through",
        "oncology_commercialization_requires_scripts",
        "score FDA/partner in Stage 2; require scripts/royalty for Green",
    ),
    Round178ScoreStagePriceAlignment(
        "samchundang_biosimilar_glp1_patent_watch_case",
        "Stage 2 / 4B watch",
        "approval and partner claims can move price before patent and commercial sales",
        "glp1_generic_patent_and_sales_gate",
        "cap Green until patent/regulatory clearance and sales evidence exist",
    ),
    Round178ScoreStagePriceAlignment(
        "medical_ai_reimbursement_korea_gate_case",
        "Stage 1 to Stage 2 only",
        "AI clearance or validation is not paid deployment",
        "medical_ai_reimbursement_required",
        "cap before reimbursement, hospital paid usage, and recurring SaaS revenue",
    ),
    Round178ScoreStagePriceAlignment(
        "jj_rybrevant_sc_crl_inspection_overlay_case",
        "4C thesis-break overlay",
        "SC formulation data is offset by manufacturing inspection CRL",
        "cmc_crl_blocks_unsafe_green",
        "hard-cap any approval expectation until inspection issue clears",
    ),
)


def _d(value: str) -> date:
    return date.fromisoformat(value)


ROUND178_CASE_CANDIDATES: tuple[Round178CaseCandidate, ...] = (
    Round178CaseCandidate(
        "alteogen_keytruda_sc_royalty_stage3_candidate",
        "SC_FORMULATION_ROYALTY_PLATFORM",
        "196170",
        "Alteogen Keytruda Qlex SC royalty platform",
        "KR",
        "4b_watch",
        None,
        _d("2025-09-19"),
        None,
        _d("2025-09-19"),
        None,
        ("keytruda_qlex_fda_approval", "merck_partner", "alteogen_enzyme_used", "30_40pct_adoption_target", "keytruda_30bn_usd_sales_reference"),
        ("royalty_revenue_not_backfilled", "actual_adoption_missing", "patent_challenge_risk", "stage4b_rerating_risk"),
        "stage2_3_candidate_with_4b_watch",
        "needs_krx_price_royalty_adoption_backfill",
        ("round_178.md Alteogen Keytruda Qlex case",),
        "Alteogen is a Korea R7 Loop-11 core case: strong Stage 2 evidence, but royalty/adoption and 4B cooling remain separate.",
        (E2RArchetype.BLOCKBUSTER_LIFE_EXTENSION_ROYALTY, E2RArchetype.PATENT_CHALLENGE_OVERLAY),
    ),
    Round178CaseCandidate(
        "yuhan_lazertinib_oncology_commercialization_case",
        "KOREA_ONCOLOGY_DRUG_COMMERCIALIZATION",
        "000100",
        "Yuhan Lazertinib oncology commercialization",
        "KR",
        "success_candidate",
        None,
        _d("2024-08-20"),
        None,
        None,
        None,
        ("fda_approval", "johnson_and_johnson_partner", "rybrevant_lazcluze_first_line_regimen", "egfr_nsclc", "peak_sales_5bn_usd_expectation"),
        ("scripts_missing", "royalty_revenue_not_backfilled", "pbm_access_missing", "tagrisso_competition"),
        "stage2_commercialization_candidate",
        "needs_scripts_royalty_price_backfill",
        ("round_178.md Yuhan Lazertinib case",),
        "Yuhan moves beyond approval only when scripts, royalty revenue, PBM/access, and market share are visible.",
    ),
    Round178CaseCandidate(
        "celltrion_us_factory_tariff_hedge_stage2_case",
        "BIOSIMILAR_TARIFF_HEDGE_MANUFACTURING",
        "068270",
        "Celltrion US factory tariff hedge manufacturing",
        "KR",
        "success_candidate",
        None,
        _d("2025-09-23"),
        None,
        None,
        None,
        ("imclone_facility_330m_usd", "eli_lilly_facility", "us_manufacturing_tariff_hedge", "700bn_krw_expansion_plan"),
        ("utilization_missing", "pbm_formulary_missing", "tech_transfer_risk", "capex_integration_risk"),
        "stage2_factory_option_with_utilization_gate",
        "needs_utilization_us_sales_pbm_price_backfill",
        ("round_178.md Celltrion US factory case",),
        "Celltrion factory acquisition is Stage 2 unless utilization, US sales, PBM/formulary, and OPM/FCF follow.",
    ),
    Round178CaseCandidate(
        "hugel_letybo_us_market_entry_case",
        "BOTULINUM_US_MARKET_ENTRY",
        "145020",
        "Hugel Letybo US botulinum market entry",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("letybo_fda_approval", "us_launch", "65_countries", "31m_treatments_reference", "repeat_aesthetic_procedure"),
        ("us_sales_missing", "market_share_missing", "licensed_channel_safety_risk", "botox_competition"),
        "stage2_3_candidate_with_us_penetration_gate",
        "needs_us_sales_market_share_price_backfill",
        ("round_178.md Hugel Letybo case",),
        "Hugel needs US penetration, repeat procedure, licensed channel, and safety evidence before Green.",
    ),
    Round178CaseCandidate(
        "classys_aesthetic_device_export_consumable_case",
        "AESTHETIC_DEVICE_EXPORT_KOREA",
        "214150",
        "Classys aesthetic device export and consumables",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("non_invasive_aesthetic_device", "60_plus_countries_export", "installed_base_option", "consumable_cartridge_revenue_needed"),
        ("consumable_data_missing", "opm_fcf_backfill_needed", "valuation_overheat", "bain_overhang"),
        "stage2_3_candidate_with_consumable_gate",
        "needs_consumable_export_opm_price_backfill",
        ("round_178.md Classys aesthetic-device case",),
        "Classys can be Green-capable only if export growth connects to repeat procedure, consumable revenue, OPM, and FCF.",
    ),
    Round178CaseCandidate(
        "ablbio_lilly_license_milestone_platform_case",
        "BIOTECH_LICENSE_MILESTONE_PLATFORM",
        "298380",
        "ABL Bio Lilly license milestone platform",
        "KR",
        "success_candidate",
        None,
        None,
        None,
        None,
        None,
        ("eli_lilly_licensing_research_deal", "big_pharma_partner", "bispecific_bbb_shuttle_platform", "founder_billionaire_stock_rerating"),
        ("milestone_detail_needed", "clinical_progress_missing", "royalty_not_visible", "4b_deal_headline_risk"),
        "stage2_license_platform_with_milestone_gate",
        "needs_milestone_clinical_cash_price_backfill",
        ("round_178.md ABL Bio license platform case",),
        "ABL Bio is Stage 2 until milestone receipt, clinical progress, royalty visibility, and cash runway are visible.",
    ),
    Round178CaseCandidate(
        "samchundang_biosimilar_glp1_patent_watch_case",
        "BIOSIMILAR_COMMERCIALIZATION_KOREA",
        "000250",
        "Sam Chun Dang biosimilar and GLP-1 generic patent watch",
        "KR",
        "4b_watch",
        None,
        None,
        None,
        None,
        None,
        ("scd411_multicountry_approval", "daiichi_sankyo_espha_japan_partner", "oral_semaglutide_generic", "ophthalmic_base_revenue"),
        ("glp1_patent_overhang", "launch_claim_overstated_risk", "commercial_sales_missing", "hype_communication_risk"),
        "stage2_with_glp1_patent_4b_watch",
        "needs_patent_clearance_sales_price_backfill",
        ("round_178.md Sam Chun Dang biosimilar and GLP-1 generic case",),
        "Sam Chun Dang is a Stage 2/4B-watch case until patent clearance, launch, prescription, and sales confirm.",
        (E2RArchetype.GLP1_GENERIC_THEME_KOREA, E2RArchetype.PATENT_CHALLENGE_OVERLAY),
    ),
    Round178CaseCandidate(
        "jj_rybrevant_sc_crl_inspection_overlay_case",
        "MANUFACTURING_INSPECTION_CRL_OVERLAY",
        "JNJ_REFERENCE",
        "J&J Rybrevant SC CRL manufacturing-inspection overlay",
        "US",
        "4c_thesis_break",
        None,
        None,
        None,
        None,
        _d("2024-12-16"),
        ("sc_formulation_clinical_data", "no_extra_clinical_trial_requested"),
        ("manufacturing_inspection_observation", "fda_crl", "approval_delay", "launch_delay"),
        "cmc_crl_thesis_break_reference",
        "needs_reference_price_backfill",
        ("round_178.md J&J Rybrevant SC CRL overlay",),
        "A clean clinical package can still be capped by manufacturing inspection and CRL issues.",
    ),
    Round178CaseCandidate(
        "merck_keytruda_qlex_approval_price_failed_case",
        "APPROVAL_ONLY_NOT_COMMERCIALIZATION",
        "MRK_REFERENCE",
        "Merck Keytruda Qlex approval without direct price rerating reference",
        "US",
        "failed_rerating",
        None,
        _d("2025-09-19"),
        None,
        None,
        None,
        ("keytruda_qlex_fda_approval",),
        ("approval_already_priced", "adoption_needed", "royalty_eps_missing"),
        "approval_without_eps_price_confirmation",
        "needs_reference_price_backfill",
        ("round_178.md Merck Keytruda Qlex approval-only reference",),
        "Approval can be a Stage 2 event without proving stock-level rerating or EPS bodyweight for every linked company.",
    ),
    Round178CaseCandidate(
        "medical_ai_reimbursement_korea_gate_case",
        "MEDICAL_AI_REIMBURSEMENT_KOREA",
        "328130/322510/315640",
        "Lunit / JLK / Deepnoid medical AI reimbursement gate",
        "KR",
        "event_premium",
        None,
        None,
        None,
        None,
        None,
        ("fda_clearance", "auc_external_validation", "hospital_pilot", "medical_ai_keyword"),
        ("reimbursement_missing", "paid_deployment_missing", "revenue_missing", "cash_burn"),
        "medical_ai_validation_not_commercialization",
        "needs_reimbursement_revenue_price_backfill",
        ("round_178.md medical AI reimbursement gate",),
        "Medical AI validation is useful, but paid deployment, reimbursement, and recurring revenue gate Stage 3.",
    ),
    Round178CaseCandidate(
        "device_safety_channel_overlay_case",
        "DEVICE_SAFETY_CHANNEL_OVERLAY",
        "K_AESTHETIC_BASKET",
        "K aesthetic device and botulinum safety-channel overlay",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("repeat_procedure", "fda_approval_or_mfds", "aesthetic_channel"),
        ("safety_warning", "counterfeit_or_off_label", "licensed_provider_channel_missing", "adverse_events"),
        "safety_channel_hard_cap",
        "needs_safety_channel_price_backfill",
        ("round_178.md device safety channel overlay",),
        "Aesthetic devices and botulinum names are capped if channel or safety quality is not verified.",
    ),
    Round178CaseCandidate(
        "biotech_disclosure_confidence_cap_case",
        "DISCLOSURE_CONFIDENCE_CAP",
        "KR_BIOTECH_DISCLOSURE_BASKET",
        "Korea biotech disclosure confidence cap basket",
        "KR",
        "failed_rerating",
        None,
        None,
        None,
        None,
        None,
        ("opendart_list_only", "license_headline", "approval_headline", "ai_performance_headline"),
        ("royalty_rate_missing", "contract_amount_missing", "prescription_missing", "reimbursement_missing"),
        "disclosure_detail_missing_cap",
        "needs_detail_disclosure_backfill",
        ("round_178.md biotech disclosure confidence cap",),
        "OpenDART list, license, approval, or AI performance headlines stay capped when detailed economics are missing.",
    ),
)


ROUND178_PRICE_FIELDS: tuple[str, ...] = (
    "approval_status",
    "approval_date",
    "partner_name",
    "contract_amount",
    "upfront_amount",
    "milestone_amount",
    "royalty_rate_if_disclosed",
    "territory",
    "launch_date",
    "commercial_sales",
    "prescription_volume",
    "procedure_volume",
    "reimbursement_status",
    "pbm_or_formulary_status",
    "medical_fee_code_status",
    "royalty_revenue",
    "enzyme_supply_revenue",
    "op_revision_1m",
    "eps_revision_1m",
    "cash_runway_months",
    "dilution_event_flag",
    "stage2_price",
    "stage3_price",
    "stage4b_price",
    "stage4c_price",
    "return_60d_after_stage2",
    "return_120d_after_stage2",
    "mfe_60d_after_stage2",
    "mfe_120d_after_stage2",
    "mae_60d_after_stage2",
    "valuation_at_stage3",
    "valuation_at_stage4b",
    "crl_flag",
    "manufacturing_inspection_issue_flag",
    "patent_litigation_flag",
    "safety_warning_flag",
    "reimbursement_failure_flag",
    "disclosure_confidence",
)


def round178_target_for(target_id: str) -> Round178ScoreTarget | None:
    for target in ROUND178_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round178_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND178_CASE_CANDIDATES:
        target = round178_target_for(candidate.target_id)
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
                f"Round178 R7 Loop-11 case for {candidate.target_id}; "
                "Korea healthcare approval, license, AI, and device narratives are separated from royalty, scripts, reimbursement, repeat revenue, OPM, FCF, and 4B/4C gates."
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
                "approval_license_ai_performance_is_not_commercialization",
                "require_royalty_scripts_reimbursement_repeat_revenue_commercial_sales_opm_fcf_for_green",
                "stage3_early_catch_requires_5_of_8_loop11_conditions",
                "do_not_invent_contract_amount_upfront_milestone_royalty_rate_scripts_reimbursement_commercial_sales_stage_prices_or_mfe_mae",
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


def round178_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND178_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "commercialization_eps_fcf_conversion": str(weights["commercialization_eps_fcf_conversion"]),
                "prescription_royalty_reimbursement_repeat_revenue_visibility": str(weights["prescription_royalty_reimbursement_repeat_revenue_visibility"]),
                "partner_approval_contract_visibility": str(weights["partner_approval_contract_visibility"]),
                "safety_regulatory_cmc_patent_disclosure_confidence": str(weights["safety_regulatory_cmc_patent_disclosure_confidence"]),
                "early_price_path_validation": str(weights["early_price_path_validation"]),
                "cash_runway_capital_discipline": str(weights["cash_runway_capital_discipline"]),
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


def round178_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND178_CASE_CANDIDATES:
        target = round178_target_for(candidate.target_id)
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


def round178_stage_date_rows() -> tuple[dict[str, str], ...]:
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
        for target in ROUND178_SCORE_TARGETS
    )


def round178_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round178_backfill": "true"} for field in ROUND178_PRICE_FIELDS)


def round178_base_score_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "component": item.component,
            "points": str(item.points),
            "loop11_direction": item.loop11_direction,
            "reason": item.reason,
            "production_scoring_changed": "false",
        }
        for item in ROUND178_BASE_SCORE_WEIGHTS
    )


def round178_stage_cap_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "stage_band": item.stage_band,
            "max_score": item.max_score,
            "required_evidence": "|".join(item.required_evidence),
            "example_cases": "|".join(item.example_cases),
            "green_policy": item.green_policy,
            "production_scoring_changed": "false",
        }
        for item in ROUND178_STAGE_CAPS
    )


def round178_score_stage_price_alignment_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "case_id": item.case_id,
            "detected_stage": item.detected_stage,
            "price_path_status": item.price_path_status,
            "verdict": item.verdict,
            "normalization_adjustment": item.normalization_adjustment,
            "production_scoring_changed": "false",
        }
        for item in ROUND178_SCORE_STAGE_PRICE_ALIGNMENT
    )


def round178_summary() -> dict[str, int | bool]:
    records = round178_case_records()
    return {
        "target_count": len(ROUND178_SCORE_TARGETS),
        "source_canonical_target_count": ROUND178_SOURCE_CANONICAL_TARGET_COUNT,
        "helper_overlay_target_count": ROUND178_HELPER_OVERLAY_TARGET_COUNT,
        "case_candidate_count": len(records),
        "base_score_component_count": len(ROUND178_BASE_SCORE_WEIGHTS),
        "stage_cap_count": len(ROUND178_STAGE_CAPS),
        "score_stage_price_alignment_count": len(ROUND178_SCORE_STAGE_PRICE_ALIGNMENT),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND178_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND178_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND178_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "gate_only_target_count": sum(1 for target in ROUND178_SCORE_TARGETS if target.gate_only),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round178_r7_loop11_reports(
    *,
    output_directory: str | Path = ROUND178_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND178_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND178_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round178_r7_loop11_biotech_healthcare_device_summary.md",
        "case_matrix": output / "round178_r7_loop11_case_matrix.csv",
        "stage_date_plan": output / "round178_r7_loop11_stage_date_plan.csv",
        "green_guardrails": output / "round178_r7_loop11_green_guardrails.md",
        "risk_overlays": output / "round178_r7_loop11_risk_overlays.md",
        "price_validation_plan": output / "round178_r7_loop11_price_validation_plan.md",
        "price_fields": output / "round178_r7_loop11_price_fields.csv",
        "base_score_weights": output / "round178_r7_loop11_base_score_weights.csv",
        "stage_caps": output / "round178_r7_loop11_stage_caps.csv",
        "score_stage_price_alignment": output / "round178_r7_loop11_score_stage_price_alignment.csv",
        "score_stage_price_alignment_md": output / "round178_r7_loop11_score_stage_price_alignment.md",
    }
    _write_case_jsonl(round178_case_records(), cases)
    _write_rows(round178_score_profile_rows(), score_profiles)
    _write_rows(round178_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round178_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round178_price_field_rows(), paths["price_fields"])
    _write_rows(round178_base_score_weight_rows(), paths["base_score_weights"])
    _write_rows(round178_stage_cap_rows(), paths["stage_caps"])
    _write_rows(round178_score_stage_price_alignment_rows(), paths["score_stage_price_alignment"])
    paths["summary"].write_text(render_round178_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round178_green_guardrail_markdown(), encoding="utf-8")
    paths["risk_overlays"].write_text(render_round178_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round178_price_validation_plan_markdown(), encoding="utf-8")
    paths["score_stage_price_alignment_md"].write_text(render_round178_score_stage_price_alignment_markdown(), encoding="utf-8")
    return paths


def render_round178_summary_markdown() -> str:
    summary = round178_summary()
    lines = [
        "# Round-178 R7 Loop-11 Korea Biotech / Healthcare / Medical Device Summary",
        "",
        f"- source_round: `{ROUND178_SOURCE_ROUND_PATH}`",
        "- large_sector: `BIOTECH_HEALTHCARE_DEVICE`",
        "- loop: `R7 Loop 11 / v11.0`",
        f"- target_count: {summary['target_count']}",
        f"- source_canonical_target_count: {summary['source_canonical_target_count']}",
        f"- helper_overlay_target_count: {summary['helper_overlay_target_count']}",
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
        "- R7 Loop 11 separates approval/license/AI performance from commercialization.",
        "- Example: `FDA approval` can be Stage 2, but scripts, royalty, reimbursement, repeat sales, OPM, and FCF decide Stage 3 review.",
        "- Example: Alteogen Keytruda Qlex can be Stage 2/3 candidate and 4B-watch at the same time when approval and partner evidence are strong but royalty/adoption are not yet backfilled.",
        "- Example: medical AI AUC or clearance is capped before paid deployment and reimbursement.",
    ]
    return "\n".join(lines) + "\n"


def render_round178_green_guardrail_markdown() -> str:
    lines = [
        "# Round-178 R7 Loop-11 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Loop-11 penalties |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND178_SCORE_TARGETS:
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
            "- Do not apply R7 Loop-11 v11.0 weights to production scoring yet.",
            "- Do not treat approval/license/AI performance, clinical result, partner name, FDA clearance, or SC formulation story as Green evidence by itself.",
            "- Do not invent contract amount, upfront, milestone, royalty rate, prescription volume, reimbursement status, commercial sales, procedure volume, OPM/FCF, stage prices, or MFE/MAE.",
            "- Green requires royalty, scripts, reimbursement, repeat sales, procedure/consumable revenue, commercial sales, OP/EPS revision, or FCF conversion with low RedTeam risk.",
            "- CRL, CMC/manufacturing inspection, patent challenge, reimbursement failure, safety issue, counterfeiting/off-label channel, cash runway, and dilution remain RedTeam gates.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round178_risk_overlay_markdown() -> str:
    lines = [
        "# Round-178 R7 Loop-11 Risk Overlays",
        "",
        "- `APPROVAL_ONLY_NOT_COMMERCIALIZATION`: approval, license, or AI performance remains Stage 1/2 before commercialization.",
        "- `ROYALTY_ADOPTION_GATE`: royalty platforms need actual adoption and revenue recognition.",
        "- `ONCOLOGY_SCRIPTS_GATE`: oncology drug approval needs scripts, PBM/access, market share, and royalty follow-through.",
        "- `BIOSIMILAR_PBM_MARGIN_GATE`: biosimilars need prescription switching, PBM/formulary, commercial sales, and margin evidence.",
        "- `BOTULINUM_US_PENETRATION_GATE`: FDA approval and launch need actual US sales, repeat procedures, and safe licensed channels.",
        "- `AESTHETIC_CONSUMABLE_GATE`: export devices need installed base, consumables, repeat procedure, OPM, and FCF.",
        "- `LICENSE_MILESTONE_CAP`: big-pharma partner names are capped before milestone receipt, clinical progress, and cash-runway visibility.",
        "- `GLP1_PATENT_THEME_CAP`: GLP-1 generic stories are capped before patent/regulatory clearance and commercial sales.",
        "- `MEDICAL_AI_REIMBURSEMENT_GATE`: AUC, FDA clearance, or pilots are capped before paid deployment, reimbursement, and recurring revenue.",
        "- `MANUFACTURING_INSPECTION_CRL_OVERLAY`: CRL and inspection observations are hard 4C gates.",
        "- `DISCLOSURE_CONFIDENCE_CAP`: royalty, contract amount, prescription, reimbursement, and commercial-sales fields must be detailed.",
        "",
        "Simple example: `partner=Merck` is strong Stage 2 evidence. It is not Green if royalty revenue and adoption are still missing.",
    ]
    return "\n".join(lines) + "\n"


def render_round178_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-178 R7 Loop-11 Price Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign stage dates only from source evidence.",
        "2. Store stage-date close prices from official price data.",
        "3. Calculate 60D/120D returns after Stage 2, plus MFE/MAE where price data exists.",
        "4. Compare approval/partner/license evidence with royalty, scripts, reimbursement, procedure volume, commercial sales, OPM, FCF, safety, CMC, and patent events.",
        "5. Keep missing stage prices and MFE/MAE null until official price backfill is available.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | target | stage marker | check |",
        "| --- | --- | --- | --- |",
    ]
    for row in round178_case_candidate_rows():
        stage_date = row["stage4c_date"] or row["stage4b_date"] or row["stage3_date"] or row["stage2_date"] or row["stage1_date"] or "undated"
        lines.append(f"| `{row['case_id']}` | `{row['target_id']}` | {stage_date} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `ROYALTY_PLATFORM_REQUIRES_ADOPTION`: SC/royalty platforms need actual adoption and royalty revenue.",
            "- `ONCOLOGY_COMMERCIALIZATION_REQUIRES_SCRIPTS`: oncology approval needs scripts, PBM/access, market share, and royalty.",
            "- `GLP1_GENERIC_PATENT_AND_SALES_GATE`: generic GLP-1 stories need patent clearance and sales.",
            "- `MEDICAL_AI_REIMBURSEMENT_REQUIRED`: AI validation needs reimbursement and recurring revenue.",
            "- `CMC_CRL_BLOCKS_UNSAFE_GREEN`: manufacturing inspection or CRL blocks approval-driven Green.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round178_score_stage_price_alignment_markdown() -> str:
    lines = [
        "# Round-178 R7 Loop-11 Score / Stage / Price Alignment",
        "",
        "Round 178 checks whether Korea healthcare evidence moves from approval, partner, and AI-performance narratives into royalty, prescriptions, reimbursement, repeat revenue, and price-path confirmation.",
        "This is calibration material only; it does not change production scoring.",
        "",
        "| case | score-stage view | price-path signal | verdict | normalization adjustment |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in ROUND178_SCORE_STAGE_PRICE_ALIGNMENT:
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
            "- Stage 3-Green remains strict. R7 Loop 11 adds better Stage 2/3 diagnostics, not weaker thresholds.",
            "- The same event can be positive and risky: for example, Alteogen approval supports Stage 2/3 review while also requiring 4B cooling if price outruns royalty adoption.",
        ]
    )
    return "\n".join(lines) + "\n"


def _score_price_alignment(candidate: Round178CaseCandidate) -> str:
    if candidate.case_type == "4c_thesis_break":
        return "false_positive_score"
    if candidate.case_type in {"4b_watch", "overheat", "event_premium"}:
        return "price_moved_without_evidence"
    if candidate.case_type == "failed_rerating":
        return "evidence_good_but_price_failed"
    if candidate.case_type in {"structural_success", "success_candidate"} and "candidate" in candidate.alignment_hint:
        return "aligned"
    return "unknown"


def _rerating_result(candidate: Round178CaseCandidate) -> str:
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


def _score_weight_hint(target: Round178ScoreTarget) -> dict[str, float]:
    weights = target.score_weight.as_dict()
    return {
        "eps_fcf": _numeric_weight(weights["commercialization_eps_fcf_conversion"]),
        "visibility": _numeric_weight(weights["prescription_royalty_reimbursement_repeat_revenue_visibility"]),
        "partner_contract": _numeric_weight(weights["partner_approval_contract_visibility"]),
        "risk_confidence": _numeric_weight(weights["safety_regulatory_cmc_patent_disclosure_confidence"]),
        "price_validation": _numeric_weight(weights["early_price_path_validation"]),
        "cash_discipline": _numeric_weight(weights["cash_runway_capital_discipline"]),
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
    "ROUND178_BASE_SCORE_WEIGHTS",
    "ROUND178_CASE_CANDIDATES",
    "ROUND178_DEFAULT_CASES_PATH",
    "ROUND178_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND178_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND178_HELPER_OVERLAY_TARGET_COUNT",
    "ROUND178_HELPER_OVERLAY_TARGET_IDS",
    "ROUND178_PRICE_FIELDS",
    "ROUND178_SCORE_STAGE_PRICE_ALIGNMENT",
    "ROUND178_SCORE_TARGETS",
    "ROUND178_SOURCE_CANONICAL_TARGET_COUNT",
    "ROUND178_SOURCE_CANONICAL_TARGET_IDS",
    "ROUND178_STAGE_CAPS",
    "render_round178_green_guardrail_markdown",
    "render_round178_price_validation_plan_markdown",
    "render_round178_risk_overlay_markdown",
    "render_round178_score_stage_price_alignment_markdown",
    "render_round178_summary_markdown",
    "round178_base_score_weight_rows",
    "round178_case_candidate_rows",
    "round178_case_records",
    "round178_price_field_rows",
    "round178_score_profile_rows",
    "round178_score_stage_price_alignment_rows",
    "round178_stage_cap_rows",
    "round178_stage_date_rows",
    "round178_summary",
    "round178_target_for",
    "write_round178_r7_loop11_reports",
]
