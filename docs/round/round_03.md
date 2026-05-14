응. 계속 확장해야 맞아. 지금 레포 28A는 구조는 잘 깔렸지만, 아직 `fixture_only: True`, mapped symbols 13개, archetype 8개만 쓰는 상태고, case library도 25개 archetype 중 **성공 2개 + 반례 2개** 기준을 충족한 게 0개야. 즉 아직 scoring을 바꾸면 안 되고, 케이스 매트릭스를 더 채워야 한다.

그리고 이 작업은 단순히 종목을 많이 나열하는 게 아니라, **각 archetype에서 EPS/FCF 체급 변화가 왜 지속되는지, 반대로 왜 일회성·사이클·테마 과열인지**를 구분해야 해. 이게 서생원식 원칙의 핵심인 “산업 구조 변화 → EPS/FCF 체급 변화 → 시장의 과거 프레임 → 밸류에이션 리레이팅”이랑 맞아.

아래는 **Round 4 확장판**이야. 이번에는 지난번에 빈 곳으로 남았던 플랫폼, 게임/IP, 리테일, 건설/PF, 유틸리티/원전, 지주/거버넌스, 로봇, 바이오, 의료기기, 금융, 그리고 추가로 분리해야 할 archetype까지 채웠어.

---

# 0. 이번 라운드에서 추가로 나눠야 할 Archetype

기존 25개에 더해, 실전에서는 아래 5개를 별도 archetype 또는 sub-archetype으로 분리하는 게 좋아 보여.

| 추가 Archetype                                 | 왜 따로 봐야 하나                                                            |
| -------------------------------------------- | --------------------------------------------------------------------- |
| **AI Data Center Infrastructure**            | 전력기기만으로 부족함. 냉각, 전력망, IDC, 서버, 통신망, ESS가 같이 움직임.                      |
| **Nuclear / SMR / Grid Policy**              | 유틸리티와 다름. 정책·수주·CAPEX·원전 수출·규제 리스크가 핵심.                               |
| **Travel / Leisure / Reopening**             | 리테일과 다름. 항공, 카지노, 호텔, 면세, 여행 수요는 강한 사이클성이 있음.                         |
| **Education / Testing / Specialty Services** | 반복매출/정책/입시/해외 확장 구조가 플랫폼과 다름.                                         |
| **Rare Metals / Strategic Materials**        | 단순 commodity보다 공급망·지정학·제련마진·M&A/지배구조가 중요함. Korea Zinc 같은 사례는 여기에 가까움. |

이건 기존 25개를 버리자는 게 아니라, **case library가 커지면 세분화해야 할 후보**야.

---

# 1. Robotics / Factory Automation

## 핵심 구조

```text
테마 기대
→ 실제 고객사 도입
→ 수주/매출 전환
→ 반복 서비스·소모품·SW 매출
→ OPM 개선
```

로봇은 “미래 성장”만으로는 E2R이 아니야. 실제로 EPS/FCF가 바뀌는 구조가 있어야 한다.

## 성공 후보

| 구분    | 케이스                                          | 왜 봐야 하나                                                                                                                                        |
| ----- | -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| 성공 후보 | **Rainbow Robotics**                         | 삼성전자가 Rainbow Robotics 지분을 추가 취득해 최대주주가 되었고, Future Robotics Office를 CEO 직속으로 신설했다는 Reuters 보도가 있음. 이건 단순 테마가 아니라 대기업 전략 편입 신호. ([Reuters][1]) |
| 성공 후보 | **Doosan Robotics**                          | 협동로봇, 글로벌 지사, 제품군 확장. 다만 상장 후 밸류와 실적 괴리 확인 필요.                                                                                                 |
| 성공 후보 | **Hyundai Motor / Boston Dynamics exposure** | Hyundai의 robotics ambition이 주가 프레임을 바꿀 수 있다는 Breakingviews 보도. 단, 자동차 본업 EPS와 로봇 기대를 분리해야 함. ([Reuters][2])                                    |
| 성공 후보 | **Neuromeka / Robotis / SBB Tech**           | 실제 수주·반복매출·고객사 도입 여부 확인 필요.                                                                                                                    |

## 반례

| 반례                     | 왜 위험한가                                                 |
| ---------------------- | ------------------------------------------------------ |
| **무실적 로봇 테마주**         | 뉴스·MOU만 있고 매출화 없으면 Stage 1 이상 주기 어렵다.                  |
| **두산로보틱스류 고밸류 IPO 구간** | 제품력은 있어도 EPS/FCF가 주가를 따라오지 않으면 Theme Overheat로 분류해야 함. |
| **대기업 투자 뉴스만 있는 소형주**  | 전략적 지분투자가 실제 수주·매출·마진으로 이어지는지 확인 필요.                   |

