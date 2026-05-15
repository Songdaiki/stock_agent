import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round45_r5_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round45_r5_consumer_retail_brand import (
    ROUND45_CASE_CANDIDATES,
    ROUND45_PRICE_FIELDS,
    ROUND45_SCORE_TARGETS,
    render_round45_green_guardrail_markdown,
    render_round45_price_validation_plan_markdown,
    render_round45_summary_markdown,
    round45_case_candidate_rows,
    round45_case_records,
    round45_price_field_rows,
    round45_score_profile_rows,
    round45_stage_date_rows,
    round45_summary,
    target_for,
    write_round45_r5_reports,
)


class Round45R5ConsumerRetailBrandTests(unittest.TestCase):
    def test_round45_targets_cover_r5_archetypes(self):
        labels = {target.target_id for target in ROUND45_SCORE_TARGETS}

        self.assertEqual(len(labels), 11)
        self.assertIn("EXPORT_RECURRING_CONSUMER", labels)
        self.assertIn("K_BEAUTY_EXPORT_DISTRIBUTION", labels)
        self.assertIn("BEAUTY_OEM_ODM_SUPPLYCHAIN", labels)
        self.assertIn("RETAIL_ECOMMERCE_LOGISTICS", labels)
        self.assertIn("HOME_LIVING_APPLIANCE_RENTAL", labels)
        self.assertIn("CONSUMER_REGULATED_PRODUCT", labels)
        for target in ROUND45_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.CONSUMER_RETAIL_BRAND)
            self.assertFalse(target.production_scoring_changed)

    def test_new_r5_canonical_archetypes_exist(self):
        expected = {
            E2RArchetype.FOOD_AGRI_LIVESTOCK_CYCLE,
            E2RArchetype.RETAIL_CONVENIENCE_OFFLINE,
            E2RArchetype.RETAIL_ECOMMERCE_LOGISTICS,
            E2RArchetype.ECOMMERCE_FRESH_LOGISTICS,
            E2RArchetype.BEAUTY_OEM_ODM_SUPPLYCHAIN,
            E2RArchetype.APPAREL_FAST_FASHION_BRAND_OEM,
            E2RArchetype.HOME_LIVING_APPLIANCE_RENTAL,
            E2RArchetype.HOME_CHILD_EDUCATION,
            E2RArchetype.CONSUMER_REGULATED_PRODUCT,
        }

        self.assertTrue(expected.issubset(set(E2RArchetype)))

    def test_export_food_and_kbeauty_are_green_possible_but_guardrailed(self):
        export = target_for("EXPORT_RECURRING_CONSUMER")
        kbeauty = target_for("K_BEAUTY_EXPORT_DISTRIBUTION")

        self.assertIsNotNone(export)
        self.assertIsNotNone(kbeauty)
        assert export is not None
        assert kbeauty is not None
        self.assertEqual(export.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("recurring_demand", export.green_conditions)
        self.assertIn("single_product_dependency", export.red_flags)
        self.assertEqual(kbeauty.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("sell_through", kbeauty.green_conditions)
        self.assertIn("receivables_growth", kbeauty.red_flags)

    def test_ecommerce_and_hardware_cases_keep_redteam_risks(self):
        ecommerce = target_for("RETAIL_ECOMMERCE_LOGISTICS")
        appliance = target_for("HOME_LIVING_APPLIANCE_RENTAL")

        self.assertIsNotNone(ecommerce)
        self.assertIsNotNone(appliance)
        assert ecommerce is not None
        assert appliance is not None
        self.assertEqual(ecommerce.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("data_breach", ecommerce.red_flags)
        self.assertIn("supplier_pressure", ecommerce.red_flags)
        self.assertEqual(appliance.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("dividend_cut", appliance.red_flags)
        self.assertIn("hardware_cycle", appliance.red_flags)

    def test_case_records_validate_and_keep_price_backfill_open(self):
        records = round45_case_records()

        self.assertEqual(len(records), len(ROUND45_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("sell_through_and_fcf_required_for_green", record.green_guardrails)
            self.assertIn("consumer_sales_growth_is_not_structural_evidence_alone", record.green_guardrails)

    def test_required_round45_cases_are_present_with_stage_dates(self):
        records = {record.case_id: record for record in round45_case_records()}

        self.assertEqual(str(records["samyang_buldak_export_rerating_case"].stage2_date), "2024-06-14")
        self.assertEqual(records["samyang_buldak_export_rerating_case"].score_price_alignment, "aligned")
        self.assertEqual(str(records["samyang_buldak_recall_risk_case"].stage4c_date), "2024-06-12")
        self.assertEqual(str(records["kbeauty_us_offline_channel_case"].stage2_date), "2025-06-05")
        self.assertIsNone(records["apr_medicube_device_export_case"].stage2_date)
        self.assertEqual(records["apr_medicube_device_export_case"].case_type, "4b_watch")
        self.assertEqual(str(records["coupang_supplier_regulation_case"].stage4c_date), "2026-02-26")
        self.assertIsNone(records["coupang_data_breach_case"].stage4c_date)
        self.assertEqual(str(records["whirlpool_hardware_cycle_4c_case"].stage4c_date), "2026-05-07")
        self.assertEqual(str(records["shein_temu_ip_regulatory_case"].stage4c_date), "2026-05-11")

    def test_score_profile_rows_mark_no_production_change(self):
        rows = {row["target_id"]: row for row in round45_score_profile_rows()}

        self.assertEqual(rows["EXPORT_RECURRING_CONSUMER"]["large_sector"], "CONSUMER_RETAIL_BRAND")
        self.assertEqual(rows["EXPORT_RECURRING_CONSUMER"]["production_scoring_changed"], "false")
        self.assertEqual(rows["FOOD_AGRI_LIVESTOCK_CYCLE"]["posture"], "REDTEAM_FIRST")
        self.assertIn("stage4c_conditions", rows["RETAIL_ECOMMERCE_LOGISTICS"])

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round45_stage_date_rows()}
        fields = {row["field"] for row in round45_price_field_rows()}

        self.assertIn("K_BEAUTY_EXPORT_DISTRIBUTION", rows)
        self.assertIn("sell_through", rows["K_BEAUTY_EXPORT_DISTRIBUTION"]["stage3"])
        for field in (
            "stage2_price",
            "MFE_180D",
            "export_sales_growth",
            "channel_sell_through_signal",
            "receivables_growth",
            "rental_accounts",
            "data_breach_flag",
            "ip_litigation_flag",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND45_PRICE_FIELDS))

    def test_summary_and_markdown_explain_r5_guardrails(self):
        summary = round45_summary()
        summary_md = render_round45_summary_markdown()
        guardrails = render_round45_green_guardrail_markdown()
        price_plan = render_round45_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 11)
        self.assertEqual(summary["case_candidate_count"], len(ROUND45_CASE_CANDIDATES))
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("repeat export/channel rerating", summary_md)
        self.assertIn("Do not apply these R5 v1.0 weights", guardrails)
        self.assertIn("samyang_buldak_export_rerating_case", price_plan)
        self.assertIn("coupang_data_breach_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round45_r5_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r5_round45.jsonl",
                score_profile_path=Path(tmp) / "score_profiles.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["stage_date_plan"].exists())
            self.assertTrue(paths["green_guardrails"].exists())
            self.assertTrue(paths["price_validation_plan"].exists())
            self.assertTrue(paths["price_fields"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND45_CASE_CANDIDATES))

    def test_case_matrix_records_are_not_production_inputs(self):
        rows = round45_case_candidate_rows()

        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row["production_input"], "false")

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

    def test_production_scoring_modules_do_not_import_round45_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round45_r5_consumer_retail_brand", text)


if __name__ == "__main__":
    unittest.main()
