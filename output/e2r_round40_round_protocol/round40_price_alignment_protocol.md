# Round-40 Score-Price Alignment Protocol

| Label | Meaning |
| --- | --- |
| `aligned` | Score, evidence, EPS/FCF, and price path move together after the evidence date. |
| `false_positive_score` | The score looked high, but price and/or fundamentals did not rerate. |
| `price_moved_without_evidence` | The price rose, but the system should not treat it as evidence-backed E2R. |
| `evidence_good_but_price_failed` | Evidence looked valid, but the market did not rerate it. |
| `cyclical_success` | The case worked as a cycle, but not as structural E2R. |
| `event_premium` | A policy, tender, takeover, or event premium drove the move. |
| `thesis_break` | A 4C-style event broke the original thesis. |
| `unknown_insufficient_price_data` | Price path is missing or insufficient; do not force alignment. |

## Example

If a stock jumps on a policy headline but there is no EPS/FCF evidence, it can be `event_premium` or `price_moved_without_evidence`; it must not become Stage 3-Green from price alone.
