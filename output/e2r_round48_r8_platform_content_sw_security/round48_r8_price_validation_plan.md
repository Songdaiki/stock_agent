# Round-48 R8 Price Validation Plan

## Method

1. Assign stage dates from source evidence only.
2. Store stage-date close prices from official price data.
3. Calculate MFE_30D / 90D / 180D / 1Y / 2Y.
4. Calculate MAE_30D / 90D / 180D / 1Y.
5. Calculate peak price, drawdown after peak, and below-stage3 flag.
6. Compare price paths with ARR, bookings, ad revenue, churn, OPM, FCF, security incidents, privacy/legal events, and launch delays.

## Priority Case Checks

| case_id | stage candidate | check |
| --- | --- | --- |
| `douzone_bizon_eqt_cloud_erp_case` | 2025-11-07 | needs_price_backfill |
| `palantir_ai_platform_revenue_case` | 2025-05-05 | needs_source_date_and_price_backfill |
| `netflix_ad_tier_growth_case` | 2024-11-12 | needs_price_backfill |
| `tencent_game_ai_ad_case` | 2026-05-13 | needs_price_backfill |
| `trade_desk_revenue_miss_case` | needs_source_date | needs_source_date_and_price_backfill |
| `crowdstrike_outage_case` | 2024-07-19 | needs_price_backfill |
| `kakao_founder_legal_overhang_case` | needs_source_date | needs_source_date_and_price_backfill |
| `roblox_safety_forecast_cut_case` | 2026-05-01 | needs_price_backfill |
| `take_two_gta_delay_case` | 2025-11-06 | needs_price_backfill |
| `wpp_ad_cycle_slowdown_case` | 2025-06-09 | needs_price_backfill |
| `meta_scam_ads_lawsuit_case` | 2026-05-11 | needs_price_backfill |

## Alignment Labels

- `aligned`: ARR/OPM/FCF/bookings/ad revenue moves with price rerating.
- `theme_or_feature_only`: AI feature, new title, security theme, or user count exists without economics.
- `premium_valuation_miss`: growth business suffers large drawdown from revenue or guide miss.
- `operational_trust_break`: outage, privacy, safety, or legal issue damages platform trust.
- `single_ip_risk`: game/content rerating depends too heavily on one launch or IP.
- `privacy_or_legal_overhang`: lawsuits and governance risk suppress rerating.
