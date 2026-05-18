import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round179_r8_loop11_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round179_r8_loop11_platform_content_sw_security import (
    ROUND179_BASE_SCORE_WEIGHTS,
    ROUND179_CASE_CANDIDATES,
    ROUND179_PRICE_FIELDS,
    ROUND179_SCORE_STAGE_PRICE_ALIGNMENT,
    ROUND179_SCORE_TARGETS,
    ROUND179_SOURCE_CANONICAL_TARGET_COUNT,
    ROUND179_SOURCE_CANONICAL_TARGET_IDS,
    ROUND179_STAGE_CAPS,
    render_round179_green_guardrail_markdown,
    render_round179_price_validation_plan_markdown,
    render_round179_risk_overlay_markdown,
    render_round179_score_stage_price_alignment_markdown,
    render_round179_summary_markdown,
    round179_base_score_weight_rows,
    round179_case_candidate_rows,
    round179_case_records,
    round179_price_field_rows,
    round179_score_profile_rows,
    round179_score_stage_price_alignment_rows,
    round179_stage_cap_rows,
    round179_stage_date_rows,
    round179_summary,
    round179_target_for,
    write_round179_r8_loop11_reports,
)


class Round179R8Loop11PlatformContentSwSecurityTests(unittest.TestCase):
    def test_round179_targets_cover_source_archetypes(self):
        labels = {target.target_id for target in ROUND179_SCORE_TARGETS}

        self.assertEqual(ROUND179_SOURCE_CANONICAL_TARGET_COUNT, 14)
        self.assertEqual(len(labels), 14)
        self.assertEqual(set(ROUND179_SOURCE_CANONICAL_TARGET_IDS), labels)
        for target in ROUND179_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY)
            self.assertFalse(target.production_scoring_changed)

    def test_new_r8_loop11_korea_platform_archetypes_exist(self):
        expected = (
            E2RArchetype.ENTERPRISE_AI_CLOUD_INFRA_KOREA,
            E2RArchetype.B2B_SAAS_ERP_WORKFLOW_KOREA,
            E2RArchetype.PRIVATE_EQUITY_SOFTWARE_RERATING,
            E2RArchetype.AI_CLOUD_CAPITAL_ALLOCATION,
            E2RArchetype.SOVEREIGN_KOREAN_AI_MODEL,
            E2RArchetype.WEBTOON_PLATFORM_IP_MONETIZATION,
            E2RArchetype.PLATFORM_PRIVACY_SECURITY_OVERLAY,
            E2RArchetype.GAME_CONTENT_IP_REPEAT_MONETIZATION,
            E2RArchetype.GAME_SINGLE_IP_EVENT_PREMIUM,
            E2RArchetype.GAME_IP_LAUNCH_DELAY_LEGAL_RISK,
            E2RArchetype.KPOP_PLATFORM_CONTENT_IP,
            E2RArchetype.ENTERTAINMENT_GOVERNANCE_LEGAL_OVERLAY,
            E2RArchetype.AD_CONTENT_PLATFORM_GUIDANCE_RISK,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_loop11_base_score_weights_and_stage_caps_match_round_note(self):
        weights = {row["component"]: row for row in round179_base_score_weight_rows()}
        caps = {row["stage_band"]: row for row in round179_stage_cap_rows()}

        self.assertEqual(len(ROUND179_BASE_SCORE_WEIGHTS), 7)
        self.assertEqual(weights["arr_bookings_ad_ip_cloud_revenue"]["points"], "24")
        self.assertEqual(weights["recurrence_retention_workflow_lockin"]["points"], "18")
        self.assertEqual(weights["opm_fcf_gross_margin_conversion"]["points"], "14")
        self.assertEqual(weights["ai_cloud_platform_ip_bottleneck"]["points"], "12")
        self.assertEqual(weights["early_price_path_validation"]["points"], "10")
        self.assertEqual(weights["operational_trust_security_legal_governance"]["points"], "14")
        self.assertEqual(weights["valuation_room_4b_runway"]["points"], "8")
        self.assertEqual(len(ROUND179_STAGE_CAPS), 5)
        self.assertEqual(caps["Stage 1"]["max_score"], "45")
        self.assertEqual(caps["Stage 2"]["max_score"], "70")
        self.assertIn("requires_5_of_8", caps["Stage 3"]["max_score"])
        self.assertIn("arr_bookings_cloud_ip_or_ad_revenue_grows", caps["Stage 3"]["required_evidence"])
        self.assertIn("requires_3_of_5", caps["Stage 4B"]["max_score"])
        self.assertIn("security_incident_or_data_leak", caps["Stage 4C"]["required_evidence"])

    def test_target_rules_separate_repeat_revenue_from_headline(self):
        sds = round179_target_for("ENTERPRISE_AI_CLOUD_INFRA_KOREA")
        douzone = round179_target_for("B2B_SAAS_ERP_WORKFLOW_KOREA")
        pe = round179_target_for("PRIVATE_EQUITY_SOFTWARE_RERATING")
        capital = round179_target_for("AI_CLOUD_CAPITAL_ALLOCATION")
        naver_ai = round179_target_for("SOVEREIGN_KOREAN_AI_MODEL")
        webtoon = round179_target_for("WEBTOON_PLATFORM_IP_MONETIZATION")
        privacy = round179_target_for("PLATFORM_PRIVACY_SECURITY_OVERLAY")
        game = round179_target_for("GAME_CONTENT_IP_REPEAT_MONETIZATION")
        single_ip = round179_target_for("GAME_SINGLE_IP_EVENT_PREMIUM")
        launch_risk = round179_target_for("GAME_IP_LAUNCH_DELAY_LEGAL_RISK")
        kpop = round179_target_for("KPOP_PLATFORM_CONTENT_IP")
        legal = round179_target_for("ENTERTAINMENT_GOVERNANCE_LEGAL_OVERLAY")
        guidance = round179_target_for("AD_CONTENT_PLATFORM_GUIDANCE_RISK")
        disclosure = round179_target_for("DISCLOSURE_CONFIDENCE_CAP")

        for target in (sds, douzone, pe, capital, naver_ai, webtoon, privacy, game, single_ip, launch_risk, kpop, legal, guidance, disclosure):
            self.assertIsNotNone(target)
        assert sds is not None
        assert douzone is not None
        assert pe is not None
        assert capital is not None
        assert naver_ai is not None
        assert webtoon is not None
        assert privacy is not None
        assert game is not None
        assert single_ip is not None
        assert launch_risk is not None
        assert kpop is not None
        assert legal is not None
        assert guidance is not None
        assert disclosure is not None
        self.assertEqual(sds.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("ai_cloud_revenue", sds.green_conditions)
        self.assertEqual(douzone.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("arr_growth", douzone.green_conditions)
        self.assertEqual(pe.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertTrue(capital.gate_only)
        self.assertIn("b2b_paid_api", naver_ai.green_conditions)
        self.assertIn("guidance_miss", webtoon.stage4c_conditions)
        self.assertTrue(privacy.gate_only)
        self.assertEqual(game.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("live_service_bookings", game.green_conditions)
        self.assertEqual(single_ip.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertTrue(launch_risk.gate_only)
        self.assertIn("fan_platform_arpu", kpop.green_conditions)
        self.assertTrue(legal.gate_only)
        self.assertTrue(guidance.gate_only)
        self.assertEqual(disclosure.score_weight.arr_bookings_ad_ip_cloud_revenue, "cap")

    def test_required_round179_cases_are_present_with_stage_markers(self):
        rows = {row["case_id"]: row for row in round179_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND179_CASE_CANDIDATES))
        self.assertEqual(rows["samsung_sds_ai_cloud_kkr_cb_stage2_4b_watch_case"]["stage2_date"], "2026-04-15")
        self.assertEqual(rows["samsung_sds_ai_cloud_kkr_cb_stage2_4b_watch_case"]["stage4b_date"], "2026-04-15")
        self.assertIn("share_price_20_8pct_jump", rows["samsung_sds_ai_cloud_kkr_cb_stage2_4b_watch_case"]["evidence_fields"])
        self.assertEqual(rows["douzone_bizon_eqt_erp_workflow_stage2_3_case"]["stage2_date"], "2025-11-07")
        self.assertEqual(rows["naver_hyperclova_x_sovereign_ai_stage1_2_case"]["target_id"], "SOVEREIGN_KOREAN_AI_MODEL")
        self.assertEqual(rows["shiftup_game_ip_repeat_monetization_4b_watch_case"]["target_id"], "GAME_CONTENT_IP_REPEAT_MONETIZATION")
        self.assertEqual(rows["krafton_pubg_bgmi_india_inzoi_stage2_3_4c_watch_case"]["stage2_date"], "2025-12-19")
        self.assertEqual(rows["sm_tencent_music_china_reopening_kpop_stage2_case"]["stage2_date"], "2025-05-27")
        self.assertEqual(rows["hybe_founder_legal_risk_kpop_cap_case"]["stage4c_date"], "2026-04-21")
        self.assertEqual(rows["webtoon_ipo_guidance_miss_4c_watch_case"]["stage2_date"], "2024-06-27")
        self.assertEqual(rows["webtoon_ipo_guidance_miss_4c_watch_case"]["stage4c_date"], "2026-05-01")
        self.assertEqual(rows["naver_line_privacy_security_governance_4c_watch_case"]["stage4c_date"], "2024-08-02")
        self.assertEqual(rows["kakao_founder_legal_overhang_relief_case"]["stage4b_date"], "2025-10-21")
        self.assertEqual(rows["krafton_subnautica2_delay_lawsuit_4c_watch_case"]["target_id"], "GAME_IP_LAUNCH_DELAY_LEGAL_RISK")
        self.assertEqual(rows["r8_disclosure_confidence_cap_case"]["target_id"], "DISCLOSURE_CONFIDENCE_CAP")

    def test_case_records_validate_and_keep_round179_guardrails(self):
        records = round179_case_records()

        self.assertEqual(len(records), len(ROUND179_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "PLATFORM_CONTENT_SW_SECURITY")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("ai_ip_mau_ipo_or_kpop_headline_is_not_stage3", record.green_guardrails)
            self.assertIn("require_arr_bookings_ad_ip_cloud_revenue_opm_fcf_retention_and_trust_for_green", record.green_guardrails)
            self.assertIn("stage3_early_catch_requires_5_of_8_loop11_conditions", record.green_guardrails)
            self.assertIn("do_not_invent_arr_bookings_cloud_revenue_ad_revenue_ip_revenue_opm_fcf_retention_stage_prices_or_mfe_mae", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["samsung_sds_ai_cloud_kkr_cb_stage2_4b_watch_case"].score_price_alignment, "price_moved_without_evidence")
        self.assertIn(E2RArchetype.AI_CLOUD_CAPITAL_ALLOCATION, by_id["samsung_sds_ai_cloud_kkr_cb_stage2_4b_watch_case"].secondary_archetypes)
        self.assertIn("arr_growth", by_id["douzone_bizon_eqt_erp_workflow_stage2_3_case"].must_have_fields)
        self.assertEqual(by_id["hybe_founder_legal_risk_kpop_cap_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["naver_hyperclova_x_sovereign_ai_stage1_2_case"].rerating_result, "event_premium")
        self.assertEqual(by_id["r8_disclosure_confidence_cap_case"].score_price_alignment, "evidence_good_but_price_failed")

    def test_score_profile_rows_mark_no_production_change(self):
        rows = round179_score_profile_rows()

        self.assertEqual(len(rows), len(ROUND179_SCORE_TARGETS))
        for row in rows:
            self.assertEqual(row["large_sector"], "PLATFORM_CONTENT_SW_SECURITY")
            self.assertEqual(row["production_scoring_changed"], "false")
            self.assertIn("loop11_penalty_axes", row)
        by_target = {row["target_id"]: row for row in rows}
        self.assertEqual(by_target["ENTERPRISE_AI_CLOUD_INFRA_KOREA"]["arr_bookings_ad_ip_cloud_revenue"], "20")
        self.assertEqual(by_target["B2B_SAAS_ERP_WORKFLOW_KOREA"]["posture"], Round10ThemePosture.GREEN_POSSIBLE.value)
        self.assertEqual(by_target["AI_CLOUD_CAPITAL_ALLOCATION"]["gate_only"], "true")
        self.assertEqual(by_target["SOVEREIGN_KOREAN_AI_MODEL"]["ai_cloud_platform_ip_bottleneck"], "22")
        self.assertEqual(by_target["PLATFORM_PRIVACY_SECURITY_OVERLAY"]["arr_bookings_ad_ip_cloud_revenue"], "gate")
        self.assertEqual(by_target["DISCLOSURE_CONFIDENCE_CAP"]["arr_bookings_ad_ip_cloud_revenue"], "cap")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round179_stage_date_rows()}
        fields = {row["field"] for row in round179_price_field_rows()}

        self.assertIn("ai_cloud_revenue", rows["ENTERPRISE_AI_CLOUD_INFRA_KOREA"]["stage3"])
        self.assertIn("arr_growth", rows["B2B_SAAS_ERP_WORKFLOW_KOREA"]["stage3"])
        self.assertIn("guidance_miss", rows["WEBTOON_PLATFORM_IP_MONETIZATION"]["stage4c"])
        self.assertIn("release_delay", rows["GAME_IP_LAUNCH_DELAY_LEGAL_RISK"]["stage4c"])
        self.assertIn("founder_legal_risk", rows["ENTERTAINMENT_GOVERNANCE_LEGAL_OVERLAY"]["stage4c"])
        for field in (
            "return_20d_after_stage2",
            "return_60d_after_stage2",
            "return_120d_after_stage2",
            "return_252d_after_stage2",
            "mfe_60d_after_stage2",
            "mfe_120d_after_stage2",
            "relative_strength_vs_software_basket",
            "relative_strength_vs_game_basket",
            "arr",
            "arr_growth_yoy",
            "bookings",
            "bookings_growth_yoy",
            "cloud_revenue",
            "ad_revenue",
            "ip_adaptation_revenue",
            "paid_content_revenue",
            "live_service_revenue",
            "fan_platform_arpu",
            "opm",
            "fcf",
            "churn",
            "retention",
            "renewal_rate",
            "strategic_investor",
            "cb_or_dilution_flag",
            "guidance_miss_flag",
            "release_delay_flag",
            "lawsuit_flag",
            "privacy_security_incident_flag",
            "founder_legal_risk_flag",
            "regulatory_pressure_flag",
        ):
            self.assertIn(field, fields)

    def test_score_stage_price_alignment_rows_and_markdown(self):
        rows = {row["case_id"]: row for row in round179_score_stage_price_alignment_rows()}
        markdown = render_round179_score_stage_price_alignment_markdown()

        self.assertEqual(len(rows), len(ROUND179_SCORE_STAGE_PRICE_ALIGNMENT))
        self.assertEqual(rows["samsung_sds_ai_cloud_kkr_cb_stage2_4b_watch_case"]["verdict"], "ai_cloud_cb_stage2_not_green")
        self.assertEqual(rows["douzone_bizon_eqt_erp_workflow_stage2_3_case"]["verdict"], "erp_workflow_requires_arr_churn_opm")
        self.assertEqual(rows["webtoon_ipo_guidance_miss_4c_watch_case"]["verdict"], "webtoon_guidance_miss_blocks_green")
        self.assertEqual(rows["naver_line_privacy_security_governance_4c_watch_case"]["verdict"], "privacy_security_governance_gate")
        self.assertIn("Samsung", markdown)
        self.assertIn("Webtoon", markdown)
        self.assertIn("privacy", markdown)

    def test_summary_and_markdown_explain_r8_loop11_guardrails(self):
        summary = round179_summary()
        summary_md = render_round179_summary_markdown()
        guardrails = render_round179_green_guardrail_markdown()
        overlays = render_round179_risk_overlay_markdown()
        price_plan = render_round179_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 14)
        self.assertEqual(summary["source_canonical_target_count"], 14)
        self.assertEqual(summary["case_candidate_count"], len(ROUND179_CASE_CANDIDATES))
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["case_records_are_candidate_generation_input"])
        self.assertIn("AI/cloud/IP/platform", summary_md)
        self.assertIn("AI feature", guardrails)
        self.assertIn("Webtoon", overlays)
        self.assertIn("ARR", price_plan)
        self.assertIn("samsung_sds_ai_cloud_kkr_cb_stage2_4b_watch_case", price_plan)

    def test_reports_are_written_and_case_jsonl_loads(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round179_r8_loop11_reports(
                output_directory=root / "reports",
                cases_path=root / "cases.jsonl",
                score_profile_path=root / "score_profiles.csv",
            )
            records = load_case_library(paths["cases"])

            self.assertEqual(len(records), len(ROUND179_CASE_CANDIDATES))
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["stage_date_plan"].exists())
            self.assertTrue(paths["price_fields"].exists())
            self.assertIn("Samsung", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("ai_ip_mau_ipo_or_kpop_headline_is_not_stage3", paths["cases"].read_text(encoding="utf-8"))

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

    def test_production_modules_do_not_import_round179(self):
        forbidden = "round179_r8_loop11_platform_content_sw_security"
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
