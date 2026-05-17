응. **기억하고 있고, 큰 구조는 유지된 상태에서 더 세분화된 거야.**
정리하면 이렇다.

> **처음 정리된 뼈대:**
> 12개 대섹터 → 약 70개 archetype/sub-archetype → 200개+ raw theme tag
>
> **이후 진행된 작업:**
> 대섹터를 더 늘린 게 아니라, 기존 12개 대섹터 안에서 **얇았던 archetype을 더 쪼개고, 성공/반례/가격검증 계획을 붙여 두껍게 만든 것**.

즉, 지금 추가된 것들은 대부분 “새 대섹터”가 아니라 **하위 sub-archetype**이야. 예를 들어 `AI·반도체·전자부품`이라는 대섹터 안에서 처음에는 HBM, 장비, 소재, PCB 정도로 나눴는데, 이후에 `AI server ODM`, `neocloud GPU rental`, `advanced packaging CoWoS`, `optical networking`, `AI data center cooling`, `industrial gases` 같은 하위축을 더 세밀하게 분리한 거다.

업로드한 정리본도 그 흐름과 맞아. 거기서는 이미 12개 대섹터별로 raw theme tag를 primary archetype, Green 정책, 핵심 증거로 매핑해놨고, 예를 들어 산업재·수주·인프라에서는 전력설비, 전선, 조선, 방산, 원전, 철도, 우크라 재건 같은 테마를 각각 수주형/정책형/이벤트형으로 나눴다.
AI·반도체 쪽도 HBM은 Green 가능성이 높지만, CXL·뉴로모픽·유리기판·AI칩 관련주는 실제 채택·매출 전까지 Watch/Red로 둬야 한다고 이미 구분되어 있다.

---

# 1. 현재까지의 최상위 구조는 그대로 12개

지금도 대섹터는 이 12개로 보는 게 맞아.

| 번호 | 대섹터           | 현재 상태                                   |
| -: | ------------- | --------------------------------------- |
|  1 | 산업재·수주·인프라    | 전력설비, 방산, 조선, 철도, 원전, 건설기계, 재건          |
|  2 | AI·반도체·전자부품   | HBM, 장비, 소재, PCB, 유리기판, AI칩, MLCC, OLED |
|  3 | 2차전지·전기차·친환경  | 2차전지, 폐배터리, ESS, 수소, 태양광, 풍력, 폐기물       |
|  4 | 소재·스프레드·전략자원  | 화학, 정유, 철강, 비철, 구리, 리튬, 희토류, 금은         |
|  5 | 소비재·유통·브랜드    | K푸드, 라면, K뷰티, 편의점, 이커머스, 의류, 생활가전       |
|  6 | 금융·자본배분·디지털금융 | 은행, 보험, 증권, 밸류업, 결제, STO, 스테이블코인        |
|  7 | 바이오·헬스케어·의료기기 | CDMO, CRO, 바이오시밀러, 의료AI, 원격의료, 미용기기     |
|  8 | 플랫폼·콘텐츠·SW·보안 | 게임, 엔터, 미디어, 클라우드, AI SW, 보안, 딥페이크      |
|  9 | 모빌리티·운송·레저    | 완성차, 부품, 항공, 해운, 카지노, 면세, 렌터카           |
| 10 | 건설·부동산·건자재    | 건설, PF, 리츠, 건자재, 시멘트, 철근, 가구            |
| 11 | 정책·지정학·재난·이벤트 | 남북경협, 우크라 재건, 세종시, 전염병, 황사, 초전도체        |
| 12 | 농업·생활서비스·기타   | 양돈, 육계, 사료, 대두, 스마트팜, 교육, 키즈, 규제소비재     |

이 12개는 “큰 서랍”이고, 점수는 여기서 바로 주면 안 된다. 점수는 그 아래의 archetype/sub-archetype에서 줘야 해.

---

# 2. 처음 70개 안팎이었던 archetype은 지금 더 세분화됨

