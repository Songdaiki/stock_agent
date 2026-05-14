# Checkpoint 28A-14: Round 13 Score Normalization Readiness

Round 13 converts the latest analyst notes into a score-weight hypothesis table.

## What Changed

- Added Round 13 score-normalization readiness module.
- Added score-weight profile CSV.
- Added Green/Watch/Red policy report.
- Added case candidate plan for future v0.3 records.
- Added tests proving production scoring does not import the Round 13 module.

## Why

The methodology is correct, but scoring is not ready to change yet.

Example:

- `MEMORY_HBM_CAPACITY` can be a structural success pattern.
- After extreme rerating, it can also become a 4B-watch pattern.
- The same case family therefore needs both success evidence and graduation/overheat evidence.

## Output Files

- `data/sector_taxonomy/score_weight_profiles_round13.csv`
- `output/e2r_round13_score_normalization/round13_score_normalization_summary.md`
- `output/e2r_round13_score_normalization/round13_score_normalization_targets.csv`
- `output/e2r_round13_score_normalization/round13_green_watch_red_policy.md`
- `output/e2r_round13_score_normalization/round13_case_candidate_plan.md`
- `output/e2r_round13_score_normalization/round13_shadow_scoring_next_plan.md`

## What Did Not Change

- Production scoring is unchanged.
- StageClassifier thresholds are unchanged.
- Theme labels remain search/routing labels only.

## Next Step

Convert planned cases into case-library records and backfill price paths. Only after score-price alignment is visible should these weights be tried in shadow scoring.
