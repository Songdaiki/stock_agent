좋아. **Round 29: 얇은 archetype 보강 + 주요 archetype 점수비중 v2.0 교정**으로 계속 채울게.

이번 라운드는 특히 바이오·헬스케어와 서비스 자동화 쪽을 더 판다. 이쪽은 테마가 자주 붙지만, **실제 EPS/FCF 체급 변화까지 가는 케이스와 “뉴스는 화려하지만 매출화가 안 되는 케이스”의 차이**가 커서 점수정규화에 매우 중요하다.

기본 원칙은 그대로다. 테마명은 점수 근거가 아니고, 점수는 **산업 구조 변화 → EPS/FCF 체급 변화 → 시장의 과거 프레임 오해 → 밸류에이션 리레이팅**에서 나와야 한다.
계약금액, 계약기간, 매출 대비 계약금액, OP YoY 같은 값도 실제 상세공시·리포트에서 확인된 것만 써야 하고, 없는 값을 추정해서 채우면 안 된다.

---

# Round 29에서 더 파는 Archetype

```text
1. BIOSIMILAR_COMMERCIALIZATION
   바이오시밀러 / 휴미라·스텔라라·프롤리아 계열 / 가격경쟁

2. OBESITY_GLP1_COMMERCIALIZATION
   비만치료제 / GLP-1 / 경구제 / 공급·가격·규제

3. GENE_THERAPY_RARE_DISEASE
   희귀질환 치료제 / 유전자치료제 / 고가 치료제 상업화

4. AI_DRUG_DISCOVERY_PLATFORM
   AI 신약개발 / Recursion·Exscientia류 / 플랫폼 vs 실제 약물

5. CONTACT_CENTER_AI_AUTOMATION
   컨택센터 / AI 상담 / CCaaS / agent assist

6. SERVICE_KIOSK_SELF_CHECKOUT
   키오스크 / 셀프체크아웃 / 무인화 / 리테일 자동화

7. BIOSIMILAR_ORIGINATOR_DEFENSE
   오리지널 제약사 / 특허만료 / 후속 신약 전환

8. PHARMA_PLATFORM_REGULATORY_RISK
   규제·광고·판매채널 리스크 / 의료 마케팅 / 불법 복제·조제약
```

---

# 1. BIOSIMILAR_COMMERCIALIZATION

## 바이오시밀러 / 휴미라·스텔라라·프롤리아 계열

### 핵심 구조

```text
특허만료
→ 바이오시밀러 허가
→ PBM·보험·약국 채택
→ 가격경쟁
→ 물량 증가와 마진 방어가 동시에 필요
```

바이오시밀러는 **허가 자체가 Stage 3가 아니다.** 허가 후 실제 처방 전환, PBM 등재, 보험 커버리지, 가격정책, 제조원가, 마진이 따라와야 한다.

### 성공 후보

바이오시밀러는 약가 부담을 크게 낮출 수 있고, 대형 오리지널 의약품 특허만료 때 시장이 열릴 수 있다. 예를 들어 Boehringer Ingelheim과 GoodRx는 AbbVie의 Humira 바이오시밀러를 정가 대비 92% 할인된 가격으로 제공하기 시작했는데, 이는 바이오시밀러가 접근성을 높일 수 있음을 보여준다. 하지만 같은 보도에서 Humira 처방은 월 60만 건 수준인 반면 해당 바이오시밀러 처방은 2024년 5월 기준 2,500건에 그쳤다고 나와, **가격이 싸도 채택이 느릴 수 있다**는 반례도 동시에 준다. ([Reuters][1])

Stelara 계열도 비슷하다. 2024~2025년에 ustekinumab 바이오시밀러가 미국·유럽에서 여럿 승인되었고, Celltrion의 Steqeyma/Qoyvolma 같은 사례도 있다. 이건 pipeline expansion 측면에서는 긍정적이지만, 승인 품목이 많아질수록 가격경쟁과 채택 경쟁이 심해진다는 뜻이기도 하다. ([위키백과][2])

### 반례