## Stage 기준

```text
Stage 1:
- 대기업 투자
- 로봇 정책/테마
- MOU/PoC
- 거래대금 증가

Stage 2:
- 실제 고객사 도입
- 매출화
- 수주잔고
- gross margin 개선
- 반복 서비스 매출 근거

Stage 3:
- 고객사 다변화
- 반복매출/소모품/SW revenue
- OPM 개선
- valuation이 아직 테마주가 아니라 산업재/플랫폼 전환을 덜 반영

4B:
- humanoid/robotics 과열
- 주가가 EPS보다 먼저 감
- 여러 리포트가 장밋빛 TAM만 강조

4C:
- 수주 지연
- 매출화 실패
- 대기업 투자 철회
- 현금흐름 악화
```

## 점수 방향

```text
EPS/FCF: 18~20
Visibility: 15
Bottleneck/Pricing: 10
Mispricing: 12
Valuation: 10
Theme penalty: 강하게
```

**Green은 매우 제한.**
로봇은 대부분 Stage 1~2 또는 Stage 3-Watch가 맞고, Green은 실제 반복매출 구조가 확인된 경우만 가능.

---

# 2. Platform / Software / Internet

## 핵심 구조

```text
트래픽/MAU
→ ARPU/take rate 상승
→ 비용 효율화
→ OPM 레버리지
→ 반복매출/lock-in
```

플랫폼은 “사용자가 많다”만으로는 부족해. **수익화와 마진 레버리지**가 핵심이다.

## 성공 후보

| 구분    | 케이스                                | 왜 봐야 하나                                                          |
| ----- | ---------------------------------- | ---------------------------------------------------------------- |
| 성공 후보 | **NAVER**                          | 광고·커머스·AI 비용효율화, 일본/글로벌 exposure. 다만 AI CAPEX 비용이 마진을 먹는지 확인 필요. |
| 성공 후보 | **Kakao 일부 턴어라운드 구간**              | 비용 구조조정, 광고/커머스 회복이 있으면 후보. 단, 규제·지배구조 리스크 큼.                    |
| 성공 후보 | **더존비즈온**                          | ERP/SaaS성 반복매출, AI/클라우드 전환, OPM 개선 여부.                           |
| 성공 후보 | **글로벌 비교: Adobe / Microsoft SaaS** | recurring revenue와 price increase가 구조적 visibility인 비교군.          |

## 반례

| 반례                                      | 왜 위험한가                                         |
| --------------------------------------- | ---------------------------------------------- |
| **MAU만 높은 플랫폼**                         | 트래픽이 수익화되지 않으면 EPS 체급 변화가 아님.                  |
| **규제 플랫폼**                              | 수수료, 광고, 데이터, 독점규제 리스크가 수익모델을 깰 수 있음.          |
| **AI 비용만 늘어나는 플랫폼**                     | AI narrative는 있지만 GPU/서버 비용 때문에 FCF가 악화될 수 있음. |
| **카카오식 governance/regulatory overhang** | 지배구조·규제·사회적 비용이 valuation rerating을 막을 수 있음.   |

## Stage 기준

```text
Stage 1:
- MAU/traffic 회복
- 광고/커머스 회복
- 비용절감 뉴스
- AI/클라우드 신사업

Stage 2:
- ARPU 상승
- take rate 개선
- OPM 개선
- 반복매출 증가
- FY1/FY2 OP 상향

Stage 3:
- recurring revenue lock-in
- 비용 레버리지
- pricing power
- regulation risk 낮음
- 시장이 아직 저성장 플랫폼 프레임으로 평가

4B:
- multiple expansion 완료
- AI/플랫폼 narrative 과열
- ARPU 성장 둔화

4C:
- 규제
- take rate 하락
- 트래픽 감소
- AI 비용 과다
```

## 점수 방향

```text
EPS/FCF: 20
Visibility: 22
Bottleneck/Pricing: 8
Mispricing: 16
Valuation: 14
Risk: regulation, AI cost
```

---

# 3. Game / Content / IP

## 핵심 구조

```text
IP / 신작 / 팬덤
→ 글로벌 매출
→ 반복 monetization
→ OPM leverage
```

게임·콘텐츠는 hit-driven이라서 Green을 쉽게 주면 안 돼. **신작 기대가 아니라, IP의 반복성과 글로벌 매출화**가 중요하다.

