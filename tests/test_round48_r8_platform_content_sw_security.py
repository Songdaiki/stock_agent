import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round48_r8_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round48_r8_platform_content_sw_security import (
    ROUND48_CASE_CANDIDATES,
    ROUND48_PRICE_FIELDS,
    ROUND48_SCORE_TARGETS,
    render_round48_green_guardrail_markdown,
    render_round48_price_validation_plan_markdown,
    render_round48_summary_markdown,
    round48_case_candidate_rows,
    round48_case_records,
    round48_price_field_rows,
    round48_score_profile_rows,
    round48_stage_date_rows,
    round48_summary,
    target_for,
    write_round48_r8_reports,
)


class Round48R8PlatformContentSWSecurityTests(unittest.TestCase):
    def test_round48_targets_cover_r8_archetypes(self):
        labels = {target.target_id for target in ROUND48_SCORE_TARGETS}

        self.assertEqual(len(labels), 12)
        self.assertIn("PLATFORM_SOFTWARE_INTERNET", labels)
        self.assertIn("CLOUD_AI_SOFTWARE_INFRA", labels)
        self.assertIn("AI_SOFTWARE_APPLICATION", labels)
        self.assertIn("GENERATIVE_AI_IP_RISK", labels)
        self.assertIn("CONTACT_CENTER_AI_AUTOMATION", labels)
        self.assertIn("SERVICE_KIOSK_SELF_CHECKOUT", labels)
        self.assertIn("GAME_CONTENT_IP", labels)
        self.assertIn("MEDIA_AD_CONTENT_CYCLE", labels)
        self.assertIn("STREAMING_AD_PLATFORM", labels)
        self.assertIn("SECURITY_IDENTITY_DEEPFAKE", labels)
        self.assertIn("METAVERSE_NFT_THEME", labels)
        self.assertIn("PLATFORM_GOVERNANCE_LEGAL_RISK", labels)
        for target in ROUND48_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY)
            self.assertFalse(target.production_scoring_changed)

    def test_new_r8_canonical_archetypes_exist(self):
        expected = {
            E2RArchetype.CLOUD_AI_SOFTWARE_INFRA,
            E2RArchetype.AI_SOFTWARE_APPLICATION,
            E2RArchetype.GENERATIVE_AI_IP_RISK,
            E2RArchetype.CONTACT_CENTER_AI_AUTOMATION,
            E2RArchetype.SERVICE_KIOSK_SELF_CHECKOUT,
            E2RArchetype.MEDIA_AD_CONTENT_CYCLE,
            E2RArchetype.STREAMING_AD_PLATFORM,
            E2RArchetype.SECURITY_IDENTITY_DEEPFAKE,
            E2RArchetype.METAVERSE_NFT_THEME,
            E2RArchetype.PLATFORM_GOVERNANCE_LEGAL_RISK,
        }

        self.assertTrue(expected.issubset(set(E2RArchetype)))

    def test_cloud_ai_is_green_possible_but_arr_and_fcf_are_required(self):
        cloud = target_for("CLOUD_AI_SOFTWARE_INFRA")

        self.assertIsNotNone(cloud)
        assert cloud is not None
        self.assertEqual(cloud.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("arr_growth", cloud.green_conditions)
        self.assertIn("fcf_conversion", cloud.green_conditions)
        self.assertIn("churn", cloud.red_flags)
        self.assertIn("ai_cost", cloud.red_flags)

    def test_ai_feature_nft_and_governance_are_not_auto_green(self):
        genai = target_for("GENERATIVE_AI_IP_RISK")
        nft = target_for("METAVERSE_NFT_THEME")
        legal = target_for("PLATFORM_GOVERNANCE_LEGAL_RISK")

        for target in (genai, nft, legal):
            self.assertIsNotNone(target)
            assert target is not None
            self.assertEqual(target.posture, Round10ThemePosture.REDTEAM_FIRST)

        assert genai is not None
        assert nft is not None
        assert legal is not None
        self.assertIn("copyright", genai.red_flags)
        self.assertIn("no_revenue", nft.red_flags)
        self.assertIn("founder_legal_case", legal.red_flags)

    def test_security_and_game_keep_operational_and_single_ip_risks(self):
        security = target_for("SECURITY_IDENTITY_DEEPFAKE")
        game = target_for("GAME_CONTENT_IP")

        self.assertIsNotNone(security)
        self.assertIsNotNone(game)
        assert security is not None
        assert game is not None
        self.assertEqual(security.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("operational_trust_intact", security.green_conditions)
        self.assertIn("outage", security.red_flags)
        self.assertEqual(game.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("bookings_growth", game.green_conditions)
        self.assertIn("single_ip", game.red_flags)

    def test_case_records_validate_and_keep_price_backfill_open(self):
        records = round48_case_records()

        self.assertEqual(len(records), len(ROUND48_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("user_count_or_ai_feature_is_not_structural_evidence_alone", record.green_guardrails)
            self.assertIn("trust_safety_legal_risk_can_block_green", record.green_guardrails)

    def test_required_round48_cases_are_present_with_stage_dates(self):
        records = {record.case_id: record for record in round48_case_records()}

        self.assertEqual(str(records["douzone_bizon_eqt_cloud_erp_case"].stage2_date), "2025-11-07")
        self.assertEqual(records["palantir_ai_platform_revenue_case"].case_type, "success_candidate")
        self.assertEqual(str(records["palantir_ai_platform_revenue_case"].stage4b_date), "2025-05-05")
        self.assertEqual(str(records["netflix_ad_tier_growth_case"].stage2_date), "2024-11-12")
        self.assertEqual(str(records["tencent_game_ai_ad_case"].stage2_date), "2026-05-13")
        self.assertIsNone(records["trade_desk_revenue_miss_case"].stage4c_date)
        self.assertEqual(str(records["crowdstrike_outage_case"].stage4c_date), "2024-07-19")
        self.assertEqual(records["kakao_founder_legal_overhang_case"].case_type, "4b_watch")
        self.assertEqual(str(records["roblox_safety_forecast_cut_case"].stage4c_date), "2026-05-01")
        self.assertEqual(str(records["take_two_gta_delay_case"].stage4c_date), "2025-11-06")
        self.assertEqual(str(records["wpp_ad_cycle_slowdown_case"].stage4c_date), "2025-06-09")
        self.assertEqual(str(records["meta_scam_ads_lawsuit_case"].stage4c_date), "2026-05-11")

    def test_score_profile_rows_mark_no_production_change(self):
        rows = {row["target_id"]: row for row in round48_score_profile_rows()}

        self.assertEqual(rows["CLOUD_AI_SOFTWARE_INFRA"]["large_sector"], "PLATFORM_CONTENT_SW_SECURITY")
        self.assertEqual(rows["CLOUD_AI_SOFTWARE_INFRA"]["production_scoring_changed"], "false")
        self.assertEqual(rows["METAVERSE_NFT_THEME"]["posture"], "REDTEAM_FIRST")
        self.assertIn("stage4c_conditions", rows["SECURITY_IDENTITY_DEEPFAKE"])

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round48_stage_date_rows()}
        fields = {row["field"] for row in round48_price_field_rows()}

        self.assertIn("GAME_CONTENT_IP", rows)
        self.assertIn("bookings_growth", rows["GAME_CONTENT_IP"]["stage2"])
        for field in (
            "stage2_price",
            "MFE_180D",
            "arr_growth",
            "net_retention_rate",
            "compute_cost_ratio",
            "copyright_lawsuit_flag",
            "bookings_growth",
            "single_ip_revenue_ratio",
            "ad_tier_users",
            "security_outage_flag",
            "renewal_rate",
            "founder_legal_case_flag",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND48_PRICE_FIELDS))

    def test_summary_and_markdown_explain_r8_guardrails(self):
        summary = round48_summary()
        summary_md = render_round48_summary_markdown()
        guardrails = render_round48_green_guardrail_markdown()
        price_plan = render_round48_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 12)
        self.assertEqual(summary["case_candidate_count"], len(ROUND48_CASE_CANDIDATES))
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("repeat-revenue and trust-risk", summary_md)
        self.assertIn("Do not apply these R8 v1.0 weights", guardrails)
        self.assertIn("user count, AI feature, new title", guardrails)
        self.assertIn("crowdstrike_outage_case", price_plan)
        self.assertIn("palantir_ai_platform_revenue_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round48_r8_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r8_round48.jsonl",
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
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND48_CASE_CANDIDATES))

    def test_case_matrix_records_are_not_production_inputs(self):
        rows = round48_case_candidate_rows()

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

    def test_production_scoring_modules_do_not_import_round48_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round48_r8_platform_content_sw_security", text)


if __name__ == "__main__":
    unittest.main()
