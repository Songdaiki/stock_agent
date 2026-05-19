from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from e2r.cli.build_round213_r9_loop8_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector
from e2r.sector.round213_r9_loop8_mobility_transport_leisure_price_validation import (
    ROUND213_CASE_CANDIDATES,
    ROUND213_GREEN_FORBIDDEN_PATTERNS,
    ROUND213_GREEN_REQUIRED_FIELDS,
    ROUND213_HARD_4C_GATES,
    ROUND213_PRICE_VALIDATION_FIELDS,
    ROUND213_REQUIRED_TARGET_ALIASES,
    ROUND213_SCORE_ADJUSTMENTS,
    ROUND213_STAGE4B_WATCH_TRIGGERS,
    render_round213_green_gate_review_markdown,
    render_round213_stage4b_4c_review_markdown,
    round213_audit_payload,
    round213_case_records,
    round213_case_rows,
    round213_summary,
    write_round213_r9_loop8_reports,
)


class Round213R9Loop8MobilityTransportLeisurePriceValidationTests(unittest.TestCase):
    def test_round213_targets_are_existing_canonical_archetypes(self) -> None:
        canonical_values = {item.value for item in E2RArchetype}

        self.assertGreaterEqual(len(ROUND213_REQUIRED_TARGET_ALIASES), 12)
        self.assertTrue(set(ROUND213_REQUIRED_TARGET_ALIASES.values()).issubset(canonical_values))
        self.assertEqual(
            ROUND213_REQUIRED_TARGET_ALIASES["AUTO_HYBRID_VALUEUP"],
            E2RArchetype.AUTO_HYBRID_VALUEUP.value,
        )
        self.assertEqual(
            ROUND213_REQUIRED_TARGET_ALIASES["AIRLINE_SAFETY_REGULATORY_OVERLAY"],
            E2RArchetype.AIRLINE_SAFETY_REGULATORY_OVERLAY.value,
        )
        self.assertEqual(
            ROUND213_REQUIRED_TARGET_ALIASES["THESIS_BREAK_4C"],
            E2RArchetype.THESIS_BREAK_4C.value,
        )

    def test_case_records_validate_and_are_calibration_only(self) -> None:
        records = round213_case_records()
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, Round10LargeSector.MOBILITY_TRANSPORT_LEISURE.value)
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertIn("full_ohlc_complete_false", record.green_guardrails)

        summary = round213_summary()
        self.assertEqual(summary["case_candidate_count"], 7)
        self.assertEqual(summary["structural_success_count"], 1)
        self.assertEqual(summary["success_candidate_count"], 2)
        self.assertEqual(summary["cyclical_success_count"], 1)
        self.assertEqual(summary["event_premium_count"], 2)
        self.assertEqual(summary["thesis_break_count"], 1)
        self.assertEqual(summary["stage3_case_count"], 0)
        self.assertEqual(summary["hard_4c_case_count"], 1)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["full_ohlc_complete"])

    def test_hyundai_and_kia_capture_hybrid_valueup_and_sdv_risks(self) -> None:
        by_id = {case.case_id: case for case in ROUND213_CASE_CANDIDATES}
        hyundai = by_id["r9_loop8_hyundai_hybrid_valueup_tariff_watch"]
        kia = by_id["r9_loop8_kia_sdv_delay_capex_watch"]

        self.assertEqual(hyundai.primary_archetype, E2RArchetype.AUTO_HYBRID_VALUEUP)
        self.assertEqual(hyundai.stage2_date.isoformat(), "2024-08-28")
        self.assertEqual(hyundai.stage4c_date.isoformat(), "2025-09-18")
        self.assertIsNone(hyundai.stage3_date)
        self.assertEqual(hyundai.extra_price_metrics["buyback_plan_krw_trn"], 4.0)
        self.assertEqual(hyundai.extra_price_metrics["relative_margin_target_cut_pct"], -13.3)
        self.assertIn("tariff_margin_target_cut", hyundai.red_flag_fields)

        self.assertEqual(kia.primary_archetype, E2RArchetype.AUTO_SDV_DELAY_CAPEX_OVERLAY)
        self.assertEqual(kia.stage2_date.isoformat(), "2026-04-09")
        self.assertEqual(kia.mae_1d, -5.5)
        self.assertEqual(kia.extra_price_metrics["relative_underperformance_pp"], -3.9)
        self.assertEqual(kia.extra_price_metrics["investment_plan_increase_pct"], 30.0)
        self.assertIn("sdv_launch_delay_one_year", kia.red_flag_fields)

    def test_airline_integration_and_safety_break_are_separated(self) -> None:
        by_id = {case.case_id: case for case in ROUND213_CASE_CANDIDATES}
        korean_air = by_id["r9_loop8_korean_air_asiana_integration"]
        jeju = by_id["r9_loop8_jeju_air_fatal_crash_hard_4c"]

        self.assertEqual(korean_air.primary_archetype, E2RArchetype.AIRLINE_INTEGRATION_SCALE)
        self.assertEqual(korean_air.extra_price_metrics["asiana_stake_acquired_pct"], 63.88)
        self.assertEqual(korean_air.extra_price_metrics["boeing_order_value_usd_bn"], 36.2)
        self.assertEqual(korean_air.extra_price_metrics["capex_scale_vs_asiana_deal_multiple"], 27.8)
        self.assertIn("integration_synergy_unverified", korean_air.red_flag_fields)

        self.assertEqual(jeju.case_type, "4c_thesis_break")
        self.assertTrue(jeju.hard_4c_confirmed)
        self.assertEqual(jeju.stage4c_date.isoformat(), "2024-12-30")
        self.assertEqual(jeju.stage4c_price_anchor, 6920.0)
        self.assertEqual(jeju.mae_1d, -15.7)
        self.assertIn("fatal_safety_accident_179_deaths", jeju.red_flag_fields)

    def test_shipping_and_tourism_events_remain_cyclical_or_event_premium(self) -> None:
        by_id = {case.case_id: case for case in ROUND213_CASE_CANDIDATES}
        hmm = by_id["r9_loop8_hmm_red_sea_freight_cycle"]
        hotel = by_id["r9_loop8_hotel_shilla_paradise_china_visa_event"]
        lotte = by_id["r9_loop8_lotte_tour_china_japan_redirect"]

        self.assertEqual(hmm.case_type, "cyclical_success")
        self.assertEqual(hmm.extra_price_metrics["freightos_index_6w_return_pct"], 40.0)
        self.assertEqual(hmm.extra_price_metrics["maersk_profit_swing_usd_bn"], 2.521)
        self.assertIn("freight_rate_spike_only", hmm.red_flag_fields)

        self.assertEqual(hotel.case_type, "event_premium")
        self.assertEqual(hotel.mfe_1d, 4.8)
        self.assertEqual(hotel.extra_price_metrics["korea_china_flight_capacity_vs_pre_pandemic_pct"], 105.0)
        self.assertIn("tourist_arrival_policy_only", hotel.red_flag_fields)

        self.assertEqual(lotte.rerating_result, "event_premium")
        self.assertEqual(lotte.mfe_1d, 20.0)
        self.assertEqual(lotte.extra_price_metrics["yellow_balloon_event_mfe_pct"], 24.0)
        self.assertIn("casino_utilization_unverified", lotte.red_flag_fields)

    def test_green_gate_and_4c_rules_are_explicit(self) -> None:
        required = set(ROUND213_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND213_GREEN_FORBIDDEN_PATTERNS)
        review = render_round213_green_gate_review_markdown()
        stage_review = render_round213_stage4b_4c_review_markdown()

        self.assertIn("unit_economics", required)
        self.assertIn("fcf_after_capex", required)
        self.assertIn("freight_rate_spike_only", forbidden)
        self.assertIn("safety_failure", forbidden)
        self.assertIn("fatal_safety_accident", ROUND213_HARD_4C_GATES)
        self.assertIn("china_visa_free_tourism_basket_spike", ROUND213_STAGE4B_WATCH_TRIGGERS)
        self.assertIn("Do not apply these weights to production scoring yet.", review)
        self.assertIn("r9_loop8_jeju_air_fatal_crash_hard_4c", stage_review)

    def test_price_validation_fields_and_score_adjustments_cover_r9_axes(self) -> None:
        fields = set(ROUND213_PRICE_VALIDATION_FIELDS)
        axes = {item.axis for item in ROUND213_SCORE_ADJUSTMENTS}

        self.assertIn("reported_price_anchor", fields)
        self.assertIn("freight_or_tourism_metric", fields)
        self.assertIn("safety_or_margin_event", fields)
        self.assertIn("hybrid_mix", axes)
        self.assertIn("unit_economics", axes)
        self.assertIn("tourist_spend_conversion", axes)
        self.assertIn("safety_failure", axes)

    def test_summary_and_audit_payload_keep_non_production_guardrails(self) -> None:
        audit = round213_audit_payload()

        self.assertEqual(audit["source_round"], "docs/round/round_213.md")
        self.assertEqual(audit["large_sector"], Round10LargeSector.MOBILITY_TRANSPORT_LEISURE.value)
        self.assertFalse(audit["summary"]["production_scoring_changed"])
        self.assertFalse(audit["summary"]["candidate_generation_input"])
        self.assertTrue(audit["summary"]["shadow_weight_only"])
        self.assertIn("do_not_use_round213_cases_as_candidate_generation_input", audit["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])
        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round213_r9_loop8_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)

            records = load_case_library(paths["cases"])
            rows = round213_case_rows()
            self.assertEqual(len(records), len(ROUND213_CASE_CANDIDATES))
            self.assertEqual(len(rows), len(ROUND213_CASE_CANDIDATES))
            self.assertIn("현대차", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("hybrid_mix", paths["score_adjustments"].read_text(encoding="utf-8"))
            self.assertIn("fatal_safety_accident", paths["stage4b_4c_review"].read_text(encoding="utf-8"))
            self.assertEqual(json.loads(rows[0]["extra_price_metrics"])["buyback_plan_krw_trn"], 4.0)


if __name__ == "__main__":
    unittest.main()
