import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round188_r4_loop12_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round188_r4_loop12_materials_spread_strategic import (
    ROUND188_BASE_SCORE_WEIGHTS,
    ROUND188_CASE_CANDIDATES,
    ROUND188_PRICE_FIELDS,
    ROUND188_SCORE_TARGETS,
    ROUND188_SOURCE_CANONICAL_TARGET_COUNT,
    ROUND188_SOURCE_CANONICAL_TARGET_IDS,
    ROUND188_STAGE_CAPS,
    render_round188_green_guardrail_markdown,
    render_round188_price_validation_plan_markdown,
    render_round188_risk_overlay_markdown,
    render_round188_score_stage_price_alignment_markdown,
    render_round188_summary_markdown,
    round188_base_score_weight_rows,
    round188_case_candidate_rows,
    round188_case_records,
    round188_price_field_rows,
    round188_score_profile_rows,
    round188_score_stage_price_alignment_rows,
    round188_stage_cap_rows,
    round188_stage_date_rows,
    round188_summary,
    round188_target_for,
    write_round188_r4_loop12_reports,
)


class Round188R4Loop12MaterialsSpreadStrategicTests(unittest.TestCase):
    def test_round188_targets_cover_loop12_archetypes(self):
        labels = {target.target_id for target in ROUND188_SCORE_TARGETS}

        self.assertEqual(len(labels), 10)
        self.assertEqual(ROUND188_SOURCE_CANONICAL_TARGET_COUNT, 10)
        self.assertEqual(set(ROUND188_SOURCE_CANONICAL_TARGET_IDS), labels)
        for target in ROUND188_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.MATERIALS_SPREAD_STRATEGIC)
            self.assertFalse(target.production_scoring_changed)

    def test_new_loop12_canonical_archetypes_exist(self):
        expected = (
            E2RArchetype.REFINING_SPREAD_TURNAROUND_KOREA,
            E2RArchetype.REFINING_PETCHEM_MIX_DRAG,
            E2RArchetype.PETROCHEMICAL_RESTRUCTURING_KOREA,
            E2RArchetype.NCC_CAPACITY_CUT_STAGE2,
            E2RArchetype.NCC_OVERLOAD_SHAHEEN_RISK,
            E2RArchetype.SPECIALTY_CHEM_GOVERNANCE_RESTRUCTURING,
            E2RArchetype.SYNTHETIC_RUBBER_TARIFF_RISK,
            E2RArchetype.TIRE_RUBBER_PRODUCTION_DISRUPTION,
            E2RArchetype.COMMODITY_SPREAD_CYCLE_NOT_STRUCTURAL,
            E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_base_weights_and_stage_caps_match_round188_note(self):
        weights = {row["component"]: row for row in round188_base_score_weight_rows()}
        caps = {row["stage_band"]: row for row in round188_stage_cap_rows()}

        self.assertEqual(len(ROUND188_BASE_SCORE_WEIGHTS), 7)
        self.assertEqual(weights["eps_fcf_opm_conversion"]["points"], "22")
        self.assertEqual(weights["spread_product_margin_durability"]["points"], "18")
        self.assertEqual(weights["restructuring_supply_cut_visibility"]["points"], "18")
        self.assertEqual(weights["early_price_path_validation"]["points"], "10")
        self.assertEqual(weights["cycle_commodity_risk"]["points"], "12")
        self.assertEqual(weights["operational_tariff_disclosure_redteam"]["points"], "12")
        self.assertEqual(weights["valuation_room_4b_runway"]["points"], "8")
        self.assertEqual(len(ROUND188_STAGE_CAPS), 5)
        self.assertEqual(caps["Stage 3"]["max_score"], "requires_5_of_8")
        self.assertIn("op_ex_inventory_effect_improves", caps["Stage 3"]["required_evidence"])
        self.assertEqual(caps["Stage 4B"]["max_score"], "requires_4_of_6")
        self.assertIn("spread_depends_on_event_supply_disruption", caps["Stage 4B"]["required_evidence"])
        self.assertEqual(caps["Stage 4C"]["max_score"], "hard_gate")
        self.assertIn("large_factory_fire_or_production_halt", caps["Stage 4C"]["required_evidence"])
        for row in weights.values():
            self.assertEqual(row["production_scoring_changed"], "false")
        for row in caps.values():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_refining_restructuring_and_hard_gate_targets_are_separated(self):
        refining = round188_target_for("REFINING_SPREAD_TURNAROUND_KOREA")
        mix_drag = round188_target_for("REFINING_PETCHEM_MIX_DRAG")
        petro = round188_target_for("PETROCHEMICAL_RESTRUCTURING_KOREA")
        ncc_cut = round188_target_for("NCC_CAPACITY_CUT_STAGE2")
        shaheen = round188_target_for("NCC_OVERLOAD_SHAHEEN_RISK")
        governance = round188_target_for("SPECIALTY_CHEM_GOVERNANCE_RESTRUCTURING")
        rubber = round188_target_for("SYNTHETIC_RUBBER_TARIFF_RISK")
        tire = round188_target_for("TIRE_RUBBER_PRODUCTION_DISRUPTION")

        for target in (refining, mix_drag, petro, ncc_cut, shaheen, governance, rubber, tire):
            self.assertIsNotNone(target)
        assert refining is not None
        assert mix_drag is not None
        assert petro is not None
        assert ncc_cut is not None
        assert shaheen is not None
        assert governance is not None
        assert rubber is not None
        assert tire is not None
        self.assertEqual(refining.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("op_ex_inventory_effect_improves", refining.green_conditions)
        self.assertEqual(mix_drag.score_weight.eps_fcf_opm, "cap")
        self.assertIn("plant_shutdown_executed", petro.green_conditions)
        self.assertIn("capacity_cut_executed", ncc_cut.green_conditions)
        self.assertTrue(shaheen.hard_gate)
        self.assertIn("new_capacity_worsens_oversupply", shaheen.red_flags)
        self.assertIn("capital_return_executed", governance.green_conditions)
        self.assertIn("china_antidumping_duty", rubber.red_flags)
        self.assertTrue(tire.hard_gate)

    def test_required_round188_cases_are_present(self):
        rows = {row["case_id"]: row for row in round188_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND188_CASE_CANDIDATES))
        self.assertEqual(rows["sk_innovation_refining_spread_turnaround_case"]["target_id"], "REFINING_SPREAD_TURNAROUND_KOREA")
        self.assertIn("q1_op_2_2tn_krw", rows["sk_innovation_refining_spread_turnaround_case"]["evidence_fields"])
        self.assertEqual(rows["sk_innovation_refining_cycle_peak_4b_case"]["case_type"], "4b_watch")
        self.assertEqual(rows["lotte_hd_hyundai_ncc_capacity_cut_stage2_case"]["target_id"], "NCC_CAPACITY_CUT_STAGE2")
        self.assertIn("1_1m_ton_shutdown", rows["lotte_hd_hyundai_ncc_capacity_cut_stage2_case"]["evidence_fields"])
        self.assertEqual(rows["lg_chem_nav_governance_restructuring_stage2_case"]["target_id"], "SPECIALTY_CHEM_GOVERNANCE_RESTRUCTURING")
        self.assertEqual(rows["soil_shaheen_oversupply_4c_watch_case"]["case_type"], "4c_thesis_break")
        self.assertEqual(rows["kumho_petrochemical_epdm_tariff_risk_case"]["target_id"], "SYNTHETIC_RUBBER_TARIFF_RISK")
        self.assertEqual(rows["kumho_tire_gwangju_fire_hard_4c_case"]["target_id"], "TIRE_RUBBER_PRODUCTION_DISRUPTION")
        self.assertEqual(rows["r4_loop12_disclosure_confidence_reference_case"]["target_id"], "DISCLOSURE_CONFIDENCE_CAP")

    def test_case_records_validate_and_keep_loop12_guardrails(self):
        records = round188_case_records()

        self.assertEqual(len(records), len(ROUND188_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "MATERIALS_SPREAD_STRATEGIC")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("stage3_early_catch_requires_5_of_8_loop12_conditions", record.green_guardrails)
            self.assertIn("commodity_spread_or_restructuring_keyword_cannot_create_stage3", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["sk_innovation_refining_cycle_peak_4b_case"].rerating_result, "theme_overheat")
        self.assertEqual(by_id["soil_shaheen_oversupply_4c_watch_case"].score_price_alignment, "false_positive_score")
        self.assertEqual(by_id["kumho_tire_gwangju_fire_hard_4c_case"].score_price_alignment, "false_positive_score")
        self.assertEqual(by_id["kumho_petrochemical_epdm_tariff_risk_case"].score_price_alignment, "evidence_good_but_price_failed")

    def test_score_profile_rows_mark_no_production_change(self):
        rows = round188_score_profile_rows()
        by_target = {row["target_id"]: row for row in rows}

        self.assertEqual(len(rows), len(ROUND188_SCORE_TARGETS))
        self.assertEqual(by_target["REFINING_SPREAD_TURNAROUND_KOREA"]["eps_fcf_opm"], "22")
        self.assertEqual(by_target["PETROCHEMICAL_RESTRUCTURING_KOREA"]["restructuring_supply_cut_visibility"], "20")
        self.assertEqual(by_target["NCC_CAPACITY_CUT_STAGE2"]["restructuring_supply_cut_visibility"], "22")
        self.assertEqual(by_target["REFINING_PETCHEM_MIX_DRAG"]["eps_fcf_opm"], "cap")
        self.assertEqual(by_target["NCC_OVERLOAD_SHAHEEN_RISK"]["hard_gate"], "true")
        self.assertEqual(by_target["TIRE_RUBBER_PRODUCTION_DISRUPTION"]["hard_gate"], "true")
        self.assertEqual(by_target["DISCLOSURE_CONFIDENCE_CAP"]["eps_fcf_opm"], "cap")
        for row in rows:
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_stage_date_price_and_alignment_rows_are_explicit(self):
        stage_rows = {row["target_id"]: row for row in round188_stage_date_rows()}
        price_fields = {row["field"] for row in round188_price_field_rows()}
        alignment_rows = {row["case_id"]: row for row in round188_score_stage_price_alignment_rows()}

        self.assertIn("op_ex_inventory_effect_improves", stage_rows["REFINING_SPREAD_TURNAROUND_KOREA"]["stage3"])
        self.assertIn("battery_loss_expands", stage_rows["REFINING_PETCHEM_MIX_DRAG"]["stage4c"])
        self.assertIn("plant_shutdown_executed", stage_rows["PETROCHEMICAL_RESTRUCTURING_KOREA"]["stage3"])
        self.assertIn("new_capacity_worsens_oversupply", stage_rows["NCC_OVERLOAD_SHAHEEN_RISK"]["stage4c"])
        self.assertIn("factory_fire", stage_rows["TIRE_RUBBER_PRODUCTION_DISRUPTION"]["stage4c"])
        for field in (
            "relative_strength_vs_chemical_basket",
            "relative_strength_vs_refining_basket",
            "relative_strength_vs_materials_basket",
            "refining_margin",
            "petrochemical_spread",
            "rubber_spread",
            "op_ex_inventory_effect",
            "capacity_cut_amount",
            "plant_shutdown_flag",
            "shutdown_duration",
            "government_support_amount",
            "asset_sale_amount",
            "new_capacity_addition",
            "china_oversupply_flag",
            "tariff_or_antidumping_flag",
            "factory_fire_flag",
            "plan_detail_disclosed_flag",
        ):
            self.assertIn(field, price_fields)
        self.assertEqual(alignment_rows["sk_innovation_refining_spread_turnaround_case"]["verdict"], "stage2_to_stage3_if_spread_fcf_drag_align")
        self.assertEqual(alignment_rows["soil_shaheen_oversupply_4c_watch_case"]["verdict"], "new_capacity_blocks_green")
        self.assertEqual(alignment_rows["kumho_tire_gwangju_fire_hard_4c_case"]["verdict"], "production_disruption_hard_gate")

    def test_summary_and_markdown_explain_loop12(self):
        summary = round188_summary()
        summary_md = render_round188_summary_markdown()
        guardrails = render_round188_green_guardrail_markdown()
        overlays = render_round188_risk_overlay_markdown()
        price_plan = render_round188_price_validation_plan_markdown()
        alignment = render_round188_score_stage_price_alignment_markdown()

        self.assertEqual(summary["target_count"], 10)
        self.assertEqual(summary["source_canonical_target_count"], 10)
        self.assertEqual(summary["case_candidate_count"], 10)
        self.assertEqual(summary["base_score_axis_count"], 7)
        self.assertEqual(summary["stage_cap_count"], 5)
        self.assertEqual(summary["score_stage_price_alignment_count"], 8)
        self.assertEqual(summary["success_candidate_count"], 4)
        self.assertEqual(summary["event_premium_count"], 0)
        self.assertEqual(summary["failed_rerating_count"], 3)
        self.assertEqual(summary["stage4b_case_count"], 1)
        self.assertEqual(summary["stage4c_case_count"], 2)
        self.assertEqual(summary["hard_gate_target_count"], 2)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R4 Loop 12", summary_md)
        self.assertIn("production_scoring_changed: false", summary_md)
        self.assertIn("at least 5 of 8 checks", guardrails)
        self.assertIn("NCC_OVERLOAD_SHAHEEN_RISK", overlays)
        self.assertIn("Required Fields", price_plan)
        self.assertIn("SK Innovation", alignment)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round188_r4_loop12_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r4_loop12_round188.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round188_r4_loop12_v12.csv",
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
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND188_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round188_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round188_r4_loop12_materials_spread_strategic", text)


if __name__ == "__main__":
    unittest.main()
