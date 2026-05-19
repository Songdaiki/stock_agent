# Checkpoint 28A Round 226 R9 Loop 9 Mobility Transport Leisure Price Validation

## Scope

Round 226 was converted into a calibration-only case pack for `MOBILITY_TRANSPORT_LEISURE`.

Production scoring was not changed. The cases are evaluation material only and must not be used as candidate-generation input.

## Files Added

- `src/e2r/sector/round226_r9_loop9_mobility_transport_leisure_price_validation.py`
- `src/e2r/cli/build_round226_r9_loop9_report.py`
- `tests/test_round226_r9_loop9_mobility_transport_leisure_price_validation.py`
- `data/e2r_case_library/cases_r9_loop9_round226.jsonl`
- `data/sector_taxonomy/round226_r9_loop9_mobility_transport_leisure_price_validation_audit.json`
- `output/e2r_round226_r9_loop9_mobility_transport_leisure_price_validation/`

## Case Pack Summary

- cases: 8
- success_candidate: 3
- event_premium: 2
- failed_rerating: 1
- cyclical_success: 1
- Stage 3 dated cases: 0
- hard 4C confirmed cases: 1
- full OHLC complete: false
- shadow weight only: true

## Key Interpretation

- 현대차 is a hybrid/value-up Stage 2 watch, but tariff cost adds 4C-watch.
- 기아 and CJ대한통운 show why useful evidence can still fail promotion when SDV delay, capex, margin, or price confirmation is weak.
- 대한항공 is integration scale watch, while 제주항공 is a hard safety/trust 4C example.
- HMM is cyclical success, not structural Green.
- Hotel Shilla/Paradise and Lotte Tour/Yellow Balloon are event premium until tourist spend, utilization, drop/hold, OPM, and FCF confirm.

Easy example: `중국 무비자 정책 + 당일 관광주 급등` is Stage 2/event premium. `정책 + 실제 관광객 소비 + 면세 매출 + casino drop/hold + OPM + FCF` is the bundle that can support deeper Stage review.

## Green Guardrails

Round 226 requires:

- unit economics
- FCF after capex
- margin durability
- hybrid mix / load factor / freight contract / tourist spend evidence
- shareholder return or deleveraging
- safety and operational trust passed
- tariff / fuel / FX / freight normalization stress passed
- price path after evidence

Round 226 blocks Green from:

- travel reopening only
- freight-rate spike only
- robotaxi or SDV story only
- tourist arrival policy only
- tourism redirect event only
- merger completion without synergy
- EV or AI mobility theme only
- capex-heavy localization without margin
- fatal safety accident
- margin guidance cut

## Verification

Commands run:

```bash
PYTHONPATH=src python -m unittest tests.test_round226_r9_loop9_mobility_transport_leisure_price_validation -v
PYTHONPATH=src python -m e2r.cli.build_round226_r9_loop9_report
```

Result:

- Round 226 targeted tests passed.
- Round 226 case library, audit JSON, CSV matrices, shadow weights, green-gate review, price-validation plan, and 4B/4C review were generated.
