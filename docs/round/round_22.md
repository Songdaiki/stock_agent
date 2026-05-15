맞아. **A를 계속 진행하면서, 내가 성공/반례를 더 채우고 그때마다 archetype별 점수비중을 계속 교정하는 방식이 제일 맞다.**

이번은 **Round 16: 얇았던 archetype + 주요 archetype 재보정 라운드**로 정리할게. 핵심은 여전히 이거야.

> **성공사례는 점수축을 강화한다.
> 반례는 Green gate와 risk penalty를 강화한다.
> 주가검증은 그 점수비중이 실제 시장에서 맞았는지 확인하는 계기판이다.**

그리고 기존 정신은 절대 버리면 안 돼. 서생원식 에이전트는 테마봇이 아니라, **산업 구조 변화 → EPS/FCF 체급 변화 → 시장의 과거 프레임 오해 → 밸류에이션 리레이팅**을 찾는 시스템이어야 해.
실제 점수도 테마명이 아니라 공시·리포트·가격·재무 증거에서 나와야 하고, 계약금액·계약기간·매출 대비 계약금액 같은 필드는 확인된 값만 써야 한다. 없는 숫자를 만들어서 scoring에 넣으면 안 된다.

---

# Round 16에서 더 채운 Archetype

이번에 더 파고든 쪽은 아래 10개야.

```text
1. SECURITIES_BROKERAGE_CYCLE
2. INSURANCE_UNDERWRITING_CYCLE
3. EDUCATION_SPECIALTY_SERVICES
4. RETAIL_CONVENIENCE_OFFLINE / ECOMMERCE_FRESH_LOGISTICS
5. BUILDING_MATERIALS_CYCLE / REIT_DEVELOPMENT_TRUST
6. CLOUD_AI_SOFTWARE_INFRA
7. CRO_CLINICAL_SERVICE
8. APPAREL_BRAND_OEM
9. MEMORY_HBM_CAPACITY 4B 보정
10. VALUE_UP_SHAREHOLDER_RETURN / HOLDING_GOVERNANCE 보정
```

---

# 1. SECURITIES_BROKERAGE_CYCLE

증권사 / VC / 거래대금 / IB / IPO

## 핵심 구조

```text
거래대금 증가
→ 브로커리지 수수료 증가
→ IPO/IB 회복
→ 자기자본 운용성과
→ ROE 개선
```

증권사는 은행·보험과 다르게 **거래대금, 시장 turnover, IB pipeline, 부동산 PF 노출, 자기자본 운용 리스크**가 핵심이야. 특히 최근 한국·대만·일본 등 아시아 증시에 헤지펀드 매수가 크게 들어오고, 반도체·하드웨어 쪽으로 자금이 몰렸다는 보도는 증권사 브로커리지/시장활동 회복의 Stage 1 신호가 될 수 있어. 다만 이건 아직 “거래대금 이벤트”일 뿐, 증권사 EPS 체급 변화로 이어지는지는 따로 봐야 한다. ([Reuters][1])

## 성공 후보

```text
- 거래대금 증가 + 브로커리지 수익 증가 증권사
- IPO/ECM/DCM pipeline 회복 증권사
- 자본비율 안정 + 배당/자사주 가능한 대형 증권사
- VC 회수시장 회복 기업
```

## 반례

```text
- 거래대금 단기 급증 후 소멸
- 부동산 PF/대체투자 손실
- 자기자본 운용손실
- IPO 시장 회복 기대만 있고 실적 없음
- VC 회수시장 막힘
```

## Stage 기준

```text
Stage 1:
거래대금 증가
증시 랠리
IPO/IB 회복 기대
value-up 수혜 기대

Stage 2:
브로커리지 수익 증가
IB fee 증가
자본비율 안정
OP/EPS 상향

Stage 3:
반복적 거래대금/IB 회복
부동산 PF 리스크 낮음
ROE 구조 개선
주주환원 가능성

4B:
시장 거래대금 peak
증권주 동반 과열
IPO 기대 선반영

4C:
거래대금 급감
PF 손실
자기자본 운용손실
자본비율 악화
```

