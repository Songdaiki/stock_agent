# Round-9 Case Record Schema Contract

## Required/Supported Fields
- `large_sector`
- `secondary_archetypes`
- `case_type`
- `stage1_evidence`
- `stage2_evidence`
- `stage3_evidence`
- `stage4b_evidence`
- `stage4c_evidence`
- `must_have_fields`
- `red_flag_fields`
- `score_price_alignment`
- `rerating_result`
- `price_pattern`
- `score_weight_hint`
- `green_guardrails`
- `notes`
- `price_validation`

## Price Pattern Values
- `unknown`
- `straight_rerating`
- `stair_step_rerating`
- `cycle_boom_bust`
- `theme_overheat`
- `accounting_trust_break`
- `governance_trust_break`
- `event_premium`
- `credit_relief_rally`
- `reopening_cycle`
- `policy_contract_delay`

## Interpretation
- `notes` is calibration text and is not production evidence.
- `governance_trust_break` is a Round-9 reporting pattern for Kakao/SMCI-like trust breaks.
