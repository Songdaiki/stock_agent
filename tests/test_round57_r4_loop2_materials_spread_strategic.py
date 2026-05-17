import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round57_r4_loop2_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round57_r4_loop2_materials_spread_strategic import (
    ROUND57_CASE_CANDIDATES,
    ROUND57_PRICE_FIELDS,
    ROUND57_SCORE_TARGETS,
    render_round57_green_guardrail_markdown,
    render_round57_price_validation_plan_markdown,
    render_round57_risk_overlay_markdown,
    render_round57_summary_markdown,
    round57_case_candidate_rows,
    round57_case_records,
    round57_price_field_rows,
    round57_score_profile_rows,
    round57_stage_date_rows,
    round57_summary,
    target_for,
    write_round57_r4_loop2_reports,
)


class Round57R4Loop2MaterialsSpreadStrategicTests(unittest.TestCase):
    def test_round57_targets_cover_r4_loop2_archetypes(self):
        labels = {target.target_id for target in ROUND57_SCORE_TARGETS}

        self.assertEqual(len(labels), 13)
        for label in (
            "REFINING_OIL_SPREAD",
            "CHEMICAL_SPREAD",
            "STEEL_METAL_SPREAD",
            "NONFERROUS_STRATEGIC_METALS",
            "RARE_METALS_STRATEGIC_MATERIALS",
            "LITHIUM_BATTERY_RAW_MATERIAL",
            "PRECIOUS_METALS_SAFE_HAVEN_MINERS",
            "ADVANCED_MATERIAL_SPECULATIVE_THEME",
            "PAPER_PACKAGING_CYCLE",
            "AGRI_COMMODITY_INPUTS",
            "LNG_ENERGY_TRADING_DISTRIBUTION",
            "GENERAL_TRADING_RESOURCE_INFRA",
            "ENERGY_UTILITY_LNG_GAS",
        ):
            self.assertIn(label, labels)
        for target in ROUND57_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.MATERIALS_SPREAD_STRATEGIC)
            self.assertFalse(target.production_scoring_changed)

    def test_new_r4_loop2_canonical_archetypes_exist(self):
        expected = (
            E2RArchetype.REFINING_OIL_SPREAD,
            E2RArchetype.CHEMICAL_SPREAD,
            E2RArchetype.STEEL_METAL_SPREAD,
            E2RArchetype.NONFERROUS_STRATEGIC_METALS,
            E2RArchetype.LITHIUM_BATTERY_RAW_MATERIAL,
            E2RArchetype.PRECIOUS_METALS_SAFE_HAVEN_MINERS,
            E2RArchetype.PAPER_PACKAGING_CYCLE,
            E2RArchetype.AGRI_COMMODITY_INPUTS,
            E2RArchetype.LNG_ENERGY_TRADING_DISTRIBUTION,
            E2RArchetype.GENERAL_TRADING_RESOURCE_INFRA,
            E2RArchetype.ENERGY_UTILITY_LNG_GAS,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_rare_metals_lng_and_general_trading_are_watch_to_green_not_default_green(self):
        rare = target_for("RARE_METALS_STRATEGIC_MATERIALS")
        lng = target_for("LNG_ENERGY_TRADING_DISTRIBUTION")
        general = target_for("GENERAL_TRADING_RESOURCE_INFRA")

        assert rare is not None
        assert lng is not None
        assert general is not None
        self.assertEqual(rare.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertEqual(rare.score_weight.structural_visibility, 20)
        self.assertIn("price_floor", rare.green_conditions)
        self.assertIn("offtake_contract", rare.green_conditions)
        self.assertIn("production_capacity", rare.green_conditions)
        self.assertEqual(lng.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("long_term_contract", lng.green_conditions)
        self.assertIn("fid_delay", lng.red_flags)
        self.assertEqual(general.score_weight.valuation, 18)
        self.assertEqual(general.score_weight.capital_allocation, 8)

    def test_chemical_and_advanced_material_are_redteam_first(self):
        chemical = target_for("CHEMICAL_SPREAD")
        advanced = target_for("ADVANCED_MATERIAL_SPECULATIVE_THEME")

        assert chemical is not None
        assert advanced is not None
        self.assertEqual(chemical.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("china_middle_east_capacity_glut", chemical.red_flags)
        self.assertIn("supply_glut", chemical.red_flags)
        self.assertEqual(advanced.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("no_commercialization", advanced.red_flags)
        self.assertIn("paper_only", advanced.red_flags)

    def test_commodity_cycle_targets_remain_watch_yellow_first(self):
        for label in (
            "REFINING_OIL_SPREAD",
            "STEEL_METAL_SPREAD",
            "NONFERROUS_STRATEGIC_METALS",
            "LITHIUM_BATTERY_RAW_MATERIAL",
            "PRECIOUS_METALS_SAFE_HAVEN_MINERS",
            "PAPER_PACKAGING_CYCLE",
            "AGRI_COMMODITY_INPUTS",
            "ENERGY_UTILITY_LNG_GAS",
        ):
            target = target_for(label)
            assert target is not None
            self.assertEqual(target.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)

    def test_required_round57_cases_are_present_with_dates_and_alignment(self):
        rows = {row["case_id"]: row for row in round57_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND57_CASE_CANDIDATES))
        self.assertEqual(rows["mp_materials_dod_apple_price_floor_case"]["stage2_date"], "")
        self.assertEqual(rows["mp_materials_dod_apple_price_floor_case"]["price_validation_status"], "needs_source_date_and_price_backfill")
        self.assertEqual(rows["china_heavy_rare_earth_export_control_case"]["stage2_date"], "2026-05-13")
        self.assertEqual(rows["posco_international_alaska_lng_20y_case"]["stage2_date"], "2025-12-04")
        self.assertEqual(rows["berkshire_japan_sogo_shosha_case"]["stage2_date"], "2025-03-17")
        self.assertEqual(rows["barrick_record_gold_buyback_case"]["stage2_date"], "2026-05-11")
        self.assertEqual(rows["sk_innovation_refining_recovery_case"]["stage2_date"], "2026-05-13")
        self.assertEqual(rows["copper_ai_grid_demand_case"]["stage2_date"], "2025-12-12")
        self.assertEqual(rows["korea_zinc_tender_offer_event_case"]["stage2_date"], "2024-09-13")
        self.assertEqual(rows["ds_smith_international_paper_packaging_case"]["stage2_date"], "2025-04-14")
        self.assertEqual(rows["lg_chem_lotte_chemical_oversupply_case"]["stage4c_date"], "2025-02-07")
        self.assertEqual(rows["lithium_price_86pct_crash_case"]["stage4c_date"], "2025-01-13")
        self.assertEqual(rows["bhp_iron_ore_profit_dividend_cut_case"]["stage4c_date"], "2025-08-18")

    def test_case_records_validate_and_keep_round57_guardrails(self):
        records = round57_case_records()

        self.assertEqual(len(records), len(ROUND57_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("commodity_price_is_not_structural_evidence", record.green_guardrails)
            self.assertIn("do_not_invent_spread_offtake_price_floor_or_stage_prices", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["berkshire_japan_sogo_shosha_case"].rerating_result, "true_rerating")
        self.assertEqual(by_id["korea_zinc_tender_offer_event_case"].score_price_alignment, "price_moved_without_evidence")
        self.assertEqual(by_id["korea_zinc_tender_offer_event_case"].rerating_result, "event_premium")
        self.assertEqual(by_id["lg_chem_lotte_chemical_oversupply_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["advanced_material_speculative_theme_counterexample"].rerating_result, "theme_overheat")

    def test_score_profile_rows_match_round57_weight_table(self):
        rows = {row["target_id"]: row for row in round57_score_profile_rows()}

        self.assertEqual(rows["REFINING_OIL_SPREAD"]["valuation"], "9")
        self.assertEqual(rows["CHEMICAL_SPREAD"]["structural_visibility"], "7")
        self.assertEqual(rows["RARE_METALS_STRATEGIC_MATERIALS"]["structural_visibility"], "20")
        self.assertEqual(rows["RARE_METALS_STRATEGIC_MATERIALS"]["capital_allocation"], "5")
        self.assertEqual(rows["GENERAL_TRADING_RESOURCE_INFRA"]["valuation"], "18")
        self.assertEqual(rows["GENERAL_TRADING_RESOURCE_INFRA"]["capital_allocation"], "8")
        self.assertEqual(rows["ADVANCED_MATERIAL_SPECULATIVE_THEME"]["eps_fcf"], "5")
        self.assertEqual(rows["ADVANCED_MATERIAL_SPECULATIVE_THEME"]["information_confidence"], "3")
        for row in rows.values():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round57_stage_date_rows()}
        fields = {row["field"] for row in round57_price_field_rows()}

        self.assertIn("inventory_loss", rows["REFINING_OIL_SPREAD"]["stage4c"])
        self.assertIn("china_middle_east_capacity_glut", rows["CHEMICAL_SPREAD"]["stage4c"])
        self.assertIn("offtake_contract", rows["RARE_METALS_STRATEGIC_MATERIALS"]["stage2"])
        self.assertIn("mine_restart", rows["LITHIUM_BATTERY_RAW_MATERIAL"]["stage4c"])
        self.assertIn("dividend_cut", rows["STEEL_METAL_SPREAD"]["stage4c"])
        self.assertIn("competition_remedy", rows["PAPER_PACKAGING_CYCLE"]["red_flags"])
        for field in (
            "commodity_price_at_stage",
            "commodity_price_change_90D",
            "refining_margin",
            "chemical_spread",
            "steel_spread",
            "smelting_margin",
            "offtake_contract_flag",
            "price_floor_flag",
            "government_support_flag",
            "tender_offer_flag",
            "event_premium_flag",
            "oversupply_flag",
            "mine_restart_flag",
            "dividend_cut_flag",
            "competition_remedy_flag",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND57_PRICE_FIELDS))

    def test_summary_and_markdown_explain_r4_loop2_guardrails(self):
        summary = round57_summary()
        summary_md = render_round57_summary_markdown()
        guardrails = render_round57_green_guardrail_markdown()
        overlays = render_round57_risk_overlay_markdown()
        price_plan = render_round57_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 13)
        self.assertEqual(summary["case_candidate_count"], 13)
        self.assertEqual(summary["structural_success_count"], 1)
        self.assertEqual(summary["success_candidate_count"], 3)
        self.assertEqual(summary["cyclical_success_count"], 2)
        self.assertEqual(summary["event_premium_count"], 3)
        self.assertEqual(summary["overheat_count"], 1)
        self.assertEqual(summary["stage4b_case_count"], 0)
        self.assertEqual(summary["stage4c_case_count"], 3)
        self.assertEqual(summary["green_possible_count"], 0)
        self.assertEqual(summary["watch_yellow_first_count"], 11)
        self.assertEqual(summary["redteam_first_count"], 2)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R4 Loop 2", summary_md)
        self.assertIn("Do not apply R4 Loop-2 v2.0 weights", guardrails)
        self.assertIn("EVENT_PREMIUM_MISCLASSIFIED", overlays)
        self.assertIn("mp_materials_dod_apple_price_floor_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round57_r4_loop2_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r4_loop2_round57.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round57_r4_loop2_v2.csv",
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
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND57_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round57_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round57_r4_loop2_materials_spread_strategic", text)


if __name__ == "__main__":
    unittest.main()