## 성공 후보

| 구분    | 케이스                 | 왜 봐야 하나                                                                                                                              |
| ----- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 성공 후보 | **Krafton**         | PUBG/BGMI 글로벌 IP, 인도 exposure, 대형 투자. Krafton은 BGMI가 2.4억 다운로드 이상이라는 Reuters 보도가 있음. ([Reuters][3])                                  |
| 성공 후보 | **Shift Up**        | Nikke, Stellar Blade, Sony second-party, 높은 OPM 가능성. Shift Up은 2024년 IPO와 Stellar Blade 판매 모멘텀, 2025년 매출·영업이익 성장 자료가 있음. ([위키백과][4]) |
| 성공 후보 | **HYBE / JYP / SM** | IP/투어/팬덤 monetization. 다만 아티스트 계약/스캔들 리스크.                                                                                           |
| 성공 후보 | **콘텐츠 제작사**         | 글로벌 OTT 판매가 반복화되는지 확인 필요.                                                                                                            |

## 반례

| 반례                  | 왜 위험한가                              |
| ------------------- | ----------------------------------- |
| **신작 기대만 있는 게임주**   | 출시 후 매출이 안 나오면 바로 4C.               |
| **단일 IP 의존**        | 한 게임/한 아티스트 흥행에 의존하면 visibility 낮음. |
| **엔터 계약 리스크**       | 핵심 아티스트 재계약·스캔들·군입대 등은 4C 조건.       |
| **중국 판호/규제 의존 게임주** | 외부 정책 리스크 큼.                        |

## Stage 기준

```text
Stage 1:
- 신작/컴백/투어
- 예약판매
- 글로벌 흥행 뉴스
- 트래픽/다운로드 증가

Stage 2:
- 실제 매출화
- OP/EPS 상향
- IP 반복성 확인

Stage 3:
- IP portfolio
- 글로벌 monetization
- 낮은 churn
- 반복 revenue 구조
- valuation이 아직 단일 hit 프레임

4B:
- 흥행 peak
- 신작 기대 과열
- multiple saturation

4C:
- 신작 실패
- 핵심 IP 훼손
- 계약/스캔들 리스크
```

## 점수 방향

```text
EPS/FCF: 20
Visibility: 18
Bottleneck/Pricing: 5~8
Mispricing: 14
Valuation: 12
Risk: hit-driven discount
```

---

# 4. Retail / Domestic Consumer

## 핵심 구조

```text
소비 회복
→ 점포효율 / 객단가 / 비용레버리지
→ OPM 개선
```

리테일은 대부분 구조적 E2R보다는 경기/소비 사이클에 가까워. Green은 **점포 효율과 비용 구조가 바뀌는 경우**만 가능.

## 성공 후보

| 구분    | 케이스              | 왜 봐야 하나                                                                           |
| ----- | ---------------- | --------------------------------------------------------------------------------- |
| 성공 후보 | **BGF리테일 / CU**  | 편의점 점포망, 해외 확장, PB상품, 점포효율. CU는 2025년 기준 18,000개 이상 매장과 해외 확장을 갖고 있음. ([위키백과][5]) |
| 성공 후보 | **GS리테일 / GS25** | 편의점 점포 수, PB상품, 해외 진출. GS25는 2024년 전국 18,000개 이상 점포로 정리됨. ([위키백과][6])             |
| 성공 후보 | **신세계 / 호텔신라**   | 관광·면세 회복, 중국/일본 관광객 mix 확인 필요.                                                    |
| 성공 후보 | **올리브영 관련 CJ**   | K뷰티 유통 플랫폼 성격이 강해 K-beauty와 cross-over.                                           |

## 반례

| 반례                                        | 왜 위험한가                              |
| ----------------------------------------- | ----------------------------------- |
| **대형마트 구조 경쟁 심화**                         | 이커머스와 가격경쟁으로 OPM이 낮아질 수 있음.         |
| **Homeplus류 leverage/balance sheet risk** | 사모펀드·부채·오프라인 경쟁 리스크.                |
| **단기 소비 회복 테마**                           | 트래픽 증가만 있고 OPM/FCF 개선이 없으면 Stage 1. |
| **면세 중국 의존**                              | 관광객 mix가 깨지면 4C.                    |

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

## 점수 방향

```text
EPS/FCF: 18
Visibility: 16
Bottleneck/Pricing: 5
Mispricing: 14
Valuation: 14
Risk: inventory, rent, wage, competition
```

