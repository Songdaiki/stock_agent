좋아. **Round 20: 주요·얇은 archetype 동시 보강 + 점수비중 v1.1 교정**으로 계속 채울게.

이번 라운드도 원칙은 그대로야.

> **테마명은 점수 근거가 아니다.**
> 테마명은 검색·분류·쿼리 생성용 tag이고, 점수는 실제 공시·리포트·뉴스·재무·가격 evidence에서만 나온다. 서생원식 핵심도 “산업 구조 변화 → EPS/FCF 체급 변화 → 시장의 과거 프레임 오해 → 밸류에이션 리레이팅”이야.
> 계약금액, 계약기간, 매출 대비 계약금액, OP YoY 같은 필드는 실제 상세공시나 리포트에서 확인될 때만 써야 하고, 없는 값은 만들면 안 된다.

이번에는 아래 10개를 더 파고들었다.

```text
1. AI_DATA_CENTER_COOLING
2. MEMORY_HBM_CAPACITY
3. K_BEAUTY_EXPORT_DISTRIBUTION / BEAUTY_OEM_ODM
4. DIGITAL_ASSET_TOKENIZATION / PAYMENT_FINTECH
5. SOLAR_TARIFF_SUPPLYCHAIN / HYDROGEN_FUEL_CELL
6. CLOUD_AI_SOFTWARE_INFRA
7. SECURITY_IDENTITY_DEEPFAKE
8. CRO_CLINICAL_SERVICE
9. CONSTRUCTION_REAL_ESTATE_CREDIT / BUILDING_MATERIALS
10. INSURANCE_UNDERWRITING / SECURITIES_BROKERAGE
```

---

# 1. AI_DATA_CENTER_COOLING

## AI 데이터센터 냉각 / HVAC / 액침냉각

### 구조

```text
AI 서버 고밀도화
→ 발열·전력 밀도 상승
→ 액체냉각 / HVAC / 열관리 병목
→ 데이터센터 CAPEX와 동행
→ 수주·납품·서비스 매출
```

### 성공사례 후보

Ecolab의 CoolIT 인수는 이 archetype을 독립적으로 둘 근거가 된다. Ecolab은 CoolIT Systems를 약 47.5억 달러에 인수하기로 했고, CoolIT은 Nvidia·AMD 같은 칩메이커에 액체냉각 시스템을 공급하는 업체로 보도됐다. 이건 “냉각 테마”가 아니라 **AI 데이터센터의 고밀도 전력·열 부하를 해결하는 병목 공급자**라는 구조에 가깝다. ([Reuters][1])

Samsung의 FlaktGroup 인수도 같은 방향의 보조 사례야. Samsung은 독일 HVAC 업체 FlaktGroup을 15억 유로에 인수해 AI 데이터센터용 냉각 역량을 강화하려 했다. 다만 시장 반응은 제한적이었고, 이게 반도체 본업 리레이팅과는 별개라는 점도 같이 봐야 한다. ([Reuters][2])

### 반례

```text
- 액침냉각 키워드만 있고 실제 고객·납품 없음
- 일반 HVAC 매출뿐이고 AI 데이터센터 exposure가 작음
- 수주는 있으나 저마진 설비 납품에 그침
- AI CAPEX 지연 또는 데이터센터 프로젝트 지연
- 고객사 집중도가 너무 높음
```

### 점수비중 v1.1

```text
EPS/FCF: 21
Structural Visibility: 22
Bottleneck/Pricing: 22
Market Mispricing: 13
Valuation Rerating: 12
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: AI_CAPEX_delay / low_margin_project / customer_concentration
```

### 정규화 교정

AI 냉각은 **Green 가능 archetype**으로 올릴 수 있다.
다만 Green 조건은 까다롭게 둬야 한다.

```text
Green 조건:
- 고객사 데이터센터 CAPEX와 직접 연결
- 실제 수주/납품
- 냉각 기술 병목 지위
- 서비스·모니터링·유지보수 반복매출
- FY1/FY2 OP 상향

Green 금지:
- 액침냉각 테마명만 있음
- AI 데이터센터 관련주로 묶였지만 매출 exposure 불명확
- 일반 설비업체인데 narrative만 AI로 바뀜
```

