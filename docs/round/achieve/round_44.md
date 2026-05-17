좋아. 정해둔 순서대로 이번은 **R4 — 소재·스프레드·전략자원**으로 넘어간다.

R4는 R1·R2와 성격이 완전히 다르다. 여기는 주가와 EPS가 크게 움직일 수 있지만, 대부분이 **구조적 리레이팅**이라기보다 **가격·스프레드·정책·지정학 사이클**에서 출발한다. 그래서 Green을 쉽게 주면 안 된다. 업로드된 Theme Tag Map에서도 화학·정유·철강·비철·리튬·희토류·금은·그래핀·맥신·초전도체·제지·골판지 같은 테마는 대부분 Watch/Red 중심이고, 전략금속도 실제 계약·매출·공급망 근거가 있을 때만 점수가 올라가도록 정리되어 있다.

서생원식 기준으로도 R4의 핵심은 “원자재 가격이 올랐다”가 아니라, **원자재·스프레드 변화가 EPS/FCF 체급 변화로 지속되고, 시장이 과거 commodity/cycle 프레임으로 낮게 평가하고 있는가**다.

---

# R4. 소재·스프레드·전략자원

## 1. 이번 라운드 대섹터

```text
R4 = 소재·스프레드·전략자원
```

기본 구조는 이거다.

```text
원자재 가격 / 제품 spread / 지정학 / 공급망 정책
→ EPS 급변
→ 단기 주가 급등 가능
→ 하지만 구조적 지속성은 낮은 경우가 많음
→ Green보다 cycle_success / event_premium / 4B·4C 방어가 중요
```

R4의 핵심 질문은 이거다.

```text
이건 구조적 EPS/FCF 체급 변화인가?
아니면 가격·스프레드·정책 이벤트인가?
```

---

## 2. 대상 canonical archetype

| 구분           | canonical archetype                   | Green 정책       |
| ------------ | ------------------------------------- | -------------- |
| 정유·유가 spread | `REFINING_OIL_SPREAD`                 | Watch          |
| 화학 spread    | `CHEMICAL_SPREAD`                     | Watch/Red      |
| 철강 spread    | `STEEL_METAL_SPREAD`                  | Watch          |
| 비철금속         | `NONFERROUS_STRATEGIC_METALS`         | Watch          |
| 전략금속·희토류     | `RARE_METALS_STRATEGIC_MATERIALS`     | Watch-to-Green |
| 리튬 원재료       | `LITHIUM_BATTERY_RAW_MATERIAL`        | Cycle/Watch    |
| 금은·금광주       | `PRECIOUS_METALS_SAFE_HAVEN_MINERS`   | Cycle/Watch    |
| 초전도체·그래핀·맥신  | `ADVANCED_MATERIAL_SPECULATIVE_THEME` | Red/Watch      |
| 제지·골판지·포장재   | `PAPER_PACKAGING_CYCLE`               | Watch          |
| 농산물 input    | `AGRI_COMMODITY_INPUTS`               | Event/Watch    |
| LNG·에너지 트레이딩 | `LNG_ENERGY_TRADING_DISTRIBUTION`     | Watch-to-Green |
| 종합상사·자원 인프라  | `GENERAL_TRADING_RESOURCE_INFRA`      | Watch-to-Green |
| LNG·가스 유틸리티  | `ENERGY_UTILITY_LNG_GAS`              | Watch          |

---

## 3. deep sub-archetype

