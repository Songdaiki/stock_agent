"""Audit raw theme tag coverage against a normalized theme map."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.theme_tag_mapper import (
    audit_theme_tag_coverage,
    load_raw_theme_tags,
    load_theme_tag_map,
    write_theme_coverage_outputs,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit E2R theme tag coverage.")
    parser.add_argument("--raw-tags", required=True)
    parser.add_argument("--map", required=True, dest="map_path")
    parser.add_argument("--output", default="output/theme_tag_coverage_v05")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    raw_tags = load_raw_theme_tags(args.raw_tags)
    entries = load_theme_tag_map(args.map_path)
    audit = audit_theme_tag_coverage(raw_tags, entries)
    paths = write_theme_coverage_outputs(audit, output_directory=Path(args.output))
    for name, path in paths.items():
        print(f"{name}={path}")
    print(f"unmatched_tags={audit.unmatched_count}")
    print(f"ambiguous_tags={audit.ambiguous_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
