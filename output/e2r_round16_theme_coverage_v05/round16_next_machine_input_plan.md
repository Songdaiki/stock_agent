# Round-16 Next Machine Input Plan

1. Review `theme_tag_map_round16.csv` for duplicate or ambiguous theme tags.
2. Collapse aliases only when the evidence requirements are identical.
3. Use the map to create `cases_v03.jsonl` candidates, not production candidates.
4. Backfill price paths and run score-price alignment before shadow scoring.
5. Keep StageClassifier and Stage 3-Green thresholds unchanged.

## What Not To Change
- Do not use raw theme names as score evidence.
- Do not use this coverage map as candidate-generation labels.
- Do not treat policy, disaster, speculative science, or one-off demand as structural E2R without recurring EPS/FCF evidence.
