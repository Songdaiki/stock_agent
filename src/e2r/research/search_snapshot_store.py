"""Point-in-time search result snapshot storage."""

from __future__ import annotations

import json
from dataclasses import dataclass, fields, is_dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from e2r.research.search_provider import SearchResult


@dataclass(frozen=True)
class SearchSnapshot:
    """One stored search result for future point-in-time backtests."""

    query: str
    search_date: date
    title: str
    url: str
    snippet: str | None
    published_at: datetime | None
    fetched_at: datetime | None
    source_type: str
    extracted_text_hash: str | None
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence_ids", tuple(self.evidence_ids))


class SearchSnapshotStore:
    """JSONL-backed search snapshot store."""

    def __init__(self, root: str | Path = "data/search_snapshots") -> None:
        self.root = Path(root)

    def save(self, snapshots: Sequence[SearchSnapshot]) -> Path:
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.root / "search_snapshots.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            for item in snapshots:
                handle.write(json.dumps(_jsonable(item), ensure_ascii=False, sort_keys=True) + "\n")
        return path

    def load(self, *, as_of_date: date | None = None, query: str | None = None) -> tuple[SearchSnapshot, ...]:
        path = self.root / "search_snapshots.jsonl"
        if not path.exists():
            return ()
        rows: list[SearchSnapshot] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            item = search_snapshot_from_mapping(json.loads(line))
            if as_of_date is not None and item.search_date > as_of_date:
                continue
            if query is not None and item.query != query:
                continue
            rows.append(item)
        return tuple(rows)


def snapshot_from_search_result(
    result: SearchResult,
    *,
    query: str,
    search_date: date,
    fetched_at: datetime | None = None,
    source_type: str = "search_result",
    extracted_text_hash: str | None = None,
    evidence_ids: Sequence[str] = (),
) -> SearchSnapshot:
    return SearchSnapshot(
        query=query,
        search_date=search_date,
        title=result.title,
        url=result.url,
        snippet=result.snippet,
        published_at=result.published_at,
        fetched_at=fetched_at,
        source_type=source_type,
        extracted_text_hash=extracted_text_hash,
        evidence_ids=tuple(evidence_ids),
    )


def search_snapshot_from_mapping(row: Mapping[str, Any]) -> SearchSnapshot:
    return SearchSnapshot(
        query=str(row["query"]),
        search_date=date.fromisoformat(str(row["search_date"])),
        title=str(row["title"]),
        url=str(row["url"]),
        snippet=row.get("snippet"),
        published_at=datetime.fromisoformat(str(row["published_at"])) if row.get("published_at") else None,
        fetched_at=datetime.fromisoformat(str(row["fetched_at"])) if row.get("fetched_at") else None,
        source_type=str(row["source_type"]),
        extracted_text_hash=row.get("extracted_text_hash"),
        evidence_ids=tuple(row.get("evidence_ids") or ()),
    )


def _jsonable(value: Any) -> Any:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if is_dataclass(value):
        return {field.name: _jsonable(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


__all__ = [
    "SearchSnapshot",
    "SearchSnapshotStore",
    "search_snapshot_from_mapping",
    "snapshot_from_search_result",
]