## 점수비중 v0.7

```text
EPS/FCF: 18
Structural Visibility: 14
Bottleneck/Pricing: 5
Market Mispricing: 15
Valuation Rerating: 18
Capital Allocation: 8
Information Confidence: 5
Risk Penalty: market_turnover / PF / proprietary_loss
```

## 정규화 포인트

증권사는 **Green보다는 Watch 중심**이 맞아. 거래대금이 폭발하면 EPS도 튈 수 있지만, 지속성이 낮다. 따라서 `structural_visibility`는 은행·보험보다 낮게, `valuation_rerating`과 `capital_allocation`은 중간 이상으로 둔다.

---

# 2. INSURANCE_UNDERWRITING_CYCLE

손해보험 / 생명보험 / 보증보험 / 화재

## 핵심 구조

```text
손해율 안정
→ CSM / ROE 개선
→ 자본비율 안정
→ 주주환원
→ PBR-ROE 프레임 리레이팅
```

보험은 금융주 안에서도 은행과 다르게 봐야 해. 은행은 NIM·CET1·충당금이 중요하고, 보험은 **손해율, CSM, K-ICS, 배당가능이익, 자사주/배당**이 핵심이야.

보증보험 쪽은 보안·운영 리스크도 봐야 한다. 예컨대 SGI서울보증은 보증보험 사업 자체는 반복적이고 안정적인 수익성이 있을 수 있지만, 2025년에 랜섬웨어 공격으로 주요 서비스가 며칠간 중단됐다는 기록이 있어 금융 인프라/보험 archetype에서 사이버 운영 리스크도 같이 봐야 한다. ([위키백과][2])

## 성공 후보

```text
- 삼성화재 / DB손보: 손해율 안정, ROE, 자본비율, 주주환원
- 생명보험사: CSM, 금리, 자본비율, 배당여력
- 보증보험/특수보험: 반복 보증료, 신용 리스크, 사이버 운영 리스크
```

## 반례

```text
- 단순 저PBR 보험주
- 손해율 악화
- 자본비율 낮아 환원 제한
- 사이버 장애/랜섬웨어
- 부동산 PF/대체투자 손실
```

## Stage 기준

```text
Stage 1:
저PBR
value-up 공시
손해율 개선
배당/자사주 기대

Stage 2:
ROE 개선
CSM 증가
K-ICS 안정
손해율 안정
환원정책 실행

Stage 3:
PBR-ROE 프레임 변화
반복 환원
보험 본업 수익성 안정
시장에 아직 value trap 프레임

4B:
PBR 정상화
모두가 보험 value-up 인정
환원 기대 과열

4C:
손해율 악화
자본비율 악화
사이버/운영 리스크
환원정책 후퇴
```

## 점수비중 v0.7

```text
EPS/FCF: 15
Structural Visibility: 21
Bottleneck/Pricing: 4
Market Mispricing: 15
Valuation Rerating: 25
Capital Allocation: 10
Information Confidence: 5
Risk Penalty: underwriting / capital_ratio / cyber_operational
```

## 정규화 포인트

보험은 **EPS 폭발형이 아니라 PBR-ROE-환원 리레이팅형**이다. 따라서 `valuation_rerating`과 `capital_allocation` 비중을 높이고, `bottleneck_pricing`은 낮게 둔다.

---

# 3. EDUCATION_SPECIALTY_SERVICES

교육 / 입시 / 취업 / 키즈 / 에듀테크

## 핵심 구조

```text
반복 수강
→ 가격 결정력
→ 온라인/성인/해외 확장
→ OPM·FCF 개선
```

한국 교육시장은 사교육 수요가 강하지만, 동시에 저출산과 규제 리스크가 너무 크다. 한국의 학원 구조는 학생 참여율이 높고 지출도 크지만, 이 자체는 교육기업 Stage 1 신호일 뿐이야. 장기적으로는 학생 수 감소와 규제가 구조적 리스크다. ([위키백과][3])

