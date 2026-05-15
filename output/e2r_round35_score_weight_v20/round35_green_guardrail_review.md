# Round-35 Green Guardrail Review

| target | posture | Green unlock evidence | Red flags |
|---|---|---|---|
| BIOSIMILAR_COMMERCIALIZATION | WATCH_YELLOW_FIRST | payer_or_pbm_adoption, prescription_volume_growth, manufacturing_cost_advantage, margin_defense | price_competition, payer_adoption, pbm_incentive, margin_pressure, approval_only |
| OBESITY_GLP1_COMMERCIALIZATION | GREEN_POSSIBLE | prescription_volume_growth, reimbursement_expansion, supply_capacity, op_eps_revision | competition, reimbursement, supply, compounded_drugs, advertising_regulation |
| GENE_THERAPY_RARE_DISEASE | REDTEAM_FIRST | patient_uptake, reimbursement_coverage, commercialization_numbers_visible, cash_runway | commercialization_slow, reimbursement, cash_burn, manufacturing, safety, approval_only |
| AI_DRUG_DISCOVERY_PLATFORM | REDTEAM_FIRST | milestone_revenue, clinical_entry, cash_runway, pipeline_diversification | clinical_failure, no_approved_drug, cash_burn, data_quality, platform_hype |
| CONTACT_CENTER_AI_AUTOMATION | GREEN_POSSIBLE | arr_growth, seat_expansion, enterprise_retention, opm_or_fcf_improvement | churn, it_budget, privacy, ai_error, seat_contraction, poc_only |
| SERVICE_KIOSK_SELF_CHECKOUT | WATCH_YELLOW_FIRST | installed_base_growth, maintenance_recurring_revenue, payment_or_software_revenue, loss_prevention_effect | theft, customer_friction, regulation, one_off_hardware, maintenance_cost, pseudo_automation |
| BIOSIMILAR_ORIGINATOR_DEFENSE | WATCH_YELLOW_FIRST | successor_revenue_growth, blockbuster_dependence_down, pipeline_diversification, eps_fcf_defense | patent_cliff, biosimilar_erosion, pipeline_failure, pricing_pressure, successor_absent |
| PHARMA_PLATFORM_REGULATORY_RISK | REDTEAM_FIRST | legal_distribution_channel, quality_control, regulatory_clarity, recurring_prescription_revenue | fda_warning, compounding_quality, illegal_pharmacy, advertising_rule, liability, gray_channel |

## What Not To Change
- Do not apply v2.0 weights to production scoring yet.
- Do not use case IDs, drug names, platform labels, or automation headlines as candidate-generation input.
- Do not invent stage dates, prices, prescription counts, payer access, reimbursement, ARR, seats, ROI, or unit economics.
- Do not lower Stage 3-Green thresholds to improve healthcare or AI-service recall.
