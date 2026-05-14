응. **이건 반복해서 내가 계속 채워가는 방식이 맞아.**
지금 바로 레포를 또 고치기보다, 먼저 내가 **섹터별 E2R case matrix를 계속 확장**하고, 그다음 어느 정도 case coverage가 찼을 때 에이전트에 한 번에 넣어서 백테스트하는 방식이 훨씬 낫다.

현재 레포 28A는 뼈대는 잘 만들었지만, 아직 `fixture_only: True`, mapped symbols 13개, archetypes used 8개뿐이야.
그리고 case library도 25개 archetype 중에서 “성공 2개 + 반례 2개”를 충족한 게 0개라서, 전부 `insufficient_case_coverage` 상태야.
즉, 지금은 scoring을 바꾸는 단계가 아니라 **내가 계속 성공/반례 케이스를 채우는 단계**가 맞아. 레포의 추천 점수비중도 전부 “do not implement yet”으로 되어 있어서 이 판단과 일치해.

---

# 0. 앞으로 반복 구조

내가 이 작업을 이렇게 반복할게.

```text
Round 1:
큰 archetype 정의
→ 성공/반례 1차 후보

Round 2:
각 archetype별 성공/실패 사례 확장
→ Stage 1/2/3/4B/4C 기준 정교화

Round 3:
가격 경로 / MFE / MAE / drawdown / peak timing 추가
→ 4B/4C 기준 보정

Round 4:
점수비중 초안 확정
→ 에이전트에 반영
→ as-of replay 재실행

Round 5:
틀린 케이스 해부
→ 다시 case matrix 보강
```

이게 맞다.
지금은 **Round 2 확장판**이라고 보면 돼.

---

# 1. 전체 구조를 다시 정리

서생원식 핵심은 단순 섹터가 아니라:

```text
산업 구조 변화
→ EPS/FCF 체급 변화
→ 시장이 아직 과거 프레임으로 오해
→ 밸류에이션 리레이팅
→ 논리 훼손 전까지 보유
```

이 순서야.

그래서 case matrix도 업종명을 외우는 게 아니라, 아래 질문에 답해야 해.

```text
이 섹터에서 EPS/FCF 체급 변화를 “지속”시키는 증거는 무엇인가?
무엇이 반대로 one-off / cycle / overheat / fake rerating인가?
Stage 1 레이더 신호는 무엇인가?
Stage 2 후보 편입 신호는 무엇인가?
Stage 3 고확신 신호는 무엇인가?
Stage 4B 졸업/과열 신호는 무엇인가?
Stage 4C 논리 훼손 신호는 무엇인가?
```

---

# 2. Round 2 확장: 우선순위 Archetype

이번에는 모든 25개를 균등하게 채우기보다, **국장에서 초과수익/오판이 자주 나오는 archetype**부터 더 깊게 채웠다.

우선순위는 이거야.

```text
1순위:
전력기기 / 방산 / 조선 / 음식료수출 / K뷰티 / 메모리-HBM / 반도체장비 / 2차전지과열 / 해운 / 의료기기

2순위:
자동차 / 금융 / 지주사 / 턴어라운드 / 게임·콘텐츠 / 플랫폼 / 바이오

3순위:
건설 / 유틸리티 / 리테일 / 로봇 / 범용 commodity
```

---

# 3. Contract / Backlog Industrial

## 구조

```text
수요 폭증
→ 공급 부족
→ 장기공급계약 / 수주잔고 / CAPA 부족
→ 가격 전가 / 리드타임 장기화
→ EPS/FCF 상향
→ 시클리컬 할인 제거
```

## 성공 사례

| 구분   | 케이스         | 이유                                                        |
| ---- | ----------- | --------------------------------------------------------- |
| 성공   | HD현대일렉트릭    | 북미 전력망, 변압기 공급부족, 수주잔고, OPM 개선, EPS 상향. 현재 레포에서도 Stage 2. |
| 성공   | 일진전기        | 장기공급계약, 계약금액/매출, 초고압 전력기기, CAPA 증설. 현재 Stage 2.           |
| 성공후보 | 효성중공업       | 저마진 수주 정리, 마진 개선, 수주잔고. 현재 Stage 1이지만 62점대로 Stage 2 직전.   |
| 성공후보 | LS ELECTRIC | 전력기기·전력자동화·북미 전력망 관련성 확인 필요.                              |
| 성공후보 | 제룡전기        | 변압기 공급부족·북미 수출성 확인 필요.                                    |

