# Round-203 R12 Loop-7 Price-Path Validation Summary

- source_round: `docs/round/round_203.md`
- large_sector: `EDUCATION_LIFE_AGRI_MISC`
- scope: smart farm, agri machinery, education policy, rental recurring service, poultry disease event, regulated consumer, and edtech policy friction
- case_candidate_count: 7
- required_target_count: 15
- score_adjustment_count: 21
- price_backfill_field_count: 54
- success_candidate_count: 3
- event_premium_count: 3
- watch_case_count: 1
- hard_4c_case_count: 0
- stage3_case_count: 0
- stage4b_watch_or_elevated_count: 7
- needs_ohlc_backfill_count: 7
- production_scoring_changed: false
- candidate_generation_input: false
- shadow_weight_only: true
- needs_ohlc_backfill: true
- r12_default_stage3_bias: conservative_except_recurring_service

## Interpretation

- R12는 구조 후보가 있지만 대부분 Stage 1~2 또는 Event/Watch에 머문다.
- 코웨이는 recurring-service 후보지만 계정·churn·ARPU·FCF 전 Stage 3 확정이 아니다.
- 대동/TYM은 농기계 수출·자율주행 테마만으로 Green을 만들지 않는다.
- 메가스터디교육은 의대정원 정책보다 실제 수강생·repeat course·OPM이 필요하다.
- 교실 디지털기기 규제는 교육/에듀테크에 양날의 policy overlay다.
- 조류독감 poultry basket은 단기 MFE 가능성이 있지만 수입제한 완화가 event fade다.
- KT&G는 현금흐름 후보지만 volume decline, HNB 경쟁, 규제 리스크를 같이 본다.
- 스마트팜은 상업 설치·수주·unit economics·반복서비스 전 Green 금지다.

쉬운 예: `as_of_date=2025-05-19`에 조류독감 수입제한 뉴스로 poultry basket이 급등해도, 2025-06-23 제한 완화가 나오면 구조적 Stage 3가 아니라 event fade로 봐야 한다.