```text
- 허가는 받았지만 처방 전환이 느림
- PBM/보험 채널에서 채택이 지연
- 약가 할인 폭이 너무 커서 마진이 낮음
- 다수 biosimilar 동시 진입으로 가격경쟁 심화
- 생산원가·품질·공급 안정성 문제
```

### 점수비중 v2.0

```text
EPS/FCF: 18
Structural Visibility: 20
Bottleneck/Pricing: 6
Market Mispricing: 13
Valuation Rerating: 11
Capital Allocation: 0
Information Confidence: 6
Risk Penalty: price_competition / payer_adoption / PBM_incentive / margin_pressure
```

### 정규화 교정

```text
점수 강화:
- FDA/EMA 등 주요 허가
- PBM/보험 등재
- 실제 처방량 증가
- 제조원가 경쟁력
- 다국가 출시
- 마진 방어

점수 제한:
- 허가 뉴스만 있음
- 처방 전환 느림
- 가격 할인 과도
- 경쟁 biosimilar 과다
- 보험·PBM 인센티브 불리
```

**핵심:**
바이오시밀러는 **Watch-to-Green**이다. 허가만으로 Green 금지. 실제 처방·등재·마진이 붙어야 Stage 2~3 후보가 된다.

---

# 2. OBESITY_GLP1_COMMERCIALIZATION

## 비만치료제 / GLP-1 / 경구제 / 공급·가격·규제

### 핵심 구조

```text
비만·당뇨 대형 수요
→ GLP-1 치료제 판매 증가
→ 공급능력·보험커버리지·가격·경쟁이 핵심
→ 장기 시장은 크지만, 리더십과 마진은 변할 수 있음
```

GLP-1 비만치료제는 구조적 수요가 매우 큰 축이지만, 점수화할 때는 **수요만 보면 안 된다.** 공급, 보험, 가격, 경쟁, 조제약·복제약, 국가별 광고규제가 동시에 작동한다.

### 성공 후보

Lilly의 경구 비만치료제는 주사제에서 경구제로 확장될 수 있는 후보로 볼 수 있다. Reuters는 Lilly의 새로운 경구 비만치료제 Foundayo가 출시 4주차에 7,335건의 처방을 기록했지만, Q2 컨센서스 매출을 맞추려면 주당 22,000건 처방이 필요하다고 보도했다. 즉 경구 GLP-1은 큰 시장 후보지만, 초기 uptake와 매출 기대 사이의 간극을 확인해야 한다. ([Reuters][3])

또 후기 임상에서 Lilly의 경구제는 기존 주사 GLP-1 사용자가 전환했을 때 체중 유지에 도움을 주는 데이터를 보였다. 이는 oral GLP-1이 “편의성 + 유지요법”으로 시장을 넓힐 수 있음을 보여주는 Stage 1~2 근거다. ([Reuters][4])

### 반례

Novo Nordisk는 GLP-1 시장의 구조적 성장 속에서도 반례를 준다. Reuters는 2025년 Novo가 Wegovy 판매 둔화와 Lilly Zepbound 경쟁, 미국 내 compounded alternative 확산 때문에 매출·영업이익 전망을 낮췄다고 보도했다. 즉 시장이 크더라도 **경쟁·가격·복제/조제 대체재·처방 성장 둔화**가 valuation을 꺾을 수 있다. ([Reuters][5])

인도에서 Lilly가 비만 인식 캠페인을 규제 우려로 중단한 사례도 중요하다. 비만치료제는 국가별 광고·의약품 홍보 규제에 민감해서, 시장 크기만으로 Green을 주면 안 된다. ([Reuters][6])

### 점수비중 v2.0

```text
EPS/FCF: 22
Structural Visibility: 20
Bottleneck/Pricing: 12
Market Mispricing: 13
Valuation Rerating: 12
Capital Allocation: 0
Information Confidence: 6
Risk Penalty: competition / reimbursement / supply / compounded_drugs / advertising_regulation
```

### 정규화 교정

```text
점수 강화:
- 실제 처방량 증가
- 보험 커버리지 확대
- 공급능력 확장
- 경구제·편의성 개선
- 장기 유지요법 데이터
- OP/EPS 상향

점수 제한:
- 초기 처방이 기대보다 느림
- 경쟁사 점유율 확대
- compounded GLP-1 대체
- 국가별 광고·홍보 규제
- 보험 커버리지 부족
```

