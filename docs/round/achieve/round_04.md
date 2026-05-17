응. 이번 라운드는 **“점수비중이 주가 리레이팅 결과와 맞았는가”**를 기준으로 더 엄격하게 확장할게.

핵심은 이거야.

> **어떤 archetype에서 점수를 높게 줬는데, 실제로 Stage 3 이후 주가가 리레이팅되지 않았거나 4C로 바로 무너졌다면, 그 점수비중은 실패한 것이다.**
> 반대로 Stage 1→2→3에서 EPS/FCF와 주가가 같이 움직이고, 4B/4C 신호도 어느 정도 설명된다면, 그 archetype의 점수비중은 강화할 수 있다.

이제부터 case library는 단순 “좋아 보이는 사례”가 아니라, 아래 네 가지를 같이 봐야 해.

```text
1. 점수상 Stage 2/3로 올라갈 근거가 있었는가
2. 실제 주가가 Stage 3 이후 정방향으로 갔는가
3. 주가가 많이 오른 뒤 4B/과열 신호가 나왔는가
4. 논리 훼손/4C가 왔을 때 주가가 꺾였는가
```

즉 **score → stage → price path → 4B/4C**가 맞물려야 한다. 이게 서생원식 “EPS 체급 변화 + 시장 오해 + 리레이팅 + 논리 훼손 전까지 보유” 구조와 맞다.

---

# 1. 이번 라운드에서 추가해야 할 case-library 필드

에이전트에 넣기 전에 case record에 아래 필드를 추가해야 해.

```text
price_validation:
  stage3_price
  peak_price
  peak_return_from_stage3
  mfe_90d
  mfe_180d
  mfe_1y
  mae_90d
  mae_180d
  below_stage3_price_flag
  time_to_50pct
  time_to_100pct
  time_to_200pct

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

stage_failure_type:
  green_success
  yellow_success
  stage2_watch_success
  false_green
  false_yellow
  should_have_been_red
  missed_structural
```

이 필드가 있어야 “네이버를 높게 줬는데 주가가 안 갔다” 같은 실패를 잡을 수 있어.
즉, 단순히 “좋은 기업”이 아니라 **E2R 점수와 주가 경로가 정합적인가**를 검증해야 한다.

---

# 2. Platform / Software / Internet — 이번 라운드 핵심 보정

## 결론

플랫폼은 지금 당장 **성공사례로 쉽게 넣으면 안 된다.**
네이버·카카오 같은 플랫폼은 좋은 회사일 수 있지만, 서생원식 E2R로 보려면 다음이 필요하다.

```text
MAU / 트래픽 증가
→ ARPU 또는 take-rate 상승
→ 비용 효율화
→ OPM/EPS 상향
→ 시장이 아직 저성장 플랫폼 프레임으로 평가
→ 주가 리레이팅
```

이 경로가 주가로 검증되지 않으면 **성공사례가 아니라 후보 또는 반례**로 둬야 한다.

## 2차 matrix

| 구분   | 케이스         | 현재 판단                                                   | 주가-점수 정합성                                       |
| ---- | ----------- | ------------------------------------------------------- | ----------------------------------------------- |
| 성공후보 | NAVER       | 광고/커머스/AI 비용효율화가 실제 OP/EPS 상향으로 이어지는지 확인 필요             | 아직 “확정 성공” 아님. Stage 2-Watch 후보로만 둬야 함          |
| 성공후보 | 더존비즈온       | ERP/SaaS 반복매출, AI/클라우드 전환, OPM 레버리지 확인 필요               | 반복매출과 OP leverage가 있으면 플랫폼형 성공 가능               |
| 반례   | 카카오         | 규제, governance, 비용, 신사업 부진이 valuation rerating을 막을 수 있음 | MAU/브랜드만으로 점수 높이면 실패                            |
| 반례   | MAU만 높은 플랫폼 | 트래픽은 있지만 ARPU/OPM이 안 오르면 E2R 아님                         | score high → price no rerating이면 false positive |

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
- Stage 3 이후 주가가 실제로 rerating

4B:
- AI/플랫폼 narrative 과열
- multiple expansion 완료
- ARPU 성장 둔화

