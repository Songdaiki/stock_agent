맞아. 이제는 **말로만 “성공 후보/반례”를 나열하는 단계에서, 실제 에이전트가 먹을 수 있는 case record 형태로 중간 패치**를 넣어야 해.

현재 레포의 28A는 아직 “분류/케이스 라이브러리의 뼈대”야. `sector_taxonomy_summary` 기준으로 full live taxonomy는 아직 아니고, fixture-only 상태이며 mapped symbols는 13개, archetypes used는 8개뿐이야.
또 case library coverage도 25개 archetype 중 “성공 2개 + 반례 2개” 조건을 만족한 항목이 0개라서 전부 insufficient coverage로 남아 있어.
그래서 추천 점수비중도 전부 “아직 적용하지 말 것”으로 되어 있는 게 맞아.

이번 중간 체크포인트의 목표는 이거야.

```text
1. 지금까지 우리가 확장한 archetype을 정리한다.
2. 성공/반례/4B/4C 후보를 case record 형태로 넣는다.
3. 각 case에 “점수-주가 정합성 검증” 필드를 추가한다.
4. 아직 production scoring은 바꾸지 않는다.
5. 에이전트가 price path/MFE/MAE를 채운 뒤, 점수비중을 다시 검증하게 한다.
```

---

# 1. 지금까지 얼마나 분류했나

## 대섹터 기준

지금까지 나는 전체 시장을 대략 **10개 대섹터**로 나눴어.

| 대섹터          | 역할                                               |
| ------------ | ------------------------------------------------ |
| 산업재/수주       | 전력기기, 방산, 조선, 원전, 산업재                            |
| AI/반도체/데이터센터 | 메모리, HBM, 반도체 장비, PCB, IDC, 냉각, 전력망              |
| 수출소비재/브랜드    | K푸드, K뷰티, 의료기기, 브랜드 소비재                          |
| 금융/자본배분      | 은행, 보험, 증권, 지주사, value-up                        |
| 사이클/스프레드     | 해운, 정유, 화학, 철강, 원자재                              |
| 플랫폼/IP/서비스   | 플랫폼, 게임, 콘텐츠, 교육, 특수서비스                          |
| 바이오/헬스케어     | pre-revenue biotech, royalty biotech, CDMO, 의료기기 |
| 내수/리오프닝      | 리테일, 면세, 카지노, 항공, 여행                             |
| 부동산/신용       | 건설, PF, 리츠, 신용위험                                 |
| 테마/일회성/과열    | one-off demand, theme overheat, price-only rally |

## Archetype 기준

처음 25개에서 출발했고, 이후 라운드에서 추가 세분화해서 현재는 **32개 정도**로 보는 게 맞아.

```text
1. CONTRACT_BACKLOG_INDUSTRIAL
2. DEFENSE_GOVERNMENT_BACKLOG
3. SHIPBUILDING_OFFSHORE_BACKLOG
4. EXPORT_RECURRING_CONSUMER
5. K_BEAUTY_EXPORT_DISTRIBUTION
6. MEMORY_HBM_CAPACITY
7. SEMI_EQUIPMENT_CAPEX
8. AI_DATA_CENTER_INFRASTRUCTURE
9. NUCLEAR_SMR_GRID_POLICY
10. BATTERY_MATERIALS_CAPEX_OVERHEAT
11. COMMODITY_SPREAD
12. RARE_METALS_STRATEGIC_MATERIALS
13. SHIPPING_FREIGHT_CYCLE
14. AUTO_MOBILITY_COMPLETED_VEHICLE
15. AUTO_MOBILITY_COMPONENTS
16. ROBOTICS_FACTORY_AUTOMATION
17. PLATFORM_SOFTWARE_INTERNET
18. GAME_CONTENT_IP
19. FINANCIAL_SPREAD_BALANCE_SHEET
20. VALUE_UP_SHAREHOLDER_RETURN
21. HOLDING_RESTRUCTURING_GOVERNANCE
22. TURNAROUND_COST_RESTRUCTURING
23. BIOTECH_PRE_REVENUE_REGULATORY
24. BIOTECH_ROYALTY_COMMERCIALIZATION
25. CDMO_HEALTHCARE_CONTRACT
26. MEDICAL_DEVICE_HEALTHCARE_EXPORT
27. RETAIL_DOMESTIC_CONSUMER
28. TRAVEL_LEISURE_REOPENING
29. CONSTRUCTION_REAL_ESTATE_CREDIT
30. UTILITIES_REGULATED_TARIFF
31. EDUCATION_SPECIALTY_SERVICES
32. ONE_OFF_OR_THEME_RISK
```

이 분류의 핵심은 “섹터명을 외우는 것”이 아니라, **EPS/FCF 체급 변화가 어떤 구조로 지속되는지**를 나누는 거야. 서생원식 핵심도 단순 저PER이 아니라 “EPS 체급 변화 + 시장의 과거 프레임 + 리레이팅”을 찾는 구조야.

---

# 2. 성공/반례로 점수정규화를 어떻게 만들었나

기본 점수축은 서생원식 7요소를 유지해.

```text
1. EPS/FCF Explosion: 20
2. Structural Visibility: 20
3. Bottleneck / Pricing Power: 20
4. Market Mispricing: 15
5. Valuation Rerating Room: 15
6. Capital Allocation: 5
7. Information Confidence: 5
```

다만 업종마다 “Structural Visibility”의 의미가 다르기 때문에, archetype별로 내부 비중을 바꿔야 해.

예를 들어:

```text
전력기기:
수주잔고, 계약기간, 매출대비 계약금액, CAPA, 리드타임

삼양식품/K푸드:
수출비중, 해외채널, 반복소비, OPM, ASP, FY1/FY2 EPS 상향

실리콘투/K뷰티:
해외채널, 브랜드 다변화, 반복 주문, 재고/채권, OPM/ROE

SK하이닉스/메모리:
HBM 수요, 메모리 가격, 공급규율, 장기계약/선수금, 중장기 revision

금융:
ROE, PBR-ROE gap, CET1, 주주환원, credit cost

바이오:
임상 뉴스가 아니라 매출화/로열티/FCF 전환

해운:
운임과 EPS는 인정하되 cyclical risk cap을 강하게 적용
```