```text
REFINING_OIL_SPREAD
- 정유
- 윤활유
- LPG
- 유류도소매
- 재고손익
- 정제마진

CHEMICAL_SPREAD
- 석유화학
- 페인트
- 주정
- 제품 spread
- 중국·중동 공급과잉

STEEL_METAL_SPREAD
- 철강 주요업체
- 철강 중소형
- 강관
- 철근
- 건자재 철근
- 중국 수출·공급과잉

NONFERROUS_STRATEGIC_METALS
- 구리
- 아연
- 알루미늄
- 제련마진
- 비철금속 cycle

RARE_METALS_STRATEGIC_MATERIALS
- 희토류
- NdPr
- dysprosium
- terbium
- 국방 공급망
- price floor
- offtake
- 정부 투자

LITHIUM_BATTERY_RAW_MATERIAL
- 리튬
- 리튬 정제
- 광산 재가동
- EV 수요
- ESS 수요
- 가격 급락

PRECIOUS_METALS_SAFE_HAVEN_MINERS
- 금
- 은
- 금광주
- AISC
- realized price
- 안전자산

ADVANCED_MATERIAL_SPECULATIVE_THEME
- 초전도체
- 맥신
- 그래핀
- 페라이트
- 양자 소재

PAPER_PACKAGING_CYCLE
- 제지
- 골판지
- 택배 포장재
- 탈플라스틱 포장재
- 원지 가격

GENERAL_TRADING_RESOURCE_INFRA
- 종합상사
- 자원권
- LNG 장기계약
- 철강 공급
- 배당·자사주
- 복합기업 discount 해소

LNG_ENERGY_TRADING_DISTRIBUTION
- LNG 장기 offtake
- LPG
- 유류도소매
- 윤활유
- 에너지 조달 안정성
```

---

# 4. 성공사례

## 4-1. 전략금속: MP Materials / Pentagon / Apple

MP Materials는 `RARE_METALS_STRATEGIC_MATERIALS`의 가장 좋은 성공 후보 중 하나다. 미국 국방부가 MP Materials에 4억 달러를 투자해 최대주주가 되었고, 신규 자석 공장 생산물을 10년간 구매하는 구조와 핵심 희토류 가격 floor를 제공했다. Apple도 5억 달러 규모 계약으로 재활용 소재 기반 자석 생산을 지원한다. 이건 단순 희토류 가격 테마가 아니라 **정부 투자 + 가격 하방 + 장기 구매계약 + 공급망 안보**가 결합된 사례다. ([AP News][1])

**가격경로 1차 판정**

```text
판정:
structural_success_candidate

가격 확인:
보도 단위에서는 MP의 주가 급등이 확인되지만,
정확한 stage price / MFE / MAE는 price backfill 필요.

점수 의미:
희토류 가격 상승만으로는 Watch.
하지만 정부 투자 + price floor + 10년 offtake가 붙으면 Watch-to-Green.
```

**점수 교정**

```text
EPS/FCF: 중간~강함
Structural Visibility: 강함
Bottleneck/Pricing: 강함
Market Mispricing: 중간~강함
Risk: project execution, commodity price, policy dependency
```

---

## 4-2. 전략금속: 중국 희토류 수출통제

중국의 희토류 수출통제는 `RARE_METALS_STRATEGIC_MATERIALS`의 정책·병목 점수를 높이는 근거다. Reuters는 2025년 4월 이후 중국의 heavy rare earth 수출 제한이 이어지고, dysprosium·terbium 같은 핵심 원소가 일본·독일 등으로 거의 공급되지 않아 생산 차질과 가격 급등을 만들었다고 보도했다. ([Reuters][2])

**가격경로 1차 판정**

```text
판정:
geopolitical_bottleneck_reference

주의:
희토류 수출통제 뉴스만으로 개별 관련주 Green 금지.
실제 생산능력, offtake, 고객사, FCF가 있어야 Stage 2 이상.
```

---

## 4-3. Korea Zinc 공개매수 이벤트

Korea Zinc는 `NONFERROUS_STRATEGIC_METALS`, `RARE_METALS_STRATEGIC_MATERIALS`, `HOLDING_GOVERNANCE_EVENT`가 섞인 사례다. MBK Partners와 Young Poong의 공개매수 발표 후 Korea Zinc 주가는 19.8% 상승했고, Young Poong은 상한가 30%까지 올랐다. 하지만 이건 구조적 FCF 리레이팅인지, 경영권·공개매수 프리미엄인지 분리해야 한다. ([Reuters][3])

**가격경로 1차 판정**

```text
가격 반응:
Korea Zinc +19.8%
Young Poong +30%

판정:
event_premium + governance_watch

의미:
전략금속 exposure는 있지만,
이 가격 반응은 우선 event premium으로 분류해야 한다.
```

**점수 교정**

```text
Strategic metal score:
중간

Governance/event score:
강함

Structural Green:
FCF 개선, 제련마진, 자본배분, 공급망 병목이 따로 확인될 때만.
```

---

## 4-4. 종합상사: Berkshire의 일본 5대 상사 투자

