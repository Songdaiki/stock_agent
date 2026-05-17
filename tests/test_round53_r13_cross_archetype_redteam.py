import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round53_r13_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10ThemePosture
from e2r.sector.round53_r13_cross_archetype_redteam import (
    ROUND53_CASE_CANDIDATES,
    ROUND53_LARGE_SECTOR,
    ROUND53_OVERLAY_TARGETS,
    render_round53_price_validation_plan_markdown,
    render_round53_redteam_gate_plan_markdown,
    render_round53_summary_markdown,
    round53_case_candidate_rows,
    round53_case_records,
    round53_price_field_rows,
    round53_score_profile_rows,
    round53_stage_date_rows,
    round53_summary,
    target_for,
    write_round53_r13_reports,
)


class Round53R13CrossArchetypeRedTeamTests(unittest.TestCase):
    def test_round53_targets_cover_cross_archetype_overlays(self):
        labels = {target.target_id for target in ROUND53_OVERLAY_TARGETS}

        self.assertEqual(len(labels), 14)
        for label in (
            "REDTEAM_ACCOUNTING_TRUST_OVERLAY",
            "FINANCIAL_REPORTING_INTEGRITY_RISK",
            "PRICE_ONLY_RALLY",
            "EVENT_PREMIUM",
            "CYCLICAL_SUCCESS",
            "STRUCTURAL_SUCCESS_ALIGNED",
            "EVIDENCE_GOOD_BUT_PRICE_FAILED",
            "FALSE_POSITIVE_SCORE",
            "CROWDED_RERATING_4B_WATCH",
            "THESIS_BREAK_4C",
            "LEGAL_REGULATORY_REDTEAM",
            "OPERATIONAL_TRUST_BREAK",
            "LEVERAGE_FCF_BREAKDOWN",
            "UNKNOWN_INSUFFICIENT_EVIDENCE",
        ):
            self.assertIn(label, labels)

    def test_new_r13_canonical_archetypes_exist(self):
        expected = (
            E2RArchetype.REDTEAM_ACCOUNTING_TRUST_OVERLAY,
            E2RArchetype.FINANCIAL_REPORTING_INTEGRITY_RISK,
            E2RArchetype.PRICE_ONLY_RALLY,
            E2RArchetype.EVENT_PREMIUM,
            E2RArchetype.CYCLICAL_SUCCESS,
            E2RArchetype.STRUCTURAL_SUCCESS_ALIGNED,
            E2RArchetype.EVIDENCE_GOOD_BUT_PRICE_FAILED,
            E2RArchetype.FALSE_POSITIVE_SCORE,
            E2RArchetype.CROWDED_RERATING_4B_WATCH,
            E2RArchetype.THESIS_BREAK_4C,
            E2RArchetype.LEGAL_REGULATORY_REDTEAM,
            E2RArchetype.OPERATIONAL_TRUST_BREAK,
            E2RArchetype.LEVERAGE_FCF_BREAKDOWN,
            E2RArchetype.UNKNOWN_INSUFFICIENT_EVIDENCE,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_hard_gates_block_green_while_structural_aligned_can_be_green_possible(self):
        accounting = target_for("REDTEAM_ACCOUNTING_TRUST_OVERLAY")
        price_only = target_for("PRICE_ONLY_RALLY")
        structural = target_for("STRUCTURAL_SUCCESS_ALIGNED")
        crowded = target_for("CROWDED_RERATING_4B_WATCH")

        self.assertIsNotNone(accounting)
        self.assertIsNotNone(price_only)
        self.assertIsNotNone(structural)
        self.assertIsNotNone(crowded)
        assert accounting is not None
        assert price_only is not None
        assert structural is not None
        assert crowded is not None
        self.assertTrue(accounting.hard_gate)
        self.assertFalse(accounting.stage3_green_allowed)
        self.assertEqual(accounting.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertFalse(price_only.stage3_green_allowed)
        self.assertIn("no_eps_fcf", price_only.red_flags)
        self.assertEqual(structural.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertTrue(structural.stage3_green_allowed)
        self.assertEqual(crowded.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("valuation_saturation", crowded.red_flags)

    def test_required_round53_cases_are_present_with_stage_dates(self):
        rows = {row["case_id"]: row for row in round53_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND53_CASE_CANDIDATES))
        self.assertEqual(rows["supermicro_accounting_trust_4c_case"]["stage4c_date"], "2024-10-30")
        self.assertEqual(rows["crowdstrike_operational_trust_break_case"]["stage4c_date"], "2024-07-31")
        self.assertEqual(rows["terrausd_luna_algorithmic_stablecoin_break_case"]["stage4c_date"], "2022-05-12")
        self.assertEqual(rows["bluebird_bio_approval_commercialization_failure_case"]["stage4c_date"], "2025-02-21")
        self.assertEqual(rows["novo_nordisk_glp1_4b_to_4c_case"]["stage4b_date"], "2025-07-29")
        self.assertEqual(rows["novo_nordisk_glp1_4b_to_4c_case"]["stage4c_date"], "2026-02-04")
        self.assertEqual(rows["hyundai_motor_valueup_strategy_aligned_case"]["stage2_date"], "2024-08-28")
        self.assertEqual(rows["price_only_theme_rally_case"]["case_type"], "overheat")

    def test_case_records_validate_and_keep_cross_evidence_guardrails(self):
        records = round53_case_records()

        self.assertEqual(len(records), len(ROUND53_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, ROUND53_LARGE_SECTOR)
            self.assertEqual(record.price_validation.price_validation_status, "needs_price_backfill")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("stage3_green_requires_cross_evidence_eps_fcf_price_alignment_no_hard_redteam", record.green_guardrails)
            self.assertIn("hard_redteam_blocks_green", record.green_guardrails)

    def test_score_profile_rows_are_overlay_not_production_scoring(self):
        rows = round53_score_profile_rows()

        self.assertEqual(len(rows), len(ROUND53_OVERLAY_TARGETS))
        for row in rows:
            self.assertEqual(row["production_scoring_changed"], "false")
        by_target = {row["target_id"]: row for row in rows}
        self.assertEqual(by_target["REDTEAM_ACCOUNTING_TRUST_OVERLAY"]["redteam_gate"], "hard_block")
        self.assertEqual(by_target["REDTEAM_ACCOUNTING_TRUST_OVERLAY"]["hard_gate"], "true")
        self.assertEqual(by_target["PRICE_ONLY_RALLY"]["stage3_green_allowed"], "false")
        self.assertEqual(by_target["STRUCTURAL_SUCCESS_ALIGNED"]["stage3_green_allowed"], "true")
        self.assertEqual(by_target["STRUCTURAL_SUCCESS_ALIGNED"]["posture"], "GREEN_POSSIBLE")

    def test_stage_date_and_price_fields_cover_r13_autopsy_needs(self):
        stage_rows = {row["target_id"]: row for row in round53_stage_date_rows()}
        price_fields = {row["field"] for row in round53_price_field_rows()}

        self.assertIn("auditor_resignation", stage_rows["REDTEAM_ACCOUNTING_TRUST_OVERLAY"]["stage4c"])
        self.assertIn("price_only_4b_watch", stage_rows["PRICE_ONLY_RALLY"]["stage4b"])
        self.assertIn("hard_4c", stage_rows["THESIS_BREAK_4C"]["stage4c"])
        self.assertIn("mfe_5d", price_fields)
        self.assertIn("mfe_2y", price_fields)
        self.assertIn("auditor_resignation_flag", price_fields)
        self.assertIn("security_outage_flag", price_fields)
        self.assertIn("score_before_redteam", price_fields)
        self.assertIn("stage_after_redteam", price_fields)

    def test_summary_and_markdown_explain_r13_validation_layer(self):
        summary = round53_summary()
        summary_md = render_round53_summary_markdown()
        gate_plan = render_round53_redteam_gate_plan_markdown()
        price_plan = render_round53_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 14)
        self.assertEqual(summary["case_candidate_count"], 15)
        self.assertEqual(summary["structural_success_count"], 1)
        self.assertEqual(summary["success_candidate_count"], 1)
        self.assertEqual(summary["cyclical_success_count"], 1)
        self.assertEqual(summary["event_premium_count"], 1)
        self.assertEqual(summary["overheat_count"], 1)
        self.assertEqual(summary["failed_rerating_count"], 3)
        self.assertEqual(summary["stage4b_case_count"], 2)
        self.assertEqual(summary["stage4c_case_count"], 7)
        self.assertEqual(summary["hard_gate_target_count"], 6)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("production_scoring_changed: false", summary_md)
        self.assertIn("common validation overlay", summary_md)
        self.assertIn("Do not apply Round53 overlay symbols", gate_plan)
        self.assertIn("score-before-RedTeam", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round53_r13_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r13_round53.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round53_r13_v1.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["target_matrix"].exists())
            self.assertTrue(paths["stage_date_plan"].exists())
            self.assertTrue(paths["redteam_gate_plan"].exists())
            self.assertTrue(paths["price_validation_plan"].exists())
            self.assertTrue(paths["price_fields"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND53_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round53_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round53_r13_cross_archetype_redteam", text)


if __name__ == "__main__":
    unittest.main()
