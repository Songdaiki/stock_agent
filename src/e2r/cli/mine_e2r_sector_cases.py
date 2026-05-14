"""Dry-run workflow for mining E2R archetype case-library candidates."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Sequence

from e2r.sector.archetypes import E2RArchetype, archetype_definition
from e2r.sector.case_library import load_case_library, write_case_coverage_outputs
from e2r.sector.taxonomy import load_sector_taxonomy


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plan or run E2R sector case mining.")
    parser.add_argument("--archetype", choices=[item.value for item in E2RArchetype])
    parser.add_argument("--sector")
    parser.add_argument("--market", default="KR")
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)
    parser.add_argument("--min-positive-cases", type=int, default=2)
    parser.add_argument("--min-counterexamples", type=int, default=2)
    parser.add_argument("--taxonomy", default="data/sector_taxonomy/korea_sector_map.csv")
    parser.add_argument("--case-library", default="data/e2r_case_library/cases.jsonl")
    parser.add_argument("--output-directory", default="output/e2r_case_library")
    parser.add_argument("--use-web-search", action="store_true")
    parser.add_argument("--use-official-apis", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def planned_searches(
    *,
    taxonomy_path: str | Path,
    archetype: str | None,
    sector: str | None,
    market: str,
    start_date: date,
    end_date: date,
) -> tuple[dict[str, str], ...]:
    rows = tuple(row for row in load_sector_taxonomy(taxonomy_path) if row.market == market)
    if archetype:
        rows = tuple(row for row in rows if row.primary_archetype.value == archetype)
    if sector:
        rows = tuple(row for row in rows if sector in row.sector_custom or sector in row.sector_raw)
    plans: list[dict[str, str]] = []
    for row in rows:
        definition = archetype_definition(row.primary_archetype)
        signals = (*definition.stage1_radar_signals[:2], *definition.stage2_candidate_signals[:2])
        for signal in signals:
            plans.append(
                {
                    "symbol": row.symbol,
                    "company_name": row.company_name,
                    "primary_archetype": row.primary_archetype.value,
                    "query": f"{row.company_name} {signal} {start_date.year} {end_date.year} PDF",
                    "purpose": "case_mining_candidate_search",
                }
            )
    return tuple(plans)


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output = Path(args.output_directory)
    output.mkdir(parents=True, exist_ok=True)
    cases = load_case_library(args.case_library)
    paths = write_case_coverage_outputs(
        cases,
        output,
        min_positive_cases=args.min_positive_cases,
        min_counterexamples=args.min_counterexamples,
    )
    plans = planned_searches(
        taxonomy_path=args.taxonomy,
        archetype=args.archetype,
        sector=args.sector,
        market=args.market,
        start_date=date.fromisoformat(args.start_date),
        end_date=date.fromisoformat(args.end_date),
    )
    plan_path = output / "planned_searches.json"
    plan_path.write_text(json.dumps(list(plans), ensure_ascii=False, indent=2), encoding="utf-8")
    plan_md = output / "planned_searches.md"
    plan_md.write_text(_render_planned_searches(plans, args.dry_run), encoding="utf-8")
    print(f"dry_run={args.dry_run}")
    print(f"planned_searches={plan_path}")
    for name, path in paths.items():
        print(f"{name}={path}")
    return 0


def _render_planned_searches(plans: tuple[dict[str, str], ...], dry_run: bool) -> str:
    lines = [
        "# E2R Sector Case Mining Plan",
        "",
        f"- dry_run: {dry_run}",
        f"- planned_search_count: {len(plans)}",
        "",
        "| symbol | company | archetype | query |",
        "|---|---|---|---|",
    ]
    for plan in plans[:200]:
        lines.append(f"| {plan['symbol']} | {plan['company_name']} | {plan['primary_archetype']} | {plan['query']} |")
    if len(plans) > 200:
        lines.append(f"| ... | ... | ... | {len(plans) - 200} more |")
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Dry-run planning does not fetch web pages or create evidence.",
            "- Existing case labels are not candidate-generation input.",
            "- If evidence is insufficient, the case remains uncovered instead of being forced.",
        ]
    )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
