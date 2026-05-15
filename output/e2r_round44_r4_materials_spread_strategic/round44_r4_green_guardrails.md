# Round-44 R4 Green Guardrails

| target | posture | Green unlock evidence | Red flags |
| --- | --- | --- | --- |
| `REFINING_OIL_SPREAD` | WATCH_YELLOW_FIRST | repeat_fcf, core_margin, inventory_noise_excluded | inventory_loss, refining_margin_drop, logistics_delay |
| `CHEMICAL_SPREAD` | REDTEAM_FIRST | supply_glut_easing, capacity_restructuring, durable_margin | china_middle_east_capacity_glut, spread_reversal, inventory_increase |
| `STEEL_METAL_SPREAD` | WATCH_YELLOW_FIRST | supply_discipline, demand_recovery, fcf_margin | chinese_exports, construction_demand_weak, price_pressure |
| `NONFERROUS_STRATEGIC_METALS` | WATCH_YELLOW_FIRST | cost_curve_advantage, supply_constraint, fcf_conversion | metal_price_drop, china_demand, margin_drop |
| `RARE_METALS_STRATEGIC_MATERIALS` | WATCH_YELLOW_FIRST | government_investment, price_floor, offtake_contract, production_capacity, fcf_conversion | project_delay, policy_dependency, price_only_rally |
| `LITHIUM_BATTERY_RAW_MATERIAL` | WATCH_YELLOW_FIRST | low_cost_mine, offtake, fcf_defense, capex_discipline | price_crash, mine_restart, ev_demand_slowdown |
| `PRECIOUS_METALS_SAFE_HAVEN_MINERS` | WATCH_YELLOW_FIRST | realized_price, aisc_control, capital_return, fcf_conversion | gold_price_correction, aisc_rise, mine_risk |
| `ADVANCED_MATERIAL_SPECULATIVE_THEME` | REDTEAM_FIRST | commercial_contract, revenue_conversion, fcf_path | paper_only, no_revenue, theme_only |
| `PAPER_PACKAGING_CYCLE` | WATCH_YELLOW_FIRST | volume_recovery, price_cost_spread, cash_return | low_volume, price_pressure, mature_industry |
| `AGRI_COMMODITY_INPUTS` | WATCH_YELLOW_FIRST | price_pass_through, repeat_margin, fcf_margin | weather_event_only, inventory_loss, commodity_reversal |
| `LNG_ENERGY_TRADING_DISTRIBUTION` | WATCH_YELLOW_FIRST | long_term_contract, margin_visible, repeat_fcf, project_stake | price_reversal, inventory_loss, financing_delay |
| `GENERAL_TRADING_RESOURCE_INFRA` | WATCH_YELLOW_FIRST | long_term_offtake, project_stake, fcf, capital_return | commodity_cycle, project_delay, capital_allocation_retreat |
| `ENERGY_UTILITY_LNG_GAS` | WATCH_YELLOW_FIRST | tariff_visibility, cash_flow_recovery, debt_reduction | tariff_freeze, debt_burden, policy_risk |

## What Not To Change

- Do not apply these R4 v1.0 weights to production scoring yet.
- Do not treat commodity price rallies, spread headlines, tender offers, policy events, or theme labels as score evidence by themselves.
- Do not invent commodity price, spread, offtake, price floor, FCF, dividend, buyback, or price-path fields.
- Do not lower Stage 3-Green for commodity cycles. Most R4 paths should remain Watch/Cycle/Event until FCF durability is proven.
- Treat supply glut, price crash, project delay, dividend cut, inventory loss, and no-commercialization advanced materials as RedTeam evidence.