일본 5대 종합상사는 `GENERAL_TRADING_RESOURCE_INFRA`의 기준 성공 사례다. Berkshire Hathaway는 Itochu, Marubeni, Mitsubishi, Mitsui, Sumitomo 지분을 9%대까지 늘렸고, 이 회사들은 원자재, 에너지, 철광석, 구리, 식품, 물류, 기계 수출 지원 등 복합 사업을 영위한다. 즉 종합상사는 단순 무역회사라기보다 **자원·에너지·무역·인프라 cash flow와 자본배분이 결합된 복합기업**으로 리레이팅될 수 있다. ([Financial Times][4])

**가격경로 1차 판정**

```text
판정:
structural_reference_case

의미:
종합상사는 단순 매출 규모가 아니라
FCF, 배당, 자사주, ROE, 자원권, 장기계약이 핵심.
```

**점수 교정**

```text
EPS/FCF: 중간
Structural Visibility: 중간~강함
Market Mispricing: 강함 가능
Valuation Rerating: 강함 가능
Capital Allocation: 강함
Risk: commodity cycle, FX, 복합기업 discount
```

---

## 4-5. POSCO International / Alaska LNG 20년 계약

POSCO International은 `GENERAL_TRADING_RESOURCE_INFRA`와 `LNG_ENERGY_TRADING_DISTRIBUTION`의 좋은 후보 사례다. Glenfarne Alaska LNG는 POSCO International에 연 100만 톤 LNG를 20년 공급하는 계약을 체결했고, POSCO는 프로젝트 투자와 807마일 파이프라인용 철강 공급도 맡을 예정이다. 이건 단순 에너지 가격 테마가 아니라 **20년 LNG 공급계약 + 프로젝트 지분 + 철강 공급**이 결합된 구조다. ([Reuters][5])

**가격경로 1차 판정**

```text
판정:
watch_to_green_candidate

확인 필요:
POSCO International stage2_price
계약 발표 후 180D/1Y MFE
실제 FID 여부
철강 공급 매출화
LNG 계약 마진
```

**점수 교정**

```text
장기계약: 점수 강화
프로젝트 FID 전: Green 제한
LNG 가격·정책·financing risk: 감점
```

---

## 4-6. Barrick / 금광주

Barrick은 `PRECIOUS_METALS_SAFE_HAVEN_MINERS`의 성공 후보 사례다. Barrick은 2026년 1분기 record gold price 덕분에 실적 예상을 상회했고, 평균 금 가격은 전년 대비 63% 상승한 4,673.5달러, 평균 실현가격은 4,823달러였다. AISC는 4% 하락했고, 순이익은 전년 대비 3배 증가했으며 30억 달러 자사주 매입도 발표했다. ([Reuters][6])

**가격경로 1차 판정**

```text
판정:
cyclical_success_candidate

의미:
금 가격 + 비용 통제 + 자사주가 같이 있으면 강한 수익 후보.
하지만 구조적 Green이라기보다 commodity/cycle 성공으로 분류.
```

**점수 교정**

```text
EPS/FCF: 강함
Structural Visibility: 낮음
Bottleneck/Pricing: 중간~강함
Capital Allocation: 중간~강함
Risk: 금 가격 조정, AISC 상승, 광산 정치 리스크
```

---

## 4-7. 정유: SK Innovation 흑자전환

SK Innovation은 2026년 1분기 2.2조 원 영업이익을 기록해 전년 동기 300억 원 손실에서 크게 흑자전환했고, 시장 예상 1.4조 원도 웃돌았다. 다만 회사는 정유사업의 생산·물류 정상화가 시간이 걸릴 수 있다고 경고했다. ([Reuters][7])

**가격경로 1차 판정**

```text
판정:
cyclical_recovery_candidate

의미:
실적은 강하지만 회사가 직접 회복 지연을 경고.
정유는 Green보다 cycle/watch가 맞다.
```

**점수 교정**

```text
EPS/FCF: 강함
Structural Visibility: 낮음~중간
Bottleneck/Pricing: 강함
Risk: 정제마진, 재고손익, 지정학, 물류 정상화
```

---

# 5. 반례

## 5-1. 화학: LG Chem / Lotte Chemical 공급과잉

