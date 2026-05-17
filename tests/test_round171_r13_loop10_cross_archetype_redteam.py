import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round171_r13_loop10_report import build_parser
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round10_theme_tag_taxonomy import Round10ThemePosture
from e2r.sector.round171_r13_loop10_cross_archetype_redteam import (
    ROUND171_CASE_CANDIDATES,
    ROUND171_LARGE_SECTOR,
    ROUND171_OVERLAY_AXES,
    ROUND171_OVERLAY_TARGETS,
    ROUND171_STAGE_CAPS,
    ROUND171_SOURCE_CANONICAL_TARGET_COUNT,
    ROUND171_SOURCE_CANONICAL_TARGET_IDS,
    render_round171_price_validation_plan_markdown,
    render_round171_redteam_gate_plan_markdown,
    render_round171_summary_markdown,
    round171_case_candidate_rows,
    round171_case_records,
    round171_overlay_axis_rows,
    round171_price_field_rows,
    round171_score_profile_rows,
    round171_stage_date_rows,
    round171_stage_cap_rows,
    round171_summary,
    round171_target_for,
    write_round171_r13_loop10_reports,
)


class Round171R13Loop10CrossArchetypeRedTeamTests(unittest.TestCase):
    def test_round171_targets_cover_loop10_overlays(self):
        labels = {target.target_id for target in ROUND171_OVERLAY_TARGETS}

        self.assertEqual(len(labels), 22)
        self.assertEqual(ROUND171_SOURCE_CANONICAL_TARGET_COUNT, 16)
        self.assertTrue(set(ROUND171_SOURCE_CANONICAL_TARGET_IDS).issubset(labels))
        for label in (
            "STRUCTURAL_SUCCESS_ALIGNED",
            "STRUCTURAL_SUCCESS_BUT_4B_WATCH",
            "STAGE2_EVIDENCE_NOT_GREEN",
            "SECTOR_SUCCESS_BUT_POLICY_SHOCK_WATCH",
            "PRICE_ONLY_RALLY",
            "EVENT_PREMIUM",
            "EVENT_TO_CONTRACT_ESCALATION",
            "CYCLICAL_SUCCESS",
            "FALSE_POSITIVE_SCORE",
            "EVIDENCE_GOOD_BUT_PRICE_FAILED",
            "REDTEAM_ACCOUNTING_TRUST_OVERLAY",
            "OPERATIONAL_TRUST_BREAK",
            "LEGAL_REGULATORY_REDTEAM",
            "LEVERAGE_FCF_BREAKDOWN",
            "COMMERCIALIZATION_FAILURE",
            "AFFO_CASHFLOW_INTEGRITY_RISK",
            "CAPEX_AFFO_DILUTION_RISK",
            "STABLECOIN_CONVERTIBILITY_RISK",
            "CIRCULAR_AI_FINANCING_WATCH",
            "POLICY_MARKET_SHOCK_EVENT",
            "DISCLOSURE_CONFIDENCE_CAPPED",
            "UNKNOWN_INSUFFICIENT_EVIDENCE",
        ):
            self.assertIn(label, labels)

    def test_round171_overlay_axes_match_v10_cross_archetype_score_table(self):
        axes = {axis.axis_id: axis for axis in ROUND171_OVERLAY_AXES}

        self.assertEqual(
            {axis.axis_id: axis.weight for axis in ROUND171_OVERLAY_AXES},
            {
                "eps_fcf_roe_affo_opm_bodyweight_change": 24,
                "evidence_visibility": 20,
                "durability_repeatability": 16,
                "disclosure_confidence_redteam": 12,
                "capital_discipline_leverage_fcf": 10,
                "market_mispricing_rerating_gap": 10,
                "valuation_room_4b_margin": 8,
            },
        )
        self.assertEqual(
            [axis.axis_id for axis in ROUND171_OVERLAY_AXES],
            [
                "eps_fcf_roe_affo_opm_bodyweight_change",
                "evidence_visibility",
                "durability_repeatability",
                "disclosure_confidence_redteam",
                "capital_discipline_leverage_fcf",
                "market_mispricing_rerating_gap",
                "valuation_room_4b_margin",
            ],
        )
        self.assertIn("affo_integrity_break", axes["eps_fcf_roe_affo_opm_bodyweight_change"].stage4c_inputs)
        self.assertIn("government_order", axes["evidence_visibility"].stage2_cap_inputs)
        self.assertIn("recurring_revenue", axes["durability_repeatability"].stage2_cap_inputs)
        self.assertIn("policy_market_shock", axes["valuation_room_4b_margin"].stage4c_inputs)
        self.assertIn("circular_financing", axes["capital_discipline_leverage_fcf"].stage4c_inputs)
        self.assertIn("auditor_resignation", axes["disclosure_confidence_redteam"].stage4c_inputs)

        rows = round171_overlay_axis_rows()
        self.assertEqual(len(rows), 7)
        self.assertTrue(all(row["production_scoring_changed"] == "false" for row in rows))

    def test_stage_caps_make_round171_final_gate_explicit(self):
        rows = {row["cap_id"]: row for row in round171_stage_cap_rows()}

        self.assertEqual(len(rows), 4)
        self.assertEqual(len(ROUND171_STAGE_CAPS), 4)
        self.assertEqual(rows["stage1_theme_headline_cap"]["score_cap"], "45")
        self.assertIn("tam", rows["stage1_theme_headline_cap"]["cap_triggers"])
        self.assertIn("government_order", rows["stage1_theme_headline_cap"]["release_conditions"])
        self.assertEqual(rows["stage2_verified_evidence_cap"]["score_cap"], "70")
        self.assertIn("tenant_lease", rows["stage2_verified_evidence_cap"]["cap_triggers"])
        self.assertIn("price_path_aligned", rows["stage2_verified_evidence_cap"]["release_conditions"])
        self.assertEqual(rows["stage3_green_all_checks_gate"]["score_cap"], "requires_all_green_checks")
        self.assertIn("4b_valuation_room", rows["stage3_green_all_checks_gate"]["release_conditions"])
        self.assertIn("circular_ai_financing", rows["stage4b_4c_final_redteam_gate"]["hard_redteam_flags"])
        for row in rows.values():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_round171_new_canonical_archetypes_exist(self):
        expected = (
            E2RArchetype.EVENT_TO_CONTRACT_ESCALATION,
            E2RArchetype.STRUCTURAL_SUCCESS_BUT_4B_WATCH,
            E2RArchetype.STAGE2_EVIDENCE_NOT_GREEN,
            E2RArchetype.SECTOR_SUCCESS_BUT_POLICY_SHOCK_WATCH,
            E2RArchetype.COMMERCIALIZATION_FAILURE,
            E2RArchetype.AFFO_CASHFLOW_INTEGRITY_RISK,
            E2RArchetype.CAPEX_AFFO_DILUTION_RISK,
            E2RArchetype.STABLECOIN_CONVERTIBILITY_RISK,
            E2RArchetype.CIRCULAR_AI_FINANCING_WATCH,
            E2RArchetype.POLICY_MARKET_SHOCK_EVENT,
            E2RArchetype.DISCLOSURE_CONFIDENCE_CAPPED,
        )

        for archetype in expected:
            self.assertIsInstance(archetype.value, str)

    def test_round171_green_and_hard_gate_rules_are_explicit(self):
        structural = round171_target_for("STRUCTURAL_SUCCESS_ALIGNED")
        sector_4b = round171_target_for("STRUCTURAL_SUCCESS_BUT_4B_WATCH")
        accounting = round171_target_for("REDTEAM_ACCOUNTING_TRUST_OVERLAY")
        stablecoin = round171_target_for("STABLECOIN_CONVERTIBILITY_RISK")
        policy_success = round171_target_for("SECTOR_SUCCESS_BUT_POLICY_SHOCK_WATCH")
        policy_shock = round171_target_for("POLICY_MARKET_SHOCK_EVENT")
        circular = round171_target_for("CIRCULAR_AI_FINANCING_WATCH")
        event_contract = round171_target_for("EVENT_TO_CONTRACT_ESCALATION")
        capex_affo = round171_target_for("CAPEX_AFFO_DILUTION_RISK")
        disclosure_cap = round171_target_for("DISCLOSURE_CONFIDENCE_CAPPED")
        stage2_not_green = round171_target_for("STAGE2_EVIDENCE_NOT_GREEN")

        self.assertIsNotNone(structural)
        self.assertIsNotNone(sector_4b)
        self.assertIsNotNone(accounting)
        self.assertIsNotNone(stablecoin)
        self.assertIsNotNone(policy_success)
        self.assertIsNotNone(policy_shock)
        self.assertIsNotNone(circular)
        self.assertIsNotNone(event_contract)
        self.assertIsNotNone(capex_affo)
        self.assertIsNotNone(disclosure_cap)
        self.assertIsNotNone(stage2_not_green)
        assert structural is not None
        assert sector_4b is not None
        assert accounting is not None
        assert stablecoin is not None
        assert policy_success is not None
        assert policy_shock is not None
        assert circular is not None
        assert event_contract is not None
        assert capex_affo is not None
        assert disclosure_cap is not None
        assert stage2_not_green is not None
        self.assertEqual(structural.posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertTrue(structural.stage3_green_allowed)
        self.assertFalse(sector_4b.stage3_green_allowed)
        self.assertIn("valuation_saturation", sector_4b.red_flags)
        self.assertTrue(accounting.hard_gate)
        self.assertIn("auditor_resignation", accounting.red_flags)
        self.assertTrue(stablecoin.hard_gate)
        self.assertIn("depeg_event", stablecoin.red_flags)
        self.assertFalse(policy_success.hard_gate)
        self.assertIn("policy_market_shock", policy_success.red_flags)
        self.assertIn("policy_shock_4b_watch", policy_success.stage4b_conditions)
        self.assertTrue(policy_shock.hard_gate)
        self.assertIn("policy_market_shock", policy_shock.red_flags)
        self.assertIn("crowded_trade_unwind", policy_shock.stage4b_conditions)
        self.assertTrue(circular.hard_gate)
        self.assertIn("supplier_investor_customer_loop", circular.red_flags)
        self.assertEqual(circular.score_weight.redteam_gate, "ai_infra_hard_review")
        self.assertFalse(event_contract.hard_gate)
        self.assertIn("binding_contract", event_contract.stage2_signals)
        self.assertTrue(capex_affo.hard_gate)
        self.assertIn("capex_growth_above_affo_growth", capex_affo.stage4c_conditions)
        self.assertFalse(disclosure_cap.hard_gate)
        self.assertFalse(disclosure_cap.stage3_green_allowed)
        self.assertEqual(disclosure_cap.score_weight.redteam_gate, "stage3_confidence_cap")
        self.assertIn("detail_missing", disclosure_cap.red_flags)
        self.assertEqual(stage2_not_green.posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertFalse(stage2_not_green.stage3_green_allowed)
        self.assertEqual(stage2_not_green.score_weight.redteam_gate, "stage2_cap")
        self.assertIn("eps_fcf_conversion", stage2_not_green.green_conditions)
        self.assertIn("stage3_green_evidence_missing", stage2_not_green.red_flags)

    def test_required_round171_cases_are_present_with_stage_dates(self):
        rows = {row["case_id"]: row for row in round171_case_candidate_rows()}

        self.assertEqual(len(rows), len(ROUND171_CASE_CANDIDATES))
        self.assertEqual(rows["sk_hynix_hbm_memory_structural_4b_watch_case"]["stage4b_date"], "2026-05-14")
        self.assertEqual(rows["supermicro_accounting_trust_4c_case"]["stage4c_date"], "2024-10-30")
        self.assertEqual(rows["crowdstrike_operational_trust_break_case"]["stage4c_date"], "2024-07-31")
        self.assertEqual(rows["terrausd_luna_algorithmic_stablecoin_break_case"]["target_id"], "STABLECOIN_CONVERTIBILITY_RISK")
        self.assertEqual(rows["terrausd_luna_algorithmic_stablecoin_break_case"]["stage4c_date"], "2022-05-12")
        self.assertEqual(rows["bluebird_bio_commercialization_failure_case"]["target_id"], "COMMERCIALIZATION_FAILURE")
        self.assertEqual(rows["bluebird_bio_commercialization_failure_case"]["stage4c_date"], "2025-02-21")
        self.assertEqual(rows["novo_nordisk_glp1_4b_to_4c_case"]["stage4b_date"], "2025-07-29")
        self.assertEqual(rows["novo_nordisk_glp1_4b_to_4c_case"]["stage4c_date"], "2026-02-04")
        self.assertEqual(rows["korea_buyback_cancellation_policy_to_execution_case"]["target_id"], "EVENT_TO_CONTRACT_ESCALATION")
        self.assertEqual(rows["circle_regulated_stablecoin_infra_4b_watch_case"]["target_id"], "STRUCTURAL_SUCCESS_BUT_4B_WATCH")
        self.assertEqual(rows["circle_regulated_stablecoin_infra_4b_watch_case"]["stage4b_date"], "2026-05-11")
        self.assertEqual(rows["blackstone_digital_infra_trust_stage1_capped_case"]["target_id"], "DISCLOSURE_CONFIDENCE_CAPPED")
        self.assertEqual(rows["blackstone_digital_infra_trust_stage1_capped_case"]["stage1_date"], "2026-05-14")
        self.assertEqual(rows["fermi_ai_real_asset_no_revenue_case"]["target_id"], "DISCLOSURE_CONFIDENCE_CAPPED")
        self.assertEqual(rows["fermi_ai_real_asset_no_revenue_case"]["stage1_date"], "2025-09-30")
        self.assertEqual(rows["event_to_contract_escalation_reference_case"]["case_type"], "success_candidate")
        self.assertEqual(rows["korea_ai_tax_policy_market_shock_case"]["target_id"], "SECTOR_SUCCESS_BUT_POLICY_SHOCK_WATCH")
        self.assertEqual(rows["korea_ai_tax_policy_market_shock_case"]["stage4b_date"], "2026-05-12")
        self.assertEqual(rows["coreweave_nvidia_circular_financing_watch_case"]["target_id"], "CIRCULAR_AI_FINANCING_WATCH")
        self.assertEqual(rows["coreweave_nvidia_circular_financing_watch_case"]["stage1_date"], "2026-05-13")
        self.assertEqual(rows["equinix_affo_cashflow_integrity_case"]["target_id"], "AFFO_CASHFLOW_INTEGRITY_RISK")
        self.assertEqual(rows["equinix_capex_affo_dilution_case"]["target_id"], "CAPEX_AFFO_DILUTION_RISK")
        self.assertEqual(rows["equinix_capex_affo_dilution_case"]["stage4c_date"], "2026-05-08")
        self.assertEqual(rows["opendart_disclosure_confidence_cap_reference_case"]["target_id"], "DISCLOSURE_CONFIDENCE_CAPPED")
        self.assertEqual(rows["ge_vernova_power_equipment_backlog_structural_case"]["target_id"], "STRUCTURAL_SUCCESS_ALIGNED")
        self.assertEqual(rows["ge_vernova_power_equipment_backlog_structural_case"]["stage3_date"], "2026-04-22")
        self.assertEqual(rows["datadog_ai_observability_structural_case"]["target_id"], "STRUCTURAL_SUCCESS_ALIGNED")
        self.assertEqual(rows["fortinet_ai_security_billings_structural_case"]["target_id"], "STRUCTURAL_SUCCESS_ALIGNED")
        self.assertIn("billings_growth", rows["fortinet_ai_security_billings_structural_case"]["evidence_fields"])
        self.assertEqual(rows["cisco_ai_networking_orders_structural_case"]["target_id"], "STRUCTURAL_SUCCESS_ALIGNED")
        self.assertIn("hyperscaler_ai_orders", rows["cisco_ai_networking_orders_structural_case"]["evidence_fields"])
        self.assertEqual(rows["bavarian_nordic_stockpile_guidance_stage2_case"]["target_id"], "EVENT_TO_CONTRACT_ESCALATION")
        self.assertEqual(rows["bavarian_nordic_stockpile_guidance_stage2_case"]["stage2_date"], "2026-05-11")
        self.assertEqual(rows["bayer_crop_science_seed_ip_ebitda_stage2_case"]["target_id"], "EVENT_TO_CONTRACT_ESCALATION")
        self.assertEqual(rows["bayer_crop_science_seed_ip_ebitda_stage2_case"]["stage2_date"], "2026-05-12")
        self.assertEqual(rows["samyang_buldak_export_asp_structural_case"]["target_id"], "STRUCTURAL_SUCCESS_ALIGNED")
        self.assertEqual(rows["samsung_hbm4_shipment_stage2_case"]["target_id"], "EVENT_TO_CONTRACT_ESCALATION")
        self.assertEqual(rows["lges_tesla_ess_contract_stage2_case"]["target_id"], "EVENT_TO_CONTRACT_ESCALATION")
        self.assertEqual(rows["palantir_enterprise_ai_4b_watch_case"]["case_type"], "4b_watch")
        self.assertEqual(rows["apr_beauty_device_4b_watch_case"]["target_id"], "STRUCTURAL_SUCCESS_BUT_4B_WATCH")
        self.assertEqual(rows["whirlpool_hardware_cycle_fcf_breakdown_case"]["stage4c_date"], "2026-05-07")
        self.assertEqual(rows["lk99_replication_failure_false_positive_case"]["target_id"], "FALSE_POSITIVE_SCORE")

    def test_case_records_validate_and_keep_green_guardrails(self):
        records = round171_case_records()

        self.assertEqual(len(records), len(ROUND171_CASE_CANDIDATES))
        for record in records:
            record.validate()
            self.assertEqual(record.large_sector, ROUND171_LARGE_SECTOR)
            self.assertEqual(record.price_validation.price_validation_status, "needs_price_backfill")
            self.assertFalse(record.data_quality.price_data_available)
            self.assertIn("do_not_use_case_as_candidate_input", record.green_guardrails)
            self.assertIn("do_not_change_production_scoring", record.green_guardrails)
            self.assertIn(
                "stage3_green_requires_cross_evidence_eps_fcf_price_alignment_no_hard_redteam_no_saturated_4b",
                record.green_guardrails,
            )
            self.assertIn("hard_redteam_blocks_green", record.green_guardrails)

    def test_score_profile_rows_are_overlay_not_production_scoring(self):
        rows = round171_score_profile_rows()

        self.assertEqual(len(rows), len(ROUND171_OVERLAY_TARGETS))
        for row in rows:
            self.assertEqual(row["production_scoring_changed"], "false")
        by_target = {row["target_id"]: row for row in rows}
        self.assertEqual(by_target["REDTEAM_ACCOUNTING_TRUST_OVERLAY"]["redteam_gate"], "hard_block")
        self.assertEqual(by_target["AFFO_CASHFLOW_INTEGRITY_RISK"]["redteam_gate"], "reit_hard_review")
        self.assertEqual(by_target["CAPEX_AFFO_DILUTION_RISK"]["redteam_gate"], "reit_infra_hard_review")
        self.assertEqual(by_target["CAPEX_AFFO_DILUTION_RISK"]["hard_gate"], "true")
        self.assertEqual(by_target["STABLECOIN_CONVERTIBILITY_RISK"]["hard_gate"], "true")
        self.assertEqual(by_target["CIRCULAR_AI_FINANCING_WATCH"]["redteam_gate"], "ai_infra_hard_review")
        self.assertEqual(by_target["CIRCULAR_AI_FINANCING_WATCH"]["hard_gate"], "true")
        self.assertEqual(by_target["POLICY_MARKET_SHOCK_EVENT"]["redteam_gate"], "policy_price_path_shock")
        self.assertEqual(by_target["POLICY_MARKET_SHOCK_EVENT"]["hard_gate"], "true")
        self.assertEqual(by_target["DISCLOSURE_CONFIDENCE_CAPPED"]["redteam_gate"], "stage3_confidence_cap")
        self.assertEqual(by_target["DISCLOSURE_CONFIDENCE_CAPPED"]["eps_fcf"], "cap")
        self.assertEqual(by_target["STAGE2_EVIDENCE_NOT_GREEN"]["redteam_gate"], "stage2_cap")
        self.assertEqual(by_target["STAGE2_EVIDENCE_NOT_GREEN"]["stage3_green_allowed"], "false")
        self.assertEqual(by_target["PRICE_ONLY_RALLY"]["stage3_green_allowed"], "false")
        self.assertEqual(by_target["STRUCTURAL_SUCCESS_ALIGNED"]["stage3_green_allowed"], "true")

    def test_stage_date_and_price_fields_cover_loop10_needs(self):
        stage_rows = {row["target_id"]: row for row in round171_stage_date_rows()}
        price_fields = {row["field"] for row in round171_price_field_rows()}

        self.assertIn("auditor_resignation", stage_rows["REDTEAM_ACCOUNTING_TRUST_OVERLAY"]["stage4c"])
        self.assertIn("4b_watch", stage_rows["STRUCTURAL_SUCCESS_BUT_4B_WATCH"]["stage4b"])
        self.assertIn("eps_fcf_conversion", stage_rows["STAGE2_EVIDENCE_NOT_GREEN"]["stage3"])
        self.assertIn("stage3_green_evidence_missing", stage_rows["STAGE2_EVIDENCE_NOT_GREEN"]["stage4c"])
        self.assertIn("policy_shock_4b_watch", stage_rows["SECTOR_SUCCESS_BUT_POLICY_SHOCK_WATCH"]["stage4b"])
        self.assertIn("government_order", stage_rows["EVENT_TO_CONTRACT_ESCALATION"]["stage2"])
        self.assertIn("depeg", stage_rows["STABLECOIN_CONVERTIBILITY_RISK"]["stage4c"])
        self.assertIn("supplier_investor_customer_loop", stage_rows["CIRCULAR_AI_FINANCING_WATCH"]["stage4c"])
        self.assertIn("market_wide_policy_shock", stage_rows["POLICY_MARKET_SHOCK_EVENT"]["stage4c"])
        self.assertIn("capex_growth_above_affo_growth", stage_rows["CAPEX_AFFO_DILUTION_RISK"]["stage4c"])
        self.assertIn("detail_missing", stage_rows["DISCLOSURE_CONFIDENCE_CAPPED"]["stage4c"])
        self.assertIn("MFE_5D", price_fields)
        self.assertIn("MFE_2Y", price_fields)
        self.assertIn("MAE_1Y", price_fields)
        self.assertIn("opendart_detail_fetched_flag", price_fields)
        self.assertIn("contract_amount_disclosed_flag", price_fields)
        self.assertIn("customer_name_disclosed_flag", price_fields)
        self.assertIn("auditor_resignation_flag", price_fields)
        self.assertIn("operational_trust_break_flag", price_fields)
        self.assertIn("affo_integrity_risk_flag", price_fields)
        self.assertIn("capex_to_affo_ratio", price_fields)
        self.assertIn("capex_affo_dilution_risk_flag", price_fields)
        self.assertIn("capex_growth_above_affo_growth_flag", price_fields)
        self.assertIn("power_water_permitting_flag", price_fields)
        self.assertIn("ai_power_campus_flag", price_fields)
        self.assertIn("asset_acquired_flag", price_fields)
        self.assertIn("binding_lease_flag", price_fields)
        self.assertIn("binding_tenant_lease_absent", price_fields)
        self.assertIn("no_revenue_flag", price_fields)
        self.assertIn("power_delivery_long_dated_flag", price_fields)
        self.assertIn("stablecoin_type", price_fields)
        self.assertIn("stablecoin_circulation", price_fields)
        self.assertIn("reserve_income", price_fields)
        self.assertIn("redemption_at_par_flag", price_fields)
        self.assertIn("algorithmic_stablecoin_flag", price_fields)
        self.assertIn("circular_financing_flag", price_fields)
        self.assertIn("supplier_investor_customer_loop_flag", price_fields)
        self.assertIn("capacity_guarantee_flag", price_fields)
        self.assertIn("gpu_collateral_debt_flag", price_fields)
        self.assertIn("customer_contract_concentration", price_fields)
        self.assertIn("policy_market_shock_flag", price_fields)
        self.assertIn("disclosure_confidence_capped_flag", price_fields)
        self.assertIn("stage_confidence_cap_reason", price_fields)
        self.assertIn("stage_after_redteam", price_fields)
        self.assertIn("sk_hynix_return_2025_pct", price_fields)
        self.assertIn("sk_hynix_return_2026_pct", price_fields)
        self.assertIn("market_cap_usd", price_fields)
        self.assertIn("one_two_year_runup_pct", price_fields)
        self.assertIn("datadog_revenue_growth_pct", price_fields)
        self.assertIn("fortinet_billings_growth_pct", price_fields)
        self.assertIn("circle_usdc_circulation", price_fields)
        self.assertIn("circle_reserve_income", price_fields)
        self.assertIn("usdc_circulation_growth_pct", price_fields)
        self.assertIn("ai_payment_option_flag", price_fields)
        self.assertIn("bayer_crop_science_ebitda_growth_pct", price_fields)
        self.assertIn("supermicro_auditor_resignation_drop_pct", price_fields)
        self.assertIn("crowdstrike_affected_devices_count", price_fields)
        self.assertIn("crowdstrike_market_cap_loss_usd", price_fields)
        self.assertIn("novo_revenue_decline_guidance_pct", price_fields)
        self.assertIn("coreweave_unused_capacity_agreement", price_fields)
        self.assertIn("nvidia_foundation_compute_purchase", price_fields)
        self.assertIn("fermi_project_tenant_absent_flag", price_fields)
        self.assertIn("fermi_funding_agreement_terminated_flag", price_fields)

    def test_summary_and_markdown_explain_loop10_validation_layer(self):
        summary = round171_summary()
        summary_md = render_round171_summary_markdown()
        gate_plan = render_round171_redteam_gate_plan_markdown()
        price_plan = render_round171_price_validation_plan_markdown()

        self.assertEqual(summary["target_count"], 22)
        self.assertEqual(summary["source_canonical_target_count"], 16)
        self.assertEqual(summary["overlay_axis_count"], 7)
        self.assertEqual(summary["stage_cap_count"], 4)
        self.assertEqual(summary["case_candidate_count"], 46)
        self.assertEqual(summary["structural_success_count"], 3)
        self.assertEqual(summary["success_candidate_count"], 14)
        self.assertEqual(summary["cyclical_success_count"], 1)
        self.assertEqual(summary["event_premium_count"], 1)
        self.assertEqual(summary["overheat_count"], 1)
        self.assertEqual(summary["failed_rerating_count"], 8)
        self.assertEqual(summary["stage4b_case_count"], 8)
        self.assertEqual(summary["stage4c_case_count"], 12)
        self.assertEqual(summary["hard_gate_target_count"], 10)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertIn("production_scoring_changed: false", summary_md)
        self.assertIn("common validation overlay", summary_md)
        self.assertIn("source_canonical_target_count: 16", summary_md)
        self.assertIn("source note names 16 canonical buckets", summary_md)
        self.assertIn("R13 v10 Cross-Archetype Overlay Axes", summary_md)
        self.assertIn("`eps_fcf_roe_affo_opm_bodyweight_change`: 24", summary_md)
        self.assertIn("R13 v10 Stage Caps", summary_md)
        self.assertIn("`stage3_green_all_checks_gate`: Stage 3 / requires_all_green_checks", summary_md)
        self.assertIn("Do not apply Round171 overlay symbols", gate_plan)
        self.assertIn("capex/AFFO dilution", gate_plan)
        self.assertIn("circular AI financing", gate_plan)
        self.assertIn("score-before-RedTeam", price_plan)
        self.assertIn("disclosure_confidence_capped", price_plan)

    def test_report_writer_outputs_cases_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round171_r13_loop10_reports(
                output_directory=Path(tmp) / "out",
                cases_path=Path(tmp) / "cases_r13_loop10_round171.jsonl",
                score_profile_path=Path(tmp) / "score_weight_profiles_round171_r13_loop10_v10.csv",
            )

            self.assertTrue(paths["cases"].exists())
            self.assertTrue(paths["score_profiles"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["case_matrix"].exists())
            self.assertTrue(paths["target_matrix"].exists())
            self.assertTrue(paths["stage_date_plan"].exists())
            self.assertTrue(paths["redteam_gate_plan"].exists())
            self.assertTrue(paths["price_validation_plan"].exists())
            self.assertTrue(paths["price_fields"].exists())
            self.assertTrue(paths["overlay_axes"].exists())
            self.assertTrue(paths["stage_caps"].exists())
            self.assertEqual(len(load_case_library(paths["cases"])), len(ROUND171_CASE_CANDIDATES))

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

    def test_production_scoring_modules_do_not_import_round171_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round171_r13_loop10_cross_archetype_redteam", text)


if __name__ == "__main__":
    unittest.main()
