# Checkpoint 28A Round 61: R8 Loop 2 Platform/Content/SW/Security

Round 61 adds the R8 Loop-2 calibration pack for platform, content, software, and security.

This is calibration and evaluation material only. It does not change production scoring, StageClassifier thresholds, or candidate generation.

## What Changed

- Added `src/e2r/sector/round61_r8_loop2_platform_content_sw_security.py`.
- Added `src/e2r/cli/build_round61_r8_loop2_report.py`.
- Added `tests/test_round61_r8_loop2_platform_content_sw_security.py`.
- Generated:
  - `data/e2r_case_library/cases_r8_loop2_round61.jsonl`
  - `data/sector_taxonomy/score_weight_profiles_round61_r8_loop2_v2.csv`
  - `output/e2r_round61_r8_loop2_platform_content_sw_security/`

## Core Rule

R8 must not score user count, AI feature launches, game-title expectations, ad-cycle recovery, cybersecurity demand, NFT, or metaverse tags as Stage 3 evidence by themselves.

Simple example:

- Weak evidence: “AI feature launched.”
- Stronger evidence: “AI workflow is paid, enterprise customers renew, compute cost is controlled, and FCF improves.”

## Target Coverage

Round 61 covers 14 targets:

- `PLATFORM_SOFTWARE_INTERNET`
- `CLOUD_AI_SOFTWARE_INFRA`
- `AI_SOFTWARE_APPLICATION`
- `GENERATIVE_AI_IP_RISK`
- `CONTACT_CENTER_AI_AUTOMATION`
- `SERVICE_KIOSK_SELF_CHECKOUT`
- `GAME_CONTENT_IP`
- `MEDIA_AD_CONTENT_CYCLE`
- `STREAMING_AD_PLATFORM`
- `SECURITY_IDENTITY_DEEPFAKE`
- `METAVERSE_NFT_THEME`
- `PLATFORM_GOVERNANCE_LEGAL_RISK`
- `OPERATIONAL_TRUST_BREAK_OVERLAY`
- `PLATFORM_AD_TRUST_OVERLAY`

Counts:

- Targets: 14
- Case records: 16
- Structural success records: 1
- Success candidates: 2
- 4B watch cases: 7
- 4C thesis-break cases: 6
- Gate-only targets: 4

## Case Pack

Key cases added:

- Douzone Bizon / EQT cloud ERP case
- Palantir Q4 2025 AI revenue case
- Palantir Q1 2026 4B-watch case
- Netflix ad tier 70m case
- Netflix ad tier 250m privacy watch case
- The Trade Desk revenue miss and weak guide cases
- CrowdStrike outage and Delta lawsuit cases
- Kakao founder legal overhang case
- Roblox safety forecast cut case
- Take-Two GTA VI delay case
- WPP ad forecast/profit deterioration cases
- Meta scam ads and youth-safety litigation cases

## Guardrails

- Do not use Round 61 cases as candidate-generation input.
- Do not change production scoring from this pack.
- Do not invent ARR, ARPU, bookings, churn, FCF, lawsuit damage, customer retention, or stage prices.
- Keep Stage 3-Green strict.
- Treat operational trust breaks, scam ads, privacy lawsuits, youth-safety litigation, founder/M&A legal risk, and single-title delay as RedTeam gates.

## Generated Reports

The CLI writes:

- `round61_r8_loop2_platform_content_sw_security_summary.md`
- `round61_r8_loop2_case_matrix.csv`
- `round61_r8_loop2_stage_date_plan.csv`
- `round61_r8_loop2_green_guardrails.md`
- `round61_r8_loop2_risk_overlays.md`
- `round61_r8_loop2_price_validation_plan.md`
- `round61_r8_loop2_price_fields.csv`

## Verification

Targeted tests:

```bash
PYTHONPATH=src python -m unittest tests.test_round61_r8_loop2_platform_content_sw_security -v
```

Report generation:

```bash
PYTHONPATH=src python -m e2r.cli.build_round61_r8_loop2_report
```

Full verification was run after implementation.
