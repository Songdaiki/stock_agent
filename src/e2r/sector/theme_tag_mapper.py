"""Theme tag mapper and unmatched audit for v0.5 taxonomy work.

Theme tags are search/routing metadata. They never create production score by
themselves.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping


VALID_GREEN_POLICIES = frozenset(
    {
        "green_allowed",
        "watch_to_green",
        "watch_only",
        "red_watch",
        "event_only",
        "red_flag",
    }
)

VALID_STAGE_BIASES = frozenset(
    {
        "stage1_radar",
        "stage2_candidate",
        "stage3_possible",
        "stage3_rare",
        "stage3_red_bias",
        "event_only",
        "red_team_first",
    }
)

AMBIGUOUS_TAGS = frozenset(
    {
        "화재",
        "인공지능(AI)",
        "카메라",
        "금은",
        "국내 상장한 중국 주",
        "엔진(조선-AI)",
    }
)


@dataclass(frozen=True)
class ThemeMapEntry:
    raw_theme_tag: str
    normalized_theme_tag: str
    large_sector: str
    primary_archetype: str
    secondary_archetypes: tuple[str, ...]
    green_policy: str
    must_have_evidence: tuple[str, ...]
    red_flag_evidence: tuple[str, ...]
    score_weight_profile: str
    default_stage_bias: str
    query_seed_terms: tuple[str, ...]
    notes: str = ""

    @classmethod
    def from_mapping(cls, row: Mapping[str, str]) -> "ThemeMapEntry":
        raw = row.get("raw_theme_tag") or row.get("theme_tag") or ""
        policy = _normalize_policy(row.get("green_policy") or "watch_only")
        stage_bias = row.get("default_stage_bias") or _stage_bias_for_policy(policy)
        return cls(
            raw_theme_tag=raw,
            normalized_theme_tag=row.get("normalized_theme_tag") or normalize_theme_tag(raw),
            large_sector=row.get("large_sector") or "",
            primary_archetype=row.get("primary_archetype") or row.get("primary_sub_archetype") or "",
            secondary_archetypes=_split_multi(row.get("secondary_archetypes") or ""),
            green_policy=policy,
            must_have_evidence=_split_multi(row.get("must_have_evidence") or ""),
            red_flag_evidence=_split_multi(row.get("red_flag_evidence") or ""),
            score_weight_profile=row.get("score_weight_profile") or row.get("primary_archetype") or row.get("primary_sub_archetype") or "",
            default_stage_bias=stage_bias,
            query_seed_terms=_split_multi(row.get("query_seed_terms") or raw),
            notes=row.get("notes") or row.get("mapping_note") or "",
        )

    def validate(self) -> None:
        if not self.raw_theme_tag:
            raise ValueError("raw_theme_tag must be non-empty")
        if not self.normalized_theme_tag:
            raise ValueError("normalized_theme_tag must be non-empty")
        if not self.primary_archetype:
            raise ValueError(f"primary_archetype must be non-empty: {self.raw_theme_tag}")
        if self.green_policy not in VALID_GREEN_POLICIES:
            raise ValueError(f"invalid green_policy: {self.green_policy}")
        if self.default_stage_bias not in VALID_STAGE_BIASES:
            raise ValueError(f"invalid default_stage_bias: {self.default_stage_bias}")

    @property
    def theme_is_score_input(self) -> bool:
        return False

    @property
    def production_scoring_changed(self) -> bool:
        return False

    def as_row(self) -> dict[str, str]:
        return {
            "raw_theme_tag": self.raw_theme_tag,
            "normalized_theme_tag": self.normalized_theme_tag,
            "large_sector": self.large_sector,
            "primary_archetype": self.primary_archetype,
            "secondary_archetypes": "|".join(self.secondary_archetypes),
            "green_policy": self.green_policy,
            "must_have_evidence": "|".join(self.must_have_evidence),
            "red_flag_evidence": "|".join(self.red_flag_evidence),
            "score_weight_profile": self.score_weight_profile,
            "default_stage_bias": self.default_stage_bias,
            "query_seed_terms": "|".join(self.query_seed_terms),
            "notes": self.notes,
            "theme_is_score_input": "false",
            "production_scoring_changed": "false",
        }


@dataclass(frozen=True)
class ThemeCoverageAudit:
    total_raw_tags: int
    normalized_tags: int
    mapped_tags: int
    unmatched_tags: tuple[str, ...]
    ambiguous_tags: tuple[str, ...]
    duplicate_aliases: tuple[str, ...]
    green_policy_distribution: Mapping[str, int]
    archetype_distribution: Mapping[str, int]
    large_sector_distribution: Mapping[str, int]

    @property
    def unmatched_count(self) -> int:
        return len(self.unmatched_tags)

    @property
    def ambiguous_count(self) -> int:
        return len(self.ambiguous_tags)


def normalize_theme_tag(value: str) -> str:
    replacements = {
        "남북경험": "남북경협",
        "컨텐츠": "콘텐츠",
        "마켓컬리오아시스": "마켓컬리오아시스",
    }
    text = value.strip()
    for old, new in replacements.items():
        text = text.replace(old, new)
    for token in ("관련주", "수혜주", "테마주"):
        text = text.replace(token, "")
    for token in (" ", "-", "·", "/", "_", "(", ")", "（", "）", ":", ",", "및"):
        text = text.replace(token, "")
    return text.casefold()


def load_raw_theme_tags(path: str | Path) -> tuple[str, ...]:
    target = Path(path)
    if target.suffix.lower() == ".csv":
        with target.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = tuple(row.get("raw_theme_tag") or row.get("theme_tag") or "" for row in reader)
            return tuple(row.strip() for row in rows if row and row.strip())
    tags: list[str] = []
    for line in target.read_text(encoding="utf-8").splitlines():
        for part in line.split(","):
            value = part.strip()
            if value:
                tags.append(value)
    return tuple(tags)


def load_theme_tag_map(path: str | Path) -> tuple[ThemeMapEntry, ...]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        entries = tuple(ThemeMapEntry.from_mapping(row) for row in reader)
    for entry in entries:
        entry.validate()
    return entries


def audit_theme_tag_coverage(raw_tags: Iterable[str], entries: Iterable[ThemeMapEntry]) -> ThemeCoverageAudit:
    raw_tuple = tuple(raw_tags)
    entry_tuple = tuple(entries)
    by_normalized: dict[str, list[ThemeMapEntry]] = {}
    for entry in entry_tuple:
        by_normalized.setdefault(entry.normalized_theme_tag, []).append(entry)
    normalized_raw = tuple(normalize_theme_tag(tag) for tag in raw_tuple)
    unmatched = tuple(tag for tag, normalized in zip(raw_tuple, normalized_raw) if normalized not in by_normalized)
    duplicate_aliases = tuple(sorted({tag for tag in normalized_raw if normalized_raw.count(tag) > 1}))
    ambiguous = sorted(tag for tag in raw_tuple if tag in AMBIGUOUS_TAGS)
    for tag, normalized in zip(raw_tuple, normalized_raw):
        if len(by_normalized.get(normalized, ())) > 1 and tag not in ambiguous:
            ambiguous.append(tag)
    mapped_entries = [by_normalized[normalized][0] for normalized in normalized_raw if normalized in by_normalized]
    return ThemeCoverageAudit(
        total_raw_tags=len(raw_tuple),
        normalized_tags=len(set(normalized_raw)),
        mapped_tags=len(mapped_entries),
        unmatched_tags=unmatched,
        ambiguous_tags=tuple(sorted(set(ambiguous))),
        duplicate_aliases=duplicate_aliases,
        green_policy_distribution=_count_by(mapped_entries, lambda entry: entry.green_policy),
        archetype_distribution=_count_by(mapped_entries, lambda entry: entry.primary_archetype),
        large_sector_distribution=_count_by(mapped_entries, lambda entry: entry.large_sector),
    )


def write_theme_tag_map(entries: Iterable[ThemeMapEntry], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    _write_rows((entry.as_row() for entry in entries), target)
    return target


def write_raw_theme_tags(tags: Iterable[str], txt_path: str | Path, csv_path: str | Path) -> dict[str, Path]:
    tag_tuple = tuple(tags)
    txt_target = Path(txt_path)
    csv_target = Path(csv_path)
    txt_target.parent.mkdir(parents=True, exist_ok=True)
    csv_target.parent.mkdir(parents=True, exist_ok=True)
    txt_target.write_text("\n".join(tag_tuple) + "\n", encoding="utf-8")
    _write_rows(({"raw_theme_tag": tag, "normalized_theme_tag": normalize_theme_tag(tag)} for tag in tag_tuple), csv_target)
    return {"txt": txt_target, "csv": csv_target}


def write_theme_coverage_outputs(
    audit: ThemeCoverageAudit,
    *,
    output_directory: str | Path = "output/theme_tag_coverage_v05",
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "report": output / "theme_coverage_report.md",
        "unmatched": output / "unmatched_theme_tags.csv",
        "ambiguous": output / "ambiguous_theme_tags.csv",
        "green_policy_distribution": output / "green_policy_distribution.csv",
        "archetype_distribution": output / "archetype_distribution.csv",
        "large_sector_distribution": output / "large_sector_distribution.csv",
    }
    paths["report"].write_text(render_theme_coverage_report(audit), encoding="utf-8")
    _write_rows(({"raw_theme_tag": tag} for tag in audit.unmatched_tags), paths["unmatched"])
    _write_rows(({"raw_theme_tag": tag, "review_reason": "manual_context_required"} for tag in audit.ambiguous_tags), paths["ambiguous"])
    _write_distribution(audit.green_policy_distribution, paths["green_policy_distribution"], "green_policy")
    _write_distribution(audit.archetype_distribution, paths["archetype_distribution"], "primary_archetype")
    _write_distribution(audit.large_sector_distribution, paths["large_sector_distribution"], "large_sector")
    return paths


def render_theme_coverage_report(audit: ThemeCoverageAudit) -> str:
    lines = [
        "# Theme Tag Coverage v0.5 Audit",
        "",
        f"- total_raw_tags: {audit.total_raw_tags}",
        f"- normalized_tags: {audit.normalized_tags}",
        f"- mapped_tags: {audit.mapped_tags}",
        f"- unmatched_tags: {audit.unmatched_count}",
        f"- ambiguous_tags: {audit.ambiguous_count}",
        f"- duplicate_aliases: {len(audit.duplicate_aliases)}",
        "- production_scoring_changed: false",
        "- theme_tags_are_score_input: false",
        "",
        "## Green Policy Distribution",
    ]
    for key, value in sorted(audit.green_policy_distribution.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Top Under-Covered Or Review Areas"])
    if audit.unmatched_tags:
        for tag in audit.unmatched_tags:
            lines.append(f"- unmatched: {tag}")
    else:
        lines.append("- unmatched: none")
    if audit.ambiguous_tags:
        for tag in audit.ambiguous_tags:
            lines.append(f"- ambiguous: {tag}")
    else:
        lines.append("- ambiguous: none")
    lines.extend(
        [
            "",
            "## Interpretation",
            "- Theme absorption is a routing milestone, not a scoring milestone.",
            "- Example: `엠폭스` may route to event-demand RedTeam checks; it should not create Green without recurring demand.",
            "- Example: `HBM` can route to memory/HBM research; score still needs EPS/FCF, pricing, and capacity evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def _normalize_policy(value: str) -> str:
    policy = value.strip()
    if policy == "event_watch":
        return "event_only"
    if policy == "red_team_first":
        return "red_watch"
    return policy if policy in VALID_GREEN_POLICIES else "watch_only"


def _stage_bias_for_policy(policy: str) -> str:
    return {
        "green_allowed": "stage3_possible",
        "watch_to_green": "stage2_candidate",
        "watch_only": "stage1_radar",
        "red_watch": "red_team_first",
        "event_only": "event_only",
        "red_flag": "stage3_red_bias",
    }[policy]


def _split_multi(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split("|") if item.strip())


def _count_by(entries: Iterable[ThemeMapEntry], key_func) -> dict[str, int]:
    counts: dict[str, int] = {}
    for entry in entries:
        key = str(key_func(entry))
        counts[key] = counts.get(key, 0) + 1
    return counts


def _write_distribution(distribution: Mapping[str, int], path: Path, key_name: str) -> Path:
    return _write_rows(({key_name: key, "count": str(value)} for key, value in sorted(distribution.items())), path)


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
    "AMBIGUOUS_TAGS",
    "ThemeCoverageAudit",
    "ThemeMapEntry",
    "VALID_GREEN_POLICIES",
    "VALID_STAGE_BIASES",
    "audit_theme_tag_coverage",
    "load_raw_theme_tags",
    "load_theme_tag_map",
    "normalize_theme_tag",
    "render_theme_coverage_report",
    "write_raw_theme_tags",
    "write_theme_coverage_outputs",
    "write_theme_tag_map",
]
