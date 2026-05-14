import json
from pathlib import Path
import tempfile
import unittest

from e2r.cli.audit_theme_tag_coverage import build_parser
from e2r.sector.case_library import load_case_library
from e2r.sector.theme_tag_mapper import (
    VALID_GREEN_POLICIES,
    audit_theme_tag_coverage,
    load_raw_theme_tags,
    load_theme_tag_map,
    normalize_theme_tag,
    write_theme_coverage_outputs,
)


class ThemeTagMapperTests(unittest.TestCase):
    def test_raw_theme_list_is_parsed_and_aliases_normalize(self):
        tags = load_raw_theme_tags("data/sector_taxonomy/raw_theme_tags_v05.csv")

        self.assertGreaterEqual(len(tags), 200)
        self.assertEqual(normalize_theme_tag("남북경험-개성공단"), normalize_theme_tag("남북경협 개성공단"))
        self.assertEqual(normalize_theme_tag("마켓컬리오아시스 관련주"), "마켓컬리오아시스")

    def test_every_raw_theme_tag_maps_or_appears_in_unmatched(self):
        raw_tags = load_raw_theme_tags("data/sector_taxonomy/raw_theme_tags_v05.csv")
        entries = load_theme_tag_map("data/sector_taxonomy/theme_tag_map_v05.csv")
        audit = audit_theme_tag_coverage(raw_tags, entries)

        self.assertEqual(audit.total_raw_tags, 208)
        self.assertEqual(audit.mapped_tags, 208)
        self.assertEqual(audit.unmatched_count, 0)
        self.assertGreaterEqual(audit.ambiguous_count, 1)

    def test_green_policy_values_are_valid(self):
        entries = load_theme_tag_map("data/sector_taxonomy/theme_tag_map_v05.csv")

        for entry in entries:
            self.assertIn(entry.green_policy, VALID_GREEN_POLICIES)
            self.assertEqual(entry.theme_is_score_input, False)
            self.assertEqual(entry.production_scoring_changed, False)

    def test_audit_writes_markdown_and_csv_outputs(self):
        raw_tags = load_raw_theme_tags("data/sector_taxonomy/raw_theme_tags_v05.csv")
        entries = load_theme_tag_map("data/sector_taxonomy/theme_tag_map_v05.csv")
        audit = audit_theme_tag_coverage(raw_tags, entries)
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_theme_coverage_outputs(audit, output_directory=tmp)

            self.assertTrue(paths["report"].exists())
            self.assertTrue(paths["unmatched"].exists())
            self.assertTrue(paths["ambiguous"].exists())
            self.assertIn("unmatched_tags: 0", paths["report"].read_text(encoding="utf-8"))

    def test_cases_v03_and_evidence_index_validate_schema(self):
        records = load_case_library("data/e2r_case_library/cases_v03.jsonl")

        self.assertGreaterEqual(len(records), 100)
        self.assertTrue(any(record.case_id == "sk_hynix_hbm_rerating" for record in records))
        for record in records:
            record.validate()

        rows = [
            json.loads(line)
            for line in Path("data/e2r_case_library/evidence_index_v03.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertGreaterEqual(len(rows), 40)
        for row in rows:
            self.assertIn("case_id", row)
            self.assertIn("source_type", row)
            self.assertIn("evidence_fields_supported", row)
            self.assertIn("confidence", row)

    def test_case_library_is_not_imported_by_production_scoring_modules(self):
        for path in ("src/e2r/features.py", "src/e2r/staging.py", "src/e2r/red_team.py"):
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("case_library", text)

    def test_cli_parser_accepts_required_arguments(self):
        args = build_parser().parse_args(
            [
                "--raw-tags",
                "data/sector_taxonomy/raw_theme_tags_v05.csv",
                "--map",
                "data/sector_taxonomy/theme_tag_map_v05.csv",
                "--output",
                "out",
            ]
        )

        self.assertEqual(args.raw_tags, "data/sector_taxonomy/raw_theme_tags_v05.csv")
        self.assertEqual(args.map_path, "data/sector_taxonomy/theme_tag_map_v05.csv")
        self.assertEqual(args.output, "out")


if __name__ == "__main__":
    unittest.main()
