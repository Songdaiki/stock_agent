# Checkpoint 28A Round 101 R9 Loop 5 Mobility / Transport / Leisure

## Summary

Round 101 applies the R9 Loop 5 mobility, transport, and leisure research pack.
This is calibration/evaluation material only. It does not change production scoring, StageClassifier thresholds, or candidate generation.

The core rule is simple:

- `demand recovery` is not Green evidence by itself.
- `hybrid` is not Green evidence without OPM, FCF, and capital-return execution.
- `robotaxi` or `autonomous trucking` launch is not Green evidence without unit economics and safety.
- `tourism policy` and `freight rate spike` are not structural evidence until spend, margin, and cycle durability are verified.

Example: a driverless truck can complete a paid route and still remain Watch if cost per mile, insurance, remote support, utilization, and repeat customer data are missing.

## Implemented Files

- `src/e2r/sector/round101_r9_loop5_mobility_transport_leisure.py`
- `src/e2r/cli/build_round101_r9_loop5_report.py`
- `tests/test_round101_r9_loop5_mobility_transport_leisure.py`
- `data/e2r_case_library/cases_r9_loop5_round101.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round101_r9_loop5_v5.csv`
- `output/e2r_round101_r9_loop5_mobility_transport_leisure/`

## Archetype Counts

- target_count: 28
- case_candidate_count: 18
- structural_success_count: 0
- success_candidate_count: 7
- cyclical_success_count: 1
- event_premium_count: 2
- stage4b_case_count: 9
- stage4c_case_count: 7
- green_possible_count: 2
- watch_yellow_first_count: 15
- redteam_first_count: 11
- gate_only_target_count: 7

## New / Confirmed Archetypes

- `AUTONOMOUS_TRUCKING_COMMERCIAL_LAUNCH`
- `AUTONOMOUS_TRUCKING_UNIT_ECONOMICS`
- `DISCLOSURE_CONFIDENCE_CAP`

`DISCLOSURE_CONFIDENCE_CAP` is cap-only, not gate-only. Missing fleet size, freight rate, certification detail, contract term, or unit-economics detail should cap Stage 3 confidence until verified.

## Key Case Splits

- Hyundai hybrid value-up remains Green-eligible only with hybrid mix, OPM, FCF, and shareholder-return execution.
- Hyundai US localization is Watch because tariff mitigation can still lower OPM and raise CAPEX burden.
- Toyota hybrid bottleneck is separated from generic auto parts and needs delivery, margin, and cost pass-through.
- Uber/Avride and Hyundai IONIQ 5 robotaxi cases are Stage 2 candidates, not Green, until ride volume, utilization, safety, and cost per mile are verified.
- Tesla wait-time and Waymo flooded-road recall remain robotaxi operational and safety RedTeam examples.
- Aurora driverless trucking is a Stage 2 candidate, but `AUTONOMOUS_TRUCKING_UNIT_ECONOMICS` gates Stage 3 until cost, utilization, insurance, and remote support are visible.
- Korean Air/Asiana integration remains cyclical/watch because fuel, FX, cargo cycle, and integration cost can reverse the thesis.
- China group visa tourism remains event premium until spend, casino drop amount, duty-free ASP, RevPAR, and OPM are verified.
- Shipping freight cycle remains Red/Watch because overcapacity and spot-rate collapse can create hard 4C.
- Hertz EV rental, Joby/Lilium/Archer eVTOL, and Michelin demand cuts remain unit-economics, cash-burn, certification, and demand-break counterexamples.
- SES satellite connectivity is Green-eligible only with recurring connectivity revenue, backlog, capex/debt control, and customer contract durability.

## Guardrails

- Do not use case records as candidate-generation input.
- Do not apply Round 101 v5.0 score weights to production scoring yet.
- Do not invent OPM, FCF, tariff cost, freight rate, casino drop, fleet utilization, cost per mile, certification, backlog, or stage-price fields.
- Do not treat demand recovery, hybrid labels, tourism policy, freight spikes, robotaxi launch, autonomous trucking launch, eVTOL milestone, or space theme as Green evidence alone.
- Require cross-evidence before higher conviction: price path, financials, operational metrics, safety/regulatory record, and source-detail confidence.

## Verification

Commands run:

```bash
PYTHONPATH=src python -m unittest tests.test_round101_r9_loop5_mobility_transport_leisure -v
PYTHONPATH=src python -m e2r.cli.build_round101_r9_loop5_report
```

Both completed successfully before the full repository test run.