**핵심:**
비만치료제는 **Green 가능성이 있지만 경쟁·규제·보험 리스크가 큰 고성장 archetype**이다. 단순 “시장 100조” 같은 narrative만으로 Green 금지.

---

# 3. GENE_THERAPY_RARE_DISEASE

## 희귀질환 치료제 / 유전자치료제 / 고가 치료제 상업화

### 핵심 구조

```text
희귀질환 unmet need
→ 고가 유전자치료제 승인
→ 실제 환자 모집·보험·센터 운영
→ 상업화 속도와 현금흐름이 핵심
```

희귀질환·유전자치료제는 FDA 승인만으로 성공이 아니다. 치료센터, 환자 선별, 보험·환급, 제조, 안전성, 현금흐름이 모두 따라와야 한다.

### 반례: bluebird bio

Bluebird bio는 이 archetype에서 매우 중요한 반례다. Reuters는 Bluebird가 cash crunch 속에서 Carlyle·SK Capital에 주당 3달러로 인수되어 비상장화되기로 했고, 이 가격은 직전 종가 대비 57.4% 할인된 수준이라고 보도했다. Bluebird는 2018년 한때 주가가 약 150달러였지만, 현금난과 유전자치료제 상업화 속도 부진으로 크게 무너졌고, Lyfgenia 등 승인 치료제 출시에도 초기 사용이 제한적이었다. ([Reuters][7])

이 케이스가 주는 교훈은 강하다.

```text
승인된 유전자치료제
≠ 상업적으로 성공한 치료제
```

### 점수비중 v2.0

```text
EPS/FCF: 8
Structural Visibility: 12
Bottleneck/Pricing: 8
Market Mispricing: 10
Valuation Rerating: 6
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: commercialization_slow / reimbursement / cash_burn / manufacturing / safety
```

### 정규화 교정

```text
점수 강화:
- 승인 후 실제 환자 투여 증가
- 보험·환급 구조
- 제조역량 안정
- 현금 runway 충분
- 반복 pipeline 매출 가능성

점수 제한:
- 승인 뉴스만 있음
- 고가 치료제 reimbursement 불확실
- 환자 모집 느림
- cash burn 큼
- 유증·CB·비상장화 리스크
```

**핵심:**
희귀질환·유전자치료제는 **Green 거의 금지에 가깝다.** 승인 후 실제 상업화 숫자가 나오기 전까지 Stage 1~2 또는 Watch.

---

# 4. AI_DRUG_DISCOVERY_PLATFORM

## AI 신약개발 / Recursion·Exscientia류 / 플랫폼 vs 실제 약물

### 핵심 구조

```text
AI 플랫폼
→ 후보물질 발굴
→ 임상 진입
→ 실제 승인·매출까지는 매우 긴 거리
```

AI 신약개발은 narrative가 강하지만, 실제 E2R로 가려면 “AI 플랫폼”이 아니라 **임상 성공률, 파트너십 매출, milestone, 승인 가능성, cash runway**가 필요하다.

### 성공 후보

Recursion과 Exscientia의 합병은 AI 신약개발 플랫폼 consolidation 사례다. Reuters는 Recursion이 Exscientia를 6.88억 달러 all-stock deal로 인수해 AI 기반 신약개발 역량과 파이프라인, 대형 제약사 파트너십을 강화하려 한다고 보도했다. 합병 후 약 8.5억 달러 현금을 보유해 향후 3년 운영을 지원할 수 있다는 점도 언급됐다. ([Reuters][8])

### 반례

하지만 AI 신약개발은 아직 “플랫폼 promise”와 “실제 승인 약물” 사이의 간격이 크다. Wired는 AI 신약개발 기업들이 후보물질을 임상에 올리고 있지만, 아직 시장에 출시된 AI-discovered drug은 없고, 약물 개발은 10년 이상 걸리며 후보 대부분이 실패한다고 지적했다. ([WIRED][9])

