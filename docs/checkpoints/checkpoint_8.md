# Checkpoint 8 Report

## Files Changed

- `AGENTS.md`
- `src/e2r/models.py`
- `src/e2r/scoring.py`
- `src/e2r/features.py`
- `src/e2r/connectors.py`
- `src/e2r/red_team.py`
- `src/e2r/staging.py`
- `src/e2r/__init__.py`
- `fixtures/historical/*`
- `tests/test_features.py`
- `tests/test_connectors.py`
- `tests/test_fixtures.py`
- `tests/test_red_team.py`
- `tests/test_staging.py`

## What Was Implemented

- Added durable repo instructions in `AGENTS.md`.
- Added `ShortageType`:
  - `none`
  - `one_off`
  - `cyclical`
  - `structural`
  - `unknown`
- Added explicit industrial sub-score model:
  - `contract_quality`
  - `backlog_rpo_visibility`
  - `capa_constraint`
  - `asp_pricing_power`
  - `structural_shortage`
  - `one_off_shortage_risk`

## Feature Engineering

Added `src/e2r/features.py` so the agent can build a score from raw domains instead of requiring hand-filled component scores.

The new path is:

```text
CSV/JSON or connector raw data
-> FeatureEngineeringInput
-> DeterministicFeatureEngineer
-> ScoringPayload
-> DeterministicScorer
-> StageClassifier
```

Example:

```text
order_backlog_to_sales=1.55
capa_utilization_pct=96
asp_yoy_pct=15
shortage_type=structural
target_price_revision_1m=21
```

becomes:

```text
backlog_rpo_visibility > 0
capa_constraint > 0
asp_pricing_power > 0
structural_shortage > one_off_shortage_risk
revision_score >= Stage 3-Green threshold
```

The feature engineer still uses deterministic rules only. It does not call live APIs and does not hardcode historical winner names.

## File Connectors

Added `CSVJSONDataConnector.from_directory(...)`.

Supported fallback files:

```text
instruments.csv/json
prices.csv/json
financial_actuals.csv/json
consensus.csv/json
consensus_revisions.csv/json
disclosures.csv/json
research_reports.csv/json
news.csv/json
```

CSV columns that are not direct model fields are preserved into `parsed_fields`. This lets fixture files carry research-style raw signals such as:

```text
contract_duration_months
prepayment_exists
rpo_to_sales
capa_locked_years
asp_yoy_pct
one_off_shortage_risk
```

## Historical Fixtures

Added file-backed historical fixtures for:

- HD현대일렉트릭
- 효성중공업
- 일진전기
- 산일전기
- 삼양식품
- NVIDIA
- Zoom
- 씨젠
- SMCI

These fixtures are data inputs only. The scoring, staging, Red Team, and backtest logic do not branch on those names or tickers.

## Stage Changes

- Kept the canonical Stage enum unchanged.
- Tightened Stage 3-Green:
  - `revision_score` must now meet a meaningful threshold, not merely be greater than zero.
  - weak `contract_quality` and high `one_off_shortage_risk` block Green.
- Split Stage 4B diagnostics without changing the Stage enum:
  - `4B-watch`
  - `4B-elevated`
  - `4B-graduated`

## Tests Added

- Structural shortage scores above one-off shortage.
- Strong EPS/FCF with weak contract quality is not Stage 3-Green.
- Stage 3-Green requires meaningful revision evidence.
- 4B status splits into watch, elevated, and graduated.
- Boom-bust cases still trigger 4B before 4C.
- CSV/JSON historical fixture data can produce a score without manual component injection.
- Financial actual rows with future `as_of_date` are filtered/rejected even if `reported_at` is old.
- News rows with future parsed `as_of_date` are filtered by connectors.

## Verification

```text
PYTHONPATH=src python -m unittest discover -s tests -v
Ran 56 tests
OK
```

Subagent review found two point-in-time gaps after the first implementation:

- `financial_actuals` needed `item.as_of_date <= query as_of_date` filtering.
- `news` needed `item.as_of_date <= query as_of_date` filtering.

Both were fixed and covered by regression tests.

## Guardrails Preserved

- No live web scraping was added.
- `as_of_date` point-in-time validation remains in models, connectors, feature engineering, staging, and backtesting.
- Historical names are fixture data only, not scoring logic.
- Morning briefing still rejects direct recommendation wording.
