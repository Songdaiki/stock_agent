# Checkpoint 28A Round 209 R5 Loop 8 Consumer Retail Brand Price Validation

## 반영 범위

`docs/round/round_209.md`의 R5 소비재·유통·브랜드 가격경로 검증 내용을 case-library 보강팩으로 반영했다.

- 대섹터: `CONSUMER_RETAIL_BRAND`
- 원천 라운드: `docs/round/round_209.md`
- production scoring 변경: `false`
- candidate generation input: `false`
- shadow weight only: `true`
- price validation: `partial_with_reported_price_anchors`
- full OHLC complete: `false`

## 핵심 해석

R5의 Stage 3 후보는 “K푸드·K뷰티가 핫하다”가 아니라 다음 묶음이 같이 확인되는 경우다.

- 반복구매 또는 반복수요
- 해외 채널과 sell-through
- ASP 또는 product mix 개선
- OPM 개선
- 재고와 매출채권 품질
- 관세, recall, regulation 통과
- evidence 이후 가격경로 확인

쉬운 예시:

- `Costco/Ulta/Target 입점 논의`는 Stage 2 attention이다.
- `입점 후 실제 판매, 반복 발주, OPM 개선, 재고 안정`이 보이면 Stage 3 후보가 될 수 있다.
- `IPO 후 한 달 2배`는 구조 증거가 아니라 4B-watch다.

## 추가 케이스

| case | company | classification | interpretation |
|---|---|---|---|
| `r5_loop8_samyang_buldak_export_aligned` | 삼양식품 | structural_success | Buldak 수출, ASP, OP revision, capacity support가 같이 확인된 R5 Stage 3 후보 |
| `r5_loop8_nongshim_shin_global_staple` | 농심 | success_candidate | global staple 구조는 강하지만 OPM/EPS revision과 sell-through 확인 전 Stage 2 watch |
| `r5_loop8_apr_medicube_device_4b` | APR | structural_success + 4B-watch | 해외 매출 mix와 미국 매출 mix가 강하지만 4배 이상 상승으로 4B-watch 필요 |
| `r5_loop8_dalba_global_ipo_overheat` | d'Alba Global | overheat | U.S. retail talks와 IPO 급등은 Green 전 sell-through 검증 필요 |
| `r5_loop8_cosmax_kolmar_odm_leverage` | 코스맥스/한국콜마 | success_candidate | ODM backbone 구조는 Stage 2 후보, 고객 다변화·OPM·재고/채권 품질 필요 |
| `r5_loop8_amorepacific_transition_watch` | 아모레퍼시픽 | failed_rerating | K-beauty macro와 회사별 실적을 분리해야 하는 transition/watch 사례 |
| `r5_loop8_fnf_taylormade_event` | F&F | event_premium | TaylorMade M&A optionality는 본업 EPS/FCF 전 Stage 3 근거가 아님 |

## 산출물

- `src/e2r/sector/round209_r5_loop8_consumer_retail_brand_price_validation.py`
- `src/e2r/cli/build_round209_r5_loop8_report.py`
- `tests/test_round209_r5_loop8_consumer_retail_brand_price_validation.py`
- `data/e2r_case_library/cases_r5_loop8_round209.jsonl`
- `data/sector_taxonomy/round209_r5_loop8_consumer_retail_brand_price_validation_audit.json`
- `output/e2r_round209_r5_loop8_consumer_retail_brand_price_validation/`

## Green Gate

필수:

- repeat purchase
- overseas sales mix
- channel sell-through
- ASP 또는 product mix
- OPM
- inventory/receivables quality
- tariff/recall/regulation 통과
- price path after evidence

금지:

- viral product only
- brand heat only
- retail talks without sell-through
- IPO first-month rally
- influencer endorsement only
- M&A optionality without EPS
- China decline without offset

## 남은 작업

원시 수정주가 OHLC가 확보되지 않은 항목은 `price_data_unavailable_after_deep_search` 또는 `reported_*_anchor_not_full_ohlc`로 남겼다. 다음 단계에서 KRX/Naver/공식 가격 cache로 Stage 3 이후 MFE/MAE를 채워야 한다.
