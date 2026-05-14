"""Create consensus/revision proxy rows from parsed broker reports.

These proxies are intentionally narrow: they only convert numbers explicitly
present in a parsed research report. Missing EPS/OP/FCF revisions remain
missing.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
from typing import Any, Mapping, Sequence

from e2r.models import ConsensusRevision, ConsensusSnapshot, ResearchReport


@dataclass(frozen=True)
class ReportConsensusProxyResult:
    """Consensus proxy rows and reports annotated with proxy metadata."""

    consensus: tuple[ConsensusSnapshot, ...]
    consensus_revisions: tuple[ConsensusRevision, ...]
    reports: tuple[ResearchReport, ...]


def build_report_consensus_proxy(
    reports: Sequence[ResearchReport],
    *,
    as_of_date: date | None = None,
) -> ReportConsensusProxyResult:
    """Convert explicit report estimate fields into consensus proxy objects."""

    consensus: list[ConsensusSnapshot] = []
    revisions: list[ConsensusRevision] = []
    annotated_reports: list[ResearchReport] = []

    for report in reports:
        report_as_of = as_of_date or report.as_of_date
        report_consensus = _consensus_from_report(report, report_as_of)
        report_revision = _revision_from_report(report, report_as_of)
        proxy_created = bool(report_consensus or report_revision)
        parsed_fields = dict(report.parsed_fields)
        if proxy_created:
            parsed_fields["consensus_proxy_created"] = True
            parsed_fields["consensus_proxy_source"] = "research_report"
        consensus.extend(report_consensus)
        if report_revision is not None:
            revisions.append(report_revision)
        annotated_reports.append(replace(report, parsed_fields=parsed_fields))

    return ReportConsensusProxyResult(
        consensus=tuple(consensus),
        consensus_revisions=tuple(revisions),
        reports=tuple(annotated_reports),
    )


def _consensus_from_report(report: ResearchReport, as_of_date: date) -> tuple[ConsensusSnapshot, ...]:
    fiscal_year = _fiscal_year(report)
    rows: list[ConsensusSnapshot] = []
    for offset, prefix in enumerate(("fy1", "fy2", "fy3")):
        values = {
            "sales_e": getattr(report, f"{prefix}_sales"),
            "op_e": getattr(report, f"{prefix}_op"),
            "eps_e": getattr(report, f"{prefix}_eps"),
        }
        if not any(value is not None for value in values.values()):
            continue
        if offset == 0:
            values["per_e"] = report.est_per
            values["pbr_e"] = report.est_pbr
            values["roe_e"] = report.roe
            values["target_price"] = report.target_price
        rows.append(
            ConsensusSnapshot(
                symbol=report.symbol,
                date=report.publish_date,
                fiscal_year=fiscal_year + offset,
                as_of_date=as_of_date,
                source="report_proxy",
                **values,
            )
        )
    return tuple(rows)


def _revision_from_report(report: ResearchReport, as_of_date: date) -> ConsensusRevision | None:
    fields = report.parsed_fields
    values = {
        "eps_revision_1m": _first_number(fields, "eps_revision_pct", "eps_revision_1m_pct", "eps_revision_1m"),
        "op_revision_1m": _first_number(fields, "op_revision_pct", "op_revision_1m_pct", "op_revision_1m"),
        "fcf_revision_1m": _first_number(fields, "fcf_revision_pct", "fcf_revision_1m_pct", "fcf_revision_1m"),
        "target_price_revision_1m": _first_number(
            fields,
            "target_price_revision_pct",
            "target_revision_pct",
            "target_price_revision_1m",
        ),
    }
    if report.target_revision_pct is not None:
        values["target_price_revision_1m"] = report.target_revision_pct
    if not any(value is not None for value in values.values()):
        return None
    return ConsensusRevision(
        symbol=report.symbol,
        date=report.publish_date,
        fiscal_year=_fiscal_year(report),
        as_of_date=as_of_date,
        **values,
    )


def _fiscal_year(report: ResearchReport) -> int:
    value = _first_number(report.parsed_fields, "fy1_fiscal_year", "fiscal_year")
    if value is not None and value >= 1900:
        return int(value)
    return report.publish_date.year


def _first_number(fields: Mapping[str, Any], *keys: str) -> float | None:
    for key in keys:
        value = fields.get(key)
        if value in (None, ""):
            continue
        try:
            return float(value)
        except (TypeError, ValueError):
            continue
    return None


__all__ = ["ReportConsensusProxyResult", "build_report_consensus_proxy"]
