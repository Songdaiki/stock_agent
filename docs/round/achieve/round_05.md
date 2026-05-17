응. 계속 확장하는 방향이 맞아. 지금은 **레포를 계속 패치하기보다, 내가 case matrix를 더 채우고 구조를 정교화한 뒤 한 번에 에이전트에 넣어 백테스트하는 단계**야.

현재 레포 28A는 뼈대는 잘 잡았지만 아직 `fixture_only: True`, mapped symbols 13개, archetypes used 8개 수준이고, 25개 archetype 중 “성공 2개 + 반례 2개” 조건을 충족한 archetype은 0개야. 그래서 최종 점수비중 적용은 아직 이르고, 케이스 라이브러리 확장이 먼저다.
기존 정신도 유지해야 해. 핵심은 **산업 구조 변화 → EPS/FCF 체급 변화 → 시장의 과거 프레임 → 밸류에이션 리레이팅 → 논리 훼손 전까지 보유**야. 단순 테마, 일회성 실적, 주가 급등만으로는 정통 E2R이 아니다.

이번 라운드는 **Round 5: 대섹터 체계 재정렬 + 빈 archetype 확장 + 점수-주가 정합성 검증 기준 추가**로 보면 돼.

---

# 1. 대섹터 분류를 먼저 다시 정리

전체 코스피·코스닥 2,600개 이상을 보려면 세부 업종 100개를 하나씩 튜닝하면 안 돼. 대신 이렇게 묶어야 해.

```text
대섹터
→ E2R Archetype
→ Stage별 증거
→ 섹터/아키타입 peer 정규화
→ 성공/반례 case로 검증
```

내가 보는 대섹터 체계는 이거야.

| 대섹터        | 포함 archetype                                                                | Green 허용도                           |
| ---------- | --------------------------------------------------------------------------- | ----------------------------------- |
| 산업재/수주     | Contract Backlog, Defense, Shipbuilding, AI Data Center Infra, Nuclear/Grid | 높음. 단, 계약질·마진·수주잔고 확인 필요            |
| 수출 소비재     | K-Food, K-Beauty, Medical Device, Consumer Export                           | 높음. 단, 반복수요·채널·OPM 필요               |
| 반도체/AI 인프라 | Memory/HBM, Semi Equipment, PCB/Packaging, Data Center Infra                | 높음. 단, CapEx cycle/4B 감시 필요         |
| 사이클/스프레드   | Shipping, Commodity, Battery Materials, Auto 일부                             | 중간~낮음. EPS 폭발 가능하지만 Green 제한        |
| 금융/자본배분    | Bank, Insurance, Brokerage, Holding/Governance                              | 중간. ROE/PBR/환원/거버넌스가 핵심             |
| 바이오/헬스케어   | Biotech Regulatory, Medical Device Export, CDMO                             | 분리 필요. 매출화 전 바이오 Green 제한           |
| 플랫폼/IP/서비스 | Platform, Software, Game, Content, Education, Specialty Services            | 중간. 반복매출·ARPU·OPM 없으면 Green 금지      |
| 내수/리오프닝    | Retail, Travel, Leisure, Domestic Consumer                                  | 낮음~중간. 경기 rebound와 구조적 E2R 분리       |
| 부동산/신용     | Construction, Real Estate, PF/Credit                                        | 낮음. PF/신용/현금흐름 우선                   |
| 테마/이벤트     | Robotics Theme, One-off Demand, Theme Overheat                              | Green 제한. Stage 1/2 또는 Red/4B 감시 중심 |

이렇게 대섹터를 잡아야 “전력기기에는 맞는데 네이버·바이오·건설·해운에는 엉망”인 상황을 줄일 수 있어.

---

# 2. 이번 라운드에서 추가로 확정할 Archetype

기존 25개에 더해, 실전에서는 아래를 별도 archetype 또는 sub-archetype으로 넣는 게 좋아.

```text
1. AI_DATA_CENTER_INFRASTRUCTURE
2. NUCLEAR_SMR_GRID_POLICY
3. TRAVEL_LEISURE_REOPENING
4. EDUCATION_SPECIALTY_SERVICES
5. RARE_METALS_STRATEGIC_MATERIALS
6. CDMO_HEALTHCARE_CONTRACT
7. VALUE_UP_SHAREHOLDER_RETURN
```

특히 **AI Data Center Infrastructure**는 전력기기 하나로 묶기엔 너무 넓어. 전력기기, 전선, 냉각, 서버, PCB, IDC, ESS, 전력망이 모두 엮인다.
**Nuclear/SMR/Grid Policy**도 유틸리티와 달라. 정책, 수주, 소송, CAPEX, 기자재 매출화가 핵심이다. 체코 원전 사례만 봐도 계약 기대와 법적 리스크가 동시에 존재한다. ([Reuters][1])

---

# 3. 이번 라운드의 가장 중요한 검증 기준

앞으로 성공사례와 반례는 반드시 **점수와 주가의 정합성**을 같이 봐야 해.

## 성공사례 인정 조건

```text
1. Stage 1/2 신호가 실제로 먼저 나왔다.
2. EPS/OP/FCF 또는 수주/수출/가격/마진 증거가 붙었다.
3. Stage 2/3 이후 6~24개월 안에 주가가 의미 있게 리레이팅됐다.
4. 주가 상승이 단순 테마가 아니라 실적/계약/수출/ROE/환원과 연결됐다.
5. 이후 4B/4C 신호도 설명 가능했다.
```

## 반례 인정 조건

