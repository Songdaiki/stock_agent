# Round-30 Green Guardrail Review

| target | posture | Green unlock evidence | Red flags |
|---|---|---|---|
| SEMI_EQUIPMENT_CAPEX | WATCH_YELLOW_FIRST | customer_capex_confirmed, order_backlog_growth, delivery_schedule, op_eps_revision, customer_concentration_risk_low | customer_capex, customer_concentration, inventory, order_delay, adoption_delay |
| AUTO_COMPLETED_VEHICLE | GREEN_POSSIBLE | op_fcf_stability, hybrid_or_mix_improvement, shareholder_return, roe_pbr_rerating, tariff_risk_low | tariff, demand_slowdown, recall, peak_margin, policy_risk |
| AUTO_COMPONENTS_TIRE | WATCH_YELLOW_FIRST | customer_diversification, cost_pass_through, op_eps_revision, raw_material_stable, quality_cost_low | raw_material, customer_concentration, ev_cycle, quality_cost, oem_pressure |
| AIRLINE_TRAVEL_CYCLE | WATCH_YELLOW_FIRST | op_recovery, integration_synergy, cost_stability, fcf_improvement, fuel_fx_risk_low | oil_price, fx, demand_cycle, integration_cost, tariff |
| CASINO_DUTYFREE_TOURISM | WATCH_YELLOW_FIRST | visitor_growth_converts_to_op, drop_amount_growth, dutyfree_ticket_recovery, tourist_mix_diversified, capex_burden_low | tourism_policy, china_dependency, capex, operating_leverage, weak_demand |
| RETAIL_CONVENIENCE_OFFLINE | WATCH_YELLOW_FIRST | same_store_sales_growth, pb_high_margin_mix, opm_improvement, fcf_stable, rent_wage_pressure_low | rent, wage, competition, same_store_sales_slowdown, store_count_only |
| AGRI_LIVESTOCK_FOOD_COMMODITY | REDTEAM_FIRST | cost_pass_through, sustained_margin, repeat_demand, weather_or_disease_risk_low | commodity_cycle, disease_event, feed_cost, weather, price_event_only |
| SPACE_SUPPLYCHAIN | WATCH_YELLOW_FIRST | actual_delivery_contract, government_or_defense_customer, repeat_component_revenue, certification_complete | no_contract, certification_delay, theme_overheat, poc_only, no_revenue |
| AI_DATA_CENTER_COOLING | GREEN_POSSIBLE | orders_or_leases, power_cooling_constraint, delivery_schedule, op_eps_revision, capex_delay_risk_low | capex_delay, project_delay, overbuild, no_revenue_exposure |
| MEMORY_HBM | GREEN_POSSIBLE | hbm_demand, memory_price_increase, fy1_fy2_op_eps_revision, supply_discipline, capacity_bottleneck | crowding, capex_reversal, memory_price_drop, customer_capex_cut |

## What Not To Change
- Do not apply v1.5 weights to production scoring yet.
- Do not use case IDs or theme labels as candidate-generation input.
- Do not invent stage dates, prices, contract size, OP YoY, ASP, OPM, store productivity, tourist mix, CAPEX, or FCF.
- Do not lower Stage 3-Green thresholds to improve recall.
