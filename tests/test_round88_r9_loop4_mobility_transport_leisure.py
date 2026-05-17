import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round88_r9_loop4_report import build_parser
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round88_r9_loop4_mobility_transport_leisure import (
    ROUND88_CASE_CANDIDATES,
    ROUND88_PRICE_FIELDS,
    ROUND88_SCORE_TARGETS,
    render_round88_green_guardrail_markdown,
    render_round88_price_validation_plan_markdown,
    render_round88_risk_overlay_markdown,
    render_round88_summary_markdown,
    round88_case_candidate_rows,
    round88_case_records,
    round88_price_field_rows,
    round88_score_profile_rows,
    round88_stage_date_rows,
    round88_summary,
    target_for,
    write_round88_r9_loop4_reports,
)


class Round88R9Loop4MobilityTransportLeisureTests(unittest.TestCase):
    def test_round88_targets_cover_r9_loop4_archetypes(self):
        labels = {target.target_id for target in ROUND88_SCORE_TARGETS}

        self.assertEqual(len(labels), 25)
        for label in (
            "AUTO_MOBILITY_COMPLETED_VEHICLE",
            "AUTO_HYBRID_VALUEUP",
            "AUTO_TARIFF_LOCALIZATION",
            "AUTO_MOBILITY_COMPONENTS",
            "HYBRID_COMPONENT_BOTTLENECK",
            "AUTO_COMPONENTS_EV_ADAS",
            "AUTONOMOUS_ROBOTAXI_DEPLOYMENT",
            "ROBOTAXI_OPERATIONAL_REALITY_CHECK",
            "ROBOTAXI_SAFETY_REGULATORY_OVERLAY",
            "TIRE_AUTO_COMPONENT_SPREAD",
            "AIRLINE_TRAVEL_CYCLE",
            "AIRLINE_INTEGRATION_SCALE",
            "TRAVEL_LEISURE_REOPENING",
            "CASINO_DUTYFREE_TOURISM",
            "SHIPPING_FREIGHT_CYCLE",
            "LOGISTICS_PARCEL_FREIGHT",
            "RENTAL_USED_CAR_MOBILITY",
            "EV_RENTAL_UNIT_ECONOMICS",
            "MOBILITY_RENTAL_MICROMOBILITY",
            "URBAN_AIR_DRONE",
            "EVTOL_CERTIFICATION_CASH_BURN",
            "SPACE_SUPPLYCHAIN",
            "SATELLITE_CONNECTIVITY_INFRA",
            "TRANSPORT_SAFETY_REGULATORY_OVERLAY",
            "FLEET_UNIT_ECONOMICS_OVERLAY",
        ):
            self.assertIn(label, labels)
        for target in ROUND88_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.MOBILITY_TRANSPORT_LEISURE)
            self.assertFalse(target.production_scoring_changed)

    def test_auto_hybrid_and_satellite_are_green_possible_but_guardrailed(self):
        hybrid = target_for("AUTO_HYBRID_VALUEUP")
        tariff = target_for("AUTO_TARIFF_LOCALIZATION")
        satellite = target_for("SATELLITE_CONNECTIVITY_INFRA")

        assert hybrid is not None
        assert tariff is not None
        assert satellite is not None
        self.assertEqual(hybrid.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(hybrid.score_weight.capital_allocation, 10)
        self.assertIn("shareholder_return_ratio", hybrid.green_conditions)
        self.assertIn("tariff", hybrid.red_flags)
        self.assertEqual(tariff.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("op_margin_cut", tariff.red_flags)
        self.assertIn("tariff_cost_absorbed", tariff.green_conditions)
        self.assertEqual(satellite.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("satellite_backlog", satellite.green_conditions)
        self.assertIn("capex_debt", satellite.red_flags)

    def test_robotaxi_shipping_evtol_and_overlays_are_redteam_or_watch_first(self):
        robotaxi = target_for("AUTONOMOUS_ROBOTAXI_DEPLOYMENT")
        robotaxi_ops = target_for("ROBOTAXI_OPERATIONAL_REALITY_CHECK")
        robotaxi_safety = target_for("ROBOTAXI_SAFETY_REGULATORY_OVERLAY")
        shipping = target_for("SHIPPING_FREIGHT_CYCLE")
        evtol = target_for("URBAN_AIR_DRONE")
        evtol_gate = target_for("EVTOL_CERTIFICATION_CASH_BURN")
        ev_rental = target_for("EV_RENTAL_UNIT_ECONOMICS")
        safety = target_for("TRANSPORT_SAFETY_REGULATORY_OVERLAY")
        fleet = target_for("FLEET_UNIT_ECONOMICS_OVERLAY")

        assert robotaxi is not None
        assert robotaxi_ops is not None
        assert robotaxi_safety is not None
        assert shipping is not None
        assert evtol is not None
        assert evtol_gate is not None
        assert ev_rental is not None
        assert safety is not None
        assert fleet is not None
        self.assertEqual(robotaxi.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertTrue(robotaxi_ops.gate_only)
        self.assertTrue(robotaxi_safety.gate_only)
        self.assertEqual(shipping.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertEqual(evtol.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertTrue(evtol_gate.gate_only)
        self.assertTrue(ev_rental.gate_only)
        self.assertTrue(safety.gate_only)
        self.assertTrue(fleet.gate_only)
        self.assertIn("long_wait_time", robotaxi_ops.stage4c_conditions)
        self.assertIn("weather_handling_failure", robotaxi_safety.stage4c_conditions)
        self.assertIn("spot_rate_below_breakeven", shipping.stage4c_conditions)
        self.assertIn("type_certification_flag", evtol.green_conditions)
        self.assertIn("type_certification_missing", evtol_gate.stage4c_conditions)
        self.assertIn("residual_value_drop", ev_rental.stage4c_conditions)
        self.assertIn("nhtsa_scrutiny", safety.red_flags)
        self.assertIn("repair_cost", fleet.red_flags)

    def test_required_round88_cases_are_present_with_stage_dates(self):
        rows = {row["case_id"]: row for row in round88_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND88_CASE_CANDIDATES))
        self.assertEqual(rows["hyundai_hybrid_valueup_case"]["target_id"], "AUTO_HYBRID_VALUEUP")
        self.assertEqual(rows["hyundai_hybrid_valueup_case"]["stage2_date"], "2024-08-28")
        self.assertEqual(rows["hyundai_tariff_margin_cut_case"]["target_id"], "AUTO_TARIFF_LOCALIZATION")
        self.assertEqual(rows["hyundai_tariff_margin_cut_case"]["stage4b_date"], "2025-09-18")
        self.assertEqual(rows["toyota_hybrid_parts_bottleneck_case"]["target_id"], "HYBRID_COMPONENT_BOTTLENECK")
        self.assertEqual(rows["toyota_hybrid_parts_bottleneck_case"]["stage2_date"], "2025-03-31")
        self.assertEqual(rows["avride_hyundai_ioniq5_robotaxi_case"]["stage2_date"], "2025-03-05")
        self.assertEqual(rows["tesla_texas_robotaxi_wait_time_case"]["target_id"], "ROBOTAXI_OPERATIONAL_REALITY_CHECK")
        self.assertEqual(rows["tesla_texas_robotaxi_wait_time_case"]["stage4c_date"], "2026-05-12")
        self.assertEqual(rows["waymo_flood_recall_robotaxi_case"]["target_id"], "ROBOTAXI_SAFETY_REGULATORY_OVERLAY")
        self.assertEqual(rows["waymo_flood_recall_robotaxi_case"]["stage4c_date"], "2026-05-12")
        self.assertEqual(rows["waymo_houston_expansion_case"]["stage4b_date"], "2026-05-13")
        self.assertEqual(rows["korean_air_asiana_integration_case"]["target_id"], "AIRLINE_INTEGRATION_SCALE")
        self.assertEqual(rows["korean_air_asiana_integration_case"]["stage2_date"], "2025-02-07")
        self.assertEqual(rows["china_group_visa_tourism_case"]["case_type"], "event_premium")
        self.assertEqual(rows["ses_airline_connectivity_case"]["stage2_date"], "2026-05-12")
        self.assertEqual(rows["maersk_hapag_container_rate_collapse_case"]["stage4c_date"], "2025-10-03")
        self.assertNotIn("maersk_suez_overcapacity_loss_case", rows)
        self.assertEqual(rows["hertz_ev_rental_failure_case"]["target_id"], "EV_RENTAL_UNIT_ECONOMICS")
        self.assertEqual(rows["hertz_ev_rental_failure_case"]["stage4c_date"], "2024-01-11")
        self.assertEqual(rows["michelin_tire_demand_cut_case"]["stage4c_date"], "2025-10-13")
        self.assertNotIn("lime_ipo_micromobility_case", rows)
        self.assertEqual(rows["joby_discounted_offering_case"]["target_id"], "EVTOL_CERTIFICATION_CASH_BURN")
        self.assertEqual(rows["joby_discounted_offering_case"]["stage4c_date"], "2025-10-08")
        self.assertEqual(rows["lilium_evtol_cash_crunch_case"]["target_id"], "EVTOL_CERTIFICATION_CASH_BURN")
        self.assertEqual(rows["lilium_evtol_cash_crunch_case"]["stage4c_date"], "2024-11-25")
        self.assertEqual(rows["archer_part135_no_type_cert_case"]["target_id"], "EVTOL_CERTIFICATION_CASH_BURN")
        self.assertEqual(rows["archer_part135_no_type_cert_case"]["case_type"], "event_premium")
        self.assertNotIn("archer_nyc_network_case", rows)

    def test_case_records_validate_and_keep_round88_guardrails(self):
        records = round88_case_records()

        self.assertEqual(len(records), len(ROUND88_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("demand_recovery_or_policy_headline_is_not_green_evidence_alone", record.green_guardrails)
            self.assertIn("hybrid_label_is_not_margin_or_fcf", record.green_guardrails)
            self.assertIn("robotaxi_deployment_is_not_unit_economics", record.green_guardrails)
            self.assertIn("freight_spike_is_not_structural_green", record.green_guardrails)
            self.assertIn("part135_is_not_type_certification_or_revenue", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["korean_air_asiana_integration_case"].rerating_result, "cyclical_rerating")
        self.assertEqual(by_id["china_group_visa_tourism_case"].score_price_alignment, "price_moved_without_evidence")
        self.assertEqual(by_id["hertz_ev_rental_failure_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["archer_part135_no_type_cert_case"].rerating_result, "event_premium")

    def test_score_profile_rows_match_round88_weight_table(self):
        rows = {row["target_id"]: row for row in round88_score_profile_rows()}

        self.assertEqual(rows["AUTO_MOBILITY_COMPLETED_VEHICLE"]["capital_allocation"], "10")
        self.assertEqual(rows["AUTO_HYBRID_VALUEUP"]["eps_fcf"], "21")
        self.assertEqual(rows["AUTO_TARIFF_LOCALIZATION"]["capital_allocation"], "5")
        self.assertEqual(rows["HYBRID_COMPONENT_BOTTLENECK"]["bottleneck_pricing"], "14")
        self.assertEqual(rows["AUTONOMOUS_ROBOTAXI_DEPLOYMENT"]["information_confidence"], "6")
        self.assertEqual(rows["ROBOTAXI_OPERATIONAL_REALITY_CHECK"]["gate_only"], "true")
        self.assertEqual(rows["ROBOTAXI_SAFETY_REGULATORY_OVERLAY"]["eps_fcf"], "gate")
        self.assertEqual(rows["AIRLINE_INTEGRATION_SCALE"]["structural_visibility"], "16")
        self.assertEqual(rows["SHIPPING_FREIGHT_CYCLE"]["structural_visibility"], "7")
        self.assertEqual(rows["EV_RENTAL_UNIT_ECONOMICS"]["gate_only"], "true")
        self.assertEqual(rows["URBAN_AIR_DRONE"]["eps_fcf"], "8")
        self.assertEqual(rows["EVTOL_CERTIFICATION_CASH_BURN"]["gate_only"], "true")
        self.assertEqual(rows["SATELLITE_CONNECTIVITY_INFRA"]["structural_visibility"], "21")
        self.assertEqual(rows["TRANSPORT_SAFETY_REGULATORY_OVERLAY"]["gate_only"], "true")
        self.assertEqual(rows["FLEET_UNIT_ECONOMICS_OVERLAY"]["eps_fcf"], "gate")
        for row in rows.values():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round88_stage_date_rows()}
        fields = {row["field"] for row in round88_price_field_rows()}

        self.assertIn("op_margin_target", rows["AUTO_HYBRID_VALUEUP"]["stage2"])
        self.assertIn("hybrid_component_order", rows["HYBRID_COMPONENT_BOTTLENECK"]["stage2"])
        self.assertIn("paid_ride_volume", rows["AUTONOMOUS_ROBOTAXI_DEPLOYMENT"]["stage2"])
        self.assertIn("long_wait_time", rows["ROBOTAXI_OPERATIONAL_REALITY_CHECK"]["stage4c"])
        self.assertIn("weather_handling_failure", rows["ROBOTAXI_SAFETY_REGULATORY_OVERLAY"]["stage4c"])
        self.assertIn("integration_synergy", rows["AIRLINE_INTEGRATION_SCALE"]["stage2"])
        self.assertIn("spot_rate_below_breakeven", rows["SHIPPING_FREIGHT_CYCLE"]["stage4c"])
        self.assertIn("residual_value_drop", rows["EV_RENTAL_UNIT_ECONOMICS"]["stage4c"])
        self.assertIn("tourist_spend", rows["CASINO_DUTYFREE_TOURISM"]["stage2"])
        self.assertIn("type_certification", rows["URBAN_AIR_DRONE"]["stage2"])
        self.assertIn("type_certification_missing", rows["EVTOL_CERTIFICATION_CASH_BURN"]["stage4c"])
        self.assertIn("nhtsa_scrutiny", rows["TRANSPORT_SAFETY_REGULATORY_OVERLAY"]["stage4c"])
        for field in (
            "stage2_price",
            "below_stage2_price_flag",
            "vehicle_sales_growth",
            "hybrid_sales_growth",
            "op_margin_target",
            "shareholder_return_ratio",
            "tariff_event_flag",
            "local_production_capacity",
            "hybrid_component_revenue",
            "capacity_normalization_flag",
            "hybrid_wait_time_months",
            "adas_component_revenue",
            "robotaxi_service_area",
            "paid_ride_volume",
            "wait_time_minutes",
            "ride_completion_rate",
            "misrouting_flag",
            "dropoff_distance_issue_flag",
            "safety_monitor_flag",
            "safety_recall_flag",
            "nhtsa_scrutiny_flag",
            "weather_handling_failure_flag",
            "insurance_liability_cost",
            "passenger_revenue_growth",
            "synergy_amount",
            "route_divestment_flag",
            "cargo_business_divestment_flag",
            "casino_drop_amount",
            "alipay_wechatpay_integration_flag",
            "freight_rate_index",
            "used_car_residual_value",
            "repair_cost_per_vehicle",
            "micromobility_fcf",
            "debt_maturity_amount",
            "type_certification_flag",
            "evtol_cash_burn",
            "part135_flag",
            "vertiport_contract_flag",
            "satellite_backlog",
            "gross_backlog",
            "capex_debt_ratio",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND88_PRICE_FIELDS))

    def test_summary_and_markdown_explain_r9_loop4_guardrails(self):
        summary = round88_summary()
        summary_md = render_round88_summary_markdown()
        guardrails = render_round88_green_guardrail_markdown()
        overlays = render_round88_risk_overlay_markdown()
        price_plan = render_round88_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 25)
        self.assertEqual(summary["case_candidate_count"], 16)
        self.assertEqual(summary["success_candidate_count"], 4)
        self.assertEqual(summary["cyclical_success_count"], 1)
        self.assertEqual(summary["event_premium_count"], 2)
        self.assertEqual(summary["stage4b_case_count"], 8)
        self.assertEqual(summary["stage4c_case_count"], 7)
        self.assertEqual(summary["green_possible_count"], 2)
        self.assertEqual(summary["watch_yellow_first_count"], 14)
        self.assertEqual(summary["redteam_first_count"], 9)
        self.assertEqual(summary["gate_only_target_count"], 6)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("Round 88", summary_md)
        self.assertIn("Do not apply R9 Loop-4 v4.0 weights", guardrails)
        self.assertIn("ROBOTAXI_SAFETY_4C", overlays)
        self.assertIn("hyundai_tariff_margin_cut_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round88_r9_loop4_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r9_loop4_round88.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round88_r9_loop4_v4.csv",
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
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND88_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round88_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round88_r9_loop4_mobility_transport_leisure", text)


if __name__ == "__main__":
    unittest.main()
