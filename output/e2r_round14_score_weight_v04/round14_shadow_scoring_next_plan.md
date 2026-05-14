# Round-14 Next Plan

1. Build `theme_tag_map.csv` from these v0.4 mappings.
2. Convert success candidates and counterexamples into `cases_v03.jsonl` records.
3. Backfill stage2/stage3 price, peak price, MFE/MAE, and drawdown.
4. Run score-price alignment before any shadow scoring.
5. Keep production StageClassifier thresholds unchanged until the case library proves the weights.

## What Not To Change
- Do not turn theme names into score inputs.
- Do not use these weights in live scoring yet.
- Do not make one-off disease, speculative science, tokenization, construction PF, or battery overheat cases Green without durable EPS/FCF evidence.
