# Round-189 R5 Loop-12 Score / Stage / Price Alignment

| case | detected stage | price path status | verdict | adjustment |
| --- | --- | --- | --- | --- |
| `cj_cheiljedang_kfood_localization_stage23_case` | Stage 2 -> Stage 3 candidate | Localization is visible, but utilization, ASP, OPM, FCF, and 60D MFE need backfill | stage2_to_stage3_if_utilization_opm_fcf_align | credit local production; cap before utilization and FCF |
| `orion_global_staple_brand_second_wave_case` | Stage 2 -> Stage 3 candidate | Repeat snack demand is visible, but regional OPM and input-cost pass-through need backfill | stage2_to_stage3_if_regional_opm_cost_align | credit repeat demand; cap regional maturity and cost risk |
| `bingle_lottewellfood_single_sku_export_watch_case` | Stage 1 -> Stage 2 watch | Single SKU export can move before multi-SKU reorder is proven | single_sku_requires_watch_cap | cap until multi-SKU reorder, OPM, and inventory improve |
| `emart_shinsegae_alibaba_jv_stage2_case` | Stage 2 | JV and +5.5% event return are real, but GMV/take-rate/FCF and data restrictions gate Stage 3 | jv_stage2_not_green_before_monetization | credit JV catalyst; cap data regulation and competition |
| `kbeauty_brand_second_wave_stage23_case` | Stage 2 -> Stage 3 candidate | Online growth is strong, but physical sell-through, reorder, inventory, and OPM need backfill | stage2_to_stage3_if_sellthrough_reorder_inventory_align | credit channel growth; require sell-through quality |
| `convenience_store_pb_sssg_stage23_case` | Stage 2 -> Stage 3 candidate | Network and PB are visible, but SSSG, franchise margin, OPM, FCF, and cost control need backfill | stage2_to_stage3_if_sssg_pb_cost_align | credit PB/SSSG; cap wage/rent/electricity risk |
| `lotte_shopping_mall_redevelopment_stage12_case` | Stage 1 -> Stage 2 | Mall plan is optionality, but CAPEX payback and traffic evidence are not proven | redevelopment_stage12_until_payback | cap before lease income, traffic, and FCF |
| `kbeauty_tariff_import_review_4c_watch_case` | 4C-watch | Tariff risk can erase U.S. import growth if margin buffer is weak | tariff_margin_buffer_hard_review | block Green until price pass-through and inventory are verified |
| `kbeauty_online_viral_not_sellthrough_4b_case` | Stage 2 -> 4B-watch | Viral online growth can be priced before physical sell-through | viral_without_sellthrough_requires_4b_watch | cool K-beauty basket if price outruns sell-through/reorder |
| `emart_alibaba_data_regulation_4c_watch_case` | 4C-watch | Data-sharing limits can delay platform monetization | data_regulation_hard_gate | block Green until monetization works inside the rule set |
| `cj_kfood_localization_capex_drag_case` | Failed rerating | Factories are cost centers until utilization and FCF appear | capex_drag_blocks_green | cap localization until utilization, OPM, and FCF |
| `orion_global_staple_brand_maturity_cap_case` | Failed rerating | A mature staple brand needs regional growth and cost pass-through | maturity_cost_cap | cap repeat-brand narrative when growth and OPM fade |
| `convenience_store_cost_pressure_4c_watch_case` | Failed rerating / 4C-watch | Cost pressure can offset PB and SSSG | cost_pressure_blocks_green | cap defensive retail until franchise margin and OPM recover |
| `r5_loop12_disclosure_confidence_reference_case` | Confidence cap | List/media/channel-only evidence lacks sell-through, inventory, OPM, and FCF | detail_confidence_cap | require verified channel, inventory, OPM, FCF, and parser confidence |

## Interpretation

- CJ and Orion show how K-food can be Stage 2~3 only when localization or repeat demand converts into OPM/FCF.
- E-Mart/Shinsegae shows why a real JV and price reaction can still be capped by data regulation and monetization risk.
- K-beauty and convenience-store cases show why sell-through, reorder, SSSG, PB mix, and inventory quality are required before Green.
