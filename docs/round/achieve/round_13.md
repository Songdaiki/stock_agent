응. 다음 라운드 진행할게.
그리고 질문한 부분에 대해 먼저 정확히 말하면:

> **우리가 “점수비중을 잘 정규화하고 있느냐”는 아직 최종 확정 단계는 아니지만, 방법론은 맞게 가고 있어.**
> 지금은 `성공사례 → 어떤 점수축을 강화해야 하는지`, `반례 → 어떤 점수축을 제한하거나 Green을 막아야 하는지`, `주가 경로 → 그 점수 판단이 실제 리레이팅과 맞았는지`를 맞추는 단계야.

현재 레포는 아직 `fixture_only: True`, mapped symbols 13개, archetypes used 8개 상태고, case library도 모든 archetype이 `insufficient_case_coverage`로 남아 있어. 그러니까 지금은 scoring을 바로 바꿀 때가 아니라, **테마 전체를 품는 case/archetype matrix를 더 깊게 채우는 단계**가 맞다.

기존 정신은 그대로야. 핵심은 **산업 구조 변화 → EPS/FCF 체급 변화 → 시장의 과거 프레임 오해 → 밸류에이션 리레이팅 → 논리 훼손 전까지 보유**다. 테마명, 단기 주가 급등, 일회성 실적은 절대 이걸 대체하면 안 된다.

---

# Round 10: 테마 흡수 구조와 신규 case 보강

이번 라운드의 핵심은 세 가지야.

```text
1. 네가 준 세부 테마를 더 촘촘한 archetype으로 흡수한다.
2. 새 archetype마다 성공사례/반례/4B/4C 조건을 만든다.
3. 점수비중이 실제 주가 리레이팅과 맞는지 검증할 수 있게 한다.
```

중요한 원칙은 이거야.

```text
테마명 = 검색/분류용 tag
점수 = evidence와 archetype 구조에서 발생
성공 = 점수와 주가/실적 경로가 정방향
반례 = 점수상 좋아 보였지만 주가·실적·4C가 어긋난 사례
```

---

# 1. 테마 구조를 이렇게 확장하는 게 맞다

네가 준 테마 목록을 다 품으려면 현재의 10개 대섹터보다 한 단계 더 촘촘해야 해. 내 기준으로는:

```text
12개 대섹터
→ 60~70개 archetype/sub-archetype
→ 200개+ theme tag
```

구조가 가장 안정적이야.

## 대섹터 v0.4

| 대섹터           | 흡수할 테마 예시                                       |
| ------------- | ----------------------------------------------- |
| 산업재·수주·인프라    | 전력설비, 전선, 방산, 조선, 건설기계, 피팅밸브, 원전, 철도            |
| AI·반도체·전자부품   | HBM, CXL, 시스템반도체, PCB, OLED, MLCC, 유리기판, 클린룸    |
| 2차전지·전기차·친환경  | 2차전지 소재/부품/장비, 폐배터리, 전고체, 전기차 인프라, 수소, 태양광, 풍력  |
| 소재·스프레드·전략자원  | 화학, 정유, 철강, 비철, 리튬, 희토류, 구리, 금은, 그래핀, 맥신        |
| 소비재·유통·브랜드    | 편의점, 홈쇼핑, 라면, K푸드, 음식료, 화장품, 의류, 건기식            |
| 금융·자본배분·디지털금융 | 은행, 보험, 증권, 금융지주, 고배당, 밸류업, 결제, STO, 스테이블코인     |
| 바이오·헬스케어·의료기기 | CMO, CRO, 바이오시밀러, 임상, 의료AI, 미용기기, 보톡스, 임플란트, 진단 |
| 플랫폼·콘텐츠·SW·보안 | 게임, 엔터, 미디어, 클라우드, AI, IT보안, 딥페이크, 메타버스, NFT    |
| 모빌리티·운송·레저    | 항공, 해운, 택배, 렌터카, 중고차, 여행, 카지노, 면세, 골프           |
| 건설·부동산·건자재    | 건설사, 리츠, 개발신탁, 건자재, 시멘트, 철근, 가구                 |
| 정책·지정학·재난·이벤트 | 남북경협, 우크라 재건, 네옴시티, 세종시, 지진, 폭염, 황사, 전염병        |
| 농업·생활서비스·기타   | 교육, 취업, 키즈, 유아용품, 스마트팜, 농기계, 양돈, 육계, 사료, 참치     |

