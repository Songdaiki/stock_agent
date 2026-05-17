좋아. **Round 30: 얇은 archetype 추가 보강 + 주요 archetype 검증계획 v2.1**로 간다.

이번 라운드부터는 단순히 점수비중을 더 붙이는 것에서 한 단계 나아가서, 각 archetype마다 **“이 점수비중이 실제 주가 경로와 맞는지 어떻게 검증할지”**까지 같이 붙일게.

핵심 원칙은 그대로다.

> 테마명은 점수 근거가 아니다.
> 점수는 산업 구조 변화, EPS/FCF 체급 변화, 시장의 과거 프레임 오해, 밸류에이션 리레이팅 가능성에서 나와야 한다.
> 계약금액, 계약기간, 매출 대비 계약금액, OP YoY 같은 값은 실제 상세공시·리포트에서 확인된 것만 써야 하고, 없는 숫자를 만들어 넣으면 안 된다.

---

# Round 30에서 더 파는 Archetype

```text
1. GRID_TRANSFORMER_SHORTAGE
   전력설비 / 변압기 / AI 데이터센터 전력망

2. ANIMAL_HEALTH_BIOSECURITY
   동물백신 / 방역 / 조류독감 / 양돈·육계 이벤트와 분리

3. TELEHEALTH_BEHAVIORAL_HEALTH
   원격의료 / 온라인 정신건강 / DTC 헬스케어 플랫폼

4. PRECIOUS_METALS_SAFE_HAVEN_MINERS
   금은 / 금광주 / 안전자산 / 원자재 cycle

5. SERVICE_KIOSK_SELF_CHECKOUT
   키오스크 / 셀프체크아웃 / 무인화

6. OPTICAL_NETWORKING_AI_DATACENTER
   광섬유 / 광케이블 / AI 데이터센터 네트워크

7. AI_GRID_FLEXIBILITY_SOFTWARE
   AI 데이터센터 전력 유연화 / 스마트그리드 SW

8. PHARMA_CHANNEL_AND_PRIVACY_RISK
   온라인 의료 플랫폼 / 개인정보 / 광고·규제 리스크
```

---

# 1. GRID_TRANSFORMER_SHORTAGE

## 전력설비 / 변압기 / 전선 / AI 데이터센터 전력망

### 핵심 구조

```text
AI 데이터센터·EV·공장·재생에너지 증가
→ 송배전망 확장 필요
→ 대형 변압기·전력기기 공급부족
→ 긴 리드타임·가격 상승
→ 수주잔고와 EPS/FCF 상향
```

이 archetype은 이제 `CONTRACT_BACKLOG_INDUSTRIAL` 안에서 더 강하게 분리해도 된다. Reuters는 미국에서 데이터센터, EV, 공장, 재생에너지 프로젝트 수요 때문에 발전용·변전용 변압기 수요가 2019년 이후 각각 크게 늘었고, 대형 변압기 리드타임이 최대 4년, 가격도 5년간 약 80% 올랐다고 보도했다. 특히 미국 개발사들이 한국·튀르키예 등 해외 공급처로 돌리고 있다는 점은 한국 전력기기/변압기 업체들의 구조적 수혜 근거가 될 수 있다. ([Reuters][1])

### 성공사례 후보

```text
- HD현대일렉트릭
- 효성중공업
- LS ELECTRIC
- 제룡전기류 변압기·전력기기
- 전선·케이블 업체 중 장기공급계약과 마진이 확인되는 기업
```

### 반례

```text
- 전력설비 테마만 있고 실제 변압기·전선 수주 없음
- 계약금액은 크지만 마진이 낮음
- CAPA 확장으로 공급부족 완화
- 고객사 데이터센터 프로젝트 지연
- 원자재·인건비 상승으로 OPM 훼손
```

### 점수비중 v2.1

```text
EPS/FCF: 22
Structural Visibility: 25
Bottleneck/Pricing: 23
Market Mispricing: 12
Valuation Rerating: 12
Capital Allocation: 1
Information Confidence: 5
Risk Penalty: capacity_normalization / low_margin_contract / project_delay / raw_material
```

### 정규화 교정

이 archetype은 **Green 가능성이 매우 높은 축**이다.
단, 계약의 질이 중요하다.

```text
점수 강화:
- 계약금액/매출 비중
- 2~5년 이상 납품기간
- 수주잔고/매출 상승
- 리드타임 장기화
- 가격 전가력
- FY1/FY2/FY3 OP 상향

점수 제한:
- 전력설비 테마명만 있음
- 저마진 계약
- CAPA 증설로 공급부족 완화
- 데이터센터 프로젝트 지연
```

### 주가검증 계획

