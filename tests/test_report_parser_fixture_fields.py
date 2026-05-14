from pathlib import Path
import unittest

from e2r.models import Market
from e2r.research.report_parser import parse_research_report_file


class ReportParserFixtureFieldTests(unittest.TestCase):
    def test_structural_report_fixtures_emit_scoring_fields(self):
        cases = (
            ("267260", "data/report_snapshots/hd_hyundai_electric_20230727.txt", ("fy1_eps", "fy2_eps", "target_revision_pct", "pricing_power_confirmed")),
            ("298040", "data/report_snapshots/hyosung_heavy_20230515.txt", ("fy1_op", "fy2_op", "order_backlog_to_sales", "pricing_power_confirmed")),
            ("103590", "data/report_snapshots/iljin_electric_20231127.txt", ("contract_amount_to_prior_sales", "contract_duration_months", "capa_increase_pct")),
            ("062040", "data/report_snapshots/sanil_electric_20250215.txt", ("fy1_eps", "export_ratio", "us_revenue_ratio", "pricing_power_confirmed")),
            ("003230", "data/report_snapshots/samyang_foods_20240516.txt", ("fy1_eps", "fy2_eps", "target_revision_pct", "pricing_power_confirmed")),
            ("012450", "data/report_snapshots/hanwha_aerospace_20240801.txt", ("contract_amount_to_prior_sales", "contract_duration_months", "order_backlog_to_sales")),
            ("257720", "data/report_snapshots/silicontwo_20240516.txt", ("export_channel_expansion", "overseas_channel_expansion", "recurring_consumer_demand", "fy2_eps")),
            ("005930", "data/report_snapshots/samsung_memory_20240401.txt", ("hbm_demand_mentioned", "memory_price_increase_mentioned", "supply_discipline_mentioned", "fy2_op")),
            ("000660", "data/report_snapshots/sk_hynix_memory_20240401.txt", ("hbm_demand_mentioned", "memory_price_increase_mentioned", "supply_discipline_mentioned", "fy2_eps")),
        )
        for symbol, path, expected_fields in cases:
            with self.subTest(path=path):
                parsed = parse_research_report_file(Path(path), symbol=symbol, market=Market.KR)
                fields = parsed.report.parsed_fields
                for field in expected_fields:
                    self.assertIn(field, fields)
                    self.assertNotIn(fields[field], (None, ""))

    def test_one_off_fixture_marks_shortage_risk(self):
        parsed = parse_research_report_file(
            "data/report_snapshots/seegene_20200814.txt",
            symbol="096530",
            market=Market.KR,
        )

        self.assertEqual(parsed.report.parsed_fields.get("shortage_type"), "one_off")
        self.assertGreaterEqual(parsed.report.parsed_fields.get("one_off_shortage_risk", 0), 90)


if __name__ == "__main__":
    unittest.main()
