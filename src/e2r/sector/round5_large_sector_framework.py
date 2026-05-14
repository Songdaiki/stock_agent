"""Round-5 large-sector framework.

Round 5 groups archetypes into broad Korea-market sectors before any production
score changes. It is calibration/reporting material only.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import E2RArchetype
from e2r.sector.case_library import E2RCaseRecord, load_case_library


ROUND5_SOURCE_ROUND_PATH = "docs/round/round_05.md"


class Round5GreenPermission(str, Enum):
    """Round-5 Green posture by large sector."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    RESTRICTED = "RESTRICTED"


class Round5LargeSector(str, Enum):
    """Ten large-sector buckets from the Round-5 synthesis."""

    INDUSTRIAL_ORDERS = "INDUSTRIAL_ORDERS"
    EXPORT_CONSUMER = "EXPORT_CONSUMER"
    SEMICONDUCTOR_AI_INFRA = "SEMICONDUCTOR_AI_INFRA"
    CYCLICAL_SPREAD = "CYCLICAL_SPREAD"
    FINANCIAL_CAPITAL_ALLOCATION = "FINANCIAL_CAPITAL_ALLOCATION"
    BIOTECH_HEALTHCARE = "BIOTECH_HEALTHCARE"
    PLATFORM_IP_SERVICES = "PLATFORM_IP_SERVICES"
    DOMESTIC_REOPENING = "DOMESTIC_REOPENING"
    REAL_ESTATE_CREDIT_REGULATED = "REAL_ESTATE_CREDIT_REGULATED"
    THEME_EVENT_GUARDRAIL = "THEME_EVENT_GUARDRAIL"


@dataclass(frozen=True)
class Round5LargeSectorDefinition:
    """One large-sector bucket and its calibration posture."""

    large_sector: Round5LargeSector
    korean_name: str
    archetypes: tuple[E2RArchetype, ...]
    green_permission: Round5GreenPermission
    green_policy: str
    required_evidence: tuple[str, ...]
    primary_risks: tuple[str, ...]
    peer_normalization_focus: tuple[str, ...]
    examples: tuple[str, ...]


def _definition(
    large_sector: Round5LargeSector,
    *,
    korean_name: str,
    archetypes: tuple[E2RArchetype, ...],
    green_permission: Round5GreenPermission,
    green_policy: str,
    required_evidence: tuple[str, ...],
    primary_risks: tuple[str, ...],
    peer_normalization_focus: tuple[str, ...],
    examples: tuple[str, ...],
) -> Round5LargeSectorDefinition:
    return Round5LargeSectorDefinition(
        large_sector=large_sector,
        korean_name=korean_name,
        archetypes=archetypes,
        green_permission=green_permission,
        green_policy=green_policy,
        required_evidence=required_evidence,
        primary_risks=primary_risks,
        peer_normalization_focus=peer_normalization_focus,
        examples=examples,
    )


