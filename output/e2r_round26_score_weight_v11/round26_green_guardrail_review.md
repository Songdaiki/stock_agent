# Round-26 Green Guardrail Review

| target | posture | Green unlock evidence | Red flags |
|---|---|---|---|
| AI_DATA_CENTER_COOLING | GREEN_POSSIBLE | customer_datacenter_capex_link, confirmed_order_or_delivery, cooling_bottleneck, repeat_service_revenue, op_eps_revision | liquid_cooling_theme_only, no_customer_order, ai_capex_delay, low_margin_project, customer_concentration |
| MEMORY_HBM_CAPACITY | GREEN_POSSIBLE | hbm_demand, supply_discipline, medium_term_revision, capacity_constraint, long_term_contract_or_prepayment | capex_reversal, cycle_peak, crowding, price_only_memory_rally, customer_ai_capex_slowdown |
| K_BEAUTY_EXPORT_DISTRIBUTION | GREEN_POSSIBLE | export_growth, channel_diversification, repeat_orders, opm_roe_improvement, inventory_receivables_clean | inventory, receivables, china_dependency, tariff, channel_stuffing, viral_only |
| DIGITAL_ASSET_TOKENIZATION | WATCH_YELLOW_FIRST | license_or_approval, actual_issuance, transaction_volume, fee_or_spread_revenue, regulatory_risk_low | regulation, security, adoption, liquidity, no_revenue, theme_only |
| HYDROGEN_RENEWABLE | WATCH_YELLOW_FIRST | actual_capex, utilization_up, customer_or_government_demand, op_eps_conversion, policy_risk_low | policy, subsidy, tariff, customs, supply_chain, utilization |
| CLOUD_AI_SOFTWARE_INFRA | GREEN_POSSIBLE | recurring_revenue, arpu, retention, opm_or_fcf_improvement, ai_cost_control | ai_feature_only, ai_cost_overrun, churn, si_revenue_only, opm_decline |
| SECURITY_IDENTITY_DEEPFAKE | GREEN_POSSIBLE | recurring_subscription, low_churn, customer_diversification, opm_improvement, no_major_outage | operational_trust, outage, legal, customer_retention, contract_absence |
| CRO_CLINICAL_SERVICE | WATCH_YELLOW_FIRST | service_backlog, customer_diversification, repeat_clinical_service_revenue, opm_improvement, funding_cycle_stable | biotech_funding_cycle_down, customer_concentration, trial_delay, low_margin_backlog, customer_budget_cut |
| CONSTRUCTION_BUILDING_MATERIALS | WATCH_YELLOW_FIRST | cost_stability, price_pass_through, shipment_recovery, pf_risk_low, fcf_improvement | credit, rates, vacancy, pf, unsold_inventory, relief_only |
| INSURANCE_UNDERWRITING_CYCLE | GREEN_POSSIBLE | roe_improvement, csm_or_loss_ratio_stability, capital_ratio_stable, shareholder_return_execution, credit_risk_low | underwriting, capital_ratio, cyber_operational, credit_cost, low_pbr_only |
| SECURITIES_BROKERAGE_CYCLE | WATCH_YELLOW_FIRST | brokerage_revenue_growth, ib_pipeline, capital_ratio_stable, pf_risk_low, roe_improvement | market_turnover, pf, proprietary_loss, ipo_cycle, vc_exit_market_weakness |

## What Not To Change
- Do not apply v1.1 weights to production scoring yet.
- Do not score policies, AI features, PoCs, revenue headlines, or theme labels without source-backed economics.
- Do not invent stage dates, prices, margins, retention, FCF, reimbursement, issuance volume, or contract values.
