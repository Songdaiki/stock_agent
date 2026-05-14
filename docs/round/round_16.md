좋아. 이번 라운드는 **Round 13: 테마 전체 커버리지 맵 v0.5 + 점수정규화 규칙 + 실제 성공/반례 연결**로 갈게.

핵심부터 말하면, 지금 방향은 맞아. 다만 이제부터는 단순히 “성공 후보 / 반례”를 늘리는 게 아니라, 네가 준 세부 테마들을 전부 다음 구조로 흡수해야 해.

```text
Raw Theme Tag
→ 대섹터
→ E2R Archetype
→ Green 정책
→ Must-have evidence
→ Red-flag evidence
→ 점수비중
→ 성공/반례 case
→ price-path validation
```

서생원식 원칙은 그대로 유지해야 한다. 즉, 테마가 아니라 **산업 구조 변화 → EPS/FCF 체급 변화 → 시장의 과거 프레임 오해 → 밸류에이션 리레이팅**이 핵심이다. 단기 주가 급등, 일회성 EPS, 정책 기대, 테마명만으로는 정통 E2R이 아니다.

---

# 1. 이번 라운드의 구조화 결론

기존에는 대략 이렇게 갔지.

```text
10~12개 대섹터
32개 전후 archetype
```

그런데 네가 준 테마 리스트를 전부 품으려면 이제 이렇게 확장해야 해.

```text
12개 대섹터
→ 70개 안팎 archetype / sub-archetype
→ 200개+ theme tag
→ 성공/반례 case library
→ price-path validation
```

중요한 건 **테마명 자체로 점수를 주면 안 된다**는 것.

예를 들어:

```text
초전도체
스테이블코인
야놀자
퓨리오사AI
마켓컬리
엠폭스
빈대
네옴시티
스페이스X
```

이런 이름은 검색과 분류용 태그다.
실제 점수는 아래 증거로만 들어간다.

```text
EPS/FCF 상향
실제 수주/계약
반복매출
수출/채널 확장
OPM/ROE 개선
자본배분 실행
장기계약/선수금/RPO
규제 승인
가격/스프레드 지속성
RedTeam 리스크 부재
```

---

# 2. Theme Tag Map v0.5: 대섹터별 흡수 구조

## A. 산업재·수주·인프라

| Theme tag | Primary archetype                                           | Green 정책    | 핵심 증거                          |
| --------- | ----------------------------------------------------------- | ----------- | ------------------------------ |
| 전력설비      | CONTRACT_BACKLOG_INDUSTRIAL / AI_DATA_CENTER_INFRASTRUCTURE | Green 가능    | 수주잔고, 계약기간, CAPA, 리드타임, EPS 상향 |
| 전선-케이블    | CONTRACT_BACKLOG_INDUSTRIAL                                 | Green 가능    | 장기공급계약, 매출대비 계약금액, 마진          |
| 피팅밸브      | SHIPBUILDING_OFFSHORE_BACKLOG / CONTRACT_BACKLOG_INDUSTRIAL | Watch~Green | 조선/LNG 수주, 납품 visibility       |
| 조선        | SHIPBUILDING_OFFSHORE_BACKLOG                               | Green 가능    | 선가, 저가수주 소진, 수주잔고 질            |
| 조선 기자재    | SHIPBUILDING_OFFSHORE_BACKLOG                               | Watch~Green | 고객사 수주, 납품 스케줄, OPM            |
| LNG선 기자재  | SHIPBUILDING_OFFSHORE_BACKLOG                               | Watch~Green | LNG선 발주, 장기 납품, 마진             |
| 방위산업      | DEFENSE_GOVERNMENT_BACKLOG                                  | Green 가능    | 정부 고객, 다년계약, 수주잔고, 납품 스케줄      |
| 항공우주      | DEFENSE_GOVERNMENT_BACKLOG / URBAN_AIR_DRONE                | Watch       | 실제 수주·납품 전 Green 제한            |
| 원자력·원전    | NUCLEAR_SMR_GRID_POLICY                                     | Watch~Green | 계약 확정, 기자재 매출화, 법적 리스크 낮음      |
| 철도        | RAIL_INFRASTRUCTURE                                         | Watch       | 실제 수주, 예산, 납품 스케줄              |
| 건설기계      | CONTRACT_BACKLOG_INDUSTRIAL / AUTO_MOBILITY_COMPONENTS      | Watch~Green | 해외수요, 수주, 원가, OPM              |
| 우크라 재건    | GEOPOLITICAL_RECONSTRUCTION                                 | Event/Watch | 실제 수주 전 Green 금지               |
| 네옴시티      | GEOPOLITICAL_RECONSTRUCTION                                 | Event/Watch | 실제 계약·매출화 필요                   |

**정규화:**
이 대섹터는 성공 사례가 많이 나올 수 있다. 단, `수주 뉴스`만으로는 부족하고 **계약질 + 마진 + EPS 상향 + 주가 리레이팅**이 같이 가야 한다.

---

## B. AI·반도체·전자부품

