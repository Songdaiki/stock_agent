import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round93_r1_loop5_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round93_r1_loop5_industrial_infra import (
    ROUND93_CASE_CANDIDATES,
    ROUND93_PRICE_FIELDS,
    ROUND93_SCORE_TARGETS,
    render_round93_green_guardrail_markdown,
    render_round93_loop5_risk_overlay_markdown,
    render_round93_price_validation_plan_markdown,
    render_round93_summary_markdown,
    round93_case_candidate_rows,
    round93_case_records,
    round93_price_field_rows,
    round93_score_profile_rows,
    round93_stage_date_rows,
    round93_summary,
    round93_target_for,
    write_round93_r1_loop5_reports,
)


class Round93R1Loop5IndustrialInfraTests(unittest.TestCase):
    def test_round93_targets_cover_r1_loop5_archetypes_and_overlays(self):
        labels = {target.target_id for target in ROUND93_SCORE_TARGETS}

        self.assertEqual(len(labels), 19)
        for label in (
            "GRID_TRANSFORMER_SHORTAGE",
            "GRID_MEDIUM_VOLTAGE_EXPANSION",
            "GRID_SUPPLY_SLOT_PREBUY",
            "AI_DATA_CENTER_POWER_EQUIPMENT",
            "GAS_TURBINE_POWER_BACKLOG",
            "CONTRACT_BACKLOG_INDUSTRIAL",
            "DEFENSE_GOVERNMENT_BACKLOG",
            "DEFENSE_LOCAL_PRODUCTION_PLATFORM",
            "DEFENSE_CAPITAL_ALLOCATION_SHOCK",
            "DEFENSE_UNMANNED_NAVAL_SYSTEMS",
            "SHIPBUILDING_OFFSHORE_BACKLOG",
            "SHIPBUILDING_NAVAL_MRO",
            "RAIL_INFRASTRUCTURE",
            "NUCLEAR_EXISTING_PPA_RESTART",
            "NUCLEAR_SMR_GRID_POLICY",
            "GEOPOLITICAL_RECONSTRUCTION",
            "DATA_CENTER_GRID_PERMITTING_OVERLAY",
            "CAPITAL_ALLOCATION_DILUTION_OVERLAY",
            "DISCLOSURE_CONFIDENCE_CAP",
        ):
            self.assertIn(label, labels)
        for target in ROUND93_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.INDUSTRIAL_ORDERS_INFRA)
            self.assertFalse(target.production_scoring_changed)

    def test_new_r1_loop5_canonical_archetypes_exist(self):
        expected = (
            E2RArchetype.GRID_MEDIUM_VOLTAGE_EXPANSION,
            E2RArchetype.GRID_SUPPLY_SLOT_PREBUY,
            E2RArchetype.GAS_TURBINE_POWER_BACKLOG,
            E2RArchetype.DEFENSE_LOCAL_PRODUCTION_PLATFORM,
            E2RArchetype.DEFENSE_CAPITAL_ALLOCATION_SHOCK,
            E2RArchetype.DEFENSE_UNMANNED_NAVAL_SYSTEMS,
            E2RArchetype.SHIPBUILDING_NAVAL_MRO,
            E2RArchetype.NUCLEAR_EXISTING_PPA_RESTART,
            E2RArchetype.DATA_CENTER_GRID_PERMITTING_OVERLAY,
            E2RArchetype.CAPITAL_ALLOCATION_DILUTION_OVERLAY,
            E2RArchetype.DISCLOSURE_CONFIDENCE_CAP,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_loop5_weights_and_penalties_are_stricter_than_loop2(self):
        transformer = round93_target_for("GRID_TRANSFORMER_SHORTAGE")
        medium_voltage = round93_target_for("GRID_MEDIUM_VOLTAGE_EXPANSION")
        slot_prebuy = round93_target_for("GRID_SUPPLY_SLOT_PREBUY")
        turbine = round93_target_for("GAS_TURBINE_POWER_BACKLOG")
        defense = round93_target_for("DEFENSE_GOVERNMENT_BACKLOG")
        defense_local = round93_target_for("DEFENSE_LOCAL_PRODUCTION_PLATFORM")
        defense_shock = round93_target_for("DEFENSE_CAPITAL_ALLOCATION_SHOCK")
        unmanned = round93_target_for("DEFENSE_UNMANNED_NAVAL_SYSTEMS")
        smr = round93_target_for("NUCLEAR_SMR_GRID_POLICY")
        ppa = round93_target_for("NUCLEAR_EXISTING_PPA_RESTART")
        permitting = round93_target_for("DATA_CENTER_GRID_PERMITTING_OVERLAY")
        dilution = round93_target_for("CAPITAL_ALLOCATION_DILUTION_OVERLAY")
        disclosure_cap = round93_target_for("DISCLOSURE_CONFIDENCE_CAP")

        self.assertIsNotNone(transformer)
        self.assertIsNotNone(medium_voltage)
        self.assertIsNotNone(slot_prebuy)
        self.assertIsNotNone(turbine)
        self.assertIsNotNone(defense)
        self.assertIsNotNone(defense_local)
        self.assertIsNotNone(defense_shock)
        self.assertIsNotNone(unmanned)
        self.assertIsNotNone(smr)
        self.assertIsNotNone(ppa)
        self.assertIsNotNone(permitting)
        self.assertIsNotNone(dilution)
        self.assertIsNotNone(disclosure_cap)
        assert transformer is not None
        assert medium_voltage is not None
        assert slot_prebuy is not None
        assert turbine is not None
        assert defense is not None
        assert defense_local is not None
        assert defense_shock is not None
        assert unmanned is not None
        assert smr is not None
        assert ppa is not None
        assert permitting is not None
        assert dilution is not None
        assert disclosure_cap is not None
        self.assertEqual(transformer.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(transformer.score_weight.eps_fcf, 24)
        self.assertEqual(transformer.score_weight.bottleneck_pricing, 24)
        self.assertIn("low_margin_long_term_contract", transformer.loop5_penalty_axes)
        self.assertEqual(medium_voltage.score_weight.bottleneck_pricing, 20)
        self.assertIn("price_normalization", medium_voltage.red_flags)
        self.assertEqual(slot_prebuy.score_weight.structural_visibility, 24)
        self.assertIn("slot_cancelled", slot_prebuy.red_flags)
        self.assertEqual(turbine.score_weight.eps_fcf, 21)
        self.assertIn("wind_segment_loss", turbine.red_flags)
        self.assertIn("capital_allocation_shock", defense.loop5_penalty_axes)
        self.assertEqual(defense_local.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertTrue(defense_shock.hard_gate)
        self.assertIn("use_of_proceeds_unclear", defense_shock.red_flags)
        self.assertIn("production_contract_absent", unmanned.red_flags)
        self.assertEqual(smr.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("customer_subscription_failure", smr.red_flags)
        self.assertEqual(ppa.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertTrue(permitting.hard_gate)
        self.assertIn("moratorium", permitting.red_flags)
        self.assertTrue(dilution.hard_gate)
        self.assertIn("dilution", dilution.red_flags)
        self.assertFalse(disclosure_cap.hard_gate)
        self.assertEqual(disclosure_cap.score_weight.eps_fcf, "cap")
        self.assertIn("detail_missing", disclosure_cap.red_flags)

    def test_required_round93_cases_are_present_with_dates_and_alignment(self):
        rows = {row["case_id"]: row for row in round93_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND93_CASE_CANDIDATES))
        self.assertEqual(rows["us_transformer_shortage_import_slots_case"]["stage2_date"], "2026-05-11")
        self.assertEqual(rows["ls_electric_525kv_us_datacenter_transformer_case"]["target_id"], "GRID_TRANSFORMER_SHORTAGE")
        self.assertEqual(rows["ls_electric_525kv_us_datacenter_transformer_case"]["stage2_date"], "2025-11-01")
        self.assertEqual(rows["abb_medium_voltage_expansion_case"]["target_id"], "GRID_MEDIUM_VOLTAGE_EXPANSION")
        self.assertEqual(rows["ge_vernova_data_center_orders_case"]["stage4b_date"], "2026-04-22")
        self.assertEqual(rows["ge_vernova_power_backlog_turbine_case"]["target_id"], "GAS_TURBINE_POWER_BACKLOG")
        self.assertEqual(rows["ge_vernova_power_backlog_turbine_case"]["stage4b_date"], "2026-04-22")
        self.assertEqual(rows["us_power_demand_record_eia_case"]["target_id"], "AI_DATA_CENTER_POWER_EQUIPMENT")
        self.assertEqual(rows["perth_data_center_withdrawal_case"]["target_id"], "DATA_CENTER_GRID_PERMITTING_OVERLAY")
        self.assertEqual(rows["perth_data_center_withdrawal_case"]["stage4c_date"], "2026-05-15")
        self.assertEqual(rows["seattle_indianapolis_data_center_moratorium_case"]["target_id"], "DATA_CENTER_GRID_PERMITTING_OVERLAY")
        self.assertEqual(rows["seattle_indianapolis_data_center_moratorium_case"]["stage4c_date"], "2026-05-15")
        self.assertEqual(rows["hanwha_aerospace_romania_k9_case"]["stage2_date"], "2024-07-09")
        self.assertEqual(rows["hanwha_aerospace_romania_k9_case"]["case_type"], "structural_success")
        self.assertEqual(rows["hanwha_aerospace_europe_sales_visibility_case"]["target_id"], "DEFENSE_LOCAL_PRODUCTION_PLATFORM")
        self.assertEqual(rows["hanwha_aerospace_europe_sales_visibility_case"]["stage2_date"], "2024-10-07")
        self.assertEqual(rows["hanwha_aerospace_dilution_case"]["target_id"], "DEFENSE_CAPITAL_ALLOCATION_SHOCK")
        self.assertEqual(rows["hanwha_aerospace_dilution_case"]["stage4b_date"], "2025-03-27")
        self.assertEqual(rows["hanwha_ocean_us_shipbuilding_sanction_case"]["target_id"], "SHIPBUILDING_NAVAL_MRO")
        self.assertEqual(
            rows["hanwha_ocean_us_shipbuilding_sanction_case"]["price_validation_status"],
            "needs_source_date_backfill",
        )
        self.assertEqual(rows["hanwha_vatn_underwater_drone_case"]["target_id"], "DEFENSE_UNMANNED_NAVAL_SYSTEMS")
        self.assertEqual(rows["hanwha_vatn_underwater_drone_case"]["stage1_date"], "2025-12-10")
        self.assertEqual(rows["hyundai_rotem_morocco_rail_case"]["stage2_date"], "2025-02-26")
        self.assertEqual(rows["meta_constellation_existing_nuclear_ppa_case"]["target_id"], "NUCLEAR_EXISTING_PPA_RESTART")
        self.assertEqual(rows["constellation_tmi_microsoft_restart_case"]["target_id"], "NUCLEAR_EXISTING_PPA_RESTART")
        self.assertEqual(rows["constellation_tmi_microsoft_restart_case"]["stage2_date"], "2026-05-11")
        self.assertEqual(rows["nuscale_uamps_smr_cancel_case"]["stage4c_date"], "2023-11-01")
        self.assertEqual(rows["ukraine_reconstruction_policy_case"]["case_type"], "event_premium")
        self.assertEqual(rows["neom_city_policy_case"]["case_type"], "event_premium")

    def test_case_records_validate_and_keep_loop5_guardrails(self):
        records = round93_case_records()

        self.assertEqual(len(records), len(ROUND93_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "INDUSTRIAL_ORDERS_INFRA")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("require_contract_quality_delivery_margin_eps_revision_fcf_for_green", record.green_guardrails)
            self.assertIn("do_not_invent_contract_dates_prices_margins_or_counterparties", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["hanwha_aerospace_dilution_case"].score_price_alignment, "evidence_good_but_price_failed")
        self.assertEqual(by_id["nuscale_uamps_smr_cancel_case"].rerating_result, "thesis_break")
        self.assertIn("project_withdrawal", by_id["perth_data_center_withdrawal_case"].red_flag_fields)
        self.assertIn("moratorium", by_id["seattle_indianapolis_data_center_moratorium_case"].red_flag_fields)

    def test_score_profile_rows_mark_no_production_change_and_include_loop5_penalties(self):
        rows = round93_score_profile_rows()

        self.assertEqual(len(rows), len(ROUND93_SCORE_TARGETS))
        for row in rows:
            self.assertEqual(row["large_sector"], "INDUSTRIAL_ORDERS_INFRA")
            self.assertEqual(row["production_scoring_changed"], "false")
            self.assertIn("loop5_penalty_axes", row)
        by_target = {row["target_id"]: row for row in rows}
        self.assertEqual(by_target["GRID_TRANSFORMER_SHORTAGE"]["eps_fcf"], "24")
        self.assertIn("low_margin_long_term_contract", by_target["GRID_TRANSFORMER_SHORTAGE"]["loop5_penalty_axes"])
        self.assertIn("slot_cancelled", by_target["GRID_SUPPLY_SLOT_PREBUY"]["loop5_penalty_axes"])
        self.assertIn("capa_normalization", by_target["GRID_MEDIUM_VOLTAGE_EXPANSION"]["loop5_penalty_axes"])
        self.assertIn("wind_segment_loss", by_target["GAS_TURBINE_POWER_BACKLOG"]["loop5_penalty_axes"])
        self.assertIn("moratorium", by_target["DATA_CENTER_GRID_PERMITTING_OVERLAY"]["loop5_penalty_axes"])
        self.assertEqual(by_target["DEFENSE_CAPITAL_ALLOCATION_SHOCK"]["hard_gate"], "true")
        self.assertEqual(by_target["CAPITAL_ALLOCATION_DILUTION_OVERLAY"]["hard_gate"], "true")
        self.assertEqual(by_target["DISCLOSURE_CONFIDENCE_CAP"]["eps_fcf"], "cap")
        self.assertEqual(by_target["NUCLEAR_SMR_GRID_POLICY"]["posture"], "REDTEAM_FIRST")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round93_stage_date_rows()}
        fields = {row["field"] for row in round93_price_field_rows()}

        self.assertIn("fy1_fy2_fy3_revision", rows["GRID_TRANSFORMER_SHORTAGE"]["stage3"])
        self.assertIn("slot_based_long_term_agreement", rows["GRID_SUPPLY_SLOT_PREBUY"]["stage2"])
        self.assertIn("medium_voltage_order", rows["GRID_MEDIUM_VOLTAGE_EXPANSION"]["stage2"])
        self.assertIn("gas_turbine_backlog", rows["GAS_TURBINE_POWER_BACKLOG"]["stage2"])
        self.assertIn("moratorium", rows["DATA_CENTER_GRID_PERMITTING_OVERLAY"]["stage4c"])
        self.assertIn("detail_missing", rows["DISCLOSURE_CONFIDENCE_CAP"]["stage4c"])
        self.assertIn("signed_ppa", rows["NUCLEAR_EXISTING_PPA_RESTART"]["stage2"])
        self.assertIn("project_cancelled", rows["NUCLEAR_SMR_GRID_POLICY"]["stage4c"])
        for field in (
            "contract_value_to_sales",
            "counterparty",
            "delivery_schedule",
            "transformer_lead_time_months",
            "transformer_voltage_kv",
            "korea_export_flag",
            "goes_cost_change",
            "copper_cost_change",
            "medium_voltage_order",
            "switchgear_order",
            "data_center_orders",
            "gas_turbine_backlog_gw",
            "gas_turbine_slot_reservation_gw",
            "power_equipment_backlog",
            "storage_equipment_order",
            "electrification_profit_growth",
            "wind_segment_loss",
            "tariff_cost_amount",
            "moratorium_flag",
            "water_permitting_delay_flag",
            "diesel_generator_noise_flag",
            "defense_backlog",
            "local_content_requirement",
            "technology_transfer_flag",
            "dilution_flag",
            "local_factory_capex_flag",
            "unmanned_system_contract_flag",
            "geopolitical_sanction_flag",
            "naval_mro_contract_flag",
            "rail_financing_secured_flag",
            "nuclear_ppa_flag",
            "nuclear_restart_flag",
            "grid_injection_rights_flag",
            "smr_cost_overrun_flag",
            "reconstruction_contract_flag",
            "opendart_detail_fetched_flag",
            "disclosure_confidence_score",
            "detail_parser_confidence",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND93_PRICE_FIELDS))

    def test_summary_and_markdown_explain_loop5_guardrails(self):
        summary = round93_summary()
        summary_md = render_round93_summary_markdown()
        guardrails = render_round93_green_guardrail_markdown()
        overlays = render_round93_loop5_risk_overlay_markdown()
        price_plan = render_round93_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 19)
        self.assertEqual(summary["case_candidate_count"], 19)
        self.assertEqual(summary["structural_success_count"], 1)
        self.assertEqual(summary["success_candidate_count"], 10)
        self.assertEqual(summary["cyclical_success_count"], 0)
        self.assertEqual(summary["event_premium_count"], 2)
        self.assertEqual(summary["failed_rerating_count"], 1)
        self.assertEqual(summary["stage4b_case_count"], 3)
        self.assertEqual(summary["stage4c_case_count"], 3)
        self.assertEqual(summary["hard_gate_target_count"], 3)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R1 Loop 5", summary_md)
        self.assertIn("Do not apply R1 Loop-5 v5.0 weights", guardrails)
        self.assertIn("NAVAL_MRO_OPTION_ONLY", overlays)
        self.assertIn("GRID_SLOT_VISIBILITY", overlays)
        self.assertIn("DISCLOSURE_CONFIDENCE_CAPPED", price_plan)
        self.assertIn("SMR_POLICY_FALSE_GREEN", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round93_r1_loop5_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r1_loop5_round93.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round93_r1_loop5_v5.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["stage_date_plan"].exists())
            self.assertTrue(paths["green_guardrails"].exists())
            self.assertTrue(paths["loop5_risk_overlays"].exists())
            self.assertTrue(paths["price_validation_plan"].exists())
            self.assertTrue(paths["price_fields"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND93_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round93_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round93_r1_loop5_industrial_infra", text)


if __name__ == "__main__":
    unittest.main()