---

# 2. 새로 확정해야 할 archetype

이번 라운드에서 특히 추가해야 할 건 아래야.

```text
RETAIL_CONVENIENCE_OFFLINE
ECOMMERCE_FRESH_LOGISTICS
INSURANCE_UNDERWRITING_CYCLE
PAYMENT_FINTECH_INFRA
DIGITAL_ASSET_TOKENIZATION
BEAUTY_OEM_ODM_SUPPLYCHAIN
AGRI_LIVESTOCK_FOOD_COMMODITY
BUILDING_MATERIALS_CYCLE
RENEWABLE_ENERGY_POLICY
HYDROGEN_FUEL_CELL_INFRA
SOLAR_TARIFF_SUPPLYCHAIN
TIRE_AUTO_COMPONENT_SPREAD
EVENT_DISEASE_PEST_DEMAND
SPECULATIVE_SCIENCE_THEME
WASTE_RECYCLING_ENVIRONMENT
MEDIA_AD_CONTENT_CYCLE
CLOUD_AI_SOFTWARE_INFRA
SECURITY_IDENTITY_DEEPFAKE
BATTERY_RECYCLING_ESS_SHIFT
```

이렇게 해야 편의점, 손해보험, 스테이블코인, 콜드체인, 타이어, 화장품 OEM, 엠폭스, 초전도체, 빈대, 폐배터리 같은 세부 테마가 무리 없이 들어간다.

---

# 3. 신규 보강: 결제서비스 / STO / 스테이블코인

## Archetype

```text
PAYMENT_FINTECH_INFRA
DIGITAL_ASSET_TOKENIZATION
```

## 포함 테마

```text
결제서비스
토스 관련주
지역화폐
신용정보
STO
스테이블코인
디지털자산·블록체인
NFT
```

## 구조

```text
규제 승인
→ 실제 발행/거래량/결제망 채택
→ 수수료·예치금·스프레드 수익
→ 반복 금융 인프라 매출
```

Toss는 해외 확장과 원화 스테이블코인 발행 의지를 밝힌 사례인데, 아직 규제 승인과 실제 발행·수익모델 확인이 필요하므로 Stage 1~2 후보로만 봐야 한다. ([Reuters][1])

## 성공 후보

| 케이스              | 분류                | 봐야 할 것                     |
| ---------------- | ----------------- | -------------------------- |
| Toss / 원화 스테이블코인 | success_candidate | 규제 승인, 발행량, 거래량, 수익모델      |
| 결제 PG사           | success_candidate | 거래액, take rate, 비용구조       |
| STO 플랫폼          | success_candidate | 토큰증권 법제화, 실제 발행, 수탁/중개 수수료 |
| 신용정보/데이터 기업      | success_candidate | 반복 데이터 매출, 금융사 채택          |

## 반례

| 반례                 | 이유                 |
| ------------------ | ------------------ |
| 코인 테마만 있는 기업       | 실질 매출 없음           |
| STO 법제화 기대만 있는 관련주 | 발행 실적과 수익모델 없음     |
| 스테이블코인 규제 지연       | Stage 1 제한 또는 4C   |
| NFT 테마             | 대부분 theme_overheat |

## 점수비중 초안

```text
EPS/FCF: 16
Structural Visibility: 18
Bottleneck/Pricing: 8
Market Mispricing: 16
Valuation: 12
Risk Penalty: regulation / security / adoption
```

## Green 조건

```text
규제 승인 + 실제 거래량 + 수수료 모델 + 반복 매출
```

규제 기대만 있으면 Green 금지다.

---

# 4. 신규 보강: 보험 / 손해보험 / 생명보험

## Archetype

```text
INSURANCE_UNDERWRITING_CYCLE
FINANCIAL_SPREAD_BALANCE_SHEET
VALUE_UP_SHAREHOLDER_RETURN
```

## 포함 테마

```text
손해보험
생명보험
화재
고배당주
금융지주회사
밸류업 지수 편입
```

## 구조

```text
손해율 / CSM / ROE / 자본비율 / 주주환원
→ PBR-ROE 프레임 리레이팅
```

보험은 은행과 다르게 NIM보다 **손해율, CSM, K-ICS 또는 자본비율, 주주환원**이 핵심이야. 단순 고배당이나 저PBR만으로는 안 된다.

## 성공 후보

