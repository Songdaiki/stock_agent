좋아. **Round 24: 주요·얇은 archetype 점수비중 v1.5 보강**으로 계속 채울게.

이번 라운드는 특히 아직 더 정교화가 필요했던 쪽을 판다.

```text
1. 반도체 장비·소재·패키징
2. 완성차·자동차 부품·타이어
3. 항공·여행·카지노·면세
4. 편의점·오프라인 유통
5. AI 인프라 Korea CAPEX 확산
6. 증권·거래대금 cycle 보정
7. 농축산·식품 원가 cycle 보정
8. 스페이스X·우주항공 테마 보정
```

기본 원칙은 그대로다.
에이전트는 테마봇이 아니라 **산업 구조 변화 → EPS/FCF 체급 변화 → 시장의 과거 프레임 오해 → 밸류에이션 리레이팅**을 찾는 시스템이어야 한다.
또 계약금액, 계약기간, 매출 대비 계약금액, OP YoY 같은 필드는 실제 상세공시나 리포트에서 확인될 때만 써야 하고, 없는 값을 추정해서 넣으면 안 된다.

---

# 1. SEMI_EQUIPMENT_CAPEX / SEMI_MATERIALS_PROCESS / ADVANCED_PACKAGING_PCB

## 반도체 장비·소재·후공정·PCB

### 핵심 구조

```text
AI/HBM 고객사 CAPEX
→ 장비·소재·패키징·PCB 수주
→ 납품·매출 인식
→ OP leverage
→ 단, 고객사 CAPEX cycle에 취약
```

### 성공사례 후보

SK하이닉스의 ASML EUV 대규모 주문은 반도체 장비·소재·공정 archetype의 상위 수요 확인 신호야. Reuters는 SK하이닉스가 2027년 말까지 ASML EUV 장비 약 11.95조원, 80억 달러 규모를 구매한다고 보도했고, 이 장비가 HBM과 advanced DRAM 생산을 지원한다고 설명했다. 이건 단순 반도체 테마가 아니라 **HBM/advanced DRAM CAPEX가 실제 장비 발주로 연결되는 사례**다. ([Reuters][1])

Nvidia가 한국 정부·삼성·SK·현대차·네이버 등에 Blackwell AI 칩 26만 개 이상을 공급하기로 한 것도 AI 인프라 수요가 반도체·서버·스마트팩토리·데이터센터로 확산되는 Stage 1~2 신호다. 다만 이건 바로 모든 관련주 Green이 아니라, 실제 수주·납품·매출 exposure가 확인된 기업만 점수가 올라가야 한다. ([Reuters][2])

### 반례

```text
- HBM/AI 키워드만 있고 고객사 수주 없음
- 고객사 CAPEX 지연
- 단일 고객 의존
- 장비 수주 후 납품 지연
- 국산화 테마만 있고 실제 매출화 없음
- PCB/소재 재고 증가
```

### 점수비중 v1.5

```text
EPS/FCF: 22
Structural Visibility: 20
Bottleneck/Pricing: 18
Market Mispricing: 14
Valuation Rerating: 12
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: customer_capex / customer_concentration / inventory / order_delay
```

### 정규화 교정

반도체 장비·PCB·소재는 **Watch-to-Green**이다.

```text
점수 강화:
- 고객사 CAPEX 확정
- 수주잔고 증가
- HBM/advanced packaging 직접 노출
- 납품 스케줄
- OP/EPS 상향
- 고객사 다변화

점수 제한:
- AI/HBM 관련주로만 묶임
- 실질 매출 exposure 없음
- 단일 고객 과의존
- CAPEX peak 우려
```

**핵심:**
HBM 자체는 Green 가능성이 높지만, 장비·소재·PCB는 고객사 CAPEX에 종속된다. 그래서 HBM보다 `structural_visibility`는 낮추고, `customer_capex risk`를 더 강하게 둬야 한다.

---

