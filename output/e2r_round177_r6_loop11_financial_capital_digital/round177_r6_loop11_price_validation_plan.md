# Round-177 R6 Loop-11 Price Validation Plan

## Method

1. Assign Stage 1/2/3/4B/4C dates from dated source evidence only.
2. Backfill KRX daily bars for `price_at_stage1` through `price_at_stage4c`.
3. Calculate 20D/60D/120D/252D returns and MFE/MAE after Stage 2.
4. Compare price speed against ROE, net profit, CET1, K-ICS, credit cost, PF exposure, actual return, security, and regulation.
5. Separate bank/insurance Green-capable cases from brokerage cycle, fintech option, stablecoin policy, security 4C, and disclosure caps.

## Priority Case Checks

| case_id | target | stage marker | check |
| --- | --- | --- | --- |
| `kb_financial_valueup_stage3_candidate` | `BANK_HOLDING_VALUEUP_CAPITAL_RETURN_KOREA` | undated | needs_krx_price_cet1_credit_cost_return_backfill |
| `shinhan_overseas_profit_valueup_candidate` | `BANK_ROE_PBR_RERATING_KOREA` | undated | needs_price_roe_cet1_return_backfill |
| `woori_financial_nonbank_capital_buffer_gate_case` | `BANK_HOLDING_VALUEUP_CAPITAL_RETURN_KOREA` | undated | needs_cet1_mna_return_price_backfill |
| `jb_financial_regional_high_roe_valueup_case` | `REGIONAL_BANK_HIGH_ROE_VALUEUP` | undated | needs_price_roe_credit_liquidity_backfill |
| `korea_insurance_capital_release_valueup_case` | `INSURANCE_CAPITAL_RELEASE_VALUEUP_KOREA` | undated | needs_kics_csm_loss_ratio_price_backfill |
| `kakaobank_profitability_valuation_cap_case` | `INTERNET_BANK_PROFITABILITY` | undated | needs_profit_credit_cost_valuation_price_backfill |
| `naver_dunamu_equity_option_security_4c_watch_case` | `DIGITAL_ASSET_EXCHANGE_EQUITY_OPTION` | 2025-11-27 | needs_intraday_and_krx_path_security_resolution_backfill |
| `toss_superapp_ipo_stablecoin_related_stock_cap_case` | `FINTECH_SUPERAPP_IPO_OPTION_KOREA` | 2025-09-09 | not_price_applicable_related_basket |
| `seoul_guarantee_ipo_ransomware_security_case` | `GUARANTEE_INSURANCE_IPO_SECURITY_RISK` | undated | needs_listing_price_and_security_remediation_backfill |
| `securities_brokerage_market_beta_cycle_case` | `SECURITIES_BROKERAGE_MARKET_BETA` | 2026-05-06 | needs_trading_value_pf_ib_price_backfill |
| `financial_valueup_crowded_4b_watch_case` | `VALUE_UP_CROWDED_4B_WATCH` | 2026-05-06 | needs_basket_relative_strength_pbr_band_backfill |
| `bank_credit_cost_pf_overlay_case` | `BANK_CREDIT_COST_PF_OVERLAY` | undated | not_price_applicable_overlay |
| `financial_disclosure_confidence_cap_case` | `DISCLOSURE_CONFIDENCE_CAP` | undated | not_price_applicable_overlay |

## Alignment Labels

- `valueup_leader_requires_capital_quality`: leader-frame rerating needs CET1 and credit-cost proof.
- `nonbank_expansion_capital_gate`: M&A expansion is capped before capital-buffer proof.
- `digital_asset_equity_option_security_gate`: exchange equity option is blocked by security events.
- `brokerage_market_beta_not_green`: trading-value cycle is not structural Green by itself.
- `valueup_crowding_4b_watch`: broad financial rally is cooled when price outruns execution.