| 케이스         | 분류                | 봐야 할 것                  |
| ----------- | ----------------- | ----------------------- |
| 삼성화재 / DB손보 | success_candidate | 손해율, CSM, ROE, 자본비율, 환원 |
| 생명보험사       | success_candidate | CSM, 금리, 자본비율, 배당여력     |
| 금융지주        | success_candidate | ROE, CET1, 자사주, 배당      |

## 반례

| 반례            | 이유                    |
| ------------- | --------------------- |
| 단순 저PBR 보험주   | ROE/환원 없으면 value trap |
| 자본비율 낮은 보험    | 배당·자사주 제한             |
| 손해율 악화        | underwriting 4C       |
| PF/충당금 리스크 금융 | credit cost 4C        |

## 점수비중 초안

```text
EPS/FCF: 15
Structural Visibility: 20
Bottleneck/Pricing: 5
Market Mispricing: 15
Valuation: 25
Capital Allocation: 10
Information Confidence: 5
```

## Green 조건

```text
ROE/CSM 개선 + 자본비율 안정 + 실제 환원정책 + PBR 리레이팅 여지
```

고배당 하나만 있으면 Green 금지다.

---

# 5. 신규 보강: K뷰티 OEM/ODM / 원재료·부자재

## Archetype

```text
BEAUTY_OEM_ODM_SUPPLYCHAIN
K_BEAUTY_EXPORT_DISTRIBUTION
```

## 포함 테마

```text
화장품 OEM-ODM
화장품 원재료 및 부자재
화장품 브랜드
K뷰티
```

## 구조

```text
K뷰티 글로벌 수요
→ ODM/OEM 주문 증가
→ 고객사 다변화
→ OPM/ROE 개선
```

K뷰티는 한국이 2024년에 미국 화장품 수출에서 프랑스를 앞섰고, 미국 주요 리테일 채널 진입이 중요한 확장 포인트로 보도됐다. 이건 K뷰티 archetype의 Stage 1~2 신호가 될 수 있지만, tariff와 브랜드 난립, 중국 둔화, 오프라인 sell-through는 반드시 확인해야 한다. ([Reuters][2])

## 성공 후보

| 케이스            | 분류                | 봐야 할 것                 |
| -------------- | ----------------- | ---------------------- |
| 코스맥스 / 한국콜마    | success_candidate | 글로벌 고객사, ODM 수주, OPM   |
| 실리콘투           | success_candidate | 글로벌 유통, 브랜드 다변화, 반복 주문 |
| APR / Medicube | success_candidate | 디바이스, 브랜드, 해외 채널       |
| 원재료/부자재 업체     | success_candidate | 고객사 다변화, 반복 수요         |

## 반례

| 반례               | 이유            |
| ---------------- | ------------- |
| 중국 의존 화장품        | 중국 채널 둔화      |
| viral-only 브랜드   | 반복 주문 없음      |
| channel stuffing | 재고/매출채권 악화    |
| tariff/규제        | 미국 관세, 인증 리스크 |

## 점수비중 초안

```text
EPS/FCF: 22
Structural Visibility: 23
Bottleneck/Pricing: 12
Market Mispricing: 16
Valuation: 13
Risk Penalty: inventory / receivables / China dependency
```

## Green 조건

```text
수출 증가 + 고객/브랜드 다변화 + OPM 개선 + 재고/채권 리스크 낮음
```

화장품 테마만으로는 Green 금지다.

---

# 6. 신규 보강: 2차전지 / 폐배터리 / ESS

## Archetype

```text
BATTERY_MATERIALS_CAPEX_OVERHEAT
BATTERY_EQUIPMENT_PARTS
BATTERY_RECYCLING_ESS_SHIFT
```

## 포함 테마

```text
2차전지 소재
2차전지 부품
2차전지 공정장비
2차전지 생산·판매
폐배터리
전고체 배터리
리튬
전기차 화재
ESS
```

## 구조

```text
EV 성장 기대
→ 소재/부품/CAPA 투자
→ EV 수요 둔화·광물가격·CAPA 과잉 리스크
→ ESS 전환이 일부 보완 가능
```

LG에너지솔루션은 EV 배터리 수요 둔화와 미국 정책·관세 불확실성을 경고했고, ESS 생산 확대와 일부 EV 라인의 ESS 전환을 계획했다. 이건 2차전지 archetype에서 “EV 소재 Green 제한 + ESS 전환 watch”를 동시에 보여주는 사례다. ([Reuters][3])
또 GM-LG JV의 Ohio 배터리 공장은 EV 수요 둔화로 가동 재개 일정이 불확실했고, Tennessee 공장은 ESS 셀 생산으로 전환하는 흐름이 나타났다. ([Reuters][4])

