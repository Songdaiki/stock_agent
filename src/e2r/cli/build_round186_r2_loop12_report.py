"""Build Round-186 R2 Loop-12 AI/semiconductor/electronics reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.round186_r2_loop12_ai_semiconductor_electronics import (
    ROUND186_DEFAULT_CASES_PATH,
    ROUND186_DEFAULT_OUTPUT_DIRECTORY,
    ROUND186_DEFAULT_SCORE_PROFILE_PATH,
    write_round186_r2_loop12_reports,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Round-186 R2 Loop-12 AI/semiconductor/electronics reports.")
    parser.add_argument("--output-directory", default=ROUND186_DEFAULT_OUTPUT_DIRECTORY)
    parser.add_argument("--cases", default=ROUND186_DEFAULT_CASES_PATH)
    parser.add_argument("--score-profiles", default=ROUND186_DEFAULT_SCORE_PROFILE_PATH)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round186_r2_loop12_reports(
        output_directory=Path(args.output_directory),
        cases_path=Path(args.cases),
        score_profile_path=Path(args.score_profiles),
    )
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
