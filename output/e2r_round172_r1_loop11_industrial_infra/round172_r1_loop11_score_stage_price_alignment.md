# Round-172 R1 Loop-11 Score -> Stage -> Price Alignment

## Base Score Weights

| component | points | direction | reason |
| --- | ---: | --- | --- |
| `eps_fcf_opm_conversion` | 24 | keep_high | Stage 3 requires OP/EPS/FCF and margin conversion, not order headlines. |
| `contract_backlog_customer_visibility` | 20 | detail_required | Contract amount, customer, period, backlog quality, and delivery schedule define Stage 2. |
| `bottleneck_pricing_power` | 18 | keep_high | Transformer lead time, CAPA shortage, shipyard slots, defense production scale, and ASP/margin matter. |
| `early_price_path_validation` | 12 | new_loop11_axis | The score must catch early 60D/120D price validation before the candidate becomes crowded. |
| `capital_discipline_dilution` | 8 | hard_review | Capex, dilution, IPO premium, and acquisition funding can cool a good backlog story. |
| `disclosure_confidence_redteam` | 8 | hard_review | LOI/MOU, legal injunction, sanctions, missing detail, or OpenDART list-only evidence caps Stage 3. |
| `valuation_room_4b_runway` | 10 | raise_4b_focus | Good structures with large 120D/252D MFE become 4B-watch rather than fresh Green. |

## Stage Caps

| stage band | max score | evidence | examples | Green policy |
| --- | --- | --- | --- | --- |
| `Stage 1` | 45 | ai_power_demand, us_grid_shortage, shipbuilding_rebuild, nuclear_export_news, defense_rearmament, government_policy | hd_hyundai_mipo_loi_only_case | Green blocked until company-level contract/backlog or execution evidence appears. |
| `Stage 2` | 70 | contract_amount, customer_name, delivery_schedule, backlog, preferred_bidder, loi_or_moa, aircraft_contract | doosan_czech_nuclear_preferred_bidder_case, kai_fa50_philippines_stage2_case | Green blocked until OP/EPS/FCF, margin, and price path confirm. |
| `Stage 2.5` | watch | combat_validation, early_price_path, strong_demand_interest, actual_contract_missing | lig_nex1_cheongung_combat_validation_stage25_case, hyosung_hico_hvdc_stage25_case | Useful watch band, but not a canonical Stage change and not Stage 3-Green. |
| `Stage 3` | requires_4_of_6 | op_eps_revision_or_beat, backlog_growth_and_long_delivery, margin_improvement, 60d_mfe_20pct, valuation_not_peer_top_quartile, dart_detail_verified | hd_hyundai_electric_transformer_stage3_4b_case | Stage 3 is early conviction only when earnings, backlog quality, margin, price path, valuation room, and detail confidence mostly line up. |
| `Stage 4B` | monitoring | stage2_120d_mfe_80pct, stage3_252d_mfe_150pct, crowded_reports, peer_top_quartile_valuation, price_faster_than_revision | hd_hyundai_marine_solution_ipo_mro_case, lig_nex1_cheongung_combat_validation_stage25_case | Good logic can be cooled when price and consensus have already run ahead. |
| `Stage 4C` | hard_gate | contract_cancel_or_correction, dilution_cb_bw, audit_or_disclosure_issue, legal_or_competition_block, sanction_or_export_control, low_margin_order, loi_failed_to_convert | hanwha_ocean_china_sanction_4c_case, doosan_czech_nuclear_legal_gate_case | Hard RedTeam overrides a positive R1 narrative. |

## Alignment Cases

| case | detected stage | price-path status | verdict | adjustment |
| --- | --- | --- | --- | --- |
| `hd_hyundai_electric_transformer_stage3_4b_case` | Stage 3 candidate + 4B-watch | KRX bars must backfill 60D/120D/252D MFE and valuation room | stage3_catch_and_4b_cool_required | raise bottleneck/visibility, reduce valuation room after crowded rerating |
| `hyosung_hico_hvdc_stage25_case` | Stage 2.5 -> Stage 3 candidate | HICO/HVDC evidence strong; OP/EPS revision and price path still need backfill | stage2_5_not_green_yet | credit US localization and HVDC, keep disclosure and margin cap |
| `doosan_czech_nuclear_preferred_bidder_case` | Stage 2 + 4B-watch | Preferred bidder produced a price rally, but final contract and scope were not yet visible | event_to_contract_not_green_yet | credit preferred bidder; cap before contract signing, scope, margin, and OP/EPS revision |
| `hd_hyundai_heavy_mipo_merger_stage2_4b_case` | Stage 2 + 4B-watch | Merger announcement had large one-day price reaction and record-high context | event_to_structural_watch | credit restructuring; apply 4B watch before real US shipbuilding/MRO contract economics |
| `hd_hyundai_marine_solution_ipo_mro_case` | Stage 2/3 candidate + IPO 4B | IPO first-day premium requires valuation-room haircut | good_model_but_ipo_4b | credit recurring MRO; cap Green before post-listing FCF/OPM and customer diversification |
| `kai_fa50_philippines_stage2_case` | Stage 2 | Customer, amount, aircraft count, and delivery deadline visible; margin and follow-on exports pending | stage2_not_green_yet | credit contract detail; cap before OP/EPS revision and margin visibility |
| `lig_nex1_cheongung_combat_validation_stage25_case` | Stage 2.5 + 4B-watch | Combat validation and +47% rally are strong but contract terms are absent | price_path_attention_not_green | allow Stage 2.5 watch; block Green before export contract and EPS revision |
| `hanwha_ocean_china_sanction_4c_case` | Stage 2 option -> 4C-watch | US shipbuilding/MRO option is offset by China sanction retaliation | hard_redteam_alignment | apply geopolitical sanction hard gate |
| `hd_hyundai_mipo_loi_only_case` | Stage 1 / weak Stage 2 | LOI/contract talk cannot support Stage 3 even if price moves | green_block_correct | cap LOI until final contract, customer, margin, and delivery detail appear |
| `doosan_czech_nuclear_legal_gate_case` | Stage 2 -> legal 4C-watch | Preferred bidder rally faced appeal / contract-signing prohibition gate | legal_gate_contains_false_green | block Stage 3 before legal gate clears and contract scope is signed |

## Interpretation

- HD현대일렉트릭 is the cleanest Korea R1 early Stage 3 / 4B-watch test.
- 효성중공업 and LIG넥스원 use Stage 2.5 as a diagnostic watch band, not a canonical Stage change.
- Czech nuclear preferred bidder cases prove price can move before final contract; that is Stage 2, not Green.
- HD현대미포 LOI and 한화오션 sanction cases prove why Stage 4C and disclosure caps must remain strict.
