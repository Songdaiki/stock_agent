"""Build the Korea sector taxonomy CSV from official/fixture universe data."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import Sequence

from e2r.backtest.historical_official_store import HistoricalOfficialStore
from e2r.models import Market
from e2r.sector.sector_mapper import load_mapping_rules
from e2r.sector.taxonomy import (
    build_taxonomy_from_instruments,
    taxonomy_summary,
    write_sector_taxonomy,
    write_taxonomy_summary,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Korea sector taxonomy from available official universe data.")
    parser.add_argument("--as-of-date", required=True)
    parser.add_argument("--market", choices=[item.value for item in Market], default=Market.KR.value)
    parser.add_argument("--official-root", default="data/historical_official")
    parser.add_argument("--rules-root", default="data/sector_taxonomy")
    parser.add_argument("--output", default="data/sector_taxonomy/korea_sector_map.csv")
    parser.add_argument("--summary-output", default="output/sector_taxonomy/sector_taxonomy_summary.md")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    as_of_date = date.fromisoformat(args.as_of_date)
    market = Market(args.market)
    store = HistoricalOfficialStore(args.official_root)
    instruments = store.load_universe(as_of_date, market)
    rules = load_mapping_rules(args.rules_root)
    rows = build_taxonomy_from_instruments(instruments, rules=rules)
    output = write_sector_taxonomy(rows, args.output)
    summary = taxonomy_summary(rows, full_live_taxonomy_built=False, fixture_only=True)
    summary_path = write_taxonomy_summary(summary, Path(args.summary_output))
    print(f"taxonomy={output}")
    print(f"summary={summary_path}")
    print(f"mapped_symbols={summary['symbol_count']}")
    print(f"unmapped_count={summary['unmapped_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
