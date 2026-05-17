import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round91_r12_loop4_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round91_r12_loop4_agri_life_misc import (
    ROUND91_CASE_CANDIDATES,
    ROUND91_PRICE_FIELDS,
    ROUND91_SCORE_TARGETS,
    render_round91_green_guardrail_markdown,
    render_round91_price_validation_plan_markdown,
    render_round91_summary_markdown,
    render_round91_unit_economics_cap_markdown,
    round91_case_candidate_rows,
    round91_case_records,
    round91_price_field_rows,
    round91_score_profile_rows,
    round91_stage_date_rows,
    round91_summary,
    target_for,
    write_round91_r12_loop4_reports,
)


class Round91R12Loop4AgriLifeMiscTests(unittest.TestCase):
    def test_round91_targets_cover_r12_loop4_archetypes_and_overlays(self):
        labels = {target.target_id for target in ROUND91_SCORE_TARGETS}

        self.assertEqual(len(labels), 21)
        for label in (
            "SMART_FARM_AGRI_TECH",
            "VERTICAL_FARMING_UNIT_ECONOMICS",
            "AGRI_MACHINERY_PRECISION_CYCLE",
            "AGRI_MACHINERY_SOFTWARE_LOCKIN",
            "AGRI_INPUT_SEED_CROP_PROTECTION",
            "FERTILIZER_INPUT_COST_CYCLE",
            "AGRI_LIVESTOCK_FOOD_COMMODITY",
            "ANIMAL_HEALTH_BIOSECURITY",
            "EDUCATION_SPECIALTY_SERVICES",
            "EDTECH_AI_DISRUPTION",
            "ONLINE_EDUCATION_OPM_DISTRESS",
            "HOME_CHILD_EDUCATION",
            "HOME_LIVING_APPLIANCE_RENTAL",
            "HOME_APPLIANCE_HARDWARE_CYCLE",
            "SERVICE_KIOSK_SELF_CHECKOUT",
            "CONSUMER_REGULATED_PRODUCT",
            "NICOTINE_ALTERNATIVE_REGULATED",
            "CANNABIS_REGULATED_PRODUCT",
            "FOOD_INPUT_REGULATED_CYCLE",
            "AGRI_DISEASE_EVENT_OVERLAY",
            "REGULATED_CONSUMER_APPROVAL_OVERLAY",
        ):
            self.assertIn(label, labels)
        for target in ROUND91_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.EDUCATION_LIFE_AGRI_MISC)
            self.assertFalse(target.production_scoring_changed)

    def test_new_round91_archetypes_exist_and_gates_are_explicit(self):
        for archetype in (
            E2RArchetype.VERTICAL_FARMING_UNIT_ECONOMICS,
            E2RArchetype.AGRI_MACHINERY_SOFTWARE_LOCKIN,
            E2RArchetype.AGRI_INPUT_SEED_CROP_PROTECTION,
            E2RArchetype.FERTILIZER_INPUT_COST_CYCLE,
            E2RArchetype.EDTECH_AI_DISRUPTION,
            E2RArchetype.ONLINE_EDUCATION_OPM_DISTRESS,
            E2RArchetype.HOME_APPLIANCE_HARDWARE_CYCLE,
            E2RArchetype.NICOTINE_ALTERNATIVE_REGULATED,
            E2RArchetype.CANNABIS_REGULATED_PRODUCT,
        ):
            self.assertIsInstance(archetype.value, str)

        edtech = target_for("EDTECH_AI_DISRUPTION")
        disease = target_for("AGRI_DISEASE_EVENT_OVERLAY")
        approval = target_for("REGULATED_CONSUMER_APPROVAL_OVERLAY")
        vertical = target_for("VERTICAL_FARMING_UNIT_ECONOMICS")
        assert edtech is not None
        assert disease is not None
        assert approval is not None
        assert vertical is not None
        for target in (edtech, disease, approval):
            self.assertTrue(target.gate_only)
            self.assertEqual(target.posture, Round10ThemePosture.REDTEAM_FIRST)
            self.assertEqual(target.score_weight.as_csv_dict()["eps_fcf"], "gate")
        self.assertFalse(vertical.gate_only)
        self.assertIn("premium_pricing_failure", vertical.stage4c_conditions)

    def test_score_profile_rows_match_round91_weight_table(self):
        rows = {row["target_id"]: row for row in round91_score_profile_rows()}

        self.assertEqual(rows["SMART_FARM_AGRI_TECH"]["eps_fcf"], "17")
        self.assertEqual(rows["VERTICAL_FARMING_UNIT_ECONOMICS"]["eps_fcf"], "8")
        self.assertEqual(rows["AGRI_MACHINERY_PRECISION_CYCLE"]["eps_fcf"], "16")
        self.assertEqual(rows["AGRI_MACHINERY_SOFTWARE_LOCKIN"]["structural_visibility"], "14")
        self.assertEqual(rows["AGRI_INPUT_SEED_CROP_PROTECTION"]["eps_fcf"], "18")
        self.assertEqual(rows["AGRI_INPUT_SEED_CROP_PROTECTION"]["structural_visibility"], "16")
        self.assertEqual(rows["FERTILIZER_INPUT_COST_CYCLE"]["bottleneck_pricing"], "14")
        self.assertEqual(rows["AGRI_LIVESTOCK_FOOD_COMMODITY"]["structural_visibility"], "8")
        self.assertEqual(rows["ANIMAL_HEALTH_BIOSECURITY"]["eps_fcf"], "18")
        self.assertEqual(rows["ANIMAL_HEALTH_BIOSECURITY"]["structural_visibility"], "16")
        self.assertEqual(rows["EDUCATION_SPECIALTY_SERVICES"]["valuation"], "10")
        self.assertEqual(rows["ONLINE_EDUCATION_OPM_DISTRESS"]["eps_fcf"], "10")
        self.assertEqual(rows["HOME_APPLIANCE_HARDWARE_CYCLE"]["eps_fcf"], "14")
        self.assertEqual(rows["SERVICE_KIOSK_SELF_CHECKOUT"]["eps_fcf"], "15")
        self.assertEqual(rows["CONSUMER_REGULATED_PRODUCT"]["structural_visibility"], "15")
        self.assertEqual(rows["NICOTINE_ALTERNATIVE_REGULATED"]["eps_fcf"], "17")
        self.assertEqual(rows["CANNABIS_REGULATED_PRODUCT"]["valuation"], "8")
        self.assertEqual(rows["EDTECH_AI_DISRUPTION"]["gate_only"], "true")
        for row in rows.values():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_required_round91_cases_are_present_with_stage_dates(self):
        rows = {row["case_id"]: row for row in round91_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND91_CASE_CANDIDATES))
        self.assertEqual(rows["john_deere_autonomous_agri_ces_case"]["stage1_date"], "2025-01-06")
        self.assertEqual(rows["deere_farm_equipment_demand_slowdown_case"]["stage4c_date"], "2025-02-13")
        self.assertEqual(rows["deere_right_to_repair_settlement_case"]["target_id"], "AGRI_MACHINERY_SOFTWARE_LOCKIN")
        self.assertEqual(rows["zoetis_bird_flu_vaccine_conditional_case"]["stage2_date"], "2025-02-14")
        self.assertEqual(rows["bayer_soy_seed_license_crop_science_case"]["stage2_date"], "2026-05-12")
        self.assertEqual(rows["bayer_soy_seed_license_crop_science_case"]["target_id"], "AGRI_INPUT_SEED_CROP_PROTECTION")
        self.assertEqual(rows["nutrien_potash_demand_cycle_case"]["target_id"], "FERTILIZER_INPUT_COST_CYCLE")
        self.assertEqual(rows["nutrien_potash_demand_cycle_case"]["case_type"], "cyclical_success")
        self.assertEqual(rows["calmaine_egg_price_regulatory_case"]["case_type"], "cyclical_success")
        self.assertEqual(rows["bowery_vertical_farming_shutdown_case"]["target_id"], "VERTICAL_FARMING_UNIT_ECONOMICS")
        self.assertEqual(rows["bowery_vertical_farming_shutdown_case"]["stage4c_date"], "2024-11-05")
        self.assertEqual(rows["appharvest_chapter11_case"]["stage4c_date"], "2023-07-24")
        self.assertEqual(rows["duolingo_ai_strategy_bookings_miss_case"]["stage4c_date"], "2026-02-26")
        self.assertEqual(rows["chegg_ai_disruption_case"]["target_id"], "EDTECH_AI_DISRUPTION")
        self.assertEqual(rows["chegg_ai_disruption_case"]["stage4c_date"], "2023-05-02")
        self.assertEqual(rows["2u_chapter11_case"]["target_id"], "ONLINE_EDUCATION_OPM_DISTRESS")
        self.assertEqual(rows["2u_chapter11_case"]["stage4c_date"], "2024-07-25")
        self.assertEqual(rows["whirlpool_dividend_suspension_case"]["stage4c_date"], "2026-05-07")
        self.assertEqual(rows["whirlpool_dividend_suspension_case"]["target_id"], "HOME_APPLIANCE_HARDWARE_CYCLE")
        self.assertEqual(rows["juul_fda_approval_case"]["stage2_date"], "2025-07-17")
        self.assertEqual(rows["fda_vape_enforcement_easing_case"]["target_id"], "NICOTINE_ALTERNATIVE_REGULATED")
        self.assertEqual(rows["who_nicotine_pouch_youth_warning_case"]["case_type"], "failed_rerating")
        self.assertEqual(rows["cannabis_schedule3_limited_case"]["target_id"], "CANNABIS_REGULATED_PRODUCT")
        self.assertEqual(rows["cannabis_schedule3_limited_case"]["stage4b_date"], "2026-05-12")

    def test_case_records_validate_and_keep_round91_guardrails(self):
        records = round91_case_records()

        self.assertEqual(len(records), len(ROUND91_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.price_validation.price_validation_status, "needs_price_backfill")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("life_essential_policy_or_disease_label_is_not_green_evidence_alone", record.green_guardrails)
            self.assertIn("repeat_contract_repeat_revenue_unit_economics_or_regulatory_scope_required", record.green_guardrails)
            self.assertIn("do_not_invent_unit_economics_orders_cac_churn_regulatory_scope_or_stage_prices", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["bayer_soy_seed_license_crop_science_case"].score_price_alignment, "aligned")
        self.assertEqual(by_id["nutrien_potash_demand_cycle_case"].rerating_result, "cyclical_rerating")
        self.assertEqual(by_id["calmaine_egg_price_regulatory_case"].rerating_result, "cyclical_rerating")
        self.assertEqual(by_id["target_self_checkout_limit_case"].rerating_result, "no_rerating")
        self.assertEqual(by_id["chegg_ai_disruption_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["fda_vape_enforcement_easing_case"].score_price_alignment, "price_moved_without_evidence")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        stage_rows = {row["target_id"]: row for row in round91_stage_date_rows()}
        price_fields = {row["field"] for row in round91_price_field_rows()}

        self.assertIn("shutdown", stage_rows["VERTICAL_FARMING_UNIT_ECONOMICS"]["stage4c"])
        self.assertIn("right_to_repair_lawsuit", stage_rows["AGRI_MACHINERY_SOFTWARE_LOCKIN"]["stage4c"])
        self.assertIn("roundup_litigation", stage_rows["AGRI_INPUT_SEED_CROP_PROTECTION"]["stage4c"])
        self.assertIn("crop_price_decline", stage_rows["FERTILIZER_INPUT_COST_CYCLE"]["stage4c"])
        self.assertIn("price_fixing_investigation", stage_rows["AGRI_LIVESTOCK_FOOD_COMMODITY"]["stage4c"])
        self.assertIn("bookings_miss", stage_rows["EDTECH_AI_DISRUPTION"]["stage4c"])
        self.assertIn("sales_authorization", stage_rows["CONSUMER_REGULATED_PRODUCT"]["stage2"])
        self.assertIn("replacement_demand_collapse", stage_rows["HOME_APPLIANCE_HARDWARE_CYCLE"]["stage4c"])
        self.assertIn("state_federal_conflict", stage_rows["CANNABIS_REGULATED_PRODUCT"]["stage4c"])
        for field in (
            "right_to_repair_flag",
            "repair_settlement_amount",
            "ftc_lawsuit_flag",
            "seed_revenue_growth",
            "crop_protection_revenue_growth",
            "licensing_revenue",
            "soy_seed_license_flag",
            "roundup_litigation_flag",
            "fertilizer_volume",
            "potash_sales_volume",
            "crop_price_change",
            "farmer_margin_indicator",
            "input_cost_spike_flag",
            "premium_pricing_success_flag",
            "shutdown_flag",
            "debt_burden_flag",
            "conditional_license_flag",
            "price_fixing_investigation_flag",
            "bookings_growth",
            "paid_conversion_rate",
            "traffic_decline_flag",
            "subscriber_decline_flag",
            "opm_model_flag",
            "partner_concentration_flag",
            "self_checkout_limit_flag",
            "employee_workload_flag",
            "fda_enforcement_easing_flag",
            "dea_registration_required_flag",
            "state_federal_conflict_flag",
            "sales_channel_authorized_flag",
            "score_price_alignment",
            "review_notes",
        ):
            self.assertIn(field, price_fields)
        self.assertEqual(len(price_fields), len(ROUND91_PRICE_FIELDS))

    def test_summary_and_markdown_explain_r12_loop4_guardrails(self):
        summary = round91_summary()
        summary_md = render_round91_summary_markdown()
        guardrails = render_round91_green_guardrail_markdown()
        caps = render_round91_unit_economics_cap_markdown()
        price_plan = render_round91_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 21)
        self.assertEqual(summary["case_candidate_count"], 19)
        self.assertEqual(summary["success_candidate_count"], 5)
        self.assertEqual(summary["cyclical_success_count"], 2)
        self.assertEqual(summary["event_premium_count"], 2)
        self.assertEqual(summary["failed_rerating_count"], 3)
        self.assertEqual(summary["stage4b_case_count"], 3)
        self.assertEqual(summary["stage4c_case_count"], 7)
        self.assertEqual(summary["green_possible_count"], 0)
        self.assertEqual(summary["watch_yellow_first_count"], 14)
        self.assertEqual(summary["redteam_first_count"], 7)
        self.assertEqual(summary["gate_only_target_count"], 3)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("Round-91", summary_md)
        self.assertIn("Do not apply these R12 Loop-4 v4 weights", guardrails)
        self.assertIn("right-to-repair", caps)
        self.assertIn("FERTILIZER_INPUT_COST_CYCLE", guardrails)
        self.assertIn("agri_input_licensed_ip_success", price_plan)
        self.assertIn("vertical_farming_4c", price_plan)
        self.assertIn("nicotine_alternative_regulatory_watch", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round91_r12_loop4_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r12_loop4_round91.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round91_r12_loop4_v4.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["stage_date_plan"].exists())
            self.assertTrue(paths["green_guardrails"].exists())
            self.assertTrue(paths["unit_economics_caps"].exists())
            self.assertTrue(paths["price_validation_plan"].exists())
            self.assertTrue(paths["price_fields"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND91_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round91_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round91_r12_loop4_agri_life_misc", text)


if __name__ == "__main__":
    unittest.main()
