from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from e2r.cli.build_round226_r9_loop9_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector
from e2r.sector.round226_r9_loop9_mobility_transport_leisure_price_validation import (
    ROUND226_CASE_CANDIDATES,
    ROUND226_GREEN_FORBIDDEN_PATTERNS,
    ROUND226_GREEN_REQUIRED_FIELDS,
    ROUND226_HARD_4C_GATES,
    ROUND226_PRICE_VALIDATION_FIELDS,
    ROUND226_REQUIRED_TARGET_ALIASES,
    ROUND226_SCORE_ADJUSTMENTS,
    ROUND226_SHADOW_WEIGHT_ROWS,
    ROUND226_STAGE4B_WATCH_TRIGGERS,
    render_round226_green_gate_review_markdown,
    render_round226_stage4b_4c_review_markdown,
    round226_audit_payload,
    round226_case_records,
    round226_case_rows,
    round226_summary,
    write_round226_r9_loop9_reports,
)


class Round226R9Loop9MobilityTransportLeisurePriceValidationTests(unittest.TestCase):
    def test_round226_targets_map_to_existing_canonical_archetypes(self) -> None:
        canonical_values = {item.value for item in E2RArchetype}

        self.assertGreaterEqual(len(ROUND226_REQUIRED_TARGET_ALIASES), 13)
        self.assertTrue(set(ROUND226_REQUIRED_TARGET_ALIASES.values()).issubset(canonical_values))
        self.assertEqual(
            ROUND226_REQUIRED_TARGET_ALIASES["AUTO_TARIFF_MARGIN_4C_WATCH"],
            E2RArchetype.AUTO_TARIFF_LOCALIZATION.value,
        )
        self.assertEqual(
            ROUND226_REQUIRED_TARGET_ALIASES["LOGISTICS_ECOMMERCE_CONTRACT"],
            E2RArchetype.ECOMMERCE_LOGISTICS_REPEAT_CONTRACT.value,
        )
        self.assertEqual(
            ROUND226_REQUIRED_TARGET_ALIASES["TRAVEL_REDIRECT_EVENT_PREMIUM"],
            E2RArchetype.TOURISM_POLICY_EVENT.value,
        )

    def test_case_records_validate_and_keep_calibration_guardrails(self) -> None:
        records = round226_case_records()
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, Round10LargeSector.MOBILITY_TRANSPORT_LEISURE.value)
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertIn("full_ohlc_complete_false", record.green_guardrails)
            self.assertIn("shadow_weight_only_true", record.green_guardrails)

        summary = round226_summary()
        self.assertEqual(summary["case_candidate_count"], 8)
        self.assertEqual(summary["success_candidate_count"], 3)
        self.assertEqual(summary["event_premium_count"], 2)
        self.assertEqual(summary["failed_rerating_count"], 1)
        self.assertEqual(summary["cyclical_success_count"], 1)
        self.assertEqual(summary["stage3_case_count"], 0)
        self.assertEqual(summary["hard_4c_case_count"], 1)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["full_ohlc_complete"])

    def test_hyundai_is_candidate_with_tariff_watch_and_kia_is_not_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND226_CASE_CANDIDATES}
        hyundai = by_id["r9_loop9_hyundai_hybrid_valueup_tariff_watch"]
        kia = by_id["r9_loop9_kia_sdv_delay_capex_watch"]

        self.assertEqual(hyundai.primary_archetype, E2RArchetype.AUTO_HYBRID_VALUEUP)
        self.assertEqual(hyundai.stage2_date.isoformat(), "2024-08-28")
        self.assertEqual(hyundai.stage4c_date.isoformat(), "2025-07-31")
        self.assertIsNone(hyundai.stage3_date)
        self.assertEqual(hyundai.extra_price_metrics["investor_day_close_return_pct"], 4.7)
        self.assertEqual(hyundai.extra_price_metrics["tariff_cost_2025_krw_tn"], 4.1)
        self.assertIn("tariff_cost_2025_4_1tn_krw", hyundai.red_flag_fields)

        self.assertEqual(kia.primary_archetype, E2RArchetype.AUTO_SDV_DELAY_CAPEX_OVERLAY)
        self.assertEqual(kia.case_type, "failed_rerating")
        self.assertEqual(kia.extra_price_metrics["investment_plan_krw_tn"], 41.4)
        self.assertEqual(kia.extra_price_metrics["ev_target_cut_pct"], 20.0)
        self.assertEqual(kia.score_price_alignment, "evidence_good_but_price_failed")
        self.assertIn("sdv_launch_delay_2027_to_2028", kia.red_flag_fields)

    def test_logistics_and_airline_integration_stay_stage2_watch(self) -> None:
        by_id = {case.case_id: case for case in ROUND226_CASE_CANDIDATES}
        cj = by_id["r9_loop9_cj_logistics_shinsegae_contract_price_failed"]
        korean_air = by_id["r9_loop9_korean_air_asiana_integration_capex_watch"]

        self.assertEqual(cj.primary_archetype, E2RArchetype.ECOMMERCE_LOGISTICS_REPEAT_CONTRACT)
        self.assertEqual(cj.stage2_price_anchor, 99100.0)
        self.assertEqual(cj.mae_1d, -0.2)
        self.assertEqual(cj.extra_price_metrics["target_upside_pct"], 17.1)
        self.assertIn("margin_unverified", cj.red_flag_fields)

        self.assertEqual(korean_air.primary_archetype, E2RArchetype.AIRLINE_INTEGRATION_SCALE)
        self.assertEqual(korean_air.extra_price_metrics["asiana_stake_pct"], 63.88)
        self.assertEqual(korean_air.extra_price_metrics["total_package_usd_bn"], 49.89)
        self.assertEqual(korean_air.extra_price_metrics["total_package_vs_asiana_deal_multiple"], 38.4)
        self.assertIn("capex_debt_burden", korean_air.red_flag_fields)

    def test_jeju_air_is_hard_4c_and_hmm_is_cyclical_not_structural_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND226_CASE_CANDIDATES}
        jeju = by_id["r9_loop9_jeju_air_fatal_crash_hard_4c"]
        hmm = by_id["r9_loop9_hmm_red_sea_shipping_cycle"]

        self.assertEqual(jeju.case_type, "4c_thesis_break")
        self.assertTrue(jeju.hard_4c_confirmed)
        self.assertEqual(jeju.stage4c_date.isoformat(), "2024-12-30")
        self.assertEqual(jeju.mae_1d, -15.7)
        self.assertEqual(jeju.extra_price_metrics["fatalities"], 179.0)
        self.assertIn("fatal_safety_accident", jeju.red_flag_fields)

        self.assertEqual(hmm.case_type, "cyclical_success")
        self.assertEqual(hmm.primary_archetype, E2RArchetype.SHIPPING_FREIGHT_CYCLE)
        self.assertIsNone(hmm.stage3_date)
        self.assertEqual(hmm.extra_price_metrics["freightos_6w_return_pct"], 40.0)
        self.assertEqual(hmm.extra_price_metrics["maersk_profit_swing_usd_bn"], 2.521)
        self.assertIn("freight_rate_spike_only", hmm.red_flag_fields)

    def test_tourism_policy_and_redirect_are_event_premium(self) -> None:
        by_id = {case.case_id: case for case in ROUND226_CASE_CANDIDATES}
        visa = by_id["r9_loop9_tourism_visa_free_retail_casino_event"]
        redirect = by_id["r9_loop9_lotte_tour_china_japan_redirect_event"]

        self.assertEqual(visa.case_type, "event_premium")
        self.assertEqual(visa.stage4b_date.isoformat(), "2025-08-06")
        self.assertEqual(visa.extra_price_metrics["hotel_shilla_event_mfe_1d_pct"], 4.8)
        self.assertEqual(visa.extra_price_metrics["target_growth_vs_2024_pct"], 12.8)
        self.assertIn("tourist_spend_unverified", visa.red_flag_fields)

        self.assertEqual(redirect.case_type, "event_premium")
        self.assertEqual(redirect.stage4b_date.isoformat(), "2025-11-21")
        self.assertEqual(redirect.extra_price_metrics["yellow_balloon_event_mfe_pct"], 24.0)
        self.assertEqual(redirect.score_price_alignment, "price_moved_without_evidence")
        self.assertIn("tourism_redirect_event_only", redirect.red_flag_fields)

    def test_green_gate_4b_4c_and_shadow_weights_are_explicit(self) -> None:
        required = set(ROUND226_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND226_GREEN_FORBIDDEN_PATTERNS)
        review = render_round226_green_gate_review_markdown()
        stage_review = render_round226_stage4b_4c_review_markdown()
        weights = {row.archetype: row for row in ROUND226_SHADOW_WEIGHT_ROWS}

        self.assertIn("unit_economics", required)
        self.assertIn("fcf_after_capex", required)
        self.assertIn("freight_rate_spike_only", forbidden)
        self.assertIn("fatal_safety_accident", forbidden)
        self.assertIn("freight_rate_collapse", ROUND226_HARD_4C_GATES)
        self.assertIn("red_sea_freight_rate_spike", ROUND226_STAGE4B_WATCH_TRIGGERS)
        self.assertIn("Do not apply these weights to production scoring yet.", review)
        self.assertIn("r9_loop9_jeju_air_fatal_crash_hard_4c", stage_review)
        self.assertEqual(weights[E2RArchetype.AUTO_HYBRID_VALUEUP].hybrid_mix, 5)
        self.assertEqual(weights[E2RArchetype.SHIPPING_FREIGHT_CYCLE].event_penalty, -5)

    def test_price_fields_and_score_axes_cover_r9_loop9(self) -> None:
        fields = set(ROUND226_PRICE_VALIDATION_FIELDS)
        axes = {item.axis for item in ROUND226_SCORE_ADJUSTMENTS}

        self.assertIn("operating_metric_anchor", fields)
        self.assertIn("capex_or_debt_anchor", fields)
        self.assertIn("cycle_or_policy_anchor", fields)
        self.assertIn("hybrid_mix", axes)
        self.assertIn("tourist_spend_conversion", axes)
        self.assertIn("safety_failure", axes)
        self.assertIn("cycle_normalization", axes)

    def test_audit_payload_marks_non_production_round(self) -> None:
        audit = round226_audit_payload()

        self.assertEqual(audit["source_round"], "docs/round/round_226.md")
        self.assertEqual(audit["large_sector"], Round10LargeSector.MOBILITY_TRANSPORT_LEISURE.value)
        self.assertFalse(audit["summary"]["production_scoring_changed"])
        self.assertFalse(audit["summary"]["candidate_generation_input"])
        self.assertTrue(audit["summary"]["shadow_weight_only"])
        self.assertIn("do_not_use_round226_cases_as_candidate_generation_input", audit["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])
        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round226_r9_loop9_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)

            records = load_case_library(paths["cases"])
            rows = round226_case_rows()
            self.assertEqual(len(records), len(ROUND226_CASE_CANDIDATES))
            self.assertEqual(len(rows), len(ROUND226_CASE_CANDIDATES))
            self.assertIn("현대차", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("freight_rate_spike_only", paths["score_adjustments"].read_text(encoding="utf-8"))
            self.assertIn("AUTO_HYBRID_VALUEUP", paths["shadow_weights"].read_text(encoding="utf-8"))
            self.assertIn("fatal_safety_accident", paths["stage4b_4c_review"].read_text(encoding="utf-8"))
            self.assertEqual(json.loads(rows[0]["extra_price_metrics"])["tariff_cost_2025_krw_tn"], 4.1)


if __name__ == "__main__":
    unittest.main()
