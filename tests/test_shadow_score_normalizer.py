from pathlib import Path
import tempfile
import unittest

from e2r.sector.case_library import E2RCaseRecord, PriceValidation, load_case_library
from e2r.sector.shadow_score_normalizer import (
    load_score_weight_profiles,
    run_shadow_score_normalizer,
    shadow_normalize_cases,
)


class ShadowScoreNormalizerTests(unittest.TestCase):
    def test_score_weight_profiles_v05_validate_dimensions(self):
        profiles = load_score_weight_profiles("data/sector_taxonomy/score_weight_profiles_v05.yml")

        self.assertIn("MEMORY_HBM_CAPACITY", profiles)
        self.assertEqual(profiles["MEMORY_HBM_CAPACITY"].dimensions["eps_fcf"], 24)
        self.assertEqual(profiles["THEME_VALUATION_OVERHEAT"].green_policy, "red_flag")

    def test_shadow_normalizer_does_not_modify_stageclassifier(self):
        before = Path("src/e2r/staging.py").read_text(encoding="utf-8")
        records = load_case_library("data/e2r_case_library/cases_v03_price_filled.jsonl")
        profiles = load_score_weight_profiles("data/sector_taxonomy/score_weight_profiles_v05.yml")

        results = shadow_normalize_cases(records, profiles)

        after = Path("src/e2r/staging.py").read_text(encoding="utf-8")
        self.assertEqual(before, after)
        self.assertGreaterEqual(len(results), 100)

    def test_event_or_red_flag_profile_cannot_create_green(self):
        record = E2RCaseRecord.from_mapping(
            {
                "case_id": "speculative_case",
                "symbol": "SPEC",
                "company_name": "투기테마",
                "market": "KR",
                "sector_raw": "초전도체",
                "primary_archetype": "THEME_VALUATION_OVERHEAT",
                "expected_group": "overheat",
                "case_type": "overheat",
                "must_have_fields": ["theme_keyword"],
                "price_validation": PriceValidation(price_validation_status="price_filled").as_dict(),
                "data_quality": {
                    "official_data_available": False,
                    "report_data_available": True,
                    "price_data_available": True,
                    "stage_dates_confidence": 0.2,
                },
            }
        )
        profiles = load_score_weight_profiles("data/sector_taxonomy/score_weight_profiles_v05.yml")

        result = shadow_normalize_cases((record,), profiles)[0]

        self.assertEqual(result.shadow_status, "green_restricted_by_profile")
        self.assertIn("red_flag", result.reason)

    def test_missing_price_data_is_not_invented(self):
        records = load_case_library("data/e2r_case_library/cases_v03_price_filled.jsonl")
        missing = next(record for record in records if record.case_id == "toss_won_stablecoin_candidate")

        self.assertEqual(missing.price_validation.price_validation_status, "missing_price_data")
        self.assertIsNone(missing.price_validation.stage3_price)

    def test_shadow_report_is_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "shadow.md"
            path = run_shadow_score_normalizer(
                cases_path="data/e2r_case_library/cases_v03_price_filled.jsonl",
                profiles_path="data/sector_taxonomy/score_weight_profiles_v05.yml",
                output_path=output,
            )

            self.assertTrue(path.exists())
            text = path.read_text(encoding="utf-8")
            self.assertIn("production_scoring_changed: false", text)
            self.assertIn("insufficient_validation", text)


if __name__ == "__main__":
    unittest.main()
