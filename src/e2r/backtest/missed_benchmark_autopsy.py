"""Autopsy for missed benchmark labels after true blind replay."""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import dataclass, field, fields, is_dataclass
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Sequence

from e2r.backtest.benchmark_labels import BenchmarkGroup, BenchmarkLabel, load_benchmark_labels
from e2r.models import Stage
from e2r.research.report_snapshot_store import ReportSnapshotStore
from e2r.research.search_snapshot_store import SearchSnapshotStore


DEFAULT_AUTOPSY_OUTPUT_DIR = Path("output/backtests/blind_discovery_autopsy")


class MissReason(str, Enum):
    NOT_IN_UNIVERSE = "not_in_universe"
    NO_OFFICIAL_SOURCE_SNAPSHOT = "no_official_source_snapshot"
    NO_PRICE_HISTORY = "no_price_history"
    NO_DISCLOSURE_SNAPSHOT = "no_disclosure_snapshot"
    NO_FINANCIAL_SNAPSHOT = "no_financial_snapshot"
    NO_SEARCH_SNAPSHOT = "no_search_snapshot"
    NO_REPORT_SNAPSHOT = "no_report_snapshot"
    SEARCH_SNAPSHOT_EXISTS_BUT_NOT_RANKED = "search_snapshot_exists_but_not_ranked"
    REPORT_SNAPSHOT_EXISTS_BUT_NOT_PARSED = "report_snapshot_exists_but_not_parsed"
    EVIDENCE_AVAILABLE_BUT_NOT_SCORED = "evidence_available_but_not_scored"
    THRESHOLD_TOO_HIGH_LAYER1 = "threshold_too_high_layer1"
    BLOCKED_BY_RED_TEAM = "blocked_by_red_team"
    STAGE_NOT_GREEN_BUT_DETECTED = "stage_not_green_but_detected"
    OUTSIDE_EXPECTED_WINDOW = "outside_expected_window"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class EvidenceAvailability:
    official: bool = False
    price: bool = False
    disclosure: bool = False
    financial: bool = False
    search_snapshot: bool = False
    report_snapshot: bool = False
    news_snapshot: bool = False


@dataclass(frozen=True)
class AutopsyConfig:
    blind_output: str | Path
    benchmark_labels: str | Path = "data/benchmark_labels/e2r_known_winners.json"
    output_directory: str | Path = DEFAULT_AUTOPSY_OUTPUT_DIR
    search_snapshot_root: str | Path = "data/search_snapshots"
    report_snapshot_root: str | Path = "data/report_snapshots"
    run_date: date = field(default_factory=date.today)


@dataclass(frozen=True)
class AutopsyRow:
    label_id: str
    company_name: str
    symbol: str
    expected_window_start: date
    expected_window_end: date
    expected_group: str
    expected_min_layer: str
    appeared_in_candidates: bool
    first_detected_date: date | None
    first_stage: str | None
    primary_miss_reason: str | None
    secondary_miss_reasons: tuple[str, ...]
    evidence_available: EvidenceAvailability
    nearest_candidate_rank: int | None = None
    nearest_detection_date: date | None = None
    recommended_fix: str = "manual_review"

    def __post_init__(self) -> None:
        object.__setattr__(self, "secondary_miss_reasons", tuple(dict.fromkeys(self.secondary_miss_reasons)))


@dataclass(frozen=True)
class MissedBenchmarkAutopsyResult:
    config: AutopsyConfig
    rows: tuple[AutopsyRow, ...]
    output_root: Path | None = None
    report_paths: Mapping[str, Path] = field(default_factory=dict)

    @property
    def detected_rows(self) -> tuple[AutopsyRow, ...]:
        return tuple(item for item in self.rows if item.appeared_in_candidates)

    @property
    def missed_rows(self) -> tuple[AutopsyRow, ...]:
        return tuple(item for item in self.rows if not item.appeared_in_candidates)


