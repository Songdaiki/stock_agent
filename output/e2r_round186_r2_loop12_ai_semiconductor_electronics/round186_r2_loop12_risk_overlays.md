# Round-186 R2 Loop-12 Risk Overlays

| target | hard gate | red flags |
| --- | --- | --- |
| `GLASS_SUBSTRATE_ADVANCED_PACKAGING_KOREA` | false | customer_missing, yield_missing, revenue_missing, capex_risk |
| `SYSTEM_SEMI_DESIGN_HOUSE_AI_ORDER` | false | order_size_missing, revenue_missing, single_customer, foundry_execution_risk |
| `HBM_TEST_EQUIPMENT_KOREA` | false | actual_order_missing, shipment_missing, price_only_rally, capex_delay |
| `ADVANCED_PACKAGING_EQUIPMENT_BASKET` | false | order_missing, governance_risk, allocation_unclear, price_failed |
| `AI_SERVER_PCB_SUBSTRATE_SECOND_WAVE` | false | inventory_risk, customer_concentration, op_eps_missing, price_only_rally |
| `MLCC_AI_SERVER_COMPONENTS` | false | inventory_risk, asp_missing, smartphone_cycle, customer_concentration |
| `CAMERA_LIDAR_ADAS_ELECTRONICS` | false | direct_revenue_missing, customer_adoption_missing, apple_concentration |
| `ON_DEVICE_AI_THEME_KOREA` | false | theme_only, direct_revenue_missing, adoption_missing, price_only_rally |
| `SEMI_CAPEX_ORDER_TO_REVENUE` | false | capex_delay, order_pushout, op_eps_missing, price_only_rally |
| `IP_LEAK_SUPPLY_CHAIN_REDTEAM` | true | ip_leak, china_catchup, customer_confidence_damage |
| `LABOR_PRODUCTION_DISRUPTION_OVERLAY` | true | labor_disruption, production_delay, delivery_delay |
| `DISCLOSURE_CONFIDENCE_CAP` | false | opendart_list_only, media_only, mou_loi, non_binding, detail_missing |

## Hard 4C Examples

- `IP_LEAK_SUPPLY_CHAIN_REDTEAM`: IP leakage and China memory catch-up reduce Korea semiconductor moat and valuation room.
- `LABOR_PRODUCTION_DISRUPTION_OVERLAY`: labor or production disruption can damage delivery reliability and customer confidence.
- `DISCLOSURE_CONFIDENCE_CAP`: list-only, media-only, MOU/LOI, order-size missing, customer missing, or shipment missing cannot create Green.

Simple example: if `as_of_date=2025-01-01`, a later customer qualification result cannot be used to make SKC/Absolics Green on that date.