## 성공사례를 통한 가중치 강화

성공사례는 아래 조건을 통과해야 해.

```text
Stage 1/2 신호 발생
+ EPS/OP/FCF 또는 수주/수출/가격/마진 증거 발생
+ 6~24개월 안에 주가 리레이팅
+ 리레이팅이 테마가 아니라 실적/계약/수출/ROE/환원과 연결
+ 이후 4B/4C 신호도 설명 가능
```

이런 사례가 있으면 해당 archetype의 핵심 증거 가중치를 강화해.

예:

```text
HD현대일렉트릭 / 일진전기
→ contract/backlog visibility와 bottleneck 가중치 강화

삼양식품
→ export/channel/OPM visibility 가중치 강화

SK하이닉스
→ HBM/capacity/long-term customer demand 가중치 강화

KB금융류
→ ROE/PBR/shareholder return 가중치 강화
```

## 반례를 통한 감점/Green 제한

반례는 아래 조건이면 들어가.

```text
주가는 올랐지만 EPS/FCF가 안 따라옴
점수상 좋아 보였지만 리레이팅 없음
일회성 EPS 폭발 후 정상화
테마/이벤트 프리미엄 종료 후 하락
Stage 3처럼 보였지만 4C가 빨리 옴
```

예:

```text
씨젠 / Zoom
→ one_off_risk 강화, Green 차단

HMM / Maersk류
→ shipping cycle risk cap 강화

에코프로비엠
→ valuation/crowding penalty 강화

SMCI
→ accounting/trust issue hard 4C

Kakao
→ governance/legal risk penalty

건설 PF
→ credit risk가 수주보다 우선
```

즉 성공은 “점수를 올리는 증거”를 알려주고, 반례는 “점수를 제한하거나 Green을 막는 조건”을 알려준다.

---

# 3. Case Record Schema v0.2

이제 case record는 이런 형태로 가는 게 좋다.

```json
{
  "case_id": "string",
  "symbol": "string|null",
  "company_name": "string",
  "market": "KR|US|GLOBAL",
  "large_sector": "string",
  "primary_archetype": "string",
  "secondary_archetypes": ["string"],
  "case_type": "structural_success|success_candidate|cyclical_success|one_off|overheat|failed_rerating|event_premium|4b_watch|4c_thesis_break",
  "stage1_date": "YYYY-MM-DD|null",
  "stage2_date": "YYYY-MM-DD|null",
  "stage3_date": "YYYY-MM-DD|null",
  "stage4b_date": "YYYY-MM-DD|null",
  "stage4c_date": "YYYY-MM-DD|null",
  "peak_date": "YYYY-MM-DD|null",
  "stage1_evidence": ["string"],
  "stage2_evidence": ["string"],
  "stage3_evidence": ["string"],
  "stage4b_evidence": ["string"],
  "stage4c_evidence": ["string"],
  "must_have_fields": ["string"],
  "red_flag_fields": ["string"],
  "price_validation": {
    "stage1_price": null,
    "stage2_price": null,
    "stage3_price": null,
    "stage4b_price": null,
    "stage4c_price": null,
    "peak_price": null,
    "mfe_90d": null,
    "mfe_180d": null,
    "mfe_1y": null,
    "mae_90d": null,
    "mae_180d": null,
    "mae_1y": null,
    "drawdown_after_peak": null,
    "below_stage3_price_flag": null,
    "price_validation_status": "needs_price_backfill"
  },
  "score_price_alignment": "unknown|aligned|false_positive_score|missed_due_to_score|price_moved_without_evidence|evidence_good_but_price_failed",
  "rerating_result": "unknown|true_rerating|cyclical_rerating|event_premium|theme_overheat|no_rerating|thesis_break|credit_relief_rally|policy_event_rerating",
  "price_pattern": "unknown|straight_rerating|stair_step_rerating|cycle_boom_bust|theme_overheat|accounting_trust_break|event_premium|credit_relief_rally|reopening_cycle|policy_contract_delay",
  "score_weight_hint": {
    "eps_fcf": 0,
    "structural_visibility": 0,
    "bottleneck_pricing": 0,
    "market_mispricing": 0,
    "valuation_rerating": 0,
    "capital_allocation": 0,
    "information_confidence": 0
  },
  "green_guardrails": ["string"],
  "notes": "string",
  "data_quality": {
    "official_data_available": false,
    "report_data_available": false,
    "price_data_available": false,
    "stage_dates_confidence": 0.0
  }
}
```

---

# 4. 중간 Case Record Pack v0.2

아래는 지금까지 라운드에서 종합한 중간 패치용 case record야.
가격 관련 필드는 아직 agent가 채워야 하니까 `needs_price_backfill`로 둔다.

## 4-1. 산업재/수주/전력/방산/조선