# 2. AUTO_MOBILITY_COMPLETED_VEHICLE / AUTO_MOBILITY_COMPONENTS

## 완성차·자동차 부품·전장·경량화

### 핵심 구조

```text
제품 mix 개선 / 하이브리드 대응 / 수출 / 환율
→ OP/FCF 안정
→ 주주환원
→ 저평가 프레임 해소
```

### 성공사례 후보

현대차는 이 archetype에서 단순 자동차 cycle이 아니라 **하이브리드 전환 + 판매 목표 + 주주환원 + 밸류 할인 해소**를 같이 보는 케이스야. Reuters는 현대차가 2030년 글로벌 판매 555만 대, 2023년 대비 30% 증가를 목표로 하고, 하이브리드 라인업을 두 배로 늘리며, 2025~2027년 최대 4조원 자사주 매입과 배당 확대를 발표했다고 보도했다. ([Reuters][3])

### 반례

```text
- EV 수요 둔화 부품주
- 완성차 판매는 좋은데 부품사 원가전가 실패
- 단일 고객 의존 부품주
- 관세·정책 리스크
- 리콜·품질 비용
- 원재료 상승으로 타이어/부품 마진 훼손
```

### 점수비중 v1.5 — 완성차

```text
EPS/FCF: 20
Structural Visibility: 18
Bottleneck/Pricing: 10
Market Mispricing: 15
Valuation Rerating: 17
Capital Allocation: 10
Information Confidence: 5
Risk Penalty: tariff / demand_slowdown / recall / peak_margin
```

### 점수비중 v1.5 — 부품·전장·타이어

```text
EPS/FCF: 20
Structural Visibility: 17
Bottleneck/Pricing: 10
Market Mispricing: 14
Valuation Rerating: 14
Capital Allocation: 3
Information Confidence: 5
Risk Penalty: raw_material / customer_concentration / EV_cycle / quality_cost
```

### 정규화 교정

```text
완성차:
Green 가능성이 있다.
특히 ROE/FCF와 자사주·배당이 붙으면 value-up 성격도 강해진다.

부품주:
Watch-to-Green.
고객 다변화와 원가전가가 없으면 Green 제한.

타이어:
원재료 spread와 RE/OE mix가 핵심.
완성차 판매 호조만으로 점수 높이면 안 됨.
```

**핵심:**
완성차는 `capital_allocation` 비중이 꽤 높아야 한다. 반면 부품주는 `customer_concentration`과 `raw material risk`가 강한 감점축이다.

---

# 3. AIRLINE_TRAVEL_CYCLE / TRAVEL_LEISURE_REOPENING

## 항공·여행·리오프닝

### 핵심 구조

```text
여객 회복 / 항공사 통합 / 화물 mix
→ fixed cost leverage
→ OP 개선
→ 단, 유가·환율·관세·경기 리스크 큼
```

### 성공사례 후보

Korean Air는 항공 archetype에서 성공후보와 반례 성격을 동시에 가진다. Reuters는 대한항공이 2024년 연간 매출 16조원, 영업이익 2조원을 기록했고, 아시아나 인수 완료 후 아시아 최대급 항공사 중 하나가 됐다고 보도했다. 동시에 2025년에는 글로벌 정치 변화와 미국의 중국 상품 관세 등 불확실성을 언급했다. ([Reuters][4])

대한항공-아시아나 인수 완료는 항공업에서 네트워크·노선·LCC 통합·규모의 경제가 생길 수 있는 구조적 후보지만, 통합비용·경쟁당국 조건·노선 조정·화물/여객 mix 리스크를 같이 봐야 한다. ([Reuters][5])

### 반례

```text
- 리오프닝 기대만 있고 OP 개선 없음
- 유가 상승
- 환율 악화
- 여객 회복 peak-out
- 화물운임 정상화
- 인수 통합비용 증가
- 중국/미국 노선 수요 둔화
```

### 점수비중 v1.5

