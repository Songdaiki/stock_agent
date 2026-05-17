import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round54_r1_loop2_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round54_r1_loop2_industrial_infra import (
    ROUND54_CASE_CANDIDATES,
    ROUND54_PRICE_FIELDS,
    ROUND54_SCORE_TARGETS,
    render_round54_green_guardrail_markdown,
    render_round54_loop2_risk_overlay_markdown,
    render_round54_price_validation_plan_markdown,
    render_round54_summary_markdown,
    round54_case_candidate_rows,
    round54_case_records,
    round54_price_field_rows,
    round54_score_profile_rows,
    round54_stage_date_rows,
    round54_summary,
    target_for,
    write_round54_r1_loop2_reports,
)


class Round54R1Loop2IndustrialInfraTests(unittest.TestCase):
    def test_round54_targets_cover_r1_loop2_archetypes(self):
        labels = {target.target_id for target in ROUND54_SCORE_TARGETS}

        self.assertEqual(len(labels), 12)
        for label in (
            "GRID_TRANSFORMER_SHORTAGE",
            "AI_DATA_CENTER_POWER_EQUIPMENT",
            "CONTRACT_BACKLOG_INDUSTRIAL",
            "DEFENSE_GOVERNMENT_BACKLOG",
            "DEFENSE_TECH_AUTONOMOUS_SYSTEMS",
            "DEFENSE_DRONE_COUNTER_UAS",
            "DEFENSE_AI_SOFTWARE_INTELLIGENCE",
            "SHIPBUILDING_OFFSHORE_BACKLOG",
            "RAIL_INFRASTRUCTURE",
            "NUCLEAR_SMR_GRID_POLICY",
            "GEOPOLITICAL_RECONSTRUCTION",
            "SMART_FACTORY_AUTOMATION",
        ):
            self.assertIn(label, labels)
        for target in ROUND54_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.INDUSTRIAL_ORDERS_INFRA)
            self.assertFalse(target.production_scoring_changed)

    def test_new_r1_loop2_canonical_archetypes_exist(self):
        expected = (
            E2RArchetype.GRID_TRANSFORMER_SHORTAGE,
            E2RArchetype.AI_DATA_CENTER_POWER_EQUIPMENT,
            E2RArchetype.DEFENSE_TECH_AUTONOMOUS_SYSTEMS,
            E2RArchetype.DEFENSE_DRONE_COUNTER_UAS,
            E2RArchetype.DEFENSE_AI_SOFTWARE_INTELLIGENCE,
            E2RArchetype.RAIL_INFRASTRUCTURE,
            E2RArchetype.SMART_FACTORY_AUTOMATION,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_transformer_is_stronger_and_defense_has_capital_allocation_penalty(self):
        transformer = target_for("GRID_TRANSFORMER_SHORTAGE")
        defense = target_for("DEFENSE_GOVERNMENT_BACKLOG")
        nuclear = target_for("NUCLEAR_SMR_GRID_POLICY")

        self.assertIsNotNone(transformer)
        self.assertIsNotNone(defense)
        self.assertIsNotNone(nuclear)
        assert transformer is not None
        assert defense is not None
        assert nuclear is not None
        self.assertEqual(transformer.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(transformer.score_weight.eps_fcf, 23)
        self.assertEqual(transformer.score_weight.structural_visibility, 25)
        self.assertEqual(transformer.score_weight.bottleneck_pricing, 23)
        self.assertIn("data_center_delay", transformer.loop2_penalty_axes)
        self.assertEqual(defense.score_weight.capital_allocation, 3)
        self.assertIn("capital_allocation_shock", defense.loop2_penalty_axes)
        self.assertIn("customer_subscription_failed", nuclear.red_flags)

    def test_policy_rail_nuclear_and_smart_factory_are_watch_not_green_by_default(self):
        for target_id in (
            "RAIL_INFRASTRUCTURE",
            "NUCLEAR_SMR_GRID_POLICY",
            "GEOPOLITICAL_RECONSTRUCTION",
            "SMART_FACTORY_AUTOMATION",
            "DEFENSE_TECH_AUTONOMOUS_SYSTEMS",
        ):
            target = target_for(target_id)
            self.assertIsNotNone(target)
            assert target is not None
            self.assertEqual(target.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        reconstruction = target_for("GEOPOLITICAL_RECONSTRUCTION")
        assert reconstruction is not None
        self.assertIn("policy_to_contract_failed", reconstruction.loop2_penalty_axes)

    def test_required_round54_cases_are_present_with_dates_and_alignment(self):
        rows = {row["case_id"]: row for row in round54_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND54_CASE_CANDIDATES))
        self.assertEqual(rows["hanwha_aerospace_romania_k9_case"]["stage2_date"], "2024-07-09")
        self.assertEqual(rows["hanwha_aerospace_romania_k9_case"]["case_type"], "structural_success")
        self.assertEqual(rows["hanwha_aerospace_europe_sales_case"]["stage2_date"], "2024-10-07")
        self.assertEqual(rows["hyundai_rotem_morocco_rail_case"]["stage2_date"], "2025-02-26")
        self.assertEqual(rows["ge_vernova_data_center_orders_case"]["stage4b_date"], "2026-04-22")
        self.assertEqual(rows["hanwha_ocean_mro_rerating_case"]["stage4b_date"], "2025-04-28")
        self.assertEqual(rows["nuscale_cfpp_cancel_case"]["stage4c_date"], "2023-11-01")
        self.assertEqual(rows["data_center_delay_transformer_soft_4c_case"]["stage4c_date"], "2026-02-24")
        self.assertEqual(rows["ls_electric_525kv_datacenter_transformer_case"]["price_validation_status"], "needs_contract_date_backfill")

    def test_case_records_validate_and_keep_loop2_guardrails(self):
        records = round54_case_records()

        self.assertEqual(len(records), len(ROUND54_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("require_contract_quality_delivery_margin_eps_revision_for_green", record.green_guardrails)
            self.assertIn("do_not_invent_contract_dates_prices_or_margins", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["hanwha_aerospace_dilution_case"].score_price_alignment, "evidence_good_but_price_failed")
        self.assertEqual(by_id["nuscale_cfpp_cancel_case"].rerating_result, "thesis_break")

    def test_score_profile_rows_mark_no_production_change_and_include_loop2_penalties(self):
        rows = round54_score_profile_rows()

        self.assertEqual(len(rows), len(ROUND54_SCORE_TARGETS))
        for row in rows:
            self.assertEqual(row["large_sector"], "INDUSTRIAL_ORDERS_INFRA")
            self.assertEqual(row["production_scoring_changed"], "false")
            self.assertIn("loop2_penalty_axes", row)
        by_target = {row["target_id"]: row for row in rows}
        self.assertEqual(by_target["GRID_TRANSFORMER_SHORTAGE"]["eps_fcf"], "23")
        self.assertIn("data_center_delay", by_target["GRID_TRANSFORMER_SHORTAGE"]["loop2_penalty_axes"])
        self.assertIn("capital_allocation_shock", by_target["DEFENSE_GOVERNMENT_BACKLOG"]["loop2_penalty_axes"])

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round54_stage_date_rows()}
        fields = {row["field"] for row in round54_price_field_rows()}

        self.assertIn("fy1_fy2_fy3_revision", rows["GRID_TRANSFORMER_SHORTAGE"]["stage3"])
        self.assertIn("data_center_project_delay", rows["GRID_TRANSFORMER_SHORTAGE"]["stage4c"])
        self.assertIn("project_cancelled", rows["NUCLEAR_SMR_GRID_POLICY"]["stage4c"])
        for field in (
            "contract_value_to_sales",
            "delivery_schedule",
            "dilution_flag",
            "data_center_delay_flag",
            "block_sale_overhang_flag",
            "nuclear_ppa_flag",
            "cost_overrun_flag",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND54_PRICE_FIELDS))

    def test_summary_and_markdown_explain_loop2_guardrails(self):
        summary = round54_summary()
        summary_md = render_round54_summary_markdown()
        guardrails = render_round54_green_guardrail_markdown()
        overlays = render_round54_loop2_risk_overlay_markdown()
        price_plan = render_round54_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 12)
        self.assertEqual(summary["case_candidate_count"], 12)
        self.assertEqual(summary["structural_success_count"], 1)
        self.assertEqual(summary["success_candidate_count"], 5)
        self.assertEqual(summary["cyclical_success_count"], 1)
        self.assertEqual(summary["failed_rerating_count"], 1)
        self.assertEqual(summary["stage4b_case_count"], 3)
        self.assertEqual(summary["stage4c_case_count"], 2)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R1 Loop 2", summary_md)
        self.assertIn("Do not apply R1 Loop-2 v2.0 weights", guardrails)
        self.assertIn("capital_allocation_shock", overlays)
        self.assertIn("hanwha_aerospace_romania_k9_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round54_r1_loop2_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r1_loop2_round54.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round54_r1_loop2_v2.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["stage_date_plan"].exists())
            self.assertTrue(paths["green_guardrails"].exists())
            self.assertTrue(paths["loop2_risk_overlays"].exists())
            self.assertTrue(paths["price_validation_plan"].exists())
            self.assertTrue(paths["price_fields"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND54_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round54_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round54_r1_loop2_industrial_infra", text)


if __name__ == "__main__":
    unittest.main()
