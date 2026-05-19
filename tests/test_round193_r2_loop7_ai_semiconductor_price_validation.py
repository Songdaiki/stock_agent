import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round193_r2_loop7_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round193_r2_loop7_ai_semiconductor_price_validation import (
    ROUND193_CASE_CANDIDATES,
    ROUND193_GREEN_FORBIDDEN_PATTERNS,
    ROUND193_GREEN_REQUIRED_FIELDS,
    ROUND193_PRICE_BACKFILL_FIELDS,
    ROUND193_REQUIRED_TARGET_ALIASES,
    ROUND193_SCORE_ADJUSTMENTS,
    render_round193_green_gate_review_markdown,
    render_round193_stage4b_4c_review_markdown,
    round193_audit_payload,
    round193_case_records,
    round193_case_rows,
    round193_price_backfill_field_rows,
    round193_score_adjustment_rows,
    round193_summary,
    write_round193_r2_loop7_reports,
)


class Round193R2Loop7AISemiconductorPriceValidationTests(unittest.TestCase):
    def test_round193_targets_map_round_labels_to_canonical_archetypes(self):
        self.assertGreaterEqual(len(ROUND193_REQUIRED_TARGET_ALIASES), 17)
        self.assertEqual(
            ROUND193_REQUIRED_TARGET_ALIASES["REDTEAM_OPERATIONAL_TRUST"],
            E2RArchetype.HBM_CATCHUP_EXECUTION_RISK.value,
        )
        self.assertEqual(
            ROUND193_REQUIRED_TARGET_ALIASES["POLICY_FOUNDRY_EVENT"],
            E2RArchetype.AI_CHIP_FABRIC_INFRA.value,
        )
        for canonical in ROUND193_REQUIRED_TARGET_ALIASES.values():
            self.assertIsInstance(E2RArchetype(canonical), E2RArchetype)

    def test_case_records_validate_and_keep_shadow_only_guardrails(self):
        records = {record.case_id: record for record in round193_case_records()}

        self.assertEqual(len(records), 6)
        self.assertEqual(records["hanmi_semiconductor_tsv_tc_bonder_4b_watch"].case_type, "structural_success")
        self.assertEqual(records["hanmi_semiconductor_tsv_tc_bonder_4b_watch"].price_validation.stage4b_price, 139100.0)
        self.assertEqual(records["db_hitek_policy_foundry_event_premium"].case_type, "event_premium")
        self.assertEqual(records["isu_petasis_ai_server_pcb_insufficient_evidence"].case_type, "overheat")
        self.assertEqual(records["sk_hynix_hbm_2026_4b_benchmark"].case_type, "4b_watch")
        for record in records.values():
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertEqual(record.price_validation.price_validation_status, "needs_ohlc_backfill")

    def test_design_win_policy_and_ai_pcb_do_not_create_green(self):
        rows = {row["case_id"]: row for row in round193_case_rows()}

        self.assertEqual(rows["gaonchips_pfn_samsung_2nm_design_win_stage2"]["stage3_date"], "")
        self.assertIn("deferred_until_tapeout", rows["gaonchips_pfn_samsung_2nm_design_win_stage2"]["stage3_decision"])
        self.assertEqual(rows["db_hitek_policy_foundry_event_premium"]["score_price_alignment"], "price_moved_without_evidence")
        self.assertEqual(rows["isu_petasis_ai_server_pcb_insufficient_evidence"]["rerating_result"], "theme_overheat")

    def test_stage4b_benchmark_is_separated_from_hard_4c(self):
        rows = {row["case_id"]: row for row in round193_case_rows()}

        self.assertEqual(rows["hanmi_semiconductor_tsv_tc_bonder_4b_watch"]["stage4b_status"], "watch")
        self.assertEqual(rows["sk_hynix_hbm_2026_4b_benchmark"]["stage4b_status"], "benchmark")
        self.assertEqual(rows["samsung_electronics_hbm_catchup_failed_2025_watch"]["hard_4c_confirmed"], "false")
        review = render_round193_stage4b_4c_review_markdown()
        self.assertIn("benchmark", review)
        self.assertIn("HBM customer qualification failure", review)

    def test_green_gate_strengthens_customer_revenue_margin_without_production_change(self):
        required = set(ROUND193_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND193_GREEN_FORBIDDEN_PATTERNS)
        adjustments = {row["axis"]: row for row in round193_score_adjustment_rows()}
        markdown = render_round193_green_gate_review_markdown()

        self.assertIn("company_level_customer_evidence", required)
        self.assertIn("revenue_recognition_path", required)
        self.assertIn("eps_fcf_revision", required)
        self.assertIn("ai_name_only", forbidden)
        self.assertIn("unconfirmed_media_report", forbidden)
        self.assertEqual(adjustments["customer_visibility"]["points"], "3")
        self.assertEqual(adjustments["ai_keyword"]["points"], "-4")
        self.assertIn("Do not apply these weights to production scoring yet", markdown)

    def test_price_backfill_fields_include_r2_specific_evidence(self):
        fields = {row["field"] for row in round193_price_backfill_field_rows()}

        self.assertGreaterEqual(len(ROUND193_PRICE_BACKFILL_FIELDS), 50)
        for field in (
            "relative_strength_vs_hbm_basket",
            "relative_strength_vs_ai_server_pcb_basket",
            "customer_visibility",
            "design_win_flag",
            "volume_production_flag",
            "hbm_lta_flag",
            "policy_foundry_flag",
            "stock_price_rally_before_evidence_flag",
            "hard_4c_confirmed",
        ):
            self.assertIn(field, fields)

    def test_summary_and_audit_payload_are_explicitly_calibration_only(self):
        summary = round193_summary()
        payload = round193_audit_payload()

        self.assertEqual(summary["case_candidate_count"], len(ROUND193_CASE_CANDIDATES))
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["candidate_generation_input"])
        self.assertTrue(summary["shadow_weight_only"])
        self.assertIn("do_not_use_round193_cases_as_candidate_generation_input", payload["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self):
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])

        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = write_round193_r2_loop7_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)
            records = load_case_library(root / "cases.jsonl")
            self.assertEqual(len(records), 6)
            self.assertIn("Stage 3", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("customer_visibility", paths["score_adjustments"].read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
