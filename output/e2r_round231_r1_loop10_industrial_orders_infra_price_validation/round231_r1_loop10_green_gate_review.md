# Round 231 R1 Green Gate Review

Do not apply these weights to production scoring yet.

R1 Stage 3-Green means order -> delivery -> revenue -> margin -> EPS/FCF. A contract headline alone is not enough.

## Required Fields

- confirmed_contract_amount
- contract_duration_or_delivery_schedule
- actual_delivery_or_revenue_recognition
- opm_eps_or_fcf_revision
- backlog_quality
- cashflow_or_working_capital_passed
- geopolitical_financing_dilution_risk_passed
- price_path_after_evidence

## Forbidden Patterns

- contract_headline_only
- policy_or_mou_without_funded_order
- record_high_policy_event
- unknown_margin
- epc_cash_collection_unknown
- local_production_economics_unknown
- geopolitical_sanction_unpriced
- dilution_after_rerating_ignored

## Easy Example
- `K2 delivery + revenue + OP revision + price reaction` can become a Stage 3 candidate.
- `$312M transformer contract + event-day price -5.4%` stays Stage 2 watch until margin/FCF confirm.
- `MASGA merger record high` is 4B-watch until funded orders and margin appear.
