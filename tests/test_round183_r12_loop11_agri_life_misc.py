import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round183_r12_loop11_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round183_r12_loop11_agri_life_misc import (
    ROUND183_BASE_SCORE_AXES,
    ROUND183_CASE_CANDIDATES,
    ROUND183_PRICE_FIELDS,
    ROUND183_SCORE_STAGE_PRICE_ALIGNMENT,
    ROUND183_SCORE_TARGETS,
    ROUND183_SOURCE_CANONICAL_TARGET_COUNT,
    ROUND183_SOURCE_CANONICAL_TARGET_IDS,
    ROUND183_STAGE_CAPS,
    render_round183_green_guardrail_markdown,
    render_round183_price_validation_plan_markdown,
    render_round183_risk_overlay_markdown,
    render_round183_score_stage_price_alignment_markdown,
    render_round183_summary_markdown,
    round183_base_score_axis_rows,
    round183_case_candidate_rows,
    round183_case_records,
    round183_price_field_rows,
    round183_score_profile_rows,
    round183_score_stage_price_alignment_rows,
    round183_stage_cap_rows,
    round183_stage_date_rows,
    round183_summary,
    round183_target_for,
    write_round183_r12_loop11_reports,
)


class Round183R12Loop11AgriLifeMiscTests(unittest.TestCase):
    def test_round183_targets_cover_source_archetypes(self):
        labels = {target.target_id for target in ROUND183_SCORE_TARGETS}

        self.assertEqual(ROUND183_SOURCE_CANONICAL_TARGET_COUNT, 14)
        self.assertEqual(len(labels), 14)
        self.assertEqual(set(ROUND183_SOURCE_CANONICAL_TARGET_IDS), labels)
        for target in ROUND183_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.EDUCATION_LIFE_AGRI_MISC)
            self.assertFalse(target.production_scoring_changed)

    def test_new_r12_loop11_korea_archetypes_exist(self):
        expected = (
            E2RArchetype.AGRI_MACHINERY_EXPORT_CYCLE_KOREA,
            E2RArchetype.AGRI_MACHINERY_AUTONOMOUS_ROBOT_OPTION,
            E2RArchetype.FERTILIZER_INPUT_PRICE_COST_KOREA,
            E2RArchetype.LIVESTOCK_DISEASE_PRICE_EVENT_KOREA,
            E2RArchetype.FEED_GRAIN_COST_PASS_THROUGH,
            E2RArchetype.TUNA_FISHERY_GLOBAL_BRAND_LEGAL_RISK,
            E2RArchetype.CONSUMER_REGULATED_PRODUCT_KOREA,
            E2RArchetype.HEATED_TOBACCO_GLOBAL_DISTRIBUTION,
            E2RArchetype.EDUCATION_POLICY_EVENT_KOREA,
            E2RArchetype.EDTECH_AI_DISRUPTION_KOREA,
            E2RArchetype.KIDS_IP_PLATFORM_KOREA,
            E2RArchetype.SMART_FARM_UNIT_ECONOMICS_KOREA,
            E2RArchetype.SERVICE_KIOSK_LOCAL_REGULATION_KOREA,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_loop11_base_score_axes_and_stage_caps_match_round_note(self):
        axes = {row["axis_id"]: row for row in round183_base_score_axis_rows()}
        caps = {row["stage_band"]: row for row in round183_stage_cap_rows()}

        self.assertEqual(len(ROUND183_BASE_SCORE_AXES), 7)
        self.assertEqual(axes["eps_fcf_opm_conversion"]["points"], "22")
        self.assertEqual(axes["recurring_order_regulatory_visibility"]["points"], "20")
        self.assertEqual(axes["unit_economics_pass_through_demand_durability"]["points"], "18")
        self.assertEqual(axes["price_path_early_validation"]["points"], "10")
        self.assertEqual(axes["regulation_litigation_public_health_disclosure"]["points"], "16")
        self.assertEqual(axes["capital_discipline_debt_cash_runway"]["points"], "8")
        self.assertEqual(axes["valuation_room_4b_margin"]["points"], "6")
        self.assertEqual(len(ROUND183_STAGE_CAPS), 5)
        self.assertEqual(caps["Stage 1"]["max_score"], "45")
        self.assertEqual(caps["Stage 2"]["max_score"], "70")
        self.assertIn("requires_5_of_8", caps["Stage 3"]["max_score"])
        self.assertIn("repeat_revenue_or_repeat_contract", caps["Stage 3"]["required_evidence"])
        self.assertIn("requires_3_of_5", caps["Stage 4B"]["max_score"])
        self.assertIn("public_health_regulation_tightening", caps["Stage 4C"]["required_evidence"])

    def test_target_rules_keep_event_names_from_stage3(self):
        agri = round183_target_for("AGRI_MACHINERY_EXPORT_CYCLE_KOREA")
        livestock = round183_target_for("LIVESTOCK_DISEASE_PRICE_EVENT_KOREA")
        ktng = round183_target_for("CONSUMER_REGULATED_PRODUCT_KOREA")
        heated = round183_target_for("HEATED_TOBACCO_GLOBAL_DISTRIBUTION")
        education = round183_target_for("EDUCATION_POLICY_EVENT_KOREA")
        ai_disruption = round183_target_for("EDTECH_AI_DISRUPTION_KOREA")
        kids = round183_target_for("KIDS_IP_PLATFORM_KOREA")
        disclosure = round183_target_for("DISCLOSURE_CONFIDENCE_CAP")

        for target in (agri, livestock, ktng, heated, education, ai_disruption, kids, disclosure):
            self.assertIsNotNone(target)
        assert agri is not None
        assert livestock is not None
        assert ktng is not None
        assert heated is not None
        assert education is not None
        assert ai_disruption is not None
        assert kids is not None
        assert disclosure is not None
        self.assertEqual(agri.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("dealer_inventory_stable", agri.green_conditions)
        self.assertTrue(livestock.gate_only)
        self.assertIn("disease_normalization", livestock.red_flags)
        self.assertEqual(ktng.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("public_health_gate_passed", ktng.green_conditions)
        self.assertIn("public_health_warning", heated.red_flags)
        self.assertIn("repeat_enrollment", education.green_conditions)
        self.assertTrue(ai_disruption.gate_only)
        self.assertIn("multi_ip_revenue", kids.green_conditions)
        self.assertEqual(disclosure.score_weight.eps_fcf_opm_conversion, "cap")

    def test_required_round183_cases_are_present_with_stage_markers(self):
        rows = {row["case_id"]: row for row in round183_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND183_CASE_CANDIDATES))
        self.assertEqual(rows["pinkfong_ipo_stage2_4b_watch_case"]["target_id"], "KIDS_IP_PLATFORM_KOREA")
        self.assertIn("ipo_max_plus_62pct", rows["pinkfong_ipo_stage2_4b_watch_case"]["evidence_fields"])
        self.assertEqual(rows["ktng_public_health_regulation_4c_watch_case"]["stage4c_date"], "2026-05-15")
        self.assertEqual(rows["megastudy_medical_quota_policy_event_case"]["stage1_date"], "2025-03-07")
        self.assertEqual(rows["megastudy_medical_quota_policy_event_case"]["stage4b_date"], "2025-03-07")
        self.assertEqual(rows["dongwon_starkist_settlement_legal_4c_watch_case"]["stage4c_date"], "2024-08-14")
        self.assertIn("starkist_130m_usd_burden", rows["dongwon_starkist_settlement_legal_4c_watch_case"]["evidence_fields"])
        self.assertEqual(rows["r12_disclosure_confidence_cap_case"]["target_id"], "DISCLOSURE_CONFIDENCE_CAP")

    def test_case_records_validate_and_keep_round183_guardrails(self):
        records = round183_case_records()

        self.assertEqual(len(records), len(ROUND183_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "EDUCATION_LIFE_AGRI_MISC")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("r12_theme_news_is_not_stage3_evidence_alone", record.green_guardrails)
            self.assertIn("repeat_revenue_opm_fcf_unit_economics_required", record.green_guardrails)
            self.assertIn("stage3_early_catch_requires_5_of_8_loop11_conditions", record.green_guardrails)
            self.assertIn("do_not_invent_stage_prices_mfe_mae_or_unit_economics", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["pinkfong_ipo_stage2_4b_watch_case"].score_price_alignment, "price_moved_without_evidence")
        self.assertEqual(by_id["pinkfong_ipo_stage2_4b_watch_case"].rerating_result, "theme_overheat")
        self.assertEqual(by_id["ktng_lil_heated_tobacco_distribution_case"].score_price_alignment, "unknown")
        self.assertEqual(by_id["dongwon_starkist_settlement_legal_4c_watch_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["kg_namhae_fertilizer_farmer_margin_cycle_case"].rerating_result, "cyclical_rerating")
        self.assertIn(E2RArchetype.CONSUMER_REGULATED_PRODUCT_KOREA, by_id["ktng_lil_heated_tobacco_distribution_case"].secondary_archetypes)

    def test_score_profile_rows_mark_no_production_change(self):
        rows = round183_score_profile_rows()

        self.assertEqual(len(rows), len(ROUND183_SCORE_TARGETS))
        for row in rows:
            self.assertEqual(row["large_sector"], "EDUCATION_LIFE_AGRI_MISC")
            self.assertEqual(row["production_scoring_changed"], "false")
            self.assertIn("loop11_penalty_axes", row)
        by_target = {row["target_id"]: row for row in rows}
        self.assertEqual(by_target["AGRI_MACHINERY_EXPORT_CYCLE_KOREA"]["eps_fcf_opm_conversion"], "16")
        self.assertEqual(by_target["CONSUMER_REGULATED_PRODUCT_KOREA"]["regulation_litigation_public_health_disclosure"], "18")
        self.assertEqual(by_target["KIDS_IP_PLATFORM_KOREA"]["price_path_early_validation"], "12")
        self.assertEqual(by_target["LIVESTOCK_DISEASE_PRICE_EVENT_KOREA"]["gate_only"], "true")
        self.assertEqual(by_target["EDTECH_AI_DISRUPTION_KOREA"]["gate_only"], "true")
        self.assertEqual(by_target["DISCLOSURE_CONFIDENCE_CAP"]["regulation_litigation_public_health_disclosure"], "+")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round183_stage_date_rows()}
        fields = {row["field"] for row in round183_price_field_rows()}

        self.assertIn("parts_service_repeat_revenue", rows["AGRI_MACHINERY_EXPORT_CYCLE_KOREA"]["stage3"])
        self.assertIn("disease_news_1d_20pct", rows["LIVESTOCK_DISEASE_PRICE_EVENT_KOREA"]["stage4b"])
        self.assertIn("price_fixing_settlement", rows["TUNA_FISHERY_GLOBAL_BRAND_LEGAL_RISK"]["stage4c"])
        self.assertIn("public_health_gate_passed", rows["CONSUMER_REGULATED_PRODUCT_KOREA"]["stage3"])
        self.assertIn("ai_substitutes_core_service", rows["EDTECH_AI_DISRUPTION_KOREA"]["stage4c"])
        self.assertIn("multi_ip_revenue", rows["KIDS_IP_PLATFORM_KOREA"]["stage3"])
        for field in (
            "stage1_date",
            "stage2_date",
            "stage4b_date",
            "price_at_stage2",
            "return_60d_after_stage2",
            "mfe_60d_after_stage2",
            "relative_strength_vs_agri_basket",
            "relative_strength_vs_education_basket",
            "relative_strength_vs_consumer_regulated_basket",
            "recurring_revenue_ratio",
            "dealer_inventory_signal",
            "feed_cost_signal",
            "public_health_risk_flag",
            "legal_settlement_flag",
            "policy_reversal_risk",
            "cac",
            "churn",
            "ip_revenue",
            "one_hit_dependency",
            "disclosure_confidence",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND183_PRICE_FIELDS))

    def test_score_stage_price_alignment_rows_and_markdown(self):
        rows = {row["case_id"]: row for row in round183_score_stage_price_alignment_rows()}
        markdown = render_round183_score_stage_price_alignment_markdown()

        self.assertEqual(len(rows), len(ROUND183_SCORE_STAGE_PRICE_ALIGNMENT))
        self.assertEqual(rows["pinkfong_ipo_stage2_4b_watch_case"]["verdict"], "stage2_price_path_not_green")
        self.assertEqual(rows["dongwon_starkist_settlement_legal_4c_watch_case"]["verdict"], "brand_cashflow_with_legal_4c")
        self.assertEqual(rows["megastudy_medical_quota_policy_event_case"]["verdict"], "policy_event_not_repeat_revenue")
        self.assertIn("Pinkfong", markdown)
        self.assertIn("KT&G", markdown)
        self.assertIn("Megastudy", markdown)

    def test_summary_and_markdown_explain_r12_loop11_guardrails(self):
        summary = round183_summary()
        summary_md = render_round183_summary_markdown()
        guardrails = render_round183_green_guardrail_markdown()
        overlays = render_round183_risk_overlay_markdown()
        price_plan = render_round183_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 14)
        self.assertEqual(summary["source_canonical_target_count"], 14)
        self.assertEqual(summary["case_candidate_count"], len(ROUND183_CASE_CANDIDATES))
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["case_records_are_candidate_generation_input"])
        self.assertIn("Pinkfong", summary_md)
        self.assertIn("KT&G", summary_md)
        self.assertIn("agriculture", guardrails)
        self.assertIn("public-health", overlays)
        self.assertIn("stage1_date", price_plan)
        self.assertIn("pinkfong_ipo_stage2_4b_watch_case", price_plan)

    def test_reports_are_written_and_case_jsonl_loads(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round183_r12_loop11_reports(
                output_directory=root / "reports",
                cases_path=root / "cases.jsonl",
                score_profile_path=root / "score_profiles.csv",
            )
            records = load_case_library(paths["cases"])

            self.assertEqual(len(records), len(ROUND183_CASE_CANDIDATES))
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["stage_date_plan"].exists())
            self.assertTrue(paths["price_fields"].exists())
            self.assertIn("Pinkfong", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("r12_theme_news_is_not_stage3_evidence_alone", paths["cases"].read_text(encoding="utf-8"))

    def test_cli_argument_parsing(self):
        args = build_parser().parse_args(
            [
                "--output-directory",
                "tmp_reports",
                "--cases",
                "tmp_cases.jsonl",
                "--score-profiles",
                "tmp_profiles.csv",
            ]
        )

        self.assertEqual(args.output_directory, "tmp_reports")
        self.assertEqual(args.cases, "tmp_cases.jsonl")
        self.assertEqual(args.score_profiles, "tmp_profiles.csv")

    def test_production_modules_do_not_import_round183(self):
        forbidden = "round183_r12_loop11_agri_life_misc"
        for rel_path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(rel_path).read_text(encoding="utf-8")
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