화학은 R4에서 Green을 가장 조심해야 하는 축이다. LG Chem과 Lotte Chemical은 2024년에 중국·중동 capacity 부담과 공급과잉 때문에 실적이 크게 훼손됐다. Lotte Chemical은 2024년 8,950억 원 영업손실을 기록했고, 이는 2011년 이후 최대 손실이었다. LG Chem의 2024년 영업이익도 63.75% 감소해 2019년 이후 최저 수준이었다. ([Reuters][8])

**교훈**

```text
제품 spread 개선 뉴스만으로 Green 금지.
중국·중동 공급과잉이 있으면 structural_visibility를 낮게 둔다.
```

**가격경로 1차 판정**

```text
판정:
hard_counterexample_for_chemical_green

의미:
화학은 EPS가 잠깐 반등해도 구조적 리레이팅으로 보기 어렵다.
```

---

## 5-2. 철강: 중국 공급과잉과 수출 압박

Baosteel은 중국 정부가 2025년에 전국 steel output cut을 추진할 가능성이 높다고 봤고, 중국 철강업은 이미 overcapacity와 약한 수요에 시달리고 있다. 2024년 중국 steel exports는 110.72 million tons로 9년 만의 고점이었다. ([Reuters][9])

**교훈**

```text
철강은 Green 제한.
중국 공급과잉, 수출, 건설수요, 원가가 핵심 감점축.
```

**가격경로 1차 판정**

```text
Baosteel은 비용절감으로 Q1 순이익이 증가하며 주가가 5.7% 상승했지만,
이는 구조적 리레이팅보다 cost-cut/cycle 개선에 가깝다. :contentReference[oaicite:11]{index=11}
```

---

## 5-3. 철광석 / BHP 반례

BHP는 철광석 가격 약세와 중국 수요 둔화, 글로벌 공급 부담 때문에 2025년 연간 underlying profit이 5년 최저 수준으로 내려갔고, 배당도 2017년 이후 가장 약한 수준으로 낮췄다. ([Reuters][10])

**교훈**

```text
원자재 대형주는 가격 cycle과 중국 수요에 묶인다.
배당·자본환원도 commodity peak 이후 빠르게 낮아질 수 있다.
```

---

## 5-4. 리튬 가격 86% 급락

리튬 가격은 2022년 11월 고점 이후 약 86% 하락했고, 이 때문에 전 세계 광산이 폐쇄되었다. 가격 안정 가능성은 있지만, 가격이 오르면 닫혔던 광산이 재가동되어 상승폭을 제한할 수 있다는 분석도 나온다. ([Reuters][11])

**교훈**

```text
리튬 가격 반등
≠ 구조적 Green

저비용 광산
장기 offtake
FCF 방어력
CAPEX 절제
가 없으면 Watch/Red.
```

---

## 5-5. Korea Zinc event premium

Korea Zinc는 전략금속과 governance가 섞인 흥미로운 케이스지만, 공개매수 발표 후 주가 상승은 우선 event premium이다. 이걸 구조적 FCF 리레이팅 성공사례로 넣으면 점수체계가 오염된다. ([Reuters][3])

---

## 5-6. 제지·골판지·포장재: 성숙 산업과 경쟁

DS Smith와 Mondi, International Paper 관련 거래는 포장재 산업의 consolidation을 보여준다. 하지만 Reuters는 DS Smith/Mondi 거래 당시 포장재 업체들이 전자상거래 수요 붐 이후 낮은 물량과 가격 압박을 겪었다고 설명했다. 즉 포장재는 지속 가능한 Green보다는 성숙 산업 consolidation과 가격·원가 cycle로 봐야 한다. ([Reuters][12])

International Paper도 DS Smith 인수 관련 EU 경쟁당국 조건을 맞추기 위해 유럽 5개 골판지 박스 공장을 매각하기로 했다. 이는 포장재 산업에서 규모의 경제와 M&A가 중요하지만, 경쟁·규제·자본배분 리스크도 함께 존재한다는 뜻이다. ([Reuters][13])

---

# 6. 4B-watch 사례

## 6-1. 희토류·전략금속 4B