---

# 2. MEMORY_HBM_CAPACITY

## HBM / 메모리 / AI 서버 병목

### 구조

```text
AI 수요
→ HBM/DRAM/NAND 병목
→ 장기계약·선수금·가격밴드
→ EPS/FCF 다년 상향
→ 과거 메모리 시클리컬 할인 제거
```

### 성공사례 후보

SK하이닉스는 이 archetype의 대표 성공사례다. Reuters는 AI 수요와 HBM 중요성으로 SK하이닉스 주가가 2025년에 274%, 2026년에 200% 이상 상승했고, 시총이 1조 달러에 근접했다고 보도했다. 이건 단순 메모리 업황 회복이 아니라, **메모리 = AI 인프라 병목**이라는 시장 프레임 전환을 보여준다. ([Reuters][3])

### 반례

```text
- 단순 DRAM/NAND 가격 반등
- HBM과 무관한 범용 메모리 회복
- 고객사 장기계약/선수금/price band 없음
- CAPEX 증설로 공급과잉 전환
- AI CAPEX 둔화
```

### 점수비중 v1.1

```text
EPS/FCF: 24
Structural Visibility: 21
Bottleneck/Pricing: 19
Market Mispricing: 15
Valuation Rerating: 12
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: cycle / capex_reversal / crowding / customer_price_resistance
```

### 4B 보정

HBM은 Green 가능성이 높지만, 성공 후에는 4B-watch가 반드시 필요하다.

```text
4B-watch 조건:
- 주가 1~2년 급등
- 시총/멀티플 포화
- 모두가 AI memory rerating 인정
- 고객사 가격 저항
- 경쟁사 CAPEX 증설 뉴스
- 글로벌 자금 crowded
```

### 정규화 교정

```text
점수 강화:
HBM 수요, 공급규율, 장기계약, 선수금, 중장기 EPS revision

점수 제한:
단순 spot price 상승, short-cycle DRAM rebound, price-only rally
```

---

# 3. K_BEAUTY_EXPORT_DISTRIBUTION / BEAUTY_OEM_ODM_SUPPLYCHAIN

## K뷰티 브랜드 / 화장품 OEM·ODM / 원재료·부자재

### 구조

```text
K뷰티 글로벌 수요
→ 미국·일본·글로벌 채널 확장
→ 브랜드·고객사 다변화
→ 반복 주문
→ OPM/ROE 개선
→ 중국 의존 화장품 프레임 탈피
```

### 성공사례 후보

Reuters는 2024년에 한국이 미국 화장품 수출에서 프랑스를 앞섰고, K뷰티 브랜드들이 Sephora, Target, Costco 같은 미국 오프라인 채널 진입을 추진한다고 보도했다. 이건 K뷰티가 단순 viral ecommerce에서 **오프라인·대형 리테일 채널로 확장될 수 있는 구조**를 보여준다. ([Reuters][4])

### 반례

```text
- 중국 의존 화장품
- TikTok viral-only 브랜드
- sell-through 없이 출하만 늘어난 channel stuffing
- 재고 증가
- 매출채권 증가
- 미국 tariff / 인증 / 규제 리스크
- 브랜드 난립으로 ASP 하락
```

### 점수비중 v1.1

```text
EPS/FCF: 22
Structural Visibility: 23
Bottleneck/Pricing: 12
Market Mispricing: 16
Valuation Rerating: 13
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: inventory / receivables / China_dependency / tariff / channel_stuffing
```

### 정규화 교정

K뷰티는 Green 가능성이 있다.
하지만 Green은 아래 조건이 같이 있어야 한다.

```text
Green 조건:
- 미국·일본·글로벌 수출 증가
- 고객사/브랜드 다변화
- 반복 주문
- OPM/ROE 개선
- 재고·채권 리스크 낮음
- 중국 의존도 하락
```

```text
Green 금지:
- viral 키워드만 있음
- 출하 증가만 있고 sell-through 불명확
- 재고/매출채권 악화
```

---

# 4. DIGITAL_ASSET_TOKENIZATION / PAYMENT_FINTECH_INFRA

