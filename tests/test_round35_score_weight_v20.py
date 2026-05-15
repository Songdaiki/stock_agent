import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round35_score_weight_report import build_parser
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10ThemePosture
from e2r.sector.round35_score_weight_v20 import (
    ROUND35_CASE_CANDIDATES,
    ROUND35_SCORE_TARGETS,
    render_round35_biotech_commercialization_markdown,
    render_round35_glp1_regulatory_markdown,
    render_round35_service_automation_markdown,
    render_round35_summary_markdown,
    round35_case_records,
    round35_score_profile_rows,
    round35_summary,
    target_for,
    write_round35_score_weight_reports,
)


class Round35ScoreWeightV20Tests(unittest.TestCase):
    def test_round35_targets_include_healthcare_and_service_automation_families(self):
        labels = {target.target_id for target in ROUND35_SCORE_TARGETS}

        self.assertEqual(len(labels), 8)
        self.assertIn("BIOSIMILAR_COMMERCIALIZATION", labels)
        self.assertIn("OBESITY_GLP1_COMMERCIALIZATION", labels)
        self.assertIn("GENE_THERAPY_RARE_DISEASE", labels)
        self.assertIn("AI_DRUG_DISCOVERY_PLATFORM", labels)
        self.assertIn("CONTACT_CENTER_AI_AUTOMATION", labels)
        self.assertIn("SERVICE_KIOSK_SELF_CHECKOUT", labels)
        self.assertIn("BIOSIMILAR_ORIGINATOR_DEFENSE", labels)
        self.assertIn("PHARMA_PLATFORM_REGULATORY_RISK", labels)

    def test_biosimilar_requires_uptake_payer_and_margin_not_approval_only(self):
        target = target_for("BIOSIMILAR_COMMERCIALIZATION")
        markdown = render_round35_biotech_commercialization_markdown()
        records = {record.case_id: record for record in round35_case_records()}

        self.assertIsNotNone(target)
        assert target is not None
        self.assertEqual(target.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertEqual(target.score_weight.information_confidence, 6)
        self.assertIn("payer_or_pbm_adoption", target.green_conditions)
        self.assertIn("prescription_volume_growth", target.green_conditions)
        self.assertIn("approval_only", target.red_flags)
        self.assertEqual(records["humira_biosimilar_slow_uptake_counterexample"].case_type, "failed_rerating")
        self.assertEqual(records["biosimilar_price_margin_pressure_4c"].case_type, "4c_thesis_break")
        self.assertIn("Approval and discount access are Stage 1 signals", markdown)

    def test_glp1_is_green_possible_but_compounded_and_regulatory_risk_are_gates(self):
        target = target_for("OBESITY_GLP1_COMMERCIALIZATION")
        channel = target_for("PHARMA_PLATFORM_REGULATORY_RISK")
        markdown = render_round35_glp1_regulatory_markdown()
        records = {record.case_id: record for record in round35_case_records()}

        self.assertIsNotNone(target)
        self.assertIsNotNone(channel)
        assert target is not None
        assert channel is not None
        self.assertEqual(target.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(channel.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("reimbursement_expansion", target.green_conditions)
        self.assertIn("compounded_drugs", target.red_flags)
        self.assertIn("advertising_regulation", target.red_flags)
        self.assertIn("fda_warning", channel.red_flags)
        self.assertEqual(records["novo_wegovy_slowdown_compounded_alternative_4c"].case_type, "4c_thesis_break")
        self.assertEqual(records["legal_telehealth_prescription_channel_candidate"].case_type, "success_candidate")
        self.assertIn("compounded alternatives", markdown)

    def test_gene_therapy_and_ai_drug_discovery_are_redteam_first(self):
        gene = target_for("GENE_THERAPY_RARE_DISEASE")
        ai_drug = target_for("AI_DRUG_DISCOVERY_PLATFORM")
        records = {record.case_id: record for record in round35_case_records()}

        self.assertIsNotNone(gene)
        self.assertIsNotNone(ai_drug)
        assert gene is not None
        assert ai_drug is not None
        self.assertEqual(gene.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertEqual(ai_drug.posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertIn("commercialization_slow", gene.red_flags)
        self.assertIn("cash_burn", gene.red_flags)
        self.assertIn("no_approved_drug", ai_drug.red_flags)
        self.assertIn("platform_hype", ai_drug.red_flags)
        self.assertEqual(records["bluebird_gene_therapy_approval_but_cash_crunch_4c"].case_type, "4c_thesis_break")
        self.assertEqual(records["ai_drug_no_approved_product_counterexample"].case_type, "failed_rerating")

    def test_contact_center_ai_can_be_green_possible_but_kiosk_stays_watch_first(self):
        contact = target_for("CONTACT_CENTER_AI_AUTOMATION")
        kiosk = target_for("SERVICE_KIOSK_SELF_CHECKOUT")
        markdown = render_round35_service_automation_markdown()
        records = {record.case_id: record for record in round35_case_records()}

        self.assertIsNotNone(contact)
        self.assertIsNotNone(kiosk)
        assert contact is not None
        assert kiosk is not None
        self.assertEqual(contact.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(kiosk.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("arr_growth", contact.green_conditions)
        self.assertIn("seat_expansion", contact.green_conditions)
        self.assertIn("poc_only", contact.red_flags)
        self.assertIn("theft", kiosk.red_flags)
        self.assertIn("pseudo_automation", kiosk.red_flags)
        self.assertEqual(records["five9_contact_center_software_candidate"].case_type, "success_candidate")
        self.assertEqual(records["self_checkout_theft_counterexample"].case_type, "failed_rerating")
        self.assertIn("recurring economics, not technology demos", markdown)

    def test_originator_defense_needs_successor_revenue_and_fcf_defense(self):
        target = target_for("BIOSIMILAR_ORIGINATOR_DEFENSE")
        records = {record.case_id: record for record in round35_case_records()}

        self.assertIsNotNone(target)
        assert target is not None
        self.assertEqual(target.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("successor_revenue_growth", target.green_conditions)
        self.assertIn("eps_fcf_defense", target.green_conditions)
        self.assertIn("biosimilar_erosion", target.red_flags)
        self.assertEqual(records["abbvie_rinvoq_skyrizi_successor_candidate"].case_type, "success_candidate")
        self.assertEqual(records["patent_cliff_no_successor_4c"].case_type, "4c_thesis_break")

    def test_case_records_validate_and_keep_backfill_open(self):
        records = round35_case_records()

        self.assertEqual(len(records), len(ROUND35_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.price_validation.price_validation_status, "needs_price_backfill")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("approval_or_market_size_alone_is_not_green", record.green_guardrails)

    def test_score_profile_rows_mark_no_production_change(self):
        for row in round35_score_profile_rows():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_summary_reports_v20_not_production_scoring(self):
        summary = round35_summary()
        markdown = render_round35_summary_markdown()

        self.assertEqual(summary["target_count"], 8)
        self.assertEqual(summary["case_candidate_count"], 32)
        self.assertEqual(summary["success_candidate_count"], 12)
        self.assertEqual(summary["stage4b_case_count"], 0)
        self.assertEqual(summary["stage4c_case_count"], 7)
        self.assertEqual(summary["green_possible_count"], 2)
        self.assertEqual(summary["watch_yellow_first_count"], 3)
        self.assertEqual(summary["redteam_first_count"], 3)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("production_scoring_changed: false", markdown)
        self.assertIn("Approval news, market-size narratives, AI labels, PoCs, and user/install counts are not score evidence", markdown)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round35_score_weight_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_v17_round35.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round35_v20.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["green_guardrails"].exists())
            self.assertTrue(paths["biotech_commercialization"].exists())
            self.assertTrue(paths["glp1_regulatory"].exists())
            self.assertTrue(paths["service_automation"].exists())
            self.assertTrue(paths["price_validation_plan"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND35_CASE_CANDIDATES))

    def test_cli_argument_parser_supports_paths(self):
        args = build_parser().parse_args(
            [
                "--output-directory",
                "out",
                "--cases",
                "cases.jsonl",
                "--score-profiles",
                "scores.csv",
            ]
        )

        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.cases, "cases.jsonl")
        self.assertEqual(args.score_profiles, "scores.csv")

    def test_production_scoring_modules_do_not_import_round35_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round35_score_weight_v20", text)


if __name__ == "__main__":
    unittest.main()
