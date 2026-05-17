import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round75_r9_loop3_report import build_parser
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round75_r9_loop3_mobility_transport_leisure import (
    ROUND75_CASE_CANDIDATES,
    ROUND75_PRICE_FIELDS,
    ROUND75_SCORE_TARGETS,
    render_round75_green_guardrail_markdown,
    render_round75_price_validation_plan_markdown,
    render_round75_risk_overlay_markdown,
    render_round75_summary_markdown,
    round75_case_candidate_rows,
    round75_case_records,
    round75_price_field_rows,
    round75_score_profile_rows,
    round75_stage_date_rows,
    round75_summary,
    target_for,
    write_round75_r9_loop3_reports,
)


class Round75R9Loop3MobilityTransportLeisureTests(unittest.TestCase):
    def test_round75_targets_cover_r9_loop3_archetypes(self):
        labels = {target.target_id for target in ROUND75_SCORE_TARGETS}

        self.assertEqual(len(labels), 19)
        for label in (
            "AUTO_MOBILITY_COMPLETED_VEHICLE",
            "AUTO_HYBRID_VALUEUP",
            "AUTO_MOBILITY_COMPONENTS",
            "HYBRID_COMPONENT_BOTTLENECK",
            "AUTO_COMPONENTS_EV_ADAS",
            "AUTONOMOUS_ROBOTAXI_DEPLOYMENT",
            "TIRE_AUTO_COMPONENT_SPREAD",
            "AIRLINE_TRAVEL_CYCLE",
            "TRAVEL_LEISURE_REOPENING",
            "CASINO_DUTYFREE_TOURISM",
            "SHIPPING_FREIGHT_CYCLE",
            "LOGISTICS_PARCEL_FREIGHT",
            "RENTAL_USED_CAR_MOBILITY",
            "MOBILITY_RENTAL_MICROMOBILITY",
            "URBAN_AIR_DRONE",
            "SPACE_SUPPLYCHAIN",
            "SATELLITE_CONNECTIVITY_INFRA",
            "TRANSPORT_SAFETY_REGULATORY_OVERLAY",
            "FLEET_UNIT_ECONOMICS_OVERLAY",
        ):
            self.assertIn(label, labels)
        for target in ROUND75_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.MOBILITY_TRANSPORT_LEISURE)
            self.assertFalse(target.production_scoring_changed)

    def test_auto_hybrid_and_satellite_are_green_possible_but_guardrailed(self):
        hybrid = target_for("AUTO_HYBRID_VALUEUP")
        satellite = target_for("SATELLITE_CONNECTIVITY_INFRA")

        assert hybrid is not None
        assert satellite is not None
        self.assertEqual(hybrid.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(hybrid.score_weight.capital_allocation, 10)
        self.assertIn("shareholder_return_ratio", hybrid.green_conditions)
        self.assertIn("tariff", hybrid.red_flags)
        self.assertEqual(satellite.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("satellite_backlog", satellite.green_conditions)
        self.assertIn("capex_debt", satellite.red_flags)

    def test_robotaxi_shipping_evtol_and_overlays_are_redteam_or_watch_first(self):
        robotaxi = target_for("AUTONOMOUS_ROBOTAXI_DEPLOYMENT")
        shipping = target_for("SHIPPING_FREIGHT_CYCLE")
        evtol = target_for("URBAN_AIR_DRONE")
        safety = target_for("TRANSPORT_SAFETY_REGULATORY_OVERLAY")
        fleet = target_for("FLEET_UNIT_ECONOMICS_OVERLAY")

        assert robotaxi is not None
        assert shipping is not None
        assert evtol is not None
        assert safety is not None
        assert fleet is not None
        self.assertEqual(robotaxi.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertEqual(shipping.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertEqual(evtol.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertTrue(safety.gate_only)
        self.assertTrue(fleet.gate_only)
        self.assertIn("spot_rate_below_breakeven", shipping.stage4c_conditions)
        self.assertIn("type_certification_flag", evtol.green_conditions)
        self.assertIn("nhtsa_scrutiny", safety.red_flags)
        self.assertIn("repair_cost", fleet.red_flags)

    def test_required_round75_cases_are_present_with_stage_dates(self):
        rows = {row["case_id"]: row for row in round75_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND75_CASE_CANDIDATES))
        self.assertEqual(rows["hyundai_hybrid_valueup_case"]["target_id"], "AUTO_HYBRID_VALUEUP")
        self.assertEqual(rows["hyundai_hybrid_valueup_case"]["stage2_date"], "2024-08-28")
        self.assertEqual(rows["hyundai_tariff_margin_cut_case"]["stage4b_date"], "2025-09-18")
        self.assertEqual(rows["toyota_hybrid_parts_bottleneck_case"]["target_id"], "HYBRID_COMPONENT_BOTTLENECK")
        self.assertEqual(rows["toyota_hybrid_parts_bottleneck_case"]["stage2_date"], "2025-03-31")
        self.assertEqual(rows["avride_hyundai_ioniq5_robotaxi_case"]["stage2_date"], "2025-03-05")
        self.assertEqual(rows["waymo_flood_recall_robotaxi_case"]["target_id"], "TRANSPORT_SAFETY_REGULATORY_OVERLAY")
        self.assertEqual(rows["waymo_flood_recall_robotaxi_case"]["stage4c_date"], "2026-05-01")
        self.assertEqual(rows["waymo_houston_expansion_case"]["stage4b_date"], "2026-05-01")
        self.assertEqual(rows["korean_air_asiana_integration_case"]["stage2_date"], "2025-02-07")
        self.assertEqual(rows["china_group_visa_tourism_case"]["case_type"], "event_premium")
        self.assertEqual(rows["ses_airline_connectivity_case"]["stage2_date"], "2026-05-12")
        self.assertEqual(rows["maersk_container_rate_collapse_case"]["stage4c_date"], "2025-10-03")
        self.assertEqual(rows["maersk_suez_overcapacity_loss_case"]["stage4b_date"], "2026-01-15")
        self.assertEqual(rows["hertz_ev_rental_failure_case"]["target_id"], "FLEET_UNIT_ECONOMICS_OVERLAY")
        self.assertEqual(rows["hertz_ev_rental_failure_case"]["stage4c_date"], "2024-01-11")
        self.assertEqual(rows["michelin_tire_demand_cut_case"]["stage4c_date"], "2025-10-13")
        self.assertEqual(rows["lime_ipo_micromobility_case"]["stage2_date"], "2026-05-08")
        self.assertEqual(rows["joby_discounted_offering_case"]["stage4c_date"], "2025-10-08")
        self.assertEqual(rows["lilium_evtol_cash_crunch_case"]["stage4c_date"], "2024-11-25")
        self.assertEqual(rows["archer_part135_no_type_cert_case"]["case_type"], "event_premium")
        self.assertEqual(rows["archer_nyc_network_case"]["stage4b_date"], "2025-04-17")

    def test_case_records_validate_and_keep_round75_guardrails(self):
        records = round75_case_records()

        self.assertEqual(len(records), len(ROUND75_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("demand_recovery_or_policy_headline_is_not_green_evidence_alone", record.green_guardrails)
            self.assertIn("hybrid_label_is_not_margin_or_fcf", record.green_guardrails)
            self.assertIn("freight_spike_is_not_structural_green", record.green_guardrails)
            self.assertIn("part135_is_not_type_certification_or_revenue", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["korean_air_asiana_integration_case"].rerating_result, "cyclical_rerating")
        self.assertEqual(by_id["china_group_visa_tourism_case"].score_price_alignment, "price_moved_without_evidence")
        self.assertEqual(by_id["hertz_ev_rental_failure_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["archer_part135_no_type_cert_case"].rerating_result, "event_premium")

    def test_score_profile_rows_match_round75_weight_table(self):
        rows = {row["target_id"]: row for row in round75_score_profile_rows()}

        self.assertEqual(rows["AUTO_MOBILITY_COMPLETED_VEHICLE"]["capital_allocation"], "10")
        self.assertEqual(rows["AUTO_HYBRID_VALUEUP"]["eps_fcf"], "21")
        self.assertEqual(rows["HYBRID_COMPONENT_BOTTLENECK"]["bottleneck_pricing"], "14")
        self.assertEqual(rows["AUTONOMOUS_ROBOTAXI_DEPLOYMENT"]["information_confidence"], "6")
        self.assertEqual(rows["SHIPPING_FREIGHT_CYCLE"]["structural_visibility"], "7")
        self.assertEqual(rows["URBAN_AIR_DRONE"]["eps_fcf"], "8")
        self.assertEqual(rows["SATELLITE_CONNECTIVITY_INFRA"]["structural_visibility"], "21")
        self.assertEqual(rows["TRANSPORT_SAFETY_REGULATORY_OVERLAY"]["gate_only"], "true")
        self.assertEqual(rows["FLEET_UNIT_ECONOMICS_OVERLAY"]["eps_fcf"], "gate")
        for row in rows.values():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round75_stage_date_rows()}
        fields = {row["field"] for row in round75_price_field_rows()}

        self.assertIn("op_margin_target", rows["AUTO_HYBRID_VALUEUP"]["stage2"])
        self.assertIn("hybrid_component_order", rows["HYBRID_COMPONENT_BOTTLENECK"]["stage2"])
        self.assertIn("paid_ride_volume", rows["AUTONOMOUS_ROBOTAXI_DEPLOYMENT"]["stage2"])
        self.assertIn("spot_rate_below_breakeven", rows["SHIPPING_FREIGHT_CYCLE"]["stage4c"])
        self.assertIn("tourist_spend", rows["CASINO_DUTYFREE_TOURISM"]["stage2"])
        self.assertIn("type_certification", rows["URBAN_AIR_DRONE"]["stage2"])
        self.assertIn("nhtsa_scrutiny", rows["TRANSPORT_SAFETY_REGULATORY_OVERLAY"]["stage4c"])
        for field in (
            "stage2_price",
            "below_stage2_price_flag",
            "vehicle_sales_growth",
            "hybrid_sales_growth",
            "op_margin_target",
            "shareholder_return_ratio",
            "tariff_event_flag",
            "hybrid_component_revenue",
            "capacity_normalization_flag",
            "adas_component_revenue",
            "robotaxi_service_area",
            "paid_ride_volume",
            "safety_recall_flag",
            "nhtsa_scrutiny_flag",
            "weather_handling_failure_flag",
            "insurance_liability_cost",
            "passenger_revenue_growth",
            "casino_drop_amount",
            "alipay_wechatpay_integration_flag",
            "freight_rate_index",
            "used_car_residual_value",
            "repair_cost_per_vehicle",
            "micromobility_fcf",
            "debt_maturity_amount",
            "type_certification_flag",
            "part135_flag",
            "vertiport_contract_flag",
            "satellite_backlog",
            "gross_backlog",
            "capex_debt_ratio",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND75_PRICE_FIELDS))

    def test_summary_and_markdown_explain_r9_loop3_guardrails(self):
        summary = round75_summary()
        summary_md = render_round75_summary_markdown()
        guardrails = render_round75_green_guardrail_markdown()
        overlays = render_round75_risk_overlay_markdown()
        price_plan = render_round75_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 19)
        self.assertEqual(summary["case_candidate_count"], 18)
        self.assertEqual(summary["success_candidate_count"], 5)
        self.assertEqual(summary["cyclical_success_count"], 1)
        self.assertEqual(summary["event_premium_count"], 3)
        self.assertEqual(summary["stage4b_case_count"], 11)
        self.assertEqual(summary["stage4c_case_count"], 6)
        self.assertEqual(summary["green_possible_count"], 2)
        self.assertEqual(summary["watch_yellow_first_count"], 12)
        self.assertEqual(summary["redteam_first_count"], 5)
        self.assertEqual(summary["gate_only_target_count"], 2)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("Round 75", summary_md)
        self.assertIn("Do not apply R9 Loop-3 v3.0 weights", guardrails)
        self.assertIn("ROBOTAXI_SAFETY_4C", overlays)
        self.assertIn("hyundai_tariff_margin_cut_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round75_r9_loop3_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r9_loop3_round75.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round75_r9_loop3_v3.csv",
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
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND75_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round75_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round75_r9_loop3_mobility_transport_leisure", text)


if __name__ == "__main__":
    unittest.main()
