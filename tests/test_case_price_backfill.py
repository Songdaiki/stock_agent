from pathlib import Path
import tempfile
import unittest

from e2r.sector.case_library import E2RCaseRecord, load_case_library
from e2r.sector.case_price_backfill import backfill_case_price_paths


class CasePriceBackfillTests(unittest.TestCase):
    def test_cases_v02_validates_schema(self):
        records = load_case_library("data/e2r_case_library/cases_v02.jsonl")

        self.assertGreaterEqual(len(records), 60)
        first = records[0]
        first.validate()
        self.assertTrue(first.large_sector)
        self.assertTrue(first.must_have_fields)
        self.assertEqual(first.price_validation.price_validation_status, "needs_price_backfill")

    def test_case_library_supports_new_fields(self):
        record = E2RCaseRecord.from_mapping(
            {
                "case_id": "schema_case",
                "symbol": "000001",
                "company_name": "스키마테스트",
                "market": "KR",
                "large_sector": "industrial",
                "sector_raw": "전력기기",
                "primary_archetype": "CONTRACT_BACKLOG_INDUSTRIAL",
                "secondary_archetypes": ["AI_DATA_CENTER_INFRASTRUCTURE"],
                "expected_group": "success_candidate",
                "case_type": "success_candidate",
                "stage1_evidence": ["supply contract"],
                "must_have_fields": ["fy1_eps"],
                "red_flag_fields": ["contract cancellation"],
                "score_price_alignment": "unknown",
                "rerating_result": "unknown",
                "stage_failure_type": "stage2_watch_success",
                "price_validation": {"price_validation_status": "needs_price_backfill"},
                "data_quality": {
                    "official_data_available": True,
                    "report_data_available": True,
                    "price_data_available": False,
                    "stage_dates_confidence": 0.4,
                },
            }
        )

        record.validate()
        self.assertEqual(record.case_type, "success_candidate")
        self.assertEqual(record.secondary_archetypes[0].value, "AI_DATA_CENTER_INFRASTRUCTURE")
        self.assertEqual(record.stage_failure_type, "stage2_watch_success")

    def test_price_backfill_leaves_null_when_price_data_missing(self):
        record = E2RCaseRecord.from_mapping(
            {
                "case_id": "missing_price_case",
                "symbol": "NO_PRICE",
                "company_name": "가격없음",
                "market": "KR",
                "sector_raw": "전력기기",
                "primary_archetype": "CONTRACT_BACKLOG_INDUSTRIAL",
                "expected_group": "structural_success",
                "case_type": "structural_success",
                "stage2_date": "2024-01-01",
                "must_have_fields": ["fy1_eps"],
                "data_quality": {
                    "official_data_available": False,
                    "report_data_available": True,
                    "price_data_available": False,
                    "stage_dates_confidence": 0.5,
                },
            }
        )

        filled = backfill_case_price_paths((record,), price_root="data/historical_official/prices")[0]

        self.assertIsNone(filled.price_validation.stage2_price)
        self.assertEqual(filled.price_validation.price_validation_status, "missing_price_data")

    def test_price_backfill_fills_known_fixture_price(self):
        records = load_case_library("data/e2r_case_library/cases_v02.jsonl")
        hd = next(record for record in records if record.case_id == "hd_hyundai_electric_2023")

        filled = backfill_case_price_paths((hd,), price_root="data/historical_official/prices")[0]

        self.assertEqual(filled.price_validation.stage3_price, 66000)
        self.assertIsNotNone(filled.price_validation.peak_return_from_stage3)
        self.assertEqual(filled.price_validation.price_validation_status, "price_filled")


if __name__ == "__main__":
    unittest.main()