class MissedBenchmarkAutopsy:
    """Classify why labels were not found by no-proxy blind replay."""

    def run(self, config: AutopsyConfig, *, write_outputs: bool = True) -> MissedBenchmarkAutopsyResult:
        blind_output = Path(config.blind_output)
        recall_rows = _load_recall(blind_output)
        candidates = _load_candidates(blind_output)
        labels = _labels_by_id(config.benchmark_labels, recall_rows)
        search_store = SearchSnapshotStore(config.search_snapshot_root)
        report_store = ReportSnapshotStore(config.report_snapshot_root)
        source_coverage = _source_coverage(blind_output)
        rows = tuple(
            _autopsy_row(
                label=labels[recall["label_id"]],
                recall=recall,
                candidates=candidates,
                search_store=search_store,
                report_store=report_store,
                source_coverage=source_coverage,
            )
            for recall in recall_rows
            if recall["label_id"] in labels
        )
        result = MissedBenchmarkAutopsyResult(config=config, rows=rows)
        if not write_outputs:
            return result
        return _write_outputs(result)


def _autopsy_row(
    *,
    label: BenchmarkLabel,
    recall: Mapping[str, Any],
    candidates: Sequence[Mapping[str, Any]],
    search_store: SearchSnapshotStore,
    report_store: ReportSnapshotStore,
    source_coverage: Mapping[str, Any],
) -> AutopsyRow:
    appeared = bool(recall.get("appeared_in_candidates"))
    first_date = _date_or_none(recall.get("first_detected_date"))
    stage = _stage_value(recall.get("first_stage"))
    evidence = _evidence_availability(label, candidates, search_store, report_store, source_coverage)
    nearest = _nearest_candidate(label, candidates)
    primary, secondary = _classify_reasons(
        label=label,
        appeared=appeared,
        first_date=first_date,
        first_stage=stage,
        candidates=candidates,
        evidence=evidence,
        nearest=nearest,
    )
    return AutopsyRow(
        label_id=label.label_id,
        company_name=label.company_name,
        symbol=label.symbol,
        expected_window_start=label.expected_window_start,
        expected_window_end=label.expected_window_end,
        expected_group=label.expected_group.value,
        expected_min_layer=label.expected_min_layer.value,
        appeared_in_candidates=appeared,
        first_detected_date=first_date,
        first_stage=stage,
        primary_miss_reason=primary.value if primary else None,
        secondary_miss_reasons=tuple(item.value for item in secondary),
        evidence_available=evidence,
        nearest_candidate_rank=int(nearest["rank"]) if nearest else None,
        nearest_detection_date=_date_or_none(nearest.get("as_of_date")) if nearest else None,
        recommended_fix=_recommended_fix(label, primary, secondary, evidence),
    )


