좋아. 아래는 **그대로 복붙해서 에이전트한테 줄 수 있는 중간 체크포인트 지시문**이야.

핵심은 이거야.

> **점수정규화는 아직 production 적용 금지.**
> **성공/반례/주가검증으로 근거를 더 쌓는다.**
> **이번 단계는 theme_tag_map CSV화 + unmatched audit + case evidence/price validation 구조화다.**

지금 우리가 만드는 에이전트의 본질은 “테마봇”이 아니라, **산업 구조 변화 → EPS/FCF 체급 변화 → 시장의 과거 프레임 오해 → 밸류에이션 리레이팅**을 찾는 시스템이야. 이 정신을 잃으면 초전도체, 엠폭스, 스테이블코인, AI, 로봇 같은 테마에 다 끌려가서 망가진다.
또 증거는 반드시 실제 공시·리포트·뉴스·가격·재무에서 나와야 하고, 계약금액·계약기간·매출대비 계약금액 같은 필드가 없으면 만들어내면 안 된다. 이건 OpenDART detail fetch 쪽 원칙과도 맞다.

---

# 딥서치 기반으로 보강한 핵심 판단

HBM/메모리 쪽은 구조적 Green이 가능한 대표 archetype이다. 빅테크 고객들이 SK하이닉스 공급 확보를 위해 생산라인·EUV 장비 자금지원, 장기계약, 가격밴드, 선수금 구조까지 제안했다는 Reuters 보도는 “단순 업황 회복”이 아니라 “구조적 병목 + 다년 visibility”의 증거로 볼 수 있다. 이쪽은 EPS/FCF, structural visibility, bottleneck/pricing 가중치를 높게 줄 수 있다. ([Reuters][1])

반대로 화학은 EPS가 반등해도 Green을 쉽게 주면 안 된다. LG화학과 롯데케미칼은 공급과잉, 특히 중국·중동 capacity 부담 속에 2024년 이익이 크게 악화됐고, 롯데케미칼은 2011년 이후 최대 영업손실을 기록했다. 화학은 `CHEMICAL_SPREAD`로 두되, structural visibility를 낮게 시작하고 supply glut risk cap을 강하게 둬야 한다. ([Reuters][2])

2차전지는 “성공 가능”보다 “과열 방어”가 더 중요하다. GM-LG Ohio 배터리 공장의 재가동 시점이 EV 수요 둔화로 불확실하고, Tennessee 공장이 ESS 셀 생산으로 전환되는 흐름은 EV 소재/CAPA 과열과 ESS 전환을 분리해서 봐야 한다는 근거다. ([Reuters][3])

CDMO는 임상 바이오와 다르게 Green 가능성이 있다. Samsung Biologics가 GSK의 Rockville 생산시설을 2억 8천만 달러에 인수해 미국 생산거점을 확보하고 60,000L drug substance capacity를 더한 것은, CDMO가 “임상 기대”가 아니라 capacity·고객사·가동률·장기계약으로 평가되어야 한다는 사례다. ([Reuters][4])

스테이블코인/STO/디지털자산은 아직 Watch 중심이다. Toss가 원화 스테이블코인 발행 의지를 보였지만 규제 승인, 실제 발행량, 거래량, 수익모델이 확인되기 전까지 Green은 금지해야 한다. ([Reuters][5])

Korea Zinc 같은 케이스는 전략금속과 거버넌스가 섞여 있지만, 경영권 분쟁·공개매수 프리미엄과 구조적 FCF 리레이팅을 분리해야 한다. 공개매수 발표 후 주가가 급등한 것은 event premium일 수 있으므로, 바로 structural_success로 넣으면 안 된다. ([Reuters][6])

건설/PF는 수주보다 신용 리스크가 먼저다. 한국 부동산 PF 연체율이 2021년 말 0.37%에서 2023년 말 2.70%로 상승했고 금융당국이 구조조정을 강화했다는 점은, 건설주에서 PF·미분양·현금흐름 리스크를 hard RedTeam으로 둬야 한다는 근거다. ([Reuters][7])

---

# 에이전트용 지시문

