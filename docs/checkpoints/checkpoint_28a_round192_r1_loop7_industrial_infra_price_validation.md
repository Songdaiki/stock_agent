# Checkpoint 28A Round192 R1 Loop7 Industrial Infra Price Validation

## Scope

- source_round: `docs/round/round_192.md`
- large_sector: `INDUSTRIAL_ORDERS_INFRA`
- patch_type: calibration/evaluation only
- production_scoring_changed: false
- candidate_generation_input: false
- shadow_weight_only: true
- needs_ohlc_backfill: true

Round192 adds a Korean R1 price-path validation pack. It focuses on defense export, shipbuilding backlog, ship MRO, IPO price-only rally, 4B timing, and hard 4C separation.

## Files Added

- `src/e2r/sector/round192_r1_loop7_industrial_infra_price_validation.py`
- `src/e2r/cli/build_round192_r1_loop7_report.py`
- `tests/test_round192_r1_loop7_industrial_infra_price_validation.py`
- `data/e2r_case_library/cases_r1_loop7_round192.jsonl`
- `data/sector_taxonomy/round192_r1_loop7_industrial_infra_price_validation_audit.json`
- `output/e2r_round192_r1_loop7_industrial_infra_price_validation/`

## Cases Captured

| case | role | stage interpretation |
| --- | --- | --- |
| `hyundai_rotem_k2_export_price_path` | structural success | Stage 2 anchor exists; Stage 3 needs delivery/revenue/OP confirmation and OHLC backfill |
| `lig_nex1_msami_iraq_combat_validation` | success candidate | Stage 2 contract; Green waits for backlog, margin, EPS, and delivery visibility |
| `hanwha_aerospace_poland_chunmoo_4b_timing` | structural success + 4B timing | 2025 dilution shock is 4B-elevated, not hard 4C while backlog/guidance survive |
| `samsung_heavy_shipbuilding_contract_stage2_not_green` | Stage 2 not Green | contract amount alone is not enough for Stage 3 |
| `hd_hyundai_marine_solution_ipo_price_only_rally` | event premium | IPO first-day rally is price-only, not Stage 3 evidence |
| `kai_fa50_philippines_stage2_watch` | Stage 2 watch | contract exists, but bodyweight change is not yet proven |
| `hanwha_ocean_sanction_watch_not_hard_4c` | sanction watch | policy/geopolitical shock exists, but hard 4C is not confirmed |

## Green Gate Update

Round192 keeps the same principle: do not lower Stage 3-Green. It records stricter R1 Green evidence requirements:

- contract amount to prior sales
- contract duration
- delivery schedule
- customer or government budget/financing
- backlog growth
- OPM or EPS revision
- price path after evidence

Forbidden Green patterns:

- order headline only
- unknown margin
- unknown delivery schedule
- unknown financing condition
- IPO or supply-demand price spike
- price moves before evidence

Simple example: `as_of_date=2024-07-01` and a 1.438 trillion KRW shipbuilding contract is visible. That can justify Stage 2. It cannot justify Stage 3-Green unless margin, delivery quality, EPS/FCF revision, and price-path confirmation are also visible by that date.

## 4B / 4C Clarification

Round192 separates:

- `4B-watch`: late-cycle price/valuation/crowding watch
- `4B-elevated`: dilution/capex burden appears, but backlog/EPS thesis remains alive
- `4B-graduated`: rerating is broadly accepted and new contracts no longer surprise
- `sanction_watch`: policy/geopolitical shock exists but thesis break is not confirmed
- `4C`: only when contract cancellation, financing failure, budget cut, delivery failure, margin collapse, EPS/FCF downshift, or disclosure/accounting trust break is confirmed

This matters because Hanwha Aerospace's dilution event is a 4B-elevated example, not an automatic hard 4C.

## Generated Reports

- `round192_r1_loop7_price_validation_summary.md`
- `round192_r1_loop7_case_matrix.csv`
- `round192_r1_loop7_target_aliases.csv`
- `round192_r1_loop7_score_adjustments.csv`
- `round192_r1_loop7_price_backfill_fields.csv`
- `round192_r1_loop7_green_gate_review.md`
- `round192_r1_loop7_price_backfill_plan.md`
- `round192_r1_loop7_stage4b_4c_review.md`

## Verification

Command run:

```bash
PYTHONPATH=src python -m unittest tests/test_round192_r1_loop7_industrial_infra_price_validation.py -v
PYTHONPATH=src python -m e2r.cli.build_round192_r1_loop7_report
```

Result:

- Round192 unit tests passed.
- Round192 reports were generated.
- No production scoring thresholds were changed.
- Case records remain calibration/evaluation material only.

## Next Step

Backfill official OHLC for these seven cases, then compare Stage 2/3 anchors against MFE/MAE and relative strength baskets. Only after that should any R1 shadow-weight experiment be considered.
