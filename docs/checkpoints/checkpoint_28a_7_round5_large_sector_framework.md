# Checkpoint 28A-7: Round 5 Large-Sector Framework

## Summary

Round 5 was applied as research/calibration material only. Production scoring
and StageClassifier thresholds were not changed.

The analyst note in `docs/round/round_05.md` was converted into a ten-bucket
large-sector framework:

```text
대섹터 -> E2R Archetype -> Stage evidence -> peer normalization
```

Easy example:

```text
해운은 운임 급등으로 EPS가 커질 수 있다.
하지만 사이클 정상화가 빠르기 때문에 Green은 제한하고 4B/4C 감시가 중요하다.

전력기기는 계약질, 수주잔고, 리드타임, OPM, EPS revision이 같이 있으면 Green 후보가 될 수 있다.
```

## Implemented Files

- `src/e2r/sector/round5_large_sector_framework.py`
- `src/e2r/cli/build_round5_large_sector_report.py`
- `tests/test_round5_large_sector_framework.py`
- `docs/e2r_large_sector_framework_round5.md`
- `output/e2r_round5_large_sector_framework/round5_large_sector_framework.md`
- `output/e2r_round5_large_sector_framework/round5_archetype_large_sector_matrix.csv`
- `output/e2r_round5_large_sector_framework/round5_green_permission_matrix.md`
- `output/e2r_round5_large_sector_framework/round5_case_coverage_by_large_sector.csv`
- `output/e2r_round5_large_sector_framework/round5_next_case_expansion_plan.md`

## Ten Large Sectors

- `INDUSTRIAL_ORDERS`: 산업재/수주
- `EXPORT_CONSUMER`: 수출 소비재
- `SEMICONDUCTOR_AI_INFRA`: 반도체/AI 인프라
- `CYCLICAL_SPREAD`: 사이클/스프레드
- `FINANCIAL_CAPITAL_ALLOCATION`: 금융/자본배분
- `BIOTECH_HEALTHCARE`: 바이오/헬스케어
- `PLATFORM_IP_SERVICES`: 플랫폼/IP/서비스
- `DOMESTIC_REOPENING`: 내수/리오프닝
- `REAL_ESTATE_CREDIT_REGULATED`: 부동산/신용/규제자산
- `THEME_EVENT_GUARDRAIL`: 테마/이벤트

## New Or Confirmed Archetypes

- `AI_DATA_CENTER_INFRASTRUCTURE`
- `NUCLEAR_SMR_GRID_POLICY`
- `TRAVEL_LEISURE_REOPENING`
- `EDUCATION_SPECIALTY_SERVICES`
- `RARE_METALS_STRATEGIC_MATERIALS`
- `CDMO_HEALTHCARE_CONTRACT`
- `VALUE_UP_SHAREHOLDER_RETURN`

## Current Output

The Round 5 report shows the framework is ready, but case alignment and price
backfill are still incomplete. That means it should guide case mining and
shadow-score design, not production scoring.

## What Not To Change

- Do not lower Stage 3-Green thresholds.
- Do not use large-sector labels as candidate-generation input.
- Do not treat event premium as true structural rerating.
- Do not apply score weights until case and price-path coverage are filled.

## Verification

Commands run:

```bash
PYTHONPATH=src python -m unittest tests.test_round5_large_sector_framework -v
PYTHONPATH=src python -m e2r.cli.build_round5_large_sector_report --cases data/e2r_case_library/cases_v02.jsonl --output-directory output/e2r_round5_large_sector_framework
```

Full test run was executed after the patch before commit.
