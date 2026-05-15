"""Round-38 cases_v20 expansion and score-weight validation v2.3.

Round 38 separates AI server ODM/EMS, AI server accounting trust risk,
neocloud GPU rental, advanced packaging, AI semi-equipment capex, SiC power
semiconductors, optical AI networking, and hard accounting-trust overlays.
It is calibration/report material only. Production feature engineering,
scoring, staging, and RedTeam code must not import this module.
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


ROUND38_SOURCE_ROUND_PATH = "docs/round/round_38.md"
ROUND38_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round38_score_weight_v23"
ROUND38_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_v20_round38.jsonl"
ROUND38_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round38_v23.csv"


@dataclass(frozen=True)
class Round38ScoreWeightDraft:
    eps_fcf: int | str
    structural_visibility: int | str
    bottleneck_pricing: int | str
    market_mispricing: int | str
    valuation: int | str
    capital_allocation: int | str = 0
    information_confidence: int | str = 5

    def as_dict(self) -> dict[str, int | str]:
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
class Round38ScoreTarget:
    target_id: str
    large_sector: Round10LargeSector
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    validation_group: str
    score_weight: Round38ScoreWeightDraft
    stage1_signals: tuple[str, ...]
    stage2_signals: tuple[str, ...]
    stage3_conditions: tuple[str, ...]
    green_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    validation_metrics: tuple[str, ...]
    success_criteria: str
    failure_criteria: str
    normalization_point: str

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round38CaseCandidate:
    case_id: str
    target_id: str
    symbol: str
    company_name: str
    market: str
    case_type: str
    evidence_fields: tuple[str, ...]
    red_flag_fields: tuple[str, ...]
    price_alignment_hint: str
    notes: str

    @property
    def expected_group(self) -> str:
        return self.case_type


ROUND38_SCORE_TARGETS: tuple[Round38ScoreTarget, ...] = (
    Round38ScoreTarget(
        "AI_SERVER_ODM_EMS_SUPPLY_CHAIN",
        Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS,
        E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE,
        Round10ThemePosture.GREEN_POSSIBLE,
        "high_growth_ai_hardware",
        Round38ScoreWeightDraft(22, 19, 16, 14, 11, 0, 5),
        ("ai_server_rack", "gpu_asic_demand", "hyperscaler_order", "ems_odm_capacity"),
        ("ai_server_revenue_growth", "rack_shipment_growth", "op_eps_revision", "capacity_expansion"),
        ("mix_changes_company_eps", "customer_diversification", "margin_control", "valuation_frame_shift"),
        ("ai_server_revenue_growth", "rack_shipment_growth", "op_eps_revision", "gross_margin_stable"),
        ("customer_concentration", "low_margin_assembly", "inventory", "accounting_trust", "supplier_related_party"),
        ("auditor_resignation", "internal_control_weakness", "inventory_glut", "margin_collapse"),
        ("mfe_90d", "mfe_180d", "mfe_1y", "mae_90d", "gross_margin", "inventory_growth", "customer_concentration", "audit_event_drawdown"),
        "AI server revenue, OP/EPS, and rerating moving together can be aligned.",
        "Revenue growth with margin, inventory, customer, or audit trust breaks becomes 4C.",
        "AI server ODM/EMS is Green-possible, but lower margin and accounting trust risk cap confidence.",
    ),
    Round38ScoreTarget(
        "AI_SERVER_ACCOUNTING_GOVERNANCE_RISK",
        Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS,
        E2RArchetype.THEME_VALUATION_OVERHEAT,
        Round10ThemePosture.REDTEAM_FIRST,
        "hard_redteam_gate",
        Round38ScoreWeightDraft("gate", "gate", "gate", "gate", "gate", "gate", "gate"),
        ("auditor_resignation", "annual_report_delay", "internal_control_weakness", "related_party_transaction"),
        ("sec_doj_probe", "filing_delay", "financial_restatement_risk", "audit_committee_trust_break"),
        ("not_applicable_gate_only",),
        (),
        ("auditor_resignation", "annual_report_delay", "internal_control_weakness", "related_party_transaction", "sec_doj_probe"),
        ("auditor_resignation", "annual_report_delay", "internal_control_weakness", "delisting_risk"),
        ("event_day_return", "mae_5d", "mae_20d", "mae_60d", "drawdown_from_peak", "filing_recovery"),
        "Accounting trust recovery can move a case back to watch after evidence is restored.",
        "Auditor resignation, filing delay, or internal-control trust break is hard 4C until resolved.",
        "This is a RedTeam gate, not a score-weight axis.",
    ),
    Round38ScoreTarget(
        "NEOCLOUD_GPU_RENTAL",
        Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS,
        E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        "high_debt_infra",
        Round38ScoreWeightDraft(18, 21, 18, 14, 10, 0, 5),
        ("gpu_cloud_contract", "take_or_pay", "openai_microsoft_customer", "ipo_filing"),
        ("contracted_backlog", "revenue_growth", "ebitda_improvement", "gpu_deployment"),
        ("fcf_turnaround", "debt_ebitda_stabilized", "customer_diversification"),
        ("take_or_pay", "contracted_backlog", "fcf_turnaround", "customer_diversification"),
        ("debt", "customer_concentration", "gpu_obsolescence", "funding_cost", "fcf_negative"),
        ("refinancing_stress", "gpu_obsolescence", "customer_loss", "funding_cost_spike"),
        ("ipo_mfe_90d", "ipo_mae_180d", "net_debt_ebitda", "fcf_margin", "contract_duration", "customer_concentration"),
        "Revenue, EBITDA, FCF conversion, and customer diversification moving together can align.",
        "Price rise with worsening debt, FCF, or concentration is false_positive_score.",
        "Neocloud has visibility through take-or-pay, but debt and GPU depreciation keep it watch-first.",
    ),
    Round38ScoreTarget(
        "ADVANCED_PACKAGING_COWOS_EMIB",
        Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS,
        E2RArchetype.SEMI_EQUIPMENT_CAPEX,
        Round10ThemePosture.GREEN_POSSIBLE,
        "ai_packaging_bottleneck",
        Round38ScoreWeightDraft(22, 21, 20, 14, 12, 0, 5),
        ("cowos", "emib", "hbm_packaging", "ai_packaging_bottleneck"),
        ("packaging_revenue_growth", "customer_capex", "orders_or_backlog", "op_eps_revision"),
        ("multi_year_packaging_constraint", "margin_visible", "valuation_frame_shift"),
        ("packaging_revenue_growth", "orders_or_backlog", "op_eps_revision", "bottleneck_visible"),
        ("capex_cycle", "customer_concentration", "bottleneck_normalization", "yield_risk"),
        ("customer_capex_delay", "yield_problem", "bottleneck_normalization", "order_pushout"),
        ("packaging_revenue_growth", "bookings_backlog", "gross_margin", "mfe_180d", "mfe_1y", "drawdown_after_capex_peak"),
        "Packaging revenue, backlog, margins, and rerating moving together are aligned.",
        "Capacity expansion or customer capex delay that normalizes the bottleneck becomes 4B/4C.",
        "Advanced packaging is a separate AI supply-chain bottleneck, not a generic semiconductor label.",
    ),
    Round38ScoreTarget(
        "SEMI_EQUIPMENT_AI_CAPEX",
        Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS,
        E2RArchetype.SEMI_EQUIPMENT_CAPEX,
        Round10ThemePosture.GREEN_POSSIBLE,
        "ai_capex_equipment",
        Round38ScoreWeightDraft(22, 20, 18, 14, 12, 0, 5),
        ("ai_fab_capex", "hbm_capex", "advanced_packaging_capex", "equipment_order"),
        ("equipment_backlog", "guidance_raise", "eps_revision", "customer_diversification"),
        ("backlog_to_revenue", "op_leverage", "capex_cycle_risk_controlled"),
        ("equipment_backlog", "guidance_raise", "eps_revision", "backlog_to_revenue"),
        ("customer_capex", "order_delay", "export_control", "capex_peak"),
        ("order_pushout", "export_control", "customer_capex_cut", "capex_peak_unwind"),
        ("orders_backlog", "revenue_guidance", "eps_revision", "mfe_180d", "mfe_1y", "mae_after_order_slowdown"),
        "Equipment backlog converting to revenue and OP leverage is aligned.",
        "Customer capex delay, export controls, or order pushout can break the thesis.",
        "Semi equipment can be Green-possible, but remains customer-capex-cycle dependent.",
    ),
    Round38ScoreTarget(
        "POWER_SEMICONDUCTOR_SIC",
        Round10LargeSector.BATTERY_EV_GREEN,
        E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        "cycle_capex_debt",
        Round38ScoreWeightDraft(16, 13, 12, 11, 8, 0, 5),
        ("sic_demand", "ev_power_device", "solar_industrial_power", "wide_bandgap"),
        ("long_term_supply_contract", "fab_ramp", "utilization_up", "fcf_improvement"),
        ("fcf_positive", "debt_stable", "customer_diversified", "pricing_stable"),
        ("long_term_supply_contract", "utilization_up", "fcf_improvement", "debt_stable"),
        ("ev_demand", "capex_debt", "utilization", "pricing", "bankruptcy"),
        ("chapter11", "demand_warning", "utilization_drop", "cash_burn"),
        ("mfe_1y", "mfe_2y", "mae_1y", "debt_ebitda", "capex_revenue", "utilization", "gross_margin", "cash_burn"),
        "Demand, utilization, FCF, and debt stability together can support Watch-to-Green.",
        "Capex and debt rising before demand and FCF makes this a 4C candidate.",
        "SiC should not get Green from long-term narrative alone; Wolfspeed-style failure risk is central.",
    ),
    Round38ScoreTarget(
        "OPTICAL_NETWORKING_AI_DATACENTER",
        Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS,
        E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE,
        Round10ThemePosture.GREEN_POSSIBLE,
        "ai_network_bottleneck",
        Round38ScoreWeightDraft(21, 22, 20, 13, 12, 0, 5),
        ("optical_transceiver", "laser_leadtime", "pcb_leadtime", "ai_datacenter_network"),
        ("hyperscaler_contract", "lead_time_extended", "order_growth", "op_eps_revision"),
        ("multi_year_contract", "delivery_economics_visible", "concentration_controlled"),
        ("hyperscaler_contract", "lead_time_extended", "order_growth", "op_eps_revision"),
        ("hyperscaler_concentration", "valuation_crowding", "capacity_normalization", "capex_delay"),
        ("lead_time_normalization", "hyperscaler_order_cut", "capacity_normalization", "valuation_unwind"),
        ("mfe_180d", "mfe_1y", "lead_time_normalization_drawdown", "valuation_crowding", "customer_concentration"),
        "Order, lead-time, OP/EPS, and rerating evidence moving together is aligned.",
        "Capacity normalization, customer concentration, or valuation crowding can move it to 4B/4C.",
        "Optical networking remains Green-possible when AI data-center order evidence is explicit.",
    ),
    Round38ScoreTarget(
        "REDTEAM_ACCOUNTING_TRUST_OVERLAY",
        Round10LargeSector.POLICY_GEOPOLITICAL_EVENT,
        E2RArchetype.THEME_VALUATION_OVERHEAT,
        Round10ThemePosture.REDTEAM_FIRST,
        "hard_redteam_gate",
        Round38ScoreWeightDraft("gate", "gate", "gate", "gate", "gate", "gate", "gate"),
        ("auditor_resignation", "annual_report_delay", "internal_control_weakness", "sec_doj_probe"),
        ("redteam_hard_finding", "stage_green_block", "price_path_priority"),
        ("not_applicable_gate_only",),
        (),
        ("auditor_resignation", "annual_report_delay", "internal_control_weakness", "sec_doj_probe", "related_party_transaction"),
        ("auditor_resignation", "delisting_risk", "financial_restatement", "trust_break"),
        ("event_day_return", "mae_5d", "mae_20d", "mae_60d", "drawdown_from_peak", "recovery_after_filing"),
        "The only success condition is verified trust restoration; otherwise Green remains blocked.",
        "Hard accounting trust events immediately block Stage 3-Green and trigger RedTeam review.",
        "This overlay is a hard gate for all high-growth AI hardware and infrastructure cases.",
    ),
)


ROUND38_CASE_CANDIDATES: tuple[Round38CaseCandidate, ...] = (
    Round38CaseCandidate("foxconn_ai_server_profit_rack_growth_candidate", "AI_SERVER_ODM_EMS_SUPPLY_CHAIN", "2354.TW", "Foxconn AI server profit rack growth candidate", "TW", "success_candidate", ("ai_server_revenue_growth", "rack_shipment_growth", "capacity_expansion"), ("customer_concentration", "low_margin_assembly"), "needs_backfill", "AI server demand and rack growth are strong but price rerating needs OHLCV validation."),
    Round38CaseCandidate("foxconn_ai_server_price_alignment_needs_backfill", "AI_SERVER_ODM_EMS_SUPPLY_CHAIN", "2354.TW_ALIGN", "Foxconn AI server price alignment needs backfill", "TW", "success_candidate", ("op_eps_revision", "ai_server_revenue_growth"), ("market_underperformance", "customer_concentration"), "needs_backfill", "Earnings evidence appears stronger than price evidence, so path validation remains open."),
    Round38CaseCandidate("supermicro_ai_server_rerating_then_accounting_4c", "AI_SERVER_ODM_EMS_SUPPLY_CHAIN", "SMCI_4C", "Supermicro AI server rerating then accounting 4C", "US", "4c_thesis_break", ("ai_server_revenue_growth", "valuation_frame_shift"), ("auditor_resignation", "internal_control_weakness", "accounting_trust"), "thesis_break", "AI server rerating followed by audit trust break is a core 4C example."),
    Round38CaseCandidate("ai_server_low_margin_customer_concentration_counterexample", "AI_SERVER_ODM_EMS_SUPPLY_CHAIN", "AI_SERVER_MARGIN", "AI server low margin customer concentration counterexample", "GLOBAL", "failed_rerating", ("ai_server_revenue_growth",), ("low_margin_assembly", "customer_concentration", "inventory"), "false_positive_score", "Revenue growth without margin and customer diversification should be capped."),
    Round38CaseCandidate("supermicro_ey_resignation_hard_4c", "AI_SERVER_ACCOUNTING_GOVERNANCE_RISK", "SMCI_EY_4C", "Supermicro EY resignation hard 4C", "US", "4c_thesis_break", ("auditor_resignation",), ("auditor_resignation", "audit_committee_trust_break"), "thesis_break", "Auditor resignation is a hard trust break regardless of growth."),
    Round38CaseCandidate("supermicro_hindenburg_delay_annual_report_4c", "AI_SERVER_ACCOUNTING_GOVERNANCE_RISK", "SMCI_DELAY_4C", "Supermicro Hindenburg delay annual report 4C", "US", "4c_thesis_break", ("annual_report_delay", "related_party_transaction"), ("annual_report_delay", "financial_restatement_risk"), "thesis_break", "Filing delay and short-report accounting flags require hard RedTeam review."),
    Round38CaseCandidate("related_party_supplier_risk_counterexample", "AI_SERVER_ACCOUNTING_GOVERNANCE_RISK", "RELATED_PARTY", "Related-party supplier risk counterexample", "GLOBAL", "failed_rerating", ("related_party_transaction",), ("supplier_related_party", "accounting_trust"), "false_positive_score", "Related-party supplier risk can invalidate high growth quality."),
    Round38CaseCandidate("auditor_resignation_redteam_overlay", "AI_SERVER_ACCOUNTING_GOVERNANCE_RISK", "AUDITOR_GATE", "Auditor resignation RedTeam overlay", "GLOBAL", "4c_thesis_break", ("auditor_resignation", "redteam_hard_finding"), ("auditor_resignation", "stage_green_block"), "thesis_break", "This is a gate case, not a score-weight case."),
    Round38CaseCandidate("coreweave_take_or_pay_contract_candidate", "NEOCLOUD_GPU_RENTAL", "CRWV_TAKEPAY", "CoreWeave take-or-pay contract candidate", "US", "success_candidate", ("take_or_pay", "contracted_backlog", "gpu_deployment"), ("debt", "customer_concentration"), "needs_backfill", "Take-or-pay creates visibility but debt and concentration keep it watch-first."),
    Round38CaseCandidate("coreweave_ipo_below_range_price_path_watch", "NEOCLOUD_GPU_RENTAL", "CRWV_IPO_WATCH", "CoreWeave IPO below range price path watch", "US", "event_premium", ("ipo_filing", "gpu_cloud_contract"), ("funding_cost", "ipo_volatility"), "price_moved_without_evidence", "IPO pricing and volatility are not proof of durable rerating."),
    Round38CaseCandidate("coreweave_high_debt_customer_concentration_counterexample", "NEOCLOUD_GPU_RENTAL", "CRWV_DEBT", "CoreWeave high debt customer concentration counterexample", "US", "failed_rerating", ("revenue_growth",), ("debt", "customer_concentration", "fcf_negative"), "false_positive_score", "Debt and customer concentration can offset revenue visibility."),
    Round38CaseCandidate("gpu_obsolescence_funding_cost_4c", "NEOCLOUD_GPU_RENTAL", "GPU_OBS_4C", "GPU obsolescence funding cost 4C", "GLOBAL", "4c_thesis_break", ("gpu_deployment",), ("gpu_obsolescence", "funding_cost_spike", "refinancing_stress"), "thesis_break", "GPU generation changes and funding cost can break the neocloud model."),
    Round38CaseCandidate("nvidia_cowos_l_packaging_bottleneck_candidate", "ADVANCED_PACKAGING_COWOS_EMIB", "NVDA_COWOS", "Nvidia CoWoS-L packaging bottleneck candidate", "US", "success_candidate", ("cowos", "hbm_packaging", "ai_packaging_bottleneck"), ("bottleneck_normalization", "customer_concentration"), "needs_backfill", "CoWoS-L demand shows packaging bottleneck, but supplier exposure must be validated."),
    Round38CaseCandidate("applied_materials_packaging_growth_candidate", "ADVANCED_PACKAGING_COWOS_EMIB", "AMAT_PACK", "Applied Materials packaging growth candidate", "US", "success_candidate", ("packaging_revenue_growth", "op_eps_revision"), ("capex_cycle", "customer_capex_delay"), "needs_backfill", "Packaging revenue growth can validate AI packaging bottleneck exposure."),
    Round38CaseCandidate("packaging_bottleneck_normalization_4b", "ADVANCED_PACKAGING_COWOS_EMIB", "PACK_NORM_4B", "Packaging bottleneck normalization 4B", "GLOBAL", "4b_watch", ("ai_packaging_bottleneck",), ("bottleneck_normalization", "valuation_unwind"), "unknown", "Capacity expansion can turn a bottleneck winner into 4B-watch."),
    Round38CaseCandidate("customer_capex_delay_packaging_4c", "ADVANCED_PACKAGING_COWOS_EMIB", "PACK_CAPEX_4C", "Customer capex delay packaging 4C", "GLOBAL", "4c_thesis_break", ("customer_capex",), ("customer_capex_delay", "order_pushout"), "thesis_break", "Customer capex delay can break packaging order conversion."),
    Round38CaseCandidate("applied_materials_ai_capex_guidance_candidate", "SEMI_EQUIPMENT_AI_CAPEX", "AMAT_CAPEX", "Applied Materials AI capex guidance candidate", "US", "success_candidate", ("ai_fab_capex", "guidance_raise", "eps_revision"), ("customer_capex", "export_control"), "needs_backfill", "AI capex guidance must be validated through order and EPS path."),
    Round38CaseCandidate("equipment_order_backlog_success_candidate", "SEMI_EQUIPMENT_AI_CAPEX", "EQUIP_BACKLOG", "Equipment order backlog success candidate", "GLOBAL", "success_candidate", ("equipment_backlog", "backlog_to_revenue"), ("order_delay", "customer_capex"), "needs_backfill", "Backlog-to-revenue conversion is the core equipment success path."),
    Round38CaseCandidate("capex_peak_equipment_4c", "SEMI_EQUIPMENT_AI_CAPEX", "EQUIP_PEAK_4C", "Capex peak equipment 4C", "GLOBAL", "4c_thesis_break", ("advanced_packaging_capex",), ("capex_peak", "customer_capex_cut"), "thesis_break", "Capex peak can break equipment rerating."),
    Round38CaseCandidate("export_control_equipment_counterexample", "SEMI_EQUIPMENT_AI_CAPEX", "EQUIP_EXPORT", "Export control equipment counterexample", "GLOBAL", "failed_rerating", ("equipment_order",), ("export_control", "order_pushout"), "false_positive_score", "Export controls can block order conversion despite demand."),
    Round38CaseCandidate("wolfspeed_chapter11_restructuring_4c", "POWER_SEMICONDUCTOR_SIC", "WOLF_CH11", "Wolfspeed Chapter 11 restructuring 4C", "US", "4c_thesis_break", ("sic_demand",), ("chapter11", "capex_debt", "cash_burn"), "thesis_break", "Chapter 11 is a hard counterexample to narrative-only SiC Green."),
    Round38CaseCandidate("wolfspeed_stock_92pct_decline_counterexample", "POWER_SEMICONDUCTOR_SIC", "WOLF_DD", "Wolfspeed stock 92pct decline counterexample", "US", "failed_rerating", ("wide_bandgap",), ("demand_warning", "capex_debt"), "false_positive_score", "Long-term SiC narrative failed when demand, debt, and capex did not align."),
    Round38CaseCandidate("sic_low_utilization_counterexample", "POWER_SEMICONDUCTOR_SIC", "SIC_UTIL", "SiC low utilization counterexample", "GLOBAL", "failed_rerating", ("fab_ramp",), ("utilization_drop", "cash_burn"), "false_positive_score", "Fab ramp without utilization and FCF should be capped."),
    Round38CaseCandidate("sic_long_term_contract_success_candidate_if_fcf", "POWER_SEMICONDUCTOR_SIC", "SIC_CONTRACT", "SiC long-term contract success candidate if FCF", "GLOBAL", "success_candidate", ("long_term_supply_contract", "fcf_improvement"), ("ev_demand", "pricing"), "needs_backfill", "SiC can improve only if long-term contract evidence converts into FCF."),
    Round38CaseCandidate("broadcom_optical_pcb_leadtime_bottleneck_candidate", "OPTICAL_NETWORKING_AI_DATACENTER", "AVGO_OPTICAL", "Broadcom optical PCB leadtime bottleneck candidate", "US", "success_candidate", ("laser_leadtime", "pcb_leadtime", "ai_datacenter_network"), ("capacity_normalization", "hyperscaler_concentration"), "needs_backfill", "Optical/PCB lead time can be a real AI data-center bottleneck."),
    Round38CaseCandidate("optical_networking_capacity_normalization_4b", "OPTICAL_NETWORKING_AI_DATACENTER", "OPTICAL_NORM_4B", "Optical networking capacity normalization 4B", "GLOBAL", "4b_watch", ("lead_time_extended",), ("capacity_normalization", "valuation_crowding"), "unknown", "Lead-time normalization is a 4B-watch signal."),
    Round38CaseCandidate("optical_hyperscaler_customer_concentration_counterexample", "OPTICAL_NETWORKING_AI_DATACENTER", "OPTICAL_CONC", "Optical hyperscaler customer concentration counterexample", "GLOBAL", "failed_rerating", ("hyperscaler_contract",), ("hyperscaler_concentration", "customer_loss"), "false_positive_score", "Hyperscaler concentration can offset bottleneck quality."),
    Round38CaseCandidate("optical_theme_no_order_counterexample", "OPTICAL_NETWORKING_AI_DATACENTER", "OPTICAL_THEME", "Optical theme no order counterexample", "GLOBAL", "failed_rerating", ("optical_transceiver",), ("unclear_ai_dc_exposure", "theme_only"), "price_moved_without_evidence", "Optical theme without order evidence is not score evidence."),
)


def target_for(target_id: str) -> Round38ScoreTarget | None:
    for target in ROUND38_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round38_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND38_CASE_CANDIDATES:
        target = target_for(candidate.target_id)
        if target is None:
            raise ValueError(f"unknown target_id: {candidate.target_id}")
        weights = target.score_weight.as_dict()
        numeric_weights = {
            "eps_fcf": _float_weight(weights["eps_fcf"]),
            "visibility": _float_weight(weights["structural_visibility"]),
            "bottleneck": _float_weight(weights["bottleneck_pricing"]),
            "mispricing": _float_weight(weights["market_mispricing"]),
            "valuation": _float_weight(weights["valuation"]),
            "capital_allocation": _float_weight(weights["capital_allocation"]),
            "information_confidence": _float_weight(weights["information_confidence"]),
        }
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
                f"Round38 v2.3 calibration candidate for {candidate.target_id}; "
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
            score_price_alignment=candidate.price_alignment_hint if candidate.price_alignment_hint in {"unknown", "aligned", "false_positive_score", "missed_due_to_score", "price_moved_without_evidence", "evidence_good_but_price_failed"} else "unknown",
            rerating_result="thesis_break" if candidate.case_type == "4c_thesis_break" else "unknown",
            price_pattern="unknown",
            score_weight_hint=numeric_weights,
            green_guardrails=(
                "do_not_use_case_as_candidate_input",
                "do_not_change_production_scoring",
                "require_price_path_validation",
                "require_cross_evidence_for_green",
                "theme_label_is_not_score_evidence",
                "do_not_invent_margins_backlog_contracts_or_prices",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Validation group: {target.validation_group}.",
            price_validation=PriceValidation(price_validation_status="needs_price_backfill"),
            data_quality=CaseDataQuality(False, False, False, 0.0),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round38_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND38_SCORE_TARGETS:
        weights = target.score_weight.as_dict()
        rows.append(
            {
                "target_id": target.target_id,
                "large_sector": target.large_sector.value,
                "canonical_archetype": target.canonical_archetype.value,
                "posture": target.posture.value,
                "validation_group": target.validation_group,
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
                "validation_metrics": "|".join(target.validation_metrics),
                "success_criteria": target.success_criteria,
                "failure_criteria": target.failure_criteria,
                "production_scoring_changed": str(target.production_scoring_changed).lower(),
                "normalization_point": target.normalization_point,
            }
        )
    return tuple(rows)


def round38_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND38_CASE_CANDIDATES:
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
                "validation_group": target.validation_group,
                "evidence_fields": "|".join(candidate.evidence_fields),
                "red_flag_fields": "|".join(candidate.red_flag_fields),
                "price_alignment_hint": candidate.price_alignment_hint,
                "price_validation_status": "needs_price_backfill",
                "production_input": "false",
                "notes": candidate.notes,
            }
        )
    return tuple(rows)


def round38_summary() -> dict[str, int | bool]:
    records = round38_case_records()
    positive = sum(1 for record in records if record.case_type in {"success_candidate", "structural_success", "cyclical_success"})
    stage4c = sum(1 for record in records if record.case_type == "4c_thesis_break")
    stage4b = sum(1 for record in records if record.case_type == "4b_watch")
    return {
        "target_count": len(ROUND38_SCORE_TARGETS),
        "case_candidate_count": len(records),
        "success_candidate_count": positive,
        "counterexample_or_risk_count": len(records) - positive,
        "stage4b_case_count": stage4b,
        "stage4c_case_count": stage4c,
        "green_possible_count": sum(1 for target in ROUND38_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND38_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND38_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round38_score_weight_reports(
    *,
    output_directory: str | Path = ROUND38_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND38_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND38_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round38_score_weight_v23_summary.md",
        "case_matrix": output / "round38_case_candidate_matrix.csv",
        "green_guardrails": output / "round38_green_guardrail_review.md",
        "validation_plan": output / "round38_archetype_price_validation_plan.md",
        "ai_server": output / "round38_ai_server_risk_review.md",
        "neocloud_packaging": output / "round38_neocloud_packaging_review.md",
        "accounting_overlay": output / "round38_accounting_trust_overlay_review.md",
    }
    _write_case_jsonl(round38_case_records(), cases)
    _write_rows(round38_score_profile_rows(), score_profiles)
    _write_rows(round38_case_candidate_rows(), paths["case_matrix"])
    paths["summary"].write_text(render_round38_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round38_green_guardrail_markdown(), encoding="utf-8")
    paths["validation_plan"].write_text(render_round38_validation_plan_markdown(), encoding="utf-8")
    paths["ai_server"].write_text(render_round38_ai_server_markdown(), encoding="utf-8")
    paths["neocloud_packaging"].write_text(render_round38_neocloud_packaging_markdown(), encoding="utf-8")
    paths["accounting_overlay"].write_text(render_round38_accounting_overlay_markdown(), encoding="utf-8")
    return paths


def render_round38_summary_markdown() -> str:
    summary = round38_summary()
    lines = [
        "# Round-38 Score-Weight Validation v2.3 Summary",
        "",
        f"- source_round: `{ROUND38_SOURCE_ROUND_PATH}`",
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
        "- Round 38 adds cases_v20 and v2.3 price-path validation plans.",
        "- Example: AI server ODM/EMS can be Green-possible, but low margin, inventory, customer concentration, and audit risk cap it.",
        "- Example: neocloud has take-or-pay visibility, but high debt and GPU depreciation keep it watch-first.",
        "- Example: Supermicro-style auditor resignation is a hard RedTeam 4C gate, not a score-weight adjustment.",
        "- Theme names, case IDs, revenue growth headlines, and price spikes are not score evidence by themselves.",
    ]
    return "\n".join(lines) + "\n"


def render_round38_green_guardrail_markdown() -> str:
    lines = [
        "# Round-38 Green Guardrail Review",
        "",
        "| target | posture | validation_group | Green unlock evidence | Red flags |",
        "|---|---|---|---|---|",
    ]
    for target in ROUND38_SCORE_TARGETS:
        lines.append(
            "| "
            f"{target.target_id} | {target.posture.value} | {target.validation_group} | "
            f"{', '.join(target.green_conditions) or 'gate-only'} | {', '.join(target.red_flags)} |"
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "- Do not apply v2.3 weights to production scoring yet.",
            "- Do not use case IDs, AI labels, revenue headlines, IPO narratives, or price spikes as candidate-generation input.",
            "- Do not invent margins, contract terms, customer concentration, debt metrics, FCF, stage dates, or prices.",
            "- Do not treat accounting-trust hard flags as ordinary score penalties; they are RedTeam gates.",
            "- Do not lower Stage 3-Green thresholds to improve recall.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round38_validation_plan_markdown() -> str:
    lines = [
        "# Round-38 Archetype Price Validation Plan",
        "",
        "Round 38 strengthens price-path validation for AI hardware, high-debt AI infra, advanced packaging, SiC, and accounting hard gates.",
        "",
        "| target | validation_group | metrics | success | failure |",
        "|---|---|---|---|---|",
    ]
    for target in ROUND38_SCORE_TARGETS:
        lines.append(
            "| "
            f"{target.target_id} | {target.validation_group} | {', '.join(target.validation_metrics)} | "
            f"{target.success_criteria} | {target.failure_criteria} |"
        )
    lines.extend(
        [
            "",
            "## Group Rules",
            "- high_growth_ai_hardware: validate revenue-to-OP/EPS conversion, margin, inventory, customer concentration, and audit-event drawdown.",
            "- high_debt_infra: validate debt/EBITDA, FCF margin, contract duration, customer concentration, refinancing drawdown, and GPU depreciation cycle.",
            "- ai_packaging_bottleneck/ai_capex_equipment/ai_network_bottleneck: validate order, backlog, OP/EPS revision, lead time, and capex-cycle drawdown.",
            "- cycle_capex_debt: classify as Watch-to-Green only when utilization, FCF, and debt stability are explicit.",
            "- hard_redteam_gate: auditor resignation, filing delay, internal-control weakness, or SEC/DOJ probe blocks Green before scoring.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round38_ai_server_markdown() -> str:
    return "\n".join(
        [
            "# Round-38 AI Server ODM/EMS Risk Review",
            "",
            "AI server ODM/EMS is not the same as HBM or grid power equipment.",
            "",
            "## Green-possible evidence",
            "- AI server rack shipments, OP/EPS revision, production capacity, and margin stability must appear together.",
            "- Customer diversification and inventory discipline are required for higher conviction.",
            "",
            "## RedTeam risks",
            "- Supermicro-style auditor resignation, annual-report delay, related-party supplier risk, or internal-control weakness is hard 4C.",
            "- Low-margin assembly and customer concentration can turn revenue growth into false_positive_score.",
        ]
    ) + "\n"


def render_round38_neocloud_packaging_markdown() -> str:
    return "\n".join(
        [
            "# Round-38 Neocloud / Packaging / Optical Review",
            "",
            "Round 38 splits AI infrastructure into different economic models.",
            "",
            "## Neocloud",
            "- Take-or-pay contracts can improve visibility.",
            "- Debt, FCF-negative growth, customer concentration, and GPU obsolescence keep it watch-first.",
            "",
            "## Advanced Packaging and Semi Equipment",
            "- CoWoS/EMIB and AI capex can support Green-possible cases when order, backlog, revenue, and OP/EPS conversion are explicit.",
            "- CAPA expansion, customer capex delay, and export controls are 4B/4C gates.",
            "",
            "## Optical Networking",
            "- Optical/laser/PCB lead-time bottlenecks can be real AI data-center evidence.",
            "- Lead-time normalization and hyperscaler concentration must be price-path tested.",
        ]
    ) + "\n"


def render_round38_accounting_overlay_markdown() -> str:
    return "\n".join(
        [
            "# Round-38 Accounting Trust Overlay",
            "",
            "This overlay is a hard RedTeam gate, not a score-weight axis.",
            "",
            "## Hard 4C triggers",
            "- auditor_resignation",
            "- annual_report_delay",
            "- internal_control_weakness",
            "- related_party_transaction",
            "- SEC/DOJ probe",
            "- financial restatement or delisting risk",
            "",
            "## Stage handling",
            "- Stage 3-Green is immediately blocked when a hard accounting-trust flag appears.",
            "- Existing Stage 3 cases require RedTeam review and short-window price-path validation.",
            "- Recovery requires verified filing and trust restoration evidence; growth headlines alone are not enough.",
        ]
    ) + "\n"


def _float_weight(value: int | str) -> float:
    if isinstance(value, str):
        return 0.0
    return float(value)


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
    "ROUND38_CASE_CANDIDATES",
    "ROUND38_DEFAULT_CASES_PATH",
    "ROUND38_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND38_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND38_SCORE_TARGETS",
    "ROUND38_SOURCE_ROUND_PATH",
    "Round38CaseCandidate",
    "Round38ScoreTarget",
    "Round38ScoreWeightDraft",
    "render_round38_accounting_overlay_markdown",
    "render_round38_ai_server_markdown",
    "render_round38_green_guardrail_markdown",
    "render_round38_neocloud_packaging_markdown",
    "render_round38_summary_markdown",
    "render_round38_validation_plan_markdown",
    "round38_case_candidate_rows",
    "round38_case_records",
    "round38_score_profile_rows",
    "round38_summary",
    "target_for",
    "write_round38_score_weight_reports",
]
