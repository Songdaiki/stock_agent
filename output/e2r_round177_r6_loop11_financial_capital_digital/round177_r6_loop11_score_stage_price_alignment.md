# Round-177 R6 Loop-11 Score -> Stage -> Price Alignment

## Base Score Weights

| component | points | direction | reason |
| --- | ---: | --- | --- |
| `roe_eps_fcf_durability` | 22 | raise_profit_quality | Low PBR is only Stage 1; ROE, net profit, EPS, and FCF durability drive Stage 2/3. |
| `capital_return_execution` | 18 | execution_before_policy | Buyback, cancellation, dividend, payout ratio, and total shareholder return must be executed, not merely expected. |
| `capital_ratio_credit_cost_stability` | 18 | hard_quality_gate | CET1, K-ICS, PF exposure, reserves, and credit cost can block financial rerating. |
| `regulatory_revenue_model_visibility` | 14 | digital_finance_gate | Digital asset, stablecoin, IPO, exchange, and fintech options need approved regulation and revenue economics. |
| `early_price_path_validation` | 10 | loop11_axis | 60D/120D MFE and relative strength separate early Stage 3 from late value-up chasing. |
| `governance_disclosure_confidence` | 10 | raise_detail_requirement | Financials need precise disclosure on cancellation, dividend, capital ratio, stake value, and security incidents. |
| `valuation_room_4b_runway` | 8 | cool_crowded_valueup | PBR band expansion and financial-basket crowding reduce Stage 3 runway. |

## Stage Caps

| stage band | max score | evidence | examples | Green policy |
| --- | --- | --- | --- | --- |
| `Stage 1` | 45 | low_pbr, valueup_policy, buyback_cancel_expectation, stablecoin_theme, toss_ipo, dunamu_stake_news | kb_financial_valueup_stage3_candidate, toss_superapp_ipo_stablecoin_related_stock_cap_case | Low PBR, policy, IPO, or stablecoin names route research only. They do not create Stage 3. |
| `Stage 2` | 70 | actual_buyback_cancel_or_dividend, roe_cet1_kics_stable, net_profit_growth, stake_acquisition, ipo_filing, regulatory_bill, users_or_transaction_volume | woori_financial_nonbank_capital_buffer_gate_case, naver_dunamu_equity_option_security_4c_watch_case | Stage 2 can be strong, but Green waits for repeat return, capital ratio, credit cost, revenue model, and price path. |
| `Stage 3` | requires_5_of_8 | roe_or_net_profit_yoy_improves, cet1_or_kics_stable_after_return, actual_cancel_or_dividend_expansion, credit_cost_pf_reserve_stable, pbr_band_starts_up, stage2_60d_mfe_20pct, relative_strength_vs_financial_basket, repeat_return_or_medium_term_target | kb_financial_valueup_stage3_candidate, shinhan_overseas_profit_valueup_candidate, jb_financial_regional_high_roe_valueup_case | Stage 3 requires financial bodyweight and capital quality, not cheap valuation by itself. |
| `Stage 4B` | requires_3_of_5 | stage2_120d_mfe_60pct, pbr_breaks_historical_top_band, valuation_expands_before_return_execution, financial_basket_crowded, price_rises_before_credit_cost_confirmation | financial_valueup_crowded_4b_watch_case, kb_financial_valueup_stage3_candidate | Financial rerating is cooled when PBR and price outrun return execution and credit quality. |
| `Stage 4C` | hard_gate | cet1_or_kics_sharp_drop, pf_credit_cost_spike, buyback_cancel_cancelled_or_return_cut, capital_raise_or_at1_pressure, exchange_hack_abnormal_withdrawal_customer_compensation, ipo_valuation_cut_or_delay, stablecoin_rule_hurts_issuer_margin, ransomware_financial_service_disruption | naver_dunamu_equity_option_security_4c_watch_case, seoul_guarantee_ipo_ransomware_security_case, bank_credit_cost_pf_overlay_case | Any capital-ratio, credit, security, regulation, or trust break can block Green immediately. |

## Alignment Cases

| case | detected stage | price-path status | verdict | adjustment |
| --- | --- | --- | --- | --- |
| `kb_financial_valueup_stage3_candidate` | Stage 3 candidate + 4B-watch | Net profit and leader frame strong; KRX/PBR/CET1 path need backfill | valueup_leader_requires_capital_quality | credit profit and return; cap before CET1, credit cost, and PBR-band proof |
| `shinhan_overseas_profit_valueup_candidate` | Stage 2/3 candidate | Overseas profit diversification supports rerating but return execution needs proof | overseas_profit_diversification_candidate | credit overseas profit; require repeat return and CET1 |
| `woori_financial_nonbank_capital_buffer_gate_case` | Stage 2 | Non-bank expansion has CET1/capital-buffer gate | nonbank_expansion_capital_gate | credit M&A option; cap before CET1 and return durability |
| `jb_financial_regional_high_roe_valueup_case` | Stage 2/3 candidate | High ROE regional bank needs liquidity and credit quality checks | regional_high_roe_with_liquidity_cap | credit high ROE; penalize liquidity and regional credit risk |
| `korea_insurance_capital_release_valueup_case` | Stage 2/3 candidate | Capital release needs K-ICS, CSM, loss ratio, and IFRS17 quality | insurance_capital_release_requires_kics_csm | credit return option; cap before K-ICS/CSM/loss ratio |
| `kakaobank_profitability_valuation_cap_case` | Stage 2/3 candidate | Record profit and non-interest income matter; users alone do not | internet_bank_profit_not_user_count | credit profit model; penalize credit cost and platform valuation |
| `naver_dunamu_equity_option_security_4c_watch_case` | Stage 2 + 4C-watch | Deal-value reaction and abnormal withdrawal occur together | digital_asset_equity_option_security_gate | credit deal value; hard-review security and approval |
| `toss_superapp_ipo_stablecoin_related_stock_cap_case` | Stage 1/2 option | Toss story is strong but listed related-stock linkage is missing | related_stock_green_cap | credit optionality; require IPO filing, direct equity, and revenue model |
| `seoul_guarantee_ipo_ransomware_security_case` | Stage 2 -> 4C-watch | IPO and guarantee balance are offset by ransomware service disruption | guarantee_insurance_security_hard_cap | credit IPO option; block Green before security remediation |
| `securities_brokerage_market_beta_cycle_case` | Stage 2 cycle | KOSPI rally can lift brokerage revenue but remains cyclical | brokerage_market_beta_not_green | credit trading value; cap before IB/PF/ROE durability |
| `financial_valueup_crowded_4b_watch_case` | 4B-watch | Financial basket rally can outrun individual return and credit confirmation | valueup_crowding_4b_watch | cool broad basket when PBR rerating precedes execution |
| `bank_credit_cost_pf_overlay_case` | hard gate | PF credit cost can invalidate value-up narratives | pf_credit_cost_hard_gate | require reserve and capital-ratio proof |

## Interpretation

- KB/Shinhan/JB/insurance are the Green-capable tests: profit, capital, return, and credit quality must align.
- Woori, KakaoBank, Toss, and Naver-Dunamu test Stage 2 option value with explicit caps.
- Seoul Guarantee, PF credit, security incidents, and stablecoin regulation are hard RedTeam checks.
- Brokerage and broad financial value-up rallies are useful Stage 2/4B signals, not automatic structural Green.
