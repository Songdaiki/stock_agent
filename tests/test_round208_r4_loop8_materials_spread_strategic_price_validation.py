from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from e2r.cli.build_round208_r4_loop8_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector
from e2r.sector.round208_r4_loop8_materials_spread_strategic_price_validation import (
    ROUND208_CASE_CANDIDATES,
    ROUND208_GREEN_FORBIDDEN_PATTERNS,
    ROUND208_GREEN_REQUIRED_FIELDS,
    ROUND208_HARD_4C_GATES,
    ROUND208_PRICE_VALIDATION_FIELDS,
    ROUND208_REQUIRED_TARGET_ALIASES,
    ROUND208_SCORE_ADJUSTMENTS,
    ROUND208_STAGE4B_WATCH_TRIGGERS,
    render_round208_green_gate_review_markdown,
    render_round208_stage4b_4c_review_markdown,
    round208_audit_payload,
    round208_case_records,
    round208_case_rows,
    round208_summary,
    write_round208_r4_loop8_reports,
)


class Round208R4Loop8MaterialsSpreadStrategicPriceValidationTests(unittest.TestCase):
    def test_round208_targets_are_existing_canonical_archetypes(self) -> None:
        canonical_values = {item.value for item in E2RArchetype}

        self.assertGreaterEqual(len(ROUND208_REQUIRED_TARGET_ALIASES), 13)
        self.assertTrue(set(ROUND208_REQUIRED_TARGET_ALIASES.values()).issubset(canonical_values))
        self.assertEqual(
            ROUND208_REQUIRED_TARGET_ALIASES["NONFERROUS_STRATEGIC_METALS"],
            E2RArchetype.NONFERROUS_STRATEGIC_METALS.value,
        )
        self.assertEqual(
            ROUND208_REQUIRED_TARGET_ALIASES["POLYSILICON_NON_CHINA_SUPPLY_OPTION"],
            E2RArchetype.POLYSILICON_NON_CHINA_SUPPLY_OPTION.value,
        )

    def test_case_records_validate_and_are_calibration_only(self) -> None:
        records = round208_case_records()
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, Round10LargeSector.MATERIALS_SPREAD_STRATEGIC.value)
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertIn("full_ohlc_complete_false", record.green_guardrails)

        summary = round208_summary()
        self.assertEqual(summary["case_candidate_count"], 7)
        self.assertEqual(summary["success_candidate_count"], 2)
        self.assertEqual(summary["cyclical_success_count"], 1)
        self.assertEqual(summary["event_premium_count"], 2)
        self.assertEqual(summary["failed_or_4c_count"], 2)
        self.assertEqual(summary["hard_4c_case_count"], 2)
        self.assertEqual(summary["stage3_case_count"], 0)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["full_ohlc_complete"])

    def test_korea_zinc_splits_governance_premium_from_strategic_material_watch(self) -> None:
        by_id = {case.case_id: case for case in ROUND208_CASE_CANDIDATES}
        korea_zinc = by_id["r4_loop8_korea_zinc_event_strategic_watch"]

        self.assertEqual(korea_zinc.primary_archetype, E2RArchetype.NONFERROUS_STRATEGIC_METALS)
        self.assertEqual(korea_zinc.case_type, "event_premium")
        self.assertIsNone(korea_zinc.stage3_date)
        self.assertEqual(korea_zinc.stage4b_date.isoformat(), "2024-10-21")
        self.assertEqual(korea_zinc.stage4c_date.isoformat(), "2024-10-30")
        self.assertEqual(korea_zinc.mfe_1d, 24.1)
        self.assertEqual(korea_zinc.mae_1d, -29.9)
        self.assertEqual(korea_zinc.stage4b_price_anchor, 877000.0)
        self.assertEqual(korea_zinc.extra_price_metrics["mfe_from_base_to_record_close"], 57.7)
        self.assertEqual(korea_zinc.extra_price_metrics["issue_price_discount_pct"], -56.6)
        self.assertIn("tender_offer_premium", korea_zinc.red_flag_fields)

    def test_petrochemical_break_cases_are_not_restructuring_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND208_CASE_CANDIDATES}
        lotte = by_id["r4_loop8_lotte_chemical_petrochem_break"]
        lg_chem = by_id["r4_loop8_lg_chem_petrochem_failed_rerating"]

        self.assertEqual(lotte.primary_archetype, E2RArchetype.PETROCHEMICAL_RESTRUCTURING_KOREA)
        self.assertEqual(lotte.case_type, "4c_thesis_break")
        self.assertTrue(lotte.hard_4c_confirmed)
        self.assertEqual(lotte.stage2_date.isoformat(), "2025-11-26")
        self.assertEqual(lotte.extra_price_metrics["operating_loss_worsening_pct"], 157.0)
        self.assertIn("china_middle_east_oversupply", lotte.red_flag_fields)

        self.assertEqual(lg_chem.primary_archetype, E2RArchetype.CHEMICAL_SPREAD)
        self.assertEqual(lg_chem.case_type, "failed_rerating")
        self.assertTrue(lg_chem.hard_4c_confirmed)
        self.assertEqual(lg_chem.extra_price_metrics["operating_profit_decline_pct"], -63.75)
        self.assertEqual(lg_chem.mae_1d, -2.9)

    def test_sk_innovation_refining_is_cyclical_success_not_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND208_CASE_CANDIDATES}
        sk = by_id["r4_loop8_sk_innovation_refining_cycle"]

        self.assertEqual(sk.primary_archetype, E2RArchetype.REFINING_OIL_SPREAD)
        self.assertEqual(sk.case_type, "cyclical_success")
        self.assertEqual(sk.rerating_result, "cyclical_rerating")
        self.assertEqual(sk.stage2_date.isoformat(), "2026-05-13")
        self.assertIsNone(sk.stage3_date)
        self.assertEqual(sk.mae_1d, -2.5)
        self.assertEqual(sk.extra_price_metrics["beat_vs_lseg_estimate_pct"], 57.1)

    def test_posco_oci_and_poongsan_require_offtake_or_confirmed_transaction(self) -> None:
        by_id = {case.case_id: case for case in ROUND208_CASE_CANDIDATES}
        posco = by_id["r4_loop8_posco_lithium_resource_security"]
        oci = by_id["r4_loop8_oci_non_china_polysilicon_event"]
        poongsan = by_id["r4_loop8_poongsan_copper_defense_event"]

        self.assertEqual(posco.primary_archetype, E2RArchetype.LITHIUM_BATTERY_RAW_MATERIAL)
        self.assertEqual(posco.case_type, "success_candidate")
        self.assertEqual(posco.mfe_1d, 10.8)
        self.assertEqual(posco.extra_price_metrics["spodumene_peak_to_low_drawdown_pct"], -89.8)
        self.assertEqual(posco.score_price_alignment, "evidence_good_but_price_failed")

        self.assertEqual(oci.primary_archetype, E2RArchetype.POLYSILICON_NON_CHINA_SUPPLY_OPTION)
        self.assertEqual(oci.stage4b_date.isoformat(), "2026-04-14")
        self.assertIn("spacex_contract_unconfirmed_media_report", oci.red_flag_fields)
        self.assertEqual(oci.extra_price_metrics["target_capacity_gw"], 10.0)

        self.assertEqual(poongsan.primary_archetype, E2RArchetype.COPPER_PROCESSING_PLUS_DEFENSE)
        self.assertEqual(poongsan.case_type, "event_premium")
        self.assertIn("transaction_not_decided", poongsan.red_flag_fields)
        self.assertEqual(poongsan.extra_price_metrics["reported_deal_value_krw_trn"], 1.5)

    def test_green_gate_and_4c_rules_are_explicit(self) -> None:
        required = set(ROUND208_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND208_GREEN_FORBIDDEN_PATTERNS)
        review = render_round208_green_gate_review_markdown()
        stage_review = render_round208_stage4b_4c_review_markdown()

        self.assertIn("actual_product_spread", required)
        self.assertIn("fcf_after_working_capital", required)
        self.assertIn("price_floor_or_offtake", required)
        self.assertIn("tender_offer_premium", forbidden)
        self.assertIn("unconfirmed_media_report", forbidden)
        self.assertIn("large_share_issue_or_dilution", ROUND208_HARD_4C_GATES)
        self.assertIn("tender_offer_buyback_governance_battle_rally", ROUND208_STAGE4B_WATCH_TRIGGERS)
        self.assertIn("Do not apply these weights to production scoring yet.", review)
        self.assertIn("Governance/tender/buyback", stage_review)

    def test_price_validation_fields_include_spread_event_and_commodity_metrics(self) -> None:
        fields = set(ROUND208_PRICE_VALIDATION_FIELDS)

        self.assertIn("mfe_from_base_to_record_close", fields)
        self.assertIn("issue_price_discount_pct", fields)
        self.assertIn("operating_loss_worsening_pct", fields)
        self.assertIn("commodity_drawdown_pct", fields)
        self.assertIn("full_ohlc_available", fields)

    def test_score_adjustments_keep_event_premium_and_spread_disciplined(self) -> None:
        axes = {item.axis for item in ROUND208_SCORE_ADJUSTMENTS}

        self.assertIn("actual_product_spread", axes)
        self.assertIn("fcf_after_working_capital", axes)
        self.assertIn("tender_offer_or_governance_premium", axes)
        self.assertIn("unconfirmed_media_report", axes)
        self.assertIn("capex_heavy_project_pre_revenue", axes)

    def test_summary_and_audit_payload_keep_non_production_guardrails(self) -> None:
        audit = round208_audit_payload()

        self.assertEqual(audit["source_round"], "docs/round/round_208.md")
        self.assertEqual(audit["large_sector"], Round10LargeSector.MATERIALS_SPREAD_STRATEGIC.value)
        self.assertFalse(audit["summary"]["production_scoring_changed"])
        self.assertFalse(audit["summary"]["candidate_generation_input"])
        self.assertTrue(audit["summary"]["shadow_weight_only"])
        self.assertIn("do_not_use_round208_cases_as_candidate_generation_input", audit["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])
        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round208_r4_loop8_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)

            records = load_case_library(paths["cases"])
            rows = round208_case_rows()
            self.assertEqual(len(records), len(ROUND208_CASE_CANDIDATES))
            self.assertEqual(len(rows), len(ROUND208_CASE_CANDIDATES))
            self.assertIn("actual_product_spread", paths["score_adjustments"].read_text(encoding="utf-8"))
            self.assertIn("고려아연", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("issue_price_discount_pct", paths["price_validation_fields"].read_text(encoding="utf-8"))
            self.assertEqual(json.loads(rows[0]["extra_price_metrics"])["event_base_price"], 556000.0)


if __name__ == "__main__":
    unittest.main()
