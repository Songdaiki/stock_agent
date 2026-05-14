from dataclasses import replace
import unittest

from e2r.sector.case_library import E2RCaseRecord, PriceValidation
from e2r.sector.score_price_alignment import evaluate_score_price_alignment


def _record(case_type: str, *, price_validation=None, must_have_fields=("fy1_eps",), stage4c_date=None) -> E2RCaseRecord:
    return E2RCaseRecord.from_mapping(
        {
            "case_id": f"{case_type}_case",
            "symbol": "TEST",
            "company_name": "테스트",
            "market": "KR",
            "sector_raw": "테스트",
            "primary_archetype": "CONTRACT_BACKLOG_INDUSTRIAL",
            "expected_group": case_type,
            "case_type": case_type,
            "stage2_date": "2024-01-01",
            "stage4c_date": stage4c_date,
            "must_have_fields": list(must_have_fields),
            "price_validation": (price_validation or PriceValidation()).as_dict(),
            "data_quality": {
                "official_data_available": True,
                "report_data_available": True,
                "price_data_available": True,
                "stage_dates_confidence": 0.5,
            },
        }
    )


class ScorePriceAlignmentTests(unittest.TestCase):
    def test_one_off_cyclical_and_overheat_are_not_true_rerating(self):
        self.assertEqual(evaluate_score_price_alignment(_record("one_off")).rerating_result, "no_rerating")
        self.assertEqual(evaluate_score_price_alignment(_record("cyclical_success")).rerating_result, "cyclical_rerating")
        self.assertEqual(evaluate_score_price_alignment(_record("overheat")).rerating_result, "theme_overheat")

    def test_event_premium_is_not_true_rerating(self):
        result = evaluate_score_price_alignment(_record("event_premium"))

        self.assertEqual(result.rerating_result, "event_premium")
        self.assertNotEqual(result.rerating_result, "true_rerating")

    def test_structural_success_with_missing_price_remains_unknown(self):
        result = evaluate_score_price_alignment(_record("structural_success"))

        self.assertEqual(result.score_price_alignment, "unknown")
        self.assertNotEqual(result.score_price_alignment, "aligned")

    def test_price_move_without_eps_fcf_evidence_is_marked(self):
        record = _record(
            "structural_success",
            price_validation=PriceValidation(
                stage2_price=100,
                peak_price=180,
                mfe_180d=80,
                price_validation_status="price_filled",
            ),
            must_have_fields=("theme_keyword",),
        )

        result = evaluate_score_price_alignment(record)

        self.assertEqual(result.score_price_alignment, "price_moved_without_evidence")

    def test_stage4c_after_candidate_becomes_thesis_break(self):
        result = evaluate_score_price_alignment(_record("4c_thesis_break", stage4c_date="2024-06-01"))

        self.assertEqual(result.rerating_result, "thesis_break")


if __name__ == "__main__":
    unittest.main()
