import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round36_score_weight_report import build_parser
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10ThemePosture
from e2r.sector.round36_score_weight_v21 import (
    ROUND36_CASE_CANDIDATES,
    ROUND36_SCORE_TARGETS,
    render_round36_cycle_service_markdown,
    render_round36_grid_optical_power_markdown,
    render_round36_healthcare_event_risk_markdown,
    render_round36_summary_markdown,
    render_round36_validation_plan_markdown,
    round36_case_records,
    round36_score_profile_rows,
    round36_summary,
    target_for,
    write_round36_score_weight_reports,
)


class Round36ScoreWeightV21Tests(unittest.TestCase):
    def test_round36_targets_include_v21_validation_families(self):
        labels = {target.target_id for target in ROUND36_SCORE_TARGETS}

        self.assertEqual(len(labels), 8)
        self.assertIn("GRID_TRANSFORMER_SHORTAGE", labels)
        self.assertIn("ANIMAL_HEALTH_BIOSECURITY", labels)
        self.assertIn("TELEHEALTH_BEHAVIORAL_HEALTH", labels)
        self.assertIn("PRECIOUS_METALS_SAFE_HAVEN_MINERS", labels)
        self.assertIn("SERVICE_KIOSK_SELF_CHECKOUT", labels)
        self.assertIn("OPTICAL_NETWORKING_AI_DATACENTER", labels)
        self.assertIn("AI_GRID_FLEXIBILITY_SOFTWARE", labels)
        self.assertIn("PHARMA_CHANNEL_AND_PRIVACY_RISK", labels)

    def test_grid_and_optical_are_green_possible_with_price_validation_metrics(self):
        grid = target_for("GRID_TRANSFORMER_SHORTAGE")
        optical = target_for("OPTICAL_NETWORKING_AI_DATACENTER")
        markdown = render_round36_grid_optical_power_markdown()
        records = {record.case_id: record for record in round36_case_records()}

        self.assertIsNotNone(grid)
        self.assertIsNotNone(optical)
        assert grid is not None
        assert optical is not None
        self.assertEqual(grid.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(optical.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(grid.validation_group, "green_possible")
        self.assertIn("backlog_growth", grid.green_conditions)
        self.assertIn("mfe_1y", grid.validation_metrics)
        self.assertIn("op_eps_revision", optical.green_conditions)
        self.assertIn("customer_concentration", optical.validation_metrics)
        self.assertEqual(records["us_transformer_shortage_korea_import_success_candidate"].case_type, "success_candidate")
        self.assertEqual(records["ai_datacenter_capex_delay_optical_4c"].case_type, "4c_thesis_break")
        self.assertIn("Power-grid and AI-networking cases can be Green-possible", markdown)

    def test_animal_health_is_event_capped_until_recurring_revenue(self):
        target = target_for("ANIMAL_HEALTH_BIOSECURITY")
        markdown = render_round36_healthcare_event_risk_markdown()
        records = {record.case_id: record for record in round36_case_records()}

        self.assertIsNotNone(target)
        assert target is not None
        self.assertEqual(target.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertEqual(target.validation_group, "cycle_event")
        self.assertIn("government_stockpile", target.green_conditions)
        self.assertIn("one_off_demand", target.red_flags)
        self.assertIn("post_event_drawdown", target.validation_metrics)
        self.assertEqual(records["hpai_poultry_event_oneoff_counterexample"].case_type, "one_off")
        self.assertEqual(records["animal_vaccine_stockpile_candidate"].case_type, "success_candidate")
        self.assertIn("Disease headline alone is one-off event evidence", markdown)

    def test_telehealth_and_pharma_channel_are_gated_by_cac_privacy_and_impairment(self):
        telehealth = target_for("TELEHEALTH_BEHAVIORAL_HEALTH")
        pharma = target_for("PHARMA_CHANNEL_AND_PRIVACY_RISK")
        records = {record.case_id: record for record in round36_case_records()}

        self.assertIsNotNone(telehealth)
        self.assertIsNotNone(pharma)
        assert telehealth is not None
        assert pharma is not None
        self.assertEqual(telehealth.validation_group, "watch_to_green")
        self.assertEqual(pharma.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertEqual(pharma.validation_group, "red_flag")
        self.assertIn("cac", telehealth.red_flags)
        self.assertIn("privacy", telehealth.red_flags)
        self.assertIn("privacy", pharma.red_flags)
        self.assertIn("fda_warning", pharma.red_flags)
        self.assertEqual(records["teladoc_betterhelp_cac_impairment_4c"].case_type, "4c_thesis_break")
        self.assertEqual(records["betterhelp_privacy_ftc_4c"].case_type, "4c_thesis_break")

    def test_precious_metals_and_kiosk_are_not_structural_by_theme_label(self):
        metals = target_for("PRECIOUS_METALS_SAFE_HAVEN_MINERS")
        kiosk = target_for("SERVICE_KIOSK_SELF_CHECKOUT")
        markdown = render_round36_cycle_service_markdown()
        records = {record.case_id: record for record in round36_case_records()}

        self.assertIsNotNone(metals)
        self.assertIsNotNone(kiosk)
        assert metals is not None
        assert kiosk is not None
        self.assertEqual(metals.validation_group, "cycle_event")
        self.assertEqual(kiosk.validation_group, "watch_to_green")
        self.assertIn("aisc_stable_or_down", metals.green_conditions)
        self.assertIn("drawdown_after_commodity_peak", metals.validation_metrics)
        self.assertIn("recurring_revenue_above_hardware", kiosk.stage3_conditions)
        self.assertIn("retailer_retreat", kiosk.red_flags)
        self.assertEqual(records["barrick_record_gold_price_profit_candidate"].case_type, "cyclical_success")
        self.assertEqual(records["gold_price_correction_4b_watch"].case_type, "4b_watch")
        self.assertEqual(records["one_off_kiosk_hardware_sales_counterexample"].case_type, "failed_rerating")
        self.assertIn("commodity and service-automation stories", markdown)

    def test_ai_grid_flexibility_requires_commercialization_not_poc(self):
        target = target_for("AI_GRID_FLEXIBILITY_SOFTWARE")
        records = {record.case_id: record for record in round36_case_records()}

        self.assertIsNotNone(target)
        assert target is not None
        self.assertEqual(target.validation_group, "watch_to_green")
        self.assertIn("utility_or_datacenter_customer", target.green_conditions)
        self.assertIn("recurring_sw_revenue", target.green_conditions)
        self.assertIn("proof_of_concept_only", target.red_flags)
        self.assertIn("contract_to_revenue", target.validation_metrics)
        self.assertEqual(records["ai_datacenter_load_forecasting_candidate"].case_type, "success_candidate")
        self.assertEqual(records["smart_grid_poc_no_revenue_counterexample"].case_type, "failed_rerating")
        self.assertEqual(records["utility_adoption_delay_4c"].case_type, "4c_thesis_break")

    def test_validation_plan_renders_all_groups_and_no_production_change(self):
        plan = render_round36_validation_plan_markdown()
        rows = round36_score_profile_rows()

        self.assertIn("green_possible", plan)
        self.assertIn("watch_to_green", plan)
        self.assertIn("cycle_event", plan)
        self.assertIn("red_flag", plan)
        for row in rows:
            self.assertEqual(row["production_scoring_changed"], "false")
            self.assertIn("validation_group", row)
            self.assertIn("validation_metrics", row)

    def test_case_records_validate_and_keep_backfill_open(self):
        records = round36_case_records()

        self.assertEqual(len(records), len(ROUND36_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.price_validation.price_validation_status, "needs_price_backfill")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_invent_stage_dates_or_prices", record.green_guardrails)

    def test_summary_reports_v21_validation_without_production_scoring(self):
        summary = round36_summary()
        markdown = render_round36_summary_markdown()

        self.assertEqual(summary["target_count"], 8)
        self.assertEqual(summary["case_candidate_count"], 32)
        self.assertEqual(summary["success_candidate_count"], 11)
        self.assertEqual(summary["stage4b_case_count"], 2)
        self.assertEqual(summary["stage4c_case_count"], 7)
        self.assertEqual(summary["green_possible_count"], 2)
        self.assertEqual(summary["watch_yellow_first_count"], 5)
        self.assertEqual(summary["redteam_first_count"], 1)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("production_scoring_changed: false", markdown)
        self.assertIn("explicit price-path validation plans", markdown)

    def test_report_writer_outputs_cases_and_validation_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round36_score_weight_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_v18_round36.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round36_v21.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["green_guardrails"].exists())
            self.assertTrue(paths["validation_plan"].exists())
            self.assertTrue(paths["grid_optical_power"].exists())
            self.assertTrue(paths["healthcare_event_risk"].exists())
            self.assertTrue(paths["cycle_service_review"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND36_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round36_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round36_score_weight_v21", text)


if __name__ == "__main__":
    unittest.main()
