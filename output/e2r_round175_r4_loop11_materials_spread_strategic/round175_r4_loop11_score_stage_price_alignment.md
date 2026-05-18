# Round-175 R4 Loop-11 Score -> Stage -> Price Alignment

## Base Score Weights

| component | points | direction | reason |
| --- | ---: | --- | --- |
| `eps_fcf_opm_conversion` | 22 | keep_high | Commodity price is capped until OP/EPS/FCF and margin conversion are visible. |
| `contract_offtake_customer_visibility` | 20 | raise_detail_requirement | Customer, contract amount, period, offtake, price floor, and confirmed sale terms drive Stage 2. |
| `bottleneck_pricing_power` | 16 | allow_macro_bottleneck_but_cap_green | Copper shortage, non-China supply, tariffs, and strategic scarcity matter only when company economics follow. |
| `early_price_path_validation` | 12 | loop11_axis | Stage 2 after-rally MFE/MAE and event-day moves distinguish early catch from late event chasing. |
| `cycle_spread_durability` | 12 | raise_for_r4 | R4 must test raw material prices, inventory P/L, export volume, spread, and pass-through durability. |
| `disclosure_confidence_redteam` | 10 | hard_review | Media-only, report-only, company denial, missing terms, CB/BW, and direct tariff exposure can hard-cap the case. |
| `valuation_room_4b_runway` | 8 | cool_event_rallies | Theme baskets, commodity spikes, M&A rumors, and tariff rallies reduce runway quickly. |

## Stage Caps

| stage band | max score | evidence | examples | Green policy |
| --- | --- | --- | --- | --- |
| `Stage 1` | 45 | copper_price_up, steel_tariff, lithium_rebound, rare_earth_export_control, polysilicon_supply_chain, mna_rumor | copper_ai_grid_korea_basket_stage2_cap_case, lithium_rare_earth_price_only_theme_case | Commodity, tariff, and resource keywords route research only. They do not create Stage 3. |
| `Stage 2` | 70 | contract, offtake, actual_customer, policy_or_tariff_confirmed, factory_or_capa_detail, mna_bid_or_sale_terms | poongsan_copper_defense_mna_unwind_case, oci_holdings_spacex_polysilicon_report_cap_case | Stage 2 is possible when evidence is real, but Green waits for OP/EPS/FCF and durability. |
| `Stage 3` | requires_4_of_7 | price_increase_to_op_eps, export_volume_or_sales_volume_up, cost_pass_through, offtake_or_price_floor, 60d_mfe_20pct, valuation_not_overheated, disclosure_detail_sufficient | copper_ai_grid_korea_basket_stage2_cap_case | Stage 3 is possible only when commodity/spread gains lock into company earnings and the price path is not already 4B. |
| `Stage 4B` | requires_3_of_5 | one_day_commodity_tariff_export_control_rally_10pct, stage2_120d_mfe_80pct, narrative_rises_before_contract_revenue, eps_revision_lags_price, theme_basket_broad_rally | lithium_rare_earth_price_only_theme_case, steel_tariff_directionality_korea_case | Commodity and tariff rallies are cooled when earnings cannot follow. |
| `Stage 4C` | hard_gate | mna_review_dropped_or_sale_denied, media_report_only_no_contract, direct_export_tariff_hit, commodity_price_crash, spread_reworsens, cb_bw_or_equity_raise, op_eps_revision_down, inventory_loss_expands, production_or_export_volume_declines | poongsan_copper_defense_mna_unwind_case, seah_steel_export_tariff_4c_case | Hard RedTeam overrides event narratives when terms disappear, tariffs hit exports, or spreads reverse. |

## Alignment Cases

| case | detected stage | price-path status | verdict | adjustment |
| --- | --- | --- | --- | --- |
| `copper_ai_grid_korea_basket_stage2_cap_case` | Stage 1/2 | Copper macro price path strong; Korean individual KRX/revision path needs backfill | macro_bottleneck_not_company_green | credit copper AI-grid bottleneck; cap before individual order backlog, OPM, and FCF |
| `poongsan_copper_defense_mna_unwind_case` | Stage 2 -> 4C-watch | M&A premium should unwind after Hanwha review drop and Poongsan sale denial | event_unwind_alignment | remove M&A premium; retain copper/defense only if OP/EPS evidence exists |
| `oci_holdings_spacex_polysilicon_report_cap_case` | Stage 1/2 option | SpaceX talks can move price but remain media-only before confirmation | report_not_contract_cap | support research routing; block Stage 3 before confirmed terms |
| `steel_tariff_directionality_korea_case` | Stage 1 event | China-only tariff can lift Korean steel while all-import tariff can hurt it | directionality_required | score tariff target and export exposure before stage upgrade |
| `seah_steel_export_tariff_4c_case` | 4C-watch | US 50% steel tariff and -8% price reaction are aligned hard risk | direct_tariff_4c_alignment | apply export exposure and local-production offset gates |
| `specialty_steel_us_localization_option_case` | Stage 1/2 option | Localization can offset tariff but needs volume and margin | localization_not_green_yet | cap before local revenue, margin, and FCF |
| `lithium_rare_earth_price_only_theme_case` | Stage 1 / 4B-watch | Lithium/rare-earth event rally is price-only without production and FCF | event_rally_not_structural | credit event only lightly; block Green without offtake and earnings |
| `rare_earth_theme_korea_stage1_case` | Stage 1 / overheat watch | Rare-earth keyword basket can rally without revenue | theme_only_contained | cap before actual rare-earth revenue and supply contract |
| `chemical_spread_korea_watch_red_case` | Watch/Red | Spread can reverse before volume and FCF stabilize | spread_durability_required | require durable spread, volume, and OPM/FCF |
| `disclosure_confidence_materials_cap_case` | cap | Missing counterparty/amount/period/volume/margin keeps Stage capped | detail_cap_correct | fetch and parse detail before considering Stage 3 |

## Interpretation

- Copper AI-grid is the strongest macro bottleneck test, but individual Korean names need company-level conversion.
- Poongsan is the clean event-unwind case: copper-defense structure and M&A premium must be split.
- OCI Holdings is the clean report-not-contract case: SpaceX talks remain capped before confirmation.
- Korean steel tariff cases force directionality parsing: China-only tariff and all-import tariff are not the same signal.
- Lithium and rare-earth themes remain price-only until offtake, production, revenue, and FCF are proven.
