# Checkpoint 28A Round208 R4 Loop8 Materials Spread Strategic Price Validation

## 목적

`docs/round/round_208.md`의 R4 Loop 8 내용을 별도 가격경로 검증 팩으로 반영했다.

이번 라운드의 핵심은 **원자재 가격, 경영권 이벤트, 구조조정 기대, 미확정 보도**를 구조적 Stage 3와 분리하는 것이다. R4에서 진짜 Stage 3는 `제품 스프레드 -> cost curve -> 공급규율/offtake -> FCF`가 잠겼을 때다.

쉬운 예:

`as_of_date=2024-09-13`에 고려아연이 공개매수로 급등해도, 그 급등은 경영권 프리미엄이다. 같은 고려아연이라도 미국 critical minerals 프로젝트는 offtake, FCF, capex, dilution 확인 전까지 Stage 2 watch다.

## 추가 파일

- `src/e2r/sector/round208_r4_loop8_materials_spread_strategic_price_validation.py`
- `src/e2r/cli/build_round208_r4_loop8_report.py`
- `tests/test_round208_r4_loop8_materials_spread_strategic_price_validation.py`
- `data/e2r_case_library/cases_r4_loop8_round208.jsonl`
- `data/sector_taxonomy/round208_r4_loop8_materials_spread_strategic_price_validation_audit.json`
- `output/e2r_round208_r4_loop8_materials_spread_strategic_price_validation/`

## 케이스 요약

| case | 판단 | 가격/재무 anchor |
| --- | --- | --- |
| 고려아연 | event premium + strategic Stage 2 watch | 556,000원 -> 877,000원 +57.7%, 신주발행 이벤트 -29.9%, 미국 smelter 이벤트 +27% |
| 롯데케미칼 | petrochemical 4C + restructuring watch | 2024 영업손실 8,950억 원, 손실 +157%, Daesan NCC 3년 중단 |
| LG화학 | failed rerating / petrochemical 4C watch | OP -63.75%, petrochem Q4 loss 990억 원, 지분매각 이벤트 -2.9% |
| SK이노베이션 | refining cyclical success | 2025 Q1 loss, 2026 OP 2.2조 원, estimate beat +57.1% |
| POSCO홀딩스 | lithium resource security Stage 2 watch | MinRes +10.8%, spodumene peak-to-low -89.8%, rebound +44.3% |
| OCI홀딩스 | non-China polysilicon Stage 2 + event premium | $1.2B U.S. expansion, 10GW by 2027, SpaceX report unconfirmed |
| 풍산 | copper/defense event premium | 1.5조 원 방산부문 인수 보도, 결정 없음 |

## Green Gate 보정 방향

올릴 축:

- `actual_product_spread`
- `fcf_after_working_capital`
- `supply_discipline_confirmed`
- `capacity_shutdown_confirmed`
- `price_floor_or_offtake`
- `cost_curve_advantage`
- `strategic_customer_or_government_offtake`
- `inventory_normalization`
- `capital_return_from_cashflow`

내릴 축:

- `commodity_price_up_only`
- `restructuring_plan_without_margin`
- `policy_support_without_fcf`
- `tender_offer_or_governance_premium`
- `unconfirmed_media_report`
- `capacity_cut_expectation_only`
- `lithium_price_event`
- `refining_margin_geopolitical_shock`
- `customer_or_contract_unconfirmed`
- `capex_heavy_project_pre_revenue`

## 4B / 4C 기준

4B-watch:

- 원자재 가격 급등 후 관련주 동반 상승
- 구조조정 기대만으로 multiple 확장
- 공개매수/자사주/경영권 분쟁으로 주가 급등
- 리튬/폴리실리콘 supply discipline 뉴스로 소재주 급등
- 정제마진 공급차질성 spike
- 미확정 고객/M&A 보도에 급등

Hard 4C:

- spread reversal
- 중국/중동 공급과잉
- inventory build
- NCC 가동중단 또는 대규모 영업손실
- 공개매수/매각 이벤트 불발
- 대규모 신주발행 / dilution
- commodity price 재하락
- project capex overrun
- offtake 부재
- FCF 악화

## 안전장치

- `production_scoring_changed = false`
- `candidate_generation_input = false`
- `shadow_weight_only = true`
- `price_validation_completed = partial_with_reported_price_anchors`
- `full_ohlc_complete = false`

이번 라운드는 production scoring을 바꾸지 않는다. 케이스는 calibration/evaluation 자료이며, 후보 생성 입력으로 쓰면 안 된다.
