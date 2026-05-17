"""Build Round-119 E2R first-principles guardrail reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.round119_e2r_first_principles import write_round119_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Round-119 E2R first-principles guardrail reports.")
    parser.add_argument("--output-directory", default="output/e2r_round119_first_principles")
    parser.add_argument("--principles", default="data/sector_taxonomy/e2r_first_principles_round119.csv")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round119_reports(
        output_directory=Path(args.output_directory),
        principles_path=Path(args.principles),
    )
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
