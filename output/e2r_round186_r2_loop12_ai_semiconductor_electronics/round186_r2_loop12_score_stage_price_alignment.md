# Round-186 R2 Loop-12 Score / Stage / Price Alignment

| case | detected stage | price path status | verdict | adjustment |
| --- | --- | --- | --- | --- |
| `skc_absolics_glass_substrate_stage2_case` | Stage 2 strong | Facility/grant/test production exists; KRX and customer-yield price backfill required | commercialization_gate_not_green | credit advanced packaging and grant; cap before customer, yield, shipment, revenue, and OPM |
| `gaonchips_pfn_samsung_2nm_stage2_case` | Stage 2 strong | Customer and technology node visible; order size and listed-company revenue missing | design_win_to_revenue_gate | credit customer/design role; cap before order size, revenue, repeat design win, and OP/EPS |
| `hbm_test_equipment_basket_stage3_candidate_case` | Stage 2~3 candidate | Macro CAPEX visible; individual order and 60D/120D MFE backfill required | stage3_candidate_if_order_revision_price_align | credit HBM test bottleneck; cap if customer order or OP/EPS missing |
| `hanwha_precision_spinoff_hbm_equipment_stage2_4c_watch_case` | Stage 2 + governance/price cap | HBM equipment option exists but price failed and governance allocation is unclear | evidence_good_but_price_failed | apply governance and value-allocation haircut until actual order and shareholder-value link appear |
| `ai_server_pcb_mlcc_second_wave_stage3_candidate_case` | Stage 2~3 candidate | AI server substrate/MLCC basket needs ASP, inventory, OPM, and customer backfill | stage3_candidate_if_asp_inventory_opm_align | credit second-wave component exposure; cap when inventory or customer detail is missing |
| `on_device_ai_theme_korea_stage1_2_4b_watch_case` | Stage 1/2 -> 4B-watch | Theme can run before mass-production revenue | price_only_theme_requires_4b_watch | route research, but block Green before design-win revenue, royalty/license, mass production, and OP/EPS |
| `samsung_supply_chain_labor_disruption_4c_case` | 4C overlay | Labor/production disruption can interrupt delivery and customer confidence | hard_redteam_alignment | apply operational disruption overlay to Samsung-exposed supply-chain candidates |
| `korea_memory_ip_leak_cxmt_4c_case` | 4C overlay | IP leakage and China catch-up reduce Korea semiconductor moat and valuation room | hard_redteam_alignment | apply IP/security overlay across memory, equipment, test, materials, and components |

## Interpretation

- SKC/Absolics and 가온칩스 are strong Stage 2 examples, not automatic Stage 3.
- HBM test equipment and AI server PCB/MLCC baskets are Stage 2~3 candidates only after order/revenue/revision and price-path validation.
- On-device AI is a research route, but price-only moves are 4B-watch until adoption revenue appears.
- Labor disruption and IP leakage are RedTeam overlays that can interrupt otherwise positive R2 narratives.
