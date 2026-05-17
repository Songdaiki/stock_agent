응. 한 라운드 더 채웠어. 이번 라운드는 그냥 “후보 종목 추가”가 아니라, **주가가 어떤 국면에서 움직였는지까지 엮어서 Stage 1 → Stage 2 → Stage 3 → Stage 4B/4C 구조를 더 선명하게 만드는 쪽**으로 정리했어.

지금 레포 28A는 뼈대는 맞지만 아직 `fixture_only: True`, mapped symbols 13개, archetypes used 8개뿐이고, case library도 25개 archetype 중 2개 성공 + 2개 반례 조건을 충족한 항목이 0개야. 즉 이 단계에서 바로 점수비중을 적용하면 또 편향될 수 있어.
서생원식 원칙상 핵심은 “좋은 섹터”가 아니라 **EPS/FCF 체급 변화가 몇 년 지속될 구조적 근거와, 시장이 아직 과거 프레임으로 보는 오해**를 찾는 거야. 그래서 이번 라운드는 성공 사례뿐 아니라 “비슷해 보였지만 정통 E2R이 아니었던 반례”까지 더 세게 넣었어.

---

# 0. 이번 라운드의 핵심 변화

이번에는 각 archetype을 이렇게 다시 봤어.

```text
1. Stage 1 레이더:
   처음 시장에 잡힐 만한 신호

2. Stage 2 후보 편입:
   EPS/OP/FCF 또는 수주/수출/가격/마진 증거가 붙는 구간

3. Stage 3 고확신:
   몇 년 지속될 구조적 visibility와 리레이팅 근거가 같이 있는 구간

4. Stage 4B:
   논리는 아직 살아 있지만 주가/밸류/리포트 톤이 많이 반영된 졸업·과열 감시 구간

5. Stage 4C:
   EPS 경로, 계약, 수요, 가격, 회계, 규제 등 핵심 논리가 깨지는 구간
```

그리고 주가 쪽은 exact MFE/MAE 숫자를 아직 다 계산한 건 아니고, 이번에는 **주가 패턴 타입**을 더 정교하게 붙였어. 예를 들면:

```text
A. 리레이팅 직행형:
   Stage 2 이후 조정 없이 급등하는 유형

B. 계단식 리레이팅형:
   Stage 2 이후 20~30% 조정 반복 후 계속 상승

C. 사이클 폭발 후 정상화형:
   EPS는 폭발하지만 4B/4C가 빨리 와야 하는 유형

D. 테마 선반영형:
   가격이 먼저 가고 EPS/FCF가 못 따라오는 유형

E. 회계/신뢰 붕괴형:
   Stage 2~3처럼 보이다가 신뢰 이슈로 4C가 터지는 유형
```

---

# 1. CONTRACT_BACKLOG_INDUSTRIAL

전력기기, 전선, 일부 산업재

## 성공 케이스 보강

| 구분    | 케이스                | Stage 구조                                                  | 주가 패턴                                                      |
| ----- | ------------------ | --------------------------------------------------------- | ---------------------------------------------------------- |
| 성공    | HD현대일렉트릭           | 공급계약, 수주잔고, 북미 전력망, 리드타임, OPM 개선. 현재 레포에서도 Stage 2까지 올라감. | **계단식 리레이팅형.** 수주/리포트가 붙은 뒤 단발이 아니라 여러 달 반복 후보로 유지되는 게 중요. |
| 성공    | 일진전기               | 장기공급계약, 계약금액/매출, 초고압 전력기기, CAPA. 현재 레포에서 Stage 2.         | **후발 리레이팅형.** HD/효성이 먼저 간 뒤 섹터 확산으로 따라붙는 유형.               |
| 성공 후보 | 효성중공업              | 저마진 수주 정리, 중공업 마진 개선, 수주잔고. 현재 점수는 Stage 2 직전.            | **마진 정상화 리레이팅형.** 계약보다 “저마진 물량 정리 → OPM 개선”이 핵심.           |
| 성공 후보 | LS ELECTRIC / 제룡전기 | 전력망/변압기/전력기기 확산 후보.                                       | **섹터 확산형.** 섹터 leader보다 늦게 Stage 1→2로 확산 가능.               |

## 반례 보강

| 반례          | 왜 반례인가                                              | Stage 처리                |
| ----------- | --------------------------------------------------- | ----------------------- |
| 대한전선-like   | 전력기기/전선 테마는 있지만 희석, 낮은 OPM/ROE, 약한 계약질이면 정통 E2R 아님. | Stage 1~2 가능, Green 금지. |
| 단기 공급계약 테마주 | 계약이 있어도 매출 대비 작고 기간 짧고 마진 불명확하면 EPS 체급 변화가 아님.      | Stage 1, 최대 Yellow.     |
| CAPA 과잉 전환  | 공급부족 논리가 깨지고 경쟁사 증설이 빨리 나오면 4C.                     | 4B-watch → 4C.          |

## 점수 보정 방향

