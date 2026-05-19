"""Build Round-192 R1 Loop-7 Korean price-path validation reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.round192_r1_loop7_industrial_infra_price_validation import (
    ROUND192_DEFAULT_AUDIT_PATH,
    ROUND192_DEFAULT_CASES_PATH,
    ROUND192_DEFAULT_OUTPUT_DIRECTORY,
    write_round192_r1_loop7_reports,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Round-192 R1 Loop-7 price-path validation reports.")
    parser.add_argument("--output-directory", default=ROUND192_DEFAULT_OUTPUT_DIRECTORY)
    parser.add_argument("--cases", default=ROUND192_DEFAULT_CASES_PATH)
    parser.add_argument("--audit", default=ROUND192_DEFAULT_AUDIT_PATH)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round192_r1_loop7_reports(
        output_directory=Path(args.output_directory),
        cases_path=Path(args.cases),
        audit_path=Path(args.audit),
    )
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
