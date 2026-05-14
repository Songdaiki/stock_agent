from datetime import date, datetime
import json
from pathlib import Path
import tempfile
import unittest

from e2r.backtest.missed_benchmark_autopsy import AutopsyConfig, MissReason, MissedBenchmarkAutopsy
from e2r.cli.analyze_blind_replay_misses import build_parser, config_from_args
from e2r.research.search_provider import SearchResult
from e2r.research.search_snapshot_store import SearchSnapshotStore, snapshot_from_search_result


def _write_blind_output(root: Path, recall_rows, candidates=()):
    root.mkdir(parents=True, exist_ok=True)
    (root / "benchmark_recall_report.json").write_text(json.dumps(recall_rows, ensure_ascii=False), encoding="utf-8")
    (root / "discovered_candidates.json").write_text(json.dumps(candidates, ensure_ascii=False), encoding="utf-8")
    (root / "blind_discovery_summary.json").write_text(
        json.dumps(
            {
                "replay_result": {
                    "source_coverage_summary": {
                        "price_available": 0,
                        "disclosure_available": 0,
                        "financial_available": 0,
                    }
                }
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def _write_labels(path: Path):
    rows = [
        {
            "label_id": "structural_missing_report",
            "symbol": "111111",
            "company_name": "구조회사",
            "market": "KR",
            "expected_window_start": "2023-01-01",
            "expected_window_end": "2023-12-31",
            "expected_group": "structural",
            "expected_min_layer": "event_search",
            "expected_safe_stage": "Green",
            "notes": "",
            "evaluation_only": True,
        },
        {
            "label_id": "overheat_no_universe",
            "symbol": "222222",
            "company_name": "과열회사",
            "market": "KR",
            "expected_window_start": "2023-01-01",
            "expected_window_end": "2023-12-31",
            "expected_group": "valuation_overheat",
            "expected_min_layer": "event_search",
            "expected_safe_stage": "Red",
            "notes": "",
            "evaluation_only": True,
        },
        {
            "label_id": "available_not_scored",
            "symbol": "333333",
            "company_name": "점수누락",
            "market": "KR",
            "expected_window_start": "2023-01-01",
            "expected_window_end": "2023-12-31",
            "expected_group": "structural",
            "expected_min_layer": "event_search",
            "expected_safe_stage": "Green",
            "notes": "",
            "evaluation_only": True,
        },
    ]
    path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")


class MissedBenchmarkAutopsyTests(unittest.TestCase):
    def test_autopsy_classifies_no_report_snapshot(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            labels = root_path / "labels.json"
            _write_labels(labels)
            blind = root_path / "blind"
            _write_blind_output(
                blind,
                [
                    {
                        "label_id": "structural_missing_report",
                        "symbol": "111111",
                        "company_name": "구조회사",
                        "expected_group": "structural",
                        "appeared_in_candidates": False,
                    }
                ],
            )
            SearchSnapshotStore(root_path / "search").save_snapshot(
                snapshot_from_search_result(
                    SearchResult(title="구조회사 Review PDF", url="https://example.com/report.pdf"),
                    query="구조회사 Review PDF",
                    search_date=date(2023, 2, 1),
                    fetched_at=datetime(2023, 2, 1, 9, 0),
                    symbol="111111",
                    company_name="구조회사",
                )
            )

            result = MissedBenchmarkAutopsy().run(
                AutopsyConfig(
                    blind_output=blind,
                    benchmark_labels=labels,
                    search_snapshot_root=root_path / "search",
                    report_snapshot_root=root_path / "reports",
                ),
                write_outputs=False,
            )

        self.assertEqual(result.rows[0].primary_miss_reason, MissReason.NO_REPORT_SNAPSHOT.value)
        self.assertIn(MissReason.NO_REPORT_SNAPSHOT.value, result.rows[0].secondary_miss_reasons)

    def test_autopsy_classifies_not_in_universe_for_warning_without_evidence(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            labels = root_path / "labels.json"
            _write_labels(labels)
            blind = root_path / "blind"
            _write_blind_output(
                blind,
                [
                    {
                        "label_id": "overheat_no_universe",
                        "symbol": "222222",
                        "company_name": "과열회사",
                        "expected_group": "valuation_overheat",
                        "appeared_in_candidates": False,
                    }
                ],
            )

            result = MissedBenchmarkAutopsy().run(
                AutopsyConfig(blind_output=blind, benchmark_labels=labels, search_snapshot_root=root_path / "search"),
                write_outputs=False,
            )

        self.assertEqual(result.rows[0].primary_miss_reason, MissReason.NOT_IN_UNIVERSE.value)
        self.assertEqual(result.rows[0].recommended_fix, "no_action_expected_false_positive")

    def test_autopsy_classifies_evidence_available_but_not_scored(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            labels = root_path / "labels.json"
            _write_labels(labels)
            blind = root_path / "blind"
            _write_blind_output(
                blind,
                [
                    {
                        "label_id": "available_not_scored",
                        "symbol": "333333",
                        "company_name": "점수누락",
                        "expected_group": "structural",
                        "appeared_in_candidates": False,
                    }
                ],
                candidates=[
                    {
                        "symbol": "333333",
                        "company_name": "점수누락",
                        "as_of_date": "2023-06-01",
                        "layer": "event_search",
                        "stage": "1",
                        "rank": 4,
                        "score": 15,
                        "evidence_types_seen": ["research_report"],
                    }
                ],
            )

            result = MissedBenchmarkAutopsy().run(
                AutopsyConfig(blind_output=blind, benchmark_labels=labels),
                write_outputs=False,
            )

        self.assertEqual(result.rows[0].primary_miss_reason, MissReason.EVIDENCE_AVAILABLE_BUT_NOT_SCORED.value)
        self.assertEqual(result.rows[0].recommended_fix, "add_feature_scoring_for_available_evidence")

    def test_autopsy_writes_outputs_and_does_not_recommend_lowering_green(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            labels = root_path / "labels.json"
            _write_labels(labels)
            blind = root_path / "blind"
            _write_blind_output(
                blind,
                [
                    {
                        "label_id": "overheat_no_universe",
                        "symbol": "222222",
                        "company_name": "과열회사",
                        "expected_group": "valuation_overheat",
                        "appeared_in_candidates": False,
                    }
                ],
            )
            output_dir = root_path / "autopsy"

            result = MissedBenchmarkAutopsy().run(
                AutopsyConfig(
                    blind_output=blind,
                    benchmark_labels=labels,
                    output_directory=output_dir,
                    run_date=date(2026, 5, 14),
                )
            )

            fixes = (output_dir / "recommended_fixes.md").read_text(encoding="utf-8")
            self.assertTrue((output_dir / "2026-05-14_autopsy.json").exists())
            self.assertTrue((output_dir / "2026-05-14_autopsy.md").exists())
            self.assertTrue((output_dir / "evidence_gap_matrix.csv").exists())
            self.assertNotIn("lower Stage 3-Green", fixes)
            self.assertIn("Stage 3-Green precision remains strict", fixes)
            self.assertEqual(result.report_paths["md"], output_dir / "2026-05-14_autopsy.md")

    def test_cli_parses_args(self):
        args = build_parser().parse_args(
            [
                "--blind-output",
                "output/backtests/blind_discovery/2023-01-01_to_2026-05-14",
                "--benchmark-labels",
                "data/benchmark_labels/e2r_known_winners.json",
                "--output-directory",
                "output/backtests/blind_discovery_autopsy",
                "--run-date",
                "2026-05-14",
            ]
        )
        config = config_from_args(args)

        self.assertEqual(config.run_date, date(2026, 5, 14))
        self.assertEqual(config.output_directory, Path("output/backtests/blind_discovery_autopsy"))


if __name__ == "__main__":
    unittest.main()
