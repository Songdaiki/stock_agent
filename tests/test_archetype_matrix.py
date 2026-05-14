import tempfile
from pathlib import Path
import unittest

from e2r.sector.archetype_matrix import (
    ROUND2_ARCHETYPE_MATRIX,
    ROUND2_DEEP_DIVE_PRIORITY_GROUPS,
    ROUND2_FIRST_SHADOW_SCORING_ARCHETYPES,
    ROUND2_PEER_NORMALIZATION_METRICS,
    ROUND2_PROMOTION_BANDS,
    all_matrix_entries,
    deep_dive_priority_tier,
    first_shadow_scoring_candidate,
    matrix_entry,
    round2_case_gap_summary,
    write_round2_matrix_reports,
)
from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.research_framework import ROUND1_CORE_ARCHETYPES


class ArchetypeMatrixTests(unittest.TestCase):
    def test_round2_matrix_covers_round1_core_archetypes(self):
        self.assertEqual(set(ROUND2_ARCHETYPE_MATRIX), set(ROUND1_CORE_ARCHETYPES))
        self.assertEqual(len(all_matrix_entries()), 25)

    def test_contract_and_consumer_green_gates_are_different(self):
        contract = matrix_entry(E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL)
        consumer = matrix_entry(E2RArchetype.EXPORT_RECURRING_CONSUMER)

        self.assertIn("contract_amount_to_sales_10pct_plus", contract.stage2_signals)
        self.assertIn("backlog_to_sales_100pct_plus", contract.stage3_signals)
        self.assertIn("recurring_consumption", consumer.stage3_signals)
        self.assertNotIn("contract_amount_to_sales_10pct_plus", consumer.stage2_signals)
        self.assertIn("Contract quality is not required", consumer.green_gate_policy)

    def test_memory_and_shipping_are_not_scored_like_same_sector(self):
        memory = matrix_entry(E2RArchetype.MEMORY_HBM_CAPACITY)
        shipping = matrix_entry(E2RArchetype.SHIPPING_FREIGHT_CYCLE)

        self.assertEqual(memory.score_weight_hint["eps_fcf"], 24)
        self.assertEqual(shipping.score_weight_hint["valuation_rerating"], 8)
        self.assertTrue(shipping.green_restricted)
        self.assertIn("multi_year_consensus_revision", memory.stage3_signals)

    def test_one_off_and_theme_are_green_guardrail_archetypes(self):
        one_off = matrix_entry(E2RArchetype.ONE_OFF_EVENT_DEMAND)
        theme = matrix_entry(E2RArchetype.THEME_VALUATION_OVERHEAT)

        self.assertTrue(one_off.green_restricted)
        self.assertTrue(theme.green_restricted)
        self.assertIn("green_blocked_unless_recurrence_proven", one_off.stage3_signals)
        self.assertIn("green_extremely_limited", theme.stage3_signals)

    def test_peer_normalization_metrics_are_explicit(self):
        self.assertIn("sector_eps_growth_percentile", ROUND2_PEER_NORMALIZATION_METRICS)
        self.assertIn("sector_trading_value_spike_percentile", ROUND2_PEER_NORMALIZATION_METRICS)

    def test_round_01_priority_layers_are_separate(self):
        self.assertIn(E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG, ROUND2_DEEP_DIVE_PRIORITY_GROUPS[1])
        self.assertIn(E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT, ROUND2_DEEP_DIVE_PRIORITY_GROUPS[1])
        self.assertEqual(len(ROUND2_FIRST_SHADOW_SCORING_ARCHETYPES), 10)
        self.assertTrue(first_shadow_scoring_candidate(E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET))
        self.assertTrue(first_shadow_scoring_candidate(E2RArchetype.ONE_OFF_EVENT_DEMAND))
        self.assertTrue(first_shadow_scoring_candidate(E2RArchetype.THEME_VALUATION_OVERHEAT))
        self.assertEqual(deep_dive_priority_tier(E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG), 1)
        self.assertEqual(deep_dive_priority_tier(E2RArchetype.PLATFORM_SOFTWARE_INTERNET), 2)

    def test_promotion_bands_include_stage_watch_without_changing_stage(self):
        self.assertIn("Stage 2-High", ROUND2_PROMOTION_BANDS)
        self.assertIn("Stage 3-Watch", ROUND2_PROMOTION_BANDS)

    def test_case_gap_summary_uses_round1_rollup(self):
        records = load_case_library("data/e2r_case_library/cases_v02.jsonl")
        rows = round2_case_gap_summary(records)
        by_archetype = {row["archetype"]: row for row in rows}

        self.assertEqual(by_archetype["K_BEAUTY_EXPORT_DISTRIBUTION"]["status"], "covered_2x2")
        self.assertGreaterEqual(by_archetype["SEMI_EQUIPMENT_CAPEX"]["positive_count"], 2)
        self.assertTrue(by_archetype["SEMI_EQUIPMENT_CAPEX"]["first_shadow_scoring_candidate"])
        self.assertEqual(by_archetype["SHIPBUILDING_OFFSHORE_BACKLOG"]["deep_dive_priority_tier"], 1)
        self.assertIn(by_archetype["ONE_OFF_EVENT_DEMAND"]["status"], {"needs_more_counterexamples", "green_guardrail_only"})

    def test_report_writer_outputs_matrix_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round2_matrix_reports(output_directory=tmp)

            self.assertTrue(paths["matrix"].exists())
            self.assertTrue(paths["weights"].exists())
            self.assertTrue(paths["priority"].exists())
            self.assertTrue(paths["peer_metrics"].exists())
            self.assertTrue(paths["case_gap_matrix"].exists())
            self.assertTrue(paths["shadow_scoring_plan"].exists())
            self.assertIn("Round-2 E2R Archetype Matrix", paths["matrix"].read_text(encoding="utf-8"))
            self.assertIn("Stage 3-Watch", paths["priority"].read_text(encoding="utf-8"))

    def test_production_scoring_modules_do_not_import_round2_matrix(self):
        paths = [
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ]
        for path in paths:
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("archetype_matrix", text)


if __name__ == "__main__":
    unittest.main()
