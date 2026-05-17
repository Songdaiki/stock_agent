응. 지금은 **더 파기 전에 한 번 지도를 고정해야 하는 시점**이 맞다.

정리하면 우리가 만든 구조는 이렇게 잡으면 된다.

```text
12개 대섹터
→ 약 70개 canonical archetype
→ 이후 딥서치로 추가된 90~110개 deep sub-archetype
→ 200개+ raw theme tag
→ 성공/반례 case library
→ 가격 경로 검증
→ shadow score 정규화
```

중요한 건 대섹터를 계속 늘리는 게 아니라, **12개 대섹터는 고정**하고 그 아래에서 canonical archetype과 deep sub-archetype을 부모-자식 구조로 관리하는 거야. 업로드된 Theme Tag Map v0.5도 12개 대섹터별로 테마를 primary archetype과 Green 정책으로 흡수하는 구조였고, 산업재·AI반도체·2차전지·소재·소비재·금융·바이오·플랫폼·모빌리티·건설·정책이벤트·농업생활서비스로 정리되어 있었다.

그리고 이 전체 구조의 기준은 계속 서생원식 원칙이다. 즉, 단순 테마가 아니라 **산업 구조 변화 → EPS/FCF 체급 변화 → 시장의 과거 프레임 오해 → 밸류에이션 리레이팅**을 찾는 구조다.
공시·리포트에서 계약금액, 계약기간, 매출 대비 계약금액 같은 값이 없으면 추정해서 채우면 안 되고, 실제로 확인된 필드만 써야 한다는 원칙도 유지해야 한다.

---

# 0. 앞으로의 사용 방식

앞으로 네가 이렇게 말하면:

```text
다음 라운드 진행해줘.
그 라운드의 대섹터, archetype, case를 기준으로
성공/반례와 실제 가격 경로까지 확인해서 점수정규화해줘.
```

나는 아래 순서에 맞춰 자동으로 넘어가면 된다.

```text
R1 산업재·수주·인프라
R2 AI·반도체·전자부품
R3 2차전지·전기차·친환경
R4 소재·스프레드·전략자원
R5 소비재·유통·브랜드
R6 금융·자본배분·디지털금융
R7 바이오·헬스케어·의료기기
R8 플랫폼·콘텐츠·SW·보안
R9 모빌리티·운송·레저
R10 건설·부동산·건자재
R11 정책·지정학·재난·이벤트
R12 농업·생활서비스·기타
R13 Cross-archetype RedTeam / 4B / 회계신뢰도 / 가격검증 총정리
```

---

# 1. 전체 검증 공통 프로토콜

각 라운드마다 같은 방식으로 검증한다.

## 1단계: case 정리

각 archetype마다 최소한 아래를 채운다.

```text
성공사례 2개 이상
성공후보 2개 이상
반례 2개 이상
4B-watch 사례 1개 이상
4C-thesis-break 사례 1개 이상
```

단, 모든 archetype에 억지로 2개씩 넣지는 않는다. **증거가 부족하면 부족하다고 표시**해야 한다.

## 2단계: stage date 후보

각 case마다 날짜를 잡는다.

```text
Stage 1:
테마·산업 변화 최초 포착일

Stage 2:
실제 공시, 계약, 수주, 실적, 리포트, EPS 상향 확인일

Stage 3:
중장기 EPS/FCF 상향 + valuation frame 전환 확인일

Stage 4B:
리레이팅 과열, 모두가 인정, valuation 포화, crowded trade

Stage 4C:
논리 훼손, 계약 취소, EPS 하향, 회계·규제·신뢰도 붕괴
```

## 3단계: 가격 경로 검증

각 case마다 아래를 확인한다.

```text
stage1_price
stage2_price
stage3_price
peak_price
stage4b_price
stage4c_price

MFE_30D / 90D / 180D / 1Y / 2Y
MAE_30D / 90D / 180D / 1Y
drawdown_after_peak
below_stage3_price_flag
```

## 4단계: score-price alignment 판정

```text
aligned:
점수 높게 준 증거 이후 EPS/FCF와 주가가 같이 리레이팅

false_positive_score:
점수는 높게 나왔지만 주가 리레이팅 실패

price_moved_without_evidence:
주가는 올랐지만 EPS/FCF 증거 없음

evidence_good_but_price_failed:
증거는 좋아 보였지만 시장이 리레이팅하지 않음

cyclical_success:
수익은 났지만 구조적 E2R이 아니라 사이클 성공

event_premium:
정책·공개매수·테마 이벤트로 오른 것

thesis_break:
4C로 논리 훼손
```

