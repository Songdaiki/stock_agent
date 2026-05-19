import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round192_r1_loop7_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round192_r1_loop7_industrial_infra_price_validation import (
    ROUND192_CASE_CANDIDATES,
    ROUND192_GREEN_FORBIDDEN_PATTERNS,
    ROUND192_GREEN_REQUIRED_FIELDS,
    ROUND192_PRICE_BACKFILL_FIELDS,
    ROUND192_REQUIRED_TARGET_ALIASES,
    ROUND192_SCORE_ADJUSTMENTS,
    render_round192_green_gate_review_markdown,
    render_round192_stage4b_4c_review_markdown,
    round192_audit_payload,
    round192_case_records,
    round192_case_rows,
    round192_price_backfill_field_rows,
    round192_score_adjustment_rows,
    round192_summary,
    write_round192_r1_loop7_reports,
)


class Round192R1Loop7IndustrialInfraPriceValidationTests(unittest.TestCase):
    def test_round192_targets_map_round_label_aliases_to_canonical_archetypes(self):
        self.assertEqual(len(ROUND192_REQUIRED_TARGET_ALIASES), 11)
        self.assertEqual(
            ROUND192_REQUIRED_TARGET_ALIASES["CROWDING_4B_WATCH"],
            E2RArchetype.CROWDED_RERATING_4B_WATCH.value,
        )
        for canonical in ROUND192_REQUIRED_TARGET_ALIASES.values():
            self.assertIsInstance(E2RArchetype(canonical), E2RArchetype)

    def test_case_records_validate_and_keep_shadow_only_guardrails(self):
        records = {record.case_id: record for record in round192_case_records()}

        self.assertEqual(len(records), 7)
        self.assertEqual(records["hyundai_rotem_k2_export_price_path"].case_type, "structural_success")
        self.assertEqual(records["hyundai_rotem_k2_export_price_path"].price_validation.stage2_price, 41300.0)
        self.assertEqual(records["hd_hyundai_marine_solution_ipo_price_only_rally"].case_type, "event_premium")
        self.assertEqual(
            records["hd_hyundai_marine_solution_ipo_price_only_rally"].score_price_alignment,
            "price_moved_without_evidence",
        )
        for record in records.values():
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertEqual(record.price_validation.price_validation_status, "needs_ohlc_backfill")

    def test_stage4b_is_separated_from_hard_4c(self):
        rows = {row["case_id"]: row for row in round192_case_rows()}

        self.assertEqual(rows["hanwha_aerospace_poland_chunmoo_4b_timing"]["stage4b_status"], "elevated")
        self.assertEqual(rows["hanwha_aerospace_poland_chunmoo_4b_timing"]["hard_4c_confirmed"], "false")
        self.assertEqual(rows["hanwha_ocean_sanction_watch_not_hard_4c"]["stage4b_status"], "sanction_watch")
        self.assertEqual(rows["hanwha_ocean_sanction_watch_not_hard_4c"]["hard_4c_confirmed"], "false")
        review = render_round192_stage4b_4c_review_markdown()
        self.assertIn("watch", review)
        self.assertIn("hard 4C is not confirmed", review)

    def test_green_gate_strengthens_contract_quality_without_production_change(self):
        required = set(ROUND192_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND192_GREEN_FORBIDDEN_PATTERNS)
        adjustments = {row["axis"]: row for row in round192_score_adjustment_rows()}
        markdown = render_round192_green_gate_review_markdown()

        self.assertIn("delivery_schedule", required)
        self.assertIn("opm_or_eps_revision", required)
        self.assertIn("margin_unknown", forbidden)
        self.assertIn("ipo_or_supply_demand_price_spike", forbidden)
        self.assertEqual(adjustments["op_eps_revision"]["points"], "3")
        self.assertEqual(adjustments["order_headline"]["points"], "-3")
        self.assertIn("Do not apply these weights to production scoring yet", markdown)

    def test_price_backfill_fields_include_round192_windows_and_relative_strength(self):
        fields = {row["field"] for row in round192_price_backfill_field_rows()}

        self.assertGreaterEqual(len(ROUND192_PRICE_BACKFILL_FIELDS), 40)
        for field in (
            "MFE_20D",
            "MFE_252D",
            "MAE_120D",
            "relative_strength_vs_defense_basket",
            "relative_strength_vs_shipbuilding_basket",
            "government_financing_flag",
            "stage4b_status",
            "hard_4c_confirmed",
        ):
            self.assertIn(field, fields)

    def test_summary_and_audit_payload_are_explicitly_calibration_only(self):
        summary = round192_summary()
        payload = round192_audit_payload()

        self.assertEqual(summary["case_candidate_count"], len(ROUND192_CASE_CANDIDATES))
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["candidate_generation_input"])
        self.assertTrue(summary["shadow_weight_only"])
        self.assertIn("do_not_use_round192_cases_as_candidate_generation_input", payload["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self):
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])

        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = write_round192_r1_loop7_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)
            records = load_case_library(root / "cases.jsonl")
            self.assertEqual(len(records), 7)
            self.assertIn("Stage 3", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("op_eps_revision", paths["score_adjustments"].read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
