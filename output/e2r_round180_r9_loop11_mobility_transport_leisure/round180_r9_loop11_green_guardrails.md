# Round-180 R9 Loop-11 Green Guardrails

| target | posture | Green unlock evidence | Loop-11 penalties |
| --- | --- | --- | --- |
| `AUTO_HYBRID_LOCALIZATION_KOREA` | WATCH_YELLOW_FIRST | hybrid_sales_growth, opm_defense, tariff_cost_absorbed, fcf_and_return_stable, sdv_capex_control | sdv_delay, ev_target_cut, capex, price_war, tariff |
| `AUTO_SDV_DELAY_CAPEX_OVERLAY` | REDTEAM_FIRST |  | delay, capex, ev_target_cut, execution |
| `AUTO_PRICE_WAR_EUROPE_OVERLAY` | REDTEAM_FIRST |  | price_cut, opm, competition, europe |
| `AUTO_COMPONENT_RESTRUCTURING_KOREA` | WATCH_YELLOW_FIRST | deal_finalized, opm_improvement, fcf_or_return_improvement, quality_cost_low | quality, recall, warranty, deal_not_final |
| `AUTO_COMPONENT_QUALITY_RECALL_OVERLAY` | REDTEAM_FIRST |  | recall, warranty, quality, trust |
| `ECOMMERCE_LOGISTICS_REPEAT_CONTRACT` | GREEN_POSSIBLE | parcel_unit_price_defended, opm_fcf_improvement, automation_efficiency, repeat_customer_contracts, labor_cost_controlled | unit_price, labor, opm, operation |
| `LOGISTICS_LABOR_REGULATION_OVERLAY` | REDTEAM_FIRST |  | labor, regulation, unit_cost, operation |
| `CASINO_DUTYFREE_TOURISM_POLICY_KOREA` | WATCH_YELLOW_FIRST | average_spend, dutyfree_sales, casino_drop_amount, hold_rate, revpar, opm_fcf | spend_missing, drop_missing, return_visitor, policy_event |
| `CASINO_RETURN_VISITOR_UNIT_ECONOMICS` | GREEN_POSSIBLE | casino_drop_amount, hold_rate, return_visitor_rate, average_spend, revpar, opm_fcf | drop, hold, return_visitor, debt |
| `AIRLINE_SAFETY_REGULATORY_OVERLAY` | REDTEAM_FIRST |  | safety, inspection, trust, cancellation |
| `SHIPPING_FREIGHT_CYCLE_KOREA` | WATCH_YELLOW_FIRST | multi_year_supply_discipline, contract_freight_visibility, fleet_discipline, cashflow_resilience | freight_cycle, overcapacity, route_normalization, new_supply |
| `PARCEL_VOLUME_PRICE_COST_SPREAD` | GREEN_POSSIBLE | parcel_unit_price_defended, delivery_cost_per_unit_down, opm_fcf_improves, automation_payback, labor_cost_controlled | unit_price, unit_cost, opm, labor |
| `TRAVEL_AGENCY_POLICY_EVENT` | WATCH_YELLOW_FIRST | package_asp_up, opm_fcf_improves, repeat_travel_demand, cancellation_low | asp, opm, policy_only, cancellation |
| `DISCLOSURE_CONFIDENCE_CAP` | REDTEAM_FIRST | contract_amount, freight_rate, casino_drop, opm_fcf, unit_economics | disclosure, detail, opm_fcf, unit_economics |

## What Not To Change

- Do not apply R9 Loop-11 v11.0 weights to production scoring yet.
- Do not treat hybrid, localization, tourism policy, freight spike, parcel volume, casino recovery, or duty-free headline as Green evidence by itself.
- Do not invent contract amount, freight rate, casino drop, OPM, FCF, unit economics, stage prices, or MFE/MAE.
- Green requires OPM/FCF conversion, repeat contract or recurring demand, unit economics, clean safety/quality/regulatory status, and price-path support.
- Safety accident, recall, warranty cost, labor regulation, price war, freight overcapacity, weak spend/drop, and low disclosure confidence remain RedTeam gates.
