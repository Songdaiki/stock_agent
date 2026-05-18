# Round-173 R2 Loop-11 Green Guardrails

| target | posture | Green unlock evidence | Loop-11 penalties |
| --- | --- | --- | --- |
| `HBM_BONDER_EQUIPMENT_KOREA` | GREEN_POSSIBLE | confirmed_contract, customer_diversification, op_eps_revision, equipment_margin, price_path_aligned | unconfirmed_report, valuation_crowding, customer_concentration |
| `ADVANCED_PACKAGING_EQUIPMENT_KOREA` | WATCH_YELLOW_FIRST | orders, shipment, revenue_conversion, op_eps_revision | order_visibility, shipment_schedule, customer_capex |
| `AI_SERVER_PCB_MLB_KOREA` | GREEN_POSSIBLE | order_visibility, op_eps_revision, customer_diversification, capacity_constraint, price_path_aligned | price_300_500pct, customer_concentration, inventory |
| `SEMICONDUCTOR_TEST_SOCKET_KOREA` | WATCH_YELLOW_FIRST | high_margin_socket, op_eps_revision, repeat_order, customer_detail | valuation_crowding, customer_detail_missing |
| `HBM_TEST_EQUIPMENT_KOREA` | WATCH_YELLOW_FIRST | customer_order, shipment_schedule, op_eps_revision, margin_visible | order_missing, shipment_delay, customer_capex |
| `SYSTEM_SEMI_FOUNDARY_OPTION_KOREA` | WATCH_YELLOW_FIRST | customer_wafer_revenue, utilization, op_eps_revision, commercial_revenue | policy_only, license_only, customer_revenue_missing |
| `AI_CHIP_FABRIC_PRIVATE_RELATED` | REDTEAM_FIRST | direct_revenue, equity_method_income, customer_contract, shipment | direct_link_missing, private_valuation, related_stock_only |
| `ON_DEVICE_AI_THEME` | REDTEAM_FIRST | design_win_revenue, customer_order, op_eps_revision | theme_only, revenue_missing, customer_missing |
| `MOU_OR_REPORT_NOT_CONTRACT` | REDTEAM_FIRST |  | mou_or_report_only, detail_missing, customer_unknown |
| `DISCLOSURE_CONFIDENCE_CAP` | REDTEAM_FIRST | contract_terms, customer_name, shipment_schedule, margin_visible | disclosure_confidence_capped, detail_missing |
| `HBM_SUPPLY_CHAIN_LABOR_DISRUPTION_OVERLAY` | REDTEAM_FIRST | labor_resolved, delivery_normalized, customer_supply_confirmed | labor_disruption, delivery_delay, execution_risk |
| `AI_CHIP_LISTED_EARNINGS_LINK_GATE` | REDTEAM_FIRST | direct_revenue, equity_method_income, customer_contract, repeat_shipment | direct_earnings_link_missing, private_valuation_only, related_stock_only |

## What Not To Change

- Do not apply R2 Loop-11 v11.0 weights to production scoring yet.
- Do not lower Stage 3-Green thresholds because AI/HBM themes have strong price paths.
- Do not use Round 173 case records as candidate-generation input.
- Do not treat media reports, MOU, private valuation, government investment, policy option, or on-device AI theme as Green by itself.
- Do not invent customer names, contract amounts, shipment schedules, margins, stage prices, MFE/MAE, or valuation bands.
- Apply 4B-watch when price moves 300-500% or narrative crowds before revisions.
- Apply 4C/hard review for direct earnings link missing, labor disruption, customer cancellation, dilution, disclosure failures, or shipment delay.
