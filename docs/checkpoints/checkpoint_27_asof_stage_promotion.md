# Checkpoint 27: As-Of Evidence Bundle Merge and Stage Promotion

## Summary

Checkpoint 27 fixes the main replay scoring gap:

```text
Before:
web report evidence -> web-only FeatureEngineeringInput -> low confidence / Stage 0-1

After:
official price + official financials + official OpenDART disclosures
+ web reports/news/disclosures
+ report-derived consensus/revision proxy
-> merged FeatureEngineeringInput -> deterministic score -> StageClassifier
```

This does not change Stage 3-Green thresholds.

## Implemented

- `src/e2r/backtest/asof_evidence_bundle.py`
  - merges official price, financials, disclosures, web reports, web news, and report-derived consensus proxies.
- `src/e2r/research/report_consensus_proxy.py`
  - converts explicit FY1/FY2/FY3 report estimates into `ConsensusSnapshot`.
  - converts explicit target/EPS/OP/FCF revisions into `ConsensusRevision`.
  - does not invent missing revision fields.
- `src/e2r/stage_gate_diagnostics.py`
  - reports Stage 2 and Stage 3-Green gate failures.
- `src/e2r/backtest/asof_stage_promotion_autopsy.py`
  - creates candidate score, gate, and coverage reports.
- Parser coverage improvements:
  - contract amount / prior sales
  - contract duration
  - pricing power confirmation
  - lead-time mention
  - capacity constraint
  - one-off shortage risk
- `AsOfResearchReplay` now writes:
  - `web_only_stage`
  - `merged_stage`
  - `web_only_score`
  - `merged_score`
  - `promotion_delta`

## Monthly Replay Result

Command run:

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
- date-verified docs: 646
- docs rejected after as-of date: 49
- discovered candidates: 120
- Stage 2 count: 22
- Stage 3-Green count: 0
- Stage 3-Yellow count: 0
- Stage 3-Red count: 0

## Structural Labels

Promoted after merged scoring:

- HD현대일렉트릭: Stage 2
- 일진전기: Stage 2

Still Stage 1:

- 효성중공업: Stage 2 total score still short
- 산일전기: Stage 2 total score still short
- 삼양식품: Stage 2 total score still short
- 한화에어로스페이스: Stage 2 total and EPS/FCF gates still short

Still Stage 0 / weak evidence:

- 실리콘투

Cyclical memory labels:

- 삼성전자 and SK하이닉스 reached Stage 1, but failed valuation and information-confidence gates.

## Safety Checks

- Unsafe one-off / overheat Stage 3-Green count: 0
- Red Team hard blocks in autopsy sample: 0
- Parser audit hard blocks in autopsy sample: 0
- Benchmark labels are still evaluation-only and not used as scoring input.
- Stage 3-Green remains strict.

## Interpretation

This is progress, not final validation.

Example:

- HD현대일렉트릭 went from web-only Stage 1 to merged Stage 2 because official price, actuals, disclosure, report, consensus proxy, and revision proxy now appear together.
- It does not become Green because Green requires much stronger visibility/bottleneck/contract-quality evidence than the current fixture text provides.

## Remaining Before Weekly Replay

- Add richer historical official/detail disclosure snapshots.
- Add more report/news snapshots for cases that remain Stage 1.
- Improve scoring only where explicit evidence is parsed but not yet used.
- Keep Green strict; improve Layer-1 and Stage 2 recall first.
