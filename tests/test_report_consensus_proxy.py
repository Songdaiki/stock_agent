from datetime import date
import unittest

from e2r.models import ResearchReport
from e2r.research.report_consensus_proxy import build_report_consensus_proxy


class ReportConsensusProxyTests(unittest.TestCase):
    def test_creates_consensus_and_revision_from_explicit_report_fields(self):
        report = ResearchReport(
            symbol="267260",
            publish_date=date(2023, 7, 27),
            broker="broker",
            title="HD현대일렉트릭 Review",
            as_of_date=date(2023, 8, 1),
            target_price=110000,
            target_revision_pct=37,
            fy1_sales=27000,
            fy1_op=3100,
            fy1_eps=6200,
            fy2_sales=33000,
            fy2_op=4700,
            fy2_eps=9300,
            est_per=9,
            est_pbr=2.2,
        )

        result = build_report_consensus_proxy((report,), as_of_date=date(2023, 8, 1))

        self.assertEqual(len(result.consensus), 2)
        self.assertEqual(result.consensus[0].sales_e, 27000)
        self.assertEqual(result.consensus[1].fiscal_year, 2024)
        self.assertEqual(len(result.consensus_revisions), 1)
        self.assertEqual(result.consensus_revisions[0].target_price_revision_1m, 37)
        self.assertTrue(result.reports[0].parsed_fields["consensus_proxy_created"])

    def test_does_not_create_revision_from_missing_fields(self):
        report = ResearchReport(
            symbol="298040",
            publish_date=date(2023, 5, 15),
            broker="broker",
            title="효성중공업 Review",
            as_of_date=date(2023, 5, 15),
            parsed_fields={},
        )

        result = build_report_consensus_proxy((report,))

        self.assertFalse(result.consensus)
        self.assertFalse(result.consensus_revisions)
        self.assertNotIn("consensus_proxy_created", result.reports[0].parsed_fields)


if __name__ == "__main__":
    unittest.main()
