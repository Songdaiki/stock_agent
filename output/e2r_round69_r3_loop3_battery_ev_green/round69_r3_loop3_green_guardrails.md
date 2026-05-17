# Round-69 R3 Loop-3 Green Guardrails

| target | posture | Green unlock evidence | Loop-3 penalties |
| --- | --- | --- | --- |
| `BATTERY_MATERIALS_CAPEX_OVERHEAT` | REDTEAM_FIRST | contract_quality, price_pass_through, fcf_after_capex, demand_visibility | ev_demand_slowdown, capa_overbuild, contract_cancellation, mineral_price |
| `BATTERY_EQUIPMENT_PARTS` | WATCH_YELLOW_FIRST | customer_order, delivery_schedule, margin_visibility, op_eps_revision | customer_capex_cut, delivery_delay, ev_line_idle |
| `BATTERY_RECYCLING_ESS_SHIFT` | WATCH_YELLOW_FIRST | recycling_volume, metal_recovery_revenue, customer_contract, soh_validation, recurring_fcf | recycling_volume, soh_validation, metal_price, contract_value_missing |
| `ESS_LFP_GRID_STORAGE` | GREEN_POSSIBLE | ess_contract_value, ess_contract_duration, customer, gwh_volume, ess_margin, fcf_conversion | ess_margin, lfp_competition, customer_concentration, subsidy |
| `EV_INFRASTRUCTURE` | WATCH_YELLOW_FIRST | utilization, recurring_revenue, profitability | utilization, fire_regulation, subsidy_dependency |
| `HYDROGEN_FUEL_CELL_INFRA` | WATCH_YELLOW_FIRST | customer_demand, production_capacity, utilization, op_eps_conversion | customer_absent, utilization, subsidy_dependency, infrastructure_gap |
| `SOLAR_TARIFF_SUPPLYCHAIN` | REDTEAM_FIRST | utilization, customer_contract, supply_chain_stable, fcf_margin | customs, tariff, uflpa, feoc, supply_chain_disruption |
| `RENEWABLE_ENERGY_POLICY` | WATCH_YELLOW_FIRST | permitting, funding, cost_schedule, margin_visibility | rates, cost_overrun, permitting, impairment |
| `WASTE_RECYCLING_ENVIRONMENT` | GREEN_POSSIBLE | permit_asset, treatment_volume, utilization, recurring_fcf | utilization, capex, metal_price, regulatory_cost |
| `CARBON_CREDIT_CBAM_COMPLIANCE` | WATCH_YELLOW_FIRST | recurring_revenue, verification_customer, cost_pass_through | policy_reform, carbon_price, greenwashing |
| `DATA_CENTER_WATER_REUSE_INFRA` | WATCH_YELLOW_FIRST | data_center_customer, contracted_revenue, unit_economics | customer_absent, local_opposition, economics |
| `EV_FIRE_RISK_OVERLAY` | REDTEAM_FIRST | not_applicable | fire, certification, recall, insurance |
| `BATTERY_HEALTH_TRANSPARENCY_OVERLAY` | REDTEAM_FIRST | not_applicable | soh, second_life_validation, battery_passport, grading_cost |
| `LITHIUM_CYCLE_OVERLAY` | WATCH_YELLOW_FIRST | low_cost_structure, long_term_offtake, fcf_defense, capex_discipline | price_crash, mine_restart, sodium_ion, ev_demand_slowdown |

## What Not To Change

- Do not apply R3 Loop-3 v3.0 weights to production scoring yet.
- Do not treat EV growth, ESS, recycling, hydrogen, solar, wind, or lithium labels as Green evidence by themselves.
- Do not invent contract value, customer, duration, GWh, margin, utilization, recovery volume, SOH, stage prices, or FCF.
- Treat plant idle, contract cancellation, customs detention, wind impairment, lithium supply rebound, EV fire, and SOH opacity as RedTeam fields.
