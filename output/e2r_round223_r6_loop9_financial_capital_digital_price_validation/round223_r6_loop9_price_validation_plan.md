# Round 223 R6 Price Validation Plan

- price_validation_completed: partial_with_reported_price_anchors
- full_ohlc_complete: false
- Do not invent OHLC, peak, MFE, MAE, stage prices, or business metrics where source anchors are unavailable.

## Backfill Fields

- price_data_source
- full_ohlc_available
- reported_price_anchor
- reported_return_anchor
- stage2_price
- stage3_price
- stage4b_price
- stage4c_price
- mfe_1d
- mae_1d
- event_swing_pp
- discount_to_nav_or_book
- transaction_value
- implied_equity_value
- reported_theme_basket_return
- regulated_revenue_confirmed
- issuer_license_confirmed
- exchange_trust_incident
- price_validation_status

## Case Anchors

| case | data source | reported anchor | status |
|---|---|---|---|
| r6_loop9_kb_financial_bank_valueup | public company profile / KED-derived summary via indexed source | 2025 net profit 5.84T KRW, +15.1%; Big4 financial groups nearly 18T KRW | price_data_unavailable_after_deep_search |
| r6_loop9_securities_financial_basket_capital_market_boom | Reuters reported market-sector return anchors | KOSPI +6.45%, securities +13.5%, financial groups +4.2%, foreign net purchase 3.1T KRW | reported_sector_return_not_full_ohlc |
| r6_loop9_sk_square_nav_discount_valueup | Reuters / Barron's valuation anchors | 200B KRW buyback/cancel programme; SK Hynix stake 20%; discount 47% in 2026 view | price_data_unavailable_after_deep_search |
| r6_loop9_samsung_life_nav_capital_release | Reuters / Barron's valuation anchors | Samsung Electronics stake sale 1.3T KRW; Samsung Electronics stake about 10% | price_data_unavailable_after_deep_search |
| r6_loop9_hana_dunamu_equity_option | Reuters / WSJ transaction anchors | 1.003T KRW for 6.55% stake; implied Dunamu equity value about 15.31T KRW | price_data_unavailable_after_deep_search |
| r6_loop9_naver_dunamu_platform_merger_trust_watch | Reuters event-return and transaction anchors | initially >+7%, then -4.2% after Upbit abnormal withdrawal; deal value 15.13T KRW | reported_event_return_not_full_ohlc |
| r6_loop9_kbank_internet_bank_ipo_watch | Reuters IPO plan anchor | IPO max 984B KRW; valuation up to 5T KRW; 1H 2024 operating profit 86.7B KRW | unlisted_no_stock_ohlc |
| r6_loop9_kakao_kakaobank_legal_governance_watch | Reuters legal event anchors | Kakao -3.4% event move, YTD -24%; bank ownership cap risk if convicted | reported_event_return_not_full_ohlc_for_kakao_kakaobank_ohlc_unavailable |
| r6_loop9_stablecoin_policy_theme_overheat | FT reported return anchors | Kakao Pay >2x, LG CNS +70%, Aton +80%, ME2ON 3x before regulated revenue clarity | reported_return_anchor_not_full_ohlc |
