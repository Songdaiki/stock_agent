import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round61_r8_loop2_report import build_parser
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round61_r8_loop2_platform_content_sw_security import (
    ROUND61_CASE_CANDIDATES,
    ROUND61_PRICE_FIELDS,
    ROUND61_SCORE_TARGETS,
    render_round61_green_guardrail_markdown,
    render_round61_price_validation_plan_markdown,
    render_round61_risk_overlay_markdown,
    render_round61_summary_markdown,
    round61_case_candidate_rows,
    round61_case_records,
    round61_price_field_rows,
    round61_score_profile_rows,
    round61_stage_date_rows,
    round61_summary,
    target_for,
    write_round61_r8_loop2_reports,
)


class Round61R8Loop2PlatformContentSwSecurityTests(unittest.TestCase):
    def test_round61_targets_cover_r8_loop2_archetypes(self):
        labels = {target.target_id for target in ROUND61_SCORE_TARGETS}

        self.assertEqual(len(labels), 14)
        for label in (
            "PLATFORM_SOFTWARE_INTERNET",
            "CLOUD_AI_SOFTWARE_INFRA",
            "AI_SOFTWARE_APPLICATION",
            "GENERATIVE_AI_IP_RISK",
            "CONTACT_CENTER_AI_AUTOMATION",
            "SERVICE_KIOSK_SELF_CHECKOUT",
            "GAME_CONTENT_IP",
            "MEDIA_AD_CONTENT_CYCLE",
            "STREAMING_AD_PLATFORM",
            "SECURITY_IDENTITY_DEEPFAKE",
            "METAVERSE_NFT_THEME",
            "PLATFORM_GOVERNANCE_LEGAL_RISK",
            "OPERATIONAL_TRUST_BREAK_OVERLAY",
            "PLATFORM_AD_TRUST_OVERLAY",
        ):
            self.assertIn(label, labels)
        for target in ROUND61_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY)
            self.assertFalse(target.production_scoring_changed)

    def test_green_possible_targets_are_repeat_revenue_guardrailed(self):
        cloud = target_for("CLOUD_AI_SOFTWARE_INFRA")

        assert cloud is not None
        self.assertEqual(cloud.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("arr_growth", cloud.green_conditions)
        self.assertIn("fcf_conversion", cloud.green_conditions)
        self.assertIn("churn", cloud.red_flags)
        self.assertIn("ai_cost", cloud.loop2_penalty_axes)

    def test_ai_features_and_platform_themes_are_not_green_by_default(self):
        ai = target_for("AI_SOFTWARE_APPLICATION")
        platform = target_for("PLATFORM_SOFTWARE_INTERNET")
        game = target_for("GAME_CONTENT_IP")
        nft = target_for("METAVERSE_NFT_THEME")

        for target in (ai, platform, game):
            assert target is not None
            self.assertEqual(target.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        assert nft is not None
        self.assertEqual(nft.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("paid_usage", ai.green_conditions)
        self.assertIn("user_count_story_overpriced", platform.stage4b_conditions)
        self.assertIn("bookings_cut", game.red_flags)
        self.assertIn("revenue_absent", nft.red_flags)

    def test_overlay_targets_are_gate_only(self):
        for target_id in (
            "GENERATIVE_AI_IP_RISK",
            "PLATFORM_GOVERNANCE_LEGAL_RISK",
            "OPERATIONAL_TRUST_BREAK_OVERLAY",
            "PLATFORM_AD_TRUST_OVERLAY",
        ):
            target = target_for(target_id)
            assert target is not None
            self.assertTrue(target.gate_only)
            self.assertEqual(target.posture, Round10ThemePosture.REDTEAM_FIRST)
            self.assertEqual(target.score_weight.eps_fcf, "gate")

        trust = target_for("OPERATIONAL_TRUST_BREAK_OVERLAY")
        ad_trust = target_for("PLATFORM_AD_TRUST_OVERLAY")
        assert trust is not None
        assert ad_trust is not None
        self.assertIn("global_outage", trust.stage4c_conditions)
        self.assertIn("scam_ads", ad_trust.red_flags)

    def test_required_round61_cases_are_present_with_stage_dates(self):
        rows = {row["case_id"]: row for row in round61_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND61_CASE_CANDIDATES))
        self.assertEqual(rows["douzone_bizon_eqt_cloud_erp_case"]["stage2_date"], "2025-11-07")
        self.assertEqual(rows["palantir_q4_2025_ai_revenue_case"]["stage2_date"], "2026-02-03")
        self.assertEqual(rows["palantir_q1_2026_fastest_growth_case"]["stage4b_date"], "2026-05-05")
        self.assertEqual(rows["netflix_ad_tier_70m_case"]["stage2_date"], "2024-11-12")
        self.assertEqual(rows["netflix_ad_250m_privacy_case"]["stage4b_date"], "2026-05-01")
        self.assertEqual(rows["trade_desk_revenue_miss_case"]["stage4c_date"], "2025-02-13")
        self.assertEqual(rows["trade_desk_weak_q2_guide_case"]["stage4b_date"], "2026-05-01")
        self.assertEqual(rows["crowdstrike_outage_shareholder_case"]["stage4c_date"], "2024-07-31")
        self.assertEqual(rows["delta_crowdstrike_lawsuit_case"]["stage4c_date"], "2024-10-25")
        self.assertEqual(rows["kakao_founder_legal_overhang_case"]["stage4b_date"], "2025-08-01")
        self.assertEqual(rows["roblox_safety_forecast_cut_case"]["stage4c_date"], "2026-05-01")
        self.assertEqual(rows["take_two_gta_delay_case"]["stage4b_date"], "2025-11-01")
        self.assertEqual(rows["wpp_ad_forecast_cut_case"]["stage4b_date"], "2025-06-09")
        self.assertEqual(rows["wpp_profit_drop_ai_disruption_case"]["stage4c_date"], "2025-08-07")
        self.assertEqual(rows["meta_scam_ads_lawsuit_case"]["stage4c_date"], "2026-05-11")
        self.assertEqual(rows["meta_youth_safety_trial_case"]["stage4b_date"], "2026-05-13")

    def test_case_records_validate_and_keep_round61_guardrails(self):
        records = round61_case_records()

        self.assertEqual(len(records), len(ROUND61_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("user_count_is_not_green_evidence_alone", record.green_guardrails)
            self.assertIn("ai_feature_is_not_revenue", record.green_guardrails)
            self.assertIn("new_title_expectation_is_not_bookings", record.green_guardrails)
            self.assertIn("security_demand_is_not_operational_trust", record.green_guardrails)
            self.assertIn("ad_revenue_must_pass_quality_filter", record.green_guardrails)
            self.assertIn(
                "do_not_invent_arr_arpu_bookings_churn_fcf_customer_damage_lawsuit_or_stage_prices",
                record.green_guardrails,
            )
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["palantir_q4_2025_ai_revenue_case"].score_price_alignment, "aligned")
        self.assertEqual(by_id["crowdstrike_outage_shareholder_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["roblox_safety_forecast_cut_case"].score_price_alignment, "false_positive_score")
        self.assertEqual(by_id["palantir_q1_2026_fastest_growth_case"].rerating_result, "unknown")

    def test_score_profile_rows_match_round61_weight_table(self):
        rows = {row["target_id"]: row for row in round61_score_profile_rows()}

        self.assertEqual(rows["PLATFORM_SOFTWARE_INTERNET"]["eps_fcf"], "18")
        self.assertEqual(rows["CLOUD_AI_SOFTWARE_INFRA"]["eps_fcf"], "21")
        self.assertEqual(rows["AI_SOFTWARE_APPLICATION"]["structural_visibility"], "19")
        self.assertEqual(rows["GENERATIVE_AI_IP_RISK"]["eps_fcf"], "gate")
        self.assertEqual(rows["GAME_CONTENT_IP"]["valuation"], "11")
        self.assertEqual(rows["MEDIA_AD_CONTENT_CYCLE"]["market_mispricing"], "13")
        self.assertEqual(rows["STREAMING_AD_PLATFORM"]["structural_visibility"], "21")
        self.assertEqual(rows["METAVERSE_NFT_THEME"]["information_confidence"], "3")
        self.assertEqual(rows["PLATFORM_GOVERNANCE_LEGAL_RISK"]["gate_only"], "true")
        self.assertEqual(rows["OPERATIONAL_TRUST_BREAK_OVERLAY"]["gate_only"], "true")
        for row in rows.values():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round61_stage_date_rows()}
        fields = {row["field"] for row in round61_price_field_rows()}

        self.assertIn("arr_growth", rows["CLOUD_AI_SOFTWARE_INFRA"]["stage2"])
        self.assertIn("paid_customer_growth", rows["AI_SOFTWARE_APPLICATION"]["stage2"])
        self.assertIn("bookings_cut", rows["GAME_CONTENT_IP"]["stage4c"])
        self.assertIn("global_outage", rows["OPERATIONAL_TRUST_BREAK_OVERLAY"]["stage4c"])
        self.assertIn("consumer_protection_lawsuit", rows["PLATFORM_AD_TRUST_OVERLAY"]["stage4c"])
        for field in (
            "stage2_price",
            "below_stage2_price_flag",
            "arr_growth",
            "subscription_revenue_growth",
            "recurring_revenue_ratio",
            "churn_rate",
            "net_retention_rate",
            "ai_revenue_contribution",
            "total_contract_value",
            "rule_of_40",
            "compute_cost_ratio",
            "bookings_growth",
            "monthly_active_users",
            "game_delay_flag",
            "platform_safety_flag",
            "ad_revenue_growth",
            "ad_arpu",
            "ad_tier_users",
            "privacy_lawsuit_flag",
            "scam_ad_lawsuit_flag",
            "security_outage_flag",
            "affected_device_count",
            "customer_lawsuit_flag",
            "founder_legal_case_flag",
            "youth_safety_lawsuit_flag",
            "copyright_lawsuit_flag",
            "generative_ai_ip_risk_flag",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND61_PRICE_FIELDS))

    def test_summary_and_markdown_explain_r8_loop2_guardrails(self):
        summary = round61_summary()
        summary_md = render_round61_summary_markdown()
        guardrails = render_round61_green_guardrail_markdown()
        overlays = render_round61_risk_overlay_markdown()
        price_plan = render_round61_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 14)
        self.assertEqual(summary["case_candidate_count"], 16)
        self.assertEqual(summary["structural_success_count"], 1)
        self.assertEqual(summary["success_candidate_count"], 2)
        self.assertEqual(summary["stage4b_case_count"], 7)
        self.assertEqual(summary["stage4c_case_count"], 6)
        self.assertEqual(summary["green_possible_count"], 1)
        self.assertEqual(summary["watch_yellow_first_count"], 8)
        self.assertEqual(summary["redteam_first_count"], 5)
        self.assertEqual(summary["gate_only_target_count"], 4)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("Round 61", summary_md)
        self.assertIn("Do not apply R8 Loop-2 v2.0 weights", guardrails)
        self.assertIn("SECURITY_TRUST_BREAK", overlays)
        self.assertIn("crowdstrike_outage_shareholder_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round61_r8_loop2_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r8_loop2_round61.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round61_r8_loop2_v2.csv",
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
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND61_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round61_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round61_r8_loop2_platform_content_sw_security", text)


if __name__ == "__main__":
    unittest.main()