```text
EPS/FCF: 18
Structural Visibility: 14
Bottleneck/Pricing: 5
Market Mispricing: 12
Valuation Rerating: 10
Capital Allocation: 2
Information Confidence: 5
Risk Penalty: oil_price / FX / demand_cycle / integration_cost / tariff
```

### 정규화 교정

항공·여행은 **Watch 중심**이다.

```text
점수 강화:
- 여객·화물 회복이 OP로 연결
- 통합 시너지 확인
- 비용 안정
- FCF 개선

점수 제한:
- 리오프닝 기대만 있음
- 유가/환율 악화
- CAPEX·통합비용 부담
- 화물/여객 수요 둔화
```

**핵심:**
항공은 주가가 크게 움직여도 대부분 cycle이다. Stage 3-Green은 매우 제한하고, `cycle cap`을 둬야 한다.

---

# 4. CASINO_DUTYFREE_TOURISM

## 카지노·면세점·호텔·중국 관광

### 핵심 구조

```text
중국/일본 관광객 회복
→ 면세·카지노·호텔 매출 증가
→ 고정비 레버리지
→ OP 개선
→ 단, 정책·관광객 mix·중국 의존 리스크 큼
```

### 성공사례 후보

한국의 중국 단체관광객 무비자 정책은 면세·호텔·카지노·화장품·백화점 등 관광 관련주의 Stage 1 신호가 될 수 있다. Reuters는 한국이 2025년 9월 말부터 2026년 6월까지 중국 단체관광객에게 무비자 입국을 허용한다고 보도했고, 이 소식에 현대백화점·호텔신라·파라다이스·한국화장품 등 관광 관련주가 상승했다고 전했다. ([Reuters][6])

다만 이건 아직 Stage 1이다. 관광객 유입이 실제 drop amount, 객단가, 면세 매출, OP 개선으로 이어져야 Stage 2 이상이 된다.

### 반례

Inspire Resort 사례는 카지노·관광 인프라 반례로 볼 수 있다. FT는 한국의 16억 달러 규모 리조트/카지노 프로젝트가 기대보다 약한 관광 수요와 운영 문제, 정치 불안정 등으로 성장 covenant를 충족하지 못해 Bain이 지배권을 가져갔다고 보도했다. 이건 카지노·리조트가 CAPEX는 크지만 관광객 유입과 운영 성과가 안 나오면 4C로 간다는 사례다. ([Financial Times][7])

### 점수비중 v1.5

```text
EPS/FCF: 18
Structural Visibility: 13
Bottleneck/Pricing: 5
Market Mispricing: 12
Valuation Rerating: 10
Capital Allocation: 2
Information Confidence: 5
Risk Penalty: tourism_policy / China_dependency / capex / operating_leverage
```

### 정규화 교정

카지노·면세·호텔은 **Watch 중심**이다.

```text
점수 강화:
- 실제 관광객 증가
- 카지노 drop amount 증가
- 면세 객단가 회복
- OP 레버리지
- 중국 의존도 낮음

점수 제한:
- 무비자 정책 기대만 있음
- 중국 단체관광 의존
- CAPEX 부담
- 리조트/카지노 운영 성과 부진
```

**핵심:**
관광 테마는 Stage 1이 자주 뜬다. 하지만 Stage 3는 실제 OP 레버리지와 관광객 mix가 확인될 때만 가능하다.

---

# 5. RETAIL_CONVENIENCE_OFFLINE

## 편의점·오프라인 유통

### 핵심 구조

```text
점포망 / PB상품 / 객단가
→ same-store sales
→ OPM 개선
→ FCF 안정
```

### 성공후보

CU와 GS25는 편의점 archetype의 기준 케이스로 쓸 수 있다. CU는 2025년 기준 국내 18,000개 이상 점포와 해외 680개 이상 점포로 정리되고, GS25도 2024년 말 국내 18,112개 점포로 정리된다. 단, 점포 수 자체는 점수 근거가 아니고, **점포 효율·PB mix·해외 확장·OPM**을 봐야 한다. ([위키백과][8])