## 성공 후보

```text
- 메가스터디교육: 입시 반복수강, 가격 결정력, 온라인 강의
- 성인교육/자격시험 플랫폼: 저출산 리스크를 상쇄할 수 있음
- B2B 교육/기업교육: 반복계약이면 Watch-to-Green 가능
```

## 반례

```text
- 유아·키즈 중심 기업: 저출산 직접 타격
- 사교육 규제
- 단기 입시제도 변경 테마
- AI 튜터 경쟁으로 가격 하락
- 오프라인 학원 고정비 부담
```

## Stage 기준

```text
Stage 1:
입시제도 변화
수강생 증가
가격 인상
교육비 증가

Stage 2:
반복매출
OPM 개선
온라인/성인교육 확장
FCF 개선

Stage 3:
저출산 리스크를 성인/해외/프리미엄 확장으로 상쇄
가격 결정력
시장에 아직 전통 학원 프레임

4B:
입시 테마 과열
정책 기대 선반영

4C:
사교육 규제
학생 수 감소
가격 인하
AI 대체
```

## 점수비중 v0.7

```text
EPS/FCF: 18
Structural Visibility: 17
Bottleneck/Pricing: 5
Market Mispricing: 12
Valuation Rerating: 12
Capital Allocation: 2
Information Confidence: 5
Risk Penalty: birthrate / regulation / AI_substitution
```

## 정규화 포인트

교육은 **Watch 중심**이다. Green을 주려면 단순 입시가 아니라 성인교육·해외·B2B·구독형 반복매출로 저출산 리스크를 상쇄해야 한다.

---

# 4. RETAIL_CONVENIENCE_OFFLINE / ECOMMERCE_FRESH_LOGISTICS

편의점 / 이커머스 / 홈쇼핑 / 콜드체인

## 핵심 구조

```text
점포 효율 / PB상품 / 물류망
→ same-store sales
→ 비용 레버리지
→ OPM·FCF 개선
```

편의점은 방어적 반복수요가 있지만, Green을 쉽게 줄 정도로 폭발성이 크진 않다. GS25는 2024년 말 기준 전국 18,000개 이상 점포를 가진 대형 편의점 네트워크로 정리되지만, 점포 수 자체가 점수 근거는 아니고 **점포당 수익성, PB mix, 비용 레버리지**가 중요하다. ([위키백과][4])

이커머스와 홈쇼핑은 더 조심해야 한다. 한국 이커머스는 중국 직구와 가격 경쟁이 강해지고, 물류비·배송비·재고 폐기 부담이 커질 수 있어. 따라서 매출 성장보다 OPM/FCF를 봐야 한다.

## 성공 후보

```text
- 편의점: PB mix, 점포 효율, OPM 개선
- 콜드체인: 의약품/신선식품 반복 물류계약
- 음식료 유통: 물류비 안정, 고마진 mix
```

## 반례

```text
- 홈쇼핑 구조 둔화
- 신선식품 e-commerce 적자 지속
- 상장 기대만 있는 관련주
- 중국 직구/저가 e-commerce 압박
- 물류비 상승
```

## Stage 기준

