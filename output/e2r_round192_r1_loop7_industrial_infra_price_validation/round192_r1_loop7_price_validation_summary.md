# Round-192 R1 Loop-7 Price-Path Validation Summary

- source_round: `docs/round/round_192.md`
- large_sector: `INDUSTRIAL_ORDERS_INFRA`
- scope: Korean defense, shipbuilding, MRO, and price-only rally validation
- case_candidate_count: 7
- required_target_count: 11
- score_adjustment_count: 13
- price_backfill_field_count: 46
- structural_success_count: 2
- success_candidate_count: 4
- event_premium_count: 1
- stage4b_watch_or_elevated_count: 4
- hard_4c_confirmed_count: 0
- needs_ohlc_backfill_count: 7
- production_scoring_changed: false
- candidate_generation_input: false
- shadow_weight_only: true
- needs_ohlc_backfill: true

## Interpretation

- R1에서 강한 증거는 수주 뉴스가 아니라 수주가 납품, 마진, OP/EPS, FCF로 넘어가는 순간이다.
- 현대로템과 한화에어로스페이스는 구조적 성공 후보지만, 정확한 MFE/MAE는 공식 OHLC backfill이 필요하다.
- LIG넥스원, 삼성중공업, KAI는 계약이 강해도 매출 인식, 마진, EPS revision 전에는 Stage 2/Watch에 머문다.
- HD현대마린솔루션 IPO 첫날 급등은 Stage 3가 아니라 event premium / price-only rally 반례다.
- 한화오션 제재 이벤트는 sanction watch다. 제재 중단이 있었으므로 hard 4C로 확정하지 않는다.

쉬운 예: `as_of_date=2024-07-01`에 삼성중공업 1.438조 원 계약을 봤다면 Stage 2 근거는 될 수 있다. 하지만 그날 마진, 납기, EPS 상향이 없으면 Stage 3-Green으로 올리면 안 된다.
