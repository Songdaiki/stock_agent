"""Korea sector taxonomy rows and CSV/report helpers."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, Mapping

from e2r.models import Instrument, Market
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.sector_mapper import SectorMappingRules, load_mapping_rules, map_sector
from e2r.sources.source_errors import date_value


@dataclass(frozen=True)
class SectorTaxonomyRow:
    """One row in the Korea sector taxonomy map."""

    symbol: str
    company_name: str
    market: str
    exchange: str
    listed_date: date | None
    sector_raw: str
    industry_raw: str
    sector_custom: str
    sector_source: str
    sector_confidence: float
    primary_archetype: E2RArchetype
    secondary_archetypes: tuple[E2RArchetype, ...]
    business_keywords: tuple[str, ...]
    product_keywords: tuple[str, ...]
    mapping_reason: str

    def as_csv_row(self) -> dict[str, str]:
        return {
            "symbol": self.symbol,
            "company_name": self.company_name,
            "market": self.market,
            "exchange": self.exchange,
            "listed_date": self.listed_date.isoformat() if self.listed_date else "",
            "sector_raw": self.sector_raw,
            "industry_raw": self.industry_raw,
            "sector_custom": self.sector_custom,
            "sector_source": self.sector_source,
            "sector_confidence": f"{self.sector_confidence:.3f}",
            "primary_archetype": self.primary_archetype.value,
            "secondary_archetypes": "|".join(item.value for item in self.secondary_archetypes),
            "business_keywords": "|".join(self.business_keywords),
            "product_keywords": "|".join(self.product_keywords),
            "mapping_reason": self.mapping_reason,
        }


TAXONOMY_FIELDS = (
    "symbol",
    "company_name",
    "market",
    "exchange",
    "listed_date",
    "sector_raw",
    "industry_raw",
    "sector_custom",
    "sector_source",
    "sector_confidence",
    "primary_archetype",
    "secondary_archetypes",
    "business_keywords",
    "product_keywords",
    "mapping_reason",
)


def build_taxonomy_from_instruments(
    instruments: Iterable[Instrument],
    *,
    rules: SectorMappingRules | None = None,
) -> tuple[SectorTaxonomyRow, ...]:
    """Build taxonomy rows from Instrument objects."""

    rules = rules or load_mapping_rules()
    rows: list[SectorTaxonomyRow] = []
    for instrument in instruments:
        sector_raw = instrument.sector_custom or instrument.sector_exchange or ""
        mapping = map_sector(
            symbol=instrument.symbol,
            company_name=instrument.name,
            sector_raw=sector_raw,
            industry_raw=instrument.sector_exchange,
            rules=rules,
        )
        rows.append(
            SectorTaxonomyRow(
                symbol=instrument.symbol,
                company_name=instrument.name,
                market=instrument.market.value if isinstance(instrument.market, Market) else str(instrument.market),
                exchange=instrument.exchange,
                listed_date=instrument.listed_date,
                sector_raw=sector_raw,
                industry_raw=instrument.sector_exchange or "",
                sector_custom=mapping.sector_custom,
                sector_source=mapping.source,
                sector_confidence=mapping.confidence,
                primary_archetype=mapping.primary_archetype,
                secondary_archetypes=mapping.secondary_archetypes,
                business_keywords=mapping.business_keywords,
                product_keywords=mapping.product_keywords,
                mapping_reason=mapping.reason,
            )
        )
    return tuple(sorted(rows, key=lambda row: row.symbol))


def write_sector_taxonomy(rows: Iterable[SectorTaxonomyRow], path: str | Path) -> Path:
    """Write taxonomy rows to CSV."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TAXONOMY_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.as_csv_row())
    return target


def load_sector_taxonomy(path: str | Path) -> tuple[SectorTaxonomyRow, ...]:
    """Load taxonomy rows from CSV."""

    target = Path(path)
    if not target.exists():
        return ()
    with target.open("r", encoding="utf-8", newline="") as handle:
        return tuple(_row_from_csv(row) for row in csv.DictReader(handle))


