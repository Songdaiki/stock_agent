import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round189_r5_loop12_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round189_r5_loop12_consumer_retail_brand import (
    ROUND189_BASE_SCORE_WEIGHTS,
    ROUND189_CASE_CANDIDATES,
    ROUND189_PRICE_FIELDS,
    ROUND189_SCORE_TARGETS,
    ROUND189_SOURCE_CANONICAL_TARGET_COUNT,
    ROUND189_SOURCE_CANONICAL_TARGET_IDS,
    ROUND189_STAGE_CAPS,
    render_round189_green_guardrail_markdown,
    render_round189_price_validation_plan_markdown,
    render_round189_risk_overlay_markdown,
    render_round189_score_stage_price_alignment_markdown,
    render_round189_summary_markdown,
    round189_base_score_weight_rows,
    round189_case_candidate_rows,
    round189_case_records,
    round189_price_field_rows,
    round189_score_profile_rows,
    round189_score_stage_price_alignment_rows,
    round189_stage_cap_rows,
    round189_stage_date_rows,
    round189_summary,
    round189_target_for,
    write_round189_r5_loop12_reports,
)


class Round189R5Loop12ConsumerRetailBrandTests(unittest.TestCase):
    def test_round189_targets_cover_loop12_archetypes(self):
        labels = {target.target_id for target in ROUND189_SCORE_TARGETS}

        self.assertEqual(len(labels), 11)
        self.assertEqual(ROUND189_SOURCE_CANONICAL_TARGET_COUNT, 11)
        self.assertEqual(set(ROUND189_SOURCE_CANONICAL_TARGET_IDS), labels)
        for target in ROUND189_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.CONSUMER_RETAIL_BRAND)
            self.assertFalse(target.production_scoring_changed)

    def test_new_loop12_canonical_archetypes_exist(self):
        expected = (
            E2RArchetype.K_FOOD_GLOBAL_LOCALIZATION,
            E2RArchetype.K_FOOD_GLOBAL_STAPLE_BRAND_SECOND_WAVE,
            E2RArchetype.K_FOOD_SINGLE_SKU_EXPORT_RISK,
            E2RArchetype.ECOMMERCE_RESTRUCTURING_JV_KOREA,
            E2RArchetype.RETAIL_PLATFORM_DATA_REGULATION_OVERLAY,
            E2RArchetype.DEPARTMENT_STORE_MALL_REDEVELOPMENT,
            E2RArchetype.CONVENIENCE_STORE_PB_SSSG_KOREA,
            E2RArchetype.K_BEAUTY_BRAND_SECOND_WAVE,
            E2RArchetype.K_BEAUTY_TARIFF_IMPORT_REVIEW,
            E2RArchetype.CHANNEL_STUFFING_INVENTORY_OVERLAY,
            E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_base_weights_and_stage_caps_match_round189_note(self):
        weights = {row["component"]: row for row in round189_base_score_weight_rows()}
        caps = {row["stage_band"]: row for row in round189_stage_cap_rows()}

        self.assertEqual(len(ROUND189_BASE_SCORE_WEIGHTS), 7)
        self.assertEqual(weights["eps_fcf_opm_conversion"]["points"], "24")
        self.assertEqual(weights["overseas_channel_localization_platform_visibility"]["points"], "20")
        self.assertEqual(weights["sellthrough_reorder_recurring_consumption"]["points"], "18")
        self.assertEqual(weights["inventory_receivables_margin_quality"]["points"], "12")
        self.assertEqual(weights["early_price_validation"]["points"], "10")
        self.assertEqual(weights["tariff_regulation_capex_disclosure_redteam"]["points"], "10")
        self.assertEqual(weights["valuation_4b_room"]["points"], "6")
        self.assertEqual(len(ROUND189_STAGE_CAPS), 5)
        self.assertEqual(caps["Stage 3"]["max_score"], "requires_5_of_8")
        self.assertIn("sellthrough_or_reorder_evidence", caps["Stage 3"]["required_evidence"])
        self.assertEqual(caps["Stage 4B"]["max_score"], "requires_4_of_6")
        self.assertIn("viral_or_channel_entry_priced_before_sellthrough", caps["Stage 4B"]["required_evidence"])
        self.assertEqual(caps["Stage 4C"]["max_score"], "hard_gate")
        self.assertIn("channel_inventory_or_receivables_spike", caps["Stage 4C"]["required_evidence"])
        for row in weights.values():
            self.assertEqual(row["production_scoring_changed"], "false")
        for row in caps.values():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_consumer_targets_separate_green_candidates_and_hard_gates(self):
        cj = round189_target_for("K_FOOD_GLOBAL_LOCALIZATION")
        orion = round189_target_for("K_FOOD_GLOBAL_STAPLE_BRAND_SECOND_WAVE")
        single_sku = round189_target_for("K_FOOD_SINGLE_SKU_EXPORT_RISK")
        jv = round189_target_for("ECOMMERCE_RESTRUCTURING_JV_KOREA")
        data_reg = round189_target_for("RETAIL_PLATFORM_DATA_REGULATION_OVERLAY")
        mall = round189_target_for("DEPARTMENT_STORE_MALL_REDEVELOPMENT")
        convenience = round189_target_for("CONVENIENCE_STORE_PB_SSSG_KOREA")
        kbeauty = round189_target_for("K_BEAUTY_BRAND_SECOND_WAVE")
        tariff = round189_target_for("K_BEAUTY_TARIFF_IMPORT_REVIEW")
        channel = round189_target_for("CHANNEL_STUFFING_INVENTORY_OVERLAY")

        for target in (cj, orion, single_sku, jv, data_reg, mall, convenience, kbeauty, tariff, channel):
            self.assertIsNotNone(target)
        assert cj is not None
        assert orion is not None
        assert single_sku is not None
        assert jv is not None
        assert data_reg is not None
        assert mall is not None
        assert convenience is not None
        assert kbeauty is not None
        assert tariff is not None
        assert channel is not None
        self.assertEqual(cj.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("plant_utilization", cj.green_conditions)
        self.assertIn("regional_opm", orion.green_conditions)
        self.assertEqual(single_sku.score_weight.eps_fcf_opm_conversion, "cap")
        self.assertIn("gmv_recovery", jv.green_conditions)
        self.assertTrue(data_reg.hard_gate)
        self.assertIn("kftc_data_sharing_restriction", data_reg.red_flags)
        self.assertIn("capex_payback", mall.green_conditions)
        self.assertIn("sssg_growth", convenience.green_conditions)
        self.assertIn("offline_sell_through", kbeauty.green_conditions)
        self.assertEqual(tariff.score_weight.eps_fcf_opm_conversion, "cap")
        self.assertTrue(channel.hard_gate)

    def test_required_round189_cases_are_present(self):
        rows = {row["case_id"]: row for row in round189_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND189_CASE_CANDIDATES))
        self.assertEqual(rows["cj_cheiljedang_kfood_localization_stage23_case"]["target_id"], "K_FOOD_GLOBAL_LOCALIZATION")
        self.assertIn("japan_hungary_us_plant", rows["cj_cheiljedang_kfood_localization_stage23_case"]["evidence_fields"])
        self.assertEqual(rows["orion_global_staple_brand_second_wave_case"]["target_id"], "K_FOOD_GLOBAL_STAPLE_BRAND_SECOND_WAVE")
        self.assertEqual(rows["bingle_lottewellfood_single_sku_export_watch_case"]["target_id"], "K_FOOD_SINGLE_SKU_EXPORT_RISK")
        self.assertEqual(rows["emart_shinsegae_alibaba_jv_stage2_case"]["target_id"], "ECOMMERCE_RESTRUCTURING_JV_KOREA")
        self.assertIn("emart_plus_5_5pct_event_return", rows["emart_shinsegae_alibaba_jv_stage2_case"]["evidence_fields"])
        self.assertEqual(rows["kbeauty_brand_second_wave_stage23_case"]["target_id"], "K_BEAUTY_BRAND_SECOND_WAVE")
        self.assertEqual(rows["convenience_store_pb_sssg_stage23_case"]["target_id"], "CONVENIENCE_STORE_PB_SSSG_KOREA")
        self.assertEqual(rows["lotte_shopping_mall_redevelopment_stage12_case"]["target_id"], "DEPARTMENT_STORE_MALL_REDEVELOPMENT")
        self.assertEqual(rows["kbeauty_tariff_import_review_4c_watch_case"]["case_type"], "4c_thesis_break")
        self.assertEqual(rows["kbeauty_online_viral_not_sellthrough_4b_case"]["case_type"], "4b_watch")
        self.assertEqual(rows["emart_alibaba_data_regulation_4c_watch_case"]["case_type"], "4c_thesis_break")
        self.assertEqual(rows["r5_loop12_disclosure_confidence_reference_case"]["target_id"], "DISCLOSURE_CONFIDENCE_CAP")

    def test_case_records_validate_and_keep_loop12_guardrails(self):
        records = round189_case_records()

        self.assertEqual(len(records), len(ROUND189_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "CONSUMER_RETAIL_BRAND")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("stage3_early_catch_requires_5_of_8_loop12_conditions", record.green_guardrails)
            self.assertIn("kfood_kbeauty_jv_convenience_keywords_cannot_create_stage3", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["kbeauty_online_viral_not_sellthrough_4b_case"].rerating_result, "theme_overheat")
        self.assertEqual(by_id["emart_alibaba_data_regulation_4c_watch_case"].score_price_alignment, "false_positive_score")
        self.assertEqual(by_id["kbeauty_tariff_import_review_4c_watch_case"].score_price_alignment, "false_positive_score")
        self.assertEqual(by_id["cj_kfood_localization_capex_drag_case"].score_price_alignment, "evidence_good_but_price_failed")

    def test_score_profile_rows_mark_no_production_change(self):
        rows = round189_score_profile_rows()
        by_target = {row["target_id"]: row for row in rows}

        self.assertEqual(len(rows), len(ROUND189_SCORE_TARGETS))
        self.assertEqual(by_target["K_FOOD_GLOBAL_LOCALIZATION"]["eps_fcf_opm_conversion"], "24")
        self.assertEqual(by_target["K_FOOD_GLOBAL_LOCALIZATION"]["overseas_channel_localization_platform_visibility"], "22")
        self.assertEqual(by_target["K_FOOD_SINGLE_SKU_EXPORT_RISK"]["eps_fcf_opm_conversion"], "cap")
        self.assertEqual(by_target["RETAIL_PLATFORM_DATA_REGULATION_OVERLAY"]["hard_gate"], "true")
        self.assertEqual(by_target["CHANNEL_STUFFING_INVENTORY_OVERLAY"]["hard_gate"], "true")
        self.assertEqual(by_target["K_BEAUTY_TARIFF_IMPORT_REVIEW"]["eps_fcf_opm_conversion"], "cap")
        self.assertEqual(by_target["DISCLOSURE_CONFIDENCE_CAP"]["eps_fcf_opm_conversion"], "cap")
        for row in rows:
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_stage_date_price_and_alignment_rows_are_explicit(self):
        stage_rows = {row["target_id"]: row for row in round189_stage_date_rows()}
        price_fields = {row["field"] for row in round189_price_field_rows()}
        alignment_rows = {row["case_id"]: row for row in round189_score_stage_price_alignment_rows()}

        self.assertIn("plant_utilization", stage_rows["K_FOOD_GLOBAL_LOCALIZATION"]["stage3"])
        self.assertIn("regional_opm", stage_rows["K_FOOD_GLOBAL_STAPLE_BRAND_SECOND_WAVE"]["stage3"])
        self.assertIn("data_sharing_restriction", stage_rows["ECOMMERCE_RESTRUCTURING_JV_KOREA"]["stage4c"])
        self.assertIn("offline_sell_through", stage_rows["K_BEAUTY_BRAND_SECOND_WAVE"]["stage3"])
        self.assertIn("wage_rent_electricity_cost_pressure", stage_rows["CONVENIENCE_STORE_PB_SSSG_KOREA"]["stage4c"])
        for field in (
            "relative_strength_vs_kfood_basket",
            "relative_strength_vs_kbeauty_basket",
            "offline_sell_through_signal",
            "reorder_signal",
            "mainstream_shelf_signal",
            "plant_utilization",
            "capex_payback_signal",
            "jv_or_platform_event",
            "data_regulation_flag",
            "sssg",
            "pb_mix",
            "inventory_days_change",
            "receivables_days_change",
            "tariff_exposure",
            "single_sku_dependency",
        ):
            self.assertIn(field, price_fields)
        self.assertEqual(alignment_rows["emart_shinsegae_alibaba_jv_stage2_case"]["verdict"], "jv_stage2_not_green_before_monetization")
        self.assertEqual(alignment_rows["kbeauty_online_viral_not_sellthrough_4b_case"]["verdict"], "viral_without_sellthrough_requires_4b_watch")
        self.assertEqual(alignment_rows["emart_alibaba_data_regulation_4c_watch_case"]["verdict"], "data_regulation_hard_gate")

    def test_summary_and_markdown_explain_loop12(self):
        summary = round189_summary()
        summary_md = render_round189_summary_markdown()
        guardrails = render_round189_green_guardrail_markdown()
        overlays = render_round189_risk_overlay_markdown()
        price_plan = render_round189_price_validation_plan_markdown()
        alignment = render_round189_score_stage_price_alignment_markdown()

        self.assertEqual(summary["target_count"], 11)
        self.assertEqual(summary["source_canonical_target_count"], 11)
        self.assertEqual(summary["case_candidate_count"], 14)
        self.assertEqual(summary["base_score_axis_count"], 7)
        self.assertEqual(summary["stage_cap_count"], 5)
        self.assertEqual(summary["score_stage_price_alignment_count"], 14)
        self.assertEqual(summary["success_candidate_count"], 7)
        self.assertEqual(summary["event_premium_count"], 0)
        self.assertEqual(summary["failed_rerating_count"], 4)
        self.assertEqual(summary["stage4b_case_count"], 1)
        self.assertEqual(summary["stage4c_case_count"], 2)
        self.assertEqual(summary["hard_gate_target_count"], 2)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R5 Loop 12", summary_md)
        self.assertIn("production_scoring_changed: false", summary_md)
        self.assertIn("at least 5 of 8 checks", guardrails)
        self.assertIn("RETAIL_PLATFORM_DATA_REGULATION_OVERLAY", overlays)
        self.assertIn("Required Fields", price_plan)
        self.assertIn("CJ", alignment)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round189_r5_loop12_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r5_loop12_round189.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round189_r5_loop12_v12.csv",
            )

            for key in (
                "cases",
                "score_profiles",
                "summary",
                "case_matrix",
                "stage_date_plan",
                "green_guardrails",
                "risk_overlays",
                "price_validation_plan",
                "price_fields",
                "base_score_weights",
                "stage_caps",
                "score_stage_price_alignment",
                "score_stage_price_alignment_md",
            ):
                self.assertTrue(paths[key].exists(), key)
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND189_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round189_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round189_r5_loop12_consumer_retail_brand", text)


if __name__ == "__main__":
    unittest.main()
