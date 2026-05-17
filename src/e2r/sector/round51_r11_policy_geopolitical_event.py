"""Round-51 R11 policy, geopolitical, disaster, and event pack.

Round 51 turns R11 into an event-risk calibration pack. The core rule is
simple: a policy headline, outbreak, disaster, summit, reconstruction slogan,
or scientific preprint can create Stage 1 attention, but it cannot create
Stage 3-Green by itself. Contract, budget, government order, recurring demand,
or EPS/FCF conversion must be source-backed first.

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


ROUND51_SOURCE_ROUND_PATH = "docs/round/round_51.md"
ROUND51_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round51_r11_policy_geopolitical_event"
ROUND51_DEFAULT_CASES_PATH = "data/e2r_case_library/cases_r11_round51.jsonl"
ROUND51_DEFAULT_SCORE_PROFILE_PATH = "data/sector_taxonomy/score_weight_profiles_round51_r11_v1.csv"


@dataclass(frozen=True)
class Round51ScoreWeightDraft:
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
class Round51ScoreTarget:
    target_id: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round51ScoreWeightDraft
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
        return Round10LargeSector.POLICY_GEOPOLITICAL_EVENT

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round51CaseCandidate:
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


ROUND51_SCORE_TARGETS: tuple[Round51ScoreTarget, ...] = (
    Round51ScoreTarget(
        "NORTH_KOREA_POLICY_EVENT",
        E2RArchetype.NORTH_KOREA_POLICY_EVENT,
        Round10ThemePosture.REDTEAM_FIRST,
        Round51ScoreWeightDraft(5, 5, 5, 8, 5, 0, 3),
        ("summit_or_dialogue", "tourism_reopening_headline", "inter_korea_infra_theme"),
        ("sanctions_relief", "binding_policy", "funded_project", "revenue_visibility"),
        ("cash_flow_project", "multi_year_contract", "low_sanctions_risk"),
        ("summit_expectation_rally", "policy_theme_basket_crowding"),
        ("military_tension", "facility_dismantle", "road_rail_destroyed", "sanctions_intact"),
        ("sanctions_relief", "funded_project", "cash_flow_project", "revenue_visibility"),
        ("sanctions", "military_tension", "facility_dismantle", "policy_reversal"),
        "Inter-Korea headlines remain RedTeam-first until binding revenue and sanctions relief exist.",
    ),
    Round51ScoreTarget(
        "GEOPOLITICAL_RECONSTRUCTION",
        E2RArchetype.GEOPOLITICAL_RECONSTRUCTION,
        Round10ThemePosture.REDTEAM_FIRST,
        Round51ScoreWeightDraft(12, 10, 8, 10, 8, 0, 4),
        ("reconstruction_conference", "mou_or_policy_declaration", "post_war_infra_theme"),
        ("actual_project", "project_financing", "participating_company", "construction_started"),
        ("multi_year_revenue", "supplier_margin", "funded_backlog", "delivery_schedule"),
        ("reconstruction_basket_rally_before_contract", "headline_project_priced"),
        ("war_escalation", "financing_failure", "insurance_delay", "project_start_delay"),
        ("actual_project", "project_financing", "company_contract", "margin_visibility"),
        ("mou_only", "financing_missing", "geopolitical_setback", "project_delay"),
        "Reconstruction needs funded projects and company-level contract economics, not slogans.",
    ),
    Round51ScoreTarget(
        "DISASTER_REBUILD_EVENT",
        E2RArchetype.DISASTER_REBUILD_EVENT,
        Round10ThemePosture.REDTEAM_FIRST,
        Round51ScoreWeightDraft(10, 6, 7, 8, 6, 0, 4),
        ("earthquake_rebuild", "wildfire_rebuild", "flood_or_typhoon_rebuild"),
        ("rebuild_order", "insurance_or_budget_approved", "sell_through", "margin_visibility"),
        ("repeat_rebuild_demand", "fcf_after_event", "multi_period_orders"),
        ("disaster_theme_rally", "material_basket_crowding"),
        ("one_off_rebuild_fade", "insurance_delay", "budget_delay", "inventory_build"),
        ("rebuild_order", "budget_approved", "margin_visibility", "repeat_demand"),
        ("one_off_demand", "budget_delay", "insurance_delay", "inventory"),
        "Disaster rebuilding is an event unless orders, budget, and margins repeat.",
    ),
    Round51ScoreTarget(
        "CLIMATE_DISASTER_EVENT",
        E2RArchetype.CLIMATE_DISASTER_EVENT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round51ScoreWeightDraft(12, 12, 10, 10, 8, 0, 5),
        ("heatwave", "cooling_demand", "grid_stress", "air_quality_event"),
        ("product_sales", "grid_investment", "cooling_order", "repeat_weather_demand"),
        ("structural_grid_capex", "recurring_cooling_demand", "op_eps_conversion"),
        ("seasonal_weather_theme_rally", "cooling_theme_crowded"),
        ("weather_normalization", "inventory_build", "demand_fade", "margin_reversal"),
        ("repeat_demand", "grid_capex", "sales_or_order", "margin_visibility"),
        ("seasonality", "weather_fade", "inventory", "no_sales_conversion"),
        "Weather events can route to grid/cooling sectors, but weather itself is not Green evidence.",
    ),
    Round51ScoreTarget(
        "EVENT_DISEASE_PEST_DEMAND",
        E2RArchetype.EVENT_DISEASE_PEST_DEMAND,
        Round10ThemePosture.REDTEAM_FIRST,
        Round51ScoreWeightDraft(12, 8, 8, 8, 6, 0, 5),
        ("outbreak_alert", "who_emergency", "pest_demand_spike", "stockpile_headline"),
        ("government_order", "stockpile_contract", "guide_up", "dose_or_amount_disclosed"),
        ("recurring_procurement", "non_event_demand", "ebitda_margin_visible"),
        ("outbreak_news_rally", "vaccine_or_pest_basket_crowding"),
        ("outbreak_normalization", "government_purchase_end", "inventory_build", "demand_cliff"),
        ("government_order", "stockpile_contract", "guide_up", "recurring_procurement"),
        ("one_off_outbreak", "demand_normalization", "purchase_end", "inventory"),
        "Outbreak/pest demand is event premium unless government orders or recurring demand are verified.",
    ),
    Round51ScoreTarget(
        "DIAGNOSTICS_INFECTIOUS_EVENT",
        E2RArchetype.DIAGNOSTICS_INFECTIOUS_EVENT,
        Round10ThemePosture.REDTEAM_FIRST,
        Round51ScoreWeightDraft(20, 5, 5, 5, 5, 0, 5),
        ("diagnostic_test_demand", "pandemic_or_outbreak_testing", "test_kit_order"),
        ("diagnostic_revenue_after_event", "recurring_non_event_demand", "margin_normalization"),
        ("durable_testing_market", "non_event_revenue_base", "fcf_conversion"),
        ("test_kit_rally_after_case_counts", "diagnostic_margin_extrapolated"),
        ("testing_demand_wane", "diagnostic_sales_decline", "guide_down", "inventory_writeoff"),
        ("non_event_revenue", "recurring_testing_demand", "margin_normalization", "fcf_conversion"),
        ("covid_like_one_off", "sales_decline", "guide_down", "inventory"),
        "Diagnostics can show EPS spikes, but one-off testing demand should not become structural Green.",
    ),
    Round51ScoreTarget(
        "SPECULATIVE_SCIENCE_THEME",
        E2RArchetype.SPECULATIVE_SCIENCE_THEME,
        Round10ThemePosture.REDTEAM_FIRST,
        Round51ScoreWeightDraft(5, 5, 5, 5, 5, 0, 3),
        ("preprint", "lab_claim", "sns_video", "paper_keyword"),
        ("replication_success", "customer_testing", "commercial_product", "contract_or_revenue"),
        ("commercial_revenue", "repeat_customer", "eps_fcf_conversion"),
        ("preprint_sns_rally", "retail_theme_crowding"),
        ("replication_failure", "impurity_explanation", "peer_review_failure", "trading_warning"),
        ("replication_success", "commercial_product", "customer_contract", "revenue"),
        ("replication_failure", "no_commercial_product", "preprint_only", "sns_only"),
        "Speculative science is Green-blocked until commercialization and revenue are real.",
    ),
    Round51ScoreTarget(
        "ADVANCED_MATERIAL_SPECULATIVE_THEME",
        E2RArchetype.ADVANCED_MATERIAL_SPECULATIVE_THEME,
        Round10ThemePosture.REDTEAM_FIRST,
        Round51ScoreWeightDraft(7, 6, 6, 8, 6, 0, 3),
        ("mxene_or_graphene_claim", "quantum_material_news", "advanced_material_theme"),
        ("technical_validation", "pilot_customer", "supply_contract", "revenue_conversion"),
        ("repeat_order", "commercial_scale", "margin_visibility"),
        ("advanced_material_theme_crowding", "paper_to_price_gap"),
        ("validation_failure", "no_customer", "no_revenue", "dilution_or_funding_need"),
        ("technical_validation", "pilot_customer", "revenue_conversion", "margin_visibility"),
        ("paper_only", "no_customer", "no_revenue", "funding_need"),
        "Advanced materials need customer or revenue validation before Watch can become scoring evidence.",
    ),
    Round51ScoreTarget(
        "POLICY_LOCAL_THEME",
        E2RArchetype.POLICY_LOCAL_THEME,
        Round10ThemePosture.REDTEAM_FIRST,
        Round51ScoreWeightDraft(5, 5, 5, 8, 5, 0, 3),
        ("local_policy_headline", "administrative_capital_theme", "regional_currency_policy"),
        ("budget_approved", "contract_awarded", "construction_started", "revenue_visibility"),
        ("repeat_project_revenue", "margin_visibility", "fcf_conversion"),
        ("local_policy_theme_rally", "election_policy_crowding"),
        ("policy_reversal", "budget_cut", "project_delay", "no_company_exposure"),
        ("budget_approved", "contract_awarded", "revenue_visibility", "margin_visibility"),
        ("budget_missing", "policy_reversal", "project_delay", "no_exposure"),
        "Local policy themes need budget and revenue; policy labels alone are search routing only.",
    ),
    Round51ScoreTarget(
        "ONE_OFF_EVENT_DEMAND",
        E2RArchetype.ONE_OFF_EVENT_DEMAND,
        Round10ThemePosture.REDTEAM_FIRST,
        Round51ScoreWeightDraft(8, 5, 5, 6, 5, 0, 4),
        ("temporary_shortage", "event_demand_spike", "emergency_purchase"),
        ("short_term_order", "reported_revenue_spike", "margin_visible"),
        ("recurrence_proven", "post_event_revenue_base", "fcf_conversion"),
        ("event_demand_extrapolated", "peak_margin_crowding"),
        ("demand_normalization", "one_off_purchase_end", "asp_or_margin_drop"),
        ("recurrence_proven", "post_event_revenue_base", "fcf_conversion"),
        ("one_off_risk", "normalization", "purchase_end", "margin_reversal"),
        "One-off event demand should usually be Yellow/Red, not Green.",
    ),
    Round51ScoreTarget(
        "THEME_VALUATION_OVERHEAT",
        E2RArchetype.THEME_VALUATION_OVERHEAT,
        Round10ThemePosture.REDTEAM_FIRST,
        Round51ScoreWeightDraft(0, 0, 0, 0, 0, 0, 0),
        ("price_only_rally", "theme_keyword_spike", "retail_crowding"),
        ("real_estimate_or_contract_needed",),
        ("normally_blocked_without_eps_fcf",),
        ("valuation_saturation", "price_blowoff", "crowded_reports"),
        ("estimate_cut", "accounting_or_trust_issue", "dilution", "theme_unwind"),
        ("cross_evidence", "eps_fcf_path", "redteam_low"),
        ("price_only", "crowding", "no_cash_flow", "dilution"),
        "This is a RedTeam overlay. It gates unsafe Green rather than adding positive score.",
    ),
)


ROUND51_CASE_CANDIDATES: tuple[Round51CaseCandidate, ...] = (
    Round51CaseCandidate(
        "bavarian_nordic_us_stockpile_contract_case",
        "EVENT_DISEASE_PEST_DEMAND",
        "BAVA.CO",
        "Bavarian Nordic U.S. stockpile contract",
        "EU",
        "success_candidate",
        date(2026, 5, 11),
        date(2026, 5, 11),
        None,
        None,
        None,
        ("government_order", "stockpile_contract", "guide_up", "ebitda_margin_visible"),
        ("one_off_outbreak", "government_purchase_end", "demand_normalization"),
        "event_to_contract_stockpile_candidate",
        "needs_price_backfill",
        ("Round51 analyst matrix",),
        "A government stockpile contract can move an outbreak case to Stage 2, but not structural Green by itself.",
    ),
    Round51CaseCandidate(
        "bavarian_nordic_mpox_emergency_case",
        "EVENT_DISEASE_PEST_DEMAND",
        "BAVA.CO",
        "Bavarian Nordic mpox emergency rally",
        "EU",
        "event_premium",
        date(2024, 8, 15),
        None,
        None,
        date(2024, 8, 16),
        None,
        ("who_emergency", "outbreak_alert", "vaccine_theme_rally"),
        ("one_off_outbreak", "purchase_unverified", "demand_normalization"),
        "outbreak_price_move_before_recurring_evidence",
        "needs_price_backfill",
        ("Round51 analyst matrix",),
        "Emergency demand can create fast price movement; recurring procurement must be checked before escalation.",
    ),
    Round51CaseCandidate(
        "ukraine_swiss_reconstruction_projects_case",
        "GEOPOLITICAL_RECONSTRUCTION",
        "UKRAINE_REBUILD_PROJECTS",
        "Ukraine Swiss reconstruction project package",
        "GLOBAL",
        "success_candidate",
        date(2025, 8, 28),
        date(2025, 8, 28),
        None,
        None,
        None,
        ("actual_project", "project_financing", "participating_company", "public_infrastructure"),
        ("financing_delay", "geopolitical_setback", "project_start_delay"),
        "funded_reconstruction_reference_candidate",
        "needs_price_backfill",
        ("Round51 analyst matrix",),
        "Funded projects are Stage 2 reference evidence; company-level contracts and margins still decide scoring.",
    ),
    Round51CaseCandidate(
        "ukraine_telecom_ebrd_ifc_case",
        "GEOPOLITICAL_RECONSTRUCTION",
        "UKRAINE_TELECOM_RECOVERY",
        "Ukraine telecom EBRD IFC financing",
        "GLOBAL",
        "success_candidate",
        date(2024, 10, 10),
        date(2024, 10, 10),
        None,
        None,
        None,
        ("project_financing", "telecom_infrastructure", "network_recovery", "participating_company"),
        ("war_escalation", "financing_delay", "insurance_delay"),
        "funded_geopolitical_infra_candidate",
        "needs_price_backfill",
        ("Round51 analyst matrix",),
        "Financing and infrastructure recovery are better than slogans, but supplier revenue must still be verified.",
    ),
    Round51CaseCandidate(
        "heatwave_ac_grid_stress_case",
        "CLIMATE_DISASTER_EVENT",
        "HEATWAVE_GRID_BASKET",
        "Heatwave air-conditioning grid stress",
        "GLOBAL",
        "event_premium",
        date(2025, 7, 18),
        None,
        None,
        None,
        None,
        ("heatwave", "cooling_demand", "grid_stress", "climate_event"),
        ("seasonality", "weather_normalization", "no_sales_conversion"),
        "climate_event_routes_to_grid_watch",
        "needs_price_backfill",
        ("Round51 analyst matrix",),
        "Heatwaves may route research toward grid, cooling, ESS, HVAC, and transformers; the weather event alone is not Green.",
    ),
    Round51CaseCandidate(
        "north_korea_kumgang_dismantle_case",
        "NORTH_KOREA_POLICY_EVENT",
        "INTER_KOREA_POLICY_BASKET",
        "North Korea Kumgang facility dismantle",
        "KR",
        "4c_thesis_break",
        date(2025, 2, 13),
        None,
        None,
        None,
        date(2025, 2, 13),
        ("facility_dismantle", "hostile_state_framing", "road_rail_destroyed"),
        ("facility_dismantle", "military_tension", "sanctions_intact", "policy_reversal"),
        "inter_korea_policy_hard_counterexample",
        "needs_price_backfill",
        ("Round51 analyst matrix",),
        "Facility dismantling and military deterioration are hard RedTeam evidence for inter-Korea policy themes.",
    ),
    Round51CaseCandidate(
        "lk99_superconductor_theme_case",
        "SPECULATIVE_SCIENCE_THEME",
        "LK99_THEME_BASKET",
        "LK-99 speculative science theme rally",
        "GLOBAL",
        "overheat",
        date(2023, 7, 31),
        None,
        None,
        date(2023, 8, 1),
        None,
        ("preprint", "sns_video", "theme_keyword_spike", "price_only_rally"),
        ("preprint_only", "no_commercial_product", "no_customer_contract"),
        "price_moved_without_technical_or_revenue_evidence",
        "needs_price_backfill",
        ("Round51 analyst matrix",),
        "Preprint/SNS-driven price movement is a theme-overheat case before replication and customers are verified.",
        (E2RArchetype.THEME_VALUATION_OVERHEAT,),
    ),
    Round51CaseCandidate(
        "lk99_replication_failure_case",
        "SPECULATIVE_SCIENCE_THEME",
        "LK99_THEME_BASKET",
        "LK-99 replication failure",
        "GLOBAL",
        "4c_thesis_break",
        date(2023, 8, 8),
        None,
        None,
        None,
        date(2023, 8, 8),
        ("replication_failure", "impurity_explanation", "peer_review_failure"),
        ("replication_failure", "no_commercial_product", "technical_validation_failure"),
        "speculative_science_thesis_break",
        "needs_price_backfill",
        ("Round51 analyst matrix",),
        "Replication failure is the clean 4C example for speculative-science themes.",
        (E2RArchetype.THEME_VALUATION_OVERHEAT,),
    ),
    Round51CaseCandidate(
        "covid_diagnostics_demand_wane_case",
        "DIAGNOSTICS_INFECTIOUS_EVENT",
        "COVID_DIAGNOSTICS_BASKET",
        "COVID diagnostics demand wanes",
        "GLOBAL",
        "4c_thesis_break",
        date(2025, 10, 15),
        None,
        None,
        None,
        date(2025, 10, 15),
        ("diagnostic_sales_decline", "testing_demand_wane", "post_event_revenue_drop"),
        ("testing_demand_wane", "diagnostic_sales_decline", "guide_down"),
        "one_off_diagnostic_demand_normalized",
        "needs_price_backfill",
        ("Round51 analyst matrix",),
        "Diagnostics revenue decline after event demand proves why COVID-style EPS spikes should not be structural Green.",
    ),
    Round51CaseCandidate(
        "california_wildfire_rebuild_material_case",
        "DISASTER_REBUILD_EVENT",
        "WILDFIRE_REBUILD_MATERIAL",
        "California wildfire rebuild material donation",
        "US",
        "event_premium",
        date(2026, 4, 1),
        None,
        None,
        None,
        None,
        ("wildfire_rebuild", "material_demand", "rebuild_aid"),
        ("one_off_rebuild_fade", "budget_delay", "insurance_delay"),
        "disaster_rebuild_one_off_event",
        "needs_price_backfill",
        ("Round51 analyst matrix",),
        "Rebuild headlines need actual orders, budget, insurance, and margin before becoming scoring evidence.",
    ),
    Round51CaseCandidate(
        "local_policy_theme_case",
        "POLICY_LOCAL_THEME",
        "LOCAL_POLICY_BASKET",
        "Local policy theme basket",
        "KR",
        "event_premium",
        None,
        None,
        None,
        None,
        None,
        ("local_policy_headline", "regional_development_theme"),
        ("budget_missing", "no_company_exposure", "policy_reversal"),
        "policy_theme_without_budget_or_revenue",
        "needs_price_backfill",
        ("Round51 analyst matrix",),
        "A local-policy label is routing data only until budget, contract, construction, or revenue is visible.",
    ),
)


ROUND51_PRICE_FIELDS: tuple[str, ...] = (
    "case_id",
    "symbol",
    "company_name",
    "primary_archetype",
    "secondary_archetypes",
    "event_type",
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
    "MFE_5D",
    "MFE_20D",
    "MFE_60D",
    "MFE_90D",
    "MFE_180D",
    "MAE_5D",
    "MAE_20D",
    "MAE_60D",
    "MAE_90D",
    "MAE_180D",
    "drawdown_after_peak",
    "below_stage1_price_flag",
    "below_stage2_price_flag",
    "below_stage3_price_flag",
    "policy_event_flag",
    "geopolitical_event_flag",
    "disaster_event_flag",
    "climate_event_flag",
    "disease_event_flag",
    "science_theme_flag",
    "government_contract_flag",
    "government_purchase_amount",
    "stockpile_contract_flag",
    "project_financing_flag",
    "budget_approved_flag",
    "construction_started_flag",
    "revenue_visibility_flag",
    "vaccine_order_doses",
    "outbreak_status",
    "diagnostic_sales_change",
    "demand_normalization_flag",
    "replication_success_flag",
    "replication_failure_flag",
    "peer_review_status",
    "commercial_product_flag",
    "customer_contract_flag",
    "sanctions_relief_flag",
    "military_tension_flag",
    "facility_dismantle_flag",
    "road_rail_destroyed_flag",
    "tourism_reopening_flag",
    "rebuild_project_flag",
    "insurance_delay_flag",
    "one_off_rebuild_flag",
    "score_price_alignment",
    "price_validation_status",
)


def target_for(target_id: str) -> Round51ScoreTarget | None:
    for target in ROUND51_SCORE_TARGETS:
        if target.target_id == target_id:
            return target
    return None


def round51_case_records() -> tuple[E2RCaseRecord, ...]:
    records: list[E2RCaseRecord] = []
    for candidate in ROUND51_CASE_CANDIDATES:
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
                f"Round51 R11 case for {candidate.target_id}; "
                "event evidence is calibration-only and missing prices remain unfilled."
            ),
            stage1_evidence=candidate.evidence_fields,
            stage2_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage2_signals or field in target.green_conditions),
            stage3_evidence=tuple(field for field in candidate.evidence_fields if field in target.stage3_conditions),
            stage4b_evidence=stage4b_evidence,
            stage4c_evidence=stage4c_evidence,
            must_have_fields=target.green_conditions,
            red_flag_fields=candidate.red_flag_fields,
            key_evidence_fields=candidate.evidence_fields,
            false_positive_reason="; ".join(candidate.red_flag_fields) if candidate.case_type in {"failed_rerating", "event_premium", "overheat", "4b_watch", "4c_thesis_break", "one_off"} else None,
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
                "event_news_is_not_green_evidence_alone",
                "contract_budget_revenue_or_recurring_demand_required_for_green",
                "date_verified_evidence_required",
                *target.red_flags,
            ),
            notes=f"{candidate.notes} Sources: {', '.join(candidate.source_refs)}.",
            price_validation=PriceValidation(price_validation_status=candidate.price_validation_status),
            data_quality=CaseDataQuality(
                official_data_available=bool(candidate.evidence_fields),
                report_data_available=False,
                price_data_available=False,
                stage_dates_confidence=0.7 if candidate.stage1_date or candidate.stage2_date or candidate.stage4b_date or candidate.stage4c_date else 0.2,
            ),
        )
        record.validate()
        records.append(record)
    return tuple(records)


def round51_score_profile_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for target in ROUND51_SCORE_TARGETS:
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


def round51_case_candidate_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for candidate in ROUND51_CASE_CANDIDATES:
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


def round51_stage_date_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "target_id": target.target_id,
            "stage1": "|".join(target.stage1_signals),
            "stage2": "|".join(target.stage2_signals),
            "stage3": "|".join(target.stage3_conditions),
            "stage4b": "|".join(target.stage4b_conditions),
            "stage4c": "|".join(target.stage4c_conditions),
            "production_scoring_changed": "false",
        }
        for target in ROUND51_SCORE_TARGETS
    )


def round51_price_field_rows() -> tuple[dict[str, str], ...]:
    return tuple({"field": field, "required_for_round51_backfill": "true"} for field in ROUND51_PRICE_FIELDS)


def round51_summary() -> dict[str, int | bool]:
    records = round51_case_records()
    return {
        "target_count": len(ROUND51_SCORE_TARGETS),
        "case_candidate_count": len(records),
        "success_candidate_count": sum(1 for record in records if record.case_type == "success_candidate"),
        "event_premium_count": sum(1 for record in records if record.case_type == "event_premium"),
        "one_off_count": sum(1 for record in records if record.case_type == "one_off"),
        "overheat_count": sum(1 for record in records if record.case_type == "overheat"),
        "failed_rerating_count": sum(1 for record in records if record.case_type == "failed_rerating"),
        "stage4b_case_count": sum(1 for record in records if record.case_type == "4b_watch" or record.stage4b_date),
        "stage4c_case_count": sum(1 for record in records if record.case_type == "4c_thesis_break"),
        "green_possible_count": sum(1 for target in ROUND51_SCORE_TARGETS if target.posture == Round10ThemePosture.GREEN_POSSIBLE),
        "watch_yellow_first_count": sum(1 for target in ROUND51_SCORE_TARGETS if target.posture == Round10ThemePosture.WATCH_YELLOW_FIRST),
        "redteam_first_count": sum(1 for target in ROUND51_SCORE_TARGETS if target.posture == Round10ThemePosture.REDTEAM_FIRST),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
    }


def write_round51_r11_reports(
    *,
    output_directory: str | Path = ROUND51_DEFAULT_OUTPUT_DIRECTORY,
    cases_path: str | Path = ROUND51_DEFAULT_CASES_PATH,
    score_profile_path: str | Path = ROUND51_DEFAULT_SCORE_PROFILE_PATH,
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
        "summary": output / "round51_r11_policy_geopolitical_event_summary.md",
        "case_matrix": output / "round51_r11_case_matrix.csv",
        "stage_date_plan": output / "round51_r11_stage_date_plan.csv",
        "green_guardrails": output / "round51_r11_green_guardrails.md",
        "event_false_positive_caps": output / "round51_r11_event_false_positive_caps.md",
        "price_validation_plan": output / "round51_r11_price_validation_plan.md",
        "price_fields": output / "round51_r11_price_fields.csv",
    }
    _write_case_jsonl(round51_case_records(), cases)
    _write_rows(round51_score_profile_rows(), score_profiles)
    _write_rows(round51_case_candidate_rows(), paths["case_matrix"])
    _write_rows(round51_stage_date_rows(), paths["stage_date_plan"])
    _write_rows(round51_price_field_rows(), paths["price_fields"])
    paths["summary"].write_text(render_round51_summary_markdown(), encoding="utf-8")
    paths["green_guardrails"].write_text(render_round51_green_guardrail_markdown(), encoding="utf-8")
    paths["event_false_positive_caps"].write_text(render_round51_event_false_positive_caps_markdown(), encoding="utf-8")
    paths["price_validation_plan"].write_text(render_round51_price_validation_plan_markdown(), encoding="utf-8")
    return paths


def render_round51_summary_markdown() -> str:
    summary = round51_summary()
    lines = [
        "# Round-51 R11 Policy / Geopolitical / Disaster / Event Summary",
        "",
        f"- source_round: `{ROUND51_SOURCE_ROUND_PATH}`",
        "- large_sector: `POLICY_GEOPOLITICAL_EVENT`",
        f"- target_count: {summary['target_count']}",
        f"- case_candidate_count: {summary['case_candidate_count']}",
        f"- success_candidate_count: {summary['success_candidate_count']}",
        f"- event_premium_count: {summary['event_premium_count']}",
        f"- overheat_count: {summary['overheat_count']}",
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
        "- R11 mostly exists to stop event headlines from becoming unsafe Stage 3-Green.",
        "- Example: `as_of_date=2024-08-15` mpox news can route a company to Stage 1, but without a verified order or recurring procurement it stays event premium.",
        "- Example: Ukraine reconstruction becomes stronger only when project financing, participating companies, contracts, and supplier margins are visible.",
        "- Example: an LK-99 preprint is not revenue evidence; replication failure is a hard 4C-style counterexample.",
    ]
    return "\n".join(lines) + "\n"


def render_round51_green_guardrail_markdown() -> str:
    lines = [
        "# Round-51 R11 Green Guardrails",
        "",
        "| target | posture | Green unlock evidence | Red flags |",
        "| --- | --- | --- | --- |",
    ]
    for target in ROUND51_SCORE_TARGETS:
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
            "- Do not apply these R11 v1.0 weights to production scoring yet.",
            "- Do not treat policy headlines, war/reconstruction slogans, disasters, outbreaks, local policy, or preprints as Green evidence by itself.",
            "- Do not invent contracts, government orders, budgets, dose amounts, project financing, replication success, revenue, or price-path fields.",
            "- Do not lower Stage 3-Green for event recall. Green requires source-backed contract, budget, revenue, recurring demand, or EPS/FCF conversion.",
            "- Treat replication failure, facility dismantling, military escalation, demand normalization, purchase end, budget delay, and no-customer science themes as RedTeam evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round51_event_false_positive_caps_markdown() -> str:
    lines = [
        "# Round-51 R11 Event False-Positive Caps",
        "",
        "- `NORTH_KOREA_POLICY_EVENT`: summit or tourism headlines are Stage 1 until sanctions relief, budget, contract, and cash flow exist.",
        "- `GEOPOLITICAL_RECONSTRUCTION`: MOU and conference headlines are not supplier revenue; use funded project and margin checks.",
        "- `DISASTER_REBUILD_EVENT`: a disaster can create short-term materials demand, but one-off rebuild demand should not be annualized.",
        "- `CLIMATE_DISASTER_EVENT`: heatwave/cooling themes can route research to grid or HVAC, but weather alone is not structural demand.",
        "- `EVENT_DISEASE_PEST_DEMAND`: outbreak alerts need government orders, stockpile contracts, or recurring demand before Stage 2+ confidence.",
        "- `DIAGNOSTICS_INFECTIOUS_EVENT`: testing revenue cliffs after COVID-like events are hard counterexamples.",
        "- `SPECULATIVE_SCIENCE_THEME`: preprints and SNS videos are not technical validation, customers, or revenue.",
        "",
        "Simple example: a stock can jump on an outbreak headline. If `government_purchase_amount` and `recurring_procurement` are empty, the case can be recorded as Stage 1/event premium, not Stage 3-Green.",
    ]
    return "\n".join(lines) + "\n"


def render_round51_price_validation_plan_markdown() -> str:
    lines = [
        "# Round-51 R11 Price Validation Plan",
        "",
        "## Method",
        "",
        "1. Assign stage dates from source evidence only.",
        "2. Store event-date close prices from official price data.",
        "3. Calculate MFE_5D / 20D / 60D / 90D / 180D and matching MAE windows.",
        "4. Compare price moves with contract, order, budget, replication, demand-normalization, and project-financing fields.",
        "5. Mark price-only rallies as event premium or 4B-watch rather than structural success.",
        "",
        "## Priority Case Checks",
        "",
        "| case_id | stage candidate | check |",
        "| --- | --- | --- |",
    ]
    for row in round51_case_candidate_rows():
        if row["stage2_date"] or row["stage4b_date"] or row["stage4c_date"]:
            stage_date = row["stage2_date"] or row["stage4b_date"] or row["stage4c_date"] or row["stage1_date"]
            lines.append(f"| `{row['case_id']}` | {stage_date} | {row['price_validation_status']} |")
    lines.extend(
        [
            "",
            "## Alignment Labels",
            "",
            "- `event_to_contract_stockpile_candidate`: event demand is backed by a government stockpile contract, but still needs recurrence and margin checks.",
            "- `funded_reconstruction_reference_candidate`: project financing exists; company-level contract and margin proof still decide scoring.",
            "- `price_moved_without_technical_or_revenue_evidence`: science or policy theme moved before technical/customer/revenue evidence.",
            "- `speculative_science_thesis_break`: replication failure or no commercialization breaks the thesis.",
            "- `one_off_diagnostic_demand_normalized`: event diagnostics revenue fell after temporary demand normalized.",
        ]
    )
    return "\n".join(lines) + "\n"


def _score_price_alignment(candidate: Round51CaseCandidate) -> str:
    if candidate.case_type == "success_candidate" and ("contract" in candidate.alignment_hint or "funded" in candidate.alignment_hint):
        return "aligned"
    if candidate.case_type in {"event_premium", "one_off", "4b_watch", "overheat"}:
        return "price_moved_without_evidence"
    if candidate.case_type in {"failed_rerating", "4c_thesis_break"}:
        return "false_positive_score"
    return "unknown"


def _rerating_result(candidate: Round51CaseCandidate) -> str:
    if candidate.case_type == "structural_success":
        return "true_rerating"
    if candidate.case_type == "success_candidate":
        if "reconstruction" in candidate.alignment_hint or "geopolitical" in candidate.alignment_hint:
            return "policy_event_rerating"
        if "contract" in candidate.alignment_hint or "stockpile" in candidate.alignment_hint:
            return "event_premium"
        return "unknown"
    if candidate.case_type in {"event_premium", "one_off"}:
        return "event_premium"
    if candidate.case_type in {"4b_watch", "overheat"}:
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
    "ROUND51_CASE_CANDIDATES",
    "ROUND51_DEFAULT_CASES_PATH",
    "ROUND51_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND51_DEFAULT_SCORE_PROFILE_PATH",
    "ROUND51_PRICE_FIELDS",
    "ROUND51_SCORE_TARGETS",
    "ROUND51_SOURCE_ROUND_PATH",
    "Round51CaseCandidate",
    "Round51ScoreTarget",
    "Round51ScoreWeightDraft",
    "render_round51_event_false_positive_caps_markdown",
    "render_round51_green_guardrail_markdown",
    "render_round51_price_validation_plan_markdown",
    "render_round51_summary_markdown",
    "round51_case_candidate_rows",
    "round51_case_records",
    "round51_price_field_rows",
    "round51_score_profile_rows",
    "round51_stage_date_rows",
    "round51_summary",
    "target_for",
    "write_round51_r11_reports",
]
