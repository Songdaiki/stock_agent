# Round-176 R5 Loop-11 Green Guardrails

| target | posture | Green unlock evidence | Loop-11 penalties |
| --- | --- | --- | --- |
| `K_BEAUTY_EXPORT_DISTRIBUTION_KOREA` | GREEN_POSSIBLE | op_eps_revision, sell_through, reorder, inventory_receivables_stable, opm_fcf | sell_through, inventory_receivables, valuation_4b |
| `K_BEAUTY_BRAND_US_CHANNEL` | WATCH_YELLOW_FIRST | actual_listing, sell_through, reorder, opm_fcf, tariff_absorption | ipo_4b, sell_through, single_brand, tariff |
| `K_BEAUTY_RETAIL_PLATFORM_OPTION` | WATCH_YELLOW_FIRST | cj_cashflow_link, opm_growth, sell_through, ipo_or_cash_realization, nav_discount_narrows | holdco_link, ipo_event, sell_through |
| `K_BEAUTY_OEM_ODM_SUPPLYCHAIN_KOREA` | GREEN_POSSIBLE | repeat_orders, customer_diversification, opm_fcf, inventory_receivables_stable, op_eps_revision | inventory_receivables, customer_churn, brand_sell_through |
| `K_FOOD_GLOBAL_STAPLE_BRAND` | GREEN_POSSIBLE | overseas_sales_growth, asp, op_eps_revision, reorder, inventory_stable | single_sku, china, op_eps |
| `K_FOOD_SINGLE_SKU_RISK` | REDTEAM_FIRST |  | single_sku, reorder, safety |
| `APPAREL_LICENSE_BRAND_CHINA_RISK` | REDTEAM_FIRST | sell_through, inventory_markdown_stable, opm_fcf, mna_discipline | china, inventory, mna_governance, brand_saturation |
| `CHINA_CONSUMER_EXPOSURE_4C` | REDTEAM_FIRST |  | china, earnings_miss, derating |
| `TARIFF_IMPORT_MARGIN_OVERLAY` | REDTEAM_FIRST |  | tariff, margin_buffer, price_hike |
| `CHANNEL_STUFFING_INVENTORY_OVERLAY` | REDTEAM_FIRST |  | inventory, receivables, sell_through, discount |
| `DISCLOSURE_CONFIDENCE_CAP` | REDTEAM_FIRST | channel, sell_through, reorder, inventory, opm_fcf | disclosure_detail, channel, inventory, margin |
| `K_BEAUTY_BRAND_MNA_VALIDATION_STAGE2_REFERENCE` | WATCH_YELLOW_FIRST | listed_company_link, transaction_price, opm, fcf | direct_link, price_detail |
| `STRONG_PRIVATE_PLATFORM_BUT_HOLDCO_LINK_CAP` | REDTEAM_FIRST |  | holdco_link, cash_realization, nav_discount |

## What Not To Change

- Do not apply R5 Loop-11 v11.0 weights to production scoring yet.
- Do not lower Stage 3-Green thresholds because a K-food or K-beauty stock moved.
- Do not use Round 176 case records as candidate-generation input.
- Do not treat K-food, K-beauty, US listing, TikTok viral, Olive Young, Amazon, or brand awareness as Green by itself.
- Do not invent channel, sell-through, reorder, inventory days, receivables days, OPM, FCF, tariff absorption, stage prices, or MFE/MAE.
- Apply 4B-watch when IPO, viral brand, K-beauty/K-food narrative, or listing news outruns OP/EPS and sell-through.
- Apply 4C/hard review for China premium demand weakness, tariff margin hit, channel stuffing, inventory/receivables spike, recall/safety issue, customer churn, license-brand saturation, or M&A overpay.
