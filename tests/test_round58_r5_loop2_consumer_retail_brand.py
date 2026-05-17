import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round58_r5_loop2_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round58_r5_loop2_consumer_retail_brand import (
    ROUND58_CASE_CANDIDATES,
    ROUND58_PRICE_FIELDS,
    ROUND58_SCORE_TARGETS,
    render_round58_green_guardrail_markdown,
    render_round58_price_validation_plan_markdown,
    render_round58_risk_overlay_markdown,
    render_round58_summary_markdown,
    round58_case_candidate_rows,
    round58_case_records,
    round58_price_field_rows,
    round58_score_profile_rows,
    round58_stage_date_rows,
    round58_summary,
    target_for,
    write_round58_r5_loop2_reports,
)


class Round58R5Loop2ConsumerRetailBrandTests(unittest.TestCase):
    def test_round58_targets_cover_r5_loop2_archetypes(self):
        labels = {target.target_id for target in ROUND58_SCORE_TARGETS}

        self.assertEqual(len(labels), 12)
        for label in (
            "EXPORT_RECURRING_CONSUMER",
            "K_BEAUTY_EXPORT_DISTRIBUTION",
            "BEAUTY_OEM_ODM_SUPPLYCHAIN",
            "RETAIL_CONVENIENCE_OFFLINE",
            "RETAIL_ECOMMERCE_LOGISTICS",
            "ECOMMERCE_FRESH_LOGISTICS",
            "APPAREL_FAST_FASHION_BRAND_OEM",
            "HOME_LIVING_APPLIANCE_RENTAL",
            "HOME_CHILD_EDUCATION",
            "CONSUMER_REGULATED_PRODUCT",
            "FOOD_SAFETY_RECALL_OVERLAY",
            "DATA_SECURITY_SUPPLIER_REGULATION_OVERLAY",
        ):
            self.assertIn(label, labels)
        for target in ROUND58_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.CONSUMER_RETAIL_BRAND)
            self.assertFalse(target.production_scoring_changed)

    def test_new_r5_loop2_canonical_archetypes_exist(self):
        expected = (
            E2RArchetype.BEAUTY_DEVICE_EXPORT,
            E2RArchetype.FOOD_SAFETY_RECALL_OVERLAY,
            E2RArchetype.DATA_SECURITY_SUPPLIER_REGULATION_OVERLAY,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_kfood_kbeauty_and_beauty_oem_remain_green_possible_but_guardrailed(self):
        export = target_for("EXPORT_RECURRING_CONSUMER")
        kbeauty = target_for("K_BEAUTY_EXPORT_DISTRIBUTION")
        oem = target_for("BEAUTY_OEM_ODM_SUPPLYCHAIN")

        assert export is not None
        assert kbeauty is not None
        assert oem is not None
        for target in (export, kbeauty, oem):
            self.assertEqual(target.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("channel_sell_through", export.green_conditions)
        self.assertIn("single_product_dependency", export.red_flags)
        self.assertIn("offline_channel_sell_through", kbeauty.green_conditions)
        self.assertIn("receivables_growth", kbeauty.red_flags)
        self.assertIn("customer_diversification", oem.green_conditions)
        self.assertIn("customer_concentration", oem.red_flags)

    def test_overlays_are_gate_only_redteam(self):
        food = target_for("FOOD_SAFETY_RECALL_OVERLAY")
        data = target_for("DATA_SECURITY_SUPPLIER_REGULATION_OVERLAY")

        assert food is not None
        assert data is not None
        self.assertEqual(food.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertTrue(food.gate_only)
        self.assertEqual(food.score_weight.eps_fcf, "gate")
        self.assertIn("recall_flag", food.stage4c_conditions)
        self.assertEqual(data.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertTrue(data.gate_only)
        self.assertIn("data_breach_flag", data.stage4c_conditions)
        self.assertIn("payment_delay", data.red_flags)

    def test_ecommerce_hardware_and_fast_fashion_have_explicit_4c_risks(self):
        ecommerce = target_for("RETAIL_ECOMMERCE_LOGISTICS")
        appliance = target_for("HOME_LIVING_APPLIANCE_RENTAL")
        apparel = target_for("APPAREL_FAST_FASHION_BRAND_OEM")

        assert ecommerce is not None
        assert appliance is not None
        assert apparel is not None
        self.assertIn("data_breach", ecommerce.red_flags)
        self.assertIn("supplier_pressure", ecommerce.red_flags)
        self.assertIn("hardware_cycle", appliance.red_flags)
        self.assertIn("dividend_suspension", appliance.stage4c_conditions)
        self.assertIn("ip_litigation", apparel.red_flags)
        self.assertIn("customs_scrutiny", apparel.red_flags)

    def test_required_round58_cases_are_present_with_dates_and_alignment(self):
        rows = {row["case_id"]: row for row in round58_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND58_CASE_CANDIDATES))
        self.assertEqual(rows["samyang_buldak_export_rerating_case"]["stage2_date"], "2024-06-14")
        self.assertEqual(rows["samyang_buldak_denmark_recall_case"]["stage4c_date"], "2024-06-12")
        self.assertEqual(rows["kbeauty_us_export_overtake_france_case"]["stage2_date"], "2025-06-05")
        self.assertEqual(rows["kbeauty_tariff_risk_case"]["stage4c_date"], "")
        self.assertEqual(rows["apr_medicube_beauty_device_case"]["stage2_date"], "2025-10-20")
        self.assertEqual(rows["apr_medicube_beauty_device_case"]["stage4b_date"], "2025-10-20")
        self.assertEqual(rows["medicube_ulta_tiktok_omnichannel_case"]["stage2_date"], "2026-02-13")
        self.assertEqual(rows["coupang_supplier_regulation_case"]["stage4c_date"], "2026-02-26")
        self.assertEqual(rows["coupang_data_breach_case"]["stage4c_date"], "")
        self.assertEqual(rows["coway_rental_recurring_case"]["stage2_date"], "")
        self.assertEqual(rows["whirlpool_dividend_suspension_case"]["stage4c_date"], "")
        self.assertEqual(rows["shein_temu_ip_litigation_case"]["stage4c_date"], "2026-05-11")

    def test_case_records_validate_and_keep_round58_guardrails(self):
        records = round58_case_records()

        self.assertEqual(len(records), len(ROUND58_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("consumer_sales_growth_is_not_structural_evidence_alone", record.green_guardrails)
            self.assertIn("do_not_invent_export_sell_through_reorder_inventory_receivables_or_stage_prices", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["samyang_buldak_export_rerating_case"].score_price_alignment, "aligned")
        self.assertEqual(by_id["apr_medicube_beauty_device_case"].rerating_result, "theme_overheat")
        self.assertEqual(by_id["coupang_data_breach_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["shein_temu_ip_litigation_case"].score_price_alignment, "false_positive_score")
        self.assertIn(E2RArchetype.BEAUTY_DEVICE_EXPORT, by_id["apr_medicube_beauty_device_case"].secondary_archetypes)

    def test_score_profile_rows_match_round58_weight_table(self):
        rows = {row["target_id"]: row for row in round58_score_profile_rows()}

        self.assertEqual(rows["EXPORT_RECURRING_CONSUMER"]["eps_fcf"], "22")
        self.assertEqual(rows["K_BEAUTY_EXPORT_DISTRIBUTION"]["structural_visibility"], "23")
        self.assertEqual(rows["BEAUTY_OEM_ODM_SUPPLYCHAIN"]["structural_visibility"], "22")
        self.assertEqual(rows["RETAIL_ECOMMERCE_LOGISTICS"]["eps_fcf"], "17")
        self.assertEqual(rows["HOME_LIVING_APPLIANCE_RENTAL"]["valuation"], "11")
        self.assertEqual(rows["FOOD_SAFETY_RECALL_OVERLAY"]["gate_only"], "true")
        self.assertEqual(rows["FOOD_SAFETY_RECALL_OVERLAY"]["eps_fcf"], "gate")
        self.assertEqual(rows["DATA_SECURITY_SUPPLIER_REGULATION_OVERLAY"]["gate_only"], "true")
        for row in rows.values():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round58_stage_date_rows()}
        fields = {row["field"] for row in round58_price_field_rows()}

        self.assertIn("channel_sell_through", rows["EXPORT_RECURRING_CONSUMER"]["stage3"])
        self.assertIn("sell_through", rows["K_BEAUTY_EXPORT_DISTRIBUTION"]["stage3"])
        self.assertIn("data_breach", rows["RETAIL_ECOMMERCE_LOGISTICS"]["stage4c"])
        self.assertIn("recall_flag", rows["FOOD_SAFETY_RECALL_OVERLAY"]["stage4c"])
        for field in (
            "export_sales_growth",
            "sell_through_signal",
            "reorder_signal",
            "offline_channel_count",
            "tiktok_shop_sales",
            "inventory_growth",
            "receivables_growth",
            "channel_stuffing_risk_flag",
            "recall_flag",
            "beauty_device_revenue",
            "supplier_regulation_flag",
            "payment_delay_flag",
            "data_breach_flag",
            "rental_accounts",
            "rental_churn",
            "dividend_suspension_flag",
            "ip_litigation_flag",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND58_PRICE_FIELDS))

    def test_summary_and_markdown_explain_r5_loop2_guardrails(self):
        summary = round58_summary()
        summary_md = render_round58_summary_markdown()
        guardrails = render_round58_green_guardrail_markdown()
        overlays = render_round58_risk_overlay_markdown()
        price_plan = render_round58_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 12)
        self.assertEqual(summary["case_candidate_count"], 11)
        self.assertEqual(summary["success_candidate_count"], 4)
        self.assertEqual(summary["stage4b_case_count"], 1)
        self.assertEqual(summary["stage4c_case_count"], 6)
        self.assertEqual(summary["green_possible_count"], 3)
        self.assertEqual(summary["watch_yellow_first_count"], 6)
        self.assertEqual(summary["redteam_first_count"], 3)
        self.assertEqual(summary["gate_only_target_count"], 2)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R5 Loop 2", summary_md)
        self.assertIn("Do not apply R5 Loop-2 v2.0 weights", guardrails)
        self.assertIn("ECOMMERCE_SCALE_WITH_TRUST_RISK", overlays)
        self.assertIn("samyang_buldak_export_rerating_case", price_plan)
        self.assertIn("coupang_data_breach_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round58_r5_loop2_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r5_loop2_round58.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round58_r5_loop2_v2.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["stage_date_plan"].exists())
            self.assertTrue(paths["green_guardrails"].exists())
            self.assertTrue(paths["risk_overlays"].exists())
            self.assertTrue(paths["price_validation_plan"].exists())
            self.assertTrue(paths["price_fields"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND58_CASE_CANDIDATES))

    def test_cli_argument_parser_supports_paths(self):
        args = build_parser().parse_args(
            [
                "--output-directory",
                "out",
                "--cases",
                "cases.jsonl",
                "--score-profiles",
                "scores.csv",
            ]
        )

        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.score_profiles, "scores.csv")

    def test_production_scoring_modules_do_not_import_round58_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round58_r5_loop2_consumer_retail_brand", text)


if __name__ == "__main__":
    unittest.main()
