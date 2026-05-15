좋아. 이제 정해둔 순서대로 **R1 — 산업재·수주·인프라**부터 진행한다.

이번 라운드는 “계약·수주·백로그가 EPS/FCF 체급 변화로 이어지는가”를 보는 라운드야. 업로드된 Theme Tag Map에서도 R1은 전력설비, 전선·케이블, 피팅밸브, 조선, 조선 기자재, 방산, 원전, 철도, 건설기계, 우크라 재건, 네옴시티 같은 테마를 흡수하는 대섹터로 정리되어 있고, 핵심은 단순 수주 뉴스가 아니라 **계약질 + 마진 + EPS 상향 + 주가 리레이팅**이 같이 가는지다.

서생원식 기준으로도 R1은 가장 중요한 축 중 하나다. 단순히 “PER이 싸다”가 아니라, 산업 구조가 바뀌면서 EPS/FCF 체급이 올라가고 시장이 아직 과거 프레임으로 낮게 평가하는 구간을 찾는 게 핵심이다.

---

# R1. 산업재·수주·인프라

## 1. 이번 라운드 대섹터

```text
R1 = 산업재·수주·인프라
```

이 라운드는 가장 “서생원식”에 가까운 대섹터다.

```text
수요 구조 변화
→ 공급 부족 / 생산능력 병목
→ 장기계약 / 수주잔고 / 납품 스케줄
→ EPS/FCF 상향
→ 시장의 과거 산업재 프레임 해소
→ 밸류에이션 리레이팅
```

하지만 수주 뉴스만으로는 부족하다. OpenDART detail fetch 원칙에서도 계약금액, 계약기간, 매출 대비 계약금액, 계약 시작·종료일, 거래상대방 같은 실제 필드를 추출하되, 없는 값은 절대 만들어내지 않도록 설계되어 있었다. 이 원칙을 R1 검증에도 그대로 적용해야 한다.

---

## 2. 대상 canonical archetype

이번 R1에서 확정할 canonical archetype은 아래로 둔다.

| 구분              | canonical archetype                | Green 정책           |
| --------------- | ---------------------------------- | ------------------ |
| 전력망·변압기         | `GRID_TRANSFORMER_SHORTAGE`        | Green 가능           |
| 일반 수주형 산업재      | `CONTRACT_BACKLOG_INDUSTRIAL`      | Green 가능           |
| 방산 정부 백로그       | `DEFENSE_GOVERNMENT_BACKLOG`       | Green 가능           |
| 방산테크·자율체계       | `DEFENSE_TECH_AUTONOMOUS_SYSTEMS`  | Watch-to-Green     |
| 드론·counter-UAS  | `DEFENSE_DRONE_COUNTER_UAS`        | Watch-to-Green     |
| 군사용 AI software | `DEFENSE_AI_SOFTWARE_INTELLIGENCE` | Watch-to-Green     |
| 조선·해양           | `SHIPBUILDING_OFFSHORE_BACKLOG`    | Green 가능, 마진 확인 필요 |
| 철도 인프라          | `RAIL_INFRASTRUCTURE`              | Watch-to-Green     |
| 원전·SMR·전력 PPA   | `NUCLEAR_SMR_GRID_POLICY`          | Watch-to-Green     |
| 재건·대형 인프라 정책    | `GEOPOLITICAL_RECONSTRUCTION`      | Event/Watch        |
| 스마트팩토리·자동화      | `SMART_FACTORY_AUTOMATION`         | Watch              |
| 데이터센터 내부 전력장비   | `AI_DATA_CENTER_POWER_EQUIPMENT`   | Green 가능, 수주 확인 필요 |

---

## 3. deep sub-archetype

R1 내부의 하위 렌즈는 이렇게 쪼갠다.

