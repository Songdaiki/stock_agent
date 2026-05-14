import tempfile
from pathlib import Path
import unittest

from e2r.sector.round10_theme_tag_taxonomy import Round10ThemePosture
from e2r.sector.round16_theme_coverage_v05 import (
    ROUND16_SCORE_WEIGHT_GROUPS,
    find_round16_theme_tag,
    render_round16_summary_markdown,
    round16_coverage_summary,
    round16_score_group_rows,
    round16_theme_tag_rows,
    write_round16_theme_coverage_reports,
)


class Round16ThemeCoverageV05Tests(unittest.TestCase):
    def test_round16_covers_twelve_large_sectors_and_many_sub_archetypes(self):
        summary = round16_coverage_summary()

        self.assertEqual(summary["large_sector_count"], 12)
        self.assertGreaterEqual(summary["sub_archetype_count"], 70)
        self.assertGreaterEqual(summary["theme_tag_row_count"], 500)
        self.assertGreaterEqual(summary["unique_theme_tag_count"], 200)

    def test_key_raw_theme_tags_are_mapped(self):
        examples = {
            "초전도체": "SPECULATIVE_SCIENCE_THEME",
            "스테이블코인": "DIGITAL_ASSET_TOKENIZATION",
            "야놀자 관련주": "AIRLINE_TRAVEL_CYCLE",
            "퓨리오사AI 관련주": "AI_CHIP_FABRIC_INFRA",
            "마켓컬리": "ECOMMERCE_FRESH_LOGISTICS",
            "엠폭스": "EVENT_DISEASE_PEST_DEMAND",
            "빈대퇴치": "EVENT_DISEASE_PEST_DEMAND",
            "네옴시티": "GEOPOLITICAL_RECONSTRUCTION",
            "스페이스X": "SPECULATIVE_SCIENCE_THEME",
        }

        for tag, expected_sub_archetype in examples.items():
            rows = find_round16_theme_tag(tag)
            self.assertTrue(rows, tag)
            self.assertIn(expected_sub_archetype, {row["primary_sub_archetype"] for row in rows})

    def test_theme_tags_are_not_score_inputs(self):
        for row in round16_theme_tag_rows():
            self.assertEqual(row["theme_is_score_input"], "false")
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_score_groups_include_green_watch_and_redteam_defaults(self):
        groups = {group.group_name: group for group in ROUND16_SCORE_WEIGHT_GROUPS}

        self.assertEqual(groups["MEMORY_HBM_GREEN"].posture, Round10ThemePosture.GREEN_POSSIBLE)
        self.assertEqual(groups["DIGITAL_ASSET_WATCH"].posture, Round10ThemePosture.WATCH_YELLOW_FIRST)
        self.assertEqual(groups["SPECULATIVE_SCIENCE_REDTEAM"].posture, Round10ThemePosture.REDTEAM_FIRST)
        self.assertEqual(groups["FINANCIAL_INSURANCE_GREEN"].valuation, 25)

    def test_score_group_rows_are_report_only(self):
        for row in round16_score_group_rows():
            self.assertEqual(row["production_scoring_changed"], "false")

    def test_report_writer_outputs_round16_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round16_theme_coverage_reports(
                output_directory=Path(tmp) / "out",
                theme_map_path=Path(tmp) / "theme_tag_map_round16.csv",
                score_group_path=Path(tmp) / "score_weight_groups_round16.csv",
            )

            self.assertTrue(paths["theme_map"].exists())
            self.assertTrue(paths["score_groups"].exists())
            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["coverage_matrix"].exists())
            self.assertTrue(paths["green_policy"].exists())
            self.assertTrue(paths["score_group_report"].exists())
            self.assertTrue(paths["next_plan"].exists())
            self.assertIn("production_scoring_changed: false", paths["summary"].read_text(encoding="utf-8"))

    def test_summary_says_coverage_map_not_production_scoring(self):
        markdown = render_round16_summary_markdown()

        self.assertIn("coverage map", markdown)
        self.assertIn("theme_tags_are_score_input: false", markdown)

    def test_production_scoring_modules_do_not_import_round16_coverage(self):
        paths = [
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ]
        for path in paths:
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round16_theme_coverage_v05", text)


if __name__ == "__main__":
    unittest.main()
