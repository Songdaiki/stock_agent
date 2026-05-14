"""Report writers for E2R case-library record packs."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from e2r.sector.archetypes import COUNTEREXAMPLE_GROUPS, POSITIVE_GROUPS, E2RArchetype, all_archetype_definitions
from e2r.sector.case_library import E2RCaseRecord


def write_case_record_pack_reports(
    records: Iterable[E2RCaseRecord],
    output_directory: str | Path = "output/e2r_case_library_v02",
) -> dict[str, Path]:
    """Write v0.2 case-pack reports."""

    record_tuple = tuple(records)
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "summary": output / "case_record_summary.md",
        "coverage": output / "archetype_coverage_matrix.csv",
        "alignment": output / "score_price_alignment_summary.md",
        "missing_price": output / "missing_price_data_report.md",
        "guardrail": output / "green_guardrail_summary.md",
    }
    paths["summary"].write_text(_render_summary(record_tuple), encoding="utf-8")
    _write_coverage_matrix(record_tuple, paths["coverage"])
    paths["alignment"].write_text(_render_alignment_summary(record_tuple), encoding="utf-8")
    paths["missing_price"].write_text(_render_missing_price(record_tuple), encoding="utf-8")
    paths["guardrail"].write_text(_render_guardrails(record_tuple), encoding="utf-8")
    return paths


def _render_summary(records: tuple[E2RCaseRecord, ...]) -> str:
    archetypes = {record.primary_archetype for record in records}
    covered = _covered_archetypes(records)
    lines = [
        "# E2R Case Record Pack v0.2 Summary",
        "",
        f"- case_count: {len(records)}",
        f"- archetypes_with_cases: {len(archetypes)}",
        f"- archetypes_covered_2x2: {len(covered)}",
        f"- cases_needing_price_backfill: {sum(1 for record in records if record.price_validation.price_validation_status != 'price_filled')}",
        "",
        "## Case Type Distribution",
    ]
    for key, value in sorted(_count_by(records, lambda record: record.case_type).items()):
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Interpretation",
            "- This pack is calibration/evaluation material only.",
            "- Production scoring thresholds are unchanged.",
            "- Archetypes without 2+ positive/candidate and 2+ counterexample/risk records remain Green-restricted.",
        ]
    )
    return "\n".join(lines) + "\n"


def _write_coverage_matrix(records: tuple[E2RCaseRecord, ...], path: Path) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("archetype", "positive_or_candidate", "counterexample_or_risk", "total", "status"),
        )
        writer.writeheader()
        for definition in all_archetype_definitions():
            subset = tuple(record for record in records if record.primary_archetype == definition.archetype)
            positive = sum(1 for record in subset if record.case_type in POSITIVE_GROUPS)
            risk = sum(1 for record in subset if record.case_type in COUNTEREXAMPLE_GROUPS)
            status = "eligible_for_future_shadow_scoring" if positive >= 2 and risk >= 2 else "green_restricted_insufficient_cases"
            writer.writerow(
                {
                    "archetype": definition.archetype.value,
                    "positive_or_candidate": positive,
                    "counterexample_or_risk": risk,
                    "total": len(subset),
                    "status": status,
                }
            )
    return path


def _render_alignment_summary(records: tuple[E2RCaseRecord, ...]) -> str:
    lines = ["# Score-Price Alignment Summary", ""]
    lines.append("## Alignment Distribution")
    for key, value in sorted(_count_by(records, lambda record: record.score_price_alignment).items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Rerating Result Distribution"])
    for key, value in sorted(_count_by(records, lambda record: record.rerating_result).items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Event Premium Cases"])
    for record in records:
        if record.rerating_result == "event_premium" or record.case_type == "event_premium":
            lines.append(f"- {record.case_id}: {record.company_name}")
    lines.extend(
        [
            "",
            "## Notes",
            "- Event premium is not treated as true structural rerating.",
            "- One-off, overheat, and thesis-break records remain guardrail cases.",
        ]
    )
    return "\n".join(lines) + "\n"


def _render_missing_price(records: tuple[E2RCaseRecord, ...]) -> str:
    lines = ["# Missing Price Data Report", "", "| case_id | symbol | status |", "|---|---|---|"]
    for record in records:
        status = record.price_validation.price_validation_status
        if status != "price_filled":
            lines.append(f"| {record.case_id} | {record.symbol} | {status} |")
    if len(lines) == 4:
        lines.append("| none | none | none |")
    return "\n".join(lines) + "\n"


def _render_guardrails(records: tuple[E2RCaseRecord, ...]) -> str:
    eligible = _covered_archetypes(records)
    lines = [
        "# Green Guardrail Summary",
        "",
        "## Archetypes Eligible for Future Shadow Scoring",
    ]
    if eligible:
        for item in sorted(archetype.value for archetype in eligible):
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.extend(["", "## Green-Restricted Archetypes"])
    for definition in all_archetype_definitions():
        if definition.archetype not in eligible:
            lines.append(f"- {definition.archetype.value}")
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Do not apply score_weight_hint to production scoring yet.",
            "- Do not let event_premium, one_off, overheat, or thesis-break cases become Green without structural evidence.",
            "- Do not fill missing price data by assumption.",
        ]
    )
    return "\n".join(lines) + "\n"


def _covered_archetypes(records: tuple[E2RCaseRecord, ...]) -> set[E2RArchetype]:
    covered: set[E2RArchetype] = set()
    for archetype in E2RArchetype:
        subset = tuple(record for record in records if record.primary_archetype == archetype)
        positive = sum(1 for record in subset if record.case_type in POSITIVE_GROUPS)
        risk = sum(1 for record in subset if record.case_type in COUNTEREXAMPLE_GROUPS)
        if positive >= 2 and risk >= 2:
            covered.add(archetype)
    return covered


def _count_by(records: tuple[E2RCaseRecord, ...], func) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        key = str(func(record))
        counts[key] = counts.get(key, 0) + 1
    return counts


__all__ = ["write_case_record_pack_reports"]
