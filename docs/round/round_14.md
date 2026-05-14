좋아. 이번 라운드는 **Round 11: 세부 테마 흡수형 case matrix 확장 + 성공/반례 기반 점수비중 초안 v0.4**로 정리할게.

먼저 답부터 말하면, **지금 우리가 하는 점수정규화 방향은 맞다.** 다만 아직 “완성된 점수표”가 아니라, **성공/반례/주가경로로 검증하기 위한 scoring hypothesis**를 만드는 중이야. 서생원식 핵심은 단순 테마가 아니라 “EPS/FCF 체급 변화 + 시장의 과거 프레임 + 밸류에이션 리레이팅”이고, 이 순서를 잃으면 안 된다.

---

# 0. 이번 라운드의 핵심 원칙

네가 준 긴 테마 리스트는 너무 많아서, 테마 하나마다 if문을 만들면 시스템이 망가져. 대신 이렇게 정리해야 해.

```text
테마 태그
→ 대섹터
→ E2R archetype
→ 성공/반례 case
→ evidence field
→ score weight
→ price-path validation
```

즉, `스테이블코인`, `편의점`, `HBM`, `초전도체`, `화장품 OEM`, `면세점`, `손해보험`, `폐배터리` 같은 이름은 **검색·분류용 태그**고, 최종 점수는 아래 구조에서 나와야 한다.

```text
EPS/FCF Explosion
Structural Visibility
Bottleneck / Pricing Power
Market Mispricing
Valuation Rerating Room
Capital Allocation
Information Confidence
Risk Penalty
```

이번 라운드에서는 특히 **신규/미흡 archetype**을 더 채우고, 성공사례와 반례를 통해 “점수비중을 어떻게 둬야 하는지”까지 정리한다.

---

# 1. RETAIL_CONVENIENCE_OFFLINE

편의점 / 홈쇼핑 / 음식료 유통 / 콜드체인

## 포함 테마

```text
편의점
홈쇼핑
음식료-유통
마켓컬리·오아시스 관련주
콜드체인
택배·종합물류 일부
키즈/유아용품 일부
```

## 핵심 구조

```text
점포망 / 물류망 / PB상품
→ same-store sales
→ 객단가 / 고마진 mix
→ 비용 레버리지
→ OPM / FCF 개선
```

## 성공 후보

| 케이스           | 판단                                  |
| ------------- | ----------------------------------- |
| BGF리테일 / CU   | 점포효율, PB상품, 해외점포, OPM 개선이 확인되면 후보   |
| GS리테일 / GS25  | 편의점 점포수보다 점포당 수익성, PB mix, 비용통제가 중요 |
| 콜드체인 물류       | 신선식품·의약품 물류 수요가 반복 매출로 이어질 때 후보     |
| 마켓컬리·오아시스 관련주 | 상장 기대가 아니라 실제 물류 효율·흑자전환·FCF 확인 필요  |

## 반례

| 반례                     | 왜 위험한가                         |
| ---------------------- | ------------------------------ |
| 홈쇼핑 구조 둔화              | TV 시청률·수수료·모바일 전환 실패 시 OPM 하락  |
| 신선식품 e-commerce 적자     | 매출은 늘어도 배송비·폐기율·물류비로 FCF 악화    |
| 상장 기대만 있는 관련주          | event premium일 뿐 EPS/FCF 변화 없음 |
| 중국 직구·저가 e-commerce 압박 | 유통마진 훼손 가능                     |

## Stage 기준

```text
Stage 1:
same-store sales 회복
점포 확대
PB/고마진 상품 뉴스
상장/지분 이벤트

Stage 2:
OPM 개선
재고 정상화
비용 레버리지
FY1/FY2 OP 상향

Stage 3:
점포 효율 구조 변화
물류/콜드체인 반복매출
FCF 개선
시장이 내수 저성장 유통 프레임으로 평가

4B:
소비 회복 모두 반영
점포 성장 한계
임대료/인건비 압박

4C:
재고 증가
온라인 경쟁 심화
소비 둔화
물류비 상승
```

## 점수비중 v0.4

```text
EPS/FCF: 18
Structural Visibility: 16
Bottleneck/Pricing: 5
Market Mispricing: 14
Valuation Rerating: 14
Capital Allocation: 3
Information Confidence: 5
Risk Penalty: 재고 / 물류비 / 온라인 경쟁
```

**정규화 포인트:**
편의점·유통은 Green이 가능하지만, **매출 성장만으로는 부족**하다. OPM과 FCF가 실제로 개선되어야 한다.

---

# 2. INSURANCE_UNDERWRITING_CYCLE

손해보험 / 생명보험 / 화재 / 고배당

## 포함 테마

```text
손해보험
생명보험
화재
고배당주
금융지주회사
밸류업 지수 편입
```

