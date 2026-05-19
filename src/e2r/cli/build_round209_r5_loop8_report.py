"""Build Round-209 R5 Loop-8 consumer/retail/brand price validation reports."""

from __future__ import annotations

import argparse

from e2r.sector.round209_r5_loop8_consumer_retail_brand_price_validation import (
    ROUND209_DEFAULT_AUDIT_PATH,
    ROUND209_DEFAULT_CASES_PATH,
    ROUND209_DEFAULT_OUTPUT_DIRECTORY,
    write_round209_r5_loop8_reports,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-directory", default=ROUND209_DEFAULT_OUTPUT_DIRECTORY)
    parser.add_argument("--cases", default=ROUND209_DEFAULT_CASES_PATH)
    parser.add_argument("--audit", default=ROUND209_DEFAULT_AUDIT_PATH)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round209_r5_loop8_reports(
        output_directory=args.output_directory,
        cases_path=args.cases,
        audit_path=args.audit,
    )
    for key, path in paths.items():
        print(f"{key}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
