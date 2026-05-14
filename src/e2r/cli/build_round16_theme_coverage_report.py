"""Build Round-16 full theme coverage v0.5 reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.round16_theme_coverage_v05 import write_round16_theme_coverage_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Round-16 E2R full theme coverage reports.")
    parser.add_argument("--output-directory", default="output/e2r_round16_theme_coverage_v05")
    parser.add_argument("--theme-map", default="data/sector_taxonomy/theme_tag_map_round16.csv")
    parser.add_argument("--score-groups", default="data/sector_taxonomy/score_weight_groups_round16.csv")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round16_theme_coverage_reports(
        output_directory=Path(args.output_directory),
        theme_map_path=Path(args.theme_map),
        score_group_path=Path(args.score_groups),
    )
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