| Theme tag  | Primary archetype                                      | Green 정책    | 핵심 증거                               |
| ---------- | ------------------------------------------------------ | ----------- | ----------------------------------- |
| 반도체-HBM    | MEMORY_HBM_CAPACITY                                    | Green 가능    | HBM 수요, CAPA 제약, 장기계약, EPS revision |
| 반도체-CXL    | MEMORY_HBM_CAPACITY / AI_CHIP_FABRIC_INFRA             | Watch       | 실제 채택·매출 전 Green 제한                 |
| 시스템반도체     | AI_CHIP_FABRIC_INFRA                                   | Watch~Green | 수주, 고객사, tape-out, 매출화              |
| 뉴로모픽 반도체   | SPECULATIVE_SCIENCE_THEME / AI_CHIP_FABRIC_INFRA       | Watch/Red   | 상용화 전 Green 금지                      |
| 퓨리오사AI 관련주 | AI_CHIP_FABRIC_INFRA / THEME_VALUATION_OVERHEAT        | Watch/Red   | 실제 지분·계약·매출 확인                      |
| 반도체 전공정 장비 | SEMI_EQUIPMENT_CAPEX                                   | Watch~Green | 고객사 CAPEX, 수주, 납품                   |
| 반도체 후공정 장비 | SEMI_EQUIPMENT_CAPEX                                   | Watch~Green | HBM/패키징 수요, 수주                      |
| 반도체 전공정 소재 | SEMI_MATERIALS_PROCESS                                 | Watch~Green | 반복 납품, 고객사 다변화, OPM                 |
| 반도체 후공정 소재 | SEMI_MATERIALS_PROCESS                                 | Watch~Green | 테스트/패키징 수요                          |
| PCB        | ADVANCED_PACKAGING_PCB / AI_DATA_CENTER_INFRASTRUCTURE | Green 가능    | AI 서버·네트워크 수요, 수주, OPM              |
| 유리기판       | ADVANCED_PACKAGING_PCB                                 | Watch       | 상용화·매출화 전 Green 제한                  |
| MLCC       | ELECTRONIC_COMPONENTS                                  | Watch       | IT/전장 수요, ASP, 재고                   |
| OLED 소재·부품 | DISPLAY_OLED_EQUIPMENT                                 | Watch       | 고객사 패널 CAPEX, 소재 출하                 |
| OLED 장비    | DISPLAY_OLED_EQUIPMENT                                 | Watch       | 장비 수주, 납품, cycle risk               |
| 클린룸        | AI_DATA_CENTER_INFRASTRUCTURE / SEMI_EQUIPMENT_CAPEX   | Watch       | 고객사 CAPEX 실제화                       |
| 스마트폰 부품·소재 | ELECTRONIC_COMPONENTS                                  | Watch       | 고객사 신제품, OPM, 단일고객 리스크              |
| 카메라        | AUTO_COMPONENTS_EV_ADAS / ELECTRONIC_COMPONENTS        | Watch       | 자율주행·스마트폰 고객사 수요                    |
| 무선충전       | ELECTRONIC_COMPONENTS                                  | Watch/Red   | 실제 채택 전 테마성 큼                       |

**실제 사례 연결:**
SK하이닉스는 HBM/메모리 병목의 대표적 구조 사례다. 최근 빅테크가 SK하이닉스 공급 확보를 위해 생산라인·EUV 장비 투자 지원, 장기계약, 가격밴드, 선수금 구조를 제안했다는 보도는 `MEMORY_HBM_CAPACITY`의 Stage 3 핵심 증거가 무엇인지 잘 보여준다. ([Reuters][1])

**정규화:**
반도체는 `메모리/HBM`과 `장비/소재/테마칩`을 분리해야 한다. HBM은 Green 가능성이 높지만, 뉴로모픽·CXL·유리기판·AI칩 관련주는 실제 매출화 전까지 Watch/Red에 가깝다.

---

## C. 2차전지·전기차·친환경