4C:
- 규제
- take-rate 하락
- 트래픽 감소
- AI 비용 과다
```

## 점수비중 보정

```text
EPS/FCF: 20
Structural Visibility: 22
Bottleneck/Pricing: 6~8
Market Mispricing: 16
Valuation: 14
Risk penalty: regulation / AI cost / governance
```

**중요:** 플랫폼은 Stage 3-Green을 잘 안 줘야 한다.
주가가 안 갔던 플랫폼은 “좋은 기업”이어도 E2R 성공사례가 아니다.

---

# 3. Game / Content / IP

## 결론

게임·콘텐츠는 **신작 기대**와 **실제 반복 monetization**을 강하게 분리해야 해.
점수는 신작 발표가 아니라, 실제 매출·OP·IP 반복성·글로벌 monetization을 봐야 한다.

## 2차 matrix

| 구분   | 케이스             | 판단                                                                                                                            | 주가-점수 정합성                   |
| ---- | --------------- | ----------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| 성공후보 | Krafton         | PUBG/BGMI 글로벌 IP, 인도 exposure. BGMI는 2022년 2.5억 다운로드를 넘겼고, 2022년 ban 이후 2023년 재출시된 이력이 있어 규제 리스크와 반복 IP를 같이 봐야 함. ([위키백과][1]) | IP 반복성 + 인도 규제 리스크 동시 반영 필요 |
| 성공후보 | Shift Up        | Nikke/Stellar Blade, 높은 OPM 가능성, 신작/IP 반복성 확인 필요                                                                              | 단일 신작 기대만이면 위험              |
| 성공후보 | HYBE / JYP / SM | 팬덤/IP/투어/글로벌 monetization                                                                                                     | 아티스트 리스크와 계약 리스크가 4C        |
| 반례   | 신작 기대만 있는 게임주   | 출시 후 매출이 안 나오면 4C                                                                                                             | score high 주면 실패            |
| 반례   | 단일 IP 의존        | IP 하나가 꺾이면 EPS/FCF 경로 깨짐                                                                                                      | Green 제한                    |

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

## 점수비중

```text
EPS/FCF: 20
Visibility: 18
Bottleneck/Pricing: 5~8
Mispricing: 14
Valuation: 12
Risk penalty: hit-driven discount
```

**주가 검증 원칙:**
신작 기대 전후로 주가가 올라도, 출시 후 EPS/OP가 안 따라오면 **Stage 3 성공이 아니라 Stage 4B/4C 반례**로 넣어야 한다.

---

# 4. Robotics / Factory Automation

## 결론

로봇은 지금 시장에서 테마성이 강해서 **Green 오판 위험이 매우 높다.**
다만 삼성전자·현대차처럼 대기업 전략 투자와 실제 공장 적용 로드맵이 있으면 Stage 1~2까지는 가능하다.

## 2차 matrix

| 구분   | 케이스                       | 판단                                                                                                                       | 주가-점수 정합성                        |
| ---- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------- |
| 성공후보 | Rainbow Robotics          | 삼성전자가 2,670억원을 투자해 최대주주가 되었고, CEO 직속 Future Robotics Office를 만든 점은 강한 Stage 1/2 신호. ([Reuters][2])                       | 대기업 편입은 강하지만 매출/OP 전환 전 Green 금지 |
| 성공후보 | Hyundai / Boston Dynamics | 현대차 로봇 narrative는 2026년 주가/시총 기대를 밀어올린 사례. Reuters는 현대차 로봇 기대와 AI 데이터센터·로봇공장 투자 뉴스로 주가가 하루 11% 오른 사례를 보도. ([Reuters][3]) | 로봇 기대가 자동차 본업 EPS와 분리되어야 함       |
| 반례   | 로봇 테마 소형주                 | MOU/테마만 있고 매출화 없으면 false positive                                                                                        | score high 금지                    |
| 반례   | 고밸류 IPO 로봇주               | 제품력은 있어도 EPS/FCF 부재면 Theme Overheat                                                                                      | Stage 3-Green 금지                 |

## Stage 기준

```text
Stage 1:
- 대기업 투자
- 로봇 정책/테마
- MOU/PoC

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

## 점수비중

```text
EPS/FCF: 18~20
Visibility: 15
Bottleneck/Pricing: 10
Mispricing: 12
Valuation: 10
Theme penalty: 강하게
```

