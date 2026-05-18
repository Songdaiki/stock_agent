import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round175_r4_loop11_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round175_r4_loop11_materials_spread_strategic import (
    ROUND175_BASE_SCORE_WEIGHTS,
    ROUND175_CASE_CANDIDATES,
    ROUND175_PRICE_FIELDS,
    ROUND175_SCORE_STAGE_PRICE_ALIGNMENT,
    ROUND175_SCORE_TARGETS,
    ROUND175_SOURCE_CANONICAL_TARGET_COUNT,
    ROUND175_SOURCE_CANONICAL_TARGET_IDS,
    ROUND175_STAGE_CAPS,
    render_round175_green_guardrail_markdown,
    render_round175_price_validation_plan_markdown,
    render_round175_risk_overlay_markdown,
    render_round175_score_stage_price_alignment_markdown,
    render_round175_summary_markdown,
    round175_base_score_weight_rows,
    round175_case_candidate_rows,
    round175_case_records,
    round175_price_field_rows,
    round175_score_profile_rows,
    round175_score_stage_price_alignment_rows,
    round175_stage_cap_rows,
    round175_stage_date_rows,
    round175_summary,
    round175_target_for,
    write_round175_r4_loop11_reports,
)


class Round175R4Loop11MaterialsSpreadStrategicTests(unittest.TestCase):
    def test_round175_targets_cover_source_archetypes(self):
        labels = {target.target_id for target in ROUND175_SCORE_TARGETS}

        self.assertEqual(ROUND175_SOURCE_CANONICAL_TARGET_COUNT, 13)
        self.assertEqual(len(labels), 13)
        self.assertEqual(set(ROUND175_SOURCE_CANONICAL_TARGET_IDS), labels)
        for target in ROUND175_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.MATERIALS_SPREAD_STRATEGIC)
            self.assertFalse(target.production_scoring_changed)

    def test_new_r4_loop11_canonical_archetypes_exist(self):
        expected = (
            E2RArchetype.COPPER_AI_GRID_KOREA,
            E2RArchetype.COPPER_PROCESSING_PLUS_DEFENSE,
            E2RArchetype.DEFENSE_AMMO_EVENT_PREMIUM,
            E2RArchetype.POLYSILICON_NON_CHINA_SUPPLY_OPTION,
            E2RArchetype.POLYSILICON_REPORT_NOT_CONTRACT,
            E2RArchetype.STEEL_TARIFF_EVENT_KOREA,
            E2RArchetype.STEEL_EXPORT_TARIFF_4C,
            E2RArchetype.SPECIALTY_STEEL_US_LOCALIZATION_OPTION,
            E2RArchetype.LITHIUM_PRICE_EVENT_KOREA,
            E2RArchetype.RARE_EARTH_THEME_KOREA,
            E2RArchetype.CHEMICAL_SPREAD_KOREA,
            E2RArchetype.EVENT_PREMIUM_GOVERNANCE_OVERLAY,
            E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_loop11_base_score_weights_and_stage_caps_match_round_note(self):
        weights = {row["component"]: row for row in round175_base_score_weight_rows()}
        caps = {row["stage_band"]: row for row in round175_stage_cap_rows()}

        self.assertEqual(len(ROUND175_BASE_SCORE_WEIGHTS), 7)
        self.assertEqual(weights["eps_fcf_opm_conversion"]["points"], "22")
        self.assertEqual(weights["contract_offtake_customer_visibility"]["points"], "20")
        self.assertEqual(weights["bottleneck_pricing_power"]["points"], "16")
        self.assertEqual(weights["early_price_path_validation"]["points"], "12")
        self.assertEqual(weights["cycle_spread_durability"]["points"], "12")
        self.assertEqual(weights["disclosure_confidence_redteam"]["points"], "10")
        self.assertEqual(weights["valuation_room_4b_runway"]["points"], "8")
        self.assertEqual(len(ROUND175_STAGE_CAPS), 5)
        self.assertEqual(caps["Stage 1"]["max_score"], "45")
        self.assertEqual(caps["Stage 2"]["max_score"], "70")
        self.assertIn("requires_4_of_7", caps["Stage 3"]["max_score"])
        self.assertIn("one_day_commodity_tariff_export_control_rally_10pct", caps["Stage 4B"]["required_evidence"])
        self.assertIn("mna_review_dropped_or_sale_denied", caps["Stage 4C"]["required_evidence"])

    def test_target_rules_split_macro_bottleneck_events_and_hard_gates(self):
        copper = round175_target_for("COPPER_AI_GRID_KOREA")
        poongsan = round175_target_for("COPPER_PROCESSING_PLUS_DEFENSE")
        ammo = round175_target_for("DEFENSE_AMMO_EVENT_PREMIUM")
        oci = round175_target_for("POLYSILICON_NON_CHINA_SUPPLY_OPTION")
        report_cap = round175_target_for("POLYSILICON_REPORT_NOT_CONTRACT")
        steel = round175_target_for("STEEL_TARIFF_EVENT_KOREA")
        steel_4c = round175_target_for("STEEL_EXPORT_TARIFF_4C")
        specialty = round175_target_for("SPECIALTY_STEEL_US_LOCALIZATION_OPTION")
        lithium = round175_target_for("LITHIUM_PRICE_EVENT_KOREA")
        rare = round175_target_for("RARE_EARTH_THEME_KOREA")
        chemical = round175_target_for("CHEMICAL_SPREAD_KOREA")
        event = round175_target_for("EVENT_PREMIUM_GOVERNANCE_OVERLAY")
        disclosure = round175_target_for("DISCLOSURE_CONFIDENCE_CAP")

        for target in (copper, poongsan, ammo, oci, report_cap, steel, steel_4c, specialty, lithium, rare, chemical, event, disclosure):
            self.assertIsNotNone(target)
        assert copper is not None
        assert poongsan is not None
        assert ammo is not None
        assert oci is not None
        assert report_cap is not None
        assert steel is not None
        assert steel_4c is not None
        assert specialty is not None
        assert lithium is not None
        assert rare is not None
        assert chemical is not None
        assert event is not None
        assert disclosure is not None
        self.assertEqual(copper.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("individual_order_backlog_up", copper.stage3_conditions)
        self.assertIn("hanwha_bid_report", poongsan.stage2_signals)
        self.assertIn("poongsan_sale_denial", poongsan.stage4c_conditions)
        self.assertTrue(ammo.hard_gate)
        self.assertIn("seller_denial", ammo.red_flags)
        self.assertIn("multi_year_supply_talks", oci.stage2_signals)
        self.assertTrue(report_cap.hard_gate)
        self.assertIn("company_confirmation_missing", report_cap.red_flags)
        self.assertIn("tariff_target_china_only", steel.stage2_signals)
        self.assertTrue(steel_4c.hard_gate)
        self.assertIn("direct_export_tariff", steel_4c.red_flags)
        self.assertIn("local_us_production", specialty.stage2_signals)
        self.assertTrue(lithium.hard_gate)
        self.assertIn("price_only_rally", lithium.red_flags)
        self.assertTrue(rare.hard_gate)
        self.assertIn("actual_revenue_missing", rare.red_flags)
        self.assertEqual(chemical.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("spread_reworsens", chemical.red_flags)
        self.assertTrue(event.hard_gate)
        self.assertEqual(disclosure.score_weight.eps_fcf_opm, "cap")

    def test_required_round175_cases_are_present_with_stage_markers(self):
        rows = {row["case_id"]: row for row in round175_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND175_CASE_CANDIDATES))
        self.assertEqual(rows["copper_ai_grid_korea_basket_stage2_cap_case"]["target_id"], "COPPER_AI_GRID_KOREA")
        self.assertIn("copper_up_35pct", rows["copper_ai_grid_korea_basket_stage2_cap_case"]["evidence_fields"])
        self.assertEqual(rows["poongsan_copper_defense_mna_unwind_case"]["stage2_date"], "2026-04-03")
        self.assertEqual(rows["poongsan_copper_defense_mna_unwind_case"]["stage4c_date"], "2026-04-09")
        self.assertEqual(rows["oci_holdings_spacex_polysilicon_report_cap_case"]["target_id"], "POLYSILICON_NON_CHINA_SUPPLY_OPTION")
        self.assertIn("media_report_only", rows["oci_holdings_spacex_polysilicon_report_cap_case"]["evidence_fields"])
        self.assertEqual(rows["steel_tariff_directionality_korea_case"]["target_id"], "STEEL_TARIFF_EVENT_KOREA")
        self.assertIn("tariff_direction_matters", rows["steel_tariff_directionality_korea_case"]["evidence_fields"])
        self.assertEqual(rows["seah_steel_export_tariff_4c_case"]["stage4c_date"], "2025-06-02")
        self.assertEqual(rows["specialty_steel_us_localization_option_case"]["target_id"], "SPECIALTY_STEEL_US_LOCALIZATION_OPTION")
        self.assertEqual(rows["lithium_rare_earth_price_only_theme_case"]["target_id"], "LITHIUM_PRICE_EVENT_KOREA")
        self.assertEqual(rows["rare_earth_theme_korea_stage1_case"]["case_type"], "overheat")
        self.assertEqual(rows["chemical_spread_korea_watch_red_case"]["target_id"], "CHEMICAL_SPREAD_KOREA")
        self.assertEqual(rows["disclosure_confidence_materials_cap_case"]["target_id"], "DISCLOSURE_CONFIDENCE_CAP")

    def test_case_records_validate_and_keep_loop11_guardrails(self):
        records = round175_case_records()

        self.assertEqual(len(records), len(ROUND175_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "MATERIALS_SPREAD_STRATEGIC")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("commodity_price_is_not_structural_evidence", record.green_guardrails)
            self.assertIn("stage3_early_catch_requires_4_of_7_loop11_conditions", record.green_guardrails)
            self.assertIn("media_report_tariff_lithium_rare_earth_mna_rumor_and_commodity_event_do_not_create_green", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["poongsan_copper_defense_mna_unwind_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["oci_holdings_spacex_polysilicon_report_cap_case"].rerating_result, "event_premium")
        self.assertEqual(by_id["seah_steel_export_tariff_4c_case"].score_price_alignment, "false_positive_score")
        self.assertEqual(by_id["rare_earth_theme_korea_stage1_case"].rerating_result, "theme_overheat")
        self.assertEqual(by_id["chemical_spread_korea_watch_red_case"].rerating_result, "no_rerating")
        self.assertIn("counterparty", by_id["disclosure_confidence_materials_cap_case"].must_have_fields)

    def test_score_profile_rows_mark_no_production_change(self):
        rows = round175_score_profile_rows()

        self.assertEqual(len(rows), len(ROUND175_SCORE_TARGETS))
        for row in rows:
            self.assertEqual(row["large_sector"], "MATERIALS_SPREAD_STRATEGIC")
            self.assertEqual(row["production_scoring_changed"], "false")
            self.assertIn("loop11_penalty_axes", row)
        by_target = {row["target_id"]: row for row in rows}
        self.assertEqual(by_target["COPPER_AI_GRID_KOREA"]["bottleneck_pricing"], "20")
        self.assertEqual(by_target["COPPER_PROCESSING_PLUS_DEFENSE"]["contract_offtake_customer_visibility"], "17")
        self.assertEqual(by_target["POLYSILICON_REPORT_NOT_CONTRACT"]["hard_gate"], "true")
        self.assertEqual(by_target["STEEL_EXPORT_TARIFF_4C"]["eps_fcf_opm"], "gate")
        self.assertEqual(by_target["LITHIUM_PRICE_EVENT_KOREA"]["eps_fcf_opm"], "event")
        self.assertEqual(by_target["RARE_EARTH_THEME_KOREA"]["hard_gate"], "true")
        self.assertEqual(by_target["DISCLOSURE_CONFIDENCE_CAP"]["eps_fcf_opm"], "cap")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round175_stage_date_rows()}
        fields = {row["field"] for row in round175_price_field_rows()}

        self.assertIn("individual_order_backlog_up", rows["COPPER_AI_GRID_KOREA"]["stage3"])
        self.assertIn("hanwha_review_dropped", rows["COPPER_PROCESSING_PLUS_DEFENSE"]["stage4c"])
        self.assertIn("contract_not_confirmed", rows["POLYSILICON_NON_CHINA_SUPPLY_OPTION"]["stage4c"])
        self.assertIn("tariff_target_china_only", rows["STEEL_TARIFF_EVENT_KOREA"]["stage2"])
        self.assertIn("us_steel_tariff_50pct", rows["STEEL_EXPORT_TARIFF_4C"]["stage4c"])
        self.assertIn("lithium_event_rally", rows["LITHIUM_PRICE_EVENT_KOREA"]["stage4b"])
        for field in (
            "return_1d_after_event",
            "return_5d_after_event",
            "return_60d_after_stage2",
            "mfe_120d_after_stage2",
            "relative_strength_vs_commodity_price",
            "commodity_price_at_stage",
            "commodity_price_change_60d",
            "contract_amount",
            "contract_counterparty",
            "offtake_volume",
            "price_floor_flag",
            "media_report_only_flag",
            "company_confirmation_flag",
            "tariff_target",
            "tariff_scope",
            "export_exposure_to_tariff_market",
            "local_production_flag",
            "inventory_loss_flag",
            "spread_margin_signal",
            "raw_material_cost_signal",
            "copper_passthrough_flag",
            "mna_bid_value",
            "mna_review_dropped_flag",
            "seller_denial_flag",
            "rare_earth_revenue_flag",
            "lithium_production_volume",
            "cb_bw_or_equity_raise_flag",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)

    def test_score_stage_price_alignment_rows_and_markdown(self):
        rows = {row["case_id"]: row for row in round175_score_stage_price_alignment_rows()}
        markdown = render_round175_score_stage_price_alignment_markdown()

        self.assertEqual(len(rows), len(ROUND175_SCORE_STAGE_PRICE_ALIGNMENT))
        self.assertEqual(rows["copper_ai_grid_korea_basket_stage2_cap_case"]["verdict"], "macro_bottleneck_not_company_green")
        self.assertEqual(rows["poongsan_copper_defense_mna_unwind_case"]["verdict"], "event_unwind_alignment")
        self.assertEqual(rows["oci_holdings_spacex_polysilicon_report_cap_case"]["verdict"], "report_not_contract_cap")
        self.assertEqual(rows["seah_steel_export_tariff_4c_case"]["verdict"], "direct_tariff_4c_alignment")
        self.assertIn("Poongsan", markdown)
        self.assertIn("OCI Holdings", markdown)
        self.assertIn("tariff", markdown.lower())

    def test_summary_and_markdown_explain_r4_loop11_guardrails(self):
        summary = round175_summary()
        summary_md = render_round175_summary_markdown()
        guardrails = render_round175_green_guardrail_markdown()
        overlays = render_round175_risk_overlay_markdown()
        price_plan = render_round175_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 13)
        self.assertEqual(summary["source_canonical_target_count"], 13)
        self.assertEqual(summary["case_candidate_count"], len(ROUND175_CASE_CANDIDATES))
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R4 Loop 11", summary_md)
        self.assertIn("EPS/FCF/OPM 22", summary_md)
        self.assertIn("Do not apply R4 Loop-11", guardrails)
        self.assertIn("STEEL_TARIFF_DIRECTIONALITY", overlays)
        self.assertIn("poongsan_copper_defense_mna_unwind_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            paths = write_round175_r4_loop11_reports(
                output_directory=tmp_path / "out",
                cases_path=tmp_path / "cases.jsonl",
                score_profile_path=tmp_path / "profiles.csv",
            )

            for path in paths.values():
                self.assertTrue(path.exists(), path)
            records = load_case_library(paths["cases"])
            self.assertEqual(len(records), len(ROUND175_CASE_CANDIDATES))
            summary = paths["summary"].read_text(encoding="utf-8")
            self.assertIn("Round-175 R4 Loop-11", summary)
            self.assertIn("production_scoring_changed: false", summary)

    def test_cli_argument_parser_supports_paths(self):
        parser = build_parser()
        args = parser.parse_args(
            [
                "--output-directory",
                "out",
                "--cases",
                "cases.jsonl",
                "--score-profiles",
                "profiles.csv",
            ]
        )

        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.score_profiles, "profiles.csv")

    def test_production_scoring_modules_do_not_import_round175_pack(self):
        root = Path(__file__).resolve().parents[1]
        forbidden = "round175_r4_loop11_materials_spread_strategic"
        for relative in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/scoring.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = (root / relative).read_text(encoding="utf-8")
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