| Theme tag | Primary archetype                                       | Green 정책    | 핵심 증거                 |
| --------- | ------------------------------------------------------- | ----------- | --------------------- |
| 2차전지 소재   | BATTERY_MATERIALS_CAPEX_OVERHEAT                        | Watch/Red   | 장기계약, 판가, EV 수요, CAPA |
| 2차전지 부품   | BATTERY_EQUIPMENT_PARTS                                 | Watch       | 고객사 수주·납품             |
| 2차전지 공정장비 | BATTERY_EQUIPMENT_PARTS                                 | Watch~Green | 장비 수주, 고객사 CAPEX      |
| 폐배터리      | BATTERY_RECYCLING_ESS_SHIFT                             | Watch       | 회수량, 금속가격, 수익성        |
| 전고체 배터리   | BATTERY_RECYCLING_ESS_SHIFT / SPECULATIVE_SCIENCE_THEME | Watch/Red   | 상용화 전 Green 금지        |
| 전기차 인프라   | EV_INFRASTRUCTURE                                       | Watch       | 충전소 매출, 이용률, 수익성      |
| 전기차 화재    | EVENT_RISK / BATTERY_RECYCLING_ESS_SHIFT                | Red flag    | 규제·리콜·수요둔화            |
| 수소차 연료전지  | HYDROGEN_FUEL_CELL_INFRA                                | Watch       | 실제 CAPEX, 고객사, 가동률    |
| 수소차 인프라   | HYDROGEN_FUEL_CELL_INFRA                                | Watch       | 정부 보조금 + 실제 사용률       |
| 태양광       | SOLAR_TARIFF_SUPPLYCHAIN                                | Watch/Red   | 보조금, 관세, 가동률          |
| 풍력        | RENEWABLE_ENERGY_POLICY                                 | Watch       | 수주, 인허가, 원가           |
| 탄소배출권     | RENEWABLE_ENERGY_POLICY / POLICY_EVENT                  | Watch       | 제도 변화 + 실제 수익화        |
| 폐기물처리     | WASTE_RECYCLING_ENVIRONMENT                             | Green 가능    | 허가권, 처리량, 반복 FCF      |
| 탈 플라스틱    | WASTE_RECYCLING_ENVIRONMENT                             | Watch       | 실제 고객사·마진 전까지 제한      |

**정규화:**
2차전지는 Green보다 **과열 방어**가 우선이다. 소재·전고체·폐배터리는 테마가 강하므로, 실제 계약·수익성·FCF가 확인되기 전까지 Stage 3-Green을 제한해야 한다.

---

## D. 소재·스프레드·전략자원

| Theme tag | Primary archetype                                | Green 정책    | 핵심 증거                |
| --------- | ------------------------------------------------ | ----------- | -------------------- |
| 화학        | CHEMICAL_SPREAD                                  | Watch/Red   | 제품 spread, 중국 공급, 원가 |
| 정유        | REFINING_OIL_SPREAD                              | Watch       | 정제마진, 재고, 수요         |
| 윤활유       | REFINING_OIL_SPREAD                              | Watch~Green | 고마진 제품 mix, 반복수요     |
| 철강 주요업체   | STEEL_METAL_SPREAD                               | Watch       | 중국 공급, 원가, 수요        |
| 철강 중소형    | STEEL_METAL_SPREAD                               | Watch/Red   | 수요·원가·재무 리스크         |
| 비철금속      | NONFERROUS_STRATEGIC_METALS                      | Watch       | 금속가격, 제련마진           |
| 구리        | NONFERROUS_STRATEGIC_METALS                      | Watch       | 전력망·AI DC 수요와 연결 가능  |
| 리튬        | BATTERY_MATERIALS_CAPEX_OVERHEAT                 | Watch/Red   | 광물가격, EV 수요          |
| 희토류       | RARE_METALS_STRATEGIC_MATERIALS                  | Watch/Event | 지정학, 공급망, 실제 매출      |
| 금은        | COMMODITY_SPREAD                                 | Watch       | 가격 사이클, 안전자산         |
| 페라이트      | ADVANCED_MATERIAL_THEMES                         | Watch/Red   | 실제 적용 전 테마성 큼        |
| 그래핀·맥신    | SPECULATIVE_SCIENCE_THEME                        | Red/Watch   | 상용화 전 Green 금지       |
| 초전도체      | SPECULATIVE_SCIENCE_THEME                        | Red         | 논문·테마만으로 Green 금지    |
| 양자 기술     | SPECULATIVE_SCIENCE_THEME / AI_CHIP_FABRIC_INFRA | Watch/Red   | 실제 계약·매출화 필요         |
| 제지·골판지    | PAPER_PACKAGING                                  | Watch       | 가격인상, 원가, 택배수요       |
| 주정        | CHEMICAL_SPREAD / FOOD_COMMODITY                 | Watch       | 원가·판가·규제             |

**실제 사례 연결:**
Korea Zinc는 금속·전략자원·거버넌스가 섞인 대표 케이스다. MBK와 Young Poong의 공개매수 발표 후 Korea Zinc 주가가 19.8% 상승했다는 보도는, 이것이 구조적 FCF 리레이팅인지 이벤트 프리미엄인지 분리해서 봐야 한다는 걸 보여준다. ([Reuters][2])

**정규화:**
소재·스프레드는 EPS가 크게 튈 수 있지만 대부분 cycle risk가 크다. `structural_visibility`를 낮게 시작하고, `bottleneck/pricing`은 높게 줄 수 있지만 Green은 엄격히 제한해야 한다.

---

## E. 소비재·유통·브랜드