FT도 여러 AI 신약개발 스타트업이 10년 넘게 투자와 제약사 파트너십을 유치했지만, 승인된 약물이 거의 없고 후기 임상 성과가 부족하다는 점을 지적했다. ([Financial Times][10])

### 점수비중 v2.0

```text
EPS/FCF: 6
Structural Visibility: 10
Bottleneck/Pricing: 7
Market Mispricing: 12
Valuation Rerating: 6
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: clinical_failure / no_approved_drug / cash_burn / data_quality / platform_hype
```

### 정규화 교정

```text
점수 강화:
- 대형 제약사 milestone 계약
- 실제 임상 진입
- 현금 runway 충분
- pipeline 다변화
- 승인 가능성 높은 후보

점수 제한:
- AI 플랫폼 설명만 있음
- 후보물질 초기 단계
- 매출 없음
- 임상 실패
- cash burn 큼
- “AI가 신약을 빠르게 만든다” narrative만 있음
```

**핵심:**
AI 신약개발은 **Red/Watch 중심**이다. 실제 milestone과 임상 성공 전까지 Green 금지.

---

# 5. CONTACT_CENTER_AI_AUTOMATION

## 컨택센터 / AI 상담 / CCaaS / agent assist

### 핵심 구조

```text
고객센터 인건비·품질 문제
→ CCaaS / agent assist / AI bot
→ AHT 감소·CSAT 개선·운영비 절감
→ 반복 SaaS 매출
```

컨택센터 AI는 로봇보다 현실적일 수 있다. B2B 구독형 매출과 비용절감 ROI가 확인되면 Watch-to-Green 가능성이 있다.

### 성공 후보

Five9은 contact center software 기준 케이스로 볼 수 있다. Reuters는 2024년 activist investor Anson Funds가 Five9 지분을 취득하고 매각 검토를 압박했으며, Five9이 3,000개 이상 고객과 2023년 매출 9.105억 달러를 기록했다고 보도했다. 이건 contact center software가 실제 B2B 고객과 recurring revenue를 가진 산업이라는 근거다. ([Reuters][11])

AI agent-assist도 실제 생산성 개선을 목표로 한다. Minerva CQ case study는 contact center에서 실시간 전사, intent/sentiment detection, entity recognition, contextual retrieval, 요약 등을 결합해 상담원 효율과 고객경험을 개선하려는 구조를 제시한다. 다만 논문·case study는 Stage 1~2 증거이지, 상장사 EPS/FCF 증거는 아니다. ([arXiv][12])

### 반례

```text
- AI bot 도입 뉴스만 있음
- 고객센터 자동화가 실제 seat expansion이나 ARR로 연결 안 됨
- 기업 IT 예산 둔화
- churn 증가
- AI 답변 오류·고객불만
- 개인정보·음성데이터 규제 리스크
```

### 점수비중 v2.0

```text
EPS/FCF: 19
Structural Visibility: 20
Bottleneck/Pricing: 8
Market Mispricing: 14
Valuation Rerating: 13
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: churn / IT_budget / privacy / AI_error / seat_contraction
```

### 정규화 교정

```text
점수 강화:
- ARR/구독매출 증가
- seat expansion
- enterprise customer retention
- AI 기능이 실제 비용절감으로 연결
- OPM/FCF 개선

점수 제한:
- AI 상담 테마만 있음
- PoC만 있음
- 고객 이탈
- IT 예산 둔화
- 개인정보·음성데이터 리스크
```

**핵심:**
컨택센터 AI는 **Watch-to-Green**이다. 반복 SaaS와 ROI가 있어야 점수 상승.

---

# 6. SERVICE_KIOSK_SELF_CHECKOUT

## 키오스크 / 셀프체크아웃 / 무인화 / 리테일 자동화

### 핵심 구조

```text
인건비 상승·무인화 수요
→ 키오스크·셀프체크아웃 도입
→ 장비 판매 + 유지보수·결제 수익
→ 단, theft·고객불만·규제 리스크 큼
```

키오스크는 “무인화니까 좋다”가 아니다. 실제 반복 유지보수, 결제수수료, software upgrade, loss prevention까지 붙어야 한다.

