import tempfile
from pathlib import Path
import unittest

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import E2RCaseRecord, PriceValidation, load_case_library
from e2r.sector.round4_score_price_validation import (
    ROUND4_PRICE_VALIDATION_REQUIRED_FIELDS,
    render_round4_field_contract_markdown,
    round4_alignment_summary,
    round4_rule_for,
    write_round4_score_price_validation_reports,
)


class Round4ScorePriceValidationTests(unittest.TestCase):
    def test_round4_rules_cover_platform_robotics_construction_and_ai_dc(self):
        platform = round4_rule_for(E2RArchetype.PLATFORM_SOFTWARE_INTERNET)
        robotics = round4_rule_for(E2RArchetype.ROBOTICS_FACTORY_AUTOMATION)
        construction = round4_rule_for(E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT)
        ai_dc = round4_rule_for(E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE)

        self.assertIn("arpu_or_take_rate_up", platform.success_requires)
        self.assertIn("revenue_conversion", robotics.success_requires)
        self.assertIn("pf_risk_resolved", construction.success_requires)
        self.assertIn("confirmed_orders", ai_dc.success_requires)
        self.assertIn("Green", construction.green_policy)

    def test_price_validation_contract_contains_round4_path_fields(self):
        markdown = render_round4_field_contract_markdown()

        self.assertIn("peak_return_from_stage3", ROUND4_PRICE_VALIDATION_REQUIRED_FIELDS)
        self.assertIn("time_to_100pct", markdown)
        self.assertIn("false_green", markdown)

    def test_price_validation_parses_and_serializes_new_fields(self):
        validation = PriceValidation.from_mapping(
            {
                "stage3_price": 100,
                "peak_price": 240,
                "peak_return_from_stage3": 140,
                "time_to_50pct": 45,
                "time_to_100pct": 90,
                "time_to_200pct": "",
                "price_validation_status": "price_filled",
            }
        )

        self.assertEqual(validation.peak_return_from_stage3, 140)
        self.assertEqual(validation.time_to_50pct, 45)
        self.assertIsNone(validation.time_to_200pct)
        self.assertEqual(validation.as_dict()["time_to_100pct"], 90)

    def test_case_record_stage_failure_type_validates(self):
        record = E2RCaseRecord.from_mapping(
            {
                "case_id": "round4_schema_case",
                "symbol": "R4",
                "company_name": "라운드4",
                "market": "KR",
                "sector_raw": "테스트",
                "primary_archetype": "PLATFORM_SOFTWARE_INTERNET",
                "expected_group": "success_candidate",
                "case_type": "success_candidate",
                "stage_failure_type": "missed_structural",
                "data_quality": {
                    "official_data_available": True,
                    "report_data_available": True,
                    "price_data_available": False,
                    "stage_dates_confidence": 0.3,
                },
            }
        )

        record.validate()
        self.assertEqual(record.as_dict()["stage_failure_type"], "missed_structural")

    def test_alignment_summary_and_report_writer_work(self):
        records = load_case_library("data/e2r_case_library/cases_v02.jsonl")
        summary = round4_alignment_summary(records)

        self.assertTrue(summary)
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round4_score_price_validation_reports(output_directory=tmp)

            self.assertTrue(paths["rules"].exists())
            self.assertTrue(paths["field_contract"].exists())
            self.assertTrue(paths["alignment_summary"].exists())
            self.assertTrue(paths["stage_failure_matrix"].exists())
            self.assertIn("Round-4 Score-Price", paths["rules"].read_text(encoding="utf-8"))

    def test_production_scoring_modules_do_not_import_round4_matrix(self):
        paths = [
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ]
        for path in paths:
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round4_score_price_validation", text)


if __name__ == "__main__":
    unittest.main()