## 핵심 구조

```text
손해율 / CSM / ROE / 자본비율 / 주주환원
→ PBR-ROE 프레임 변화
→ 밸류업 리레이팅
```

보험은 은행과 다르게 **손해율, CSM, 자본비율, 환원정책**이 핵심이야. 삼성화재 같은 대형 손보사는 underwriting quality와 자본비율이 좋을 때 금융 value-up archetype의 성공 후보가 된다. 삼성화재는 국내 대표 손해보험사이고 자동차·장기·일반보험 포트폴리오를 갖고 있어, 보험 archetype의 기준 케이스로 쓰기 좋다. ([위키백과][1])

## 성공 후보

| 케이스            | 판단                         |
| -------------- | -------------------------- |
| 삼성화재 / DB손보    | 손해율, CSM, ROE, 자본비율, 환원 확인 |
| 생명보험사          | CSM, 금리, 자본비율, 배당여력 확인     |
| KB금융 / 신한 / 하나 | 보험은 아니지만 금융 value-up 비교군   |
| 메리츠금융          | 자본효율·환원정책 비교군              |

## 반례

| 반례            | 왜 위험한가                    |
| ------------- | ------------------------- |
| 단순 저PBR 보험주   | ROE/환원 없으면 value trap     |
| 자본비율 낮은 보험    | 배당·자사주 제한                 |
| 손해율 악화        | underwriting thesis break |
| PF/충당금 리스크 금융 | credit cost 증가 시 4C       |

## Stage 기준

```text
Stage 1:
value-up 공시
자사주/배당
저PBR
손해율 개선 뉴스

Stage 2:
ROE 개선
CSM 증가
K-ICS/CET1 안정
환원정책 실행

Stage 3:
PBR-ROE 프레임 변화
반복 환원정책
손해율 안정
시장이 아직 value trap 프레임으로 평가

4B:
PBR이 ROE 대비 정상화
모두가 value-up 성공주로 인정

4C:
손해율 악화
credit cost 증가
자본비율 악화
환원정책 후퇴
```

## 점수비중 v0.4

```text
EPS/FCF: 15
Structural Visibility: 20
Bottleneck/Pricing: 5
Market Mispricing: 15
Valuation Rerating: 25
Capital Allocation: 10
Information Confidence: 5
Risk Penalty: 손해율 / 자본비율 / PF·충당금
```

**정규화 포인트:**
보험·금융은 EPS 폭발보다 **ROE-PBR-환원정책의 정합성**이 중요하다. 저PBR만으로 Green을 주면 안 된다.

---

# 3. PAYMENT_FINTECH_INFRA / DIGITAL_ASSET_TOKENIZATION

결제서비스 / 토스 / STO / 스테이블코인

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

## 핵심 구조

```text
규제 승인
→ 실제 발행/거래량/결제망 채택
→ 수수료·예치금·스프레드 수익
→ 반복 금융 인프라 매출
```

Toss는 해외 확장과 원화 스테이블코인 발행 의지를 밝힌 대표적 후보지만, 아직 규제 승인과 실제 발행·수익모델 확인이 필요하므로 Stage 1~2 후보로 봐야 한다. ([Reuters][2])
스테이블코인은 cross-border나 closed-loop 결제에서는 장점이 있지만, open-loop retail payment에서는 소비자 보호·분쟁처리·사용성 측면의 구조적 약점이 있다는 연구가 있다. ([arXiv][3])
또 한국에서는 원화 스테이블코인 발행 주체를 두고 중앙은행과 입법권 사이의 긴장이 존재해, 규제 리스크가 매우 크다. ([Financial Times][4])

## 성공 후보

| 케이스              | 판단                           |
| ---------------- | ---------------------------- |
| Toss / 원화 스테이블코인 | 규제 승인, 발행량, 거래량, 수익모델 필요     |
| 결제 PG사           | 거래액, take rate, 비용구조, 반복 결제망 |
| STO 플랫폼          | 실제 발행, 수탁/중개 수수료, 법제화        |
| 신용정보/데이터 기업      | 반복 데이터 매출, 금융사 채택            |

## 반례

| 반례                 | 왜 위험한가             |
| ------------------ | ------------------ |
| 코인 테마만 있는 기업       | 실질 매출 없음           |
| STO 법제화 기대만 있는 관련주 | 발행 실적과 수익모델 없음     |
| 스테이블코인 규제 지연       | Stage 1 제한 또는 4C   |
| NFT 테마             | 대부분 theme overheat |

## Stage 기준

