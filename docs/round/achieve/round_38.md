좋아. **Round 32: 이미 했던 주요 archetype 재검증 + 얇은 archetype 점수비중 v2.3 + 가격경로 검증계획 강화**로 갈게.

이번부터는 케이스마다 단순히 “성공 후보 / 반례”만 붙이지 않고, **가격경로 1차 판정**도 같이 붙인다. 아직 에이전트가 실제 OHLCV로 MFE/MAE를 계산한 건 아니지만, 공개 보도에서 확인되는 주가 반응·시총 변화·급락 이벤트를 이용해서 “이 archetype의 점수비중이 맞는 방향인지” 1차로 점검한다.

기본 원칙은 그대로다.

> 테마명은 점수 근거가 아니다.
> 점수는 **산업 구조 변화 → EPS/FCF 체급 변화 → 시장의 과거 프레임 오해 → 밸류에이션 리레이팅**에서 나와야 한다.
> 계약금액, 계약기간, 매출 대비 계약금액, OP YoY 같은 값은 실제 공시·리포트에서 확인된 것만 써야 하고, 없는 숫자를 만들어 넣으면 안 된다.

---

# Round 32에서 더 파는 축

```text
1. AI_SERVER_ODM_EMS_SUPPLY_CHAIN
   AI 서버 ODM/EMS, Foxconn, Wiwynn, Quanta, Supermicro류

2. AI_SERVER_ACCOUNTING_GOVERNANCE_RISK
   AI 서버 고성장주 안의 회계·감사·내부통제 4C

3. NEOCLOUD_GPU_RENTAL
   CoreWeave, GPU cloud, take-or-pay contract, 고부채 AI 인프라

4. ADVANCED_PACKAGING_COWOS_EMIB
   CoWoS, EMIB, HBM 패키징, AI packaging bottleneck

5. SEMI_EQUIPMENT_AI_CAPEX
   Applied Materials류 장비, AI fab/packaging CAPEX

6. POWER_SEMICONDUCTOR_SIC
   SiC, 전력반도체, Wolfspeed, EV·태양광·산업용 전력소자

7. OPTICAL_NETWORKING_AI_DATACENTER 재보정
   광통신·광케이블·AI 데이터센터 네트워크

8. REDTEAM_ACCOUNTING_TRUST_OVERLAY
   모든 고성장 archetype에 얹는 hard 4C overlay
```

---

# 1. AI_SERVER_ODM_EMS_SUPPLY_CHAIN

## AI 서버 ODM/EMS / Foxconn / Wiwynn / Supermicro류

### 핵심 구조

```text
AI GPU/ASIC 수요
→ AI 서버·랙·네트워킹 장비 조립 수요
→ hyperscaler / Nvidia / ASIC 고객사 수주
→ 대량 생산능력·공급망·마진 관리
→ OP/EPS 상향
```

이 archetype은 `AI_DATA_CENTER_INFRASTRUCTURE`의 하위축이지만, 전력기기·HBM과 다르다. AI 서버 ODM/EMS는 수요는 강하지만 **마진이 낮고, 고객사 집중·부품 조달·회계 신뢰도·재고 리스크**가 크다.

## 성공 후보: Foxconn

Foxconn은 AI 서버 ODM/EMS의 성공 후보로 볼 수 있다. Reuters는 Foxconn이 2026년 1분기 순이익이 전년 대비 19% 증가해 예상을 웃돌았고, AI 제품 수요가 실적을 견인했으며, 올해 AI server rack shipments가 2배 이상 늘 것으로 예상한다고 보도했다. CEO는 AI를 장기 성장요인으로 언급했고, AI 서버 생산능력 확대를 위해 CAPEX도 늘릴 계획이라고 했다. 다만 같은 보도에서 Foxconn 주가는 연초 이후 6% 상승에 그쳐 대만 시장 전체 상승률보다 낮았다고 나와, **실적은 강하지만 주가 리레이팅은 아직 상대적으로 제한적**일 수 있음을 보여준다. ([Reuters][1])

## 반례: Supermicro

