# Checkpoint 17 Rate Limit And Smoke Safety Report

## Scope

This checkpoint adds live-call safety before broader Korea live-lite pilots.

The goal is:

```text
live_enabled=True
-> source-level rate limiter
-> serial HTTP calls by default
-> smoke preset budgets
-> run_log rate-limit diagnostics
```

Simple example:

```text
OpenDART min interval = 0.2 seconds
two OpenDART calls happen back to back
-> HttpClient sleeps before the second request
-> run_log.rate_limit_waits increments
```

## Added Components

- `src/e2r/sources/rate_limit.py`
  - `SourceRateLimit`
  - `RateLimitState`
  - `RateLimitDecision`
  - `RateLimiter`
  - request-to-source mapping helper

- `src/e2r/sources/http_client.py`
  - consults `RateLimiter` before live requests
  - returns `HttpResult(ok=False, error="rate_limit_exceeded")` when blocked
  - records rate-limit waits and skips
  - records actual HTTP requests by source
  - records logical queries by source
  - records max concurrency used by source

- `src/e2r/pipeline/korea_live_lite.py`
  - live-lite default rate limits
  - serial live execution fields
  - smoke presets
  - extended run log diagnostics

## Default Source Limits

Live-lite still uses the existing daily budgets:

```text
OpenDART: config.budget.max_opendart_calls_per_day
Naver Search: config.budget.max_naver_search_calls_per_day
KRX: config.budget.max_krx_calls_per_day
data.go.kr: config.budget.max_data_go_kr_calls_per_day
```

Source-level defaults start conservative:

```text
OpenDART: max_concurrency=1, min_interval_seconds=0.2
Naver Search: max_concurrency=1, min_interval_seconds=0.3
data.go.kr: max_concurrency=1, min_interval_seconds=0.2
KRX: max_concurrency=1, min_interval_seconds=0.2
```

This means broad parallel live execution is intentionally not enabled yet.

## Serial Default

New config fields:

```text
allow_parallel_live_requests = False
max_global_live_workers = 1
```

If `allow_parallel_live_requests=False`, `max_global_live_workers` must stay `1`.

This keeps early live pilots easy to reason about:

```text
one request
-> log it
-> rate-limit it
-> parse it
-> move to the next request
```

## Smoke Presets

Use:

```python
from datetime import date
from e2r.pipeline.korea_live_lite import KoreaLiveLiteConfig

config = KoreaLiveLiteConfig.smoke_preset("tiny", as_of_date=date.today())
```

Presets:

```text
tiny:
  universe_limit = 50
  max_naver_search_calls_per_day = 50
  event_search symbols = 5
  deep_research symbols = 1

small:
  universe_limit = 300
  max_naver_search_calls_per_day = 300
  event_search symbols = 30
  deep_research symbols = 5

standard_shadow:
  universe_limit = None
  max_naver_search_calls_per_day = 2000
  event_search symbols = 200
  deep_research symbols = 30
```

Fixture mode remains default. Live mode must still be explicit.

## Run Log

`run_log.json` now includes:

```text
rate_limit_waits
rate_limit_skips
actual_http_requests_by_source
logical_queries_by_source
max_concurrency_used_by_source
live_smoke_preset_used
```

Interpretation:

```text
rate_limit_waits > 0
-> requests were allowed, but delayed to respect source pacing

rate_limit_skips > 0
-> requests were blocked before network execution

max_concurrency_used_by_source.naver_search = 1
-> Naver Search stayed serial
```

## Tests

Tests prove:

- the rate limiter blocks after `max_requests_per_day`
- min interval sleeps use a fake sleep hook
- default source concurrency is `1`
- tiny smoke preset applies expected budget values
- run logs expose rate-limit fields
- API keys are still not written to run logs
- existing tests pass

## Guardrails

- No real network calls in tests.
- No paid API dependency was added.
- Fixture mode remains default.
- Live mode remains explicit.
- API keys are not logged.
- Bulk/date collection remains preferred over per-symbol live calls.
