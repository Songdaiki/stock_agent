"""Build v0.2 case-library coverage and alignment reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.case_library import load_case_library
from e2r.sector.case_reports import write_case_record_pack_reports
from e2r.sector.score_price_alignment import align_case_records


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build E2R case-library v0.2 reports.")
    parser.add_argument("--cases", default="data/e2r_case_library/cases_v02.jsonl")
    parser.add_argument("--output-directory", default="output/e2r_case_library_v02")
    parser.add_argument("--apply-alignment", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    records = load_case_library(args.cases)
    if args.apply_alignment:
        records = align_case_records(records)
    paths = write_case_record_pack_reports(records, Path(args.output_directory))
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
