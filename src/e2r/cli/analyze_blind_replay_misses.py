"""CLI for blind replay miss autopsy."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import Sequence

from e2r.backtest.missed_benchmark_autopsy import AutopsyConfig, MissedBenchmarkAutopsy, render_autopsy_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze missed benchmark labels after blind replay.")
    parser.add_argument("--blind-output", required=True)
    parser.add_argument("--benchmark-labels", default="data/benchmark_labels/e2r_known_winners.json")
    parser.add_argument("--output-directory", default="output/backtests/blind_discovery_autopsy")
    parser.add_argument("--search-snapshot-root", default="data/search_snapshots")
    parser.add_argument("--report-snapshot-root", default="data/report_snapshots")
    parser.add_argument("--run-date")
    return parser


def config_from_args(args: argparse.Namespace) -> AutopsyConfig:
    return AutopsyConfig(
        blind_output=Path(args.blind_output),
        benchmark_labels=Path(args.benchmark_labels),
        output_directory=Path(args.output_directory),
        search_snapshot_root=Path(args.search_snapshot_root),
        report_snapshot_root=Path(args.report_snapshot_root),
        run_date=date.fromisoformat(args.run_date) if args.run_date else date.today(),
    )


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = MissedBenchmarkAutopsy().run(config_from_args(args))
    print(render_autopsy_markdown(result))
    if result.output_root:
        print(f"output_root={result.output_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
