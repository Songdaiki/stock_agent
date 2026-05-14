from datetime import date
import unittest

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.peer_normalizer import PeerMetricRow, SectorPeerNormalizer
from e2r.sector.taxonomy import SectorTaxonomyRow


def _row(symbol: str, sector: str, archetype: E2RArchetype) -> SectorTaxonomyRow:
    return SectorTaxonomyRow(
        symbol=symbol,
        company_name=symbol,
        market="KR",
        exchange="KRX",
        listed_date=date(2020, 1, 1),
        sector_raw=sector,
        industry_raw="",
        sector_custom=sector,
        sector_source="test",
        sector_confidence=0.9,
        primary_archetype=archetype,
        secondary_archetypes=(),
        business_keywords=(),
        product_keywords=(),
        mapping_reason="test",
    )


class SectorPeerNormalizerTests(unittest.TestCase):
    def test_peer_normalizer_computes_percentile_and_fallback_reason(self):
        rows = (
            _row("A", "전력기기", E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL),
            _row("B", "전력기기", E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL),
            _row("C", "반도체", E2RArchetype.MEMORY_HBM_CAPACITY),
            _row("D", "반도체", E2RArchetype.MEMORY_HBM_CAPACITY),
        )
        metrics = (
            PeerMetricRow("A", {"eps_growth": 10, "price_strength": 20}),
            PeerMetricRow("B", {"eps_growth": 20, "price_strength": 40}),
            PeerMetricRow("C", {"eps_growth": 30, "price_strength": 60}),
            PeerMetricRow("D", {"eps_growth": 40, "price_strength": 80}),
        )

        result = SectorPeerNormalizer(rows, min_peer_count=3).normalize("A", metrics)

        self.assertEqual(result.percentile_source, "market")
        self.assertEqual(result.fallback_reason, "sector_and_archetype_peer_count_below_minimum")
        self.assertEqual(result.peer_count, 4)
        self.assertEqual(result.percentiles["sector_eps_growth_percentile"], 25.0)


if __name__ == "__main__":
    unittest.main()