| Theme tag   | Primary archetype                          | Green 정책    | 핵심 증거              |
| ----------- | ------------------------------------------ | ----------- | ------------------ |
| 라면          | EXPORT_RECURRING_CONSUMER                  | Green 가능    | 수출, 반복소비, ASP, OPM |
| K-푸드        | EXPORT_RECURRING_CONSUMER                  | Green 가능    | 해외 채널, FY1/FY2 EPS |
| 음식료         | EXPORT_RECURRING_CONSUMER / FOOD_COMMODITY | Watch~Green | 브랜드/수출 여부에 따라 분기   |
| 건강기능식품      | EXPORT_RECURRING_CONSUMER                  | Watch       | 반복구매, 채널, 규제       |
| 음식료 유통      | RETAIL_ECOMMERCE_LOGISTICS                 | Watch       | 물류효율, FCF          |
| 편의점         | RETAIL_CONVENIENCE_OFFLINE                 | Watch~Green | SSSG, PB, OPM      |
| 홈쇼핑         | RETAIL_CONVENIENCE_OFFLINE                 | Watch/Red   | 구조 둔화·수수료 압박       |
| 마켓컬리·오아시스   | ECOMMERCE_FRESH_LOGISTICS                  | Watch/Event | 상장 기대와 흑자전환 분리     |
| 콜드체인        | ECOMMERCE_FRESH_LOGISTICS                  | Watch       | 반복 물류 수요, 마진       |
| 화장품 브랜드     | K_BEAUTY_EXPORT_DISTRIBUTION               | Green 가능    | 미국/일본 수출, 채널, OPM  |
| 화장품 OEM·ODM | BEAUTY_OEM_ODM_SUPPLYCHAIN                 | Green 가능    | 고객사 다변화, 반복 주문     |
| 화장품 원재료·부자재 | BEAUTY_OEM_ODM_SUPPLYCHAIN                 | Watch~Green | 고객사 다변화, 마진        |
| 의류 브랜드      | APPAREL_BRAND_OEM                          | Watch       | 재고, 브랜드, 채널        |
| 의류 OEM·ODM  | APPAREL_BRAND_OEM                          | Watch       | 고객사 주문, 환율, 마진     |
| 유아용품·키즈     | HOME_CHILD_EDUCATION                       | Watch       | 저출산 리스크            |
| 밥솥·생활가전     | HOME_LIVING_APPLIANCE                      | Watch       | 반복수요 낮음, 수출 확인 필요  |

**정규화:**
소비재는 `수출·반복소비·OPM·채널 확장`이 있으면 Green 가능하다. 반대로 단일 제품 유행, 재고, 매출채권, 리콜, 원가 상승은 4C 후보가 된다.

---

## F. 금융·자본배분·디지털금융

| Theme tag | Primary archetype                     | Green 정책    | 핵심 증거                      |
| --------- | ------------------------------------- | ----------- | -------------------------- |
| 은행        | FINANCIAL_SPREAD_BALANCE_SHEET        | Green 가능    | ROE, CET1, 환원, credit cost |
| 금융지주      | FINANCIAL_SPREAD_BALANCE_SHEET        | Green 가능    | PBR-ROE, 환원정책              |
| 손해보험      | INSURANCE_UNDERWRITING_CYCLE          | Green 가능    | 손해율, CSM, 자본비율             |
| 생명보험      | INSURANCE_UNDERWRITING_CYCLE          | Watch~Green | CSM, 금리, 배당여력              |
| 증권사       | SECURITIES_BROKERAGE_CYCLE            | Watch       | 거래대금, IB, 자본비율             |
| VC        | SECURITIES_BROKERAGE_CYCLE            | Watch/Red   | 회수시장, 밸류 리스크               |
| 고배당주      | VALUE_UP_SHAREHOLDER_RETURN           | Watch~Green | 배당 지속성, FCF                |
| 밸류업 지수 편입 | VALUE_UP_SHAREHOLDER_RETURN           | Watch       | 편입 자체보다 환원 실행              |
| 부동산 자산 보유 | HOLDING_RESTRUCTURING_GOVERNANCE      | Watch       | NAV, 자산가치, 현금화             |
| 결제서비스     | PAYMENT_FINTECH_INFRA                 | Watch~Green | 거래액, take rate, 반복매출       |
| 토스 관련주    | PAYMENT_FINTECH_INFRA / EVENT_PREMIUM | Watch/Event | 지분·상장·실적 연결 확인             |
| 신용정보      | PAYMENT_FINTECH_INFRA                 | Watch~Green | 반복 데이터 매출                  |
| 지역화폐      | PAYMENT_FINTECH_INFRA / POLICY_EVENT  | Watch       | 정책 의존성                     |
| STO       | DIGITAL_ASSET_TOKENIZATION            | Watch       | 법제화 + 실제 발행                |
| 스테이블코인    | DIGITAL_ASSET_TOKENIZATION            | Watch       | 규제 승인 + 발행량 + 수익모델         |
| NFT       | METAVERSE_NFT_THEME                   | Red/Watch   | 실적 전까지 Green 금지            |

**실제 사례 연결:**
스테이블코인·토큰화 금융은 규제·실제 발행·거래량·수익모델이 필요하다. Toss의 원화 스테이블코인 추진은 Stage 1~2 후보가 될 수 있지만, 규제 승인과 실제 수익모델 전까지 Green은 제한해야 한다. 스테이블코인 자체도 시장·유동성·규제 리스크가 크므로 risk penalty를 강하게 둬야 한다. ([arXiv][3])