## 성공 후보

| 케이스        | 분류                | 봐야 할 것              |
| ---------- | ----------------- | ------------------- |
| ESS 전환 배터리 | success_candidate | ESS 수요, LFP, 가동률 개선 |
| 폐배터리       | success_candidate | 실제 회수량, 금속가격, 마진    |
| 2차전지 공정장비  | success_candidate | 수주/납품/고객사 CAPEX     |
| 전고체 배터리    | watch_only        | 상용화 전 Green 제한      |

## 반례

| 반례             | 이유                 |
| -------------- | ------------------ |
| 에코프로비엠/에코프로 과열 | valuation/crowding |
| EV 수요 둔화       | 매출/가동률 훼손          |
| 광물가격 하락        | 판가/마진 훼손           |
| CAPA 과잉        | FCF 악화             |

## 점수비중 초안

```text
EPS/FCF: 20
Structural Visibility: 16
Bottleneck/Pricing: 14
Market Mispricing: 10
Valuation: 10
Risk Penalty: very high
```

## Green 조건

매우 제한적이다.

```text
장기계약 + 가격전가 + 수요 지속 + FCF 훼손 없는 CAPEX
```

EV 수요 기대나 폐배터리 테마만으로 Green 금지.

---

# 7. 신규 보강: 수소 / 태양광 / 풍력 / 탄소배출권

## Archetype

```text
RENEWABLE_ENERGY_POLICY
SOLAR_TARIFF_SUPPLYCHAIN
HYDROGEN_FUEL_CELL_INFRA
```

## 포함 테마

```text
태양광
풍력
탄소배출권
수소차 연료전지
수소차 인프라
수소차 기타부품
LNG 발전유통
스마트그리드
```

## 구조

```text
정책 / 보조금 / CAPEX
→ 실제 수주·생산·가동률
→ OP/EPS 전환
```

현대차는 울산에 약 9,300억원 규모의 수소연료전지 생산시설을 착공했고, 2027년 완공 후 승용차·상용차·건설기계·선박 등에 쓰일 연료전지와 전해조를 생산할 계획이다. 이건 수소 테마 중에서도 실제 CAPEX가 있는 Stage 1~2 후보로 볼 수 있다. ([Reuters][5])

## 성공 후보

| 케이스           | 분류                | 봐야 할 것                |
| ------------- | ----------------- | --------------------- |
| 현대차 수소연료전지 공장 | success_candidate | 실제 CAPEX, 생산능력, 고객/수요 |
| 연료전지 업체       | success_candidate | 수주, 가동률, 반복 서비스       |
| 풍력 기자재        | success_candidate | 터빈/타워 수주, 정책 지원       |
| 태양광 공급망       | watch_only        | tariff, 보조금, 원가       |

## 반례

| 반례           | 이유          |
| ------------ | ----------- |
| 태양광 관세/공급망   | 정책·관세 리스크   |
| 보조금 의존 사업    | 정책 변경 시 4C  |
| 수소 테마만 있는 기업 | 실제 생산/매출 없음 |
| 풍력 프로젝트 지연   | 인허가·원가 리스크  |

## 점수비중 초안

```text
EPS/FCF: 18
Structural Visibility: 18
Bottleneck/Pricing: 12
Market Mispricing: 12
Valuation: 10
Risk Penalty: policy / subsidy / supply chain
```

## Green 조건

```text
실제 CAPEX + 수주/고객 + 가동률 + OP/EPS 전환
```

정책 테마만으로 Green 금지.

---

# 8. 신규 보강: 타이어 / 자동차 부품 / 경량화

## Archetype

```text
TIRE_AUTO_COMPONENT_SPREAD
AUTO_MOBILITY_COMPONENTS
```

## 포함 테마

```text
타이어
현대·기아차 부품주
자동차 연비개선 경량화
전기차 부품
자율주행
카메라
스마트폰 부품 일부
```

## 구조

```text
완성차 판매 / OE·RE 타이어 수요
→ ASP와 원재료 spread
→ OPM 개선
→ 고객사 다변화
```

