"""Peer-group helpers for sector taxonomy rows."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from e2r.sector.taxonomy import SectorTaxonomyRow


@dataclass(frozen=True)
class PeerGroups:
    """Symbol lookup maps by raw sector, custom sector, and archetype."""

    by_sector: dict[str, tuple[str, ...]]
    by_custom_sector: dict[str, tuple[str, ...]]
    by_archetype: dict[str, tuple[str, ...]]

    def peers_for_symbol(self, symbol: str, rows: Iterable[SectorTaxonomyRow]) -> tuple[str, ...]:
        row_by_symbol = {row.symbol: row for row in rows}
        row = row_by_symbol.get(symbol)
        if row is None:
            return ()
        return self.by_custom_sector.get(row.sector_custom) or self.by_archetype.get(row.primary_archetype.value, ())


def build_peer_groups(rows: Iterable[SectorTaxonomyRow]) -> PeerGroups:
    sector: dict[str, list[str]] = defaultdict(list)
    custom: dict[str, list[str]] = defaultdict(list)
    archetype: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        sector[row.sector_raw or "unknown"].append(row.symbol)
        custom[row.sector_custom or "unknown"].append(row.symbol)
        archetype[row.primary_archetype.value].append(row.symbol)
    return PeerGroups(
        by_sector={key: tuple(sorted(value)) for key, value in sector.items()},
        by_custom_sector={key: tuple(sorted(value)) for key, value in custom.items()},
        by_archetype={key: tuple(sorted(value)) for key, value in archetype.items()},
    )


__all__ = ["PeerGroups", "build_peer_groups"]