```text
1. 점수상 좋아 보였지만 주가 리레이팅이 안 됐다.
2. 주가는 올랐지만 EPS/FCF가 안 따라왔다.
3. Stage 3처럼 보였지만 4C가 빨리 왔다.
4. 리포트는 좋았지만 실제 매출화가 실패했다.
5. 이벤트 프리미엄이 끝나자 주가가 무너졌다.
```

즉, 앞으로 case record에는 아래를 꼭 넣어야 해.

```text
score_price_alignment:
  aligned
  false_positive_score
  missed_due_to_score
  price_moved_without_evidence
  evidence_good_but_price_failed

rerating_result:
  true_rerating
  cyclical_rerating
  event_premium
  theme_overheat
  no_rerating
  thesis_break
```

---

# 4. Platform / Software / Internet 보강

## 결론

플랫폼은 **절대 쉽게 성공사례로 넣으면 안 돼.**
네이버, 카카오 모두 좋은 회사일 수 있지만, 서생원식 E2R은 “좋은 회사”가 아니라 **EPS/FCF 체급 변화 + 시장 프레임 변화 + 주가 리레이팅**이 있어야 해.

## 성공 후보와 반례

| 구분    | 케이스          | 판단                                                                                                                           |
| ----- | ------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| 성공 후보 | NAVER        | 광고·커머스 회복, AI 비용 효율화, 클라우드/커머스 반복매출이 OP/EPS로 연결되는지 확인 필요. 아직 확정 성공 아님                                                        |
| 후보/반례 | Kakao        | 플랫폼 자산은 있지만, 규제·거버넌스·SM 인수 관련 법적 리스크가 valuation rerating을 막을 수 있음. 창업자 김범수의 SM 주가조작 혐의 기소와 법적 이슈가 실제 리스크로 보도됨 ([Reuters][2]) |
| 성공 후보 | 더존비즈온        | ERP/SaaS 반복매출, AI/클라우드 전환, OPM 레버리지 확인 필요                                                                                    |
| 반례    | MAU만 높은 플랫폼  | 트래픽이 수익화되지 않으면 E2R 아님                                                                                                        |
| 반례    | AI 비용 과다 플랫폼 | AI narrative는 있지만 GPU/서버 비용 때문에 FCF가 훼손될 수 있음                                                                                |

## Stage 기준

```text
Stage 1:
- 트래픽/MAU 회복
- 광고/커머스 회복
- 비용절감
- AI/클라우드 신사업

Stage 2:
- ARPU 상승
- take-rate 상승
- OPM 개선
- FY1/FY2 OP 상향
- 반복매출 증가

Stage 3:
- recurring revenue lock-in
- 비용 레버리지
- regulation risk 낮음
- 시장이 아직 저성장 플랫폼 프레임으로 평가
- Stage 3 이후 실제 주가 리레이팅

4B:
- AI/플랫폼 narrative 과열
- multiple expansion 완료
- ARPU 성장 둔화

4C:
- 규제
- take-rate 하락
- 트래픽 감소
- AI 비용 과다
- governance/legal risk
```

## 점수 보정

```text
EPS/FCF: 20
Visibility: 22
Bottleneck/Pricing: 6~8
Mispricing: 16
Valuation: 14
Risk penalty: regulation / AI cost / governance
```

**검증 규칙:**
플랫폼에서 MAU나 AI 키워드만으로 점수를 높게 줬는데 주가 리레이팅이 안 되면, 그건 점수 실패다. ARPU·OPM·FCF 가중치를 높이고, 트래픽/테마 가중치는 낮춰야 한다.

---

# 5. Game / Content / IP 보강

## 결론

게임·콘텐츠는 **신작 기대**와 **반복 monetization**을 반드시 분리해야 해. 주가가 신작 기대만으로 오르면 Stage 3가 아니라 Stage 1~2 또는 4B-watch일 수 있다.

## 성공 후보와 반례

| 구분    | 케이스              | 판단                                                                                                                 |
| ----- | ---------------- | ------------------------------------------------------------------------------------------------------------------ |
| 성공 후보 | Krafton          | PUBG/BGMI 글로벌 IP와 인도 exposure. BGMI는 2022년 2.5억 다운로드를 넘겼고, 이후 ban/relaunch 이력도 있어 성장성과 규제 리스크를 같이 봐야 함 ([위키백과][3]) |
| 성공 후보 | Shift Up         | Nikke/Stellar Blade, 높은 OPM 가능성. 2024년 IPO와 이후 실적 자료가 있어 게임/IP 반복성 검증 후보 ([위키백과][4])                               |
| 성공 후보 | HYBE / JYP / SM  | IP·투어·팬덤 monetization. 다만 아티스트·계약·거버넌스 리스크 큼                                                                       |
| 반례    | 신작 기대만 있는 게임주    | 출시 후 매출이 안 나오면 4C                                                                                                  |
| 반례    | 단일 IP 의존         | 한 게임/한 아티스트가 꺾이면 EPS/FCF 경로가 깨짐                                                                                    |
| 반례    | K-pop 경영권/계약 이벤트 | SM 인수전처럼 event premium은 생기지만 반복 EPS/FCF와 분리해야 함 ([AP News][5])                                                     |

## Stage 기준

```text
Stage 1:
- 신작/컴백/투어
- 예약판매
- 글로벌 흥행 뉴스
- 다운로드/트래픽 증가

Stage 2:
- 실제 매출화
- OP/EPS 상향
- IP 반복성 확인

Stage 3:
- IP portfolio
- 글로벌 monetization
- 낮은 churn
- 반복 revenue 구조
- 시장이 아직 단일 hit 프레임으로 평가

4B:
- 신작 흥행 peak
- 신작 기대 과열
- multiple saturation

4C:
- 신작 실패
- 핵심 IP 훼손
- 아티스트/계약 리스크
- 규제/판호 리스크
```

