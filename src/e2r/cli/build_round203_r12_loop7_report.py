"""Build Round-203 R12 Loop-7 agri/life/misc reports."""

from __future__ import annotations

import argparse

from e2r.sector.round203_r12_loop7_agri_life_misc_price_validation import (
    ROUND203_DEFAULT_AUDIT_PATH,
    ROUND203_DEFAULT_CASES_PATH,
    ROUND203_DEFAULT_OUTPUT_DIRECTORY,
    write_round203_r12_loop7_reports,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-directory", default=ROUND203_DEFAULT_OUTPUT_DIRECTORY)
    parser.add_argument("--cases", default=ROUND203_DEFAULT_CASES_PATH)
    parser.add_argument("--audit", default=ROUND203_DEFAULT_AUDIT_PATH)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round203_r12_loop7_reports(
        output_directory=args.output_directory,
        cases_path=args.cases,
        audit_path=args.audit,
    )
    for key, path in paths.items():
        print(f"{key}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
