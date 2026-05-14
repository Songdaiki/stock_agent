from datetime import date
from pathlib import Path
import tempfile
import unittest

from e2r.backtest.historical_official_store import HistoricalOfficialStore
from e2r.models import Market
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.sector_mapper import map_sector
from e2r.sector.taxonomy import build_taxonomy_from_instruments, load_sector_taxonomy, write_sector_taxonomy


class SectorTaxonomyTests(unittest.TestCase):
    def test_taxonomy_maps_fixture_universe(self):
        instruments = HistoricalOfficialStore().load_universe(date(2026, 5, 14), Market.KR)
        rows = build_taxonomy_from_instruments(instruments)

        self.assertGreaterEqual(len(rows), 13)
        by_symbol = {row.symbol: row for row in rows}
        self.assertEqual(by_symbol["267260"].primary_archetype, E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL)
        self.assertEqual(by_symbol["003230"].primary_archetype, E2RArchetype.EXPORT_RECURRING_CONSUMER)
        self.assertEqual(by_symbol["257720"].primary_archetype, E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION)
        self.assertNotEqual(by_symbol["005930"].primary_archetype, E2RArchetype.GENERIC_UNCLASSIFIED)

    def test_round_trip_taxonomy_csv(self):
        instruments = HistoricalOfficialStore().load_universe(date(2026, 5, 14), Market.KR)
        rows = build_taxonomy_from_instruments(instruments)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "taxonomy.csv"
            write_sector_taxonomy(rows, path)
            loaded = load_sector_taxonomy(path)

        self.assertEqual(len(loaded), len(rows))
        self.assertEqual(loaded[0].symbol, rows[0].symbol)

    def test_archetype_mapping_covers_at_least_20_sector_families(self):
        examples = {
            "전력기기": E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,
            "방산": E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,
            "조선": E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG,
            "음식료": E2RArchetype.EXPORT_RECURRING_CONSUMER,
            "화장품": E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,
            "반도체": E2RArchetype.MEMORY_HBM_CAPACITY,
            "반도체장비": E2RArchetype.SEMI_EQUIPMENT_CAPEX,
            "2차전지": E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT,
            "화학": E2RArchetype.COMMODITY_SPREAD,
            "해운": E2RArchetype.SHIPPING_FREIGHT_CYCLE,
            "자동차": E2RArchetype.AUTO_MOBILITY_COMPONENTS,
            "로봇": E2RArchetype.ROBOTICS_FACTORY_AUTOMATION,
            "인터넷": E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
            "게임": E2RArchetype.GAME_CONTENT_IP,
            "은행": E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
            "바이오": E2RArchetype.BIOTECH_REGULATORY,
            "의료기기": E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT,
            "유통": E2RArchetype.RETAIL_DOMESTIC_CONSUMER,
            "건설": E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT,
            "전력": E2RArchetype.UTILITIES_REGULATED_TARIFF,
            "지주": E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE,
            "구조조정": E2RArchetype.TURNAROUND_COST_RESTRUCTURING,
            "진단키트": E2RArchetype.ONE_OFF_EVENT_DEMAND,
            "테마": E2RArchetype.THEME_VALUATION_OVERHEAT,
        }

        for sector, expected in examples.items():
            with self.subTest(sector=sector):
                mapping = map_sector(symbol="TEST", company_name=f"{sector} 테스트", sector_raw=sector)
                self.assertEqual(mapping.primary_archetype, expected)


if __name__ == "__main__":
    unittest.main()
