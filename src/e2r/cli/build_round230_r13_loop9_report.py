"""Build Round-230 R13 Loop-9 cross-archetype RedTeam reports."""

from __future__ import annotations

import argparse
from pathlib import Path

from e2r.sector.round230_r13_loop9_cross_archetype_redteam_price_validation import (
    ROUND230_DEFAULT_AUDIT_PATH,
    ROUND230_DEFAULT_CASES_PATH,
    ROUND230_DEFAULT_OUTPUT_DIRECTORY,
    write_round230_r13_loop9_reports,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-directory", default=ROUND230_DEFAULT_OUTPUT_DIRECTORY)
    parser.add_argument("--cases", default=ROUND230_DEFAULT_CASES_PATH)
    parser.add_argument("--audit", default=ROUND230_DEFAULT_AUDIT_PATH)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    paths = write_round230_r13_loop9_reports(
        output_directory=Path(args.output_directory),
        cases_path=Path(args.cases),
        audit_path=Path(args.audit),
    )
    for name, path in paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
