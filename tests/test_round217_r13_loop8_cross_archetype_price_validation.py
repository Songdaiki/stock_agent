from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from e2r.cli.build_round217_r13_loop8_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round217_r13_loop8_cross_archetype_price_validation import (
    ROUND217_CASE_CANDIDATES,
    ROUND217_GREEN_FORBIDDEN_PATTERNS,
    ROUND217_GREEN_REQUIRED_FIELDS,
    ROUND217_HARD_4C_GATES,
    ROUND217_PRICE_VALIDATION_FIELDS,
    ROUND217_REQUIRED_TARGET_ALIASES,
    ROUND217_SHADOW_WEIGHT_ROWS,
    ROUND217_STAGE4B_WATCH_TRIGGERS,
    render_round217_green_gate_review_markdown,
    render_round217_stage4b_4c_review_markdown,
    round217_audit_payload,
    round217_case_records,
    round217_shadow_weight_rows,
    round217_summary,
    write_round217_r13_loop8_reports,
)


class Round217R13Loop8CrossArchetypePriceValidationTests(unittest.TestCase):
    def test_targets_are_existing_canonical_archetypes(self) -> None:
        canonical_values = {item.value for item in E2RArchetype}

        self.assertGreaterEqual(len(ROUND217_REQUIRED_TARGET_ALIASES), 17)
        self.assertTrue(set(ROUND217_REQUIRED_TARGET_ALIASES.values()).issubset(canonical_values))
        self.assertEqual(
            ROUND217_REQUIRED_TARGET_ALIASES["CONTRACT_QUALITY_BREAK"],
            E2RArchetype.CONTRACT_QUALITY_BREAK.value,
        )
        self.assertEqual(
            ROUND217_REQUIRED_TARGET_ALIASES["ORDER_TO_REVENUE_CONVERSION"],
            E2RArchetype.ORDER_TO_REVENUE_CONVERSION.value,
        )
        self.assertEqual(
            ROUND217_REQUIRED_TARGET_ALIASES["STRATEGIC_MATERIALS_WITH_GOVERNANCE_OVERLAY"],
            E2RArchetype.STRATEGIC_MATERIALS_WITH_GOVERNANCE_OVERLAY.value,
        )

    def test_case_records_validate_and_remain_calibration_only(self) -> None:
        records = round217_case_records()
        for record in records:
            record.validate()
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertIn("shadow_weight_only_true", record.green_guardrails)
            self.assertIn("full_ohlc_complete_false", record.green_guardrails)

        summary = round217_summary()
        self.assertEqual(summary["case_candidate_count"], 8)
        self.assertEqual(summary["structural_success_count"], 2)
        self.assertEqual(summary["event_premium_count"], 1)
        self.assertEqual(summary["overheat_count"], 1)
        self.assertEqual(summary["hard_4c_case_count"], 2)
        self.assertEqual(summary["stage3_case_count"], 2)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["candidate_generation_input"])
        self.assertFalse(summary["full_ohlc_complete"])

    def test_structural_success_cases_have_price_alignment_anchors(self) -> None:
        by_id = {case.case_id: case for case in ROUND217_CASE_CANDIDATES}
        hynix = by_id["r13_loop8_sk_hynix_hbm_stage3_4b"]
        rotem = by_id["r13_loop8_hyundai_rotem_k2_delivery_aligned"]

        self.assertEqual(hynix.primary_archetype, E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH)
        self.assertEqual(hynix.stage3_date.isoformat(), "2024-06-25")
        self.assertEqual(hynix.stage4b_date.isoformat(), "2026-05-14")
        self.assertEqual(hynix.stage3_price_anchor, 222000.0)
        self.assertEqual(hynix.peak_price_anchor, 1946000.0)
        self.assertEqual(hynix.reported_mfe_pct, 776.6)
        self.assertEqual(hynix.reported_market_cap_mfe_pct, 842.0)
        self.assertEqual(hynix.score_price_alignment, "aligned")

        self.assertEqual(rotem.primary_archetype, E2RArchetype.ORDER_TO_REVENUE_CONVERSION)
        self.assertEqual(rotem.stage3_price_anchor, 41300.0)
        self.assertEqual(rotem.mfe_1d, 9.3)
        self.assertEqual(rotem.extra_price_metrics["relative_outperformance_vs_kospi_pp"], 9.6)
        self.assertEqual(rotem.extra_price_metrics["poland_second_contract_usd_bn"], 6.5)

    def test_capital_raise_is_4b_not_automatic_4c(self) -> None:
        hanwha = next(
            case
            for case in ROUND217_CASE_CANDIDATES
            if case.case_id == "r13_loop8_hanwha_aero_dilution_4b_not_4c"
        )

        self.assertEqual(hanwha.case_type, "4b_watch")
        self.assertEqual(hanwha.stage4b_status, "elevated")
        self.assertEqual(hanwha.mae_1d, -13.0)
        self.assertEqual(hanwha.extra_price_metrics["capital_raise_krw_trn"], 3.6)
        self.assertFalse(hanwha.hard_4c_confirmed)
        self.assertIn("not_automatic_4c", hanwha.red_flag_fields)

    def test_price_only_resource_and_stablecoin_events_do_not_create_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND217_CASE_CANDIDATES}
        kogas = by_id["r13_loop8_kogas_resource_price_only"]
        stablecoin = by_id["r13_loop8_stablecoin_theme_price_only"]

        self.assertEqual(kogas.primary_archetype, E2RArchetype.PRICE_ONLY_RALLY)
        self.assertEqual(kogas.mfe_1d, 30.0)
        self.assertEqual(kogas.stage4b_date.isoformat(), "2024-06-03")
        self.assertEqual(kogas.score_price_alignment, "price_moved_without_evidence")
        self.assertIn("resource_estimate_without_commerciality", kogas.red_flag_fields)
        self.assertIsNone(kogas.stage3_date)

        self.assertEqual(stablecoin.primary_archetype, E2RArchetype.KRW_STABLECOIN_POLICY_THEME)
        self.assertEqual(stablecoin.case_type, "overheat")
        self.assertEqual(stablecoin.extra_price_metrics["me2on_mfe_month_pct"], 200.0)
        self.assertEqual(stablecoin.score_price_alignment, "price_moved_without_evidence")
        self.assertIn("stablecoin_policy_theme_only", stablecoin.red_flag_fields)

    def test_hard_4c_cases_cover_contract_quality_and_operational_trust(self) -> None:
        by_id = {case.case_id: case for case in ROUND217_CASE_CANDIDATES}
        contract = by_id["r13_loop8_lges_lnf_contract_quality_4c"]
        jeju = by_id["r13_loop8_jeju_air_operational_trust_hard_4c"]

        self.assertTrue(contract.hard_4c_confirmed)
        self.assertEqual(contract.primary_archetype, E2RArchetype.CONTRACT_QUALITY_BREAK)
        self.assertEqual(contract.contract_value_drawdown_pct, -99.999745)
        self.assertEqual(contract.lost_revenue_vs_prior_revenue_pct, 52.7)
        self.assertIn("contract_value_collapse", contract.red_flag_fields)

        self.assertTrue(jeju.hard_4c_confirmed)
        self.assertEqual(jeju.primary_archetype, E2RArchetype.OPERATIONAL_TRUST_BREAK)
        self.assertEqual(jeju.stage4c_price_anchor, 6920.0)
        self.assertEqual(jeju.mae_1d, -15.7)
        self.assertIn("fatal_safety_accident", jeju.red_flag_fields)

    def test_korea_zinc_is_stage2_watch_not_green_until_governance_clears(self) -> None:
        zinc = next(
            case
            for case in ROUND217_CASE_CANDIDATES
            if case.case_id == "r13_loop8_korea_zinc_strategic_governance_watch"
        )

        self.assertEqual(zinc.primary_archetype, E2RArchetype.STRATEGIC_MATERIALS_WITH_GOVERNANCE_OVERLAY)
        self.assertEqual(zinc.case_type, "success_candidate")
        self.assertEqual(zinc.stage2_date.isoformat(), "2025-12-01")
        self.assertIsNone(zinc.stage3_date)
        self.assertEqual(zinc.extra_price_metrics["us_smelter_project_usd_bn"], 7.4)
        self.assertIn("dilution_without_clear_fcf", zinc.red_flag_fields)

    def test_green_gate_and_stage4_rules_are_explicit(self) -> None:
        required = set(ROUND217_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND217_GREEN_FORBIDDEN_PATTERNS)
        green_markdown = render_round217_green_gate_review_markdown()
        stage_review = render_round217_stage4b_4c_review_markdown()

        self.assertIn("price_path_after_evidence_confirmed", required)
        self.assertIn("no_hard_redteam", required)
        self.assertIn("contract_operational_governance_trust_passed", required)
        self.assertIn("resource_estimate_without_commerciality", forbidden)
        self.assertIn("stablecoin_policy_theme_only", forbidden)
        self.assertIn("contract_headline_without_calloff", forbidden)
        self.assertIn("Do not apply these weights to production scoring yet.", green_markdown)
        self.assertIn("large_capital_raise_cb_or_share_issue", ROUND217_STAGE4B_WATCH_TRIGGERS)
        self.assertIn("contract_value_collapse", ROUND217_HARD_4C_GATES)
        self.assertIn("fatal_safety_accident", ROUND217_HARD_4C_GATES)
        self.assertIn("r13_loop8_lges_lnf_contract_quality_4c", stage_review)

    def test_shadow_weights_cover_success_4b_price_only_and_hard_4c(self) -> None:
        shadow_text = "\n".join(str(row) for row in round217_shadow_weight_rows())

        self.assertEqual(len(ROUND217_SHADOW_WEIGHT_ROWS), 8)
        self.assertIn("STRUCTURAL_SUCCESS_ALIGNED", shadow_text)
        self.assertIn("PRICE_ONLY_RALLY", shadow_text)
        self.assertIn("CONTRACT_QUALITY_BREAK", shadow_text)
        self.assertIn("OPERATIONAL_TRUST_BREAK", shadow_text)
        self.assertIn("KRW_STABLECOIN_POLICY_THEME", shadow_text)

    def test_price_validation_fields_include_cross_archetype_anchors(self) -> None:
        fields = set(ROUND217_PRICE_VALIDATION_FIELDS)

        self.assertIn("stage3_price", fields)
        self.assertIn("peak_return_from_stage3_pct", fields)
        self.assertIn("market_cap_mfe_minimum_pct", fields)
        self.assertIn("contract_value_drawdown_pct", fields)
        self.assertIn("lost_revenue_vs_prior_revenue_pct", fields)
        self.assertIn("price_validation_status", fields)

    def test_summary_and_audit_payload_are_calibration_only(self) -> None:
        audit = round217_audit_payload()

        self.assertEqual(audit["source_round"], "docs/round/round_217.md")
        self.assertFalse(audit["summary"]["production_scoring_changed"])
        self.assertFalse(audit["summary"]["candidate_generation_input"])
        self.assertTrue(audit["summary"]["shadow_weight_only"])
        self.assertIn("do_not_use_round217_cases_as_candidate_generation_input", audit["what_not_to_change"])
        self.assertIn("do_not_lower_stage3_green_thresholds", audit["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])
        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round217_r13_loop8_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)

            records = load_case_library(paths["cases"])
            self.assertEqual(len(records), len(ROUND217_CASE_CANDIDATES))
            self.assertIn("SK하이닉스", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("price_path_alignment", paths["score_adjustments"].read_text(encoding="utf-8"))
            self.assertIn("KRW_STABLECOIN_POLICY_THEME", paths["shadow_weights"].read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