### 성공 후보

셀프체크아웃과 키오스크는 인건비 절감과 checkout 효율화 측면에서 수요가 있다. 컴퓨터비전 기반 self-checkout 연구도 상품 인식 정확도와 checkout speed 향상을 목표로 한다. 다만 이건 기술 가능성이고, 기업 점수는 실제 매출·유지보수·도입률에서 나와야 한다. ([arXiv][13])

### 반례

Self-checkout은 강한 반례도 많다. The Guardian은 self-checkout이 고객 불편과 절도 증가 문제를 낳았고, 일부 소매업체들이 self-checkout을 축소하거나 재검토하고 있다고 보도했다. 또 고객이 self-checkout에서 훔칠 가능성이 일반 계산대보다 훨씬 높다는 연구·보도도 인용했다. ([가디언][14])

셀프서비스 기술은 실제 자동화라기보다 고객에게 노동을 떠넘기는 pseudo-automation으로 작동할 수 있다는 연구도 있다. 이 경우 직원은 여러 고객의 문제 해결·감시·갈등 관리를 동시에 해야 하고, 단순 인건비 절감 논리가 깨질 수 있다. ([arXiv][15])

### 점수비중 v2.0

```text
EPS/FCF: 17
Structural Visibility: 15
Bottleneck/Pricing: 7
Market Mispricing: 12
Valuation Rerating: 10
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: theft / customer_friction / regulation / one_off_hardware / maintenance_cost
```

### 정규화 교정

```text
점수 강화:
- 설치대수 증가
- 유지보수 반복매출
- 결제수수료·software revenue
- loss prevention 효과
- 고객경험 개선

점수 제한:
- 장비 일회성 판매
- 절도 증가
- 고객불만
- 지자체 규제
- 직원 workload 증가
```

**핵심:**
키오스크·셀프체크아웃은 대부분 **Watch 중심**이다. hardware 판매만 있으면 Green 금지.

---

# 7. BIOSIMILAR_ORIGINATOR_DEFENSE

## 오리지널 제약사 / 특허만료 / 후속 신약 전환

### 핵심 구조

```text
대형 블록버스터 특허만료
→ biosimilar 침투
→ 기존 매출 감소
→ 후속 신약으로 전환 성공 여부
```

이 archetype은 바이오시밀러 수혜기업뿐 아니라 오리지널 제약사 방어전략도 점수화해야 한다.

### 성공 후보

AbbVie는 Humira 특허만료 후속전환의 기준 케이스다. Humira 매출은 biosimilar 경쟁으로 줄었지만, Rinvoq와 Skyrizi 같은 후속 면역질환 치료제가 성장하면서 방어전략을 펼치고 있다. Reuters는 AbbVie의 Rinvoq가 Humira와의 head-to-head arthritis study에서 더 나은 결과를 냈고, AbbVie가 Rinvoq·Skyrizi 합산 매출을 2027년 310억 달러 이상으로 기대한다고 보도했다. ([Reuters][16])

### 반례

반대로 후속 신약 전환이 안 되면 오리지널 제약사는 특허만료 후 매출 erosion이 크게 올 수 있다. Humira 바이오시밀러가 92% 할인 가격으로 제공되는 사례는 특허만료 후 pricing power가 얼마나 빨리 약해질 수 있는지를 보여준다. ([Reuters][1])

### 점수비중 v2.0

```text
EPS/FCF: 19
Structural Visibility: 18
Bottleneck/Pricing: 8
Market Mispricing: 13
Valuation Rerating: 11
Capital Allocation: 2
Information Confidence: 6
Risk Penalty: patent_cliff / biosimilar_erosion / pipeline_failure / pricing_pressure
```

### 정규화 교정

```text
점수 강화:
- 후속 신약 매출 성장
- 기존 블록버스터 의존도 하락
- pipeline 다변화
- pricing pressure 방어
- EPS/FCF 유지

점수 제한:
- 특허만료 의존도 큼
- biosimilar erosion 빠름
- 후속 신약 부재
- 가격 할인 압박
```