## 점수 보정

```text
EPS/FCF: 20
Visibility: 18
Bottleneck/Pricing: 5~8
Mispricing: 14
Valuation: 12
Risk penalty: hit-driven discount
```

**검증 규칙:**
신작 발표 후 주가가 올라가도, 출시 후 OP/EPS가 못 따라오면 성공사례가 아니라 **false score / theme overheat**로 넣어야 한다.

---

# 6. Robotics / Factory Automation 보강

## 결론

로봇은 **테마 과열 가능성이 매우 큰 archetype**이야.
대기업 투자와 정책이 Stage 1/2 신호는 될 수 있지만, 실제 수주·매출·반복매출 전환 전에는 Green 금지에 가깝다.

## 성공 후보와 반례

| 구분    | 케이스                       | 판단                                                                                                    |
| ----- | ------------------------- | ----------------------------------------------------------------------------------------------------- |
| 성공 후보 | Rainbow Robotics          | 삼성전자가 2,670억원 지분 취득으로 최대주주가 됐고, Future Robotics Office를 CEO 직속으로 만든 점은 강한 Stage 1/2 신호 ([Reuters][6]) |
| 성공 후보 | Hyundai / Boston Dynamics | 현대차의 로봇·AI 데이터센터·로봇공장 투자 narrative는 주가를 자극할 수 있지만, 자동차 본업 EPS와 분리해야 함                                 |
| 반례    | 무실적 로봇 테마주                | 대기업 투자·정책 뉴스만 있고 매출화가 없으면 Green 금지                                                                    |
| 반례    | 고밸류 IPO 로봇주               | 제품력은 있어도 EPS/FCF가 주가를 따라오지 않으면 Theme Overheat                                                         |
| 반례    | MOU/PoC만 있는 자동화주          | 실제 수주/매출화 전환 전 Stage 3 금지                                                                             |

## Stage 기준

```text
Stage 1:
- 대기업 투자
- 로봇 정책/테마
- MOU/PoC
- 거래대금 증가

Stage 2:
- 실제 고객사 도입
- 수주/매출화
- gross margin 개선
- 반복 서비스/소모품 매출

Stage 3:
- 고객사 다변화
- 반복 매출 구조
- OPM 개선
- valuation이 아직 테마가 아니라 산업재/플랫폼 전환을 덜 반영

4B:
- humanoid/robotics 과열
- EPS보다 주가가 먼저 감
- 장밋빛 TAM 리포트 남발

4C:
- 수주 지연
- 매출화 실패
- 대기업 투자 철회
- 현금흐름 악화
```

## 점수 보정

```text
EPS/FCF: 18~20
Visibility: 15
Bottleneck/Pricing: 10
Mispricing: 12
Valuation: 10
Theme penalty: 강하게
```

**검증 규칙:**
로봇은 주가 급등 자체가 성공이 아니다. 대기업 투자 뉴스 이후 실제 매출·수주·OP가 안 붙으면 반례다.

---

# 7. Retail / Domestic Consumer 보강

## 결론

리테일은 대부분 **경기 rebound**와 **구조적 E2R**을 분리해야 해.
편의점은 점포효율·PB·해외 확장, 면세/백화점은 관광객 mix와 재고/마진이 핵심이다.

## 성공 후보와 반례

| 구분    | 케이스           | 판단                                                                                     |
| ----- | ------------- | -------------------------------------------------------------------------------------- |
| 성공 후보 | BGF리테일 / CU   | CU는 2025년 기준 18,000개 이상 매장과 해외 점포를 갖춘 것으로 정리되어 있어, 점포효율·해외 확장·PB mix를 봐야 함 ([위키백과][7]) |
| 성공 후보 | GS리테일 / GS25  | GS25는 2024년 말 전국 18,000개 이상 점포로 정리되어 있어, 점포효율과 편의점 경쟁 강도를 같이 봐야 함 ([위키백과][8])          |
| 성공 후보 | 호텔신라 / 신세계    | 관광·면세 회복. 중국 의존도와 객단가 확인 필요                                                            |
| 반례    | 대형마트 구조 경쟁 심화 | 이커머스 경쟁과 마진 악화                                                                         |
| 반례    | 단기 소비 회복 테마   | 트래픽만 있고 OPM/FCF 개선 없으면 Stage 1                                                         |
| 반례    | 면세 중국 의존      | 중국 관광객·정책 변화에 취약                                                                       |

## Stage 기준

```text
Stage 1:
- same-store sales 회복
- 소비 회복
- 관광객 증가
- 점포 확대

Stage 2:
- OPM 개선
- 재고 정상화
- 비용 레버리지
- PB/고마진 mix 증가

Stage 3:
- 점포 효율 구조 변화
- 해외/신사업 반복매출
- FCF 개선
- valuation discount 해소

4B:
- 소비 회복 모두 반영
- 점포 성장 한계
- 임대료/인건비 압박

4C:
- 재고 증가
- 온라인 경쟁 심화
- 소비 둔화
```

## 점수 보정

```text
EPS/FCF: 18
Visibility: 16
Bottleneck/Pricing: 5
Mispricing: 14
Valuation: 14
Risk penalty: inventory / rent / wage / competition
```

**검증 규칙:**
리테일은 주가 rebound가 와도, OPM/FCF 개선이 2~4분기 이상 이어지지 않으면 Stage 3 성공사례가 아니다.

---

# 8. Construction / Real Estate / Credit 보강

## 결론

건설은 수주보다 **PF·미분양·현금흐름·신용 리스크**가 먼저다.
수주잔고가 커도 PF가 터지면 E2R이 아니라 credit risk다.

## 성공 후보와 반례