## 5단계: 점수비중 교정

성공사례는 가중치를 강화한다.

```text
성공사례가 많으면:
EPS/FCF
structural_visibility
bottleneck_pricing
market_mispricing
valuation_rerating
```

반례는 감점축과 Green gate를 강화한다.

```text
반례가 많으면:
risk_penalty 강화
Green 제한
Stage 3 진입 조건 강화
4B/4C 조기 탐지 조건 추가
```

---

# 2. R1 — 산업재·수주·인프라

## 대섹터

```text
산업재·수주·인프라
```

## canonical archetype

```text
CONTRACT_BACKLOG_INDUSTRIAL
GRID_TRANSFORMER_SHORTAGE
DEFENSE_GOVERNMENT_BACKLOG
DEFENSE_TECH_AUTONOMOUS_SYSTEMS
DEFENSE_DRONE_COUNTER_UAS
DEFENSE_AI_SOFTWARE_INTELLIGENCE
SHIPBUILDING_OFFSHORE_BACKLOG
RAIL_INFRASTRUCTURE
NUCLEAR_SMR_GRID_POLICY
GEOPOLITICAL_RECONSTRUCTION
SMART_FACTORY_AUTOMATION
AI_DATA_CENTER_POWER_EQUIPMENT
```

## deep sub-archetype

```text
전력설비·변압기
전선·케이블
피팅밸브
조선 기자재
LNG선 기자재
방산 AI
드론·counter-UAS
컨테이너형 미사일
군사용 AI software
철도 수출
원전 PPA
SMR
데이터센터 UPS/PDU/switchgear
```

## 검증 핵심

이 라운드는 **Green 가능 archetype이 많다.**
하지만 수주 뉴스만으로는 부족하고:

```text
계약금액/매출 비중
계약기간
수주잔고
납품 스케줄
마진
OP/EPS 상향
```

이 같이 확인되어야 한다.

## 가격 경로 기대

```text
성공형:
Stage 2 계약/실적 확인 후 6~24개월 stair-step rerating

반례형:
수주 뉴스 후 주가만 오르고 마진·EPS가 안 따라오면 false_positive
```

---

# 3. R2 — AI·반도체·전자부품

## 대섹터

```text
AI·반도체·전자부품
```

## canonical archetype

```text
MEMORY_HBM_CAPACITY
COMMODITY_MEMORY_GENERAL_SEMI
SEMI_EQUIPMENT_CAPEX
SEMI_MATERIALS_PROCESS
ADVANCED_PACKAGING_PCB
ADVANCED_PACKAGING_COWOS_EMIB
DISPLAY_OLED_SUPPLYCHAIN
ELECTRONIC_COMPONENTS_MLCC_SENSOR
AI_CHIP_FABRIC_INFRA
AI_ACCELERATOR_CHIP_PUREPLAY
AI_SERVER_ODM_EMS_SUPPLY_CHAIN
NEOCLOUD_GPU_RENTAL
OPTICAL_NETWORKING_AI_DATACENTER
INDUSTRIAL_GASES_SEMICONDUCTOR_INFRA
AI_DATA_CENTER_INFRASTRUCTURE
AI_DATA_CENTER_COOLING
DATA_CENTER_REIT_INFRASTRUCTURE
AI_GRID_FLEXIBILITY_SOFTWARE
REDTEAM_ACCOUNTING_TRUST_OVERLAY
```

## deep sub-archetype

```text
HBM
범용 DRAM/NAND
AI 서버 ODM/EMS
GPU cloud / neocloud
CoWoS / EMIB / advanced packaging
EUV / 반도체 장비
반도체용 산업가스
AI 데이터센터 냉각
광통신·광케이블
데이터센터 REIT
AI grid flexibility
AI accelerator pure-play
CXL
유리기판
뉴로모픽
```

## 검증 핵심

AI·반도체는 가장 중요하지만 가장 위험하기도 하다.