ROUND5_LARGE_SECTOR_DEFINITIONS: Mapping[Round5LargeSector, Round5LargeSectorDefinition] = {
    Round5LargeSector.INDUSTRIAL_ORDERS: _definition(
        Round5LargeSector.INDUSTRIAL_ORDERS,
        korean_name="산업재/수주",
        archetypes=(
            E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,
            E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,
            E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG,
            E2RArchetype.NUCLEAR_SMR_GRID_POLICY,
        ),
        green_permission=Round5GreenPermission.HIGH,
        green_policy="Green possible with contract quality, backlog, margin path, and low cancellation/legal risk.",
        required_evidence=("contract_quality", "backlog_or_delivery_schedule", "op_eps_revision", "margin_visibility"),
        primary_risks=("contract_cancellation", "low_margin_backlog", "legal_or_policy_delay", "cost_overrun"),
        peer_normalization_focus=("order_backlog_to_sales", "op_revision_percentile", "margin_expansion_percentile"),
        examples=("HD현대일렉트릭", "일진전기", "한화에어로스페이스", "체코 원전"),
    ),
    Round5LargeSector.EXPORT_CONSUMER: _definition(
        Round5LargeSector.EXPORT_CONSUMER,
        korean_name="수출 소비재",
        archetypes=(
            E2RArchetype.EXPORT_RECURRING_CONSUMER,
            E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,
            E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT,
        ),
        green_permission=Round5GreenPermission.HIGH,
        green_policy="Green possible when repeat demand, export/channel expansion, OPM, and FY1/FY2 revisions align.",
        required_evidence=("export_growth", "channel_expansion", "recurring_demand", "opm_or_roe_improvement"),
        primary_risks=("single_product_fad", "inventory_or_receivables", "regulatory_or_recall", "channel_stuffing"),
        peer_normalization_focus=("export_growth_percentile", "opm_expansion_percentile", "roe_percentile"),
        examples=("삼양식품", "실리콘투", "Classys"),
    ),
    Round5LargeSector.SEMICONDUCTOR_AI_INFRA: _definition(
        Round5LargeSector.SEMICONDUCTOR_AI_INFRA,
        korean_name="반도체/AI 인프라",
        archetypes=(
            E2RArchetype.MEMORY_HBM_CAPACITY,
            E2RArchetype.SEMI_EQUIPMENT_CAPEX,
            E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE,
        ),
        green_permission=Round5GreenPermission.HIGH,
        green_policy="Green possible only with HBM/data-center demand, confirmed orders or pricing, and revision support.",
        required_evidence=("hbm_or_ai_dc_demand", "capacity_bottleneck", "pricing_or_order_support", "medium_term_revision"),
        primary_risks=("capex_cut", "supply_glut", "ai_keyword_only", "customer_concentration"),
        peer_normalization_focus=("revision_percentile", "price_strength_percentile", "capex_order_visibility"),
        examples=("SK하이닉스", "한미반도체", "이수페타시스", "AI 데이터센터 전력망"),
    ),
    Round5LargeSector.CYCLICAL_SPREAD: _definition(
        Round5LargeSector.CYCLICAL_SPREAD,
        korean_name="사이클/스프레드",
        archetypes=(
            E2RArchetype.SHIPPING_FREIGHT_CYCLE,
            E2RArchetype.COMMODITY_SPREAD,
            E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT,
            E2RArchetype.AUTO_MOBILITY_COMPONENTS,
            E2RArchetype.AUTO_MOBILITY_COMPLETED_VEHICLE,
            E2RArchetype.RARE_METALS_STRATEGIC_MATERIALS,
        ),
        green_permission=Round5GreenPermission.LOW,
        green_policy="Green is capped unless the move is more than a spot spread or theme cycle.",
        required_evidence=("spread_or_price_support", "cost_curve_or_supply_discipline", "revision_support", "cycle_risk_control"),
        primary_risks=("cycle_normalization", "overcapacity", "valuation_overheat", "demand_slowdown"),
        peer_normalization_focus=("spread_percentile", "revision_percentile", "valuation_heat_percentile"),
        examples=("HMM 운임 사이클", "정유/화학 스프레드", "2차전지 과열", "희소금속 이벤트"),
    ),
    Round5LargeSector.FINANCIAL_CAPITAL_ALLOCATION: _definition(
        Round5LargeSector.FINANCIAL_CAPITAL_ALLOCATION,
        korean_name="금융/자본배분",
        archetypes=(
            E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
            E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN,
            E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE,
            E2RArchetype.TURNAROUND_COST_RESTRUCTURING,
        ),
        green_permission=Round5GreenPermission.MEDIUM,
        green_policy="Green requires ROE/PBR, executed capital return, NAV/FCF support, or durable cost restructuring.",
        required_evidence=("roe_or_fcf_improvement", "capital_return_execution", "balance_sheet_quality", "discount_narrowing_catalyst"),
        primary_risks=("low_pbr_value_trap", "credit_cost", "event_premium_only", "buyback_without_cancel"),
        peer_normalization_focus=("roe_percentile", "pbr_discount_percentile", "capital_return_percentile"),
        examples=("KB금융", "메리츠금융", "SK스퀘어", "삼성물산"),
    ),
    Round5LargeSector.BIOTECH_HEALTHCARE: _definition(
        Round5LargeSector.BIOTECH_HEALTHCARE,
        korean_name="바이오/헬스케어",
        archetypes=(
            E2RArchetype.BIOTECH_REGULATORY,
            E2RArchetype.BIOTECH_PRE_REVENUE_REGULATORY,
            E2RArchetype.BIOTECH_ROYALTY_COMMERCIALIZATION,
            E2RArchetype.CDMO_HEALTHCARE_CONTRACT,
        ),
        green_permission=Round5GreenPermission.LOW,
        green_policy="Pre-revenue biotech is Green-blocked; royalty, commercial revenue, or CDMO contract conversion is required.",
        required_evidence=("commercialization_path", "royalty_or_revenue", "cash_runway", "dilution_risk_low"),
        primary_risks=("clinical_failure", "approval_delay", "cb_or_rights_dilution", "underutilized_capacity"),
        peer_normalization_focus=("revenue_conversion_visibility", "cash_runway", "dilution_risk"),
        examples=("알테오젠", "유한양행", "삼성바이오로직스", "셀트리온"),
    ),
    Round5LargeSector.PLATFORM_IP_SERVICES: _definition(
        Round5LargeSector.PLATFORM_IP_SERVICES,
        korean_name="플랫폼/IP/서비스",
        archetypes=(
            E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
            E2RArchetype.GAME_CONTENT_IP,
            E2RArchetype.EDUCATION_SPECIALTY_SERVICES,
        ),
        green_permission=Round5GreenPermission.MEDIUM,
        green_policy="Green requires monetization, repeat revenue, OPM/FCF leverage, and low regulation/IP risk.",
        required_evidence=("arpu_or_take_rate", "repeat_monetization", "opm_or_fcf_leverage", "retention_or_ip_repeatability"),
        primary_risks=("mau_without_monetization", "new_launch_hype", "single_ip_dependence", "policy_or_governance_risk"),
        peer_normalization_focus=("arpu_growth_percentile", "opm_expansion_percentile", "recurring_revenue_percentile"),
        examples=("NAVER", "더존비즈온", "Krafton", "메가스터디교육"),
    ),
    Round5LargeSector.DOMESTIC_REOPENING: _definition(
        Round5LargeSector.DOMESTIC_REOPENING,
        korean_name="내수/리오프닝",
        archetypes=(
            E2RArchetype.RETAIL_DOMESTIC_CONSUMER,
            E2RArchetype.TRAVEL_LEISURE_REOPENING,
        ),
        green_permission=Round5GreenPermission.LOW,
        green_policy="Green needs repeated OPM/FCF improvement, not only traffic or reopening rebound.",
        required_evidence=("same_store_or_visitor_growth", "opm_improvement", "inventory_normalization", "fixed_cost_leverage"),
        primary_risks=("traffic_only_rebound", "china_dependency", "oil_or_fx_shock", "rent_or_wage_pressure"),
        peer_normalization_focus=("same_store_sales_percentile", "opm_expansion_percentile", "inventory_turnover"),
        examples=("BGF리테일", "GS리테일", "호텔신라", "대한항공"),
    ),
    Round5LargeSector.REAL_ESTATE_CREDIT_REGULATED: _definition(
        Round5LargeSector.REAL_ESTATE_CREDIT_REGULATED,
        korean_name="부동산/신용/규제자산",
        archetypes=(
            E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT,
            E2RArchetype.UTILITIES_REGULATED_TARIFF,
        ),
        green_permission=Round5GreenPermission.RESTRICTED,
        green_policy="Green is very restricted because PF, credit, tariff, debt, and regulation dominate headline growth.",
        required_evidence=("pf_or_debt_risk_resolved", "cash_flow_improvement", "policy_or_tariff_durability", "cost_pass_through"),
        primary_risks=("pf_loss", "unsold_inventory", "tariff_freeze", "debt_burden"),
        peer_normalization_focus=("cash_flow_improvement", "debt_ratio", "policy_risk_score"),
        examples=("PF 리스크 해소형 건설사", "한국전력", "한국가스공사"),
    ),
    Round5LargeSector.THEME_EVENT_GUARDRAIL: _definition(
        Round5LargeSector.THEME_EVENT_GUARDRAIL,
        korean_name="테마/이벤트",
        archetypes=(
            E2RArchetype.ROBOTICS_FACTORY_AUTOMATION,
            E2RArchetype.ONE_OFF_EVENT_DEMAND,
            E2RArchetype.THEME_VALUATION_OVERHEAT,
            E2RArchetype.GENERIC_UNCLASSIFIED,
        ),
        green_permission=Round5GreenPermission.RESTRICTED,
        green_policy="Mostly Stage 1/2, Red, 4B, or 4C guardrail; Green requires unusually strong cash-flow conversion.",
        required_evidence=("revenue_conversion", "eps_fcf_support", "low_one_off_risk", "low_crowding"),
        primary_risks=("theme_only", "price_only_rally", "one_off_normalization", "valuation_saturation"),
        peer_normalization_focus=("valuation_heat_percentile", "price_strength_percentile", "revision_absence"),
        examples=("로봇 테마", "씨젠 2020", "SMCI 2024", "에코프로비엠 2023"),
    ),
}


