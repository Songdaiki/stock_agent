좋아. 정해둔 순서대로 이번은 **R3 — 2차전지·전기차·친환경**으로 넘어간다.

R3는 R1·R2보다 훨씬 더 조심해야 하는 라운드야. 이유는 간단해. 이 대섹터는 성장 테마가 강해서 주가는 크게 움직일 수 있지만, 실제로는 **CAPEX 과잉, EV 수요 둔화, 광물가격 급락, 보조금·관세·정책 리스크** 때문에 Green 오판이 자주 나온다. 업로드된 Theme Tag Map에서도 2차전지 소재는 Watch/Red, 폐배터리·전고체는 Watch/Red, 태양광은 Watch/Red, 폐기물처리만 허가권·처리량·반복 FCF가 있으면 Green 가능으로 구분되어 있다.

서생원식 기준으로도 R3는 “성장산업이라 좋다”가 아니라, **EPS/FCF 체급 변화가 실제로 지속되는지**를 봐야 한다. 단순 테마, 정책, CAPA 증설, MOU는 점수 근거가 아니고, 실제 계약·가동률·마진·FCF·가격경로가 따라와야 한다.

---

# R3. 2차전지·전기차·친환경

## 1. 이번 라운드 대섹터

```text
R3 = 2차전지·전기차·친환경
```

기본 구조는 이거다.

```text
EV·ESS·재생에너지·탄소규제 수요 증가
→ 소재·부품·장비·충전·수소·태양광·폐기물·탄소회계 수요 발생
→ 실제 계약·가동률·마진·FCF로 연결되는지 확인
→ Green 가능 / Watch / Red를 분리
```

R3의 핵심은 **성장성보다 지속성**이다.

```text
좋은 신호:
장기계약, 가격전가, 가동률 상승, FCF 개선, 보조금 없이도 수익성 유지

나쁜 신호:
CAPA 과잉, EV 수요 둔화, 광물가격 하락, 보조금 의존, 관세·통관 리스크, 프로젝트 지연
```

---

## 2. 대상 canonical archetype

| 구분            | canonical archetype                | Green 정책        |
| ------------- | ---------------------------------- | --------------- |
| 2차전지 소재 과열    | `BATTERY_MATERIALS_CAPEX_OVERHEAT` | Watch/Red       |
| 2차전지 장비·부품    | `BATTERY_EQUIPMENT_PARTS`          | Watch-to-Green  |
| 폐배터리·ESS 전환   | `BATTERY_RECYCLING_ESS_SHIFT`      | Watch           |
| EV 충전·인프라     | `EV_INFRASTRUCTURE`                | Watch           |
| 수소·연료전지       | `HYDROGEN_FUEL_CELL_INFRA`         | Watch-to-Green  |
| 태양광 공급망       | `SOLAR_TARIFF_SUPPLYCHAIN`         | Watch/Red       |
| 풍력·재생에너지      | `RENEWABLE_ENERGY_POLICY`          | Watch           |
| LNG·에너지 유통    | `ENERGY_DISTRIBUTION_FUEL`         | Watch           |
| 폐기물·재활용       | `WASTE_RECYCLING_ENVIRONMENT`      | Green 가능        |
| 탄소배출권·CBAM    | `CARBON_CREDIT_CBAM_COMPLIANCE`    | Watch           |
| 데이터센터 물 재활용   | `DATA_CENTER_WATER_REUSE_INFRA`    | Watch-to-Green  |
| 전기차 화재·규제 리스크 | `EV_FIRE_RISK_OVERLAY`             | RedTeam overlay |

---

## 3. deep sub-archetype

