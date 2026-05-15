# Round-36 Archetype Price Validation Plan

Round 36 separates validation by archetype behavior rather than by theme name.

| target | validation_group | metrics | success | failure |
|---|---|---|---|---|
| GRID_TRANSFORMER_SHORTAGE | green_possible | mfe_90d, mfe_180d, mfe_1y, mfe_2y, mae_90d, op_eps_revision, backlog_growth, per_pbr_band | Stage 2/3 after order backlog and OP/EPS revisions should align with 6-24 month rerating. | Theme rally without OP/EPS or margin follow-through becomes false_positive_score. |
| ANIMAL_HEALTH_BIOSECURITY | cycle_event | mfe_30d, mfe_90d, post_event_drawdown, next_year_revenue_retention, inventory_oneoff_check | Recurring vaccine or biosecurity revenue after the event can support Watch-to-Green. | Disease headline rally that normalizes with no recurring revenue is one_off_event. |
| TELEHEALTH_BEHAVIORAL_HEALTH | watch_to_green | revenue_growth, cac_to_revenue, fcf_margin, churn, privacy_event_drawdown, mfe_90d, mae_1y | Revenue growth plus improving FCF and stable CAC can align. | DTC growth with CAC, impairment, or privacy drawdown becomes false_positive_score. |
| PRECIOUS_METALS_SAFE_HAVEN_MINERS | cycle_event | gold_relative_return, aisc_change, fcf_yield, capital_return, drawdown_after_commodity_peak | Gold price, cost discipline, FCF, and capital return moving together can align as cyclical_success. | Gold price headline without cost/production/FCF support becomes false_positive_score. |
| SERVICE_KIOSK_SELF_CHECKOUT | watch_to_green | hardware_vs_recurring_revenue, gross_margin, renewal_rate, shrink_change, mfe_180d, mae_180d | Recurring maintenance, payment, or software economics can support Watch-to-Green. | One-off hardware or retailer rollback after theft/customer friction is one_off_hardware. |
| OPTICAL_NETWORKING_AI_DATACENTER | green_possible | mfe_90d, mfe_180d, mfe_1y, op_eps_revision, customer_concentration, valuation_multiple, drawdown_after_4b | Contract, OP/EPS revision, and rerating moving together are aligned. | AI optical theme rally without order/EPS support is price_moved_without_evidence. |
| AI_GRID_FLEXIBILITY_SOFTWARE | watch_to_green | contract_to_revenue, arr_or_recurring_revenue, opm_improvement, theme_drawdown, mfe_1y, mae_1y | PoC converting into recurring contracts and revenue can support Watch-to-Green. | Research or policy headline without revenue is theme_watch or false_positive. |
| PHARMA_CHANNEL_AND_PRIVACY_RISK | red_flag | cac_to_revenue, fcf_margin, privacy_legal_drawdown, churn, mfe_1y, mae_1y | B2B contracts, low CAC, privacy compliance, legal channels, and FCF can align. | DTC growth followed by privacy/CAC/impairment is 4C-style failure. |

## Group Rules
- green_possible: compare Stage 2/3 dates with MFE/MAE, revision persistence, and valuation-band changes.
- watch_to_green: require recurring revenue, margin/FCF improvement, and customer retention before Green-like interpretation.
- cycle_event: report cyclical_success separately from structural_success and track drawdown after peak.
- red_flag: treat privacy, regulation, CAC, and legal events as thesis-break candidates before promotion.