| 구분    | 케이스            | 판단                                                                                              |
| ----- | -------------- | ----------------------------------------------------------------------------------------------- |
| 성공 후보 | PF 리스크 해소형 건설사 | 부실 정리 후 cash flow 회복 시 후보                                                                       |
| 성공 후보 | 해외 플랜트/인프라 수주형 | 수주 질과 마진이 확정적이면 후보                                                                              |
| 반례    | PF 부실 건설사      | 한국 부동산 PF 연체율은 2021년 말 0.37%에서 2023년 말 2.70%로 상승했고, 금융당국이 구조조정을 강화했다는 Reuters 보도 ([Reuters][9]) |
| 반례    | 유동성 지원 의존 기업   | 정부/은행 지원은 Stage 1 relief일 수 있지만 구조적 E2R은 아님                                                     |
| 반례    | 원가 상승 미반영      | 매출은 늘어도 원가율 상승으로 OP/FCF 훼손                                                                      |

## Stage 기준

```text
Stage 1:
- PF 우려 완화
- 대형 수주
- 유동성 지원
- 주가 낙폭과대

Stage 2:
- 부실 정리
- cash flow 개선
- 원가율 안정
- 부채 감소

Stage 3:
- 매우 제한적
- 구조조정 후 반복 cash flow
- 해외수주 마진 확정
- PF risk 낮음

4B:
- 부동산 회복 기대 과열
- 미분양 risk 무시

4C:
- PF 부실
- 미분양 증가
- 신용등급 하락
- 유동성 위기
```

## 점수 보정

```text
EPS/FCF: 18
Visibility: 10~12
Bottleneck/Pricing: 5
Mispricing: 12
Valuation: 10
Risk penalty: 매우 큼
```

**검증 규칙:**
건설주가 반등했더라도 PF/미분양/현금흐름이 해결되지 않으면 E2R 성공이 아니라 **credit relief rally**다.

---

# 9. Utilities / Regulated Tariff 보강

## 결론

유틸리티는 싸다고 E2R이 아니다.
핵심은 **요금·원가·부채·규제 프레임 변화**야.

## 성공 후보와 반례

| 구분    | 케이스       | 판단                                                                            |
| ----- | --------- | ----------------------------------------------------------------------------- |
| 성공 후보 | 한국전력      | 요금 정상화, 원가 안정, 부채 축소 여부                                                       |
| 성공 후보 | 한국가스공사    | 미수금 회수, 원가보상, 배당 가능성                                                          |
| 반례    | 요금 동결     | EPS 개선 지속성 낮음                                                                 |
| 반례    | 부채 과다     | 주주환원 불가능, valuation trap                                                      |
| 반례    | 전력시장 구조왜곡 | 한국 전력시장 가격 신호 왜곡과 transmission constraint는 장기 투자·효율 문제를 만들 수 있음 ([arXiv][10]) |

## Stage 기준

```text
Stage 1:
- 요금 인상
- 원가 하락
- 정책 변화

Stage 2:
- 적자 축소
- cash flow 개선
- 부채 증가 둔화

Stage 3:
- 규제 프레임 변화
- 지속적인 cost pass-through
- 부채 정상화
- 배당 가능성

4B:
- 요금 정상화 기대 선반영
- 원가 하락 peak

4C:
- 요금 동결
- 원가 급등
- 정책 반전
- 부채 부담 확대
```

## 점수 보정

```text
EPS/FCF: 18
Visibility: 18
Bottleneck/Pricing: 5
Mispricing: 12
Valuation: 10
Regulatory risk cap
```

**검증 규칙:**
유틸리티는 주가가 올라가도 정책/부채/배당이 같이 개선되지 않으면 **규제 이벤트 trade**다.

---

# 10. Nuclear / SMR / Grid Policy 확정

## 결론

원전은 유틸리티와 다르다.
정책, 수주, 법적 리스크, project financing, 기자재 매출화가 핵심이다.

## 성공 후보와 반례

| 구분    | 케이스                           | 판단                                                                                                                             |
| ----- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 성공 후보 | KHNP / 두산에너빌리티 / 한전기술 / 한전KPS | 체코 원전, 설계·정비·주기기 수주 경로                                                                                                         |
| 성공 후보 | Czech Dukovany                | 체코 경쟁당국이 EDF 항소를 기각하면서 KHNP 계약 경로가 열렸지만, 이후 EDF 법적 challenge로 서명 중단 injunction도 발생. 이건 성공과 리스크가 동시에 있는 좋은 case ([Reuters][11]) |
| 반례    | 수주 기대만 있는 원전 테마               | 계약 전 기대만으로 Stage 3 금지                                                                                                          |
| 반례    | 소송/정책 지연                      | legal risk는 4C 또는 hard RedTeam 후보                                                                                              |
| 반례    | 프로젝트 원가 상승                    | 장기 프로젝트는 cost overrun이 thesis break                                                                                            |

## Stage 기준

```text
Stage 1:
- 원전 정책
- 우선협상대상자
- SMR 테마

Stage 2:
- 실제 계약/LOI
- project financing
- 기자재 매출화 경로

Stage 3:
- 다년 수주잔고
- 수익성/마진 확인
- 법적/정책 리스크 낮음

4B:
- 원전 기대가 가격에 선반영
- 테마주 동반 과열

4C:
- 소송 패소/지연
- 정책 반전
- 프로젝트 지연
- 원가 상승
```

## 점수 보정

```text
EPS/FCF: 18
Visibility: 22
Bottleneck/Pricing: 8
Mispricing: 14
Valuation: 12
Risk penalty: legal / policy / delay
```

