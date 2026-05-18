# Checkpoint 28A Round 178: R7 Loop 11 Korea Biotech / Healthcare / Medical Device

## Scope

- source_round: `docs/round/round_178.md`
- large_sector: `BIOTECH_HEALTHCARE_DEVICE`
- loop: `R7 Loop 11 / v11.0`
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

Round 178 narrows healthcare calibration to Korea-focused cases such as 알테오젠, 유한양행, 셀트리온, 휴젤, 클래시스, 삼천당제약, ABL바이오, and 루닛/JLK/딥노이드-style medical AI. The main rule is simple: approval, license, partner name, or AI performance can open Stage 1/2, but Stage 3-Green requires commercialization evidence such as royalty revenue, scripts, reimbursement, repeat procedure revenue, commercial sales, OPM, FCF, or EPS revision.

Example: `FDA approval` is useful Stage 2 evidence. It is not enough for Green if royalty revenue, actual adoption, or reimbursement is missing.

## Outputs

- `data/e2r_case_library/cases_r7_loop11_round178.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round178_r7_loop11_v11.csv`
- `output/e2r_round178_r7_loop11_biotech_healthcare_device/round178_r7_loop11_biotech_healthcare_device_summary.md`
- `output/e2r_round178_r7_loop11_biotech_healthcare_device/round178_r7_loop11_case_matrix.csv`
- `output/e2r_round178_r7_loop11_biotech_healthcare_device/round178_r7_loop11_stage_date_plan.csv`
- `output/e2r_round178_r7_loop11_biotech_healthcare_device/round178_r7_loop11_green_guardrails.md`
- `output/e2r_round178_r7_loop11_biotech_healthcare_device/round178_r7_loop11_risk_overlays.md`
- `output/e2r_round178_r7_loop11_biotech_healthcare_device/round178_r7_loop11_price_validation_plan.md`
- `output/e2r_round178_r7_loop11_biotech_healthcare_device/round178_r7_loop11_score_stage_price_alignment.md`

## Added Targets

- source canonical targets: 14
- helper overlay targets: 1
- total score targets: 15
- case candidates: 12
- base score components: 7
- stage caps: 5

The added targets cover SC royalty platforms, blockbuster life-extension royalties, Korea oncology commercialization, biosimilar manufacturing/commercialization, botulinum US entry, aesthetic-device export, license/milestone platforms, GLP-1 generic themes, medical AI reimbursement, approval-only caps, CMC/CRL overlays, patent overlays, disclosure caps, and device safety/channel overlays.

## Guardrails

- Do not use these case records as candidate-generation input.
- Do not apply Round 178 weights to production scoring yet.
- Do not treat approval/license/AI performance as commercialization.
- Do not invent contract amount, upfront, milestone, royalty rate, prescription volume, reimbursement, commercial sales, procedure volume, stage prices, or MFE/MAE.
- CRL, manufacturing inspection, patent challenge, reimbursement failure, safety issue, counterfeiting/off-label channel, cash runway, and dilution remain RedTeam gates.

## Validation

Commands run:

```bash
PYTHONPATH=src python -m unittest tests.test_round178_r7_loop11_biotech_healthcare_device -v
PYTHONPATH=src python -m e2r.cli.build_round178_r7_loop11_report
```

Result:

- Round 178 unit tests passed.
- Case JSONL and score-profile CSV were generated.
- Report outputs were generated.

Full repository validation and commit/push were performed after this checkpoint patch.
