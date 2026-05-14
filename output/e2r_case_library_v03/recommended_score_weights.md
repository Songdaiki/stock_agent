# Recommended Score Weights

These are design recommendations only. They are not applied to scoring in Checkpoint 28A.

| archetype | status | recommended emphasis | do not implement yet? |
|---|---|---|---|
| CONTRACT_BACKLOG_INDUSTRIAL | insufficient_case_coverage | earnings_visibility=24, bottleneck_pricing=22, eps_fcf_explosion=20 | yes |
| DEFENSE_GOVERNMENT_BACKLOG | insufficient_case_coverage | earnings_visibility=24, eps_fcf_explosion=20, bottleneck_pricing=17 | yes |
| SHIPBUILDING_OFFSHORE_BACKLOG | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| EXPORT_RECURRING_CONSUMER | insufficient_case_coverage | earnings_visibility=23, eps_fcf_explosion=22, market_mispricing=16 | yes |
| K_BEAUTY_EXPORT_DISTRIBUTION | covered | earnings_visibility=23, eps_fcf_explosion=22, market_mispricing=16 | no |
| MEMORY_HBM_CAPACITY | covered | eps_fcf_explosion=24, earnings_visibility=21, bottleneck_pricing=19 | no |
| SEMI_EQUIPMENT_CAPEX | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| BATTERY_MATERIALS_CAPEX_OVERHEAT | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| COMMODITY_SPREAD | covered | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | no |
| SHIPPING_FREIGHT_CYCLE | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| AUTO_MOBILITY_COMPONENTS | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| AUTO_MOBILITY_COMPLETED_VEHICLE | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| ROBOTICS_FACTORY_AUTOMATION | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| AI_DATA_CENTER_INFRASTRUCTURE | insufficient_case_coverage | eps_fcf_explosion=22, earnings_visibility=22, bottleneck_pricing=21 | yes |
| NUCLEAR_SMR_GRID_POLICY | insufficient_case_coverage | earnings_visibility=24, eps_fcf_explosion=18, market_mispricing=15 | yes |
| TRAVEL_LEISURE_REOPENING | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| EDUCATION_SPECIALTY_SERVICES | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| RARE_METALS_STRATEGIC_MATERIALS | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| VALUE_UP_SHAREHOLDER_RETURN | insufficient_case_coverage | market_mispricing=24, valuation_rerating=20, earnings_visibility=19 | yes |
| PLATFORM_SOFTWARE_INTERNET | covered | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | no |
| GAME_CONTENT_IP | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| FINANCIAL_SPREAD_BALANCE_SHEET | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| BIOTECH_REGULATORY | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| BIOTECH_PRE_REVENUE_REGULATORY | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| BIOTECH_ROYALTY_COMMERCIALIZATION | insufficient_case_coverage | earnings_visibility=23, market_mispricing=18, eps_fcf_explosion=15 | yes |
| CDMO_HEALTHCARE_CONTRACT | covered | earnings_visibility=24, eps_fcf_explosion=20, bottleneck_pricing=16 | no |
| MEDICAL_DEVICE_HEALTHCARE_EXPORT | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| RETAIL_DOMESTIC_CONSUMER | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| CONSTRUCTION_REAL_ESTATE_CREDIT | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| UTILITIES_REGULATED_TARIFF | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| HOLDING_RESTRUCTURING_GOVERNANCE | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| TURNAROUND_COST_RESTRUCTURING | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |
| ONE_OFF_EVENT_DEMAND | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=8, bottleneck_pricing=8 | yes |
| THEME_VALUATION_OVERHEAT | insufficient_case_coverage | eps_fcf_explosion=18, earnings_visibility=8, bottleneck_pricing=8 | yes |
| GENERIC_UNCLASSIFIED | insufficient_case_coverage | eps_fcf_explosion=20, earnings_visibility=20, bottleneck_pricing=15 | yes |

## What not to do
- Do not lower Stage 3-Green thresholds just to increase recall.
- Do not use case labels as evidence.
- Do not implement final archetype weights where case coverage is insufficient.
