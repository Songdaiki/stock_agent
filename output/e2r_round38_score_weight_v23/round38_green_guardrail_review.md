# Round-38 Green Guardrail Review

| target | posture | validation_group | Green unlock evidence | Red flags |
|---|---|---|---|---|
| AI_SERVER_ODM_EMS_SUPPLY_CHAIN | GREEN_POSSIBLE | high_growth_ai_hardware | ai_server_revenue_growth, rack_shipment_growth, op_eps_revision, gross_margin_stable | customer_concentration, low_margin_assembly, inventory, accounting_trust, supplier_related_party |
| AI_SERVER_ACCOUNTING_GOVERNANCE_RISK | REDTEAM_FIRST | hard_redteam_gate | gate-only | auditor_resignation, annual_report_delay, internal_control_weakness, related_party_transaction, sec_doj_probe |
| NEOCLOUD_GPU_RENTAL | WATCH_YELLOW_FIRST | high_debt_infra | take_or_pay, contracted_backlog, fcf_turnaround, customer_diversification | debt, customer_concentration, gpu_obsolescence, funding_cost, fcf_negative |
| ADVANCED_PACKAGING_COWOS_EMIB | GREEN_POSSIBLE | ai_packaging_bottleneck | packaging_revenue_growth, orders_or_backlog, op_eps_revision, bottleneck_visible | capex_cycle, customer_concentration, bottleneck_normalization, yield_risk |
| SEMI_EQUIPMENT_AI_CAPEX | GREEN_POSSIBLE | ai_capex_equipment | equipment_backlog, guidance_raise, eps_revision, backlog_to_revenue | customer_capex, order_delay, export_control, capex_peak |
| POWER_SEMICONDUCTOR_SIC | WATCH_YELLOW_FIRST | cycle_capex_debt | long_term_supply_contract, utilization_up, fcf_improvement, debt_stable | ev_demand, capex_debt, utilization, pricing, bankruptcy |
| OPTICAL_NETWORKING_AI_DATACENTER | GREEN_POSSIBLE | ai_network_bottleneck | hyperscaler_contract, lead_time_extended, order_growth, op_eps_revision | hyperscaler_concentration, valuation_crowding, capacity_normalization, capex_delay |
| REDTEAM_ACCOUNTING_TRUST_OVERLAY | REDTEAM_FIRST | hard_redteam_gate | gate-only | auditor_resignation, annual_report_delay, internal_control_weakness, sec_doj_probe, related_party_transaction |

## What Not To Change
- Do not apply v2.3 weights to production scoring yet.
- Do not use case IDs, AI labels, revenue headlines, IPO narratives, or price spikes as candidate-generation input.
- Do not invent margins, contract terms, customer concentration, debt metrics, FCF, stage dates, or prices.
- Do not treat accounting-trust hard flags as ordinary score penalties; they are RedTeam gates.
- Do not lower Stage 3-Green thresholds to improve recall.
