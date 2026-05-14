"""E2R archetype definitions.

Archetypes describe business-model patterns, not individual stocks. They are
used for taxonomy, case-library coverage, and later score-weight design.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class E2RArchetype(str, Enum):
    """Canonical E2R sector/business archetypes."""

    CONTRACT_BACKLOG_INDUSTRIAL = "CONTRACT_BACKLOG_INDUSTRIAL"
    DEFENSE_GOVERNMENT_BACKLOG = "DEFENSE_GOVERNMENT_BACKLOG"
    SHIPBUILDING_OFFSHORE_BACKLOG = "SHIPBUILDING_OFFSHORE_BACKLOG"
    EXPORT_RECURRING_CONSUMER = "EXPORT_RECURRING_CONSUMER"
    K_BEAUTY_EXPORT_DISTRIBUTION = "K_BEAUTY_EXPORT_DISTRIBUTION"
    MEMORY_HBM_CAPACITY = "MEMORY_HBM_CAPACITY"
    SEMI_EQUIPMENT_CAPEX = "SEMI_EQUIPMENT_CAPEX"
    BATTERY_MATERIALS_CAPEX_OVERHEAT = "BATTERY_MATERIALS_CAPEX_OVERHEAT"
    COMMODITY_SPREAD = "COMMODITY_SPREAD"
    SHIPPING_FREIGHT_CYCLE = "SHIPPING_FREIGHT_CYCLE"
    AUTO_MOBILITY_COMPONENTS = "AUTO_MOBILITY_COMPONENTS"
    ROBOTICS_FACTORY_AUTOMATION = "ROBOTICS_FACTORY_AUTOMATION"
    PLATFORM_SOFTWARE_INTERNET = "PLATFORM_SOFTWARE_INTERNET"
    GAME_CONTENT_IP = "GAME_CONTENT_IP"
    FINANCIAL_SPREAD_BALANCE_SHEET = "FINANCIAL_SPREAD_BALANCE_SHEET"
    BIOTECH_REGULATORY = "BIOTECH_REGULATORY"
    MEDICAL_DEVICE_HEALTHCARE_EXPORT = "MEDICAL_DEVICE_HEALTHCARE_EXPORT"
    RETAIL_DOMESTIC_CONSUMER = "RETAIL_DOMESTIC_CONSUMER"
    CONSTRUCTION_REAL_ESTATE_CREDIT = "CONSTRUCTION_REAL_ESTATE_CREDIT"
    UTILITIES_REGULATED_TARIFF = "UTILITIES_REGULATED_TARIFF"
    HOLDING_RESTRUCTURING_GOVERNANCE = "HOLDING_RESTRUCTURING_GOVERNANCE"
    TURNAROUND_COST_RESTRUCTURING = "TURNAROUND_COST_RESTRUCTURING"
    ONE_OFF_EVENT_DEMAND = "ONE_OFF_EVENT_DEMAND"
    THEME_VALUATION_OVERHEAT = "THEME_VALUATION_OVERHEAT"
    GENERIC_UNCLASSIFIED = "GENERIC_UNCLASSIFIED"


@dataclass(frozen=True)
class ArchetypeDefinition:
    """Lifecycle signals and future score-weight guidance for one archetype."""

    archetype: E2RArchetype
    stage1_radar_signals: tuple[str, ...]
    stage2_candidate_signals: tuple[str, ...]
    stage3_high_conviction_signals: tuple[str, ...]
    stage4a_ongoing_signals: tuple[str, ...]
    stage4b_graduation_overheat_signals: tuple[str, ...]
    stage4c_thesis_break_signals: tuple[str, ...]
    key_evidence_families: tuple[str, ...]
    false_positive_patterns: tuple[str, ...]
    preferred_score_weights: Mapping[str, float]


def _weights(
    *,
    eps_fcf: float,
    visibility: float,
    bottleneck: float,
    mispricing: float,
    valuation: float,
    confidence: float = 5.0,
) -> Mapping[str, float]:
    return {
        "eps_fcf_explosion": eps_fcf,
        "earnings_visibility": visibility,
        "bottleneck_pricing": bottleneck,
        "market_mispricing": mispricing,
        "valuation_rerating": valuation,
        "information_confidence": confidence,
    }


def _generic_definition(archetype: E2RArchetype) -> ArchetypeDefinition:
    return ArchetypeDefinition(
        archetype=archetype,
        stage1_radar_signals=("price/trading value breakout", "sector keyword appears", "company event disclosure"),
        stage2_candidate_signals=("reported OP/EPS acceleration", "research report confirmation", "valuation frame change"),
        stage3_high_conviction_signals=("multi-source evidence", "EPS/FCF bodyweight change", "old-frame mispricing"),
        stage4a_ongoing_signals=("evidence remains intact", "revision path remains positive"),
        stage4b_graduation_overheat_signals=("large rerating return", "crowded positive reports", "revision slowdown"),
        stage4c_thesis_break_signals=("estimate cuts", "margin reversal", "hard disclosure risk"),
        key_evidence_families=("price", "financial_actual", "research_report", "news"),
        false_positive_patterns=("single-source story", "theme-only runup", "no revision support"),
        preferred_score_weights=_weights(eps_fcf=20, visibility=20, bottleneck=15, mispricing=15, valuation=15),
    )


ARCHETYPE_DEFINITIONS: dict[E2RArchetype, ArchetypeDefinition] = {
    archetype: _generic_definition(archetype) for archetype in E2RArchetype
}

ARCHETYPE_DEFINITIONS.update(
    {
        E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL: ArchetypeDefinition(
            archetype=E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL,
            stage1_radar_signals=("supply contract disclosure", "backlog keyword", "price/trading value breakout"),
            stage2_candidate_signals=("contract_amount_to_prior_sales", "contract_duration_months", "backlog_to_sales", "OP/EPS revision"),
            stage3_high_conviction_signals=("multi-year order visibility", "capacity constraint", "ASP/pricing power", "EPS/FCF bodyweight change"),
            stage4a_ongoing_signals=("backlog remains high", "delivery/margin path intact", "revision path remains positive"),
            stage4b_graduation_overheat_signals=("multiple expansion", "revision slowdown", "universally bullish reports"),
            stage4c_thesis_break_signals=("contract cancellation", "backlog decline", "margin/ASP drop"),
            key_evidence_families=("disclosure", "research_report", "consensus_revision", "price"),
            false_positive_patterns=("small one-time contract", "low margin backlog", "valuation already saturated"),
            preferred_score_weights=_weights(eps_fcf=20, visibility=24, bottleneck=22, mispricing=13, valuation=12),
        ),
        E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG: ArchetypeDefinition(
            archetype=E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG,
            stage1_radar_signals=("export defense contract", "government customer disclosure", "backlog keyword"),
            stage2_candidate_signals=("multi-year delivery schedule", "order backlog", "margin recovery", "target/EPS revision"),
            stage3_high_conviction_signals=("government-backed backlog", "export mix improvement", "delivery visibility", "EPS bodyweight change"),
            stage4a_ongoing_signals=("delivery schedule on track", "new orders continue", "margin path intact"),
            stage4b_graduation_overheat_signals=("crowded defense reports", "price outruns revision", "delivery risk ignored"),
            stage4c_thesis_break_signals=("delivery delay", "contract change", "cost overrun", "export approval issue"),
            key_evidence_families=("disclosure", "research_report", "financial_actual", "news"),
            false_positive_patterns=("headline contract without margin", "political delay", "single export customer risk"),
            preferred_score_weights=_weights(eps_fcf=20, visibility=24, bottleneck=17, mispricing=14, valuation=12),
        ),
        E2RArchetype.EXPORT_RECURRING_CONSUMER: ArchetypeDefinition(
            archetype=E2RArchetype.EXPORT_RECURRING_CONSUMER,
            stage1_radar_signals=("export growth", "OPM surprise", "channel expansion"),
            stage2_candidate_signals=("FY1/FY2 EPS/OP revision", "export mix increase", "repeated overseas demand"),
            stage3_high_conviction_signals=("recurring demand", "channel expansion", "OPM leverage", "valuation below new frame"),
            stage4a_ongoing_signals=("sell-through remains strong", "new channels add revenue", "margin remains high"),
            stage4b_graduation_overheat_signals=("peak margin", "crowded reports", "decelerating sell-through"),
            stage4c_thesis_break_signals=("export slowdown", "channel inventory issue", "ASP/margin reversal"),
            key_evidence_families=("research_report", "financial_actual", "consensus_revision", "news"),
            false_positive_patterns=("short-lived product fad", "inventory stuffing", "FX-only margin lift"),
            preferred_score_weights=_weights(eps_fcf=22, visibility=23, bottleneck=14, mispricing=16, valuation=14),
        ),
        E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION: ArchetypeDefinition(
            archetype=E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION,
            stage1_radar_signals=("export growth", "platform/distribution expansion", "OPM/ROE improvement"),
            stage2_candidate_signals=("brand/customer diversification", "FY1/FY2 OP/EPS revision", "repeat orders"),
            stage3_high_conviction_signals=("recurring export channel", "platform scale", "margin leverage", "new valuation frame"),
            stage4a_ongoing_signals=("channel expansion continues", "brand breadth improves", "cash conversion remains healthy"),
            stage4b_graduation_overheat_signals=("single-platform crowding", "margin peak", "inventory risk ignored"),
            stage4c_thesis_break_signals=("export channel slowdown", "inventory spike", "platform fee/margin reversal"),
            key_evidence_families=("research_report", "financial_actual", "news", "consensus_revision"),
            false_positive_patterns=("single brand fad", "channel stuffing", "low-quality receivables growth"),
            preferred_score_weights=_weights(eps_fcf=22, visibility=23, bottleneck=13, mispricing=16, valuation=14),
        ),
        E2RArchetype.MEMORY_HBM_CAPACITY: ArchetypeDefinition(
            archetype=E2RArchetype.MEMORY_HBM_CAPACITY,
            stage1_radar_signals=("HBM demand", "memory price increase", "earnings turnaround"),
            stage2_candidate_signals=("consensus revision", "DRAM/NAND/HBM pricing", "supply discipline"),
            stage3_high_conviction_signals=("multi-year EPS path", "HBM/capacity bottleneck", "old cyclical discount removal"),
            stage4a_ongoing_signals=("prices and revisions remain positive", "capacity allocation holds", "customer demand intact"),
            stage4b_graduation_overheat_signals=("full rerating", "revision slowdown", "capex overbuild signs"),
            stage4c_thesis_break_signals=("customer capex collapse", "supply glut", "memory price decline"),
            key_evidence_families=("financial_actual", "research_report", "consensus_revision", "news"),
            false_positive_patterns=("pure cyclical bounce", "price-only memory rally", "capex overbuild ignored"),
            preferred_score_weights=_weights(eps_fcf=24, visibility=21, bottleneck=19, mispricing=15, valuation=12),
        ),
        E2RArchetype.ONE_OFF_EVENT_DEMAND: ArchetypeDefinition(
            archetype=E2RArchetype.ONE_OFF_EVENT_DEMAND,
            stage1_radar_signals=("explosive temporary demand", "one-time supply shock", "pandemic/event keyword"),
            stage2_candidate_signals=("short-term EPS spike", "news volume spike", "price breakout"),
            stage3_high_conviction_signals=("normally not Green unless recurrence is proven",),
            stage4a_ongoing_signals=("temporary demand persists longer than expected",),
            stage4b_graduation_overheat_signals=("peak margins", "consensus extrapolates one-off demand"),
            stage4c_thesis_break_signals=("normalization", "ASP collapse", "demand cliff"),
            key_evidence_families=("news", "financial_actual", "research_report"),
            false_positive_patterns=("one-off demand treated as structural", "temporary margin annualized"),
            preferred_score_weights=_weights(eps_fcf=20, visibility=8, bottleneck=8, mispricing=8, valuation=8),
        ),
        E2RArchetype.THEME_VALUATION_OVERHEAT: ArchetypeDefinition(
            archetype=E2RArchetype.THEME_VALUATION_OVERHEAT,
            stage1_radar_signals=("theme keyword spike", "price-only breakout", "retail/crowding signal"),
            stage2_candidate_signals=("requires real estimates or official evidence; otherwise remains watch"),
            stage3_high_conviction_signals=("normally blocked without evidence-backed EPS/FCF path",),
            stage4a_ongoing_signals=("theme evidence remains but valuation is watched"),
            stage4b_graduation_overheat_signals=("return multiple excessive", "reports universally bullish", "valuation saturated"),
            stage4c_thesis_break_signals=("funding/dilution", "estimate cuts", "theme unwind"),
            key_evidence_families=("price", "news", "research_report"),
            false_positive_patterns=("story-only rerating", "no cash flow", "dilution ignored"),
            preferred_score_weights=_weights(eps_fcf=18, visibility=8, bottleneck=8, mispricing=7, valuation=5),
        ),
    }
)


def archetype_definition(archetype: E2RArchetype | str) -> ArchetypeDefinition:
    """Return the definition for an archetype."""

    if not isinstance(archetype, E2RArchetype):
        archetype = E2RArchetype(str(archetype))
    return ARCHETYPE_DEFINITIONS[archetype]


def all_archetype_definitions() -> tuple[ArchetypeDefinition, ...]:
    """Return definitions for all archetypes."""

    return tuple(ARCHETYPE_DEFINITIONS[item] for item in E2RArchetype)


POSITIVE_GROUPS = frozenset({"structural_success", "cyclical_success"})
COUNTEREXAMPLE_GROUPS = frozenset({"one_off", "boom_bust", "overheat", "failed_rerating"})


__all__ = [
    "ARCHETYPE_DEFINITIONS",
    "COUNTEREXAMPLE_GROUPS",
    "POSITIVE_GROUPS",
    "ArchetypeDefinition",
    "E2RArchetype",
    "all_archetype_definitions",
    "archetype_definition",
]
