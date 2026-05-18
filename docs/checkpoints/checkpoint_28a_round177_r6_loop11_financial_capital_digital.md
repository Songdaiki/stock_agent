# Checkpoint 28A Round 177: R6 Loop 11 금융·자본배분·디지털금융 반영

## 목적

`docs/round/round_177.md`의 국장 중심 금융·자본배분·디지털금융 프레임을 case library와 score profile 초안으로 구조화했다.

이번 라운드는 은행지주, 지역은행, 보험, 증권, 인터넷은행, 네이버-Dunamu, Toss, 원화 스테이블코인, 서울보증보험, PF/보안/규제 리스크를 다룬다. 생산 점수 로직은 바꾸지 않았다.

쉬운 예시:

- `KB금융`은 저PBR이라서가 아니라 ROE, CET1, credit cost, 실제 환원, PBR band 변화가 같이 맞아야 Stage 3 후보가 된다.
- `네이버-Dunamu`는 거래 자체는 Stage 2 증거지만, abnormal withdrawal 같은 보안 이슈가 있으면 4C-watch가 붙는다.
- `Toss 관련주`는 IPO와 원화 스테이블코인 기대가 있어도 직접 지분과 수익모델이 없으면 Green이 아니다.

## 추가된 항목

- `src/e2r/sector/round177_r6_loop11_financial_capital_digital.py`
- `src/e2r/cli/build_round177_r6_loop11_report.py`
- `tests/test_round177_r6_loop11_financial_capital_digital.py`
- `data/e2r_case_library/cases_r6_loop11_round177.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round177_r6_loop11_v11.csv`
- `output/e2r_round177_r6_loop11_financial_capital_digital/`

## Archetype 확장

라운드 177 원문 canonical target 14개와 보조 4B overlay 1개를 반영했다.

- `BANK_HOLDING_VALUEUP_CAPITAL_RETURN_KOREA`
- `BANK_ROE_PBR_RERATING_KOREA`
- `BANK_CREDIT_COST_PF_OVERLAY`
- `REGIONAL_BANK_HIGH_ROE_VALUEUP`
- `INSURANCE_CAPITAL_RELEASE_VALUEUP_KOREA`
- `INSURANCE_KICS_CSM_GATE`
- `SECURITIES_BROKERAGE_MARKET_BETA`
- `SECURITIES_IB_PF_RISK_OVERLAY`
- `INTERNET_BANK_PROFITABILITY`
- `DIGITAL_ASSET_EXCHANGE_EQUITY_OPTION`
- `FINTECH_SUPERAPP_IPO_OPTION_KOREA`
- `KRW_STABLECOIN_POLICY_OPTION`
- `GUARANTEE_INSURANCE_IPO_SECURITY_RISK`
- `DISCLOSURE_CONFIDENCE_CAP`
- `VALUE_UP_CROWDED_4B_WATCH`

## Base Score Weight 초안

이 비중은 production scoring에 적용하지 않았다. 향후 shadow scoring 캘리브레이션용이다.

| 축 | 점수 |
| --- | ---: |
| ROE/EPS/FCF 지속성 | 22 |
| 자본환원 실행력 | 18 |
| 자본비율·credit cost 안정성 | 18 |
| 규제·수익모델 visibility | 14 |
| 가격경로 조기검증 | 10 |
| governance / disclosure confidence | 10 |
| valuation room / 4B 여지 | 8 |

## Stage 가드레일

- Stage 1: 저PBR, 밸류업 정책, 고배당, Toss IPO, stablecoin, Dunamu 지분가치는 research routing 신호다.
- Stage 2: 실제 소각·배당, ROE/CET1/K-ICS 안정, 지분취득, IPO filing, 규제안, 사용자·거래액 확인까지 가능하다.
- Stage 3: 8개 조건 중 5개 이상이 필요하다.
- Stage 4B: Stage 2 이후 120D MFE +60%, PBR 상단 돌파, 환원보다 valuation 선반영, 금융주 basket 동반 급등, credit cost 확인 전 주가 상승 중 3개 이상이면 watch가 필요하다.
- Stage 4C: CET1/K-ICS 급락, PF credit cost spike, 환원 축소, 자본조달 압박, 거래소 해킹/이상출금, IPO valuation cut, stablecoin issuer margin 훼손, ransomware 금융 서비스 중단은 hard review다.

## Case Pack

13개 case candidate를 추가했다.

- `kb_financial_valueup_stage3_candidate`
- `shinhan_overseas_profit_valueup_candidate`
- `woori_financial_nonbank_capital_buffer_gate_case`
- `jb_financial_regional_high_roe_valueup_case`
- `korea_insurance_capital_release_valueup_case`
- `kakaobank_profitability_valuation_cap_case`
- `naver_dunamu_equity_option_security_4c_watch_case`
- `toss_superapp_ipo_stablecoin_related_stock_cap_case`
- `seoul_guarantee_ipo_ransomware_security_case`
- `securities_brokerage_market_beta_cycle_case`
- `financial_valueup_crowded_4b_watch_case`
- `bank_credit_cost_pf_overlay_case`
- `financial_disclosure_confidence_cap_case`

## 산출물

생성 명령:

```bash
PYTHONPATH=src python -m e2r.cli.build_round177_r6_loop11_report
```

주요 산출물:

- `output/e2r_round177_r6_loop11_financial_capital_digital/round177_r6_loop11_financial_capital_digital_summary.md`
- `output/e2r_round177_r6_loop11_financial_capital_digital/round177_r6_loop11_case_matrix.csv`
- `output/e2r_round177_r6_loop11_financial_capital_digital/round177_r6_loop11_stage_date_plan.csv`
- `output/e2r_round177_r6_loop11_financial_capital_digital/round177_r6_loop11_green_guardrails.md`
- `output/e2r_round177_r6_loop11_financial_capital_digital/round177_r6_loop11_risk_overlays.md`
- `output/e2r_round177_r6_loop11_financial_capital_digital/round177_r6_loop11_price_validation_plan.md`
- `output/e2r_round177_r6_loop11_financial_capital_digital/round177_r6_loop11_score_stage_price_alignment.md`

## 검증

라운드 전용 테스트:

```bash
PYTHONPATH=src python -m unittest tests.test_round177_r6_loop11_financial_capital_digital -v
```

확인한 가드레일:

- production scoring 변경 없음
- case records는 candidate-generation input이 아님
- 저PBR, 밸류업, 고배당, Toss IPO, stablecoin, Dunamu 지분가치는 단독 Green 신호가 아님
- CET1, K-ICS, credit cost, PF exposure, 환원 실행, 지분가치, 보안 복구, stage price, MFE/MAE는 없으면 비워 둠

## 다음 작업

- 은행/보험/증권 KRX price path backfill
- ROE, CET1, K-ICS, credit cost, PF exposure, reserve build backfill
- 자사주 소각·배당 detail fetch와 OpenDART normalizer 보강
- 네이버-Dunamu 보안/승인 이벤트와 price-path 연결
- Toss/스테이블코인 관련주는 직접 지분·수익모델 확인 전 Green 제한 유지
