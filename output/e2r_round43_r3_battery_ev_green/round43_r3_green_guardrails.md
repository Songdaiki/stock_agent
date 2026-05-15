# Round-43 R3 Green Guardrails

| target | posture | Green unlock evidence | Red flags |
| --- | --- | --- | --- |
| `BATTERY_MATERIALS_CAPEX_OVERHEAT` | REDTEAM_FIRST | contract_quality, price_pass_through, fcf_after_capex, demand_visibility | ev_demand_slowdown, capa_overbuild, lithium_price_crash, customer_capex_cut |
| `BATTERY_EQUIPMENT_PARTS` | WATCH_YELLOW_FIRST | customer_order, delivery_schedule, margin_visibility, op_eps_revision | customer_capex_cut, delivery_delay, single_customer |
| `BATTERY_RECYCLING_ESS_SHIFT` | WATCH_YELLOW_FIRST | ess_contract, capacity_utilization, recycling_volume, fcf_margin | recycling_volume_shortfall, ev_demand_slowdown, metal_price_drop, utilization_drop |
| `EV_INFRASTRUCTURE` | WATCH_YELLOW_FIRST | utilization, recurring_revenue, profitability | low_utilization, subsidy_dependency, fire_regulation |
| `HYDROGEN_FUEL_CELL_INFRA` | WATCH_YELLOW_FIRST | customer_demand, production_capacity, utilization, op_eps_conversion | subsidy_dependency, customer_absent, low_utilization |
| `SOLAR_TARIFF_SUPPLYCHAIN` | REDTEAM_FIRST | utilization, customer_contract, supply_chain_stable, fcf_margin | tariff_risk, customs_detention, uflpa_detention, subsidy_dependency |
| `RENEWABLE_ENERGY_POLICY` | WATCH_YELLOW_FIRST | permitting, funding, cost_schedule, margin_visibility | permitting_delay, financing_cost, cost_overrun, impairment |
| `ENERGY_DISTRIBUTION_FUEL` | WATCH_YELLOW_FIRST | spread_improvement, inventory_status, fcf_margin | price_reversal, inventory_loss, policy_shock |
| `WASTE_RECYCLING_ENVIRONMENT` | GREEN_POSSIBLE | permit_asset, treatment_volume, utilization, recurring_fcf | utilization_drop, capex_burden, commodity_recycling_price_drop |
| `CARBON_CREDIT_CBAM_COMPLIANCE` | WATCH_YELLOW_FIRST | recurring_revenue, verification_customer, cost_pass_through | carbon_price_volatility, greenwashing, policy_reversal |
| `DATA_CENTER_WATER_REUSE_INFRA` | WATCH_YELLOW_FIRST | data_center_customer, contracted_revenue, unit_economics | customer_absent, local_opposition, weak_economics |
| `EV_FIRE_RISK_OVERLAY` | REDTEAM_FIRST | not applicable | recall, fire_regulation, insurance_cost, plant_shutdown, customer_loss |

## What Not To Change

- Do not apply these R3 v1.0 weights to production scoring yet.
- Do not treat EV, ESS, solar, hydrogen, recycling, or carbon-policy labels as score evidence by themselves.
- Do not invent contracts, utilization, margin, FCF, CAPEX, subsidy, tariff, mineral-price, or price-path fields.
- Do not lower Stage 3-Green for growth themes. Most R3 paths should remain Watch until FCF is visible.
- Treat plant idle, worker furlough, customs detention, impairment, lithium price crash, fire, recall, and regulation as RedTeam evidence.
