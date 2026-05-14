"""E2R archetype case library.

The case library is evaluation and calibration material only. Production
candidate generation and scoring must not import this module.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping

from e2r.sector.archetypes import (
    COUNTEREXAMPLE_GROUPS,
    POSITIVE_GROUPS,
    E2RArchetype,
    all_archetype_definitions,
    archetype_definition,
)
from e2r.sources.source_errors import date_value


EXPECTED_GROUPS = POSITIVE_GROUPS | COUNTEREXAMPLE_GROUPS


@dataclass(frozen=True)
class PricePathSummary:
    stage3_price: float | None = None
    peak_price: float | None = None
    mfe_30d: float | None = None
    mfe_90d: float | None = None
    mfe_180d: float | None = None
    mfe_1y: float | None = None
    mfe_2y: float | None = None
    mae_30d: float | None = None
    mae_90d: float | None = None
    mae_180d: float | None = None
    mae_1y: float | None = None
    mae_2y: float | None = None
    drawdown_after_peak: float | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "PricePathSummary":
        return cls(**{key: _float_or_none((value or {}).get(key)) for key in cls.__dataclass_fields__})

    def as_dict(self) -> dict[str, float | None]:
        return {key: getattr(self, key) for key in self.__dataclass_fields__}


@dataclass(frozen=True)
class CaseDataQuality:
    official_data_available: bool
    report_data_available: bool
    price_data_available: bool
    stage_dates_confidence: float

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CaseDataQuality":
        return cls(
            official_data_available=_bool(value.get("official_data_available")),
            report_data_available=_bool(value.get("report_data_available")),
            price_data_available=_bool(value.get("price_data_available")),
            stage_dates_confidence=float(value.get("stage_dates_confidence", 0.0)),
        )

    def as_dict(self) -> dict[str, bool | float]:
        return {
            "official_data_available": self.official_data_available,
            "report_data_available": self.report_data_available,
            "price_data_available": self.price_data_available,
            "stage_dates_confidence": self.stage_dates_confidence,
        }


@dataclass(frozen=True)
class E2RCaseRecord:
    """One positive or counterexample case for an archetype."""

    case_id: str
    symbol: str
    company_name: str
    market: str
    sector_raw: str
    primary_archetype: E2RArchetype
    expected_group: str
    stage1_date: date | None = None
    stage2_date: date | None = None
    stage3_date: date | None = None
    stage4a_date: date | None = None
    stage4b_date: date | None = None
    stage4c_date: date | None = None
    peak_date: date | None = None
    evidence_summary: str = ""
    key_evidence_fields: tuple[str, ...] = field(default_factory=tuple)
    false_positive_reason: str | None = None
    price_path: PricePathSummary = field(default_factory=PricePathSummary)
    data_quality: CaseDataQuality = field(
        default_factory=lambda: CaseDataQuality(False, False, False, 0.0)
    )

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "E2RCaseRecord":
        return cls(
            case_id=str(value["case_id"]),
            symbol=str(value["symbol"]),
            company_name=str(value["company_name"]),
            market=str(value.get("market") or "KR"),
            sector_raw=str(value.get("sector_raw") or ""),
            primary_archetype=E2RArchetype(value["primary_archetype"]),
            expected_group=str(value["expected_group"]),
            stage1_date=_date_or_none(value.get("stage1_date")),
            stage2_date=_date_or_none(value.get("stage2_date")),
            stage3_date=_date_or_none(value.get("stage3_date")),
            stage4a_date=_date_or_none(value.get("stage4a_date")),
            stage4b_date=_date_or_none(value.get("stage4b_date")),
            stage4c_date=_date_or_none(value.get("stage4c_date")),
            peak_date=_date_or_none(value.get("peak_date")),
            evidence_summary=str(value.get("evidence_summary") or ""),
            key_evidence_fields=tuple(value.get("key_evidence_fields") or ()),
            false_positive_reason=value.get("false_positive_reason"),
            price_path=PricePathSummary.from_mapping(value.get("price_path")),
            data_quality=CaseDataQuality.from_mapping(value.get("data_quality") or {}),
        )

    def validate(self) -> None:
        if not self.case_id.strip():
            raise ValueError("case_id must be non-empty")
        if not self.symbol.strip():
            raise ValueError("symbol must be non-empty")
        if self.expected_group not in EXPECTED_GROUPS:
            raise ValueError(f"unsupported expected_group: {self.expected_group}")
        if self.data_quality.stage_dates_confidence < 0 or self.data_quality.stage_dates_confidence > 1:
            raise ValueError("stage_dates_confidence must be between 0 and 1")

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "symbol": self.symbol,
            "company_name": self.company_name,
            "market": self.market,
            "sector_raw": self.sector_raw,
            "primary_archetype": self.primary_archetype.value,
            "expected_group": self.expected_group,
            "stage1_date": _date_text(self.stage1_date),
            "stage2_date": _date_text(self.stage2_date),
            "stage3_date": _date_text(self.stage3_date),
            "stage4a_date": _date_text(self.stage4a_date),
            "stage4b_date": _date_text(self.stage4b_date),
            "stage4c_date": _date_text(self.stage4c_date),
            "peak_date": _date_text(self.peak_date),
            "evidence_summary": self.evidence_summary,
            "key_evidence_fields": list(self.key_evidence_fields),
            "false_positive_reason": self.false_positive_reason,
            "price_path": self.price_path.as_dict(),
            "data_quality": self.data_quality.as_dict(),
        }


@dataclass(frozen=True)
class ArchetypeCoverage:
    archetype: E2RArchetype
    positive_count: int
    counterexample_count: int
    total_count: int
    status: str
    positive_case_ids: tuple[str, ...]
    counterexample_case_ids: tuple[str, ...]


def load_case_library(path: str | Path = "data/e2r_case_library/cases.jsonl") -> tuple[E2RCaseRecord, ...]:
    target = Path(path)
    if not target.exists():
        return ()
    records: list[E2RCaseRecord] = []
    for line in target.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text:
            continue
        record = E2RCaseRecord.from_mapping(json.loads(text))
        record.validate()
        records.append(record)
    return tuple(records)


def write_case_library(records: Iterable[E2RCaseRecord], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for record in records:
        record.validate()
        lines.append(json.dumps(record.as_dict(), ensure_ascii=False, sort_keys=True))
    target.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return target


def coverage_by_archetype(
    records: Iterable[E2RCaseRecord],
    *,
    min_positive_cases: int = 2,
    min_counterexamples: int = 2,
) -> tuple[ArchetypeCoverage, ...]:
    records_tuple = tuple(records)
    coverage: list[ArchetypeCoverage] = []
    for definition in all_archetype_definitions():
        archetype_records = tuple(record for record in records_tuple if record.primary_archetype == definition.archetype)
        positive = tuple(record for record in archetype_records if record.expected_group in POSITIVE_GROUPS)
        counter = tuple(record for record in archetype_records if record.expected_group in COUNTEREXAMPLE_GROUPS)
        status = (
            "covered"
            if len(positive) >= min_positive_cases and len(counter) >= min_counterexamples
            else "insufficient_case_coverage"
        )
        coverage.append(
            ArchetypeCoverage(
                archetype=definition.archetype,
                positive_count=len(positive),
                counterexample_count=len(counter),
                total_count=len(archetype_records),
                status=status,
                positive_case_ids=tuple(record.case_id for record in positive),
                counterexample_case_ids=tuple(record.case_id for record in counter),
            )
        )
    return tuple(coverage)


def render_case_coverage_summary(coverage: Iterable[ArchetypeCoverage]) -> str:
    rows = tuple(coverage)
    covered = sum(1 for row in rows if row.status == "covered")
    lines = [
        "# E2R Case Library Coverage",
        "",
        f"- archetypes_total: {len(rows)}",
        f"- archetypes_covered_2x2: {covered}",
        f"- archetypes_under_covered: {len(rows) - covered}",
        "",
        "## Coverage Matrix",
        "",
        "| archetype | positive | counterexamples | status |",
        "|---|---:|---:|---|",
    ]
    for row in rows:
        lines.append(f"| {row.archetype.value} | {row.positive_count} | {row.counterexample_count} | {row.status} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "- covered means at least two positive and two counterexample records exist.",
            "- insufficient_case_coverage means the archetype should not receive final score-weight changes yet.",
            "- Cases are calibration/evaluation material only, not production candidate-generation input.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_case_coverage_outputs(
    records: Iterable[E2RCaseRecord],
    output_directory: str | Path = "output/e2r_case_library",
    *,
    min_positive_cases: int = 2,
    min_counterexamples: int = 2,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    coverage = coverage_by_archetype(
        tuple(records), min_positive_cases=min_positive_cases, min_counterexamples=min_counterexamples
    )
    summary_path = output / "case_coverage_summary.md"
    summary_path.write_text(render_case_coverage_summary(coverage), encoding="utf-8")
    matrix_path = _write_case_matrix(coverage, output / "archetype_case_matrix.csv")
    weights_path = output / "recommended_score_weights.md"
    weights_path.write_text(render_recommended_score_weights(coverage), encoding="utf-8")
    return {"summary": summary_path, "matrix": matrix_path, "weights": weights_path}


def render_recommended_score_weights(coverage: Iterable[ArchetypeCoverage]) -> str:
    lines = [
        "# Recommended Score Weights",
        "",
        "These are design recommendations only. They are not applied to scoring in Checkpoint 28A.",
        "",
        "| archetype | status | recommended emphasis | do not implement yet? |",
        "|---|---|---|---|",
    ]
    for row in coverage:
        definition = archetype_definition(row.archetype)
        top_weights = ", ".join(
            f"{key}={value:g}" for key, value in sorted(definition.preferred_score_weights.items(), key=lambda item: -item[1])[:3]
        )
        blocked = "yes" if row.status != "covered" else "no"
        lines.append(f"| {row.archetype.value} | {row.status} | {top_weights} | {blocked} |")
    lines.extend(
        [
            "",
            "## What not to do",
            "- Do not lower Stage 3-Green thresholds just to increase recall.",
            "- Do not use case labels as evidence.",
            "- Do not implement final archetype weights where case coverage is insufficient.",
        ]
    )
    return "\n".join(lines) + "\n"


def _write_case_matrix(coverage: Iterable[ArchetypeCoverage], path: Path) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "archetype",
                "positive_count",
                "counterexample_count",
                "total_count",
                "status",
                "positive_case_ids",
                "counterexample_case_ids",
            ),
        )
        writer.writeheader()
        for row in coverage:
            writer.writerow(
                {
                    "archetype": row.archetype.value,
                    "positive_count": row.positive_count,
                    "counterexample_count": row.counterexample_count,
                    "total_count": row.total_count,
                    "status": row.status,
                    "positive_case_ids": "|".join(row.positive_case_ids),
                    "counterexample_case_ids": "|".join(row.counterexample_case_ids),
                }
            )
    return path


def _date_or_none(value: Any) -> date | None:
    if value in (None, ""):
        return None
    return date_value(value)


def _date_text(value: date | None) -> str | None:
    return value.isoformat() if value else None


def _float_or_none(value: Any) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value in (None, ""):
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on", "있음"}


__all__ = [
    "ArchetypeCoverage",
    "CaseDataQuality",
    "E2RCaseRecord",
    "EXPECTED_GROUPS",
    "PricePathSummary",
    "coverage_by_archetype",
    "load_case_library",
    "render_case_coverage_summary",
    "render_recommended_score_weights",
    "write_case_coverage_outputs",
    "write_case_library",
]
