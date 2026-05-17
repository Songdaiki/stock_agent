"""Build Round-131 R12 Loop-7 agriculture/life/misc reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.round131_r12_loop7_agri_life_misc import write_round131_r12_loop7_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Round-131 R12 Loop-7 agriculture/life/misc reports.")
    parser.add_argument("--output-directory", default="output/e2r_round131_r12_loop7_agri_life_misc")
    parser.add_argument("--cases", default="data/e2r_case_library/cases_r12_loop7_round131.jsonl")
    parser.add_argument("--score-profiles", default="data/sector_taxonomy/score_weight_profiles_round131_r12_loop7_v7.csv")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round131_r12_loop7_reports(
        output_directory=Path(args.output_directory),
        cases_path=Path(args.cases),
        score_profile_path=Path(args.score_profiles),
    )
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
