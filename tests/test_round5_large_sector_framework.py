import tempfile
from pathlib import Path
import unittest

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import load_case_library
from e2r.sector.round5_large_sector_framework import (
    ROUND5_NEW_OR_CONFIRMED_ARCHETYPES,
    Round5GreenPermission,
    Round5LargeSector,
    render_round5_green_permission_markdown,
    round5_archetype_rows,
    round5_case_coverage_by_large_sector,
    round5_definition,
    round5_large_sector_for,
    round5_large_sectors_for,
    write_round5_large_sector_reports,
)


class Round5LargeSectorFrameworkTests(unittest.TestCase):
    def test_round5_has_exactly_ten_large_sectors(self):
        self.assertEqual(len(tuple(Round5LargeSector)), 10)
        self.assertEqual(round5_definition(Round5LargeSector.INDUSTRIAL_ORDERS).korean_name, "산업재/수주")

    def test_every_current_archetype_has_large_sector_row(self):
        rows = round5_archetype_rows()
        by_archetype = {row["archetype"]: row for row in rows}

        self.assertEqual(len(rows), len(tuple(E2RArchetype)))
        for archetype in E2RArchetype:
            self.assertIn(archetype.value, by_archetype)
            self.assertTrue(by_archetype[archetype.value]["primary_large_sector"])

    def test_cross_sector_archetypes_keep_secondary_context(self):
        ai_dc = round5_large_sectors_for(E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE)
        medical = round5_large_sectors_for(E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT)

        self.assertEqual(ai_dc[0], Round5LargeSector.SEMICONDUCTOR_AI_INFRA)
        self.assertIn(Round5LargeSector.INDUSTRIAL_ORDERS, ai_dc)
        self.assertEqual(medical[0], Round5LargeSector.EXPORT_CONSUMER)
        self.assertIn(Round5LargeSector.BIOTECH_HEALTHCARE, medical)

    def test_green_permission_matches_round5_guardrails(self):
        self.assertEqual(
            round5_definition(round5_large_sector_for(E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL)).green_permission,
            Round5GreenPermission.HIGH,
        )
        self.assertEqual(
            round5_definition(round5_large_sector_for(E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT)).green_permission,
            Round5GreenPermission.RESTRICTED,
        )
        self.assertEqual(
            round5_definition(round5_large_sector_for(E2RArchetype.ROBOTICS_FACTORY_AUTOMATION)).green_permission,
            Round5GreenPermission.RESTRICTED,
        )

    def test_round5_new_or_confirmed_archetypes_are_present(self):
        self.assertIn(E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE, ROUND5_NEW_OR_CONFIRMED_ARCHETYPES)
        self.assertIn(E2RArchetype.NUCLEAR_SMR_GRID_POLICY, ROUND5_NEW_OR_CONFIRMED_ARCHETYPES)
        self.assertIn(E2RArchetype.RARE_METALS_STRATEGIC_MATERIALS, ROUND5_NEW_OR_CONFIRMED_ARCHETYPES)
        self.assertIn(E2RArchetype.CDMO_HEALTHCARE_CONTRACT, ROUND5_NEW_OR_CONFIRMED_ARCHETYPES)

    def test_case_coverage_rolls_up_to_large_sector(self):
        records = load_case_library("data/e2r_case_library/cases_v02.jsonl")
        rows = round5_case_coverage_by_large_sector(records)
        by_sector = {row["large_sector"]: row for row in rows}

        self.assertGreater(by_sector["EXPORT_CONSUMER"]["case_count"], 0)
        self.assertGreaterEqual(by_sector["THEME_EVENT_GUARDRAIL"]["price_backfill_needed_count"], 0)

    def test_report_writer_outputs_round5_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_round5_large_sector_reports(output_directory=tmp)

            self.assertTrue(paths["framework"].exists())
            self.assertTrue(paths["matrix"].exists())
            self.assertTrue(paths["green"].exists())
            self.assertTrue(paths["coverage"].exists())
            self.assertTrue(paths["next_plan"].exists())
            self.assertIn("Round-5 Large-Sector Framework", paths["framework"].read_text(encoding="utf-8"))
            self.assertIn("해운은 운임 급등", render_round5_green_permission_markdown())

    def test_production_scoring_modules_do_not_import_round5_framework(self):
        paths = [
            "src/e2r/features.py",
            "src/e2r/staging.py",
            "src/e2r/red_team.py",
            "src/e2r/pipeline/e2r_standard_flow.py",
        ]
        for path in paths:
            text = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("round5_large_sector_framework", text)


if __name__ == "__main__":
    unittest.main()
