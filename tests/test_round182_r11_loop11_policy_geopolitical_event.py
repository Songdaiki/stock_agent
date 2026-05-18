import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round182_r11_loop11_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round182_r11_loop11_policy_geopolitical_event import (
    ROUND182_BASE_SCORE_WEIGHTS,
    ROUND182_CASE_CANDIDATES,
    ROUND182_PRICE_FIELDS,
    ROUND182_SCORE_STAGE_PRICE_ALIGNMENT,
    ROUND182_SCORE_TARGETS,
    ROUND182_SOURCE_CANONICAL_TARGET_COUNT,
    ROUND182_SOURCE_CANONICAL_TARGET_IDS,
    ROUND182_STAGE_CAPS,
    render_round182_green_guardrail_markdown,
    render_round182_price_validation_plan_markdown,
    render_round182_risk_overlay_markdown,
    render_round182_score_stage_price_alignment_markdown,
    render_round182_summary_markdown,
    round182_base_score_weight_rows,
    round182_case_candidate_rows,
    round182_case_records,
    round182_price_field_rows,
    round182_score_profile_rows,
    round182_score_stage_price_alignment_rows,
    round182_stage_cap_rows,
    round182_stage_date_rows,
    round182_summary,
    round182_target_for,
    write_round182_r11_loop11_reports,
)