```text
Stage 1 date:
변압기/전력망/AI 데이터센터 수요 뉴스 또는 sector report 최초 포착일

Stage 2 date:
OpenDART 공급계약, 실적 서프라이즈, 수주잔고 급증, OP/EPS 상향 리포트 발생일

Stage 3 date:
중장기 EPS/OP 상향 + 다년 수주잔고 + 목표가/valuation frame 전환이 동시에 확인된 날

검증지표:
MFE_90D, MFE_180D, MFE_1Y, MFE_2Y
MAE_90D, MAE_180D
Stage 3 이후 20~30% 조정 후 재상승 여부
OP/EPS revision 지속 여부
수주잔고 증가율
PBR/PER band 상승 여부

성공 판정:
Stage 2/3 이후 주가가 6~24개월 내 구조적으로 리레이팅되고,
OP/EPS 상향과 수주잔고 증가가 같이 갔으면 aligned.

실패 판정:
수주 뉴스 후 주가는 올랐지만 OP/EPS·마진이 안 따라오거나,
계약이 저마진으로 확인되면 false_positive_score.
```

---

# 2. ANIMAL_HEALTH_BIOSECURITY

## 동물백신 / 방역 / 조류독감 / ASF / 양돈·육계 이벤트와 분리

### 핵심 구조

```text
질병 이벤트
→ 백신·방역 수요 증가
→ 정부 승인·비축·반복 접종
→ 단, 대부분 이벤트성 수요
```

동물백신은 `AGRI_LIVESTOCK_FOOD_COMMODITY`나 `EVENT_DISEASE_PEST_DEMAND`와 섞이면 안 된다. 백신·동물의약품 기업은 반복 매출이 생길 수 있지만, 조류독감·ASF 이벤트 테마주는 대부분 일회성이다.

Zoetis의 조류독감 백신 조건부 승인 사례는 이 archetype의 Stage 1~2 후보로 좋다. Reuters는 미국 USDA가 Zoetis의 가금류 조류독감 백신 사용을 조건부 승인했고, 이 승인은 긴급·특수 상황에서 안전성과 기대 효능을 근거로 부여된 것이라고 보도했다. 동시에 USDA가 백신 비축을 검토하고 있다는 점은 정부 수요의 가능성을 보여준다. ([Reuters][2])

반면 브라질 상업 농장의 HPAI 발생 연구는 질병 이벤트가 빠른 대응으로 통제될 수 있고, 발견 지연에 따라 2차 감염이 크게 달라질 수 있음을 보여준다. 즉 질병 뉴스 하나만으로 장기 수요를 가정하면 안 된다. ([arXiv][3])

### 성공 후보

```text
- Zoetis류 동물백신 기업
- 반복 접종이 필요한 동물의약품
- 정부 비축·방역 계약
- 대형 축산 고객·수의 채널 보유 기업
```

### 반례

```text
- 조류독감/ASF 뉴스만 있는 테마주
- 방역약품 단기 수요
- 살처분·이동제한 이벤트
- 질병이 빠르게 통제되어 수요가 사라짐
- 정부 백신 사용정책 불확실
```

### 점수비중 v2.1

```text
EPS/FCF: 16
Structural Visibility: 14
Bottleneck/Pricing: 8
Market Mispricing: 10
Valuation Rerating: 8
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: disease_event_normalization / policy_uncertainty / one_off_demand
```

### 정규화 교정

```text
점수 강화:
- 정부 승인
- 정부 비축 또는 장기 방역계약
- 반복 접종 수요
- 축산·수의 유통망
- 실제 매출 증가

점수 제한:
- 질병 뉴스만 있음
- 방역 테마만 있음
- 일회성 살처분·방역 수요
- 정부 사용정책 불확실
```

### 주가검증 계획

```text
Stage 1 date:
질병 발생 뉴스, 정부 방역 강화, 백신 조건부 승인일

Stage 2 date:
백신/동물의약품 매출 증가, 정부 비축계약, 반복 접종 evidence 확인일

Stage 3 date:
반복 매출과 장기 계약이 확인된 경우만 설정

검증지표:
질병 뉴스 후 MFE_30D/90D
질병 통제 후 drawdown
매출이 다음 분기/다음 해 유지되는지
재고·일회성 매출 여부

성공 판정:
질병 이벤트 후에도 백신·동물의약품 반복매출이 유지되면 Watch-to-Green.

실패 판정:
질병 뉴스 후 급등했지만 수요 정상화로 주가와 매출이 꺾이면 one_off_event.
```

---

# 3. TELEHEALTH_BEHAVIORAL_HEALTH

## 원격의료 / 온라인 정신건강 / DTC 헬스케어 플랫폼

### 핵심 구조

```text
의료 접근성 문제
→ 원격진료·온라인 상담 플랫폼
→ 반복 이용·기업/보험 계약
→ 단, CAC·광고비·개인정보·보험수가 리스크
```