```text
Stage 1:
same-store sales 회복
점포 확대
PB상품 뉴스
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
시장에 내수 저성장 유통 프레임

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

## 점수비중 v0.7

```text
EPS/FCF: 18
Structural Visibility: 16
Bottleneck/Pricing: 5
Market Mispricing: 13
Valuation Rerating: 14
Capital Allocation: 3
Information Confidence: 5
Risk Penalty: inventory / logistics_cost / competition
```

## 정규화 포인트

편의점은 Watch-to-Green 가능, 이커머스·홈쇼핑은 Watch 중심. **매출 성장보다 OPM/FCF**를 우선한다.

---

# 5. BUILDING_MATERIALS_CYCLE / REIT_DEVELOPMENT_TRUST

건자재 / 시멘트 / 철근 / 리츠

## 핵심 구조

```text
착공량 / 가격인상 / 원가 / 금리
→ OPM·배당·FCF
```

건자재와 리츠는 건설 PF와 금리에 민감해. 삼표, 한일시멘트, 아세아시멘트 같은 기업들은 cement/concrete 생산능력과 시장지위를 가지고 있지만, 이 자체가 Green 근거는 아니야. 실제 점수는 **가격인상, 출하량, 원가, PF 리스크, 착공량**에서 나온다. ([위키백과][5])

## 성공 후보

```text
- 시멘트 가격 인상 + 원가 안정
- 철근 spread 개선
- 출하량 회복
- 리츠 금리 하락 + 배당 안정
```

## 반례

```text
- PF 부실
- 착공 감소
- 원가 상승
- 공실률 상승
- 배당 삭감
```

## Stage 기준

```text
Stage 1:
가격 인상
착공 회복
금리 하락
배당 매력

Stage 2:
OPM 개선
출하량 회복
원가 안정
배당 안정

Stage 3:
공급 재편
가격협상력
반복 임대수익
부채 리스크 낮음

4B:
부동산 회복 기대 선반영
배당주 과열

4C:
PF 부실
착공 감소
공실률 증가
배당 삭감
원가 상승
```

## 점수비중 v0.7

```text
EPS/FCF: 17
Structural Visibility: 12
Bottleneck/Pricing: 12
Market Mispricing: 12
Valuation Rerating: 12
Capital Allocation: 5
Information Confidence: 5
Risk Penalty: credit / rates / vacancy / PF
```

## 정규화 포인트

건자재/리츠는 **Green 제한**이 맞다. 가격인상과 출하량이 좋아져도 PF·금리·공실·배당 리스크가 있으면 Stage 2~Watch에 머문다.

---

# 6. CLOUD_AI_SOFTWARE_INFRA

클라우드 / ERP / B2B SaaS / 컨택센터

## 핵심 구조

```text
반복 소프트웨어 매출
→ 고객 lock-in
→ ARPU / OPM 개선
→ FCF 개선
```

더존비즈온은 이 archetype의 좋은 기준 케이스야. EQT는 더존비즈온 지분 37.6%를 약 9.3억 달러에 인수하기로 했고, Reuters는 더존비즈온이 한국 중소기업 대상 클라우드 ERP·회계·세무·컴플라이언스 소프트웨어를 제공한다고 설명했다. 이건 단순 AI 테마가 아니라 **반복 B2B 소프트웨어 매출 + 운영 개선 가능성**을 보는 Stage 1~2 사례다. ([Reuters][6])

## 성공 후보

```text
- 더존비즈온: ERP/SaaS 반복매출
- B2B 보안·컨택센터 SaaS
- 클라우드 전환으로 OPM 개선되는 기업
```

## 반례

```text
- AI 기능만 추가하고 FCF 훼손
- 클라우드 비용 증가
- 고객 이탈
- SI성 매출만 있고 SaaS 전환 없음
- 원격근무 테마만 있고 반복매출 없음
```

## Stage 기준

```text
Stage 1:
클라우드 전환
ERP/SaaS 수요
AI 기능 도입
B2B 고객 증가

Stage 2:
반복매출 증가
ARPU 상승
OPM 개선
고객 retention 확인

Stage 3:
고객 lock-in
높은 FCF conversion
가격 인상 가능
시장에 아직 전통 SW 프레임

4B:
SaaS/AI SW narrative 과열
multiple 포화