ROUND5_ARCHETYPE_PRIMARY_LARGE_SECTOR: Mapping[E2RArchetype, Round5LargeSector] = {
    archetype: definition.large_sector
    for definition in ROUND5_LARGE_SECTOR_DEFINITIONS.values()
    for archetype in definition.archetypes
}

ROUND5_ARCHETYPE_SECONDARY_LARGE_SECTORS: Mapping[E2RArchetype, tuple[Round5LargeSector, ...]] = {
    E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE: (Round5LargeSector.INDUSTRIAL_ORDERS,),
    E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT: (Round5LargeSector.BIOTECH_HEALTHCARE,),
    E2RArchetype.ROBOTICS_FACTORY_AUTOMATION: (Round5LargeSector.PLATFORM_IP_SERVICES,),
    E2RArchetype.RARE_METALS_STRATEGIC_MATERIALS: (Round5LargeSector.FINANCIAL_CAPITAL_ALLOCATION,),
}


ROUND5_NEW_OR_CONFIRMED_ARCHETYPES = (
    E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE,
    E2RArchetype.NUCLEAR_SMR_GRID_POLICY,
    E2RArchetype.TRAVEL_LEISURE_REOPENING,
    E2RArchetype.EDUCATION_SPECIALTY_SERVICES,
    E2RArchetype.RARE_METALS_STRATEGIC_MATERIALS,
    E2RArchetype.CDMO_HEALTHCARE_CONTRACT,
    E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN,
)