| case_id                          | archetype                     | type               | 성공/반례 판단 | 핵심 lesson                                                     |
| -------------------------------- | ----------------------------- | ------------------ | -------- | ------------------------------------------------------------- |
| hd_hyundai_electric_2023         | CONTRACT_BACKLOG_INDUSTRIAL   | structural_success | 성공       | 수주잔고, 리드타임, 변압기 공급부족, EPS 상향이 같이 있을 때 visibility 강화           |
| iljin_electric_2023_2024         | CONTRACT_BACKLOG_INDUSTRIAL   | structural_success | 성공       | 장기공급계약 + 계약금액/매출 + CAPA가 Stage 2/3 핵심                         |
| hyosung_heavy_2023               | CONTRACT_BACKLOG_INDUSTRIAL   | success_candidate  | 성공후보     | 저마진 수주 정리와 OPM 개선을 contract_quality 대신 margin_recovery로 반영 필요 |
| daehan_cable_like_2026           | CONTRACT_BACKLOG_INDUSTRIAL   | failed_rerating    | 반례       | 전선/전력 테마라도 수익성·희석·밸류 품질 약하면 Green 금지                          |
| hanwha_aerospace_2024            | DEFENSE_GOVERNMENT_BACKLOG    | structural_success | 성공       | 정부고객, 다년계약, 수주잔고, 납품 스케줄이 핵심                                  |
| defense_theme_no_backlog         | DEFENSE_GOVERNMENT_BACKLOG    | failed_rerating    | 반례       | 방산 테마만 있고 수주잔고/납품 스케줄 없으면 Stage 1 제한                          |
| hyundai_rotem_k2_export          | DEFENSE_GOVERNMENT_BACKLOG    | success_candidate  | 성공후보     | 전차/해외정부 계약은 계약 확정·납품·마진 경로 확인 필요                              |
| samsung_heavy_shipbuilding_cycle | SHIPBUILDING_OFFSHORE_BACKLOG | success_candidate  | 성공후보     | 선가 상승 + 저가수주 소진 + 고마진 선박 인도 확인 필요                             |
| shipbuilding_low_margin_backlog  | SHIPBUILDING_OFFSHORE_BACKLOG | failed_rerating    | 반례       | 수주잔고가 커도 저가수주/원가 상승이면 Green 금지                                |
| nuclear_czech_policy_contract    | NUCLEAR_SMR_GRID_POLICY       | success_candidate  | 성공후보     | 정책 기대와 계약 확정, 법적 리스크를 분리해야 함                                  |
| nuclear_legal_delay              | NUCLEAR_SMR_GRID_POLICY       | 4c_thesis_break    | 반례       | 소송/정책 지연은 원전 archetype의 hard risk                             |

---

## 4-2. AI/반도체/데이터센터

| case_id                           | archetype                     | type               | 성공/반례 판단 | 핵심 lesson                                      |
| --------------------------------- | ----------------------------- | ------------------ | -------- | ---------------------------------------------- |
| sk_hynix_hbm_rerating             | MEMORY_HBM_CAPACITY           | structural_success | 성공       | HBM 수요, 공급확보 경쟁, 장기계약/선수금, multi-year revision |
| sk_hynix_hbm_4b_watch             | MEMORY_HBM_CAPACITY           | 4b_watch           | 4B 후보    | 성공 후 주가 급등·시총 리레이팅이 과도해지면 4B-watch             |
| samsung_memory_recovery           | MEMORY_HBM_CAPACITY           | success_candidate  | 성공후보     | 메모리 반등만으로 Green 금지. HBM 경쟁력·중장기 revision 필요    |
| simple_dram_rebound               | MEMORY_HBM_CAPACITY           | cyclical_success   | 반례/주의    | 단순 DRAM 가격 반등은 cyclical Yellow, 구조적 Green 제한   |
| hanmi_semi_hbm_equipment          | SEMI_EQUIPMENT_CAPEX          | success_candidate  | 성공후보     | HBM 장비 병목, 고객사 CAPEX, 수주→매출화 확인                |
| semi_equipment_customer_capex_cut | SEMI_EQUIPMENT_CAPEX          | 4c_thesis_break    | 반례       | 고객사 CAPEX cut이면 장비주 4C                         |
| ai_dc_power_grid                  | AI_DATA_CENTER_INFRASTRUCTURE | structural_success | 성공후보     | AI 데이터센터 CAPEX → 전력/냉각/PCB/전력망 병목              |
| ai_dc_theme_no_order              | AI_DATA_CENTER_INFRASTRUCTURE | theme_overheat     | 반례       | AI DC 테마만 있고 수주/납품/EPS 없으면 Green 금지            |
| esopcb_ai_server                  | AI_DATA_CENTER_INFRASTRUCTURE | success_candidate  | 성공후보     | AI 서버/네트워크 PCB는 DC infra로 따로 분류                |

---

## 4-3. 수출소비재/K푸드/K뷰티/의료기기

| case_id                     | archetype                        | type               | 성공/반례 판단 | 핵심 lesson                            |
| --------------------------- | -------------------------------- | ------------------ | -------- | ------------------------------------ |
| samyang_foods_2024          | EXPORT_RECURRING_CONSUMER        | structural_success | 성공       | 수출비중, 반복소비, OPM, ASP, FY1/FY2 EPS 상향 |
| one_product_fad_consumer    | EXPORT_RECURRING_CONSUMER        | failed_rerating    | 반례       | 단일 제품 유행이 반복소비/채널로 이어지지 않으면 Green 금지 |
| consumer_recall_regulation  | EXPORT_RECURRING_CONSUMER        | 4c_thesis_break    | 반례       | 리콜/규제/ASP 하락은 4C                     |
| silicontwo_2024             | K_BEAUTY_EXPORT_DISTRIBUTION     | success_candidate  | 성공후보     | 해외채널, 반복주문, 브랜드 다변화, OPM/ROE 필요      |
| apr_kbeauty_device          | K_BEAUTY_EXPORT_DISTRIBUTION     | success_candidate  | 성공후보     | 브랜드+디바이스+해외채널 복합형                    |
| kbeauty_china_dependency    | K_BEAUTY_EXPORT_DISTRIBUTION     | failed_rerating    | 반례       | 중국 의존/단일채널이면 Green 제한                |
| kbeauty_channel_stuffing    | K_BEAUTY_EXPORT_DISTRIBUTION     | 4c_thesis_break    | 반례       | 재고/매출채권 악화는 4C                       |
| classys_medical_export      | MEDICAL_DEVICE_HEALTHCARE_EXPORT | success_candidate  | 성공후보     | 수출국, 소모품 반복매출, OPM, FCF conversion   |
| single_device_no_consumable | MEDICAL_DEVICE_HEALTHCARE_EXPORT | failed_rerating    | 반례       | 단일 장비 판매만 있고 반복소모품 없으면 visibility 낮음 |
| medical_approval_delay      | MEDICAL_DEVICE_HEALTHCARE_EXPORT | 4c_thesis_break    | 반례       | 허가 지연/경쟁 심화/ASP 하락                   |

