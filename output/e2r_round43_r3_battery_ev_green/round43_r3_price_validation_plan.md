# Round-43 R3 Price Validation Plan

## Method

1. Assign stage dates from source evidence only.
2. Store stage-date close prices from official price data.
3. Calculate MFE_30D / 90D / 180D / 1Y / 2Y.
4. Calculate MAE_30D / 90D / 180D / 1Y.
5. Calculate peak price, drawdown after peak, and below-stage3 flag.
6. Compare price paths with OP/EPS revision, utilization, CAPEX, FCF, mineral prices, subsidy/tariff events, and project-break evidence.

## Priority Case Checks

| case_id | stage candidate | check |
| --- | --- | --- |
| `lg_energy_solution_ess_shift_case` | 2025-07-25 | needs_price_backfill |
| `gm_lg_ultium_ohio_ev_slowdown_case` | 2026-05-12 | needs_price_backfill |
| `hyundai_hydrogen_fuel_cell_plant_case` | 2025-10-30 | needs_price_backfill |
| `eqt_kj_environment_waste_platform_case` | 2024-08-16 | missing_public_price_data |
| `eu_ets_cbam_policy_case` | 2026-05-12 | missing_direct_symbol_mapping |
| `qcells_customs_detention_case` | 2025-11-08 | missing_public_price_data |
| `qcells_china_linked_solar_policy_case` | 2026-05-08 | missing_public_price_data |
| `orsted_sunrise_wind_impairment_case` | 2025-01-20 | needs_price_backfill |
| `lithium_price_86pct_crash_case` | 2025-01-13 | missing_price_data |
| `albemarle_cost_cut_low_lithium_case` | 2025-02-12 | needs_price_backfill |

## Alignment Labels

- `aligned`: contracts, utilization, margin, FCF, and price rerating persist together.
- `cyclical_success`: mineral or energy cycle helped price, but structural durability is not proven.
- `event_premium`: subsidy, policy, plant, MOU, or factory news moved attention without revenue conversion.
- `false_positive_score`: growth-theme evidence looked strong, but demand, CAPEX, margin, or FCF failed.
- `thesis_break`: plant idle, worker furlough, customs detention, impairment, or mineral-price crash damages the thesis.
