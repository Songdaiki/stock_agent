"""Round-3 E2R extension archetype matrix.

This module captures the analyst's third round of sector/archetype research as
calibration material. It is intentionally separate from production scoring.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import COUNTEREXAMPLE_GROUPS, POSITIVE_GROUPS, E2RArchetype
from e2r.sector.case_library import E2RCaseRecord, load_case_library
from e2r.sector.research_framework import round1_core_for


ROUND3_SOURCE_ROUND_PATH = "docs/round/round_03.md"


class Round3StagePosture(str, Enum):
    """Report-facing posture before production scoring changes."""

    GREEN_ELIGIBLE = "GREEN_ELIGIBLE"
    YELLOW_WATCH = "YELLOW_WATCH"
    RED_4B_GUARDRAIL = "RED_4B_GUARDRAIL"


@dataclass(frozen=True)
class Round3ExtensionEntry:
    """Round-3 lifecycle guidance for one core or extension archetype."""

    archetype: E2RArchetype
    stage_posture: Round3StagePosture
    priority_rank: int
    structure: str
    must_have_fields: tuple[str, ...]
    red_flag_fields: tuple[str, ...]
    example_cases: tuple[str, ...]
    green_policy: str
    notes: str

    @property
    def green_restricted(self) -> bool:
        return self.stage_posture != Round3StagePosture.GREEN_ELIGIBLE


def _entry(
    archetype: E2RArchetype,
    *,
    stage_posture: Round3StagePosture,
    priority_rank: int,
    structure: str,
    must_have_fields: tuple[str, ...],
    red_flag_fields: tuple[str, ...],
    example_cases: tuple[str, ...] = (),
    green_policy: str,
    notes: str = "",
) -> Round3ExtensionEntry:
    return Round3ExtensionEntry(
        archetype=archetype,
        stage_posture=stage_posture,
        priority_rank=priority_rank,
        structure=structure,
        must_have_fields=must_have_fields,
        red_flag_fields=red_flag_fields,
        example_cases=example_cases,
        green_policy=green_policy,
        notes=notes,
    )


ROUND3_STAGE_POSTURE_GROUPS: Mapping[Round3StagePosture, tuple[E2RArchetype, ...]] = {
    Round3StagePosture.GREEN_ELIGIBLE: (
        E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,
        E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,
        E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG,
        E2RArchetype.EXPORT_RECURRING_CONSUMER,
        E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,
        E2RArchetype.MEMORY_HBM_CAPACITY,
        E2RArchetype.SEMI_EQUIPMENT_CAPEX,
        E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT,
        E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
        E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE,
        E2RArchetype.TURNAROUND_COST_RESTRUCTURING,
        E2RArchetype.CDMO_HEALTHCARE_CONTRACT,
    ),
    Round3StagePosture.YELLOW_WATCH: (
        E2RArchetype.ROBOTICS_FACTORY_AUTOMATION,
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        E2RArchetype.GAME_CONTENT_IP,
        E2RArchetype.AUTO_MOBILITY_COMPONENTS,
        E2RArchetype.AUTO_MOBILITY_COMPLETED_VEHICLE,
        E2RArchetype.UTILITIES_REGULATED_TARIFF,
        E2RArchetype.NUCLEAR_SMR_GRID_POLICY,
        E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE,
        E2RArchetype.VALUE_UP_SHAREHOLDER_RETURN,
        E2RArchetype.RARE_METALS_STRATEGIC_MATERIALS,
        E2RArchetype.TRAVEL_LEISURE_REOPENING,
        E2RArchetype.BIOTECH_ROYALTY_COMMERCIALIZATION,
        E2RArchetype.EDUCATION_SPECIALTY_SERVICES,
        E2RArchetype.RETAIL_DOMESTIC_CONSUMER,
    ),
    Round3StagePosture.RED_4B_GUARDRAIL: (
        E2RArchetype.SHIPPING_FREIGHT_CYCLE,
        E2RArchetype.COMMODITY_SPREAD,
        E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT,
        E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT,
        E2RArchetype.BIOTECH_REGULATORY,
        E2RArchetype.BIOTECH_PRE_REVENUE_REGULATORY,
        E2RArchetype.ONE_OFF_EVENT_DEMAND,
        E2RArchetype.THEME_VALUATION_OVERHEAT,
        E2RArchetype.GENERIC_UNCLASSIFIED,
    ),
}


ROUND3_PRIORITY_ARCHETYPES = (
    E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,
    E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,
    E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG,
    E2RArchetype.EXPORT_RECURRING_CONSUMER,
    E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,
    E2RArchetype.MEMORY_HBM_CAPACITY,
    E2RArchetype.SEMI_EQUIPMENT_CAPEX,
    E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
    E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT,
    E2RArchetype.THEME_VALUATION_OVERHEAT,
    E2RArchetype.ONE_OFF_EVENT_DEMAND,
    E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE,
    E2RArchetype.ROBOTICS_FACTORY_AUTOMATION,
    E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
    E2RArchetype.GAME_CONTENT_IP,
    E2RArchetype.SHIPPING_FREIGHT_CYCLE,
    E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT,
    E2RArchetype.UTILITIES_REGULATED_TARIFF,
    E2RArchetype.NUCLEAR_SMR_GRID_POLICY,
    E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE,
    E2RArchetype.TRAVEL_LEISURE_REOPENING,
    E2RArchetype.BIOTECH_REGULATORY,
    E2RArchetype.RARE_METALS_STRATEGIC_MATERIALS,
)


ROUND3_CASE_RECORD_REQUIRED_FIELDS = (
    "case_id",
    "symbol",
    "company_name",
    "market",
    "archetype",
    "case_type",
    "stage1_date",
    "stage2_date",
    "stage3_date",
    "stage4b_date",
    "stage4c_date",
    "peak_date",
    "stage1_evidence",
    "stage2_evidence",
    "stage3_evidence",
    "stage4b_evidence",
    "stage4c_evidence",
    "price_pattern",
    "must_have_fields",
    "red_flag_fields",
    "score_weight_hint",
)


ROUND3_EXTENSION_MATRIX: Mapping[E2RArchetype, Round3ExtensionEntry] = {
    E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE: _entry(
        E2RArchetype.AI_DATA_CENTER_INFRASTRUCTURE,
        stage_posture=Round3StagePosture.GREEN_ELIGIBLE,
        priority_rank=12,
        structure="AI 데이터센터 증설 -> 전력/냉각/서버/네트워크 병목 -> 다년 CAPEX -> 수주잔고와 EPS 상향",
        must_have_fields=("confirmed_orders", "customer_capex_visibility", "op_eps_revision", "capacity_bottleneck"),
        red_flag_fields=("ai_capex_cut", "data_center_delay", "theme_without_revenue"),
        example_cases=("HD현대일렉트릭/효성중공업 전력망", "이수페타시스 AI 서버 PCB"),
        green_policy="Green possible only with confirmed order/revenue exposure, not AI keyword exposure.",
        notes="Round 3 promotes this from a mere extension candidate to a high-priority calibration bucket.",
    ),
    E2RArchetype.NUCLEAR_SMR_GRID_POLICY: _entry(
        E2RArchetype.NUCLEAR_SMR_GRID_POLICY,
        stage_posture=Round3StagePosture.YELLOW_WATCH,
        priority_rank=19,
        structure="정책/수출 수주 -> project financing/기자재 매출화 -> 규제·소송 리스크 확인",
        must_have_fields=("actual_contract_or_loi", "project_financing", "revenue_conversion_path"),
        red_flag_fields=("legal_delay", "policy_reversal", "cost_overrun"),
        example_cases=("두산에너빌리티", "체코 원전 정책계약", "원전 법적 지연"),
        green_policy="Watch by default; Green requires binding contract economics and low legal/policy risk.",
    ),
    E2RArchetype.TRAVEL_LEISURE_REOPENING: _entry(
        E2RArchetype.TRAVEL_LEISURE_REOPENING,
        stage_posture=Round3StagePosture.YELLOW_WATCH,
        priority_rank=21,
        structure="출입국/관광 회복 -> 고정비 레버리지 -> OP/EPS 상향, but cycle/policy risk remains",
        must_have_fields=("visitor_recovery", "op_eps_revision", "fixed_cost_leverage", "customer_mix"),
        red_flag_fields=("oil_or_fx_shock", "china_tourism_dependency", "demand_slowdown"),
        example_cases=("대한항공 리오프닝", "면세 중국 관광 의존"),
        green_policy="Normally Watch/Yellow; Green needs repeat visitor growth and low China/oil/FX dependence.",
    ),
    E2RArchetype.RARE_METALS_STRATEGIC_MATERIALS: _entry(
        E2RArchetype.RARE_METALS_STRATEGIC_MATERIALS,
        stage_posture=Round3StagePosture.YELLOW_WATCH,
        priority_rank=23,
        structure="제련마진/전략금속 공급망/거버넌스 이벤트가 섞이는 소재 archetype",
        must_have_fields=("smelting_margin", "strategic_supply_chain", "fcf_or_governance_improvement"),
        red_flag_fields=("pure_metal_price_rally", "event_premium_only", "governance_dispute_drag"),
        example_cases=("Korea Zinc governance battle", "순수 금속가격 상승 반례"),
        green_policy="Watch by default; event premium alone is not structural Green.",
    ),
    E2RArchetype.ROBOTICS_FACTORY_AUTOMATION: _entry(
        E2RArchetype.ROBOTICS_FACTORY_AUTOMATION,
        stage_posture=Round3StagePosture.YELLOW_WATCH,
        priority_rank=13,
        structure="테마 기대 -> 실제 고객사 도입 -> 수주/매출 전환 -> 반복 서비스/SW 매출",
        must_have_fields=("customer_adoption", "revenue_conversion", "repeat_service_or_consumables", "gross_margin_improvement"),
        red_flag_fields=("theme_only_mou", "no_revenue", "cash_flow_deterioration"),
        example_cases=("Rainbow Robotics", "Doosan Robotics", "무실적 로봇 테마주"),
        green_policy="Green very restricted until repeat revenue and OPM evidence are visible.",
    ),
    E2RArchetype.PLATFORM_SOFTWARE_INTERNET: _entry(
        E2RArchetype.PLATFORM_SOFTWARE_INTERNET,
        stage_posture=Round3StagePosture.YELLOW_WATCH,
        priority_rank=14,
        structure="MAU/traffic -> ARPU/take rate -> 비용 효율화 -> OPM leverage",
        must_have_fields=("arpu_or_take_rate_up", "opm_improvement", "recurring_revenue", "fy1_fy2_op_revision"),
        red_flag_fields=("mau_without_monetization", "regulation", "ai_cost_overrun"),
        example_cases=("NAVER", "Kakao turnaround", "더존비즈온"),
        green_policy="MAU alone cannot create Green; monetization and margin leverage are required.",
    ),
    E2RArchetype.GAME_CONTENT_IP: _entry(
        E2RArchetype.GAME_CONTENT_IP,
        stage_posture=Round3StagePosture.YELLOW_WATCH,
        priority_rank=15,
        structure="IP/신작/팬덤 -> 글로벌 매출 -> 반복 monetization -> OPM leverage",
        must_have_fields=("actual_revenue_conversion", "ip_repeatability", "global_monetization", "op_eps_revision"),
        red_flag_fields=("new_game_hype_only", "single_ip_dependence", "contract_or_scandal_risk"),
        example_cases=("Krafton", "Shift Up", "HYBE/JYP/SM", "신작 기대만 있는 게임주"),
        green_policy="Green restricted unless IP portfolio and repeat monetization are proven.",
    ),
    E2RArchetype.RETAIL_DOMESTIC_CONSUMER: _entry(
        E2RArchetype.RETAIL_DOMESTIC_CONSUMER,
        stage_posture=Round3StagePosture.YELLOW_WATCH,
        priority_rank=24,
        structure="소비 회복 -> 점포효율/객단가/비용 레버리지 -> OPM 개선",
        must_have_fields=("same_store_sales", "opm_improvement", "inventory_normalization", "high_margin_mix"),
        red_flag_fields=("inventory_increase", "online_competition", "rent_or_wage_pressure"),
        example_cases=("BGF리테일/CU", "GS리테일/GS25", "단기 소비 회복 테마"),
        green_policy="Watch by default; Green requires structural store efficiency and FCF improvement.",
    ),
    E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT: _entry(
        E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT,
        stage_posture=Round3StagePosture.RED_4B_GUARDRAIL,
        priority_rank=17,
        structure="수주/분양보다 PF·현금흐름·원가율이 먼저인 credit-sensitive archetype",
        must_have_fields=("cash_flow_improvement", "cost_ratio_stable", "debt_reduction", "pf_risk_low"),
        red_flag_fields=("pf_loss", "unsold_inventory", "liquidity_stress", "credit_rating_downgrade"),
        example_cases=("PF 리스크 해소형 건설사", "Taeyoung E&C류 PF 문제"),
        green_policy="Green very restricted; order headline cannot override PF/cash-flow risk.",
    ),
    E2RArchetype.UTILITIES_REGULATED_TARIFF: _entry(
        E2RArchetype.UTILITIES_REGULATED_TARIFF,
        stage_posture=Round3StagePosture.YELLOW_WATCH,
        priority_rank=18,
        structure="정책·요금·원가 -> EPS 턴어라운드, but regulation risk remains",
        must_have_fields=("tariff_or_cost_improvement", "cash_flow_improvement", "debt_normalization"),
        red_flag_fields=("tariff_freeze", "policy_reversal", "debt_burden"),
        example_cases=("KEPCO", "한국가스공사"),
        green_policy="Watch by default; Green needs durable cost pass-through regime change.",
    ),
    E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE: _entry(
        E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE,
        stage_posture=Round3StagePosture.YELLOW_WATCH,
        priority_rank=20,
        structure="NAV discount -> 자사주/소각/배당/지배구조 개선 -> Korea discount 해소",
        must_have_fields=("actual_cancellation_or_return", "nav_discount_catalyst", "governance_execution"),
        red_flag_fields=("buyback_without_cancel", "subsidiary_value_impairment", "event_premium_only"),
        example_cases=("SK스퀘어", "삼성물산", "Korea Zinc governance battle"),
        green_policy="Watch until capital return is executed and backed by FCF/NAV improvement.",
    ),
    E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET: _entry(
        E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET,
        stage_posture=Round3StagePosture.GREEN_ELIGIBLE,
        priority_rank=8,
        structure="ROE 지속성 + PBR-ROE gap + 자본비율 + 주주환원",
        must_have_fields=("roe_improvement", "cet1_or_capital_ratio_stable", "credit_cost_stable", "capital_return_execution"),
        red_flag_fields=("pf_credit_cost", "capital_ratio_deterioration", "roe_decline"),
        example_cases=("KB금융", "신한지주", "메리츠금융", "단순 저PBR 지방은행"),
        green_policy="Green possible only with ROE/PBR and executed capital return, not low PBR alone.",
    ),
    E2RArchetype.BIOTECH_REGULATORY: _entry(
        E2RArchetype.BIOTECH_REGULATORY,
        stage_posture=Round3StagePosture.RED_4B_GUARDRAIL,
        priority_rank=22,
        structure="임상/허가/기술이전 -> 매출화/로열티 전환 여부가 핵심",
        must_have_fields=("milestone_payment", "commercialization_path", "cash_runway"),
        red_flag_fields=("clinical_failure", "approval_delay", "cb_or_rights_dilution"),
        example_cases=("알테오젠", "유한양행", "임상 뉴스만 있는 바이오"),
        green_policy="Pre-revenue clinical stories are Green-blocked; royalty or revenue conversion is required.",
    ),
    E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT: _entry(
        E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT,
        stage_posture=Round3StagePosture.GREEN_ELIGIBLE,
        priority_rank=9,
        structure="의료/미용기기 수출 -> 소모품/반복 매출 -> OPM/ROE",
        must_have_fields=("export_country_expansion", "consumable_or_repeat_revenue", "opm_roe", "fy1_fy2_eps_revision"),
        red_flag_fields=("approval_delay", "competition_intensifies", "asp_decline"),
        example_cases=("Classys", "파마리서치", "휴젤", "원텍"),
        green_policy="Green possible with export channel plus recurring consumable/service revenue.",
    ),
}


def stage_posture_for(archetype: E2RArchetype | str) -> Round3StagePosture:
    item = _archetype(archetype)
    if item in ROUND3_EXTENSION_MATRIX:
        return ROUND3_EXTENSION_MATRIX[item].stage_posture
    for posture, archetypes in ROUND3_STAGE_POSTURE_GROUPS.items():
        if item in archetypes:
            return posture
    return Round3StagePosture.RED_4B_GUARDRAIL


def round3_entry(archetype: E2RArchetype | str) -> Round3ExtensionEntry:
    item = _archetype(archetype)
    if item in ROUND3_EXTENSION_MATRIX:
        return ROUND3_EXTENSION_MATRIX[item]
    core = round1_core_for(item)
    posture = stage_posture_for(core)
    priority_rank = ROUND3_PRIORITY_ARCHETYPES.index(item) + 1 if item in ROUND3_PRIORITY_ARCHETYPES else 999
    return _entry(
        item,
        stage_posture=posture,
        priority_rank=priority_rank,
        structure=f"Falls back to Round-1 core archetype {core.value}.",
        must_have_fields=("multi_source_evidence", "eps_fcf_support"),
        red_flag_fields=("single_source_story", "theme_only"),
        green_policy="Fallback entry; assign a more specific archetype before allowing Green.",
    )


def round3_case_coverage(records: Iterable[E2RCaseRecord]) -> tuple[dict[str, object], ...]:
    rows = tuple(records)
    output: list[dict[str, object]] = []
    for archetype in _round3_report_archetypes():
        direct_records = tuple(record for record in rows if record.primary_archetype == archetype)
        positive = tuple(record for record in direct_records if record.case_type in POSITIVE_GROUPS)
        counter = tuple(record for record in direct_records if record.case_type in COUNTEREXAMPLE_GROUPS)
        entry = round3_entry(archetype)
        status = "covered_2x2" if len(positive) >= 2 and len(counter) >= 2 else "needs_more_cases"
        if entry.stage_posture == Round3StagePosture.RED_4B_GUARDRAIL and len(counter) >= 2:
            status = "guardrail_counterexamples_present"
        output.append(
            {
                "priority_rank": entry.priority_rank,
                "archetype": archetype.value,
                "round1_core": round1_core_for(archetype).value,
                "stage_posture": entry.stage_posture.value,
                "positive_count": len(positive),
                "counterexample_count": len(counter),
                "status": status,
                "must_have_fields": entry.must_have_fields,
                "red_flag_fields": entry.red_flag_fields,
            }
        )
    return tuple(sorted(output, key=lambda row: (int(row["priority_rank"]), str(row["archetype"]))))


def write_round3_extension_reports(
    *,
    case_path: str | Path = "data/e2r_case_library/cases_v02.jsonl",
    output_directory: str | Path = "output/e2r_round3_extension_matrix",
) -> dict[str, Path]:
    records = load_case_library(case_path)
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    extension_plan = output / "round3_extension_archetype_plan.md"
    posture_csv = output / "round3_stage_posture_matrix.csv"
    field_contract = output / "round3_case_record_field_contract.md"
    coverage_md = output / "round3_case_coverage_summary.md"
    extension_plan.write_text(render_round3_extension_plan_markdown(records), encoding="utf-8")
    _write_stage_posture_csv(posture_csv, records)
    field_contract.write_text(render_case_record_field_contract_markdown(), encoding="utf-8")
    coverage_md.write_text(render_round3_case_coverage_markdown(records), encoding="utf-8")
    return {
        "extension_plan": extension_plan,
        "stage_posture_matrix": posture_csv,
        "case_record_field_contract": field_contract,
        "case_coverage_summary": coverage_md,
    }


def render_round3_extension_plan_markdown(records: Iterable[E2RCaseRecord]) -> str:
    coverage = {row["archetype"]: row for row in round3_case_coverage(records)}
    lines = [
        "# Round-3 Extension Archetype Matrix",
        "",
        f"Source round: `{ROUND3_SOURCE_ROUND_PATH}`",
        "",
        "This is calibration material. It does not change production scoring.",
        "",
        "## Stage Posture Levels",
        "",
        "- `GREEN_ELIGIBLE`: Green can exist later, but only with strict cross-evidence.",
        "- `YELLOW_WATCH`: useful candidates, but Green is exceptional.",
        "- `RED_4B_GUARDRAIL`: mainly used to prevent unsafe Green or detect 4B/4C.",
        "",
        "## Priority Queue",
        "",
        "| rank | archetype | posture | direct positives | direct counterexamples | status |",
        "|---:|---|---|---:|---:|---|",
    ]
    for archetype in ROUND3_PRIORITY_ARCHETYPES:
        row = coverage.get(archetype.value)
        entry = round3_entry(archetype)
        lines.append(
            f"| {entry.priority_rank} | {archetype.value} | {entry.stage_posture.value} | "
            f"{row['positive_count'] if row else 0} | {row['counterexample_count'] if row else 0} | "
            f"{row['status'] if row else 'needs_more_cases'} |"
        )
    lines.extend(
        [
            "",
            "## Extension Details",
        ]
    )
    for entry in sorted(ROUND3_EXTENSION_MATRIX.values(), key=lambda item: item.priority_rank):
        lines.extend(
            [
                "",
                f"### {entry.archetype.value}",
                f"- posture: {entry.stage_posture.value}",
                f"- structure: {entry.structure}",
                f"- must_have_fields: {', '.join(entry.must_have_fields)}",
                f"- red_flag_fields: {', '.join(entry.red_flag_fields)}",
                f"- example_cases: {', '.join(entry.example_cases) if entry.example_cases else '-'}",
                f"- Green policy: {entry.green_policy}",
            ]
        )
    lines.extend(
        [
            "",
            "## What Not To Change",
            "- Do not change StageClassifier thresholds from this matrix.",
            "- Do not use case records as candidate-generation input.",
            "- Do not treat extension labels as stock-name rules.",
            "- Keep one-off, theme, construction/PF, and pre-revenue biotech Green-restricted.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_case_record_field_contract_markdown() -> str:
    lines = [
        "# Round-3 Case Record Field Contract",
        "",
        "Round 3 asks future case records to be close to JSONL-ready instead of narrative-only.",
        "",
        "## Required Fields",
    ]
    for field_name in ROUND3_CASE_RECORD_REQUIRED_FIELDS:
        lines.append(f"- `{field_name}`")
    lines.extend(
        [
            "",
            "## Example",
            "",
            "A robotics case must include `stage2_evidence` such as actual customer adoption and revenue conversion.",
            "A theme-overheat case must include `red_flag_fields` such as price-only rally or no EPS/FCF support.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round3_case_coverage_markdown(records: Iterable[E2RCaseRecord]) -> str:
    rows = round3_case_coverage(records)
    lines = [
        "# Round-3 Case Coverage Summary",
        "",
        "| rank | archetype | posture | positives | counterexamples | status |",
        "|---:|---|---|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['priority_rank']} | {row['archetype']} | {row['stage_posture']} | "
            f"{row['positive_count']} | {row['counterexample_count']} | {row['status']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "- A `covered_2x2` row can later be used for shadow-score experiments.",
            "- `needs_more_cases` means do not apply score-weight changes.",
            "- Guardrail archetypes can be useful even before positives are complete, because they block unsafe Green.",
        ]
    )
    return "\n".join(lines) + "\n"


def _write_stage_posture_csv(path: Path, records: Iterable[E2RCaseRecord]) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "priority_rank",
                "archetype",
                "round1_core",
                "stage_posture",
                "positive_count",
                "counterexample_count",
                "status",
                "must_have_fields",
                "red_flag_fields",
            ),
        )
        writer.writeheader()
        for row in round3_case_coverage(records):
            writer.writerow(
                {
                    **{key: value for key, value in row.items() if key not in {"must_have_fields", "red_flag_fields"}},
                    "must_have_fields": "|".join(row["must_have_fields"]),
                    "red_flag_fields": "|".join(row["red_flag_fields"]),
                }
            )
    return path


def _round3_report_archetypes() -> tuple[E2RArchetype, ...]:
    seen: set[E2RArchetype] = set()
    ordered: list[E2RArchetype] = []
    for archetype in ROUND3_PRIORITY_ARCHETYPES + tuple(ROUND3_EXTENSION_MATRIX):
        if archetype not in seen:
            seen.add(archetype)
            ordered.append(archetype)
    return tuple(ordered)


def _archetype(value: E2RArchetype | str) -> E2RArchetype:
    if isinstance(value, E2RArchetype):
        return value
    return E2RArchetype(str(value))


__all__ = [
    "ROUND3_CASE_RECORD_REQUIRED_FIELDS",
    "ROUND3_EXTENSION_MATRIX",
    "ROUND3_PRIORITY_ARCHETYPES",
    "ROUND3_SOURCE_ROUND_PATH",
    "ROUND3_STAGE_POSTURE_GROUPS",
    "Round3ExtensionEntry",
    "Round3StagePosture",
    "render_case_record_field_contract_markdown",
    "render_round3_case_coverage_markdown",
    "render_round3_extension_plan_markdown",
    "round3_case_coverage",
    "round3_entry",
    "stage_posture_for",
    "write_round3_extension_reports",
]