**핵심:**
오리지널 제약사는 **후속 신약 전환 성공 시 Watch-to-Green**, 실패하면 4C다.

---

# 8. PHARMA_PLATFORM_REGULATORY_RISK

## 의료 마케팅 / 불법 조제약 / 온라인 약국 / 안전성

### 핵심 구조

```text
대형 약물 수요
→ 온라인 처방·telehealth·조제약 확산
→ 접근성 증가
→ 동시에 규제·안전·품질 리스크
```

비만치료제처럼 수요가 폭발하는 약물에서는 판매채널과 조제약 이슈가 매우 중요하다.

### 반례

Novo Nordisk는 Wegovy 판매 둔화와 compounded alternative 확산이 2025년 전망 하향의 원인 중 하나였다고 Reuters가 보도했다. 즉 대형 약물 수요가 있어도, 규제 회색지대의 조제약·가격·접근성 문제가 원제약사의 매출과 valuation을 흔들 수 있다. ([Reuters][5])

또 FDA는 semaglutide sodium/acetate 같은 일부 compounded semaglutide formulations의 안전성과 효과가 입증되지 않았다고 경고한 바 있고, 불법 온라인 약국 문제도 존재한다. 이런 구조는 GLP-1 관련 플랫폼·제약·유통기업에서 safety/regulatory risk를 강하게 봐야 한다. ([위키백과][17])

### 점수비중 v2.0

```text
EPS/FCF: 17
Structural Visibility: 15
Bottleneck/Pricing: 8
Market Mispricing: 12
Valuation Rerating: 10
Capital Allocation: 0
Information Confidence: 6
Risk Penalty: FDA_warning / compounding_quality / illegal_pharmacy / advertising_rule / liability
```

### 정규화 교정

```text
점수 강화:
- 합법적 처방·유통채널
- 보험·약국 네트워크
- 규제 명확성
- 안전성·품질관리
- 반복 처방 매출

점수 제한:
- 불법 온라인 약국
- 조제약 품질 불확실
- 광고·홍보 규제
- 안전성 이슈
```

**핵심:**
약물 수요가 커져도 판매채널이 회색이면 Green 금지. 규제·품질·책임 리스크를 강하게 둔다.

---

# Round 29 점수비중 요약표

| Archetype                      | EPS/FCF | Visibility | Bottleneck | Mispricing | Valuation | Capital | 핵심 리스크                         |
| ------------------------------ | ------: | ---------: | ---------: | ---------: | --------: | ------: | ------------------------------ |
| BIOSIMILAR_COMMERCIALIZATION   |      18 |         20 |          6 |         13 |        11 |       0 | 가격경쟁, PBM, 처방전환                |
| OBESITY_GLP1_COMMERCIALIZATION |      22 |         20 |         12 |         13 |        12 |       0 | 경쟁, 보험, 조제약                    |
| GENE_THERAPY_RARE_DISEASE      |       8 |         12 |          8 |         10 |         6 |       0 | 상업화 지연, cash burn              |
| AI_DRUG_DISCOVERY_PLATFORM     |       6 |         10 |          7 |         12 |         6 |       0 | 임상실패, 매출 부재                    |
| CONTACT_CENTER_AI_AUTOMATION   |      19 |         20 |          8 |         14 |        13 |       0 | churn, IT예산, 개인정보              |
| SERVICE_KIOSK_SELF_CHECKOUT    |      17 |         15 |          7 |         12 |        10 |       0 | 절도, 고객불만, 일회성 장비               |
| BIOSIMILAR_ORIGINATOR_DEFENSE  |      19 |         18 |          8 |         13 |        11 |       2 | patent cliff, pipeline failure |
| PHARMA_PLATFORM_REGULATORY     |      17 |         15 |          8 |         12 |        10 |       0 | 조제약, 광고규제, 안전성                 |

---

# cases_v17 추가 후보

