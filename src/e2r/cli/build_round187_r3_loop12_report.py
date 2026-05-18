"""Build Round-187 R3 Loop-12 battery/EV/green reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.round187_r3_loop12_battery_ev_green import (
    ROUND187_DEFAULT_CASES_PATH,
    ROUND187_DEFAULT_OUTPUT_DIRECTORY,
    ROUND187_DEFAULT_SCORE_PROFILE_PATH,
    write_round187_r3_loop12_reports,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Round-187 R3 Loop-12 battery/EV/green reports.")
    parser.add_argument("--output-directory", default=ROUND187_DEFAULT_OUTPUT_DIRECTORY)
    parser.add_argument("--cases", default=ROUND187_DEFAULT_CASES_PATH)
    parser.add_argument("--score-profiles", default=ROUND187_DEFAULT_SCORE_PROFILE_PATH)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round187_r3_loop12_reports(
        output_directory=Path(args.output_directory),
        cases_path=Path(args.cases),
        score_profile_path=Path(args.score_profiles),
    )
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