def _classify_reasons(
    *,
    label: BenchmarkLabel,
    appeared: bool,
    first_date: date | None,
    first_stage: str | None,
    candidates: Sequence[Mapping[str, Any]],
    evidence: EvidenceAvailability,
    nearest: Mapping[str, Any] | None,
) -> tuple[MissReason | None, tuple[MissReason, ...]]:
    reasons: list[MissReason] = []
    if not evidence.official:
        reasons.append(MissReason.NO_OFFICIAL_SOURCE_SNAPSHOT)
    if not evidence.price:
        reasons.append(MissReason.NO_PRICE_HISTORY)
    if not evidence.disclosure:
        reasons.append(MissReason.NO_DISCLOSURE_SNAPSHOT)
    if not evidence.financial:
        reasons.append(MissReason.NO_FINANCIAL_SNAPSHOT)
    if not evidence.search_snapshot:
        reasons.append(MissReason.NO_SEARCH_SNAPSHOT)
    if not evidence.report_snapshot:
        reasons.append(MissReason.NO_REPORT_SNAPSHOT)

    in_window_candidate = any(
        item.get("symbol") == label.symbol
        and label.expected_window_start <= _date_or_none(item.get("as_of_date")) <= label.expected_window_end
        for item in candidates
        if _date_or_none(item.get("as_of_date")) is not None
    )
    if not appeared and in_window_candidate:
        return MissReason.EVIDENCE_AVAILABLE_BUT_NOT_SCORED, tuple(reasons)
    if appeared:
        if label.expected_safe_stage == "Green" and first_stage != Stage.STAGE_3_GREEN.value:
            return MissReason.STAGE_NOT_GREEN_BUT_DETECTED, tuple(reasons)
        return None, tuple(reasons)
    if nearest is not None:
        return MissReason.OUTSIDE_EXPECTED_WINDOW, tuple(reasons)
    if evidence.search_snapshot and not evidence.report_snapshot and not in_window_candidate:
        return MissReason.NO_REPORT_SNAPSHOT, tuple(reasons)
    if evidence.search_snapshot and evidence.report_snapshot and not in_window_candidate:
        return MissReason.SEARCH_SNAPSHOT_EXISTS_BUT_NOT_RANKED, tuple(reasons)
    if evidence.report_snapshot and not in_window_candidate:
        return MissReason.REPORT_SNAPSHOT_EXISTS_BUT_NOT_PARSED, tuple(reasons)
    if _is_warning_group(label) and not evidence.search_snapshot and not evidence.report_snapshot:
        return MissReason.NOT_IN_UNIVERSE, tuple(reasons)
    if not evidence.search_snapshot:
        return MissReason.NO_SEARCH_SNAPSHOT, tuple(reasons)
    if not evidence.report_snapshot:
        return MissReason.NO_REPORT_SNAPSHOT, tuple(reasons)
    return MissReason.UNKNOWN, tuple(reasons)


def _evidence_availability(
    label: BenchmarkLabel,
    candidates: Sequence[Mapping[str, Any]],
    search_store: SearchSnapshotStore,
    report_store: ReportSnapshotStore,
    source_coverage: Mapping[str, Any],
) -> EvidenceAvailability:
    symbol_candidates = [item for item in candidates if item.get("symbol") == label.symbol]
    evidence_types = {value for item in symbol_candidates for value in item.get("evidence_types_seen", [])}
    search_snapshots = search_store.load_snapshots(symbol=label.symbol, as_of_date=label.expected_window_end)
    if not search_snapshots:
        search_snapshots = search_store.load_snapshots(company_name=label.company_name, as_of_date=label.expected_window_end)
    report_snapshots = report_store.load_snapshots(symbol=label.symbol, as_of_date=label.expected_window_end)
    if not report_snapshots:
        report_snapshots = report_store.load_snapshots(company_name=label.company_name, as_of_date=label.expected_window_end)
    source_has_price = bool(source_coverage.get("price_available"))
    source_has_disclosure = bool(source_coverage.get("disclosure_available"))
    source_has_financial = bool(source_coverage.get("financial_available"))
    price = "price" in evidence_types or source_has_price
    disclosure = "disclosure" in evidence_types or source_has_disclosure
    financial = "financial_actual" in evidence_types or source_has_financial
    return EvidenceAvailability(
        official=price or disclosure or financial,
        price=price,
        disclosure=disclosure,
        financial=financial,
        search_snapshot=bool(search_snapshots),
        report_snapshot=bool(report_snapshots),
        news_snapshot=any(item.source_type in {"news", "naver_news"} for item in search_snapshots),
    )


