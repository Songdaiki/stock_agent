# Round-175 R4 Loop-11 Green Guardrails

| target | posture | Green unlock evidence | Loop-11 penalties |
| --- | --- | --- | --- |
| `COPPER_AI_GRID_KOREA` | WATCH_YELLOW_FIRST | order_backlog, copper_passthrough, opm, op_eps_revision, fcf | commodity_cycle, individual_order_missing, opm_missing |
| `COPPER_PROCESSING_PLUS_DEFENSE` | WATCH_YELLOW_FIRST | actual_sale_contract, defense_backlog, processing_margin, op_eps_revision, fcf | mna_event, confirmation, processing_margin |
| `DEFENSE_AMMO_EVENT_PREMIUM` | REDTEAM_FIRST |  | mna_rumor, final_terms_missing, unwind |
| `POLYSILICON_NON_CHINA_SUPPLY_OPTION` | WATCH_YELLOW_FIRST | confirmed_contract, amount, period, volume, asp_opm, fcf | confirmation, contract_terms, polysilicon_cycle |
| `POLYSILICON_REPORT_NOT_CONTRACT` | REDTEAM_FIRST |  | report_only, confirmation, terms |
| `STEEL_TARIFF_EVENT_KOREA` | WATCH_YELLOW_FIRST | asp, export_volume, opm, fcf, cost_control | tariff_scope, export_exposure, cost_control |
| `STEEL_EXPORT_TARIFF_4C` | REDTEAM_FIRST |  | tariff_scope, export_exposure, local_production |
| `SPECIALTY_STEEL_US_LOCALIZATION_OPTION` | WATCH_YELLOW_FIRST | local_revenue, margin, tariff_offset, op_eps_revision, fcf | localization, margin, volume |
| `LITHIUM_PRICE_EVENT_KOREA` | REDTEAM_FIRST |  | event_rally, production, fcf, cash_burn |
| `RARE_EARTH_THEME_KOREA` | REDTEAM_FIRST |  | theme_only, revenue, offtake, dilution |
| `CHEMICAL_SPREAD_KOREA` | REDTEAM_FIRST | durable_spread, volume, opm, fcf, low_cost_position | spread, inventory, volume, china_supply |
| `EVENT_PREMIUM_GOVERNANCE_OVERLAY` | REDTEAM_FIRST |  | event_premium, final_terms, unwind |
| `DISCLOSURE_CONFIDENCE_CAP` | REDTEAM_FIRST | counterparty, amount, period, offtake_volume, price_floor, opm_fcf | disclosure_detail, confirmation, terms |

## What Not To Change

- Do not apply R4 Loop-11 v11.0 weights to production scoring yet.
- Do not lower Stage 3-Green thresholds because a commodity or steel basket moved.
- Do not use Round 175 case records as candidate-generation input.
- Do not treat copper price, steel tariff, rare-earth export control, lithium rebound, non-China polysilicon, M&A rumor, or SpaceX name as Green by itself.
- Do not invent contract amount, counterparty, period, offtake volume, price floor, tariff scope, stage prices, MFE/MAE, OPM, FCF, or commodity price exposure.
- Apply 4B-watch when commodity, tariff, export-control, or M&A event rallies outrun OP/EPS revision.
- Apply 4C/hard review for M&A review dropped, sale denial, media-only contract, direct export tariff, spread reversal, inventory loss, OP/EPS downgrade, CB/BW, or production/export volume decline.
