# Round-178 R7 Loop-11 Green Guardrails

| target | posture | Green unlock evidence | Loop-11 penalties |
| --- | --- | --- | --- |
| `SC_FORMULATION_ROYALTY_PLATFORM` | GREEN_POSSIBLE | royalty_revenue, actual_adoption, commercial_sales, op_eps_revision, stage2_60d_mfe_20pct | patent, royalty_missing, adoption_missing, valuation_4b |
| `BLOCKBUSTER_LIFE_EXTENSION_ROYALTY` | GREEN_POSSIBLE | royalty_revenue_recognition, actual_adoption, eps_revision, commercial_launch | adoption, payer, patent, valuation_4b |
| `KOREA_ONCOLOGY_DRUG_COMMERCIALIZATION` | GREEN_POSSIBLE | scripts, royalty_revenue, pbm_access, market_share, op_eps_revision | scripts, pbm, competition, safety |
| `BIOSIMILAR_TARIFF_HEDGE_MANUFACTURING` | WATCH_YELLOW_FIRST | facility_utilization, us_sales, pbm_formulary, opm_fcf_improvement | utilization, pbm, tech_transfer, capex |
| `BIOSIMILAR_COMMERCIALIZATION_KOREA` | GREEN_POSSIBLE | prescription_volume, pbm_formulary, commercial_sales, margin, op_eps_revision | patent, launch, pbm, margin |
| `BOTULINUM_US_MARKET_ENTRY` | GREEN_POSSIBLE | us_sales, market_share, repeat_aesthetic_procedure, op_eps_revision, licensed_channel | safety, channel, competition, penetration_missing |
| `AESTHETIC_DEVICE_EXPORT_KOREA` | GREEN_POSSIBLE | consumable_revenue, procedure_volume, export_sales, opm_fcf, channel_repeat_order | consumable_missing, safety, inventory, valuation |
| `BIOTECH_LICENSE_MILESTONE_PLATFORM` | WATCH_YELLOW_FIRST | milestone_receipt, royalty_visibility, clinical_progress, cash_runway_extended | milestone_missing, clinical, cash, dilution |
| `GLP1_GENERIC_THEME_KOREA` | REDTEAM_FIRST | commercial_sales, prescription_volume, patent_clearance, margin | patent, regulatory, commercial_sales_missing, theme_crowding |
| `MEDICAL_AI_REIMBURSEMENT_KOREA` | WATCH_YELLOW_FIRST | reimbursement_revenue, recurring_saas_revenue, repeat_hospital_usage, op_eps_revision | reimbursement, paid_deployment, revenue, cash_burn |
| `APPROVAL_ONLY_NOT_COMMERCIALIZATION` | REDTEAM_FIRST |  | approval_only, adoption, commercialization, disclosure |
| `MANUFACTURING_INSPECTION_CRL_OVERLAY` | REDTEAM_FIRST |  | cmc, inspection, approval_delay |
| `PATENT_CHALLENGE_OVERLAY` | REDTEAM_FIRST |  | patent, launch, royalty_window |
| `DISCLOSURE_CONFIDENCE_CAP` | REDTEAM_FIRST | contract_amount, royalty_rate, prescription_volume, reimbursement_status, commercial_sales | disclosure_detail, royalty, contract_amount, prescription, reimbursement |
| `DEVICE_SAFETY_CHANNEL_OVERLAY` | REDTEAM_FIRST |  | safety, channel, counterfeit, off_label |

## What Not To Change

- Do not apply R7 Loop-11 v11.0 weights to production scoring yet.
- Do not treat approval/license/AI performance, clinical result, partner name, FDA clearance, or SC formulation story as Green evidence by itself.
- Do not invent contract amount, upfront, milestone, royalty rate, prescription volume, reimbursement status, commercial sales, procedure volume, OPM/FCF, stage prices, or MFE/MAE.
- Green requires royalty, scripts, reimbursement, repeat sales, procedure/consumable revenue, commercial sales, OP/EPS revision, or FCF conversion with low RedTeam risk.
- CRL, CMC/manufacturing inspection, patent challenge, reimbursement failure, safety issue, counterfeiting/off-label channel, cash runway, and dilution remain RedTeam gates.
