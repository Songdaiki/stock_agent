# Round 223 R6 Loop 9 Financial Capital Digital Price Validation

This pack is calibration-only. Production scoring and candidate generation are unchanged.

## Summary

- source_round: docs/round/round_223.md
- analyst_round_id: round_151
- large_sector: FINANCIAL_CAPITAL_DIGITAL
- cases: 9
- success_candidate: 5
- cyclical_success: 1
- event_premium: 1
- overheat: 1
- 4c_thesis_break: 1
- Stage 3 dated cases: 0
- 4B-watch cases: 8
- 4C-watch cases: 2
- full_ohlc_complete: false

## Case Matrix

| case | company | type | stage2 | stage3 | 4B | 4C-watch | alignment | note |
|---|---|---|---|---|---|---|---|---|
| r6_loop9_kb_financial_bank_valueup | KB금융 | success_candidate | 2025-01-01 |  |  |  | unknown | Value-up Stage 2 candidate; Stage 3 requires ROE/CET1/credit cost and repeated shareholder return execution. |
| r6_loop9_securities_financial_basket_capital_market_boom | 증권주/금융주 basket | cyclical_success | 2026-05-06 |  | 2026-05-06 |  | aligned | Securities rally is Stage 2/cyclical; brokerage/IB revenue, ROE and risk controls required before Green. |
| r6_loop9_sk_square_nav_discount_valueup | SK스퀘어 | success_candidate | 2024-11-21 |  | 2026-05-01 |  | unknown | Actual cancellation supports Stage 2; repeated cancellation and discount narrowing required for Stage 3. |
| r6_loop9_samsung_life_nav_capital_release | 삼성생명 | success_candidate | 2026-03-19 |  |  |  | unknown | Hidden NAV and capital release are Stage 2; use of proceeds, K-ICS/CSM and shareholder return required for Stage 3. |
| r6_loop9_hana_dunamu_equity_option | 하나금융/하나은행 | success_candidate | 2026-05-14 |  |  |  | unknown | Dunamu stake is Stage 2; regulated revenue, equity-method earnings, capital impact and exchange trust required for Stage 3. |
| r6_loop9_naver_dunamu_platform_merger_trust_watch | NAVER / NAVER Financial / Dunamu | event_premium | 2025-11-27 |  | 2025-11-27 | 2025-11-27 | price_moved_without_evidence | Strong Stage 2 digital-asset merger, but abnormal withdrawal creates exchange-trust 4C-watch. |
| r6_loop9_kbank_internet_bank_ipo_watch | K Bank | success_candidate | 2024-09-10 |  |  |  | unknown | IPO profitability Stage 2 candidate; listed price path, ROE/NIM/credit cost required before Green. |
| r6_loop9_kakao_kakaobank_legal_governance_watch | Kakao / KakaoBank | 4c_thesis_break |  |  |  | 2024-07-23 | evidence_good_but_price_failed | Major shareholder legal risk blocks KakaoBank Green until ownership-risk and profitability metrics clear. |
| r6_loop9_stablecoin_policy_theme_overheat | Kakao Pay / stablecoin basket | overheat |  |  | 2025-06-01 |  | price_moved_without_evidence | Stablecoin theme rallied before licensed issuer, reserve income, fee revenue or regulatory capital clarity. |

## Interpretation
- KB, SK Square, Samsung Life, Hana, and K Bank are Stage 2 candidates until capital execution and price-path proof improve.
- Securities basket strength is cyclical_success; company-level brokerage, IB revenue, ROE, and risk controls must confirm.
- NAVER/Dunamu is event-premium Stage 2 with exchange-trust 4C-watch.
- Stablecoin policy basket rallies are price_moved_without_evidence until licensing, reserve income, fee revenue, and capital rules exist.
- Kakao/KakaoBank shows major-shareholder legal risk can block Green before internet-bank growth scoring matters.
