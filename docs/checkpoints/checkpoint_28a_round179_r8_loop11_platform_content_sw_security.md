# Checkpoint 28A Round 179: R8 Loop 11 Korea Platform / Content / Software / Security

## Scope

- source_round: `docs/round/round_179.md`
- large_sector: `PLATFORM_CONTENT_SW_SECURITY`
- loop: `R8 Loop 11 / v11.0`
- production_scoring_changed: false
- case_records_are_candidate_generation_input: false

Round 179 narrows platform/content/software/security calibration to Korea-focused AI cloud, ERP/SaaS, Webtoon, game IP, K-pop, privacy/security, legal, and guidance-risk cases. The core rule is simple: AI, IP, IPO, MAU, strategic-investor, or K-pop headlines can open Stage 1/2, but Stage 3-Green requires ARR, bookings, cloud revenue, ad/IP revenue, live-service revenue, OPM, FCF, retention, clean security/legal status, and price-path support.

Example: `AI cloud` is useful Stage 2 evidence. It is not enough for Green if paid cloud revenue, ARR, OPM/FCF, and dilution discipline are missing.

## Outputs

- `data/e2r_case_library/cases_r8_loop11_round179.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round179_r8_loop11_v11.csv`
- `output/e2r_round179_r8_loop11_platform_content_sw_security/round179_r8_loop11_platform_content_sw_security_summary.md`
- `output/e2r_round179_r8_loop11_platform_content_sw_security/round179_r8_loop11_case_matrix.csv`
- `output/e2r_round179_r8_loop11_platform_content_sw_security/round179_r8_loop11_stage_date_plan.csv`
- `output/e2r_round179_r8_loop11_platform_content_sw_security/round179_r8_loop11_green_guardrails.md`
- `output/e2r_round179_r8_loop11_platform_content_sw_security/round179_r8_loop11_risk_overlays.md`
- `output/e2r_round179_r8_loop11_platform_content_sw_security/round179_r8_loop11_price_validation_plan.md`
- `output/e2r_round179_r8_loop11_platform_content_sw_security/round179_r8_loop11_score_stage_price_alignment.md`

## Added Targets

- source canonical targets: 14
- total score targets: 14
- case candidates: 12
- base score components: 7
- stage caps: 5

The added targets cover Samsung SDS-style enterprise AI cloud, Douzone-style ERP/SaaS workflow, PE software rerating, AI cloud capital allocation, NAVER sovereign AI, Webtoon IP monetization, platform privacy/security, game repeat monetization, single-IP game event premium, game launch/legal risk, K-pop platform IP, entertainment governance/legal risk, ad/content guidance risk, and disclosure confidence caps.

## Guardrails

- Do not use these case records as candidate-generation input.
- Do not apply Round 179 weights to production scoring yet.
- Do not treat AI feature, game IP, Webtoon IPO, K-pop IP, platform MAU, strategic investor, or M&A headline as Stage 3 evidence.
- Do not invent ARR, bookings, cloud revenue, ad revenue, IP revenue, OPM, FCF, churn, retention, stage prices, or MFE/MAE.
- Security incident, privacy leak, founder legal risk, release delay, lawsuit, guidance miss, IP adaptation miss, and platform governance conflict remain RedTeam gates.

## Validation

Commands run:

```bash
PYTHONPATH=src python -m unittest tests.test_round179_r8_loop11_platform_content_sw_security -v
PYTHONPATH=src python -m e2r.cli.build_round179_r8_loop11_report
```

Result:

- Round 179 unit tests passed.
- Case JSONL and score-profile CSV were generated.
- Report outputs were generated.

Full repository validation and commit/push were performed after this checkpoint patch.
