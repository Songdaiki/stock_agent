# Checkpoint 28A Round 180: R9 Loop 11 Mobility / Transport / Leisure

## Scope

Round 180 adds the Korea-focused R9 Loop 11 mobility, transport, and leisure
case pack. This is calibration material only, not production scoring.

Included areas:

- completed vehicle hybrid localization and SDV/capex risk
- auto-parts restructuring and quality/recall risk
- e-commerce logistics repeat contracts and parcel unit economics
- casino/duty-free/tourism policy events and return-visitor economics
- airline safety hard gates
- Korea shipping freight cycle cooling
- travel-agency policy event caps
- disclosure confidence caps for missing contract, freight, drop, OPM, and unit-economics detail

## Key Principle

R9 headlines are not Stage 3 evidence by themselves.

Example:

- `기아 하이브리드 미국 현지생산` can support Stage 2.
- But `SDV 지연`, `EV 목표 하향`, `CAPEX 증가`, `유럽 가격경쟁` are RedTeam inputs.
- Therefore Green waits for OPM/FCF, tariff-cost absorption, and price-path support.

Another example:

- `중국 단체관광 무비자` can move Hotel Shilla, Paradise, GKL, and Lotte Tour prices.
- But Stage 3 waits for visitor spend, casino drop, hold rate, RevPAR, and OPM/FCF.

## Files Added

- `src/e2r/sector/round180_r9_loop11_mobility_transport_leisure.py`
- `src/e2r/cli/build_round180_r9_loop11_report.py`
- `tests/test_round180_r9_loop11_mobility_transport_leisure.py`
- `data/e2r_case_library/cases_r9_loop11_round180.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round180_r9_loop11_v11.csv`
- `output/e2r_round180_r9_loop11_mobility_transport_leisure/`

## Canonical Targets

Round 180 adds 14 R9 Loop 11 targets:

- `AUTO_HYBRID_LOCALIZATION_KOREA`
- `AUTO_SDV_DELAY_CAPEX_OVERLAY`
- `AUTO_PRICE_WAR_EUROPE_OVERLAY`
- `AUTO_COMPONENT_RESTRUCTURING_KOREA`
- `AUTO_COMPONENT_QUALITY_RECALL_OVERLAY`
- `ECOMMERCE_LOGISTICS_REPEAT_CONTRACT`
- `LOGISTICS_LABOR_REGULATION_OVERLAY`
- `CASINO_DUTYFREE_TOURISM_POLICY_KOREA`
- `CASINO_RETURN_VISITOR_UNIT_ECONOMICS`
- `AIRLINE_SAFETY_REGULATORY_OVERLAY`
- `SHIPPING_FREIGHT_CYCLE_KOREA`
- `PARCEL_VOLUME_PRICE_COST_SPREAD`
- `TRAVEL_AGENCY_POLICY_EVENT`
- `DISCLOSURE_CONFIDENCE_CAP`

## Guardrails

- Do not use Round 180 case records as candidate-generation input.
- Do not apply these weights to production scoring yet.
- Do not treat hybrid, localization, tourism, freight, parcel volume, casino, or duty-free headlines as Green evidence alone.
- Do not fabricate contract amount, freight rate, casino drop, OPM, FCF, unit economics, stage prices, or MFE/MAE.
- Safety accident, recall, warranty cost, labor regulation, price war, freight overcapacity, weak spend/drop, and low disclosure confidence remain RedTeam gates.

## Output Interpretation

Generated reports under `output/e2r_round180_r9_loop11_mobility_transport_leisure/` explain:

- the R9 stage caps
- score-weight draft axes
- case matrix
- score/stage/price alignment
- price-field backfill plan
- Green guardrails
- risk overlays

This pack is ready for later shadow scoring, but not for production Stage threshold changes.
