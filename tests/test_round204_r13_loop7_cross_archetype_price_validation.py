from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from e2r.cli.build_round204_r13_loop7_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round204_r13_loop7_cross_archetype_price_validation import (
    ROUND204_CASE_CANDIDATES,
    ROUND204_GREEN_FORBIDDEN_PATTERNS,
    ROUND204_GREEN_REQUIRED_FIELDS,
    ROUND204_HARD_4C_GATES,
    ROUND204_PRICE_VALIDATION_FIELDS,
    ROUND204_REQUIRED_TARGET_ALIASES,
    render_round204_green_gate_review_markdown,
    render_round204_stage4b_4c_review_markdown,
    round204_audit_payload,
    round204_case_records,
    round204_summary,
    write_round204_r13_loop7_reports,
)


class Round204R13Loop7CrossArchetypePriceValidationTests(unittest.TestCase):
    def test_round204_targets_are_existing_canonical_archetypes(self) -> None:
        canonical_values = {item.value for item in E2RArchetype}

        self.assertGreaterEqual(len(ROUND204_REQUIRED_TARGET_ALIASES), 16)
        self.assertTrue(set(ROUND204_REQUIRED_TARGET_ALIASES.values()).issubset(canonical_values))
        self.assertEqual(
            ROUND204_REQUIRED_TARGET_ALIASES["STRUCTURAL_SUCCESS_BUT_4B_WATCH"],
            E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH.value,
        )
        self.assertEqual(ROUND204_REQUIRED_TARGET_ALIASES["PRICE_ONLY_RALLY"], E2RArchetype.PRICE_ONLY_RALLY.value)

    def test_case_records_validate_and_keep_cross_overlay_guardrails(self) -> None:
        records = round204_case_records()
        for record in records:
            record.validate()
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertIn("full_ohlc_complete_false", record.green_guardrails)

        summary = round204_summary()
        self.assertEqual(summary["stage3_case_count"], 0)
        self.assertEqual(summary["price_validation_completed"], "partial_with_reported_price_anchors")
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["full_ohlc_complete"])

    def test_structural_success_cases_are_aligned_but_4b_watch(self) -> None:
        by_id = {case.case_id: case for case in ROUND204_CASE_CANDIDATES}
        hynix = by_id["r13_sk_hynix_hbm_4b_benchmark"]
        hanwha = by_id["r13_hanwha_aerospace_defense_mfe_4b"]

        self.assertEqual(hynix.primary_archetype, E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH)
        self.assertEqual(hynix.score_price_alignment, "aligned")
        self.assertEqual(hynix.reported_mfe_minimum_pct, 1022.0)
        self.assertEqual(hynix.stage4b_status, "elevated")

        self.assertEqual(hanwha.reported_mfe_minimum_pct, 665.3)
        self.assertEqual(hanwha.mae_1d, -13.0)
        self.assertFalse(hanwha.hard_4c_confirmed)

    def test_price_only_events_do_not_create_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND204_CASE_CANDIDATES}
        kogas = by_id["r13_kogas_resource_price_only"]
        sds = by_id["r13_samsung_sds_kkr_ai_cb_event"]

        self.assertEqual(kogas.primary_archetype, E2RArchetype.PRICE_ONLY_RALLY)
        self.assertEqual(kogas.score_price_alignment, "price_moved_without_evidence")
        self.assertIn("resource_estimate_without_commerciality", kogas.red_flag_fields)
        self.assertIsNone(kogas.stage3_date)
        self.assertEqual(kogas.mfe_1d, 30.0)

        self.assertIn("ai_capex_or_partnership_without_revenue", sds.red_flag_fields)
        self.assertEqual(sds.mfe_1d, 20.8)
        self.assertIsNone(sds.stage3_date)

    def test_hard_4c_cases_are_operational_or_contract_breaks(self) -> None:
        by_id = {case.case_id: case for case in ROUND204_CASE_CANDIDATES}
        jeju = by_id["r13_jeju_air_fatal_crash_hard_4c"]
        lges = by_id["r13_lges_contract_cancellation_4c"]
        lnf = by_id["r13_lnf_tesla_contract_value_collapse"]

        self.assertTrue(jeju.hard_4c_confirmed)
        self.assertEqual(jeju.primary_archetype, E2RArchetype.OPERATIONAL_TRUST_BREAK)
        self.assertEqual(jeju.mae_1d, -15.7)
        self.assertIn("fatal_safety_accident", jeju.red_flag_fields)

        self.assertTrue(lges.hard_4c_confirmed)
        self.assertEqual(lges.lost_revenue_vs_prior_revenue_pct, 52.7)
        self.assertIn("contract_cancellation", lges.red_flag_fields)

        self.assertTrue(lnf.hard_4c_confirmed)
        self.assertEqual(lnf.contract_value_drawdown_pct, -99.999745)
        self.assertIn("contract_value_collapse", lnf.red_flag_fields)

    def test_capital_raise_overlay_is_4b_not_automatic_4c(self) -> None:
        overlay = next(
            case
            for case in ROUND204_CASE_CANDIDATES
            if case.case_id == "r13_hanwha_aerospace_capital_raise_4b_not_4c"
        )

        self.assertEqual(overlay.primary_archetype, E2RArchetype.CROWDED_RERATING_4B_WATCH)
        self.assertEqual(overlay.case_type, "4b_watch")
        self.assertEqual(overlay.stage4b_status, "elevated")
        self.assertFalse(overlay.hard_4c_confirmed)
        self.assertIn("not_automatic_4c", overlay.red_flag_fields)

    def test_green_gate_requires_price_path_alignment_and_blocks_price_only(self) -> None:
        required = set(ROUND204_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND204_GREEN_FORBIDDEN_PATTERNS)
        markdown = render_round204_green_gate_review_markdown()

        self.assertIn("price_path_alignment_confirmed", required)
        self.assertIn("no_hard_redteam", required)
        self.assertIn("not_saturated_4b", required)
        self.assertIn("resource_estimate_without_commerciality", forbidden)
        self.assertIn("ai_capex_or_partnership_without_revenue", forbidden)
        self.assertIn("contract_headline_without_calloff", forbidden)
        self.assertIn("Do not apply these weights to production scoring yet.", markdown)

    def test_price_validation_fields_include_reported_anchor_and_contract_collapse(self) -> None:
        fields = set(ROUND204_PRICE_VALIDATION_FIELDS)

        self.assertIn("price_data_source", fields)
        self.assertIn("full_ohlc_available", fields)
        self.assertIn("reported_return_anchor", fields)
        self.assertIn("reported_mfe_minimum_pct", fields)
        self.assertIn("contract_value_drawdown_pct", fields)
        self.assertIn("lost_revenue_vs_prior_revenue_pct", fields)

    def test_stage4b_4c_review_contains_cross_archetype_hard_gates(self) -> None:
        review = render_round204_stage4b_4c_review_markdown()

        self.assertIn("fatal_safety_accident", ROUND204_HARD_4C_GATES)
        self.assertIn("contract_value_collapse", ROUND204_HARD_4C_GATES)
        self.assertIn("accounting_or_disclosure_trust_break", ROUND204_HARD_4C_GATES)
        self.assertIn("4B is not automatic hard 4C", review)
        self.assertIn("Operational trust", review)

    def test_summary_and_audit_payload_are_calibration_only(self) -> None:
        audit = round204_audit_payload()

        self.assertEqual(audit["source_round"], "docs/round/round_204.md")
        self.assertFalse(audit["summary"]["production_scoring_changed"])
        self.assertFalse(audit["summary"]["candidate_generation_input"])
        self.assertTrue(audit["summary"]["shadow_weight_only"])
        self.assertIn("do_not_use_round204_cases_as_candidate_generation_input", audit["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])
        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round204_r13_loop7_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)

            records = load_case_library(paths["cases"])
            self.assertEqual(len(records), len(ROUND204_CASE_CANDIDATES))
            self.assertIn("price_path_alignment", paths["score_adjustments"].read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
