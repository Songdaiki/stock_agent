# Round-200 R9 Loop-7 Price-Path Validation Summary

- source_round: `docs/round/round_200.md`
- large_sector: `MOBILITY_TRANSPORT_LEISURE`
- scope: auto hybrid/value-up, tariff-localization, airline integration, safety, freight cycle, tourism policy, duty-free, and casino utilization
- case_candidate_count: 7
- required_target_count: 22
- score_adjustment_count: 23
- price_backfill_field_count: 52
- structural_success_count: 1
- success_candidate_count: 3
- cyclical_success_count: 1
- failed_rerating_count: 1
- hard_4c_case_count: 1
- stage3_case_count: 0
- stage4b_watch_or_elevated_count: 6
- needs_ohlc_backfill_count: 7
- production_scoring_changed: false
- candidate_generation_input: false
- shadow_weight_only: true
- needs_ohlc_backfill: true

## Interpretation

- R9는 hybrid/value-up처럼 구조 후보가 있지만, 해운·항공·여행은 사이클과 이벤트가 가격을 먼저 밀기 쉽다.
- 현대차는 hybrid mix, 주주환원, OPM target이 강하지만 tariff margin cut을 4C-watch로 붙인다.
- 기아 SDV/AI mobility는 paid software revenue와 unit economics 전 Stage 3가 아니다.
- 대한항공 Asiana completion은 Stage 2지만 통합 시너지, FCF, load factor, yield 전 Green 금지다.
- 제주항공 fatal accident는 operational trust hard 4C gate다.
- HMM freight rebound는 cyclical success로 보고 구조적 Green과 분리한다.
- 호텔신라/롯데관광개발은 관광객 수보다 tourist spend, drop, hold, occupancy, OPM이 필요하다.

쉬운 예: `as_of_date=2025-09-29`에 중국 무비자 정책이 시작되어도 면세 매출과 객단가가 없으면 Stage 3-Green이 아니라 Stage 1~2 watch다.