```text
HBM:
Green 가능성이 높음.

AI 서버 ODM:
수요는 강하지만 저마진·재고·회계 리스크 큼.

Neocloud:
take-or-pay visibility는 있으나 고부채·GPU 감가상각 리스크 큼.

Advanced packaging:
병목은 강하지만 CAPEX cycle과 병목 완화 리스크 있음.

AI chip pure-play:
실제 고객·양산·매출 전까지 대부분 Watch/Red.
```

## 가격 경로 기대

```text
성공형:
EPS revision과 valuation multiple이 동시에 상승

4B형:
이미 1~2년 급등, 모두가 AI rerating 인정, crowded trade

4C형:
감사인 사임, filing delay, CAPEX cut, 고객사 주문 취소
```

---

# 4. R3 — 2차전지·전기차·친환경

## 대섹터

```text
2차전지·전기차·친환경
```

## canonical archetype

```text
BATTERY_MATERIALS_CAPEX_OVERHEAT
BATTERY_EQUIPMENT_PARTS
BATTERY_RECYCLING_ESS_SHIFT
EV_INFRASTRUCTURE
HYDROGEN_FUEL_CELL_INFRA
RENEWABLE_ENERGY_POLICY
SOLAR_TARIFF_SUPPLYCHAIN
ENERGY_DISTRIBUTION_FUEL
WASTE_RECYCLING_ENVIRONMENT
CARBON_CREDIT_CBAM_COMPLIANCE
DATA_CENTER_WATER_REUSE_INFRA
```

## deep sub-archetype

```text
2차전지 소재
2차전지 부품
2차전지 공정장비
폐배터리
ESS 전환
전고체 배터리
수소연료전지
태양광 관세·공급망
풍력 프로젝트
탄소배출권/CBAM
폐기물처리
탈플라스틱
데이터센터 물 재활용
```

## 검증 핵심

이 라운드는 **Green보다 과열 방어가 우선**이다.

```text
폐기물처리:
허가권·처리시설·반복 FCF가 있으면 Green 가능.

2차전지 소재:
EV 수요 둔화, CAPA 과잉, 광물가격이 hard risk.

수소/태양광:
정책 뉴스가 아니라 실제 CAPEX·가동률·OP 전환 필요.

탄소배출권:
탄소가격 exposure가 아니라 비용 전가력·탄소회계 매출을 봐야 함.
```

## 가격 경로 기대

```text
성공형:
실제 계약·가동률·FCF가 확인된 뒤 완만한 리레이팅

반례형:
정책/보조금/테마로 급등 후 CAPA·수요·가격 문제로 drawdown
```

---

# 5. R4 — 소재·스프레드·전략자원

## 대섹터

```text
소재·스프레드·전략자원
```

## canonical archetype

```text
REFINING_OIL_SPREAD
CHEMICAL_SPREAD
STEEL_METAL_SPREAD
NONFERROUS_STRATEGIC_METALS
RARE_METALS_STRATEGIC_MATERIALS
LITHIUM_BATTERY_RAW_MATERIAL
PRECIOUS_METALS_SAFE_HAVEN_MINERS
ADVANCED_MATERIAL_SPECULATIVE_THEME
PAPER_PACKAGING_CYCLE
AGRI_COMMODITY_INPUTS
LNG_ENERGY_TRADING_DISTRIBUTION
GENERAL_TRADING_RESOURCE_INFRA
ENERGY_UTILITY_LNG_GAS
```

## deep sub-archetype

```text
정유
화학
철강
비철금속
구리
리튬
희토류
금은
금광주
페라이트
그래핀
맥신
초전도체
제지·골판지
종합상사
LNG 장기계약
가스 유틸리티
```

## 검증 핵심

이 라운드는 대부분 cycle과 구조를 분리해야 한다.

```text
화학:
공급과잉 때문에 Green 제한.

리튬:
가격 반등만으로 Green 금지.

희토류:
정부지원·offtake·가격 floor가 있으면 Watch-to-Green.

금광주:
금 가격 + AISC + FCF + 자본환원 확인.

종합상사:
단순 무역 매출이 아니라 자원권·장기계약·자본배분이 핵심.
```

## 가격 경로 기대

```text
대부분:
cyclical_success와 structural_success를 분리

검증:
commodity price peak와 종목 peak 비교
EPS peak 이후 drawdown
다음 회계연도 EPS 정상화 여부
```

---

# 6. R5 — 소비재·유통·브랜드

## 대섹터

```text
소비재·유통·브랜드
```

