# Round-4 Stage Failure Matrix

| stage_failure_type | case_count | interpretation |
|---|---:|---|
| green_success | 0 | Stage 3-Green and price path both matched structural rerating. |
| yellow_success | 0 | Yellow/watch posture was enough; Green was not necessary. |
| stage2_watch_success | 0 | Stage 2/Watch captured the case without over-promoting. |
| false_green | 0 | Green would have been unsafe because price/evidence later failed. |
| false_yellow | 0 | Yellow looked plausible but price/evidence did not confirm. |
| should_have_been_red | 0 | Red/4C guardrail should dominate the candidate. |
| missed_structural | 0 | A structural move may have been missed by evidence or scoring. |
| unknown | 66 | Insufficient stage or price validation data. |

## Interpretation
- `false_green` means the score/gate would have promoted too aggressively.
- `missed_structural` means evidence or scoring may have missed a real rerating.
- `unknown` usually means price backfill or stage dates are incomplete.
