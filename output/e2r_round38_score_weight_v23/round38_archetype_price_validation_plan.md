# Round-38 Archetype Price Validation Plan

Round 38 strengthens price-path validation for AI hardware, high-debt AI infra, advanced packaging, SiC, and accounting hard gates.

| target | validation_group | metrics | success | failure |
|---|---|---|---|---|
| AI_SERVER_ODM_EMS_SUPPLY_CHAIN | high_growth_ai_hardware | mfe_90d, mfe_180d, mfe_1y, mae_90d, gross_margin, inventory_growth, customer_concentration, audit_event_drawdown | AI server revenue, OP/EPS, and rerating moving together can be aligned. | Revenue growth with margin, inventory, customer, or audit trust breaks becomes 4C. |
| AI_SERVER_ACCOUNTING_GOVERNANCE_RISK | hard_redteam_gate | event_day_return, mae_5d, mae_20d, mae_60d, drawdown_from_peak, filing_recovery | Accounting trust recovery can move a case back to watch after evidence is restored. | Auditor resignation, filing delay, or internal-control trust break is hard 4C until resolved. |
| NEOCLOUD_GPU_RENTAL | high_debt_infra | ipo_mfe_90d, ipo_mae_180d, net_debt_ebitda, fcf_margin, contract_duration, customer_concentration | Revenue, EBITDA, FCF conversion, and customer diversification moving together can align. | Price rise with worsening debt, FCF, or concentration is false_positive_score. |
| ADVANCED_PACKAGING_COWOS_EMIB | ai_packaging_bottleneck | packaging_revenue_growth, bookings_backlog, gross_margin, mfe_180d, mfe_1y, drawdown_after_capex_peak | Packaging revenue, backlog, margins, and rerating moving together are aligned. | Capacity expansion or customer capex delay that normalizes the bottleneck becomes 4B/4C. |
| SEMI_EQUIPMENT_AI_CAPEX | ai_capex_equipment | orders_backlog, revenue_guidance, eps_revision, mfe_180d, mfe_1y, mae_after_order_slowdown | Equipment backlog converting to revenue and OP leverage is aligned. | Customer capex delay, export controls, or order pushout can break the thesis. |
| POWER_SEMICONDUCTOR_SIC | cycle_capex_debt | mfe_1y, mfe_2y, mae_1y, debt_ebitda, capex_revenue, utilization, gross_margin, cash_burn | Demand, utilization, FCF, and debt stability together can support Watch-to-Green. | Capex and debt rising before demand and FCF makes this a 4C candidate. |
| OPTICAL_NETWORKING_AI_DATACENTER | ai_network_bottleneck | mfe_180d, mfe_1y, lead_time_normalization_drawdown, valuation_crowding, customer_concentration | Order, lead-time, OP/EPS, and rerating evidence moving together is aligned. | Capacity normalization, customer concentration, or valuation crowding can move it to 4B/4C. |
| REDTEAM_ACCOUNTING_TRUST_OVERLAY | hard_redteam_gate | event_day_return, mae_5d, mae_20d, mae_60d, drawdown_from_peak, recovery_after_filing | The only success condition is verified trust restoration; otherwise Green remains blocked. | Hard accounting trust events immediately block Stage 3-Green and trigger RedTeam review. |

## Group Rules
- high_growth_ai_hardware: validate revenue-to-OP/EPS conversion, margin, inventory, customer concentration, and audit-event drawdown.
- high_debt_infra: validate debt/EBITDA, FCF margin, contract duration, customer concentration, refinancing drawdown, and GPU depreciation cycle.
- ai_packaging_bottleneck/ai_capex_equipment/ai_network_bottleneck: validate order, backlog, OP/EPS revision, lead time, and capex-cycle drawdown.
- cycle_capex_debt: classify as Watch-to-Green only when utilization, FCF, and debt stability are explicit.
- hard_redteam_gate: auditor resignation, filing delay, internal-control weakness, or SEC/DOJ probe blocks Green before scoring.
