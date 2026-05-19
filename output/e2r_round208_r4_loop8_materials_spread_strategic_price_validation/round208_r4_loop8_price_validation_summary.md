# Round-208 R4 Loop-8 Price-Path Validation Summary

- source_round: `docs/round/round_208.md`
- large_sector: `MATERIALS_SPREAD_STRATEGIC`
- scope: Korea Zinc event premium, petrochemical restructuring, refining cycle, lithium resource security, non-China polysilicon, and copper-defense event premium
- case_candidate_count: 7
- required_target_count: 13
- score_adjustment_count: 19
- price_validation_field_count: 17
- success_candidate_count: 2
- cyclical_success_count: 1
- event_premium_count: 2
- failed_or_4c_count: 2
- hard_4c_case_count: 2
- stage3_case_count: 0
- stage4b_watch_count: 6
- reported_price_anchor_count: 4
- production_scoring_changed: false
- candidate_generation_input: false
- shadow_weight_only: true
- price_validation_completed: partial_with_reported_price_anchors
- full_ohlc_complete: false

## Interpretation

- 고려아연은 전략광물 후보지만 2024년 공개매수/자사주/신주발행 구간은 event premium과 4B/4C-watch다.
- 롯데케미칼과 LG화학은 구조조정 기대보다 실제 spread, OPM, FCF 회복 전까지 Red/Watch가 우선이다.
- SK이노베이션의 정제마진 반등은 cyclical Stage 2이며, multi-quarter margin floor 전까지 Green은 보류한다.
- POSCO홀딩스 리튬 JV는 resource-security Stage 2지만 lithium cycle과 downstream margin을 확인해야 한다.
- OCI SpaceX 보도와 풍산 M&A 보도는 미확정 media report라서 Stage 3 근거가 아니다.

쉬운 예: `as_of_date=2024-09-13`에 고려아연이 공개매수로 급등해도, 그 급등은 경영권 프리미엄이다. offtake와 FCF가 확인된 전략자원 Stage 3와는 분리해야 한다.