**검증 규칙:**
원전주는 수주 기대만으로 급등할 수 있다. Stage 3 성공으로 인정하려면 **계약 확정 + 기자재 매출화 + 마진 경로**가 있어야 한다.

---

# 11. Holding / Governance / Restructuring 보강

## 결론

지주/거버넌스는 EPS 폭발보다 **NAV discount 해소와 자본배분 실행**이 핵심이다.
그러나 공개매수·경영권 분쟁만으로 주가가 오른 건 E2R이 아니라 event premium일 수 있다.

## 성공 후보와 반례

| 구분         | 케이스                | 판단                                                                                                                |
| ---------- | ------------------ | ----------------------------------------------------------------------------------------------------------------- |
| 성공 후보      | SK스퀘어 / 삼성물산       | 자회사 가치, 자사주/소각, NAV discount 해소 여부                                                                                |
| 이벤트 후보     | Korea Zinc         | MBK/Young Poong 공개매수 발표 후 주가가 19.8% 상승했고, 경영권·거버넌스 논쟁이 기업가치 이벤트로 작용 ([Reuters][12])                               |
| 이벤트/리스크 후보 | Korea Zinc 유상증자 철회 | Korea Zinc는 18억 달러 규모 신주발행 계획을 철회했고, 금융당국 조사와 주가 변동이 동반됨. event premium과 governance risk를 같이 봐야 함 ([Reuters][13]) |
| 반례         | 자사주 발표만 있고 소각 없음   | value trap 가능                                                                                                     |
| 반례         | 경영권 분쟁만 있는 종목      | EPS/FCF 변화 없이 event premium만 있으면 Stage 3 금지                                                                       |
| 반례         | 자회사 가치 훼손          | NAV discount가 정당화                                                                                                 |

## Stage 기준

```text
Stage 1:
- 자사주/소각/배당
- 경영권 분쟁
- value-up 공시

Stage 2:
- 실제 소각
- 반복 환원정책
- 자회사 실적 개선
- discount 축소 가능성

Stage 3:
- governance regime change
- 반복 환원정책
- NAV discount 구조적 해소

4B:
- 이벤트 프리미엄 반영 완료
- 공개매수/분쟁 종결

4C:
- 환원 미이행
- 자회사 가치 훼손
- 지배주주 리스크 재부각
```

## 점수 보정

```text
EPS/FCF: 10~12
Visibility: 18
Mispricing: 20
Valuation: 25
Capital Allocation: 10
```

**검증 규칙:**
경영권 분쟁으로 주가가 올랐으면 `event_premium`으로 분류하고, 구조적 NAV/환원 변화가 없으면 E2R 성공사례로 넣지 않는다.

---

# 12. Financial Spread / Balance Sheet 보강

## 결론

금융주는 EPS 폭발보다 **ROE-PBR-주주환원**의 정합성이 핵심이다.
저PBR만으로는 성공사례가 아니다.

## 성공 후보와 반례

| 구분    | 케이스                | 판단                                                                             |
| ----- | ------------------ | ------------------------------------------------------------------------------ |
| 성공 후보 | KB금융 / 신한지주 / 하나금융 | ROE, CET1, 자사주·배당, value-up                                                    |
| 성공 후보 | 메리츠금융 / 삼성화재       | 자본효율, 환원정책, 보험계약마진/ROE                                                         |
| 정책 배경 | Korea value-up     | 한국의 corporate governance/value-up 흐름은 저PBR 리레이팅 배경이 될 수 있지만, ROE와 실제 환원이 같이 필요 |
| 반례    | 단순 저PBR 금융주        | ROE/환원정책 없으면 value trap                                                        |
| 반례    | PF/충당금 리스크 금융      | credit cost 상승이면 4C                                                            |

## Stage 기준

```text
Stage 1:
- value-up 공시
- 자사주/배당
- 저PBR

Stage 2:
- ROE 개선
- 자본비율 안정
- 충당금 안정
- 환원정책 실행

Stage 3:
- PBR-ROE 프레임 변화
- recurring ROE
- shareholder return credible
- credit risk 낮음

4B:
- PBR이 ROE 대비 정상화
- 모두가 value-up 성공주로 인정

4C:
- credit cost 증가
- PF 부실
- 자본비율 악화
```

## 점수 보정

```text
EPS/FCF: 15
Visibility: 20
Bottleneck/Pricing: 5
Mispricing: 15
Valuation: 25
Capital Allocation: 10
```

**검증 규칙:**
금융주는 주가가 올라가도 ROE/CET1/환원정책이 따라오지 않으면 E2R 성공이 아니라 저PBR 이벤트다.

---

# 13. Biotech / Regulatory 세분화

## 결론

바이오는 하나로 묶으면 위험하다. 최소 세 가지로 나눠야 해.

```text
A. Pre-revenue clinical biotech
B. Royalty / technology-transfer biotech
C. Revenue-generating pharma / CDMO
```

## 성공 후보와 반례

| 구분    | 케이스                  | 판단                                                   |
| ----- | -------------------- | ---------------------------------------------------- |
| 성공 후보 | 알테오젠                 | 기술이전/SC 제형/로열티 가능성. 실제 royalty visibility가 핵심        |
| 성공 후보 | 유한양행                 | 신약 허가·로열티·매출화 여부                                     |
| 성공 후보 | 삼성바이오로직스             | CDMO 장기계약/가동률. 일반 바이오보다 contract backlog healthcare형 |
| 성공 후보 | 셀트리온                 | 바이오시밀러 매출화, 글로벌 판매, FCF                              |
| 반례    | 임상 뉴스만 있는 바이오        | EPS/FCF 전환 전 Green 금지                                |
| 반례    | CB/유증 반복 바이오         | dilution risk로 Green 차단                              |
| 반례    | 기술이전 headline만 있는 회사 | milestone/royalty 불확실하면 Stage 1~2                    |