Teladoc은 원격의료 반례로 반드시 넣어야 한다. Reuters는 Teladoc이 BetterHelp 관련 7.9억 달러 impairments를 기록하고, 고객획득비 증가와 매출 둔화로 2024년 연간·장기 전망을 철회했다고 보도했다. 주가는 2024년에 크게 하락했고, 온라인 mental health 사업의 광고비 부담이 핵심 문제로 지적됐다. ([Reuters][4])

BetterHelp의 개인정보 논란도 중요하다. BetterHelp는 민감한 정신건강 데이터를 광고 목적으로 공유했다는 FTC 혐의에 대해 780만 달러 합의금을 낸 바 있다. 온라인 헬스케어 플랫폼에서는 **반복 이용자 수보다 개인정보·광고·CAC·신뢰도**가 더 중요해질 수 있다. ([위키백과][5])

### 성공 후보

```text
- 기업/보험 계약 기반 원격의료
- 낮은 CAC로 반복 이용자 확보
- chronic care·integrated care 모델
- 병원·보험사와 연결된 B2B/B2B2C 구조
```

### 반례

```text
- DTC 광고비 의존
- CAC 상승
- 개인정보·민감정보 이슈
- BetterHelp류 매출 둔화
- 보험/기업 계약 없이 소비자 직접판매만 의존
```

### 점수비중 v2.1

```text
EPS/FCF: 17
Structural Visibility: 16
Bottleneck/Pricing: 6
Market Mispricing: 12
Valuation Rerating: 10
Capital Allocation: 0
Information Confidence: 6
Risk Penalty: CAC / privacy / reimbursement / churn / impairment
```

### 정규화 교정

```text
점수 강화:
- 보험사·고용주 계약
- 반복 이용률
- 낮은 CAC
- chronic care integration
- FCF 개선

점수 제한:
- DTC 광고비로 성장
- 개인정보 이슈
- BetterHelp식 impairment
- 전망 철회
- churn 증가
```

### 주가검증 계획

```text
Stage 1 date:
telehealth adoption 뉴스, 신규 서비스 출시, 기업/보험 제휴일

Stage 2 date:
구독/계약 매출 증가, CAC 안정, FCF 개선 확인일

Stage 3 date:
B2B/B2B2C 반복 매출과 low churn이 확인된 경우만

검증지표:
매출 성장률
CAC 또는 광고비 비율
FCF margin
churn
개인정보 이슈 후 drawdown
MFE/MAE 90D/1Y

성공 판정:
매출 성장과 FCF가 같이 개선되면 aligned.

실패 판정:
매출은 성장했지만 CAC·impairment·개인정보 리스크로 주가가 꺾이면 false_positive_score.
```

---

# 4. PRECIOUS_METALS_SAFE_HAVEN_MINERS

## 금은 / 금광주 / 안전자산 / 귀금속 cycle

### 핵심 구조

```text
금·은 가격 상승
→ 광산업체 realized price 상승
→ 비용 통제 시 FCF 급증
→ 단, 금 자체는 macro/real yield cycle
```

금·은은 테마가 아니라 commodity cycle로 봐야 한다. 다만 금광주는 금 가격 상승과 비용 통제가 같이 있으면 EPS/FCF가 크게 증가할 수 있다.

Barrick은 좋은 성공 후보야. Reuters는 Barrick이 2026년 1분기 record gold price 덕분에 이익 예상을 상회했고, 평균 금 가격이 전년 대비 63% 오른 4,673.5달러였으며, 평균 실현 가격은 4,823달러, 생산 비용은 4% 감소했다고 보도했다. 순이익은 전년 대비 3배 증가했고 30억 달러 자사주 매입도 발표했다. ([Reuters][6])

반면 금·은은 높은 가격 자체가 리스크다. 2026년 금과 은이 고점에서 조정받는 장면은 안전자산이라도 금리·인플레이션·실질금리·달러에 따라 흔들릴 수 있음을 보여준다. ([월스트리트저널][7])

### 성공 후보

```text
- Barrick류 금광주
- 낮은 AISC, 높은 realized price
- 생산량 증가
- 자사주·배당
- 정치 리스크 낮은 광산 포트폴리오
```

### 반례

```text
- 금 가격 상승만 보고 관련주 Green
- AISC 상승
- 광산 정치 리스크
- 생산량 감소
- 금리 상승으로 금 가격 조정
```

### 점수비중 v2.1

```text
EPS/FCF: 20
Structural Visibility: 10
Bottleneck/Pricing: 16
Market Mispricing: 9
Valuation Rerating: 8
Capital Allocation: 5
Information Confidence: 5
Risk Penalty: gold_price_reversal / AISC / jurisdiction / production_decline
```

### 정규화 교정

