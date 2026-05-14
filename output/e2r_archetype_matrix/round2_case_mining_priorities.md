# Round-2 Case Mining Priorities

Priority 1 is where current engine weaknesses are most visible.

| priority | archetype | positive | counterexamples | status |
|---:|---|---:|---:|---|
| 1 | CONTRACT_BACKLOG_INDUSTRIAL | 3 | 1 | needs_more_cases |
| 1 | DEFENSE_GOVERNMENT_BACKLOG | 1 | 1 | needs_more_cases |
| 1 | EXPORT_RECURRING_CONSUMER | 1 | 2 | needs_more_cases |
| 1 | K_BEAUTY_EXPORT_DISTRIBUTION | 2 | 2 | covered_2x2 |
| 1 | MEMORY_HBM_CAPACITY | 2 | 2 | covered_2x2 |
| 1 | ONE_OFF_EVENT_DEMAND | 0 | 1 | needs_more_counterexamples |
| 1 | SHIPPING_FREIGHT_CYCLE | 1 | 1 | needs_more_cases |
| 1 | THEME_VALUATION_OVERHEAT | 0 | 1 | needs_more_counterexamples |
| 2 | AUTO_MOBILITY_COMPONENTS | 0 | 0 | needs_more_cases |
| 2 | BATTERY_MATERIALS_CAPEX_OVERHEAT | 0 | 2 | needs_more_cases |
| 2 | COMMODITY_SPREAD | 1 | 1 | needs_more_cases |
| 2 | FINANCIAL_SPREAD_BALANCE_SHEET | 0 | 5 | needs_more_cases |
| 2 | MEDICAL_DEVICE_HEALTHCARE_EXPORT | 2 | 3 | covered_2x2 |
| 2 | SEMI_EQUIPMENT_CAPEX | 3 | 2 | covered_2x2 |
| 2 | SHIPBUILDING_OFFSHORE_BACKLOG | 1 | 1 | needs_more_cases |
| 2 | TURNAROUND_COST_RESTRUCTURING | 0 | 0 | needs_more_cases |
| 3 | BIOTECH_REGULATORY | 2 | 3 | covered_2x2 |
| 3 | CONSTRUCTION_REAL_ESTATE_CREDIT | 0 | 2 | needs_more_cases |
| 3 | GAME_CONTENT_IP | 1 | 1 | needs_more_cases |
| 3 | GENERIC_UNCLASSIFIED | 0 | 0 | needs_more_counterexamples |
| 3 | HOLDING_RESTRUCTURING_GOVERNANCE | 0 | 3 | needs_more_cases |
| 3 | PLATFORM_SOFTWARE_INTERNET | 2 | 2 | covered_2x2 |
| 3 | RETAIL_DOMESTIC_CONSUMER | 2 | 2 | covered_2x2 |
| 3 | ROBOTICS_FACTORY_AUTOMATION | 0 | 2 | needs_more_cases |
| 3 | UTILITIES_REGULATED_TARIFF | 0 | 2 | needs_more_cases |

## What not to change yet
- Do not apply score weights before case/path coverage is checked.
- Do not lower Stage 3-Green to improve recall.
- Do not use this matrix as candidate-generation input.
- Use it to decide what evidence snapshots, price paths, and counterexamples to add next.