```text
BATTERY_MATERIALS_CAPEX_OVERHEAT
- 양극재
- 음극재
- 전해액
- 분리막
- 리튬
- 니켈
- 흑연
- CAPA 증설
- EV 수요 둔화
- 광물가격 하락

BATTERY_EQUIPMENT_PARTS
- 2차전지 공정장비
- 배터리 부품
- 셀 제조장비
- 고객사 CAPEX
- 납품 스케줄

BATTERY_RECYCLING_ESS_SHIFT
- 폐배터리
- ESS
- LFP ESS
- 전고체 배터리
- 회수량
- 금속 회수 수익
- ESS 전환

EV_INFRASTRUCTURE
- 충전소
- 충전기
- 전기차 인프라
- 이용률
- 수익성
- 전기차 화재 규제

HYDROGEN_FUEL_CELL_INFRA
- 수소연료전지
- 수소차 인프라
- 수소 생산설비
- 전해조
- 상용차·선박·건설기계용 수소

SOLAR_TARIFF_SUPPLYCHAIN
- 태양광 셀
- 모듈
- 폴리실리콘
- 미국 공장
- 관세
- UFLPA 통관 리스크
- 보조금

RENEWABLE_ENERGY_POLICY
- 풍력
- 해상풍력
- 탄소배출권
- 재생에너지 정책
- 프로젝트 지연
- 원가 상승

WASTE_RECYCLING_ENVIRONMENT
- 폐기물처리
- 플라스틱 재활용
- 폐기물 에너지화
- 탈플라스틱
- 허가권
- 반복 FCF

CARBON_CREDIT_CBAM_COMPLIANCE
- 탄소배출권
- EU ETS
- CBAM
- 탄소회계
- 검증·모니터링
- 탄소비용 전가

DATA_CENTER_WATER_REUSE_INFRA
- AI 데이터센터 물 사용
- 물 재활용
- 수처리
- closed-loop cooling
```

---

# 4. 성공사례

## 4-1. LG에너지솔루션 ESS 전환 — `BATTERY_RECYCLING_ESS_SHIFT`

LG에너지솔루션은 2025년 7월 EV 배터리 수요 둔화와 미국 관세·정책 리스크를 경고하면서, ESS 배터리 생산 확대와 일부 미국 EV 라인의 ESS 전환 가능성을 제시했다. Q2 영업이익은 강했지만 회사는 북미 EV 수요가 2026년 초까지 둔화될 수 있다고 봤고, LFP 기반 ESS 생산능력을 2025년 17GWh에서 2026년 30GWh 이상으로 늘리려는 계획도 언급됐다. 주가는 발표 후 1.6% 하락했다. ([Reuters][1])

**가격경로 1차 판정**

```text
판정:
mixed_watch_candidate

긍정:
ESS 전환은 새로운 수요축.
LFP ESS는 EV 수요 둔화의 완충재가 될 수 있음.

부정:
발표 당일 주가 -1.6%.
시장은 EV 수요 둔화와 정책 리스크를 더 크게 봄.

현재 alignment:
evidence_good_but_price_failed_or_delayed
```

**점수 교정**

```text
ESS 전환은 점수 강화.
EV 수요 둔화는 risk penalty 강화.
Stage 3-Green은 아직 제한.
```

---

## 4-2. GM-LG Ultium Ohio plant / Tennessee ESS 전환 — `BATTERY_RECYCLING_ESS_SHIFT`

GM과 LG에너지솔루션의 Ohio Ultium Cells 공장은 EV 수요 둔화로 완전 재가동 일정이 불확실해졌고, 약 850명의 layoff 이후 소수 직원만 복귀 예정인 상태로 보도됐다. 반면 Tennessee 공장은 ESS 셀 생산으로 전환하는 흐름이 나타났다. 이 사례는 R3에서 가장 중요한 교훈을 준다. **EV 배터리 수요 둔화는 반례이고, ESS 전환은 별도 Watch 후보**다. ([Reuters][2])

**가격경로 1차 판정**

```text
판정:
EV_demand_slowdown_4c + ESS_shift_watch_candidate

의미:
EV CAPA 증설을 Green으로 보던 점수는 낮춰야 함.
ESS 전환은 별도 sub-archetype으로 분리해야 함.
```

**점수 교정**

```text
BATTERY_MATERIALS_CAPEX_OVERHEAT:
risk penalty 강화.

BATTERY_RECYCLING_ESS_SHIFT:
ESS 계약·가동률·마진 확인 시 Watch-to-Green 가능.
```

---

## 4-3. 현대차 수소연료전지 울산 공장 — `HYDROGEN_FUEL_CELL_INFRA`

