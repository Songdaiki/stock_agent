# Round-204 R13 Loop-7 Price Validation Plan

## Required Fields

- `price_data_source`
- `full_ohlc_available`
- `reported_price_anchor`
- `reported_return_anchor`
- `stage3_price`
- `stage4b_price`
- `stage4c_price`
- `peak_price`
- `reported_mfe_minimum_pct`
- `reported_market_cap_mfe_minimum_pct`
- `mfe_1d`
- `mfe_30d`
- `mfe_90d`
- `mfe_180d`
- `mfe_1y`
- `mfe_2y`
- `mae_1d`
- `mae_30d`
- `mae_90d`
- `drawdown_after_peak`
- `below_stage3_price_flag`
- `contract_value_before`
- `contract_value_after`
- `contract_value_drawdown_pct`
- `lost_expected_revenue`
- `lost_revenue_vs_prior_revenue_pct`
- `price_validation_status`

## Case Anchors

| case | price data source | reported anchor | status |
| --- | --- | --- | --- |
| `r13_sk_hynix_hbm_4b_benchmark` | Reuters reported return path | 2025 +274%; 2026 to 2026-05-14 >+200% | `reported_return_anchor_not_full_ohlc` |
| `r13_hanwha_aerospace_defense_mfe_4b` | FT/Reuters reported price anchors | +665.3% from reported anchor to reported peak; -13% on capital raise event | `reported_price_anchor_not_full_ohlc` |
| `r13_kogas_resource_price_only` | WSJ intraday price anchor | +30% intraday | `event_anchor_not_stage3` |
| `r13_samsung_sds_kkr_ai_cb_event` | Reuters intraday return anchor | +20.8% intraday | `event_anchor_not_stage3` |
| `r13_jeju_air_fatal_crash_hard_4c` | Reuters intraday price anchor | -15.7% intraday | `reported_intraday_anchor` |
| `r13_lges_contract_cancellation_4c` | Reuters intraday return and lost revenue anchors | -7.6% intraday on Ford cancellation | `reported_intraday_anchor` |
| `r13_lnf_tesla_contract_value_collapse` | Reuters contract-value anchor | contract value $2.9B to $7,386 | `contract_value_anchor_stock_ohlc_unavailable` |
| `r13_hanwha_aerospace_capital_raise_4b_not_4c` | FT/Reuters event return | -13% on capital raise announcement | `reported_event_anchor_not_full_ohlc` |

## Backfill Rule

- Use reported Reuters/FT/WSJ anchors only for fields they explicitly support.
- Keep full OHLC fields unavailable until KRX/Naver/Yahoo adjusted daily bars are backfilled.
- Split Stage 3 anchor, 4B event, 4C event, and contract-value collapse date.
- Do not create a Stage 3 anchor when the case intentionally has no Stage 3 date.
- Price-only rally cases must remain Stage 1/4B-watch until revenue/EPS evidence appears.
