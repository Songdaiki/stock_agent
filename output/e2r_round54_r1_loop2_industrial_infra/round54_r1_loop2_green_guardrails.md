# Round-54 R1 Loop-2 Green Guardrails

| target | posture | Green unlock evidence | Loop-2 penalties |
| --- | --- | --- | --- |
| `GRID_TRANSFORMER_SHORTAGE` | GREEN_POSSIBLE | contract_quality, lead_time_extended, pricing_power, backlog_growth, op_eps_revision | data_center_delay, project_delay, capa_normalization, low_margin_contract |
| `AI_DATA_CENTER_POWER_EQUIPMENT` | GREEN_POSSIBLE | bookings_growth, delivery_schedule, backlog_growth, op_margin_improvement | bookings_slowdown, project_delay, low_margin_project |
| `CONTRACT_BACKLOG_INDUSTRIAL` | GREEN_POSSIBLE | contract_value, contract_duration, delivery_schedule, margin_visible, op_eps_revision | contract_quality_unclear, delivery_delay, margin_uncertainty |
| `DEFENSE_GOVERNMENT_BACKLOG` | GREEN_POSSIBLE | government_customer, multi_year_contract, delivery_schedule, backlog_growth, opm_improvement | capital_allocation_shock, dilution, delivery_delay, export_permit_issue |
| `DEFENSE_TECH_AUTONOMOUS_SYSTEMS` | WATCH_YELLOW_FIRST | framework_to_order_conversion, production_capacity, customer_budget, eps_conversion | prototype_only, procurement_delay, valuation_overheat |
| `DEFENSE_DRONE_COUNTER_UAS` | WATCH_YELLOW_FIRST | actual_order, delivery_schedule, production_capacity, repeat_procurement | prototype_only, mna_dilution, export_control |
| `DEFENSE_AI_SOFTWARE_INTELLIGENCE` | WATCH_YELLOW_FIRST | government_customer, deployment_schedule, recurring_license, gross_margin_visible | prototype_stage, budget_cycle, political_ethics_risk |
| `SHIPBUILDING_OFFSHORE_BACKLOG` | GREEN_POSSIBLE | newbuilding_price_up, low_margin_backlog_rolloff, high_margin_delivery_start, op_eps_revision | low_margin_backlog, steel_plate_cost, labor_cost, block_sale_overhang |
| `RAIL_INFRASTRUCTURE` | WATCH_YELLOW_FIRST | official_contract, contract_amount_to_sales, delivery_schedule, margin_visible, financing_secured | project_delay, margin_uncertainty, financing |
| `NUCLEAR_SMR_GRID_POLICY` | WATCH_YELLOW_FIRST | ppa_or_signed_contract, permitting, financing, supplier_revenue_path, ppa_price_visible | cost_overrun, financing_failed, legal_delay, customer_subscription_failed |
| `GEOPOLITICAL_RECONSTRUCTION` | WATCH_YELLOW_FIRST | binding_contract, revenue_schedule, financing_visible, margin_visible | policy_to_contract_failed, financing_failure, mou_only |
| `SMART_FACTORY_AUTOMATION` | WATCH_YELLOW_FIRST | actual_order, installed_base, recurring_revenue, opm_improvement | mou_only, poc_only, customer_capex_delay |

## What Not To Change

- Do not apply R1 Loop-2 v2.0 weights to production scoring yet.
- Do not lower Stage 3-Green thresholds because R1 is Green-capable.
- Do not treat MOU, policy expectation, prototype, or project headline as Green evidence.
- Do not invent contract values, contract dates, delivery schedules, margins, or stage prices.
- Treat project delay, capital-allocation shock, CAPA normalization, low-margin backlog, financing failure, and cost overrun as strong penalties.
