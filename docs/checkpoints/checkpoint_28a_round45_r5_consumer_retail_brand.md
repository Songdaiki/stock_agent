# Checkpoint 28A Round 45 - R5 Consumer / Retail / Brand

## Scope

Round 45 adds the R5 consumer, retail, and brand calibration pack. This is
still calibration/evaluation material only. It does not change production
feature engineering, scoring, staging, RedTeam, or candidate generation.

## Files Added

- `src/e2r/sector/round45_r5_consumer_retail_brand.py`
- `src/e2r/cli/build_round45_r5_report.py`
- `tests/test_round45_r5_consumer_retail_brand.py`
- `data/e2r_case_library/cases_r5_round45.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round45_r5_v1.csv`
- `output/e2r_round45_r5_consumer_retail_brand/`

## Archetype Updates

Round 45 adds R5-specific canonical archetype labels so future sector scoring
can distinguish consumer structures instead of forcing every consumer story
into generic retail or export buckets.

Added labels:

- `FOOD_AGRI_LIVESTOCK_CYCLE`
- `RETAIL_CONVENIENCE_OFFLINE`
- `RETAIL_ECOMMERCE_LOGISTICS`
- `ECOMMERCE_FRESH_LOGISTICS`
- `BEAUTY_OEM_ODM_SUPPLYCHAIN`
- `APPAREL_FAST_FASHION_BRAND_OEM`
- `HOME_LIVING_APPLIANCE_RENTAL`
- `HOME_CHILD_EDUCATION`
- `CONSUMER_REGULATED_PRODUCT`

Example: `K푸드` and `K뷰티` can become Green candidates when repeat export
demand, channel expansion, OPM/FCF, and revision evidence move together. A
store-count story or GMV story remains Watch until unit economics and FCF are
verified.

## Output Summary

- target_count: 11
- case_candidate_count: 10
- success_candidate_count: 4
- stage4b_case_count: 1
- stage4c_case_count: 5
- green_possible_count: 3
- watch_yellow_first_count: 6
- redteam_first_count: 2
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

## Case Coverage

Positive / watch-to-Green candidates:

- `samyang_buldak_export_rerating_case`
- `kbeauty_us_offline_channel_case`
- `cu_gs25_store_efficiency_case`
- `coway_rental_recurring_case`

4B / 4C guardrail cases:

- `apr_medicube_device_export_case`
- `samyang_buldak_recall_risk_case`
- `coupang_supplier_regulation_case`
- `coupang_data_breach_case`
- `whirlpool_hardware_cycle_4c_case`
- `shein_temu_ip_regulatory_case`

## R5 Green Rule

R5 Green is not “popular product” or “big sales” by itself. It requires the
consumer loop to close:

`export/channel growth -> repeat demand -> ASP or mix support -> OPM/FCF -> clean inventory/receivables -> price-path validation`

Easy example: Buldak export growth can be a strong route into research, but
if overseas inventory builds up or a food-safety recall blocks a market, the
same case becomes a RedTeam issue.

## What Not To Change

- Do not apply R5 v1.0 weights to production scoring yet.
- Do not use these case records as candidate-generation input.
- Do not treat viral traffic, GMV, store count, user count, or celebrity demand as structural evidence by itself.
- Do not invent export growth, sell-through, inventory, receivables, churn, rental accounts, OPM, FCF, or price-path fields.
- Do not lower Stage 3-Green thresholds for consumer stories.

## Verification

Commands run:

```bash
PYTHONPATH=src python -m unittest tests/test_round45_r5_consumer_retail_brand.py -v
PYTHONPATH=src python -m compileall -q src/e2r/sector/round45_r5_consumer_retail_brand.py src/e2r/cli/build_round45_r5_report.py tests/test_round45_r5_consumer_retail_brand.py
PYTHONPATH=src python -m e2r.cli.build_round45_r5_report
```

Result:

- Round 45 targeted tests passed.
- Report generation succeeded.
- Production scoring modules do not import the Round 45 pack.
