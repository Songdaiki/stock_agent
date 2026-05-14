"""Build Round-9 case record pack reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.round9_case_record_pack_audit import write_round9_case_record_pack_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Round-9 E2R case record pack audit reports.")
    parser.add_argument("--cases", default="data/e2r_case_library/cases_v02.jsonl")
    parser.add_argument("--output-directory", default="output/e2r_round9_case_record_pack")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round9_case_record_pack_reports(
        case_path=args.cases,
        output_directory=Path(args.output_directory),
    )
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
