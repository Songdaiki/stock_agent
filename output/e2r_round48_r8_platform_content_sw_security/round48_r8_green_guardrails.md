# Round-48 R8 Green Guardrails

| target | posture | Green unlock evidence | Red flags |
| --- | --- | --- | --- |
| `PLATFORM_SOFTWARE_INTERNET` | WATCH_YELLOW_FIRST | arpu_growth, recurring_revenue, opm_improvement, fcf_conversion, governance_clean | regulation, governance, privacy, legal_overhang, trust_damage |
| `CLOUD_AI_SOFTWARE_INFRA` | GREEN_POSSIBLE | arr_growth, recurring_revenue_ratio, net_retention_rate, opm_improvement, fcf_conversion | churn, ai_cost, si_revenue_mix, customer_concentration, margin_slowdown |
| `AI_SOFTWARE_APPLICATION` | WATCH_YELLOW_FIRST | paid_usage, api_revenue, workflow_integration, compute_cost_controlled, fcf_conversion | compute_cost, model_dependency, copyright, data_privacy, free_user_growth_only |
| `GENERATIVE_AI_IP_RISK` | REDTEAM_FIRST | licensed_data, rights_cleared_revenue, enterprise_contract, liability_risk_low | copyright, license_risk, privacy, open_source_supply_chain |
| `CONTACT_CENTER_AI_AUTOMATION` | WATCH_YELLOW_FIRST | enterprise_contract, seat_expansion, low_churn, retention_rate, opm_improvement | churn, it_budget_cut, privacy, roi_failure |
| `SERVICE_KIOSK_SELF_CHECKOUT` | WATCH_YELLOW_FIRST | maintenance_revenue, payment_fee_revenue, store_roi, customer_acceptance | theft, customer_complaint, hardware_one_off, regulation |
| `GAME_CONTENT_IP` | WATCH_YELLOW_FIRST | bookings_growth, sell_through, live_service_monetization, repeat_ip_portfolio | single_ip, game_delay, child_safety, regulatory_ban, bookings_cut |
| `MEDIA_AD_CONTENT_CYCLE` | WATCH_YELLOW_FIRST | ad_revenue_growth, ad_arpu, opm_improvement, budget_resilience | ad_cycle, client_budget_cut, privacy, scam_ads, ai_disintermediation |
| `STREAMING_AD_PLATFORM` | WATCH_YELLOW_FIRST | ad_tier_users, ad_revenue_growth, ad_arpu, privacy_risk_low | privacy, ad_arpu_saturation, ad_load, subscriber_churn |
| `SECURITY_IDENTITY_DEEPFAKE` | WATCH_YELLOW_FIRST | arr_growth, low_churn, renewal_rate, customer_diversification, operational_trust_intact | outage, lawsuit, renewal_risk, trust_damage, gross_negligence_claim |
| `METAVERSE_NFT_THEME` | REDTEAM_FIRST | platform_fee_revenue, repeat_transaction_volume, regulated_revenue | no_revenue, liquidity, token_price_only, regulation |
| `PLATFORM_GOVERNANCE_LEGAL_RISK` | REDTEAM_FIRST | legal_overhang_resolved, governance_improvement, trust_recovered | founder_legal_case, regulatory_investigation, governance, trust_damage |

## What Not To Change

- Do not apply these R8 v1.0 weights to production scoring yet.
- Do not treat user count, AI feature, new title, security threat headline, NFT/metaverse label, or ad recovery headline as Green evidence by itself.
- Do not invent ARR, ARPU, churn, net retention, bookings, ad revenue, ad-tier users, security renewal, incident recovery, legal status, or price-path fields.
- Do not lower Stage 3-Green for platform recall. Green requires repeat revenue, ARPU/ARR, OPM, FCF, retention, and trust/legal safety.
- Treat outage, customer lawsuit, privacy lawsuit, scam ads, founder legal case, single-IP delay, child-safety forecast cut, and no recurring revenue as RedTeam evidence.