```text
GRID_TRANSFORMER_SHORTAGE
- 변압기
- 배전반
- 전력설비
- 전선·케이블
- AI 데이터센터 전력망
- 리드타임 장기화
- 전력장비 가격 상승

CONTRACT_BACKLOG_INDUSTRIAL
- 산업용 장비
- 피팅밸브
- 강관
- 건설기계
- 장기공급계약형 산업재

DEFENSE_GOVERNMENT_BACKLOG
- K9
- 천무
- K2
- 탄약
- 항공우주
- KF-21
- 정부 장기계약

DEFENSE_TECH_AUTONOMOUS_SYSTEMS
- 저가 대량 미사일
- autonomous system
- 방산 AI
- containerized munitions

DEFENSE_DRONE_COUNTER_UAS
- 드론
- loitering munition
- counter-UAS
- directed energy

DEFENSE_AI_SOFTWARE_INTELLIGENCE
- Maven류 군사용 AI
- 지휘통제 소프트웨어
- 정보융합 플랫폼

SHIPBUILDING_OFFSHORE_BACKLOG
- 조선
- LNG선
- 조선 기자재
- 엔진
- 피팅밸브
- 선가 상승
- 저가수주 소진

RAIL_INFRASTRUCTURE
- 철도차량
- 고속철
- 해외 철도 수출
- 도시철도
- 납품 스케줄

NUCLEAR_SMR_GRID_POLICY
- 원전 수출
- SMR
- 기존 원전 PPA
- 기자재
- 법적·허가 리스크

AI_DATA_CENTER_POWER_EQUIPMENT
- UPS
- PDU
- switchgear
- modular power
- 데이터센터 내부 전력장비
```

---

# 4. 성공사례

## 4-1. 전력설비·변압기: 구조적 Green 후보

미국에서는 데이터센터, EV, 공장, 재생에너지 프로젝트 수요로 변압기 수요가 크게 늘었고, 대형 변압기 리드타임이 최대 4년, 가격은 5년 동안 약 80% 상승했다. Reuters는 미국 전력 개발사들이 지연을 피하려고 한국·튀르키예 등 해외 공급처로도 눈을 돌리고 있다고 보도했다. 이건 `GRID_TRANSFORMER_SHORTAGE`의 구조적 성공 근거다. ([Reuters][1])

**점수 판단**

```text
EPS/FCF: 강함
Structural Visibility: 매우 강함
Bottleneck/Pricing: 매우 강함
Market Mispricing: 중간~강함
Valuation Rerating: 중간~강함
```

**가격경로 1차 판정**

```text
보도 자체는 산업 병목과 가격 상승을 명확히 보여준다.
다만 HD현대일렉트릭, 효성중공업, LS ELECTRIC 등 개별 종목의 정확한 stage price / MFE / MAE는 에이전트 가격 데이터로 backfill해야 한다.
현재 판정: structural_success_candidate / price_alignment = needs_price_backfill
```

---

## 4-2. 방산: 한화에어로스페이스 K9 루마니아 계약

한화에어로스페이스는 루마니아에 K9 자주포 54문, K10 탄약운반장갑차 36대, 탄약·지원 패키지를 공급하는 약 10억 달러 계약을 따냈고, 계약기간은 2029년까지다. Reuters는 한화 방산 수주잔고가 2021년 말 5.1조원에서 2024년 3월 약 30조원으로 증가했고, 해당 계약 보도 당일 한화에어로스페이스 주가가 5% 이상 올라 장중 사상 최고가를 기록했다고 보도했다. ([Reuters][2])

**점수 판단**

```text
EPS/FCF: 강함
Structural Visibility: 매우 강함
Bottleneck/Pricing: 강함
Market Mispricing: 중간~강함
Valuation Rerating: 강함
Capital Allocation: 주의 필요
```

**가격경로 1차 판정**

```text
계약 보도 당일 +5% 이상, record high 반응 확인.
Stage 2 이벤트와 가격 반응이 즉시 연결됨.
다만 이후 6~24개월 MFE/MAE와 EPS revision 지속 여부는 추가 검증 필요.
현재 판정: aligned_candidate
```

---

## 4-3. 방산 유럽 매출 visibility

한화에어로스페이스는 유럽 육상무기 매출이 2027년까지 두 배가 될 것으로 기대한다고 밝혔고, Reuters는 폴란드 92억 달러, 루마니아 10억 달러 계약과 현지 생산 선호가 수요 배경이라고 보도했다. 이건 방산 수주가 단발 계약이 아니라 지역별 장기 생산·납품 구조로 갈 수 있음을 보여준다. ([Reuters][3])

**점수 판단**

```text
Structural Visibility: 강화
Backlog-to-sales: 강화
납품 스케줄: 확인 필요
OPM: 추후 확인 필요
```

