# Round 228 R11 Price Validation Plan

- price_validation_completed: partial_with_reported_price_anchors
- full_ohlc_complete: false
- r11_default_stage3_bias: very_conservative
- Do not invent OHLC, peak, MFE, or MAE where raw adjusted daily prices are unavailable.

## Backfill Fields

- price_data_source
- full_ohlc_available
- reported_price_anchor
- reported_return_anchor
- market_index_anchor
- stage1_price
- stage2_price
- stage3_price
- stage4b_price
- stage4c_price
- mfe_1d
- mae_1d
- policy_amount_anchor
- contract_or_offtake_anchor
- macro_growth_or_fx_anchor
- resource_commerciality_anchor
- price_validation_status