## 반례

| 구분 | 케이스               | 이유                                     |
| -- | ----------------- | -------------------------------------- |
| 반례 | 대한전선-like         | 전선/전력 테마라도 희석·낮은 수익성·밸류 부담이면 Green 금지. |
| 반례 | 단기 공급계약 테마주       | 계약금액 작고 기간 짧고 마진 불명확하면 Stage 1~2 제한.   |
| 반례 | 공급계약은 크지만 원가전가 실패 | 매출은 늘어도 OPM/FCF 훼손이면 4C.               |

## Stage 기준

```text
Stage 1:
- 공급계약 공시
- 변압기/전선/전력망 키워드
- 거래대금 급증

Stage 2:
- 계약금액/매출 10~20% 이상
- 계약기간 2~3년 이상
- 수주잔고 증가
- OP/EPS 상향

Stage 3:
- 수주잔고/매출 100% 이상
- 리드타임 장기화
- CAPA 부족
- ASP/OPM 개선
- FY1/FY2 EPS 동시 상향
- 과거 저마진/시클리컬 프레임 제거

Stage 4B:
- 목표가 상향이 쏟아짐
- 신규수주 모멘텀 둔화
- 가격 급등 후 밸류 포화
- 모두가 변압기/전력기기 구조주로 인정

Stage 4C:
- 계약 취소/지연
- ASP 하락
- 수주잔고 감소
- CAPA 과잉
```

## 점수비중 초안

```text
EPS/FCF: 20
Structural Visibility: 24
Bottleneck/Pricing: 22
Mispricing: 12
Valuation: 12
Info confidence: 5
```

---

# 4. Defense / Government Backlog

## 구조

```text
지정학/국방비 증가
→ 정부 고객 장기계약
→ 수주잔고와 납품 스케줄
→ 매출/OP visibility
→ 방산 프레임 리레이팅
```

## 성공 사례

| 구분   | 케이스       | 이유                                                                                                             |
| ---- | --------- | -------------------------------------------------------------------------------------------------------------- |
| 성공   | 한화에어로스페이스 | 루마니아 K9 계약은 10억 달러 규모, 2029년까지 진행. Reuters는 방산 수주잔고가 2021년 말 5.1조원에서 2024년 3월 약 30조원으로 늘었다고 보도. ([Reuters][1]) |
| 성공후보 | 현대로템      | K2 전차, 폴란드·해외 수출, 장기 납품 스케줄 확인 필요.                                                                             |
| 성공후보 | LIG넥스원    | 천궁-II, 미사일/방공 수출, 중동·유럽 수요.                                                                                    |
| 성공후보 | 한국항공우주    | KF-21, FA-50, 정부·해외 발주.                                                                                        |

## 반례

```text
- 방산 테마 소형주: 실제 정부계약/수주잔고/납품 스케줄 없으면 Green 금지
- 납기 지연 방산: 수주잔고는 커도 원가율 훼손이면 4C
- 정치/수출허가 리스크: 계약이 있어도 발효/납품 지연 가능
```

## Stage 기준

```text
Stage 1:
- 방산 계약 뉴스
- 정부 고객
- 지정학 모멘텀

Stage 2:
- 다년 납품 스케줄
- 수주잔고/매출 상승
- OP/EPS 추정 상향

Stage 3:
- 정부 고객 + 다년계약 + OPM 개선
- 해외 수출 비중 확대
- FY2/FY3까지 상향
- 밸류가 아직 내수 방산/저성장 프레임

4B:
- 방산주 전체 과열
- 신규계약 기대가 가격에 과반영
- target multiple 포화

4C:
- 납기 지연
- 원가 상승
- 계약 취소
- 수출허가/정치 리스크
```

## 점수비중

```text
EPS/FCF: 20
Visibility: 24
Bottleneck/Pricing: 17
Mispricing: 14
Valuation: 14
Risk penalty: 납기/원가/정치
```