def round5_large_sector_for(archetype: E2RArchetype | str) -> Round5LargeSector:
    item = _archetype(archetype)
    return ROUND5_ARCHETYPE_PRIMARY_LARGE_SECTOR.get(item, Round5LargeSector.THEME_EVENT_GUARDRAIL)


def round5_large_sectors_for(archetype: E2RArchetype | str) -> tuple[Round5LargeSector, ...]:
    item = _archetype(archetype)
    primary = round5_large_sector_for(item)
    secondary = ROUND5_ARCHETYPE_SECONDARY_LARGE_SECTORS.get(item, ())
    return tuple(dict.fromkeys((primary, *secondary)))


def round5_definition(large_sector: Round5LargeSector | str) -> Round5LargeSectorDefinition:
    item = large_sector if isinstance(large_sector, Round5LargeSector) else Round5LargeSector(str(large_sector))
    return ROUND5_LARGE_SECTOR_DEFINITIONS[item]


def round5_archetype_rows() -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for archetype in E2RArchetype:
        primary = round5_large_sector_for(archetype)
        sectors = round5_large_sectors_for(archetype)
        definition = round5_definition(primary)
        rows.append(
            {
                "archetype": archetype.value,
                "primary_large_sector": primary.value,
                "secondary_large_sectors": "|".join(item.value for item in sectors[1:]),
                "korean_name": definition.korean_name,
                "green_permission": definition.green_permission.value,
                "green_policy": definition.green_policy,
                "required_evidence": "|".join(definition.required_evidence),
                "primary_risks": "|".join(definition.primary_risks),
            }
        )
    return tuple(rows)