```text
BIOSIMILAR_COMMERCIALIZATION:
- humira_biosimilar_discount_access_candidate
- humira_biosimilar_slow_uptake_counterexample
- ustekinumab_biosimilar_multi_approval_candidate
- biosimilar_price_margin_pressure_4c

OBESITY_GLP1_COMMERCIALIZATION:
- lilly_oral_glp1_foundayo_candidate
- novo_wegovy_slowdown_compounded_alternative_4c
- glp1_advertising_regulation_india_counterexample
- oral_glp1_uptake_below_expectation_counterexample

GENE_THERAPY_RARE_DISEASE:
- bluebird_gene_therapy_approval_but_cash_crunch_4c
- rare_disease_reimbursement_delay_counterexample
- gene_therapy_patient_uptake_slow_counterexample
- gene_therapy_commercialization_success_candidate_if_reimbursement

AI_DRUG_DISCOVERY_PLATFORM:
- recursion_exscientia_ai_drug_platform_candidate
- ai_drug_no_approved_product_counterexample
- ai_drug_cash_burn_counterexample
- ai_drug_big_pharma_milestone_candidate

CONTACT_CENTER_AI_AUTOMATION:
- five9_contact_center_software_candidate
- minerva_cq_agent_assist_case_candidate
- contact_center_ai_no_arr_counterexample
- ai_customer_service_privacy_error_4c

SERVICE_KIOSK_SELF_CHECKOUT:
- computer_vision_self_checkout_candidate
- self_checkout_theft_counterexample
- pseudo_automation_workload_counterexample
- kiosk_one_off_hardware_counterexample

BIOSIMILAR_ORIGINATOR_DEFENSE:
- abbvie_rinvoq_skyrizi_successor_candidate
- humira_biosimilar_erosion_counterexample
- patent_cliff_no_successor_4c
- pipeline_transition_success_case

PHARMA_PLATFORM_REGULATORY:
- compounded_glp1_quality_risk_4c
- online_pharmacy_illegal_risk_counterexample
- legal_telehealth_prescription_channel_candidate
- pharma_advertising_regulation_4c
```

---

# 이번 라운드 핵심 교정

```text
1. 바이오시밀러는 허가만으로 Green 금지.
   실제 처방전환, PBM/보험 등재, 마진 방어가 필요하다.

2. 비만치료제/GLP-1은 구조적 성장성이 있지만 경쟁·보험·조제약·광고규제가 강한 감점축이다.

3. 유전자치료제/희귀질환은 승인 후에도 상업화가 느리면 무너질 수 있다.
   Bluebird 사례 때문에 Green을 매우 보수적으로.

4. AI 신약개발은 아직 대부분 Watch/Red.
   AI 플랫폼보다 임상 성공·milestone·승인 가능성이 핵심.

5. 컨택센터 AI는 반복 SaaS와 ROI가 있으면 Watch-to-Green 가능.
   PoC나 AI 상담 테마만으로는 부족하다.

6. 키오스크/셀프체크아웃은 절도·고객불만·pseudo-automation 문제가 있어 Green 제한.

7. 오리지널 제약사는 특허만료 후 후속 신약 전환 성공 여부가 핵심이다.

8. 약물 플랫폼·telehealth·조제약은 접근성 확대와 동시에 규제·품질·책임 리스크가 크다.
```

---

# 현재 판단

이번 라운드로 바이오·헬스케어와 서비스 자동화 쪽 점수비중이 훨씬 더 현실적으로 보정됐다.

특히 중요한 변화는:

```text
- 바이오시밀러: 허가 뉴스 → 실제 처방·마진 중심으로 보정
- GLP-1: 시장 크기 → 경쟁·보험·조제약 리스크 반영
- 유전자치료제: 승인 → 상업화·환급·cash runway 중심으로 보정
- AI 신약개발: 플랫폼 narrative → 임상·milestone·승인 중심으로 보정
- 컨택센터 AI: AI 기능 → ARR·seat·ROI 중심으로 보정
- 키오스크: 자동화 narrative → theft·고객경험·유지보수 중심으로 보정
```

이제 점수비중 가설은 **v2.0 수준**으로 꽤 두꺼워졌다.
그래도 마지막은 변하지 않는다.

```text
cases_v17 반영
→ stage date 후보 설정
→ price path backfill
→ MFE/MAE/drawdown 계산
→ score-price alignment
→ shadow scoring
→ 틀린 archetype 재교정
```

