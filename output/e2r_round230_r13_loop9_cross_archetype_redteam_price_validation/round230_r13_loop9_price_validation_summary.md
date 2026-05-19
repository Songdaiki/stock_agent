# Round 230 R13 Loop 9 Cross-Archetype RedTeam Price Validation

This pack is calibration-only. Production scoring and candidate generation are unchanged.

## Summary

- source_round: docs/round/round_230.md
- large_sector: CROSS_ARCHETYPE_REDTEAM_PRICE_VALIDATION
- cases: 8
- structural_success: 2
- success_candidate: 1
- failed_rerating: 1
- overheat: 1
- hard_4c_case_count: 2
- Stage 3 dated cases: 2
- 4B-watch cases: 4
- price_moved_without_evidence: 2
- deep_sub_archetype_count: 8
- shadow_weight_row_count: 8
- r13_default_stage3_bias: redteam_first_after_price_validation
- full_ohlc_complete: false

## Case Matrix

| case | company | source | type | stage3 | 4B | 4C | round alignment | note |
|---|---|---|---|---|---|---|---|---|
| r13_loop9_sk_hynix_hbm_stage3_4b | SK하이닉스 | R2 | structural_success | 2024-06-25 | 2026-05-04 |  | aligned | Stage 3 성공 benchmark다. 다만 2026년 현재는 신규 Green이 아니라 4B-watch/crowding watch다. |
| r13_loop9_apr_medicube_structural_4b | APR / Medicube | R5 | structural_success | 2025-10-01 | 2025-07-08 |  | aligned | Viral이 실제 해외 매출로 내려온 구조 후보지만 매출 집중도와 valuation 때문에 4B-watch가 필요하다. |
| r13_loop9_samsung_sds_kkr_ai_event_4b | 삼성SDS | R8 | success_candidate |  | 2026-04-15 |  | event_premium_success_candidate | 좋은 Stage 2 후보지만 AI revenue conversion 전 +20.8%는 Green이 아니라 4B-watch다. |
| r13_loop9_hyundai_steel_policy_capex_failure | 현대제철 | R4/R11 | failed_rerating |  |  | 2025-04-22 | false_positive_score_prevention | 정책·관세 대응 CAPEX는 funding·margin·FCF가 없으면 Green이 아니라 RedTeam이다. |
| r13_loop9_lges_lnf_contract_quality_hard_4c | LGES / L&F | R3 | 4c_thesis_break |  |  | 2025-12-17 | thesis_break | R3 Green gate는 고객명이 아니라 actual call-off, take-or-pay, volume, OPM, FCF다. |
| r13_loop9_jeju_air_operational_safety_hard_4c | 제주항공 | R9 | 4c_thesis_break |  |  | 2024-12-30 | thesis_break | 여행수요가 좋아도 fatal accident가 나오면 Green은 즉시 차단한다. |
| r13_loop9_skt_security_privacy_4c_watch | SK텔레콤 | R8 | 4c_thesis_break |  |  | 2025-04-28 | thesis_break_watch | 보안사고는 단순 one-day issue가 아니라 매출전망·보상비용·신뢰비용으로 이어지는 4C gate다. |
| r13_loop9_policy_resource_stablecoin_price_only | Korea Gas / stablecoin policy basket | R6/R11 | overheat |  | 2024-06-03 |  | price_moved_without_evidence | 정책·자원·디지털자산 이벤트는 실제 계약·경제성·규제수익 전에는 Green 금지다. |

## Interpretation
- SK Hynix and APR/Medicube are aligned structural-success benchmarks, but both need 4B-watch after major rerating.
- Samsung SDS is Stage 2 plus 4B-watch; CB and AI capital allocation are not recurring AI revenue.
- Hyundai Steel prevents false Green from policy-induced CAPEX without funding or margin clarity.
- LGES/L&F and Jeju Air are hard 4C anchors.
- SK Telecom is strong security/privacy 4C-watch because breach cost and revenue forecast changed.
- Korea Gas and stablecoin basket are price_moved_without_evidence before commerciality or licensed revenue.
