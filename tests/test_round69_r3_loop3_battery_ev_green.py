import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round69_r3_loop3_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round69_r3_loop3_battery_ev_green import (
    ROUND69_CASE_CANDIDATES,
    ROUND69_PRICE_FIELDS,
    ROUND69_SCORE_TARGETS,
    render_round69_green_guardrail_markdown,
    render_round69_price_validation_plan_markdown,
    render_round69_risk_overlay_markdown,
    render_round69_summary_markdown,
    round69_case_candidate_rows,
    round69_case_records,
    round69_price_field_rows,
    round69_score_profile_rows,
    round69_stage_date_rows,
    round69_summary,
    round69_target_for,
    write_round69_r3_loop3_reports,
)


class Round69R3Loop3BatteryEVGreenTests(unittest.TestCase):
    def test_round69_targets_cover_r3_loop3_archetypes_and_overlays(self):
        labels = {target.target_id for target in ROUND69_SCORE_TARGETS}

        self.assertEqual(len(labels), 14)
        for label in (
            "BATTERY_MATERIALS_CAPEX_OVERHEAT",
            "BATTERY_EQUIPMENT_PARTS",
            "BATTERY_RECYCLING_ESS_SHIFT",
            "ESS_LFP_GRID_STORAGE",
            "EV_INFRASTRUCTURE",
            "HYDROGEN_FUEL_CELL_INFRA",
            "SOLAR_TARIFF_SUPPLYCHAIN",
            "RENEWABLE_ENERGY_POLICY",
            "WASTE_RECYCLING_ENVIRONMENT",
            "CARBON_CREDIT_CBAM_COMPLIANCE",
            "DATA_CENTER_WATER_REUSE_INFRA",
            "EV_FIRE_RISK_OVERLAY",
            "BATTERY_HEALTH_TRANSPARENCY_OVERLAY",
            "LITHIUM_CYCLE_OVERLAY",
        ):
            self.assertIn(label, labels)
        for target in ROUND69_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.BATTERY_EV_GREEN)
            self.assertFalse(target.production_scoring_changed)

    def test_new_loop3_canonical_archetypes_exist(self):
        expected = (
            E2RArchetype.ESS_LFP_GRID_STORAGE,
            E2RArchetype.BATTERY_HEALTH_TRANSPARENCY_OVERLAY,
            E2RArchetype.LITHIUM_CYCLE_OVERLAY,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_ess_and_waste_are_green_possible_while_materials_solar_and_health_are_guarded(self):
        ess = round69_target_for("ESS_LFP_GRID_STORAGE")
        waste = round69_target_for("WASTE_RECYCLING_ENVIRONMENT")
        materials = round69_target_for("BATTERY_MATERIALS_CAPEX_OVERHEAT")
        solar = round69_target_for("SOLAR_TARIFF_SUPPLYCHAIN")
        health = round69_target_for("BATTERY_HEALTH_TRANSPARENCY_OVERLAY")

        for target in (ess, waste, materials, solar, health):
            self.assertIsNotNone(target)
        assert ess is not None
        assert waste is not None
        assert materials is not None
        assert solar is not None
        assert health is not None
        self.assertEqual(ess.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("ess_contract_value", ess.green_conditions)
        self.assertIn("gwh_volume", ess.green_conditions)
        self.assertEqual(waste.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("recurring_fcf", waste.green_conditions)
        self.assertEqual(materials.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("customer_contract_cancelled", materials.red_flags)
        self.assertEqual(solar.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("uflpa_detention", solar.red_flags)
        self.assertEqual(health.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertTrue(health.gate_only)
        self.assertEqual(health.score_weight.eps_fcf, "gate")

    def test_lithium_is_cycle_overlay_not_structural_green_by_default(self):
        lithium = round69_target_for("LITHIUM_CYCLE_OVERLAY")

        self.assertIsNotNone(lithium)
        assert lithium is not None
        self.assertEqual(lithium.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertEqual(lithium.score_weight.eps_fcf, "cycle")
        self.assertIn("mine_restart", lithium.red_flags)
        self.assertIn("sodium_ion", lithium.loop3_penalty_axes)

    def test_required_round69_cases_are_present_with_stage_markers(self):
        rows = {row["case_id"]: row for row in round69_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND69_CASE_CANDIDATES))
        self.assertEqual(rows["lg_energy_tesla_lfp_ess_contract_case"]["target_id"], "ESS_LFP_GRID_STORAGE")
        self.assertEqual(rows["lg_energy_tesla_lfp_ess_contract_case"]["stage2_date"], "2025-07-30")
        self.assertEqual(rows["sk_on_flatiron_ess_7_2gwh_case"]["stage2_date"], "2025-09-03")
        self.assertEqual(rows["gm_lg_ultium_ohio_idle_case"]["stage4c_date"], "2026-05-12")
        self.assertEqual(rows["ford_lges_ev_contract_cancel_case"]["stage4c_date"], "2025-12-17")
        self.assertEqual(rows["redwood_recycling_energy_storage_case"]["stage4b_date"], "2025-10-23")
        self.assertEqual(rows["eqt_kj_environment_waste_platform_case"]["case_type"], "structural_success")
        self.assertEqual(rows["hyundai_hydrogen_fuel_cell_plant_case"]["stage4b_date"], "2025-10-30")
        self.assertEqual(rows["qcells_customs_detention_furlough_case"]["stage4c_date"], "2025-11-08")
        self.assertEqual(rows["orsted_sunrise_wind_impairment_case"]["stage4c_date"], "2025-01-20")
        self.assertEqual(rows["lithium_price_86pct_crash_case"]["target_id"], "LITHIUM_CYCLE_OVERLAY")
        self.assertEqual(rows["lithium_price_86pct_crash_case"]["stage4c_date"], "2025-01-13")
        self.assertEqual(rows["lithium_ess_demand_recovery_case"]["case_type"], "cyclical_success")
        self.assertEqual(rows["korea_ev_battery_certification_fire_case"]["stage4c_date"], "2024-08-25")
        self.assertEqual(rows["battery_soh_transparency_case"]["target_id"], "BATTERY_HEALTH_TRANSPARENCY_OVERLAY")

    def test_case_records_validate_and_keep_loop3_guardrails(self):
        records = round69_case_records()

        self.assertEqual(len(records), len(ROUND69_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "BATTERY_EV_GREEN")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("ev_growth_is_not_fcf_evidence", record.green_guardrails)
            self.assertIn("do_not_invent_contract_value_margin_utilization_customer_or_stage_prices", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["eqt_kj_environment_waste_platform_case"].rerating_result, "true_rerating")
        self.assertEqual(by_id["ford_lges_ev_contract_cancel_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["sk_on_flatiron_ess_7_2gwh_case"].score_price_alignment, "evidence_good_but_price_failed")
        self.assertEqual(by_id["lithium_ess_demand_recovery_case"].rerating_result, "cyclical_rerating")
        self.assertIn("soh_validation_failure", by_id["battery_soh_transparency_case"].red_flag_fields)

    def test_score_profile_rows_match_round69_weight_table(self):
        rows = {row["target_id"]: row for row in round69_score_profile_rows()}

        self.assertEqual(rows["BATTERY_MATERIALS_CAPEX_OVERHEAT"]["eps_fcf"], "17")
        self.assertEqual(rows["BATTERY_MATERIALS_CAPEX_OVERHEAT"]["valuation"], "7")
        self.assertEqual(rows["ESS_LFP_GRID_STORAGE"]["eps_fcf"], "22")
        self.assertEqual(rows["ESS_LFP_GRID_STORAGE"]["structural_visibility"], "21")
        self.assertEqual(rows["WASTE_RECYCLING_ENVIRONMENT"]["structural_visibility"], "22")
        self.assertEqual(rows["CARBON_CREDIT_CBAM_COMPLIANCE"]["information_confidence"], "6")
        self.assertEqual(rows["BATTERY_HEALTH_TRANSPARENCY_OVERLAY"]["gate_only"], "true")
        self.assertEqual(rows["LITHIUM_CYCLE_OVERLAY"]["eps_fcf"], "cycle")
        for row in rows.values():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round69_stage_date_rows()}
        fields = {row["field"] for row in round69_price_field_rows()}

        self.assertIn("customer_contract_cancelled", rows["BATTERY_MATERIALS_CAPEX_OVERHEAT"]["stage4c"])
        self.assertIn("ess_contract_value", rows["ESS_LFP_GRID_STORAGE"]["stage2"])
        self.assertIn("soh_validation_failure", rows["BATTERY_RECYCLING_ESS_SHIFT"]["stage4c"])
        self.assertIn("customs_detention", rows["SOLAR_TARIFF_SUPPLYCHAIN"]["stage4c"])
        self.assertIn("impairment", rows["RENEWABLE_ENERGY_POLICY"]["stage4c"])
        self.assertIn("battery_supplier_disclosure", rows["EV_FIRE_RISK_OVERLAY"]["stage4c"])
        self.assertIn("soh_unreliable", rows["BATTERY_HEALTH_TRANSPARENCY_OVERLAY"]["stage4c"])
        self.assertIn("mine_restart_supply_rebound", rows["LITHIUM_CYCLE_OVERLAY"]["stage4c"])
        for field in (
            "ess_contract_value",
            "grid_storage_flag",
            "data_center_storage_flag",
            "ev_model_discontinued_flag",
            "recovery_rate",
            "soh_validation_flag",
            "battery_passport_compliance_flag",
            "battery_grading_cost",
            "catchment_area_population_share",
            "hydrogen_capacity_utilization",
            "grid_connection_delay_flag",
            "underground_parking_regulation_flag",
            "overcharge_prevention_charger_flag",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND69_PRICE_FIELDS))

    def test_summary_and_markdown_explain_r3_loop3_guardrails(self):
        summary = round69_summary()
        summary_md = render_round69_summary_markdown()
        guardrails = render_round69_green_guardrail_markdown()
        overlays = render_round69_risk_overlay_markdown()
        price_plan = render_round69_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 14)
        self.assertEqual(summary["case_candidate_count"], 13)
        self.assertEqual(summary["structural_success_count"], 1)
        self.assertEqual(summary["success_candidate_count"], 4)
        self.assertEqual(summary["cyclical_success_count"], 1)
        self.assertEqual(summary["failed_rerating_count"], 1)
        self.assertEqual(summary["stage4b_case_count"], 2)
        self.assertEqual(summary["stage4c_case_count"], 6)
        self.assertEqual(summary["green_possible_count"], 2)
        self.assertEqual(summary["redteam_first_count"], 4)
        self.assertEqual(summary["gate_only_target_count"], 2)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R3 Loop 3", summary_md)
        self.assertIn("Do not apply R3 Loop-3 v3.0 weights", guardrails)
        self.assertIn("EV_CAPA_FALSE_GREEN", overlays)
        self.assertIn("battery_soh_transparency_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round69_r3_loop3_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r3_loop3_round69.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round69_r3_loop3_v3.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["stage_date_plan"].exists())
            self.assertTrue(paths["green_guardrails"].exists())
            self.assertTrue(paths["risk_overlays"].exists())
            self.assertTrue(paths["price_validation_plan"].exists())
            self.assertTrue(paths["price_fields"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND69_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round69_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round69_r3_loop3_battery_ev_green", text)


if __name__ == "__main__":
    unittest.main()