Kumho Tire는 2025년 광주공장 화재로 생산이 중단됐고, 해당 공장은 글로벌 생산능력의 약 20%를 차지했다. 이후 주가가 8% 하락했다는 보도도 있어, 타이어/부품 archetype의 4C 반례로 좋다. ([Reuters][6]) ([Reuters][7])

## 성공 후보

| 케이스          | 분류                | 봐야 할 것                     |
| ------------ | ----------------- | -------------------------- |
| 한국타이어        | success_candidate | RE/OE mix, ASP, 원재료 spread |
| 현대모비스 / HL만도 | success_candidate | ADAS/전장, 고객 다변화            |
| 경량화 부품       | success_candidate | 실제 채택률, 마진                 |
| 카메라/자율주행 부품  | success_candidate | 고객사와 매출화                   |

## 반례

| 반례          | 이유                          |
| ----------- | --------------------------- |
| 생산중단/화재     | supply disruption 4C        |
| 원재료 상승      | margin compression          |
| EV 수요 둔화 부품 | 고객사 수요 둔화                   |
| 단일 고객 부품주   | customer concentration risk |

## 점수비중 초안

```text
EPS/FCF: 20
Structural Visibility: 18
Bottleneck/Pricing: 10
Market Mispricing: 14
Valuation: 14
Risk Penalty: raw materials / customer concentration
```

## Green 조건

```text
고객 다변화 + OPM 개선 + 원재료 안정 + 반복 납품 visibility
```

---

# 9. 신규 보강: CDMO / CMO / 원료의약품

## Archetype

```text
CDMO_HEALTHCARE_CONTRACT
```

## 포함 테마

```text
CMO·원료의약품
바이오시밀러
CRO 일부
원료의약품
```

## 구조

```text
장기 생산계약 / capacity / 고객사 다변화
→ 가동률 상승
→ OP/FCF 개선
```

Samsung Biologics는 GSK로부터 미국 Rockville 생산시설을 2억 8천만 달러에 인수한다고 발표했고, 이 시설은 60,000L drug substance capacity를 가진다. 이건 CDMO archetype에서 실제 capacity·글로벌 고객·장기 수요를 보는 사례다. ([Reuters][8])

## 성공 후보

| 케이스          | 분류                | 봐야 할 것                   |
| ------------ | ----------------- | ------------------------ |
| 삼성바이오로직스     | success_candidate | capacity, 고객사, 가동률, 장기계약 |
| 셀트리온         | success_candidate | 바이오시밀러 매출화, 가격경쟁         |
| CMO 원료의약품 업체 | success_candidate | 계약/가동률/마진                |

## 반례

| 반례                 | 이유             |
| ------------------ | -------------- |
| capacity overbuild | 가동률 하락         |
| patent/litigation  | 제품 출시 지연       |
| 가격경쟁               | 마진 훼손          |
| 고객 집중              | 계약 지연 시 EPS 훼손 |

## 점수비중 초안

```text
EPS/FCF: 20
Structural Visibility: 24
Bottleneck/Pricing: 12
Market Mispricing: 12
Valuation: 12
Risk Penalty: litigation / capacity utilization
```

## Green 조건

```text
다년 생산 visibility + 높은 가동률 + 고객 다변화 + FCF conversion
```

---

# 10. 신규 보강: 플랫폼 / 카카오 / 보안·딥페이크

## Archetype

```text
PLATFORM_SOFTWARE_INTERNET
SECURITY_IDENTITY_DEEPFAKE
CLOUD_AI_SOFTWARE_INFRA
```

## 포함 테마

```text
클라우드 컴퓨팅
원격근무
컨택센터
광고
IT보안
딥페이크
생체인식
CCTV
스마트홈
AI 소프트웨어
```

## 구조

```text
반복 소프트웨어 매출
→ ARPU / take-rate / 보안수요 증가
→ OPM 레버리지
```

Kakao는 플랫폼 자산이 있지만, SM엔터 인수 관련 주가조작 혐의로 창업자에 대한 법적 리스크가 부각됐다. 이런 사례는 플랫폼 archetype에서 governance/legal risk가 valuation rerating을 막는 반례로 써야 한다. ([Reuters][9])

## 성공 후보

| 케이스 | 분류 | 봐야 할 것 |
|---|---|
| 더존비즈온 | SaaS/ERP 반복매출, OPM |
| 보안/생체인식 업체 | 반복 보안 수요, 공공/기업 계약 |
| 클라우드/컨택센터 | 구독형 매출, 비용 구조 |
| 딥페이크 보안 | 규제와 실제 도입계약 |

