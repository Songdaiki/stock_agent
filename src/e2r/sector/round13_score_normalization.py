"""Round-13 score normalization readiness.

Round 13 keeps production scoring unchanged and turns the analyst notes into a
shadow score-weight hypothesis table. The table explains what evidence should
raise conviction, what blocks Green, and what needs price-path validation.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.round10_theme_tag_taxonomy import Round10ThemePosture


ROUND13_SOURCE_ROUND_PATH = "docs/round/round_13.md"


@dataclass(frozen=True)
class Round13ScoreWeightHypothesis:
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
class Round13NormalizationTarget:
    sub_archetype: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    score_weight: Round13ScoreWeightHypothesis
    green_conditions: tuple[str, ...]
    stage4b_conditions: tuple[str, ...]
    stage4c_conditions: tuple[str, ...]
    red_flags: tuple[str, ...]
    case_candidates: tuple[str, ...]
    interpretation: str

    @property
    def production_scoring_changed(self) -> bool:
        return False


ROUND13_NORMALIZATION_TARGETS: tuple[Round13NormalizationTarget, ...] = (
    Round13NormalizationTarget(
        "PAYMENT_FINTECH_INFRA",
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round13ScoreWeightHypothesis(16, 18, 8, 16, 12, 0, 5),
        ("regulation_approval", "transaction_volume", "fee_model", "recurring_revenue"),
        ("regulatory_expectation_overheated", "related_stocks_rally_without_revenue"),
        ("regulation_denied_or_delayed", "security_issue", "transaction_volume_disappoints"),
        ("law_delay", "security_issue", "no_revenue", "theme_only_payment"),
        ("stablecoin_payment_infra_candidate", "sto_platform_candidate"),
        "Payment/fintech can become more than a theme only after adoption and fee economics are visible.",
    ),
    Round13NormalizationTarget(
        "DIGITAL_ASSET_TOKENIZATION",
        E2RArchetype.THEME_VALUATION_OVERHEAT,
        Round10ThemePosture.REDTEAM_FIRST,
        Round13ScoreWeightHypothesis(10, 8, 5, 8, 5, 0, 5),
        ("regulated_revenue", "issued_volume", "institutional_adoption", "cash_flow"),
        ("law_expectation_crowding", "crypto_theme_price_run"),
        ("regulation_crackdown", "security_issue", "volume_absent"),
        ("no_regulated_revenue", "theme_only_tokenization", "law_delay"),
        ("crypto_theme_no_revenue_counterexample", "regulation_crackdown_4c"),
        "Tokenization is RedTeam-first; law headlines do not create structural EPS/FCF evidence.",
    ),
    Round13NormalizationTarget(
        "INSURANCE_UNDERWRITING_CYCLE",
        E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round13ScoreWeightHypothesis(15, 20, 5, 15, 25, 10, 5),
        ("loss_ratio_improvement", "csm_growth", "capital_ratio_stable", "shareholder_return_execution"),
        ("pbr_roe_gap_normalized", "valueup_consensus_crowded"),
        ("loss_ratio_worsens", "capital_ratio_down", "return_policy_retreat"),
        ("low_pbr_only", "weak_capital_ratio", "credit_cost"),
        ("nonlife_insurance_loss_ratio_success_candidate", "life_insurance_csm_candidate", "low_pbr_no_roe_value_trap"),
        "Insurance needs underwriting quality and capital return; high dividend alone is not enough.",
    ),
    Round13NormalizationTarget(
        "BEAUTY_OEM_ODM_SUPPLYCHAIN",
        E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round13ScoreWeightHypothesis(22, 23, 12, 16, 13, 0, 5),
        ("export_growth", "customer_diversification", "opm_roe_improvement", "working_capital_clean"),
        ("kbeauty_reports_crowded", "margin_peak", "target_multiple_saturated"),
        ("sell_through_slowdown", "receivables_spike", "tariff_or_regulation_hit"),
        ("china_dependency", "viral_only_brand", "channel_stuffing"),
        ("kbeauty_oem_odm_success_candidate", "channel_stuffing_receivables_4c"),
        "K-beauty supply chain can be Green-eligible only when repeat orders and working capital quality align.",
    ),
    Round13NormalizationTarget(
        "BATTERY_RECYCLING_ESS_SHIFT",
        E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round13ScoreWeightHypothesis(20, 16, 14, 10, 10, 0, 5),
        ("ess_demand", "lifecycle_recycling_volume", "utilization_improvement", "fcf_after_capex"),
        ("ess_shift_fully_priced", "ev_slowdown_ignored", "capacity_story_crowded"),
        ("ev_demand_slows", "mineral_price_down", "utilization_down", "capex_overbuild"),
        ("ev_demand_headline_only", "recycling_volume_absent", "margin_unclear"),
        ("ess_shift_battery_candidate", "battery_capa_overbuild"),
        "ESS/recycling is a watch path inside battery, not automatic Green while EV/CAPA risk remains high.",
    ),
    Round13NormalizationTarget(
        "HYDROGEN_FUEL_CELL_INFRA",
        E2RArchetype.THEME_VALUATION_OVERHEAT,
        Round10ThemePosture.REDTEAM_FIRST,
        Round13ScoreWeightHypothesis(18, 18, 12, 12, 10, 0, 5),
        ("actual_capex", "production_capacity", "customer_demand", "op_eps_conversion"),
        ("policy_support_fully_priced", "factory_announcement_without_orders"),
        ("subsidy_cut", "utilization_down", "project_delay"),
        ("policy_only", "no_customer", "no_revenue"),
        ("hydrogen_fuel_cell_plant_candidate", "hydrogen_theme_no_revenue_counterexample"),
        "Hydrogen needs CAPEX plus customers and utilization; policy enthusiasm is not enough.",
    ),
    Round13NormalizationTarget(
        "SOLAR_TARIFF_SUPPLYCHAIN",
        E2RArchetype.UTILITIES_REGULATED_TARIFF,
        Round10ThemePosture.REDTEAM_FIRST,
        Round13ScoreWeightHypothesis(18, 18, 12, 12, 10, 0, 5),
        ("project_backlog", "tariff_visibility", "subsidy_support", "margin_visibility"),
        ("subsidy_story_crowded", "policy_premium_ahead_of_orders"),
        ("customs_hold", "tariff_delay", "subsidy_cut", "supply_chain_disruption"),
        ("policy_dependency", "module_oversupply", "tariff_risk"),
        ("solar_policy_candidate", "solar_tariff_supplychain_4c"),
        "Solar policy is RedTeam-first where tariff/customs risk can quickly break the thesis.",
    ),
    Round13NormalizationTarget(
        "TIRE_AUTO_COMPONENT_SPREAD",
        E2RArchetype.AUTO_MOBILITY_COMPONENTS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round13ScoreWeightHypothesis(20, 18, 10, 14, 14, 0, 5),
        ("customer_diversification", "opm_improvement", "raw_material_spread", "repeat_supply_visibility"),
        ("peak_margin", "auto_cycle_peak", "valuation_normalized"),
        ("raw_material_spike", "factory_disruption", "customer_demand_slowdown", "recall_quality_cost"),
        ("single_customer_dependency", "ev_demand_slowdown", "factory_fire"),
        ("tire_spread_success_candidate", "factory_fire_4c_counterexample"),
        "Tire/component evidence must connect ASP, raw-material spread, and customer diversification.",
    ),
    Round13NormalizationTarget(
        "CDMO_HEALTHCARE_CONTRACT",
        E2RArchetype.CDMO_HEALTHCARE_CONTRACT,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round13ScoreWeightHypothesis(20, 24, 12, 12, 12, 0, 5),
        ("multi_year_production_visibility", "capacity_utilization", "customer_diversification", "fcf_conversion"),
        ("capacity_expectation_overheated", "valuation_saturated", "new_plant_fully_priced"),
        ("utilization_down", "patent_litigation", "contract_delay", "price_competition"),
        ("capacity_overbuild", "customer_concentration", "litigation"),
        ("cro_cmo_contract_candidate", "cdmo_capacity_underutilization"),
        "CDMO is contract/utilization scoring, not clinical-story scoring.",
    ),
    Round13NormalizationTarget(
        "SECURITY_IDENTITY_DEEPFAKE",
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round13ScoreWeightHypothesis(20, 22, 8, 16, 14, 0, 5),
        ("recurring_contract", "security_demand", "opm_leverage", "legal_risk_low"),
        ("security_theme_crowded", "ai_security_narrative_ahead_of_revenue"),
        ("budget_cut", "churn", "governance_or_legal_risk"),
        ("theme_only_security", "no_recurring_revenue", "ai_cost_overrun"),
        ("security_identity_candidate", "deepfake_theme_no_revenue_counterexample"),
        "Security/deepfake tags need recurring contracts and low legal/governance risk.",
    ),
    Round13NormalizationTarget(
        "RARE_METALS_GOVERNANCE_EVENT",
        E2RArchetype.RARE_METALS_STRATEGIC_MATERIALS,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round13ScoreWeightHypothesis(18, 16, 15, 16, 15, 10, 5),
        ("fcf_improvement", "capital_allocation_execution", "governance_rerating", "supply_chain_value"),
        ("tender_offer_event_premium", "governance_event_fully_priced"),
        ("governance_dispute_worsens", "investment_delay", "commodity_reversal"),
        ("event_premium_only", "pure_metal_price", "governance_discount"),
        ("korea_zinc_event_premium", "sk_square_valueup"),
        "Strategic metals and holding events must separate true FCF/governance change from event premium.",
    ),
    Round13NormalizationTarget(
        "MEMORY_HBM_CAPACITY_4B_WATCH",
        E2RArchetype.MEMORY_HBM_CAPACITY,
        Round10ThemePosture.GREEN_POSSIBLE,
        Round13ScoreWeightHypothesis(24, 21, 19, 15, 12, 0, 5),
        ("hbm_demand", "memory_price_increase", "supply_discipline", "multi_year_revision"),
        ("one_to_two_year_price_surge", "market_cap_multiple_saturation", "customer_price_resistance", "capex_expansion_news"),
        ("customer_capex_cut", "supply_glut", "memory_price_decline", "revision_down"),
        ("pure_cyclical_bounce", "price_only_memory_rally", "capex_overbuild"),
        ("sk_hynix_hbm_rerating", "sk_hynix_hbm_4b_watch"),
        "HBM is a success archetype and a 4B-watch benchmark after extreme rerating.",
    ),
    Round13NormalizationTarget(
        "AUTO_COMPLETED_VEHICLE_VALUEUP",
        E2RArchetype.AUTO_MOBILITY_COMPLETED_VEHICLE,
        Round10ThemePosture.WATCH_YELLOW_FIRST,
        Round13ScoreWeightHypothesis(20, 18, 10, 15, 17, 10, 5),
        ("hybrid_mix_improvement", "roe_fcf", "shareholder_return", "valuation_discount"),
        ("peak_margin", "valueup_fully_priced", "buyback_no_longer_incremental"),
        ("tariff_policy_risk", "demand_slowdown", "recall_quality_cost", "margin_break"),
        ("policy_risk", "cost_pass_through_failure", "peak_margin"),
        ("hyundai_motor_valueup_candidate", "ev_demand_slowdown_component"),
        "Completed vehicle value-up needs mix, FCF, and executed return, not buyback headline alone.",
    ),
)


def round13_target_rows() -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for item in ROUND13_NORMALIZATION_TARGETS:
        weights = item.score_weight.as_dict()
        rows.append(
            {
                "sub_archetype": item.sub_archetype,
                "canonical_archetype": item.canonical_archetype.value,
                "posture": item.posture.value,
                "eps_fcf": str(weights["eps_fcf"]),
                "structural_visibility": str(weights["structural_visibility"]),
                "bottleneck_pricing": str(weights["bottleneck_pricing"]),
                "market_mispricing": str(weights["market_mispricing"]),
                "valuation": str(weights["valuation"]),
                "capital_allocation": str(weights["capital_allocation"]),
                "information_confidence": str(weights["information_confidence"]),
                "green_conditions": "|".join(item.green_conditions),
                "stage4b_conditions": "|".join(item.stage4b_conditions),
                "stage4c_conditions": "|".join(item.stage4c_conditions),
                "red_flags": "|".join(item.red_flags),
                "case_candidates": "|".join(item.case_candidates),
                "production_scoring_changed": str(item.production_scoring_changed).lower(),
                "interpretation": item.interpretation,
            }
        )
    return tuple(rows)


def target_for(sub_archetype: str) -> Round13NormalizationTarget | None:
    for item in ROUND13_NORMALIZATION_TARGETS:
        if item.sub_archetype == sub_archetype:
            return item
    return None


def round13_policy_groups() -> dict[str, tuple[str, ...]]:
    groups: dict[str, list[str]] = {posture.value: [] for posture in Round10ThemePosture}
    for item in ROUND13_NORMALIZATION_TARGETS:
        groups[item.posture.value].append(item.sub_archetype)
    return {key: tuple(value) for key, value in groups.items()}


def write_round13_score_normalization_reports(
    *,
    output_directory: str | Path = "output/e2r_round13_score_normalization",
    score_profile_path: str | Path = "data/sector_taxonomy/score_weight_profiles_round13.csv",
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    score_profile = Path(score_profile_path)
    score_profile.parent.mkdir(parents=True, exist_ok=True)
    paths = {
        "score_profiles": score_profile,
        "summary": output / "round13_score_normalization_summary.md",
        "target_matrix": output / "round13_score_normalization_targets.csv",
        "green_policy": output / "round13_green_watch_red_policy.md",
        "case_candidate_plan": output / "round13_case_candidate_plan.md",
        "next_plan": output / "round13_shadow_scoring_next_plan.md",
    }
    _write_rows(round13_target_rows(), paths["score_profiles"])
    _write_rows(round13_target_rows(), paths["target_matrix"])
    paths["summary"].write_text(render_round13_summary_markdown(), encoding="utf-8")
    paths["green_policy"].write_text(render_round13_green_policy_markdown(), encoding="utf-8")
    paths["case_candidate_plan"].write_text(render_round13_case_candidate_plan_markdown(), encoding="utf-8")
    paths["next_plan"].write_text(render_round13_next_plan_markdown(), encoding="utf-8")
    return paths


def render_round13_summary_markdown() -> str:
    groups = round13_policy_groups()
    lines = [
        "# Round-13 Score Normalization Readiness",
        "",
        f"- source_round: `{ROUND13_SOURCE_ROUND_PATH}`",
        f"- normalization_target_count: {len(ROUND13_NORMALIZATION_TARGETS)}",
        f"- green_possible_count: {len(groups[Round10ThemePosture.GREEN_POSSIBLE.value])}",
        f"- watch_yellow_first_count: {len(groups[Round10ThemePosture.WATCH_YELLOW_FIRST.value])}",
        f"- redteam_first_count: {len(groups[Round10ThemePosture.REDTEAM_FIRST.value])}",
        "- production_scoring_changed: false",
        "",
        "## Interpretation",
        "- Round 13 is a score-weight hypothesis, not a StageClassifier change.",
        "- Success cases tell us which score axis may deserve more weight.",
        "- Counterexamples tell us which evidence gaps or risks should block Green.",
        "- Price paths still need backfill before shadow scoring can be trusted.",
    ]
    return "\n".join(lines) + "\n"


def render_round13_green_policy_markdown() -> str:
    groups = round13_policy_groups()
    lines = ["# Round-13 Green / Watch / Red Policy", ""]
    for posture in Round10ThemePosture:
        lines.append(f"## {posture.value}")
        for label in groups[posture.value]:
            lines.append(f"- `{label}`")
        lines.append("")
    lines.extend(
        [
            "## Easy Examples",
            "- `DIGITAL_ASSET_TOKENIZATION` is RedTeam-first: law headlines are not EPS/FCF evidence.",
            "- `INSURANCE_UNDERWRITING_CYCLE` can be Green-possible only with loss ratio, CSM/capital, ROE, and executed return.",
            "- `MEMORY_HBM_CAPACITY_4B_WATCH` can be a success case and a 4B watch case after extreme rerating.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round13_case_candidate_plan_markdown() -> str:
    lines = ["# Round-13 Case Candidate Plan", ""]
    for item in ROUND13_NORMALIZATION_TARGETS:
        lines.append(f"## {item.sub_archetype}")
        for case_id in item.case_candidates:
            lines.append(f"- `{case_id}`")
        lines.append("")
    return "\n".join(lines)


def render_round13_next_plan_markdown() -> str:
    return "\n".join(
        [
            "# Round-13 Shadow Scoring Next Plan",
            "",
            "1. Convert planned candidates into case-library records.",
            "2. Backfill stage price, peak price, MFE/MAE, and drawdown.",
            "3. Run shadow scoring with these weight hypotheses only after price-path validation.",
            "4. Keep production Stage 3-Green thresholds unchanged until evidence and price alignment are proven.",
            "",
            "## What Not To Change",
            "- Do not use theme tags as production evidence.",
            "- Do not apply these score weights directly to live scoring.",
            "- Do not treat one-off disease, tokenization, speculative science, or policy themes as Green without verified recurring EPS/FCF evidence.",
            "",
        ]
    )


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
    "ROUND13_NORMALIZATION_TARGETS",
    "ROUND13_SOURCE_ROUND_PATH",
    "Round13NormalizationTarget",
    "Round13ScoreWeightHypothesis",
    "render_round13_case_candidate_plan_markdown",
    "render_round13_green_policy_markdown",
    "render_round13_next_plan_markdown",
    "render_round13_summary_markdown",
    "round13_policy_groups",
    "round13_target_rows",
    "target_for",
    "write_round13_score_normalization_reports",
]