---

## 4-4. 금융/지주/value-up/거버넌스

| case_id                   | archetype                        | type              | 성공/반례 판단 | 핵심 lesson                            |
| ------------------------- | -------------------------------- | ----------------- | -------- | ------------------------------------ |
| kb_financial_valueup      | FINANCIAL_SPREAD_BALANCE_SHEET   | success_candidate | 성공후보     | ROE, PBR, CET1, 자사주/배당이 같이 있어야 함     |
| meritz_financial_return   | FINANCIAL_SPREAD_BALANCE_SHEET   | success_candidate | 성공후보     | 자본효율과 반복 환원정책                        |
| low_pbr_no_roe_bank       | FINANCIAL_SPREAD_BALANCE_SHEET   | failed_rerating   | 반례       | 저PBR만 있고 ROE/환원 없으면 value trap       |
| pf_credit_cost_financial  | FINANCIAL_SPREAD_BALANCE_SHEET   | 4c_thesis_break   | 반례       | PF/충당금 증가는 금융 4C                     |
| sk_square_valueup         | HOLDING_RESTRUCTURING_GOVERNANCE | success_candidate | 성공후보     | NAV discount, 자사주 소각, 자회사 가치         |
| korea_zinc_event_premium  | RARE_METALS_STRATEGIC_MATERIALS  | event_premium     | 이벤트/반례   | 경영권 이벤트와 구조적 FCF 리레이팅 분리 필요          |
| holding_buyback_no_cancel | HOLDING_RESTRUCTURING_GOVERNANCE | failed_rerating   | 반례       | 자사주 발표만 있고 소각/반복환원 없으면 실패            |
| governance_dispute_no_fcf | HOLDING_RESTRUCTURING_GOVERNANCE | event_premium     | 반례       | 경영권 분쟁만 있고 EPS/FCF 변화 없으면 Stage 3 금지 |

---

## 4-5. 사이클/스프레드/건설/리오프닝

| case_id                        | archetype                        | type              | 성공/반례 판단 | 핵심 lesson                                    |
| ------------------------------ | -------------------------------- | ----------------- | -------- | -------------------------------------------- |
| hmm_2021_freight_cycle         | SHIPPING_FREIGHT_CYCLE           | cyclical_success  | 사이클 성공   | 운임 급등으로 EPS 폭발 가능. 구조적 Green은 제한             |
| shipping_overcapacity_4c       | SHIPPING_FREIGHT_CYCLE           | 4c_thesis_break   | 반례       | 운임 하락·선복 과잉은 4C                              |
| refining_spread_recovery       | COMMODITY_SPREAD                 | success_candidate | 성공후보     | 정제마진/제품 spread는 Stage 2 가능, Green 제한         |
| chemical_china_oversupply      | COMMODITY_SPREAD                 | 4c_thesis_break   | 반례       | 중국 공급과잉은 화학 4C                               |
| ecopro_bm_2023                 | BATTERY_MATERIALS_CAPEX_OVERHEAT | overheat          | 반례       | EV 소재 성장이라도 valuation/crowding이 앞서면 Green 금지 |
| battery_capa_overbuild         | BATTERY_MATERIALS_CAPEX_OVERHEAT | 4c_thesis_break   | 반례       | CAPA 과잉, 광물가격, EV 수요 둔화                      |
| construction_pf_stress         | CONSTRUCTION_REAL_ESTATE_CREDIT  | 4c_thesis_break   | 반례       | PF/미분양/신용위험은 수주보다 우선                         |
| overseas_infra_margin_contract | CONSTRUCTION_REAL_ESTATE_CREDIT  | success_candidate | 성공후보     | 해외수주라도 마진 확정과 현금흐름 필요                        |
| korean_air_reopening           | TRAVEL_LEISURE_REOPENING         | cyclical_success  | 사이클 후보   | 리오프닝/통합 시너지 가능. 유가·환율·수요 둔화 감시               |
| dutyfree_china_tourism_only    | TRAVEL_LEISURE_REOPENING         | failed_rerating   | 반례       | 중국 단체관광 기대만 있고 actual OP 없으면 Stage 1         |

---

## 4-6. 플랫폼/게임/로봇/교육

| case_id                     | archetype                    | type              | 성공/반례 판단 | 핵심 lesson                                    |
| --------------------------- | ---------------------------- | ----------------- | -------- | -------------------------------------------- |
| naver_platform_candidate    | PLATFORM_SOFTWARE_INTERNET   | success_candidate | 후보       | ARPU, OPM, FCF, AI 비용 통제 확인 전 성공 금지          |
| kakao_governance_risk       | PLATFORM_SOFTWARE_INTERNET   | 4c_thesis_break   | 반례       | 플랫폼 자산보다 governance/legal risk가 valuation 눌림 |
| douzone_saas_candidate      | PLATFORM_SOFTWARE_INTERNET   | success_candidate | 후보       | ERP/SaaS 반복매출과 OPM 레버리지 확인                   |
| mau_only_platform           | PLATFORM_SOFTWARE_INTERNET   | failed_rerating   | 반례       | MAU만 있고 수익화 없으면 Green 금지                     |
| krafton_ip_candidate        | GAME_CONTENT_IP              | success_candidate | 후보       | 글로벌 IP, 반복 monetization, 규제 리스크 확인           |
| new_game_hype_fail          | GAME_CONTENT_IP              | 4c_thesis_break   | 반례       | 출시 전 주가만 오르고 매출 실패하면 4C                      |
| rainbow_robotics_samsung    | ROBOTICS_FACTORY_AUTOMATION  | success_candidate | 후보       | 대기업 편입은 Stage 1/2. 매출화 전 Green 금지            |
| robot_tam_no_revenue        | ROBOTICS_FACTORY_AUTOMATION  | theme_overheat    | 반례       | TAM/MOU만 있고 매출 없으면 Green 금지                  |
| megastudy_education         | EDUCATION_SPECIALTY_SERVICES | success_candidate | 후보       | 반복수강, 가격, 수강생 수, 저출산 리스크                     |
| education_policy_regulation | EDUCATION_SPECIALTY_SERVICES | 4c_thesis_break   | 반례       | 사교육 규제·학생 수 감소·AI 경쟁                         |