```text
Stage 3 Green에 필요한 것:
- 계약금액/매출 20%+
- 계약기간 3년+
- 수주잔고/매출 100%+
- FY1/FY2 OP/EPS 상향
- 리드타임 장기화 또는 CAPA 부족
- OPM 개선

Stage 4B:
- 목표가 상향이 여러 증권사에서 반복
- PER/PBR 프레임이 이미 새 프레임으로 이동
- 신규수주 모멘텀 둔화

Stage 4C:
- 계약 취소/지연
- ASP/OPM 하락
- 수주잔고 감소
```

**이 archetype은 Green을 줄 수 있는 archetype이지만, 계약 크기만으로 Green을 주면 안 돼.** 계약 규모 + 기간 + 마진 + 수주잔고 + EPS 상향이 같이 있어야 한다.

---

# 2. DEFENSE_GOVERNMENT_BACKLOG

방산, 항공우주, 정부 장기계약

## 성공 케이스 보강

| 구분    | 케이스       | Stage 구조                                                                                                                                     | 주가 패턴                                                     |
| ----- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| 성공    | 한화에어로스페이스 | 해외 정부 장기계약, 수주잔고 급증, 규모의 경제, OPM 개선. Reuters는 루마니아 K9 계약이 약 10억 달러 규모이고 2029년까지 진행되며, 방산 수주잔고가 2021년 말 5.1조원에서 2024년 3월 약 30조원까지 증가했다고 보도했어. | **백로그 리레이팅형.** 계약 하나가 아니라 수주잔고 체급이 바뀌는 구조. ([Reuters][1]) |
| 성공 후보 | 현대로템      | K2 전차 폴란드 2차 계약. Reuters는 폴란드가 180대 K2 추가 계약을 체결했고, 약 65억 달러 규모로 보도했어.                                                                       | **정부계약 누적형.** 수주잔고와 납품 스케줄이 핵심. ([Reuters][2])            |
| 성공 후보 | LIG넥스원    | 미사일/방공 수요.                                                                                                                                   | **지정학 수요형.** 수주 공시와 실적 반영 확인 필요.                          |
| 성공 후보 | 한국항공우주    | FA-50, KF-21, 정부·해외 발주.                                                                                                                      | **프로그램 milestone형.** 수주→납품→매출 인식까지 시간차 큼.                 |

## 반례

```text
1. 방산 테마 소형주:
   실제 정부 고객, 수주잔고, 납품 스케줄이 없으면 Green 금지.

2. 납기 지연/원가 상승 방산:
   수주잔고는 커도 OPM이 깨지면 4C.

3. 정치/수출허가 리스크:
   계약 체결 전 기대만으로 Stage 3 금지.
```

## Stage 기준

```text
Stage 1:
- 방산 계약 뉴스
- 지정학 수요
- 정부 고객 언급

Stage 2:
- 실제 계약금액
- 수주잔고/매출 상승
- 납품 스케줄
- OP/EPS 상향

Stage 3:
- 다년 정부계약
- 수출 비중 확대
- OPM 개선
- FY2/FY3 추정치 상향
- 시장이 아직 “내수 방산”으로 평가

4B:
- 방산주 전반 과열
- 신규 계약 기대가 주가에 선반영
- target multiple 포화

4C:
- 납기 지연
- 원가 상승
- 계약 취소
- 수출허가/정치 리스크
```

---

# 3. SHIPBUILDING_OFFSHORE_BACKLOG

조선, 조선기자재, 해양플랜트

## 성공 케이스 보강

| 구분    | 케이스                | Stage 구조                                                                                                | 주가 패턴                                              |
| ----- | ------------------ | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| 성공 후보 | 삼성중공업              | 선가 상승, 신규수주, 저가수주 소진. WSJ는 한국 조선주가 계약 재개와 신조선가 상승으로 랠리했고, 삼성중공업은 당시 16% 급등했다고 보도했어.                     | **선가/수주 동시 리레이팅형.** ([The Wall Street Journal][3]) |
| 성공 후보 | HD현대중공업 / HD한국조선해양 | LNG선, 특수선, 슬롯, 선가 상승.                                                                                   | **수주잔고 질 개선형.**                                    |
| 성공 후보 | 한화오션               | LNG + 방산 조선 + 미 해군 MRO. 한화오션은 미 해군 MRO와 미국 조선 인프라 투자 이슈가 있었고, 중국 제재 뉴스 때 주가 급락도 나와 지정학 리스크까지 case화 가능해. | **MRO 기대 + 지정학 리스크 혼합형.** ([AP News][4])           |

## 반례

```text
1. 저가수주 잔존 조선사:
   수주잔고는 많아도 적자 호선이면 visibility 낮음.

2. 러시아/Zvezda 계약 취소:
   대형 계약도 지정학/제재/결제 리스크가 있으면 4C.

3. 후판가/인건비 상승:
   선가 상승보다 원가 상승이 빠르면 EPS 훼손.
```

## Stage 기준

```text
Stage 1:
- 대형 수주
- 신조선가 상승
- 거래대금 증가

Stage 2:
- 저가수주 소진
- OP 흑자전환
- 고마진 선박 인도 시작

Stage 3:
- 수주잔고 질 개선
- 선가 상승분이 FY2/FY3 OP에 반영
- 원가 안정
- 장기 인도 슬롯

4B:
- 신조선가 피크
- 신규수주 피크
- 모두가 조선 턴어라운드를 인정

4C:
- 계약 취소
- 후판가/인건비 급등
- 발주 사이클 둔화
```

