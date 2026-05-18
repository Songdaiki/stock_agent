from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from e2r.cli.build_round190_r6_loop12_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round190_r6_loop12_financial_capital_digital import (
    ROUND190_SOURCE_CANONICAL_TARGET_IDS,
    render_round190_green_guardrail_markdown,
    render_round190_price_validation_plan_markdown,
    render_round190_risk_overlay_markdown,
    render_round190_score_stage_price_alignment_markdown,
    render_round190_summary_markdown,
    round190_base_score_weight_rows,
    round190_case_candidate_rows,
    round190_case_records,
    round190_price_field_rows,
    round190_score_profile_rows,
    round190_score_stage_price_alignment_rows,
    round190_stage_cap_rows,
    round190_stage_date_rows,
    round190_summary,
    round190_target_for,
    write_round190_r6_loop12_reports,
)


class Round190R6Loop12FinancialCapitalDigitalTests(unittest.TestCase):
    def test_round190_targets_cover_loop12_archetypes(self):
        self.assertEqual(len(ROUND190_SOURCE_CANONICAL_TARGET_IDS), 11)
        rows = round190_score_profile_rows()
        self.assertEqual(len(rows), 11)
        self.assertEqual({row["target_id"] for row in rows}, set(ROUND190_SOURCE_CANONICAL_TARGET_IDS))
        self.assertEqual({row["large_sector"] for row in rows}, {Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL.value})
        self.assertEqual({row["production_scoring_changed"] for row in rows}, {"false"})

        for target_id in ROUND190_SOURCE_CANONICAL_TARGET_IDS:
            self.assertTrue(hasattr(E2RArchetype, target_id))

    def test_base_weights_and_stage_caps_match_round190_note(self):
        weights = {row["component"]: row for row in round190_base_score_weight_rows()}
        self.assertEqual(weights["roe_eps_fcf_durability"]["points"], "22")
        self.assertEqual(weights["capital_return_execution"]["points"], "18")
        self.assertEqual(weights["capital_ratio_credit_cost_stability"]["points"], "16")
        self.assertEqual(weights["digital_finance_revenue_model_visibility"]["points"], "16")
        self.assertEqual(weights["early_price_validation"]["points"], "10")
        self.assertEqual(weights["security_privacy_policy_redteam"]["points"], "12")
        self.assertEqual(weights["valuation_4b_room"]["points"], "6")

        caps = {row["stage_band"]: row for row in round190_stage_cap_rows()}
        self.assertEqual(caps["Stage 3"]["max_score"], "requires_6_of_9")
        self.assertIn("actual_buyback_cancel_or_dividend_expansion_executed", caps["Stage 3"]["required_evidence"])
        self.assertIn("digital_take_rate_issuance_or_equity_method_income_confirmed", caps["Stage 3"]["required_evidence"])
        self.assertEqual(caps["Stage 4B"]["max_score"], "requires_4_of_6")
        self.assertIn("pbr_rerating_ahead_of_roe_eps", caps["Stage 4B"]["required_evidence"])
        self.assertEqual(caps["Stage 4C"]["max_score"], "hard_gate")
        self.assertIn("privacy_or_biometric_data_leak", caps["Stage 4C"]["required_evidence"])

    def test_round190_target_rules_are_specific(self):
        samsung_life = round190_target_for("INSURANCE_NAV_VALUEUP_SAMSUNG_ELECTRONICS_STAKE")
        self.assertIsNotNone(samsung_life)
        assert samsung_life is not None
        self.assertEqual(samsung_life.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("k_ics_csm_stable", samsung_life.green_conditions)
        self.assertIn("return_execution_missing", samsung_life.red_flags)

        meritz = round190_target_for("SHAREHOLDER_RETURN_COMPOUNDING_FINANCIAL_HOLDCO")
        self.assertIsNotNone(meritz)
        assert meritz is not None
        self.assertEqual(meritz.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("repeat_buyback_cancel", meritz.green_conditions)

        stablecoin = round190_target_for("KRW_STABLECOIN_POLICY_THEME")
        self.assertIsNotNone(stablecoin)
        assert stablecoin is not None
        self.assertEqual(stablecoin.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("issuer_economics_missing", stablecoin.red_flags)

        privacy = round190_target_for("PAYMENT_PRIVACY_REGULATORY_4C")
        buyback = round190_target_for("BUYBACK_EXECUTION_PRICE_FAILED")
        policy = round190_target_for("POLICY_TAX_REVERSAL_MARKET_SHOCK")
        self.assertTrue(privacy and privacy.hard_gate)
        self.assertTrue(buyback and buyback.hard_gate)
        self.assertTrue(policy and policy.hard_gate)

    def test_required_round190_cases_are_present(self):
        rows = {row["case_id"]: row for row in round190_case_candidate_rows()}
        required = {
            "samsung_life_insurance_nav_valueup_stage23_case",
            "meritz_financial_shareholder_return_stage23_case",
            "hana_financial_dunamu_equity_option_stage2_case",
            "toss_facepay_payment_biometric_stage2_case",
            "nice_credit_information_recurring_data_stage23_case",
            "krw_stablecoin_policy_theme_4b_watch_case",
            "kakaopay_privacy_regulatory_4c_watch_case",
            "samsung_electronics_buyback_execution_price_failed_case",
            "policy_tax_reversal_market_shock_4c_watch_case",
            "securities_brokerage_market_beta_cycle_case",
            "stablecoin_related_stock_price_only_rally_case",
            "digital_asset_exchange_security_incident_4c_reference_case",
            "r6_loop12_disclosure_confidence_reference_case",
        }
        self.assertTrue(required.issubset(rows))
        self.assertEqual(rows["krw_stablecoin_policy_theme_4b_watch_case"]["case_type"], "4b_watch")
        self.assertEqual(rows["kakaopay_privacy_regulatory_4c_watch_case"]["case_type"], "4c_thesis_break")
        self.assertEqual(rows["securities_brokerage_market_beta_cycle_case"]["case_type"], "cyclical_success")
        self.assertEqual({row["production_input"] for row in rows.values()}, {"false"})

    def test_case_records_validate_and_keep_green_guardrails(self):
        records = round190_case_records()
        self.assertEqual(len(records), 13)
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL.value)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("stage3_early_catch_requires_6_of_9_loop12_conditions", record.green_guardrails)
            self.assertIn("low_pbr_valueup_stablecoin_dunamu_facepay_or_buyback_headline_is_not_structural_evidence", record.green_guardrails)
            self.assertIn("require_roe_capital_ratio_actual_return_revenue_model_security_and_price_path_for_green", record.green_guardrails)

        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["krw_stablecoin_policy_theme_4b_watch_case"].rerating_result, "theme_overheat")
        self.assertEqual(by_id["stablecoin_related_stock_price_only_rally_case"].score_price_alignment, "price_moved_without_evidence")
        self.assertEqual(by_id["kakaopay_privacy_regulatory_4c_watch_case"].score_price_alignment, "false_positive_score")
        self.assertEqual(by_id["policy_tax_reversal_market_shock_4c_watch_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["samsung_electronics_buyback_execution_price_failed_case"].score_price_alignment, "evidence_good_but_price_failed")
        self.assertEqual(by_id["securities_brokerage_market_beta_cycle_case"].rerating_result, "cyclical_rerating")

    def test_stage_price_and_alignment_rows_cover_round190_fields(self):
        stage_rows = {row["target_id"]: row for row in round190_stage_date_rows()}
        self.assertEqual(stage_rows["PAYMENT_PRIVACY_REGULATORY_4C"]["hard_gate"], "true")
        self.assertIn("platform_trust_damage", stage_rows["PAYMENT_PRIVACY_REGULATORY_4C"]["red_flags"])
        self.assertIn("same_day_price_drop", stage_rows["BUYBACK_EXECUTION_PRICE_FAILED"]["stage4c"])

        price_fields = {row["field"] for row in round190_price_field_rows()}
        for field in {
            "relative_strength_vs_fintech_basket",
            "k_ics_ratio",
            "csm",
            "digital_asset_stake_value",
            "stablecoin_issuance_volume",
            "reserve_income",
            "merchant_count",
            "user_count",
            "privacy_fine_flag",
            "biometric_data_risk_flag",
            "tax_policy_shock_flag",
        }:
            self.assertIn(field, price_fields)

        alignment_rows = {row["case_id"]: row for row in round190_score_stage_price_alignment_rows()}
        self.assertEqual(alignment_rows["krw_stablecoin_policy_theme_4b_watch_case"]["detected_stage"], "Stage 2 -> 4B-watch")
        self.assertIn("price-only", alignment_rows["stablecoin_related_stock_price_only_rally_case"]["price_path_status"])

    def test_summary_and_markdown_outputs(self):
        summary = round190_summary()
        self.assertEqual(summary["target_count"], 11)
        self.assertEqual(summary["source_canonical_target_count"], 11)
        self.assertEqual(summary["case_candidate_count"], 13)
        self.assertEqual(summary["success_candidate_count"], 5)
        self.assertEqual(summary["cyclical_success_count"], 1)
        self.assertEqual(summary["failed_rerating_count"], 2)
        self.assertEqual(summary["stage4b_case_count"], 2)
        self.assertEqual(summary["stage4c_case_count"], 3)
        self.assertEqual(summary["hard_gate_target_count"], 3)
        self.assertFalse(summary["production_scoring_changed"])

        summary_md = render_round190_summary_markdown()
        guardrails = render_round190_green_guardrail_markdown()
        overlays = render_round190_risk_overlay_markdown()
        price_plan = render_round190_price_validation_plan_markdown()
        alignment = render_round190_score_stage_price_alignment_markdown()
        self.assertIn("R6 Loop 12", summary_md)
        self.assertIn("production_scoring_changed: false", summary_md)
        self.assertIn("at least 6 of 9 checks", guardrails)
        self.assertIn("PAYMENT_PRIVACY_REGULATORY_4C", overlays)
        self.assertIn("Required Fields", price_plan)
        self.assertIn("Samsung Life", alignment)

    def test_writer_and_cli_parse_args(self):
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--score-profiles", "profiles.csv"])
        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.score_profiles, "profiles.csv")

        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round190_r6_loop12_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r6_loop12_round190.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round190_r6_loop12_v12.csv",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)
            self.assertIn("R6 Loop 12", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("stage3_early_catch_requires_6_of_9_loop12_conditions", paths["cases"].read_text(encoding="utf-8"))
            self.assertIn("PAYMENT_PRIVACY_REGULATORY_4C", paths["score_profiles"].read_text(encoding="utf-8"))

    def test_production_scoring_modules_do_not_import_round190_pack(self):
        forbidden = "round190_r6_loop12_financial_capital_digital"
        for relative in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
            "src/e2r/backtest/asof_research_replay.py",
        ):
            text = Path(relative).read_text(encoding="utf-8")
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
