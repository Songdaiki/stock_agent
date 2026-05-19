# Round 214 R10 Price Validation Plan

- price_validation_completed: partial_with_reported_price_anchors
- full_ohlc_complete: false
- Do not invent OHLC, peak, MFE, or MAE where raw adjusted daily prices are unavailable.

## Backfill Fields

- price_data_source
- full_ohlc_available
- reported_price_anchor
- reported_return_anchor
- stage2_event_peak_price
- stage2_event_mfe_1d_pct
- implied_pre_event_reference_price
- kospi_context_return_pct
- relative_outperformance_pp
- contract_value_or_capex
- pf_delinquency_or_support_metric
- safety_or_quality_metric
- tenant_noi_affo_status
- price_validation_status