## Stage 기준

```text
Stage 1:
- 임상/허가/기술이전 뉴스

Stage 2:
- milestone payment
- 허가 가능성
- cash runway
- 매출화 계획

Stage 3:
- 실제 매출/로열티
- EPS/FCF 전환
- dilution risk 낮음
- 반복 revenue visibility

4B:
- 신약 기대 과열
- valuation이 매출화보다 먼저 감

4C:
- 임상 실패
- 허가 지연
- 유증/CB
- 파트너 계약 해지
```

## 점수 보정

```text
Pre-revenue:
  EPS/FCF 낮게, Green 거의 금지

Royalty/tech transfer:
  Visibility = milestone + royalty probability

CDMO/revenue pharma:
  EPS/FCF와 contract visibility로 평가 가능
```

**검증 규칙:**
바이오는 주가가 급등해도 매출화 전이면 E2R 성공사례가 아니라 regulatory/event premium일 수 있다.

---

# 14. Medical Device / Healthcare Export 보강

## 결론

의료기기는 바이오보다 E2R에 더 적합할 수 있어.
제품 판매, 소모품 반복매출, 수출채널, OPM이 확인 가능하기 때문이다.

## 성공 후보와 반례

| 구분    | 케이스             | 판단                                                          |
| ----- | --------------- | ----------------------------------------------------------- |
| 성공 후보 | Classys         | 비침습 피부미용 의료기기 회사이고, 2025년 기준 60개국 이상 수출한다고 정리됨 ([위키백과][14]) |
| 성공 후보 | 파마리서치 / 휴젤 / 원텍 | 수출, 인허가, 소모품/시술 반복 확인 필요                                    |
| 반례    | 단일 장비 판매        | 반복 소모품/서비스 없으면 visibility 낮음                                |
| 반례    | 허가 지연           | 매출화 지연이면 4C                                                 |
| 반례    | 경쟁 심화           | ASP 하락과 마진 훼손                                               |

## Stage 기준

```text
Stage 1:
- 수출국 확대
- 인허가
- 신제품

Stage 2:
- 소모품/반복매출
- OPM/ROE
- FY1/FY2 EPS 상향

Stage 3:
- 글로벌 채널
- 반복 소모품 구조
- 높은 FCF conversion
- 규제 리스크 낮음

4C:
- 허가 지연
- 경쟁 심화
- ASP 하락
```

## 점수 보정

```text
EPS/FCF: 20
Visibility: 22
Bottleneck/Pricing: 13
Mispricing: 14
Valuation: 12
```

**검증 규칙:**
의료기기는 장비 판매만으로 Green 금지. 반복 소모품·시술·수출 재주문이 있어야 Stage 3 가능.

---

# 15. Travel / Leisure / Reopening 신규 archetype

## 결론

리테일과 분리해야 한다.
여행·카지노·항공·면세는 **reopening / 관광 / 환율 / 유가 / 중국 의존**의 사이클성이 강하다.

## 성공 후보와 반례

| 구분    | 케이스                | 판단                                   |
| ----- | ------------------ | ------------------------------------ |
| 성공 후보 | 파라다이스 / GKL        | 카지노 drop amount, 일본/중국 VIP, 관광객 회복   |
| 성공 후보 | 호텔신라 / 신세계         | 면세·관광 회복, 중국 의존도 확인                  |
| 성공 후보 | 대한항공 / 제주항공        | 여객 회복, 유가, 환율, 화물 정상화                |
| 반례    | 중국 단체관광 기대만 있는 면세주 | actual traffic/매출 없이 기대만 있으면 Stage 1 |
| 반례    | 유가 급등 항공주          | 수요는 좋아도 마진 훼손                        |
| 반례    | 리오프닝 peak          | 관광객 회복이 모두 반영되면 4B                   |

## Stage 기준

```text
Stage 1:
- 출입국 회복
- 관광객 증가
- 카지노 drop / 면세 매출

Stage 2:
- OP/EPS 상향
- fixed cost leverage
- 고마진 고객 mix

Stage 3:
- 반복 관광/구조적 방문객 증가
- 중국 의존도 낮음
- 비용/유가 안정

4B:
- reopening 기대 모두 반영
- 관광객 peak

4C:
- 경기 둔화
- 유가/환율 악화
- 중국/규제 리스크
```

## 점수 보정

```text
EPS/FCF: 18
Visibility: 14
Bottleneck/Pricing: 5
Mispricing: 12
Valuation: 10
Cyclical risk cap
```

**검증 규칙:**
리오프닝 주가 급등은 구조적 E2R이 아닐 수 있다. Stage 3 성공은 관광객/매출/OPM이 지속될 때만 인정.

---

# 16. AI Data Center Infrastructure 신규 archetype

## 결론

이건 반드시 별도 archetype으로 두는 게 맞아.
전력기기만으로는 부족하고, AI 데이터센터 CAPEX의 파급 경로 전체를 봐야 한다.

```text
AI 데이터센터 증설
→ 전력/냉각/서버/네트워크/전력망/ESS 병목
→ 다년 CAPEX
→ 수주잔고와 EPS 상향
```

## 포함 섹터

```text
전력기기
전선
IDC
냉각
서버/PCB
전력망
ESS
통신망
```

## 성공 후보와 반례

