"""Build Round-39 taxonomy consolidation reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.round39_taxonomy_consolidation import write_round39_taxonomy_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Round-39 taxonomy consolidation reports.")
    parser.add_argument("--output-directory", default="output/e2r_round39_taxonomy_consolidation")
    parser.add_argument("--deep-registry", default="data/sector_taxonomy/round39_deep_sub_archetype_registry.csv")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round39_taxonomy_reports(
        output_directory=Path(args.output_directory),
        deep_registry_path=Path(args.deep_registry),
    )
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