**주가 검증 원칙:**
로봇은 “주가가 올랐다”만으로 성공사례가 아니다. 주가 급등 후 EPS/OP가 못 따라오면 **Theme Overheat 반례**로 넣어야 한다.

---

# 5. Retail / Domestic Consumer

## 결론

리테일은 구조적 E2R보다 **소비 사이클 + 점포효율 + 재고/비용 레버리지**에 가깝다.
주가가 올라도 EPS/FCF 체급 변화가 아니라면 Stage 3 성공으로 넣으면 안 된다.

## 2차 matrix

| 구분   | 케이스            | 판단                               |
| ---- | -------------- | -------------------------------- |
| 성공후보 | BGF리테일 / GS리테일 | 점포효율, PB상품, 비용레버리지, 동일점 성장 확인 필요 |
| 성공후보 | 호텔신라 / 신세계     | 관광·면세 회복. 중국 의존도와 객단가 확인 필요      |
| 반례   | 이마트류 구조 경쟁 심화  | 온라인 경쟁, 마진 악화, 대형마트 구조 문제        |
| 반례   | 단기 소비 회복 테마    | 트래픽만 있고 OPM/FCF 개선 없으면 Stage 1   |

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

## 점수비중

```text
EPS/FCF: 18
Visibility: 16
Bottleneck/Pricing: 5
Mispricing: 14
Valuation: 14
Risk penalty: inventory / rent / wage / competition
```

**주가 검증 원칙:**
리테일은 단기 rebound가 많으니, Stage 3 성공으로 인정하려면 **OPM/FCF 개선이 2~4분기 이상 이어져야 한다.**

---

# 6. Construction / Real Estate / Credit

## 결론

건설은 수주보다 **PF·미분양·현금흐름·신용 리스크**가 먼저다.
수주잔고가 커도 신용 리스크가 있으면 Green 금지.

## 2차 matrix

| 구분   | 케이스            | 판단                                                                                      |
| ---- | -------------- | --------------------------------------------------------------------------------------- |
| 성공후보 | PF 리스크 해소형 건설사 | 부실 정리 후 cash flow 회복 시 후보                                                               |
| 성공후보 | 해외 플랜트/인프라 수주형 | 수주 질과 마진이 확정적이면 후보                                                                      |
| 반례   | PF 부실 건설사      | FSS는 부동산 프로젝트 연체율이 2021년 말 0.37%에서 2023년 말 2.70%로 상승했다고 밝혔고, 구조조정을 강화했다. ([Reuters][4]) |
| 반례   | 원가 상승 미반영      | 매출은 늘어도 원가율 상승으로 OP/FCF 훼손                                                              |

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

## 점수비중

```text
EPS/FCF: 18
Visibility: 10~12
Bottleneck/Pricing: 5
Mispricing: 12
Valuation: 10
Risk penalty: 매우 큼
```

**주가 검증 원칙:**
건설은 주가 rebound가 와도 PF/부채가 해결되지 않으면 Stage 3 성공이 아니라 **credit relief rally**로 분류해야 한다.

---

# 7. Utilities / Regulated Tariff

## 결론

유틸리티는 EPS/FCF보다 **요금·원가·부채·규제**가 핵심이다.
싸다고 Green이 아니라, 규제 프레임이 바뀌어야 한다.

## 2차 matrix

| 구분   | 케이스    | 판단                       |
| ---- | ------ | ------------------------ |
| 성공후보 | 한국전력   | 요금 정상화, 원가 안정, 부채 축소 여부  |
| 성공후보 | 한국가스공사 | 미수금 회수, 원가보상, 배당 가능성     |
| 반례   | 요금 동결  | EPS 개선 지속성 낮음            |
| 반례   | 부채 과다  | 주주환원 불가능, valuation trap |

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

## 점수비중

```text
EPS/FCF: 18
Visibility: 18
Bottleneck/Pricing: 5
Mispricing: 12
Valuation: 10
Regulatory risk cap
```

**주가 검증 원칙:**
유틸리티는 주가가 올라가도 정책/부채/배당이 같이 개선되지 않으면 E2R이 아니라 **규제 이벤트 trade**다.

---

# 8. Nuclear / SMR / Grid Policy — 별도 archetype 확정

## 결론

