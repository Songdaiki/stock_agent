import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round41_r1_report import build_parser
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round41_r1_industrial_infra import (
    ROUND41_CASE_CANDIDATES,
    ROUND41_PRICE_FIELDS,
    ROUND41_SCORE_TARGETS,
    render_round41_green_guardrail_markdown,
    render_round41_price_validation_plan_markdown,
    render_round41_summary_markdown,
    round41_case_candidate_rows,
    round41_case_records,
    round41_price_field_rows,
    round41_score_profile_rows,
    round41_stage_date_rows,
    round41_summary,
    target_for,
    write_round41_r1_reports,
)


class Round41R1IndustrialInfraTests(unittest.TestCase):
    def test_round41_targets_cover_r1_archetypes(self):
        labels = {target.target_id for target in ROUND41_SCORE_TARGETS}

        self.assertEqual(len(labels), 12)
        self.assertIn("GRID_TRANSFORMER_SHORTAGE", labels)
        self.assertIn("DEFENSE_GOVERNMENT_BACKLOG", labels)
        self.assertIn("SHIPBUILDING_OFFSHORE_BACKLOG", labels)
        self.assertIn("RAIL_INFRASTRUCTURE", labels)
        self.assertIn("NUCLEAR_SMR_GRID_POLICY", labels)
        self.assertIn("AI_DATA_CENTER_POWER_EQUIPMENT", labels)
        for target in ROUND41_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.INDUSTRIAL_ORDERS_INFRA)
            self.assertFalse(target.production_scoring_changed)

    def test_transformer_and_defense_are_green_possible_with_specific_guards(self):
        transformer = target_for("GRID_TRANSFORMER_SHORTAGE")
        defense = target_for("DEFENSE_GOVERNMENT_BACKLOG")

        self.assertIsNotNone(transformer)
        self.assertIsNotNone(defense)
        assert transformer is not None
        assert defense is not None
        self.assertEqual(transformer.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(transformer.score_weight.structural_visibility, 25)
        self.assertEqual(transformer.score_weight.bottleneck_pricing, 23)
        self.assertIn("lead_time_extended", transformer.green_conditions)
        self.assertIn("capa_normalization", transformer.red_flags)
        self.assertEqual(defense.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(defense.score_weight.capital_allocation, 3)
        self.assertIn("dilution", defense.red_flags)

    def test_policy_reconstruction_and_smart_factory_are_watch_not_green(self):
        reconstruction = target_for("GEOPOLITICAL_RECONSTRUCTION")
        automation = target_for("SMART_FACTORY_AUTOMATION")

        self.assertIsNotNone(reconstruction)
        self.assertIsNotNone(automation)
        assert reconstruction is not None
        assert automation is not None
        self.assertEqual(reconstruction.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("actual_contract_missing", reconstruction.red_flags)
        self.assertEqual(automation.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("poc_only", automation.red_flags)

    def test_case_records_validate_and_keep_price_backfill_open(self):
        records = round41_case_records()

        self.assertEqual(len(records), len(ROUND41_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("theme_label_is_not_score_evidence", record.green_guardrails)

    def test_required_round41_cases_are_present_with_stage_dates(self):
        records = {record.case_id: record for record in round41_case_records()}

        self.assertIn("hanwha_aerospace_romania_k9_success_case", records)
        self.assertEqual(str(records["hanwha_aerospace_romania_k9_success_case"].stage2_date), "2024-07-09")
        self.assertEqual(records["hanwha_aerospace_romania_k9_success_case"].case_type, "structural_success")
        self.assertIn("hyundai_rotem_morocco_rail_order_case", records)
        self.assertEqual(str(records["hyundai_rotem_morocco_rail_order_case"].stage2_date), "2025-02-26")
        self.assertEqual(records["nuscale_cfpp_cancel_4c_case"].rerating_result, "thesis_break")
        self.assertEqual(records["geopolitical_reconstruction_no_contract_event_watch"].case_type, "event_premium")

    def test_score_profile_rows_mark_no_production_change(self):
        for row in round41_score_profile_rows():
            self.assertEqual(row["large_sector"], "INDUSTRIAL_ORDERS_INFRA")
            self.assertEqual(row["production_scoring_changed"], "false")
            self.assertIn("stage4c_conditions", row)

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round41_stage_date_rows()}
        fields = {row["field"] for row in round41_price_field_rows()}

        self.assertIn("GRID_TRANSFORMER_SHORTAGE", rows)
        self.assertIn("fy1_fy2_fy3_revision", rows["GRID_TRANSFORMER_SHORTAGE"]["stage3"])
        for field in (
            "stage2_price",
            "MFE_180D",
            "MAE_90D",
            "contract_amount_to_sales",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND41_PRICE_FIELDS))

    def test_summary_and_markdown_explain_r1_guardrails(self):
        summary = round41_summary()
        summary_md = render_round41_summary_markdown()
        guardrails = render_round41_green_guardrail_markdown()
        price_plan = render_round41_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 12)
        self.assertEqual(summary["case_candidate_count"], 15)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("order headlines alone are not enough", summary_md)
        self.assertIn("Do not apply these R1 v1.0 weights", guardrails)
        self.assertIn("hanwha_aerospace_romania_k9_success_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round41_r1_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r1_round41.jsonl",
                score_profile_path=Path(tmp) / "score_profiles.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["stage_date_plan"].exists())
            self.assertTrue(paths["green_guardrails"].exists())
            self.assertTrue(paths["price_validation_plan"].exists())
            self.assertTrue(paths["price_fields"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND41_CASE_CANDIDATES))

    def test_case_matrix_records_are_not_production_inputs(self):
        rows = round41_case_candidate_rows()

        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row["production_input"], "false")

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

    def test_production_scoring_modules_do_not_import_round41_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round41_r1_industrial_infra", text)


if __name__ == "__main__":
    unittest.main()