```text
Stage 1:
법안/규제 뉴스
사업 진출 발표
거래소/은행/핀테크 제휴

Stage 2:
실제 라이선스/발행/거래량
수수료 모델
금융기관 채택
반복 매출

Stage 3:
결제/수탁/정산 인프라로 고착
규제 리스크 낮음
FCF/OPM 개선
시장이 아직 테마주로 평가

4B:
규제 기대 과열
관련주 동반 급등
실적 대비 valuation 과다

4C:
규제 지연/불허
보안사고
거래량 부진
수익모델 부재
```

## 점수비중 v0.4

```text
EPS/FCF: 16
Structural Visibility: 18
Bottleneck/Pricing: 8
Market Mispricing: 16
Valuation Rerating: 12
Capital Allocation: 3
Information Confidence: 5
Risk Penalty: regulation / security / adoption
```

**정규화 포인트:**
디지털금융은 **규제 승인 + 실제 거래량 + 수익모델**이 있어야 Stage 2 이상. 법안 기대만으로 Green 금지.

---

# 4. BEAUTY_OEM_ODM_SUPPLYCHAIN

화장품 OEM/ODM / 원재료 / 부자재

## 포함 테마

```text
화장품 OEM-ODM
화장품 원재료 및 부자재
화장품 브랜드
K뷰티
```

## 핵심 구조

```text
K뷰티 글로벌 수요
→ ODM/OEM 주문 증가
→ 고객사 다변화
→ OPM/ROE 개선
→ 중국 화장품 프레임 탈피
```

K뷰티는 2024년 한국이 미국 화장품 수출에서 프랑스를 앞섰고, 미국 오프라인 채널 진입이 중요한 확장 포인트로 보도됐다. 이건 K뷰티 archetype의 Stage 1~2 신호가 될 수 있지만, tariff·경쟁심화·브랜드 난립·sell-through 둔화는 4B/4C 리스크다. ([Reuters][5])

## 성공 후보

| 케이스            | 판단                     |
| -------------- | ---------------------- |
| 코스맥스 / 한국콜마    | 글로벌 고객사, ODM 수주, OPM   |
| 실리콘투           | 글로벌 유통, 브랜드 다변화, 반복 주문 |
| APR / Medicube | 디바이스, 브랜드, 해외 채널       |
| 원재료/부자재 업체     | 고객사 다변화, 반복 수요         |

## 반례

| 반례               | 왜 위험한가        |
| ---------------- | ------------- |
| 중국 의존 화장품        | 중국 채널 둔화      |
| viral-only 브랜드   | 반복 주문 없음      |
| channel stuffing | 재고/매출채권 악화    |
| tariff/규제        | 미국 관세, 인증 리스크 |

## Stage 기준

```text
Stage 1:
미국/일본 수출 증가
K뷰티 viral
ODM 주문 증가

Stage 2:
FY1/FY2 OP/EPS 상향
OPM/ROE 개선
고객사 다변화
채널 확대

Stage 3:
반복 주문
오프라인/대형 리테일 진입
재고/채권 문제 없음
중국 의존도 하락
시장이 아직 중국 화장품주 프레임으로 평가

4B:
K뷰티 overcrowding
목표가 과열
경쟁 브랜드 난립

4C:
sell-through 둔화
재고 증가
매출채권 악화
tariff/regulation impact
```

## 점수비중 v0.4

```text
EPS/FCF: 22
Structural Visibility: 23
Bottleneck/Pricing: 12
Market Mispricing: 16
Valuation Rerating: 13
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: inventory / receivables / China dependency
```

**정규화 포인트:**
K뷰티는 Green 가능성이 있지만, **재고·매출채권·채널 stuffing**이 보이면 4C 쪽으로 바로 내려야 한다.

---

# 5. BATTERY_RECYCLING_ESS_SHIFT

2차전지 / 폐배터리 / ESS / 전고체

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

## 핵심 구조

```text
EV 성장 기대
→ 소재/부품/CAPA 투자
→ EV 수요 둔화·광물가격·CAPA 과잉 리스크
→ ESS 전환이 일부 보완 가능
```

GM-LG의 Ohio 배터리 공장은 EV 수요 둔화로 완전 재가동 시점이 불확실했고, Tennessee 공장은 ESS용 배터리셀 생산으로 전환되는 흐름이 나타났다. 이는 2차전지 archetype에서 **EV 소재 Green 제한 + ESS 전환 watch**를 동시에 보여주는 좋은 반례/전환 케이스다. ([Reuters][6])

## 성공 후보

| 케이스        | 판단                      |
| ---------- | ----------------------- |
| ESS 전환 배터리 | EV 둔화를 ESS 수요가 보완하는지 확인 |
| 폐배터리       | 실제 회수량, 금속가격, 마진 필요     |
| 2차전지 공정장비  | 고객사 CAPEX, 수주, 납품 필요    |
| 전고체 배터리    | 상용화 전 Green 제한          |

## 반례