```text
점수 강화:
- 금·은 실현가격 상승
- AISC 안정 또는 하락
- 생산량 증가
- FCF 증가
- 자사주·배당

점수 제한:
- 금 가격 테마만 있음
- 생산 비용 상승
- 광산 정치 리스크
- 금리 상승과 가격 조정
```

### 주가검증 계획

```text
Stage 1 date:
금·은 가격 breakout, 실질금리 하락, 안전자산 수요 뉴스

Stage 2 date:
광산업체 실적에서 realized price, AISC, FCF 개선 확인일

Stage 3 date:
금 가격 상승 + 비용 통제 + 자본환원이 같이 확인될 때만

검증지표:
금/은 가격 대비 종목 상대수익률
AISC 변화
FCF yield
자사주/배당
drawdown after commodity peak

성공 판정:
금 가격 상승과 FCF·자본환원이 동행하면 cyclical_success 또는 Watch-to-Green.

실패 판정:
금 가격만 오르고 비용·생산·정치 리스크로 FCF가 안 나오면 false_positive.
```

---

# 5. SERVICE_KIOSK_SELF_CHECKOUT

## 키오스크 / 셀프체크아웃 / 무인화

### 핵심 구조

```text
인건비 상승·무인화 수요
→ 키오스크·셀프체크아웃 설치
→ 장비 판매 + 유지보수·결제 수익
→ 단, theft·고객불만·pseudo-automation 리스크
```

셀프체크아웃은 자동화처럼 보이지만 강한 반례가 많다. Target, Dollar General, Five Below 등 여러 미국 유통사가 도난·고객경험 문제 때문에 셀프체크아웃을 제한하거나 축소했다는 보도가 있었다. ([뉴욕 포스트][8])

또 self-service machine이 실제 자동화라기보다 고객에게 노동을 이전하는 pseudo-automation으로 작동하고, 직원은 여러 고객의 문제 해결·감시·갈등 관리까지 맡게 된다는 연구도 있다. ([arXiv][9])

### 성공 후보

```text
- 유지보수 반복매출이 있는 키오스크 업체
- 결제수수료·SW upgrade가 붙는 무인화 플랫폼
- theft reduction·loss prevention 기능이 있는 솔루션
- 점포 운영비 절감이 검증된 B2B 계약
```

### 반례

```text
- 장비 일회성 판매
- 절도 증가
- 고객불만
- 직원 workload 증가
- 유통사가 self-checkout을 축소
```

### 점수비중 v2.1

```text
EPS/FCF: 17
Structural Visibility: 15
Bottleneck/Pricing: 7
Market Mispricing: 12
Valuation Rerating: 10
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: theft / customer_friction / one_off_hardware / maintenance_cost / retailer_retreat
```

### 정규화 교정

```text
점수 강화:
- 설치대수 증가
- 유지보수 반복매출
- 결제수수료
- loss prevention 성과
- B2B 장기계약

점수 제한:
- 키오스크 테마만 있음
- 장비 일회성 판매
- theft 증가
- 고객불만
- 유통사 축소 전환
```

### 주가검증 계획

```text
Stage 1 date:
무인화·키오스크 도입 뉴스, 최저임금/인건비 이슈

Stage 2 date:
설치대수 증가, 유지보수 매출, 결제수수료 매출 확인일

Stage 3 date:
반복매출이 hardware 매출을 넘어서는 경우만

검증지표:
장비 매출 vs recurring revenue 비중
gross margin
고객사 재계약률
도입 유통사의 shrink 변화
주가 MFE/MAE 180D

성공 판정:
recurring revenue와 margin이 동행하면 Watch-to-Green.

실패 판정:
장비 판매 후 반복매출 없이 둔화되면 one_off_hardware.
```

---

# 6. OPTICAL_NETWORKING_AI_DATACENTER

## 광섬유 / 광케이블 / AI 데이터센터 네트워크

### 핵심 구조

```text
AI GPU cluster 확대
→ 서버 간 데이터 이동 폭증
→ 광섬유·광트랜시버·케이블 수요 증가
→ hyperscaler 장기계약
```

이 archetype은 `TELECOM_5G_6G_CAPEX_CYCLE`과 분리해야 한다. 통신사 5G 장비는 CAPEX cycle이지만, AI 데이터센터 optical networking은 hyperscaler CAPEX와 직접 연결된다.

### 성공 후보

Meta와 Corning의 광섬유 계약은 대표 성공 후보로 계속 유지한다. 이 구조는 “AI 데이터센터 → 광섬유·광케이블 병목 → 장기계약”이다. 광통신이 단순 통신망 교체가 아니라 AI 데이터센터 하위 병목으로 바뀌는 경우에는 Green 가능성이 올라간다.

### 반례

