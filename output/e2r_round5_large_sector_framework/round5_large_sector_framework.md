# Round-5 Large-Sector Framework

Source round: `docs/round/round_05.md`

This is calibration material. It does not change production scoring.

## Ten Large Sectors

| large_sector | Korean name | archetypes | Green permission |
|---|---|---:|---|
| INDUSTRIAL_ORDERS | 산업재/수주 | 4 | HIGH |
| EXPORT_CONSUMER | 수출 소비재 | 3 | HIGH |
| SEMICONDUCTOR_AI_INFRA | 반도체/AI 인프라 | 3 | HIGH |
| CYCLICAL_SPREAD | 사이클/스프레드 | 6 | LOW |
| FINANCIAL_CAPITAL_ALLOCATION | 금융/자본배분 | 4 | MEDIUM |
| BIOTECH_HEALTHCARE | 바이오/헬스케어 | 4 | LOW |
| PLATFORM_IP_SERVICES | 플랫폼/IP/서비스 | 3 | MEDIUM |
| DOMESTIC_REOPENING | 내수/리오프닝 | 2 | LOW |
| REAL_ESTATE_CREDIT_REGULATED | 부동산/신용/규제자산 | 2 | RESTRICTED |
| THEME_EVENT_GUARDRAIL | 테마/이벤트 | 4 | RESTRICTED |

## Why This Exists
- Full KOSPI/KOSDAQ coverage should not be tuned one narrow industry at a time.
- Large sectors define the evidence family before archetype-level score weights are tested.
- Example: shipping and diagnostics can show EPS explosions, but their Green posture is restricted because normalization risk is high.

## New Or Confirmed Extension Archetypes
- AI_DATA_CENTER_INFRASTRUCTURE: primary_large_sector=SEMICONDUCTOR_AI_INFRA
- NUCLEAR_SMR_GRID_POLICY: primary_large_sector=INDUSTRIAL_ORDERS
- TRAVEL_LEISURE_REOPENING: primary_large_sector=DOMESTIC_REOPENING
- EDUCATION_SPECIALTY_SERVICES: primary_large_sector=PLATFORM_IP_SERVICES
- RARE_METALS_STRATEGIC_MATERIALS: primary_large_sector=CYCLICAL_SPREAD
- CDMO_HEALTHCARE_CONTRACT: primary_large_sector=BIOTECH_HEALTHCARE
- VALUE_UP_SHAREHOLDER_RETURN: primary_large_sector=FINANCIAL_CAPITAL_ALLOCATION

## Guardrails
- Do not use large-sector labels as candidate-generation answers.
- Do not loosen Stage 3-Green thresholds from this report.
- Use this framework to decide which cases and price paths must be backfilled next.