원전은 유틸리티가 아니라 **정책 + 수주 + 법적 리스크 + 장기 CAPEX** archetype으로 분리해야 한다.

## 2차 matrix

| 구분   | 케이스                           | 판단                                                                                                |
| ---- | ----------------------------- | ------------------------------------------------------------------------------------------------- |
| 성공후보 | KHNP / 두산에너빌리티 / 한전기술 / 한전KPS | 체코 원전, 원전 수출, 설계/정비/주기기                                                                           |
| 성공후보 | Czech Dukovany                | UOHS가 EDF 이의를 기각하면서 KHNP 계약 체결 길이 열렸으나, 이후 법원이 EDF appeal로 signing을 일시 중단한 사례가 있음. ([Reuters][5]) |
| 반례   | 수주 기대만 있는 원전 테마               | 계약 전 기대만으로 Stage 3 금지                                                                             |
| 반례   | 소송/정책 지연                      | EDF appeal처럼 법적 지연은 4C 또는 risk flag                                                               |

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

## 점수비중

```text
EPS/FCF: 18
Visibility: 22
Bottleneck/Pricing: 8
Mispricing: 14
Valuation: 12
Risk penalty: legal / policy / delay
```

**주가 검증 원칙:**
원전주는 수주 기대만으로 급등할 수 있다. Stage 3 성공으로 인정하려면 **계약 확정 + 기자재 매출화 + 마진 경로**가 필요하다.

---

# 9. Holding / Governance / Restructuring

## 결론

지주·거버넌스는 EPS 폭발보다 **NAV discount 해소와 자본배분 실행**이 핵심이다.
하지만 경영권 분쟁만으로 주가가 오른 건 E2R이 아니라 이벤트 프리미엄일 수 있다.

## 2차 matrix

| 구분   | 케이스              | 판단                                                                                  |
| ---- | ---------------- | ----------------------------------------------------------------------------------- |
| 성공후보 | SK스퀘어 / 삼성물산     | 자회사 가치, 자사주/소각, NAV discount 해소 여부                                                  |
| 성공후보 | Korea Zinc       | MBK/Young Poong 공개매수로 주가가 19.8% 급등했고, 경영권·거버넌스 이슈가 기업가치 논쟁으로 이어진 사례. ([Reuters][6]) |
| 반례   | 경영권 분쟁만 있는 종목    | EPS/FCF 변화 없이 이벤트 프리미엄만 있으면 Stage 3 금지                                              |
| 반례   | 자사주 발표만 있고 소각 없음 | value trap 가능                                                                       |

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

## 점수비중

```text
EPS/FCF: 10~12
Visibility: 18
Mispricing: 20
Valuation: 25
Capital Allocation: 10
```

**주가 검증 원칙:**
경영권 분쟁으로 주가가 올랐으면 **event premium**으로 분류하고, EPS/FCF·NAV·환원 구조가 바뀌었는지 따로 검증해야 한다.

---

# 10. Financial Spread / Balance Sheet

## 결론

금융주는 EPS 폭발보다 **ROE-PBR-주주환원**의 정합성이 핵심이다.
저PBR만으로는 절대 성공사례가 아니다.

## 2차 matrix

| 구분   | 케이스                | 판단                          |
| ---- | ------------------ | --------------------------- |
| 성공후보 | KB금융 / 신한지주 / 하나금융 | ROE, CET1, 자사주·배당, value-up |
| 성공후보 | 메리츠금융 / 삼성화재       | 자본효율, 환원정책, 보험계약마진/ROE      |
| 반례   | 단순 저PBR 금융주        | ROE/환원정책 없으면 value trap     |
| 반례   | PF/충당금 리스크 금융      | credit cost 상승이면 4C         |

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

## 점수비중

```text
EPS/FCF: 15
Visibility: 20
Bottleneck/Pricing: 5
Mispricing: 15
Valuation: 25
Capital Allocation: 10
```

**주가 검증 원칙:**
금융주는 주가가 올라가도 ROE/CET1/환원정책이 따라오지 않으면 E2R 성공이 아니라 저PBR 이벤트다.

---

# 11. Biotech / Regulatory — 세분화 필요

## 결론

바이오는 하나로 묶으면 위험하다. 세 가지로 나눠야 한다.

```text
A. Pre-revenue clinical biotech
B. Royalty / technology-transfer biotech
C. Revenue-generating pharma / CDMO
```

