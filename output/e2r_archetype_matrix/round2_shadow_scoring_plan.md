# Round-2 First Shadow-Scoring Plan

This is not production scoring. It identifies which archetypes should be compared first in a future shadow-score run.

| archetype | positive | counterexamples | coverage status | Green posture |
|---|---:|---:|---|---|
| CONTRACT_BACKLOG_INDUSTRIAL | 3 | 1 | needs_more_cases | Green allowed only with disclosure + financial actual + research/consensus-revision cross evidence. |
| DEFENSE_GOVERNMENT_BACKLOG | 1 | 1 | needs_more_cases | Green allowed with government customer, delivery visibility, and margin/revision evidence. |
| EXPORT_RECURRING_CONSUMER | 1 | 2 | needs_more_cases | Contract quality is not required; recurring export demand and EPS/OP revision are required. |
| K_BEAUTY_EXPORT_DISTRIBUTION | 2 | 2 | covered_2x2 | Green allowed through export/channel/recurring-demand evidence, not contract quality. |
| MEMORY_HBM_CAPACITY | 2 | 2 | covered_2x2 | Green allowed with memory-specific revision, pricing, supply discipline, and capacity evidence. |
| SEMI_EQUIPMENT_CAPEX | 3 | 2 | covered_2x2 | Green allowed with confirmed order-to-revenue conversion and customer capex durability. |
| SHIPPING_FREIGHT_CYCLE | 1 | 1 | needs_more_cases | Green very restricted; normally cyclical success or Yellow/Red rather than structural Green. |
| ONE_OFF_EVENT_DEMAND | 0 | 1 | needs_more_counterexamples | Green blocked by default; normally Stage 3-Red/Yellow guardrail. |
| THEME_VALUATION_OVERHEAT | 0 | 1 | needs_more_counterexamples | Green blocked unless real EPS/FCF evidence overwhelms overheat risk. |
| FINANCIAL_SPREAD_BALANCE_SHEET | 0 | 5 | needs_more_cases | Green allowed with ROE/PBR and durable capital return, not low PBR alone. |

## Rules
- Run old deterministic score and future archetype-aware score side by side.
- Do not replace StageClassifier in the first shadow run.
- Use promotion bands for visibility before changing Green gates.
- Keep one-off and overheat archetypes as guardrails, not Green factories.
- Review price-pattern labels before treating a move as durable rerating.
