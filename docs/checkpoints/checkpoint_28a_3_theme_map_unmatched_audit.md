# Checkpoint 28A-3: Theme Map, Unmatched Audit, and Shadow Score Loop

## Summary

Round 18 was implemented as a research/calibration checkpoint.

Production scoring was not changed.

The key rule remains:

> Theme tags route research. Evidence creates score.

Example: `초전도체` is mapped, but it remains a speculative science route. It
does not create EPS/FCF, contract, visibility, or valuation rerating score.

## Implemented

- Raw theme tag files:
  - `data/sector_taxonomy/raw_theme_tags_v05.txt`
  - `data/sector_taxonomy/raw_theme_tags_v05.csv`
- Theme map and aliases:
  - `data/sector_taxonomy/theme_tag_map_v05.csv`
  - `data/sector_taxonomy/theme_aliases_v05.yml`
- Taxonomy files:
  - `data/sector_taxonomy/large_sector_v05.yml`
  - `data/sector_taxonomy/archetype_rules_v05.yml`
- Shadow score profile file:
  - `data/sector_taxonomy/score_weight_profiles_v05.yml`
- Case/evidence expansion:
  - `data/e2r_case_library/cases_v03.jsonl`
  - `data/e2r_case_library/cases_v03_price_filled.jsonl`
  - `data/e2r_case_library/evidence_index_v03.jsonl`
- New modules:
  - `src/e2r/sector/theme_tag_mapper.py`
  - `src/e2r/sector/large_sectors.py`
  - `src/e2r/sector/shadow_score_normalizer.py`
- New CLIs:
  - `src/e2r/cli/audit_theme_tag_coverage.py`
  - `src/e2r/cli/run_shadow_score_normalizer.py`

## Theme Coverage Result

- total_raw_tags: 208
- mapped_tags: 208
- unmatched_tags: 0
- ambiguous_tags: 6

Ambiguous tags:

- `국내 상장한 중국 주`
- `금은`
- `엔진(조선-AI)`
- `인공지능(AI)`
- `카메라`
- `화재`

These are mapped, but require manual context review. For example, `화재` could
mean insurance, EV fire, or disaster/event demand depending the article.

## Green Policy Distribution

- green_allowed: 16
- watch_to_green: 26
- watch_only: 125
- red_watch: 19
- event_only: 16
- red_flag: 6

## Case Coverage Status

- cases_v03 total records: 108
- evidence_index_v03 rows: 44
- cases with missing/unfilled price validation after backfill: 96

The case library is expanded, but it is still calibration material.

## Shadow Score Loop

The shadow normalizer reads:

- `cases_v03_price_filled.jsonl`
- `score_weight_profiles_v05.yml`

It writes:

- `output/e2r_case_library_v03/shadow_score_profile_report.md`

It does not call or modify production `FeatureEngineering` or `StageClassifier`.

## Why Production Scoring Is Still Too Early

- Theme absorption is now good, but theme names are not evidence.
- Many case records still lack price-path validation.
- Some archetypes still lack 2+ success/candidate and 2+ counterexample/risk records.
- Red/event/speculative tags require RedTeam-first handling.

## Commands Run

```bash
PYTHONPATH=src python -m e2r.cli.audit_theme_tag_coverage \
  --raw-tags data/sector_taxonomy/raw_theme_tags_v05.csv \
  --map data/sector_taxonomy/theme_tag_map_v05.csv \
  --output output/theme_tag_coverage_v05

PYTHONPATH=src python -m e2r.cli.backfill_case_price_paths \
  --cases data/e2r_case_library/cases_v03.jsonl \
  --price-root data/historical_official/prices \
  --output data/e2r_case_library/cases_v03_price_filled.jsonl

PYTHONPATH=src python -m e2r.cli.run_shadow_score_normalizer \
  --cases data/e2r_case_library/cases_v03_price_filled.jsonl \
  --profiles data/sector_taxonomy/score_weight_profiles_v05.yml \
  --output output/e2r_case_library_v03/shadow_score_profile_report.md
```

## Next Step

Checkpoint 28B should run archetype-aware scoring in shadow mode only. Do not
promote the profiles into production until price validation and score-price
alignment are materially stronger.
