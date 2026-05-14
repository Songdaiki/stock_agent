import tempfile
from pathlib import Path
import unittest

from e2r.sector.case_library import E2RCaseRecord, load_case_library
from e2r.sector.round9_case_record_pack_audit import (
    ROUND9_ARCHETYPE_VIEW,
    ROUND9_LARGE_SECTORS,
    ROUND9_PRICE_PATTERN_VALUES,
    ROUND9_REQUIRED_CASE_IDS,
    render_round9_schema_contract_markdown,
    round9_archetype_view_coverage,
    round9_case_pack_audit,
    write_round9_case_record_pack_reports,
)


class Round9CaseRecordPackAuditTests(unittest.TestCase):
    def test_round9_has_ten_large_sectors_and_32_archetype_views(self):
        self.assertEqual(len(ROUND9_LARGE_SECTORS), 10)
        self.assertEqual(len(ROUND9_ARCHETYPE_VIEW), 32)
        self.assertEqual(ROUND9_ARCHETYPE_VIEW[-1].label, "ONE_OFF_OR_THEME_RISK")

    def test_required_round9_cases_are_present_in_v02_pack(self):
        records = load_case_library("data/e2r_case_library/cases_v02.jsonl")
        audit = round9_case_pack_audit(records)

        self.assertGreaterEqual(audit.case_count, len(ROUND9_REQUIRED_CASE_IDS))
        self.assertEqual(audit.required_case_count, len(ROUND9_REQUIRED_CASE_IDS))
        self.assertEqual(audit.missing_case_ids, ())
        self.assertEqual(audit.present_required_case_count, len(ROUND9_REQUIRED_CASE_IDS))

    def test_case_library_preserves_round9_notes_field(self):
        record = E2RCaseRecord.from_mapping(
            {
                "case_id": "notes_case",
                "symbol": "000001",
                "company_name": "노트테스트",
                "market": "KR",
                "sector_raw": "플랫폼",
                "primary_archetype": "PLATFORM_SOFTWARE_INTERNET",
                "expected_group": "success_candidate",
                "notes": "Round 9 calibration note",
                "data_quality": {
                    "official_data_available": False,
                    "report_data_available": False,
                    "price_data_available": False,
                    "stage_dates_confidence": 0.0,
                },
            }
        )

        self.assertEqual(record.notes, "Round 9 calibration note")
        self.assertEqual(record.as_dict()["notes"], "Round 9 calibration note")

    def test_schema_contract_mentions_governance_trust_break(self):
        markdown = render_round9_schema_contract_markdown()

        self.assertIn("governance_trust_break", ROUND9_PRICE_PATTERN_VALUES)
        self.assertIn("notes", markdown)
        self.assertIn("governance_trust_break", markdown)

    def test_archetype_view_coverage_uses_one_off_or_theme_alias(self):
        records = load_case_library("data/e2r_case_library/cases_v02.jsonl")
        rows = round9_archetype_view_coverage(records)
        by_view = {row["archetype_view"]: row for row in rows}

        self.assertIn("ONE_OFF_EVENT_DEMAND", by_view["ONE_OFF_OR_THEME_RISK"]["canonical_archetypes"])
        self.assertIn("THEME_VALUATION_OVERHEAT", by_view["ONE_OFF_OR_THEME_RISK"]["canonical_archetypes"])
        self.assertGreaterEqual(by_view["ONE_OFF_OR_THEME_RISK"]["case_count"], 2)

    def test_report_writer_outputs_round9_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round9_case_record_pack_reports(output_directory=tmp)

            self.assertTrue(paths["framework"].exists())
            self.assertTrue(paths["required_case_matrix"].exists())
            self.assertTrue(paths["audit"].exists())
            self.assertTrue(paths["archetype_coverage"].exists())
            self.assertTrue(paths["schema_contract"].exists())
            self.assertTrue(paths["next_plan"].exists())
            self.assertIn("Round-9 Case Pack Audit", paths["audit"].read_text(encoding="utf-8"))

    def test_production_scoring_modules_do_not_import_round9_audit(self):
        paths = [
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ]
        for path in paths:
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round9_case_record_pack_audit", text)


if __name__ == "__main__":
    unittest.main()