| 반례             | 왜 위험한가             |
| -------------- | ------------------ |
| 에코프로비엠/에코프로 과열 | valuation/crowding |
| EV 수요 둔화       | 매출/가동률 훼손          |
| 광물가격 하락        | 판가/마진 훼손           |
| CAPA 과잉        | FCF 악화             |
| 전고체 테마         | 상용화 전 EPS/FCF 없음   |

## Stage 기준

```text
Stage 1:
장기계약
CAPA 증설
EV/ESS 수요 뉴스

Stage 2:
가격/마진 동반 개선
customer contract quality
FCF 훼손 없는 CAPEX
ESS 전환 실적화

Stage 3:
매우 제한적
장기계약 + 가격전가 + 수요지속 + valuation 여지

4B:
price runup
crowding
PER/PBR 과열
revision slowdown

4C:
EV 수요 둔화
광물가격 하락
CAPA 과잉
margin compression
```

## 점수비중 v0.4

```text
EPS/FCF: 20
Structural Visibility: 16
Bottleneck/Pricing: 14
Market Mispricing: 10
Valuation Rerating: 10
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: very high
```

**정규화 포인트:**
2차전지는 **성공 가능성보다 Green 오판 방어가 더 중요**하다. ESS 전환은 후보가 될 수 있지만, EV 소재 기대만으로 Green 금지.

---

# 6. HYDROGEN_FUEL_CELL_INFRA / RENEWABLE_ENERGY_POLICY

수소 / 태양광 / 풍력 / 탄소배출권

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

## 핵심 구조

```text
정책 / 보조금 / CAPEX
→ 실제 수주·생산·가동률
→ OP/EPS 전환
```

수소·태양광·풍력은 정책성이 강해서 Stage 1은 자주 나오지만, Stage 3는 실제 수주와 가동률, 수익성 검증이 필요하다. ESS·BESS는 AI 데이터센터 전력 안정화에도 연결될 수 있다. 최근 연구도 데이터센터 부하 변동을 완화하기 위해 ESS와 슈퍼커패시터를 결합하는 방식을 제안해, 향후 AI 데이터센터 인프라와 ESS가 연결될 수 있음을 보여준다. ([arXiv][7])

## 성공 후보

| 케이스           | 판단                       |
| ------------- | ------------------------ |
| 수소 연료전지 공장/설비 | 실제 CAPEX, 생산능력, 고객/수요 필요 |
| 연료전지 업체       | 수주, 가동률, 유지보수 반복매출       |
| 풍력 기자재        | 터빈/타워 수주, 정책 지원          |
| ESS/BESS      | AI DC·산업단지 전력 안정화 수요     |

## 반례

| 반례             | 왜 위험한가        |
| -------------- | ------------- |
| 태양광 관세/공급망 리스크 | 정책·통관·보조금 리스크 |
| 보조금 의존 사업      | 정책 변경 시 4C    |
| 수소 테마만 있는 기업   | 실제 생산/매출 없음   |
| 풍력 프로젝트 지연     | 인허가·원가 리스크    |

## Stage 기준

```text
Stage 1:
정책/보조금
수소/태양광/풍력 CAPEX
공장 착공
수주 뉴스

Stage 2:
실제 계약/가동률
OP/EPS 상향
보조금과 수익성 확인

Stage 3:
다년 수요
고객사/정부 수요 고정
정책 리스크 낮음
원가 경쟁력 확보

4B:
정책 기대 과열
보조금 수혜 선반영
CAPEX 부담 부각

4C:
보조금 축소
관세/통관/공급망 문제
프로젝트 지연
가동률 하락
```

## 점수비중 v0.4

```text
EPS/FCF: 18
Structural Visibility: 18
Bottleneck/Pricing: 12
Market Mispricing: 12
Valuation Rerating: 10
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: policy / subsidy / supply chain
```

**정규화 포인트:**
친환경 테마는 정책 신호만으로는 Green 금지. **수주·가동률·OP/EPS 전환**이 있어야 한다.

---

# 7. TIRE_AUTO_COMPONENT_SPREAD

타이어 / 자동차 부품 / 경량화

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

## 핵심 구조

```text
완성차 판매 / OE·RE 수요
→ ASP와 원재료 spread
→ OPM 개선
→ 고객사 다변화
```

Kumho Tire는 광주공장 화재로 생산이 중단됐고, 해당 공장이 글로벌 생산능력의 약 20%를 차지하는 것으로 보도됐다. 이런 사례는 타이어/부품 archetype에서 **생산중단 4C 반례**로 중요하다. ([Reuters][8])

## 성공 후보

| 케이스          | 판단                         |
| ------------ | -------------------------- |
| 한국타이어        | RE/OE mix, ASP, 원재료 spread |
| 현대모비스 / HL만도 | ADAS/전장, 고객 다변화            |
| 경량화 부품       | 실제 채택률, 마진                 |
| 카메라/자율주행 부품  | 고객사와 매출화                   |