## 스테이블코인 / STO / 결제서비스 / 토스 / 신용정보

### 구조

```text
규제 승인
→ 실제 발행·거래량·결제망 채택
→ 수수료·예치금·스프레드 수익
→ 반복 금융 인프라 매출
```

### 성공사례 후보

Toss는 글로벌 확장과 원화 스테이블코인 발행 의지를 밝힌 대표 후보지만, 아직 규제 승인과 실제 발행·수익모델이 확인되어야 한다. Reuters는 Toss가 호주 진출과 원화 스테이블코인 발행을 목표로 하고 있으며, 관련 입법이 준비 중이라고 보도했다. ([Reuters][5])

스테이블코인은 구조적 잠재력은 있지만, 금융시장 구조와 규제에 강하게 묶인다. 2025년 연구는 Tether의 미국 T-bill 보유가 단기금리에 영향을 줄 정도의 규모가 됐다고 분석했다. 이건 stablecoin이 금융 인프라로 커질 수 있음을 보여주지만, 동시에 발행·준비금·규제·유동성 리스크가 매우 중요하다는 뜻이기도 하다. ([arXiv][6])

### 반례

```text
- 코인 테마만 있는 기업
- STO 법제화 기대만 있고 실제 발행 없음
- 스테이블코인 규제 지연
- 거래량 부진
- 보안사고
- 수익모델 부재
- NFT/메타버스 식 price-only rally
```

### 점수비중 v1.1

```text
EPS/FCF: 16
Structural Visibility: 18
Bottleneck/Pricing: 8
Market Mispricing: 16
Valuation Rerating: 12
Capital Allocation: 3
Information Confidence: 5
Risk Penalty: regulation / security / adoption / liquidity / no_revenue
```

### 정규화 교정

디지털금융은 아직 **Watch 중심**이다.

```text
Stage 1:
법안, 사업 진출, 제휴, 상장 기대

Stage 2:
실제 라이선스, 발행, 거래량, 수수료 모델

Stage 3:
결제/수탁/정산 인프라로 고착
규제 리스크 낮음
반복매출과 FCF 확인
```

```text
Green 금지:
규제 기대만 있음
관련주로 묶였지만 실질 지분/매출 없음
거래량·수익모델 없음
```

---

# 5. SOLAR_TARIFF_SUPPLYCHAIN / HYDROGEN_FUEL_CELL_INFRA

## 태양광 / 수소 / 풍력 / 탄소배출권

### 구조

```text
정책·보조금·CAPEX
→ 실제 수주·생산·가동률
→ OP/EPS 전환
```

### 성공사례 후보

Hyundai는 울산에 약 6.5억 달러 규모의 수소연료전지 생산시설을 착공했고, 이 시설은 승용차·상용차·건설기계·선박 등에 쓰일 연료전지와 전해조를 생산할 계획이다. 이건 수소 테마 중에서도 **실제 CAPEX와 생산능력**이 있는 Stage 1~2 후보로 볼 수 있다. ([Reuters][7])

### 반례

Qcells/Hanwha Solutions는 태양광 supply-chain risk의 좋은 반례다. AP는 Qcells가 미국 세관의 부품 억류로 조지아 공장 직원 약 1,000명의 근무시간과 임금을 줄이고 300명의 계약직을 해고했다고 보도했다. 정책 수혜와 미국 생산시설이 있어도 **관세·통관·공급망 리스크**가 가동률과 FCF를 훼손할 수 있다. ([AP News][8])

### 점수비중 v1.1

```text
EPS/FCF: 18
Structural Visibility: 18
Bottleneck/Pricing: 12
Market Mispricing: 12
Valuation Rerating: 10
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: policy / subsidy / tariff / customs / supply_chain / utilization
```

### 정규화 교정

```text
Green 조건:
- 실제 CAPEX
- 생산능력/가동률
- 고객사·정부 수요
- OP/EPS 전환
- 보조금·관세 리스크 낮음
```

```text
Green 금지:
- 수소/태양광/풍력 정책 키워드만 있음
- 보조금 의존
- 통관·관세·부품 공급망 리스크
- 프로젝트 지연
```

---

