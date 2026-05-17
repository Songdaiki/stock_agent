# Round-51 R11 Price Validation Plan

## Method

1. Assign stage dates from source evidence only.
2. Store event-date close prices from official price data.
3. Calculate MFE_5D / 20D / 60D / 90D / 180D and matching MAE windows.
4. Compare price moves with contract, order, budget, replication, demand-normalization, and project-financing fields.
5. Mark price-only rallies as event premium or 4B-watch rather than structural success.

## Priority Case Checks

| case_id | stage candidate | check |
| --- | --- | --- |
| `bavarian_nordic_us_stockpile_contract_case` | 2026-05-11 | needs_price_backfill |
| `bavarian_nordic_mpox_emergency_case` | 2024-08-16 | needs_price_backfill |
| `ukraine_swiss_reconstruction_projects_case` | 2025-08-28 | needs_price_backfill |
| `ukraine_telecom_ebrd_ifc_case` | 2024-10-10 | needs_price_backfill |
| `north_korea_kumgang_dismantle_case` | 2025-02-13 | needs_price_backfill |
| `lk99_superconductor_theme_case` | 2023-08-01 | needs_price_backfill |
| `lk99_replication_failure_case` | 2023-08-08 | needs_price_backfill |
| `covid_diagnostics_demand_wane_case` | 2025-10-15 | needs_price_backfill |

## Alignment Labels

- `event_to_contract_stockpile_candidate`: event demand is backed by a government stockpile contract, but still needs recurrence and margin checks.
- `funded_reconstruction_reference_candidate`: project financing exists; company-level contract and margin proof still decide scoring.
- `price_moved_without_technical_or_revenue_evidence`: science or policy theme moved before technical/customer/revenue evidence.
- `speculative_science_thesis_break`: replication failure or no commercialization breaks the thesis.
- `one_off_diagnostic_demand_normalized`: event diagnostics revenue fell after temporary demand normalized.
