# Checkpoint 17 Run Review And Parser Audit Report

## Scope

Checkpoint 17 adds the operational quality loop before full Korea live-lite shadow running.

The new flow is:

```text
run live-lite
-> write candidates/evidence/brief/run_log
-> audit parsed evidence
-> block unsafe Stage 3-Green
-> review the run summary from CLI
-> plan OpenDART detail fetches for important disclosures
```

Simple example:

```text
report parser reads "계약 매출액 대비 600%"
-> parser audit marks contract_ratio_too_high as hard
-> affected Stage 3-Green is downgraded to Stage 3-Yellow
-> run_log records manual_review_required
```

## Added Components

- `src/e2r/audit/parser_audit.py`
  - `AuditFinding`
  - `audit_parser_outputs`
  - sanity checks for parsed ratios, valuation fields, OPM, confidence, and Green-stage evidence quality

- `src/e2r/cli/review_korea_run.py`
  - reads one Korea live-lite output bundle
  - summarizes candidates, source modes, live request stats, skipped reasons, dropped reasons, low-confidence evidence, and manual-review items

- `src/e2r/pipeline/korea_live_lite.py`
  - runs parser audit before final output
  - writes `audit_findings` into `run_log.json`
  - blocks unsafe Stage 3-Green when hard audit findings exist
  - plans OpenDART disclosure detail requests without executing them

- `src/e2r/sources/opendart.py`
  - adds disclosure detail request metadata builder for `document.xml`

## Parser Audit Rules

The audit flags abnormal parsed fields:

```text
contract_amount_to_prior_sales > 5.0
contract_duration_months > 120
opm > 80
est_per < 1 or est_per > 300
est_pbr < 0.1 or est_pbr > 50
target_revision_pct > 300
fifty_two_week_low > current_price
parser_confidence < 0.5
contract_quality exists but contract amount/duration is missing
Stage 3-Green has only low-confidence evidence
```

Findings use:

```text
severity = info | warning | hard
suggested_action = allow | downgrade_to_yellow | manual_review | block_green
```

Current hard findings block Stage 3-Green by downgrading affected symbols to Stage 3-Yellow with grade `parser-audit-blocked`.

## Run Review CLI

Run:

```bash
PYTHONPATH=src python -m e2r.cli.review_korea_run 2024-05-21 --output-directory output
```

It reads:

```text
YYYY-MM-DD_candidates.json
YYYY-MM-DD_evidence.json
YYYY-MM-DD_brief.md
YYYY-MM-DD_run_log.json
```

It prints:

```text
total candidates
event_search count
deep_research count
Stage distribution if present in the brief
source_modes
live request counts
cache stats
missing credentials
top skipped reasons
top dropped-result reasons
low-confidence evidence
manual-review items
```

## OpenDART Detail Fetch Planning

The runner now plans, but does not execute, detail requests for watch disclosures:

```text
단일판매·공급계약체결
신규시설투자
잠정실적
영업실적 전망
유상증자
전환사채
감사의견
거래정지
```

Planned requests are written to:

```text
run_log.planned_opendart_detail_requests
```

They point to:

```text
https://opendart.fss.or.kr/api/document.xml?rcept_no=...
```

No network call is made for these planned detail requests in this checkpoint.

## Tests

Tests prove:

- the review CLI summarizes fixture output
- impossible contract ratios are caught
- low parser confidence is caught
- hard audit findings block Stage 3-Green
- OpenDART detail requests are planned only for watch disclosures
- API keys are not written to run logs
- existing tests still pass

## Guardrails

- No real network calls in tests.
- No paid data dependency was added.
- API keys are not logged.
- Missing fields are not invented.
- `as_of_date` point-in-time filtering is preserved.
- Output remains E2R monitoring context, not buy/sell wording.