# 6. CLOUD_AI_SOFTWARE_INFRA

## 클라우드 / ERP / B2B SaaS / 컨택센터

### 구조

```text
반복 소프트웨어 매출
→ 고객 lock-in
→ ARPU / OPM 개선
→ FCF 개선
```

### 성공사례 후보

Douzone Bizon은 국내 B2B 소프트웨어 기준 케이스로 볼 수 있다. Reuters는 EQT가 더존비즈온 지분 37.6%를 약 9.3억 달러에 인수하기로 했고, 더존비즈온이 중소기업 대상 클라우드 ERP·회계·세무·컴플라이언스 소프트웨어를 제공한다고 설명했다. 이건 **반복 B2B 소프트웨어 매출 + 고객 lock-in + 운영 개선 가능성**을 보는 Stage 1~2 사례다. ([Reuters][9])

### 반례

```text
- AI 기능만 추가하고 매출화 없음
- 클라우드 비용 증가로 OPM 하락
- 고객 이탈 / churn 상승
- SI성 매출만 있고 SaaS 전환 없음
- 컨택센터·원격근무 테마만 있음
```

### 점수비중 v1.1

```text
EPS/FCF: 20
Structural Visibility: 23
Bottleneck/Pricing: 8
Market Mispricing: 16
Valuation Rerating: 14
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: AI_cost / churn / margin / SI_revenue_mix
```

### 정규화 교정

클라우드/SaaS는 Green 가능성이 있다.
하지만 AI 키워드가 아니라 아래가 핵심이다.

```text
Green 조건:
- 반복매출 증가
- ARPU 상승
- 고객 retention
- OPM 개선
- FCF conversion
- AI 비용 통제
```

---

# 7. SECURITY_IDENTITY_DEEPFAKE

## IT보안 / 딥페이크 / 생체인식 / CCTV

### 구조

```text
보안 위협 증가 / 규제 강화
→ 기업·정부 보안 지출
→ 반복 구독 또는 장기계약
→ ARR·OPM·FCF 개선
```

### 성공사례 후보

보안은 구조적 수요가 있다. 딥페이크·생체인식·CCTV는 규제와 공공/기업 도입이 붙으면 Stage 1~2 후보가 될 수 있다.

### 강한 반례

CrowdStrike는 이 archetype에서 반드시 넣어야 하는 4C 반례다. Reuters는 CrowdStrike의 잘못된 소프트웨어 업데이트가 800만 대 이상의 컴퓨터에 영향을 주었고, 주가가 12일간 32% 하락해 약 250억 달러의 시가총액이 사라졌다고 보도했다. 반복매출이 있어도 **운영 신뢰도·장애·소송 리스크**가 깨지면 바로 thesis break가 된다. ([Reuters][10])

### 점수비중 v1.1

```text
EPS/FCF: 20
Structural Visibility: 20
Bottleneck/Pricing: 10
Market Mispricing: 14
Valuation Rerating: 13
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: operational_trust / outage / legal / customer_retention
```

### 정규화 교정

```text
Green 조건:
- 반복 구독 매출
- 낮은 churn
- 고객 다변화
- OPM 개선
- 대형 장애·소송 리스크 부재
```

```text
4C 조건:
- 대형 장애
- 고객 소송
- 보안 신뢰 훼손
- 갱신율 하락
```

---

# 8. CRO_CLINICAL_SERVICE

## CRO / 임상시험수탁 / 임상서비스

### 구조

```text
제약·바이오 R&D 증가
→ 임상시험 수탁
→ 반복 서비스 매출
→ 고객사 다변화
→ OP/FCF 개선
```

### 반례

Charles River Laboratories는 CRO/바이오서비스 반례로 중요하다. Reuters는 Charles River가 바이오 고객사의 funding crunch가 지속되면서 2024년 전망을 낮췄고, 이 소식에 주가가 premarket에서 15% 하락했다고 보도했다. 즉 CRO는 반복 서비스처럼 보여도 **바이오 funding cycle과 고객사 R&D 예산**이 꺾이면 4C로 가야 한다. ([Reuters][11])

### 점수비중 v1.1