def round5_case_coverage_by_large_sector(records: Iterable[E2RCaseRecord]) -> tuple[dict[str, object], ...]:
    rows = tuple(records)
    output: list[dict[str, object]] = []
    for large_sector in Round5LargeSector:
        definition = round5_definition(large_sector)
        subset = tuple(record for record in rows if round5_large_sector_for(record.primary_archetype) == large_sector)
        output.append(
            {
                "large_sector": large_sector.value,
                "korean_name": definition.korean_name,
                "green_permission": definition.green_permission.value,
                "archetype_count": len(definition.archetypes),
                "case_count": len(subset),
                "aligned_count": sum(1 for record in subset if record.score_price_alignment == "aligned"),
                "unknown_alignment_count": sum(1 for record in subset if record.score_price_alignment == "unknown"),
                "price_backfill_needed_count": sum(
                    1 for record in subset if record.price_validation.price_validation_status != "price_filled"
                ),
            }
        )
    return tuple(output)


def write_round5_large_sector_reports(
    *,
    case_path: str | Path = "data/e2r_case_library/cases_v02.jsonl",
    output_directory: str | Path = "output/e2r_round5_large_sector_framework",
) -> dict[str, Path]:
    records = load_case_library(case_path)
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "framework": output / "round5_large_sector_framework.md",
        "matrix": output / "round5_archetype_large_sector_matrix.csv",
        "green": output / "round5_green_permission_matrix.md",
        "coverage": output / "round5_case_coverage_by_large_sector.csv",
        "next_plan": output / "round5_next_case_expansion_plan.md",
    }
    paths["framework"].write_text(render_round5_large_sector_framework_markdown(), encoding="utf-8")
    _write_archetype_matrix(paths["matrix"])
    paths["green"].write_text(render_round5_green_permission_markdown(), encoding="utf-8")
    _write_case_coverage_csv(records, paths["coverage"])
    paths["next_plan"].write_text(render_round5_next_case_expansion_plan(records), encoding="utf-8")
    return paths


