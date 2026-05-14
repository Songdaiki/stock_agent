from datetime import date
from pathlib import Path
import unittest

from e2r.models import Market
from e2r.research.report_parser import parse_research_report_file, parse_research_report_text


ROOT = Path(__file__).resolve().parents[1]


class ResearchReportParserTests(unittest.TestCase):
    def test_korean_report_fixture_extracts_numeric_and_keyword_fields(self):
        result = parse_research_report_file(
            ROOT / "tests/fixtures/reports/hd_hyundai_electric_2023_07_27.txt",
            symbol="267260",
            market=Market.KR,
        )

        report = result.report
        fields = result.parsed_fields

        self.assertEqual(report.publish_date, date(2023, 7, 27))
        self.assertEqual(report.broker, "HistoricalBroker")
        self.assertEqual(report.analyst, "Fixture Analyst")
        self.assertEqual(report.current_price, 69600)
        self.assertEqual(report.target_price, 95000)
        self.assertEqual(report.target_revision_pct, 25)
        self.assertEqual(report.fy1_op, 620000)
        self.assertEqual(report.fy2_eps, 15800)
        self.assertEqual(report.est_per, 6.3)
        self.assertEqual(report.order_backlog_to_sales, 155)
        self.assertEqual(report.capa_increase_pct, 35)
        self.assertTrue(report.asp_increase_mentioned)
        self.assertTrue(report.lead_time_mentioned)
        self.assertTrue(report.shortage_mentioned)
        self.assertIn("수주잔고 확대", report.investment_points)
        self.assertEqual(result.evidence.source_type, "research_report")
        self.assertGreater(fields["parser_confidence"], 0.7)

    def test_qualitative_sector_fields_are_extracted_without_numeric_fabrication(self):
        text = """2024.05.16
제목: 삼양식품 Review
불닭 수출 비중 확대와 해외 채널 확장으로 반복 수요가 확인된다.
ASP 상승과 고마진 믹스 개선으로 OPM 개선이 이어진다.
"""
        result = parse_research_report_text(
            symbol="003230",
            market=Market.KR,
            text=text,
            metadata={"publish_date": date(2024, 5, 16), "as_of_date": date(2024, 5, 16)},
        )
        fields = result.parsed_fields

        self.assertTrue(fields["export_channel_expansion"])
        self.assertTrue(fields["overseas_channel_expansion"])
        self.assertTrue(fields["recurring_consumer_demand"])
        self.assertTrue(fields["pricing_power_mentioned"])
        self.assertNotIn("export_growth_pct", fields)

    def test_memory_qualitative_fields_are_extracted(self):
        text = """2024.04.01
제목: 삼성전자 메모리 리레이팅
HBM 수요 증가와 메모리 가격 상승, 공급조절이 확인된다.
"""
        result = parse_research_report_text(
            symbol="005930",
            market=Market.KR,
            text=text,
            metadata={"publish_date": date(2024, 4, 1), "as_of_date": date(2024, 4, 1)},
        )
        fields = result.parsed_fields

        self.assertTrue(fields["hbm_demand_mentioned"])
        self.assertTrue(fields["memory_price_increase_mentioned"])
        self.assertTrue(fields["supply_discipline_mentioned"])


if __name__ == "__main__":
    unittest.main()
