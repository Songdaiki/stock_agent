# Round 217 R13 Loop 8 Cross-Archetype Price Validation

This pack is calibration-only. Production scoring and candidate generation are unchanged.

## Summary

- source_round: docs/round/round_217.md
- large_sector: CROSS_ARCHETYPE_REDTEAM_PRICE_VALIDATION
- cases: 8
- structural_success: 2
- event_premium: 1
- overheat: 1
- hard_4c: 2
- price_moved_without_evidence: 2
- Stage 3 dated cases: 2
- 4B watch/elevated cases: 6
- price_validation_completed: partial_with_reported_price_anchors
- full_ohlc_complete: false

## Case Matrix

| case | company | type | stage3 | 4B | 4C | alignment | note |
|---|---|---|---|---|---|---|---|
| r13_loop8_sk_hynix_hbm_stage3_4b | SK하이닉스 | structural_success | 2024-06-25 | 2026-05-14 |  | aligned | HBM와 OP revision이 가격경로와 맞은 Stage 3 성공 benchmark지만 2026년 5월 기준 신규 Green이 아니라 4B-watch다. |
| r13_loop8_hyundai_rotem_k2_delivery_aligned | 현대로템 | structural_success | 2024-04-09 | 2025-08-01 |  | aligned | 현대로템은 방산 수주 headline보다 납품·매출·OP revision이 Stage 3를 만든다는 기준점이다. |
| r13_loop8_hanwha_aero_dilution_4b_not_4c | 한화에어로스페이스 | 4b_watch |  | 2025-03-21 |  | aligned | 대시세 후 증자는 4B-watch/elevated다. 수주·EPS thesis가 살아 있으면 자동 hard 4C가 아니다. |
| r13_loop8_kogas_resource_price_only | 한국가스공사 | event_premium |  | 2024-06-03 |  | price_moved_without_evidence | 정책·자원발견 이벤트는 경제성·상업성 전까지 Stage 1/4B-watch이며 Green 금지다. |
| r13_loop8_lges_lnf_contract_quality_4c | LG에너지솔루션 / L&F | 4c_thesis_break |  |  | 2025-12-18 | aligned | 계약 headline은 충분조건이 아니다. 계약 취소와 가치 붕괴는 hard 4C다. |
| r13_loop8_jeju_air_operational_trust_hard_4c | 제주항공 | 4c_thesis_break |  |  | 2024-12-30 | aligned | 여행수요가 좋아도 fatal safety accident는 operational trust hard 4C다. |
| r13_loop8_stablecoin_theme_price_only | Kakao Pay / stablecoin basket | overheat |  | 2025-06-01 |  | price_moved_without_evidence | 스테이블코인 정책 기대는 발행권·reserve income·수수료·규제자본 전까지 Stage 3 금지다. |
| r13_loop8_korea_zinc_strategic_governance_watch | 고려아연 | success_candidate |  | 2025-12-24 |  | unknown | 전략광물 프로젝트는 Stage 2 후보지만 offtake, FCF, dilution, governance가 풀리기 전 Stage 3는 보류한다. |

## Interpretation
- SK하이닉스와 현대로템은 Stage 3가 실제 대형 MFE나 강한 price reaction을 만들 수 있음을 보여준다.
- 한화에어로스페이스 증자 shock은 4B-watch/elevated이지 자동 hard 4C가 아니다.
- 한국가스공사와 stablecoin basket은 가격이 증거보다 먼저 간 event premium이다.
- LGES/L&F와 제주항공은 계약품질·운영신뢰 hard 4C 기준점이다.
- 고려아연은 전략자원 Stage 2 후보지만 governance/dilution이 풀리기 전 Stage 3 보류다.
