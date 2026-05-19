# Checkpoint 28A Round193 R2 Loop7 AI Semiconductor Price Validation

## Scope

- source_round: `docs/round/round_193.md`
- large_sector: `AI_SEMICONDUCTOR_ELECTRONICS`
- patch_type: calibration/evaluation only
- production_scoring_changed: false
- candidate_generation_input: false
- shadow_weight_only: true
- needs_ohlc_backfill: true

Round193 adds a Korean R2 price-path validation pack. It focuses on HBM equipment, AI chip design-house evidence, Samsung HBM catch-up risk, policy foundry events, AI server PCB overheat risk, and SK Hynix 4B benchmark calibration.

## Files Added

- `src/e2r/sector/round193_r2_loop7_ai_semiconductor_price_validation.py`
- `src/e2r/cli/build_round193_r2_loop7_report.py`
- `tests/test_round193_r2_loop7_ai_semiconductor_price_validation.py`
- `data/e2r_case_library/cases_r2_loop7_round193.jsonl`
- `data/sector_taxonomy/round193_r2_loop7_ai_semiconductor_price_validation_audit.json`
- `output/e2r_round193_r2_loop7_ai_semiconductor_price_validation/`

## Cases Captured

| case | role | stage interpretation |
| --- | --- | --- |
| `hanmi_semiconductor_tsv_tc_bonder_4b_watch` | structural success + 4B-watch | HBM bonder customer/order evidence can support Stage 3 candidate status, but unconfirmed Micron report spike needs 4B-watch |
| `gaonchips_pfn_samsung_2nm_design_win_stage2` | Stage 2 success candidate | design win is strong Stage 2 evidence, but tape-out, volume production, revenue, and margin are needed for Stage 3 |
| `samsung_electronics_hbm_catchup_failed_2025_watch` | failed rerating / watch | 2025 HBM catch-up was not Green because HBM sales and chip profit were weak |
| `db_hitek_policy_foundry_event_premium` | policy event premium | government foundry review is Stage 1/weak Stage 2 attention before orders and revenue |
| `isu_petasis_ai_server_pcb_insufficient_evidence` | overheat / insufficient evidence | AI server PCB narrative is not Green before customer, order, margin, and EPS evidence |
| `sk_hynix_hbm_2026_4b_benchmark` | 4B benchmark | existing success anchor used for 4B timing, not a new Stage 3 case |

## Green Gate Update

Round193 keeps Stage 3-Green strict. Required R2 evidence:

- company-level customer evidence
- order/contract/shipment/design-win quality distinction
- revenue recognition path
- gross margin or OPM improvement
- EPS/FCF revision
- customer diversification or long-term demand
- price path after evidence

Forbidden Green patterns:

- AI name only
- HBM keyword only
- server theme only
- broker target only
- unconfirmed media report
- policy beneficiary only
- stock price moves before evidence
- unknown margin

Simple example: `as_of_date=2024-07-09` and Gaonchips is named in a Samsung 2nm AI-chip design flow. That can be Stage 2. It cannot become Stage 3-Green until tape-out, volume production, revenue recognition, margin, and EPS path are visible by that date.

## 4B / 4C Clarification

Round193 separates:

- `4B-watch`: AI/HBM logic is plausible but price, valuation, or consensus is running ahead
- `4B-elevated`: customer CAPEX, margin, financing, or concentration risk becomes material
- `4B-graduated`: new orders or earnings beats no longer create meaningful rerating
- `benchmark`: already-successful anchor used for timing calibration, not a new Stage 3 candidate
- `4C`: only when qualification failure, order push-out, CAPEX cut, memory price decline, capacity oversupply, prolonged production disruption, accounting trust break, IP leakage, circular financing, or dilution breaks the thesis

Samsung Electronics labor risk is recorded as watch, not hard 4C, until it actually damages production, customers, or EPS/FCF.

## Generated Reports

- `round193_r2_loop7_price_validation_summary.md`
- `round193_r2_loop7_case_matrix.csv`
- `round193_r2_loop7_target_aliases.csv`
- `round193_r2_loop7_score_adjustments.csv`
- `round193_r2_loop7_price_backfill_fields.csv`
- `round193_r2_loop7_green_gate_review.md`
- `round193_r2_loop7_price_backfill_plan.md`
- `round193_r2_loop7_stage4b_4c_review.md`

## Verification

Command run:

```bash
PYTHONPATH=src python -m unittest tests/test_round193_r2_loop7_ai_semiconductor_price_validation.py -v
PYTHONPATH=src python -m e2r.cli.build_round193_r2_loop7_report
```

Result:

- Round193 unit tests passed.
- Round193 reports were generated.
- No production scoring thresholds were changed.
- Case records remain calibration/evaluation material only.

## Next Step

Backfill official OHLC and evidence dates for these six cases, then compare Stage 2/3 anchors against MFE/MAE, HBM basket relative strength, semiconductor equipment basket relative strength, and AI server PCB basket relative strength.
