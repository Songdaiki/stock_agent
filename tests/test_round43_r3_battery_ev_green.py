import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round43_r3_report import build_parser
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round43_r3_battery_ev_green import (
    ROUND43_CASE_CANDIDATES,
    ROUND43_PRICE_FIELDS,
    ROUND43_SCORE_TARGETS,
    render_round43_green_guardrail_markdown,
    render_round43_price_validation_plan_markdown,
    render_round43_summary_markdown,
    round43_case_candidate_rows,
    round43_case_records,
    round43_price_field_rows,
    round43_score_profile_rows,
    round43_stage_date_rows,
    round43_summary,
    target_for,
    write_round43_r3_reports,
)


class Round43R3BatteryEVGreenTests(unittest.TestCase):
    def test_round43_targets_cover_r3_archetypes(self):
        labels = {target.target_id for target in ROUND43_SCORE_TARGETS}

        self.assertEqual(len(labels), 12)
        self.assertIn("BATTERY_MATERIALS_CAPEX_OVERHEAT", labels)
        self.assertIn("BATTERY_RECYCLING_ESS_SHIFT", labels)
        self.assertIn("HYDROGEN_FUEL_CELL_INFRA", labels)
        self.assertIn("SOLAR_TARIFF_SUPPLYCHAIN", labels)
        self.assertIn("WASTE_RECYCLING_ENVIRONMENT", labels)
        self.assertIn("EV_FIRE_RISK_OVERLAY", labels)
        for target in ROUND43_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.BATTERY_EV_GREEN)
            self.assertFalse(target.production_scoring_changed)

    def test_waste_is_green_possible_but_battery_materials_and_solar_are_redteam_first(self):
        waste = target_for("WASTE_RECYCLING_ENVIRONMENT")
        materials = target_for("BATTERY_MATERIALS_CAPEX_OVERHEAT")
        solar = target_for("SOLAR_TARIFF_SUPPLYCHAIN")

        self.assertIsNotNone(waste)
        self.assertIsNotNone(materials)
        self.assertIsNotNone(solar)
        assert waste is not None
        assert materials is not None
        assert solar is not None
        self.assertEqual(waste.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("recurring_fcf", waste.green_conditions)
        self.assertEqual(materials.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("ev_demand_slowdown", materials.red_flags)
        self.assertIn("lithium_price_crash", materials.red_flags)
        self.assertEqual(solar.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("customs_detention", solar.red_flags)

    def test_ess_hydrogen_and_water_reuse_are_watch_to_green_not_green_by_label(self):
        ess = target_for("BATTERY_RECYCLING_ESS_SHIFT")
        hydrogen = target_for("HYDROGEN_FUEL_CELL_INFRA")
        water = target_for("DATA_CENTER_WATER_REUSE_INFRA")

        self.assertIsNotNone(ess)
        self.assertIsNotNone(hydrogen)
        self.assertIsNotNone(water)
        assert ess is not None
        assert hydrogen is not None
        assert water is not None
        self.assertEqual(ess.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("ess_contract", ess.green_conditions)
        self.assertEqual(hydrogen.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("low_utilization", hydrogen.red_flags)
        self.assertEqual(water.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("customer_absent", water.red_flags)

    def test_ev_fire_overlay_is_redteam_gate_only(self):
        overlay = target_for("EV_FIRE_RISK_OVERLAY")

        self.assertIsNotNone(overlay)
        assert overlay is not None
        self.assertEqual(overlay.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertTrue(overlay.gate_only)
        self.assertEqual(overlay.score_weight.eps_fcf, 0)
        self.assertIn("recall", overlay.red_flags)
        self.assertIn("fire_regulation", overlay.red_flags)
        self.assertIn("insurance_cost", overlay.red_flags)

    def test_case_records_validate_and_keep_price_backfill_open(self):
        records = round43_case_records()

        self.assertEqual(len(records), len(ROUND43_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("theme_label_is_not_score_evidence", record.green_guardrails)
            self.assertIn("growth_theme_is_not_fcf_evidence", record.green_guardrails)

    def test_required_round43_cases_are_present_with_stage_dates(self):
        records = {record.case_id: record for record in round43_case_records()}

        self.assertIn("lg_energy_solution_ess_shift_case", records)
        self.assertEqual(str(records["lg_energy_solution_ess_shift_case"].stage2_date), "2025-07-25")
        self.assertEqual(records["lg_energy_solution_ess_shift_case"].score_price_alignment, "evidence_good_but_price_failed")
        self.assertIn("gm_lg_ultium_ohio_ev_slowdown_case", records)
        self.assertEqual(str(records["gm_lg_ultium_ohio_ev_slowdown_case"].stage4c_date), "2026-05-12")
        self.assertEqual(records["gm_lg_ultium_ohio_ev_slowdown_case"].rerating_result, "thesis_break")
        self.assertEqual(str(records["qcells_customs_detention_case"].stage4c_date), "2025-11-08")
        self.assertEqual(str(records["orsted_sunrise_wind_impairment_case"].stage4c_date), "2025-01-20")
        self.assertEqual(records["eqt_kj_environment_waste_platform_case"].case_type, "structural_success")

    def test_score_profile_rows_mark_no_production_change(self):
        rows = {row["target_id"]: row for row in round43_score_profile_rows()}

        self.assertEqual(rows["BATTERY_MATERIALS_CAPEX_OVERHEAT"]["large_sector"], "BATTERY_EV_GREEN")
        self.assertEqual(rows["BATTERY_MATERIALS_CAPEX_OVERHEAT"]["production_scoring_changed"], "false")
        self.assertIn("stage4c_conditions", rows["BATTERY_MATERIALS_CAPEX_OVERHEAT"])
        self.assertEqual(rows["EV_FIRE_RISK_OVERLAY"]["gate_only"], "true")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round43_stage_date_rows()}
        fields = {row["field"] for row in round43_price_field_rows()}

        self.assertIn("BATTERY_MATERIALS_CAPEX_OVERHEAT", rows)
        self.assertIn("fcf_after_capex", rows["BATTERY_MATERIALS_CAPEX_OVERHEAT"]["stage3"])
        for field in (
            "stage2_price",
            "MFE_180D",
            "ev_demand_indicator",
            "customs_detention_flag",
            "project_impairment_flag",
            "carbon_credit_price",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND43_PRICE_FIELDS))

    def test_summary_and_markdown_explain_r3_guardrails(self):
        summary = round43_summary()
        summary_md = render_round43_summary_markdown()
        guardrails = render_round43_green_guardrail_markdown()
        price_plan = render_round43_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 12)
        self.assertEqual(summary["case_candidate_count"], len(ROUND43_CASE_CANDIDATES))
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R3 is a growth-theme sector", summary_md)
        self.assertIn("Do not apply these R3 v1.0 weights", guardrails)
        self.assertIn("lg_energy_solution_ess_shift_case", price_plan)
        self.assertIn("qcells_customs_detention_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round43_r3_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r3_round43.jsonl",
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
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND43_CASE_CANDIDATES))

    def test_case_matrix_records_are_not_production_inputs(self):
        rows = round43_case_candidate_rows()

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

    def test_production_scoring_modules_do_not_import_round43_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round43_r3_battery_ev_green", text)


if __name__ == "__main__":
    unittest.main()