Supermicro는 AI 서버 archetype에서 반드시 넣어야 하는 반례다. AI 서버 수요로 2023년 초 약 44억 달러였던 시가총액이 2024년 3월 약 670억 달러까지 급등했지만, 이후 회계·내부통제·감사 리스크가 터졌다. Reuters는 Ernst & Young이 Supermicro의 감사인에서 사임하자 주가가 30% 이상 급락했고, 감사인이 경영진과 감사위원회의 진술을 더 이상 신뢰할 수 없다고 밝혔다고 보도했다. ([Reuters][2])

### 점수비중 v2.3

```text
EPS/FCF: 22
Structural Visibility: 19
Bottleneck/Pricing: 16
Market Mispricing: 14
Valuation Rerating: 11
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: customer_concentration / low_margin_assembly / inventory / accounting_trust / supplier_related_party
```

### 정규화 교정

```text
점수 강화:
- AI server rack shipment 증가
- hyperscaler/Nvidia/ASIC 고객사 수요
- 생산능력 확장
- OP/EPS 상향
- 공급망 관리능력
- 고객사 다변화

점수 제한:
- 단순 AI 서버 테마
- 매출은 크지만 마진 낮음
- 고객사 집중
- 재고 증가
- 관련자 거래·회계·감사 리스크
- auditor resignation / filing delay
```

### 가격경로 1차 판정

```text
Foxconn:
실적 evidence는 강함.
다만 주가가 시장 대비 크게 압도했다는 증거는 아직 약함.
→ success_candidate, price_alignment = needs_backfill

Supermicro:
AI 서버 수요로 큰 리레이팅은 있었지만, 감사인 사임 후 급락.
→ early_rerating_success + hard_4c_thesis_break
```

### 주가검증 계획

```text
Stage 1:
AI server demand, Nvidia/ASIC 고객 수요, rack shipment 성장 뉴스

Stage 2:
분기 실적에서 AI server revenue/OP 증가 확인일

Stage 3:
AI server mix가 회사 전체 EPS/FCF 체급을 바꾸고 valuation frame이 바뀐 날

검증지표:
MFE_90D / 180D / 1Y
MAE_90D / 180D
gross margin / OP margin
inventory growth
customer concentration
audit/internal-control event drawdown

성공:
AI server 매출과 OP/EPS, 주가 리레이팅이 같이 가면 aligned.

실패:
매출은 늘었지만 margin·재고·회계 신뢰도 문제로 주가가 붕괴하면 4C.
```

---

# 2. AI_SERVER_ACCOUNTING_GOVERNANCE_RISK

## AI 고성장주 회계·감사·내부통제 overlay

이건 별도 산업 archetype이라기보다, 모든 고성장 AI 하드웨어/서버/인프라에 얹어야 하는 **hard RedTeam overlay**야.

### 핵심 구조

```text
AI 수요 급증
→ 매출 폭증
→ 시장이 숫자를 빠르게 믿음
→ 내부통제·감사·관련자거래 문제가 나오면 thesis break
```

Supermicro는 이 overlay의 기준 반례다. AP도 EY 사임 후 Supermicro 주가가 33% 급락했다고 보도했고, EY가 회사의 투명성·내부통제·경영진 윤리성에 의문을 제기했다고 설명했다. ([AP News][3])

### Overlay 규칙

```text
hard 4C 조건:
- 감사인 사임
- 감사보고서 지연
- 내부통제 중대 결함
- 관련자거래 의혹
- SEC/DOJ 조사
- 재무제표 재작성 가능성
- 주요 고객/공급업체와 가족·내부자 관계 의혹
```

### 점수 적용 방식

```text
이 overlay는 점수비중이 아니라 gate다.

회계/감사 hard flag 발생 시:
- Stage 3-Green 금지
- 기존 Stage 3도 RedTeam review
- score_price_alignment = thesis_break_pending
- price_validation 우선순위 최상위
```

### 주가검증 계획

