# Round-36 Green Guardrail Review

| target | posture | validation_group | Green unlock evidence | Red flags |
|---|---|---|---|---|
| GRID_TRANSFORMER_SHORTAGE | GREEN_POSSIBLE | green_possible | contract_to_sales, multi_year_delivery, backlog_growth, pricing_power, op_eps_revision | capacity_normalization, low_margin_contract, project_delay, raw_material |
| ANIMAL_HEALTH_BIOSECURITY | WATCH_YELLOW_FIRST | cycle_event | government_stockpile, repeat_vaccination, biosecurity_contract, animal_health_sales_growth | disease_event_normalization, policy_uncertainty, one_off_demand, disease_control |
| TELEHEALTH_BEHAVIORAL_HEALTH | WATCH_YELLOW_FIRST | watch_to_green | employer_or_insurance_contract, repeat_usage, cac_stable, fcf_improvement | cac, privacy, reimbursement, churn, impairment, dtc_ad_dependency |
| PRECIOUS_METALS_SAFE_HAVEN_MINERS | WATCH_YELLOW_FIRST | cycle_event | realized_price_up, aisc_stable_or_down, fcf_growth, buyback_or_dividend | gold_price_reversal, aisc, jurisdiction, production_decline, price_theme_only |
| SERVICE_KIOSK_SELF_CHECKOUT | WATCH_YELLOW_FIRST | watch_to_green | installed_base_growth, maintenance_recurring_revenue, payment_fee_revenue, loss_prevention_effect | theft, customer_friction, one_off_hardware, maintenance_cost, retailer_retreat, pseudo_automation |
| OPTICAL_NETWORKING_AI_DATACENTER | GREEN_POSSIBLE | green_possible | hyperscaler_long_contract, direct_ai_datacenter_supply, bottleneck_optical_component, op_eps_revision | hyperscaler_concentration, valuation_crowding, capex_delay, inventory, unclear_ai_dc_exposure |
| AI_GRID_FLEXIBILITY_SOFTWARE | WATCH_YELLOW_FIRST | watch_to_green | utility_or_datacenter_customer, recurring_sw_revenue, interconnection_savings, opm_improvement | commercialization, utility_adoption, regulation, proof_of_concept_only, no_revenue |
| PHARMA_CHANNEL_AND_PRIVACY_RISK | REDTEAM_FIRST | red_flag | b2b_b2b2c_contract, low_cac, privacy_compliance, legal_distribution_channel | privacy, advertising_cac, fda_warning, illegal_pharmacy, liability, impairment |

## What Not To Change
- Do not apply v2.1 weights to production scoring yet.
- Do not use case IDs, theme labels, disease headlines, PoCs, or commodity prices as candidate-generation input.
- Do not invent stage dates, prices, contract terms, vaccine stockpile, CAC, AISC, recurring revenue, hyperscaler terms, ARR, or privacy status.
- Do not lower Stage 3-Green thresholds to improve recall.
