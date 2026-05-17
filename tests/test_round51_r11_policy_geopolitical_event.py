import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round51_r11_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10ThemePosture
from e2r.sector.round51_r11_policy_geopolitical_event import (
    ROUND51_CASE_CANDIDATES,
    ROUND51_SCORE_TARGETS,
    render_round51_event_false_positive_caps_markdown,
    render_round51_green_guardrail_markdown,
    render_round51_price_validation_plan_markdown,
    render_round51_summary_markdown,
    round51_case_candidate_rows,
    round51_case_records,
    round51_price_field_rows,
    round51_score_profile_rows,
    round51_stage_date_rows,
    round51_summary,
    target_for,
    write_round51_r11_reports,
)


class Round51R11PolicyGeopoliticalEventTests(unittest.TestCase):
    def test_round51_targets_cover_r11_archetypes(self):
        labels = {target.target_id for target in ROUND51_SCORE_TARGETS}

        self.assertEqual(len(labels), 11)
        for label in (
            "NORTH_KOREA_POLICY_EVENT",
            "GEOPOLITICAL_RECONSTRUCTION",
            "DISASTER_REBUILD_EVENT",
            "CLIMATE_DISASTER_EVENT",
            "EVENT_DISEASE_PEST_DEMAND",
            "DIAGNOSTICS_INFECTIOUS_EVENT",
            "SPECULATIVE_SCIENCE_THEME",
            "ADVANCED_MATERIAL_SPECULATIVE_THEME",
            "POLICY_LOCAL_THEME",
            "ONE_OFF_EVENT_DEMAND",
            "THEME_VALUATION_OVERHEAT",
        ):
            self.assertIn(label, labels)

    def test_new_r11_canonical_archetypes_exist(self):
        expected = (
            E2RArchetype.NORTH_KOREA_POLICY_EVENT,
            E2RArchetype.GEOPOLITICAL_RECONSTRUCTION,
            E2RArchetype.CLIMATE_DISASTER_EVENT,
            E2RArchetype.EVENT_DISEASE_PEST_DEMAND,
            E2RArchetype.DIAGNOSTICS_INFECTIOUS_EVENT,
            E2RArchetype.SPECULATIVE_SCIENCE_THEME,
            E2RArchetype.ADVANCED_MATERIAL_SPECULATIVE_THEME,
            E2RArchetype.POLICY_LOCAL_THEME,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_event_and_science_targets_are_redteam_first(self):
        north_korea = target_for("NORTH_KOREA_POLICY_EVENT")
        science = target_for("SPECULATIVE_SCIENCE_THEME")
        disease = target_for("EVENT_DISEASE_PEST_DEMAND")
        climate = target_for("CLIMATE_DISASTER_EVENT")

        self.assertIsNotNone(north_korea)
        self.assertIsNotNone(science)
        self.assertIsNotNone(disease)
        self.assertIsNotNone(climate)
        assert north_korea is not None
        assert science is not None
        assert disease is not None
        assert climate is not None
        self.assertEqual(north_korea.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("facility_dismantle", north_korea.red_flags)
        self.assertEqual(science.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("replication_failure", science.red_flags)
        self.assertEqual(disease.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("stockpile_contract", disease.green_conditions)
        self.assertEqual(climate.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)

    def test_required_round51_cases_are_present_with_stage_dates(self):
        rows = {row["case_id"]: row for row in round51_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND51_CASE_CANDIDATES))
        self.assertEqual(rows["bavarian_nordic_us_stockpile_contract_case"]["stage2_date"], "2026-05-11")
        self.assertEqual(rows["bavarian_nordic_mpox_emergency_case"]["stage4b_date"], "2024-08-16")
        self.assertEqual(rows["ukraine_swiss_reconstruction_projects_case"]["stage2_date"], "2025-08-28")
        self.assertEqual(rows["ukraine_telecom_ebrd_ifc_case"]["stage2_date"], "2024-10-10")
        self.assertEqual(rows["north_korea_kumgang_dismantle_case"]["stage4c_date"], "2025-02-13")
        self.assertEqual(rows["lk99_replication_failure_case"]["stage4c_date"], "2023-08-08")
        self.assertEqual(rows["covid_diagnostics_demand_wane_case"]["case_type"], "4c_thesis_break")

    def test_case_records_validate_and_keep_event_green_blocked(self):
        records = round51_case_records()

        self.assertEqual(len(records), len(ROUND51_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.price_validation.price_validation_status, "needs_price_backfill")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("event_news_is_not_green_evidence_alone", record.green_guardrails)
            self.assertIn("contract_budget_revenue_or_recurring_demand_required_for_green", record.green_guardrails)

    def test_score_profile_rows_mark_no_production_change(self):
        rows = round51_score_profile_rows()

        self.assertEqual(len(rows), len(ROUND51_SCORE_TARGETS))
        for row in rows:
            self.assertEqual(row["production_scoring_changed"], "false")
        by_target = {row["target_id"]: row for row in rows}
        self.assertEqual(by_target["NORTH_KOREA_POLICY_EVENT"]["posture"], "REDTEAM_FIRST")
        self.assertEqual(by_target["THEME_VALUATION_OVERHEAT"]["eps_fcf"], "0")
        self.assertEqual(by_target["CLIMATE_DISASTER_EVENT"]["posture"], "WATCH_YELLOW_FIRST")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        stage_rows = {row["target_id"]: row for row in round51_stage_date_rows()}
        price_fields = {row["field"] for row in round51_price_field_rows()}

        self.assertIn("facility_dismantle", stage_rows["NORTH_KOREA_POLICY_EVENT"]["stage4c"])
        self.assertIn("replication_failure", stage_rows["SPECULATIVE_SCIENCE_THEME"]["stage4c"])
        self.assertIn("stockpile_contract", stage_rows["EVENT_DISEASE_PEST_DEMAND"]["stage2"])
        self.assertIn("MFE_5D", price_fields)
        self.assertIn("government_purchase_amount", price_fields)
        self.assertIn("replication_failure_flag", price_fields)
        self.assertIn("facility_dismantle_flag", price_fields)

    def test_summary_and_markdown_explain_r11_guardrails(self):
        summary = round51_summary()
        summary_md = render_round51_summary_markdown()
        guardrails = render_round51_green_guardrail_markdown()
        caps = render_round51_event_false_positive_caps_markdown()
        price_plan = render_round51_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 11)
        self.assertEqual(summary["case_candidate_count"], 11)
        self.assertEqual(summary["success_candidate_count"], 3)
        self.assertEqual(summary["event_premium_count"], 4)
        self.assertEqual(summary["overheat_count"], 1)
        self.assertEqual(summary["stage4b_case_count"], 2)
        self.assertEqual(summary["stage4c_case_count"], 3)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("production_scoring_changed: false", summary_md)
        self.assertIn("Do not apply these R11 v1.0 weights", guardrails)
        self.assertIn("preprints and SNS videos", caps)
        self.assertIn("MFE_5D", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round51_r11_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r11_round51.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round51_r11_v1.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["stage_date_plan"].exists())
            self.assertTrue(paths["green_guardrails"].exists())
            self.assertTrue(paths["event_false_positive_caps"].exists())
            self.assertTrue(paths["price_validation_plan"].exists())
            self.assertTrue(paths["price_fields"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND51_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round51_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round51_r11_policy_geopolitical_event", text)


if __name__ == "__main__":
    unittest.main()
