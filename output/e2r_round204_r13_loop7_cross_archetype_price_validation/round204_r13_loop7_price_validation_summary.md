# Round-204 R13 Loop-7 Price-Path Validation Summary

- source_round: `docs/round/round_204.md`
- large_sector: `CROSS_ARCHETYPE_OVERLAY`
- scope: Stage 3 success, 4B timing, price-only rally, event premium, hard 4C, contract quality, and operational trust
- case_candidate_count: 8
- required_target_count: 16
- score_adjustment_count: 16
- price_validation_field_count: 27
- structural_success_count: 2
- event_premium_count: 1
- hard_4c_case_count: 3
- stage3_case_count: 0
- stage4b_watch_or_elevated_count: 5
- reported_price_anchor_count: 8
- production_scoring_changed: false
- candidate_generation_input: false
- shadow_weight_only: true
- price_validation_completed: partial_with_reported_price_anchors
- full_ohlc_complete: false

## Interpretation

- SK하이닉스와 한화에어로스페이스는 Stage 3가 대형 MFE를 잡을 수 있음을 보여주는 aligned success benchmark다.
- SK하이닉스는 2026-05-14 기준 신규 Green보다 4B-watch/elevated로 보는 게 맞다.
- 한화에어로스페이스 증자 충격은 4B-watch/elevated이지 backlog/EPS thesis가 살아 있으면 hard 4C가 아니다.
- 한국가스공사와 삼성SDS는 가격이 증거보다 먼저 간 이벤트라 Green을 막아야 한다.
- 제주항공 fatal crash는 operational trust hard 4C다.
- LGES와 L&F는 계약 취소와 계약가치 붕괴 hard 4C 기준점이다.

쉬운 예: `as_of_date=2026-04-15`에 삼성SDS가 KKR CB와 AI 인프라 기대감으로 장중 급등해도, AI 매출·마진·반복 cloud revenue가 없으면 Stage 3-Green이 아니라 Stage 2/4B-watch다.