즉 지금까지 쌓은 건 **점수비중의 지도**이고, 다음에는 이 지도가 실제 주가 경로와 맞는지 검증해야 한다.

[1]: https://www.reuters.com/business/healthcare-pharmaceuticals/boehringer-goodrx-partner-offer-humira-rival-92-discount-2024-07-18/?utm_source=chatgpt.com "Boehringer-GoodRx partner to offer Humira rival at 92% discount"
[2]: https://en.wikipedia.org/wiki/Ustekinumab?utm_source=chatgpt.com "Ustekinumab"
[3]: https://www.reuters.com/legal/litigation/lillys-obesity-pill-tops-7000-prescriptions-fourth-week-signals-modest-uptake-2026-05-08/?utm_source=chatgpt.com "Lilly's obesity pill tops 7,000 prescriptions in fourth week, signals modest uptake"
[4]: https://www.reuters.com/legal/litigation/patients-dont-regain-much-weight-switching-injections-lillys-weight-loss-pill-2026-05-12/?utm_source=chatgpt.com "Patients don't regain much weight switching from injections to Lilly's weight-loss pill, study finds"
[5]: https://www.reuters.com/business/healthcare-pharmaceuticals/obesity-drugmaker-novo-nordisk-cuts-2025-outlook-posts-q1-profit-above-forecast-2025-05-07/?utm_source=chatgpt.com "Novo Nordisk cuts 2025 outlook as Wegovy obesity drug sales slow"
[6]: https://www.reuters.com/business/healthcare-pharmaceuticals/lilly-halts-india-obesity-awareness-campaign-after-regulatory-scrutiny-seeks-2026-05-11/?utm_source=chatgpt.com "Lilly halts India obesity awareness campaign after regulatory scrutiny, seeks rules clarity"
[7]: https://www.reuters.com/markets/deals/bluebird-bio-be-taken-private-by-carlyle-sk-capital-amid-cash-crunch-2025-02-21/?utm_source=chatgpt.com "Gene therapy maker bluebird to go private in discounted deal amid cash crunch"
[8]: https://www.reuters.com/markets/deals/biotech-firm-recursion-buy-smaller-peer-exscientia-688-million-2024-08-08/?utm_source=chatgpt.com "Biotech firm Recursion to buy smaller peer Exscientia for $688 million"
[9]: https://www.wired.com/story/artificial-intelligence-drug-discovery?utm_source=chatgpt.com "Where Are All the AI Drugs?"
[10]: https://www.ft.com/content/9a8aee4e-9cf6-4bb3-b7ea-d95ddd0d5e79?utm_source=chatgpt.com "Why is AI struggling to discover new drugs?"
[11]: https://www.reuters.com/markets/us/anson-funds-pushing-five9-explore-sale-sources-say-2024-07-11/?utm_source=chatgpt.com "Anson Funds pushing Five9 to explore a sale, sources say"
[12]: https://arxiv.org/abs/2509.12589?utm_source=chatgpt.com "Redefining CX with Agentic AI: Minerva CQ Case Study"
[13]: https://arxiv.org/abs/2407.21308?utm_source=chatgpt.com "Enhanced Self-Checkout System for Retail Based on Improved YOLOv10"
[14]: https://www.theguardian.com/business/2024/feb/04/self-checkout-theft-security?utm_source=chatgpt.com "Self-checkout is turning us into thieves - but it's not our fault"
[15]: https://arxiv.org/abs/2410.02888?utm_source=chatgpt.com "Pseudo-Automation: How Labor-Offsetting Technologies Reconfigure Roles and Relationships in Frontline Retail Work"
[16]: https://www.reuters.com/business/healthcare-pharmaceuticals/abbvies-rinvoq-shows-superiority-over-humira-head-to-head-study-2025-10-20/?utm_source=chatgpt.com "AbbVie's Rinvoq shows superiority over Humira in head-to-head arthritis study"
[17]: https://en.wikipedia.org/wiki/Semaglutide?utm_source=chatgpt.com "Semaglutide"