---

# 5. Construction / Real Estate / Credit

## 핵심 구조

```text
수주/분양보다 PF·현금흐름·원가율이 먼저
```

건설은 겉으로 수주잔고가 커 보여도 PF/미분양/원가 리스크가 크면 Green 금지.

## 성공 후보

| 구분    | 케이스                     | 왜 봐야 하나                                               |
| ----- | ----------------------- | ----------------------------------------------------- |
| 성공 후보 | **PF 리스크 해소형 건설사**      | 부실 프로젝트 정리 후 cash flow 회복.                            |
| 성공 후보 | **해외 플랜트/인프라 수주형**      | 수주잔고 질과 마진이 확정적이면 후보.                                 |
| 성공 후보 | **Yongsan/대형개발 관련 인프라** | 대형 프로젝트는 Stage 1 radar 가능. 다만 긴 기간과 financing risk 큼. |

## 반례

| 반례                      | 왜 위험한가                                                                                                                           |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Taeyoung E&C류 PF 문제** | Reuters는 한국 정부가 고금리와 부동산 침체로 어려운 중소기업·건설사를 지원하기 위해 40.6조원 규모 지원을 준비했다고 보도했고, Taeyoung E&C 등 중견 건설사 유동성 우려가 배경이었다. ([Reuters][7]) |
| **PF 연체율 상승**           | Reuters는 부동산 프로젝트 연체율이 2021년 말 0.37%에서 2023년 말 2.70%로 상승했다고 보도. ([Reuters][8])                                                   |
| **원가 상승 미반영**           | 매출은 늘지만 원가율 상승으로 OP/FCF 훼손.                                                                                                      |
| **미분양 증가**              | 수주가 있어도 현금흐름이 막힘.                                                                                                                |

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

## 점수 방향

```text
EPS/FCF: 18
Visibility: 10~12
Bottleneck/Pricing: 5
Mispricing: 12
Valuation: 10
Risk penalty: 매우 큼
```

---

# 6. Utilities / Regulated Tariff

## 핵심 구조

```text
정책·요금·원가
→ EPS 턴어라운드
→ 그러나 규제 리스크가 항상 큼
```

유틸리티는 “싸다”보다 **요금/원가/정책 프레임이 바뀌는지**가 핵심.

## 성공 후보

| 구분    | 케이스                       | 왜 봐야 하나                                                    |
| ----- | ------------------------- | ---------------------------------------------------------- |
| 성공 후보 | **KEPCO**                 | 요금 정상화, 원가 안정, 부채. 다만 정책 리스크가 큼.                           |
| 성공 후보 | **한국가스공사**                | 미수금 회수, 원가보상, 배당 가능성.                                      |
| 성공 후보 | **전력망/송전 인프라 관련사**        | 유틸리티보다는 AI data center / grid capex archetype과 cross-over. |
| 성공 후보 | **원전 수출 관련 KHNP/두산에너빌리티** | 원전/SMR은 별도 Nuclear archetype으로 분리 필요.                      |

## 반례

| 반례            | 왜 위험한가                                                          |
| ------------- | --------------------------------------------------------------- |
| **요금 동결**     | EPS 개선 지속성 낮음.                                                  |
| **부채 과다**     | 주주환원 불가능.                                                       |
| **정책 변동성**    | 정부 요금정책이 thesis를 좌우.                                            |
| **전력시장 구조왜곡** | 한국 전력시장의 가격 신호 왜곡이 재생에너지/전력 투자 효율을 해친다는 최근 연구도 있음. ([arXiv][9]) |

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
- 배당/주주환원 가능성

4B:
- 요금정상화 기대 선반영
- 원가 하락 peak

4C:
- 요금 동결
- 원가 급등
- 정책 반전
- 부채 부담 확대
```

## 점수 방향

```text
EPS/FCF: 18
Visibility: 18
Bottleneck/Pricing: 5
Mispricing: 12
Valuation: 10
Regulatory risk cap
```

---

# 7. Nuclear / SMR / Grid Policy — 추가 Archetype 후보

## 왜 별도 분리?

원전은 유틸리티와 달라.
**정책 + 수출 수주 + CAPEX + 원가경쟁력 + 규제/소송 리스크**가 같이 움직인다.

## 성공 후보

| 구분    | 케이스               | 왜 봐야 하나                                                                                                     |
| ----- | ----------------- | ----------------------------------------------------------------------------------------------------------- |
| 성공 후보 | **두산에너빌리티**       | 원전 수출, SMR, 터빈/주기기.                                                                                         |
| 성공 후보 | **한전기술 / 한전KPS**  | 원전 설계·정비.                                                                                                   |
| 성공 후보 | **KHNP 체코 원전 관련** | FT는 체코 법원이 프랑스 EDF의 이의제기로 한국 KHNP의 180억 달러 원전 계약을 중단시켰다고 보도. 수주 성공뿐 아니라 법적 리스크도 중요. ([Financial Times][10]) |

## 반례

```text
- 원전 테마만 있는 소형주
- 수주 발표 전 기대감 과열
- 소송/정책 리스크
- 프로젝트 지연
```

## Stage 기준

```text
Stage 1:
- 원전 정책/수출 뉴스
- 입찰 우선협상대상자
- SMR 테마

