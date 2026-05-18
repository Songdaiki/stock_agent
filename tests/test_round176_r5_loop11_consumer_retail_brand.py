import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round176_r5_loop11_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round176_r5_loop11_consumer_retail_brand import (
    ROUND176_BASE_SCORE_WEIGHTS,
    ROUND176_CASE_CANDIDATES,
    ROUND176_PRICE_FIELDS,
    ROUND176_SCORE_STAGE_PRICE_ALIGNMENT,
    ROUND176_SCORE_TARGETS,
    ROUND176_SOURCE_CANONICAL_TARGET_COUNT,
    ROUND176_SOURCE_CANONICAL_TARGET_IDS,
    ROUND176_STAGE_CAPS,
    render_round176_green_guardrail_markdown,
    render_round176_price_validation_plan_markdown,
    render_round176_risk_overlay_markdown,
    render_round176_score_stage_price_alignment_markdown,
    render_round176_summary_markdown,
    round176_base_score_weight_rows,
    round176_case_candidate_rows,
    round176_case_records,
    round176_price_field_rows,
    round176_score_profile_rows,
    round176_score_stage_price_alignment_rows,
    round176_stage_cap_rows,
    round176_stage_date_rows,
    round176_summary,
    round176_target_for,
    write_round176_r5_loop11_reports,
)


