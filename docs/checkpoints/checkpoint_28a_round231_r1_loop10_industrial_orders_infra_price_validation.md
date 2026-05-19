# Checkpoint 28A Round 231 R1 Loop 10 Industrial Infra Price Validation

## 반영 내용

- `docs/round/round_231.md`의 R1 Loop 10 라운드를 calibration-only 검증팩으로 구조화했다.
- 전력기기/변압기, 방산 수출, 해외 EPC, 사우디 가스 인프라, 조선정책/MASGA, 지정학 제재 케이스를 추가했다.
- Reuters/WSJ/MarketWatch/AP/FT류 reported anchor에서 확인된 가격, 계약, 이벤트 수익률만 저장했다.
- 원시 OHLC가 없는 항목은 `price_data_unavailable_after_deep_search` 또는 `reported_*_not_full_ohlc`로 명시했다.
- production scoring과 candidate generation은 변경하지 않았다.

## 핵심 케이스

- LS ELECTRIC: 미국 grid/data-center와 525kV 변압기 계약 증거는 강하지만, 2024-07-01 target 상향 당일 가격이 -5.4%였으므로 Stage 2 watch로 유지했다.
- Hyundai Rotem: K2 납품, 매출, OP revision, +9.3% 가격 반응이 같이 나온 R1 order-to-revenue 성공 anchor로 저장했다.
- LIG Nex1: Iraq Cheongung-II/M-SAM 수출은 Stage 2지만 1H +69% 뒤 -11% 조정이 있어 4B/crowding watch를 붙였다.
- Hanwha Aerospace: Poland missile JV는 Stage 2지만 3.6조 원 증자 shock 때문에 dilution 4B-watch를 붙였다.
- Samsung E&A / GS E&C: Fadhili EPC는 Stage 2지만 margin, progress revenue, cash collection, working capital 전에는 Green 금지로 남겼다.
- Hyundai E&C: Jafurah/main gas network는 Stage 2지만 회사별 가격 anchor와 cash recovery가 부족하다.
- HD Hyundai Heavy / Mipo: MASGA/merger record-high 이벤트는 policy event premium + 4B-watch로 처리했다.
- Hanwha Ocean: China sanctions는 4C-watch로 처리했고, 실제 revenue/contract disruption 전에는 hard 4C로 확정하지 않았다.

## Green Gate 보강

R1 Stage 3-Green은 단순히 `수주 있음`이 아니다.

예를 들어, 수주 공시만 있으면 씨앗이 있는 상태이고, Stage 3는 그 씨앗이 납품, 매출, 마진, EPS/FCF, 가격경로로 실제 확인되는 순간이다.

필수 조건:

- 계약금액 확인
- 계약기간 또는 납기 확인
- 실제 납품 또는 매출 인식 확인
- OPM/EPS/FCF revision 확인
- 수주잔고 품질 확인
- 현금흐름 또는 working capital 통과
- 지정학/financing/dilution risk 통과
- 증거 이후 가격경로 확인

금지 조건:

- 수주 headline만 있음
- 정책/MOU만 있음
- record-high policy event
- 마진 불명
- EPC cash collection 불명
- local production economics 불명
- geopolitical sanction risk 무시

## 산출물

- `data/e2r_case_library/cases_r1_loop10_round231.jsonl`
- `data/sector_taxonomy/round231_r1_loop10_industrial_orders_infra_price_validation_audit.json`
- `output/e2r_round231_r1_loop10_industrial_orders_infra_price_validation/round231_r1_loop10_price_validation_summary.md`
- `output/e2r_round231_r1_loop10_industrial_orders_infra_price_validation/round231_r1_loop10_case_matrix.csv`
- `output/e2r_round231_r1_loop10_industrial_orders_infra_price_validation/round231_r1_loop10_shadow_weights.csv`
- `output/e2r_round231_r1_loop10_industrial_orders_infra_price_validation/round231_r1_loop10_green_gate_review.md`
- `output/e2r_round231_r1_loop10_industrial_orders_infra_price_validation/round231_r1_loop10_stage4b_4c_review.md`

## 검증

- `PYTHONPATH=src python -m unittest tests/test_round231_r1_loop10_industrial_orders_infra_price_validation.py -v`
- `PYTHONPATH=src python -m e2r.cli.build_round231_r1_loop10_report`

## 다음 단계

- 원시 수정주가 OHLC를 확보하면 `reported_price_anchor_not_full_ohlc` 항목의 MFE/MAE를 정밀 backfill한다.
- R1 shadow weight는 아직 production scoring에 적용하지 않는다.
- 다음 scoring 라운드에서는 R1에서 `order_to_revenue_conversion`과 `cashflow_or_working_capital_passed`를 Green gate 핵심 축으로 shadow 비교한다.