def render_round5_large_sector_framework_markdown() -> str:
    lines = [
        "# Round-5 Large-Sector Framework",
        "",
        f"Source round: `{ROUND5_SOURCE_ROUND_PATH}`",
        "",
        "This is calibration material. It does not change production scoring.",
        "",
        "## Ten Large Sectors",
        "",
        "| large_sector | Korean name | archetypes | Green permission |",
        "|---|---|---:|---|",
    ]
    for definition in ROUND5_LARGE_SECTOR_DEFINITIONS.values():
        lines.append(
            f"| {definition.large_sector.value} | {definition.korean_name} | "
            f"{len(definition.archetypes)} | {definition.green_permission.value} |"
        )
    lines.extend(
        [
            "",
            "## Why This Exists",
            "- Full KOSPI/KOSDAQ coverage should not be tuned one narrow industry at a time.",
            "- Large sectors define the evidence family before archetype-level score weights are tested.",
            "- Example: shipping and diagnostics can show EPS explosions, but their Green posture is restricted because normalization risk is high.",
            "",
            "## New Or Confirmed Extension Archetypes",
        ]
    )
    for item in ROUND5_NEW_OR_CONFIRMED_ARCHETYPES:
        lines.append(f"- {item.value}: primary_large_sector={round5_large_sector_for(item).value}")
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Do not use large-sector labels as candidate-generation answers.",
            "- Do not loosen Stage 3-Green thresholds from this report.",
            "- Use this framework to decide which cases and price paths must be backfilled next.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round5_green_permission_markdown() -> str:
    lines = [
        "# Round-5 Green Permission Matrix",
        "",
        "| large_sector | permission | Green policy | required evidence | primary risks |",
        "|---|---|---|---|---|",
    ]
    for definition in ROUND5_LARGE_SECTOR_DEFINITIONS.values():
        lines.append(
            f"| {definition.korean_name} | {definition.green_permission.value} | {definition.green_policy} | "
            f"{', '.join(definition.required_evidence)} | {', '.join(definition.primary_risks)} |"
        )
    lines.extend(
        [
            "",
            "## Easy Examples",
            "- 전력기기는 계약질, 수주잔고, 리드타임, OPM이 같이 있으면 Green 후보가 될 수 있다.",
            "- 해운은 운임 급등으로 EPS가 커져도 사이클 정상화가 빨라 Green을 제한한다.",
            "- 플랫폼은 MAU가 아니라 ARPU, OPM, FCF가 따라와야 한다.",
            "- 건설은 수주보다 PF와 현금흐름 리스크가 먼저다.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round5_next_case_expansion_plan(records: Iterable[E2RCaseRecord]) -> str:
    coverage = round5_case_coverage_by_large_sector(records)
    lines = [
        "# Round-5 Next Case Expansion Plan",
        "",
        "## Coverage By Large Sector",
        "",
        "| large_sector | cases | unknown_alignment | price_backfill_needed | priority |",
        "|---|---:|---:|---:|---|",
    ]
    for row in coverage:
        priority = _priority_for_coverage(row)
        lines.append(
            f"| {row['large_sector']} | {row['case_count']} | {row['unknown_alignment_count']} | "
            f"{row['price_backfill_needed_count']} | {priority} |"
        )
    lines.extend(
        [
            "",
            "## Priority Rules",
            "- Fill stage dates and price paths before applying score weights.",
            "- Add at least two positive and two counterexample cases per archetype before production score changes.",
            "- Keep platform, game, robotics, construction, utilities, and pre-revenue biotech Green-restricted until score-price validation is filled.",
        ]
    )
    return "\n".join(lines) + "\n"


def _write_archetype_matrix(path: Path) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = (
            "archetype",
            "primary_large_sector",
            "secondary_large_sectors",
            "korean_name",
            "green_permission",
            "green_policy",
            "required_evidence",
            "primary_risks",
        )
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in round5_archetype_rows():
            writer.writerow(row)
    return path


def _write_case_coverage_csv(records: Iterable[E2RCaseRecord], path: Path) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = (
            "large_sector",
            "korean_name",
            "green_permission",
            "archetype_count",
            "case_count",
            "aligned_count",
            "unknown_alignment_count",
            "price_backfill_needed_count",
        )
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in round5_case_coverage_by_large_sector(records):
            writer.writerow(row)
    return path


def _priority_for_coverage(row: Mapping[str, object]) -> str:
    if int(row["price_backfill_needed_count"]) > 0:
        return "fill_price_paths"
    if int(row["unknown_alignment_count"]) > 0:
        return "classify_alignment"
    if str(row["green_permission"]) in {"LOW", "RESTRICTED"}:
        return "add_counterexamples"
    return "ready_for_shadow_review"


def _archetype(value: E2RArchetype | str) -> E2RArchetype:
    if isinstance(value, E2RArchetype):
        return value
    return E2RArchetype(str(value))


__all__ = [
    "ROUND5_ARCHETYPE_PRIMARY_LARGE_SECTOR",
    "ROUND5_ARCHETYPE_SECONDARY_LARGE_SECTORS",
    "ROUND5_LARGE_SECTOR_DEFINITIONS",
    "ROUND5_NEW_OR_CONFIRMED_ARCHETYPES",
    "ROUND5_SOURCE_ROUND_PATH",
    "Round5GreenPermission",
    "Round5LargeSector",
    "Round5LargeSectorDefinition",
    "render_round5_green_permission_markdown",
    "render_round5_large_sector_framework_markdown",
    "render_round5_next_case_expansion_plan",
    "round5_archetype_rows",
    "round5_case_coverage_by_large_sector",
    "round5_definition",
    "round5_large_sector_for",
    "round5_large_sectors_for",
    "write_round5_large_sector_reports",
]