### 반례

```text
- 점포 수 증가하지만 점포당 수익성 하락
- 임대료·인건비 상승
- 편의점 경쟁 심화
- PB상품 mix 약화
- 소비 둔화
```

### 점수비중 v1.5

```text
EPS/FCF: 18
Structural Visibility: 16
Bottleneck/Pricing: 5
Market Mispricing: 13
Valuation Rerating: 14
Capital Allocation: 3
Information Confidence: 5
Risk Penalty: rent / wage / competition / same_store_sales_slowdown
```

### 정규화 교정

편의점은 **Watch-to-Green**이다.

```text
점수 강화:
- same-store sales 증가
- PB/고마진 mix 확대
- OPM 개선
- 해외 점포가 실제 수익화
- FCF 안정

점수 제한:
- 점포 수만 증가
- 임대료/인건비 상승
- 과밀 경쟁
```

**핵심:**
편의점은 방어적이지만 폭발적 E2R은 드물다. Green은 가능하지만 보수적으로.

---

# 6. SEMI_EQUIPMENT_CAPEX 재보정

## 반도체 장비·후공정·CXL·유리기판·PCB

### 성공과 반례를 나눠야 하는 이유

SK하이닉스의 EUV 장비 대형 주문처럼 고객사 CAPEX가 확인되면 장비·소재·후공정 생태계에 Stage 1~2 신호가 된다. 하지만 CXL, 유리기판, 뉴로모픽, 일부 AI칩 관련주는 실제 매출 전까지 테마성이 강하다. ([Reuters][1])

### 점수비중 v1.5

```text
EPS/FCF: 22
Structural Visibility: 20
Bottleneck/Pricing: 18
Market Mispricing: 14
Valuation Rerating: 12
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: customer_capex / adoption_delay / customer_concentration / inventory
```

### 정규화 교정

```text
Green 가능:
- 반도체 장비/소재가 실제 고객사 CAPEX에 연결
- 수주잔고 증가
- 납품 스케줄 확정
- OP/EPS 상향

Watch:
- CXL
- 유리기판
- 뉴로모픽
- AI칩 관련주
- 국산화 테마

Red:
- 실제 매출 없음
- 고객사 수주 없음
- price-only rally
```

---

# 7. AGRI_LIVESTOCK_FOOD_COMMODITY

## 양돈·육계·사료·대두·농기계·참치

### 핵심 구조

```text
곡물/사료/육류/어가 가격
→ 원가 또는 판가
→ 단기 OP 변화
→ 대부분 cycle/event
```

### 성공후보

```text
- 스마트팜/농기계 해외 수주
- 원양어업: 어가, 환율, 유가 개선
- 종자·농약·비료: 가격전가와 반복수요
```

### 반례

```text
- 조류독감/질병 이벤트
- 사료 원가 급등
- 대두 가격 상승
- 날씨 이벤트
- 판가전가 실패
```

### 점수비중 v1.5

```text
EPS/FCF: 18
Structural Visibility: 10
Bottleneck/Pricing: 14
Market Mispricing: 8
Valuation Rerating: 8
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: commodity_cycle / disease_event / feed_cost / weather
```

### 정규화 교정

농축산·사료는 대부분 **Red/Watch 중심**이다.

```text
Stage 2 가능:
- 판가전가
- 원가 안정
- 반복수요
- 실제 수주/해외확장

Green 제한:
- 질병 이벤트
- 가격 급등 테마
- 원가 변화만 있음
```

---

# 8. SPACE_SUPPLYCHAIN / URBAN_AIR_DRONE

## 스페이스X·드론·플라잉카·우주항공

### 핵심 구조

```text
우주/드론/항공 narrative
→ 실제 납품·계약·정부 수주
→ 반복 매출
→ 단, 대부분 테마성이 강함
```

### 성공후보