def taxonomy_summary(rows: Iterable[SectorTaxonomyRow], *, full_live_taxonomy_built: bool = False, fixture_only: bool = True) -> dict[str, object]:
    """Return aggregate taxonomy coverage stats."""

    row_tuple = tuple(rows)
    sectors = {row.sector_custom for row in row_tuple if row.sector_custom}
    archetypes = {row.primary_archetype.value for row in row_tuple}
    unmapped = [row for row in row_tuple if row.primary_archetype == E2RArchetype.GENERIC_UNCLASSIFIED]
    return {
        "full_live_taxonomy_built": full_live_taxonomy_built,
        "fixture_only": fixture_only,
        "symbol_count": len(row_tuple),
        "sector_count": len(sectors),
        "archetype_count": len(archetypes),
        "unmapped_count": len(unmapped),
        "sector_distribution": _count_by(row_tuple, lambda row: row.sector_custom),
        "archetype_distribution": _count_by(row_tuple, lambda row: row.primary_archetype.value),
    }


def render_taxonomy_summary(summary: Mapping[str, object]) -> str:
    """Render taxonomy coverage markdown."""

    lines = [
        "# Korea Sector Taxonomy Summary",
        "",
        f"- full_live_taxonomy_built: {summary['full_live_taxonomy_built']}",
        f"- fixture_only: {summary['fixture_only']}",
        f"- mapped symbols: {summary['symbol_count']}",
        f"- mapped sectors: {summary['sector_count']}",
        f"- archetypes used: {summary['archetype_count']}",
        f"- unmapped_count: {summary['unmapped_count']}",
        "",
        "## Archetype Distribution",
    ]
    for key, value in sorted(dict(summary["archetype_distribution"]).items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Sector Distribution"])
    for key, value in sorted(dict(summary["sector_distribution"]).items()):
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Notes",
            "- This taxonomy is metadata for coverage and future score-weight design.",
            "- It is not a candidate-generation input label and does not change StageClassifier thresholds.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_taxonomy_summary(summary: Mapping[str, object], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_taxonomy_summary(summary), encoding="utf-8")
    return target


def _row_from_csv(row: Mapping[str, str]) -> SectorTaxonomyRow:
    return SectorTaxonomyRow(
        symbol=row["symbol"],
        company_name=row["company_name"],
        market=row.get("market") or "KR",
        exchange=row.get("exchange") or "KRX",
        listed_date=date_value(row["listed_date"]) if row.get("listed_date") else None,
        sector_raw=row.get("sector_raw") or "",
        industry_raw=row.get("industry_raw") or "",
        sector_custom=row.get("sector_custom") or "",
        sector_source=row.get("sector_source") or "rule",
        sector_confidence=float(row.get("sector_confidence") or 0),
        primary_archetype=E2RArchetype(row.get("primary_archetype") or E2RArchetype.GENERIC_UNCLASSIFIED.value),
        secondary_archetypes=tuple(
            E2RArchetype(item) for item in (row.get("secondary_archetypes") or "").split("|") if item
        ),
        business_keywords=tuple(item for item in (row.get("business_keywords") or "").split("|") if item),
        product_keywords=tuple(item for item in (row.get("product_keywords") or "").split("|") if item),
        mapping_reason=row.get("mapping_reason") or "",
    )


def _count_by(rows: Iterable[SectorTaxonomyRow], key_func) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        key = str(key_func(row) or "unknown")
        counts[key] = counts.get(key, 0) + 1
    return counts


__all__ = [
    "SectorTaxonomyRow",
    "TAXONOMY_FIELDS",
    "build_taxonomy_from_instruments",
    "load_sector_taxonomy",
    "render_taxonomy_summary",
    "taxonomy_summary",
    "write_sector_taxonomy",
    "write_taxonomy_summary",
]