## 2차 matrix

| 구분   | 케이스                  | 판단                                                   |
| ---- | -------------------- | ---------------------------------------------------- |
| 성공후보 | 알테오젠                 | 기술이전/SC 제형/로열티 가능성. 실제 royalty visibility가 핵심        |
| 성공후보 | 유한양행                 | 신약 허가/로열티/매출화 여부                                     |
| 성공후보 | 삼성바이오로직스             | CDMO 장기계약/가동률. 일반 바이오보다 contract backlog healthcare형 |
| 반례   | 임상 뉴스만 있는 바이오        | EPS/FCF 전환 전 Green 금지                                |
| 반례   | CB/유증 반복 바이오         | dilution risk로 Green 차단                              |
| 반례   | 기술이전 headline만 있는 회사 | milestone/royalty 불확실하면 Stage 1~2                    |

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

## 점수비중

```text
Pre-revenue:
EPS/FCF 낮게, Green 거의 금지

Royalty/tech transfer:
Visibility = milestone + royalty probability

CDMO/revenue pharma:
EPS/FCF와 contract visibility로 평가 가능
```

**주가 검증 원칙:**
바이오는 주가가 급등해도 매출화 전이면 E2R 성공사례가 아니라 **regulatory/event premium**일 수 있다.

---

# 12. Medical Device / Healthcare Export

## 결론

의료기기는 바이오보다 E2R에 더 적합할 수 있다.
이유는 **제품 판매 + 소모품 반복매출 + 수출채널 + OPM**이 확인 가능하기 때문이야.

## 2차 matrix

| 구분   | 케이스             | 판단                                                              |
| ---- | --------------- | --------------------------------------------------------------- |
| 성공후보 | Classys         | 비침습 피부미용 의료기기 회사이고, 2025년 기준 60개국 이상 수출한다고 정리되어 있음. ([위키백과][7]) |
| 성공후보 | 파마리서치 / 휴젤 / 원텍 | 수출, 인허가, 소모품/시술 반복 확인 필요                                        |
| 반례   | 단일 장비 판매        | 반복 소모품/서비스 없으면 visibility 낮음                                    |
| 반례   | 허가 지연           | 매출화 지연이면 4C                                                     |

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

## 점수비중

```text
EPS/FCF: 20
Visibility: 22
Bottleneck/Pricing: 13
Mispricing: 14
Valuation: 12
```

**주가 검증 원칙:**
의료기기는 장비 판매만으로 Green 금지. 반복 소모품·시술·수출 재주문이 있어야 Stage 3 가능.

---

# 13. Travel / Leisure / Reopening — 신규 archetype

## 결론

리테일과 분리해야 한다.
여행·카지노·항공·면세는 **reopening / 관광 / 환율 / 유가 / 중국 의존**의 사이클성이 강하다.

## 2차 matrix

| 구분   | 케이스                | 판단                                   |
| ---- | ------------------ | ------------------------------------ |
| 성공후보 | 파라다이스 / GKL        | 카지노 drop amount, 일본/중국 VIP, 관광객 회복   |
| 성공후보 | 호텔신라 / 신세계         | 면세·관광 회복, 중국 의존도 확인                  |
| 성공후보 | 대한항공 / 제주항공        | 여객 회복, 유가, 환율, 화물 정상화                |
| 반례   | 중국 단체관광 기대만 있는 면세주 | actual traffic/매출 없이 기대만 있으면 Stage 1 |
| 반례   | 유가 급등 항공주          | 수요는 좋아도 마진 훼손                        |

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

## 점수비중

```text
EPS/FCF: 18
Visibility: 14
Bottleneck/Pricing: 5
Mispricing: 12
Valuation: 10
Cyclical risk cap
```

**주가 검증 원칙:**
Reopening 주가는 강하게 튈 수 있지만, traffic peak 후 EPS가 꺾이면 Stage 3 성공이 아니라 cycle trade다.

---

# 14. AI Data Center Infrastructure — 신규 archetype 확정

## 결론

이건 이제 독립 archetype으로 분리해야 한다.
전력기기 하나로 묶기엔 너무 넓다.

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

## 성공후보