---

# 4. EXPORT_RECURRING_CONSUMER

음식료, 소비재 수출

## 성공 케이스 보강

| 구분    | 케이스  | Stage 구조                                                                                                                 | 주가 패턴                                                           |
| ----- | ---- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------- |
| 성공    | 삼양식품 | 불닭 수출, 미국/유럽 선적, ASP 상승, CAPA 확장, OP/EPS 상향. MarketWatch는 Kiwoom이 2Q 영업이익 추정치를 전년 대비 84% 증가로 올리고 목표가를 83만원으로 상향했다고 보도했어. | **수출 소비재 리레이팅형.** 내수 음식료 프레임이 글로벌 브랜드 프레임으로 바뀌는 구조. ([마켓워치][5]) |
| 성공 후보 | 농심   | 미국 라면, 해외 매출, 반복소비.                                                                                                      | **반복소비 확장형.**                                                   |
| 성공 후보 | 오리온  | 중국/베트남/러시아 포트폴리오, OPM.                                                                                                   | **글로벌 포트폴리오형.**                                                 |

## 반례

| 반례        | 이유                                                                               |
| --------- | -------------------------------------------------------------------------------- |
| 단일 제품 유행  | TikTok/viral 수요는 강하지만 반복소비와 채널 확장이 없으면 Stage 1~2.                                |
| 원가 상승 음식료 | 매출 증가에도 OPM/FCF가 안 따라오면 탈락.                                                      |
| 리콜/규제 이슈  | Samyang은 덴마크에서 일부 매운 라면 recall 이슈가 있었고, 이런 제품·규제 리스크는 4B/4C 감시용으로 필요해. ([타임][6]) |

## Stage 기준

```text
Stage 1:
- 수출 급증
- 해외 채널 뉴스
- 실적 서프라이즈

Stage 2:
- FY1/FY2 EPS 상향
- 수출비중 상승
- OPM expansion
- 목표가 상향

Stage 3:
- 반복소비
- 해외 채널 다변화
- ASP 유지
- CAPA 확장과 판매량 동시 증가
- 시장이 아직 내수 음식료 프레임으로 평가

4B:
- margin peak
- 모두가 글로벌 브랜드로 인정
- 재고/channel stuffing 우려

4C:
- 수출 성장 둔화
- 해외 재고 문제
- ASP/OPM 하락
- 규제/리콜
```

## 점수 보정

```text
contract_quality는 Green 필수 조건에서 제외.
대신 structural_visibility_quality =
수출비중 + 해외채널 + 반복소비 + ASP/OPM + FY1/FY2 상향.
```

---

# 5. K_BEAUTY_EXPORT_DISTRIBUTION

화장품, ODM, 브랜드, 플랫폼 유통

## 성공 케이스 보강

| 구분    | 케이스              | Stage 구조                                                                                                        | 주가 패턴                             |
| ----- | ---------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| 성공 후보 | 실리콘투             | K뷰티 글로벌 유통 플랫폼. Reuters는 한국이 2024년 미국 화장품 수출에서 프랑스를 앞섰고, Silicon2 CEO가 장기 성공에는 미국 오프라인 매출 확대가 중요하다고 언급했다고 보도했어. | **중국 의존 프레임 탈피형.** ([Reuters][7]) |
| 성공 후보 | APR / Medicube   | Vogue는 Medicube가 TikTok과 Ulta 등 omnichannel 유통을 통해 글로벌 breakout을 보였고, APR의 해외 매출 비중이 크게 증가했다고 설명했어.             | **브랜드+디바이스+채널 복합형.** ([Vogue][8]) |
| 성공 후보 | 코스맥스 / 한국콜마      | K뷰티 ODM. 브랜드 다변화의 shovel seller.                                                                                | **ODM 레버리지형.**                    |
| 성공 후보 | 브이티 / 파마리서치 / 휴젤 | 브랜드, 의료미용, 수출.                                                                                                  | **K뷰티+헬스케어 교차형.**                 |

## 반례

```text
1. 중국 의존 화장품:
   중국 채널 둔화 시 구조적 visibility 낮음.

2. Viral 인디브랜드:
   반복 주문/오프라인 채널 없으면 Stage 1~2.

3. Channel stuffing:
   매출채권/재고 악화면 4C.

4. Tariff/regulatory:
   AP는 2025년 미국의 한국 제품 관세가 K뷰티 boom을 위협할 수 있다고 보도했어. :contentReference[oaicite:11]{index=11}
```

## Stage 기준

```text
Stage 1:
- 미국/일본 수출 증가
- K뷰티 viral
- 화장품 수출 데이터

Stage 2:
- FY1/FY2 OP/EPS 상향
- OPM/ROE 개선
- 채널 확대
- 브랜드/고객 다변화

Stage 3:
- 반복 주문
- 오프라인/대형 리테일 진입
- 재고/채권 문제 없음
- 중국 의존도 하락
- 시장이 아직 중국 화장품주 프레임으로 평가

4B:
- K뷰티 overcrowding
- 신생 브랜드 난립
- 목표가 과열

4C:
- sell-through 둔화
- 재고 증가
- 매출채권 악화
- tariff/regulation impact
```