```text
EPS/FCF: 18
Structural Visibility: 20
Bottleneck/Pricing: 8
Market Mispricing: 12
Valuation Rerating: 12
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: biotech_funding_cycle / customer_concentration / backlog_quality
```

### 정규화 교정

```text
CRO Green 조건:
- 수주잔고 증가
- 고객사 다변화
- 매출/OP 증가
- R&D funding cycle 안정
- 고마진 서비스 mix
```

CDMO보다 약하고, pre-revenue biotech보다 강한 중간형 archetype이다.

---

# 9. CONSTRUCTION_REAL_ESTATE_CREDIT / BUILDING_MATERIALS_CYCLE

## 건설 / PF / 건자재 / 시멘트 / 철근 / 리츠

### 구조

```text
수주보다 PF·미분양·원가율·현금흐름이 먼저
```

### 강한 반례

한국 부동산 PF 연체율은 2021년 말 0.37%에서 2023년 말 2.70%로 상승했고, 금융당국은 프로젝트 구조조정 강화를 발표했다. 이건 건설·건자재·리츠 archetype에서 **PF·미분양·신용위험을 hard RedTeam 조건으로 넣어야 한다**는 근거다. ([Reuters][12])

### 점수비중 v1.1

```text
EPS/FCF: 17
Structural Visibility: 12
Bottleneck/Pricing: 12
Market Mispricing: 12
Valuation Rerating: 12
Capital Allocation: 5
Information Confidence: 5
Risk Penalty: credit / rates / vacancy / PF / unsold_inventory
```

### 정규화 교정

```text
Green 조건:
- 원가 안정
- 가격인상 성공
- 출하량 회복
- PF 리스크 낮음
- 배당 안정 또는 FCF 개선
```

```text
Green 금지:
- 수주만 증가
- PF/미분양 리스크 존재
- 정부·은행 지원에 의존한 relief rally
```

건설·건자재는 Watch 중심. PF 리스크가 있으면 바로 RedTeam 우선이다.

---

# 10. INSURANCE_UNDERWRITING / SECURITIES_BROKERAGE

## 보험 / 증권 / 금융 value-up

### 보험 구조

```text
손해율 안정
→ CSM / ROE 개선
→ 자본비율 안정
→ 주주환원
→ PBR-ROE 프레임 리레이팅
```

### 증권 구조

```text
거래대금 증가
→ 브로커리지 수수료 증가
→ IPO/IB 회복
→ 자기자본 운용성과
→ ROE 개선
```

### 점수비중 v1.1 — 보험

```text
EPS/FCF: 15
Structural Visibility: 21
Bottleneck/Pricing: 4
Market Mispricing: 15
Valuation Rerating: 25
Capital Allocation: 10
Information Confidence: 5
Risk Penalty: underwriting / capital_ratio / cyber_operational / credit_cost
```

### 점수비중 v1.1 — 증권

```text
EPS/FCF: 18
Structural Visibility: 14
Bottleneck/Pricing: 5
Market Mispricing: 15
Valuation Rerating: 18
Capital Allocation: 8
Information Confidence: 5
Risk Penalty: market_turnover / PF / proprietary_loss / IPO_cycle
```

### 정규화 교정

```text
보험:
Green 가능. ROE/CSM/자본비율/환원정책 중심.

증권:
Watch 중심. 거래대금·IB cycle 성격이 강해 Green은 제한.
```

---

# Round 20 점수비중 요약표