Stage 2:
- 실제 계약/LOI
- project financing
- 기자재 매출화 경로

Stage 3:
- 다년 수주잔고
- 수익성/마진 확인
- 소송/정책 리스크 낮음

4B:
- 수주 기대가 가격에 선반영
- 모든 원전주 동반 과열

4C:
- 소송 패소/지연
- 정책 반전
- 원가 상승/수익성 훼손
```

---

# 8. Holding / Governance / Restructuring

## 핵심 구조

```text
NAV discount
→ 자사주/소각/배당/지배구조 개선
→ Korea discount 해소
```

## 성공 후보

| 구분    | 케이스                              | 왜 봐야 하나                                                                                                    |
| ----- | -------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 성공 후보 | **SK스퀘어**                        | 자회사 NAV, 반도체 exposure, 자사주/소각 여부.                                                                          |
| 성공 후보 | **삼성물산 / 삼성생명**                  | 지배구조, 자산가치, 주주환원.                                                                                          |
| 성공 후보 | **Korea Zinc governance battle** | Reuters는 MBK/Young Poong의 Korea Zinc 공개매수가 경영권·거버넌스·기업가치 논쟁을 만들었고, 주가가 공개매수 발표 후 급등했다고 보도. ([Reuters][11]) |
| 성공 후보 | **Korea Zinc 2025 주총/경영권 분쟁**    | Reuters는 Korea Zinc 특별주총에서 경영권 분쟁이 4개월간 이어졌고, 이사회 구성을 둘러싼 표대결이 있었다고 보도. ([Reuters][12])                    |

## 반례

| 반례                 | 왜 위험한가                               |
| ------------------ | ------------------------------------ |
| **자사주 발표만 있는 지주사** | 소각·배당·지배구조 개선 없이 할인 지속.              |
| **경영권 분쟁만 있는 종목**  | 주가 이벤트는 있지만 EPS/FCF 체급 변화가 아닐 수 있음.  |
| **자회사 가치 훼손**      | NAV discount가 정당화.                   |
| **주주환원 불확실**       | policy promise만 있고 실행 없으면 Stage 1~2. |

## Stage 기준

```text
Stage 1:
- 자사주/소각/배당 발표
- 경영권 분쟁
- value-up 공시

Stage 2:
- 실제 소각
- 주주환원 정책 반복
- 자회사 실적 개선
- discount 축소 가능성

Stage 3:
- governance regime change
- 반복 환원정책
- NAV discount 구조적 해소
- 시장이 여전히 지주사 discount로 평가

4B:
- 이벤트 프리미엄 과열
- 소각/분쟁 결과 반영 완료

4C:
- 환원 미이행
- 자회사 가치 훼손
- 지배주주 리스크 재부각
```

## 점수 방향

```text
EPS/FCF: 10~12
Visibility: 18
Mispricing: 20
Valuation: 25
Capital allocation: 10
Governance execution이 핵심
```

---

# 9. Financial Spread / Balance Sheet

## 보강

금융은 일반 제조업과 다르게 EPS 폭발보다:

```text
ROE 지속성
PBR-ROE gap
자본비율
주주환원
충당금/부실 리스크
```

를 봐야 한다.

## 성공 후보

```text
KB금융
신한지주
하나금융
메리츠금융
삼성화재
DB손해보험
```

## 반례

```text
단순 저PBR 지방은행
PF/부동산 충당금 리스크 은행
자본비율 낮은 보험/증권
배당만 높고 ROE가 하락하는 금융주
```

## 정책 배경

한국의 corporate value-up과 상법/거버넌스 개혁은 저PBR 금융주 리레이팅의 배경이 될 수 있지만, 정책만으로 Green을 주면 안 돼. **ROE와 실제 환원정책**이 같이 있어야 한다. 레포의 서생원 원칙도 “시장 프레임이 틀렸다는 증거”가 필요하다고 강조해.

## Stage 기준

```text
Stage 1:
- value-up 공시
- 자사주/배당
- 저PBR