초기에는 “약 70개 안팎”이라고 봤는데, 이후 딥서치 라운드를 계속 돌면서 **실제로는 90~110개 안팎의 sub-archetype 후보**까지 확장됐다고 보는 게 맞아.

다만 이건 “분류가 난잡해졌다”는 뜻이 아니라, **같은 대섹터 안에서도 점수비중이 완전히 달라지는 것들을 분리했다**는 뜻이야.

예를 들어 AI 인프라 안에서도:

```text
HBM
AI server ODM
AI data center cooling
advanced packaging
optical networking
neocloud GPU rental
data center REIT
AI grid flexibility
industrial gases for semiconductor fab
AI data center power equipment
```

이것들은 전부 AI 수혜처럼 보이지만, 점수비중이 달라.

* HBM은 EPS/FCF와 병목 점수를 높게 줄 수 있음.
* AI server ODM은 매출은 크지만 저마진·재고·회계 리스크가 큼.
* Neocloud는 take-or-pay visibility는 있지만 고부채·GPU 감가상각 리스크가 큼.
* Data center REIT는 EPS보다 AFFO, tenant, funding cost를 봐야 함.
* Optical networking은 hyperscaler 장기계약이 있으면 Green 가능성이 생김.
* AI grid flexibility는 아직 PoC/상용화 리스크가 커서 Watch 쪽.

이런 식으로 “테마는 같아 보이지만 점수 구조가 다른 것”들을 더 쪼갠 거야.

---

# 3. 지금까지 두껍게 판 주요 축

## Green 가능성이 비교적 높은 쪽

이쪽은 성공사례를 통해 점수비중을 꽤 많이 채웠다.

| Archetype                        | 왜 Green 가능성이 있는가                    | 핵심 점수축                          |
| -------------------------------- | ----------------------------------- | ------------------------------- |
| GRID_TRANSFORMER_SHORTAGE / 전력설비 | AI 데이터센터·전력망 병목, 리드타임, 수주잔고         | EPS/FCF, visibility, bottleneck |
| MEMORY_HBM_CAPACITY              | HBM 병목, 장기계약, CAPA 제약, EPS revision | EPS/FCF, bottleneck, 리레이팅       |
| AI_DATA_CENTER_COOLING           | 액침냉각/HVAC 병목, 고객사 DC CAPEX          | bottleneck, visibility          |
| OPTICAL_NETWORKING_AI_DC         | AI 데이터센터 광통신 병목, hyperscaler 계약     | bottleneck, visibility          |
| DEFENSE_GOVERNMENT_BACKLOG       | 정부고객, 다년계약, 수주잔고                    | visibility, backlog             |
| SHIPBUILDING_OFFSHORE_BACKLOG    | 선가, 저가수주 소진, 수주잔고 질                 | EPS, visibility, pricing        |
| EXPORT_RECURRING_CONSUMER        | K푸드/라면 수출, 반복소비, ASP, OPM           | EPS, visibility, mispricing     |
| K_BEAUTY / OEM_ODM               | 미국·일본 채널, 고객사 다변화, 반복 주문            | EPS, visibility                 |
| CDMO_HEALTHCARE_CONTRACT         | 장기계약, capacity, 가동률                 | visibility, FCF                 |
| MEDICAL_DEVICE_EXPORT            | 반복 시술·소모품·수출국 확대                    | EPS, visibility                 |
| INSURANCE_UNDERWRITING           | 손해율, CSM, ROE, 자본비율, 환원             | valuation, capital allocation   |
| VALUE_UP_SHAREHOLDER_RETURN      | 실제 소각·배당·ROE/NAV 개선                 | valuation, capital allocation   |

이쪽은 “성공사례가 많고, 점수비중도 어느 정도 안정화된 축”이라고 보면 된다.

---

## Watch-to-Green 쪽

좋은 사례가 나올 수는 있지만, 조건이 까다로운 축이다.