---

## 4-7. 바이오/CDMO/로열티

| case_id                        | archetype                         | type              | 성공/반례 판단 | 핵심 lesson                                         |
| ------------------------------ | --------------------------------- | ----------------- | -------- | ------------------------------------------------- |
| samsung_biologics_cdmo         | CDMO_HEALTHCARE_CONTRACT          | success_candidate | 후보       | 장기계약, capacity, 고객사, 가동률                          |
| celltrion_biosimilar           | CDMO_HEALTHCARE_CONTRACT          | success_candidate | 후보       | 바이오시밀러 매출화, 가격경쟁, FCF                             |
| cdmo_capacity_underutilization | CDMO_HEALTHCARE_CONTRACT          | 4c_thesis_break   | 반례       | 설비는 늘었는데 가동률 하락하면 4C                              |
| yuhan_lazertinib               | BIOTECH_ROYALTY_COMMERCIALIZATION | success_candidate | 후보       | approval → commercialization → royalty/revenue 경로 |
| alteogen_royalty               | BIOTECH_ROYALTY_COMMERCIALIZATION | success_candidate | 후보       | 기술이전 headline보다 royalty visibility가 핵심            |
| prerevenue_clinical_biotech    | BIOTECH_PRE_REVENUE_REGULATORY    | failed_rerating   | 반례       | 임상 뉴스만으로 Green 금지                                 |
| biotech_cb_dilution            | BIOTECH_PRE_REVENUE_REGULATORY    | 4c_thesis_break   | 반례       | 유증/CB 반복은 dilution hard risk                      |
| seegene_2020_red               | ONE_OFF_OR_THEME_RISK             | one_off           | 반례       | EPS 폭발이 있어도 팬데믹 일회성 수요                            |
| smci_2024_accounting           | ONE_OFF_OR_THEME_RISK             | 4c_thesis_break   | 반례       | AI 서버 성장이라도 회계/신뢰 이슈는 hard 4C                     |

---

# 5. 실제 JSONL 예시

아래는 에이전트에 넣을 때 형태 예시야. 전부 다 JSONL로 넣기엔 답변이 너무 길어지니까, archetype별 대표만 보여줄게. 지시문에서는 위 테이블을 전체 JSONL로 변환하게 시키면 된다.