Stage 2:
- ROE 개선
- CET1/자본비율 안정
- 충당금 안정
- 환원정책 실행

Stage 3:
- PBR-ROE 프레임 변화
- 반복 환원
- credit risk 낮음
- 시장이 여전히 저PBR value trap으로 평가

4B:
- PBR이 ROE 대비 정상화
- 모두가 value-up 성공주로 인정

4C:
- credit cost 증가
- PF 부실
- 자본비율 악화
```

---

# 10. Biotech / Regulatory

## 더 세분화 필요

바이오는 하나로 묶으면 위험해. 최소 3개로 나눠야 해.

```text
A. Pre-revenue clinical biotech
B. Royalty / technology-transfer biotech
C. Revenue-generating pharma / CDMO
```

## 케이스 후보

| 구분    | 케이스                  | 분류                                               |
| ----- | -------------------- | ------------------------------------------------ |
| 성공 후보 | **알테오젠**             | 기술이전/로열티 가능성. B형.                                |
| 성공 후보 | **유한양행**             | 신약 허가·로열티·매출화. B~C형.                             |
| 성공 후보 | **삼성바이오로직스**         | CDMO 장기계약/가동률. 사실상 Contract/Backlog Healthcare형. |
| 성공 후보 | **셀트리온**             | 바이오시밀러 매출화, 글로벌 판매. C형.                          |
| 반례    | 임상 뉴스만 있는 바이오        | A형. Green 금지.                                    |
| 반례    | CB/유증 반복 바이오         | dilution risk.                                   |
| 반례    | 기술이전 headline만 있는 기업 | milestone/royalty 불확실하면 Stage 1~2.               |

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
- 신약 기대가 과열
- valuation이 매출화보다 먼저 감

4C:
- 임상 실패
- 허가 지연
- 유증/CB
- 파트너 계약 해지
```

## 점수 방향

```text
Pre-revenue:
Green 거의 금지

Royalty/tech transfer:
Visibility는 milestone/royalty 확률 기반

CDMO/revenue pharma:
일반 E2R처럼 EPS/FCF 가능
```

---

# 11. Medical Device / Healthcare Export

## 보강

의료기기는 바이오와 달라.
제품이 팔리고, 소모품/시술이 반복되면 훨씬 E2R에 가깝다.

## 성공 후보

| 케이스         | 이유                                      |
| ----------- | --------------------------------------- |
| **Classys** | 비침습 피부미용 의료기기, 60개국 이상 수출. ([위키백과][13]) |
| **파마리서치**   | 미용·재생 제품, 수출·반복시술.                      |
| **휴젤**      | 톡신/필러, 글로벌 허가와 판매.                      |
| **원텍**      | 미용기기, 장비+소모품 구조 확인 필요.                  |

## 반례

```text
- 단일 장비 판매만 있는 기업
- 허가 지연
- 소모품 반복 매출 없음
- 경쟁 심화로 ASP 하락
```

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

---

# 12. Commodity / Rare Metals / Strategic Materials

기존 Commodity Spread에 **Rare Metals / Strategic Materials**를 별도 sub-archetype으로 추가해야 해.

## 왜 분리?

Korea Zinc 같은 경우는 단순 아연 가격 스프레드가 아니라:

```text
제련마진
전략금속 공급망
경영권/거버넌스
M&A/공개매수
2차전지 소재 exposure
```

가 섞인다.

## 케이스

| 구분          | 케이스               | 이유                                                                                                           |
| ----------- | ----------------- | ------------------------------------------------------------------------------------------------------------ |
| 성공/이벤트 후보   | **Korea Zinc**    | 경영권 분쟁, 자사주/공개매수, 공급망 중요성. Reuters는 MBK/Young Poong 공개매수 발표 후 Korea Zinc 주가가 19.8% 상승했다고 보도. ([Reuters][11]) |
| 이벤트/거버넌스 후보 | **Korea Zinc 주총** | 특별주총, 이사회 구성 표대결, 거버넌스 변화 가능성. ([Reuters][12])                                                               |
| 반례          | 순수 금속가격 상승        | 가격만으로는 구조적 visibility 낮음.                                                                                    |
| 반례          | 경영권 이벤트만 있는 종목    | EPS/FCF 변화 없이 이벤트 프리미엄만 있으면 4B/Red.                                                                          |

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

