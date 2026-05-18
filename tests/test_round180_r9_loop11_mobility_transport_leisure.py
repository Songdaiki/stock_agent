import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round180_r9_loop11_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round180_r9_loop11_mobility_transport_leisure import (
    ROUND180_BASE_SCORE_WEIGHTS,
    ROUND180_CASE_CANDIDATES,
    ROUND180_PRICE_FIELDS,
    ROUND180_SCORE_STAGE_PRICE_ALIGNMENT,
    ROUND180_SCORE_TARGETS,
    ROUND180_SOURCE_CANONICAL_TARGET_COUNT,
    ROUND180_SOURCE_CANONICAL_TARGET_IDS,
    ROUND180_STAGE_CAPS,
    render_round180_green_guardrail_markdown,
    render_round180_price_validation_plan_markdown,
    render_round180_risk_overlay_markdown,
    render_round180_score_stage_price_alignment_markdown,
    render_round180_summary_markdown,
    round180_base_score_weight_rows,
    round180_case_candidate_rows,
    round180_case_records,
    round180_price_field_rows,
    round180_score_profile_rows,
    round180_score_stage_price_alignment_rows,
    round180_stage_cap_rows,
    round180_stage_date_rows,
    round180_summary,
    round180_target_for,
    write_round180_r9_loop11_reports,
)


