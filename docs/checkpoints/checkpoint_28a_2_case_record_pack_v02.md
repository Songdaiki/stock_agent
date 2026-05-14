# Checkpoint 28A-2: Case Record Pack v0.2

## What Changed

Checkpoint 28A-2 adds the intermediate case record pack and price-alignment
schema needed before Checkpoint 28B scoring work.

Added:

- expanded E2R archetypes
- v0.2 case schema fields
- `data/e2r_case_library/cases_v02.jsonl`
- price-path backfill CLI
- score-price alignment evaluator
- v0.2 case-library reports
- schema documentation

Production scoring is unchanged.

## Why This Is Still Calibration

The case pack is like a study notebook, not a live scanner input.

Example:

```text
SK하이닉스 HBM 사례
-> memory/HBM archetype calibration
-> helps design future weights
-> does not make SK하이닉스 a live candidate by itself
```

Cases are never used as candidate-generation input. They are only used to
evaluate whether future scoring rules are reasonable.

## Case Pack Result

Generated from `data/e2r_case_library/cases_v02_price_filled.jsonl`:

- case_count: 66
- archetypes_with_cases: 27
- archetypes_covered_2x2: 3
- cases_needing_price_backfill: 54

Covered enough for future shadow-scoring experiments:

- `K_BEAUTY_EXPORT_DISTRIBUTION`
- `MEMORY_HBM_CAPACITY`
- `PLATFORM_SOFTWARE_INTERNET`

Still Green-restricted:

- most archetypes, including contract/backlog industrial, defense, shipping,
  AI data center infrastructure, CDMO, value-up, travel/reopening, construction,
  one-off demand, and theme overheat.

This does not mean those sectors are unimportant. It means the case pack does
not yet have enough positive plus counterexample coverage for final Green logic.

## Score-Price Alignment

The evaluator separates evidence quality from price behavior:

- structural case with no price data -> `unknown`
- price rise without EPS/FCF evidence -> `price_moved_without_evidence`
- good evidence but weak price path -> `evidence_good_but_price_failed`
- one-off demand -> `no_rerating`
- cyclical case -> `cyclical_rerating`
- event-only governance case -> `event_premium`
- 4C after candidate signal -> `thesis_break`

This prevents a simple price spike from being counted as true E2R rerating.

## Price Backfill

Command:

```bash
PYTHONPATH=src python -m e2r.cli.backfill_case_price_paths \
  --cases data/e2r_case_library/cases_v02.jsonl \
  --price-root data/historical_official/prices \
  --output data/e2r_case_library/cases_v02_price_filled.jsonl
```

Rules:

- if historical price exists, fill stage prices and MFE/MAE
- if price is missing, keep null
- set `price_validation_status = missing_price_data`
- do not invent prices

## Reports

Generated:

- `output/e2r_case_library_v02/case_record_summary.md`
- `output/e2r_case_library_v02/archetype_coverage_matrix.csv`
- `output/e2r_case_library_v02/score_price_alignment_summary.md`
- `output/e2r_case_library_v02/missing_price_data_report.md`
- `output/e2r_case_library_v02/green_guardrail_summary.md`

## What Remains Before Checkpoint 28B

- Add more counterexamples for contract/backlog industrial.
- Add better price history for non-fixture symbols.
- Add value-up cases where FCF/NAV/shareholder-return actually improved.
- Add AI data center infrastructure cases with confirmed orders.
- Add CDMO and biotech cases with commercial economics versus dilution failures.
- Only then design sector-aware shadow scoring.

## Guardrails

- Do not change StageClassifier thresholds yet.
- Do not apply `score_weight_hint` in live scoring.
- Do not use case records as candidate-generation input.
- Do not call event premium true rerating.
- Do not fill missing price or stage dates by assumption.