현대차는 울산에 9,300억 원, 약 6.54억 달러 규모의 수소연료전지 생산시설 착공을 발표했다. 이 시설은 2027년 완공 예정이며, 승용차·상용차·버스·건설기계·선박용 연료전지와 전해조를 생산할 계획이다. 이건 수소 테마 중에서도 단순 정책 뉴스가 아니라 **실제 CAPEX와 생산능력**이 있는 Stage 1~2 후보로 볼 수 있다. ([Reuters][3])

**가격경로 1차 판정**

```text
판정:
stage1_to_stage2_success_candidate

검증 필요:
현대차 본사 주가보다, 수소 부품·연료전지 공급망의 실제 매출 연결성 확인 필요.
```

**점수 교정**

```text
수소는 Watch-to-Green.
실제 CAPEX는 점수 강화.
하지만 고객·가동률·OP 전환 전 Green은 금지.
```

---

## 4-4. 폐기물처리 플랫폼 — `WASTE_RECYCLING_ENVIRONMENT`

EQT는 한국 KJ Environment와 계열사를 인수해 폐기물 처리 플랫폼을 만들기로 했고, 해당 플랫폼은 플라스틱 재활용, 폐기물 에너지화, 재활용 폐기물 선별을 포함하며 한국 인구 절반 이상을 커버할 수 있는 구조로 보도됐다. 기업가치는 7.33억 달러 이상으로 제시됐다. 이건 폐기물처리가 단순 ESG 테마가 아니라 **허가권·처리시설·반복 FCF형 인프라**가 될 수 있음을 보여준다. ([Reuters][4])

**가격경로 1차 판정**

```text
판정:
structural_success_reference

주의:
비상장/인프라 reference 성격.
한국 상장 폐기물 업체에 매핑하려면 처리량, 허가권, FCF, M&A 프리미엄을 확인해야 함.
```

**점수 교정**

```text
WASTE_RECYCLING_ENVIRONMENT는 R3에서 드물게 Green 가능.
다만 폐배터리·재활용 테마만 있으면 Watch.
```

---

## 4-5. 탄소 ETS / CBAM — `CARBON_CREDIT_CBAM_COMPLIANCE`

EU 집행위는 EU ETS 개편을 검토하고 있고, 탄소가격제 수익을 더 산업계로 돌려 탈탄소 투자를 유도하는 방향이 논의되고 있다. ETS는 2005년부터 작동한 핵심 탄소가격제지만 산업 경쟁력과 에너지 가격에 대한 우려도 같이 존재한다. ([Reuters][5])

CBAM은 전기, 시멘트, 비료, 알루미늄, 철강 등 수입품에 탄소가격을 적용하는 구조이고, EU ETS와 함께 탄소누출을 막기 위한 장치로 작동한다. 연구 자료도 CBAM이 탄소 관련 무역 리스크와 산업 전환 관리에서 중요해질 수 있다고 정리한다. ([arXiv][6])

**가격경로 1차 판정**

```text
판정:
policy_structural_watch

의미:
탄소배출권 가격 테마 자체는 Green이 아님.
CBAM 대응·탄소회계·저탄소 제품 premium이 실제 매출로 연결되어야 함.
```

**점수 교정**

```text
탄소배출권:
Watch.

탄소회계·검증·CBAM compliance 반복매출:
Watch-to-Green 가능.

탄소가격 단순 exposure:
Green 금지.
```

---

# 5. 반례

## 5-1. EV 배터리 수요 둔화 — `BATTERY_MATERIALS_CAPEX_OVERHEAT`

LG에너지솔루션은 EV 배터리 수요가 관세와 미국 보조금 종료 영향으로 둔화될 수 있다고 경고했고, GM·Tesla 같은 주요 고객사가 영향을 받을 수 있다고 봤다. 이는 EV 배터리 소재·셀·부품 점수에서 **수요 지속성**을 보수적으로 봐야 한다는 핵심 반례다. ([Reuters][1])

**교훈**

