# Round 217 R13 Price Validation Plan

- price_validation_completed: partial_with_reported_price_anchors
- full_ohlc_complete: false
- Do not invent OHLC, stage prices, MFE, or MAE where raw adjusted daily prices are unavailable.

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
- peak_price
- peak_return_from_stage3_pct
- mfe_1d
- mae_1d
- reported_return_2025_pct
- reported_return_2026_ytd_pct
- market_cap_mfe_minimum_pct
- contract_value_drawdown_pct
- lost_revenue_vs_prior_revenue_pct
- event_mfe_pct
- event_mae_pct
- price_validation_status

## Case Anchors

| case | data source | reported anchor | status |
|---|---|---|---|
| r13_loop8_sk_hynix_hbm_stage3_4b | MarketWatch / Reuters / Tom's Hardware reported anchors | Stage 3 to reported peak +776.6%; 2025 +274%; 2026 YTD >+200% | reported_price_anchor_not_full_ohlc |
| r13_loop8_hyundai_rotem_k2_delivery_aligned | WSJ / Reuters reported price and contract anchors | +9.3% event move; KOSPI relative outperformance +9.6pp | reported_price_anchor_not_full_ohlc |
| r13_loop8_hanwha_aero_dilution_4b_not_4c | Reuters / FT reported event anchors | -13% event drawdown; share sale discount -16%; pre-event YTD more than doubled | reported_event_anchor_not_full_ohlc |
| r13_loop8_kogas_resource_price_only | WSJ reported intraday price anchor | +30% intraday before commerciality evidence | reported_event_anchor_not_stage3 |
| r13_loop8_lges_lnf_contract_quality_4c | Reuters reported event return and contract-value anchors | LGES expected revenue loss 13.5T KRW; L&F $2.9B to $7,386 | reported_event_and_contract_anchor_not_full_ohlc |
| r13_loop8_jeju_air_operational_trust_hard_4c | Reuters reported price/event anchors | -15.7% intraday; market cap wipeout 95.7B KRW | reported_price_anchor_not_full_ohlc |
| r13_loop8_stablecoin_theme_price_only | FT reported return anchors | Kakao Pay >+100%, LG CNS +70%, Aton +80%, ME2ON +200% | reported_return_anchor_not_full_ohlc |
| r13_loop8_korea_zinc_strategic_governance_watch | Reuters reported event anchors | U.S. smelter event +5%; YoungPoong event -10.5% | reported_event_anchor_not_full_ohlc |
