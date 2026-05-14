# Checkpoint 23 Canonical Flow And Blind Discovery

## 1. Canonical E2R_STANDARD Flow

The canonical production flow is now named:

```text
E2R_STANDARD
```

It is implemented in:

```text
src/e2r/pipeline/e2r_standard_flow.py
```

Flow:

```text
Universe
-> official cheap scan
-> OpenDART detail fetch for watch disclosures
-> Report Radar
-> Free Web Research
-> Evidence Builder
-> Feature Engineering
-> optional LLM Evidence Analyst
-> Deterministic Score
-> StageClassifier
-> RedTeam
-> Parser Audit
-> Stage Lifecycle Monitor
-> Brief / Report
```

## 2. Diagnostic Modes Are Separated

These remain diagnostic only:

```text
official_only
case_fixture
hybrid
```

They are for evidence coverage checks, regression tests, and fixture replay.

They are not the default production flow.

Prominent warning:

```text
case_fixture success is regression success, not proof of live discovery.
```

## 3. Benchmark Labels Are Excluded From Pipeline Input

Benchmark labels live in:

```text
data/benchmark_labels/e2r_known_winners.json
src/e2r/backtest/benchmark_labels.py
```

They are evaluation-only.

Tests verify production modules do not import benchmark labels:

```text
E2R_STANDARD
cheap scan
features
staging
red_team
```

## 4. Blind Replay

Blind replay is implemented in:

```text
src/e2r/backtest/blind_discovery_replay.py
src/e2r/cli/run_blind_discovery_replay.py
```

It generates candidates first and applies labels afterward.

Example command:

```bash
PYTHONPATH=src python -m e2r.cli.run_blind_discovery_replay \
  --start-date 2023-01-01 \
  --end-date 2026-05-14 \
  --frequency monthly \
  --market KR \
  --flow E2R_STANDARD \
  --output-directory output/backtests/blind_discovery
```

## 5. Benchmark Label Output

The benchmark recall report answers whether labels such as:

```text
HD현대일렉트릭
효성중공업
일진전기
산일전기
삼양식품
한화에어로스페이스
실리콘투
삼성전자 메모리 리레이팅
SK하이닉스 메모리 리레이팅
씨젠
SMCI
에코프로비엠
HMM
대한전선-like
```

appeared in candidates.

Missing labels report why:

```text
source_missing_or_not_in_universe
no_report_snapshot
not_in_universe
unknown
```

## 6. LLM Research Analyst Layer

Added:

```text
src/e2r/llm/
docs/llm_research_analyst_layer.md
```

Allowed:

```text
query expansion
document extraction review
contradiction flags
Korean deterministic Stage explanation
```

Not allowed:

```text
override deterministic Stage
invent missing fields
produce buy/sell wording
```

FakeLLMProvider is used in tests.

## 7. 4A/4B/4C Detector

Added:

```text
src/e2r/backtest/stage_lifecycle_detector.py
docs/stage_lifecycle_detection.md
```

It distinguishes:

```text
4A ongoing
price_only_4b_watch
4B-watch / 4B-elevated / 4B-graduated
hard 4C
```

Important:

```text
price-only warning is not full 4B
missing evidence stays unknown
```

## 8. Snapshot Stores

Added:

```text
src/e2r/research/search_snapshot_store.py
src/e2r/research/report_snapshot_store.py
docs/search_snapshot_policy.md
```

Future live runs can store search results and fetched document hashes so future backtests become genuinely point-in-time.

## 9. Remaining Work Before True Large-Scale Blind Backtest

Still needed:

```text
more archived historical search snapshots
more report/news document snapshots
more official historical disclosure detail rows
more 4B evidence fixtures
weekly blind replay after monthly sanity passes
```

Do not loosen Stage 3-Green thresholds just to improve recall.
Layer 1 should improve recall; Stage 3-Green should preserve precision.
