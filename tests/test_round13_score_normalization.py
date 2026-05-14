import tempfile
from pathlib import Path
import unittest

from e2r.sector.round10_theme_tag_taxonomy import Round10ThemePosture
from e2r.sector.round13_score_normalization import (
    ROUND13_NORMALIZATION_TARGETS,
    render_round13_summary_markdown,
    round13_policy_groups,
    round13_target_rows,
    target_for,
    write_round13_score_normalization_reports,
)


class Round13ScoreNormalizationTests(unittest.TestCase):
    def test_round13_targets_include_new_score_normalization_families(self):
        labels = {target.sub_archetype for target in ROUND13_NORMALIZATION_TARGETS}

        self.assertIn("BATTERY_RECYCLING_ESS_SHIFT", labels)
        self.assertIn("CDMO_HEALTHCARE_CONTRACT", labels)
        self.assertIn("MEMORY_HBM_CAPACITY_4B_WATCH", labels)
        self.assertIn("AUTO_COMPLETED_VEHICLE_VALUEUP", labels)

    def test_tokenization_is_redteam_first_and_not_production_score_change(self):
        target = target_for("DIGITAL_ASSET_TOKENIZATION")

        self.assertIsNotNone(target)
        assert target is not None
        self.assertEqual(target.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertFalse(target.production_scoring_changed)
        self.assertIn("regulated_revenue", target.green_conditions)
        self.assertIn("no_regulated_revenue", target.red_flags)

    def test_insurance_weight_profile_emphasizes_valuation_and_capital_allocation(self):
        target = target_for("INSURANCE_UNDERWRITING_CYCLE")

        self.assertIsNotNone(target)
        assert target is not None
        weights = target.score_weight.as_dict()
        self.assertEqual(weights["valuation"], 25)
        self.assertEqual(weights["capital_allocation"], 10)
        self.assertIn("loss_ratio_improvement", target.green_conditions)

    def test_hbm_target_records_4b_watch_conditions(self):
        target = target_for("MEMORY_HBM_CAPACITY_4B_WATCH")

        self.assertIsNotNone(target)
        assert target is not None
        self.assertIn("one_to_two_year_price_surge", target.stage4b_conditions)
        self.assertIn("sk_hynix_hbm_4b_watch", target.case_candidates)

    def test_policy_groups_include_green_watch_and_redteam(self):
        groups = round13_policy_groups()

        self.assertIn("INSURANCE_UNDERWRITING_CYCLE", groups[Round10ThemePosture.GREEN_POSSIBLE.value])
        self.assertIn("AUTO_COMPLETED_VEHICLE_VALUEUP", groups[Round10ThemePosture.WATCH_YELLOW_FIRST.value])
        self.assertIn("SOLAR_TARIFF_SUPPLYCHAIN", groups[Round10ThemePosture.REDTEAM_FIRST.value])

    def test_target_rows_mark_no_production_scoring_change(self):
        for row in round13_target_rows():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_report_writer_outputs_round13_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round13_score_normalization_reports(
                output_directory=Path(tmp) / "out",
                score_profile_path=Path(tmp) / "score_weight_profiles_round13.csv",
            )

            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["target_matrix"].exists())
            self.assertTrue(paths["green_policy"].exists())
            self.assertTrue(paths["case_candidate_plan"].exists())
            self.assertTrue(paths["next_plan"].exists())
            self.assertIn("production_scoring_changed: false", paths["summary"].read_text(encoding="utf-8"))

    def test_summary_says_this_is_not_stageclassifier_change(self):
        markdown = render_round13_summary_markdown()

        self.assertIn("not a StageClassifier change", markdown)

    def test_production_scoring_modules_do_not_import_round13_normalization(self):
        paths = [
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ]
        for path in paths:
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round13_score_normalization", text)


if __name__ == "__main__":
    unittest.main()