## 반례

| 반례                    | 이유        |
| --------------------- | --------- |
| Kakao governance risk | 법적/규제 리스크 |
| MAU만 높은 플랫폼           | 수익화 없음    |
| AI 비용 과다              | FCF 악화    |
| 보안 테마만 있는 기업          | 실제 계약 없음  |

## 점수비중 초안

```text
EPS/FCF: 20
Structural Visibility: 22
Bottleneck/Pricing: 8
Market Mispricing: 16
Valuation: 14
Risk Penalty: regulation / governance / AI cost
```

## Green 조건

```text
반복매출 + OPM 개선 + 규제/법적 리스크 낮음 + 주가 리레이팅
```

---

# 11. 신규 보강: 지주 / Korea Zinc / 전략금속

## Archetype

```text
RARE_METALS_STRATEGIC_MATERIALS
HOLDING_RESTRUCTURING_GOVERNANCE
VALUE_UP_SHAREHOLDER_RETURN
```

## 포함 테마

```text
비철금속
구리
리튬
희토류
금은
부동산 자산 보유
밸류업
고배당주
지주사
```

## 구조

```text
전략소재 / 제련마진 / 공급망 / 경영권 / 자본배분
```

Korea Zinc는 MBK·Young Poong의 공개매수 발표 후 주가가 19.8% 상승했다. 이건 전략소재 rerating이 아니라 **event premium과 governance risk를 분리해야 하는 사례**다. ([Reuters][10])
SK스퀘어는 SK하이닉스 지분가치 대비 저평가, 자사주 매입·소각, 독립이사 선임이 결합된 value-up 후보로 볼 수 있다. ([Reuters][11])

## 성공 후보

| 케이스        | 분류                                  | 봐야 할 것                       |
| ---------- | ----------------------------------- | ---------------------------- |
| SK스퀘어      | success_candidate                   | NAV discount, 자사주 소각, 자회사 가치 |
| Korea Zinc | event_premium / strategic candidate | 경영권 이벤트와 FCF 구조 변화 분리        |
| 고려아연류 전략금속 | success_candidate                   | 제련마진, 공급망, 자본배분              |

## 반례

| 반례              | 이유                         |
| --------------- | -------------------------- |
| 공개매수 이벤트만 있는 종목 | EPS/FCF 변화 없음              |
| 자사주 매입 후 미소각    | value-up 실패                |
| 경영권 분쟁 장기화      | 투자 지연, governance discount |
| 순수 금속가격 상승      | commodity cycle            |

## 점수비중 초안

```text
EPS/FCF: 18
Structural Visibility: 16
Bottleneck/Pricing: 15
Market Mispricing: 16
Valuation: 15
Capital Allocation: 10
Risk Penalty: governance/event risk
```

## Green 조건

```text
FCF 개선 + 자본배분 실행 + governance rerating
```

이벤트 프리미엄만으로 Green 금지.

---

# 12. 신규 보강: 메모리 / HBM / AI 반도체

## Archetype

```text
MEMORY_HBM_CAPACITY
AI_DATA_CENTER_INFRASTRUCTURE
SEMI_EQUIPMENT_CAPEX
```

SK하이닉스는 구조적 성공사례이면서 4B-watch 기준을 잡는 핵심 케이스야. 빅테크 고객들이 SK하이닉스 공급 확보를 위해 생산라인·EUV 장비 자금지원과 장기계약, 가격밴드, 선수금 구조를 제안했다는 보도는 Stage 3 근거에 해당한다. ([Reuters][12])
동시에 SK하이닉스 주가는 2025년 274%, 2026년 200% 이상 상승하며 시총 1조 달러에 근접했다는 보도가 있어서, 성공 후 4B-watch의 표본으로도 써야 한다. ([Reuters][13])

## 점수비중 초안

```text
EPS/FCF: 24
Structural Visibility: 21
Bottleneck/Pricing: 19
Market Mispricing: 15
Valuation: 12
Risk Penalty: cycle / capex reversal
```

## Green 조건

```text
HBM 수요
DRAM/NAND 가격 상승
공급규율
장기계약/선수금/price band
CAPA constraint
multiple-year consensus revision
```

## 4B 조건