**가격경로 1차 판정**

```text
계약·백로그는 강하지만, 실제 주가 검증은 계약별 stage date와 분기별 실적 인식이 필요하다.
현재 판정: success_candidate / needs_price_backfill
```

---

## 4-4. 철도: 현대로템 모로코 수주

현대로템은 모로코 국영철도 ONCF로부터 약 2.2조원, 15.4억 달러 규모의 2층 전동차 수주를 확보했다. Reuters는 이 계약이 현대로템 철도사업 사상 최대 수주라고 보도했고, 별도 Reuters 보도에서는 모로코가 2030 월드컵을 앞두고 168대 열차를 구매하며 도시·고속철 네트워크를 확장하려 한다고 설명했다. ([Reuters][4])

**점수 판단**

```text
EPS/FCF: 중간~강함
Structural Visibility: 강함
Bottleneck/Pricing: 중간
Market Mispricing: 중간
Valuation Rerating: 중간
Risk: 프로젝트 마진, 납기, financing
```

**가격경로 1차 판정**

```text
수주 규모는 강하지만, 현재 검색 결과만으로 즉시 주가 반응은 확인하지 못했다.
Stage 2 date는 2025-02-26으로 잡고, 주가 MFE/MAE backfill 필요.
현재 판정: success_candidate / price_alignment = unknown_until_backfill
```

---

## 4-5. 조선: 한국 조선주 수주·선가 리레이팅

WSJ는 한국 조선주들이 계약 수주 재개와 신조선가 상승으로 급등했고, 삼성중공업은 16%, 한화오션은 13%, HD현대중공업은 11% 상승했다고 보도했다. Clarksons 신조선가 지수 상승과 대형 수주가 profitability 개선 기대를 만들었다는 설명도 붙어 있었다. ([월스트리트저널][5])

**점수 판단**

```text
EPS/FCF: 강함
Structural Visibility: 중간~강함
Bottleneck/Pricing: 강함
Market Mispricing: 중간
Valuation Rerating: 중간~강함
Risk: 저가수주, 후판가, 인건비, 발주 cycle
```

**가격경로 1차 판정**

```text
수주·선가 뉴스와 주가 급등이 동시에 확인됨.
하지만 조선은 수주잔고의 양보다 수주잔고의 질, 선가, 저가수주 소진, 인도 시점 마진이 핵심이다.
현재 판정: cyclical_to_structural_success_candidate
```

---

## 4-6. 원전 PPA: Meta–Constellation

Meta는 Constellation의 Clinton 원전과 20년 전력계약을 맺어 원전의 계속 운전과 재허가를 지원하기로 했다. Reuters는 이 계약이 AI·데이터센터 전력 수요 증가 속에서 Big Tech가 장기 무탄소 전력을 확보하려는 흐름을 보여준다고 보도했다. ([Reuters][6])

**점수 판단**

```text
EPS/FCF: 중간
Structural Visibility: 강함
Bottleneck/Pricing: 중간
Market Mispricing: 중간
Valuation Rerating: 중간
Risk: 규제, PPA 가격, 원전 운영비
```

**가격경로 1차 판정**

```text
기존 원전 PPA는 SMR보다 훨씬 증거 강도가 높다.
하지만 한국 원전 기자재주로 연결하려면 직접 계약·납품·매출화 evidence가 필요하다.
현재 판정: archetype_success_reference / Korean_equity_mapping_needed
```

---

## 4-7. 방산테크: Pentagon LCCM / Anduril

미 국방부는 Anduril, CoAspire, Leidos, Zone 5와 Low-Cost Containerized Munitions 프로그램 관련 framework agreement를 맺고, 2027년부터 3년간 1만 발 이상 저가 컨테이너형 미사일 조달을 목표로 하고 있다. 이건 방산테크·자율무기 archetype에서 “prototype 테마”가 아니라 **framework agreement → 평가 → 대량 조달**로 이어질 수 있는 성공 후보 구조다. ([Reuters][7])

**점수 판단**

```text
EPS/FCF: 중간~강함
Structural Visibility: 강함, 단 실제 발주 전까지 Watch
Bottleneck/Pricing: 중간
Market Mispricing: 강함 가능
Valuation Rerating: 강함 가능
Risk: 조달 지연, valuation 과열, 프로그램 취소
```

