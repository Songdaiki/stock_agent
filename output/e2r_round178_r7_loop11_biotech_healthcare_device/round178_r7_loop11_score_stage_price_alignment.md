# Round-178 R7 Loop-11 Score / Stage / Price Alignment

Round 178 checks whether Korea healthcare evidence moves from approval, partner, and AI-performance narratives into royalty, prescriptions, reimbursement, repeat revenue, and price-path confirmation.
This is calibration material only; it does not change production scoring.

| case | score-stage view | price-path signal | verdict | normalization adjustment |
| --- | --- | --- | --- | --- |
| `alteogen_keytruda_sc_royalty_stage3_candidate` | Stage 2 to Stage 3 candidate plus 4B watch | approval and partner evidence can precede royalty revenue, but stock may already have rerated | royalty_platform_requires_adoption_revenue_and_4b_cooling | give Stage 2/3 credit only after royalty/adoption; flag 4B when valuation moves first |
| `yuhan_lazertinib_oncology_commercialization_case` | Stage 2 to Stage 3 candidate | FDA approval and J&J partnership need scripts, PBM, and royalty follow-through | oncology_commercialization_requires_scripts | score FDA/partner in Stage 2; require scripts/royalty for Green |
| `samchundang_biosimilar_glp1_patent_watch_case` | Stage 2 / 4B watch | approval and partner claims can move price before patent and commercial sales | glp1_generic_patent_and_sales_gate | cap Green until patent/regulatory clearance and sales evidence exist |
| `medical_ai_reimbursement_korea_gate_case` | Stage 1 to Stage 2 only | AI clearance or validation is not paid deployment | medical_ai_reimbursement_required | cap before reimbursement, hospital paid usage, and recurring SaaS revenue |
| `jj_rybrevant_sc_crl_inspection_overlay_case` | 4C thesis-break overlay | SC formulation data is offset by manufacturing inspection CRL | cmc_crl_blocks_unsafe_green | hard-cap any approval expectation until inspection issue clears |

## What This Means

- Stage 3-Green remains strict. R7 Loop 11 adds better Stage 2/3 diagnostics, not weaker thresholds.
- The same event can be positive and risky: for example, Alteogen approval supports Stage 2/3 review while also requiring 4B cooling if price outruns royalty adoption.