---

## G. 바이오·헬스케어·의료기기

| Theme tag | Primary archetype                                | Green 정책    | 핵심 증거           |
| --------- | ------------------------------------------------ | ----------- | --------------- |
| CMO·원료의약품 | CDMO_HEALTHCARE_CONTRACT                         | Green 가능    | 장기계약, 가동률, 고객사  |
| CRO       | CDMO_HEALTHCARE_CONTRACT / BIOTECH_SERVICE       | Watch       | 반복계약, 고객사       |
| 바이오시밀러    | CDMO_HEALTHCARE_CONTRACT / BIOTECH_ROYALTY       | Watch~Green | 매출화, 가격경쟁       |
| 의료AI      | DIGITAL_HEALTHCARE_AI                            | Watch       | 병원 도입, 규제, 수익모델 |
| 원격의료      | DIGITAL_HEALTHCARE_AI                            | Watch       | 법제화, 실제 매출      |
| 유전체검사     | DIGITAL_HEALTHCARE_AI                            | Watch       | 반복검사, 규제        |
| 마이크로바이옴   | BIOTECH_PRE_REVENUE_REGULATORY                   | Watch/Red   | 매출화 전 Green 제한  |
| AI 신약개발   | BIOTECH_PRE_REVENUE_REGULATORY                   | Watch/Red   | 후보물질·계약·매출화 필요  |
| 이중항체      | BIOTECH_PRE_REVENUE_REGULATORY / BIOTECH_ROYALTY | Watch       | 임상/기술이전         |
| 면역세포치료제   | BIOTECH_PRE_REVENUE_REGULATORY                   | Watch/Red   | 임상·매출화 전 제한     |
| 줄기세포치료제   | BIOTECH_PRE_REVENUE_REGULATORY                   | Watch/Red   | 규제·임상 리스크       |
| 치매치료      | BIOTECH_PRE_REVENUE_REGULATORY                   | Watch/Red   | 허가·매출화 필요       |
| 비만치료제     | BIOTECH_ROYALTY_COMMERCIALIZATION                | Watch       | 실제 매출·로열티       |
| 탈모치료      | BIOTECH_PRE_REVENUE_REGULATORY                   | Watch/Red   | 상용화 전 제한        |
| 난임        | BIOTECH_ROYALTY / MEDICAL_DEVICE                 | Watch       | 실제 매출 필요        |
| 보톡스       | MEDICAL_DEVICE_HEALTHCARE_EXPORT                 | Green 가능    | 수출, 허가, 반복시술    |
| 치아·임플란트   | MEDICAL_DEVICE_HEALTHCARE_EXPORT                 | Green 가능    | 수출, 반복수요, OPM   |
| 미용기기      | MEDICAL_DEVICE_HEALTHCARE_EXPORT                 | Green 가능    | 수출국, 소모품, OPM   |
| 수술용 로봇    | MEDICAL_DEVICE_HEALTHCARE_EXPORT / ROBOTICS      | Watch~Green | 반복소모품/시술 매출     |
| 전염병 진단    | DIAGNOSTICS_INFECTIOUS_EVENT                     | Red/Watch   | one-off risk    |

**정규화:**
바이오는 세 갈래로 나눠야 한다.

```text
Pre-revenue biotech: Green 거의 금지
Royalty/commercialization biotech: 매출화·로열티 필요
CDMO/medical device: 장기계약·반복매출이면 Green 가능
```

---

## H. 플랫폼·콘텐츠·SW·보안

| Theme tag | Primary archetype                        | Green 정책    | 핵심 증거                   |
| --------- | ---------------------------------------- | ----------- | ----------------------- |
| 게임        | GAME_CONTENT_IP                          | Watch       | 실제 매출화, IP 반복성          |
| 엔터        | GAME_CONTENT_IP                          | Watch       | 팬덤 monetization, 계약 리스크 |
| 미디어 콘텐츠   | GAME_CONTENT_IP / MEDIA_AD_CONTENT_CYCLE | Watch       | 글로벌 판매, 반복 IP           |
| 음원서비스     | GAME_CONTENT_IP / PLATFORM               | Watch       | 반복매출, ARPU              |
| 방송·언론     | MEDIA_AD_CONTENT_CYCLE                   | Watch/Red   | 광고 cycle, 규제            |
| 광고        | MEDIA_AD_CONTENT_CYCLE                   | Watch       | 광고 회복, OPM              |
| 클라우드 컴퓨팅  | CLOUD_AI_SOFTWARE_INFRA                  | Watch~Green | 반복매출, OPM, 고객사          |
| 인공지능 AI   | CLOUD_AI_SOFTWARE_INFRA / THEME_OVERHEAT | Watch       | 실제 매출 전 Green 제한        |
| 원격근무      | PLATFORM_SOFTWARE_INTERNET               | Watch       | 반복구독 여부                 |
| 컨택센터      | PLATFORM_SOFTWARE / SERVICE_AUTOMATION   | Watch       | B2B 반복매출                |
| IT보안      | SECURITY_IDENTITY_DEEPFAKE               | Watch~Green | 반복 보안계약                 |
| 딥페이크      | SECURITY_IDENTITY_DEEPFAKE               | Watch       | 규제·도입계약 필요              |
| 생체인식      | SECURITY_IDENTITY_DEEPFAKE               | Watch       | 공공/기업 계약                |
| CCTV      | SECURITY_IDENTITY_DEEPFAKE               | Watch       | 반복매출·마진                 |
| 메타버스      | METAVERSE_NFT_THEME                      | Red/Watch   | 실적 전 Green 금지           |
| NFT       | METAVERSE_NFT_THEME                      | Red/Watch   | 실적 전 Green 금지           |

