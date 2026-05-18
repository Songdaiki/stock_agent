# Round-190 R6 Loop-12 Risk Overlays

| target | hard gate | red flags |
| --- | --- | --- |
| `INSURANCE_NAV_VALUEUP_SAMSUNG_ELECTRONICS_STAKE` | false | k_ics_csm_missing, return_execution_missing, nav_is_price_only |
| `SHAREHOLDER_RETURN_COMPOUNDING_FINANCIAL_HOLDCO` | false | credit_cost_unconfirmed, capital_ratio_unconfirmed, return_detail_missing |
| `DIGITAL_ASSET_BANK_EQUITY_OPTION` | false | regulatory_approval_pending, exchange_security_risk, equity_method_income_missing |
| `KRW_STABLECOIN_POLICY_THEME` | false | issuer_economics_missing, regulatory_framework_unclear, price_only_rally |
| `PAYMENT_BIOMETRIC_INFRASTRUCTURE` | false | take_rate_missing, biometric_privacy_risk, direct_revenue_link_missing |
| `PAYMENT_PRIVACY_REGULATORY_4C` | true | privacy_fine, consent_issue, platform_trust_damage |
| `CREDIT_INFORMATION_RECURRING_DATA` | false | security_incident_risk, growth_rate_missing, regulatory_data_protection |
| `SECURITIES_BROKERAGE_MARKET_BETA` | false | market_beta_only, trading_value_cycle, pf_ib_loss_risk, tax_policy_risk |
| `BUYBACK_EXECUTION_PRICE_FAILED` | true | price_failed, operating_concern_dominates, eps_roe_missing |
| `POLICY_TAX_REVERSAL_MARKET_SHOCK` | true | tax_policy_shock, valueup_basket_crowding, policy_reversal |
| `DISCLOSURE_CONFIDENCE_CAP` | false | opendart_list_only, media_report_only, detail_missing, security_detail_missing |

## Hard / Cap Examples

- `PAYMENT_PRIVACY_REGULATORY_4C`: 개인정보·동의·플랫폼 신뢰 문제는 결제 플랫폼 Green hard gate다.
- `BUYBACK_EXECUTION_PRICE_FAILED`: 실제 소각도 가격과 영업 논리가 실패하면 Green 근거가 아니다.
- `POLICY_TAX_REVERSAL_MARKET_SHOCK`: 세제 역풍은 value-up 바스켓을 4C-watch로 돌릴 수 있다.
- `KRW_STABLECOIN_POLICY_THEME`: 발행량·reserve income·take-rate 없는 주가 급등은 4B-watch다.
- `DISCLOSURE_CONFIDENCE_CAP`: 환원·자본비율·디지털 수익모델·보안 detail 없으면 Green 금지.
