# Round-19 Deep Search Readiness

- source_round: `docs/round/r_19.md`
- raw_theme_tags: 208
- mapped_theme_tags: 208
- unmatched_theme_tags: 0
- ambiguous_theme_tags: 6
- theme_absorption_ready: true
- case_count: 108
- deep_search_targets: 25
- targets_needing_deep_search: 17
- targets_needing_price_validation: 8
- targets_ready_for_shadow_review: 0
- production_scoring_changed: false
- production_scoring_ready: false
- readiness_reason: `theme_absorption_ready_but_case_price_validation_incomplete`

## Interpretation
- 테마 흡수 구조는 동작한다. 예: `스테이블코인`도 검색/라우팅 태그로는 흡수된다.
- 하지만 점수는 테마명이 아니라 실제 증거에서 나와야 한다. 예: 규제 승인, 실제 거래량, 수익모델이 없으면 Green 근거가 아니다.
- 현재 단계는 shadow scoring과 case validation이다. Production StageClassifier/score weight는 변경하지 않는다.

## Priority Targets

| target | canonical | priority | positive | counter | price gaps | status | next step |
|---|---|---|---:|---:|---:|---|---|
| K_BEAUTY_OEM_ODM_EXPORT | K_BEAUTY_EXPORT_DISTRIBUTION | GREEN_VALIDATION | 4 | 4 | 7 | needs_price_path_validation | backfill_stage_prices_mfe_mae_before_shadow_weight_review |
| MEDICAL_DEVICE_EXPORT | MEDICAL_DEVICE_HEALTHCARE_EXPORT | GREEN_VALIDATION | 1 | 2 | 3 | needs_success_counterexample_deep_search | add_missing_success_or_counterexample_cases |
| CDMO_CONTRACT_UTILIZATION | CDMO_HEALTHCARE_CONTRACT | GREEN_VALIDATION | 3 | 3 | 6 | needs_price_path_validation | backfill_stage_prices_mfe_mae_before_shadow_weight_review |
| INSURANCE_UNDERWRITING_VALUEUP | FINANCIAL_SPREAD_BALANCE_SHEET | GREEN_VALIDATION | 0 | 2 | 2 | needs_success_counterexample_deep_search | add_missing_success_or_counterexample_cases |
| AI_DATA_CENTER_POWER_GRID | AI_DATA_CENTER_INFRASTRUCTURE | GREEN_VALIDATION | 2 | 1 | 3 | needs_success_counterexample_deep_search | add_missing_success_or_counterexample_cases |
| SEMI_EQUIPMENT_PCB | SEMI_EQUIPMENT_CAPEX | GREEN_VALIDATION | 1 | 1 | 2 | needs_success_counterexample_deep_search | add_missing_success_or_counterexample_cases |
| BATTERY_EV_OVERHEAT_ESS_SHIFT | BATTERY_MATERIALS_CAPEX_OVERHEAT | REDTEAM_DEFENSE | 1 | 5 | 5 | needs_success_counterexample_deep_search | add_counterexamples_and_4b_4c_cases_first |
| CHEMICAL_SPREAD_OVERSUPPLY | COMMODITY_SPREAD | REDTEAM_DEFENSE | 2 | 4 | 6 | needs_price_path_validation | backfill_stage_prices_mfe_mae_before_shadow_weight_review |
| CONSTRUCTION_PF_CREDIT | CONSTRUCTION_REAL_ESTATE_CREDIT | REDTEAM_DEFENSE | 0 | 5 | 5 | needs_success_counterexample_deep_search | add_counterexamples_and_4b_4c_cases_first |
| SHIPPING_FREIGHT_BOOM_BUST | SHIPPING_FREIGHT_CYCLE | REDTEAM_DEFENSE | 1 | 1 | 1 | needs_success_counterexample_deep_search | add_counterexamples_and_4b_4c_cases_first |
| DIGITAL_ASSET_TOKENIZATION | THEME_VALUATION_OVERHEAT | REDTEAM_DEFENSE | 1 | 6 | 7 | needs_success_counterexample_deep_search | add_counterexamples_and_4b_4c_cases_first |
| ROBOTICS_REVENUE_CONVERSION | ROBOTICS_FACTORY_AUTOMATION | REDTEAM_DEFENSE | 0 | 2 | 2 | needs_success_counterexample_deep_search | add_counterexamples_and_4b_4c_cases_first |
| PLATFORM_GOVERNANCE_MONETIZATION | PLATFORM_SOFTWARE_INTERNET | REDTEAM_DEFENSE | 3 | 3 | 6 | needs_price_path_validation | backfill_stage_prices_mfe_mae_before_shadow_weight_review |
| WASTE_RECYCLING_ENVIRONMENT | UTILITIES_REGULATED_TARIFF | THIN_BACKFILL | 1 | 3 | 4 | needs_success_counterexample_deep_search | add_2_positive_and_2_counterexample_case_candidates |
| CRO_CLINICAL_SERVICE | CDMO_HEALTHCARE_CONTRACT | THIN_BACKFILL | 3 | 3 | 6 | needs_price_path_validation | backfill_stage_prices_mfe_mae_before_shadow_weight_review |
| DIGITAL_HEALTHCARE_AI | MEDICAL_DEVICE_HEALTHCARE_EXPORT | THIN_BACKFILL | 1 | 2 | 3 | needs_success_counterexample_deep_search | add_2_positive_and_2_counterexample_case_candidates |
| SECURITY_IDENTITY_DEEPFAKE | PLATFORM_SOFTWARE_INTERNET | THIN_BACKFILL | 3 | 3 | 6 | needs_price_path_validation | backfill_stage_prices_mfe_mae_before_shadow_weight_review |
| CLOUD_AI_SOFTWARE_INFRA | PLATFORM_SOFTWARE_INTERNET | THIN_BACKFILL | 3 | 3 | 6 | needs_price_path_validation | backfill_stage_prices_mfe_mae_before_shadow_weight_review |
| APPAREL_BRAND_OEM | EXPORT_RECURRING_CONSUMER | THIN_BACKFILL | 1 | 2 | 2 | needs_success_counterexample_deep_search | add_2_positive_and_2_counterexample_case_candidates |
| BUILDING_MATERIALS_CYCLE | CONSTRUCTION_REAL_ESTATE_CREDIT | THIN_BACKFILL | 0 | 5 | 5 | needs_success_counterexample_deep_search | add_2_positive_and_2_counterexample_case_candidates |
| REIT_DEVELOPMENT_TRUST | HOLDING_RESTRUCTURING_GOVERNANCE | THIN_BACKFILL | 0 | 3 | 3 | needs_success_counterexample_deep_search | add_2_positive_and_2_counterexample_case_candidates |
| RAIL_INFRASTRUCTURE | CONTRACT_BACKLOG_INDUSTRIAL | THIN_BACKFILL | 4 | 1 | 1 | needs_success_counterexample_deep_search | add_2_positive_and_2_counterexample_case_candidates |
| SERVICE_KIOSK_AUTOMATION | ROBOTICS_FACTORY_AUTOMATION | THIN_BACKFILL | 0 | 2 | 2 | needs_success_counterexample_deep_search | add_2_positive_and_2_counterexample_case_candidates |
| URBAN_AIR_DRONE | DEFENSE_GOVERNMENT_BACKLOG | THIN_BACKFILL | 2 | 1 | 3 | needs_success_counterexample_deep_search | add_2_positive_and_2_counterexample_case_candidates |
| POLICY_EVENT_DISASTER_THEMES | ONE_OFF_EVENT_DEMAND | EVENT_POLICY_GUARDRAIL | 0 | 3 | 2 | needs_price_path_validation | backfill_stage_prices_mfe_mae_before_shadow_weight_review |

## Research Loop
1. Audit unmatched/ambiguous theme tags.
2. Deep-search under-covered archetypes only.
3. Add success and counterexample cases with must-have/red-flag evidence.
4. Backfill stage-date price paths and MFE/MAE.
5. Run shadow score profiles and compare score-price alignment.
6. Recalibrate weak archetypes before any production scoring change.

## What Not To Change
- Do not lower Stage 3-Green thresholds to improve recall.
- Do not use raw theme tags as score evidence.
- Do not use case labels or benchmark labels as candidate-generation input.
- Do not fabricate OpenDART detail fields, report numbers, dates, or prices.
- Do not apply score_weight_profiles_v05 to production scoring yet.
