# Round-187 R3 Loop-12 Risk Overlays

| target | hard gate | red flags |
| --- | --- | --- |
| `EV_TO_ESS_CAPACITY_REDEPLOYMENT_KOREA` | false | profit_ex_subsidy_weak, utilization_missing, ev_slowdown, contract_cancellation |
| `BATTERY_CONTRACT_CANCELLATION_4C` | true | contract_cancelled, customer_strategy_risk, revenue_loss, expected_revenue_loss |
| `BATTERY_TAX_CREDIT_QUALITY_OVERLAY` | false | profit_ex_subsidy_weak, policy_dependency, core_margin_missing |
| `SEPARATOR_EV_DEMAND_CYCLE` | false | sale_review, ev_slowdown, parent_loss, utilization_missing |
| `COPPER_FOIL_EV_DEMAND_CYCLE` | false | ev_slowdown, utilization_missing, opm_missing |
| `ELECTROLYTE_CAPA_SUPPLYCHAIN` | false | customer_missing, opm_missing, capa_before_demand |
| `BATTERY_EQUIPMENT_CAPEX_CYCLE` | false | capex_delay, order_pushout, shipment_missing |
| `BATTERY_RECYCLING_UNIT_ECONOMICS` | false | unit_economics_missing, metal_price_risk, volume_missing |
| `SODIUM_ION_NEXTGEN_MATERIALS` | false | commercial_customer_missing, revenue_missing, cost_advantage_unproven |
| `HYDROGEN_FUEL_CELL_INFRA_KOREA` | false | customer_missing, opm_missing, subsidy_dependence |
| `SOLAR_US_LOCALIZATION_SUPPLYCHAIN` | false | customs_detention, uflpa_risk, production_disruption |
| `WIND_POLICY_PERMITTING_RISK` | true | permit_halt, lease_suspension, project_cancel |
| `BATTERY_SAFETY_INDUSTRIAL_ACCIDENT_OVERLAY` | true | fatal_accident, quality_failure, safety_management_failure |
| `EV_BATTERY_TRANSPARENCY_REGULATORY_OVERLAY` | true | supplier_disclosure_issue, consumer_trust_damage, regulatory_fine |
| `DISCLOSURE_CONFIDENCE_CAP` | false | opendart_list_only, media_only, mou_loi, detail_missing |

## Hard 4C Examples

- `BATTERY_CONTRACT_CANCELLATION_4C`: Ford/Freudenberg-style customer contract cancellations and expected revenue loss.
- `WIND_POLICY_PERMITTING_RISK`: permit halt, lease suspension, national-security review, and project delay.
- `BATTERY_SAFETY_INDUSTRIAL_ACCIDENT_OVERLAY`: fatal accident, quality failure, safety management failure, and criminal liability.
- `EV_BATTERY_TRANSPARENCY_REGULATORY_OVERLAY`: supplier disclosure issue, EV fire trust context, fine, and consumer trust damage.
- `DISCLOSURE_CONFIDENCE_CAP`: list-only, media-only, policy-only, factory-only, or missing utilization/OPM details cannot create Green.