**실제 사례 연결:**
Kakao는 플랫폼 자산이 있어도 거버넌스·법적 리스크가 valuation rerating을 막을 수 있는 반례다. SM엔터 인수 과정의 주가조작 혐의로 카카오 창업자 관련 법적 이슈가 부각된 사례는 `PLATFORM_SOFTWARE_INTERNET`의 hard RedTeam 조건으로 넣어야 한다. ([Reuters][4])

---

## I. 모빌리티·운송·레저

| Theme tag  | Primary archetype                             | Green 정책    | 핵심 증거                |
| ---------- | --------------------------------------------- | ----------- | -------------------- |
| 항공사        | AIRLINE_TRAVEL_CYCLE                          | Watch       | 여객, 유가, 환율, 화물       |
| 여행·레저      | TRAVEL_LEISURE_REOPENING                      | Watch       | 객실·방문객·OPM           |
| 야놀자 관련주    | TRAVEL_LEISURE_REOPENING / EVENT_PREMIUM      | Watch/Event | 지분·상장·실적 연결          |
| 카지노        | CASINO_DUTYFREE_TOURISM                       | Watch       | drop amount, VIP mix |
| 면세점        | CASINO_DUTYFREE_TOURISM                       | Watch       | 중국 의존도, 객단가          |
| 금강산 관광     | NORTH_KOREA_POLICY_EVENT                      | Event/Red   | 정책 이벤트, Green 금지     |
| 해운         | SHIPPING_FREIGHT_CYCLE                        | Red/Watch   | 운임, 선복, cycle        |
| 택배·종합물류    | ECOMMERCE_FRESH_LOGISTICS                     | Watch       | 물동량, 단가, 비용          |
| 렌터카·중고차    | RENTAL_USED_CAR_MOBILITY                      | Watch       | 잔존가치, 금리, 수요         |
| 자전거        | RETAIL_CONSUMER_CYCLE                         | Watch/Red   | 단기 수요 가능             |
| 현대·기아차 부품주 | AUTO_MOBILITY_COMPONENTS                      | Watch~Green | 고객사, OPM, 전장화        |
| 자율주행       | AUTO_COMPONENTS_EV_ADAS                       | Watch       | 실제 채택·매출             |
| 경량화        | AUTO_COMPONENTS_EV_ADAS                       | Watch       | 고객사 적용, 마진           |
| 드론·플라잉카    | URBAN_AIR_DRONE                               | Watch/Red   | 상용화 전 Green 제한       |
| 스페이스X      | SPECULATIVE_SCIENCE_THEME / SPACE_SUPPLYCHAIN | Watch/Red   | 실제 납품/계약 확인          |

**정규화:**
모빌리티는 대부분 cycle/Watch다. 완성차 value-up이나 부품 고객다변화처럼 실적·환원·반복납품이 있을 때만 Green 가능.

---

## J. 건설·부동산·건자재

| Theme tag    | Primary archetype                             | Green 정책    | 핵심 증거         |
| ------------ | --------------------------------------------- | ----------- | ------------- |
| 대형 건설사       | CONSTRUCTION_REAL_ESTATE_CREDIT               | Watch/Red   | PF, 현금흐름, 원가율 |
| 중소형 건설사      | CONSTRUCTION_REAL_ESTATE_CREDIT               | Red/Watch   | 신용위험 큼        |
| 부동산 자산 보유    | HOLDING_GOVERNANCE / REIT                     | Watch       | NAV, 현금화      |
| 개발신탁리츠       | REIT_DEVELOPMENT_TRUST                        | Watch       | 금리, 배당, 자산가치  |
| 건자재          | BUILDING_MATERIALS_CYCLE                      | Watch       | 착공, 원가, 가격인상  |
| 시멘트·레미콘·콘크리트 | BUILDING_MATERIALS_CYCLE                      | Watch       | 출하량, 가격, 원가   |
| 철근           | BUILDING_MATERIALS_CYCLE / STEEL              | Watch       | 건설수요, 원가      |
| 가구           | RETAIL_DOMESTIC_CONSUMER / BUILDING_MATERIALS | Watch       | 부동산 경기        |
| 거푸집          | BUILDING_MATERIALS_CYCLE                      | Watch       | 착공량           |
| 우크라 재건       | GEOPOLITICAL_RECONSTRUCTION                   | Event/Watch | 실제 수주 필요      |
| 네옴시티         | GEOPOLITICAL_RECONSTRUCTION                   | Event/Watch | 실제 수주 필요      |
| 세종시          | POLICY_LOCAL_THEME                            | Event       | 정책 이벤트        |

