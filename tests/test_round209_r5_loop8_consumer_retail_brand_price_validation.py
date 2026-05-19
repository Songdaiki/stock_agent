from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from e2r.cli.build_round209_r5_loop8_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector
from e2r.sector.round209_r5_loop8_consumer_retail_brand_price_validation import (
    ROUND209_CASE_CANDIDATES,
    ROUND209_GREEN_FORBIDDEN_PATTERNS,
    ROUND209_GREEN_REQUIRED_FIELDS,
    ROUND209_HARD_4C_GATES,
    ROUND209_PRICE_VALIDATION_FIELDS,
    ROUND209_REQUIRED_TARGET_ALIASES,
    ROUND209_SCORE_ADJUSTMENTS,
    ROUND209_STAGE4B_WATCH_TRIGGERS,
    render_round209_green_gate_review_markdown,
    render_round209_stage4b_4c_review_markdown,
    round209_audit_payload,
    round209_case_records,
    round209_case_rows,
    round209_summary,
    write_round209_r5_loop8_reports,
)


class Round209R5Loop8ConsumerRetailBrandPriceValidationTests(unittest.TestCase):
    def test_round209_targets_are_existing_canonical_archetypes(self) -> None:
        canonical_values = {item.value for item in E2RArchetype}

        self.assertGreaterEqual(len(ROUND209_REQUIRED_TARGET_ALIASES), 15)
        self.assertTrue(set(ROUND209_REQUIRED_TARGET_ALIASES.values()).issubset(canonical_values))
        self.assertEqual(
            ROUND209_REQUIRED_TARGET_ALIASES["K_FOOD_GLOBAL_STAPLE_BRAND"],
            E2RArchetype.K_FOOD_GLOBAL_STAPLE_BRAND.value,
        )
        self.assertEqual(
            ROUND209_REQUIRED_TARGET_ALIASES["PRICE_ONLY_RALLY"],
            E2RArchetype.PRICE_ONLY_RALLY.value,
        )

    def test_case_records_validate_and_are_calibration_only(self) -> None:
        records = round209_case_records()
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, Round10LargeSector.CONSUMER_RETAIL_BRAND.value)
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertIn("full_ohlc_complete_false", record.green_guardrails)

        summary = round209_summary()
        self.assertEqual(summary["case_candidate_count"], 7)
        self.assertEqual(summary["structural_success_count"], 2)
        self.assertEqual(summary["success_candidate_count"], 2)
        self.assertEqual(summary["overheat_count"], 1)
        self.assertEqual(summary["failed_rerating_count"], 1)
        self.assertEqual(summary["event_premium_count"], 1)
        self.assertEqual(summary["stage3_case_count"], 2)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["full_ohlc_complete"])

    def test_samyang_is_export_asp_op_revision_candidate_with_reported_anchor(self) -> None:
        by_id = {case.case_id: case for case in ROUND209_CASE_CANDIDATES}
        samyang = by_id["r5_loop8_samyang_buldak_export_aligned"]

        self.assertEqual(samyang.primary_archetype, E2RArchetype.EXPORT_RECURRING_CONSUMER)
        self.assertEqual(samyang.case_type, "structural_success")
        self.assertEqual(samyang.stage3_date.isoformat(), "2024-06-14")
        self.assertEqual(samyang.stage3_price_anchor, 647000.0)
        self.assertEqual(samyang.mfe_1d, 5.7)
        self.assertEqual(samyang.extra_price_metrics["target_upside_pct"], 28.3)
        self.assertIn("single_sku_dependence", samyang.red_flag_fields)

    def test_nongshim_and_odm_are_stage2_watch_until_opm_and_sellthrough(self) -> None:
        by_id = {case.case_id: case for case in ROUND209_CASE_CANDIDATES}
        nongshim = by_id["r5_loop8_nongshim_shin_global_staple"]
        odm = by_id["r5_loop8_cosmax_kolmar_odm_leverage"]

        self.assertEqual(nongshim.primary_archetype, E2RArchetype.K_FOOD_GLOBAL_STAPLE_BRAND)
        self.assertEqual(nongshim.stage2_date.isoformat(), "2024-05-27")
        self.assertIsNone(nongshim.stage3_date)
        self.assertEqual(nongshim.extra_price_metrics["implied_us_target_growth_pct"], 178.8)
        self.assertIn("opm_eps_revision_unverified", nongshim.red_flag_fields)

        self.assertEqual(odm.primary_archetype, E2RArchetype.K_BEAUTY_OEM_ODM_SUPPLYCHAIN_KOREA)
        self.assertEqual(odm.stage2_date.isoformat(), "2025-06-05")
        self.assertIsNone(odm.stage3_date)
        self.assertIn("inventory_receivables_quality_unverified", odm.red_flag_fields)

    def test_apr_is_structural_success_with_4b_watch(self) -> None:
        by_id = {case.case_id: case for case in ROUND209_CASE_CANDIDATES}
        apr = by_id["r5_loop8_apr_medicube_device_4b"]

        self.assertEqual(apr.primary_archetype, E2RArchetype.BEAUTY_DEVICE_EXPORT)
        self.assertEqual(apr.stage2_price_anchor, 158300.0)
        self.assertEqual(apr.stage3_date.isoformat(), "2025-10-20")
        self.assertEqual(apr.stage4b_date.isoformat(), "2025-10-20")
        self.assertEqual(apr.stage4b_status, "watch")
        self.assertEqual(apr.extra_price_metrics["market_cap_mfe_july_to_oct_pct"], 42.9)
        self.assertEqual(apr.extra_price_metrics["reported_mfe_since_january_pct"], 300.0)

    def test_dalba_amore_and_fnf_are_not_green_evidence(self) -> None:
        rows = {row["case_id"]: row for row in round209_case_rows()}
        dalba = rows["r5_loop8_dalba_global_ipo_overheat"]
        amore = rows["r5_loop8_amorepacific_transition_watch"]
        fnf = rows["r5_loop8_fnf_taylormade_event"]

        self.assertEqual(dalba["score_price_alignment"], "price_moved_without_evidence")
        self.assertEqual(dalba["rerating_result"], "theme_overheat")
        self.assertEqual(dalba["stage4b_date"], "2025-06-05")
        self.assertIn("retail_talks_without_sellthrough", dalba["red_flag_fields"])

        self.assertEqual(amore["rerating_result"], "no_rerating")
        self.assertIn("china_exports_decline", amore["red_flag_fields"])

        self.assertEqual(fnf["rerating_result"], "event_premium")
        self.assertEqual(fnf["stage1_date"], "2025-07-21")
        self.assertIn("mna_optionality_without_eps", fnf["red_flag_fields"])

    def test_green_gate_and_4c_rules_are_explicit(self) -> None:
        required = set(ROUND209_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND209_GREEN_FORBIDDEN_PATTERNS)
        review = render_round209_green_gate_review_markdown()
        stage_review = render_round209_stage4b_4c_review_markdown()

        self.assertIn("repeat_purchase_evidence", required)
        self.assertIn("channel_sell_through_confirmed", required)
        self.assertIn("inventory_and_receivables_stable", required)
        self.assertIn("viral_product_only", forbidden)
        self.assertIn("ipo_first_month_rally", forbidden)
        self.assertIn("mna_optionality_without_eps", forbidden)
        self.assertIn("food_safety_recall", ROUND209_HARD_4C_GATES)
        self.assertIn("ipo_first_month_double", ROUND209_STAGE4B_WATCH_TRIGGERS)
        self.assertIn("Do not apply these weights to production scoring yet.", review)
        self.assertIn("r5_loop8_fnf_taylormade_event", stage_review)

    def test_price_validation_fields_and_score_adjustments_cover_r5_axes(self) -> None:
        fields = set(ROUND209_PRICE_VALIDATION_FIELDS)
        axes = {item.axis for item in ROUND209_SCORE_ADJUSTMENTS}

        self.assertIn("target_upside_pct", fields)
        self.assertIn("reported_mfe_since_debut_pct", fields)
        self.assertIn("market_cap_mfe_july_to_oct_pct", fields)
        self.assertIn("implied_target_growth_pct", fields)
        self.assertIn("repeat_demand", axes)
        self.assertIn("channel_sell_through", axes)
        self.assertIn("ipo_first_month_rally", axes)
        self.assertIn("mna_optionality_without_eps", axes)

    def test_summary_and_audit_payload_keep_non_production_guardrails(self) -> None:
        audit = round209_audit_payload()

        self.assertEqual(audit["source_round"], "docs/round/round_209.md")
        self.assertEqual(audit["large_sector"], Round10LargeSector.CONSUMER_RETAIL_BRAND.value)
        self.assertFalse(audit["summary"]["production_scoring_changed"])
        self.assertFalse(audit["summary"]["candidate_generation_input"])
        self.assertTrue(audit["summary"]["shadow_weight_only"])
        self.assertIn("do_not_use_round209_cases_as_candidate_generation_input", audit["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])
        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round209_r5_loop8_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)

            records = load_case_library(paths["cases"])
            rows = round209_case_rows()
            self.assertEqual(len(records), len(ROUND209_CASE_CANDIDATES))
            self.assertEqual(len(rows), len(ROUND209_CASE_CANDIDATES))
            self.assertIn("삼양식품", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("channel_sell_through", paths["score_adjustments"].read_text(encoding="utf-8"))
            self.assertIn("ipo_first_month_double", paths["stage4b_4c_review"].read_text(encoding="utf-8"))
            self.assertEqual(json.loads(rows[0]["extra_price_metrics"])["target_price"], 830000.0)


if __name__ == "__main__":
    unittest.main()