```jsonl
{"case_id":"hd_hyundai_electric_2023","symbol":"267260","company_name":"HD현대일렉트릭","market":"KR","large_sector":"산업재/수주","primary_archetype":"CONTRACT_BACKLOG_INDUSTRIAL","secondary_archetypes":["AI_DATA_CENTER_INFRASTRUCTURE"],"case_type":"structural_success","stage1_date":"2023-05-01","stage2_date":"2023-07-27","stage3_date":"2023-07-27","stage4b_date":null,"stage4c_date":null,"stage1_evidence":["전력망/변압기 수요","수주잔고 키워드"],"stage2_evidence":["공급계약","OP/EPS 상향","리포트 목표가 상향"],"stage3_evidence":["리드타임 장기화","수주잔고/매출 visibility","시장 과거 산업재 프레임"],"stage4b_evidence":["목표가 상향 과밀","신규수주 둔화","valuation saturation"],"stage4c_evidence":["계약 취소","ASP/OPM 하락","CAPA 과잉"],"must_have_fields":["contract_amount_to_prior_sales","contract_duration_months","backlog_to_sales","fy1_op","fy1_eps","lead_time_extended"],"red_flag_fields":["contract_cancellation","margin_compression","capacity_overbuild"],"score_price_alignment":"unknown","rerating_result":"unknown","price_pattern":"stair_step_rerating","score_weight_hint":{"eps_fcf":20,"structural_visibility":24,"bottleneck_pricing":22,"market_mispricing":12,"valuation_rerating":12,"capital_allocation":1,"information_confidence":5},"green_guardrails":["requires_disclosure_financial_report_cross_evidence","requires_low_red_team_risk"],"data_quality":{"official_data_available":true,"report_data_available":true,"price_data_available":true,"stage_dates_confidence":0.8}}
{"case_id":"samyang_foods_2024","symbol":"003230","company_name":"삼양식품","market":"KR","large_sector":"수출소비재/브랜드","primary_archetype":"EXPORT_RECURRING_CONSUMER","secondary_archetypes":[],"case_type":"structural_success","stage1_date":"2024-05-16","stage2_date":"2024-05-16","stage3_date":null,"stage4b_date":null,"stage4c_date":null,"stage1_evidence":["수출 급증","실적 서프라이즈"],"stage2_evidence":["FY1/FY2 EPS 상향","수출비중 상승","OPM expansion"],"stage3_evidence":["반복소비","해외채널 다변화","ASP 유지","시장 내수 음식료 프레임"],"stage4b_evidence":["margin peak","글로벌 브랜드 프레임 과밀"],"stage4c_evidence":["수출 둔화","해외 재고","리콜/규제","ASP/OPM 하락"],"must_have_fields":["export_ratio","export_growth_pct","overseas_channel_expansion","recurring_consumer_demand","opm","fy1_eps","fy2_eps"],"red_flag_fields":["inventory_build","recall_regulation","export_slowdown","asp_decline"],"score_price_alignment":"unknown","rerating_result":"unknown","price_pattern":"straight_rerating","score_weight_hint":{"eps_fcf":22,"structural_visibility":23,"bottleneck_pricing":12,"market_mispricing":16,"valuation_rerating":13,"capital_allocation":0,"information_confidence":5},"green_guardrails":["contract_quality_not_required","requires_export_channel_and_eps_cross_evidence"],"data_quality":{"official_data_available":true,"report_data_available":true,"price_data_available":true,"stage_dates_confidence":0.75}}
{"case_id":"sk_hynix_hbm_rerating","symbol":"000660","company_name":"SK하이닉스","market":"KR","large_sector":"AI/반도체/데이터센터","primary_archetype":"MEMORY_HBM_CAPACITY","secondary_archetypes":["AI_DATA_CENTER_INFRASTRUCTURE"],"case_type":"structural_success","stage1_date":"2024-04-01","stage2_date":null,"stage3_date":null,"stage4b_date":null,"stage4c_date":null,"stage1_evidence":["HBM 수요","메모리 가격 상승","earnings turnaround"],"stage2_evidence":["FY1/FY2/FY3 OP/EPS 상향","공급규율","고객사 공급 확보 경쟁"],"stage3_evidence":["장기계약/선수금/price band","CAPA constraint","multiple-year consensus revision","PBR에서 PER 프레임 전환"],"stage4b_evidence":["주가 급등","PER 리레이팅 모두 인정","CAPEX 증설 뉴스"],"stage4c_evidence":["HBM/DRAM 가격 하락","AI capex 둔화","공급과잉","revision down"],"must_have_fields":["hbm_demand_mentioned","memory_price_increase_mentioned","supply_discipline_mentioned","fy1_op","fy2_op","consensus_revision","capacity_constraint"],"red_flag_fields":["memory_price_decline","ai_capex_cut","supply_glut","revision_down"],"score_price_alignment":"unknown","rerating_result":"unknown","price_pattern":"stair_step_rerating","score_weight_hint":{"eps_fcf":24,"structural_visibility":21,"bottleneck_pricing":19,"market_mispricing":15,"valuation_rerating":12,"capital_allocation":0,"information_confidence":5},"green_guardrails":["requires_revision_and_capacity_evidence","cyclical_rebound_alone_not_green"],"data_quality":{"official_data_available":true,"report_data_available":true,"price_data_available":true,"stage_dates_confidence":0.55}}
{"case_id":"hmm_2021_freight_cycle","symbol":"011200","company_name":"HMM","market":"KR","large_sector":"사이클/스프레드","primary_archetype":"SHIPPING_FREIGHT_CYCLE","secondary_archetypes":[],"case_type":"cyclical_success","stage1_date":"2021-03-01","stage2_date":null,"stage3_date":null,"stage4b_date":"2021-06-01","stage4c_date":null,"stage1_evidence":["spot freight spike","container shortage"],"stage2_evidence":["contract freight 반영","OP/EPS 폭발"],"stage3_evidence":[],"stage4b_evidence":["운임 peak","신규선박 공급","spot/future divergence"],"stage4c_evidence":["운임 급락","overcapacity","demand slowdown"],"must_have_fields":["freight_rate","spot_rate","contract_rate","eps_growth"],"red_flag_fields":["overcapacity","freight_rate_decline","new_vessel_supply"],"score_price_alignment":"unknown","rerating_result":"cyclical_rerating","price_pattern":"cycle_boom_bust","score_weight_hint":{"eps_fcf":20,"structural_visibility":8,"bottleneck_pricing":18,"market_mispricing":8,"valuation_rerating":8,"capital_allocation":0,"information_confidence":5},"green_guardrails":["structural_green_limited","cyclical_risk_cap_required"],"data_quality":{"official_data_available":true,"report_data_available":false,"price_data_available":true,"stage_dates_confidence":0.45}}
{"case_id":"kakao_governance_risk","symbol":null,"company_name":"Kakao","market":"KR","large_sector":"플랫폼/IP/서비스","primary_archetype":"PLATFORM_SOFTWARE_INTERNET","secondary_archetypes":["ONE_OFF_OR_THEME_RISK"],"case_type":"4c_thesis_break","stage1_date":null,"stage2_date":null,"stage3_date":null,"stage4b_date":null,"stage4c_date":null,"stage1_evidence":["플랫폼 자산","광고/커머스 회복 가능성"],"stage2_evidence":["ARPU/OPM 개선이 있을 때만"],"stage3_evidence":["반복매출과 regulation risk 낮음이 필요"],"stage4b_evidence":["AI/platform narrative 과열"],"stage4c_evidence":["governance/legal risk","규제","take-rate 하락"],"must_have_fields":["arpu_growth","opm_improvement","recurring_revenue","fy1_op"],"red_flag_fields":["governance_risk","legal_issue","regulatory_risk","ai_cost_overrun"],"score_price_alignment":"unknown","rerating_result":"thesis_break","price_pattern":"governance_trust_break","score_weight_hint":{"eps_fcf":20,"structural_visibility":22,"bottleneck_pricing":8,"market_mispricing":16,"valuation_rerating":14,"capital_allocation":0,"information_confidence":5},"green_guardrails":["traffic_or_mau_alone_not_green","requires_opm_and_fcf"],"data_quality":{"official_data_available":false,"report_data_available":false,"price_data_available":false,"stage_dates_confidence":0.0}}
```

---

# 6. 에이전트 중간 체크포인트 지시문

아래 그대로 넣으면 돼.
이번은 **Checkpoint 28B가 아니라 28A-2**로 두는 게 좋아. 아직 scoring 적용 전이니까.