**가격경로 1차 판정**

```text
비상장/해외 reference 성격이 강하다.
한국 상장사에 매핑하려면 실제 납품계약·부품 공급·방산 SW exposure 필요.
현재 판정: success_reference / not_direct_KR_candidate_yet
```

---

## 4-8. 방산 AI software: Palantir Maven

Palantir는 미 육군으로부터 Maven Smart System prototype 개발을 위해 4.8억 달러 계약을 받았다. Reuters는 Maven이 여러 데이터 소스에서 관심 지점을 식별하는 군사 정보 분석 prototype이며 2029년까지 완료 예정이라고 보도했다. ([Reuters][8])

**점수 판단**

```text
EPS/FCF: 중간
Structural Visibility: 중간~강함
Bottleneck/Pricing: 중간
Market Mispricing: 강함 가능
Valuation Rerating: 강함 가능
Risk: prototype 단계, 윤리·정치 리스크, 정부 예산 cycle
```

**가격경로 1차 판정**

```text
prototype 계약은 Stage 2 초입이다.
장기 program of record와 반복 software revenue로 전환되는지 확인해야 한다.
현재 판정: watch_to_green_candidate
```

---

# 5. 반례

## 5-1. 방산 capital allocation 반례: 한화에어로스페이스 유상증자

한화에어로스페이스는 해외 생산능력 확대와 방산 투자 재원을 위해 대규모 자본조달을 추진했지만, 한국 금융당국이 공시 보완을 요구했고, 발표 후 주가는 2016년 이후 최악의 하루 낙폭인 13% 하락했다. Reuters는 투자자들이 자금조달 목적과 필요성에 의문을 제기했다고 보도했다. ([Reuters][9])

**교훈**

```text
방산 수주잔고가 아무리 좋아도 dilution/capital allocation risk를 감점해야 한다.
```

**가격경로 1차 판정**

```text
event_day_return: -13% 보도 확인.
Stage 4C까지는 아니지만 4B/RedTeam risk로 분류해야 한다.
현재 판정: capital_allocation_counterexample
```

---

## 5-2. 원전·SMR 반례: NuScale CFPP 취소

NuScale의 Carbon Free Power Project는 비용 증가와 충분한 구독 확보 실패로 2023년 취소되었다. 공개 자료에 따르면 예상 전력가격과 건설비가 크게 상승했고, 취소 이후 NuScale은 인력 감축도 진행했다. ([위키백과][10])

**교훈**

```text
SMR은 정책·AI 전력 narrative만으로 Green 금지.
PPA, financing, 전력단가, 허가, 고객 확보가 필요하다.
```

**가격경로 1차 판정**

```text
프로젝트 취소는 4C thesis break.
SMR 관련주는 stage2 이전에는 Watch/Red에 가깝다.
```

---

## 5-3. 원전 수출 법적 리스크: KHNP–체코

체코 법원은 EDF의 항소를 이유로 KHNP와 CEZ의 원전 계약 서명을 일시적으로 막았다. AP는 체코 법원이 EDF 사건을 심리할 때까지 계약 서명을 막았으며, 원전 프로젝트는 각 원자로 약 91억 달러 규모로 예상된다고 보도했다. ([AP News][11])

**교훈**

```text
원전은 수주 기대가 있어도 법적·정책·financing 리스크가 hard gate다.
```

**가격경로 1차 판정**

```text
원전 기자재주·정책 수혜주는 계약 전 기대만으로 Stage 3 금지.
현재 판정: legal_delay_4c_watch
```

---

## 5-4. 조선 반례: 저마진 수주잔고

조선주는 선가 상승과 수주 재개가 붙으면 강하지만, 수주잔고가 많아도 저가수주가 남아 있거나 후판가·인건비가 상승하면 EPS가 늦게 따라온다. WSJ의 조선주 랠리 보도도 결국 신조선가 상승과 profitability 개선 기대가 핵심이었지, 수주잔고의 양 자체가 핵심은 아니었다. ([월스트리트저널][5])

**교훈**

```text
조선은 backlog quantity보다 backlog quality.
```

**가격경로 1차 판정**

```text
수주 뉴스 후 주가는 급등 가능.
하지만 저가수주 소진과 마진 확인 전에는 Stage 3-Green 보수적으로.
```

