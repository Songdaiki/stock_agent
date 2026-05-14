"""Raw API response schema profiling for Korea API probes."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from e2r.probe.expected_fields import compare_expected_fields


@dataclass(frozen=True)
class FieldProfile:
    """Observed raw field shape."""

    name: str
    types: tuple[str, ...]
    samples: tuple[Any, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class SchemaProfile:
    """Schema summary for one raw response."""

    source_name: str
    top_level_keys: tuple[str, ...]
    item_path_candidates: tuple[str, ...]
    selected_item_path: str | None
    item_count: int
    fields: tuple[FieldProfile, ...]
    expected_field_comparison: Mapping[str, object]


def load_raw_payload(path: str | Path) -> Any:
    """Load a JSON raw response for profiling."""

    return json.loads(Path(path).read_text(encoding="utf-8"))


def profile_payload(source_name: str, payload: Any, *, sample_size: int = 20) -> SchemaProfile:
    """Profile one raw JSON-like payload."""

    top_level_keys = tuple(sorted(str(key) for key in payload.keys())) if isinstance(payload, Mapping) else ()
    list_candidates = find_list_candidates(payload)
    selected_path, rows = select_item_rows(payload, list_candidates)
    field_map = collect_field_profiles(rows[:sample_size])
    observed_fields = set(field_map)
    if isinstance(payload, Mapping):
        observed_fields.update(str(key) for key in payload.keys())
    comparison = compare_expected_fields(source_name, observed_fields)
    return SchemaProfile(
        source_name=source_name,
        top_level_keys=top_level_keys,
        item_path_candidates=tuple(path for path, _rows in list_candidates),
        selected_item_path=selected_path,
        item_count=len(rows),
        fields=tuple(field_map.values()),
        expected_field_comparison=comparison,
    )


def find_list_candidates(payload: Any, *, prefix: str = "") -> tuple[tuple[str, list[Any]], ...]:
    """Find list-like item paths inside a JSON-like payload."""

    found: list[tuple[str, list[Any]]] = []
    if isinstance(payload, list):
        found.append((prefix or "$", payload))
        for index, item in enumerate(payload[:3]):
            child_prefix = f"{prefix}[{index}]" if prefix else f"$[{index}]"
            found.extend(find_list_candidates(item, prefix=child_prefix))
        return tuple(found)
    if not isinstance(payload, Mapping):
        return ()
    for key, value in payload.items():
        path = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, list):
            found.append((path, value))
            for index, item in enumerate(value[:3]):
                found.extend(find_list_candidates(item, prefix=f"{path}[{index}]"))
        elif isinstance(value, Mapping):
            found.extend(find_list_candidates(value, prefix=path))
    return tuple(found)


def select_item_rows(payload: Any, candidates: Sequence[tuple[str, list[Any]]]) -> tuple[str | None, list[Mapping[str, Any]]]:
    """Select the most likely list of item rows."""

    best_path: str | None = None
    best_rows: list[Mapping[str, Any]] = []
    for path, rows in candidates:
        dict_rows = [row for row in rows if isinstance(row, Mapping)]
        if not dict_rows:
            continue
        if len(dict_rows) > len(best_rows) or _path_rank(path) > _path_rank(best_path or ""):
            best_path = path
            best_rows = [dict(row) for row in dict_rows]
    if best_rows:
        return best_path, best_rows
    if isinstance(payload, Mapping):
        return "$", [dict(payload)]
    return None, []


def collect_field_profiles(rows: Sequence[Mapping[str, Any]]) -> dict[str, FieldProfile]:
    """Collect field names, inferred basic types, and sample values."""

    values_by_field: dict[str, list[Any]] = {}
    for row in rows:
        for key, value in flatten_mapping(row).items():
            values_by_field.setdefault(key, []).append(value)
    profiles: dict[str, FieldProfile] = {}
    for key in sorted(values_by_field):
        values = values_by_field[key]
        types = tuple(sorted({_infer_type(value) for value in values}))
        samples = tuple(_sample_values(values, limit=3))
        profiles[key] = FieldProfile(name=key, types=types, samples=samples)
    return profiles


def flatten_mapping(row: Mapping[str, Any], *, prefix: str = "") -> dict[str, Any]:
    """Flatten nested dict fields while keeping list item hints."""

    flattened: dict[str, Any] = {}
    for key, value in row.items():
        path = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, Mapping):
            flattened.update(flatten_mapping(value, prefix=path))
        elif isinstance(value, list):
            flattened[path] = value
            for item in value[:3]:
                if isinstance(item, Mapping):
                    flattened.update(flatten_mapping(item, prefix=f"{path}[]"))
        else:
            flattened[path] = value
    return flattened


def render_schema_markdown(profiles: Sequence[SchemaProfile]) -> str:
    """Render a compact schema summary for operator review."""

    lines = ["# API Probe Schema Summary", ""]
    for profile in profiles:
        comparison = profile.expected_field_comparison
        lines.extend(
            [
                f"## {profile.source_name}",
                "",
                f"- top_level_keys: {', '.join(profile.top_level_keys) or '(none)'}",
                f"- selected_item_path: {profile.selected_item_path or '(none)'}",
                f"- item_count: {profile.item_count}",
                f"- missing_expected_fields: {', '.join(comparison.get('missing_expected_fields', ())) or '(none)'}",
                f"- unexpected_fields: {', '.join(comparison.get('unexpected_fields', ())) or '(none)'}",
                "",
                "| field | types | samples |",
                "| --- | --- | --- |",
            ]
        )
        for field_profile in profile.fields[:40]:
            samples = ", ".join(str(item) for item in field_profile.samples)
            lines.append(f"| `{field_profile.name}` | {', '.join(field_profile.types)} | {samples} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _path_rank(path: str) -> int:
    lowered = path.lower()
    if lowered.endswith("items.item") or lowered.endswith(".item"):
        return 4
    if lowered.endswith("list"):
        return 3
    if "output" in lowered or "data" in lowered:
        return 2
    return 1


def _infer_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool_like"
    if isinstance(value, int) and not isinstance(value, bool):
        return "int_like"
    if isinstance(value, float):
        return "float_like"
    if isinstance(value, (date, datetime)):
        return "date_like"
    if isinstance(value, str):
        text = value.strip().replace(",", "")
        if not text:
            return "null"
        if _looks_date_like(text):
            return "date_like"
        if text.lower() in {"true", "false", "y", "n", "yes", "no", "있음", "없음"}:
            return "bool_like"
        if re.fullmatch(r"[-+]?\d+", text):
            return "int_like"
        if re.fullmatch(r"[-+]?\d+\.\d+", text):
            return "float_like"
        return "str"
    if isinstance(value, list):
        return "list"
    if isinstance(value, Mapping):
        return "object"
    return type(value).__name__


def _looks_date_like(text: str) -> bool:
    return bool(re.fullmatch(r"\d{8}", text) or re.fullmatch(r"\d{4}-\d{2}-\d{2}", text))


def _sample_values(values: Sequence[Any], *, limit: int) -> list[Any]:
    samples: list[Any] = []
    for value in values:
        if value in samples:
            continue
        samples.append(value)
        if len(samples) >= limit:
            break
    return samples


__all__ = [
    "FieldProfile",
    "SchemaProfile",
    "collect_field_profiles",
    "find_list_candidates",
    "flatten_mapping",
    "load_raw_payload",
    "profile_payload",
    "render_schema_markdown",
    "select_item_rows",
]
