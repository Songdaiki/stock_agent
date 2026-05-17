import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round62_r9_loop2_report import build_parser
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round62_r9_loop2_mobility_transport_leisure import (
    ROUND62_CASE_CANDIDATES,
    ROUND62_PRICE_FIELDS,
    ROUND62_SCORE_TARGETS,
    render_round62_green_guardrail_markdown,
    render_round62_price_validation_plan_markdown,
    render_round62_risk_overlay_markdown,
    render_round62_summary_markdown,
    round62_case_candidate_rows,
    round62_case_records,
    round62_price_field_rows,
    round62_score_profile_rows,
    round62_stage_date_rows,
    round62_summary,
    target_for,
    write_round62_r9_loop2_reports,
)


class Round62R9Loop2MobilityTransportLeisureTests(unittest.TestCase):
    def test_round62_targets_cover_r9_loop2_archetypes(self):
        labels = {target.target_id for target in ROUND62_SCORE_TARGETS}

        self.assertEqual(len(labels), 14)
        for label in (
            "AUTO_MOBILITY_COMPLETED_VEHICLE",
            "AUTO_MOBILITY_COMPONENTS",
            "AUTO_COMPONENTS_EV_ADAS",
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
        ):
            self.assertIn(label, labels)
        for target in ROUND62_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.MOBILITY_TRANSPORT_LEISURE)
            self.assertFalse(target.production_scoring_changed)

    def test_completed_vehicle_and_satellite_are_green_possible_but_guardrailed(self):
        completed = target_for("AUTO_MOBILITY_COMPLETED_VEHICLE")
        satellite = target_for("SATELLITE_CONNECTIVITY_INFRA")

        assert completed is not None
        assert satellite is not None
        self.assertEqual(completed.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(completed.score_weight.capital_allocation, 10)
        self.assertIn("shareholder_return", completed.green_conditions)
        self.assertIn("op_margin_cut", completed.red_flags)
        self.assertEqual(satellite.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("satellite_backlog", satellite.green_conditions)
        self.assertIn("capex_debt", satellite.red_flags)

    def test_shipping_and_evtol_are_redteam_first_and_part135_is_not_green(self):
        shipping = target_for("SHIPPING_FREIGHT_CYCLE")
        evtol = target_for("URBAN_AIR_DRONE")
        tourism = target_for("CASINO_DUTYFREE_TOURISM")

        assert shipping is not None
        assert evtol is not None
        assert tourism is not None
        self.assertEqual(shipping.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertEqual(evtol.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertEqual(tourism.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("spot_rate_below_breakeven", shipping.stage4c_conditions)
        self.assertIn("type_certification_flag", evtol.green_conditions)
        self.assertIn("policy_event_only", tourism.red_flags)

    def test_required_round62_cases_are_present_with_stage_dates(self):
        rows = {row["case_id"]: row for row in round62_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND62_CASE_CANDIDATES))
        self.assertEqual(rows["hyundai_hybrid_valueup_case"]["stage2_date"], "2024-08-28")
        self.assertEqual(rows["hyundai_tariff_margin_cut_case"]["stage4b_date"], "2025-09-18")
        self.assertEqual(rows["toyota_hybrid_parts_bottleneck_case"]["stage2_date"], "2025-03-31")
        self.assertEqual(rows["korean_air_asiana_integration_case"]["stage2_date"], "2025-02-07")
        self.assertEqual(rows["china_group_visa_tourism_case"]["case_type"], "event_premium")
        self.assertEqual(rows["china_group_visa_tourism_case"]["stage1_date"], "2025-09-29")
        self.assertEqual(rows["ses_airline_connectivity_case"]["stage2_date"], "2026-05-12")
        self.assertEqual(rows["maersk_overcapacity_rate_collapse_case"]["stage4c_date"], "2025-10-03")
        self.assertEqual(rows["maersk_suez_route_normalization_case"]["stage4b_date"], "2026-01-15")
        self.assertEqual(rows["hertz_ev_rental_failure_case"]["stage4c_date"], "2024-01-11")
        self.assertEqual(rows["hertz_additional_ev_charge_case"]["stage4c_date"], "2024-04-25")
        self.assertEqual(rows["michelin_tire_demand_cut_case"]["stage4c_date"], "2025-10-13")
        self.assertEqual(rows["lime_ipo_micromobility_case"]["stage2_date"], "2026-05-08")
        self.assertEqual(rows["joby_discounted_offering_case"]["stage4c_date"], "2025-10-08")
        self.assertEqual(rows["lilium_evtol_cash_crunch_case"]["stage4c_date"], "2024-11-25")
        self.assertEqual(rows["archer_part135_no_type_cert_case"]["case_type"], "event_premium")

    def test_case_records_validate_and_keep_round62_guardrails(self):
        records = round62_case_records()

        self.assertEqual(len(records), len(ROUND62_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("demand_recovery_or_policy_headline_is_not_green_evidence_alone", record.green_guardrails)
            self.assertIn("hybrid_label_is_not_margin_or_fcf", record.green_guardrails)
            self.assertIn("freight_spike_is_not_structural_green", record.green_guardrails)
            self.assertIn("part135_is_not_type_certification_or_revenue", record.green_guardrails)
            self.assertIn(
                "do_not_invent_opm_fcf_tariff_freight_drop_unit_economics_certification_backlog_or_stage_prices",
                record.green_guardrails,
            )
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["korean_air_asiana_integration_case"].rerating_result, "cyclical_rerating")
        self.assertEqual(by_id["china_group_visa_tourism_case"].score_price_alignment, "price_moved_without_evidence")
        self.assertEqual(by_id["hertz_ev_rental_failure_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["archer_part135_no_type_cert_case"].rerating_result, "event_premium")

    def test_score_profile_rows_match_round62_weight_table(self):
        rows = {row["target_id"]: row for row in round62_score_profile_rows()}

        self.assertEqual(rows["AUTO_MOBILITY_COMPLETED_VEHICLE"]["capital_allocation"], "10")
        self.assertEqual(rows["AUTO_MOBILITY_COMPONENTS"]["structural_visibility"], "18")
        self.assertEqual(rows["TIRE_AUTO_COMPONENT_SPREAD"]["valuation"], "9")
        self.assertEqual(rows["SHIPPING_FREIGHT_CYCLE"]["structural_visibility"], "7")
        self.assertEqual(rows["URBAN_AIR_DRONE"]["eps_fcf"], "9")
        self.assertEqual(rows["SATELLITE_CONNECTIVITY_INFRA"]["structural_visibility"], "20")
        for row in rows.values():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round62_stage_date_rows()}
        fields = {row["field"] for row in round62_price_field_rows()}

        self.assertIn("op_margin_target", rows["AUTO_MOBILITY_COMPLETED_VEHICLE"]["stage2"])
        self.assertIn("spot_rate_below_breakeven", rows["SHIPPING_FREIGHT_CYCLE"]["stage4c"])
        self.assertIn("tourist_spend", rows["CASINO_DUTYFREE_TOURISM"]["stage2"])
        self.assertIn("type_certification", rows["URBAN_AIR_DRONE"]["stage2"])
        for field in (
            "stage2_price",
            "below_stage2_price_flag",
            "vehicle_sales_growth",
            "hybrid_sales_growth",
            "op_margin_target",
            "op_margin_cut_flag",
            "shareholder_return_ratio",
            "tariff_event_flag",
            "hybrid_component_order",
            "passenger_revenue_growth",
            "cargo_revenue_growth",
            "casino_drop_amount",
            "duty_free_asp",
            "freight_rate_index",
            "spot_rate_below_breakeven_flag",
            "suez_route_normalization_flag",
            "used_car_residual_value",
            "repair_cost_per_vehicle",
            "micromobility_fcf",
            "debt_maturity_amount",
            "going_concern_flag",
            "type_certification_flag",
            "part135_flag",
            "discounted_offering_flag",
            "satellite_backlog",
            "gross_backlog",
            "capex_debt_ratio",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND62_PRICE_FIELDS))

    def test_summary_and_markdown_explain_r9_loop2_guardrails(self):
        summary = round62_summary()
        summary_md = render_round62_summary_markdown()
        guardrails = render_round62_green_guardrail_markdown()
        overlays = render_round62_risk_overlay_markdown()
        price_plan = render_round62_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 14)
        self.assertEqual(summary["case_candidate_count"], 15)
        self.assertEqual(summary["success_candidate_count"], 4)
        self.assertEqual(summary["cyclical_success_count"], 1)
        self.assertEqual(summary["event_premium_count"], 2)
        self.assertEqual(summary["stage4b_case_count"], 9)
        self.assertEqual(summary["stage4c_case_count"], 6)
        self.assertEqual(summary["green_possible_count"], 2)
        self.assertEqual(summary["watch_yellow_first_count"], 9)
        self.assertEqual(summary["redteam_first_count"], 3)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("Round 62", summary_md)
        self.assertIn("Do not apply R9 Loop-2 v2.0 weights", guardrails)
        self.assertIn("EVTOL_CERTIFICATION_NOT_COMMERCIALIZATION", overlays)
        self.assertIn("hyundai_tariff_margin_cut_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round62_r9_loop2_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r9_loop2_round62.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round62_r9_loop2_v2.csv",
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
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND62_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round62_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round62_r9_loop2_mobility_transport_leisure", text)


if __name__ == "__main__":
    unittest.main()
