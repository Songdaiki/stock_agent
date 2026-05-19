from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from e2r.cli.build_round229_r12_loop9_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector
from e2r.sector.round229_r12_loop9_agri_life_service_misc_price_validation import (
    ROUND229_CASE_CANDIDATES,
    ROUND229_DEFAULT_STAGE3_BIAS,
    ROUND229_GREEN_FORBIDDEN_PATTERNS,
    ROUND229_GREEN_REQUIRED_FIELDS,
    ROUND229_HARD_4C_GATES,
    ROUND229_PRICE_VALIDATION_FIELDS,
    ROUND229_REQUIRED_TARGET_ALIASES,
    ROUND229_SCORE_ADJUSTMENTS,
    ROUND229_SHADOW_WEIGHT_ROWS,
    ROUND229_STAGE4B_WATCH_TRIGGERS,
    render_round229_green_gate_review_markdown,
    render_round229_stage4b_4c_review_markdown,
    round229_audit_payload,
    round229_case_records,
    round229_case_rows,
    round229_deep_sub_archetype_rows,
    round229_shadow_weight_rows,
    round229_summary,
    write_round229_r12_loop9_reports,
)


class Round229R12Loop9AgriLifeServiceMiscPriceValidationTests(unittest.TestCase):
    def test_round229_targets_map_to_existing_canonical_archetypes(self) -> None:
        canonical_values = {item.value for item in E2RArchetype}

        self.assertGreaterEqual(len(ROUND229_REQUIRED_TARGET_ALIASES), 14)
        self.assertTrue(set(ROUND229_REQUIRED_TARGET_ALIASES.values()).issubset(canonical_values))
        self.assertEqual(
            ROUND229_REQUIRED_TARGET_ALIASES["CONSUMER_REGULATED_CASHFLOW"],
            E2RArchetype.CONSUMER_REGULATED_PRODUCT.value,
        )
        self.assertEqual(
            ROUND229_REQUIRED_TARGET_ALIASES["AGRI_MACHINERY_EXPORT_CYCLE"],
            E2RArchetype.AGRI_MACHINERY_EXPORT_CYCLE_KOREA.value,
        )
        self.assertEqual(
            ROUND229_REQUIRED_TARGET_ALIASES["CLASSROOM_DEVICE_REGULATION"],
            E2RArchetype.EDTECH_AI_DISRUPTION_KOREA.value,
        )

    def test_case_records_validate_and_are_calibration_only(self) -> None:
        records = round229_case_records()
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, Round10LargeSector.EDUCATION_LIFE_AGRI_MISC.value)
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertIn("full_ohlc_complete_false", record.green_guardrails)
            self.assertIn("r12_default_stage3_bias_conservative_except_recurring_service", record.green_guardrails)

        summary = round229_summary()
        self.assertEqual(summary["case_candidate_count"], 8)
        self.assertEqual(summary["success_candidate_count"], 3)
        self.assertEqual(summary["event_premium_count"], 3)
        self.assertEqual(summary["failed_rerating_count"], 1)
        self.assertEqual(summary["overheat_count"], 1)
        self.assertEqual(summary["stage3_case_count"], 0)
        self.assertEqual(summary["hard_4c_case_count"], 0)
        self.assertEqual(summary["r12_default_stage3_bias"], ROUND229_DEFAULT_STAGE3_BIAS)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["full_ohlc_complete"])

    def test_coway_and_ktng_are_structural_candidates_but_not_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND229_CASE_CANDIDATES}
        coway = by_id["r12_loop9_coway_recurring_rental_watch"]
        ktng = by_id["r12_loop9_ktng_regulated_cashflow_watch"]

        self.assertEqual(coway.primary_archetype, E2RArchetype.HOME_LIVING_APPLIANCE_RENTAL)
        self.assertIsNone(coway.stage3_date)
        self.assertEqual(coway.round_alignment_label, "success_candidate")
        self.assertIn("churn_unverified", coway.red_flag_fields)
        self.assertIn("fcf_unverified", coway.red_flag_fields)

        self.assertEqual(ktng.primary_archetype, E2RArchetype.CONSUMER_REGULATED_PRODUCT)
        self.assertEqual(ktng.extra_price_metrics["revenue_2024_krw_trn"], 5.9)
        self.assertIn("tax_regulation_watch", ktng.red_flag_fields)
        self.assertEqual(ktng.round_rerating_label, "regulated_cashflow_watch")

    def test_agri_machinery_and_smart_farm_require_unit_economics(self) -> None:
        by_id = {case.case_id: case for case in ROUND229_CASE_CANDIDATES}
        agri = by_id["r12_loop9_daedong_tym_agri_machinery_watch"]
        smart_farm = by_id["r12_loop9_smart_farm_unit_economics_watch"]

        self.assertEqual(agri.primary_archetype, E2RArchetype.AGRI_MACHINERY_EXPORT_CYCLE_KOREA)
        self.assertIn("dealer_inventory_unknown", agri.red_flag_fields)
        self.assertEqual(agri.round_stage_failure_label, "stage1_attention_only")

        self.assertEqual(smart_farm.primary_archetype, E2RArchetype.SMART_FARM_AGRI_TECH)
        self.assertEqual(smart_farm.extra_price_metrics["uav_counting_accuracy_pct"], 94.4)
        self.assertEqual(smart_farm.extra_price_metrics["uav_weight_estimation_accuracy_pct"], 87.5)
        self.assertIn("commercial_installation_unverified", smart_farm.red_flag_fields)

    def test_education_policy_and_phone_ban_are_policy_watch_not_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND229_CASE_CANDIDATES}
        quota = by_id["r12_loop9_megastudy_medical_quota_policy"]
        phone_ban = by_id["r12_loop9_edtech_phone_ban_policy_watch"]

        self.assertEqual(quota.primary_archetype, E2RArchetype.EDUCATION_POLICY_EVENT)
        self.assertEqual(quota.stage2_date.isoformat(), "2026-02-01")
        self.assertEqual(quota.extra_price_metrics["quota_increase_2027_pct"], 16.0)
        self.assertEqual(quota.extra_price_metrics["quota_increase_2031_pct"], 26.6)
        self.assertIn("education_policy_only", quota.red_flag_fields)

        self.assertEqual(phone_ban.primary_archetype, E2RArchetype.EDTECH_AI_DISRUPTION_KOREA)
        self.assertEqual(phone_ban.stage4c_date.isoformat(), "2026-03-01")
        self.assertEqual(phone_ban.extra_price_metrics["social_media_daily_life_impact_pct"], 37.0)
        self.assertEqual(phone_ban.extra_price_metrics["anxiety_without_social_media_pct"], 22.0)
        self.assertEqual(phone_ban.round_alignment_label, "policy_watch")

    def test_disease_and_celebrity_food_events_stay_event_or_overheat(self) -> None:
        by_id = {case.case_id: case for case in ROUND229_CASE_CANDIDATES}
        poultry = by_id["r12_loop9_poultry_bird_flu_import_event"]
        chicken = by_id["r12_loop9_kyochon_jensen_chicken_event"]

        self.assertEqual(poultry.primary_archetype, E2RArchetype.LIVESTOCK_DISEASE_PRICE_REGULATORY)
        self.assertEqual(poultry.extra_price_metrics["brazil_2024_poultry_exports_mn_tons"], 5.0)
        self.assertIn("restriction_easing_event_fade", poultry.red_flag_fields)

        self.assertEqual(chicken.primary_archetype, E2RArchetype.FOOD_SERVICE_EVENT_PREMIUM)
        self.assertEqual(chicken.stage4b_date.isoformat(), "2025-10-31")
        self.assertEqual(chicken.mfe_1d, 25.0)
        self.assertEqual(chicken.score_price_alignment, "price_moved_without_evidence")
        self.assertIn("celebrity_food_event_only", chicken.red_flag_fields)

    def test_green_gate_and_4c_rules_are_explicit(self) -> None:
        required = set(ROUND229_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND229_GREEN_FORBIDDEN_PATTERNS)
        review = render_round229_green_gate_review_markdown()
        stage_review = render_round229_stage4b_4c_review_markdown()

        self.assertIn("recurring_revenue_or_repeat_purchase_confirmed", required)
        self.assertIn("unit_economics_confirmed", required)
        self.assertIn("cash_conversion_visible", required)
        self.assertIn("education_policy_only", forbidden)
        self.assertIn("celebrity_food_event_only", forbidden)
        self.assertIn("smart_farm_technology_paper_only", forbidden)
        self.assertIn("celebrity_food_event_plus_20_to_30pct_without_sales", ROUND229_STAGE4B_WATCH_TRIGGERS)
        self.assertIn("churn_spike", ROUND229_HARD_4C_GATES)
        self.assertIn("Do not apply these weights to production scoring yet.", review)
        self.assertIn("Smart-farm", stage_review)

    def test_price_fields_score_axes_shadow_and_deep_rows_cover_round229(self) -> None:
        fields = set(ROUND229_PRICE_VALIDATION_FIELDS)
        axes = {item.axis for item in ROUND229_SCORE_ADJUSTMENTS}
        shadow_rows = {row["archetype"]: row for row in round229_shadow_weight_rows()}
        deep_rows = round229_deep_sub_archetype_rows()

        self.assertIn("unit_economics_anchor", fields)
        self.assertIn("business_metric_anchor", fields)
        self.assertIn("recurring_revenue", axes)
        self.assertIn("celebrity_food_event_only", axes)
        self.assertIn("subsidy_dependent_unit_economics", axes)
        self.assertEqual(len(ROUND229_SHADOW_WEIGHT_ROWS), 8)
        self.assertEqual(shadow_rows["HOME_LIVING_APPLIANCE_RENTAL"]["recurring_revenue"], "+5")
        self.assertEqual(shadow_rows["FOOD_SERVICE_EVENT_PREMIUM"]["event_penalty"], "-5")
        self.assertTrue(any("Coway" in row["terms"] for row in deep_rows))
        self.assertTrue(any("Jensen Huang chicken event" in row["terms"] for row in deep_rows))

    def test_summary_and_audit_payload_keep_non_production_guardrails(self) -> None:
        audit = round229_audit_payload()

        self.assertEqual(audit["source_round"], "docs/round/round_229.md")
        self.assertEqual(audit["raw_large_sector_label"], "AGRI_LIFE_SERVICE_MISC")
        self.assertEqual(audit["large_sector"], Round10LargeSector.EDUCATION_LIFE_AGRI_MISC.value)
        self.assertFalse(audit["summary"]["production_scoring_changed"])
        self.assertFalse(audit["summary"]["candidate_generation_input"])
        self.assertTrue(audit["summary"]["shadow_weight_only"])
        self.assertEqual(audit["summary"]["r12_default_stage3_bias"], "conservative_except_recurring_service")
        self.assertEqual(len(audit["shadow_weights"]), 8)
        self.assertEqual(len(audit["deep_sub_archetypes"]), 8)
        self.assertIn("do_not_use_round229_cases_as_candidate_generation_input", audit["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])
        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round229_r12_loop9_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)

            records = load_case_library(paths["cases"])
            rows = round229_case_rows()
            self.assertEqual(len(records), len(ROUND229_CASE_CANDIDATES))
            self.assertEqual(len(rows), len(ROUND229_CASE_CANDIDATES))
            self.assertIn("코웨이", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("recurring_revenue", paths["score_adjustments"].read_text(encoding="utf-8"))
            self.assertIn("HOME_LIVING_APPLIANCE_RENTAL", paths["shadow_weights"].read_text(encoding="utf-8"))
            self.assertIn("Jensen Huang chicken event", paths["deep_sub_archetypes"].read_text(encoding="utf-8"))
            self.assertEqual(json.loads(rows[-1]["extra_price_metrics"])["uav_counting_accuracy_pct"], 94.4)


if __name__ == "__main__":
    unittest.main()