## canonical archetype

```text
EXPORT_RECURRING_CONSUMER
FOOD_AGRI_LIVESTOCK_CYCLE
RETAIL_CONVENIENCE_OFFLINE
RETAIL_ECOMMERCE_LOGISTICS
ECOMMERCE_FRESH_LOGISTICS
COLD_CHAIN_REIT_LOGISTICS
K_BEAUTY_EXPORT_DISTRIBUTION
BEAUTY_OEM_ODM_SUPPLYCHAIN
APPAREL_FAST_FASHION_BRAND_OEM
HOME_LIVING_APPLIANCE_RENTAL
CONSUMER_REGULATED_PRODUCT
```

## deep sub-archetype

```text
라면
K푸드
건강기능식품
편의점
홈쇼핑
마켓컬리·오아시스
콜드체인
K뷰티 브랜드
화장품 OEM/ODM
화장품 원재료
의류 브랜드
fast fashion
밥솥·생활가전
렌탈
전자담배
주정
```

## 검증 핵심

이 라운드는 Green 가능과 Watch가 섞여 있다.

```text
K푸드/K뷰티:
Green 가능. 수출, 채널, 반복소비, OPM, 재고/채권 안정이 핵심.

편의점:
점포 수가 아니라 SSSG, PB mix, OPM, FCF.

이커머스:
매출 성장보다 물류비, FCF, 규제, 데이터 보안.

의류:
재고·할인율·IP·초저가 경쟁 때문에 보수적.

생활가전:
hardware cycle이면 Watch/Red, 렌탈 반복매출이면 Watch-to-Green.
```

## 가격 경로 기대

```text
성공형:
수출/채널/OPM 상향 후 straight 또는 stair-step rerating

반례형:
viral/product hype 후 재고·채권·리콜·규제로 drawdown
```

---

# 7. R6 — 금융·자본배분·디지털금융

## 대섹터

```text
금융·자본배분·디지털금융
```

## canonical archetype

```text
FINANCIAL_SPREAD_BALANCE_SHEET
INSURANCE_UNDERWRITING_CYCLE
SECURITIES_BROKERAGE_CYCLE
VALUE_UP_SHAREHOLDER_RETURN
HOLDING_RESTRUCTURING_GOVERNANCE
PAYMENT_FINTECH_INFRA
DIGITAL_ASSET_TOKENIZATION
```

## deep sub-archetype

```text
은행
금융지주
손해보험
생명보험
증권사
VC
고배당
밸류업
자사주 소각
부동산 자산 보유
결제서비스
PG
e-wallet
신용정보
토스 관련주
STO
스테이블코인
NFT와의 분리
```

## 검증 핵심

```text
은행·보험:
Green 가능. ROE, CET1/K-ICS, CSM, 손해율, 환원정책.

증권:
거래대금·IB cycle이 강해서 Watch 중심.

밸류업:
지수 편입이 아니라 실제 소각·배당·ROE/NAV 개선.

결제/PG:
사용자 수가 아니라 거래액, take rate, FCF.

스테이블코인/STO:
규제 승인, 실제 발행량, 거래량, 수익모델 전까지 Green 금지.
```

## 가격 경로 기대

```text
보험/은행:
PBR-ROE rerating 확인

증권:
거래대금 peak 이후 drawdown 확인

밸류업:
소각·배당 실행일 이후 PBR band 변화 확인

디지털금융:
법안 뉴스와 실제 수익화 구분
```

---

# 8. R7 — 바이오·헬스케어·의료기기

## 대섹터

```text
바이오·헬스케어·의료기기
```

## canonical archetype

```text
CDMO_HEALTHCARE_CONTRACT
CRO_CLINICAL_SERVICE
BIOSIMILAR_COMMERCIALIZATION
BIOSIMILAR_ORIGINATOR_DEFENSE
OBESITY_GLP1_COMMERCIALIZATION
GENE_THERAPY_RARE_DISEASE
AI_DRUG_DISCOVERY_PLATFORM
DIGITAL_HEALTHCARE_AI
DIGITAL_HEALTHCARE_REMOTE_MEDICINE
TELEHEALTH_BEHAVIORAL_HEALTH
PHARMA_CHANNEL_AND_PRIVACY_RISK
MEDICAL_DEVICE_HEALTHCARE_EXPORT
MEDICAL_DEVICE_DENTAL_IMPLANT
DIAGNOSTICS_INFECTIOUS_DISEASE
ANIMAL_HEALTH_BIOSECURITY
```