---

# 5. Shipbuilding / Offshore Backlog

## 구조

```text
선가 상승
→ 좋은 가격의 신규수주
→ 저가수주 소진
→ 인도 시점 고마진 선박 반영
→ EPS 턴어라운드
```

## 성공 사례

| 구분   | 케이스                | 이유                                                                                          |
| ---- | ------------------ | ------------------------------------------------------------------------------------------- |
| 성공후보 | 삼성중공업              | 한국 조선주가 계약 재개와 신조선가 상승으로 랠리했다는 보도. ([The Wall Street Journal][2])                           |
| 성공후보 | HD현대중공업 / HD한국조선해양 | LNG선, 특수선, 인도 슬롯, 선가 상승.                                                                    |
| 성공후보 | 한화오션               | LNG, 방산 조선, 미 해군 MRO 관련성. Hanwha Ocean은 2024년 미국 해군 MSRA를 체결한 한국 조선사 중 하나로 정리됨. ([위키백과][3]) |

## 반례

```text
- 저가수주 잔존 조선사: 수주잔고는 크지만 적자 호선이면 visibility 낮음
- 계약 취소/지정학 리스크: 대형 계약 취소는 4C
- 후판가/인건비 상승: 선가 상승보다 원가가 더 빠르면 EPS 훼손
```

## Stage 기준

```text
Stage 1:
- 대형 수주
- 신조선가 상승
- 조선주 거래대금 급증

Stage 2:
- 저가수주 소진
- 고마진 선박 인도 시작
- OP 흑자전환

Stage 3:
- 수주잔고 질 개선
- 선가 상승분 FY2/FY3 OP 반영
- 원가 안정
- 장기 인도 슬롯

4B:
- 신조선가 피크
- 수주 피크
- 밸류 포화

4C:
- 계약 취소
- 후판가/인건비 급등
- 발주 사이클 둔화
```

---

# 6. Export / Recurring Consumer

## 구조

```text
해외 수요 증가
→ 채널 확장
→ 반복소비
→ ASP/OPM 상승
→ EPS 체급 변화
→ 내수 저성장 소비재 프레임 제거
```

## 성공 사례

| 구분   | 케이스  | 이유                                                         |
| ---- | ---- | ---------------------------------------------------------- |
| 성공   | 삼양식품 | 불닭 수출, 해외 채널, ASP/OPM, EPS 상향. 레포에서도 structural benchmark. |
| 성공후보 | 농심   | 미국/해외 라면 매출, 반복소비 구조 확인 필요.                                |
| 성공후보 | 오리온  | 글로벌 제과, 중국·베트남·러시아 포트폴리오, OPM 확인 필요.                       |

## 반례

```text
- 단일 제품 유행: viral 수요가 반복소비/채널로 안 이어지면 Stage 1~2
- 원가 상승 음식료: 매출 증가에도 OPM/FCF 훼손
- 리콜/규제 이슈: 제품 리스크는 RedTeam
```

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

Stage 3:
- 반복소비
- 해외 채널 다변화
- ASP/판가 유지
- CAPA 확장 + 판매량 증가
- 시장이 아직 내수 음식료로 평가

4B:
- margin peak
- 모든 리포트가 글로벌 브랜드로 인정
- 재고/channel stuffing 우려