---

# 13. 추가 Empty Archetype: Travel / Leisure / Reopening

이건 기존 Retail에 넣기엔 다르다.

## 구조

```text
출입국/관광 회복
→ 객실/카지노/면세/항공 수요
→ OP leverage
→ 하지만 경기·환율·정책·중국 의존 리스크 큼
```

## 성공 후보

```text
파라다이스 / GKL:
카지노 방문객, 중국/일본 VIP, drop amount.

호텔신라 / 신세계:
면세/관광 회복.

대한항공 / 아시아나:
여객 회복, 화물 정상화, 유가/환율.
```

## 반례

```text
- 중국 단체관광 기대만 있는 면세주
- 유가 급등 항공주
- 환율/경기 둔화
- 이벤트성 여행 회복 후 둔화
```

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
- 규제/중국 리스크
```

---

# 14. 추가 Empty Archetype: AI Data Center Infrastructure

이건 앞으로 매우 중요해. 기존 전력기기만으로 부족하다.

## 구조

```text
AI 데이터센터 증설
→ 전력/냉각/서버/네트워크/전력망 병목
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

## 성공 후보

```text
HD현대일렉트릭 / 효성중공업:
전력망/변압기

LS ELECTRIC / LS전선 관련:
전력망, 전선

이수페타시스:
AI 서버/네트워크 PCB

냉각/공조 관련 기업:
데이터센터 cooling exposure 확인 필요
```

## 반례

```text
- AI 데이터센터 테마만 붙은 기업
- 실제 수주/매출 exposure 없음
- CAPEX 기대는 크지만 valuation이 먼저 간 기업
```

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

---

# 15. 이번 라운드 후 우선순위

이제 제일 먼저 채워야 하는 건 아래 12개 archetype이야.

```text
1. CONTRACT_BACKLOG_INDUSTRIAL
2. DEFENSE_GOVERNMENT_BACKLOG
3. SHIPBUILDING_OFFSHORE_BACKLOG
4. EXPORT_RECURRING_CONSUMER
5. K_BEAUTY_EXPORT_DISTRIBUTION
6. MEMORY_HBM_CAPACITY
7. SEMI_EQUIPMENT_CAPEX
8. FINANCIAL_SPREAD_BALANCE_SHEET
9. MEDICAL_DEVICE_HEALTHCARE_EXPORT
10. THEME_VALUATION_OVERHEAT
11. ONE_OFF_EVENT_DEMAND
12. AI_DATA_CENTER_INFRASTRUCTURE
```

그 다음:

```text
13. ROBOTICS_FACTORY_AUTOMATION
14. PLATFORM_SOFTWARE_INTERNET
15. GAME_CONTENT_IP
16. SHIPPING_FREIGHT_CYCLE
17. CONSTRUCTION_REAL_ESTATE_CREDIT
18. UTILITIES_REGULATED_TARIFF
19. NUCLEAR_SMR_GRID_POLICY
20. HOLDING_RESTRUCTURING_GOVERNANCE
21. TRAVEL_LEISURE_REOPENING
22. BIOTECH_REGULATORY
23. RARE_METALS_STRATEGIC_MATERIALS
```

---

# 16. 점수 정규화 방향 업데이트

이제 점수비중을 이렇게 3레벨로 나누는 게 좋아.

## Level 1: Green 가능 Archetype

```text
Contract/Backlog
Defense
Shipbuilding
Export Consumer
K-Beauty
Memory/HBM
Semi Equipment
Medical Device
Financial
AI Data Center Infrastructure
Turnaround
```

이들은 증거가 충분하면 Stage 3-Green 가능.

## Level 2: Yellow/Watch 중심 Archetype

```text
Robotics
Platform/Software
Game/IP
Auto
Utilities
Nuclear/SMR
Holding/Governance
Rare Metals
Travel/Leisure
```

이들은 강한 후보가 나올 수 있지만, Green은 증거가 매우 탄탄해야 함.

## Level 3: Red/4B 방어 중심 Archetype

```text
Shipping
Commodity Spread
Battery Materials Overheat
Construction/Credit
Pre-revenue Biotech
One-off Event
Theme Overheat
```

이들은 EPS가 폭발해도 구조적 Green을 매우 제한해야 함.

---

# 17. 다음에 에이전트에 넣을 때 필요한 데이터 필드

케이스 매트릭스를 넣을 때는 단순 설명 말고 아래 필드로 넣어야 해.