```text
- 실제 정부·방산·우주 부품 계약
- SpaceX 또는 위성통신 supply chain 납품 확인
- 드론 방산 수주
- 항공우주 부품 장기계약
```

### 반례

```text
- 스페이스X 관련주로 묶였지만 실제 매출 없음
- 드론·플라잉카 정책 테마
- 기술 PoC만 있고 양산 없음
- 규제·인증 지연
```

### 점수비중 v1.5

```text
EPS/FCF: 16
Structural Visibility: 14
Bottleneck/Pricing: 8
Market Mispricing: 12
Valuation Rerating: 10
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: no_contract / certification_delay / theme_overheat
```

### 정규화 교정

우주·드론은 대부분 **Watch/Red**다.

```text
Green 조건:
- 실제 납품계약
- 방산/정부 고객
- 반복 부품 매출
- 인증 완료
```

테마명만으로는 Green 금지.

---

# Round 24 점수비중 요약표

| Archetype              | EPS/FCF | Visibility | Bottleneck | Mispricing | Valuation | Capital | 핵심 리스크                   |
| ---------------------- | ------: | ---------: | ---------: | ---------: | --------: | ------: | ------------------------ |
| SEMI_EQUIPMENT_CAPEX   |      22 |         20 |         18 |         14 |        12 |       0 | 고객 CAPEX, 재고             |
| AUTO_COMPLETED_VEHICLE |      20 |         18 |         10 |         15 |        17 |      10 | 관세, peak margin          |
| AUTO_COMPONENTS/TIRE   |      20 |         17 |         10 |         14 |        14 |       3 | 원재료, 고객집중                |
| AIRLINE_TRAVEL_CYCLE   |      18 |         14 |          5 |         12 |        10 |       2 | 유가, 환율, 통합비용             |
| CASINO_DUTYFREE        |      18 |         13 |          5 |         12 |        10 |       2 | 중국 의존, CAPEX             |
| RETAIL_CONVENIENCE     |      18 |         16 |          5 |         13 |        14 |       3 | 임대료, 인건비                 |
| AGRI_LIVESTOCK         |      18 |         10 |         14 |          8 |         8 |       0 | 원가, 질병, 날씨               |
| SPACE_SUPPLYCHAIN      |      16 |         14 |          8 |         12 |        10 |       0 | 계약 없음, 테마 과열             |
| AI_DATA_CENTER_COOLING |      21 |         22 |         22 |         13 |        12 |       0 | CAPEX 지연                 |
| MEMORY_HBM             |      24 |         21 |         19 |         15 |        12 |       0 | crowding, CAPEX reversal |

---

# cases_v12 추가 후보

```text
SEMI_EQUIPMENT_CAPEX:
- sk_hynix_asml_euv_capex_success_signal
- hbm_equipment_order_backlog_candidate
- cxl_glass_substrate_no_revenue_counterexample
- customer_capex_cut_equipment_4c

AUTO_MOBILITY:
- hyundai_hybrid_shareholder_return_candidate
- kia_mix_shareholder_return_candidate
- auto_parts_customer_concentration_counterexample
- tire_raw_material_margin_4c

AIRLINE_TRAVEL_CYCLE:
- korean_air_asiana_integration_candidate
- korean_air_record_revenue_cycle_candidate
- airline_oil_fx_4c
- cargo_passenger_mix_slowdown_counterexample

CASINO_DUTYFREE_TOURISM:
- korea_china_group_visa_free_tourism_stage1
- hotel_shilla_paradise_tourism_candidate
- inspire_resort_underperformance_4c
- dutyfree_china_dependency_counterexample

RETAIL_CONVENIENCE:
- cu_overseas_store_efficiency_candidate
- gs25_pb_store_efficiency_candidate
- convenience_store_wage_rent_pressure_counterexample
- convenience_overcrowding_same_store_slowdown_4c

AGRI_LIVESTOCK:
- smart_farm_export_order_candidate
- tuna_price_fx_candidate
- feed_cost_pressure_counterexample
- livestock_disease_event_oneoff

SPACE_SUPPLYCHAIN:
- defense_drone_contract_candidate
- spacex_supplier_contract_candidate
- spacex_theme_no_revenue_counterexample
- drone_policy_no_contract_counterexample
```