```text
Goal:
Implement Checkpoint 28A-2: E2R Case Record Pack v0.2 and Price-Alignment Validation Schema.

Context:
Checkpoint 28A added:
- sector taxonomy package
- E2R archetype definitions
- case library schema
- peer normalizer design
- dry-run case mining CLI
- output coverage reports

Current limitation:
- taxonomy is still fixture-only
- case coverage is insufficient
- no archetype has 2 positive + 2 counterexample records
- recommended score weights are not applied yet

Now add the intermediate case record pack from the analyst’s Round 1~8 synthesis.
Do not change production scoring yet.
Do not use case records as candidate-generation input.
The case library is calibration/evaluation material only.

Read:
- docs/e2r_standard_flow.md
- docs/checkpoints/checkpoint_28a_sector_taxonomy_and_case_mining.md
- output/sector_taxonomy/sector_taxonomy_summary.md
- output/e2r_case_library/case_coverage_summary.md
- output/e2r_case_library/recommended_score_weights.md
- data/e2r_case_library/cases.jsonl
- src/e2r/sector/archetypes.py
- src/e2r/sector/case_library.py
- src/e2r/sector/peer_normalizer.py
- src/e2r/staging.py
- src/e2r/features.py

Part A: Extend archetype taxonomy

Add or confirm these additional archetypes:

- AI_DATA_CENTER_INFRASTRUCTURE
- NUCLEAR_SMR_GRID_POLICY
- TRAVEL_LEISURE_REOPENING
- EDUCATION_SPECIALTY_SERVICES
- RARE_METALS_STRATEGIC_MATERIALS
- VALUE_UP_SHAREHOLDER_RETURN
- BIOTECH_PRE_REVENUE_REGULATORY
- BIOTECH_ROYALTY_COMMERCIALIZATION
- CDMO_HEALTHCARE_CONTRACT
- AUTO_MOBILITY_COMPLETED_VEHICLE
- AUTO_MOBILITY_COMPONENTS

Keep existing archetypes:
- CONTRACT_BACKLOG_INDUSTRIAL
- DEFENSE_GOVERNMENT_BACKLOG
- SHIPBUILDING_OFFSHORE_BACKLOG
- EXPORT_RECURRING_CONSUMER
- K_BEAUTY_EXPORT_DISTRIBUTION
- MEMORY_HBM_CAPACITY
- SEMI_EQUIPMENT_CAPEX
- BATTERY_MATERIALS_CAPEX_OVERHEAT
- COMMODITY_SPREAD
- SHIPPING_FREIGHT_CYCLE
- ROBOTICS_FACTORY_AUTOMATION
- PLATFORM_SOFTWARE_INTERNET
- GAME_CONTENT_IP
- FINANCIAL_SPREAD_BALANCE_SHEET
- MEDICAL_DEVICE_HEALTHCARE_EXPORT
- RETAIL_DOMESTIC_CONSUMER
- CONSTRUCTION_REAL_ESTATE_CREDIT
- UTILITIES_REGULATED_TARIFF
- HOLDING_RESTRUCTURING_GOVERNANCE
- TURNAROUND_COST_RESTRUCTURING
- ONE_OFF_EVENT_DEMAND
- THEME_VALUATION_OVERHEAT
- GENERIC_UNCLASSIFIED

Part B: Expand case library schema

Update case library schema to include:

- large_sector
- secondary_archetypes
- case_type
- stage1_evidence
- stage2_evidence
- stage3_evidence
- stage4b_evidence
- stage4c_evidence
- must_have_fields
- red_flag_fields
- score_price_alignment
- rerating_result
- price_pattern
- score_weight_hint
- green_guardrails
- price_validation
  - stage1_price
  - stage2_price
  - stage3_price
  - stage4b_price
  - stage4c_price
  - peak_price
  - mfe_90d
  - mfe_180d
  - mfe_1y
  - mae_90d
  - mae_180d
  - mae_1y
  - drawdown_after_peak
  - below_stage3_price_flag
  - price_validation_status

Allowed case_type values:
- structural_success
- success_candidate
- cyclical_success
- one_off
- overheat
- failed_rerating
- event_premium
- 4b_watch
- 4c_thesis_break

Allowed score_price_alignment values:
- unknown
- aligned
- false_positive_score
- missed_due_to_score
- price_moved_without_evidence
- evidence_good_but_price_failed

Allowed rerating_result values:
- unknown
- true_rerating
- cyclical_rerating
- event_premium
- theme_overheat
- no_rerating
- thesis_break
- credit_relief_rally
- policy_event_rerating

Part C: Add case record pack v0.2

Create:
- data/e2r_case_library/cases_v02.jsonl

Include at least the following case records:

Industrial / contract:
- hd_hyundai_electric_2023
- iljin_electric_2023_2024
- hyosung_heavy_2023
- daehan_cable_like_2026
- defense_theme_no_backlog
- hyundai_rotem_k2_export
- samsung_heavy_shipbuilding_cycle
- shipbuilding_low_margin_backlog
- nuclear_czech_policy_contract
- nuclear_legal_delay

AI / semiconductor / data center:
- sk_hynix_hbm_rerating
- sk_hynix_hbm_4b_watch
- samsung_memory_recovery
- simple_dram_rebound
- hanmi_semi_hbm_equipment
- semi_equipment_customer_capex_cut
- ai_dc_power_grid
- ai_dc_theme_no_order
- esopcb_ai_server

Export consumer / beauty / healthcare:
- samyang_foods_2024
- one_product_fad_consumer
- consumer_recall_regulation
- silicontwo_2024
- apr_kbeauty_device
- kbeauty_china_dependency
- kbeauty_channel_stuffing
- classys_medical_export
- single_device_no_consumable
- medical_approval_delay

Financial / holding / governance:
- kb_financial_valueup
- meritz_financial_return
- low_pbr_no_roe_bank
- pf_credit_cost_financial
- sk_square_valueup
- korea_zinc_event_premium
- holding_buyback_no_cancel
- governance_dispute_no_fcf

Cycle / credit / reopening:
- hmm_2021_freight_cycle
- shipping_overcapacity_4c
- refining_spread_recovery
- chemical_china_oversupply
- ecopro_bm_2023
- battery_capa_overbuild
- construction_pf_stress
- overseas_infra_margin_contract
- korean_air_reopening
- dutyfree_china_tourism_only

Platform / game / robot / education:
- naver_platform_candidate
- kakao_governance_risk
- douzone_saas_candidate
- mau_only_platform
- krafton_ip_candidate
- new_game_hype_fail
- rainbow_robotics_samsung
- robot_tam_no_revenue
- megastudy_education
- education_policy_regulation

Biotech / CDMO / royalty:
- samsung_biologics_cdmo
- celltrion_biosimilar
- cdmo_capacity_underutilization
- yuhan_lazertinib
- alteogen_royalty
- prerevenue_clinical_biotech
- biotech_cb_dilution
- seegene_2020_red
- smci_2024_accounting

For cases with unknown dates/prices:
- keep price_validation_status = needs_price_backfill
- do not invent prices
- do not invent stage dates
- preserve nulls

Part D: Add price-path backfill CLI

Add:
- src/e2r/cli/backfill_case_price_paths.py
- src/e2r/sector/case_price_backfill.py
- tests/test_case_price_backfill.py

Command:
PYTHONPATH=src python -m e2r.cli.backfill_case_price_paths \
  --cases data/e2r_case_library/cases_v02.jsonl \
  --price-root data/historical_official/prices \
  --output data/e2r_case_library/cases_v02_price_filled.jsonl

It must calculate:
- stage1_price
- stage2_price
- stage3_price
- stage4b_price
- stage4c_price
- peak_price
- MFE_90D / 180D / 1Y
- MAE_90D / 180D / 1Y
- drawdown_after_peak
- below_stage3_price_flag

If price data is missing:
- keep null
- set price_validation_status = missing_price_data
- do not invent values

Part E: Add score-price alignment evaluator

Add:
- src/e2r/sector/score_price_alignment.py
- tests/test_score_price_alignment.py

Rules:
- structural_success requires price rerating after Stage 2/3 evidence.
- price rise without EPS/FCF evidence becomes price_moved_without_evidence.
- strong evidence but no price rerating becomes evidence_good_but_price_failed.
- one-off/cyclical/overheat cases should not be treated as true_rerating.
- Stage 4C after Stage 2/3 becomes thesis_break.
- event-only governance cases become event_premium unless NAV/FCF/shareholder-return improves.

Part F: Generate coverage reports

Create:
- output/e2r_case_library_v02/case_record_summary.md
- output/e2r_case_library_v02/archetype_coverage_matrix.csv
- output/e2r_case_library_v02/score_price_alignment_summary.md
- output/e2r_case_library_v02/missing_price_data_report.md
- output/e2r_case_library_v02/green_guardrail_summary.md

Reports must answer:
- How many cases are in v0.2?
- How many archetypes are covered?
- Which archetypes now have 2+ success/candidate and 2+ counterexample/risk records?
- Which archetypes still lack counterexamples?
- Which cases need price backfill?
- Which cases are event_premium rather than true_rerating?
- Which archetypes should remain Green-restricted?
- Which archetypes are eligible for future shadow scoring?

Part G: Do not change production scoring yet

Important:
- Do not modify StageClassifier thresholds.
- Do not apply score_weight_hint to live scoring yet.
- Do not use cases as candidate-generation input.
- Case records are calibration/evaluation only.

Part H: Tests

Required tests:
- cases_v02 validates schema
- case library supports new fields
- scoring modules do not import case library
- price backfill leaves null when price data missing
- score_price_alignment marks one-off/cyclical/overheat correctly
- event_premium is not true_rerating
- structural_success with missing price remains unknown, not aligned
- existing tests pass

Part I: Docs

Create:
- docs/checkpoints/checkpoint_28a_2_case_record_pack_v02.md
- docs/e2r_case_record_schema_v02.md

Checkpoint report must explain:
- why this is still calibration, not production scoring
- how many cases were added
- how score-price alignment works
- which archetypes are Green-eligible
- which archetypes are Green-restricted
- what remains before Checkpoint 28B scoring implementation

Constraints:
- No API keys in output
- No fabricated price data
- No fabricated stage dates
- No buy/sell recommendation wording
- No case labels as candidate-generation input
- Preserve as_of_date and stage dates
- Do not change production scoring yet

Done when:
- all tests pass
- cases_v02.jsonl exists
- price backfill CLI exists
- score-price alignment evaluator exists
- v0.2 reports exist
- checkpoint_28a_2_case_record_pack_v02.md exists
```

---

# 7. 지금까지의 전체 설명 요약

지금까지 우리는:

```text
1. 전체 시장을 10개 대섹터로 나눴고
2. 25개 기본 archetype을 32개 안팎으로 확장했고
3. 성공/반례/4B/4C 후보를 약 60개 case record 후보로 정리했고
4. 각 case가 어떤 점수축을 강화하거나 제한해야 하는지 정의했고
5. 점수와 주가 경로가 맞지 않으면 성공사례로 인정하지 않는 규칙을 추가했고
6. 다음 단계에서 price path를 채워 점수비중을 검증하게 만들었다.
```

핵심은 이거야.

> **성공사례는 “좋아 보이는 회사”가 아니라, 점수상 높았고 실제로 EPS/FCF와 주가가 같이 리레이팅된 케이스여야 한다.**
> **반례는 “나쁜 회사”가 아니라, 점수상 좋아 보일 수 있었지만 실제로는 일회성·사이클·이벤트·테마·4C였던 케이스다.**

이렇게 해야 나중에 에이전트가 전 종목을 볼 때, 전력기기만 잘 맞고 플랫폼·바이오·건설·해운에서 엉망이 되는 걸 막을 수 있다.
