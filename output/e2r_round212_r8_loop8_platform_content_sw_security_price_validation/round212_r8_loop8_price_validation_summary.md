# Round 212 R8 Loop 8 Platform Content Software Security Price Validation

This pack is calibration-only. Production scoring and candidate generation are unchanged.

## Summary

- source_round: docs/round/round_212.md
- large_sector: PLATFORM_CONTENT_SW_SECURITY
- cases: 7
- success_candidate: 3
- event_premium: 1
- overheat: 1
- failed_rerating: 2
- Stage 3 dated cases: 0
- 4B-watch cases: 7
- hard_4c_case_count: 0
- full_ohlc_complete: false

## Case Matrix

| case | company | type | stage2 | stage3 | 4B | 4C | alignment | note |
|---|---|---|---|---|---|---|---|---|
| r8_loop8_douzone_bizon_eqt_saas | 더존비즈온 | success_candidate | 2025-11-07 |  |  |  | unknown | EQT investment supports Stage 2, but Stage 3 waits for ARR proxy, churn, OPM, and FCF conversion. |
| r8_loop8_samsung_sds_kkr_ai_event | 삼성SDS | event_premium | 2026-04-15 |  | 2026-04-15 |  | price_moved_without_evidence | KKR/AI capital allocation is Stage 2 and 4B-watch; AI revenue conversion and FCF are required for Stage 3. |
| r8_loop8_lg_cns_ai_cloud_ipo_failed_price | LG CNS | failed_rerating | 2025-02-05 |  |  |  | evidence_good_but_price_failed | Cloud/AI sales mix was real, but IPO price action failed; recurring revenue, margin, retention, and FCF are required. |
| r8_loop8_naver_webtoon_ip_platform | NAVER/Webtoon | success_candidate | 2024-06-19 |  | 2024-06-27 |  | unknown | Webtoon MAU and IPO are Stage 2. Stage 3 requires paid content, ARPU, IP monetization, operating leverage, and FCF. |
| r8_loop8_kakao_openai_ai_partnership | 카카오 | overheat |  |  | 2025-02-04 |  | price_moved_without_evidence | OpenAI partnership is routing evidence, not Green; paid usage, ARPU, OPM, and FCF must appear first. |
| r8_loop8_krafton_inzoi_adk_ip | 크래프톤 | success_candidate | 2025-04-04 |  |  |  | unknown | First-week sales and ADK acquisition support Stage 2. Stage 3 waits for repeat bookings, retention, and IP extension revenue. |
| r8_loop8_hybe_legal_governance_watch | HYBE | failed_rerating |  |  |  | 2026-04-21 | false_positive_score | Legal/governance risk blocks Green. Warrant decline means hard 4C is not confirmed, so this remains 4C-watch. |

## Interpretation
- Douzone is a B2B SaaS Stage 2 candidate, but Stage 3 waits for ARR proxy, churn, OPM, and FCF.
- Samsung SDS is Stage 2 and 4B-watch because price moved before AI revenue conversion.
- LG CNS shows that cloud/AI evidence can still fail price validation at IPO.
- NAVER/Webtoon needs paid content, ARPU, IP monetization, operating leverage, and FCF beyond MAU and IPO valuation.
- Kakao/OpenAI is price-moved-without-evidence until paid AI usage and margin improve.
- Krafton needs retention and repeat bookings beyond inZOI first-week sales.
- HYBE remains governance/legal 4C-watch, not hard 4C, because the warrant was declined later.