| 구분   | 케이스                   | 판단                             |
| ---- | --------------------- | ------------------------------ |
| 성공후보 | HD현대일렉트릭 / 효성중공업      | 데이터센터 전력망·변압기 수요               |
| 성공후보 | LS ELECTRIC / LS전선 관련 | 전력망, 전선, 배전                    |
| 성공후보 | 이수페타시스                | AI 서버/네트워크 PCB                 |
| 성공후보 | 냉각/공조 관련 기업           | 데이터센터 cooling exposure 확인 필요   |
| 반례   | AI 데이터센터 테마만 붙은 기업    | 실제 수주/매출 exposure 없으면 Green 금지 |
| 반례   | CAPEX 기대 선반영          | valuation이 먼저 간 경우 4B-watch    |

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

## 점수비중

```text
EPS/FCF: 22
Visibility: 23
Bottleneck/Pricing: 20
Mispricing: 14
Valuation: 12
Risk penalty: AI capex cut / project delay
```

**주가 검증 원칙:**
AI 데이터센터 테마는 주가가 먼저 움직이기 쉽다. 실제 수주·납품·EPS revision 없으면 Theme Overheat로 내려야 한다.

---

# 15. Education / Specialty Services — 신규 archetype 후보

## 왜 추가?

교육·시험·특수 서비스는 플랫폼도 아니고 소비재도 아니다.
반복 수강, 정책 변화, 해외 진출, 가격 인상, B2B/B2C subscription이 핵심이다.

## 성공후보

```text
메가스터디교육:
입시/사교육, 반복 수강, 가격/학생 수.

웅진씽크빅 / 대교:
학습지/에듀테크, 반복매출.

특수 시험/자격 서비스 기업:
규제/정책 변화로 수요 증가 가능.
```

## 반례

```text
- 저출산으로 TAM 축소
- 정책 규제
- 단기 입시 제도 변경 수혜
- AI 튜터 경쟁으로 가격 하락
```

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

## 점수비중

```text
EPS/FCF: 18
Visibility: 20
Bottleneck/Pricing: 5
Mispricing: 12
Valuation: 12
Risk: population / regulation
```

---

# 16. 이번 라운드의 “점수-주가 정합성” 규칙

이제 case library에 아래 규칙을 넣어야 한다.

## 성공사례로 인정하려면

```text
1. Stage 2/3 신호 발생 후 주가가 6~24개월 안에 의미 있게 리레이팅
2. EPS/OP/FCF revision이 주가 상승과 같이 움직임
3. 상승이 단순 테마가 아니라 실적/계약/수출/ROE/환원과 연결
4. peak 이후에도 4B/4C 신호가 설명 가능
```

## 반례로 넣어야 하는 경우

```text
1. 점수상 좋아 보였지만 주가가 리레이팅되지 않음
2. 주가는 올랐지만 EPS/FCF가 안 따라옴
3. Stage 3처럼 보였지만 4C가 빨리 옴
4. 리포트는 좋았지만 실제 매출화 실패
5. 테마/이벤트 프리미엄이 끝나자 주가 하락
```

## 점수비중 실패 판정

```text
A. Platform에서 MAU/AI 키워드로 높은 점수
   → 주가 리레이팅 없음
   → ARPU/OPM/FCF 가중치를 더 높이고 MAU 가중치 낮춤

B. Robotics에서 대기업 투자 뉴스로 높은 점수
   → 매출화 없음
   → customer adoption / revenue conversion gate 추가

C. Biotech에서 임상 뉴스로 높은 점수
   → 유증/임상지연
   → pre-revenue Green 차단

D. Shipping에서 EPS 폭발로 높은 점수
   → 운임 정상화 후 붕괴
   → cyclical cap / 4B trigger 강화

E. Governance에서 공개매수로 높은 점수
   → 이벤트 종료 후 주가 하락
   → event premium과 structural governance rerating 분리
```

---

# 17. 다음에 에이전트에 넣어야 할 case-library 구조

이번 라운드부터는 아래 형식으로 case를 넣어야 해.

