"""CLI for filling case-library price validation fields."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.case_price_backfill import backfill_case_price_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Backfill E2R case-library price paths from historical prices.")
    parser.add_argument("--cases", required=True)
    parser.add_argument("--price-root", default="data/historical_official/prices")
    parser.add_argument("--output", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output = backfill_case_price_file(cases_path=args.cases, price_root=args.price_root, output_path=args.output)
    print(f"price_filled_cases={Path(output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