```text
- 광통신 테마만 있음
- AI 데이터센터 납품 확인 없음
- hyperscaler 단일 고객 과의존
- valuation crowding
- CAPEX 지연
```

### 점수비중 v2.1

```text
EPS/FCF: 21
Structural Visibility: 22
Bottleneck/Pricing: 20
Market Mispricing: 13
Valuation Rerating: 12
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: hyperscaler_concentration / valuation_crowding / capex_delay / inventory
```

### 정규화 교정

```text
Green 가능:
- hyperscaler 장기계약
- AI 데이터센터 직접 납품
- optical bottleneck
- OP/EPS 상향

Green 금지:
- 5G/광통신 테마만 있음
- 고객사 불명확
- 수주 없음
- 주가 과열
```

### 주가검증 계획

```text
Stage 1 date:
AI 데이터센터 optical networking 수요 뉴스

Stage 2 date:
hyperscaler 계약·수주·납품 evidence 확인일

Stage 3 date:
OP/EPS 상향 + 다년계약 + 병목 프레임 전환 확인일

검증지표:
수주 발표 후 MFE_90D/180D/1Y
OP/EPS revision
매출처 concentration
valuation multiple expansion
4B 이후 drawdown

성공 판정:
계약·EPS 상향·주가 리레이팅이 같이 가면 aligned.

실패 판정:
AI optical 테마로 주가만 뛰고 수주·EPS가 없으면 price_moved_without_evidence.
```

---

# 7. AI_GRID_FLEXIBILITY_SOFTWARE

## AI 데이터센터 전력 유연화 / 스마트그리드 SW

### 핵심 구조

```text
AI 데이터센터 전력 변동성
→ grid interconnection 병목
→ load shifting·forecasting·flexibility SW
→ 전력비 절감·접속기간 단축
→ 단, 아직 상용화 초기
```

AI 데이터센터 전력부하는 기존 데이터센터와 다르게 빠르고 크게 변동할 수 있다. AI 데이터센터의 단기 전력 수요 예측 연구는 GPU workload 변동이 전력망 운영에 도전이 되며, LSTM/GRU/CNN 기반 예측모델이 필요하다고 설명한다. ([arXiv][10])

또 AI 데이터센터가 rigid load가 아니라 유연하게 조정 가능한 load가 되면 grid investment와 운영비를 줄일 수 있지만, 그 효과는 위치·부하조건·유연성 범위에 따라 달라진다는 연구가 있다. ([arXiv][11])

### 성공 후보

```text
- 데이터센터 load forecasting SW
- grid interconnection optimization
- ESS + AI workload scheduling
- 유틸리티와 데이터센터 연결 소프트웨어
```

### 반례

```text
- 연구/PoC만 있음
- 실제 유틸리티/데이터센터 고객 없음
- 수익모델 없음
- 규제·계통운영자 채택 지연
```

### 점수비중 v2.1

```text
EPS/FCF: 17
Structural Visibility: 17
Bottleneck/Pricing: 15
Market Mispricing: 13
Valuation Rerating: 10
Capital Allocation: 0
Information Confidence: 6
Risk Penalty: commercialization / utility_adoption / regulation / proof_of_concept_only
```

### 정규화 교정

```text
점수 강화:
- 실제 유틸리티·데이터센터 고객
- 전력 절감·접속기간 단축 증거
- 반복 SW 매출
- 규제·계통운영자 채택

점수 제한:
- 논문/PoC 단계
- 스마트그리드 테마만 있음
- 매출 없음
- 고객 없음
```

### 주가검증 계획

```text
Stage 1 date:
AI data center grid stress, load forecasting, smart grid flexibility 뉴스

Stage 2 date:
유틸리티/데이터센터 계약, 파일럿 상용화, 반복 SW 매출 확인일

Stage 3 date:
반복 매출 + 고객 다변화 + EPS/OP 상향이 확인될 때만

검증지표:
계약 후 매출 인식 여부
ARR 또는 recurring revenue
OPM 개선
AI grid theme rally 이후 drawdown
MFE/MAE 1Y

성공 판정:
PoC에서 계약·매출로 전환되면 Watch-to-Green.

실패 판정:
PoC·정책 뉴스만 있고 매출이 없으면 theme_watch 또는 false_positive.
```

---

# 8. PHARMA_CHANNEL_AND_PRIVACY_RISK

## 온라인 의료 플랫폼 / 약물 유통 / 개인정보 / 광고·규제

### 핵심 구조

```text
온라인 의료 접근성 증가
→ telehealth·온라인 약국·약물 플랫폼
→ 반복 매출 가능
→ 단, 개인정보·광고·품질·규제 리스크 큼
```

