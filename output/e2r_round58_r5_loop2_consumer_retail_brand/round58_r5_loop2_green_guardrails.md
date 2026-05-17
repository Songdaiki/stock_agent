# Round-58 R5 Loop-2 Green Guardrails

| target | posture | Green unlock evidence | Loop-2 penalties |
| --- | --- | --- | --- |
| `EXPORT_RECURRING_CONSUMER` | GREEN_POSSIBLE | export_growth, recurring_demand, channel_sell_through, opm_improvement, eps_revision | single_product, recall, inventory, channel_stuffing |
| `K_BEAUTY_EXPORT_DISTRIBUTION` | GREEN_POSSIBLE | export_growth, offline_channel_sell_through, reorder_signal, opm_roe_improvement | tariff, sell_through, inventory, receivables |
| `BEAUTY_OEM_ODM_SUPPLYCHAIN` | GREEN_POSSIBLE | customer_diversification, repeat_orders, capacity_utilization, opm_improvement | customer_diversification, inventory, receivables |
| `RETAIL_CONVENIENCE_OFFLINE` | WATCH_YELLOW_FIRST | same_store_sales, pb_mix, opm_improvement, fcf_stability | sssg, pb_mix, store_profitability |
| `RETAIL_ECOMMERCE_LOGISTICS` | WATCH_YELLOW_FIRST | repeat_customer_base, logistics_efficiency, fcf_improvement, trust_and_regulation_clean | data_security, supplier_regulation, logistics_cost, fcf |
| `ECOMMERCE_FRESH_LOGISTICS` | WATCH_YELLOW_FIRST | unit_economics, repeat_orders, waste_rate_control, fcf_path | waste_rate, delivery_cost, cash_burn |
| `APPAREL_FAST_FASHION_BRAND_OEM` | WATCH_YELLOW_FIRST | order_visibility, inventory_turnover, discount_rate_control, opm_improvement | inventory, ip_litigation, product_safety, customs |
| `HOME_LIVING_APPLIANCE_RENTAL` | WATCH_YELLOW_FIRST | rental_accounts, churn_stable, recurring_service_revenue, fcf_improvement | rental_accounts, churn, service_revenue, hardware_cycle |
| `HOME_CHILD_EDUCATION` | REDTEAM_FIRST | recurring_demand, channel_expansion, opm_improvement | birth_rate, tam, policy, inventory |
| `CONSUMER_REGULATED_PRODUCT` | WATCH_YELLOW_FIRST | legal_revenue, approval, repeat_revenue, margin_visibility | approval, public_health, regulatory_ban |
| `FOOD_SAFETY_RECALL_OVERLAY` | REDTEAM_FIRST |  | food_safety, recall, country_ban |
| `DATA_SECURITY_SUPPLIER_REGULATION_OVERLAY` | REDTEAM_FIRST |  | data_security, supplier_regulation, payment_delay |

## What Not To Change

- Do not apply R5 Loop-2 v2.0 weights to production scoring yet.
- Do not treat viral demand, channel entry, GMV, store count, or appliance hardware sales as Green evidence by themselves.
- Do not invent export growth, sell-through, reorder, inventory, receivables, churn, FCF, or stage prices.
- Treat food recall, data breach, supplier regulation, payment delay, IP litigation, product safety, and tariff damage as RedTeam fields.
