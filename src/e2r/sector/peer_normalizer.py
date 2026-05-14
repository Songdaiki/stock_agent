"""Peer percentile normalization design for future sector-aware scoring."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from e2r.sector.taxonomy import SectorTaxonomyRow


METRIC_TO_PERCENTILE_NAME = {
    "eps_growth": "sector_eps_growth_percentile",
    "op_growth": "sector_op_growth_percentile",
    "opm_expansion": "sector_opm_expansion_percentile",
    "fcf_growth": "sector_fcf_growth_percentile",
    "revision": "sector_revision_percentile",
    "price_strength": "sector_price_strength_percentile",
    "valuation_discount": "sector_valuation_discount_percentile",
    "trading_value_spike": "sector_trading_value_spike_percentile",
}


@dataclass(frozen=True)
class PeerMetricRow:
    """One symbol's raw metric values for peer percentile calculation."""

    symbol: str
    metrics: Mapping[str, float]


@dataclass(frozen=True)
class PeerNormalizationResult:
    """Percentiles with fallback metadata."""

    symbol: str
    percentiles: Mapping[str, float]
    peer_count: int
    fallback_reason: str
    percentile_source: str


class SectorPeerNormalizer:
    """Compute peer percentiles with sector -> archetype -> market fallback."""

    def __init__(self, taxonomy_rows: tuple[SectorTaxonomyRow, ...], min_peer_count: int = 5) -> None:
        self.taxonomy_rows = taxonomy_rows
        self.min_peer_count = max(1, min_peer_count)
        self._taxonomy_by_symbol = {row.symbol: row for row in taxonomy_rows}

    def normalize(self, symbol: str, metric_rows: tuple[PeerMetricRow, ...]) -> PeerNormalizationResult:
        metrics_by_symbol = {row.symbol: row.metrics for row in metric_rows}
        target_metrics = metrics_by_symbol.get(symbol, {})
        peer_symbols, source, fallback_reason = self._select_peer_symbols(symbol, metrics_by_symbol)
        percentiles: dict[str, float] = {}
        for metric, output_name in METRIC_TO_PERCENTILE_NAME.items():
            if metric not in target_metrics:
                continue
            peer_values = [metrics_by_symbol[item][metric] for item in peer_symbols if metric in metrics_by_symbol.get(item, {})]
            if not peer_values:
                continue
            percentiles[output_name] = _percentile(float(target_metrics[metric]), peer_values)
        return PeerNormalizationResult(
            symbol=symbol,
            percentiles=percentiles,
            peer_count=len(peer_symbols),
            fallback_reason=fallback_reason,
            percentile_source=source,
        )

    def _select_peer_symbols(self, symbol: str, metrics_by_symbol: Mapping[str, Mapping[str, float]]) -> tuple[tuple[str, ...], str, str]:
        target = self._taxonomy_by_symbol.get(symbol)
        available = set(metrics_by_symbol)
        if target is None:
            return tuple(sorted(available)), "market", "symbol_not_in_taxonomy"

        sector_peers = tuple(
            row.symbol for row in self.taxonomy_rows if row.sector_custom == target.sector_custom and row.symbol in available
        )
        if len(sector_peers) >= self.min_peer_count:
            return sector_peers, "sector", "none"

        archetype_peers = tuple(
            row.symbol for row in self.taxonomy_rows if row.primary_archetype == target.primary_archetype and row.symbol in available
        )
        if len(archetype_peers) >= self.min_peer_count:
            return archetype_peers, "archetype", "sector_peer_count_below_minimum"

        return tuple(sorted(available)), "market", "sector_and_archetype_peer_count_below_minimum"


def _percentile(value: float, peer_values: list[float]) -> float:
    below_or_equal = sum(1 for item in peer_values if item <= value)
    return round(100.0 * below_or_equal / len(peer_values), 3)


__all__ = [
    "METRIC_TO_PERCENTILE_NAME",
    "PeerMetricRow",
    "PeerNormalizationResult",
    "SectorPeerNormalizer",
]