## 반례

| 반례          | 왜 위험한가                      |
| ----------- | --------------------------- |
| 생산중단/화재     | supply disruption 4C        |
| 원재료 상승      | margin compression          |
| EV 수요 둔화 부품 | 고객사 수요 둔화                   |
| 단일 고객 부품주   | customer concentration risk |

## Stage 기준

```text
Stage 1:
완성차 판매 호조
ASP 상승
고객사 수주

Stage 2:
OPM 개선
원재료 안정
고객 다변화
FY1/FY2 OP 상향

Stage 3:
고마진 mix 전환
전장/ADAS/EV exposure
반복 납품 visibility
valuation discount 해소

4B:
peak margin
완성차 cycle peak
valuation 정상화

4C:
원재료 급등
생산중단
고객사 판매 둔화
리콜/품질비용
```

## 점수비중 v0.4

```text
EPS/FCF: 20
Structural Visibility: 18
Bottleneck/Pricing: 10
Market Mispricing: 14
Valuation Rerating: 14
Capital Allocation: 3
Information Confidence: 5
Risk Penalty: raw materials / customer concentration
```

**정규화 포인트:**
자동차 부품은 고객사와 원가에 크게 묶인다. 고객 다변화와 원재료 안정 없이는 Green 제한.

---

# 8. CDMO_HEALTHCARE_CONTRACT

CMO / 원료의약품 / 바이오시밀러

## 포함 테마

```text
CMO-원료의약품
바이오시밀러
CRO 일부
원료의약품
```

## 핵심 구조

```text
장기 생산계약 / capacity / 고객사 다변화
→ 가동률 상승
→ OP/FCF 개선
```

Samsung Biologics는 GSK로부터 미국 Rockville 생산시설을 2억 8천만 달러에 인수해 첫 미국 생산거점을 확보하고, 60,000L drug substance capacity를 더했다. 이건 CDMO archetype에서 실제 capacity·글로벌 고객·장기 수요를 보는 좋은 후보 사례다. ([Reuters][9])

## 성공 후보

| 케이스          | 판단                       |
| ------------ | ------------------------ |
| 삼성바이오로직스     | capacity, 고객사, 가동률, 장기계약 |
| 셀트리온         | 바이오시밀러 매출화, 가격경쟁         |
| CMO 원료의약품 업체 | 계약/가동률/마진                |

## 반례

| 반례                 | 왜 위험한가         |
| ------------------ | -------------- |
| capacity overbuild | 가동률 하락         |
| patent/litigation  | 제품 출시 지연       |
| 가격경쟁               | 마진 훼손          |
| 고객 집중              | 계약 지연 시 EPS 훼손 |

## Stage 기준

```text
Stage 1:
대형 생산계약
capacity 확장
미국/글로벌 생산거점 확보

Stage 2:
가동률 상승
매출/OP 상향
장기계약
고객사 다변화

Stage 3:
다년 생산 visibility
높은 FCF conversion
계약/가동률/마진 동시 개선
시장이 아직 고정비/바이오 할인 프레임

4B:
capacity 기대 과열
valuation 포화
신규 설비 기대 모두 반영

4C:
가동률 하락
계약 지연
patent/litigation
가격경쟁
```

## 점수비중 v0.4

```text
EPS/FCF: 20
Structural Visibility: 24
Bottleneck/Pricing: 12
Market Mispricing: 12
Valuation Rerating: 12
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: litigation / capacity utilization
```

**정규화 포인트:**
CDMO는 바이오 임상주가 아니라 **계약·capacity·가동률**로 보는 게 맞다.

---

# 9. PLATFORM_SOFTWARE / SECURITY_IDENTITY_DEEPFAKE

클라우드 / 보안 / 딥페이크 / 생체인식

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

## 핵심 구조

```text
반복 소프트웨어 매출
→ ARPU / take-rate / 보안수요 증가
→ OPM 레버리지
```

Kakao는 플랫폼 자산이 있지만 SM엔터 인수 관련 stock manipulation 의혹으로 founder의 법적 리스크가 부각되었다. 이런 사례는 플랫폼 archetype에서 **governance/legal risk가 valuation rerating을 막는 반례**로 쓰기 좋다. ([Reuters][10])

## 성공 후보

| 케이스        | 판단                 |
| ---------- | ------------------ |
| 더존비즈온      | SaaS/ERP 반복매출, OPM |
| 보안/생체인식 업체 | 반복 보안 수요, 공공/기업 계약 |
| 클라우드/컨택센터  | 구독형 매출, 비용 구조      |
| 딥페이크 보안    | 규제와 실제 도입계약        |

