import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round172_r1_loop11_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round172_r1_loop11_industrial_infra import (
    ROUND172_BASE_SCORE_WEIGHTS,
    ROUND172_CASE_CANDIDATES,
    ROUND172_PRICE_FIELDS,
    ROUND172_SCORE_STAGE_PRICE_ALIGNMENT,
    ROUND172_SCORE_TARGETS,
    ROUND172_SOURCE_CANONICAL_TARGET_COUNT,
    ROUND172_SOURCE_CANONICAL_TARGET_IDS,
    ROUND172_STAGE_CAPS,
    render_round172_green_guardrail_markdown,
    render_round172_loop11_risk_overlay_markdown,
    render_round172_price_validation_plan_markdown,
    render_round172_score_stage_price_alignment_markdown,
    render_round172_summary_markdown,
    round172_base_score_weight_rows,
    round172_case_candidate_rows,
    round172_case_records,
    round172_price_field_rows,
    round172_score_profile_rows,
    round172_score_stage_price_alignment_rows,
    round172_stage_cap_rows,
    round172_stage_date_rows,
    round172_summary,
    round172_target_for,
    write_round172_r1_loop11_reports,
)


class Round172R1Loop11IndustrialInfraTests(unittest.TestCase):
    def test_round172_targets_cover_korea_r1_loop11_archetypes(self):
        labels = {target.target_id for target in ROUND172_SCORE_TARGETS}

        self.assertEqual(ROUND172_SOURCE_CANONICAL_TARGET_COUNT, 11)
        self.assertEqual(len(labels), 12)
        self.assertTrue(set(ROUND172_SOURCE_CANONICAL_TARGET_IDS).issubset(labels))
        self.assertIn("NUCLEAR_EXPORT_LEGAL_GATE", labels)
        for target in ROUND172_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.INDUSTRIAL_ORDERS_INFRA)
            self.assertFalse(target.production_scoring_changed)

    def test_new_r1_loop11_canonical_archetypes_exist(self):
        expected = (
            E2RArchetype.GRID_TRANSFORMER_SHORTAGE_KOREA,
            E2RArchetype.GRID_US_LOCALIZATION_CAPA,
            E2RArchetype.POWER_EQUIPMENT_BACKLOG_TO_FCF_KOREA,
            E2RArchetype.SHIPBUILDING_US_PLATFORM_RESTRUCTURING,
            E2RArchetype.SHIP_MRO_RECURRING_PLATFORM,
            E2RArchetype.NUCLEAR_EXPORT_PREFERRED_BIDDER,
            E2RArchetype.DEFENSE_AIRCRAFT_EXPORT_BACKLOG,
            E2RArchetype.DEFENSE_INTERCEPTOR_COMBAT_VALIDATION,
            E2RArchetype.GEOPOLITICAL_SHIPBUILDING_SANCTION_OVERLAY,
            E2RArchetype.MOU_LOI_NOT_CONTRACT,
            E2RArchetype.NUCLEAR_EXPORT_LEGAL_GATE,
            E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_loop11_base_score_weights_prioritize_early_price_validation(self):
        weights = {row["component"]: row for row in round172_base_score_weight_rows()}
        caps = {row["stage_band"]: row for row in round172_stage_cap_rows()}

        self.assertEqual(len(ROUND172_BASE_SCORE_WEIGHTS), 7)
        self.assertEqual(weights["eps_fcf_opm_conversion"]["points"], "24")
        self.assertEqual(weights["contract_backlog_customer_visibility"]["points"], "20")
        self.assertEqual(weights["bottleneck_pricing_power"]["points"], "18")
        self.assertEqual(weights["early_price_path_validation"]["points"], "12")
        self.assertEqual(weights["valuation_room_4b_runway"]["points"], "10")
        self.assertEqual(len(ROUND172_STAGE_CAPS), 6)
        self.assertEqual(caps["Stage 1"]["max_score"], "45")
        self.assertEqual(caps["Stage 2"]["max_score"], "70")
        self.assertEqual(caps["Stage 2.5"]["max_score"], "watch")
        self.assertIn("60d_mfe_20pct", caps["Stage 3"]["required_evidence"])
        self.assertIn("stage2_120d_mfe_80pct", caps["Stage 4B"]["required_evidence"])
        self.assertIn("sanction_or_export_control", caps["Stage 4C"]["required_evidence"])

    def test_loop11_target_rules_separate_green_watch_and_hard_gate(self):
        transformer = round172_target_for("GRID_TRANSFORMER_SHORTAGE_KOREA")
        hyosung = round172_target_for("GRID_US_LOCALIZATION_CAPA")
        nuclear = round172_target_for("NUCLEAR_EXPORT_PREFERRED_BIDDER")
        interceptor = round172_target_for("DEFENSE_INTERCEPTOR_COMBAT_VALIDATION")
        sanction = round172_target_for("GEOPOLITICAL_SHIPBUILDING_SANCTION_OVERLAY")
        loi = round172_target_for("MOU_LOI_NOT_CONTRACT")
        legal = round172_target_for("NUCLEAR_EXPORT_LEGAL_GATE")
        disclosure = round172_target_for("DISCLOSURE_CONFIDENCE_CAP")

        self.assertIsNotNone(transformer)
        self.assertIsNotNone(hyosung)
        self.assertIsNotNone(nuclear)
        self.assertIsNotNone(interceptor)
        self.assertIsNotNone(sanction)
        self.assertIsNotNone(loi)
        self.assertIsNotNone(legal)
        self.assertIsNotNone(disclosure)
        assert transformer is not None
        assert hyosung is not None
        assert nuclear is not None
        assert interceptor is not None
        assert sanction is not None
        assert loi is not None
        assert legal is not None
        assert disclosure is not None
        self.assertEqual(transformer.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(transformer.score_weight.early_price_validation, 12)
        self.assertIn("60d_mfe_20pct", transformer.stage3_conditions)
        self.assertEqual(hyosung.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("hico_utilization", hyosung.stage3_conditions)
        self.assertIn("preferred_bidder_only", nuclear.red_flags)
        self.assertIn("actual_contract_missing", interceptor.red_flags)
        self.assertTrue(sanction.hard_gate)
        self.assertIn("china_sanctions", sanction.stage4c_conditions)
        self.assertTrue(loi.hard_gate)
        self.assertIn("final_contract_missing", loi.red_flags)
        self.assertTrue(legal.hard_gate)
        self.assertIn("contract_signing_prohibited", legal.stage4c_conditions)
        self.assertFalse(disclosure.hard_gate)
        self.assertEqual(disclosure.score_weight.eps_fcf_opm, "cap")

    def test_required_round172_cases_are_present_with_stage_markers(self):
        rows = {row["case_id"]: row for row in round172_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND172_CASE_CANDIDATES))
        self.assertEqual(rows["hd_hyundai_electric_transformer_stage3_4b_case"]["target_id"], "GRID_TRANSFORMER_SHORTAGE_KOREA")
        self.assertEqual(rows["hd_hyundai_electric_transformer_stage3_4b_case"]["stage3_date"], "2026-05-11")
        self.assertEqual(rows["hd_hyundai_electric_transformer_stage3_4b_case"]["stage4b_date"], "2026-05-11")
        self.assertEqual(rows["hyosung_hico_hvdc_stage25_case"]["target_id"], "GRID_US_LOCALIZATION_CAPA")
        self.assertIn("hvdc_transformer", rows["hyosung_hico_hvdc_stage25_case"]["evidence_fields"])
        self.assertEqual(rows["doosan_czech_nuclear_preferred_bidder_case"]["target_id"], "NUCLEAR_EXPORT_PREFERRED_BIDDER")
        self.assertEqual(rows["doosan_czech_nuclear_preferred_bidder_case"]["stage2_date"], "2024-07-17")
        self.assertEqual(rows["kepco_engineering_czech_nuclear_preferred_bidder_case"]["symbol"], "052690")
        self.assertEqual(rows["kepco_kps_czech_nuclear_preferred_bidder_case"]["symbol"], "051600")
        self.assertEqual(rows["hd_hyundai_heavy_mipo_merger_stage2_4b_case"]["stage4b_date"], "2025-08-27")
        self.assertEqual(rows["hd_hyundai_marine_solution_ipo_mro_case"]["case_type"], "4b_watch")
        self.assertEqual(rows["kai_fa50_philippines_stage2_case"]["target_id"], "DEFENSE_AIRCRAFT_EXPORT_BACKLOG")
        self.assertIn("aircraft_count_12", rows["kai_fa50_philippines_stage2_case"]["evidence_fields"])
        self.assertEqual(rows["lig_nex1_cheongung_combat_validation_stage25_case"]["target_id"], "DEFENSE_INTERCEPTOR_COMBAT_VALIDATION")
        self.assertEqual(rows["lig_nex1_cheongung_combat_validation_stage25_case"]["stage4b_date"], "2025-06-13")
        self.assertEqual(rows["hanwha_ocean_china_sanction_4c_case"]["target_id"], "GEOPOLITICAL_SHIPBUILDING_SANCTION_OVERLAY")
        self.assertEqual(rows["hanwha_ocean_china_sanction_4c_case"]["price_validation_status"], "needs_source_date_backfill")
        self.assertEqual(rows["hd_hyundai_mipo_loi_only_case"]["target_id"], "MOU_LOI_NOT_CONTRACT")
        self.assertEqual(rows["hd_hyundai_mipo_loi_only_case"]["stage1_date"], "2025-04-08")
        self.assertEqual(rows["doosan_czech_nuclear_legal_gate_case"]["target_id"], "NUCLEAR_EXPORT_LEGAL_GATE")
        self.assertEqual(rows["doosan_czech_nuclear_legal_gate_case"]["stage4c_date"], "2024-10-30")

    def test_case_records_validate_and_keep_loop11_guardrails(self):
        records = round172_case_records()

        self.assertEqual(len(records), len(ROUND172_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "INDUSTRIAL_ORDERS_INFRA")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("stage3_early_catch_requires_4_of_6_loop11_conditions", record.green_guardrails)
            self.assertIn("stage4b_cooling_required_when_price_runs_ahead_of_revision", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["hd_hyundai_electric_transformer_stage3_4b_case"].score_price_alignment, "aligned")
        self.assertEqual(by_id["hd_hyundai_mipo_loi_only_case"].rerating_result, "event_premium")
        self.assertEqual(by_id["doosan_czech_nuclear_legal_gate_case"].rerating_result, "thesis_break")
        self.assertIn("china_sanctions", by_id["hanwha_ocean_china_sanction_4c_case"].red_flag_fields)

    def test_score_profile_rows_mark_no_production_change(self):
        rows = round172_score_profile_rows()

        self.assertEqual(len(rows), len(ROUND172_SCORE_TARGETS))
        for row in rows:
            self.assertEqual(row["large_sector"], "INDUSTRIAL_ORDERS_INFRA")
            self.assertEqual(row["production_scoring_changed"], "false")
            self.assertIn("loop11_penalty_axes", row)
        by_target = {row["target_id"]: row for row in rows}
        self.assertEqual(by_target["GRID_TRANSFORMER_SHORTAGE_KOREA"]["eps_fcf_opm"], "24")
        self.assertEqual(by_target["GRID_TRANSFORMER_SHORTAGE_KOREA"]["early_price_validation"], "12")
        self.assertIn("valuation_crowding", by_target["GRID_TRANSFORMER_SHORTAGE_KOREA"]["loop11_penalty_axes"])
        self.assertEqual(by_target["MOU_LOI_NOT_CONTRACT"]["hard_gate"], "true")
        self.assertEqual(by_target["NUCLEAR_EXPORT_LEGAL_GATE"]["hard_gate"], "true")
        self.assertEqual(by_target["GEOPOLITICAL_SHIPBUILDING_SANCTION_OVERLAY"]["hard_gate"], "true")
        self.assertEqual(by_target["DISCLOSURE_CONFIDENCE_CAP"]["eps_fcf_opm"], "cap")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round172_stage_date_rows()}
        fields = {row["field"] for row in round172_price_field_rows()}

        self.assertIn("60d_mfe_20pct", rows["GRID_TRANSFORMER_SHORTAGE_KOREA"]["stage3"])
        self.assertIn("hico_utilization", rows["GRID_US_LOCALIZATION_CAPA"]["stage3"])
        self.assertIn("final_contract_signed", rows["NUCLEAR_EXPORT_PREFERRED_BIDDER"]["stage3"])
        self.assertIn("ipo_first_day_premium", rows["SHIP_MRO_RECURRING_PLATFORM"]["stage4b"])
        self.assertIn("actual_export_contract", rows["DEFENSE_INTERCEPTOR_COMBAT_VALIDATION"]["stage3"])
        self.assertIn("china_sanctions", rows["GEOPOLITICAL_SHIPBUILDING_SANCTION_OVERLAY"]["stage4c"])
        self.assertIn("final_contract_missing", rows["MOU_LOI_NOT_CONTRACT"]["stage4c"])
        for field in (
            "price_at_stage2",
            "return_60d_after_stage2",
            "return_252d_after_stage3",
            "mfe_120d_after_stage2",
            "relative_strength_vs_kospi",
            "relative_strength_vs_sector",
            "valuation_at_stage3",
            "eps_revision_before_stage3",
            "op_revision_after_stage3",
            "contract_amount",
            "customer_name",
            "hico_plant_expansion_usd",
            "hvdc_transformer_flag",
            "czech_preferred_bidder_flag",
            "westinghouse_appeal_flag",
            "share_exchange_ratio",
            "ipo_first_day_return_pct",
            "mro_recurring_revenue_flag",
            "fa50_aircraft_count",
            "combat_validation_flag",
            "price_up_47pct_flag",
            "china_sanction_flag",
            "mou_flag",
            "loi_flag",
            "final_contract_missing_flag",
            "opendart_detail_fetched_flag",
            "contract_amount_disclosed_flag",
            "margin_disclosed_flag",
            "stage_after_redteam",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND172_PRICE_FIELDS))

    def test_score_stage_price_alignment_table_covers_loop11_core_examples(self):
        rows = {row["case_id"]: row for row in round172_score_stage_price_alignment_rows()}

        self.assertEqual(len(ROUND172_SCORE_STAGE_PRICE_ALIGNMENT), 10)
        self.assertEqual(rows["hd_hyundai_electric_transformer_stage3_4b_case"]["verdict"], "stage3_catch_and_4b_cool_required")
        self.assertEqual(rows["hyosung_hico_hvdc_stage25_case"]["verdict"], "stage2_5_not_green_yet")
        self.assertEqual(rows["doosan_czech_nuclear_preferred_bidder_case"]["verdict"], "event_to_contract_not_green_yet")
        self.assertEqual(rows["hd_hyundai_marine_solution_ipo_mro_case"]["verdict"], "good_model_but_ipo_4b")
        self.assertEqual(rows["hanwha_ocean_china_sanction_4c_case"]["verdict"], "hard_redteam_alignment")
        self.assertEqual(rows["hd_hyundai_mipo_loi_only_case"]["verdict"], "green_block_correct")

    def test_summary_and_markdown_explain_loop11_guardrails(self):
        summary = round172_summary()
        summary_md = render_round172_summary_markdown()
        guardrails = render_round172_green_guardrail_markdown()
        overlays = render_round172_loop11_risk_overlay_markdown()
        price_plan = render_round172_price_validation_plan_markdown()
        alignment = render_round172_score_stage_price_alignment_markdown()

        self.assertEqual(summary["target_count"], 12)
        self.assertEqual(summary["source_canonical_target_count"], 11)
        self.assertEqual(summary["case_candidate_count"], 12)
        self.assertEqual(summary["base_score_component_count"], 7)
        self.assertEqual(summary["stage_cap_count"], 6)
        self.assertEqual(summary["score_stage_price_alignment_count"], 10)
        self.assertEqual(summary["structural_success_count"], 1)
        self.assertEqual(summary["success_candidate_count"], 7)
        self.assertEqual(summary["event_premium_count"], 1)
        self.assertEqual(summary["stage4b_case_count"], 5)
        self.assertEqual(summary["stage4c_case_count"], 2)
        self.assertEqual(summary["hard_gate_target_count"], 3)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R1 Loop 11", summary_md)
        self.assertIn("Korea-first", summary_md)
        self.assertIn("early price-path validation", summary_md)
        self.assertIn("Do not apply R1 Loop-11 v11.0 weights", guardrails)
        self.assertIn("STAGE2_5_WATCH", overlays)
        self.assertIn("K_TRANSFORMER_4B", overlays)
        self.assertIn("LOI_NOT_CONTRACT", overlays)
        self.assertIn("score_price_alignment", price_plan)
        self.assertIn("HD현대일렉트릭", alignment)
        self.assertIn("Stage Caps", alignment)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round172_r1_loop11_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r1_loop11_round172.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round172_r1_loop11_v11.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["stage_date_plan"].exists())
            self.assertTrue(paths["green_guardrails"].exists())
            self.assertTrue(paths["loop11_risk_overlays"].exists())
            self.assertTrue(paths["price_validation_plan"].exists())
            self.assertTrue(paths["price_fields"].exists())
            self.assertTrue(paths["base_score_weights"].exists())
            self.assertTrue(paths["stage_caps"].exists())
            self.assertTrue(paths["score_stage_price_alignment"].exists())
            self.assertTrue(paths["score_stage_price_alignment_md"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND172_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round172_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round172_r1_loop11_industrial_infra", text)


if __name__ == "__main__":
    unittest.main()