4C:
- 수출 둔화
- 해외 재고 문제
- ASP/OPM 하락
- 규제/리콜
```

## 점수비중

```text
EPS/FCF: 22
Visibility: 23
Bottleneck/Pricing: 12
Mispricing: 16
Valuation: 13
Contract quality: 필수 아님
```

---

# 7. K-Beauty / Export Distribution

## 구조

```text
K뷰티 글로벌 수요
→ 미국/일본/유럽 채널 확장
→ 브랜드 다변화 / 반복 주문
→ OPM/ROE 개선
→ 중국 의존 화장품 프레임 제거
```

## 성공 사례

| 구분   | 케이스                 | 이유                                                                                                                                          |
| ---- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 성공후보 | 실리콘투                | K뷰티 글로벌 유통 플랫폼, 해외 채널 확장. Reuters는 2024년 한국이 미국 화장품 수출에서 프랑스를 앞섰고, K뷰티 업체들이 Sephora·Target·Costco 등 미국 오프라인 채널 진입을 추진한다고 보도. ([Reuters][4]) |
| 성공후보 | APR                 | FT는 APR이 K뷰티 디바이스 성공으로 valuation이 급상승했고, 2025년 Q2 매출의 약 80%가 해외에서 나왔다고 보도. ([파이낸셜 타임스][5])                                                  |
| 성공후보 | 코스맥스 / 한국콜마         | ODM, 글로벌 고객사, 미국·일본 수출 확인 필요.                                                                                                               |
| 성공후보 | 브이티 / 파마리서치 / 휴젤 일부 | 브랜드·의료미용 교차 영역.                                                                                                                             |

## 반례

```text
- 중국 의존 화장품: 중국 채널 둔화·단일시장 의존
- viral 인디브랜드: 반복주문/오프라인 채널 없으면 Green 금지
- channel stuffing: 매출채권/재고 악화
- tariff/regulatory risk: 미국 관세·인증 리스크
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

## 점수비중

```text
EPS/FCF: 22
Visibility: 23
Bottleneck/Pricing: 12
Mispricing: 16
Valuation: 13
Risk penalty: 재고/채권/중국의존
```

---

# 8. Memory / HBM Capacity

## 구조

```text
AI 수요
→ HBM/DRAM/NAND 수요
→ CAPA 재배치/공급규율
→ 고객사 장기계약·선수금·가격밴드
→ EPS/FCF 다년 상향
→ 과거 메모리 시클리컬 할인 제거
```

## 성공 사례

| 구분     | 케이스             | 이유                                                                                                                |
| ------ | --------------- | ----------------------------------------------------------------------------------------------------------------- |
| 성공     | SK하이닉스          | Reuters는 빅테크가 SK하이닉스 공급 확보를 위해 신규 생산라인·EUV 장비 투자 제안을 했고, 장기계약·가격밴드·선수금 구조가 논의된다고 보도. ([Reuters][6])               |
| 성공     | SK하이닉스 EUV/CAPA | Reuters는 SK하이닉스가 11.95조원 규모 ASML EUV 장비를 2027년 말까지 도입하고, 이 장비가 HBM과 advanced DRAM 생산에 쓰일 것이라고 보도. ([Reuters][7])  |
| 성공후보   | 삼성전자 메모리        | 메모리 반등, HBM 격차 회복 여부, 자사주 등 주주환원. 단, HBM 경쟁력 확인 필요. Samsung은 2024년 AI칩 경쟁력 우려 속 10조원 자사주 매입을 발표했다. ([Reuters][8]) |
| 글로벌 비교 | Micron          | 글로벌 메모리 cycle confirmation용.                                                                                      |

## 반례

```text
- 단순 DRAM 가격 반등: 중장기 계약/선수금/컨센서스 상향 없으면 cyclical Yellow
- 공급과잉 전환: 고객사 capex 둔화, 가격 하락
- 과도한 4B 구간: SK하이닉스 시총/주가가 너무 빠르게 오른 구간은 4B-watch 필요
```

Reuters는 2026년 SK하이닉스가 AI 수요로 시총 1조 달러에 근접하고 주가가 2025년 274%, 2026년 200% 이상 상승했다고 보도했다. 이건 구조적 성공이면서 동시에 4B-watch의 좋은 사례야. ([Reuters][9])

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

## 점수비중

```text
EPS/FCF: 24
Visibility: 21
Bottleneck/Pricing: 19
Mispricing: 15
Valuation: 12
Risk penalty: cycle / capex reversal
```

---

# 9. Semi Equipment / Advanced Packaging

## 구조

```text
고객사 AI/HBM capex
→ 병목 장비/소재/패키징 수요
→ 수주잔고/매출화
→ OP leverage
```

## 성공후보

```text
한미반도체: HBM TC bonder, advanced packaging 병목
이수페타시스: AI 서버/네트워크 PCB
ISC / 리노공업: 테스트 소켓, 반복수요
하나마이크론 / 두산테스나: 패키징·테스트 capex leverage
```

## 반례

