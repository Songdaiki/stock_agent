"""Build Round-170 R11 Loop-10 policy/geopolitical/disaster/event reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.round170_r11_loop10_policy_geopolitical_event import write_round170_r11_loop10_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Round-170 R11 Loop-10 policy/geopolitical/disaster/event reports.")
    parser.add_argument("--output-directory", default="output/e2r_round170_r11_loop10_policy_geopolitical_event")
    parser.add_argument("--cases", default="data/e2r_case_library/cases_r11_loop10_round170.jsonl")
    parser.add_argument("--score-profiles", default="data/sector_taxonomy/score_weight_profiles_round170_r11_loop10_v10.csv")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round170_r11_loop10_reports(
        output_directory=Path(args.output_directory),
        cases_path=Path(args.cases),
        score_profile_path=Path(args.score_profiles),
    )
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