```text
case_id
symbol
company_name
market
archetype
case_type:
  structural_success
  cyclical_success
  one_off
  overheat
  failed_rerating
  4b_graduation
  4c_thesis_break

stage1_date
stage2_date
stage3_date
stage4b_date
stage4c_date
peak_date

stage1_evidence
stage2_evidence
stage3_evidence
stage4b_evidence
stage4c_evidence

price_pattern:
  straight_rerating
  stair_step_rerating
  cycle_boom_bust
  theme_overheat
  accounting_trust_break
  event_premium
  slow_compounder

must_have_fields
red_flag_fields
score_weight_hint
```

---

# 18. 결론

응, 계속 채우는 게 맞다.
이번 라운드에서 빈 archetype을 꽤 많이 채웠고, 특히 아래가 더 선명해졌어.

```text
- 로봇은 Green보다 매출화 확인이 우선.
- 플랫폼은 MAU보다 ARPU/OPM/규제가 핵심.
- 게임/IP는 신작 기대보다 반복 monetization이 핵심.
- 리테일은 점포효율과 재고가 핵심.
- 건설은 수주보다 PF/현금흐름이 핵심.
- 유틸리티는 요금/정책/부채가 핵심.
- 원전은 유틸리티와 별도 archetype이 필요.
- 지주/거버넌스는 NAV discount와 환원 실행이 핵심.
- 금융은 PBR-ROE-환원 프레임.
- 바이오는 매출화 전 Green 금지.
- 의료기기는 반복 소모품/수출이면 E2R 가능.
- Korea Zinc류는 rare metals / governance / strategic materials로 따로 봐야 함.
- AI 데이터센터 인프라는 독립 archetype으로 추가할 가치가 큼.
```

다음 라운드에서는 이걸 더 구체적으로 **JSONL case record 형태**에 가까워지도록, 각 archetype별로 최소 2개 성공 + 2개 반례를 실제 후보명과 stage evidence로 더 채우는 쪽으로 가면 된다.

[1]: https://www.reuters.com/technology/samsung-electronics-becomes-largest-shareholder-south-koreas-rainbow-robotics-2024-12-30/?utm_source=chatgpt.com "Samsung Electronics becomes largest shareholder of South Korea's Rainbow Robotics"
[2]: https://www.reuters.com/commentary/breakingviews/hyundai-motors-robots-herald-hardware-reboot-2026-03-04/?utm_source=chatgpt.com "Hyundai Motor's robots herald hardware reboot"
[3]: https://www.reuters.com/world/asia-pacific/pubg-maker-krafton-leads-south-korean-trio-666-million-india-tech-bet-2025-12-19/?utm_source=chatgpt.com "PUBG maker Krafton leads South Korean trio in $666 million India tech bet"
[4]: https://en.wikipedia.org/wiki/Shift_Up?utm_source=chatgpt.com "Shift Up"
[5]: https://en.wikipedia.org/wiki/CU_%28store%29?utm_source=chatgpt.com "CU (store)"
[6]: https://en.wikipedia.org/wiki/GS25?utm_source=chatgpt.com "GS25"
[7]: https://www.reuters.com/markets/asia/south-korea-prepares-financial-support-small-businesses-builders-2024-03-27/?utm_source=chatgpt.com "South Korea prepares financial support for small businesses, builders"
[8]: https://www.reuters.com/markets/asia/south-korea-tightens-scrutiny-speed-up-real-estate-restructuring-2024-05-13/?utm_source=chatgpt.com "South Korea tightens scrutiny to speed up real estate restructuring"
[9]: https://arxiv.org/abs/2605.09318?utm_source=chatgpt.com "Price Distortions in Korea's Electricity Market: Barriers to Renewable Integration and Reform Pathways"
[10]: https://www.ft.com/content/4ee071b3-dbef-4d8b-a8d7-27099caa6926?utm_source=chatgpt.com "Czech court halts $18bn nuclear reactor deal after rival complaint"
[11]: https://www.reuters.com/markets/deals/private-equity-mbk-young-poong-launch-15-bln-tender-offer-korea-zinc-shares-2024-09-13/?utm_source=chatgpt.com "Private equity MBK, Young Poong launch $1.5 bln tender offer for Korea Zinc shares"
[12]: https://www.reuters.com/markets/commodities/korea-zinc-takeover-battle-culminates-shareholders-meeting-2025-01-22/?utm_source=chatgpt.com "Korea Zinc takeover battle culminates in shareholders' meeting"
[13]: https://en.wikipedia.org/wiki/Classys?utm_source=chatgpt.com "Classys"