## deep sub-archetype

```text
CDMO
CRO
바이오시밀러
오리지널 특허방어
GLP-1 비만치료제
유전자치료제
희귀질환
AI 신약개발
의료AI
원격의료
온라인 정신건강
약물 플랫폼·조제약
미용기기
보톡스
치아·임플란트
진단키트
동물백신·방역
```

## 검증 핵심

```text
CDMO:
Green 가능. 장기계약, capacity, 가동률.

의료기기:
Green 가능. 수출국, 반복 시술/소모품, OPM.

바이오시밀러:
허가만으로 부족. 처방전환, PBM/보험, 마진.

GLP-1:
수요는 구조적이나 경쟁·보험·조제약·광고규제 확인.

유전자치료제:
승인 후에도 상업화 실패 가능. Green 매우 제한.

AI 신약개발:
대부분 Watch/Red. 플랫폼 narrative보다 milestone과 임상.

원격의료:
CAC, privacy, reimbursement, B2B 계약.
```

## 가격 경로 기대

```text
의료기기/CDMO:
실적·계약 기반 리레이팅 가능

바이오시밀러/GLP-1:
허가·처방량·보험 등재 후 가격 경로 확인

AI신약/유전자치료:
승인·임상 뉴스 후 MAE/drawdown 중점 확인
```

---

# 9. R8 — 플랫폼·콘텐츠·SW·보안

## 대섹터

```text
플랫폼·콘텐츠·SW·보안
```

## canonical archetype

```text
PLATFORM_SOFTWARE_INTERNET
CLOUD_AI_SOFTWARE_INFRA
AI_SOFTWARE_APPLICATION
CONTACT_CENTER_AI_AUTOMATION
SERVICE_KIOSK_SELF_CHECKOUT
GAME_CONTENT_IP
MEDIA_AD_CONTENT_CYCLE
METAVERSE_NFT_THEME
SECURITY_IDENTITY_DEEPFAKE
GENERATIVE_AI_IP_RISK
```

## deep sub-archetype

```text
플랫폼
SaaS
ERP
클라우드
AI 소프트웨어
생성AI 앱
컨택센터 AI
키오스크
게임 IP
엔터
미디어·광고
스트리밍 광고
보안
딥페이크
생체인식
CCTV
NFT
메타버스
```

## 검증 핵심

```text
SaaS/클라우드:
Green 가능. 반복매출, OPM, FCF, churn.

보안:
Green 가능하지만 CrowdStrike식 장애는 hard 4C.

AI software:
반복매출 있으면 후보. 저작권, license, compute cost가 감점.

게임/IP:
다운로드가 아니라 monetization과 OP/EPS.

미디어:
광고 cycle과 플랫폼 전환 구분.

NFT/메타버스:
거의 Green 금지.
```

## 가격 경로 기대

```text
성공형:
ARR/OPM/FCF와 주가 동행

반례형:
AI/NFT/신작 테마로 급등 후 매출화 실패

Hard 4C:
보안장애, 개인정보, 저작권 소송, 회계·신뢰도 붕괴
```

---

# 10. R9 — 모빌리티·운송·레저

## 대섹터

```text
모빌리티·운송·레저
```

## canonical archetype

```text
AUTO_MOBILITY_COMPLETED_VEHICLE
AUTO_MOBILITY_COMPONENTS
TIRE_AUTO_COMPONENT_SPREAD
AIRLINE_TRAVEL_CYCLE
TRAVEL_LEISURE_REOPENING
CASINO_DUTYFREE_TOURISM
SHIPPING_FREIGHT_CYCLE
RENTAL_USED_CAR_MOBILITY
MOBILITY_RENTAL_MICROMOBILITY
URBAN_AIR_DRONE
SPACE_SUPPLYCHAIN
SATELLITE_CONNECTIVITY_INFRA
```

## deep sub-archetype

```text
완성차
하이브리드
자동차 부품
전장
자율주행
타이어
항공사
여행·레저
카지노
면세점
해운
렌터카
중고차
자전거
공유 모빌리티
드론·플라잉카
스페이스X 관련주
위성통신
```

## 검증 핵심