```text
EV 성장 narrative
≠ 무조건 구조적 Green

EV 수요 둔화가 나오면:
CAPA 증설
양극재
리튬
폐배터리
공정장비
모두 risk penalty 상승
```

---

## 5-2. Qcells 공급망·통관 리스크 — `SOLAR_TARIFF_SUPPLYCHAIN`

Qcells는 미국 세관이 중국 강제노동방지법 관련으로 핵심 부품 수입을 억류하면서 조지아 공장 약 1,000명의 근무시간·임금을 줄이고 300명의 계약직을 해고했다. Reuters도 Qcells가 부품 지연으로 미국 태양광 공장 직원 약 1,000명을 furlough했다고 보도했다. 이건 태양광 archetype에서 **보조금·정책 수혜가 있어도 관세·통관·부품 공급망이 4C로 작동할 수 있음**을 보여준다. ([AP News][7])

**교훈**

```text
태양광 Green 금지 조건:
부품 억류
관세·통관 문제
보조금 축소
중국 공급망 리스크
가동률 하락
```

---

## 5-3. 트럼프 행정부의 중국계 태양광 규제 — `SOLAR_TARIFF_SUPPLYCHAIN`

중국계 태양광 기업에 대한 미국의 규제 강화는 미국 태양광 제조업 투자와 financing을 흔드는 요인이 됐다. Reuters는 중국 관련 소유·통제 기준 때문에 주요 installer, 보험사, 은행들이 일부 중국계 미국 태양광 공장과 거래를 중단했고, 이 공장들이 미국 태양광 패널 capacity의 3분의 1 이상을 차지한다고 보도했다. ([Reuters][8])

**교훈**

```text
태양광은 정책 수혜와 정책 리스크가 동시에 존재.
정책 뉴스만으로 Stage 3-Green 금지.
```

---

## 5-4. 풍력 프로젝트 지연·비용 상승 — `RENEWABLE_ENERGY_POLICY`

Ørsted는 Sunrise Wind 프로젝트 지연과 비용 상승, 미국 financing cost 증가로 17억 달러 impairment를 인식했다. 프로젝트는 2027년 하반기 가동 예정으로 밀렸고, monopile foundation 비용 증가가 핵심 원인 중 하나로 언급됐다. ([Reuters][9])

**교훈**

```text
풍력은 수주·정책이 있어도:
인허가
공급망
금리
foundation 비용
프로젝트 지연
이 모두 4C가 될 수 있다.
```

---

## 5-5. 리튬 가격 cycle — `LITHIUM_BATTERY_RAW_MATERIAL`

리튬 가격은 2022년 11월 고점 이후 약 86% 급락했고, 이로 인해 전 세계 광산 폐쇄가 발생했다. 2025년에 가격 안정 가능성이 있었지만, 닫힌 광산이 수익성이 생기면 재가동될 수 있어 상승폭이 제한될 수 있다는 분석도 나왔다. ([Reuters][10])

Albemarle은 비용절감으로 분기 흑자 전환에 성공했지만, 에너지 저장 부문 매출은 리튬 가격 하락으로 11억 달러 줄었고, 2025년 CAPEX를 전년 대비 절반 수준으로 낮추기로 했다. ([Reuters][11])

**교훈**

```text
리튬 가격 반등
≠ 구조적 Green

저비용 구조
장기 offtake
FCF 방어력
CAPEX 절제
가 있어야 Watch-to-Green 가능.
```

---

## 5-6. 전고체·폐배터리 테마 반례

전고체·폐배터리는 R3에서 가장 자주 오판되는 테마다.

```text
전고체:
상용화 전까지 SPECULATIVE/Watch.

폐배터리:
실제 회수량, 금속 회수율, 고객사, 마진 없으면 Watch.

폐배터리 테마주:
주가가 먼저 가도 recycling volume이 없으면 price_moved_without_evidence.
```

업로드된 테마맵에서도 전고체 배터리는 상용화 전 Green 금지, 폐배터리는 회수량·금속가격·수익성을 확인해야 하는 Watch로 분류되어 있다.

---

# 6. 4B-watch 사례

## 6-1. 2차전지 소재 과열

