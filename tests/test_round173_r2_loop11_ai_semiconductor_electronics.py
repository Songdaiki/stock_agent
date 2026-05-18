import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round173_r2_loop11_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round173_r2_loop11_ai_semiconductor_electronics import (
    ROUND173_BASE_SCORE_WEIGHTS,
    ROUND173_CASE_CANDIDATES,
    ROUND173_PRICE_FIELDS,
    ROUND173_SCORE_STAGE_PRICE_ALIGNMENT,
    ROUND173_SCORE_TARGETS,
    ROUND173_SOURCE_CANONICAL_TARGET_COUNT,
    ROUND173_SOURCE_CANONICAL_TARGET_IDS,
    ROUND173_STAGE_CAPS,
    render_round173_green_guardrail_markdown,
    render_round173_loop11_risk_overlay_markdown,
    render_round173_price_validation_plan_markdown,
    render_round173_score_stage_price_alignment_markdown,
    render_round173_summary_markdown,
    round173_base_score_weight_rows,
    round173_case_candidate_rows,
    round173_case_records,
    round173_price_field_rows,
    round173_score_profile_rows,
    round173_score_stage_price_alignment_rows,
    round173_stage_cap_rows,
    round173_stage_date_rows,
    round173_summary,
    round173_target_for,
    write_round173_r2_loop11_reports,
)