```text
- 단일 고객 장비주: 고객사 capex 지연 시 EPS 급락
- 국산화 테마주: 실제 수주/매출화 없으면 Green 금지
- 장비 lead time 정상화: 4B/4C
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

---

# 10. Battery Materials / Capex Overheat

## 구조

```text
EV 성장 기대
→ 소재 장기계약/CAPA 투자
→ 광물가격·EV수요·CAPA 과잉에 매우 취약
```

## 성공/반례

| 구분   | 케이스                | 이유                                           |
| ---- | ------------------ | -------------------------------------------- |
| 성공후보 | 초기 양극재 장기계약 구간     | 수요·계약·마진이 같이 있을 때만 후보.                       |
| 반례   | 에코프로비엠 / 에코프로 2023 | valuation/crowding이 EPS revision보다 앞선 과열 반례. |
| 반례   | 소재 CAPA 과잉         | EV 수요 둔화 + 가동률 하락.                           |
| 반례   | 광물가격 하락            | 판가/마진 훼손.                                    |

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
- 장기계약 + 가격전가 + 수요지속 + valuation 여지

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

## 점수비중

```text
EPS/FCF: 20
Visibility: 16
Bottleneck/Pricing: 14
Mispricing: 10
Valuation: 10
Risk penalty: 매우 큼
```

---

# 11. Commodity Spread

## 구조

```text
제품가격 - 원가 스프레드
→ OP leverage
→ 대부분은 구조적 E2R보다 사이클
```

## 성공후보

```text
정유 spread 회복주
화학 spread 회복주
철강 가격-원가 spread 회복
비철/제련마진 구조주
```

## 반례

```text
순수 가격 사이클
중국 공급과잉 화학
재고 build-up
수요 둔화
```

## Stage 기준

```text
Stage 1:
- 제품가격 상승
- spread 개선

Stage 2:
- OP/EPS 추정 상향
- 재고/수요 개선
- 비용구조 개선

Stage 3:
- 매우 제한적
- cost curve advantage
- capacity discipline
- long-term structural supply constraint

4B:
- spread peak
- inventory build
- 모두가 호황 인정

4C:
- spread reversal
- 중국/글로벌 증설
- 수요 둔화
```

---

# 12. Shipping / Freight Cycle

## 구조

```text
운임 급등
→ EPS 폭발
→ 공급 정상화/운임 하락 시 급락
```

## 성공/반례

| 구분     | 케이스              | 이유                                                                                    |
| ------ | ---------------- | ------------------------------------------------------------------------------------- |
| 사이클 성공 | HMM 2020~2021    | 운임 급등, 컨테이너 부족. 구조적 Green보다는 cyclical success.                                        |
| 글로벌 비교 | Maersk 2020~2021 | Maersk는 trade recovery와 freight rate로 실적이 급증한 구간이 있었음.                                |
| 반례     | Maersk 2024      | Maersk CEO는 컨테이너 운임이 unsustainable level로 하락했고 overcapacity가 문제라고 언급. ([Reuters][10]) |
| 반례     | HMM 고점 이후        | 운임 정상화와 EPS 급락.                                                                       |

## Stage 기준

```text
Stage 1:
- spot freight spike
- container shortage

Stage 2:
- contract freight 반영
- OP/EPS 폭발

Stage 3:
- 구조적 Green 매우 제한
- multi-year contract freight와 선복 공급 제약이 있어야 함

4B:
- 운임 peak
- 신규선박 공급
- spot/future divergence