```text
4B 조건:
- 중국 수출통제 뉴스로 관련주 동반 급등
- 정부지원·offtake 없는 기업까지 같이 상승
- 희토류 가격 급등만으로 valuation 확장
- 실제 생산능력과 FCF 확인 전 가격이 먼저 감
```

MP Materials처럼 정부 투자·price floor·offtake가 있는 경우는 다르지만, 대부분의 희토류 테마주는 price-only rally가 될 수 있다. ([AP News][1])

---

## 6-2. Korea Zinc 경영권 이벤트 4B

```text
4B 조건:
- 공개매수 가격 주변으로 주가 급등
- 경영권 프리미엄이 과열
- 본업 FCF보다 지배권 이벤트가 가격을 지배
```

Korea Zinc +19.8%, Young Poong +30%는 강한 가격 반응이지만 event premium으로 우선 분류한다. ([Reuters][3])

---

## 6-3. 금·금광주 4B

```text
4B 조건:
- 금 가격 record high
- 금광주 EPS 급등
- 안전자산 narrative 과밀
- 금리·달러·인플레이션 방향이 바뀌기 시작
```

Barrick처럼 금 가격, AISC, 자사주가 같이 있으면 성공 후보지만, gold price peak 이후 drawdown을 반드시 봐야 한다. ([Reuters][6])

---

## 6-4. 정유·화학 회복 기대 4B

```text
4B 조건:
- 정제마진·화학 spread 회복 기대가 과도하게 선반영
- 실제 demand recovery 없이 주가만 반등
- 재고손익이 본업 개선처럼 오인됨
```

SK Innovation처럼 실적이 좋아도 회사가 회복 지연을 경고하면 Green이 아니라 cycle/watch로 둬야 한다. ([Reuters][7])

---

# 7. 4C-thesis-break 사례

## 7-1. 화학 공급과잉 지속

```text
4C:
China/Middle East capacity glut
제품 spread 재악화
재고 증가
OP/FCF 재하락
```

LG Chem과 Lotte Chemical의 2024년 실적 악화는 화학 Green 오판의 대표 4C다. ([Reuters][8])

---

## 7-2. 리튬 가격 급락과 광산 재가동

```text
4C:
lithium_price_crash
mine_shutdown
mine_restart_supply_rebound
CAPEX cut
EV demand slowdown
```

리튬은 가격이 올라가도 폐쇄 광산 재가동 가능성이 상승을 제한할 수 있다. ([Reuters][11])

---

## 7-3. 철강 중국 공급과잉

```text
4C:
Chinese steel exports surge
domestic demand weak
tariff conflict
price pressure
```

Baosteel이 언급한 overcapacity와 110.72 million ton export는 철강 structural Green을 제한한다. ([Reuters][9])

---

## 7-4. 원자재 대형주 배당 축소

BHP는 철광석 가격 약세와 중국 수요 둔화로 이익이 5년 최저 수준을 기록했고, 배당도 낮췄다. 원자재 cycle이 꺾이면 FCF와 자본환원도 같이 약해진다. ([Reuters][10])

---

## 7-5. 포장재 M&A 기대와 성숙산업 한계

포장재는 e-commerce와 탈플라스틱 narrative가 있지만, 낮은 물량·가격 압박과 성숙산업 특성이 강하다. M&A 프리미엄이 있어도 구조적 리레이팅은 따로 검증해야 한다. ([Reuters][12])

---

# 8. 점수비중 보정표 — R4 v1.0

