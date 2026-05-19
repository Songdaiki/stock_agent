from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from e2r.cli.build_round212_r8_loop8_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector
from e2r.sector.round212_r8_loop8_platform_content_sw_security_price_validation import (
    ROUND212_CASE_CANDIDATES,
    ROUND212_GREEN_FORBIDDEN_PATTERNS,
    ROUND212_GREEN_REQUIRED_FIELDS,
    ROUND212_HARD_4C_GATES,
    ROUND212_PRICE_VALIDATION_FIELDS,
    ROUND212_REQUIRED_TARGET_ALIASES,
    ROUND212_SCORE_ADJUSTMENTS,
    ROUND212_STAGE4B_WATCH_TRIGGERS,
    render_round212_green_gate_review_markdown,
    render_round212_stage4b_4c_review_markdown,
    round212_audit_payload,
    round212_case_records,
    round212_case_rows,
    round212_summary,
    write_round212_r8_loop8_reports,
)


class Round212R8Loop8PlatformContentSWSecurityPriceValidationTests(unittest.TestCase):
    def test_round212_targets_are_existing_canonical_archetypes(self) -> None:
        canonical_values = {item.value for item in E2RArchetype}

        self.assertGreaterEqual(len(ROUND212_REQUIRED_TARGET_ALIASES), 14)
        self.assertTrue(set(ROUND212_REQUIRED_TARGET_ALIASES.values()).issubset(canonical_values))
        self.assertEqual(
            ROUND212_REQUIRED_TARGET_ALIASES["B2B_SAAS_ERP_WORKFLOW"],
            E2RArchetype.B2B_SAAS_ERP_WORKFLOW.value,
        )
        self.assertEqual(
            ROUND212_REQUIRED_TARGET_ALIASES["WEBTOON_PLATFORM_IP_MONETIZATION"],
            E2RArchetype.WEBTOON_PLATFORM_IP_MONETIZATION.value,
        )

    def test_case_records_validate_and_are_calibration_only(self) -> None:
        records = round212_case_records()
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY.value)
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertIn("full_ohlc_complete_false", record.green_guardrails)

        summary = round212_summary()
        self.assertEqual(summary["case_candidate_count"], 7)
        self.assertEqual(summary["success_candidate_count"], 3)
        self.assertEqual(summary["event_premium_count"], 1)
        self.assertEqual(summary["overheat_count"], 1)
        self.assertEqual(summary["failed_rerating_count"], 2)
        self.assertEqual(summary["stage3_case_count"], 0)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["full_ohlc_complete"])

    def test_douzone_and_krafton_are_stage2_until_repeat_metrics_confirm(self) -> None:
        by_id = {case.case_id: case for case in ROUND212_CASE_CANDIDATES}
        douzone = by_id["r8_loop8_douzone_bizon_eqt_saas"]
        krafton = by_id["r8_loop8_krafton_inzoi_adk_ip"]

        self.assertEqual(douzone.primary_archetype, E2RArchetype.B2B_SAAS_ERP_WORKFLOW)
        self.assertEqual(douzone.stage2_date.isoformat(), "2025-11-07")
        self.assertIsNone(douzone.stage3_date)
        self.assertEqual(douzone.extra_price_metrics["implied_equity_value_usd_bn"], 2.473)
        self.assertIn("arr_proxy_unverified", douzone.red_flag_fields)

        self.assertEqual(krafton.primary_archetype, E2RArchetype.GAME_CONTENT_IP_REPEAT_MONETIZATION)
        self.assertEqual(krafton.extra_price_metrics["inzoi_first_week_sales_mn"], 1.0)
        self.assertEqual(krafton.extra_price_metrics["steam_peak_concurrent_players"], 87377.0)
        self.assertIn("retention_unverified", krafton.red_flag_fields)

    def test_ai_cloud_and_ipo_events_do_not_force_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND212_CASE_CANDIDATES}
        samsung_sds = by_id["r8_loop8_samsung_sds_kkr_ai_event"]
        lg_cns = by_id["r8_loop8_lg_cns_ai_cloud_ipo_failed_price"]
        kakao = by_id["r8_loop8_kakao_openai_ai_partnership"]

        self.assertEqual(samsung_sds.case_type, "event_premium")
        self.assertEqual(samsung_sds.stage4b_date.isoformat(), "2026-04-15")
        self.assertEqual(samsung_sds.mfe_1d, 20.8)
        self.assertEqual(samsung_sds.extra_price_metrics["relative_intraday_outperformance_vs_kospi_pp"], 17.8)
        self.assertIn("ai_capex_without_revenue", samsung_sds.red_flag_fields)

        self.assertEqual(lg_cns.score_price_alignment, "evidence_good_but_price_failed")
        self.assertEqual(lg_cns.stage2_price_anchor, 61900.0)
        self.assertEqual(lg_cns.mae_1d, -3.55)
        self.assertIn("ipo_debut_price_failed", lg_cns.red_flag_fields)

        self.assertEqual(kakao.case_type, "overheat")
        self.assertEqual(kakao.mfe_1d, 9.0)
        self.assertEqual(kakao.mae_1d, -2.0)
        self.assertEqual(kakao.extra_price_metrics["event_fade_from_peak_pp"], -11.0)
        self.assertIn("partnership_headline_only", kakao.red_flag_fields)

    def test_naver_webtoon_and_hybe_capture_ip_monetization_and_governance_risk(self) -> None:
        by_id = {case.case_id: case for case in ROUND212_CASE_CANDIDATES}
        naver = by_id["r8_loop8_naver_webtoon_ip_platform"]
        hybe = by_id["r8_loop8_hybe_legal_governance_watch"]

        self.assertEqual(naver.primary_archetype, E2RArchetype.WEBTOON_PLATFORM_IP_MONETIZATION)
        self.assertEqual(naver.stage2_price_anchor, 165300.0)
        self.assertEqual(naver.extra_price_metrics["webtoon_mfe_from_ipo_to_intraday_high_pct"], 22.2)
        self.assertEqual(naver.extra_price_metrics["net_loss_margin_pct"], 11.3)
        self.assertIn("mau_without_arpu", naver.red_flag_fields)

        self.assertEqual(hybe.primary_archetype, E2RArchetype.PLATFORM_GOVERNANCE_LEGAL_RISK)
        self.assertEqual(hybe.stage4c_date.isoformat(), "2026-04-21")
        self.assertFalse(hybe.hard_4c_confirmed)
        self.assertEqual(hybe.mae_1d, -2.4)
        self.assertIn("founder_legal_risk", hybe.red_flag_fields)

    def test_green_gate_and_4c_rules_are_explicit(self) -> None:
        required = set(ROUND212_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND212_GREEN_FORBIDDEN_PATTERNS)
        review = render_round212_green_gate_review_markdown()
        stage_review = render_round212_stage4b_4c_review_markdown()

        self.assertIn("recurring_revenue_or_bookings", required)
        self.assertIn("arr_proxy_or_paid_usage", required)
        self.assertIn("fcf_conversion", required)
        self.assertIn("ai_partnership_headline_only", forbidden)
        self.assertIn("ipo_debut_premium_only", forbidden)
        self.assertIn("game_launch_first_week_only", forbidden)
        self.assertIn("founder_or_major_shareholder_legal_break", ROUND212_HARD_4C_GATES)
        self.assertIn("ai_partnership_announcement_spike", ROUND212_STAGE4B_WATCH_TRIGGERS)
        self.assertIn("Do not apply these weights to production scoring yet.", review)
        self.assertIn("r8_loop8_hybe_legal_governance_watch", stage_review)

    def test_price_validation_fields_and_score_adjustments_cover_r8_axes(self) -> None:
        fields = set(ROUND212_PRICE_VALIDATION_FIELDS)
        axes = {item.axis for item in ROUND212_SCORE_ADJUSTMENTS}

        self.assertIn("ipo_price", fields)
        self.assertIn("debut_price", fields)
        self.assertIn("arr_or_revenue_proxy", fields)
        self.assertIn("recurring_revenue", axes)
        self.assertIn("arr_proxy", axes)
        self.assertIn("partnership_headline_only", axes)
        self.assertIn("founder_legal_risk", axes)

    def test_summary_and_audit_payload_keep_non_production_guardrails(self) -> None:
        audit = round212_audit_payload()

        self.assertEqual(audit["source_round"], "docs/round/round_212.md")
        self.assertEqual(audit["large_sector"], Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY.value)
        self.assertFalse(audit["summary"]["production_scoring_changed"])
        self.assertFalse(audit["summary"]["candidate_generation_input"])
        self.assertTrue(audit["summary"]["shadow_weight_only"])
        self.assertIn("do_not_use_round212_cases_as_candidate_generation_input", audit["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])
        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round212_r8_loop8_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)

            records = load_case_library(paths["cases"])
            rows = round212_case_rows()
            self.assertEqual(len(records), len(ROUND212_CASE_CANDIDATES))
            self.assertEqual(len(rows), len(ROUND212_CASE_CANDIDATES))
            self.assertIn("더존비즈온", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("recurring_revenue", paths["score_adjustments"].read_text(encoding="utf-8"))
            self.assertIn("founder_or_major_shareholder_legal_break", paths["stage4b_4c_review"].read_text(encoding="utf-8"))
            self.assertEqual(json.loads(rows[1]["extra_price_metrics"])["stage2_event_mfe_1d_pct"], 20.8)


if __name__ == "__main__":
    unittest.main()
