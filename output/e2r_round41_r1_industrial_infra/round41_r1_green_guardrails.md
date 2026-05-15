# Round-41 R1 Green Guardrails

| target | posture | Green unlock evidence | Red flags |
| --- | --- | --- | --- |
| `GRID_TRANSFORMER_SHORTAGE` | GREEN_POSSIBLE | contract_quality, lead_time_extended, pricing_power, op_eps_revision, backlog_growth | capa_normalization, low_margin_contract, project_delay |
| `CONTRACT_BACKLOG_INDUSTRIAL` | GREEN_POSSIBLE | contract_amount_to_sales, contract_duration, delivery_schedule, margin_visible, op_eps_revision | contract_quality_unclear, delivery_delay, margin_uncertainty |
| `DEFENSE_GOVERNMENT_BACKLOG` | GREEN_POSSIBLE | government_customer, multi_year_contract, delivery_schedule, backlog_growth, opm_improvement | delivery_delay, cost_overrun, export_permit_issue, dilution |
| `DEFENSE_TECH_AUTONOMOUS_SYSTEMS` | WATCH_YELLOW_FIRST | framework_to_order_conversion, production_capacity, customer_budget, eps_conversion | procurement_delay, valuation_overheat, program_cancelled |
| `DEFENSE_DRONE_COUNTER_UAS` | WATCH_YELLOW_FIRST | actual_order, delivery_schedule, production_capacity, repeat_procurement | mna_dilution, export_control, prototype_only |
| `DEFENSE_AI_SOFTWARE_INTELLIGENCE` | WATCH_YELLOW_FIRST | government_customer, deployment_schedule, recurring_license, gross_margin_visible | prototype_stage, political_ethics_risk, budget_cycle |
| `SHIPBUILDING_OFFSHORE_BACKLOG` | GREEN_POSSIBLE | newbuilding_price_up, low_margin_backlog_rolloff, high_margin_delivery_start, op_eps_revision | low_margin_backlog, steel_plate_cost, labor_cost, contract_cancellation |
| `RAIL_INFRASTRUCTURE` | WATCH_YELLOW_FIRST | official_contract, contract_amount_to_sales, delivery_schedule, margin_visible | project_delay, margin_uncertainty, financing |
| `NUCLEAR_SMR_GRID_POLICY` | WATCH_YELLOW_FIRST | ppa_or_signed_contract, permitting, financing, supplier_revenue_path | legal_delay, cost_overrun, financing_failed, policy_headline_only |
| `GEOPOLITICAL_RECONSTRUCTION` | WATCH_YELLOW_FIRST | binding_contract, revenue_schedule, financing_visible, margin_visible | actual_contract_missing, policy_event_only, mou_only |
| `SMART_FACTORY_AUTOMATION` | WATCH_YELLOW_FIRST | actual_order, installed_base, recurring_revenue, opm_improvement | mou_only, poc_only, revenue_conversion_failure |
| `AI_DATA_CENTER_POWER_EQUIPMENT` | GREEN_POSSIBLE | confirmed_booking, delivery_schedule, backlog_growth, op_margin_improvement | bookings_slowdown, low_margin_project, capex_delay |

## What Not To Change

- Do not apply these R1 v1.0 weights to production scoring yet.
- Do not treat order headlines, MOU, policy events, or case IDs as score evidence.
- Do not invent contract size, duration, margin, backlog, EPS, FCF, or price path fields.
- Do not lower Stage 3-Green thresholds because R1 is a Green-capable sector.
