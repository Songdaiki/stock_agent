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
- source round: `docs/round/round_01.md`

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

There are two priority concepts.

```text
deep-dive priority
-> which archetypes need more case research first

first shadow-scoring candidate
-> which archetypes should be compared first in a future shadow-score run
```

Example:

```text
SHIPBUILDING_OFFSHORE_BACKLOG
-> deep-dive priority 1, because cases are still thin

ONE_OFF_EVENT_DEMAND
-> first shadow-scoring candidate, because it is a guardrail against unsafe Green
```

Deep-dive Priority 1:

- `CONTRACT_BACKLOG_INDUSTRIAL`
- `DEFENSE_GOVERNMENT_BACKLOG`
- `SHIPBUILDING_OFFSHORE_BACKLOG`
- `EXPORT_RECURRING_CONSUMER`
- `K_BEAUTY_EXPORT_DISTRIBUTION`
- `MEMORY_HBM_CAPACITY`
- `SEMI_EQUIPMENT_CAPEX`
- `BATTERY_MATERIALS_CAPEX_OVERHEAT`
- `SHIPPING_FREIGHT_CYCLE`
- `MEDICAL_DEVICE_HEALTHCARE_EXPORT`

First shadow-scoring candidate set:

- `CONTRACT_BACKLOG_INDUSTRIAL`
- `DEFENSE_GOVERNMENT_BACKLOG`
- `EXPORT_RECURRING_CONSUMER`
- `K_BEAUTY_EXPORT_DISTRIBUTION`
- `MEMORY_HBM_CAPACITY`
- `SEMI_EQUIPMENT_CAPEX`
- `SHIPPING_FREIGHT_CYCLE`
- `ONE_OFF_EVENT_DEMAND`
- `THEME_VALUATION_OVERHEAT`
- `FINANCIAL_SPREAD_BALANCE_SHEET`

Legacy matrix priority remains in the report for continuity:

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

## Promotion Bands

The matrix records the reporting bands from `round_01.md`:

```text
Stage 2
Stage 2-High
Stage 3-Watch
Stage 3-Yellow
Stage 3-Green
```

This does not change deterministic Stage classification. It only gives the
operator a cleaner way to see a near-miss.

Example:

```text
deterministic_stage = Stage 2
promotion_band = Stage 3-Watch
```

## Guardrails

- Do not lower Stage 3-Green thresholds to improve recall.
- Do not use benchmark or case labels as evidence.
- Do not use case records for candidate generation.
- Do not treat one-off, cycle, or theme-overheat cases as structural Green.
- Do not implement score weights until case/path coverage is adequate.
