from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from e2r.cli.build_round231_r1_loop10_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round231_r1_loop10_industrial_orders_infra_price_validation import (
    ROUND231_CASE_CANDIDATES,
    ROUND231_GREEN_FORBIDDEN_PATTERNS,
    ROUND231_GREEN_REQUIRED_FIELDS,
    ROUND231_HARD_4C_GATES,
    ROUND231_LARGE_SECTOR,
    ROUND231_PRICE_VALIDATION_FIELDS,
    ROUND231_REQUIRED_TARGET_ALIASES,
    ROUND231_SCORE_ADJUSTMENTS,
    ROUND231_SHADOW_WEIGHT_ROWS,
    ROUND231_STAGE4B_WATCH_TRIGGERS,
    render_round231_green_gate_review_markdown,
    render_round231_stage4b_4c_review_markdown,
    round231_audit_payload,
    round231_case_records,
    round231_case_rows,
    round231_deep_sub_archetype_rows,
    round231_shadow_weight_rows,
    round231_summary,
    write_round231_r1_loop10_reports,
)


class Round231R1Loop10IndustrialOrdersInfraPriceValidationTests(unittest.TestCase):
    def test_round231_targets_map_to_existing_canonical_archetypes(self) -> None:
        canonical_values = {item.value for item in E2RArchetype}

        self.assertEqual(len(ROUND231_REQUIRED_TARGET_ALIASES), 12)
        self.assertTrue(set(ROUND231_REQUIRED_TARGET_ALIASES.values()).issubset(canonical_values))
        self.assertEqual(
            ROUND231_REQUIRED_TARGET_ALIASES["DEFENSE_EXPORT_ORDER_TO_REVENUE"],
            E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG.value,
        )
        self.assertEqual(
            ROUND231_REQUIRED_TARGET_ALIASES["MISSILE_DEFENSE_EXPORT_PLATFORM"],
            E2RArchetype.DEFENSE_INTERCEPTOR_COMBAT_VALIDATION.value,
        )
        self.assertEqual(
            ROUND231_REQUIRED_TARGET_ALIASES["SAUDI_GAS_INFRA_BACKLOG"],
            E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG_KOREA.value,
        )

    def test_case_records_validate_and_are_calibration_only(self) -> None:
        records = round231_case_records()
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, ROUND231_LARGE_SECTOR)
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertIn("shadow_weight_only_true", record.green_guardrails)
            self.assertIn("full_ohlc_complete_false", record.green_guardrails)

        summary = round231_summary()
        self.assertEqual(summary["case_candidate_count"], 8)
        self.assertEqual(summary["structural_success_count"], 1)
        self.assertEqual(summary["success_candidate_count"], 6)
        self.assertEqual(summary["hard_4c_case_count"], 0)
        self.assertEqual(summary["stage3_case_count"], 1)
        self.assertEqual(summary["target_archetype_count"], 12)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["full_ohlc_complete"])

    def test_power_equipment_case_keeps_price_failure_out_of_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND231_CASE_CANDIDATES}
        ls = by_id["r1_loop10_ls_electric_grid_transformer_price_failed"]

        self.assertEqual(ls.primary_archetype, E2RArchetype.GRID_POWER_EQUIPMENT_AI_DATACENTER)
        self.assertEqual(ls.stage2_date.isoformat(), "2024-07-01")
        self.assertIsNone(ls.stage3_date)
        self.assertEqual(ls.stage2_price_anchor, 208500.0)
        self.assertEqual(ls.mae_1d, -5.4)
        self.assertEqual(ls.extra_price_metrics["us_utility_transformer_contract_usd_mn"], 312.0)
        self.assertEqual(ls.score_price_alignment, "evidence_good_but_price_failed")
        self.assertEqual(ls.round_stage_failure_label, "stage2_watch_not_green")

    def test_hyundai_rotem_is_order_to_revenue_success_anchor(self) -> None:
        by_id = {case.case_id: case for case in ROUND231_CASE_CANDIDATES}
        rotem = by_id["r1_loop10_hyundai_rotem_k2_export_aligned"]

        self.assertEqual(rotem.primary_archetype, E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG)
        self.assertEqual(rotem.stage3_date.isoformat(), "2024-04-09")
        self.assertEqual(rotem.stage3_price_anchor, 41300.0)
        self.assertEqual(rotem.mfe_1d, 9.3)
        self.assertEqual(rotem.extra_price_metrics["relative_outperformance_vs_kospi_pp"], 9.6)
        self.assertEqual(rotem.extra_price_metrics["poland_second_contract_usd_bn"], 6.5)
        self.assertEqual(rotem.rerating_result, "true_rerating")
        self.assertEqual(rotem.stage_failure_type, "green_success")

    def test_defense_epc_shipbuilding_watch_cases_are_not_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND231_CASE_CANDIDATES}
        lig = by_id["r1_loop10_lig_nex1_cheongung_export_crowding"]
        aero = by_id["r1_loop10_hanwha_aerospace_poland_missile_jv_dilution_watch"]
        epc = by_id["r1_loop10_samsung_ea_gs_fadhili_epc"]
        ship = by_id["r1_loop10_hd_hyundai_heavy_mipo_masga_event"]

        self.assertIsNone(lig.stage3_date)
        self.assertEqual(lig.stage4b_date.isoformat(), "2024-07-02")
        self.assertEqual(lig.extra_price_metrics["first_half_2024_stock_gain_pct"], 69.0)
        self.assertIn("downgrade_after_crowding", lig.red_flag_fields)

        self.assertEqual(aero.mae_1d, -13.0)
        self.assertIn("dilution_after_rerating", aero.red_flag_fields)
        self.assertEqual(aero.round_stage_failure_label, "4B_watch_not_hard_4C")

        self.assertEqual(epc.stage2_price_anchor, 26750.0)
        self.assertEqual(epc.extra_price_metrics["samsung_share_of_total_project_pct"], 77.9)
        self.assertIn("cash_collection_unknown", epc.red_flag_fields)

        self.assertEqual(ship.score_price_alignment, "price_moved_without_evidence")
        self.assertEqual(ship.rerating_result, "event_premium")
        self.assertTrue(ship.extra_price_metrics["record_high_status"])

    def test_hanwha_ocean_sanction_is_watch_not_hard_4c(self) -> None:
        by_id = {case.case_id: case for case in ROUND231_CASE_CANDIDATES}
        ocean = by_id["r1_loop10_hanwha_ocean_china_sanction_watch"]

        self.assertEqual(ocean.primary_archetype, E2RArchetype.GEOPOLITICAL_SHIPBUILDING_SANCTION)
        self.assertEqual(ocean.stage4c_date.isoformat(), "2025-10-14")
        self.assertFalse(ocean.hard_4c_confirmed)
        self.assertEqual(ocean.mae_1d, -5.8)
        self.assertEqual(ocean.rerating_result, "thesis_break")
        self.assertEqual(ocean.round_stage_failure_label, "4C_watch_not_hard_4C")

    def test_green_gate_and_stage4_rules_are_explicit(self) -> None:
        required = set(ROUND231_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND231_GREEN_FORBIDDEN_PATTERNS)
        review = render_round231_green_gate_review_markdown()
        stage_review = render_round231_stage4b_4c_review_markdown()

        self.assertIn("actual_delivery_or_revenue_recognition", required)
        self.assertIn("cashflow_or_working_capital_passed", required)
        self.assertIn("contract_headline_only", forbidden)
        self.assertIn("policy_or_mou_without_funded_order", forbidden)
        self.assertIn("good_news_with_weak_or_negative_price_response", ROUND231_STAGE4B_WATCH_TRIGGERS)
        self.assertIn("geopolitical_sanction_causing_revenue_disruption", ROUND231_HARD_4C_GATES)
        self.assertIn("Do not apply these weights to production scoring yet.", review)
        self.assertIn("order -> delivery -> revenue -> margin -> EPS/FCF", review)
        self.assertIn("Hanwha Ocean is 4C-watch", stage_review)

    def test_price_fields_score_axes_shadow_and_deep_rows_cover_round231(self) -> None:
        fields = set(ROUND231_PRICE_VALIDATION_FIELDS)
        axes = {item.axis for item in ROUND231_SCORE_ADJUSTMENTS}
        shadow_rows = {row["archetype"]: row for row in round231_shadow_weight_rows()}
        deep_rows = round231_deep_sub_archetype_rows()

        self.assertIn("contract_value_anchor", fields)
        self.assertIn("target_price_anchor", fields)
        self.assertIn("confirmed_contract_amount", axes)
        self.assertIn("epc_backlog_without_cashflow", axes)
        self.assertEqual(len(ROUND231_SHADOW_WEIGHT_ROWS), 8)
        self.assertEqual(shadow_rows["GRID_POWER_EQUIPMENT_AI_DATACENTER"]["us_grid_exposure"], "+5")
        self.assertEqual(shadow_rows["SHIPBUILDING_US_POLICY_MASGA"]["event_penalty"], "-5")
        self.assertTrue(any("Hyundai Rotem" in row["terms"] for row in deep_rows))
        self.assertTrue(any("Hanwha Ocean" in row["terms"] for row in deep_rows))

    def test_summary_and_audit_payload_keep_non_production_guardrails(self) -> None:
        audit = round231_audit_payload()

        self.assertEqual(audit["source_round"], "docs/round/round_231.md")
        self.assertEqual(audit["large_sector"], ROUND231_LARGE_SECTOR)
        self.assertFalse(audit["summary"]["production_scoring_changed"])
        self.assertFalse(audit["summary"]["candidate_generation_input"])
        self.assertTrue(audit["summary"]["shadow_weight_only"])
        self.assertEqual(len(audit["shadow_weights"]), 8)
        self.assertEqual(len(audit["deep_sub_archetypes"]), 8)
        self.assertIn("do_not_use_round231_cases_as_candidate_generation_input", audit["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])
        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round231_r1_loop10_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)

            records = load_case_library(paths["cases"])
            rows = round231_case_rows()
            self.assertEqual(len(records), len(ROUND231_CASE_CANDIDATES))
            self.assertEqual(len(rows), len(ROUND231_CASE_CANDIDATES))
            self.assertIn("Hyundai Rotem", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("contract_headline_only", paths["green_gate_review"].read_text(encoding="utf-8"))
            self.assertIn("SHIPBUILDING_US_POLICY_MASGA", paths["shadow_weights"].read_text(encoding="utf-8"))
            self.assertIn("Hanwha Ocean", paths["deep_sub_archetypes"].read_text(encoding="utf-8"))
            self.assertEqual(json.loads(rows[0]["extra_price_metrics"])["target_raise_pct"], 86.7)


if __name__ == "__main__":
    unittest.main()
