# E2R Archetype Matrix Round 2

This document records the analyst's second matrix before production scoring
changes.

The point is simple:

```text
Sector name is not enough.
The system must learn which structure turns into durable EPS/FCF change.
```

Example:

```text
Power equipment:
contract + backlog + lead time + CAPA + ASP

K-food:
export channel + repeat demand + ASP/OPM + FY1/FY2 revision

Memory/HBM:
HBM demand + pricing + supply discipline + capacity bottleneck + medium-term revision
```

So the repo now has a Round-2 playbook layer:

- `src/e2r/sector/archetype_matrix.py`
- `src/e2r/cli/build_round2_archetype_matrix_report.py`
- `output/e2r_archetype_matrix/*`

## What This Is

This is calibration material:

- stage criteria by archetype
- success and counterexample targets
- draft score weights
- Green gate policy
- peer-normalization metrics
- case coverage gaps

## What This Is Not

This is not production scoring.

The following modules must not import it:

- `features.py`
- `staging.py`
- `red_team.py`
- production pipeline modules
- live/web research modules

## Round-2 Priority

Priority 1:

- `CONTRACT_BACKLOG_INDUSTRIAL`
- `DEFENSE_GOVERNMENT_BACKLOG`
- `EXPORT_RECURRING_CONSUMER`
- `K_BEAUTY_EXPORT_DISTRIBUTION`
- `MEMORY_HBM_CAPACITY`
- `ONE_OFF_EVENT_DEMAND`
- `THEME_VALUATION_OVERHEAT`
- `SHIPPING_FREIGHT_CYCLE`

Priority 2:

- `SHIPBUILDING_OFFSHORE_BACKLOG`
- `SEMI_EQUIPMENT_CAPEX`
- `BATTERY_MATERIALS_CAPEX_OVERHEAT`
- `MEDICAL_DEVICE_HEALTHCARE_EXPORT`
- `FINANCIAL_SPREAD_BALANCE_SHEET`
- `TURNAROUND_COST_RESTRUCTURING`
- `AUTO_MOBILITY_COMPONENTS`

Priority 3:

- `PLATFORM_SOFTWARE_INTERNET`
- `GAME_CONTENT_IP`
- `BIOTECH_REGULATORY`
- `CONSTRUCTION_REAL_ESTATE_CREDIT`
- `UTILITIES_REGULATED_TARIFF`
- `HOLDING_RESTRUCTURING_GOVERNANCE`
- `RETAIL_DOMESTIC_CONSUMER`
- `ROBOTICS_FACTORY_AUTOMATION`
- `GENERIC_UNCLASSIFIED`

## Guardrails

- Do not lower Stage 3-Green thresholds to improve recall.
- Do not use benchmark or case labels as evidence.
- Do not use case records for candidate generation.
- Do not treat one-off, cycle, or theme-overheat cases as structural Green.
- Do not implement score weights until case/path coverage is adequate.