4C:
고객 이탈
AI 비용 과다
OPM 하락
경쟁 심화
```

## 점수비중 v0.7

```text
EPS/FCF: 20
Structural Visibility: 23
Bottleneck/Pricing: 8
Market Mispricing: 16
Valuation Rerating: 14
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: AI_cost / churn / margin
```

## 정규화 포인트

클라우드/SaaS는 Green 가능. 하지만 AI 키워드가 아니라 **반복매출·OPM·FCF**가 핵심이다.

---

# 7. CRO_CLINICAL_SERVICE

CRO / 임상시험수탁 / 임상서비스

## 핵심 구조

```text
제약·바이오 R&D
→ 임상시험 수탁
→ 반복 서비스 매출
→ 고객사 다변화
```

CRO는 pre-revenue biotech이 아니라 서비스 기업에 가깝다. ICON은 글로벌 CRO로 2024년 기준 55개국, 4만 명 이상 인력을 가진 대형 clinical research organization이며, 2024년 매출도 82억 달러 이상으로 정리된다. 이건 scale과 고객사 다변화가 CRO의 핵심이라는 기준 사례가 된다. ([위키백과][7])

Medpace는 중소형 CRO 성공사례로 좋다. Medpace는 2020년 9.3억 달러 매출에서 2024년 21.1억 달러 매출로 성장했고, 순이익도 2024년 4억 달러 수준으로 정리된다. 즉 CRO가 실제 매출·이익으로 성장하면 Watch-to-Green 가능성이 있다. ([위키백과][8])

## 성공 후보

```text
- ICON: 글로벌 CRO scale
- Medpace: 매출·이익 성장형 CRO
- 국내 CRO: 고객사 다변화와 수주잔고가 있으면 후보
```

## 반례

```text
- 바이오 funding crunch
- 임상 축소
- 단일 고객 의존
- 수주잔고는 있으나 마진 낮음
```

## Stage 기준

```text
Stage 1:
임상 건수 증가
제약 R&D 증가
수주잔고 증가

Stage 2:
매출/OP 증가
고객사 다변화
반복 서비스 매출

Stage 3:
다년 수주잔고
고객사 포트폴리오 다변화
높은 FCF conversion

4B:
바이오 R&D 기대 과열

4C:
임상 축소
고객사 예산 삭감
수주 취소
```

## 점수비중 v0.7

```text
EPS/FCF: 18
Structural Visibility: 20
Bottleneck/Pricing: 8
Market Mispricing: 12
Valuation Rerating: 12
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: biotech_funding_cycle / customer_concentration
```

## 정규화 포인트

CRO는 CDMO보다 약하지만, pre-revenue biotech보다 훨씬 점수화 가능하다. **수주잔고와 고객 다변화**가 핵심이다.

---

# 8. APPAREL_BRAND_OEM

의류 브랜드 / 의류 OEM·ODM / 의류소재

## 핵심 구조

```text
브랜드 / 수출 / 고객사 주문
→ 재고 회전
→ 할인율 통제
→ OPM·FCF 개선
```

의류는 K푸드/K뷰티보다 훨씬 더 유행성과 재고 리스크가 크다. 따라서 Green을 훨씬 보수적으로 줘야 해.

## 성공 후보

```text
- 글로벌 채널이 열리는 K패션 브랜드
- 고객사 다변화된 OEM·ODM
- 재고 회전 빠르고 할인율 낮은 브랜드
```

## 반례

```text
- 단일 유행 브랜드
- 재고 증가
- 할인 판매 증가
- 중국/단일 채널 의존
- OEM 고객사 주문 둔화
```

## Stage 기준

```text
Stage 1:
해외 팝업
K패션 협업
주문 증가
셀럽·IP 콜라보

Stage 2:
해외 매출 증가
재고 회전 안정
OPM 개선
고객사 다변화

Stage 3:
브랜드 반복 구매
글로벌 채널 확장
FCF 개선
시장에 아직 내수 패션 프레임

4B:
브랜드 hype 과열
재고 리스크 확대

