import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round70_r4_loop3_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round70_r4_loop3_materials_spread_strategic import (
    ROUND70_CASE_CANDIDATES,
    ROUND70_PRICE_FIELDS,
    ROUND70_SCORE_TARGETS,
    render_round70_green_guardrail_markdown,
    render_round70_price_validation_plan_markdown,
    render_round70_risk_overlay_markdown,
    render_round70_summary_markdown,
    round70_case_candidate_rows,
    round70_case_records,
    round70_price_field_rows,
    round70_score_profile_rows,
    round70_stage_date_rows,
    round70_summary,
    round70_target_for,
    write_round70_r4_loop3_reports,
)


class Round70R4Loop3MaterialsSpreadStrategicTests(unittest.TestCase):
    def test_round70_targets_cover_r4_loop3_archetypes_and_overlays(self):
        labels = {target.target_id for target in ROUND70_SCORE_TARGETS}

        self.assertEqual(len(labels), 16)
        for label in (
            "REFINING_OIL_SPREAD",
            "LUBRICANTS_HIGH_MARGIN_MIX",
            "CHEMICAL_SPREAD",
            "STEEL_METAL_SPREAD",
            "NONFERROUS_STRATEGIC_METALS",
            "COPPER_AI_GRID_STRUCTURAL_DEMAND",
            "RARE_METALS_STRATEGIC_MATERIALS",
            "LITHIUM_BATTERY_RAW_MATERIAL",
            "PRECIOUS_METALS_SAFE_HAVEN_MINERS",
            "GENERAL_TRADING_RESOURCE_INFRA",
            "LNG_ENERGY_TRADING_DISTRIBUTION",
            "PAPER_PACKAGING_CYCLE",
            "ADVANCED_MATERIAL_SPECULATIVE_THEME",
            "SPECULATIVE_SCIENCE_THEME",
            "EVENT_PREMIUM_GOVERNANCE_OVERLAY",
            "COMMODITY_PRICE_4C_OVERLAY",
        ):
            self.assertIn(label, labels)
        for target in ROUND70_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.MATERIALS_SPREAD_STRATEGIC)
            self.assertFalse(target.production_scoring_changed)

    def test_new_loop3_canonical_archetypes_exist(self):
        expected = (
            E2RArchetype.LUBRICANTS_HIGH_MARGIN_MIX,
            E2RArchetype.COPPER_AI_GRID_STRUCTURAL_DEMAND,
            E2RArchetype.EVENT_PREMIUM_GOVERNANCE_OVERLAY,
            E2RArchetype.COMMODITY_PRICE_4C_OVERLAY,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_rare_copper_trading_and_lng_are_green_possible_but_chemicals_and_overlays_are_guarded(self):
        rare = round70_target_for("RARE_METALS_STRATEGIC_MATERIALS")
        copper = round70_target_for("COPPER_AI_GRID_STRUCTURAL_DEMAND")
        trading = round70_target_for("GENERAL_TRADING_RESOURCE_INFRA")
        lng = round70_target_for("LNG_ENERGY_TRADING_DISTRIBUTION")
        chemical = round70_target_for("CHEMICAL_SPREAD")
        event = round70_target_for("EVENT_PREMIUM_GOVERNANCE_OVERLAY")

        for target in (rare, copper, trading, lng, chemical, event):
            self.assertIsNotNone(target)
        assert rare is not None
        assert copper is not None
        assert trading is not None
        assert lng is not None
        assert chemical is not None
        assert event is not None
        self.assertEqual(rare.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("price_floor", rare.green_conditions)
        self.assertIn("offtake_contract", rare.green_conditions)
        self.assertEqual(copper.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("low_cost_production", copper.green_conditions)
        self.assertEqual(trading.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("capital_return", trading.green_conditions)
        self.assertEqual(lng.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("fid_status", lng.green_conditions)
        self.assertEqual(chemical.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("china_middle_east_capacity_glut", chemical.red_flags)
        self.assertTrue(event.gate_only)
        self.assertEqual(event.score_weight.eps_fcf, "gate")

    def test_required_round70_cases_are_present_with_stage_markers(self):
        rows = {row["case_id"]: row for row in round70_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND70_CASE_CANDIDATES))
        self.assertEqual(rows["mp_materials_dod_apple_price_floor_case"]["target_id"], "RARE_METALS_STRATEGIC_MATERIALS")
        self.assertEqual(rows["mp_materials_dod_apple_price_floor_case"]["stage2_date"], "")
        self.assertEqual(rows["china_heavy_rare_earth_export_control_case"]["stage2_date"], "2026-05-13")
        self.assertEqual(rows["posco_international_alaska_lng_20y_case"]["stage2_date"], "2025-12-04")
        self.assertEqual(rows["berkshire_japan_sogo_shosha_case"]["case_type"], "structural_success")
        self.assertEqual(rows["barrick_record_gold_buyback_case"]["stage4b_date"], "2026-05-11")
        self.assertEqual(rows["sk_innovation_refining_recovery_case"]["stage2_date"], "2026-05-13")
        self.assertEqual(rows["copper_ai_grid_demand_case"]["target_id"], "COPPER_AI_GRID_STRUCTURAL_DEMAND")
        self.assertEqual(rows["lg_chem_lotte_chemical_oversupply_case"]["stage4c_date"], "2025-02-07")
        self.assertEqual(rows["lithium_price_86pct_crash_case"]["stage4c_date"], "2025-01-13")
        self.assertEqual(rows["lithium_ess_demand_recovery_case"]["case_type"], "cyclical_success")
        self.assertEqual(rows["bhp_iron_ore_profit_dividend_cut_case"]["stage4c_date"], "2025-02-18")
        self.assertEqual(rows["korea_zinc_tender_offer_event_case"]["target_id"], "EVENT_PREMIUM_GOVERNANCE_OVERLAY")
        self.assertEqual(rows["international_paper_ds_smith_divestment_case"]["stage2_date"], "2025-04-14")
        self.assertEqual(rows["graphene_mxene_superconductor_theme_case"]["case_type"], "overheat")

    def test_case_records_validate_and_keep_loop3_guardrails(self):
        records = round70_case_records()

        self.assertEqual(len(records), len(ROUND70_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "MATERIALS_SPREAD_STRATEGIC")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("commodity_price_is_not_structural_evidence", record.green_guardrails)
            self.assertIn("do_not_invent_spread_offtake_price_floor_fcf_or_stage_prices", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["berkshire_japan_sogo_shosha_case"].rerating_result, "true_rerating")
        self.assertEqual(by_id["korea_zinc_tender_offer_event_case"].rerating_result, "event_premium")
        self.assertEqual(by_id["lg_chem_lotte_chemical_oversupply_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["graphene_mxene_superconductor_theme_case"].score_price_alignment, "price_moved_without_evidence")
        self.assertIn("price_floor", by_id["mp_materials_dod_apple_price_floor_case"].must_have_fields)

    def test_score_profile_rows_match_round70_weight_table(self):
        rows = {row["target_id"]: row for row in round70_score_profile_rows()}

        self.assertEqual(rows["REFINING_OIL_SPREAD"]["eps_fcf"], "20")
        self.assertEqual(rows["CHEMICAL_SPREAD"]["structural_visibility"], "6")
        self.assertEqual(rows["RARE_METALS_STRATEGIC_MATERIALS"]["structural_visibility"], "21")
        self.assertEqual(rows["COPPER_AI_GRID_STRUCTURAL_DEMAND"]["bottleneck_pricing"], "17")
        self.assertEqual(rows["GENERAL_TRADING_RESOURCE_INFRA"]["valuation"], "18")
        self.assertEqual(rows["EVENT_PREMIUM_GOVERNANCE_OVERLAY"]["gate_only"], "true")
        self.assertEqual(rows["COMMODITY_PRICE_4C_OVERLAY"]["eps_fcf"], "gate")
        for row in rows.values():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round70_stage_date_rows()}
        fields = {row["field"] for row in round70_price_field_rows()}

        self.assertIn("inventory_gain_loss_excluded", rows["REFINING_OIL_SPREAD"]["stage2"])
        self.assertIn("china_middle_east_capacity_glut", rows["CHEMICAL_SPREAD"]["stage4c"])
        self.assertIn("tariff_inventory_unwind", rows["COPPER_AI_GRID_STRUCTURAL_DEMAND"]["stage4c"])
        self.assertIn("price_floor", rows["RARE_METALS_STRATEGIC_MATERIALS"]["stage2"])
        self.assertIn("sodium_ion_substitution", rows["LITHIUM_BATTERY_RAW_MATERIAL"]["stage4c"])
        self.assertIn("tender_offer", rows["EVENT_PREMIUM_GOVERNANCE_OVERLAY"]["stage1"])
        for field in (
            "commodity_price_at_stage",
            "inventory_gain_loss",
            "refining_margin",
            "lubricants_mix_ratio",
            "copper_inventory_distortion_flag",
            "tariff_stockpile_flag",
            "offtake_contract_flag",
            "price_floor_flag",
            "government_investment_amount",
            "gold_realized_price",
            "lng_contract_volume_mtpa",
            "fid_status",
            "tender_offer_flag",
            "event_premium_flag",
            "speculative_material_theme_flag",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND70_PRICE_FIELDS))

    def test_summary_and_markdown_explain_r4_loop3_guardrails(self):
        summary = round70_summary()
        summary_md = render_round70_summary_markdown()
        guardrails = render_round70_green_guardrail_markdown()
        overlays = render_round70_risk_overlay_markdown()
        price_plan = render_round70_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 16)
        self.assertEqual(summary["case_candidate_count"], 14)
        self.assertEqual(summary["structural_success_count"], 1)
        self.assertEqual(summary["success_candidate_count"], 3)
        self.assertEqual(summary["cyclical_success_count"], 3)
        self.assertEqual(summary["event_premium_count"], 3)
        self.assertEqual(summary["overheat_count"], 1)
        self.assertEqual(summary["stage4b_case_count"], 3)
        self.assertEqual(summary["stage4c_case_count"], 3)
        self.assertEqual(summary["green_possible_count"], 5)
        self.assertEqual(summary["redteam_first_count"], 5)
        self.assertEqual(summary["gate_only_target_count"], 2)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R4 Loop 3", summary_md)
        self.assertIn("Do not apply R4 Loop-3 v3.0 weights", guardrails)
        self.assertIn("COMMODITY_PRICE_4C", overlays)
        self.assertIn("mp_materials_dod_apple_price_floor_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round70_r4_loop3_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r4_loop3_round70.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round70_r4_loop3_v3.csv",
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
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND70_CASE_CANDIDATES))

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


if __name__ == "__main__":
    unittest.main()
