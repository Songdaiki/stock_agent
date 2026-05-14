"""Run shadow-only score profile normalization for case records."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.shadow_score_normalizer import run_shadow_score_normalizer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run E2R shadow score profile normalization.")
    parser.add_argument("--cases", required=True)
    parser.add_argument("--profiles", required=True)
    parser.add_argument("--output", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output = run_shadow_score_normalizer(
        cases_path=Path(args.cases),
        profiles_path=Path(args.profiles),
        output_path=Path(args.output),
    )
    print(f"shadow_score_report={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
