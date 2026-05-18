# Round-182 R11 Loop-11 Green Guardrails

| target | posture | Green unlock evidence | Loop-11 penalties |
| --- | --- | --- | --- |
| `DOMESTIC_RESOURCE_DISCOVERY_EVENT` | WATCH_YELLOW_FIRST | commercial_discovery, development_plan, commercial_production_or_long_term_contract, op_eps_fcf_reflected | drill_bit, commerciality, time_to_revenue, success_probability |
| `RESOURCE_EXPLORATION_DRILL_BIT_GATE` | REDTEAM_FIRST |  | failure_probability, commerciality, reserve_unconfirmed, fid_missing |
| `ENERGY_SECURITY_POLICY_EVENT` | WATCH_YELLOW_FIRST | company_revenue_path, contract_or_margin_impact, op_eps_fcf_conversion | import_cost, policy_reversal, exploration, margin |
| `MARKET_STRUCTURE_SHORT_SELLING_POLICY` | WATCH_YELLOW_FIRST | brokerage_revenue_or_roe_link, trading_value_sustained, company_eps_fcf_conversion | fundamental_link_missing, price_only_squeeze, resumption, foreign_access |
| `SHORT_SELLING_RESUMPTION_RISK` | REDTEAM_FIRST |  | short_squeeze, valuation, resumption, liquidity |
| `POLITICAL_SYSTEM_SHOCK_KOREA` | REDTEAM_FIRST |  | political_risk, fx, foreign_flow, valuation_room |
| `GEOPOLITICAL_ENERGY_IMPORT_SHOCK` | REDTEAM_FIRST |  | oil_import_dependency, fx, market_mae, input_cost |
| `EVENT_PRICE_RALLY_NOT_STAGE3` | REDTEAM_FIRST |  | price_only, crowding, no_revenue, detail_missing |
| `POLICY_DIRECTIONALITY_ERROR` | REDTEAM_FIRST |  | directionality, beneficiary_mapping, policy_reversal, no_exposure |
| `DISCLOSURE_CONFIDENCE_CAP` | REDTEAM_FIRST | budget_contract_order_detail, exploration_result, guidance_detail, company_conversion | disclosure, detail, guidance, parser_confidence |

## What Not To Change

- Do not apply R11 Loop-11 v11.0 weights to production scoring yet.
- Do not treat policy announcement, exploration headline, short-selling ban, political event, or war shock as Green evidence by itself.
- Do not invent contracts, budgets, government orders, exploration results, guidance, stage prices, or MFE/MAE.
- Green requires actual money/result plus company revenue, OP/EPS, FCF, recurrence, and low policy reversal risk.
- Price-only rallies, drill-bit risk, policy reversal, martial-law shock, energy-import shock, and low disclosure confidence remain RedTeam gates.