| 구분    | 케이스                   | 판단                             |
| ----- | --------------------- | ------------------------------ |
| 성공 후보 | HD현대일렉트릭 / 효성중공업      | 데이터센터 전력망·변압기 수요               |
| 성공 후보 | LS ELECTRIC / LS전선 관련 | 전력망, 전선, 배전                    |
| 성공 후보 | 이수페타시스                | AI 서버/네트워크 PCB                 |
| 성공 후보 | 냉각/공조 관련 기업           | 데이터센터 cooling exposure 확인 필요   |
| 반례    | AI 데이터센터 테마만 붙은 기업    | 실제 수주/매출 exposure 없으면 Green 금지 |
| 반례    | CAPEX 기대 선반영          | valuation이 먼저 간 경우 4B-watch    |
| 반례    | AI CAPEX cut          | 고객사 데이터센터 투자 지연이면 4C           |

## Stage 기준

```text
Stage 1:
- 데이터센터 capex 뉴스
- 전력부족/냉각/전력망 키워드

Stage 2:
- 수주/계약
- 고객사 capex visibility
- OP/EPS revision

Stage 3:
- 다년 capex visibility
- 핵심 병목 위치
- 공급 제약
- 가격전가력

4B:
- AI capex narrative 과열
- 신규 capacity 과잉 우려

4C:
- AI capex cut
- 데이터센터 지연
- 전력망/인허가 병목으로 매출 지연
```

## 점수 보정

```text
EPS/FCF: 22
Visibility: 23
Bottleneck/Pricing: 20
Mispricing: 14
Valuation: 12
Risk penalty: AI capex cut / project delay
```

**검증 규칙:**
AI 데이터센터 테마는 주가가 먼저 움직이기 쉽다. 실제 수주·납품·EPS revision 없으면 Theme Overheat로 내려야 한다.

---

# 17. Education / Specialty Services 신규 archetype

## 결론

교육·시험·특수서비스는 플랫폼도 소비재도 아니다.
반복 수강, 정책, 가격 인상, 성인교육/해외 확장, B2B 구독이 핵심이다.

## 성공 후보와 반례

| 구분    | 케이스          | 판단                     |
| ----- | ------------ | ---------------------- |
| 성공 후보 | 메가스터디교육      | 입시/사교육 반복수요, 가격, 수강생 수 |
| 성공 후보 | 웅진씽크빅 / 대교   | 학습지/에듀테크, 반복매출         |
| 성공 후보 | 자격시험/특수교육 기업 | 정책/시험 수요 증가 가능         |
| 반례    | 저출산 TAM 축소   | 장기 수요 감소               |
| 반례    | 정책 규제        | 사교육 규제, 가격 제한          |
| 반례    | AI 튜터 경쟁     | 가격 하락과 차별화 약화          |

## Stage 기준

```text
Stage 1:
- 정책 변화
- 학생 수/수강생 증가
- 가격 인상

Stage 2:
- 반복매출
- OPM 개선
- 비용 효율화

Stage 3:
- 구조적 lock-in
- 해외/성인교육 확장
- 저출산 리스크 상쇄

4C:
- 정책 규제
- 학생 수 감소
- 가격 하락
```

## 점수 보정

```text
EPS/FCF: 18
Visibility: 20
Bottleneck/Pricing: 5
Mispricing: 12
Valuation: 12
Risk: population / regulation
```

---

# 18. Rare Metals / Strategic Materials 신규 archetype

## 결론

단순 commodity spread와 다르다.
전략금속은 공급망, 제련마진, 지정학, M&A/경영권, 정부정책이 함께 움직인다.

## 성공 후보와 반례

| 구분      | 케이스                | 판단                                                                                                    |
| ------- | ------------------ | ----------------------------------------------------------------------------------------------------- |
| 이벤트 후보  | Korea Zinc         | 세계 최대급 제련사, 전략소재 공급망, 공개매수/경영권 이벤트. MBK/Young Poong 공개매수 발표 후 Korea Zinc 주가는 19.8% 상승 ([Reuters][12]) |
| 이벤트/리스크 | Korea Zinc 신주발행 철회 | 18억 달러 신주발행 철회와 금융당국 조사, 주가 변동이 동반돼 event premium과 governance risk가 함께 존재 ([Reuters][13])             |
| 반례      | 순수 금속가격 상승         | 가격만으로는 구조적 visibility 낮음                                                                              |
| 반례      | 경영권 이벤트만 있는 종목     | EPS/FCF 변화 없이 event premium이면 Stage 3 금지                                                              |
| 반례      | 장기 분쟁              | 투자·경영 지연, governance discount                                                                         |

## Stage 기준

```text
Stage 1:
- 금속가격 상승
- 공개매수/거버넌스 이벤트
- 전략소재 supply chain 뉴스

Stage 2:
- 제련마진 개선
- 자본배분 개선
- governance change
- cash flow 개선

Stage 3:
- 공급망 bottleneck + FCF + governance rerating
- 단순 이벤트가 아닌 구조 변화

4B:
- 공개매수 프리미엄 반영
- 이벤트 종료

4C:
- 경영권 분쟁 장기화
- 투자 지연
- 마진 악화
```

## 점수 보정

```text
EPS/FCF: 18
Visibility: 16
Bottleneck/Pricing: 15
Mispricing: 16
Valuation: 15
Governance/event risk 별도
```

---

# 19. 이번 라운드 후 정리된 “Green 허용 등급”

## Green 가능성이 상대적으로 높은 archetype

```text
Contract / Backlog Industrial
Defense / Government Backlog
Shipbuilding / Offshore Backlog
Export / Recurring Consumer
K-Beauty / Export Distribution
Memory / HBM Capacity
Semi Equipment / Advanced Packaging
Medical Device / Healthcare Export
AI Data Center Infrastructure
Financial Spread / Shareholder Return
Turnaround / Cost Restructuring
```

## Stage 3-Watch / Yellow 중심 archetype