```json
{
  "case_id": "platform_naver_candidate_2024",
  "archetype": "PLATFORM_SOFTWARE_INTERNET",
  "case_type": "candidate_or_counterexample",
  "stage1_signal": ["traffic_recovery", "ai_cost_efficiency"],
  "stage2_signal": ["op_margin_improvement", "fy1_op_revision"],
  "stage3_signal": ["recurring_revenue", "arpu_growth", "valuation_frame_shift"],
  "stage4b_signal": ["multiple_saturation", "ai_narrative_overcrowding"],
  "stage4c_signal": ["regulatory_risk", "take_rate_decline", "ai_cost_overrun"],
  "price_validation": {
    "required": true,
    "accept_success_only_if": "stage3_after_price_rerating_and_revision_support",
    "reject_if": "score_high_but_no_rerating"
  },
  "score_weight_hint": {
    "eps_fcf": 20,
    "visibility": 22,
    "bottleneck_pricing": 8,
    "mispricing": 16,
    "valuation": 14
  }
}
```

즉 이제 단순히 성공/반례를 나열하는 게 아니라, **점수와 주가가 같은 방향으로 움직였는지**를 검증 항목으로 넣어야 한다.

---

# 18. 이번 라운드 최종 정리

이번에 더 확장해서 정리한 핵심은 이거야.

```text
1. 플랫폼은 네이버/카카오를 성공사례로 쉽게 넣으면 안 된다.
   ARPU/OPM/FCF와 주가 리레이팅이 같이 확인되어야 한다.

2. 게임/IP는 신작 기대가 아니라 반복 monetization이 핵심이다.

3. 로봇은 대기업 투자 뉴스만으로 Green 금지.
   실제 수주/매출/반복매출 전환이 필요하다.

4. 리테일은 소비 회복 trade와 구조적 E2R을 분리해야 한다.

5. 건설은 수주보다 PF/현금흐름/신용 리스크가 우선이다.

6. 유틸리티는 요금/정책/부채가 핵심이고, 싸다고 Green이 아니다.

7. 원전은 별도 archetype이 필요하다.
   수주 기대와 계약 확정/매출화를 분리해야 한다.

8. 지주/거버넌스는 이벤트 프리미엄과 구조적 discount 해소를 분리해야 한다.

9. 금융은 ROE-PBR-주주환원 프레임으로 봐야 한다.

10. 바이오는 매출화 전 Green을 거의 금지해야 한다.

11. 의료기기는 반복 소모품/수출/OPM이 있으면 E2R 가능성이 있다.

12. 여행/리오프닝, AI 데이터센터 인프라, 교육/특수서비스는 추가 archetype으로 분리할 가치가 있다.

13. 성공사례와 반례는 반드시 주가 경로와 연결해야 한다.
    점수는 높았는데 주가가 안 갔으면 그건 점수 실패다.
```

다음 라운드에서는 이걸 더 실제 case record 형태로 바꿔서, **각 archetype별 “성공 2개 + 반례 2개”를 채우는 표**로 더 정리하면 된다.

[1]: https://en.wikipedia.org/wiki/Battlegrounds_Mobile_India?utm_source=chatgpt.com "Battlegrounds Mobile India"
[2]: https://www.reuters.com/technology/samsung-electronics-becomes-largest-shareholder-south-koreas-rainbow-robotics-2024-12-30/?utm_source=chatgpt.com "Samsung Electronics becomes largest shareholder of South Korea's Rainbow Robotics"
[3]: https://www.reuters.com/commentary/breakingviews/hyundai-motors-robots-herald-hardware-reboot-2026-03-04/?utm_source=chatgpt.com "Hyundai Motor's robots herald hardware reboot"
[4]: https://www.reuters.com/markets/asia/south-korea-tightens-scrutiny-speed-up-real-estate-restructuring-2024-05-13/?utm_source=chatgpt.com "South Korea tightens scrutiny to speed up real estate restructuring"
[5]: https://www.reuters.com/business/energy/czechs-clear-sign-18-billion-nuclear-power-deal-after-edf-appeals-rejected-2025-04-24/?utm_source=chatgpt.com "Czechs clear to sign $18 billion nuclear power deal after EDF appeals rejected"
[6]: https://www.reuters.com/markets/deals/private-equity-mbk-young-poong-launch-15-bln-tender-offer-korea-zinc-shares-2024-09-13/?utm_source=chatgpt.com "Private equity MBK, Young Poong launch $1.5 bln tender offer for Korea Zinc shares"
[7]: https://en.wikipedia.org/wiki/Classys?utm_source=chatgpt.com "Classys"