BetterHelp와 Teladoc 사례는 온라인 의료 플랫폼에서 개인정보와 광고비가 얼마나 큰 리스크인지 보여준다. Teladoc은 BetterHelp 부문 impairment와 고객획득비 증가로 전망을 철회했고, BetterHelp는 민감한 정신건강 데이터를 광고 목적으로 공유했다는 FTC 혐의로 합의금을 낸 바 있다. ([Reuters][4])

### 성공 후보

```text
- 보험사·고용주 계약 기반 온라인 의료
- 합법적 처방·약물 유통 채널
- 개인정보 보호·규제 준수
- 낮은 CAC와 반복 사용
```

### 반례

```text
- DTC 광고비 의존
- 개인정보 유출·광고 활용
- 조제약 품질 문제
- 불법 온라인 약국
- 규제 당국 경고
```

### 점수비중 v2.1

```text
EPS/FCF: 16
Structural Visibility: 15
Bottleneck/Pricing: 6
Market Mispricing: 12
Valuation Rerating: 10
Capital Allocation: 0
Information Confidence: 6
Risk Penalty: privacy / advertising_CAC / FDA_warning / illegal_pharmacy / liability
```

### 정규화 교정

```text
점수 강화:
- B2B/B2B2C 계약
- 낮은 CAC
- privacy compliance
- 합법적 처방·유통
- 반복 사용

점수 제한:
- DTC 광고비 의존
- 민감정보 활용
- 불법 온라인 약국
- FDA/FTC 경고
- impairment
```

### 주가검증 계획

```text
Stage 1 date:
온라인 의료 서비스 출시, telehealth 제휴, 약물 플랫폼 성장 뉴스

Stage 2 date:
보험·고용주 계약, recurring revenue, CAC 안정 확인일

Stage 3 date:
FCF 개선과 개인정보 리스크 안정 확인일

검증지표:
CAC/revenue
FCF margin
privacy/legal event drawdown
churn
MFE/MAE 1Y

성공 판정:
B2B 계약 기반 recurring revenue와 FCF 개선이 동행하면 aligned.

실패 판정:
DTC 성장 후 privacy/CAC/impairment로 꺾이면 4C.
```

---

# Round 30 점수비중 요약표

| Archetype                   | EPS/FCF | Visibility | Bottleneck | Mispricing | Valuation | Capital | 핵심 리스크                |
| --------------------------- | ------: | ---------: | ---------: | ---------: | --------: | ------: | --------------------- |
| GRID_TRANSFORMER_SHORTAGE   |      22 |         25 |         23 |         12 |        12 |       1 | CAPA 정상화, 저마진         |
| ANIMAL_HEALTH_BIOSECURITY   |      16 |         14 |          8 |         10 |         8 |       0 | one-off 질병 이벤트        |
| TELEHEALTH_BEHAVIORAL       |      17 |         16 |          6 |         12 |        10 |       0 | CAC, 개인정보             |
| PRECIOUS_METALS_MINERS      |      20 |         10 |         16 |          9 |         8 |       5 | 금가격, AISC             |
| SERVICE_KIOSK_SELF_CHECKOUT |      17 |         15 |          7 |         12 |        10 |       0 | theft, 고객불만           |
| OPTICAL_NETWORKING_AI_DC    |      21 |         22 |         20 |         13 |        12 |       0 | 고객집중, 과열              |
| AI_GRID_FLEXIBILITY_SW      |      17 |         17 |         15 |         13 |        10 |       0 | PoC, 상용화 지연           |
| PHARMA_CHANNEL_PRIVACY      |      16 |         15 |          6 |         12 |        10 |       0 | privacy, CAC, FDA/FTC |

---

# cases_v18 추가 후보

```text
GRID_TRANSFORMER_SHORTAGE:
- us_transformer_shortage_korea_import_success_candidate
- transformer_leadtime_price_increase_success_candidate
- low_margin_power_equipment_contract_counterexample
- datacenter_project_delay_transformer_4c

ANIMAL_HEALTH_BIOSECURITY:
- zoetis_bird_flu_vaccine_conditional_approval_candidate
- hpai_poultry_event_oneoff_counterexample
- animal_vaccine_stockpile_candidate
- disease_control_normalization_counterexample

TELEHEALTH_BEHAVIORAL_HEALTH:
- teladoc_betterhelp_cac_impairment_4c
- employer_insurance_telehealth_contract_candidate
- betterhelp_privacy_ftc_counterexample
- telehealth_dtc_ad_cost_counterexample

PRECIOUS_METALS_SAFE_HAVEN_MINERS:
- barrick_record_gold_price_profit_candidate
- gold_price_correction_4b_watch
- miner_aisc_inflation_counterexample
- jurisdiction_risk_gold_miner_4c

SERVICE_KIOSK_SELF_CHECKOUT:
- kiosk_recurring_service_candidate
- target_dollar_general_self_checkout_theft_counterexample
- pseudo_automation_worker_burden_counterexample
- one_off_kiosk_hardware_sales_counterexample

OPTICAL_NETWORKING_AI_DATACENTER:
- meta_corning_fiber_contract_success_candidate
- optical_networking_valuation_crowding_4b
- optical_customer_concentration_counterexample
- ai_datacenter_capex_delay_optical_4c

AI_GRID_FLEXIBILITY_SOFTWARE:
- ai_datacenter_load_forecasting_candidate
- grid_flexible_datacenter_candidate
- smart_grid_poc_no_revenue_counterexample
- utility_adoption_delay_4c

PHARMA_CHANNEL_AND_PRIVACY_RISK:
- betterhelp_privacy_ftc_4c
- teladoc_betterhelp_impairment_4c
- legal_telehealth_b2b_contract_candidate
- online_pharma_cac_privacy_counterexample
```

