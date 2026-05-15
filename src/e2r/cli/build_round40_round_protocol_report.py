"""Build Round-40 round protocol reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from e2r.sector.round40_round_protocol import write_round40_round_protocol_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Round-40 round protocol reports.")
    parser.add_argument("--output-directory", default="output/e2r_round40_round_protocol")
    parser.add_argument("--round-plan", default="data/sector_taxonomy/round40_round_protocol.csv")
    parser.add_argument("--validation-protocol", default="data/sector_taxonomy/round40_validation_protocol.csv")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_round40_round_protocol_reports(
        output_directory=Path(args.output_directory),
        round_plan_path=Path(args.round_plan),
        validation_protocol_path=Path(args.validation_protocol),
    )
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