def _recommended_fix(
    label: BenchmarkLabel,
    primary: MissReason | None,
    secondary: Sequence[MissReason],
    evidence: EvidenceAvailability,
) -> str:
    if primary is None:
        return "manual_review"
    if primary == MissReason.EVIDENCE_AVAILABLE_BUT_NOT_SCORED:
        return "add_feature_scoring_for_available_evidence"
    if primary == MissReason.THRESHOLD_TOO_HIGH_LAYER1:
        return "adjust_layer1_threshold"
    if primary == MissReason.STAGE_NOT_GREEN_BUT_DETECTED:
        return "manual_review"
    if _is_warning_group(label) and primary in {MissReason.NOT_IN_UNIVERSE, MissReason.OUTSIDE_EXPECTED_WINDOW, MissReason.NO_SEARCH_SNAPSHOT}:
        return "no_action_expected_false_positive"
    if primary == MissReason.NO_PRICE_HISTORY or MissReason.NO_PRICE_HISTORY in secondary:
        if not evidence.search_snapshot and label.expected_group in {BenchmarkGroup.STRUCTURAL, BenchmarkGroup.CYCLICAL}:
            return "add_search_snapshot"
        return "add_price_history"
    if primary in {MissReason.NO_DISCLOSURE_SNAPSHOT, MissReason.NO_OFFICIAL_SOURCE_SNAPSHOT}:
        return "add_opendart_disclosure_snapshot"
    if primary == MissReason.NO_FINANCIAL_SNAPSHOT:
        return "add_feature_scoring_for_available_evidence"
    if primary == MissReason.NO_SEARCH_SNAPSHOT:
        return "add_search_snapshot"
    if primary == MissReason.NO_REPORT_SNAPSHOT:
        return "add_report_snapshot"
    if primary == MissReason.SEARCH_SNAPSHOT_EXISTS_BUT_NOT_RANKED:
        return "improve_report_radar_query"
    if primary == MissReason.REPORT_SNAPSHOT_EXISTS_BUT_NOT_PARSED:
        return "improve_normalizer"
    if primary == MissReason.OUTSIDE_EXPECTED_WINDOW:
        return "add_search_snapshot"
    if primary == MissReason.NOT_IN_UNIVERSE:
        return "improve_snapshot_symbol_mapping"
    return "manual_review"


