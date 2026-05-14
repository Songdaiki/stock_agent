# Korea API Probe Runbook

## Purpose

Run this before the full Korea live-lite flow.

The API probe does not try to find E2R candidates. It only checks what the approved APIs actually return.

Example:

```text
API docs say stock price has clpr
real response has CLPRC instead
-> probe catches missing clpr
-> update normalizer before running live-lite
```

This prevents the full agent from silently using wrong field assumptions.

## What The Probe Does

```text
tiny API request
-> raw response file
-> schema summary
-> expected-field comparison
-> normalizer dry-run
-> probe run log
```

It does not run:

```text
cheap scan
web deep research
E2R score
Stage classification
morning brief
```

## Fixture Probe

Use fixture mode first:

```bash
PYTHONPATH=src python -m e2r.cli.probe_korea_apis \
  --date 2026-05-14 \
  --fixture \
  --output-directory output/api_probe
```

This writes sample raw files and confirms the probe pipeline itself works.

## Live Probe

Set only the approved API keys you intend to test:

```bash
export OPENDART_API_KEY=...
export NAVER_CLIENT_ID=...
export NAVER_CLIENT_SECRET=...
export DATA_GO_KR_SERVICE_KEY=...
export KRX_OPENAPI_KEY=...
```

Then run:

```bash
PYTHONPATH=src python -m e2r.cli.probe_korea_apis \
  --date 2026-05-14 \
  --live \
  --sample-symbol 005930 \
  --output-directory output/api_probe
```

Skip sources if you are not ready to test them:

```bash
PYTHONPATH=src python -m e2r.cli.probe_korea_apis \
  --date 2026-05-14 \
  --live \
  --skip-krx \
  --sample-symbol 005930
```

## Output Files

For a run date:

```text
output/api_probe/YYYY-MM-DD/raw/
output/api_probe/YYYY-MM-DD/schema_summary.json
output/api_probe/YYYY-MM-DD/schema_summary.md
output/api_probe/YYYY-MM-DD/normalizer_report.json
output/api_probe/YYYY-MM-DD/normalizer_report.md
output/api_probe/YYYY-MM-DD/probe_run_log.json
```

Raw examples:

```text
raw/opendart_list.json
raw/naver_news.json
raw/naver_web.json
raw/naver_doc.json
raw/data_go_kr_listed_items.json
raw/data_go_kr_stock_prices.json
raw/data_go_kr_corp_basic.json
raw/data_go_kr_financial_stat.json
raw/data_go_kr_disclosure_info.json
raw/krx_stk_bydd_trd.json
raw/krx_ksq_bydd_trd.json
raw/krx_stk_isu_base_info.json
raw/krx_ksq_isu_base_info.json
raw/krx_kospi_dd_trd.json
raw/krx_kosdaq_dd_trd.json
```

## How To Read `schema_summary.md`

Look for:

```text
top_level_keys
selected_item_path
item_count
missing_expected_fields
field / types / samples table
```

Example:

```text
missing_expected_fields: clpr, trqu
```

Meaning:

```text
The stock-price normalizer expects closing price and volume fields,
but the raw response did not expose them under the expected names.
```

Fix the normalizer or expected-field aliases before running live-lite.

## How To Read `normalizer_report.md`

Look for:

```text
rows_seen
rows_normalized
failures
failure_examples
missing_expected_fields
```

Example:

```text
rows_seen = 1
rows_normalized = 0
failures = 1
failure_examples = ValueError:close must be positive
```

Meaning:

```text
The API returned a row, but our PriceBar conversion could not build a valid E2R model.
```

This is exactly what the probe is supposed to catch.

## How To Read `probe_run_log.json`

Check:

```text
source_modes
credentials_present
requests_attempted
requests_succeeded
requests_failed
cache_hits
cache_writes
rate_limit_waits
rate_limit_skips
failed_sources
skipped_sources
fallback_reasons
warnings
```

The credential values themselves are never written. The log only says whether each credential was present:

```json
{
  "credentials_present": {
    "DATA_GO_KR_SERVICE_KEY": true
  }
}
```

## What To Fix Before Tiny Smoke

Do not run the full live-lite flow until:

```text
1. raw files exist for the sources you plan to use
2. schema_summary has no unexpected missing fields for core rows
3. normalizer_report shows rows_normalized > 0 for:
   - listed items -> Instrument
   - stock prices -> PriceBar
   - disclosures -> DisclosureEvent
   - Naver rows -> SearchResult
4. probe_run_log has no failed source you rely on
```

For example:

```text
data_go_kr_stock_prices rows_normalized = 0
-> do not run KoreaLiveLiteRunner yet
-> update DataGoKrFSCConnector.normalize_price_bar first
```

## Why Probe Comes First

The live-lite runner assumes normalized rows are usable.

The probe checks the raw contract first:

```text
raw API response
-> schema OK
-> normalizer OK
-> then tiny live-lite smoke
```

This is safer than discovering field mismatches after a full scan has already produced candidates.
