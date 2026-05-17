"""Build Round-126 R7 Loop-7 biotech/healthcare/device reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.round126_r7_loop7_biotech_healthcare_device import (
    ROUND126_DEFAULT_CASES_PATH,
    ROUND126_DEFAULT_OUTPUT_DIRECTORY,
    ROUND126_DEFAULT_SCORE_PROFILE_PATH,
    write_round126_r7_loop7_reports,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Round-126 R7 Loop-7 biotech/healthcare/device reports.")
    parser.add_argument("--output-directory", default=ROUND126_DEFAULT_OUTPUT_DIRECTORY)
    parser.add_argument("--cases", default=ROUND126_DEFAULT_CASES_PATH)
    parser.add_argument("--score-profiles", default=ROUND126_DEFAULT_SCORE_PROFILE_PATH)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round126_r7_loop7_reports(
        output_directory=Path(args.output_directory),
        cases_path=Path(args.cases),
        score_profile_path=Path(args.score_profiles),
    )
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
