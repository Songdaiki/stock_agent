# Round-119 Theme Tag Guardrails

| rule | routing use | scoring limit | required upgrade |
| --- | --- | --- | --- |
| `theme_tag_is_routing_only` | Use raw market theme tags to route searches and cheap scan attention. | Do not give EPS/FCF or Green score from the tag itself. | Upgrade only when company-level evidence creates score fields. |
| `opendart_list_is_not_detail` | Use list disclosures to decide whether detail fetch is needed. | Do not score missing contract amount, counterparty, term, or OP fields. | Upgrade after document/detail parsing confirms fields. |
| `event_needs_conversion` | Use events, policy, disease, or disaster headlines as Stage 1 attention. | Do not call event premium structural rerating. | Upgrade only with funded budget, order, financing, revenue, or guidance. |
| `price_needs_evidence` | Use price and trading value to prioritize research. | Do not let price-only movement create Stage 3-Green. | Upgrade only when price follows dated evidence and EPS/FCF path. |
| `redteam_overrides_score` | Use RedTeam flags after scoring and before final stage interpretation. | Do not ignore hard trust, accounting, leverage, legal, or commercialization breaks. | Downgrade or block Green when hard RedTeam is present. |

## Core Rule

Raw theme tags route attention. They do not create Green evidence. A tag such as `HBM`, `power grid`, `value-up`, or `policy event` must be upgraded into dated company-level fields before scoring.
