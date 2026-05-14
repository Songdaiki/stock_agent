import tempfile
from pathlib import Path
import unittest

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round3_extension_matrix import (
    ROUND3_CASE_RECORD_REQUIRED_FIELDS,
    ROUND3_PRIORITY_ARCHETYPES,
    Round3StagePosture,
    round3_case_coverage,
    round3_entry,
    stage_posture_for,
    write_round3_extension_reports,
)


class Round3ExtensionMatrixTests(unittest.TestCase):
    def test_stage_posture_groups_reflect_round3_green_watch_guardrail(self):
        self.assertEqual(
            stage_posture_for(E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE),
            Round3StagePosture.GREEN_ELIGIBLE,
        )
        self.assertEqual(
            stage_posture_for(E2RArchetype.TRAVEL_LEISURE_REOPENING),
            Round3StagePosture.YELLOW_WATCH,
        )
        self.assertEqual(
            stage_posture_for(E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT),
            Round3StagePosture.RED_4B_GUARDRAIL,
        )

    def test_extension_entries_keep_green_policy_specific(self):
        robot = round3_entry(E2RArchetype.ROBOTICS_FACTORY_AUTOMATION)
        ai_dc = round3_entry(E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE)
        biotech = round3_entry(E2RArchetype.BIOTECH_REGULATORY)

        self.assertIn("revenue_conversion", robot.must_have_fields)
        self.assertIn("confirmed_orders", ai_dc.must_have_fields)
        self.assertIn("dilution", biotech.red_flag_fields[-1])
        self.assertTrue(robot.green_restricted)
        self.assertFalse(ai_dc.green_restricted)

    def test_priority_queue_contains_round3_top_12(self):
        self.assertEqual(ROUND3_PRIORITY_ARCHETYPES[0], E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL)
        self.assertIn(E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE, ROUND3_PRIORITY_ARCHETYPES[:12])
        self.assertIn(E2RArchetype.THEME_VALUATION_OVERHEAT, ROUND3_PRIORITY_ARCHETYPES[:12])
        self.assertEqual(round3_entry(E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL).priority_rank, 1)
        self.assertEqual(round3_entry(E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE).priority_rank, 12)

    def test_case_record_field_contract_includes_price_pattern_and_evidence(self):
        self.assertIn("price_pattern", ROUND3_CASE_RECORD_REQUIRED_FIELDS)
        self.assertIn("stage4c_evidence", ROUND3_CASE_RECORD_REQUIRED_FIELDS)
        self.assertIn("red_flag_fields", ROUND3_CASE_RECORD_REQUIRED_FIELDS)

    def test_case_coverage_reports_direct_extension_cases(self):
        records = load_case_library("data/e2r_case_library/cases_v02.jsonl")
        rows = round3_case_coverage(records)
        by_archetype = {row["archetype"]: row for row in rows}

        self.assertGreaterEqual(by_archetype["AI_DATA_CENTER_INFRASTRUCTURE"]["positive_count"], 2)
        self.assertEqual(by_archetype["THEME_VALUATION_OVERHEAT"]["stage_posture"], "RED_4B_GUARDRAIL")
        self.assertIn("must_have_fields", by_archetype["ROBOTICS_FACTORY_AUTOMATION"])

    def test_report_writer_outputs_round3_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round3_extension_reports(output_directory=tmp)

            self.assertTrue(paths["extension_plan"].exists())
            self.assertTrue(paths["stage_posture_matrix"].exists())
            self.assertTrue(paths["case_record_field_contract"].exists())
            self.assertTrue(paths["case_coverage_summary"].exists())
            self.assertIn("Round-3 Extension Archetype Matrix", paths["extension_plan"].read_text(encoding="utf-8"))
            self.assertIn("AI_DATA_CENTER_INFRASTRUCTURE", paths["stage_posture_matrix"].read_text(encoding="utf-8"))

    def test_production_scoring_modules_do_not_import_round3_matrix(self):
        paths = [
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ]
        for path in paths:
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round3_extension_matrix", text)


if __name__ == "__main__":
    unittest.main()
