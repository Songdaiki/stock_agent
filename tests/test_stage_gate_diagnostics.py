from datetime import date
import unittest

from e2r.models import ScoreSnapshot
from e2r.red_team import RedTeamAssessment
from e2r.stage_gate_diagnostics import diagnose_stage_gates


class StageGateDiagnosticsTests(unittest.TestCase):
    def test_reports_failed_stage2_and_stage3_gates(self):
        score = ScoreSnapshot(
            symbol="267260",
            as_of_date=date(2023, 8, 1),
            eps_fcf_explosion_score=20,
            earnings_visibility_score=12,
            bottleneck_pricing_score=8,
            market_mispricing_score=10,
            valuation_rerating_score=9,
            capital_allocation_score=1,
            information_confidence_score=2,
            risk_penalty=0,
            total_score=62,
            diagnostic_scores={"revision_score": 100, "contract_quality": 40, "one_off_shortage_risk": 0},
        )

        diag = diagnose_stage_gates(score, RedTeamAssessment.empty("267260", date(2023, 8, 1)))

        self.assertFalse(diag.stage2_gate_passed)
        self.assertFalse(diag.stage3_green_gate_passed)
        self.assertIn("failed_stage2_total_score", diag.failed_gate_names)
        self.assertIn("failed_stage3_bottleneck", diag.failed_gate_names)
        self.assertIn("failed_stage3_contract_quality", diag.failed_gate_names)
        self.assertEqual(diag.values_vs_thresholds["failed_stage3_revision"]["passed"], True)


if __name__ == "__main__":
    unittest.main()
