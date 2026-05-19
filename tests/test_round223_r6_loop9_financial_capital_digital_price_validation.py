from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from e2r.cli.build_round223_r6_loop9_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector
from e2r.sector.round223_r6_loop9_financial_capital_digital_price_validation import (
    ROUND223_CASE_CANDIDATES,
    ROUND223_GREEN_FORBIDDEN_PATTERNS,
    ROUND223_GREEN_REQUIRED_FIELDS,
    ROUND223_HARD_4C_GATES,
    ROUND223_PRICE_VALIDATION_FIELDS,
    ROUND223_REQUIRED_TARGET_ALIASES,
    ROUND223_SHADOW_WEIGHT_ROWS,
    ROUND223_STAGE4B_WATCH_TRIGGERS,
    render_round223_green_gate_review_markdown,
    render_round223_stage4b_4c_review_markdown,
    round223_audit_payload,
    round223_case_records,
    round223_case_rows,
    round223_shadow_weight_rows,
    round223_summary,
    write_round223_r6_loop9_reports,
)


class Round223R6Loop9FinancialCapitalDigitalPriceValidationTests(unittest.TestCase):
    def test_targets_alias_to_existing_canonical_archetypes(self) -> None:
        canonical_values = {item.value for item in E2RArchetype}

        self.assertGreaterEqual(len(ROUND223_REQUIRED_TARGET_ALIASES), 13)
        self.assertTrue(set(ROUND223_REQUIRED_TARGET_ALIASES.values()).issubset(canonical_values))
        self.assertEqual(
            ROUND223_REQUIRED_TARGET_ALIASES["BANK_VALUEUP_ROE_PBR_RERATING"],
            E2RArchetype.BANK_ROE_PBR_RERATING_KOREA.value,
        )
        self.assertEqual(
            ROUND223_REQUIRED_TARGET_ALIASES["DIGITAL_ASSET_PLATFORM_MERGER"],
            E2RArchetype.DIGITAL_ASSET_EXCHANGE_CONSOLIDATION.value,
        )
        self.assertEqual(
            ROUND223_REQUIRED_TARGET_ALIASES["INTERNET_BANK_GOVERNANCE_4C"],
            E2RArchetype.PLATFORM_GOVERNANCE_LEGAL_RISK.value,
        )

    def test_case_records_validate_and_remain_calibration_only(self) -> None:
        records = round223_case_records()
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL.value)
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertIn("shadow_weight_only_true", record.green_guardrails)
            self.assertIn("full_ohlc_complete_false", record.green_guardrails)

        summary = round223_summary()
        self.assertEqual(summary["case_candidate_count"], 9)
        self.assertEqual(summary["success_candidate_count"], 5)
        self.assertEqual(summary["cyclical_success_count"], 1)
        self.assertEqual(summary["event_premium_count"], 1)
        self.assertEqual(summary["overheat_count"], 1)
        self.assertEqual(summary["thesis_break_count"], 1)
        self.assertEqual(summary["stage3_case_count"], 0)
        self.assertEqual(summary["stage4c_watch_count"], 2)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["candidate_generation_input"])
        self.assertFalse(summary["full_ohlc_complete"])

    def test_bank_and_nav_cases_are_stage2_until_execution_confirms(self) -> None:
        kb = _case("r6_loop9_kb_financial_bank_valueup")
        sk_square = _case("r6_loop9_sk_square_nav_discount_valueup")
        samsung_life = _case("r6_loop9_samsung_life_nav_capital_release")

        self.assertEqual(kb.primary_archetype, E2RArchetype.BANK_ROE_PBR_RERATING_KOREA)
        self.assertEqual(kb.extra_price_metrics["kb_2025_net_profit_krw_trn"], 5.84)
        self.assertEqual(kb.extra_price_metrics["kb_share_of_big4_profit_pct"], 32.4)
        self.assertIn("roe_cet1_credit_cost_unverified", kb.red_flag_fields)

        self.assertEqual(sk_square.primary_archetype, E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE)
        self.assertEqual(sk_square.stage2_date.isoformat(), "2024-11-21")
        self.assertEqual(sk_square.extra_price_metrics["total_buyback_cancel_program_krw_bn"], 200.0)
        self.assertEqual(sk_square.extra_price_metrics["barrons_discount_2026_pct"], 47.0)

        self.assertEqual(samsung_life.primary_archetype, E2RArchetype.INSURANCE_NAV_VALUEUP_SAMSUNG_ELECTRONICS_STAKE)
        self.assertEqual(samsung_life.extra_price_metrics["samsung_electronics_stake_sale_krw_trn"], 1.3)
        self.assertIn("kics_csm_unverified", samsung_life.red_flag_fields)

    def test_securities_and_stablecoin_are_4b_watch_not_green(self) -> None:
        securities = _case("r6_loop9_securities_financial_basket_capital_market_boom")
        stablecoin = _case("r6_loop9_stablecoin_policy_theme_overheat")

        self.assertEqual(securities.case_type, "cyclical_success")
        self.assertEqual(securities.stage4b_date.isoformat(), "2026-05-06")
        self.assertEqual(securities.mfe_1d, 13.5)
        self.assertEqual(securities.extra_price_metrics["securities_relative_outperformance_pp"], 7.05)
        self.assertIn("market_cycle_revenue_not_structural", securities.red_flag_fields)

        self.assertEqual(stablecoin.primary_archetype, E2RArchetype.KRW_STABLECOIN_POLICY_THEME)
        self.assertEqual(stablecoin.case_type, "overheat")
        self.assertEqual(stablecoin.score_price_alignment, "price_moved_without_evidence")
        self.assertEqual(stablecoin.extra_price_metrics["me2on_mfe_month_pct"], 200.0)
        self.assertFalse(stablecoin.extra_price_metrics["regulated_revenue_confirmed"])

    def test_digital_asset_and_internet_bank_cases_keep_trust_and_listing_gates(self) -> None:
        hana = _case("r6_loop9_hana_dunamu_equity_option")
        naver = _case("r6_loop9_naver_dunamu_platform_merger_trust_watch")
        kbank = _case("r6_loop9_kbank_internet_bank_ipo_watch")
        kakao = _case("r6_loop9_kakao_kakaobank_legal_governance_watch")

        self.assertEqual(hana.primary_archetype, E2RArchetype.DIGITAL_ASSET_BANK_EQUITY_OPTION)
        self.assertEqual(hana.extra_price_metrics["implied_dunamu_equity_value_krw_trn"], 15.31)
        self.assertIn("capital_ratio_impact_unverified", hana.red_flag_fields)

        self.assertEqual(naver.primary_archetype, E2RArchetype.DIGITAL_ASSET_EXCHANGE_CONSOLIDATION)
        self.assertEqual(naver.stage4c_date.isoformat(), "2025-11-27")
        self.assertEqual(naver.mfe_1d, 7.0)
        self.assertEqual(naver.mae_1d, -4.2)
        self.assertEqual(naver.extra_price_metrics["event_swing_pp"], -11.2)
        self.assertIn("abnormal_withdrawal_54bn_krw", naver.red_flag_fields)

        self.assertEqual(kbank.primary_archetype, E2RArchetype.INTERNET_BANK_PROFITABILITY)
        self.assertEqual(kbank.extra_price_metrics["implied_market_cap_at_12000_krw_trn"], 4.512)
        self.assertIn("unlisted_no_stock_ohlc", kbank.red_flag_fields)

        self.assertEqual(kakao.case_type, "4c_thesis_break")
        self.assertEqual(kakao.primary_archetype, E2RArchetype.PLATFORM_GOVERNANCE_LEGAL_RISK)
        self.assertEqual(kakao.mae_1d, -3.4)
        self.assertIn("major_shareholder_legal_risk", kakao.red_flag_fields)

    def test_green_gate_and_stage4_rules_are_explicit(self) -> None:
        required = set(ROUND223_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND223_GREEN_FORBIDDEN_PATTERNS)
        green_markdown = render_round223_green_gate_review_markdown()
        stage_review = render_round223_stage4b_4c_review_markdown()

        self.assertIn("roe_improvement_or_sustainability", required)
        self.assertIn("cet1_kics_or_capital_buffer", required)
        self.assertIn("regulated_digital_revenue_or_equity_method_income", required)
        self.assertIn("stablecoin_policy_theme_only", forbidden)
        self.assertIn("internet_bank_ipo_without_listed_price_path", forbidden)
        self.assertIn("major_shareholder_legal_risk", forbidden)
        self.assertIn("exchange_security_incident_or_abnormal_withdrawal", ROUND223_HARD_4C_GATES)
        self.assertIn("stablecoin_related_basket_two_to_three_x_without_revenue", ROUND223_STAGE4B_WATCH_TRIGGERS)
        self.assertIn("Do not apply these weights to production scoring yet.", green_markdown)
        self.assertIn("r6_loop9_naver_dunamu_platform_merger_trust_watch", stage_review)

    def test_shadow_weights_and_price_fields_cover_r6_axes(self) -> None:
        shadow_text = "\n".join(str(row) for row in round223_shadow_weight_rows())
        fields = set(ROUND223_PRICE_VALIDATION_FIELDS)

        self.assertEqual(len(ROUND223_SHADOW_WEIGHT_ROWS), 9)
        self.assertIn("BANK_ROE_PBR_RERATING_KOREA", shadow_text)
        self.assertIn("SECURITIES_BROKERAGE_MARKET_BETA", shadow_text)
        self.assertIn("INSURANCE_NAV_VALUEUP_SAMSUNG_ELECTRONICS_STAKE", shadow_text)
        self.assertIn("DIGITAL_ASSET_EXCHANGE_CONSOLIDATION", shadow_text)
        self.assertIn("KRW_STABLECOIN_POLICY_THEME", shadow_text)
        self.assertIn("discount_to_nav_or_book", fields)
        self.assertIn("regulated_revenue_confirmed", fields)
        self.assertIn("exchange_trust_incident", fields)

    def test_summary_and_audit_payload_are_calibration_only(self) -> None:
        audit = round223_audit_payload()

        self.assertEqual(audit["source_round"], "docs/round/round_223.md")
        self.assertEqual(audit["analyst_round_id"], "round_151")
        self.assertEqual(audit["large_sector"], Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL.value)
        self.assertFalse(audit["summary"]["production_scoring_changed"])
        self.assertFalse(audit["summary"]["candidate_generation_input"])
        self.assertTrue(audit["summary"]["shadow_weight_only"])
        self.assertIn("do_not_use_round223_cases_as_candidate_generation_input", audit["what_not_to_change"])
        self.assertIn("do_not_lower_stage3_green_thresholds", audit["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])
        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round223_r6_loop9_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)

            records = load_case_library(paths["cases"])
            rows = round223_case_rows()
            self.assertEqual(len(records), len(ROUND223_CASE_CANDIDATES))
            self.assertEqual(len(rows), len(ROUND223_CASE_CANDIDATES))
            self.assertIn("KB금융", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("roe_sustainability", paths["score_adjustments"].read_text(encoding="utf-8"))
            self.assertIn("KRW_STABLECOIN_POLICY_THEME", paths["shadow_weights"].read_text(encoding="utf-8"))
            self.assertIn("regulated_revenue_confirmed", paths["price_validation_fields"].read_text(encoding="utf-8"))


def _case(case_id: str):
    return next(case for case in ROUND223_CASE_CANDIDATES if case.case_id == case_id)


if __name__ == "__main__":
    unittest.main()
