"""Build Round-19 deep-search readiness reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.round19_deep_search_readiness import (
    ROUND19_DEFAULT_CASE_LIBRARY,
    ROUND19_DEFAULT_OUTPUT_DIRECTORY,
    ROUND19_DEFAULT_RAW_TAGS,
    ROUND19_DEFAULT_THEME_MAP,
    write_round19_deep_search_readiness_reports,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Round-19 deep-search readiness reports.")
    parser.add_argument("--case-library", default=ROUND19_DEFAULT_CASE_LIBRARY)
    parser.add_argument("--raw-tags", default=ROUND19_DEFAULT_RAW_TAGS)
    parser.add_argument("--theme-map", default=ROUND19_DEFAULT_THEME_MAP)
    parser.add_argument("--output-directory", default=ROUND19_DEFAULT_OUTPUT_DIRECTORY)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round19_deep_search_readiness_reports(
        case_library_path=Path(args.case_library),
        raw_tags_path=Path(args.raw_tags),
        theme_map_path=Path(args.theme_map),
        output_directory=Path(args.output_directory),
    )
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