4C:
- 운임 급락
- overcapacity
- demand slowdown
```

---

# 13. Auto / Mobility Components

## 구조

```text
믹스 개선 / 하이브리드 / 수출 / 주주환원
→ EPS/FCF 안정 성장
→ 저평가 프레임 해소
```

## 성공/반례

| 구분   | 케이스          | 이유                                                                                                        |
| ---- | ------------ | --------------------------------------------------------------------------------------------------------- |
| 성공후보 | 현대차          | Reuters는 현대차가 2030년 판매 30% 증가 목표, 하이브리드 라인업 확대, 2025~2027년 4조원 자사주 매입과 주주환원 확대를 발표했다고 보도. ([Reuters][11]) |
| 성공후보 | 기아           | 고마진 mix, 미국 판매, 주주환원.                                                                                     |
| 성공후보 | 현대모비스 / HL만도 | 전장/ADAS, 고객 다변화.                                                                                          |
| 반례   | 원가전가 실패 부품주  | 매출 증가에도 OPM 훼손.                                                                                           |
| 반례   | EV 수요 둔화 부품주 | CAPA 확장 후 수요 미달.                                                                                          |

## 점수비중

```text
EPS/FCF: 20
Visibility: 18
Bottleneck/Pricing: 10
Mispricing: 15
Valuation: 17
Capital allocation: 중요
```

---

# 14. Financial Spread / Balance Sheet

## 구조

```text
ROE + 저PBR + 자본정책
→ Korea discount 해소
→ PBR-ROE 프레임 리레이팅
```

## 성공/반례

| 구분   | 케이스                 | 이유                                 |
| ---- | ------------------- | ---------------------------------- |
| 성공후보 | KB금융                | 대형 금융지주, ROE/PBR/주주환원 value-up 후보. |
| 성공후보 | 신한지주 / 하나금융 / 메리츠금융 | 주주환원·자본효율·ROE.                     |
| 반례   | 단순 저PBR 금융주         | ROE와 주주환원 없으면 value trap.          |
| 반례   | PF/충당금 리스크 금융       | credit cost 상승이면 4C.               |

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

## 점수비중

```text
EPS/FCF: 15
Visibility: 20
Bottleneck/Pricing: 5
Mispricing: 15
Valuation: 25
Capital allocation: 10
```

---

# 15. Biotech / Regulatory

## 구조

```text
임상/허가/기술이전
→ 매출화/로열티 전환 여부가 핵심
```

## 성공후보

```text
알테오젠: 기술이전/SC 제형/로열티 가능성
유한양행: 신약 허가/로열티/매출화 가능성
셀트리온/삼성바이오: CMO/바이오시밀러 매출화 구조
```

## 반례

```text
임상 뉴스만 있는 바이오
기술이전 headline만 있고 수익화 불명확
허가 지연/임상 실패
CB/유증 반복
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

## 점수비중

```text
EPS/FCF: 5~10 before revenue
Visibility: 15
Mispricing: 10
Valuation: 5
RedTeam/Dilution 매우 중요
```

---

# 16. Medical Device / Healthcare Export

## 구조

```text
의료기기/미용기기 수출
→ 소모품/반복매출
→ OPM/ROE
```

## 성공/반례

| 구분   | 케이스             | 이유                                                           |
| ---- | --------------- | ------------------------------------------------------------ |
| 성공후보 | 클래시스            | 비침습 피부미용 의료기기 회사이고, 2025년 기준 60개국 이상 수출한다고 정리됨. ([위키백과][12]) |
| 성공후보 | 파마리서치 / 휴젤 / 원텍 | 수출, 인허가, 소모품/시술 반복.                                          |
| 반례   | 단일 장비 판매        | 반복 소모품/서비스 없으면 visibility 낮음.                                |
| 반례   | 규제·허가 지연        | 매출화 지연이면 4C.                                                 |

## 점수비중

```text
EPS/FCF: 20
Visibility: 22
Bottleneck/Pricing: 13
Mispricing: 14
Valuation: 12
```

---

# 17. One-off Event Demand

## 구조

```text
일회성 수요
→ EPS 폭발
→ 다음 해 정상화
```

## 반례

| 구분 | 케이스               | 이유                                                                         |
| -- | ----------------- | -------------------------------------------------------------------------- |
| 반례 | 씨젠 2020           | COVID 진단키트 수요. EPS 폭발은 있어도 반복 구조가 아님.                                      |
| 반례 | Abbott COVID test | Abbott는 COVID test 수요 감소로 2021년 profit guidance를 낮췄고 주가가 하락. ([Axios][13]) |
| 반례 | Zoom 2020         | 비대면 일회성 수요가 과대외삽된 사례.                                                      |
| 반례 | 기타 팬데믹 수혜주        | 다음 해 역성장 위험.                                                               |

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

---

# 18. Theme / Valuation Overheat

## 구조

```text
테마 / 주가 급등 / 밸류 과열
→ EPS/FCF가 따라오지 않으면 붕괴
```

