# Round 226 R9 Price Validation Plan

- price_validation_completed: partial_with_reported_price_anchors
- full_ohlc_complete: false
- Do not invent OHLC, peak, MFE, or MAE where raw adjusted daily prices are unavailable.

## Backfill Fields

- price_data_source
- full_ohlc_available
- reported_price_anchor
- reported_return_anchor
- stage1_price
- stage2_price
- stage3_price
- stage4b_price
- stage4c_price
- mfe_1d
- mae_1d
- mfe_event
- mae_event
- relative_underperformance_pp
- operating_metric_anchor
- capex_or_debt_anchor
- cycle_or_policy_anchor
- price_validation_status
