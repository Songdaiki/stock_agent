# Round-45 R5 Green Guardrails

| target | posture | Green unlock evidence | Red flags |
| --- | --- | --- | --- |
| `EXPORT_RECURRING_CONSUMER` | GREEN_POSSIBLE | export_growth, recurring_demand, channel_expansion, op_eps_revision, inventory_stable | single_product_dependency, recall, inventory_build, channel_stuffing |
| `FOOD_AGRI_LIVESTOCK_CYCLE` | REDTEAM_FIRST | repeat_margin, cost_pass_through, fcf_margin | one_off_price, commodity_reversal, inventory_loss |
| `RETAIL_CONVENIENCE_OFFLINE` | WATCH_YELLOW_FIRST | same_store_sales, pb_mix, opm_improvement, fcf_stability | store_count_only, labor_cost_pressure, rent_pressure, store_density |
| `RETAIL_ECOMMERCE_LOGISTICS` | WATCH_YELLOW_FIRST | repeat_customer_base, logistics_efficiency, fcf_improvement, trust_and_regulation_clean | data_breach, supplier_pressure, payment_delay, trust_damage |
| `ECOMMERCE_FRESH_LOGISTICS` | WATCH_YELLOW_FIRST | unit_economics, repeat_orders, waste_rate_control, fcf_path | cash_burn, waste_rate, delivery_cost, profitability_delay |
| `K_BEAUTY_EXPORT_DISTRIBUTION` | GREEN_POSSIBLE | export_growth, channel_diversification, sell_through, repeat_orders, opm_roe_improvement | tariff, china_dependency, inventory_build, receivables_growth, sell_through_failure |
| `BEAUTY_OEM_ODM_SUPPLYCHAIN` | GREEN_POSSIBLE | customer_diversification, repeat_orders, capacity_utilization, opm_improvement | inventory_build, receivables_growth, customer_concentration, sell_through_failure |
| `APPAREL_FAST_FASHION_BRAND_OEM` | WATCH_YELLOW_FIRST | order_visibility, inventory_turnover, discount_rate_control, opm_improvement | ip_litigation, regulatory_enforcement, unsafe_products, inventory_buildup, discounting |
| `HOME_LIVING_APPLIANCE_RENTAL` | WATCH_YELLOW_FIRST | rental_accounts, churn_stable, recurring_service_revenue, fcf_improvement | hardware_cycle, housing_cycle, consumer_sentiment, dividend_cut, quality_recall |
| `HOME_CHILD_EDUCATION` | REDTEAM_FIRST | recurring_demand, channel_expansion, opm_improvement | low_birth_rate, tam_decline, policy_regulation |
| `CONSUMER_REGULATED_PRODUCT` | WATCH_YELLOW_FIRST | legal_revenue, approval, repeat_revenue, margin_visibility | regulatory_ban, social_backlash, product_safety_issue |

## What Not To Change

- Do not apply these R5 v1.0 weights to production scoring yet.
- Do not treat viral traffic, GMV, store count, user count, product hype, or listing expectation as score evidence by themselves.
- Do not invent export growth, sell-through, inventory, receivables, churn, rental accounts, OPM, FCF, or price-path fields.
- Do not lower Stage 3-Green for consumer stories. Green requires repeat demand, channel expansion, OPM/FCF, and clean inventory/receivables.
- Treat recall, food safety, supplier regulation, data breach, IP litigation, product safety, and hardware replacement-cycle failure as RedTeam evidence.