class Round180R9Loop11MobilityTransportLeisureTests(unittest.TestCase):
    def test_round180_targets_cover_source_archetypes(self):
        labels = {target.target_id for target in ROUND180_SCORE_TARGETS}

        self.assertEqual(ROUND180_SOURCE_CANONICAL_TARGET_COUNT, 14)
        self.assertEqual(len(labels), 14)
        self.assertEqual(set(ROUND180_SOURCE_CANONICAL_TARGET_IDS), labels)
        for target in ROUND180_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.MOBILITY_TRANSPORT_LEISURE)
            self.assertFalse(target.production_scoring_changed)

    def test_new_r9_loop11_korea_mobility_archetypes_exist(self):
        expected = (
            E2RArchetype.AUTO_HYBRID_LOCALIZATION_KOREA,
            E2RArchetype.AUTO_SDV_DELAY_CAPEX_OVERLAY,
            E2RArchetype.AUTO_PRICE_WAR_EUROPE_OVERLAY,
            E2RArchetype.AUTO_COMPONENT_RESTRUCTURING_KOREA,
            E2RArchetype.AUTO_COMPONENT_QUALITY_RECALL_OVERLAY,
            E2RArchetype.ECOMMERCE_LOGISTICS_REPEAT_CONTRACT,
            E2RArchetype.LOGISTICS_LABOR_REGULATION_OVERLAY,
            E2RArchetype.CASINO_DUTYFREE_TOURISM_POLICY_KOREA,
            E2RArchetype.CASINO_RETURN_VISITOR_UNIT_ECONOMICS,
            E2RArchetype.AIRLINE_SAFETY_REGULATORY_OVERLAY,
            E2RArchetype.SHIPPING_FREIGHT_CYCLE_KOREA,
            E2RArchetype.PARCEL_VOLUME_PRICE_COST_SPREAD,
            E2RArchetype.TRAVEL_AGENCY_POLICY_EVENT,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_loop11_base_score_weights_and_stage_caps_match_round_note(self):
        weights = {row["component"]: row for row in round180_base_score_weight_rows()}
        caps = {row["stage_band"]: row for row in round180_stage_cap_rows()}

        self.assertEqual(len(ROUND180_BASE_SCORE_WEIGHTS), 7)
        self.assertEqual(weights["eps_fcf_opm_conversion"]["points"], "22")
        self.assertEqual(weights["contract_volume_operating_visibility"]["points"], "18")
        self.assertEqual(weights["unit_fleet_economics"]["points"], "18")
        self.assertEqual(weights["safety_regulation_labor_quality_risk"]["points"], "14")
        self.assertEqual(weights["early_price_path_validation"]["points"], "10")
        self.assertEqual(weights["recurrence_demand_durability"]["points"], "10")
        self.assertEqual(weights["valuation_room_4b_runway"]["points"], "8")
        self.assertEqual(len(ROUND180_STAGE_CAPS), 5)
        self.assertEqual(caps["Stage 1"]["max_score"], "45")
        self.assertEqual(caps["Stage 2"]["max_score"], "70")
        self.assertIn("requires_5_of_8", caps["Stage 3"]["max_score"])
        self.assertIn("opm_fcf_improves", caps["Stage 3"]["required_evidence"])
        self.assertIn("requires_3_of_5", caps["Stage 4B"]["max_score"])
        self.assertIn("airline_or_large_safety_accident", caps["Stage 4C"]["required_evidence"])

    def test_target_rules_separate_unit_economics_from_headline(self):
        kia = round180_target_for("AUTO_HYBRID_LOCALIZATION_KOREA")
        sdv = round180_target_for("AUTO_SDV_DELAY_CAPEX_OVERLAY")
        price_war = round180_target_for("AUTO_PRICE_WAR_EUROPE_OVERLAY")
        mobis = round180_target_for("AUTO_COMPONENT_RESTRUCTURING_KOREA")
        recall = round180_target_for("AUTO_COMPONENT_QUALITY_RECALL_OVERLAY")
        logistics = round180_target_for("ECOMMERCE_LOGISTICS_REPEAT_CONTRACT")
        labor = round180_target_for("LOGISTICS_LABOR_REGULATION_OVERLAY")
        tourism = round180_target_for("CASINO_DUTYFREE_TOURISM_POLICY_KOREA")
        casino = round180_target_for("CASINO_RETURN_VISITOR_UNIT_ECONOMICS")
        airline = round180_target_for("AIRLINE_SAFETY_REGULATORY_OVERLAY")
        shipping = round180_target_for("SHIPPING_FREIGHT_CYCLE_KOREA")
        parcel = round180_target_for("PARCEL_VOLUME_PRICE_COST_SPREAD")
        travel = round180_target_for("TRAVEL_AGENCY_POLICY_EVENT")
        disclosure = round180_target_for("DISCLOSURE_CONFIDENCE_CAP")

        for target in (kia, sdv, price_war, mobis, recall, logistics, labor, tourism, casino, airline, shipping, parcel, travel, disclosure):
            self.assertIsNotNone(target)
        assert kia is not None
        assert sdv is not None
        assert price_war is not None
        assert mobis is not None
        assert recall is not None
        assert logistics is not None
        assert labor is not None
        assert tourism is not None
        assert casino is not None
        assert airline is not None
        assert shipping is not None
        assert parcel is not None
        assert travel is not None
        assert disclosure is not None
        self.assertEqual(kia.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("opm_defense", kia.green_conditions)
        self.assertTrue(sdv.gate_only)
        self.assertTrue(price_war.gate_only)
        self.assertEqual(mobis.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertTrue(recall.gate_only)
        self.assertEqual(logistics.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertTrue(labor.gate_only)
        self.assertEqual(tourism.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertEqual(casino.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertTrue(airline.gate_only)
        self.assertEqual(shipping.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertEqual(parcel.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(travel.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertEqual(disclosure.score_weight.eps_fcf_opm_conversion, "cap")
        self.assertIn("casino_drop_amount", casino.green_conditions)
        self.assertIn("freight_rate_decline", shipping.red_flags)
        self.assertIn("labor_regulation_cost", parcel.red_flags)

    def test_required_round180_cases_are_present_with_stage_markers(self):
        rows = {row["case_id"]: row for row in round180_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND180_CASE_CANDIDATES))
        self.assertEqual(rows["kia_hybrid_localization_sdv_delay_stage2_4c_watch_case"]["target_id"], "AUTO_HYBRID_LOCALIZATION_KOREA")
        self.assertEqual(rows["kia_hybrid_localization_sdv_delay_stage2_4c_watch_case"]["stage2_date"], "2025-03-28")
        self.assertEqual(rows["kia_hybrid_localization_sdv_delay_stage2_4c_watch_case"]["stage4c_date"], "2026-04-09")
        self.assertIn("georgia_hybrid_production", rows["kia_hybrid_localization_sdv_delay_stage2_4c_watch_case"]["evidence_fields"])
        self.assertEqual(rows["hyundai_mobis_lighting_restructuring_quality_recall_case"]["target_id"], "AUTO_COMPONENT_RESTRUCTURING_KOREA")
        self.assertEqual(rows["hyundai_mobis_lighting_restructuring_quality_recall_case"]["stage2_date"], "2026-01-27")
        self.assertEqual(rows["cj_logistics_shinsegae_oneday_volume_stage2_3_case"]["target_id"], "ECOMMERCE_LOGISTICS_REPEAT_CONTRACT")
        self.assertIn("one_day_overnight_volume_120pct_growth", rows["cj_logistics_shinsegae_oneday_volume_stage2_3_case"]["evidence_fields"])
        self.assertEqual(rows["tourism_visa_free_dutyfree_casino_policy_event_case"]["stage1_date"], "2025-08-06")
        self.assertEqual(rows["tourism_visa_free_dutyfree_casino_policy_event_case"]["stage2_date"], "2025-09-29")
        self.assertEqual(rows["casino_return_visitor_unit_economics_gate_case"]["target_id"], "CASINO_RETURN_VISITOR_UNIT_ECONOMICS")
        self.assertEqual(rows["jeju_air_muan_crash_hard_4c_case"]["target_id"], "AIRLINE_SAFETY_REGULATORY_OVERLAY")
        self.assertEqual(rows["jeju_air_muan_crash_hard_4c_case"]["stage4c_date"], "2024-12-30")
        self.assertEqual(rows["hmm_pan_ocean_freight_cycle_4b_4c_watch_case"]["target_id"], "SHIPPING_FREIGHT_CYCLE_KOREA")
        self.assertEqual(rows["kia_sdv_delay_capex_price_war_overlay_case"]["target_id"], "AUTO_SDV_DELAY_CAPEX_OVERLAY")
        self.assertEqual(rows["hyundai_mobis_iccu_quality_recall_overlay_case"]["target_id"], "AUTO_COMPONENT_QUALITY_RECALL_OVERLAY")
        self.assertEqual(rows["cj_logistics_labor_regulation_margin_cap_case"]["target_id"], "LOGISTICS_LABOR_REGULATION_OVERLAY")
        self.assertEqual(rows["travel_agency_policy_event_stage1_2_case"]["target_id"], "TRAVEL_AGENCY_POLICY_EVENT")
        self.assertEqual(rows["r9_disclosure_confidence_cap_case"]["target_id"], "DISCLOSURE_CONFIDENCE_CAP")

    def test_case_records_validate_and_keep_round180_guardrails(self):
        records = round180_case_records()

        self.assertEqual(len(records), len(ROUND180_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "MOBILITY_TRANSPORT_LEISURE")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("mobility_tourism_freight_hybrid_headline_is_not_stage3", record.green_guardrails)
            self.assertIn("require_opm_fcf_unit_economics_repeat_contract_or_repeat_demand_for_green", record.green_guardrails)
            self.assertIn("stage3_early_catch_requires_5_of_8_loop11_conditions", record.green_guardrails)
            self.assertIn("do_not_invent_contract_amount_freight_rate_casino_drop_opm_unit_economics_stage_prices_or_mfe_mae", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertIn(E2RArchetype.AUTO_SDV_DELAY_CAPEX_OVERLAY, by_id["kia_hybrid_localization_sdv_delay_stage2_4c_watch_case"].secondary_archetypes)
        self.assertIn("opm_defense", by_id["kia_hybrid_localization_sdv_delay_stage2_4c_watch_case"].must_have_fields)
        self.assertEqual(by_id["tourism_visa_free_dutyfree_casino_policy_event_case"].score_price_alignment, "price_moved_without_evidence")
        self.assertEqual(by_id["jeju_air_muan_crash_hard_4c_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["hmm_pan_ocean_freight_cycle_4b_4c_watch_case"].rerating_result, "cyclical_rerating")
        self.assertEqual(by_id["r9_disclosure_confidence_cap_case"].score_price_alignment, "evidence_good_but_price_failed")

    def test_score_profile_rows_mark_no_production_change(self):
        rows = round180_score_profile_rows()

        self.assertEqual(len(rows), len(ROUND180_SCORE_TARGETS))
        for row in rows:
            self.assertEqual(row["large_sector"], "MOBILITY_TRANSPORT_LEISURE")
            self.assertEqual(row["production_scoring_changed"], "false")
            self.assertIn("loop11_penalty_axes", row)
        by_target = {row["target_id"]: row for row in rows}
        self.assertEqual(by_target["AUTO_HYBRID_LOCALIZATION_KOREA"]["eps_fcf_opm_conversion"], "20")
        self.assertEqual(by_target["ECOMMERCE_LOGISTICS_REPEAT_CONTRACT"]["posture"], Round10ThemePosture.GREEN_POSSIBLE.value)
        self.assertEqual(by_target["AUTO_SDV_DELAY_CAPEX_OVERLAY"]["gate_only"], "true")
        self.assertEqual(by_target["CASINO_RETURN_VISITOR_UNIT_ECONOMICS"]["unit_fleet_economics"], "22")
        self.assertEqual(by_target["AIRLINE_SAFETY_REGULATORY_OVERLAY"]["eps_fcf_opm_conversion"], "gate")
        self.assertEqual(by_target["DISCLOSURE_CONFIDENCE_CAP"]["eps_fcf_opm_conversion"], "cap")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round180_stage_date_rows()}
        fields = {row["field"] for row in round180_price_field_rows()}

        self.assertIn("opm_defense", rows["AUTO_HYBRID_LOCALIZATION_KOREA"]["stage3"])
        self.assertIn("sdv_delay", rows["AUTO_SDV_DELAY_CAPEX_OVERLAY"]["stage4c"])
        self.assertIn("opm_fcf_improvement", rows["ECOMMERCE_LOGISTICS_REPEAT_CONTRACT"]["stage3"])
        self.assertIn("casino_drop_amount", rows["CASINO_RETURN_VISITOR_UNIT_ECONOMICS"]["stage3"])
        self.assertIn("fatal_accident", rows["AIRLINE_SAFETY_REGULATORY_OVERLAY"]["stage4c"])
        self.assertIn("freight_rate_decline", rows["SHIPPING_FREIGHT_CYCLE_KOREA"]["stage4c"])
        for field in (
            "return_1d_after_event",
            "return_5d_after_event",
            "return_60d_after_stage2",
            "mfe_60d_after_stage2",
            "relative_strength_vs_transport_basket",
            "relative_strength_vs_auto_basket",
            "relative_strength_vs_tourism_basket",
            "relative_strength_vs_shipping_basket",
            "vehicle_sales_volume",
            "hybrid_mix",
            "us_localization_ratio",
            "tariff_cost",
            "price_cut_signal",
            "sdv_delay_flag",
            "capex_hike_flag",
            "parcel_volume",
            "parcel_unit_price",
            "delivery_cost_per_unit",
            "automation_capex",
            "labor_regulation_flag",
            "visitor_arrivals",
            "average_spend",
            "duty_free_sales",
            "casino_drop_amount",
            "casino_hold_rate",
            "hotel_revpar",
            "freight_rate_index",
            "teu_or_bulk_volume",
            "vessel_supply_growth",
            "red_sea_route_normalization_flag",
            "safety_accident_flag",
            "recall_flag",
            "quality_cost_flag",
            "insurance_compensation_flag",
        ):
            self.assertIn(field, fields)

    def test_score_stage_price_alignment_rows_and_markdown(self):
        rows = {row["case_id"]: row for row in round180_score_stage_price_alignment_rows()}
        markdown = render_round180_score_stage_price_alignment_markdown()

        self.assertEqual(len(rows), len(ROUND180_SCORE_STAGE_PRICE_ALIGNMENT))
        self.assertEqual(rows["kia_hybrid_localization_sdv_delay_stage2_4c_watch_case"]["verdict"], "hybrid_stage2_not_green_until_opm_tariff")
        self.assertEqual(rows["cj_logistics_shinsegae_oneday_volume_stage2_3_case"]["verdict"], "logistics_volume_needs_unit_margin")
        self.assertEqual(rows["jeju_air_muan_crash_hard_4c_case"]["verdict"], "airline_safety_hard_gate")
        self.assertIn("Kia", markdown)
        self.assertIn("CJ Logistics", markdown)
        self.assertIn("Jeju Air", markdown)

    def test_summary_and_markdown_explain_r9_loop11_guardrails(self):
        summary = round180_summary()
        summary_md = render_round180_summary_markdown()
        guardrails = render_round180_green_guardrail_markdown()
        overlays = render_round180_risk_overlay_markdown()
        price_plan = render_round180_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 14)
        self.assertEqual(summary["source_canonical_target_count"], 14)
        self.assertEqual(summary["case_candidate_count"], len(ROUND180_CASE_CANDIDATES))
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["case_records_are_candidate_generation_input"])
        self.assertIn("hybrid", summary_md)
        self.assertIn("OPM/FCF", summary_md)
        self.assertIn("tourism policy", guardrails)
        self.assertIn("visitor count", overlays)
        self.assertIn("casino_drop_amount", price_plan)
        self.assertIn("cj_logistics_shinsegae_oneday_volume_stage2_3_case", price_plan)

    def test_reports_are_written_and_case_jsonl_loads(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round180_r9_loop11_reports(
                output_directory=root / "reports",
                cases_path=root / "cases.jsonl",
                score_profile_path=root / "score_profiles.csv",
            )
            records = load_case_library(paths["cases"])

            self.assertEqual(len(records), len(ROUND180_CASE_CANDIDATES))
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["stage_date_plan"].exists())
            self.assertTrue(paths["price_fields"].exists())
            self.assertIn("Kia", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("mobility_tourism_freight_hybrid_headline_is_not_stage3", paths["cases"].read_text(encoding="utf-8"))

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

    def test_production_modules_do_not_import_round180(self):
        forbidden = "round180_r9_loop11_mobility_transport_leisure"
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
