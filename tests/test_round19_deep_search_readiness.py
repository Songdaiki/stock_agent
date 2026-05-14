import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round19_deep_search_readiness_report import build_parser
from e2r.sector.round19_deep_search_readiness import (
    ROUND19_DEEP_SEARCH_TARGETS,
    Round19Priority,
    render_round19_readiness_report,
    round19_readiness_summary,
    round19_target_statuses,
    round19_theme_absorption_summary,
    write_round19_deep_search_readiness_reports,
)
from e2r.sector.case_library import load_case_library


class Round19DeepSearchReadinessTests(unittest.TestCase):
    def test_theme_absorption_is_ready_but_scoring_is_not(self):
        theme = round19_theme_absorption_summary()
        summary = round19_readiness_summary()

        self.assertEqual(theme["raw_theme_tags"], 208)
        self.assertEqual(theme["unmatched_theme_tags"], 0)
        self.assertTrue(theme["theme_absorption_ready"])
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["production_scoring_ready"])
        self.assertEqual(summary["reason"], "theme_absorption_ready_but_case_price_validation_incomplete")

    def test_round19_targets_cover_green_validation_redteam_and_thin_backfill(self):
        targets = {target.target_id: target for target in ROUND19_DEEP_SEARCH_TARGETS}

        self.assertEqual(targets["K_BEAUTY_OEM_ODM_EXPORT"].priority, Round19Priority.GREEN_VALIDATION)
        self.assertEqual(targets["CHEMICAL_SPREAD_OVERSUPPLY"].priority, Round19Priority.REDTEAM_DEFENSE)
        self.assertEqual(targets["WASTE_RECYCLING_ENVIRONMENT"].priority, Round19Priority.THIN_BACKFILL)
        self.assertIn("export_growth", targets["K_BEAUTY_OEM_ODM_EXPORT"].must_have_evidence)
        self.assertIn("china_oversupply", targets["CHEMICAL_SPREAD_OVERSUPPLY"].red_flag_evidence)

    def test_statuses_explain_deep_search_or_price_validation_need(self):
        records = load_case_library("data/e2r_case_library/cases_v03_price_filled.jsonl")
        statuses = {status.target.target_id: status for status in round19_target_statuses(records)}

        self.assertIn(
            statuses["K_BEAUTY_OEM_ODM_EXPORT"].readiness_status,
            {"needs_success_counterexample_deep_search", "needs_price_path_validation", "shadow_profile_ready_for_review"},
        )
        self.assertEqual(statuses["ROBOTICS_REVENUE_CONVERSION"].readiness_status, "needs_success_counterexample_deep_search")
        self.assertGreaterEqual(statuses["CHEMICAL_SPREAD_OVERSUPPLY"].missing_positive_cases, 0)

    def test_report_writer_outputs_round19_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round19_deep_search_readiness_reports(output_directory=Path(tmp) / "out")

            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["targets"].exists())
            self.assertTrue(paths["plan"].exists())
            self.assertTrue(paths["price_gaps"].exists())
            self.assertTrue(paths["blockers"].exists())
            text = paths["summary"].read_text(encoding="utf-8")
            self.assertIn("production_scoring_ready: false", text)
            self.assertIn("ThemeClassifier", text) if "ThemeClassifier" in text else self.assertIn("테마", text)

    def test_summary_keeps_theme_tags_as_routing_not_score_evidence(self):
        markdown = render_round19_readiness_report()

        self.assertIn("테마명이 아니라 실제 증거", markdown)
        self.assertIn("Production StageClassifier/score weight는 변경하지 않는다", markdown)
        self.assertIn("Do not use raw theme tags as score evidence", markdown)

    def test_cli_argument_parser_supports_paths(self):
        args = build_parser().parse_args(
            [
                "--case-library",
                "cases.jsonl",
                "--raw-tags",
                "raw.csv",
                "--theme-map",
                "map.csv",
                "--output-directory",
                "out",
            ]
        )

        self.assertEqual(args.case_library, "cases.jsonl")
        self.assertEqual(args.raw_tags, "raw.csv")
        self.assertEqual(args.theme_map, "map.csv")
        self.assertEqual(args.output_directory, "out")

    def test_production_scoring_modules_do_not_import_round19_readiness(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round19_deep_search_readiness", text)


if __name__ == "__main__":
    unittest.main()
