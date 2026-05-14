"""Round-16 full theme coverage map v0.5.

Round 16 consolidates the theme taxonomy work into a machine-readable coverage
map. It is report/calibration material only. Theme tags route research; they do
not become scoring evidence or candidate-generation labels.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.round10_theme_tag_taxonomy import (
    ROUND10_THEME_ARCHETYPES_RAW,
    Round10LargeSector,
    Round10ThemePosture,
)
from e2r.sector.round12_theme_refinement import ROUND12_REFINEMENTS
from e2r.sector.round14_score_weight_v04 import ROUND14_SCORE_WEIGHT_TARGETS
from e2r.sector.round15_theme_absorption_v05 import ROUND15_THEME_ABSORPTION_TARGETS


ROUND16_SOURCE_ROUND_PATH = "docs/round/round_16.md"
ROUND16_SOURCE_ROUNDS = (
    "docs/round/round_10.md",
    "docs/round/round_12.md",
    "docs/round/round_14.md",
    "docs/round/round_15.md",
    ROUND16_SOURCE_ROUND_PATH,
)


@dataclass(frozen=True)
class Round16ThemeCoverageEntry:
    theme_tag: str
    large_sector: Round10LargeSector
    primary_sub_archetype: str
    canonical_archetype: E2RArchetype
    posture: Round10ThemePosture
    must_have_evidence: tuple[str, ...]
    red_flag_evidence: tuple[str, ...]
    green_policy: str
    source_round: str

    @property
    def theme_is_score_input(self) -> bool:
        return False

    @property
    def production_scoring_changed(self) -> bool:
        return False


@dataclass(frozen=True)
class Round16ScoreWeightGroup:
    group_name: str
    posture: Round10ThemePosture
    examples: tuple[str, ...]
    eps_fcf: int
    structural_visibility: int
    bottleneck_pricing: int
    market_mispricing: int
    valuation: int
    capital_allocation: int = 0
    interpretation: str = ""


ROUND16_SCORE_WEIGHT_GROUPS: tuple[Round16ScoreWeightGroup, ...] = (
    Round16ScoreWeightGroup("CONTRACT_BACKLOG_GREEN", Round10ThemePosture.GREEN_POSSIBLE, ("전력설비", "전선-케이블", "방산", "조선"), 20, 24, 22, 12, 12, 0, "Contract/backlog evidence can support Green only with quality, margin, and EPS/FCF revision."),
    Round16ScoreWeightGroup("AI_DATA_CENTER_INFRA_GREEN", Round10ThemePosture.GREEN_POSSIBLE, ("AI 데이터센터", "전력망", "PCB", "냉각시스템"), 22, 23, 20, 14, 12, 0, "AI infrastructure needs orders, bottleneck evidence, and revision support."),
    Round16ScoreWeightGroup("K_FOOD_BEAUTY_GREEN", Round10ThemePosture.GREEN_POSSIBLE, ("라면", "K-푸드", "K뷰티", "화장품 OEM"), 22, 23, 12, 16, 13, 0, "Export consumer/beauty evidence comes from channel, repeat demand, OPM, and revisions."),
    Round16ScoreWeightGroup("MEMORY_HBM_GREEN", Round10ThemePosture.GREEN_POSSIBLE, ("HBM", "반도체-HBM", "종합반도체"), 24, 21, 19, 15, 12, 0, "HBM needs multi-year demand, price/capacity discipline, and medium-term revision."),
    Round16ScoreWeightGroup("CDMO_MEDICAL_DEVICE_GREEN", Round10ThemePosture.GREEN_POSSIBLE, ("CMO", "바이오시밀러", "미용기기", "임플란트"), 20, 24, 13, 14, 12, 0, "CDMO/medical device Green requires contract/utilization or repeat consumable revenue."),
    Round16ScoreWeightGroup("FINANCIAL_INSURANCE_GREEN", Round10ThemePosture.GREEN_POSSIBLE, ("은행", "손해보험", "생명보험", "밸류업"), 15, 20, 5, 15, 25, 10, "Financial rerating depends on ROE/PBR, capital strength, and executed return."),
    Round16ScoreWeightGroup("PLATFORM_SOFTWARE_WATCH", Round10ThemePosture.WATCH_YELLOW_FIRST, ("클라우드 컴퓨팅", "AI 소프트웨어", "IT보안"), 20, 22, 8, 16, 14, 0, "Platform/SW is Watch until monetization, recurring revenue, and margin leverage are visible."),
    Round16ScoreWeightGroup("ROBOTICS_WATCH", Round10ThemePosture.WATCH_YELLOW_FIRST, ("피지컬AI", "휴머노이드", "제조용 로봇"), 18, 15, 10, 12, 10, 0, "Robotics requires revenue conversion before high-conviction treatment."),
    Round16ScoreWeightGroup("NUCLEAR_POLICY_WATCH", Round10ThemePosture.WATCH_YELLOW_FIRST, ("원자력", "SMR", "스마트그리드"), 18, 22, 8, 14, 12, 0, "Nuclear/policy themes need binding contracts and low legal risk."),
    Round16ScoreWeightGroup("AUTO_COMPONENTS_WATCH", Round10ThemePosture.WATCH_YELLOW_FIRST, ("현대차", "기아", "타이어", "자율주행"), 20, 18, 10, 15, 17, 0, "Auto needs mix, customer diversification, cost control, and sometimes shareholder return."),
    Round16ScoreWeightGroup("RETAIL_ECOMMERCE_WATCH", Round10ThemePosture.WATCH_YELLOW_FIRST, ("편의점", "홈쇼핑", "마켓컬리", "콜드체인"), 18, 16, 5, 14, 14, 0, "Retail/e-commerce needs OPM and FCF, not traffic or listing events alone."),
    Round16ScoreWeightGroup("DIGITAL_ASSET_WATCH", Round10ThemePosture.WATCH_YELLOW_FIRST, ("STO", "스테이블코인", "결제서비스"), 16, 18, 8, 16, 12, 0, "Digital finance is Watch until regulation, volume, and fee economics are real."),
    Round16ScoreWeightGroup("SHIPPING_FREIGHT_REDTEAM", Round10ThemePosture.REDTEAM_FIRST, ("해운", "운임", "종합물류"), 20, 10, 18, 8, 8, 0, "Shipping can explode cyclically, so Green is highly restricted."),
    Round16ScoreWeightGroup("COMMODITY_CHEMICAL_REDTEAM", Round10ThemePosture.REDTEAM_FIRST, ("화학", "철강", "비철금속", "대두"), 20, 10, 18, 10, 10, 0, "Commodity/spread cases need reversal and oversupply guards."),
    Round16ScoreWeightGroup("BATTERY_OVERHEAT_REDTEAM", Round10ThemePosture.REDTEAM_FIRST, ("2차전지 소재", "전고체 배터리", "리튬"), 20, 16, 14, 10, 10, 0, "Battery themes require strong overheat and CAPA risk defense."),
    Round16ScoreWeightGroup("CONSTRUCTION_PF_REDTEAM", Round10ThemePosture.REDTEAM_FIRST, ("건설사", "PF", "건자재"), 18, 10, 8, 12, 10, 0, "Construction is credit-risk first; relief rallies are not structural E2R."),
    Round16ScoreWeightGroup("ONE_OFF_DISEASE_REDTEAM", Round10ThemePosture.REDTEAM_FIRST, ("엠폭스", "코로나19", "빈대퇴치", "황사마스크"), 20, 5, 5, 5, 5, 0, "One-off disease/event EPS spikes are usually Red/4B defense material."),
    Round16ScoreWeightGroup("SPECULATIVE_SCIENCE_REDTEAM", Round10ThemePosture.REDTEAM_FIRST, ("초전도체", "맥신", "그래핀", "양자 기술"), 5, 5, 5, 5, 5, 0, "Speculative science is Green-blocked until commercialization and revenue exist."),
)


def round16_coverage_entries() -> tuple[Round16ThemeCoverageEntry, ...]:
    entries: list[Round16ThemeCoverageEntry] = []
    entries.extend(_entries_from_round10())
    entries.extend(_entries_from_round12())
    entries.extend(_entries_from_round14())
    entries.extend(_entries_from_round15())
    return tuple(entries)


def round16_theme_tag_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "theme_tag": entry.theme_tag,
            "large_sector": entry.large_sector.value,
            "primary_sub_archetype": entry.primary_sub_archetype,
            "canonical_archetype": entry.canonical_archetype.value,
            "posture": entry.posture.value,
            "must_have_evidence": "|".join(entry.must_have_evidence),
            "red_flag_evidence": "|".join(entry.red_flag_evidence),
            "green_policy": entry.green_policy,
            "theme_is_score_input": str(entry.theme_is_score_input).lower(),
            "production_scoring_changed": str(entry.production_scoring_changed).lower(),
            "source_round": entry.source_round,
        }
        for entry in round16_coverage_entries()
    )


def round16_score_group_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "group_name": group.group_name,
            "posture": group.posture.value,
            "examples": "|".join(group.examples),
            "eps_fcf": str(group.eps_fcf),
            "structural_visibility": str(group.structural_visibility),
            "bottleneck_pricing": str(group.bottleneck_pricing),
            "market_mispricing": str(group.market_mispricing),
            "valuation": str(group.valuation),
            "capital_allocation": str(group.capital_allocation),
            "interpretation": group.interpretation,
            "production_scoring_changed": "false",
        }
        for group in ROUND16_SCORE_WEIGHT_GROUPS
    )


def round16_coverage_summary() -> dict[str, int | bool]:
    entries = round16_coverage_entries()
    return {
        "large_sector_count": len({entry.large_sector for entry in entries}),
        "sub_archetype_count": len({entry.primary_sub_archetype for entry in entries}),
        "theme_tag_row_count": len(entries),
        "unique_theme_tag_count": len({entry.theme_tag for entry in entries}),
        "score_group_count": len(ROUND16_SCORE_WEIGHT_GROUPS),
        "production_scoring_changed": False,
        "theme_tags_are_score_input": False,
    }


def find_round16_theme_tag(tag: str) -> tuple[dict[str, str], ...]:
    needle = tag.lower()
    return tuple(row for row in round16_theme_tag_rows() if row["theme_tag"].lower() == needle)


def write_round16_theme_coverage_reports(
    *,
    output_directory: str | Path = "output/e2r_round16_theme_coverage_v05",
    theme_map_path: str | Path = "data/sector_taxonomy/theme_tag_map_round16.csv",
    score_group_path: str | Path = "data/sector_taxonomy/score_weight_groups_round16.csv",
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    theme_map = Path(theme_map_path)
    score_group = Path(score_group_path)
    theme_map.parent.mkdir(parents=True, exist_ok=True)
    score_group.parent.mkdir(parents=True, exist_ok=True)
    paths = {
        "theme_map": theme_map,
        "score_groups": score_group,
        "summary": output / "round16_theme_coverage_v05_summary.md",
        "coverage_matrix": output / "round16_theme_coverage_matrix.csv",
        "green_policy": output / "round16_green_watch_red_policy.md",
        "score_group_report": output / "round16_score_weight_groups.md",
        "next_plan": output / "round16_next_machine_input_plan.md",
    }
    _write_rows(round16_theme_tag_rows(), paths["theme_map"])
    _write_rows(round16_theme_tag_rows(), paths["coverage_matrix"])
    _write_rows(round16_score_group_rows(), paths["score_groups"])
    paths["summary"].write_text(render_round16_summary_markdown(), encoding="utf-8")
    paths["green_policy"].write_text(render_round16_green_policy_markdown(), encoding="utf-8")
    paths["score_group_report"].write_text(render_round16_score_group_markdown(), encoding="utf-8")
    paths["next_plan"].write_text(render_round16_next_plan_markdown(), encoding="utf-8")
    return paths


def render_round16_summary_markdown() -> str:
    summary = round16_coverage_summary()
    return "\n".join(
        [
            "# Round-16 Theme Coverage v0.5 Summary",
            "",
            f"- source_round: `{ROUND16_SOURCE_ROUND_PATH}`",
            f"- source_rounds: {', '.join(f'`{path}`' for path in ROUND16_SOURCE_ROUNDS)}",
            f"- large_sector_count: {summary['large_sector_count']}",
            f"- sub_archetype_count: {summary['sub_archetype_count']}",
            f"- theme_tag_row_count: {summary['theme_tag_row_count']}",
            f"- unique_theme_tag_count: {summary['unique_theme_tag_count']}",
            f"- score_group_count: {summary['score_group_count']}",
            "- production_scoring_changed: false",
            "- theme_tags_are_score_input: false",
            "",
            "## Interpretation",
            "- Round 16 is a coverage map, not a production scoring change.",
            "- Raw theme tags route search and case mining.",
            "- Evidence fields, score-price alignment, and price-path validation decide future scoring.",
            "- Example: `초전도체` routes to speculative-science RedTeam checks; it does not create score.",
        ]
    ) + "\n"


def render_round16_green_policy_markdown() -> str:
    rows = round16_theme_tag_rows()
    groups: dict[str, set[str]] = {posture.value: set() for posture in Round10ThemePosture}
    for row in rows:
        groups[row["posture"]].add(row["primary_sub_archetype"])
    lines = ["# Round-16 Green / Watch / Red Policy", ""]
    for posture in Round10ThemePosture:
        lines.append(f"## {posture.value}")
        for label in sorted(groups[posture.value]):
            lines.append(f"- `{label}`")
        lines.append("")
    return "\n".join(lines)


def render_round16_score_group_markdown() -> str:
    lines = ["# Round-16 Score-Weight Groups v0.5", ""]
    for group in ROUND16_SCORE_WEIGHT_GROUPS:
        lines.append(f"## {group.group_name}")
        lines.append(f"- posture: `{group.posture.value}`")
        lines.append(f"- examples: {', '.join(f'`{item}`' for item in group.examples)}")
        lines.append(
            "- weights: "
            f"EPS/FCF {group.eps_fcf}, "
            f"Visibility {group.structural_visibility}, "
            f"Bottleneck {group.bottleneck_pricing}, "
            f"Mispricing {group.market_mispricing}, "
            f"Valuation {group.valuation}, "
            f"Capital Allocation {group.capital_allocation}"
        )
        lines.append(f"- interpretation: {group.interpretation}")
        lines.append("")
    lines.append("production_scoring_changed: false")
    return "\n".join(lines) + "\n"


def render_round16_next_plan_markdown() -> str:
    return "\n".join(
        [
            "# Round-16 Next Machine Input Plan",
            "",
            "1. Review `theme_tag_map_round16.csv` for duplicate or ambiguous theme tags.",
            "2. Collapse aliases only when the evidence requirements are identical.",
            "3. Use the map to create `cases_v03.jsonl` candidates, not production candidates.",
            "4. Backfill price paths and run score-price alignment before shadow scoring.",
            "5. Keep StageClassifier and Stage 3-Green thresholds unchanged.",
            "",
            "## What Not To Change",
            "- Do not use raw theme names as score evidence.",
            "- Do not use this coverage map as candidate-generation labels.",
            "- Do not treat policy, disaster, speculative science, or one-off demand as structural E2R without recurring EPS/FCF evidence.",
            "",
        ]
    )


def _entries_from_round10() -> tuple[Round16ThemeCoverageEntry, ...]:
    entries: list[Round16ThemeCoverageEntry] = []
    for item in ROUND10_THEME_ARCHETYPES_RAW:
        for tag in item.theme_tags:
            entries.append(
                Round16ThemeCoverageEntry(
                    theme_tag=tag,
                    large_sector=item.large_sector,
                    primary_sub_archetype=item.label,
                    canonical_archetype=item.canonical_archetype,
                    posture=item.posture,
                    must_have_evidence=item.must_have_evidence,
                    red_flag_evidence=(),
                    green_policy=item.green_policy,
                    source_round="round10",
                )
            )
    return tuple(entries)


def _entries_from_round12() -> tuple[Round16ThemeCoverageEntry, ...]:
    entries: list[Round16ThemeCoverageEntry] = []
    for item in ROUND12_REFINEMENTS:
        for tag in item.theme_tags:
            entries.append(
                Round16ThemeCoverageEntry(
                    theme_tag=tag,
                    large_sector=item.large_sector,
                    primary_sub_archetype=item.sub_archetype,
                    canonical_archetype=item.canonical_archetype,
                    posture=item.posture,
                    must_have_evidence=item.must_have_evidence,
                    red_flag_evidence=item.red_flag_evidence,
                    green_policy=item.green_policy,
                    source_round="round12",
                )
            )
    return tuple(entries)


def _entries_from_round14() -> tuple[Round16ThemeCoverageEntry, ...]:
    entries: list[Round16ThemeCoverageEntry] = []
    for item in ROUND14_SCORE_WEIGHT_TARGETS:
        for tag in item.theme_tags:
            entries.append(
                Round16ThemeCoverageEntry(
                    theme_tag=tag,
                    large_sector=item.large_sector,
                    primary_sub_archetype=item.sub_archetype,
                    canonical_archetype=item.canonical_archetype,
                    posture=item.posture,
                    must_have_evidence=item.must_have_evidence,
                    red_flag_evidence=item.red_flags,
                    green_policy=item.normalization_point,
                    source_round="round14",
                )
            )
    return tuple(entries)


def _entries_from_round15() -> tuple[Round16ThemeCoverageEntry, ...]:
    entries: list[Round16ThemeCoverageEntry] = []
    for item in ROUND15_THEME_ABSORPTION_TARGETS:
        for tag in item.theme_tags:
            entries.append(
                Round16ThemeCoverageEntry(
                    theme_tag=tag,
                    large_sector=item.large_sector,
                    primary_sub_archetype=item.sub_archetype,
                    canonical_archetype=item.canonical_archetype,
                    posture=item.posture,
                    must_have_evidence=item.must_have_evidence,
                    red_flag_evidence=item.red_flags,
                    green_policy=item.normalization_point,
                    source_round="round15",
                )
            )
    return tuple(entries)


def _write_rows(rows: Iterable[Mapping[str, str]], path: Path) -> Path:
    row_tuple = tuple(rows)
    if not row_tuple:
        path.write_text("", encoding="utf-8")
        return path
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(row_tuple[0].keys()))
        writer.writeheader()
        for row in row_tuple:
            writer.writerow(row)
    return path


__all__ = [
    "ROUND16_SCORE_WEIGHT_GROUPS",
    "ROUND16_SOURCE_ROUND_PATH",
    "ROUND16_SOURCE_ROUNDS",
    "Round16ScoreWeightGroup",
    "Round16ThemeCoverageEntry",
    "find_round16_theme_tag",
    "render_round16_green_policy_markdown",
    "render_round16_next_plan_markdown",
    "render_round16_score_group_markdown",
    "render_round16_summary_markdown",
    "round16_coverage_entries",
    "round16_coverage_summary",
    "round16_score_group_rows",
    "round16_theme_tag_rows",
    "write_round16_theme_coverage_reports",
]
