"""Round-119 E2R first-principles guardrail pack.

Round 119 is a meta round. It does not add a sector case pack and it does not
change production scoring. It freezes the research principle that every loop
must keep: structural industry change must translate into durable EPS/FCF body
weight change, old-frame mispricing, valuation rerating, price-path validation,
and 4B/4C RedTeam survival.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping


ROUND119_SOURCE_ROUND_PATH = "docs/round/round_119.md"
ROUND119_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round119_first_principles"
ROUND119_DEFAULT_PRINCIPLES_PATH = "data/sector_taxonomy/e2r_first_principles_round119.csv"


@dataclass(frozen=True)
class Round119PrincipleStep:
    order: int
    step_id: str
    description: str
    required_evidence: tuple[str, ...]
    failure_mode: str

    def as_row(self) -> dict[str, str]:
        return {
            "order": str(self.order),
            "step_id": self.step_id,
            "description": self.description,
            "required_evidence": "|".join(self.required_evidence),
            "failure_mode": self.failure_mode,
        }


@dataclass(frozen=True)
class Round119GreenGate:
    gate_id: str
    description: str
    example_pass: str
    example_fail: str
    stage_effect: str

    def as_row(self) -> dict[str, str]:
        return {
            "gate_id": self.gate_id,
            "description": self.description,
            "example_pass": self.example_pass,
            "example_fail": self.example_fail,
            "stage_effect": self.stage_effect,
        }


@dataclass(frozen=True)
class Round119LoopFocus:
    loop_id: str
    domain: str
    not_enough: tuple[str, ...]
    required_focus: tuple[str, ...]
    green_blocker: tuple[str, ...]

    def as_row(self) -> dict[str, str]:
        return {
            "loop_id": self.loop_id,
            "domain": self.domain,
            "not_enough": "|".join(self.not_enough),
            "required_focus": "|".join(self.required_focus),
            "green_blocker": "|".join(self.green_blocker),
        }


@dataclass(frozen=True)
class Round119ThemeTagRule:
    rule_id: str
    routing_use: str
    scoring_limit: str
    required_upgrade: str
    example: str

    def as_row(self) -> dict[str, str]:
        return {
            "rule_id": self.rule_id,
            "routing_use": self.routing_use,
            "scoring_limit": self.scoring_limit,
            "required_upgrade": self.required_upgrade,
            "example": self.example,
        }


ROUND119_PRINCIPLE_CHAIN: tuple[Round119PrincipleStep, ...] = (
    Round119PrincipleStep(
        1,
        "industry_structure_change",
        "Industry structure changes before the market fully updates the frame.",
        ("supply_demand_change", "capacity_constraint_or_channel_shift", "company_level_event"),
        "good_theme_without_company_evidence",
    ),
    Round119PrincipleStep(
        2,
        "eps_fcf_bodyweight_change",
        "The structure must lift medium-term EPS/FCF, not just produce a headline.",
        ("fy1_fy2_revision", "op_or_fcf_growth", "margin_or_cash_conversion"),
        "price_or_news_without_eps_fcf",
    ),
    Round119PrincipleStep(
        3,
        "durability_lock",
        "The earnings change needs durability through contracts, backlog, RPO, capacity, channel, or recurring demand.",
        ("contract_quality", "backlog_rpo", "capacity_lock", "recurring_revenue_or_demand"),
        "one_off_shortage_or_event",
    ),
    Round119PrincipleStep(
        4,
        "old_frame_mispricing",
        "The market still prices the company with the old industry frame.",
        ("valuation_discount", "old_peer_frame", "underappreciated_revision_path"),
        "already_fully_rerated",
    ),
    Round119PrincipleStep(
        5,
        "valuation_rerating",
        "A credible new valuation frame must exist and still have runway.",
        ("new_peer_multiple", "pbr_roe_or_per_frame_shift", "rerating_room"),
        "valuation_saturation",
    ),
    Round119PrincipleStep(
        6,
        "price_path_validation",
        "The post-signal price path must align with evidence instead of being price-only noise.",
        ("stage_price", "mfe_mae", "below_entry_check", "peak_and_drawdown"),
        "price_moved_without_evidence",
    ),
    Round119PrincipleStep(
        7,
        "redteam_4b_4c_survival",
        "The candidate must survive accounting, leverage, commercialization, policy, cycle, 4B, and 4C checks.",
        ("no_hard_redteam", "no_thesis_break", "not_saturated_4b", "policy_shock_review"),
        "hard_redteam_or_4c",
    ),
)


ROUND119_GREEN_GATES: tuple[Round119GreenGate, ...] = (
    Round119GreenGate(
        "cross_evidence",
        "Stage 3-Green requires more than one independent evidence family.",
        "disclosure plus financial_actual plus research_report",
        "single news headline or search result",
        "block_green_if_missing",
    ),
    Round119GreenGate(
        "eps_fcf_durability",
        "EPS/FCF must be durable beyond one quarter or one event.",
        "FY1/FY2 OP and FCF revisions supported by backlog or recurring demand",
        "temporary demand spike",
        "block_green_if_missing",
    ),
    Round119GreenGate(
        "structural_visibility",
        "Visibility must match the archetype, such as contracts for industrials or channels for consumer exports.",
        "multi-year contract or export channel sell-through",
        "theme keyword with no visibility field",
        "block_green_if_weak",
    ),
    Round119GreenGate(
        "old_frame_mispricing",
        "The market must still be using an old frame or discount.",
        "cyclical discount remains while earnings path changed",
        "new frame already universally accepted",
        "downgrade_to_watch_or_4b_if_saturated",
    ),
    Round119GreenGate(
        "price_path_alignment",
        "MFE/MAE and drawdown should validate the evidence path.",
        "price rerates after evidence date without breaking below stage price materially",
        "price ran first and evidence never arrived",
        "block_green_or_mark_price_only",
    ),
    Round119GreenGate(
        "no_hard_redteam",
        "Accounting, operational trust, leverage, commercialization, legal, or policy hard breaks block Green.",
        "no filing delay, no auditor resignation, no cash runway collapse",
        "auditor resignation or contract cancellation",
        "hard_block_green",
    ),
    Round119GreenGate(
        "not_saturated_4b",
        "A good structure already in crowded 4B is monitoring, not a fresh Green promotion.",
        "revision still strong and valuation runway remains",
        "target multiples saturated with crowded reports",
        "mark_4b_watch_or_elevated",
    ),
)


ROUND119_FALSE_GREEN_PATTERNS: tuple[str, ...] = (
    "hot_theme_without_eps_fcf",
    "good_industry_without_company_evidence",
    "single_headline_or_mou",
    "low_per_low_pbr_without_bodyweight_change",
    "price_only_rally",
    "one_off_shortage",
    "cycle_success_without_supply_discipline",
    "event_premium_without_contract_budget_or_revenue",
    "pre_revenue_story_without_commercialization",
    "hard_redteam_ignored",
)


ROUND119_LOOP7_FOCUS: tuple[Round119LoopFocus, ...] = (
    Round119LoopFocus(
        "R1",
        "industrial_infra",
        ("order_headline", "power_grid_theme"),
        ("contract_quality", "margin", "eps_fcf_revision", "price_path"),
        ("contract_cancelled", "margin_unknown", "capacity_relief"),
    ),
    Round119LoopFocus(
        "R2",
        "ai_semiconductor",
        ("ai_name", "server_theme"),
        ("hbm_lta", "prepayment", "capacity_constraint", "consensus_revision", "rerating_room"),
        ("capex_cut", "supply_glut", "circular_financing"),
    ),
    Round119LoopFocus(
        "R3",
        "battery_ev_green",
        ("ev_theme", "ess_theme", "capa_announcement"),
        ("contract_amount", "gwh_volume", "opm", "fcf", "customer_quality"),
        ("overcapacity", "mineral_price_down", "negative_fcf"),
    ),
    Round119LoopFocus(
        "R4",
        "materials_spread_strategic",
        ("commodity_price_up",),
        ("price_floor", "offtake", "cost_curve", "fcf", "supply_discipline"),
        ("spread_reversal", "china_oversupply", "inventory_build"),
    ),
    Round119LoopFocus(
        "R5",
        "consumer_retail_brand",
        ("viral_product", "brand_heat"),
        ("repeat_demand", "asp", "channel_sell_through", "opm", "inventory_quality"),
        ("fad_normalization", "channel_stuffing", "recall_or_regulation"),
    ),
    Round119LoopFocus(
        "R6",
        "financial_capital_digital",
        ("low_pbr", "policy_valueup"),
        ("roe", "cet1", "buyback_cancellation", "shareholder_return", "credit_cost"),
        ("pf_credit_cost", "capital_ratio_weak", "event_premium_only"),
    ),
    Round119LoopFocus(
        "R7",
        "biotech_healthcare_device",
        ("approval_news", "clinical_headline"),
        ("prescription_volume", "reimbursement", "commercial_revenue", "cash_runway", "royalty"),
        ("commercialization_failure", "dilution", "approval_delay"),
    ),
    Round119LoopFocus(
        "R8",
        "platform_content_sw_security",
        ("ai_feature", "mau_growth"),
        ("arr", "churn", "arpu", "fcf", "operational_trust"),
        ("outage", "privacy_breach", "regulatory_take_rate_damage"),
    ),
    Round119LoopFocus(
        "R9",
        "mobility_transport_leisure",
        ("robotaxi_name", "autonomous_truck_story", "travel_reopening"),
        ("unit_economics", "safety", "fleet_utilization", "margin", "repeat_revenue"),
        ("safety_failure", "utilization_weak", "cycle_normalization"),
    ),
    Round119LoopFocus(
        "R10",
        "construction_real_estate_materials",
        ("ai_data_center_theme", "asset_headline"),
        ("tenant", "noi_affo", "power_water", "funding_cost", "capex_per_share"),
        ("tenant_absent", "affo_integrity_risk", "capex_dilution"),
    ),
    Round119LoopFocus(
        "R11",
        "policy_geopolitical_event",
        ("policy_news", "mou", "geopolitical_headline"),
        ("contract", "budget", "financing", "actual_order", "revenue_conversion"),
        ("policy_reversal", "unfunded_budget", "event_fade"),
    ),
    Round119LoopFocus(
        "R12",
        "agri_life_misc",
        ("defensive_theme", "education_policy", "agri_cycle"),
        ("recurring_revenue", "unit_economics", "regulatory_pass", "cash_conversion"),
        ("policy_cap", "commodity_reversal", "one_off_disease_event"),
    ),
    Round119LoopFocus(
        "R13",
        "cross_archetype_redteam",
        ("high_score", "past_winner_similarity"),
        ("structural_vs_cycle_vs_event", "4b", "4c", "accounting_trust", "price_validation"),
        ("hard_redteam", "saturated_4b", "false_positive_score"),
    ),
)


ROUND119_THEME_TAG_RULES: tuple[Round119ThemeTagRule, ...] = (
    Round119ThemeTagRule(
        "theme_tag_is_routing_only",
        "Use raw market theme tags to route searches and cheap scan attention.",
        "Do not give EPS/FCF or Green score from the tag itself.",
        "Upgrade only when company-level evidence creates score fields.",
        "power_equipment tag routes; contract amount, backlog, margin, and revisions score.",
    ),
    Round119ThemeTagRule(
        "opendart_list_is_not_detail",
        "Use list disclosures to decide whether detail fetch is needed.",
        "Do not score missing contract amount, counterparty, term, or OP fields.",
        "Upgrade after document/detail parsing confirms fields.",
        "supply contract title routes; amount-to-sales and duration score.",
    ),
    Round119ThemeTagRule(
        "event_needs_conversion",
        "Use events, policy, disease, or disaster headlines as Stage 1 attention.",
        "Do not call event premium structural rerating.",
        "Upgrade only with funded budget, order, financing, revenue, or guidance.",
        "MOU remains event premium; government order plus guidance can become Stage 2.",
    ),
    Round119ThemeTagRule(
        "price_needs_evidence",
        "Use price and trading value to prioritize research.",
        "Do not let price-only movement create Stage 3-Green.",
        "Upgrade only when price follows dated evidence and EPS/FCF path.",
        "price spike without reports or disclosures becomes price_only_rally.",
    ),
    Round119ThemeTagRule(
        "redteam_overrides_score",
        "Use RedTeam flags after scoring and before final stage interpretation.",
        "Do not ignore hard trust, accounting, leverage, legal, or commercialization breaks.",
        "Downgrade or block Green when hard RedTeam is present.",
        "auditor resignation blocks Green even after strong prior revenue growth.",
    ),
)


def round119_principle_rows() -> list[dict[str, str]]:
    return [step.as_row() for step in ROUND119_PRINCIPLE_CHAIN]


def round119_green_gate_rows() -> list[dict[str, str]]:
    return [gate.as_row() for gate in ROUND119_GREEN_GATES]


def round119_loop7_focus_rows() -> list[dict[str, str]]:
    return [focus.as_row() for focus in ROUND119_LOOP7_FOCUS]


def round119_theme_tag_rule_rows() -> list[dict[str, str]]:
    return [rule.as_row() for rule in ROUND119_THEME_TAG_RULES]


def round119_summary() -> dict[str, object]:
    return {
        "source_round": ROUND119_SOURCE_ROUND_PATH,
        "principle_step_count": len(ROUND119_PRINCIPLE_CHAIN),
        "green_gate_count": len(ROUND119_GREEN_GATES),
        "loop7_focus_count": len(ROUND119_LOOP7_FOCUS),
        "theme_tag_rule_count": len(ROUND119_THEME_TAG_RULES),
        "false_green_pattern_count": len(ROUND119_FALSE_GREEN_PATTERNS),
        "production_scoring_changed": False,
        "case_records_are_candidate_generation_input": False,
        "theme_tags_are_score_evidence": False,
    }


def render_round119_summary_markdown() -> str:
    summary = round119_summary()
    lines = [
        "# Round-119 E2R First Principles Guardrail",
        "",
        f"- source_round: `{summary['source_round']}`",
        f"- principle_step_count: {summary['principle_step_count']}",
        f"- green_gate_count: {summary['green_gate_count']}",
        f"- loop7_focus_count: {summary['loop7_focus_count']}",
        f"- theme_tag_rule_count: {summary['theme_tag_rule_count']}",
        f"- false_green_pattern_count: {summary['false_green_pattern_count']}",
        f"- production_scoring_changed: {str(summary['production_scoring_changed']).lower()}",
        f"- case_records_are_candidate_generation_input: {str(summary['case_records_are_candidate_generation_input']).lower()}",
        f"- theme_tags_are_score_evidence: {str(summary['theme_tags_are_score_evidence']).lower()}",
        "",
        "## Principle Chain",
        "",
        "industry structure change -> EPS/FCF bodyweight change -> durability lock -> old-frame mispricing -> valuation rerating -> price-path validation -> RedTeam/4B/4C survival",
        "",
        "## Interpretation",
        "",
        "- Good industry is not enough.",
        "- Hot news is not enough.",
        "- Price-only movement is not enough.",
        "- Low PER/PBR is not enough.",
        "- Stage 3-Green requires cross-evidence, durable EPS/FCF, structural visibility, old-frame mispricing, price-path alignment, no hard RedTeam, and no saturated 4B.",
        "- Example: power equipment is routed by theme tags, but contract quality, backlog, margin, EPS/FCF revision, and price path must do the scoring.",
        "- Example: AI semiconductor is not Green because it says AI; HBM capacity, LTA/prepayment, consensus revision, and rerating room must be visible.",
        "- Example: disease, policy, MOU, or disaster headlines stay event premium until budget, order, financing, revenue, or guidance appears.",
        "",
        "## What Not To Change",
        "",
        "- Do not apply Round119 as production scoring.",
        "- Do not use theme tags as direct score evidence.",
        "- Do not lower Stage 3-Green to improve recall.",
        "- Do not use benchmark or case labels as candidate-generation input.",
        "- Do not fabricate missing EPS, FCF, contract, backlog, price, or disclosure fields.",
    ]
    return "\n".join(lines) + "\n"


def render_round119_green_gate_markdown() -> str:
    lines = [
        "# Round-119 Stage 3-Green Gate Checklist",
        "",
        "| gate | effect | pass example | fail example |",
        "| --- | --- | --- | --- |",
    ]
    for gate in ROUND119_GREEN_GATES:
        lines.append(f"| `{gate.gate_id}` | {gate.stage_effect} | {gate.example_pass} | {gate.example_fail} |")
    lines.extend(
        [
            "",
            "## Easy Example",
            "",
            "A company can have a strong transformer headline and a price breakout, but if there is no contract amount, no margin evidence, no EPS/FCF revision, and no price-path validation after the dated evidence, it stays below Stage 3-Green.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round119_theme_guardrail_markdown() -> str:
    lines = [
        "# Round-119 Theme Tag Guardrails",
        "",
        "| rule | routing use | scoring limit | required upgrade |",
        "| --- | --- | --- | --- |",
    ]
    for rule in ROUND119_THEME_TAG_RULES:
        lines.append(
            f"| `{rule.rule_id}` | {rule.routing_use} | {rule.scoring_limit} | {rule.required_upgrade} |"
        )
    lines.extend(
        [
            "",
            "## Core Rule",
            "",
            "Raw theme tags route attention. They do not create Green evidence. A tag such as `HBM`, `power grid`, `value-up`, or `policy event` must be upgraded into dated company-level fields before scoring.",
        ]
    )
    return "\n".join(lines) + "\n"


def _write_csv(path: Path, rows: Iterable[Mapping[str, str]]) -> None:
    materialized = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not materialized:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(materialized[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(materialized)


def write_round119_reports(
    output_directory: Path = Path(ROUND119_DEFAULT_OUTPUT_DIRECTORY),
    principles_path: Path = Path(ROUND119_DEFAULT_PRINCIPLES_PATH),
) -> dict[str, Path]:
    output_directory.mkdir(parents=True, exist_ok=True)

    summary_json = output_directory / "round119_first_principles_summary.json"
    summary_md = output_directory / "round119_first_principles_summary.md"
    green_gate_md = output_directory / "round119_green_gate_checklist.md"
    loop7_focus_csv = output_directory / "round119_loop7_focus_map.csv"
    theme_guardrail_md = output_directory / "round119_theme_tag_guardrails.md"
    false_green_csv = output_directory / "round119_false_green_patterns.csv"

    principles_path.parent.mkdir(parents=True, exist_ok=True)
    _write_csv(principles_path, round119_principle_rows())
    _write_csv(loop7_focus_csv, round119_loop7_focus_rows())
    _write_csv(
        false_green_csv,
        [{"pattern": pattern, "stage_effect": "block_or_downgrade_green"} for pattern in ROUND119_FALSE_GREEN_PATTERNS],
    )
    summary_json.write_text(json.dumps(round119_summary(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary_md.write_text(render_round119_summary_markdown(), encoding="utf-8")
    green_gate_md.write_text(render_round119_green_gate_markdown(), encoding="utf-8")
    theme_guardrail_md.write_text(render_round119_theme_guardrail_markdown(), encoding="utf-8")

    return {
        "principles": principles_path,
        "summary_json": summary_json,
        "summary_md": summary_md,
        "green_gate_checklist": green_gate_md,
        "loop7_focus_map": loop7_focus_csv,
        "theme_tag_guardrails": theme_guardrail_md,
        "false_green_patterns": false_green_csv,
    }
