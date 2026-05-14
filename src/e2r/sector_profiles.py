"""Sector-aware structural evidence profiles for E2R scoring.

The profiles keep Stage 3 discipline while avoiding one universal contract
gate for every business model. For example, transformer cases usually need
contracts/backlog, while K-food export cases can have visibility from export
channels and repeat consumer demand.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Sequence


class SectorProfile(str, Enum):
    """Domain profiles used for structural visibility scoring."""

    POWER_EQUIPMENT = "POWER_EQUIPMENT"
    DEFENSE = "DEFENSE"
    K_FOOD_EXPORT = "K_FOOD_EXPORT"
    K_BEAUTY_EXPORT = "K_BEAUTY_EXPORT"
    MEMORY_HBM = "MEMORY_HBM"
    CYCLICAL_SHIPPING = "CYCLICAL_SHIPPING"
    BATTERY_OVERHEAT = "BATTERY_OVERHEAT"
    GENERIC = "GENERIC"


_PROFILE_IDS: dict[SectorProfile, int] = {
    SectorProfile.GENERIC: 0,
    SectorProfile.POWER_EQUIPMENT: 1,
    SectorProfile.DEFENSE: 2,
    SectorProfile.K_FOOD_EXPORT: 3,
    SectorProfile.K_BEAUTY_EXPORT: 4,
    SectorProfile.MEMORY_HBM: 5,
    SectorProfile.CYCLICAL_SHIPPING: 6,
    SectorProfile.BATTERY_OVERHEAT: 7,
}
_ID_PROFILES = {value: key for key, value in _PROFILE_IDS.items()}


@dataclass(frozen=True)
class SectorProfileDefinition:
    """Evidence preferences for one sector profile."""

    profile: SectorProfile
    preferred_visibility_fields: tuple[str, ...]
    preferred_bottleneck_fields: tuple[str, ...]
    preferred_pricing_fields: tuple[str, ...]
    stage3_green_required_evidence_families: tuple[str, ...]
    red_team_risk_fields: tuple[str, ...]
    contract_required_for_green: bool = False


PROFILE_DEFINITIONS: Mapping[SectorProfile, SectorProfileDefinition] = {
    SectorProfile.POWER_EQUIPMENT: SectorProfileDefinition(
        profile=SectorProfile.POWER_EQUIPMENT,
        preferred_visibility_fields=(
            "contract_amount_to_prior_sales",
            "contract_duration_months",
            "order_backlog_to_sales",
            "record_backlog",
            "lead_time_extended",
            "capa_constraint",
        ),
        preferred_bottleneck_fields=(
            "lead_time_months",
            "capacity_constraint",
            "capa_shortage",
            "transformer_supply_shortage",
        ),
        preferred_pricing_fields=("asp_yoy_pct", "pricing_power_mentioned", "pricing_power_confirmed"),
        stage3_green_required_evidence_families=("disclosure", "research_report", "consensus_revision"),
        red_team_risk_fields=("contract_cancelled_or_delayed", "backlog_or_rpo_decline", "asp_decline"),
        contract_required_for_green=True,
    ),
    SectorProfile.DEFENSE: SectorProfileDefinition(
        profile=SectorProfile.DEFENSE,
        preferred_visibility_fields=(
            "order_backlog_to_sales",
            "multi_year_contract",
            "government_customer",
            "export_contract",
            "delivery_schedule",
        ),
        preferred_bottleneck_fields=("capacity_constraint", "delivery_schedule", "capa_constraint"),
        preferred_pricing_fields=("opm_expansion_pctp", "high_margin_mix_improvement"),
        stage3_green_required_evidence_families=("disclosure", "research_report", "consensus_revision"),
        red_team_risk_fields=("delivery_delay", "contract_cancelled_or_delayed", "cost_overrun"),
        contract_required_for_green=True,
    ),
    SectorProfile.K_FOOD_EXPORT: SectorProfileDefinition(
        profile=SectorProfile.K_FOOD_EXPORT,
        preferred_visibility_fields=(
            "export_ratio",
            "export_growth_pct",
            "export_channel_expansion",
            "overseas_channel_expansion",
            "recurring_consumer_demand",
            "opm_expansion_pctp",
        ),
        preferred_bottleneck_fields=("high_margin_mix_improvement", "brand_channel_expansion"),
        preferred_pricing_fields=("asp_yoy_pct", "price_increase_pct", "pricing_power_mentioned"),
        stage3_green_required_evidence_families=("research_report", "consensus_revision", "financial_actual"),
        red_team_risk_fields=("single_product_risk", "trend_fade_risk", "raw_material_cost_risk"),
        contract_required_for_green=False,
    ),
    SectorProfile.K_BEAUTY_EXPORT: SectorProfileDefinition(
        profile=SectorProfile.K_BEAUTY_EXPORT,
        preferred_visibility_fields=(
            "export_growth_pct",
            "platform_distribution_scale",
            "brand_customer_diversification",
            "export_channel_expansion",
            "overseas_channel_expansion",
            "recurring_consumer_demand",
        ),
        preferred_bottleneck_fields=("platform_distribution_scale", "brand_channel_expansion"),
        preferred_pricing_fields=("high_margin_mix_improvement", "pricing_power_mentioned"),
        stage3_green_required_evidence_families=("research_report", "consensus_revision", "financial_actual"),
        red_team_risk_fields=("single_channel_risk", "platform_fee_risk", "inventory_spike"),
        contract_required_for_green=False,
    ),
    SectorProfile.MEMORY_HBM: SectorProfileDefinition(
        profile=SectorProfile.MEMORY_HBM,
        preferred_visibility_fields=(
            "hbm_demand_mentioned",
            "memory_price_increase_mentioned",
            "supply_discipline_mentioned",
            "medium_term_revision_visibility",
            "customer_preorder_or_allocation",
        ),
        preferred_bottleneck_fields=("hbm_capacity_constraint", "advanced_packaging_bottleneck", "capa_constraint"),
        preferred_pricing_fields=("memory_price_increase_mentioned", "pricing_power_mentioned", "asp_yoy_pct"),
        stage3_green_required_evidence_families=("research_report", "consensus_revision", "financial_actual"),
        red_team_risk_fields=("memory_price_decline", "customer_capex_decline", "supply_glut"),
        contract_required_for_green=False,
    ),
    SectorProfile.CYCLICAL_SHIPPING: SectorProfileDefinition(
        profile=SectorProfile.CYCLICAL_SHIPPING,
        preferred_visibility_fields=("freight_rate_increase", "contract_rate", "capacity_discipline"),
        preferred_bottleneck_fields=("vessel_shortage", "port_congestion"),
        preferred_pricing_fields=("freight_rate_increase",),
        stage3_green_required_evidence_families=("research_report", "financial_actual", "news"),
        red_team_risk_fields=("freight_rate_decline", "capacity_addition", "one_off_shortage"),
        contract_required_for_green=False,
    ),
    SectorProfile.BATTERY_OVERHEAT: SectorProfileDefinition(
        profile=SectorProfile.BATTERY_OVERHEAT,
        preferred_visibility_fields=("contract_amount_to_prior_sales", "order_backlog_to_sales"),
        preferred_bottleneck_fields=("raw_material_bottleneck",),
        preferred_pricing_fields=("asp_yoy_pct",),
        stage3_green_required_evidence_families=("disclosure", "research_report", "consensus_revision"),
        red_team_risk_fields=("theme_overheat_score", "valuation_overheat", "customer_capex_decline"),
        contract_required_for_green=True,
    ),
    SectorProfile.GENERIC: SectorProfileDefinition(
        profile=SectorProfile.GENERIC,
        preferred_visibility_fields=("contract_quality", "backlog_rpo_visibility", "medium_term_revision_visibility"),
        preferred_bottleneck_fields=("capa_constraint", "asp_pricing_power", "structural_shortage"),
        preferred_pricing_fields=("asp_yoy_pct", "pricing_power_mentioned"),
        stage3_green_required_evidence_families=("research_report", "consensus_revision", "disclosure"),
        red_team_risk_fields=("one_off_shortage", "valuation_overheat", "contract_cancelled_or_delayed"),
        contract_required_for_green=False,
    ),
}


def profile_id(profile: SectorProfile) -> float:
    """Return numeric ID safe for ``ScoreSnapshot.diagnostic_scores``."""

    return float(_PROFILE_IDS[profile])


def profile_from_id(value: float | int | None) -> SectorProfile:
    """Decode numeric profile ID stored in diagnostics."""

    if value is None:
        return SectorProfile.GENERIC
    return _ID_PROFILES.get(int(value), SectorProfile.GENERIC)


def infer_sector_profile(
    *,
    symbol: str | None = None,
    company_name: str | None = None,
    sector_custom: str | None = None,
    text: str | None = None,
    parsed_fields: Mapping[str, Any] | None = None,
) -> SectorProfile:
    """Infer sector profile from metadata and explicit evidence text.

    This function uses only company/source context available to the pipeline.
    Benchmark labels are intentionally not imported or consulted.
    """

    del symbol  # symbol-specific benchmark lookups are deliberately avoided.
    parsed_fields = parsed_fields or {}
    if (
        any(key in parsed_fields for key in ("lead_time_months", "lead_time_extended", "capa_utilization_pct"))
        and any(key in parsed_fields for key in ("order_backlog_to_sales", "rpo_to_sales", "backlog_to_sales"))
    ):
        return SectorProfile.POWER_EQUIPMENT
    haystack = " ".join(
        str(part or "")
        for part in (
            company_name,
            sector_custom,
            text,
            " ".join(str(key) for key, value in parsed_fields.items() if bool(value)),
        )
    ).lower()

    if any(token in haystack for token in ("hbm", "메모리", "dram", "d램", "nand", "낸드", "반도체", "advanced packaging")):
        return SectorProfile.MEMORY_HBM
    if any(token in haystack for token in ("방산", "방위", "k9", "천무", "폴란드", "정부 고객", "government customer")):
        return SectorProfile.DEFENSE
    if any(token in haystack for token in ("변압기", "전력기기", "초고압", "전선", "케이블", "transformer", "power equipment")):
        return SectorProfile.POWER_EQUIPMENT
    if any(token in haystack for token in ("삼양식품", "불닭", "라면", "식품", "k-food", "k푸드", "k-푸드")):
        return SectorProfile.K_FOOD_EXPORT
    if any(token in haystack for token in ("실리콘투", "화장품", "뷰티", "k-beauty", "k뷰티", "k-뷰티", "beauty")):
        return SectorProfile.K_BEAUTY_EXPORT
    if any(token in haystack for token in ("해운", "운임", "scfi", "hmm", "shipping")):
        return SectorProfile.CYCLICAL_SHIPPING
    if any(token in haystack for token in ("2차전지", "배터리", "양극재", "에코프로", "battery")):
        return SectorProfile.BATTERY_OVERHEAT
    return SectorProfile.GENERIC


def definition_for(profile: SectorProfile) -> SectorProfileDefinition:
    """Return profile definition."""

    return PROFILE_DEFINITIONS[profile]


def profile_name_from_diagnostic(value: float | int | None) -> str:
    """Return a stable profile name from a numeric diagnostic value."""

    return profile_from_id(value).value


def field_presence_score(parsed_fields: Mapping[str, Any], fields: Sequence[str], *, points_each: float = 20.0) -> float:
    """Score bounded qualitative field presence."""

    score = 0.0
    for key in fields:
        value = parsed_fields.get(key)
        if value not in (None, "", False, 0):
            score += points_each
    return min(100.0, score)


__all__ = [
    "PROFILE_DEFINITIONS",
    "SectorProfile",
    "SectorProfileDefinition",
    "definition_for",
    "field_presence_score",
    "infer_sector_profile",
    "profile_from_id",
    "profile_id",
    "profile_name_from_diagnostic",
]
