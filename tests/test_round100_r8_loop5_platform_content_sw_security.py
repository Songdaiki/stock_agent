import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round100_r8_loop5_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round100_r8_loop5_platform_content_sw_security import (
    ROUND100_CASE_CANDIDATES,
    ROUND100_PRICE_FIELDS,
    ROUND100_SCORE_TARGETS,
    render_round100_green_guardrail_markdown,
    render_round100_price_validation_plan_markdown,
    render_round100_risk_overlay_markdown,
    render_round100_summary_markdown,
    round100_case_candidate_rows,
    round100_case_records,
    round100_price_field_rows,
    round100_score_profile_rows,
    round100_stage_date_rows,
    round100_summary,
    round100_target_for,
    write_round100_r8_loop5_reports,
)


class Round100R8Loop5PlatformContentSwSecurityTests(unittest.TestCase):
    def test_round100_targets_cover_r8_loop5_archetypes(self):
        labels = {target.target_id for target in ROUND100_SCORE_TARGETS}

        self.assertEqual(len(labels), 24)
        for label in (
            "PLATFORM_SOFTWARE_INTERNET",
            "B2B_SAAS_ERP_WORKFLOW",
            "ENTERPRISE_AI_ONTOLOGY_WORKFLOW",
            "CLOUD_AI_SOFTWARE_INFRA",
            "EDGE_AI_CLOUD_INFRASTRUCTURE",
            "AI_SOFTWARE_APPLICATION",
            "LEGACY_SAAS_AI_DISRUPTION_OVERLAY",
            "OBSERVABILITY_AI_OPERATIONS",
            "OBSERVABILITY_GUIDANCE_RISK",
            "CONTACT_CENTER_AI_AUTOMATION",
            "GAME_CONTENT_IP",
            "SINGLE_IP_RELEASE_EVENT_PREMIUM",
            "UGC_GAME_PLATFORM_SAFETY",
            "MEDIA_AD_CONTENT_CYCLE",
            "ADTECH_PLATFORM_PREMIUM",
            "STREAMING_AD_PLATFORM",
            "SECURITY_IDENTITY_DEEPFAKE",
            "SECURITY_OPERATIONAL_TRUST_OVERLAY",
            "PLATFORM_GOVERNANCE_LEGAL_RISK",
            "PLATFORM_AD_TRUST_OVERLAY",
            "PLATFORM_PRIVACY_YOUTH_SAFETY_OVERLAY",
            "GENERATIVE_AI_IP_RISK",
            "METAVERSE_NFT_THEME",
            "DISCLOSURE_CONFIDENCE_CAP",
        ):
            self.assertIn(label, labels)
        for target in ROUND100_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY)
            self.assertFalse(target.production_scoring_changed)
        self.assertEqual(E2RArchetype.EDGE_AI_CLOUD_INFRASTRUCTURE.value, "EDGE_AI_CLOUD_INFRASTRUCTURE")
        self.assertEqual(E2RArchetype.ENTERPRISE_AI_ONTOLOGY_WORKFLOW.value, "ENTERPRISE_AI_ONTOLOGY_WORKFLOW")
        self.assertEqual(E2RArchetype.LEGACY_SAAS_AI_DISRUPTION_OVERLAY.value, "LEGACY_SAAS_AI_DISRUPTION_OVERLAY")
        self.assertEqual(E2RArchetype.OBSERVABILITY_GUIDANCE_RISK.value, "OBSERVABILITY_GUIDANCE_RISK")
        self.assertEqual(E2RArchetype.SINGLE_IP_RELEASE_EVENT_PREMIUM.value, "SINGLE_IP_RELEASE_EVENT_PREMIUM")
        self.assertEqual(E2RArchetype.PLATFORM_PRIVACY_YOUTH_SAFETY_OVERLAY.value, "PLATFORM_PRIVACY_YOUTH_SAFETY_OVERLAY")
        self.assertEqual(E2RArchetype.DISCLOSURE_CONFIDENCE_CAP.value, "DISCLOSURE_CONFIDENCE_CAP")

    def test_green_possible_targets_are_repeat_revenue_guardrailed(self):
        b2b = round100_target_for("B2B_SAAS_ERP_WORKFLOW")
        enterprise = round100_target_for("ENTERPRISE_AI_ONTOLOGY_WORKFLOW")
        cloud = round100_target_for("CLOUD_AI_SOFTWARE_INFRA")
        edge = round100_target_for("EDGE_AI_CLOUD_INFRASTRUCTURE")

        assert b2b is not None
        assert enterprise is not None
        assert cloud is not None
        assert edge is not None
        self.assertEqual(b2b.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("arr_growth", b2b.green_conditions)
        self.assertIn("low_churn", b2b.green_conditions)
        self.assertIn("churn", b2b.red_flags)
        self.assertEqual(enterprise.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("auditable_workflow", enterprise.green_conditions)
        self.assertIn("workflow_lock_in", enterprise.stage3_conditions)
        self.assertEqual(cloud.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("paid_ai_contract", cloud.green_conditions)
        self.assertIn("ai_cost", cloud.loop5_penalty_axes)
        self.assertEqual(edge.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("long_term_ai_cloud_contract", edge.green_conditions)
        self.assertIn("capex", edge.loop5_penalty_axes)

    def test_ai_game_and_ugc_themes_are_not_green_by_default(self):
        ai = round100_target_for("AI_SOFTWARE_APPLICATION")
        game = round100_target_for("GAME_CONTENT_IP")
        single_ip = round100_target_for("SINGLE_IP_RELEASE_EVENT_PREMIUM")
        ugc = round100_target_for("UGC_GAME_PLATFORM_SAFETY")
        nft = round100_target_for("METAVERSE_NFT_THEME")

        for target in (ai, game, single_ip, ugc):
            assert target is not None
            self.assertEqual(target.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        assert nft is not None
        self.assertEqual(nft.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("paid_usage", ai.green_conditions)
        self.assertIn("booking_deferral", game.stage4c_conditions)
        assert single_ip is not None
        self.assertIn("preorder_actual", single_ip.stage2_signals)
        self.assertIn("preorder_rumor", single_ip.red_flags)
        self.assertIn("child_safety", ugc.red_flags)
        self.assertIn("revenue_absent", nft.red_flags)

    def test_overlay_targets_are_gate_only(self):
        for target_id in (
            "GENERATIVE_AI_IP_RISK",
            "LEGACY_SAAS_AI_DISRUPTION_OVERLAY",
            "OBSERVABILITY_GUIDANCE_RISK",
            "SECURITY_OPERATIONAL_TRUST_OVERLAY",
            "PLATFORM_GOVERNANCE_LEGAL_RISK",
            "PLATFORM_AD_TRUST_OVERLAY",
            "PLATFORM_PRIVACY_YOUTH_SAFETY_OVERLAY",
        ):
            target = round100_target_for(target_id)
            assert target is not None
            self.assertTrue(target.gate_only)
            self.assertEqual(target.posture, Round10ThemePosture.REDTEAM_FIRST)
            self.assertEqual(target.score_weight.eps_fcf, "gate")

        trust = round100_target_for("SECURITY_OPERATIONAL_TRUST_OVERLAY")
        ad_trust = round100_target_for("PLATFORM_AD_TRUST_OVERLAY")
        privacy = round100_target_for("PLATFORM_PRIVACY_YOUTH_SAFETY_OVERLAY")
        observability_risk = round100_target_for("OBSERVABILITY_GUIDANCE_RISK")
        legacy = round100_target_for("LEGACY_SAAS_AI_DISRUPTION_OVERLAY")
        assert trust is not None
        assert ad_trust is not None
        assert privacy is not None
        assert observability_risk is not None
        assert legacy is not None
        self.assertIn("global_outage", trust.stage4c_conditions)
        self.assertIn("scam_ads", ad_trust.red_flags)
        self.assertIn("privacy_lawsuit", privacy.red_flags)
        self.assertIn("guidance_miss", observability_risk.red_flags)
        self.assertIn("license_downsell", legacy.red_flags)

    def test_disclosure_confidence_cap_is_cap_only(self):
        cap = round100_target_for("DISCLOSURE_CONFIDENCE_CAP")

        assert cap is not None
        self.assertEqual(cap.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertFalse(cap.gate_only)
        self.assertEqual(cap.score_weight.eps_fcf, "cap")
        self.assertEqual(cap.score_weight.information_confidence, "+")
        self.assertIn("disclosure_confidence_low", cap.red_flags)

    def test_required_round100_cases_are_present_with_stage_dates(self):
        rows = {row["case_id"]: row for row in round100_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND100_CASE_CANDIDATES))
        self.assertEqual(rows["douzone_bizon_eqt_cloud_erp_case"]["target_id"], "B2B_SAAS_ERP_WORKFLOW")
        self.assertEqual(rows["douzone_bizon_eqt_cloud_erp_case"]["stage2_date"], "2025-11-07")
        self.assertEqual(rows["palantir_q4_2025_ai_revenue_case"]["target_id"], "ENTERPRISE_AI_ONTOLOGY_WORKFLOW")
        self.assertEqual(rows["palantir_q4_2025_ai_revenue_case"]["stage2_date"], "2026-02-03")
        self.assertEqual(rows["palantir_q1_2026_fastest_growth_case"]["target_id"], "ENTERPRISE_AI_ONTOLOGY_WORKFLOW")
        self.assertEqual(rows["palantir_q1_2026_fastest_growth_case"]["stage4b_date"], "2026-05-04")
        self.assertEqual(rows["akamai_frontier_model_ai_cloud_deal_case"]["target_id"], "EDGE_AI_CLOUD_INFRASTRUCTURE")
        self.assertEqual(rows["akamai_frontier_model_ai_cloud_deal_case"]["stage2_date"], "2026-05-08")
        self.assertEqual(rows["akamai_frontier_model_ai_cloud_deal_case"]["stage4b_date"], "2026-05-08")
        self.assertEqual(rows["datadog_q1_2026_ai_observability_case"]["stage2_date"], "2026-05-07")
        self.assertEqual(rows["dynatrace_q4_2026_arr_guidance_case"]["target_id"], "OBSERVABILITY_GUIDANCE_RISK")
        self.assertEqual(rows["dynatrace_q4_2026_arr_guidance_case"]["stage4c_date"], "2026-05-14")
        self.assertEqual(rows["fortinet_q1_2026_security_billings_case"]["stage2_date"], "2026-05-07")
        self.assertEqual(rows["netflix_ad_tier_250m_case"]["stage2_date"], "2026-05-13")
        self.assertEqual(rows["trade_desk_revenue_miss_case"]["target_id"], "ADTECH_PLATFORM_PREMIUM")
        self.assertEqual(rows["trade_desk_revenue_miss_case"]["stage4c_date"], "2025-02-13")
        self.assertEqual(rows["crowdstrike_outage_shareholder_case"]["target_id"], "SECURITY_OPERATIONAL_TRUST_OVERLAY")
        self.assertEqual(rows["crowdstrike_outage_shareholder_case"]["stage4c_date"], "2024-07-31")
        self.assertEqual(rows["kakao_founder_legal_overhang_case"]["stage4b_date"], "2025-10-21")
        self.assertEqual(rows["roblox_safety_forecast_cut_case"]["target_id"], "UGC_GAME_PLATFORM_SAFETY")
        self.assertEqual(rows["roblox_safety_forecast_cut_case"]["stage4c_date"], "2026-05-01")
        self.assertEqual(rows["take_two_gta_preorder_rumor_case"]["target_id"], "SINGLE_IP_RELEASE_EVENT_PREMIUM")
        self.assertEqual(rows["take_two_gta_preorder_rumor_case"]["case_type"], "event_premium")
        self.assertEqual(rows["take_two_gta_preorder_rumor_case"]["stage4b_date"], "2026-05-14")
        self.assertEqual(rows["wpp_ad_forecast_cut_case"]["stage4b_date"], "2025-06-09")
        self.assertNotIn("wpp_profit_drop_ai_disruption_case", rows)
        self.assertEqual(rows["netflix_texas_privacy_lawsuit_case"]["target_id"], "PLATFORM_PRIVACY_YOUTH_SAFETY_OVERLAY")
        self.assertEqual(rows["netflix_texas_privacy_lawsuit_case"]["stage4b_date"], "2026-05-11")
        self.assertEqual(rows["meta_scam_ads_lawsuit_case"]["stage4c_date"], "2026-05-11")
        self.assertEqual(rows["meta_youth_safety_trial_case"]["target_id"], "PLATFORM_PRIVACY_YOUTH_SAFETY_OVERLAY")
        self.assertEqual(rows["meta_youth_safety_trial_case"]["stage4b_date"], "2026-05-13")
        self.assertEqual(rows["legacy_saas_ai_disruption_case"]["target_id"], "LEGACY_SAAS_AI_DISRUPTION_OVERLAY")
        self.assertEqual(rows["legacy_saas_ai_disruption_case"]["stage4c_date"], "2026-05-14")
        self.assertEqual(rows["salesforce_agentforce_arr_case"]["target_id"], "AI_SOFTWARE_APPLICATION")
        self.assertEqual(rows["salesforce_agentforce_arr_case"]["stage2_date"], "2026-05-14")

    def test_case_records_validate_and_keep_round100_guardrails(self):
        records = round100_case_records()

        self.assertEqual(len(records), len(ROUND100_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("user_count_is_not_green_evidence_alone", record.green_guardrails)
            self.assertIn("ai_feature_is_not_revenue", record.green_guardrails)
            self.assertIn("new_title_expectation_is_not_bookings", record.green_guardrails)
            self.assertIn("security_demand_is_not_operational_trust", record.green_guardrails)
            self.assertIn("ad_revenue_must_pass_quality_filter", record.green_guardrails)
            self.assertIn("arr_arpu_bookings_opm_fcf_churn_and_legal_stability_required_for_green", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["palantir_q4_2025_ai_revenue_case"].score_price_alignment, "aligned")
        self.assertEqual(by_id["palantir_q4_2025_ai_revenue_case"].primary_archetype.value, "ENTERPRISE_AI_ONTOLOGY_WORKFLOW")
        self.assertEqual(by_id["crowdstrike_outage_shareholder_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["roblox_safety_forecast_cut_case"].score_price_alignment, "false_positive_score")
        self.assertEqual(by_id["take_two_gta_preorder_rumor_case"].rerating_result, "event_premium")
        self.assertEqual(by_id["take_two_gta_preorder_rumor_case"].primary_archetype.value, "SINGLE_IP_RELEASE_EVENT_PREMIUM")
        self.assertEqual(by_id["legacy_saas_ai_disruption_case"].primary_archetype.value, "LEGACY_SAAS_AI_DISRUPTION_OVERLAY")
        self.assertEqual(by_id["salesforce_agentforce_arr_case"].primary_archetype.value, "AI_SOFTWARE_APPLICATION")
        self.assertEqual(by_id["akamai_frontier_model_ai_cloud_deal_case"].primary_archetype.value, "EDGE_AI_CLOUD_INFRASTRUCTURE")
        self.assertEqual(by_id["dynatrace_q4_2026_arr_guidance_case"].primary_archetype.value, "OBSERVABILITY_GUIDANCE_RISK")

    def test_score_profile_rows_match_round100_weight_table(self):
        rows = {row["target_id"]: row for row in round100_score_profile_rows()}

        self.assertEqual(rows["PLATFORM_SOFTWARE_INTERNET"]["eps_fcf"], "18")
        self.assertEqual(rows["B2B_SAAS_ERP_WORKFLOW"]["structural_visibility"], "23")
        self.assertEqual(rows["ENTERPRISE_AI_ONTOLOGY_WORKFLOW"]["eps_fcf"], "23")
        self.assertEqual(rows["ENTERPRISE_AI_ONTOLOGY_WORKFLOW"]["information_confidence"], "6")
        self.assertEqual(rows["CLOUD_AI_SOFTWARE_INFRA"]["eps_fcf"], "22")
        self.assertEqual(rows["CLOUD_AI_SOFTWARE_INFRA"]["valuation"], "10")
        self.assertEqual(rows["EDGE_AI_CLOUD_INFRASTRUCTURE"]["bottleneck_pricing"], "12")
        self.assertEqual(rows["EDGE_AI_CLOUD_INFRASTRUCTURE"]["valuation"], "9")
        self.assertEqual(rows["LEGACY_SAAS_AI_DISRUPTION_OVERLAY"]["gate_only"], "true")
        self.assertEqual(rows["OBSERVABILITY_AI_OPERATIONS"]["structural_visibility"], "22")
        self.assertEqual(rows["OBSERVABILITY_AI_OPERATIONS"]["valuation"], "10")
        self.assertEqual(rows["OBSERVABILITY_GUIDANCE_RISK"]["gate_only"], "true")
        self.assertEqual(rows["SINGLE_IP_RELEASE_EVENT_PREMIUM"]["eps_fcf"], "10")
        self.assertEqual(rows["UGC_GAME_PLATFORM_SAFETY"]["valuation"], "8")
        self.assertEqual(rows["ADTECH_PLATFORM_PREMIUM"]["market_mispricing"], "14")
        self.assertEqual(rows["ADTECH_PLATFORM_PREMIUM"]["valuation"], "8")
        self.assertEqual(rows["STREAMING_AD_PLATFORM"]["valuation"], "11")
        self.assertEqual(rows["SECURITY_IDENTITY_DEEPFAKE"]["valuation"], "11")
        self.assertEqual(rows["SECURITY_OPERATIONAL_TRUST_OVERLAY"]["gate_only"], "true")
        self.assertEqual(rows["PLATFORM_AD_TRUST_OVERLAY"]["eps_fcf"], "gate")
        self.assertEqual(rows["PLATFORM_PRIVACY_YOUTH_SAFETY_OVERLAY"]["gate_only"], "true")
        self.assertEqual(rows["METAVERSE_NFT_THEME"]["information_confidence"], "3")
        self.assertEqual(rows["DISCLOSURE_CONFIDENCE_CAP"]["eps_fcf"], "cap")
        self.assertEqual(rows["DISCLOSURE_CONFIDENCE_CAP"]["information_confidence"], "+")
        self.assertEqual(rows["DISCLOSURE_CONFIDENCE_CAP"]["gate_only"], "false")
        for row in rows.values():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round100_stage_date_rows()}
        fields = {row["field"] for row in round100_price_field_rows()}

        self.assertIn("arr_growth", rows["B2B_SAAS_ERP_WORKFLOW"]["stage2"])
        self.assertIn("auditable_workflow", rows["ENTERPRISE_AI_ONTOLOGY_WORKFLOW"]["stage2"])
        self.assertIn("paid_ai_contract", rows["CLOUD_AI_SOFTWARE_INFRA"]["stage2"])
        self.assertIn("seat_churn_measured", rows["LEGACY_SAAS_AI_DISRUPTION_OVERLAY"]["stage2"])
        self.assertIn("long_term_ai_cloud_contract", rows["EDGE_AI_CLOUD_INFRASTRUCTURE"]["stage2"])
        self.assertIn("ai_monitoring_customer_growth", rows["OBSERVABILITY_AI_OPERATIONS"]["stage2"])
        self.assertIn("guidance_miss", rows["OBSERVABILITY_GUIDANCE_RISK"]["stage4c"])
        self.assertIn("preorder_actual", rows["SINGLE_IP_RELEASE_EVENT_PREMIUM"]["stage2"])
        self.assertIn("bookings_guide_cut", rows["UGC_GAME_PLATFORM_SAFETY"]["stage4c"])
        self.assertIn("revenue_miss", rows["ADTECH_PLATFORM_PREMIUM"]["stage4c"])
        self.assertIn("global_outage", rows["SECURITY_OPERATIONAL_TRUST_OVERLAY"]["stage4c"])
        self.assertIn("consumer_protection_lawsuit", rows["PLATFORM_AD_TRUST_OVERLAY"]["stage4c"])
        self.assertIn("age_verification_order", rows["PLATFORM_PRIVACY_YOUTH_SAFETY_OVERLAY"]["stage4c"])
        self.assertIn("stage3_cap_until_arr_contract_or_incident_details_verified", rows["DISCLOSURE_CONFIDENCE_CAP"]["stage3"])
        for field in (
            "stage2_price",
            "below_stage2_price_flag",
            "arr_growth",
            "net_retention_rate",
            "ai_revenue_contribution",
            "ai_arr",
            "ai_attach_rate",
            "total_contract_value",
            "revenue_per_employee",
            "government_revenue_growth",
            "commercial_revenue_growth",
            "ontology_workflow_flag",
            "seat_churn_flag",
            "license_downsell_flag",
            "gross_margin_impact_from_ai",
            "agent_cost_overrun_flag",
            "edge_cloud_contract_value",
            "edge_cloud_contract_duration_years",
            "frontier_model_customer_flag",
            "customer_disclosed_flag",
            "cloud_infrastructure_services_revenue",
            "cdn_legacy_revenue_change",
            "edge_inference_revenue_flag",
            "cloud_capex_amount",
            "ai_customer_concentration",
            "observability_revenue",
            "observability_arr",
            "ai_workload_customer_count",
            "cloud_optimization_risk_flag",
            "arr_miss_flag",
            "guidance_miss_flag",
            "net_new_arr_change",
            "bookings_growth",
            "communication_engagement_change",
            "preorder_event_flag",
            "ad_tier_users",
            "ad_growth_forecast_cut",
            "ai_production_disruption_flag",
            "dark_pattern_allegation_flag",
            "autoplay_restriction_flag",
            "security_billings_growth",
            "security_arr_growth",
            "affected_device_count",
            "customer_lawsuit_flag",
            "founder_legal_case_flag",
            "youth_safety_lawsuit_flag",
            "age_verification_order_flag",
            "algorithm_modification_order_flag",
            "addictive_design_claim_flag",
            "infinite_scroll_restriction_flag",
            "copyright_lawsuit_flag",
            "generative_ai_ip_risk_flag",
            "opendart_rcept_no",
            "opendart_detail_fetched_flag",
            "disclosure_confidence_score",
            "detail_parser_confidence",
            "disclosure_signal_class",
            "routine_disclosure_flag",
            "risk_disclosure_flag",
            "high_signal_disclosure_flag",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND100_PRICE_FIELDS))

    def test_summary_and_markdown_explain_r8_loop5_guardrails(self):
        summary = round100_summary()
        summary_md = render_round100_summary_markdown()
        guardrails = render_round100_green_guardrail_markdown()
        overlays = render_round100_risk_overlay_markdown()
        price_plan = render_round100_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 24)
        self.assertEqual(summary["case_candidate_count"], 19)
        self.assertEqual(summary["structural_success_count"], 1)
        self.assertEqual(summary["success_candidate_count"], 6)
        self.assertEqual(summary["event_premium_count"], 1)
        self.assertEqual(summary["stage4b_case_count"], 7)
        self.assertEqual(summary["stage4c_case_count"], 6)
        self.assertEqual(summary["green_possible_count"], 3)
        self.assertEqual(summary["watch_yellow_first_count"], 12)
        self.assertEqual(summary["redteam_first_count"], 9)
        self.assertEqual(summary["gate_only_target_count"], 7)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("Round 100", summary_md)
        self.assertIn("Do not apply R8 Loop-5 v5.0 weights", guardrails)
        self.assertIn("SECURITY_TRUST_BREAK", overlays)
        self.assertIn("EDGE_AI_CLOUD_CONTRACT_ALIGNED", overlays)
        self.assertIn("OBSERVABILITY_GUIDANCE_FAILED", overlays)
        self.assertIn("ENTERPRISE_AI_WORKFLOW_ALIGNED", overlays)
        self.assertIn("LEGACY_SAAS_AI_DISRUPTION", overlays)
        self.assertIn("PRIVACY_YOUTH_SAFETY_GATE", overlays)
        self.assertIn("DISCLOSURE_CONFIDENCE_CAP", overlays)
        self.assertIn("crowdstrike_outage_shareholder_case", price_plan)
        self.assertIn("salesforce_agentforce_arr_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round100_r8_loop5_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r8_loop5_round100.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round100_r8_loop5_v5.csv",
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
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND100_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round100_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round100_r8_loop5_platform_content_sw_security", text)


if __name__ == "__main__":
    unittest.main()
