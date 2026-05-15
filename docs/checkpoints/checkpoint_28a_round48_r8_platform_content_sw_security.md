# Checkpoint 28A Round 48 - R8 Platform / Content / Software / Security

Round 48 adds the R8 platform, content, software, and security calibration
pack. This is still case-library and score-weight design material only. It
does not change production scoring, StageClassifier thresholds, or RedTeam
logic.

## Files Added

- `src/e2r/sector/round48_r8_platform_content_sw_security.py`
- `src/e2r/cli/build_round48_r8_report.py`
- `tests/test_round48_r8_platform_content_sw_security.py`
- `data/e2r_case_library/cases_r8_round48.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round48_r8_v1.csv`
- `output/e2r_round48_r8_platform_content_sw_security/`

## Archetype Updates

Round 48 adds R8-specific canonical archetype labels:

- `CLOUD_AI_SOFTWARE_INFRA`
- `AI_SOFTWARE_APPLICATION`
- `GENERATIVE_AI_IP_RISK`
- `CONTACT_CENTER_AI_AUTOMATION`
- `SERVICE_KIOSK_SELF_CHECKOUT`
- `MEDIA_AD_CONTENT_CYCLE`
- `STREAMING_AD_PLATFORM`
- `SECURITY_IDENTITY_DEEPFAKE`
- `METAVERSE_NFT_THEME`
- `PLATFORM_GOVERNANCE_LEGAL_RISK`

## R8 Split

R8 is treated as a repeat-revenue and trust-risk sector, not a user-count or
AI-feature sector.

- Green-eligible with strict proof: cloud/AI software infrastructure.
- Watch-to-Green: platform software, AI application, contact-center AI, kiosk/self-checkout, game/content IP, media/ad cycle, streaming ad platform, security/identity.
- RedTeam-first: generative AI IP risk, metaverse/NFT, platform governance/legal risk.

Example: a B2B SaaS company can improve only when ARR, retention, OPM, and FCF
are visible. A security company can have recurring revenue, but a global outage
can still create hard 4C evidence.

## Case Pack

Round 48 stores 11 calibration records:

- Douzone Bizon EQT cloud ERP case
- Palantir AI platform revenue case
- Netflix ad tier growth case
- Tencent gaming and AI advertising mixed case
- The Trade Desk revenue miss case
- CrowdStrike outage case
- Kakao founder legal overhang case
- Roblox safety forecast cut case
- Take-Two GTA VI delay case
- WPP ad-cycle slowdown case
- Meta scam ads lawsuit case

All case records are marked as calibration/evaluation material. Missing prices
remain open for backfill.

## R8 Green Rule

R8 Green is not "user count", "AI feature", "new title", "security theme",
"NFT/metaverse label", or "ad recovery headline" by itself. It requires
evidence such as:

- ARR / ARPU / recurring revenue
- low churn and high net retention
- OPM and FCF conversion
- bookings and repeat IP monetization
- ad revenue and ad ARPU
- security renewal and operational trust
- clean privacy, legal, and platform safety record

## What Not To Change

- Do not apply R8 v1.0 weights to production scoring yet.
- Do not use R8 case records as candidate-generation input.
- Do not lower Stage 3-Green thresholds for platform recall.
- Do not invent ARR, ARPU, churn, bookings, ad revenue, renewal, legal status, or price-path fields.
- Do not treat user growth, AI feature, security headline, or new-title expectation as Green evidence alone.

## Verification

Commands used:

```bash
PYTHONPATH=src python -m unittest tests/test_round48_r8_platform_content_sw_security.py -v
PYTHONPATH=src python -m compileall -q src/e2r/sector/round48_r8_platform_content_sw_security.py src/e2r/cli/build_round48_r8_report.py tests/test_round48_r8_platform_content_sw_security.py
PYTHONPATH=src python -m e2r.cli.build_round48_r8_report
```

Full-suite status is tracked separately because the local tree still has
pre-existing deleted `docs/round/round_17.md` files that break the older
round-17 tests.
