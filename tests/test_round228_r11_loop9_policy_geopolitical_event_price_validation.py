from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from e2r.cli.build_round228_r11_loop9_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector
from e2r.sector.round228_r11_loop9_policy_geopolitical_event_price_validation import (
    ROUND228_CASE_CANDIDATES,
    ROUND228_DEFAULT_STAGE3_BIAS,
    ROUND228_GREEN_FORBIDDEN_PATTERNS,
    ROUND228_GREEN_REQUIRED_FIELDS,
    ROUND228_HARD_4C_GATES,
    ROUND228_PRICE_VALIDATION_FIELDS,
    ROUND228_REQUIRED_TARGET_ALIASES,
    ROUND228_SCORE_ADJUSTMENTS,
    ROUND228_SHADOW_WEIGHT_ROWS,
    ROUND228_STAGE4B_WATCH_TRIGGERS,
    render_round228_green_gate_review_markdown,
    render_round228_stage4b_4c_review_markdown,
    round228_audit_payload,
    round228_case_records,
    round228_case_rows,
    round228_deep_sub_archetype_rows,
    round228_shadow_weight_rows,
    round228_summary,
    write_round228_r11_loop9_reports,
)


class Round228R11Loop9PolicyGeopoliticalEventPriceValidationTests(unittest.TestCase):
    def test_round228_targets_map_to_existing_canonical_archetypes(self) -> None:
        canonical_values = {item.value for item in E2RArchetype}

        self.assertGreaterEqual(len(ROUND228_REQUIRED_TARGET_ALIASES), 12)
        self.assertTrue(set(ROUND228_REQUIRED_TARGET_ALIASES.values()).issubset(canonical_values))
        self.assertEqual(
            ROUND228_REQUIRED_TARGET_ALIASES["GOVERNANCE_REFORM_VALUEUP_POLICY"],
            E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN.value,
        )
        self.assertEqual(
            ROUND228_REQUIRED_TARGET_ALIASES["US_KOREA_TARIFF_TRADE_DEAL"],
            E2RArchetype.INDUSTRIAL_POLICY_TARIFF_EVENT.value,
        )
        self.assertEqual(
            ROUND228_REQUIRED_TARGET_ALIASES["DOMESTIC_RESOURCE_DISCOVERY_EVENT"],
            E2RArchetype.DOMESTIC_RESOURCE_DISCOVERY_EVENT.value,
        )

    def test_case_records_validate_and_are_calibration_only(self) -> None:
        records = round228_case_records()
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, Round10LargeSector.POLICY_GEOPOLITICAL_EVENT.value)
            self.assertIn("production_scoring_changed_false", record.green_guardrails)
            self.assertIn("candidate_generation_input_false", record.green_guardrails)
            self.assertIn("full_ohlc_complete_false", record.green_guardrails)
            self.assertIn("r11_default_stage3_bias_very_conservative", record.green_guardrails)

        summary = round228_summary()
        self.assertEqual(summary["case_candidate_count"], 8)
        self.assertEqual(summary["success_candidate_count"], 4)
        self.assertEqual(summary["event_premium_count"], 2)
        self.assertEqual(summary["failed_rerating_count"], 2)
        self.assertEqual(summary["stage3_case_count"], 0)
        self.assertEqual(summary["hard_4c_case_count"], 0)
        self.assertEqual(summary["r11_default_stage3_bias"], ROUND228_DEFAULT_STAGE3_BIAS)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["full_ohlc_complete"])

    def test_valueup_reform_is_market_structure_stage2_not_company_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND228_CASE_CANDIDATES}
        valueup = by_id["r11_loop9_commercial_act_valueup_reform"]

        self.assertEqual(valueup.primary_archetype, E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN)
        self.assertEqual(valueup.stage1_date.isoformat(), "2025-07-03")
        self.assertEqual(valueup.stage2_date.isoformat(), "2025-08-25")
        self.assertIsNone(valueup.stage3_date)
        self.assertEqual(valueup.stage1_price_anchor, 3116.27)
        self.assertEqual(valueup.mfe_1d, 1.34)
        self.assertIn("company_level_payout_unverified", valueup.red_flag_fields)

    def test_tax_shock_and_hyundai_steel_are_4c_watch_not_green(self) -> None:
        by_id = {case.case_id: case for case in ROUND228_CASE_CANDIDATES}
        tax = by_id["r11_loop9_tax_policy_market_shock"]
        steel = by_id["r11_loop9_hyundai_steel_us_capex_tariff_strategy_fail"]

        self.assertEqual(tax.primary_archetype, E2RArchetype.TAX_POLICY_MARKET_SHOCK_OVERLAY)
        self.assertEqual(tax.mae_1d, -3.9)
        self.assertEqual(tax.extra_price_metrics["threshold_reduction_pct"], -80.0)
        self.assertIn("tax_policy_surprise", tax.red_flag_fields)

        self.assertEqual(steel.primary_archetype, E2RArchetype.STEEL_TARIFF_EVENT_KOREA)
        self.assertEqual(steel.mae_1d, -21.0)
        self.assertEqual(steel.extra_price_metrics["us_plant_investment_usd_bn"], 6.0)
        self.assertEqual(steel.score_price_alignment, "evidence_good_but_price_failed")
        self.assertIn("capex_for_tariff_without_funding", steel.red_flag_fields)

    def test_tariff_deal_chip_support_and_fiscal_stimulus_stay_stage2_or_event(self) -> None:
        by_id = {case.case_id: case for case in ROUND228_CASE_CANDIDATES}
        tariff = by_id["r11_loop9_us_korea_trade_tariff_fx_watch"]
        chip = by_id["r11_loop9_semiconductor_support_package"]
        stimulus = by_id["r11_loop9_fiscal_stimulus_voucher_event"]

        self.assertEqual(tariff.primary_archetype, E2RArchetype.INDUSTRIAL_POLICY_TARIFF_EVENT)
        self.assertEqual(tariff.extra_price_metrics["tariff_reduction_pct"], -40.0)
        self.assertEqual(tariff.extra_price_metrics["us_investment_pledge_usd_bn"], 350.0)
        self.assertIn("macro_fx_outflow_risk", tariff.red_flag_fields)

        self.assertEqual(chip.primary_archetype, E2RArchetype.MEMORY_SUPERCYCLE_AI_CAPEX)
        self.assertEqual(chip.extra_price_metrics["support_package_increase_pct"], 26.9)
        self.assertIn("support_package_without_order", chip.red_flag_fields)

        self.assertEqual(stimulus.case_type, "event_premium")
        self.assertEqual(stimulus.extra_price_metrics["approved_stimulus_krw_trn"], 31.8)
        self.assertEqual(stimulus.extra_price_metrics["share_receiving_250k_pct"], 84.0)
        self.assertIn("fiscal_stimulus_without_revenue_conversion", stimulus.red_flag_fields)

    def test_posco_lng_is_stage2_offtake_and_kogas_is_price_without_evidence(self) -> None:
        by_id = {case.case_id: case for case in ROUND228_CASE_CANDIDATES}
        posco = by_id["r11_loop9_posco_international_alaska_lng_offtake"]
        kogas = by_id["r11_loop9_kogas_east_sea_resource_event"]

        self.assertEqual(posco.primary_archetype, E2RArchetype.ENERGY_SECURITY_POLICY_EVENT)
        self.assertEqual(posco.stage2_date.isoformat(), "2025-12-04")
        self.assertEqual(posco.extra_price_metrics["total_contract_volume_mt"], 20.0)
        self.assertIn("fid_not_confirmed", posco.red_flag_fields)

        self.assertEqual(kogas.primary_archetype, E2RArchetype.DOMESTIC_RESOURCE_DISCOVERY_EVENT)
        self.assertEqual(kogas.stage4b_date.isoformat(), "2024-06-03")
        self.assertEqual(kogas.stage1_price_anchor, 38700.0)
        self.assertEqual(kogas.mfe_1d, 30.0)
        self.assertEqual(kogas.extra_price_metrics["failure_probability_pct"], 80.0)
        self.assertEqual(kogas.score_price_alignment, "price_moved_without_evidence")
        self.assertIn("resource_estimate_without_drilling", kogas.red_flag_fields)

    def test_green_gate_and_4c_rules_are_explicit(self) -> None:
        required = set(ROUND228_GREEN_REQUIRED_FIELDS)
        forbidden = set(ROUND228_GREEN_FORBIDDEN_PATTERNS)
        review = render_round228_green_gate_review_markdown()
        stage_review = render_round228_stage4b_4c_review_markdown()

        self.assertIn("policy_or_event_escalated_to_company_contract", required)
        self.assertIn("financing_or_fid_confirmed", required)
        self.assertIn("margin_or_eps_fcf_revision_visible", required)
        self.assertIn("policy_news_only", forbidden)
        self.assertIn("resource_estimate_without_drilling", forbidden)
        self.assertIn("macro_fx_outflow_risk", forbidden)
        self.assertIn("same_day_policy_or_resource_spike", ROUND228_STAGE4B_WATCH_TRIGGERS)
        self.assertIn("tax_policy_confidence_break", ROUND228_HARD_4C_GATES)
        self.assertIn("Do not apply these weights to production scoring yet.", review)
        self.assertIn("Resource discovery", stage_review)

    def test_price_fields_score_axes_shadow_and_deep_rows_cover_round228(self) -> None:
        fields = set(ROUND228_PRICE_VALIDATION_FIELDS)
        axes = {item.axis for item in ROUND228_SCORE_ADJUSTMENTS}
        shadow_rows = {row["archetype"]: row for row in round228_shadow_weight_rows()}
        deep_rows = round228_deep_sub_archetype_rows()

        self.assertIn("policy_amount_anchor", fields)
        self.assertIn("contract_or_offtake_anchor", fields)
        self.assertIn("resource_commerciality_anchor", fields)
        self.assertIn("actual_contract_or_budget", axes)
        self.assertIn("macro_fx_outflow_risk", axes)
        self.assertIn("price_rally_before_commerciality", axes)
        self.assertEqual(len(ROUND228_SHADOW_WEIGHT_ROWS), 8)
        self.assertEqual(shadow_rows["VALUE_UP_SHAREHOLDER_RETURN"]["shareholder_rights_reform"], "+5")
        self.assertEqual(shadow_rows["DOMESTIC_RESOURCE_DISCOVERY_EVENT"]["event_penalty"], "-5")
        self.assertTrue(any("Commercial Act amendment" in row["terms"] for row in deep_rows))
        self.assertTrue(any("East Sea oil and gas" in row["terms"] for row in deep_rows))

    def test_summary_and_audit_payload_keep_non_production_guardrails(self) -> None:
        audit = round228_audit_payload()

        self.assertEqual(audit["source_round"], "docs/round/round_228.md")
        self.assertEqual(audit["large_sector"], Round10LargeSector.POLICY_GEOPOLITICAL_EVENT.value)
        self.assertFalse(audit["summary"]["production_scoring_changed"])
        self.assertFalse(audit["summary"]["candidate_generation_input"])
        self.assertTrue(audit["summary"]["shadow_weight_only"])
        self.assertEqual(audit["summary"]["r11_default_stage3_bias"], "very_conservative")
        self.assertEqual(len(audit["shadow_weights"]), 8)
        self.assertEqual(len(audit["deep_sub_archetypes"]), 8)
        self.assertIn("do_not_use_round228_cases_as_candidate_generation_input", audit["what_not_to_change"])

    def test_cli_parser_and_writer_outputs(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--output-directory", "out", "--cases", "cases.jsonl", "--audit", "audit.json"])
        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.audit, "audit.json")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round228_r11_loop9_reports(
                output_directory=root / "out",
                cases_path=root / "cases.jsonl",
                audit_path=root / "audit.json",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), path)

            records = load_case_library(paths["cases"])
            rows = round228_case_rows()
            self.assertEqual(len(records), len(ROUND228_CASE_CANDIDATES))
            self.assertEqual(len(rows), len(ROUND228_CASE_CANDIDATES))
            self.assertIn("한국가스공사", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("actual_contract_or_budget", paths["score_adjustments"].read_text(encoding="utf-8"))
            self.assertIn("VALUE_UP_SHAREHOLDER_RETURN", paths["shadow_weights"].read_text(encoding="utf-8"))
            self.assertIn("East Sea oil and gas", paths["deep_sub_archetypes"].read_text(encoding="utf-8"))
            self.assertEqual(json.loads(rows[-1]["extra_price_metrics"])["failure_probability_pct"], 80.0)


if __name__ == "__main__":
    unittest.main()