```text
완성차:
Green 가능. FCF, 하이브리드, 주주환원.

부품:
고객 다변화, 원가전가, OPM.

항공/여행:
cycle/Watch. 유가·환율·관광객 mix.

카지노/면세:
정책 Stage 1과 실제 OP 레버리지 분리.

해운:
cyclical_success. structural Green 제한.

우주/드론:
실제 정부·방산·위성계약 없으면 테마.
```

## 가격 경로 기대

```text
완성차:
PBR/ROE/value-up 리레이팅 가능

항공·여행:
리오프닝 peak 이후 drawdown 확인

해운:
운임 peak와 종목 peak 비교

드론·우주:
계약 없는 price-only rally 필터
```

---

# 11. R10 — 건설·부동산·건자재

## 대섹터

```text
건설·부동산·건자재
```

## canonical archetype

```text
CONSTRUCTION_REAL_ESTATE_CREDIT
REIT_DEVELOPMENT_TRUST
BUILDING_MATERIALS_CYCLE
DATA_CENTER_REIT_INFRASTRUCTURE
COLD_CHAIN_REIT_LOGISTICS
INFRA_RECONSTRUCTION_POLICY
DISASTER_REBUILD_EVENT
```

## deep sub-archetype

```text
대형 건설사
중소형 건설사
PF
미분양
리츠
개발신탁
건자재
시멘트
레미콘
철근
거푸집
가구
데이터센터 REIT
콜드체인 REIT
우크라 재건
네옴시티
재난복구
```

## 검증 핵심

```text
건설:
PF와 현금흐름이 먼저.

건자재:
가격인상과 원가 안정이 핵심. PF 리스크 감점.

REIT:
FFO/AFFO, occupancy, funding cost.

데이터센터 REIT:
hyperscale tenant, 전력·냉각·토지, AFFO.

콜드체인:
NOI/AFFO, energy cost, occupancy.
```

## 가격 경로 기대

```text
건설:
relief rally와 구조적 회복 분리

리츠:
금리 하락 뉴스와 AFFO/배당 커버리지 비교

건자재:
가격인상 후 OPM 개선 여부 확인

데이터센터 REIT:
CAPEX 부담과 FFO 증가 동행 여부 확인
```

---

# 12. R11 — 정책·지정학·재난·이벤트

## 대섹터

```text
정책·지정학·재난·이벤트
```

## canonical archetype

```text
NORTH_KOREA_POLICY_EVENT
GEOPOLITICAL_RECONSTRUCTION
CLIMATE_DISASTER_EVENT
EVENT_DISEASE_PEST_DEMAND
SPECULATIVE_SCIENCE_THEME
ADVANCED_MATERIAL_SPECULATIVE_THEME
POLICY_LOCAL_THEME
ONE_OFF_EVENT_DEMAND
THEME_VALUATION_OVERHEAT
```

## deep sub-archetype

```text
남북경협
DMZ
개성공단
금강산
북한 광물
우크라 재건
네옴시티
세종시
지진
폭염
황사
마스크
엠폭스
빈대
코로나
초전도체
맥신
그래핀
양자
페라이트
```

## 검증 핵심

이 라운드는 대부분 **Green 금지**다.

```text
정책 이벤트:
실제 계약 전까지 event_only.

재난 이벤트:
one-off 수요.

전염병:
진단키트·마스크는 one-off risk.

초전도체/그래핀/맥신:
상용화·매출 전까지 Red/Watch.
```

## 가격 경로 기대

```text
뉴스 후 MFE_5D / 20D / 60D
뉴스 소멸 후 drawdown
EPS/FCF evidence 여부
price-only rally 여부
```

---

# 13. R12 — 농업·생활서비스·기타

## 대섹터

```text
농업·생활서비스·기타
```

## canonical archetype

```text
SMART_FARM_AGRI_TECH
AGRI_LIVESTOCK_FOOD_COMMODITY
ANIMAL_HEALTH_BIOSECURITY
HOME_CHILD_EDUCATION
EDUCATION_SPECIALTY_SERVICES
HOME_LIVING_APPLIANCE_RENTAL
SERVICE_KIOSK_SELF_CHECKOUT
CONSUMER_REGULATED_PRODUCT
```

## deep sub-archetype

```text
스마트팜
농기계
종자·비료·농약
양돈
육계
대두
배합사료
참치
동물백신
교육
취업
키즈
유아용품
밥솥
생활가전 렌탈
키오스크
전자담배
마리화나
주정
```

