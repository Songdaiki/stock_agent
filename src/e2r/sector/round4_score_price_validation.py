"""Round-4 score-to-price validation matrix.

Round 4 turns the analyst notes into a calibration-only contract: case records
must explain whether a high score, stage label, and later price path actually
matched. This module does not change production scoring.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import E2RCaseRecord, load_case_library


ROUND4_SOURCE_ROUND_PATH = "docs/round/round_04.md"

ROUND4_PRICE_VALIDATION_REQUIRED_FIELDS = (
    "stage3_price",
    "peak_price",
    "peak_return_from_stage3",
    "mfe_90d",
    "mfe_180d",
    "mfe_1y",
    "mae_90d",
    "mae_180d",
    "mae_1y",
    "below_stage3_price_flag",
    "time_to_50pct",
    "time_to_100pct",
    "time_to_200pct",
)

ROUND4_STAGE_FAILURE_TYPES = (
    "green_success",
    "yellow_success",
    "stage2_watch_success",
    "false_green",
    "false_yellow",
    "should_have_been_red",
    "missed_structural",
)


@dataclass(frozen=True)
class Round4ValidationRule:
    """Score-price validation rule for one archetype."""

    archetype: E2RArchetype
    validation_principle: str
    success_requires: tuple[str, ...]
    reject_if: tuple[str, ...]
    expected_rerating_result: str
    stage_failure_focus: tuple[str, ...]
    score_weight_adjustment_hint: str
    green_policy: str


def _rule(
    archetype: E2RArchetype,
    *,
    validation_principle: str,
    success_requires: tuple[str, ...],
    reject_if: tuple[str, ...],
    expected_rerating_result: str,
    stage_failure_focus: tuple[str, ...],
    score_weight_adjustment_hint: str,
    green_policy: str,
) -> Round4ValidationRule:
    return Round4ValidationRule(
        archetype=archetype,
        validation_principle=validation_principle,
        success_requires=success_requires,
        reject_if=reject_if,
        expected_rerating_result=expected_rerating_result,
        stage_failure_focus=stage_failure_focus,
        score_weight_adjustment_hint=score_weight_adjustment_hint,
        green_policy=green_policy,
    )


ROUND4_ALIGNMENT_RULES = (
    "Score must lead to a Stage label before the relevant price path is judged.",
    "A structural success needs rerating within roughly 6-24 months after Stage 2/3 evidence.",
    "Price movement must be supported by EPS/OP/FCF or credible revision evidence, not theme alone.",
    "If a Stage 3-like score is followed by quick 4C, the score was probably a false positive.",
    "Event premium, one-off demand, and credit relief can move price but are not true structural rerating.",
)

ROUND4_COUNTEREXAMPLE_RULES = (
    "High price return without EPS/FCF evidence becomes price_moved_without_evidence.",
    "Good evidence without rerating becomes evidence_good_but_price_failed.",
    "A Green-like score that should have been Red becomes should_have_been_red.",
    "A report-driven candidate with no commercialization or cash-flow conversion remains Green-restricted.",
)


ROUND4_VALIDATION_RULES: Mapping[E2RArchetype, Round4ValidationRule] = {
    E2RArchetype.PLATFORM_SOFTWARE_INTERNET: _rule(
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        validation_principle="MAU나 트래픽이 아니라 ARPU, take-rate, OPM, FCF가 주가 경로와 맞아야 한다.",
        success_requires=("arpu_or_take_rate_up", "opm_improvement", "fcf_improvement", "rerating_after_monetization"),
        reject_if=("mau_without_monetization", "traffic_only", "ai_cost_overrun", "regulatory_margin_hit"),
        expected_rerating_result="true_rerating_or_no_rerating",
        stage_failure_focus=("false_yellow", "missed_structural"),
        score_weight_adjustment_hint="Increase monetization/OPM proof; do not score MAU as structural visibility by itself.",
        green_policy="Green is rare and requires monetization plus margin/FCF proof.",
    ),
    E2RArchetype.GAME_CONTENT_IP: _rule(
        E2RArchetype.GAME_CONTENT_IP,
        validation_principle="신작 기대와 반복 IP monetization을 분리해서 검증한다.",
        success_requires=("actual_revenue_conversion", "ip_repeatability", "global_sales", "op_eps_revision"),
        reject_if=("new_game_hype_only", "single_ip_dependence", "launch_failure", "contract_or_scandal_risk"),
        expected_rerating_result="true_rerating_or_event_premium",
        stage_failure_focus=("false_green", "should_have_been_red"),
        score_weight_adjustment_hint="Give credit after revenue conversion; heavily penalize pre-launch hype.",
        green_policy="Green requires repeat monetization, not release anticipation.",
    ),
    E2RArchetype.ROBOTICS_FACTORY_AUTOMATION: _rule(
        E2RArchetype.ROBOTICS_FACTORY_AUTOMATION,
        validation_principle="대기업 투자나 MOU는 Stage 1/2 재료지만, 실제 매출/OP 전환 전 Green은 막는다.",
        success_requires=("customer_adoption", "revenue_conversion", "repeat_order", "opm_improvement"),
        reject_if=("theme_only_mou", "strategic_investment_without_revenue", "cash_burn", "price_only_rally"),
        expected_rerating_result="theme_overheat_or_true_rerating",
        stage_failure_focus=("should_have_been_red", "missed_structural"),
        score_weight_adjustment_hint="Treat strategic investment as radar; score revenue conversion separately.",
        green_policy="Green blocked until revenue and margin evidence are visible.",
    ),
    E2RArchetype.RETAIL_DOMESTIC_CONSUMER: _rule(
        E2RArchetype.RETAIL_DOMESTIC_CONSUMER,
        validation_principle="단순 반등이 아니라 2-4개 분기 OPM/FCF 개선이 이어지는지 본다.",
        success_requires=("same_store_sales", "opm_improvement", "fcf_improvement", "inventory_normalization"),
        reject_if=("traffic_only_rebound", "inventory_build", "wage_or_rent_pressure", "one_quarter_rebound"),
        expected_rerating_result="true_rerating_or_cyclical_rerating",
        stage_failure_focus=("false_yellow", "evidence_good_but_price_failed"),
        score_weight_adjustment_hint="Require repeated margin/FCF evidence before structural credit.",
        green_policy="Green requires durable store efficiency or cash-flow improvement.",
    ),
    E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT: _rule(
        E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT,
        validation_principle="PF, 현금흐름, 신용위험이 수주 뉴스보다 먼저다.",
        success_requires=("pf_risk_resolved", "cash_flow_improvement", "debt_reduction", "cost_ratio_stable"),
        reject_if=("credit_relief_only", "pf_loss", "unsold_inventory", "liquidity_stress"),
        expected_rerating_result="credit_relief_rally_or_no_rerating",
        stage_failure_focus=("should_have_been_red", "false_green"),
        score_weight_adjustment_hint="Cap order/backlog score when PF and liquidity risk remain unresolved.",
        green_policy="Green very restricted; credit risk must be resolved first.",
    ),
    E2RArchetype.UTILITIES_REGULATED_TARIFF: _rule(
        E2RArchetype.UTILITIES_REGULATED_TARIFF,
        validation_principle="저평가가 아니라 요금, 원가보상, 부채 정상화가 가격 경로와 맞아야 한다.",
        success_requires=("tariff_or_cost_pass_through", "debt_normalization", "cash_flow_improvement", "policy_durability"),
        reject_if=("tariff_freeze", "policy_event_only", "debt_burden", "dividend_capacity_absent"),
        expected_rerating_result="policy_event_rerating_or_no_rerating",
        stage_failure_focus=("false_yellow", "should_have_been_red"),
        score_weight_adjustment_hint="Score policy durability and balance-sheet repair, not low valuation alone.",
        green_policy="Green requires durable regulatory regime change.",
    ),
    E2RArchetype.NUCLEAR_SMR_GRID_POLICY: _rule(
        E2RArchetype.NUCLEAR_SMR_GRID_POLICY,
        validation_principle="정책 기대와 실제 계약/매출 전환을 분리한다.",
        success_requires=("binding_contract", "revenue_conversion_path", "project_financing", "margin_visibility"),
        reject_if=("policy_headline_only", "legal_delay", "project_financing_absent", "cost_overrun"),
        expected_rerating_result="policy_event_rerating_or_true_rerating",
        stage_failure_focus=("false_yellow", "should_have_been_red"),
        score_weight_adjustment_hint="Keep policy signal as radar unless contract economics are visible.",
        green_policy="Green only with contract economics and low legal/policy risk.",
    ),
    E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE: _rule(
        E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE,
        validation_principle="이벤트 프리미엄과 구조적 discount narrowing을 분리한다.",
        success_requires=("buyback_cancellation_or_return", "nav_discount_catalyst", "fcf_support", "governance_execution"),
        reject_if=("governance_dispute_only", "buyback_without_cancel", "subsidiary_value_impairment", "event_premium_only"),
        expected_rerating_result="event_premium_or_true_rerating",
        stage_failure_focus=("false_yellow", "stage2_watch_success"),
        score_weight_adjustment_hint="Score executed shareholder return and NAV/FCF support above event headlines.",
        green_policy="Green requires executed capital return backed by NAV/FCF improvement.",
    ),
    E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET: _rule(
        E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
        validation_principle="저PBR만이 아니라 ROE, 자본비율, 주주환원이 같이 리레이팅을 설명해야 한다.",
        success_requires=("roe_improvement", "capital_ratio_stable", "credit_cost_stable", "capital_return_execution"),
        reject_if=("low_pbr_only", "pf_credit_cost", "capital_ratio_deterioration", "roe_decline"),
        expected_rerating_result="true_rerating_or_no_rerating",
        stage_failure_focus=("false_green", "false_yellow"),
        score_weight_adjustment_hint="Reward ROE/PBR and executed return; penalize credit cost risk.",
        green_policy="Green possible with ROE/PBR gap plus executed shareholder return.",
    ),
    E2RArchetype.BIOTECH_REGULATORY: _rule(
        E2RArchetype.BIOTECH_REGULATORY,
        validation_principle="임상/허가 뉴스와 매출화/로열티 현금흐름을 분리한다.",
        success_requires=("commercialization_path", "royalty_or_revenue_conversion", "cash_runway", "dilution_risk_low"),
        reject_if=("clinical_news_only", "approval_delay", "cb_or_rights_dilution", "cash_burn"),
        expected_rerating_result="event_premium_or_no_rerating",
        stage_failure_focus=("should_have_been_red", "false_green"),
        score_weight_adjustment_hint="Block pre-revenue Green unless royalty/revenue conversion is visible.",
        green_policy="Pre-revenue clinical stories are Green-blocked.",
    ),
    E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT: _rule(
        E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT,
        validation_principle="단일 장비 판매가 아니라 반복 소모품/수출 재주문이 리레이팅을 설명해야 한다.",
        success_requires=("export_country_expansion", "repeat_consumable_revenue", "opm_roe", "fy1_fy2_eps_revision"),
        reject_if=("single_device_sale", "approval_delay", "competition_intensifies", "asp_decline"),
        expected_rerating_result="true_rerating",
        stage_failure_focus=("missed_structural", "false_yellow"),
        score_weight_adjustment_hint="Increase repeat revenue visibility; do not over-score one-time device sales.",
        green_policy="Green possible with export channel plus recurring revenue and FCF proof.",
    ),
    E2RArchetype.TRAVEL_LEISURE_REOPENING: _rule(
        E2RArchetype.TRAVEL_LEISURE_REOPENING,
        validation_principle="리오프닝 반등과 구조적 수익성 개선을 구분한다.",
        success_requires=("visitor_recovery", "fixed_cost_leverage", "op_eps_revision", "customer_mix_improvement"),
        reject_if=("one_time_reopening", "oil_or_fx_shock", "china_tourism_dependency", "demand_slowdown"),
        expected_rerating_result="cyclical_rerating_or_no_rerating",
        stage_failure_focus=("false_yellow", "should_have_been_red"),
        score_weight_adjustment_hint="Treat reopening as cyclical unless repeated margin/FCF improvement exists.",
        green_policy="Green exceptional; most cases stay Yellow/Watch.",
    ),
    E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE: _rule(
        E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE,
        validation_principle="AI 키워드가 아니라 주문, 병목, 매출 전환이 리레이팅과 맞아야 한다.",
        success_requires=("confirmed_orders", "customer_capex_visibility", "capacity_bottleneck", "op_eps_revision"),
        reject_if=("ai_keyword_only", "no_confirmed_order", "customer_capex_cut", "price_only_rally"),
        expected_rerating_result="true_rerating_or_theme_overheat",
        stage_failure_focus=("missed_structural", "should_have_been_red"),
        score_weight_adjustment_hint="Score confirmed order/revenue exposure above AI keyword exposure.",
        green_policy="Green possible only with confirmed order/revenue and cross-evidence.",
    ),
    E2RArchetype.EDUCATION_SPECIALTY_SERVICES: _rule(
        E2RArchetype.EDUCATION_SPECIALTY_SERVICES,
        validation_principle="정책/입시 이벤트와 반복 서비스 매출을 구분한다.",
        success_requires=("recurring_service_revenue", "opm_improvement", "student_retention_or_pricing", "policy_risk_low"),
        reject_if=("policy_event_only", "regulatory_change", "one_time_enrollment_spike", "margin_pressure"),
        expected_rerating_result="event_premium_or_true_rerating",
        stage_failure_focus=("false_yellow", "stage2_watch_success"),
        score_weight_adjustment_hint="Reward recurring revenue and retention; cap policy-event rallies.",
        green_policy="Green requires durable recurring revenue, not policy-event traffic.",
    ),
}


def round4_rule_for(archetype: E2RArchetype | str) -> Round4ValidationRule:
    item = archetype if isinstance(archetype, E2RArchetype) else E2RArchetype(str(archetype))
    return ROUND4_VALIDATION_RULES.get(
        item,
        _rule(
            item,
            validation_principle="Use generic score-price alignment until a specific Round-4 rule is written.",
            success_requires=("eps_fcf_support", "multi_source_evidence", "rerating_after_signal"),
            reject_if=("theme_only", "single_source_story", "stage4c_after_signal"),
            expected_rerating_result="unknown",
            stage_failure_focus=("unknown",),
            score_weight_adjustment_hint="Do not change production scoring until case coverage exists.",
            green_policy="Fallback rule; keep Green restricted until archetype-specific validation exists.",
        ),
    )


def round4_alignment_summary(records: Iterable[E2RCaseRecord]) -> tuple[dict[str, object], ...]:
    rows = tuple(records)
    output: list[dict[str, object]] = []
    for archetype in sorted({record.primary_archetype for record in rows}, key=lambda item: item.value):
        subset = tuple(record for record in rows if record.primary_archetype == archetype)
        rule = round4_rule_for(archetype)
        output.append(
            {
                "archetype": archetype.value,
                "case_count": len(subset),
                "aligned": sum(1 for record in subset if record.score_price_alignment == "aligned"),
                "unknown": sum(1 for record in subset if record.score_price_alignment == "unknown"),
                "false_positive_score": sum(1 for record in subset if record.score_price_alignment == "false_positive_score"),
                "price_moved_without_evidence": sum(
                    1 for record in subset if record.score_price_alignment == "price_moved_without_evidence"
                ),
                "evidence_good_but_price_failed": sum(
                    1 for record in subset if record.score_price_alignment == "evidence_good_but_price_failed"
                ),
                "green_policy": rule.green_policy,
            }
        )
    return tuple(output)


def write_round4_score_price_validation_reports(
    *,
    case_path: str | Path = "data/e2r_case_library/cases_v02.jsonl",
    output_directory: str | Path = "output/e2r_round4_score_price_validation",
) -> dict[str, Path]:
    records = load_case_library(case_path)
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "rules": output / "round4_score_price_validation_rules.md",
        "field_contract": output / "round4_case_field_contract.md",
        "alignment_summary": output / "round4_alignment_summary.csv",
        "stage_failure_matrix": output / "round4_stage_failure_matrix.md",
    }
    paths["rules"].write_text(render_round4_rules_markdown(), encoding="utf-8")
    paths["field_contract"].write_text(render_round4_field_contract_markdown(), encoding="utf-8")
    _write_alignment_summary_csv(records, paths["alignment_summary"])
    paths["stage_failure_matrix"].write_text(render_round4_stage_failure_matrix_markdown(records), encoding="utf-8")
    return paths


def render_round4_rules_markdown() -> str:
    lines = [
        "# Round-4 Score-Price Validation Rules",
        "",
        f"Source round: `{ROUND4_SOURCE_ROUND_PATH}`",
        "",
        "This is calibration material. It does not change production scoring.",
        "",
        "## Global Alignment Rules",
    ]
    for item in ROUND4_ALIGNMENT_RULES:
        lines.append(f"- {item}")
    lines.extend(["", "## Counterexample Rules"])
    for item in ROUND4_COUNTEREXAMPLE_RULES:
        lines.append(f"- {item}")
    lines.extend(["", "## Archetype Rules"])
    for rule in sorted(ROUND4_VALIDATION_RULES.values(), key=lambda item: item.archetype.value):
        lines.extend(
            [
                "",
                f"### {rule.archetype.value}",
                f"- principle: {rule.validation_principle}",
                f"- success_requires: {', '.join(rule.success_requires)}",
                f"- reject_if: {', '.join(rule.reject_if)}",
                f"- expected_rerating_result: {rule.expected_rerating_result}",
                f"- stage_failure_focus: {', '.join(rule.stage_failure_focus)}",
                f"- score_weight_adjustment_hint: {rule.score_weight_adjustment_hint}",
                f"- Green policy: {rule.green_policy}",
            ]
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "- Do not change StageClassifier thresholds from Round 4.",
            "- Do not use case records as candidate-generation input.",
            "- Do not treat price-only rallies as structural rerating.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round4_field_contract_markdown() -> str:
    lines = [
        "# Round-4 Case Field Contract",
        "",
        "Round 4 adds price-path and failure-type fields so case records can explain whether scoring matched reality.",
        "",
        "## Price Validation Fields",
    ]
    for field_name in ROUND4_PRICE_VALIDATION_REQUIRED_FIELDS:
        lines.append(f"- `{field_name}`")
    lines.extend(["", "## Stage Failure Types"])
    for item in ROUND4_STAGE_FAILURE_TYPES:
        lines.append(f"- `{item}`")
    lines.extend(
        [
            "",
            "## Example",
            "",
            "`as_of_date=2023-07-27`인 Stage 3 후보라면, 2023-07-28 이후 리포트는 evidence가 아니라 "
            "forward price validation 구간의 결과로만 봐야 한다.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round4_stage_failure_matrix_markdown(records: Iterable[E2RCaseRecord]) -> str:
    rows = tuple(records)
    lines = [
        "# Round-4 Stage Failure Matrix",
        "",
        "| stage_failure_type | case_count | interpretation |",
        "|---|---:|---|",
    ]
    counts: dict[str, int] = {}
    for record in rows:
        counts[record.stage_failure_type] = counts.get(record.stage_failure_type, 0) + 1
    for item in ("green_success", "yellow_success", "stage2_watch_success", "false_green", "false_yellow", "should_have_been_red", "missed_structural", "unknown"):
        lines.append(f"| {item} | {counts.get(item, 0)} | {_stage_failure_interpretation(item)} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "- `false_green` means the score/gate would have promoted too aggressively.",
            "- `missed_structural` means evidence or scoring may have missed a real rerating.",
            "- `unknown` usually means price backfill or stage dates are incomplete.",
        ]
    )
    return "\n".join(lines) + "\n"


def _write_alignment_summary_csv(records: Iterable[E2RCaseRecord], path: Path) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "archetype",
                "case_count",
                "aligned",
                "unknown",
                "false_positive_score",
                "price_moved_without_evidence",
                "evidence_good_but_price_failed",
                "green_policy",
            ),
        )
        writer.writeheader()
        for row in round4_alignment_summary(records):
            writer.writerow(row)
    return path


def _stage_failure_interpretation(value: str) -> str:
    return {
        "green_success": "Stage 3-Green and price path both matched structural rerating.",
        "yellow_success": "Yellow/watch posture was enough; Green was not necessary.",
        "stage2_watch_success": "Stage 2/Watch captured the case without over-promoting.",
        "false_green": "Green would have been unsafe because price/evidence later failed.",
        "false_yellow": "Yellow looked plausible but price/evidence did not confirm.",
        "should_have_been_red": "Red/4C guardrail should dominate the candidate.",
        "missed_structural": "A structural move may have been missed by evidence or scoring.",
        "unknown": "Insufficient stage or price validation data.",
    }.get(value, "Unknown failure type.")


__all__ = [
    "ROUND4_ALIGNMENT_RULES",
    "ROUND4_COUNTEREXAMPLE_RULES",
    "ROUND4_PRICE_VALIDATION_REQUIRED_FIELDS",
    "ROUND4_SOURCE_ROUND_PATH",
    "ROUND4_STAGE_FAILURE_TYPES",
    "ROUND4_VALIDATION_RULES",
    "Round4ValidationRule",
    "render_round4_field_contract_markdown",
    "render_round4_rules_markdown",
    "render_round4_stage_failure_matrix_markdown",
    "round4_alignment_summary",
    "round4_rule_for",
    "write_round4_score_price_validation_reports",
]