---

## 5-5. 재건·정책형 인프라 반례

우크라 재건, 네옴시티, 대형 철도 정책, 해외 인프라 MOU는 Stage 1 이벤트로는 의미가 있지만, 실제 계약·매출·납품 스케줄 없이는 Green을 주면 안 된다. Theme Tag Map에서도 우크라 재건과 네옴시티는 Event/Watch로 분류되어 있고, 실제 수주 전 Green 금지로 정리되어 있다.

---

# 6. 4B-watch 사례

## 6-1. 방산주 crowded rerating

한화에어로스페이스는 유럽 수주와 방산 수요로 강한 구조적 후보지만, FT는 해외 확장 자금조달 발표 후 주가가 13% 하락했다고 보도했다. 이는 “좋은 구조”가 있어도 주가가 이미 많이 올라 있고 추가 자본조달이 나오면 4B-watch가 켜져야 함을 보여준다. ([Financial Times][12])

```text
4B 조건:
- 모두가 K방산 수주를 인정
- valuation band 상승
- 추가 자본조달 또는 해외공장 투자 발표
- EPS보다 CAPEX/dilution 우려가 커짐
```

---

## 6-2. 조선주 계약 랠리 이후 4B-watch

삼성중공업 +16%, 한화오션 +13%, HD현대중공업 +11% 같은 하루 급등은 Stage 2 가격 반응으로는 긍정적이지만, 이후 모두가 신조선가·LNG선·조선 호황을 인정하는 구간에서는 4B-watch가 필요하다. ([월스트리트저널][5])

```text
4B 조건:
- 조선주 동반 급등
- 선가 상승 narrative 과밀
- 목표가 상향 집중
- 저가수주 소진이 이미 가격에 반영
```

---

## 6-3. 전력설비 4B-watch

변압기 리드타임 4년, 가격 80% 상승 같은 병목은 Green 근거이지만, 향후 미국·멕시코·국내 증설이 진행되고 신규 생산 slot이 풀리면 4B-watch가 필요하다. ([Reuters][1])

```text
4B 조건:
- 전력설비주 모두가 AI 전력망 수혜로 인정
- CAPA 증설 뉴스 증가
- 신규 경쟁자 진입
- 수주잔고는 높지만 신규수주 증가율 둔화
```

---

# 7. 4C-thesis-break 사례

## 7-1. SMR 프로젝트 취소

NuScale CFPP 취소는 `NUCLEAR_SMR_GRID_POLICY`의 대표 4C다. 비용 증가, 전력단가 부담, 고객 확보 실패가 한꺼번에 나온 경우 Stage 3는 즉시 금지해야 한다. ([위키백과][10])

```text
4C:
project_cancelled
cost_overrun
financing_failed
customer_subscription_failed
```

---

## 7-2. 원전 계약 법적 지연

체코 원전 프로젝트처럼 경쟁사 항소와 법원 가처분으로 계약 서명이 지연되면, 원전 기자재·정책 수혜는 Stage 2에서 멈춰야 한다. ([AP News][11])

```text
4C-watch:
legal_delay
contract_signing_blocked
state_aid_or_tender_dispute
```

---

## 7-3. 방산 자본조달 shock

한화에어로스페이스의 자본조달 논란은 계약논리 자체의 4C는 아니지만, capital allocation 4C-watch다. 주가가 13% 하락했다는 점은 가격경로상 무시하면 안 된다. ([Reuters][9])

```text
4C-watch:
dilution
unclear_use_of_proceeds
regulator_revision_request
```

---

# 8. 점수비중 보정표 — R1 v1.0

