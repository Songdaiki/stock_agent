import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round178_r7_loop11_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10LargeSector, Round10ThemePosture
from e2r.sector.round178_r7_loop11_biotech_healthcare_device import (
    ROUND178_BASE_SCORE_WEIGHTS,
    ROUND178_CASE_CANDIDATES,
    ROUND178_HELPER_OVERLAY_TARGET_COUNT,
    ROUND178_HELPER_OVERLAY_TARGET_IDS,
    ROUND178_PRICE_FIELDS,
    ROUND178_SCORE_STAGE_PRICE_ALIGNMENT,
    ROUND178_SCORE_TARGETS,
    ROUND178_SOURCE_CANONICAL_TARGET_COUNT,
    ROUND178_SOURCE_CANONICAL_TARGET_IDS,
    ROUND178_STAGE_CAPS,
    render_round178_green_guardrail_markdown,
    render_round178_price_validation_plan_markdown,
    render_round178_risk_overlay_markdown,
    render_round178_score_stage_price_alignment_markdown,
    render_round178_summary_markdown,
    round178_base_score_weight_rows,
    round178_case_candidate_rows,
    round178_case_records,
    round178_price_field_rows,
    round178_score_profile_rows,
    round178_score_stage_price_alignment_rows,
    round178_stage_cap_rows,
    round178_stage_date_rows,
    round178_summary,
    round178_target_for,
    write_round178_r7_loop11_reports,
)


