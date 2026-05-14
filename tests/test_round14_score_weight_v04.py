import tempfile
from pathlib import Path
import unittest

from e2r.sector.round10_theme_tag_taxonomy import Round10ThemePosture
from e2r.sector.round14_score_weight_v04 import (
    ROUND14_SCORE_WEIGHT_TARGETS,
    render_round14_summary_markdown,
    round14_policy_groups,
    round14_target_rows,
    round14_theme_tag_rows,
    target_for,
    write_round14_score_weight_reports,
)


class Round14ScoreWeightV04Tests(unittest.TestCase):
    def test_round14_targets_include_new_v04_theme_families(self):
        labels = {target.sub_archetype for target in ROUND14_SCORE_WEIGHT_TARGETS}

        self.assertIn("RETAIL_CONVENIENCE_OFFLINE", labels)
        self.assertIn("PAYMENT_FINTECH_INFRA", labels)
        self.assertIn("RENEWABLE_ENERGY_POLICY", labels)
        self.assertIn("EVENT_DISEASE_PEST_DEMAND", labels)
        self.assertIn("AGRI_LIVESTOCK_FOOD_COMMODITY", labels)

    def test_theme_tags_are_search_routing_not_score_inputs(self):
        for row in round14_theme_tag_rows():
            self.assertEqual(row["theme_is_score_input"], "false")

    def test_retail_requires_margin_and_fcf_not_traffic_alone(self):
        target = target_for("RETAIL_CONVENIENCE_OFFLINE")

        self.assertIsNotNone(target)
        assert target is not None
        self.assertIn("opm_improvement", target.must_have_evidence)
        self.assertIn("fcf_improvement", target.must_have_evidence)
        self.assertIn("traffic_only", target.red_flags)
        self.assertEqual(target.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)

    def test_insurance_weight_profile_emphasizes_roe_pbr_and_return(self):
        target = target_for("INSURANCE_UNDERWRITING_CYCLE")

        self.assertIsNotNone(target)
        assert target is not None
        weights = target.score_weight.as_dict()
        self.assertEqual(weights["valuation"], 25)
        self.assertEqual(weights["capital_allocation"], 10)
        self.assertIn("loss_ratio_improvement", target.must_have_evidence)
        self.assertIn("low_pbr_only", target.red_flags)

    def test_payment_and_tokenization_have_different_guardrails(self):
        payment = target_for("PAYMENT_FINTECH_INFRA")
        tokenization = target_for("DIGITAL_ASSET_TOKENIZATION")

        self.assertIsNotNone(payment)
        self.assertIsNotNone(tokenization)
        assert payment is not None
        assert tokenization is not None
        self.assertEqual(payment.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertEqual(tokenization.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("transaction_volume", payment.must_have_evidence)
        self.assertIn("theme_only_tokenization", tokenization.red_flags)

    def test_redteam_first_group_contains_event_and_speculative_science(self):
        groups = round14_policy_groups()

        redteam = groups[Round10ThemePosture.REDTEAM_FIRST.value]
        self.assertIn("EVENT_DISEASE_PEST_DEMAND", redteam)
        self.assertIn("SPECULATIVE_SCIENCE_THEME", redteam)
        self.assertIn("CONSTRUCTION_REAL_ESTATE_CREDIT", redteam)

    def test_target_rows_mark_no_production_scoring_change(self):
        for row in round14_target_rows():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_report_writer_outputs_round14_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round14_score_weight_reports(
                output_directory=Path(tmp) / "out",
                score_profile_path=Path(tmp) / "score_weight_profiles_round14.csv",
                theme_map_path=Path(tmp) / "theme_tag_map_round14.csv",
            )

            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["theme_map"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["target_matrix"].exists())
            self.assertTrue(paths["theme_policy"].exists())
            self.assertTrue(paths["case_candidate_plan"].exists())
            self.assertTrue(paths["next_plan"].exists())
            self.assertIn("production_scoring_changed: false", paths["summary"].read_text(encoding="utf-8"))

    def test_summary_says_theme_tags_are_not_score_inputs(self):
        markdown = render_round14_summary_markdown()

        self.assertIn("theme_tags_are_score_input: false", markdown)
        self.assertIn("not a production score change", markdown)

    def test_production_scoring_modules_do_not_import_round14_matrix(self):
        paths = [
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ]
        for path in paths:
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round14_score_weight_v04", text)


if __name__ == "__main__":
    unittest.main()