## 반례

| 구분 | 케이스                          | 이유                                                                                                                                |
| -- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 반례 | 에코프로비엠 / 에코프로 2023           | 2차전지 과열, crowding, valuation heat.                                                                                                |
| 반례 | SMCI 2024                    | AI 서버 수요는 있었지만 회계/신뢰 이슈. Reuters는 SMCI가 내부통제 평가 필요로 연차보고서 제출을 지연했고, Hindenburg short report 이후 회계 관련 이슈가 있었다고 보도. ([Reuters][14]) |
| 반례 | AP: SMCI auditor resignation | AP는 EY가 투명성·내부통제·경영진 신뢰 문제로 SMCI 감사에서 사임했고 주가가 33% 급락했다고 보도. ([AP News][15])                                                      |
| 반례 | 로봇/AI 무실적 테마주                | price-only rally.                                                                                                                 |

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

---

# 19. 지금 가장 중요한 추가 결론

## 19-1. 전 섹터를 한 번에 완성하려 하지 말고, “채워진 archetype”부터 scoring 후보

현재 case coverage가 전부 부족하니까, 최종 scoring을 당장 적용하면 위험하다.
하지만 **우선순위 archetype부터 빠르게 채우면** 다음 라운드에 shadow scoring을 할 수 있어.

우선순위:

```text
1. Contract / Backlog
2. Defense
3. Export Consumer
4. K-Beauty
5. Memory/HBM
6. Semi Equipment
7. Shipping/Freight
8. One-off Event
9. Theme Overheat
10. Financial Spread
```

이 10개만 먼저 2+2 case를 채워도, 국장 주요 초과수익/오판 사례의 큰 부분을 커버할 수 있어.

---

## 19-2. Stage 3-Green은 희귀하게, Stage 3-Watch를 더 적극적으로

지금까지의 결과를 보면 Green을 쉽게 만들면 안 돼.
대신 에이전트 출력에 아래를 추가하는 게 맞아.

```text
Stage 2
Stage 2-High
Stage 3-Watch
Stage 3-Yellow
Stage 3-Green
```

즉 HD현대일렉트릭/일진전기처럼 강한 후보인데 Green gate 일부가 부족한 경우는:

```text
deterministic_stage = Stage 2
promotion_band = Stage 3-Watch
```

처럼 보여줘야 해.

이게 내가 수동으로 했던 느낌과 더 가깝다.

---

## 19-3. 4B/4C는 “가격”만 보면 안 되고 archetype별 논리 훼손을 봐야 함

```text
전력기기:
수주잔고 둔화, ASP 하락, CAPA 완화

음식료/K뷰티:
수출 둔화, 재고/채권 증가, 채널 stuffing

메모리:
가격 하락, 고객 capex 둔화, 공급과잉

방산:
납기 지연, 원가 상승, 계약 취소

해운:
운임 하락, 신규 선복 증가

금융:
충당금 증가, 자본비율 악화

바이오:
임상 실패, 허가 지연, 유증
```

이걸 4B/4C detector에 archetype별로 넣어야 한다.

---

# 20. 다음 반복에서 내가 더 채울 부분

다음 라운드에서는 아래를 더 깊게 채우는 게 좋다.

```text
A. 조선/조선기자재 세부 케이스
- HD현대중공업
- 삼성중공업
- 한화오션
- HD현대미포
- 기자재주 반례

B. K뷰티 세부 케이스
- 실리콘투
- APR
- 코스맥스
- 한국콜마
- 브이티
- channel stuffing 반례

C. 메모리/반도체 장비
- SK하이닉스
- 삼성전자
- 한미반도체
- 이수페타시스
- ISC
- capex peak 반례

D. 금융/value-up
- KB금융
- 신한지주
- 메리츠금융
- 단순 저PBR 반례

E. 의료기기
- 클래시스
- 파마리서치
- 휴젤
- 단일 장비/허가 지연 반례

F. 바이오
- 알테오젠
- 유한양행
- 임상 뉴스만 있는 반례
- 유증/CB 반복 반례
```

---

# 21. 결론

응. **이 작업은 내가 계속 반복해서 채워갈 수 있고, 그렇게 하는 게 맞다.**

