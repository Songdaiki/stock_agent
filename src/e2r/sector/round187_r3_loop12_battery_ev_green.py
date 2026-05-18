"""Round-187 R3 Loop-12 Korea battery, EV, and green-energy pack.

Round 187 extends the R3 case library around Korea-listed battery cell,
ESS pivot, sodium-ion, separator, copper foil, electrolyte, battery equipment,
recycling, hydrogen fuel cell, solar localization, wind policy, battery
safety, and battery transparency risks. It is calibration/report material
only. Production feature engineering, scoring, staging, and RedTeam code must
not import this module.
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


ROUND187_SOURCE_ROUND_PATH = "docs/round/round_187.md"
ROUND187_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round187_r3_loop12_battery_ev_green"
ROUND187_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r3_loop12_round187.jsonl"
ROUND187_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round187_r3_loop12_v12.csv"
ROUND187_SOURCE_CANONICAL_TARGET_IDS: tuple[str, ...] = (
    "EV_TO_ESS_CAPACITY_REDEPLOYMENT_KOREA",
    "BATTERY_CONTRACT_CANCELLATION_4C",
    "BATTERY_TAX_CREDIT_QUALITY_OVERLAY",
    "SEPARATOR_EV_DEMAND_CYCLE",
    "COPPER_FOIL_EV_DEMAND_CYCLE",
    "ELECTROLYTE_CAPA_SUPPLYCHAIN",
    "BATTERY_EQUIPMENT_CAPEX_CYCLE",
    "BATTERY_RECYCLING_UNIT_ECONOMICS",
    "SODIUM_ION_NEXTGEN_MATERIALS",
    "HYDROGEN_FUEL_CELL_INFRA_KOREA",
    "SOLAR_US_LOCALIZATION_SUPPLYCHAIN",
    "WIND_POLICY_PERMITTING_RISK",
    "BATTERY_SAFETY_INDUSTRIAL_ACCIDENT_OVERLAY",
    "EV_BATTERY_TRANSPARENCY_REGULATORY_OVERLAY",
    "DISCLOSURE_CONFIDENCE_CAP",
)
ROUND187_SOURCE_CANONICAL_TARGET_COUNT = len(ROUND187_SOURCE_CANONICAL_TARGET_IDS)


@dataclass(frozen=True)
class Round187ScoreWeightDraft:
    eps_fcf_opm: int | str
    contract_customer_utilization_visibility: int | str
    capa_line_conversion: int | str
    policy_subsidy_quality: int | str
    early_price_validation: int | str
    safety_regulatory_quality_disclosure: int | str
    valuation_4b_room: int | str

    def as_dict(self) -> dict[str, int | str]:
        return {
            "eps_fcf_opm": self.eps_fcf_opm,
            "contract_customer_utilization_visibility": self.contract_customer_utilization_visibility,
            "capa_line_conversion": self.capa_line_conversion,
            "policy_subsidy_quality": self.policy_subsidy_quality,
            "early_price_validation": self.early_price_validation,
            "safety_regulatory_quality_disclosure": self.safety_regulatory_quality_disclosure,
            "valuation_4b_room": self.valuation_4b_room,
        }


@dataclass(frozen=True)
class Round187ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round187ScoreWeightDraft
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
        return Round10LargeSector.BATTERY_EV_GREEN

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round187CaseCandidate:
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
class Round187BaseScoreWeight:
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
class Round187StageCap:
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
class Round187ScoreStagePriceAlignment:
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
    capa: int | str,
    policy: int | str,
    price: int | str,
    safety: int | str,
    valuation: int | str,
) -> Round187ScoreWeightDraft:
    return Round187ScoreWeightDraft(eps, visibility, capa, policy, price, safety, valuation)


CAP_WEIGHT = _w("cap", "cap", "cap", "cap", "cap", "cap", "+")
GATE_WEIGHT = _w("gate", "gate", "gate", "gate", "gate", "gate", "gate")


ROUND187_BASE_SCORE_WEIGHTS: tuple[Round187BaseScoreWeight, ...] = (
    Round187BaseScoreWeight("eps_fcf_opm_conversion", 24, "keep_high", "R3 Loop 12 requires OP/EPS/FCF conversion, not EV/ESS/hydrogen/solar/wind keywords."),
    Round187BaseScoreWeight("contract_customer_utilization_visibility", 22, "detail_required", "Customer, amount, period, GWh/MW/tonnage, production timing, and utilization drive Stage 2 quality."),
    Round187BaseScoreWeight("capa_redeployment_line_conversion", 12, "stage2_not_green", "EV-to-ESS conversion, solar localization, fuel-cell mass production, and wind delivery need utilization proof."),
    Round187BaseScoreWeight("policy_subsidy_quality", 10, "raised_for_loop12", "IRA AMPC, UFLPA, hydrogen subsidy, and wind permitting can create or break reported profit quality."),
    Round187BaseScoreWeight("early_price_path_validation", 10, "required_backfill", "Stage 2 이후 MFE, cancellation MAE, event return, and relative strength separate validation from overheating."),
    Round187BaseScoreWeight("safety_regulatory_quality_disclosure", 12, "hard_review", "Battery fire, quality failure, customs detention, supplier disclosure, and missing detail can block Green."),
    Round187BaseScoreWeight("valuation_room_4b_runway", 10, "cool_crowded_names", "Battery/ESS/hydrogen/solar/wind narratives often need 4B cooling when price outruns ex-subsidy earnings."),
)


ROUND187_STAGE_CAPS: tuple[Round187StageCap, ...] = (
    Round187StageCap(
        "Stage 1",
        "45",
        ("ev_growth", "ess_growth", "hydrogen", "solar_localization", "wind_policy", "battery_recycling", "sodium_ion", "solid_state"),
        ("r3_loop12_keyword_4b_watch_case",),
        "Theme keywords route research only. Green is blocked before contract, utilization, ex-subsidy margin, FCF, and safety evidence.",
    ),
    Round187StageCap(
        "Stage 2",
        "70",
        ("customer_name", "contract_amount", "supply_period", "gwh_mw_or_tonnage", "production_start", "line_conversion", "factory_investment", "strategic_partnership"),
        ("lges_ess_pivot_tax_credit_stage2_case", "lg_chem_sinopec_sodium_ion_stage2_option_case", "qcells_us_localization_stage2_case"),
        "Stage 2 can be strong, but Stage 3 waits for utilization, OP/FCF, customer diversification, safety, and policy-risk clearance.",
    ),
    Round187StageCap(
        "Stage 3",
        "requires_5_of_8",
        ("customer_amount_period_confirmed", "op_eps_revision_or_op_beat", "profit_ex_subsidy_or_fcf_improves", "utilization_recovery", "60d_mfe_20pct_after_stage2", "repeat_contract_or_new_customer", "no_safety_customs_policy_hard_issue", "valuation_not_overheated"),
        ("doosan_fuelcell_ceres_sofc_stage23_candidate_case", "battery_equipment_capex_cycle_stage2_candidate_case"),
        "Stage 3 early catch is possible only when customer/contract detail, utilization, ex-subsidy profit, FCF, price path, and RedTeam align.",
    ),
    Round187StageCap(
        "Stage 4B",
        "requires_4_of_6",
        ("stage2_120d_mfe_80pct", "keyword_rally_without_contract_or_utilization", "profit_ex_subsidy_weak_but_price_rises", "crowded_ess_hydrogen_solar_wind_reports", "op_eps_revision_lags_price", "ev_slowdown_ignored_by_material_equipment_basket"),
        ("r3_loop12_keyword_4b_watch_case",),
        "Policy, subsidy, ESS, hydrogen, solar, wind, sodium-ion, and recycling rallies are cooled when earnings cannot follow.",
    ),
    Round187StageCap(
        "Stage 4C",
        "hard_gate",
        ("large_customer_contract_cancellation", "customer_ev_model_cancellation", "factory_utilization_collapse_or_sale_review", "profit_ex_subsidy_collapse", "customs_uflpa_supply_chain_block", "wind_permit_or_lease_halt", "battery_fire_or_fatal_accident", "battery_supplier_disclosure_trust_issue", "large_dilution_or_cash_burn"),
        ("lges_ford_freudenberg_contract_cancellation_4c_case", "aricell_battery_safety_fire_hard_4c_case"),
        "A single hard contract, utilization, subsidy-quality, customs, policy, safety, disclosure, or dilution issue can block Green.",
    ),
)


ROUND187_SCORE_TARGETS: tuple[Round187ScoreTarget, ...] = (
    Round187ScoreTarget(
        "EV_TO_ESS_CAPACITY_REDEPLOYMENT_KOREA",
        E2RArchetype.EV_TO_ESS_CAPACITY_REDEPLOYMENT_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(24, 22, 14, 10, 10, 12, 8),
        ("ev_slowdown", "ess_battery", "data_center_power", "ira_ampc"),
        ("ess_production_expansion", "investment_delay", "line_redeployment", "quarterly_profit_improvement"),
        ("ess_revenue_growth", "profit_ex_subsidy_improves", "utilization_recovery", "fcf_improvement", "customer_diversification"),
        ("ess_keyword_rally_before_ex_subsidy_profit", "policy_credit_priced_as_core_profit"),
        ("ev_slowdown_persists", "subsidy_dependency", "contract_cancellation", "plant_ramp_delay"),
        ("profit_ex_subsidy_improves", "utilization_recovery", "fcf_improvement", "customer_diversification"),
        ("profit_ex_subsidy_weak", "utilization_missing", "ev_slowdown", "contract_cancellation"),
        ("subsidy_quality", "utilization", "ess_pivot_to_fcf"),
        "ESS pivot is Stage 2 evidence, not Green before ex-subsidy OPM, utilization, FCF, and customer diversification.",
    ),
    Round187ScoreTarget(
        "BATTERY_CONTRACT_CANCELLATION_4C",
        E2RArchetype.BATTERY_CONTRACT_CANCELLATION_4C,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        ("battery_supply_contract", "ev_customer_demand", "long_term_contract"),
        ("contract_cancellation_identified", "customer_strategy_shift"),
        ("not_green_until_customer_strategy_and_utilization_recovered",),
        ("battery_contract_value_priced_without_customer_strategy_risk",),
        ("contract_cancelled", "expected_revenue_loss", "customer_ev_model_cancelled", "utilization_ramp_delay"),
        ("customer_strategy_stable", "replacement_customer", "utilization_recovered"),
        ("contract_cancelled", "customer_strategy_risk", "revenue_loss", "expected_revenue_loss"),
        ("contract_cancellation", "customer_strategy_reversal", "utilization_risk"),
        "Large battery contract cancellations are hard 4C until replacement demand, utilization, and revenue recovery are proven.",
        hard_gate=True,
    ),
    Round187ScoreTarget(
        "BATTERY_TAX_CREDIT_QUALITY_OVERLAY",
        E2RArchetype.BATTERY_TAX_CREDIT_QUALITY_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        CAP_WEIGHT,
        ("ira_ampc", "tax_credit_profit", "reported_op_improvement"),
        ("profit_ex_subsidy_disclosed", "subsidy_dependence_measured"),
        ("not_green_until_profit_ex_subsidy_or_fcf_improves",),
        ("tax_credit_drives_price_before_core_margin",),
        ("profit_ex_subsidy_weak", "subsidy_policy_change", "core_opm_missing"),
        ("profit_ex_subsidy_improves", "fcf_improvement", "policy_risk_low"),
        ("profit_ex_subsidy_weak", "policy_dependency", "core_margin_missing"),
        ("subsidy_quality", "core_margin"),
        "Reported profit quality is capped when ex-subsidy profit and FCF are weak.",
    ),
    Round187ScoreTarget(
        "SEPARATOR_EV_DEMAND_CYCLE",
        E2RArchetype.SEPARATOR_EV_DEMAND_CYCLE,
        Round10ThemePosture.REDTEAM_FIRST,
        _w(18, 14, 10, 8, 8, 12, 8),
        ("separator", "ev_battery_material", "sk_on_volume"),
        ("customer_shipment", "capa", "utilization_signal"),
        ("utilization_recovery", "opm_improvement", "customer_diversification", "fcf_signal"),
        ("separator_keyword_rally_ignores_ev_slowdown",),
        ("sale_review", "ev_demand_slowdown", "parent_loss", "utilization_risk"),
        ("utilization_recovery", "opm_improvement", "customer_diversification"),
        ("sale_review", "ev_slowdown", "parent_loss", "utilization_missing"),
        ("ev_demand_cycle", "utilization", "parent_restructuring"),
        "Separator strategic value is capped when EV demand slowdown, parent losses, or sale review break utilization visibility.",
    ),
    Round187ScoreTarget(
        "COPPER_FOIL_EV_DEMAND_CYCLE",
        E2RArchetype.COPPER_FOIL_EV_DEMAND_CYCLE,
        Round10ThemePosture.REDTEAM_FIRST,
        _w(18, 15, 10, 8, 8, 10, 8),
        ("copper_foil", "ev_battery_material", "customer_capa"),
        ("customer_contract", "utilization_signal", "spread_or_asp_signal"),
        ("utilization_recovery", "opm_improvement", "customer_diversification", "fcf_signal"),
        ("copper_foil_theme_rally_without_utilization",),
        ("ev_slowdown", "utilization_missing", "asp_pressure", "customer_concentration"),
        ("customer_contract", "utilization_recovery", "opm_improvement"),
        ("ev_slowdown", "utilization_missing", "opm_missing"),
        ("ev_demand_cycle", "utilization_gate"),
        "Copper foil remains Watch/Red until customers, utilization, ASP/spread, and OPM improve.",
    ),
    Round187ScoreTarget(
        "ELECTROLYTE_CAPA_SUPPLYCHAIN",
        E2RArchetype.ELECTROLYTE_CAPA_SUPPLYCHAIN,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(20, 17, 12, 8, 8, 10, 8),
        ("electrolyte", "battery_chemicals", "capa_expansion"),
        ("customer_contract", "production_start", "capa_visibility"),
        ("opm_improvement", "utilization_recovery", "customer_diversification", "fcf_signal"),
        ("electrolyte_capa_keyword_rally",),
        ("customer_missing", "opm_missing", "utilization_missing", "raw_material_cost"),
        ("customer_contract", "opm_improvement", "utilization_recovery"),
        ("customer_missing", "opm_missing", "capa_before_demand"),
        ("capa_to_margin", "customer_contract"),
        "Electrolyte CAPA is Stage 1/2 evidence until customer, utilization, OPM, and FCF are visible.",
    ),
    Round187ScoreTarget(
        "BATTERY_EQUIPMENT_CAPEX_CYCLE",
        E2RArchetype.BATTERY_EQUIPMENT_CAPEX_CYCLE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(21, 19, 12, 8, 10, 10, 8),
        ("battery_equipment", "cell_equipment", "customer_capex"),
        ("equipment_order", "customer_name", "shipment_schedule", "capex_plan"),
        ("shipment_revenue", "op_eps_revision", "repeat_order", "margin_visible"),
        ("equipment_order_priced_before_delivery",),
        ("customer_capex_delay", "order_pushout", "ev_demand_slowdown", "op_eps_missing"),
        ("equipment_order", "shipment_revenue", "op_eps_revision", "repeat_order"),
        ("capex_delay", "order_pushout", "shipment_missing"),
        ("customer_capex_cycle", "order_to_revenue"),
        "Battery equipment can be Stage 2~3 only when customer CAPEX becomes orders, shipment revenue, OP/EPS, and repeat demand.",
    ),
    Round187ScoreTarget(
        "BATTERY_RECYCLING_UNIT_ECONOMICS",
        E2RArchetype.BATTERY_RECYCLING_UNIT_ECONOMICS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(19, 16, 10, 8, 8, 10, 8),
        ("battery_recycling", "black_mass", "metal_recovery", "closed_loop"),
        ("collection_volume", "customer_contract", "metal_price_context"),
        ("unit_economics_positive", "recovery_volume", "opm_improvement", "fcf_signal"),
        ("recycling_theme_rally_without_unit_economics",),
        ("metal_price_decline", "collection_volume_missing", "margin_missing", "policy_only"),
        ("unit_economics_positive", "volume_visible", "opm_improvement"),
        ("unit_economics_missing", "metal_price_risk", "volume_missing"),
        ("unit_economics", "recovery_volume"),
        "Battery recycling needs recovery volume, metal-price sensitivity, margin, and FCF before Stage 3.",
    ),
    Round187ScoreTarget(
        "SODIUM_ION_NEXTGEN_MATERIALS",
        E2RArchetype.SODIUM_ION_NEXTGEN_MATERIALS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(18, 16, 10, 10, 8, 10, 8),
        ("sodium_ion", "nextgen_battery", "low_cost_ess", "low_speed_ev"),
        ("strategic_development_partner", "target_market_defined", "commercialization_timeline"),
        ("commercial_customer", "material_supply_contract", "mass_production_revenue", "opm_fcf_visible"),
        ("sodium_ion_keyword_rally_without_revenue",),
        ("commercial_customer_missing", "revenue_missing", "cost_advantage_unproven", "technology_substitution_risk"),
        ("commercial_customer", "supply_contract", "mass_production_revenue", "cost_advantage"),
        ("commercial_customer_missing", "revenue_missing", "cost_advantage_unproven"),
        ("commercialization_gate", "nextgen_material"),
        "Sodium-ion is Stage 2 option evidence before commercial customers, supply contracts, revenue, OPM, and FCF.",
    ),
    Round187ScoreTarget(
        "HYDROGEN_FUEL_CELL_INFRA_KOREA",
        E2RArchetype.HYDROGEN_FUEL_CELL_INFRA_KOREA,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(21, 18, 12, 10, 10, 10, 8),
        ("hydrogen_fuel_cell", "sofc", "ai_data_center_power", "electrolyzer"),
        ("mass_production", "factory_capacity_mw", "sales_plan", "hydrogen_capa_investment"),
        ("revenue_recognition", "repeat_service", "opm_fcf_improvement", "data_center_customer"),
        ("hydrogen_ai_power_keyword_rally",),
        ("customer_missing", "profitability_missing", "subsidy_dependence", "infrastructure_gap"),
        ("revenue_recognition", "repeat_service", "opm_fcf_improvement", "customer_visible"),
        ("customer_missing", "opm_missing", "subsidy_dependence"),
        ("fuel_cell_sales_to_margin", "ai_data_center_power"),
        "Hydrogen/fuel-cell Stage 2 evidence becomes Stage 3 only with sales, customers, recurring service, OPM, and FCF.",
    ),
    Round187ScoreTarget(
        "SOLAR_US_LOCALIZATION_SUPPLYCHAIN",
        E2RArchetype.SOLAR_US_LOCALIZATION_SUPPLYCHAIN,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        _w(20, 18, 12, 12, 8, 12, 8),
        ("solar_us_localization", "ira_solar", "qcells_georgia", "china_dependency_reduction"),
        ("us_factory_investment", "supply_chain_localization", "production_ramp"),
        ("normal_operation", "asp_margin_visible", "ira_credit_quality", "fcf_signal", "customer_shipments"),
        ("solar_localization_keyword_rally",),
        ("customs_detention", "uflpa_risk", "furlough", "component_import_block", "china_supply_dependency"),
        ("normal_operation", "margin_visible", "fcf_signal", "customs_cleared"),
        ("customs_detention", "uflpa_risk", "production_disruption"),
        ("localization_to_normal_operation", "customs_gate"),
        "Solar localization is Stage 2 evidence, but customs/UFLPA, normal operations, margin, and FCF gate Stage 3.",
    ),
    Round187ScoreTarget(
        "WIND_POLICY_PERMITTING_RISK",
        E2RArchetype.WIND_POLICY_PERMITTING_RISK,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        ("offshore_wind", "wind_tower", "us_wind_project", "permit_policy"),
        ("project_backlog", "customer_contract", "policy_review_identified"),
        ("not_green_until_permit_and_project_financing_clear",),
        ("wind_policy_keyword_rally_ignores_permit_risk",),
        ("permit_halt", "lease_suspension", "national_security_review", "project_delay_or_cancel"),
        ("permit_clear", "delivery_revenue", "project_financing_stable"),
        ("permit_halt", "lease_suspension", "project_cancel"),
        ("policy_permit_gate", "delivery_revenue"),
        "Wind equipment needs contract and delivery revenue; permit or lease halt is a hard policy overlay.",
        hard_gate=True,
    ),
    Round187ScoreTarget(
        "BATTERY_SAFETY_INDUSTRIAL_ACCIDENT_OVERLAY",
        E2RArchetype.BATTERY_SAFETY_INDUSTRIAL_ACCIDENT_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        ("battery_factory", "battery_safety", "quality_control"),
        ("fatal_accident_identified", "quality_failure_investigation", "safety_training_gap"),
        ("not_green_until_safety_quality_controls_recovered",),
        ("battery_growth_story_ignores_safety_gate",),
        ("fatal_accident", "quality_failure", "safety_management_failure", "criminal_liability", "consumer_trust_damage"),
        ("safety_controls_recovered", "quality_controls_verified", "regulatory_clearance"),
        ("fatal_accident", "quality_failure", "safety_management_failure"),
        ("safety_quality_hard_gate",),
        "Fatal battery accidents and quality failures are hard 4C overlays across battery manufacturing, materials, and equipment.",
        hard_gate=True,
    ),
    Round187ScoreTarget(
        "EV_BATTERY_TRANSPARENCY_REGULATORY_OVERLAY",
        E2RArchetype.EV_BATTERY_TRANSPARENCY_REGULATORY_OVERLAY,
        Round10ThemePosture.REDTEAM_FIRST,
        GATE_WEIGHT,
        ("ev_battery_supplier", "supplier_disclosure", "consumer_trust"),
        ("supplier_disclosure_issue", "regulatory_probe_or_fine"),
        ("not_green_until_supplier_transparency_and_trust_recovered",),
        ("ev_battery_story_ignores_supplier_transparency",),
        ("supplier_misrepresentation", "ev_fire_trust_issue", "regulatory_fine", "consumer_trust_damage"),
        ("transparent_supplier_disclosure", "quality_trust_recovered"),
        ("supplier_disclosure_issue", "consumer_trust_damage", "regulatory_fine"),
        ("battery_transparency_gate",),
        "Battery supplier disclosure and trust issues are hard RedTeam overlays for cell makers and auto customers.",
        hard_gate=True,
    ),
    Round187ScoreTarget(
        "DISCLOSURE_CONFIDENCE_CAP",
        E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        Round10ThemePosture.REDTEAM_FIRST,
        CAP_WEIGHT,
        ("opendart_list_only", "media_report", "mou", "policy_headline", "factory_announcement"),
        ("detail_fetch_required", "customer_amount_period_utilization_opm_required"),
        ("not_green_until_binding_detail_and_eps_fcf_path",),
        ("headline_priced_before_detail",),
        ("customer_missing", "amount_missing", "period_missing", "utilization_missing", "opm_unknown", "non_binding"),
        ("binding_contract", "customer_name", "contract_amount", "utilization", "opm_fcf_visible"),
        ("opendart_list_only", "media_only", "mou_loi", "detail_missing"),
        ("detail_missing", "customer_unknown", "utilization_unknown"),
        "Round 187 caps list-only, media-only, policy-only, factory-only, and missing-detail evidence before Green.",
    ),
)


ROUND187_CASE_CANDIDATES: tuple[Round187CaseCandidate, ...] = (
    Round187CaseCandidate(
        "lges_ess_pivot_tax_credit_stage2_case",
        "EV_TO_ESS_CAPACITY_REDEPLOYMENT_KOREA",
        "373220",
        "LG에너지솔루션 ESS pivot / tax credit quality",
        "KR",
        "success_candidate",
        ("ev_slowdown", "ess_production_expansion", "investment_delay", "quarterly_profit_improvement", "ira_ampc_dependency"),
        ("profit_ex_subsidy_weak", "demand_slowdown_warning", "share_price_minus_2_3pct", "utilization_recovery_needed"),
        "stage2_strong_but_green_blocked_before_ex_subsidy_opm_utilization_fcf",
        "needs_profit_ex_subsidy_utilization_fcf_price_backfill",
        ("round_187.md Reuters LGES Q2 profit / demand slowdown",),
        "LGES ESS pivot is Stage 2 evidence, but ex-subsidy OPM, utilization, FCF, and customer diversification gate Stage 3.",
        (E2RArchetype.BATTERY_TAX_CREDIT_QUALITY_OVERLAY, E2RArchetype.EVIDENCE_GOOD_BUT_PRICE_FAILED),
    ),
    Round187CaseCandidate(
        "lg_chem_sinopec_sodium_ion_stage2_option_case",
        "SODIUM_ION_NEXTGEN_MATERIALS",
        "051910",
        "LG화학 Sinopec sodium-ion materials option",
        "KR",
        "success_candidate",
        ("sodium_ion_materials", "sinopec_joint_development", "ess_low_speed_ev_target_market", "china_market_growth_forecast"),
        ("commercial_customer_missing", "supply_contract_missing", "mass_production_revenue_missing", "cost_advantage_unproven"),
        "stage2_option_not_green_before_commercial_customer_revenue_opm",
        "needs_customer_supply_contract_revenue_price_backfill",
        ("round_187.md Reuters LG Chem / Sinopec sodium-ion partnership",),
        "Sodium-ion partnership is Stage 2 option evidence. Stage 3 waits for commercial customer, supply contract, revenue, OPM, and cost advantage.",
        (E2RArchetype.STAGE2_EVIDENCE_NOT_GREEN, E2RArchetype.COMMERCIALIZATION_FAILURE),
    ),
    Round187CaseCandidate(
        "doosan_fuelcell_ceres_sofc_stage23_candidate_case",
        "HYDROGEN_FUEL_CELL_INFRA_KOREA",
        "336260",
        "두산퓨얼셀 / Ceres SOFC mass-production candidate",
        "KR",
        "success_candidate",
        ("sofc_mass_production", "factory_capacity_50mw", "ai_data_center_power_target", "sales_plan", "recurring_service_option"),
        ("customer_missing", "revenue_recognition_missing", "opm_fcf_missing", "subsidy_dependence"),
        "stage2_to_stage3_candidate_if_sales_customer_opm_fcf_align",
        "needs_sales_customer_opm_fcf_price_backfill",
        ("round_187.md Ceres SOFC mass production in Korea",),
        "Doosan fuel-cell path can move toward Stage 3 only if SOFC sales, customers, recurring service, OPM, FCF, and price path align.",
        (E2RArchetype.STRUCTURAL_STAGE3_EARLY_CAPTURE,),
    ),
    Round187CaseCandidate(
        "hyundai_hydrogen_fuelcell_ulsan_stage2_macro_case",
        "HYDROGEN_FUEL_CELL_INFRA_KOREA",
        "005380/HYDROGEN_BASKET",
        "현대차 울산 수소연료전지 공장 macro",
        "KR",
        "success_candidate",
        ("hydrogen_fuelcell_capa", "ulsan_930bn_krw_investment", "2027_completion_target", "fuel_cell_electrolyzer_plan"),
        ("utilization_missing", "customer_missing", "revenue_missing", "subsidy_dependence"),
        "stage2_macro_for_hydrogen_value_chain_not_green_before_utilization",
        "needs_utilization_customer_revenue_price_backfill",
        ("round_187.md Reuters Hyundai hydrogen fuel cell plant",),
        "Hyundai hydrogen CAPA is macro Stage 2 evidence for the value chain; utilization, customers, revenue, and margins gate Stage 3.",
        (E2RArchetype.STAGE2_EVIDENCE_NOT_GREEN,),
    ),
    Round187CaseCandidate(
        "qcells_us_localization_stage2_case",
        "SOLAR_US_LOCALIZATION_SUPPLYCHAIN",
        "009830",
        "한화솔루션 / Qcells U.S. solar localization",
        "KR",
        "success_candidate",
        ("us_solar_localization", "georgia_factory_investment", "cartersville_ramp", "ira_solar_supply_chain"),
        ("customs_uflpa_gate", "normal_operation_needed", "margin_fcf_missing", "component_import_risk"),
        "stage2_localization_not_green_before_customs_normal_operation_margin_fcf",
        "needs_customs_operation_margin_fcf_price_backfill",
        ("round_187.md AP Qcells Georgia investment",),
        "Qcells localization is Stage 2 evidence, but customs/UFLPA clearance, normal operation, margin, and FCF gate Stage 3.",
        (E2RArchetype.STAGE2_EVIDENCE_NOT_GREEN,),
    ),
    Round187CaseCandidate(
        "lges_ford_freudenberg_contract_cancellation_4c_case",
        "BATTERY_CONTRACT_CANCELLATION_4C",
        "373220",
        "LG에너지솔루션 Ford / Freudenberg contract cancellations",
        "KR",
        "4c_thesis_break",
        ("ford_contract_cancelled", "freudenberg_contract_cancelled", "expected_revenue_loss_13_5tn_krw", "share_price_minus_7_6pct"),
        ("contract_cancelled", "customer_ev_model_cancelled", "expected_revenue_loss", "utilization_ramp_delay"),
        "large_customer_cancellation_hard_4c",
        "needs_contract_loss_mae_utilization_backfill",
        ("round_187.md Reuters LGES Ford cancellation", "round_187.md Reuters Freudenberg cancellation"),
        "Large battery supply cancellations are hard 4C until replacement demand, utilization, and revenue recovery are proven.",
        (E2RArchetype.CONTRACT_CANCELLATION_CUSTOMER_STRATEGY_RISK,),
    ),
    Round187CaseCandidate(
        "skiet_separator_sale_review_4c_case",
        "SEPARATOR_EV_DEMAND_CYCLE",
        "361610/096770",
        "SK IE Technology separator sale review / SK On loss",
        "KR",
        "4c_thesis_break",
        ("separator", "sale_review", "ev_demand_slowdown", "sk_on_loss_expansion"),
        ("sale_review", "parent_loss", "ev_demand_slowdown", "utilization_risk"),
        "separator_demand_visibility_breaks_until_utilization_and_parent_restructuring_resolved",
        "needs_sale_review_utilization_loss_price_backfill",
        ("round_187.md Reuters SK Innovation considering SKIET sale",),
        "Separator exposure is capped when EV slowdown, parent losses, and sale review break utilization visibility.",
        (E2RArchetype.EVIDENCE_GOOD_BUT_PRICE_FAILED,),
    ),
    Round187CaseCandidate(
        "qcells_customs_detention_furlough_4c_case",
        "SOLAR_US_LOCALIZATION_SUPPLYCHAIN",
        "009830",
        "Qcells customs detention / furlough 4C watch",
        "KR",
        "4c_thesis_break",
        ("customs_detention", "uflpa_supply_chain_scrutiny", "furlough_1000_workers", "contractor_reduction"),
        ("customs_detention", "uflpa_risk", "production_disruption", "component_import_block"),
        "solar_localization_capped_by_customs_and_supply_chain_disruption",
        "needs_customs_resolution_production_price_backfill",
        ("round_187.md Reuters Qcells furlough due stalled shipments",),
        "U.S. localization does not create Green if customs detention and component supply-chain disruption stop normal production.",
        (E2RArchetype.OPERATIONAL_TRUST_BREAK,),
    ),
    Round187CaseCandidate(
        "cswind_wind_policy_permitting_4c_watch_case",
        "WIND_POLICY_PERMITTING_RISK",
        "112610/100090",
        "씨에스윈드·SK오션플랜트 offshore wind policy risk",
        "KR",
        "4c_thesis_break",
        ("offshore_wind", "permit_halt", "lease_suspension", "national_security_review", "project_delay_or_cancel"),
        ("permit_halt", "lease_suspension", "project_cancel", "customer_project_delay"),
        "wind_equipment_backlog_capped_by_policy_permitting_hard_gate",
        "needs_project_backlog_delivery_policy_price_backfill",
        ("round_187.md AP offshore wind permit pause", "round_187.md Guardian offshore wind lease suspension"),
        "Wind supply-chain candidates need project permits, financing, delivery revenue, and margin; permit/lease halt is a hard policy overlay.",
        (E2RArchetype.RENEWABLE_ENERGY_PROJECT_ECONOMICS,),
    ),
    Round187CaseCandidate(
        "aricell_battery_safety_fire_hard_4c_case",
        "BATTERY_SAFETY_INDUSTRIAL_ACCIDENT_OVERLAY",
        "BATTERY_SAFETY_KR",
        "Aricell battery factory fire safety overlay",
        "KR",
        "4c_thesis_break",
        ("battery_fire", "fatal_accident_23_deaths", "quality_failure", "safety_management_failure", "ceo_sentence"),
        ("fatal_accident", "quality_failure", "safety_management_failure", "criminal_liability", "consumer_trust_damage"),
        "fatal_battery_safety_issue_is_hard_4c_overlay",
        "needs_safety_resolution_regulatory_price_backfill",
        ("round_187.md Reuters Aricell fire police finding", "round_187.md Reuters CEO sentence"),
        "Fatal battery factory safety and quality failure is a hard 4C overlay for battery manufacturing, materials, and equipment candidates.",
        (E2RArchetype.EV_FIRE_RISK_OVERLAY, E2RArchetype.OPERATIONAL_TRUST_BREAK),
    ),
    Round187CaseCandidate(
        "mercedes_battery_supplier_disclosure_trust_case",
        "EV_BATTERY_TRANSPARENCY_REGULATORY_OVERLAY",
        "EV_BATTERY_TRUST_KR",
        "Mercedes EV battery supplier disclosure trust overlay",
        "KR",
        "4c_thesis_break",
        ("battery_supplier_disclosure_issue", "regulatory_fine", "ev_fire_trust_context", "consumer_trust_damage"),
        ("supplier_misrepresentation", "supplier_disclosure_issue", "regulatory_fine", "consumer_trust_damage"),
        "battery_supplier_transparency_issue_is_redteam_overlay",
        "needs_supplier_transparency_resolution_price_backfill",
        ("round_187.md Reuters Mercedes battery supplier disclosure fine",),
        "Battery supplier transparency and consumer-trust risk must remain visible for cell makers and EV customers.",
        (E2RArchetype.BATTERY_HEALTH_TRANSPARENCY_OVERLAY,),
    ),
    Round187CaseCandidate(
        "copper_foil_ev_demand_cycle_watch_case",
        "COPPER_FOIL_EV_DEMAND_CYCLE",
        "020150/336370",
        "롯데에너지머티리얼즈·솔루스첨단소재 copper foil EV demand cycle",
        "KR",
        "failed_rerating",
        ("copper_foil", "ev_battery_material", "customer_contract_needed", "utilization_needed"),
        ("ev_slowdown", "utilization_missing", "asp_pressure", "opm_missing"),
        "watch_red_until_customer_utilization_asp_opm_are_visible",
        "needs_customer_utilization_asp_opm_price_backfill",
        ("round_187.md copper foil watch/red rule",),
        "Copper foil is not Green before customer visibility, utilization, ASP/spread, OPM, and FCF are visible.",
    ),
    Round187CaseCandidate(
        "electrolyte_capa_supplychain_watch_case",
        "ELECTROLYTE_CAPA_SUPPLYCHAIN",
        "348370/025900",
        "엔켐·동화기업 electrolyte CAPA watch",
        "KR",
        "success_candidate",
        ("electrolyte_capa", "battery_chemical_supplychain", "customer_contract_needed", "opm_needed"),
        ("customer_missing", "opm_missing", "utilization_missing", "raw_material_cost"),
        "stage1_2_watch_not_green_before_customer_opm_utilization",
        "needs_customer_opm_utilization_price_backfill",
        ("round_187.md electrolyte CAPA rule",),
        "Electrolyte CAPA can route research, but customer, utilization, OPM, and FCF are required before Stage 3.",
    ),
    Round187CaseCandidate(
        "battery_equipment_capex_cycle_stage2_candidate_case",
        "BATTERY_EQUIPMENT_CAPEX_CYCLE",
        "137400/222080/299030",
        "피엔티·씨아이에스·하나기술 battery equipment CAPEX cycle",
        "KR",
        "success_candidate",
        ("battery_equipment", "customer_capex", "equipment_order_needed", "shipment_schedule_needed"),
        ("customer_capex_delay", "order_pushout", "shipment_missing", "op_eps_missing"),
        "stage2_candidate_only_when_customer_order_shipment_revision_backfilled",
        "needs_order_shipment_op_revision_price_backfill",
        ("round_187.md battery equipment capex cycle rule",),
        "Battery equipment can become Stage 2~3 only when customer CAPEX turns into orders, shipment revenue, OP/EPS, and repeat demand.",
        (E2RArchetype.STAGE2_EVIDENCE_NOT_GREEN,),
    ),
    Round187CaseCandidate(
        "battery_recycling_unit_economics_watch_case",
        "BATTERY_RECYCLING_UNIT_ECONOMICS",
        "365340/107600",
        "성일하이텍·새빗켐 battery recycling unit economics watch",
        "KR",
        "success_candidate",
        ("battery_recycling", "recovery_volume_needed", "metal_price_context_needed", "unit_economics_needed"),
        ("unit_economics_missing", "metal_price_risk", "collection_volume_missing", "margin_missing"),
        "watch_until_recovery_volume_unit_economics_opm_fcf_are_visible",
        "needs_volume_unit_economics_margin_price_backfill",
        ("round_187.md battery recycling unit economics rule",),
        "Recycling needs recovery volume, metal-price sensitivity, unit economics, OPM, and FCF before Stage 3.",
    ),
    Round187CaseCandidate(
        "r3_loop12_keyword_4b_watch_case",
        "BATTERY_TAX_CREDIT_QUALITY_OVERLAY",
        "R3_KEYWORD_4B",
        "R3 Loop 12 ESS·수소·태양광·풍력 keyword 4B watch",
        "KR",
        "4b_watch",
        ("ess_hydrogen_solar_wind_keyword_rally", "subsidy_or_policy_narrative", "op_eps_revision_lags_price"),
        ("profit_ex_subsidy_weak", "contract_utilization_missing", "crowded_narrative", "price_faster_than_revision"),
        "keyword_rally_before_contract_utilization_or_ex_subsidy_profit_is_4b_watch",
        "needs_mfe_mae_revision_valuation_backfill",
        ("round_187.md Stage 4B early conversion rule",),
        "R3 keywords can rally first, but price-only or subsidy-only moves need 4B cooling before they are mislabeled Stage 3.",
        (E2RArchetype.PRICE_ONLY_RALLY, E2RArchetype.CROWDED_RERATING_4B_WATCH),
    ),
    Round187CaseCandidate(
        "r3_loop12_disclosure_confidence_reference_case",
        "DISCLOSURE_CONFIDENCE_CAP",
        "R3_DISCLOSURE_CAP",
        "R3 Loop 12 OpenDART detail confidence reference",
        "KR",
        "failed_rerating",
        ("watch_disclosure_detail_required", "customer_amount_period_required", "utilization_opm_required", "subsidy_quality_required"),
        ("opendart_list_only", "media_only", "mou_loi", "detail_missing", "customer_missing", "utilization_unknown"),
        "list_media_policy_factory_only_cannot_create_green",
        "needs_opendart_detail_parser_backfill",
        ("round_187.md OpenDART detail and no-invented-fields rule",),
        "R3 Loop 12 requires detail fetch and forbids invented missing contract, utilization, subsidy, safety, and OPM fields.",
    ),
)


ROUND187_SCORE_STAGE_PRICE_ALIGNMENT: tuple[Round187ScoreStagePriceAlignment, ...] = (
    Round187ScoreStagePriceAlignment("lges_ess_pivot_tax_credit_stage2_case", "Stage 2 + quality cap", "Reported profit improved but ex-subsidy profit and price reaction need backfill", "subsidy_quality_not_green", "credit ESS pivot; cap before ex-subsidy OPM, utilization, FCF, and customer diversification"),
    Round187ScoreStagePriceAlignment("lg_chem_sinopec_sodium_ion_stage2_option_case", "Stage 2 option", "Joint development is not commercial revenue", "commercialization_gate_not_green", "credit sodium-ion option; cap before customer, supply contract, mass-production revenue, and OPM"),
    Round187ScoreStagePriceAlignment("doosan_fuelcell_ceres_sofc_stage23_candidate_case", "Stage 2~3 candidate", "SOFC mass production can be meaningful if sales/customer/OPM path validates", "stage3_candidate_if_revenue_opm_price_align", "credit SOFC/data-center power; require customer sales, recurring service, OPM, FCF, and price path"),
    Round187ScoreStagePriceAlignment("qcells_us_localization_stage2_case", "Stage 2 + customs gate", "Localization is useful but UFLPA/customs and normal-operation proof are pending", "localization_to_operation_gate", "credit U.S. supply chain; cap before customs clearance, normal operations, margin, and FCF"),
    Round187ScoreStagePriceAlignment("lges_ford_freudenberg_contract_cancellation_4c_case", "4C hard gate", "Large customer cancellations and revenue loss can dominate ESS pivot evidence", "contract_cancellation_blocks_green", "apply customer strategy and utilization hard gate"),
    Round187ScoreStagePriceAlignment("skiet_separator_sale_review_4c_case", "4C-watch", "EV slowdown, parent losses, and sale review break separator visibility", "separator_demand_break", "apply separator utilization and parent restructuring penalty"),
    Round187ScoreStagePriceAlignment("aricell_battery_safety_fire_hard_4c_case", "4C hard gate", "Fatal accident and quality failure are hard RedTeam overlays", "safety_hard_gate_alignment", "block Green until safety, quality controls, and regulatory clearance are proven"),
    Round187ScoreStagePriceAlignment("r3_loop12_keyword_4b_watch_case", "Stage 1/2 -> 4B-watch", "Keywords and subsidy/policy narratives can outrun ex-subsidy profit", "price_only_keyword_requires_4b_watch", "cool crowded ESS/hydrogen/solar/wind rallies before Stage 3 evidence appears"),
)


ROUND187_PRICE_FIELDS: tuple[str, ...] = (
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
    "relative_strength_vs_battery_basket",
    "relative_strength_vs_renewable_basket",
    "relative_strength_vs_hydrogen_basket",
    "contract_amount",
    "contract_counterparty",
    "contract_period",
    "gwh_mw_or_tonnage",
    "production_start_date",
    "revenue_recognition_timing",
    "customer_name_disclosed",
    "customer_strategy_risk",
    "utilization_rate",
    "line_conversion_flag",
    "ess_revenue_signal",
    "ev_revenue_signal",
    "subsidy_amount",
    "profit_ex_subsidy",
    "ira_ampc_dependency",
    "op_revision_before_stage3",
    "op_revision_after_stage3",
    "eps_revision_before_stage3",
    "eps_revision_after_stage3",
    "opm",
    "fcf_signal",
    "contract_cancellation_flag",
    "factory_idle_or_sale_review_flag",
    "customs_detention_flag",
    "uflpa_risk_flag",
    "wind_permit_halt_flag",
    "battery_fire_flag",
    "fatal_accident_flag",
    "supplier_disclosure_issue_flag",
    "inventory_loss_flag",
    "raw_material_price_exposure",
    "safety_or_quality_issue",
    "dilution_event_flag",
    "disclosure_confidence",
    "valuation_at_stage3",
    "valuation_at_stage4b",
)


def round187_target_for(target_id: str) -> Round187ScoreTarget | None:
    for target in ROUND187_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round187_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND187_CASE_CANDIDATES:
        target = round187_target_for(candidate.target_id)
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
                f"Round187 R3 Loop-12 Korea battery/EV/green case for {candidate.target_id}; "
                "calibration-only and focused on contract/customer/utilization, ex-subsidy OPM, FCF, policy/customs/safety risk, and price path."
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
            score_price_alignment=_round187_score_price_alignment(candidate),
            rerating_result=_round187_rerating_result(candidate),
            price_pattern=candidate.alignment_hint,
            score_weight_hint={
                "eps_fcf": _numeric_weight(weights["eps_fcf_opm"]),
                "visibility": _numeric_weight(weights["contract_customer_utilization_visibility"]),
                "capa_line_conversion": _numeric_weight(weights["capa_line_conversion"]),
                "policy_subsidy_quality": _numeric_weight(weights["policy_subsidy_quality"]),
                "early_price_validation": _numeric_weight(weights["early_price_validation"]),
                "safety_regulatory_disclosure": _numeric_weight(weights["safety_regulatory_quality_disclosure"]),
                "valuation_4b_room": _numeric_weight(weights["valuation_4b_room"]),
            },
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "stage3_early_catch_requires_5_of_8_loop12_conditions",
                "stage4b_cooling_requires_4_of_6_loop12_conditions",
                "require_contract_utilization_ex_subsidy_opm_fcf_price_path_for_green",
                "safety_customs_policy_disclosure_and_contract_cancellation_can_block_green",
                "ev_ess_hydrogen_solar_wind_recycling_keywords_cannot_create_stage3",
                "do_not_invent_contract_prices_utilization_subsidy_profit_mfe_mae_or_safety_resolution",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=False,
                price_data_available=False,
                stage_dates_confidence=0.2,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round187_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND187_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "eps_fcf_opm": str(weights["eps_fcf_opm"]),
                "contract_customer_utilization_visibility": str(weights["contract_customer_utilization_visibility"]),
                "capa_line_conversion": str(weights["capa_line_conversion"]),
                "policy_subsidy_quality": str(weights["policy_subsidy_quality"]),
                "early_price_validation": str(weights["early_price_validation"]),
                "safety_regulatory_quality_disclosure": str(weights["safety_regulatory_quality_disclosure"]),
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


def round187_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND187_CASE_CANDIDATES:
        target = round187_target_for(candidate.target_id)
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


def round187_stage_date_rows() -> tuple[dict[str, str], ...]:
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
        for target in ROUND187_SCORE_TARGETS
    )


def round187_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round187_backfill": "true"} for field in ROUND187_PRICE_FIELDS)


def round187_base_score_weight_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND187_BASE_SCORE_WEIGHTS)


def round187_stage_cap_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND187_STAGE_CAPS)


def round187_score_stage_price_alignment_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND187_SCORE_STAGE_PRICE_ALIGNMENT)


def round187_summary() -> dict[str, int | bool]:
    records = round187_case_records()
    return {
        "target_count": len(ROUND187_SCORE_TARGETS),
        "source_canonical_target_count": ROUND187_SOURCE_CANONICAL_TARGET_COUNT,
        "case_candidate_count": len(records),
        "base_score_axis_count": len(ROUND187_BASE_SCORE_WEIGHTS),
        "stage_cap_count": len(ROUND187_STAGE_CAPS),
        "score_stage_price_alignment_count": len(ROUND187_SCORE_STAGE_PRICE_ALIGNMENT),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "hard_gate_target_count": sum(1 for target in ROUND187_SCORE_TARGETS if target.hard_gate),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round187_r3_loop12_reports(
    *,
    output_directory: str | Path = ROUND187_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND187_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND187_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round187_r3_loop12_battery_ev_green_summary.md",
        "case_matrix": output / "round187_r3_loop12_case_matrix.csv",
        "stage_date_plan": output / "round187_r3_loop12_stage_date_plan.csv",
        "green_guardrails": output / "round187_r3_loop12_green_guardrails.md",
        "risk_overlays": output / "round187_r3_loop12_risk_overlays.md",
        "price_validation_plan": output / "round187_r3_loop12_price_validation_plan.md",
        "price_fields": output / "round187_r3_loop12_price_fields.csv",
        "base_score_weights": output / "round187_r3_loop12_base_score_weights.csv",
        "stage_caps": output / "round187_r3_loop12_stage_caps.csv",
        "score_stage_price_alignment": output / "round187_r3_loop12_score_stage_price_alignment.csv",
        "score_stage_price_alignment_md": output / "round187_r3_loop12_score_stage_price_alignment.md",
    }
    _write_case_jsonl(round187_case_records(), cases)
    _write_rows(round187_score_profile_rows(), score_profiles)
    _write_rows(round187_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round187_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round187_price_field_rows(), paths["price_fields"])
    _write_rows(round187_base_score_weight_rows(), paths["base_score_weights"])
    _write_rows(round187_stage_cap_rows(), paths["stage_caps"])
    _write_rows(round187_score_stage_price_alignment_rows(), paths["score_stage_price_alignment"])
    paths["summary"].write_text(render_round187_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round187_green_guardrail_markdown(), encoding="utf-8")
    paths["risk_overlays"].write_text(render_round187_risk_overlay_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round187_price_validation_plan_markdown(), encoding="utf-8")
    paths["score_stage_price_alignment_md"].write_text(render_round187_score_stage_price_alignment_markdown(), encoding="utf-8")
    return paths


def render_round187_summary_markdown() -> str:
    summary = round187_summary()
    lines = [
        "# Round-187 R3 Loop-12 Battery / EV / Green Summary",
        "",
        f"- source_round: `{ROUND187_SOURCE_ROUND_PATH}`",
        f"- large_sector: `{Round10LargeSector.BATTERY_EV_GREEN.value}`",
        "- loop: `R3 Loop 12 / v12.0`",
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
        "- R3 Loop 12 is Korea-first and reduces repeated focus on prior battery material names.",
        "- Example: LGES ESS pivot is Stage 2 evidence, but ex-subsidy OPM and utilization must improve before Stage 3.",
        "- Example: LG Chem sodium-ion partnership is Stage 2 option evidence, not commercial revenue.",
        "- Example: Qcells U.S. localization can be Stage 2, but customs/UFLPA and normal-operation proof gate Stage 3.",
        "- Example: Aricell fire, battery supplier disclosure, wind permit halt, and contract cancellation are RedTeam overlays.",
    ]
    return "\n".join(lines) + "\n"


def render_round187_green_guardrail_markdown() -> str:
    lines = [
        "# Round-187 R3 Loop-12 Green Guardrails",
        "",
        "Stage 3-Green is not granted for EV, ESS, hydrogen, solar, wind, recycling, sodium-ion, policy, subsidy, or factory words alone.",
        "",
        "## Stage 3 Early Catch",
        "",
        "R3 Loop 12 requires at least 5 of 8 checks:",
    ]
    stage3 = next(item for item in ROUND187_STAGE_CAPS if item.stage_band == "Stage 3")
    lines.extend(f"- `{field}`" for field in stage3.required_evidence)
    lines.extend(
        [
            "",
            "## What This Means",
            "",
            "- LGES: ESS pivot는 Stage 2지만 보조금 제외 OPM, 가동률, FCF가 필요.",
            "- Sodium-ion: 공동개발은 Stage 2 option이고 상용 고객·매출 전에는 Green 금지.",
            "- Hydrogen/SOFC: 양산 뉴스는 Stage 2이고 고객·매출·OPM·반복 서비스가 필요.",
            "- Solar/Wind: 미국 내재화와 수주잔고는 유용하지만 통관, permit, lease halt는 Green을 막는다.",
            "- Battery safety: fatal fire, quality failure, supplier disclosure issue는 hard RedTeam이다.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round187_risk_overlay_markdown() -> str:
    lines = [
        "# Round-187 R3 Loop-12 Risk Overlays",
        "",
        "| target | hard gate | red flags |",
        "| --- | --- | --- |",
    ]
    for target in ROUND187_SCORE_TARGETS:
        lines.append(f"| `{target.target_id}` | {str(target.hard_gate).lower()} | {', '.join(target.red_flags)} |")
    lines.extend(
        [
            "",
            "## Hard 4C Examples",
            "",
            "- `BATTERY_CONTRACT_CANCELLATION_4C`: Ford/Freudenberg-style customer contract cancellations and expected revenue loss.",
            "- `WIND_POLICY_PERMITTING_RISK`: permit halt, lease suspension, national-security review, and project delay.",
            "- `BATTERY_SAFETY_INDUSTRIAL_ACCIDENT_OVERLAY`: fatal accident, quality failure, safety management failure, and criminal liability.",
            "- `EV_BATTERY_TRANSPARENCY_REGULATORY_OVERLAY`: supplier disclosure issue, EV fire trust context, fine, and consumer trust damage.",
            "- `DISCLOSURE_CONFIDENCE_CAP`: list-only, media-only, policy-only, factory-only, or missing utilization/OPM details cannot create Green.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round187_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-187 R3 Loop-12 Price Validation Plan",
        "",
        "R3 Loop 12 must backfill contract, cancellation, subsidy-quality, utilization, safety, and policy fields together.",
        "",
        "## Required Fields",
        "",
    ]
    lines.extend(f"- `{field}`" for field in ROUND187_PRICE_FIELDS)
    lines.extend(
        [
            "",
            "## Backfill Priorities",
            "",
            "- `lges_ess_pivot_tax_credit_stage2_case`: profit_ex_subsidy, utilization, ESS revenue, FCF, and price path.",
            "- `lges_ford_freudenberg_contract_cancellation_4c_case`: cancellation dates, expected revenue loss, MAE, and utilization impact.",
            "- `doosan_fuelcell_ceres_sofc_stage23_candidate_case`: sales, customer, recurring service, OPM, FCF, and 60D/120D MFE.",
            "- `qcells_us_localization_stage2_case`: customs clearance, normal operation, margin, FCF, and localization price path.",
            "- `aricell_battery_safety_fire_hard_4c_case`: safety resolution, regulatory clearance, and trust recovery.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round187_score_stage_price_alignment_markdown() -> str:
    lines = [
        "# Round-187 R3 Loop-12 Score / Stage / Price Alignment",
        "",
        "| case | detected stage | price path status | verdict | adjustment |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in ROUND187_SCORE_STAGE_PRICE_ALIGNMENT:
        lines.append(f"| `{row.case_id}` | {row.detected_stage} | {row.price_path_status} | {row.verdict} | {row.normalization_adjustment} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- LGES and Qcells show why Stage 2 evidence can be useful while Green remains blocked by subsidy/customs/utilization gates.",
            "- Doosan Fuel Cell is a Stage 2~3 candidate only if sales, customers, recurring service, OPM, FCF, and price path align.",
            "- Battery contract cancellations, safety accidents, and supplier disclosure issues are not noise; they are RedTeam events.",
        ]
    )
    return "\n".join(lines) + "\n"


def _round187_score_price_alignment(candidate: Round187CaseCandidate) -> str:
    if candidate.case_type in {"success_candidate", "structural_success"}:
        return "unknown"
    if candidate.case_type in {"event_premium", "4b_watch", "cyclical_success"}:
        return "price_moved_without_evidence"
    if candidate.case_type == "4c_thesis_break":
        return "false_positive_score"
    if candidate.case_type == "failed_rerating":
        return "evidence_good_but_price_failed"
    return "unknown"


def _round187_rerating_result(candidate: Round187CaseCandidate) -> str:
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
    "ROUND187_BASE_SCORE_WEIGHTS",
    "ROUND187_CASE_CANDIDATES",
    "ROUND187_DEFAULT_CASES_PATH",
    "ROUND187_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND187_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND187_PRICE_FIELDS",
    "ROUND187_SCORE_STAGE_PRICE_ALIGNMENT",
    "ROUND187_SCORE_TARGETS",
    "ROUND187_SOURCE_CANONICAL_TARGET_COUNT",
    "ROUND187_SOURCE_CANONICAL_TARGET_IDS",
    "ROUND187_STAGE_CAPS",
    "render_round187_green_guardrail_markdown",
    "render_round187_price_validation_plan_markdown",
    "render_round187_risk_overlay_markdown",
    "render_round187_score_stage_price_alignment_markdown",
    "render_round187_summary_markdown",
    "round187_base_score_weight_rows",
    "round187_case_candidate_rows",
    "round187_case_records",
    "round187_price_field_rows",
    "round187_score_profile_rows",
    "round187_score_stage_price_alignment_rows",
    "round187_stage_cap_rows",
    "round187_stage_date_rows",
    "round187_summary",
    "round187_target_for",
    "write_round187_r3_loop12_reports",
]
