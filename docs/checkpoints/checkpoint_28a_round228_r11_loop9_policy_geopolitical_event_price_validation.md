# Checkpoint 28A Round 228 R11 Loop 9 Policy Geopolitical Event Price Validation

## Scope

Round 228 was converted into a calibration-only case pack for `POLICY_GEOPOLITICAL_EVENT`.

Production scoring was not changed. The cases are evaluation material only and must not be used as candidate-generation input.

## Files Added

- `src/e2r/sector/round228_r11_loop9_policy_geopolitical_event_price_validation.py`
- `src/e2r/cli/build_round228_r11_loop9_report.py`
- `tests/test_round228_r11_loop9_policy_geopolitical_event_price_validation.py`
- `data/e2r_case_library/cases_r11_loop9_round228.jsonl`
- `data/sector_taxonomy/round228_r11_loop9_policy_geopolitical_event_price_validation_audit.json`
- `output/e2r_round228_r11_loop9_policy_geopolitical_event_price_validation/`

## Case Pack Summary

- cases: 8
- success_candidate: 4
- event_premium: 2
- failed_rerating: 2
- Stage 3 dated cases: 0
- hard 4C confirmed cases: 0
- default Stage 3 bias: very conservative
- full OHLC complete: false
- shadow weight only: true

## Key Interpretation

- Commercial Act reform is positive market-structure Stage 2, but company-level Green needs actual treasury-share cancellation, payout, ROE/EPS, and FCF.
- Tax-policy shock is a policy-confidence 4C-watch, not positive evidence.
- U.S.-Korea tariff relief is macro Stage 2, while $350B investment pledge and FX outflow remain watch items.
- Hyundai Steel U.S. CAPEX shows policy-induced tariff hedge can fail when funding, margin, and ROI are unclear.
- Semiconductor support and fiscal stimulus are Stage 1/2 policy support, not company Green.
- POSCO International Alaska LNG offtake is stronger than headline policy because it is a 20-year offtake, but FID, pricing, margin, and cashflow still gate Green.
- Korea Gas East Sea event is the clean `price_moved_without_evidence` example: +30% before drilling or commerciality.

Easy example: `정부 지원 package + 관련주 급등`은 Stage 1/2 관심 이벤트입니다. `지원 package + 실제 발주 + financing + 매출 인식 + EPS/FCF revision`까지 이어져야 더 높은 Stage 검토가 가능합니다.

## Green Guardrails

Round 228 requires:

- policy/event escalated to company-level contract
- contract amount or funded budget confirmed
- financing or FID confirmed
- actual order or procurement award
- revenue recognition path visible
- margin or EPS/FCF revision visible
- repeat demand, not event fade
- policy reversal and macro FX risk passed
- price path after evidence

Round 228 blocks Green from:

- policy news only
- MOU only
- geopolitical headline only
- resource estimate without drilling
- fiscal stimulus without revenue conversion
- support package without order
- energy-security headline only
- CAPEX for tariff without funding
- tax-policy surprise
- macro FX outflow risk
- price rally before commerciality

## Verification

Commands run:

```bash
PYTHONPATH=src python -m unittest tests.test_round228_r11_loop9_policy_geopolitical_event_price_validation -v
PYTHONPATH=src python -m e2r.cli.build_round228_r11_loop9_report
```

Result:

- Round 228 targeted tests passed.
- Round 228 case library, audit JSON, CSV matrices, deep-sub-archetype map, shadow weights, green-gate review, price-validation plan, and 4B/4C review were generated.