| Archetype                  | EPS/FCF | Visibility | Bottleneck | Mispricing | Valuation | Capital | 성격                   |
| -------------------------- | ------: | ---------: | ---------: | ---------: | --------: | ------: | -------------------- |
| AI_DATA_CENTER_COOLING     |      21 |         22 |         22 |         13 |        12 |       0 | Green 가능, 수주·고객 필수   |
| MEMORY_HBM_CAPACITY        |      24 |         21 |         19 |         15 |        12 |       0 | Green 가능 + 4B 감시     |
| K_BEAUTY / OEM_ODM         |      22 |         23 |         12 |         16 |        13 |       0 | Green 가능, 재고·채권 감시   |
| DIGITAL_ASSET_TOKENIZATION |      16 |         18 |          8 |         16 |        12 |       3 | Watch, 규제·거래량 필요     |
| HYDROGEN / SOLAR           |      18 |         18 |         12 |         12 |        10 |       0 | Watch, 정책 리스크 큼      |
| CLOUD_AI_SOFTWARE_INFRA    |      20 |         23 |          8 |         16 |        14 |       0 | Green 가능, 반복매출 핵심    |
| SECURITY_IDENTITY          |      20 |         20 |         10 |         14 |        13 |       0 | Green 가능, 장애는 4C     |
| CRO_CLINICAL_SERVICE       |      18 |         20 |          8 |         12 |        12 |       0 | Watch-to-Green       |
| BUILDING_MATERIALS / REIT  |      17 |         12 |         12 |         12 |        12 |       5 | Watch, PF·금리 리스크     |
| INSURANCE_UNDERWRITING     |      15 |         21 |          4 |         15 |        25 |      10 | Green 가능, ROE/PBR/환원 |
| SECURITIES_BROKERAGE       |      18 |         14 |          5 |         15 |        18 |       8 | Watch, 거래대금 cycle    |

---

# cases_v08 추가 후보

```text
AI_DATA_CENTER_COOLING:
- ecolab_coolit_ai_liquid_cooling_candidate
- samsung_flaktgroup_hvac_candidate
- liquid_cooling_theme_no_order_counterexample
- ai_capex_delay_cooling_4c

MEMORY_HBM_CAPACITY:
- sk_hynix_hbm_success_case
- sk_hynix_4b_crowding_watch
- simple_dram_rebound_counterexample
- ai_capex_cut_memory_4c

K_BEAUTY_EXPORT_DISTRIBUTION:
- kbeauty_us_offline_channel_candidate
- kbeauty_oem_odm_customer_diversification_candidate
- china_dependency_cosmetic_counterexample
- channel_stuffing_inventory_receivables_4c

DIGITAL_ASSET_TOKENIZATION:
- toss_won_stablecoin_candidate
- stablecoin_regulatory_delay_4c
- sto_law_expectation_without_revenue_counterexample
- crypto_theme_no_revenue_counterexample

HYDROGEN_RENEWABLE:
- hyundai_hydrogen_fuel_cell_plant_candidate
- qcells_customs_detention_4c
- hydrogen_theme_no_revenue_counterexample
- solar_subsidy_dependency_counterexample

CLOUD_AI_SOFTWARE_INFRA:
- douzone_bizon_cloud_erp_candidate
- ai_feature_no_fcf_counterexample
- cloud_cost_margin_pressure_4c
- saas_churn_counterexample

SECURITY_IDENTITY_DEEPFAKE:
- recurring_security_subscription_candidate
- crowdstrike_outage_4c
- deepfake_regulation_stage1_candidate
- security_theme_no_contract_counterexample

CRO_CLINICAL_SERVICE:
- cro_revenue_backlog_candidate
- charles_river_funding_crunch_4c
- biotech_customer_budget_cut_counterexample
- cro_customer_diversification_success_candidate

CONSTRUCTION_BUILDING_MATERIALS:
- pf_delinquency_4c
- building_materials_price_hike_candidate
- reit_rate_cut_dividend_candidate
- builder_liquidity_support_relief_rally_counterexample

INSURANCE_SECURITIES:
- insurer_underwriting_valueup_candidate
- low_pbr_insurer_no_capital_return_counterexample
- brokerage_trading_value_rally_candidate
- securities_pf_loss_4c
```

---

# 이번 라운드 핵심 교정

```text
1. AI 냉각은 Green 가능하지만, 실제 수주·고객·서비스 매출이 필수.
2. HBM은 Green 가능성이 높지만, 성공 후 4B-watch를 강하게 켜야 함.
3. K뷰티는 Green 가능하지만, 재고·채권·중국 의존·channel stuffing은 hard risk.
4. 스테이블코인/STO는 아직 Watch. 규제·거래량·수익모델 전까지 Green 금지.
5. 수소/태양광은 정책 테마가 아니라 실제 CAPEX·가동률·OP 전환을 봐야 함.
6. 클라우드/SaaS는 Green 가능하지만, AI 키워드보다 반복매출·OPM·FCF가 핵심.
7. 보안은 Green 가능하지만, CrowdStrike형 장애는 즉시 4C.
8. CRO는 CDMO보다 약하고 pre-revenue biotech보다 강한 중간형.
9. 건설·건자재·리츠는 PF·금리·미분양 리스크 때문에 Watch 중심.
10. 보험은 Green 가능, 증권은 거래대금 cycle 때문에 Watch 중심.
```

