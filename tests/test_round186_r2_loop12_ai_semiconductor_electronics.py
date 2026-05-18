import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round186_r2_loop12_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round186_r2_loop12_ai_semiconductor_electronics import (
    ROUND186_BASE_SCORE_WEIGHTS,
    ROUND186_CASE_CANDIDATES,
    ROUND186_PRICE_FIELDS,
    ROUND186_SCORE_TARGETS,
    ROUND186_SOURCE_CANONICAL_TARGET_COUNT,
    ROUND186_SOURCE_CANONICAL_TARGET_IDS,
    ROUND186_STAGE_CAPS,
    render_round186_green_guardrail_markdown,
    render_round186_price_validation_plan_markdown,
    render_round186_risk_overlay_markdown,
    render_round186_score_stage_price_alignment_markdown,
    render_round186_summary_markdown,
    round186_base_score_weight_rows,
    round186_case_candidate_rows,
    round186_case_records,
    round186_price_field_rows,
    round186_score_profile_rows,
    round186_score_stage_price_alignment_rows,
    round186_stage_cap_rows,
    round186_stage_date_rows,
    round186_summary,
    round186_target_for,
    write_round186_r2_loop12_reports,
)


class Round186R2Loop12AISemiconductorElectronicsTests(unittest.TestCase):
    def test_round186_targets_cover_loop12_archetypes(self):
        labels = {target.target_id for target in ROUND186_SCORE_TARGETS}

        self.assertEqual(len(labels), 12)
        self.assertEqual(ROUND186_SOURCE_CANONICAL_TARGET_COUNT, 12)
        self.assertEqual(set(ROUND186_SOURCE_CANONICAL_TARGET_IDS), labels)
        for target in ROUND186_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS)
            self.assertFalse(target.production_scoring_changed)

    def test_new_loop12_canonical_archetypes_exist(self):
        expected = (
            E2RArchetype.GLASS_SUBSTRATE_ADVANCED_PACKAGING_KOREA,
            E2RArchetype.SYSTEM_SEMI_DESIGN_HOUSE_AI_ORDER,
            E2RArchetype.HBM_TEST_EQUIPMENT_KOREA,
            E2RArchetype.ADVANCED_PACKAGING_EQUIPMENT_BASKET,
            E2RArchetype.AI_SERVER_PCB_SUBSTRATE_SECOND_WAVE,
            E2RArchetype.MLCC_AI_SERVER_COMPONENTS,
            E2RArchetype.CAMERA_LIDAR_ADAS_ELECTRONICS,
            E2RArchetype.ON_DEVICE_AI_THEME_KOREA,
            E2RArchetype.SEMI_CAPEX_ORDER_TO_REVENUE,
            E2RArchetype.IP_LEAK_SUPPLY_CHAIN_REDTEAM,
            E2RArchetype.LABOR_PRODUCTION_DISRUPTION_OVERLAY,
            E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_base_weights_and_stage_caps_match_round186_note(self):
        weights = {row["component"]: row for row in round186_base_score_weight_rows()}
        caps = {row["stage_band"]: row for row in round186_stage_cap_rows()}

        self.assertEqual(len(ROUND186_BASE_SCORE_WEIGHTS), 7)
        self.assertEqual(weights["eps_fcf_opm_conversion"]["points"], "24")
        self.assertEqual(weights["customer_contract_shipment_visibility"]["points"], "22")
        self.assertEqual(weights["bottleneck_process_technology_adoption"]["points"], "16")
        self.assertEqual(weights["early_price_path_validation"]["points"], "12")
        self.assertEqual(weights["mass_production_yield_customer_diversification"]["points"], "8")
        self.assertEqual(weights["ip_labor_security_disclosure_redteam"]["points"], "10")
        self.assertEqual(weights["valuation_room_4b_runway"]["points"], "8")
        self.assertEqual(len(ROUND186_STAGE_CAPS), 5)
        self.assertEqual(caps["Stage 3"]["max_score"], "requires_5_of_8")
        self.assertIn("shipment_or_mass_production_schedule", caps["Stage 3"]["required_evidence"])
        self.assertEqual(caps["Stage 4B"]["max_score"], "requires_4_of_6")
        self.assertIn("media_mou_design_win_only_price_rally", caps["Stage 4B"]["required_evidence"])
        self.assertEqual(caps["Stage 4C"]["max_score"], "hard_gate")
        self.assertIn("ip_leak_or_china_catchup", caps["Stage 4C"]["required_evidence"])
        for row in weights.values():
            self.assertEqual(row["production_scoring_changed"], "false")
        for row in caps.values():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_green_watch_and_hard_gate_targets_are_separated(self):
        glass = round186_target_for("GLASS_SUBSTRATE_ADVANCED_PACKAGING_KOREA")
        design = round186_target_for("SYSTEM_SEMI_DESIGN_HOUSE_AI_ORDER")
        hbm_test = round186_target_for("HBM_TEST_EQUIPMENT_KOREA")
        pcb = round186_target_for("AI_SERVER_PCB_SUBSTRATE_SECOND_WAVE")
        on_device = round186_target_for("ON_DEVICE_AI_THEME_KOREA")
        ip = round186_target_for("IP_LEAK_SUPPLY_CHAIN_REDTEAM")
        labor = round186_target_for("LABOR_PRODUCTION_DISRUPTION_OVERLAY")

        for target in (glass, design, hbm_test, pcb, on_device, ip, labor):
            self.assertIsNotNone(target)
        assert glass is not None
        assert design is not None
        assert hbm_test is not None
        assert pcb is not None
        assert on_device is not None
        assert ip is not None
        assert labor is not None
        self.assertEqual(glass.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("yield_visible", glass.green_conditions)
        self.assertIn("order_size", design.green_conditions)
        self.assertEqual(hbm_test.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("customer_order", hbm_test.green_conditions)
        self.assertEqual(pcb.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("inventory_normalization", pcb.green_conditions)
        self.assertEqual(on_device.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("direct_revenue_missing", on_device.red_flags)
        self.assertTrue(ip.hard_gate)
        self.assertIn("ip_leak", ip.red_flags)
        self.assertTrue(labor.hard_gate)
        self.assertIn("production_delay", labor.red_flags)

    def test_required_round186_cases_are_present(self):
        rows = {row["case_id"]: row for row in round186_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND186_CASE_CANDIDATES))
        self.assertEqual(rows["skc_absolics_glass_substrate_stage2_case"]["target_id"], "GLASS_SUBSTRATE_ADVANCED_PACKAGING_KOREA")
        self.assertIn("chips_grant_75m_usd", rows["skc_absolics_glass_substrate_stage2_case"]["evidence_fields"])
        self.assertEqual(rows["gaonchips_pfn_samsung_2nm_stage2_case"]["target_id"], "SYSTEM_SEMI_DESIGN_HOUSE_AI_ORDER")
        self.assertIn("order_size_undisclosed", rows["gaonchips_pfn_samsung_2nm_stage2_case"]["red_flag_fields"])
        self.assertEqual(rows["hbm_test_equipment_basket_stage3_candidate_case"]["target_id"], "HBM_TEST_EQUIPMENT_KOREA")
        self.assertEqual(rows["hanwha_precision_spinoff_hbm_equipment_stage2_4c_watch_case"]["case_type"], "failed_rerating")
        self.assertEqual(rows["on_device_ai_theme_korea_stage1_2_4b_watch_case"]["case_type"], "4b_watch")
        self.assertEqual(rows["samsung_supply_chain_labor_disruption_4c_case"]["case_type"], "4c_thesis_break")
        self.assertEqual(rows["korea_memory_ip_leak_cxmt_4c_case"]["target_id"], "IP_LEAK_SUPPLY_CHAIN_REDTEAM")
        self.assertEqual(rows["r2_loop12_disclosure_confidence_reference_case"]["target_id"], "DISCLOSURE_CONFIDENCE_CAP")

    def test_case_records_validate_and_keep_loop12_guardrails(self):
        records = round186_case_records()

        self.assertEqual(len(records), len(ROUND186_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "AI_SEMICONDUCTOR_ELECTRONICS")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("stage3_early_catch_requires_5_of_8_loop12_conditions", record.green_guardrails)
            self.assertIn("design_win_mou_media_only_cannot_create_stage3", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["on_device_ai_theme_korea_stage1_2_4b_watch_case"].rerating_result, "theme_overheat")
        self.assertEqual(by_id["samsung_supply_chain_labor_disruption_4c_case"].score_price_alignment, "false_positive_score")
        self.assertEqual(by_id["hanwha_precision_spinoff_hbm_equipment_stage2_4c_watch_case"].score_price_alignment, "evidence_good_but_price_failed")

    def test_score_profile_rows_mark_no_production_change(self):
        rows = round186_score_profile_rows()
        by_target = {row["target_id"]: row for row in rows}

        self.assertEqual(len(rows), len(ROUND186_SCORE_TARGETS))
        self.assertEqual(by_target["HBM_TEST_EQUIPMENT_KOREA"]["eps_fcf_opm"], "23")
        self.assertEqual(by_target["GLASS_SUBSTRATE_ADVANCED_PACKAGING_KOREA"]["customer_contract_shipment_visibility"], "20")
        self.assertEqual(by_target["IP_LEAK_SUPPLY_CHAIN_REDTEAM"]["hard_gate"], "true")
        self.assertEqual(by_target["LABOR_PRODUCTION_DISRUPTION_OVERLAY"]["hard_gate"], "true")
        self.assertEqual(by_target["DISCLOSURE_CONFIDENCE_CAP"]["eps_fcf_opm"], "cap")
        for row in rows:
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_stage_date_price_and_alignment_rows_are_explicit(self):
        stage_rows = {row["target_id"]: row for row in round186_stage_date_rows()}
        price_fields = {row["field"] for row in round186_price_field_rows()}
        alignment_rows = {row["case_id"]: row for row in round186_score_stage_price_alignment_rows()}

        self.assertIn("customer_qualification", stage_rows["GLASS_SUBSTRATE_ADVANCED_PACKAGING_KOREA"]["stage3"])
        self.assertIn("order_size_visible", stage_rows["SYSTEM_SEMI_DESIGN_HOUSE_AI_ORDER"]["stage3"])
        self.assertIn("ip_leak", stage_rows["IP_LEAK_SUPPLY_CHAIN_REDTEAM"]["stage4c"])
        self.assertIn("labor_disruption", stage_rows["LABOR_PRODUCTION_DISRUPTION_OVERLAY"]["stage4c"])
        for field in (
            "relative_strength_vs_ai_hardware_basket",
            "relative_strength_vs_hbm_equipment_basket",
            "order_size",
            "customer_name",
            "design_win_flag",
            "mass_production_flag",
            "yield_signal",
            "customer_qualification_status",
            "customer_capex_delay_flag",
            "ip_leak_risk_flag",
            "labor_disruption_flag",
            "disclosure_confidence",
            "valuation_at_stage4b",
        ):
            self.assertIn(field, price_fields)
        self.assertEqual(alignment_rows["skc_absolics_glass_substrate_stage2_case"]["verdict"], "commercialization_gate_not_green")
        self.assertEqual(alignment_rows["korea_memory_ip_leak_cxmt_4c_case"]["verdict"], "hard_redteam_alignment")

    def test_summary_and_markdown_explain_loop12(self):
        summary = round186_summary()
        summary_md = render_round186_summary_markdown()
        guardrails = render_round186_green_guardrail_markdown()
        overlays = render_round186_risk_overlay_markdown()
        price_plan = render_round186_price_validation_plan_markdown()
        alignment = render_round186_score_stage_price_alignment_markdown()

        self.assertEqual(summary["target_count"], 12)
        self.assertEqual(summary["source_canonical_target_count"], 12)
        self.assertEqual(summary["case_candidate_count"], 13)
        self.assertEqual(summary["base_score_axis_count"], 7)
        self.assertEqual(summary["stage_cap_count"], 5)
        self.assertEqual(summary["score_stage_price_alignment_count"], 8)
        self.assertEqual(summary["success_candidate_count"], 7)
        self.assertEqual(summary["event_premium_count"], 0)
        self.assertEqual(summary["failed_rerating_count"], 3)
        self.assertEqual(summary["stage4b_case_count"], 1)
        self.assertEqual(summary["stage4c_case_count"], 2)
        self.assertEqual(summary["hard_gate_target_count"], 2)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R2 Loop 12", summary_md)
        self.assertIn("production_scoring_changed: false", summary_md)
        self.assertIn("at least 5 of 8 checks", guardrails)
        self.assertIn("IP_LEAK_SUPPLY_CHAIN_REDTEAM", overlays)
        self.assertIn("Required Fields", price_plan)
        self.assertIn("SKC/Absolics", alignment)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round186_r2_loop12_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r2_loop12_round186.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round186_r2_loop12_v12.csv",
            )

            for key in (
                "cases",
                "score_profiles",
                "summary",
                "case_matrix",
                "stage_date_plan",
                "green_guardrails",
                "risk_overlays",
                "price_validation_plan",
                "price_fields",
                "base_score_weights",
                "stage_caps",
                "score_stage_price_alignment",
                "score_stage_price_alignment_md",
            ):
                self.assertTrue(paths[key].exists(), key)
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND186_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round186_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round186_r2_loop12_ai_semiconductor_electronics", text)


if __name__ == "__main__":
    unittest.main()