| canonical archetype                | EPS/FCF | Visibility | Bottleneck | Mispricing | Valuation | Capital | Info | 핵심 감점                     |
| ---------------------------------- | ------: | ---------: | ---------: | ---------: | --------: | ------: | ---: | ------------------------- |
| `GRID_TRANSFORMER_SHORTAGE`        |      22 |         25 |         23 |         12 |        12 |       1 |    5 | CAPA 정상화, 저마진 계약, 프로젝트 지연 |
| `CONTRACT_BACKLOG_INDUSTRIAL`      |      20 |         24 |         18 |         13 |        12 |       1 |    5 | 계약질 불명확, 납기, 마진           |
| `DEFENSE_GOVERNMENT_BACKLOG`       |      20 |         24 |         17 |         14 |        14 |       3 |    5 | 납기, 원가, 수출허가, dilution    |
| `DEFENSE_TECH_AUTONOMOUS_SYSTEMS`  |      20 |         22 |         15 |         15 |        14 |       2 |    5 | 조달 지연, valuation 과열       |
| `DEFENSE_DRONE_COUNTER_UAS`        |      20 |         22 |         14 |         14 |        13 |       3 |    5 | 생산능력, M&A dilution, 수출통제  |
| `DEFENSE_AI_SOFTWARE_INTELLIGENCE` |      19 |         21 |         10 |         15 |        14 |       0 |    5 | prototype, 정치·윤리 리스크      |
| `SHIPBUILDING_OFFSHORE_BACKLOG`    |      20 |         22 |         18 |         13 |        13 |       1 |    5 | 저가수주, 후판가, 인건비            |
| `RAIL_INFRASTRUCTURE`              |      20 |         23 |         12 |         14 |        12 |       1 |    5 | 납기, 마진, financing         |
| `NUCLEAR_SMR_GRID_POLICY`          |      18 |         22 |         10 |         14 |        12 |       2 |    5 | 허가, 소송, 비용초과, financing   |
| `GEOPOLITICAL_RECONSTRUCTION`      |      10 |          8 |          8 |         10 |         7 |       0 |    4 | 실제 계약 없음, 정책 이벤트          |
| `SMART_FACTORY_AUTOMATION`         |      18 |         16 |          8 |         12 |        10 |       0 |    5 | MOU/PoC, 매출화 실패           |
| `AI_DATA_CENTER_POWER_EQUIPMENT`   |      21 |         22 |         18 |         13 |        12 |       0 |    5 | bookings 둔화, 저마진 프로젝트     |

---

# 9. stage date 후보

## `GRID_TRANSFORMER_SHORTAGE`

```text
Stage 1:
AI 데이터센터·EV·재생에너지로 변압기 부족 뉴스가 본격화된 날짜

Stage 2:
개별 기업의 공급계약 공시, 수주잔고 급증, 실적 서프라이즈, OP/EPS 상향 리포트 발생일

Stage 3:
FY1/FY2/FY3 추정치가 같이 올라가고, 시장이 과거 산업재가 아니라 AI 전력망 병목으로 평가하기 시작한 날

Stage 4B:
전력설비주 전반이 모두 AI 수혜로 인정되고 valuation band가 과거 대비 크게 상승한 날

Stage 4C:
신규수주 둔화, 저마진 계약, CAPA 정상화, 데이터센터 프로젝트 지연 확인일
```

## `DEFENSE_GOVERNMENT_BACKLOG`

```text
Stage 1:
유럽·중동·NATO 방산 수요 증가 뉴스

Stage 2:
공식 수주계약, 납품 스케줄, 수주잔고 증가 확인일

Stage 3:
다년 매출 visibility와 OPM 개선, EPS 상향 확인일

Stage 4B:
방산주 동반 과열, 모두가 K방산 수출 성장 인정

Stage 4C:
납기 지연, 수출허가 문제, 대규모 dilution, 계약 취소
```

## `SHIPBUILDING_OFFSHORE_BACKLOG`

```text
Stage 1:
신조선가 상승, LNG선·선박 발주 회복 뉴스

Stage 2:
대형 수주, 선가 상승, 저가수주 소진 확인

Stage 3:
고마진 선박 인도가 실적에 반영되고 FY2/FY3 OP 상향

Stage 4B:
조선주 동반 급등, 선가 상승 narrative 과밀

Stage 4C:
후판가·인건비 상승, 발주 둔화, 저마진 수주 확인
```

## `RAIL_INFRASTRUCTURE`

```text
Stage 1:
해외 철도 투자·입찰 뉴스

Stage 2:
공식 계약, 계약금액/매출 비중, 납품 스케줄 확인

Stage 3:
납품 visibility와 OP/EPS 상향이 같이 확인

Stage 4B:
대형 수주 기대가 가격에 모두 반영

Stage 4C:
프로젝트 지연, financing 문제, 마진 악화
```

