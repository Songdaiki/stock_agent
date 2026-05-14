"""Build Round-13 score normalization readiness reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.round13_score_normalization import write_round13_score_normalization_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Round-13 E2R score-normalization readiness reports.")
    parser.add_argument("--output-directory", default="output/e2r_round13_score_normalization")
    parser.add_argument("--score-profiles", default="data/sector_taxonomy/score_weight_profiles_round13.csv")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round13_score_normalization_reports(
        output_directory=Path(args.output_directory),
        score_profile_path=Path(args.score_profiles),
    )
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
