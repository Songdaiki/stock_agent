# Checkpoint 28A-11: Round 9 Case Record Pack Audit

## Summary

Round 9 was applied as calibration/report material only. Production scoring and
StageClassifier thresholds were not changed.

Round 9 checks whether the Round 1-8 synthesis is represented as actual case
records:

```text
10 large sectors
-> 32 practical archetype views
-> required case ids
-> score/price/lifecycle schema
```

쉬운 예시:

```text
Kakao is not a platform success just because it has traffic.
If governance/legal risk blocks rerating, it is a trust-break guardrail case.
```

## Implemented Files

- `src/e2r/sector/round9_case_record_pack_audit.py`
- `src/e2r/cli/build_round9_case_record_pack_report.py`
- `tests/test_round9_case_record_pack_audit.py`
- `docs/e2r_case_record_pack_round9.md`
- `output/e2r_round9_case_record_pack/round9_case_record_pack_framework.md`
- `output/e2r_round9_case_record_pack/round9_required_case_matrix.csv`
- `output/e2r_round9_case_record_pack/round9_case_pack_audit.md`
- `output/e2r_round9_case_record_pack/round9_archetype_view_coverage.csv`
- `output/e2r_round9_case_record_pack/round9_case_record_schema_contract.md`
- `output/e2r_round9_case_record_pack/round9_next_price_alignment_plan.md`

## Schema Update

`E2RCaseRecord` now preserves:

- `notes`

This is calibration text only. It is not production evidence.

## Case Pack Update

Added missing Round 9 required case:

- `hanwha_aerospace_2024`

Prices and stage prices remain null with `price_validation_status=needs_price_backfill`.

## Audit Result

The Round 9 required case id list is fully present in `cases_v02.jsonl` after this patch.

## What Not To Change

- Do not lower Stage 3-Green thresholds.
- Do not use case records as production candidate-generation input.
- Do not treat price-only movement as EPS/FCF rerating.
- Do not fabricate missing stage dates or prices.

## Verification

Commands run:

```bash
PYTHONPATH=src python -m unittest tests.test_round9_case_record_pack_audit -v
PYTHONPATH=src python -m e2r.cli.build_round9_case_record_pack_report --cases data/e2r_case_library/cases_v02.jsonl --output-directory output/e2r_round9_case_record_pack
```

Full test run was executed after the patch before commit.
