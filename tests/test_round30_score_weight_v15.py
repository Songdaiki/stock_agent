import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round30_score_weight_report import build_parser
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10ThemePosture
from e2r.sector.round30_score_weight_v15 import (
    ROUND30_CASE_CANDIDATES,
    ROUND30_SCORE_TARGETS,
    render_round30_cycle_cap_markdown,
    render_round30_semicapex_boundary_markdown,
    render_round30_summary_markdown,
    round30_case_records,
    round30_score_profile_rows,
    round30_summary,
    target_for,
    write_round30_score_weight_reports,
)


class Round30ScoreWeightV15Tests(unittest.TestCase):
    def test_round30_targets_include_v15_calibration_families(self):
        labels = {target.target_id for target in ROUND30_SCORE_TARGETS}

        self.assertEqual(len(labels), 10)
        self.assertIn("SEMI_EQUIPMENT_CAPEX", labels)
        self.assertIn("AUTO_COMPLETED_VEHICLE", labels)
        self.assertIn("AUTO_COMPONENTS_TIRE", labels)
        self.assertIn("AIRLINE_TRAVEL_CYCLE", labels)
        self.assertIn("CASINO_DUTYFREE_TOURISM", labels)
        self.assertIn("RETAIL_CONVENIENCE_OFFLINE", labels)
        self.assertIn("AGRI_LIVESTOCK_FOOD_COMMODITY", labels)
        self.assertIn("SPACE_SUPPLYCHAIN", labels)
        self.assertIn("AI_DATA_CENTER_COOLING", labels)
        self.assertIn("MEMORY_HBM", labels)

    def test_semi_equipment_is_watch_first_and_customer_capex_dependent(self):
        target = target_for("SEMI_EQUIPMENT_CAPEX")
        records = {record.case_id: record for record in round30_case_records()}
        boundary = render_round30_semicapex_boundary_markdown()

        self.assertIsNotNone(target)
        assert target is not None
        self.assertEqual(target.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("customer_capex_confirmed", target.green_conditions)
        self.assertIn("customer_concentration_risk_low", target.green_conditions)
        self.assertIn("customer_capex", target.red_flags)
        self.assertIn("Customer CAPEX", boundary)
        self.assertEqual(records["sk_hynix_asml_euv_capex_success_signal"].case_type, "success_candidate")
        self.assertEqual(records["customer_capex_cut_equipment_4c"].case_type, "4c_thesis_break")

    def test_completed_vehicle_can_be_green_possible_but_parts_and_tires_stay_watch(self):
        completed = target_for("AUTO_COMPLETED_VEHICLE")
        parts = target_for("AUTO_COMPONENTS_TIRE")
        records = {record.case_id: record for record in round30_case_records()}

        self.assertIsNotNone(completed)
        self.assertIsNotNone(parts)
        assert completed is not None
        assert parts is not None
        self.assertEqual(completed.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(completed.score_weight.capital_allocation, 10)
        self.assertIn("shareholder_return", completed.green_conditions)
        self.assertEqual(parts.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("customer_concentration", parts.red_flags)
        self.assertIn("raw_material", parts.red_flags)
        self.assertEqual(records["hyundai_hybrid_shareholder_return_candidate"].case_type, "success_candidate")
        self.assertEqual(records["tire_raw_material_margin_4c"].case_type, "4c_thesis_break")

    def test_airline_and_casino_are_cycle_watch_first_not_policy_green(self):
        airline = target_for("AIRLINE_TRAVEL_CYCLE")
        casino = target_for("CASINO_DUTYFREE_TOURISM")
        records = {record.case_id: record for record in round30_case_records()}
        cycle_review = render_round30_cycle_cap_markdown()

        self.assertIsNotNone(airline)
        self.assertIsNotNone(casino)
        assert airline is not None
        assert casino is not None
        self.assertEqual(airline.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertEqual(casino.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("fuel_fx_risk_low", airline.green_conditions)
        self.assertIn("tourist_mix_diversified", casino.green_conditions)
        self.assertEqual(records["korea_china_group_visa_free_tourism_stage1"].case_type, "event_premium")
        self.assertEqual(records["inspire_resort_underperformance_4c"].case_type, "4c_thesis_break")
        self.assertIn("visa or tourism policy is Stage 1", cycle_review)

    def test_retail_convenience_scores_productivity_not_store_count(self):
        target = target_for("RETAIL_CONVENIENCE_OFFLINE")
        records = {record.case_id: record for record in round30_case_records()}

        self.assertIsNotNone(target)
        assert target is not None
        self.assertEqual(target.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("same_store_sales_growth", target.green_conditions)
        self.assertIn("pb_high_margin_mix", target.green_conditions)
        self.assertIn("store_count_only", target.red_flags)
        self.assertEqual(records["cu_overseas_store_efficiency_candidate"].case_type, "success_candidate")
        self.assertEqual(records["convenience_overcrowding_same_store_slowdown_4c"].case_type, "4c_thesis_break")

    def test_agri_livestock_is_redteam_first_and_space_requires_contracts(self):
        agri = target_for("AGRI_LIVESTOCK_FOOD_COMMODITY")
        space = target_for("SPACE_SUPPLYCHAIN")
        records = {record.case_id: record for record in round30_case_records()}

        self.assertIsNotNone(agri)
        self.assertIsNotNone(space)
        assert agri is not None
        assert space is not None
        self.assertEqual(agri.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("disease_event", agri.red_flags)
        self.assertEqual(space.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("actual_delivery_contract", space.green_conditions)
        self.assertIn("no_contract", space.red_flags)
        self.assertEqual(records["livestock_disease_event_oneoff"].case_type, "one_off")
        self.assertEqual(records["spacex_theme_no_revenue_counterexample"].case_type, "failed_rerating")

    def test_ai_cooling_and_memory_hbm_are_green_possible_with_4c_monitoring(self):
        ai = target_for("AI_DATA_CENTER_COOLING")
        memory = target_for("MEMORY_HBM")

        self.assertIsNotNone(ai)
        self.assertIsNotNone(memory)
        assert ai is not None
        assert memory is not None
        self.assertEqual(ai.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(memory.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(memory.score_weight.eps_fcf, 24)
        self.assertIn("power_cooling_constraint", ai.green_conditions)
        self.assertIn("capex_delay", ai.red_flags)
        self.assertIn("hbm_demand", memory.green_conditions)
        self.assertIn("capex_reversal", memory.red_flags)

    def test_case_records_validate_and_keep_backfill_open(self):
        records = round30_case_records()

        self.assertEqual(len(records), len(ROUND30_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.price_validation.price_validation_status, "needs_price_backfill")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("theme_label_is_not_score_evidence", record.green_guardrails)

    def test_score_profile_rows_mark_no_production_change(self):
        for row in round30_score_profile_rows():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_summary_reports_v15_not_production_scoring(self):
        summary = round30_summary()
        markdown = render_round30_summary_markdown()

        self.assertEqual(summary["target_count"], 10)
        self.assertEqual(summary["case_candidate_count"], 28)
        self.assertEqual(summary["success_candidate_count"], 13)
        self.assertEqual(summary["stage4b_case_count"], 0)
        self.assertEqual(summary["stage4c_case_count"], 5)
        self.assertEqual(summary["green_possible_count"], 3)
        self.assertEqual(summary["watch_yellow_first_count"], 6)
        self.assertEqual(summary["redteam_first_count"], 1)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("production_scoring_changed: false", markdown)
        self.assertIn("Theme names, policy headlines, store counts, tourism headlines, and price rallies are not score evidence", markdown)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round30_score_weight_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_v12_round30.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round30_v15.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["green_guardrails"].exists())
            self.assertTrue(paths["cycle_cap"].exists())
            self.assertTrue(paths["semicapex_boundary"].exists())
            self.assertTrue(paths["price_validation_plan"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND30_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round30_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round30_score_weight_v15", text)


if __name__ == "__main__":
    unittest.main()
