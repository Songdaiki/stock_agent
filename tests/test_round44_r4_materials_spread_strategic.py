import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round44_r4_report import build_parser
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round44_r4_materials_spread_strategic import (
    ROUND44_CASE_CANDIDATES,
    ROUND44_PRICE_FIELDS,
    ROUND44_SCORE_TARGETS,
    render_round44_green_guardrail_markdown,
    render_round44_price_validation_plan_markdown,
    render_round44_summary_markdown,
    round44_case_candidate_rows,
    round44_case_records,
    round44_price_field_rows,
    round44_score_profile_rows,
    round44_stage_date_rows,
    round44_summary,
    target_for,
    write_round44_r4_reports,
)


class Round44R4MaterialsSpreadStrategicTests(unittest.TestCase):
    def test_round44_targets_cover_r4_archetypes(self):
        labels = {target.target_id for target in ROUND44_SCORE_TARGETS}

        self.assertEqual(len(labels), 13)
        self.assertIn("REFINING_OIL_SPREAD", labels)
        self.assertIn("CHEMICAL_SPREAD", labels)
        self.assertIn("RARE_METALS_STRATEGIC_MATERIALS", labels)
        self.assertIn("LITHIUM_BATTERY_RAW_MATERIAL", labels)
        self.assertIn("GENERAL_TRADING_RESOURCE_INFRA", labels)
        self.assertIn("ENERGY_UTILITY_LNG_GAS", labels)
        for target in ROUND44_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.MATERIALS_SPREAD_STRATEGIC)
            self.assertFalse(target.production_scoring_changed)

    def test_chemical_and_speculative_materials_are_redteam_first(self):
        chemical = target_for("CHEMICAL_SPREAD")
        advanced = target_for("ADVANCED_MATERIAL_SPECULATIVE_THEME")

        self.assertIsNotNone(chemical)
        self.assertIsNotNone(advanced)
        assert chemical is not None
        assert advanced is not None
        self.assertEqual(chemical.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("china_middle_east_capacity_glut", chemical.red_flags)
        self.assertIn("spread_reversal", chemical.red_flags)
        self.assertEqual(advanced.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("paper_only", advanced.red_flags)
        self.assertIn("no_revenue", advanced.red_flags)

    def test_rare_metals_and_trading_houses_are_watch_to_green_not_auto_green(self):
        rare = target_for("RARE_METALS_STRATEGIC_MATERIALS")
        trading = target_for("GENERAL_TRADING_RESOURCE_INFRA")

        self.assertIsNotNone(rare)
        self.assertIsNotNone(trading)
        assert rare is not None
        assert trading is not None
        self.assertEqual(rare.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("offtake_contract", rare.green_conditions)
        self.assertIn("price_floor", rare.green_conditions)
        self.assertEqual(trading.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("capital_return", trading.green_conditions)

    def test_case_records_validate_and_keep_price_backfill_open(self):
        records = round44_case_records()

        self.assertEqual(len(records), len(ROUND44_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("theme_label_is_not_score_evidence", record.green_guardrails)
            self.assertIn("commodity_price_is_not_structural_evidence", record.green_guardrails)

    def test_required_round44_cases_are_present_with_stage_dates(self):
        records = {record.case_id: record for record in round44_case_records()}

        self.assertIn("mp_materials_dod_apple_offtake_case", records)
        self.assertEqual(records["mp_materials_dod_apple_offtake_case"].case_type, "success_candidate")
        self.assertEqual(records["mp_materials_dod_apple_offtake_case"].price_validation.price_validation_status, "needs_source_date_and_price_backfill")
        self.assertEqual(str(records["korea_zinc_tender_event_premium_case"].stage2_date), "2024-09-13")
        self.assertEqual(records["korea_zinc_tender_event_premium_case"].case_type, "event_premium")
        self.assertEqual(str(records["posco_international_alaska_lng_20y_case"].stage2_date), "2025-12-04")
        self.assertEqual(str(records["sk_innovation_refining_recovery_watch"].stage2_date), "2026-05-13")
        self.assertEqual(str(records["lg_chem_lotte_chemical_oversupply_4c"].stage4c_date), "2025-02-07")
        self.assertEqual(records["lg_chem_lotte_chemical_oversupply_4c"].rerating_result, "thesis_break")
        self.assertEqual(str(records["bhp_iron_ore_profit_dividend_cut_case"].stage4c_date), "2025-08-18")

    def test_score_profile_rows_mark_no_production_change(self):
        rows = {row["target_id"]: row for row in round44_score_profile_rows()}

        self.assertEqual(rows["REFINING_OIL_SPREAD"]["large_sector"], "MATERIALS_SPREAD_STRATEGIC")
        self.assertEqual(rows["REFINING_OIL_SPREAD"]["production_scoring_changed"], "false")
        self.assertIn("stage4c_conditions", rows["RARE_METALS_STRATEGIC_MATERIALS"])
        self.assertEqual(rows["ADVANCED_MATERIAL_SPECULATIVE_THEME"]["posture"], "REDTEAM_FIRST")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round44_stage_date_rows()}
        fields = {row["field"] for row in round44_price_field_rows()}

        self.assertIn("RARE_METALS_STRATEGIC_MATERIALS", rows)
        self.assertIn("production_capacity", rows["RARE_METALS_STRATEGIC_MATERIALS"]["stage3"])
        for field in (
            "stage2_price",
            "MFE_180D",
            "commodity_price_at_stage",
            "spread_metric",
            "offtake_contract_flag",
            "price_floor_flag",
            "tender_offer_flag",
            "supply_glut_flag",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND44_PRICE_FIELDS))

    def test_summary_and_markdown_explain_r4_guardrails(self):
        summary = round44_summary()
        summary_md = render_round44_summary_markdown()
        guardrails = render_round44_green_guardrail_markdown()
        price_plan = render_round44_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 13)
        self.assertEqual(summary["case_candidate_count"], len(ROUND44_CASE_CANDIDATES))
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R4 should separate structural rerating", summary_md)
        self.assertIn("Do not apply these R4 v1.0 weights", guardrails)
        self.assertIn("mp_materials_dod_apple_offtake_case", price_plan)
        self.assertIn("korea_zinc_tender_event_premium_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round44_r4_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r4_round44.jsonl",
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
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND44_CASE_CANDIDATES))

    def test_case_matrix_records_are_not_production_inputs(self):
        rows = round44_case_candidate_rows()

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

    def test_production_scoring_modules_do_not_import_round44_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round44_r4_materials_spread_strategic", text)


if __name__ == "__main__":
    unittest.main()
