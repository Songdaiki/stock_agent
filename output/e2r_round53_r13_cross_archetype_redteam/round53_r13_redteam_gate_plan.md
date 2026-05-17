# Round-53 R13 RedTeam Gate Plan

| target | posture | hard gate | Green allowed | Red flags |
| --- | --- | --- | --- | --- |
| `REDTEAM_ACCOUNTING_TRUST_OVERLAY` | REDTEAM_FIRST | true | false | auditor_resignation, filing_delay, internal_control_issue, related_party_risk |
| `FINANCIAL_REPORTING_INTEGRITY_RISK` | REDTEAM_FIRST | true | false | late_filing, material_weakness, restatement, qualified_opinion |
| `PRICE_ONLY_RALLY` | REDTEAM_FIRST | false | false | no_eps_fcf, no_contract, no_revenue, theme_only |
| `EVENT_PREMIUM` | WATCH_YELLOW_FIRST | false | false | mou_only, policy_only, event_only, deal_failure |
| `CYCLICAL_SUCCESS` | WATCH_YELLOW_FIRST | false | false | normalization_risk, new_supply, spot_price_reversal |
| `STRUCTURAL_SUCCESS_ALIGNED` | GREEN_POSSIBLE | false | true | crowded_4b, valuation_saturation, revision_slowdown |
| `EVIDENCE_GOOD_BUT_PRICE_FAILED` | WATCH_YELLOW_FIRST | false | false | price_failed, valuation_frame_stuck, liquidity_low |
| `FALSE_POSITIVE_SCORE` | REDTEAM_FIRST | false | false | score_overfit, no_eps_fcf, price_failed, redteam_ignored |
| `CROWDED_RERATING_4B_WATCH` | WATCH_YELLOW_FIRST | false | false | crowding, valuation_saturation, revision_slowdown, capacity_addition |
| `THESIS_BREAK_4C` | REDTEAM_FIRST | true | false | contract_cancellation, order_cut, regulatory_denial, demand_crash, trust_break |
| `LEGAL_REGULATORY_REDTEAM` | REDTEAM_FIRST | true | false | lawsuit, regulatory_probe, approval_denial, license_risk |
| `OPERATIONAL_TRUST_BREAK` | REDTEAM_FIRST | true | false | security_outage, privacy_breach, customer_lawsuit, operational_trust_damage |
| `LEVERAGE_FCF_BREAKDOWN` | REDTEAM_FIRST | true | false | negative_fcf, cash_runway, refinancing, dilution, dividend_cut |
| `UNKNOWN_INSUFFICIENT_EVIDENCE` | REDTEAM_FIRST | false | false | missing_evidence, date_unverified, single_source, unknown |

## What Not To Change

- Do not apply Round53 overlay symbols to production scoring yet.
- Do not lower Stage 3-Green to improve recall.
- Do not use R13 case records as candidate-generation input.
- Do not treat price-only movement, event premium, or cycle success as structural Green by itself.
- Do not ignore hard RedTeam evidence such as auditor resignation, filing delay, regulatory denial, operational trust break, cash runway collapse, or hard thesis break.