**정규화:**
건설은 PF와 현금흐름이 먼저다. 수주잔고만으로 Green을 주면 위험하다.

---

## K. 정책·재난·이벤트

| Theme tag    | Primary archetype                           | Green 정책    | 핵심 증거            |
| ------------ | ------------------------------------------- | ----------- | ---------------- |
| 남북경협         | NORTH_KOREA_POLICY_EVENT                    | Event/Red   | 실제 계약 전 Green 금지 |
| DMZ          | NORTH_KOREA_POLICY_EVENT                    | Event/Red   | 정책 이벤트           |
| 개성공단         | NORTH_KOREA_POLICY_EVENT                    | Event/Red   | 정책 이벤트           |
| 광물자원개발       | NORTH_KOREA_POLICY_EVENT / STRATEGIC_METALS | Event/Watch | 실제 사업권 필요        |
| 지진           | CLIMATE_DISASTER_EVENT                      | Event       | 단기 건자재·복구        |
| 폭염           | CLIMATE_DISASTER_EVENT                      | Event/Watch | 전력수요·냉각          |
| 황사·미세먼지 공기정화 | CLIMATE_DISASTER_EVENT                      | Event/Watch | 단기 수요            |
| 황사마스크        | EVENT_DISEASE_PEST_DEMAND                   | Event/Red   | one-off          |
| 엠폭스          | EVENT_DISEASE_PEST_DEMAND                   | Event/Red   | one-off          |
| 빈대퇴치         | EVENT_DISEASE_PEST_DEMAND                   | Event/Red   | one-off          |
| 코로나19 제약     | DIAGNOSTICS_INFECTIOUS_EVENT                | Event/Red   | one-off risk     |
| 초전도체         | SPECULATIVE_SCIENCE_THEME                   | Red         | Green 금지         |
| 맥신           | SPECULATIVE_SCIENCE_THEME                   | Red         | Green 금지         |
| 그래핀          | SPECULATIVE_SCIENCE_THEME                   | Red         | Green 금지         |
| 양자 기술        | SPECULATIVE_SCIENCE_THEME                   | Watch/Red   | 실제 계약 필요         |

**정규화:**
정책·재난·과학 테마는 대부분 `event premium` 또는 `theme overheat`다. Stage 3-Green보다 RedTeam/4B 방어가 중요하다.

---

## L. 농업·생활서비스·기타

| Theme tag | Primary archetype                           | Green 정책    | 핵심 증거           |
| --------- | ------------------------------------------- | ----------- | --------------- |
| 양돈주       | AGRI_LIVESTOCK_FOOD_COMMODITY               | Watch/Red   | 돼지고기 가격, 사료비    |
| 육계주       | AGRI_LIVESTOCK_FOOD_COMMODITY               | Watch/Red   | 닭고기 가격, 사료비     |
| 배합사료      | AGRI_LIVESTOCK_FOOD_COMMODITY               | Watch       | 곡물가격, 판가전가      |
| 대두        | AGRI_LIVESTOCK_FOOD_COMMODITY               | Event/Watch | commodity cycle |
| 농기계       | SMART_FARM_AGRI_TECH                        | Watch       | 수주, 해외확장        |
| 종자·비료·농약  | SMART_FARM_AGRI_TECH / COMMODITY            | Watch       | 가격전가, 정책        |
| 스마트팜      | SMART_FARM_AGRI_TECH                        | Watch       | 실제 수주·운영        |
| 참치 원양어업   | AGRI_LIVESTOCK_FOOD_COMMODITY               | Watch       | 어가, 유가, 환율      |
| 교육        | EDUCATION_SPECIALTY_SERVICES                | Watch       | 반복수강, OPM       |
| 취업일자리     | EDUCATION_SPECIALTY_SERVICES / POLICY_EVENT | Watch       | 정책·반복매출         |
| 키즈·유아용품   | HOME_CHILD_EDUCATION                        | Watch/Red   | 저출산 리스크         |
| 전자담배      | CONSUMER_REGULATED_PRODUCT                  | Watch       | 규제·반복수요         |
| 주정        | CHEMICAL_SPREAD / FOOD_INPUT                | Watch       | 원가·판가           |

---

# 3. 점수비중 v0.5: Green 정책별 기본값

## Green 가능군

| Archetype group       | EPS/FCF | Visibility | Bottleneck | Mispricing | Valuation | 특징          |
| --------------------- | ------: | ---------: | ---------: | ---------: | --------: | ----------- |
| Contract / Backlog    |      20 |         24 |         22 |         12 |        12 | 계약·수주잔고 중심  |
| AI Data Center Infra  |      22 |         23 |         20 |         14 |        12 | 다년 CAPEX·병목 |
| K-Food / K-Beauty     |      22 |         23 |         12 |         16 |        13 | 수출·채널·OPM   |
| Memory / HBM          |      24 |         21 |         19 |         15 |        12 | HBM·공급규율    |
| CDMO / Medical Device |      20 |      22~24 |      12~13 |      12~14 |        12 | 반복 계약/소모품   |
| Financial / Insurance |      15 |         20 |          5 |         15 |        25 | ROE-PBR-환원  |

