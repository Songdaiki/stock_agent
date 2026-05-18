import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round187_r3_loop12_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round187_r3_loop12_battery_ev_green import (
    ROUND187_BASE_SCORE_WEIGHTS,
    ROUND187_CASE_CANDIDATES,
    ROUND187_PRICE_FIELDS,
    ROUND187_SCORE_TARGETS,
    ROUND187_SOURCE_CANONICAL_TARGET_COUNT,
    ROUND187_SOURCE_CANONICAL_TARGET_IDS,
    ROUND187_STAGE_CAPS,
    render_round187_green_guardrail_markdown,
    render_round187_price_validation_plan_markdown,
    render_round187_risk_overlay_markdown,
    render_round187_score_stage_price_alignment_markdown,
    render_round187_summary_markdown,
    round187_base_score_weight_rows,
    round187_case_candidate_rows,
    round187_case_records,
    round187_price_field_rows,
    round187_score_profile_rows,
    round187_score_stage_price_alignment_rows,
    round187_stage_cap_rows,
    round187_stage_date_rows,
    round187_summary,
    round187_target_for,
    write_round187_r3_loop12_reports,
)


class Round187R3Loop12BatteryEVGreenTests(unittest.TestCase):
    def test_round187_targets_cover_loop12_archetypes(self):
        labels = {target.target_id for target in ROUND187_SCORE_TARGETS}

        self.assertEqual(len(labels), 15)
        self.assertEqual(ROUND187_SOURCE_CANONICAL_TARGET_COUNT, 15)
        self.assertEqual(set(ROUND187_SOURCE_CANONICAL_TARGET_IDS), labels)
        for target in ROUND187_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.BATTERY_EV_GREEN)
            self.assertFalse(target.production_scoring_changed)

    def test_new_loop12_canonical_archetypes_exist(self):
        expected = (
            E2RArchetype.EV_TO_ESS_CAPACITY_REDEPLOYMENT_KOREA,
            E2RArchetype.BATTERY_CONTRACT_CANCELLATION_4C,
            E2RArchetype.BATTERY_TAX_CREDIT_QUALITY_OVERLAY,
            E2RArchetype.SEPARATOR_EV_DEMAND_CYCLE,
            E2RArchetype.COPPER_FOIL_EV_DEMAND_CYCLE,
            E2RArchetype.ELECTROLYTE_CAPA_SUPPLYCHAIN,
            E2RArchetype.BATTERY_EQUIPMENT_CAPEX_CYCLE,
            E2RArchetype.BATTERY_RECYCLING_UNIT_ECONOMICS,
            E2RArchetype.SODIUM_ION_NEXTGEN_MATERIALS,
            E2RArchetype.HYDROGEN_FUEL_CELL_INFRA_KOREA,
            E2RArchetype.SOLAR_US_LOCALIZATION_SUPPLYCHAIN,
            E2RArchetype.WIND_POLICY_PERMITTING_RISK,
            E2RArchetype.BATTERY_SAFETY_INDUSTRIAL_ACCIDENT_OVERLAY,
            E2RArchetype.EV_BATTERY_TRANSPARENCY_REGULATORY_OVERLAY,
            E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_base_weights_and_stage_caps_match_round187_note(self):
        weights = {row["component"]: row for row in round187_base_score_weight_rows()}
        caps = {row["stage_band"]: row for row in round187_stage_cap_rows()}

        self.assertEqual(len(ROUND187_BASE_SCORE_WEIGHTS), 7)
        self.assertEqual(weights["eps_fcf_opm_conversion"]["points"], "24")
        self.assertEqual(weights["contract_customer_utilization_visibility"]["points"], "22")
        self.assertEqual(weights["capa_redeployment_line_conversion"]["points"], "12")
        self.assertEqual(weights["policy_subsidy_quality"]["points"], "10")
        self.assertEqual(weights["early_price_path_validation"]["points"], "10")
        self.assertEqual(weights["safety_regulatory_quality_disclosure"]["points"], "12")
        self.assertEqual(weights["valuation_room_4b_runway"]["points"], "10")
        self.assertEqual(len(ROUND187_STAGE_CAPS), 5)
        self.assertEqual(caps["Stage 3"]["max_score"], "requires_5_of_8")
        self.assertIn("profit_ex_subsidy_or_fcf_improves", caps["Stage 3"]["required_evidence"])
        self.assertEqual(caps["Stage 4B"]["max_score"], "requires_4_of_6")
        self.assertIn("profit_ex_subsidy_weak_but_price_rises", caps["Stage 4B"]["required_evidence"])
        self.assertEqual(caps["Stage 4C"]["max_score"], "hard_gate")
        self.assertIn("battery_fire_or_fatal_accident", caps["Stage 4C"]["required_evidence"])
        for row in weights.values():
            self.assertEqual(row["production_scoring_changed"], "false")
        for row in caps.values():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_stage2_targets_caps_and_hard_gates_are_separated(self):
        ess = round187_target_for("EV_TO_ESS_CAPACITY_REDEPLOYMENT_KOREA")
        cancellation = round187_target_for("BATTERY_CONTRACT_CANCELLATION_4C")
        tax_credit = round187_target_for("BATTERY_TAX_CREDIT_QUALITY_OVERLAY")
        sodium = round187_target_for("SODIUM_ION_NEXTGEN_MATERIALS")
        hydrogen = round187_target_for("HYDROGEN_FUEL_CELL_INFRA_KOREA")
        solar = round187_target_for("SOLAR_US_LOCALIZATION_SUPPLYCHAIN")
        wind = round187_target_for("WIND_POLICY_PERMITTING_RISK")
        safety = round187_target_for("BATTERY_SAFETY_INDUSTRIAL_ACCIDENT_OVERLAY")
        transparency = round187_target_for("EV_BATTERY_TRANSPARENCY_REGULATORY_OVERLAY")

        for target in (ess, cancellation, tax_credit, sodium, hydrogen, solar, wind, safety, transparency):
            self.assertIsNotNone(target)
        assert ess is not None
        assert cancellation is not None
        assert tax_credit is not None
        assert sodium is not None
        assert hydrogen is not None
        assert solar is not None
        assert wind is not None
        assert safety is not None
        assert transparency is not None
        self.assertFalse(ess.hard_gate)
        self.assertIn("profit_ex_subsidy_improves", ess.green_conditions)
        self.assertTrue(cancellation.hard_gate)
        self.assertIn("expected_revenue_loss", cancellation.red_flags)
        self.assertEqual(tax_credit.score_weight.eps_fcf_opm, "cap")
        self.assertIn("commercial_customer", sodium.green_conditions)
        self.assertIn("revenue_recognition", hydrogen.green_conditions)
        self.assertIn("customs_detention", solar.red_flags)
        self.assertTrue(wind.hard_gate)
        self.assertTrue(safety.hard_gate)
        self.assertTrue(transparency.hard_gate)

    def test_required_round187_cases_are_present(self):
        rows = {row["case_id"]: row for row in round187_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND187_CASE_CANDIDATES))
        self.assertEqual(rows["lges_ess_pivot_tax_credit_stage2_case"]["target_id"], "EV_TO_ESS_CAPACITY_REDEPLOYMENT_KOREA")
        self.assertIn("ira_ampc_dependency", rows["lges_ess_pivot_tax_credit_stage2_case"]["evidence_fields"])
        self.assertEqual(rows["lg_chem_sinopec_sodium_ion_stage2_option_case"]["target_id"], "SODIUM_ION_NEXTGEN_MATERIALS")
        self.assertIn("commercial_customer_missing", rows["lg_chem_sinopec_sodium_ion_stage2_option_case"]["red_flag_fields"])
        self.assertEqual(rows["doosan_fuelcell_ceres_sofc_stage23_candidate_case"]["target_id"], "HYDROGEN_FUEL_CELL_INFRA_KOREA")
        self.assertEqual(rows["qcells_us_localization_stage2_case"]["target_id"], "SOLAR_US_LOCALIZATION_SUPPLYCHAIN")
        self.assertEqual(rows["lges_ford_freudenberg_contract_cancellation_4c_case"]["case_type"], "4c_thesis_break")
        self.assertEqual(rows["aricell_battery_safety_fire_hard_4c_case"]["target_id"], "BATTERY_SAFETY_INDUSTRIAL_ACCIDENT_OVERLAY")
        self.assertEqual(rows["mercedes_battery_supplier_disclosure_trust_case"]["target_id"], "EV_BATTERY_TRANSPARENCY_REGULATORY_OVERLAY")
        self.assertEqual(rows["r3_loop12_disclosure_confidence_reference_case"]["target_id"], "DISCLOSURE_CONFIDENCE_CAP")

    def test_case_records_validate_and_keep_loop12_guardrails(self):
        records = round187_case_records()

        self.assertEqual(len(records), len(ROUND187_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "BATTERY_EV_GREEN")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("stage3_early_catch_requires_5_of_8_loop12_conditions", record.green_guardrails)
            self.assertIn("ev_ess_hydrogen_solar_wind_recycling_keywords_cannot_create_stage3", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["r3_loop12_keyword_4b_watch_case"].rerating_result, "theme_overheat")
        self.assertEqual(by_id["lges_ford_freudenberg_contract_cancellation_4c_case"].score_price_alignment, "false_positive_score")
        self.assertEqual(by_id["aricell_battery_safety_fire_hard_4c_case"].score_price_alignment, "false_positive_score")
        self.assertEqual(by_id["copper_foil_ev_demand_cycle_watch_case"].score_price_alignment, "evidence_good_but_price_failed")

    def test_score_profile_rows_mark_no_production_change(self):
        rows = round187_score_profile_rows()
        by_target = {row["target_id"]: row for row in rows}

        self.assertEqual(len(rows), len(ROUND187_SCORE_TARGETS))
        self.assertEqual(by_target["EV_TO_ESS_CAPACITY_REDEPLOYMENT_KOREA"]["eps_fcf_opm"], "24")
        self.assertEqual(by_target["BATTERY_CONTRACT_CANCELLATION_4C"]["hard_gate"], "true")
        self.assertEqual(by_target["BATTERY_TAX_CREDIT_QUALITY_OVERLAY"]["eps_fcf_opm"], "cap")
        self.assertEqual(by_target["BATTERY_SAFETY_INDUSTRIAL_ACCIDENT_OVERLAY"]["hard_gate"], "true")
        self.assertEqual(by_target["EV_BATTERY_TRANSPARENCY_REGULATORY_OVERLAY"]["hard_gate"], "true")
        for row in rows:
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_stage_date_price_and_alignment_rows_are_explicit(self):
        stage_rows = {row["target_id"]: row for row in round187_stage_date_rows()}
        price_fields = {row["field"] for row in round187_price_field_rows()}
        alignment_rows = {row["case_id"]: row for row in round187_score_stage_price_alignment_rows()}

        self.assertIn("profit_ex_subsidy_improves", stage_rows["EV_TO_ESS_CAPACITY_REDEPLOYMENT_KOREA"]["stage3"])
        self.assertIn("contract_cancelled", stage_rows["BATTERY_CONTRACT_CANCELLATION_4C"]["stage4c"])
        self.assertIn("customs_detention", stage_rows["SOLAR_US_LOCALIZATION_SUPPLYCHAIN"]["stage4c"])
        self.assertIn("permit_halt", stage_rows["WIND_POLICY_PERMITTING_RISK"]["stage4c"])
        self.assertIn("fatal_accident", stage_rows["BATTERY_SAFETY_INDUSTRIAL_ACCIDENT_OVERLAY"]["stage4c"])
        for field in (
            "relative_strength_vs_battery_basket",
            "relative_strength_vs_renewable_basket",
            "relative_strength_vs_hydrogen_basket",
            "profit_ex_subsidy",
            "ira_ampc_dependency",
            "contract_cancellation_flag",
            "customs_detention_flag",
            "uflpa_risk_flag",
            "wind_permit_halt_flag",
            "battery_fire_flag",
            "fatal_accident_flag",
            "supplier_disclosure_issue_flag",
            "valuation_at_stage4b",
        ):
            self.assertIn(field, price_fields)
        self.assertEqual(alignment_rows["lges_ess_pivot_tax_credit_stage2_case"]["verdict"], "subsidy_quality_not_green")
        self.assertEqual(alignment_rows["lges_ford_freudenberg_contract_cancellation_4c_case"]["verdict"], "contract_cancellation_blocks_green")
        self.assertEqual(alignment_rows["aricell_battery_safety_fire_hard_4c_case"]["verdict"], "safety_hard_gate_alignment")

    def test_summary_and_markdown_explain_loop12(self):
        summary = round187_summary()
        summary_md = render_round187_summary_markdown()
        guardrails = render_round187_green_guardrail_markdown()
        overlays = render_round187_risk_overlay_markdown()
        price_plan = render_round187_price_validation_plan_markdown()
        alignment = render_round187_score_stage_price_alignment_markdown()

        self.assertEqual(summary["target_count"], 15)
        self.assertEqual(summary["source_canonical_target_count"], 15)
        self.assertEqual(summary["case_candidate_count"], 17)
        self.assertEqual(summary["base_score_axis_count"], 7)
        self.assertEqual(summary["stage_cap_count"], 5)
        self.assertEqual(summary["score_stage_price_alignment_count"], 8)
        self.assertEqual(summary["success_candidate_count"], 8)
        self.assertEqual(summary["event_premium_count"], 0)
        self.assertEqual(summary["failed_rerating_count"], 2)
        self.assertEqual(summary["stage4b_case_count"], 1)
        self.assertEqual(summary["stage4c_case_count"], 6)
        self.assertEqual(summary["hard_gate_target_count"], 4)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R3 Loop 12", summary_md)
        self.assertIn("production_scoring_changed: false", summary_md)
        self.assertIn("at least 5 of 8 checks", guardrails)
        self.assertIn("BATTERY_CONTRACT_CANCELLATION_4C", overlays)
        self.assertIn("Required Fields", price_plan)
        self.assertIn("LGES", alignment)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round187_r3_loop12_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r3_loop12_round187.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round187_r3_loop12_v12.csv",
            )

            for key in (
                "cases",
                "score_profiles",
                "summary",
                "case_matrix",
                "stage_date_plan",
                "green_guardrails",
                "risk_overlays",
                "price_validation_plan",
                "price_fields",
                "base_score_weights",
                "stage_caps",
                "score_stage_price_alignment",
                "score_stage_price_alignment_md",
            ):
                self.assertTrue(paths[key].exists(), key)
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND187_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round187_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round187_r3_loop12_battery_ev_green", text)


if __name__ == "__main__":
    unittest.main()
