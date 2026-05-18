import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round177_r6_loop11_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round177_r6_loop11_financial_capital_digital import (
    ROUND177_BASE_SCORE_WEIGHTS,
    ROUND177_CASE_CANDIDATES,
    ROUND177_PRICE_FIELDS,
    ROUND177_SCORE_STAGE_PRICE_ALIGNMENT,
    ROUND177_SCORE_TARGETS,
    ROUND177_SOURCE_CANONICAL_TARGET_COUNT,
    ROUND177_SOURCE_CANONICAL_TARGET_IDS,
    ROUND177_STAGE_CAPS,
    render_round177_green_guardrail_markdown,
    render_round177_price_validation_plan_markdown,
    render_round177_risk_overlay_markdown,
    render_round177_score_stage_price_alignment_markdown,
    render_round177_summary_markdown,
    round177_base_score_weight_rows,
    round177_case_candidate_rows,
    round177_case_records,
    round177_price_field_rows,
    round177_score_profile_rows,
    round177_score_stage_price_alignment_rows,
    round177_stage_cap_rows,
    round177_stage_date_rows,
    round177_summary,
    round177_target_for,
    write_round177_r6_loop11_reports,
)


class Round177R6Loop11FinancialCapitalDigitalTests(unittest.TestCase):
    def test_round177_targets_cover_source_and_crowding_overlay(self):
        labels = {target.target_id for target in ROUND177_SCORE_TARGETS}

        self.assertEqual(ROUND177_SOURCE_CANONICAL_TARGET_COUNT, 14)
        self.assertEqual(len(labels), 15)
        self.assertTrue(set(ROUND177_SOURCE_CANONICAL_TARGET_IDS).issubset(labels))
        self.assertIn("VALUE_UP_CROWDED_4B_WATCH", labels)
        for target in ROUND177_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL)
            self.assertFalse(target.production_scoring_changed)

    def test_new_r6_loop11_financial_archetypes_exist(self):
        expected = (
            E2RArchetype.BANK_HOLDING_VALUEUP_CAPITAL_RETURN_KOREA,
            E2RArchetype.BANK_ROE_PBR_RERATING_KOREA,
            E2RArchetype.REGIONAL_BANK_HIGH_ROE_VALUEUP,
            E2RArchetype.INSURANCE_CAPITAL_RELEASE_VALUEUP_KOREA,
            E2RArchetype.INSURANCE_KICS_CSM_GATE,
            E2RArchetype.SECURITIES_BROKERAGE_MARKET_BETA,
            E2RArchetype.SECURITIES_IB_PF_RISK_OVERLAY,
            E2RArchetype.INTERNET_BANK_PROFITABILITY,
            E2RArchetype.DIGITAL_ASSET_EXCHANGE_EQUITY_OPTION,
            E2RArchetype.FINTECH_SUPERAPP_IPO_OPTION_KOREA,
            E2RArchetype.KRW_STABLECOIN_POLICY_OPTION,
            E2RArchetype.GUARANTEE_INSURANCE_IPO_SECURITY_RISK,
            E2RArchetype.VALUE_UP_CROWDED_4B_WATCH,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_loop11_base_score_weights_and_stage_caps_match_round_note(self):
        weights = {row["component"]: row for row in round177_base_score_weight_rows()}
        caps = {row["stage_band"]: row for row in round177_stage_cap_rows()}

        self.assertEqual(len(ROUND177_BASE_SCORE_WEIGHTS), 7)
        self.assertEqual(weights["roe_eps_fcf_durability"]["points"], "22")
        self.assertEqual(weights["capital_return_execution"]["points"], "18")
        self.assertEqual(weights["capital_ratio_credit_cost_stability"]["points"], "18")
        self.assertEqual(weights["regulatory_revenue_model_visibility"]["points"], "14")
        self.assertEqual(weights["early_price_path_validation"]["points"], "10")
        self.assertEqual(weights["governance_disclosure_confidence"]["points"], "10")
        self.assertEqual(weights["valuation_room_4b_runway"]["points"], "8")
        self.assertEqual(len(ROUND177_STAGE_CAPS), 5)
        self.assertEqual(caps["Stage 1"]["max_score"], "45")
        self.assertEqual(caps["Stage 2"]["max_score"], "70")
        self.assertIn("requires_5_of_8", caps["Stage 3"]["max_score"])
        self.assertIn("stage2_60d_mfe_20pct", caps["Stage 3"]["required_evidence"])
        self.assertIn("requires_3_of_5", caps["Stage 4B"]["max_score"])
        self.assertIn("ransomware_financial_service_disruption", caps["Stage 4C"]["required_evidence"])

    def test_target_rules_separate_banks_insurance_cycles_and_digital_gates(self):
        bank = round177_target_for("BANK_HOLDING_VALUEUP_CAPITAL_RETURN_KOREA")
        bank_rerating = round177_target_for("BANK_ROE_PBR_RERATING_KOREA")
        pf = round177_target_for("BANK_CREDIT_COST_PF_OVERLAY")
        regional = round177_target_for("REGIONAL_BANK_HIGH_ROE_VALUEUP")
        insurance = round177_target_for("INSURANCE_CAPITAL_RELEASE_VALUEUP_KOREA")
        kics = round177_target_for("INSURANCE_KICS_CSM_GATE")
        securities = round177_target_for("SECURITIES_BROKERAGE_MARKET_BETA")
        ib_pf = round177_target_for("SECURITIES_IB_PF_RISK_OVERLAY")
        internet_bank = round177_target_for("INTERNET_BANK_PROFITABILITY")
        digital = round177_target_for("DIGITAL_ASSET_EXCHANGE_EQUITY_OPTION")
        toss = round177_target_for("FINTECH_SUPERAPP_IPO_OPTION_KOREA")
        stablecoin = round177_target_for("KRW_STABLECOIN_POLICY_OPTION")
        guarantee = round177_target_for("GUARANTEE_INSURANCE_IPO_SECURITY_RISK")
        disclosure = round177_target_for("DISCLOSURE_CONFIDENCE_CAP")
        crowded = round177_target_for("VALUE_UP_CROWDED_4B_WATCH")

        for target in (bank, bank_rerating, pf, regional, insurance, kics, securities, ib_pf, internet_bank, digital, toss, stablecoin, guarantee, disclosure, crowded):
            self.assertIsNotNone(target)
        assert bank is not None
        assert bank_rerating is not None
        assert pf is not None
        assert regional is not None
        assert insurance is not None
        assert kics is not None
        assert securities is not None
        assert ib_pf is not None
        assert internet_bank is not None
        assert digital is not None
        assert toss is not None
        assert stablecoin is not None
        assert guarantee is not None
        assert disclosure is not None
        assert crowded is not None
        self.assertEqual(bank.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("cet1_ratio", bank.green_conditions)
        self.assertIn("pbr_band_change", bank_rerating.green_conditions)
        self.assertTrue(pf.hard_gate)
        self.assertIn("pf_credit_cost_spike", pf.stage4c_conditions)
        self.assertEqual(regional.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(insurance.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertTrue(kics.hard_gate)
        self.assertEqual(securities.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertTrue(ib_pf.hard_gate)
        self.assertIn("record_profit", internet_bank.stage2_signals)
        self.assertIn("abnormal_withdrawal", digital.red_flags)
        self.assertIn("direct_equity_link", toss.green_conditions)
        self.assertEqual(stablecoin.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("issued_volume_missing", stablecoin.red_flags)
        self.assertTrue(guarantee.hard_gate)
        self.assertEqual(disclosure.score_weight.roe_eps_fcf, "cap")
        self.assertTrue(crowded.hard_gate)

    def test_required_round177_cases_are_present_with_stage_markers(self):
        rows = {row["case_id"]: row for row in round177_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND177_CASE_CANDIDATES))
        self.assertEqual(rows["kb_financial_valueup_stage3_candidate"]["target_id"], "BANK_HOLDING_VALUEUP_CAPITAL_RETURN_KOREA")
        self.assertIn("net_profit_5_84tn_krw", rows["kb_financial_valueup_stage3_candidate"]["evidence_fields"])
        self.assertEqual(rows["shinhan_overseas_profit_valueup_candidate"]["target_id"], "BANK_ROE_PBR_RERATING_KOREA")
        self.assertEqual(rows["woori_financial_nonbank_capital_buffer_gate_case"]["target_id"], "BANK_HOLDING_VALUEUP_CAPITAL_RETURN_KOREA")
        self.assertEqual(rows["jb_financial_regional_high_roe_valueup_case"]["target_id"], "REGIONAL_BANK_HIGH_ROE_VALUEUP")
        self.assertEqual(rows["korea_insurance_capital_release_valueup_case"]["target_id"], "INSURANCE_CAPITAL_RELEASE_VALUEUP_KOREA")
        self.assertEqual(rows["kakaobank_profitability_valuation_cap_case"]["target_id"], "INTERNET_BANK_PROFITABILITY")
        self.assertEqual(rows["naver_dunamu_equity_option_security_4c_watch_case"]["stage2_date"], "2025-11-27")
        self.assertEqual(rows["naver_dunamu_equity_option_security_4c_watch_case"]["stage4c_date"], "2025-11-27")
        self.assertEqual(rows["toss_superapp_ipo_stablecoin_related_stock_cap_case"]["stage2_date"], "2025-09-09")
        self.assertEqual(rows["seoul_guarantee_ipo_ransomware_security_case"]["case_type"], "4c_thesis_break")
        self.assertEqual(rows["securities_brokerage_market_beta_cycle_case"]["case_type"], "cyclical_success")
        self.assertEqual(rows["financial_valueup_crowded_4b_watch_case"]["stage4b_date"], "2026-05-06")
        self.assertEqual(rows["bank_credit_cost_pf_overlay_case"]["target_id"], "BANK_CREDIT_COST_PF_OVERLAY")

    def test_case_records_validate_and_keep_round177_guardrails(self):
        records = round177_case_records()

        self.assertEqual(len(records), len(ROUND177_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "FINANCIAL_CAPITAL_DIGITAL")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("low_pbr_valueup_high_dividend_stablecoin_toss_ipo_or_dunamu_headline_is_not_structural_evidence", record.green_guardrails)
            self.assertIn("require_roe_cet1_kics_credit_cost_actual_return_revenue_model_and_price_path_for_green", record.green_guardrails)
            self.assertIn("stage3_early_catch_requires_5_of_8_loop11_conditions", record.green_guardrails)
            self.assertIn("do_not_invent_cet1_kics_credit_cost_pf_return_stake_value_security_resolution_stage_prices_or_mfe_mae", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["naver_dunamu_equity_option_security_4c_watch_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["toss_superapp_ipo_stablecoin_related_stock_cap_case"].rerating_result, "event_premium")
        self.assertEqual(by_id["securities_brokerage_market_beta_cycle_case"].rerating_result, "cyclical_rerating")
        self.assertEqual(by_id["financial_valueup_crowded_4b_watch_case"].score_price_alignment, "price_moved_without_evidence")
        self.assertIn("roe", by_id["kb_financial_valueup_stage3_candidate"].must_have_fields)
        self.assertIn("abnormal_withdrawal_54bn_krw", by_id["naver_dunamu_equity_option_security_4c_watch_case"].red_flag_fields)

    def test_score_profile_rows_mark_no_production_change(self):
        rows = round177_score_profile_rows()

        self.assertEqual(len(rows), len(ROUND177_SCORE_TARGETS))
        for row in rows:
            self.assertEqual(row["large_sector"], "FINANCIAL_CAPITAL_DIGITAL")
            self.assertEqual(row["production_scoring_changed"], "false")
            self.assertIn("loop11_penalty_axes", row)
        by_target = {row["target_id"]: row for row in rows}
        self.assertEqual(by_target["BANK_HOLDING_VALUEUP_CAPITAL_RETURN_KOREA"]["roe_eps_fcf"], "23")
        self.assertEqual(by_target["BANK_ROE_PBR_RERATING_KOREA"]["valuation_4b_room"], "12")
        self.assertEqual(by_target["BANK_CREDIT_COST_PF_OVERLAY"]["hard_gate"], "true")
        self.assertEqual(by_target["INSURANCE_KICS_CSM_GATE"]["roe_eps_fcf"], "gate")
        self.assertEqual(by_target["DIGITAL_ASSET_EXCHANGE_EQUITY_OPTION"]["regulatory_revenue_visibility"], "24")
        self.assertEqual(by_target["DISCLOSURE_CONFIDENCE_CAP"]["roe_eps_fcf"], "cap")
        self.assertEqual(by_target["VALUE_UP_CROWDED_4B_WATCH"]["hard_gate"], "true")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round177_stage_date_rows()}
        fields = {row["field"] for row in round177_price_field_rows()}

        self.assertIn("repeat_return_policy", rows["BANK_HOLDING_VALUEUP_CAPITAL_RETURN_KOREA"]["stage3"])
        self.assertIn("pbr_band_upper_break", rows["BANK_ROE_PBR_RERATING_KOREA"]["stage4b"])
        self.assertIn("k_ics_detail_required", rows["INSURANCE_KICS_CSM_GATE"]["stage2"])
        self.assertIn("record_profit", rows["INTERNET_BANK_PROFITABILITY"]["stage2"])
        self.assertIn("abnormal_withdrawal", rows["DIGITAL_ASSET_EXCHANGE_EQUITY_OPTION"]["stage4c"])
        for field in (
            "return_60d_after_stage2",
            "return_120d_after_stage2",
            "mfe_60d_after_stage2",
            "mae_60d_after_stage2",
            "relative_strength_vs_financial_basket",
            "relative_strength_vs_bank_basket",
            "relative_strength_vs_insurance_basket",
            "roe",
            "roe_change_yoy",
            "net_profit",
            "net_profit_growth_yoy",
            "cet1_ratio",
            "k_ics_ratio",
            "credit_cost",
            "pf_exposure",
            "dividend_payout_ratio",
            "cancelled_share_amount",
            "total_shareholder_return_ratio",
            "pbr_band_percentile",
            "digital_asset_stake_value",
            "equity_method_income",
            "exchange_security_incident_flag",
            "stablecoin_regulatory_status",
            "ipo_valuation",
            "governance_risk_flag",
            "score_price_alignment",
        ):
            self.assertIn(field, fields)

    def test_score_stage_price_alignment_rows_and_markdown(self):
        rows = {row["case_id"]: row for row in round177_score_stage_price_alignment_rows()}
        markdown = render_round177_score_stage_price_alignment_markdown()

        self.assertEqual(len(rows), len(ROUND177_SCORE_STAGE_PRICE_ALIGNMENT))
        self.assertEqual(rows["kb_financial_valueup_stage3_candidate"]["verdict"], "valueup_leader_requires_capital_quality")
        self.assertEqual(rows["naver_dunamu_equity_option_security_4c_watch_case"]["verdict"], "digital_asset_equity_option_security_gate")
        self.assertEqual(rows["seoul_guarantee_ipo_ransomware_security_case"]["verdict"], "guarantee_insurance_security_hard_cap")
        self.assertEqual(rows["financial_valueup_crowded_4b_watch_case"]["verdict"], "valueup_crowding_4b_watch")
        self.assertIn("KB", markdown)
        self.assertIn("Naver-Dunamu", markdown)
        self.assertIn("security", markdown.lower())

    def test_summary_and_markdown_explain_r6_loop11_guardrails(self):
        summary = round177_summary()
        summary_md = render_round177_summary_markdown()
        guardrails = render_round177_green_guardrail_markdown()
        overlays = render_round177_risk_overlay_markdown()
        price_plan = render_round177_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 15)
        self.assertEqual(summary["source_canonical_target_count"], 14)
        self.assertEqual(summary["case_candidate_count"], len(ROUND177_CASE_CANDIDATES))
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("R6 Loop 11", summary_md)
        self.assertIn("ROE/EPS/FCF 22", summary_md)
        self.assertIn("Do not apply R6 Loop-11", guardrails)
        self.assertIn("LOW_PBR_NOT_GREEN", overlays)
        self.assertIn("naver_dunamu_equity_option_security_4c_watch_case", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            paths = write_round177_r6_loop11_reports(
                output_directory=tmp_path / "out",
                cases_path=tmp_path / "cases.jsonl",
                score_profile_path=tmp_path / "profiles.csv",
            )

            for path in paths.values():
                self.assertTrue(path.exists(), path)
            records = load_case_library(paths["cases"])
            self.assertEqual(len(records), len(ROUND177_CASE_CANDIDATES))
            summary = paths["summary"].read_text(encoding="utf-8")
            self.assertIn("Round-177 R6 Loop-11", summary)
            self.assertIn("production_scoring_changed: false", summary)

    def test_cli_argument_parser_supports_paths(self):
        parser = build_parser()
        args = parser.parse_args(
            [
                "--output-directory",
                "out",
                "--cases",
                "cases.jsonl",
                "--score-profiles",
                "profiles.csv",
            ]
        )

        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.score_profiles, "profiles.csv")

    def test_production_scoring_modules_do_not_import_round177_pack(self):
        root = Path(__file__).resolve().parents[1]
        forbidden = "round177_r6_loop11_financial_capital_digital"
        for relative in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/scoring.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = (root / relative).read_text(encoding="utf-8")
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