```text
Goal:
Implement Checkpoint 28A-3: Theme Tag Map v0.5, Unmatched Theme Audit, Case Validation Expansion, and Score-Normalization Research Loop.

Context:
We are NOT ready to apply production scoring changes.

The current priority is:
1. Convert the expanded raw Korean theme list into a normalized theme_tag_map CSV.
2. Run unmatched audit until every raw theme tag is mapped.
3. Expand archetypes/sub-archetypes so all themes can be absorbed without creating one-off stock-name hacks.
4. Expand success/counterexample case records.
5. Add price-path validation requirements.
6. Generate score-normalization recommendations from success/counterexample evidence.
7. Keep all scoring changes in research/shadow mode only.

Core philosophy:
The agent must not become a theme-chasing bot.
The agent must preserve the E2R / SeoSaengWon style logic:

Industrial structure change
-> EPS/FCF bodyweight change
-> market still uses old frame
-> valuation rerating
-> hold until thesis damage / graduation

Theme tags are only for search, classification, and query planning.
Theme tags are not direct scoring evidence.

Do not change production StageClassifier thresholds yet.
Do not apply score_weight_hint to production scoring.
Do not use case records as candidate-generation input.
Do not fabricate evidence, prices, dates, or parsed fields.

Read:
- docs/e2r_standard_flow.md
- docs/korea_sector_taxonomy.md
- docs/e2r_case_library_runbook.md
- docs/e2r_case_record_schema_v02.md if present
- docs/checkpoints/checkpoint_28a_sector_taxonomy_and_case_mining.md
- docs/checkpoints/checkpoint_28a_2_case_record_pack_v02.md if present
- data/e2r_case_library/cases.jsonl
- data/e2r_case_library/cases_v02.jsonl if present
- data/sector_taxonomy/korea_sector_map.csv
- src/e2r/sector/archetypes.py
- src/e2r/sector/taxonomy.py
- src/e2r/sector/sector_mapper.py
- src/e2r/sector/case_library.py
- src/e2r/sector/peer_normalizer.py
- src/e2r/features.py
- src/e2r/staging.py

Part A: Add raw theme tag input file

Create:
- data/sector_taxonomy/raw_theme_tags_v05.txt
- data/sector_taxonomy/raw_theme_tags_v05.csv

The raw list should include all user-supplied Korean themes, including but not limited to:
편의점, 손해보험, 부동산 자산 보유, 카지노, 종합상사, 라면, 생명보험, 면세점, 양돈주, 홈쇼핑, 음식료, 태양광, 비철금속, 미용기기, 마켓컬리오아시스 관련주, 타이어, 대형 건설사, 항공사, K-푸드, 화학, 야놀자 관련주, NFT, 밸류업 지수 편입, 금융지주회사, 2차전지 소재, 대두, 건강기능식품, 은행, 화장품 원재료 및 부자재, 화장품 OEM-ODM, 엔터, 스테이블코인, 여행-레저, 게임, 엠폭스, 탄소배출권, 탈모치료, 음식료-유통, 퓨리오사AI 관련주, LNG 발전유통, 화재, 결제서비스, 건자재, 메타버스, 반도체-HBM, 철강 주요업체, 콜드체인, 탈 플라스틱, 의류소재, 건자재-철근, 금강산 관광, LED, 인쇄회로기판(PCB), 배합사료, 유가 상승 수혜-윤활유, 부동산-개발신탁리츠, 폐배터리, OLED-소재부품, 의류 브랜드, 화장품 브랜드, 제지, 전기차-인프라, LPG, CCTV, 전기차 화재, 반도체-디스플레이-클린룸, 스마트폰 부품-소재, 참치 원양어업, 수소차-연료전지, 폐기물처리, 보툴리눔 톡신, 골판지, 미디어 컨텐츠, 렌터카-중고차, 키즈, 바이오-이중항체, STO, 카메라, 마이크로바이옴, 증권사, 전자담배, 스마트홈, 피지컬AI, 치아-임플란트, 방송-언론, 바이오시밀러, 치매치료, 고배당주, 마리화나, 드론-플라잉카, 유전체검사, 비철금속-리튬, 폭염, 클라우드 컴퓨팅, 무선충전, 난임, 초전도체, 밥솥, 교육, 벤처캐피탈, 주정, AI 신약개발, 중소형 건설사, 비만 치료제, 시스템반도체, 페인트, 반도체-전공정 소재, 냉각시스템, 전고체 배터리, 유가 상승 수혜-유류도소매, 세종시, 신용정보, 원격의료, 강관, 반도체-후공정 소재, 인공지능(AI), 의류 OEM-ODM, 지역화폐, 원격근무, 농업-종자비료농약, 음원서비스, CMO-원료의약품, 우크라 재건, 지진, 철강 중소형업체, 의료 AI, 동물백신-방역, 건자재-시멘트레미콘콘크리트, 철도, 2차전지 부품, 풍력, 유아용품, 금은, 빈대퇴치, 수소차-인프라, 전염병-진단, OLED-장비, 골프, 해운, 맥신, MLCC, 방위산업, 남북경협-광물자원개발, 반도체-후공정 장비, 코로나19-제약, 취업일자리, 토스 관련주, 종합반도체, 자전거, 희토류, 택배와 종합물류, 디지털자산-블록체인, 2차전지 생산-판매, 컨택센터, 남북경협-DMZ, 원자력(원전), 자동차 연비개선-경량화, 스마트팜, 건자재-가구, 네옴시티, 희귀질환 치료제, 건자재-거푸집, 자율주행, 유리기판, 황사미세먼지-공기정화, 반도체-전공정 장비, 2차전지 공정장비, 그래핀, 육계주, 피팅 밸브, 남북경협-개성공단, 황사미세먼지-마스크, 딥페이크, 키오스크, 생체인식, 수소차-기타부품, 제조용 로봇/스마트팩토리, 국내 상장한 중국 주, 뉴로모픽 반도체, 스페이스X, 건설기계, IT 보안, 비철금속-구리, 스마트그리드, 광고, 항공우주, 반도체-CXL, 전기차 부품, 페라이트, 면역세포치료제, 농업-농기계, 서비스용 로봇, 줄기세포치료제, 현대-기아차 부품주, 반도체-디스플레이-이송장비, 화학-정유, 5G-6G, 조선 기자재, 엔진(조선-AI), 광섬유-광케이블-광통신, 전력설비, 수술용 로봇, LNG선-기자재, CRO, 조선, 로봇 부품, 양자 기술, 전선-케이블.

Normalize duplicates:
- 비철금속 appears multiple times.
- 남북경험 should likely normalize to 남북경협 if typo detected.
- 화재 should be treated carefully: could be fire insurance, fire accident, or EV fire depending context.
- 전염병/코로나/엠폭스/빈대/마스크 should map to event/one-off unless recurring platform evidence exists.
- AI-related tags should not automatically become high score.

Part B: Add 12 large sector taxonomy

Create or update:
- data/sector_taxonomy/large_sector_v05.yml
- src/e2r/sector/large_sectors.py

Large sectors:
1. 산업재·수주·인프라
2. AI·반도체·전자부품
3. 2차전지·전기차·친환경
4. 소재·스프레드·전략자원
5. 소비재·유통·브랜드
6. 금융·자본배분·디지털금융
7. 바이오·헬스케어·의료기기
8. 플랫폼·콘텐츠·SW·보안
9. 모빌리티·운송·레저
10. 건설·부동산·건자재
11. 정책·지정학·재난·이벤트
12. 농업·생활서비스·기타

Part C: Expand archetype taxonomy to v0.5

Create or update:
- data/sector_taxonomy/archetype_rules_v05.yml
- src/e2r/sector/archetypes.py

Add or confirm these archetypes/sub-archetypes:

Industrial / infrastructure:
- CONTRACT_BACKLOG_INDUSTRIAL
- DEFENSE_GOVERNMENT_BACKLOG
- SHIPBUILDING_OFFSHORE_BACKLOG
- AI_DATA_CENTER_INFRASTRUCTURE
- NUCLEAR_SMR_GRID_POLICY
- RAIL_INFRASTRUCTURE
- GEOPOLITICAL_RECONSTRUCTION
- SMART_FACTORY_AUTOMATION

AI / semiconductor / electronics:
- MEMORY_HBM_CAPACITY
- SEMI_EQUIPMENT_CAPEX
- SEMI_MATERIALS_PROCESS
- ADVANCED_PACKAGING_PCB
- DISPLAY_OLED_EQUIPMENT
- ELECTRONIC_COMPONENTS
- AI_CHIP_FABRIC_INFRA
- CYBER_AI_SECURITY

Battery / EV / green:
- BATTERY_MATERIALS_CAPEX_OVERHEAT
- BATTERY_EQUIPMENT_PARTS
- BATTERY_RECYCLING_ESS_SHIFT
- EV_INFRASTRUCTURE
- HYDROGEN_FUEL_CELL_INFRA
- RENEWABLE_ENERGY_POLICY
- SOLAR_TARIFF_SUPPLYCHAIN
- ENERGY_DISTRIBUTION_FUEL

Materials / spread / strategic:
- REFINING_OIL_SPREAD
- CHEMICAL_SPREAD
- STEEL_METAL_SPREAD
- NONFERROUS_STRATEGIC_METALS
- RARE_METALS_STRATEGIC_MATERIALS
- ADVANCED_MATERIAL_THEMES
- SPECULATIVE_SCIENCE_THEME
- PAPER_PACKAGING
- AGRI_COMMODITY_INPUTS

Consumer / retail / brand:
- EXPORT_RECURRING_CONSUMER
- FOOD_AGRI_LIVESTOCK_CYCLE
- RETAIL_CONVENIENCE_OFFLINE
- ECOMMERCE_FRESH_LOGISTICS
- K_BEAUTY_EXPORT_DISTRIBUTION
- BEAUTY_OEM_ODM_SUPPLYCHAIN
- APPAREL_BRAND_OEM
- HOME_LIVING_APPLIANCE

Financial / capital return / digital finance:
- FINANCIAL_SPREAD_BALANCE_SHEET
- INSURANCE_UNDERWRITING_CYCLE
- SECURITIES_BROKERAGE_CYCLE
- VALUE_UP_SHAREHOLDER_RETURN
- HOLDING_RESTRUCTURING_GOVERNANCE
- PAYMENT_FINTECH_INFRA
- DIGITAL_ASSET_TOKENIZATION

Bio / healthcare:
- BIOTECH_PRE_REVENUE_REGULATORY
- BIOTECH_ROYALTY_COMMERCIALIZATION
- CDMO_HEALTHCARE_CONTRACT
- CRO_CLINICAL_SERVICE
- DIAGNOSTICS_INFECTIOUS_DISEASE
- MEDICAL_DEVICE_HEALTHCARE_EXPORT
- DIGITAL_HEALTHCARE_AI
- CANNABIS_REGULATED_HEALTH

Platform / software / content:
- PLATFORM_SOFTWARE_INTERNET
- GAME_CONTENT_IP
- MEDIA_AD_CONTENT_CYCLE
- METAVERSE_NFT_THEME
- AI_SOFTWARE_APPLICATION
- CLOUD_AI_SOFTWARE_INFRA
- SECURITY_IDENTITY_DEEPFAKE
- EDUCATION_SPECIALTY_SERVICES

Mobility / transport / leisure:
- AIRLINE_TRAVEL_CYCLE
- TRAVEL_LEISURE_REOPENING
- CASINO_DUTYFREE_TOURISM
- SHIPPING_FREIGHT_CYCLE
- AUTO_MOBILITY_COMPLETED_VEHICLE
- AUTO_MOBILITY_COMPONENTS
- TIRE_AUTO_COMPONENT_SPREAD
- RENTAL_USED_CAR_MOBILITY
- URBAN_AIR_DRONE

Construction / real estate / building materials:
- CONSTRUCTION_REAL_ESTATE_CREDIT
- REIT_DEVELOPMENT_TRUST
- BUILDING_MATERIALS_CYCLE
- INFRA_RECONSTRUCTION_POLICY
- DISASTER_REBUILD_EVENT

Policy / event:
- NORTH_KOREA_POLICY_EVENT
- CLIMATE_DISASTER_EVENT
- EVENT_DISEASE_PEST_DEMAND
- POLICY_LOCAL_THEME
- ONE_OFF_EVENT_DEMAND
- THEME_VALUATION_OVERHEAT

Agriculture / lifestyle / services:
- SMART_FARM_AGRI_TECH
- AGRI_LIVESTOCK_FOOD_COMMODITY
- HOME_CHILD_EDUCATION
- WASTE_RECYCLING_ENVIRONMENT
- SERVICE_KIOSK_AUTOMATION
- CONSUMER_REGULATED_PRODUCT

Part D: Build theme_tag_map_v05.csv

Create:
- data/sector_taxonomy/theme_tag_map_v05.csv
- data/sector_taxonomy/theme_aliases_v05.yml

CSV columns:
- raw_theme_tag
- normalized_theme_tag
- large_sector
- primary_archetype
- secondary_archetypes
- green_policy
- must_have_evidence
- red_flag_evidence
- score_weight_profile
- default_stage_bias
- query_seed_terms
- notes

Allowed green_policy:
- green_allowed
- watch_to_green
- watch_only
- red_watch
- event_only
- red_flag

Allowed default_stage_bias:
- stage1_radar
- stage2_candidate
- stage3_possible
- stage3_rare
- stage3_red_bias
- event_only
- red_team_first

Important mapping principles:
- theme tag itself must not create score.
- theme tag can generate search queries and evidence expectations.
- Green requires evidence, not theme membership.
- red_flag/event themes may still be useful, but mostly for 4B/4C and RedTeam.

Part E: Run unmatched audit

Add:
- src/e2r/cli/audit_theme_tag_coverage.py
- src/e2r/sector/theme_tag_mapper.py
- tests/test_theme_tag_mapper.py

Command:
PYTHONPATH=src python -m e2r.cli.audit_theme_tag_coverage \
  --raw-tags data/sector_taxonomy/raw_theme_tags_v05.csv \
  --map data/sector_taxonomy/theme_tag_map_v05.csv \
  --output output/theme_tag_coverage_v05

Audit outputs:
- output/theme_tag_coverage_v05/theme_coverage_report.md
- output/theme_tag_coverage_v05/unmatched_theme_tags.csv
- output/theme_tag_coverage_v05/ambiguous_theme_tags.csv
- output/theme_tag_coverage_v05/green_policy_distribution.csv
- output/theme_tag_coverage_v05/archetype_distribution.csv
- output/theme_tag_coverage_v05/large_sector_distribution.csv

Required report answers:
- total raw tags
- normalized tags
- mapped tags
- unmatched tags
- ambiguous tags
- duplicate aliases
- green_allowed count
- watch_to_green count
- watch_only count
- red_watch count
- event_only count
- red_flag count
- top under-covered archetypes

Done condition:
- unmatched_theme_tags must be zero or explicitly explained with proposed new archetype/alias.
- Ambiguous tags must be listed for manual review.

Part F: Add score-weight profile v0.5

Create:
- data/sector_taxonomy/score_weight_profiles_v05.yml
- docs/score_weight_profiles_v05.md

Do not apply these to production scoring yet.
Use only for research/shadow scoring.

Base dimensions:
- eps_fcf
- structural_visibility
- bottleneck_pricing
- market_mispricing
- valuation_rerating
- capital_allocation
- information_confidence
- risk_penalty

Profiles:

GREEN-ELIGIBLE STRUCTURAL:
CONTRACT_BACKLOG_INDUSTRIAL:
  eps_fcf: 20
  structural_visibility: 24
  bottleneck_pricing: 22
  market_mispricing: 12
  valuation_rerating: 12
  capital_allocation: 1
  information_confidence: 5
  risk_penalty: medium

AI_DATA_CENTER_INFRASTRUCTURE:
  eps_fcf: 22
  structural_visibility: 23
  bottleneck_pricing: 20
  market_mispricing: 14
  valuation_rerating: 12
  capital_allocation: 0
  information_confidence: 5
  risk_penalty: medium_high

EXPORT_RECURRING_CONSUMER:
  eps_fcf: 22
  structural_visibility: 23
  bottleneck_pricing: 12
  market_mispricing: 16
  valuation_rerating: 13
  capital_allocation: 0
  information_confidence: 5
  risk_penalty: medium

K_BEAUTY_EXPORT_DISTRIBUTION and BEAUTY_OEM_ODM_SUPPLYCHAIN:
  eps_fcf: 22
  structural_visibility: 23
  bottleneck_pricing: 12
  market_mispricing: 16
  valuation_rerating: 13
  capital_allocation: 0
  information_confidence: 5
  risk_penalty: inventory_receivables_china_dependency

MEMORY_HBM_CAPACITY:
  eps_fcf: 24
  structural_visibility: 21
  bottleneck_pricing: 19
  market_mispricing: 15
  valuation_rerating: 12
  capital_allocation: 0
  information_confidence: 5
  risk_penalty: cycle_capex_reversal

CDMO_HEALTHCARE_CONTRACT:
  eps_fcf: 20
  structural_visibility: 24
  bottleneck_pricing: 12
  market_mispricing: 12
  valuation_rerating: 12
  capital_allocation: 0
  information_confidence: 5
  risk_penalty: litigation_capacity_utilization

FINANCIAL_SPREAD_BALANCE_SHEET / INSURANCE_UNDERWRITING_CYCLE:
  eps_fcf: 15
  structural_visibility: 20
  bottleneck_pricing: 5
  market_mispricing: 15
  valuation_rerating: 25
  capital_allocation: 10
  information_confidence: 5
  risk_penalty: credit_underwriting_capital

WATCH / YELLOW:
PLATFORM_SOFTWARE_INTERNET:
  eps_fcf: 20
  structural_visibility: 22
  bottleneck_pricing: 8
  market_mispricing: 16
  valuation_rerating: 14
  capital_allocation: 0
  information_confidence: 5
  risk_penalty: regulation_ai_cost_governance

ROBOTICS_FACTORY_AUTOMATION:
  eps_fcf: 18
  structural_visibility: 15
  bottleneck_pricing: 10
  market_mispricing: 12
  valuation_rerating: 10
  capital_allocation: 0
  information_confidence: 5
  risk_penalty: monetization_failure_theme

DIGITAL_ASSET_TOKENIZATION:
  eps_fcf: 16
  structural_visibility: 18
  bottleneck_pricing: 8
  market_mispricing: 16
  valuation_rerating: 12
  capital_allocation: 3
  information_confidence: 5
  risk_penalty: regulation_security_adoption

HYDROGEN_FUEL_CELL_INFRA / RENEWABLE_ENERGY_POLICY:
  eps_fcf: 18
  structural_visibility: 18
  bottleneck_pricing: 12
  market_mispricing: 12
  valuation_rerating: 10
  capital_allocation: 0
  information_confidence: 5
  risk_penalty: policy_subsidy_supply_chain

RETAIL_CONVENIENCE_OFFLINE / ECOMMERCE_FRESH_LOGISTICS:
  eps_fcf: 18
  structural_visibility: 16
  bottleneck_pricing: 5
  market_mispricing: 14
  valuation_rerating: 14
  capital_allocation: 3
  information_confidence: 5
  risk_penalty: logistics_inventory_competition

RED / 4B DEFENSE:
SHIPPING_FREIGHT_CYCLE:
  eps_fcf: 20
  structural_visibility: 8
  bottleneck_pricing: 18
  market_mispricing: 8
  valuation_rerating: 8
  capital_allocation: 0
  information_confidence: 5
  risk_penalty: very_high_cycle

CHEMICAL_SPREAD:
  eps_fcf: 20
  structural_visibility: 8
  bottleneck_pricing: 16
  market_mispricing: 8
  valuation_rerating: 8
  capital_allocation: 0
  information_confidence: 5
  risk_penalty: oversupply_china

BATTERY_MATERIALS_CAPEX_OVERHEAT:
  eps_fcf: 20
  structural_visibility: 16
  bottleneck_pricing: 14
  market_mispricing: 10
  valuation_rerating: 10
  capital_allocation: 0
  information_confidence: 5
  risk_penalty: very_high_capex_overheat

CONSTRUCTION_REAL_ESTATE_CREDIT:
  eps_fcf: 18
  structural_visibility: 10
  bottleneck_pricing: 8
  market_mispricing: 12
  valuation_rerating: 10
  capital_allocation: 0
  information_confidence: 5
  risk_penalty: very_high_credit_pf

EVENT_DISEASE_PEST_DEMAND:
  eps_fcf: 20
  structural_visibility: 5
  bottleneck_pricing: 5
  market_mispricing: 5
  valuation_rerating: 5
  capital_allocation: 0
  information_confidence: 5
  risk_penalty: extreme_one_off

SPECULATIVE_SCIENCE_THEME:
  eps_fcf: 5
  structural_visibility: 5
  bottleneck_pricing: 5
  market_mispricing: 5
  valuation_rerating: 5
  capital_allocation: 0
  information_confidence: 3
  risk_penalty: extreme_theme

Part G: Expand case library v03

Create:
- data/e2r_case_library/cases_v03.jsonl

Add cases for newly mapped/under-covered archetypes.
Cases may have unknown prices initially, but must not fabricate dates/prices.

Required case groups:

HBM / memory:
- sk_hynix_hbm_rerating
- sk_hynix_hbm_4b_watch
- samsung_memory_recovery
- simple_dram_rebound_counterexample

Chemical / spread:
- lotte_chemical_oversupply_2024
- lg_chem_petrochemical_oversupply_2024
- refining_spread_recovery_candidate
- chemical_china_supply_glut_4c

Battery / ESS:
- gm_lg_ohio_ev_demand_slowdown
- lg_energy_solution_ess_shift
- ecopro_bm_2023_overheat
- battery_capa_overbuild_4c

CDMO / healthcare:
- samsung_biologics_us_capacity_candidate
- celltrion_biosimilar_candidate
- cdmo_capacity_underutilization_4c
- patent_litigation_delay_4c

Digital finance:
- toss_won_stablecoin_candidate
- sto_law_expectation_without_revenue_counterexample
- crypto_theme_no_revenue_counterexample
- stablecoin_regulatory_delay_4c

Governance / strategic metals:
- korea_zinc_tender_event_premium
- korea_zinc_governance_risk
- sk_square_valueup_candidate
- buyback_without_cancellation_counterexample

Construction / PF:
- korea_pf_stress_2024
- builder_liquidity_support_relief_rally
- overseas_infra_margin_contract_candidate
- construction_cost_overrun_4c

Retail / e-commerce:
- convenience_store_efficiency_candidate
- cold_chain_recurring_logistics_candidate
- ecommerce_fresh_loss_counterexample
- china_direct_purchase_margin_pressure_counterexample

Beauty:
- kbeauty_oem_odm_export_candidate
- silicontwo_export_distribution_candidate
- kbeauty_channel_stuffing_4c
- china_dependency_cosmetic_counterexample

Renewable / hydrogen:
- hyundai_hydrogen_fuel_cell_plant_candidate
- hydrogen_theme_no_revenue_counterexample
- solar_tariff_supply_chain_4c
- wind_project_delay_4c

Event / speculative:
- seegene_2020_one_off
- infectious_disease_event_oneoff
- superconductor_theme_counterexample
- graphene_mxene_no_revenue_counterexample

For each case:
- include large_sector
- primary_archetype
- secondary_archetypes
- case_type
- evidence summary
- must_have_fields
- red_flag_fields
- score_weight_hint
- green_guardrails
- source_refs if available
- price_validation with nulls if not yet backfilled
- price_validation_status = needs_price_backfill if prices missing

Part H: Add deep research evidence index

Create:
- data/e2r_case_library/evidence_index_v03.jsonl
- output/e2r_case_library_v03/deep_research_evidence_index.md

For each case, store:
- case_id
- source_title
- source_type: official_disclosure / broker_report / news / academic / company_ir / other
- published_at
- url_or_ref
- evidence_summary
- evidence_fields_supported
- supports_success_or_counterexample
- confidence

No long copyrighted excerpts.
Summarize only.

Part I: Price-path validation remains required

Do not claim case alignment until price path is filled.

Update:
- src/e2r/sector/case_price_backfill.py
- src/e2r/sector/score_price_alignment.py

Required outputs:
- stage1_price
- stage2_price
- stage3_price
- stage4b_price
- stage4c_price
- peak_price
- MFE_90D
- MFE_180D
- MFE_1Y
- MAE_90D
- MAE_180D
- MAE_1Y
- drawdown_after_peak
- below_stage3_price_flag
- price_validation_status

If price data missing:
- leave null
- set missing_price_data
- do not invent

Part J: Shadow normalization only

Create:
- src/e2r/sector/shadow_score_normalizer.py
- tests/test_shadow_score_normalizer.py
- output/e2r_case_library_v03/shadow_score_profile_report.md

Shadow normalizer:
- reads cases_v03
- reads score_weight_profiles_v05
- computes hypothetical archetype score profiles
- does not affect production StageClassifier
- compares score direction with score_price_alignment if price data exists
- marks insufficient_validation if price data missing

Do not modify:
- src/e2r/staging.py production thresholds
- src/e2r/features.py production score weights
unless only adding diagnostics, never changing production output.

Part K: Reports

Create:
- output/theme_tag_coverage_v05/theme_coverage_report.md
- output/theme_tag_coverage_v05/unmatched_theme_tags.csv
- output/theme_tag_coverage_v05/ambiguous_theme_tags.csv
- output/theme_tag_coverage_v05/green_policy_distribution.csv
- output/theme_tag_coverage_v05/archetype_distribution.csv

Create:
- output/e2r_case_library_v03/case_coverage_summary.md
- output/e2r_case_library_v03/archetype_case_matrix.csv
- output/e2r_case_library_v03/score_weight_profiles_v05_summary.md
- output/e2r_case_library_v03/price_validation_gap_report.md
- output/e2r_case_library_v03/green_guardrail_summary.md
- output/e2r_case_library_v03/production_scoring_not_ready.md

Reports must answer:
- Are all raw theme tags mapped?
- Which tags are ambiguous?
- Which archetypes have 2+ success/candidate and 2+ counterexample/risk cases?
- Which archetypes remain under-covered?
- Which Green policies dominate?
- Which themes are Green-restricted?
- Which cases require price backfill?
- Which score-weight profiles are still unvalidated?
- Why production scoring must not be changed yet.

Part L: Tests

Required tests:
- raw theme list is parsed
- theme aliases normalize duplicates
- every raw theme tag maps to a primary_archetype or appears in unmatched
- unmatched audit writes CSV and markdown
- green_policy values are valid
- score_weight_profiles_v05 validates dimensions
- cases_v03 validates schema
- evidence_index_v03 validates schema
- case library is not imported by production scoring modules
- shadow normalizer does not modify StageClassifier
- event_only/red_flag themes cannot create Green in shadow policy
- missing price data is not invented
- existing tests pass

Part M: Commands to run

PYTHONPATH=src python -m e2r.cli.audit_theme_tag_coverage \
  --raw-tags data/sector_taxonomy/raw_theme_tags_v05.csv \
  --map data/sector_taxonomy/theme_tag_map_v05.csv \
  --output output/theme_tag_coverage_v05

PYTHONPATH=src python -m e2r.cli.backfill_case_price_paths \
  --cases data/e2r_case_library/cases_v03.jsonl \
  --price-root data/historical_official/prices \
  --output data/e2r_case_library/cases_v03_price_filled.jsonl

PYTHONPATH=src python -m e2r.cli.run_shadow_score_normalizer \
  --cases data/e2r_case_library/cases_v03_price_filled.jsonl \
  --profiles data/sector_taxonomy/score_weight_profiles_v05.yml \
  --output output/e2r_case_library_v03/shadow_score_profile_report.md

Part N: Docs

Create:
- docs/checkpoints/checkpoint_28a_3_theme_map_unmatched_audit.md
- docs/theme_tag_map_v05.md
- docs/score_weight_profiles_v05.md
- docs/production_scoring_not_ready.md

Checkpoint report must explain:
1. Theme absorption status.
2. Raw theme count.
3. Mapped count.
4. Unmatched count.
5. Ambiguous count.
6. Large sector distribution.
7. Archetype distribution.
8. Green policy distribution.
9. Case coverage status.
10. Why production scoring is still too early.
11. What remains before Checkpoint 28B.

Constraints:
- No API keys in output.
- No fabricated evidence.
- No fabricated dates.
- No fabricated prices.
- No buy/sell recommendation wording.
- Do not apply score profiles to production scoring.
- Do not use case records as candidate-generation input.
- Do not let theme tags directly create scores.
- Preserve E2R / SeoSaengWon principle.
- All tests must pass.

Done when:
- theme_tag_map_v05.csv exists
- unmatched audit exists
- unmatched tags are zero or explicitly documented
- cases_v03.jsonl exists
- score_weight_profiles_v05.yml exists
- evidence_index_v03.jsonl exists
- shadow normalizer exists
- reports exist
- docs/checkpoints/checkpoint_28a_3_theme_map_unmatched_audit.md exists
- all tests pass
```

