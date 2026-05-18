# Round-177 R6 Loop-11 Green Guardrails

| target | posture | Green unlock evidence | Loop-11 penalties |
| --- | --- | --- | --- |
| `BANK_HOLDING_VALUEUP_CAPITAL_RETURN_KOREA` | GREEN_POSSIBLE | roe, net_profit_growth, cet1_ratio, credit_cost, shareholder_return_execution, pbr_roe_band_change | credit_cost, cet1, pf_exposure, return_execution, valueup_crowding |
| `BANK_ROE_PBR_RERATING_KOREA` | GREEN_POSSIBLE | roe, pbr_band_change, credit_cost, repeat_capital_return, relative_strength | roe_quality, credit_cost, pbr_crowding |
| `BANK_CREDIT_COST_PF_OVERLAY` | REDTEAM_FIRST |  | pf_exposure, credit_cost, reserve, capital_ratio |
| `REGIONAL_BANK_HIGH_ROE_VALUEUP` | GREEN_POSSIBLE | high_roe, credit_cost_stable, dividend_policy, pbr_band_change, liquidity_discount_eases | credit_quality, liquidity, dividend_sustainability |
| `INSURANCE_CAPITAL_RELEASE_VALUEUP_KOREA` | GREEN_POSSIBLE | k_ics_ratio, csm_quality, loss_ratio, roe, shareholder_return_execution | k_ics, csm, loss_ratio, ifrs17 |
| `INSURANCE_KICS_CSM_GATE` | REDTEAM_FIRST |  | k_ics, csm, loss_ratio |
| `SECURITIES_BROKERAGE_MARKET_BETA` | WATCH_YELLOW_FIRST | brokerage_revenue, ib_fee, pf_risk_low, roe_improvement | market_beta, pf_loss, tax_policy, trading_value_cycle |
| `SECURITIES_IB_PF_RISK_OVERLAY` | REDTEAM_FIRST |  | pf, ib_loss, liquidity |
| `INTERNET_BANK_PROFITABILITY` | WATCH_YELLOW_FIRST | record_profit, roe, credit_cost, non_interest_income_repeatability, valuation_room | valuation, credit_cost, loan_quality, user_count_only |
| `DIGITAL_ASSET_EXCHANGE_EQUITY_OPTION` | WATCH_YELLOW_FIRST | regulatory_approval, security_stability, equity_method_income, revenue_model, shareholder_value_transmission | security, regulatory, equity_transmission, crypto_volume |
| `FINTECH_SUPERAPP_IPO_OPTION_KOREA` | WATCH_YELLOW_FIRST | ipo_filing, profitability, fcf, direct_equity_link, regulated_revenue_model | ipo_delay, direct_link, stablecoin_approval, valuation |
| `KRW_STABLECOIN_POLICY_OPTION` | WATCH_YELLOW_FIRST |  | regulatory, reserve, issuer_margin, volume |
| `GUARANTEE_INSURANCE_IPO_SECURITY_RISK` | REDTEAM_FIRST | cyber_resilience, service_stability, capital_quality, dividend_policy | security, service_disruption, trust |
| `DISCLOSURE_CONFIDENCE_CAP` | REDTEAM_FIRST | capital_return_detail, capital_ratio_detail, credit_cost_detail, regulatory_detail, security_detail | disclosure_detail, capital_ratio, credit_cost, security |
| `VALUE_UP_CROWDED_4B_WATCH` | REDTEAM_FIRST |  | crowding, policy_only, execution_missing |

## What Not To Change

- Do not apply R6 Loop-11 v11.0 weights to production scoring yet.
- Do not lower Stage 3-Green thresholds because a financial stock rerated.
- Do not use Round 177 case records as candidate-generation input.
- Do not treat low PBR, value-up policy, high dividend, Toss IPO, stablecoin, Dunamu stake, or brokerage volume as Green by itself.
- Do not invent CET1, K-ICS, credit cost, PF exposure, buyback cancellation, dividends, stake value, security remediation, stage prices, or MFE/MAE.
- Apply 4B-watch when PBR/price expands before individual return execution and credit quality are confirmed.
- Apply 4C/hard review for PF credit-cost spike, capital-ratio deterioration, return cut, abnormal withdrawal, ransomware, IPO valuation cut, or stablecoin issuer-margin damage.
