# Checkpoint 28A Round 214 R10 Loop 8 Construction Real Estate Materials Price Validation

## 목적

라운드214는 R10 건설·부동산·건자재 가격경로 검증 팩이다.

핵심 원칙은 단순하다. `대형 EPC 수주`, `PF 지원책`, `데이터센터 투자`, `부동산 회복 테마`는 Stage 1~2 후보를 만들 수 있다. 하지만 Stage 3-Green은 마진, 공정률, working capital 이후 현금흐름, tenant 계약, NOI/AFFO, 전력·용수·인허가, 안전·품질 신뢰가 확인된 뒤에만 가능하다.

예를 들면 삼성E&A의 $6B EPC 수주는 강한 Stage 2다. 그러나 저마진 수주이거나 현금 회수가 늦어지면 Green이 아니라 4C-watch가 된다.

## 반영 내용

- `src/e2r/sector/round214_r10_loop8_construction_real_estate_materials_price_validation.py` 추가
- `src/e2r/cli/build_round214_r10_loop8_report.py` 추가
- `tests/test_round214_r10_loop8_construction_real_estate_materials_price_validation.py` 추가
- R10 Loop 8 케이스 7개를 calibration-only case record로 구조화
- Reuters / WSJ / 공개 사고기록의 reported anchor로 계산 가능한 값만 반영
- full OHLC가 확보되지 않은 항목은 `price_data_unavailable_after_deep_search`로 명시
- production scoring과 candidate generation은 변경하지 않음

## 케이스 요약

| case | 판단 | Stage 3 처리 |
|---|---|---|
| 삼성E&A | Fadhili $6B EPC Stage 2 + event 4B-watch | EPC margin·progress revenue·cash collection 전 보류 |
| 현대건설 | Jafurah / Saudi gas network Stage 2 | 마진·working capital·현금회수 전 보류 |
| 대우건설 | Grand Faw handover Stage 2 | 수익 인식·현금 회수·추가 수주 전 보류 |
| 태영건설/PF stress | PF hard 4C | 지원책은 relief이지 Green 증거가 아님 |
| HDC현대산업개발 | apartment quality/safety hard 4C | 안전·품질 신뢰 회복 전 Green 금지 |
| POSCO E&C / DL Construction | operational trust 4C-watch | 반복 사망사고·현장중단·면허/벌금 리스크 감시 |
| SK/AWS·OpenAI 데이터센터 | real asset 후보 + event premium | tenant·NOI/AFFO·power/water·capex per share 전 보류 |

## Green Gate

R10 Stage 3-Green 필수 조건:

- company_level_contract_or_tenant
- margin_or_noi_affo_visibility
- cash_flow_after_working_capital
- pf_funding_cost_passed
- project_progress_or_cost_control
- tenant_occupancy_utilization_confirmed
- capex_per_share_or_dilution_passed
- safety_quality_trust_passed
- price_path_after_evidence

Green 금지 패턴:

- contract_headline_only
- pf_relief_policy_only
- real_estate_rebound_theme_only
- data_center_theme_without_tenant
- asset_headline_without_noi_affo
- reit_dividend_headline_only
- safety_incident
- working_capital_deterioration
- low_margin_epc_order
- tenant_absent
- power_water_permitting_failure

## 4B / 4C 보정

4B-watch는 대형 EPC 수주 발표 직후 급등, PF 지원책으로 건설주 동반 급등, 데이터센터 테마 basket rally, 금리 인하 기대만으로 REIT 급등, 재건·재난복구 테마가 가격에 먼저 반영되는 경우에 붙인다.

Hard 4C는 PF workout, 채무재조정, PF 연체율 급등, 미분양/분양 실패, 공사비 원가율 급등, working capital 악화, 수주 취소, 발주처 지급 지연, 저마진 EPC 손실, 아파트 붕괴, 반복 사망사고, 현장중단, 면허 취소 리스크, tenant 부재, 전력·용수·인허가 실패, AFFO integrity 훼손, capex dilution처럼 논리 훼손이 명확할 때만 확정한다.

## 산출물

- `data/e2r_case_library/cases_r10_loop8_round214.jsonl`
- `data/sector_taxonomy/round214_r10_loop8_construction_real_estate_materials_price_validation_audit.json`
- `output/e2r_round214_r10_loop8_construction_real_estate_materials_price_validation/round214_r10_loop8_price_validation_summary.md`
- `output/e2r_round214_r10_loop8_construction_real_estate_materials_price_validation/round214_r10_loop8_case_matrix.csv`
- `output/e2r_round214_r10_loop8_construction_real_estate_materials_price_validation/round214_r10_loop8_score_adjustments.csv`
- `output/e2r_round214_r10_loop8_construction_real_estate_materials_price_validation/round214_r10_loop8_green_gate_review.md`
- `output/e2r_round214_r10_loop8_construction_real_estate_materials_price_validation/round214_r10_loop8_stage4b_4c_review.md`

## 검증

라운드214 전용 테스트와 전체 테스트를 실행한다.

```bash
PYTHONPATH=src python -m unittest tests.test_round214_r10_loop8_construction_real_estate_materials_price_validation -v
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
```

## 결론

라운드214는 R10에서 Stage 3를 보수적으로 둬야 하는 이유를 명확히 했다. 건설·부동산·데이터센터는 headline보다 현금흐름과 신뢰가 먼저다. PF와 안전사고는 R10의 가장 강한 4C hard gate로 유지한다.
