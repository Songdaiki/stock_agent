from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from e2r.cli.build_round203_r12_loop7_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round203_r12_loop7_agri_life_misc_price_validation import (
    ROUND203_CASE_CANDIDATES,
    ROUND203_GREEN_FORBIDDEN_PATTERNS,
    ROUND203_GREEN_REQUIRED_FIELDS,
    ROUND203_HARD_4C_GATES,
    ROUND203_PRICE_BACKFILL_FIELDS,
    ROUND203_REQUIRED_TARGET_ALIASES,
    render_round203_green_gate_review_markdown,
    render_round203_stage4b_4c_review_markdown,
    round203_audit_payload,
    round203_case_records,
    round203_summary,
    write_round203_r12_loop7_reports,
)


class Round203R12Loop7AgriLifeMiscPriceValidationTests(unittest.TestCase):
    def test_round203_targets_are_existing_canonical_archetypes(self) -> None:
        canonical_values = {item.value for item in E2RArchetype}

        self.assertGreaterEqual(len(ROUND203_REQUIRED_TARGET_ALIASES), 15)
        self.assertTrue(set(ROUND203_REQUIRED_TARGET_ALIASES.values()).issubset(canonical_values))
        self.assertEqual(
            ROUND203_REQUIRED_TARGET_ALIASES["HOME_LIVING_APPLIANCE_RENTAL"],
            E2RArchetype.HOME_LIVING_APPLIANCE_RENTAL.value,
        )
        self.assertEqual(
            ROUND203_REQUIRED_TARGET_ALIASES["SMART_FARM_AGRI_TECH"],
            E2RArchetype.SMART_FARM_AGRI_TECH.value,
        )

    def test_case_records_validate_and_keep_r12_conservative_bias(self) -> None:
        records = round203_case_records()
        for record in records:
            record.validate()
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertIn("r12_default_stage3_bias_conservative_except_recurring_service", record.green_guardrails)
            self.assertIsNone(record.stage3_date)

        summary = round203_summary()
        self.assertEqual(summary["stage3_case_count"], 0)
        self.assertEqual(summary["r12_default_stage3_bias"], "conservative_except_recurring_service")
        self.assertFalse(summary["production_scoring_changed"])

    def test_coway_is_recurring_candidate_but_not_green_without_churn_arpu_fcf(self) -> None:
        coway = next(case for case in ROUND203_CASE_CANDIDATES if case.case_id == "coway_rental_recurring_service_candidate")

        self.assertEqual(coway.primary_archetype, E2RArchetype.HOME_LIVING_APPLIANCE_RENTAL)
        self.assertEqual(coway.case_type, "success_candidate")
        self.assertIn("rental_account_base", coway.evidence_fields)
        self.assertIn("churn_unverified", coway.red_flag_fields)
        self.assertIn("fcf_conversion_unverified", coway.red_flag_fields)
        self.assertIsNone(coway.stage3_date)

    def test_education_policy_and_edtech_policy_are_watch_not_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND203_CASE_CANDIDATES}
        megastudy = by_id["megastudy_medical_quota_policy_event_watch"]
        edtech = by_id["education_edtech_phone_ban_policy_watch"]

        self.assertEqual(megastudy.primary_archetype, E2RArchetype.EDUCATION_SPECIALTY_SERVICES)
        self.assertEqual(megastudy.stage2_date.isoformat(), "2025-03-07")
        self.assertIn("education_policy_only", megastudy.red_flag_fields)
        self.assertEqual(megastudy.score_price_alignment, "price_moved_without_evidence")

        self.assertEqual(edtech.primary_archetype, E2RArchetype.EDTECH_AI_DISRUPTION)
        self.assertEqual(edtech.stage1_date.isoformat(), "2025-08-27")
        self.assertIsNone(edtech.stage3_date)

    def test_poultry_disease_event_has_import_ban_reversal_fade(self) -> None:
        poultry = next(
            case
            for case in ROUND203_CASE_CANDIDATES
            if case.case_id == "poultry_basket_brazil_bird_flu_import_ban_event_fade_r12"
        )

        self.assertEqual(poultry.case_type, "event_premium")
        self.assertIn("disease_event_only", poultry.red_flag_fields)
        self.assertIn("import_ban_reversal", poultry.red_flag_fields)
        self.assertEqual(poultry.stage4c_date.isoformat(), "2025-06-23")
        self.assertEqual(poultry.rerating_result, "event_premium")

    def test_agri_machinery_and_smart_farm_require_unit_economics(self) -> None:
        by_id = {case.case_id: case for case in ROUND203_CASE_CANDIDATES}
        agri = by_id["daedong_tym_agri_machinery_export_watch"]
        smart_farm = by_id["smart_farm_basket_unit_economics_insufficient"]

        self.assertEqual(agri.primary_archetype, E2RArchetype.AGRI_MACHINERY_DEMAND_CYCLE)
        self.assertIn(E2RArchetype.AGRI_MACHINERY_SOFTWARE_LOCKIN, agri.secondary_archetypes)
        self.assertIn("dealer_inventory_unknown", agri.red_flag_fields)
        self.assertIsNone(agri.stage3_date)

        self.assertEqual(smart_farm.primary_archetype, E2RArchetype.SMART_FARM_AGRI_TECH)
        self.assertIn("smart_farm_policy_only", smart_farm.red_flag_fields)
        self.assertIn("unit_economics_unverified", smart_farm.red_flag_fields)

    def test_green_gate_requires_recurring_unit_economics_cash_and_regulatory_pass(self) -> None:
        required = set(ROUND203_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND203_GREEN_FORBIDDEN_PATTERNS)
        markdown = render_round203_green_gate_review_markdown()

        self.assertIn("recurring_revenue_confirmed", required)
        self.assertIn("churn_or_retention_stable", required)
        self.assertIn("unit_economics_positive", required)
        self.assertIn("cash_conversion_confirmed", required)
        self.assertIn("education_policy_only", forbidden)
        self.assertIn("smart_farm_policy_only", forbidden)
        self.assertIn("disease_event_only", forbidden)
        self.assertIn("Do not apply these weights to production scoring yet.", markdown)

    def test_price_backfill_fields_cover_event_and_recurring_service_inputs(self) -> None:
        fields = set(ROUND203_PRICE_BACKFILL_FIELDS)

        self.assertIn("MFE_5D", fields)
        self.assertIn("MFE_20D", fields)
        self.assertIn("recurring_account_count", fields)
        self.assertIn("churn_rate", fields)
        self.assertIn("arpu", fields)
        self.assertIn("dealer_inventory", fields)
        self.assertIn("import_restriction_status", fields)
        self.assertIn("unit_economics_metric", fields)

    def test_stage4b_4c_review_contains_r12_hard_gates(self) -> None:
        review = render_round203_stage4b_4c_review_markdown()

        self.assertIn("churn_spike", ROUND203_HARD_4C_GATES)
        self.assertIn("dealer_inventory_build", ROUND203_HARD_4C_GATES)
        self.assertIn("education_policy_reversal", ROUND203_HARD_4C_GATES)
        self.assertIn("unit_economics_failure", ROUND203_HARD_4C_GATES)
        self.assertIn("recurring-service", review)
        self.assertIn("import-ban reversal", review)

    def test_summary_and_audit_payload_are_calibration_only(self) -> None:
        audit = round203_audit_payload()

        self.assertEqual(audit["source_round"], "docs/round/round_203.md")
        self.assertFalse(audit["summary"]["production_scoring_changed"])
        self.assertFalse(audit["summary"]["candidate_generation_input"])
        self.assertTrue(audit["summary"]["shadow_weight_only"])
        self.assertIn("do_not_use_round203_cases_as_candidate_generation_input", audit["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])
        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round203_r12_loop7_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)

            records = load_case_library(paths["cases"])
            self.assertEqual(len(records), len(ROUND203_CASE_CANDIDATES))
            self.assertIn("recurring_revenue", paths["score_adjustments"].read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