## `NUCLEAR_SMR_GRID_POLICY`

```text
Stage 1:
원전 정책, AI 전력수요, PPA, 우선협상 뉴스

Stage 2:
PPA 또는 실제 계약 서명, 기자재 매출화 경로 확인

Stage 3:
법적·허가·financing 리스크 낮고 FY2/FY3 매출 visibility 확인

Stage 4B:
원전 테마주 동반 과열

Stage 4C:
법원 가처분, 계약 지연, 프로젝트 취소, 비용초과
```

---

# 10. 가격경로 검증계획

## R1 공통 검증 방식

```text
1. 각 case의 stage1_date, stage2_date, stage3_date를 지정한다.
2. 해당 날짜의 종가를 stage_price로 저장한다.
3. 30D / 90D / 180D / 1Y / 2Y MFE를 계산한다.
4. 30D / 90D / 180D / 1Y MAE를 계산한다.
5. peak_price와 drawdown_after_peak를 계산한다.
6. EPS revision, 수주잔고, 계약질 지표와 주가 경로를 비교한다.
```

## 성공 판정

```text
aligned:
Stage 2/3 이후 주가가 6~24개월 동안 리레이팅되고,
OP/EPS 상향 또는 수주잔고 증가가 같이 지속됨.

cyclical_success:
주가는 크게 올랐지만, 구조적 EPS 지속성이 아니라 cycle이 원인.

event_premium:
정책·입찰·재건·MOU로 급등했지만 실제 계약·매출 없음.

false_positive_score:
계약 뉴스는 강했지만 마진·EPS가 안 따라오거나 주가가 원위치.

thesis_break:
계약 취소, 법적 지연, 감사·회계 문제, dilution shock, 프로젝트 취소.
```

## 이번 R1에서 우선 검증할 가격 case

| case_id                                              |      stage2 후보일 | 확인할 가격 경로                            |
| ---------------------------------------------------- | --------------: | ------------------------------------ |
| `hd_hyundai_electric_transformer_shortage_candidate` | 각 주요 공급계약/실적발표일 | 1Y/2Y MFE, EPS revision 지속           |
| `hyosung_heavy_transformer_backlog_candidate`        |     수주잔고·실적 상향일 | 수주잔고 대비 주가 리레이팅                      |
| `hanwha_aerospace_romania_k9_success_case`           |      2024-07-09 | 당일 +5% 이후 1Y MFE/MAE                 |
| `hanwha_aerospace_dilution_risk_case`                |      2025-03-27 | 당일 -13% 이후 회복 여부                     |
| `hyundai_rotem_morocco_rail_order_case`              |      2025-02-26 | 180D/1Y MFE, OP revision             |
| `korean_shipbuilders_contract_rally_case`            |         WSJ 보도일 | 하루 급등 이후 180D/1Y 지속 여부               |
| `meta_constellation_nuclear_ppa_reference`           |      2025-06-03 | Constellation/원전 PPA 관련주 반응          |
| `nuscale_cfpp_cancel_4c_case`                        |         2023-11 | 프로젝트 취소 후 drawdown                   |
| `khnp_czech_legal_delay_case`                        |         2025-05 | 원전 기자재·정책주 반응                        |
| `palantir_maven_contract_case`                       |      2024-05-29 | prototype 계약 후 장기 revenue 전환         |
| `anduril_lccm_reference_case`                        |      2026-05-13 | 비상장 reference, 상장 supply chain 매핑 필요 |

---

# 11. 다음에 에이전트가 채워야 할 price fields

R1 case library에 아래 필드를 채우게 하면 된다.

```text
case_id
symbol
company_name
primary_archetype
secondary_archetypes

stage1_date
stage2_date
stage3_date
stage4b_date
stage4c_date

stage1_price
stage2_price
stage3_price
stage4b_price
stage4c_price
peak_price

MFE_30D
MFE_90D
MFE_180D
MFE_1Y
MFE_2Y

MAE_30D
MAE_90D
MAE_180D
MAE_1Y

drawdown_after_peak
below_stage3_price_flag

op_revision_1q
op_revision_1y
eps_revision_1q
eps_revision_1y
backlog_growth
contract_amount_to_sales
contract_duration_months
margin_change

score_price_alignment
price_validation_status
```