---

# 이번 라운드 핵심 교정

```text
1. 반도체 장비·소재는 HBM 수요의 2차 수혜지만, 고객사 CAPEX 의존도가 커서 HBM보다 visibility를 낮춘다.

2. 완성차는 하이브리드·FCF·주주환원이 붙으면 Green 가능성이 있다. 부품주는 고객 다변화와 원가전가가 없으면 Watch.

3. 항공은 통합 시너지와 매출 회복이 있어도 cycle 성격이 강하다. Stage 3-Green은 제한.

4. 카지노·면세는 중국 관광 정책이 Stage 1 신호가 될 수 있지만, OP 레버리지 확인 전까지 Green 금지.

5. 편의점은 점포 수가 아니라 SSSG, PB mix, OPM, FCF가 핵심이다.

6. 농축산·사료·참치는 대부분 가격 cycle/event라 Green 제한.

7. 스페이스X·드론·플라잉카는 실제 납품계약 전까지 테마로 본다.

8. AI 냉각·HBM은 Green 가능성이 높은 쪽이지만, 성공 후 4B-watch와 CAPEX reversal 리스크를 반드시 켠다.
```

---

# 현재 판단

이제 점수비중은 **v1.5 수준의 가설 지도**로 꽤 넓어졌다.
하지만 여전히 마지막 단계는 같다.

```text
성공/반례 case 추가
→ stage date 후보 설정
→ price path backfill
→ MFE/MAE/drawdown 계산
→ score-price alignment
→ shadow scoring
→ 틀린 archetype 재교정
```

지금까지 쌓은 성공/반례는 점수정규화에 충분히 도움이 되고 있다. 다만 실제 적용은 반드시 주가검증 이후다.

[1]: https://www.reuters.com/world/asia-pacific/sk-hynix-buy-euv-scanners-8-billion-asml-korea-2026-03-24/?utm_source=chatgpt.com "SK Hynix to buy $8 billion in ASML chipmaking tools in largest disclosed order"
[2]: https://www.reuters.com/business/media-telecom/nvidia-supply-more-than-260000-blackwell-ai-chips-south-korea-2025-10-31/?utm_source=chatgpt.com "Nvidia to supply more than 260,000 Blackwell AI chips to South Korea"
[3]: https://www.reuters.com/business/autos-transportation/hyundai-motor-targets-30-rise-sales-by-2030-it-expands-hybrid-lineup-2024-08-28/?utm_source=chatgpt.com "Hyundai targets 30% rise in sales by 2030, as it doubles hybrid lineups"
[4]: https://www.reuters.com/business/aerospace-defense/korean-air-reports-record-annual-revenue-flags-uncertainties-global-politics-2025-02-07/?utm_source=chatgpt.com "Korean Air reports record annual revenue, flags uncertainties from global politics"
[5]: https://www.reuters.com/markets/deals/korean-air-completes-asiana-takeover-form-one-asias-biggest-airlines-2024-12-12/?utm_source=chatgpt.com "Korean Air completes Asiana takeover to form one of Asia's biggest airlines"
[6]: https://www.reuters.com/world/china/south-korea-offer-visa-fee-entry-chinese-tourists-late-september-2025-08-06/?utm_source=chatgpt.com "South Korea to offer visa-fee entry to Chinese tourists from late September"
[7]: https://www.ft.com/content/d8a84f6d-f227-4698-9e19-ff170791b8c2?utm_source=chatgpt.com "How Bain took over a $1.6bn Native American casino in South Korea"
[8]: https://en.wikipedia.org/wiki/CU_%28store%29?utm_source=chatgpt.com "CU (store)"
