# Round-178 R7 Loop-11 Price Validation Plan

## Method

1. Assign stage dates only from source evidence.
2. Store stage-date close prices from official price data.
3. Calculate 60D/120D returns after Stage 2, plus MFE/MAE where price data exists.
4. Compare approval/partner/license evidence with royalty, scripts, reimbursement, procedure volume, commercial sales, OPM, FCF, safety, CMC, and patent events.
5. Keep missing stage prices and MFE/MAE null until official price backfill is available.

## Priority Case Checks

| case_id | target | stage marker | check |
| --- | --- | --- | --- |
| `alteogen_keytruda_sc_royalty_stage3_candidate` | `SC_FORMULATION_ROYALTY_PLATFORM` | 2025-09-19 | needs_krx_price_royalty_adoption_backfill |
| `yuhan_lazertinib_oncology_commercialization_case` | `KOREA_ONCOLOGY_DRUG_COMMERCIALIZATION` | 2024-08-20 | needs_scripts_royalty_price_backfill |
| `celltrion_us_factory_tariff_hedge_stage2_case` | `BIOSIMILAR_TARIFF_HEDGE_MANUFACTURING` | 2025-09-23 | needs_utilization_us_sales_pbm_price_backfill |
| `hugel_letybo_us_market_entry_case` | `BOTULINUM_US_MARKET_ENTRY` | undated | needs_us_sales_market_share_price_backfill |
| `classys_aesthetic_device_export_consumable_case` | `AESTHETIC_DEVICE_EXPORT_KOREA` | undated | needs_consumable_export_opm_price_backfill |
| `ablbio_lilly_license_milestone_platform_case` | `BIOTECH_LICENSE_MILESTONE_PLATFORM` | undated | needs_milestone_clinical_cash_price_backfill |
| `samchundang_biosimilar_glp1_patent_watch_case` | `BIOSIMILAR_COMMERCIALIZATION_KOREA` | undated | needs_patent_clearance_sales_price_backfill |
| `jj_rybrevant_sc_crl_inspection_overlay_case` | `MANUFACTURING_INSPECTION_CRL_OVERLAY` | 2024-12-16 | needs_reference_price_backfill |
| `merck_keytruda_qlex_approval_price_failed_case` | `APPROVAL_ONLY_NOT_COMMERCIALIZATION` | 2025-09-19 | needs_reference_price_backfill |
| `medical_ai_reimbursement_korea_gate_case` | `MEDICAL_AI_REIMBURSEMENT_KOREA` | undated | needs_reimbursement_revenue_price_backfill |
| `device_safety_channel_overlay_case` | `DEVICE_SAFETY_CHANNEL_OVERLAY` | undated | needs_safety_channel_price_backfill |
| `biotech_disclosure_confidence_cap_case` | `DISCLOSURE_CONFIDENCE_CAP` | undated | needs_detail_disclosure_backfill |

## Alignment Labels

- `ROYALTY_PLATFORM_REQUIRES_ADOPTION`: SC/royalty platforms need actual adoption and royalty revenue.
- `ONCOLOGY_COMMERCIALIZATION_REQUIRES_SCRIPTS`: oncology approval needs scripts, PBM/access, market share, and royalty.
- `GLP1_GENERIC_PATENT_AND_SALES_GATE`: generic GLP-1 stories need patent clearance and sales.
- `MEDICAL_AI_REIMBURSEMENT_REQUIRED`: AI validation needs reimbursement and recurring revenue.
- `CMC_CRL_BLOCKS_UNSAFE_GREEN`: manufacturing inspection or CRL blocks approval-driven Green.
