from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from e2r.cli.build_round211_r7_loop8_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector
from e2r.sector.round211_r7_loop8_biotech_healthcare_device_price_validation import (
    ROUND211_CASE_CANDIDATES,
    ROUND211_GREEN_FORBIDDEN_PATTERNS,
    ROUND211_GREEN_REQUIRED_FIELDS,
    ROUND211_HARD_4C_GATES,
    ROUND211_PRICE_VALIDATION_FIELDS,
    ROUND211_REQUIRED_TARGET_ALIASES,
    ROUND211_SCORE_ADJUSTMENTS,
    ROUND211_STAGE4B_WATCH_TRIGGERS,
    render_round211_green_gate_review_markdown,
    render_round211_stage4b_4c_review_markdown,
    round211_audit_payload,
    round211_case_records,
    round211_case_rows,
    round211_summary,
    write_round211_r7_loop8_reports,
)


class Round211R7Loop8BiotechHealthcareDevicePriceValidationTests(unittest.TestCase):
    def test_round211_targets_are_existing_canonical_archetypes(self) -> None:
        canonical_values = {item.value for item in E2RArchetype}

        self.assertGreaterEqual(len(ROUND211_REQUIRED_TARGET_ALIASES), 16)
        self.assertTrue(set(ROUND211_REQUIRED_TARGET_ALIASES.values()).issubset(canonical_values))
        self.assertEqual(
            ROUND211_REQUIRED_TARGET_ALIASES["SC_FORMULATION_ROYALTY_PLATFORM"],
            E2RArchetype.SC_FORMULATION_ROYALTY_PLATFORM.value,
        )
        self.assertEqual(
            ROUND211_REQUIRED_TARGET_ALIASES["VACCINE_CMO_RESTRUCTURING"],
            E2RArchetype.VACCINE_CMO_RESTRUCTURING.value,
        )

    def test_case_records_validate_and_are_calibration_only(self) -> None:
        records = round211_case_records()
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE.value)
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertIn("full_ohlc_complete_false", record.green_guardrails)

        summary = round211_summary()
        self.assertEqual(summary["case_candidate_count"], 7)
        self.assertEqual(summary["success_candidate_count"], 5)
        self.assertEqual(summary["event_premium_count"], 1)
        self.assertEqual(summary["failed_rerating_count"], 1)
        self.assertEqual(summary["stage3_case_count"], 0)
        self.assertEqual(summary["hard_4c_case_count"], 0)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["full_ohlc_complete"])

    def test_alteogen_is_commercialization_watch_not_confirmed_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND211_CASE_CANDIDATES}
        alteogen = by_id["r7_loop8_alteogen_keytruda_qlex_royalty_watch"]

        self.assertEqual(alteogen.primary_archetype, E2RArchetype.SC_FORMULATION_ROYALTY_PLATFORM)
        self.assertEqual(alteogen.stage1_date.isoformat(), "2025-03-27")
        self.assertEqual(alteogen.stage2_date.isoformat(), "2025-09-19")
        self.assertIsNone(alteogen.stage3_date)
        self.assertEqual(alteogen.stage4c_date.isoformat(), "2025-03-05")
        self.assertEqual(alteogen.extra_price_metrics["keytruda_qlex_2025_sales_usd_mn"], 40.0)
        self.assertEqual(alteogen.extra_price_metrics["potential_qlex_sales_vs_keytruda_2024_pct"], 20.0)
        self.assertIn("royalty_recognition_unverified", alteogen.red_flag_fields)

    def test_yuhan_hugel_and_lunit_stay_stage2_until_real_commercialization(self) -> None:
        by_id = {case.case_id: case for case in ROUND211_CASE_CANDIDATES}
        yuhan = by_id["r7_loop8_yuhan_lazcluze_approval_royalty_watch"]
        hugel = by_id["r7_loop8_hugel_letybo_us_launch"]
        lunit = by_id["r7_loop8_lunit_medical_ai_validation_not_green"]

        self.assertEqual(yuhan.stage2_date.isoformat(), "2024-08-20")
        self.assertIsNone(yuhan.stage3_date)
        self.assertEqual(yuhan.extra_price_metrics["risk_reduction_vs_osimertinib_pct"], 30.0)
        self.assertIn("approval_only_not_green", yuhan.red_flag_fields)

        self.assertEqual(hugel.primary_archetype, E2RArchetype.BOTULINUM_US_MARKET_ENTRY)
        self.assertEqual(hugel.extra_price_metrics["potential_discount_high_pct"], 33.3)
        self.assertIn("us_sales_unverified", hugel.red_flag_fields)

        self.assertEqual(lunit.case_type, "failed_rerating")
        self.assertEqual(lunit.extra_price_metrics["exam_count"], 163449.0)
        self.assertEqual(lunit.extra_price_metrics["overall_auc"], 0.91)
        self.assertIn("subgroup_performance_risk", lunit.red_flag_fields)

    def test_cdmo_cmo_events_are_stage2_or_saturation_watch(self) -> None:
        by_id = {case.case_id: case for case in ROUND211_CASE_CANDIDATES}
        sk_bio = by_id["r7_loop8_sk_bioscience_idt_cmo_event"]
        celltrion = by_id["r7_loop8_celltrion_us_factory_tariff_hedge"]
        samsung_bio = by_id["r7_loop8_samsung_biologics_gsk_facility_saturation"]

        self.assertEqual(sk_bio.case_type, "event_premium")
        self.assertEqual(sk_bio.stage4b_date.isoformat(), "2024-06-27")
        self.assertEqual(sk_bio.stage2_price_anchor, 52200.0)
        self.assertEqual(sk_bio.mfe_1d, 11.7)
        self.assertIn("mna_without_utilization", sk_bio.red_flag_fields)

        self.assertEqual(celltrion.primary_archetype, E2RArchetype.BIOSIMILAR_TARIFF_HEDGE_MANUFACTURING)
        self.assertEqual(celltrion.extra_price_metrics["imclone_acquisition_usd_mn"], 330.0)
        self.assertIn("utilization_unverified", celltrion.red_flag_fields)

        self.assertEqual(samsung_bio.primary_archetype, E2RArchetype.CDMO_US_TARIFF_HEDGE_CAPACITY)
        self.assertEqual(samsung_bio.mae_1d, -0.4)
        self.assertEqual(samsung_bio.extra_price_metrics["relative_underperformance_pp"], -2.4)
        self.assertEqual(samsung_bio.score_price_alignment, "evidence_good_but_price_failed")

    def test_green_gate_and_4c_rules_are_explicit(self) -> None:
        required = set(ROUND211_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND211_GREEN_FORBIDDEN_PATTERNS)
        review = render_round211_green_gate_review_markdown()
        stage_review = render_round211_stage4b_4c_review_markdown()

        self.assertIn("prescription_volume_or_hospital_adoption", required)
        self.assertIn("reimbursement_or_payer_access", required)
        self.assertIn("revenue_recognition", required)
        self.assertIn("approval_news_only", forbidden)
        self.assertIn("paper_validation_without_revenue", forbidden)
        self.assertIn("mna_without_utilization", forbidden)
        self.assertIn("patent_ip_legal_loss", ROUND211_HARD_4C_GATES)
        self.assertIn("mna_announcement_day_spike", ROUND211_STAGE4B_WATCH_TRIGGERS)
        self.assertIn("Do not apply these weights to production scoring yet.", review)
        self.assertIn("r7_loop8_lunit_medical_ai_validation_not_green", stage_review)

    def test_price_validation_fields_and_score_adjustments_cover_r7_axes(self) -> None:
        fields = set(ROUND211_PRICE_VALIDATION_FIELDS)
        axes = {item.axis for item in ROUND211_SCORE_ADJUSTMENTS}

        self.assertIn("commercial_sales_anchor", fields)
        self.assertIn("trial_size", fields)
        self.assertIn("capacity_or_transaction_value", fields)
        self.assertIn("commercial_revenue", axes)
        self.assertIn("royalty_recognition", axes)
        self.assertIn("approval_news_only", axes)
        self.assertIn("paper_validation_without_revenue", axes)

    def test_summary_and_audit_payload_keep_non_production_guardrails(self) -> None:
        audit = round211_audit_payload()

        self.assertEqual(audit["source_round"], "docs/round/round_211.md")
        self.assertEqual(audit["large_sector"], Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE.value)
        self.assertFalse(audit["summary"]["production_scoring_changed"])
        self.assertFalse(audit["summary"]["candidate_generation_input"])
        self.assertTrue(audit["summary"]["shadow_weight_only"])
        self.assertIn("do_not_use_round211_cases_as_candidate_generation_input", audit["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])
        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round211_r7_loop8_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)

            records = load_case_library(paths["cases"])
            rows = round211_case_rows()
            self.assertEqual(len(records), len(ROUND211_CASE_CANDIDATES))
            self.assertEqual(len(rows), len(ROUND211_CASE_CANDIDATES))
            self.assertIn("알테오젠", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("approval_news_only", paths["score_adjustments"].read_text(encoding="utf-8"))
            self.assertIn("patent_ip_legal_loss", paths["stage4b_4c_review"].read_text(encoding="utf-8"))
            self.assertEqual(json.loads(rows[0]["extra_price_metrics"])["keytruda_qlex_2025_sales_usd_mn"], 40.0)


if __name__ == "__main__":
    unittest.main()