```text
주가 1~2년 급등
시총/멀티플 포화
고객사 가격 저항
CAPEX 증설 뉴스
모두가 AI memory rerating 인정
```

---

# 13. 신규 보강: 완성차 / 하이브리드 / 주주환원

## Archetype

```text
AUTO_MOBILITY_COMPLETED_VEHICLE
AUTO_MOBILITY_COMPONENTS
```

Hyundai Motor는 2030년 판매 30% 증가 목표, 하이브리드 라인업 확대, 2025~2027년 4조원 자사주 매입, 배당 확대를 발표했다. 이건 자동차 archetype에서 “믹스 개선 + 하이브리드 대응 + 주주환원 + valuation discount 해소”가 같이 있는 Stage 1~2 후보로 볼 수 있다. ([Reuters][14])

## 성공 후보

| 케이스        | 분류                | 봐야 할 것                  |
| ---------- | ----------------- | ----------------------- |
| 현대차        | success_candidate | 하이브리드, 판매 목표, FCF, 주주환원 |
| 기아         | success_candidate | 고마진 mix, 미국 판매, 주주환원    |
| 현대모비스/HL만도 | success_candidate | 전장/ADAS, 고객 다변화         |

## 반례

| 반례           | 이유           |
| ------------ | ------------ |
| EV 수요 둔화 부품주 | 고객사 수요 둔화    |
| 원가전가 실패 부품주  | OPM 훼손       |
| 관세/정책 리스크    | 4C           |
| 리콜/품질 비용     | margin break |

## 점수비중 초안

```text
EPS/FCF: 20
Structural Visibility: 18
Bottleneck/Pricing: 10
Market Mispricing: 15
Valuation: 17
Capital Allocation: 10
```

---

# 14. 이번 라운드 정리: 테마별 Green 정책

## Green 가능

```text
HBM
AI 데이터센터 인프라
전력설비
전선-케이블
방산
조선
K푸드
K뷰티 ODM/브랜드/유통
CDMO
의료기기 수출
금융 value-up
손해보험/생명보험 underwriting 개선
완성차 value-up
```

단, 반드시 실적·수주·수출·ROE·환원 등 증거 필요.

## Watch / Yellow 중심

```text
스테이블코인
STO
결제서비스
원전
수소
태양광
풍력
로봇
플랫폼
게임/IP
리테일
여행/항공/카지노
교육
전략금속/경영권
```

뉴스와 테마는 강할 수 있지만, 매출화·규제승인·계약·FCF 확인 전 Green 금지.

## Red / 4B 방어 중심

```text
초전도체
맥신
그래핀
엠폭스
빈대
황사마스크
코로나 진단
해운 운임 사이클
2차전지 과열
건설 PF
임상 뉴스만 있는 바이오
NFT/메타버스 테마
코인 테마만 있는 종목
```

이들은 주가가 급등해도 구조적 E2R이 아닐 가능성이 높아서, Stage 3-Green보다 RedTeam과 4B/4C 감지가 중요하다.

---

# 15. 지금까지의 답: 정규화가 제대로 되고 있나?

**방향은 맞다.**
하지만 아직 확정은 아니다.

정확히 말하면:

```text
현재:
성공/반례 기반 score-weight hypothesis를 만들고 있음

아직 필요한 것:
각 case의 stage price, peak price, MFE/MAE, drawdown_after_peak를 채워서 검증

검증 후:
점수비중을 shadow scoring으로 돌림

그 다음:
실제 StageClassifier에 반영
```

즉 지금은 “정규화 완료”가 아니라 **정규화할 근거를 제대로 쌓는 중**이야.

하지만 방식은 맞다.

```text
성공사례:
어떤 evidence가 EPS/FCF와 주가 리레이팅을 만들었는지 알려줌

반례:
어떤 evidence가 겉보기엔 좋아도 Green을 막아야 하는지 알려줌

주가 경로:
그 점수비중이 실제 시장에서 맞았는지 검증함
```

---

# 16. 다음 라운드에서 더 해야 할 것

다음은 이제 `theme_tag_map.csv` 초안과 `cases_v03` 후보를 더 구체화해야 해.

필요한 작업:

```text
1. 네가 준 테마 전체를 theme_tag_map으로 변환
2. 각 tag에 primary_archetype / secondary_archetype 부여
3. green_policy 부여:
   - green_allowed
   - watch_only
   - red_flag
   - event_only

4. 각 archetype별 최소 2개 성공 + 2개 반례를 채움
5. 각 case에 price_validation_status를 부여
6. agent가 가격 데이터를 채워 MFE/MAE 계산
7. 점수비중 shadow test
```

