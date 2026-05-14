# Round-2 Case Mining Priorities

Source rounds: `docs/round/round_01.md`, `docs/round/round_02.md`

There are two priority concepts:

- deep-dive priority: where the case matrix should be expanded first
- first shadow-scoring candidate: where shadow weights can be compared first after coverage improves

| current priority | deep-dive priority | first shadow? | archetype | positive | counterexamples | status |
|---:|---:|---|---|---:|---:|---|
| 1 | 1 | yes | CONTRACT_BACKLOG_INDUSTRIAL | 3 | 1 | needs_more_cases |
| 1 | 1 | yes | DEFENSE_GOVERNMENT_BACKLOG | 1 | 1 | needs_more_cases |
| 1 | 1 | yes | EXPORT_RECURRING_CONSUMER | 1 | 2 | needs_more_cases |
| 1 | 1 | yes | K_BEAUTY_EXPORT_DISTRIBUTION | 2 | 2 | covered_2x2 |
| 1 | 1 | yes | MEMORY_HBM_CAPACITY | 2 | 2 | covered_2x2 |
| 1 | 1 | yes | SHIPPING_FREIGHT_CYCLE | 1 | 1 | needs_more_cases |
| 2 | 1 | no | BATTERY_MATERIALS_CAPEX_OVERHEAT | 0 | 2 | needs_more_cases |
| 2 | 1 | no | MEDICAL_DEVICE_HEALTHCARE_EXPORT | 2 | 3 | covered_2x2 |
| 2 | 1 | yes | SEMI_EQUIPMENT_CAPEX | 3 | 2 | covered_2x2 |
| 2 | 1 | no | SHIPBUILDING_OFFSHORE_BACKLOG | 1 | 1 | needs_more_cases |
| 2 | 2 | no | AUTO_MOBILITY_COMPONENTS | 0 | 0 | needs_more_cases |
| 2 | 2 | yes | FINANCIAL_SPREAD_BALANCE_SHEET | 0 | 5 | needs_more_cases |
| 2 | 2 | no | TURNAROUND_COST_RESTRUCTURING | 0 | 0 | needs_more_cases |
| 3 | 2 | no | BIOTECH_REGULATORY | 2 | 3 | covered_2x2 |
| 3 | 2 | no | GAME_CONTENT_IP | 1 | 1 | needs_more_cases |
| 3 | 2 | no | HOLDING_RESTRUCTURING_GOVERNANCE | 0 | 3 | needs_more_cases |
| 3 | 2 | no | PLATFORM_SOFTWARE_INTERNET | 2 | 2 | covered_2x2 |
| 1 | 3 | yes | ONE_OFF_EVENT_DEMAND | 0 | 1 | needs_more_counterexamples |
| 1 | 3 | yes | THEME_VALUATION_OVERHEAT | 0 | 1 | needs_more_counterexamples |
| 2 | 3 | no | COMMODITY_SPREAD | 1 | 1 | needs_more_cases |
| 3 | 3 | no | CONSTRUCTION_REAL_ESTATE_CREDIT | 0 | 2 | needs_more_cases |
| 3 | 3 | no | GENERIC_UNCLASSIFIED | 0 | 0 | needs_more_counterexamples |
| 3 | 3 | no | RETAIL_DOMESTIC_CONSUMER | 2 | 2 | covered_2x2 |
| 3 | 3 | no | ROBOTICS_FACTORY_AUTOMATION | 0 | 2 | needs_more_cases |
| 3 | 3 | no | UTILITIES_REGULATED_TARIFF | 0 | 2 | needs_more_cases |

## Deep-Dive Priority Groups
- Priority 1: CONTRACT_BACKLOG_INDUSTRIAL, DEFENSE_GOVERNMENT_BACKLOG, SHIPBUILDING_OFFSHORE_BACKLOG, EXPORT_RECURRING_CONSUMER, K_BEAUTY_EXPORT_DISTRIBUTION, MEMORY_HBM_CAPACITY, SEMI_EQUIPMENT_CAPEX, BATTERY_MATERIALS_CAPEX_OVERHEAT, SHIPPING_FREIGHT_CYCLE, MEDICAL_DEVICE_HEALTHCARE_EXPORT
- Priority 2: AUTO_MOBILITY_COMPONENTS, FINANCIAL_SPREAD_BALANCE_SHEET, HOLDING_RESTRUCTURING_GOVERNANCE, TURNAROUND_COST_RESTRUCTURING, GAME_CONTENT_IP, PLATFORM_SOFTWARE_INTERNET, BIOTECH_REGULATORY
- Priority 3: CONSTRUCTION_REAL_ESTATE_CREDIT, UTILITIES_REGULATED_TARIFF, RETAIL_DOMESTIC_CONSUMER, ROBOTICS_FACTORY_AUTOMATION, COMMODITY_SPREAD, ONE_OFF_EVENT_DEMAND, THEME_VALUATION_OVERHEAT, GENERIC_UNCLASSIFIED

## First Shadow-Scoring Candidate Set
CONTRACT_BACKLOG_INDUSTRIAL, DEFENSE_GOVERNMENT_BACKLOG, EXPORT_RECURRING_CONSUMER, K_BEAUTY_EXPORT_DISTRIBUTION, MEMORY_HBM_CAPACITY, SEMI_EQUIPMENT_CAPEX, SHIPPING_FREIGHT_CYCLE, ONE_OFF_EVENT_DEMAND, THEME_VALUATION_OVERHEAT, FINANCIAL_SPREAD_BALANCE_SHEET

## Promotion Band Reminder
Stage 2, Stage 2-High, Stage 3-Watch, Stage 3-Yellow, Stage 3-Green

A strong candidate can remain deterministic Stage 2 while being reported as Stage 3-Watch.
Example: HD/Iljin-style cases can show `deterministic_stage=Stage 2` and `promotion_band=Stage 3-Watch` until Green evidence is complete.

Round 2 also adds price-pattern labels. Example: a shipping case can be `CYCLE_SPIKE_NORMALIZATION`, while SMCI-like cases can be `ACCOUNTING_TRUST_COLLAPSE`.

## What not to change yet
- Do not apply score weights before case/path coverage is checked.
- Do not lower Stage 3-Green to improve recall.
- Do not use this matrix as candidate-generation input.
- Use it to decide what evidence snapshots, price paths, and counterexamples to add next.
