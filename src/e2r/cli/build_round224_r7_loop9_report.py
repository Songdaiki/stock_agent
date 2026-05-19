"""Build Round-224 R7 Loop-9 biotech/healthcare/device validation reports."""

from __future__ import annotations

import argparse
from pathlib import Path

from e2r.sector.round224_r7_loop9_biotech_healthcare_device_price_validation import (
    ROUND224_DEFAULT_AUDIT_PATH,
    ROUND224_DEFAULT_CASES_PATH,
    ROUND224_DEFAULT_OUTPUT_DIRECTORY,
    write_round224_r7_loop9_reports,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-directory", default=ROUND224_DEFAULT_OUTPUT_DIRECTORY)
    parser.add_argument("--cases", default=ROUND224_DEFAULT_CASES_PATH)
    parser.add_argument("--audit", default=ROUND224_DEFAULT_AUDIT_PATH)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    paths = write_round224_r7_loop9_reports(
        output_directory=Path(args.output_directory),
        cases_path=Path(args.cases),
        audit_path=Path(args.audit),
    )
    for name, path in paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
