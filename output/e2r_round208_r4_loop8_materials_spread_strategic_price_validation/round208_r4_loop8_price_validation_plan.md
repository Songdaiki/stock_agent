# Round-208 R4 Loop-8 Price Validation Plan

## Required Fields

- `price_data_source`
- `full_ohlc_available`
- `reported_price_anchor`
- `reported_return_anchor`
- `stage2_price`
- `stage3_price`
- `stage4b_price`
- `stage4c_price`
- `peak_price`
- `mfe_1d`
- `mae_1d`
- `mfe_from_base_to_record_close`
- `issue_price_discount_pct`
- `operating_loss_worsening_pct`
- `profit_swing`
- `commodity_drawdown_pct`
- `price_validation_status`

## Case Anchors

| case | price data source | reported anchor | status |
| --- | --- | --- | --- |
| `r4_loop8_korea_zinc_event_strategic_watch` | Reuters/WSJ/FT reported price anchors | +19.8% tender event; +24.1% base to intraday peak; +57.7% to record close; -29.9% share issue event; +27% critical minerals event | `reported_price_anchor_not_full_ohlc` |
| `r4_loop8_lotte_chemical_petrochem_break` | Reuters financial and restructuring evidence | 2024 operating loss 895.0bn KRW; loss worsened +157%; Daesan NCC 1.1mn tpy shutdown for 3 years | `price_data_unavailable_after_deep_search` |
| `r4_loop8_lg_chem_petrochem_failed_rerating` | Reuters financial and event return anchors | LG Chem -2.9% and LGES -6.0% after stake-sale plan; OP -63.75%; petrochemical Q4 loss 99.0bn KRW | `reported_event_anchor_not_full_ohlc` |
| `r4_loop8_sk_innovation_refining_cycle` | Reuters financial and event return anchors | 2025 Q1 shares -2.5% before earnings; 2026 Q1 OP 2.2tn KRW vs 1.4tn estimate, +57.1% beat | `reported_event_anchor_not_full_ohlc` |
| `r4_loop8_posco_lithium_resource_security` | Reuters commodity and transaction anchors | MinRes +10.8%; spodumene >$6,000/t to ~$610/t then ~$880/t | `posco_stock_ohlc_unavailable_after_deep_search` |
| `r4_loop8_oci_non_china_polysilicon_event` | FT/Reuters evidence anchors | $1.2B U.S. expansion; target 10GW by 2027; SpaceX report unconfirmed | `price_data_unavailable_after_deep_search` |
| `r4_loop8_poongsan_copper_defense_event` | Reuters evidence source only | reported deal value 1.5tn KRW; transaction not decided | `price_data_unavailable_after_deep_search` |

## Backfill Rule

- Use reported Reuters/FT/WSJ/MarketWatch anchors only for fields they explicitly support.
- Keep full OHLC unavailable until official or adjusted daily price backfill is done.
- Separate Stage 2 strategic/resource/restructuring evidence, Green-required operating proof, 4B event premium, and 4C spread/dilution breaks.
- Do not create a Stage 3 anchor when the case intentionally has no Stage 3 date.
