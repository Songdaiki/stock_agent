# Checkpoint 28A: Sector Taxonomy and Case Mining

## What Changed

Checkpoint 28A adds the research scaffolding needed before changing
sector-aware scoring weights:

- full Korea sector taxonomy package
- E2R archetype definitions
- sector/archetype case-library schema
- dry-run case-mining CLI
- peer normalization design
- coverage reports and score-weight recommendations

This checkpoint does not change deterministic scoring thresholds.

## Why

The old scoring leaned too heavily on contract/backlog evidence. That works for
전력기기 and 방산, but it can under-score:

- 삼양식품: export channel and recurring consumer demand
- 실리콘투: K-beauty distribution and repeat overseas orders
- 삼성전자/SK하이닉스: HBM, memory price, supply discipline

So the next scoring step needs a case library first. Example:

```text
전력기기: 계약금액/수주잔고 성공 사례와 저품질 반례를 같이 모음
식품수출: 수출채널 성공 사례와 일회성 유행 반례를 같이 모음
```

## New Files

- `src/e2r/sector/taxonomy.py`
- `src/e2r/sector/sector_mapper.py`
- `src/e2r/sector/archetypes.py`
- `src/e2r/sector/peer_groups.py`
- `src/e2r/sector/peer_normalizer.py`
- `src/e2r/sector/case_library.py`
- `src/e2r/cli/build_korea_sector_taxonomy.py`
- `src/e2r/cli/mine_e2r_sector_cases.py`
- `data/sector_taxonomy/*`
- `data/e2r_case_library/cases.jsonl`

## Outputs

- `data/sector_taxonomy/korea_sector_map.csv`
- `output/sector_taxonomy/sector_taxonomy_summary.md`
- `output/e2r_case_library/case_coverage_summary.md`
- `output/e2r_case_library/archetype_case_matrix.csv`
- `output/e2r_case_library/recommended_score_weights.md`

## Current Coverage

The fixture taxonomy maps the current historical-official universe. It is not a
full live KOSPI/KOSDAQ taxonomy yet.

Generated fixture taxonomy result:

- mapped symbols: 13
- mapped sectors: 8
- archetypes used: 8
- unmapped_count: 0

Generated case-library coverage result:

- archetypes_total: 25
- archetypes_covered_2x2: 0
- archetypes_under_covered: 25

This is expected at Checkpoint 28A. The case library intentionally reports
under-covered archetypes. That is a feature, not a failure. For example, if
K-beauty has one positive case and no counterexamples, final score weights
should wait.

Current examples:

- `CONTRACT_BACKLOG_INDUSTRIAL`: 3 positives, 1 counterexample
- `MEMORY_HBM_CAPACITY`: 3 positives, 0 counterexamples
- `EXPORT_RECURRING_CONSUMER`: 1 positive, 0 counterexamples
- `ONE_OFF_EVENT_DEMAND`: 0 positives, 2 counterexamples

## Guardrails

- Benchmark/case labels are not candidate-generation input.
- Scoring modules do not import the case library.
- Missing evidence remains missing.
- No buy/sell wording is generated.
- Final score changes are deferred until case coverage is strong enough.

## Next Step

Use the case coverage report to decide which archetypes need more historical
examples before implementing final sector-aware score weights.

Recommended next data additions:

- at least one more poor-quality contract/backlog counterexample
- K-food export counterexamples such as one-product fad or channel inventory
- K-beauty counterexamples with channel stuffing or receivables risk
- memory/HBM counterexamples where price rally lacked revision support
- shipbuilding, auto, software, healthcare, financial, construction, and utility examples