## Watch / Yellow 중심군

| Archetype group     | EPS/FCF | Visibility | Bottleneck | Mispricing | Valuation | 특징             |
| ------------------- | ------: | ---------: | ---------: | ---------: | --------: | -------------- |
| Platform / Software |      20 |         22 |          8 |         16 |        14 | ARPU·OPM·규제    |
| Robotics            |      18 |         15 |         10 |         12 |        10 | 매출화 전 Green 금지 |
| Nuclear / SMR       |      18 |         22 |          8 |         14 |        12 | 계약·법적 리스크      |
| Auto / Components   |      20 |         18 |         10 |      14~15 |     14~17 | 믹스·환원·원가       |
| Retail / E-commerce |      18 |         16 |          5 |         14 |        14 | OPM·FCF 필요     |
| Digital Asset / STO |      16 |         18 |          8 |         16 |        12 | 규제·거래량 필요      |

## Red / 4B 방어군

| Archetype group      | EPS/FCF | Visibility | Bottleneck | Mispricing | Valuation | 특징              |
| -------------------- | ------: | ---------: | ---------: | ---------: | --------: | --------------- |
| Shipping / Freight   |      20 |       8~10 |         18 |          8 |         8 | 운임 cycle        |
| Commodity / Chemical |   18~20 |       8~12 |      16~18 |       8~10 |      8~10 | spread reversal |
| Battery Overheat     |      20 |         16 |         14 |         10 |        10 | CAPA·EV risk    |
| Construction / PF    |      18 |         10 |          8 |         12 |        10 | credit risk     |
| One-off Disease      |      20 |          5 |          5 |          5 |         5 | 일회성             |
| Speculative Science  |    5~10 |          5 |          5 |          5 |         5 | Green 거의 금지     |

---

# 4. 이번 라운드의 핵심 정리

이제 네가 준 세부 테마는 거의 다 아래 구조 안에 들어간다.

```text
12개 대섹터
→ 약 70개 archetype / sub-archetype
→ theme tag map
→ 성공/반례 case
→ price-path validation
→ shadow scoring
```

중요한 결론은 이것.

```text
1. 테마명은 점수 근거가 아니다.
2. 점수는 EPS/FCF, visibility, bottleneck, mispricing, valuation, risk evidence에서 나온다.
3. Green 가능 archetype과 Green 제한 archetype을 분리해야 한다.
4. 성공사례는 주가와 EPS/FCF 리레이팅이 같이 가야 한다.
5. 반례는 주가가 올랐어도 EPS/FCF가 안 따라가거나 4C가 빨리 온 케이스다.
```

---

# 5. 다음 라운드에서 할 것

다음은 이제 **진짜 기계 입력 구조**에 가까워져야 해.

```text
1. theme_tag_map.csv 초안
   - theme_tag
   - large_sector
   - primary_archetype
   - secondary_archetypes
   - green_policy
   - must_have_evidence
   - red_flag_evidence

2. cases_v03.jsonl 후보
   - 각 archetype별 성공 2개 + 반례 2개 목표

3. price_validation 요구 필드
   - stage2_price
   - stage3_price
   - peak_price
   - MFE/MAE
   - drawdown_after_peak

4. shadow scoring 설계
   - production StageClassifier는 아직 유지
   - archetype-aware score는 병렬 계산
   - price-path와 비교해 점수비중 검증
```

지금까지의 확장으로, 네가 보낸 테마 리스트는 대부분 커버 가능한 구조까지 왔다. 다음 라운드에서는 이것을 **테마 매핑표 형태**로 더 압축해서 줄 수 있다.

[1]: https://www.reuters.com/world/asia-pacific/sk-hynix-flooded-with-unprecedented-offers-big-tech-firms-secure-chip-supplies-2026-05-07/?utm_source=chatgpt.com "SK Hynix flooded with unprecedented offers from big tech firms to secure chip supplies"
[2]: https://www.reuters.com/markets/deals/private-equity-mbk-young-poong-launch-15-bln-tender-offer-korea-zinc-shares-2024-09-13/?utm_source=chatgpt.com "Private equity MBK, Young Poong launch $1.5 bln tender offer for Korea Zinc shares"
[3]: https://arxiv.org/abs/2505.12413?utm_source=chatgpt.com "The Stablecoin Discount: Evidence of Tether's U.S. Treasury Bill Market Share in Lowering Yields"
[4]: https://www.reuters.com/business/media-telecom/south-korea-prosecutors-seek-15-year-jail-term-kakao-founder-kim-2025-08-29/?utm_source=chatgpt.com "South Korea prosecutors seek 15-year jail term for Kakao founder Kim"