| Archetype                   | 왜 Watch인가                         | Green으로 올라가는 조건                 |
| --------------------------- | --------------------------------- | ------------------------------- |
| CLOUD_AI_SOFTWARE_INFRA     | AI 키워드만으로는 부족                     | 반복매출, OPM, FCF, 낮은 churn        |
| SECURITY_IDENTITY_DEEPFAKE  | 보안 수요는 구조적이나 장애·소송 리스크 큼          | ARR, 고객 다변화, 신뢰도 유지             |
| CRO_CLINICAL_SERVICE        | 서비스 매출은 있으나 바이오 funding cycle에 민감 | backlog, 고객 다변화, OP 개선          |
| DIGITAL_HEALTHCARE_AI       | 논문·PoC와 매출화 간극 큼                  | 허가, 병원도입, 수가, 매출                |
| TELEHEALTH_BEHAVIORAL       | CAC·개인정보·광고비 리스크 큼                | 보험/고용주 계약, 낮은 CAC, FCF          |
| PAYMENT_FINTECH_INFRA       | 사용자 수보다 take rate·수익성이 중요         | 거래액, take rate, 흑자·FCF          |
| DIGITAL_ASSET_TOKENIZATION  | 규제 승인 전까지 테마성 큼                   | 실제 발행·거래량·수수료                   |
| RAIL_INFRASTRUCTURE         | 실제 계약이면 후보, 정책만이면 이벤트             | 계약금액, 납품 스케줄, 마진                |
| NUCLEAR_SMR_GRID_POLICY     | AI 전력수요는 강하지만 허가·비용·PPA 필요        | PPA, 확정 프로젝트, 기자재 매출            |
| DATA_CENTER_REIT_INFRA      | AI 수요는 강하지만 CAPEX·funding cost 큼  | tenant, occupancy, AFFO         |
| COLD_CHAIN_REIT_LOGISTICS   | 수요는 반복적이나 에너지비·금리 리스크             | occupancy, NOI/AFFO             |
| INDUSTRIAL_GASES_SEMI_INFRA | fab utility-like 매출 가능            | 장기 공급계약, fab ramp-up            |
| ADVANCED_PACKAGING_COWOS    | AI packaging 병목 가능                | 실제 수주, revenue growth, yield 안정 |

이쪽은 “두껍게 파긴 했지만, 반드시 가격검증과 실제 재무 검증이 필요한 축”이다.

---

## Red / 4B / 반례 방어 중심

이쪽은 테마가 강하게 붙어도 Green을 거의 막아야 하는 축이다.

| Archetype                        | 왜 위험한가                         |
| -------------------------------- | ------------------------------ |
| BATTERY_MATERIALS_CAPEX_OVERHEAT | EV 수요 둔화, CAPA 과잉, 광물가격        |
| LITHIUM_BATTERY_RAW_MATERIAL     | 리튬가격 cycle, 광산 재가동, 가격 급락      |
| POWER_SEMICONDUCTOR_SIC          | SiC narrative와 고부채·CAPEX 실패 위험 |
| CHEMICAL_SPREAD                  | 중국·중동 공급과잉, spread reversal    |
| SHIPPING_FREIGHT_CYCLE           | 운임 peak 이후 EPS 정상화             |
| CONSTRUCTION_REAL_ESTATE_CREDIT  | PF, 미분양, 신용위험                  |
| EVENT_DISEASE_PEST_DEMAND        | 엠폭스·빈대·마스크·진단키트 one-off        |
| SPECULATIVE_SCIENCE_THEME        | 초전도체·맥신·그래핀, 상용화 전 Green 금지    |
| METAVERSE_NFT_THEME              | 수익모델 없이 price-only rally       |
| NORTH_KOREA_POLICY_EVENT         | 남북경협·금강산·개성공단, event_only      |
| AI_DRUG_DISCOVERY_PLATFORM       | AI 신약개발 narrative와 실제 승인 간극    |
| GENE_THERAPY_RARE_DISEASE        | 승인 후에도 상업화·환급·cash burn 리스크    |
| SERVICE_KIOSK_SELF_CHECKOUT      | 절도·고객불만·일회성 장비판매               |
| AGRI_LIVESTOCK_FOOD_COMMODITY    | 질병·사료·날씨·가격 cycle              |