| canonical archetype                   | EPS/FCF | Visibility | Bottleneck | Mispricing | Valuation | Capital | Info | 핵심 감점                          |
| ------------------------------------- | ------: | ---------: | ---------: | ---------: | --------: | ------: | ---: | ------------------------------ |
| `REFINING_OIL_SPREAD`                 |      20 |         10 |         18 |         10 |        10 |       2 |    5 | 정제마진, 재고손익, 지정학, 물류            |
| `CHEMICAL_SPREAD`                     |      20 |          8 |         16 |          8 |         8 |       0 |    5 | 중국·중동 공급과잉, spread reversal    |
| `STEEL_METAL_SPREAD`                  |      18 |         10 |         16 |         10 |        10 |       1 |    5 | 중국 수출, 건설수요, 원가                |
| `NONFERROUS_STRATEGIC_METALS`         |      18 |         14 |         15 |         12 |        11 |       2 |    5 | 금속가격, 제련마진, 중국 수요              |
| `RARE_METALS_STRATEGIC_MATERIALS`     |      18 |         18 |         18 |         14 |        13 |       5 |    5 | 정책 의존, 생산능력, project execution |
| `LITHIUM_BATTERY_RAW_MATERIAL`        |      19 |         10 |         16 |          9 |         8 |       0 |    5 | 가격 급락, 광산 재가동, EV 둔화           |
| `PRECIOUS_METALS_SAFE_HAVEN_MINERS`   |      20 |         10 |         16 |          9 |         8 |       5 |    5 | 금가격 조정, AISC, 광산 정치 리스크        |
| `ADVANCED_MATERIAL_SPECULATIVE_THEME` |       5 |          5 |          5 |          5 |         5 |       0 |    3 | 상용화 부재, 논문·테마만 있음              |
| `PAPER_PACKAGING_CYCLE`               |      17 |         13 |         12 |         10 |         9 |       3 |    5 | 원가, 과잉경쟁, 성숙산업                 |
| `AGRI_COMMODITY_INPUTS`               |      18 |         10 |         14 |          8 |         8 |       0 |    5 | 곡물·날씨·질병·원가                    |
| `LNG_ENERGY_TRADING_DISTRIBUTION`     |      18 |         15 |         16 |         10 |        10 |       2 |    5 | 가격·재고·관세·지정학                   |
| `GENERAL_TRADING_RESOURCE_INFRA`      |      17 |         19 |         12 |         15 |        18 |       8 |    5 | commodity, FX, 복합기업 discount   |
| `ENERGY_UTILITY_LNG_GAS`              |      17 |         18 |          6 |         12 |        10 |       5 |    5 | 요금규제, 부채, 미수금                  |

---

# 9. stage date 후보

## `CHEMICAL_SPREAD`

```text
Stage 1:
화학 spread 회복 기대, 중국 stimulus, 제품가격 반등 뉴스

Stage 2:
실제 영업이익 개선, 제품 spread 개선, 재고 정상화 확인일

Stage 3:
공급과잉 완화와 구조조정이 확인될 때만

Stage 4B:
spread 회복 기대가 주가에 과도하게 반영

Stage 4C:
중국·중동 공급과잉 지속, OP 재악화, 재고 증가
```

## `REFINING_OIL_SPREAD`

```text
Stage 1:
정제마진 반등, 유가·지정학 이벤트

Stage 2:
정유 영업이익 개선, 재고손익 제외 본업 마진 확인

Stage 3:
구조적 Green은 제한. 반복 FCF와 고마진 mix가 확인된 경우만

Stage 4B:
정제마진 peak와 주가 과열

Stage 4C:
정제마진 하락, 재고손실, 물류·생산 정상화 지연
```

## `RARE_METALS_STRATEGIC_MATERIALS`

```text
Stage 1:
희토류 수출통제, 정부 공급망 정책, 국방 수요 뉴스

Stage 2:
정부 투자, price floor, offtake, 장기 구매계약 확인

Stage 3:
생산능력과 FCF 전환이 확인될 때

Stage 4B:
희토류 테마 전반 과열

Stage 4C:
프로젝트 지연, 가격 하락, 정책지원 축소
```

## `LITHIUM_BATTERY_RAW_MATERIAL`

```text
Stage 1:
리튬 가격 반등, 광산 폐쇄, EV 수요 뉴스

Stage 2:
저비용 광산, offtake, FCF 방어 확인

Stage 3:
극히 제한적. 가격 cycle을 넘어선 FCF 지속성 필요

Stage 4B:
리튬 가격 반등 기대 과열

Stage 4C:
가격 급락, 광산 재가동, EV 수요 둔화
```

## `PRECIOUS_METALS_SAFE_HAVEN_MINERS`

```text
Stage 1:
금·은 가격 breakout, 실질금리 하락, 안전자산 수요

Stage 2:
금광주 realized price, AISC, FCF 개선 확인

Stage 3:
자본환원과 비용 통제가 붙을 때만 Watch-to-Green

Stage 4B:
금 가격 record high와 금광주 동반 과열

Stage 4C:
금 가격 조정, AISC 상승, 생산량 감소
```

