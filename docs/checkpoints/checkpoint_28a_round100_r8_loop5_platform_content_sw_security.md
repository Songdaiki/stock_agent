# Checkpoint 28A Round 100 R8 Loop 5 Platform / Content / SW / Security

## Summary

Round 100 applies the R8 Loop 5 platform, content, software, and security research pack.
This is calibration/evaluation material only. It does not change production scoring, StageClassifier thresholds, or candidate generation.

The core rule is simple:

- `AI feature launch` is not Green evidence.
- `user growth` is not Green evidence.
- `new game launch expectation` is not Green evidence.
- `security demand` is not Green evidence if operational trust breaks.

Example: a company can announce an AI agent and still fail E2R if it increases compute cost, cannibalizes seats, or does not create ARR/FCF.

## Implemented Files

- `src/e2r/sector/round100_r8_loop5_platform_content_sw_security.py`
- `src/e2r/cli/build_round100_r8_loop5_report.py`
- `tests/test_round100_r8_loop5_platform_content_sw_security.py`
- `data/e2r_case_library/cases_r8_loop5_round100.jsonl`
- `data/sector_taxonomy/score_weight_profiles_round100_r8_loop5_v5.csv`
- `output/e2r_round100_r8_loop5_platform_content_sw_security/`

## Archetype Counts

- target_count: 24
- case_candidate_count: 19
- structural_success_count: 1
- success_candidate_count: 6
- event_premium_count: 1
- stage4b_case_count: 7
- stage4c_case_count: 6
- green_possible_count: 3
- watch_yellow_first_count: 12
- redteam_first_count: 9
- gate_only_target_count: 7

## New / Confirmed Archetypes

- `ENTERPRISE_AI_ONTOLOGY_WORKFLOW`
- `LEGACY_SAAS_AI_DISRUPTION_OVERLAY`
- `SINGLE_IP_RELEASE_EVENT_PREMIUM`
- `DISCLOSURE_CONFIDENCE_CAP`

`DISCLOSURE_CONFIDENCE_CAP` is cap-only, not gate-only. Missing ARR, customer contract, incident detail, lawsuit detail, impairment detail, or customer concentration should cap Stage 3 confidence until verified.

## Key Case Splits

- Palantir is mapped to `ENTERPRISE_AI_ONTOLOGY_WORKFLOW`, not generic AI software.
- Salesforce Agentforce is treated as AI application evidence with legacy SaaS disruption as a secondary risk.
- Take-Two GTA preorder rumor is mapped to `SINGLE_IP_RELEASE_EVENT_PREMIUM`, not structural game IP.
- CrowdStrike outage remains a hard `SECURITY_OPERATIONAL_TRUST_OVERLAY` 4C example.
- Netflix ad tier is a streaming ad candidate, but privacy/youth-safety risk remains a separate gate.
- Meta scam ads and youth-safety cases remain platform trust and privacy/youth-safety RedTeam examples.

## Guardrails

- Do not use case records as candidate-generation input.
- Do not apply Round 100 v5.0 score weights to production scoring yet.
- Do not invent ARR, ARPU, bookings, churn, billings, FCF, customer-damage, lawsuit, security-incident, or stage-price fields.
- Do not treat AI features, user count, preorder rumor, ad recovery, security demand, NFT, or metaverse tags as Green evidence alone.
- Require ARR/ARPU/bookings/billings, OPM, FCF, low churn, renewal, operational trust, legal stability, ad quality, and privacy/youth-safety clearance before higher conviction.

## Verification

Commands run:

```bash
PYTHONPATH=src python -m unittest tests.test_round100_r8_loop5_platform_content_sw_security -v
PYTHONPATH=src python -m e2r.cli.build_round100_r8_loop5_report
```

Both completed successfully before the full repository test run.