이쪽은 성공사례보다 **반례와 4C 조건**을 더 많이 쌓는 쪽으로 갔고, 그게 맞다.

정책·재난·과학 테마는 대부분 event premium 또는 theme overheat이고, Stage 3-Green보다 RedTeam과 4B 방어가 중요하다고 이미 정리되어 있다.
2차전지 쪽도 Green보다 과열 방어가 우선이며, 소재·전고체·폐배터리는 실제 계약·수익성·FCF 확인 전까지 Stage 3-Green을 제한해야 한다고 정리되어 있다.

---

# 4. “다 기억하고 차례대로 얇은 애들도 두껍게 팠냐?”에 대한 답

응. 방향은 이렇게 진행됐다.

## 1단계: 테마 흡수

처음에는 네가 준 긴 테마 리스트를 전부 흡수할 수 있는 구조를 만들었다.

```text
12개 대섹터
→ 70개 안팎 archetype/sub-archetype
→ 200개+ raw theme tag
```

업로드된 `Theme Tag Map v0.5`가 이 단계의 기준 지도야. 산업재·AI반도체·2차전지·소재·소비재·금융·바이오·플랫폼·모빌리티·건설·정책이벤트·농업생활서비스로 나눠서 각 테마를 primary archetype과 Green 정책으로 매핑했다.

## 2단계: 얇은 archetype 보강

그다음에는 얇았던 애들을 계속 두껍게 팠다. 대표적으로:

```text
CRO
의료AI
원격의료
컨택센터 AI
키오스크
콜드체인 REIT
데이터센터 REIT
데이터센터 물 재활용
반도체 산업가스
광통신
AI 서버 ODM
Neocloud
SiC
AI 신약개발
유전자치료제
규제형 소비재
스마트팜
탄소배출권
종합상사
LNG 에너지 트레이딩
OLED
MLCC
위성통신
방산 AI 소프트웨어
드론 counter-UAS
```

이것들은 처음 70개 지도에서는 묶여 있었거나 얇게 처리됐는데, 이후에는 점수비중과 성공/반례 조건까지 세분화했다.

## 3단계: 주요 archetype 재보정

이미 두껍게 팠던 핵심 축도 다시 파면서 교정했다.

```text
HBM
전력기기/변압기
AI 데이터센터 인프라
K뷰티
K푸드
방산
조선
금융/보험/밸류업
2차전지
화학
건설 PF
클라우드/SaaS
보안
의료기기
바이오시밀러
GLP-1
```

예를 들어 반도체는 처음부터 HBM, 장비, 소재, AI칩을 구분했지만, 이후에는 HBM과 범용 DRAM/NAND, AI 서버 ODM, Neocloud, CoWoS, optical networking, industrial gases까지 더 나눴다. 이건 “반도체 테마” 하나로 점수 주지 않기 위해서야. HBM은 Green 가능성이 높지만, CXL·뉴로모픽·AI칩 관련주는 실제 채택·매출 전까지 Watch/Red로 둬야 한다는 원칙도 유지되고 있다.

## 4단계: 가격경로 검증 계획 추가

마지막으로 단순 case library가 아니라, 각 archetype을 실제 주가 경로로 검증하는 계획까지 붙였다.

```text
Stage 1:
산업 변화 또는 테마 최초 포착

Stage 2:
실제 계약·수주·매출·EPS 상향 확인

Stage 3:
중장기 EPS/FCF 상향 + valuation frame 변화

검증:
MFE_90D / 180D / 1Y / 2Y
MAE_90D / 180D
drawdown_after_peak
EPS revision 지속성
PBR/PER band 변화
event 이후 회복 여부
```

이건 서생원식 기본 점수축과도 맞아. 서생원식 점수화는 EPS 폭발성, 이익 지속성/가시성, 공급 병목/가격 결정력, 시장 오해, 밸류에이션 리레이팅 여지, 자본배분, 정보 신뢰도를 보는 구조로 정리되어 있다.