## `GENERAL_TRADING_RESOURCE_INFRA`

```text
Stage 1:
자원·에너지·장기계약, 배당·자사주, 복합기업 re-rating 뉴스

Stage 2:
장기 offtake, 프로젝트 지분, FCF, 자본배분 확인

Stage 3:
시장 프레임이 단순 무역회사에서 자원·인프라 FCF 기업으로 전환

Stage 4B:
Buffett류 종합상사 narrative 과밀

Stage 4C:
commodity 가격 하락, 프로젝트 지연, 자본배분 후퇴
```

---

# 10. 가격경로 검증계획

## R4 공통 검증 방식

```text
1. 각 case의 stage1_date, stage2_date, stage3_date를 지정한다.
2. stage date 기준 종가를 저장한다.
3. MFE_30D / 90D / 180D / 1Y / 2Y를 계산한다.
4. MAE_30D / 90D / 180D / 1Y를 계산한다.
5. peak_price와 drawdown_after_peak를 계산한다.
6. commodity price, 제품 spread, EPS revision, FCF, 배당·자사주와 주가 경로를 비교한다.
```

## R4에서 반드시 분리할 판정

```text
structural_success:
price floor, offtake, 장기계약, FCF, 자본배분이 같이 있는 경우

cyclical_success:
원자재 가격·spread 덕분에 주가와 EPS가 오른 경우

event_premium:
공개매수, 경영권 분쟁, 정책 이벤트로 오른 경우

false_positive_score:
가격·spread 뉴스는 강했지만 EPS/FCF가 지속되지 않은 경우

thesis_break:
공급과잉, 가격 급락, 프로젝트 지연, 배당 축소, 재고손실 발생
```

## 이번 R4에서 우선 검증할 가격 case

| case_id                                   |      stage2 후보일 | 현재 1차 가격판정                             |
| ----------------------------------------- | --------------: | -------------------------------------- |
| `lg_chem_lotte_chemical_oversupply_4c`    |      2025-02-07 | chemical Green hard counterexample     |
| `sk_innovation_refining_recovery_watch`   |      2026-05-13 | 흑자전환이나 recovery delay, cycle watch     |
| `baosteel_steel_oversupply_cost_cut_case` |      2025-04-28 | 비용절감 + 주가 +5.7%, cycle success         |
| `bhp_iron_ore_profit_dividend_cut_case`   |      2025-08-18 | iron ore downcycle 4C                  |
| `mp_materials_dod_apple_offtake_case`     |         2025-07 | strategic rare earth success candidate |
| `korea_zinc_tender_event_premium_case`    |      2024-09-13 | +19.8%, event_premium                  |
| `posco_international_alaska_lng_20y_case` |      2025-12-04 | 20년 LNG 계약, Watch-to-Green             |
| `berkshire_japan_sogo_shosha_case`        |      2025-03-17 | 종합상사 rerating reference                |
| `barrick_record_gold_buyback_case`        |      2026-05-11 | gold cyclical_success                  |
| `lithium_price_86pct_crash_case`          |      2025-01-13 | lithium 4C/cycle                       |
| `ds_smith_packaging_consolidation_case`   | 2024-03~2025-04 | packaging mature consolidation         |

---

# 11. 다음에 에이전트가 채워야 할 price fields

R4 case library에는 아래 필드가 필요하다.

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

commodity_price_at_stage
commodity_price_peak
commodity_price_change_90D
commodity_price_change_1Y

spread_metric
spread_change
inventory_gain_loss
revenue_revision_1q
op_revision_1q
eps_revision_1y
fcf_margin
dividend_change
buyback_amount

offtake_contract_flag
price_floor_flag
government_support_flag
tender_offer_flag
governance_event_flag
capex_cut_flag
oversupply_flag
supply_glut_flag

score_price_alignment
price_validation_status
```

---

# R4 결론

R4는 대부분 **Green보다 Watch/Cycle/Red 방어가 중요한 대섹터**다.

```text
Green 가능성이 생기는 경우:
- 희토류/전략금속에 정부투자 + price floor + offtake가 붙는 경우
- 종합상사에 장기계약 + 자원권 + FCF + 자본배분이 붙는 경우
- LNG 장기계약이 실제 FCF와 프로젝트 지분으로 연결되는 경우
- 금광주가 금 가격 + AISC 통제 + 자사주/배당을 동시에 보여주는 경우

