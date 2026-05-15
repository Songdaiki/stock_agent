import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round38_score_weight_report import build_parser
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10ThemePosture
from e2r.sector.round38_score_weight_v23 import (
    ROUND38_CASE_CANDIDATES,
    ROUND38_SCORE_TARGETS,
    render_round38_accounting_overlay_markdown,
    render_round38_ai_server_markdown,
    render_round38_neocloud_packaging_markdown,
    render_round38_summary_markdown,
    render_round38_validation_plan_markdown,
    round38_case_records,
    round38_score_profile_rows,
    round38_summary,
    target_for,
    write_round38_score_weight_reports,
)


class Round38ScoreWeightV23Tests(unittest.TestCase):
    def test_round38_targets_include_ai_server_neocloud_packaging_sic_and_overlay(self):
        labels = {target.target_id for target in ROUND38_SCORE_TARGETS}

        self.assertEqual(len(labels), 8)
        self.assertIn("AI_SERVER_ODM_EMS_SUPPLY_CHAIN", labels)
        self.assertIn("AI_SERVER_ACCOUNTING_GOVERNANCE_RISK", labels)
        self.assertIn("NEOCLOUD_GPU_RENTAL", labels)
        self.assertIn("ADVANCED_PACKAGING_COWOS_EMIB", labels)
        self.assertIn("SEMI_EQUIPMENT_AI_CAPEX", labels)
        self.assertIn("POWER_SEMICONDUCTOR_SIC", labels)
        self.assertIn("OPTICAL_NETWORKING_AI_DATACENTER", labels)
        self.assertIn("REDTEAM_ACCOUNTING_TRUST_OVERLAY", labels)

    def test_ai_server_is_green_possible_but_accounting_and_margin_risks_are_explicit(self):
        target = target_for("AI_SERVER_ODM_EMS_SUPPLY_CHAIN")
        markdown = render_round38_ai_server_markdown()
        records = {record.case_id: record for record in round38_case_records()}

        self.assertIsNotNone(target)
        assert target is not None
        self.assertEqual(target.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(target.validation_group, "high_growth_ai_hardware")
        self.assertIn("rack_shipment_growth", target.green_conditions)
        self.assertIn("gross_margin_stable", target.green_conditions)
        self.assertIn("accounting_trust", target.red_flags)
        self.assertIn("low_margin_assembly", target.red_flags)
        self.assertEqual(records["supermicro_ai_server_rerating_then_accounting_4c"].case_type, "4c_thesis_break")
        self.assertEqual(records["ai_server_low_margin_customer_concentration_counterexample"].score_price_alignment, "false_positive_score")
        self.assertIn("Supermicro-style auditor resignation", markdown)

    def test_accounting_trust_targets_are_hard_redteam_gates_not_score_weights(self):
        risk = target_for("AI_SERVER_ACCOUNTING_GOVERNANCE_RISK")
        overlay = target_for("REDTEAM_ACCOUNTING_TRUST_OVERLAY")
        markdown = render_round38_accounting_overlay_markdown()
        records = {record.case_id: record for record in round38_case_records()}

        self.assertIsNotNone(risk)
        self.assertIsNotNone(overlay)
        assert risk is not None
        assert overlay is not None
        self.assertEqual(risk.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertEqual(overlay.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertEqual(risk.validation_group, "hard_redteam_gate")
        self.assertEqual(risk.score_weight.eps_fcf, "gate")
        self.assertIn("auditor_resignation", risk.red_flags)
        self.assertEqual(records["supermicro_ey_resignation_hard_4c"].rerating_result, "thesis_break")
        self.assertIn("Stage 3-Green is immediately blocked", markdown)

    def test_neocloud_is_watch_first_due_to_debt_customer_concentration_and_fcf(self):
        target = target_for("NEOCLOUD_GPU_RENTAL")
        records = {record.case_id: record for record in round38_case_records()}

        self.assertIsNotNone(target)
        assert target is not None
        self.assertEqual(target.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertEqual(target.validation_group, "high_debt_infra")
        self.assertIn("take_or_pay", target.green_conditions)
        self.assertIn("fcf_negative", target.red_flags)
        self.assertIn("gpu_obsolescence", target.red_flags)
        self.assertEqual(records["coreweave_take_or_pay_contract_candidate"].case_type, "success_candidate")
        self.assertEqual(records["coreweave_ipo_below_range_price_path_watch"].case_type, "event_premium")
        self.assertEqual(records["gpu_obsolescence_funding_cost_4c"].case_type, "4c_thesis_break")

    def test_packaging_equipment_and_optical_are_green_possible_but_capex_cycle_is_tested(self):
        packaging = target_for("ADVANCED_PACKAGING_COWOS_EMIB")
        equipment = target_for("SEMI_EQUIPMENT_AI_CAPEX")
        optical = target_for("OPTICAL_NETWORKING_AI_DATACENTER")
        markdown = render_round38_neocloud_packaging_markdown()
        records = {record.case_id: record for record in round38_case_records()}

        for target in (packaging, equipment, optical):
            self.assertIsNotNone(target)
            assert target is not None
            self.assertEqual(target.posture, Round10ThemePosture.GREEN_POSSIBLE)

        assert packaging is not None
        assert equipment is not None
        assert optical is not None
        self.assertIn("bottleneck_normalization", packaging.red_flags)
        self.assertIn("export_control", equipment.red_flags)
        self.assertIn("capacity_normalization", optical.red_flags)
        self.assertEqual(records["packaging_bottleneck_normalization_4b"].case_type, "4b_watch")
        self.assertEqual(records["capex_peak_equipment_4c"].case_type, "4c_thesis_break")
        self.assertEqual(records["optical_networking_capacity_normalization_4b"].case_type, "4b_watch")
        self.assertIn("CoWoS/EMIB", markdown)

    def test_sic_is_watch_first_and_wolfspeed_is_hard_counterexample(self):
        target = target_for("POWER_SEMICONDUCTOR_SIC")
        records = {record.case_id: record for record in round38_case_records()}

        self.assertIsNotNone(target)
        assert target is not None
        self.assertEqual(target.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertEqual(target.validation_group, "cycle_capex_debt")
        self.assertIn("capex_debt", target.red_flags)
        self.assertIn("bankruptcy", target.red_flags)
        self.assertEqual(records["wolfspeed_chapter11_restructuring_4c"].case_type, "4c_thesis_break")
        self.assertEqual(records["sic_long_term_contract_success_candidate_if_fcf"].case_type, "success_candidate")

    def test_validation_plan_renders_ai_hardware_high_debt_and_hard_gate_groups(self):
        plan = render_round38_validation_plan_markdown()
        rows = round38_score_profile_rows()

        self.assertIn("high_growth_ai_hardware", plan)
        self.assertIn("high_debt_infra", plan)
        self.assertIn("hard_redteam_gate", plan)
        for row in rows:
            self.assertEqual(row["production_scoring_changed"], "false")
            self.assertIn("validation_group", row)
            self.assertIn("validation_metrics", row)

    def test_case_records_validate_and_keep_backfill_open(self):
        records = round38_case_records()

        self.assertEqual(len(records), len(ROUND38_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.price_validation.price_validation_status, "needs_price_backfill")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_invent_margins_backlog_contracts_or_prices", record.green_guardrails)

    def test_summary_reports_v23_validation_without_production_scoring(self):
        summary = round38_summary()
        markdown = render_round38_summary_markdown()

        self.assertEqual(summary["target_count"], 8)
        self.assertEqual(summary["case_candidate_count"], 28)
        self.assertEqual(summary["success_candidate_count"], 9)
        self.assertEqual(summary["stage4b_case_count"], 2)
        self.assertEqual(summary["stage4c_case_count"], 8)
        self.assertEqual(summary["green_possible_count"], 4)
        self.assertEqual(summary["watch_yellow_first_count"], 2)
        self.assertEqual(summary["redteam_first_count"], 2)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("production_scoring_changed: false", markdown)
        self.assertIn("v2.3 price-path validation plans", markdown)

    def test_report_writer_outputs_cases_and_validation_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round38_score_weight_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_v20_round38.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round38_v23.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["green_guardrails"].exists())
            self.assertTrue(paths["validation_plan"].exists())
            self.assertTrue(paths["ai_server"].exists())
            self.assertTrue(paths["neocloud_packaging"].exists())
            self.assertTrue(paths["accounting_overlay"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND38_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round38_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round38_score_weight_v23", text)


if __name__ == "__main__":
    unittest.main()