```text
Platform / Software
Game / Content / IP
Robotics / Factory Automation
Auto / Mobility
Nuclear / SMR / Grid Policy
Holding / Governance
Travel / Leisure
Education / Specialty Services
Rare Metals / Strategic Materials
Utilities / Regulated Tariff
```

## Red / 4B 방어 중심 archetype

```text
Shipping / Freight Cycle
Commodity Spread
Battery Materials / Capex Overheat
Construction / Real Estate / Credit
Pre-revenue Biotech
One-off Event Demand
Theme / Valuation Overheat
```

이 구분을 에이전트가 알아야 해.
똑같이 EPS가 폭발해도 해운·진단키트·배터리 소재 과열은 Green으로 가면 위험하고, 전력기기·방산·수출소비재·HBM은 구조적 visibility가 있으면 Green 후보가 될 수 있다.

---

# 20. 다음 라운드에서 더 채울 부분

아직 더 채워야 하는 부분은 분명해.

```text
1. 실제 price path 숫자화
   - stage3_price
   - peak_price
   - MFE/MAE
   - drawdown_after_peak

2. 각 archetype별 최소 2개 성공 + 2개 반례 채우기

3. Platform/NAVER/Kakao를 실제 주가-실적 정합성으로 검증
   - 성공인지 반례인지 아직 확정 금지

4. 금융/value-up 실제 성공사례와 value trap 반례 분리

5. Biotech를 pre-revenue / royalty / CDMO로 나눠 case 채우기

6. AI Data Center Infrastructure case를 전력기기·냉각·PCB·IDC로 세분화

7. Nuclear/SMR은 수주 기대와 계약 확정/매출화 분리

8. Travel/Leisure와 Retail을 분리해서 reopening rebound와 구조적 E2R 구분
```

---

# 21. 이번 라운드의 결론

이번 라운드에서 가장 중요한 정리는 이거야.

```text
성공사례는 “좋아 보이는 기업”이 아니라,
점수상 높았고 실제 주가도 EPS/FCF 리레이팅 방향으로 움직인 케이스여야 한다.

반례는 “나쁜 기업”이 아니라,
점수상 높게 보일 수 있었지만 실제로는 E2R이 아니었거나
주가가 따라오지 않았거나
4C가 빨리 온 케이스여야 한다.
```

그리고 새로 확정할 방향은:

```text
- AI Data Center Infrastructure는 별도 archetype
- Nuclear/SMR/Grid Policy도 별도 archetype
- Travel/Leisure/Reopening도 별도 archetype
- Education/Specialty Services도 후보 archetype
- Rare Metals/Strategic Materials도 commodity와 분리
- Platform/Game/Robotics는 Green보다 false-positive 방어가 중요
- Construction/Utilities/Biotech는 리스크 cap이 강해야 함
```

이렇게 가면 대섹터 누락을 줄이면서도, 기존 서생원식 E2R 정신을 유지할 수 있어.

[1]: https://www.reuters.com/business/energy/cez-will-appeal-injunction-halting-nuclear-power-deal-signing-2025-05-07/?utm_source=chatgpt.com "CEZ will appeal injunction halting nuclear power deal signing"
[2]: https://www.reuters.com/markets/asia/south-korea-prosecutors-indict-kakao-group-founder-stock-manipulation-charges-2024-08-08/?utm_source=chatgpt.com "South Korea prosecutors indict Kakao group founder on stock manipulation charges, Yonhap reports"
[3]: https://en.wikipedia.org/wiki/Battlegrounds_Mobile_India?utm_source=chatgpt.com "Battlegrounds Mobile India"
[4]: https://en.wikipedia.org/wiki/Shift_Up?utm_source=chatgpt.com "Shift Up"
[5]: https://apnews.com/article/e04e965fb5f8db38f446c61fb456e050?utm_source=chatgpt.com "Korea's Hybe completes purchase of 14.8% stake in rival SM"
[6]: https://www.reuters.com/technology/samsung-electronics-becomes-largest-shareholder-south-koreas-rainbow-robotics-2024-12-30/?utm_source=chatgpt.com "Samsung Electronics becomes largest shareholder of South Korea's Rainbow Robotics"
[7]: https://en.wikipedia.org/wiki/CU_%28store%29?utm_source=chatgpt.com "CU (store)"
[8]: https://en.wikipedia.org/wiki/GS25?utm_source=chatgpt.com "GS25"
[9]: https://www.reuters.com/markets/asia/south-korea-tightens-scrutiny-speed-up-real-estate-restructuring-2024-05-13/?utm_source=chatgpt.com "South Korea tightens scrutiny to speed up real estate restructuring"
[10]: https://arxiv.org/abs/2605.09318?utm_source=chatgpt.com "Price Distortions in Korea's Electricity Market: Barriers to Renewable Integration and Reform Pathways"
[11]: https://www.reuters.com/sustainability/boards-policy-regulation/czech-court-halts-nuclear-plant-signing-with-khnp-after-last-minute-appeal-2025-05-06/?utm_source=chatgpt.com "Czech court halts nuclear plant signing with KHNP after last-minute appeal"
[12]: https://www.reuters.com/markets/deals/private-equity-mbk-young-poong-launch-15-bln-tender-offer-korea-zinc-shares-2024-09-13/?utm_source=chatgpt.com "Private equity MBK, Young Poong launch $1.5 bln tender offer for Korea Zinc shares"
[13]: https://www.reuters.com/markets/commodities/korea-zinc-withdraws-plan-issue-18-bln-new-shares-2024-11-13/?utm_source=chatgpt.com "Korea Zinc pulls $1.8 bln share sale, turns sights to board fight"
[14]: https://en.wikipedia.org/wiki/Classys?utm_source=chatgpt.com "Classys"
