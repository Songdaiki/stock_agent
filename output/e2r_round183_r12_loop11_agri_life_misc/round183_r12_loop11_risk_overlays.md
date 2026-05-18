# Round-183 R12 Loop-11 Risk Overlays

| target | stage4c conditions | red flags |
| --- | --- | --- |
| `AGRI_MACHINERY_EXPORT_CYCLE_KOREA` | north_america_tractor_demand_slowdown, dealer_inventory_increase, grain_price_or_farm_income_weakness, financing_cost_delay | dealer_inventory_increase, farm_income_weakness, financing_cost_delay |
| `AGRI_MACHINERY_AUTONOMOUS_ROBOT_OPTION` | commercial_sales_missing, farmer_roi_missing, right_to_repair_or_service_backlash | commercial_sales_missing, farmer_roi_missing, service_backlash |
| `FERTILIZER_INPUT_PRICE_COST_KOREA` | grain_price_decline, farmer_purchase_delay, ammonia_urea_energy_cost_spike, inventory_loss | input_cost_spike, farmer_margin_risk, volume_missing, inventory_loss |
| `LIVESTOCK_DISEASE_PRICE_EVENT_KOREA` | disease_normalization, livestock_price_decline, feed_cost_rise, consumer_or_antitrust_backlash | disease_normalization, price_normalization, feed_cost_rise, antitrust_or_price_investigation |
| `FEED_GRAIN_COST_PASS_THROUGH` | grain_cost_spike_not_passed_through, livestock_demand_drop, margin_squeeze | cost_not_passed_through, demand_drop, margin_squeeze |
| `TUNA_FISHERY_GLOBAL_BRAND_LEGAL_RISK` | price_fixing_settlement, legal_reserve, fuel_cost_spike, fishery_quota_risk | legal_settlement, price_fixing, fuel_cost, quota |
| `CONSUMER_REGULATED_PRODUCT_KOREA` | public_health_regulation, tax_increase, youth_safety_controversy, advertising_or_flavor_restriction | public_health_regulation, tax_increase, youth_safety, advertising_restriction |
| `HEATED_TOBACCO_GLOBAL_DISTRIBUTION` | reduced_risk_claim_denied, public_health_warning, youth_safety_controversy, tax_or_display_restriction | public_health_warning, youth_safety, tax_or_display_restriction |
| `EDUCATION_POLICY_EVENT_KOREA` | policy_freeze_or_reversal, doctor_strike_policy_uncertainty, low_birth_rate, ai_tutor_substitution | policy_reversal, low_birth_rate, ai_substitution, opm_missing |
| `EDTECH_AI_DISRUPTION_KOREA` | ai_substitutes_core_service, tuition_price_pressure, cac_rise, content_commoditization | ai_substitution, price_pressure, cac_rise, content_commoditization |
| `KIDS_IP_PLATFORM_KOREA` | one_hit_ip_revenue_slowdown, post_ipo_guidance_miss, ip_dependency_high | one_hit_dependency, ipo_premium, guidance_miss |
| `SMART_FARM_UNIT_ECONOMICS_KOREA` | unit_economics_failure, energy_cost_spike, capex_burden, dilution_or_cash_burn | unit_economics_failure, energy_cost, capex_burden, cash_burn |
| `SERVICE_KIOSK_LOCAL_REGULATION_KOREA` | local_regulation, accessibility_rule_cost, security_or_payment_issue, merchant_demand_slowdown | local_regulation, accessibility_cost, security_issue, demand_slowdown |
| `DISCLOSURE_CONFIDENCE_CAP` | contract_detail_missing, repeat_revenue_missing, unit_economics_missing, regulatory_scope_missing, opm_fcf_missing | detail_missing, parser_confidence_low, opm_fcf_missing |

## Interpretation

- R12 is sensitive to legal settlement, public-health regulation, policy reversal, AI tutor substitution, disease normalization, input-cost squeeze, one-hit IP, and dealer inventory.
- Example: Pinkfong can have strong price-path but still needs one-hit and IPO-premium 4B checks.
- Example: Dongwon/StarKist brand cash flow needs legal-settlement RedTeam before higher-stage confidence.
