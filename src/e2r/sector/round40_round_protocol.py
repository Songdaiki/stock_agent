"""Round-40 round protocol map.

Round 40 freezes the work map before adding more cases. It keeps the 12
large-sector drawers fixed, defines R1-R12 sector validation order, and keeps
R13 as a cross-archetype RedTeam/4B/price-validation overlay.

This module is calibration/report material only. It is not production scoring,
candidate generation, staging, or RedTeam input.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from e2r.sector.round10_theme_tag_taxonomy import ROUND10_LARGE_SECTORS, Round10LargeSector


ROUND40_SOURCE_ROUND_PATH = "docs/round/round_40.md"
ROUND40_DEFAULT_OUTPUT_DIRECTORY = "output/e2r_round40_round_protocol"
ROUND40_DEFAULT_ROUND_PLAN_PATH = "data/sector_taxonomy/round40_round_protocol.csv"
ROUND40_DEFAULT_VALIDATION_PROTOCOL_PATH = "data/sector_taxonomy/round40_validation_protocol.csv"


@dataclass(frozen=True)
class Round40ValidationStep:
    step_order: int
    step_id: str
    description: str
    required_outputs: tuple[str, ...]
    guardrails: tuple[str, ...]

    def as_row(self) -> dict[str, str]:
        return {
            "step_order": str(self.step_order),
            "step_id": self.step_id,
            "description": self.description,
            "required_outputs": "|".join(self.required_outputs),
            "guardrails": "|".join(self.guardrails),
        }


@dataclass(frozen=True)
class Round40RoundPlan:
    round_id: str
    order: int
    large_sector: Round10LargeSector | None
    korean_name: str
    focus: str
    canonical_archetypes: tuple[str, ...]
    deep_sub_archetypes: tuple[str, ...]
    validation_focus: tuple[str, ...]
    expected_price_path: str
    production_scoring_changed: bool = False
    candidate_generation_input: bool = False

    @property
    def large_sector_key(self) -> str:
        return self.large_sector.value if self.large_sector is not None else "CROSS_ARCHETYPE_OVERLAY"

    def as_row(self) -> dict[str, str]:
        return {
            "round_id": self.round_id,
            "order": str(self.order),
            "large_sector": self.large_sector_key,
            "korean_name": self.korean_name,
            "focus": self.focus,
            "canonical_archetypes": "|".join(self.canonical_archetypes),
            "deep_sub_archetypes": "|".join(self.deep_sub_archetypes),
            "validation_focus": "|".join(self.validation_focus),
            "expected_price_path": self.expected_price_path,
            "production_scoring_changed": str(self.production_scoring_changed).lower(),
            "candidate_generation_input": str(self.candidate_generation_input).lower(),
        }


ROUND40_ALIGNMENT_VALUES: tuple[str, ...] = (
    "aligned",
    "false_positive_score",
    "price_moved_without_evidence",
    "evidence_good_but_price_failed",
    "cyclical_success",
    "event_premium",
    "thesis_break",
    "unknown_insufficient_price_data",
)


ROUND40_VALIDATION_PROTOCOL: tuple[Round40ValidationStep, ...] = (
    Round40ValidationStep(
        1,
        "case_coverage",
        "Collect success, success-candidate, counterexample, 4B-watch, and 4C-thesis-break cases per archetype.",
        (
            "success_cases",
            "success_candidate_cases",
            "counterexample_cases",
            "4b_watch_cases",
            "4c_thesis_break_cases",
            "insufficient_case_coverage_flags",
        ),
        (
            "do_not_force_cases_without_evidence",
            "do_not_use_case_labels_as_candidate_generation_input",
        ),
    ),
    Round40ValidationStep(
        2,
        "stage_date_candidates",
        "Assign Stage 1/2/3/4B/4C candidate dates from source evidence only.",
        (
            "stage1_theme_or_industry_detection_date",
            "stage2_disclosure_contract_financial_or_report_date",
            "stage3_mid_term_eps_fcf_and_valuation_frame_date",
            "stage4b_overheat_or_crowding_date",
            "stage4c_thesis_break_date",
        ),
        (
            "preserve_as_of_date",
            "do_not_invent_stage_dates",
            "do_not_use_future_data",
        ),
    ),
    Round40ValidationStep(
        3,
        "price_path_validation",
        "Backfill stage prices and forward MFE/MAE paths from price data only.",
        (
            "stage1_price",
            "stage2_price",
            "stage3_price",
            "peak_price",
            "stage4b_price",
            "stage4c_price",
            "mfe_30d_90d_180d_1y_2y",
            "mae_30d_90d_180d_1y",
            "drawdown_after_peak",
            "below_stage3_price_flag",
        ),
        (
            "do_not_fabricate_price_data",
            "mark_missing_price_data_explicitly",
        ),
    ),
    Round40ValidationStep(
        4,
        "score_price_alignment",
        "Classify whether the score, evidence, and price path actually line up.",
        ROUND40_ALIGNMENT_VALUES,
        (
            "separate_cyclical_success_from_structural_rerating",
            "separate_event_premium_from_true_rerating",
            "do_not_call_price_only_rally_green",
        ),
    ),
    Round40ValidationStep(
        5,
        "score_weight_correction",
        "Use success cases to propose weight increases and counterexamples to strengthen risk gates.",
        (
            "recommended_weight_direction",
            "green_gate_tightening",
            "risk_penalty_axis",
            "4b_4c_early_warning_fields",
            "shadow_only_status",
        ),
        (
            "do_not_change_production_scoring_in_round40",
            "do_not_lower_stage3_green_thresholds_blindly",
        ),
    ),
)


ROUND40_ROUND_PLANS: tuple[Round40RoundPlan, ...] = (
    Round40RoundPlan(
        "R1",
        1,
        Round10LargeSector.INDUSTRIAL_ORDERS_INFRA,
        "산업재·수주·인프라",
        "Contracts, backlog, grid, defense, shipbuilding, rail, nuclear, and data-center power equipment.",
        (
            "CONTRACT_BACKLOG_INDUSTRIAL",
            "GRID_TRANSFORMER_SHORTAGE",
            "DEFENSE_GOVERNMENT_BACKLOG",
            "DEFENSE_TECH_AUTONOMOUS_SYSTEMS",
            "DEFENSE_DRONE_COUNTER_UAS",
            "DEFENSE_AI_SOFTWARE_INTELLIGENCE",
            "SHIPBUILDING_OFFSHORE_BACKLOG",
            "RAIL_INFRASTRUCTURE",
            "NUCLEAR_SMR_GRID_POLICY",
            "GEOPOLITICAL_RECONSTRUCTION",
            "SMART_FACTORY_AUTOMATION",
            "AI_DATA_CENTER_POWER_EQUIPMENT",
        ),
        (
            "전력설비·변압기",
            "전선·케이블",
            "피팅밸브",
            "조선 기자재",
            "LNG선 기자재",
            "방산 AI",
            "드론·counter-UAS",
            "컨테이너형 미사일",
            "군사용 AI software",
            "철도 수출",
            "원전 PPA",
            "SMR",
            "데이터센터 UPS/PDU/switchgear",
        ),
        ("contract_amount_to_sales", "contract_duration", "backlog", "delivery_schedule", "op_eps_revision", "margin"),
        "Successful cases should rerate in a 6-24 month stair-step after contract and earnings confirmation.",
    ),
    Round40RoundPlan(
        "R2",
        2,
        Round10LargeSector.AI_SEMICONDUCTOR_ELECTRONICS,
        "AI·반도체·전자부품",
        "HBM, commodity memory, semi equipment, packaging, AI server supply chain, neocloud, optical networking, cooling, and trust overlays.",
        (
            "MEMORY_HBM_CAPACITY",
            "COMMODITY_MEMORY_GENERAL_SEMI",
            "SEMI_EQUIPMENT_CAPEX",
            "SEMI_MATERIALS_PROCESS",
            "ADVANCED_PACKAGING_PCB",
            "ADVANCED_PACKAGING_COWOS_EMIB",
            "DISPLAY_OLED_SUPPLYCHAIN",
            "ELECTRONIC_COMPONENTS_MLCC_SENSOR",
            "AI_CHIP_FABRIC_INFRA",
            "AI_ACCELERATOR_CHIP_PUREPLAY",
            "AI_SERVER_ODM_EMS_SUPPLY_CHAIN",
            "NEOCLOUD_GPU_RENTAL",
            "OPTICAL_NETWORKING_AI_DATACENTER",
            "INDUSTRIAL_GASES_SEMICONDUCTOR_INFRA",
            "AI_DATA_CENTER_INFRASTRUCTURE",
            "AI_DATA_CENTER_COOLING",
            "DATA_CENTER_REIT_INFRASTRUCTURE",
            "AI_GRID_FLEXIBILITY_SOFTWARE",
            "REDTEAM_ACCOUNTING_TRUST_OVERLAY",
        ),
        (
            "HBM",
            "범용 DRAM/NAND",
            "AI 서버 ODM/EMS",
            "GPU cloud / neocloud",
            "CoWoS / EMIB / advanced packaging",
            "EUV / 반도체 장비",
            "반도체용 산업가스",
            "AI 데이터센터 냉각",
            "광통신·광케이블",
            "데이터센터 REIT",
            "AI grid flexibility",
            "AI accelerator pure-play",
            "CXL",
            "유리기판",
            "뉴로모픽",
        ),
        ("eps_revision", "capacity_bottleneck", "customer_order", "gross_margin", "inventory", "accounting_trust"),
        "Strong cases show EPS revision and valuation multiple expansion together; 4B/4C cases show crowding, filing delay, CAPEX cut, or trust breaks.",
    ),
    Round40RoundPlan(
        "R3",
        3,
        Round10LargeSector.BATTERY_EV_GREEN,
        "2차전지·전기차·친환경",
        "Battery materials, equipment, recycling, ESS, hydrogen, renewable policy, CBAM, waste, and data-center water reuse.",
        (
            "BATTERY_MATERIALS_CAPEX_OVERHEAT",
            "BATTERY_EQUIPMENT_PARTS",
            "BATTERY_RECYCLING_ESS_SHIFT",
            "EV_INFRASTRUCTURE",
            "HYDROGEN_FUEL_CELL_INFRA",
            "RENEWABLE_ENERGY_POLICY",
            "SOLAR_TARIFF_SUPPLYCHAIN",
            "ENERGY_DISTRIBUTION_FUEL",
            "WASTE_RECYCLING_ENVIRONMENT",
            "CARBON_CREDIT_CBAM_COMPLIANCE",
            "DATA_CENTER_WATER_REUSE_INFRA",
        ),
        (
            "2차전지 소재",
            "2차전지 부품",
            "2차전지 공정장비",
            "폐배터리",
            "ESS 전환",
            "전고체 배터리",
            "수소연료전지",
            "태양광 관세·공급망",
            "풍력 프로젝트",
            "탄소배출권/CBAM",
            "폐기물처리",
            "탈플라스틱",
            "데이터센터 물 재활용",
        ),
        ("contract_quality", "utilization", "fcf", "ev_demand", "capa_overbuild", "commodity_price"),
        "Most cases need overheat defense; successful cases should rerate only after contract, utilization, and FCF evidence.",
    ),
    Round40RoundPlan(
        "R4",
        4,
        Round10LargeSector.MATERIALS_SPREAD_STRATEGIC,
        "소재·스프레드·전략자원",
        "Refining, chemical, steel, nonferrous, rare metals, lithium, precious metals, paper, agrifood inputs, LNG, trading, and gas utilities.",
        (
            "REFINING_OIL_SPREAD",
            "CHEMICAL_SPREAD",
            "STEEL_METAL_SPREAD",
            "NONFERROUS_STRATEGIC_METALS",
            "RARE_METALS_STRATEGIC_MATERIALS",
            "LITHIUM_BATTERY_RAW_MATERIAL",
            "PRECIOUS_METALS_SAFE_HAVEN_MINERS",
            "ADVANCED_MATERIAL_SPECULATIVE_THEME",
            "PAPER_PACKAGING_CYCLE",
            "AGRI_COMMODITY_INPUTS",
            "LNG_ENERGY_TRADING_DISTRIBUTION",
            "GENERAL_TRADING_RESOURCE_INFRA",
            "ENERGY_UTILITY_LNG_GAS",
        ),
        (
            "정유",
            "화학",
            "철강",
            "비철금속",
            "구리",
            "리튬",
            "희토류",
            "금은",
            "금광주",
            "페라이트",
            "그래핀",
            "맥신",
            "초전도체",
            "제지·골판지",
            "종합상사",
            "LNG 장기계약",
            "가스 유틸리티",
        ),
        ("product_spread", "cost_curve", "capacity_discipline", "commodity_peak", "eps_normalization"),
        "Separate cyclical_success from structural_success by comparing commodity peak, EPS peak, and stock peak.",
    ),
    Round40RoundPlan(
        "R5",
        5,
        Round10LargeSector.CONSUMER_RETAIL_BRAND,
        "소비재·유통·브랜드",
        "K-food, convenience/offline retail, e-commerce logistics, cold chain, K-beauty, ODM, apparel, home/living, rental, and regulated products.",
        (
            "EXPORT_RECURRING_CONSUMER",
            "FOOD_AGRI_LIVESTOCK_CYCLE",
            "RETAIL_CONVENIENCE_OFFLINE",
            "RETAIL_ECOMMERCE_LOGISTICS",
            "ECOMMERCE_FRESH_LOGISTICS",
            "COLD_CHAIN_REIT_LOGISTICS",
            "K_BEAUTY_EXPORT_DISTRIBUTION",
            "BEAUTY_OEM_ODM_SUPPLYCHAIN",
            "APPAREL_FAST_FASHION_BRAND_OEM",
            "HOME_LIVING_APPLIANCE_RENTAL",
            "CONSUMER_REGULATED_PRODUCT",
        ),
        (
            "라면",
            "K푸드",
            "건강기능식품",
            "편의점",
            "홈쇼핑",
            "마켓컬리·오아시스",
            "콜드체인",
            "K뷰티 브랜드",
            "화장품 OEM/ODM",
            "화장품 원재료",
            "의류 브랜드",
            "fast fashion",
            "밥솥·생활가전",
            "렌탈",
            "전자담배",
            "주정",
        ),
        ("export_growth", "channel_expansion", "repeat_demand", "opm", "inventory", "receivables", "recall_regulation"),
        "Successful cases show export/channel/OPM stair-step rerating; counterexamples draw down from viral hype, inventory, receivables, recall, or regulation.",
    ),
    Round40RoundPlan(
        "R6",
        6,
        Round10LargeSector.FINANCIAL_CAPITAL_DIGITAL,
        "금융·자본배분·디지털금융",
        "Banks, insurance, brokerage, value-up, holding restructuring, payments, fintech, and digital asset/tokenization themes.",
        (
            "FINANCIAL_SPREAD_BALANCE_SHEET",
            "INSURANCE_UNDERWRITING_CYCLE",
            "SECURITIES_BROKERAGE_CYCLE",
            "VALUE_UP_SHAREHOLDER_RETURN",
            "HOLDING_RESTRUCTURING_GOVERNANCE",
            "PAYMENT_FINTECH_INFRA",
            "DIGITAL_ASSET_TOKENIZATION",
        ),
        (
            "은행",
            "금융지주",
            "손해보험",
            "생명보험",
            "증권사",
            "VC",
            "고배당",
            "밸류업",
            "자사주 소각",
            "부동산 자산 보유",
            "결제서비스",
            "PG",
            "e-wallet",
            "신용정보",
            "토스 관련주",
            "STO",
            "스테이블코인",
            "NFT와의 분리",
        ),
        ("roe", "capital_ratio", "csm", "loss_ratio", "buyback_cancel", "pbr_roe_gap", "regulated_revenue"),
        "Banks and insurers validate PBR-ROE rerating; tokenization and fintech require real regulated revenue before Green.",
    ),
    Round40RoundPlan(
        "R7",
        7,
        Round10LargeSector.BIOTECH_HEALTHCARE_DEVICE,
        "바이오·헬스케어·의료기기",
        "CDMO, CRO, biosimilar, GLP-1, gene therapy, AI drug discovery, digital healthcare, telehealth, medical device, diagnostics, and animal health.",
        (
            "CDMO_HEALTHCARE_CONTRACT",
            "CRO_CLINICAL_SERVICE",
            "BIOSIMILAR_COMMERCIALIZATION",
            "BIOSIMILAR_ORIGINATOR_DEFENSE",
            "OBESITY_GLP1_COMMERCIALIZATION",
            "GENE_THERAPY_RARE_DISEASE",
            "AI_DRUG_DISCOVERY_PLATFORM",
            "DIGITAL_HEALTHCARE_AI",
            "DIGITAL_HEALTHCARE_REMOTE_MEDICINE",
            "TELEHEALTH_BEHAVIORAL_HEALTH",
            "PHARMA_CHANNEL_AND_PRIVACY_RISK",
            "MEDICAL_DEVICE_HEALTHCARE_EXPORT",
            "MEDICAL_DEVICE_DENTAL_IMPLANT",
            "DIAGNOSTICS_INFECTIOUS_DISEASE",
            "ANIMAL_HEALTH_BIOSECURITY",
        ),
        (
            "CDMO",
            "CRO",
            "바이오시밀러",
            "오리지널 특허방어",
            "GLP-1 비만치료제",
            "유전자치료제",
            "희귀질환",
            "AI 신약개발",
            "의료AI",
            "원격의료",
            "온라인 정신건강",
            "약물 플랫폼·조제약",
            "미용기기",
            "보톡스",
            "치아·임플란트",
            "진단키트",
            "동물백신·방역",
        ),
        ("contract_backlog", "capacity_utilization", "approval", "reimbursement", "commercialization", "dilution", "privacy"),
        "Medical device/CDMO can rerate on contracts and recurring revenue; pre-revenue biotech remains Watch/Red until commercialization and cash-flow visibility.",
    ),
    Round40RoundPlan(
        "R8",
        8,
        Round10LargeSector.PLATFORM_CONTENT_SW_SECURITY,
        "플랫폼·콘텐츠·SW·보안",
        "Platform, SaaS, cloud, AI application software, contact-center AI, kiosk, game/content IP, media/ad cycle, security, deepfake, and generative-AI IP risk.",
        (
            "PLATFORM_SOFTWARE_INTERNET",
            "CLOUD_AI_SOFTWARE_INFRA",
            "AI_SOFTWARE_APPLICATION",
            "CONTACT_CENTER_AI_AUTOMATION",
            "SERVICE_KIOSK_SELF_CHECKOUT",
            "GAME_CONTENT_IP",
            "MEDIA_AD_CONTENT_CYCLE",
            "METAVERSE_NFT_THEME",
            "SECURITY_IDENTITY_DEEPFAKE",
            "GENERATIVE_AI_IP_RISK",
        ),
        (
            "플랫폼",
            "SaaS",
            "ERP",
            "클라우드",
            "AI 소프트웨어",
            "생성AI 앱",
            "컨택센터 AI",
            "키오스크",
            "게임 IP",
            "엔터",
            "미디어·광고",
            "스트리밍 광고",
            "보안",
            "딥페이크",
            "생체인식",
            "CCTV",
            "NFT",
            "메타버스",
        ),
        ("arr", "opm", "fcf", "churn", "paid_usage", "ip_monetization", "privacy_security_incident"),
        "Successful cases pair ARR/OPM/FCF with price; hard 4C includes security outages, privacy, copyright, and trust failures.",
    ),
    Round40RoundPlan(
        "R9",
        9,
        Round10LargeSector.MOBILITY_TRANSPORT_LEISURE,
        "모빌리티·운송·레저",
        "Completed vehicles, components, tires, airlines, travel, casino/duty-free tourism, shipping, rental/used car mobility, UAM/drone, space, and satellite connectivity.",
        (
            "AUTO_MOBILITY_COMPLETED_VEHICLE",
            "AUTO_MOBILITY_COMPONENTS",
            "TIRE_AUTO_COMPONENT_SPREAD",
            "AIRLINE_TRAVEL_CYCLE",
            "TRAVEL_LEISURE_REOPENING",
            "CASINO_DUTYFREE_TOURISM",
            "SHIPPING_FREIGHT_CYCLE",
            "RENTAL_USED_CAR_MOBILITY",
            "MOBILITY_RENTAL_MICROMOBILITY",
            "URBAN_AIR_DRONE",
            "SPACE_SUPPLYCHAIN",
            "SATELLITE_CONNECTIVITY_INFRA",
        ),
        (
            "완성차",
            "하이브리드",
            "자동차 부품",
            "전장",
            "자율주행",
            "타이어",
            "항공사",
            "여행·레저",
            "카지노",
            "면세점",
            "해운",
            "렌터카",
            "중고차",
            "자전거",
            "공유 모빌리티",
            "드론·플라잉카",
            "스페이스X 관련주",
            "위성통신",
        ),
        ("fcf", "hybrid_mix", "shareholder_return", "customer_diversification", "freight_rate", "tourist_mix", "government_contract"),
        "Autos can show PBR/ROE/value-up rerating; travel and shipping are mostly cyclical and need peak/drawdown validation.",
    ),
    Round40RoundPlan(
        "R10",
        10,
        Round10LargeSector.CONSTRUCTION_REAL_ESTATE_MATERIALS,
        "건설·부동산·건자재",
        "Construction credit, REIT/development trusts, building materials, data-center REITs, cold-chain logistics, reconstruction policy, and disaster rebuild events.",
        (
            "CONSTRUCTION_REAL_ESTATE_CREDIT",
            "REIT_DEVELOPMENT_TRUST",
            "BUILDING_MATERIALS_CYCLE",
            "DATA_CENTER_REIT_INFRASTRUCTURE",
            "COLD_CHAIN_REIT_LOGISTICS",
            "INFRA_RECONSTRUCTION_POLICY",
            "DISASTER_REBUILD_EVENT",
        ),
        (
            "대형 건설사",
            "중소형 건설사",
            "PF",
            "미분양",
            "리츠",
            "개발신탁",
            "건자재",
            "시멘트",
            "레미콘",
            "철근",
            "거푸집",
            "가구",
            "데이터센터 REIT",
            "콜드체인 REIT",
            "우크라 재건",
            "네옴시티",
            "재난복구",
        ),
        ("pf_credit", "cash_flow", "cost_ratio", "occupancy", "affo", "funding_cost", "tenant_contract"),
        "Separate relief rallies from structural recovery; REIT cases need AFFO and dividend coverage, not rate headlines alone.",
    ),
    Round40RoundPlan(
        "R11",
        11,
        Round10LargeSector.POLICY_GEOPOLITICAL_EVENT,
        "정책·지정학·재난·이벤트",
        "North Korea policy, reconstruction, climate/disaster, disease/pest demand, speculative science, advanced material themes, and local policy themes.",
        (
            "NORTH_KOREA_POLICY_EVENT",
            "GEOPOLITICAL_RECONSTRUCTION",
            "CLIMATE_DISASTER_EVENT",
            "EVENT_DISEASE_PEST_DEMAND",
            "SPECULATIVE_SCIENCE_THEME",
            "ADVANCED_MATERIAL_SPECULATIVE_THEME",
            "POLICY_LOCAL_THEME",
            "ONE_OFF_EVENT_DEMAND",
            "THEME_VALUATION_OVERHEAT",
        ),
        (
            "남북경협",
            "DMZ",
            "개성공단",
            "금강산",
            "북한 광물",
            "우크라 재건",
            "네옴시티",
            "세종시",
            "지진",
            "폭염",
            "황사",
            "마스크",
            "엠폭스",
            "빈대",
            "코로나",
            "초전도체",
            "맥신",
            "그래핀",
            "양자",
            "페라이트",
        ),
        ("event_date", "contract_absence", "mfe_5d_20d_60d", "drawdown_after_news_fade", "eps_fcf_absence"),
        "Most cases are Green-blocked; validate short MFE and post-event drawdown rather than forcing structural conviction.",
    ),
    Round40RoundPlan(
        "R12",
        12,
        Round10LargeSector.EDUCATION_LIFE_AGRI_MISC,
        "농업·생활서비스·기타",
        "Smart farm, agri/livestock commodity, animal health, education, home/living rental, kiosks, and regulated consumer products.",
        (
            "SMART_FARM_AGRI_TECH",
            "AGRI_LIVESTOCK_FOOD_COMMODITY",
            "ANIMAL_HEALTH_BIOSECURITY",
            "HOME_CHILD_EDUCATION",
            "EDUCATION_SPECIALTY_SERVICES",
            "HOME_LIVING_APPLIANCE_RENTAL",
            "SERVICE_KIOSK_SELF_CHECKOUT",
            "CONSUMER_REGULATED_PRODUCT",
        ),
        (
            "스마트팜",
            "농기계",
            "종자·비료·농약",
            "양돈",
            "육계",
            "대두",
            "배합사료",
            "참치",
            "동물백신",
            "교육",
            "취업",
            "키즈",
            "유아용품",
            "밥솥",
            "생활가전 렌탈",
            "키오스크",
            "전자담배",
            "마리화나",
            "주정",
        ),
        ("commercial_installation", "recurring_service", "disease_event", "repeat_course", "churn", "regulatory_approval"),
        "Validate disease/agri event drawdowns, education retention, rental FCF, and kiosk recurring revenue separately.",
    ),
    Round40RoundPlan(
        "R13",
        13,
        None,
        "Cross-archetype RedTeam / 4B / 가격검증 총정리",
        "Cross-sector overlays for accounting trust, valuation overheat, one-off demand, price-only rallies, crowding, 4B, 4C, and score-price alignment.",
        (
            "REDTEAM_ACCOUNTING_TRUST_OVERLAY",
            "THEME_VALUATION_OVERHEAT",
            "ONE_OFF_EVENT_DEMAND",
            "PRICE_ONLY_RALLY",
            "CROWDING_4B_WATCH",
        ),
        (
            "감사인 사임",
            "감사보고서 지연",
            "내부통제 중대 결함",
            "SEC/검찰/규제기관 조사",
            "관련자거래 의혹",
            "계약 취소",
            "수주 취소",
            "대형 보안 장애",
            "개인정보 유출",
            "규제 불허",
            "현금 runway 붕괴",
        ),
        ("accounting_trust", "crowding", "valuation_band", "price_only_rally", "hard_4c", "score_price_alignment"),
        "R13 classifies every R1-R12 case into alignment labels and adds cross-sector 4B/4C guardrails.",
    ),
)


def round40_summary() -> dict[str, int | bool]:
    canonical_count = sum(len(item.canonical_archetypes) for item in ROUND40_ROUND_PLANS if item.large_sector is not None)
    deep_count = sum(len(item.deep_sub_archetypes) for item in ROUND40_ROUND_PLANS if item.large_sector is not None)
    return {
        "large_sector_count": len(ROUND10_LARGE_SECTORS),
        "round_count": len(ROUND40_ROUND_PLANS),
        "sector_round_count": sum(1 for item in ROUND40_ROUND_PLANS if item.large_sector is not None),
        "cross_overlay_round_count": sum(1 for item in ROUND40_ROUND_PLANS if item.large_sector is None),
        "canonical_archetype_mentions": canonical_count,
        "deep_sub_archetype_mentions": deep_count,
        "validation_step_count": len(ROUND40_VALIDATION_PROTOCOL),
        "alignment_value_count": len(ROUND40_ALIGNMENT_VALUES),
        "production_scoring_changed": False,
        "round_plan_is_candidate_generation_input": False,
    }


def round40_round_plan_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND40_ROUND_PLANS)


def round40_validation_protocol_rows() -> tuple[dict[str, str], ...]:
    return tuple(item.as_row() for item in ROUND40_VALIDATION_PROTOCOL)


def render_round40_summary_markdown() -> str:
    summary = round40_summary()
    lines = [
        "# Round-40 Round Protocol Summary",
        "",
        f"- source_round: `{ROUND40_SOURCE_ROUND_PATH}`",
        f"- large_sector_count: {summary['large_sector_count']}",
        f"- round_count: {summary['round_count']}",
        f"- sector_round_count: {summary['sector_round_count']}",
        f"- cross_overlay_round_count: {summary['cross_overlay_round_count']}",
        f"- canonical_archetype_mentions: {summary['canonical_archetype_mentions']}",
        f"- deep_sub_archetype_mentions: {summary['deep_sub_archetype_mentions']}",
        f"- validation_step_count: {summary['validation_step_count']}",
        f"- alignment_value_count: {summary['alignment_value_count']}",
        "- production_scoring_changed: false",
        "- round_plan_is_candidate_generation_input: false",
        "",
        "## Interpretation",
        "",
        "- The 12 large-sector map is fixed.",
        "- R1-R12 are the sector-by-sector case mining sequence.",
        "- R13 is a cross-archetype RedTeam, 4B/4C, and price-validation overlay.",
        "- The round plan is a calibration roadmap. It does not change production scoring.",
        "",
        "## Simple Example",
        "",
        "`AI server ODM` belongs to the AI/semiconductor drawer, but it is not the same scoring problem as `HBM`. The ODM case needs margin, inventory, customer, and trust checks; HBM needs capacity, pricing, and multi-year revision checks.",
    ]
    return "\n".join(lines) + "\n"


def render_round40_round_sequence_markdown() -> str:
    lines = [
        "# Round-40 R1-R13 Sequence",
        "",
        "| Round | Large Sector | Focus | Canonical Archetypes |",
        "| --- | --- | --- | --- |",
    ]
    for item in ROUND40_ROUND_PLANS:
        lines.append(
            f"| {item.round_id} | {item.korean_name} | {item.focus} | {len(item.canonical_archetypes)} |"
        )
    lines.extend(
        [
            "",
            "## Guardrail",
            "",
            "- Do not add a 13th production large sector for every new theme.",
            "- Add new themes under a parent large sector and a canonical archetype.",
            "- Keep R13 as an overlay, not a separate candidate-generation source.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round40_validation_protocol_markdown() -> str:
    lines = ["# Round-40 Common Validation Protocol", ""]
    for step in ROUND40_VALIDATION_PROTOCOL:
        lines.extend(
            [
                f"## {step.step_order}. {step.step_id}",
                "",
                step.description,
                "",
                "Required outputs:",
                *[f"- `{item}`" for item in step.required_outputs],
                "",
                "Guardrails:",
                *[f"- `{item}`" for item in step.guardrails],
                "",
            ]
        )
    lines.extend(
        [
            "## What Not To Change",
            "",
            "- Do not use benchmark or case labels as candidate-generation input.",
            "- Do not invent contracts, prices, dates, or EPS/FCF fields.",
            "- Do not lower Stage 3-Green thresholds to improve recall.",
            "- Do not apply final score weights before case and price-path coverage is sufficient.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_round40_price_alignment_markdown() -> str:
    descriptions = {
        "aligned": "Score, evidence, EPS/FCF, and price path move together after the evidence date.",
        "false_positive_score": "The score looked high, but price and/or fundamentals did not rerate.",
        "price_moved_without_evidence": "The price rose, but the system should not treat it as evidence-backed E2R.",
        "evidence_good_but_price_failed": "Evidence looked valid, but the market did not rerate it.",
        "cyclical_success": "The case worked as a cycle, but not as structural E2R.",
        "event_premium": "A policy, tender, takeover, or event premium drove the move.",
        "thesis_break": "A 4C-style event broke the original thesis.",
        "unknown_insufficient_price_data": "Price path is missing or insufficient; do not force alignment.",
    }
    lines = [
        "# Round-40 Score-Price Alignment Protocol",
        "",
        "| Label | Meaning |",
        "| --- | --- |",
    ]
    for label in ROUND40_ALIGNMENT_VALUES:
        lines.append(f"| `{label}` | {descriptions[label]} |")
    lines.extend(
        [
            "",
            "## Example",
            "",
            "If a stock jumps on a policy headline but there is no EPS/FCF evidence, it can be `event_premium` or `price_moved_without_evidence`; it must not become Stage 3-Green from price alone.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_round40_round_protocol_reports(
    *,
    output_directory: str | Path = ROUND40_DEFAULT_OUTPUT_DIRECTORY,
    round_plan_path: str | Path = ROUND40_DEFAULT_ROUND_PLAN_PATH,
    validation_protocol_path: str | Path = ROUND40_DEFAULT_VALIDATION_PROTOCOL_PATH,
) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    round_plan = Path(round_plan_path)
    round_plan.parent.mkdir(parents=True, exist_ok=True)
    validation_protocol = Path(validation_protocol_path)
    validation_protocol.parent.mkdir(parents=True, exist_ok=True)

    paths = {
        "round_plan": round_plan,
        "validation_protocol": validation_protocol,
        "summary": output / "round40_round_protocol_summary.md",
        "round_sequence": output / "round40_round_sequence.md",
        "validation_protocol_md": output / "round40_validation_protocol.md",
        "price_alignment_protocol": output / "round40_price_alignment_protocol.md",
    }
    _write_rows(round40_round_plan_rows(), paths["round_plan"])
    _write_rows(round40_validation_protocol_rows(), paths["validation_protocol"])
    paths["summary"].write_text(render_round40_summary_markdown(), encoding="utf-8")
    paths["round_sequence"].write_text(render_round40_round_sequence_markdown(), encoding="utf-8")
    paths["validation_protocol_md"].write_text(render_round40_validation_protocol_markdown(), encoding="utf-8")
    paths["price_alignment_protocol"].write_text(render_round40_price_alignment_markdown(), encoding="utf-8")
    return paths


def _write_rows(rows: Iterable[Mapping[str, str]], path: Path) -> Path:
    row_tuple = tuple(rows)
    if not row_tuple:
        path.write_text("", encoding="utf-8")
        return path
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(row_tuple[0].keys()), lineterminator="\n")
        writer.writeheader()
        for row in row_tuple:
            writer.writerow(row)
    return path


__all__ = [
    "ROUND40_ALIGNMENT_VALUES",
    "ROUND40_DEFAULT_OUTPUT_DIRECTORY",
    "ROUND40_DEFAULT_ROUND_PLAN_PATH",
    "ROUND40_DEFAULT_VALIDATION_PROTOCOL_PATH",
    "ROUND40_ROUND_PLANS",
    "ROUND40_SOURCE_ROUND_PATH",
    "ROUND40_VALIDATION_PROTOCOL",
    "Round40RoundPlan",
    "Round40ValidationStep",
    "render_round40_price_alignment_markdown",
    "render_round40_round_sequence_markdown",
    "render_round40_summary_markdown",
    "render_round40_validation_protocol_markdown",
    "round40_round_plan_rows",
    "round40_summary",
    "round40_validation_protocol_rows",
    "write_round40_round_protocol_reports",
]