```text
4B-watch 조건:
- EV 소재 관련주가 모두 성장주로 재평가
- PER/PBR이 EPS보다 먼저 올라감
- 공급계약보다 CAPA 발표가 더 많아짐
- 애널리스트 목표가가 과밀하게 상향
- 광물가격과 EV 수요가 이미 둔화 조짐
```

2차전지 소재는 Stage 3-Green보다 4B-watch가 더 중요하다.

---

## 6-2. ESS 전환 과열

ESS 전환은 좋은 후보지만, EV 라인을 ESS로 전환한다는 뉴스만으로 모든 배터리·소재 기업이 리레이팅되면 4B-watch를 켜야 한다.

```text
4B 조건:
- ESS narrative가 너무 빠르게 반영
- 실제 ESS 계약·마진보다 주가가 먼저 감
- LFP ESS 경쟁자 증가
- 보조금 의존도 높음
```

---

## 6-3. 폐기물·재활용 M&A 프리미엄

폐기물처리는 Green 가능성이 있지만, 인프라펀드 M&A 프리미엄이 상장주 전체로 과도하게 번질 경우 4B-watch가 필요하다.

```text
4B 조건:
- 허가권 가치가 모두 반영
- M&A 프리미엄 기대가 과밀
- 처리량·FCF보다 multiple만 상승
```

---

## 6-4. 태양광 보조금 수혜 과열

태양광은 정책·보조금·미국 공장 narrative가 강하게 붙으면 단기 급등할 수 있다. 그러나 Qcells 사례처럼 통관·부품·관세 문제가 나오면 바로 4C로 전환될 수 있다. ([Reuters][12])

---

# 7. 4C-thesis-break 사례

## 7-1. EV 수요 둔화와 공장 가동 중단

GM-LG Ohio battery plant의 완전 재가동 일정 불확실성은 EV 배터리 CAPA thesis의 대표 4C-watch다. EV 수요 둔화로 공장이 idled 되고, 노동자 복귀 일정도 불확실해진 상황은 CAPA 증설 narrative를 직접 훼손한다. ([Reuters][2])

```text
4C:
EV_demand_slowdown
plant_idle
layoff
capacity_underutilization
```

---

## 7-2. 태양광 통관·관세·부품 억류

Qcells의 핵심 부품 억류와 worker furlough는 태양광 공급망 thesis의 hard 4C다. ([Reuters][12])

```text
4C:
customs_detention
tariff_risk
forced_labor_compliance
production_disruption
```

---

## 7-3. 풍력 impairment

Ørsted의 Sunrise Wind 17억 달러 impairment는 해상풍력 프로젝트가 정책 수혜에도 불구하고 금리·원가·일정 지연으로 무너질 수 있음을 보여준다. ([Reuters][9])

```text
4C:
cost_overrun
project_delay
financing_cost
impairment
```

---

## 7-4. 리튬 가격 급락

리튬 가격 86% 급락과 Albemarle의 매출 감소·CAPEX 축소는 `LITHIUM_BATTERY_RAW_MATERIAL`의 대표 4C다. ([Reuters][10])

```text
4C:
lithium_price_crash
mine_shutdown
capex_cut
revenue_drop
```

---

# 8. 점수비중 보정표 — R3 v1.0

