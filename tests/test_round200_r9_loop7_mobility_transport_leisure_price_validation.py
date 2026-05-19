import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round200_r9_loop7_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round200_r9_loop7_mobility_transport_leisure_price_validation import (
    ROUND200_CASE_CANDIDATES,
    ROUND200_GREEN_FORBIDDEN_PATTERNS,
    ROUND200_GREEN_REQUIRED_FIELDS,
    ROUND200_HARD_4C_GATES,
    ROUND200_PRICE_BACKFILL_FIELDS,
    ROUND200_REQUIRED_TARGET_ALIASES,
    render_round200_green_gate_review_markdown,
    render_round200_stage4b_4c_review_markdown,
    round200_audit_payload,
    round200_case_records,
    round200_case_rows,
    round200_price_backfill_field_rows,
    round200_score_adjustment_rows,
    round200_summary,
    write_round200_r9_loop7_reports,
)


class Round200R9Loop7MobilityTransportLeisurePriceValidationTests(unittest.TestCase):
    def test_round200_targets_are_existing_canonical_archetypes(self):
        self.assertGreaterEqual(len(ROUND200_REQUIRED_TARGET_ALIASES), 22)
        self.assertEqual(
            ROUND200_REQUIRED_TARGET_ALIASES["AUTO_HYBRID_VALUEUP"],
            E2RArchetype.AUTO_HYBRID_VALUEUP.value,
        )
        self.assertEqual(
            ROUND200_REQUIRED_TARGET_ALIASES["AIRLINE_SAFETY_REGULATORY_OVERLAY"],
            E2RArchetype.AIRLINE_SAFETY_REGULATORY_OVERLAY.value,
        )
        self.assertEqual(
            ROUND200_REQUIRED_TARGET_ALIASES["FLEET_UNIT_ECONOMICS_OVERLAY"],
            E2RArchetype.FLEET_UNIT_ECONOMICS_OVERLAY.value,
        )
        for canonical in ROUND200_REQUIRED_TARGET_ALIASES.values():
            self.assertIsInstance(E2RArchetype(canonical), E2RArchetype)

    def test_case_records_validate_and_remain_shadow_only(self):
        records = {record.case_id: record for record in round200_case_records()}

        self.assertEqual(len(records), 7)
        self.assertEqual(records["hyundai_motor_hybrid_valueup_tariff_4c_watch"].case_type, "structural_success")
        self.assertEqual(records["kia_hybrid_valueup_sdv_delay_capex_watch"].case_type, "success_candidate")
        self.assertEqual(records["jeju_air_fatal_crash_operational_trust_4c_break"].case_type, "4c_thesis_break")
        self.assertEqual(records["hmm_red_sea_freight_cycle_stage2_4b_watch"].case_type, "cyclical_success")
        self.assertEqual(records["lotte_tour_dream_tower_casino_utilization_gap_watch"].case_type, "failed_rerating")
        for record in records.values():
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertIn("shadow_weight_only_true", record.green_guardrails)
            self.assertEqual(record.price_validation.price_validation_status, "needs_ohlc_backfill")

    def test_auto_cases_separate_hybrid_valueup_from_tariff_and_sdv_risk(self):
        rows = {row["case_id"]: row for row in round200_case_rows()}
        hyundai = rows["hyundai_motor_hybrid_valueup_tariff_4c_watch"]
        kia = rows["kia_hybrid_valueup_sdv_delay_capex_watch"]

        self.assertEqual(hyundai["stage2_date"], "2024-08-28")
        self.assertEqual(hyundai["stage3_date"], "")
        self.assertEqual(hyundai["stage4c_date"], "2025-09-18")
        self.assertEqual(hyundai["hard_4c_confirmed"], "false")
        self.assertIn("tariff_margin_cut_2025_watch", hyundai["red_flag_fields"])
        self.assertEqual(kia["stage2_date"], "2026-04-09")
        self.assertEqual(kia["stage4c_date"], "2026-04-09")
        self.assertEqual(kia["score_price_alignment"], "evidence_good_but_price_failed")
        self.assertIn("sdv_launch_delay_2028", kia["red_flag_fields"])

    def test_airline_shipping_and_tourism_cases_block_green_when_unit_economics_missing(self):
        rows = {row["case_id"]: row for row in round200_case_rows()}
        korean_air = rows["korean_air_asiana_integration_scale_stage2_watch"]
        hmm = rows["hmm_red_sea_freight_cycle_stage2_4b_watch"]
        hotel = rows["hotel_shilla_china_visa_tourism_event_stage2_watch"]
        lotte = rows["lotte_tour_dream_tower_casino_utilization_gap_watch"]

        self.assertEqual(korean_air["stage2_date"], "2024-12-12")
        self.assertEqual(korean_air["stage3_date"], "")
        self.assertIn("integration_synergy_unverified", korean_air["red_flag_fields"])
        self.assertEqual(hmm["case_type"], "cyclical_success")
        self.assertEqual(hmm["stage2_date"], "2025-11-06")
        self.assertIn("freight_rate_spike_only", hmm["red_flag_fields"])
        self.assertEqual(hotel["stage1_date"], "2025-03-20")
        self.assertEqual(hotel["stage2_date"], "2025-09-29")
        self.assertIn("tourist_spend_unverified", hotel["red_flag_fields"])
        self.assertEqual(lotte["stage1_date"], "2025-09-29")
        self.assertEqual(lotte["stage2_date"], "")
        self.assertIn("casino_drop_unverified", lotte["red_flag_fields"])

    def test_jeju_air_is_hard_4c_operational_trust_break(self):
        rows = {row["case_id"]: row for row in round200_case_rows()}
        jeju = rows["jeju_air_fatal_crash_operational_trust_4c_break"]

        self.assertEqual(jeju["case_type"], "4c_thesis_break")
        self.assertEqual(jeju["stage4c_date"], "2024-12-30")
        self.assertEqual(jeju["hard_4c_confirmed"], "true")
        self.assertEqual(jeju["rerating_result"], "thesis_break")
        self.assertIn("fatal_safety_accident", jeju["red_flag_fields"])
        self.assertIn("operational_trust_break", jeju["red_flag_fields"])

    def test_green_gate_requires_unit_economics_and_blocks_cycle_or_policy_only(self):
        required = set(ROUND200_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND200_GREEN_FORBIDDEN_PATTERNS)
        adjustments = {row["axis"]: row for row in round200_score_adjustment_rows()}
        markdown = render_round200_green_gate_review_markdown()

        self.assertIn("unit_economics_confirmed", required)
        self.assertIn("fcf_after_capex_confirmed", required)
        self.assertIn("margin_durability_confirmed", required)
        self.assertIn("safety_and_operational_trust_passed", required)
        self.assertIn("travel_reopening_only", forbidden)
        self.assertIn("freight_rate_spike_only", forbidden)
        self.assertIn("tourist_arrival_policy_only", forbidden)
        self.assertIn("safety_failure", forbidden)
        self.assertEqual(adjustments["hybrid_mix"]["points"], "5")
        self.assertEqual(adjustments["freight_rate_spike_only"]["points"], "-5")
        self.assertEqual(adjustments["safety_failure"]["points"], "-5")
        self.assertIn("Do not apply these weights to production scoring yet", markdown)

    def test_price_backfill_fields_include_r9_unit_economics_and_cycle_inputs(self):
        fields = {row["field"] for row in round200_price_backfill_field_rows()}

        self.assertGreaterEqual(len(ROUND200_PRICE_BACKFILL_FIELDS), 50)
        for field in (
            "hybrid_mix",
            "fcf_after_capex",
            "shareholder_return_execution",
            "operating_margin",
            "tariff_cost",
            "load_factor",
            "yield",
            "integration_synergy",
            "freight_rate",
            "tourist_spend",
            "casino_drop",
            "casino_hold_rate",
            "safety_incident_flag",
            "hard_4c_confirmed",
        ):
            self.assertIn(field, fields)

    def test_stage4b_4c_review_contains_r9_hard_gates(self):
        review = render_round200_stage4b_4c_review_markdown()

        self.assertIn("fatal_safety_accident", ROUND200_HARD_4C_GATES)
        self.assertIn("operational_trust_break", ROUND200_HARD_4C_GATES)
        self.assertIn("freight_rate_collapse", ROUND200_HARD_4C_GATES)
        self.assertIn("casino_utilization_collapse", ROUND200_HARD_4C_GATES)
        self.assertIn("fatal safety accident is hard 4C", review)
        self.assertIn("freight spike is cyclical success", review)
        self.assertIn("jeju_air_fatal_crash_operational_trust_4c_break", review)

    def test_summary_and_audit_payload_are_calibration_only(self):
        summary = round200_summary()
        payload = round200_audit_payload()

        self.assertEqual(summary["case_candidate_count"], len(ROUND200_CASE_CANDIDATES))
        self.assertEqual(summary["stage3_case_count"], 0)
        self.assertEqual(summary["hard_4c_case_count"], 1)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["candidate_generation_input"])
        self.assertTrue(summary["shadow_weight_only"])
        self.assertIn("do_not_use_round200_cases_as_candidate_generation_input", payload["what_not_to_change"])
        self.assertIn("do_not_treat_travel_reopening_freight_spike_sdv_policy_merger_or_tourism_headline_as_green_evidence", payload["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self):
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])

        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = write_round200_r9_loop7_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)
            records = load_case_library(root / "cases.jsonl")
            self.assertEqual(len(records), 7)
            self.assertIn("Stage 3-Green", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("unit_economics", paths["score_adjustments"].read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
