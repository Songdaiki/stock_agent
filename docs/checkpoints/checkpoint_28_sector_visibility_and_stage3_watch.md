# Checkpoint 28: Sector Visibility and Stage 3 Watch

## What Changed

Checkpoint 28 replaced the universal contract-centric Stage 3 visibility gate with sector-aware structural visibility.

The key change is:

- before: every sector effectively needed strong `contract_quality`
- now: every sector needs strong `structural_visibility_quality`

For example:

- transformer/defense cases still need contracts, backlog, delivery visibility, lead time, CAPA, ASP, and shortage evidence.
- K-food/K-beauty cases can use export/channel expansion, recurring demand, OPM expansion, FY1/FY2 growth, and pricing power.
- memory/HBM cases can use HBM demand, memory price increases, supply discipline, capacity bottlenecks, and medium-term revisions.

No benchmark labels are used as scoring input.

## New Code

- `src/e2r/sector_profiles.py`
- sector-aware metrics in `src/e2r/features.py`
- sector-aware Stage diagnostics in `src/e2r/stage_gate_diagnostics.py`
- `promotion_band` diagnostic output in as-of replay/autopsy
- report-derived consensus proxies now flow through `FreeWebResearchRunner`

## Parser Improvements

The parser now captures explicit qualitative evidence such as:

- lead time extension
- supply shortage mention
- structural shortage mention
- export/channel expansion
- recurring consumer demand
- high-margin mix improvement
- ASP/pricing power
- HBM demand
- memory price increase
- supply discipline
- government customer
- multi-year contract

These are bounded qualitative credits. They do not invent numbers.

## Evidence Snapshots Added

Added reconstructed/as-of report fixtures for:

- 실리콘투
- 삼성전자 memory rerating
- SK하이닉스 memory rerating

These are source fixtures, not benchmark labels.

## Test Result

Command:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Result:

```text
Ran 243 tests
OK
```

## Replay Result

Command:

```bash
PYTHONPATH=src python -m e2r.cli.run_asof_research_replay \
  --start-date 2023-01-01 \
  --end-date 2026-05-14 \
  --frequency monthly \
  --market KR \
  --max-candidates-per-date 50 \
  --max-web-research-candidates-per-date 20 \
  --max-queries-per-candidate 8 \
  --max-results-per-query 5 \
  --require-date-verified-for-green \
  --allow-undated-docs-for-yellow-only \
  --save-reconstructed-snapshots \
  --output-directory output/backtests/asof_research_replay
```

Output:

- replay dates: 41
- universe rows scanned: 514
- Layer-1 candidates: 120
- web researched candidates: 120
- date verified documents: 860
- documents rejected after as_of_date: 25
- discovered candidates: 120
- Stage 2: 60
- Stage 3-Green: 0
- Stage 3-Yellow: 0
- Stage 3-Red: 0

## Autopsy Result

Command:

```bash
PYTHONPATH=src python -m e2r.cli.analyze_asof_stage_promotion \
  --asof-output output/backtests/asof_research_replay/2023-01-01_to_2026-05-14 \
  --output-directory output/backtests/asof_stage_promotion_autopsy \
  --official-root data/historical_official \
  --search-snapshot-root data/search_snapshots \
  --report-snapshot-root data/report_snapshots \
  --top-candidates 80 \
  --report-date 2026-05-14
```

Headline:

- candidates analyzed: 82
- Stage 2: 45
- Stage 3-Green: 0
- Stage 3-Yellow: 0
- Stage 3-Red: 0

## Benchmark Answers

HD현대일렉트릭:

- moved to Stage 2 / `Stage 2-High`
- still blocked by Stage 3 total score, bottleneck, and contract-quality gate

효성중공업:

- moved to Stage 2 / `Stage 2-High`
- still blocked by Stage 3 total score, visibility, bottleneck, and contract-quality gate

일진전기:

- moved to Stage 2 / `Stage 2-High`
- still blocked by Stage 3 total score, bottleneck, contract-quality, and sector-bottleneck evidence

삼양식품:

- improved through K-food profile
- still Stage 1 with score near Stage 2 threshold
- blocked mainly by total score and Stage 3 visibility/bottleneck/mispricing gates

산일전기:

- remains Stage 1
- needs stronger visibility/contract/bottleneck evidence

한화에어로스페이스:

- remains Stage 1
- structural defense visibility is present, but EPS/FCF evidence is still insufficient

실리콘투:

- now receives K-beauty/export evidence
- remains Stage 1 because EPS/FCF score and total score are still too low

삼성전자/SK하이닉스 memory:

- now receive memory/HBM-specific evidence
- both reach Stage 2 / `Stage 2-High`
- still blocked by total score, visibility, and bottleneck gates

Warning labels:

- unsafe one-off/overheat Green remains 0
- 에코프로비엠/대한전선-like stay contained

## What Still Blocks Green

The main Green blockers are still:

- total score below 85
- bottleneck/pricing component below 15
- sector-specific bottleneck evidence too thin
- contract-quality gate for power equipment and defense
- missing stronger official/financial evidence for some cases

This is acceptable for now. The checkpoint improves Stage 2 recall and diagnostic visibility without loosening Green.

## Next Step

The next useful patch is not to lower Green thresholds. It is to improve evidence coverage:

- add more verified report/disclosure details for power equipment contract quality
- add stronger financial actual/consensus evidence for K-food/K-beauty
- add memory-specific consensus/revision fixtures for Samsung/SK Hynix
- refine bottleneck scoring once more real evidence is available
