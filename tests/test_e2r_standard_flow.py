from datetime import date
from pathlib import Path
import unittest

from e2r.cheap_scan import DataGoKrFSCConnector, KoreaCheapScanSources
from e2r.llm import FakeLLMProvider
from e2r.models import Market
from e2r.pipeline.e2r_standard_flow import DIAGNOSTIC_REPLAY_MODES, E2R_STANDARD, E2RStandardConfig, E2RStandardFlow
from e2r.research.search_budget import SearchBudget
from e2r.research.search_provider import EmptySearchProvider
from e2r.sources import KINDConnector, KRXConnector, OpenDARTConnector


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "data/raw/korea_cheap_scan"
AS_OF = date(2024, 5, 21)


class E2RStandardFlowTests(unittest.TestCase):
    def test_e2r_standard_flow_exists_and_is_default_name(self):
        result = E2RStandardFlow().run(
            E2RStandardConfig(
                as_of_date=AS_OF,
                sources=_sources(),
                universe_limit=2,
                report_radar_enabled=False,
                browser_provider=EmptySearchProvider(),
                free_search_provider=EmptySearchProvider(),
                search_budget=SearchBudget(max_total_queries_per_day=3, max_queries_per_symbol=3),
            )
        )

        self.assertEqual(result.flow_name, E2R_STANDARD)
        self.assertGreaterEqual(result.cheap_scan.instruments_scanned, 1)
        self.assertTrue(result.candidates)
        self.assertIn("official_only", DIAGNOSTIC_REPLAY_MODES)
        self.assertIn("case_fixture", DIAGNOSTIC_REPLAY_MODES)
        self.assertIn("hybrid", DIAGNOSTIC_REPLAY_MODES)

    def test_diagnostic_modes_are_not_default_production_flow(self):
        self.assertEqual(E2RStandardFlow.flow_name, E2R_STANDARD)
        self.assertNotIn(E2R_STANDARD, DIAGNOSTIC_REPLAY_MODES)

    def test_optional_llm_layer_runs_without_overriding_stage(self):
        provider = FakeLLMProvider()
        result = E2RStandardFlow().run(
            E2RStandardConfig(
                as_of_date=AS_OF,
                sources=_sources(),
                universe_limit=2,
                report_radar_enabled=False,
                browser_provider=EmptySearchProvider(),
                free_search_provider=EmptySearchProvider(),
                search_budget=SearchBudget(max_total_queries_per_day=3, max_queries_per_symbol=3),
                llm_enabled=True,
                llm_provider=provider,
            )
        )

        self.assertTrue(result.llm_outputs)
        self.assertTrue(all(item.attempted_stage_override is None for item in result.llm_outputs))


def _sources() -> KoreaCheapScanSources:
    return KoreaCheapScanSources(
        krx=KRXConnector(fixture_root=FIXTURE_ROOT / "krx"),
        opendart=OpenDARTConnector(fixture_root=FIXTURE_ROOT / "opendart"),
        kind=KINDConnector(fixture_root=FIXTURE_ROOT / "kind"),
        fsc=DataGoKrFSCConnector(fixture_root=FIXTURE_ROOT / "data_go_kr_fsc"),
    )


if __name__ == "__main__":
    unittest.main()
