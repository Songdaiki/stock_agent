# Round-173 R2 Loop-11 Score -> Stage -> Price Alignment

## Base Score Weights

| component | points | direction | reason |
| --- | ---: | --- | --- |
| `eps_fcf_opm_conversion` | 24 | keep_high | AI semiconductor candidates need OP/EPS/FCF conversion, not keyword exposure. |
| `customer_contract_shipment_visibility` | 22 | raise_detail_requirement | Customer name, contract amount, shipment schedule, repeat orders, and diversification drive Stage 2/3. |
| `bottleneck_pricing_power` | 18 | keep_high | HBM bonder, AI server PCB, test socket, and foundry capacity bottlenecks matter only when revenue conversion is visible. |
| `early_price_path_validation` | 12 | new_loop11_axis | Stage 2 must be tested against 60D/120D MFE before a late 4B crowding call. |
| `information_confidence_disclosure_detail` | 8 | hard_review | Media reports, MOU, private-company linkage, and missing customer details cap Stage 3. |
| `capital_discipline_fcf_stability` | 6 | watch | Capex, dilution, customer concentration, and FCF drag can cool equipment and component stories. |
| `valuation_room_4b_runway` | 10 | raise_4b_focus | Large semiconductor reratings must be cooled when price outruns revisions or narratives crowd. |

## Stage Caps

| stage band | max score | evidence | examples | Green policy |
| --- | --- | --- | --- | --- |
| `Stage 1` | 45 | hbm, ai_server, cxl, glass_substrate, on_device_ai, npu, system_semi, pcb_or_test_theme | on_device_ai_revenue_missing_case | Theme keywords route research only. Green is blocked before customer, shipment, revenue, and OP/EPS evidence. |
| `Stage 2` | 70 | customer_name, contract_amount, shipment_schedule, government_investment, technology_license, mou_or_report | db_hitek_foundry_reram_stage2_case, rebellions_sapeon_related_stock_green_cap_case | Stage 2 can include policy/license/private AI-chip ecosystem evidence, but Stage 3 waits for listed-company earnings link. |
| `Stage 2.5` | watch | quality_business, early_price_path, ai_testing_or_pcb_exposure, op_eps_detail_missing | leeno_ai_test_socket_stage25_case | Useful diagnostic watch band, not a canonical Stage change and not Stage 3-Green. |
| `Stage 3` | requires_4_of_7 | op_eps_revision_or_beat, confirmed_customer_contract_terms, revenue_conversion, customer_diversification, 60d_mfe_20pct, relative_strength, valuation_not_peer_top_quartile | hanmi_hbm_bonder_stage3_4b_case | Stage 3 is possible when earnings, customer terms, bottleneck revenue conversion, price path, and valuation room mostly align. |
| `Stage 4B` | requires_3_of_5 | stage2_120d_mfe_80pct, stage3_252d_mfe_150pct, price_300_500pct, narrative_before_earnings, keyword_crowding | isu_petasys_ai_server_pcb_487pct_4b_case, hanmi_micron_media_report_not_contract_case | Good logic is cooled when price and AI narrative crowding outrun OP/EPS revision. |
| `Stage 4C` | hard_gate | mou_or_media_report_mistaken_for_contract, customer_order_cancel, dilution_cb_bw, audit_disclosure_issue, single_customer_capex_cut, shipment_delay, op_eps_revision_down, direct_earnings_link_missing | samsung_labor_disruption_overlay_case, ai_chip_private_related_direct_revenue_missing_case | Hard RedTeam overrides AI/HBM narratives when contract, shipment, disclosure, or earnings linkage breaks. |

## Alignment Cases

| case | detected stage | price-path status | verdict | adjustment |
| --- | --- | --- | --- | --- |
| `hanmi_hbm_bonder_stage3_4b_case` | Stage 3 candidate + 4B-watch | Micron media report and SK Hynix order created early price reaction; exact stage prices need KRX backfill | stage3_catch_and_4b_cool_required | credit confirmed customer contract; cap unconfirmed Micron report; reduce valuation room after rapid rally |
| `isu_petasys_ai_server_pcb_487pct_4b_case` | Stage 3 candidate -> 4B-watch | AI server PCB rerating can be real, but 487% reference move makes valuation runway limited | structural_success_but_late_4b | credit AI server PCB exposure before rerating; apply 4B haircut after 300-500% move |
| `leeno_ai_test_socket_stage25_case` | Stage 2.5 -> Stage 3 candidate | 70% AI boom rally is attention, not Green without OP/EPS and socket demand detail | quality_business_not_green_yet | credit high-margin socket and testing exposure; cap Stage 3 before customer and revision data |
| `db_hitek_foundry_reram_stage2_case` | Stage 1/2 | Policy foundry and ReRAM license are options, not wafer revenue | policy_license_not_green | credit policy and license; block Green before customer wafer revenue and OP/EPS revision |
| `rebellions_sapeon_related_stock_green_cap_case` | Stage 1/2 event | Private-company merger and government investment do not automatically flow into listed EPS | listed_link_missing | credit ecosystem event; require equity-method income, direct revenue, or customer shipment |
| `hanmi_micron_media_report_not_contract_case` | Stage 2 + 4B-watch | Possible Micron deal moved price but was not a finalized disclosed contract | media_report_cap_correct | treat as supporting evidence only until final contract terms are verified |
| `samsung_labor_disruption_overlay_case` | 4C overlay | Labor disruption can hurt Samsung exposure and broader supply chain delivery reliability | hard_redteam_alignment | apply operational disruption overlay to delivery and execution confidence |
| `on_device_ai_revenue_missing_case` | Stage 1/2 | On-device AI theme can move price before actual adoption revenue appears | theme_without_revenue_blocked | allow research routing; block Green before design-win revenue and OP/EPS revision |
| `hbm_test_equipment_stage2_case` | Stage 2 | HBM test narrative needs actual customer orders, shipment schedule, and OP/EPS conversion | equipment_watch_not_green_yet | credit HBM test bottleneck; cap before order and revision proof |
| `ai_chip_private_related_direct_revenue_missing_case` | event premium / 4C gate | Private valuation and listed-company price are separated until direct earnings link appears | direct_earnings_gate_contains_false_green | block Stage 3 when listed company has no direct revenue or equity-method income |

## Interpretation

- 한미반도체 is the cleanest Korea R2 early Stage 3 / 4B-watch test, but media-report-only evidence is capped.
- 이수페타시스 tests whether AI server PCB was catchable before a 300-500% move and cooled afterward.
- 리노공업 uses Stage 2.5 as a diagnostic watch band, not a canonical Stage change.
- DB하이텍 and 리벨리온·사피온 related stocks show why policy, license, private valuation, and related-stock narratives must not create Green without revenue.
- 삼성 파업 overlay keeps operational disruption visible to RedTeam without turning it into a recommendation.