| canonical archetype                | EPS/FCF | Visibility | Bottleneck | Mispricing | Valuation | Capital | Info | 핵심 감점                    |
| ---------------------------------- | ------: | ---------: | ---------: | ---------: | --------: | ------: | ---: | ------------------------ |
| `BATTERY_MATERIALS_CAPEX_OVERHEAT` |      20 |         16 |         14 |         10 |        10 |       0 |    5 | EV 수요 둔화, CAPA 과잉, 광물가격  |
| `BATTERY_EQUIPMENT_PARTS`          |      19 |         17 |         12 |         12 |        10 |       0 |    5 | 고객사 CAPEX cut, 납품 지연     |
| `BATTERY_RECYCLING_ESS_SHIFT`      |      20 |         16 |         14 |         10 |        10 |       0 |    5 | 회수량 부족, ESS 마진, EV 둔화    |
| `EV_INFRASTRUCTURE`                |      17 |         14 |          7 |         11 |         9 |       0 |    5 | 이용률 부족, 보조금 의존, 화재 규제    |
| `HYDROGEN_FUEL_CELL_INFRA`         |      18 |         18 |         12 |         12 |        10 |       0 |    5 | 고객 부재, 보조금 의존, 가동률       |
| `SOLAR_TARIFF_SUPPLYCHAIN`         |      18 |         17 |         12 |         12 |        10 |       0 |    5 | 관세, 통관, 보조금, 공급망         |
| `RENEWABLE_ENERGY_POLICY`          |      18 |         16 |         10 |         11 |         9 |       0 |    5 | 인허가, 금리, 원가, 프로젝트 지연     |
| `ENERGY_DISTRIBUTION_FUEL`         |      18 |         15 |         16 |         10 |        10 |       2 |    5 | 에너지 가격, 재고손익, 관세         |
| `WASTE_RECYCLING_ENVIRONMENT`      |      18 |         22 |         15 |         13 |        12 |       3 |    5 | 가동률, CAPEX, 금속가격         |
| `CARBON_CREDIT_CBAM_COMPLIANCE`    |      14 |         17 |         10 |         12 |         8 |       2 |    6 | 정책개편, 가격변동, greenwashing |
| `DATA_CENTER_WATER_REUSE_INFRA`    |      16 |         18 |         14 |         12 |        10 |       2 |    5 | 고객 부재, 지역반발, 경제성         |
| `EV_FIRE_RISK_OVERLAY`             |    gate |       gate |       gate |       gate |      gate |    gate | gate | 리콜, 화재, 규제, 보험비용         |

---

# 9. stage date 후보

## `BATTERY_MATERIALS_CAPEX_OVERHEAT`

```text
Stage 1:
EV 성장, 장기공급계약, CAPA 증설 뉴스

Stage 2:
실제 계약, 판가·마진 개선, OP/EPS 상향 확인일

Stage 3:
장기계약 + 가격전가 + FCF 훼손 없는 CAPEX가 확인된 경우만

Stage 4B:
PER/PBR 과열, CAPA 경쟁, 목표가 과밀 상향

Stage 4C:
EV 수요 둔화, 광물가격 하락, CAPA 과잉, 고객사 라인 가동중단
```

## `BATTERY_RECYCLING_ESS_SHIFT`

```text
Stage 1:
ESS 전환, 폐배터리, LFP ESS 생산 뉴스

Stage 2:
ESS 고객계약, 가동률, 회수량, 금속 회수 수익 확인

Stage 3:
ESS/재활용 매출이 반복 FCF로 이어질 때만

Stage 4B:
ESS narrative 과열, recycling premium 과열

Stage 4C:
회수량 부족, 금속가격 하락, 가동률 하락
```

## `HYDROGEN_FUEL_CELL_INFRA`

```text
Stage 1:
수소 공장 착공, 정책, 설비투자 뉴스

Stage 2:
고객사·수요처·생산능력·납품계약 확인

Stage 3:
가동률과 OP/EPS 전환 확인

Stage 4B:
수소 테마 동반 과열

Stage 4C:
보조금 축소, 고객 부재, 가동률 낮음, 프로젝트 지연
```

## `SOLAR_TARIFF_SUPPLYCHAIN`

```text
Stage 1:
미국 공장, 보조금, 태양광 수요 뉴스

Stage 2:
가동률, 고객사, 부품 공급 안정, OP 전환 확인

Stage 3:
보조금 없이도 FCF가 나올 때만

Stage 4B:
미국 태양광 제조 narrative 과열

Stage 4C:
관세, 통관, UFLPA 억류, 보조금 축소, worker furlough
```

## `WASTE_RECYCLING_ENVIRONMENT`

```text
Stage 1:
폐기물처리 M&A, 규제 강화, 재활용 수요 뉴스

Stage 2:
처리량, 장기계약, 가동률, FCF 확인

Stage 3:
허가권·처리시설·반복 FCF가 valuation frame을 바꿀 때

Stage 4B:
M&A 프리미엄 과열

Stage 4C:
가동률 하락, CAPEX 부담, 금속가격 하락
```

