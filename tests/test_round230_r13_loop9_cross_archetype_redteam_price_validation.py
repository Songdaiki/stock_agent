from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from e2r.cli.build_round230_r13_loop9_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round230_r13_loop9_cross_archetype_redteam_price_validation import (
    ROUND230_CASE_CANDIDATES,
    ROUND230_DEFAULT_STAGE3_BIAS,
    ROUND230_GREEN_FORBIDDEN_PATTERNS,
    ROUND230_GREEN_REQUIRED_FIELDS,
    ROUND230_HARD_4C_GATES,
    ROUND230_LARGE_SECTOR,
    ROUND230_PRICE_VALIDATION_FIELDS,
    ROUND230_REQUIRED_TARGET_ALIASES,
    ROUND230_SCORE_ADJUSTMENTS,
    ROUND230_SHADOW_WEIGHT_ROWS,
    ROUND230_STAGE4B_WATCH_TRIGGERS,
    render_round230_green_gate_review_markdown,
    render_round230_stage4b_4c_review_markdown,
    round230_audit_payload,
    round230_case_records,
    round230_case_rows,
    round230_deep_sub_archetype_rows,
    round230_shadow_weight_rows,
    round230_summary,
    write_round230_r13_loop9_reports,
)


class Round230R13Loop9CrossArchetypeRedTeamPriceValidationTests(unittest.TestCase):
    def test_round230_targets_map_to_existing_canonical_archetypes(self) -> None:
        canonical_values = {item.value for item in E2RArchetype}

        self.assertGreaterEqual(len(ROUND230_REQUIRED_TARGET_ALIASES), 15)
        self.assertTrue(set(ROUND230_REQUIRED_TARGET_ALIASES.values()).issubset(canonical_values))
        self.assertEqual(
            ROUND230_REQUIRED_TARGET_ALIASES["SECURITY_PRIVACY_TRUST_BREAK"],
            E2RArchetype.SECURITY_OPERATIONAL_TRUST_OVERLAY.value,
        )
        self.assertEqual(
            ROUND230_REQUIRED_TARGET_ALIASES["POLICY_RESOURCE_EVENT_PREMIUM"],
            E2RArchetype.DOMESTIC_RESOURCE_DISCOVERY_EVENT.value,
        )
        self.assertEqual(
            ROUND230_REQUIRED_TARGET_ALIASES["K_BEAUTY_DEVICE_GLOBAL_BRAND"],
            E2RArchetype.BEAUTY_DEVICE_EXPORT.value,
        )

    def test_case_records_validate_and_are_calibration_only(self) -> None:
        records = round230_case_records()
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, ROUND230_LARGE_SECTOR)
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertIn("full_ohlc_complete_false", record.green_guardrails)
            self.assertIn("r13_default_stage3_bias_redteam_first_after_price_validation", record.green_guardrails)

        summary = round230_summary()
        self.assertEqual(summary["case_candidate_count"], 8)
        self.assertEqual(summary["structural_success_count"], 2)
        self.assertEqual(summary["success_candidate_count"], 1)
        self.assertEqual(summary["failed_rerating_count"], 1)
        self.assertEqual(summary["overheat_count"], 1)
        self.assertEqual(summary["hard_4c_case_count"], 2)
        self.assertEqual(summary["stage3_case_count"], 2)
        self.assertEqual(summary["r13_default_stage3_bias"], ROUND230_DEFAULT_STAGE3_BIAS)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["full_ohlc_complete"])

    def test_sk_hynix_and_apr_validate_structural_success_but_need_4b_watch(self) -> None:
        by_id = {case.case_id: case for case in ROUND230_CASE_CANDIDATES}
        hynix = by_id["r13_loop9_sk_hynix_hbm_stage3_4b"]
        apr = by_id["r13_loop9_apr_medicube_structural_4b"]

        self.assertEqual(hynix.primary_archetype, E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH)
        self.assertEqual(hynix.stage3_date.isoformat(), "2024-06-25")
        self.assertEqual(hynix.stage3_price_anchor, 222000.0)
        self.assertEqual(hynix.peak_price_anchor, 1447000.0)
        self.assertEqual(hynix.peak_return_from_stage3_pct, 551.8)
        self.assertEqual(hynix.rerating_result, "true_rerating")
        self.assertIn("market_cap_milestone_headline", hynix.red_flag_fields)

        self.assertEqual(apr.primary_archetype, E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH)
        self.assertEqual(apr.stage2_price_anchor, 158300.0)
        self.assertEqual(apr.extra_price_metrics["q4_2025_revenue_growth_pct"], 124.0)
        self.assertEqual(apr.extra_price_metrics["q4_2025_overseas_growth_pct"], 203.0)
        self.assertEqual(apr.extra_price_metrics["medicube_revenue_share_pct"], 91.7)
        self.assertIn("single_brand_device_concentration", apr.red_flag_fields)

    def test_samsung_sds_and_hyundai_steel_are_not_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND230_CASE_CANDIDATES}
        sds = by_id["r13_loop9_samsung_sds_kkr_ai_event_4b"]
        steel = by_id["r13_loop9_hyundai_steel_policy_capex_failure"]

        self.assertEqual(sds.primary_archetype, E2RArchetype.AI_CLOUD_CAPITAL_ALLOCATION)
        self.assertEqual(sds.stage2_date.isoformat(), "2026-04-15")
        self.assertEqual(sds.mfe_1d, 20.8)
        self.assertEqual(sds.extra_price_metrics["relative_intraday_outperformance_vs_kospi_pp"], 17.8)
        self.assertIn("ai_capital_allocation_without_revenue", sds.red_flag_fields)
        self.assertEqual(sds.round_stage_failure_label, "should_not_be_green_yet")

        self.assertEqual(steel.primary_archetype, E2RArchetype.EVIDENCE_GOOD_BUT_PRICE_FAILED)
        self.assertEqual(steel.mae_1d, -21.2)
        self.assertEqual(steel.extra_price_metrics["relative_underperformance_vs_kospi_pp"], -15.7)
        self.assertIn("capex_without_funding_or_margin", steel.red_flag_fields)
        self.assertEqual(steel.round_alignment_label, "false_positive_score_prevention")

    def test_contract_safety_and_security_cases_are_4c_gates(self) -> None:
        by_id = {case.case_id: case for case in ROUND230_CASE_CANDIDATES}
        contract = by_id["r13_loop9_lges_lnf_contract_quality_hard_4c"]
        jeju = by_id["r13_loop9_jeju_air_operational_safety_hard_4c"]
        skt = by_id["r13_loop9_skt_security_privacy_4c_watch"]

        self.assertTrue(contract.hard_4c_confirmed)
        self.assertEqual(contract.primary_archetype, E2RArchetype.CONTRACT_QUALITY_BREAK)
        self.assertEqual(contract.extra_price_metrics["lost_revenue_vs_2024_revenue_pct"], 52.7)
        self.assertEqual(contract.extra_price_metrics["lnf_contract_value_drawdown_pct"], -99.999745)
        self.assertIn("contract_value_collapse", contract.red_flag_fields)

        self.assertTrue(jeju.hard_4c_confirmed)
        self.assertEqual(jeju.primary_archetype, E2RArchetype.OPERATIONAL_TRUST_BREAK)
        self.assertEqual(jeju.mae_1d, -15.7)
        self.assertEqual(jeju.extra_price_metrics["fatalities"], 179.0)
        self.assertIn("fatal_safety_accident", jeju.red_flag_fields)

        self.assertFalse(skt.hard_4c_confirmed)
        self.assertEqual(skt.primary_archetype, E2RArchetype.SECURITY_OPERATIONAL_TRUST_OVERLAY)
        self.assertEqual(skt.mae_1d, -8.5)
        self.assertEqual(skt.extra_price_metrics["revenue_forecast_cut_2025_krw_bn"], 800.0)
        self.assertEqual(skt.round_stage_failure_label, "strong_4C_watch")

    def test_policy_resource_stablecoin_cluster_is_price_moved_without_evidence(self) -> None:
        by_id = {case.case_id: case for case in ROUND230_CASE_CANDIDATES}
        cluster = by_id["r13_loop9_policy_resource_stablecoin_price_only"]

        self.assertEqual(cluster.primary_archetype, E2RArchetype.PRICE_ONLY_RALLY)
        self.assertEqual(cluster.mfe_1d, 30.0)
        self.assertEqual(cluster.stage4b_price_anchor, 38700.0)
        self.assertEqual(cluster.extra_price_metrics["kogas_implied_pre_event_reference_price"], 29769.0)
        self.assertEqual(cluster.extra_price_metrics["me2on_mfe_month_pct"], 200.0)
        self.assertFalse(cluster.extra_price_metrics["regulated_revenue_confirmed"])
        self.assertEqual(cluster.score_price_alignment, "price_moved_without_evidence")

    def test_green_gate_and_4c_rules_are_explicit(self) -> None:
        required = set(ROUND230_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND230_GREEN_FORBIDDEN_PATTERNS)
        review = render_round230_green_gate_review_markdown()
        stage_review = render_round230_stage4b_4c_review_markdown()

        self.assertIn("price_path_after_evidence", required)
        self.assertIn("stage3_to_large_mfe_confirmation", required)
        self.assertIn("contract_operational_governance_security_trust_passed", required)
        self.assertIn("stablecoin_policy_theme_only", forbidden)
        self.assertIn("ai_capital_allocation_without_revenue", forbidden)
        self.assertIn("fatal_safety_accident", forbidden)
        self.assertIn("market_cap_milestone_headline", ROUND230_STAGE4B_WATCH_TRIGGERS)
        self.assertIn("contract_value_collapse", ROUND230_HARD_4C_GATES)
        self.assertIn("Do not apply these weights to production scoring yet.", review)
        self.assertIn("4C is about thesis break", stage_review)

    def test_price_fields_score_axes_shadow_and_deep_rows_cover_round230(self) -> None:
        fields = set(ROUND230_PRICE_VALIDATION_FIELDS)
        axes = {item.axis for item in ROUND230_SCORE_ADJUSTMENTS}
        shadow_rows = {row["archetype"]: row for row in round230_shadow_weight_rows()}
        deep_rows = round230_deep_sub_archetype_rows()

        self.assertIn("peak_return_from_stage3", fields)
        self.assertIn("trust_break_cost_anchor", fields)
        self.assertIn("price_path_alignment", axes)
        self.assertIn("stablecoin_policy_theme_only", axes)
        self.assertIn("hard_4c_early_warning", axes)
        self.assertEqual(len(ROUND230_SHADOW_WEIGHT_ROWS), 8)
        self.assertEqual(shadow_rows["STRUCTURAL_SUCCESS_BUT_4B_WATCH"]["4b_watch_sensitivity"], "+5")
        self.assertEqual(shadow_rows["PRICE_ONLY_RALLY"]["event_penalty"], "-5")
        self.assertTrue(any("SK Hynix HBM" in row["terms"] for row in deep_rows))
        self.assertTrue(any("SK Telecom" in row["terms"] for row in deep_rows))

    def test_summary_and_audit_payload_keep_non_production_guardrails(self) -> None:
        audit = round230_audit_payload()

        self.assertEqual(audit["source_round"], "docs/round/round_230.md")
        self.assertEqual(audit["large_sector"], ROUND230_LARGE_SECTOR)
        self.assertFalse(audit["summary"]["production_scoring_changed"])
        self.assertFalse(audit["summary"]["candidate_generation_input"])
        self.assertTrue(audit["summary"]["shadow_weight_only"])
        self.assertEqual(audit["summary"]["r13_default_stage3_bias"], "redteam_first_after_price_validation")
        self.assertEqual(len(audit["shadow_weights"]), 8)
        self.assertEqual(len(audit["deep_sub_archetypes"]), 8)
        self.assertIn("do_not_use_round230_cases_as_candidate_generation_input", audit["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])
        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round230_r13_loop9_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)

            records = load_case_library(paths["cases"])
            rows = round230_case_rows()
            self.assertEqual(len(records), len(ROUND230_CASE_CANDIDATES))
            self.assertEqual(len(rows), len(ROUND230_CASE_CANDIDATES))
            self.assertIn("SK하이닉스", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("price_path_alignment", paths["score_adjustments"].read_text(encoding="utf-8"))
            self.assertIn("STRUCTURAL_SUCCESS_BUT_4B_WATCH", paths["shadow_weights"].read_text(encoding="utf-8"))
            self.assertIn("SK Telecom", paths["deep_sub_archetypes"].read_text(encoding="utf-8"))
            self.assertEqual(json.loads(rows[0]["extra_price_metrics"])["market_cap_2026_usd_bn"], 942.0)


if __name__ == "__main__":
    unittest.main()