class Round176R5Loop11ConsumerRetailBrandTests(unittest.TestCase):
    def test_round176_targets_cover_source_and_auxiliary_archetypes(self):
        labels = {target.target_id for target in ROUND176_SCORE_TARGETS}

        self.assertEqual(ROUND176_SOURCE_CANONICAL_TARGET_COUNT, 11)
        self.assertEqual(len(labels), 13)
        self.assertTrue(set(ROUND176_SOURCE_CANONICAL_TARGET_IDS).issubset(labels))
        self.assertIn("K_BEAUTY_BRAND_MNA_VALIDATION_STAGE2_REFERENCE", labels)
        self.assertIn("STRONG_PRIVATE_PLATFORM_BUT_HOLDCO_LINK_CAP", labels)
        for target in ROUND176_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.CONSUMER_RETAIL_BRAND)
            self.assertFalse(target.production_scoring_changed)

    def test_new_r5_loop11_consumer_archetypes_exist(self):
        expected = (
            E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION_KOREA,
            E2RArchetype.K_BEAUTY_BRAND_US_CHANNEL,
            E2RArchetype.K_BEAUTY_RETAIL_PLATFORM_OPTION,
            E2RArchetype.K_BEAUTY_OEM_ODM_SUPPLYCHAIN_KOREA,
            E2RArchetype.K_FOOD_GLOBAL_STAPLE_BRAND,
            E2RArchetype.K_FOOD_SINGLE_SKU_RISK,
            E2RArchetype.APPAREL_LICENSE_BRAND_CHINA_RISK,
            E2RArchetype.CHINA_CONSUMER_EXPOSURE_4C,
            E2RArchetype.TARIFF_IMPORT_MARGIN_OVERLAY,
            E2RArchetype.CHANNEL_STUFFING_INVENTORY_OVERLAY,
            E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
            E2RArchetype.K_BEAUTY_BRAND_MNA_VALIDATION_STAGE2_REFERENCE,
            E2RArchetype.STRONG_PRIVATE_PLATFORM_BUT_HOLDCO_LINK_CAP,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_loop11_base_score_weights_and_stage_caps_match_round_note(self):
        weights = {row["component"]: row for row in round176_base_score_weight_rows()}
        caps = {row["stage_band"]: row for row in round176_stage_cap_rows()}

        self.assertEqual(len(ROUND176_BASE_SCORE_WEIGHTS), 7)
        self.assertEqual(weights["eps_fcf_opm_conversion"]["points"], "23")
        self.assertEqual(weights["export_channel_visibility"]["points"], "21")
        self.assertEqual(weights["sell_through_reorder_repeat_consumption"]["points"], "18")
        self.assertEqual(weights["inventory_receivables_margin_quality"]["points"], "12")
        self.assertEqual(weights["early_price_path_validation"]["points"], "10")
        self.assertEqual(weights["safety_tariff_disclosure_confidence"]["points"], "8")
        self.assertEqual(weights["valuation_room_4b_runway"]["points"], "8")
        self.assertEqual(len(ROUND176_STAGE_CAPS), 5)
        self.assertEqual(caps["Stage 1"]["max_score"], "45")
        self.assertEqual(caps["Stage 2"]["max_score"], "70")
        self.assertIn("requires_4_of_7", caps["Stage 3"]["max_score"])
        self.assertIn("sell_through_or_reorder", caps["Stage 3"]["required_evidence"])
        self.assertIn("requires_3_of_5", caps["Stage 4B"]["max_score"])
        self.assertIn("channel_stuffing", caps["Stage 4C"]["required_evidence"])

    def test_target_rules_separate_green_candidates_from_redteam_overlays(self):
        distribution = round176_target_for("K_BEAUTY_EXPORT_DISTRIBUTION_KOREA")
        brand = round176_target_for("K_BEAUTY_BRAND_US_CHANNEL")
        platform = round176_target_for("K_BEAUTY_RETAIL_PLATFORM_OPTION")
        odm = round176_target_for("K_BEAUTY_OEM_ODM_SUPPLYCHAIN_KOREA")
        food = round176_target_for("K_FOOD_GLOBAL_STAPLE_BRAND")
        single_sku = round176_target_for("K_FOOD_SINGLE_SKU_RISK")
        apparel = round176_target_for("APPAREL_LICENSE_BRAND_CHINA_RISK")
        china = round176_target_for("CHINA_CONSUMER_EXPOSURE_4C")
        tariff = round176_target_for("TARIFF_IMPORT_MARGIN_OVERLAY")
        channel = round176_target_for("CHANNEL_STUFFING_INVENTORY_OVERLAY")
        disclosure = round176_target_for("DISCLOSURE_CONFIDENCE_CAP")
        mna = round176_target_for("K_BEAUTY_BRAND_MNA_VALIDATION_STAGE2_REFERENCE")
        holdco = round176_target_for("STRONG_PRIVATE_PLATFORM_BUT_HOLDCO_LINK_CAP")

        for target in (distribution, brand, platform, odm, food, single_sku, apparel, china, tariff, channel, disclosure, mna, holdco):
            self.assertIsNotNone(target)
        assert distribution is not None
        assert brand is not None
        assert platform is not None
        assert odm is not None
        assert food is not None
        assert single_sku is not None
        assert apparel is not None
        assert china is not None
        assert tariff is not None
        assert channel is not None
        assert disclosure is not None
        assert mna is not None
        assert holdco is not None
        self.assertEqual(distribution.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("sell_through", distribution.green_conditions)
        self.assertEqual(brand.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("ipo_price_doubles", brand.stage4b_conditions)
        self.assertIn("cj_consolidated_earnings_link", platform.stage3_conditions)
        self.assertIn("repeat_orders", odm.stage3_conditions)
        self.assertIn("walmart_mainstream_shelf", food.stage2_signals)
        self.assertTrue(single_sku.hard_gate)
        self.assertIn("single_sku_dependency", single_sku.red_flags)
        self.assertEqual(apparel.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertTrue(china.hard_gate)
        self.assertTrue(tariff.hard_gate)
        self.assertTrue(channel.hard_gate)
        self.assertEqual(disclosure.score_weight.eps_fcf_opm, "cap")
        self.assertIn("global_major_acquires_korean_brand", mna.stage2_signals)
        self.assertTrue(holdco.hard_gate)

    def test_required_round176_cases_are_present_with_stage_markers(self):
        rows = {row["case_id"]: row for row in round176_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND176_CASE_CANDIDATES))
        self.assertEqual(rows["silicon2_kbeauty_distribution_stage3_candidate"]["target_id"], "K_BEAUTY_EXPORT_DISTRIBUTION_KOREA")
        self.assertIn("physical_store_sell_through_needed", rows["silicon2_kbeauty_distribution_stage3_candidate"]["evidence_fields"])
        self.assertEqual(rows["dalba_global_ipo_4b_watch_case"]["stage4b_date"], "2025-06-05")
        self.assertEqual(rows["cj_oliveyoung_platform_holdco_cap_case"]["target_id"], "K_BEAUTY_RETAIL_PLATFORM_OPTION")
        self.assertEqual(rows["nongshim_global_staple_stage2_case"]["target_id"], "K_FOOD_GLOBAL_STAPLE_BRAND")
        self.assertEqual(rows["kbeauty_oem_odm_supplychain_stage3_candidate"]["target_id"], "K_BEAUTY_OEM_ODM_SUPPLYCHAIN_KOREA")
        self.assertEqual(rows["drg_kbeauty_mna_stage2_reference_case"]["stage2_date"], "2024-12-23")
        self.assertEqual(rows["amorepacific_china_exposure_4c_case"]["case_type"], "4c_thesis_break")
        self.assertEqual(rows["kbeauty_tariff_import_margin_review_case"]["target_id"], "TARIFF_IMPORT_MARGIN_OVERLAY")
        self.assertEqual(rows["fnf_license_brand_china_mna_watch_case"]["stage1_date"], "2025-07-21")
        self.assertEqual(rows["channel_stuffing_inventory_overlay_case"]["target_id"], "CHANNEL_STUFFING_INVENTORY_OVERLAY")
        self.assertEqual(rows["kfood_single_sku_viral_risk_case"]["case_type"], "event_premium")

    def test_case_records_validate_and_keep_round176_guardrails(self):
        records = round176_case_records()

        self.assertEqual(len(records), len(ROUND176_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "CONSUMER_RETAIL_BRAND")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("brand_awareness_or_listing_is_not_structural_evidence", record.green_guardrails)
            self.assertIn("require_export_channel_sellthrough_reorder_inventory_receivables_opm_fcf_for_green", record.green_guardrails)
            self.assertIn("stage3_early_catch_requires_4_of_7_loop11_conditions", record.green_guardrails)
            self.assertIn("do_not_invent_channel_sellthrough_reorder_inventory_receivables_margin_stage_prices_or_mfe_mae", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["dalba_global_ipo_4b_watch_case"].rerating_result, "theme_overheat")
        self.assertEqual(by_id["amorepacific_china_exposure_4c_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["channel_stuffing_inventory_overlay_case"].score_price_alignment, "false_positive_score")
        self.assertIn("sell_through", by_id["silicon2_kbeauty_distribution_stage3_candidate"].must_have_fields)
        self.assertIn("cj_cashflow_link_missing", by_id["cj_oliveyoung_platform_holdco_cap_case"].red_flag_fields)

    def test_score_profile_rows_mark_no_production_change(self):
        rows = round176_score_profile_rows()

        self.assertEqual(len(rows), len(ROUND176_SCORE_TARGETS))
        for row in rows:
            self.assertEqual(row["large_sector"], "CONSUMER_RETAIL_BRAND")
            self.assertEqual(row["production_scoring_changed"], "false")
            self.assertIn("loop11_penalty_axes", row)
        by_target = {row["target_id"]: row for row in rows}
        self.assertEqual(by_target["K_BEAUTY_EXPORT_DISTRIBUTION_KOREA"]["export_channel_visibility"], "22")
        self.assertEqual(by_target["K_BEAUTY_OEM_ODM_SUPPLYCHAIN_KOREA"]["inventory_receivables_margin_quality"], "13")
        self.assertEqual(by_target["K_FOOD_SINGLE_SKU_RISK"]["hard_gate"], "true")
        self.assertEqual(by_target["TARIFF_IMPORT_MARGIN_OVERLAY"]["eps_fcf_opm"], "gate")
        self.assertEqual(by_target["DISCLOSURE_CONFIDENCE_CAP"]["eps_fcf_opm"], "cap")
        self.assertEqual(by_target["STRONG_PRIVATE_PLATFORM_BUT_HOLDCO_LINK_CAP"]["hard_gate"], "true")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round176_stage_date_rows()}
        fields = {row["field"] for row in round176_price_field_rows()}

        self.assertIn("sell_through", rows["K_BEAUTY_EXPORT_DISTRIBUTION_KOREA"]["stage3"])
        self.assertIn("ipo_price_doubles", rows["K_BEAUTY_BRAND_US_CHANNEL"]["stage4b"])
        self.assertIn("walmart_mainstream_shelf", rows["K_FOOD_GLOBAL_STAPLE_BRAND"]["stage2"])
        self.assertIn("china_demand_weakness", rows["CHINA_CONSUMER_EXPOSURE_4C"]["stage4c"])
        self.assertIn("inventory_days_up", rows["CHANNEL_STUFFING_INVENTORY_OVERLAY"]["stage4c"])
        for field in (
            "return_60d_after_stage2",
            "return_120d_after_stage2",
            "mfe_60d_after_stage2",
            "mae_60d_after_stage2",
            "relative_strength_vs_consumer_basket",
            "relative_strength_vs_kbeauty_basket",
            "export_growth_yoy",
            "us_sales_growth_yoy",
            "japan_sales_growth_yoy",
            "europe_sales_growth_yoy",
            "amazon_sales_signal",
            "tiktok_sales_signal",
            "ulta_sephora_costco_target_signal",
            "offline_sell_through_signal",
            "reorder_signal",
            "inventory_days_change",
            "receivables_days_change",
            "gross_margin",
            "opm",
            "discount_rate_signal",
            "tariff_exposure",
            "china_exposure",
            "single_sku_dependency",
            "holdco_cashflow_link",
            "nav_discount_signal",
            "valuation_at_stage4b",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)

    def test_score_stage_price_alignment_rows_and_markdown(self):
        rows = {row["case_id"]: row for row in round176_score_stage_price_alignment_rows()}
        markdown = render_round176_score_stage_price_alignment_markdown()

        self.assertEqual(len(rows), len(ROUND176_SCORE_STAGE_PRICE_ALIGNMENT))
        self.assertEqual(rows["silicon2_kbeauty_distribution_stage3_candidate"]["verdict"], "portfolio_distribution_not_brand_keyword")
        self.assertEqual(rows["dalba_global_ipo_4b_watch_case"]["verdict"], "ipo_double_requires_4b_watch")
        self.assertEqual(rows["cj_oliveyoung_platform_holdco_cap_case"]["verdict"], "holdco_link_cap")
        self.assertEqual(rows["amorepacific_china_exposure_4c_case"]["verdict"], "china_exposure_4c_alignment")
        self.assertIn("Silicon2", markdown)
        self.assertIn("D'Alba", markdown)
        self.assertIn("tariff", markdown.lower())

    def test_summary_and_markdown_explain_r5_loop11_guardrails(self):
        summary = round176_summary()
        summary_md = render_round176_summary_markdown()
        guardrails = render_round176_green_guardrail_markdown()
        overlays = render_round176_risk_overlay_markdown()
        price_plan = render_round176_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 13)
        self.assertEqual(summary["source_canonical_target_count"], 11)
        self.assertEqual(summary["case_candidate_count"], len(ROUND176_CASE_CANDIDATES))
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R5 Loop 11", summary_md)
        self.assertIn("EPS/FCF/OPM 23", summary_md)
        self.assertIn("Do not apply R5 Loop-11", guardrails)
        self.assertIn("SELL_THROUGH_REQUIRED", overlays)
        self.assertIn("dalba_global_ipo_4b_watch_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            paths = write_round176_r5_loop11_reports(
                output_directory=tmp_path / "out",
                cases_path=tmp_path / "cases.jsonl",
                score_profile_path=tmp_path / "profiles.csv",
            )

            for path in paths.values():
                self.assertTrue(path.exists(), path)
            records = load_case_library(paths["cases"])
            self.assertEqual(len(records), len(ROUND176_CASE_CANDIDATES))
            summary = paths["summary"].read_text(encoding="utf-8")
            self.assertIn("Round-176 R5 Loop-11", summary)
            self.assertIn("production_scoring_changed: false", summary)

    def test_cli_argument_parser_supports_paths(self):
        parser = build_parser()
        args = parser.parse_args(
            [
                "--output-directory",
                "out",
                "--cases",
                "cases.jsonl",
                "--score-profiles",
                "profiles.csv",
            ]
        )

        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.score_profiles, "profiles.csv")

    def test_production_scoring_modules_do_not_import_round176_pack(self):
        root = Path(__file__).resolve().parents[1]
        forbidden = "round176_r5_loop11_consumer_retail_brand"
        for relative in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/scoring.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = (root / relative).read_text(encoding="utf-8")
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
