# Checkpoint 28A Round58 R5 Loop 2: Consumer / Retail / Brand

## 목적

`docs/round/round_58.md`의 R5 Loop 2 내용을 반영했다. 이번 라운드는 소비재·유통·브랜드에서 반복 소비 기반 리레이팅과 일회성 viral/event를 분리하는 작업이다.

쉬운 예시는 이렇다.

- K푸드 수출 증가와 ASP 상승, OPM 개선, EPS 상향이 같이 있으면 상위 후보가 될 수 있다.
- 하지만 같은 회사라도 리콜이나 국가별 판매 제한이 나오면 Food Safety overlay가 켜져 Stage 3-Green을 재검토해야 한다.
- K뷰티도 Sephora/Ulta 입점만으로는 부족하고, 실제 sell-through와 재주문, 재고·매출채권 안정이 필요하다.

## 반영 내용

- R5 Loop 2 전용 calibration module을 추가했다.
- `BEAUTY_DEVICE_EXPORT`, `FOOD_SAFETY_RECALL_OVERLAY`, `DATA_SECURITY_SUPPLIER_REGULATION_OVERLAY` archetype을 추가했다.
- Food Safety와 Data/Supplier Regulation을 gate-only RedTeam overlay로 분리했다.
- case library JSONL, score-weight draft CSV, case matrix, stage-date plan, guardrail, risk overlay, price-validation plan을 생성했다.
- production scoring/staging/red-team 로직은 변경하지 않았다.

## 핵심 분리

- `EXPORT_RECURRING_CONSUMER`: Green 가능. 수출, ASP, 반복소비, OPM, EPS 상향, 재고 안정 필요.
- `K_BEAUTY_EXPORT_DISTRIBUTION`: Green 가능. 채널 입점보다 sell-through와 재주문이 중요.
- `BEAUTY_OEM_ODM_SUPPLYCHAIN`: Green 가능. 고객사 다변화, 반복 주문, 재고·매출채권 확인 필요.
- `RETAIL_ECOMMERCE_LOGISTICS`: Watch. GMV보다 FCF, 물류비, 데이터 보안, 공급업체 규제가 중요.
- `HOME_LIVING_APPLIANCE_RENTAL`: Watch-to-Green. 하드웨어 판매가 아니라 렌탈 계정, 해지율, 서비스 반복매출이 핵심.
- `APPAREL_FAST_FASHION_BRAND_OEM`: Watch. 재고, 할인율, IP 소송, 제품안전, 공급망 규제 리스크가 크다.
- `FOOD_SAFETY_RECALL_OVERLAY`: gate-only RedTeam.
- `DATA_SECURITY_SUPPLIER_REGULATION_OVERLAY`: gate-only RedTeam.

## 산출물

- `src/e2r/sector/round58_r5_loop2_consumer_retail_brand.py`
- `src/e2r/cli/build_round58_r5_loop2_report.py`
- `tests/test_round58_r5_loop2_consumer_retail_brand.py`
- `data/e2r_case_library/cases_r5_loop2_round58.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round58_r5_loop2_v2.csv`
- `output/e2r_round58_r5_loop2_consumer_retail_brand/round58_r5_loop2_consumer_retail_brand_summary.md`
- `output/e2r_round58_r5_loop2_consumer_retail_brand/round58_r5_loop2_case_matrix.csv`
- `output/e2r_round58_r5_loop2_consumer_retail_brand/round58_r5_loop2_stage_date_plan.csv`
- `output/e2r_round58_r5_loop2_consumer_retail_brand/round58_r5_loop2_green_guardrails.md`
- `output/e2r_round58_r5_loop2_consumer_retail_brand/round58_r5_loop2_risk_overlays.md`
- `output/e2r_round58_r5_loop2_consumer_retail_brand/round58_r5_loop2_price_validation_plan.md`
- `output/e2r_round58_r5_loop2_consumer_retail_brand/round58_r5_loop2_price_fields.csv`

## 케이스 요약

- target_count: 12
- case_candidate_count: 11
- success_candidate_count: 4
- stage4b_case_count: 1
- stage4c_case_count: 6
- green_possible_count: 3
- watch_yellow_first_count: 6
- redteam_first_count: 3
- gate_only_target_count: 2
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## 핵심 guardrail

- viral, 채널 입점, GMV, 점포 수, 생활가전 판매량만으로 Green을 만들지 않는다.
- 수출, sell-through, 재주문, OPM, EPS revision, 재고·매출채권 안정, FCF가 함께 확인되어야 한다.
- 식품 리콜, 국가별 판매금지, 데이터 유출, 공급업체 압박, 대금지연, IP 소송, 제품안전 문제는 RedTeam 필드다.
- case library는 calibration/evaluation 자료이며 candidate-generation input으로 쓰지 않는다.

## 실행 명령

```bash
PYTHONPATH=src python -m e2r.cli.build_round58_r5_loop2_report
PYTHONPATH=src python -m unittest tests.test_round58_r5_loop2_consumer_retail_brand -v
```

## 남은 일

- Stage 날짜와 가격 데이터는 아직 backfill 대상이다.
- Round58 weight는 shadow/calibration draft이며 production scoring에 적용하지 않았다.
- 다음 단계에서는 K푸드/K뷰티 sell-through, 재주문, 재고·매출채권, 이커머스 보안/규제 이벤트, 렌탈 계정/해지율 가격 경로를 채워야 한다.