---

# 이번 라운드 핵심 교정

```text
1. 전력설비/변압기는 Green 가능성이 매우 높다.
   AI 데이터센터 전력망 병목과 실제 수주·리드타임·가격 상승이 핵심이다.

2. 동물백신/방역은 반복 백신·정부 비축이면 후보지만, 질병 뉴스만 있으면 one-off event다.

3. 원격의료/온라인 정신건강은 CAC·개인정보·DTC 광고비가 핵심 리스크다.

4. 금은/금광주는 commodity cycle이다.
   realized price와 AISC, FCF, 자본환원이 같이 있어야 후보.

5. 키오스크/셀프체크아웃은 절도·고객불만·pseudo-automation 때문에 Green 제한.

6. 광섬유/광통신은 AI 데이터센터와 직접 연결되면 Green 가능성이 생긴다.

7. AI grid flexibility SW는 기술적으로 중요하지만 PoC에서 실제 반복 매출로 넘어가는지가 핵심이다.

8. 온라인 의료/약물 플랫폼은 개인정보·광고비·규제·품질 리스크를 강하게 감점해야 한다.
```

---

# Archetype별 실제 주가 경로 검증 계획

이제부터는 각 archetype을 이렇게 검증해야 한다.

## 1. Green 가능형 검증

대상:

```text
GRID_TRANSFORMER_SHORTAGE
AI_DATA_CENTER_COOLING
OPTICAL_NETWORKING_AI_DC
MEMORY_HBM_CAPACITY
K_BEAUTY_EXPORT_DISTRIBUTION
CDMO_HEALTHCARE_CONTRACT
MEDICAL_DEVICE_HEALTHCARE_EXPORT
INSURANCE_UNDERWRITING_CYCLE
```

검증 방식:

```text
Stage 1:
산업 구조 변화 최초 evidence 발생일

Stage 2:
실제 계약·실적·수주잔고·EPS 상향 확인일

Stage 3:
중장기 EPS/FCF 상향 + valuation frame 변화 확인일

가격 검증:
MFE_90D / 180D / 1Y / 2Y
MAE_90D / 180D
drawdown_after_peak
PBR/PER band 변화
컨센서스 revision 지속성

성공:
Stage 2/3 이후 EPS/FCF와 주가가 같이 리레이팅

실패:
뉴스는 강했지만 EPS/FCF가 안 따라오거나 주가가 6~12개월 내 원위치
```

---

## 2. Watch-to-Green형 검증

대상:

```text
CLOUD_AI_SOFTWARE_INFRA
DIGITAL_HEALTHCARE_AI
TELEHEALTH_BEHAVIORAL_HEALTH
CRO_CLINICAL_SERVICE
PAYMENT_FINTECH_INFRA
DATA_CENTER_REIT_INFRASTRUCTURE
AI_GRID_FLEXIBILITY_SW
SERVICE_KIOSK_SELF_CHECKOUT
```

검증 방식:

```text
Stage 1:
테마/기술/규제/서비스 출시

Stage 2:
반복매출·계약·고객사·OPM 개선 확인

Stage 3:
FCF 전환 또는 recurring revenue가 valuation frame을 바꾸는지 확인

가격 검증:
ARR/revenue growth와 주가 동행 여부
gross margin/OPM 변화
CAC/churn/security/legal event 발생 여부
MFE_180D / 1Y
MAE_180D / 1Y

성공:
기술 뉴스가 반복매출·FCF로 전환되고 주가가 리레이팅

실패:
PoC·테마·사용자 수는 있었지만 CAC/규제/개인정보/운영비로 무너짐
```

---

## 3. Cycle / Event형 검증

대상:

```text
PRECIOUS_METALS_MINERS
LITHIUM_BATTERY_RAW_MATERIAL
AGRI_LIVESTOCK_FOOD_COMMODITY
SHIPPING_FREIGHT_CYCLE
CHEMICAL_SPREAD
REFINING_OIL_SPREAD
EVENT_DISEASE_PEST_DEMAND
```