## 반례

| 반례                    | 왜 위험한가    |
| --------------------- | --------- |
| Kakao governance risk | 법적/규제 리스크 |
| MAU만 높은 플랫폼           | 수익화 없음    |
| AI 비용 과다              | FCF 악화    |
| 보안 테마만 있는 기업          | 실제 계약 없음  |

## 점수비중 v0.4

```text
EPS/FCF: 20
Structural Visibility: 22
Bottleneck/Pricing: 8
Market Mispricing: 16
Valuation Rerating: 14
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: regulation / governance / AI cost
```

**정규화 포인트:**
플랫폼·보안은 **반복매출 + OPM 개선 + 낮은 규제/법적 리스크**가 있어야 Stage 3 후보. MAU나 AI 키워드만으로 Green 금지.

---

# 10. ROBOTICS_FACTORY_AUTOMATION

피지컬AI / 휴머노이드 / 제조용·서비스용 로봇

## 포함 테마

```text
피지컬AI
휴머노이드
제조용 로봇
서비스용 로봇
수술용 로봇
로봇 부품
스마트팩토리
드론·플라잉카 일부
```

## 핵심 구조

```text
대기업 투자 / 정책
→ 실제 고객사 도입
→ 수주/매출화
→ 반복 서비스·소모품 매출
```

Samsung은 Rainbow Robotics에 2670억원을 투자해 최대주주가 되었고 CEO 직속 Future Robotics Office를 만들었다. 이건 강한 Stage 1~2 신호지만, 실제 매출·OP 전환 전에는 Green을 주면 안 된다. ([Reuters][11])

## 성공 후보

| 케이스              | 판단                                  |
| ---------------- | ----------------------------------- |
| Rainbow Robotics | 삼성 전략 편입, 매출화 전 Green 제한            |
| 현대차 로봇공장         | 피지컬AI 인프라 후보                        |
| 두산로보틱스           | 협동로봇, 글로벌 확장, valuation 확인          |
| 수술용 로봇           | 반복 소모품/시술 수익 있으면 의료기기 archetype과 교차 |

## 반례

| 반례             | 왜 위험한가                |
| -------------- | --------------------- |
| 무실적 로봇 테마주     | TAM만 있고 매출 없음         |
| MOU/PoC만 있는 기업 | 수주/매출 전환 전 Stage 3 금지 |
| 고밸류 IPO 로봇주    | EPS/FCF가 주가를 못 따라감    |
| 서비스로봇 유행성 테마   | 반복 매출 불명확             |

## 점수비중 v0.4

```text
EPS/FCF: 18
Structural Visibility: 15
Bottleneck/Pricing: 10
Market Mispricing: 12
Valuation Rerating: 10
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: theme / monetization failure
```

**정규화 포인트:**
로봇은 대부분 Stage 1~2 또는 Watch. 실제 매출화 전 Green 금지.

---

# 11. CONSTRUCTION_REAL_ESTATE_CREDIT / BUILDING_MATERIALS

건설 / PF / 건자재 / 시멘트 / 철근

## 포함 테마

```text
대형 건설사
중소형 건설사
부동산 자산 보유
개발신탁리츠
건자재
시멘트·레미콘·콘크리트
철근
거푸집
가구
```

## 핵심 구조

```text
수주보다 PF / 미분양 / 원가율 / 현금흐름이 먼저
```

한국 부동산 PF 연체율은 2021년 말 0.37%에서 2023년 말 2.70%로 상승했고, 금융당국은 부실 프로젝트 구조조정을 강화했다. 건설 archetype에서는 이걸 hard RedTeam 조건으로 넣어야 한다. ([Reuters][12])
또 한국 정부는 고금리로 어려움을 겪는 건설사와 중소기업에 40.6조원 규모 금융지원책을 준비했다. 이런 지원은 Stage 1 relief일 수 있지만, 구조적 E2R 성공은 아니다. ([Reuters][13])

## 성공 후보

| 케이스            | 판단                   |
| -------------- | -------------------- |
| PF 리스크 해소형 건설사 | 부실 정리 후 cash flow 회복 |
| 해외 플랜트/인프라 수주형 | 마진 확정형 수주            |
| 시멘트/철근 가격 인상   | 수요와 원가 안정 동반 필요      |
| 리츠/개발신탁        | 금리·자산가치·배당 안정성 확인    |

## 반례

| 반례           | 왜 위험한가                |
| ------------ | --------------------- |
| PF 부실 건설사    | 수주잔고보다 credit risk 우선 |
| 유동성 지원 의존 기업 | 구조적 개선이 아님            |
| 원가 상승 미반영    | 매출 증가에도 OP/FCF 훼손     |
| 미분양 증가       | 현금흐름 악화               |