4C:
재고 증가
할인 판매
채널 둔화
주문 취소
```

## 점수비중 v0.7

```text
EPS/FCF: 18
Structural Visibility: 16
Bottleneck/Pricing: 8
Market Mispricing: 14
Valuation Rerating: 12
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: inventory / markdown / fashion_cycle / channel_concentration
```

## 정규화 포인트

의류는 Watch 중심. Green 가능하려면 K뷰티처럼 **반복 채널 + 재고 안정 + OPM 개선**이 필요하다.

---

# 9. MEMORY_HBM_CAPACITY — 4B 기준 재보정

## 핵심 구조

```text
AI 수요
→ HBM/DRAM/NAND 병목
→ 장기계약·선수금·가격밴드
→ EPS/FCF 다년 상향
→ 시클리컬 할인 제거
```

SK하이닉스는 구조적 성공사례이면서 동시에 4B-watch의 기준 사례다. 2026년 현재 SK하이닉스는 AI 수요에 힘입어 시총 1조 달러에 근접했고, 2025년에 274%, 2026년에 200% 이상 주가가 상승했다는 보도가 있다. 이건 Stage 3 성공 후 **리레이팅이 충분히 반영된 4B-watch**를 정의하는 데 중요하다. ([Reuters][9])

## Stage 3 조건

```text
HBM 수요
DRAM/NAND 가격 상승
공급규율
장기계약/선수금/price band
CAPA constraint
multiple-year consensus revision
PBR에서 PER 프레임 전환
```

## 4B 조건

```text
주가 1~2년 급등
시총/멀티플 포화
고객사 가격 저항
CAPEX 증설 뉴스
모두가 AI memory rerating을 인정
헤지펀드/글로벌 자금 crowded
```

최근 Morgan Stanley가 한국·일본·대만 equities에 10년 내 최대 규모의 hedge fund weekly buying이 있었다고 보도한 점도, 반도체/하드웨어 쪽 crowding을 4B-watch 보조지표로 쓸 수 있다. ([Reuters][1])

## 점수비중 v0.7

```text
EPS/FCF: 24
Structural Visibility: 21
Bottleneck/Pricing: 19
Market Mispricing: 15
Valuation Rerating: 12
Capital Allocation: 0
Information Confidence: 5
Risk Penalty: cycle / capex_reversal / crowding
```

## 정규화 포인트

HBM은 Green 가능성이 높다. 하지만 주가가 이미 1~2년 폭등하고 글로벌 자금이 crowding되면 4B-watch를 강하게 켜야 한다.

---

# 10. VALUE_UP_SHAREHOLDER_RETURN / HOLDING_GOVERNANCE

## 핵심 구조

```text
저PBR / NAV discount
→ 자사주·소각·배당
→ 지배구조 개선
→ PBR-ROE 또는 NAV 프레임 리레이팅
```

한국 정부가 배당 확대를 유도하기 위해 세제 개편을 추진하고, “Korea discount” 해소를 목표로 주주보호와 자본시장 개혁을 밀고 있다는 보도는 value-up archetype의 Stage 1 배경이 된다. 다만 정책 자체만으로 Green은 아니다. 실제 환원정책과 ROE/FCF가 따라와야 한다. ([Reuters][10])

## 성공 후보

```text
- SK스퀘어: NAV discount, 자사주 소각, SK하이닉스 exposure
- 삼성물산/삼성생명: 자산가치와 지배구조 이슈
- 금융지주/보험: ROE-PBR-환원 프레임
```

## 반례

```text
- 자사주 매입 후 미소각
- 이벤트성 경영권 분쟁
- ROE 낮은 저PBR주
- 지배주주 리스크
- 환원정책 후퇴
```

## Stage 기준

```text
Stage 1:
value-up 공시
자사주/배당
저PBR
거버넌스 개혁 뉴스

Stage 2:
실제 소각
반복 환원정책
ROE 개선
NAV discount 축소 가능성

Stage 3:
PBR-ROE 또는 NAV 프레임 변화
반복 환원
지배구조 할인 완화

4B:
모두가 value-up 성공주로 인정
PBR 정상화
이벤트 프리미엄 반영 완료