대부분 Watch/Red인 경우:
- 화학 spread
- 정유 spread
- 철강
- 리튬
- 제지·골판지
- 초전도체·그래핀·맥신
- 단순 commodity price rally
```

**R4 점수정규화의 핵심 문장:**

> 소재·스프레드·전략자원은 “가격이 올랐다”가 아니라 **가격 상승이 얼마나 오래 EPS/FCF로 남는지, 그리고 그 지속성을 장기계약·price floor·offtake·자본배분이 보강하는지**를 봐야 한다.
> 그 증거가 없으면 대부분 structural_success가 아니라 cyclical_success 또는 event_premium이다.

다음에 네가 “다음 라운드 진행해줘”라고 하면, 정해둔 순서에 따라 **R5 — 소비재·유통·브랜드**로 넘어간다.

[1]: https://apnews.com/article/7efe8b903b9668433d7c0a60be50b8c9?utm_source=chatgpt.com "America's only rare earth producer gets a boost from Apple and Pentagon agreements"
[2]: https://www.reuters.com/business/aerospace-defense/trump-xi-weigh-rare-earth-truce-extension-chinas-curbs-still-bite-2026-05-13/?utm_source=chatgpt.com "Trump, Xi to weigh rare earth truce extension, but China's curbs still bite"
[3]: https://www.reuters.com/markets/deals/private-equity-mbk-young-poong-launch-15-bln-tender-offer-korea-zinc-shares-2024-09-13/?utm_source=chatgpt.com "Private equity MBK, Young Poong launch $1.5 bln tender offer for Korea Zinc shares"
[4]: https://www.ft.com/content/a267a933-0e6d-4091-bcb1-ddbb1bbf0cab?utm_source=chatgpt.com "Warren Buffett's Berkshire Hathaway lifts stakes in Japanese trading houses"
[5]: https://www.reuters.com/business/energy/glenfarne-finalizes-20-year-lng-supply-deal-with-south-koreas-posco-2025-12-04/?utm_source=chatgpt.com "Glenfarne finalizes 20-year LNG supply deal with South Korea's POSCO"
[6]: https://www.reuters.com/business/barrick-mining-beats-first-quarter-profit-estimates-2026-05-11/?utm_source=chatgpt.com "Barrick beats Q1 profit estimates on record gold prices, unveils $3 bln buyback"
[7]: https://www.reuters.com/world/asia-pacific/sk-innovation-warns-refining-recovery-take-time-beats-q1-profit-estimates-2026-05-13/?utm_source=chatgpt.com "SK Innovation warns refining recovery to take time, beats Q1 profit estimates"
[8]: https://www.reuters.com/markets/commodities/south-korean-petrochemical-firms-profits-plunge-2024-oversupply-persists-2025-02-07/?utm_source=chatgpt.com "South Korean petrochemical firms' profits plunge in 2024 as oversupply persists"
[9]: https://www.reuters.com/business/energy/chinas-baosteel-expects-nationwide-output-cuts-this-year-2025-04-28/?utm_source=chatgpt.com "China's Baosteel expects nationwide output cuts this year"
[10]: https://www.reuters.com/world/china/bhp-posts-smallest-profit-five-years-lower-iron-ore-prices-2025-08-18/?utm_source=chatgpt.com "BHP posts smallest profit in five years on lower iron ore prices"
[11]: https://www.reuters.com/markets/commodities/lithium-prices-stabilise-2025-mine-closures-china-ev-sales-ease-glut-analysts-2025-01-13/?utm_source=chatgpt.com "Lithium prices to stabilise in 2025 as mine closures, China EV sales ease glut, analysts say"
[12]: https://www.reuters.com/markets/deals/mondi-reaches-offer-buy-smaller-rival-ds-smith-2024-03-07/?utm_source=chatgpt.com "British packaging firm Mondi offers to buy smaller rival DS Smith for $6.57 billion"
[13]: https://www.reuters.com/markets/deals/international-paper-talks-divest-five-plants-europe-2025-04-14/?utm_source=chatgpt.com "International Paper in talks to divest five plants in Europe"
