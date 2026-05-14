# Round-3 Case Coverage Summary

| rank | archetype | posture | positives | counterexamples | status |
|---:|---|---|---:|---:|---|
| 1 | CONTRACT_BACKLOG_INDUSTRIAL | GREEN_ELIGIBLE | 3 | 1 | needs_more_cases |
| 2 | DEFENSE_GOVERNMENT_BACKLOG | GREEN_ELIGIBLE | 1 | 1 | needs_more_cases |
| 3 | SHIPBUILDING_OFFSHORE_BACKLOG | GREEN_ELIGIBLE | 1 | 1 | needs_more_cases |
| 4 | EXPORT_RECURRING_CONSUMER | GREEN_ELIGIBLE | 1 | 2 | needs_more_cases |
| 5 | K_BEAUTY_EXPORT_DISTRIBUTION | GREEN_ELIGIBLE | 2 | 2 | covered_2x2 |
| 6 | MEMORY_HBM_CAPACITY | GREEN_ELIGIBLE | 2 | 2 | covered_2x2 |
| 7 | SEMI_EQUIPMENT_CAPEX | GREEN_ELIGIBLE | 1 | 1 | needs_more_cases |
| 8 | FINANCIAL_SPREAD_BALANCE_SHEET | GREEN_ELIGIBLE | 0 | 2 | needs_more_cases |
| 9 | MEDICAL_DEVICE_HEALTHCARE_EXPORT | GREEN_ELIGIBLE | 1 | 2 | needs_more_cases |
| 10 | THEME_VALUATION_OVERHEAT | RED_4B_GUARDRAIL | 0 | 1 | needs_more_cases |
| 11 | ONE_OFF_EVENT_DEMAND | RED_4B_GUARDRAIL | 0 | 1 | needs_more_cases |
| 12 | AI_DATA_CENTER_INFRASTRUCTURE | GREEN_ELIGIBLE | 2 | 1 | needs_more_cases |
| 13 | ROBOTICS_FACTORY_AUTOMATION | YELLOW_WATCH | 0 | 2 | needs_more_cases |
| 14 | PLATFORM_SOFTWARE_INTERNET | YELLOW_WATCH | 2 | 2 | covered_2x2 |
| 15 | GAME_CONTENT_IP | YELLOW_WATCH | 1 | 1 | needs_more_cases |
| 16 | SHIPPING_FREIGHT_CYCLE | RED_4B_GUARDRAIL | 1 | 1 | needs_more_cases |
| 17 | CONSTRUCTION_REAL_ESTATE_CREDIT | RED_4B_GUARDRAIL | 0 | 2 | guardrail_counterexamples_present |
| 18 | UTILITIES_REGULATED_TARIFF | YELLOW_WATCH | 0 | 0 | needs_more_cases |
| 19 | NUCLEAR_SMR_GRID_POLICY | YELLOW_WATCH | 0 | 2 | needs_more_cases |
| 20 | HOLDING_RESTRUCTURING_GOVERNANCE | YELLOW_WATCH | 0 | 3 | needs_more_cases |
| 21 | TRAVEL_LEISURE_REOPENING | YELLOW_WATCH | 1 | 1 | needs_more_cases |
| 22 | BIOTECH_REGULATORY | RED_4B_GUARDRAIL | 0 | 0 | needs_more_cases |
| 23 | RARE_METALS_STRATEGIC_MATERIALS | YELLOW_WATCH | 0 | 0 | needs_more_cases |
| 24 | RETAIL_DOMESTIC_CONSUMER | YELLOW_WATCH | 0 | 0 | needs_more_cases |

## Interpretation
- A `covered_2x2` row can later be used for shadow-score experiments.
- `needs_more_cases` means do not apply score-weight changes.
- Guardrail archetypes can be useful even before positives are complete, because they block unsafe Green.