---

# R1 결론

이번 R1은 **Green 가능성이 높은 대섹터**다. 특히:

```text
전력설비·변압기
방산 정부 백로그
조선 고마진 수주
철도 대형 수출
데이터센터 전력장비
```

이쪽은 서생원식 구조와 잘 맞는다.

다만 전부 Green이 아니라, archetype별 gate가 다르다.

```text
전력설비:
계약질 + 리드타임 + 가격전가 + EPS 상향 필요.

방산:
정부계약 + 다년 납품 + 수주잔고 + 자본배분 리스크 확인.

조선:
선가 + 저가수주 소진 + 마진 인식 시점 확인.

철도:
실제 계약과 납품 스케줄은 좋지만 마진·financing 확인.

원전/SMR:
PPA·계약 확정은 좋지만 허가·소송·비용초과 리스크 큼.

재건/네옴/정책:
실제 계약 전까지 event_watch.
```

**R1 점수정규화의 핵심 문장:**

> 산업재·수주·인프라는 “수주 뉴스”가 아니라 **계약질, 납품기간, 수주잔고, 마진, EPS 상향, 가격경로 리레이팅**이 같이 확인될 때만 Stage 3 후보가 된다.

다음에 네가 “다음 라운드 진행해줘”라고 하면, 정해둔 순서에 따라 **R2 — AI·반도체·전자부품**으로 넘어간다.

[1]: https://www.reuters.com/business/energy/us-power-transformer-buyers-scramble-imports-factory-slots--reeii-2026-05-11/?utm_source=chatgpt.com "US power transformer buyers scramble for imports, factory slots"
[2]: https://www.reuters.com/business/aerospace-defense/south-koreas-hanwha-aerospace-wins-1-bln-order-romania-k9-howitzers-2024-07-09/?utm_source=chatgpt.com "South Korea's Hanwha Aerospace wins $1 bln order from Romania for self-propelled howitzers"
[3]: https://www.reuters.com/business/aerospace-defense/hanwha-aerospaces-europe-land-arms-sales-double-by-2027-ceo-says-2024-10-07/?utm_source=chatgpt.com "Hanwha Aerospace's Europe land arms sales to double by 2027, CEO says"
[4]: https://www.reuters.com/markets/deals/hyundai-rotem-wins-15-billion-order-moroccos-national-rail-operator-2025-02-26/?utm_source=chatgpt.com "Hyundai Rotem wins $1.5 billion order from Morocco's national rail operator"
[5]: https://www.wsj.com/articles/south-korean-shipbuilders-rally-on-brisk-contract-wins-d44ecb8a?utm_source=chatgpt.com "South Korean Shipbuilders Rally on Brisk Contract Wins"
[6]: https://www.reuters.com/sustainability/climate-energy/meta-signs-power-agreement-with-constellation-nuclear-plant-2025-06-03/?utm_source=chatgpt.com "Meta signs power agreement with Constellation nuclear plant"
[7]: https://www.reuters.com/business/pentagon-strikes-agreements-with-defense-firms-containerized-missiles-2026-05-13/?utm_source=chatgpt.com "Pentagon strikes agreements with defense firms on containerized missiles"
[8]: https://www.reuters.com/technology/palantir-wins-480-million-us-army-deal-maven-prototype-2024-05-29/?utm_source=chatgpt.com "Pentagon awards $480 million deal to Palantir for 'Maven' prototype"
[9]: https://www.reuters.com/business/aerospace-defense/south-korea-market-watchdog-orders-hanwha-aerospace-revise-share-issuance-plan-2025-03-27/?utm_source=chatgpt.com "S. Korea watchdog blocks Hanwha Aerospace $2.5 billion capital raising plan"
[10]: https://en.wikipedia.org/wiki/NuScale_Power?utm_source=chatgpt.com "NuScale Power"
[11]: https://apnews.com/article/2dcaa77856b7837c596cb0291dad5659?utm_source=chatgpt.com "A Czech court blocks the signing of a deal with South Korea's KHNP to build 2 nuclear reactors"
[12]: https://www.ft.com/content/994a0a80-414f-442f-bf41-f2dbde5a04ca?utm_source=chatgpt.com "South Korea's biggest defence group plans $2.5bn share sale to expand overseas"
