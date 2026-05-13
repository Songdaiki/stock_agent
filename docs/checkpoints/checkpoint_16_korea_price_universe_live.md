# Checkpoint 16 Korea Price/Universe Live Execution Report

## Scope

Checkpoint 16 adds a controlled live execution path for Korea universe and price data through the free data.go.kr Financial Services Commission APIs.

The goal is simple:

```text
data.go.kr listed item response
-> Instrument

data.go.kr stock price response
-> PriceBar

Instrument + PriceBar
-> KoreaCheapScanner candidate
```

Fixture mode is still the default. Tests use mocked HTTP and do not call the real network.

## Added Components

- `src/e2r/cheap_scan/korea_sources.py`
  - paginated listed-item request builder
  - bulk stock-price date-window request builder
  - data.go.kr row normalizers for `Instrument` and `PriceBar`

- `src/e2r/pipeline/korea_live_lite.py`
  - data.go.kr live execution path
  - raw JSON cache path under `data/cache/data_go_kr/YYYY-MM-DD/`
  - `source_modes.data_go_kr = live_executed` when mocked/live responses succeed
  - explicit fallback reasons when budget or response failures prevent live use

- `tests/test_korea_live_lite.py`
  - mocked listed item response becomes a cheap-scan instrument
  - mocked stock price response becomes a price signal
  - data.go.kr source mode becomes `live_executed`
  - API keys are not written to run logs
  - budget-too-small path falls back before calls
  - failed response path falls back clearly

## Live Path

The implemented free path uses:

```text
GetKrxListedInfoService/getItemInfo
GetStockSecuritiesInfoService/getStockPriceInfo
```

The runner executes them as bulk/page requests:

```text
listed items page
stock prices for beginBasDt/endBasDt page
```

It does not call the price endpoint once per symbol.

Example:

```text
1 listed-item call + 1 stock-price call
-> rows for many symbols
-> local filtering inside KoreaCheapScanner
```

## Source Modes

`run_log.json` now distinguishes Korea price/universe source state:

```text
data_go_kr = fixture | live_executed | fallback | request_only
krx        = fixture | request_only | fallback
```

In this checkpoint:

```text
DATA_GO_KR_SERVICE_KEY present + live_enabled=True + mocked/live response ok
-> source_modes.data_go_kr = live_executed

DATA_GO_KR_SERVICE_KEY present + response fails
-> source_modes.data_go_kr = fallback

fixture_mode=True
-> source_modes.data_go_kr = fixture
```

KRX remains request-only until a dedicated KRX live executor is wired in.

## Cache

Raw data.go.kr JSON is cached under:

```text
data/cache/data_go_kr/YYYY-MM-DD/listed_items_page_0001.json
data/cache/data_go_kr/YYYY-MM-DD/stock_prices_page_0001.json
```

API keys are attached only to the live request sent to the HTTP client. Serialized `built_requests` keep credential metadata but do not include the secret value.

## Budget Behavior

The pilot requires at least two data.go.kr calls:

```text
1. listed items
2. stock prices
```

If `max_data_go_kr_calls_per_day < 2`, it falls back before making data.go.kr requests.

This avoids a half-live state where the universe is live but prices are missing.

## Tests

The checkpoint tests prove:

- listed-item JSON normalizes into an `Instrument`
- stock-price JSON normalizes into a `PriceBar`
- the resulting live symbol can become a price-driven cheap-scan candidate
- source mode is `live_executed` for successful mocked data.go.kr calls
- response failure is recorded as fallback
- too-small data.go.kr budget is respected
- secrets such as `DATA_GO_KR_SERVICE_KEY` are not written to `run_log.json`

No test makes a real network call.

## Guardrails

- Fixture mode remains default.
- Live mode is explicit.
- No paid data dependency was added.
- No per-symbol daily price calls were added.
- `as_of_date` filtering is preserved.
- Output remains E2R monitoring context, not buy/sell wording.
