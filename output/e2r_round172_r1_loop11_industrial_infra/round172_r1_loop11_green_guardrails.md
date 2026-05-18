# Round-172 R1 Loop-11 Green Guardrails

| target | posture | Green unlock evidence | Loop-11 penalties |
| --- | --- | --- | --- |
| `GRID_TRANSFORMER_SHORTAGE_KOREA` | GREEN_POSSIBLE | op_eps_fcf_revision, backlog_quality, margin_visible, price_path_aligned, valuation_room_remaining | capa_normalization, valuation_crowding, raw_material_cost, project_delay |
| `GRID_US_LOCALIZATION_CAPA` | WATCH_YELLOW_FIRST | us_local_capa, hvdc_option, margin_visible, op_eps_revision | local_capa_capex, utilization, margin_unknown |
| `POWER_EQUIPMENT_BACKLOG_TO_FCF_KOREA` | GREEN_POSSIBLE | fcf_conversion, margin_sustained, backlog_quality, op_eps_revision | low_margin_backlog, fcf_miss, valuation_crowding |
| `SHIPBUILDING_US_PLATFORM_RESTRUCTURING` | WATCH_YELLOW_FIRST | actual_contract, margin_visible, yard_execution, op_eps_revision | mna_event_only, margin_unknown, contract_missing |
| `SHIP_MRO_RECURRING_PLATFORM` | WATCH_YELLOW_FIRST | recurring_revenue, opm_sustained, fcf_visible, customer_diversified | ipo_premium, overhang, fcf_missing |
| `NUCLEAR_EXPORT_PREFERRED_BIDDER` | WATCH_YELLOW_FIRST | final_contract, scope_confirmed, op_eps_revision, margin_visible | preferred_bidder_only, legal_gate, scope_unknown |
| `DEFENSE_AIRCRAFT_EXPORT_BACKLOG` | WATCH_YELLOW_FIRST | contract_amount, delivery_schedule, government_customer, margin_visible, op_eps_revision | margin_unknown, delivery_delay, warranty_cost |
| `DEFENSE_INTERCEPTOR_COMBAT_VALIDATION` | WATCH_YELLOW_FIRST | actual_contract, contract_amount, delivery_schedule, op_eps_revision | actual_contract_missing, war_event_only, valuation_crowding |
| `GEOPOLITICAL_SHIPBUILDING_SANCTION_OVERLAY` | REDTEAM_FIRST |  | sanction, export_control, geopolitical_retaliation |
| `MOU_LOI_NOT_CONTRACT` | REDTEAM_FIRST |  | loi_only, mou_only, detail_missing |
| `DISCLOSURE_CONFIDENCE_CAP` | REDTEAM_FIRST | contract_value, contract_duration, counterparty, delivery_schedule, margin_visible | disclosure_confidence_capped, detail_missing, margin_unknown |
| `NUCLEAR_EXPORT_LEGAL_GATE` | REDTEAM_FIRST |  | appeal_pending, contract_signing_block, ip_dispute |

## What Not To Change

- Do not apply R1 Loop-11 v11.0 weights to production scoring yet.
- Do not lower Stage 3-Green thresholds because Korea R1 has strong winners.
- Do not use Round 172 case records as candidate-generation input.
- Do not treat preferred bidder, LOI, MOU, merger, IPO premium, or combat validation as Stage 3-Green by itself.
- Do not invent contract amounts, counterparties, delivery schedules, margins, stage prices, MFE/MAE, or valuation bands.
- Apply 4B-watch when price and consensus move faster than revisions.
- Apply 4C/hard review for legal gates, sanctions, contract cancellation/correction, dilution, or disclosure failures.
