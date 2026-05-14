"""Sector-to-archetype mapping rules for Korea equities.

The mapper is intentionally rule based and transparent. It uses sector,
industry, company, and product keywords, but it does not assign scores or
stages. The output is taxonomy metadata used for coverage analysis and future
weight design.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.archetypes import E2RArchetype


@dataclass(frozen=True)
class SectorMapping:
    """Result of mapping one company to a custom sector and archetype."""

    sector_custom: str
    primary_archetype: E2RArchetype
    secondary_archetypes: tuple[E2RArchetype, ...]
    business_keywords: tuple[str, ...]
    product_keywords: tuple[str, ...]
    confidence: float
    reason: str
    source: str = "rule"


@dataclass(frozen=True)
class SectorMappingRules:
    """Keyword rules loaded from defaults plus optional local rule files."""

    sector_aliases: Mapping[str, str]
    archetype_keywords: Mapping[E2RArchetype, tuple[str, ...]]
    manual_overrides: Mapping[str, SectorMapping]


DEFAULT_SECTOR_ALIASES: dict[str, str] = {
    "전력기기": "전력기기/전선",
    "전선": "전력기기/전선",
    "변압기": "전력기기/전선",
    "중전기": "전력기기/전선",
    "방산": "방산",
    "항공우주": "방산",
    "조선": "조선/해양",
    "해양플랜트": "조선/해양",
    "음식료": "식품수출",
    "식품": "식품수출",
    "라면": "식품수출",
    "화장품": "K-뷰티/유통",
    "화장품유통": "K-뷰티/유통",
    "뷰티": "K-뷰티/유통",
    "반도체": "메모리/HBM",
    "메모리": "메모리/HBM",
    "HBM": "메모리/HBM",
    "반도체장비": "반도체장비",
    "2차전지": "2차전지/소재",
    "배터리": "2차전지/소재",
    "양극재": "2차전지/소재",
    "화학": "소재/스프레드",
    "철강": "소재/스프레드",
    "정유": "소재/스프레드",
    "해운": "해운/운임",
    "자동차": "자동차/부품",
    "모빌리티": "자동차/부품",
    "로봇": "로봇/자동화",
    "자동화": "로봇/자동화",
    "인터넷": "플랫폼/소프트웨어",
    "플랫폼": "플랫폼/소프트웨어",
    "소프트웨어": "플랫폼/소프트웨어",
    "게임": "게임/콘텐츠",
    "콘텐츠": "게임/콘텐츠",
    "엔터": "게임/콘텐츠",
    "은행": "금융",
    "보험": "금융",
    "증권": "금융",
    "금융": "금융",
    "바이오": "바이오/제약",
    "제약": "바이오/제약",
    "진단": "의료기기/헬스케어",
    "의료기기": "의료기기/헬스케어",
    "헬스케어": "의료기기/헬스케어",
    "유통": "내수소비/유통",
    "소매": "내수소비/유통",
    "건설": "건설/부동산",
    "부동산": "건설/부동산",
    "전력": "유틸리티",
    "가스": "유틸리티",
    "유틸리티": "유틸리티",
    "지주": "지주/거버넌스",
    "홀딩스": "지주/거버넌스",
    "구조조정": "턴어라운드",
    "턴어라운드": "턴어라운드",
    "진단키트": "일회성 이벤트 수요",
    "테마": "테마/밸류에이션 과열",
}


DEFAULT_ARCHETYPE_KEYWORDS: dict[E2RArchetype, tuple[str, ...]] = {
    E2RArchetype.CONTRACT_BACKLOG_INDUSTRIAL: ("전력기기", "전선", "변압기", "중전기", "수주", "장기공급"),
    E2RArchetype.DEFENSE_GOVERNMENT_BACKLOG: ("방산", "항공우주", "K9", "천무", "정부", "폴란드"),
    E2RArchetype.SHIPBUILDING_OFFSHORE_BACKLOG: ("조선", "해양플랜트", "선박", "LNG선", "수주잔고"),
    E2RArchetype.EXPORT_RECURRING_CONSUMER: ("음식료", "식품", "라면", "불닭", "수출", "소비재"),
    E2RArchetype.K_BEAUTY_EXPORT_DISTRIBUTION: ("화장품", "뷰티", "화장품유통", "K-뷰티", "해외 채널"),
    E2RArchetype.MEMORY_HBM_CAPACITY: ("반도체", "메모리", "HBM", "DRAM", "NAND"),
    E2RArchetype.SEMI_EQUIPMENT_CAPEX: ("반도체장비", "장비", "식각", "증착", "패키징"),
    E2RArchetype.BATTERY_MATERIALS_CAPEX_OVERHEAT: ("2차전지", "배터리", "양극재", "음극재", "전해액"),
    E2RArchetype.COMMODITY_SPREAD: ("화학", "철강", "정유", "스프레드", "원자재"),
    E2RArchetype.SHIPPING_FREIGHT_CYCLE: ("해운", "운임", "컨테이너", "벌크"),
    E2RArchetype.AUTO_MOBILITY_COMPONENTS: ("자동차", "부품", "모빌리티", "전장"),
    E2RArchetype.ROBOTICS_FACTORY_AUTOMATION: ("로봇", "자동화", "FA", "스마트팩토리"),
    E2RArchetype.PLATFORM_SOFTWARE_INTERNET: ("인터넷", "플랫폼", "소프트웨어", "클라우드", "SaaS"),
    E2RArchetype.GAME_CONTENT_IP: ("게임", "콘텐츠", "IP", "엔터", "웹툰"),
    E2RArchetype.FINANCIAL_SPREAD_BALANCE_SHEET: ("은행", "보험", "증권", "금융", "순이자마진"),
    E2RArchetype.BIOTECH_REGULATORY: ("바이오", "제약", "임상", "허가"),
    E2RArchetype.MEDICAL_DEVICE_HEALTHCARE_EXPORT: ("의료기기", "진단", "헬스케어", "수출"),
    E2RArchetype.RETAIL_DOMESTIC_CONSUMER: ("유통", "소매", "편의점", "내수소비"),
    E2RArchetype.CONSTRUCTION_REAL_ESTATE_CREDIT: ("건설", "부동산", "PF", "분양"),
    E2RArchetype.UTILITIES_REGULATED_TARIFF: ("전력", "가스", "유틸리티", "요금"),
    E2RArchetype.HOLDING_RESTRUCTURING_GOVERNANCE: ("지주", "홀딩스", "거버넌스", "자회사"),
    E2RArchetype.TURNAROUND_COST_RESTRUCTURING: ("구조조정", "턴어라운드", "비용절감", "흑자전환"),
    E2RArchetype.ONE_OFF_EVENT_DEMAND: ("진단키트", "팬데믹", "일회성", "특수"),
    E2RArchetype.THEME_VALUATION_OVERHEAT: ("테마", "과열", "밈", "급등"),
}


def default_mapping_rules() -> SectorMappingRules:
    """Return built-in mapping rules."""

    return SectorMappingRules(
        sector_aliases=dict(DEFAULT_SECTOR_ALIASES),
        archetype_keywords=dict(DEFAULT_ARCHETYPE_KEYWORDS),
        manual_overrides={},
    )


def load_mapping_rules(root: str | Path = "data/sector_taxonomy") -> SectorMappingRules:
    """Load mapping rules.

    The repo ships human-readable YAML files, but the runtime does not require
    PyYAML. Defaults are authoritative; the local files document and lightly
    extend them when they follow a simple ``key: value`` form.
    """

    root_path = Path(root)
    aliases = dict(DEFAULT_SECTOR_ALIASES)
    aliases.update(_load_simple_mapping(root_path / "sector_aliases.yml"))

    archetype_keywords = dict(DEFAULT_ARCHETYPE_KEYWORDS)
    raw_rules = _load_simple_mapping(root_path / "archetype_rules.yml")
    for archetype_name, value in raw_rules.items():
        try:
            archetype = E2RArchetype(archetype_name)
        except ValueError:
            continue
        keywords = tuple(item.strip() for item in value.replace("|", ",").split(",") if item.strip())
        if keywords:
            archetype_keywords[archetype] = tuple(dict.fromkeys((*archetype_keywords.get(archetype, ()), *keywords)))

    return SectorMappingRules(sector_aliases=aliases, archetype_keywords=archetype_keywords, manual_overrides={})


def map_sector(
    *,
    symbol: str,
    company_name: str,
    sector_raw: str | None = None,
    industry_raw: str | None = None,
    text: str | None = None,
    rules: SectorMappingRules | None = None,
) -> SectorMapping:
    """Map raw sector/company text to E2R taxonomy metadata."""

    rules = rules or default_mapping_rules()
    override = rules.manual_overrides.get(symbol)
    if override is not None:
        return override

    haystack = " ".join(item for item in (company_name, sector_raw or "", industry_raw or "", text or "") if item).lower()
    matched_keywords: list[str] = []
    sector_custom = str(sector_raw or industry_raw or "미분류")
    for keyword, alias in rules.sector_aliases.items():
        if keyword.lower() in haystack:
            sector_custom = alias
            matched_keywords.append(keyword)
            break

    scored: list[tuple[int, int, E2RArchetype, tuple[str, ...]]] = []
    for archetype, keywords in rules.archetype_keywords.items():
        hits = tuple(keyword for keyword in keywords if keyword.lower() in haystack)
        if hits:
            scored.append((len(hits), sum(len(item) for item in hits), archetype, hits))
    scored.sort(key=lambda item: (-item[0], -item[1], item[2].value))

    if scored:
        primary = scored[0][2]
        secondary = tuple(item[2] for item in scored[1:3])
        keywords = tuple(dict.fromkeys(keyword for _, _, _, hits in scored for keyword in hits))
        confidence = min(1.0, 0.55 + 0.12 * len(keywords))
        reason = f"keyword_match:{','.join(keywords[:5])}"
    else:
        primary = E2RArchetype.GENERIC_UNCLASSIFIED
        secondary = ()
        keywords = tuple(matched_keywords)
        confidence = 0.25 if sector_custom != "미분류" else 0.1
        reason = "no_archetype_keyword"

    business_keywords = tuple(dict.fromkeys((*matched_keywords, *keywords)))
    product_keywords = tuple(item for item in business_keywords if item in {"변압기", "HBM", "불닭", "K9", "진단키트", "양극재"})
    return SectorMapping(
        sector_custom=sector_custom,
        primary_archetype=primary,
        secondary_archetypes=secondary,
        business_keywords=business_keywords,
        product_keywords=product_keywords,
        confidence=round(confidence, 3),
        reason=reason,
    )


def map_many(rows: Iterable[Mapping[str, str]], rules: SectorMappingRules | None = None) -> tuple[SectorMapping, ...]:
    """Map simple row dictionaries."""

    return tuple(
        map_sector(
            symbol=str(row.get("symbol") or ""),
            company_name=str(row.get("company_name") or row.get("name") or ""),
            sector_raw=row.get("sector_raw") or row.get("sector_custom"),
            industry_raw=row.get("industry_raw"),
            text=row.get("text"),
            rules=rules,
        )
        for row in rows
    )


def _load_simple_mapping(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    mapping: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line or line.startswith("-"):
            continue
        key, value = line.split(":", 1)
        key = key.strip().strip('"').strip("'")
        value = value.strip().strip('"').strip("'")
        if key and value and not value.startswith("{"):
            mapping[key] = value
    return mapping


__all__ = [
    "DEFAULT_ARCHETYPE_KEYWORDS",
    "DEFAULT_SECTOR_ALIASES",
    "SectorMapping",
    "SectorMappingRules",
    "default_mapping_rules",
    "load_mapping_rules",
    "map_many",
    "map_sector",
]
