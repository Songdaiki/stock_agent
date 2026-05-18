# Round-183 R12 Loop-11 Green Guardrails

| target | posture | Green unlock evidence | Loop-11 penalties |
| --- | --- | --- | --- |
| `AGRI_MACHINERY_EXPORT_CYCLE_KOREA` | WATCH_YELLOW_FIRST | opm_fcf_improvement, dealer_inventory_stable, parts_service_repeat_revenue, price_path_confirmed | dealer_inventory, farmer_capex_cycle, opm_fcf_backfill |
| `AGRI_MACHINERY_AUTONOMOUS_ROBOT_OPTION` | WATCH_YELLOW_FIRST | paid_order, recurring_software_or_service_revenue, farmer_roi_verified, op_eps_conversion | commercialization, farmer_roi, service_attach |
| `FERTILIZER_INPUT_PRICE_COST_KOREA` | REDTEAM_FIRST | price_pass_through, volume_maintained, opm_fcf_improvement, farmer_roi_maintained | input_cost, farmer_margin, volume, inventory |
| `LIVESTOCK_DISEASE_PRICE_EVENT_KOREA` | REDTEAM_FIRST |  | one_off_disease, price_normalization, feed_cost, consumer_backlash |
| `FEED_GRAIN_COST_PASS_THROUGH` | WATCH_YELLOW_FIRST | feed_cost_pass_through, volume_stable, opm_fcf_improvement | grain_cost, pass_through, volume, receivables |
| `TUNA_FISHERY_GLOBAL_BRAND_LEGAL_RISK` | WATCH_YELLOW_FIRST | brand_opm, legal_cost_normalized, fcf_improvement | legal, fuel, quota, fx |
| `CONSUMER_REGULATED_PRODUCT_KOREA` | GREEN_POSSIBLE | opm_fcf_maintained, recurring_consumption, shareholder_return, public_health_gate_passed | public_health, tax, youth_safety, regulatory_scope |
| `HEATED_TOBACCO_GLOBAL_DISTRIBUTION` | WATCH_YELLOW_FIRST | ngp_overseas_revenue_growth, opm_fcf_maintained, regulatory_stability | public_health, ngp_sales, regulatory_scope, youth_safety |
| `EDUCATION_POLICY_EVENT_KOREA` | WATCH_YELLOW_FIRST | repeat_enrollment, paid_conversion, cac_stable, opm_fcf_improvement | policy_reversal, student_count, ai_tutor, cac |
| `EDTECH_AI_DISRUPTION_KOREA` | REDTEAM_FIRST |  | cannibalization, cac, paid_conversion, bookings |
| `KIDS_IP_PLATFORM_KOREA` | WATCH_YELLOW_FIRST | multi_ip_revenue, opm_fcf_maintained, post_ipo_guidance_met | one_hit, ipo_premium, direct_earnings_link, guidance |
| `SMART_FARM_UNIT_ECONOMICS_KOREA` | WATCH_YELLOW_FIRST | unit_economics_verified, opm_fcf_positive, repeat_order | unit_economics, energy_cost, capex, cash_runway |
| `SERVICE_KIOSK_LOCAL_REGULATION_KOREA` | WATCH_YELLOW_FIRST | maintenance_or_fee_revenue, opm_fcf_improvement, regulatory_accessibility_compliance | maintenance_revenue, fee_revenue, local_regulation, security |
| `DISCLOSURE_CONFIDENCE_CAP` | REDTEAM_FIRST | repeat_revenue_detail, unit_economics_detail, regulatory_scope_detail, opm_fcf_detail | disclosure, detail, unit_economics, parser_confidence |

## What Not To Change

- Do not apply R12 Loop-11 v11.0 weights to production scoring yet.
- Do not treat agriculture, disease-beneficiary, medical-quota, AI education, smart-farm, heated-tobacco, or kids-IP headlines as Green evidence by themselves.
- Do not invent stage prices, MFE/MAE, OPM, FCF, unit economics, repeat revenue, contracts, regulatory scope, or price pass-through.
- Green requires repeat revenue or contract, OPM/FCF conversion, unit economics, price pass-through, and legal/regulatory stability.
- OpenDART list-only evidence is insufficient; detail fetch should stay limited to watch disclosures.
