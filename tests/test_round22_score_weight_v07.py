import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round22_score_weight_report import build_parser
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10ThemePosture
from e2r.sector.round22_score_weight_v07 import (
    ROUND22_CASE_CANDIDATES,
    ROUND22_SCORE_TARGETS,
    render_round22_stage4b_watch_markdown,
    render_round22_summary_markdown,
    round22_case_records,
    round22_score_profile_rows,
    round22_summary,
    target_for,
    write_round22_score_weight_reports,
)


class Round22ScoreWeightV07Tests(unittest.TestCase):
    def test_round22_targets_include_v07_recalibration_families(self):
        labels = {target.target_id for target in ROUND22_SCORE_TARGETS}

        self.assertIn("SECURITIES_BROKERAGE_CYCLE", labels)
        self.assertIn("INSURANCE_UNDERWRITING_CYCLE", labels)
        self.assertIn("RETAIL_ECOMMERCE_LOGISTICS", labels)
        self.assertIn("MEMORY_HBM_CAPACITY", labels)
        self.assertIn("VALUE_UP_SHAREHOLDER_RETURN", labels)

    def test_brokerage_is_watch_first_and_pf_sensitive(self):
        target = target_for("SECURITIES_BROKERAGE_CYCLE")

        self.assertIsNotNone(target)
        assert target is not None
        self.assertEqual(target.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        weights = target.score_weight.as_dict()
        self.assertLess(weights["structural_visibility"], weights["valuation"])
        self.assertIn("pf_loss", target.red_flags)
        self.assertIn("trading_value_collapse", target.stage4c_conditions)

    def test_insurance_emphasizes_valuation_and_capital_return(self):
        target = target_for("INSURANCE_UNDERWRITING_CYCLE")

        self.assertIsNotNone(target)
        assert target is not None
        weights = target.score_weight.as_dict()
        self.assertEqual(weights["valuation"], 25)
        self.assertEqual(weights["capital_allocation"], 10)
        self.assertIn("loss_ratio_stability", target.green_conditions)
        self.assertIn("cyber_operational_risk", target.red_flags)

    def test_hbm_has_4b_crowding_watch_conditions(self):
        target = target_for("MEMORY_HBM_CAPACITY")
        markdown = render_round22_stage4b_watch_markdown()

        self.assertIsNotNone(target)
        assert target is not None
        self.assertEqual(target.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("one_to_two_year_price_surge", target.stage4b_conditions)
        self.assertIn("global_crowding", target.stage4b_conditions)
        self.assertIn("price_only_4b_watch", markdown)

    def test_case_records_validate_and_keep_backfill_open(self):
        records = round22_case_records()

        self.assertEqual(len(records), len(ROUND22_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.price_validation.price_validation_status, "needs_price_backfill")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)

    def test_value_up_does_not_treat_policy_headline_as_green(self):
        target = target_for("VALUE_UP_SHAREHOLDER_RETURN")
        records = {record.case_id: record for record in round22_case_records()}

        self.assertIsNotNone(target)
        assert target is not None
        self.assertIn("policy_headline_only", target.red_flags)
        self.assertEqual(records["buyback_no_cancel_counterexample"].case_type, "failed_rerating")
        self.assertIn("buyback_no_cancel", records["buyback_no_cancel_counterexample"].red_flag_fields)

    def test_score_profile_rows_mark_no_production_change(self):
        for row in round22_score_profile_rows():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_summary_reports_v07_not_production_scoring(self):
        summary = round22_summary()
        markdown = render_round22_summary_markdown()

        self.assertEqual(summary["target_count"], 10)
        self.assertEqual(summary["case_candidate_count"], 40)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("production_scoring_changed: false", markdown)
        self.assertIn("Theme names, case IDs, and policy headlines are not score evidence", markdown)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round22_score_weight_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_v04_round22.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round22_v07.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["green_guardrails"].exists())
            self.assertTrue(paths["stage4b_watch_review"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND22_CASE_CANDIDATES))

    def test_cli_argument_parser_supports_paths(self):
        args = build_parser().parse_args(
            [
                "--output-directory",
                "out",
                "--cases",
                "cases.jsonl",
                "--score-profiles",
                "scores.csv",
            ]
        )

        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.score_profiles, "scores.csv")

    def test_production_scoring_modules_do_not_import_round22_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round22_score_weight_v07", text)


if __name__ == "__main__":
    unittest.main()