---

# 6. MEMORY_HBM_CAPACITY

메모리, HBM, AI 인프라 병목

## 성공 케이스 보강

| 구분          | 케이스              | Stage 구조                                                                                                               | 주가 패턴                                      |
| ----------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| 성공          | SK하이닉스           | HBM/AI 서버 수요, 공급확보 경쟁, 장기계약/선수금. Reuters는 빅테크가 SK하이닉스 공급 확보를 위해 생산라인·EUV 장비 자금지원 제안을 했고, 장기계약·가격밴드·선수금 구조가 논의된다고 보도했어. | **메모리 시클리컬 → AI 병목 리레이팅형.** ([Reuters][9]) |
| 성공/4B-watch | SK하이닉스 2025~2026 | Reuters는 SK하이닉스 주가가 2025년 274%, 2026년 200% 이상 상승했고 시총이 1조 달러에 접근했다고 보도했어. 구조적 성공이면서 4B-watch의 표본이야.                    | **구조적 성공 + 4B-watch 동시.** ([Reuters][9])   |
| 성공 후보       | 삼성전자 메모리         | 메모리 반등, HBM 격차 회복 여부, 과거 PBR 프레임 탈피 가능성. 삼성은 2024년에 AI칩 경쟁 우려 속 10조원 자사주 매입을 발표했어.                                     | **안정형 메모리 리레이팅 후보.** ([Barron's][10])      |
| 글로벌 비교      | Nvidia           | AI 데이터센터 수요가 GPU에서 메모리/서버/전력으로 파급되는 비교 기준.                                                                             | **병목 이동 관찰용.**                             |

## 반례

```text
1. 단순 DRAM 가격 반등:
   장기계약/선수금/중장기 EPS 상향 없으면 cyclical Yellow.

2. 공급과잉 전환:
   CAPEX 증설이 수요를 앞지르면 4C.

3. AI capex 둔화:
   고객사 데이터센터 투자가 꺾이면 thesis break.
```

## Stage 기준

```text
Stage 1:
- 메모리 가격 상승
- HBM 수요
- earnings turnaround

Stage 2:
- FY1/FY2/FY3 OP/EPS 상향
- 고객사 공급 확보 경쟁
- 공급규율
- 가격 상승

Stage 3:
- 장기계약 / 선수금 / price band
- CAPA constraint
- multiple-year consensus revision
- PBR에서 PER 평가 전환
- 과거 시클리컬 프레임 제거

4B:
- 모두가 PER 리레이팅 인정
- target multiple 포화
- capex 증설 뉴스
- 고객사 가격 저항
- 주가 급등 후 crowding

4C:
- HBM/DRAM/NAND 가격 하락
- 공급과잉
- 고객사 AI capex 둔화
- consensus revision down
```

---

# 7. SEMI_EQUIPMENT_CAPEX

반도체 장비, 패키징, 테스트, PCB

## 성공 후보 확장

```text
한미반도체:
HBM TC bonder / advanced packaging 병목.

이수페타시스:
AI 서버/네트워크 PCB, 데이터센터 capex leverage.

ISC / 리노공업:
테스트 소켓, 반복 수요, 고마진.

하나마이크론 / 두산테스나:
패키징·테스트 capex leverage.
```

## 반례 확장

```text
단일 고객 장비주:
고객사 capex 지연 시 EPS 급락.

국산화 테마 장비주:
실제 수주/매출화 없이 테마만 있으면 Green 금지.

장비 lead time 정상화:
수주잔고가 꺾이기 전 4B-watch 필요.
```

## Stage 기준

```text
Stage 1:
- 고객사 capex 뉴스
- HBM/AI keyword
- 장비 수주

Stage 2:
- backlog 증가
- 고객사 다변화
- revenue conversion
- OP/EPS 상향

Stage 3:
- 병목 장비 지위
- 고객사 CAPEX multi-year
- 반복 소모품/서비스
- 높은 OPM

4B:
- capex peak
- 주문 둔화
- lead time 정상화

4C:
- order cancellation
- customer capex cut
- inventory build
```

## 점수 보정

```text
EPS/FCF: 22
Visibility: 20
Bottleneck/Pricing: 18
Mispricing: 14
Valuation: 12
Risk penalty: 단일고객/CAPEX cycle
```

---

# 8. BATTERY_MATERIALS_CAPEX_OVERHEAT

2차전지 소재, 양극재, 음극재, 전해액

## 성공/반례 보강

| 구분    | 케이스                | Stage 구조                                  |
| ----- | ------------------ | ----------------------------------------- |
| 성공 후보 | 초기 양극재 장기계약 구간     | 수요·계약·마진이 동시에 있을 때만 후보.                   |
| 반례    | 에코프로비엠 / 에코프로 2023 | valuation/crowding이 EPS revision보다 앞선 과열. |
| 반례    | 소재 CAPA 과잉         | EV 수요 둔화 + 가동률 하락.                        |
| 반례    | 광물가격 하락            | 판가/마진 훼손.                                 |

## Stage 기준

```text
Stage 1:
- 장기계약
- CAPA 증설
- EV 수요 기대

Stage 2:
- 가격/마진 동반 상승
- contract quality
- FCF 훼손 없는 CAPEX

Stage 3:
- 매우 제한적
- 장기계약 + 가격전가 + 수요지속 + valuation 여지 필요

4B:
- price runup
- crowding
- PER/PBR 과열
- revision slowdown

4C:
- EV 수요 둔화
- 광물가격 하락
- CAPA 과잉
- margin compression
```

## 핵심 보정

```text
Battery 소재는 Green보다 Red/4B/4C 방어가 더 중요.
price_stage_score와 crowding penalty를 강하게 둬야 함.
```

---

# 9. SHIPPING_FREIGHT_CYCLE

해운, 운임, 물류

## 주가/사이클 반례 강화

| 구분     | 케이스              | 이유                                                                                    |
| ------ | ---------------- | ------------------------------------------------------------------------------------- |
| 사이클 성공 | HMM 2020~2021    | 운임 급등, 컨테이너 부족으로 EPS 폭발. 하지만 구조적 Green보다는 cyclical success.                           |
| 글로벌 비교 | Maersk 2021~2022 | AP는 Maersk가 2022년에 회사 역사상 가장 수익성 높은 해를 기록했지만, 이후 컨테이너 물동량과 운임 하락으로 이익 감소를 경고했다고 보도했어. |
| 반례/4C  | Maersk 2024      | Reuters는 2024년 컨테이너 시장이 과잉공급이고 운임이 지속 불가능한 수준으로 떨어졌다고 보도.                             |
| 반례/4C  | Maersk 2023 감원   | AP는 Maersk가 운임 하락과 어려운 컨테이너 시장으로 1만명 감원을 발표했다고 보도.                                    |

해운은 **주가와 EPS가 폭발할 수 있지만 Stage 3-Green을 매우 제한해야 하는 archetype**이야. 운임이 peak-out하면 EPS/FCF가 빠르게 무너질 수 있어. ([AP News][11])

## Stage 기준

```text
Stage 1:
- spot freight spike
- 컨테이너 shortage

Stage 2:
- contract freight 반영
- OP/EPS 폭발
- 선복 부족

Stage 3:
- 구조적 Green 매우 제한
- multi-year contract freight와 선복 공급 제약 필요

4B:
- 운임 peak
- 신규선박 공급
- spot/future divergence

4C:
- 운임 급락
- overcapacity
- demand slowdown
```

## 점수 보정

```text
EPS/FCF: 높게 인정 가능
Visibility: 낮게 시작
Cyclical risk: 매우 높게
Stage 3-Green: 원칙적으로 제한
Stage 3-Red/Yellow: 가능
```

---

# 10. AUTO_MOBILITY_COMPONENTS

자동차, 부품, 전장

## 성공 케이스 보강

| 구분    | 케이스          | Stage 구조                                                                                   |
| ----- | ------------ | ------------------------------------------------------------------------------------------ |
| 성공 후보 | 현대차          | Reuters는 현대차가 2030년 판매 30% 증가 목표, hybrid 라인업 확대, 2025~2027년 4조원 자사주 매입, 배당 확대를 발표했다고 보도했어. |
| 성공 후보 | 기아           | 고마진 mix, 미국 판매, 주주환원.                                                                      |
| 성공 후보 | 현대모비스 / HL만도 | 전장/ADAS, 고객 다변화.                                                                           |
| 반례    | 원가전가 실패 부품주  | 매출 증가에도 OPM 훼손.                                                                            |
| 반례    | EV 수요 둔화 부품주 | CAPA 확장 후 수요 미달.                                                                           |

현대차 케이스는 자동차 archetype이 단순 제조 사이클이 아니라 **믹스 개선 + 하이브리드 대응 + 주주환원 + valuation discount 해소**로도 작동할 수 있음을 보여줘. ([Reuters][12])

## Stage 기준

```text
Stage 1:
- 판매/환율/믹스 개선
- 주주환원 발표

Stage 2:
- OP/EPS 상향
- high-margin mix
- shareholder return

Stage 3:
- global share gain
- valuation discount 해소
- ROE/FCF 지속성

4B:
- peak margin
- tariff/policy risk
- valuation rerating 완료

4C:
- 관세/수요둔화
- 원가 상승
- 리콜/품질 비용
```

## 점수 보정

```text
EPS/FCF: 20
Visibility: 18
Bottleneck/Pricing: 10
Mispricing: 15
Valuation: 17
Capital allocation: 10까지 확대 가능
```

---

# 11. FINANCIAL_SPREAD_BALANCE_SHEET

은행, 보험, 증권, 카드

## 성공/반례 보강

| 구분    | 케이스                | Stage 구조                    |
| ----- | ------------------ | --------------------------- |
| 성공 후보 | KB금융 / 신한지주 / 하나금융 | ROE, 저PBR, 자본비율, 배당/자사주.    |
| 성공 후보 | 메리츠금융 / 삼성화재       | 자본효율, 환원정책, PBR-ROE 리레이팅.   |
| 반례    | 단순 저PBR 금융주        | ROE 개선·환원정책 없으면 value trap. |
| 반례    | PF/충당금 리스크 금융      | credit cost 상승이면 4C.        |

한국 value-up과 상법 개정/거버넌스 개선은 금융주 리레이팅 배경이 될 수 있지만, 정책만으로 Green을 주면 안 돼. Reuters는 한국의 법 개정이 Korea discount 해소와 소액주주 보호를 겨냥한다고 보도했어. ([Reuters][12])

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
- 환원정책 지속성

Stage 3:
- PBR-ROE 프레임 변화
- recurring ROE
- shareholder return credible

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
Capital allocation: 10
```

---

# 12. MEDICAL_DEVICE_HEALTHCARE_EXPORT

의료기기, 미용기기, 소모품 반복매출

## 성공/반례 보강

| 구분    | 케이스             | Stage 구조                                                    |
| ----- | --------------- | ----------------------------------------------------------- |
| 성공 후보 | 클래시스            | Classys는 비침습 피부미용 의료기기 회사이고, 2025년 기준 60개국 이상 수출한다고 정리돼 있어. |
| 성공 후보 | 파마리서치 / 휴젤 / 원텍 | 수출, 인허가, 소모품/시술 반복.                                         |
| 반례    | 단일 장비 판매        | 반복 소모품/서비스 없으면 visibility 낮음.                               |
| 반례    | 허가 지연           | 매출화 지연이면 4C.                                                |

([위키백과][13])

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

4C:
- 허가 지연
- 규제
- 경쟁 심화
```

---

# 13. BIOTECH_REGULATORY

바이오, 제약, 임상, 허가

## 보강 포인트

바이오는 **일반 E2R와 다르게 Green을 매우 보수적으로 줘야 해.**

```text
임상/허가 뉴스
≠ EPS/FCF 체급 변화

기술이전
≠ 반복 FCF

신약 기대
≠ 매출화
```

## 성공 후보

```text
알테오젠:
기술이전/SC 제형/로열티 가능성. 단, 실제 매출화와 로열티 visibility 필요.

유한양행:
신약 허가/로열티/매출화 가능성.

삼성바이오로직스:
CMO 수주/가동률/장기계약형에 가까워 biotech보다 contract backlog + healthcare export 혼합으로 볼 수 있음.
```

## 반례

```text
임상 뉴스만 있는 바이오
허가 지연
CB/유증 반복
기술이전 headline만 있고 수익화 불명확
```

## Stage 기준

```text
Stage 1:
- 임상/허가/기술이전 뉴스

Stage 2:
- milestone/payment
- 매출화 가능성
- cash runway

Stage 3:
- 실제 매출/로열티
- EPS/FCF 전환
- dilution risk 낮음

4C:
- 임상 실패
- 허가 지연
- 유증/CB
```

## 점수 보정

```text
EPS/FCF: 매출화 전에는 낮게
Visibility: 임상 milestone만으로 부족
RedTeam: dilution/임상 실패 강하게
```

---

# 14. THEME_VALUATION_OVERHEAT

테마 과열, 회계/신뢰, price-only rally

## 반례 보강

| 구분 | 케이스                | 이유                                                                                                                   |
| -- | ------------------ | -------------------------------------------------------------------------------------------------------------------- |
| 반례 | 에코프로비엠 / 에코프로 2023 | 2차전지 과열, crowding, valuation heat.                                                                                   |
| 반례 | SMCI 2024          | AI 서버 수요는 있었지만 회계/감사 신뢰 이슈. Reuters는 EY 사임 이후 SMCI 주가가 30% 이상 급락했고, 내부통제/회계 우려와 연차보고서 지연이 있었다고 보도했어. ([Reuters][14]) |
| 반례 | SMCI AP            | AP도 EY 사임 후 SMCI 주가가 33% 급락했다고 보도했어. ([AP News][15])                                                                 |
| 반례 | 로봇/AI 무실적 테마주      | EPS/FCF 없이 price-only rally.                                                                                         |

## Stage 기준

```text
Stage 1:
- 주가 급등
- 테마 뉴스

Stage 2:
- 실제 EPS/FCF evidence 있을 때만

Stage 3:
- Green 극히 제한

4B:
- valuation saturation
- crowded reports
- price blowoff

4C:
- accounting issue
- guidance miss
- revision down
```

## 주가 패턴

```text
SMCI형:
Stage 1/2처럼 보이는 강한 성장
→ price-only 4B-watch
→ auditor/accounting issue
→ hard 4C

이건 4B/4C detector의 필수 반례.
```

---

# 15. ONE_OFF_EVENT_DEMAND

팬데믹, 일회성 수요, temporary shortage

## 반례 보강

| 구분 | 케이스               | 이유                                                                                                                                     |
| -- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| 반례 | 씨젠 2020           | COVID 진단키트 수요. Seegene은 2020년 COVID test 제조·수출로 3Q profit growth가 1,000% 이상이었다고 정리돼 있지만, 이건 반복 구조가 아니라 팬데믹 one-off로 봐야 해. ([위키백과][16]) |
| 반례 | Abbott COVID test | Abbott는 2021년 COVID test 수요 감소로 profit guidance를 낮췄고, 이런 구조는 one-off 정상화 반례야.                                                          |
| 반례 | Zoom 2020         | 비대면 수요 폭증. 일시적으로는 구조처럼 보였지만 reopening 이후 정상화.                                                                                          |

## Stage 기준

```text
Stage 1:
- 실적 폭발
- event demand spike

Stage 2:
- 가능하나 Red flag 동반

Stage 3:
- Green 금지에 가깝다
- Stage 3-Red/Yellow 가능

4B:
- 모두가 구조 성장주로 착각
- valuation overheat

4C:
- 수요 정상화
- guidance down
```

## 점수 보정

```text
EPS/FCF: 폭발해도 인정
Visibility: 매우 낮게
one_off_shortage_risk: 매우 높게
Green: 차단
```

---

# 16. 이번 라운드에서 새로 더 명확해진 점수 원칙

## 16-1. Green은 구조형 archetype에서만 자주 허용

Green 가능성이 높은 쪽:

```text
Contract / Backlog
Defense
Shipbuilding
Export Consumer
K-Beauty
Memory/HBM
Semi Equipment
Medical Device
Financial
Turnaround
```

Green을 매우 제한해야 하는 쪽:

```text
Shipping
Commodity
Battery Materials
Biotech pre-revenue
One-off Event
Theme Overheat
Robotics theme-only
Game hit-driven
Construction credit-risk
```

## 16-2. Stage 3-Watch가 필요함

지금 모델이 Stage 2와 Stage 3-Green 사이가 너무 벌어져 있어.

그래서 앞으로 리포트에는:

```text
deterministic_stage = Stage 2
promotion_band = Stage 3-Watch
```

가 필요해.

예:

```text
HD현대일렉트릭:
Stage 2이지만 EPS/FCF 20, revision 100, backlog 85
→ Stage 3-Watch 가능

일진전기:
Stage 2, 계약/수주/리포트 있음
→ Stage 3-Watch 가능

효성중공업:
Stage 1이지만 62점으로 Stage 2 근접
→ Stage 2-High 가능
```

## 16-3. 4B/4C는 archetype별로 다르게 봐야 함

```text
전력기기:
수주잔고 둔화, ASP 하락, CAPA 완화

방산:
납기 지연, 원가 상승, 계약 취소

조선:
선가 peak, 저가수주, 후판가, 계약 취소

음식료:
수출 둔화, 재고, ASP/OPM 하락, 리콜

K뷰티:
sell-through 둔화, 재고/채권, tariff, 중국 의존

메모리:
가격 하락, 고객 capex 둔화, 공급과잉

해운:
운임 하락, 신규선박 공급, overcapacity

SMCI/테마:
회계/감사/신뢰 이슈
```

---

# 17. 다음 라운드에 더 채워야 할 빈 곳

아직 덜 채워진 archetype은 이거야.

```text
1. Platform / Software / Internet
2. Game / Content / IP
3. Retail / Domestic Consumer
4. Construction / Real Estate / Credit
5. Utilities / Regulated Tariff
6. Holding / Governance / Restructuring
7. Robotics / Factory Automation
8. Commodity Spread 세부 사례
9. Auto 부품 세부 사례
10. Biotech 매출화 성공/실패 세부 사례
```

이쪽은 아직 사례를 더 찾아야 해. 특히 price path와 4B/4C 사례가 필요해.

---

# 18. 지금까지 case library에 넣을 수 있는 2차 보강 후보

에이전트에 넣을 때는 아래처럼 “추가 후보”로 들어가면 돼.

```text
CONTRACT_BACKLOG_INDUSTRIAL:
+ LS ELECTRIC
+ 제룡전기
+ poor-quality cable/contract counterexample

DEFENSE_GOVERNMENT_BACKLOG:
+ 현대로템
+ LIG넥스원
+ 한국항공우주
+ 납기/원가 리스크 방산 반례

SHIPBUILDING_OFFSHORE_BACKLOG:
+ 삼성중공업
+ HD현대중공업
+ 한화오션
+ 러시아/Zvezda 계약 취소 반례
+ 저가수주 잔존 반례

EXPORT_RECURRING_CONSUMER:
+ 농심
+ 오리온
+ 단일 제품 유행 반례
+ 원가 상승/리콜 반례

K_BEAUTY_EXPORT_DISTRIBUTION:
+ APR
+ 코스맥스
+ 한국콜마
+ 브이티
+ 중국 의존 반례
+ channel stuffing 반례

MEMORY_HBM_CAPACITY:
+ SK하이닉스 2025~2026 4B-watch case
+ 삼성전자 HBM 회복 case
+ Micron global confirmation
+ 단순 DRAM 반등 반례

SEMI_EQUIPMENT_CAPEX:
+ 한미반도체
+ 이수페타시스
+ ISC
+ customer capex cut 반례

SHIPPING_FREIGHT_CYCLE:
+ HMM 2020~2021
+ Maersk 2021~2022
+ Maersk 2024 overcapacity
+ HMM post-peak

THEME_VALUATION_OVERHEAT:
+ SMCI 2024
+ 에코프로비엠 2023
+ 로봇/AI 무실적 테마주
```

---

# 19. 결론

응. **한 라운드 더 하니까 방향이 더 선명해졌어.**

지금 가장 중요한 결론은 이거야.

```text
1. 전력기기/방산/조선은 계약·수주잔고·CAPA·리드타임 중심.
2. 음식료/K뷰티/의료기기는 수출·채널·반복수요·OPM 중심.
3. 메모리/반도체장비는 HBM·가격·공급규율·고객사 CAPEX 중심.
4. 해운/commodity/2차전지는 EPS 폭발이 있어도 cycle/overheat penalty가 강해야 함.
5. 바이오/테마/로봇은 EPS/FCF 매출화 전 Green 금지.
6. 금융/지주사는 EPS 폭발보다 ROE/PBR/주주환원/거버넌스가 핵심.
7. Stage 3-Green은 희귀하게 유지하고, Stage 3-Watch/Stage 2-High를 리포트에 추가해야 함.
```

아직 다음 라운드에서 더 채울 건 있어. 특히 **플랫폼/게임/리테일/건설/유틸리티/지주사/로봇/바이오 세부 사례**는 더 봐야 해.

지금은 에이전트에 바로 점수 구현을 시키기보다, 이 2차 matrix를 `cases.jsonl` 확장 후보로 넣고, 다음 라운드에서 부족한 archetype을 더 채운 뒤 적용하는 게 맞다.

[1]: https://www.reuters.com/business/aerospace-defense/south-koreas-hanwha-aerospace-wins-1-bln-order-romania-k9-howitzers-2024-07-09/?utm_source=chatgpt.com "South Korea's Hanwha Aerospace wins $1 bln order from Romania for self-propelled howitzers"
[2]: https://www.reuters.com/markets/emerging/poland-signs-contract-buy-more-south-korean-battle-tanks-2025-08-01/?utm_source=chatgpt.com "Poland signs contract to buy more South Korean battle tanks"
[3]: https://www.wsj.com/articles/south-korean-shipbuilders-rally-on-brisk-contract-wins-d44ecb8a?utm_source=chatgpt.com "South Korean Shipbuilders Rally on Brisk Contract Wins"
[4]: https://apnews.com/article/cb72348bb00cb95801c2d6b5a47702fa?utm_source=chatgpt.com "China sanctions 5 US units of South Korean shipbuilder Hanwha Ocean over probe by Washington"
[5]: https://www.marketwatch.com/story/samyang-foods-set-to-post-strong-2q-earnings-market-talk-d654e045?utm_source=chatgpt.com "Samyang Foods Set to Post Strong 2Q Earnings -- Market Talk"
[6]: https://time.com/6988005/denmark-recalls-samyang-spicy-ramen-noodles/?utm_source=chatgpt.com "Denmark Recalls Popular Korean Instant Noodles Because They Are Too Spicy"
[7]: https://www.reuters.com/world/asia-pacific/korean-beauty-startups-bet-booming-us-demand-outlasts-tariff-pain-2025-06-05/?utm_source=chatgpt.com "Korean beauty startups bet booming US demand outlasts tariff pain"
[8]: https://www.vogue.com/article/how-k-beauty-brand-medicube-pulled-off-its-global-breakout?utm_source=chatgpt.com "How K-Beauty Brand Medicube Pulled Off Its Global Breakout"
[9]: https://www.reuters.com/world/asia-pacific/ai-boom-puts-sk-hynix-cusp-1-trillion-market-value-2026-05-14/?utm_source=chatgpt.com "AI boom puts SK Hynix on cusp of $1 trillion market value"
[10]: https://www.barrons.com/articles/hedge-funds-south-korea-stocks-samsung-sk-hynix-bb2aa94f?utm_source=chatgpt.com "Why Hedge Funds Still See Value in Red-Hot South Korean Stocks"
[11]: https://apnews.com/article/9e8161cf189d3da13c112d529e2f4c7d?utm_source=chatgpt.com "Shipper Maersk reports most profitable year, warns of drop"
[12]: https://www.reuters.com/business/autos-transportation/hyundai-motor-targets-30-rise-sales-by-2030-it-expands-hybrid-lineup-2024-08-28/?utm_source=chatgpt.com "Hyundai targets 30% rise in sales by 2030, as it doubles hybrid lineups"
[13]: https://en.wikipedia.org/wiki/Classys?utm_source=chatgpt.com "Classys"
[14]: https://www.reuters.com/technology/super-micro-computer-says-ernst-young-resigns-its-accountant-shares-tank-2024-10-30/?utm_source=chatgpt.com "Super Micro Computer says Ernst & Young resigns as auditor, shares tank"
[15]: https://apnews.com/article/d1cc4377628b3024e659dcfec9318dcd?utm_source=chatgpt.com "Super Micro Computer's shares plunge 33% after server maker's accounting firm quits"
[16]: https://en.wikipedia.org/wiki/Seegene?utm_source=chatgpt.com "Seegene"