```text
검증일:
감사인 사임일, 연차보고서 지연일, 공매도 리포트 발행일, 규제기관 조사 보도일

검증지표:
event_day_return
MFE/MAE 5D / 20D / 60D
drawdown_from_peak
회복 여부
재무제표 정상 제출 여부

성공:
회계 이슈가 해소되고 재무제표 신뢰가 회복되면 watch로 복귀 가능.

실패:
감사인 사임·조사·delisting risk로 장기 drawdown이면 hard_4c 확정.
```

---

# 3. NEOCLOUD_GPU_RENTAL

## CoreWeave / GPU cloud / take-or-pay / 고부채 AI 인프라

### 핵심 구조

```text
AI 모델 학습·추론 수요
→ Nvidia GPU cloud 임대
→ take-or-pay 장기계약
→ 높은 EBITDA 가능성
→ 단, GPU 담보부채·고객집중·감가상각·금리 리스크
```

Neocloud는 AI 인프라에서 아주 중요한 신규 archetype이지만, Green을 쉽게 주면 위험하다. 고객 수요는 강해도 자본구조가 너무 무겁다.

### 성공 후보: CoreWeave take-or-pay

Reuters Breakingviews는 CoreWeave 같은 neocloud 업체들이 AI compute 수요로 빠르게 커졌고, CoreWeave 계약의 96%가 다년간 고정 지급을 보장하는 committed 또는 take-or-pay 구조라고 설명했다. 이는 고객에게 일부 수요위험을 넘기고, CoreWeave가 GPU 인프라를 빠르게 배치할 수 있게 해주는 구조적 visibility다. ([Reuters][4])

### 반례: 부채·고객집중·IPO 가격경로

CoreWeave는 IPO에서 기대가보다 낮은 40달러에 가격이 책정됐고, Microsoft가 2024년 매출의 62%를 차지했으며, 2024년 매출 19억 달러에 순손실 8.63억 달러, 부채 80억 달러 수준이었다고 Investopedia가 정리했다. 즉 수요는 크지만 **고부채·고객집중·GPU 감가상각·FCF 적자**가 강한 감점축이다. ([Investopedia][5])