지금 레포는 28A로 구조를 만들었고, 내가 할 일은:

```text
성공/반례 case matrix를 계속 확장
→ Stage 1/2/3/4B/4C 기준 정리
→ 점수비중 후보 작성
→ 에이전트에 넣을 JSONL/CSV 구조로 변환
→ 백테스트 결과와 비교
→ 다시 보정
```

이 순서야.

지금 2차 확장으로 보면, 다음에 바로 에이전트에 넣기보다는 **한 라운드 더 case matrix를 채워도 좋다.** 특히 K뷰티, 조선, 금융, 의료기기, 바이오, 반도체장비는 아직 덜 찼어.

[1]: https://www.reuters.com/business/aerospace-defense/south-koreas-hanwha-aerospace-wins-1-bln-order-romania-k9-howitzers-2024-07-09/?utm_source=chatgpt.com "South Korea's Hanwha Aerospace wins $1 bln order from Romania for self-propelled howitzers"
[2]: https://www.wsj.com/articles/south-korean-shipbuilders-rally-on-brisk-contract-wins-d44ecb8a?utm_source=chatgpt.com "South Korean Shipbuilders Rally on Brisk Contract Wins"
[3]: https://en.wikipedia.org/wiki/Hanwha_Ocean?utm_source=chatgpt.com "Hanwha Ocean"
[4]: https://www.reuters.com/world/asia-pacific/korean-beauty-startups-bet-booming-us-demand-outlasts-tariff-pain-2025-06-05/?utm_source=chatgpt.com "Korean beauty startups bet booming US demand outlasts tariff pain"
[5]: https://www.ft.com/content/6a0f7e2c-f3b9-4eb6-961c-d69af28f7183?utm_source=chatgpt.com "Kardashian endorsement of skincare gadget creates K-beauty champion"
[6]: https://www.reuters.com/world/asia-pacific/sk-hynix-flooded-with-unprecedented-offers-big-tech-firms-secure-chip-supplies-2026-05-07/?utm_source=chatgpt.com "SK Hynix flooded with unprecedented offers from big tech firms to secure chip supplies"
[7]: https://www.reuters.com/world/asia-pacific/sk-hynix-buy-euv-scanners-8-billion-asml-korea-2026-03-24/?utm_source=chatgpt.com "SK Hynix to buy $8 billion in ASML chipmaking tools in largest disclosed order"
[8]: https://www.reuters.com/technology/samsung-electronics-plans-72-bln-buyback-boost-shareholder-value-2024-11-15/?utm_source=chatgpt.com "Samsung Electronics plans $7.2 billion buyback after share price plunges"
[9]: https://www.reuters.com/world/asia-pacific/ai-boom-puts-sk-hynix-cusp-1-trillion-market-value-2026-05-14/?utm_source=chatgpt.com "AI boom puts SK Hynix on cusp of $1 trillion market value"
[10]: https://www.reuters.com/markets/europe/maersk-ceo-says-container-rates-have-fallen-unsustainable-levels-2024-03-14/?utm_source=chatgpt.com "Container rates drop to unsustainable levels, Maersk CEO says"
[11]: https://www.reuters.com/business/autos-transportation/hyundai-motor-targets-30-rise-sales-by-2030-it-expands-hybrid-lineup-2024-08-28/?utm_source=chatgpt.com "Hyundai targets 30% rise in sales by 2030, as it doubles hybrid lineups"
[12]: https://en.wikipedia.org/wiki/Classys?utm_source=chatgpt.com "Classys"
[13]: https://www.axios.com/2021/06/01/abbott-covid-tests-profit-guidance-slash-vaccines?utm_source=chatgpt.com "Abbott's stock falls after company forecasts fewer COVID tests"
[14]: https://www.reuters.com/technology/super-micro-computer-gets-extension-file-delayed-annual-report-2024-12-06/?utm_source=chatgpt.com "Super Micro Computer gets extension to file delayed annual report"
[15]: https://apnews.com/article/d1cc4377628b3024e659dcfec9318dcd?utm_source=chatgpt.com "Super Micro Computer's shares plunge 33% after server maker's accounting firm quits"