---

# 5. 현재 기준 “층위”를 다시 정리하면

지금은 이렇게 보는 게 가장 정확하다.

```text
Layer 0: Raw theme tag
- 200개+ 테마명
- 편의점, HBM, 스테이블코인, 초전도체, K푸드, 방산, 폐배터리 등

Layer 1: Large sector
- 12개 대섹터
- 큰 서랍 역할

Layer 2: Canonical archetype
- 대략 70개 안팎
- theme_tag_map_v05의 주 분류

Layer 3: Deep sub-archetype
- 이후 딥서치로 추가된 세부축
- 현재는 90~110개 안팎으로 봐도 됨

Layer 4: Case library
- 성공 후보
- 구조적 성공
- cyclical success
- event premium
- false positive
- 4B watch
- 4C thesis break

Layer 5: Price-path validation
- stage date
- MFE/MAE
- drawdown
- score-price alignment
- shadow scoring
```

즉, 처음의:

```text
12개 대섹터
→ 70개 안팎 archetype
→ 200개+ raw theme tag
```

는 여전히 맞다.

다만 이후 작업으로:

```text
70개 archetype
→ 90~110개 수준의 세부 sub-archetype 후보
```

까지 깊어진 상태다.

---

# 6. 기억해야 할 핵심 축

앞으로 헷갈리지 않으려면 이렇게 기억하면 돼.

## 대섹터는 12개로 고정

더 늘리지 않는 게 좋다.
대섹터가 늘어나면 지도 자체가 복잡해져.

## canonical archetype은 70개 안팎

에이전트 코드/CSV에서는 이 정도가 기본 분류 단위가 좋다.

## deep sub-archetype은 계속 늘어날 수 있음

딥서치하면서 다음처럼 늘어나는 건 정상이다.

```text
AI_DATA_CENTER_INFRASTRUCTURE
→ AI_DATA_CENTER_COOLING
→ OPTICAL_NETWORKING_AI_DC
→ AI_DC_POWER_EQUIPMENT
→ DATA_CENTER_REIT_INFRA
→ DATA_CENTER_WATER_REUSE
→ AI_GRID_FLEXIBILITY_SW
```

이건 대분류를 망가뜨리는 게 아니라, 점수비중을 정교하게 하는 “하위 렌즈”다.

---

# 7. 지금까지의 결론

응. **다 기억하고 있고, 차례대로 얇은 애들도 두껍게 파고든 게 맞다.**

현재 상태는 이렇게 보면 된다.

```text
테마 흡수:
거의 완료.

12개 대섹터:
유지.

70개 안팎 canonical archetype:
기본 지도 역할.

추가된 deep sub-archetype:
90~110개 수준까지 확장.

성공/반례:
많이 쌓였고, 특히 Green 가능 / Watch / Red archetype 경계가 선명해짐.

점수비중:
v2.3 수준의 가설 지도로 두꺼워짐.

남은 핵심:
실제 가격경로 검증.
```

그리고 제일 중요한 건, 이 모든 작업이 서생원식 핵심과 같은 방향이라는 점이야. 종목명이나 테마명이 아니라, **EPS 체급 변화와 밸류에이션 기준 변화가 동시에 일어나는 구조**를 찾는 방식이다. 서생원식 요약도 결국 “시장 과거 프레임에 갇힌 사이 EPS 체급과 밸류에이션 기준이 동시에 바뀌는 종목을 크게 사고, 리레이팅이 끝날 때까지 들고 간다”는 구조다.

다음에 진행할 때는 새로 더 파기 전에, 이 정리 기준으로:

```text
1. 12개 대섹터 고정
2. 70개 canonical archetype 정리
3. 추가 sub-archetype은 parent archetype 밑에 귀속
4. cases_vXX를 parent/sub-archetype별로 정렬
5. 가격경로 검증 계획을 붙임
```

이 순서로 한 번 정돈하고 가는 게 맞다.