검증 방식:

```text
Stage 1:
가격·질병·공급충격·운임 급등

Stage 2:
실제 EPS/OP 급증

Stage 3:
구조적 Green은 원칙적으로 제한.
대신 Stage 3-Red 또는 Stage 2-High로 분리

가격 검증:
commodity price peak와 종목 peak 비교
EPS peak 이후 drawdown
MFE_90D / 180D
drawdown_after_peak
다음 회계연도 EPS 정상화 여부

성공:
cycle trade로는 성공했지만 structural_success가 아니라 cyclical_success

실패:
EPS peak를 구조적 리레이팅으로 오판
```

---

## 4. Event / Red-flag형 검증

대상:

```text
NORTH_KOREA_POLICY_EVENT
METAVERSE_NFT_THEME
ADVANCED_MATERIAL_SPECULATIVE_THEME
SPECULATIVE_SCIENCE_THEME
ONE_OFF_EVENT_DEMAND
```

검증 방식:

```text
Stage 1:
정책·논문·테마 뉴스

Stage 2:
실제 계약/매출이 없는 경우 대부분 없음

Stage 3:
원칙적으로 Green 금지

가격 검증:
뉴스 후 MFE_5D / 20D / 60D
뉴스 소멸 후 drawdown
EPS/FCF evidence 존재 여부
price_only_rally 여부

성공:
대부분 trading event로만 분류

실패:
Stage 3 후보로 오분류되면 false_green
```

---

# 현재 판단

이제 점수비중 지도는 **v2.1 수준**까지 꽤 두꺼워졌다.
하지만 너 말대로 성공/반례는 많을수록 좋고, 특히 이제부터는 **각 archetype별 주가 경로 검증계획**까지 같이 붙여야 한다.

다음 단계는 명확하다.

```text
1. cases_v18까지 case library에 넣기
2. archetype별 stage date 후보 부여
3. price path backfill
4. MFE/MAE/drawdown 계산
5. score-price alignment 확인
6. Green 가능형 / Watch형 / Cycle형 / Event형으로 결과 분리
7. 틀린 점수비중 다시 교정
```

지금까지 한 작업은 “테마를 다 품는 지도”를 만드는 단계였고, 이제 다음부터는 **이 지도와 실제 주가 경로가 맞는지 검증하는 계기판**을 붙이는 단계다.

[1]: https://www.reuters.com/business/energy/us-power-transformer-buyers-scramble-imports-factory-slots--reeii-2026-05-11/?utm_source=chatgpt.com "US power transformer buyers scramble for imports, factory slots"
[2]: https://www.reuters.com/business/healthcare-pharmaceuticals/us-grants-conditional-clearance-zoetis-bird-flu-vaccine-poultry-2025-02-14/?utm_source=chatgpt.com "US gives conditional nod to Zoetis' bird flu vaccine for poultry"
[3]: https://arxiv.org/abs/2509.08492?utm_source=chatgpt.com "First highly pathogenic avian influenza outbreak in a commercial farm in Brazil: outbreak timeline, control actions, risk analysis, and transmission modeling"
[4]: https://www.reuters.com/business/healthcare-pharmaceuticals/teladoc-shares-hit-record-low-after-telehealth-firm-withdraws-2024-forecast-2024-08-01/?utm_source=chatgpt.com "Teladoc shares hit record low after telehealth firm withdraws 2024 forecast"
[5]: https://en.wikipedia.org/wiki/BetterHelp?utm_source=chatgpt.com "BetterHelp"
[6]: https://www.reuters.com/business/barrick-mining-beats-first-quarter-profit-estimates-2026-05-11/?utm_source=chatgpt.com "Barrick beats Q1 profit estimates on record gold prices, unveils $3 bln buyback"
[7]: https://www.wsj.com/finance/commodities-futures/gold-rises-defensive-appeal-remains-intact-f75acc88?utm_source=chatgpt.com "Comex Gold Settles 0.42% Lower at $4678.10"
[8]: https://nypost.com/2024/03/16/target-to-limit-self-checkout-option-to-10-items/?utm_source=chatgpt.com "Target to limit self-checkout to 10 items as stores trend away from the technology amid concerns of theft"
[9]: https://arxiv.org/abs/2410.02888?utm_source=chatgpt.com "Pseudo-Automation: How Labor-Offsetting Technologies Reconfigure Roles and Relationships in Frontline Retail Work"
[10]: https://arxiv.org/abs/2503.07756?utm_source=chatgpt.com "Short-Term Load Forecasting for AI-Data Center"
[11]: https://arxiv.org/abs/2604.05376?utm_source=chatgpt.com "To Defer or To Shift? The Role of AI Data Center Flexibility on Grid Interconnection"
