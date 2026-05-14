# Checkpoint 28A-17: Round 16 Theme Coverage v0.5

## Summary

Round 16 was converted into a report-only full theme coverage map.

It consolidates the previous theme work into:

- 12 large sectors
- 70+ sub-archetypes
- 200+ unique raw theme tags
- Green / Watch / RedTeam posture
- must-have evidence
- red-flag evidence
- score-weight group hypotheses

## Core Rule

Theme tags are routing labels, not score evidence.

Example:

`네옴시티` routes to geopolitical reconstruction/event-premium checks. It does not become structural E2R until funded orders, contract economics, margin path, and EPS/FCF evidence appear.

## Added

- `src/e2r/sector/round16_theme_coverage_v05.py`
- `src/e2r/cli/build_round16_theme_coverage_report.py`
- `tests/test_round16_theme_coverage_v05.py`
- `docs/e2r_theme_coverage_round16.md`
- Round 16 CSV outputs under `data/sector_taxonomy/`
- Round 16 report outputs under `output/e2r_round16_theme_coverage_v05/`

## Coverage Result

The generated summary reports:

- `large_sector_count: 12`
- `sub_archetype_count: 92`
- `theme_tag_row_count: 600`
- `unique_theme_tag_count: 280`
- `score_group_count: 18`
- `production_scoring_changed: false`
- `theme_tags_are_score_input: false`

## Guardrails

- Production scoring unchanged.
- StageClassifier thresholds unchanged.
- Case/theme labels are not candidate-generation inputs.
- Event, policy, speculative science, one-off disease, and commodity cycle themes remain guarded unless recurring EPS/FCF evidence appears.

## Verification

- Round 16 unit tests added.
- Production scoring modules are tested to ensure they do not import the Round 16 coverage module.
- Full test suite passed after implementation.

## Next Step

Use `theme_tag_map_round16.csv` as the basis for `cases_v03.jsonl` planning. Price-path backfill and score-price alignment must happen before any shadow scoring implementation.