4C:
환원 미이행
자회사 가치 훼손
credit cost 증가
지배주주 리스크 재부각
```

## 점수비중 v0.7

```text
EPS/FCF: 12~15
Structural Visibility: 18~20
Bottleneck/Pricing: 4~5
Market Mispricing: 20
Valuation Rerating: 25
Capital Allocation: 10
Information Confidence: 5
Risk Penalty: governance / execution / credit
```

## 정규화 포인트

Value-up은 Green 가능하지만, **정책 기대가 아니라 실제 소각·배당·ROE·NAV discount 축소**가 있어야 한다.

---

# cases_v04 추가 후보

이번 라운드에서 cases_v04에 추가할 후보는 이렇게 정리하면 된다.

```text
SECURITIES_BROKERAGE_CYCLE:
- korea_brokerage_trading_value_rally_candidate
- securities_pf_loss_4c
- ipo_pipeline_recovery_candidate
- vc_exit_market_weakness_counterexample

INSURANCE_UNDERWRITING_CYCLE:
- samsung_fire_underwriting_valueup_candidate
- db_insurance_loss_ratio_candidate
- low_pbr_insurer_no_capital_return_counterexample
- sgi_ransomware_operational_risk_4c

EDUCATION_SPECIALTY_SERVICES:
- megastudy_private_education_candidate
- adult_education_subscription_candidate
- low_birthrate_kids_education_counterexample
- education_regulation_4c

RETAIL_ECOMMERCE_LOGISTICS:
- convenience_store_pb_efficiency_candidate
- cold_chain_recurring_logistics_candidate
- ecommerce_fresh_loss_counterexample
- home_shopping_structural_decline_counterexample

BUILDING_MATERIALS_REIT:
- cement_price_hike_candidate
- reit_rate_cut_dividend_candidate
- pf_delinquency_building_materials_4c
- vacancy_dividend_cut_reit_4c

CLOUD_AI_SOFTWARE_INFRA:
- douzone_bizon_cloud_erp_candidate
- ai_feature_no_fcf_counterexample
- cloud_cost_margin_pressure_4c
- saas_churn_counterexample

CRO_CLINICAL_SERVICE:
- icon_global_cro_scale_candidate
- medpace_growth_cro_candidate
- biotech_funding_crunch_4c
- customer_budget_cut_cro_counterexample

APPAREL_BRAND_OEM:
- kfashion_global_channel_candidate
- apparel_oem_customer_diversification_candidate
- inventory_markdown_4c
- fashion_cycle_single_brand_counterexample

MEMORY_HBM_CAPACITY:
- sk_hynix_hbm_success_case
- sk_hynix_4b_crowding_watch
- simple_dram_rebound_counterexample
- ai_capex_cut_memory_4c

VALUE_UP_SHAREHOLDER_RETURN:
- sk_square_nav_discount_candidate
- financial_valueup_pbr_roe_candidate
- buyback_no_cancel_counterexample
- low_roe_value_trap_counterexample
```

---

# 이번 라운드 점수비중 요약

| Archetype                    | EPS/FCF | Visibility | Bottleneck | Mispricing | Valuation | Capital | 핵심         |
| ---------------------------- | ------: | ---------: | ---------: | ---------: | --------: | ------: | ---------- |
| SECURITIES_BROKERAGE_CYCLE   |      18 |         14 |          5 |         15 |        18 |       8 | 거래대금·IB·PF |
| INSURANCE_UNDERWRITING_CYCLE |      15 |         21 |          4 |         15 |        25 |      10 | 손해율·CSM·환원 |
| EDUCATION_SPECIALTY_SERVICES |      18 |         17 |          5 |         12 |        12 |       2 | 반복수강·저출산   |
| RETAIL_ECOMMERCE_LOGISTICS   |      18 |         16 |          5 |         13 |        14 |       3 | OPM·물류비    |
| BUILDING_MATERIALS_REIT      |      17 |         12 |         12 |         12 |        12 |       5 | PF·금리·공실   |
| CLOUD_AI_SOFTWARE_INFRA      |      20 |         23 |          8 |         16 |        14 |       0 | 반복매출·OPM   |
| CRO_CLINICAL_SERVICE         |      18 |         20 |          8 |         12 |        12 |       0 | 수주·고객다변화   |
| APPAREL_BRAND_OEM            |      18 |         16 |          8 |         14 |        12 |       0 | 재고·채널      |
| MEMORY_HBM_CAPACITY          |      24 |         21 |         19 |         15 |        12 |       0 | HBM·병목·4B  |
| VALUE_UP_SHAREHOLDER_RETURN  |   12~15 |      18~20 |        4~5 |         20 |        25 |      10 | ROE·PBR·소각 |

---

# 현재 정규화 판단

이번 라운드에서 중요한 교정은 이거야.

```text
1. 증권사는 Green보다 Watch 중심.
   거래대금은 강하지만 지속성이 약하므로 visibility를 낮게 둔다.