class Round182R11Loop11PolicyGeopoliticalEventTests(unittest.TestCase):
    def test_round182_targets_cover_source_archetypes(self):
        labels = {target.target_id for target in ROUND182_SCORE_TARGETS}

        self.assertEqual(ROUND182_SOURCE_CANONICAL_TARGET_COUNT, 10)
        self.assertEqual(len(labels), 10)
        self.assertEqual(set(ROUND182_SOURCE_CANONICAL_TARGET_IDS), labels)
        for target in ROUND182_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.POLICY_GEOPOLITICAL_EVENT)
            self.assertFalse(target.production_scoring_changed)

    def test_new_r11_loop11_korea_event_archetypes_exist(self):
        expected = (
            E2RArchetype.DOMESTIC_RESOURCE_DISCOVERY_EVENT,
            E2RArchetype.RESOURCE_EXPLORATION_DRILL_BIT_GATE,
            E2RArchetype.ENERGY_SECURITY_POLICY_EVENT,
            E2RArchetype.MARKET_STRUCTURE_SHORT_SELLING_POLICY,
            E2RArchetype.SHORT_SELLING_RESUMPTION_RISK,
            E2RArchetype.POLITICAL_SYSTEM_SHOCK_KOREA,
            E2RArchetype.GEOPOLITICAL_ENERGY_IMPORT_SHOCK,
            E2RArchetype.EVENT_PRICE_RALLY_NOT_STAGE3,
            E2RArchetype.POLICY_DIRECTIONALITY_ERROR,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_loop11_base_score_weights_and_stage_caps_match_round_note(self):
        weights = {row["component"]: row for row in round182_base_score_weight_rows()}
        caps = {row["stage_band"]: row for row in round182_stage_cap_rows()}

        self.assertEqual(len(ROUND182_BASE_SCORE_WEIGHTS), 7)
        self.assertEqual(weights["contract_budget_order_exploration_visibility"]["points"], "26")
        self.assertEqual(weights["eps_fcf_revenue_guidance_conversion"]["points"], "18")
        self.assertEqual(weights["price_path_event_detection"]["points"], "14")
        self.assertEqual(weights["recurrence_durability"]["points"], "12")
        self.assertEqual(weights["redteam_disclosure_confidence"]["points"], "14")
        self.assertEqual(weights["policy_directionality"]["points"], "8")
        self.assertEqual(weights["valuation_room_4b_runway"]["points"], "8")
        self.assertEqual(len(ROUND182_STAGE_CAPS), 5)
        self.assertEqual(caps["Stage 1"]["max_score"], "45")
        self.assertEqual(caps["Stage 2"]["max_score"], "70")
        self.assertIn("requires_5_of_8", caps["Stage 3"]["max_score"])
        self.assertIn("contract_budget_order_or_commercial_exploration_result", caps["Stage 3"]["required_evidence"])
        self.assertIn("requires_3_of_5", caps["Stage 4B"]["max_score"])
        self.assertIn("political_system_shock", caps["Stage 4C"]["required_evidence"])

    def test_target_rules_separate_event_price_from_stage3(self):
        resource = round182_target_for("DOMESTIC_RESOURCE_DISCOVERY_EVENT")
        drill_bit = round182_target_for("RESOURCE_EXPLORATION_DRILL_BIT_GATE")
        energy = round182_target_for("ENERGY_SECURITY_POLICY_EVENT")
        short_policy = round182_target_for("MARKET_STRUCTURE_SHORT_SELLING_POLICY")
        short_risk = round182_target_for("SHORT_SELLING_RESUMPTION_RISK")
        political = round182_target_for("POLITICAL_SYSTEM_SHOCK_KOREA")
        hormuz = round182_target_for("GEOPOLITICAL_ENERGY_IMPORT_SHOCK")
        event_price = round182_target_for("EVENT_PRICE_RALLY_NOT_STAGE3")
        directionality = round182_target_for("POLICY_DIRECTIONALITY_ERROR")
        disclosure = round182_target_for("DISCLOSURE_CONFIDENCE_CAP")

        for target in (resource, drill_bit, energy, short_policy, short_risk, political, hormuz, event_price, directionality, disclosure):
            self.assertIsNotNone(target)
        assert resource is not None
        assert drill_bit is not None
        assert energy is not None
        assert short_policy is not None
        assert short_risk is not None
        assert political is not None
        assert hormuz is not None
        assert event_price is not None
        assert directionality is not None
        assert disclosure is not None
        self.assertEqual(resource.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("commercial_discovery", resource.green_conditions)
        self.assertTrue(drill_bit.gate_only)
        self.assertIn("80pct_failure_probability", drill_bit.red_flags)
        self.assertEqual(energy.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertEqual(short_policy.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertTrue(short_risk.gate_only)
        self.assertTrue(political.gate_only)
        self.assertTrue(hormuz.gate_only)
        self.assertTrue(event_price.gate_only)
        self.assertTrue(directionality.gate_only)
        self.assertEqual(disclosure.score_weight.contract_budget_order_exploration_visibility, "cap")

    def test_required_round182_cases_are_present_with_stage_markers(self):
        rows = {row["case_id"]: row for row in round182_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND182_CASE_CANDIDATES))
        self.assertEqual(rows["korea_east_sea_gas_discovery_stage1_4b_watch_case"]["stage1_date"], "2024-06-03")
        self.assertEqual(rows["korea_east_sea_gas_discovery_stage1_4b_watch_case"]["stage4b_date"], "2024-06-03")
        self.assertIn("kogas_plus_30pct", rows["korea_east_sea_gas_discovery_stage1_4b_watch_case"]["evidence_fields"])
        self.assertEqual(rows["korea_gas_daewang_whale_drill_bit_gate_case"]["stage1_date"], "2024-06-07")
        self.assertEqual(rows["short_selling_ban_extension_policy_overlay_case"]["stage1_date"], "2024-04-25")
        self.assertEqual(rows["short_selling_ban_extension_policy_overlay_case"]["stage2_date"], "2024-06-13")
        self.assertEqual(rows["political_system_shock_martial_law_case"]["stage4c_date"], "2024-12-03")
        self.assertEqual(rows["hormuz_middle_east_energy_import_shock_case"]["stage4c_date"], "2026-03-04")
        self.assertEqual(rows["brokerage_short_selling_fines_market_trust_case"]["stage2_date"], "2025-02-13")
        self.assertEqual(rows["r11_disclosure_confidence_cap_case"]["target_id"], "DISCLOSURE_CONFIDENCE_CAP")

    def test_case_records_validate_and_keep_round182_guardrails(self):
        records = round182_case_records()

        self.assertEqual(len(records), len(ROUND182_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "POLICY_GEOPOLITICAL_EVENT")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("event_news_is_not_green_evidence_alone", record.green_guardrails)
            self.assertIn("contract_budget_order_exploration_revenue_or_eps_required", record.green_guardrails)
            self.assertIn("stage3_early_catch_requires_5_of_8_loop11_conditions", record.green_guardrails)
            self.assertIn("do_not_invent_contracts_budgets_orders_exploration_results_guidance_stage_prices_or_mfe_mae", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertIn(E2RArchetype.EVENT_PRICE_RALLY_NOT_STAGE3, by_id["korea_east_sea_gas_discovery_stage1_4b_watch_case"].secondary_archetypes)
        self.assertEqual(by_id["korea_east_sea_gas_discovery_stage1_4b_watch_case"].score_price_alignment, "price_moved_without_evidence")
        self.assertEqual(by_id["political_system_shock_martial_law_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["hormuz_middle_east_energy_import_shock_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["short_selling_resumption_high_beta_4b_watch_case"].rerating_result, "theme_overheat")
        self.assertEqual(by_id["brokerage_short_selling_fines_market_trust_case"].score_price_alignment, "evidence_good_but_price_failed")

    def test_score_profile_rows_mark_no_production_change(self):
        rows = round182_score_profile_rows()

        self.assertEqual(len(rows), len(ROUND182_SCORE_TARGETS))
        for row in rows:
            self.assertEqual(row["large_sector"], "POLICY_GEOPOLITICAL_EVENT")
            self.assertEqual(row["production_scoring_changed"], "false")
            self.assertIn("loop11_penalty_axes", row)
        by_target = {row["target_id"]: row for row in rows}
        self.assertEqual(by_target["DOMESTIC_RESOURCE_DISCOVERY_EVENT"]["price_path_event_detection"], "18")
        self.assertEqual(by_target["MARKET_STRUCTURE_SHORT_SELLING_POLICY"]["policy_directionality"], "18")
        self.assertEqual(by_target["RESOURCE_EXPLORATION_DRILL_BIT_GATE"]["contract_budget_order_exploration_visibility"], "gate")
        self.assertEqual(by_target["POLITICAL_SYSTEM_SHOCK_KOREA"]["gate_only"], "true")
        self.assertEqual(by_target["GEOPOLITICAL_ENERGY_IMPORT_SHOCK"]["gate_only"], "true")
        self.assertEqual(by_target["DISCLOSURE_CONFIDENCE_CAP"]["redteam_disclosure_confidence"], "+")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round182_stage_date_rows()}
        fields = {row["field"] for row in round182_price_field_rows()}

        self.assertIn("commercial_discovery", rows["DOMESTIC_RESOURCE_DISCOVERY_EVENT"]["stage3"])
        self.assertIn("80pct_failure_probability", rows["RESOURCE_EXPLORATION_DRILL_BIT_GATE"]["stage4c"])
        self.assertIn("brokerage_revenue_or_roe_link", rows["MARKET_STRUCTURE_SHORT_SELLING_POLICY"]["stage3"])
        self.assertIn("short_selling_resumption", rows["SHORT_SELLING_RESUMPTION_RISK"]["stage4c"])
        self.assertIn("market_wide_risk_premium_spike", rows["POLITICAL_SYSTEM_SHOCK_KOREA"]["stage4c"])
        self.assertIn("market_circuit_breaker", rows["GEOPOLITICAL_ENERGY_IMPORT_SHOCK"]["stage4c"])
        self.assertIn("price_rally_before_cashflow", rows["EVENT_PRICE_RALLY_NOT_STAGE3"]["stage4b"])
        for field in (
            "event_type",
            "event_date",
            "price_at_event",
            "return_1d_after_event",
            "return_5d_after_event",
            "mfe_5d_after_event",
            "mae_5d_after_event",
            "relative_strength_vs_kospi",
            "market_wide_shock_flag",
            "daily_limit_flag",
            "volume_spike_flag",
            "contract_or_budget_confirmed",
            "government_order_flag",
            "exploration_result_flag",
            "commerciality_confirmed_flag",
            "guidance_raised_flag",
            "policy_reversal_risk",
            "drill_bit_gate",
            "resource_success_probability",
            "market_structure_event_flag",
            "short_selling_resumption_flag",
            "political_risk_flag",
            "geopolitical_energy_shock_flag",
        ):
            self.assertIn(field, fields)
        self.assertEqual(len(fields), len(ROUND182_PRICE_FIELDS))

    def test_score_stage_price_alignment_rows_and_markdown(self):
        rows = {row["case_id"]: row for row in round182_score_stage_price_alignment_rows()}
        markdown = render_round182_score_stage_price_alignment_markdown()

        self.assertEqual(len(rows), len(ROUND182_SCORE_STAGE_PRICE_ALIGNMENT))
        self.assertEqual(rows["korea_east_sea_gas_discovery_stage1_4b_watch_case"]["verdict"], "resource_event_rally_not_stage3")
        self.assertEqual(rows["political_system_shock_martial_law_case"]["verdict"], "political_shock_hard_overlay")
        self.assertEqual(rows["hormuz_middle_east_energy_import_shock_case"]["verdict"], "energy_import_shock_hard_overlay")
        self.assertIn("KOGAS", markdown)
        self.assertIn("Martial-law", markdown)
        self.assertIn("Hormuz", markdown)

    def test_summary_and_markdown_explain_r11_loop11_guardrails(self):
        summary = round182_summary()
        summary_md = render_round182_summary_markdown()
        guardrails = render_round182_green_guardrail_markdown()
        overlays = render_round182_risk_overlay_markdown()
        price_plan = render_round182_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 10)
        self.assertEqual(summary["source_canonical_target_count"], 10)
        self.assertEqual(summary["case_candidate_count"], len(ROUND182_CASE_CANDIDATES))
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["case_records_are_candidate_generation_input"])
        self.assertIn("KOGAS", summary_md)
        self.assertIn("short-selling", summary_md)
        self.assertIn("policy announcement", guardrails)
        self.assertIn("drill-bit", overlays)
        self.assertIn("event_date", price_plan)
        self.assertIn("korea_east_sea_gas_discovery_stage1_4b_watch_case", price_plan)

    def test_reports_are_written_and_case_jsonl_loads(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round182_r11_loop11_reports(
                output_directory=root / "reports",
                cases_path=root / "cases.jsonl",
                score_profile_path=root / "score_profiles.csv",
            )
            records = load_case_library(paths["cases"])

            self.assertEqual(len(records), len(ROUND182_CASE_CANDIDATES))
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["stage_date_plan"].exists())
            self.assertTrue(paths["price_fields"].exists())
            self.assertIn("KOGAS", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("event_news_is_not_green_evidence_alone", paths["cases"].read_text(encoding="utf-8"))

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

    def test_production_modules_do_not_import_round182(self):
        forbidden = "round182_r11_loop11_policy_geopolitical_event"
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