---

# 현재 판단

이제 대부분의 주요·얇은 archetype에 대해 **점수비중 가설 v1.1**까지 쌓였다.
하지만 아직 최종 적용은 아니야.

다음 필수 단계는 변하지 않는다.

```text
1. cases_v08 반영
2. 각 case의 stage date 후보 설정
3. price path backfill
4. MFE/MAE/drawdown 계산
5. shadow scoring
6. score-price alignment 확인
7. 틀린 archetype 재교정
```

지금 우리가 하는 작업은 “점수비중의 지도”를 만드는 것이고, 다음부터는 그 지도가 실제 시장 가격 경로와 맞는지 검증해야 한다.

[1]: https://www.reuters.com/business/ecolab-acquire-coolit-systems-475-billion-2026-03-20/?utm_source=chatgpt.com "Ecolab to buy CoolIT for $4.75 billion to tap into AI data center boom"
[2]: https://www.reuters.com/markets/deals/samsung-electronics-buy-flktgroup-15-bln-euro-2025-05-13/?utm_source=chatgpt.com "Samsung to buy German cooling system maker FlaktGroup for $1.7 billion"
[3]: https://www.reuters.com/world/asia-pacific/ai-boom-puts-sk-hynix-cusp-1-trillion-market-value-2026-05-14/?utm_source=chatgpt.com "AI boom puts SK Hynix on cusp of $1 trillion market value"
[4]: https://www.reuters.com/world/asia-pacific/korean-beauty-startups-bet-booming-us-demand-outlasts-tariff-pain-2025-06-05/?utm_source=chatgpt.com "Korean beauty startups bet booming US demand outlasts tariff pain"
[5]: https://www.reuters.com/business/finance/south-korean-fintech-toss-plans-global-push-starting-australia-aims-issue-won-2025-09-09/?utm_source=chatgpt.com "South Korean fintech Toss plans global push starting in Australia, aims to issue won stablecoin"
[6]: https://arxiv.org/abs/2505.12413?utm_source=chatgpt.com "The Stablecoin Discount: Evidence of Tether's U.S. Treasury Bill Market Share in Lowering Yields"
[7]: https://www.reuters.com/world/asia-pacific/hyundai-motor-breaks-ground-680-million-hydrogen-fuel-cell-plant-south-korea-2025-10-30/?utm_source=chatgpt.com "Hyundai Motor breaks ground on $680 million hydrogen fuel cell plant in South Korea"
[8]: https://apnews.com/article/f49d0579e0584d689f1feec36ff16ad1?utm_source=chatgpt.com "South Korean solar firm cuts pay and hours for Georgia workers as US officials detain imports"
[9]: https://www.reuters.com/world/asia-pacific/swedish-firm-eqt-shells-out-930-million-slice-south-koreas-douzone-bizon-2025-11-07/?utm_source=chatgpt.com "Swedish firm EQT shells out $930 million for a slice of South Korea's Douzone Bizon"
[10]: https://www.reuters.com/legal/crowdstrike-is-sued-by-shareholders-over-huge-software-outage-2024-07-31/?utm_source=chatgpt.com "CrowdStrike is sued by shareholders over huge software outage"
[11]: https://www.reuters.com/business/healthcare-pharmaceuticals/charles-river-cuts-2024-forecast-funding-crunch-among-biotech-clients-persists-2024-08-07/?utm_source=chatgpt.com "Charles River cuts 2024 forecast as funding crunch among biotech clients persists"
[12]: https://www.reuters.com/markets/asia/south-korea-tightens-scrutiny-speed-up-real-estate-restructuring-2024-05-13/?utm_source=chatgpt.com "South Korea tightens scrutiny to speed up real estate restructuring"
