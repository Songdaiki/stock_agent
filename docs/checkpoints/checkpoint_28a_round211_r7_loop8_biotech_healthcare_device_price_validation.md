# Checkpoint 28A Round 211 R7 Loop 8 Biotech Healthcare Device Price Validation

## 목적

라운드211은 R7 바이오·헬스케어·의료기기 가격경로 검증 팩이다.

핵심 원칙은 단순하다. `FDA 승인`이나 `좋은 논문`은 Stage 2 관심 신호가 될 수 있지만, Stage 3-Green은 처방량, 보험·수가 접근, 매출, 로열티, 가동률, 마진, FCF, 현금 runway가 확인된 뒤에만 가능하다.

예를 들면 알테오젠은 Keytruda Qlex 승인과 초기 매출이 확인되어 Stage 2→3 후보가 될 수 있지만, 알테오젠이 실제로 로열티를 인식하고 현금 유입이 확인되기 전에는 Green으로 확정하지 않는다.

## 반영 내용

- `src/e2r/sector/round211_r7_loop8_biotech_healthcare_device_price_validation.py` 추가
- `src/e2r/cli/build_round211_r7_loop8_report.py` 추가
- `tests/test_round211_r7_loop8_biotech_healthcare_device_price_validation.py` 추가
- `VACCINE_CMO_RESTRUCTURING` canonical archetype 추가
- R7 Loop 8 케이스 7개를 calibration-only case record로 구조화
- production scoring과 candidate generation은 변경하지 않음

## 케이스 요약

| case | 판단 | Stage 3 처리 |
|---|---|---|
| 알테오젠 | SC royalty commercialization watch | 로열티 인식·현금 유입 전 보류 |
| 유한양행 | FDA approval to royalty watch | 처방량·J&J 매출·유한양행 로열티 전 보류 |
| SK바이오사이언스 | CMO M&A event premium | 가동률·수주잔고·마진·FCF 전 보류 |
| 셀트리온 | U.S. tariff hedge manufacturing watch | 제품 이전·가동률·마진·FCF 전 보류 |
| 삼성바이오로직스 | CDMO U.S. capacity watch | 가격 반응 약해 valuation saturation watch |
| 휴젤 | U.S. botulinum launch watch | 미국 매출·채널·ASP·반복 주문 전 보류 |
| 루닛 | medical AI validation not Green | 수가·병원 도입·반복매출·cash runway 전 보류 |

## Green Gate

R7 Stage 3-Green 필수 조건:

- approval_or_regulatory_clearance
- commercial_launch
- prescription_volume_or_hospital_adoption
- reimbursement_or_payer_access
- revenue_recognition
- royalty_or_gross_margin_confirmation
- capacity_utilization_or_channel_penetration
- cash_runway_and_dilution_risk_passed
- partner_execution_risk_passed
- price_path_after_evidence

Green 금지 패턴:

- approval_news_only
- clinical_headline_only
- paper_validation_without_revenue
- mna_without_utilization
- fda_approval_without_commercial_sales
- partner_peak_sales_without_royalty_visibility
- pre_revenue_biotech_story
- cash_burn_or_dilution_risk
- manufacturing_inspection_issue
- subgroup_performance_risk

## 4B / 4C 보정

4B-watch는 승인 직후 주가 급등, M&A 발표 당일 급등, CDMO capacity premium이 가동률보다 먼저 커지는 경우, 의료AI 검증 뉴스만으로 주가가 먼저 움직이는 경우에 붙인다.

Hard 4C는 FDA CRL, 임상 실패, 상업화 실패, 처방량 부진, 급여 실패, 로열티 미발생, 대규모 희석, cash runway 붕괴, 제조 inspection 실패, 제품 safety issue, patent/IP legal loss처럼 원문과 날짜가 명확할 때만 확정한다.

## 산출물

- `data/e2r_case_library/cases_r7_loop8_round211.jsonl`
- `data/sector_taxonomy/round211_r7_loop8_biotech_healthcare_device_price_validation_audit.json`
- `output/e2r_round211_r7_loop8_biotech_healthcare_device_price_validation/round211_r7_loop8_price_validation_summary.md`
- `output/e2r_round211_r7_loop8_biotech_healthcare_device_price_validation/round211_r7_loop8_case_matrix.csv`
- `output/e2r_round211_r7_loop8_biotech_healthcare_device_price_validation/round211_r7_loop8_score_adjustments.csv`
- `output/e2r_round211_r7_loop8_biotech_healthcare_device_price_validation/round211_r7_loop8_green_gate_review.md`
- `output/e2r_round211_r7_loop8_biotech_healthcare_device_price_validation/round211_r7_loop8_stage4b_4c_review.md`

## 검증

라운드211 전용 테스트와 전체 테스트를 실행한다.

```bash
PYTHONPATH=src python -m unittest tests.test_round211_r7_loop8_biotech_healthcare_device_price_validation -v
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
```

## 결론

라운드211은 R7에서 Stage 3를 가장 보수적으로 줘야 한다는 기준을 명시했다. 승인·임상·논문·M&A는 좋은 Stage 2 후보를 만들 수 있지만, 실제 돈이 들어오는 증거가 없으면 Green으로 올리지 않는다.
