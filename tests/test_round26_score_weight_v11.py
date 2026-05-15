import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round26_score_weight_report import build_parser
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10ThemePosture
from e2r.sector.round26_score_weight_v11 import (
    ROUND26_CASE_CANDIDATES,
    ROUND26_SCORE_TARGETS,
    render_round26_stage4b_watch_markdown,
    render_round26_summary_markdown,
    round26_case_records,
    round26_score_profile_rows,
    round26_summary,
    target_for,
    write_round26_score_weight_reports,
)


class Round26ScoreWeightV11Tests(unittest.TestCase):
    def test_round26_targets_include_v11_calibration_families(self):
        labels = {target.target_id for target in ROUND26_SCORE_TARGETS}

        self.assertIn("AI_DATA_CENTER_COOLING", labels)
        self.assertIn("MEMORY_HBM_CAPACITY", labels)
        self.assertIn("K_BEAUTY_EXPORT_DISTRIBUTION", labels)
        self.assertIn("DIGITAL_ASSET_TOKENIZATION", labels)
        self.assertIn("HYDROGEN_RENEWABLE", labels)
        self.assertIn("CLOUD_AI_SOFTWARE_INFRA", labels)
        self.assertIn("SECURITY_IDENTITY_DEEPFAKE", labels)
        self.assertIn("CRO_CLINICAL_SERVICE", labels)
        self.assertIn("CONSTRUCTION_BUILDING_MATERIALS", labels)
        self.assertIn("INSURANCE_UNDERWRITING_CYCLE", labels)
        self.assertIn("SECURITIES_BROKERAGE_CYCLE", labels)

    def test_kbeauty_green_possible_but_inventory_and_channel_stuffing_block(self):
        target = target_for("K_BEAUTY_EXPORT_DISTRIBUTION")
        records = {record.case_id: record for record in round26_case_records()}

        self.assertIsNotNone(target)
        assert target is not None
        self.assertEqual(target.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("repeat_orders", target.green_conditions)
        self.assertIn("inventory_receivables_clean", target.green_conditions)
        self.assertIn("channel_stuffing", target.red_flags)
        self.assertIn("receivables", target.red_flags)
        self.assertIn("china_dependency", target.red_flags)
        self.assertEqual(records["channel_stuffing_inventory_receivables_4c"].case_type, "4c_thesis_break")

    def test_digital_asset_tokenization_stays_watch_until_real_economics(self):
        target = target_for("DIGITAL_ASSET_TOKENIZATION")
        records = {record.case_id: record for record in round26_case_records()}

        self.assertIsNotNone(target)
        assert target is not None
        self.assertEqual(target.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("license_or_approval", target.green_conditions)
        self.assertIn("actual_issuance", target.green_conditions)
        self.assertIn("transaction_volume", target.green_conditions)
        self.assertIn("fee_or_spread_revenue", target.green_conditions)
        self.assertEqual(records["stablecoin_regulatory_delay_4c"].case_type, "4c_thesis_break")
        self.assertEqual(records["sto_law_expectation_without_revenue_counterexample"].case_type, "failed_rerating")
        self.assertEqual(records["crypto_theme_no_revenue_counterexample"].case_type, "failed_rerating")

    def test_policy_and_credit_sensitive_targets_are_watch_first(self):
        hydrogen = target_for("HYDROGEN_RENEWABLE")
        construction = target_for("CONSTRUCTION_BUILDING_MATERIALS")

        self.assertIsNotNone(hydrogen)
        self.assertIsNotNone(construction)
        assert hydrogen is not None
        assert construction is not None
        self.assertEqual(hydrogen.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertEqual(construction.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("customs", hydrogen.red_flags)
        self.assertIn("policy", hydrogen.red_flags)
        self.assertIn("pf", construction.red_flags)
        self.assertIn("unsold_inventory", construction.red_flags)

    def test_hbm_and_ai_cooling_keep_green_possible_with_4b_watch(self):
        cooling = target_for("AI_DATA_CENTER_COOLING")
        hbm = target_for("MEMORY_HBM_CAPACITY")
        records = {record.case_id: record for record in round26_case_records()}
        markdown = render_round26_stage4b_watch_markdown()

        self.assertIsNotNone(cooling)
        self.assertIsNotNone(hbm)
        assert cooling is not None
        assert hbm is not None
        self.assertEqual(cooling.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(hbm.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("repeat_service_revenue", cooling.green_conditions)
        self.assertIn("global_crowding", hbm.stage4b_conditions)
        self.assertEqual(records["sk_hynix_hbm_success_case"].case_type, "structural_success")
        self.assertEqual(records["sk_hynix_4b_crowding_watch"].case_type, "4b_watch")
        self.assertIn("price_only_4b_watch", markdown)

    def test_insurance_can_be_green_but_brokerage_is_watch_first(self):
        insurance = target_for("INSURANCE_UNDERWRITING_CYCLE")
        brokerage = target_for("SECURITIES_BROKERAGE_CYCLE")

        self.assertIsNotNone(insurance)
        self.assertIsNotNone(brokerage)
        assert insurance is not None
        assert brokerage is not None
        self.assertEqual(insurance.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(brokerage.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertEqual(insurance.score_weight.valuation, 25)
        self.assertEqual(insurance.score_weight.capital_allocation, 10)
        self.assertIn("shareholder_return_execution", insurance.green_conditions)
        self.assertIn("market_turnover", brokerage.red_flags)
        self.assertIn("pf", brokerage.red_flags)

    def test_case_records_validate_and_keep_backfill_open(self):
        records = round26_case_records()

        self.assertEqual(len(records), len(ROUND26_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.price_validation.price_validation_status, "needs_price_backfill")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)

    def test_score_profile_rows_mark_no_production_change(self):
        for row in round26_score_profile_rows():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_summary_reports_v11_not_production_scoring(self):
        summary = round26_summary()
        markdown = render_round26_summary_markdown()

        self.assertEqual(summary["target_count"], 11)
        self.assertEqual(summary["case_candidate_count"], 40)
        self.assertEqual(summary["success_candidate_count"], 16)
        self.assertEqual(summary["stage4b_case_count"], 1)
        self.assertEqual(summary["stage4c_case_count"], 10)
        self.assertEqual(summary["green_possible_count"], 6)
        self.assertEqual(summary["watch_yellow_first_count"], 5)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("production_scoring_changed: false", markdown)
        self.assertIn("Theme names, case IDs, policies, PoCs, and revenue growth headlines are not score evidence", markdown)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round26_score_weight_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_v08_round26.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round26_v11.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["green_guardrails"].exists())
            self.assertTrue(paths["stage4b_watch"].exists())
            self.assertTrue(paths["risk_boundary"].exists())
            self.assertTrue(paths["price_validation_plan"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND26_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round26_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round26_score_weight_v11", text)


if __name__ == "__main__":
    unittest.main()
