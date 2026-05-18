# Round-179 R8 Loop-11 Green Guardrails

| target | posture | Green unlock evidence | Loop-11 penalties |
| --- | --- | --- | --- |
| `ENTERPRISE_AI_CLOUD_INFRA_KOREA` | WATCH_YELLOW_FIRST | ai_cloud_revenue, arr, long_term_cloud_contract, opm_fcf_improvement, mna_execution | cb_dilution, ai_arr_missing, mna_execution, margin |
| `B2B_SAAS_ERP_WORKFLOW_KOREA` | GREEN_POSSIBLE | arr_growth, low_churn, opm_fcf_improvement, arpu_growth, renewal_rate | arr_missing, churn, opm, pe_event_premium |
| `PRIVATE_EQUITY_SOFTWARE_RERATING` | WATCH_YELLOW_FIRST | opm_improvement, fcf_conversion, arr_growth, operational_kpi_improves | event_premium, execution, governance |
| `AI_CLOUD_CAPITAL_ALLOCATION` | REDTEAM_FIRST | disciplined_mna, ai_revenue_after_capex, fcf_after_investment | dilution, mna, capex, margin |
| `SOVEREIGN_KOREAN_AI_MODEL` | WATCH_YELLOW_FIRST | b2b_paid_api, cloud_revenue, ai_search_ad_arpu, inference_margin, enterprise_contract | monetization, inference_cost, arpu, competition |
| `WEBTOON_PLATFORM_IP_MONETIZATION` | WATCH_YELLOW_FIRST | paid_content_growth, ad_arpu, ip_adaptation_revenue, opm_fcf, retention | guidance, ip_adaptation, net_loss, monetization |
| `PLATFORM_PRIVACY_SECURITY_OVERLAY` | REDTEAM_FIRST |  | privacy, security, regulatory, governance |
| `GAME_CONTENT_IP_REPEAT_MONETIZATION` | GREEN_POSSIBLE | live_service_bookings, repeat_sales, opm_fcf, pipeline_stability, bookings_growth | single_ip, launch, legal, valuation |
| `GAME_SINGLE_IP_EVENT_PREMIUM` | WATCH_YELLOW_FIRST | repeat_bookings, retention, follow_on_sales, opm_fcf | single_ip, ipo, pipeline, retention |
| `GAME_IP_LAUNCH_DELAY_LEGAL_RISK` | REDTEAM_FIRST |  | release_delay, lawsuit, community, trust |
| `KPOP_PLATFORM_CONTENT_IP` | WATCH_YELLOW_FIRST | fan_platform_arpu, album_tour_revenue, opm_fcf, artist_pipeline_stability, china_performance_reopens | legal, governance, artist_ip, china |
| `ENTERTAINMENT_GOVERNANCE_LEGAL_OVERLAY` | REDTEAM_FIRST |  | legal, governance, fan_backlash |
| `AD_CONTENT_PLATFORM_GUIDANCE_RISK` | REDTEAM_FIRST |  | guidance, ad_revenue, ip_adaptation, loss |
| `DISCLOSURE_CONFIDENCE_CAP` | REDTEAM_FIRST | arr, bookings, cloud_revenue, ad_revenue, ip_revenue, opm_fcf, security_legal_clean | disclosure, arr_bookings, opm_fcf, legal_security |

## What Not To Change

- Do not apply R8 Loop-11 v11.0 weights to production scoring yet.
- Do not treat AI feature, game IP, Webtoon IPO, K-pop IP, platform MAU, strategic investor, or M&A headline as Green evidence by itself.
- Do not invent ARR, bookings, cloud revenue, ad revenue, IP revenue, OPM, FCF, churn, retention, stage prices, or MFE/MAE.
- Green requires ARR/bookings/revenue evidence, repeatability, OPM/FCF conversion, clean trust/legal status, and price-path support.
- Security incident, privacy leak, founder legal risk, release delay, lawsuit, guidance miss, IP adaptation miss, and platform governance conflict remain RedTeam gates.
