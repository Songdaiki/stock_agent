import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round40_round_protocol_report import build_parser
from e2r.sector.round10_theme_tag_taxonomy import ROUND10_LARGE_SECTORS
from e2r.sector.round40_round_protocol import (
    ROUND40_ALIGNMENT_VALUES,
    ROUND40_ROUND_PLANS,
    ROUND40_VALIDATION_PROTOCOL,
    render_round40_price_alignment_markdown,
    render_round40_round_sequence_markdown,
    render_round40_summary_markdown,
    render_round40_validation_protocol_markdown,
    round40_round_plan_rows,
    round40_summary,
    round40_validation_protocol_rows,
    write_round40_round_protocol_reports,
)


class Round40RoundProtocolTests(unittest.TestCase):
    def test_round40_keeps_twelve_sector_rounds_and_one_cross_overlay(self):
        summary = round40_summary()

        self.assertEqual(summary["large_sector_count"], 12)
        self.assertEqual(summary["round_count"], 13)
        self.assertEqual(summary["sector_round_count"], 12)
        self.assertEqual(summary["cross_overlay_round_count"], 1)
        self.assertGreaterEqual(summary["canonical_archetype_mentions"], 70)
        self.assertGreaterEqual(summary["deep_sub_archetype_mentions"], 90)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["round_plan_is_candidate_generation_input"])

    def test_r1_r2_and_r13_capture_round40_map(self):
        rows = {row["round_id"]: row for row in round40_round_plan_rows()}

        self.assertEqual(rows["R1"]["large_sector"], "INDUSTRIAL_ORDERS_INFRA")
        self.assertIn("GRID_TRANSFORMER_SHORTAGE", rows["R1"]["canonical_archetypes"])
        self.assertIn("AI_DATA_CENTER_POWER_EQUIPMENT", rows["R1"]["canonical_archetypes"])
        self.assertEqual(rows["R2"]["large_sector"], "AI_SEMICONDUCTOR_ELECTRONICS")
        self.assertIn("NEOCLOUD_GPU_RENTAL", rows["R2"]["canonical_archetypes"])
        self.assertIn("REDTEAM_ACCOUNTING_TRUST_OVERLAY", rows["R2"]["canonical_archetypes"])
        self.assertEqual(rows["R13"]["large_sector"], "CROSS_ARCHETYPE_OVERLAY")
        self.assertIn("PRICE_ONLY_RALLY", rows["R13"]["canonical_archetypes"])
        self.assertIn("hard_4c", rows["R13"]["validation_focus"])

    def test_each_sector_round_maps_to_existing_large_sector(self):
        valid_large_sectors = {sector.value for sector in ROUND10_LARGE_SECTORS}
        sector_rounds = [item for item in ROUND40_ROUND_PLANS if item.large_sector is not None]

        self.assertEqual(len(sector_rounds), 12)
        self.assertEqual({item.large_sector_key for item in sector_rounds}, valid_large_sectors)
        for item in ROUND40_ROUND_PLANS:
            self.assertFalse(item.production_scoring_changed)
            self.assertFalse(item.candidate_generation_input)
            self.assertTrue(item.validation_focus)

    def test_common_validation_protocol_has_five_fixed_steps(self):
        rows = {row["step_id"]: row for row in round40_validation_protocol_rows()}

        self.assertEqual(len(ROUND40_VALIDATION_PROTOCOL), 5)
        for step_id in (
            "case_coverage",
            "stage_date_candidates",
            "price_path_validation",
            "score_price_alignment",
            "score_weight_correction",
        ):
            self.assertIn(step_id, rows)

        self.assertIn("stage3_price", rows["price_path_validation"]["required_outputs"])
        self.assertIn("do_not_invent_stage_dates", rows["stage_date_candidates"]["guardrails"])
        self.assertIn("do_not_change_production_scoring_in_round40", rows["score_weight_correction"]["guardrails"])

    def test_alignment_values_include_price_and_evidence_failure_modes(self):
        markdown = render_round40_price_alignment_markdown()

        for label in (
            "aligned",
            "false_positive_score",
            "price_moved_without_evidence",
            "evidence_good_but_price_failed",
            "cyclical_success",
            "event_premium",
            "thesis_break",
            "unknown_insufficient_price_data",
        ):
            self.assertIn(label, ROUND40_ALIGNMENT_VALUES)
            self.assertIn(label, markdown)

    def test_markdown_explains_round40_guardrails(self):
        summary = render_round40_summary_markdown()
        sequence = render_round40_round_sequence_markdown()
        protocol = render_round40_validation_protocol_markdown()

        self.assertIn("12 large-sector map is fixed", summary)
        self.assertIn("R13 is a cross-archetype", summary)
        self.assertIn("Do not add a 13th production large sector", sequence)
        self.assertIn("Do not use benchmark or case labels", protocol)
        self.assertIn("Do not lower Stage 3-Green thresholds", protocol)

    def test_report_writer_outputs_csv_and_markdown_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round40_round_protocol_reports(
                output_directory=Path(tmp) / "out",
                round_plan_path=Path(tmp) / "round_plan.csv",
                validation_protocol_path=Path(tmp) / "validation.csv",
            )

            self.assertTrue(paths["round_plan"].exists())
            self.assertTrue(paths["validation_protocol"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["round_sequence"].exists())
            self.assertTrue(paths["validation_protocol_md"].exists())
            self.assertTrue(paths["price_alignment_protocol"].exists())
            self.assertIn("R1", paths["round_plan"].read_text(encoding="utf-8"))
            self.assertIn("score_price_alignment", paths["validation_protocol"].read_text(encoding="utf-8"))

    def test_cli_argument_parser_supports_paths(self):
        args = build_parser().parse_args(
            [
                "--output-directory",
                "out",
                "--round-plan",
                "round.csv",
                "--validation-protocol",
                "validation.csv",
            ]
        )

        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.round_plan, "round.csv")
        self.assertEqual(args.validation_protocol, "validation.csv")

    def test_production_scoring_modules_do_not_import_round40_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round40_round_protocol", text)


if __name__ == "__main__":
    unittest.main()