## `CARBON_CREDIT_CBAM_COMPLIANCE`

```text
Stage 1:
EU ETS·CBAM 제도 변화 뉴스

Stage 2:
탄소회계·검증·저탄소 제품 premium 매출 확인

Stage 3:
반복 규제 대응 매출과 비용 전가력 확인

Stage 4B:
탄소가격 테마 과열

Stage 4C:
탄소가격 급락, free allowance 확대, greenwashing 논란
```

---

# 10. 가격경로 검증계획

## R3 공통 검증 방식

```text
1. 각 case의 stage1_date, stage2_date, stage3_date를 지정한다.
2. 해당 날짜의 종가를 stage_price로 저장한다.
3. MFE_30D / 90D / 180D / 1Y / 2Y를 계산한다.
4. MAE_30D / 90D / 180D / 1Y를 계산한다.
5. peak_price와 drawdown_after_peak를 계산한다.
6. OP/EPS revision, 가동률, CAPEX, FCF, 광물가격, 보조금/관세 이벤트와 가격 경로를 비교한다.
```

## R3에서 반드시 분리할 판정

```text
aligned:
계약·가동률·마진·FCF가 확인된 뒤 주가가 리레이팅.

cyclical_success:
광물가격·에너지 가격·정책 덕분에 수익은 났지만 구조적 Green은 아님.

event_premium:
보조금, 정책, 착공, MOU, 공장 뉴스로 주가만 오른 경우.

false_positive_score:
성장 테마 점수는 높았지만 EV 수요·CAPA·마진이 안 따라옴.

thesis_break:
공장 idle, worker furlough, 통관 억류, impairment, 광물가격 급락.
```

## 이번 R3에서 우선 검증할 가격 case

| case_id                                  | stage2 후보일 | 현재 1차 가격판정                           |
| ---------------------------------------- | ---------: | ------------------------------------ |
| `lg_energy_solution_ess_shift_case`      | 2025-07-25 | 발표 후 -1.6%, mixed watch              |
| `gm_lg_ultium_ohio_ev_slowdown_case`     | 2026-05-12 | EV demand 4C + ESS watch             |
| `hyundai_hydrogen_fuel_cell_plant_case`  | 2025-10-30 | Stage 1~2 후보, 가격 backfill 필요         |
| `qcells_customs_detention_case`          | 2025-11-08 | solar supply chain 4C                |
| `orsted_sunrise_wind_impairment_case`    | 2025-01-20 | wind project 4C                      |
| `eqt_kj_environment_waste_platform_case` | 2024-08-16 | 폐기물 Green reference, 상장 매핑 필요        |
| `eu_ets_cbam_policy_case`                | 2026-05-12 | policy watch, 직접 매출 확인 필요            |
| `lithium_price_86pct_crash_case`         | 2025-01-13 | lithium cycle 4C                     |
| `albemarle_cost_cut_low_lithium_case`    | 2025-02-12 | after-hours +2.5%, cost-cut survival |
| `qcells_china_linked_solar_policy_case`  | 2026-05-08 | solar policy/supply-chain risk       |

---

# 11. 다음에 에이전트가 채워야 할 price fields

R3 case library에는 아래 필드가 필요하다.

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

ev_demand_indicator
ess_contract_value
capacity_utilization
capex_amount
capex_to_revenue
fcf_margin
op_margin_change
eps_revision_1q
eps_revision_1y

lithium_price_change
nickel_price_change
raw_material_price_change
solar_tariff_event
customs_detention_flag
subsidy_change_flag
plant_idle_flag
furlough_layoff_flag
project_impairment_flag

recycling_volume
metal_recovery_revenue
waste_treatment_volume
carbon_credit_price
cbam_exposure

score_price_alignment
price_validation_status
```

---

# R3 결론

R3는 “미래 성장산업”처럼 보이지만, 점수정규화에서는 가장 보수적으로 봐야 하는 라운드 중 하나다.

```text
Green 가능:
폐기물처리
일부 ESS 전환
일부 수소 CAPEX
탄소회계·CBAM compliance 반복매출

