"""Build Round-180 R9 Loop-11 Korea mobility/transport/leisure reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.round180_r9_loop11_mobility_transport_leisure import (
    ROUND180_DEFAULT_CASES_PATH,
    ROUND180_DEFAULT_OUTPUT_DIRECTORY,
    ROUND180_DEFAULT_SCORE_PROFILE_PATH,
    write_round180_r9_loop11_reports,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Round-180 R9 Loop-11 Korea mobility/transport/leisure reports.")
    parser.add_argument("--output-directory", default=ROUND180_DEFAULT_OUTPUT_DIRECTORY)
    parser.add_argument("--cases", default=ROUND180_DEFAULT_CASES_PATH)
    parser.add_argument("--score-profiles", default=ROUND180_DEFAULT_SCORE_PROFILE_PATH)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round180_r9_loop11_reports(
        output_directory=Path(args.output_directory),
        cases_path=Path(args.cases),
        score_profile_path=Path(args.score_profiles),
    )
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
