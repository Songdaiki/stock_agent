"""Build Round-14 score-weight v0.4 reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.round14_score_weight_v04 import write_round14_score_weight_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Round-14 E2R score-weight v0.4 reports.")
    parser.add_argument("--output-directory", default="output/e2r_round14_score_weight_v04")
    parser.add_argument("--score-profiles", default="data/sector_taxonomy/score_weight_profiles_round14.csv")
    parser.add_argument("--theme-map", default="data/sector_taxonomy/theme_tag_map_round14.csv")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round14_score_weight_reports(
        output_directory=Path(args.output_directory),
        score_profile_path=Path(args.score_profiles),
        theme_map_path=Path(args.theme_map),
    )
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