Watch:
2차전지 장비·부품
폐배터리
EV 충전 인프라
수소 인프라
풍력
탄소배출권

Red/4C 방어 중심:
2차전지 소재 과열
EV CAPA 과잉
전고체 테마
태양광 관세·통관 리스크
리튬 가격 cycle
풍력 impairment
EV 화재·리콜·규제
```

**R3 점수정규화의 핵심 문장:**

> 2차전지·전기차·친환경은 “성장 테마”가 아니라 **가동률, 계약, 가격전가, 보조금 의존도, CAPEX 부담, FCF 전환**으로 봐야 한다.
> 실제 FCF가 확인되기 전까지 대부분은 Green이 아니라 Watch이며, EV 수요 둔화·광물가격 하락·통관 리스크·프로젝트 impairment는 즉시 4C 후보가 된다.

다음에 네가 “다음 라운드 진행해줘”라고 하면, 정해둔 순서에 따라 **R4 — 소재·스프레드·전략자원**으로 넘어간다.

[1]: https://www.reuters.com/business/autos-transportation/lg-energy-solution-warns-slowing-ev-battery-demand-due-us-tariffs-policy-2025-07-25/?utm_source=chatgpt.com "LG Energy Solution warns of slowing EV battery demand due to U.S. tariffs, policy headwinds"
[2]: https://www.reuters.com/legal/litigation/gms-restart-date-ohio-battery-plant-uncertain-2026-05-12/?utm_source=chatgpt.com "GM-LG's restart date at Ohio battery plant uncertain"
[3]: https://www.reuters.com/world/asia-pacific/hyundai-motor-breaks-ground-680-million-hydrogen-fuel-cell-plant-south-korea-2025-10-30/?utm_source=chatgpt.com "Hyundai Motor breaks ground on $680 million hydrogen fuel cell plant in South Korea"
[4]: https://www.reuters.com/markets/deals/eqt-strikes-deal-acquire-south-korean-waste-treatment-platform-2024-08-16/?utm_source=chatgpt.com "EQT strikes deal to acquire South Korean waste treatment platform"
[5]: https://www.reuters.com/sustainability/climate-energy/eu-carbon-trading-revamp-boost-revenue-return-industry-commissioner-says-2026-05-12/?utm_source=chatgpt.com "EU carbon trading revamp to boost revenue return to industry, commissioner says"
[6]: https://arxiv.org/abs/2601.05490?utm_source=chatgpt.com "How Carbon Border Adjustment Mechanism is Energizing the EU Carbon Market and Industrial Transformation"
[7]: https://apnews.com/article/f49d0579e0584d689f1feec36ff16ad1?utm_source=chatgpt.com "South Korean solar firm cuts pay and hours for Georgia workers as US officials detain imports"
[8]: https://www.reuters.com/legal/litigation/trumps-crackdown-china-linked-solar-firms-stalls-us-factory-boom-2026-05-08/?utm_source=chatgpt.com "Trump's crackdown on China-linked solar firms stalls U.S. factory boom"
[9]: https://www.reuters.com/business/energy/orsted-flags-impairments-about-17-billion-us-rate-increases-2025-01-20/?utm_source=chatgpt.com "Orsted flags $1.7 bln impairment on Sunrise Wind delays, increased costs"
[10]: https://www.reuters.com/markets/commodities/lithium-prices-stabilise-2025-mine-closures-china-ev-sales-ease-glut-analysts-2025-01-13/?utm_source=chatgpt.com "Lithium prices to stabilise in 2025 as mine closures, China EV sales ease glut, analysts say"
[11]: https://www.reuters.com/markets/commodities/albemarle-swings-quarterly-profit-cost-cuts-offset-lithium-price-drop-2025-02-12/?utm_source=chatgpt.com "Cost cuts help Albemarle's results offset low lithium prices"
[12]: https://www.reuters.com/sustainability/climate-energy/qcells-furloughs-1000-workers-us-solar-factories-due-stalled-shipments-2025-11-08/?utm_source=chatgpt.com "Qcells furloughs 1,000 workers at US solar factories due to stalled shipments"
