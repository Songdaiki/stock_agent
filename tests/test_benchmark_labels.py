from pathlib import Path
import unittest

from e2r.backtest.benchmark_labels import BenchmarkGroup, labels_for_market, load_benchmark_labels
from e2r.models import Market


ROOT = Path(__file__).resolve().parents[1]


class BenchmarkLabelTests(unittest.TestCase):
    def test_labels_load_as_evaluation_only(self):
        labels = load_benchmark_labels(ROOT / "data/benchmark_labels/e2r_known_winners.json")

        self.assertGreaterEqual(len(labels), 10)
        self.assertTrue(all(item.evaluation_only for item in labels))
        self.assertIn(BenchmarkGroup.STRUCTURAL, {item.expected_group for item in labels})
        self.assertIn(BenchmarkGroup.ONE_OFF, {item.expected_group for item in labels})

    def test_labels_can_be_filtered_by_market(self):
        labels = load_benchmark_labels(ROOT / "data/benchmark_labels/e2r_known_winners.json")
        kr_labels = labels_for_market(labels, Market.KR)

        self.assertTrue(kr_labels)
        self.assertTrue(all(item.market == Market.KR for item in kr_labels))

    def test_production_pipeline_does_not_import_benchmark_labels(self):
        production_files = [
            ROOT / "src/e2r/pipeline/e2r_standard_flow.py",
            ROOT / "src/e2r/cheap_scan/korea_scanner.py",
            ROOT / "src/e2r/features.py",
            ROOT / "src/e2r/staging.py",
            ROOT / "src/e2r/red_team.py",
        ]

        for path in production_files:
            with self.subTest(path=path.name):
                self.assertNotIn("benchmark_labels", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
