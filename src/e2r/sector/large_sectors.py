"""Round-18 large sector definitions for theme coverage v0.5.

This module is taxonomy/report material only. It is not imported by production
scoring or staging logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class LargeSectorV05(str, Enum):
    INDUSTRIAL_ORDERS_INFRA = "산업재·수주·인프라"
    AI_SEMICONDUCTOR_ELECTRONICS = "AI·반도체·전자부품"
    BATTERY_EV_GREEN = "2차전지·전기차·친환경"
    MATERIALS_SPREAD_STRATEGIC = "소재·스프레드·전략자원"
    CONSUMER_RETAIL_BRAND = "소비재·유통·브랜드"
    FINANCIAL_CAPITAL_DIGITAL = "금융·자본배분·디지털금융"
    BIOTECH_HEALTHCARE_DEVICE = "바이오·헬스케어·의료기기"
    PLATFORM_CONTENT_SW_SECURITY = "플랫폼·콘텐츠·SW·보안"
    MOBILITY_TRANSPORT_LEISURE = "모빌리티·운송·레저"
    CONSTRUCTION_REAL_ESTATE_MATERIALS = "건설·부동산·건자재"
    POLICY_GEOPOLITICAL_EVENT = "정책·지정학·재난·이벤트"
    EDUCATION_LIFE_AGRI_MISC = "농업·생활서비스·기타"


@dataclass(frozen=True)
class LargeSectorDefinitionV05:
    sector: LargeSectorV05
    order: int
    role: str


LARGE_SECTOR_DEFINITIONS_V05: tuple[LargeSectorDefinitionV05, ...] = (
    LargeSectorDefinitionV05(LargeSectorV05.INDUSTRIAL_ORDERS_INFRA, 1, "contracts, backlog, grid, defense, shipbuilding, nuclear, rail"),
    LargeSectorDefinitionV05(LargeSectorV05.AI_SEMICONDUCTOR_ELECTRONICS, 2, "HBM, semiconductors, packaging, display, AI electronics"),
    LargeSectorDefinitionV05(LargeSectorV05.BATTERY_EV_GREEN, 3, "battery, EV, recycling, hydrogen, renewable policy"),
    LargeSectorDefinitionV05(LargeSectorV05.MATERIALS_SPREAD_STRATEGIC, 4, "chemical, refining, steel, nonferrous, rare metals, advanced materials"),
    LargeSectorDefinitionV05(LargeSectorV05.CONSUMER_RETAIL_BRAND, 5, "K-food, beauty, retail, apparel, home/living"),
    LargeSectorDefinitionV05(LargeSectorV05.FINANCIAL_CAPITAL_DIGITAL, 6, "banks, insurance, value-up, payment, tokenization"),
    LargeSectorDefinitionV05(LargeSectorV05.BIOTECH_HEALTHCARE_DEVICE, 7, "CDMO, biotech, diagnostics, medical device, digital healthcare"),
    LargeSectorDefinitionV05(LargeSectorV05.PLATFORM_CONTENT_SW_SECURITY, 8, "platform, software, game, content, cloud, security"),
    LargeSectorDefinitionV05(LargeSectorV05.MOBILITY_TRANSPORT_LEISURE, 9, "airline, travel, casino, shipping, auto, tire, UAM"),
    LargeSectorDefinitionV05(LargeSectorV05.CONSTRUCTION_REAL_ESTATE_MATERIALS, 10, "construction, PF credit, REIT, building materials"),
    LargeSectorDefinitionV05(LargeSectorV05.POLICY_GEOPOLITICAL_EVENT, 11, "North Korea policy, reconstruction, disaster, disease, speculative science"),
    LargeSectorDefinitionV05(LargeSectorV05.EDUCATION_LIFE_AGRI_MISC, 12, "smart farm, livestock, education, waste, kiosk, regulated consumer"),
)


def large_sector_rows_v05() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "order": str(item.order),
            "large_sector": item.sector.value,
            "role": item.role,
            "production_scoring_changed": "false",
        }
        for item in LARGE_SECTOR_DEFINITIONS_V05
    )


__all__ = ["LARGE_SECTOR_DEFINITIONS_V05", "LargeSectorDefinitionV05", "LargeSectorV05", "large_sector_rows_v05"]