지금 라운드에서 새로 채운 핵심은:

```text
- 결제/STO/스테이블코인
- 보험/손해율/CSM
- K뷰티 OEM/ODM
- 2차전지 ESS/폐배터리
- 수소/태양광/풍력
- 타이어/자동차 부품
- CDMO
- 보안/딥페이크/플랫폼 리스크
- 전략금속/거버넌스
- HBM 4B-watch
- 완성차 value-up
```

이걸 계속 이어가면 네가 준 세부 테마들을 거의 다 흡수할 수 있어.

[1]: https://www.reuters.com/business/finance/south-korean-fintech-toss-plans-global-push-starting-australia-aims-issue-won-2025-09-09/?utm_source=chatgpt.com "South Korean fintech Toss plans global push starting in Australia, aims to issue won stablecoin"
[2]: https://www.reuters.com/world/asia-pacific/korean-beauty-startups-bet-booming-us-demand-outlasts-tariff-pain-2025-06-05/?utm_source=chatgpt.com "Korean beauty startups bet booming US demand outlasts tariff pain"
[3]: https://www.reuters.com/business/autos-transportation/lg-energy-solution-warns-slowing-ev-battery-demand-due-us-tariffs-policy-2025-07-25/?utm_source=chatgpt.com "LG Energy Solution warns of slowing EV battery demand due to U.S. tariffs, policy headwinds"
[4]: https://www.reuters.com/legal/litigation/gms-restart-date-ohio-battery-plant-uncertain-2026-05-12/?utm_source=chatgpt.com "GM-LG's restart date at Ohio battery plant uncertain"
[5]: https://www.reuters.com/world/asia-pacific/hyundai-motor-breaks-ground-680-million-hydrogen-fuel-cell-plant-south-korea-2025-10-30/?utm_source=chatgpt.com "Hyundai Motor breaks ground on $680 million hydrogen fuel cell plant in South Korea"
[6]: https://www.reuters.com/en/south-koreas-kumho-tire-plant-production-suspended-due-fire-2025-05-17/?utm_source=chatgpt.com "South Korea's Kumho Tire plant production suspended due to fire"
[7]: https://www.reuters.com/markets/europe/kumho-tire-shares-skid-after-weekend-fire-disrupts-production-2025-05-19/?utm_source=chatgpt.com "Kumho Tire shares skid after weekend fire disrupts production"
[8]: https://www.reuters.com/business/healthcare-pharmaceuticals/samsung-biologics-buy-us-drug-production-facility-gsk-280-mln-2025-12-21/?utm_source=chatgpt.com "Samsung Biologics to buy US drug production facility from GSK for $280 million"
[9]: https://www.reuters.com/business/south-korea-court-decide-arrest-warrant-kakao-founder-2024-07-22/?utm_source=chatgpt.com "South Korea court to decide on arrest warrant for Kakao founder"
[10]: https://www.reuters.com/markets/deals/private-equity-mbk-young-poong-launch-15-bln-tender-offer-korea-zinc-shares-2024-09-13/?utm_source=chatgpt.com "Private equity MBK, Young Poong launch $1.5 bln tender offer for Korea Zinc shares"
[11]: https://www.reuters.com/technology/artificial-intelligence/south-koreas-ai-chip-investor-announces-plan-share-buybacks-2024-11-21/?utm_source=chatgpt.com "South Korea's AI chip investor announces plan for share buybacks"
[12]: https://www.reuters.com/world/asia-pacific/sk-hynix-flooded-with-unprecedented-offers-big-tech-firms-secure-chip-supplies-2026-05-07/?utm_source=chatgpt.com "SK Hynix flooded with unprecedented offers from big tech firms to secure chip supplies"
[13]: https://www.reuters.com/world/asia-pacific/ai-boom-puts-sk-hynix-cusp-1-trillion-market-value-2026-05-14/?utm_source=chatgpt.com "AI boom puts SK Hynix on cusp of $1 trillion market value"
[14]: https://www.reuters.com/business/autos-transportation/hyundai-motor-targets-30-rise-sales-by-2030-it-expands-hybrid-lineup-2024-08-28/?utm_source=chatgpt.com "Hyundai targets 30% rise in sales by 2030, as it doubles hybrid lineups"