## 검증 핵심

```text
스마트팜:
정책이 아니라 실제 수주와 운영계약.

농축산:
질병·사료·날씨 이벤트. Green 제한.

동물백신:
반복 접종·정부 비축이면 후보, 질병 뉴스만 있으면 one-off.

교육:
저출산·규제 때문에 Watch.

생활가전:
hardware cycle이면 Watch/Red, 렌탈 반복매출이면 Watch-to-Green.

키오스크:
hardware one-off와 유지보수 반복매출 분리.

규제형 소비재:
규제 승인/불허가 Stage를 좌우.
```

## 가격 경로 기대

```text
농축산:
질병·가격 이벤트 후 drawdown 확인

교육:
반복수강·OPM 개선과 주가 동행 확인

렌탈:
계정 수·해지율·FCF와 주가 동행 확인

키오스크:
설치대수보다 recurring revenue 확인
```

---

# 14. R13 — Cross-archetype RedTeam / 4B / 가격검증 총정리

이건 대섹터가 아니라 모든 라운드에 걸쳐 적용되는 최종 검증 라운드다.

## hard overlay

```text
REDTEAM_ACCOUNTING_TRUST_OVERLAY
THEME_VALUATION_OVERHEAT
ONE_OFF_EVENT_DEMAND
PRICE_ONLY_RALLY
CROWDING_4B_WATCH
```

## hard 4C 조건

```text
감사인 사임
감사보고서 지연
내부통제 중대 결함
SEC/검찰/규제기관 조사
관련자거래 의혹
계약 취소
수주 취소
대형 보안 장애
개인정보 유출
규제 불허
현금 runway 붕괴
```

## 4B 조건

```text
모두가 새 프레임을 인정
목표가 상향 과밀
valuation band 포화
1~2년 급등 후 crowded trade
EPS revision은 계속되지만 multiple 확장 여지 축소
```

## 전체 가격검증

```text
R1~R12 모든 case를 모아:

aligned
false_positive_score
price_moved_without_evidence
evidence_good_but_price_failed
cyclical_success
event_premium
thesis_break
unknown_insufficient_price_data

로 분류한다.
```

---

# 15. 앞으로 라운드별 산출물 형식

각 라운드를 진행할 때 내가 내야 할 결과는 고정한다.

```text
1. 이번 라운드 대섹터
2. 대상 canonical archetype
3. deep sub-archetype
4. 성공사례
5. 반례
6. 4B-watch 사례
7. 4C-thesis-break 사례
8. 점수비중 보정표
9. stage date 후보
10. 가격경로 검증계획
11. 다음에 에이전트가 채워야 할 price fields
12. production scoring 반영 여부: 항상 아직은 shadow
```

---

# 16. 최종 정리

지금 기준으로 확정할 지도는 이거다.

```text
12개 대섹터는 고정.
70개 안팎 canonical archetype은 기본 지도.
90~110개 deep sub-archetype은 점수비중 보정용 하위 렌즈.
200개+ raw theme tag는 검색·분류·쿼리 생성용.
성공/반례 case는 점수정규화 학습용.
가격경로 검증은 최종 gate.
```

앞으로 네가 “다음 라운드 진행해줘”라고 하면 나는 이 순서대로 간다.

```text
R1 산업재·수주·인프라
→ R2 AI·반도체·전자부품
→ R3 2차전지·전기차·친환경
→ R4 소재·스프레드·전략자원
→ R5 소비재·유통·브랜드
→ R6 금융·자본배분·디지털금융
→ R7 바이오·헬스케어·의료기기
→ R8 플랫폼·콘텐츠·SW·보안
→ R9 모빌리티·운송·레저
→ R10 건설·부동산·건자재
→ R11 정책·지정학·재난·이벤트
→ R12 농업·생활서비스·기타
→ R13 Cross-archetype RedTeam / 4B / 가격검증 총정리
```

그리고 각 라운드에서는 단순히 더 많은 사례를 붙이는 게 아니라:

```text
성공사례가 실제 주가 경로에서도 성공이었는지
반례가 실제 drawdown과 thesis break로 이어졌는지
점수비중이 실제 가격경로와 맞았는지
```

까지 같이 확인해서 점수정규화를 더 완성도 있게 만든다.