## 점수비중 v0.4

```text
EPS/FCF: 18
Structural Visibility: 10
Bottleneck/Pricing: 8
Market Mispricing: 12
Valuation Rerating: 10
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: PF / 미분양 / 신용위험 very high
```

**정규화 포인트:**
건설은 주가 rebound가 와도 PF와 현금흐름이 해결되지 않으면 **credit relief rally**일 뿐이다.

---

# 12. EVENT_DISEASE_PEST / SPECULATIVE_SCIENCE

엠폭스 / 빈대 / 황사 / 초전도체 / 맥신 / 그래핀

## 포함 테마

```text
엠폭스
코로나19
전염병 진단
동물백신·방역
빈대퇴치
황사·미세먼지 마스크
초전도체
맥신
그래핀
양자 기술
```

## 핵심 구조

```text
이벤트성 수요 또는 과학 테마
→ 주가 급등 가능
→ EPS/FCF 지속성은 낮음
```

## 성공 후보

매우 제한적이다.

```text
반복 소모품 진단 플랫폼
실제 정부계약/매출 반복 방역
상용화된 과학기술 제품
```

## 반례

| 반례            | 왜 위험한가                |
| ------------- | --------------------- |
| 씨젠 2020       | 팬데믹 one-off demand    |
| 엠폭스·빈대·마스크 테마 | 단기 이벤트 수요             |
| 초전도체/맥신/그래핀   | 논문·테마만 있고 매출 없음       |
| 양자 기술 관련주     | 실제 계약·매출 전까지 Green 금지 |

## Stage 기준

```text
Stage 1:
전염병/논문/재난 뉴스
거래대금 급증

Stage 2:
실제 매출/계약 확인 시만

Stage 3:
Green 거의 금지
반복 수요·상용화·매출 전환이 있을 때만 Watch

4B:
price-only rally
관련주 동반 급등

4C:
검증 실패
수요 정상화
관련성 부인
재고 증가
```

## 점수비중 v0.4

```text
EPS/FCF: 5~20
Structural Visibility: 5
Bottleneck/Pricing: 5
Market Mispricing: 5
Valuation Rerating: 5
Risk Penalty: extreme
```

**정규화 포인트:**
이벤트·과학 테마는 주가가 급등해도 **정통 E2R 성공사례가 아니다**. 대부분 Red/4B 방어용.

---

# 13. AGRI_LIVESTOCK_FOOD_COMMODITY

양돈 / 육계 / 사료 / 대두 / 농기계 / 참치

## 포함 테마

```text
양돈주
육계주
배합사료
대두
농업 종자비료농약
참치 원양어업
스마트팜
농기계
```

## 핵심 구조

```text
곡물/사료/육류/어가 가격
→ 원가 또는 판가
→ 단기 OP 변화
→ 대부분 사이클
```

## 성공 후보

| 케이스      | 판단                   |
| -------- | -------------------- |
| 스마트팜/농기계 | 실제 수주, 해외 확장, 반복 서비스 |
| 원양어업     | 참치 가격, 어획량, 유가, 환율   |
| 종자/농약/비료 | 가격전가, 정책, 반복수요       |

## 반례

| 반례          | 왜 위험한가                   |
| ----------- | ------------------------ |
| 조류독감/질병 이벤트 | 단기 가격 급등                 |
| 사료 원가 상승    | 양돈/육계 margin compression |
| 대두 가격 급등    | 음식료/사료 원가 부담             |
| 날씨 이벤트      | 단기 테마                    |

## 점수비중 v0.4

```text
EPS/FCF: 18
Structural Visibility: 8~12
Bottleneck/Pricing: 14
Market Mispricing: 8
Valuation Rerating: 8
Risk Penalty: commodity / disease event
```

**정규화 포인트:**
농축산은 대부분 cycle/event. 판가 전가와 반복수요가 없으면 Green 제한.

---

# 14. 이번 라운드 요약: 테마별 Green 정책 v0.4

## Green 가능성이 있는 테마군

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

단, 실제 증거 필요:

```text
계약
수주잔고
수출/채널
OPM/ROE
CSM/자본비율
EPS/FCF revision
price-path alignment
```

## Watch / Yellow 중심 테마군

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

조건:

```text
매출화, 규제승인, 실제 수주, 반복매출 전까지 Green 제한
```

## Red / 4B 방어 중심 테마군

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

조건:

```text
주가 급등해도 구조적 E2R로 보지 않는다.
대부분 Stage 1, Stage 3-Red, 4B-watch, 4C 감시 대상.
```

---

# 15. 점수정규화가 잘 되고 있는지에 대한 답

**지금 방식은 맞다.**
다만 “정규화 완료”가 아니라 “정규화 근거를 쌓는 중”이야.

