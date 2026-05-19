from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from e2r.cli.build_round214_r10_loop8_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector
from e2r.sector.round214_r10_loop8_construction_real_estate_materials_price_validation import (
    ROUND214_CASE_CANDIDATES,
    ROUND214_GREEN_FORBIDDEN_PATTERNS,
    ROUND214_GREEN_REQUIRED_FIELDS,
    ROUND214_HARD_4C_GATES,
    ROUND214_PRICE_VALIDATION_FIELDS,
    ROUND214_REQUIRED_TARGET_ALIASES,
    ROUND214_SCORE_ADJUSTMENTS,
    ROUND214_STAGE4B_WATCH_TRIGGERS,
    render_round214_green_gate_review_markdown,
    render_round214_stage4b_4c_review_markdown,
    round214_audit_payload,
    round214_case_records,
    round214_case_rows,
    round214_summary,
    write_round214_r10_loop8_reports,
)


class Round214R10Loop8ConstructionRealEstateMaterialsPriceValidationTests(unittest.TestCase):
    def test_round214_targets_are_existing_canonical_archetypes(self) -> None:
        canonical_values = {item.value for item in E2RArchetype}

        self.assertGreaterEqual(len(ROUND214_REQUIRED_TARGET_ALIASES), 11)
        self.assertTrue(set(ROUND214_REQUIRED_TARGET_ALIASES.values()).issubset(canonical_values))
        self.assertEqual(
            ROUND214_REQUIRED_TARGET_ALIASES["OVERSEAS_EPC_CONTRACT_BACKLOG_KOREA"],
            E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG_KOREA.value,
        )
        self.assertEqual(
            ROUND214_REQUIRED_TARGET_ALIASES["PF_CREDIT_REDTEAM_OVERLAY"],
            E2RArchetype.PF_CREDIT_REDTEAM_OVERLAY.value,
        )
        self.assertEqual(
            ROUND214_REQUIRED_TARGET_ALIASES["AI_DATA_CENTER_REAL_ASSET_DEVELOPMENT"],
            E2RArchetype.AI_DATA_CENTER_REAL_ASSET_DEVELOPMENT.value,
        )

    def test_case_records_validate_and_are_calibration_only(self) -> None:
        records = round214_case_records()
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, Round10LargeSector.CONSTRUCTION_REAL_ESTATE_MATERIALS.value)
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertIn("full_ohlc_complete_false", record.green_guardrails)

        summary = round214_summary()
        self.assertEqual(summary["case_candidate_count"], 7)
        self.assertEqual(summary["success_candidate_count"], 4)
        self.assertEqual(summary["failed_rerating_count"], 1)
        self.assertEqual(summary["thesis_break_count"], 2)
        self.assertEqual(summary["price_moved_without_evidence_count"], 1)
        self.assertEqual(summary["stage3_case_count"], 0)
        self.assertEqual(summary["hard_4c_case_count"], 2)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["full_ohlc_complete"])

    def test_epc_cases_are_stage2_until_margin_cash_and_cost_control_confirm(self) -> None:
        by_id = {case.case_id: case for case in ROUND214_CASE_CANDIDATES}
        samsung = by_id["r10_loop8_samsung_ea_fadhili_epc"]
        hyundai = by_id["r10_loop8_hyundai_ec_jafurah_gas_infra"]
        daewoo = by_id["r10_loop8_daewoo_ec_grand_faw_handover"]

        self.assertEqual(samsung.primary_archetype, E2RArchetype.OVERSEAS_EPC_CONTRACT_BACKLOG_KOREA)
        self.assertEqual(samsung.stage2_date.isoformat(), "2024-04-03")
        self.assertEqual(samsung.stage4b_date.isoformat(), "2024-04-03")
        self.assertIsNone(samsung.stage3_date)
        self.assertEqual(samsung.stage2_price_anchor, 26750.0)
        self.assertEqual(samsung.mfe_1d, 8.5)
        self.assertEqual(samsung.extra_price_metrics["relative_intraday_outperformance_vs_kospi_pp"], 9.9)
        self.assertEqual(samsung.extra_price_metrics["target_upside_from_event_peak_pct"], 30.8)
        self.assertIn("epc_margin_unverified", samsung.red_flag_fields)

        self.assertEqual(hyundai.extra_price_metrics["aramco_contract_package_usd_bn"], 25.0)
        self.assertEqual(hyundai.extra_price_metrics["jafurah_gas_reserves_tcf"], 229.0)
        self.assertIn("working_capital_burden_watch", hyundai.red_flag_fields)

        self.assertEqual(daewoo.primary_archetype, E2RArchetype.INFRA_RECONSTRUCTION_POLICY)
        self.assertEqual(daewoo.stage2_date.isoformat(), "2024-11-12")
        self.assertEqual(daewoo.extra_price_metrics["completed_docks"], 5.0)
        self.assertEqual(daewoo.extra_price_metrics["iraq_development_road_project_usd_bn"], 17.0)
        self.assertIn("cash_collection_unverified", daewoo.red_flag_fields)

    def test_pf_and_safety_cases_are_redteam_or_4c_not_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND214_CASE_CANDIDATES}
        taeyoung = by_id["r10_loop8_taeyoung_pf_hard_4c"]
        hdc = by_id["r10_loop8_hdc_hyundai_development_quality_safety_4c"]
        safety_watch = by_id["r10_loop8_posco_ec_dl_construction_safety_watch"]

        self.assertEqual(taeyoung.case_type, "4c_thesis_break")
        self.assertTrue(taeyoung.hard_4c_confirmed)
        self.assertEqual(taeyoung.extra_price_metrics["pf_delinquency_relative_increase_pct"], 629.7)
        self.assertEqual(taeyoung.extra_price_metrics["government_support_package_krw_trn"], 40.6)
        self.assertIn("pf_workout_debt_reschedule", taeyoung.red_flag_fields)

        self.assertEqual(hdc.primary_archetype, E2RArchetype.APARTMENT_QUALITY_SAFETY_OVERLAY)
        self.assertTrue(hdc.hard_4c_confirmed)
        self.assertEqual(hdc.stage4c_date.isoformat(), "2022-01-11")
        self.assertEqual(hdc.extra_price_metrics["combined_related_gwangju_fatalities"], 15.0)
        self.assertIn("apartment_collapse_quality_failure", hdc.red_flag_fields)

        self.assertEqual(safety_watch.case_type, "failed_rerating")
        self.assertFalse(safety_watch.hard_4c_confirmed)
        self.assertEqual(safety_watch.extra_price_metrics["posco_ec_sites_halted"], 103.0)
        self.assertEqual(safety_watch.extra_price_metrics["proposed_fine_pct_of_operating_profit"], 5.0)
        self.assertIn("repeated_workplace_fatality", safety_watch.red_flag_fields)

    def test_ai_data_center_real_asset_watch_is_not_green_without_tenant_noi_affo(self) -> None:
        by_id = {case.case_id: case for case in ROUND214_CASE_CANDIDATES}
        ai_dc = by_id["r10_loop8_ai_data_center_real_asset_watch"]

        self.assertEqual(ai_dc.primary_archetype, E2RArchetype.AI_DATA_CENTER_REAL_ASSET_DEVELOPMENT)
        self.assertEqual(ai_dc.stage1_date.isoformat(), "2025-06-20")
        self.assertEqual(ai_dc.stage2_date.isoformat(), "2026-02-11")
        self.assertEqual(ai_dc.stage4b_date.isoformat(), "2025-06-20")
        self.assertIsNone(ai_dc.stage3_date)
        self.assertEqual(ai_dc.score_price_alignment, "price_moved_without_evidence")
        self.assertEqual(ai_dc.extra_price_metrics["sk_aws_investment_krw_trn"], 7.0)
        self.assertEqual(ai_dc.extra_price_metrics["capacity_expansion_potential_multiple"], 10.0)
        self.assertEqual(ai_dc.extra_price_metrics["kakao_event_mfe_pct"], 11.0)
        self.assertIn("tenant_absent", ai_dc.red_flag_fields)
        self.assertIn("noi_affo_unverified", ai_dc.red_flag_fields)

    def test_green_gate_and_4c_rules_are_explicit(self) -> None:
        required = set(ROUND214_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND214_GREEN_FORBIDDEN_PATTERNS)
        review = render_round214_green_gate_review_markdown()
        stage_review = render_round214_stage4b_4c_review_markdown()

        self.assertIn("margin_or_noi_affo_visibility", required)
        self.assertIn("cash_flow_after_working_capital", required)
        self.assertIn("safety_quality_trust_passed", required)
        self.assertIn("contract_headline_only", forbidden)
        self.assertIn("pf_relief_policy_only", forbidden)
        self.assertIn("data_center_theme_without_tenant", forbidden)
        self.assertIn("pf_workout_debt_reschedule", ROUND214_HARD_4C_GATES)
        self.assertIn("apartment_collapse_quality_failure", ROUND214_HARD_4C_GATES)
        self.assertIn("data_center_theme_basket_rally", ROUND214_STAGE4B_WATCH_TRIGGERS)
        self.assertIn("Do not apply these weights to production scoring yet.", review)
        self.assertIn("r10_loop8_hdc_hyundai_development_quality_safety_4c", stage_review)

    def test_price_validation_fields_and_score_adjustments_cover_r10_axes(self) -> None:
        fields = set(ROUND214_PRICE_VALIDATION_FIELDS)
        axes = {item.axis for item in ROUND214_SCORE_ADJUSTMENTS}

        self.assertIn("stage2_event_peak_price", fields)
        self.assertIn("pf_delinquency_or_support_metric", fields)
        self.assertIn("tenant_noi_affo_status", fields)
        self.assertIn("cash_flow_after_working_capital", axes)
        self.assertIn("epc_margin_visibility", axes)
        self.assertIn("tenant_contract_quality", axes)
        self.assertIn("quality_safety_incident", axes)

    def test_summary_and_audit_payload_keep_non_production_guardrails(self) -> None:
        audit = round214_audit_payload()

        self.assertEqual(audit["source_round"], "docs/round/round_214.md")
        self.assertEqual(audit["large_sector"], Round10LargeSector.CONSTRUCTION_REAL_ESTATE_MATERIALS.value)
        self.assertFalse(audit["summary"]["production_scoring_changed"])
        self.assertFalse(audit["summary"]["candidate_generation_input"])
        self.assertTrue(audit["summary"]["shadow_weight_only"])
        self.assertIn("do_not_use_round214_cases_as_candidate_generation_input", audit["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])
        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round214_r10_loop8_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)

            records = load_case_library(paths["cases"])
            rows = round214_case_rows()
            self.assertEqual(len(records), len(ROUND214_CASE_CANDIDATES))
            self.assertEqual(len(rows), len(ROUND214_CASE_CANDIDATES))
            self.assertIn("삼성E&A", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("epc_margin_visibility", paths["score_adjustments"].read_text(encoding="utf-8"))
            self.assertIn("pf_workout_debt_reschedule", paths["stage4b_4c_review"].read_text(encoding="utf-8"))
            self.assertEqual(json.loads(rows[0]["extra_price_metrics"])["contract_value_usd_bn"], 6.0)


if __name__ == "__main__":
    unittest.main()
