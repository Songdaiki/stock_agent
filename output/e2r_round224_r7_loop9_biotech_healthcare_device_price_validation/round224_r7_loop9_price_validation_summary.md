# Round 224 R7 Loop 9 Biotech Healthcare Device Price Validation

This pack is calibration-only. Production scoring and candidate generation are unchanged.

## Summary

- source_round: docs/round/round_224.md
- large_sector: BIOTECH_HEALTHCARE_DEVICE
- cases: 7
- success_candidate: 5
- event_premium: 1
- failed_rerating: 1
- Stage 3 dated cases: 0
- 4B-watch cases: 7
- hard_4c_case_count: 0
- full_ohlc_complete: false

## Case Matrix

| case | company | type | stage2 | stage3 | 4B | 4C | alignment | note |
|---|---|---|---|---|---|---|---|---|
| r7_loop9_alteogen_keytruda_qlex_commercialization | 알테오젠 | success_candidate | 2025-09-19 |  |  |  | unknown | Qlex commercial sales validate the Stage 2-to-3 path, but Alteogen royalty recognition and cash receipt are required before Stage 3 confirmation. |
| r7_loop9_yuhan_lazcluze_approval_royalty_watch | 유한양행 | success_candidate | 2024-08-20 |  |  | 2024-12-16 | unknown | Approval is Stage 2; prescription volume, J&J product sales, Yuhan royalty recognition, and EPS revision are required for Stage 3. |
| r7_loop9_sk_bioscience_idt_cmo_mna | SK바이오사이언스 | event_premium | 2024-06-27 |  | 2024-06-27 |  | price_moved_without_evidence | IDT acquisition is Stage 2/event premium; utilization, backlog, margin, and FCF are required before Green. |
| r7_loop9_celltrion_us_factory_tariff_hedge | 셀트리온 | success_candidate | 2025-09-23 |  |  |  | unknown | U.S. facility is Stage 2 tariff-hedge evidence; product transfer, utilization, margin, and FCF decide promotion. |
| r7_loop9_samsung_biologics_gsk_facility_price_failed | 삼성바이오로직스 | success_candidate | 2025-12-22 |  |  |  | evidence_good_but_price_failed | Good U.S. CDMO capacity event but immediate price reaction failed; utilization/contract transfer is needed for a fresh Stage 3 path. |
| r7_loop9_hugel_letybo_us_launch | 휴젤 | success_candidate | 2025-03-01 |  |  |  | unknown | U.S. launch is Stage 2; U.S. sales, channel penetration, ASP, repeat order, and OPM are required before Green. |
| r7_loop9_lunit_medical_ai_external_validation | 루닛 | failed_rerating | 2025-03-17 |  |  |  | unknown | External validation is Stage 2 evidence; reimbursement, hospital adoption, recurring revenue, gross margin, and cash runway are required before Green. |

## Interpretation
- Alteogen is the strongest R7 commercialization watch, but Stage 3 waits for Alteogen royalty recognition and cash receipt.
- Yuhan and Hugel are Stage 2 until prescriptions, sales, royalties, channel penetration, and reimbursement confirm.
- SK Bioscience IDT is Stage 2/event premium because M&A without utilization is not Green.
- Celltrion and Samsung Biologics U.S. facility events need product transfer, utilization, margin, and FCF.
- Lunit external validation is not Green without reimbursement, hospital adoption, recurring revenue, and cash runway.