현재 우리가 하는 정규화는 이렇게 구성된다.

```text
성공사례:
어떤 evidence가 EPS/FCF와 주가 리레이팅을 만들었는지 알려줌

반례:
어떤 evidence가 겉보기엔 좋아도 Green을 막아야 하는지 알려줌

주가 경로:
점수비중이 실제 시장에서 맞았는지 검증함
```

그래서 다음 단계에서 반드시 해야 할 건:

```text
1. theme_tag_map.csv 구성
2. cases_v03.jsonl 구성
3. 각 case price-path backfill
4. score_price_alignment 계산
5. shadow scoring
6. 틀린 archetype 재보정
```

---

# 16. 다음 라운드에서 더 채울 것

다음에는 아래를 더 해야 해.

```text
1. theme_tag_map.csv 초안 생성
   - 네가 준 모든 테마를 primary_archetype에 매핑
   - green_policy 부여

2. cases_v03 후보 확장
   - 이번 라운드의 신규 archetype별 성공/반례 추가

3. price validation 설계
   - stage2_price, stage3_price, peak_price, MFE/MAE, drawdown

4. 점수비중 shadow test 설계
   - production scoring은 아직 건드리지 않고 병렬점수로 비교

5. under-covered archetype 체크
   - 성공 2개 + 반례 2개 미만인 곳 표시
```

이번 라운드에서 새로 깊게 채운 건:

```text
편의점/유통
손해보험/생명보험
스테이블코인/STO/결제
K뷰티 OEM/ODM
2차전지 ESS/폐배터리
수소/태양광/풍력
타이어/자동차 부품
CDMO
플랫폼/보안/딥페이크
로봇
건설/PF/건자재
전염병/초전도체/이벤트
농축산/사료/대두
```

이제 상당수 세부 테마가 12개 대섹터와 60~70개 archetype 안에 들어갈 수 있게 됐다.

[1]: https://en.wikipedia.org/wiki/Samsung_Fire_%26_Marine_Insurance?utm_source=chatgpt.com "Samsung Fire & Marine Insurance"
[2]: https://www.reuters.com/business/finance/south-korean-fintech-toss-plans-global-push-starting-australia-aims-issue-won-2025-09-09/?utm_source=chatgpt.com "South Korean fintech Toss plans global push starting in Australia, aims to issue won stablecoin"
[3]: https://arxiv.org/abs/2601.00196?utm_source=chatgpt.com "SoK: Stablecoins in Retail Payments"
[4]: https://www.ft.com/content/106a1e79-0a64-4c51-b74f-ad4d4f8896f6?utm_source=chatgpt.com "Stablecoins craze pits central bank against lawmakers in South Korea"
[5]: https://www.reuters.com/world/asia-pacific/korean-beauty-startups-bet-booming-us-demand-outlasts-tariff-pain-2025-06-05/?utm_source=chatgpt.com "Korean beauty startups bet booming US demand outlasts tariff pain"
[6]: https://www.reuters.com/legal/litigation/gms-restart-date-ohio-battery-plant-uncertain-2026-05-12/?utm_source=chatgpt.com "GM-LG's restart date at Ohio battery plant uncertain"
[7]: https://arxiv.org/abs/2512.08076?utm_source=chatgpt.com "Mitigation of Datacenter Demand Ramping and Fluctuation using Hybrid ESS and Supercapacitor"
[8]: https://www.reuters.com/en/south-koreas-kumho-tire-plant-production-suspended-due-fire-2025-05-17/?utm_source=chatgpt.com "South Korea's Kumho Tire plant production suspended due to fire"
[9]: https://www.reuters.com/business/healthcare-pharmaceuticals/samsung-biologics-buy-us-drug-production-facility-gsk-280-mln-2025-12-21/?utm_source=chatgpt.com "Samsung Biologics to buy US drug production facility from GSK for $280 million"
[10]: https://www.reuters.com/business/south-korea-court-decide-arrest-warrant-kakao-founder-2024-07-22/?utm_source=chatgpt.com "South Korea court to decide on arrest warrant for Kakao founder"
[11]: https://www.reuters.com/technology/samsung-electronics-becomes-largest-shareholder-south-koreas-rainbow-robotics-2024-12-30/?utm_source=chatgpt.com "Samsung Electronics becomes largest shareholder of South Korea's Rainbow Robotics"
[12]: https://www.reuters.com/markets/asia/south-korea-tightens-scrutiny-speed-up-real-estate-restructuring-2024-05-13/?utm_source=chatgpt.com "South Korea tightens scrutiny to speed up real estate restructuring"
[13]: https://www.reuters.com/markets/asia/south-korea-prepares-financial-support-small-businesses-builders-2024-03-27/?utm_source=chatgpt.com "South Korea prepares financial support for small businesses, builders"
