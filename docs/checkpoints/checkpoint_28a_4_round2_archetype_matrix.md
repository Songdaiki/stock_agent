# Checkpoint 28A-4: Round-2 Archetype Matrix

## Why

Checkpoint 28A and 28A-2 created the taxonomy and case-library structure, but
case coverage is still not enough to apply final scoring weights.

The analyst Round-2 matrix adds the missing research layer:

```text
archetype
-> EPS/FCF structure
-> Stage 1/2/3/4B/4C evidence
-> success/counterexample targets
-> draft weights
-> Green gate guardrails
```

## What Changed

Added:

- `src/e2r/sector/archetype_matrix.py`
- `src/e2r/cli/build_round2_archetype_matrix_report.py`
- `tests/test_archetype_matrix.py`
- `docs/e2r_archetype_matrix_round2.md`
- `output/e2r_archetype_matrix/round2_archetype_matrix.md`
- `output/e2r_archetype_matrix/round2_score_weight_table.csv`
- `output/e2r_archetype_matrix/round2_case_mining_priorities.md`
- `output/e2r_archetype_matrix/round2_peer_normalization_metrics.md`
- `output/e2r_archetype_matrix/round2_case_gap_matrix.csv`
- `output/e2r_archetype_matrix/round2_shadow_scoring_plan.md`
- `output/e2r_archetype_matrix/round2_price_pattern_taxonomy.md`

## Round 01 Patch

`docs/round/round_01.md` added three clarifications:

1. Deep-dive priority and first shadow-scoring candidates are different lists.
2. `Stage 2-High` and `Stage 3-Watch` should be used as report-facing bands
   before loosening Green.
3. 4B/4C must be interpreted by archetype-specific thesis-break signals, not
   price alone.

Example:

```text
HD/Iljin-style candidate
-> deterministic_stage = Stage 2
-> promotion_band = Stage 3-Watch
-> not forced into Stage 3-Green
```

The generated priority report now shows:

- deep-dive priority tier
- first shadow-scoring candidate flag
- promotion band reminder

## Round 02 Patch

`docs/round/round_02.md` added price-path context to the same archetype matrix.
This does not change production scoring. It adds lifecycle labels so a case can
be reviewed with the right price pattern.

Examples:

```text
HD현대일렉트릭-like backlog case
-> price_pattern = STAIR_STEP_RERATING
-> Stage 2/Stage 3-Watch can survive a pullback only if backlog, margin, and revision evidence remain intact

HMM/씨젠-like one-off or cycle case
-> price_pattern = CYCLE_SPIKE_NORMALIZATION
-> EPS explosion is not enough for structural Green

SMCI-like trust issue
-> price_pattern = ACCOUNTING_TRUST_COLLAPSE
-> strong prior growth must still be blocked by audit/trust 4C evidence
```

The generated reports now include:

- archetype-specific price patterns in the matrix
- `round2_price_pattern_taxonomy.md`
- price-pattern columns in the case-gap matrix

## Important

No production scoring changed.

The matrix is not imported by:

- feature engineering
- stage classification
- Red Team
- E2R standard pipeline
- web research

## Example

`CONTRACT_BACKLOG_INDUSTRIAL` can use contract quality, backlog, lead time, CAPA,
and ASP as visibility evidence.

`EXPORT_RECURRING_CONSUMER` should not require contract quality. It uses export
growth, channel expansion, repeat demand, ASP/OPM, and FY1/FY2 revision.

That distinction is the whole reason this matrix exists.

## Current Use

Use the generated reports to decide:

- which cases to add next
- which price paths need backfill
- which archetypes need more counterexamples
- which Green gates should remain restricted

Do not use it to force Stage 3-Green.

## Still Not Changed

- StageClassifier thresholds
- production feature scoring
- live candidate generation
- Red Team decisions