class Round173R2Loop11AISemiconductorElectronicsTests(unittest.TestCase):
    def test_round173_targets_cover_korea_r2_loop11_archetypes(self):
        labels = {target.target_id for target in ROUND173_SCORE_TARGETS}

        self.assertEqual(ROUND173_SOURCE_CANONICAL_TARGET_COUNT, 10)
        self.assertEqual(len(labels), 12)
        self.assertTrue(set(ROUND173_SOURCE_CANONICAL_TARGET_IDS).issubset(labels))
        self.assertIn("HBM_SUPPLY_CHAIN_LABOR_DISRUPTION_OVERLAY", labels)
        self.assertIn("AI_CHIP_LISTED_EARNINGS_LINK_GATE", labels)
        for target in ROUND173_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS)
            self.assertFalse(target.production_scoring_changed)

    def test_new_r2_loop11_canonical_archetypes_exist(self):
        expected = (
            E2RArchetype.HBM_BONDER_EQUIPMENT_KOREA,
            E2RArchetype.ADVANCED_PACKAGING_EQUIPMENT_KOREA,
            E2RArchetype.AI_SERVER_PCB_MLB_KOREA,
            E2RArchetype.SEMICONDUCTOR_TEST_SOCKET_KOREA,
            E2RArchetype.HBM_TEST_EQUIPMENT_KOREA,
            E2RArchetype.SYSTEM_SEMI_FOUNDARY_OPTION_KOREA,
            E2RArchetype.AI_CHIP_FABRIC_PRIVATE_RELATED,
            E2RArchetype.ON_DEVICE_AI_THEME,
            E2RArchetype.MOU_OR_REPORT_NOT_CONTRACT,
            E2RArchetype.HBM_SUPPLY_CHAIN_LABOR_DISRUPTION_OVERLAY,
            E2RArchetype.AI_CHIP_LISTED_EARNINGS_LINK_GATE,
            E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_loop11_base_score_weights_and_stage_caps_match_round_note(self):
        weights = {row["component"]: row for row in round173_base_score_weight_rows()}
        caps = {row["stage_band"]: row for row in round173_stage_cap_rows()}

        self.assertEqual(len(ROUND173_BASE_SCORE_WEIGHTS), 7)
        self.assertEqual(weights["eps_fcf_opm_conversion"]["points"], "24")
        self.assertEqual(weights["customer_contract_shipment_visibility"]["points"], "22")
        self.assertEqual(weights["bottleneck_pricing_power"]["points"], "18")
        self.assertEqual(weights["early_price_path_validation"]["points"], "12")
        self.assertEqual(weights["information_confidence_disclosure_detail"]["points"], "8")
        self.assertEqual(weights["capital_discipline_fcf_stability"]["points"], "6")
        self.assertEqual(weights["valuation_room_4b_runway"]["points"], "10")
        self.assertEqual(len(ROUND173_STAGE_CAPS), 6)
        self.assertEqual(caps["Stage 1"]["max_score"], "45")
        self.assertEqual(caps["Stage 2"]["max_score"], "70")
        self.assertEqual(caps["Stage 2.5"]["max_score"], "watch")
        self.assertIn("requires_4_of_7", caps["Stage 3"]["max_score"])
        self.assertIn("price_300_500pct", caps["Stage 4B"]["required_evidence"])
        self.assertIn("direct_earnings_link_missing", caps["Stage 4C"]["required_evidence"])

    def test_loop11_target_rules_separate_green_watch_event_and_hard_gates(self):
        hanmi = round173_target_for("HBM_BONDER_EQUIPMENT_KOREA")
        pcb = round173_target_for("AI_SERVER_PCB_MLB_KOREA")
        leeno = round173_target_for("SEMICONDUCTOR_TEST_SOCKET_KOREA")
        db = round173_target_for("SYSTEM_SEMI_FOUNDARY_OPTION_KOREA")
        private = round173_target_for("AI_CHIP_FABRIC_PRIVATE_RELATED")
        report_cap = round173_target_for("MOU_OR_REPORT_NOT_CONTRACT")
        labor = round173_target_for("HBM_SUPPLY_CHAIN_LABOR_DISRUPTION_OVERLAY")
        earnings_gate = round173_target_for("AI_CHIP_LISTED_EARNINGS_LINK_GATE")

        for target in (hanmi, pcb, leeno, db, private, report_cap, labor, earnings_gate):
            self.assertIsNotNone(target)
        assert hanmi is not None
        assert pcb is not None
        assert leeno is not None
        assert db is not None
        assert private is not None
        assert report_cap is not None
        assert labor is not None
        assert earnings_gate is not None
        self.assertEqual(hanmi.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("op_eps_revision", hanmi.stage3_conditions)
        self.assertEqual(pcb.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("price_300_500pct", pcb.stage4b_conditions)
        self.assertEqual(leeno.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("customer_detail_missing", leeno.red_flags)
        self.assertIn("customer_wafer_revenue", db.stage3_conditions)
        self.assertEqual(private.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("direct_earnings_link_missing", private.red_flags)
        self.assertTrue(report_cap.hard_gate)
        self.assertIn("final_contract_missing", report_cap.stage4c_conditions)
        self.assertTrue(labor.hard_gate)
        self.assertIn("labor_strike", labor.stage4c_conditions)
        self.assertTrue(earnings_gate.hard_gate)

    def test_required_round173_cases_are_present_with_stage_markers(self):
        rows = {row["case_id"]: row for row in round173_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND173_CASE_CANDIDATES))
        self.assertEqual(rows["hanmi_hbm_bonder_stage3_4b_case"]["target_id"], "HBM_BONDER_EQUIPMENT_KOREA")
        self.assertIn("sk_hynix_contract", rows["hanmi_hbm_bonder_stage3_4b_case"]["evidence_fields"])
        self.assertEqual(rows["isu_petasys_ai_server_pcb_487pct_4b_case"]["case_type"], "4b_watch")
        self.assertIn("stock_surge_487pct", rows["isu_petasys_ai_server_pcb_487pct_4b_case"]["evidence_fields"])
        self.assertEqual(rows["leeno_ai_test_socket_stage25_case"]["target_id"], "SEMICONDUCTOR_TEST_SOCKET_KOREA")
        self.assertIn("ai_boom_price_up_70pct", rows["leeno_ai_test_socket_stage25_case"]["evidence_fields"])
        self.assertEqual(rows["db_hitek_foundry_reram_stage2_case"]["stage2_date"], "2025-12-10")
        self.assertEqual(rows["rebellions_sapeon_related_stock_green_cap_case"]["stage2_date"], "2026-03-26")
        self.assertEqual(rows["hanmi_micron_media_report_not_contract_case"]["target_id"], "MOU_OR_REPORT_NOT_CONTRACT")
        self.assertEqual(rows["samsung_labor_disruption_overlay_case"]["stage4c_date"], "2026-05-15")
        self.assertEqual(rows["hbm_test_equipment_stage2_case"]["target_id"], "HBM_TEST_EQUIPMENT_KOREA")
        self.assertEqual(rows["ai_chip_private_related_direct_revenue_missing_case"]["target_id"], "AI_CHIP_LISTED_EARNINGS_LINK_GATE")

    def test_case_records_validate_and_keep_loop11_guardrails(self):
        records = round173_case_records()

        self.assertEqual(len(records), len(ROUND173_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "AI_SEMICONDUCTOR_ELECTRONICS")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("stage3_early_catch_requires_4_of_7_loop11_conditions", record.green_guardrails)
            self.assertIn("direct_listed_company_earnings_link_required_for_private_ai_chip_related_stocks", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["hanmi_hbm_bonder_stage3_4b_case"].score_price_alignment, "aligned")
        self.assertEqual(by_id["isu_petasys_ai_server_pcb_487pct_4b_case"].rerating_result, "theme_overheat")
        self.assertEqual(by_id["rebellions_sapeon_related_stock_green_cap_case"].rerating_result, "event_premium")
        self.assertEqual(by_id["samsung_labor_disruption_overlay_case"].rerating_result, "thesis_break")
        self.assertIn("direct_earnings_link_missing", by_id["ai_chip_private_related_direct_revenue_missing_case"].red_flag_fields)

    def test_score_profile_rows_mark_no_production_change(self):
        rows = round173_score_profile_rows()

        self.assertEqual(len(rows), len(ROUND173_SCORE_TARGETS))
        for row in rows:
            self.assertEqual(row["large_sector"], "AI_SEMICONDUCTOR_ELECTRONICS")
            self.assertEqual(row["production_scoring_changed"], "false")
            self.assertIn("loop11_penalty_axes", row)
        by_target = {row["target_id"]: row for row in rows}
        self.assertEqual(by_target["HBM_BONDER_EQUIPMENT_KOREA"]["eps_fcf_opm"], "24")
        self.assertEqual(by_target["HBM_BONDER_EQUIPMENT_KOREA"]["customer_contract_shipment_visibility"], "22")
        self.assertEqual(by_target["MOU_OR_REPORT_NOT_CONTRACT"]["hard_gate"], "true")
        self.assertEqual(by_target["HBM_SUPPLY_CHAIN_LABOR_DISRUPTION_OVERLAY"]["hard_gate"], "true")
        self.assertEqual(by_target["AI_CHIP_LISTED_EARNINGS_LINK_GATE"]["hard_gate"], "true")
        self.assertEqual(by_target["DISCLOSURE_CONFIDENCE_CAP"]["eps_fcf_opm"], "cap")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round173_stage_date_rows()}
        fields = {row["field"] for row in round173_price_field_rows()}

        self.assertIn("op_eps_revision", rows["HBM_BONDER_EQUIPMENT_KOREA"]["stage3"])
        self.assertIn("price_300_500pct", rows["AI_SERVER_PCB_MLB_KOREA"]["stage4b"])
        self.assertIn("high_margin_socket_mix", rows["SEMICONDUCTOR_TEST_SOCKET_KOREA"]["stage3"])
        self.assertIn("customer_wafer_revenue", rows["SYSTEM_SEMI_FOUNDARY_OPTION_KOREA"]["stage3"])
        self.assertIn("direct_earnings_link_missing", rows["AI_CHIP_FABRIC_PRIVATE_RELATED"]["stage4c"])
        self.assertIn("final_contract_missing", rows["MOU_OR_REPORT_NOT_CONTRACT"]["stage4c"])
        self.assertIn("labor_strike", rows["HBM_SUPPLY_CHAIN_LABOR_DISRUPTION_OVERLAY"]["stage4c"])
        for field in (
            "price_at_stage2",
            "return_60d_after_stage2",
            "return_252d_after_stage3",
            "mfe_120d_after_stage2",
            "relative_strength_vs_semiconductor_basket",
            "valuation_at_stage4b",
            "eps_revision_before_stage3",
            "op_revision_after_stage3",
            "contract_amount",
            "customer_name",
            "customer_diversification_flag",
            "shipment_schedule",
            "hbm_bonder_flag",
            "sk_hynix_contract_flag",
            "micron_final_contract_flag",
            "ai_server_pcb_flag",
            "stock_surge_300_500pct_flag",
            "test_socket_flag",
            "hbm_test_equipment_flag",
            "system_foundry_policy_flag",
            "reram_license_flag",
            "private_ai_chip_flag",
            "listed_company_direct_revenue_flag",
            "on_device_ai_flag",
            "media_report_only_flag",
            "labor_strike_flag",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)

    def test_score_stage_price_alignment_rows_and_markdown(self):
        rows = {row["case_id"]: row for row in round173_score_stage_price_alignment_rows()}
        markdown = render_round173_score_stage_price_alignment_markdown()

        self.assertEqual(len(rows), len(ROUND173_SCORE_STAGE_PRICE_ALIGNMENT))
        self.assertEqual(rows["hanmi_hbm_bonder_stage3_4b_case"]["verdict"], "stage3_catch_and_4b_cool_required")
        self.assertEqual(rows["isu_petasys_ai_server_pcb_487pct_4b_case"]["verdict"], "structural_success_but_late_4b")
        self.assertEqual(rows["db_hitek_foundry_reram_stage2_case"]["verdict"], "policy_license_not_green")
        self.assertIn("한미반도체", markdown)
        self.assertIn("이수페타시스", markdown)
        self.assertIn("private valuation", markdown.lower())

    def test_summary_and_markdown_explain_r2_loop11_guardrails(self):
        summary = round173_summary()
        summary_md = render_round173_summary_markdown()
        guardrails = render_round173_green_guardrail_markdown()
        overlays = render_round173_loop11_risk_overlay_markdown()
        price_plan = render_round173_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 12)
        self.assertEqual(summary["source_canonical_target_count"], 10)
        self.assertEqual(summary["case_candidate_count"], len(ROUND173_CASE_CANDIDATES))
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R2 Loop 11", summary_md)
        self.assertIn("customer/contract/shipment visibility 22", summary_md)
        self.assertIn("Do not apply R2 Loop-11", guardrails)
        self.assertIn("PRIVATE_AI_CHIP_LISTED_LINK_GATE", overlays)
        self.assertIn("hanmi_hbm_bonder_stage3_4b_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            paths = write_round173_r2_loop11_reports(
                output_directory=tmp_path / "out",
                cases_path=tmp_path / "cases.jsonl",
                score_profile_path=tmp_path / "profiles.csv",
            )

            for path in paths.values():
                self.assertTrue(path.exists(), path)
            records = load_case_library(paths["cases"])
            self.assertEqual(len(records), len(ROUND173_CASE_CANDIDATES))
            summary = paths["summary"].read_text(encoding="utf-8")
            self.assertIn("Round-173 R2 Loop-11", summary)
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

    def test_production_scoring_modules_do_not_import_round173_pack(self):
        root = Path(__file__).resolve().parents[1]
        forbidden = "round173_r2_loop11_ai_semiconductor_electronics"
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