Barron’s는 CoreWeave가 상장 후 40달러에서 65달러까지 올랐다가 관세 뉴스 속 33.52달러까지 내려갔고, 고부채와 고객집중이 핵심 리스크라고 분석했다. 이는 가격경로가 이미 **high beta / high leverage / high drawdown** 구조라는 걸 보여준다. ([Barron's][6])

### 점수비중 v2.3

```text
EPS/FCF: 18
Structural Visibility: 21
Bottleneck/Pricing: 18
Market Mispricing: 14
Valuation Rerating: 10
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: debt / customer_concentration / GPU_obsolescence / funding_cost / FCF_negative
```

### 정규화 교정

```text
점수 강화:
- take-or-pay 장기계약
- OpenAI/Microsoft/대형 고객 계약
- GPU deployment 속도
- EBITDA margin
- 고객 다변화
- debt cost 하락

점수 제한:
- 매출은 급증하지만 FCF 적자
- Microsoft/Nvidia/OpenAI 집중
- GPU 담보부채
- GPU 세대교체 리스크
- IPO 이후 큰 변동성
```

### 가격경로 1차 판정

```text
CoreWeave:
수요·계약 구조는 강하지만, IPO 가격이 기대보다 낮고 상장 후 큰 변동성.
→ success_candidate가 아니라 high_risk_watch_candidate
```

### 주가검증 계획

```text
Stage 1:
대형 AI cloud 계약, OpenAI/Microsoft 계약, IPO filing

Stage 2:
take-or-pay backlog, revenue growth, EBITDA improvement 확인일

Stage 3:
FCF 전환 또는 debt/EBITDA 안정화가 확인될 때만

검증지표:
IPO price 대비 90D/180D/1Y MFE/MAE
net debt / EBITDA
FCF margin
customer concentration
contract duration
GPU depreciation cycle
refinancing cost

성공:
매출·EBITDA·FCF 전환이 같이 가고 고객 다변화가 일어나면 aligned.

실패:
주가는 올랐지만 debt/FCF/customer concentration이 악화되면 false_positive_score.
```

---

# 4. ADVANCED_PACKAGING_COWOS_EMIB

## CoWoS / EMIB / HBM 패키징 / AI packaging bottleneck

### 핵심 구조

```text
AI accelerator + HBM
→ advanced packaging 필요
→ CoWoS / CoWoS-L / EMIB / 2.5D packaging 병목
→ 장비·소재·기판·패키징 CAPEX 증가
```

### 성공 후보: Nvidia CoWoS-L 변화

Reuters는 Nvidia CEO Jensen Huang이 Nvidia의 advanced packaging 수요가 감소하는 게 아니라 변화하고 있으며, Blackwell이 CoWoS-L을 사용하고 CoWoS-S와 CoWoS-L 모두 수요가 있다고 설명했다고 보도했다. 또한 packaging constraint가 지난 2년간 완화됐지만 여전히 병목이라고 했다. 이건 advanced packaging이 AI 공급망의 독립 병목임을 보여준다. ([Reuters][7])

### 성공 후보: Applied Materials

Applied Materials는 AI spending과 advanced packaging 수요의 직접 수혜 후보로 볼 수 있다. Reuters는 Applied Materials가 2026년 3분기 매출 전망을 시장 예상보다 높게 제시했고, 반도체 장비는 30% 이상, packaging revenue는 50% 이상 성장할 것으로 전망했다고 보도했다. 주가도 실적 발표 후 시간외에서 3% 상승했다. ([Reuters][8])

### 반례: 공급 병목 완화와 CAPEX cycle

Broadcom은 TSMC capacity bottleneck뿐 아니라 lasers와 PCB lead time 증가도 언급했지만, 신규 진입과 capacity expansion이 eventually solution이 될 수 있다고 봤다. 즉 병목은 강하지만 **CAPA 확장 후 병목 완화**가 4B/4C 조건이 될 수 있다. ([Reuters][9])

### 점수비중 v2.3

```text
EPS/FCF: 22
Structural Visibility: 21
Bottleneck/Pricing: 20
Market Mispricing: 14
Valuation Rerating: 12
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: capex_cycle / customer_concentration / bottleneck_normalization / yield_risk
```

### 정규화 교정

```text
점수 강화:
- CoWoS/EMIB/HBM packaging 수요
- 고객사 CAPEX 확정
- 장비·소재·기판 수주 증가
- packaging revenue growth
- OP/EPS 상향

점수 제한:
- 패키징 테마만 있음
- 고객사 수주 불명확
- CAPA 증설로 병목 완화
- yield 문제
- CAPEX peak risk
```

### 주가검증 계획

```text
Stage 1:
Nvidia/AMD/Broadcom packaging bottleneck 언급일

Stage 2:
장비·소재·기판 업체 수주 또는 packaging revenue 상향 확인일

Stage 3:
다년 packaging bottleneck + EPS 상향 + valuation frame 전환 확인일

검증지표:
packaging revenue growth
bookings/backlog
gross margin
MFE_180D / 1Y
CAPEX cycle peak 이후 drawdown
```

---

# 5. SEMI_EQUIPMENT_AI_CAPEX

## Applied Materials / Lam / KLA / Tokyo Electron류 장비

### 핵심 구조

```text
AI fab·HBM·advanced packaging CAPEX
→ 장비 수주
→ backlog / shipment
→ OP leverage
→ 단, 고객사 CAPEX cycle에 종속
```

Applied Materials 사례는 이 archetype을 계속 Green 가능 쪽으로 두게 해준다. 단, 장비주는 HBM 생산업체보다 고객 CAPEX cycle에 더 민감하다.

### 점수비중 v2.3

```text
EPS/FCF: 22
Structural Visibility: 20
Bottleneck/Pricing: 18
Market Mispricing: 14
Valuation Rerating: 12
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: customer_capex / order_delay / export_control / capex_peak
```

### 정규화 교정

```text
점수 강화:
- 고객사 AI/HBM fab CAPEX
- 장비 backlog 증가
- packaging / advanced node exposure
- 매출·EPS 상향
- 고객사 다변화

점수 제한:
- 장비 테마만 있음
- 고객사 CAPEX 지연
- 수출통제
- order push-out
- CAPEX peak 이후 둔화
```

### 주가검증 계획

```text
Stage 1:
고객사 CAPEX 발표, AI fab/packaging 투자 뉴스

Stage 2:
장비사 수주·가이던스 상향 확인일

Stage 3:
backlog가 매출·OP로 전환되고 valuation frame이 바뀐 시점

검증지표:
orders/backlog
revenue guidance
EPS revision
MFE_180D / 1Y
MAE after order slowdown
```

---

# 6. POWER_SEMICONDUCTOR_SIC

## SiC / 전력반도체 / Wolfspeed / EV·태양광·산업용 전력소자

### 핵심 구조

```text
EV·태양광·산업용 전력효율 수요
→ SiC wafer/device CAPEX
→ 장기적으로 유망
→ 단, EV 수요 둔화·고부채·CAPEX 부담이 치명적
```

### 반례: Wolfspeed

Wolfspeed는 이 archetype에서 가장 중요한 반례 중 하나다. Reuters는 Wolfspeed가 2025년 Chapter 11에서 벗어나며 총부채를 약 70% 줄이고 연간 현금 이자비용을 60% 줄였다고 보도했다. 하지만 그 전에는 무역정책 불확실성과 수요 약화로 파산보호를 신청했었다. ([Reuters][10])

또 Reuters는 Jana Partners가 Wolfspeed 지분을 청산했고, Wolfspeed 주식이 5년 동안 약 92% 하락했으며 파산 가능성을 검토 중이었다고 보도했다. 이는 **SiC 장기 성장 narrative가 있어도 CAPEX·수요·부채가 틀리면 주가 경로가 완전히 무너진다**는 강한 반례다. ([Reuters][11])

### 점수비중 v2.3

```text
EPS/FCF: 16
Structural Visibility: 13
Bottleneck/Pricing: 12
Market Mispricing: 11
Valuation Rerating: 8
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: EV_demand / capex_debt / utilization / pricing / bankruptcy
```

### 정규화 교정

```text
점수 강화:
- 실제 장기공급계약
- 가동률 상승
- 낮은 부채
- EV 외 산업·태양광 고객 다변화
- FCF 개선

점수 제한:
- SiC 테마만 있음
- EV 수요 둔화
- CAPEX 과잉
- 고부채
- 가동률 낮음
- 파산/구조조정 위험
```

### 가격경로 1차 판정

```text
Wolfspeed:
장기 성장 테마였지만 주가 5년 -90%대, Chapter 11.
→ structural_failure / hard_counterexample
```

### 주가검증 계획

```text
Stage 1:
SiC 수요·EV/태양광 성장 narrative

Stage 2:
장기공급계약, fab ramp-up, 매출 증가 확인일

Stage 3:
FCF 개선과 부채 안정이 확인된 경우만

검증지표:
MFE/MAE 1Y/2Y
debt/EBITDA
capex/revenue
utilization
gross margin
cash burn
drawdown after demand warning

성공:
수요·가동률·FCF가 같이 개선되면 Watch-to-Green.

실패:
CAPEX와 부채가 먼저 커지고 수요가 둔화되면 4C.
```

---

# 7. OPTICAL_NETWORKING_AI_DATACENTER 재보정

## 광섬유 / 광케이블 / AI 데이터센터 네트워크

Broadcom은 TSMC capacity뿐 아니라 lasers와 optical transceiver PCB lead time 증가를 언급했다. AI 데이터센터 병목이 GPU·HBM에서 광통신·PCB·레이저로 퍼지는 구조라서 이 archetype은 Green 가능 하위축으로 유지한다. 다만 Broadcom은 장기적으로 신규 진입과 CAPA 확대로 병목이 완화될 수 있다고도 봤으므로, 4B-watch도 필요하다. ([Reuters][9])

### 점수비중 v2.3

```text
EPS/FCF: 21
Structural Visibility: 22
Bottleneck/Pricing: 20
Market Mispricing: 13
Valuation Rerating: 12
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: hyperscaler_concentration / valuation_crowding / capacity_normalization / capex_delay
```

### 가격검증 계획

```text
Stage 1:
AI optical/laser/PCB bottleneck 언급

Stage 2:
실제 hyperscaler 계약·lead time·수주 evidence

Stage 3:
OP/EPS 상향과 장기계약 확인

검증:
수주 후 MFE_180D/1Y
lead time 정상화 후 drawdown
valuation crowding
고객사 concentration
```

---

# 8. REDTEAM_ACCOUNTING_TRUST_OVERLAY 재보정

Supermicro 사례 때문에 이 overlay는 모든 고성장 AI 하드웨어/인프라/서버에 강하게 적용해야 한다.

```text
Hard RedTeam:
- auditor resignation
- annual report delay
- internal control weakness
- DOJ/SEC probe
- related-party transaction issue
- repeated past accounting violation
```

Supermicro는 AI 서버 수요로 고성장했지만, 감사인 사임 후 30% 이상 급락했다. 이는 “성장률이 아무리 좋아도 회계 신뢰도가 깨지면 Stage 3를 유지하면 안 된다”는 명확한 기준이다. ([Reuters][2])

### 적용 방식

```text
이 overlay는 점수비중이 아니라 gate다.

발생 시:
- Stage 3-Green 즉시 금지
- RedTeam hard finding
- score_price_alignment 재검토
- price path 5D/20D/60D 우선 계산
```

---

# Round 32 점수비중 요약표

| Archetype                | EPS/FCF | Visibility | Bottleneck | Mispricing | Valuation | Capital | 핵심 리스크             |
| ------------------------ | ------: | ---------: | ---------: | ---------: | --------: | ------: | ------------------ |
| AI_SERVER_ODM_EMS        |      22 |         19 |         16 |         14 |        11 |       0 | 저마진, 고객집중, 회계      |
| NEOCLOUD_GPU_RENTAL      |      18 |         21 |         18 |         14 |        10 |       0 | 고부채, GPU 감가상각      |
| ADVANCED_PACKAGING_COWOS |      22 |         21 |         20 |         14 |        12 |       0 | CAPEX cycle, 병목 완화 |
| SEMI_EQUIPMENT_AI_CAPEX  |      22 |         20 |         18 |         14 |        12 |       0 | 고객 CAPEX, 수출통제     |
| POWER_SEMICONDUCTOR_SIC  |      16 |         13 |         12 |         11 |         8 |       0 | EV 수요, 부채, 파산      |
| OPTICAL_NETWORKING_AI_DC |      21 |         22 |         20 |         13 |        12 |       0 | 고객집중, 과열           |
| ACCOUNTING_TRUST_OVERLAY |    gate |       gate |       gate |       gate |      gate |    gate | hard 4C            |

---

# cases_v20 추가 후보

```text
AI_SERVER_ODM_EMS_SUPPLY_CHAIN:
- foxconn_ai_server_profit_rack_growth_candidate
- foxconn_ai_server_price_alignment_needs_backfill
- supermicro_ai_server_rerating_then_accounting_4c
- ai_server_low_margin_customer_concentration_counterexample

AI_SERVER_ACCOUNTING_GOVERNANCE_RISK:
- supermicro_ey_resignation_hard_4c
- supermicro_hindenburg_delay_annual_report_4c
- related_party_supplier_risk_counterexample
- auditor_resignation_redteam_overlay

NEOCLOUD_GPU_RENTAL:
- coreweave_take_or_pay_contract_candidate
- coreweave_ipo_below_range_price_path_watch
- coreweave_high_debt_customer_concentration_counterexample
- gpu_obsolescence_funding_cost_4c

ADVANCED_PACKAGING_COWOS_EMIB:
- nvidia_cowos_l_packaging_bottleneck_candidate
- applied_materials_packaging_growth_candidate
- packaging_bottleneck_normalization_4b
- customer_capex_delay_packaging_4c

SEMI_EQUIPMENT_AI_CAPEX:
- applied_materials_ai_capex_guidance_candidate
- equipment_order_backlog_success_candidate
- capex_peak_equipment_4c
- export_control_equipment_counterexample

POWER_SEMICONDUCTOR_SIC:
- wolfspeed_chapter11_restructuring_4c
- wolfspeed_stock_92pct_decline_counterexample
- sic_low_utilization_counterexample
- sic_long_term_contract_success_candidate_if_fcf

OPTICAL_NETWORKING_AI_DATACENTER:
- broadcom_optical_pcb_leadtime_bottleneck_candidate
- optical_networking_capacity_normalization_4b
- optical_hyperscaler_customer_concentration_counterexample
- optical_theme_no_order_counterexample
```

---

# 이번 라운드 핵심 교정

```text
1. AI 서버 ODM/EMS는 Green 가능하지만 HBM/전력기기보다 마진·회계·고객집중 리스크가 크다.

2. Supermicro는 AI 서버 success case가 아니라,
   “AI 수요로 리레이팅된 뒤 회계 신뢰도 4C로 무너진 반례”로 넣어야 한다.

3. Neocloud/CoreWeave는 take-or-pay 계약 때문에 visibility는 높지만,
   debt, FCF 적자, GPU 감가상각, 고객집중 때문에 Green은 아직 제한.

4. Advanced packaging은 AI 공급망 병목으로 Green 가능성이 있지만,
   CAPA 확장 후 병목 완화가 4B/4C 조건이다.

5. 반도체 장비는 AI CAPEX 수혜지만 고객사 CAPEX cycle에 종속된다.

6. SiC 전력반도체는 장기 성장 narrative만으로 Green을 주면 안 된다.
   Wolfspeed가 핵심 반례다.

7. 광통신/optical networking은 AI 데이터센터 병목이지만,
   고객사 집중과 valuation crowding을 감시해야 한다.

8. 회계·감사·내부통제 이슈는 모든 고성장 AI 관련주에 hard RedTeam gate로 얹어야 한다.
```

---

# Archetype별 가격경로 검증 업데이트

## 1. 고성장 AI 하드웨어형

대상:

```text
AI_SERVER_ODM_EMS
ADVANCED_PACKAGING_COWOS
SEMI_EQUIPMENT_AI_CAPEX
OPTICAL_NETWORKING_AI_DC
AI_DATA_CENTER_COOLING
MEMORY_HBM_CAPACITY
```

검증:

```text
Stage 1:
AI 수요·고객사 CAPEX·병목 뉴스

Stage 2:
수주·매출·가이던스·OP/EPS 상향 확인

Stage 3:
다년 visibility + valuation frame 변화 확인

필수 가격지표:
MFE_90D / 180D / 1Y
MAE_90D / 180D
drawdown_after_peak
valuation multiple expansion
EPS revision 지속성
margin trend

성공:
매출·OP/EPS·주가가 같이 리레이팅.

실패:
매출은 늘었지만 마진·재고·회계·고객집중 이슈로 주가가 무너짐.
```

---

## 2. 고부채 인프라형

대상:

```text
NEOCLOUD_GPU_RENTAL
DATA_CENTER_REIT_INFRA
COLD_CHAIN_REIT_LOGISTICS
AI_GRID_FLEXIBILITY_SW
```

검증:

```text
핵심 가격지표:
debt/EBITDA
interest expense
FCF margin
contract duration
tenant/customer concentration
MFE_180D / 1Y
drawdown_after_refinancing_or_capex_news

성공:
장기계약과 FCF 전환이 주가와 동행.

실패:
매출은 늘지만 부채·CAPEX·금리로 주가가 눌림.
```

---

## 3. 사이클·과열형

대상:

```text
POWER_SEMICONDUCTOR_SIC
LITHIUM_BATTERY_RAW_MATERIAL
CHEMICAL_SPREAD
SHIPPING_FREIGHT_CYCLE
AGRI_LIVESTOCK_FOOD_COMMODITY
```

검증:

```text
핵심 가격지표:
commodity price peak
EPS peak
drawdown_after_peak
capex/revenue
debt/cash runway
MFE_90D / 180D

성공:
cyclical_success로 분류.
structural_success로 오분류 금지.

실패:
가격 상승 또는 테마를 구조적 리레이팅으로 오판.
```

---

# 현재 판단

이제 점수비중 지도는 **v2.3**까지 왔다.
특히 이번 라운드에서 중요한 건, “AI 인프라” 안에서도 다음을 분리했다는 점이야.

```text
HBM:
구조적 Green 가능성이 높음.

AI server ODM/EMS:
수요는 강하지만 마진·회계·고객집중 리스크 큼.

Neocloud:
계약 visibility는 있지만 고부채·GPU 감가상각 리스크 큼.

Advanced packaging:
병목은 강하지만 CAPEX cycle과 병목 완화 리스크 있음.

SiC:
장기 narrative는 강하지만 Wolfspeed처럼 실패 가능성이 큼.
```

이제부터는 계속 이렇게 해야 한다.

```text
성공/반례 추가
→ 각 case stage date 후보 설정
→ 실제 가격 path backfill
→ MFE/MAE/drawdown 계산
→ score-price alignment 확인
→ 틀린 점수비중 재교정
```

여기까지 오면 에이전트가 단순 테마에 끌려가는 게 아니라, **성공처럼 보이는 테마 안에서도 진짜 구조적 E2R과 false-positive를 가르는 방향**으로 점점 가까워진다.

[1]: https://www.reuters.com/world/china/taiwans-foxconn-reports-185-rise-q1-profit-beats-forecast-2026-05-14/?utm_source=chatgpt.com "Foxconn reports forecast-beating 19% jump in Q1 profit on AI demand"
[2]: https://www.reuters.com/technology/super-micro-computer-says-ernst-young-resigns-its-accountant-shares-tank-2024-10-30/?utm_source=chatgpt.com "Super Micro Computer says Ernst & Young resigns as auditor, shares tank"
[3]: https://apnews.com/article/d1cc4377628b3024e659dcfec9318dcd?utm_source=chatgpt.com "Super Micro Computer's shares plunge 33% after server maker's accounting firm quits"
[4]: https://www.reuters.com/commentary/breakingviews/neoclouds-fine-print-is-silver-lining-sorts-2025-10-22/?utm_source=chatgpt.com "Neoclouds' fine print is a silver lining of sorts"
[5]: https://www.investopedia.com/nvidia-backed-coreweave-prices-its-ipo-at-usd40-per-share-below-expectations-11701963?utm_source=chatgpt.com "Nvidia-Backed CoreWeave Prices Its IPO at $40 Per Share, Below Expectations"
[6]: https://www.barrons.com/articles/coreweave-stock-price-buy-ratings-31598085?utm_source=chatgpt.com "CoreWeave Stock Gets a Wave of Buy Ratings. But No One Is Denying the Risk."
[7]: https://www.reuters.com/technology/nvidia-ceo-says-its-advanced-packaging-technology-needs-are-changing-2025-01-16/?utm_source=chatgpt.com "Nvidia CEO says its advanced packaging technology needs are changing"
[8]: https://www.reuters.com/business/applied-materials-sees-quarterly-revenue-above-estimates-2026-05-14/?utm_source=chatgpt.com "Applied Materials sees quarterly revenue above estimates on sustained AI spending"
[9]: https://www.reuters.com/world/asia-pacific/broadcom-flags-supply-constraints-says-tsmc-capacity-bottleneck-2026-03-24/?utm_source=chatgpt.com "Broadcom flags supply constraints, says TSMC capacity a bottleneck"
[10]: https://www.reuters.com/business/wolfspeed-exits-chapter-11-bankruptcy-slashes-debt-interest-costs-2025-09-29/?utm_source=chatgpt.com "Wolfspeed exits Chapter 11 bankruptcy, slashes debt and interest costs"
[11]: https://www.reuters.com/sustainability/sustainable-finance-reporting/jana-partners-liquidated-position-wolfspeed-q1-filing-2025-05-15/?utm_source=chatgpt.com "Jana Partners liquidated position in Wolfspeed in Q1, filing"