2. 보험은 은행보다 underwriting/CSM/자본비율을 본다.
   valuation과 capital allocation 비중을 높인다.

3. 교육은 저출산·규제 리스크 때문에 Green 제한.
   성인교육/해외/구독형이 있어야 올라간다.

4. 편의점/유통은 OPM과 FCF가 핵심.
   매출 성장만으로는 부족하다.

5. 건자재/리츠는 PF·금리·공실 리스크 때문에 Green 제한.

6. 클라우드/SaaS는 Green 가능.
   AI 키워드가 아니라 반복매출·OPM·FCF가 핵심.

7. CRO는 CDMO보다 약하지만 pre-revenue biotech보다 강하다.
   고객사 다변화와 backlog가 핵심.

8. 의류는 K푸드/K뷰티보다 보수적.
   재고·할인율·단일채널 리스크가 크다.

9. HBM은 Green 가능하지만 이미 큰 리레이팅 후에는 4B-watch 필요.

10. Value-up은 정책이 아니라 실제 환원과 ROE/PBR 정합성이 핵심.
```

다음 라운드에서는 이걸 기반으로 **cases_v04를 더 실제 JSONL 형태로 변환**하거나, 아직 얇은 `SERVICE_KIOSK_AUTOMATION`, `DIGITAL_HEALTHCARE_AI`, `RARE_METALS`, `RENEWABLE`, `AGRI_LIVESTOCK` 쪽을 더 파면 된다.

[1]: https://www.reuters.com/markets/wealth/hedge-funds-record-decade-high-weekly-buying-korea-japan-taiwan-equities-morgan-2026-05-12/?utm_source=chatgpt.com "Hedge funds record decade-high weekly buying in Korea, Japan, Taiwan equities, Morgan Stanley says"
[2]: https://en.wikipedia.org/wiki/Seoul_Guarantee_Insurance?utm_source=chatgpt.com "Seoul Guarantee Insurance"
[3]: https://en.wikipedia.org/wiki/Hagwon?utm_source=chatgpt.com "Hagwon"
[4]: https://en.wikipedia.org/wiki/GS25?utm_source=chatgpt.com "GS25"
[5]: https://en.wikipedia.org/wiki/Sampyo?utm_source=chatgpt.com "Sampyo"
[6]: https://www.reuters.com/world/asia-pacific/swedish-firm-eqt-shells-out-930-million-slice-south-koreas-douzone-bizon-2025-11-07/?utm_source=chatgpt.com "Swedish firm EQT shells out $930 million for a slice of South Korea's Douzone Bizon"
[7]: https://en.wikipedia.org/wiki/ICON_PLC?utm_source=chatgpt.com "ICON PLC"
[8]: https://en.wikipedia.org/wiki/Medpace?utm_source=chatgpt.com "Medpace"
[9]: https://www.reuters.com/world/asia-pacific/ai-boom-puts-sk-hynix-cusp-1-trillion-market-value-2026-05-14/?utm_source=chatgpt.com "AI boom puts SK Hynix on cusp of $1 trillion market value"
[10]: https://www.reuters.com/world/asia-pacific/south-korea-revamp-tax-scheme-boost-dividends-part-stock-market-reform-2025-06-11/?utm_source=chatgpt.com "South Korea to revamp tax scheme to boost dividends as part of stock market reform"
