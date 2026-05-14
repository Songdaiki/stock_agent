# E2R_STANDARD Flow

`E2R_STANDARD` is the canonical production flow.

It is the path that live runs and serious blind backtests should use.

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

Simple example:

```text
OpenDART finds 단일판매·공급계약체결
-> detail parser extracts amount/duration if available
-> Report Radar searches "수주잔고 OPM PDF"
-> evidence becomes feature input
-> deterministic StageClassifier decides Stage
-> LLM may explain, but cannot override Stage
```

## Production vs Diagnostic

Production flow:

```text
E2R_STANDARD
```

Diagnostic replay modes:

```text
official_only
case_fixture
hybrid
```

Diagnostic modes are useful for evidence coverage and regression tests, but they are not production flow.

## Blind Discovery Rule

Blind discovery tests must use `E2R_STANDARD`.

Benchmark labels are never input evidence.

Example:

```text
Wrong:
known winner label -> candidate generation

Correct:
E2R_STANDARD output -> compare against benchmark labels afterward
```

## LLM Role

The LLM layer is optional.

Allowed:

```text
query expansion
document extraction review
contradiction flags
Korean stage explanation
```

Not allowed:

```text
final Stage decision
score override
invent missing contract amount or EPS
buy/sell wording
```

The deterministic score and StageClassifier remain the source of truth.
