"""Round-9 case record pack audit.

Round 9 checks that the analyst's Round 1-8 synthesis has been converted into
agent-readable case records. It is calibration/report material only and does
not change production scoring.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import COUNTEREXAMPLE_GROUPS, POSITIVE_GROUPS, E2RArchetype
from e2r.sector.case_library import E2RCaseRecord, load_case_library


ROUND9_SOURCE_ROUND_PATH = "docs/round/round_09.md"


@dataclass(frozen=True)
class Round9LargeSector:
    name: str
    role: str
    archetype_labels: tuple[str, ...]


@dataclass(frozen=True)
class Round9ArchetypeView:
    label: str
    canonical_archetypes: tuple[E2RArchetype, ...]
    note: str = ""


@dataclass(frozen=True)
class Round9CasePackAudit:
    case_count: int
    required_case_count: int
    present_required_case_count: int
    missing_case_ids: tuple[str, ...]
    large_sector_count: int
    archetype_view_count: int
    production_scoring_changed: bool = False


ROUND9_LARGE_SECTORS: tuple[Round9LargeSector, ...] = (
    Round9LargeSector("산업재/수주", "전력기기, 방산, 조선, 원전, 산업재", ("CONTRACT_BACKLOG_INDUSTRIAL", "DEFENSE_GOVERNMENT_BACKLOG", "SHIPBUILDING_OFFSHORE_BACKLOG", "NUCLEAR_SMR_GRID_POLICY")),
    Round9LargeSector("AI/반도체/데이터센터", "메모리, HBM, 반도체 장비, PCB, IDC, 냉각, 전력망", ("MEMORY_HBM_CAPACITY", "SEMI_EQUIPMENT_CAPEX", "AI_DATA_CENTER_INFRASTRUCTURE")),
    Round9LargeSector("수출소비재/브랜드", "K푸드, K뷰티, 의료기기, 브랜드 소비재", ("EXPORT_RECURRING_CONSUMER", "K_BEAUTY_EXPORT_DISTRIBUTION", "MEDICAL_DEVICE_HEALTHCARE_EXPORT")),
    Round9LargeSector("금융/자본배분", "은행, 보험, 증권, 지주사, value-up", ("FINANCIAL_SPREAD_BALANCE_SHEET", "VALUE_UP_SHAREHOLDER_RETURN", "HOLDING_RESTRUCTURING_GOVERNANCE")),
    Round9LargeSector("사이클/스프레드", "해운, 정유, 화학, 철강, 원자재", ("SHIPPING_FREIGHT_CYCLE", "COMMODITY_SPREAD", "RARE_METALS_STRATEGIC_MATERIALS", "BATTERY_MATERIALS_CAPEX_OVERHEAT")),
    Round9LargeSector("플랫폼/IP/서비스", "플랫폼, 게임, 콘텐츠, 교육, 특수서비스", ("PLATFORM_SOFTWARE_INTERNET", "GAME_CONTENT_IP", "EDUCATION_SPECIALTY_SERVICES", "ROBOTICS_FACTORY_AUTOMATION")),
    Round9LargeSector("바이오/헬스케어", "pre-revenue biotech, royalty biotech, CDMO, 의료기기", ("BIOTECH_PRE_REVENUE_REGULATORY", "BIOTECH_ROYALTY_COMMERCIALIZATION", "CDMO_HEALTHCARE_CONTRACT", "MEDICAL_DEVICE_HEALTHCARE_EXPORT")),
    Round9LargeSector("내수/리오프닝", "리테일, 면세, 카지노, 항공, 여행", ("RETAIL_DOMESTIC_CONSUMER", "TRAVEL_LEISURE_REOPENING")),
    Round9LargeSector("부동산/신용", "건설, PF, 리츠, 신용위험", ("CONSTRUCTION_REAL_ESTATE_CREDIT", "UTILITIES_REGULATED_TARIFF")),
    Round9LargeSector("테마/일회성/과열", "one-off demand, theme overheat, price-only rally", ("ONE_OFF_EVENT_DEMAND", "THEME_VALUATION_OVERHEAT")),
)


ROUND9_ARCHETYPE_VIEW: tuple[Round9ArchetypeView, ...] = (
    Round9ArchetypeView("CONTRACT_BACKLOG_INDUSTRIAL", (E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,)),
    Round9ArchetypeView("DEFENSE_GOVERNMENT_BACKLOG", (E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,)),
    Round9ArchetypeView("SHIPBUILDING_OFFSHORE_BACKLOG", (E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG,)),
    Round9ArchetypeView("EXPORT_RECURRING_CONSUMER", (E2RArchetype.EXPORT_RECURRING_CONSUMER,)),
    Round9ArchetypeView("K_BEAUTY_EXPORT_DISTRIBUTION", (E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,)),
    Round9ArchetypeView("MEMORY_HBM_CAPACITY", (E2RArchetype.MEMORY_HBM_CAPACITY,)),
    Round9ArchetypeView("SEMI_EQUIPMENT_CAPEX", (E2RArchetype.SEMI_EQUIPMENT_CAPEX,)),
    Round9ArchetypeView("AI_DATA_CENTER_INFRASTRUCTURE", (E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE,)),
    Round9ArchetypeView("NUCLEAR_SMR_GRID_POLICY", (E2RArchetype.NUCLEAR_SMR_GRID_POLICY,)),
    Round9ArchetypeView("BATTERY_MATERIALS_CAPEX_OVERHEAT", (E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT,)),
    Round9ArchetypeView("COMMODITY_SPREAD", (E2RArchetype.COMMODITY_SPREAD,)),
    Round9ArchetypeView("RARE_METALS_STRATEGIC_MATERIALS", (E2RArchetype.RARE_METALS_STRATEGIC_MATERIALS,)),
    Round9ArchetypeView("SHIPPING_FREIGHT_CYCLE", (E2RArchetype.SHIPPING_FREIGHT_CYCLE,)),
    Round9ArchetypeView("AUTO_MOBILITY_COMPLETED_VEHICLE", (E2RArchetype.AUTO_MOBILITY_COMPLETED_VEHICLE,)),
    Round9ArchetypeView("AUTO_MOBILITY_COMPONENTS", (E2RArchetype.AUTO_MOBILITY_COMPONENTS,)),
    Round9ArchetypeView("ROBOTICS_FACTORY_AUTOMATION", (E2RArchetype.ROBOTICS_FACTORY_AUTOMATION,)),
    Round9ArchetypeView("PLATFORM_SOFTWARE_INTERNET", (E2RArchetype.PLATFORM_SOFTWARE_INTERNET,)),
    Round9ArchetypeView("GAME_CONTENT_IP", (E2RArchetype.GAME_CONTENT_IP,)),
    Round9ArchetypeView("FINANCIAL_SPREAD_BALANCE_SHEET", (E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,)),
    Round9ArchetypeView("VALUE_UP_SHAREHOLDER_RETURN", (E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN,)),
    Round9ArchetypeView("HOLDING_RESTRUCTURING_GOVERNANCE", (E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE,)),
    Round9ArchetypeView("TURNAROUND_COST_RESTRUCTURING", (E2RArchetype.TURNAROUND_COST_RESTRUCTURING,)),
    Round9ArchetypeView("BIOTECH_PRE_REVENUE_REGULATORY", (E2RArchetype.BIOTECH_PRE_REVENUE_REGULATORY,)),
    Round9ArchetypeView("BIOTECH_ROYALTY_COMMERCIALIZATION", (E2RArchetype.BIOTECH_ROYALTY_COMMERCIALIZATION,)),
    Round9ArchetypeView("CDMO_HEALTHCARE_CONTRACT", (E2RArchetype.CDMO_HEALTHCARE_CONTRACT,)),
    Round9ArchetypeView("MEDICAL_DEVICE_HEALTHCARE_EXPORT", (E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT,)),
    Round9ArchetypeView("RETAIL_DOMESTIC_CONSUMER", (E2RArchetype.RETAIL_DOMESTIC_CONSUMER,)),
    Round9ArchetypeView("TRAVEL_LEISURE_REOPENING", (E2RArchetype.TRAVEL_LEISURE_REOPENING,)),
    Round9ArchetypeView("CONSTRUCTION_REAL_ESTATE_CREDIT", (E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT,)),
    Round9ArchetypeView("UTILITIES_REGULATED_TARIFF", (E2RArchetype.UTILITIES_REGULATED_TARIFF,)),
    Round9ArchetypeView("EDUCATION_SPECIALTY_SERVICES", (E2RArchetype.EDUCATION_SPECIALTY_SERVICES,)),
    Round9ArchetypeView(
        "ONE_OFF_OR_THEME_RISK",
        (E2RArchetype.ONE_OFF_EVENT_DEMAND, E2RArchetype.THEME_VALUATION_OVERHEAT),
        "Round 9 reporting alias; production enum keeps one-off and theme overheat separate.",
    ),
)


ROUND9_REQUIRED_CASE_IDS = (
    "hd_hyundai_electric_2023",
    "iljin_electric_2023_2024",
    "hyosung_heavy_2023",
    "daehan_cable_like_2026",
    "hanwha_aerospace_2024",
    "defense_theme_no_backlog",
    "hyundai_rotem_k2_export",
    "samsung_heavy_shipbuilding_cycle",
    "shipbuilding_low_margin_backlog",
    "nuclear_czech_policy_contract",
    "nuclear_legal_delay",
    "sk_hynix_hbm_rerating",
    "sk_hynix_hbm_4b_watch",
    "samsung_memory_recovery",
    "simple_dram_rebound",
    "hanmi_semi_hbm_equipment",
    "semi_equipment_customer_capex_cut",
    "ai_dc_power_grid",
    "ai_dc_theme_no_order",
    "esopcb_ai_server",
    "samyang_foods_2024",
    "one_product_fad_consumer",
    "consumer_recall_regulation",
    "silicontwo_2024",
    "apr_kbeauty_device",
    "kbeauty_china_dependency",
    "kbeauty_channel_stuffing",
    "classys_medical_export",
    "single_device_no_consumable",
    "medical_approval_delay",
    "kb_financial_valueup",
    "meritz_financial_return",
    "low_pbr_no_roe_bank",
    "pf_credit_cost_financial",
    "sk_square_valueup",
    "korea_zinc_event_premium",
    "holding_buyback_no_cancel",
    "governance_dispute_no_fcf",
    "hmm_2021_freight_cycle",
    "shipping_overcapacity_4c",
    "refining_spread_recovery",
    "chemical_china_oversupply",
    "ecopro_bm_2023",
    "battery_capa_overbuild",
    "construction_pf_stress",
    "overseas_infra_margin_contract",
    "korean_air_reopening",
    "dutyfree_china_tourism_only",
    "naver_platform_candidate",
    "kakao_governance_risk",
    "douzone_saas_candidate",
    "mau_only_platform",
    "krafton_ip_candidate",
    "new_game_hype_fail",
    "rainbow_robotics_samsung",
    "robot_tam_no_revenue",
    "megastudy_education",
    "education_policy_regulation",
    "samsung_biologics_cdmo",
    "celltrion_biosimilar",
    "cdmo_capacity_underutilization",
    "yuhan_lazertinib",
    "alteogen_royalty",
    "prerevenue_clinical_biotech",
    "biotech_cb_dilution",
    "seegene_2020_red",
    "smci_2024_accounting",
)


ROUND9_PRICE_PATTERN_VALUES = (
    "unknown",
    "straight_rerating",
    "stair_step_rerating",
    "cycle_boom_bust",
    "theme_overheat",
    "accounting_trust_break",
    "governance_trust_break",
    "event_premium",
    "credit_relief_rally",
    "reopening_cycle",
    "policy_contract_delay",
)


def round9_case_pack_audit(records: Iterable[E2RCaseRecord]) -> Round9CasePackAudit:
    record_tuple = tuple(records)
    ids = {record.case_id for record in record_tuple}
    missing = tuple(case_id for case_id in ROUND9_REQUIRED_CASE_IDS if case_id not in ids)
    return Round9CasePackAudit(
        case_count=len(record_tuple),
        required_case_count=len(ROUND9_REQUIRED_CASE_IDS),
        present_required_case_count=len(ROUND9_REQUIRED_CASE_IDS) - len(missing),
        missing_case_ids=missing,
        large_sector_count=len(ROUND9_LARGE_SECTORS),
        archetype_view_count=len(ROUND9_ARCHETYPE_VIEW),
    )


def round9_required_case_rows(records: Iterable[E2RCaseRecord]) -> tuple[dict[str, object], ...]:
    by_id = {record.case_id: record for record in records}
    rows: list[dict[str, object]] = []
    for case_id in ROUND9_REQUIRED_CASE_IDS:
        record = by_id.get(case_id)
        rows.append(
            {
                "case_id": case_id,
                "present": bool(record),
                "company_name": record.company_name if record else "",
                "primary_archetype": record.primary_archetype.value if record else "",
                "case_type": record.case_type if record else "",
                "price_validation_status": record.price_validation.price_validation_status if record else "",
            }
        )
    return tuple(rows)


def round9_archetype_view_coverage(records: Iterable[E2RCaseRecord]) -> tuple[dict[str, object], ...]:
    record_tuple = tuple(records)
    rows: list[dict[str, object]] = []
    for view in ROUND9_ARCHETYPE_VIEW:
        subset = tuple(record for record in record_tuple if record.primary_archetype in view.canonical_archetypes)
        positive = sum(1 for record in subset if record.case_type in POSITIVE_GROUPS)
        counter = sum(1 for record in subset if record.case_type in COUNTEREXAMPLE_GROUPS)
        rows.append(
            {
                "archetype_view": view.label,
                "canonical_archetypes": "|".join(item.value for item in view.canonical_archetypes),
                "case_count": len(subset),
                "positive_or_candidate": positive,
                "counterexample_or_risk": counter,
                "status": "covered_2x2" if positive >= 2 and counter >= 2 else "insufficient_case_coverage",
                "note": view.note,
            }
        )
    return tuple(rows)


def write_round9_case_record_pack_reports(
    *,
    case_path: str | Path = "data/e2r_case_library/cases_v02.jsonl",
    output_directory: str | Path = "output/e2r_round9_case_record_pack",
) -> dict[str, Path]:
    records = load_case_library(case_path)
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "framework": output / "round9_case_record_pack_framework.md",
        "required_case_matrix": output / "round9_required_case_matrix.csv",
        "audit": output / "round9_case_pack_audit.md",
        "archetype_coverage": output / "round9_archetype_view_coverage.csv",
        "schema_contract": output / "round9_case_record_schema_contract.md",
        "next_plan": output / "round9_next_price_alignment_plan.md",
    }
    paths["framework"].write_text(render_round9_framework_markdown(), encoding="utf-8")
    _write_required_case_matrix(records, paths["required_case_matrix"])
    paths["audit"].write_text(render_round9_audit_markdown(records), encoding="utf-8")
    _write_archetype_view_coverage(records, paths["archetype_coverage"])
    paths["schema_contract"].write_text(render_round9_schema_contract_markdown(), encoding="utf-8")
    paths["next_plan"].write_text(render_round9_next_plan_markdown(records), encoding="utf-8")
    return paths


def render_round9_framework_markdown() -> str:
    lines = [
        "# Round-9 Case Record Pack Framework",
        "",
        f"Source round: `{ROUND9_SOURCE_ROUND_PATH}`",
        "",
        "Round 9 confirms that the Round 1-8 synthesis is represented as case records, not production scoring.",
        "",
        "## Large Sectors",
        "",
        "| large_sector | role | archetypes |",
        "|---|---|---:|",
    ]
    for sector in ROUND9_LARGE_SECTORS:
        lines.append(f"| {sector.name} | {sector.role} | {len(sector.archetype_labels)} |")
    lines.extend(
        [
            "",
            "## Archetype View",
            "",
            f"- round9_archetype_view_count: {len(ROUND9_ARCHETYPE_VIEW)}",
            "- `ONE_OFF_OR_THEME_RISK` is a reporting alias only. Production logic keeps one-off and theme-overheat separate.",
            "",
            "## Guardrails",
            "- Do not use case records as candidate-generation input.",
            "- Do not apply score_weight_hint to live scoring yet.",
            "- Do not fabricate missing stage dates or prices.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round9_audit_markdown(records: Iterable[E2RCaseRecord]) -> str:
    audit = round9_case_pack_audit(records)
    lines = [
        "# Round-9 Case Pack Audit",
        "",
        f"- case_count: {audit.case_count}",
        f"- required_case_count: {audit.required_case_count}",
        f"- present_required_case_count: {audit.present_required_case_count}",
        f"- missing_required_case_count: {len(audit.missing_case_ids)}",
        f"- large_sector_count: {audit.large_sector_count}",
        f"- archetype_view_count: {audit.archetype_view_count}",
        f"- production_scoring_changed: {str(audit.production_scoring_changed).lower()}",
        "",
        "## Missing Required Cases",
    ]
    if audit.missing_case_ids:
        lines.extend(f"- {case_id}" for case_id in audit.missing_case_ids)
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Easy Example",
            "",
            "If `hmm_2021_freight_cycle` is present, it still remains a cyclical case. It does not become structural Green just because price and EPS exploded.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round9_schema_contract_markdown() -> str:
    fields = (
        "large_sector",
        "secondary_archetypes",
        "case_type",
        "stage1_evidence",
        "stage2_evidence",
        "stage3_evidence",
        "stage4b_evidence",
        "stage4c_evidence",
        "must_have_fields",
        "red_flag_fields",
        "score_price_alignment",
        "rerating_result",
        "price_pattern",
        "score_weight_hint",
        "green_guardrails",
        "notes",
        "price_validation",
    )
    lines = ["# Round-9 Case Record Schema Contract", "", "## Required/Supported Fields"]
    for field in fields:
        lines.append(f"- `{field}`")
    lines.extend(["", "## Price Pattern Values"])
    for value in ROUND9_PRICE_PATTERN_VALUES:
        lines.append(f"- `{value}`")
    lines.extend(
        [
            "",
            "## Interpretation",
            "- `notes` is calibration text and is not production evidence.",
            "- `governance_trust_break` is a Round-9 reporting pattern for Kakao/SMCI-like trust breaks.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round9_next_plan_markdown(records: Iterable[E2RCaseRecord]) -> str:
    coverage_rows = round9_archetype_view_coverage(records)
    missing_coverage = [row for row in coverage_rows if row["status"] != "covered_2x2"]
    needs_price = sum(1 for record in records if record.price_validation.price_validation_status != "price_filled")
    lines = [
        "# Round-9 Next Price-Alignment Plan",
        "",
        f"- insufficient_archetype_views: {len(missing_coverage)}",
        f"- cases_needing_price_backfill: {needs_price}",
        "",
        "## Priority",
        "1. Fill stage prices, MFE/MAE, peak price, and drawdown for required cases.",
        "2. Classify score_price_alignment after price backfill.",
        "3. Keep one-off, event-premium, cycle, and trust-break cases as guardrails.",
        "",
        "## What Not To Change",
        "- Do not lower Stage 3-Green thresholds.",
        "- Do not use case labels as live candidate evidence.",
        "- Do not treat price-only movement as EPS/FCF rerating.",
    ]
    return "\n".join(lines) + "\n"


def _write_required_case_matrix(records: Iterable[E2RCaseRecord], path: Path) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = ("case_id", "present", "company_name", "primary_archetype", "case_type", "price_validation_status")
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in round9_required_case_rows(records):
            writer.writerow(row)
    return path


def _write_archetype_view_coverage(records: Iterable[E2RCaseRecord], path: Path) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = (
            "archetype_view",
            "canonical_archetypes",
            "case_count",
            "positive_or_candidate",
            "counterexample_or_risk",
            "status",
            "note",
        )
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in round9_archetype_view_coverage(records):
            writer.writerow(row)
    return path


__all__ = [
    "ROUND9_ARCHETYPE_VIEW",
    "ROUND9_LARGE_SECTORS",
    "ROUND9_PRICE_PATTERN_VALUES",
    "ROUND9_REQUIRED_CASE_IDS",
    "ROUND9_SOURCE_ROUND_PATH",
    "Round9ArchetypeView",
    "Round9CasePackAudit",
    "Round9LargeSector",
    "render_round9_audit_markdown",
    "render_round9_framework_markdown",
    "render_round9_next_plan_markdown",
    "render_round9_schema_contract_markdown",
    "round9_archetype_view_coverage",
    "round9_case_pack_audit",
    "round9_required_case_rows",
    "write_round9_case_record_pack_reports",
]