class Round178R7Loop11BiotechHealthcareDeviceTests(unittest.TestCase):
    def test_round178_targets_cover_source_and_helper_overlay(self):
        labels = {target.target_id for target in ROUND178_SCORE_TARGETS}

        self.assertEqual(ROUND178_SOURCE_CANONICAL_TARGET_COUNT, 14)
        self.assertEqual(ROUND178_HELPER_OVERLAY_TARGET_COUNT, 1)
        self.assertEqual(len(labels), 15)
        self.assertTrue(set(ROUND178_SOURCE_CANONICAL_TARGET_IDS).issubset(labels))
        self.assertEqual(set(ROUND178_HELPER_OVERLAY_TARGET_IDS), {"DEVICE_SAFETY_CHANNEL_OVERLAY"})
        for target in ROUND178_SCORE_TARGETS:
            self.assertEqual(target.large_sector, Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE)
            self.assertFalse(target.production_scoring_changed)

    def test_new_r7_loop11_korea_healthcare_archetypes_exist(self):
        expected = (
            E2RArchetype.SC_FORMULATION_ROYALTY_PLATFORM,
            E2RArchetype.BLOCKBUSTER_LIFE_EXTENSION_ROYALTY,
            E2RArchetype.KOREA_ONCOLOGY_DRUG_COMMERCIALIZATION,
            E2RArchetype.BIOSIMILAR_TARIFF_HEDGE_MANUFACTURING,
            E2RArchetype.BIOSIMILAR_COMMERCIALIZATION_KOREA,
            E2RArchetype.BOTULINUM_US_MARKET_ENTRY,
            E2RArchetype.AESTHETIC_DEVICE_EXPORT_KOREA,
            E2RArchetype.BIOTECH_LICENSE_MILESTONE_PLATFORM,
            E2RArchetype.GLP1_GENERIC_THEME_KOREA,
            E2RArchetype.MEDICAL_AI_REIMBURSEMENT_KOREA,
            E2RArchetype.APPROVAL_ONLY_NOT_COMMERCIALIZATION,
            E2RArchetype.MANUFACTURING_INSPECTION_CRL_OVERLAY,
            E2RArchetype.PATENT_CHALLENGE_OVERLAY,
            E2RArchetype.DEVICE_SAFETY_CHANNEL_OVERLAY,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_loop11_base_score_weights_and_stage_caps_match_round_note(self):
        weights = {row["component"]: row for row in round178_base_score_weight_rows()}
        caps = {row["stage_band"]: row for row in round178_stage_cap_rows()}

        self.assertEqual(len(ROUND178_BASE_SCORE_WEIGHTS), 7)
        self.assertEqual(weights["commercialization_eps_fcf_conversion"]["points"], "24")
        self.assertEqual(weights["prescription_royalty_reimbursement_repeat_revenue_visibility"]["points"], "22")
        self.assertEqual(weights["partner_approval_contract_visibility"]["points"], "16")
        self.assertEqual(weights["safety_regulatory_cmc_patent_disclosure_confidence"]["points"], "14")
        self.assertEqual(weights["early_price_path_validation"]["points"], "10")
        self.assertEqual(weights["cash_runway_capital_discipline"]["points"], "8")
        self.assertEqual(weights["valuation_room_4b_runway"]["points"], "6")
        self.assertEqual(len(ROUND178_STAGE_CAPS), 5)
        self.assertEqual(caps["Stage 1"]["max_score"], "45")
        self.assertEqual(caps["Stage 2"]["max_score"], "70")
        self.assertIn("requires_5_of_8", caps["Stage 3"]["max_score"])
        self.assertIn("stage2_60d_mfe_20pct", caps["Stage 3"]["required_evidence"])
        self.assertIn("requires_3_of_5", caps["Stage 4B"]["max_score"])
        self.assertIn("manufacturing_inspection_issue", caps["Stage 4C"]["required_evidence"])

    def test_target_rules_separate_commercialization_from_approval_only(self):
        alteogen = round178_target_for("SC_FORMULATION_ROYALTY_PLATFORM")
        oncology = round178_target_for("KOREA_ONCOLOGY_DRUG_COMMERCIALIZATION")
        celltrion = round178_target_for("BIOSIMILAR_TARIFF_HEDGE_MANUFACTURING")
        hugel = round178_target_for("BOTULINUM_US_MARKET_ENTRY")
        classys = round178_target_for("AESTHETIC_DEVICE_EXPORT_KOREA")
        license_platform = round178_target_for("BIOTECH_LICENSE_MILESTONE_PLATFORM")
        glp1 = round178_target_for("GLP1_GENERIC_THEME_KOREA")
        ai = round178_target_for("MEDICAL_AI_REIMBURSEMENT_KOREA")
        approval_cap = round178_target_for("APPROVAL_ONLY_NOT_COMMERCIALIZATION")
        cmc = round178_target_for("MANUFACTURING_INSPECTION_CRL_OVERLAY")
        patent = round178_target_for("PATENT_CHALLENGE_OVERLAY")
        disclosure = round178_target_for("DISCLOSURE_CONFIDENCE_CAP")
        device_safety = round178_target_for("DEVICE_SAFETY_CHANNEL_OVERLAY")

        for target in (alteogen, oncology, celltrion, hugel, classys, license_platform, glp1, ai, approval_cap, cmc, patent, disclosure, device_safety):
            self.assertIsNotNone(target)
        assert alteogen is not None
        assert oncology is not None
        assert celltrion is not None
        assert hugel is not None
        assert classys is not None
        assert license_platform is not None
        assert glp1 is not None
        assert ai is not None
        assert approval_cap is not None
        assert cmc is not None
        assert patent is not None
        assert disclosure is not None
        assert device_safety is not None
        self.assertEqual(alteogen.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertIn("royalty_revenue", alteogen.green_conditions)
        self.assertIn("scripts", oncology.green_conditions)
        self.assertEqual(celltrion.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("facility_utilization", celltrion.green_conditions)
        self.assertIn("us_sales", hugel.green_conditions)
        self.assertIn("consumable_revenue", classys.green_conditions)
        self.assertEqual(license_platform.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertTrue(glp1.gate_only)
        self.assertIn("patent_overhang", glp1.red_flags)
        self.assertEqual(ai.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertIn("reimbursement_revenue", ai.green_conditions)
        self.assertTrue(approval_cap.gate_only)
        self.assertTrue(cmc.gate_only)
        self.assertTrue(patent.gate_only)
        self.assertEqual(disclosure.score_weight.commercialization_eps_fcf_conversion, "cap")
        self.assertTrue(device_safety.gate_only)

    def test_required_round178_cases_are_present_with_stage_markers(self):
        rows = {row["case_id"]: row for row in round178_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND178_CASE_CANDIDATES))
        self.assertEqual(rows["alteogen_keytruda_sc_royalty_stage3_candidate"]["target_id"], "SC_FORMULATION_ROYALTY_PLATFORM")
        self.assertEqual(rows["alteogen_keytruda_sc_royalty_stage3_candidate"]["stage2_date"], "2025-09-19")
        self.assertEqual(rows["alteogen_keytruda_sc_royalty_stage3_candidate"]["stage4b_date"], "2025-09-19")
        self.assertIn("keytruda_qlex_fda_approval", rows["alteogen_keytruda_sc_royalty_stage3_candidate"]["evidence_fields"])
        self.assertEqual(rows["yuhan_lazertinib_oncology_commercialization_case"]["stage2_date"], "2024-08-20")
        self.assertEqual(rows["celltrion_us_factory_tariff_hedge_stage2_case"]["stage2_date"], "2025-09-23")
        self.assertEqual(rows["hugel_letybo_us_market_entry_case"]["target_id"], "BOTULINUM_US_MARKET_ENTRY")
        self.assertEqual(rows["classys_aesthetic_device_export_consumable_case"]["target_id"], "AESTHETIC_DEVICE_EXPORT_KOREA")
        self.assertEqual(rows["ablbio_lilly_license_milestone_platform_case"]["target_id"], "BIOTECH_LICENSE_MILESTONE_PLATFORM")
        self.assertEqual(rows["samchundang_biosimilar_glp1_patent_watch_case"]["case_type"], "4b_watch")
        self.assertEqual(rows["jj_rybrevant_sc_crl_inspection_overlay_case"]["stage4c_date"], "2024-12-16")
        self.assertEqual(rows["merck_keytruda_qlex_approval_price_failed_case"]["stage2_date"], "2025-09-19")
        self.assertEqual(rows["medical_ai_reimbursement_korea_gate_case"]["case_type"], "event_premium")
        self.assertEqual(rows["device_safety_channel_overlay_case"]["target_id"], "DEVICE_SAFETY_CHANNEL_OVERLAY")
        self.assertEqual(rows["biotech_disclosure_confidence_cap_case"]["target_id"], "DISCLOSURE_CONFIDENCE_CAP")

    def test_case_records_validate_and_keep_round178_guardrails(self):
        records = round178_case_records()

        self.assertEqual(len(records), len(ROUND178_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, "BIOTECH_HEALTHCARE_DEVICE")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn("approval_license_ai_performance_is_not_commercialization", record.green_guardrails)
            self.assertIn("require_royalty_scripts_reimbursement_repeat_revenue_commercial_sales_opm_fcf_for_green", record.green_guardrails)
            self.assertIn("stage3_early_catch_requires_5_of_8_loop11_conditions", record.green_guardrails)
            self.assertIn("do_not_invent_contract_amount_upfront_milestone_royalty_rate_scripts_reimbursement_commercial_sales_stage_prices_or_mfe_mae", record.green_guardrails)
        by_id = {record.case_id: record for record in records}
        self.assertEqual(by_id["alteogen_keytruda_sc_royalty_stage3_candidate"].score_price_alignment, "price_moved_without_evidence")
        self.assertIn(E2RArchetype.PATENT_CHALLENGE_OVERLAY, by_id["alteogen_keytruda_sc_royalty_stage3_candidate"].secondary_archetypes)
        self.assertIn("royalty_revenue", by_id["alteogen_keytruda_sc_royalty_stage3_candidate"].must_have_fields)
        self.assertEqual(by_id["jj_rybrevant_sc_crl_inspection_overlay_case"].rerating_result, "thesis_break")
        self.assertEqual(by_id["medical_ai_reimbursement_korea_gate_case"].rerating_result, "event_premium")
        self.assertEqual(by_id["merck_keytruda_qlex_approval_price_failed_case"].score_price_alignment, "evidence_good_but_price_failed")

    def test_score_profile_rows_mark_no_production_change(self):
        rows = round178_score_profile_rows()

        self.assertEqual(len(rows), len(ROUND178_SCORE_TARGETS))
        for row in rows:
            self.assertEqual(row["large_sector"], "BIOTECH_HEALTHCARE_DEVICE")
            self.assertEqual(row["production_scoring_changed"], "false")
            self.assertIn("loop11_penalty_axes", row)
        by_target = {row["target_id"]: row for row in rows}
        self.assertEqual(by_target["SC_FORMULATION_ROYALTY_PLATFORM"]["commercialization_eps_fcf_conversion"], "24")
        self.assertEqual(by_target["KOREA_ONCOLOGY_DRUG_COMMERCIALIZATION"]["prescription_royalty_reimbursement_repeat_revenue_visibility"], "23")
        self.assertEqual(by_target["BIOSIMILAR_TARIFF_HEDGE_MANUFACTURING"]["posture"], Round10ThemePosture.WATCH_YELLOW_FIRST.value)
        self.assertEqual(by_target["GLP1_GENERIC_THEME_KOREA"]["gate_only"], "true")
        self.assertEqual(by_target["APPROVAL_ONLY_NOT_COMMERCIALIZATION"]["commercialization_eps_fcf_conversion"], "gate")
        self.assertEqual(by_target["DISCLOSURE_CONFIDENCE_CAP"]["commercialization_eps_fcf_conversion"], "cap")
        self.assertEqual(by_target["DEVICE_SAFETY_CHANNEL_OVERLAY"]["gate_only"], "true")

    def test_stage_date_and_price_field_plans_are_explicit(self):
        rows = {row["target_id"]: row for row in round178_stage_date_rows()}
        fields = {row["field"] for row in round178_price_field_rows()}

        self.assertIn("royalty_revenue", rows["SC_FORMULATION_ROYALTY_PLATFORM"]["stage3"])
        self.assertIn("scripts", rows["KOREA_ONCOLOGY_DRUG_COMMERCIALIZATION"]["stage3"])
        self.assertIn("facility_utilization", rows["BIOSIMILAR_TARIFF_HEDGE_MANUFACTURING"]["stage3"])
        self.assertIn("us_sales", rows["BOTULINUM_US_MARKET_ENTRY"]["stage3"])
        self.assertIn("reimbursement_absent", rows["MEDICAL_AI_REIMBURSEMENT_KOREA"]["stage4c"])
        for field in (
            "approval_status",
            "approval_date",
            "partner_name",
            "contract_amount",
            "upfront_amount",
            "milestone_amount",
            "royalty_rate_if_disclosed",
            "territory",
            "launch_date",
            "commercial_sales",
            "prescription_volume",
            "procedure_volume",
            "reimbursement_status",
            "pbm_or_formulary_status",
            "medical_fee_code_status",
            "royalty_revenue",
            "cash_runway_months",
            "dilution_event_flag",
            "crl_flag",
            "manufacturing_inspection_issue_flag",
            "patent_litigation_flag",
            "safety_warning_flag",
            "reimbursement_failure_flag",
            "disclosure_confidence",
            "valuation_at_stage3",
            "valuation_at_stage4b",
        ):
            self.assertIn(field, fields)

    def test_score_stage_price_alignment_rows_and_markdown(self):
        rows = {row["case_id"]: row for row in round178_score_stage_price_alignment_rows()}
        markdown = render_round178_score_stage_price_alignment_markdown()

        self.assertEqual(len(rows), len(ROUND178_SCORE_STAGE_PRICE_ALIGNMENT))
        self.assertEqual(rows["alteogen_keytruda_sc_royalty_stage3_candidate"]["verdict"], "royalty_platform_requires_adoption_revenue_and_4b_cooling")
        self.assertEqual(rows["medical_ai_reimbursement_korea_gate_case"]["verdict"], "medical_ai_reimbursement_required")
        self.assertEqual(rows["jj_rybrevant_sc_crl_inspection_overlay_case"]["verdict"], "cmc_crl_blocks_unsafe_green")
        self.assertIn("Alteogen", markdown)
        self.assertIn("CRL", markdown)
        self.assertIn("reimbursement", markdown)

    def test_summary_and_markdown_explain_r7_loop11_guardrails(self):
        summary = round178_summary()
        summary_md = render_round178_summary_markdown()
        guardrails = render_round178_green_guardrail_markdown()
        overlays = render_round178_risk_overlay_markdown()
        price_plan = render_round178_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 15)
        self.assertEqual(summary["source_canonical_target_count"], 14)
        self.assertEqual(summary["helper_overlay_target_count"], 1)
        self.assertEqual(summary["case_candidate_count"], len(ROUND178_CASE_CANDIDATES))
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["case_records_are_candidate_generation_input"])
        self.assertIn("Alteogen", summary_md)
        self.assertIn("approval/license/AI performance", guardrails)
        self.assertIn("Merck", overlays)
        self.assertIn("royalty", price_plan)
        self.assertIn("medical_ai_reimbursement_korea_gate_case", price_plan)

    def test_reports_are_written_and_case_jsonl_loads(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = write_round178_r7_loop11_reports(
                output_directory=root / "reports",
                cases_path=root / "cases.jsonl",
                score_profile_path=root / "score_profiles.csv",
            )
            records = load_case_library(paths["cases"])

            self.assertEqual(len(records), len(ROUND178_CASE_CANDIDATES))
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["stage_date_plan"].exists())
            self.assertTrue(paths["price_fields"].exists())
            self.assertIn("Keytruda", paths["summary"].read_text(encoding="utf-8"))
            self.assertIn("approval_license_ai_performance_is_not_commercialization", paths["cases"].read_text(encoding="utf-8"))

    def test_cli_argument_parsing(self):
        args = build_parser().parse_args(
            [
                "--output-directory",
                "tmp_reports",
                "--cases",
                "tmp_cases.jsonl",
                "--score-profiles",
                "tmp_profiles.csv",
            ]
        )

        self.assertEqual(args.output_directory, "tmp_reports")
        self.assertEqual(args.cases, "tmp_cases.jsonl")
        self.assertEqual(args.score_profiles, "tmp_profiles.csv")

    def test_production_modules_do_not_import_round178(self):
        forbidden = "round178_r7_loop11_biotech_healthcare_device"
        for rel_path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(rel_path).read_text(encoding="utf-8")
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
