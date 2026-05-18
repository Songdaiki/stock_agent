# Round-176 R5 Loop-11 Score -> Stage -> Price Alignment

## Base Score Weights

| component | points | direction | reason |
| --- | ---: | --- | --- |
| `eps_fcf_opm_conversion` | 23 | keep_high | Stage 3 needs OP/EPS/FCF and margin conversion, not K-food or K-beauty keywords. |
| `export_channel_visibility` | 21 | raise_channel_detail | US/Japan/Europe sales, Amazon/TikTok/Ulta/Sephora/Costco/Target, offline entry, ASP, and mainstream shelf drive Stage 2. |
| `sell_through_reorder_repeat_consumption` | 18 | raise_for_loop11 | Shipment and listing are capped until sell-through, reorder, and repeat consumption are visible. |
| `inventory_receivables_margin_quality` | 12 | hard_quality_gate | Inventory days, receivables days, gross margin, OPM, and discount rate decide whether growth is real. |
| `early_price_path_validation` | 10 | loop11_axis | 60D/120D price path separates early Stage 3 catch from late 4B chasing. |
| `safety_tariff_disclosure_confidence` | 8 | redteam_review | Tariff, China exposure, recalls, product safety, and disclosure gaps cap Stage 3. |
| `valuation_room_4b_runway` | 8 | cool_brand_rallies | IPO doubles, viral brand rerating, and K-beauty/K-food crowding reduce runway quickly. |

## Stage Caps

| stage band | max score | evidence | examples | Green policy |
| --- | --- | --- | --- | --- |
| `Stage 1` | 45 | k_food_viral, k_beauty_viral, us_listing_expectation, tiktok_shop, amazon, ulta_sephora_costco_target, olive_young_us_news | silicon2_kbeauty_distribution_stage3_candidate, dalba_global_ipo_4b_watch_case | Viral, listing, GMV, and brand awareness route research only. They do not create Stage 3. |
| `Stage 2` | 70 | us_japan_europe_sales, retail_partnership, online_sales, export_growth, asp, ipo_or_platform_option, oem_order_visibility | cj_oliveyoung_platform_holdco_cap_case, nongshim_global_staple_stage2_case | Stage 2 can be strong, but Green waits for sell-through, reorder, OPM, FCF, and inventory/receivables quality. |
| `Stage 3` | requires_4_of_7 | export_or_overseas_sales_growth, op_eps_revision_or_op_beat, us_japan_europe_channel_expansion, sell_through_or_reorder, inventory_receivables_not_worse, 60d_mfe_20pct, valuation_not_peer_top_quartile | silicon2_kbeauty_distribution_stage3_candidate, kbeauty_oem_odm_supplychain_stage3_candidate, nongshim_global_staple_stage2_case | Stage 3 is possible only when channel growth converts into repeat demand, earnings, and quality of working capital. |
| `Stage 4B` | requires_3_of_5 | stage2_120d_mfe_80pct, ipo_or_viral_brand_price_doubles, narrative_before_earnings, inventory_receivables_start_rising, kbeauty_kfood_keyword_crowded | dalba_global_ipo_4b_watch_case, silicon2_kbeauty_distribution_stage3_candidate | Brand and IPO rallies are cooled when price outruns sell-through, reorder, or OP/EPS. |
| `Stage 4C` | hard_gate | china_premium_demand_slowdown_earnings_miss, us_tariff_price_competitiveness_hit, channel_stuffing, inventory_or_receivables_spike, single_viral_sku_demand_drop, recall_or_safety_issue, oem_customer_order_cancel_or_indie_brand_churn, license_brand_saturation_or_mna_overpay | amorepacific_china_exposure_4c_case, fnf_license_brand_china_mna_watch_case, channel_stuffing_inventory_overlay_case | Hard RedTeam overrides consumer export narratives when sell-through, inventory, tariff, China exposure, or brand saturation breaks the path. |

## Alignment Cases

| case | detected stage | price-path status | verdict | adjustment |
| --- | --- | --- | --- | --- |
| `silicon2_kbeauty_distribution_stage3_candidate` | Stage 2/3 candidate | K-beauty import/e-commerce evidence strong; KRX and working capital path need backfill | portfolio_distribution_not_brand_keyword | credit portfolio distribution and US channel; cap before sell-through, inventory, receivables, OPM, FCF |
| `dalba_global_ipo_4b_watch_case` | Stage 2 + 4B-watch | Post-listing price more than doubled before sell-through proof | ipo_double_requires_4b_watch | credit US channel talks; apply IPO valuation and single-brand risk |
| `cj_oliveyoung_platform_holdco_cap_case` | Stage 2 option | Strong private platform but CJ cash-flow/NAV link needs proof | holdco_link_cap | credit platform; cap before IPO/cash realization or consolidated OP/FCF link |
| `nongshim_global_staple_stage2_case` | Stage 2/3 candidate | Global staple evidence strong; OP/EPS and KRX path need backfill | staple_export_candidate | credit overseas mix and mainstream shelf; cap before OP/EPS and inventory proof |
| `kbeauty_oem_odm_supplychain_stage3_candidate` | Stage 2/3 candidate | OEM/ODM can catch multi-brand repeat demand before single brands | repeat_order_supplychain_candidate | credit customer diversification; cap before receivables and OPM proof |
| `drg_kbeauty_mna_stage2_reference_case` | Stage 2 reference | Private M&A validates strategic value, not direct listed-company Green | reference_not_direct_green | support sector evidence only; require listed revenue/OPM link |
| `amorepacific_china_exposure_4c_case` | 4C-watch | China demand weakness and earnings miss override K-beauty narrative | china_exposure_4c_alignment | apply China premium exposure and earnings miss gate |
| `kbeauty_tariff_import_margin_review_case` | RedTeam overlay | US import growth positive but tariff can pressure margin and reorder | tariff_margin_gate | require margin buffer and price pass-through |
| `fnf_license_brand_china_mna_watch_case` | Watch/Red | License brand saturation and TaylorMade M&A governance risk cap rerating | license_brand_governance_risk | require sell-through, inventory, and M&A discipline |
| `channel_stuffing_inventory_overlay_case` | hard gate | Shipment growth can hide sell-through weakness | sell_through_inventory_gate | require inventory days, receivables days, reorder, and margin quality |

## Interpretation

- Silicon2 is the clean platform-distribution test: portfolio evidence matters, but working capital gates Green.
- D'Alba is the clean IPO/brand 4B test: US channels can be Stage 2 while valuation is cooled.
- CJ/Olive Young is the private-platform-to-listed-parent transmission test.
- Nongshim and K-beauty OEM/ODM test whether repeat demand reaches OP/EPS before crowding.
- Amorepacific, F&F, tariff, and channel-stuffing overlays prevent broad K-beauty/K-food narratives from becoming unsafe Green.
