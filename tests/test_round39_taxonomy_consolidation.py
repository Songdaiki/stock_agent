import tempfile
from pathlib import Path
import unittest

from e2r.cli.build_round39_taxonomy_consolidation_report import build_parser
from e2r.sector.round10_theme_tag_taxonomy import ROUND10_LARGE_SECTORS, ROUND10_THEME_ARCHETYPES, Round10ThemePosture
from e2r.sector.round39_taxonomy_consolidation import (
    ROUND39_DEEP_SUB_ARCHETYPES,
    render_round39_green_policy_rollup_markdown,
    render_round39_layer_model_markdown,
    render_round39_price_validation_next_steps_markdown,
    render_round39_summary_markdown,
    round39_deep_sub_archetype_rows,
    round39_large_sector_rows,
    round39_summary,
    write_round39_taxonomy_reports,
)


class Round39TaxonomyConsolidationTests(unittest.TestCase):
    def test_round39_keeps_twelve_large_sectors_and_adds_deep_lenses(self):
        summary = round39_summary()

        self.assertEqual(summary["large_sector_count"], 12)
        self.assertEqual(summary["base_theme_archetype_count"], len(ROUND10_THEME_ARCHETYPES))
        self.assertEqual(summary["deep_sub_archetype_count"], 41)
        self.assertEqual(summary["combined_view_count"], len(ROUND10_THEME_ARCHETYPES) + 41)
        self.assertGreaterEqual(summary["combined_view_count"], 90)
        self.assertLessEqual(summary["combined_view_count"], 110)
        self.assertFalse(summary["production_scoring_changed"])
        self.assertFalse(summary["deep_sub_archetypes_are_candidate_generation_input"])

    def test_all_deep_lenses_map_to_existing_large_sector_and_are_not_score_inputs(self):
        valid_large_sectors = set(ROUND10_LARGE_SECTORS)

        for item in ROUND39_DEEP_SUB_ARCHETYPES:
            self.assertIn(item.parent_large_sector, valid_large_sectors)
            self.assertFalse(item.theme_is_score_input)
            self.assertFalse(item.production_scoring_changed)
            self.assertTrue(item.evidence_focus)
            self.assertTrue(item.price_validation_focus)

    def test_ai_infra_sub_archetypes_are_separate_under_same_large_sector(self):
        rows = {row["label"]: row for row in round39_deep_sub_archetype_rows()}

        for label in (
            "MEMORY_HBM_CAPACITY_EXTENSION",
            "AI_SERVER_ODM_EMS_SUPPLY_CHAIN",
            "NEOCLOUD_GPU_RENTAL",
            "ADVANCED_PACKAGING_COWOS_EMIB",
            "OPTICAL_NETWORKING_AI_DATACENTER",
            "INDUSTRIAL_GASES_SEMICONDUCTOR_INFRA",
            "AI_DATA_CENTER_POWER_EQUIPMENT",
            "AI_DATA_CENTER_COOLING",
        ):
            self.assertEqual(rows[label]["parent_large_sector"], "AI_SEMICONDUCTOR_ELECTRONICS")

        self.assertIn("accounting_trust", rows["AI_SERVER_ODM_EMS_SUPPLY_CHAIN"]["risk_focus"])
        self.assertIn("debt", rows["NEOCLOUD_GPU_RENTAL"]["risk_focus"])
        self.assertIn("bottleneck_normalization", rows["ADVANCED_PACKAGING_COWOS_EMIB"]["risk_focus"])

    def test_green_watch_and_redteam_rollup_is_explicit(self):
        summary = round39_summary()
        markdown = render_round39_green_policy_rollup_markdown()

        self.assertGreater(summary["green_possible_deep_count"], 0)
        self.assertGreater(summary["watch_yellow_first_deep_count"], 0)
        self.assertGreater(summary["redteam_first_deep_count"], 0)
        self.assertIn("Green-Possible", markdown)
        self.assertIn("Watch-to-Green", markdown)
        self.assertIn("RedTeam-First", markdown)
        self.assertIn("Do not use deep sub-archetype labels as candidate-generation evidence", markdown)

    def test_large_sector_hierarchy_rows_cover_every_sector(self):
        rows = round39_large_sector_rows()
        labels = {row["large_sector"] for row in rows}

        self.assertEqual(len(rows), 12)
        self.assertEqual(labels, {sector.value for sector in ROUND10_LARGE_SECTORS})
        self.assertTrue(any(int(row["deep_sub_archetype_count"]) > 0 for row in rows))

    def test_layer_model_and_next_steps_explain_parent_child_design(self):
        layer = render_round39_layer_model_markdown()
        next_steps = render_round39_price_validation_next_steps_markdown()
        summary = render_round39_summary_markdown()

        self.assertIn("Raw theme tag", layer)
        self.assertIn("Large sector", layer)
        self.assertIn("Deep sub-archetype", layer)
        self.assertIn("Price-path validation", layer)
        self.assertIn("Keep the 12 large-sector map fixed", next_steps)
        self.assertIn("combined_view_count", summary)

    def test_report_writer_outputs_registry_and_markdown_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round39_taxonomy_reports(
                output_directory=Path(tmp) / "out",
                deep_registry_path=Path(tmp) / "deep_registry.csv",
            )

            self.assertTrue(paths["deep_registry"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["large_sector_hierarchy"].exists())
            self.assertTrue(paths["layer_model"].exists())
            self.assertTrue(paths["green_policy_rollup"].exists())
            self.assertTrue(paths["price_validation_next_steps"].exists())
            self.assertIn("AI_DATA_CENTER_INFRASTRUCTURE", paths["price_validation_next_steps"].read_text(encoding="utf-8"))

    def test_cli_argument_parser_supports_paths(self):
        args = build_parser().parse_args(
            [
                "--output-directory",
                "out",
                "--deep-registry",
                "deep.csv",
            ]
        )

        self.assertEqual(args.output_directory, "out")
        self.assertEqual(args.deep_registry, "deep.csv")

    def test_production_scoring_modules_do_not_import_round39_pack(self):
        for path in (
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round39_taxonomy_consolidation", text)


if __name__ == "__main__":
    unittest.main()
