# Round-176 R5 Loop-11 Price Validation Plan

## Method

1. Assign Stage 1/2/3/4B/4C dates from dated source evidence only.
2. Backfill KRX daily bars for `price_at_stage1` through `price_at_stage4c`.
3. Calculate 20D/60D/120D/252D returns and MFE/MAE after Stage 2.
4. Compare price speed against OP/EPS revision, sell-through, reorder, inventory, receivables, margin, tariff, and China exposure.
5. Separate distribution/platform/OEM Stage 2 evidence from brand-viral 4B-watch and China/tariff/working-capital 4C-watch.
6. Keep IPO, private-platform, tariff, single-SKU, channel-stuffing, and disclosure-detail caps explicit.

## Priority Case Checks

| case_id | target | stage marker | check |
| --- | --- | --- | --- |
| `silicon2_kbeauty_distribution_stage3_candidate` | `K_BEAUTY_EXPORT_DISTRIBUTION_KOREA` | 2025-06-05 | needs_krx_price_and_working_capital_backfill |
| `dalba_global_ipo_4b_watch_case` | `K_BEAUTY_BRAND_US_CHANNEL` | 2025-06-05 | needs_exact_ipo_price_path_backfill |
| `cj_oliveyoung_platform_holdco_cap_case` | `K_BEAUTY_RETAIL_PLATFORM_OPTION` | 2025-06-05 | needs_cj_price_and_oliveyoung_financial_link_backfill |
| `nongshim_global_staple_stage2_case` | `K_FOOD_GLOBAL_STAPLE_BRAND` | undated | needs_source_date_and_krx_price_backfill |
| `kbeauty_oem_odm_supplychain_stage3_candidate` | `K_BEAUTY_OEM_ODM_SUPPLYCHAIN_KOREA` | 2025-06-05 | needs_krx_price_op_revision_inventory_receivables_backfill |
| `drg_kbeauty_mna_stage2_reference_case` | `K_BEAUTY_BRAND_MNA_VALIDATION_STAGE2_REFERENCE` | 2024-12-23 | not_price_applicable_private_reference |
| `amorepacific_china_exposure_4c_case` | `CHINA_CONSUMER_EXPOSURE_4C` | undated | needs_exact_stage_date_backfill |
| `kbeauty_tariff_import_margin_review_case` | `TARIFF_IMPORT_MARGIN_OVERLAY` | undated | not_price_applicable_overlay |
| `fnf_license_brand_china_mna_watch_case` | `APPAREL_LICENSE_BRAND_CHINA_RISK` | 2025-07-21 | needs_price_inventory_margin_backfill |
| `channel_stuffing_inventory_overlay_case` | `CHANNEL_STUFFING_INVENTORY_OVERLAY` | undated | not_price_applicable_overlay |
| `kfood_single_sku_viral_risk_case` | `K_FOOD_SINGLE_SKU_RISK` | undated | not_price_applicable_overlay |

## Alignment Labels

- `portfolio_distribution_not_brand_keyword`: distributor quality needs sell-through and working capital proof.
- `ipo_double_requires_4b_watch`: post-listing doubling is not Green by itself.
- `holdco_link_cap`: private platform value needs listed-parent transmission.
- `staple_export_candidate`: staple food export evidence needs OP/EPS and inventory proof.
- `repeat_order_supplychain_candidate`: OEM/ODM strength needs customer diversification and receivables quality.
- `china_exposure_4c_alignment`: China demand weakness and earnings miss override broad K-beauty narratives.