def render_autopsy_markdown(result: MissedBenchmarkAutopsyResult) -> str:
    rows = result.rows
    detected = [item for item in rows if item.appeared_in_candidates]
    missed = [item for item in rows if not item.appeared_in_candidates]
    reason_counts = Counter(item.primary_miss_reason or "detected" for item in rows)
    fix_counts = Counter(item.recommended_fix for item in rows)
    lines = [
        "# Blind Replay Miss Autopsy",
        "",
        "## Executive Summary",
        "",
        f"- labels_analyzed: {len(rows)}",
        f"- detected: {len(detected)}",
        f"- missed: {len(missed)}",
        f"- missing_snapshot_related: {sum(1 for item in missed if _snapshot_related(item))}",
        f"- scoring_or_threshold_related: {sum(1 for item in missed if _scoring_related(item))}",
        f"- acceptable_warning_misses: {sum(1 for item in missed if item.recommended_fix == 'no_action_expected_false_positive')}",
        "",
        "## Recall Summary",
        "",
        "| company | group | appeared | first date | first stage | primary reason | fix |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in rows:
        lines.append(
            f"| {item.company_name} | {item.expected_group} | {'yes' if item.appeared_in_candidates else 'no'} | "
            f"{item.first_detected_date.isoformat() if item.first_detected_date else 'n/a'} | {item.first_stage or 'n/a'} | "
            f"{item.primary_miss_reason or 'detected'} | {item.recommended_fix} |"
        )
    lines.extend(_section("Missed Structural Labels", [item for item in missed if item.expected_group == "structural"]))
    lines.extend(_section("Missed Cyclical Labels", [item for item in missed if item.expected_group == "cyclical"]))
    lines.extend(_section("Missed One-Off / Boom-Bust / Overheat Labels", [item for item in missed if item.expected_group in {"one_off", "boom_bust", "valuation_overheat"}]))
    lines.extend(
        [
            "## Evidence Gap Matrix",
            "",
            "| label | official | price | disclosure | financial | search | report | news |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in rows:
        ev = item.evidence_available
        lines.append(
            f"| {item.company_name} | {_yn(ev.official)} | {_yn(ev.price)} | {_yn(ev.disclosure)} | "
            f"{_yn(ev.financial)} | {_yn(ev.search_snapshot)} | {_yn(ev.report_snapshot)} | {_yn(ev.news_snapshot)} |"
        )
    lines.extend(
        [
            "",
            "## Fix Priority",
            "",
            "| recommended fix | count |",
            "| --- | ---: |",
        ]
    )
    for fix, count in fix_counts.most_common():
        lines.append(f"| {fix} | {count} |")
    lines.extend(
        [
            "",
            "Primary reason distribution:",
            "",
            "| reason | count |",
            "| --- | ---: |",
        ]
    )
    for reason, count in reason_counts.most_common():
        lines.append(f"| {reason} | {count} |")
    lines.extend(
        [
            "",
            "## What Not To Change",
            "",
            "- Do not lower Stage 3-Green thresholds to improve recall.",
            "- Do not use benchmark labels as evidence.",
            "- Do not claim fixture proxy success as blind discovery.",
            "- Do not fabricate report/news snapshots.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_recommended_fixes(result: MissedBenchmarkAutopsyResult) -> str:
    rows_by_fix: dict[str, list[AutopsyRow]] = {}
    for row in result.rows:
        rows_by_fix.setdefault(row.recommended_fix, []).append(row)
    lines = ["# Recommended Fixes", ""]
    for fix, rows in sorted(rows_by_fix.items(), key=lambda item: (-len(item[1]), item[0])):
        lines.extend([f"## {fix}", ""])
        for row in rows:
            lines.append(f"- {row.company_name} ({row.symbol}): {row.primary_miss_reason or 'detected'}")
        lines.append("")
    lines.extend(
        [
            "## Guardrails",
            "",
            "- Stage 3-Green precision remains strict.",
            "- Add source coverage before changing scoring thresholds.",
            "- Fixture proxy is diagnostic only.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _section(title: str, rows: Sequence[AutopsyRow]) -> list[str]:
    lines = ["", f"## {title}", ""]
    if not rows:
        lines.append("No rows.")
        return lines
    lines.extend(["| label | company | reason | secondary | fix |", "| --- | --- | --- | --- | --- |"])
    for item in rows:
        lines.append(
            f"| {item.label_id} | {item.company_name} | {item.primary_miss_reason} | "
            f"{', '.join(item.secondary_miss_reasons) or 'none'} | {item.recommended_fix} |"
        )
    return lines


def _write_outputs(result: MissedBenchmarkAutopsyResult) -> MissedBenchmarkAutopsyResult:
    output_root = Path(result.config.output_directory)
    output_root.mkdir(parents=True, exist_ok=True)
    prefix = result.config.run_date.isoformat()
    paths = {
        "json": output_root / f"{prefix}_autopsy.json",
        "md": output_root / f"{prefix}_autopsy.md",
        "matrix_csv": output_root / "evidence_gap_matrix.csv",
        "fixes_md": output_root / "recommended_fixes.md",
    }
    paths["json"].write_text(json.dumps(_jsonable(result), ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    paths["md"].write_text(render_autopsy_markdown(result), encoding="utf-8")
    paths["fixes_md"].write_text(render_recommended_fixes(result), encoding="utf-8")
    _write_gap_matrix(paths["matrix_csv"], result.rows)
    return MissedBenchmarkAutopsyResult(
        config=result.config,
        rows=result.rows,
        output_root=output_root,
        report_paths=paths,
    )


def _write_gap_matrix(path: Path, rows: Sequence[AutopsyRow]) -> None:
    fieldnames = (
        "label_id",
        "company_name",
        "symbol",
        "expected_group",
        "appeared_in_candidates",
        "primary_miss_reason",
        "official",
        "price",
        "disclosure",
        "financial",
        "search_snapshot",
        "report_snapshot",
        "news_snapshot",
        "recommended_fix",
    )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            ev = row.evidence_available
            writer.writerow(
                {
                    "label_id": row.label_id,
                    "company_name": row.company_name,
                    "symbol": row.symbol,
                    "expected_group": row.expected_group,
                    "appeared_in_candidates": row.appeared_in_candidates,
                    "primary_miss_reason": row.primary_miss_reason,
                    "official": ev.official,
                    "price": ev.price,
                    "disclosure": ev.disclosure,
                    "financial": ev.financial,
                    "search_snapshot": ev.search_snapshot,
                    "report_snapshot": ev.report_snapshot,
                    "news_snapshot": ev.news_snapshot,
                    "recommended_fix": row.recommended_fix,
                }
            )


def _load_recall(blind_output: Path) -> tuple[Mapping[str, Any], ...]:
    path = blind_output / "benchmark_recall_report.json"
    return tuple(json.loads(path.read_text(encoding="utf-8")))


def _load_candidates(blind_output: Path) -> tuple[Mapping[str, Any], ...]:
    path = blind_output / "discovered_candidates.json"
    if not path.exists():
        return ()
    return tuple(json.loads(path.read_text(encoding="utf-8")))


def _labels_by_id(path: str | Path, recall_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, BenchmarkLabel]:
    labels = {item.label_id: item for item in load_benchmark_labels(path)}
    return {str(row["label_id"]): labels[str(row["label_id"])] for row in recall_rows if str(row["label_id"]) in labels}


def _source_coverage(blind_output: Path) -> Mapping[str, Any]:
    path = blind_output / "blind_discovery_summary.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    summary = data.get("replay_result", {}).get("source_coverage_summary", {})
    return summary if isinstance(summary, Mapping) else {}


def _nearest_candidate(label: BenchmarkLabel, candidates: Sequence[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    same_symbol = [item for item in candidates if item.get("symbol") == label.symbol and _date_or_none(item.get("as_of_date"))]
    if not same_symbol:
        return None

    def distance(row: Mapping[str, Any]) -> int:
        row_date = _date_or_none(row.get("as_of_date"))
        if row_date is None:
            return 10**9
        if row_date < label.expected_window_start:
            return (label.expected_window_start - row_date).days
        if row_date > label.expected_window_end:
            return (row_date - label.expected_window_end).days
        return 0

    return sorted(same_symbol, key=lambda item: (distance(item), int(item.get("rank") or 9999)))[0]


def _date_or_none(value: Any) -> date | None:
    if value in (None, "", "n/a"):
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    return date.fromisoformat(str(value))


def _stage_value(value: Any) -> str | None:
    if value in (None, "", "n/a"):
        return None
    return str(value)


def _is_warning_group(label: BenchmarkLabel) -> bool:
    return label.expected_group in {BenchmarkGroup.ONE_OFF, BenchmarkGroup.BOOM_BUST, BenchmarkGroup.VALUATION_OVERHEAT}


def _snapshot_related(row: AutopsyRow) -> bool:
    reasons = {row.primary_miss_reason, *row.secondary_miss_reasons}
    return bool(
        reasons
        & {
            MissReason.NO_SEARCH_SNAPSHOT.value,
            MissReason.NO_REPORT_SNAPSHOT.value,
            MissReason.NO_OFFICIAL_SOURCE_SNAPSHOT.value,
            MissReason.NO_PRICE_HISTORY.value,
            MissReason.NO_DISCLOSURE_SNAPSHOT.value,
            MissReason.NO_FINANCIAL_SNAPSHOT.value,
        }
    )


def _scoring_related(row: AutopsyRow) -> bool:
    return row.primary_miss_reason in {
        MissReason.EVIDENCE_AVAILABLE_BUT_NOT_SCORED.value,
        MissReason.THRESHOLD_TOO_HIGH_LAYER1.value,
        MissReason.STAGE_NOT_GREEN_BUT_DETECTED.value,
    }


def _yn(value: bool) -> str:
    return "yes" if value else "no"


def _jsonable(value: Any) -> Any:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Path):
        return str(value)
    if is_dataclass(value):
        return {field.name: _jsonable(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_jsonable(item) for item in value]
    return value


__all__ = [
    "AutopsyConfig",
    "AutopsyRow",
    "EvidenceAvailability",
    "MissReason",
    "MissedBenchmarkAutopsy",
    "MissedBenchmarkAutopsyResult",
    "render_autopsy_markdown",
    "render_recommended_fixes",
]