---

# 짧은 정리

이번 체크포인트는 **점수를 고치는 단계가 아니라, 점수를 고치기 전에 필요한 지도를 완성하는 단계**야.

해야 하는 일은 세 가지다.

```text
1. 네가 준 테마 전부를 theme_tag_map_v05.csv로 매핑
2. unmatched audit로 테마 흡수율 100% 확인
3. 성공/반례/주가검증 기반으로 score_weight_profiles_v05를 shadow mode로만 검증
```

이게 끝나면 다음에야 Checkpoint 28B에서:

```text
archetype-aware sector-normalized scoring
```

을 production이 아니라 shadow로 먼저 돌려볼 수 있어.

[1]: https://www.reuters.com/world/asia-pacific/sk-hynix-flooded-with-unprecedented-offers-big-tech-firms-secure-chip-supplies-2026-05-07/?utm_source=chatgpt.com "SK Hynix flooded with unprecedented offers from big tech firms to secure chip supplies"
[2]: https://www.reuters.com/markets/commodities/south-korean-petrochemical-firms-profits-plunge-2024-oversupply-persists-2025-02-07/?utm_source=chatgpt.com "South Korean petrochemical firms' profits plunge in 2024 as oversupply persists"
[3]: https://www.reuters.com/legal/litigation/gms-restart-date-ohio-battery-plant-uncertain-2026-05-12/?utm_source=chatgpt.com "GM-LG's restart date at Ohio battery plant uncertain"
[4]: https://www.reuters.com/business/healthcare-pharmaceuticals/samsung-biologics-buy-us-drug-production-facility-gsk-280-mln-2025-12-21/?utm_source=chatgpt.com "Samsung Biologics to buy US drug production facility from GSK for $280 million"
[5]: https://www.reuters.com/business/finance/south-korean-fintech-toss-plans-global-push-starting-australia-aims-issue-won-2025-09-09/?utm_source=chatgpt.com "South Korean fintech Toss plans global push starting in Australia, aims to issue won stablecoin"
[6]: https://www.reuters.com/markets/deals/private-equity-mbk-young-poong-launch-15-bln-tender-offer-korea-zinc-shares-2024-09-13/?utm_source=chatgpt.com "Private equity MBK, Young Poong launch $1.5 bln tender offer for Korea Zinc shares"
[7]: https://www.reuters.com/markets/asia/south-korea-tightens-scrutiny-speed-up-real-estate-restructuring-2024-05-13/?utm_source=chatgpt.com "South Korea tightens scrutiny to speed up real estate restructuring"
