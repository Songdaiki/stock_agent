# Checkpoint 28A Round 190: R6 Loop 12 Financial / Capital / Digital

`docs/round/round_190.md`의 R6 Loop 12 내용을 calibration pack으로 반영했다.

## 반영 범위

- `src/e2r/sector/archetypes.py`
- `src/e2r/sector/round190_r6_loop12_financial_capital_digital.py`
- `src/e2r/cli/build_round190_r6_loop12_report.py`
- `tests/test_round190_r6_loop12_financial_capital_digital.py`
- `data/e2r_case_library/cases_r6_loop12_round190.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round190_r6_loop12_v12.csv`
- `output/e2r_round190_r6_loop12_financial_capital_digital/*`

## 핵심 분류

이번 라운드는 금융·자본배분·디지털금융을 다음 11개 target으로 쪼갰다.

- `INSURANCE_NAV_VALUEUP_SAMSUNG_ELECTRONICS_STAKE`
- `SHAREHOLDER_RETURN_COMPOUNDING_FINANCIAL_HOLDCO`
- `DIGITAL_ASSET_BANK_EQUITY_OPTION`
- `KRW_STABLECOIN_POLICY_THEME`
- `PAYMENT_BIOMETRIC_INFRASTRUCTURE`
- `PAYMENT_PRIVACY_REGULATORY_4C`
- `CREDIT_INFORMATION_RECURRING_DATA`
- `SECURITIES_BROKERAGE_MARKET_BETA`
- `BUYBACK_EXECUTION_PRICE_FAILED`
- `POLICY_TAX_REVERSAL_MARKET_SHOCK`
- `DISCLOSURE_CONFIDENCE_CAP`

예를 들어 `KRW_STABLECOIN_POLICY_THEME`은 주가가 먼저 크게 움직일 수 있지만, 실제 발행량·reserve income·take-rate·규제 프레임이 없으면 Stage 3-Green이 아니라 4B-watch로 식힌다.

## 케이스팩

- target_count: 11
- case_candidate_count: 13
- success_candidate_count: 5
- cyclical_success_count: 1
- failed_rerating_count: 2
- stage4b_case_count: 2
- stage4c_case_count: 3
- hard_gate_target_count: 3

대표 케이스:

- `samsung_life_insurance_nav_valueup_stage23_case`: 삼성전자 지분/NAV는 Stage 2 근거지만, K-ICS·CSM·ROE·환원 실행 전 Green 금지.
- `meritz_financial_shareholder_return_stage23_case`: 반복 환원과 ROE가 자본비율·credit cost와 같이 맞아야 Green 후보.
- `hana_financial_dunamu_equity_option_stage2_case`: Dunamu 지분가치는 옵션이지만 equity-method income과 보안/규제가 필요.
- `krw_stablecoin_policy_theme_4b_watch_case`: 원화 스테이블코인 정책 테마와 가격 급등은 4B-watch.
- `kakaopay_privacy_regulatory_4c_watch_case`: 개인정보·동의·플랫폼 신뢰 문제는 결제 플랫폼 hard gate.
- `samsung_electronics_buyback_execution_price_failed_case`: 실제 자사주 소각도 영업 논리와 가격 검증이 실패하면 rerating 근거가 약하다.

## Guardrail

생산 점수 로직은 바꾸지 않았다.

- production_scoring_changed: false
- case_records_are_candidate_generation_input: false
- Stage 3-Green은 “저PBR”, “밸류업”, “스테이블코인”, “Dunamu”, “FacePay”, “자사주 소각” 키워드만으로 만들 수 없다.
- 6 of 9 조건: ROE/순이익 YoY 개선, CET1/K-ICS/CSM 안정, 실제 소각 또는 배당 확대, credit cost/PF reserve 안정, Stage 2 이후 60D MFE +20%, PBR band 상승, 반복 환원정책 또는 TSR 목표, 디지털금융 take-rate/발행량/equity-method income, 개인정보·보안·규제 hard issue 없음.
- 4B 조건: Stage 2 이후 120D MFE +60%, 금융 value-up/stablecoin/Dunamu 키워드가 실적보다 먼저 가격을 두 배로 밀어올림, ROE/EPS보다 PBR rerating이 앞섬, 실제 소각/equity-method/take-rate 부재, 정책/규제 프레임 불명확, 금융 바스켓 crowded.
- 4C hard gate: CET1/K-ICS 급락, PF credit cost spike, 환원 축소, 대규모 증자/자본압박, 거래소 보안사고, 개인정보/생체정보 유출, 스테이블코인 규제로 issuer margin 훼손, 세제 역풍, 자사주 소각 후 가격 실패와 영업 우려 우세.

## 생성 산출물

```bash
PYTHONPATH=src python -m e2r.cli.build_round190_r6_loop12_report
```

생성 파일:

- `data/e2r_case_library/cases_r6_loop12_round190.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round190_r6_loop12_v12.csv`
- `output/e2r_round190_r6_loop12_financial_capital_digital/round190_r6_loop12_financial_capital_digital_summary.md`
- `output/e2r_round190_r6_loop12_financial_capital_digital/round190_r6_loop12_case_matrix.csv`
- `output/e2r_round190_r6_loop12_financial_capital_digital/round190_r6_loop12_stage_date_plan.csv`
- `output/e2r_round190_r6_loop12_financial_capital_digital/round190_r6_loop12_green_guardrails.md`
- `output/e2r_round190_r6_loop12_financial_capital_digital/round190_r6_loop12_risk_overlays.md`
- `output/e2r_round190_r6_loop12_financial_capital_digital/round190_r6_loop12_price_validation_plan.md`
- `output/e2r_round190_r6_loop12_financial_capital_digital/round190_r6_loop12_price_fields.csv`
- `output/e2r_round190_r6_loop12_financial_capital_digital/round190_r6_loop12_base_score_weights.csv`
- `output/e2r_round190_r6_loop12_financial_capital_digital/round190_r6_loop12_stage_caps.csv`
- `output/e2r_round190_r6_loop12_financial_capital_digital/round190_r6_loop12_score_stage_price_alignment.csv`
- `output/e2r_round190_r6_loop12_financial_capital_digital/round190_r6_loop12_score_stage_price_alignment.md`

## 검증

```bash
PYTHONPATH=src python -m unittest tests/test_round190_r6_loop12_financial_capital_digital.py -v
```

결과: 통과.

## 다음 작업

R6 금융·자본배분·디지털금융은 가격경로와 실제 실행 지표 backfill이 중요하다. 다음에는 삼성생명/메리츠/하나금융/Dunamu/FacePay/NICE/스테이블코인 바스켓의 `roe`, `k_ics_ratio`, `csm`, `credit_cost`, `buyback_amount`, `cancelled_share_amount`, `digital_asset_stake_value`, `equity_method_income`, `stablecoin_issuance_volume`, `reserve_income`, `take_rate`, `privacy_fine_flag`, `60D/120D MFE`를 채워 Stage 2와 Stage 3-Watch 경계를 검증해야 한다.
