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

